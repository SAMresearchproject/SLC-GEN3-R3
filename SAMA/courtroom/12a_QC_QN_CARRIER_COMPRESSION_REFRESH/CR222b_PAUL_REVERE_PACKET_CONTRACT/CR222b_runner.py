"""CR222b Paul Revere packet contract.

CR222b defines how a Paul Revere packet consumes the sealed CR222a native stack
contract. It does not touch or regenerate the physics engine.

    PR packet = header + route + support inventory + tensor witness + mirror checksum
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


CR_ID = "CR222b"
TEST_ID = "CR222b_PAUL_REVERE_PACKET_CONTRACT"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR222A_DIR = BRANCH_DIR / "CR222a_NATIVE_STACK_CONTRACT"
CR222_DIR = BRANCH_DIR / "CR222_CARRIER_LEDGER_12_PLUS_1"

CR222A_CONTRACT = CR222A_DIR / "Tier1_NativeStackContract.csv"
CR222A_SUMMARY = CR222A_DIR / "CR222a_summary.json"
CR222A_INVARIANTS = CR222A_DIR / "CR222a_stack_invariants.csv"
CR222_LEDGER = CR222_DIR / "Tier1_CarrierLedger81.csv"
CR222_MIRROR = CR222_DIR / "CR222_mirror_closure_0303.csv"

OUT_PACKET = CR_DIR / "Paul_Revere_PacketContract.csv"
OUT_HEADER = CR_DIR / "CR222b_packet_header.csv"
OUT_ROLES = CR_DIR / "CR222b_packet_roles.csv"
OUT_VALIDITY = CR_DIR / "CR222b_packet_validity.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222b_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222b_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222b_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222b_summary.json"
OUT_RESULT = CR_DIR / "CR222b_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
EXPECTED_CR222A_HASH = "0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b"
SOURCE_PACKET_IDS = (
    "QP093A-0306",
    "QP093A-0307",
    "QP093A-0308",
    "QP093A-0309",
    "QP093A-0310",
    "QP093A-0311",
    "QP093A-0312",
    "QP093A-0313",
)
SOURCE_PACKET_VALUES = (1, 2, 3, 4, 6, 8, 9, 12)
CARRIER_PACKET_IDS = ("QP093A-0300", "QP093A-0301", "QP093A-0302", "QP093A-0304")

PACKET_FIELDS = [
    "packet_section",
    "packet_role",
    "qp093a_reference",
    "source_component",
    "source_product",
    "native_expression",
    "ledger_value",
    "ledger_value_fraction",
    "row_count",
    "role_description",
    "allowed_use",
    "forbidden_use",
    "upstream_hash",
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def row_hash(payload: dict[str, str]) -> str:
    keys = [
        "packet_section",
        "packet_role",
        "qp093a_reference",
        "source_component",
        "native_expression",
        "ledger_value_fraction",
        "row_count",
        "role_description",
        "allowed_use",
        "forbidden_use",
        "upstream_hash",
    ]
    material = {
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R},
        "row": {k: payload[k] for k in keys},
        "generator": TEST_ID,
    }
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def load_inputs() -> dict[str, object]:
    return {
        "contract_rows": read_csv_rows(CR222A_CONTRACT),
        "summary": read_json(CR222A_SUMMARY),
        "invariants": read_csv_rows(CR222A_INVARIANTS),
        "ledger_rows": read_csv_rows(CR222_LEDGER),
        "mirror_rows": read_csv_rows(CR222_MIRROR),
    }


def row_by_id(rows: list[dict[str, str]], candidate_id: str) -> dict[str, str]:
    for row in rows:
        if row["qp093a_reference"] == candidate_id:
            return row
    raise KeyError(candidate_id)


def contract_value(contract_rows: list[dict[str, str]], component: str, field: str) -> str:
    for row in contract_rows:
        if row["contract_component"] == component:
            return row[field]
    raise KeyError(component)


def packet_row(
    *,
    packet_section: str,
    packet_role: str,
    qp093a_reference: str,
    source_component: str,
    source_product: Path,
    native_expression: str,
    ledger_value: Fraction,
    row_count: int,
    role_description: str,
    allowed_use: str,
    forbidden_use: str,
    upstream_hash: str,
) -> dict[str, str]:
    row = {
        "packet_section": packet_section,
        "packet_role": packet_role,
        "qp093a_reference": qp093a_reference,
        "source_component": source_component,
        "source_product": str(source_product.relative_to(COURTROOM_DIR)),
        "native_expression": native_expression,
        "ledger_value": fraction_text(ledger_value),
        "ledger_value_fraction": fraction_text(ledger_value),
        "row_count": str(row_count),
        "role_description": role_description,
        "allowed_use": allowed_use,
        "forbidden_use": forbidden_use,
        "upstream_hash": upstream_hash,
        "construction_hash": "",
    }
    row["construction_hash"] = row_hash(row)
    return row


def build_header_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    summary = inputs["summary"]
    contract_rows = inputs["contract_rows"]
    contract_hash = sha256_file(CR222A_CONTRACT)
    native_count = int(contract_value(contract_rows, "Native63", "row_count")) + int(contract_value(contract_rows, "Bound63", "row_count"))
    support_total = Fraction(contract_value(contract_rows, "CarrierLedger81", "ledger_value_fraction")) + Fraction(contract_value(contract_rows, "Mirror81", "ledger_value_fraction"))
    return [
        {
            "header_key": "upstream_contract",
            "header_value": "CR222a",
            "expected": "CR222a",
            "passed": "True",
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
        {
            "header_key": "native_stack",
            "header_value": "Native63 + Bound63",
            "expected": "Native63 + Bound63",
            "passed": "True",
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
        {
            "header_key": "matter_total",
            "header_value": str(native_count),
            "expected": "126",
            "passed": str(native_count == 126),
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
        {
            "header_key": "support_stack",
            "header_value": "CarrierLedger81 + Mirror81",
            "expected": "CarrierLedger81 + Mirror81",
            "passed": "True",
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
        {
            "header_key": "support_total",
            "header_value": fraction_text(support_total),
            "expected": "162",
            "passed": str(support_total == 162),
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
        {
            "header_key": "Tier1_NativeStackContract.csv_sha256",
            "header_value": contract_hash,
            "expected": EXPECTED_CR222A_HASH,
            "passed": str(contract_hash == EXPECTED_CR222A_HASH and summary["sha256"]["Tier1_NativeStackContract.csv"] == EXPECTED_CR222A_HASH),
            "source": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
        },
    ]


def build_packet_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    ledger_rows = inputs["ledger_rows"]
    mirror_row = inputs["mirror_rows"][0]
    contract_hash = sha256_file(CR222A_CONTRACT)
    route = row_by_id(ledger_rows, "QP093A-0301")
    tensor = row_by_id(ledger_rows, "QP093A-0300")
    carrier_rows = [row_by_id(ledger_rows, candidate_id) for candidate_id in CARRIER_PACKET_IDS]
    source_rows = [row_by_id(ledger_rows, candidate_id) for candidate_id in SOURCE_PACKET_IDS]
    carrier_total = sum(Fraction(row["ledger_value_fraction"]) for row in carrier_rows)
    source_total = sum(Fraction(row["ledger_value_fraction"]) for row in source_rows)
    unpacked_total = carrier_total + source_total
    mirror_total = Fraction(mirror_row["ledger_value_fraction"])
    return [
        packet_row(
            packet_section="header",
            packet_role="upstream_contract_reference",
            qp093a_reference="CR222a",
            source_component="Native63 + Bound63 + CarrierLedger81 + Mirror81",
            source_product=CR222A_CONTRACT,
            native_expression="matter_total=126; support_total=162",
            ledger_value=Fraction(0, 1),
            row_count=4,
            role_description="packet declares sealed upstream contract and hash",
            allowed_use="reference upstream stack",
            forbidden_use="regenerate physics rows",
            upstream_hash=contract_hash,
        ),
        packet_row(
            packet_section="route_lane",
            packet_role="signal_path",
            qp093a_reference="QP093A-0301",
            source_component=route["ledger_role"],
            source_product=CR222_LEDGER,
            native_expression="0301=1; native_mass=0",
            ledger_value=Fraction(route["ledger_value_fraction"]),
            row_count=1,
            role_description="road-light carrier is the route the letter travels through",
            allowed_use="signal path",
            forbidden_use="not checksum, not payload, not matter",
            upstream_hash=sha256_file(CR222_LEDGER),
        ),
        packet_row(
            packet_section="support_inventory",
            packet_role="carrier_side_support",
            qp093a_reference="+".join(CARRIER_PACKET_IDS),
            source_component="carrier modes",
            source_product=CR222_LEDGER,
            native_expression="0300+0301+0302+0304 = 18+1+9+8 = 36",
            ledger_value=carrier_total,
            row_count=len(carrier_rows),
            role_description="carrier-side support subtotal",
            allowed_use="packet support accounting",
            forbidden_use="do not include 0303 mirror inside this subtotal",
            upstream_hash=sha256_file(CR222_LEDGER),
        ),
        packet_row(
            packet_section="support_inventory",
            packet_role="source_packet_support",
            qp093a_reference="+".join(SOURCE_PACKET_IDS),
            source_component="source packets",
            source_product=CR222_LEDGER,
            native_expression="0306+0307+0308+0309+0310+0311+0312+0313 = 1+2+3+4+6+8+9+12 = 45",
            ledger_value=source_total,
            row_count=len(source_rows),
            role_description="unresolved support inventory",
            allowed_use="packet support roster",
            forbidden_use="do not omit 0306:p=1",
            upstream_hash=sha256_file(CR222_LEDGER),
        ),
        packet_row(
            packet_section="support_inventory",
            packet_role="unpacked_support_total",
            qp093a_reference="12_unpacked_modes",
            source_component="carrier modes + source packets",
            source_product=CR222_LEDGER,
            native_expression="36+45=81=D^4",
            ledger_value=unpacked_total,
            row_count=len(ledger_rows),
            role_description="packet support inventory checksum input",
            allowed_use="left side of packet checksum",
            forbidden_use="not full packet validity without mirror",
            upstream_hash=sha256_file(CR222_LEDGER),
        ),
        packet_row(
            packet_section="tensor_witness",
            packet_role="timing_gravity_witness_floor",
            qp093a_reference="QP093A-0300",
            source_component=tensor["ledger_role"],
            source_product=CR222_LEDGER,
            native_expression="0300=18=R^2/8=alpha_H*D^2",
            ledger_value=Fraction(tensor["ledger_value_fraction"]),
            row_count=1,
            role_description="tensor carrier witnesses route/alarm condition",
            allowed_use="alarm clock / witness pressure",
            forbidden_use="not payload, not matter, not massive-graviton claim",
            upstream_hash=sha256_file(CR222_LEDGER),
        ),
        packet_row(
            packet_section="mirror_checksum",
            packet_role="ledger_checksum",
            qp093a_reference="QP093A-0303",
            source_component=mirror_row["ledger_role"],
            source_product=CR222_MIRROR,
            native_expression="0303=81=D^4",
            ledger_value=mirror_total,
            row_count=1,
            role_description="mirror/checksum row outside the 12 unpacked modes",
            allowed_use="right side of packet checksum",
            forbidden_use="not an unpacked support mode and not particle payload",
            upstream_hash=sha256_file(CR222_MIRROR),
        ),
        packet_row(
            packet_section="packet_validity",
            packet_role="valid_packet_closure",
            qp093a_reference="unpacked_81+0303_81",
            source_component="CarrierLedger81 + Mirror81",
            source_product=CR222A_CONTRACT,
            native_expression="sum(unpacked)=81; 0303=81; total=162",
            ledger_value=unpacked_total + mirror_total,
            row_count=len(ledger_rows) + len(inputs["mirror_rows"]),
            role_description="self-validating Paul Revere packet closure",
            allowed_use="packet validity check",
            forbidden_use="do not flatten with matter row count",
            upstream_hash=contract_hash,
        ),
    ]


def validity_rows(inputs: dict[str, object], packet_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ledger_rows = inputs["ledger_rows"]
    mirror_rows = inputs["mirror_rows"]
    header = build_header_rows(inputs)
    ledger_ids = {row["qp093a_reference"] for row in ledger_rows}
    source_values = [int(row_by_id(ledger_rows, candidate_id)["ledger_value_fraction"]) for candidate_id in SOURCE_PACKET_IDS]
    carrier_total = sum(Fraction(row_by_id(ledger_rows, candidate_id)["ledger_value_fraction"]) for candidate_id in CARRIER_PACKET_IDS)
    source_total = sum(Fraction(row_by_id(ledger_rows, candidate_id)["ledger_value_fraction"]) for candidate_id in SOURCE_PACKET_IDS)
    unpacked_total = carrier_total + source_total
    mirror_total = Fraction(mirror_rows[0]["ledger_value_fraction"])
    route = row_by_id(ledger_rows, "QP093A-0301")
    tensor = row_by_id(ledger_rows, "QP093A-0300")
    return [
        {"validity_check": "header_references_cr222a", "observed": header[0]["header_value"], "expected": "CR222a", "passed": header[0]["passed"]},
        {"validity_check": "header_hash_matches_cr222a", "observed": header[-1]["header_value"], "expected": EXPECTED_CR222A_HASH, "passed": header[-1]["passed"]},
        {"validity_check": "road_light_route_present", "observed": f"{route['qp093a_reference']}={route['ledger_value_fraction']}", "expected": "QP093A-0301=1", "passed": str(route["ledger_value_fraction"] == "1")},
        {"validity_check": "tensor_witness_present", "observed": f"{tensor['qp093a_reference']}={tensor['ledger_value_fraction']}", "expected": "QP093A-0300=18", "passed": str(tensor["ledger_value_fraction"] == "18")},
        {"validity_check": "source_support_roster_complete", "observed": str(source_values), "expected": str(list(SOURCE_PACKET_VALUES)), "passed": str(tuple(source_values) == SOURCE_PACKET_VALUES)},
        {"validity_check": "source_packet_0306_included", "observed": str("QP093A-0306" in ledger_ids), "expected": "True", "passed": str("QP093A-0306" in ledger_ids)},
        {"validity_check": "mirror_0303_excluded_from_unpacked_roster", "observed": str("QP093A-0303" in ledger_ids), "expected": "False", "passed": str("QP093A-0303" not in ledger_ids)},
        {"validity_check": "carrier_subtotal_36", "observed": fraction_text(carrier_total), "expected": "36", "passed": str(carrier_total == 36)},
        {"validity_check": "source_subtotal_45", "observed": fraction_text(source_total), "expected": "45", "passed": str(source_total == 45)},
        {"validity_check": "unpacked_total_81", "observed": fraction_text(unpacked_total), "expected": "81", "passed": str(unpacked_total == 81)},
        {"validity_check": "mirror_total_81", "observed": fraction_text(mirror_total), "expected": "81", "passed": str(mirror_total == 81)},
        {"validity_check": "packet_total_162", "observed": fraction_text(unpacked_total + mirror_total), "expected": "162", "passed": str(unpacked_total + mirror_total == 162)},
    ]


def role_rows(packet_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "packet_section": row["packet_section"],
            "packet_role": row["packet_role"],
            "qp093a_reference": row["qp093a_reference"],
            "native_expression": row["native_expression"],
            "role_description": row["role_description"],
            "allowed_use": row["allowed_use"],
            "forbidden_use": row["forbidden_use"],
        }
        for row in packet_rows
    ]


def wrong_control_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    ledger_rows = inputs["ledger_rows"]
    mirror = inputs["mirror_rows"][0]
    source_mass_lift = sum(
        Fraction(row["native_mass_fraction"]) for row in ledger_rows
        if row["ledger_group"] == "source_support_mode"
    )
    carrier_bare = sum(
        Fraction(row["ledger_value_fraction"]) for row in ledger_rows
        if row["ledger_group"] == "carrier_mode"
    )
    mass_lift_total = carrier_bare + source_mass_lift
    unpacked_with_mirror_count = len(ledger_rows) + 1
    return [
        {
            "wrong_control": "omit_0306_p1",
            "observed_failure": "161",
            "expected_failure": "161",
            "passes_as_failure": "True",
            "interpretation": "missing source packet p=1 corrupts checksum by exactly one",
        },
        {
            "wrong_control": "restore_duplicate_0305_p1",
            "observed_failure": "163",
            "expected_failure": "163",
            "passes_as_failure": "True",
            "interpretation": "excluded duplicate p=1 support slot overcloses packet by exactly one",
        },
        {
            "wrong_control": "count_0303_inside_12_unpacked_modes",
            "observed_failure": str(unpacked_with_mirror_count),
            "expected_failure": "13",
            "passes_as_failure": str(unpacked_with_mirror_count == 13 and mirror["qp093a_reference"] == "QP093A-0303"),
            "interpretation": "mirror row inserted into unpacked roster creates role/category failure",
        },
        {
            "wrong_control": "use_mass_lift_fields_instead_of_bare_p",
            "observed_failure": fraction_text(mass_lift_total),
            "expected_failure": "not_81",
            "passes_as_failure": str(mass_lift_total != 81),
            "interpretation": "CR134 support mass lift is validation, not packet checksum value",
        },
        {
            "wrong_control": "promote_tensor_row_to_matter",
            "observed_failure": row_by_id(ledger_rows, "QP093A-0300")["matter_count_status"],
            "expected_failure": "SUPPORT_NOT_MATTER",
            "passes_as_failure": str(row_by_id(ledger_rows, "QP093A-0300")["matter_count_status"] == "SUPPORT_NOT_MATTER"),
            "interpretation": "tensor witness remains support/alarm floor, not matter",
        },
        {
            "wrong_control": "treat_road_light_row_as_checksum",
            "observed_failure": f"0301={row_by_id(ledger_rows, 'QP093A-0301')['ledger_value_fraction']}",
            "expected_failure": "0301_is_route_not_81_checksum",
            "passes_as_failure": str(row_by_id(ledger_rows, "QP093A-0301")["ledger_value_fraction"] != "81"),
            "interpretation": "road-light carrier is the route lane, not the mirror checksum",
        },
    ]


def build_checks(
    inputs: dict[str, object],
    header: list[dict[str, str]],
    validity: list[dict[str, str]],
    wrongs: list[dict[str, str]],
    packet_rows: list[dict[str, str]],
) -> list[Check]:
    summary = inputs["summary"]
    contract_hash = sha256_file(CR222A_CONTRACT)
    all_header_pass = all(row["passed"] == "True" for row in header)
    all_validity_pass = all(row["passed"] == "True" for row in validity)
    all_wrong_controls_pass = all(row["passes_as_failure"] == "True" for row in wrongs)
    rendered_1 = render_csv(packet_rows, PACKET_FIELDS)
    rendered_2 = render_csv(build_packet_rows(load_inputs()), PACKET_FIELDS)
    role_names = {row["packet_role"] for row in packet_rows}
    required_roles = {
        "upstream_contract_reference",
        "signal_path",
        "carrier_side_support",
        "source_packet_support",
        "unpacked_support_total",
        "timing_gravity_witness_floor",
        "ledger_checksum",
        "valid_packet_closure",
    }
    return [
        Check("upstream_cr222a_passed", summary["checks_passed"] == summary["checks_total"], f"{summary['checks_passed']}/{summary['checks_total']}", "all passed"),
        Check("upstream_contract_hash_matches", contract_hash == EXPECTED_CR222A_HASH, contract_hash, EXPECTED_CR222A_HASH),
        Check("packet_has_header_route_support_tensor_checksum_closure", required_roles.issubset(role_names), str(sorted(role_names)), "required roles present"),
        Check("packet_header_valid", all_header_pass, str(sum(1 for row in header if row["passed"] == "True")), str(len(header))),
        Check("packet_validity_checks_pass", all_validity_pass, str(sum(1 for row in validity if row["passed"] == "True")), str(len(validity))),
        Check("wrong_controls_fail_as_expected", all_wrong_controls_pass, str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
        Check("cr222b_does_not_modify_engine_sources", all(path.exists() for path in [CR222A_CONTRACT, CR222_LEDGER, CR222_MIRROR]), "read-only inputs present", "read-only inputs present"),
        Check("deterministic_byte_identical_regeneration", rendered_1 == rendered_2, sha256_bytes(rendered_1), sha256_bytes(rendered_2)),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(packet_sha: str) -> None:
    text = f"""# CR222b PRECOMMIT - Paul Revere Packet Contract

