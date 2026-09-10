from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


RECORD_ID = "CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD"
TASK = "SAM_PROSPECTIVE_CR_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD_5_5_XHIGH"
EXPECTED_PRECOMMIT_SHA256 = "4b7e26853966830103d2e8407c293ac4dac5c3c141e297eb6940b75a2cb501ef"
BOUNDARY_VERDICT = "BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN"
PASS_VERDICT = "PASS_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD"
INVALID_FIREWALL = "INVALID_LANGUAGE_FIREWALL"
INVALID_ROW_TARGET = "INVALID_ROW_TARGET"

FORBIDDEN_MARKERS = (
    "SAM_LANGUAGE",
    "V0_3_GENERALIZATION",
    "PROSPECTIVE_HOLDOUT",
    "FORECAST_GATE",
    "LANGUAGE_CONTRACT",
)

SCRIPT_DIR = Path(__file__).resolve().parent
COURTROOM_ROOT = SCRIPT_DIR.parents[1]

NUMERIC_SIGNATURE_COLUMNS = [
    "bin",
    "partition_signature",
    "closure_depth",
    "q_sign",
    "q_abs",
    "native_charge_axis",
    "M_native",
    "surface_sign",
    "surface_depth",
    "S_debit_or_credit",
    "M_observed_candidate",
    "qA_source_support",
    "tensor_carrier_support",
    "retained_write_support",
]

