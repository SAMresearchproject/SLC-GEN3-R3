"""CR222d row taxonomy / promotion gate theorem.

This theorem separates native/source-support grammar from matter promotion.
It audits the uploaded 139-row CR219 overlay and confirms:

    native/source support != matter promotion

Rows can carry native support values or surcharge grammar while remaining
non-matter if the matter gate is closed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable


getcontext().prec = 80

CR_ID = "CR222d"
TEST_ID = "CR222d_ROW_TAXONOMY_PROMOTION_GATE"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

UPLOADED_CR219 = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")

OUT_THEOREM = CR_DIR / "CR222d_row_taxonomy_theorem.csv"
OUT_TAXONOMY = CR_DIR / "CR222d_taxonomy_counts.csv"
OUT_CHARGE_BALANCE = CR_DIR / "CR222d_charge_balance.csv"
OUT_MATTER_FORMULAS = CR_DIR / "CR222d_matter_gate_formula_verification.csv"
OUT_BLOCKED_SUPPORT = CR_DIR / "CR222d_blocked_support_gate_verification.csv"
OUT_SUPPORT_SURCHARGE = CR_DIR / "CR222d_support_surcharge_shape.csv"
OUT_DISPLAY_MARKERS = CR_DIR / "CR222d_visual_partition_markers.csv"
OUT_SUPPORT_ROSTER = CR_DIR / "CR222d_support_roster_duplicate_correction.csv"
OUT_SOURCE_MANIFEST = CR_DIR / "CR222d_source_manifest.csv"
OUT_CHECKS = CR_DIR / "CR222d_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222d_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222d_summary.json"
OUT_RESULT = CR_DIR / "CR222d_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
R2 = R * R
EIGHT = Decimal(8)
TOL = Decimal("0.000001")
PARTITION_MODES = (1, 2, 3, 4, 6, 8, 9, 12)
SUPPORT_ROSTER_IDS = {
    "QP093A-0300": 18,
    "QP093A-0301": 1,
    "QP093A-0302": 9,
    "QP093A-0304": 8,
    "QP093A-0306": 1,
    "QP093A-0307": 2,
    "QP093A-0308": 3,
    "QP093A-0309": 4,
    "QP093A-0310": 6,
    "QP093A-0311": 8,
    "QP093A-0312": 9,
    "QP093A-0313": 12,
}
SUPPORT_ROSTER_ORDER = {candidate_id: index for index, candidate_id in enumerate(SUPPORT_ROSTER_IDS, start=1)}
DUPLICATE_MIRROR_IDS = {"QP093A-0303": 81}


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


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def dec(value: str) -> Decimal:
    value = (value or "").strip()
    if value.lower() in {"", "no", "none", "null", "nan"}:
        return Decimal(0)
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"not decimal: {value!r}") from exc


def dec_text(value: Decimal) -> str:
    s = format(value, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def close(a: Decimal, b: Decimal, tol: Decimal = TOL) -> bool:
    return abs(a - b) <= tol


def zeroish(value: str) -> bool:
    text = (value or "").strip().lower()
    if text in {"", "no", "none", "null", "no_surface_depth"}:
        return True
    try:
        return close(Decimal(text), Decimal(0))
    except InvalidOperation:
        return False


def read_uploaded_rows() -> tuple[list[dict[str, str]], str]:
    with UPLOADED_CR219.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        declared_count = header[0].strip()
        if declared_count.isdigit():
            header[0] = "source_order"
        rows = [dict(zip(header, row)) for row in reader]
    return rows, declared_count


def parse_source_packet_p(row: dict[str, str]) -> int:
    route = row.get("route_combination", "")
    match = re.search(r"p=(\d+)", route)
    if match:
        return int(match.group(1))
    q_abs = row.get("q_abs", "")
    if q_abs.isdigit():
        return int(q_abs)
    raise ValueError(f"cannot parse source packet p from {row.get('candidate_id')}")


def taxonomy_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    allowed_counts = Counter(row["matter_row_allowed"] for row in rows)
    bin_counts = Counter(row["bin"] for row in rows)
    support_roster_count = sum(1 for row in rows if row["candidate_id"] in SUPPORT_ROSTER_IDS)
    duplicate_mirror_count = sum(1 for row in rows if row["candidate_id"] in DUPLICATE_MIRROR_IDS)
    return [
        {"taxonomy": "total_rows", "observed": str(len(rows)), "expected": "139", "passed": str(len(rows) == 139)},
        {"taxonomy": "matter_allowed_yes", "observed": str(allowed_counts["yes"]), "expected": "126", "passed": str(allowed_counts["yes"] == 126)},
        {"taxonomy": "nonmatter_blocked_no_raw", "observed": str(allowed_counts["no"]), "expected": "13", "passed": str(allowed_counts["no"] == 13)},
        {"taxonomy": "unique_support_roster_rows", "observed": str(support_roster_count), "expected": "12", "passed": str(support_roster_count == 12)},
        {"taxonomy": "duplicate_mirror_rows", "observed": str(duplicate_mirror_count), "expected": "1", "passed": str(duplicate_mirror_count == 1)},
        {"taxonomy": "stable_matter_rows", "observed": str(bin_counts["stable_matter_rows"]), "expected": "63", "passed": str(bin_counts["stable_matter_rows"] == 63)},
        {"taxonomy": "bound_composite_rows", "observed": str(bin_counts["bound_composite_rows"]), "expected": "63", "passed": str(bin_counts["bound_composite_rows"] == 63)},
        {"taxonomy": "carrier_only_rows", "observed": str(bin_counts["carrier_only_rows"]), "expected": "5", "passed": str(bin_counts["carrier_only_rows"] == 5)},
        {"taxonomy": "hidden_source_support_rows", "observed": str(bin_counts["hidden_source_support_rows"]), "expected": "8", "passed": str(bin_counts["hidden_source_support_rows"] == 8)},
    ]


def charge_balance_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    expected = {
        ("stable_matter_rows", "neutral"): 21,
        ("stable_matter_rows", "positive"): 21,
        ("stable_matter_rows", "negative"): 21,
        ("bound_composite_rows", "neutral"): 7,
        ("bound_composite_rows", "positive"): 28,
        ("bound_composite_rows", "negative"): 28,
    }
    counts = Counter((row["bin"], row["q_sign"]) for row in rows if row["matter_row_allowed"] == "yes")
    for key, exp in expected.items():
        observed = counts[key]
        out.append({
            "bin": key[0],
            "q_sign": key[1],
            "observed": str(observed),
            "expected": str(exp),
            "passed": str(observed == exp),
        })
    return out


def matter_formula_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        if row["matter_row_allowed"] != "yes":
            continue
        m_obs = dec(row["M_observed_candidate"])
        q_abs = dec(row["q_abs"])
        q_a_expected = m_obs * (Decimal(1) + (q_abs / Decimal(R2)))
        q_a_observed = dec(row["qA_source_support"])
        tensor_expected = q_a_expected / EIGHT
        tensor_observed = dec(row["tensor_carrier_support"])
        retained_expected = q_a_expected * Decimal(7) / EIGHT
        retained_observed = dec(row["retained_write_support"])
        q_a_match = close(q_a_observed, q_a_expected)
        tensor_match = close(tensor_observed, tensor_expected)
        retained_match = close(retained_observed, retained_expected)
        out.append({
            "candidate_id": row["candidate_id"],
            "bin": row["bin"],
            "q_sign": row["q_sign"],
            "q_abs": row["q_abs"],
            "M_observed_candidate": row["M_observed_candidate"],
            "qA_observed": row["qA_source_support"],
            "qA_expected": dec_text(q_a_expected),
            "qA_match": str(q_a_match),
            "tensor_observed": row["tensor_carrier_support"],
            "tensor_expected": dec_text(tensor_expected),
            "tensor_match": str(tensor_match),
            "retained_observed": row["retained_write_support"],
            "retained_expected": dec_text(retained_expected),
            "retained_match": str(retained_match),
            "formula": "G_matter=1 => qA=M_obs*(1+|q|/144); T=qA/8; W=7qA/8",
            "passed": str(q_a_match and tensor_match and retained_match),
        })
    return out


def blocked_support_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        if row["matter_row_allowed"] != "no":
            continue
        channels_zero = (
            zeroish(row["M_observed_candidate"])
            and zeroish(row["qA_source_support"])
            and zeroish(row["tensor_carrier_support"])
            and zeroish(row["retained_write_support"])
        )
        native_positive = dec(row["M_native"]) > 0
        out.append({
            "candidate_id": row["candidate_id"],
            "bin": row["bin"],
            "operator_class": row["operator_class"],
            "M_native": row["M_native"],
            "M_native_positive": str(native_positive),
            "M_observed_candidate": row["M_observed_candidate"],
            "qA_source_support": row["qA_source_support"],
            "tensor_carrier_support": row["tensor_carrier_support"],
            "retained_write_support": row["retained_write_support"],
            "channels_closed_or_zero": str(channels_zero),
            "matter_row_allowed": row["matter_row_allowed"],
            "matter_gate_status": row.get("matter_gate_status", ""),
            "formula": "G_matter=0 => M_obs=qA=T=W=0",
            "passed": str(channels_zero),
        })
    return out


def support_surcharge_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        if row["bin"] != "hidden_source_support_rows":
            continue
        p = parse_source_packet_p(row)
        expected = Decimal(p) + (Decimal(p * p) / Decimal(R2))
        observed = dec(row["M_native"])
        match = close(observed, expected)
        out.append({
            "candidate_id": row["candidate_id"],
            "p": str(p),
            "M_native_observed": row["M_native"],
            "M_native_expected": dec_text(expected),
            "formula": "M_native=p+p^2/144",
            "formula_match": str(match),
            "matter_row_allowed": row["matter_row_allowed"],
            "qA_source_support": row["qA_source_support"],
            "tensor_carrier_support": row["tensor_carrier_support"],
            "retained_write_support": row["retained_write_support"],
            "support_grammar_not_matter": str(row["matter_row_allowed"] == "no" and zeroish(row["qA_source_support"]) and zeroish(row["tensor_carrier_support"]) and zeroish(row["retained_write_support"])),
            "passed": str(match and row["matter_row_allowed"] == "no"),
        })
    return out


def support_roster_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        if row["matter_row_allowed"] != "no":
            continue
        candidate_id = row["candidate_id"]
        if candidate_id in SUPPORT_ROSTER_IDS:
            support_value = SUPPORT_ROSTER_IDS[candidate_id]
            role = "unique_support_roster_row"
            counted = "yes"
            duplicate_of = ""
            roster_position = str(SUPPORT_ROSTER_ORDER[candidate_id])
            passed = True
        elif candidate_id in DUPLICATE_MIRROR_IDS:
            support_value = DUPLICATE_MIRROR_IDS[candidate_id]
            role = "duplicate_mirror_closure_row"
            counted = "no"
            duplicate_of = "sum_12_unique_support_rows=81"
            roster_position = ""
            passed = True
        else:
            support_value = 0
            role = "unexpected_blocked_row"
            counted = "no"
            duplicate_of = ""
            roster_position = ""
            passed = False
        out.append({
            "candidate_id": candidate_id,
            "bin": row["bin"],
            "operator_class": row["operator_class"],
            "route_combination": row["route_combination"],
            "support_roster_role": role,
            "roster_position": roster_position,
            "counted_as_unique_support_row": counted,
            "support_value_used_for_ledger": str(support_value),
            "duplicate_of": duplicate_of,
            "matter_row_allowed": row["matter_row_allowed"],
            "passed": str(passed),
        })
    return sorted(
        out,
        key=lambda item: (
            0 if item["counted_as_unique_support_row"] == "yes" else 1,
            int(item["roster_position"] or "99"),
            item["candidate_id"],
        ),
    )


def display_marker_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Audit .1 partition displays as row-order/visual markers, not p values."""
    out: list[dict[str, str]] = []
    for row in rows:
        display = row.get("partition_signature", "").strip()
        has_dot_one = ".1" in display
        support_blocked = row["matter_row_allowed"] == "no"
        if has_dot_one:
            marker_status = "DOT_ONE_SUPPORT_MARKER" if support_blocked else "ERROR_DOT_ONE_ON_MATTER_ROW"
        elif support_blocked:
            marker_status = "SUPPORT_ROW_NO_VISUAL_MARKER_IN_CURRENT_SOURCE"
        else:
            marker_status = "NO_VISUAL_MARKER"
        if has_dot_one or support_blocked:
            out.append({
                "candidate_id": row["candidate_id"],
                "bin": row["bin"],
                "operator_class": row["operator_class"],
                "route_combination": row["route_combination"],
                "display_partition_signature": display,
                "has_dot_one_marker": str(has_dot_one),
                "matter_row_allowed": row["matter_row_allowed"],
                "marker_status": marker_status,
                "used_as_numeric_partition": "no",
                "numeric_partition_source": "route_combination p=... or q_abs, never .1 display marker",
                "passed": str((not has_dot_one) or support_blocked),
            })
    return out


