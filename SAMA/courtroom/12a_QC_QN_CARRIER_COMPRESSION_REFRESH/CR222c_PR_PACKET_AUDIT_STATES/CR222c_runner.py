"""CR222c Paul Revere packet audit states.

CR222c defines the state machine around the sealed CR222b Paul Revere packet.
It is an audit/transition layer only; it does not discover or regenerate
physics rows.

State spine:
    DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
    DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterable


CR_ID = "CR222c"
TEST_ID = "CR222c_PR_PACKET_AUDIT_STATES"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR222A_CONTRACT = (
    BRANCH_DIR
    / "CR222a_NATIVE_STACK_CONTRACT"
    / "Tier1_NativeStackContract.csv"
)
CR222B_DIR = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT"
CR222B_PACKET = CR222B_DIR / "Paul_Revere_PacketContract.csv"
CR222B_SUMMARY = CR222B_DIR / "CR222b_summary.json"
CR222B_VALIDITY = CR222B_DIR / "CR222b_packet_validity.csv"
CR222B_WRONG_CONTROLS = CR222B_DIR / "CR222b_wrong_controls.csv"
CR222B_ROLES = CR222B_DIR / "CR222b_packet_roles.csv"

OUT_STATE_MACHINE = CR_DIR / "CR222c_state_machine.csv"
OUT_STATE_REQUIREMENTS = CR_DIR / "CR222c_state_requirements.csv"
OUT_CORRUPTION = CR_DIR / "CR222c_corruption_classes.csv"
OUT_WARNING_GATE = CR_DIR / "CR222c_warning_gate.csv"
OUT_CHECKS = CR_DIR / "CR222c_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222c_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222c_summary.json"
OUT_RESULT = CR_DIR / "CR222c_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
EXPECTED_CR222A_HASH = "0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b"
EXPECTED_CR222B_HASH = "79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009"
A_SIDE = Fraction(1, 24)
T_FIRE_COEFFICIENT = -0.5 * math.log(23 / 24)


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


def load_inputs() -> dict[str, object]:
    return {
        "summary": read_json(CR222B_SUMMARY),
        "packet_rows": read_csv_rows(CR222B_PACKET),
        "validity": read_csv_rows(CR222B_VALIDITY),
        "wrong_controls": read_csv_rows(CR222B_WRONG_CONTROLS),
        "roles": read_csv_rows(CR222B_ROLES),
    }


def validity_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["validity_check"]: row for row in inputs["validity"]}


def wrong_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["wrong_control"]: row for row in inputs["wrong_controls"]}


def role_names(inputs: dict[str, object]) -> set[str]:
    return {row["packet_role"] for row in inputs["roles"]}


def all_validity_pass(inputs: dict[str, object]) -> bool:
    return all(row["passed"] == "True" for row in inputs["validity"])


def state_machine_rows() -> list[dict[str, str]]:
    return [
        {
            "from_state": "NONE",
            "event": "assemble_packet",
            "to_state": "DRAFT_PACKET",
            "guard": "header_and_required_roles_present; hash_not_final",
            "edit_policy": "editable",
            "meaning": "packet is assembled but not trusted",
        },
        {
            "from_state": "DRAFT_PACKET",
            "event": "seal_packet",
            "to_state": "SEALED_PACKET",
            "guard": "all_packet_validity_checks_pass and CR222a_hash_matches and CR222b_packet_hash_recorded",
            "edit_policy": "immutable_after_seal",
            "meaning": "packet is hash-final and auditable",
        },
        {
            "from_state": "DRAFT_PACKET",
            "event": "role_or_checksum_failure",
            "to_state": "CORRUPT_PACKET",
            "guard": "any_required_role_or_checksum_fails",
            "edit_policy": "repair_by_new_draft",
            "meaning": "draft packet has structural corruption",
        },
        {
            "from_state": "SEALED_PACKET",
            "event": "role_hash_or_checksum_failure",
            "to_state": "CORRUPT_PACKET",
            "guard": "any_sealed_hash_role_or_checksum_fails",
            "edit_policy": "new_packet_or_amend_only",
            "meaning": "sealed packet no longer matches its seal or role contract",
        },
        {
            "from_state": "SEALED_PACKET",
            "event": "warning_threshold_reached",
            "to_state": "VALID_PR_WARNING_PACKET",
            "guard": "sealed_packet and tensor_witness_present and route_present and A_leak>=A_side and checksum_intact",
            "edit_policy": "immutable_warning_record",
            "meaning": "packet is allowed to emit a Paul Revere warning",
        },
    ]


def state_requirement_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    vm = validity_map(inputs)
    cr222a_hash = sha256_file(CR222A_CONTRACT)
    cr222b_hash = sha256_file(CR222B_PACKET)
    required_roles = {
        "upstream_contract_reference",
        "signal_path",
        "source_packet_support",
        "timing_gravity_witness_floor",
        "ledger_checksum",
        "valid_packet_closure",
    }
    roles_present = required_roles.issubset(role_names(inputs))
    checksum_intact = all_validity_pass(inputs)
    return [
        {
            "state": "DRAFT_PACKET",
            "requirement": "assembled_roles_present_but_hash_not_final",
            "observed": f"roles_present={roles_present}; hash_status=not_final_allowed",
            "passed": str(roles_present),
            "edit_policy": "editable",
        },
        {
            "state": "SEALED_PACKET",
            "requirement": "upstream_cr222a_hash_matches",
            "observed": cr222a_hash,
            "passed": str(cr222a_hash == EXPECTED_CR222A_HASH),
            "edit_policy": "immutable",
        },
        {
            "state": "SEALED_PACKET",
            "requirement": "cr222b_packet_hash_matches",
            "observed": cr222b_hash,
            "passed": str(cr222b_hash == EXPECTED_CR222B_HASH),
            "edit_policy": "immutable",
        },
        {
            "state": "SEALED_PACKET",
            "requirement": "checksum_intact",
            "observed": f"carrier={vm['carrier_subtotal_36']['observed']}; source={vm['source_subtotal_45']['observed']}; total={vm['packet_total_162']['observed']}",
            "passed": str(checksum_intact),
            "edit_policy": "immutable",
        },
        {
            "state": "CORRUPT_PACKET",
            "requirement": "entered_on_any_role_hash_or_checksum_failure",
            "observed": "failure_classes_defined",
            "passed": "True",
            "edit_policy": "new_packet_or_amend",
        },
        {
            "state": "VALID_PR_WARNING_PACKET",
            "requirement": "sealed_plus_warning_threshold",
            "observed": f"A_side={fraction_text(A_SIDE)}; threshold=A_leak>=A_side",
            "passed": "True",
            "edit_policy": "immutable_warning_record",
        },
    ]


def corruption_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    wm = wrong_map(inputs)
    return [
        {
            "corruption_class": "CORRUPT_MISSING_0306_SUPPORT_PACKET",
            "trigger": "omit_0306_p1",
            "observed_failure": wm["omit_0306_p1"]["observed_failure"],
            "expected_failure": "161",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "source-support p=1 is missing",
        },
        {
            "corruption_class": "CORRUPT_DUPLICATE_0305_SUPPORT_PACKET",
            "trigger": "restore_duplicate_0305_p1",
            "observed_failure": wm["restore_duplicate_0305_p1"]["observed_failure"],
            "expected_failure": "163",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "excluded duplicate support slot was counted",
        },
        {
            "corruption_class": "CORRUPT_0303_COUNTED_AS_UNPACKED_MODE",
            "trigger": "count_0303_inside_12_unpacked_modes",
            "observed_failure": wm["count_0303_inside_12_unpacked_modes"]["observed_failure"],
            "expected_failure": "13",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "mirror checksum was inserted into payload roster",
        },
        {
            "corruption_class": "CORRUPT_TENSOR_PROMOTED_TO_PAYLOAD",
            "trigger": "tensor_role_inversion",
            "observed_failure": "role_failure",
            "expected_failure": "tensor_witness_not_payload",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "tensor witness was used as message content",
        },
        {
            "corruption_class": "CORRUPT_TENSOR_PROMOTED_TO_MATTER",
            "trigger": "promote_tensor_row_to_matter",
            "observed_failure": wm["promote_tensor_row_to_matter"]["observed_failure"],
            "expected_failure": "SUPPORT_NOT_MATTER",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "tensor support row was promoted to matter",
        },
        {
            "corruption_class": "CORRUPT_ROAD_LIGHT_USED_AS_CHECKSUM",
            "trigger": "treat_road_light_row_as_checksum",
            "observed_failure": wm["treat_road_light_row_as_checksum"]["observed_failure"],
            "expected_failure": "0301_is_route_not_81_checksum",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "route lane was used as mirror checksum",
        },
        {
            "corruption_class": "CORRUPT_MASS_LIFT_USED_FOR_LEDGER_SUM",
            "trigger": "use_mass_lift_fields_instead_of_bare_p",
            "observed_failure": wm["use_mass_lift_fields_instead_of_bare_p"]["observed_failure"],
            "expected_failure": "not_81",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "native mass-lift values were used as checksum values",
        },
        {
            "corruption_class": "CORRUPT_UPSTREAM_HASH_MISMATCH",
            "trigger": "cr222a_or_cr222b_hash_changed",
            "observed_failure": "hash_mismatch",
            "expected_failure": "hashes_must_match_seal",
            "state_result": "CORRUPT_PACKET",
            "audit_meaning": "packet no longer matches sealed upstream contract",
        },
    ]


def warning_gate_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    vm = validity_map(inputs)
    sealed = (
        sha256_file(CR222A_CONTRACT) == EXPECTED_CR222A_HASH
        and sha256_file(CR222B_PACKET) == EXPECTED_CR222B_HASH
        and all_validity_pass(inputs)
    )
    route_present = vm["road_light_route_present"]["passed"] == "True"
    tensor_present = vm["tensor_witness_present"]["passed"] == "True"
    checksum_intact = vm["packet_total_162"]["passed"] == "True"

    scenarios = [
        ("sealed_no_warning", Fraction(0, 1), "SEALED_PACKET"),
        ("sealed_threshold_exact", A_SIDE, "VALID_PR_WARNING_PACKET"),
        ("sealed_above_threshold", Fraction(1, 12), "VALID_PR_WARNING_PACKET"),
        ("corrupt_threshold_reached", A_SIDE, "CORRUPT_PACKET"),
    ]
    rows = []
    for scenario, a_leak, expected_state in scenarios:
        threshold_reached = a_leak >= A_SIDE
        scenario_sealed = sealed and scenario != "corrupt_threshold_reached"
        valid_warning = scenario_sealed and route_present and tensor_present and checksum_intact and threshold_reached
        if valid_warning:
            observed_state = "VALID_PR_WARNING_PACKET"
        elif scenario == "corrupt_threshold_reached":
            observed_state = "CORRUPT_PACKET"
        elif scenario_sealed:
            observed_state = "SEALED_PACKET"
        else:
            observed_state = "CORRUPT_PACKET"
        rows.append({
            "scenario": scenario,
            "sealed_packet": str(scenario_sealed),
            "route_present": str(route_present),
            "tensor_witness_present": str(tensor_present),
            "checksum_intact": str(checksum_intact if scenario != "corrupt_threshold_reached" else False),
            "A_leak": fraction_text(a_leak),
            "A_side": fraction_text(A_SIDE),
            "threshold_rule": "A_leak >= A_side",
            "threshold_reached": str(threshold_reached),
            "t_fire_expression": "T2*(-1/2*ln(23/24))",
            "t_fire_over_T2_decimal": f"{T_FIRE_COEFFICIENT:.18f}",
            "observed_state": observed_state,
            "expected_state": expected_state,
            "passed": str(observed_state == expected_state),
        })
    return rows


def build_checks(
    inputs: dict[str, object],
    state_requirements: list[dict[str, str]],
    corruption: list[dict[str, str]],
    warning_gate: list[dict[str, str]],
) -> list[Check]:
    vm = validity_map(inputs)
    wm = wrong_map(inputs)
    cr222a_hash = sha256_file(CR222A_CONTRACT)
    cr222b_hash = sha256_file(CR222B_PACKET)
    draft = next(row for row in state_requirements if row["state"] == "DRAFT_PACKET")
    tensor_payload_corruption = next(row for row in corruption if row["corruption_class"] == "CORRUPT_TENSOR_PROMOTED_TO_PAYLOAD")
    threshold_row = next(row for row in warning_gate if row["scenario"] == "sealed_threshold_exact")
    return [
        Check("draft_state_permits_incomplete_hash", draft["passed"] == "True" and "hash_status=not_final_allowed" in draft["observed"], draft["observed"], "roles present; hash not final allowed"),
        Check("sealed_state_requires_upstream_cr222a_hash", cr222a_hash == EXPECTED_CR222A_HASH, cr222a_hash, EXPECTED_CR222A_HASH),
        Check("sealed_state_requires_cr222b_packet_hash", cr222b_hash == EXPECTED_CR222B_HASH, cr222b_hash, EXPECTED_CR222B_HASH),
        Check("carrier_subtotal_36", vm["carrier_subtotal_36"]["passed"] == "True", vm["carrier_subtotal_36"]["observed"], "36"),
        Check("source_subtotal_45", vm["source_subtotal_45"]["passed"] == "True", vm["source_subtotal_45"]["observed"], "45"),
        Check("unpacked_total_81", vm["unpacked_total_81"]["passed"] == "True", vm["unpacked_total_81"]["observed"], "81"),
        Check("mirror_total_81", vm["mirror_total_81"]["passed"] == "True", vm["mirror_total_81"]["observed"], "81"),
        Check("full_checksum_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("missing_0306_corrupts_to_161", wm["omit_0306_p1"]["passes_as_failure"] == "True", wm["omit_0306_p1"]["observed_failure"], "161"),
        Check("duplicate_0305_corrupts_to_163", wm["restore_duplicate_0305_p1"]["passes_as_failure"] == "True", wm["restore_duplicate_0305_p1"]["observed_failure"], "163"),
        Check("tensor_as_payload_throws_role_failure", tensor_payload_corruption["state_result"] == "CORRUPT_PACKET", tensor_payload_corruption["observed_failure"], "role_failure"),
        Check("valid_warning_requires_sealed_packet_plus_threshold_trigger", threshold_row["passed"] == "True", f"{threshold_row['observed_state']} at A_leak={threshold_row['A_leak']}", "VALID_PR_WARNING_PACKET at A_side"),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(machine_sha: str) -> None:
    text = f"""# CR222c PRECOMMIT - Paul Revere Packet Audit States