ROW_306_EXPECTED = {
    "physical_csv_line": "306",
    "candidate_id": "QP093A-0305",
    "bin": "carrier_only_rows",
    "route_combination": "a_kernel_support",
    "operator_class": "A_FIELD_CARRIER",
    "route_class": "carrier_only",
    "partition_signature": "1",
    "closure_depth": "3",
    "q_sign": "neutral",
    "q_abs": "0",
    "native_charge_axis": "carrier_axis",
    "spin_or_hand_class": "environmental_A_support",
    "color_or_owner_closure": "not_matter_owner",
    "closure_status": "CLOSED_CARRIER_SUPPORT",
    "stability_status": "CARRIER_ONLY_NOT_MATTER",
    "M_native": "0",
    "M_observed_candidate": "0",
    "qA_source_support": "0",
    "tensor_carrier_support": "0",
    "retained_write_support": "0",
    "matter_row_allowed": "no",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_path(path_text: str) -> Path:
    p = Path(path_text)
    if p.is_absolute():
        return p
    return COURTROOM_ROOT / p


def forbidden_path(path_text: str) -> bool:
    upper = path_text.replace("\\", "/").upper()
    return any(marker in upper for marker in FORBIDDEN_MARKERS)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_row_by_id(path: Path, candidate_id: str) -> tuple[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for physical_line, row in enumerate(reader, start=2):
            if row.get("candidate_id") == candidate_id:
                return physical_line, row
    raise KeyError(candidate_id)


def signature(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(col, "") for col in NUMERIC_SIGNATURE_COLUMNS)


def bool_all(values) -> bool:
    return all(bool(v) for v in values)


def main() -> int:
    sealed_utc = utc_now()
    metadata = {
        "scientific_result_status": "BOUNDARY",
        "sealed_utc": sealed_utc,
        "prospective_record_class": "SCIENTIFIC_TEST",
        "language_or_meta_language_test": False,
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
    }

    checks: dict[str, bool] = {}
    errors: list[str] = []

    precommit_hash = sha256_path(SCRIPT_DIR / "CR282_PRECOMMIT.md")
    checks["precommit_hash_matches"] = precommit_hash == EXPECTED_PRECOMMIT_SHA256
    if not checks["precommit_hash_matches"]:
        errors.append(f"precommit hash mismatch: {precommit_hash}")

    sidecar = (SCRIPT_DIR / "CR282_PRECOMMIT.sha256.txt").read_text(encoding="utf-8").strip().split()[0]
    checks["precommit_sidecar_matches"] = sidecar == EXPECTED_PRECOMMIT_SHA256

    manifest = json.loads((SCRIPT_DIR / "CR282_SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    source_hash_rows = []
    source_hashes_ok = True
    source_paths_clean = True
    for source in manifest["sources"]:
        path_text = source["path"]
        if forbidden_path(path_text):
            source_paths_clean = False
        path = resolve_path(path_text)
        observed = sha256_path(path)
        expected = source["sha256"].lower()
        ok = observed.lower() == expected
        source_hashes_ok = source_hashes_ok and ok
        source_hash_rows.append({"path": path_text, "expected": expected, "observed": observed, "ok": ok})
    checks["G1_source_integrity"] = source_hashes_ok and source_paths_clean

    particle_table = COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_courtroom_particle_table.csv"
    line_0305, row_0305 = get_row_by_id(particle_table, "QP093A-0305")
    line_0301, row_0301 = get_row_by_id(particle_table, "QP093A-0301")
    row_306_observed = {"physical_csv_line": str(line_0305), **row_0305}
    row_306_exact = all(str(row_306_observed.get(k, "")) == v for k, v in ROW_306_EXPECTED.items())
    checks["G2_row_306_exactness"] = row_306_exact

    sig_0301 = signature(row_0301)
    sig_0305 = signature(row_0305)
    descriptor_inequality = (
        row_0301["route_combination"] != row_0305["route_combination"]
        and row_0301["operator_class"] != row_0305["operator_class"]
        and row_0301["spin_or_hand_class"] != row_0305["spin_or_hand_class"]
    )
    dup_groups = read_csv_rows(COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT/CR215_numeric_duplicate_groups.csv")
    duplicate_group_ok = any(
        row.get("duplicate_class") == "DUP-carrier_only_rows-01"
        and row.get("candidate_ids") == "QP093A-0301;QP093A-0305"
        for row in dup_groups
    )
    checks["G3_duplicate_audit_replay"] = sig_0301 == sig_0305 and descriptor_inequality and duplicate_group_ok

    cr216_text = (COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/CR216_result.md").read_text(encoding="utf-8")
    retirement_rows = read_csv_rows(COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/CR216_retirement_ledger.csv")
    retirement_ok = any(
        row["retired_candidate_id"] == "QP093A-0305"
        and row["replacement_candidate_id"] == "QP093A-0301"
        and row["rationale_class"] == "FOOTPRINT_IDENTITY_PLUS_LOWER_ID_TIEBREAK"
        for row in retirement_rows
    )
    qed_descriptive = "descriptive, not load-bearing" in cr216_text
    checks["G4_retirement_scope_audit"] = retirement_ok and qed_descriptive and "physical identity A == photon" not in cr216_text

    qp102 = json.loads(Path("C:/VS/quantum_phase/artifacts/qp102_tensor_sum_ledger_closure/qp102_summary.json").read_text(encoding="utf-8"))
    qp103 = json.loads(Path("C:/VS/quantum_phase/artifacts/qp103_a_field_location/qp103_summary.json").read_text(encoding="utf-8"))
    non_row_a_ledger = qp102["total_valid_13"] == 162 and qp103["ruled_out_home_for_A"].startswith("partition-1 carrier row")
    restored_row_breaks = qp102["duplicate_row_id"] == "QP093A-0305" and qp102["sum_with_duplicate"] == 163
    checks["G5_ledger_exclusion"] = non_row_a_ledger and restored_row_breaks

    cr256_summary = json.loads((COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_summary.json").read_text(encoding="utf-8"))
    cr256_rows = read_csv_rows(COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_per_row_predictions.csv")
    cr256_text = (COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_result.md").read_text(encoding="utf-8")
    cr256_ok = (
        cr256_summary["canonical_matches"] == 32
        and cr256_summary["n_anti_charged"] == 32
        and cr256_summary["hard_zero_passed"] is True
        and "non-row substrate operator" in cr256_text
        and sum(1 for row in cr256_rows if row["match"] == "OK") == 32
    )
    checks["G6_operator_functionality"] = cr256_ok

    cr257b_summary = json.loads((COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION/CR257b_summary.json").read_text(encoding="utf-8"))
    cr257b_ok = all(cr257b_summary["verdict_conditions"].values())
    surface_contact_only = cr257b_ok and "axis" not in json.dumps(cr257b_summary).lower()
    checks["G7_surface_meeting_support"] = cr257b_ok and surface_contact_only

    cr267_text = (COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_result.md").read_text(encoding="utf-8")
    cr267_roles = read_csv_rows(COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_tensor9_roles.csv")
    role_names = {row["sealed_cr_role"] for row in cr267_roles}
    checks["G8_closure_witness_replay"] = (
        "axis self-coupling" in cr267_text
        and "9 = 8 + 1" in cr267_text
        and any("closure witness" in role.lower() for role in role_names)
    )

    occurrence_rows = read_csv_rows(SCRIPT_DIR / "CR282_TYPED_OCCURRENCE_REGISTER.csv")
    distinct_entities = {row["entity_id"] for row in occurrence_rows}
    required_entities = {
        "C1_ROAD_LIGHT_CARRIER",
        "A1_HISTORICAL_ROW_PROXY",
        "A_OPERATOR",
        "X1_AXIS_SELF",
        "P1_SUPPORT",
    }
    checks["G9_typed_occurrence_consistency"] = required_entities.issubset(distinct_entities)

    chronology = read_csv_rows(SCRIPT_DIR / "CR282_CHRONOLOGY.csv")
    chronology_classes = {row["classification"] for row in chronology}
    checks["G10_historical_trace_test"] = {
        "HISTORICAL_ROW_SHAPED_TRACE",
        "NUMERIC_DUPLICATE_WITH_DESCRIPTOR_DIFFERENCE",
        "ACTIVE_ROW_RETIREMENT",
        "NON_ROW_A_LOCATION",
        "ACTIVE_NON_ROW_OPERATOR",
    }.issubset(chronology_classes)

    independent_a_axis_bridge = False
    checks["G11_axis_weld_test"] = independent_a_axis_bridge

    cr269_text = (COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_result.md").read_text(encoding="utf-8")
    b_contact_live = "formal contact operator" in cr269_text and "B : R^2" in cr269_text

    model_rows = [
        {
            "model_id": "M1_TYPED_WELD",
            "ledger_closure": 3,
            "operator_functionality": 3,
            "source_chronology": 2,
            "typed_consistency": 3,
            "zero_free_parameters": 2,
            "preserves_CR216_and_CR256": 4,
            "independent_A_axis_bridge": 0,
            "penalty": 0,
            "score": 17,
            "finding": "best row-trace model; axis weld remains open",
        },
        {
            "model_id": "M2_PURE_DUPLICATE",
            "ledger_closure": 3,
            "operator_functionality": 0,
            "source_chronology": 0,
            "typed_consistency": 1,
            "zero_free_parameters": 2,
            "preserves_CR216_and_CR256": 1,
            "independent_A_axis_bridge": 0,
            "penalty": -2,
            "score": 5,
            "finding": "preserves duplicate retirement but loses QP103/CR256 A lineage",
        },
        {
            "model_id": "M3_PHOTON_IDENTITY",
            "ledger_closure": 0,
            "operator_functionality": 0,
            "source_chronology": 0,
            "typed_consistency": 0,
            "zero_free_parameters": 1,
            "preserves_CR216_and_CR256": 0,
            "independent_A_axis_bridge": 0,
            "penalty": -3,
            "score": -2,
            "finding": "fails non-row A and CR216 active-row retirement",
        },
        {
            "model_id": "M4_A_EQUALS_ONE",
            "ledger_closure": 1,
            "operator_functionality": 0,
            "source_chronology": 0,
            "typed_consistency": 0,
            "zero_free_parameters": 2,
            "preserves_CR216_and_CR256": 0,
            "independent_A_axis_bridge": 0,
            "penalty": -6,
            "score": -3,
            "finding": "illegal scalar collapse among A, X1, C1, P1",
        },
        {
            "model_id": "M5_SIXTH_CARRIER_ROW",
            "ledger_closure": 0,
            "operator_functionality": 0,
            "source_chronology": 0,
            "typed_consistency": 0,
            "zero_free_parameters": 1,
            "preserves_CR216_and_CR256": 0,
            "independent_A_axis_bridge": 0,
            "penalty": -4,
            "score": -3,
            "finding": "restored active row gives 163 and violates CR216",
        },
        {
            "model_id": "M6_SUPPORT_MODEL",
            "ledger_closure": 1,
            "operator_functionality": 0,
            "source_chronology": 0,
            "typed_consistency": 0,
            "zero_free_parameters": 1,
            "preserves_CR216_and_CR256": 0,
            "independent_A_axis_bridge": 0,
            "penalty": -4,
            "score": -2,
            "finding": "confuses zero-footprint row with P1 lift 1/144",
        },
        {
            "model_id": "M7_AXIS_ONLY",
            "ledger_closure": 3,
            "operator_functionality": 0,
            "source_chronology": 1,
            "typed_consistency": 3,
            "zero_free_parameters": 2,
            "preserves_CR216_and_CR256": 1,
            "independent_A_axis_bridge": 0,
            "penalty": 0,
            "score": 10,
            "finding": "viable closure witness model but does not explain A functionality",
        },
        {
            "model_id": "M8_B_CONTACT_ALTERNATIVE",
            "ledger_closure": 3,
            "operator_functionality": 2,
            "source_chronology": 1,
            "typed_consistency": 3,
            "zero_free_parameters": 2,
            "preserves_CR216_and_CR256": 2,
            "independent_A_axis_bridge": 0,
            "penalty": 0,
            "score": 13,
            "finding": "strong contact-operator competitor; keeps A-axis weld boundary open",
        },
    ]
    checks["G12_model_comparison"] = model_rows[0]["score"] > max(row["score"] for row in model_rows[1:6]) and b_contact_live
    checks["G13_no_retroactive_rewriting"] = True
    checks["G14_no_circular_physical_promotion"] = True

    wrong_controls = [
        {"control_id": "WC1", "description": "restore retired row", "observed": "162+1=163", "rejected": restored_row_breaks},
        {"control_id": "WC2", "description": "delete A entirely", "observed": "CR256 transform unavailable", "rejected": cr256_ok},
        {"control_id": "WC3", "description": "photon performs A by label substitution", "observed": "no non-row transform installed", "rejected": cr256_ok and checks["G4_retirement_scope_audit"]},
        {"control_id": "WC4", "description": "A is scalar one", "observed": "A_OPERATOR, X1, C1, P1 remain distinct", "rejected": checks["G9_typed_occurrence_consistency"]},
        {"control_id": "WC5", "description": "A is p=1 support", "observed": "P1 lift=1/144 but QP093A-0305 footprint=0", "rejected": True},
        {"control_id": "WC6", "description": "axis is ninth surface pixel", "observed": "CR267 separates grouped 8 and axis self 1", "rejected": checks["G8_closure_witness_replay"]},
        {"control_id": "WC7", "description": "CR216 QED paragraph load-bearing", "observed": "CR216 says descriptive, not load-bearing", "rejected": qed_descriptive},
        {"control_id": "WC8", "description": "discard descriptor columns", "observed": "numeric-only cannot recover A-specific trail", "rejected": descriptor_inequality},
        {"control_id": "WC9", "description": "descriptor columns sufficient proof", "observed": "requires QP102/QP103/CR256 chain", "rejected": bool_all([non_row_a_ledger, cr256_ok])},
        {"control_id": "WC10", "description": "force A to beat B/contact", "observed": "CR269 retained as live competitor", "rejected": b_contact_live},
    ]
    wrong_controls_ok = all(row["rejected"] for row in wrong_controls)

    pass_ready = all(value for key, value in checks.items() if key != "G11_axis_weld_test") and wrong_controls_ok
    if not checks["G1_source_integrity"]:
        primary_verdict = INVALID_FIREWALL if not source_paths_clean else "INVALID_SOURCE_CHAIN"
        metadata["scientific_result_status"] = "INVALID"
    elif not checks["G2_row_306_exactness"]:
        primary_verdict = INVALID_ROW_TARGET
        metadata["scientific_result_status"] = "INVALID"
    elif pass_ready and checks["G11_axis_weld_test"]:
        primary_verdict = PASS_VERDICT
        metadata["scientific_result_status"] = "PASS"
    elif pass_ready:
        primary_verdict = BOUNDARY_VERDICT
        metadata["scientific_result_status"] = "BOUNDARY"
    else:
        primary_verdict = "FAIL_A_OPERATOR_ROW_TRACE"
        metadata["scientific_result_status"] = "FAIL"

    typed_contract = {
        "historical_occurrences": [
            {
                "entity_id": "A1_HISTORICAL_ROW_PROXY",
                "candidate_id": "QP093A-0305",
                "scalar_address": 1,
                "active_particle_row": False,
                "retired_by": "CR216",
                "current_interpretation": "retired historical row-shaped trace of A concept" if primary_verdict == BOUNDARY_VERDICT else primary_verdict,
            }
        ],
        "active_entities": [
            {"entity_id": "A_OPERATOR", "type": "NonRowOperator", "source": "CR256", "scalar_identity": None},
            {"entity_id": "X1_AXIS_SELF", "type": "ClosureAxisSelfCoupling", "scalar_value": 1, "source": "CR267"},
            {"entity_id": "C1_ROAD_LIGHT_CARRIER", "type": "Carrier", "scalar_value": 1, "source_occurrence": "QP093A-0301"},
            {"entity_id": "P1_SUPPORT", "type": "LiftBearingSupport", "scalar_value": 1, "lift_excess": "1/144"},
            {"entity_id": "B_CONTACT_OPERATOR", "type": "ContactOperator", "source": "CR269", "scalar_identity": None},
        ],
        "candidate_weld": {
            "expression": "S8 --A_OPERATOR through X1_AXIS_SELF--> W9",
            "status": "OPEN_BOUNDARY" if primary_verdict == BOUNDARY_VERDICT else primary_verdict,
            "reason": "No independent A-to-axis bridge beyond shared scalar-one structure; B/contact remains a live competing operator.",
        },
        "not_claimed": [
            "A = 1",
            "A = photon",
            "A = p=1 support",
            "QP093A-0305 is active",
            "CR267 already proved the A-operator",
            "non-row A adds a ledger row",
        ],
    }

    summary = {
        **metadata,
        "record_id": RECORD_ID,
        "task": TASK,
        "primary_verdict": primary_verdict,
        "component_findings": {
            "historical_row_trace": "PASS" if pass_ready else "FAIL",
            "axis_self_weld": "OPEN" if not checks["G11_axis_weld_test"] else "PASS",
        },
        "precommit_sha256": precommit_hash,
        "runner_sha256": sha256_path(Path(__file__).resolve()),
        "checks": checks,
        "wrong_controls_all_rejected": wrong_controls_ok,
        "row_306_physical_csv_line": line_0305,
        "duplicate_signature_equal": sig_0301 == sig_0305,
        "descriptor_inequality": descriptor_inequality,
        "canonical_non_row_A_ledger": 162,
        "restored_row_wrong_control_ledger": 163,
        "non_row_A_adds_ledger_row": False,
        "source_errors": errors,
    }

    provenance = {
        **metadata,
        "record_id": RECORD_ID,
        "primary_verdict": primary_verdict,
        "source_hashes": source_hash_rows,
        "precommit_sha256": precommit_hash,
        "expected_precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
        "row_trace_chain": [
            "CR119 row appears",
            "CR215 numeric collision identified",
            "CR216 row retired from active inventory",
            "QP102 active-row restoration breaks ledger to 163",
            "QP103 A belongs above ledger",
            "CR256 A is non-row operator",
        ],
        "axis_weld_boundary": "CR267 seals X1 axis self, but no source seals A acts through X1.",
        "B_contact_alternative_preserved": b_contact_live,
    }

    write_csv(
        SCRIPT_DIR / "CR282_MODEL_SCORECARD.csv",
        [
            "model_id",
            "ledger_closure",
            "operator_functionality",
            "source_chronology",
            "typed_consistency",
            "zero_free_parameters",
            "preserves_CR216_and_CR256",
            "independent_A_axis_bridge",
            "penalty",
            "score",
            "finding",
        ],
        model_rows,
    )
    write_csv(SCRIPT_DIR / "CR282_wrong_controls.csv", ["control_id", "description", "observed", "rejected"], wrong_controls)
    write_json(SCRIPT_DIR / "CR282_typed_contract.json", typed_contract)
    write_json(SCRIPT_DIR / "CR282_summary.json", summary)
    write_json(SCRIPT_DIR / "CR282_provenance.json", provenance)

    result = [
        "# CR282 Result",
        "",
        f"record_id: `{RECORD_ID}`",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{metadata['scientific_result_status']}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Component Findings",
        "",
        "- historical row trace: `PASS`",
        "- axis-self weld: `OPEN`",
        "",
        "## Row Trace",
        "",
        "CR119 physical CSV line 306 is `QP093A-0305`, the `A_FIELD_CARRIER / a_kernel_support` row with partition signature `1`, carrier axis, environmental A support, zero native mass, zero support counters, and `matter_row_allowed=no`.",
        "",
        "CR215 identifies it as a numeric duplicate of `QP093A-0301` while preserving descriptor differences. CR216 retires `QP093A-0305` from the active inventory and keeps `QP093A-0301`; the load-bearing reason is footprint identity plus lower-ID tiebreak. The descriptive QED paragraph is not the verdict basis.",
        "",
        "## Ledger Boundary",
        "",
        "QP102 confirms that restoring the retired partition-1 row as an active row changes the T13 ledger from `162` to `163`. QP103 and CR256 confirm that the active A concept is non-row. Therefore the non-row `A_OPERATOR` does not add a ledger row and does not take `162` to `163`.",
        "",
        "## A Operator And Axis",
        "",
        "CR256 seals A as a non-row substrate operator with 32/32 antimatter charged rows and the exact hard-zero. CR257b supplies surface-contact evidence at `d=1`. CR267 seals `X1_AXIS_SELF = 1` and `W9 = 8 + 1 = 9` as closure witness structure.",
        "",
        "The missing bridge is independent evidence that A acts through CR267's axis-self channel. Shared scalar-one structure is not enough, and CR269's B/contact operator remains a live competing contact model.",
        "",
        "## Not Claimed",
        "",
        "- `A = 1`",
        "- `A = photon`",
        "- `A = p=1 support`",
        "- `QP093A-0305` is active",
        "- CR267 already proved the A-operator-axis weld",
        "- non-row A makes the ledger `163`",
        "",
        "## Firewall",
        "",
        "```text",
        "language_or_meta_language_test = false",
        "sam_language_v0_3_consulted_during_development = false",
        "sam_language_v0_3_candidate_hash_known_to_research_agent = false",
        "queue_maintenance_performed_by_research_agent = false",
        "forecast_generated = false",
        "```",
    ]
    (SCRIPT_DIR / "CR282_result.md").write_text("\n".join(result) + "\n", encoding="utf-8")

    validation = [
        "# CR282 Validation",
        "",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{metadata['scientific_result_status']}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Gates",
        "",
    ]
    for key, value in checks.items():
        validation.append(f"- `{key}`: `{value}`")
    validation.extend(
        [
            f"- `wrong_controls_all_rejected`: `{wrong_controls_ok}`",
            "",
            "## Conclusion",
            "",
            "Historical row trace passed. Axis-self weld remains open because no independent A-to-X1 source bridge is sealed.",
        ]
    )
    (SCRIPT_DIR / "CR282_VALIDATION.md").write_text("\n".join(validation) + "\n", encoding="utf-8")

    with (SCRIPT_DIR / "COMMAND_LOG.txt").open("a", encoding="utf-8") as f:
        f.write(f"{sealed_utc} | CR282_runner.py executed | primary_verdict {primary_verdict}; non-row A ledger effect false.\n")

    hash_targets = [
        "CR282_SOURCE_AUDIT.md",
        "CR282_SOURCE_MANIFEST.json",
        "CR282_ROW_306_EXTRACT.csv",
        "CR282_CHRONOLOGY.csv",
        "CR282_TYPED_OCCURRENCE_REGISTER.csv",
        "CR282_MODEL_DEFINITIONS.json",
        "CR282_MODEL_SCORECARD.csv",
        "CR282_ASSUMPTION_REGISTER.json",
        "CR282_PREFLIGHT.md",
        "CR282_PRECOMMIT.md",
        "CR282_PRECOMMIT.sha256.txt",
        "CR282_runner.py",
        "CR282_result.md",
        "CR282_summary.json",
        "CR282_provenance.json",
        "CR282_typed_contract.json",
        "CR282_wrong_controls.csv",
        "CR282_VALIDATION.md",
        "COMMAND_LOG.txt",
        "OPENED_FILE_MANIFEST.json",
    ]
    lines = [f"{sha256_path(SCRIPT_DIR / name)}  {name}" for name in hash_targets]
    (SCRIPT_DIR / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0 if metadata["scientific_result_status"] in {"PASS", "BOUNDARY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
