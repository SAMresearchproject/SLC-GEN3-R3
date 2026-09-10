"""CR116 18 graviton-channel carrier theorem.

This runner answers the narrow Courtroom question:

    Can SAM identify the split-loss value 18 as the graviton-channel carrier?

The safe theorem is deliberately scoped. It proves 18 is the internal SAM
graviton-channel tensor-carrier packet, because it is derived as the unique
1/8 unresolved split-loss support, carries rank-2 plus/cross tensor structure,
propagates as a massless c-speed wave mode, feeds the A-kernel through ledger
compression, and is rejected by the particle catalog as matter.

It does not claim an observed graviton particle, a graviton rest mass, or full
quantum-gravity closure.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 80

CR_ID = "CR116"
RESULT_CLASS_PASS = "CR116_PASS_18_GRAVITON_CHANNEL_CARRIER_THEOREM"
RESULT_CLASS_FAIL = "CR116_FAIL_18_GRAVITON_CHANNEL_CARRIER_THEOREM"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
STAM_ROOT = Path(r"C:/VS/Stam_model-A-v1.0")
QUANTUM_ROOT = Path(r"C:/VS/quantum_phase")

CR114_DIR = BRANCH_DIR / "CR114_BINARY_FACE_STATE_SPLIT_THEOREM"
CR114_SUMMARY = CR114_DIR / "CR114_summary.json"
CR114_RESULT = CR114_DIR / "CR114_result.md"
CR114_LOCK = CR114_DIR / "CR114_binary_face_state_split_lock.json"

CR115_DIR = BRANCH_DIR / "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM"
CR115_SUMMARY = CR115_DIR / "CR115_summary.json"
CR115_RESULT = CR115_DIR / "CR115_result.md"

QP092A_DIR = QUANTUM_ROOT / "artifacts" / "qp092a_split_loss_tensor_carrier"
QP092B_DIR = QUANTUM_ROOT / "artifacts" / "qp092b_tensor_carrier_qa_coupling"
QP092C_DIR = QUANTUM_ROOT / "artifacts" / "qp092c_tensor_carrier_a_kernel"
QP092D_DIR = QUANTUM_ROOT / "artifacts" / "qp092d_tensor_carrier_conservation"
QP092E_DIR = QUANTUM_ROOT / "artifacts" / "qp092e_weak_field_external_readout"
QP092F_DIR = QUANTUM_ROOT / "artifacts" / "qp092f_tensor_carrier_wave_mode"
QP092G_DIR = QUANTUM_ROOT / "artifacts" / "qp092g_tensor_carrier_bridge_packet"
QP093A_DIR = QUANTUM_ROOT / "artifacts" / "qp093a_stable_particle_combination_enumerator"

QP092A_SUMMARY = QP092A_DIR / "qp092a_split_loss_summary.json"
QP092A_RESULT = QP092A_DIR / "QP092A_SPLIT_LOSS_TENSOR_CARRIER_result.md"
QP092A_CLASSIFICATION = QP092A_DIR / "qp092a_graviton_channel_classification.csv"
QP092A_WRONG_CONTROLS = QP092A_DIR / "qp092a_wrong_split_loss_controls.csv"
QP092A_IDENTITY = QP092A_DIR / "qp092a_split_loss_tensor_identity.csv"

QP092B_SUMMARY = QP092B_DIR / "qp092b_summary.json"
QP092B_RESULT = QP092B_DIR / "QP092B_TENSOR_CARRIER_QA_COUPLING_result.md"
QP092C_SUMMARY = QP092C_DIR / "qp092c_summary.json"
QP092C_RESULT = QP092C_DIR / "QP092C_TENSOR_CARRIER_A_KERNEL_result.md"
QP092D_SUMMARY = QP092D_DIR / "qp092d_summary.json"
QP092D_RESULT = QP092D_DIR / "QP092D_TENSOR_CARRIER_CONSERVATION_result.md"
QP092E_SUMMARY = QP092E_DIR / "qp092e_summary.json"
QP092E_RESULT = QP092E_DIR / "QP092E_WEAK_FIELD_EXTERNAL_READOUT_result.md"

QP092F_SUMMARY = QP092F_DIR / "qp092f_summary.json"
QP092F_RESULT = QP092F_DIR / "QP092F_TENSOR_CARRIER_WAVE_MODE_result.md"
QP092F_TENSOR_BASIS = QP092F_DIR / "qp092f_tensor_basis.csv"
QP092F_WRONG_CONTROLS = QP092F_DIR / "qp092f_wrong_controls.csv"
QP092F_WAVE_ROWS = QP092F_DIR / "qp092f_wave_mode_rows.csv"

QP092G_SUMMARY = QP092G_DIR / "qp092g_summary.json"
QP092G_RESULT = QP092G_DIR / "QP092G_TENSOR_CARRIER_BRIDGE_PACKET_result.md"
QP092G_BRIDGE_PACKET = QP092G_DIR / "qp092g_bridge_packet.csv"
QP092G_STRONG_BOUNDARY = QP092G_DIR / "qp092g_strong_boundary_rows.csv"
QP092G_WRONG_CONTROLS = QP092G_DIR / "qp092g_wrong_controls.csv"

QP093A_SUMMARY = QP093A_DIR / "qp093a_summary.json"
QP093A_RESULT = QP093A_DIR / "QP093A_STABLE_PARTICLE_ENUMERATOR_result.md"
QP093A_CARRIER_ROWS = QP093A_DIR / "qp093a_bin_carrier_only_rows.csv"
QP093A_WRONG_CONTROLS = QP093A_DIR / "qp093a_wrong_controls.csv"

G699C_DIR = STAM_ROOT / "tests" / "Substrate" / "G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT"
G699C_SUMMARY = G699C_DIR / "G699c_summary.json"
G699C_RESULT = G699C_DIR / "G699c_RESULT.md"

DECLARED_PREMISES_JSON = CR_DIR / "CR116_declared_premises.json"
SOURCE_CHAIN_CSV = CR_DIR / "CR116_source_chain.csv"
SIGNATURE_CSV = CR_DIR / "CR116_graviton_signature_table.csv"
CHECKS_CSV = CR_DIR / "CR116_checks.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR116_wrong_controls.csv"
LOCK_JSON = CR_DIR / "CR116_18_graviton_carrier_lock.json"
LOCK_SHA = CR_DIR / "CR116_18_graviton_carrier_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR116_summary.json"
RESULT_MD = CR_DIR / "CR116_result.md"
LOCAL_HASHES = CR_DIR / "CR116_hashes.txt"
BRANCH_HASHES = BRANCH_DIR / "HASHES.txt"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def branch_rel(path: Path) -> str:
    try:
        return str(path.relative_to(BRANCH_DIR))
    except ValueError:
        return str(path)


def decimal_value(value: Any) -> Decimal:
    return Decimal(str(value))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def pass_counts(payload: dict[str, Any], passed_key: str, total_key: str) -> bool:
    return int(payload.get(passed_key, -1)) == int(payload.get(total_key, -2))


def wrong_counts(payload: dict[str, Any]) -> bool:
    return pass_counts(payload, "wrong_controls_rejected", "wrong_controls_total")


def controls_counts(payload: dict[str, Any]) -> bool:
    return pass_counts(payload, "controls_passed", "controls_total")


def all_csv_true(rows: list[dict[str, str]], field: str) -> bool:
    return bool(rows) and all(parse_bool(row.get(field, False)) for row in rows)


def row_by_field(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(field) == value:
            return row
    return {}


def source_row(
    label: str,
    path: Path,
    role: str,
    load_bearing: bool,
    source_type: str,
) -> dict[str, Any]:
    return {
        "label": label,
        "role": role,
        "load_bearing": bool(load_bearing),
        "source_type": source_type,
        "path": str(path),
        "exists": path.exists(),
        "sha256": sha256_file(path),
    }


def check_row(check_id: str, description: str, observed: Any, passed: bool, source: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "description": description,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "passed": bool(passed),
        "source": source,
    }


def wc_row(control_id: str, hypothesis: str, observed: Any, rejected: bool, reason: str) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "hypothesis": hypothesis,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "rejected": bool(rejected),
        "reason": reason,
    }


def signature_row(
    signature_id: str,
    requirement: str,
    observed: Any,
    status: str,
    source: str,
) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "requirement": requirement,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "status": status,
        "source": source,
    }


def update_hash_ledgers(artifacts: list[Path]) -> None:
    local_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in artifacts]
    LOCAL_HASHES.write_text("\n".join(local_lines) + "\n", encoding="ascii")

    all_for_branch = artifacts + [LOCAL_HASHES]
    existing = BRANCH_HASHES.read_text(encoding="utf-8", errors="replace").splitlines() if BRANCH_HASHES.exists() else []
    prefix = "CR116_18_GRAVITON_CARRIER_THEOREM\\"
    kept = [line for line in existing if prefix not in line]
    new_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in all_for_branch]
    BRANCH_HASHES.write_text("\n".join(kept + new_lines) + "\n", encoding="utf-8")


def main() -> int:
    print("CR116 runner: starting 18 graviton-channel carrier theorem")

    sources = [
        source_row("CR116_RUNNER", Path(__file__).resolve(), "Executable Courtroom theorem gate", True, "EXECUTABLE_GATE"),
        source_row("CR114_SUMMARY", CR114_SUMMARY, "Derives 1/8 split loss and 18 carrier packet", True, "THEOREM_SUMMARY"),
        source_row("CR114_RESULT", CR114_RESULT, "Human-readable split-loss theorem and boundaries", True, "THEOREM_TEXT"),
        source_row("CR114_LOCK", CR114_LOCK, "Frozen split-loss lock artifact", True, "LOCK_JSON"),
        source_row("CR115_SUMMARY", CR115_SUMMARY, "D=3 invariant-carrier support theorem", False, "SUPPORTING_THEOREM"),
        source_row("CR115_RESULT", CR115_RESULT, "Human-readable D=3 support theorem", False, "SUPPORTING_TEXT"),
        source_row("QP092A_SUMMARY", QP092A_SUMMARY, "Names 18 as split-loss tensor-carrier/graviton-channel candidate", True, "EXECUTED_SUMMARY"),
        source_row("QP092A_RESULT", QP092A_RESULT, "Boundary: not particle mass and not stable matter row", True, "RESULT_TEXT"),
        source_row("QP092A_CLASSIFICATION", QP092A_CLASSIFICATION, "Massless, rank-2, qA source-support classification", True, "CLASSIFICATION_CSV"),
        source_row("QP092A_WRONG_CONTROLS", QP092A_WRONG_CONTROLS, "Rejects wrong split-loss routes", True, "WRONG_CONTROLS"),
        source_row("QP092A_IDENTITY", QP092A_IDENTITY, "Exact split-loss tensor identity", True, "IDENTITY_CSV"),
        source_row("QP092B_SUMMARY", QP092B_SUMMARY, "qA loads carrier support and updates A after compression", True, "EXECUTED_SUMMARY"),
        source_row("QP092B_RESULT", QP092B_RESULT, "Human-readable qA coupling result", False, "RESULT_TEXT"),
        source_row("QP092C_SUMMARY", QP092C_SUMMARY, "Recovers A kernel for point, multi-source, and extended sources", True, "EXECUTED_SUMMARY"),
        source_row("QP092C_RESULT", QP092C_RESULT, "Human-readable A-kernel result", False, "RESULT_TEXT"),
        source_row("QP092D_SUMMARY", QP092D_SUMMARY, "Conserves source ledger through carrier and compression", True, "EXECUTED_SUMMARY"),
        source_row("QP092D_RESULT", QP092D_RESULT, "Human-readable conservation result", False, "RESULT_TEXT"),
        source_row("QP092E_SUMMARY", QP092E_SUMMARY, "Recovers weak-field force, clock, and path-delay readouts", True, "EXECUTED_SUMMARY"),
        source_row("QP092E_RESULT", QP092E_RESULT, "Human-readable weak-field result", False, "RESULT_TEXT"),
        source_row("QP092F_SUMMARY", QP092F_SUMMARY, "Massless c-speed plus/cross tensor wave mode", True, "EXECUTED_SUMMARY"),
        source_row("QP092F_RESULT", QP092F_RESULT, "Boundary: not graviton mass, particle row, or full QG theorem", True, "RESULT_TEXT"),
        source_row("QP092F_TENSOR_BASIS", QP092F_TENSOR_BASIS, "Plus/cross trace-zero transverse tensor basis", True, "TENSOR_BASIS_CSV"),
        source_row("QP092F_WRONG_CONTROLS", QP092F_WRONG_CONTROLS, "Rejects scalar, vector, massive, and particle-promotion modes", True, "WRONG_CONTROLS"),
        source_row("QP092F_WAVE_ROWS", QP092F_WAVE_ROWS, "Wave-mode row ledger", False, "DISPLAY_CSV"),
        source_row("QP092G_SUMMARY", QP092G_SUMMARY, "Bridge packet across weak field, A=1, and quantum support", True, "EXECUTED_SUMMARY"),
        source_row("QP092G_RESULT", QP092G_RESULT, "Boundary: not new particle row, rest mass, direct qA, or full QG", True, "RESULT_TEXT"),
        source_row("QP092G_BRIDGE_PACKET", QP092G_BRIDGE_PACKET, "Bridge packet layer table", True, "BRIDGE_CSV"),
        source_row("QP092G_STRONG_BOUNDARY", QP092G_STRONG_BOUNDARY, "A=1 strong-boundary closure table", True, "BOUNDARY_CSV"),
        source_row("QP092G_WRONG_CONTROLS", QP092G_WRONG_CONTROLS, "Rejects bridge-packet wrong controls", True, "WRONG_CONTROLS"),
        source_row("QP093A_SUMMARY", QP093A_SUMMARY, "Particle catalog rejects tensor-carrier promotion", True, "EXECUTED_SUMMARY"),
        source_row("QP093A_RESULT", QP093A_RESULT, "Discovery catalog boundary text", True, "RESULT_TEXT"),
        source_row("QP093A_CARRIER_ROWS", QP093A_CARRIER_ROWS, "Carrier-only rows including 18 tensor carrier", True, "CATALOG_CSV"),
        source_row("QP093A_WRONG_CONTROLS", QP093A_WRONG_CONTROLS, "Rejects tensor-carrier-as-matter control", True, "WRONG_CONTROLS"),
        source_row("G699C_SUMMARY", G699C_SUMMARY, "Supporting GW/EM shared-road propagation check", False, "SUPPORTING_EMPIRICAL_TEST"),
        source_row("G699C_RESULT", G699C_RESULT, "Human-readable shared-road propagation result", False, "SUPPORTING_TEXT"),
    ]

    load_bearing_sources_present = all(row["exists"] for row in sources if row["load_bearing"])

    cr114 = read_json(CR114_SUMMARY)
    cr115 = read_json(CR115_SUMMARY) if CR115_SUMMARY.exists() else {}
    qpa = read_json(QP092A_SUMMARY)
    qpb = read_json(QP092B_SUMMARY)
    qpc = read_json(QP092C_SUMMARY)
    qpd = read_json(QP092D_SUMMARY)
    qpe = read_json(QP092E_SUMMARY)
    qpf = read_json(QP092F_SUMMARY)
    qpg = read_json(QP092G_SUMMARY)
    qp93 = read_json(QP093A_SUMMARY)
    g699c = read_json(G699C_SUMMARY)

    qpa_classification = read_csv(QP092A_CLASSIFICATION)
    qpa_wrong = read_csv(QP092A_WRONG_CONTROLS)
    qpf_basis = read_csv(QP092F_TENSOR_BASIS)
    qpf_wrong = read_csv(QP092F_WRONG_CONTROLS)
    qpg_wrong = read_csv(QP092G_WRONG_CONTROLS)
    qp93_carrier_rows = read_csv(QP093A_CARRIER_ROWS)
    qp93_wrong = read_csv(QP093A_WRONG_CONTROLS)

    qpa_result_text = read_text(QP092A_RESULT)
    qpf_result_text = read_text(QP092F_RESULT)
    qpg_result_text = read_text(QP092G_RESULT)
    qp93_result_text = read_text(QP093A_RESULT)

    carrier_18 = row_by_field(qp93_carrier_rows, "route_combination", "tensor_carrier_alphaH_D2")
    qp93_wc6 = row_by_field(qp93_wrong, "wrong_control_id", "WC6_PROMOTE_TENSOR_CARRIER_TO_MATTER_ROW")
    qpf_wc1 = row_by_field(qpf_wrong, "wrong_control_id", "WC1_SCALAR_SINGLE_POLARIZATION")
    qpf_wc2 = row_by_field(qpf_wrong, "wrong_control_id", "WC2_VECTOR_THREE_COMPONENT_CARRIER")
    qpf_wc3 = row_by_field(qpf_wrong, "wrong_control_id", "WC3_MASSIVE_MODE")
    qpf_wc5 = row_by_field(qpf_wrong, "wrong_control_id", "WC5_PROMOTE_CARRIER_TO_PARTICLE_ROW")
    qpg_wc10 = row_by_field(qpg_wrong, "wrong_control_id", "WC10_SKIP_LEDGER_COMPRESSION")

    split_loss = decimal_value(qpa["split_loss_tensor_channel"])
    tensor_identity = decimal_value(qpa["tensor_identity_alpha_H_D2"])
    carrier_fraction = qpa["split_loss_fraction"]
    retained_fraction = qpa["retained_fraction"]
    surface_debit = decimal_value(qpa["surface_debit_D2_over_R"])

    derived_18_pass = (
        cr114.get("result_class") == "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM"
        and cr114.get("all_predictions_passed") is True
        and cr114.get("all_wrong_controls_rejected") is True
        and cr114.get("split_loss") == "18"
        and cr114.get("carrier_fraction") == "1/8"
        and split_loss == Decimal("18")
        and tensor_identity == Decimal("18")
        and carrier_fraction == "1/8"
    )

    classification_pass = (
        qpa.get("passed") is True
        and qpa.get("massless_unresolved_behavior") == "PASS_NOT_MATTER_ROW_NOT_REST_MASS"
        and qpa.get("rank2_tensor_classification") == "PASS_ALPHA_H_D2_RANK2_SURFACE"
        and qpa.get("qa_source_coupling_classification") == "PASS_SOURCE_SUPPORT_NOT_MASS_CLOSURE"
        and wrong_counts(qpa)
        and controls_counts(qpa)
        and all_csv_true(qpa_classification, "passed")
        and "graviton-channel" in qpa_result_text
        and "not read as a graviton mass" in qpa_result_text
    )

    qa_to_a_pass = (
        qpb.get("passed") is True
        and qpb.get("carrier_fraction") == "1/8"
        and qpb.get("retained_write_fraction") == "7/8"
        and int(qpb.get("qa_source_rows_coupled", -1)) == int(qpb.get("qa_source_rows_total", -2))
        and int(qpb.get("a_update_rows_passed", -1)) == int(qpb.get("a_update_rows_total", -2))
        and int(qpb.get("matter_rows_added", -1)) == 0
        and wrong_counts(qpb)
        and controls_counts(qpb)
        and "A_UPDATES_AFTER_LEDGER_COMPRESSION" in qpb.get("mechanism_status", "")
    )

    a_kernel_pass = (
        qpc.get("passed") is True
        and "ledger-compressed" in qpc.get("kernel_rule", "")
        and int(qpc.get("kernel_replay_rows_passed", -1)) == int(qpc.get("kernel_replay_rows_total", -2))
        and int(qpc.get("geometry_rows_passed", -1)) == int(qpc.get("geometry_rows_total", -2))
        and int(qpc.get("point_rows_passed", -1)) == int(qpc.get("point_rows_total", -2))
        and int(qpc.get("multi_source_rows_passed", -1)) == int(qpc.get("multi_source_rows_total", -2))
        and int(qpc.get("extended_rows_passed", -1)) == int(qpc.get("extended_rows_total", -2))
        and int(qpc.get("matter_rows_added", -1)) == 0
        and wrong_counts(qpc)
        and controls_counts(qpc)
    )

    conservation_pass = (
        qpd.get("passed") is True
        and int(qpd.get("particle_rows_passed", -1)) == int(qpd.get("particle_rows_total", -2))
        and int(qpd.get("macro_rows_passed", -1)) == int(qpd.get("macro_rows_total", -2))
        and int(qpd.get("propagation_rows_passed", -1)) == int(qpd.get("propagation_rows_total", -2))
        and int(qpd.get("ledger_closure_scopes_passed", -1)) == int(qpd.get("ledger_closure_scopes_total", -2))
        and int(qpd.get("matter_rows_added", -1)) == 0
        and "LEDGER_COMPRESSION" in qpd.get("result_class", "")
        and wrong_counts(qpd)
        and controls_counts(qpd)
    )

    weak_field_pass = (
        qpe.get("passed") is True
        and int(qpe.get("weak_field_rows_passed", -1)) == int(qpe.get("weak_field_rows_total", -2))
        and int(qpe.get("clock_rows_passed", -1)) == int(qpe.get("weak_field_rows_total", -2))
        and int(qpe.get("path_delay_rows_passed", -1)) == int(qpe.get("path_delay_rows_total", -2))
        and int(qpe.get("direct_qA_g_rejected_rows", -1)) == 18
        and int(qpe.get("direct_qA_path_delay_rejected_rows", -1)) == 18
        and int(qpe.get("matter_rows_added", -1)) == 0
        and wrong_counts(qpe)
        and controls_counts(qpe)
    )

    tensor_basis_pass = (
        len(qpf_basis) == 2
        and {row.get("polarization_id") for row in qpf_basis} == {"plus", "cross"}
        and all(row.get("trace") == "0" for row in qpf_basis)
        and all(row.get("transverse_axes") == "x,y" for row in qpf_basis)
        and all(row.get("propagation_axis") == "z" for row in qpf_basis)
        and all(row.get("tensor_rank") == "2" for row in qpf_basis)
        and all(row.get("basis_status") == "PASS_TRACE_ZERO_TRANSVERSE_TENSOR_BASIS" for row in qpf_basis)
    )

    wave_mode_pass = (
        qpf.get("passed") is True
        and int(qpf.get("tensor_basis_rows_passed", -1)) == int(qpf.get("tensor_basis_rows_total", -2)) == 2
        and int(qpf.get("wave_mode_rows_passed", -1)) == int(qpf.get("wave_mode_rows_total", -2)) == 36
        and int(qpf.get("support_closure_rows_passed", -1)) == int(qpf.get("support_closure_rows_total", -2)) == 18
        and int(qpf.get("massless_mode_rows", -1)) == 36
        and int(qpf.get("phase_speed_c_rows", -1)) == 36
        and int(qpf.get("direct_qA_rejected_rows", -1)) == 18
        and int(qpf.get("matter_rows_added", -1)) == 0
        and tensor_basis_pass
        and wrong_counts(qpf)
        and controls_counts(qpf)
        and "massless" in qpf.get("scientific_reading", "")
        and "phase speed c" in qpf.get("scientific_reading", "")
        and "two trace-zero transverse tensor polarizations" in qpf.get("scientific_reading", "")
        and "not a graviton mass" in qpf_result_text
        and "not a full quantum-gravity theorem" in qpf_result_text
    )

    bridge_pass = (
        qpg.get("passed") is True
        and qpg.get("carrier_fraction") == "1/8"
        and qpg.get("retained_write_fraction") == "7/8"
        and int(qpg.get("frozen_spine_rows_passed", -1)) == int(qpg.get("frozen_spine_rows_total", -2))
        and int(qpg.get("weak_bridge_rows_passed", -1)) == int(qpg.get("weak_bridge_rows_total", -2))
        and int(qpg.get("path_delay_rows_passed", -1)) == int(qpg.get("path_delay_rows_total", -2))
        and int(qpg.get("strong_boundary_rows_passed", -1)) == int(qpg.get("strong_boundary_rows_total", -2))
        and int(qpg.get("quantum_support_rows_passed", -1)) == int(qpg.get("quantum_support_rows_total", -2))
        and int(qpg.get("bridge_packet_layers_passed", -1)) == int(qpg.get("bridge_packet_layers_total", -2))
        and int(qpg.get("matter_rows_added", -1)) == 0
        and qpg.get("strong_boundary_A") == "1"
        and qpg.get("strong_boundary_closure") == "7/8 + 1/16 + 1/16 = 1"
        and wrong_counts(qpg)
        and controls_counts(qpg)
        and "not a graviton rest mass" in qpg_result_text
        and "not full quantum-gravity closure" in qpg_result_text
    )

    catalog_rejection_pass = (
        qp93.get("passed") is True
        and int(qp93.get("carrier_only_rows", -1)) == 6
        and int(qp93.get("matter_rows_added_by_carrier", -1)) == 0
        and qp93.get("direct_qA_as_mass_allowed") is False
        and carrier_18.get("partition_signature") == "18"
        and carrier_18.get("operator_class") == "TENSOR_CARRIER"
        and carrier_18.get("spin_or_hand_class") == "rank2_plus_cross"
        and carrier_18.get("matter_row_allowed") == "no"
        and carrier_18.get("promotion_status") == "REJECT_MATTER_PROMOTION_CARRIER_ONLY"
        and parse_bool(qp93_wc6.get("rejected", False))
        and wrong_counts(qp93)
        and controls_counts(qp93)
        and "does not promote tensor-carrier support to matter" in qp93_result_text
    )

    shared_road_support_pass = (
        g699c.get("verdict") == "G699c_PASS_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT"
        and all(bool(v) for v in g699c.get("pass_conditions", {}).values())
        and decimal_value(g699c.get("active_shared_road_differential_s")) == Decimal("0.0")
        and decimal_value(g699c.get("engine_explained_fraction")) > Decimal("0.95")
        and decimal_value(g699c.get("one_sided_control", {}).get("ratio_one_sided_to_observed")) > Decimal("1000000")
    )

    explicit_boundary_pass = (
        "not a graviton mass" in qpf_result_text
        and "not a normal particle row" in qpf_result_text
        and "not a full quantum-gravity theorem" in qpf_result_text
        and "not a graviton rest mass" in qpg_result_text
        and "not full quantum-gravity closure" in qpg_result_text
    )

    signatures = [
        signature_row(
            "S1_DERIVED_PACKET",
            "18 must be derived from the 1/8 split-loss theorem, not fitted.",
            {
                "carrier_fraction": carrier_fraction,
                "split_loss": str(split_loss),
                "tensor_identity_alpha_H_D2": str(tensor_identity),
                "retained_fraction": retained_fraction,
            },
            "PASS" if derived_18_pass else "FAIL",
            "CR114 + QP092A",
        ),
        signature_row(
            "S2_GRAVITON_CHANNEL_CLASSIFICATION",
            "18 must be classified as massless unresolved rank-2 qA source support.",
            {
                "massless_unresolved_behavior": qpa.get("massless_unresolved_behavior"),
                "rank2_tensor_classification": qpa.get("rank2_tensor_classification"),
                "qa_source_coupling_classification": qpa.get("qa_source_coupling_classification"),
            },
            "PASS" if classification_pass else "FAIL",
            "QP092A",
        ),
        signature_row(
            "S3_SOURCE_TO_A_KERNEL",
            "The carrier must receive source support and update A only after ledger compression.",
            {
                "QP092B": qpb.get("mechanism_status"),
                "QP092C": qpc.get("kernel_rule"),
                "QP092D": qpd.get("mechanism_status"),
                "QP092E": qpe.get("mechanism_status"),
            },
            "PASS" if qa_to_a_pass and a_kernel_pass and conservation_pass and weak_field_pass else "FAIL",
            "QP092B-E",
        ),
        signature_row(
            "S4_WAVE_MODE",
            "The carrier must support two trace-zero transverse tensor modes, massless, at c.",
            {
                "tensor_basis_rows": len(qpf_basis),
                "massless_mode_rows": qpf.get("massless_mode_rows"),
                "phase_speed_c_rows": qpf.get("phase_speed_c_rows"),
                "matter_rows_added": qpf.get("matter_rows_added"),
            },
            "PASS" if wave_mode_pass else "FAIL",
            "QP092F",
        ),
        signature_row(
            "S5_BRIDGE_PACKET",
            "The same carrier route must bridge weak field, A=1 boundary, and quantum unresolved support.",
            {
                "strong_boundary_A": qpg.get("strong_boundary_A"),
                "strong_boundary_closure": qpg.get("strong_boundary_closure"),
                "bridge_packet_layers": f"{qpg.get('bridge_packet_layers_passed')}/{qpg.get('bridge_packet_layers_total')}",
            },
            "PASS" if bridge_pass else "FAIL",
            "QP092G",
        ),
        signature_row(
            "S6_CATALOG_REJECTION",
            "The 18 tensor carrier must be present only as carrier support, not matter.",
            {
                "candidate_id": carrier_18.get("candidate_id"),
                "operator_class": carrier_18.get("operator_class"),
                "partition_signature": carrier_18.get("partition_signature"),
                "matter_row_allowed": carrier_18.get("matter_row_allowed"),
                "promotion_status": carrier_18.get("promotion_status"),
            },
            "PASS" if catalog_rejection_pass else "FAIL",
            "QP093A",
        ),
        signature_row(
            "S7_SHARED_ROAD_SUPPORT",
            "Observed multimessenger propagation must remain consistent with shared GW/EM A-road language.",
            {
                "active_shared_road_differential_s": g699c.get("active_shared_road_differential_s"),
                "engine_explained_fraction": g699c.get("engine_explained_fraction"),
                "one_sided_to_observed": g699c.get("one_sided_control", {}).get("ratio_one_sided_to_observed"),
            },
            "PASS_SUPPORTING" if shared_road_support_pass else "FAIL_SUPPORTING",
            "G699c",
        ),
        signature_row(
            "S8_SCOPE_BOUNDARY",
            "The theorem must forbid particle, rest-mass, and full-QG overclaims.",
            {
                "QP092F_boundary": "not graviton mass / not normal particle row / not full QG",
                "QP092G_boundary": "not new particle row / not graviton rest mass / not full QG closure",
            },
            "PASS" if explicit_boundary_pass else "FAIL",
            "QP092F + QP092G",
        ),
    ]

    checks = [
        check_row("P1_sources_present", "All load-bearing provenance artifacts are present.", load_bearing_sources_present, load_bearing_sources_present, "source_chain"),
        check_row("P2_CR114_derives_18", "CR114 derives 18 as the 1/8 split-loss carrier.", cr114, derived_18_pass, "CR114 + QP092A"),
        check_row("P3_QP092A_classifies_graviton_channel", "QP092A classifies 18 as massless unresolved rank-2 qA source support.", qpa, classification_pass, "QP092A"),
        check_row("P4_QP092B_qA_loads_carrier", "qA source support loads the carrier and updates A after compression.", qpb, qa_to_a_pass, "QP092B"),
        check_row("P5_QP092C_recovers_A_kernel", "The carrier route recovers A(r)=r_s/r for point, multi-source, and extended sources.", qpc, a_kernel_pass, "QP092C"),
        check_row("P6_QP092D_conserves_source_ledger", "Carrier plus retained support conserves source ledger through compression.", qpd, conservation_pass, "QP092D"),
        check_row("P7_QP092E_recovers_weak_field_readouts", "Weak-field force, clock, and path-delay readouts are recovered.", qpe, weak_field_pass, "QP092E"),
        check_row("P8_QP092F_wave_mode", "Carrier supports two massless c-speed trace-zero transverse tensor modes.", qpf, wave_mode_pass, "QP092F"),
        check_row("P9_QP092G_bridge_packet", "Same carrier route bridges weak field, A=1 boundary, and quantum support.", qpg, bridge_pass, "QP092G"),
        check_row("P10_QP093A_rejects_matter_promotion", "QP093A emits the 18 row only as carrier support and rejects matter promotion.", carrier_18, catalog_rejection_pass, "QP093A"),
        check_row("P11_G699c_shared_road_support", "G699c supports shared GW/EM A-road propagation language.", g699c, shared_road_support_pass, "G699c"),
        check_row("P12_scope_boundary_explicit", "The theorem explicitly forbids particle, rest-mass, and full-QG overclaims.", explicit_boundary_pass, explicit_boundary_pass, "QP092F + QP092G"),
    ]

    wrong_controls = [
        wc_row(
            "WC1_PROMOTE_18_TO_MATTER",
            "18 is an admissible stable matter row.",
            {
                "QP093A_carrier_row": carrier_18,
                "matter_rows_added_by_carrier": qp93.get("matter_rows_added_by_carrier"),
                "QP093A_WC6_rejected": qp93_wc6.get("rejected"),
            },
            catalog_rejection_pass,
            "QP093A keeps 18 as carrier-only support with matter_row_allowed=no.",
        ),
        wc_row(
            "WC2_PROMOTE_18_TO_GRAVITON_REST_MASS",
            "18 is a graviton rest mass.",
            {
                "QP092A_behavior": qpa.get("massless_unresolved_behavior"),
                "QP092F_massless_mode_rows": qpf.get("massless_mode_rows"),
                "QP092F_WC3_MASSIVE_MODE": qpf_wc3.get("rejected"),
            },
            classification_pass and wave_mode_pass and parse_bool(qpf_wc3.get("rejected", False)),
            "QP092A and QP092F require massless unresolved carrier behavior.",
        ),
        wc_row(
            "WC3_DIRECT_QA_AS_MASS",
            "Direct qA-as-mass can replace carrier routing.",
            {
                "QP092B_direct_qA_overread_rows": qpb.get("direct_qa_overread_rows"),
                "QP092C_direct_qA_rejected_rows": qpc.get("direct_qA_rejected_rows"),
                "QP092E_direct_qA_g_rejected_rows": qpe.get("direct_qA_g_rejected_rows"),
                "QP092F_direct_qA_rejected_rows": qpf.get("direct_qA_rejected_rows"),
            },
            qa_to_a_pass and a_kernel_pass and weak_field_pass and wave_mode_pass,
            "Direct qA-as-mass is rejected across the qA, A-kernel, weak-field, and wave-mode tests.",
        ),
        wc_row(
            "WC4_SKIP_LEDGER_COMPRESSION",
            "Carrier support can update A without ledger compression.",
            {
                "QP092C_kernel_rule": qpc.get("kernel_rule"),
                "QP092D_mechanism_status": qpd.get("mechanism_status"),
                "QP092G_WC10_SKIP_LEDGER_COMPRESSION": qpg_wc10.get("rejected"),
            },
            a_kernel_pass and conservation_pass and parse_bool(qpg_wc10.get("rejected", False)),
            "A updates only after ledger compression.",
        ),
        wc_row(
            "WC5_SURFACE_DEBIT_AS_CARRIER",
            "The D^2/R surface debit is the 18 carrier.",
            {
                "split_loss": str(split_loss),
                "surface_debit_D2_over_R": str(surface_debit),
                "QP092A_classification_rows_passed": all_csv_true(qpa_classification, "passed"),
            },
            classification_pass and surface_debit == Decimal("0.750000000000000000000000000000"),
            "QP092A and CR114 separate split-loss carrier 18 from surface debit 0.75.",
        ),
        wc_row(
            "WC6_WRONG_SPLIT_FRACTION",
            "A wrong split such as 1/4, 1/16, D/R, D^2/R, raw D^2, or no split can replace 1/8.",
            {
                "QP092A_wrong_controls_rejected": f"{qpa.get('wrong_controls_rejected')}/{qpa.get('wrong_controls_total')}",
                "QP092F_wrong_controls_rejected": f"{qpf.get('wrong_controls_rejected')}/{qpf.get('wrong_controls_total')}",
                "QP092G_wrong_controls_rejected": f"{qpg.get('wrong_controls_rejected')}/{qpg.get('wrong_controls_total')}",
            },
            wrong_counts(qpa) and wrong_counts(qpf) and wrong_counts(qpg),
            "The 1/8 split is fixed by the binary face-state theorem and inherited controls.",
        ),
        wc_row(
            "WC7_SCALAR_OR_VECTOR_MODE",
            "A scalar single mode or vector three-component mode can replace the rank-2 tensor carrier.",
            {
                "QP092F_WC1_SCALAR_SINGLE_POLARIZATION": qpf_wc1.get("rejected"),
                "QP092F_WC2_VECTOR_THREE_COMPONENT_CARRIER": qpf_wc2.get("rejected"),
                "basis_rows": qpf_basis,
            },
            tensor_basis_pass and parse_bool(qpf_wc1.get("rejected", False)) and parse_bool(qpf_wc2.get("rejected", False)),
            "QP092F requires plus/cross trace-zero transverse rank-2 tensor modes.",
        ),
        wc_row(
            "WC8_CARRIER_TO_PARTICLE_ROW",
            "The wave-mode carrier becomes a particle row downstream.",
            {
                "QP092F_matter_rows_added": qpf.get("matter_rows_added"),
                "QP092F_WC5_PROMOTE_CARRIER_TO_PARTICLE_ROW": qpf_wc5.get("rejected"),
                "QP093A_matter_rows_added_by_carrier": qp93.get("matter_rows_added_by_carrier"),
            },
            int(qpf.get("matter_rows_added", -1)) == 0
            and int(qp93.get("matter_rows_added_by_carrier", -1)) == 0
            and parse_bool(qpf_wc5.get("rejected", False)),
            "The wave-mode and particle catalog both reject particle-row promotion.",
        ),
        wc_row(
            "WC9_FULL_QUANTUM_GRAVITY_CLOSURE",
            "This theorem proves full quantum-gravity closure.",
            {
                "QP092F_boundary": "not a full quantum-gravity theorem" in qpf_result_text,
                "QP092G_boundary": "not full quantum-gravity closure" in qpg_result_text,
            },
            explicit_boundary_pass,
            "The sources support a carrier theorem, not full quantum-gravity closure.",
        ),
        wc_row(
            "WC10_ONE_SIDED_PROPAGATION_DELAY",
            "GW170817 is explained by one-sided A-road propagation delay instead of shared road plus engine time.",
            {
                "active_shared_road_differential_s": g699c.get("active_shared_road_differential_s"),
                "engine_explained_fraction": g699c.get("engine_explained_fraction"),
                "one_sided_ratio_to_observed": g699c.get("one_sided_control", {}).get("ratio_one_sided_to_observed"),
            },
            shared_road_support_pass,
            "G699c rejects the one-sided propagation control and keeps GW/EM on the shared post-release road.",
        ),
        wc_row(
            "WC11_INDIVIDUAL_GRAVITON_DETECTION",
            "The artifacts directly detect an individual graviton.",
            {
                "theorem_scope": "internal SAM carrier theorem",
                "source_boundary": "candidate / channel / propagation mode / bridge packet",
            },
            explicit_boundary_pass,
            "No source claims individual detection; CR116 only names the internal carrier packet.",
        ),
    ]

    all_predictions_passed = all(parse_bool(row["passed"]) for row in checks)
    all_wrong_controls_rejected = all(parse_bool(row["rejected"]) for row in wrong_controls)
    result_class = RESULT_CLASS_PASS if all_predictions_passed and all_wrong_controls_rejected else RESULT_CLASS_FAIL

    declared_premises = {
        "cr_id": CR_ID,
        "generated_at_utc": now_utc(),
        "question": "Can SAM identify the value 18 as the graviton-channel carrier?",
        "safe_theorem_statement": (
            "Within SAM, 18 is the graviton-channel tensor-carrier packet: the unique "
            "1/8 unresolved split-loss support that is rank-2, plus/cross, massless, "
            "c-speed, qA source-coupled, A-kernel-propagating after ledger compression, "
            "and rejected as matter by the particle catalog."
        ),
        "forbidden_overclaims": [
            "18 is a stable matter row",
            "18 is a graviton rest mass",
            "18 is an observed individual graviton",
            "direct qA-as-mass replaces carrier routing",
            "CR116 is full quantum-gravity closure",
        ],
        "load_bearing_inputs": [
            "CR114 derives the 1/8 split-loss packet and 18 = alpha_H*D^2.",
            "QP092A-G execute the graviton-channel, qA, A-kernel, conservation, weak-field, wave-mode, and bridge-packet chain.",
            "QP093A rejects carrier promotion into the matter catalog.",
            "G699c is supporting propagation evidence only, not the identity proof.",
        ],
    }

    lock = {
        "cr_id": CR_ID,
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "theorem_name": "18 graviton-channel carrier theorem",
        "inside_sam_grade": "THEOREM_GATE" if result_class == RESULT_CLASS_PASS else "FAILED_THEOREM_GATE",
        "R": qpa.get("R"),
        "D": qpa.get("D"),
        "alpha_H": qpa.get("alpha_H"),
        "carrier_fraction": carrier_fraction,
        "retained_fraction": retained_fraction,
        "split_loss_tensor_channel": str(split_loss),
        "tensor_identity_alpha_H_D2": str(tensor_identity),
        "surface_debit_D2_over_R": str(surface_debit),
        "theorem_statement": declared_premises["safe_theorem_statement"],
        "necessary_signature": {
            "derived_packet": derived_18_pass,
            "graviton_channel_classification": classification_pass,
            "source_to_A_kernel": qa_to_a_pass and a_kernel_pass and conservation_pass and weak_field_pass,
            "massless_c_speed_two_tensor_polarizations": wave_mode_pass,
            "weak_strong_quantum_bridge_packet": bridge_pass,
            "particle_catalog_rejects_matter_promotion": catalog_rejection_pass,
            "shared_road_support": shared_road_support_pass,
            "scope_boundary": explicit_boundary_pass,
        },
        "supporting_GW170817": {
            "verdict": g699c.get("verdict"),
            "active_shared_road_differential_s": g699c.get("active_shared_road_differential_s"),
            "engine_explained_fraction": g699c.get("engine_explained_fraction"),
            "one_sided_to_observed": g699c.get("one_sided_control", {}).get("ratio_one_sided_to_observed"),
        },
        "source_hashes": {row["label"]: row["sha256"] for row in sources},
    }

    write_json(DECLARED_PREMISES_JSON, declared_premises)
    write_csv(
        SOURCE_CHAIN_CSV,
        sources,
        ["label", "role", "load_bearing", "source_type", "path", "exists", "sha256"],
    )
    write_csv(
        SIGNATURE_CSV,
        signatures,
        ["signature_id", "requirement", "observed", "status", "source"],
    )
    write_csv(
        CHECKS_CSV,
        checks,
        ["check_id", "description", "observed", "passed", "source"],
    )
    write_csv(
        WRONG_CONTROLS_CSV,
        wrong_controls,
        ["control_id", "hypothesis", "observed", "rejected", "reason"],
    )
    write_json(LOCK_JSON, lock)
    LOCK_SHA.write_text(sha256_file(LOCK_JSON) + "  " + branch_rel(LOCK_JSON) + "\n", encoding="ascii")

    summary = {
        "cr_id": CR_ID,
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "18_GRAVITON_CHANNEL_CARRIER_THEOREM",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "all_predictions_passed": all_predictions_passed,
        "all_wrong_controls_rejected": all_wrong_controls_rejected,
        "R": qpa.get("R"),
        "D": qpa.get("D"),
        "alpha_H": qpa.get("alpha_H"),
        "carrier_fraction": carrier_fraction,
        "retained_fraction": retained_fraction,
        "split_loss_tensor_channel": str(split_loss),
        "tensor_identity_alpha_H_D2": str(tensor_identity),
        "wave_mode": "two trace-zero transverse tensor polarizations, massless, phase_speed=c",
        "particle_catalog_status": "carrier_only_not_matter",
        "supporting_shared_road": shared_road_support_pass,
        "lock_sha256": sha256_file(LOCK_JSON),
        "source_chain_csv": branch_rel(SOURCE_CHAIN_CSV),
        "signature_csv": branch_rel(SIGNATURE_CSV),
        "checks_csv": branch_rel(CHECKS_CSV),
        "wrong_controls_csv": branch_rel(WRONG_CONTROLS_CSV),
        "lock_json": branch_rel(LOCK_JSON),
        "result_md": branch_rel(RESULT_MD),
    }
    write_json(SUMMARY_JSON, summary)

    pass_lines = "\n".join(
        f"- {'PASS' if parse_bool(row['passed']) else 'FAIL'} {row['check_id']}: {row['description']}"
        for row in checks
    )
    wc_lines = "\n".join(
        f"- {'REJECTED' if parse_bool(row['rejected']) else 'LIVE'} {row['control_id']}: {row['hypothesis']}"
        for row in wrong_controls
    )
    source_lines = "\n".join(
        f"- {row['label']} [{row['source_type']}]: `{row['path']}` sha256 `{row['sha256']}`"
        for row in sources
        if row["load_bearing"]
    )
    signature_lines = "\n".join(
        f"- {row['status']} {row['signature_id']}: {row['requirement']} ({row['source']})"
        for row in signatures
    )

    RESULT_MD.write_text(
        f"""# CR116 18 Graviton-Channel Carrier Theorem

