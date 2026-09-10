"""
Phase 6: Four gated candidate operators (per second-set-of-eyes review).

Each operator must PASS two gates to be adopted:
  Gate A: improves the target family residuals meaningfully (>2 MeV mean drop)
  Gate B: does NOT worsen any currently-clean control (|resid|<5 stays <5,
          and no clean control degrades by more than 1.0 MeV)

Only operators that pass BOTH gates get incorporated. This keeps the fit
honest — the SAM tensor accounting stays sealed, only the nuclear-readout
layer changes, and each addition has to earn its place.

Baseline: Model K from Phase 5 (12 outliers, 78.2% within 5 MeV).

Four candidate operators (each with its own family and structural motivation):

  O_82_precursor:
    Target: Nd-142 (Z=60, N=82, resid −11.6)
    Family: N=82 isotones with Z > 56 (approaches doubly-magic proton
            territory but doesn't reach it)
    Feature: (Z − 56)² × [N == 82]  (positive → binds down, reducing
             over-prediction just above N=82 magic shell)
    Substrate motivation: Z valence starts eroding N=82 shell closure
    as protons stack above the Z=50-82 mid-shell.

  O_3d_oddZ_pairing:
    Target: Mn-55, Co-59, Cu-63 (odd-Z 3d transition metals)
    Family: (Z odd) AND (20 < Z < 30)
    Feature: indicator [Z odd, 20<Z<30]
    Substrate motivation: 3d shell has residual pairing debit not
    captured by SEMF δ term.

  O_doubmag_saturation:
    Target: Pb-208 (+7.2)
    Family: doubly-magic with A ≥ 100 (heavy doubly-magic)
    Feature: indicator [Z magic AND N magic AND A ≥ 100]
    Substrate motivation: at heavy doubly-magic, shell_prox saturates
    and current linear form over-shoots.

  O_midshell_fill:
    Target: Ag-107 (−9.2), Sn-120 (−6.7)
    Family: Z ∈ (28, 50] AND N ∈ (50, 82) — Z near Z=50 upper shell,
            N mid-shell 50–82
    Feature: n_N valence × [Z ∈ (28, 50]]
    Substrate motivation: Z=50 shell fills with N valence still
    building; the current quadrupole term over-predicts.
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
    """Baseline features from Model K (Phase 5) + four new operators."""
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

    # -- Phase 6 gated operators --
    # O_82_precursor: N=82 isotones with Z > 56
    f_op_82pre = (Z - 56) ** 2 if (N == 82 and Z > 56) else 0.0
    # O_3d_oddZ_pairing: odd Z in 3d shell
    f_op_3d_odd = 1.0 if (Z % 2 == 1 and 20 < Z < 30) else 0.0
    # O_doubmag_sat: heavy doubly-magic
    f_op_dm_sat = 1.0 if (Z in MAGIC_SET and N in MAGIC_SET and A >= 100) else 0.0
    # O_midshell_fill: Z in (28, 50], N in (50, 82) — mid-shell filling
    f_op_ms_fill = nN if (28 < Z <= 50 and 50 < N < 82) else 0.0

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
        # Gated operators
        "op_82pre": f_op_82pre,
        "op_3d_odd": f_op_3d_odd,
        "op_dm_sat": f_op_dm_sat,
        "op_ms_fill": f_op_ms_fill,
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


def fit_and_residuals(rows, feat_names, lam=0.0):
    free_names = [n for n in feat_names if n != "asym"]
    X, y = [], []
    for r in rows:
        f = features(r)
        X.append([f[n] for n in free_names])
        y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
    beta = solve_ridge(X, y, lam=lam)
    beta_dict = dict(zip(free_names, beta))
    beta_dict["asym"] = D_LOCKED
    residuals = {}
    for r in rows:
        f = features(r)
        pred = sum(beta_dict[n] * f[n] for n in feat_names)
        residuals[r["isotope"]] = {
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": pred,
            "resid": r["B_u_obs"] - pred,
        }
    return beta_dict, residuals


BASE_K = ["vol", "surf", "coul", "asym", "pair",
          "quadZ_A", "quadN_A", "quad_cross_A2",
          "shell_prox", "lightodd",
          "alpha", "reonset", "doubmag"]


def in_family(iso, Z, N, A, family):
    """Which family an isotope belongs to (or None)."""
    if family == "82pre" and N == 82 and Z > 56:
        return True
    if family == "3d_odd" and Z % 2 == 1 and 20 < Z < 30:
        return True
    if family == "dm_sat" and Z in MAGIC_SET and N in MAGIC_SET and A >= 100:
        return True
    if family == "ms_fill" and 28 < Z <= 50 and 50 < N < 82:
        return True
    return False


def evaluate_operator(rows, baseline_res, op_name, op_feature):
    """
    Fit BASE_K + op_feature, compare to baseline.
    Report:
      - target family residual improvement
      - worst degradation on clean controls (|resid|<5 in baseline)
      - Gate A: family improves by mean > 2 MeV
      - Gate B: no clean control degrades by > 1 MeV
    """
    print("─" * 78)
    print(f"Operator: {op_name}")
    print("─" * 78)

    feats = BASE_K + [op_feature]
    beta, new_res = fit_and_residuals(rows, feats)
    print(f"  Fitted coefficient for {op_feature}: {beta[op_feature]:+.4f}")

    # Family analysis
    family_key = op_feature.replace("op_", "")
    family_isos = [iso for iso, r in baseline_res.items()
                   if in_family(iso, r["Z"], r["N"], r["A"], family_key)]

    print(f"  Target family ({family_key}): {family_isos}")
    print(f"  {'isotope':>8s} {'baseline':>9s} {'new':>9s} {'improve':>9s}")
    fam_improvements = []
    for iso in family_isos:
        base_abs = abs(baseline_res[iso]["resid"])
        new_abs = abs(new_res[iso]["resid"])
        improve = base_abs - new_abs
        fam_improvements.append(improve)
        print(f"  {iso:>8s} "
              f"{baseline_res[iso]['resid']:>+9.3f} "
              f"{new_res[iso]['resid']:>+9.3f} "
              f"{improve:>+9.3f}")

    if fam_improvements:
        mean_improve = sum(fam_improvements) / len(fam_improvements)
        print(f"  Family mean improvement: {mean_improve:+.3f} MeV")
        gate_A = mean_improve > 2.0
    else:
        mean_improve = 0
        gate_A = False
        print("  Family empty — no isotopes to test")

    # Clean control analysis
    clean_isos = [iso for iso, r in baseline_res.items()
                  if abs(r["resid"]) < 5.0 and iso not in family_isos]
    worst_degrade = 0.0
    worst_iso = None
    n_broken = 0
    for iso in clean_isos:
        base_abs = abs(baseline_res[iso]["resid"])
        new_abs = abs(new_res[iso]["resid"])
        degrade = new_abs - base_abs
        if degrade > worst_degrade:
            worst_degrade = degrade
            worst_iso = iso
        if new_abs > 5.0:
            n_broken += 1

    print(f"  Clean controls: {len(clean_isos)} baseline-clean isotopes")
    print(f"  Worst degradation: {worst_iso} {worst_degrade:+.3f} MeV")
    print(f"  Newly-broken clean controls: {n_broken}")
    gate_B = worst_degrade < 1.0 and n_broken == 0

    all_res = [r["resid"] for r in new_res.values()]
    n_out = sum(1 for r in new_res.values() if abs(r["resid"]) > 5)
    print(f"  Overall RMS: {rms(all_res):.4f} MeV, outliers: {n_out}/55")

    print(f"  Gate A (family improves): {'PASS' if gate_A else 'FAIL'}")
    print(f"  Gate B (clean not worse): {'PASS' if gate_B else 'FAIL'}")
    verdict = "ADOPT" if (gate_A and gate_B) else "REJECT"
    print(f"  → {verdict}")
    return {
        "feat": op_feature,
        "verdict": verdict,
        "beta": beta,
        "residuals": new_res,
        "family_improve": mean_improve,
        "worst_degrade": worst_degrade,
        "n_broken": n_broken,
    }


def main():
    print("=" * 78)
    print("Phase 6: Gated candidate operators")
    print("=" * 78)
    rows = load_data()

    # Baseline: Model K
    print("\nBaseline: Model K from Phase 5")
    beta_K, res_K = fit_and_residuals(rows, BASE_K)
    all_res = [r["resid"] for r in res_K.values()]
    n_out = sum(1 for r in res_K.values() if abs(r["resid"]) > 5)
    print(f"  RMS: {rms(all_res):.4f}   outliers: {n_out}/55")
    print()

    # Each operator gated separately
    ops = [
        ("O_82_precursor", "op_82pre"),
        ("O_3d_oddZ_pairing", "op_3d_odd"),
        ("O_doubly_magic_saturation", "op_dm_sat"),
        ("O_mid_shell_fill", "op_ms_fill"),
    ]

    verdicts = []
    for name, feat in ops:
        result = evaluate_operator(rows, res_K, name, feat)
        verdicts.append((name, feat, result))
        print()

    # Combine all adopted operators
    adopted = [feat for _, feat, r in verdicts if r["verdict"] == "ADOPT"]
    print("=" * 78)
    print("COMBINED MODEL — adopting only operators that passed BOTH gates")
    print("=" * 78)
    print(f"Adopted: {adopted}")
    print()

    if adopted:
        combo_feats = BASE_K + adopted
        beta_combo, res_combo = fit_and_residuals(rows, combo_feats)
        for k, v in beta_combo.items():
            print(f"  {k:18s} = {v:+.5f}")
        all_res = [r["resid"] for r in res_combo.values()]
        n_out = sum(1 for r in res_combo.values() if abs(r["resid"]) > 5)
        print(f"\n  Combined RMS: {rms(all_res):.4f} MeV")
        print(f"  Combined outliers: {n_out}/55 "
              f"({(55-n_out)/55*100:.1f}% within 5 MeV)")
        print()
        print("Outlier list:")
        for iso, r in res_combo.items():
            if abs(r["resid"]) > 5:
                print(f"  {iso:>8s} Z={r['Z']:>3d} N={r['N']:>3d}: "
                      f"resid = {r['resid']:+8.3f} MeV")
    else:
        print("No operators passed both gates.")


if __name__ == "__main__":
    main()
