"""
CR274 -- Gated Nuclear-Readout Operators for CR261 Binding Closure

Adds four family-scoped candidate operators on top of a frozen Model K
substrate base, keeping the tensor cipher sealed (G0) and the base fit
unchanged (each operator's feature is zero outside its family).

precommit : c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9
"""

import builtins
import csv
import hashlib
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = os.path.dirname(HERE)

PRECOMMIT_PATH = os.path.join(HERE, "CR274_PRECOMMIT.md")
PRECOMMIT_HASH = "c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9"
STEWARDSHIP_HASH = "d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88"

FIT_CSV = os.path.join(BRANCH, "CR261_PAIR_WRITE_BINDING_EXTENSION",
                       "CR261_bw_fit_per_row.csv")
FIT_HASH = "3212a36064244e6addc30e465af6577d68df7997715f6c68ff9bb983b0d8eef2"

OUT_SUMMARY = os.path.join(HERE, "CR274_summary.json")
OUT_RESULT = os.path.join(HERE, "CR274_result.md")
OUT_RESIDUALS = os.path.join(HERE, "CR274_residuals.csv")
OUT_OPERATORS = os.path.join(HERE, "CR274_operators.csv")
OUT_HASHES = os.path.join(HERE, "HASHES.txt")

WHITELIST = {
    os.path.normcase(os.path.abspath(p)) for p in (
        PRECOMMIT_PATH, FIT_CSV,
        os.path.abspath(__file__),
        OUT_SUMMARY, OUT_RESULT, OUT_RESIDUALS, OUT_OPERATORS, OUT_HASHES,
    )
}
OPENED = []
FORBIDDEN_OPENED = []
_real_open = builtins.open


def guarded_open(file, mode="r", *args, **kwargs):
    try:
        abs_path = os.path.normcase(os.path.abspath(file))
    except Exception:
        abs_path = str(file)
    OPENED.append(abs_path)
    if abs_path not in WHITELIST:
        FORBIDDEN_OPENED.append(abs_path)
    return _real_open(file, mode, *args, **kwargs)


builtins.open = guarded_open


def file_sha256(p):
    with _real_open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ── Substrate constants (locked from CR238/CR245) ──
G_p = Fraction(145, 16)
G_e = Fraction(145, 768)
G_n = Fraction(1, 64)
KAPPA_NUM = 7117
KAPPA_DEN = 768
GAP_NUM = 7093
GAP_DEN = 192
D_LOCKED_FRAC = Fraction(GAP_NUM * GAP_NUM, GAP_DEN * KAPPA_NUM)
D_LOCKED = float(D_LOCKED_FRAC)

MAGIC = [2, 8, 20, 28, 50, 82, 126]
MAGIC_SET = set(MAGIC)

ANCHORS = ["O-16", "Fe-56", "Au-197", "Pb-208"]


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "set": row["set"],
                "isotope": row["isotope"],
                "Z": int(row["Z"]),
                "N": int(row["N"]),
                "A": int(row["A"]),
                "B_u_obs": float(row["B_u_obs_MeV"]),
            })
    return rows


# ── Phase 1: cipher regression at exact Fraction arithmetic ──
def cipher_check(rows):
    max_dev = Fraction(0)
    per_row = []
    for r in rows:
        Z, N, A = r["Z"], r["N"], r["A"]
        G_P = Z * (G_p + G_e) + N * G_n
        Q_mass = Fraction(4 * A * KAPPA_NUM, KAPPA_DEN)
        Q_sub = 8 * G_P
        F_actual = Q_mass - Q_sub
        F_expected = Fraction((N - Z) * GAP_NUM, GAP_DEN)
        dev = F_actual - F_expected
        if abs(dev) > abs(max_dev):
            max_dev = dev
        per_row.append({
            "isotope": r["isotope"],
            "F_actual_num": F_actual.numerator,
            "F_actual_den": F_actual.denominator,
            "F_expected_num": F_expected.numerator,
            "F_expected_den": F_expected.denominator,
            "deviation": float(dev),
        })
    return max_dev, per_row


