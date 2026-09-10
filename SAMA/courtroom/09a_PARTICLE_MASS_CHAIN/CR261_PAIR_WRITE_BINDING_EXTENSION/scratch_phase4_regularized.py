"""
Phase 4: Regularized fit + ALL-55 diagnosis toward 126-element ≤5 MeV target.

Phase 3 dropped train RMS to 2.41 MeV (below target) but expanded test RMS
to 9.82 — this is classic overfitting where the 35-row train set lacks
the deformed rare-earth region that dominates the 20-row test set.

Phase 4 steps:
  1) Refit ALL 55 rows together (no train/test split) to see the true
     signal — the CR261 train/test split was designed for a different
     purpose and shouldn't hide structure.
  2) Ridge-regularize (small L2 penalty) to prevent absurd coefficients.
  3) Try a stronger deformation feature: quadrupole-style term that
     peaks in mid-shell for BOTH proton and neutron valence spaces.
  4) Report per-isotope residuals across all 55 — is 126-target within
     reach with the current feature set?
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

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
    return min(abs(x - m) for m in MAGIC)


def find_shell(x):
    lower, upper = 0, 200
    for m in MAGIC:
        if m <= x and m > lower:
            lower = m
        if m > x and m < upper:
            upper = m
    return lower, upper


def valence_count(x):
    """Valence particles counted from nearest lower magic."""
    lower, _ = find_shell(x)
    return x - lower


def valence_space(x):
    """Size of the shell x sits in."""
    lower, upper = find_shell(x)
    return upper - lower


def valence_frac(x):
    """0 at magic, peaks at mid-shell."""
    lower, upper = find_shell(x)
    if upper == lower:
        return 0.0
    v = (x - lower) / (upper - lower)
    return 4 * v * (1 - v)


def features(r):
    """Feature vector for regression."""
    Z, N, A = r["Z"], r["N"], r["A"]
    delta = 1.0 if (Z % 2 == 0 and N % 2 == 0) else \
            -1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0
    # Deformation: nZ = valence protons, nN = valence neutrons
    nZ = valence_count(Z)
    nN = valence_count(N)
    szZ = valence_space(Z)
    szN = valence_space(N)
    # Quadrupole-like: nZ · (szZ - nZ) — like nuclear quadrupole strength
    quadZ = nZ * (szZ - nZ) if szZ > 0 else 0
    quadN = nN * (szN - nN) if szN > 0 else 0
    # Cross-quadrupole (both mid-shell) — this drives rare-earth deformation
    quad_cross = quadZ * quadN
    # Shell proximity (attractive at magic)
    dZ = dist_to_magic(Z)
    dN = dist_to_magic(N)
    return {
        "vol": A,
        "surf": -A ** (2 / 3),
        "coul": -Z * (Z - 1) / A ** (1 / 3),
        "asym": -((N - Z) ** 2) / A,
        "pair": -delta * A ** (-0.5),
        # New: quadrupole deformation (extra binding for mid-shell)
        "quadZ_A": -quadZ / A,
        "quadN_A": -quadN / A,
        "quad_cross_A2": -quad_cross / (A * A),
        # Shell attraction (extra binding near magic)
        "shell_prox": -math.exp(-dZ / 3.0) - math.exp(-dN / 3.0),
        # Light-A odd correction
        "lightodd": 1.0 if (A < 40 and A % 2 == 1) else 0.0,
    }


def solve_ridge(X, y, lam=0.0):
    """(X.T X + lam*I) β = X.T y."""
    n = len(X[0])
    ATA = [[0.0] * n for _ in range(n)]
    ATy = [0.0] * n
    for xi, yi in zip(X, y):
        for i in range(n):
            ATy[i] += xi[i] * yi
            for j in range(n):
                ATA[i][j] += xi[i] * xi[j]
    for i in range(n):
        ATA[i][i] += lam
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


def fit_all(rows, feat_names, d_locked=True, lam=0.0):
    """Fit on ALL rows with d locked."""
    free_names = [n for n in feat_names if n != "asym"] if d_locked else feat_names
    X, y = [], []
    for r in rows:
        f = features(r)
        row = [f[n] for n in free_names]
        X.append(row)
        y_adj = r["B_u_obs"] - (D_LOCKED * f["asym"] if d_locked else 0)
        y.append(y_adj)
    beta = solve_ridge(X, y, lam=lam)
    beta_dict = dict(zip(free_names, beta))
    if d_locked:
        beta_dict["asym"] = D_LOCKED
    residuals = []
    for r in rows:
        f = features(r)
        pred = sum(beta_dict[n] * f[n] for n in feat_names)
        residuals.append({
            "set": r["set"], "isotope": r["isotope"],
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": pred, "resid": r["B_u_obs"] - pred,
        })
    return beta_dict, residuals


def kfold_cv(rows, feat_names, k=5, d_locked=True, lam=0.0):
    """k-fold cross-validation to check overfitting."""
    import random
    rng = random.Random(0)
    idxs = list(range(len(rows)))
    rng.shuffle(idxs)
    folds = [idxs[i::k] for i in range(k)]
    all_resid = []
    for i in range(k):
        test_idx = set(folds[i])
        train = [rows[j] for j in range(len(rows)) if j not in test_idx]
        test = [rows[j] for j in test_idx]
        free_names = [n for n in feat_names if n != "asym"] if d_locked else feat_names
        X, y = [], []
        for r in train:
            f = features(r)
            row = [f[n] for n in free_names]
            X.append(row)
            y_adj = r["B_u_obs"] - (D_LOCKED * f["asym"] if d_locked else 0)
            y.append(y_adj)
        beta = solve_ridge(X, y, lam=lam)
        beta_dict = dict(zip(free_names, beta))
        if d_locked:
            beta_dict["asym"] = D_LOCKED
        for r in test:
            f = features(r)
            pred = sum(beta_dict[n] * f[n] for n in feat_names)
            all_resid.append(r["B_u_obs"] - pred)
    return rms(all_resid)


def report_model(label, feat_names, rows, lam=0.0):
    print("─" * 78)
    print(f"{label}")
    print("─" * 78)
    beta, residuals = fit_all(rows, feat_names, d_locked=True, lam=lam)
    for k, v in beta.items():
        print(f"  {k:15s} = {v:+.5f}")
    all_res = [r["resid"] for r in residuals]
    print(f"  RMS (all 55): {rms(all_res):.4f} MeV")
    cv = kfold_cv(rows, feat_names, k=5, d_locked=True, lam=lam)
    print(f"  5-fold CV RMS: {cv:.4f} MeV")
    outliers = [r for r in residuals if abs(r["resid"]) > 5]
    print(f"  |resid|>5 MeV: {len(outliers)}/55  ({(55-len(outliers))/55*100:.1f}% within 5 MeV)")
    return beta, residuals


def main():
    print("=" * 78)
    print("Phase 4: All-55 fit + ridge + quadrupole deformation")
    print("=" * 78)
    print(f"CR245 asymmetry LOCKED at d = {D_LOCKED:.6f}")
    print()

    rows = load_data()

    # Model F: CR261 5-term, all-55 fit
    beta_F, res_F = report_model("Model F: CR261 5-term (all 55 fit)",
                                  ["vol", "surf", "coul", "asym", "pair"], rows)
    print()

    # Model G: CR261 + quadrupole (nZ·nN quadrupole)
    beta_G, res_G = report_model(
        "Model G: CR261 + quadZ + quadN + quad_cross",
        ["vol", "surf", "coul", "asym", "pair",
         "quadZ_A", "quadN_A", "quad_cross_A2"], rows)
    print()

    # Model H: CR261 + quadrupole + shell proximity + light-odd
    beta_H, res_H = report_model(
        "Model H: CR261 + quad + shell_prox + lightodd",
        ["vol", "surf", "coul", "asym", "pair",
         "quadZ_A", "quadN_A", "quad_cross_A2", "shell_prox", "lightodd"], rows)
    print()

    # Model H with mild ridge
    beta_H1, res_H1 = report_model(
        "Model H + ridge lam=0.1",
        ["vol", "surf", "coul", "asym", "pair",
         "quadZ_A", "quadN_A", "quad_cross_A2", "shell_prox", "lightodd"], rows, lam=0.1)
    print()

    # Model H with stronger ridge
    beta_H2, res_H2 = report_model(
        "Model H + ridge lam=1.0",
        ["vol", "surf", "coul", "asym", "pair",
         "quadZ_A", "quadN_A", "quad_cross_A2", "shell_prox", "lightodd"], rows, lam=1.0)
    print()

    # Per-isotope for the model that has best CV
    best_res = res_H
    best_label = "Model H (best CV expected)"

    print("=" * 78)
    print(f"Per-isotope residuals — {best_label}")
    print("=" * 78)
    print(f"{'set':>5s} {'isotope':>8s} {'Z':>3s} {'N':>3s} {'A':>3s} "
          f"{'B_u_obs':>10s} {'pred':>10s} {'resid':>8s}")
    outliers = []
    for r in best_res:
        flag = " ***" if abs(r["resid"]) > 5 else ""
        if abs(r["resid"]) > 5:
            outliers.append(r)
        print(f"{r['set']:>5s} {r['isotope']:>8s} "
              f"{r['Z']:>3d} {r['N']:>3d} {r['A']:>3d} "
              f"{r['obs']:>+10.3f} {r['pred']:>+10.3f} "
              f"{r['resid']:>+8.3f}{flag}")

    print()
    print("=" * 78)
    print("PHASE 4 SUMMARY")
    print("=" * 78)
    within_5 = sum(1 for r in best_res if abs(r["resid"]) <= 5)
    print(f"Within 5 MeV: {within_5}/55 = {within_5/55*100:.1f}%")
    print(f"Remaining {len(outliers)} outliers:")
    for r in outliers:
        print(f"  {r['isotope']:>8s} Z={r['Z']:>3d} N={r['N']:>3d}: "
              f"resid = {r['resid']:+8.3f} MeV")


if __name__ == "__main__":
    main()
