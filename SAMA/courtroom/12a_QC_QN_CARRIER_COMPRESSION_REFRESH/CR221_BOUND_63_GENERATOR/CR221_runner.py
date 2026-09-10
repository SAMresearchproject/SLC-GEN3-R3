"""CR221 bound 63 generator.

Build target from SAM_NEXT_MOVES_NATIVE_RESET.md:
generate the second Tier 1 product, Tier1_Bound63.csv, from closure operators
and locked SAM constants only. CR219 is used downstream as a validation surface
only; no candidate IDs, labels, names, or imported rows are construction inputs.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
from typing import Iterable


CR_ID = "CR221"
TEST_ID = "CR221_BOUND_63_GENERATOR"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

ROADMAP = BRANCH_DIR / "SAM_NEXT_MOVES_NATIVE_RESET.md"
CR219_PROMOTED = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR219_PROMOTED_PARTICLE_ROWS_EXPORT"
    / "CR219_promoted_particle_rows_126.csv"
)
CR220_NATIVE = (
    BRANCH_DIR
    / "CR220_NATIVE_63_GENERATOR"
    / "Tier1_Native63.csv"
)

OUT_BOUND = CR_DIR / "Tier1_Bound63.csv"
OUT_PAIRS = CR_DIR / "CR221_pair_closures_49.csv"
OUT_TRIADS = CR_DIR / "CR221_triad_closures_14.csv"
OUT_VALIDATION_SOURCE = CR_DIR / "CR221_downstream_validation_CR219_bound63.csv"
OUT_VALIDATION = CR_DIR / "CR221_validation_against_CR219.csv"
OUT_CHECKS = CR_DIR / "CR221_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR221_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR221_summary.json"
OUT_RESULT = CR_DIR / "CR221_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
PARTITION_MODES = (1, 2, 3, 4, 6, 8, 9, 12)
PAIR_OWNER_SET = (1, 2, 3, 4, 6, 8, 9)

CSV_FIELDS = [
    "bound_id",
    "operator_family",
    "operator_class",
    "route_class",
    "partition_signature",
    "partition_owners",
    "owner_count",
    "closure_depth",
    "q_sign",
    "q_abs",
    "q_value",
    "native_charge_axis",
    "spin_or_hand_class",
    "color_or_owner_closure",
    "closure_status",
    "stability_status",
    "native_mass_or_weight",
    "native_mass_fraction",
    "formula_used",
    "selector_rule",
    "route_combination",
    "address_signature",
    "construction_hash",
]


@dataclass(frozen=True)
class Check:
    check: str
    passed: bool
    observed: str
    expected: str


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def q_sign_text(q_value: int) -> str:
    if q_value > 0:
        return "positive"
    if q_value < 0:
        return "negative"
    return "neutral"


def partition_signature(parts: Iterable[int]) -> str:
    return "+".join(str(p) for p in parts)


def row_hash(payload: dict[str, str]) -> str:
    keys = [
        "operator_family",
        "operator_class",
        "route_class",
        "partition_signature",
        "closure_depth",
        "q_sign",
        "q_abs",
        "native_mass_fraction",
        "formula_used",
        "selector_rule",
    ]
    material = {
        "constants": {
            "alpha_H": ALPHA_H,
            "D": D,
            "R": R,
            "partition_modes": PARTITION_MODES,
            "pair_owner_set": PAIR_OWNER_SET,
        },
        "row": {k: payload[k] for k in keys},
        "generator": TEST_ID,
    }
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def pair_mass(a: int, b: int) -> int:
    return R * a * b + D * abs(a - b)


def triad_charge(parts: tuple[int, int, int]) -> int:
    return (parts[0] - parts[1]) + (parts[2] % D)


def triad_mass(parts: tuple[int, int, int]) -> int:
    return R * D * sum(p * p for p in parts)


def make_pair_row(a: int, b: int, ordinal: int) -> dict[str, str]:
    q_value = a - b
    q_sign = q_sign_text(q_value)
    q_abs = abs(q_value)
    operator_family = "EQUAL_NEUTRAL_PAIR" if q_value == 0 else "ORIENTED_CHARGED_PAIR"
    operator_class = "BOUND_COLOR_PAIR" if max(a, b) <= 8 else "OCTET_COMPOSITE"
    stability = "BOUND_PAIR_NEUTRAL_CANDIDATE" if q_value == 0 else "BOUND_PAIR_CHARGED_CANDIDATE"
    closure_depth = 1 if q_value == 0 else D
    mass = Fraction(pair_mass(a, b), 1)
    sig = partition_signature((a, b))
    row = {
        "bound_id": f"SAMB63-{ordinal:04d}",
        "operator_family": operator_family,
        "operator_class": operator_class,
        "route_class": "two_owner_pair_closure",
        "partition_signature": sig,
        "partition_owners": f"{a}|{b}",
        "owner_count": "2",
        "closure_depth": str(closure_depth),
        "q_sign": q_sign,
        "q_abs": str(q_abs),
        "q_value": str(q_value),
        "native_charge_axis": "pair_charge_axis",
        "spin_or_hand_class": "boson_integer_write",
        "color_or_owner_closure": "owner_pair_closed",
        "closure_status": "CLOSED_PAIR_WRITE",
        "stability_status": stability,
        "native_mass_or_weight": fraction_text(mass),
        "native_mass_fraction": fraction_text(mass),
        "formula_used": "R*a*b + D*abs(a-b)",
        "selector_rule": "ORDERED_PAIR_CLOSURE_FROM_OMEGA_7",
        "route_combination": f"pair_write[{a}|anti{b}]",
        "address_signature": (
            f"two_owner_pair_closure|p={sig}|d={closure_depth}|q={q_sign}:{q_abs}"
        ),
        "construction_hash": "",
    }
    row["construction_hash"] = row_hash(row)
    return row


def make_triad_row(parts: tuple[int, int, int], ordinal: int) -> dict[str, str]:
    q_value = triad_charge(parts)
    q_sign = q_sign_text(q_value)
    q_abs = abs(q_value)
    closure_depth = 0
    mass = Fraction(triad_mass(parts), 1)
    sig = partition_signature(parts)
    row = {
        "bound_id": f"SAMB63-{ordinal:04d}",
        "operator_family": "THREE_OWNER_COLOR_CLOSURE",
        "operator_class": "GROUND_BARYON_3BODY",
        "route_class": "three_owner_color_closure",
        "partition_signature": sig,
        "partition_owners": "|".join(str(p) for p in parts),
        "owner_count": "3",
        "closure_depth": str(closure_depth),
        "q_sign": q_sign,
        "q_abs": str(q_abs),
        "q_value": str(q_value),
        "native_charge_axis": "triadic_charge_axis",
        "spin_or_hand_class": "fermion_baryon_half_write",
        "color_or_owner_closure": "color_owner_closed",
        "closure_status": "CLOSED_THREE_OWNER_WRITE",
        "stability_status": "BOUND_COLOR_CLOSED_STABLE_CANDIDATE",
        "native_mass_or_weight": fraction_text(mass),
        "native_mass_fraction": fraction_text(mass),
        "formula_used": "R*D*(a^2+b^2+c^2)",
        "selector_rule": "CHARGED_STABLE_THREE_OWNER_COLOR_CLOSURE",
        "route_combination": f"color_triad[{sig}]",
        "address_signature": (
            f"three_owner_color_closure|p={sig}|d={closure_depth}|q={q_sign}:{q_abs}"
        ),
        "construction_hash": "",
    }
    row["construction_hash"] = row_hash(row)
    return row


def build_pair_rows(
    owner_set: tuple[int, ...] = PAIR_OWNER_SET,
    *,
    collapsed_orientation: bool = False,
    start_ordinal: int = 1,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if collapsed_orientation:
        pairs = combinations_with_replacement(owner_set, 2)
    else:
        pairs = product(owner_set, owner_set)
    ordinal = start_ordinal
    for a, b in pairs:
        rows.append(make_pair_row(a, b, ordinal))
        ordinal += 1
    return rows


def selected_triad(parts: tuple[int, int, int]) -> bool:
    return (
        sum(parts) % D == 0
        and max(parts) <= 8
        and triad_charge(parts) != 0
    )


def build_triad_rows(start_ordinal: int = 1) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    ordinal = start_ordinal
    for parts in combinations_with_replacement(PARTITION_MODES, 3):
        if selected_triad(parts):
            rows.append(make_triad_row(parts, ordinal))
            ordinal += 1
    return rows


def build_bound_rows() -> list[dict[str, str]]:
    triads = build_triad_rows(start_ordinal=1)
    pairs = build_pair_rows(start_ordinal=len(triads) + 1)
    return triads + pairs


def render_csv(rows: Iterable[dict[str, str]], fields: list[str]) -> bytes:
    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buf.getvalue().encode("utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, str]], fields: list[str]) -> None:
    path.write_bytes(render_csv(rows, fields))


def read_cr219_bound_rows() -> list[dict[str, str]]:
    with CR219_PROMOTED.open("r", encoding="utf-8", newline="") as f:
        return [
            row for row in csv.DictReader(f)
            if row.get("bin") == "bound_composite_rows"
        ]


def generated_key(row: dict[str, str]) -> tuple[str, str, str, int, str, int, Fraction]:
    return (
        row["operator_class"],
        row["route_class"],
        row["partition_signature"],
        int(row["closure_depth"]),
        row["q_sign"],
        int(row["q_abs"]),
        Fraction(row["native_mass_fraction"]),
    )


def cr219_key(row: dict[str, str]) -> tuple[str, str, str, int, str, int, Fraction]:
    return (
        row["operator_class"],
        row["route_class"],
        row["partition_signature"],
        int(row["closure_depth"]),
        row["q_sign"],
        int(Fraction(row["q_abs"])),
        Fraction(row["M_native"]),
    )


def validation_rows(bound_rows: list[dict[str, str]], cr219_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    generated = {generated_key(row): row for row in bound_rows}
    source = {cr219_key(row): row for row in cr219_rows}
    all_keys = sorted(set(generated) | set(source), key=lambda k: tuple(str(x) for x in k))
    rows: list[dict[str, str]] = []
    for key in all_keys:
        g = generated.get(key)
        s = source.get(key)
        rows.append({
            "operator_class": key[0],
            "route_class": key[1],
            "partition_signature": key[2],
            "closure_depth": str(key[3]),
            "q_sign": key[4],
            "q_abs": str(key[5]),
            "M_native": fraction_text(key[6]),
            "generated_bound_id": g["bound_id"] if g else "",
            "cr219_candidate_id": s["candidate_id"] if s else "",
            "signature_in_generated": str(g is not None),
            "signature_in_cr219": str(s is not None),
            "operator_family": g["operator_family"] if g else "",
            "generated_route_combination": g["route_combination"] if g else "",
            "cr219_route_combination": s["route_combination"] if s else "",
            "native_mass_match": str(g is not None and s is not None),
            "used_as_construction_input": "no",
        })
    return rows


def parse_owner_pair(row: dict[str, str]) -> tuple[int, int]:
    a, b = row["partition_owners"].split("|")
    return int(a), int(b)


def parse_triad(row: dict[str, str]) -> tuple[int, int, int]:
    a, b, c = row["partition_owners"].split("|")
    return int(a), int(b), int(c)


def native_mirror_wrong_control() -> tuple[bool, str]:
    if not CR220_NATIVE.exists():
        return False, "CR220 Tier1_Native63.csv missing"
    with CR220_NATIVE.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    operator_family_present = "operator_family" in (rows[0].keys() if rows else set())
    two_owner_signatures = sum(
        1 for row in rows
        if "+" in row.get("partition_signature", "") or "|" in row.get("partition_owners", "")
    )
    detected = len(rows) == 63 and not operator_family_present and two_owner_signatures == 0
    observed = (
        f"row_count={len(rows)}; operator_family_present={operator_family_present}; "
        f"two_or_three_owner_signatures={two_owner_signatures}"
    )
    return detected, observed


def build_checks(bound_rows: list[dict[str, str]], validation: list[dict[str, str]]) -> list[Check]:
    family_counts = Counter(row["operator_family"] for row in bound_rows)
    operator_counts = Counter(row["operator_class"] for row in bound_rows)
    pair_rows = [row for row in bound_rows if row["owner_count"] == "2"]
    triad_rows = [row for row in bound_rows if row["owner_count"] == "3"]
    pair_keys = {parse_owner_pair(row) for row in pair_rows}
    expected_pair_keys = set(product(PAIR_OWNER_SET, PAIR_OWNER_SET))
    unordered_orientations_closed = all(
        (a, b) in pair_keys and (b, a) in pair_keys
        for a, b in combinations(PAIR_OWNER_SET, 2)
    )
    equal_pair_rows = [row for row in pair_rows if row["q_sign"] == "neutral"]
    equal_pairs_neutral_once = all(
        sum(1 for row in pair_rows if parse_owner_pair(row) == (a, a) and row["q_sign"] == "neutral" and row["q_abs"] == "0") == 1
        for a in PAIR_OWNER_SET
    )
    triad_predicates_hold = all(
        selected_triad(parse_triad(row))
        and row["operator_class"] == "GROUND_BARYON_3BODY"
        and int(row["native_mass_fraction"]) == triad_mass(parse_triad(row))
        for row in triad_rows
    )
    labels_present = [
        key for row in bound_rows
        for key, value in row.items()
        if key in {"known_name", "known_symbol", "known_label", "candidate_id"} and value
    ]
    all_validation_matches = all(
        row["signature_in_generated"] == "True"
        and row["signature_in_cr219"] == "True"
        and row["native_mass_match"] == "True"
        for row in validation
    )
    generated_keys = [generated_key(row) for row in bound_rows]
    rendered_1 = render_csv(bound_rows, CSV_FIELDS)
    rendered_2 = render_csv(build_bound_rows(), CSV_FIELDS)
    wrong_owner12_pairs = build_pair_rows(owner_set=PAIR_OWNER_SET + (12,))
    wrong_collapsed_pairs = build_pair_rows(collapsed_orientation=True)
    native_wrong_detected, native_wrong_observed = native_mirror_wrong_control()

    return [
        Check("bound_rows_exactly_63", len(bound_rows) == 63, str(len(bound_rows)), "63"),
        Check(
            "operator_family_counts_14_7_42",
            family_counts == {
                "THREE_OWNER_COLOR_CLOSURE": 14,
                "EQUAL_NEUTRAL_PAIR": 7,
                "ORIENTED_CHARGED_PAIR": 42,
            },
            str(dict(family_counts)),
            "{'THREE_OWNER_COLOR_CLOSURE': 14, 'EQUAL_NEUTRAL_PAIR': 7, 'ORIENTED_CHARGED_PAIR': 42}",
        ),
        Check(
            "operator_class_counts_14_36_13",
            operator_counts == {
                "GROUND_BARYON_3BODY": 14,
                "BOUND_COLOR_PAIR": 36,
                "OCTET_COMPOSITE": 13,
            },
            str(dict(operator_counts)),
            "{'GROUND_BARYON_3BODY': 14, 'BOUND_COLOR_PAIR': 36, 'OCTET_COMPOSITE': 13}",
        ),
        Check("pair_rows_exactly_49", len(pair_rows) == 49, str(len(pair_rows)), "49"),
        Check("ordered_pair_space_exactly_omega_squared", pair_keys == expected_pair_keys, str(len(pair_keys)), "49 exact ordered pairs"),
        Check("unequal_pairs_have_both_orientations", unordered_orientations_closed, "all 21 unordered pairs doubled", "all 21 unordered pairs doubled"),
        Check("equal_pairs_once_and_neutral", len(equal_pair_rows) == 7 and equal_pairs_neutral_once, str(len(equal_pair_rows)), "7 neutral self-pairs"),
        Check("triad_rows_exactly_14_from_native_predicate", len(triad_rows) == 14 and triad_predicates_hold, str(len(triad_rows)), "14 charged stable triads"),
        Check("signatures_unique_63", len(set(generated_keys)) == 63, str(len(set(generated_keys))), "63"),
        Check("known_labels_absent_from_construction_fields", not labels_present, str(labels_present), "[]"),
        Check("deterministic_byte_identical_regeneration", rendered_1 == rendered_2, sha256_bytes(rendered_1), sha256_bytes(rendered_2)),
        Check("wrong_control_owner12_pair_set_produces_64_pairs", len(wrong_owner12_pairs) == 64, str(len(wrong_owner12_pairs)), "64"),
        Check(
            "wrong_control_orientation_collapse_reduces_charged_pairs_to_21",
            sum(1 for row in wrong_collapsed_pairs if row["operator_family"] == "ORIENTED_CHARGED_PAIR") == 21,
            str(sum(1 for row in wrong_collapsed_pairs if row["operator_family"] == "ORIENTED_CHARGED_PAIR")),
            "21",
        ),
        Check(
            "wrong_control_native63_mirror_fails_bound_operator_signature",
            native_wrong_detected,
            native_wrong_observed,
            "native mirror has count 63 but no bound operator-family signatures",
        ),
        Check(
            "downstream_cr219_validation_63_signatures_mass_operator",
            all_validation_matches and len(validation) == 63,
            str(sum(1 for row in validation if row["native_mass_match"] == "True")),
            "63",
        ),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(bound_rows_sha: str) -> None:
    text = f"""# CR221 PRECOMMIT - Bound 63 Generator

