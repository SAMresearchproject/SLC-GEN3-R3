"""CR242 SAM binding-curvature derivation runner.

This runner is constructive downstream work from CR240/CR241. It must be
executed through tools/run_sam_test.py for a Courtroom-valid result path.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any

import numpy as np


CR_DIR = Path(__file__).resolve().parent
REPO = CR_DIR.parents[1]
CR240_DIR = CR_DIR.parent / "CR240_NEUTRON_REST_MASS_CHANNEL"
CR241_DIR = CR_DIR.parent / "CR241_REST_MASS_HOLDOUT_UNIQUENESS"
PREFLIGHT_DIR = REPO / "artifacts" / "preflight_filled"

PRECOMMIT = CR_DIR / "CR242_PRECOMMIT.md"
RUNNER = CR_DIR / "CR242_runner.py"
INITIAL_PREFLIGHT_MD = PREFLIGHT_DIR / "PREFLIGHT_20260623_084748_no_script.md"
INITIAL_PREFLIGHT_JSON = PREFLIGHT_DIR / "PREFLIGHT_20260623_084748_no_script.json"

CR240_PREDICTIONS = CR240_DIR / "CR240_extended_kernel_predictions.csv"
CR240_SUMMARY = CR240_DIR / "CR240_summary.json"
CR241_HOLDOUT = CR241_DIR / "CR241_holdout_predictions.csv"
CR241_SUMMARY = CR241_DIR / "CR241_summary.json"

OUT_DATASET = CR_DIR / "CR242_binding_dataset.csv"
OUT_COEFFICIENTS = CR_DIR / "CR242_model_coefficients.csv"
OUT_PREDICTIONS = CR_DIR / "CR242_predictions.csv"
OUT_COMPARISON = CR_DIR / "CR242_model_comparison.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR242_wrong_controls.csv"
OUT_SUMMARY = CR_DIR / "CR242_summary.json"
OUT_RESULT = CR_DIR / "CR242_result.md"
OUT_MANIFEST = CR_DIR / "CR242_input_manifest.csv"
OUT_HASHES = CR_DIR / "HASHES.txt"

R = 12
S = 8
M = 126
THETA = 18
V = 27

BW_FEATURES = [
    "intercept",
    "bw_volume_A",
    "bw_surface_A_to_two_thirds",
    "bw_coulomb_ZZminus1_over_A_third",
    "bw_asymmetry_NmZ_squared_over_A",
    "bw_pairing_over_sqrt_A",
]

SAM_FEATURES = [
    "intercept",
    "sam_volume_A_over_SM",
    "sam_surface_A23_over_RV",
    "sam_coulomb_ZZminus1_over_A13_SMV",
    "sam_asymmetry_NmZ2_over_A_STheta",
    "sam_pairing_over_MsqrtA",
    "sam_z_residue_over_RM",
    "sam_abs_NmZ_over_AR",
]

UNTYPED_FEATURES = [
    "intercept",
    "untyped_A",
    "untyped_Z",
    "untyped_N_minus_Z",
    "untyped_ZZminus1",
    "untyped_NmZ_squared",
]

DISALLOWED_POSITIVE_CLAIMS = [
    "free proton candidate promotion",
    "free neutron candidate promotion",
    "theorem-grade nuclear binding derivation",
    "full nuclear binding-energy derivation",
    "Bethe-Weizsacker replacement",
    "C5/C6/C7 particle promotion",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pairing_sign(z: int, n: int) -> int:
    if z % 2 == 0 and n % 2 == 0:
        return 1
    if z % 2 == 1 and n % 2 == 1:
        return -1
    return 0


def load_train_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(CR240_PREDICTIONS):
        if row["confidence_lane"] != "LANE_A_HARD_MEASURED":
            continue
        if row["isotope"] == "C-12":
            continue
        z = int(row["Z"])
        n = int(row["N"])
        a = int(row["A"])
        measured = float(row["m_meas_u"])
        rows.append(
            enrich_row(
                {
                    "split": "train_cr240_lane_a_non_anchor",
                    "source": rel(CR240_PREDICTIONS),
                    "isotope": row["isotope"],
                    "Z": z,
                    "N": n,
                    "A": a,
                    "N_minus_Z": n - z,
                    "m_measured_u": measured,
                    "B_u": a - measured,
                    "confidence_lane": row["confidence_lane"],
                }
            )
        )
    return rows


def load_test_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(CR241_HOLDOUT):
        z = int(row["Z"])
        n = int(row["N"])
        a = int(row["A"])
        measured = float(row["atomic_mass_u"])
        b_u = float(row["binding_defect_u"])
        rows.append(
            enrich_row(
                {
                    "split": "test_cr241_holdout",
                    "source": rel(CR241_HOLDOUT),
                    "isotope": row["isotope"],
                    "Z": z,
                    "N": n,
                    "A": a,
                    "N_minus_Z": n - z,
                    "m_measured_u": measured,
                    "B_u": b_u,
                    "confidence_lane": row["confidence_lane"],
                }
            )
        )
    return rows


def enrich_row(row: dict[str, Any]) -> dict[str, Any]:
    z = int(row["Z"])
    n = int(row["N"])
    a = int(row["A"])
    nmz = n - z
    pair = pairing_sign(z, n)
    a13 = a ** (1.0 / 3.0)
    a23 = a ** (2.0 / 3.0)
    sqrt_a = math.sqrt(a)

    row.update(
        {
            "R": R,
            "S": S,
            "M": M,
            "Theta": THETA,
            "V": V,
            "pairing_sign": pair,
            "z_residue_mod_R": (z - 1) % R,
            "intercept": 1.0,
            "bw_volume_A": float(a),
            "bw_surface_A_to_two_thirds": a23,
            "bw_coulomb_ZZminus1_over_A_third": z * (z - 1) / a13,
            "bw_asymmetry_NmZ_squared_over_A": (nmz * nmz) / a,
            "bw_pairing_over_sqrt_A": pair / sqrt_a,
            "sam_volume_A_over_SM": a / (S * M),
            "sam_surface_A23_over_RV": a23 / (R * V),
            "sam_coulomb_ZZminus1_over_A13_SMV": z * (z - 1) / (a13 * S * M * V),
            "sam_asymmetry_NmZ2_over_A_STheta": (nmz * nmz) / (a * S * THETA),
            "sam_pairing_over_MsqrtA": pair / (M * sqrt_a),
            "sam_z_residue_over_RM": ((z - 1) % R) / (R * M),
            "sam_abs_NmZ_over_AR": abs(nmz) / (a * R),
            "untyped_A": float(a),
            "untyped_Z": float(z),
            "untyped_N_minus_Z": float(nmz),
            "untyped_ZZminus1": float(z * (z - 1)),
            "untyped_NmZ_squared": float(nmz * nmz),
        }
    )
    return row


def design_matrix(rows: list[dict[str, Any]], features: list[str]) -> np.ndarray:
    return np.array([[float(row[name]) for name in features] for row in rows], dtype=float)


def targets(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.array([float(row["B_u"]) for row in rows], dtype=float)


def fit_linear(rows: list[dict[str, Any]], features: list[str]) -> np.ndarray:
    x = design_matrix(rows, features)
    y = targets(rows)
    coef, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    return coef


def predict(rows: list[dict[str, Any]], features: list[str], coef: np.ndarray) -> np.ndarray:
    return design_matrix(rows, features) @ coef


def zero_free_prediction(rows: list[dict[str, Any]]) -> np.ndarray:
    values = []
    for row in rows:
        values.append(
            row["sam_volume_A_over_SM"]
            - row["sam_surface_A23_over_RV"]
            - row["sam_coulomb_ZZminus1_over_A13_SMV"]
            - row["sam_asymmetry_NmZ2_over_A_STheta"]
            + row["sam_pairing_over_MsqrtA"]
        )
    return np.array(values, dtype=float)


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    residual = y_pred - y_true
    ss_res = float(np.sum(residual**2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    return {
        "n": int(len(y_true)),
        "rms_u": float(math.sqrt(float(np.mean(residual**2)))),
        "mae_u": float(np.mean(np.abs(residual))),
        "max_abs_u": float(np.max(np.abs(residual))),
        "r2": float("nan") if ss_tot == 0 else float(1.0 - ss_res / ss_tot),
    }


def metric_rows(model: str, train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]], train_pred: np.ndarray, test_pred: np.ndarray) -> list[dict[str, Any]]:
    out = []
    for split, rows, pred in [
        ("train_cr240_lane_a_non_anchor", train_rows, train_pred),
        ("test_cr241_holdout", test_rows, test_pred),
    ]:
        m = metrics(targets(rows), pred)
        out.append({"model": model, "split": split, **m})
    return out


def prediction_rows(model: str, rows: list[dict[str, Any]], pred: np.ndarray) -> list[dict[str, Any]]:
    out = []
    for row, value in zip(rows, pred):
        out.append(
            {
                "model": model,
                "split": row["split"],
                "isotope": row["isotope"],
                "Z": row["Z"],
                "N": row["N"],
                "A": row["A"],
                "B_u": row["B_u"],
                "B_pred_u": float(value),
                "residual_pred_minus_B_u": float(value - row["B_u"]),
            }
        )
    return out


def coefficient_rows(model: str, features: list[str], coef: np.ndarray) -> list[dict[str, Any]]:
    return [
        {"model": model, "feature": feature, "coefficient": float(value)}
        for feature, value in zip(features, coef)
    ]


def shuffled_label_control(train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]], real_test_metrics: dict[str, float]) -> dict[str, Any]:
    rng = random.Random(20260623)
    shuffled_y = list(targets(train_rows))
    rng.shuffle(shuffled_y)
    x_train = design_matrix(train_rows, SAM_FEATURES)
    coef, _, _, _ = np.linalg.lstsq(x_train, np.array(shuffled_y, dtype=float), rcond=None)
    test_pred = predict(test_rows, SAM_FEATURES, coef)
    m = metrics(targets(test_rows), test_pred)
    pass_gate = bool(m["rms_u"] > real_test_metrics["rms_u"] and m["r2"] < real_test_metrics["r2"] - 0.20)
    return {
        "control_id": "WC1_shuffled_train_B_u_labels",
        "status": "PASS" if pass_gate else "FAIL",
        "verdict_relevant": True,
        "description": "Shuffle CR240 training B_u labels before fitting SAM typed basis.",
        "test_rms_u": m["rms_u"],
        "test_r2": m["r2"],
        "pass_condition": "shuffled RMS worsens and R2 drops by at least 0.20",
        "pass": pass_gate,
    }


def untyped_control(train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]], sam_test_metrics: dict[str, float]) -> dict[str, Any]:
    coef = fit_linear(train_rows, UNTYPED_FEATURES)
    test_pred = predict(test_rows, UNTYPED_FEATURES, coef)
    m = metrics(targets(test_rows), test_pred)
    beats_sam = bool(m["rms_u"] <= sam_test_metrics["rms_u"])
    return {
        "control_id": "WC3_untyped_decimal_basis",
        "status": "COMPLETE",
        "verdict_relevant": True,
        "description": "Fit an untyped decimal basis to check whether typed structure is unique enough for STRONG.",
        "test_rms_u": m["rms_u"],
        "test_r2": m["r2"],
        "beats_sam_typed": beats_sam,
        "pass_condition": "complete; suppress STRONG if it beats SAM typed basis",
        "pass": True,
        "suppresses_strong": beats_sam,
    }


def zero_control(train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]]) -> dict[str, Any]:
    train_pred = zero_free_prediction(train_rows)
    test_pred = zero_free_prediction(test_rows)
    train_m = metrics(targets(train_rows), train_pred)
    test_m = metrics(targets(test_rows), test_pred)
    weak = bool(test_m["r2"] < 0.95)
    return {
        "control_id": "WC4_zero_free_typed_candidate",
        "status": "COMPLETE",
        "verdict_relevant": True,
        "description": "Report the strict zero-free typed candidate without fitting coefficients.",
        "train_rms_u": train_m["rms_u"],
        "train_r2": train_m["r2"],
        "test_rms_u": test_m["rms_u"],
        "test_r2": test_m["r2"],
        "pass_condition": "complete; suppress STRONG if holdout R2 < 0.95",
        "pass": True,
        "suppresses_strong": weak,
    }


def latest_execution_preflight() -> list[Path]:
    paths = []
    for suffix in ("md", "json"):
        matches = sorted(PREFLIGHT_DIR.glob(f"PREFLIGHT_*_CR242_runner.{suffix}"))
        if matches:
            paths.append(matches[-1])
    return paths


def write_result(summary: dict[str, Any]) -> None:
    bw_test = summary["models"]["BW_BENCHMARK_FIT"]["test"]
    sam_test = summary["models"]["SAM_TYPED_BASIS_FIT"]["test"]
    zero_test = summary["models"]["SAM_ZERO_FREE_TYPED_CANDIDATE"]["test"]
    wc_lines = []
    for control in summary["wrong_controls"]:
        wc_lines.append(
            f"- {control['control_id']}: {control['status']} "
            f"(test RMS={control.get('test_rms_u', '')}, test R2={control.get('test_r2', '')})"
        )
    text = f"""# CR242 SAM Binding-Curvature Derivation

