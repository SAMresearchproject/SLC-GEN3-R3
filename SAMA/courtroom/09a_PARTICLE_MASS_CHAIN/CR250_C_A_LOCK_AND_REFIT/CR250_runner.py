"""CR250 — c_A Lock-and-Refit runner.

Locks c_A = 1/(S*L) = 1/1296 and refits the remaining 4 binding coefficients
(c_V, c_S, c_C, c_P) on Lane A train.  Compares to free-c_A baseline.
Runs 6 wrong controls per round5.pdf: alternative typed values for c_A.
"""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).parent
TRAIN_CSV = HERE / "CR250_train_lane_a.csv"
TEST_CSV = HERE / "CR250_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR250_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "f2552f61ea6621564f94b52794def59d8f253549eb1a65a3dfb4ab9fd56b8626"

KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R, D, S, M_LEDGER, L_LEDGER, V_LEDGER, THETA = 12, 3, 8, 126, 162, 27, 18
U_TO_MEV = 931.49410242

# Locked c_A candidate
C_A_LOCKED = Fraction(1, S * L_LEDGER)  # = 1/1296


def sha256(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def read_isotope_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open() as f:
        for row in csv.DictReader(f):
            row["Z"] = int(row["Z"]); row["N"] = int(row["N"]); row["A"] = int(row["A"])
            row["atomic_mass_u"] = float(row["atomic_mass_u"])
            row["B_u"] = row["A"] - row["atomic_mass_u"]
            rows.append(row)
    return rows


def compute_features(rows: list[dict[str, Any]]) -> None:
    kappa_f = float(KAPPA); g_f = float(G)
    for r in rows:
        A, Z, N = r["A"], r["Z"], r["N"]
        Q_mass = 4 * A * kappa_f
        Q_sub = 8 * (Z * kappa_f + (N - Z) * g_f)
        r["Q_mass"] = Q_mass; r["Q_sub"] = Q_sub
        r["dQ"] = Q_mass - Q_sub
        r["asym_feature"] = (r["dQ"] ** 2) / Q_mass if Q_mass > 0 else 0.0
        if Z % 2 == 0 and N % 2 == 0:
            r["delta_pair"] = +1.0
        elif Z % 2 == 1 and N % 2 == 1:
            r["delta_pair"] = -1.0
        else:
            r["delta_pair"] = 0.0


def design_full5(rows: list[dict[str, Any]]) -> np.ndarray:
    """5-shape design matrix: [A, -A^(2/3), -Z(Z-1)/A^(1/3), -asym, +delta_pair]."""
    return np.array([
        [r["A"], -(r["A"] ** (2/3)), -(r["Z"]*(r["Z"]-1) / r["A"]**(1/3)),
         -r["asym_feature"], r["delta_pair"]]
        for r in rows
    ])


def design_4term(rows: list[dict[str, Any]]) -> np.ndarray:
    """4-shape design matrix (asymmetry removed; will be handled via fixed c_A)."""
    return np.array([
        [r["A"], -(r["A"] ** (2/3)), -(r["Z"]*(r["Z"]-1) / r["A"]**(1/3)),
         r["delta_pair"]]
        for r in rows
    ])


def fit_free(rows: list[dict[str, Any]]) -> dict[str, Any]:
    X = design_full5(rows); y = np.array([r["B_u"] for r in rows])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef; residual = pred - y
    ss_res = float(np.sum(residual ** 2)); ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return {
        "coef_names": ["c_V", "c_S", "c_C", "c_A", "c_P"],
        "coef": coef.tolist(),
        "rms_u": float(np.sqrt(np.mean(residual ** 2))),
        "rms_MeV": float(np.sqrt(np.mean(residual ** 2))) * U_TO_MEV,
        "R2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "n": len(rows), "pred": pred.tolist(),
    }


def fit_locked(rows: list[dict[str, Any]], c_A_locked: float) -> dict[str, Any]:
    """Lock c_A to a given value; refit c_V, c_S, c_C, c_P.

    The asymmetry term enters B_SAM as -c_A * asym_feature.  Move it to the
    LHS: B_u_obs + c_A_locked * asym_feature = c_V*A - c_S*A^(2/3)
                                              - c_C*Z(Z-1)/A^(1/3) + c_P*delta.
    """
    X = design_4term(rows)
    y = np.array([r["B_u"] + c_A_locked * r["asym_feature"] for r in rows])
    coef4, *_ = np.linalg.lstsq(X, y, rcond=None)
    # Reconstruct B_u_pred under the locked + refitted model:
    # pred_B_u = coef4 @ X_row - c_A_locked * asym_feature  (since asym enters with minus sign)
    pred_lhs = X @ coef4
    pred_B_u = pred_lhs - np.array([c_A_locked * r["asym_feature"] for r in rows])
    y_obs = np.array([r["B_u"] for r in rows])
    residual = pred_B_u - y_obs
    ss_res = float(np.sum(residual ** 2)); ss_tot = float(np.sum((y_obs - np.mean(y_obs)) ** 2))
    return {
        "coef_names_4": ["c_V", "c_S", "c_C", "c_P"],
        "coef4": coef4.tolist(),
        "c_A_locked": c_A_locked,
        "rms_u": float(np.sqrt(np.mean(residual ** 2))),
        "rms_MeV": float(np.sqrt(np.mean(residual ** 2))) * U_TO_MEV,
        "R2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "n": len(rows), "pred": pred_B_u.tolist(),
    }


def evaluate_locked_model_on(rows: list[dict[str, Any]],
                             coef4: list[float], c_A_locked: float) -> dict[str, Any]:
    """Evaluate the locked+refitted model on a different row set (e.g., test)."""
    X = design_4term(rows)
    pred_lhs = X @ np.array(coef4)
    pred_B_u = pred_lhs - np.array([c_A_locked * r["asym_feature"] for r in rows])
    y_obs = np.array([r["B_u"] for r in rows])
    residual = pred_B_u - y_obs
    ss_res = float(np.sum(residual ** 2)); ss_tot = float(np.sum((y_obs - np.mean(y_obs)) ** 2))
    return {
        "rms_u": float(np.sqrt(np.mean(residual ** 2))),
        "rms_MeV": float(np.sqrt(np.mean(residual ** 2))) * U_TO_MEV,
        "R2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "n": len(rows), "pred": pred_B_u.tolist(),
    }


def evaluate_free_model_on(rows: list[dict[str, Any]], coef5: list[float]) -> dict[str, Any]:
    X = design_full5(rows)
    pred = X @ np.array(coef5)
    y_obs = np.array([r["B_u"] for r in rows])
    residual = pred - y_obs
    ss_res = float(np.sum(residual ** 2)); ss_tot = float(np.sum((y_obs - np.mean(y_obs)) ** 2))
    return {
        "rms_u": float(np.sqrt(np.mean(residual ** 2))),
        "rms_MeV": float(np.sqrt(np.mean(residual ** 2))) * U_TO_MEV,
        "R2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "n": len(rows), "pred": pred.tolist(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text(""); return
    fieldnames: list[str] = []; seen: set[str] = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k); fieldnames.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in rows: w.writerow(r)


def main() -> None:
    actual_train = sha256(TRAIN_CSV); actual_test = sha256(TEST_CSV); actual_pre = sha256(PRECOMMIT_MD)
    if actual_train != EXPECTED_TRAIN_SHA:
        raise SystemExit(f"TRAIN SHA mismatch")
    if actual_test != EXPECTED_TEST_SHA:
        raise SystemExit(f"TEST SHA mismatch")
    if actual_pre != EXPECTED_PRECOMMIT_SHA:
        raise SystemExit(f"PRECOMMIT SHA mismatch")

    train_all = read_isotope_csv(TRAIN_CSV)
    test_all = read_isotope_csv(TEST_CSV)
    compute_features(train_all); compute_features(test_all)

    train_fit = [r for r in train_all if r["A"] != 12 and r["A"] >= 16 and r["N"] >= r["Z"]]
    test_eval = [r for r in test_all if r["N"] >= r["Z"]]

    # Baseline: free-c_A 5-term fit
    baseline = fit_free(train_fit)
    baseline_test = evaluate_free_model_on(test_eval, baseline["coef"])

    # Locked: c_A = 1/(S*L), refit 4 coefficients
    c_A_locked_value = float(C_A_LOCKED)
    locked = fit_locked(train_fit, c_A_locked_value)
    locked_test = evaluate_locked_model_on(test_eval, locked["coef4"], c_A_locked_value)

    # Wrong controls
    wc_specs = [
        ("WC-A1", "1/L         = 1/162",   Fraction(1, L_LEDGER)),
        ("WC-A2", "1/(S*M)     = 1/1008",  Fraction(1, S * M_LEDGER)),
        ("WC-A3", "1/(S*R^2)   = 1/1152",  Fraction(1, S * R * R)),
        ("WC-A4", "1/(R*L)     = 1/1944",  Fraction(1, R * L_LEDGER)),
        ("WC-A5", "2/(S*L)     = 2/1296",  Fraction(2, S * L_LEDGER)),
        ("WC-A6", "(1/2)/(S*L) = 1/2592",  Fraction(1, 2 * S * L_LEDGER)),
    ]
    wcs = []
    for label, desc, frac in wc_specs:
        cv = float(frac)
        fit_wc = fit_locked(train_fit, cv)
        eval_wc = evaluate_locked_model_on(test_eval, fit_wc["coef4"], cv)
        ratio_train = fit_wc["rms_u"] / locked["rms_u"] if locked["rms_u"] > 0 else float("inf")
        ratio_test = eval_wc["rms_u"] / locked["rms_u"] if locked["rms_u"] > 0 else float("inf")
        wcs.append({
            "label": label,
            "description": desc,
            "c_A_value_u": cv,
            "c_A_value_MeV": cv * U_TO_MEV,
            "c_A_fraction": f"{frac.numerator}/{frac.denominator}",
            "fit_coef4": fit_wc["coef4"],
            "train_rms_u": fit_wc["rms_u"], "train_rms_MeV": fit_wc["rms_MeV"],
            "train_R2": fit_wc["R2"],
            "test_rms_u": eval_wc["rms_u"], "test_rms_MeV": eval_wc["rms_MeV"],
            "test_R2": eval_wc["R2"],
            "train_ratio_to_locked": ratio_train,
            "test_ratio_to_locked": ratio_test,
            "degrades_by_1p2x_train": ratio_train >= 1.20,
        })

    # Verdict gates
    train_ratio = locked["rms_u"] / baseline["rms_u"]
    test_ratio  = locked_test["rms_u"] / baseline_test["rms_u"]

    S1 = train_ratio <= 1.10
    S2 = test_ratio  <= 1.10
    S3 = locked["R2"] >= 0.95
    S4 = locked_test["R2"] >= 0.95
    S5 = all(w["degrades_by_1p2x_train"] for w in wcs)
    S6 = locked["rms_MeV"] <= 5.0

    strong_pass = all([S1, S2, S3, S4, S5, S6])
    F1 = train_ratio > 1.10
    F2 = test_ratio > 1.30
    F3 = locked["rms_MeV"] > 10.0
    F4 = not (wcs[4]["degrades_by_1p2x_train"] and wcs[5]["degrades_by_1p2x_train"])
    # F5: all alt typed (WC-A1..A4) fit comparably
    F5 = all(not w["degrades_by_1p2x_train"] for w in wcs[:4])

    if F1 or F3 or F4:
        verdict = "FAIL"
        signature = "CR250_FAIL_1_OVER_S_L_NOT_STRUCTURALLY_REAL"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR250_STRONG_PASS_1_OVER_S_L_IS_STRUCTURALLY_REAL__"
                     "LOCKED_FIT_WITHIN_1p10X_FREE__"
                     "ALL_WCS_DEGRADE_BY_1p20X__"
                     "ASYMMETRY_COEFFICIENT_THEOREM_GRADE_TYPED")
    else:
        verdict = "BOUNDARY"
        signature = ("CR250_BOUNDARY_LOCKED_FIT_CLOSE_BUT_SOME_WC_GATES_NOT_MET")

    # Anchor cases under locked model
    anchors_spec = [("C-12", 6, 6), ("C-13", 6, 7), ("Au-197", 79, 118)]
    all_rows = train_all + test_all
    anchor_rows = []
    for label, Z, N in anchors_spec:
        m_obs = None
        for r in all_rows:
            if r["Z"] == Z and r["N"] == N:
                m_obs = r["atomic_mass_u"]; break
        A = Z + N
        Q_mass = 4 * A * float(KAPPA)
        Q_sub = 8 * (Z * float(KAPPA) + (N - Z) * float(G))
        asym = ((Q_mass - Q_sub) ** 2) / Q_mass
        delta_pair = +1.0 if (Z%2==0 and N%2==0) else (-1.0 if (Z%2==1 and N%2==1) else 0.0)
        B_u_obs = A - m_obs
        c4 = locked["coef4"]
        pred_locked = (c4[0]*A - c4[1]*A**(2/3) - c4[2]*Z*(Z-1)/A**(1/3)
                       - c_A_locked_value * asym + c4[3] * delta_pair)
        c5 = baseline["coef"]
        pred_free = (c5[0]*A - c5[1]*A**(2/3) - c5[2]*Z*(Z-1)/A**(1/3)
                     - c5[3]*asym + c5[4]*delta_pair)
        anchor_rows.append({
            "label": label, "Z": Z, "N": N, "A": A,
            "B_u_observed_u": B_u_obs, "B_u_observed_MeV": B_u_obs * U_TO_MEV,
            "B_u_free_pred_MeV": pred_free * U_TO_MEV,
            "B_u_locked_pred_MeV": pred_locked * U_TO_MEV,
            "free_residual_MeV": (pred_free - B_u_obs) * U_TO_MEV,
            "locked_residual_MeV": (pred_locked - B_u_obs) * U_TO_MEV,
        })

    summary = {
        "verdict": verdict, "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA, "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "locked_c_A": {
            "fraction": f"{C_A_LOCKED.numerator}/{C_A_LOCKED.denominator}",
            "value_u": c_A_locked_value,
            "value_MeV": c_A_locked_value * U_TO_MEV,
            "structural_form": "1/(S*L) = 1/(8*162) = 1/1296",
        },
        "baseline_free_fit": {
            "coef_names": baseline["coef_names"],
            "coef_u": baseline["coef"],
            "coef_MeV": [c * U_TO_MEV for c in baseline["coef"]],
            "train_rms_u": baseline["rms_u"], "train_rms_MeV": baseline["rms_MeV"],
            "train_R2": baseline["R2"], "train_n": baseline["n"],
            "test_rms_u": baseline_test["rms_u"], "test_rms_MeV": baseline_test["rms_MeV"],
            "test_R2": baseline_test["R2"], "test_n": baseline_test["n"],
        },
        "locked_fit": {
            "coef_names_4": locked["coef_names_4"],
            "coef4_u": locked["coef4"],
            "coef4_MeV": [c * U_TO_MEV for c in locked["coef4"]],
            "c_A_locked_u": c_A_locked_value,
            "c_A_locked_MeV": c_A_locked_value * U_TO_MEV,
            "train_rms_u": locked["rms_u"], "train_rms_MeV": locked["rms_MeV"],
            "train_R2": locked["R2"], "train_n": locked["n"],
            "test_rms_u": locked_test["rms_u"], "test_rms_MeV": locked_test["rms_MeV"],
            "test_R2": locked_test["R2"], "test_n": locked_test["n"],
            "train_ratio_to_baseline": train_ratio,
            "test_ratio_to_baseline": test_ratio,
        },
        "wrong_controls": wcs,
        "anchor_cases": anchor_rows,
        "strong_pass_conditions": {
            "S1_train_within_1p10x_free": S1, "S2_test_within_1p10x_free": S2,
            "S3_train_R2_ge_0p95": S3, "S4_test_R2_ge_0p95": S4,
            "S5_all_wcs_degrade_1p2x": S5, "S6_train_rms_le_5MeV": S6,
        },
        "fail_conditions": {"F1_train_gt_1p10x": F1, "F2_test_gt_1p30x": F2,
                            "F3_train_rms_gt_10MeV": F3,
                            "F4_2x_or_half_doesnt_degrade": F4,
                            "F5_all_alt_typed_fit_comparably": F5},
    }
    (HERE / "CR250_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    write_csv(HERE / "CR250_baseline_free_fit.csv", [
        {"coefficient": n, "value_u": v, "value_MeV": v * U_TO_MEV}
        for n, v in zip(baseline["coef_names"], baseline["coef"])
    ] + [{"coefficient": "train_RMS_MeV", "value_u": baseline["rms_u"], "value_MeV": baseline["rms_MeV"]},
         {"coefficient": "test_RMS_MeV", "value_u": baseline_test["rms_u"], "value_MeV": baseline_test["rms_MeV"]},
         {"coefficient": "train_R2", "value_u": baseline["R2"], "value_MeV": baseline["R2"]},
         {"coefficient": "test_R2", "value_u": baseline_test["R2"], "value_MeV": baseline_test["R2"]}])
    write_csv(HERE / "CR250_locked_c_A_fit.csv", [
        {"coefficient": n, "value_u": v, "value_MeV": v * U_TO_MEV}
        for n, v in zip(locked["coef_names_4"], locked["coef4"])
    ] + [{"coefficient": "c_A_locked", "value_u": c_A_locked_value, "value_MeV": c_A_locked_value * U_TO_MEV},
         {"coefficient": "train_RMS_MeV", "value_u": locked["rms_u"], "value_MeV": locked["rms_MeV"]},
         {"coefficient": "test_RMS_MeV", "value_u": locked_test["rms_u"], "value_MeV": locked_test["rms_MeV"]},
         {"coefficient": "train_R2", "value_u": locked["R2"], "value_MeV": locked["R2"]},
         {"coefficient": "test_R2", "value_u": locked_test["R2"], "value_MeV": locked_test["R2"]},
         {"coefficient": "train_ratio_to_baseline", "value_u": train_ratio, "value_MeV": train_ratio},
         {"coefficient": "test_ratio_to_baseline", "value_u": test_ratio, "value_MeV": test_ratio}])
    write_csv(HERE / "CR250_wrong_controls.csv", [
        {k: v for k, v in w.items() if not isinstance(v, list)} for w in wcs])
    write_csv(HERE / "CR250_anchor_cases.csv", anchor_rows)
    manifest = [
        {"file": "CR250_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train_all)},
        {"file": "CR250_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test_all)},
        {"file": "CR250_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR250_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print()
    print(f"Baseline (free c_A, 5-term):")
    print(f"  c_A_free = {baseline['coef'][3]:+.6e} u  ({baseline['coef'][3]*U_TO_MEV:+.4f} MeV)")
    print(f"  train RMS = {baseline['rms_MeV']:.4f} MeV  R^2 = {baseline['R2']:.5f}")
    print(f"  test  RMS = {baseline_test['rms_MeV']:.4f} MeV  R^2 = {baseline_test['R2']:.5f}")
    print()
    print(f"Locked (c_A = 1/(S*L) = 1/{S * L_LEDGER} = {c_A_locked_value:.6e} u, refit 4-term):")
    for n, v in zip(locked["coef_names_4"], locked["coef4"]):
        print(f"  {n} = {v:+.6e} u  ({v*U_TO_MEV:+.4f} MeV)")
    print(f"  train RMS = {locked['rms_MeV']:.4f} MeV  R^2 = {locked['R2']:.5f}  (ratio to baseline: {train_ratio:.4f}x)")
    print(f"  test  RMS = {locked_test['rms_MeV']:.4f} MeV  R^2 = {locked_test['R2']:.5f}  (ratio to baseline: {test_ratio:.4f}x)")
    print()
    print("Wrong controls:")
    print(f"  {'label':10s} {'description':25s} {'c_A (MeV)':>12s} {'train RMS (MeV)':>18s} {'ratio':>8s} {'pass':>6s}")
    for w in wcs:
        print(f"  {w['label']:10s} {w['description']:25s} {w['c_A_value_MeV']:>12.6f} {w['train_rms_MeV']:>18.4f} {w['train_ratio_to_locked']:>8.3f}x {str(w['degrades_by_1p2x_train']):>6s}")
    print()
    print("Anchor cases under locked model:")
    for a in anchor_rows:
        print(f"  {a['label']:8s} obs {a['B_u_observed_MeV']:+9.4f} MeV   free pred {a['B_u_free_pred_MeV']:+9.4f} (res {a['free_residual_MeV']:+8.4f})   locked pred {a['B_u_locked_pred_MeV']:+9.4f} (res {a['locked_residual_MeV']:+8.4f})")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4} S5={S5} S6={S6}")
    print(f"FAIL flags: F1={F1} F2={F2} F3={F3} F4={F4} F5={F5}")


if __name__ == "__main__":
    main()
