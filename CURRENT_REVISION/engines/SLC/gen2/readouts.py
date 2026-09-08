"""Exact source-defined readout compilation and conditional inverse strategies.

The six-axis and shell strategies implement prop4 equations (11)--(12).
Generic finite inverses preserve all admitted members, including aliases.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Mapping

from .exact import rational, canonical, digest
from .dependencies.native.quadratic import quadratic_change


def vec(values):
    return tuple(rational(x) for x in values)


def matrix(values, rows=None, columns=None, symmetric=False):
    result = tuple(vec(row) for row in values)
    n = len(result)
    m = len(result[0]) if n else 0
    if (rows is not None and n != rows) or (columns is not None and m != columns):
        raise ValueError("matrix dimensions differ from the declared source")
    if any(len(row) != m for row in result):
        raise ValueError("ragged matrix")
    if symmetric and (n != m or any(result[i][j] != result[j][i] for i in range(n) for j in range(i))):
        raise ValueError("source form must be symmetric")
    return result


def dot(left, right):
    if len(left) != len(right):
        raise ValueError("vector dimensions differ")
    return sum((x * y for x, y in zip(left, right)), Fraction())


def matvec(a, x):
    return tuple(dot(row, x) for row in a)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(dot(row, col) for col in bt) for row in a)


def quadratic_value(a, x):
    return dot(x, matvec(a, x))


def linear_inverse(coefficients, observed, *, domain=None):
    """All rational solutions, or all members of an explicitly supplied finite domain."""
    a = matrix(coefficients)
    y = vec(observed)
    if len(a) != len(y) or not a:
        raise ValueError("linear inverse requires one observed value per nonempty matrix row")
    width = len(a[0])
    if domain is not None:
        members = []
        examined = 0
        for candidate in domain:
            x = vec(candidate)
            if len(x) != width:
                raise ValueError("admitted domain dimension differs")
            examined += 1
            if matvec(a, x) == y:
                members.append(x)
        return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "FINITE_CONFIGURATION",
                          "complete": True, "unique": len(members) == 1,
                          "members": members, "member_count": len(members), "domain_count": examined})
    work = [list(row) + [rhs] for row, rhs in zip(a, y)]
    pivots = []
    r = 0
    for column in range(width):
        pivot = next((i for i in range(r, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        scale = work[r][column]
        work[r] = [x / scale for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][column]:
                scale = work[i][column]
                work[i] = [x - scale * z for x, z in zip(work[i], work[r])]
        pivots.append(column)
        r += 1
        if r == len(work):
            break
    inconsistent = any(not any(row[:width]) and row[-1] for row in work)
    if inconsistent:
        return {"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "EXACT_LINEAR", "complete": True,
                "unique": False, "member_count": 0, "members": []}
    particular = [Fraction()] * width
    for i, column in enumerate(pivots):
        particular[column] = work[i][-1]
    free = [i for i in range(width) if i not in pivots]
    basis = []
    for column in free:
        direction = [Fraction()] * width
        direction[column] = Fraction(1)
        for i, pivot in enumerate(pivots):
            direction[pivot] = -work[i][column]
        basis.append(direction)
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "EXACT_LINEAR",
                      "complete": True, "unique": not free,
                      "member_count": "INFINITE_RATIONAL_AFFINE_FAMILY" if free else 1,
                      "members": [particular] if not free else [], "particular": particular,
                      "nullspace_basis": basis, "free_coordinates": free,
                      "parameter_domain": "RATIONAL", "rank": len(pivots)})


def _native_value(value):
    """Convert the preserved native receiver's rational envelopes to this schema."""
    if isinstance(value, dict):
        if set(value) == {"rational"}:
            return Fraction(int(value["rational"][0]), int(value["rational"][1]))
        return {key: _native_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_native_value(item) for item in value]
    return value


