"""
SAM SN/BAO distance formula scratch.

Tests the formula from distances.pdf:
  Omega_A = 1 - 1/pi
  E_SAM(z) = sqrt( (1/pi) (1+z)^3 + (1 - 1/pi) )
  D_M(z) = (c/H_0) * integral_0^z dz' / E_SAM(z')
  D_L(z) = (1+z) * D_M(z)

This is exploratory work. NOT a sealed CR.

Quick comparison: SAM with Omega_m = 1/pi vs LambdaCDM with Omega_m = 0.3 on
the Pantheon+SH0ES sample. One nuisance offset M absorbs H_0 scaling.
"""

from __future__ import annotations

from pathlib import Path
import math

import numpy as np
from scipy.integrate import quad

PANTHEON = Path(
    r"C:\VS\quantum_phase\data\external\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat"
)

C = 299792.458  # km/s


def E_SAM(z: float) -> float:
    """SAM E(z) per distances.pdf."""
    inv_pi = 1.0 / math.pi
    return math.sqrt(inv_pi * (1.0 + z) ** 3 + (1.0 - inv_pi))


def E_LCDM(z: float, Omega_m: float) -> float:
    """Standard flat LambdaCDM E(z)."""
    return math.sqrt(Omega_m * (1.0 + z) ** 3 + (1.0 - Omega_m))


def D_M_unitless(z: float, E_func) -> float:
    """Integral of dz' / E(z') from 0 to z. Units of c/H_0."""
    val, _ = quad(lambda zp: 1.0 / E_func(zp), 0.0, z, limit=200, epsabs=1e-9)
    return val


def mu_theory(z: float, E_func, H0_kms_Mpc: float = 70.0) -> float:
    """Distance modulus in mag for a given E(z) shape, fixed H0."""
    DH = C / H0_kms_Mpc  # Hubble distance in Mpc
    DM = DH * D_M_unitless(z, E_func)
    DL = (1.0 + z) * DM
    return 25.0 + 5.0 * math.log10(DL)  # mu = 25 + 5 log10(DL/Mpc)


def load_pantheon(path: Path):
    """Return (z, mu_obs, mu_err, is_calibrator) arrays."""
    with path.open("r") as f:
        header = f.readline().strip().split()
    idx_z   = header.index("zHD")
    idx_mu  = header.index("MU_SH0ES")
    idx_err = header.index("MU_SH0ES_ERR_DIAG")
    idx_cal = header.index("IS_CALIBRATOR")

    rows = np.genfromtxt(path, skip_header=1, dtype=float,
                         usecols=(idx_z, idx_mu, idx_err, idx_cal))
    z   = rows[:, 0]
    mu  = rows[:, 1]
    err = rows[:, 2]
    cal = rows[:, 3].astype(int)
    return z, mu, err, cal


def fit_offset_and_chi2(z, mu_obs, mu_err, E_func, H0=70.0):
    """Fit a single nuisance offset Delta and return (Delta, chi2, n)."""
    mu_th = np.array([mu_theory(zi, E_func, H0) for zi in z])
    # Weighted offset = sum(w*(obs-th)) / sum(w), w = 1/err^2
    w = 1.0 / (mu_err ** 2)
    delta = float(np.sum(w * (mu_obs - mu_th)) / np.sum(w))
    resid = mu_obs - mu_th - delta
    chi2 = float(np.sum((resid / mu_err) ** 2))
    return delta, chi2, len(z), resid


