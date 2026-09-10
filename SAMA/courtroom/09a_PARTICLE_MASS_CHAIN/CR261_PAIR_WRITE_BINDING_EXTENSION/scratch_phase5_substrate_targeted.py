"""
Phase 5: Targeted substrate-motivated features for remaining outlier families.

Model H from Phase 4 has 17 outliers grouped:
  A) α-cluster    : Si-28, S-32 (self-conjugate N=Z, A divisible by 4)
  B) rare-earth   : Nd-142, Er-166, Yb-172, Hf-178, Dy-162 (Z=60-72, N>82)
  C) doubly-magic : Pb-208 over-predicts
  D) odd-Z 3d     : Mn-55, Co-59, Cu-63

Substrate-motivated features:
  F_alpha:  count of α-quartets when N=Z AND A%4=0
            = A/4  (else 0)
            → extra binding proportional to number of Θ-quartets

  F_reonset: rare-earth onset — sharp turn-on above N=82 shell,
             turns off above N=126. Only activates when Z ∈ [50, 82].
             = max(0, (N-82))·max(0,(126-N))·(Z-50)·(82-Z)/normalization
             This peaks at (Z=66, N=104) — canonical rare-earth center.

  F_doubmag: doubly-magic saturation flag (Z magic AND N magic)
             → binds down the overshoot at Pb-208
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
D_LOCKED = (GAP_NUM * GAP_NUM) / (GAP_DEN * KAPPA_NUM)

MAGIC = [2, 8, 20, 28, 50, 82, 126]
MAGIC_SET = set(MAGIC)


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


def features(r):
    Z, N, A = r["Z"], r["N"], r["A"]
    delta = 1.0 if (Z % 2 == 0 and N % 2 == 0) else \
            -1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0
    dZ = dist_to_magic(Z)
    dN = dist_to_magic(N)
    # Quadrupole
    lowerZ, upperZ = find_shell(Z)
    lowerN, upperN = find_shell(N)
    nZ = Z - lowerZ
    nN = N - lowerN
    spZ = upperZ - lowerZ
    spN = upperN - lowerN
    quadZ = nZ * (spZ - nZ)
    quadN = nN * (spN - nN)
    # α-cluster feature
    f_alpha = (A // 4) if (N == Z and A % 4 == 0) else 0.0
    # Rare-earth deformation onset — bounded by Z=[50,82] and N=[82,126]
    if 50 < Z < 82 and 82 < N < 126:
        # normalized so peaks at 1 near (Z=66, N=104)
        zt = (Z - 50) * (82 - Z) / ((32/2)**2)   # peak = 1 at Z=66
        nt = (N - 82) * (126 - N) / ((44/2)**2)  # peak = 1 at N=104
        f_reonset = -zt * nt   # negative → extra binding
    else:
        f_reonset = 0.0
    # Doubly magic flag
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


def solve_ridge(X, y, lam=0.0):
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


def fit_all(rows, feat_names, lam=0.0):
    free_names = [n for n in feat_names if n != "asym"]
    X, y = [], []
    for r in rows:
        f = features(r)
        X.append([f[n] for n in free_names])
        y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
    beta = solve_ridge(X, y, lam=lam)
    beta_dict = dict(zip(free_names, beta))
    beta_dict["asym"] = D_LOCKED
    residuals = []
    for r in rows:
        f = features(r)
        pred = sum(beta_dict[n] * f[n] for n in feat_names)
        residuals.append({
            "set": r["set"], "isotope": r["isotope"],
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": pred,
            "resid": r["B_u_obs"] - pred,
        })
    return beta_dict, residuals


def kfold_cv(rows, feat_names, k=5, lam=0.0):
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
        free_names = [n for n in feat_names if n != "asym"]
        X, y = [], []
        for r in train:
            f = features(r)
            X.append([f[n] for n in free_names])
            y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
        beta = solve_ridge(X, y, lam=lam)
        beta_dict = dict(zip(free_names, beta))
        beta_dict["asym"] = D_LOCKED
        for r in test:
            f = features(r)
            pred = sum(beta_dict[n] * f[n] for n in feat_names)
            all_resid.append(r["B_u_obs"] - pred)
    return rms(all_resid)


def report(label, feat_names, rows, lam=0.0):
    print("─" * 78)
    print(label)
    print("─" * 78)
    beta, residuals = fit_all(rows, feat_names, lam=lam)
    for k, v in beta.items():
        print(f"  {k:15s} = {v:+.5f}")
    all_res = [r["resid"] for r in residuals]
    print(f"  RMS (all 55): {rms(all_res):.4f} MeV")
    cv = kfold_cv(rows, feat_names, k=5, lam=lam)
    print(f"  5-fold CV RMS: {cv:.4f} MeV")
    n_out = sum(1 for r in residuals if abs(r["resid"]) > 5)
    print(f"  |resid|>5: {n_out}/55  ({(55-n_out)/55*100:.1f}% within 5 MeV)")
    return beta, residuals


def main():
    print("=" * 78)
    print("Phase 5: Substrate-targeted features for 3 outlier families")
    print("=" * 78)
    rows = load_data()

    print("\nSanity check on new features:")
    for iso in ["Si-28", "S-32", "Ca-40", "Nd-142", "Er-166", "Pb-208", "Ba-138"]:
        r = next((x for x in rows if x["isotope"] == iso), None)
        if r is None:
            continue
        f = features(r)
        print(f"  {iso:8s}: alpha={f['alpha']:.2f}, reonset={f['reonset']:+.4f}, "
              f"doubmag={f['doubmag']:.0f}")
    print()

    base_H = ["vol", "surf", "coul", "asym", "pair",
              "quadZ_A", "quadN_A", "quad_cross_A2",
              "shell_prox", "lightodd"]

    # Model I: H + alpha
    _, _ = report("Model I: Model H + α-cluster",
                  base_H + ["alpha"], rows)
    print()

    # Model J: H + reonset
    _, _ = report("Model J: Model H + rare-earth onset",
                  base_H + ["reonset"], rows)
    print()

    # Model K: H + alpha + reonset + doubmag
    beta_K, res_K = report("Model K: Model H + α + reonset + doubly-magic",
                           base_H + ["alpha", "reonset", "doubmag"], rows)
    print()

    # Model L: K + ridge
    beta_L, res_L = report("Model L: Model K + ridge λ=0.1",
                           base_H + ["alpha", "reonset", "doubmag"], rows, lam=0.1)
    print()

    # Per-isotope report for Model K
    print("=" * 78)
    print("Per-isotope residuals — Model K")
    print("=" * 78)
    print(f"{'set':>5s} {'isotope':>8s} {'Z':>3s} {'N':>3s} {'A':>3s} "
          f"{'B_u_obs':>10s} {'pred':>10s} {'resid':>8s}")
    outliers = []
    for r in res_K:
        flag = " ***" if abs(r["resid"]) > 5 else ""
        if abs(r["resid"]) > 5:
            outliers.append(r)
        print(f"{r['set']:>5s} {r['isotope']:>8s} "
              f"{r['Z']:>3d} {r['N']:>3d} {r['A']:>3d} "
              f"{r['obs']:>+10.3f} {r['pred']:>+10.3f} "
              f"{r['resid']:>+8.3f}{flag}")

    print()
    print("=" * 78)
    print("PHASE 5 SUMMARY")
    print("=" * 78)
    print(f"Best model K: within 5 MeV: {55 - len(outliers)}/55 = "
          f"{(55 - len(outliers))/55*100:.1f}%")
    print(f"Remaining {len(outliers)} outliers:")
    for r in outliers:
        print(f"  {r['isotope']:>8s} Z={r['Z']:>3d} N={r['N']:>3d}: "
              f"resid = {r['resid']:+8.3f} MeV")


if __name__ == "__main__":
    main()
