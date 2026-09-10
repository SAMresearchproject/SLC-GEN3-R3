from __future__ import annotations

import csv
import hashlib
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import numpy as np


getcontext().prec = 80

RECORD_ID = "CR120Q_P9_G0_UPDATED_SHEET_BINDING_MAGNITUDE_HOLDOUT_SENSITIVITY"
TASK = "Measure binding residual improvement from updated p9 g0 spreadsheet assemblies"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SOURCE_MANIFEST = HERE / "CR120Q_SOURCE_MANIFEST.csv"
PRECOMMIT = HERE / "CR120Q_PRECOMMIT.md"
PRECOMMIT_HASH_FILE = HERE / "CR120Q_PRECOMMIT.sha256.txt"

ROSTER100 = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120N_FRESH_QP093A_UPDATED_SHEET_100_81_ROSTER_COMPARISON" / "CR120N_ROSTER100_RAW.csv"
ROSTER81 = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120N_FRESH_QP093A_UPDATED_SHEET_100_81_ROSTER_COMPARISON" / "CR120N_ROSTER81_RAW.csv"
DERIVATION = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120K_P9_G0_W9_8_PLUS_1_INDEPENDENT_INVENTORY_DISCRIMINATION" / "CR120K_DERIVATION_MATRIX.json"
CR242_DIR = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR242_SAM_BINDING_CURVATURE_DERIVATION"
CR242_DATASET = CR242_DIR / "CR242_binding_dataset.csv"
CR242_COEFFICIENTS = CR242_DIR / "CR242_model_coefficients.csv"
CR242_COMPARISON = CR242_DIR / "CR242_model_comparison.csv"

TRAIN_SPLIT = "train_cr240_lane_a_non_anchor"
TEST_SPLIT = "test_cr241_holdout"
U_TO_MEV = 931.49410242
R = 12.0
S = 8.0
THETA = 18.0
V = 27.0

FEATURES = [
    "intercept",
    "sam_volume_A_over_SM",
    "sam_surface_A23_over_RV",
    "sam_coulomb_ZZminus1_over_A13_SMV",
    "sam_asymmetry_NmZ2_over_A_STheta",
    "sam_pairing_over_MsqrtA",
    "sam_z_residue_over_RM",
    "sam_abs_NmZ_over_AR",
]

SCENARIO_ORDER = [
    "BASELINE_REGISTERED_M126",
    "SHEET81_AS_SAVED_12600",
    "SHEET81_P9G0_REMOVED_12550P5",
    "SHEET100_P9G0_REMOVED_16200",
]

EXPECTED_P9_IDS = {
    "QP093A-0019",
    "QP093A-0020",
    "QP093A-0021",
    "QP093A-0085",
    "QP093A-0086",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def manifest_path(text: str) -> Path:
    path = Path(text)
    return path if path.is_absolute() else ROOT / path


def verify_sources() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_MANIFEST):
        path = manifest_path(row["path"])
        exists = path.is_file()
        actual_bytes = path.stat().st_size if exists else None
        actual_hash = sha256(path) if exists else None
        passed = bool(
            exists
            and actual_bytes == int(row["bytes"])
            and actual_hash == row["sha256"].lower()
        )
        checks.append(
            {
                "ordinal": int(row["ordinal"]),
                "role": row["role"],
                "authority": row["authority"],
                "path": row["path"],
                "expected_bytes": int(row["bytes"]),
                "actual_bytes": actual_bytes,
                "expected_sha256": row["sha256"].lower(),
                "actual_sha256": actual_hash,
                "pass": passed,
            }
        )
    if not all(check["pass"] for check in checks):
        raise RuntimeError("Frozen source validation failed")

    expected_precommit = PRECOMMIT_HASH_FILE.read_text(encoding="utf-8").split()[0].lower()
    if sha256(PRECOMMIT) != expected_precommit:
        raise RuntimeError("Precommit hash validation failed")
    return checks