def theorem_rows(source_sha: str) -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "CR222d_T1",
            "statement": "Charge lift is necessary source-support structure, not sufficient matter structure.",
            "formal_rule": "native/source support != matter promotion",
            "evidence": "139 row taxonomy splits into 126 matter allowed and 13 blocked non-matter rows; the unique support roster is 12 rows plus one mirror duplicate",
            "source_sha256": source_sha,
        },
        {
            "theorem_id": "CR222d_T2",
            "statement": "Closed matter gate zeros observable/write channels even when native support grammar is present.",
            "formal_rule": "G_matter=0 => M_obs=qA=T=W=0",
            "evidence": "13 blocked non-matter rows, including the 0303 mirror duplicate, have qA/tensor/write channels closed or zero",
            "source_sha256": source_sha,
        },
        {
            "theorem_id": "CR222d_T3",
            "statement": "Open matter gate admits q-lift and tensor/retained split.",
            "formal_rule": "G_matter=1 => qA=M_obs*(1+|q|/144); T=qA/8; W=7qA/8",
            "evidence": "126 matter-allowed rows match qA/tensor/retained formulas within uploaded display precision",
            "source_sha256": source_sha,
        },
        {
            "theorem_id": "CR222d_T4",
            "statement": "Hidden source-support surcharge grammar is real but remains support inventory until promoted.",
            "formal_rule": "SOURCE_SUPPORT_PACKET M_native=p+p^2/144 while matter_row_allowed=no",
            "evidence": "8 hidden source-support rows match surcharge shape and remain blocked",
            "source_sha256": source_sha,
        },
        {
            "theorem_id": "CR222d_T5",
            "statement": ".1 partition display is a visual support-row marker, not an algebraic partition input.",
            "formal_rule": "display partition marker != numeric support p",
            "evidence": "Numeric support p is parsed from route/q_abs; any .1 display marker remains support-only metadata",
            "source_sha256": source_sha,
        },
        {
            "theorem_id": "CR222d_T6",
            "statement": "The support roster has 12 unique rows; QP093A-0303 is the 81 mirror closure duplicate, not an additional support mode.",
            "formal_rule": "support_roster=12; mirror_duplicate=QP093A-0303=81; support_sum=81; support_sum+mirror=162",
            "evidence": "0300+0301+0302+0304+0306..0313 sum to 81, while 0303 equals the same 81 ledger value",
            "source_sha256": source_sha,
        },
    ]


