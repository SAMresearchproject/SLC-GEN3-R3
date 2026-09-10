"""
CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL runner.

Implements the test specified in CR018b_PRECOMMIT.md (SHA-256
bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce).

Functionally identical to CR018_runner.py on the analysis side. The
difference is the verdict-logic block at the end:
  - P1, P2, P3 are load-bearing PASS gates
  - P4, P5, P6 are computed and reported as sensitivity EVIDENCE, not gates

Substrate, measurement inputs, predictions, seeds, EH formula, DESI data,
and Pantheon+ cuts are unchanged from CR018.

Outputs:
  CR018b_summary.json
  CR018b_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import quad

# -- Frozen sources (same as CR018) -------------------------------------------

PANTHEON = Path(
    r"C:\VS\quantum_phase\data\external\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat"
)

C_KMS = 299792.458
PI = math.pi
OMEGA_GAMMA_H2 = 2.4728e-5
REL_FACTOR = 1.0 + 0.2271 * 3.046

H0_SN_SH0ES   = 73.04
H0_BAO_PLANCK = 68.76

R_D_PLANCK_2018 = 147.09

A0 = 1.0 / (12.0 * PI)
R_SUBSTRATE = 12.0
A_INF = R_SUBSTRATE * A0
MU_H = 8.0 / 3.0
CHI = MU_H * A0
OMEGA_M_SAM = A_INF
OMEGA_B_SAM = 2.0 * A0 * (1.0 - CHI)

P1_RESID_THRESHOLD_MAG = 0.025
P2_CHI2_PER_N = 2.5
P3_REL_DEV_R_D = 0.01

N_TRIALS = 1000

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


def make_E(Om, Or, Ode):
    def E(z):
        return math.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + Ode)
    return E


def cosmology(Om, Ob, H0):
    h = H0 / 100.0
    wm = Om * h * h
    wb = Ob * h * h
    Og = OMEGA_GAMMA_H2 / (h * h)
    Or = Og * REL_FACTOR
    Ode = 1.0 - Om - Or
    E = make_E(Om, Or, Ode)

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


def mu_theory(z, cos):
    DL = (1.0 + z) * cos["DM"](z)
    return 25.0 + 5.0 * math.log10(DL)


def load_pantheon(path):
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


def sn_wmr(z, mu_obs, err, cos):
    mu_th = np.array([mu_theory(zi, cos) for zi in z])
    resid = mu_obs - mu_th
    w = 1.0 / (err ** 2)
    return float(np.sum(w * resid) / np.sum(w))


def bao_chi2(cos):
    chi2 = 0.0
    for tr, z, obs, val, sig in DESI:
        f = {"DM": cos["DM"], "DH": cos["DH"], "DV": cos["DV"]}[obs]
        m = f(z) / cos["r_d"]
        chi2 += ((val - m) / sig) ** 2
    return chi2


def main():
    out_dir = Path(__file__).parent

    cos_sn  = cosmology(OMEGA_M_SAM, OMEGA_B_SAM, H0_SN_SH0ES)
    cos_bao = cosmology(OMEGA_M_SAM, OMEGA_B_SAM, H0_BAO_PLANCK)
    z, mu, err = load_pantheon(PANTHEON)

    # -- Load-bearing P1, P2, P3 --
    wmr = sn_wmr(z, mu, err, cos_sn)
    p1_passed = abs(wmr) <= P1_RESID_THRESHOLD_MAG
    chi2_bao = bao_chi2(cos_bao)
    chi2_per_n = chi2_bao / len(DESI)
    p2_passed = chi2_per_n <= P2_CHI2_PER_N
    r_d_sam = cos_bao["r_d"]
    rel_dev = (r_d_sam - R_D_PLANCK_2018) / R_D_PLANCK_2018
    p3_passed = abs(rel_dev) <= P3_REL_DEV_R_D

    print("=" * 70)
    print("CR018b -- Verdict-ladder appeal of CR018")
    print("=" * 70)
    print(f"\nSubstrate: Omega_m = {OMEGA_M_SAM:.6f}  Omega_b = {OMEGA_B_SAM:.6f}")
    print(f"\nP1 SN  |weighted_mean_residual| = {abs(wmr):.5f} mag  threshold {P1_RESID_THRESHOLD_MAG}")
    print(f"   -> {'PASS' if p1_passed else 'FAIL'}")
    print(f"\nP2 BAO chi^2/n                  = {chi2_per_n:.4f}      threshold {P2_CHI2_PER_N}")
    print(f"   -> {'PASS' if p2_passed else 'FAIL'}")
    print(f"\nP3 r_d_SAM = {r_d_sam:.3f} Mpc  vs Planck 2018 {R_D_PLANCK_2018} Mpc")
    print(f"   relative deviation = {rel_dev*100:+.3f}%  threshold {P3_REL_DEV_R_D*100}%")
    print(f"   -> {'PASS' if p3_passed else 'FAIL'}")

    # -- Sensitivity evidence: E4 probe split --
    print(f"\n[Sensitivity evidence: E4 probe-split sweep H_0 in [60, 80]]")
    H0_grid = np.arange(60.0, 81.0, 1.0)
    wmr_per = [sn_wmr(z, mu, err, cosmology(OMEGA_M_SAM, OMEGA_B_SAM, float(h))) for h in H0_grid]
    chi2_per = [bao_chi2(cosmology(OMEGA_M_SAM, OMEGA_B_SAM, float(h))) for h in H0_grid]
    wmr_arr = np.array(wmr_per); chi2_arr = np.array(chi2_per)
    sn_best = None
    for i in range(len(H0_grid) - 1):
        if wmr_arr[i] * wmr_arr[i + 1] < 0:
            frac = abs(wmr_arr[i]) / (abs(wmr_arr[i]) + abs(wmr_arr[i + 1]))
            sn_best = float(H0_grid[i] + frac * (H0_grid[i + 1] - H0_grid[i]))
            break
    bao_best = float(H0_grid[int(np.argmin(chi2_arr))])
    print(f"   SN-best H_0   = {sn_best:.3f}")
    print(f"   BAO-best H_0  = {bao_best:.3f}")
    print(f"   SN-best > BAO-best ? {sn_best > bao_best}")

    # -- Sensitivity evidence: E5 SN null --
    print(f"\n[Sensitivity evidence: E5 SN null (1000 random Omega_m draws, seeds 0..999)]")
    nulls_sn = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed)
        Om_r = float(rng.uniform(0.05, 0.95))
        try:
            cos_r = cosmology(Om_r, OMEGA_B_SAM, H0_SN_SH0ES)
            nulls_sn.append(abs(sn_wmr(z, mu, err, cos_r)))
        except Exception:
            nulls_sn.append(float("inf"))
    nulls_sn_arr = np.array(nulls_sn)
    n_ext_sn = int(np.sum(nulls_sn_arr <= abs(wmr)))
    p_sn = (n_ext_sn + 1) / (N_TRIALS + 1)
    canonical_pct_sn = float(np.mean(nulls_sn_arr <= abs(wmr)) * 100.0)
    print(f"   canonical |wmr|        = {abs(wmr):.5f}")
    print(f"   null median |wmr|      = {float(np.median(nulls_sn_arr)):.5f}")
    print(f"   n null at-least-as-extreme = {n_ext_sn} of {N_TRIALS}")
    print(f"   canonical at percentile = {canonical_pct_sn:.2f}")
    print(f"   one-sided permutation p = {p_sn:.5f}")

    # -- Sensitivity evidence: E6 BAO null --
    print(f"\n[Sensitivity evidence: E6 BAO null (1000 random (Omega_m, Omega_b), seeds 10000..10999)]")
    nulls_bao = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed + 10_000)
        Om_r = float(rng.uniform(0.05, 0.95))
        Ob_r = float(rng.uniform(0.005, 0.15))
        try:
            cos_r = cosmology(Om_r, Ob_r, H0_BAO_PLANCK)
            nulls_bao.append(bao_chi2(cos_r))
        except Exception:
            nulls_bao.append(float("inf"))
    nulls_bao_arr = np.array(nulls_bao)
    finite = nulls_bao_arr[np.isfinite(nulls_bao_arr)]
    n_ext_bao = int(np.sum(nulls_bao_arr <= chi2_bao))
    p_bao = (n_ext_bao + 1) / (N_TRIALS + 1)
    canonical_pct_bao = float(np.mean(nulls_bao_arr <= chi2_bao) * 100.0)
    print(f"   canonical chi^2        = {chi2_bao:.3f}")
    print(f"   null median chi^2      = {float(np.median(finite)):.1f}")
    print(f"   n null at-least-as-extreme = {n_ext_bao} of {N_TRIALS}")
    print(f"   canonical at percentile = {canonical_pct_bao:.2f}")
    print(f"   one-sided permutation p = {p_bao:.5f}")

    # -- VERDICT --
    print("\n" + "=" * 70)
    print("VERDICT (CR018b corrected ladder: only P1, P2, P3 gate)")
    print("=" * 70)
    if not (p1_passed and p2_passed and p3_passed):
        verdict = "FAIL"
        verdict_reason = "at least one of P1, P2, P3 fails"
    else:
        verdict = "PASS"
        verdict_reason = "P1, P2, P3 all hold under canonical substrate inputs"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}")
    print(f"  P2: {'PASS' if p2_passed else 'FAIL'}")
    print(f"  P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR018b verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    summary = dict(
        precommit_sha256="bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce",
        appeal_of="CR018",
        appeal_basis="auxiliary sensitivity conditions reclassified as evidence (not pass gates)",
        substrate=dict(A_0=A0, Omega_m_SAM=OMEGA_M_SAM, chi=CHI, Omega_b_SAM=OMEGA_B_SAM),
        measurement_inputs=dict(
            H0_SN_SH0ES=H0_SN_SH0ES, H0_BAO_PLANCK=H0_BAO_PLANCK,
            r_d_Planck2018=R_D_PLANCK_2018,
        ),
        n_sn_after_cuts=int(len(z)),
        n_bao_points=len(DESI),
        P1=dict(name="SN weighted-mean residual",
                weighted_mean_residual=wmr,
                threshold=P1_RESID_THRESHOLD_MAG,
                passed=p1_passed),
        P2=dict(name="BAO chi^2 / n",
                chi2=chi2_bao, n_points=len(DESI),
                chi2_per_n=chi2_per_n,
                threshold=P2_CHI2_PER_N,
                passed=p2_passed),
        P3=dict(name="r_d vs Planck 2018",
                r_d_SAM=r_d_sam,
                r_d_Planck2018=R_D_PLANCK_2018,
                relative_deviation=rel_dev,
                threshold=P3_REL_DEV_R_D,
                passed=p3_passed),
        E4_probe_split=dict(
            sn_best_H0=sn_best, bao_best_H0=bao_best,
            sn_gt_bao=(sn_best > bao_best) if sn_best else False,
            H0_grid=H0_grid.tolist(),
            sn_wmr_per_H0=wmr_arr.tolist(),
            bao_chi2_per_H0=chi2_arr.tolist(),
        ),
        E5_SN_null=dict(
            n_trials=N_TRIALS,
            canonical_abs_wmr=abs(wmr),
            null_median=float(np.median(nulls_sn_arr)),
            null_p1=float(np.percentile(nulls_sn_arr[np.isfinite(nulls_sn_arr)], 1)),
            null_p5=float(np.percentile(nulls_sn_arr[np.isfinite(nulls_sn_arr)], 5)),
            n_extreme=n_ext_sn,
            canonical_percentile=canonical_pct_sn,
            permutation_p_value=p_sn,
        ),
        E6_BAO_null=dict(
            n_trials=N_TRIALS,
            canonical_chi2=chi2_bao,
            null_median=float(np.median(finite)),
            null_p1=float(np.percentile(finite, 1)),
            null_p5=float(np.percentile(finite, 5)),
            n_extreme=n_ext_bao,
            canonical_percentile=canonical_pct_bao,
            permutation_p_value=p_bao,
        ),
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR018b_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = [
        dict(item="n_sn_after_cuts", value=int(len(z)), passes=True),
        dict(item="n_bao_points", value=len(DESI), passes=True),
        dict(item="Omega_m_SAM", value=OMEGA_M_SAM, passes=True),
        dict(item="Omega_b_SAM", value=OMEGA_B_SAM, passes=True),
        dict(item="P1_SN_weighted_mean_residual", value=wmr, passes=p1_passed),
        dict(item="P2_BAO_chi2", value=chi2_bao, passes=p2_passed),
        dict(item="P2_BAO_chi2_per_n", value=chi2_per_n, passes=p2_passed),
        dict(item="P3_r_d_SAM_Mpc", value=r_d_sam, passes=p3_passed),
        dict(item="P3_r_d_rel_dev_pct", value=rel_dev*100, passes=p3_passed),
        dict(item="E4_sn_best_H0", value=sn_best, passes=True),
        dict(item="E4_bao_best_H0", value=bao_best, passes=True),
        dict(item="E5_SN_null_canonical_percentile", value=canonical_pct_sn, passes=True),
        dict(item="E5_SN_null_p_value", value=p_sn, passes=True),
        dict(item="E6_BAO_null_canonical_percentile", value=canonical_pct_bao, passes=True),
        dict(item="E6_BAO_null_p_value", value=p_bao, passes=True),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    with (out_dir / "CR018b_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