def exact_decimal(value: str | int | float) -> Decimal:
    text = str(value).strip()
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return Decimal(numerator) / Decimal(denominator)
    return Decimal(text)


def dstr(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text if text and text != "-0" else "0"


def reconstruct_scenarios() -> tuple[list[dict[str, Any]], dict[str, float], dict[str, Any]]:
    roster100 = read_csv(ROSTER100)
    roster81 = read_csv(ROSTER81)
    derivation = json.loads(DERIVATION.read_text(encoding="utf-8-sig"))
    derivation_rows = derivation["rows"]

    derivation_ids = {row["candidate_id"] for row in derivation_rows}
    relation_ok = (
        len(derivation_rows) == 5
        and derivation_ids == EXPECTED_P9_IDS
        and all(row["M_native_exact_additivity"] for row in derivation_rows)
        and all(exact_decimal(row["M_native_residual"]) == 0 for row in derivation_rows)
        and all(row["all_type_checks_passed"] for row in derivation_rows)
        and all(row["derived_partition_expression"] == "8+1" for row in derivation_rows)
    )

    ids100 = {row["candidate_id"] for row in roster100}
    ids81 = {row["candidate_id"] for row in roster81}
    sum100 = sum((exact_decimal(row["M_native"]) for row in roster100), Decimal(0))
    sum81 = sum((exact_decimal(row["M_native"]) for row in roster81), Decimal(0))
    retained81 = [row for row in roster81 if row["candidate_id"] in EXPECTED_P9_IDS]
    retained81_sum = sum((exact_decimal(row["M_native"]) for row in retained81), Decimal(0))
    corrected81 = sum81 - retained81_sum

    parent_ids = {
        parent
        for row in derivation_rows
        for parent in (row["parent_p1_id"], row["parent_p8_id"])
    }
    reconstruction_ok = (
        relation_ok
        and len(roster100) == 100
        and len(ids100) == 100
        and sum100 == Decimal("16200")
        and not (ids100 & EXPECTED_P9_IDS)
        and parent_ids.issubset(ids100)
        and len(roster81) == 81
        and len(ids81) == 81
        and sum81 == Decimal("12600")
        and {row["candidate_id"] for row in retained81} == EXPECTED_P9_IDS - {"QP093A-0021"}
        and retained81_sum == Decimal("49.5")
        and corrected81 == Decimal("12550.5")
        and parent_ids.issubset(ids81)
    )
    if not reconstruction_ok:
        raise RuntimeError("Spreadsheet-sum reconstruction failed")

    scenario_rows = [
        {
            "scenario": "BASELINE_REGISTERED_M126",
            "M_scale_sum": "126",
            "source_rows": "",
            "p9_g0_values_removed": "baseline_not_applicable",
            "source_status": "frozen_CR242_baseline",
        },
        {
            "scenario": "SHEET81_AS_SAVED_12600",
            "M_scale_sum": dstr(sum81),
            "source_rows": len(roster81),
            "p9_g0_values_removed": "false",
            "source_status": "as_saved_control_four_charged_p9_g0_values_retained",
        },
        {
            "scenario": "SHEET81_P9G0_REMOVED_12550P5",
            "M_scale_sum": dstr(corrected81),
            "source_rows": len(roster81),
            "p9_g0_values_removed": "true",
            "source_status": "four_remaining_charged_p9_g0_values_zeroed_neutral_already_absent",
        },
        {
            "scenario": "SHEET100_P9G0_REMOVED_16200",
            "M_scale_sum": dstr(sum100),
            "source_rows": len(roster100),
            "p9_g0_values_removed": "true",
            "source_status": "all_five_p9_g0_values_absent_as_saved",
        },
    ]
    scenarios = {row["scenario"]: float(row["M_scale_sum"]) for row in scenario_rows}
    reconstruction = {
        "exact_p9_g0_relation_pass": relation_ok,
        "roster100_rows": len(roster100),
        "roster100_sum_M_native": dstr(sum100),
        "roster100_p9_g0_rows": sorted(ids100 & EXPECTED_P9_IDS),
        "roster81_rows": len(roster81),
        "roster81_sum_M_native_as_saved": dstr(sum81),
        "roster81_retained_p9_g0_ids": sorted(row["candidate_id"] for row in retained81),
        "roster81_retained_p9_g0_sum": dstr(retained81_sum),
        "roster81_sum_after_specific_p9_g0_removal": dstr(corrected81),
        "all_ten_parent_rows_retained_in_both": parent_ids.issubset(ids100) and parent_ids.issubset(ids81),
        "all_values_are_whole_roster_sums": True,
        "means_used": False,
    }
    return scenario_rows, scenarios, reconstruction


def feature_vector(row: dict[str, str], m_scale: float) -> list[float]:
    z = int(row["Z"])
    n = int(row["N"])
    a = int(row["A"])
    nmz = n - z
    pair = int(row["pairing_sign"])
    a13 = a ** (1.0 / 3.0)
    a23 = a ** (2.0 / 3.0)
    sqrt_a = math.sqrt(a)
    return [
        1.0,
        a / (S * m_scale),
        a23 / (R * V),
        z * (z - 1) / (a13 * S * m_scale * V),
        (nmz * nmz) / (a * S * THETA),
        pair / (m_scale * sqrt_a),
        ((z - 1) % int(R)) / (R * m_scale),
        abs(nmz) / (a * R),
    ]


def design(rows: list[dict[str, str]], m_scale: float) -> np.ndarray:
    return np.asarray([feature_vector(row, m_scale) for row in rows], dtype=float)


def targets(rows: list[dict[str, str]]) -> np.ndarray:
    return np.asarray([float(row["B_u"]) for row in rows], dtype=float)


def zero_free_predictions(rows: list[dict[str, str]], m_scale: float) -> np.ndarray:
    predictions: list[float] = []
    for row in rows:
        z = int(row["Z"])
        n = int(row["N"])
        a = int(row["A"])
        nmz = n - z
        pair = int(row["pairing_sign"])
        a13 = a ** (1.0 / 3.0)
        a23 = a ** (2.0 / 3.0)
        prediction = (
            a / (S * m_scale)
            - a23 / (R * V)
            - z * (z - 1) / (a13 * S * m_scale * V)
            - (nmz * nmz) / (a * S * THETA)
            + pair / (m_scale * math.sqrt(a))
        )
        predictions.append(prediction)
    return np.asarray(predictions, dtype=float)


def metric(y: np.ndarray, prediction: np.ndarray) -> dict[str, float]:
    residual = y - prediction
    return {
        "rms_u": float(np.sqrt(np.mean(residual * residual))),
        "mae_u": float(np.mean(np.abs(residual))),
        "max_abs_u": float(np.max(np.abs(residual))),
        "bias_obs_minus_pred_u": float(np.mean(residual)),
        "rms_MeV": float(np.sqrt(np.mean(residual * residual)) * U_TO_MEV),
        "mae_MeV": float(np.mean(np.abs(residual)) * U_TO_MEV),
        "max_abs_MeV": float(np.max(np.abs(residual)) * U_TO_MEV),
        "bias_obs_minus_pred_MeV": float(np.mean(residual) * U_TO_MEV),
    }


def published_metric(model: str, split: str) -> dict[str, str]:
    matches = [
        row for row in read_csv(CR242_COMPARISON)
        if row["model"] == model and row["split"] == split
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Missing published CR242 metric for {model}/{split}")
    return matches[0]


def frozen_coefficients() -> np.ndarray:
    rows = [
        row for row in read_csv(CR242_COEFFICIENTS)
        if row["model"] == "SAM_TYPED_BASIS_FIT"
    ]
    by_feature = {row["feature"]: float(row["coefficient"]) for row in rows}
    if set(by_feature) != set(FEATURES):
        raise RuntimeError("Frozen CR242 SAM coefficient set mismatch")
    return np.asarray([by_feature[name] for name in FEATURES], dtype=float)


def classify(delta_rms_mev: float, delta_mae_mev: float) -> tuple[str, bool]:
    if delta_rms_mev > 1e-9:
        direction = "IMPROVED"
    elif abs(delta_rms_mev) <= 1e-9:
        direction = "UNCHANGED"
    else:
        direction = "WORSE"
    material = delta_rms_mev >= 0.01 and delta_mae_mev >= -1e-9
    return direction, material


def main() -> None:
    source_checks = verify_sources()
    scenario_rows, scenarios, reconstruction = reconstruct_scenarios()
    write_csv(HERE / "CR120Q_scale_scenarios.csv", scenario_rows)

    dataset = read_csv(CR242_DATASET)
    train_rows = [row for row in dataset if row["split"] == TRAIN_SPLIT]
    test_rows = [row for row in dataset if row["split"] == TEST_SPLIT]
    if len(train_rows) != 49 or len(test_rows) != 20 or len(dataset) != 69:
        raise RuntimeError("Frozen CR242 split gate failed")

    y_train = targets(train_rows)
    y_test = targets(test_rows)
    frozen_coef = frozen_coefficients()

    predictions: dict[tuple[str, str, str], np.ndarray] = {}
    coefficients_output: list[dict[str, Any]] = []
    rank_rows: list[dict[str, Any]] = []

    for scenario in SCENARIO_ORDER:
        m_scale = scenarios[scenario]
        x_train = design(train_rows, m_scale)
        x_test = design(test_rows, m_scale)

        predictions[("FROZEN_COEFFICIENT_TRANSFER", scenario, TRAIN_SPLIT)] = x_train @ frozen_coef
        predictions[("FROZEN_COEFFICIENT_TRANSFER", scenario, TEST_SPLIT)] = x_test @ frozen_coef
        for feature, coefficient in zip(FEATURES, frozen_coef):
            coefficients_output.append(
                {
                    "surface": "FROZEN_COEFFICIENT_TRANSFER",
                    "scenario": scenario,
                    "feature": feature,
                    "coefficient": repr(float(coefficient)),
                    "fit_rows": 0,
                    "coefficient_source": "CR242_model_coefficients.csv",
                }
            )

        refit_coef, _, refit_rank, singular = np.linalg.lstsq(x_train, y_train, rcond=None)
        predictions[("TRAIN_ONLY_REFIT", scenario, TRAIN_SPLIT)] = x_train @ refit_coef
        predictions[("TRAIN_ONLY_REFIT", scenario, TEST_SPLIT)] = x_test @ refit_coef
        for feature, coefficient in zip(FEATURES, refit_coef):
            coefficients_output.append(
                {
                    "surface": "TRAIN_ONLY_REFIT",
                    "scenario": scenario,
                    "feature": feature,
                    "coefficient": repr(float(coefficient)),
                    "fit_rows": len(train_rows),
                    "coefficient_source": "training_rows_only",
                }
            )

        predictions[("FIXED_ZERO_FREE_SURFACE", scenario, TRAIN_SPLIT)] = zero_free_predictions(train_rows, m_scale)
        predictions[("FIXED_ZERO_FREE_SURFACE", scenario, TEST_SPLIT)] = zero_free_predictions(test_rows, m_scale)

        rank_rows.append(
            {
                "scenario": scenario,
                "M_scale_sum": m_scale,
                "train_design_rank": int(np.linalg.matrix_rank(x_train)),
                "reported_lstsq_rank": int(refit_rank),
                "feature_count": len(FEATURES),
                "train_rows": len(train_rows),
                "smallest_singular_value": float(np.min(singular)),
                "largest_singular_value": float(np.max(singular)),
                "condition_number": float(np.max(singular) / np.min(singular)),
            }
        )

    write_csv(HERE / "CR120Q_coefficients.csv", coefficients_output)

    surfaces = ["FROZEN_COEFFICIENT_TRANSFER", "TRAIN_ONLY_REFIT", "FIXED_ZERO_FREE_SURFACE"]
    metric_records: dict[tuple[str, str, str], dict[str, float]] = {}
    for surface in surfaces:
        for scenario in SCENARIO_ORDER:
            for split, rows, y in ((TRAIN_SPLIT, train_rows, y_train), (TEST_SPLIT, test_rows, y_test)):
                metric_records[(surface, scenario, split)] = metric(y, predictions[(surface, scenario, split)])

    metrics_output: list[dict[str, Any]] = []
    for surface in surfaces:
        baseline_test = metric_records[(surface, "BASELINE_REGISTERED_M126", TEST_SPLIT)]
        for scenario in SCENARIO_ORDER:
            for split in (TRAIN_SPLIT, TEST_SPLIT):
                values = metric_records[(surface, scenario, split)]
                if split == TEST_SPLIT:
                    delta_rms = baseline_test["rms_MeV"] - values["rms_MeV"]
                    delta_mae = baseline_test["mae_MeV"] - values["mae_MeV"]
                    if scenario == "BASELINE_REGISTERED_M126":
                        direction, material = "BASELINE", False
                    else:
                        direction, material = classify(delta_rms, delta_mae)
                else:
                    delta_rms, delta_mae, direction, material = math.nan, math.nan, "NOT_SCORED", False
                metrics_output.append(
                    {
                        "surface": surface,
                        "scenario": scenario,
                        "M_scale_sum": scenarios[scenario],
                        "split": split,
                        "n": len(train_rows) if split == TRAIN_SPLIT else len(test_rows),
                        **values,
                        "delta_RMS_MeV_vs_same_surface_M126": "" if math.isnan(delta_rms) else delta_rms,
                        "delta_MAE_MeV_vs_same_surface_M126": "" if math.isnan(delta_mae) else delta_mae,
                        "direction": direction,
                        "material_improvement": material,
                    }
                )
    write_csv(HERE / "CR120Q_metrics.csv", metrics_output)

    prediction_rows: list[dict[str, Any]] = []
    for surface in surfaces:
        for scenario in SCENARIO_ORDER:
            for split, rows, y in ((TRAIN_SPLIT, train_rows, y_train), (TEST_SPLIT, test_rows, y_test)):
                pred = predictions[(surface, scenario, split)]
                for row, target, prediction in zip(rows, y, pred):
                    residual = float(target - prediction)
                    prediction_rows.append(
                        {
                            "surface": surface,
                            "scenario": scenario,
                            "M_scale_sum": scenarios[scenario],
                            "split": split,
                            "isotope": row["isotope"],
                            "Z": row["Z"],
                            "N": row["N"],
                            "A": row["A"],
                            "B_u_observed_u": float(target),
                            "B_u_predicted_u": float(prediction),
                            "residual_obs_minus_pred_u": residual,
                            "abs_residual_u": abs(residual),
                            "residual_obs_minus_pred_MeV": residual * U_TO_MEV,
                            "abs_residual_MeV": abs(residual) * U_TO_MEV,
                        }
                    )
    write_csv(HERE / "CR120Q_predictions.csv", prediction_rows)

    published_sam_train = float(published_metric("SAM_TYPED_BASIS_FIT", TRAIN_SPLIT)["rms_u"])
    published_sam_test = float(published_metric("SAM_TYPED_BASIS_FIT", TEST_SPLIT)["rms_u"])
    published_zero_train = float(published_metric("SAM_ZERO_FREE_TYPED_CANDIDATE", TRAIN_SPLIT)["rms_u"])
    published_zero_test = float(published_metric("SAM_ZERO_FREE_TYPED_CANDIDATE", TEST_SPLIT)["rms_u"])
    refit_train = metric_records[("TRAIN_ONLY_REFIT", "BASELINE_REGISTERED_M126", TRAIN_SPLIT)]["rms_u"]
    refit_test = metric_records[("TRAIN_ONLY_REFIT", "BASELINE_REGISTERED_M126", TEST_SPLIT)]["rms_u"]
    zero_train = metric_records[("FIXED_ZERO_FREE_SURFACE", "BASELINE_REGISTERED_M126", TRAIN_SPLIT)]["rms_u"]
    zero_test = metric_records[("FIXED_ZERO_FREE_SURFACE", "BASELINE_REGISTERED_M126", TEST_SPLIT)]["rms_u"]

    reproduction = {
        "refit_train_abs_delta_u": abs(refit_train - published_sam_train),
        "refit_test_abs_delta_u": abs(refit_test - published_sam_test),
        "zero_free_train_abs_delta_u": abs(zero_train - published_zero_train),
        "zero_free_test_abs_delta_u": abs(zero_test - published_zero_test),
    }
    reproduction_pass = all(delta <= 1e-12 for delta in reproduction.values())

    baseline_refit_test_pred = predictions[("TRAIN_ONLY_REFIT", "BASELINE_REGISTERED_M126", TEST_SPLIT)]
    refit_invariance = {}
    for scenario in SCENARIO_ORDER[1:]:
        candidate = predictions[("TRAIN_ONLY_REFIT", scenario, TEST_SPLIT)]
        refit_invariance[scenario] = {
            "max_abs_prediction_delta_u_vs_M126": float(np.max(np.abs(candidate - baseline_refit_test_pred))),
            "rms_prediction_delta_u_vs_M126": float(np.sqrt(np.mean((candidate - baseline_refit_test_pred) ** 2))),
        }

    x_base = design(train_rows, scenarios["BASELINE_REGISTERED_M126"])
    base_rank = int(np.linalg.matrix_rank(x_base))
    constant_rank_controls = {}
    for label, value in {
        "sum_16200": 16200.0,
        "sum_12600": 12600.0,
        "sum_12550p5": 12550.5,
        "five_row_50p625": 50.625,
        "remaining_four_49p5": 49.5,
        "sum_difference_3600": 3600.0,
    }.items():
        augmented = np.column_stack([x_base, np.full(len(train_rows), value)])
        constant_rank_controls[label] = {
            "constant_value": value,
            "base_rank": base_rank,
            "augmented_rank": int(np.linalg.matrix_rank(augmented)),
            "rank_increased": int(np.linalg.matrix_rank(augmented)) > base_rank,
            "exact_scalar_multiple_of_intercept": bool(np.all(augmented[:, -1] == value * augmented[:, 0])),
        }

    rank_controls = {
        "record_id": RECORD_ID,
        "scenario_designs": rank_rows,
        "train_only_refit_prediction_invariance": refit_invariance,
        "global_constant_feature_controls": constant_rank_controls,
        "all_global_constants_rejected_as_independent_features": all(
            not row["rank_increased"] and row["exact_scalar_multiple_of_intercept"]
            for row in constant_rank_controls.values()
        ),
    }
    write_json(HERE / "CR120Q_rank_controls.json", rank_controls)

    direct_candidate_keys = [
        (surface, scenario)
        for surface in ("FROZEN_COEFFICIENT_TRANSFER", "FIXED_ZERO_FREE_SURFACE")
        for scenario in ("SHEET81_P9G0_REMOVED_12550P5", "SHEET100_P9G0_REMOVED_16200")
    ]
    direct_readouts: list[dict[str, Any]] = []
    for surface, scenario in direct_candidate_keys:
        candidate = metric_records[(surface, scenario, TEST_SPLIT)]
        baseline = metric_records[(surface, "BASELINE_REGISTERED_M126", TEST_SPLIT)]
        delta_rms = baseline["rms_MeV"] - candidate["rms_MeV"]
        delta_mae = baseline["mae_MeV"] - candidate["mae_MeV"]
        direction, material = classify(delta_rms, delta_mae)
        direct_readouts.append(
            {
                "surface": surface,
                "scenario": scenario,
                "holdout_RMS_MeV": candidate["rms_MeV"],
                "holdout_MAE_MeV": candidate["mae_MeV"],
                "delta_RMS_MeV_vs_M126": delta_rms,
                "delta_MAE_MeV_vs_M126": delta_mae,
                "direction": direction,
                "material_improvement": material,
            }
        )

    any_material = any(row["material_improvement"] for row in direct_readouts)
    mixed_material = any(
        row["delta_RMS_MeV_vs_M126"] >= 0.01 and row["delta_MAE_MeV_vs_M126"] < -1e-9
        for row in direct_readouts
    )
    gates_pass = (
        all(check["pass"] for check in source_checks)
        and reconstruction["exact_p9_g0_relation_pass"]
        and reconstruction["all_ten_parent_rows_retained_in_both"]
        and reproduction_pass
        and len(train_rows) == 49
        and len(test_rows) == 20
        and rank_controls["all_global_constants_rejected_as_independent_features"]
    )
    if not gates_pass:
        overall_verdict = "FAIL_INVALID_BINDING_MAGNITUDE_COMPARISON"
    elif any_material:
        overall_verdict = "PASS_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT"
    elif mixed_material:
        overall_verdict = "BOUNDARY_MIXED_BINDING_MAGNITUDE_RESPONSE"
    else:
        overall_verdict = "PASS_NO_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT"

    wrong_controls = {
        "record_id": RECORD_ID,
        "whole_roster_sums_used": True,
        "means_used": False,
        "holdout_rows_used_in_fit": 0,
        "holdout_targets_used_in_scenario_construction": False,
        "isotope_to_QP093A_map_invented": False,
        "qA_or_one_ninth_used": False,
        "W9_identity_used": False,
        "all_depth_p9_relation_used": False,
        "as_saved_12600_reported_as_p9_g0_removed": False,
        "CR242_artifacts_modified": False,
        "global_constant_features_rejected": rank_controls["all_global_constants_rejected_as_independent_features"],
        "training_error_used_as_improvement_verdict": False,
        "every_scenario_reported": True,
    }
    write_json(HERE / "CR120Q_wrong_controls.json", wrong_controls)

    summary = {
        "record_id": RECORD_ID,
        "task": TASK,
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "precommit_sha256": sha256(PRECOMMIT),
        "source_count": len(source_checks),
        "all_sources_verified": all(check["pass"] for check in source_checks),
        "spreadsheet_reconstruction": reconstruction,
        "binding_data": {
            "train_rows": len(train_rows),
            "holdout_rows": len(test_rows),
            "holdout_fit_rows": 0,
            "U_TO_MEV": U_TO_MEV,
        },
        "baseline_reproduction": {**reproduction, "pass": reproduction_pass},
        "direct_p9_g0_removed_holdout_readouts": direct_readouts,
        "all_global_constants_rejected_as_independent_features": rank_controls["all_global_constants_rejected_as_independent_features"],
        "overall_verdict": overall_verdict,
    }
    write_json(HERE / "CR120Q_summary.json", summary)

    def holdout_row(surface: str, scenario: str) -> dict[str, Any]:
        candidate = metric_records[(surface, scenario, TEST_SPLIT)]
        baseline = metric_records[(surface, "BASELINE_REGISTERED_M126", TEST_SPLIT)]
        delta_rms = baseline["rms_MeV"] - candidate["rms_MeV"]
        delta_mae = baseline["mae_MeV"] - candidate["mae_MeV"]
        direction, material = classify(delta_rms, delta_mae) if scenario != "BASELINE_REGISTERED_M126" else ("BASELINE", False)
        return {
            "rms": candidate["rms_MeV"],
            "mae": candidate["mae_MeV"],
            "delta_rms": delta_rms,
            "delta_mae": delta_mae,
            "direction": direction,
            "material": material,
        }

    result_lines = [
        "# CR120Q Result",
        "",
        "## Verdict",
        "",
        f"`{overall_verdict}`",
        "",
        "## Direct answer",
        "",
    ]
    if overall_verdict == "PASS_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT":
        result_lines.append("Yes. At least one specifically p9,g0-corrected whole-sheet sum materially lowered untouched holdout binding residual magnitudes under a direct predeclared surface.")
    elif overall_verdict == "PASS_NO_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT":
        result_lines.append("No. The new whole-sheet sums were run, but neither specifically p9,g0-corrected sum materially lowered untouched holdout binding residual magnitudes under the direct predeclared surfaces.")
    elif overall_verdict == "BOUNDARY_MIXED_BINDING_MAGNITUDE_RESPONSE":
        result_lines.append("Mixed. A corrected sum lowered holdout RMS materially but worsened MAE, so the magnitude response did not earn an improvement verdict.")
    else:
        result_lines.append("The comparison failed a frozen source, split, reproduction, scope, or leakage gate and cannot answer the magnitude question.")

    result_lines.extend(
        [
            "",
            "## Holdout readout (MeV)",
            "",
            "| surface | scenario | RMS | MAE | delta RMS vs M=126 | delta MAE vs M=126 | direction | material |",
            "|---|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for surface in surfaces:
        for scenario in SCENARIO_ORDER:
            values = holdout_row(surface, scenario)
            result_lines.append(
                f"| `{surface}` | `{scenario}` | {values['rms']:.9f} | {values['mae']:.9f} | {values['delta_rms']:.9f} | {values['delta_mae']:.9f} | `{values['direction']}` | `{str(values['material']).lower()}` |"
            )

    result_lines.extend(
        [
            "",
            "## Source and split checks",
            "",
            f"- Live 100-row sum reconstructed exactly: `{reconstruction['roster100_sum_M_native']}`.",
            f"- Live 81-row as-saved sum reconstructed exactly: `{reconstruction['roster81_sum_M_native_as_saved']}`.",
            f"- Specific remaining p9,g0 removal from the 81-row sheet: `{reconstruction['roster81_sum_M_native_as_saved']} - {reconstruction['roster81_retained_p9_g0_sum']} = {reconstruction['roster81_sum_after_specific_p9_g0_removal']}`.",
            "- All arithmetic used whole-roster sums; no mean was used.",
            f"- Frozen split: `{len(train_rows)}` training rows and `{len(test_rows)}` untouched holdout rows; holdout fit rows: `0`.",
            f"- CR242 baseline reproduction: `{'PASS' if reproduction_pass else 'FAIL'}`.",
            "",
            "## Interpretation",
            "",
            "Surface A answers direct substitution with the original CR242 coefficients held fixed. Surface B answers whether training-only coefficient refitting extracts any new predictive shape. Surface C challenges the fixed zero-free magnitude formula. The global sums were also tested as additive features and rejected because each is an exact scalar multiple of the intercept.",
            "",
            "This result measures numerical holdout response only. It does not install the sums as a new registered M value or create the still-missing isotope-to-QP093A occupancy map.",
        ]
    )
    (HERE / "CR120Q_result.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    hash_targets = [
        "CR120Q_SOURCE_MANIFEST.csv",
        "CR120Q_PRECOMMIT.md",
        "CR120Q_PRECOMMIT.sha256.txt",
        "CR120Q_runner.py",
        "CR120Q_scale_scenarios.csv",
        "CR120Q_metrics.csv",
        "CR120Q_predictions.csv",
        "CR120Q_coefficients.csv",
        "CR120Q_rank_controls.json",
        "CR120Q_wrong_controls.json",
        "CR120Q_summary.json",
        "CR120Q_result.md",
    ]
    (HERE / "HASHES.txt").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in hash_targets),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
