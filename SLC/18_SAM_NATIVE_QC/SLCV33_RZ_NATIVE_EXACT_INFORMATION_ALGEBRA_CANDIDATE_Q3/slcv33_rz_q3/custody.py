"""Exact source-visible custody profile for frozen Q2 physical groups."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any, Mapping

from .foundation import BOUND_CUSTODY_SCHEMA, BoundV6Foundation
from .geometry import orientation_order_key
from .source import Q3Group, SourceVisibleChoice


class CustodyError(ValueError):
    """A source-visible group does not admit the frozen custody structure."""


def _container_bits(cardinality: int) -> int:
    if cardinality < 1:
        raise CustodyError("receipt alphabet cardinality must be positive")
    return 0 if cardinality == 1 else (cardinality - 1).bit_length()


def _formal_coefficients(value: object, label: str) -> tuple[tuple[int, Fraction], ...]:
    """Project a strict V6 FormalLogElement serialization into Q3 coordinates."""

    if not isinstance(value, Mapping) or value.get("schema") != "SLC_FORMAL_LOG_ELEMENT_V1":
        raise CustodyError(f"{label} is not a bound V6 formal-log serialization")
    raw = value.get("coefficients")
    if not isinstance(raw, list):
        raise CustodyError(f"{label} coefficient roster differs")
    result: list[tuple[int, Fraction]] = []
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != {"prime", "coefficient"}:
            raise CustodyError(f"{label} has noncanonical coefficient fields")
        prime = row["prime"]
        fraction = row["coefficient"]
        if type(prime) is not int or not isinstance(fraction, Mapping):
            raise CustodyError(f"{label} coefficient is not exact")
        numerator, denominator = fraction.get("numerator"), fraction.get("denominator")
        if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
            raise CustodyError(f"{label} coefficient fraction differs")
        exact = Fraction(numerator, denominator)
        if exact.numerator != numerator or exact.denominator != denominator:
            raise CustodyError(f"{label} coefficient fraction is not reduced")
        result.append((prime, exact))
    if tuple(sorted(result)) != tuple(result) or len({prime for prime, _ in result}) != len(result):
        raise CustodyError(f"{label} coefficient order differs")
    return tuple(result)


@dataclass(frozen=True, slots=True)
class CustodyAudit:
    orientation_count: int
    direct_multiplicity: int
    best_orientation_multiplicity: int
    other_orientation_multiplicity: int
    chain_rule_residual: tuple[tuple[int, Fraction], ...]
    exact_reconstruction: bool
    minimal_receipt_channel_count: int
    receipt_redundancy: int
    composition_depth: int
    uncomputation_erased_information: tuple[tuple[int, Fraction], ...]

    @property
    def passed(self) -> bool:
        return (
            self.orientation_count == 2
            and not self.chain_rule_residual
            and self.exact_reconstruction
            and self.minimal_receipt_channel_count == 2
            and self.receipt_redundancy == 0
            and self.composition_depth == 2
            and not self.uncomputation_erased_information
        )


CUSTODY_FEATURE_NAMES = (
    "best_orientation_multiplicity",
    "other_orientation_multiplicity",
    "minimum_orientation_multiplicity",
    "maximum_orientation_multiplicity",
    "orientation_multiplicity_delta",
    "orientation_multiplicity_product",
    "orientation_multiplicity_gcd",
    "direct_container_bits",
    "best_branch_container_bits",
    "other_branch_container_bits",
    "expected_hierarchical_container_bits",
    "direct_minus_expected_hierarchical_bits",
    "direct_ln2_coefficient",
    "direct_ln5_coefficient",
    "orientation_innovation_ln2_coefficient",
    "orientation_innovation_ln5_coefficient",
    "realization_innovation_ln2_coefficient",
    "realization_innovation_ln5_coefficient",
    "hierarchical_support_ln2_coefficient",
    "hierarchical_support_ln5_coefficient",
    "support_overhead_ln2_coefficient",
    "support_overhead_ln5_coefficient",
)


@dataclass(frozen=True, slots=True)
class CustodyProfile:
    direct_multiplicity: int
    best_orientation_multiplicity: int
    other_orientation_multiplicity: int
    direct_information: tuple[tuple[int, Fraction], ...]
    orientation_innovation: tuple[tuple[int, Fraction], ...]
    realization_innovation: tuple[tuple[int, Fraction], ...]
    hierarchical_support: tuple[tuple[int, Fraction], ...]
    support_overhead: tuple[tuple[int, Fraction], ...]
    expected_hierarchical_container_bits: Fraction
    audit: CustodyAudit
    foundation_serialization: Mapping[str, Any]

    def feature_block(self) -> tuple[Fraction, ...]:
        best = self.best_orientation_multiplicity
        other = self.other_orientation_multiplicity
        direct_bits = _container_bits(self.direct_multiplicity)
        expected_bits = self.expected_hierarchical_container_bits
        direct = dict(self.direct_information)
        orientation = dict(self.orientation_innovation)
        realization = dict(self.realization_innovation)
        support = dict(self.hierarchical_support)
        overhead = dict(self.support_overhead)
        values = (
            best,
            other,
            min(best, other),
            max(best, other),
            abs(best - other),
            best * other,
            gcd(best, other),
            direct_bits,
            _container_bits(best),
            _container_bits(other),
            expected_bits,
            Fraction(direct_bits) - expected_bits,
            direct.get(2, Fraction()),
            direct.get(5, Fraction()),
            orientation.get(2, Fraction()),
            orientation.get(5, Fraction()),
            realization.get(2, Fraction()),
            realization.get(5, Fraction()),
            support.get(2, Fraction()),
            support.get(5, Fraction()),
            overhead.get(2, Fraction()),
            overhead.get(5, Fraction()),
        )
        exact = tuple(Fraction(value) for value in values)
        if len(exact) != 22:
            raise CustodyError("custody feature width differs")
        return exact


def build_custody_profile(
    query: SourceVisibleChoice,
    group: Q3Group,
    foundation: BoundV6Foundation,
) -> CustodyProfile:
    """Project bound-V6 custody into 22 source-visible exact coordinates."""

    orientations = Counter(record.visible for record in group.records)
    if len(orientations) != 2:
        raise CustodyError("frozen physical group must have two visible orientations")
    ordered = sorted(orientations, key=lambda choice: orientation_order_key(query, choice))
    best, other = orientations[ordered[0]], orientations[ordered[1]]
    multiplicity = best + other
    if multiplicity != group.multiplicity:
        raise CustodyError("orientation partition does not cover physical group")

    serialized = foundation.serialize_custody(best, other)
    if serialized.get("schema") != BOUND_CUSTODY_SCHEMA:
        raise CustodyError("bound V6 custody schema differs")
    if (
        serialized.get("best_orientation_multiplicity") != best
        or serialized.get("other_orientation_multiplicity") != other
        or serialized.get("direct_multiplicity") != multiplicity
    ):
        raise CustodyError("bound V6 custody multiplicities differ")
    formal_logs = serialized.get("formal_logs")
    if not isinstance(formal_logs, Mapping):
        raise CustodyError("bound V6 custody formal logs are absent")
    direct = _formal_coefficients(formal_logs.get("direct_information"), "direct information")
    orientation = _formal_coefficients(
        formal_logs.get("orientation_innovation"), "orientation innovation"
    )
    realization = _formal_coefficients(
        formal_logs.get("realization_innovation"), "realization innovation"
    )
    hierarchical_support = _formal_coefficients(
        formal_logs.get("hierarchical_support"), "hierarchical support"
    )
    support_overhead = _formal_coefficients(
        formal_logs.get("support_overhead"), "support overhead"
    )
    sufficiency = serialized.get("receipt_sufficiency")
    uncomputation = serialized.get("uncomputation_plan")
    identity = serialized.get("information_identity")
    if not isinstance(sufficiency, Mapping) or not isinstance(uncomputation, Mapping):
        raise CustodyError("bound V6 receipt or uncomputation certificate is absent")
    if not isinstance(identity, Mapping):
        raise CustodyError("bound V6 custody identity is absent")
    erased = _formal_coefficients(
        uncomputation.get("logical_erasure_exact_nats"), "uncomputation erasure"
    )
    expected_bits = (
        Fraction(best, multiplicity) * (1 + _container_bits(best))
        + Fraction(other, multiplicity) * (1 + _container_bits(other))
    )
    audit = CustodyAudit(
        orientation_count=2,
        direct_multiplicity=multiplicity,
        best_orientation_multiplicity=best,
        other_orientation_multiplicity=other,
        chain_rule_residual=(
            ()
            if serialized.get("chain_law_exact") is True and identity.get("identity_exact") is True
            else ((-1, Fraction(1)),)
        ),
        exact_reconstruction=sufficiency.get("reconstructs_source") is True,
        minimal_receipt_channel_count=len(tuple(sufficiency.get("selected_channels", ()))),
        receipt_redundancy=len(tuple(sufficiency.get("redundant_channels", ()))),
        composition_depth=serialized.get("composition_depth"),
        uncomputation_erased_information=erased,
    )
    if not audit.passed:
        raise CustodyError("custody chain or receipt audit differs")
    return CustodyProfile(
        direct_multiplicity=multiplicity,
        best_orientation_multiplicity=best,
        other_orientation_multiplicity=other,
        direct_information=direct,
        orientation_innovation=orientation,
        realization_innovation=realization,
        hierarchical_support=hierarchical_support,
        support_overhead=support_overhead,
        expected_hierarchical_container_bits=expected_bits,
        audit=audit,
        foundation_serialization=serialized,
    )