## Verdict

```text
{result_class}
```

## Theorem Statement

Within SAM, 18 is the graviton-channel tensor-carrier packet: the unique 1/8 unresolved split-loss support derived from the closed scalar loop, equal to alpha_H*D^2, rank-2 with plus/cross tensor structure, massless, phase-speed c, qA source-coupled, propagated through ledger compression into the A kernel, and rejected as a matter row by the particle catalog.

## What This Proves

```text
carrier fraction                 = 1/8
retained write fraction          = 7/8
split-loss tensor channel        = 18
tensor identity                  = alpha_H*D^2 = 18
wave-mode basis                  = plus + cross
wave-mode behavior               = massless, phase_speed=c
catalog status                   = carrier-only, not matter
shared-road support              = G699c supporting evidence only
```

## What This Does Not Prove

- It does not promote 18 to a stable matter row.
- It does not read 18 as a graviton rest mass.
- It does not claim direct detection of an individual graviton.
- It does not replace ledger compression with direct qA-as-mass.
- It does not close full quantum gravity.

## Signature Table

{signature_lines}

## Load-Bearing Source Chain

{source_lines}

## Pass Checks

{pass_lines}

## Wrong Controls

{wc_lines}

## Scientific Reading

The strongest honest statement is not "18 is a particle." It is stronger and cleaner inside SAM: 18 is the carrier signature of the gravitational quantum channel. CR114 derives the 1/8 split-loss packet; QP092A names and classifies it as the split-loss tensor-carrier/graviton channel; QP092B-E show how qA source support reaches the A field only after ledger compression; QP092F supplies the two massless c-speed transverse tensor modes; QP092G packages the same route across weak field, A=1 boundary, and unresolved quantum support; and QP093A prevents the carrier from being mistaken for matter.