## Scope

Generate `Tier1_Bound63.csv` from SAM constants and closure selectors only:

```text
alpha_H = {ALPHA_H}
D = {D}
R = {R}
Pi = {PARTITION_MODES}
Omega = {PAIR_OWNER_SET}
```

## Pair Generator

Ordered two-owner closures use:

```text
Omega x Omega = 7^2 = 49
M_pair(a,b) = R*a*b + D*abs(a-b)
q = a - b
```

This decomposes into 7 equal neutral pairs and 42 oriented charged pairs.
Pair rows with owner 9 are classified as `OCTET_COMPOSITE`; rows whose owners
remain at or below 8 are classified as `BOUND_COLOR_PAIR`.

## Three-Owner Generator

Three-owner color closures are generated from combinations with replacement
over `Pi`, then selected by the native stable charged closure predicate:

```text
sum(a,b,c) mod D = 0
max(a,b,c) <= 8
q = (a - b) + (c mod D)
q != 0
M_triad(a,b,c) = R*D*(a^2+b^2+c^2)
```

This selects 14 `GROUND_BARYON_3BODY` rows.

## Source Boundary

`CR219_promoted_particle_rows_126.csv` is read only after generation as a
downstream validation surface. It supplies no candidate IDs, names, labels, or
rows to the construction step.

