"""
Phase 6b: Gated operators with FROZEN Model K base.

Refit-based gating (Phase 6a) let the least-squares ripple through the
base-K coefficients and move clean controls. The stricter — and truer to
"nuclear readout layer only" — approach is:

  1. Freeze all Model K coefficients (base tensor + Phase-5 corrections).
  2. For each candidate operator O_i, fit its coefficient γ_i on the
     TARGET FAMILY ONLY, minimizing family residual sum.
  3. Check: does O_i affect any clean control? Since γ_i × feature_i = 0
     outside the family (by construction of gated features), the answer
     is automatically NO.
  4. Adopt if family mean residual drops below 5 MeV.

This is fitted-mass-formula-proof: each operator is a per-family
correction that leaves the rest of the fit alone. It is a genuine
"nuclear-readout layer" — the tensor accounting from Phase 1 is
unchanged.
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


def op_features(r):
    Z, N, A = r["Z"], r["N"], r["A"]
    lowerN, upperN = find_shell(N)
    nN = N - lowerN
    # O_82_precursor
    f_op_82pre = (Z - 56) ** 2 if (N == 82 and Z > 56) else 0.0
    # O_3d_oddZ_pairing
    f_op_3d_odd = 1.0 if (Z % 2 == 1 and 20 < Z < 30) else 0.0
    # O_doubly-magic-saturation
    f_op_dm_sat = 1.0 if (Z in MAGIC_SET and N in MAGIC_SET and A >= 100) else 0.0
    # O_mid_shell_fill: Z in (28, 50], N in mid-shell 50-82
    f_op_ms_fill = nN if (28 < Z <= 50 and 50 < N < 82) else 0.0
    return {
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


def fit_base_K(rows):
    """Fit Model K on all 55, return frozen coefficients."""
    base_names = ["vol", "surf", "coul", "pair",
                  "quadZ_A", "quadN_A", "quad_cross_A2",
                  "shell_prox", "lightodd",
                  "alpha", "reonset", "doubmag"]
    X, y = [], []
    for r in rows:
        f = base_features(r)
        X.append([f[n] for n in base_names])
        y.append(r["B_u_obs"] - D_LOCKED * f["asym"])
    beta = solve_ridge(X, y)
    beta_dict = dict(zip(base_names, beta))
    beta_dict["asym"] = D_LOCKED
    return beta_dict


def base_predict(r, beta):
    f = base_features(r)
    return sum(beta[n] * f[n] for n in beta)


def in_family(iso, Z, N, A, family):
    if family == "op_82pre" and N == 82 and Z > 56:
        return True
    if family == "op_3d_odd" and Z % 2 == 1 and 20 < Z < 30:
        return True
    if family == "op_dm_sat" and Z in MAGIC_SET and N in MAGIC_SET and A >= 100:
        return True
    if family == "op_ms_fill" and 28 < Z <= 50 and 50 < N < 82:
        return True
    return False


def fit_operator(rows, beta_base, op_name):
    """
    Fit γ on TARGET FAMILY ONLY, minimizing sum of squared residuals
    on family isotopes. Since feature = 0 outside family, this doesn't
    affect any non-family isotope.

    γ = argmin Σ_family (r - γ*f_i)²
      = (Σ r*f_i) / (Σ f_i²)
    where r = residual after base = B_u_obs - B_u_pred_base
    """
    num = 0.0
    den = 0.0
    family_isos = []
    for r in rows:
        if not in_family(r["isotope"], r["Z"], r["N"], r["A"], op_name):
            continue
        family_isos.append(r["isotope"])
        f = op_features(r)[op_name]
        base_pred = base_predict(r, beta_base)
        resid = r["B_u_obs"] - base_pred
        num += resid * f
        den += f * f
    if den == 0:
        return 0.0, family_isos
    gamma = num / den
    return gamma, family_isos


def evaluate_frozen(rows, beta_base, base_residuals, op_name):
    print("─" * 78)
    print(f"Operator: {op_name}")
    print("─" * 78)
    gamma, family_isos = fit_operator(rows, beta_base, op_name)
    print(f"  Fitted γ = {gamma:+.5f}")
    print(f"  Target family: {family_isos}")
    print(f"  {'isotope':>8s} {'baseline':>9s} {'new':>9s} {'improve':>9s}")
    improvements = []
    new_residuals = {}
    for r in rows:
        base_pred = base_predict(r, beta_base)
        f = op_features(r)[op_name]
        new_pred = base_pred + gamma * f
        new_resid = r["B_u_obs"] - new_pred
        new_residuals[r["isotope"]] = {
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "resid": new_resid,
        }
    for iso in family_isos:
        base_abs = abs(base_residuals[iso]["resid"])
        new_abs = abs(new_residuals[iso]["resid"])
        improve = base_abs - new_abs
        improvements.append(improve)
        print(f"  {iso:>8s} "
              f"{base_residuals[iso]['resid']:>+9.3f} "
              f"{new_residuals[iso]['resid']:>+9.3f} "
              f"{improve:>+9.3f}")

    # Non-family isotopes are UNCHANGED (feature = 0)
    # so clean controls are automatically preserved
    print(f"  → Non-family isotopes unchanged (feature = 0 outside family)")

    # Family remaining outliers
    fam_outliers = [iso for iso in family_isos
                    if abs(new_residuals[iso]["resid"]) > 5]
    mean_impr = sum(improvements) / len(improvements) if improvements else 0
    print(f"  Family mean improvement: {mean_impr:+.3f} MeV")
    print(f"  Family remaining |resid|>5: {len(fam_outliers)}/{len(family_isos)}")

    # Overall
    all_res = [r["resid"] for r in new_residuals.values()]
    total_out = sum(1 for r in new_residuals.values() if abs(r["resid"]) > 5)
    print(f"  Overall RMS: {rms(all_res):.4f} MeV, outliers: {total_out}/55")

    gate_A = mean_impr > 2.0
    gate_B = True  # by construction, no non-family isotope changes
    print(f"  Gate A (family improves >2 MeV): {'PASS' if gate_A else 'FAIL'}")
    print(f"  Gate B (clean not worse):        AUTO-PASS (feature-gated)")
    verdict = "ADOPT" if gate_A else "REJECT"
    print(f"  → {verdict}")
    return {
        "op_name": op_name,
        "gamma": gamma,
        "family_isos": family_isos,
        "mean_impr": mean_impr,
        "verdict": verdict,
        "new_residuals": new_residuals,
    }


def main():
    print("=" * 78)
    print("Phase 6b: Gated operators with FROZEN Model K base")
    print("=" * 78)
    rows = load_data()

    # Fit base Model K
    beta_K = fit_base_K(rows)
    print("\nFrozen Model K coefficients:")
    for k, v in beta_K.items():
        print(f"  {k:18s} = {v:+.5f}")

    # Baseline residuals
    base_residuals = {}
    for r in rows:
        base_pred = base_predict(r, beta_K)
        base_residuals[r["isotope"]] = {
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": base_pred,
            "resid": r["B_u_obs"] - base_pred,
        }
    all_res = [r["resid"] for r in base_residuals.values()]
    n_out = sum(1 for r in base_residuals.values() if abs(r["resid"]) > 5)
    print(f"\nBaseline: RMS = {rms(all_res):.4f} MeV, outliers = {n_out}/55")
    print()

    # Evaluate each operator
    ops = ["op_82pre", "op_3d_odd", "op_dm_sat", "op_ms_fill"]
    results = []
    for op in ops:
        r = evaluate_frozen(rows, beta_K, base_residuals, op)
        results.append(r)
        print()

    # Combined: apply all adopted operators (since feature-gated, no interaction)
    adopted = [r for r in results if r["verdict"] == "ADOPT"]
    print("=" * 78)
    print(f"COMBINED with all adopted operators ({len(adopted)}):")
    print("=" * 78)
    for r in adopted:
        print(f"  {r['op_name']:15s} γ={r['gamma']:+.4f}  "
              f"mean improve={r['mean_impr']:+.3f} MeV")

    # Compose predictions
    combined_res = {}
    for r in rows:
        base_pred = base_predict(r, beta_K)
        correction = 0.0
        for op_result in adopted:
            f = op_features(r)[op_result["op_name"]]
            correction += op_result["gamma"] * f
        pred = base_pred + correction
        combined_res[r["isotope"]] = {
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "obs": r["B_u_obs"], "pred": pred,
            "resid": r["B_u_obs"] - pred,
        }

    all_res = [r["resid"] for r in combined_res.values()]
    n_out = sum(1 for r in combined_res.values() if abs(r["resid"]) > 5)
    print(f"\nCombined RMS: {rms(all_res):.4f} MeV, outliers: {n_out}/55 "
          f"= {(55-n_out)/55*100:.1f}% within 5 MeV")

    print("\nCombined outlier list:")
    for iso, r in combined_res.items():
        if abs(r["resid"]) > 5:
            print(f"  {iso:>8s} Z={r['Z']:>3d} N={r['N']:>3d}: "
                  f"resid = {r['resid']:+8.3f} MeV")


if __name__ == "__main__":
    main()
