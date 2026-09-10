"""Independent finite reference enumerator for the frozen QP grammar.

This file intentionally imports no v0.5 runtime or constructor module.
"""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path


ALPHABET = (1, 2, 3, 4, 6, 8, 9, 12)
DEPTHS = (0, 1, 2)
ROUTES = ("plus", "minus", "neutral")
EXCLUSIONS = {(8, 2), (9, 2), (12, 2)}
CARRIERS = {
    "TENSOR_CARRIER": Fraction(18),
    "ROAD_LIGHT_CARRIER": Fraction(0),
    "WEAK_VECTOR_CARRIER": Fraction(9),
    "NEUTRAL_VECTOR_CARRIER": Fraction(81),
    "COLOR_OWNER_CARRIER": Fraction(8),
    "A_FIELD_CARRIER": Fraction(0),
}
CONTROLS = (
    "DIRECT_QA_AS_MASS",
    "PROMOTE_TENSOR_CARRIER",
    "SKIP_LEDGER_COMPRESSION",
    "RANDOM_ROUTE_CLOSURE",
    "NEAREST_KNOWN_PARTICLE_MATCH",
    "OPEN_COLOR_NO_OWNER",
    "SURFACE_STACK_DISABLED",
    "FAKE_PARENT_NO_CLOSED_LOOP",
)


def _record(signature, semantic_type, role, native, components, payload):
    return {
        "signature": signature,
        "constructor": signature.split(":", 1)[0],
        "semantic_type": semantic_type,
        "census_role": role,
        "native_account": str(native),
        "components": "|".join(str(item) for item in components),
        "constituent_payload": payload,
        "semantic_scope": "STRUCTURAL_GRAMMAR",
    }


def enumerate_reference(registry_dir: str | Path) -> list[dict]:
    with (Path(registry_dir) / "QP_TRIAD_ADMISSIBILITY.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        allowed = {
            row["signature"]
            for row in csv.DictReader(handle)
            if row["typed_guard_allowed"].lower() == "true"
        }
    rows = []
    for p in ALPHABET:
        for depth in DEPTHS:
            base = Fraction(p * 12**depth)
            for route in ROUTES:
                factor = {"plus": Fraction(5, 4), "minus": Fraction(3, 2), "neutral": Fraction(1, 8)}[route]
                native = base * factor
                rows.append(_record(f"UD:{p}:{depth}:{route}", "QPUnaryDirectTemplate", "LEGAL_LOCAL_TEMPLATE", native, (p, depth, route), True))
                if route != "neutral" and (p, depth) not in EXCLUSIONS:
                    rows.append(_record(f"UC:{p}:{depth}:{route}", "QPUnaryConjugateTemplate", "LEGAL_LOCAL_TEMPLATE", native, (p, depth, route), True))
    for a in ALPHABET:
        for b in ALPHABET:
            rows.append(_record(f"OP:{a}:{b}", "QPOrderedPairTemplate", "LEGAL_LOCAL_TEMPLATE", Fraction(12 * a * b + 3 * abs(a - b)), (a, b), False))
    for a, b, c in combinations_with_replacement(ALPHABET, 3):
        short = f"{a}+{b}+{c}"
        admitted = short in allowed
        rows.append(
            _record(
                f"UT:{short}",
                "QPLocalTriadTemplate" if admitted else "QPRejectedConstruction",
                "LEGAL_LOCAL_TEMPLATE" if admitted else "REJECTED",
                Fraction(36 * (a * a + b * b + c * c)),
                (a, b, c),
                False,
            )
        )
    for p in ALPHABET:
        rows.append(_record(f"HS:{p}", "QPHiddenSupport", "INFRASTRUCTURE", Fraction(p) + Fraction(p * p, 144), (p,), False))
    for name, native in CARRIERS.items():
        rows.append(_record(f"CI:{name}", "QPCarrierInfrastructure", "INFRASTRUCTURE", native, (name,), False))
    rows.append(_record("GS:HIGGS_REVEAL_PARENT", "QPGlobalScalarParent", "GLOBAL", Fraction(126000), (), False))
    for name in CONTROLS:
        rows.append(_record(f"XC:{name}", "QPRejectedConstruction", "REJECTED", Fraction(0), (name,), False))
    return sorted(rows, key=lambda row: row["signature"])


def main() -> int:
    candidate = Path(__file__).resolve().parents[1]
    print(json.dumps(enumerate_reference(candidate / "registry"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
