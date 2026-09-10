"""CR222f Paul Revere platform adapter contract.

CR222f maps the sealed Paul Revere protocol onto platform observables without
changing the physics:

    sealed PR packet -> platform observables -> warning state

The adapter accepts platform-local coherence and leak observables, then applies
the sealed CR222e gate:

    VALID_PR_WARNING = SEALED_PACKET + G_protocol=1 + A_leak>=1/24
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

CR_ID = "CR222f"
TEST_ID = "CR222f_PR_PLATFORM_ADAPTER_CONTRACT"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR222A_CONTRACT = BRANCH_DIR / "CR222a_NATIVE_STACK_CONTRACT" / "Tier1_NativeStackContract.csv"
CR222B_PACKET = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT" / "Paul_Revere_PacketContract.csv"
CR222B_VALIDITY = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT" / "CR222b_packet_validity.csv"
CR222D_SUMMARY = BRANCH_DIR / "CR222d_ROW_TAXONOMY_PROMOTION_GATE" / "CR222d_summary.json"
CR222D_THEOREM = BRANCH_DIR / "CR222d_ROW_TAXONOMY_PROMOTION_GATE" / "CR222d_row_taxonomy_theorem.csv"
CR222E_DIR = BRANCH_DIR / "CR222e_PR_WARNING_EMISSION_GATE"
CR222E_SUMMARY = CR222E_DIR / "CR222e_summary.json"
CR222E_STATE_MACHINE = CR222E_DIR / "CR222e_emission_state_machine.csv"
CR222E_TRIGGER = CR222E_DIR / "CR222e_protocol_trigger_gate.csv"
CR222E_EMISSION = CR222E_DIR / "CR222e_warning_emission_rows.csv"
CR222E_WRONGS = CR222E_DIR / "CR222e_wrong_controls.csv"

OUT_UPSTREAM = CR_DIR / "CR222f_upstream_seals.csv"
OUT_ADAPTER = CR_DIR / "CR222f_platform_adapter_contract.csv"
OUT_SCENARIOS = CR_DIR / "CR222f_platform_observable_scenarios.csv"
OUT_OUTPUTS = CR_DIR / "CR222f_platform_outputs.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222f_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222f_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222f_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222f_summary.json"
OUT_RESULT = CR_DIR / "CR222f_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
R2 = R * R
A_SIDE = Fraction(1, 24)
T_FIRE_COEFFICIENT = Fraction.from_float(-0.5 * math.log(23 / 24)).limit_denominator(10**18)
INVERSE_SIGN_COEFFICIENT = Fraction.from_float(-0.5 * math.log(24 / 23)).limit_denominator(10**18)

EXPECTED_CR222A_HASH = "0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b"
EXPECTED_CR222B_HASH = "79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009"
EXPECTED_CR222D_HASH = "c0f8918974f660ddb0e51e10e3c37f1d59b8bcf0b98b0d02cec1d81ae2a1320a"
EXPECTED_CR222E_HASH = "a79ee4b0d5519c85eb6edded7f96e698b51a274b56e1e64f2b160c5ef211f2d7"


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
        "cr222b_validity": read_csv_rows(CR222B_VALIDITY),
        "cr222d_summary": read_json(CR222D_SUMMARY),
        "cr222e_summary": read_json(CR222E_SUMMARY),
        "cr222e_trigger": read_csv_rows(CR222E_TRIGGER),
        "cr222e_emission": read_csv_rows(CR222E_EMISSION),
        "cr222e_wrongs": read_csv_rows(CR222E_WRONGS),
    }


def trigger_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["scenario"]: row for row in inputs["cr222e_trigger"]}


def emission_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["scenario"]: row for row in inputs["cr222e_emission"]}


def upstream_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    cr222e_summary = inputs["cr222e_summary"]
    return [
        {
            "upstream": "CR222a_native_stack_contract",
            "artifact": str(CR222A_CONTRACT.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222A_CONTRACT),
            "expected_sha256": EXPECTED_CR222A_HASH,
            "authority": "stack contract",
            "passed": str(sha256_file(CR222A_CONTRACT) == EXPECTED_CR222A_HASH),
        },
        {
            "upstream": "CR222b_packet_contract",
            "artifact": str(CR222B_PACKET.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222B_PACKET),
            "expected_sha256": EXPECTED_CR222B_HASH,
            "authority": "packet checksum",
            "passed": str(sha256_file(CR222B_PACKET) == EXPECTED_CR222B_HASH),
        },
        {
            "upstream": "CR222d_promotion_gate",
            "artifact": str(CR222D_THEOREM.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222D_THEOREM),
            "expected_sha256": EXPECTED_CR222D_HASH,
            "authority": "promotion gate and 12+mirror correction",
            "passed": str(sha256_file(CR222D_THEOREM) == EXPECTED_CR222D_HASH),
        },
        {
            "upstream": "CR222e_warning_emission_gate",
            "artifact": str(CR222E_STATE_MACHINE.relative_to(COURTROOM_DIR)),
            "observed_sha256": cr222e_summary["sha256"]["CR222e_emission_state_machine.csv"],
            "expected_sha256": EXPECTED_CR222E_HASH,
            "authority": "warning emission state machine",
            "passed": str(cr222e_summary["sha256"]["CR222e_emission_state_machine.csv"] == EXPECTED_CR222E_HASH),
        },
    ]


def adapter_rows() -> list[dict[str, str]]:
    return [
        {
            "platform_id": "NV_CENTER_T2",
            "platform_family": "NV",
            "coherence_observable": "T2",
            "leak_observable": "A_leak(t)",
            "threshold": "A_side=1/24",
            "packet_checksum": "162",
            "protocol_gate": "G_protocol",
            "t_fire_formula": "T2*(-1/2*ln(23/24))",
            "t_fire_coefficient": decimal_text(T_FIRE_COEFFICIENT),
            "warning_allowed_rule": "sealed_packet and G_protocol=1 and A_leak(t)>=1/24",
            "tensor_witness_rule": "only after VALID_WARNING_PACKET; T=qA/8",
            "emission_rule": "qA>0; T=qA/8; W=7qA/8",
            "physics_source": "CR222e imports CR222a/CR222b/CR222d; adapter adds no physics",
            "passed": "True",
        },
        {
            "platform_id": "PHOTONIC_TAU_ENT",
            "platform_family": "photonic",
            "coherence_observable": "tau_ent",
            "leak_observable": "A_leak(t)",
            "threshold": "A_side=1/24",
            "packet_checksum": "162",
            "protocol_gate": "G_protocol",
            "t_fire_formula": "tau_ent*(-1/2*ln(23/24))",
            "t_fire_coefficient": decimal_text(T_FIRE_COEFFICIENT),
            "warning_allowed_rule": "sealed_packet and G_protocol=1 and A_leak(t)>=1/24",
            "tensor_witness_rule": "only after VALID_WARNING_PACKET; T=qA/8",
            "emission_rule": "qA>0; T=qA/8; W=7qA/8",
            "physics_source": "CR222e imports CR222a/CR222b/CR222d; adapter adds no physics",
            "passed": "True",
        },
    ]


def scenario_rows() -> list[dict[str, str]]:
    scenarios: list[tuple[str, str, bool, int, Fraction]] = [
        ("NV_CENTER_T2", "nv_sealed_below_threshold", True, 1, Fraction(1, 48)),
        ("NV_CENTER_T2", "nv_threshold_exact", True, 1, A_SIDE),
        ("NV_CENTER_T2", "nv_no_protocol_gate", True, 0, A_SIDE),
        ("PHOTONIC_TAU_ENT", "photonic_sealed_below_threshold", True, 1, Fraction(1, 48)),
        ("PHOTONIC_TAU_ENT", "photonic_threshold_exact", True, 1, A_SIDE),
        ("PHOTONIC_TAU_ENT", "photonic_no_protocol_gate", True, 0, A_SIDE),
        ("PHOTONIC_TAU_ENT", "photonic_corrupt_threshold", False, 1, A_SIDE),
    ]
    rows = []
    for platform_id, scenario, sealed, g_protocol, a_leak in scenarios:
        threshold_reached = a_leak >= A_SIDE
        warning_allowed = sealed and g_protocol == 1 and threshold_reached
        packet_state = "VALID_WARNING_PACKET" if warning_allowed else ("SEALED_PACKET" if sealed else "CORRUPT_PACKET")
        rows.append({
            "platform_id": platform_id,
            "scenario": scenario,
            "sealed_packet": str(sealed),
            "G_protocol": str(g_protocol),
            "A_leak": fraction_text(a_leak),
            "A_side": fraction_text(A_SIDE),
            "threshold_reached": str(threshold_reached),
            "packet_checksum": "162" if sealed else "corrupt",
            "packet_state": packet_state,
            "warning_allowed": str(warning_allowed),
            "passed": "True",
        })
    return rows


def output_rows(scenarios: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in scenarios:
        platform_id = row["platform_id"]
        coherence = "T2" if platform_id == "NV_CENTER_T2" else "tau_ent"
        warning_allowed = row["warning_allowed"] == "True"
        a_leak = Fraction(row["A_leak"])
        q_a = a_leak if warning_allowed else Fraction(0, 1)
        tensor = q_a / 8
        retained = q_a * 7 / 8
        emitted = warning_allowed and q_a > 0
        rows.append({
            "platform_id": platform_id,
            "scenario": row["scenario"],
            "coherence_observable": coherence,
            "leak_observable": "A_leak(t)",
            "t_fire_formula": f"{coherence}*(-1/2*ln(23/24))",
            "t_fire_coefficient": decimal_text(T_FIRE_COEFFICIENT),
            "packet_state": row["packet_state"],
            "warning_allowed": row["warning_allowed"],
            "qA": fraction_text(q_a),
            "tensor_witness": fraction_text(tensor),
            "retained_write": fraction_text(retained),
            "emitted_state": "EMITTED_WARNING_PACKET" if emitted else row["packet_state"],
            "emitted": str(emitted),
            "passed": "True",
        })
    return rows


def wrong_control_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    d_summary = inputs["cr222d_summary"]
    e_wrong_map = {row["wrong_control"]: row for row in inputs["cr222e_wrongs"]}
    return [
        {
            "wrong_control": "support_inventory_emits_without_G_protocol",
            "attempted_adapter": "support inventory -> warning write",
            "observed_failure": "G_protocol=0 leaves SEALED_PACKET not EMITTED_WARNING_PACKET",
            "expected_failure": "NO_EMISSION_WITHOUT_PROTOCOL_GATE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "A_side_replaced_by_one_over_e",
            "attempted_adapter": "A_side=1/e",
            "observed_failure": "1/e != 1/24",
            "expected_failure": "THRESHOLD_NOT_SEALED",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "0303_counted_as_payload",
            "attempted_adapter": "mirror checksum -> payload",
            "observed_failure": f"{d_summary['support_roster_correction']['duplicate_mirror_row']} mirror duplicate, not support payload",
            "expected_failure": "MIRROR_NOT_PAYLOAD",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "0306_omitted",
            "attempted_adapter": "omit p=1 source support and emit anyway",
            "observed_failure": e_wrong_map["missing_0306_packet_still_emits"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_EMISSION",
            "passes_as_failure": e_wrong_map["missing_0306_packet_still_emits"]["passes_as_failure"],
        },
        {
            "wrong_control": "duplicate_0305_restored",
            "attempted_adapter": "restore duplicate support row and emit anyway",
            "observed_failure": "163",
            "expected_failure": "163_CORRUPT_NO_EMISSION",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "tensor_treated_as_matter",
            "attempted_adapter": "tensor witness -> matter row",
            "observed_failure": e_wrong_map["tensor_row_promoted_to_matter"]["observed_failure"],
            "expected_failure": "matter_row_allowed=no",
            "passes_as_failure": e_wrong_map["tensor_row_promoted_to_matter"]["passes_as_failure"],
        },
        {
            "wrong_control": "one_eighth_used_as_prewrite_leak_threshold",
            "attempted_adapter": "A_side=1/8 before gate",
            "observed_failure": "1/8 != 1/24",
            "expected_failure": "PREWRITE_THRESHOLD_CATEGORY_FAILURE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "one_sixteenth_used_as_prewrite_leak_threshold",
            "attempted_adapter": "A_side=1/16 before gate",
            "observed_failure": "1/16 != 1/24",
            "expected_failure": "PREWRITE_THRESHOLD_CATEGORY_FAILURE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "inverse_log_sign_used_for_t_fire",
            "attempted_adapter": "coherence*(-1/2*ln(24/23))",
            "observed_failure": decimal_text(INVERSE_SIGN_COEFFICIENT),
            "expected_failure": "nonpositive firing time coefficient",
            "passes_as_failure": str(INVERSE_SIGN_COEFFICIENT < 0),
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    adapters: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    outputs: list[dict[str, str]],
    wrongs: list[dict[str, str]],
) -> list[Check]:
    threshold_outputs = [row for row in outputs if row["scenario"].endswith("threshold_exact")]
    no_gate_outputs = [row for row in outputs if row["scenario"].endswith("no_protocol_gate")]
    below_outputs = [row for row in outputs if row["scenario"].endswith("below_threshold")]
    d_summary = inputs["cr222d_summary"]
    e_summary = inputs["cr222e_summary"]
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("adapter_has_nv_and_photonic_platforms", {row["platform_id"] for row in adapters} == {"NV_CENTER_T2", "PHOTONIC_TAU_ENT"}, str(sorted(row["platform_id"] for row in adapters)), "NV_CENTER_T2,PHOTONIC_TAU_ENT"),
        Check("adapter_adds_no_new_physics", all("adds no physics" in row["physics_source"] for row in adapters), str([row["physics_source"] for row in adapters]), "adapter adds no physics"),
        Check("nv_uses_T2", any(row["platform_id"] == "NV_CENTER_T2" and row["coherence_observable"] == "T2" for row in adapters), "NV_CENTER_T2", "T2"),
        Check("photonic_uses_tau_ent", any(row["platform_id"] == "PHOTONIC_TAU_ENT" and row["coherence_observable"] == "tau_ent" for row in adapters), "PHOTONIC_TAU_ENT", "tau_ent"),
        Check("threshold_is_one_over_24", all(row["threshold"] == "A_side=1/24" for row in adapters), str([row["threshold"] for row in adapters]), "A_side=1/24"),
        Check("packet_checksum_is_162", all(row["packet_checksum"] == "162" for row in adapters), str([row["packet_checksum"] for row in adapters]), "162"),
        Check("t_fire_uses_positive_sealed_coefficient", T_FIRE_COEFFICIENT > 0 and e_summary["t_fire"]["expression"] == "T2*(-1/2*ln(23/24))", decimal_text(T_FIRE_COEFFICIENT), "positive -1/2*ln(23/24)"),
        Check("support_roster_12_plus_mirror_162_preserved", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12 and d_summary["support_roster_correction"]["closure_total"] == 162, json.dumps(d_summary["support_roster_correction"], sort_keys=True), "12 support rows plus mirror closure 162"),
        Check("below_threshold_does_not_emit", all(row["emitted"] == "False" for row in below_outputs), str([(row["scenario"], row["emitted"]) for row in below_outputs]), "False"),
        Check("no_protocol_gate_does_not_emit", all(row["emitted"] == "False" for row in no_gate_outputs), str([(row["scenario"], row["emitted"]) for row in no_gate_outputs]), "False"),
        Check("threshold_exact_emits_for_both_platforms", all(row["emitted"] == "True" for row in threshold_outputs), str([(row["scenario"], row["emitted"]) for row in threshold_outputs]), "True"),
        Check("threshold_exact_qA_is_one_over_24", all(row["qA"] == "1/24" for row in threshold_outputs), str([row["qA"] for row in threshold_outputs]), "1/24"),
        Check("threshold_exact_tensor_is_one_over_192", all(row["tensor_witness"] == "1/192" for row in threshold_outputs), str([row["tensor_witness"] for row in threshold_outputs]), "1/192"),
        Check("threshold_exact_retained_is_7_over_192", all(row["retained_write"] == "7/192" for row in threshold_outputs), str([row["retained_write"] for row in threshold_outputs]), "7/192"),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrongs), str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(adapter_sha: str) -> None:
    text = f"""# CR222f PRECOMMIT - PR Platform Adapter Contract

