"""CR249 — A-Kernel Binding Geometry runner.

Phase A: free-fit B_SAM = c_V*A - c_S*A^(2/3) - c_C*Z(Z-1)/A^(1/3)
                       - c_A*(dQ)^2/Q_mass + c_P*delta_pair  on Lane A train (A>=16).
Phase B: typed-coefficient candidate search + zero-free evaluation.
WCs: shape-removal (5), geometric-scaling (2), pairing-variant (1, report only),
     shuffle (1).
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).parent
TRAIN_CSV = HERE / "CR249_train_lane_a.csv"
TEST_CSV = HERE / "CR249_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR249_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "d4a93d3f87908b3630e4e9d68618109e1394c97830dfd5b22bc400651e29399b"

KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R, D, S, M_LEDGER, L_LEDGER, V_LEDGER, THETA = 12, 3, 8, 126, 162, 27, 18
U_TO_MEV = 931.49410242


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def read_isotope_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open() as f:
        for row in csv.DictReader(f):
            row["Z"] = int(row["Z"])
            row["N"] = int(row["N"])
            row["A"] = int(row["A"])
            row["atomic_mass_u"] = float(row["atomic_mass_u"])
            row["B_u"] = row["A"] - row["atomic_mass_u"]
            rows.append(row)
    return rows


def compute_sob_columns(rows: list[dict[str, Any]]) -> None:
    """Add Q_mass, Q_sub, dQ, asym_feature to each row."""
    kappa_f = float(KAPPA); g_f = float(G)
    for r in rows:
        A = r["A"]; Z = r["Z"]; N = r["N"]
        r["Q_mass"] = 4 * A * kappa_f
        r["Q_sub"] = 8 * (Z * kappa_f + (N - Z) * g_f)
        r["dQ"] = r["Q_mass"] - r["Q_sub"]
        r["asym_feature"] = (r["dQ"] ** 2) / r["Q_mass"] if r["Q_mass"] > 0 else 0.0
        if Z % 2 == 0 and N % 2 == 0:
            r["delta_pair"] = +1.0
        elif Z % 2 == 1 and N % 2 == 1:
            r["delta_pair"] = -1.0
        else:
            r["delta_pair"] = 0.0


def design_matrix(rows: list[dict[str, Any]],
                  drop_shape: str | None = None,
                  surface_exponent: float = 2.0 / 3,
                  road_exponent: float = 1.0 / 3,
                  pair_form: str = "delta_pair") -> tuple[np.ndarray, list[str]]:
    """Build design matrix per locked binding form (with optional shape drops or
    geometric-scaling perturbations for WCs)."""
    cols = []
    col_names = []
    for r in rows:
        A, Z, N = r["A"], r["Z"], r["N"]
        v_vol = A
        v_surf = -(A ** surface_exponent)
        v_coul = -(Z * (Z - 1) / A ** road_exponent)
        v_asym = -r["asym_feature"]
        if pair_form == "delta_pair":
            v_pair = r["delta_pair"]
        elif pair_form == "delta_over_sqrtA":
            v_pair = r["delta_pair"] / (A ** 0.5)
        else:
            raise ValueError(pair_form)
        row_vec = [v_vol, v_surf, v_coul, v_asym, v_pair]
        names = ["c_V", "c_S", "c_C", "c_A", "c_P"]
        if drop_shape == "volume":
            row_vec = row_vec[1:]; names = names[1:]
        elif drop_shape == "surface":
            row_vec = [row_vec[0]] + row_vec[2:]; names = ["c_V"] + names[2:]
        elif drop_shape == "coulomb":
            row_vec = row_vec[:2] + row_vec[3:]; names = names[:2] + names[3:]
        elif drop_shape == "asymmetry":
            row_vec = row_vec[:3] + row_vec[4:]; names = names[:3] + names[4:]
        elif drop_shape == "pairing":
            row_vec = row_vec[:4]; names = names[:4]
        cols.append(row_vec)
    return np.array(cols), names


def fit(rows: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
    X, names = design_matrix(rows, **kwargs)
    y = np.array([r["B_u"] for r in rows])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    residual = pred - y
    rms_u = float(np.sqrt(np.mean(residual ** 2)))
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return {"coef": coef.tolist(), "names": names,
            "rms_u": rms_u, "rms_MeV": rms_u * U_TO_MEV,
            "R2": r2, "n": len(rows), "pred": pred.tolist(),
            "residual": residual.tolist()}


def evaluate_with(rows: list[dict[str, Any]], coef: list[float],
                  **design_kwargs: Any) -> dict[str, Any]:
    X, _ = design_matrix(rows, **design_kwargs)
    y = np.array([r["B_u"] for r in rows])
    pred = X @ np.array(coef)
    residual = pred - y
    rms_u = float(np.sqrt(np.mean(residual ** 2)))
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return {"rms_u": rms_u, "rms_MeV": rms_u * U_TO_MEV, "R2": r2,
            "n": len(rows), "pred": pred.tolist()}


def typed_candidates() -> dict[str, Fraction]:
    atoms = {
        "R": Fraction(R), "D": Fraction(D), "S": Fraction(S),
        "M": Fraction(M_LEDGER), "L": Fraction(L_LEDGER),
        "V": Fraction(V_LEDGER), "Theta": Fraction(THETA),
        "kappa": KAPPA, "g": G, "kappa-2g": KAPPA - 2 * G,
    }
    out: dict[str, Fraction] = {}
    for name, v in atoms.items():
        if v != 0:
            out[f"1/{name}"] = Fraction(1) / v
        out[name] = v
    items = list(atoms.items())
    for i, (n1, v1) in enumerate(items):
        for n2, v2 in items[i:]:
            if v1 * v2 != 0:
                out[f"1/({n1}*{n2})"] = Fraction(1) / (v1 * v2)
    for n, v in atoms.items():
        if v != 0 and n != "kappa":
            out[f"kappa/{n}"] = KAPPA / v
        if v != 0 and n != "g":
            out[f"g/{n}"] = G / v
    for n1, v1 in atoms.items():
        for n2, v2 in atoms.items():
            if n1 == n2 or v2 == 0 or n1 in ("kappa", "g") or n2 in ("kappa", "g"):
                continue
            out[f"{n1}/{n2}"] = v1 / v2
    for n, v in atoms.items():
        if v != 0 and n not in ("kappa", "g", "kappa-2g"):
            out[f"(kappa-2g)/{n}"] = (KAPPA - 2 * G) / v
    out["kappa^2"] = KAPPA * KAPPA
    out["g^2"] = G * G
    out["kappa*g"] = KAPPA * G
    out["(D+2)/(R*(D+1))"] = Fraction(D + 2, R * (D + 1))
    out["(D^2+S)/(D*S^2)"] = Fraction(D * D + S, D * S * S)
    out["7093^2/(192*7117)"] = Fraction(7093 * 7093, 192 * 7117)
    return out


def find_best(fitted: float, cands: dict[str, Fraction]) -> dict[str, Any]:
    best: dict[str, Any] | None = None
    for name, frac in cands.items():
        for sign in (+1, -1):
            cv = sign * float(frac)
            if fitted == 0:
                rel = 1.0 if cv != 0 else 0.0
            else:
                rel = abs((fitted - cv) / fitted)
            if best is None or rel < best["rel_dev"]:
                best = {"name": ("+" if sign > 0 else "-") + name,
                        "value": cv,
                        "fraction": f"{sign*frac.numerator}/{frac.denominator}",
                        "rel_dev": rel}
    best["within_5pct"] = best["rel_dev"] <= 0.05
    best["within_1pct"] = best["rel_dev"] <= 0.01
    return best


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
    compute_sob_columns(train_all); compute_sob_columns(test_all)

    train_fit = [r for r in train_all if r["A"] != 12 and r["A"] >= 16 and r["N"] >= r["Z"]]
    test_eval = [r for r in test_all if r["N"] >= r["Z"]]

    # --- Phase A: free-fit five-shape model ---
    phase_a = fit(train_fit)
    coef_names = phase_a["names"]
    c_V, c_S, c_C, c_A, c_P = phase_a["coef"]
    test_eval_results = evaluate_with(test_eval, phase_a["coef"])

    S1 = phase_a["rms_MeV"] <= 5.0
    S2 = test_eval_results["rms_MeV"] <= 5.0
    S3 = phase_a["R2"] >= 0.95
    S4 = test_eval_results["R2"] >= 0.95

    # Anchor predictions
    anchors_spec = [("C-12", 6, 6), ("C-13", 6, 7), ("Au-197", 79, 118)]
    all_rows = train_all + test_all
    anchor_rows = []
    for label, Z, N in anchors_spec:
        m_obs = None
        for r in all_rows:
            if r["Z"] == Z and r["N"] == N:
                m_obs = r["atomic_mass_u"]; break
        if m_obs is None:
            continue
        A = Z + N
        Q_mass = 4 * A * float(KAPPA)
        Q_sub = 8 * (Z * float(KAPPA) + (N - Z) * float(G))
        dQ = Q_mass - Q_sub
        asym_feat = (dQ ** 2) / Q_mass if Q_mass > 0 else 0.0
        delta_pair = +1.0 if (Z % 2 == 0 and N % 2 == 0) else (-1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0)
        B_u_obs = A - m_obs
        B_u_pred = (c_V * A - c_S * A**(2/3) - c_C * Z*(Z-1)/A**(1/3)
                    - c_A * asym_feat + c_P * delta_pair)
        anchor_rows.append({
            "label": label, "Z": Z, "N": N, "A": A,
            "Q_mass": Q_mass, "Q_sub": Q_sub, "dQ": dQ,
            "asym_feature": asym_feat, "delta_pair": delta_pair,
            "B_u_observed_u": B_u_obs, "B_u_predicted_u": B_u_pred,
            "B_u_observed_MeV": B_u_obs * U_TO_MEV,
            "B_u_predicted_MeV": B_u_pred * U_TO_MEV,
            "residual_u": B_u_pred - B_u_obs,
            "residual_MeV": (B_u_pred - B_u_obs) * U_TO_MEV,
        })

    # --- Phase B: typed-coefficient search ---
    cands = typed_candidates()
    fitted_by_name = {"c_V": c_V, "c_S": c_S, "c_C": c_C, "c_A": c_A, "c_P": c_P}
    typed_search = {}
    for k, v in fitted_by_name.items():
        typed_search[k] = {"fitted_u": v, "fitted_MeV": v * U_TO_MEV,
                           "best_candidate": find_best(v, cands)}
    matched_5pct = sum(1 for x in typed_search.values() if x["best_candidate"]["within_5pct"])
    matched_1pct = sum(1 for x in typed_search.values() if x["best_candidate"]["within_1pct"])

    zf_coef = []
    substitutions = {}
    for k in ("c_V", "c_S", "c_C", "c_A", "c_P"):
        b = typed_search[k]["best_candidate"]
        if b["within_5pct"]:
            zf_coef.append(b["value"])
            substitutions[k] = {"substituted": True, "typed_name": b["name"],
                                "typed_value": b["value"], "rel_dev": b["rel_dev"]}
        else:
            zf_coef.append(fitted_by_name[k])
            substitutions[k] = {"substituted": False, "fitted_value": fitted_by_name[k],
                                "best_attempt": b["name"], "rel_dev": b["rel_dev"]}
    zf_train = evaluate_with(train_fit, zf_coef)
    zf_test = evaluate_with(test_eval, zf_coef)

    # --- Wrong controls ---
    wcs = []
    for label, drop in [("WC-1_drop_volume", "volume"),
                        ("WC-2_drop_surface", "surface"),
                        ("WC-3_drop_coulomb", "coulomb"),
                        ("WC-4_drop_asymmetry", "asymmetry"),
                        ("WC-5_drop_pairing", "pairing")]:
        f = fit(train_fit, drop_shape=drop)
        ratio = f["rms_u"] / phase_a["rms_u"] if phase_a["rms_u"] > 0 else float("inf")
        wcs.append({"label": label,
                    "description": f"Drop {drop} shape; refit remaining 4-term",
                    "rms_MeV": f["rms_MeV"], "R2": f["R2"],
                    "ratio_to_canonical": ratio,
                    "pass": ratio >= 1.5})
    # WC-6: A^(2/3) -> A^(1/2)
    f6 = fit(train_fit, surface_exponent=0.5)
    ratio6 = f6["rms_u"] / phase_a["rms_u"]
    wcs.append({"label": "WC-6_surface_A_half",
                "description": "Replace surface A^(2/3) with A^(1/2)",
                "rms_MeV": f6["rms_MeV"], "R2": f6["R2"],
                "ratio_to_canonical": ratio6,
                "pass": ratio6 >= 1.2})
    # WC-7: road 1/A^(1/3) -> 1/A^(2/3)
    f7 = fit(train_fit, road_exponent=2/3)
    ratio7 = f7["rms_u"] / phase_a["rms_u"]
    wcs.append({"label": "WC-7_road_A_two_thirds",
                "description": "Replace road 1/A^(1/3) with 1/A^(2/3)",
                "rms_MeV": f7["rms_MeV"], "R2": f7["R2"],
                "ratio_to_canonical": ratio7,
                "pass": ratio7 >= 1.2})
    # WC-8: pairing delta -> delta/sqrt(A)
    f8 = fit(train_fit, pair_form="delta_over_sqrtA")
    wcs.append({"label": "WC-8_pairing_delta_over_sqrtA",
                "description": "Replace pairing delta_pair with delta_pair/sqrt(A)",
                "rms_MeV": f8["rms_MeV"], "R2": f8["R2"],
                "ratio_to_canonical": f8["rms_u"] / phase_a["rms_u"],
                "pass": True, "note": "report-only; no degradation gate"})
    # WC-9: shuffle B_u labels
    rng = random.Random(20260623)
    y_shuf = list([r["B_u"] for r in train_fit])
    rng.shuffle(y_shuf)
    X9, _ = design_matrix(train_fit)
    coef9, *_ = np.linalg.lstsq(X9, np.array(y_shuf), rcond=None)
    pred9 = X9 @ coef9
    rms9 = float(np.sqrt(np.mean((pred9 - np.array(y_shuf)) ** 2)))
    ratio9 = rms9 / phase_a["rms_u"]
    wcs.append({"label": "WC-9_shuffle_B_u",
                "description": "Shuffle B_u labels seed 20260623; refit",
                "rms_MeV": rms9 * U_TO_MEV, "R2": float("nan"),
                "ratio_to_canonical": ratio9,
                "pass": ratio9 >= 2.0})

    S5 = all(w["pass"] for w in wcs[:5])
    S6 = wcs[5]["pass"] and wcs[6]["pass"]
    S7 = wcs[8]["pass"]

    strong_pass = all([S1, S2, S3, S4, S5, S6, S7])
    F1 = phase_a["rms_MeV"] > 10.0
    # F2 fires only if a shape-removal WC truly does NOT degrade (ratio < 1.05),
    # not merely "fails to reach the 1.5x strong-pass gate".  Per precommit:
    # "preserves RMS (no degradation)".
    F2 = any(w["ratio_to_canonical"] < 1.05 for w in wcs[:5])
    F3 = not S7

    if F1 or F2 or F3:
        verdict = "FAIL"; signature = "CR249_FAIL_GEOMETRY_INSUFFICIENT_OR_WC_FAILED"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR249_STRONG_PASS_A_KERNEL_BINDING_GEOMETRY__"
                     "FIVE_SHAPES_FIT_WITHIN_TOL__SHAPE_REMOVAL_WCS_DEGRADE__"
                     "GEOMETRIC_SCALING_WCS_DEGRADE__SHUFFLE_DEGRADES")
    else:
        verdict = "BOUNDARY"
        signature = ("CR249_BOUNDARY_A_KERNEL_GEOMETRY_FITS_BW_RANGE__"
                     "SOME_WC_GATES_NOT_MET")

    summary = {
        "verdict": verdict, "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA, "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "substrate_atoms": {"R": R, "D": D, "S": S, "Theta": THETA,
                            "M": M_LEDGER, "L": L_LEDGER, "V": V_LEDGER,
                            "kappa": str(KAPPA), "g": str(G)},
        "geometric_dictionary": {
            "rho_A": "A^(1/3)", "V_A": "rho_A^3 = A",
            "S_A": "rho_A^2 = A^(2/3)", "R_A_inv": "rho_A^(-1) = A^(-1/3)",
            "dQ": "Q_mass - Q_sub = (N-Z)*7093/192 (CR245 identity)",
        },
        "phase_a_fit": {
            "design_matrix_basis": "[A, -A^(2/3), -Z(Z-1)/A^(1/3), -(dQ)^2/Q_mass, +delta_pair]",
            "coef_names": coef_names,
            "coefficients_u": {n: c for n, c in zip(coef_names, phase_a["coef"])},
            "coefficients_MeV": {n: c * U_TO_MEV for n, c in zip(coef_names, phase_a["coef"])},
            "train_rms_u": phase_a["rms_u"], "train_rms_MeV": phase_a["rms_MeV"],
            "train_R2": phase_a["R2"], "train_n": phase_a["n"],
            "test_rms_u": test_eval_results["rms_u"],
            "test_rms_MeV": test_eval_results["rms_MeV"],
            "test_R2": test_eval_results["R2"], "test_n": test_eval_results["n"],
        },
        "phase_a_anchors": anchor_rows,
        "phase_b_typed_search": typed_search,
        "phase_b_summary": {
            "matched_within_5pct": matched_5pct,
            "matched_within_1pct": matched_1pct,
        },
        "phase_b_zero_free": {
            "substitutions": substitutions,
            "train_rms_u": zf_train["rms_u"], "train_rms_MeV": zf_train["rms_MeV"],
            "train_R2": zf_train["R2"],
            "test_rms_u": zf_test["rms_u"], "test_rms_MeV": zf_test["rms_MeV"],
            "test_R2": zf_test["R2"],
        },
        "wrong_controls": wcs,
        "strong_pass_conditions": {
            "S1_train_rms_le_5MeV": S1, "S2_test_rms_le_5MeV": S2,
            "S3_train_R2_ge_0p95": S3, "S4_test_R2_ge_0p95": S4,
            "S5_shape_removals_all_degrade_1p5x": S5,
            "S6_geom_scalings_degrade_1p2x": S6,
            "S7_shuffle_degrades_2x": S7,
        },
        "fail_conditions": {"F1_train_rms_gt_10MeV": F1,
                            "F2_shape_removal_fails": F2,
                            "F3_shuffle_no_degrade": F3},
    }
    (HERE / "CR249_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    write_csv(HERE / "CR249_phase_a_fit.csv", [{
        "coefficient": n,
        "fitted_u": phase_a["coef"][i],
        "fitted_MeV": phase_a["coef"][i] * U_TO_MEV,
        "best_typed": typed_search[n]["best_candidate"]["name"],
        "best_typed_value": typed_search[n]["best_candidate"]["value"],
        "rel_dev": typed_search[n]["best_candidate"]["rel_dev"],
        "within_5pct": typed_search[n]["best_candidate"]["within_5pct"],
        "within_1pct": typed_search[n]["best_candidate"]["within_1pct"],
    } for i, n in enumerate(coef_names)])
    write_csv(HERE / "CR249_anchor_cases.csv", anchor_rows)
    write_csv(HERE / "CR249_typed_candidates.csv", [
        {"coefficient": k, "fitted_u": info["fitted_u"], "fitted_MeV": info["fitted_MeV"],
         "best_typed": info["best_candidate"]["name"],
         "best_typed_value": info["best_candidate"]["value"],
         "best_typed_fraction": info["best_candidate"]["fraction"],
         "rel_dev": info["best_candidate"]["rel_dev"],
         "within_5pct": info["best_candidate"]["within_5pct"],
         "within_1pct": info["best_candidate"]["within_1pct"]}
        for k, info in typed_search.items()])
    write_csv(HERE / "CR249_zero_free_predictions.csv",
              [{"split": "train_summary", "rms_MeV": zf_train["rms_MeV"], "R2": zf_train["R2"]},
               {"split": "test_summary",  "rms_MeV": zf_test["rms_MeV"],  "R2": zf_test["R2"]}])
    write_csv(HERE / "CR249_wrong_controls.csv", [
        {k: v for k, v in w.items() if not isinstance(v, dict)} for w in wcs])
    manifest = [
        {"file": "CR249_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train_all)},
        {"file": "CR249_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test_all)},
        {"file": "CR249_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR249_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print()
    print("Phase A — A-Kernel Geometry Free-Fit:")
    for n, c in zip(coef_names, phase_a["coef"]):
        print(f"  {n}: fitted = {c:+.6e} u  ({c * U_TO_MEV:+.4f} MeV)")
    print(f"  train RMS = {phase_a['rms_MeV']:.4f} MeV   R^2 = {phase_a['R2']:.5f}   n = {phase_a['n']}")
    print(f"  test  RMS = {test_eval_results['rms_MeV']:.4f} MeV   R^2 = {test_eval_results['R2']:.5f}   n = {test_eval_results['n']}")
    print()
    print("Anchor B_u predictions:")
    for a in anchor_rows:
        print(f"  {a['label']:8s}  obs {a['B_u_observed_MeV']:+9.4f} MeV   pred {a['B_u_predicted_MeV']:+9.4f} MeV   resid {a['residual_MeV']:+8.4f} MeV")
    print()
    print("Phase B — Typed-Coefficient Search:")
    for k, info in typed_search.items():
        b = info["best_candidate"]
        flag = "WITHIN_5PCT" if b["within_5pct"] else "out"
        flag1 = "  WITHIN_1PCT" if b["within_1pct"] else ""
        print(f"  {k:5s} fitted={info['fitted_u']:+.5e} u  ({info['fitted_MeV']:+8.4f} MeV)  best={b['name']:24s}  rel={b['rel_dev']:.4f}  {flag}{flag1}")
    print(f"  Matched 5pct: {matched_5pct}/5; 1pct: {matched_1pct}/5")
    print(f"  Zero-free typed candidate: train {zf_train['rms_MeV']:.4f} MeV / test {zf_test['rms_MeV']:.4f} MeV")
    print()
    print("Wrong controls:")
    for w in wcs:
        print(f"  {w['label']:32s} {w['description'][:55]:55s} RMS {w['rms_MeV']:7.4f} MeV  ratio {w['ratio_to_canonical']:5.2f}x  pass={w['pass']}")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4} S5={S5} S6={S6} S7={S7}")


if __name__ == "__main__":
    main()
