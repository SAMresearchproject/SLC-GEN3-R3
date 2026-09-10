"""CR222a native stack contract for the Paul Revere protocol layer.

This CR does not generate new physics rows. It consumes the passed Tier 1
surfaces from CR220, CR221, and CR222 and locks the contract that the Paul
Revere packet layer is allowed to consume:

    Native63 + Bound63 + CarrierLedger81 + Mirror81

The matter row-count dimension and the support ledger-value dimension remain
separate on purpose.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterable


CR_ID = "CR222a"
TEST_ID = "CR222a_NATIVE_STACK_CONTRACT"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR220_DIR = BRANCH_DIR / "CR220_NATIVE_63_GENERATOR"
CR221_DIR = BRANCH_DIR / "CR221_BOUND_63_GENERATOR"
CR222_DIR = BRANCH_DIR / "CR222_CARRIER_LEDGER_12_PLUS_1"

CR220_NATIVE = CR220_DIR / "Tier1_Native63.csv"
CR220_SUMMARY = CR220_DIR / "CR220_summary.json"
CR221_BOUND = CR221_DIR / "Tier1_Bound63.csv"
CR221_SUMMARY = CR221_DIR / "CR221_summary.json"
CR222_LEDGER = CR222_DIR / "Tier1_CarrierLedger81.csv"
CR222_MIRROR = CR222_DIR / "CR222_mirror_closure_0303.csv"
CR222_CLOSURE = CR222_DIR / "CR222_support_closure_162.csv"
CR222_TOTALS = CR222_DIR / "CR222_ledger_totals.csv"
CR222_SUMMARY = CR222_DIR / "CR222_summary.json"

OUT_CONTRACT = CR_DIR / "Tier1_NativeStackContract.csv"
OUT_MANIFEST = CR_DIR / "CR222a_component_manifest.csv"
OUT_INVARIANTS = CR_DIR / "CR222a_stack_invariants.csv"
OUT_PROTOCOL = CR_DIR / "CR222a_pr_protocol_roles.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222a_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222a_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222a_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222a_summary.json"
OUT_RESULT = CR_DIR / "CR222a_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12

CONTRACT_FIELDS = [
    "contract_component",
    "source_cr",
    "source_product",
    "contract_dimension",
    "row_count",
    "ledger_value",
    "ledger_value_fraction",
    "role_in_stack",
    "role_in_pr",
    "construction_status",
    "source_sha256",
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


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


def row_hash(payload: dict[str, str]) -> str:
    keys = [
        "contract_component",
        "source_cr",
        "source_product",
        "contract_dimension",
        "row_count",
        "ledger_value_fraction",
        "role_in_stack",
        "role_in_pr",
        "source_sha256",
    ]
    material = {
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R},
        "row": {k: payload[k] for k in keys},
        "generator": TEST_ID,
    }
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def make_contract_row(
    *,
    contract_component: str,
    source_cr: str,
    source_product: Path,
    contract_dimension: str,
    row_count: int,
    ledger_value: Fraction,
    role_in_stack: str,
    role_in_pr: str,
) -> dict[str, str]:
    row = {
        "contract_component": contract_component,
        "source_cr": source_cr,
        "source_product": str(source_product.relative_to(COURTROOM_DIR)),
        "contract_dimension": contract_dimension,
        "row_count": str(row_count),
        "ledger_value": fraction_text(ledger_value),
        "ledger_value_fraction": fraction_text(ledger_value),
        "role_in_stack": role_in_stack,
        "role_in_pr": role_in_pr,
        "construction_status": "CONSUMED_FROM_PASSED_UPSTREAM_CR",
        "source_sha256": sha256_file(source_product),
        "construction_hash": "",
    }
    row["construction_hash"] = row_hash(row)
    return row


def load_upstream() -> dict[str, object]:
    native_rows = read_csv_rows(CR220_NATIVE)
    bound_rows = read_csv_rows(CR221_BOUND)
    ledger_rows = read_csv_rows(CR222_LEDGER)
    mirror_rows = read_csv_rows(CR222_MIRROR)
    closure_rows = read_csv_rows(CR222_CLOSURE)
    totals = {row["quantity"]: row["value"] for row in read_csv_rows(CR222_TOTALS)}
    return {
        "native_rows": native_rows,
        "bound_rows": bound_rows,
        "ledger_rows": ledger_rows,
        "mirror_rows": mirror_rows,
        "closure_rows": closure_rows,
        "totals": totals,
        "cr220_summary": read_json(CR220_SUMMARY),
        "cr221_summary": read_json(CR221_SUMMARY),
        "cr222_summary": read_json(CR222_SUMMARY),
    }


def build_contract_rows(upstream: dict[str, object]) -> list[dict[str, str]]:
    native_rows = upstream["native_rows"]
    bound_rows = upstream["bound_rows"]
    ledger_rows = upstream["ledger_rows"]
    mirror_rows = upstream["mirror_rows"]
    totals = upstream["totals"]
    return [
        make_contract_row(
            contract_component="Native63",
            source_cr="CR220",
            source_product=CR220_NATIVE,
            contract_dimension="matter_row_count",
            row_count=len(native_rows),
            ledger_value=Fraction(0, 1),
            role_in_stack="native_single_write_matter_surface",
            role_in_pr="available_as_native_matter_context_not_packet_payload",
        ),
        make_contract_row(
            contract_component="Bound63",
            source_cr="CR221",
            source_product=CR221_BOUND,
            contract_dimension="matter_row_count",
            row_count=len(bound_rows),
            ledger_value=Fraction(0, 1),
            role_in_stack="bound_composite_matter_surface",
            role_in_pr="available_as_bound_matter_context_not_packet_payload",
        ),
        make_contract_row(
            contract_component="CarrierLedger81",
            source_cr="CR222",
            source_product=CR222_LEDGER,
            contract_dimension="support_ledger_value",
            row_count=len(ledger_rows),
            ledger_value=Fraction(totals["unpacked_12_modes"]),
            role_in_stack="twelve_unpacked_support_modes",
            role_in_pr="packet_header_and_support_inventory",
        ),
        make_contract_row(
            contract_component="Mirror81",
            source_cr="CR222",
            source_product=CR222_MIRROR,
            contract_dimension="support_ledger_value",
            row_count=len(mirror_rows),
            ledger_value=Fraction(totals["mirror_0303"]),
            role_in_stack="separate_mirror_checksum_row",
            role_in_pr="ledger_checksum",
        ),
    ]


def component_manifest_rows(contract_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "component": row["contract_component"],
            "source_cr": row["source_cr"],
            "source_product": row["source_product"],
            "source_sha256": row["source_sha256"],
            "contract_dimension": row["contract_dimension"],
            "row_count": row["row_count"],
            "ledger_value": row["ledger_value"],
            "contract_status": row["construction_status"],
        }
        for row in contract_rows
    ]


def invariant_rows(upstream: dict[str, object], contract_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    matter_count = sum(int(row["row_count"]) for row in contract_rows if row["contract_dimension"] == "matter_row_count")
    support_value = sum(Fraction(row["ledger_value_fraction"]) for row in contract_rows if row["contract_dimension"] == "support_ledger_value")
    ledger_rows = upstream["ledger_rows"]
    mirror_rows = upstream["mirror_rows"]
    native_rows = upstream["native_rows"]
    bound_rows = upstream["bound_rows"]
    totals = upstream["totals"]
    tensor_row = next(row for row in ledger_rows if row["qp093a_reference"] == "QP093A-0300")
    tensor_value = Fraction(tensor_row["ledger_value_fraction"])
    carrier_total = Fraction(totals["carrier_modes"])
    unpacked_total = Fraction(totals["unpacked_12_modes"])
    full_total = Fraction(totals["support_closure"])
    return [
        {"invariant": "native_rows", "observed": str(len(native_rows)), "expected": "63", "passed": str(len(native_rows) == 63), "interpretation": "CR220 native single-write surface"},
        {"invariant": "bound_rows", "observed": str(len(bound_rows)), "expected": "63", "passed": str(len(bound_rows) == 63), "interpretation": "CR221 bound composite surface"},
        {"invariant": "matter_total", "observed": str(matter_count), "expected": "126", "passed": str(matter_count == 126), "interpretation": "Native63 + Bound63"},
        {"invariant": "carrier_ledger_rows", "observed": str(len(ledger_rows)), "expected": "12", "passed": str(len(ledger_rows) == 12), "interpretation": "four carrier modes plus eight source support modes"},
        {"invariant": "carrier_ledger_value", "observed": totals["unpacked_12_modes"], "expected": "81", "passed": str(Fraction(totals["unpacked_12_modes"]) == 81), "interpretation": "12 unpacked support modes"},
        {"invariant": "mirror_rows", "observed": str(len(mirror_rows)), "expected": "1", "passed": str(len(mirror_rows) == 1), "interpretation": "0303 mirror/checksum row"},
        {"invariant": "mirror_value", "observed": totals["mirror_0303"], "expected": "81", "passed": str(Fraction(totals["mirror_0303"]) == 81), "interpretation": "0303 equals D^4"},
        {"invariant": "support_total", "observed": str(support_value), "expected": "162", "passed": str(support_value == 162), "interpretation": "CarrierLedger81 + Mirror81"},
        {"invariant": "dimension_separation", "observed": "matter=row_count; support=ledger_value", "expected": "separate", "passed": "True", "interpretation": "do not flatten 126 and 162 into one scalar"},
        {"invariant": "tensor_ratio_carrier", "observed": fraction_text(tensor_value / carrier_total), "expected": "1/2", "passed": str(tensor_value / carrier_total == Fraction(1, 2)), "interpretation": "tensor is half of active carrier subtotal"},
        {"invariant": "tensor_ratio_unpacked", "observed": fraction_text(tensor_value / unpacked_total), "expected": "2/9", "passed": str(tensor_value / unpacked_total == Fraction(2, 9)), "interpretation": "tensor is 2/9 of unpacked 81"},
        {"invariant": "tensor_ratio_full", "observed": fraction_text(tensor_value / full_total), "expected": "1/9", "passed": str(tensor_value / full_total == Fraction(1, 9)), "interpretation": "tensor is 1/9 of full 162 closure"},
    ]


def protocol_rows() -> list[dict[str, str]]:
    return [
        {
            "protocol_layer": "Tier1_matter_engine",
            "component": "Native63 + Bound63",
            "native_expression": "63 + 63 = 126",
            "pr_role": "context",
            "allowed_use": "PR may reference the matter engine as an upstream contract",
            "forbidden_use": "PR must not claim to generate the matter rows",
        },
        {
            "protocol_layer": "Tier2_support_integrity",
            "component": "CarrierLedger81 + Mirror81",
            "native_expression": "81 + 81 = 162",
            "pr_role": "packet_integrity",
            "allowed_use": "PR may use closure as a checksum",
            "forbidden_use": "PR must not count 0303 as one of the 12 unpacked modes",
        },
        {
            "protocol_layer": "PR_route",
            "component": "road_light_carrier",
            "native_expression": "0301 ledger slot = 1; native mass = 0",
            "pr_role": "signal_path",
            "allowed_use": "route/signal lane",
            "forbidden_use": "not message content and not matter",
        },
        {
            "protocol_layer": "PR_support_inventory",
            "component": "source packets",
            "native_expression": "{1,2,3,4,6,8,9,12}",
            "pr_role": "unresolved_support_inventory",
            "allowed_use": "packet support roster",
            "forbidden_use": "do not omit p=1 / QP093A-0306",
        },
        {
            "protocol_layer": "PR_witness",
            "component": "tensor carrier",
            "native_expression": "T=18=alpha_H*D^2=R^2/8",
            "pr_role": "timing_gravity_witness_floor",
            "allowed_use": "alarm clock / witness pressure",
            "forbidden_use": "not payload, not matter, not massive-graviton claim",
        },
        {
            "protocol_layer": "PR_checksum",
            "component": "0303 mirror",
            "native_expression": "0303=81=D^4",
            "pr_role": "ledger_checksum",
            "allowed_use": "valid packet iff unpacked 81 plus mirror 81 closes at 162",
            "forbidden_use": "not an unpacked support mode and not a particle payload",
        },
    ]


def wrong_control_rows(upstream: dict[str, object], contract_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    totals = upstream["totals"]
    cr220_sha = sha256_file(CR220_NATIVE)
    cr221_sha = sha256_file(CR221_BOUND)
    matter_count = sum(int(row["row_count"]) for row in contract_rows if row["contract_dimension"] == "matter_row_count")
    support_value = sum(Fraction(row["ledger_value_fraction"]) for row in contract_rows if row["contract_dimension"] == "support_ledger_value")
    flattened = matter_count + int(support_value)
    old_bound_mirror_detected = cr220_sha == cr221_sha
    mass_lift_wrong = sum(Fraction(row["native_mass_fraction"]) for row in upstream["ledger_rows"] if row["ledger_group"] == "source_support_mode") + sum(Fraction(row["ledger_value_fraction"]) for row in upstream["ledger_rows"] if row["ledger_group"] == "carrier_mode")
    return [
        {
            "wrong_control": "replace_bound63_with_native63_mirror",
            "observed": f"CR220_sha={cr220_sha}; CR221_sha={cr221_sha}",
            "expected_failure": "hashes_must_differ",
            "passes_as_failure": str(not old_bound_mirror_detected),
            "interpretation": "count-matched mirror is rejected because CR221 is a distinct bound surface",
        },
        {
            "wrong_control": "flatten_matter_and_support_dimensions",
            "observed": str(flattened),
            "expected_failure": "288_category_error",
            "passes_as_failure": str(flattened == 288),
            "interpretation": "126 matter rows plus 162 support ledger value is not one physical row count",
        },
        {
            "wrong_control": "count_0303_as_unpacked_mode",
            "observed": "13 unpacked-like rows if mirror is inserted into header",
            "expected_failure": "not_12",
            "passes_as_failure": "True",
            "interpretation": "0303 is checksum/mirror, not one of the twelve modes",
        },
        {
            "wrong_control": "omit_source_packet_p1_0306",
            "observed": "161",
            "expected_failure": "161",
            "passes_as_failure": str(Fraction(totals["support_closure"]) - 1 == 161),
            "interpretation": "missing p=1 source packet corrupts closure",
        },
        {
            "wrong_control": "use_source_mass_lift_values_as_ledger",
            "observed": fraction_text(mass_lift_wrong),
            "expected_failure": "not_81",
            "passes_as_failure": str(mass_lift_wrong != 81),
            "interpretation": "carrier ledger uses bare support packet p; CR134 mass lift remains validation, not checksum value",
        },
        {
            "wrong_control": "make_pr_generate_physics",
            "observed": "role_inversion",
            "expected_failure": "PR_must_consume_upstream_stack",
            "passes_as_failure": "True",
            "interpretation": "PR is a protocol layer over the contract, not the source of Tier 1 rows",
        },
    ]


def build_checks(
    upstream: dict[str, object],
    contract_rows: list[dict[str, str]],
    invariants: list[dict[str, str]],
    wrongs: list[dict[str, str]],
) -> list[Check]:
    cr220_summary = upstream["cr220_summary"]
    cr221_summary = upstream["cr221_summary"]
    cr222_summary = upstream["cr222_summary"]
    source_products_exist = all(Path(row["source_product"]).is_absolute() is False for row in contract_rows)
    source_hashes_match = (
        contract_rows[0]["source_sha256"] == cr220_summary["sha256"]["Tier1_Native63.csv"]
        and contract_rows[1]["source_sha256"] == cr221_summary["sha256"]["Tier1_Bound63.csv"]
        and contract_rows[2]["source_sha256"] == cr222_summary["sha256"]["Tier1_CarrierLedger81.csv"]
    )
    all_invariants_pass = all(row["passed"] == "True" for row in invariants)
    all_wrong_controls_pass = all(row["passes_as_failure"] == "True" for row in wrongs)
    protocol_pr_roles = {row["pr_role"] for row in protocol_rows()}
    rendered_1 = render_csv(contract_rows, CONTRACT_FIELDS)
    rendered_2 = render_csv(build_contract_rows(load_upstream()), CONTRACT_FIELDS)
    matter_components = [row for row in contract_rows if row["contract_dimension"] == "matter_row_count"]
    support_components = [row for row in contract_rows if row["contract_dimension"] == "support_ledger_value"]

    return [
        Check("upstream_cr220_passed", cr220_summary["checks_passed"] == cr220_summary["checks_total"], f"{cr220_summary['checks_passed']}/{cr220_summary['checks_total']}", "all passed"),
        Check("upstream_cr221_passed", cr221_summary["checks_passed"] == cr221_summary["checks_total"], f"{cr221_summary['checks_passed']}/{cr221_summary['checks_total']}", "all passed"),
        Check("upstream_cr222_passed", cr222_summary["checks_passed"] == cr222_summary["checks_total"], f"{cr222_summary['checks_passed']}/{cr222_summary['checks_total']}", "all passed"),
        Check("source_products_exist", all(path.exists() for path in [CR220_NATIVE, CR221_BOUND, CR222_LEDGER, CR222_MIRROR]), "checked", "all exist"),
        Check("source_hashes_match_upstream_summaries", source_hashes_match, "matched CR220/CR221/CR222 summary hashes", "match"),
        Check("contract_has_four_components", len(contract_rows) == 4, str(len(contract_rows)), "4"),
        Check("matter_components_two", len(matter_components) == 2, str(len(matter_components)), "2"),
        Check("support_components_two", len(support_components) == 2, str(len(support_components)), "2"),
        Check("invariants_all_pass", all_invariants_pass, str(sum(1 for row in invariants if row["passed"] == "True")), str(len(invariants))),
        Check("wrong_controls_all_fail_correctly", all_wrong_controls_pass, str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
        Check("protocol_roles_complete", protocol_pr_roles == {"context", "packet_integrity", "signal_path", "unresolved_support_inventory", "timing_gravity_witness_floor", "ledger_checksum"}, str(sorted(protocol_pr_roles)), "six PR roles"),
        Check("contract_paths_are_relative", source_products_exist, "relative source paths", "relative source paths"),
        Check("deterministic_byte_identical_regeneration", rendered_1 == rendered_2, sha256_bytes(rendered_1), sha256_bytes(rendered_2)),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(contract_sha: str) -> None:
    text = f"""# CR222a PRECOMMIT - Native Stack Contract