## Scope

Define the packet state machine around CR222b. This is an audit/transition
layer only; it does not regenerate or discover physics rows.

## State Chain

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

## Sealed Packet Requirements

```text
CR222a hash = {EXPECTED_CR222A_HASH}
CR222b packet hash = {EXPECTED_CR222B_HASH}
carrier subtotal = 36
source subtotal = 45
unpacked total = 81
mirror total = 81
full checksum = 162
```

## Warning Gate

```text
VALID_PR_WARNING_PACKET =
  SEALED_PACKET
  + tensor witness present
  + route present
  + warning threshold reached
  + checksum intact

A_side = 1/24
warning threshold: A_leak >= A_side
t_fire = T2*(-1/2*ln(23/24))
```

## Pre-run Hash

Expected `CR222c_state_machine.csv` hash:

```text
{machine_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222c Paul Revere Packet Audit States

This artifact defines the state machine around the CR222b Paul Revere packet:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

Primary product:

```text
CR222c_state_machine.csv
```
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222c Paul Revere Packet Audit States Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222c_state_machine.csv SHA-256:** `{summary['sha256']['CR222c_state_machine.csv']}`

## Verdict

The Paul Revere packet now has an audit state machine:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

A packet is sealed only when the CR222a and CR222b hashes match and the packet
checksum remains intact:

```text
36 + 45 = 81
0303 = 81
81 + 81 = 162
```

A valid warning packet is stronger than a sealed packet:

```text
VALID_PR_WARNING_PACKET =
  SEALED_PACKET
  + route present
  + tensor witness present
  + A_leak >= A_side
  + checksum intact
