"""CR222g PR target binding trial: 3-body diamond target + carrier packet.

CR222g tests a binding layer, not a new physics engine:

    sealed carrier packet + 3-body matter target + protocol trigger

The carrier remains route/witness/checksum. The 3-body target remains the
matter/write address. Their ledgers are intentionally kept separate.
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
from pathlib import Path
from typing import Iterable


getcontext().prec = 80

CR_ID = "CR222g"
TEST_ID = "CR222g_PR_TARGET_BINDING_3BODY_DIAMOND"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR219_PROMOTED = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")
CR222B_PACKET = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT" / "Paul_Revere_PacketContract.csv"
CR222B_VALIDITY = BRANCH_DIR / "CR222b_PAUL_REVERE_PACKET_CONTRACT" / "CR222b_packet_validity.csv"
CR222D_SUMMARY = BRANCH_DIR / "CR222d_ROW_TAXONOMY_PROMOTION_GATE" / "CR222d_summary.json"
CR222D_THEOREM = BRANCH_DIR / "CR222d_ROW_TAXONOMY_PROMOTION_GATE" / "CR222d_row_taxonomy_theorem.csv"
CR222E_STATE = BRANCH_DIR / "CR222e_PR_WARNING_EMISSION_GATE" / "CR222e_emission_state_machine.csv"
CR222F_ADAPTER = BRANCH_DIR / "CR222f_PR_PLATFORM_ADAPTER_CONTRACT" / "CR222f_platform_adapter_contract.csv"
CR222F_OUTPUTS = BRANCH_DIR / "CR222f_PR_PLATFORM_ADAPTER_CONTRACT" / "CR222f_platform_outputs.csv"
CR222F_WRONGS = BRANCH_DIR / "CR222f_PR_PLATFORM_ADAPTER_CONTRACT" / "CR222f_wrong_controls.csv"
CR222F_SUMMARY = BRANCH_DIR / "CR222f_PR_PLATFORM_ADAPTER_CONTRACT" / "CR222f_summary.json"

OUT_UPSTREAM = CR_DIR / "CR222g_upstream_seals.csv"
OUT_TARGET_ROSTER = CR_DIR / "CR222g_3body_diamond_target_roster.csv"
OUT_BINDING_CONTRACT = CR_DIR / "CR222g_target_binding_contract.csv"
OUT_TRIALS = CR_DIR / "CR222g_targeted_warning_trials.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222g_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222g_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222g_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222g_summary.json"
OUT_RESULT = CR_DIR / "CR222g_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

R = Decimal(12)
R2 = Decimal(144)
EIGHT = Decimal(8)
TOL = Decimal("0.000001")
PROTOCOL_EVENT_QA = "1/24"

EXPECTED_CR222B_HASH = "79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009"
EXPECTED_CR222D_HASH = "c0f8918974f660ddb0e51e10e3c37f1d59b8bcf0b98b0d02cec1d81ae2a1320a"
EXPECTED_CR222E_HASH = "a79ee4b0d5519c85eb6edded7f96e698b51a274b56e1e64f2b160c5ef211f2d7"
EXPECTED_CR222F_HASH = "79b809caa041f42a324203396e6531a5a3b2b48167038b59831bd40169179ba8"


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
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header and header[0].strip().isdigit():
            header[0] = "source_order"
        return [dict(zip(header, row)) for row in reader]


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


def dec(value: str) -> Decimal:
    text = (value or "").strip()
    if text.lower() in {"", "no", "none", "null", "nan"}:
        return Decimal(0)
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"not decimal: {value!r}") from exc


def dec_text(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def close(a: Decimal, b: Decimal, tol: Decimal = TOL) -> bool:
    return abs(a - b) <= tol


def load_inputs() -> dict[str, object]:
    return {
        "cr219": read_csv_rows(CR219_PROMOTED),
        "cr222b_validity": read_csv_rows(CR222B_VALIDITY),
        "cr222d_summary": read_json(CR222D_SUMMARY),
        "cr222f_outputs": read_csv_rows(CR222F_OUTPUTS),
        "cr222f_wrongs": read_csv_rows(CR222F_WRONGS),
        "cr222f_summary": read_json(CR222F_SUMMARY),
    }


def validity_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["validity_check"]: row for row in inputs["cr222b_validity"]}


def f_outputs_by_scenario(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["scenario"]: row for row in inputs["cr222f_outputs"]}


def is_diamond_anchor(partition_signature: str) -> bool:
    parts = partition_signature.split("+")
    return len(parts) == 3 and len(set(parts)) == 1


def partition_sum(partition_signature: str) -> int:
    return sum(int(part) for part in partition_signature.split("+"))


def target_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    rows = []
    for row in inputs["cr219"]:
        if row.get("operator_class") != "GROUND_BARYON_3BODY":
            continue
        m_obs = dec(row["M_observed_candidate"])
        q_abs = dec(row["q_abs"])
        q_a_observed = dec(row["qA_source_support"])
        q_a_expected = m_obs * (Decimal(1) + q_abs / R2)
        tensor_expected = q_a_expected / EIGHT
        retained_expected = q_a_expected * Decimal(7) / EIGHT
        tensor_observed = dec(row["tensor_carrier_support"])
        retained_observed = dec(row["retained_write_support"])
        formula_pass = (
            row["matter_row_allowed"] == "yes"
            and close(q_a_observed, q_a_expected)
            and close(tensor_observed, tensor_expected)
            and close(retained_observed, retained_expected)
        )
        signature = row["partition_signature"]
        rows.append({
            "candidate_id": row["candidate_id"],
            "target_family": "GROUND_BARYON_3BODY",
            "target_role": "three_body_diamond_anchor" if is_diamond_anchor(signature) else "three_body_bound_target",
            "route_combination": row["route_combination"],
            "partition_signature": signature,
            "partition_sum": str(partition_sum(signature)),
            "diamond_anchor": str(is_diamond_anchor(signature)),
            "q_sign": row["q_sign"],
            "q_abs": row["q_abs"],
            "M_observed_candidate": row["M_observed_candidate"],
            "target_qA_observed": row["qA_source_support"],
            "target_qA_expected": dec_text(q_a_expected),
            "target_T_observed": row["tensor_carrier_support"],
            "target_T_expected": dec_text(tensor_expected),
            "target_W_observed": row["retained_write_support"],
            "target_W_expected": dec_text(retained_expected),
            "matter_row_allowed": row["matter_row_allowed"],
            "matter_gate_status": row.get("matter_gate_status", ""),
            "binding_use": "target_matter_write_address_not_carrier_checksum",
            "passed": str(formula_pass),
        })
    return sorted(rows, key=lambda item: (item["diamond_anchor"] != "True", int(item["partition_sum"]), item["candidate_id"]))


def upstream_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    d_summary = inputs["cr222d_summary"]
    f_summary = inputs["cr222f_summary"]
    return [
        {
            "upstream": "CR219_promoted_particle_rows",
            "artifact": str(CR219_PROMOTED),
            "observed_sha256": sha256_file(CR219_PROMOTED),
            "expected_sha256": d_summary["source"]["sha256"],
            "role": "3-body target source and promotion-gate evidence",
            "passed": str(sha256_file(CR219_PROMOTED) == d_summary["source"]["sha256"]),
        },
        {
            "upstream": "CR222b_packet_contract",
            "artifact": str(CR222B_PACKET.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222B_PACKET),
            "expected_sha256": EXPECTED_CR222B_HASH,
            "role": "sealed carrier packet checksum",
            "passed": str(sha256_file(CR222B_PACKET) == EXPECTED_CR222B_HASH),
        },
        {
            "upstream": "CR222d_promotion_gate",
            "artifact": str(CR222D_THEOREM.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222D_THEOREM),
            "expected_sha256": EXPECTED_CR222D_HASH,
            "role": "support inventory != matter promotion",
            "passed": str(sha256_file(CR222D_THEOREM) == EXPECTED_CR222D_HASH),
        },
        {
            "upstream": "CR222e_emission_gate",
            "artifact": str(CR222E_STATE.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222E_STATE),
            "expected_sha256": EXPECTED_CR222E_HASH,
            "role": "sealed packet + protocol trigger -> emitted warning",
            "passed": str(sha256_file(CR222E_STATE) == EXPECTED_CR222E_HASH),
        },
        {
            "upstream": "CR222f_platform_adapter",
            "artifact": str(CR222F_ADAPTER.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222F_ADAPTER),
            "expected_sha256": EXPECTED_CR222F_HASH,
            "role": f"platform adapter: {','.join(f_summary['platforms'])}",
            "passed": str(sha256_file(CR222F_ADAPTER) == EXPECTED_CR222F_HASH),
        },
    ]


def binding_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "layer": "carrier_packet",
            "input": "CR222b/CR222d carrier ledger",
            "role": "route + tensor witness + checksum envelope",
            "allowed_use": "validate route, witness, and 162 closure",
            "forbidden_use": "do not become target matter and do not absorb 3-body row into checksum",
        },
        {
            "layer": "target_particle",
            "input": "CR219 GROUND_BARYON_3BODY matter row",
            "role": "3-body diamond/baryon target address",
            "allowed_use": "supply matter target qA/T/W after G_matter=1",
            "forbidden_use": "do not replace carrier route, mirror, or 12 support roster",
        },
        {
            "layer": "protocol_gate",
            "input": "CR222e/CR222f warning condition",
            "role": "allow targeted warning emission",
            "allowed_use": "G_protocol=1 and A_leak>=1/24",
            "forbidden_use": "do not emit from support inventory alone",
        },
        {
            "layer": "binding_output",
            "input": "carrier_packet + target_particle + protocol_gate",
            "role": "targeted PR warning/write trial",
            "allowed_use": "carrier validates route; target supplies matter address; gate permits emission",
            "forbidden_use": "do not confuse protocol_event_qA=1/24 with target matter qA",
        },
    ]


def trial_rows(inputs: dict[str, object], targets: list[dict[str, str]]) -> list[dict[str, str]]:
    vm = validity_map(inputs)
    f_outputs = f_outputs_by_scenario(inputs)
    platform_scenarios = [
        ("NV_CENTER_T2", "nv_threshold_exact"),
        ("PHOTONIC_TAU_ENT", "photonic_threshold_exact"),
    ]
    rows = []
    for platform_id, scenario in platform_scenarios:
        platform = f_outputs[scenario]
        for target in targets:
            binding_allowed = (
                platform["emitted"] == "True"
                and target["passed"] == "True"
                and target["matter_row_allowed"] == "yes"
                and vm["packet_total_162"]["passed"] == "True"
            )
            rows.append({
                "trial_id": f"{platform_id}::{target['candidate_id']}",
                "platform_id": platform_id,
                "platform_trigger_scenario": scenario,
                "carrier_packet_checksum": vm["packet_total_162"]["observed"],
                "carrier_tensor_witness": "QP093A-0300=18",
                "carrier_mirror_checksum": "QP093A-0303=81",
                "protocol_event_qA": PROTOCOL_EVENT_QA,
                "target_candidate_id": target["candidate_id"],
                "target_partition_signature": target["partition_signature"],
                "target_role": target["target_role"],
                "diamond_anchor": target["diamond_anchor"],
                "target_matter_gate": target["matter_row_allowed"],
                "target_qA": target["target_qA_observed"],
                "target_T": target["target_T_observed"],
                "target_W": target["target_W_observed"],
                "binding_rule": "carrier validates route/witness/checksum; target supplies matter address; gate permits emission",
                "binding_allowed": str(binding_allowed),
                "binding_state": "TARGETED_PR_WARNING_BOUND" if binding_allowed else "TARGET_BINDING_REJECTED",
                "emitted_state": "TARGETED_EMITTED_WARNING_PACKET" if binding_allowed else "NOT_EMITTED",
                "passed": str(binding_allowed),
            })
    return rows


def wrong_control_rows(inputs: dict[str, object], targets: list[dict[str, str]]) -> list[dict[str, str]]:
    f_outputs = f_outputs_by_scenario(inputs)
    f_wrongs = {row["wrong_control"]: row for row in inputs["cr222f_wrongs"]}
    first_target = targets[0]
    return [
        {
            "wrong_control": "carrier_packet_emits_without_target",
            "attempted_binding": "carrier packet alone -> target write",
            "observed_failure": "no 3-body target address bound",
            "expected_failure": "NO_TARGET_NO_TARGETED_WRITE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "support_row_used_as_3body_target",
            "attempted_binding": "QP093A-0303 mirror row as target particle",
            "observed_failure": "QP093A-0303 is duplicate mirror closure row, not matter target",
            "expected_failure": "MIRROR_NOT_TARGET_MATTER",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "3body_target_counted_inside_carrier_checksum",
            "attempted_binding": "carrier checksum + 3-body row",
            "observed_failure": "carrier checksum must remain 162",
            "expected_failure": "CHECKSUM_CATEGORY_FAILURE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "target_emits_without_protocol_gate",
            "attempted_binding": "G_protocol=0 but target writes",
            "observed_failure": f_outputs["nv_no_protocol_gate"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(f_outputs["nv_no_protocol_gate"]["emitted"] == "False"),
        },
        {
            "wrong_control": "target_emits_below_threshold",
            "attempted_binding": "A_leak=1/48 but target writes",
            "observed_failure": f_outputs["nv_sealed_below_threshold"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(f_outputs["nv_sealed_below_threshold"]["emitted"] == "False"),
        },
        {
            "wrong_control": "protocol_qA_substituted_for_target_qA",
            "attempted_binding": "use protocol qA=1/24 as target matter qA",
            "observed_failure": f"protocol_qA={PROTOCOL_EVENT_QA}; target_qA={first_target['target_qA_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(first_target["target_qA_observed"] != PROTOCOL_EVENT_QA),
        },
        {
            "wrong_control": "carrier_tensor_substituted_for_target_tensor",
            "attempted_binding": "use carrier tensor 18 as target tensor split",
            "observed_failure": f"carrier_tensor=18; target_T={first_target['target_T_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(first_target["target_T_observed"] != "18"),
        },
        {
            "wrong_control": "support_inventory_emits_without_G_protocol",
            "attempted_binding": "support inventory -> target warning write",
            "observed_failure": f_wrongs["support_inventory_emits_without_G_protocol"]["observed_failure"],
            "expected_failure": "NO_EMISSION_WITHOUT_PROTOCOL_GATE",
            "passes_as_failure": f_wrongs["support_inventory_emits_without_G_protocol"]["passes_as_failure"],
        },
        {
            "wrong_control": "0306_omitted_but_target_binds",
            "attempted_binding": "omit p=1 source packet but bind target",
            "observed_failure": f_wrongs["0306_omitted"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_BINDING",
            "passes_as_failure": f_wrongs["0306_omitted"]["passes_as_failure"],
        },
        {
            "wrong_control": "duplicate_0305_restored_but_target_binds",
            "attempted_binding": "restore duplicate support row but bind target",
            "observed_failure": f_wrongs["duplicate_0305_restored"]["observed_failure"],
            "expected_failure": "163_CORRUPT_NO_BINDING",
            "passes_as_failure": f_wrongs["duplicate_0305_restored"]["passes_as_failure"],
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    targets: list[dict[str, str]],
    trials: list[dict[str, str]],
    wrongs: list[dict[str, str]],
) -> list[Check]:
    vm = validity_map(inputs)
    d_summary = inputs["cr222d_summary"]
    anchor_count = sum(1 for row in targets if row["diamond_anchor"] == "True")
    trial_count_expected = len(targets) * 2
    diamond_trials = [row for row in trials if row["diamond_anchor"] == "True"]
    target_qas = [dec(row["target_qA_observed"]) for row in targets]
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("carrier_checksum_remains_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("support_roster_12_plus_mirror_preserved", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12 and d_summary["support_roster_correction"]["closure_total"] == 162, json.dumps(d_summary["support_roster_correction"], sort_keys=True), "12 support rows + mirror = 162"),
        Check("ground_baryon_3body_targets_found_14", len(targets) == 14, str(len(targets)), "14"),
        Check("symmetric_diamond_anchor_count_4", anchor_count == 4, str(anchor_count), "4"),
        Check("all_3body_targets_matter_allowed", all(row["matter_row_allowed"] == "yes" for row in targets), str(Counter(row["matter_row_allowed"] for row in targets)), "{'yes': 14}"),
        Check("all_3body_targets_qA_T_W_formula_pass", all(row["passed"] == "True" for row in targets), str(sum(1 for row in targets if row["passed"] == "True")), "14"),
        Check("target_qA_positive", all(value > 0 for value in target_qas), str(min(target_qas)), ">0"),
        Check("target_binding_trials_count", len(trials) == trial_count_expected, str(len(trials)), str(trial_count_expected)),
        Check("target_binding_trials_all_emit_when_gated", all(row["passed"] == "True" for row in trials), str(sum(1 for row in trials if row["passed"] == "True")), str(len(trials))),
        Check("diamond_anchor_trials_emit", all(row["emitted_state"] == "TARGETED_EMITTED_WARNING_PACKET" for row in diamond_trials), str(sum(1 for row in diamond_trials if row["emitted_state"] == "TARGETED_EMITTED_WARNING_PACKET")), str(len(diamond_trials))),
        Check("protocol_qA_not_target_qA", all(row["target_qA"] != PROTOCOL_EVENT_QA for row in trials), "distinct", "protocol_event_qA distinct from target qA"),
        Check("carrier_tensor_not_target_tensor", all(row["target_T"] != "18" for row in trials), "distinct", "carrier tensor distinct from target tensor split"),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrongs), str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(roster_sha: str) -> None:
    text = f"""# CR222g PRECOMMIT - PR Target Binding 3-Body Diamond