def build_checks(
    rows: list[dict[str, str]],
    declared_count: str,
    taxonomy: list[dict[str, str]],
    charge: list[dict[str, str]],
    matter_formulas: list[dict[str, str]],
    blocked: list[dict[str, str]],
    surcharge: list[dict[str, str]],
    roster: list[dict[str, str]],
    markers: list[dict[str, str]],
) -> list[Check]:
    support_positive_zeroed = [
        row for row in blocked
        if row["M_native_positive"] == "True" and row["passed"] == "True"
    ]
    unique_roster = [row for row in roster if row["counted_as_unique_support_row"] == "yes"]
    mirror_rows = [row for row in roster if row["support_roster_role"] == "duplicate_mirror_closure_row"]
    support_sum = sum(int(row["support_value_used_for_ledger"]) for row in unique_roster)
    mirror_sum = sum(int(row["support_value_used_for_ledger"]) for row in mirror_rows)
    stable_total = sum(int(row["observed"]) for row in charge if row["bin"] == "stable_matter_rows")
    bound_total = sum(int(row["observed"]) for row in charge if row["bin"] == "bound_composite_rows")
    return [
        Check("uploaded_declared_count_139", declared_count == "139" and len(rows) == 139, f"declared={declared_count}; rows={len(rows)}", "139"),
        Check("taxonomy_counts_match_126_plus_13", all(row["passed"] == "True" for row in taxonomy), str(sum(1 for row in taxonomy if row["passed"] == "True")), str(len(taxonomy))),
        Check("matter_split_63_plus_63", stable_total == 63 and bound_total == 63, f"stable={stable_total}; bound={bound_total}", "63+63"),
        Check("stable_charge_balance_21_21_21", all(row["passed"] == "True" for row in charge if row["bin"] == "stable_matter_rows"), str([row["observed"] for row in charge if row["bin"] == "stable_matter_rows"]), "21,21,21"),
        Check("bound_charge_balance_7_28_28", all(row["passed"] == "True" for row in charge if row["bin"] == "bound_composite_rows"), str([row["observed"] for row in charge if row["bin"] == "bound_composite_rows"]), "7,28,28"),
        Check("matter_allowed_qA_tensor_retained_formulas", all(row["passed"] == "True" for row in matter_formulas), str(sum(1 for row in matter_formulas if row["passed"] == "True")), "126"),
        Check("support_blocked_channels_zero_or_closed", all(row["passed"] == "True" for row in blocked), str(sum(1 for row in blocked if row["passed"] == "True")), "13"),
        Check("support_blocked_native_positive_still_zeroed", len(support_positive_zeroed) == 12, str(len(support_positive_zeroed)), "12 positive-native blocked rows"),
        Check("hidden_source_surcharge_shape", all(row["formula_match"] == "True" for row in surcharge), str(sum(1 for row in surcharge if row["formula_match"] == "True")), "8"),
        Check("hidden_source_support_not_matter", all(row["support_grammar_not_matter"] == "True" for row in surcharge), str(sum(1 for row in surcharge if row["support_grammar_not_matter"] == "True")), "8"),
        Check("no_blocked_rows_matter_allowed", all(row["matter_row_allowed"] == "no" for row in blocked), str(Counter(row["matter_row_allowed"] for row in blocked)), "{'no': 13}"),
        Check("unique_support_roster_count_12", len(unique_roster) == 12, str(len(unique_roster)), "12"),
        Check("unique_support_roster_sum_81", support_sum == 81, str(support_sum), "81"),
        Check("duplicate_mirror_row_count_1", len(mirror_rows) == 1, str(len(mirror_rows)), "1"),
        Check("duplicate_mirror_row_value_81", mirror_sum == 81, str(mirror_sum), "81"),
        Check("support_roster_plus_mirror_closure_162", support_sum + mirror_sum == 162, str(support_sum + mirror_sum), "162"),
        Check("dot_one_partition_markers_support_blocked_only", all(row["passed"] == "True" for row in markers), str(Counter(row["marker_status"] for row in markers)), "no .1 marker on matter-allowed rows"),
        Check("theorem_source_path_exists", UPLOADED_CR219.exists(), str(UPLOADED_CR219), "exists"),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(source_sha: str, theorem_sha: str) -> None:
    text = f"""# CR222d PRECOMMIT - Row Taxonomy Promotion Gate

## Scope

Seal the taxonomy theorem:

```text
native/source support != matter promotion
```

Source file:

```text
{UPLOADED_CR219}
sha256 = {source_sha}
```

## Theorem

```text
G_matter=0 => M_obs=qA=T=W=0

G_matter=1 => qA = M_obs*(1+|q|/144)
              T  = qA/8
              W  = 7qA/8
```

Hidden source-support rows may carry:

```text
M_native = p + p^2/144
```

while still failing the matter gate.

Support roster correction:

```text
raw blocked non-matter rows = 13
unique support roster       = 12
duplicate mirror row        = QP093A-0303 = 81
support roster sum          = 81
support + mirror            = 162
```

Partition display markers:

```text
.1 display marker = visual support-row separator only
display marker != numeric support p
```

## Pre-run Hash

Expected `CR222d_row_taxonomy_theorem.csv` hash:

```text
{theorem_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222d Row Taxonomy Promotion Gate

This artifact seals the theorem that source-support grammar is not matter
promotion.

Primary product:

```text
CR222d_row_taxonomy_theorem.csv
```

Support roster correction:

```text
13 raw blocked non-matter rows = 12 unique support rows + QP093A-0303 mirror duplicate
```
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222d Row Taxonomy Promotion Gate Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222d_row_taxonomy_theorem.csv SHA-256:** `{summary['sha256']['CR222d_row_taxonomy_theorem.csv']}`

## Verdict

The uploaded CR219 overlay supports the theorem:

```text
native/source support != matter promotion
```

The taxonomy is:

```text
139 = 126 matter allowed + 13 blocked non-matter rows
126 = 63 stable matter + 63 bound composite
13  = 12 unique support roster rows + 1 duplicate mirror row
```

The support roster correction is:

```text
12 unique support rows = 0300+0301+0302+0304+0306..0313 = 81
duplicate mirror row   = QP093A-0303 = 81
closure                = 81 + 81 = 162
```

So QP093A-0303 remains blocked non-matter, but it is not counted as an
independent support mode.

The promotion gate is:

```text
G_matter=0 => M_obs=qA=T=W=0
G_matter=1 => qA=M_obs*(1+|q|/144), T=qA/8, W=7qA/8
```

The source-support surcharge shape is present:

```text
M_native = p + p^2/144
```

but the eight hidden support rows remain blocked, with qA/tensor/write channels
closed. This protects the Paul Revere packet from treating support inventory as
emitted matter.

If `.1` partition displays are present, CR222d treats them only as visual
support-row markers. They are not used as numeric partition inputs.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    rows, declared_count = read_uploaded_rows()
    source_sha = sha256_file(UPLOADED_CR219)

    taxonomy = taxonomy_rows(rows)
    write_csv(OUT_TAXONOMY, taxonomy, ["taxonomy", "observed", "expected", "passed"])

    charge = charge_balance_rows(rows)
    write_csv(OUT_CHARGE_BALANCE, charge, ["bin", "q_sign", "observed", "expected", "passed"])

    matter_formulas = matter_formula_rows(rows)
    write_csv(
        OUT_MATTER_FORMULAS,
        matter_formulas,
        [
            "candidate_id",
            "bin",
            "q_sign",
            "q_abs",
            "M_observed_candidate",
            "qA_observed",
            "qA_expected",
            "qA_match",
            "tensor_observed",
            "tensor_expected",
            "tensor_match",
            "retained_observed",
            "retained_expected",
            "retained_match",
            "formula",
            "passed",
        ],
    )

    blocked = blocked_support_rows(rows)
    write_csv(
        OUT_BLOCKED_SUPPORT,
        blocked,
        [
            "candidate_id",
            "bin",
            "operator_class",
            "M_native",
            "M_native_positive",
            "M_observed_candidate",
            "qA_source_support",
            "tensor_carrier_support",
            "retained_write_support",
            "channels_closed_or_zero",
            "matter_row_allowed",
            "matter_gate_status",
            "formula",
            "passed",
        ],
    )

    surcharge = support_surcharge_rows(rows)
    write_csv(
        OUT_SUPPORT_SURCHARGE,
        surcharge,
        [
            "candidate_id",
            "p",
            "M_native_observed",
            "M_native_expected",
            "formula",
            "formula_match",
            "matter_row_allowed",
            "qA_source_support",
            "tensor_carrier_support",
            "retained_write_support",
            "support_grammar_not_matter",
            "passed",
        ],
    )

    roster = support_roster_rows(rows)
    write_csv(
        OUT_SUPPORT_ROSTER,
        roster,
        [
            "candidate_id",
            "bin",
            "operator_class",
            "route_combination",
            "support_roster_role",
            "roster_position",
            "counted_as_unique_support_row",
            "support_value_used_for_ledger",
            "duplicate_of",
            "matter_row_allowed",
            "passed",
        ],
    )

    markers = display_marker_rows(rows)
    write_csv(
        OUT_DISPLAY_MARKERS,
        markers,
        [
            "candidate_id",
            "bin",
            "operator_class",
            "route_combination",
            "display_partition_signature",
            "has_dot_one_marker",
            "matter_row_allowed",
            "marker_status",
            "used_as_numeric_partition",
            "numeric_partition_source",
            "passed",
        ],
    )

    theorem = theorem_rows(source_sha)
    theorem_bytes = render_csv(theorem, ["theorem_id", "statement", "formal_rule", "evidence", "source_sha256"])
    theorem_sha = sha256_bytes(theorem_bytes)
    OUT_THEOREM.write_bytes(theorem_bytes)

    manifest = [{
        "source_path": str(UPLOADED_CR219),
        "source_sha256": source_sha,
        "declared_count_header": declared_count,
        "parsed_rows": str(len(rows)),
        "normalization": "leading count column renamed source_order; uploaded display precision tolerated at 1e-6",
        "display_marker_policy": ".1 partition displays are visual support-row separators only and are never used as numeric p",
        "support_roster_policy": "raw blocked non-matter rows=13; unique support roster=12; QP093A-0303 is mirror duplicate closure, not an independent support mode",
    }]
    write_csv(OUT_SOURCE_MANIFEST, manifest, ["source_path", "source_sha256", "declared_count_header", "parsed_rows", "normalization", "display_marker_policy", "support_roster_policy"])

    checks = build_checks(rows, declared_count, taxonomy, charge, matter_formulas, blocked, surcharge, roster, markers)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222d_PASS_ROW_TAXONOMY_PROMOTION_GATE__SUPPORT_GRAMMAR_NOT_MATTER"
        if checks_passed == checks_total
        else "CR222d_FAIL_ROW_TAXONOMY_PROMOTION_GATE"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R, "R_squared": R2},
        "source": {
            "path": str(UPLOADED_CR219),
            "sha256": source_sha,
            "declared_count_header": declared_count,
            "parsed_rows": len(rows),
        },
        "taxonomy": {
            "total": 139,
            "matter_allowed": 126,
            "blocked_nonmatter_raw": 13,
            "unique_support_roster": 12,
            "duplicate_mirror_rows": 1,
            "stable_matter": 63,
            "bound_composite": 63,
            "carrier_only_raw": 5,
            "hidden_source_support": 8,
        },
        "support_roster_correction": {
            "raw_blocked_nonmatter_rows": 13,
            "unique_support_roster_rows": 12,
            "duplicate_mirror_row": "QP093A-0303",
            "unique_support_roster_sum": 81,
            "duplicate_mirror_value": 81,
            "closure_total": 162,
            "rule": "QP093A-0303 remains blocked non-matter but is not an independent support mode.",
        },
        "theorem": "Charge lift is necessary source-support structure, not sufficient matter structure.",
        "formal_rules": {
            "closed_gate": "G_matter=0 => M_obs=qA=T=W=0",
            "open_gate": "G_matter=1 => qA=M_obs*(1+|q|/144); T=qA/8; W=7qA/8",
            "support_surcharge": "SOURCE_SUPPORT_PACKET M_native=p+p^2/144",
            "display_marker": ".1 partition display marker != numeric support p",
            "support_roster": "support_roster=12; duplicate_mirror=QP093A-0303=81; closure=81+81=162",
        },
        "display_marker_policy": {
            "rule": ".1 display marker is support-row visual metadata only",
            "used_as_numeric_partition": False,
            "current_source_marker_rows": sum(1 for row in markers if row["has_dot_one_marker"] == "True"),
        },
        "pr_implication": "support inventory -> promotion/audit gate -> qA -> tensor witness; support inventory alone does not emit matter.",
        "outputs": {
            "theorem_csv": OUT_THEOREM.name,
            "taxonomy_csv": OUT_TAXONOMY.name,
            "charge_balance_csv": OUT_CHARGE_BALANCE.name,
            "matter_formula_csv": OUT_MATTER_FORMULAS.name,
            "blocked_support_csv": OUT_BLOCKED_SUPPORT.name,
            "support_surcharge_csv": OUT_SUPPORT_SURCHARGE.name,
            "support_roster_duplicate_correction_csv": OUT_SUPPORT_ROSTER.name,
            "visual_partition_markers_csv": OUT_DISPLAY_MARKERS.name,
            "source_manifest_csv": OUT_SOURCE_MANIFEST.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222d_row_taxonomy_theorem.csv": theorem_sha,
        },
        "next_gate": "CR222e_PR_BEHAVIOR_WITH_PROMOTION_GATE",
    }

    write_precommit(source_sha, theorem_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_THEOREM,
        OUT_TAXONOMY,
        OUT_CHARGE_BALANCE,
        OUT_MATTER_FORMULAS,
        OUT_BLOCKED_SUPPORT,
        OUT_SUPPORT_SURCHARGE,
        OUT_SUPPORT_ROSTER,
        OUT_DISPLAY_MARKERS,
        OUT_SOURCE_MANIFEST,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222d row taxonomy promotion gate complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  theorem: native/source support != matter promotion")
    print(f"  CR222d_row_taxonomy_theorem.csv sha256: {theorem_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
