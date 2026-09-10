"""Finite, exact QP particle grammar embedded in SAM Language v0.5.

This module contains constructor mathematics and canonical production values.
It has no dependency on the historical QP sidecar, UI, network, or physical
particle assignment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations_with_replacement
from typing import Any, Iterable

from .errors import QPDomainError


ALPHABET = (1, 2, 3, 4, 6, 8, 9, 12)
DEPTHS = (0, 1, 2)
ROUTES = ("plus", "minus", "neutral")
DEEP_CONJUGATE_EXCLUSIONS = frozenset({(8, 2), (9, 2), (12, 2)})

CARRIER_NATIVE: dict[str, Fraction] = {
    "TENSOR_CARRIER": Fraction(18),
    "ROAD_LIGHT_CARRIER": Fraction(0),
    "WEAK_VECTOR_CARRIER": Fraction(9),
    "NEUTRAL_VECTOR_CARRIER": Fraction(81),
    "COLOR_OWNER_CARRIER": Fraction(8),
    "A_FIELD_CARRIER": Fraction(0),
}

CONTROL_NAMES = (
    "DIRECT_QA_AS_MASS",
    "PROMOTE_TENSOR_CARRIER",
    "SKIP_LEDGER_COMPRESSION",
    "RANDOM_ROUTE_CLOSURE",
    "NEAREST_KNOWN_PARTICLE_MATCH",
    "OPEN_COLOR_NO_OWNER",
    "SURFACE_STACK_DISABLED",
    "FAKE_PARENT_NO_CLOSED_LOOP",
)


@dataclass(frozen=True)
class ProductionSpec:
    signature: str
    semantic_type: str
    census_role: str
    native_account: Fraction
    components: tuple[Any, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def record(self) -> dict[str, Any]:
        return {
            "signature": self.signature,
            "constructor": self.signature.split(":", 1)[0],
            "semantic_type": self.semantic_type,
            "census_role": self.census_role,
            "native_account": str(self.native_account),
            "components": "|".join(str(item) for item in self.components),
            "constituent_payload": bool(self.metadata.get("constituent_payload", True)),
            "semantic_scope": "STRUCTURAL_GRAMMAR",
        }


def _require_member(value: int, domain: Iterable[int], label: str) -> None:
    if value not in domain:
        raise QPDomainError(f"{label}={value} is outside the frozen QP domain")


def unary_native(p: int, depth: int, route: str) -> Fraction:
    _require_member(p, ALPHABET, "partition")
    _require_member(depth, DEPTHS, "depth")
    if route not in ROUTES:
        raise QPDomainError(f"route={route!r} is outside the frozen QP domain")
    factor = {
        "plus": Fraction(5, 4),
        "minus": Fraction(3, 2),
        "neutral": Fraction(1, 8),
    }[route]
    return Fraction(p * (12**depth)) * factor


def unary_direct(p: int, depth: int, route: str) -> ProductionSpec:
    return ProductionSpec(
        f"UD:{p}:{depth}:{route}",
        "QPUnaryDirectTemplate",
        "LEGAL_LOCAL_TEMPLATE",
        unary_native(p, depth, route),
        (p, depth, route),
        {"constituent_payload": True, "arity": 1, "constructor": "QP_UNARY_DIRECT"},
    )


def unary_conjugate(p: int, depth: int, route: str) -> ProductionSpec:
    unary_native(p, depth, route)
    if route == "neutral":
        raise QPDomainError("Neutral unary conjugation is unresolved and is not synthesized")
    if (p, depth) in DEEP_CONJUGATE_EXCLUSIONS:
        raise QPDomainError(f"Explicit deep conjugate is absent for p={p}, depth={depth}")
    return ProductionSpec(
        f"UC:{p}:{depth}:{route}",
        "QPUnaryConjugateTemplate",
        "LEGAL_LOCAL_TEMPLATE",
        unary_native(p, depth, route),
        (p, depth, route),
        {"constituent_payload": True, "arity": 1, "constructor": "QP_UNARY_CONJUGATE"},
    )


def ordered_pair(a: int, b: int) -> ProductionSpec:
    _require_member(a, ALPHABET, "left partition")
    _require_member(b, ALPHABET, "right partition")
    return ProductionSpec(
        f"OP:{a}:{b}",
        "QPOrderedPairTemplate",
        "LEGAL_LOCAL_TEMPLATE",
        Fraction(12 * a * b + 3 * abs(a - b)),
        (a, b),
        {
            "constituent_payload": False,
            "ordered": True,
            "arity": 2,
            "constructor": "QP_ORDERED_PAIR",
        },
    )


def unordered_triad_candidate(a: int, b: int, c: int) -> ProductionSpec:
    labels = tuple(sorted((a, b, c)))
    for value in labels:
        _require_member(value, ALPHABET, "triad partition")
    x, y, z = labels
    return ProductionSpec(
        f"UT:{x}+{y}+{z}",
        "QPUnorderedTriadCandidate",
        "CANDIDATE",
        Fraction(36 * (x * x + y * y + z * z)),
        labels,
        {
            "constituent_payload": False,
            "owner_occurrences": 3,
            "arity": 3,
            "constructor": "QP_UNORDERED_TRIAD",
        },
    )


def triad_surface_gate(candidate: ProductionSpec, allowed: set[str] | frozenset[str]) -> ProductionSpec:
    if candidate.semantic_type != "QPUnorderedTriadCandidate":
        raise QPDomainError("QP_TRIAD_SURFACE_GATE requires a QPUnorderedTriadCandidate")
    short = candidate.signature.split(":", 1)[1]
    if short not in allowed:
        raise QPDomainError(f"Triad {short} is a frozen rejected construction")
    metadata = dict(candidate.metadata)
    metadata.update({"surface_gate": "PASS", "constructor": "QP_TRIAD_SURFACE_GATE"})
    return ProductionSpec(
        candidate.signature,
        "QPLocalTriadTemplate",
        "LEGAL_LOCAL_TEMPLATE",
        candidate.native_account,
        candidate.components,
        metadata,
    )


def rejected_triad(candidate: ProductionSpec) -> ProductionSpec:
    metadata = dict(candidate.metadata)
    metadata.update({"surface_gate": "REJECTED", "candidate_type": candidate.semantic_type})
    return ProductionSpec(
        candidate.signature,
        "QPRejectedConstruction",
        "REJECTED",
        candidate.native_account,
        candidate.components,
        metadata,
    )


def hidden_support(p: int) -> ProductionSpec:
    _require_member(p, ALPHABET, "partition")
    return ProductionSpec(
        f"HS:{p}",
        "QPHiddenSupport",
        "INFRASTRUCTURE",
        Fraction(p) + Fraction(p * p, 144),
        (p,),
        {"constituent_payload": False, "arity": 0, "constructor": "QP_HIDDEN_SUPPORT"},
    )


def carrier_terminal(name: str) -> ProductionSpec:
    if name not in CARRIER_NATIVE:
        raise QPDomainError(f"Unknown frozen carrier terminal {name}")
    return ProductionSpec(
        f"CI:{name}",
        "QPCarrierInfrastructure",
        "INFRASTRUCTURE",
        CARRIER_NATIVE[name],
        (name,),
        {
            "constituent_payload": False,
            "source_defined": True,
            "arity": 0,
            "constructor": "QP_CARRIER_TERMINAL",
        },
    )


def scalar_parent() -> ProductionSpec:
    return ProductionSpec(
        "GS:HIGGS_REVEAL_PARENT",
        "QPGlobalScalarParent",
        "GLOBAL",
        Fraction(126000),
        (),
        {
            "multiplicity": "GLOBAL_ONCE",
            "source_defined": True,
            "constituent_payload": False,
            "arity": 0,
            "constructor": "QP_SCALAR_PARENT",
        },
    )


def explicit_control(name: str) -> ProductionSpec:
    if name not in CONTROL_NAMES:
        raise QPDomainError(f"Unknown frozen explicit control {name}")
    return ProductionSpec(
        f"XC:{name}",
        "QPRejectedConstruction",
        "REJECTED",
        Fraction(0),
        (name,),
        {
            "constituent_payload": False,
            "source_defined": True,
            "arity": 0,
            "constructor": "QP_EXPLICIT_CONTROL",
        },
    )


def enumerate_production_specs(allowed_triads: set[str] | frozenset[str]) -> list[ProductionSpec]:
    specs: list[ProductionSpec] = []
    for p in ALPHABET:
        for depth in DEPTHS:
            for route in ROUTES:
                specs.append(unary_direct(p, depth, route))
                if route != "neutral" and (p, depth) not in DEEP_CONJUGATE_EXCLUSIONS:
                    specs.append(unary_conjugate(p, depth, route))
    for a in ALPHABET:
        for b in ALPHABET:
            specs.append(ordered_pair(a, b))
    for labels in combinations_with_replacement(ALPHABET, 3):
        candidate = unordered_triad_candidate(*labels)
        short = candidate.signature.split(":", 1)[1]
        specs.append(
            triad_surface_gate(candidate, allowed_triads)
            if short in allowed_triads
            else rejected_triad(candidate)
        )
    specs.extend(hidden_support(p) for p in ALPHABET)
    specs.extend(carrier_terminal(name) for name in CARRIER_NATIVE)
    specs.append(scalar_parent())
    specs.extend(explicit_control(name) for name in CONTROL_NAMES)
    return sorted(specs, key=lambda spec: spec.signature)


def census_payload(specs: Iterable[ProductionSpec]) -> dict[str, Any]:
    rows = list(specs)
    by_constructor: dict[str, int] = {}
    by_role: dict[str, int] = {}
    admitted = rejected = 0
    for spec in rows:
        constructor = spec.signature.split(":", 1)[0]
        by_constructor[constructor] = by_constructor.get(constructor, 0) + 1
        by_role[spec.census_role] = by_role.get(spec.census_role, 0) + 1
        if constructor == "UT":
            if spec.census_role == "LEGAL_LOCAL_TEMPLATE":
                admitted += 1
            else:
                rejected += 1
    return {
        "status": "PASS",
        "total": len(rows),
        "constructors": dict(sorted(by_constructor.items())),
        "triad_candidates": admitted + rejected,
        "triad_admitted": admitted,
        "triad_rejected": rejected,
        "roles": dict(sorted(by_role.items())),
        "unique_signatures": len({spec.signature for spec in rows}),
    }
