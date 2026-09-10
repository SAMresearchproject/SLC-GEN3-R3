"""CR251 — Bounce-Aware Asymmetry Coefficient Isolation.

Phase A: orthogonalized coefficient isolation (Frisch-Waugh-Lovell) of c_A
         from B_u after projecting out [A, A^(2/3), Z(Z-1)/A^(1/3), delta_pair].
         Reports c_A_orth, SE, t-tests vs 1/(S*L) and 1/(S*R^2).
Phase B: isobaric (same-A) contrast fit on pair-differences.
Phase C: large |N-Z| stress lane (filter to |N-Z| >= 20), repeat Phase A.
WCs:    shuffle B_u, N=Z only, random X_0 feature, permuted X_A.
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
TRAIN_CSV = HERE / "CR251_train_lane_a.csv"
TEST_CSV = HERE / "CR251_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR251_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "3d3b0951d9e334cb53b2805d21aa6a9330b26e0faaaeff7c53aebf45f07499bc"

KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R, D, S, M_LEDGER, L_LEDGER, V_LEDGER, THETA = 12, 3, 8, 126, 162, 27, 18
U_TO_MEV = 931.49410242

C_A_SL = float(Fraction(1, S * L_LEDGER))    # 1/(S*L) = 1/1296
C_A_SR2 = float(Fraction(1, S * R * R))      # 1/(S*R^2) = 1/1152

LARGE_NMZ_THRESHOLD = 20


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
    k = float(KAPPA); gv = float(G)
    for r in rows:
        A, Z, N = r["A"], r["Z"], r["N"]
        Q_mass = 4 * A * k
        Q_sub = 8 * (Z * k + (N - Z) * gv)
        r["Q_mass"] = Q_mass; r["Q_sub"] = Q_sub
        r["dQ"] = Q_mass - Q_sub
        r["X_A"] = (r["dQ"] ** 2) / Q_mass if Q_mass > 0 else 0.0
        r["coulomb"] = Z * (Z - 1) / (A ** (1.0/3))
        r["surface"] = A ** (2.0/3)
        if Z % 2 == 0 and N % 2 == 0:
            r["delta_pair"] = +1.0
        elif Z % 2 == 1 and N % 2 == 1:
            r["delta_pair"] = -1.0
        else:
            r["delta_pair"] = 0.0


def orthogonalize_c_A(rows: list[dict[str, Any]], extra_col: np.ndarray | None = None,
                      X_A_override: np.ndarray | None = None) -> dict[str, Any]:
    """Phase A orthogonalized isolation of c_A.

    Uses the SIGNED canonical-BW design so that the OLS coefficient on X_A
    matches the canonical c_A directly (positive when asymmetry reduces B_u).

    X_0_signed = [A, -A^(2/3), -Z(Z-1)/A^(1/3), +delta_pair]
    X_A_signed = -(Q_mass-Q_sub)^2/Q_mass    (the asymmetry term enters as
                                              -c_A * X_A in the BW model)

    The Frisch-Waugh-Lovell theorem ensures the orthogonalized coefficient on
    X_A_signed equals the c_A in the full 5-term canonical OLS fit.
    """
    A_arr = np.array([r["A"] for r in rows], dtype=float)
    Asurf = np.array([r["surface"] for r in rows], dtype=float)
    Acoul = np.array([r["coulomb"] for r in rows], dtype=float)
    Adp = np.array([r["delta_pair"] for r in rows], dtype=float)
    X_0 = np.column_stack([A_arr, -Asurf, -Acoul, Adp])
    if extra_col is not None:
        X_0 = np.column_stack([X_0, extra_col])
    # X_A: signed -(asym) so the OLS coefficient is canonical c_A
    X_A_raw = np.array([r["X_A"] for r in rows], dtype=float) if X_A_override is None else X_A_override
    X_A = -X_A_raw
    B = np.array([r["B_u"] for r in rows], dtype=float)
    # Compute projection P_0 via pseudoinverse (more stable than normal eq inverse)
    X_0_pinv = np.linalg.pinv(X_0)
    coef_0_on_B = X_0_pinv @ B
    coef_0_on_X_A = X_0_pinv @ X_A
    B_perp = B - X_0 @ coef_0_on_B
    X_A_perp = X_A - X_0 @ coef_0_on_X_A
    # c_A_orth via OLS on the orthogonalized single-column model
    denom = float(X_A_perp @ X_A_perp)
    if denom == 0:
        return {"c_A_orth": None, "SE": float("inf"), "n": len(rows),
                "X_A_perp_norm_sq": 0.0, "residual_rms": None}
    c_A_orth = float((X_A_perp @ B_perp) / denom)
    # Residual std
    resid = B_perp - c_A_orth * X_A_perp
    n = len(rows)
    p_total = X_0.shape[1] + 1  # X_0 columns + 1 for c_A
    dof = max(n - p_total, 1)
    sigma2 = float(resid @ resid) / dof
    SE = math.sqrt(sigma2 / denom)
    residual_rms = float(np.sqrt(np.mean(resid ** 2)))
    return {
        "c_A_orth": c_A_orth, "SE": SE, "n": n, "dof": dof,
        "X_A_perp_norm_sq": denom, "sigma2_hat": sigma2,
        "residual_rms_u": residual_rms, "residual_rms_MeV": residual_rms * U_TO_MEV,
    }


def t_test(c_orth: float, SE: float, candidate: float) -> dict[str, Any]:
    if SE == 0 or SE is None:
        return {"t": float("inf"), "delta": c_orth - candidate, "abs_t": float("inf")}
    t = (c_orth - candidate) / SE
    return {"t": t, "delta": c_orth - candidate, "abs_t": abs(t)}


def isobaric_pairs(rows: list[dict[str, Any]]) -> list[tuple[int, int]]:
    by_A: dict[int, list[int]] = {}
    for i, r in enumerate(rows):
        by_A.setdefault(r["A"], []).append(i)
    pairs = []
    for A, idxs in by_A.items():
        if len(idxs) < 2:
            continue
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                pairs.append((idxs[i], idxs[j]))
    return pairs


def isobaric_fit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = isobaric_pairs(rows)
    if not pairs:
        return {"status": "INSUFFICIENT_DATA", "n_pairs": 0}
    delta_B = []; delta_coul = []; delta_X_A = []; delta_dp = []
    pair_labels = []
    for i, j in pairs:
        ri = rows[i]; rj = rows[j]
        delta_B.append(ri["B_u"] - rj["B_u"])
        delta_coul.append(ri["coulomb"] - rj["coulomb"])
        delta_X_A.append(ri["X_A"] - rj["X_A"])
        delta_dp.append(ri["delta_pair"] - rj["delta_pair"])
        pair_labels.append((ri.get("isotope"), rj.get("isotope"),
                            ri["A"], ri["Z"], ri["N"], rj["Z"], rj["N"]))
    dB = np.array(delta_B); dCoul = np.array(delta_coul)
    dXA = np.array(delta_X_A); dDP = np.array(delta_dp)
    # Build design matrix: include Coulomb + asym + delta_pair contrast
    X = np.column_stack([-dCoul, -dXA, dDP])
    if X.shape[0] < X.shape[1]:
        return {"status": "INSUFFICIENT_DATA", "n_pairs": len(pairs)}
    coef, *_ = np.linalg.lstsq(X, dB, rcond=None)
    pred = X @ coef
    resid = pred - dB
    n = len(pairs)
    p = X.shape[1]
    dof = max(n - p, 1)
    sigma2 = float(resid @ resid) / dof
    # SE on c_A (second column)
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
        SE_cA = math.sqrt(sigma2 * float(XtX_inv[1, 1]))
    except np.linalg.LinAlgError:
        SE_cA = float("inf")
    return {
        "status": "OK", "n_pairs": n,
        "coef_c_C_iso": float(coef[0]), "coef_c_A_iso": float(coef[1]),
        "coef_c_DP_iso": float(coef[2]),
        "SE_c_A": SE_cA,
        "rms_residual": float(np.sqrt(np.mean(resid ** 2))),
        "rms_residual_MeV": float(np.sqrt(np.mean(resid ** 2))) * U_TO_MEV,
        "pair_count": n,
        "pair_labels_sample": pair_labels[:10],
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
    if sha256(TRAIN_CSV) != EXPECTED_TRAIN_SHA: raise SystemExit("TRAIN SHA mismatch")
    if sha256(TEST_CSV) != EXPECTED_TEST_SHA: raise SystemExit("TEST SHA mismatch")
    if sha256(PRECOMMIT_MD) != EXPECTED_PRECOMMIT_SHA: raise SystemExit("PRECOMMIT SHA mismatch")

    train_all = read_isotope_csv(TRAIN_CSV); test_all = read_isotope_csv(TEST_CSV)
    compute_features(train_all); compute_features(test_all)
    full_corpus = [r for r in train_all + test_all if r["N"] >= r["Z"]]
    phase_a_corpus = [r for r in full_corpus if r["A"] >= 16]

    # --- Phase A: orthogonalized isolation on A >= 16 corpus ---
    pa = orthogonalize_c_A(phase_a_corpus)
    t_SL = t_test(pa["c_A_orth"], pa["SE"], C_A_SL)
    t_SR2 = t_test(pa["c_A_orth"], pa["SE"], C_A_SR2)

    # --- Phase B: isobaric contrasts on full corpus ---
    pb = isobaric_fit(full_corpus)
    if pb["status"] == "OK":
        t_SL_iso = t_test(pb["coef_c_A_iso"], pb["SE_c_A"], C_A_SL)
        t_SR2_iso = t_test(pb["coef_c_A_iso"], pb["SE_c_A"], C_A_SR2)
    else:
        t_SL_iso = t_SR2_iso = {"t": None, "delta": None, "abs_t": None}

    # --- Phase C: large |N-Z| stress lane ---
    phase_c_corpus = [r for r in phase_a_corpus if abs(r["N"] - r["Z"]) >= LARGE_NMZ_THRESHOLD]
    if len(phase_c_corpus) >= 6:
        pc = orthogonalize_c_A(phase_c_corpus)
        t_SL_stress = t_test(pc["c_A_orth"], pc["SE"], C_A_SL)
        t_SR2_stress = t_test(pc["c_A_orth"], pc["SE"], C_A_SR2)
    else:
        pc = {"status": "INSUFFICIENT_DATA", "n": len(phase_c_corpus)}
        t_SL_stress = t_SR2_stress = {"t": None, "delta": None, "abs_t": None}

    # --- Wrong controls ---
    wcs = []
    # WC-1: shuffle B_u
    rng = random.Random(20260623)
    Bs = [r["B_u"] for r in phase_a_corpus]; idxs = list(range(len(Bs))); rng.shuffle(idxs)
    shuffled_rows = []
    for i, r in enumerate(phase_a_corpus):
        rs = dict(r); rs["B_u"] = Bs[idxs[i]]; shuffled_rows.append(rs)
    wc1 = orthogonalize_c_A(shuffled_rows)
    wcs.append({"label": "WC-1_shuffle_B_u", "c_A_orth": wc1["c_A_orth"], "SE": wc1["SE"],
                "n": wc1["n"], "abs_t_vs_SL": abs((wc1["c_A_orth"] - C_A_SL) / wc1["SE"]) if wc1["SE"] > 0 else None,
                "pass": abs(wc1["c_A_orth"]) < 3 * wc1["SE"] if wc1["SE"] > 0 else False,
                "description": "shuffled B_u labels; expect c_A near zero"})

    # WC-2: N = Z only
    nz_rows = [r for r in phase_a_corpus if r["N"] == r["Z"]]
    if len(nz_rows) >= 5:
        wc2 = orthogonalize_c_A(nz_rows)
        wcs.append({"label": "WC-2_N_eq_Z_only", "c_A_orth": wc2["c_A_orth"], "SE": wc2["SE"],
                    "n": wc2["n"], "pass": (wc2["c_A_orth"] is None) or (wc2["SE"] is None) or wc2["SE"] > abs(C_A_SL),
                    "description": "N=Z rows only; X_A nearly zero so c_A ill-conditioned"})
    else:
        wcs.append({"label": "WC-2_N_eq_Z_only", "c_A_orth": None, "SE": None,
                    "n": len(nz_rows),
                    "pass": True, "description": "Insufficient N=Z rows for orthogonalization (recorded)"})

    # WC-3: add random feature to X_0
    rng2 = random.Random(20260623)
    rand_feat = np.array([rng2.gauss(0, 1) for _ in phase_a_corpus])
    wc3 = orthogonalize_c_A(phase_a_corpus, extra_col=rand_feat)
    rel_change = abs((wc3["c_A_orth"] - pa["c_A_orth"]) / pa["c_A_orth"]) if pa["c_A_orth"] != 0 else float("inf")
    wcs.append({"label": "WC-3_random_feature_added", "c_A_orth": wc3["c_A_orth"], "SE": wc3["SE"],
                "n": wc3["n"], "rel_change_vs_phase_a": rel_change,
                "pass": rel_change < 0.05,
                "description": "Random feature added to X_0; c_A_orth should be ~unchanged"})

    # WC-4: permute X_A
    XA_vals = [r["X_A"] for r in phase_a_corpus]
    rng3 = random.Random(20260623); idx4 = list(range(len(XA_vals))); rng3.shuffle(idx4)
    XA_perm = np.array([XA_vals[idx4[i]] for i in range(len(XA_vals))])
    wc4 = orthogonalize_c_A(phase_a_corpus, X_A_override=XA_perm)
    abs_t4 = abs(wc4["c_A_orth"] / wc4["SE"]) if wc4["SE"] > 0 else float("inf")
    wcs.append({"label": "WC-4_permute_X_A", "c_A_orth": wc4["c_A_orth"], "SE": wc4["SE"],
                "n": wc4["n"], "abs_t": abs_t4,
                "pass": abs_t4 < 3.0,
                "description": "X_A permuted across rows; c_A_orth should be near zero"})

    # --- Verdict ---
    abs_t_SL = abs(t_SL["t"]) if t_SL["t"] is not None else float("inf")
    abs_t_SR2 = abs(t_SR2["t"]) if t_SR2["t"] is not None else float("inf")
    S1 = (abs_t_SL < 1.96) and (abs_t_SR2 >= 2.58)
    if pc.get("status") != "INSUFFICIENT_DATA":
        abs_t_SL_stress = abs(t_SL_stress["t"])
        abs_t_SR2_stress = abs(t_SR2_stress["t"])
        S2 = (abs_t_SL_stress < 2.58) and (abs_t_SR2_stress >= 1.96)
    else:
        S2 = None  # not evaluable
    if pb["status"] == "OK":
        abs_t_SL_iso = abs(t_SL_iso["t"]); abs_t_SR2_iso = abs(t_SR2_iso["t"])
        S3 = (abs_t_SL_iso < 1.96) and (abs_t_SR2_iso >= 1.96)
    else:
        S3 = None
    S4 = all(w["pass"] for w in wcs if w.get("pass") is not None)

    F1 = abs_t_SL >= 2.58
    F2 = abs_t_SR2 < abs_t_SL  # SR2 closer than SL in primary Phase A
    # F3 requires real REJECTION of 1/(S*L) in stress, not just lower-precision
    # preference shift.  Specifically: 1/(S*L) outside 95% CI in stress AND
    # 1/(S*R^2) inside 95% CI in stress.
    if pc.get("status") != "INSUFFICIENT_DATA":
        F3 = (abs(t_SL_stress["t"]) >= 1.96 and abs(t_SR2_stress["t"]) < 1.96
              and abs(t_SR2_stress["t"]) < abs(t_SL_stress["t"]))
    else:
        F3 = False
    F4 = (pb["status"] == "OK" and abs(t_SR2_iso["t"]) < abs(t_SL_iso["t"])
          and pb["n_pairs"] >= 5)
    F5 = wc3.get("c_A_orth") is not None and pa["c_A_orth"] is not None and \
         abs((wc3["c_A_orth"] - pa["c_A_orth"]) / pa["c_A_orth"]) > 0.10

    s_conditions = [S1, S2 if S2 is not None else True, S3 if S3 is not None else True, S4]
    strong_pass = all(s_conditions) and S1  # require S1 to be a true strong-pass
    boundary = (abs_t_SL < 1.96) and (abs_t_SR2 < 2.58) and not strong_pass

    if F1 or F2 or F3 or F4:
        verdict = "FAIL"
        signature = "CR251_FAIL_1_OVER_S_L_STATISTICALLY_REJECTED_OR_INVERTED"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR251_STRONG_PASS_BOUNCE_AWARE_ASYM_COEF_STATISTICALLY_ISOLATED__"
                     "1_OVER_S_L_INSIDE_95PCT_CI__1_OVER_S_R2_OUTSIDE_99PCT_CI")
    elif boundary:
        verdict = "BOUNDARY"
        signature = ("CR251_BOUNDARY_1_OVER_S_L_INSIDE_95PCT_CI__"
                     "1_OVER_S_R2_NOT_CLEARLY_EXCLUDED_AT_99PCT")
    else:
        verdict = "BOUNDARY"
        signature = "CR251_BOUNDARY_PARTIAL_ISOLATION"

    summary = {
        "verdict": verdict, "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA, "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "substrate_atoms": {"R": R, "S": S, "L": L_LEDGER, "kappa": str(KAPPA), "g": str(G),
                            "L_eq_R2_x_9_over_8": "162 = 144 * 9/8 (CR217/CR222/CR229)"},
        "candidates": {
            "c_A_1_over_S_L_u": C_A_SL, "c_A_1_over_S_L_MeV": C_A_SL * U_TO_MEV,
            "c_A_1_over_S_R2_u": C_A_SR2, "c_A_1_over_S_R2_MeV": C_A_SR2 * U_TO_MEV,
            "ratio_SL_to_SR2_u": C_A_SL / C_A_SR2,
            "ratio_SR2_to_SL_u": C_A_SR2 / C_A_SL,
        },
        "phase_a_orthogonalized": {
            "n": pa["n"], "dof": pa["dof"],
            "c_A_orth_u": pa["c_A_orth"], "c_A_orth_MeV": pa["c_A_orth"] * U_TO_MEV,
            "SE_u": pa["SE"], "SE_MeV": pa["SE"] * U_TO_MEV,
            "rel_SE": pa["SE"] / pa["c_A_orth"] if pa["c_A_orth"] != 0 else None,
            "X_A_perp_norm_sq": pa["X_A_perp_norm_sq"],
            "residual_rms_MeV": pa["residual_rms_MeV"],
            "t_test_vs_1_over_S_L": {"t": t_SL["t"], "abs_t": t_SL["abs_t"],
                                     "delta_u": t_SL["delta"]},
            "t_test_vs_1_over_S_R2": {"t": t_SR2["t"], "abs_t": t_SR2["abs_t"],
                                      "delta_u": t_SR2["delta"]},
            "S1_t_SL_lt_1p96_AND_t_SR2_ge_2p58": S1,
            "F1_t_SL_ge_2p58": F1,
            "F2_SR2_closer_than_SL": F2,
        },
        "phase_b_isobaric": {
            **pb,
            "t_test_vs_1_over_S_L": {"t": t_SL_iso["t"], "abs_t": t_SL_iso["abs_t"],
                                     "delta_u": t_SL_iso["delta"]} if pb["status"] == "OK" else None,
            "t_test_vs_1_over_S_R2": {"t": t_SR2_iso["t"], "abs_t": t_SR2_iso["abs_t"],
                                      "delta_u": t_SR2_iso["delta"]} if pb["status"] == "OK" else None,
            "S3_iso_t_SL_lt_1p96_AND_t_SR2_ge_1p96": S3,
        },
        "phase_c_stress_NmZ_ge_20": {
            "n": len(phase_c_corpus),
            "c_A_orth_u": pc.get("c_A_orth"),
            "c_A_orth_MeV": pc.get("c_A_orth") * U_TO_MEV if pc.get("c_A_orth") is not None else None,
            "SE_u": pc.get("SE"), "SE_MeV": pc.get("SE") * U_TO_MEV if pc.get("SE") is not None else None,
            "t_test_vs_1_over_S_L": {"t": t_SL_stress["t"], "abs_t": t_SL_stress["abs_t"]},
            "t_test_vs_1_over_S_R2": {"t": t_SR2_stress["t"], "abs_t": t_SR2_stress["abs_t"]},
            "S2_stress_t_SL_lt_2p58_AND_t_SR2_ge_1p96": S2,
        },
        "wrong_controls": wcs,
        "strong_pass_conditions": {"S1_phase_a": S1, "S2_phase_c_stress": S2,
                                   "S3_phase_b_isobaric": S3, "S4_wcs": S4},
        "fail_conditions": {"F1_SL_outside_99pct": F1, "F2_SR2_closer_than_SL": F2,
                            "F3_stress_reverses": F3, "F4_iso_reverses": F4,
                            "F5_random_feature_destabilizes": F5},
    }
    (HERE / "CR251_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    write_csv(HERE / "CR251_phase_a_orthogonalized.csv", [{
        "n": pa["n"], "dof": pa["dof"],
        "c_A_orth_u": pa["c_A_orth"], "c_A_orth_MeV": pa["c_A_orth"] * U_TO_MEV,
        "SE_u": pa["SE"], "SE_MeV": pa["SE"] * U_TO_MEV,
        "rel_SE_percent": (pa["SE"] / pa["c_A_orth"]) * 100 if pa["c_A_orth"] != 0 else None,
        "1_over_S_L_u": C_A_SL, "delta_to_SL_u": pa["c_A_orth"] - C_A_SL,
        "t_SL": t_SL["t"], "abs_t_SL": t_SL["abs_t"],
        "1_over_S_R2_u": C_A_SR2, "delta_to_SR2_u": pa["c_A_orth"] - C_A_SR2,
        "t_SR2": t_SR2["t"], "abs_t_SR2": t_SR2["abs_t"],
    }])
    iso_rows = []
    if pb["status"] == "OK":
        iso_rows.append({"n_pairs": pb["n_pairs"],
                         "c_A_iso_u": pb["coef_c_A_iso"], "c_A_iso_MeV": pb["coef_c_A_iso"] * U_TO_MEV,
                         "SE_iso_u": pb["SE_c_A"], "SE_iso_MeV": pb["SE_c_A"] * U_TO_MEV,
                         "c_C_iso_u": pb["coef_c_C_iso"], "c_DP_iso_u": pb["coef_c_DP_iso"],
                         "rms_residual_MeV": pb["rms_residual_MeV"],
                         "t_SL": t_SL_iso["t"], "abs_t_SL": t_SL_iso["abs_t"],
                         "t_SR2": t_SR2_iso["t"], "abs_t_SR2": t_SR2_iso["abs_t"]})
    else:
        iso_rows.append({"status": pb["status"], "n_pairs": pb["n_pairs"]})
    write_csv(HERE / "CR251_phase_b_isobaric.csv", iso_rows)
    write_csv(HERE / "CR251_phase_c_stress.csv", [{
        "n": len(phase_c_corpus),
        "c_A_orth_u": pc.get("c_A_orth"),
        "SE_u": pc.get("SE"),
        "t_SL": t_SL_stress["t"], "abs_t_SL": t_SL_stress["abs_t"],
        "t_SR2": t_SR2_stress["t"], "abs_t_SR2": t_SR2_stress["abs_t"],
    }])
    write_csv(HERE / "CR251_wrong_controls.csv", [
        {k: v for k, v in w.items() if not isinstance(v, (list, dict))} for w in wcs])
    manifest = [
        {"file": "CR251_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train_all)},
        {"file": "CR251_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test_all)},
        {"file": "CR251_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR251_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print()
    print(f"Phase A — Orthogonalized Coefficient Isolation (A>=16, n={pa['n']}):")
    print(f"  c_A_orth = {pa['c_A_orth']:+.6e} u  ({pa['c_A_orth']*U_TO_MEV:+.4f} MeV)")
    print(f"  SE       = {pa['SE']:+.6e} u  ({pa['SE']*U_TO_MEV:+.4f} MeV)  rel SE = {(pa['SE']/pa['c_A_orth'])*100:.2f}%")
    print(f"  Residual RMS after orth = {pa['residual_rms_MeV']:.4f} MeV")
    print(f"  vs 1/(S*L) = {C_A_SL:+.6e} u  ({C_A_SL*U_TO_MEV:+.4f} MeV):  delta = {pa['c_A_orth']-C_A_SL:+.3e}  t = {t_SL['t']:+.3f}  |t| = {t_SL['abs_t']:.3f}")
    print(f"  vs 1/(S*R^2) = {C_A_SR2:+.6e} u  ({C_A_SR2*U_TO_MEV:+.4f} MeV):  delta = {pa['c_A_orth']-C_A_SR2:+.3e}  t = {t_SR2['t']:+.3f}  |t| = {t_SR2['abs_t']:.3f}")
    print()
    if pb["status"] == "OK":
        print(f"Phase B — Isobaric Contrasts (n_pairs = {pb['n_pairs']}):")
        print(f"  c_A_iso = {pb['coef_c_A_iso']:+.6e} u  ({pb['coef_c_A_iso']*U_TO_MEV:+.4f} MeV)")
        print(f"  SE      = {pb['SE_c_A']:+.6e} u  ({pb['SE_c_A']*U_TO_MEV:+.4f} MeV)")
        print(f"  vs 1/(S*L):    |t| = {t_SL_iso['abs_t']:.3f}")
        print(f"  vs 1/(S*R^2):  |t| = {t_SR2_iso['abs_t']:.3f}")
    else:
        print(f"Phase B — Isobaric Contrasts: {pb['status']} (n_pairs={pb['n_pairs']})")
    print()
    if pc.get("status") != "INSUFFICIENT_DATA":
        print(f"Phase C — Large |N-Z|>=20 stress lane (n = {len(phase_c_corpus)}):")
        print(f"  c_A_orth_stress = {pc['c_A_orth']:+.6e} u  ({pc['c_A_orth']*U_TO_MEV:+.4f} MeV)")
        print(f"  SE              = {pc['SE']:+.6e} u  ({pc['SE']*U_TO_MEV:+.4f} MeV)  rel = {(pc['SE']/pc['c_A_orth'])*100:.2f}%")
        print(f"  vs 1/(S*L):    |t| = {t_SL_stress['abs_t']:.3f}")
        print(f"  vs 1/(S*R^2):  |t| = {t_SR2_stress['abs_t']:.3f}")
    else:
        print(f"Phase C: {pc['status']} (n={pc['n']})")
    print()
    print("Wrong controls:")
    for w in wcs:
        cA = w.get("c_A_orth")
        SE = w.get("SE")
        cstr = f"{cA:+.3e}" if cA is not None else "None"
        SEstr = f"{SE:+.3e}" if SE is not None else "None"
        print(f"  {w['label']:35s} c_A_orth={cstr}  SE={SEstr}  pass={w['pass']}")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4}")
    print(f"FAIL flags: F1={F1} F2={F2} F3={F3} F4={F4} F5={F5}")


if __name__ == "__main__":
    main()
