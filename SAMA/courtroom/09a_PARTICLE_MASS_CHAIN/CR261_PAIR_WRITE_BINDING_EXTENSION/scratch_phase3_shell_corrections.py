"""
Phase 3: Shell + deformation corrections toward 126-element ≤5 MeV target.

Phase 2 confirmed CR261 (a=8.174, b=19.767, c=0.5854, d=36.818 LOCKED,
e=-41.89) is the least-squares optimum for that functional form.
The 27/55 outliers cluster in three families:

  A) DEFORMED rare-earth region (mid-shell 82<N<126, 60≤Z≤78):
     Nd-142 +17.5, Er-166 +13.2, Yb-172 +10.9, Hf-178 +9.1, W-184 +6.6,
     Pt-194 +10.2, Dy-162 +6.6, U-234 +14.3
     → underbound because SEMF assumes sphericity; deformation adds binding

  B) MAGIC SHELL closures:
     Pb-208 (Z=82, N=126) -11.5, Ba-138 (N=82) -13.8, Ni-58 (Z=28) +6.3,
     Zn-64 (Z=30) +9.6, Zr-90 (N=50) +9.6
     → the pairing term isn't enough to capture shell energy at closures

  C) LIGHT odd-Z:
     O-17, Na-23, Mg-25, Al-27, P-31 (all Z≤15, A odd, residual -5 to -7)
     → over-corrected pairing for light odd-A

Approach: add substrate-motivated corrections layered on CR261 baseline.

  Term 1: shell energy at magic Z, N ∈ {2, 8, 20, 28, 50, 82, 126}
          E_shell = γ · (proximity to magic) with saturation
  Term 2: mid-shell deformation
          E_def = β · valence_pairs_between_closures / A
  Term 3: light odd-A correction
          Small pairing tweak for A < 40 odd

Fit with (d LOCKED at 7093²/(192·7117)); other CR261 coefficients free to
adjust; add three new shell/deformation terms.
"""

import csv
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

# CR245 asymmetry (LOCKED)
GAP_NUM = 7093
GAP_DEN = 192
KAPPA_NUM = 7117
KAPPA_DEN = 768
D_LOCKED = (GAP_NUM * GAP_NUM) / (GAP_DEN * KAPPA_NUM)  # 36.818130

MAGIC = [2, 8, 20, 28, 50, 82, 126]


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Z = int(row["Z"])
            N = int(row["N"])
            A = int(row["A"])
            rows.append({
                "set": row["set"],
                "isotope": row["isotope"],
                "Z": Z, "N": N, "A": A,
                "B_u_obs": float(row["B_u_obs_MeV"]),
            })
    return rows


def dist_to_magic(x):
    """Distance from x to nearest magic number."""
    return min(abs(x - m) for m in MAGIC)


def find_shell(x):
    """Return (m_lower, m_upper) magic bracket containing x."""
    lower = 0
    upper = 200
    for m in MAGIC:
        if m <= x and m > lower:
            lower = m
        if m > x and m < upper:
            upper = m
    return lower, upper


def valence_frac(x):
    """
    Mid-shell valence fraction 0 at magic, peaks at mid-shell.
    Returns v·(1-v)·4 where v = position in shell (0..1).
    """
    lower, upper = find_shell(x)
    if upper == lower:
        return 0.0
    span = upper - lower
    v = (x - lower) / span
    return 4 * v * (1 - v)


def features(r):
    """Compute feature vector for row r. Returns dict of feature values."""
    Z, N, A = r["Z"], r["N"], r["A"]
    delta = 1.0 if (Z % 2 == 0 and N % 2 == 0) else \
            -1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0
    # CR261 features
    f_vol = A
    f_surf = -A ** (2 / 3)
    f_coul = -Z * (Z - 1) / A ** (1 / 3)
    f_asym = -((N - Z) ** 2) / A
    f_pair = -delta * A ** (-0.5)
    # New shell/deformation features
    # T1: proximity bonus at magic Z + magic N (negative distance in shell units)
    # Shell energy is NEGATIVE at closure (extra binding), so use −exp(−d/σ)
    dZ = dist_to_magic(Z)
    dN = dist_to_magic(N)
    f_shellZ = -math.exp(-dZ / 3.0)
    f_shellN = -math.exp(-dN / 3.0)
    # T2: mid-shell deformation (peaks between magic numbers)
    f_defZ = valence_frac(Z)
    f_defN = valence_frac(N)
    # T3: light odd-A correction
    f_lightodd = 1.0 if (A < 40 and A % 2 == 1) else 0.0
    # Deformation gives extra binding → sign not fixed, fit decides
    # Product v_Z · v_N is strongest for both-mid-shell (rare earths)
    f_def_prod = f_defZ * f_defN
    return {
        "vol": f_vol, "surf": f_surf, "coul": f_coul, "asym": f_asym,
        "pair": f_pair,
        "shellZ": f_shellZ, "shellN": f_shellN,
        "defZ": f_defZ, "defN": f_defN,
        "def_prod": f_def_prod,
        "lightodd": f_lightodd,
    }