# ── Model K base features ──
def dist_to_magic(x):
    return min(abs(x - m) for m in MAGIC)


def find_shell(x):
    lower, upper = 0, 200
    for m in MAGIC:
        if m <= x and m > lower:
            lower = m
        if m > x and m < upper:
            upper = m
    return lower, upper


def base_features(r):
    Z, N, A = r["Z"], r["N"], r["A"]
    delta = 1.0 if (Z % 2 == 0 and N % 2 == 0) else \
            -1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0
    dZ = dist_to_magic(Z)
    dN = dist_to_magic(N)
    lowerZ, upperZ = find_shell(Z)
    lowerN, upperN = find_shell(N)
    nZ = Z - lowerZ
    nN = N - lowerN
    spZ = upperZ - lowerZ
    spN = upperN - lowerN
    quadZ = nZ * (spZ - nZ)
    quadN = nN * (spN - nN)
    f_alpha = (A // 4) if (N == Z and A % 4 == 0) else 0.0
    if 50 < Z < 82 and 82 < N < 126:
        zt = (Z - 50) * (82 - Z) / ((32 / 2) ** 2)
        nt = (N - 82) * (126 - N) / ((44 / 2) ** 2)
        f_reonset = -zt * nt
    else:
        f_reonset = 0.0
    f_doubmag = 1.0 if (Z in MAGIC_SET and N in MAGIC_SET) else 0.0
    return {
        "vol": A,
        "surf": -A ** (2 / 3),
        "coul": -Z * (Z - 1) / A ** (1 / 3),
        "asym": -((N - Z) ** 2) / A,
        "pair": -delta * A ** (-0.5),
        "quadZ_A": -quadZ / A,
        "quadN_A": -quadN / A,
        "quad_cross_A2": -quadZ * quadN / (A * A),
        "shell_prox": -math.exp(-dZ / 3.0) - math.exp(-dN / 3.0),
        "lightodd": 1.0 if (A < 40 and A % 2 == 1) else 0.0,
        "alpha": f_alpha,
        "reonset": f_reonset,
        "doubmag": f_doubmag,
    }


BASE_NAMES = ["vol", "surf", "coul", "pair",
              "quadZ_A", "quadN_A", "quad_cross_A2",
              "shell_prox", "lightodd",
              "alpha", "reonset", "doubmag"]


# ── Operators ──
def op_features(r):
    Z, N, A = r["Z"], r["N"], r["A"]
    lowerN, upperN = find_shell(N)
    nN = N - lowerN
    return {
        "op_82pre": (Z - 56) ** 2 if (N == 82 and Z > 56) else 0.0,
        "op_3d_odd": 1.0 if (Z % 2 == 1 and 20 < Z < 30) else 0.0,
        "op_dm_sat": 1.0 if (Z in MAGIC_SET and N in MAGIC_SET and A >= 100) else 0.0,
        "op_ms_fill": nN if (28 < Z <= 50 and 50 < N < 82) else 0.0,
    }


def in_family(iso_row, op_name):
    Z, N, A = iso_row["Z"], iso_row["N"], iso_row["A"]
    if op_name == "op_82pre":
        return N == 82 and Z > 56
    if op_name == "op_3d_odd":
        return Z % 2 == 1 and 20 < Z < 30
    if op_name == "op_dm_sat":
        return Z in MAGIC_SET and N in MAGIC_SET and A >= 100
    if op_name == "op_ms_fill":
        return 28 < Z <= 50 and 50 < N < 82
    return False


# ── Least squares (Gauss-Jordan) ──
def solve_ols(X, y):
    n = len(X[0])
    ATA = [[0.0] * n for _ in range(n)]
    ATy = [0.0] * n
    for xi, yi in zip(X, y):
        for i in range(n):
            ATy[i] += xi[i] * yi
            for j in range(n):
                ATA[i][j] += xi[i] * xi[j]
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    for i in range(n):
        piv = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[piv] = M[piv], M[i]
        piv_val = M[i][i]
        if abs(piv_val) < 1e-14:
            raise RuntimeError(f"Singular at col {i}")
        for j in range(i, n + 1):
            M[i][j] /= piv_val
        for k in range(n):
            if k == i:
                continue
            factor = M[k][i]
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]
    return [M[i][n] for i in range(n)]