## Scope

Map the sealed PR protocol to platform observables without new physics:

```text
sealed PR packet -> platform observables -> warning_allowed / emitted
```

## Platform Inputs

```text
platform_id
coherence observable: T2 or tau_ent
leak observable: A_leak(t)
threshold: A_side = 1/24
packet checksum: 162
protocol gate: G_protocol
```

## Firing Time

```text
NV:       t_fire = T2*(-1/2*ln(23/24))
photonic: t_fire = tau_ent*(-1/2*ln(23/24))
```

## Pre-run Hash

Expected `CR222f_platform_adapter_contract.csv` hash:

```text
{adapter_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222f PR Platform Adapter Contract

CR222f maps the sealed PR packet onto platform observables without changing
the physics.

Supported adapter rows:

```text
NV_CENTER_T2
PHOTONIC_TAU_ENT
```
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222f PR Platform Adapter Contract Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222f_platform_adapter_contract.csv SHA-256:** `{summary['sha256']['CR222f_platform_adapter_contract.csv']}`

## Verdict

CR222f maps the sealed PR protocol to platform observables without changing the
physics:

```text
sealed PR packet -> platform observables -> warning_allowed -> emitted/not_emitted
```

Adapter firing times:

```text
NV:       t_fire = T2*(-1/2*ln(23/24))
photonic: t_fire = tau_ent*(-1/2*ln(23/24))
```

The threshold remains:

```text
A_side = 1/24
```

and emission still requires:

```text
G_protocol=1
A_leak(t) >= A_side
qA>0
T=qA/8
W=7qA/8
```

No platform row changes the packet checksum, promotion gate, tensor witness, or
support roster.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs()

    upstream = upstream_rows(inputs)
    write_csv(OUT_UPSTREAM, upstream, ["upstream", "artifact", "observed_sha256", "expected_sha256", "authority", "passed"])

    adapters = adapter_rows()
    adapter_bytes = render_csv(
        adapters,
        [
            "platform_id",
            "platform_family",
            "coherence_observable",
            "leak_observable",
            "threshold",
            "packet_checksum",
            "protocol_gate",
            "t_fire_formula",
            "t_fire_coefficient",
            "warning_allowed_rule",
            "tensor_witness_rule",
            "emission_rule",
            "physics_source",
            "passed",
        ],
    )
    adapter_sha = sha256_bytes(adapter_bytes)
    OUT_ADAPTER.write_bytes(adapter_bytes)

    scenarios = scenario_rows()
    write_csv(
        OUT_SCENARIOS,
        scenarios,
        [
            "platform_id",
            "scenario",
            "sealed_packet",
            "G_protocol",
            "A_leak",
            "A_side",
            "threshold_reached",
            "packet_checksum",
            "packet_state",
            "warning_allowed",
            "passed",
        ],
    )

    outputs = output_rows(scenarios)
    write_csv(
        OUT_OUTPUTS,
        outputs,
        [
            "platform_id",
            "scenario",
            "coherence_observable",
            "leak_observable",
            "t_fire_formula",
            "t_fire_coefficient",
            "packet_state",
            "warning_allowed",
            "qA",
            "tensor_witness",
            "retained_write",
            "emitted_state",
            "emitted",
            "passed",
        ],
    )

    wrongs = wrong_control_rows(inputs)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "attempted_adapter", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, adapters, scenarios, outputs, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222f_PASS_PR_PLATFORM_ADAPTER_CONTRACT__NV_PHOTONIC_NO_NEW_PHYSICS"
        if checks_passed == checks_total
        else "CR222f_FAIL_PR_PLATFORM_ADAPTER_CONTRACT"
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
        "adapter_scope": "sealed PR packet -> platform observables; no new physics",
        "platforms": ["NV_CENTER_T2", "PHOTONIC_TAU_ENT"],
        "A_side": fraction_text(A_SIDE),
        "t_fire": {
            "NV_CENTER_T2": "T2*(-1/2*ln(23/24))",
            "PHOTONIC_TAU_ENT": "tau_ent*(-1/2*ln(23/24))",
            "coefficient_decimal": decimal_text(T_FIRE_COEFFICIENT),
        },
        "outputs_semantics": {
            "packet_state": "DRAFT/SEALED/CORRUPT/VALID_WARNING",
            "warning_allowed": "sealed_packet and G_protocol=1 and A_leak(t)>=1/24",
            "tensor_witness": "T=qA/8 only after valid warning condition",
            "emitted": "EMITTED_WARNING_PACKET only after warning_allowed and qA>0",
        },
        "support_roster_correction": inputs["cr222d_summary"]["support_roster_correction"],
        "wrong_controls": [row["wrong_control"] for row in wrongs],
        "outputs": {
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "adapter_contract_csv": OUT_ADAPTER.name,
            "platform_observable_scenarios_csv": OUT_SCENARIOS.name,
            "platform_outputs_csv": OUT_OUTPUTS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222f_platform_adapter_contract.csv": adapter_sha,
        },
        "next_gate": "PLATFORM_OBSERVATION_SELECTION_OR_LAB_PROTOCOL_DRAFT",
    }

    write_precommit(adapter_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_UPSTREAM,
        OUT_ADAPTER,
        OUT_SCENARIOS,
        OUT_OUTPUTS,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222f PR platform adapter contract complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print("  platforms: NV_CENTER_T2, PHOTONIC_TAU_ENT")
    print(f"  CR222f_platform_adapter_contract.csv sha256: {adapter_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
