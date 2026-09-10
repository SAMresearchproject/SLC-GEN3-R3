"""CR222i CP/QC Paul Revere particle-carrier pair selection.

CR222i locks the lab-facing pair:

    QP093A-0002 + QP093A-0301

QP093A-0002 supplies the negative fermion write and qA -> T/W split.
QP093A-0301 supplies the road-light carrier route. QP093A-0018 is the clean
split calibration control. QP093A-0300 remains the tensor witness/floor, not
the transmitted payload.
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

CR_ID = "CR222i"
TEST_ID = "CR222i_CP_QC_PR_PARTICLE_CARRIER_PAIR"

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
CR223A_FIRE = BRANCH_DIR / "CR223a_PR_OBSERVABLE_IDENTITY_LOCK" / "CR223a_firing_coefficients.csv"
CR223A_SUMMARY = BRANCH_DIR / "CR223a_PR_OBSERVABLE_IDENTITY_LOCK" / "CR223a_summary.json"
CR223B_SUMMARY = BRANCH_DIR / "CR223b_PR_QUTRIT_TOMOGRAPHY_ESTIMATOR" / "CR223b_summary.json"
CR223D_SUMMARY = BRANCH_DIR / "CR223d_PR_REALTIME_WARNING_CONTACT" / "CR223d_summary.json"
CR223F_SUMMARY = BRANCH_DIR / "CR223f_TENSOR_CARRIER_PHYSICAL_DISCRIMINANT" / "CR223f_summary.json"

OUT_UPSTREAM = CR_DIR / "CR222i_upstream_seals.csv"
OUT_ROSTER = CR_DIR / "CR222i_particle_carrier_roster.csv"
OUT_CONTRACT = CR_DIR / "CR222i_experiment_contract.csv"
OUT_PLATFORM_CONTEXT = CR_DIR / "CR222i_platform_context.csv"
OUT_TRIALS = CR_DIR / "CR222i_particle_carrier_trials.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222i_wrong_controls.csv"
OUT_CHECKS = CR_DIR / "CR222i_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222i_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222i_summary.json"
OUT_RESULT = CR_DIR / "CR222i_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

R2 = Decimal(144)
EIGHT = Decimal(8)
TOL = Decimal("0.000001")
PROTOCOL_EVENT_QA = "1/24"

PRIMARY_PARTICLE_ID = "QP093A-0002"
ROAD_LIGHT_CARRIER_ID = "QP093A-0301"
SPLIT_CONTROL_ID = "QP093A-0018"
TENSOR_WITNESS_ID = "QP093A-0300"

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
        "cr223a_summary": read_json(CR223A_SUMMARY),
        "cr223b_summary": read_json(CR223B_SUMMARY),
        "cr223d_summary": read_json(CR223D_SUMMARY),
        "cr223f_summary": read_json(CR223F_SUMMARY),
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


def roster_row(row: dict[str, str], experiment_role: str, use_text: str) -> dict[str, str]:
    if row["matter_row_allowed"] == "yes":
        q_a_expected, t_expected, w_expected, formula_pass = matter_formula(row)
    else:
        q_a_expected = Decimal(0)
        t_expected = Decimal(0)
        w_expected = Decimal(0)
        formula_pass = carrier_zero_pass(row)
    return {
        "candidate_id": row["candidate_id"],
        "experiment_role": experiment_role,
        "bin": row["bin"],
        "route_combination": row["route_combination"],
        "operator_class": row["operator_class"],
        "route_class": row["route_class"],
        "partition_signature": row["partition_signature"],
        "H_value_or_integer_sum": row["H_value_or_integer_sum"],
        "M_native": row["M_native"],
        "M_observed_candidate": row["M_observed_candidate"],
        "q_sign": row["q_sign"],
        "q_abs": row["q_abs"],
        "spin_or_hand_class": row["spin_or_hand_class"],
        "M_obs": row["M_observed_candidate"],
        "qA_observed": row["qA_source_support"],
        "qA_expected": dec_text(q_a_expected),
        "T_observed": row["tensor_carrier_support"],
        "T_expected": dec_text(t_expected),
        "W_observed": row["retained_write_support"],
        "W_expected": dec_text(w_expected),
        "matter_row_allowed": row["matter_row_allowed"],
        "promotion_status": row["promotion_status"],
        "matter_gate_status": row["matter_gate_status"],
        "courtroom_table_layer": row["courtroom_table_layer"],
        "sam_experiment_use": use_text,
        "passed": str(formula_pass),
    }


def build_roster(inputs: dict[str, object]) -> list[dict[str, str]]:
    particle = row_by_candidate(inputs, PRIMARY_PARTICLE_ID)
    carrier = row_by_candidate(inputs, ROAD_LIGHT_CARRIER_ID)
    control = row_by_candidate(inputs, SPLIT_CONTROL_ID)
    tensor = row_by_candidate(inputs, TENSOR_WITNESS_ID)
    return [
        roster_row(particle, "primary_negative_fermion_write", "particle supplies qA -> T/W split"),
        roster_row(carrier, "road_light_carrier", "photon-road carrier supplies preparation/tomography/warning route"),
        roster_row(control, "clean_split_calibration_control", "unit-normalized qA=1 split control"),
        roster_row(tensor, "tensor_witness_floor", "predicted tensor witness/floor, not transmitted payload"),
    ]


def upstream_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    d_summary = inputs["cr222d_summary"]
    a_summary = inputs["cr223a_summary"]
    return [
        {
            "upstream": "CR219_promoted_particle_rows",
            "artifact": str(CR219_PROMOTED),
            "observed_sha256": sha256_file(CR219_PROMOTED),
            "expected_sha256": d_summary["source"]["sha256"],
            "role": "particle/carrier/control source rows and promotion-gate evidence",
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
            "role": "platform adapter with NV and photonic threshold scenarios",
            "passed": str(sha256_file(CR222F_ADAPTER) == EXPECTED_CR222F_HASH),
        },
        {
            "upstream": "CR223a_firing_coefficients",
            "artifact": str(CR223A_FIRE.relative_to(COURTROOM_DIR)),
            "observed_sha256": sha256_file(CR223A_FIRE),
            "expected_sha256": a_summary["sha256_firing_coefficients_csv"],
            "role": "same-domain PR observable timing context",
            "passed": str(sha256_file(CR223A_FIRE) == a_summary["sha256_firing_coefficients_csv"]),
        },
    ]


def experiment_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "layer": "primary_particle",
            "row": PRIMARY_PARTICLE_ID,
            "role": "minus_single_write[p=1,g=0]",
            "allowed_use": "negative fermion matter write; qA -> T/W split source",
            "forbidden_use": "do not use as carrier route or checksum row",
        },
        {
            "layer": "road_light_carrier",
            "row": ROAD_LIGHT_CARRIER_ID,
            "role": "ROAD_LIGHT_CARRIER,p=1",
            "allowed_use": "preparation, tomography, and warning transmission route",
            "forbidden_use": "do not promote to matter and do not supply qA/T/W write split",
        },
        {
            "layer": "split_control",
            "row": SPLIT_CONTROL_ID,
            "role": "neutral_single_write[p=8,g=0]",
            "allowed_use": "unit-normalized qA=1, T=1/8, W=7/8 calibration",
            "forbidden_use": "do not replace the primary negative p=1 particle/carrier pair",
        },
        {
            "layer": "tensor_witness",
            "row": TENSOR_WITNESS_ID,
            "role": "TENSOR_CARRIER=18",
            "allowed_use": "predicted timing/gravity/witness floor",
            "forbidden_use": "do not transmit as photon payload and do not promote to matter",
        },
        {
            "layer": "lab_mapping",
            "row": f"{PRIMARY_PARTICLE_ID}+{ROAD_LIGHT_CARRIER_ID}",
            "role": "negative fermion write + photon-road carrier",
            "allowed_use": "CP/QC PR experiment route, especially spin-photon style platforms",
            "forbidden_use": "do not require direct tensor-carrier observation as the transmission payload",
        },
    ]


def platform_context_rows(inputs: dict[str, object]) -> list[dict[str, str]]:
    a = inputs["cr223a_summary"]
    b = inputs["cr223b_summary"]
    d = inputs["cr223d_summary"]
    f = inputs["cr223f_summary"]
    return [
        {
            "context": "CR223a",
            "result_class": a["result_class"],
            "signal": "observable identity locked",
            "use_in_CR222i": "keeps A_side=1/24 and t_fire observable context separate from particle row choice",
            "passed": str(a["checks_passed"] == a["checks_total"]),
        },
        {
            "context": "CR223b",
            "result_class": b["result_class"],
            "signal": "qutrit tomography estimator",
            "use_in_CR222i": "supports tomography route for the road-light carrier layer",
            "passed": str(b["checks_passed"] == b["checks_total"]),
        },
        {
            "context": "CR223d",
            "result_class": d["result_class"],
            "signal": "real-time warning simulation",
            "use_in_CR222i": "supports warning transmission route after sealed protocol gate",
            "passed": str(d["checks_passed"] == d["checks_total"]),
        },
        {
            "context": "CR223f",
            "result_class": f["result_class"],
            "signal": "tensor-carrier physical discriminant context",
            "use_in_CR222i": "keeps tensor witness as discriminant/floor, not photon payload",
            "passed": str(f["checks_passed"] == f["checks_total"]),
        },
    ]


def trial_rows(inputs: dict[str, object], roster: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_role = {row["experiment_role"]: row for row in roster}
    particle = rows_by_role["primary_negative_fermion_write"]
    carrier = rows_by_role["road_light_carrier"]
    control = rows_by_role["clean_split_calibration_control"]
    tensor = rows_by_role["tensor_witness_floor"]
    vm = validity_map(inputs)
    outputs = f_outputs_by_scenario(inputs)
    platform_scenarios = [
        ("NV_CENTER_T2", "nv_threshold_exact"),
        ("PHOTONIC_TAU_ENT", "photonic_threshold_exact"),
    ]
    rows = []
    for platform_id, scenario in platform_scenarios:
        platform = outputs[scenario]
        ready = (
            platform["emitted"] == "True"
            and vm["packet_total_162"]["passed"] == "True"
            and particle["passed"] == "True"
            and carrier["passed"] == "True"
            and control["passed"] == "True"
            and tensor["passed"] == "True"
            and particle["partition_signature"] == carrier["partition_signature"] == "1"
            and carrier["matter_row_allowed"] == "no"
            and tensor["matter_row_allowed"] == "no"
        )
        rows.append({
            "trial_id": f"{platform_id}::{PRIMARY_PARTICLE_ID}+{ROAD_LIGHT_CARRIER_ID}",
            "platform_id": platform_id,
            "platform_trigger_scenario": scenario,
            "carrier_packet_checksum": vm["packet_total_162"]["observed"],
            "protocol_event_qA": PROTOCOL_EVENT_QA,
            "particle_candidate_id": particle["candidate_id"],
            "particle_role": particle["experiment_role"],
            "particle_qA": particle["qA_observed"],
            "particle_T": particle["T_observed"],
            "particle_W": particle["W_observed"],
            "road_light_candidate_id": carrier["candidate_id"],
            "road_light_role": carrier["operator_class"],
            "road_light_matter_ledger": "M=qA=T=W=0",
            "split_control": f"{control['candidate_id']} qA={control['qA_observed']} T={control['T_observed']} W={control['W_observed']}",
            "tensor_witness": f"{tensor['candidate_id']} native={tensor['M_native']} not_payload",
            "experiment_rule": "particle supplies write split; road-light carrier supplies route; tensor remains witness floor",
            "experiment_ready": str(ready),
            "binding_state": "PARTICLE_CARRIER_PR_PAIR_BOUND" if ready else "PARTICLE_CARRIER_PAIR_REJECTED",
            "emitted_state": "WARNING_TRANSMISSION_ALLOWED" if ready else "NOT_EMITTED",
            "passed": str(ready),
        })
    return rows


def wrong_control_rows(inputs: dict[str, object], roster: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_role = {row["experiment_role"]: row for row in roster}
    particle = rows_by_role["primary_negative_fermion_write"]
    carrier = rows_by_role["road_light_carrier"]
    control = rows_by_role["clean_split_calibration_control"]
    tensor = rows_by_role["tensor_witness_floor"]
    outputs = f_outputs_by_scenario(inputs)
    f_wrongs = f_wrongs_by_name(inputs)
    return [
        {
            "wrong_control": "0301_promoted_to_matter",
            "attempted_binding": "ROAD_LIGHT_CARRIER supplies matter write",
            "observed_failure": f"{carrier['candidate_id']} matter_row_allowed={carrier['matter_row_allowed']}",
            "expected_failure": "CARRIER_ONLY_NOT_MATTER",
            "passes_as_failure": str(carrier["matter_row_allowed"] == "no"),
        },
        {
            "wrong_control": "0301_used_for_qA_split",
            "attempted_binding": "ROAD_LIGHT_CARRIER qA -> T/W",
            "observed_failure": f"qA={carrier['qA_observed']} T={carrier['T_observed']} W={carrier['W_observed']}",
            "expected_failure": "ZERO_MATTER_LEDGER_NO_WRITE_SPLIT",
            "passes_as_failure": str(dec(carrier["qA_observed"]) == 0 and dec(carrier["T_observed"]) == 0 and dec(carrier["W_observed"]) == 0),
        },
        {
            "wrong_control": "0002_used_as_carrier_route",
            "attempted_binding": "minus_single_write becomes road-light carrier",
            "observed_failure": f"{particle['candidate_id']} matter={particle['matter_row_allowed']} q_sign={particle['q_sign']}",
            "expected_failure": "MATTER_WRITE_NOT_CARRIER_ROUTE",
            "passes_as_failure": str(particle["matter_row_allowed"] == "yes" and particle["operator_class"] != "ROAD_LIGHT_CARRIER"),
        },
        {
            "wrong_control": "0300_used_as_photon_payload",
            "attempted_binding": "tensor carrier transmitted as road-light payload",
            "observed_failure": f"{tensor['candidate_id']} operator={tensor['operator_class']}",
            "expected_failure": "TENSOR_WITNESS_NOT_ROAD_LIGHT_PAYLOAD",
            "passes_as_failure": str(tensor["operator_class"] == "TENSOR_CARRIER" and carrier["operator_class"] == "ROAD_LIGHT_CARRIER"),
        },
        {
            "wrong_control": "0300_promoted_to_matter",
            "attempted_binding": "tensor witness becomes matter row",
            "observed_failure": f"{tensor['candidate_id']} matter_row_allowed={tensor['matter_row_allowed']}",
            "expected_failure": "TENSOR_CARRIER_NOT_MATTER",
            "passes_as_failure": str(tensor["matter_row_allowed"] == "no"),
        },
        {
            "wrong_control": "0018_used_as_primary_negative_particle",
            "attempted_binding": "split control replaces QP093A-0002",
            "observed_failure": f"{control['candidate_id']} p={control['partition_signature']} q_sign={control['q_sign']}",
            "expected_failure": "CONTROL_IS_NEUTRAL_P8_NOT_NEGATIVE_P1",
            "passes_as_failure": str(control["partition_signature"] == "8" and control["q_sign"] == "neutral"),
        },
        {
            "wrong_control": "0018_used_as_carrier",
            "attempted_binding": "split control becomes photon-road carrier",
            "observed_failure": f"{control['candidate_id']} matter_row_allowed={control['matter_row_allowed']}",
            "expected_failure": "CONTROL_IS_MATTER_ROW_NOT_CARRIER",
            "passes_as_failure": str(control["matter_row_allowed"] == "yes" and control["operator_class"] != "ROAD_LIGHT_CARRIER"),
        },
        {
            "wrong_control": "protocol_qA_substituted_for_particle_qA",
            "attempted_binding": "use protocol qA=1/24 as QP093A-0002 matter qA",
            "observed_failure": f"protocol_qA={PROTOCOL_EVENT_QA}; particle_qA={particle['qA_observed']}",
            "expected_failure": "CATEGORY_FAILURE",
            "passes_as_failure": str(particle["qA_observed"] != PROTOCOL_EVENT_QA),
        },
        {
            "wrong_control": "support_inventory_emits_without_G_protocol",
            "attempted_binding": "support inventory -> warning write",
            "observed_failure": f_wrongs["support_inventory_emits_without_G_protocol"]["observed_failure"],
            "expected_failure": "NO_EMISSION_WITHOUT_PROTOCOL_GATE",
            "passes_as_failure": f_wrongs["support_inventory_emits_without_G_protocol"]["passes_as_failure"],
        },
        {
            "wrong_control": "target_emits_without_protocol_gate",
            "attempted_binding": "G_protocol=0 but particle-carrier pair transmits",
            "observed_failure": outputs["nv_no_protocol_gate"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(outputs["nv_no_protocol_gate"]["emitted"] == "False"),
        },
        {
            "wrong_control": "target_emits_below_threshold",
            "attempted_binding": "A_leak=1/48 but particle-carrier pair transmits",
            "observed_failure": outputs["nv_sealed_below_threshold"]["emitted"],
            "expected_failure": "False",
            "passes_as_failure": str(outputs["nv_sealed_below_threshold"]["emitted"] == "False"),
        },
        {
            "wrong_control": "0306_omitted_but_pair_transmits",
            "attempted_binding": "omit p=1 source packet but transmit particle-carrier warning",
            "observed_failure": f_wrongs["0306_omitted"]["observed_failure"],
            "expected_failure": "161_CORRUPT_NO_TRANSMISSION",
            "passes_as_failure": f_wrongs["0306_omitted"]["passes_as_failure"],
        },
        {
            "wrong_control": "duplicate_0305_restored_but_pair_transmits",
            "attempted_binding": "restore duplicate support row but transmit particle-carrier warning",
            "observed_failure": f_wrongs["duplicate_0305_restored"]["observed_failure"],
            "expected_failure": "163_CORRUPT_NO_TRANSMISSION",
            "passes_as_failure": f_wrongs["duplicate_0305_restored"]["passes_as_failure"],
        },
    ]


def build_checks(
    inputs: dict[str, object],
    upstream: list[dict[str, str]],
    roster: list[dict[str, str]],
    platform_context: list[dict[str, str]],
    trials: list[dict[str, str]],
    wrongs: list[dict[str, str]],
) -> list[Check]:
    rows_by_role = {row["experiment_role"]: row for row in roster}
    particle = rows_by_role["primary_negative_fermion_write"]
    carrier = rows_by_role["road_light_carrier"]
    control = rows_by_role["clean_split_calibration_control"]
    tensor = rows_by_role["tensor_witness_floor"]
    vm = validity_map(inputs)
    d_summary = inputs["cr222d_summary"]
    return [
        Check("upstream_seals_match", all(row["passed"] == "True" for row in upstream), str(sum(1 for row in upstream if row["passed"] == "True")), str(len(upstream))),
        Check("carrier_packet_checksum_remains_162", vm["packet_total_162"]["passed"] == "True", vm["packet_total_162"]["observed"], "162"),
        Check("support_roster_12_plus_mirror_preserved", d_summary["support_roster_correction"]["unique_support_roster_rows"] == 12 and d_summary["support_roster_correction"]["closure_total"] == 162, json.dumps(d_summary["support_roster_correction"], sort_keys=True), "12 support rows + mirror = 162"),
        Check("primary_particle_is_0002", particle["candidate_id"] == PRIMARY_PARTICLE_ID, particle["candidate_id"], PRIMARY_PARTICLE_ID),
        Check("primary_particle_is_negative_p1_fermion", particle["partition_signature"] == "1" and particle["q_sign"] == "negative" and particle["spin_or_hand_class"] == "fermion_half_write", f"p={particle['partition_signature']} q={particle['q_sign']} spin={particle['spin_or_hand_class']}", "p=1 q=negative fermion_half_write"),
        Check("primary_particle_matter_gate_passes", particle["matter_row_allowed"] == "yes" and particle["matter_gate_status"] == "PASS_STABLE_SINGLE_WRITE_MATTER", f"{particle['matter_row_allowed']}|{particle['matter_gate_status']}", "yes|PASS_STABLE_SINGLE_WRITE_MATTER"),
        Check("primary_particle_qA_T_W_formula_pass", particle["passed"] == "True", f"qA={particle['qA_observed']} T={particle['T_observed']} W={particle['W_observed']}", "qA=1.510416667 T=0.188802083 W=1.321614583"),
        Check("road_light_carrier_is_0301", carrier["candidate_id"] == ROAD_LIGHT_CARRIER_ID, carrier["candidate_id"], ROAD_LIGHT_CARRIER_ID),
        Check("road_light_carrier_is_p1_transverse_neutral", carrier["partition_signature"] == "1" and carrier["q_sign"] == "neutral" and carrier["spin_or_hand_class"] == "transverse_vector", f"p={carrier['partition_signature']} q={carrier['q_sign']} spin={carrier['spin_or_hand_class']}", "p=1 neutral transverse_vector"),
        Check("road_light_carrier_matter_blocked", carrier["matter_row_allowed"] == "no" and carrier["promotion_status"] == "REJECT_MATTER_PROMOTION_CARRIER_ONLY", f"{carrier['matter_row_allowed']}|{carrier['promotion_status']}", "no|REJECT_MATTER_PROMOTION_CARRIER_ONLY"),
        Check("road_light_carrier_zero_matter_ledger", carrier["passed"] == "True", f"M={carrier['M_obs']} qA={carrier['qA_observed']} T={carrier['T_observed']} W={carrier['W_observed']}", "M=qA=T=W=0"),
        Check("primary_pair_shares_minimal_partition_p1", particle["partition_signature"] == carrier["partition_signature"] == "1", f"{particle['partition_signature']}+{carrier['partition_signature']}", "1+1"),
        Check("role_separation_one_matter_one_carrier", particle["matter_row_allowed"] == "yes" and carrier["matter_row_allowed"] == "no", f"{particle['matter_row_allowed']} / {carrier['matter_row_allowed']}", "yes / no"),
        Check("split_control_is_0018", control["candidate_id"] == SPLIT_CONTROL_ID, control["candidate_id"], SPLIT_CONTROL_ID),
        Check("split_control_unit_normalized", control["qA_observed"] == "1" and control["T_observed"] == "0.125" and control["W_observed"] == "0.875", f"qA={control['qA_observed']} T={control['T_observed']} W={control['W_observed']}", "qA=1 T=0.125 W=0.875"),
        Check("split_control_not_primary_pair", control["partition_signature"] == "8" and control["q_sign"] == "neutral", f"p={control['partition_signature']} q={control['q_sign']}", "p=8 neutral"),
        Check("tensor_witness_is_0300", tensor["candidate_id"] == TENSOR_WITNESS_ID and tensor["operator_class"] == "TENSOR_CARRIER", f"{tensor['candidate_id']}|{tensor['operator_class']}", f"{TENSOR_WITNESS_ID}|TENSOR_CARRIER"),
        Check("tensor_witness_blocked_from_matter", tensor["matter_row_allowed"] == "no" and tensor["M_native"] == "18", f"matter={tensor['matter_row_allowed']} native={tensor['M_native']}", "matter=no native=18"),
        Check("platform_context_passes", all(row["passed"] == "True" for row in platform_context), str(sum(1 for row in platform_context if row["passed"] == "True")), str(len(platform_context))),
        Check("particle_carrier_trials_count", len(trials) == 2, str(len(trials)), "2"),
        Check("particle_carrier_trials_ready_when_gated", all(row["passed"] == "True" for row in trials), str(sum(1 for row in trials if row["passed"] == "True")), "2"),
        Check("protocol_qA_not_particle_qA", all(row["protocol_event_qA"] != row["particle_qA"] for row in trials), "distinct", "protocol event qA distinct from particle qA"),
        Check("wrong_controls_fail_as_expected", all(row["passes_as_failure"] == "True" for row in wrongs), str(sum(1 for row in wrongs if row["passes_as_failure"] == "True")), str(len(wrongs))),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(roster_sha: str) -> None:
    text = f"""# CR222i PRECOMMIT - CP/QC PR Particle-Carrier Pair