def rms(vals):
    return math.sqrt(sum(v * v for v in vals) / len(vals)) if vals else 0.0


def fit_base_K(rows):
    X, y = [], []
    for r in rows:
        f = base_features(r)
        X.append([f[n] for n in BASE_NAMES])
        y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
    beta = solve_ols(X, y)
    beta_dict = dict(zip(BASE_NAMES, beta))
    beta_dict["asym"] = D_LOCKED
    return beta_dict


def base_predict(r, beta):
    f = base_features(r)
    return sum(beta[n] * f[n] for n in beta if n in f)


def fit_operator(rows, beta_base, op_name):
    num = 0.0
    den = 0.0
    family = []
    for r in rows:
        if not in_family(r, op_name):
            continue
        family.append(r["isotope"])
        f = op_features(r)[op_name]
        base_pred = base_predict(r, beta_base)
        resid = r["B_u_obs"] - base_pred
        num += resid * f
        den += f * f
    if den == 0:
        return 0.0, family
    return num / den, family


def kfold_cv_base(rows, k=5, seed=0):
    import random
    rng = random.Random(seed)
    idxs = list(range(len(rows)))
    rng.shuffle(idxs)
    folds = [idxs[i::k] for i in range(k)]
    all_res = []
    for i in range(k):
        test_idx = set(folds[i])
        train = [rows[j] for j in range(len(rows)) if j not in test_idx]
        test = [rows[j] for j in test_idx]
        X, y = [], []
        for r in train:
            f = base_features(r)
            X.append([f[n] for n in BASE_NAMES])
            y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
        beta = solve_ols(X, y)
        bd = dict(zip(BASE_NAMES, beta))
        bd["asym"] = D_LOCKED
        for r in test:
            all_res.append(r["B_u_obs"] - base_predict(r, bd))
    return rms(all_res)


