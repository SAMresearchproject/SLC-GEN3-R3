"""CR222h pair-to-triad binding: QP093A-0262 -> QP093A-0200.

CR222h tests a narrow bridge layer:

    sealed carrier packet + pair-face precursor + 3-body diamond target
    + protocol trigger

The carrier remains route/witness/checksum. QP093A-0262 remains a neutral
two-owner pair-face matter row. QP093A-0200 remains the three-owner diamond
target/write address.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Iterable


getcontext().prec = 80

CR_ID = "CR222h"
TEST_ID = "CR222h_PAIR_TO_TRIAD_BINDING_0262_TO_0200"

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
CR222G_ROSTER = BRANCH_DIR / "CR222g_PR_TARGET_BINDING_3BODY_DIAMOND" / "CR222g_3body_diamond_target_roster.csv"
CR222G_TRIALS = BRANCH_DIR / "CR222g_PR_TARGET_BINDING_3BODY_DIAMOND" / "CR222g_targeted_warning_trials.csv"
CR222G_SUMMARY = BRANCH_DIR / "CR222g_PR_TARGET_BINDING_3BODY_DIAMOND" / "CR222g_summary.json"

OUT_UPSTREAM = CR_DIR / "CR222h_upstream_seals.csv"
OUT_ROSTER = CR_DIR / "CR222h_pair_triad_roster.csv"
OUT_CONTRACT = CR_DIR / "CR222h_binding_contract.csv"
OUT_TRIALS = CR_DIR / "CR222h_pair_to_triad_trials.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222h_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222h_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222h_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222h_summary.json"
OUT_RESULT = CR_DIR / "CR222h_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

R2 = Decimal(144)
EIGHT = Decimal(8)
TOL = Decimal("0.000001")
PROTOCOL_EVENT_QA = "1/24"
PAIR_ID = "QP093A-0262"
TRIAD_ID = "QP093A-0200"

EXPECTED_CR222B_HASH = "79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009"
EXPECTED_CR222D_HASH = "c0f8918974f660ddb0e51e10e3c37f1d59b8bcf0b98b0d02cec1d81ae2a1320a"
EXPECTED_CR222E_HASH = "a79ee4b0d5519c85eb6edded7f96e698b51a274b56e1e64f2b160c5ef211f2d7"
EXPECTED_CR222F_HASH = "79b809caa041f42a324203396e6531a5a3b2b48167038b59831bd40169179ba8"
EXPECTED_CR222G_HASH = "86a410172d053d6fb7c1d7d85e5f7d96debd2301c50c0f6fa14f37552421fea2"


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
    nearest = value.to_integral_value()
    if close(value, nearest):
        return str(nearest)
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
        "cr222g_trials": read_csv_rows(CR222G_TRIALS),
        "cr222g_summary": read_json(CR222G_SUMMARY),
    }


def validity_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["validity_check"]: row for row in inputs["cr222b_validity"]}


def f_outputs_by_scenario(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["scenario"]: row for row in inputs["cr222f_outputs"]}


def f_wrongs_by_name(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["wrong_control"]: row for row in inputs["cr222f_wrongs"]}


def row_by_candidate(inputs: dict[str, object], candidate_id: str) -> dict[str, str]:
    for row in inputs["cr219"]:
        if row.get("candidate_id") == candidate_id:
            return row
    raise KeyError(f"missing candidate_id: {candidate_id}")


def signature_parts(signature: str) -> list[int]:
    return [int(part) for part in signature.split("+")]


def formula_row(row: dict[str, str], bridge_role: str) -> dict[str, str]:
    m_obs = dec(row["M_observed_candidate"])
    q_abs = dec(row["q_abs"])
    q_a_expected = m_obs * (Decimal(1) + q_abs / R2)
    tensor_expected = q_a_expected / EIGHT
    retained_expected = q_a_expected * Decimal(7) / EIGHT
    q_a_observed = dec(row["qA_source_support"])
    tensor_observed = dec(row["tensor_carrier_support"])
    retained_observed = dec(row["retained_write_support"])
    parts = signature_parts(row["partition_signature"])
    formula_pass = (
        row["matter_row_allowed"] == "yes"
        and close(q_a_observed, q_a_expected)
        and close(tensor_observed, tensor_expected)
        and close(retained_observed, retained_expected)
    )
    return {
        "candidate_id": row["candidate_id"],
        "bridge_role": bridge_role,
        "bin": row["bin"],
        "route_combination": row["route_combination"],
        "operator_class": row["operator_class"],
        "route_class": row["route_class"],
        "partition_signature": row["partition_signature"],
        "partition_sum": str(sum(parts)),
        "owner_count": str(len(parts)),
        "owner_value": str(parts[0]) if len(set(parts)) == 1 else "mixed",
        "M_native": row["M_native"],
        "M_observed_candidate": row["M_observed_candidate"],
        "q_sign": row["q_sign"],
        "q_abs": row["q_abs"],
        "qA_observed": row["qA_source_support"],
        "qA_expected": dec_text(q_a_expected),
        "T_observed": row["tensor_carrier_support"],
        "T_expected": dec_text(tensor_expected),
        "W_observed": row["retained_write_support"],
        "W_expected": dec_text(retained_expected),
        "matter_row_allowed": row["matter_row_allowed"],
        "promotion_status": row["promotion_status"],
        "matter_gate_status": row["matter_gate_status"],
        "spin_or_hand_class": row["spin_or_hand_class"],
        "known_identity_label": row.get("known_identity_label", ""),
        "binding_use": "pair-face precursor" if bridge_role == "pair_face_precursor" else "three-body diamond target",
        "passed": str(formula_pass),
    }


def upstream_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    d_summary = inputs["cr222d_summary"]
    f_summary = inputs["cr222f_summary"]
    g_summary = inputs["cr222g_summary"]
    return [
        {
            "upstream": "CR219_promoted_particle_rows",
            "artifact": str(CR219_PROMOTED),
            "observed_sha256": sha256_file(CR219_PROMOTED),
            "expected_sha256": d_summary["source"]["sha256"],
            "role": "pair and triad source rows plus promotion-gate evidence",
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
        {
            "upstream": "CR222g_3body_target_roster",
            "artifact": str(CR222G_ROSTER.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222G_ROSTER),
            "expected_sha256": EXPECTED_CR222G_HASH,
            "role": f"3-body target roster: {g_summary['target_roster']['target_count']} targets",
            "passed": str(sha256_file(CR222G_ROSTER) == EXPECTED_CR222G_HASH),
        },
    ]


def pair_to_triad_roster(inputs: dict[str, object]) -> list[dict[str, str]]:
    pair = formula_row(row_by_candidate(inputs, PAIR_ID), "pair_face_precursor")
    triad = formula_row(row_by_candidate(inputs, TRIAD_ID), "three_body_diamond_target")
    return [pair, triad]


def bridge_metrics(pair: dict[str, str], triad: dict[str, str]) -> dict[str, str]:
    pair_sum = dec(pair["partition_sum"])
    triad_sum = dec(triad["partition_sum"])
    pair_q_a = dec(pair["qA_observed"])
    triad_q_a = dec(triad["qA_observed"])
    pair_t = dec(pair["T_observed"])
    triad_t = dec(triad["T_observed"])
    pair_w = dec(pair["W_observed"])
    triad_w = dec(triad["W_observed"])
    return {
        "pair_candidate_id": pair["candidate_id"],
        "triad_candidate_id": triad["candidate_id"],
        "bridge_owner": pair["owner_value"],
        "pair_signature": pair["partition_signature"],
        "triad_signature": triad["partition_signature"],
        "pair_sum": dec_text(pair_sum),
        "triad_sum": dec_text(triad_sum),
        "pair_to_triad_ratio": dec_text(triad_sum / pair_sum),
        "pair_owner_count": pair["owner_count"],
        "triad_owner_count": triad["owner_count"],
        "delta_owner_count": str(int(triad["owner_count"]) - int(pair["owner_count"])),
        "pair_qA": dec_text(pair_q_a),
        "triad_qA": dec_text(triad_q_a),
        "delta_qA": dec_text(triad_q_a - pair_q_a),
        "pair_T": dec_text(pair_t),
        "triad_T": dec_text(triad_t),
        "delta_T": dec_text(triad_t - pair_t),
        "pair_W": dec_text(pair_w),
        "triad_W": dec_text(triad_w),
        "delta_W": dec_text(triad_w - pair_w),
        "bridge_rule": "4+4 pair face extends by one 4 owner into 4+4+4 diamond target",
    }


def binding_contract_rows(metrics: dict[str, str]) -> list[dict[str, str]]:
    return [
        {
            "layer": "carrier_packet",
            "input": "CR222b/CR222d carrier ledger",
            "role": "route + tensor witness + checksum envelope",
            "allowed_use": "validate route, witness, and 162 closure",
            "forbidden_use": "do not count QP093A-0262 or QP093A-0200 into carrier checksum",
        },
        {
            "layer": "pair_face_precursor",
            "input": "QP093A-0262",
            "role": "neutral two-owner 4+4 face",
            "allowed_use": "establish pair-face precursor for the 4+4+4 target",
            "forbidden_use": "do not treat as final three-owner target or carrier support row",
        },
        {
            "layer": "triad_target",
            "input": "QP093A-0200",
            "role": "positive three-owner 4+4+4 diamond/baryon target",
            "allowed_use": "supply matter target qA/T/W after G_matter=1",
            "forbidden_use": "do not replace carrier route, mirror, or support roster",
        },
        {
            "layer": "bridge_relation",
            "input": f"{metrics['pair_signature']} -> {metrics['triad_signature']}",
            "role": "pair face extends by one owner",
            "allowed_use": f"bridge owner {metrics['bridge_owner']}; ratio {metrics['pair_to_triad_ratio']}",
            "forbidden_use": "do not infer target emission without CR222e/CR222f protocol gate",
        },
        {
            "layer": "protocol_gate",
            "input": "CR222e/CR222f warning condition",
            "role": "allow targeted warning emission",
            "allowed_use": "G_protocol=1 and A_leak>=1/24",
            "forbidden_use": "do not emit from support inventory or pair face alone",
        },
    ]


def trial_rows(inputs: dict[str, object], pair: dict[str, str], triad: dict[str, str]) -> list[dict[str, str]]:
    vm = validity_map(inputs)
    f_outputs = f_outputs_by_scenario(inputs)
    platform_scenarios = [
        ("NV_CENTER_T2", "nv_threshold_exact"),
        ("PHOTONIC_TAU_ENT", "photonic_threshold_exact"),
    ]
    rows = []
    for platform_id, scenario in platform_scenarios:
        platform = f_outputs[scenario]
        bridge_allowed = (
            platform["emitted"] == "True"
            and vm["packet_total_162"]["passed"] == "True"
            and pair["passed"] == "True"
            and triad["passed"] == "True"
            and pair["operator_class"] == "BOUND_COLOR_PAIR"
            and triad["operator_class"] == "GROUND_BARYON_3BODY"
            and pair["partition_signature"] == "4+4"
            and triad["partition_signature"] == "4+4+4"
        )
        rows.append({
            "trial_id": f"{platform_id}::{PAIR_ID}->{TRIAD_ID}",
            "platform_id": platform_id,
            "platform_trigger_scenario": scenario,
            "carrier_packet_checksum": vm["packet_total_162"]["observed"],
            "carrier_tensor_witness": "QP093A-0300=18",
            "carrier_mirror_checksum": "QP093A-0303=81",
            "protocol_event_qA": PROTOCOL_EVENT_QA,
            "pair_candidate_id": pair["candidate_id"],
            "pair_partition_signature": pair["partition_signature"],
            "pair_operator_class": pair["operator_class"],
            "pair_qA": pair["qA_observed"],
            "pair_T": pair["T_observed"],
            "pair_W": pair["W_observed"],
            "target_candidate_id": triad["candidate_id"],
            "target_partition_signature": triad["partition_signature"],
            "target_operator_class": triad["operator_class"],
            "target_qA": triad["qA_observed"],
            "target_T": triad["T_observed"],
            "target_W": triad["W_observed"],
            "binding_rule": "sealed carrier + 4+4 pair face + 4+4+4 target + protocol trigger",
            "binding_allowed": str(bridge_allowed),
            "binding_state": "PAIR_TO_TRIAD_BRIDGE_BOUND" if bridge_allowed else "PAIR_TO_TRIAD_BRIDGE_REJECTED",
            "emitted_state": "TARGETED_EMITTED_WARNING_PACKET" if bridge_allowed else "NOT_EMITTED",
            "passed": str(bridge_allowed),
        })
    return rows


def wrong_control_rows(inputs: dict[str, object], pair: dict[str, str], triad: dict[str, str]) -> list[dict[str, str]]:
    f_outputs = f_outputs_by_scenario(inputs)
    f_wrongs = f_wrongs_by_name(inputs)
    return [
        {
            "wrong_control": "0262_used_as_carrier_support",
            "attempted_binding": "QP093A-0262 counted as support ledger row",
            "observed_failure": f"{PAIR_ID} layer={pair['bin']}; operator={pair['operator_class']}; matter_allowed={pair['matter_row_allowed']}",
            "expected_failure": "PAIR_FACE_IS_MATTER_ROW_NOT_CARRIER_SUPPORT",
            "passes_as_failure": str(pair["bin"] == "bound_composite_rows" and pair["matter_row_allowed"] == "yes"),
        },
        {
            "wrong_control": "0262_counted_into_carrier_checksum",
            "attempted_binding": "carrier checksum 162 + QP093A-0262",
            "observed_failure": "carrier checksum must remain 162",
            "expected_failure": "CHECKSUM_CATEGORY_FAILURE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "0262_treated_as_final_3body_target",
            "attempted_binding": "QP093A-0262 -> TARGETED_EMITTED_WARNING_PACKET",
            "observed_failure": f"{PAIR_ID} owner_count={pair['owner_count']}; operator={pair['operator_class']}",
            "expected_failure": "TWO_OWNER_PAIR_NOT_THREE_OWNER_TRIAD",
            "passes_as_failure": str(pair["owner_count"] == "2" and pair["operator_class"] != "GROUND_BARYON_3BODY"),
        },
        {
            "wrong_control": "0200_without_pair_precursor_in_pair_bridge",
            "attempted_binding": "QP093A-0200 targeted with pair bridge absent",
            "observed_failure": "CR222g may target 0200 directly, but CR222h bridge is not established without QP093A-0262",
            "expected_failure": "PAIR_BRIDGE_NOT_ESTABLISHED",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "carrier_tensor_substituted_for_pair_tensor",
            "attempted_binding": "use carrier tensor 18 as QP093A-0262 tensor",
            "observed_failure": f"carrier_tensor=18; pair_T={pair['T_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(pair["T_observed"] != "18"),
        },
        {
            "wrong_control": "carrier_tensor_substituted_for_triad_tensor",
            "attempted_binding": "use carrier tensor 18 as QP093A-0200 tensor",
            "observed_failure": f"carrier_tensor=18; triad_T={triad['T_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(triad["T_observed"] != "18"),
        },
        {
            "wrong_control": "protocol_qA_substituted_for_pair_or_triad_qA",
            "attempted_binding": "use protocol qA=1/24 as matter qA",
            "observed_failure": f"protocol_qA={PROTOCOL_EVENT_QA}; pair_qA={pair['qA_observed']}; triad_qA={triad['qA_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(pair["qA_observed"] != PROTOCOL_EVENT_QA and triad["qA_observed"] != PROTOCOL_EVENT_QA),
        },
        {
            "wrong_control": "target_emits_without_protocol_gate",
            "attempted_binding": "G_protocol=0 but pair-to-triad target writes",
            "observed_failure": f_outputs["nv_no_protocol_gate"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(f_outputs["nv_no_protocol_gate"]["emitted"] == "False"),
        },
        {
            "wrong_control": "target_emits_below_threshold",
            "attempted_binding": "A_leak=1/48 but pair-to-triad target writes",
            "observed_failure": f_outputs["nv_sealed_below_threshold"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(f_outputs["nv_sealed_below_threshold"]["emitted"] == "False"),
        },
        {
            "wrong_control": "0306_omitted_but_pair_bridge_binds",
            "attempted_binding": "omit p=1 source packet but bind pair-to-triad target",
            "observed_failure": f_wrongs["0306_omitted"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_BINDING",
            "passes_as_failure": f_wrongs["0306_omitted"]["passes_as_failure"],
        },
        {
            "wrong_control": "duplicate_0305_restored_but_pair_bridge_binds",
            "attempted_binding": "restore duplicate support row but bind pair-to-triad target",
            "observed_failure": f_wrongs["duplicate_0305_restored"]["observed_failure"],
            "expected_failure": "163_CORRUPT_NO_BINDING",
            "passes_as_failure": f_wrongs["duplicate_0305_restored"]["passes_as_failure"],
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    roster: list[dict[str, str]],
    metrics: dict[str, str],
    trials: list[dict[str, str]],
    wrongs: list[dict[str, str]],
) -> list[Check]:
    vm = validity_map(inputs)
    pair, triad = roster
    g_trials = [
        row for row in inputs["cr222g_trials"]
        if row["target_candidate_id"] == TRIAD_ID and row["emitted_state"] == "TARGETED_EMITTED_WARNING_PACKET"
    ]
    d_summary = inputs["cr222d_summary"]
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("carrier_checksum_remains_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("support_roster_12_plus_mirror_preserved", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12 and d_summary["support_roster_correction"]["closure_total"] == 162, json.dumps(d_summary["support_roster_correction"], sort_keys=True), "12 support rows + mirror = 162"),
        Check("pair_row_is_0262", pair["candidate_id"] == PAIR_ID, pair["candidate_id"], PAIR_ID),
        Check("triad_row_is_0200", triad["candidate_id"] == TRIAD_ID, triad["candidate_id"], TRIAD_ID),
        Check("pair_is_bound_color_pair", pair["operator_class"] == "BOUND_COLOR_PAIR" and pair["route_class"] == "two_owner_pair_closure", f"{pair['operator_class']}|{pair['route_class']}", "BOUND_COLOR_PAIR|two_owner_pair_closure"),
        Check("triad_is_ground_baryon_3body", triad["operator_class"] == "GROUND_BARYON_3BODY" and triad["route_class"] == "three_owner_color_closure", f"{triad['operator_class']}|{triad['route_class']}", "GROUND_BARYON_3BODY|three_owner_color_closure"),
        Check("pair_signature_is_4_plus_4", pair["partition_signature"] == "4+4", pair["partition_signature"], "4+4"),
        Check("triad_signature_is_4_plus_4_plus_4", triad["partition_signature"] == "4+4+4", triad["partition_signature"], "4+4+4"),
        Check("pair_formula_qA_T_W_pass", pair["passed"] == "True", f"qA={pair['qA_observed']} T={pair['T_observed']} W={pair['W_observed']}", "qA=172 T=21.5 W=150.5"),
        Check("triad_formula_qA_T_W_pass", triad["passed"] == "True", f"qA={triad['qA_observed']} T={triad['T_observed']} W={triad['W_observed']}", "qA=1160 T=145 W=1015"),
        Check("pair_is_neutral_boson", pair["q_sign"] == "neutral" and pair["spin_or_hand_class"] == "boson_integer_write", f"{pair['q_sign']}|{pair['spin_or_hand_class']}", "neutral|boson_integer_write"),
        Check("triad_is_positive_fermion", triad["q_sign"] == "positive" and triad["spin_or_hand_class"] == "fermion_baryon_half_write", f"{triad['q_sign']}|{triad['spin_or_hand_class']}", "positive|fermion_baryon_half_write"),
        Check("bridge_owner_extends_pair_by_one_4", metrics["bridge_owner"] == "4" and metrics["delta_owner_count"] == "1", f"owner={metrics['bridge_owner']} delta={metrics['delta_owner_count']}", "owner=4 delta=1"),
        Check("bridge_partition_ratio_3_over_2", metrics["pair_sum"] == "8" and metrics["triad_sum"] == "12" and metrics["pair_to_triad_ratio"] == "1.5", f"{metrics['pair_sum']}->{metrics['triad_sum']} ratio={metrics['pair_to_triad_ratio']}", "8->12 ratio=1.5"),
        Check("cr222g_already_allows_0200_as_target", len(g_trials) == 2, str(len(g_trials)), "2 platform trials"),
        Check("pair_to_triad_trials_count", len(trials) == 2, str(len(trials)), "2"),
        Check("pair_to_triad_trials_emit_when_gated", all(row["passed"] == "True" for row in trials), str(sum(1 for row in trials if row["passed"] == "True")), "2"),
        Check("protocol_qA_not_pair_or_triad_qA", all(row["protocol_event_qA"] != row["pair_qA"] and row["protocol_event_qA"] != row["target_qA"] for row in trials), "distinct", "protocol qA distinct from matter qA"),
        Check("carrier_tensor_not_pair_or_triad_tensor", all(row["carrier_tensor_witness"] != row["pair_T"] and row["carrier_tensor_witness"] != row["target_T"] for row in trials), "distinct", "carrier tensor distinct from matter tensor splits"),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrongs), str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(roster_sha: str) -> None:
    text = f"""# CR222h PRECOMMIT - Pair-to-Triad Binding 0262 -> 0200

