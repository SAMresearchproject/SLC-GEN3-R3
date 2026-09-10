"""
Phase 2: Derive volume/surface/Coulomb/pairing coefficients from substrate.

Strategy:
  1. Lock asymmetry from CR245: d = 7093²/(192·7117) ≈ 36.8181 MeV
  2. Compute "non-asymmetry" B_u: B_u_obs + d·(N−Z)²/A for each isotope
  3. On Z=N nuclei (asymmetry = 0), the entire B_u comes from
     volume + surface + Coulomb + pairing
  4. Look for structural expressions for the four remaining coefficients

Starting hypothesis:
  Standard SEMF has a_V ≈ 15.75, but CR261 has a = 8.174.
  Difference ≈ 7.68 MeV ≈ average nucleon mass excess:
    (Δ_p + Δ_n)/2 = (7.289 + 8.071)/2 = 7.68 MeV
  This is because CR261's B_u = mass excess (not binding energy),
  which subtracts the free-nucleon mass excess.
"""

import csv
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

# CR261 coefficients (fitted; d locked from CR245)
A_VOL = 8.1741
B_SUR = 19.7669
C_COUL = 0.5854
D_ASYM_LOCKED = 7093**2 / (192 * 7117)  # = 36.8181296...
E_PAIR = -41.8907

# CR220 cipher constants
G_p = 9.0625
G_e = 0.188802083333333
G_n = 0.015625
KAPPA = 7117 / 768  # 9.267...
GAP_UNIT = 7093 / 192  # 36.94...

# Nucleon mass excess (physics constants, for structural comparison)
DELTA_P_MeV = 7.28897  # hydrogen atom mass excess
DELTA_N_MeV = 8.07131  # neutron mass excess


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
                "B_u_pred_CR261": float(row["B_u_pred_MeV"]),
                "residual_CR261": float(row["residual_MeV"]),
            })
    return rows


def delta_pair(Z, N):
    """Pairing delta: +1 (even-even), 0 (odd-mass), -1 (odd-odd)."""
    if Z % 2 == 0 and N % 2 == 0:
        return 1
    if Z % 2 == 1 and N % 2 == 1:
        return -1
    return 0


def rms(vals):
    return math.sqrt(sum(v * v for v in vals) / len(vals)) if vals else 0.0


