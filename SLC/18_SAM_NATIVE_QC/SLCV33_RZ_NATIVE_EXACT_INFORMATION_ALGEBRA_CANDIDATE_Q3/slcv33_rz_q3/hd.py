"""Q3 feature projections of canonical HD objects constructed by bound V6."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping

from .canonical import canonical_sha256
from .foundation import BOUND_HD_SCHEMA, UNDEFINED_QUOTIENT_SCHEMA, BoundV6Foundation


class HDError(ValueError):
    """A bound V6 HD serialization or Q3 projection is invalid."""


def _fraction_from_dict(value: object, label: str) -> Fraction:
    if not isinstance(value, Mapping) or set(value) != {"numerator", "denominator"}:
        raise HDError(f"{label} is not a canonical fraction")
    numerator, denominator = value["numerator"], value["denominator"]
    if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
        raise HDError(f"{label} is not an exact reduced fraction")
    result = Fraction(numerator, denominator)
    if result.numerator != numerator or result.denominator != denominator:
        raise HDError(f"{label} is not reduced")
    return result


def _verify_semantic(value: Mapping[str, Any]) -> None:
    semantic = value.get("semantic_sha256")
    if not isinstance(semantic, str):
        raise HDError("bound V6 projection lacks a semantic identity")
    body = dict(value)
    body.pop("semantic_sha256", None)
    if canonical_sha256(body) != semantic:
        raise HDError("bound V6 projection semantic identity differs")


@dataclass(frozen=True, slots=True)
class FactorProof:
    """Read-only projection of a V6 ``RationalFactorProof`` serialization."""

    numerator: int
    denominator: int
    numerator_factors: tuple[tuple[int, int], ...]
    denominator_factors: tuple[tuple[int, int], ...]
    complete: bool

    @property
    def valid(self) -> bool:
        return self.complete


def _factor_rows(value: object, label: str) -> tuple[tuple[int, int], ...]:
    if not isinstance(value, list):
        raise HDError(f"{label} is not a V6 factor roster")
    result: list[tuple[int, int]] = []
    for row in value:
        if not isinstance(row, Mapping) or set(row) != {"prime", "exponent"}:
            raise HDError(f"{label} has noncanonical fields")
        prime, exponent = row["prime"], row["exponent"]
        if type(prime) is not int or type(exponent) is not int or prime < 2 or exponent < 1:
            raise HDError(f"{label} has invalid exact integers")
        result.append((prime, exponent))
    return tuple(result)


@dataclass(frozen=True, slots=True)
class HDSigma:
    """Frozen-width Q3 coordinates projected from one strict V6 object."""

    variant: str
    sign: int = 0
    v2: int = 0
    v3: int = 0
    u: Fraction = Fraction(0)
    proof: FactorProof | None = None
    foundation_serialization: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.variant not in {"ZERO", "NONZERO", "UNDEFINED_QUOTIENT"}:
            raise HDError(f"unknown HD variant: {self.variant}")
        if self.foundation_serialization is None:
            raise HDError("Q3 HD coordinates require a bound V6 serialization")
        _verify_semantic(self.foundation_serialization)
        expected_schema = UNDEFINED_QUOTIENT_SCHEMA if self.undefined else BOUND_HD_SCHEMA
        if self.foundation_serialization.get("schema") != expected_schema:
            raise HDError("Q3 HD projection schema differs from its variant")
        if self.variant == "NONZERO":
            if self.sign not in {-1, 1} or self.u <= 0:
                raise HDError("NONZERO HD projection has invalid sign or residual")
            if self.u.numerator % 2 == 0 or self.u.denominator % 2 == 0:
                raise HDError("HD residual retains a factor of 2")
            if self.u.numerator % 3 == 0 or self.u.denominator % 3 == 0:
                raise HDError("HD residual retains a factor of 3")
            if self.proof is None or not self.proof.valid:
                raise HDError("NONZERO HD projection lacks its V6 factor proof")

    @property
    def zero(self) -> bool:
        return self.variant == "ZERO"

    @property
    def undefined(self) -> bool:
        return self.variant == "UNDEFINED_QUOTIENT"

    @property
    def exact_value(self) -> Fraction | None:
        if self.zero:
            return Fraction(0)
        if self.undefined:
            return None
        magnitude = self.u
        magnitude = magnitude * (2 ** self.v2) if self.v2 >= 0 else magnitude / (2 ** -self.v2)
        magnitude = magnitude * (3 ** self.v3) if self.v3 >= 0 else magnitude / (3 ** -self.v3)
        return self.sign * magnitude

    @property
    def semantic_sha256(self) -> str:
        assert self.foundation_serialization is not None
        return str(self.foundation_serialization["semantic_sha256"])

    def to_dict(self) -> dict[str, object]:
        body: dict[str, object] = {
            "variant": self.variant,
            "bound_v6_semantic_sha256": self.semantic_sha256,
        }
        if self.variant == "NONZERO":
            body.update({
                "sign": self.sign,
                "v2": self.v2,
                "v3": self.v3,
                "u": {"numerator": self.u.numerator, "denominator": self.u.denominator},
                "factor_proof_complete": self.proof.valid if self.proof else False,
            })
        return body


def project_bound_hd(value: Mapping[str, Any]) -> HDSigma:
    """Project a strict foundation serialization without originating algebra."""

    if not isinstance(value, Mapping):
        raise HDError("bound V6 HD projection input is not a mapping")
    _verify_semantic(value)
    if value.get("schema") == UNDEFINED_QUOTIENT_SCHEMA:
        if value.get("variant") != "UNDEFINED_QUOTIENT":
            raise HDError("undefined quotient wrapper differs")
        return HDSigma("UNDEFINED_QUOTIENT", foundation_serialization=dict(value))
    if value.get("schema") != BOUND_HD_SCHEMA:
        raise HDError("bound V6 HD object schema differs")
    signature = value.get("hd_signature")
    if not isinstance(signature, Mapping):
        raise HDError("bound V6 HD signature is absent")
    exact = _fraction_from_dict(value.get("exact_rational"), "exact_rational")
    if signature.get("variant") == "ZERO":
        if exact != 0 or value.get("bounded_factor_proof") is not None:
            raise HDError("bound V6 ZERO serialization differs")
        return HDSigma("ZERO", foundation_serialization=dict(value))
    if signature.get("variant") != "NONZERO":
        raise HDError("bound V6 HD signature variant differs")
    proof_row = value.get("bounded_factor_proof")
    if not isinstance(proof_row, Mapping) or proof_row.get("complete") is not True:
        raise HDError("bound V6 factor proof is absent or incomplete")
    proof_value = _fraction_from_dict(proof_row.get("value"), "factor proof value")
    if proof_value != exact:
        raise HDError("bound V6 factor proof value differs")
    proof = FactorProof(
        numerator=abs(exact.numerator),
        denominator=exact.denominator,
        numerator_factors=_factor_rows(proof_row.get("numerator_factors"), "numerator factors"),
        denominator_factors=_factor_rows(proof_row.get("denominator_factors"), "denominator factors"),
        complete=True,
    )
    result = HDSigma(
        "NONZERO",
        sign=signature.get("sign"),
        v2=signature.get("v2"),
        v3=signature.get("v3"),
        u=_fraction_from_dict(signature.get("coprime_cofactor"), "HD cofactor"),
        proof=proof,
        foundation_serialization=dict(value),
    )
    if result.exact_value != exact:
        raise HDError("Q3 HD projection does not reconstruct its V6 rational")
    return result


def sigma_hd(
    value: int | Fraction,
    foundation: BoundV6Foundation,
    *,
    source_provenance: str = "Q3_SOURCE_VISIBLE_HD_OBJECT",
) -> HDSigma:
    return project_bound_hd(foundation.serialize_hd(value, source_provenance=source_provenance))


def multiply_hd(
    left: HDSigma,
    right: HDSigma,
    foundation: BoundV6Foundation,
    *,
    source_provenance: str = "Q3_SOURCE_VISIBLE_HD_PRODUCT",
) -> HDSigma:
    if left.undefined or right.undefined:
        raise HDError("an undefined quotient cannot enter V6 HD multiplication")
    assert left.foundation_serialization is not None and right.foundation_serialization is not None
    result = project_bound_hd(foundation.hd_product(
        left.foundation_serialization,
        right.foundation_serialization,
        source_provenance=source_provenance,
    ))
    if result.exact_value != left.exact_value * right.exact_value:
        raise HDError("bound V6 HD product law differs")
    return result


def divide_hd(
    numerator: HDSigma,
    denominator: HDSigma,
    foundation: BoundV6Foundation,
    *,
    source_provenance: str = "Q3_SOURCE_VISIBLE_HD_QUOTIENT",
) -> HDSigma:
    if numerator.undefined or denominator.undefined:
        raise HDError("an undefined quotient cannot enter V6 HD division")
    assert numerator.foundation_serialization is not None and denominator.foundation_serialization is not None
    result = project_bound_hd(foundation.hd_quotient(
        numerator.foundation_serialization,
        denominator.foundation_serialization,
        source_provenance=source_provenance,
    ))
    if denominator.zero:
        if not result.undefined:
            raise HDError("bound V6 zero-denominator boundary differs")
    elif result.exact_value != numerator.exact_value / denominator.exact_value:
        raise HDError("bound V6 HD quotient law differs")
    return result


def base_feature_block(value: HDSigma) -> tuple[Fraction, ...]:
    if value.undefined:
        raise HDError("undefined quotient cannot enter a base HD block")
    if value.zero:
        return (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    return (
        Fraction(0), Fraction(value.sign), Fraction(value.v2), Fraction(value.v3),
        Fraction(value.u.numerator), Fraction(value.u.denominator),
    )


def relation_feature_block(value: HDSigma) -> tuple[Fraction, ...]:
    if value.undefined:
        return (Fraction(1),) + (Fraction(0),) * 6
    return (Fraction(0),) + base_feature_block(value)


def closure_feature_block(value: HDSigma) -> tuple[Fraction, ...]:
    if value.variant != "NONZERO":
        return (Fraction(0),) * 5
    a, b = value.v2, value.v3
    return tuple(Fraction(item) for item in (2 * a, 2 * a + b, a + 2 * b, b - a, 2 * b - 3 * a))


def structured_node_block(value: HDSigma) -> tuple[Fraction, ...]:
    return relation_feature_block(value) + closure_feature_block(value)


def law_receipt(left: HDSigma, right: HDSigma, foundation: BoundV6Foundation) -> dict[str, object]:
    product = multiply_hd(left, right, foundation)
    quotient = divide_hd(left, right, foundation)
    return {
        "foundation": "BOUND_V6_SNAPSHOT",
        "left_semantic_sha256": left.semantic_sha256,
        "right_semantic_sha256": right.semantic_sha256,
        "product_semantic_sha256": product.semantic_sha256,
        "quotient_semantic_sha256": quotient.semantic_sha256,
        "product_factor_proof_complete": product.zero or bool(product.proof and product.proof.valid),
        "quotient_factor_proof_complete_or_typed_undefined": (
            quotient.undefined or quotient.zero or bool(quotient.proof and quotient.proof.valid)
        ),
        "product_direct_equality": product.exact_value == left.exact_value * right.exact_value,
        "quotient_direct_equality": (
            quotient.undefined if right.zero else quotient.exact_value == left.exact_value / right.exact_value
        ),
    }


__all__ = (
    "FactorProof", "HDError", "HDSigma", "base_feature_block",
    "closure_feature_block", "divide_hd", "law_receipt", "multiply_hd",
    "project_bound_hd", "relation_feature_block", "sigma_hd", "structured_node_block",
)
