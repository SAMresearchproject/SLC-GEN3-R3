"""Source-native signed receiver changes (H000935), with explicit units."""
from __future__ import annotations

from .exact import ExactError, bilinear, seal, symmetric_matrix, token, vector


def quadratic_weights(before, after) -> tuple:
    h0, h1 = vector(before), vector(after)
    if len(h0) != len(h1):
        raise ExactError("before/after dimensions differ")
    return tuple((i, j, (1 if i == j else 2)*(h1[i]*h1[j]-h0[i]*h0[j]))
                 for i in range(len(h0)) for j in range(i, len(h0)))


def quadratic_change(before, after, matrix, *, coefficient_unit: str,
                     source_unit: str = "DIMENSIONLESS", normalization: str = "AS_SUPPLIED") -> dict:
    h0, h1 = vector(before), vector(after)
    if len(h0) != len(h1):
        raise ExactError("before/after dimensions differ")
    q = symmetric_matrix(matrix, len(h0))
    current = tuple(y-x for x, y in zip(h0, h1))
    old, new = bilinear(h0, q, h0), bilinear(h1, q, h1)
    self_term, cross = bilinear(current, q, current), 2*bilinear(h0, q, current)
    weights = quadratic_weights(h0, h1)
    if new-old != self_term+cross or new-old != sum(w*q[i][j] for i, j, w in weights):
        raise ExactError("quadratic reconstruction differs")
    return seal("Q3_SIGNED_QUADRATIC_CHANGE_V1", before=h0, after=h1, matrix=q,
                current=current, energy_before=old, energy_after=new, signed_change=new-old,
                current_self=self_term, occupied_cross=cross, coordinate_weights=weights,
                nonzero_coordinate_count=sum(w != 0 for _, _, w in weights),
                coefficient_unit=token(coefficient_unit), source_unit=token(source_unit),
                output_unit=f"({coefficient_unit})*({source_unit})^2",
                normalization=token(normalization))


def reciprocal_receiver(left, right, current, matrix, *, coefficient_unit: str) -> dict:
    a, b, c = vector(left), vector(right), vector(current)
    if len(a) != len(b) or len(a) != len(c):
        raise ExactError("reciprocal receiver dimensions differ")
    q = symmetric_matrix(matrix, len(a))
    out_a = tuple(x+y for x, y in zip(a, c))
    out_b = tuple(x-y for x, y in zip(b, c))
    delta_a = bilinear(out_a, q, out_a)-bilinear(a, q, a)
    delta_b = bilinear(out_b, q, out_b)-bilinear(b, q, b)
    return seal("Q3_SIGNED_RECIPROCAL_RECEIVER_V1",
                left=quadratic_change(a, out_a, q, coefficient_unit=coefficient_unit),
                right=quadratic_change(b, out_b, q, coefficient_unit=coefficient_unit),
                directed_changes=(delta_a, delta_b), whole_change=delta_a+delta_b,
                coefficient_unit=coefficient_unit)