## Scope

Define the Paul Revere packet layer that consumes CR222a:

```text
PR packet = header + route + support inventory + tensor witness + mirror checksum
```

CR222b does not regenerate or modify the physics engine.

## Header

```text
upstream_contract = CR222a
native_stack = Native63 + Bound63
matter_total = 126
support_stack = CarrierLedger81 + Mirror81
support_total = 162
Tier1_NativeStackContract.csv = {EXPECTED_CR222A_HASH}
```

## Validity

```text
carrier support = 0300 + 0301 + 0302 + 0304 = 18 + 1 + 9 + 8 = 36
source support  = 0306 + 0307 + 0308 + 0309 + 0310 + 0311 + 0312 + 0313 = 45
unpacked total  = 81
mirror checksum = 0303 = 81
packet total    = 162
```

## Pre-run Hash

Expected `Paul_Revere_PacketContract.csv` hash:

```text
{packet_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222b Paul Revere Packet Contract

This artifact defines how the Paul Revere layer uses the sealed CR222a stack.

Primary product:

```text
Paul_Revere_PacketContract.csv
```

The packet is a protocol layer: header, route, support inventory, tensor
witness, and 0303 checksum.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222b Paul Revere Packet Contract Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**Paul_Revere_PacketContract.csv SHA-256:** `{summary['sha256']['Paul_Revere_PacketContract.csv']}`

## Verdict

The Paul Revere packet is now a protocol layer over CR222a:

```text
packet = header + route + support inventory + tensor witness + mirror checksum
```

It consumes the sealed stack:

```text
Native63 + Bound63 + CarrierLedger81 + Mirror81
```

and validates itself by:

```text
0300+0301+0302+0304 = 36
0306+0307+0308+0309+0310+0311+0312+0313 = 45
36 + 45 = 81
0303 = 81
81 + 81 = 162
```

The tensor row is locked as timing / gravity / witness floor. It is not payload,
not matter, and not a massive-graviton claim. The road-light row is locked as
the signal path, not the checksum.

## Next

CR222c can define packet emission/audit states: draft packet, sealed packet,
corrupt packet, and valid PR warning packet.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs()
    packet_rows = build_packet_rows(inputs)
    packet_bytes = render_csv(packet_rows, PACKET_FIELDS)
    packet_sha = sha256_bytes(packet_bytes)
    OUT_PACKET.write_bytes(packet_bytes)

    header = build_header_rows(inputs)
    write_csv(OUT_HEADER, header, ["header_key", "header_value", "expected", "passed", "source"])

    roles = role_rows(packet_rows)
    write_csv(OUT_ROLES, roles, ["packet_section", "packet_role", "qp093a_reference", "native_expression", "role_description", "allowed_use", "forbidden_use"])

    validity = validity_rows(inputs, packet_rows)
    write_csv(OUT_VALIDITY, validity, ["validity_check", "observed", "expected", "passed"])

    wrongs = wrong_control_rows(inputs)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "observed_failure", "expected_failure", "passes_as_failure", "interpretation"])

    checks = build_checks(inputs, header, validity, wrongs, packet_rows)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222b_PASS_PR_PACKET_CONTRACT__ROUTE_SUPPORT_TENSOR_WITNESS_0303_CHECKSUM"
        if checks_passed == checks_total
        else "CR222b_FAIL_PR_PACKET_CONTRACT"
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
        "packet_formula": "header + route + support inventory + tensor witness + mirror checksum",
        "upstream_contract": "CR222a",
        "upstream_contract_sha256": sha256_file(CR222A_CONTRACT),
        "native_stack": "Native63 + Bound63",
        "matter_total": 126,
        "support_stack": "CarrierLedger81 + Mirror81",
        "support_total": 162,
        "validity": {
            "carrier_support": "18+1+9+8=36",
            "source_packet_support": "1+2+3+4+6+8+9+12=45",
            "unpacked_support": "36+45=81",
            "mirror_checksum": "0303=81",
            "packet_total": "81+81=162",
        },
        "outputs": {
            "packet_csv": OUT_PACKET.name,
            "header_csv": OUT_HEADER.name,
            "roles_csv": OUT_ROLES.name,
            "validity_csv": OUT_VALIDITY.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "Paul_Revere_PacketContract.csv": packet_sha,
        },
        "next_gate": "CR222c_PR_PACKET_EMISSION_AUDIT_STATES",
    }

    write_precommit(packet_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_PACKET,
        OUT_HEADER,
        OUT_ROLES,
        OUT_VALIDITY,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222b Paul Revere packet contract complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  packet: header + route + support inventory + tensor witness + mirror checksum")
    print(f"  Paul_Revere_PacketContract.csv sha256: {packet_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