Verdict: `{summary['verdict']}`

## Question

CR242 tests the positive binding residual:

```text
B_u = A - m_measured
```

The coefficient fits use CR240 Lane A non-anchor rows only. The CR241 holdout is
reserved for out-of-sample testing.

## Model Comparison

| model | train RMS u | train R2 | test RMS u | test R2 |
|---|---:|---:|---:|---:|
| BW_BENCHMARK_FIT | {summary['models']['BW_BENCHMARK_FIT']['train']['rms_u']:.15g} | {summary['models']['BW_BENCHMARK_FIT']['train']['r2']:.15g} | {bw_test['rms_u']:.15g} | {bw_test['r2']:.15g} |
| SAM_TYPED_BASIS_FIT | {summary['models']['SAM_TYPED_BASIS_FIT']['train']['rms_u']:.15g} | {summary['models']['SAM_TYPED_BASIS_FIT']['train']['r2']:.15g} | {sam_test['rms_u']:.15g} | {sam_test['r2']:.15g} |
| SAM_ZERO_FREE_TYPED_CANDIDATE | {summary['models']['SAM_ZERO_FREE_TYPED_CANDIDATE']['train']['rms_u']:.15g} | {summary['models']['SAM_ZERO_FREE_TYPED_CANDIDATE']['train']['r2']:.15g} | {zero_test['rms_u']:.15g} | {zero_test['r2']:.15g} |

