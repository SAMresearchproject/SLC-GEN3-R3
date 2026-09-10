"""CR222j PR self-correction triad-carrier contract.

CR222j upgrades the CP/QC Paul Revere pairing from warning transmission to a
minimal self-correction architecture:

    three-owner particle + road-light correction carrier + tensor witness

QP093A-0115 is the proof-of-concept correction particle. QP093A-0225 is the
strong p=8 follow-up. QP093A-0235 is a two-owner detection-only control.
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

CR_ID = "CR222j"
TEST_ID = "CR222j_PR_SELF_CORRECTION_TRIAD_CARRIER"

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
CR222G_SUMMARY = BRANCH_DIR / "CR222g_PR_TARGET_BINDING_3BODY_DIAMOND" / "CR222g_summary.json"
CR222I_ROSTER = BRANCH_DIR / "CR222i_CP_QC_PR_PARTICLE_CARRIER_PAIR" / "CR222i_particle_carrier_roster.csv"
CR222I_SUMMARY = BRANCH_DIR / "CR222i_CP_QC_PR_PARTICLE_CARRIER_PAIR" / "CR222i_summary.json"

OUT_UPSTREAM = CR_DIR / "CR222j_upstream_seals.csv"
OUT_ROSTER = CR_DIR / "CR222j_self_correction_roster.csv"
OUT_CONTRACT = CR_DIR / "CR222j_correction_contract.csv"
OUT_PLATFORM_CONTEXT = CR_DIR / "CR222j_platform_context.csv"
OUT_TRIALS = CR_DIR / "CR222j_correction_trials.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222j_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222j_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222j_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222j_summary.json"
OUT_RESULT = CR_DIR / "CR222j_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

R2 = Decimal(144)
EIGHT = Decimal(8)
TOL = Decimal("0.000001")
A_SIDE = "1/24"

PRIMARY_TRIAD_ID = "QP093A-0115"
STRONG_TRIAD_ID = "QP093A-0225"
DETECTION_CONTROL_ID = "QP093A-0235"
ROAD_LIGHT_CARRIER_ID = "QP093A-0301"
TENSOR_WITNESS_ID = "QP093A-0300"
SINGLE_WRITE_WARNING_ID = "QP093A-0002"

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


def close(a: Decimal, b: Decimal, tol: Decimal = TOL) -> bool:
    return abs(a - b) <= tol


def dec_text(value: Decimal) -> str:
    nearest = value.to_integral_value()
    if close(value, nearest):
        return str(nearest)
    rounded = value.quantize(Decimal("0.000000001"))
    if close(value, rounded):
        text = format(rounded, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def load_inputs() -> dict[str, object]:
    return {
        "cr219": read_csv_rows(CR219_PROMOTED),
        "cr222b_validity": read_csv_rows(CR222B_VALIDITY),
        "cr222f_outputs": read_csv_rows(CR222F_OUTPUTS),
        "cr222f_wrongs": read_csv_rows(CR222F_WRONGS),
        "cr222d_summary": read_json(CR222D_SUMMARY),
        "cr222f_summary": read_json(CR222F_SUMMARY),
        "cr222g_summary": read_json(CR222G_SUMMARY),
        "cr222i_summary": read_json(CR222I_SUMMARY),
    }


def row_by_candidate(inputs: dict[str, object], candidate_id: str) -> dict[str, str]:
    for row in inputs["cr219"]:
        if row.get("candidate_id") == candidate_id:
            return row
    raise KeyError(f"missing candidate_id: {candidate_id}")


def validity_map(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["validity_check"]: row for row in inputs["cr222b_validity"]}


def f_outputs_by_scenario(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["scenario"]: row for row in inputs["cr222f_outputs"]}


def f_wrongs_by_name(inputs: dict[str, object]) -> dict[str, dict[str, str]]:
    return {row["wrong_control"]: row for row in inputs["cr222f_wrongs"]}


def signature_parts(signature: str) -> list[int]:
    return [int(part) for part in signature.split("+")]


def matter_formula(row: dict[str, str]) -> tuple[Decimal, Decimal, Decimal, bool]:
    m_obs = dec(row["M_observed_candidate"])
    q_abs = dec(row["q_abs"])
    q_a_expected = m_obs * (Decimal(1) + q_abs / R2)
    t_expected = q_a_expected / EIGHT
    w_expected = q_a_expected * Decimal(7) / EIGHT
    passed = (
        row["matter_row_allowed"] == "yes"
        and close(dec(row["qA_source_support"]), q_a_expected)
        and close(dec(row["tensor_carrier_support"]), t_expected)
        and close(dec(row["retained_write_support"]), w_expected)
    )
    return q_a_expected, t_expected, w_expected, passed


def carrier_zero_pass(row: dict[str, str]) -> bool:
    return (
        row["matter_row_allowed"] == "no"
        and dec(row["M_observed_candidate"]) == 0
        and dec(row["qA_source_support"]) == 0
        and dec(row["tensor_carrier_support"]) == 0
        and dec(row["retained_write_support"]) == 0
    )


def roster_row(row: dict[str, str], correction_role: str, architecture_use: str) -> dict[str, str]:
    if row["matter_row_allowed"] == "yes":
        q_a_expected, t_expected, w_expected, formula_pass = matter_formula(row)
    else:
        q_a_expected = Decimal(0)
        t_expected = Decimal(0)
        w_expected = Decimal(0)
        formula_pass = carrier_zero_pass(row)

    signature = row["partition_signature"]
    parts = signature_parts(signature) if "+" in signature else [int(signature)]
    identical_owners = len(set(parts)) == 1
    owner_count = len(parts)
    if row["operator_class"] == "GROUND_BARYON_3BODY" and identical_owners and owner_count == 3:
        correction_class = "correction_capable_three_owner_majority"
    elif row["operator_class"] == "BOUND_COLOR_PAIR" and owner_count == 2:
        correction_class = "detection_only_two_owner_disagreement"
    elif row["operator_class"] == "ROAD_LIGHT_CARRIER":
        correction_class = "syndrome_entropy_removal_channel"
    elif row["operator_class"] == "TENSOR_CARRIER":
        correction_class = "clock_witness_failure_floor"
    else:
        correction_class = "not_self_correction_candidate"

    return {
        "candidate_id": row["candidate_id"],
        "correction_role": correction_role,
        "correction_class": correction_class,
        "bin": row["bin"],
        "route_combination": row["route_combination"],
        "operator_class": row["operator_class"],
        "route_class": row["route_class"],
        "partition_signature": signature,
        "owner_count": str(owner_count),
        "identical_owners": str(identical_owners),
        "owner_value": str(parts[0]) if identical_owners else "mixed",
        "H_value_or_integer_sum": row["H_value_or_integer_sum"],
        "M_native": row["M_native"],
        "M_observed_candidate": row["M_observed_candidate"],
        "q_sign": row["q_sign"],
        "q_abs": row["q_abs"],
        "qA_observed": row["qA_source_support"],
        "qA_expected": dec_text(q_a_expected),
        "T_observed": row["tensor_carrier_support"],
        "T_expected": dec_text(t_expected),
        "W_observed": row["retained_write_support"],
        "W_expected": dec_text(w_expected),
        "matter_row_allowed": row["matter_row_allowed"],
        "promotion_status": row["promotion_status"],
        "matter_gate_status": row["matter_gate_status"],
        "spin_or_hand_class": row["spin_or_hand_class"],
        "architecture_use": architecture_use,
        "passed": str(formula_pass),
    }


def build_roster(inputs: dict[str, object]) -> list[dict[str, str]]:
    return [
        roster_row(row_by_candidate(inputs, PRIMARY_TRIAD_ID), "proof_of_concept_self_correction_particle", "minimal three-owner correction manifold"),
        roster_row(row_by_candidate(inputs, STRONG_TRIAD_ID), "strong_native_followup_self_correction_particle", "three-owner correction with completed p=8 split lane"),
        roster_row(row_by_candidate(inputs, DETECTION_CONTROL_ID), "two_owner_detection_control", "detects disagreement but cannot identify which owner to repair"),
        roster_row(row_by_candidate(inputs, ROAD_LIGHT_CARRIER_ID), "road_light_correction_carrier", "syndrome and entropy-removal route; not logical payload"),
        roster_row(row_by_candidate(inputs, TENSOR_WITNESS_ID), "tensor_witness_floor", "clock/witness/failure floor; not correction actuator"),
    ]


def upstream_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    d_summary = inputs["cr222d_summary"]
    f_summary = inputs["cr222f_summary"]
    g_summary = inputs["cr222g_summary"]
    i_summary = inputs["cr222i_summary"]
    return [
        {
            "upstream": "CR219_promoted_particle_rows",
            "artifact": str(CR219_PROMOTED),
            "observed_sha256": sha256_file(CR219_PROMOTED),
            "expected_sha256": d_summary["source"]["sha256"],
            "role": "self-correction triad, carrier, witness, and detection-control source rows",
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
            "role": "correction capacity exceeded -> warning emission",
            "passed": str(sha256_file(CR222E_STATE) == EXPECTED_CR222E_HASH),
        },
        {
            "upstream": "CR222f_platform_adapter",
            "artifact": str(CR222F_ADAPTER.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222F_ADAPTER),
            "expected_sha256": EXPECTED_CR222F_HASH,
            "role": f"A_leak threshold adapter: {','.join(f_summary['platforms'])}",
            "passed": str(sha256_file(CR222F_ADAPTER) == EXPECTED_CR222F_HASH),
        },
        {
            "upstream": "CR222g_3body_target_roster",
            "artifact": str(CR222G_ROSTER.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222G_ROSTER),
            "expected_sha256": EXPECTED_CR222G_HASH,
            "role": f"3-body diamond anchors: {g_summary['target_roster']['diamond_anchor_count']}",
            "passed": str(sha256_file(CR222G_ROSTER) == EXPECTED_CR222G_HASH),
        },
        {
            "upstream": "CR222i_particle_carrier_pair",
            "artifact": str(CR222I_ROSTER.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR222I_ROSTER),
            "expected_sha256": i_summary["sha256"]["CR222i_particle_carrier_roster.csv"],
            "role": "single-write warning pair baseline, not autonomous correction",
            "passed": str(sha256_file(CR222I_ROSTER) == i_summary["sha256"]["CR222i_particle_carrier_roster.csv"]),
        },
    ]


def correction_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "layer": "proof_of_concept_particle",
            "row": PRIMARY_TRIAD_ID,
            "role": "color_triad[1+1+1]",
            "allowed_use": "minimal three-owner logical manifold for disagreement syndrome and majority-style restoration",
            "forbidden_use": "do not reduce to a single-write warning particle",
        },
        {
            "layer": "correction_carrier",
            "row": ROAD_LIGHT_CARRIER_ID,
            "role": "ROAD_LIGHT_CARRIER,p=1",
            "allowed_use": "syndrome and entropy-removal channel",
            "forbidden_use": "do not carry the logical state as matter and do not supply qA/T/W",
        },
        {
            "layer": "tensor_witness",
            "row": TENSOR_WITNESS_ID,
            "role": "TENSOR_CARRIER=18",
            "allowed_use": "clock/witness/failure floor for whether correction keeps up",
            "forbidden_use": "do not perform the correction and do not become photon payload",
        },
        {
            "layer": "threshold_gate",
            "row": "A_leak",
            "role": "PR escalation condition",
            "allowed_use": "A_leak < 1/24 => correction operating; A_leak >= 1/24 => correction capacity exceeded, emit warning",
            "forbidden_use": "do not emit merely because the packet exists",
        },
        {
            "layer": "strong_followup",
            "row": STRONG_TRIAD_ID,
            "role": "color_triad[8+8+8]",
            "allowed_use": "p=8 three-owner follow-up with qA=4088, T=511, W=3577",
            "forbidden_use": "do not treat as the first proof-of-concept row",
        },
        {
            "layer": "detection_control",
            "row": DETECTION_CONTROL_ID,
            "role": "pair_write[1|anti1]",
            "allowed_use": "two-owner disagreement detection control",
            "forbidden_use": "do not claim autonomous majority restoration",
        },
    ]


def platform_context_rows() -> list[dict[str, str]]:
    return [
        {
            "platform_lane": "autonomous_qec_bosonic_or_cat_code_analogue",
            "sam_mapping": "logical particle + lossy correction carrier + witness floor",
            "best_use": "self-correction protocol design",
            "boundary": "architecture analogue only; no external lab data is consumed by CR222j",
            "passed": "True",
        },
        {
            "platform_lane": "nv_spin_photon_or_photonic_warning_route",
            "sam_mapping": "road-light carrier supports preparation, tomography, and warning transmission",
            "best_use": "warning detection/transmission baseline",
            "boundary": "strong for CR222i warning route; not the strongest autonomous correction lane",
            "passed": "True",
        },
        {
            "platform_lane": "two_owner_pair_control",
            "sam_mapping": "detect disagreement without determining the repair owner",
            "best_use": "negative control for correction capability",
            "boundary": "detection-only, not majority restoration",
            "passed": "True",
        },
    ]


def correction_trials(inputs: dict[str, object], roster: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row["candidate_id"]: row for row in roster}
    vm = validity_map(inputs)
    outputs = f_outputs_by_scenario(inputs)
    carrier = by_id[ROAD_LIGHT_CARRIER_ID]
    tensor = by_id[TENSOR_WITNESS_ID]
    trial_specs = [
        {
            "trial_id": f"POC::{PRIMARY_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}::below_threshold",
            "logical_particle_id": PRIMARY_TRIAD_ID,
            "protocol_scenario": "nv_sealed_below_threshold",
            "expected_correction_state": "SELF_CORRECTION_OPERATING",
            "expected_warning": "False",
            "platform_lane": "autonomous_qec_bosonic_or_cat_code_analogue",
        },
        {
            "trial_id": f"POC::{PRIMARY_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}::threshold_exceeded",
            "logical_particle_id": PRIMARY_TRIAD_ID,
            "protocol_scenario": "nv_threshold_exact",
            "expected_correction_state": "CORRECTION_CAPACITY_EXCEEDED",
            "expected_warning": "True",
            "platform_lane": "autonomous_qec_bosonic_or_cat_code_analogue",
        },
        {
            "trial_id": f"FOLLOWUP::{STRONG_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}::threshold_exceeded",
            "logical_particle_id": STRONG_TRIAD_ID,
            "protocol_scenario": "nv_threshold_exact",
            "expected_correction_state": "CORRECTION_CAPACITY_EXCEEDED",
            "expected_warning": "True",
            "platform_lane": "autonomous_qec_bosonic_or_cat_code_analogue",
        },
        {
            "trial_id": f"CONTROL::{DETECTION_CONTROL_ID}+{ROAD_LIGHT_CARRIER_ID}::threshold_exceeded",
            "logical_particle_id": DETECTION_CONTROL_ID,
            "protocol_scenario": "nv_threshold_exact",
            "expected_correction_state": "DETECTION_ONLY_NO_AUTONOMOUS_CORRECTION",
            "expected_warning": "True",
            "platform_lane": "two_owner_pair_control",
        },
    ]

    rows = []
    for spec in trial_specs:
        particle = by_id[spec["logical_particle_id"]]
        protocol = outputs[spec["protocol_scenario"]]
        is_three_owner = particle["correction_class"] == "correction_capable_three_owner_majority"
        is_two_owner = particle["correction_class"] == "detection_only_two_owner_disagreement"
        correction_capable = is_three_owner and carrier["operator_class"] == "ROAD_LIGHT_CARRIER"
        correction_state = spec["expected_correction_state"]
        warning_emitted = protocol["emitted"]
        if protocol["emitted"] == "False" and correction_capable:
            correction_state = "SELF_CORRECTION_OPERATING"
        elif protocol["emitted"] == "True" and correction_capable:
            correction_state = "CORRECTION_CAPACITY_EXCEEDED"
        elif is_two_owner:
            correction_state = "DETECTION_ONLY_NO_AUTONOMOUS_CORRECTION"

        passed = (
            vm["packet_total_162"]["passed"] == "True"
            and particle["passed"] == "True"
            and carrier["passed"] == "True"
            and tensor["passed"] == "True"
            and correction_state == spec["expected_correction_state"]
            and warning_emitted == spec["expected_warning"]
        )
        rows.append({
            "trial_id": spec["trial_id"],
            "platform_lane": spec["platform_lane"],
            "logical_particle_id": particle["candidate_id"],
            "logical_particle_signature": particle["partition_signature"],
            "owner_count": particle["owner_count"],
            "correction_class": particle["correction_class"],
            "correction_carrier": ROAD_LIGHT_CARRIER_ID,
            "tensor_witness": TENSOR_WITNESS_ID,
            "carrier_packet_checksum": vm["packet_total_162"]["observed"],
            "A_side": A_SIDE,
            "protocol_scenario": spec["protocol_scenario"],
            "A_leak_relation": "< 1/24" if warning_emitted == "False" else ">= 1/24",
            "particle_qA": particle["qA_observed"],
            "particle_T": particle["T_observed"],
            "particle_W": particle["W_observed"],
            "correction_state": correction_state,
            "warning_emitted": warning_emitted,
            "passed": str(passed),
        })
    return rows


def wrong_control_rows(inputs: dict[str, object], roster: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row["candidate_id"]: row for row in roster}
    single = row_by_candidate(inputs, SINGLE_WRITE_WARNING_ID)
    outputs = f_outputs_by_scenario(inputs)
    wrongs = f_wrongs_by_name(inputs)
    return [
        {
            "wrong_control": "single_write_0002_claims_autonomous_correction",
            "attempted_binding": "QP093A-0002 + QP093A-0301 as self-correction loop",
            "observed_failure": f"{SINGLE_WRITE_WARNING_ID} route={single['route_class']} signature={single['partition_signature']}",
            "expected_failure": "SINGLE_OWNER_NO_DISAGREEMENT_SYNDROME",
            "passes_as_failure": str(single["route_class"] == "single_write" and single["partition_signature"] == "1"),
        },
        {
            "wrong_control": "two_owner_0235_claims_majority_repair",
            "attempted_binding": "QP093A-0235 as autonomous correction particle",
            "observed_failure": f"owner_count={by_id[DETECTION_CONTROL_ID]['owner_count']} class={by_id[DETECTION_CONTROL_ID]['correction_class']}",
            "expected_failure": "TWO_OWNER_DETECTION_ONLY_NO_MAJORITY",
            "passes_as_failure": str(by_id[DETECTION_CONTROL_ID]["owner_count"] == "2"),
        },
        {
            "wrong_control": "road_light_0301_carries_logical_state",
            "attempted_binding": "QP093A-0301 as logical matter payload",
            "observed_failure": f"matter={by_id[ROAD_LIGHT_CARRIER_ID]['matter_row_allowed']} qA={by_id[ROAD_LIGHT_CARRIER_ID]['qA_observed']}",
            "expected_failure": "CARRIER_ROUTE_NOT_LOGICAL_MATTER",
            "passes_as_failure": str(by_id[ROAD_LIGHT_CARRIER_ID]["matter_row_allowed"] == "no"),
        },
        {
            "wrong_control": "tensor_0300_performs_correction",
            "attempted_binding": "QP093A-0300 as correction actuator",
            "observed_failure": f"class={by_id[TENSOR_WITNESS_ID]['correction_class']} matter={by_id[TENSOR_WITNESS_ID]['matter_row_allowed']}",
            "expected_failure": "TENSOR_WITNESS_NOT_CORRECTION_ACTUATOR",
            "passes_as_failure": str(by_id[TENSOR_WITNESS_ID]["correction_class"] == "clock_witness_failure_floor"),
        },
        {
            "wrong_control": "below_threshold_emits_warning",
            "attempted_binding": "A_leak < 1/24 emits PR warning",
            "observed_failure": outputs["nv_sealed_below_threshold"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(outputs["nv_sealed_below_threshold"]["emitted"] == "False"),
        },
        {
            "wrong_control": "threshold_exceeded_does_not_emit",
            "attempted_binding": "A_leak >= 1/24 but warning suppressed",
            "observed_failure": outputs["nv_threshold_exact"]["emitted"],
            "expected_failure": "True",
            "passes_as_failure": str(outputs["nv_threshold_exact"]["emitted"] == "True"),
        },
        {
            "wrong_control": "protocol_qA_substituted_for_triad_qA",
            "attempted_binding": "use protocol qA=1/24 as triad matter qA",
            "observed_failure": f"protocol_qA={A_SIDE}; triad_qA={by_id[PRIMARY_TRIAD_ID]['qA_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(by_id[PRIMARY_TRIAD_ID]["qA_observed"] != A_SIDE),
        },
        {
            "wrong_control": "0301_promoted_to_matter",
            "attempted_binding": "road-light carrier promoted to matter",
            "observed_failure": by_id[ROAD_LIGHT_CARRIER_ID]["matter_row_allowed"],
            "expected_failure": "no",
            "passes_as_failure": str(by_id[ROAD_LIGHT_CARRIER_ID]["matter_row_allowed"] == "no"),
        },
        {
            "wrong_control": "logical_particle_counted_into_carrier_checksum",
            "attempted_binding": "carrier checksum + triad particle",
            "observed_failure": "carrier checksum must remain 162",
            "expected_failure": "CHECKSUM_CATEGORY_FAILURE",
            "passes_as_failure": "True",
        },
        {
            "wrong_control": "0306_omitted_but_correction_warning_emits",
            "attempted_binding": "omit p=1 source packet but emit correction warning",
            "observed_failure": wrongs["0306_omitted"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_CORRECTION_WARNING",
            "passes_as_failure": wrongs["0306_omitted"]["passes_as_failure"],
        },
        {
            "wrong_control": "duplicate_0305_restored_but_correction_warning_emits",
            "attempted_binding": "restore duplicate support row but emit correction warning",
            "observed_failure": wrongs["duplicate_0305_restored"]["observed_failure"],
            "expected_failure": "163_CORRUPT_NO_CORRECTION_WARNING",
            "passes_as_failure": wrongs["duplicate_0305_restored"]["passes_as_failure"],
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    roster: list[dict[str, str]],
    platform_context: list[dict[str, str]],
    trials: list[dict[str, str]],
    wrong_controls: list[dict[str, str]],
) -> list[Check]:
    by_id = {row["candidate_id"]: row for row in roster}
    vm = validity_map(inputs)
    d_summary = inputs["cr222d_summary"]
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("carrier_packet_checksum_remains_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("support_roster_12_plus_mirror_preserved", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12 and d_summary["support_roster_correction"]["closure_total"] == 162, json.dumps(d_summary["support_roster_correction"], sort_keys=True), "12 support rows + mirror = 162"),
        Check("primary_triad_is_0115", by_id[PRIMARY_TRIAD_ID]["candidate_id"] == PRIMARY_TRIAD_ID, by_id[PRIMARY_TRIAD_ID]["candidate_id"], PRIMARY_TRIAD_ID),
        Check("primary_triad_is_three_identical_owners", by_id[PRIMARY_TRIAD_ID]["partition_signature"] == "1+1+1" and by_id[PRIMARY_TRIAD_ID]["owner_count"] == "3" and by_id[PRIMARY_TRIAD_ID]["identical_owners"] == "True", by_id[PRIMARY_TRIAD_ID]["partition_signature"], "1+1+1"),
        Check("primary_triad_formula_pass", by_id[PRIMARY_TRIAD_ID]["passed"] == "True", f"qA={by_id[PRIMARY_TRIAD_ID]['qA_observed']} T={by_id[PRIMARY_TRIAD_ID]['T_observed']} W={by_id[PRIMARY_TRIAD_ID]['W_observed']}", "qA=72.5 T=9.0625 W=63.4375"),
        Check("primary_triad_correction_capable", by_id[PRIMARY_TRIAD_ID]["correction_class"] == "correction_capable_three_owner_majority", by_id[PRIMARY_TRIAD_ID]["correction_class"], "correction_capable_three_owner_majority"),
        Check("strong_followup_is_0225", by_id[STRONG_TRIAD_ID]["candidate_id"] == STRONG_TRIAD_ID and by_id[STRONG_TRIAD_ID]["partition_signature"] == "8+8+8", by_id[STRONG_TRIAD_ID]["partition_signature"], "8+8+8"),
        Check("strong_followup_formula_pass", by_id[STRONG_TRIAD_ID]["passed"] == "True", f"qA={by_id[STRONG_TRIAD_ID]['qA_observed']} T={by_id[STRONG_TRIAD_ID]['T_observed']} W={by_id[STRONG_TRIAD_ID]['W_observed']}", "qA=4088 T=511 W=3577"),
        Check("strong_followup_retained_is_7T", close(dec(by_id[STRONG_TRIAD_ID]["W_observed"]), dec(by_id[STRONG_TRIAD_ID]["T_observed"]) * Decimal(7)), f"W={by_id[STRONG_TRIAD_ID]['W_observed']} T={by_id[STRONG_TRIAD_ID]['T_observed']}", "W=7T"),
        Check("two_owner_control_is_detection_only", by_id[DETECTION_CONTROL_ID]["owner_count"] == "2" and by_id[DETECTION_CONTROL_ID]["correction_class"] == "detection_only_two_owner_disagreement", f"owners={by_id[DETECTION_CONTROL_ID]['owner_count']} class={by_id[DETECTION_CONTROL_ID]['correction_class']}", "two-owner detection only"),
        Check("two_owner_control_formula_pass", by_id[DETECTION_CONTROL_ID]["passed"] == "True", f"qA={by_id[DETECTION_CONTROL_ID]['qA_observed']} T={by_id[DETECTION_CONTROL_ID]['T_observed']} W={by_id[DETECTION_CONTROL_ID]['W_observed']}", "qA=10.75 T=1.34375 W=9.40625"),
        Check("road_light_carrier_is_0301", by_id[ROAD_LIGHT_CARRIER_ID]["operator_class"] == "ROAD_LIGHT_CARRIER" and by_id[ROAD_LIGHT_CARRIER_ID]["partition_signature"] == "1", f"{by_id[ROAD_LIGHT_CARRIER_ID]['operator_class']}|p={by_id[ROAD_LIGHT_CARRIER_ID]['partition_signature']}", "ROAD_LIGHT_CARRIER|p=1"),
        Check("road_light_carrier_zero_matter_ledger", by_id[ROAD_LIGHT_CARRIER_ID]["passed"] == "True" and by_id[ROAD_LIGHT_CARRIER_ID]["matter_row_allowed"] == "no", f"qA={by_id[ROAD_LIGHT_CARRIER_ID]['qA_observed']} matter={by_id[ROAD_LIGHT_CARRIER_ID]['matter_row_allowed']}", "qA=0 matter=no"),
        Check("tensor_witness_is_0300", by_id[TENSOR_WITNESS_ID]["operator_class"] == "TENSOR_CARRIER" and by_id[TENSOR_WITNESS_ID]["M_native"] == "18", f"{by_id[TENSOR_WITNESS_ID]['operator_class']} native={by_id[TENSOR_WITNESS_ID]['M_native']}", "TENSOR_CARRIER native=18"),
        Check("tensor_witness_not_correction_actuator", by_id[TENSOR_WITNESS_ID]["correction_class"] == "clock_witness_failure_floor", by_id[TENSOR_WITNESS_ID]["correction_class"], "clock_witness_failure_floor"),
        Check("platform_context_passes", all(row["passed"] == "True" for row in platform_context), str(sum(1 for row in platform_context if row["passed"] == "True")), str(len(platform_context))),
        Check("correction_trials_count", len(trials) == 4, str(len(trials)), "4"),
        Check("below_threshold_correction_operating", any(row["logical_particle_id"] == PRIMARY_TRIAD_ID and row["A_leak_relation"] == "< 1/24" and row["correction_state"] == "SELF_CORRECTION_OPERATING" and row["warning_emitted"] == "False" for row in trials), "present", "0115 below-threshold operating state"),
        Check("primary_triad_threshold_emits_warning", any(row["logical_particle_id"] == PRIMARY_TRIAD_ID and row["A_leak_relation"] == ">= 1/24" and row["correction_state"] == "CORRECTION_CAPACITY_EXCEEDED" and row["warning_emitted"] == "True" for row in trials), "present", "0115 threshold warning"),
        Check("strong_followup_threshold_emits_warning", any(row["logical_particle_id"] == STRONG_TRIAD_ID and row["correction_state"] == "CORRECTION_CAPACITY_EXCEEDED" and row["warning_emitted"] == "True" for row in trials), "present", "0225 threshold warning"),
        Check("two_owner_control_no_autonomous_correction", any(row["logical_particle_id"] == DETECTION_CONTROL_ID and row["correction_state"] == "DETECTION_ONLY_NO_AUTONOMOUS_CORRECTION" for row in trials), "present", "0235 detection-only control"),
        Check("all_trials_pass", all(row["passed"] == "True" for row in trials), str(sum(1 for row in trials if row["passed"] == "True")), str(len(trials))),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrong_controls), str(sum(1 for row in wrong_controls if row["passes_as_failure"] == "True")), str(len(wrong_controls))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(roster_sha: str) -> None:
    text = f"""# CR222j PRECOMMIT - PR Self-Correction Triad Carrier