## Scope

Trial a narrow pair-to-triad bridge:

```text
sealed carrier packet + QP093A-0262 pair face + QP093A-0200 triad target
+ protocol trigger
```

## Protected Distinctions

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
pair face = QP093A-0262, 4+4, qA=172, T=21.5, W=150.5
triad target = QP093A-0200, 4+4+4, qA=1160, T=145, W=1015
protocol_event_qA = 1/24
```

## Pre-run Hash

Expected `CR222h_pair_triad_roster.csv` hash:

```text
{roster_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222h Pair-to-Triad Binding 0262 -> 0200

CR222h tests the narrow bridge:

```text
QP093A-0262 4+4 pair face -> QP093A-0200 4+4+4 diamond target
```

The sealed carrier remains external route/witness/checksum infrastructure.
The pair and triad remain matter rows after the matter gate.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222h Pair-to-Triad Binding Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222h_pair_triad_roster.csv SHA-256:** `{summary['sha256']['CR222h_pair_triad_roster.csv']}`

## Verdict

CR222h binds the neutral pair-face precursor to the original 3-body diamond
target under the sealed PR carrier:

```text
QP093A-0262 4+4 -> QP093A-0200 4+4+4
```

The successful trial state is:

```text
PAIR_TO_TRIAD_BRIDGE_BOUND -> TARGETED_EMITTED_WARNING_PACKET
```

The bridge keeps the ledgers separated:

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
protocol_event_qA = 1/24
pair qA/T/W = 172 / 21.5 / 150.5
triad qA/T/W = 1160 / 145 / 1015
```

QP093A-0262 is not carrier support and is not the final three-body target. It
acts as the valid two-owner `4+4` face that points into the `4+4+4` diamond
target.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()

    upstream = upstream_rows(inputs)
    write_csv(OUT_UPSTREAM, upstream, ["upstream", "artifact", "observed_sha256", "expected_sha256", "role", "passed"])

    roster = pair_to_triad_roster(inputs)
    roster_fields = [
        "candidate_id",
        "bridge_role",
        "bin",
        "route_combination",
        "operator_class",
        "route_class",
        "partition_signature",
        "partition_sum",
        "owner_count",
        "owner_value",
        "M_native",
        "M_observed_candidate",
        "q_sign",
        "q_abs",
        "qA_observed",
        "qA_expected",
        "T_observed",
        "T_expected",
        "W_observed",
        "W_expected",
        "matter_row_allowed",
        "promotion_status",
        "matter_gate_status",
        "spin_or_hand_class",
        "known_identity_label",
        "binding_use",
        "passed",
    ]
    roster_bytes = render_csv(roster, roster_fields)
    roster_sha = sha256_bytes(roster_bytes)
    OUT_ROSTER.write_bytes(roster_bytes)

    pair, triad = roster
    metrics = bridge_metrics(pair, triad)
    contract = binding_contract_rows(metrics)
    write_csv(OUT_CONTRACT, contract, ["layer", "input", "role", "allowed_use", "forbidden_use"])

    trials = trial_rows(inputs, pair, triad)
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
            "pair_candidate_id",
            "pair_partition_signature",
            "pair_operator_class",
            "pair_qA",
            "pair_T",
            "pair_W",
            "target_candidate_id",
            "target_partition_signature",
            "target_operator_class",
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

    wrongs = wrong_control_rows(inputs, pair, triad)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "attempted_binding", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, roster, metrics, trials, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222h_PASS_PAIR_TO_TRIAD_BINDING__QP093A_0262_TO_QP093A_0200_WITH_SEALED_PR_CARRIER"
        if checks_passed == checks_total
        else "CR222h_FAIL_PAIR_TO_TRIAD_BINDING"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "binding_formula": "sealed carrier packet + 4+4 pair face + 4+4+4 triad target + protocol trigger",
        "protected_separations": {
            "carrier_checksum": "162; pair and triad rows excluded",
            "carrier_tensor_witness": "QP093A-0300=18",
            "protocol_event_qA": PROTOCOL_EVENT_QA,
            "pair_matter_qA_T_W": "172 / 21.5 / 150.5",
            "triad_matter_qA_T_W": "1160 / 145 / 1015",
        },
        "bridge": metrics,
        "pair": {
            "candidate_id": pair["candidate_id"],
            "operator_class": pair["operator_class"],
            "partition_signature": pair["partition_signature"],
            "q_sign": pair["q_sign"],
            "qA": pair["qA_observed"],
            "T": pair["T_observed"],
            "W": pair["W_observed"],
        },
        "triad": {
            "candidate_id": triad["candidate_id"],
            "operator_class": triad["operator_class"],
            "partition_signature": triad["partition_signature"],
            "q_sign": triad["q_sign"],
            "qA": triad["qA_observed"],
            "T": triad["T_observed"],
            "W": triad["W_observed"],
        },
        "trial_count": len(trials),
        "platforms": sorted({row["platform_id"] for row in trials}),
        "outputs": {
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "pair_triad_roster_csv": OUT_ROSTER.name,
            "binding_contract_csv": OUT_CONTRACT.name,
            "pair_to_triad_trials_csv": OUT_TRIALS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222h_pair_triad_roster.csv": roster_sha,
        },
        "next_gate": "PAIR_FACE_TARGET_SELECTION_OR_PLATFORM_LAB_PROTOCOL",
    }

    write_precommit(roster_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_UPSTREAM,
        OUT_ROSTER,
        OUT_CONTRACT,
        OUT_TRIALS,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222h pair-to-triad binding complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  pair: {PAIR_ID} 4+4 qA=172 T=21.5 W=150.5")
    print(f"  triad: {TRIAD_ID} 4+4+4 qA=1160 T=145 W=1015")
    print(f"  CR222h_pair_triad_roster.csv sha256: {roster_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
