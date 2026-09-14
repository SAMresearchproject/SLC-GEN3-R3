"""Exact low-cost Starbreaker FORM0 Home-formation state machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import re
from typing import Any, Iterable, Mapping

from .exact import exact_value, fraction_text, record_sha256


PRE_CLOSE_OPERATIONS = {
    "CONTACT_WRITE",
    "PRE_CLOSE_CAPTURE",
    "APPROACH_A1",
    "SEAL_HOME",
}
POST_CLOSE_OPERATIONS = {
    "EXTERIOR_ARRIVAL",
    "POST_CLOSE_IN_ATTEMPT",
    "OUT_SELECTED",
    "OUT_QUANTUM_REALIZED",
}
ALL_OPERATIONS = PRE_CLOSE_OPERATIONS | POST_CLOSE_OPERATIONS
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class TransitionError(ValueError):
    """Raised when an event is not admitted by the native FORM0 grammar."""


def _positive_fraction(value: Fraction | int | str, name: str) -> Fraction:
    item = value if isinstance(value, Fraction) else Fraction(value)
    if item <= 0:
        raise TransitionError(f"{name} must be strict positive")
    return item


def _balance_text(values: Mapping[str, Fraction]) -> dict[str, str]:
    return {
        key: fraction_text(value)
        for key, value in sorted(values.items())
        if value != 0
    }


@dataclass
class HomeFormationState:
    """One isolated source carried through an exact Home-sealing grammar."""

    source_id: str
    origin_mass: Fraction
    phase: str = "OPEN"
    sealed: bool = False
    crossing_allowed: bool = True
    interior_balances: dict[str, Fraction] = field(default_factory=dict)
    exterior_balances: dict[str, Fraction] = field(default_factory=dict)
    captured_packet_refs: dict[str, dict[str, Any]] = field(default_factory=dict)
    internal_history: list[str] = field(default_factory=list)
    theta_packets: list[str] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)
    m_form: Fraction | None = None
    r_form: Fraction | None = None
    seal_event_id: str | None = None
    parent_mass_loss: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        self.origin_mass = _positive_fraction(self.origin_mass, "origin_mass")
        if not self.source_id:
            raise TransitionError("source_id must be nonempty")

    @property
    def interior_total(self) -> Fraction:
        return self.origin_mass + sum(self.interior_balances.values(), Fraction(0))

    @property
    def exterior_total(self) -> Fraction:
        return sum(self.exterior_balances.values(), Fraction(0))

    @property
    def total_mass(self) -> Fraction:
        if self.m_form is None:
            return self.interior_total
        return self.m_form + self.exterior_total

    def snapshot(self) -> dict[str, Any]:
        return {
            "captured_packet_refs": exact_value(self.captured_packet_refs),
            "crossing_allowed": self.crossing_allowed,
            "event_ids": list(self.event_ids),
            "exterior_balances": _balance_text(self.exterior_balances),
            "exterior_total": fraction_text(self.exterior_total),
            "interior_balances": _balance_text(self.interior_balances),
            "interior_total": fraction_text(self.interior_total),
            "internal_history": list(self.internal_history),
            "m_form": None if self.m_form is None else fraction_text(self.m_form),
            "parent_mass_loss": fraction_text(self.parent_mass_loss),
            "phase": self.phase,
            "r_form": None if self.r_form is None else fraction_text(self.r_form),
            "seal_event_id": self.seal_event_id,
            "sealed": self.sealed,
            "source_id": self.source_id,
            "theta_packets": list(self.theta_packets),
            "total_mass": fraction_text(self.total_mass),
            "w_state": "W8/W8/X1=0",
        }

    def _require_pre_close(self, operation: str) -> None:
        if self.sealed or not self.crossing_allowed:
            raise TransitionError(f"{operation} is unavailable after Home sealing")

    def _require_post_close(self, operation: str) -> None:
        if not self.sealed or self.crossing_allowed:
            raise TransitionError(f"{operation} requires a sealed Home")

    def apply(self, raw_event: Mapping[str, Any]) -> dict[str, Any]:
        event = dict(raw_event)
        event_id = str(event.get("event_id", ""))
        operation = str(event.get("operation", ""))
        if not event_id:
            raise TransitionError("event_id must be nonempty")
        if event_id in self.event_ids:
            raise TransitionError(f"duplicate event_id: {event_id}")
        if operation not in ALL_OPERATIONS:
            raise TransitionError(f"unsupported operation: {operation}")

        radius = _positive_fraction(event.get("radius", 0), "radius")
        r_s = _positive_fraction(event.get("r_s", 0), "r_s")
        accumulation = r_s / radius
        before = self.snapshot()
        before_hash = record_sha256(before)
        status = "COMPLETED"
        phase_event = self.phase
        transient_state = "W8/W8/X1=0"
        matter_id = event.get("matter_id")
        matter_packet_ref = event.get("matter_packet_ref")
        amount = Fraction(event.get("amount", 0))
        theta_output: dict[str, Any] | None = None
        parent_payload: dict[str, str] | None = None
        internal_history_changed = False

        if operation in PRE_CLOSE_OPERATIONS:
            self._require_pre_close(operation)
        else:
            self._require_post_close(operation)

        if operation == "CONTACT_WRITE":
            if accumulation >= 1:
                raise TransitionError("CONTACT_WRITE requires A<1")
            transient_state = "W8/W9/X1=1"
            self.phase = "FORMING"
            tag = f"CONTACT:{event_id}:{event.get('direction', 'FORWARD')}"
            self.internal_history.append(tag)
            internal_history_changed = True

        elif operation == "PRE_CLOSE_CAPTURE":
            if accumulation >= 1:
                raise TransitionError("PRE_CLOSE_CAPTURE requires A<1")
            if not matter_id:
                raise TransitionError("PRE_CLOSE_CAPTURE requires matter_id")
            amount = _positive_fraction(amount, "amount")
            normalized_packet_ref: dict[str, Any] | None = None
            if matter_packet_ref is not None:
                if not isinstance(matter_packet_ref, Mapping):
                    raise TransitionError("matter_packet_ref must be a typed mapping")
                semantic = str(matter_packet_ref.get("semantic_sha256", ""))
                status_value = matter_packet_ref.get("status")
                if not SHA256_RE.fullmatch(semantic):
                    raise TransitionError("matter_packet_ref requires a semantic SHA-256")
                if status_value != "EXACT_ATOMIC_ACCUMULATED_WRITE_IDENTITY_ACCEPTED":
                    raise TransitionError("matter_packet_ref is not an accepted A3D18 identity")
                normalized_packet_ref = exact_value(dict(matter_packet_ref))
                existing = self.captured_packet_refs.get(str(matter_id))
                if existing is not None and existing != normalized_packet_ref:
                    raise TransitionError("matter_id cannot change atomic packet identity")
            self.phase = "FORMING"
            self.interior_balances[str(matter_id)] = (
                self.interior_balances.get(str(matter_id), Fraction(0)) + amount
            )
            if normalized_packet_ref is not None:
                self.captured_packet_refs[str(matter_id)] = normalized_packet_ref
            self.internal_history.append(f"CAPTURE:{matter_id}")
            internal_history_changed = True
            transient_state = "W8/W9/X1=1"

        elif operation == "APPROACH_A1":
            if accumulation >= 1:
                raise TransitionError("APPROACH_A1 requires A<1")
            self.phase = "FORMING"

        elif operation == "SEAL_HOME":
            if self.phase != "FORMING":
                raise TransitionError("SEAL_HOME requires a prior FORMING state")
            if accumulation != 1:
                raise TransitionError("SEAL_HOME requires exact A=1")
            phase_event = "CLOSURE"
            transient_state = "W8/W9/X1=1"
            self.m_form = self.interior_total
            self.r_form = radius
            self.sealed = True
            self.crossing_allowed = False
            self.phase = "SEALED"
            self.seal_event_id = event_id
            self.internal_history.append(f"SEAL:{event_id}")
            internal_history_changed = True
            packet_id = f"FORM0:{self.source_id}:{event_id}:FORMATION_BURST"
            self.theta_packets.append(packet_id)
            theta_output = {
                "kind": "NON_HAWKING_FORMATION_BURST",
                "packet_id": packet_id,
                "retained_matter_credit": "0/1",
            }

        elif operation == "EXTERIOR_ARRIVAL":
            if not matter_id:
                raise TransitionError("EXTERIOR_ARRIVAL requires matter_id")
            amount = _positive_fraction(amount, "amount")
            self.phase = "POST_FORMATION"
            self.exterior_balances[str(matter_id)] = (
                self.exterior_balances.get(str(matter_id), Fraction(0)) + amount
            )

        elif operation == "POST_CLOSE_IN_ATTEMPT":
            self.phase = "POST_FORMATION"
            status = "IN_FAILED_NO_WRITE"
            transient_state = "W8/W8/X1=0"

        elif operation == "OUT_SELECTED":
            if not matter_id:
                raise TransitionError("OUT_SELECTED requires matter_id")
            amount = _positive_fraction(amount, "amount")
            if self.exterior_balances.get(str(matter_id), Fraction(0)) < amount:
                raise TransitionError("OUT_SELECTED exceeds exterior custody")
            self.phase = "POST_FORMATION"
            status = "OUT_OPTION_RETAINED_NO_DEBIT"

        elif operation == "OUT_QUANTUM_REALIZED":
            if not matter_id:
                raise TransitionError("OUT_QUANTUM_REALIZED requires matter_id")
            amount = _positive_fraction(amount, "amount")
            available = self.exterior_balances.get(str(matter_id), Fraction(0))
            if available < amount:
                raise TransitionError("OUT_QUANTUM_REALIZED exceeds exterior custody")
            self.phase = "POST_FORMATION"
            self.exterior_balances[str(matter_id)] = available - amount
            self.parent_mass_loss += amount
            parent_payload = {"M_loss": fraction_text(amount)}
            status = "OUT_QUANTUM_REALIZED"

        self.event_ids.append(event_id)
        after = self.snapshot()
        after_hash = record_sha256(after)
        if self.sealed:
            if self.m_form is None or self.r_form is None:
                raise AssertionError("sealed Home lost formation invariants")
            if self.exterior_total < 0 or self.total_mass < self.m_form:
                raise AssertionError("post-formation balance invariant failed")
            if self.crossing_allowed:
                raise AssertionError("sealed Home retained ordinary crossing")

        receipt = {
            "A": fraction_text(accumulation),
            "amount": fraction_text(amount),
            "completion_state": "W8/W8/X1=0",
            "event_id": event_id,
            "internal_history_changed": internal_history_changed,
            "matter_id": matter_id,
            "matter_packet_ref": exact_value(matter_packet_ref),
            "operation": operation,
            "parent_payload": parent_payload,
            "phase_after": self.phase,
            "phase_before": before["phase"],
            "phase_event": phase_event,
            "r_s": fraction_text(r_s),
            "radius": fraction_text(radius),
            "rh_observer": {
                "connection_operator": None,
                "contact_direction": None,
                "formation_current": None,
                "source_cone_vector": None,
                "surface_operator_after": None,
                "surface_operator_before": None,
                "status": "SCHEMA_RESERVED_DORMANT",
            },
            "state_after": after,
            "state_after_sha256": after_hash,
            "state_before": before,
            "state_before_sha256": before_hash,
            "status": status,
            "theta_output": theta_output,
            "transient_state": transient_state,
        }
        return exact_value(receipt)


def execute_trace(
    trace_id: str,
    source_id: str,
    origin_mass: Fraction | int | str,
    events: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    state = HomeFormationState(source_id=source_id, origin_mass=Fraction(origin_mass))
    receipts = [state.apply(event) for event in events]
    return {
        "final_state": state.snapshot(),
        "final_state_sha256": record_sha256(state.snapshot()),
        "receipt_count": len(receipts),
        "receipts": receipts,
        "trace_id": trace_id,
    }