def main():
    z, mu, err, cal = load_pantheon(PANTHEON)
    print(f"Loaded {len(z)} Pantheon+ rows")

    # Standard cosmology cuts: z > 0.01, non-calibrators
    mask = (z > 0.01) & (cal == 0) & np.isfinite(mu) & np.isfinite(err) & (err > 0)
    z = z[mask]; mu = mu[mask]; err = err[mask]
    print(f"After z>0.01 + non-calibrator cuts: {len(z)} rows")
    print(f"z range: [{z.min():.4f}, {z.max():.4f}]")

    # ---------- ZERO-CATALOG-PARAMETER TEST ----------
    # H_0 = 73.04 km/s/Mpc is the SH0ES measurement input baked into MU_SH0ES.
    # No offset fit. No catalog-derived nuisance. Pure prediction.
    print("\n=== SAM ZERO-PARAMETER prediction: Omega_m=1/pi, H_0=73.04 SH0ES input ===")
    H0_SH0ES = 73.04
    mu_th_zero = np.array([mu_theory(zi, E_SAM, H0_SH0ES) for zi in z])
    resid_zero = mu - mu_th_zero
    w0 = 1.0 / (err ** 2)
    mean_resid_zero = float(np.sum(w0 * resid_zero) / np.sum(w0))
    chi2_zero = float(np.sum((resid_zero / err) ** 2))
    rms_zero = float(np.sqrt(np.mean(resid_zero ** 2)))
    print(f"  catalog-fit parameters used:    0")
    print(f"  measurement inputs:             H_0 = 73.04 (SH0ES), Omega_m = 1/pi (substrate)")
    print(f"  weighted mean residual:         {mean_resid_zero:+.4f} mag")
    print(f"  chi^2 / n (no offset fit):      {chi2_zero:.2f} / {n_sam if False else len(z)} = {chi2_zero/len(z):.4f}")
    print(f"  RMS residual:                   {rms_zero:.4f} mag")

    # For comparison: LCDM Planck Omega_m + SH0ES H_0 with no fit either
    mu_th_l_zero = np.array([mu_theory(zi, lambda zp: E_LCDM(zp, 0.315), H0_SH0ES) for zi in z])
    resid_l_zero = mu - mu_th_l_zero
    mean_resid_l_zero = float(np.sum(w0 * resid_l_zero) / np.sum(w0))
    chi2_l_zero = float(np.sum((resid_l_zero / err) ** 2))
    rms_l_zero = float(np.sqrt(np.mean(resid_l_zero ** 2)))
    print(f"\n  LCDM(Planck Omega_m=0.315, H_0=73.04, NO offset fit):")
    print(f"    weighted mean residual:       {mean_resid_l_zero:+.4f} mag")
    print(f"    chi^2 / n:                    {chi2_l_zero/len(z):.4f}")
    print(f"    RMS residual:                 {rms_l_zero:.4f} mag")

    print("\n=== SAM distance formula (Omega_m = 1/pi) with single nuisance offset fit ===")
    delta_sam, chi2_sam, n_sam, resid_sam = fit_offset_and_chi2(
        z, mu, err, lambda zp: E_SAM(zp)
    )
    rms_sam = float(np.sqrt(np.mean(resid_sam ** 2)))
    print(f"  best-fit nuisance offset Delta = {delta_sam:+.4f} mag")
    print(f"  chi^2 / n = {chi2_sam:.2f} / {n_sam} = {chi2_sam/n_sam:.4f}")
    print(f"  RMS residual = {rms_sam:.4f} mag")
    print(f"  Omega_m = 1/pi = {1/math.pi:.6f}")
    print(f"  Omega_A = 1 - 1/pi = {1 - 1/math.pi:.6f}")

    print("\n=== LambdaCDM baseline Omega_m = 0.30 ===")
    delta_lcdm, chi2_lcdm, n_lcdm, resid_lcdm = fit_offset_and_chi2(
        z, mu, err, lambda zp: E_LCDM(zp, 0.30)
    )
    rms_lcdm = float(np.sqrt(np.mean(resid_lcdm ** 2)))
    print(f"  best-fit nuisance offset Delta = {delta_lcdm:+.4f} mag")
    print(f"  chi^2 / n = {chi2_lcdm:.2f} / {n_lcdm} = {chi2_lcdm/n_lcdm:.4f}")
    print(f"  RMS residual = {rms_lcdm:.4f} mag")

    print("\n=== LambdaCDM Omega_m = 0.315 (Planck) ===")
    delta_p, chi2_p, n_p, resid_p = fit_offset_and_chi2(
        z, mu, err, lambda zp: E_LCDM(zp, 0.315)
    )
    rms_p = float(np.sqrt(np.mean(resid_p ** 2)))
    print(f"  best-fit nuisance offset Delta = {delta_p:+.4f} mag")
    print(f"  chi^2 / n = {chi2_p:.2f} / {n_p} = {chi2_p/n_p:.4f}")
    print(f"  RMS residual = {rms_p:.4f} mag")

    # Direct comparison
    print("\n=== Side-by-side at headline redshifts ===")
    print(f"  {'z':>7}  {'mu_SAM':>9}  {'mu_LCDM(0.30)':>13}  {'mu_LCDM(Planck)':>16}  delta")
    for zi in (0.05, 0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0):
        mu_s = mu_theory(zi, E_SAM, 70.0)
        mu_l = mu_theory(zi, lambda zp: E_LCDM(zp, 0.30), 70.0)
        mu_p = mu_theory(zi, lambda zp: E_LCDM(zp, 0.315), 70.0)
        print(f"  {zi:>7.3f}  {mu_s:>9.4f}  {mu_l:>13.4f}  {mu_p:>16.4f}  "
              f"SAM-LCDM={mu_s-mu_l:+.4f}")

    # Headline comparison
    print("\n=== Headline ===")
    print(f"  SAM        : chi^2/n = {chi2_sam/n_sam:.4f}   RMS = {rms_sam:.4f}")
    print(f"  LCDM(0.30) : chi^2/n = {chi2_lcdm/n_lcdm:.4f}   RMS = {rms_lcdm:.4f}")
    print(f"  LCDM(0.315): chi^2/n = {chi2_p/n_p:.4f}   RMS = {rms_p:.4f}")
    print(f"  Delta chi^2: SAM - LCDM(0.30) = {chi2_sam - chi2_lcdm:+.2f}")
    print(f"               SAM - LCDM(0.315) = {chi2_sam - chi2_p:+.2f}")

    # Z-binned residual structure
    print("\n=== SAM residuals binned in z (sanity check for systematic trends) ===")
    bin_edges = np.array([0.01, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.5])
    print(f"  {'z_low':>7}  {'z_high':>7}  {'n':>5}  {'mean_resid':>11}  {'std_resid':>11}")
    for i in range(len(bin_edges) - 1):
        m = (z >= bin_edges[i]) & (z < bin_edges[i + 1])
        if m.sum() < 3:
            continue
        print(f"  {bin_edges[i]:>7.2f}  {bin_edges[i+1]:>7.2f}  "
              f"{m.sum():>5d}  {resid_sam[m].mean():>+11.4f}  {resid_sam[m].std():>11.4f}")


if __name__ == "__main__":
    main()
