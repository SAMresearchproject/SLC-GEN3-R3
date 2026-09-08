#!/usr/bin/env python3
"""Typed SLC v0.5 IR and exact T18/legacy-fiber adapter."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Mapping

import numpy as np


THETA_PACKET_ARITY = 9
THETA_ARITY = 18
FACTOR_DIMENSION = 1 << THETA_PACKET_ARITY
ASSIGNMENT_COUNT = 1 << THETA_ARITY
LOW_MASK = FACTOR_DIMENSION - 1
EXPECTED_LEGACY_MAP_SHA256 = (
    "5cd4e3001b11e8c1ecb828087aaab94bbace51c1129d5bacbd4218f95e7f9ab3"
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


class SitePhase(str, Enum):
    W8_NON_CONTACT = "W8_NON_CONTACT"
    W9_ACTIVE_WRITE = "W9_ACTIVE_WRITE"


class QEvent(str, Enum):
    IDENTITY = "IDENTITY"
    FORWARD = "FORWARD"
    REVERSE = "REVERSE"


class RepresentationKind(str, Enum):
    M126_RETENTION = "M126_SYMMETRIC_DIFFERENCE_RETENTION"
    N144 = "N144_INDEPENDENT_UNION_STATE"
    N144_PLUS_D = "N144_PLUS_THETA_CONSTRAINT_DEFECT"
    L162 = "L162_CONTACT_EXPANDED_OCCURRENCES"


@dataclass(frozen=True)
class MatterObjectId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("MatterObjectId must be nonempty")


@dataclass(frozen=True)
class SubstrateSiteId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("SubstrateSiteId must be nonempty")


@dataclass(frozen=True)
class X1MirrorCustody:
    bit: int

    def __post_init__(self) -> None:
        if type(self.bit) is not int or self.bit not in (0, 1):
            raise ValueError("X1 custody is exactly one binary witness")

    @property
    def ledger_contribution(self) -> int:
        return 0


@dataclass(frozen=True)
class ContactOrderWitness:
    order_id: str
    event_index: int
    source_site: SubstrateSiteId
    target_site: SubstrateSiteId

    def __post_init__(self) -> None:
        if not self.order_id:
            raise ValueError("contact order id must be nonempty")
        if type(self.event_index) is not int or self.event_index < 0:
            raise ValueError("contact event index must be nonnegative")
        if self.source_site == self.target_site:
            raise ValueError("contact source and target must be distinct")


@dataclass(frozen=True)
class AdaptiveArityPromotionReceipt:
    representation: RepresentationKind
    defect_rank: int
    effective_arity: int


def select_representation(
    *,
    matter_retention_only: bool,
    defect_rank: int,
    independent_occurrences_requested: bool,
) -> AdaptiveArityPromotionReceipt:
    if type(defect_rank) is not int or not 0 <= defect_rank <= 18:
        raise ValueError("Theta constraint-defect rank must lie in 0..18")
    if matter_retention_only:
        return AdaptiveArityPromotionReceipt(
            RepresentationKind.M126_RETENTION,
            defect_rank,
            126,
        )
    if independent_occurrences_requested or defect_rank == 18:
        return AdaptiveArityPromotionReceipt(
            RepresentationKind.L162,
            defect_rank,
            162,
        )
    if defect_rank == 0:
        return AdaptiveArityPromotionReceipt(
            RepresentationKind.N144,
            defect_rank,
            144,
        )
    return AdaptiveArityPromotionReceipt(
        RepresentationKind.N144_PLUS_D,
        defect_rank,
        144 + defect_rank,
    )


@dataclass(frozen=True)
class ThetaWriteReceipt:
    record_index: int
    event: QEvent
    source_q: int
    target_q: int
    low_factor_changed: bool
    high_factor_changed: bool
    source_phase_during: SitePhase = SitePhase.W8_NON_CONTACT
    direct_target_phase_during: SitePhase = SitePhase.W9_ACTIVE_WRITE
    completion_phase: SitePhase = SitePhase.W8_NON_CONTACT


@dataclass(frozen=True)
class Theta18Fiber:
    """Two computational Theta9 factors encoding nine active Z4 records."""

    theta_low9: int
    theta_high9: int

    def __post_init__(self) -> None:
        for name, value in (
            ("theta_low9", self.theta_low9),
            ("theta_high9", self.theta_high9),
        ):
            if type(value) is not int or not 0 <= value < FACTOR_DIMENSION:
                raise ValueError(f"{name} must be a nine-bit integer")

    @classmethod
    def from_address(cls, address: int) -> "Theta18Fiber":
        if type(address) is not int or not 0 <= address < ASSIGNMENT_COUNT:
            raise ValueError("T18 address must lie in 0..2^18-1")
        return cls(address & LOW_MASK, address >> THETA_PACKET_ARITY)

    @classmethod
    def from_q_vector(cls, q_values: tuple[int, ...]) -> "Theta18Fiber":
        if len(q_values) != THETA_PACKET_ARITY:
            raise ValueError("T18 requires exactly nine q coordinates")
        low = 0
        high = 0
        for index, raw_q in enumerate(q_values):
            if type(raw_q) is not int or not 0 <= raw_q < 4:
                raise ValueError("every q coordinate must lie in Z4")
            low |= (raw_q & 1) << index
            high |= ((raw_q >> 1) & 1) << index
        return cls(low, high)

    @property
    def address(self) -> int:
        return self.theta_low9 | (
            self.theta_high9 << THETA_PACKET_ARITY
        )

    @property
    def q_vector(self) -> tuple[int, ...]:
        return tuple(
            (((self.theta_high9 >> index) & 1) << 1)
            | ((self.theta_low9 >> index) & 1)
            for index in range(THETA_PACKET_ARITY)
        )

    def apply(
        self,
        *,
        record_index: int,
        event: QEvent,
    ) -> tuple["Theta18Fiber", ThetaWriteReceipt]:
        if type(record_index) is not int or not 0 <= record_index < 9:
            raise ValueError("record_index must lie in 0..8")
        if not isinstance(event, QEvent):
            raise TypeError("event must be a QEvent")
        source_q = self.q_vector[record_index]
        delta = {
            QEvent.IDENTITY: 0,
            QEvent.FORWARD: 1,
            QEvent.REVERSE: -1,
        }[event]
        target_q = (source_q + delta) % 4
        q_values = list(self.q_vector)
        q_values[record_index] = target_q
        target = Theta18Fiber.from_q_vector(tuple(q_values))
        bit = 1 << record_index
        receipt = ThetaWriteReceipt(
            record_index=record_index,
            event=event,
            source_q=source_q,
            target_q=target_q,
            low_factor_changed=bool(
                (self.theta_low9 ^ target.theta_low9) & bit
            ),
            high_factor_changed=bool(
                (self.theta_high9 ^ target.theta_high9) & bit
            ),
        )
        return target, receipt


def build_t18_transition_maps() -> tuple[np.ndarray, dict[str, Any]]:
    """Exhaust the 18 signed maps over all 2^18 T18 addresses."""

    addresses = np.arange(ASSIGNMENT_COUNT, dtype=np.uint32)
    low = addresses & np.uint32(LOW_MASK)
    high = addresses >> np.uint32(THETA_PACKET_ARITY)
    maps = np.empty(
        (2, THETA_PACKET_ARITY, ASSIGNMENT_COUNT),
        dtype=np.uint32,
    )
    carry_counts: list[dict[str, int]] = []
    for record_index in range(THETA_PACKET_ARITY):
        bit = np.uint32(1 << record_index)
        low_bit = (low >> np.uint32(record_index)) & np.uint32(1)
        target_low = low ^ bit
        forward_high = high ^ (low_bit * bit)
        reverse_high = high ^ ((np.uint32(1) - low_bit) * bit)
        forward = target_low | (
            forward_high << np.uint32(THETA_PACKET_ARITY)
        )
        reverse = target_low | (
            reverse_high << np.uint32(THETA_PACKET_ARITY)
        )
        maps[0, record_index, :] = forward
        maps[1, record_index, :] = reverse
        if not np.array_equal(reverse[forward], addresses):
            raise RuntimeError("T18 reverse-after-forward did not close")
        if not np.array_equal(forward[reverse], addresses):
            raise RuntimeError("T18 forward-after-reverse did not close")
        carry_counts.append(
            {
                "record_index": record_index,
                "forward_high_factor_changes": int(
                    np.count_nonzero((high ^ forward_high) & bit)
                ),
                "reverse_high_factor_changes": int(
                    np.count_nonzero((high ^ reverse_high) & bit)
                ),
            }
        )
    map_sha256 = hashlib.sha256(
        np.ascontiguousarray(maps, dtype=">u4").tobytes(order="C")
    ).hexdigest()
    receipt = {
        "schema": "SLCV05_T18_EXHAUSTIVE_COMPATIBILITY_RECEIPT_V1",
        "arity": THETA_ARITY,
        "packet_count": 2,
        "theta_coordinates_per_packet": THETA_PACKET_ARITY,
        "q_coordinate_count": THETA_PACKET_ARITY,
        "coordinate_group": "Z4",
        "factor_dimensions": [FACTOR_DIMENSION, FACTOR_DIMENSION],
        "assignment_count": ASSIGNMENT_COUNT,
        "signed_map_count": 2 * THETA_PACKET_ARITY,
        "event_count_per_record": 3,
        "transition_count_exercised": (
            3 * THETA_PACKET_ARITY * ASSIGNMENT_COUNT
        ),
        "map_sha256": map_sha256,
        "carry_counts": carry_counts,
        "all_signed_maps_closed_and_invertible": True,
        "physical_theta_partition_selected": False,
        "public_name_component": "T18",
        "legacy_encoding": "ACTIVE_512_BY_512_Z4_9",
    }
    return maps, receipt


def run_ir_self_checks() -> Mapping[str, bool]:
    source = SubstrateSiteId("source")
    target = SubstrateSiteId("target")
    witness = ContactOrderWitness("LEXICOGRAPHIC", 0, source, target)
    x1 = X1MirrorCustody(1)
    zero = Theta18Fiber(0, 0)
    checks = {
        "theta18_arity_is_18": THETA_ARITY == 18,
        "two_theta9_factors_are_512_by_512": (
            FACTOR_DIMENSION == 512 and ASSIGNMENT_COUNT == 512 * 512
        ),
        "zero_address_roundtrips": Theta18Fiber.from_address(0) == zero,
        "maximum_address_roundtrips": (
            Theta18Fiber.from_address(ASSIGNMENT_COUNT - 1).address
            == ASSIGNMENT_COUNT - 1
        ),
        "all_four_local_q_values_roundtrip": all(
            Theta18Fiber.from_q_vector((q,) + (0,) * 8).q_vector[0] == q
            for q in range(4)
        ),
        "forward_reverse_local_roundtrip": all(
            Theta18Fiber.from_q_vector((q,) + (0,) * 8)
            .apply(record_index=0, event=QEvent.FORWARD)[0]
            .apply(record_index=0, event=QEvent.REVERSE)[0]
            == Theta18Fiber.from_q_vector((q,) + (0,) * 8)
            for q in range(4)
        ),
        "contact_order_witness_is_explicit": witness.event_index == 0,
        "x1_is_one_bit_and_nonadditive": (
            x1.bit == 1 and x1.ledger_contribution == 0
        ),
        "matter_retention_routes_to_m126": (
            select_representation(
                matter_retention_only=True,
                defect_rank=7,
                independent_occurrences_requested=False,
            ).representation
            is RepresentationKind.M126_RETENTION
        ),
        "rank_zero_routes_to_n144": (
            select_representation(
                matter_retention_only=False,
                defect_rank=0,
                independent_occurrences_requested=False,
            ).representation
            is RepresentationKind.N144
        ),
        "interior_rank_routes_to_n144_plus_d": (
            select_representation(
                matter_retention_only=False,
                defect_rank=9,
                independent_occurrences_requested=False,
            ).effective_arity
            == 153
        ),
        "rank_eighteen_routes_to_l162": (
            select_representation(
                matter_retention_only=False,
                defect_rank=18,
                independent_occurrences_requested=False,
            ).representation
            is RepresentationKind.L162
        ),
    }
    if not all(checks.values()):
        raise RuntimeError("SLC v0.5 typed IR self-check failed")
    return checks


__all__ = [
    "ASSIGNMENT_COUNT",
    "ContactOrderWitness",
    "EXPECTED_LEGACY_MAP_SHA256",
    "FACTOR_DIMENSION",
    "MatterObjectId",
    "QEvent",
    "RepresentationKind",
    "SitePhase",
    "SubstrateSiteId",
    "THETA_ARITY",
    "THETA_PACKET_ARITY",
    "Theta18Fiber",
    "ThetaWriteReceipt",
    "X1MirrorCustody",
    "build_t18_transition_maps",
    "canonical_bytes",
    "canonical_sha256",
    "run_ir_self_checks",
    "select_representation",
]
