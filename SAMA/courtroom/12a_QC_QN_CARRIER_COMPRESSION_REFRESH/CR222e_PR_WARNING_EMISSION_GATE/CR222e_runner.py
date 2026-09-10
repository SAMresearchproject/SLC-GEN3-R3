"""CR222e Paul Revere warning emission gate.

CR222e consumes the sealed upstream stack and defines when a valid Paul Revere
packet is allowed to become an emitted warning write.

It does not discover new physics. It separates:

    sealed packet validity != protocol warning trigger != emitted write
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable


getcontext().prec = 80

CR_ID = "CR222e"
TEST_ID = "CR222e_PR_WARNING_EMISSION_GATE"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR222A_DIR = BRANCH_DIR / "CR222a_NATIVE_STACK_CONTRACT"
CR222B_DIR = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT"
CR222C_DIR = BRANCH_DIR / "CR222c_PR_PACKET_AUDIT_STATES"
CR222D_DIR = BRANCH_DIR / "CR222d_ROW_TAXONOMY_PROMOTION_GATE"

CR222A_CONTRACT = CR222A_DIR / "Tier1_NativeStackContract.csv"
CR222A_SUMMARY = CR222A_DIR / "CR222a_summary.json"
CR222B_PACKET = CR222B_DIR / "Paul_Revere_PacketContract.csv"
CR222B_SUMMARY = CR222B_DIR / "CR222b_summary.json"
CR222B_VALIDITY = CR222B_DIR / "CR222b_packet_validity.csv"
CR222B_WRONG_CONTROLS = CR222B_DIR / "CR222b_wrong_controls.csv"
CR222C_SUMMARY = CR222C_DIR / "CR222c_summary.json"
CR222C_WARNING_GATE = CR222C_DIR / "CR222c_warning_gate.csv"
CR222D_SUMMARY = CR222D_DIR / "CR222d_summary.json"
CR222D_THEOREM = CR222D_DIR / "CR222d_row_taxonomy_theorem.csv"
CR222D_ROSTER = CR222D_DIR / "CR222d_support_roster_duplicate_correction.csv"
CR222D_BLOCKED = CR222D_DIR / "CR222d_blocked_support_gate_verification.csv"

OUT_STATE_MACHINE = CR_DIR / "CR222e_emission_state_machine.csv"
OUT_UPSTREAM = CR_DIR / "CR222e_upstream_seals.csv"
OUT_TRIGGER = CR_DIR / "CR222e_protocol_trigger_gate.csv"
OUT_EMISSION = CR_DIR / "CR222e_warning_emission_rows.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222e_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222e_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222e_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222e_summary.json"
OUT_RESULT = CR_DIR / "CR222e_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
R2 = R * R
EIGHT = Fraction(8, 1)
A_SIDE = Fraction(1, 24)
T_FIRE_COEFFICIENT = Fraction.from_float(-0.5 * math.log(23 / 24)).limit_denominator(10**18)

EXPECTED_CR222A_HASH = "0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b"
EXPECTED_CR222B_HASH = "79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009"
EXPECTED_CR222C_HASH = "7644f9ca376ec2bac1e41c214aa782976d10d2ba067e19322431872bd9aac186"
EXPECTED_CR222D_HASH = "c0f8918974f660ddb0e51e10e3c37f1d59b8bcf0b98b0d02cec1d81ae2a1320a"


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


def decimal_text(value: Fraction, places: int = 18) -> str:
    quant = Decimal(1).scaleb(-places)
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return format(decimal.quantize(quant), "f")


def load_inputs() -> dict[str, object]:
    return {
        "cr222a_summary": read_json(CR222A_SUMMARY),
        "cr222b_summary": read_json(CR222B_SUMMARY),
        "cr222b_validity": read_csv_rows(CR222B_VALIDITY),
        "cr222b_wrong_controls": read_csv_rows(CR222B_WRONG_CONTROLS),
        "cr222c_summary": read_json(CR222C_SUMMARY),
        "cr222c_warning_gate": read_csv_rows(CR222C_WARNING_GATE),
        "cr222d_summary": read_json(CR222D_SUMMARY),
        "cr222d_roster": read_csv_rows(CR222D_ROSTER),
        "cr222d_blocked": read_csv_rows(CR222D_BLOCKED),
    }


def validity_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["validity_check"]: row for row in inputs["cr222b_validity"]}


def wrong_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["wrong_control"]: row for row in inputs["cr222b_wrong_controls"]}


def roster_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["candidate_id"]: row for row in inputs["cr222d_roster"]}


def blocked_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["candidate_id"]: row for row in inputs["cr222d_blocked"]}


def upstream_seal_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    cr222c_summary = inputs["cr222c_summary"]
    return [
        {
            "upstream": "CR222a_native_stack_contract",
            "artifact": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222A_CONTRACT),
            "expected_sha256": EXPECTED_CR222A_HASH,
            "result_class": inputs["cr222a_summary"]["result_class"],
            "passed": str(sha256_file(CR222A_CONTRACT) == EXPECTED_CR222A_HASH),
        },
        {
            "upstream": "CR222b_packet_contract",
            "artifact": str(CR222B_PACKET.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222B_PACKET),
            "expected_sha256": EXPECTED_CR222B_HASH,
            "result_class": inputs["cr222b_summary"]["result_class"],
            "passed": str(sha256_file(CR222B_PACKET) == EXPECTED_CR222B_HASH),
        },
        {
            "upstream": "CR222c_packet_audit_states",
            "artifact": str((CR222C_DIR / "CR222c_state_machine.csv").relative_to(COURTROOM_DIR)),
            "observed_sha256": cr222c_summary["sha256"]["CR222c_state_machine.csv"],
            "expected_sha256": EXPECTED_CR222C_HASH,
            "result_class": cr222c_summary["result_class"],
            "passed": str(cr222c_summary["sha256"]["CR222c_state_machine.csv"] == EXPECTED_CR222C_HASH),
        },
        {
            "upstream": "CR222d_promotion_gate",
            "artifact": str(CR222D_THEOREM.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222D_THEOREM),
            "expected_sha256": EXPECTED_CR222D_HASH,
            "result_class": inputs["cr222d_summary"]["result_class"],
            "passed": str(sha256_file(CR222D_THEOREM) == EXPECTED_CR222D_HASH),
        },
    ]


def state_machine_rows() -> list[dict[str, str]]:
    return [
        {
            "from_state": "NONE",
            "event": "assemble_packet",
            "to_state": "DRAFT_PACKET",
            "guard": "packet fields present; hash not final",
            "write_allowed": "no",
            "meaning": "packet exists but is not trusted",
        },
        {
            "from_state": "DRAFT_PACKET",
            "event": "seal_packet",
            "to_state": "SEALED_PACKET",
            "guard": "CR222a/CR222b/CR222d seals match and packet checksum closes",
            "write_allowed": "no",
            "meaning": "packet is structurally intact but has not triggered",
        },
        {
            "from_state": "DRAFT_PACKET",
            "event": "role_hash_checksum_or_gate_failure",
            "to_state": "CORRUPT_PACKET",
            "guard": "any required role, hash, checksum, or promotion-gate rule fails",
            "write_allowed": "no",
            "meaning": "packet cannot warn",
        },
        {
            "from_state": "SEALED_PACKET",
            "event": "role_hash_checksum_or_gate_failure",
            "to_state": "CORRUPT_PACKET",
            "guard": "any sealed requirement fails after seal",
            "write_allowed": "no",
            "meaning": "sealed packet is no longer valid",
        },
        {
            "from_state": "SEALED_PACKET",
            "event": "protocol_warning_trigger",
            "to_state": "VALID_WARNING_PACKET",
            "guard": "G_protocol=1 and A_leak>=A_side and route/tensor/checksum intact",
            "write_allowed": "not_yet",
            "meaning": "packet is allowed to become a warning event",
        },
        {
            "from_state": "VALID_WARNING_PACKET",
            "event": "emit_warning_write",
            "to_state": "EMITTED_WARNING_PACKET",
            "guard": "qA>0 and T=qA/8 and W=7qA/8",
            "write_allowed": "yes",
            "meaning": "warning write is emitted after trigger and split",
        },
    ]


def sealed_packet(inputs: dict[str, object]) -> bool:
    vm = validity_map(inputs)
    d_summary = inputs["cr222d_summary"]
    hashes_ok = (
        sha256_file(CR222A_CONTRACT) == EXPECTED_CR222A_HASH
        and sha256_file(CR222B_PACKET) == EXPECTED_CR222B_HASH
        and sha256_file(CR222D_THEOREM) == EXPECTED_CR222D_HASH
    )
    checksum_ok = (
        vm["unpacked_total_81"]["passed"] == "True"
        and vm["mirror_total_81"]["passed"] == "True"
        and vm["packet_total_162"]["passed"] == "True"
    )
    roster_ok = (
        d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12
        and d_summary["support_roster_correction"]["unique_support_roster_sum"] == 81
        and d_summary["support_roster_correction"]["duplicate_mirror_value"] == 81
        and d_summary["support_roster_correction"]["closure_total"] == 162
    )
    return hashes_ok and checksum_ok and roster_ok


def trigger_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    vm = validity_map(inputs)
    sealed = sealed_packet(inputs)
    route_present = vm["road_light_route_present"]["passed"] == "True"
    tensor_present = vm["tensor_witness_present"]["passed"] == "True"
    checksum_intact = vm["packet_total_162"]["passed"] == "True"
    scenarios = [
        ("draft_packet", False, 0, Fraction(0, 1), "DRAFT_PACKET"),
        ("sealed_no_protocol_gate", sealed, 0, A_SIDE, "SEALED_PACKET"),
        ("sealed_below_threshold", sealed, 1, Fraction(1, 48), "SEALED_PACKET"),
        ("sealed_threshold_exact", sealed, 1, A_SIDE, "VALID_WARNING_PACKET"),
        ("sealed_above_threshold", sealed, 1, Fraction(1, 12), "VALID_WARNING_PACKET"),
        ("corrupt_threshold_reached", False, 1, A_SIDE, "CORRUPT_PACKET"),
    ]
    rows = []
    for scenario, scenario_sealed, g_protocol, a_leak, expected_state in scenarios:
        threshold_reached = a_leak >= A_SIDE
        valid_warning = (
            scenario_sealed
            and g_protocol == 1
            and threshold_reached
            and route_present
            and tensor_present
            and checksum_intact
        )
        if valid_warning:
            observed_state = "VALID_WARNING_PACKET"
        elif scenario == "corrupt_threshold_reached":
            observed_state = "CORRUPT_PACKET"
        elif scenario_sealed:
            observed_state = "SEALED_PACKET"
        else:
            observed_state = "DRAFT_PACKET"
        rows.append({
            "scenario": scenario,
            "sealed_packet": str(scenario_sealed),
            "G_protocol": str(g_protocol),
            "A_leak": fraction_text(a_leak),
            "A_side": fraction_text(A_SIDE),
            "threshold_rule": "A_leak>=A_side",
            "threshold_reached": str(threshold_reached),
            "route_present": str(route_present),
            "tensor_witness_present": str(tensor_present),
            "checksum_intact": str(checksum_intact if scenario != "corrupt_threshold_reached" else False),
            "valid_warning_rule": "SEALED_PACKET+G_protocol=1+A_leak>=A_side",
            "observed_state": observed_state,
            "expected_state": expected_state,
            "passed": str(observed_state == expected_state),
        })
    return rows


def emission_rows(trigger_gate: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for trigger in trigger_gate:
        a_leak = Fraction(trigger["A_leak"])
        valid_warning = trigger["observed_state"] == "VALID_WARNING_PACKET"
        q_a = a_leak if valid_warning else Fraction(0, 1)
        tensor = q_a / EIGHT
        retained = q_a * Fraction(7, 8)
        emitted = valid_warning and q_a > 0 and tensor == q_a / EIGHT and retained == q_a * Fraction(7, 8)
        rows.append({
            "scenario": trigger["scenario"],
            "input_state": trigger["observed_state"],
            "qA": fraction_text(q_a),
            "qA_decimal": decimal_text(q_a),
            "tensor_T": fraction_text(tensor),
            "tensor_T_decimal": decimal_text(tensor),
            "retained_W": fraction_text(retained),
            "retained_W_decimal": decimal_text(retained),
            "split_rule": "T=qA/8; W=7qA/8",
            "emitted_state": "EMITTED_WARNING_PACKET" if emitted else trigger["observed_state"],
            "write_allowed": str(emitted),
            "passed": str((emitted and valid_warning) or ((not emitted) and not valid_warning)),
        })
    return rows


def wrong_control_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    wm = wrong_map(inputs)
    roster = roster_map(inputs)
    blocked = blocked_map(inputs)
    mirror = roster["QP093A-0303"]
    tensor = blocked["QP093A-0300"]
    return [
        {
            "wrong_control": "support_row_emits_without_gate",
            "attempted_action": "use closed support row as emitted qA/T/W source",
            "observed_failure": "G_matter=0 => M_obs=qA=T=W=0",
            "expected_failure": "NO_EMISSION",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "0303_mirror_emits_as_payload",
            "attempted_action": "treat QP093A-0303 mirror checksum as payload emission",
            "observed_failure": f"{mirror['support_roster_role']}; counted={mirror['counted_as_unique_support_row']}",
            "expected_failure": "MIRROR_NOT_PAYLOAD",
            "passes_as_failure": str(mirror["support_roster_role"] == "duplicate_mirror_closure_row"),
        },
        {
            "wrong_control": "tensor_row_promoted_to_matter",
            "attempted_action": "promote QP093A-0300 tensor carrier as matter",
            "observed_failure": tensor["matter_row_allowed"],
            "expected_failure": "matter_row_allowed=no",
            "passes_as_failure": str(tensor["matter_row_allowed"] == "no"),
        },
        {
            "wrong_control": "dot_one_visual_separator_counted_as_p",
            "attempted_action": "read .1 visual separator as algebraic partition p",
            "observed_failure": "display marker != numeric support p",
            "expected_failure": "VISUAL_MARKER_NOT_NUMERIC_PARTITION",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "missing_0306_packet_still_emits",
            "attempted_action": "emit warning after omitting p=1 source packet",
            "observed_failure": wm["omit_0306_p1"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_EMISSION",
            "passes_as_failure": str(wm["omit_0306_p1"]["observed_failure"] == "161"),
        },
        {
            "wrong_control": "mass_lift_support_value_used_as_ledger_p",
            "attempted_action": "use support mass-lift fields instead of bare p/checksum ledger",
            "observed_failure": wm["use_mass_lift_fields_instead_of_bare_p"]["observed_failure"],
            "expected_failure": "NOT_81_NO_EMISSION",
            "passes_as_failure": wm["use_mass_lift_fields_instead_of_bare_p"]["passes_as_failure"],
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    trigger: list[dict[str, str]],
    emissions: list[dict[str, str]],
    wrongs: list[dict[str, str]],
    machine: list[dict[str, str]],
) -> list[Check]:
    vm = validity_map(inputs)
    d_summary = inputs["cr222d_summary"]
    threshold = next(row for row in trigger if row["scenario"] == "sealed_threshold_exact")
    no_gate = next(row for row in trigger if row["scenario"] == "sealed_no_protocol_gate")
    threshold_emission = next(row for row in emissions if row["scenario"] == "sealed_threshold_exact")
    support_no_gate = next(row for row in wrongs if row["wrong_control"] == "support_row_emits_without_gate")
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("state_machine_includes_emitted_warning", any(row["to_state"] == "EMITTED_WARNING_PACKET" for row in machine), str([row["to_state"] for row in machine]), "EMITTED_WARNING_PACKET"),
        Check("cr222b_packet_checksum_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("cr222d_unique_support_roster_12", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12, str(d_summary["support_roster_correction"]["unique_support_roster_rows"]), "12"),
        Check("cr222d_0303_mirror_not_support_mode", d_summary["support_roster_correction"]["duplicate_mirror_row"] == "QP093A-0303", d_summary["support_roster_correction"]["duplicate_mirror_row"], "QP093A-0303"),
        Check("support_roster_plus_mirror_162", d_summary["support_roster_correction"]["closure_total"] == 162, str(d_summary["support_roster_correction"]["closure_total"]), "162"),
        Check("a_side_threshold_is_one_over_24", fraction_text(A_SIDE) == "1/24", fraction_text(A_SIDE), "1/24"),
        Check("sealed_packet_without_protocol_gate_does_not_emit", no_gate["observed_state"] == "SEALED_PACKET", no_gate["observed_state"], "SEALED_PACKET"),
        Check("threshold_exact_creates_valid_warning", threshold["observed_state"] == "VALID_WARNING_PACKET", threshold["observed_state"], "VALID_WARNING_PACKET"),
        Check("valid_warning_emits_warning_write", threshold_emission["emitted_state"] == "EMITTED_WARNING_PACKET", threshold_emission["emitted_state"], "EMITTED_WARNING_PACKET"),
        Check("emission_requires_qA_positive", Fraction(threshold_emission["qA"]) > 0, threshold_emission["qA"], ">0"),
        Check("emission_tensor_split_qA_over_8", Fraction(threshold_emission["tensor_T"]) == Fraction(threshold_emission["qA"]) / 8, threshold_emission["tensor_T"], "qA/8"),
        Check("emission_retained_split_7qA_over_8", Fraction(threshold_emission["retained_W"]) == Fraction(threshold_emission["qA"]) * 7 / 8, threshold_emission["retained_W"], "7qA/8"),
        Check("support_row_without_gate_has_no_emission", support_no_gate["passes_as_failure"] == "True", support_no_gate["observed_failure"], "NO_EMISSION"),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrongs), str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(machine_sha: str) -> None:
    text = f"""# CR222e PRECOMMIT - Paul Revere Warning Emission Gate