# ── Main ──
def main():
    print("=" * 78)
    print("CR274 — Gated Nuclear-Readout Operators")
    print(f"precommit hash locked: {PRECOMMIT_HASH}")
    print("=" * 78)

    # Verify precommit + input hashes
    actual_precommit = file_sha256(PRECOMMIT_PATH)
    precommit_ok = actual_precommit == PRECOMMIT_HASH
    print(f"precommit sha256 match: {precommit_ok}")
    actual_fit = file_sha256(FIT_CSV)
    fit_ok = actual_fit == FIT_HASH
    print(f"input CR261 fit csv match: {fit_ok}")

    rows = load_data()
    print(f"Loaded {len(rows)} isotopes")

    # G0: cipher regression
    max_dev, cipher_rows = cipher_check(rows)
    g0 = (max_dev == 0)
    print(f"\nG0 cipher regression: max |deviation| = {max_dev} → {'PASS' if g0 else 'FAIL'}")

    # Base Model K
    beta_K = fit_base_K(rows)
    print("\nModel K coefficients:")
    for k in ["vol", "surf", "coul", "asym", "pair",
              "quadZ_A", "quadN_A", "quad_cross_A2",
              "shell_prox", "lightodd",
              "alpha", "reonset", "doubmag"]:
        print(f"  {k:16s} = {beta_K[k]:+.5f}")

    base_res = []
    for r in rows:
        pred = base_predict(r, beta_K)
        base_res.append({
            "isotope": r["isotope"],
            "set": r["set"],
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "base_pred": pred,
            "base_resid": r["B_u_obs"] - pred,
        })
    base_rms = rms([x["base_resid"] for x in base_res])
    n_base_out = sum(1 for x in base_res if abs(x["base_resid"]) > 5)
    g1 = base_rms <= 4.5
    print(f"\nBase Model K: RMS = {base_rms:.4f} MeV, outliers = {n_base_out}/55")
    print(f"G1 base RMS ≤ 4.5: {'PASS' if g1 else 'FAIL'}")

    # CV diagnostic
    cv_rms = kfold_cv_base(rows, k=5)
    print(f"5-fold CV RMS (Model K base): {cv_rms:.4f} MeV (diagnostic, not gated)")

    # Fit operators
    print("\nOperator gating (each fitted on target family only):")
    op_names = ["op_82pre", "op_3d_odd", "op_dm_sat", "op_ms_fill"]
    op_results = {}
    n_passed = 0
    for op in op_names:
        gamma, family = fit_operator(rows, beta_K, op)
        improvements = []
        for iso in family:
            r = next(x for x in rows if x["isotope"] == iso)
            base_p = base_predict(r, beta_K)
            f = op_features(r)[op]
            new_resid = r["B_u_obs"] - (base_p + gamma * f)
            base_resid_iso = r["B_u_obs"] - base_p
            improvements.append(abs(base_resid_iso) - abs(new_resid))
        mean_imp = sum(improvements) / len(improvements) if improvements else 0
        passed = mean_imp > 2.0
        if passed:
            n_passed += 1
        op_results[op] = {
            "gamma": gamma,
            "family": family,
            "family_size": len(family),
            "mean_improve": mean_imp,
            "passed": passed,
        }
        print(f"  {op:14s}  γ={gamma:+.5f}  |F|={len(family):2d}  "
              f"mean_improve={mean_imp:+.3f}  → {'PASS' if passed else 'FAIL'}")
    g2 = n_passed >= 3
    print(f"G2 ≥3 of 4 operators pass: {n_passed}/4 → {'PASS' if g2 else 'FAIL'}")

    # Combined
    final_res = []
    for r in rows:
        base_p = base_predict(r, beta_K)
        correction = 0.0
        for op in op_names:
            if op_results[op]["passed"]:
                f = op_features(r)[op]
                correction += op_results[op]["gamma"] * f
        pred = base_p + correction
        final_res.append({
            "isotope": r["isotope"],
            "set": r["set"],
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"],
            "base_pred": base_p,
            "final_pred": pred,
            "final_resid": r["B_u_obs"] - pred,
        })
    final_rms = rms([x["final_resid"] for x in final_res])
    n_within = sum(1 for x in final_res if abs(x["final_resid"]) <= 5)
    g3 = final_rms <= 3.5
    g4 = n_within >= 45
    print(f"\nCombined: RMS = {final_rms:.4f} MeV, within 5 MeV = {n_within}/55")
    print(f"G3 combined RMS ≤ 3.5: {'PASS' if g3 else 'FAIL'}")
    print(f"G4 ≥ 45/55 within 5 MeV: {'PASS' if g4 else 'FAIL'}")

    # G5 anchors
    anchor_res = {}
    for a in ANCHORS:
        row = next((x for x in final_res if x["isotope"] == a), None)
        if row is None:
            anchor_res[a] = None
        else:
            anchor_res[a] = row["final_resid"]
    g5 = all(v is not None and abs(v) <= 10 for v in anchor_res.values())
    print(f"\nG5 anchors within 10 MeV:")
    for a, v in anchor_res.items():
        status = "MISS" if v is None else ("PASS" if abs(v) <= 10 else "FAIL")
        print(f"  {a:8s}  resid = {v}  [{status}]")
    print(f"G5 all anchors PASS: {'PASS' if g5 else 'FAIL'}")

    # Write residuals CSV
    with open(OUT_RESIDUALS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["isotope", "set", "Z", "N", "A", "B_u_obs",
                    "base_pred", "base_resid",
                    "final_pred", "final_resid",
                    "in_op_82pre", "in_op_3d_odd", "in_op_dm_sat", "in_op_ms_fill"])
        for x, br in zip(final_res, base_res):
            row_orig = next(rr for rr in rows if rr["isotope"] == x["isotope"])
            w.writerow([x["isotope"], x["set"], x["Z"], x["N"], x["A"],
                        f"{x['obs']:.4f}",
                        f"{br['base_pred']:.4f}", f"{br['base_resid']:.4f}",
                        f"{x['final_pred']:.4f}", f"{x['final_resid']:.4f}",
                        int(in_family(row_orig, "op_82pre")),
                        int(in_family(row_orig, "op_3d_odd")),
                        int(in_family(row_orig, "op_dm_sat")),
                        int(in_family(row_orig, "op_ms_fill"))])

    # Operators CSV
    with open(OUT_OPERATORS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["operator", "gamma", "family_size", "family_isotopes",
                    "mean_improve_MeV", "adopted"])
        for op in op_names:
            r = op_results[op]
            w.writerow([op, f"{r['gamma']:.5f}", r["family_size"],
                        ";".join(r["family"]), f"{r['mean_improve']:.4f}",
                        int(r["passed"])])

    # Determine verdict
    g6 = precommit_ok and fit_ok and len(FORBIDDEN_OPENED) == 0
    all_gates = [g0, g1, g2, g3, g4, g5, g6]
    print(f"\nG6 hashes + whitelist: precommit={precommit_ok}, "
          f"input={fit_ok}, forbidden_opens={len(FORBIDDEN_OPENED)}")
    print(f"G6 PASS: {g6}")

    if all(all_gates):
        verdict = "PASS"
    elif g0 and g6 and sum([g1, g2, g3, g4]) >= 2:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"\nVERDICT: {verdict}")

    # Remaining outliers for reporting
    outliers = [x for x in final_res if abs(x["final_resid"]) > 5]

    summary = {
        "cr": "CR274",
        "verdict": verdict,
        "gates": {
            "G0_cipher_exact": g0,
            "G1_base_RMS_leq_4.5": g1,
            "G2_operators_geq_3_pass": g2,
            "G3_combined_RMS_leq_3.5": g3,
            "G4_within_5MeV_geq_45": g4,
            "G5_anchors_within_10MeV": g5,
            "G6_hash_whitelist": g6,
        },
        "metrics": {
            "cipher_max_deviation_num": max_dev.numerator,
            "cipher_max_deviation_den": max_dev.denominator,
            "base_RMS_MeV": base_rms,
            "base_5fold_CV_RMS_MeV": cv_rms,
            "base_outliers_gt_5MeV": n_base_out,
            "n_operators_passed": n_passed,
            "combined_RMS_MeV": final_rms,
            "within_5MeV_count": n_within,
            "within_5MeV_fraction": n_within / 55,
            "n_outliers_gt_5MeV": len(outliers),
        },
        "beta_K": beta_K,
        "operators": {
            op: {
                "gamma": r["gamma"],
                "family_size": r["family_size"],
                "family": r["family"],
                "mean_improve_MeV": r["mean_improve"],
                "adopted": r["passed"],
            } for op, r in op_results.items()
        },
        "anchors": {a: v for a, v in anchor_res.items()},
        "outliers": [{"isotope": x["isotope"], "Z": x["Z"], "N": x["N"],
                      "A": x["A"], "final_resid": x["final_resid"]}
                     for x in outliers],
        "stewardship_hash": STEWARDSHIP_HASH,
        "precommit_hash": PRECOMMIT_HASH,
    }

    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)

    # Write result.md
    write_result(verdict, summary, final_res, base_res, op_results,
                 anchor_res, outliers, cv_rms)

    # HASHES.txt
    with open(OUT_HASHES, "w") as f:
        f.write("# CR274 hashes\n\n")
        f.write(f"CR274_PRECOMMIT.md sha256 = {file_sha256(PRECOMMIT_PATH)}\n")
        f.write(f"CR274_runner.py sha256 = {file_sha256(os.path.abspath(__file__))}\n")
        f.write(f"CR274_summary.json sha256 = {file_sha256(OUT_SUMMARY)}\n")
        f.write(f"CR274_residuals.csv sha256 = {file_sha256(OUT_RESIDUALS)}\n")
        f.write(f"CR274_operators.csv sha256 = {file_sha256(OUT_OPERATORS)}\n")
        f.write("\n# Input files (hash-locked)\n")
        f.write(f"CR261_bw_fit_per_row.csv sha256 = {file_sha256(FIT_CSV)}\n")
        f.write(f"\nstewardship sha256 = {STEWARDSHIP_HASH}\n")

    # result.md hash last
    result_hash = file_sha256(OUT_RESULT)
    with open(OUT_HASHES, "a") as f:
        f.write(f"CR274_result.md sha256 = {result_hash}\n")

    print(f"\nWritten: {OUT_SUMMARY}")
    print(f"Written: {OUT_RESULT}")
    print(f"Written: {OUT_RESIDUALS}")
    print(f"Written: {OUT_OPERATORS}")
    print(f"Written: {OUT_HASHES}")

    return verdict