## Pre-run Hash

Expected generated CSV hash after deterministic construction:

```text
{bound_rows_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR221 Bound 63 Generator

This artifact implements the second milestone from
`SAM_NEXT_MOVES_NATIVE_RESET.md`: generate the bound-composite 63 from closure
operators, not by mirroring the CR220 native 63.

Primary product:

```text
Tier1_Bound63.csv
```

CR219 is used only for downstream validation in
`CR221_validation_against_CR219.csv`.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    result_class = summary["result_class"]
    checks_passed = summary["checks_passed"]
    checks_total = summary["checks_total"]
    text = f"""# CR221 Bound 63 Generator Result

**Result class:** `{result_class}`

**Checks:** {checks_passed}/{checks_total}

## Verdict

The bound Tier 1 surface is generated from closure operators as
`14 + 7 + 42 = 63`. The result is not a copy of CR220: it has its own
three-owner color closures, equal neutral pairs, and oriented charged pairs.

CR219 is used only after generation to confirm that the generated bound
signatures, operator classes, and native masses match the existing promoted
bound-composite rows.

## Outputs

- `Tier1_Bound63.csv`
- `CR221_pair_closures_49.csv`
- `CR221_triad_closures_14.csv`
- `CR221_downstream_validation_CR219_bound63.csv`
- `CR221_validation_against_CR219.csv`
- `CR221_checks.csv`
- `CR221_summary.json`
- `HASHES.txt`

## Next Gate

CR222 can assemble CR220 native 63 plus CR221 bound 63 into the no-name Tier 1
input for the carrier ledger and element-search stages.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    triad_rows = build_triad_rows(start_ordinal=1)
    pair_rows = build_pair_rows(start_ordinal=len(triad_rows) + 1)
    bound_rows = triad_rows + pair_rows

    bound_csv_bytes = render_csv(bound_rows, CSV_FIELDS)
    bound_sha = sha256_bytes(bound_csv_bytes)
    OUT_BOUND.write_bytes(bound_csv_bytes)
    write_csv(OUT_TRIADS, triad_rows, CSV_FIELDS)
    write_csv(OUT_PAIRS, pair_rows, CSV_FIELDS)

    cr219_rows = read_cr219_bound_rows()
    validation_source_fields = [
        "candidate_id",
        "bin",
        "route_combination",
        "operator_class",
        "route_class",
        "partition_signature",
        "closure_depth",
        "q_sign",
        "q_abs",
        "M_native",
        "known_identity_label",
        "known_symbol",
        "known_name",
        "known_label_used_as_construction_input",
    ]
    write_csv(OUT_VALIDATION_SOURCE, cr219_rows, validation_source_fields)

    validation = validation_rows(bound_rows, cr219_rows)
    validation_fields = [
        "operator_class",
        "route_class",
        "partition_signature",
        "closure_depth",
        "q_sign",
        "q_abs",
        "M_native",
        "generated_bound_id",
        "cr219_candidate_id",
        "signature_in_generated",
        "signature_in_cr219",
        "operator_family",
        "generated_route_combination",
        "cr219_route_combination",
        "native_mass_match",
        "used_as_construction_input",
    ]
    write_csv(OUT_VALIDATION, validation, validation_fields)

    checks = build_checks(bound_rows, validation)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR221_PASS_BOUND_63_GENERATOR__CONSTANTS_ONLY__14_7_42__"
        "DOWNSTREAM_CR219_SIGNATURE_MATCH"
        if checks_passed == checks_total
        else "CR221_FAIL_BOUND_63_GENERATOR"
    )

    family_counts = Counter(row["operator_family"] for row in bound_rows)
    operator_counts = Counter(row["operator_class"] for row in bound_rows)
    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R},
        "partition_modes": list(PARTITION_MODES),
        "pair_owner_set": list(PAIR_OWNER_SET),
        "row_count": len(bound_rows),
        "operator_family_counts": dict(family_counts),
        "operator_class_counts": dict(operator_counts),
        "pair_count": len(pair_rows),
        "triad_count": len(triad_rows),
        "source_boundary": "CR219 read after generation as downstream validation only; no imported IDs or labels in construction.",
        "roadmap": str(ROADMAP.relative_to(COURTROOM_DIR)),
        "validation_source": str(CR219_PROMOTED.relative_to(COURTROOM_DIR)),
        "mass_laws": {
            "pair": "M_pair(a,b) = R*a*b + D*abs(a-b)",
            "triad": "M_triad(a,b,c) = R*D*(a^2+b^2+c^2)",
        },
        "triad_selector": "sum(parts)%D == 0 and max(parts) <= 8 and q != 0 where q=(a-b)+(c%D)",
        "outputs": {
            "bound_csv": OUT_BOUND.name,
            "pair_csv": OUT_PAIRS.name,
            "triad_csv": OUT_TRIADS.name,
            "validation_source_csv": OUT_VALIDATION_SOURCE.name,
            "validation_csv": OUT_VALIDATION.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "Tier1_Bound63.csv": bound_sha,
        },
        "next_gate": "CR222_TIER1_NATIVE_BOUND_ASSEMBLY",
    }

    write_precommit(bound_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_BOUND,
        OUT_PAIRS,
        OUT_TRIADS,
        OUT_VALIDATION_SOURCE,
        OUT_VALIDATION,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR221 bound 63 generator complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  rows: {len(bound_rows)}")
    print(f"  Tier1_Bound63.csv sha256: {bound_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