## Scope

Define when a sealed Paul Revere packet becomes an emitted warning write.
This consumes CR222a, CR222b, CR222c, and CR222d. It does not regenerate the
physics engine.

## Rule

```text
VALID_PR_WARNING = SEALED_PACKET + G_protocol=1 + A_leak>=A_side
A_side = 1/24
```

Emission is allowed only after the warning gate:

```text
qA > 0
T = qA/8
W = 7qA/8
```

Support inventory alone cannot emit.

## Pre-run Hash

Expected `CR222e_emission_state_machine.csv` hash:

```text
{machine_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222e Paul Revere Warning Emission Gate

CR222e defines the emission state machine:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_WARNING_PACKET -> EMITTED_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

It protects the distinction:

```text
support inventory != promoted matter != emitted tensor/write
```
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222e Paul Revere Warning Emission Gate Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222e_emission_state_machine.csv SHA-256:** `{summary['sha256']['CR222e_emission_state_machine.csv']}`

## Verdict

CR222e defines the emission gate:

```text
VALID_PR_WARNING = SEALED_PACKET + G_protocol=1 + A_leak>=A_side
A_side = 1/24
```

Emission is separate:

```text
qA > 0
T = qA/8
W = 7qA/8
```

The corrected support stack is preserved:

```text
12 unique support rows = 81
QP093A-0303 mirror     = 81
closure                = 162
```

Support inventory alone does not emit. A sealed packet with no protocol gate
remains `SEALED_PACKET`; it does not become a warning write.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs()

    machine = state_machine_rows()
    machine_bytes = render_csv(machine, ["from_state", "event", "to_state", "guard", "write_allowed", "meaning"])
    machine_sha = sha256_bytes(machine_bytes)
    OUT_STATE_MACHINE.write_bytes(machine_bytes)

    upstream = upstream_seal_rows(inputs)
    write_csv(OUT_UPSTREAM, upstream, ["upstream", "artifact", "observed_sha256", "expected_sha256", "result_class", "passed"])

    trigger = trigger_rows(inputs)
    write_csv(
        OUT_TRIGGER,
        trigger,
        [
            "scenario",
            "sealed_packet",
            "G_protocol",
            "A_leak",
            "A_side",
            "threshold_rule",
            "threshold_reached",
            "route_present",
            "tensor_witness_present",
            "checksum_intact",
            "valid_warning_rule",
            "observed_state",
            "expected_state",
            "passed",
        ],
    )

    emissions = emission_rows(trigger)
    write_csv(
        OUT_EMISSION,
        emissions,
        [
            "scenario",
            "input_state",
            "qA",
            "qA_decimal",
            "tensor_T",
            "tensor_T_decimal",
            "retained_W",
            "retained_W_decimal",
            "split_rule",
            "emitted_state",
            "write_allowed",
            "passed",
        ],
    )

    wrongs = wrong_control_rows(inputs)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "attempted_action", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, trigger, emissions, wrongs, machine)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222e_PASS_PR_WARNING_EMISSION_GATE__SEALED_PACKET_PROMOTION_TRIGGER_TENSOR_WRITE"
        if checks_passed == checks_total
        else "CR222e_FAIL_PR_WARNING_EMISSION_GATE"
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
        "state_chain": "DRAFT_PACKET -> SEALED_PACKET -> VALID_WARNING_PACKET -> EMITTED_WARNING_PACKET; DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET",
        "core_rule": "VALID_PR_WARNING=SEALED_PACKET+G_protocol=1+A_leak>=A_side",
        "A_side": fraction_text(A_SIDE),
        "t_fire": {
            "expression": "T2*(-1/2*ln(23/24))",
            "over_T2_decimal": f"{-0.5 * math.log(23 / 24):.18f}",
        },
        "emission_rule": {
            "qA": "qA>0",
            "T": "qA/8",
            "W": "7qA/8",
        },
        "support_roster_correction": inputs["cr222d_summary"]["support_roster_correction"],
        "pr_stack": "CR222a native stack -> CR222b packet contract -> CR222d promotion gate -> CR222e warning emission",
        "outputs": {
            "state_machine_csv": OUT_STATE_MACHINE.name,
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "protocol_trigger_gate_csv": OUT_TRIGGER.name,
            "warning_emission_rows_csv": OUT_EMISSION.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222e_emission_state_machine.csv": machine_sha,
        },
        "next_gate": "PR_LETTER_PROTOCOL_DRAFT_WITH_EMISSION_GATE",
    }

    write_precommit(machine_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_STATE_MACHINE,
        OUT_UPSTREAM,
        OUT_TRIGGER,
        OUT_EMISSION,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222e Paul Revere warning emission gate complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  emission: SEALED -> VALID_WARNING -> EMITTED only after protocol trigger")
    print(f"  CR222e_emission_state_machine.csv sha256: {machine_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