@dataclass(frozen=True)
class PolynomialReadout:
    constant: Fraction
    linear: tuple
    quadratic: tuple
    output_unit: str = "NATIVE_SOURCE_ACTION"
    input_unit: str = "DIMENSIONLESS"
    normalization: str = "AS_SUPPLIED"

    @classmethod
    def from_dict(cls, source):
        c = vec(source["linear"])
        if not c:
            raise ValueError("a readout requires at least one input coordinate")
        a = matrix(source.get("quadratic", [[0] * len(c) for _ in c]), len(c), len(c), True)
        unit = source.get("output_unit", "NATIVE_SOURCE_ACTION")
        input_unit = source.get("input_unit", "DIMENSIONLESS")
        if not isinstance(unit, str) or not unit.strip() or not isinstance(input_unit, str) or not input_unit.strip():
            raise ValueError("readout units must be nonempty strings")
        return cls(rational(source.get("constant", 0)), c, a, unit, input_unit,
                   source.get("normalization", "AS_SUPPLIED"))

    def anchor_matrix(self):
        return ((self.constant,) + tuple(x / 2 for x in self.linear),) + tuple(
            (c / 2,) + row for c, row in zip(self.linear, self.quadratic))

    def evaluate(self, after, before=None):
        w1 = vec(after)
        if len(w1) != len(self.linear):
            raise ValueError("readout operand dimension differs")
        h1 = (Fraction(1),) + w1
        if before is None:
            h0 = (Fraction(),) * len(h1)
        else:
            w0 = vec(before)
            if len(w0) != len(w1):
                raise ValueError("readout before dimension differs")
            h0 = (Fraction(1),) + w0
        native = quadratic_change(h0, h1, self.anchor_matrix(), coefficient_unit=self.output_unit,
                                  source_unit=self.input_unit, normalization=self.normalization)
        values = _native_value(native)
        # The native receipt remains byte/semantic valid in its original envelope.
        return canonical({"schema": "GEN2_POLYNOMIAL_READOUT_V1", "value": values["energy_after"],
                          "before_value": values["energy_before"], "difference": values["signed_change"],
                          "self": values["current_self"], "cross": values["occupied_cross"],
                          "output_unit": self.output_unit, "input_unit": self.input_unit,
                          "normalization": self.normalization, "anchor_is_compiler_scalar": True,
                          "source": {"constant": self.constant, "linear": self.linear, "quadratic": self.quadratic},
                          "native_receipt": native})


SHELL_RADII = tuple(Fraction(2 * k + 3, 2) for k in range(6))
AXES = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def radial_readout(amounts, *, radii=SHELL_RADII, compact=False):
    w, r = vec(amounts), vec(radii)
    if len(w) != len(r) or not w or any(x <= 0 for x in r):
        raise ValueError("radial amounts and positive radii must match")
    running = Fraction()
    values = []
    for amount, radius in zip(w, r):
        running += amount
        values.append(running / radius)
    return tuple(values[:-1] if compact else values)


def radial_inverse(observed, *, radii=SHELL_RADII, total=None):
    y, r = vec(observed), vec(radii)
    if any(x <= 0 for x in r) or not r:
        raise ValueError("positive shell radii required")
    if len(y) not in (len(r), len(r) - 1):
        raise ValueError("full or one-short radial observation required")
    if len(y) < len(r) and total is None:
        raise ValueError("compact radial inverse requires supplied total or a finite admitted domain")
    accumulated = [radius * value for radius, value in zip(r, y)]
    if len(accumulated) < len(r):
        accumulated.append(rational(total))
    elif total is not None and accumulated[-1] != rational(total):
        return {"complete": True, "members": [], "member_count": 0, "unique": False}
    w = [accumulated[0]] + [b - a for a, b in zip(accumulated, accumulated[1:])]
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "RADIAL_ANALYTIC",
                      "complete": True, "unique": True, "member_count": 1, "members": [w]})


def angular_readout(amounts, *, directions=AXES):
    w = vec(amounts)
    directions = tuple(vec(row) for row in directions)
    if not w or len(w) != len(directions) or any(len(row) != 3 or dot(row, row) != 1 for row in directions):
        raise ValueError("one declared exact unit direction is required per amount")
    total = sum(w, Fraction())
    dipole = tuple(sum((a * row[k] for a, row in zip(w, directions)), Fraction()) for k in range(3))
    q = tuple(tuple(sum((a * (3 * row[k] * row[l] - int(k == l)) for a, row in zip(w, directions)), Fraction())
                    for l in range(3)) for k in range(3))
    return {"total": total, "dipole": dipole, "quadrupole": q,
            "power": (total * total, dot(dipole, dipole), sum((x * x for row in q for x in row), Fraction()))}


def six_axis_values(amounts, *, compact=False, power=False):
    if len(amounts) != 6:
        raise ValueError("six-axis strategy requires six amounts in (+x,-x,+y,-y,+z,-z) order")
    data = angular_readout(amounts)
    if power:
        return data["power"]
    diagonal = tuple(data["quadrupole"][k][k] for k in range(3))
    return data["dipole"] + diagonal[:2] if compact else (data["total"],) + data["dipole"] + diagonal


def angular_inverse(observed, *, total=None, compact=False):
    y = vec(observed)
    if compact:
        if len(y) != 5 or total is None:
            raise ValueError("compact angular inverse requires five coordinates and a supplied total")
        m, d, q = rational(total), y[:3], y[3:] + (-y[3] - y[4],)
    else:
        if len(y) != 7:
            raise ValueError("full six-axis observation requires M, three D and three Q coordinates")
        m, d, q = y[0], y[1:4], y[4:]
        if total is not None and m != rational(total):
            return {"complete": True, "unique": False, "member_count": 0, "members": []}
    if sum(q) != 0:
        return {"complete": True, "unique": False, "member_count": 0, "members": []}
    w = tuple(value for k in range(3) for value in (((q[k] + m) / 3 + d[k]) / 2,
                                                 ((q[k] + m) / 3 - d[k]) / 2))
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "SIX_AXIS_ANALYTIC",
                      "complete": True, "unique": True, "member_count": 1, "members": [w]})


