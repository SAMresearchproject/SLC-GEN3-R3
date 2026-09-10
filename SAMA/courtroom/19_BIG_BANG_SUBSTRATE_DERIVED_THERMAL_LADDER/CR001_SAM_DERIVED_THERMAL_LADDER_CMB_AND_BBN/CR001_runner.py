"""
CR001@19_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN runner.

Implements the test specified in CR001_PRECOMMIT.md (SHA-256
7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff).

Full ladder (per PDF):
  A_0, alpha_H, D -> Omega_m, Omega_b
  thermal clock H(a), T(a)
  z_eq, k_eq
  Saha + tau_Thomson(a_*) = 1 -> z_*  (DERIVED, no Hu-Sugiyama)
  r_s(z_*), D_M(z_*), theta_*, ell_A
  tau_drag(a_d) = 1 -> z_d            (DERIVED, no Eisenstein-Hu)
  r_d
  eta_10, Y_p schematic, D/H ~ eta^-1.6

Outputs:
  CR001_summary.json
  CR001_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import cumulative_trapezoid

# ============================================================================
# CONSTANTS (SI)
# ============================================================================
PI = math.pi
C_KMS = 299792.458
C_M_S = 2.99792458e8
HBAR = 1.054571817e-34          # J*s
K_B = 1.380649e-23              # J/K
M_E = 9.1093837015e-31          # kg (electron)
M_P = 1.67262192369e-27         # kg (proton)
G_N = 6.67430e-11               # m^3/(kg s^2)
SIGMA_T = 6.6524587321e-29      # m^2 Thomson cross-section
EV_J = 1.602176634e-19          # J/eV
ION_E_J = 13.6 * EV_J           # hydrogen ionization energy
MPC_M = 3.0856775815e22         # m/Mpc
KM_M = 1000.0                   # m/km
ZETA3 = 1.2020569

# Particle physics (natural units, GeV)
GEV_J = 1.602176634e-10         # J/GeV
G_F_GEVM2 = 1.1663787e-5        # GeV^-2 Fermi constant
M_PL_GEV = 1.220890e19          # GeV reduced Planck mass times sqrt(8 pi) ~ Planck mass
DELTA_M_NP_GEV = 1.2933e-3      # GeV neutron-proton mass difference
TAU_N_S = 879.4                 # s neutron mean lifetime
G_A = 1.2754                    # axial coupling
HBAR_OVER_GEV = HBAR / GEV_J    # 6.582e-25 s (1 GeV^-1 in seconds)

# ============================================================================
# SUBSTRATE INPUTS (sealed identities)
# ============================================================================
A_0 = 1.0 / (12.0 * PI)
ALPHA_H = 2
D_DIM = 3
R_RADIX = 2 * ALPHA_H * D_DIM    # 12
S_SPLIT = 2 ** D_DIM             # 8
THETA = ALPHA_H * D_DIM ** 2     # 18

OMEGA_M_SAM = R_RADIX * A_0      # 1/pi
CHI = (S_SPLIT / D_DIM) * A_0    # (8/3)*A_0 = 2/(9 pi)
OMEGA_B_SAM = 2.0 * A_0 * (1.0 - CHI)

# ============================================================================
# MEASUREMENT INPUTS
# ============================================================================
H0_KMS_MPC = 68.76
T_0 = 2.7255                     # K (FIRAS)
N_EFF = 3.046
REL_FACTOR = 1.0 + (7.0/8.0) * (4.0/11.0)**(4.0/3.0) * N_EFF  # 1 + 0.2271 N_eff

# ============================================================================
# PLANCK 2018 REFERENCES
# ============================================================================
PLANCK_Z_EQ           = 3402.0
PLANCK_Z_STAR         = 1089.92
PLANCK_Z_DRAG         = 1059.94
PLANCK_RS_ZSTAR_MPC   = 144.43
PLANCK_R_D_MPC        = 147.09
PLANCK_DM_ZSTAR_MPC   = 13869.6
PLANCK_ELL_A          = 301.76
PLANCK_100THETA_STAR  = 1.04110

# BBN observation
OBS_Y_P     = 0.245
OBS_D_H     = 2.527e-5
OBS_ETA_10  = 6.10

# ============================================================================
# GATES
# ============================================================================
P1_THRESH = 0.05   # 100*theta_*
P2_THRESH = 0.05   # ell_A
P3_THRESH = 0.05   # r_d

N_TRIALS = 1000

# ============================================================================
# THERMAL LADDER (per-trial)
# ============================================================================

def thermal_ladder(Omega_m, Omega_b, H0_kms_Mpc):
    """Run the full SAM thermal ladder. Returns dict or None on unphysical."""
    if Omega_m <= 0 or Omega_b <= 0 or H0_kms_Mpc <= 0:
        return None
    if Omega_b >= Omega_m:
        return None

    h_si = H0_kms_Mpc * KM_M / MPC_M  # s^-1
    rho_c_0 = 3.0 * h_si**2 / (8.0 * PI * G_N)  # kg/m^3

    # Photon density from FIRAS T_0
    rho_gamma_energy = (PI**2 / 15.0) * (K_B * T_0)**4 / (HBAR**3 * C_M_S**3)  # J/m^3
    rho_gamma_mass = rho_gamma_energy / C_M_S**2  # kg/m^3
    Omega_gamma = rho_gamma_mass / rho_c_0
    Omega_r = Omega_gamma * REL_FACTOR
    Omega_L = 1.0 - Omega_m - Omega_r

    if Omega_L <= 0:
        return None

    # a grid in log space
    a_grid = np.logspace(-7, 0, 4000)
    E_grid = np.sqrt(Omega_r / a_grid**4 + Omega_m / a_grid**3 + Omega_L)
    H_grid_si = h_si * E_grid

    # Equality
    a_eq = Omega_r / Omega_m
    z_eq = 1.0 / a_eq - 1.0
    E_aeq = math.sqrt(Omega_r / a_eq**4 + Omega_m / a_eq**3 + Omega_L)
    H_aeq_si = h_si * E_aeq
    k_eq_per_m = a_eq * H_aeq_si / C_M_S
    k_eq_per_Mpc = k_eq_per_m * MPC_M

    # Saha x_e
    T_K = T_0 / a_grid
    T_J = K_B * T_K
    n_b_grid = Omega_b * rho_c_0 / (M_P * a_grid**3)
    prefactor = (M_E * T_J / (2.0 * PI * HBAR**2))**1.5
    # Use safe exponent to avoid underflow
    exponent = -ION_E_J / T_J
    boltzmann = np.exp(np.clip(exponent, -700.0, 700.0))
    S_grid = prefactor * boltzmann / n_b_grid
    # x_e = (-S + sqrt(S^2 + 4S))/2.  For S large, x_e -> 1.  For S small, x_e -> sqrt(S).
    S_capped = np.clip(S_grid, 0.0, 1e20)
    sqrt_term = np.sqrt(S_capped**2 + 4.0 * S_capped)
    x_e_grid = 0.5 * (-S_capped + sqrt_term)
    x_e_grid = np.clip(x_e_grid, 0.0, 1.0)
    # Force full ionization at very high T
    x_e_grid = np.where(S_capped > 1e10, 1.0, x_e_grid)

    n_e_grid = x_e_grid * n_b_grid

    # Thomson optical depth: tau(a) = int_a^1 n_e sigma_T c / (a^2 H) da
    integrand_tau = n_e_grid * SIGMA_T * C_M_S / (a_grid**2 * H_grid_si)
    # Cumulative from right
    a_rev = a_grid[::-1]
    integrand_rev = integrand_tau[::-1]
    # cumulative_trapezoid with reversed grid: dx = a_rev[i+1] - a_rev[i] is negative
    # so we negate to get positive contributions
    tau_rev = cumulative_trapezoid(-integrand_rev, a_rev, initial=0.0)
    tau_grid = tau_rev[::-1]  # tau as function of a in original a order

    # Find a_* where tau = 1
    a_star = _interp_a_at_unit_tau(a_grid, tau_grid)
    if a_star is None:
        return None
    z_star = 1.0 / a_star - 1.0

    # Sound horizon r_s(a) = int_0^a c_s/(a'^2 H) da'
    R_b_grid = 0.75 * Omega_b / Omega_gamma * a_grid
    c_s_grid = C_M_S / np.sqrt(3.0 * (1.0 + R_b_grid))
    rs_integrand = c_s_grid / (a_grid**2 * H_grid_si)  # in m
    rs_cum = cumulative_trapezoid(rs_integrand, a_grid, initial=0.0)  # m
    rs_at_astar_m = np.interp(np.log(a_star), np.log(a_grid), rs_cum)
    rs_at_astar_Mpc = rs_at_astar_m / MPC_M

    # D_M(a_*) = c * int_{a_*}^1 da/(a^2 H)
    DM_integrand = 1.0 / (a_grid**2 * H_grid_si)  # s/m
    DM_cum = cumulative_trapezoid(DM_integrand, a_grid, initial=0.0)
    DM_total = DM_cum[-1]
    DM_at_astar = np.interp(np.log(a_star), np.log(a_grid), DM_cum)
    DM_zstar_m = C_M_S * (DM_total - DM_at_astar)
    DM_zstar_Mpc = DM_zstar_m / MPC_M

    # Acoustic angle
    theta_star = rs_at_astar_Mpc / DM_zstar_Mpc
    hundred_theta_star = 100.0 * theta_star
    ell_A = PI / theta_star

    # Drag epoch: tau_d(a) = int_a^1 n_e sigma_T c / (a^2 H R_b) da
    R_b_safe = np.where(R_b_grid > 1e-50, R_b_grid, 1e-50)
    integrand_taud = n_e_grid * SIGMA_T * C_M_S / (a_grid**2 * H_grid_si * R_b_safe)
    integrand_taud_rev = integrand_taud[::-1]
    taud_rev = cumulative_trapezoid(-integrand_taud_rev, a_rev, initial=0.0)
    taud_grid = taud_rev[::-1]
    a_d = _interp_a_at_unit_tau(a_grid, taud_grid)
    if a_d is None:
        return None
    z_d = 1.0 / a_d - 1.0
    rd_m = np.interp(np.log(a_d), np.log(a_grid), rs_cum)
    rd_Mpc = rd_m / MPC_M

    return dict(
        Omega_m=Omega_m, Omega_b=Omega_b, Omega_c=Omega_m - Omega_b,
        Omega_gamma=Omega_gamma, Omega_r=Omega_r, Omega_L=Omega_L,
        H0=H0_kms_Mpc, rho_c_0=rho_c_0,
        a_eq=a_eq, z_eq=z_eq, k_eq_per_Mpc=k_eq_per_Mpc,
        a_star=a_star, z_star=z_star,
        rs_zstar_Mpc=rs_at_astar_Mpc, DM_zstar_Mpc=DM_zstar_Mpc,
        theta_star=theta_star, hundred_theta_star=hundred_theta_star,
        ell_A=ell_A,
        a_d=a_d, z_d=z_d, rd_Mpc=rd_Mpc,
    )


def _interp_a_at_unit_tau(a_grid, tau_grid):
    """Find a where tau(a) = 1 via log-a interpolation. tau_grid is
    monotonically decreasing in a (large tau at small a)."""
    if tau_grid[0] < 1.0:
        return None
    # find first index where tau crosses below 1
    idx = np.argmax(tau_grid < 1.0)
    if idx <= 0:
        return None
    # linear interp in log(a)
    log_a_lo = math.log(a_grid[idx - 1])
    log_a_hi = math.log(a_grid[idx])
    tau_lo = tau_grid[idx - 1]
    tau_hi = tau_grid[idx]
    frac = (tau_lo - 1.0) / (tau_lo - tau_hi)
    log_a_star = log_a_lo + frac * (log_a_hi - log_a_lo)
    return math.exp(log_a_star)


# ============================================================================
# BBN (schematic Wagoner)
# ============================================================================

def bbn_observables(Omega_b, H0_kms_Mpc):
    """Schematic Wagoner BBN. Returns dict."""
    h_si = H0_kms_Mpc * KM_M / MPC_M
    rho_c_0 = 3.0 * h_si**2 / (8.0 * PI * G_N)
    n_b_0 = Omega_b * rho_c_0 / M_P                              # m^-3
    n_gamma_0 = (2.0 * ZETA3 / PI**2) * (K_B * T_0 / (HBAR * C_M_S))**3  # m^-3
    eta = n_b_0 / n_gamma_0
    eta_10 = 1.0e10 * eta

    # Weak freeze-out (natural units)
    g_star = 10.75
    coeff = (7.0 * PI / 60.0) * (1.0 + 3.0 * G_A**2)
    T_f_cubed = 1.66 * math.sqrt(g_star) / (coeff * G_F_GEVM2**2 * M_PL_GEV)
    T_f_GeV = T_f_cubed ** (1.0 / 3.0)
    T_f_MeV = T_f_GeV * 1000.0

    n_p_freeze = math.exp(-DELTA_M_NP_GEV / T_f_GeV)

    # Time at freeze-out (radiation era): t = 1/(2H)
    t_f_natural = M_PL_GEV / (2.0 * 1.66 * math.sqrt(g_star) * T_f_GeV**2)
    t_f_s = t_f_natural * HBAR_OVER_GEV

    # T_BBN (deuterium bottleneck)
    T_BBN_MeV = 0.073
    T_BBN_GeV = T_BBN_MeV * 1.0e-3
    g_star_BBN = 3.36
    t_BBN_natural = M_PL_GEV / (2.0 * 1.66 * math.sqrt(g_star_BBN) * T_BBN_GeV**2)
    t_BBN_s = t_BBN_natural * HBAR_OVER_GEV

    delta_t_s = t_BBN_s - t_f_s
    n_p_bbn = n_p_freeze * math.exp(-delta_t_s / TAU_N_S)
    Y_p = 2.0 * n_p_bbn / (1.0 + n_p_bbn)

    # D/H scaling
    D_H = OBS_D_H * (OBS_ETA_10 / eta_10) ** 1.6

    return dict(
        eta=eta, eta_10=eta_10,
        T_f_MeV=T_f_MeV, n_p_freeze=n_p_freeze,
        t_f_s=t_f_s, t_BBN_s=t_BBN_s, delta_t_s=delta_t_s,
        n_p_bbn=n_p_bbn, Y_p=Y_p,
        D_H=D_H,
    )


# ============================================================================
# MAIN
# ============================================================================

def deviation(sam, ref):
    return (sam - ref) / ref


def main():
    out_dir = Path(__file__).parent

    print("=" * 78)
    print("CR001@19 -- SAM-derived thermal ladder: CMB compressed geometry + BBN")
    print("=" * 78)
    print(f"\nSubstrate inventory (sealed):")
    print(f"  A_0      = 1/(12*pi)              = {A_0:.8f}")
    print(f"  alpha_H  = {ALPHA_H}")
    print(f"  D        = {D_DIM}")
    print(f"  R        = 2*alpha_H*D            = {R_RADIX}")
    print(f"  S        = 2^D                    = {S_SPLIT}")
    print(f"  Theta    = alpha_H*D^2            = {THETA}")
    print(f"\nDerived densities (sealed identities):")
    print(f"  Omega_m  = R*A_0 = 1/pi           = {OMEGA_M_SAM:.6f}")
    print(f"  chi      = (S/D)*A_0 = 2/(9 pi)   = {CHI:.6f}")
    print(f"  Omega_b  = 2*A_0*(1-chi)          = {OMEGA_B_SAM:.6f}")
    print(f"  Omega_c  = Omega_m - Omega_b      = {OMEGA_M_SAM - OMEGA_B_SAM:.6f}")
    print(f"\nMeasurement inputs (not catalog fit):")
    print(f"  H_0      = {H0_KMS_MPC} km/s/Mpc")
    print(f"  T_0      = {T_0} K (FIRAS)")
    print(f"  N_eff    = {N_EFF}")

    # === Canonical thermal ladder ===
    canon = thermal_ladder(OMEGA_M_SAM, OMEGA_B_SAM, H0_KMS_MPC)
    if canon is None:
        print("\nERROR: canonical ladder failed (unphysical?)")
        return
    bbn = bbn_observables(OMEGA_B_SAM, H0_KMS_MPC)

    print(f"\nRadiation: Omega_gamma = {canon['Omega_gamma']:.4e}, "
          f"Omega_r = {canon['Omega_r']:.4e}, Omega_L = {canon['Omega_L']:.6f}")

    print("\n" + "=" * 78)
    print("Thermal ladder outputs vs Planck 2018 base-LCDM")
    print("=" * 78)
    rows = [
        ("z_eq",            canon["z_eq"],             PLANCK_Z_EQ),
        ("z_star (DERIVED)", canon["z_star"],          PLANCK_Z_STAR),
        ("z_drag (DERIVED)", canon["z_d"],             PLANCK_Z_DRAG),
        ("r_s(z_star) Mpc", canon["rs_zstar_Mpc"],     PLANCK_RS_ZSTAR_MPC),
        ("r_d Mpc",         canon["rd_Mpc"],           PLANCK_R_D_MPC),
        ("D_M(z_star) Mpc", canon["DM_zstar_Mpc"],     PLANCK_DM_ZSTAR_MPC),
        ("ell_A",           canon["ell_A"],            PLANCK_ELL_A),
        ("100*theta_*",     canon["hundred_theta_star"], PLANCK_100THETA_STAR),
    ]
    print(f"{'observable':<22s} {'SAM':>14s}    {'Planck 2018':>14s}    {'dev':>10s}")
    print("-" * 78)
    for name, sam, planck in rows:
        dev = deviation(sam, planck) * 100.0
        print(f"{name:<22s} {sam:14.4f}    {planck:14.4f}    {dev:+9.3f}%")

    print(f"\nk_eq                            = {canon['k_eq_per_Mpc']:.5f} 1/Mpc  (reported, no Planck point ref)")

    print("\n" + "=" * 78)
    print("BBN observables (schematic Wagoner; reported, not gated)")
    print("=" * 78)
    print(f"  eta_10                = {bbn['eta_10']:.3f}        (obs: {OBS_ETA_10}, dev: {(bbn['eta_10']-OBS_ETA_10)/OBS_ETA_10*100:+.2f}%)")
    print(f"  T_f                   = {bbn['T_f_MeV']:.4f} MeV  (textbook ~0.8 MeV; schematic with g_A={G_A})")
    print(f"  (n/p)_freeze          = {bbn['n_p_freeze']:.4f}")
    print(f"  t_f                   = {bbn['t_f_s']:.3f} s")
    print(f"  t_BBN                 = {bbn['t_BBN_s']:.3f} s")
    print(f"  delta_t               = {bbn['delta_t_s']:.3f} s   (neutron decay window)")
    print(f"  (n/p)_BBN             = {bbn['n_p_bbn']:.4f}")
    print(f"  Y_p (schematic)       = {bbn['Y_p']:.4f}        (obs: {OBS_Y_P}, dev: {(bbn['Y_p']-OBS_Y_P)/OBS_Y_P*100:+.2f}%)")
    print(f"  D/H (eta^-1.6 scale)  = {bbn['D_H']:.3e}    (obs: {OBS_D_H:.3e}, dev: {(bbn['D_H']-OBS_D_H)/OBS_D_H*100:+.2f}%)")

    # === Gates ===
    dev_100theta = deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR)
    dev_ellA     = deviation(canon["ell_A"],              PLANCK_ELL_A)
    dev_rd       = deviation(canon["rd_Mpc"],             PLANCK_R_D_MPC)

    p1_passed = abs(dev_100theta) <= P1_THRESH
    p2_passed = abs(dev_ellA)     <= P2_THRESH
    p3_passed = abs(dev_rd)       <= P3_THRESH

    print("\n" + "=" * 78)
    print("Load-bearing gates (5% on each acoustic-geometry observable)")
    print("=" * 78)
    print(f"  P1  |100*theta_* dev| = {abs(dev_100theta)*100:.3f}%   thresh {P1_THRESH*100:.1f}%   {'PASS' if p1_passed else 'FAIL'}")
    print(f"  P2  |ell_A dev|       = {abs(dev_ellA)*100:.3f}%   thresh {P2_THRESH*100:.1f}%   {'PASS' if p2_passed else 'FAIL'}")
    print(f"  P3  |r_d dev|         = {abs(dev_rd)*100:.3f}%   thresh {P3_THRESH*100:.1f}%   {'PASS' if p3_passed else 'FAIL'}")

    # === WC1: random Omega_m ===
    print("\n" + "=" * 78)
    print(f"WC1 null (random Omega_m in [0.05, 0.95], {N_TRIALS} seeded trials)")
    print("=" * 78)
    canonical_abs_dev = abs(deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR))
    wc1_nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed)
        Om_r = float(rng.uniform(0.05, 0.95))
        g = thermal_ladder(Om_r, OMEGA_B_SAM, H0_KMS_MPC)
        if g is None:
            wc1_nulls.append(float("inf"))
        else:
            wc1_nulls.append(abs(deviation(g["hundred_theta_star"], PLANCK_100THETA_STAR)))
    wc1_arr = np.array(wc1_nulls)
    finite_wc1 = wc1_arr[np.isfinite(wc1_arr)]
    n_ext_wc1 = int(np.sum(wc1_arr <= canonical_abs_dev))
    p_wc1 = (n_ext_wc1 + 1) / (N_TRIALS + 1)
    canonical_pct_wc1 = float(np.mean(wc1_arr <= canonical_abs_dev) * 100.0)
    print(f"  canonical |100*theta_* dev| / 1.04110 = {canonical_abs_dev:.5f}")
    print(f"  null median |dev|                     = {float(np.median(finite_wc1)):.5f}")
    print(f"  null 1st percentile                   = {float(np.percentile(finite_wc1, 1)):.5f}")
    print(f"  null 5th percentile                   = {float(np.percentile(finite_wc1, 5)):.5f}")
    print(f"  n_null_at_least_as_extreme            = {n_ext_wc1} of {N_TRIALS}")
    print(f"  canonical percentile in null          = {canonical_pct_wc1:.2f}%")
    print(f"  one-sided permutation p-value         = {p_wc1:.5f}")

    # === WC2: random joint ===
    print("\n" + "=" * 78)
    print(f"WC2 null (random (Omega_m, Omega_b), {N_TRIALS} seeded trials)")
    print("=" * 78)
    wc2_nulls = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed + 10_000)
        Om_r = float(rng.uniform(0.05, 0.95))
        Ob_r = float(rng.uniform(0.005, 0.15))
        g = thermal_ladder(Om_r, Ob_r, H0_KMS_MPC)
        if g is None:
            wc2_nulls.append(float("inf"))
        else:
            wc2_nulls.append(abs(deviation(g["hundred_theta_star"], PLANCK_100THETA_STAR)))
    wc2_arr = np.array(wc2_nulls)
    finite_wc2 = wc2_arr[np.isfinite(wc2_arr)]
    n_ext_wc2 = int(np.sum(wc2_arr <= canonical_abs_dev))
    p_wc2 = (n_ext_wc2 + 1) / (N_TRIALS + 1)
    canonical_pct_wc2 = float(np.mean(wc2_arr <= canonical_abs_dev) * 100.0)
    print(f"  canonical |100*theta_* dev| / 1.04110 = {canonical_abs_dev:.5f}")
    print(f"  null median |dev|                     = {float(np.median(finite_wc2)):.5f}")
    print(f"  null 1st percentile                   = {float(np.percentile(finite_wc2, 1)):.5f}")
    print(f"  null 5th percentile                   = {float(np.percentile(finite_wc2, 5)):.5f}")
    print(f"  n_null_at_least_as_extreme            = {n_ext_wc2} of {N_TRIALS}")
    print(f"  canonical percentile in null          = {canonical_pct_wc2:.2f}%")
    print(f"  one-sided permutation p-value         = {p_wc2:.5f}")

    # === Verdict ===
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    gates_pass = p1_passed and p2_passed and p3_passed
    if gates_pass:
        verdict = "PASS"
        verdict_reason = "P1, P2, P3 all hold under canonical substrate inputs"
    else:
        verdict = "FAIL"
        failed = [k for k, v in [("P1", p1_passed), ("P2", p2_passed), ("P3", p3_passed)] if not v]
        verdict_reason = f"failed gate(s): {failed}"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}    P2: {'PASS' if p2_passed else 'FAIL'}    P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR001@19 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # === Write outputs ===
    summary = dict(
        precommit_sha256="7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff",
        substrate=dict(
            A_0=A_0, alpha_H=ALPHA_H, D=D_DIM, R=R_RADIX, S=S_SPLIT, Theta=THETA,
            Omega_m_SAM=OMEGA_M_SAM, chi=CHI,
            Omega_b_SAM=OMEGA_B_SAM, Omega_c_SAM=OMEGA_M_SAM - OMEGA_B_SAM,
        ),
        measurement_inputs=dict(H0=H0_KMS_MPC, T_0=T_0, N_eff=N_EFF),
        planck_reference=dict(
            z_eq=PLANCK_Z_EQ, z_star=PLANCK_Z_STAR, z_drag=PLANCK_Z_DRAG,
            rs_zstar=PLANCK_RS_ZSTAR_MPC, r_d=PLANCK_R_D_MPC,
            DM_zstar=PLANCK_DM_ZSTAR_MPC, ell_A=PLANCK_ELL_A,
            hundred_theta_star=PLANCK_100THETA_STAR,
        ),
        canonical=canon,
        bbn=bbn,
        deviations=dict(
            z_eq_pct          = deviation(canon["z_eq"], PLANCK_Z_EQ) * 100,
            z_star_pct        = deviation(canon["z_star"], PLANCK_Z_STAR) * 100,
            z_drag_pct        = deviation(canon["z_d"], PLANCK_Z_DRAG) * 100,
            rs_zstar_pct      = deviation(canon["rs_zstar_Mpc"], PLANCK_RS_ZSTAR_MPC) * 100,
            r_d_pct           = deviation(canon["rd_Mpc"], PLANCK_R_D_MPC) * 100,
            DM_zstar_pct      = deviation(canon["DM_zstar_Mpc"], PLANCK_DM_ZSTAR_MPC) * 100,
            ell_A_pct         = deviation(canon["ell_A"], PLANCK_ELL_A) * 100,
            hundred_theta_pct = deviation(canon["hundred_theta_star"], PLANCK_100THETA_STAR) * 100,
            Y_p_pct           = (bbn["Y_p"] - OBS_Y_P) / OBS_Y_P * 100,
            D_H_pct           = (bbn["D_H"] - OBS_D_H) / OBS_D_H * 100,
            eta_10_pct        = (bbn["eta_10"] - OBS_ETA_10) / OBS_ETA_10 * 100,
        ),
        P1=dict(name="100*theta_* vs Planck", deviation=dev_100theta, threshold=P1_THRESH, passed=p1_passed),
        P2=dict(name="ell_A vs Planck",       deviation=dev_ellA,     threshold=P2_THRESH, passed=p2_passed),
        P3=dict(name="r_d vs Planck",         deviation=dev_rd,       threshold=P3_THRESH, passed=p3_passed),
        WC1=dict(
            n_trials=N_TRIALS, canonical_abs_dev=canonical_abs_dev,
            null_median=float(np.median(finite_wc1)),
            null_p1=float(np.percentile(finite_wc1, 1)),
            null_p5=float(np.percentile(finite_wc1, 5)),
            n_extreme=n_ext_wc1, canonical_percentile=canonical_pct_wc1, p_value=p_wc1,
        ),
        WC2=dict(
            n_trials=N_TRIALS, canonical_abs_dev=canonical_abs_dev,
            null_median=float(np.median(finite_wc2)),
            null_p1=float(np.percentile(finite_wc2, 1)),
            null_p5=float(np.percentile(finite_wc2, 5)),
            n_extreme=n_ext_wc2, canonical_percentile=canonical_pct_wc2, p_value=p_wc2,
        ),
        verdict=verdict, verdict_reason=verdict_reason,
    )
    (out_dir / "CR001_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    # Evidence rows
    evidence = []
    for name, sam, planck in rows:
        evidence.append(dict(item=f"{name}_SAM", value=sam, passes=True))
        evidence.append(dict(item=f"{name}_Planck", value=planck, passes=True))
        evidence.append(dict(item=f"{name}_dev_pct", value=deviation(sam, planck) * 100, passes=True))
    evidence.append(dict(item="k_eq_per_Mpc", value=canon["k_eq_per_Mpc"], passes=True))
    # BBN
    evidence.append(dict(item="eta_10_SAM", value=bbn["eta_10"], passes=True))
    evidence.append(dict(item="eta_10_obs", value=OBS_ETA_10, passes=True))
    evidence.append(dict(item="eta_10_dev_pct", value=(bbn["eta_10"]-OBS_ETA_10)/OBS_ETA_10*100, passes=True))
    evidence.append(dict(item="T_f_MeV_schematic", value=bbn["T_f_MeV"], passes=True))
    evidence.append(dict(item="(n/p)_freeze_schematic", value=bbn["n_p_freeze"], passes=True))
    evidence.append(dict(item="(n/p)_BBN_schematic", value=bbn["n_p_bbn"], passes=True))
    evidence.append(dict(item="Y_p_SAM_schematic", value=bbn["Y_p"], passes=True))
    evidence.append(dict(item="Y_p_obs", value=OBS_Y_P, passes=True))
    evidence.append(dict(item="Y_p_dev_pct_schematic", value=(bbn["Y_p"]-OBS_Y_P)/OBS_Y_P*100, passes=True))
    evidence.append(dict(item="D_H_SAM_scaled", value=bbn["D_H"], passes=True))
    evidence.append(dict(item="D_H_obs", value=OBS_D_H, passes=True))
    evidence.append(dict(item="D_H_dev_pct", value=(bbn["D_H"]-OBS_D_H)/OBS_D_H*100, passes=True))
    # Gates
    evidence.append(dict(item="P1_100theta_passed", value=p1_passed, passes=p1_passed))
    evidence.append(dict(item="P2_ellA_passed",     value=p2_passed, passes=p2_passed))
    evidence.append(dict(item="P3_rd_passed",       value=p3_passed, passes=p3_passed))
    # WCs
    evidence.append(dict(item="WC1_canonical_percentile", value=canonical_pct_wc1, passes=True))
    evidence.append(dict(item="WC1_p_value",              value=p_wc1, passes=True))
    evidence.append(dict(item="WC2_canonical_percentile", value=canonical_pct_wc2, passes=True))
    evidence.append(dict(item="WC2_p_value",              value=p_wc2, passes=True))
    evidence.append(dict(item="verdict", value=verdict, passes=(verdict == "PASS")))

    with (out_dir / "CR001_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