def main():
    print("=" * 78)
    print("Phase 2: Derive volume/surface/Coulomb/pairing from substrate")
    print("=" * 78)
    print()

    rows = load_data()

    # === Step 1: Verify subtracting locked asymmetry works ===
    print("Step 1: Non-asymmetry B_u (subtracting locked CR245 asymmetry)")
    print(f"  d_locked = 7093²/(192·7117) = {D_ASYM_LOCKED:.6f} MeV")
    print()

    for r in rows:
        asym = D_ASYM_LOCKED * (r["N"] - r["Z"])**2 / r["A"]
        r["B_u_non_asym"] = r["B_u_obs"] + asym  # observed volume+surface+Coul+pairing
        r["asymmetry_MeV"] = -asym
        r["delta_pair"] = delta_pair(r["Z"], r["N"])

    # === Step 2: Z=N sample (isolate volume/surface/Coulomb/pairing) ===
    z_eq_n_rows = [r for r in rows if r["Z"] == r["N"]]
    print(f"Step 2: Z=N nuclei (asymmetry = 0), all B_u from vol/surf/Coul/pair")
    print(f"        {len(z_eq_n_rows)} rows in dataset")
    print()
    print(f"{'isotope':>8s} {'Z':>3s} {'A':>3s} {'δ':>3s} "
          f"{'B_u_obs':>10s} {'CR261 vol':>10s} {'CR261 surf':>11s} "
          f"{'CR261 coul':>11s} {'CR261 pair':>11s}")
    print("-" * 90)
    for r in z_eq_n_rows:
        A = r["A"]
        Z = r["Z"]
        vol = A_VOL * A
        surf = -B_SUR * A**(2/3)
        coul = -C_COUL * Z * (Z - 1) / A**(1/3)
        pair = -E_PAIR * r["delta_pair"] / A**(0.5)
        cr261_sum = vol + surf + coul + pair
        print(f"{r['isotope']:>8s} {Z:>3d} {A:>3d} {r['delta_pair']:>+3d} "
              f"{r['B_u_obs']:>+10.3f} {vol:>+10.2f} {surf:>+11.2f} "
              f"{coul:>+11.2f} {pair:>+11.2f}")
    print()

    # === Step 3: Structural check on volume coefficient ===
    print("Step 3: Volume coefficient structural check")
    print(f"  Standard SEMF a_V ≈ 15.75 MeV")
    print(f"  CR261 fitted a = {A_VOL} MeV")
    print(f"  Difference = {15.75 - A_VOL:.3f} MeV")
    print(f"  Nucleon mass excess avg (Δ_p + Δ_n)/2 = "
          f"{(DELTA_P_MeV + DELTA_N_MeV)/2:.3f} MeV")
    print(f"  → CR261 a ≈ SEMF a_V - Δ_nucleon = {15.75 - (DELTA_P_MeV + DELTA_N_MeV)/2:.3f}")
    print(f"  Match to CR261's a = {A_VOL}?  "
          f"|diff| = {abs(A_VOL - (15.75 - (DELTA_P_MeV + DELTA_N_MeV)/2)):.3f} MeV")
    print()

    # === Step 4: Coulomb coefficient structural check ===
    print("Step 4: Coulomb coefficient structural check")
    print(f"  Standard c_C = 3/5 · e²/(4πε₀·r₀) ≈ 0.72 MeV")
    print(f"  CR261 fitted c = {C_COUL} MeV")
    print()
    # Try substrate-derived Coulomb: uses proton pair interaction
    # Each proton pair loses binding via retained_write channels
    # proton retained_write = 63.4375 per proton (from QP093A-0115)
    # If Coulomb term per pair ~ 63.4375 · μ_Q · 931.494 · some_factor ...
    ret_p = 63.4375
    print(f"  proton retained_write (from CR220) = {ret_p}")
    print(f"  μ_Q = 192/7117 = {192/7117:.10f}")
    print(f"  Try: ret_p · μ_Q · 931.494 / 8 · scale?")
    print(f"    ret_p · μ_Q · 931.494 = {ret_p * (192/7117) * 931.494:.3f} MeV")
    print(f"    /64 = {ret_p * (192/7117) * 931.494 / 64:.4f} MeV")
    print(f"    /128 = {ret_p * (192/7117) * 931.494 / 128:.4f} MeV")
    print()

    # === Step 5: Look for surface + pairing structural forms ===
    print("Step 5: Surface + pairing structural check")
    print(f"  Surface: CR261 b = {B_SUR}. 2·κ = {2*KAPPA:.4f}. "
          f"Ratio b/κ = {B_SUR/KAPPA:.4f}")
    print(f"  Pairing: CR261 e = {E_PAIR}. Related to nucleon mass excess * some factor?")
    print(f"    Δ_n - Δ_p = {DELTA_N_MeV - DELTA_P_MeV:.3f} MeV (small, +0.78)")
    print(f"    |e|/κ = {abs(E_PAIR)/KAPPA:.4f}")
    print()

    # === Step 6: Test CR261 formula RMS with COEFFICIENTS UNCHANGED but ===
    # === re-verify to make sure our understanding matches CR261's fit    ===
    print("Step 6: Verify CR261 formula reproduces fit predictions")
    train_res = []
    test_res = []
    for r in rows:
        A = r["A"]
        Z = r["Z"]
        N = r["N"]
        vol = A_VOL * A
        surf = -B_SUR * A**(2/3)
        coul = -C_COUL * Z * (Z - 1) / A**(1/3)
        asym = -D_ASYM_LOCKED * (N - Z)**2 / A
        pair = -E_PAIR * r["delta_pair"] / A**(0.5)
        B_u_pred_recomputed = vol + surf + coul + asym + pair
        our_residual = B_u_pred_recomputed - r["B_u_obs"]
        r["our_pred"] = B_u_pred_recomputed
        r["our_resid"] = our_residual
        if r["set"] == "train":
            train_res.append(our_residual)
        else:
            test_res.append(our_residual)
    print(f"  Recomputed formula train RMS = {rms(train_res):.4f} "
          f"(CR261 sealed = 5.555)")
    print(f"  Recomputed formula test RMS  = {rms(test_res):.4f} "
          f"(CR261 sealed = 8.574)")
    print()

    # === Step 7: Optimize a, b, c, e with d locked, check for improvement ===
    print("Step 7: Refit (a, b, c, e) with d LOCKED - can we do better?")
    print("        (least-squares fit on TRAIN set)")

    # Build linear system: B_u_obs + asymmetry_contribution = a·X_v + b·X_s + c·X_c + e·X_p
    # where X_v = A, X_s = -A^(2/3), X_c = -Z(Z-1)/A^(1/3), X_p = -δ/√A
    train_rows = [r for r in rows if r["set"] == "train"]
    X = []  # matrix of features
    y = []  # target
    for r in train_rows:
        A = r["A"]
        Z = r["Z"]
        asym = -D_ASYM_LOCKED * (r["N"] - r["Z"])**2 / A
        target = r["B_u_obs"] - asym  # subtract locked asymmetry
        X.append([A, -A**(2/3), -Z*(Z-1)/A**(1/3), -r["delta_pair"]/A**0.5])
        y.append(target)

    # Solve X·β = y (least squares)
    # β = (X^T X)^-1 X^T y
    n = len(X)
    m = 4
    # Compute X^T X
    XtX = [[sum(X[k][i]*X[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    # Compute X^T y
    Xty = [sum(X[k][i]*y[k] for k in range(n)) for i in range(m)]
    # Gauss-Jordan invert 4x4
    def inv4(M):
        aug = [row[:] + [1 if i==j else 0 for j in range(4)] for i, row in enumerate(M)]
        for i in range(4):
            pivot = aug[i][i]
            for j in range(8):
                aug[i][j] /= pivot
            for k in range(4):
                if k != i:
                    factor = aug[k][i]
                    for j in range(8):
                        aug[k][j] -= factor * aug[i][j]
        return [[aug[i][j+4] for j in range(4)] for i in range(4)]

    XtX_inv = inv4(XtX)
    beta = [sum(XtX_inv[i][j]*Xty[j] for j in range(m)) for i in range(m)]
    print(f"  Refitted (with d locked at {D_ASYM_LOCKED:.4f}):")
    print(f"    a = {beta[0]:.4f}   (CR261 fitted: {A_VOL})")
    print(f"    b = {beta[1]:.4f}   (CR261 fitted: {B_SUR})")
    print(f"    c = {beta[2]:.4f}   (CR261 fitted: {C_COUL})")
    print(f"    e = {beta[3]:.4f}   (CR261 fitted: {E_PAIR})")
    print()

    # Compute new residuals with refit
    new_train_res = []
    new_test_res = []
    per_isotope_new_resid = []
    for r in rows:
        A = r["A"]
        Z = r["Z"]
        N = r["N"]
        vol = beta[0] * A
        surf = -beta[1] * A**(2/3)
        coul = -beta[2] * Z * (Z - 1) / A**(1/3)
        asym = -D_ASYM_LOCKED * (N - Z)**2 / A
        pair = -beta[3] * r["delta_pair"] / A**0.5
        B_u_new = vol + surf + coul + asym + pair
        r["B_u_refit"] = B_u_new
        r["residual_refit"] = B_u_new - r["B_u_obs"]
        per_isotope_new_resid.append((r["isotope"], r["set"], r["residual_refit"]))
        if r["set"] == "train":
            new_train_res.append(r["residual_refit"])
        else:
            new_test_res.append(r["residual_refit"])
    print(f"  Refitted train RMS = {rms(new_train_res):.4f}")
    print(f"  Refitted test RMS  = {rms(new_test_res):.4f}")
    print()

    # === Step 8: Per-isotope residuals (find outliers > 5 MeV) ===
    print("Step 8: Per-isotope residuals (target: |resid| ≤ 5 MeV)")
    print()
    print("Isotopes with |residual| > 5 MeV (outliers preventing 126-target):")
    print(f"{'set':>5s} {'isotope':>8s} {'Z':>3s} {'N':>3s} {'A':>3s} "
          f"{'B_u_obs':>10s} {'refit resid':>12s} {'CR261 resid':>12s}")
    print("-" * 80)
    outliers = 0
    for r in rows:
        if abs(r["residual_refit"]) > 5:
            outliers += 1
            print(f"{r['set']:>5s} {r['isotope']:>8s} {r['Z']:>3d} {r['N']:>3d} "
                  f"{r['A']:>3d} {r['B_u_obs']:>+10.3f} "
                  f"{r['residual_refit']:>+12.3f} {r['residual_CR261']:>+12.3f}")
    within_5 = len(rows) - outliers
    print()
    print(f"  {within_5}/{len(rows)} isotopes within 5 MeV = "
          f"{within_5/len(rows)*100:.1f}%")
    print(f"  {outliers} isotopes still outside 5 MeV target")
    print()

    print("=" * 78)
    print("PHASE 2 SUMMARY")
    print("=" * 78)
    print(f"  CR245 asymmetry LOCKED at d = {D_ASYM_LOCKED:.6f}")
    print(f"  Refit (a, b, c, e): {beta[0]:.4f}, {beta[1]:.4f}, {beta[2]:.4f}, {beta[3]:.4f}")
    print(f"  Train RMS: {rms(new_train_res):.3f} (was 5.555)")
    print(f"  Test RMS:  {rms(new_test_res):.3f} (was 8.574)")
    print(f"  Within 5 MeV: {within_5}/{len(rows)}")
    print()
    print("  a ≈ SEMF a_V - Δ_nucleon (mass excess absorbed into volume)")
    print("  Need Phase 3 (shell corrections) to reduce outliers")


if __name__ == "__main__":
    main()
