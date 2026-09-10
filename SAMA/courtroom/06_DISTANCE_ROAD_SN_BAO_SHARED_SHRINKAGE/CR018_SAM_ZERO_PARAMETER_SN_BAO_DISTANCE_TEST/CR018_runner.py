"""
CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST runner.

Implements the test specified in CR018_PRECOMMIT.md (SHA-256
04f562aa61417995b46091d74b516acf20a425d72dcff672895875a6be6c7e85).

Substrate inputs (zero-parameter):
  Omega_m = 1/pi
  Omega_b = 2 * A_0 * (1 - 2/(9 pi))    where A_0 = 1/(12 pi)
  flat geometry, w = -1

Measurement inputs (external, not catalog fit):
  H_0 = 73.04 km/s/Mpc (SH0ES; SN test)
  H_0 = 68.76 km/s/Mpc (Planck-style; BAO test)
  r_d from Eisenstein-Hu fitting formula

External data:
  Pantheon+SH0ES.dat (Brout et al. 2022)
  DESI DR1 BAO 2024 release (12 distance ratios, hardcoded)

Outputs:
  CR018_summary.json
  CR018_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import quad

# -- Frozen sources -----------------------------------------------------------

PANTHEON = Path(
    r"C:\VS\quantum_phase\data\external\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat"
)

# -- Frozen test parameters per precommit -------------------------------------

C_KMS = 299792.458
PI = math.pi
OMEGA_GAMMA_H2 = 2.4728e-5
REL_FACTOR = 1.0 + 0.2271 * 3.046

H0_SN_SH0ES   = 73.04
H0_BAO_PLANCK = 68.76

R_D_PLANCK_2018 = 147.09  # Mpc, base-LambdaCDM drag sound horizon

# Substrate identities (Section 7)
A0 = 1.0 / (12.0 * PI)
R_SUBSTRATE = 12.0
A_INF = R_SUBSTRATE * A0           # = 1/pi
MU_H = 8.0 / 3.0                   # 2^D / D with D=3
CHI = MU_H * A0                    # = 2/(9 pi)
OMEGA_M_SAM = A_INF                # = 1/pi
OMEGA_B_SAM = 2.0 * A0 * (1.0 - CHI)  # full Section 7 form

# Falsifier thresholds
P1_RESID_THRESHOLD_MAG = 0.025
P2_CHI2_PER_N = 2.5
P3_REL_DEV_R_D = 0.01
P5_P_THRESHOLD = 0.01
P6_P_THRESHOLD = 0.01

N_TRIALS = 1000

# DESI DR1 (2024) BAO measurements -- HARDCODED per precommit
DESI = [
    ("BGS",       0.295, "DV",  7.93, 0.15),
    ("LRG1",      0.510, "DM", 13.62, 0.25),
    ("LRG1",      0.510, "DH", 20.98, 0.61),
    ("LRG2",      0.706, "DM", 16.85, 0.32),
    ("LRG2",      0.706, "DH", 20.08, 0.60),
    ("LRG3+ELG",  0.930, "DM", 21.71, 0.28),
    ("LRG3+ELG",  0.930, "DH", 17.88, 0.35),
    ("ELG",       1.317, "DM", 27.79, 0.69),
    ("ELG",       1.317, "DH", 13.82, 0.42),
    ("QSO",       1.491, "DV", 26.07, 0.67),
    ("Lya",       2.330, "DM", 39.71, 0.94),
    ("Lya",       2.330, "DH",  8.52, 0.17),
]


# -- Cosmology ----------------------------------------------------------------


def make_E(Om: float, Or: float, Ode: float):
    def E(z: float) -> float:
        return math.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + Ode)
    return E


def cosmology(Om: float, Ob: float, H0: float) -> dict:
    h = H0 / 100.0
    wm = Om * h * h
    wb = Ob * h * h
    Og = OMEGA_GAMMA_H2 / (h * h)
    Or = Og * REL_FACTOR
    Ode = 1.0 - Om - Or
    E = make_E(Om, Or, Ode)

    # Eisenstein-Hu z_drag
    b1 = 0.313 * wm ** -0.419 * (1.0 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    zdrag = 1291.0 * wm ** 0.251 / (1.0 + 0.659 * wm ** 0.828) * (1.0 + b1 * wb ** b2)

    def cs_over_H(z):
        Rb = 0.75 * Ob / Og / (1.0 + z)
        return C_KMS / math.sqrt(3.0 * (1.0 + Rb)) / (H0 * E(z))

    r_d, _ = quad(cs_over_H, zdrag, np.inf, limit=400)

    def DM(z):
        val, _ = quad(lambda x: 1.0 / E(x), 0.0, z, limit=200)
        return C_KMS / H0 * val

    def DH(z):
        return C_KMS / (H0 * E(z))

    def DV(z):
        return (z * DM(z) ** 2 * DH(z)) ** (1.0 / 3.0)

    return dict(E=E, DM=DM, DH=DH, DV=DV, r_d=r_d,
                Om=Om, Ob=Ob, H0=H0, wm=wm, wb=wb, zdrag=zdrag, Ode=Ode)


def mu_theory(z: float, cos: dict) -> float:
    DL = (1.0 + z) * cos["DM"](z)
    return 25.0 + 5.0 * math.log10(DL)


# -- Data loaders -------------------------------------------------------------


def load_pantheon(path: Path):
    with path.open("r") as f:
        header = f.readline().strip().split()
    idx_z   = header.index("zHD")
    idx_mu  = header.index("MU_SH0ES")
    idx_err = header.index("MU_SH0ES_ERR_DIAG")
    idx_cal = header.index("IS_CALIBRATOR")
    rows = np.genfromtxt(path, skip_header=1, dtype=float,
                         usecols=(idx_z, idx_mu, idx_err, idx_cal))
    z = rows[:, 0]; mu = rows[:, 1]; err = rows[:, 2]
    cal = rows[:, 3].astype(int)
    mask = (z > 0.01) & (cal == 0) & np.isfinite(mu) & np.isfinite(err) & (err > 0)
    return z[mask], mu[mask], err[mask]


# -- Predictions --------------------------------------------------------------


def sn_weighted_mean_residual(z, mu_obs, err, cos) -> float:
    mu_th = np.array([mu_theory(zi, cos) for zi in z])
    resid = mu_obs - mu_th
    w = 1.0 / (err ** 2)
    return float(np.sum(w * resid) / np.sum(w))


def bao_chi2(cos) -> float:
    chi2 = 0.0
    for tr, z, obs, val, sig in DESI:
        f = {"DM": cos["DM"], "DH": cos["DH"], "DV": cos["DV"]}[obs]
        m = f(z) / cos["r_d"]
        chi2 += ((val - m) / sig) ** 2
    return chi2


def evaluate_p1(z, mu_obs, err, cos) -> dict:
    wmr = sn_weighted_mean_residual(z, mu_obs, err, cos)
    out = dict(name="P1", weighted_mean_residual=wmr,
               threshold=P1_RESID_THRESHOLD_MAG,
               passed=abs(wmr) <= P1_RESID_THRESHOLD_MAG)
    out["reason"] = (f"|wmr| = {abs(wmr):.5f} <= {P1_RESID_THRESHOLD_MAG}"
                     if out["passed"]
                     else f"|wmr| = {abs(wmr):.5f} > {P1_RESID_THRESHOLD_MAG}")
    return out


def evaluate_p2(cos) -> dict:
    chi2 = bao_chi2(cos)
    chi2_per_n = chi2 / len(DESI)
    out = dict(name="P2", chi2=chi2, n_points=len(DESI),
               chi2_per_n=chi2_per_n, threshold=P2_CHI2_PER_N,
               passed=chi2_per_n <= P2_CHI2_PER_N)
    out["reason"] = (f"chi^2/n = {chi2_per_n:.4f} <= {P2_CHI2_PER_N}"
                     if out["passed"]
                     else f"chi^2/n = {chi2_per_n:.4f} > {P2_CHI2_PER_N}")
    return out


def evaluate_p3(cos) -> dict:
    rd = cos["r_d"]
    rel_dev = (rd - R_D_PLANCK_2018) / R_D_PLANCK_2018
    abs_rel = abs(rel_dev)
    out = dict(name="P3", r_d_SAM=rd, r_d_Planck2018=R_D_PLANCK_2018,
               rel_dev=rel_dev, abs_rel_dev=abs_rel,
               threshold=P3_REL_DEV_R_D,
               passed=abs_rel <= P3_REL_DEV_R_D)
    out["reason"] = (f"|rel_dev| = {abs_rel:.5f} ({rel_dev*100:+.3f}%) "
                     f"<= {P3_REL_DEV_R_D}"
                     if out["passed"]
                     else f"|rel_dev| = {abs_rel:.5f} > {P3_REL_DEV_R_D}")
    return out


def evaluate_p4(z, mu_obs, err) -> dict:
    """Sweep H_0 in [60, 80] at 21 grid points, both probes."""
    H0_grid = np.arange(60.0, 81.0, 1.0)
    wmr_per_h0 = []
    chi2_per_h0 = []
    for H0 in H0_grid:
        cos = cosmology(OMEGA_M_SAM, OMEGA_B_SAM, float(H0))
        wmr_per_h0.append(sn_weighted_mean_residual(z, mu_obs, err, cos))
        chi2_per_h0.append(bao_chi2(cos))
    wmr_arr = np.array(wmr_per_h0)
    chi2_arr = np.array(chi2_per_h0)

    # P4a: SN wmr zero crossing in [70, 75]
    sn_best_h0 = None
    for i in range(len(H0_grid) - 1):
        if wmr_arr[i] * wmr_arr[i + 1] < 0:
            # Linear interpolation for crossing
            frac = abs(wmr_arr[i]) / (abs(wmr_arr[i]) + abs(wmr_arr[i + 1]))
            sn_best_h0 = float(H0_grid[i] + frac * (H0_grid[i + 1] - H0_grid[i]))
            if 70.0 <= sn_best_h0 <= 75.0:
                break

    # P4b: BAO chi^2 minimum in [66, 71]
    min_idx = int(np.argmin(chi2_arr))
    bao_best_h0 = float(H0_grid[min_idx])

    p4a = sn_best_h0 is not None and 70.0 <= sn_best_h0 <= 75.0
    p4b = 66.0 <= bao_best_h0 <= 71.0
    p4c = (sn_best_h0 is not None) and bao_best_h0 is not None and sn_best_h0 > bao_best_h0

    return dict(
        name="P4",
        sn_best_H0=sn_best_h0,
        bao_best_H0=bao_best_h0,
        P4a_sn_zero_crossing_in_70_75=p4a,
        P4b_bao_min_in_66_71=p4b,
        P4c_sn_best_gt_bao_best=p4c,
        H0_grid=H0_grid.tolist(),
        sn_wmr_per_h0=wmr_arr.tolist(),
        bao_chi2_per_h0=chi2_arr.tolist(),
        passed=p4a and p4b and p4c,
        reason=(
            f"sn_best={sn_best_h0:.3f}, bao_best={bao_best_h0:.3f}, "
            f"P4a={p4a}, P4b={p4b}, P4c={p4c}"
        ),
    )


def evaluate_p5_sn_null(z, mu_obs, err, canonical_wmr_abs) -> dict:
    """1000 random Omega_m draws -> null distribution of |weighted_mean_residual|."""
    nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed)
        Om_random = float(rng.uniform(0.05, 0.95))
        try:
            cos_r = cosmology(Om_random, OMEGA_B_SAM, H0_SN_SH0ES)
            wmr_r = sn_weighted_mean_residual(z, mu_obs, err, cos_r)
            nulls.append(abs(wmr_r))
        except Exception:
            nulls.append(float("inf"))
    nulls_arr = np.array(nulls)
    n_extreme = int(np.sum(nulls_arr <= canonical_wmr_abs))
    p_val = (n_extreme + 1) / (N_TRIALS + 1)
    return dict(
        name="P5",
        canonical_abs_wmr=canonical_wmr_abs,
        n_trials=N_TRIALS,
        null_mean=float(np.mean(nulls_arr[np.isfinite(nulls_arr)])),
        null_min=float(np.min(nulls_arr)),
        null_max=float(np.max(nulls_arr[np.isfinite(nulls_arr)])),
        null_median=float(np.median(nulls_arr)),
        null_p1=float(np.percentile(nulls_arr[np.isfinite(nulls_arr)], 1)),
        null_p5=float(np.percentile(nulls_arr[np.isfinite(nulls_arr)], 5)),
        null_p10=float(np.percentile(nulls_arr[np.isfinite(nulls_arr)], 10)),
        n_extreme=n_extreme,
        p_value=p_val,
        threshold=P5_P_THRESHOLD,
        passed=p_val < P5_P_THRESHOLD,
    )


def evaluate_p6_bao_null(canonical_chi2) -> dict:
    """1000 random (Omega_m, Omega_b) draws -> null distribution of chi^2."""
    nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed + 10_000)  # different seed family from P5
        Om_random = float(rng.uniform(0.05, 0.95))
        Ob_random = float(rng.uniform(0.005, 0.15))
        try:
            cos_r = cosmology(Om_random, Ob_random, H0_BAO_PLANCK)
            chi2_r = bao_chi2(cos_r)
            nulls.append(chi2_r if math.isfinite(chi2_r) else float("inf"))
        except Exception:
            nulls.append(float("inf"))
    nulls_arr = np.array(nulls)
    n_extreme = int(np.sum(nulls_arr <= canonical_chi2))
    p_val = (n_extreme + 1) / (N_TRIALS + 1)
    finite = nulls_arr[np.isfinite(nulls_arr)]
    return dict(
        name="P6",
        canonical_chi2=canonical_chi2,
        n_trials=N_TRIALS,
        null_mean=float(np.mean(finite)),
        null_min=float(np.min(finite)),
        null_max=float(np.max(finite)),
        null_median=float(np.median(finite)),
        null_p1=float(np.percentile(finite, 1)),
        null_p5=float(np.percentile(finite, 5)),
        null_p10=float(np.percentile(finite, 10)),
        n_extreme=n_extreme,
        p_value=p_val,
        threshold=P6_P_THRESHOLD,
        passed=p_val < P6_P_THRESHOLD,
    )


# -- Main ---------------------------------------------------------------------


def main():
    out_dir = Path(__file__).parent

    print("Substrate values:")
    print(f"  A_0       = 1/(12 pi)        = {A0:.6f}")
    print(f"  Omega_m   = 1/pi             = {OMEGA_M_SAM:.6f}")
    print(f"  chi       = 2/(9 pi)         = {CHI:.6f}")
    print(f"  Omega_b   = 2*A_0*(1-chi)    = {OMEGA_B_SAM:.6f}")

    # SN cosmology
    cos_sn = cosmology(OMEGA_M_SAM, OMEGA_B_SAM, H0_SN_SH0ES)
    # BAO cosmology
    cos_bao = cosmology(OMEGA_M_SAM, OMEGA_B_SAM, H0_BAO_PLANCK)

    print(f"\nSN cosmology (H_0 = {H0_SN_SH0ES}):")
    print(f"  r_d = {cos_sn['r_d']:.3f} Mpc (not used for SN test)")
    print(f"\nBAO cosmology (H_0 = {H0_BAO_PLANCK}):")
    print(f"  r_d = {cos_bao['r_d']:.3f} Mpc")
    print(f"  Planck 2018 r_d = {R_D_PLANCK_2018} Mpc")
    rel_dev = (cos_bao['r_d'] - R_D_PLANCK_2018) / R_D_PLANCK_2018
    print(f"  Relative deviation: {rel_dev*100:+.3f}%")

    # Load SN data
    z, mu, err = load_pantheon(PANTHEON)
    print(f"\nLoaded {len(z)} Pantheon+ SNe after z>0.01 + non-calibrator cuts")

    # --- P1 ---
    print("\n--- P1: SN weighted mean residual (no offset, no host correction) ---")
    p1 = evaluate_p1(z, mu, err, cos_sn)
    print(f"  weighted_mean_residual = {p1['weighted_mean_residual']:+.5f} mag")
    print(f"  |wmr| threshold: {p1['threshold']}")
    print(f"  P1: {'PASS' if p1['passed'] else 'FAIL'} -- {p1['reason']}")

    # --- P2 ---
    print("\n--- P2: BAO chi^2 ---")
    p2 = evaluate_p2(cos_bao)
    print(f"  chi^2 = {p2['chi2']:.3f}  over {p2['n_points']} points")
    print(f"  chi^2 / n = {p2['chi2_per_n']:.4f}")
    print(f"  P2: {'PASS' if p2['passed'] else 'FAIL'} -- {p2['reason']}")

    # --- P3 ---
    print("\n--- P3: r_d vs Planck 2018 ---")
    p3 = evaluate_p3(cos_bao)
    print(f"  r_d_SAM = {p3['r_d_SAM']:.3f} Mpc")
    print(f"  r_d_Planck2018 = {p3['r_d_Planck2018']} Mpc")
    print(f"  P3: {'PASS' if p3['passed'] else 'FAIL'} -- {p3['reason']}")

    # --- P4 ---
    print("\n--- P4: probe-split H_0 sweep ---")
    p4 = evaluate_p4(z, mu, err)
    print(f"  SN-best H_0  = {p4['sn_best_H0']}  (P4a {p4['P4a_sn_zero_crossing_in_70_75']})")
    print(f"  BAO-best H_0 = {p4['bao_best_H0']}  (P4b {p4['P4b_bao_min_in_66_71']})")
    print(f"  P4c (SN best > BAO best)? {p4['P4c_sn_best_gt_bao_best']}")
    print(f"  P4: {'PASS' if p4['passed'] else 'FAIL'}")

    # --- P5 ---
    print("\n--- P5: SN null distribution (1000 random Omega_m) ---")
    p5 = evaluate_p5_sn_null(z, mu, err, abs(p1['weighted_mean_residual']))
    print(f"  canonical |wmr|       = {p5['canonical_abs_wmr']:.5f}")
    print(f"  null median |wmr|     = {p5['null_median']:.5f}")
    print(f"  null 1st percentile   = {p5['null_p1']:.5f}")
    print(f"  null 5th percentile   = {p5['null_p5']:.5f}")
    print(f"  n_null_at_least_as_extreme = {p5['n_extreme']}")
    print(f"  p_value = {p5['p_value']:.6f}")
    print(f"  P5: {'PASS' if p5['passed'] else 'FAIL'} (threshold p < {p5['threshold']})")

    # --- P6 ---
    print("\n--- P6: BAO null distribution (1000 random (Omega_m, Omega_b)) ---")
    p6 = evaluate_p6_bao_null(p2['chi2'])
    print(f"  canonical chi^2       = {p6['canonical_chi2']:.3f}")
    print(f"  null median chi^2     = {p6['null_median']:.1f}")
    print(f"  null 1st percentile   = {p6['null_p1']:.3f}")
    print(f"  null 5th percentile   = {p6['null_p5']:.3f}")
    print(f"  n_null_at_least_as_extreme = {p6['n_extreme']}")
    print(f"  p_value = {p6['p_value']:.6f}")
    print(f"  P6: {'PASS' if p6['passed'] else 'FAIL'} (threshold p < {p6['threshold']})")

    # --- Verdict ---
    print("\n=== VERDICT ===")
    pass_conditions = {
        "P1_SN_weighted_residual": p1["passed"],
        "P2_BAO_chi2": p2["passed"],
        "P3_r_d_vs_Planck": p3["passed"],
        "P4_probe_split": p4["passed"],
        "P5_SN_null_percentile": p5["passed"],
        "P6_BAO_null_percentile": p6["passed"],
    }
    for k, v in pass_conditions.items():
        print(f"  {k:30s}  {'PASS' if v else 'FAIL'}")

    fails_p1_p3 = not (p1["passed"] and p2["passed"] and p3["passed"])
    if fails_p1_p3:
        verdict = "FAIL"
        verdict_reason = "one of P1, P2, P3 failed (direct prediction-vs-data)"
    elif all(pass_conditions.values()):
        verdict = "PASS"
        verdict_reason = "all P1-P6 hold under canonical substrate values"
    else:
        failed = [k for k, v in pass_conditions.items() if not v]
        verdict = "BOUNDARY"
        verdict_reason = f"P1-P3 hold but failed: {failed}"
    print(f"\n  CR018 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # --- Write outputs ---
    summary = dict(
        precommit_sha256="04f562aa61417995b46091d74b516acf20a425d72dcff672895875a6be6c7e85",
        substrate=dict(
            A_0=A0, Omega_m_SAM=OMEGA_M_SAM, chi=CHI, Omega_b_SAM=OMEGA_B_SAM,
            R_substrate=R_SUBSTRATE,
        ),
        measurement_inputs=dict(
            H0_SN_SH0ES=H0_SN_SH0ES, H0_BAO_PLANCK=H0_BAO_PLANCK,
            r_d_Planck2018=R_D_PLANCK_2018,
        ),
        sn_cosmology=dict(
            H0=H0_SN_SH0ES, r_d_Mpc=cos_sn["r_d"],
            zdrag=cos_sn["zdrag"], wm=cos_sn["wm"], wb=cos_sn["wb"],
        ),
        bao_cosmology=dict(
            H0=H0_BAO_PLANCK, r_d_Mpc=cos_bao["r_d"],
            zdrag=cos_bao["zdrag"], wm=cos_bao["wm"], wb=cos_bao["wb"],
        ),
        n_sn_after_cuts=int(len(z)),
        n_bao_points=len(DESI),
        P1=p1, P2=p2, P3=p3, P4=p4, P5=p5, P6=p6,
        pass_conditions=pass_conditions,
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR018_summary.json").write_text(
        json.dumps(summary, indent=2, default=str)
    )

    evidence = [
        dict(item="n_sn_after_cuts", value=int(len(z)), passes=True),
        dict(item="n_bao_points", value=len(DESI), passes=True),
        dict(item="Omega_m_SAM", value=OMEGA_M_SAM, passes=True),
        dict(item="Omega_b_SAM", value=OMEGA_B_SAM, passes=True),
        dict(item="r_d_SAM_at_H0_68_76", value=cos_bao["r_d"], passes=True),
        dict(item="r_d_Planck2018", value=R_D_PLANCK_2018, passes=True),
        dict(item="P1_SN_weighted_mean_residual", value=p1["weighted_mean_residual"], passes=p1["passed"]),
        dict(item="P2_BAO_chi2", value=p2["chi2"], passes=p2["passed"]),
        dict(item="P2_BAO_chi2_per_n", value=p2["chi2_per_n"], passes=p2["passed"]),
        dict(item="P3_r_d_rel_dev_pct", value=p3["rel_dev"]*100, passes=p3["passed"]),
        dict(item="P4_sn_best_H0", value=p4["sn_best_H0"], passes=p4["P4a_sn_zero_crossing_in_70_75"]),
        dict(item="P4_bao_best_H0", value=p4["bao_best_H0"], passes=p4["P4b_bao_min_in_66_71"]),
        dict(item="P5_SN_null_p_value", value=p5["p_value"], passes=p5["passed"]),
        dict(item="P5_SN_null_n_extreme", value=p5["n_extreme"], passes=p5["passed"]),
        dict(item="P6_BAO_null_p_value", value=p6["p_value"], passes=p6["passed"]),
        dict(item="P6_BAO_null_n_extreme", value=p6["n_extreme"], passes=p6["passed"]),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    with (out_dir / "CR018_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