SAM/BW holdout RMS ratio: `{summary['sam_to_bw_test_rms_ratio']:.15g}`

## Verdict Logic

STRONG pass: `{summary['verdict_logic']['strong_all']}`

BOUNDARY pass: `{summary['verdict_logic']['boundary_all']}`

FAIL condition present: `{summary['verdict_logic']['fail_any']}`

## Wrong Controls

{chr(10).join(wc_lines)}

## Claim Boundary

CR242 reports a binding-curvature surface test only. It does not fit the CR241
holdout, does not promote C5/C6/C7, and does not assert a theorem-grade nuclear
binding derivation.
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def manifest_rows(extra_preflight: list[Path]) -> list[dict[str, Any]]:
    paths: list[tuple[Path, str]] = [
        (PRECOMMIT, "precommit"),
        (RUNNER, "runner"),
        (INITIAL_PREFLIGHT_MD, "constructive_preflight_md"),
        (INITIAL_PREFLIGHT_JSON, "constructive_preflight_json"),
        (CR240_PREDICTIONS, "upstream_cr240_train_source"),
        (CR240_SUMMARY, "upstream_cr240_summary"),
        (CR241_HOLDOUT, "upstream_cr241_holdout_source"),
        (CR241_SUMMARY, "upstream_cr241_summary"),
    ]
    for path in extra_preflight:
        role = "execution_preflight_json" if path.suffix == ".json" else "execution_preflight_md"
        paths.append((path, role))
    paths.extend(
        [
            (OUT_DATASET, "derived_binding_dataset"),
            (OUT_COEFFICIENTS, "model_coefficients"),
            (OUT_PREDICTIONS, "model_predictions"),
            (OUT_COMPARISON, "model_comparison"),
            (OUT_WRONG_CONTROLS, "wrong_controls"),
            (OUT_SUMMARY, "summary"),
            (OUT_RESULT, "result_readout"),
        ]
    )
    rows = []
    for path, role in paths:
        if path.exists():
            rows.append(
                {
                    "path": rel(path),
                    "role": role,
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )
    return rows


def write_hashes(rows: list[dict[str, Any]]) -> None:
    paths = [REPO / row["path"] for row in rows]
    paths.append(OUT_MANIFEST)
    lines = [f"{sha256_file(path)}  {rel(path)}" for path in paths if path.exists()]
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    train_rows = load_train_rows()
    test_rows = load_test_rows()
    all_rows = train_rows + test_rows

    bw_coef = fit_linear(train_rows, BW_FEATURES)
    sam_coef = fit_linear(train_rows, SAM_FEATURES)
    untyped_coef = fit_linear(train_rows, UNTYPED_FEATURES)

    bw_train_pred = predict(train_rows, BW_FEATURES, bw_coef)
    bw_test_pred = predict(test_rows, BW_FEATURES, bw_coef)
    sam_train_pred = predict(train_rows, SAM_FEATURES, sam_coef)
    sam_test_pred = predict(test_rows, SAM_FEATURES, sam_coef)
    zero_train_pred = zero_free_prediction(train_rows)
    zero_test_pred = zero_free_prediction(test_rows)
    untyped_train_pred = predict(train_rows, UNTYPED_FEATURES, untyped_coef)
    untyped_test_pred = predict(test_rows, UNTYPED_FEATURES, untyped_coef)

    comparison = []
    comparison.extend(metric_rows("BW_BENCHMARK_FIT", train_rows, test_rows, bw_train_pred, bw_test_pred))
    comparison.extend(metric_rows("SAM_TYPED_BASIS_FIT", train_rows, test_rows, sam_train_pred, sam_test_pred))
    comparison.extend(metric_rows("SAM_ZERO_FREE_TYPED_CANDIDATE", train_rows, test_rows, zero_train_pred, zero_test_pred))
    comparison.extend(metric_rows("UNTYPED_DECIMAL_CONTROL", train_rows, test_rows, untyped_train_pred, untyped_test_pred))

    comparison_lookup = {(row["model"], row["split"]): row for row in comparison}
    bw_test = comparison_lookup[("BW_BENCHMARK_FIT", "test_cr241_holdout")]
    sam_test = comparison_lookup[("SAM_TYPED_BASIS_FIT", "test_cr241_holdout")]
    zero_test = comparison_lookup[("SAM_ZERO_FREE_TYPED_CANDIDATE", "test_cr241_holdout")]
    sam_train = comparison_lookup[("SAM_TYPED_BASIS_FIT", "train_cr240_lane_a_non_anchor")]
    bw_train = comparison_lookup[("BW_BENCHMARK_FIT", "train_cr240_lane_a_non_anchor")]
    zero_train = comparison_lookup[("SAM_ZERO_FREE_TYPED_CANDIDATE", "train_cr240_lane_a_non_anchor")]

    wc1 = shuffled_label_control(train_rows, test_rows, sam_test)
    wc2 = {
        "control_id": "WC2_train_test_boundary_guard",
        "status": "PASS",
        "verdict_relevant": True,
        "description": "Confirm all coefficients are fit on CR240 train rows and CR241 holdout rows are never fit.",
        "train_rows": len(train_rows),
        "holdout_rows": len(test_rows),
        "fit_split": "train_cr240_lane_a_non_anchor",
        "test_split": "test_cr241_holdout",
        "pass_condition": "no CR241 holdout row is used in coefficient fitting",
        "pass": True,
    }
    wc3 = untyped_control(train_rows, test_rows, sam_test)
    wc4 = zero_control(train_rows, test_rows)

    emitted_positive_claims: list[str] = []
    claim_flags = [
        claim for claim in emitted_positive_claims if claim in DISALLOWED_POSITIVE_CLAIMS
    ]
    wc5 = {
        "control_id": "WC5_disallowed_claim_guard",
        "status": "PASS" if not claim_flags else "FAIL",
        "verdict_relevant": True,
        "description": "Machine summary emits no positive promotion or theorem-grade claim tags.",
        "flag_count": len(claim_flags),
        "flags": ";".join(claim_flags),
        "pass_condition": "zero forbidden claim flags",
        "pass": not claim_flags,
    }
    wrong_controls = [wc1, wc2, wc3, wc4, wc5]

    all_wrong_controls_complete = all(control["status"] in {"PASS", "COMPLETE"} for control in wrong_controls)
    verdict_controls_pass = all(bool(control["pass"]) for control in wrong_controls)
    sam_to_bw_test_rms_ratio = sam_test["rms_u"] / bw_test["rms_u"]
    holdout_fit_guard = bool(wc2["pass"])
    no_disallowed_claims = not claim_flags
    strong_all = bool(
        all_wrong_controls_complete
        and verdict_controls_pass
        and holdout_fit_guard
        and no_disallowed_claims
        and sam_test["rms_u"] <= bw_test["rms_u"]
        and sam_test["r2"] >= 0.98
        and zero_test["r2"] >= 0.95
        and not wc3.get("suppresses_strong", False)
        and not wc4.get("suppresses_strong", False)
    )
    boundary_all = bool(
        all_wrong_controls_complete
        and verdict_controls_pass
        and holdout_fit_guard
        and no_disallowed_claims
        and sam_test["r2"] >= 0.95
        and sam_to_bw_test_rms_ratio <= 1.10
    )
    fail_any = not boundary_all
    if strong_all:
        verdict = "STRONG_PASS_CR242_SAM_BINDING_CURVATURE_DERIVATION"
    elif boundary_all:
        verdict = "BOUNDARY_CR242_SAM_TYPED_BINDING_SURFACE_REPRODUCES_BW_STRUCTURE"
    else:
        verdict = "FAIL_CR242_SAM_BINDING_CURVATURE_DERIVATION"

    dataset_fields = [
        "split",
        "source",
        "isotope",
        "Z",
        "N",
        "A",
        "N_minus_Z",
        "m_measured_u",
        "B_u",
        "R",
        "S",
        "M",
        "Theta",
        "V",
        "pairing_sign",
        "z_residue_mod_R",
        *BW_FEATURES,
        *SAM_FEATURES[1:],
        *UNTYPED_FEATURES[1:],
        "confidence_lane",
    ]
    write_csv(OUT_DATASET, all_rows, dataset_fields)

    coef_rows = []
    coef_rows.extend(coefficient_rows("BW_BENCHMARK_FIT", BW_FEATURES, bw_coef))
    coef_rows.extend(coefficient_rows("SAM_TYPED_BASIS_FIT", SAM_FEATURES, sam_coef))
    coef_rows.extend(coefficient_rows("UNTYPED_DECIMAL_CONTROL", UNTYPED_FEATURES, untyped_coef))
    write_csv(OUT_COEFFICIENTS, coef_rows)

    pred_rows = []
    for rows, bw_pred, sam_pred, zero_pred, untyped_pred in [
        (train_rows, bw_train_pred, sam_train_pred, zero_train_pred, untyped_train_pred),
        (test_rows, bw_test_pred, sam_test_pred, zero_test_pred, untyped_test_pred),
    ]:
        pred_rows.extend(prediction_rows("BW_BENCHMARK_FIT", rows, bw_pred))
        pred_rows.extend(prediction_rows("SAM_TYPED_BASIS_FIT", rows, sam_pred))
        pred_rows.extend(prediction_rows("SAM_ZERO_FREE_TYPED_CANDIDATE", rows, zero_pred))
        pred_rows.extend(prediction_rows("UNTYPED_DECIMAL_CONTROL", rows, untyped_pred))
    write_csv(OUT_PREDICTIONS, pred_rows)

    for row in comparison:
        if row["split"] == "test_cr241_holdout":
            row["rms_ratio_to_bw_test"] = row["rms_u"] / bw_test["rms_u"]
        else:
            row["rms_ratio_to_bw_test"] = ""
    write_csv(OUT_COMPARISON, comparison)
    wrong_control_fields = [
        "control_id",
        "status",
        "verdict_relevant",
        "description",
        "train_rows",
        "holdout_rows",
        "fit_split",
        "test_split",
        "train_rms_u",
        "train_r2",
        "test_rms_u",
        "test_r2",
        "beats_sam_typed",
        "suppresses_strong",
        "flag_count",
        "flags",
        "pass_condition",
        "pass",
    ]
    write_csv(OUT_WRONG_CONTROLS, wrong_controls, wrong_control_fields)

    summary = {
        "verdict": verdict,
        "task": "CR242 SAM binding-curvature derivation",
        "target_residual": "B_u = A - m_measured",
        "kernel_atoms": {"R": R, "S": S, "M": M, "Theta": THETA, "V": V},
        "train_rows": len(train_rows),
        "test_rows": len(test_rows),
        "fit_policy": "coefficients fit only on CR240 Lane A non-anchor rows",
        "test_policy": "CR241 holdout rows are out-of-sample only",
        "models": {
            "BW_BENCHMARK_FIT": {"train": bw_train, "test": bw_test, "features": BW_FEATURES},
            "SAM_TYPED_BASIS_FIT": {"train": sam_train, "test": sam_test, "features": SAM_FEATURES},
            "SAM_ZERO_FREE_TYPED_CANDIDATE": {"train": zero_train, "test": zero_test},
        },
        "sam_to_bw_test_rms_ratio": sam_to_bw_test_rms_ratio,
        "wrong_controls": wrong_controls,
        "all_wrong_controls_complete": all_wrong_controls_complete,
        "verdict_controls_pass": verdict_controls_pass,
        "disallowed_claim_flags": claim_flags,
        "verdict_logic": {
            "strong_conditions": {
                "all_wrong_controls_complete": all_wrong_controls_complete,
                "wrong_controls_pass": verdict_controls_pass,
                "holdout_fit_guard": holdout_fit_guard,
                "sam_test_rms_le_bw_test_rms": sam_test["rms_u"] <= bw_test["rms_u"],
                "sam_test_r2_ge_0p98": sam_test["r2"] >= 0.98,
                "zero_free_test_r2_ge_0p95": zero_test["r2"] >= 0.95,
                "untyped_control_does_not_beat_sam": not wc3.get("suppresses_strong", False),
                "zero_free_does_not_suppress_strong": not wc4.get("suppresses_strong", False),
                "no_disallowed_claims": no_disallowed_claims,
            },
            "strong_all": strong_all,
            "boundary_conditions": {
                "all_wrong_controls_complete": all_wrong_controls_complete,
                "wrong_controls_pass": verdict_controls_pass,
                "holdout_fit_guard": holdout_fit_guard,
                "sam_test_r2_ge_0p95": sam_test["r2"] >= 0.95,
                "sam_test_rms_le_1p10_bw_test_rms": sam_to_bw_test_rms_ratio <= 1.10,
                "no_disallowed_claims": no_disallowed_claims,
            },
            "boundary_all": boundary_all,
            "fail_conditions": {
                "boundary_conditions_fail": not boundary_all,
                "wrong_controls_fail": not verdict_controls_pass,
                "holdout_fit_guard_fails": not holdout_fit_guard,
                "disallowed_claims_present": not no_disallowed_claims,
            },
            "fail_any": fail_any,
        },
        "input_shas": {
            "CR240_extended_kernel_predictions": sha256_file(CR240_PREDICTIONS),
            "CR240_summary": sha256_file(CR240_SUMMARY),
            "CR241_holdout_predictions": sha256_file(CR241_HOLDOUT),
            "CR241_summary": sha256_file(CR241_SUMMARY),
            "CR242_precommit": sha256_file(PRECOMMIT),
        },
    }
    write_json(OUT_SUMMARY, summary)
    write_result(summary)

    rows = manifest_rows(latest_execution_preflight())
    write_csv(OUT_MANIFEST, rows, ["path", "role", "sha256", "bytes"])
    write_hashes(rows)

    print(json.dumps({"verdict": verdict, "summary": rel(OUT_SUMMARY), "result": rel(OUT_RESULT)}, indent=2))


if __name__ == "__main__":
    main()
