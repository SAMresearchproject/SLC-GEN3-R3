"""Scale-covariant A(r) and finite post-formation Home radius law."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Mapping

from .exact import exact_value, fraction_text, record_sha256


class RadialLawError(ValueError):
    """Raised when an event violates the frozen HOME-AR1 law."""


def positive(value: Fraction | int | str, name: str) -> Fraction:
    item = value if isinstance(value, Fraction) else Fraction(value)
    if item <= 0:
        raise RadialLawError(f"{name} must be strict positive")
    return item


@dataclass
class HomeRadialState:
    home_id: str
    depth: int
    formation_mass: Fraction
    radius_per_mass: Fraction
    x_inf: Fraction
    exterior_mass: Fraction = Fraction(0)
    event_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.formation_mass = positive(self.formation_mass, "formation_mass")
        self.radius_per_mass = positive(self.radius_per_mass, "radius_per_mass")
        self.x_inf = positive(self.x_inf, "x_inf")
        if self.depth < 0:
            raise RadialLawError("depth must be nonnegative")
        if self.exterior_mass < 0 or self.exterior_mass > self.max_exterior_mass:
            raise RadialLawError("exterior mass lies outside the finite Home interval")

    @property
    def formation_radius(self) -> Fraction:
        return self.radius_per_mass * self.formation_mass

    @property
    def total_mass(self) -> Fraction:
        return self.formation_mass + self.exterior_mass

    @property
    def schwarzschild_radius(self) -> Fraction:
        return self.radius_per_mass * self.total_mass

    @property
    def horizon_radius(self) -> Fraction:
        return self.schwarzschild_radius

    @property
    def normalized_exterior(self) -> Fraction:
        return self.exterior_mass / self.formation_mass

    @property
    def normalized_horizon_radius(self) -> Fraction:
        return self.horizon_radius / self.formation_radius

    @property
    def max_exterior_mass(self) -> Fraction:
        return self.x_inf * self.formation_mass

    @property
    def max_horizon_radius(self) -> Fraction:
        return self.formation_radius * (1 + self.x_inf)

    @property
    def available_capacity(self) -> Fraction:
        return self.max_exterior_mass - self.exterior_mass

    def accumulation_at(self, radius: Fraction | int | str) -> Fraction:
        r = positive(radius, "radius")
        return self.schwarzschild_radius / r

    def probe(self, horizon_multiplier: Fraction | int | str) -> dict[str, Any]:
        multiplier = positive(horizon_multiplier, "horizon_multiplier")
        radius = multiplier * self.horizon_radius
        accumulation = self.accumulation_at(radius)
        region = "HORIZON" if accumulation == 1 else ("EXTERIOR" if accumulation < 1 else "INTERIOR_NO_ORDINARY_CROSSING")
        return exact_value({
            "A": accumulation,
            "horizon_multiplier": multiplier,
            "radius": radius,
            "region": region,
        })

    def dimensionless_signature(self) -> dict[str, str]:
        return {
            "A_at_horizon": fraction_text(self.accumulation_at(self.horizon_radius)),
            "e": fraction_text(self.normalized_exterior),
            "rho_horizon": fraction_text(self.normalized_horizon_radius),
            "rho_minus_one_minus_e": fraction_text(self.normalized_horizon_radius - 1 - self.normalized_exterior),
        }

    def snapshot(self) -> dict[str, Any]:
        return exact_value({
            "available_capacity": self.available_capacity,
            "depth": self.depth,
            "event_ids": list(self.event_ids),
            "exterior_mass": self.exterior_mass,
            "formation_mass": self.formation_mass,
            "formation_radius": self.formation_radius,
            "home_id": self.home_id,
            "horizon_radius": self.horizon_radius,
            "max_exterior_mass": self.max_exterior_mass,
            "max_horizon_radius": self.max_horizon_radius,
            "normalized_exterior": self.normalized_exterior,
            "normalized_horizon_radius": self.normalized_horizon_radius,
            "radius_per_mass": self.radius_per_mass,
            "recursive_law": "A_H(rho,e)=(1+e)/rho",
            "schwarzschild_radius": self.schwarzschild_radius,
            "surface_A": self.accumulation_at(self.horizon_radius),
            "total_mass": self.total_mass,
            "x_inf": self.x_inf,
            "x_inf_home_cap_status": "EXPLORATORY_CANDIDATE",
        })

    def apply(self, raw_event: Mapping[str, Any]) -> dict[str, Any]:
        event = dict(raw_event)
        event_id = str(event.get("event_id", ""))
        operation = str(event.get("operation", ""))
        if not event_id or event_id in self.event_ids:
            raise RadialLawError("event_id must be nonempty and unique")
        before = self.snapshot()
        frozen_formation = self.formation_mass
        parent_retained = Fraction(0)
        parent_credit = Fraction(0)

        if operation == "ACCUMULATE":
            incoming = positive(event["amount"], "amount")
            accepted = min(incoming, self.available_capacity)
            parent_retained = incoming - accepted
            self.exterior_mass += accepted
            status = "SATURATION_REACHED_PARENT_RETAINS_OVERFLOW" if parent_retained > 0 else "HORIZON_EXPANDED_BY_EXTERIOR_CUSTODY"
            transfer = {
                "accepted_exterior": accepted,
                "incoming": incoming,
                "parent_retained_not_captured": parent_retained,
            }
        elif operation == "QW1_HR_RETURN":
            amount = positive(event["amount"], "amount")
            if amount > self.exterior_mass:
                raise RadialLawError("QW1/HR return exceeds exterior custody")
            self.exterior_mass -= amount
            parent_credit = amount
            status = "HORIZON_CONTRACTED_BY_REALIZED_QW1_HR_RETURN"
            transfer = {
                "formation_debit": Fraction(0),
                "parent_credit": parent_credit,
                "returned_exterior": amount,
            }
        else:
            raise RadialLawError(f"unsupported operation: {operation}")

        self.event_ids.append(event_id)
        if self.formation_mass != frozen_formation:
            raise AssertionError("formation floor changed")
        if not (0 <= self.exterior_mass <= self.max_exterior_mass):
            raise AssertionError("exterior custody escaped finite interval")
        if self.horizon_radius < self.formation_radius or self.horizon_radius > self.max_horizon_radius:
            raise AssertionError("horizon radius escaped finite interval")
        if self.accumulation_at(self.horizon_radius) != 1:
            raise AssertionError("moving surface left exact A=1")

        after = self.snapshot()
        return exact_value({
            "event_id": event_id,
            "operation": operation,
            "parent_credit": parent_credit,
            "parent_retained": parent_retained,
            "rh_observer": {"source_cone_vector": None, "status": "SCHEMA_RESERVED_DORMANT"},
            "state_after": after,
            "state_after_sha256": record_sha256(after),
            "state_before": before,
            "state_before_sha256": record_sha256(before),
            "status": status,
            "transfer": transfer,
        })


def execute_trace(spec: Mapping[str, Any], x_inf: Fraction) -> dict[str, Any]:
    state = HomeRadialState(
        str(spec["home_id"]), int(spec["depth"]), Fraction(spec["formation_mass"]),
        Fraction(spec["radius_per_mass"]), x_inf,
    )
    receipts = [state.apply(event) for event in spec["events"]]
    final = state.snapshot()
    return {
        "final_state": final,
        "final_state_sha256": record_sha256(final),
        "receipt_count": len(receipts),
        "receipts": receipts,
        "trace_id": spec["trace_id"],
    }


def recursion_atlas(depth_count: int, formation_at_depth, occupancy_ratios, probe_multipliers, x_inf: Fraction) -> list[dict[str, Any]]:
    rows = []
    for depth in range(depth_count):
        formation = formation_at_depth(depth)
        for occupancy in occupancy_ratios:
            e = Fraction(occupancy)
            state = HomeRadialState(
                f"HOME_DEPTH_{depth}", depth, formation, Fraction(1), x_inf,
                exterior_mass=formation * e,
            )
            rows.append(exact_value({
                "depth": depth,
                "dimensionless_signature": state.dimensionless_signature(),
                "formation_mass": formation,
                "formation_radius": state.formation_radius,
                "home_id": state.home_id,
                "occupancy_ratio": e,
                "probes": [state.probe(item) for item in probe_multipliers],
                "scale_from_root": formation / formation_at_depth(0),
            }))
    return rows

