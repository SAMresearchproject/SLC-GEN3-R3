"""Typed native formula compilation to the installed HFM4 device grammar."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .exact import ExactError, fraction, integer, seal, token, vector

SCALE = 1_000_000
I32_MIN, I32_MAX = -(1 << 31), (1 << 31)-1
I64_MAX = (1 << 63)-1


def unit(value) -> tuple:
    powers = {}
    for name, exponent in value:
        name, exponent = token(name), integer(exponent)
        powers[name] = powers.get(name, 0)+exponent
    return tuple(sorted((name, exponent) for name, exponent in powers.items() if exponent))


def multiply_units(left, right) -> tuple:
    return unit(tuple(left)+tuple(right))


def fixed(value) -> int:
    value = fraction(value)*SCALE
    if value.denominator != 1:
        raise ExactError("value needs an explicit quantization adapter before device lowering")
    result = value.numerator
    if not I32_MIN <= result <= I32_MAX:
        raise ExactError("fixed-point operand exceeds signed i32")
    return result


def trunc_div(numerator: int, denominator: int) -> int:
    return (1 if numerator >= 0 else -1)*(abs(numerator)//denominator)


@dataclass(frozen=True)
class Operand:
    name: str
    values: tuple
    semantic_type: str
    unit: tuple
    normalization: str
    source_ref: str

    def __post_init__(self):
        for name in ("name", "semantic_type", "normalization", "source_ref"):
            token(getattr(self, name))
        if self.semantic_type in {"HELD_TARGET", "PRECOMPUTED_RESIDUAL", "RESULT_LABEL"}:
            raise ExactError("result or held target cannot be a formula source operand")
        object.__setattr__(self, "values", vector(self.values))
        object.__setattr__(self, "unit", unit(self.unit))


@dataclass(frozen=True)
class Formula:
    name: str
    terms: tuple
    output_type: str
    output_unit: tuple

    def __post_init__(self):
        token(self.name)
        token(self.output_type)
        terms = tuple((integer(index, minimum=0), fraction(coefficient), unit(coefficient_unit))
                      for index, coefficient, coefficient_unit in self.terms)
        if not 1 <= len(terms) <= 4:
            raise ExactError("device formula must contain one through four explicit source terms")
        object.__setattr__(self, "terms", terms)
        object.__setattr__(self, "output_unit", unit(self.output_unit))


def compile_formulas(operands, formulas) -> dict:
    operands, formulas = tuple(operands), tuple(formulas)
    if not operands or not formulas or any(not isinstance(x, Operand) for x in operands) or \
       any(not isinstance(x, Formula) for x in formulas):
        raise ExactError("typed source and formula rosters are required")
    if len({x.name for x in operands}) != len(operands) or len({x.name for x in formulas}) != len(formulas):
        raise ExactError("duplicate source or formula name")
    row_count = len(operands[0].values)
    if any(len(x.values) != row_count for x in operands):
        raise ExactError("source row rosters differ")
    features = [[fixed(value) for value in item.values] for item in operands]
    compiled, predictions = [], []
    for formula in formulas:
        for index, coefficient, coefficient_unit in formula.terms:
            if index >= len(operands):
                raise ExactError("formula source index is outside the roster")
            if multiply_units(coefficient_unit, operands[index].unit) != formula.output_unit:
                raise ExactError("coefficient and source units do not give the declared output")
        indices = [index for index, _, _ in formula.terms]
        coefficients = [fixed(coefficient) for _, coefficient, _ in formula.terms]
        bounds = [sum(abs(c*features[i][row]) for i, c in zip(indices, coefficients))
                  for row in range(row_count)]
        if any(bound > I64_MAX for bound in bounds):
            raise ExactError("formula intermediate exceeds signed i64")
        predicted = [trunc_div(sum(c*features[i][row] for i, c in zip(indices, coefficients)), SCALE)
                     for row in range(row_count)]
        # The installed HFM4 metric kernel accumulates signed-i64 squared error.
        if any(abs(value) > 0xffffffff for value in predicted) or \
           sum(value*value for value in predicted) > I64_MAX:
            raise ExactError("formula exceeds the installed exact metric accumulation range")
        compiled.append({"name": formula.name, "indices": indices+[0]*(4-len(indices)),
                         "coefficients": coefficients+[0]*(4-len(coefficients)), "intercept": 0,
                         "expression_size": 2*len(indices), "output_type": formula.output_type,
                         "output_unit": formula.output_unit})
        predictions.append(predicted)
    return seal("Q3_TYPED_FORMULA_COMPILATION_V1", operands=operands, formulas=formulas,
                compiled=compiled, source_features_fixed=features,
                exact_cpu_signed_predictions_fixed=predictions, scale=SCALE,
                row_count=row_count, formula_count=len(formulas),
                arithmetic="SIGNED_I64_SUM_THEN_TRUNCATE_TOWARD_ZERO",
                source_normalizations=[x.normalization for x in operands])


def explicit_payload(compilation: dict, *, run_id: str, start: int, stop: int) -> dict:
    from .exact import verify
    verify(compilation, "Q3_TYPED_FORMULA_COMPILATION_V1")
    start, stop = integer(start, minimum=0), integer(stop, minimum=1)
    if not start < stop <= compilation["formula_count"]:
        raise ExactError("formula shard bounds differ")
    rows = compilation["compiled"][start:stop]
    # HFM4's ceil partition and 24-row durable limit admit a complete 16-row
    # explicit shard. Other tails need a separate route, never invented work.
    if len(rows) != 16:
        raise ExactError("installed full-Ryzen explicit lane requires a 16-formula shard")
    return {"run_id": token(run_id), "mode": "explicit",
            "score_features_fixed": compilation["source_features_fixed"],
            "score_target_fixed": [0]*compilation["row_count"],
            "indices": [x["indices"] for x in rows],
            "coefficients": [x["coefficients"] for x in rows],
            "intercepts": [0]*len(rows), "expression_size": [x["expression_size"] for x in rows]}