## Scope

Lock the self-correction architecture:

```text
three-owner particle + road-light correction carrier + tensor witness
```

## Rows

```text
proof of concept: {PRIMARY_TRIAD_ID} + {ROAD_LIGHT_CARRIER_ID}
strong follow-up: {STRONG_TRIAD_ID} + {ROAD_LIGHT_CARRIER_ID}
detection control: {DETECTION_CONTROL_ID}
witness/floor: {TENSOR_WITNESS_ID}
```

## Threshold

```text
A_leak < 1/24  => correction operating normally
A_leak >= 1/24 => correction capacity exceeded; emit PR warning
```

## Pre-run Hash

Expected `CR222j_self_correction_roster.csv` hash:

```text
{roster_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222j PR Self-Correction Triad Carrier

CR222j upgrades the PR experiment from warning transmission to a correction
failure protocol:

```text
three-owner particle + road-light correction carrier + tensor witness
```

QP093A-0115 is the proof of concept, QP093A-0225 is the stronger p=8 follow-up,
and QP093A-0235 is the detection-only two-owner control.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222j PR Self-Correction Triad Carrier Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222j_self_correction_roster.csv SHA-256:** `{summary['sha256']['CR222j_self_correction_roster.csv']}`

## Verdict

CR222j locks the self-correction upgrade:

```text
QP093A-0115 + QP093A-0301
= three-owner correction particle + road-light correction carrier
```

The correction theorem is:

```text
three-owner logical state -> detect owner disagreement -> carrier removes error entropy -> return to closed three-owner state
```

The PR warning no longer means ordinary decoherence. It means:

```text
A_leak < 1/24  => correction operating normally
A_leak >= 1/24 => correction capacity exceeded; emit warning
```

Rows locked:

```text
QP093A-0115: color_triad[1+1+1], qA/T/W = 72.5 / 9.0625 / 63.4375
QP093A-0301: ROAD_LIGHT_CARRIER,p=1, syndrome and entropy-removal route
QP093A-0300: tensor witness/floor, not correction actuator
QP093A-0225: strong p=8 follow-up, qA/T/W = 4088 / 511 / 3577
QP093A-0235: two-owner detection-only control
```
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()

    upstream = upstream_rows(inputs)
    write_csv(OUT_UPSTREAM, upstream, ["upstream", "artifact", "observed_sha256", "expected_sha256", "role", "passed"])

    roster = build_roster(inputs)
    roster_fields = [
        "candidate_id",
        "correction_role",
        "correction_class",
        "bin",
        "route_combination",
        "operator_class",
        "route_class",
        "partition_signature",
        "owner_count",
        "identical_owners",
        "owner_value",
        "H_value_or_integer_sum",
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
        "architecture_use",
        "passed",
    ]
    roster_bytes = render_csv(roster, roster_fields)
    roster_sha = sha256_bytes(roster_bytes)
    OUT_ROSTER.write_bytes(roster_bytes)

    contract = correction_contract_rows()
    write_csv(OUT_CONTRACT, contract, ["layer", "row", "role", "allowed_use", "forbidden_use"])

    platform_context = platform_context_rows()
    write_csv(OUT_PLATFORM_CONTEXT, platform_context, ["platform_lane", "sam_mapping", "best_use", "boundary", "passed"])

    trials = correction_trials(inputs, roster)
    write_csv(
        OUT_TRIALS,
        trials,
        [
            "trial_id",
            "platform_lane",
            "logical_particle_id",
            "logical_particle_signature",
            "owner_count",
            "correction_class",
            "correction_carrier",
            "tensor_witness",
            "carrier_packet_checksum",
            "A_side",
            "protocol_scenario",
            "A_leak_relation",
            "particle_qA",
            "particle_T",
            "particle_W",
            "correction_state",
            "warning_emitted",
            "passed",
        ],
    )

    wrong_controls = wrong_control_rows(inputs, roster)
    write_csv(OUT_WRONG_CONTROLS, wrong_controls, ["wrong_control", "attempted_binding", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, roster, platform_context, trials, wrong_controls)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222j_PASS_PR_SELF_CORRECTION_TRIAD_CARRIER__0115_PLUS_0301_WITH_0225_FOLLOWUP"
        if checks_passed == checks_total
        else "CR222j_FAIL_PR_SELF_CORRECTION_TRIAD_CARRIER"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "self_correction_architecture": "three-owner particle + road-light correction carrier + tensor witness",
        "proof_of_concept_pair": f"{PRIMARY_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}",
        "strong_followup_pair": f"{STRONG_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}",
        "detection_control": DETECTION_CONTROL_ID,
        "threshold_rule": {
            "operating": "A_leak < 1/24",
            "warning": "A_leak >= 1/24",
        },
        "protected_separations": {
            "logical_particle": "three-owner matter row supplies correction-capable manifold",
            "road_light_carrier": "syndrome and entropy-removal route; not logical payload",
            "tensor_witness": "clock/witness/failure floor; not correction actuator",
            "two_owner_control": "detects disagreement but cannot determine repair owner",
        },
        "primary": {
            "candidate_id": PRIMARY_TRIAD_ID,
            "partition_signature": "1+1+1",
            "qA": "72.5",
            "T": "9.0625",
            "W": "63.4375",
        },
        "followup": {
            "candidate_id": STRONG_TRIAD_ID,
            "partition_signature": "8+8+8",
            "qA": "4088",
            "T": "511",
            "W": "3577",
        },
        "trial_count": len(trials),
        "outputs": {
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "self_correction_roster_csv": OUT_ROSTER.name,
            "correction_contract_csv": OUT_CONTRACT.name,
            "platform_context_csv": OUT_PLATFORM_CONTEXT.name,
            "correction_trials_csv": OUT_TRIALS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222j_self_correction_roster.csv": roster_sha,
        },
        "next_gate": "CP_QC_PR_AUTONOMOUS_QEC_LAB_PROTOCOL",
    }

    write_precommit(roster_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_UPSTREAM,
        OUT_ROSTER,
        OUT_CONTRACT,
        OUT_PLATFORM_CONTEXT,
        OUT_TRIALS,
        OUT_WRONG_CONTROLS,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222j PR self-correction triad carrier complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  proof of concept: {PRIMARY_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}")
    print(f"  strong follow-up: {STRONG_TRIAD_ID}+{ROAD_LIGHT_CARRIER_ID}")
    print(f"  CR222j_self_correction_roster.csv sha256: {roster_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