def distribution_domain(total=6):
    return tuple(w for w in product(range(3), repeat=6) if total is None or sum(w) == total)


def standard_readout_forms():
    """The sixteen source-bound C/D outputs, lowered through native receivers."""
    forms = []
    for k, radius in enumerate(SHELL_RADII):
        forms.append(("radial_" + str(k), PolynomialReadout.from_dict({"linear": [Fraction(int(i <= k), 1) / radius for i in range(6)],
                      "output_unit": "NORMALIZED_RADIAL_READOUT"})))
    angular = [[1] * 6]
    angular.extend([[direction[k] for direction in AXES] for k in range(3)])
    angular.extend([[3 * direction[k] * direction[k] - 1 for direction in AXES] for k in range(3)])
    for name, coefficients in zip(("M", "D0", "D1", "D2", "Q0", "Q1", "Q2"), angular):
        forms.append((name, PolynomialReadout.from_dict({"linear": coefficients, "output_unit": "NORMALIZED_SIGNED_MOMENT"})))
    forms.append(("M2", PolynomialReadout.from_dict({"linear": [0] * 6, "quadratic": [[1] * 6 for _ in range(6)],
                  "output_unit": "NORMALIZED_ANGULAR_POWER"})))
    forms.append(("D2_power", PolynomialReadout.from_dict({"linear": [0] * 6, "quadratic": [[dot(a, b) for b in AXES] for a in AXES],
                  "output_unit": "NORMALIZED_ANGULAR_POWER"})))
    forms.append(("Q2_power", PolynomialReadout.from_dict({"linear": [0] * 6, "quadratic": [[9 * dot(a, b) ** 2 - 3 for b in AXES] for a in AXES],
                  "output_unit": "NORMALIZED_ANGULAR_POWER"})))
    return tuple(forms)


def _view(strategy, source, payload):
    if strategy in ("radial", "radial_compact"):
        return radial_readout(source, radii=payload.get("radii", SHELL_RADII), compact=strategy.endswith("compact"))
    if strategy in ("angular", "angular_compact", "angular_power"):
        return six_axis_values(source, compact=strategy.endswith("compact"), power=strategy.endswith("power"))
    raise ValueError("unregistered readout strategy")


def finite_readout_inverse(strategy, observed, domain, *, total=None, options=None):
    """Finite caller domain is an explicit condition, never guessed from observation."""
    y = vec(observed)
    matches, count = [], 0
    for source in domain:
        w = vec(source)
        count += 1
        if total is not None and sum(w) != rational(total):
            continue
        if _view(strategy, w, options or {}) == y:
            matches.append(w)
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "FINITE_CONFIGURATION",
                      "view": strategy, "complete": True, "unique": len(matches) == 1,
                      "members": matches, "member_count": len(matches), "domain_count": count,
                      "known_total": total})


def _dispatch_base(operation, payload):
    operation = operation.removeprefix("GEN2_")
    if operation == "READOUT":
        if payload.get("strategy", "polynomial") == "polynomial":
            return PolynomialReadout.from_dict(payload["source"]).evaluate(payload["after"], payload.get("before"))
        return canonical({"schema": "GEN2_READOUT_V1", "strategy": payload["strategy"],
                          "values": _view(payload["strategy"], payload["amounts"], payload),
                          "source_unit": payload.get("source_unit", "DECLARED_NORMALIZED_AMOUNT")})
    if operation == "READOUT_INVERSE":
        strategy, y = payload["strategy"], payload["observed"]
        if strategy == "linear":
            return linear_inverse(payload["matrix"], y, domain=payload.get("domain"))
        if "domain" in payload:
            return finite_readout_inverse(strategy, y, payload["domain"], total=payload.get("total"), options=payload)
        if strategy in ("radial", "radial_compact"):
            return radial_inverse(y, radii=payload.get("radii", SHELL_RADII), total=payload.get("total"))
        if strategy in ("angular", "angular_compact"):
            return angular_inverse(y, total=payload.get("total"), compact=strategy.endswith("compact"))
        raise ValueError("this inverse strategy requires a finite admitted domain")
    raise ValueError("unsupported GEN2 readout operation")


def dispatch(operation, payload):
    from .motion_adapters import readout_geometry
    from .boundary_information import register_ordinary
    return register_ordinary(operation, payload,
                             readout_geometry(operation, payload, _dispatch_base(operation, payload)))