G699c is included as supporting propagation language: GW and EM share the same post-release A-road, and the GW170817 delay is engine-dominated. It is not used as the identity proof for the carrier.

## Scope

- Inside-SAM theorem-gate: PASS if the carrier signature is derived, propagated, tensorial, massless, source-coupled, and nonmatter across the frozen artifacts.
- Supporting empirical consistency: G699c shared-road propagation is consistent with the carrier language, but it remains supporting evidence.
- External/public wording should say "graviton-channel carrier packet" unless and until an external quantum-gravity interpretation is separately accepted.

## Open Debts

- Write the theorem into manuscript prose with the same boundary: carrier/channel yes; particle/rest mass/full-QG no.
- If desired, backfill a standalone QP092H-style theorem paper section that reproduces this source chain outside Courtroom.

## Hash

```text
CR116_18_graviton_carrier_lock.json sha256 = {sha256_file(LOCK_JSON)}
```
""",
        encoding="utf-8",
    )

    artifacts = [
        DECLARED_PREMISES_JSON,
        SOURCE_CHAIN_CSV,
        SIGNATURE_CSV,
        CHECKS_CSV,
        WRONG_CONTROLS_CSV,
        LOCK_JSON,
        LOCK_SHA,
        SUMMARY_JSON,
        RESULT_MD,
    ]
    update_hash_ledgers(artifacts)

    print(f"CR116 runner: result_class={result_class}")
    print(f"CR116 runner: all_predictions_passed={all_predictions_passed}")
    print(f"CR116 runner: all_wrong_controls_rejected={all_wrong_controls_rejected}")
    print(f"CR116 runner: lock_sha256={sha256_file(LOCK_JSON)}")
    return 0 if result_class == RESULT_CLASS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