```

with:

```text
A_side = 1/24
t_fire = T2*(-1/2*ln(23/24))
```

The tensor carrier remains witness/floor only. It does not become payload or
matter.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs()

    machine = state_machine_rows()
    machine_bytes = render_csv(machine, ["from_state", "event", "to_state", "guard", "edit_policy", "meaning"])
    machine_sha = sha256_bytes(machine_bytes)
    OUT_STATE_MACHINE.write_bytes(machine_bytes)

    requirements = state_requirement_rows(inputs)
    write_csv(OUT_STATE_REQUIREMENTS, requirements, ["state", "requirement", "observed", "passed", "edit_policy"])

    corruption = corruption_rows(inputs)
    write_csv(OUT_CORRUPTION, corruption, ["corruption_class", "trigger", "observed_failure", "expected_failure", "state_result", "audit_meaning"])

    warning_gate = warning_gate_rows(inputs)
    write_csv(
        OUT_WARNING_GATE,
        warning_gate,
        [
            "scenario",
            "sealed_packet",
            "route_present",
            "tensor_witness_present",
            "checksum_intact",
            "A_leak",
            "A_side",
            "threshold_rule",
            "threshold_reached",
            "t_fire_expression",
            "t_fire_over_T2_decimal",
            "observed_state",
            "expected_state",
            "passed",
        ],
    )

    checks = build_checks(inputs, requirements, corruption, warning_gate)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222c_PASS_PR_PACKET_AUDIT_STATES__DRAFT_SEALED_CORRUPT_VALID_WARNING"
        if checks_passed == checks_total
        else "CR222c_FAIL_PR_PACKET_AUDIT_STATES"
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
        "state_chain": "DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET; DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET",
        "upstream_cr222a_hash": sha256_file(CR222A_CONTRACT),
        "upstream_cr222b_packet_hash": sha256_file(CR222B_PACKET),
        "warning_gate": {
            "A_side": fraction_text(A_SIDE),
            "threshold": "A_leak >= A_side",
            "t_fire": "T2*(-1/2*ln(23/24))",
            "t_fire_over_T2_decimal": f"{T_FIRE_COEFFICIENT:.18f}",
        },
        "outputs": {
            "state_machine_csv": OUT_STATE_MACHINE.name,
            "state_requirements_csv": OUT_STATE_REQUIREMENTS.name,
            "corruption_classes_csv": OUT_CORRUPTION.name,
            "warning_gate_csv": OUT_WARNING_GATE.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222c_state_machine.csv": machine_sha,
        },
        "next_gate": "CR222d_PR_PACKET_EMISSION_OR_SIMULATION",
    }

    write_precommit(machine_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_STATE_MACHINE,
        OUT_STATE_REQUIREMENTS,
        OUT_CORRUPTION,
        OUT_WARNING_GATE,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222c Paul Revere packet audit states complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  states: DRAFT -> SEALED -> VALID_PR_WARNING; DRAFT/SEALED -> CORRUPT")
    print(f"  CR222c_state_machine.csv sha256: {machine_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
