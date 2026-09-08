"""Source-visible Q2 compatibility geometry and six admitted HD objects."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

from .canonical import file_sha256
from .source import Q2_ROOT, SourceAdmissionError, SourceVisibleChoice


EXPECTED_Q2_ENGINE_SHA256 = "c901d6a330b75f0d06f6925a2d3dcf8642b85b4e4b2e3a04e92369ab4e352703"
Q2_ENGINE = Q2_ROOT / "slcv32_rz_q2/engine.py"
QUADRATIC_CLIP_MAX = 16_777_215


class GeometryError(ValueError):
    """Source-visible relative geometry is invalid."""


@dataclass(frozen=True, slots=True)
class Alignment:
    signed: tuple[int, int]
    absolute: tuple[int, int]
    squared: tuple[int, int]
    sum_sq: int
    abs_sum: int
    direction_mismatch: int
    direction_matches: tuple[int, int]
    parity_match: int
    candidate_span: int

    @property
    def order_key(self) -> tuple[Any, ...]:
        return (
            self.sum_sq,
            self.abs_sum,
            self.direction_mismatch,
            -self.parity_match,
            self.signed,
            self.direction_matches,
        )


@dataclass(frozen=True, slots=True)
class VisibleGeometry:
    best: Alignment
    other: Alignment
    midpoint_delta: int
    query_span: int
    candidate_span_abs: int
    best_span_relation: int
    other_span_relation: int

    @property
    def hd_objects(self) -> tuple[int, ...]:
        return (
            self.best.signed[0],
            self.best.signed[1],
            self.other.signed[0],
            self.other.signed[1],
            self.best_span_relation,
            self.other_span_relation,
        )


HD_OBJECT_NAMES = (
    "best_left_signed",
    "best_right_signed",
    "other_left_signed",
    "other_right_signed",
    "best_span_relation",
    "other_span_relation",
)


def signed_centered_delta(left: int, right: int, modulus: int = 256) -> int:
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (left, right, modulus)):
        raise GeometryError("centered-delta inputs must be exact integers")
    residue = (left - right) % modulus
    return residue - modulus if residue > modulus // 2 else residue


def _alignment(
    query: SourceVisibleChoice,
    candidate_left: int,
    candidate_right: int,
    direction_left: int,
    direction_right: int,
) -> Alignment:
    signed = (
        signed_centered_delta(query.left_shell, candidate_left),
        signed_centered_delta(query.right_shell, candidate_right),
    )
    absolute = tuple(abs(value) for value in signed)
    squared = tuple(value * value for value in signed)
    direction_matches = (
        int(query.left_direction == direction_left),
        int(query.right_direction == direction_right),
    )
    return Alignment(
        signed=signed,
        absolute=absolute,
        squared=squared,
        sum_sq=sum(squared),
        abs_sum=sum(absolute),
        direction_mismatch=2 - sum(direction_matches),
        direction_matches=direction_matches,
        parity_match=int((query.left_shell - candidate_left) % 2 == 0)
        + int((query.right_shell - candidate_right) % 2 == 0),
        candidate_span=candidate_right - candidate_left,
    )


def build_visible_geometry(
    query: SourceVisibleChoice,
    candidate: SourceVisibleChoice,
) -> VisibleGeometry:
    if query.axis != candidate.axis or query.modulus != candidate.modulus:
        raise GeometryError("Q3 feature rows require same-axis, same-modulus choices")
    alignments = sorted(
        (
            _alignment(
                query,
                candidate.left_shell,
                candidate.right_shell,
                candidate.left_direction,
                candidate.right_direction,
            ),
            _alignment(
                query,
                candidate.right_shell,
                candidate.left_shell,
                candidate.right_direction,
                candidate.left_direction,
            ),
        ),
        key=lambda row: row.order_key,
    )
    best, other = alignments
    midpoint_delta = (query.left_shell + query.right_shell) - (
        candidate.left_shell + candidate.right_shell
    )
    query_span = query.right_shell - query.left_shell
    return VisibleGeometry(
        best=best,
        other=other,
        midpoint_delta=midpoint_delta,
        query_span=query_span,
        candidate_span_abs=abs(candidate.right_shell - candidate.left_shell),
        best_span_relation=query_span - best.candidate_span,
        other_span_relation=query_span - other.candidate_span,
    )


def orientation_order_key(
    query: SourceVisibleChoice,
    candidate: SourceVisibleChoice,
) -> tuple[Any, ...]:
    """Canonical target-blind ordering of a concrete reciprocal orientation."""

    return _alignment(
        query,
        candidate.left_shell,
        candidate.right_shell,
        candidate.left_direction,
        candidate.right_direction,
    ).order_key


def q2_compat_features70(
    query: SourceVisibleChoice,
    candidate: SourceVisibleChoice,
) -> tuple[int, ...]:
    """Reconstruct Q2's 70 features and require frozen-byte equality."""

    geometry = build_visible_geometry(query, candidate)
    best, other = geometry.best, geometry.other
    signed = (*best.signed, *other.signed)
    absolute = (*best.absolute, *other.absolute)
    squared = (*best.squared, *other.squared)
    best_sum_sq, other_sum_sq = best.sum_sq, other.sum_sq
    minimum_sum_sq, maximum_sum_sq = sorted((best_sum_sq, other_sum_sq))
    best_abs_sum, other_abs_sum = best.abs_sum, other.abs_sum
    minimum_abs_sum, maximum_abs_sum = sorted((best_abs_sum, other_abs_sum))
    unordered_parity = int(
        sorted((query.left_shell % 2, query.right_shell % 2))
        == sorted((candidate.left_shell % 2, candidate.right_shell % 2))
    )
    route_match = int(query.route_domain == candidate.route_domain)
    relation_match = int(
        query.physical_relation_domain == candidate.physical_relation_domain
    )

    def full_v2(value: int) -> int:
        magnitude = abs(value)
        if magnitude == 0:
            return 8
        return min(8, (magnitude & -magnitude).bit_length() - 1)

    def clip(value: int) -> int:
        return max(-QUADRATIC_CLIP_MAX, min(QUADRATIC_CLIP_MAX, value))

    reconstructed = (
        1,
        *(int(query.axis == axis) for axis in range(4)),
        int(query.modulus == 524287),
        route_match,
        relation_match,
        *signed,
        *absolute,
        *squared,
        best_sum_sq,
        other_sum_sq,
        minimum_sum_sq,
        maximum_sum_sq,
        best_abs_sum,
        other_abs_sum,
        minimum_abs_sum,
        maximum_abs_sum,
        geometry.midpoint_delta,
        abs(geometry.midpoint_delta),
        geometry.query_span,
        geometry.candidate_span_abs,
        geometry.best_span_relation,
        abs(geometry.best_span_relation),
        geometry.other_span_relation,
        abs(geometry.other_span_relation),
        best.direction_mismatch,
        other.direction_mismatch,
        min(best.direction_mismatch, other.direction_mismatch),
        *best.direction_matches,
        *other.direction_matches,
        query.left_shell % 2,
        query.right_shell % 2,
        *sorted((candidate.left_shell % 2, candidate.right_shell % 2)),
        best.parity_match,
        other.parity_match,
        unordered_parity,
        *(full_v2(value) for value in signed),
        full_v2(geometry.best_span_relation),
        full_v2(geometry.other_span_relation),
        clip(minimum_sum_sq * min(best.direction_mismatch, other.direction_mismatch)),
        clip(minimum_abs_sum * abs(geometry.best_span_relation)),
        clip(abs(geometry.midpoint_delta) * abs(geometry.best_span_relation)),
        clip(best_sum_sq * abs(geometry.midpoint_delta)),
        clip(best_sum_sq * other_sum_sq),
        clip(geometry.best_span_relation * geometry.best_span_relation),
        clip(geometry.midpoint_delta * geometry.midpoint_delta),
        clip(minimum_abs_sum * minimum_abs_sum),
        clip(other_abs_sum * other_abs_sum),
        clip(best.direction_mismatch * best_sum_sq),
        clip(other.direction_mismatch * other_sum_sq),
        clip((2 - max(best.parity_match, other.parity_match)) * minimum_abs_sum),
        clip(route_match * minimum_sum_sq),
        clip(relation_match * abs(geometry.best_span_relation)),
    )
    if len(reconstructed) != 70:
        raise GeometryError("candidate-owned Q2 compatibility width differs")

    if file_sha256(Q2_ENGINE) != EXPECTED_Q2_ENGINE_SHA256:
        raise SourceAdmissionError("frozen Q2 engine bytes differ")
    if str(Q2_ROOT) not in sys.path:
        sys.path.insert(0, str(Q2_ROOT))
    from slcv32_rz_q2.engine import visible_features  # noqa: PLC0415

    frozen = visible_features(query, candidate)
    if len(frozen) != 70 or any(isinstance(value, bool) or not isinstance(value, int) for value in frozen):
        raise GeometryError("frozen Q2 compatibility feature row differs")
    if reconstructed != frozen:
        raise GeometryError("candidate-owned Q2 feature reconstruction differs from frozen Q2")
    return reconstructed
