"""
CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST runner.

Implements the test specified in CR019_PRECOMMIT.md (SHA-256
ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da).

Outputs:
  CR019_summary.json
  CR019_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import quad

# ---------------- substrate inputs (sealed identities) -----------------------
PI = math.pi
C_KMS = 299792.458

A_0 = 1.0 / (12.0 * PI)
OMEGA_M_SAM = 1.0 / PI
CHI = (8.0 / 3.0) * A_0
OMEGA_B_SAM = 2.0 * A_0 * (1.0 - CHI)

# ---------------- measurement inputs (external, not catalog fit) -------------
H0 = 68.76
T_CMB = 2.7255
N_EFF = 3.046

OMEGA_GAMMA_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4
REL_FACTOR = 1.0 + (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * N_EFF

# ---------------- Planck 2018 reference (base-LCDM TT,TE,EE+lowE+lensing) ----
PLANCK_Z_EQ          = 3402.0
PLANCK_Z_STAR        = 1089.92
PLANCK_Z_DRAG        = 1059.94
PLANCK_RS_ZSTAR      = 144.43
PLANCK_R_D           = 147.09
PLANCK_DM_ZSTAR      = 13869.6
PLANCK_ELL_A         = 301.76
PLANCK_100THETA_STAR = 1.04110

# ---------------- gates ------------------------------------------------------
P1_THRESH = 0.01   # 100*theta_*
P2_THRESH = 0.01   # ell_A
P3_THRESH = 0.01   # r_d

N_TRIALS = 1000


# ---------------- compressed-geometry computation ----------------------------

def compressed_geometry(Omega_m, Omega_b, H0_local):
    """Return dict with all compressed CMB geometry observables for
    given (Omega_m, Omega_b, H0). T_CMB and N_eff use module constants."""
    h = H0_local / 100.0
    wm = Omega_m * h * h
    wb = Omega_b * h * h
    Omega_r = OMEGA_GAMMA_H2 * REL_FACTOR / (h * h)
    Omega_DE = 1.0 - Omega_m - Omega_r

    # z_eq
    z_eq = wm / (OMEGA_GAMMA_H2 * REL_FACTOR) - 1.0

    # z_* (Hu-Sugiyama)
    g1 = 0.0783 * wb ** (-0.238) / (1.0 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * wb ** 1.81)
    z_star = 1048.0 * (1.0 + 0.00124 * wb ** (-0.738)) * (1.0 + g1 * wm ** g2)

    # z_drag (Eisenstein-Hu)
    b1 = 0.313 * wm ** (-0.419) * (1.0 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    z_drag = 1291.0 * wm ** 0.251 / (1.0 + 0.659 * wm ** 0.828) * (1.0 + b1 * wb ** b2)

    def E(z):
        return math.sqrt(Omega_m * (1.0 + z) ** 3 + Omega_r * (1.0 + z) ** 4 + Omega_DE)

    def cs(z):
        R = 0.75 * wb / OMEGA_GAMMA_H2 / (1.0 + z)
        return C_KMS / math.sqrt(3.0 * (1.0 + R))

    rs_zstar, _ = quad(lambda z: cs(z) / (H0_local * E(z)), z_star, np.inf, limit=400)
    rs_zd, _    = quad(lambda z: cs(z) / (H0_local * E(z)), z_drag, np.inf, limit=400)

    DM_zstar_int, _ = quad(lambda x: 1.0 / E(x), 0.0, z_star, limit=400)
    DM_zstar = C_KMS / H0_local * DM_zstar_int

    ell_A = PI * DM_zstar / rs_zstar
    theta_star = rs_zstar / DM_zstar
    hundred_theta_star = 100.0 * theta_star

    return dict(
        z_eq=z_eq,
        z_star=z_star,
        z_drag=z_drag,
        rs_zstar=rs_zstar,
        rs_zd=rs_zd,
        DM_zstar=DM_zstar,
        ell_A=ell_A,
        hundred_theta_star=hundred_theta_star,
        Omega_m=Omega_m, Omega_b=Omega_b, H0=H0_local,
    )


def deviation(sam, ref):
    return (sam - ref) / ref


def main():
    out_dir = Path(__file__).parent

    # -------- canonical --------
    canon = compressed_geometry(OMEGA_M_SAM, OMEGA_B_SAM, H0)

    print("=" * 74)
    print("CR019 -- SAM-zero-parameter CMB compressed acoustic geometry")
    print("=" * 74)
    print(f"\nSubstrate inputs:")
    print(f"  Omega_m  = 1/pi             = {OMEGA_M_SAM:.6f}")
    print(f"  Omega_b  = 2*A_0*(1-chi)    = {OMEGA_B_SAM:.6f}")
    print(f"  H_0      = {H0}")
    print(f"  T_CMB    = {T_CMB}")
    print(f"  N_eff    = {N_EFF}")

    print("\n" + "=" * 74)
    print("Compressed CMB geometry: SAM vs Planck 2018 base-LCDM")
    print("=" * 74)
    rows = [
        ("z_eq",            canon["z_eq"],             PLANCK_Z_EQ),
        ("z_star",          canon["z_star"],           PLANCK_Z_STAR),
        ("z_drag",          canon["z_drag"],           PLANCK_Z_DRAG),
        ("r_s(z_star) Mpc", canon["rs_zstar"],         PLANCK_RS_ZSTAR),
        ("r_d Mpc",         canon["rs_zd"],            PLANCK_R_D),
        ("D_M(z_star) Mpc", canon["DM_zstar"],         PLANCK_DM_ZSTAR),
        ("ell_A",           canon["ell_A"],            PLANCK_ELL_A),
        ("100*theta_*",     canon["hundred_theta_star"], PLANCK_100THETA_STAR),
    ]
    print(f"{'observable':<18s} {'SAM':>14s}    {'Planck 2018':>14s}    {'dev':>10s}")
    print("-" * 74)
    for name, sam, planck in rows:
        dev = deviation(sam, planck) * 100.0
        print(f"{name:<18s} {sam:14.4f}    {planck:14.4f}    {dev:+9.3f}%")

    # -------- gates --------
    dev_100theta = deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR)
    dev_ellA     = deviation(canon["ell_A"],              PLANCK_ELL_A)
    dev_rd       = deviation(canon["rs_zd"],              PLANCK_R_D)

    p1_passed = abs(dev_100theta) <= P1_THRESH
    p2_passed = abs(dev_ellA)     <= P2_THRESH
    p3_passed = abs(dev_rd)       <= P3_THRESH

    print("\n" + "=" * 74)
    print("Load-bearing gates")
    print("=" * 74)
    print(f"  P1  |100*theta_* dev| = {abs(dev_100theta)*100:.3f}%   "
          f"thresh {P1_THRESH*100:.1f}%   {'PASS' if p1_passed else 'FAIL'}")
    print(f"  P2  |ell_A dev|       = {abs(dev_ellA)*100:.3f}%   "
          f"thresh {P2_THRESH*100:.1f}%   {'PASS' if p2_passed else 'FAIL'}")
    print(f"  P3  |r_d dev|         = {abs(dev_rd)*100:.3f}%   "
          f"thresh {P3_THRESH*100:.1f}%   {'PASS' if p3_passed else 'FAIL'}")

    # -------- WC1: random Omega_m --------
    print("\n" + "=" * 74)
    print("WC1 null (random Omega_m in [0.05, 0.95], 1000 seeded trials)")
    print("=" * 74)
    canonical_abs_dev = abs(deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR))
    wc1_nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed)
        Om_r = float(rng.uniform(0.05, 0.95))
        try:
            g = compressed_geometry(Om_r, OMEGA_B_SAM, H0)
            wc1_nulls.append(abs(deviation(g["hundred_theta_star"], PLANCK_100THETA_STAR)))
        except Exception:
            wc1_nulls.append(float("inf"))
    wc1_arr = np.array(wc1_nulls)
    n_ext_wc1 = int(np.sum(wc1_arr <= canonical_abs_dev))
    p_wc1 = (n_ext_wc1 + 1) / (N_TRIALS + 1)
    canonical_pct_wc1 = float(np.mean(wc1_arr <= canonical_abs_dev) * 100.0)
    finite_wc1 = wc1_arr[np.isfinite(wc1_arr)]
    print(f"  canonical |100*theta_* - 1.04110| / 1.04110 = {canonical_abs_dev:.5f}")
    print(f"  n_trials                          = {N_TRIALS}")
    print(f"  null median |dev|                 = {float(np.median(finite_wc1)):.5f}")
    print(f"  null 1st percentile |dev|         = {float(np.percentile(finite_wc1, 1)):.5f}")
    print(f"  null 5th percentile |dev|         = {float(np.percentile(finite_wc1, 5)):.5f}")
    print(f"  n_null_at_least_as_extreme        = {n_ext_wc1} of {N_TRIALS}")
    print(f"  canonical percentile in null      = {canonical_pct_wc1:.2f}%")
    print(f"  one-sided permutation p-value     = {p_wc1:.5f}")

    # -------- WC2: random (Omega_m, Omega_b) --------
    print("\n" + "=" * 74)
    print("WC2 null (random (Omega_m, Omega_b), 1000 seeded trials)")
    print("=" * 74)
    wc2_nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed + 10_000)
        Om_r = float(rng.uniform(0.05, 0.95))
        Ob_r = float(rng.uniform(0.005, 0.15))
        try:
            g = compressed_geometry(Om_r, Ob_r, H0)
            wc2_nulls.append(abs(deviation(g["hundred_theta_star"], PLANCK_100THETA_STAR)))
        except Exception:
            wc2_nulls.append(float("inf"))
    wc2_arr = np.array(wc2_nulls)
    n_ext_wc2 = int(np.sum(wc2_arr <= canonical_abs_dev))
    p_wc2 = (n_ext_wc2 + 1) / (N_TRIALS + 1)
    canonical_pct_wc2 = float(np.mean(wc2_arr <= canonical_abs_dev) * 100.0)
    finite_wc2 = wc2_arr[np.isfinite(wc2_arr)]
    print(f"  canonical |100*theta_* - 1.04110| / 1.04110 = {canonical_abs_dev:.5f}")
    print(f"  n_trials                          = {N_TRIALS}")
    print(f"  null median |dev|                 = {float(np.median(finite_wc2)):.5f}")
    print(f"  null 1st percentile |dev|         = {float(np.percentile(finite_wc2, 1)):.5f}")
    print(f"  null 5th percentile |dev|         = {float(np.percentile(finite_wc2, 5)):.5f}")
    print(f"  n_null_at_least_as_extreme        = {n_ext_wc2} of {N_TRIALS}")
    print(f"  canonical percentile in null      = {canonical_pct_wc2:.2f}%")
    print(f"  one-sided permutation p-value     = {p_wc2:.5f}")

    # -------- VERDICT --------
    print("\n" + "=" * 74)
    print("VERDICT")
    print("=" * 74)
    gates_pass = p1_passed and p2_passed and p3_passed
    if gates_pass:
        verdict = "PASS"
        verdict_reason = "P1, P2, P3 all hold under canonical substrate inputs"
    else:
        verdict = "FAIL"
        failed = [k for k, v in [("P1", p1_passed), ("P2", p2_passed), ("P3", p3_passed)] if not v]
        verdict_reason = f"failed gate(s): {failed}"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}")
    print(f"  P2: {'PASS' if p2_passed else 'FAIL'}")
    print(f"  P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR019 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # -------- write outputs --------
    summary = dict(
        precommit_sha256="ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da",
        substrate=dict(A_0=A_0, Omega_m_SAM=OMEGA_M_SAM, chi=CHI, Omega_b_SAM=OMEGA_B_SAM),
        measurement_inputs=dict(H0=H0, T_CMB=T_CMB, N_eff=N_EFF),
        planck_reference=dict(
            z_eq=PLANCK_Z_EQ, z_star=PLANCK_Z_STAR, z_drag=PLANCK_Z_DRAG,
            rs_zstar=PLANCK_RS_ZSTAR, r_d=PLANCK_R_D,
            DM_zstar=PLANCK_DM_ZSTAR, ell_A=PLANCK_ELL_A,
            hundred_theta_star=PLANCK_100THETA_STAR,
        ),
        canonical=canon,
        deviations=dict(
            z_eq_pct          = deviation(canon["z_eq"],             PLANCK_Z_EQ) * 100,
            z_star_pct        = deviation(canon["z_star"],           PLANCK_Z_STAR) * 100,
            z_drag_pct        = deviation(canon["z_drag"],           PLANCK_Z_DRAG) * 100,
            rs_zstar_pct      = deviation(canon["rs_zstar"],         PLANCK_RS_ZSTAR) * 100,
            r_d_pct           = deviation(canon["rs_zd"],            PLANCK_R_D) * 100,
            DM_zstar_pct      = deviation(canon["DM_zstar"],         PLANCK_DM_ZSTAR) * 100,
            ell_A_pct         = deviation(canon["ell_A"],            PLANCK_ELL_A) * 100,
            hundred_theta_pct = deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR) * 100,
        ),
        P1=dict(name="100*theta_* vs Planck", deviation=dev_100theta,
                threshold=P1_THRESH, passed=p1_passed),
        P2=dict(name="ell_A vs Planck", deviation=dev_ellA,
                threshold=P2_THRESH, passed=p2_passed),
        P3=dict(name="r_d vs Planck", deviation=dev_rd,
                threshold=P3_THRESH, passed=p3_passed),
        WC1=dict(n_trials=N_TRIALS,
                 canonical_abs_dev=canonical_abs_dev,
                 null_median=float(np.median(finite_wc1)),
                 null_p1=float(np.percentile(finite_wc1, 1)),
                 null_p5=float(np.percentile(finite_wc1, 5)),
                 n_extreme=n_ext_wc1,
                 canonical_percentile=canonical_pct_wc1,
                 p_value=p_wc1),
        WC2=dict(n_trials=N_TRIALS,
                 canonical_abs_dev=canonical_abs_dev,
                 null_median=float(np.median(finite_wc2)),
                 null_p1=float(np.percentile(finite_wc2, 1)),
                 null_p5=float(np.percentile(finite_wc2, 5)),
                 n_extreme=n_ext_wc2,
                 canonical_percentile=canonical_pct_wc2,
                 p_value=p_wc2),
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR019_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = []
    for name, sam, planck in rows:
        evidence.append(dict(
            item=f"{name}_SAM", value=sam, passes=True,
        ))
        evidence.append(dict(
            item=f"{name}_Planck", value=planck, passes=True,
        ))
        evidence.append(dict(
            item=f"{name}_dev_pct", value=deviation(sam, planck) * 100, passes=True,
        ))
    evidence.append(dict(item="P1_100theta_passed", value=p1_passed, passes=p1_passed))
    evidence.append(dict(item="P2_ellA_passed",     value=p2_passed, passes=p2_passed))
    evidence.append(dict(item="P3_rd_passed",       value=p3_passed, passes=p3_passed))
    evidence.append(dict(item="WC1_canonical_percentile", value=canonical_pct_wc1, passes=True))
    evidence.append(dict(item="WC1_p_value",        value=p_wc1, passes=True))
    evidence.append(dict(item="WC2_canonical_percentile", value=canonical_pct_wc2, passes=True))
    evidence.append(dict(item="WC2_p_value",        value=p_wc2, passes=True))
    evidence.append(dict(item="verdict",            value=verdict, passes=(verdict == "PASS")))

    with (out_dir / "CR019_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