def write_result(verdict, summary, final_res, base_res, op_results,
                 anchor_res, outliers, cv_rms):
    beta_K = summary["beta_K"]
    m = summary["metrics"]
    lines = []
    lines.append("# CR274 — Gated Nuclear-Readout Operators for CR261 Binding Closure")
    lines.append("")
    lines.append(f"**Verdict:** {verdict}")
    lines.append(f"**Stewardship:** `{STEWARDSHIP_HASH}`")
    lines.append(f"**Precommit:** `{PRECOMMIT_HASH}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    lines.append("| gate | requirement | result | status |")
    lines.append("| --- | --- | --- | --- |")
    dev = f"num={m['cipher_max_deviation_num']}, den={m['cipher_max_deviation_den']}"
    lines.append(f"| G0 | cipher exact on all 55 | max|dev|={dev} | "
                 f"{'PASS' if summary['gates']['G0_cipher_exact'] else 'FAIL'} |")
    lines.append(f"| G1 | base Model K RMS ≤ 4.5 MeV | {m['base_RMS_MeV']:.4f} | "
                 f"{'PASS' if summary['gates']['G1_base_RMS_leq_4.5'] else 'FAIL'} |")
    lines.append(f"| G2 | ≥3 of 4 operators pass | {m['n_operators_passed']}/4 | "
                 f"{'PASS' if summary['gates']['G2_operators_geq_3_pass'] else 'FAIL'} |")
    lines.append(f"| G3 | combined RMS ≤ 3.5 MeV | {m['combined_RMS_MeV']:.4f} | "
                 f"{'PASS' if summary['gates']['G3_combined_RMS_leq_3.5'] else 'FAIL'} |")
    lines.append(f"| G4 | ≥45/55 within 5 MeV | {m['within_5MeV_count']}/55 | "
                 f"{'PASS' if summary['gates']['G4_within_5MeV_geq_45'] else 'FAIL'} |")
    anchors_str = ", ".join(f"{a}={v:+.3f}" for a, v in anchor_res.items())
    lines.append(f"| G5 | anchors within 10 MeV | {anchors_str} | "
                 f"{'PASS' if summary['gates']['G5_anchors_within_10MeV'] else 'FAIL'} |")
    lines.append(f"| G6 | hashes + whitelist | precommit/input verified | "
                 f"{'PASS' if summary['gates']['G6_hash_whitelist'] else 'FAIL'} |")
    lines.append("")

    lines.append("## Model K coefficients (fitted, d locked from CR245)")
    lines.append("")
    lines.append("```text")
    for k in ["vol", "surf", "coul", "asym", "pair",
              "quadZ_A", "quadN_A", "quad_cross_A2",
              "shell_prox", "lightodd",
              "alpha", "reonset", "doubmag"]:
        lines.append(f"  {k:16s} = {beta_K[k]:+.5f}")
    lines.append("```")
    lines.append("")

    lines.append("## Operator adoption")
    lines.append("")
    lines.append("| operator | γ | |F| | family | mean_improve MeV | verdict |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for op in ["op_82pre", "op_3d_odd", "op_dm_sat", "op_ms_fill"]:
        r = op_results[op]
        fam = ", ".join(r["family"])
        adopt = "ADOPT" if r["passed"] else "REJECT"
        lines.append(f"| `{op}` | {r['gamma']:+.4f} | {r['family_size']} | "
                     f"{fam} | {r['mean_improve']:+.3f} | {adopt} |")
    lines.append("")

    lines.append("## Result summary")
    lines.append("")
    lines.append(f"- Base Model K RMS (all 55): **{m['base_RMS_MeV']:.4f} MeV**")
    lines.append(f"- Base Model K 5-fold CV RMS: {cv_rms:.4f} MeV (diagnostic)")
    lines.append(f"- Base outliers (|resid|>5): {m['base_outliers_gt_5MeV']}/55")
    lines.append(f"- Combined (base + adopted ops) RMS: **{m['combined_RMS_MeV']:.4f} MeV**")
    lines.append(f"- Combined within 5 MeV: **{m['within_5MeV_count']}/55 "
                 f"({m['within_5MeV_fraction']*100:.1f}%)**")
    lines.append(f"- Remaining outliers: {m['n_outliers_gt_5MeV']}/55")
    lines.append("")

    lines.append("## Anchor cases")
    lines.append("")
    lines.append("| anchor | Z | N | A | B_u_obs | final_pred | resid | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for a in ANCHORS:
        row = next((x for x in final_res if x["isotope"] == a), None)
        if row is None:
            lines.append(f"| {a} | - | - | - | - | - | - | MISS |")
        else:
            status = "PASS" if abs(row["final_resid"]) <= 10 else "FAIL"
            lines.append(f"| {a} | {row['Z']} | {row['N']} | {row['A']} | "
                         f"{row['obs']:+.3f} | {row['final_pred']:+.3f} | "
                         f"{row['final_resid']:+.3f} | {status} |")
    lines.append("")

    lines.append("## Remaining outliers (|resid| > 5 MeV)")
    lines.append("")
    if outliers:
        lines.append("| isotope | Z | N | A | resid MeV | family membership |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for x in outliers:
            fam = []
            row_orig = {"Z": x["Z"], "N": x["N"], "A": x["A"]}
            for op in ["op_82pre", "op_3d_odd", "op_dm_sat", "op_ms_fill"]:
                if in_family(row_orig, op):
                    fam.append(op)
            fam_str = ", ".join(fam) if fam else "none (Phase 7 candidate)"
            lines.append(f"| {x['isotope']} | {x['Z']} | {x['N']} | {x['A']} | "
                         f"{x['final_resid']:+.3f} | {fam_str} |")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Per-isotope residuals (full)")
    lines.append("")
    lines.append("| isotope | set | Z | N | A | B_u_obs | base_resid | final_resid |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for x, br in zip(final_res, base_res):
        lines.append(f"| {x['isotope']} | {x['set']} | {x['Z']} | {x['N']} | "
                     f"{x['A']} | {x['obs']:+.3f} | {br['base_resid']:+.3f} | "
                     f"{x['final_resid']:+.3f} |")
    lines.append("")

    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- CR261_bw_fit_per_row.csv sha256 = `{FIT_HASH}`")
    lines.append(f"- Precommit sha256 = `{PRECOMMIT_HASH}`")
    lines.append(f"- Stewardship sha256 = `{STEWARDSHIP_HASH}`")
    lines.append("")

    with open(OUT_RESULT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    verdict = main()
    sys.exit(0 if verdict in ("PASS", "BOUNDARY") else 1)