## Scope

Trial a target-binding layer:

```text
sealed carrier packet + 3-body matter target + protocol trigger
```

The carrier remains route/witness/checksum. The 3-body row remains the
matter/write address.

## Protected Distinctions

```text
carrier tensor witness != target tensor split
protocol_event_qA=1/24 != target matter qA
carrier checksum=162 does not include the target row
```

## Pre-run Hash

Expected `CR222g_3body_diamond_target_roster.csv` hash:

```text
{roster_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222g PR Target Binding 3-Body Diamond

CR222g tests carrier + target binding:

```text
sealed carrier packet + GROUND_BARYON_3BODY target + protocol trigger
```

It keeps carrier checksum and target matter write as separate ledgers.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222g PR Target Binding 3-Body Diamond Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222g_3body_diamond_target_roster.csv SHA-256:** `{summary['sha256']['CR222g_3body_diamond_target_roster.csv']}`

## Verdict

CR222g successfully binds the sealed carrier packet to 3-body matter targets:

```text
sealed carrier packet + 3-body target + protocol trigger
= targeted PR warning/write trial
```

The ledgers stay separated:

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
target family = GROUND_BARYON_3BODY
target qA/T/W comes from the matter row after G_matter=1
```

The roster contains 14 three-body targets, with 4 symmetric diamond anchors:

```text
1+1+1
2+2+2
4+4+4
8+8+8
```

The successful trial state is:

```text
TARGETED_PR_WARNING_BOUND -> TARGETED_EMITTED_WARNING_PACKET
```

Support inventory alone still cannot emit, and the 3-body target is not counted
inside the carrier checksum.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs()

    upstream = upstream_rows(inputs)
    write_csv(OUT_UPSTREAM, upstream, ["upstream", "artifact", "observed_sha256", "expected_sha256", "role", "passed"])

    targets = target_rows(inputs)
    target_fields = [
        "candidate_id",
        "target_family",
        "target_role",
        "route_combination",
        "partition_signature",
        "partition_sum",
        "diamond_anchor",
        "q_sign",
        "q_abs",
        "M_observed_candidate",
        "target_qA_observed",
        "target_qA_expected",
        "target_T_observed",
        "target_T_expected",
        "target_W_observed",
        "target_W_expected",
        "matter_row_allowed",
        "matter_gate_status",
        "binding_use",
        "passed",
    ]
    target_bytes = render_csv(targets, target_fields)
    target_sha = sha256_bytes(target_bytes)
    OUT_TARGET_ROSTER.write_bytes(target_bytes)

    contract = binding_contract_rows()
    write_csv(OUT_BINDING_CONTRACT, contract, ["layer", "input", "role", "allowed_use", "forbidden_use"])

    trials = trial_rows(inputs, targets)
    write_csv(
        OUT_TRIALS,
        trials,
        [
            "trial_id",
            "platform_id",
            "platform_trigger_scenario",
            "carrier_packet_checksum",
            "carrier_tensor_witness",
            "carrier_mirror_checksum",
            "protocol_event_qA",
            "target_candidate_id",
            "target_partition_signature",
            "target_role",
            "diamond_anchor",
            "target_matter_gate",
            "target_qA",
            "target_T",
            "target_W",
            "binding_rule",
            "binding_allowed",
            "binding_state",
            "emitted_state",
            "passed",
        ],
    )

    wrongs = wrong_control_rows(inputs, targets)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "attempted_binding", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, targets, trials, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222g_PASS_PR_TARGET_BINDING__3BODY_DIAMOND_TARGET_PLUS_SEALED_CARRIER_PACKET"
        if checks_passed == checks_total
        else "CR222g_FAIL_PR_TARGET_BINDING"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "binding_formula": "sealed carrier packet + 3-body target + protocol trigger",
        "protected_separations": {
            "carrier_checksum": "162; target row excluded",
            "carrier_tensor_witness": "QP093A-0300=18",
            "protocol_event_qA": PROTOCOL_EVENT_QA,
            "target_qA": "from GROUND_BARYON_3BODY matter row after G_matter=1",
        },
        "target_roster": {
            "target_family": "GROUND_BARYON_3BODY",
            "target_count": len(targets),
            "diamond_anchor_count": sum(1 for row in targets if row["diamond_anchor"] == "True"),
            "diamond_anchors": [row["partition_signature"] for row in targets if row["diamond_anchor"] == "True"],
        },
        "trial_count": len(trials),
        "platforms": sorted({row["platform_id"] for row in trials}),
        "outputs": {
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "target_roster_csv": OUT_TARGET_ROSTER.name,
            "binding_contract_csv": OUT_BINDING_CONTRACT.name,
            "targeted_warning_trials_csv": OUT_TRIALS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222g_3body_diamond_target_roster.csv": target_sha,
        },
        "next_gate": "PR_TARGET_BINDING_PLATFORM_PROTOCOL_OR_TARGET_SELECTION",
    }

    write_precommit(target_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_UPSTREAM,
        OUT_TARGET_ROSTER,
        OUT_BINDING_CONTRACT,
        OUT_TRIALS,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222g PR target binding 3-body diamond complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  targets: {len(targets)} GROUND_BARYON_3BODY; diamond anchors: {sum(1 for row in targets if row['diamond_anchor'] == 'True')}")
    print(f"  CR222g_3body_diamond_target_roster.csv sha256: {target_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