def solve_normal(X, y):
    """Least squares (X.T X) β = X.T y via Gauss-Jordan."""
    n = len(X[0])
    ATA = [[0.0] * n for _ in range(n)]
    ATy = [0.0] * n
    for xi, yi in zip(X, y):
        for i in range(n):
            ATy[i] += xi[i] * yi
            for j in range(n):
                ATA[i][j] += xi[i] * xi[j]
    # Augment and solve
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    for i in range(n):
        # Pivot
        piv = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[piv] = M[piv], M[i]
        piv_val = M[i][i]
        if abs(piv_val) < 1e-12:
            raise RuntimeError(f"Singular at column {i}")
        for j in range(i, n + 1):
            M[i][j] /= piv_val
        for k in range(n):
            if k == i:
                continue
            factor = M[k][i]
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]
    return [M[i][n] for i in range(n)]


def predict(beta, feat, feat_names, d_locked_index=None, d_val=None):
    """Predict B_u given coefficients and features."""
    total = 0.0
    j = 0
    for name in feat_names:
        if name == "asym":
            total += d_val * feat[name]
        else:
            total += beta[j] * feat[name]
            j += 1
    return total


def rms(vals):
    return math.sqrt(sum(v * v for v in vals) / len(vals)) if vals else 0.0


def run_fit(rows, feat_names, d_locked=True):
    """
    Fit B_u_obs = sum_i beta_i * f_i(r).
    If d_locked, asym coefficient is fixed at D_LOCKED, others free.
    Returns (beta_dict, train_rms, test_rms, per_row_residuals).
    """
    train = [r for r in rows if r["set"] == "train"]
    all_feats = [features(r) for r in rows]

    if d_locked:
        free_names = [n for n in feat_names if n != "asym"]
    else:
        free_names = feat_names

    # Build X, y for training set
    X = []
    y = []
    for r in train:
        f = features(r)
        row = [f[n] for n in free_names]
        X.append(row)
        # If asym is locked, subtract its contribution from y
        if d_locked:
            y_adj = r["B_u_obs"] - D_LOCKED * f["asym"]
        else:
            y_adj = r["B_u_obs"]
        y.append(y_adj)

    beta = solve_normal(X, y)
    beta_dict = {name: b for name, b in zip(free_names, beta)}
    if d_locked:
        beta_dict["asym"] = D_LOCKED

    # Compute per-row residuals
    residuals = []
    for r in rows:
        f = features(r)
        pred = sum(beta_dict[n] * f[n] for n in feat_names)
        residuals.append({
            "set": r["set"], "isotope": r["isotope"],
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": pred, "resid": r["B_u_obs"] - pred,
        })
    train_res = [x["resid"] for x in residuals if x["set"] == "train"]
    test_res = [x["resid"] for x in residuals if x["set"] == "test"]
    return beta_dict, rms(train_res), rms(test_res), residuals