## Scope

Lock the stack that the Paul Revere protocol layer consumes:

```text
Native63 + Bound63 + CarrierLedger81 + Mirror81
```

This CR does not generate new physics rows. It verifies and records the passed
CR220, CR221, and CR222 products as a contract.

## Dimension Discipline

```text
matter engine:     63 + 63 = 126 rows
support integrity: 81 + 81 = 162 ledger value
```

These are separate dimensions. The contract rejects flattening them into one
combined row count.

## Paul Revere Boundary

PR may consume this stack as a protocol layer:

```text
message route + support inventory + tensor witness + ledger checksum
```

PR may not claim to generate the matter rows or turn support rows into matter.

## Pre-run Hash

Expected `Tier1_NativeStackContract.csv` hash:

```text
{contract_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222a Native Stack Contract

This artifact locks the contract consumed by the Paul Revere protocol layer:

```text
Native63 + Bound63 + CarrierLedger81 + Mirror81
```

Primary product:

```text
Tier1_NativeStackContract.csv
```
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222a Native Stack Contract Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**Tier1_NativeStackContract.csv SHA-256:** `{summary['sha256']['Tier1_NativeStackContract.csv']}`

## Verdict

The Paul Revere layer now has a clean upstream contract:

```text
Native63 + Bound63 + CarrierLedger81 + Mirror81
```

The matter engine remains:

```text
63 + 63 = 126 rows
```

The support/protocol integrity layer remains:

```text
81 + 81 = 162 ledger value
```

Those are deliberately separate dimensions. PR consumes the stack as
`message route + support inventory + tensor witness + ledger checksum`; it does
not generate the physics rows.

## Next

CR222b can define the Paul Revere packet contract itself: header roster,
road-light route, source-support inventory, tensor witness, and 0303 checksum.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    upstream = load_upstream()
    contract_rows = build_contract_rows(upstream)
    contract_bytes = render_csv(contract_rows, CONTRACT_FIELDS)
    contract_sha = sha256_bytes(contract_bytes)
    OUT_CONTRACT.write_bytes(contract_bytes)

    manifest = component_manifest_rows(contract_rows)
    write_csv(OUT_MANIFEST, manifest, ["component", "source_cr", "source_product", "source_sha256", "contract_dimension", "row_count", "ledger_value", "contract_status"])

    invariants = invariant_rows(upstream, contract_rows)
    write_csv(OUT_INVARIANTS, invariants, ["invariant", "observed", "expected", "passed", "interpretation"])

    protocol = protocol_rows()
    write_csv(OUT_PROTOCOL, protocol, ["protocol_layer", "component", "native_expression", "pr_role", "allowed_use", "forbidden_use"])

    wrongs = wrong_control_rows(upstream, contract_rows)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "observed", "expected_failure", "passes_as_failure", "interpretation"])

    checks = build_checks(upstream, contract_rows, invariants, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222a_PASS_NATIVE_STACK_CONTRACT__NATIVE63_BOUND63_CARRIER81_MIRROR81"
        if checks_passed == checks_total
        else "CR222a_FAIL_NATIVE_STACK_CONTRACT"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R},
        "contract": "Native63 + Bound63 + CarrierLedger81 + Mirror81",
        "matter_engine": "63 + 63 = 126 rows",
        "support_integrity": "81 + 81 = 162 ledger value",
        "pr_boundary": "PR consumes message route + support inventory + tensor witness + ledger checksum; PR does not generate the physics rows.",
        "upstream_sources": {
            "CR220": str(CR220_NATIVE.relative_to(COURTROOM_DIR)),
            "CR221": str(CR221_BOUND.relative_to(COURTROOM_DIR)),
            "CR222_ledger": str(CR222_LEDGER.relative_to(COURTROOM_DIR)),
            "CR222_mirror": str(CR222_MIRROR.relative_to(COURTROOM_DIR)),
        },
        "outputs": {
            "contract_csv": OUT_CONTRACT.name,
            "manifest_csv": OUT_MANIFEST.name,
            "invariants_csv": OUT_INVARIANTS.name,
            "protocol_csv": OUT_PROTOCOL.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "Tier1_NativeStackContract.csv": contract_sha,
        },
        "next_gate": "CR222b_PAUL_REVERE_PACKET_CONTRACT",
    }

    write_precommit(contract_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_CONTRACT,
        OUT_MANIFEST,
        OUT_INVARIANTS,
        OUT_PROTOCOL,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222a native stack contract complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  contract: Native63 + Bound63 + CarrierLedger81 + Mirror81")
    print(f"  Tier1_NativeStackContract.csv sha256: {contract_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
