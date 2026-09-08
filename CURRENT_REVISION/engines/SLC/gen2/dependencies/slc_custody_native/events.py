"""Typed custody events and explicit reset semantics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, getcontext
from enum import Enum

from .algebra import PrimeLogWeight


getcontext().prec = 50
K_B_EXACT_SI = Decimal("1.380649e-23")


class CustodyOperation(str, Enum):
    PERMUTE = "PERMUTE"
    HIDE = "HIDE"
    TRANSFER = "TRANSFER"
    MERGE = "MERGE"
    RELEASE = "RELEASE"
    RESET = "RESET"


@dataclass(frozen=True, slots=True)
class ResetRecord:
    schema: str
    morphism_id: str
    visible_fiber_multiplicity: int
    erased_information_exact_nats: str
    erased_information_nats: float
    erased_information_bits: float
    logical_reset_declared: bool
    physical_reset_declared: bool
    temperature_kelvin: str | None
    landauer_lower_bound_exact_joules: str | None
    landauer_lower_bound_joules: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def declare_reset(
    morphism_id: str,
    fiber_multiplicity: int,
    *,
    physical_reset_declared: bool = False,
    temperature_kelvin: Decimal | int | str | None = None,
) -> ResetRecord:
    """Declare receipt destruction; physical heat requires temperature."""

    weight = PrimeLogWeight.from_multiplicity(fiber_multiplicity)
    temperature_text: str | None = None
    exact_joules: str | None = None
    evaluated_joules: str | None = None

    if temperature_kelvin is not None:
        temperature = Decimal(str(temperature_kelvin))
        if temperature < 0:
            raise ValueError("temperature cannot be negative")
        temperature_text = str(temperature)
    else:
        temperature = None

    if physical_reset_declared:
        if temperature is None:
            raise ValueError("a physical reset requires temperature")
        exact_joules = f"k_B*{temperature_text}*({weight.expression})"
        evaluated_joules = str(K_B_EXACT_SI * temperature * Decimal(str(weight.nats)))

    return ResetRecord(
        schema="SLC_CUSTODY_NATIVE_RESET_RECORD_V1",
        morphism_id=morphism_id,
        visible_fiber_multiplicity=fiber_multiplicity,
        erased_information_exact_nats=weight.expression,
        erased_information_nats=weight.nats,
        erased_information_bits=weight.bits,
        logical_reset_declared=True,
        physical_reset_declared=physical_reset_declared,
        temperature_kelvin=temperature_text,
        landauer_lower_bound_exact_joules=exact_joules,
        landauer_lower_bound_joules=evaluated_joules,
    )