def main():
    print("=" * 78)
    print("Phase 3: Shell + deformation corrections")
    print("=" * 78)
    print(f"CR245 asymmetry LOCKED at d = {D_LOCKED:.6f}")
    print(f"Magic set: {MAGIC}")
    print()

    rows = load_data()
    print(f"Loaded {len(rows)} isotopes\n")

    # Baseline: CR261 5 terms with d locked
    print("─" * 78)
    print("Model A: CR261 baseline (5 terms, d LOCKED)")
    print("─" * 78)
    feats_A = ["vol", "surf", "coul", "asym", "pair"]
    beta, trms, tems, resA = run_fit(rows, feats_A, d_locked=True)
    for k, v in beta.items():
        print(f"  {k:10s} = {v:+.5f}")
    print(f"  train RMS = {trms:.4f}   test RMS = {tems:.4f}")
    out_A = sum(1 for r in resA if abs(r["resid"]) > 5)
    print(f"  isotopes |resid| > 5 MeV: {out_A}/{len(resA)}\n")

    # Model B: CR261 + shell (Z, N)
    print("─" * 78)
    print("Model B: CR261 + shell_Z + shell_N (7 terms)")
    print("─" * 78)
    feats_B = ["vol", "surf", "coul", "asym", "pair", "shellZ", "shellN"]
    beta, trms, tems, resB = run_fit(rows, feats_B, d_locked=True)
    for k, v in beta.items():
        print(f"  {k:10s} = {v:+.5f}")
    print(f"  train RMS = {trms:.4f}   test RMS = {tems:.4f}")
    out_B = sum(1 for r in resB if abs(r["resid"]) > 5)
    print(f"  isotopes |resid| > 5 MeV: {out_B}/{len(resB)}\n")

    # Model C: CR261 + shell + deformation
    print("─" * 78)
    print("Model C: CR261 + shell + deformation valence-fraction (9 terms)")
    print("─" * 78)
    feats_C = ["vol", "surf", "coul", "asym", "pair",
               "shellZ", "shellN", "defZ", "defN"]
    beta, trms, tems, resC = run_fit(rows, feats_C, d_locked=True)
    for k, v in beta.items():
        print(f"  {k:10s} = {v:+.5f}")
    print(f"  train RMS = {trms:.4f}   test RMS = {tems:.4f}")
    out_C = sum(1 for r in resC if abs(r["resid"]) > 5)
    print(f"  isotopes |resid| > 5 MeV: {out_C}/{len(resC)}\n")

    # Model D: CR261 + shell + deformation product + light odd
    print("─" * 78)
    print("Model D: CR261 + shell + def_product + light_odd (9 terms)")
    print("─" * 78)
    feats_D = ["vol", "surf", "coul", "asym", "pair",
               "shellZ", "shellN", "def_prod", "lightodd"]
    beta, trms, tems, resD = run_fit(rows, feats_D, d_locked=True)
    for k, v in beta.items():
        print(f"  {k:10s} = {v:+.5f}")
    print(f"  train RMS = {trms:.4f}   test RMS = {tems:.4f}")
    out_D = sum(1 for r in resD if abs(r["resid"]) > 5)
    print(f"  isotopes |resid| > 5 MeV: {out_D}/{len(resD)}\n")

    # Model E: everything together
    print("─" * 78)
    print("Model E: CR261 + shell_Z + shell_N + defZ + defN + def_prod + light_odd")
    print("─" * 78)
    feats_E = ["vol", "surf", "coul", "asym", "pair",
               "shellZ", "shellN", "defZ", "defN", "def_prod", "lightodd"]
    beta, trms, tems, resE = run_fit(rows, feats_E, d_locked=True)
    for k, v in beta.items():
        print(f"  {k:10s} = {v:+.5f}")
    print(f"  train RMS = {trms:.4f}   test RMS = {tems:.4f}")
    out_E = sum(1 for r in resE if abs(r["resid"]) > 5)
    print(f"  isotopes |resid| > 5 MeV: {out_E}/{len(resE)}\n")

    # Show best model per-isotope residuals
    print("=" * 78)
    print("Per-isotope residuals — Model E (all corrections)")
    print("=" * 78)
    print(f"{'set':>5s} {'isotope':>8s} {'Z':>3s} {'N':>3s} {'A':>3s} "
          f"{'B_u_obs':>10s} {'pred':>10s} {'resid':>8s} {'|>5?|':>6s}")
    print("-" * 80)
    outliers = []
    for r in resE:
        flag = " ***" if abs(r["resid"]) > 5 else ""
        if abs(r["resid"]) > 5:
            outliers.append(r)
        print(f"{r['set']:>5s} {r['isotope']:>8s} "
              f"{r['Z']:>3d} {r['N']:>3d} {r['A']:>3d} "
              f"{r['obs']:>+10.3f} {r['pred']:>+10.3f} "
              f"{r['resid']:>+8.3f}{flag}")

    print()
    print("=" * 78)
    print("PHASE 3 SUMMARY")
    print("=" * 78)
    print(f"Model A (baseline):  train={trms:.3f}  outliers=?")
    print(f"Best (Model E):      train_rms={trms:.4f}  test_rms={tems:.4f}")
    print(f"Within 5 MeV: {len(resE) - out_E}/{len(resE)} = "
          f"{(len(resE) - out_E) / len(resE) * 100:.1f}%")
    print(f"Remaining {out_E} outliers:")
    for r in outliers:
        print(f"  {r['isotope']:>8s} Z={r['Z']} N={r['N']}: "
              f"resid = {r['resid']:+.3f} MeV")


if __name__ == "__main__":
    main()