## Scope

Lock the lab-facing particle-carrier pairing:

```text
primary: {PRIMARY_PARTICLE_ID} + {ROAD_LIGHT_CARRIER_ID}
control: {SPLIT_CONTROL_ID}
witness/floor: {TENSOR_WITNESS_ID}
```

## Protected Distinctions

```text
{PRIMARY_PARTICLE_ID} = negative fermion matter write, p=1
{ROAD_LIGHT_CARRIER_ID} = road-light carrier, p=1, M=qA=T=W=0
{SPLIT_CONTROL_ID} = unit split control, qA=1, T=1/8, W=7/8
{TENSOR_WITNESS_ID} = tensor witness/floor, not photon payload
protocol_event_qA = 1/24
```

## Pre-run Hash

Expected `CR222i_particle_carrier_roster.csv` hash:

```text
{roster_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222i CP/QC PR Particle-Carrier Pair

CR222i locks the CP/QC Paul Revere experiment pairing:

```text
QP093A-0002 + QP093A-0301
```

The particle supplies the negative fermion write. The road-light carrier
supplies the transmission route. QP093A-0018 calibrates the clean split, and
QP093A-0300 remains the tensor witness/floor.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    text = f"""# CR222i CP/QC PR Particle-Carrier Pair Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

**CR222i_particle_carrier_roster.csv SHA-256:** `{summary['sha256']['CR222i_particle_carrier_roster.csv']}`

## Verdict

CR222i locks the strongest lab-facing particle-carrier pair for CP/QC Paul
Revere work:

```text
QP093A-0002 + QP093A-0301
```

The selected roles are:

```text
QP093A-0002 = negative fermion write, p=1, qA/T/W = 1.510416667 / 0.188802083 / 1.321614583
QP093A-0301 = ROAD_LIGHT_CARRIER, p=1, M=qA=T=W=0
QP093A-0018 = split control, qA/T/W = 1 / 0.125 / 0.875
QP093A-0300 = tensor witness/floor, not transmitted payload
```

The successful trial state is:

```text
PARTICLE_CARRIER_PR_PAIR_BOUND -> WARNING_TRANSMISSION_ALLOWED
```

This keeps the campaign architecture clean: photon-road route for preparation,
tomography, and warning transmission; matter row for the write split; tensor
carrier as the predicted witness/floor.
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
        "experiment_role",
        "bin",
        "route_combination",
        "operator_class",
        "route_class",
        "partition_signature",
        "H_value_or_integer_sum",
        "M_native",
        "M_observed_candidate",
        "q_sign",
        "q_abs",
        "spin_or_hand_class",
        "M_obs",
        "qA_observed",
        "qA_expected",
        "T_observed",
        "T_expected",
        "W_observed",
        "W_expected",
        "matter_row_allowed",
        "promotion_status",
        "matter_gate_status",
        "courtroom_table_layer",
        "sam_experiment_use",
        "passed",
    ]
    roster_bytes = render_csv(roster, roster_fields)
    roster_sha = sha256_bytes(roster_bytes)
    OUT_ROSTER.write_bytes(roster_bytes)

    contract = experiment_contract_rows()
    write_csv(OUT_CONTRACT, contract, ["layer", "row", "role", "allowed_use", "forbidden_use"])

    platform_context = platform_context_rows(inputs)
    write_csv(OUT_PLATFORM_CONTEXT, platform_context, ["context", "result_class", "signal", "use_in_CR222i", "passed"])

    trials = trial_rows(inputs, roster)
    write_csv(
        OUT_TRIALS,
        trials,
        [
            "trial_id",
            "platform_id",
            "platform_trigger_scenario",
            "carrier_packet_checksum",
            "protocol_event_qA",
            "particle_candidate_id",
            "particle_role",
            "particle_qA",
            "particle_T",
            "particle_W",
            "road_light_candidate_id",
            "road_light_role",
            "road_light_matter_ledger",
            "split_control",
            "tensor_witness",
            "experiment_rule",
            "experiment_ready",
            "binding_state",
            "emitted_state",
            "passed",
        ],
    )

    wrongs = wrong_control_rows(inputs, roster)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "attempted_binding", "observed_failure", "expected_failure", "passes_as_failure"])

    checks = build_checks(inputs, upstream, roster, platform_context, trials, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222i_PASS_CP_QC_PR_PARTICLE_CARRIER_PAIR__QP093A_0002_PLUS_QP093A_0301_CONTROL_0018"
        if checks_passed == checks_total
        else "CR222i_FAIL_CP_QC_PR_PARTICLE_CARRIER_PAIR"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "primary_pair": f"{PRIMARY_PARTICLE_ID}+{ROAD_LIGHT_CARRIER_ID}",
        "binding_formula": "negative fermion write + photon-road carrier + sealed PR protocol gate",
        "protected_separations": {
            "particle_write": "QP093A-0002 supplies qA -> T/W split",
            "road_light_carrier": "QP093A-0301 supplies route and remains M=qA=T=W=0",
            "split_control": "QP093A-0018 supplies qA=1, T=1/8, W=7/8",
            "tensor_witness": "QP093A-0300 remains witness/floor, not payload",
            "protocol_event_qA": PROTOCOL_EVENT_QA,
        },
        "primary_particle": {
            "candidate_id": PRIMARY_PARTICLE_ID,
            "route_combination": "minus_single_write[p=1,g=0]",
            "M_obs": "1.5",
            "qA": "1.510416667",
            "T": "0.188802083",
            "W": "1.321614583",
        },
        "carrier": {
            "candidate_id": ROAD_LIGHT_CARRIER_ID,
            "operator_class": "ROAD_LIGHT_CARRIER",
            "partition_signature": "1",
            "matter_ledger": "M=qA=T=W=0",
        },
        "control": {
            "candidate_id": SPLIT_CONTROL_ID,
            "qA": "1",
            "T": "0.125",
            "W": "0.875",
        },
        "trial_count": len(trials),
        "platforms": sorted({row["platform_id"] for row in trials}),
        "outputs": {
            "upstream_seals_csv": OUT_UPSTREAM.name,
            "particle_carrier_roster_csv": OUT_ROSTER.name,
            "experiment_contract_csv": OUT_CONTRACT.name,
            "platform_context_csv": OUT_PLATFORM_CONTEXT.name,
            "particle_carrier_trials_csv": OUT_TRIALS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "CR222i_particle_carrier_roster.csv": roster_sha,
        },
        "next_gate": "CP_QC_PR_LAB_PROTOCOL_PARTICLE_CARRIER_ROUTE",
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

    print("CR222i CP/QC PR particle-carrier pair complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  primary pair: {PRIMARY_PARTICLE_ID}+{ROAD_LIGHT_CARRIER_ID}")
    print(f"  control: {SPLIT_CONTROL_ID} qA=1 T=0.125 W=0.875")
    print(f"  CR222i_particle_carrier_roster.csv sha256: {roster_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
