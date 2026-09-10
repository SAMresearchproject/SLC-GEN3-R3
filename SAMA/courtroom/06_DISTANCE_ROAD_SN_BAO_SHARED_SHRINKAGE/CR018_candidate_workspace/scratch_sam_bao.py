"""
SAM BAO scratch — DESI DR1 (2024).

Same SAM cosmology as scratch_sam_distance.py, now against the DESI BAO
distance ratios D_M/r_d, D_H/r_d, D_V/r_d.

Zero catalog parameters fit. Measurement inputs:
  - H_0 (external; we test at H_0 = 68.76 SAM-CMB-preferred and 73.04 SH0ES)
  - r_d computed from Eisenstein-Hu fitting formula given SAM Omega_m and Omega_b
SAM substrate inputs:
  - Omega_m = 1/pi              (A_inf = R * A_0 = 1/pi, Section 7)
  - Omega_b = 2*A_0*(1 - chi)    (Section 7 with chi = (2^D/D)*A_0 = (8/3)/(12 pi) = 2/(9 pi))

DESI DR1 BAO values are HARDCODED from the published 2024 release.
Errors treated as independent (no covariance). r_d carries a ~2% EH
fitting-formula systematic; STAM-vs-LCDM relative comparison cancels it.
"""

from __future__ import annotations
import math
import numpy as np
from scipy.integrate import quad

C = 299792.458
PI = math.pi
OMEGA_GAMMA_H2 = 2.4728e-5
REL_FACTOR = 1.0 + 0.2271 * 3.046

# --- DESI DR1 (2024) BAO measurements
# (tracer, z_eff, observable, value, sigma); observable in {DM, DH, DV} / r_d
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


def sam_omegas():
    """Section 7 zero-parameter substrate values."""
    A_0 = 1.0 / (12.0 * PI)        # native accumulation floor
    R = 12.0
    A_inf = R * A_0                # = 1/pi
    Om = A_inf                     # = 1/pi  (matter density fraction)
    mu_H = 8.0 / 3.0               # 2^D / D with D = 3
    chi = mu_H * A_0               # = 2 / (9*pi)
    Ob = 2.0 * A_0 * (1.0 - chi)   # full Section 7 horizon-quotient-corrected
    return Om, Ob, chi


def cosmology(Om, Ob, H0):
    """Flat-LCDM-shape cosmology with EH r_d. Same form used by SAM and LCDM
    reference; only Om, Ob, H0 differ."""
    h = H0 / 100.0
    wm = Om * h * h
    wb = Ob * h * h
    Og = OMEGA_GAMMA_H2 / (h * h)
    Or = Og * REL_FACTOR
    Ode = 1.0 - Om - Or

    def E(z):
        return math.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + Ode)

    # Eisenstein-Hu z_drag
    b1 = 0.313 * wm ** -0.419 * (1.0 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    zdrag = 1291.0 * wm ** 0.251 / (1.0 + 0.659 * wm ** 0.828) * (1.0 + b1 * wb ** b2)

    def cs_over_H(z):
        Rb = 0.75 * Ob / Og / (1.0 + z)
        return C / math.sqrt(3.0 * (1.0 + Rb)) / (H0 * E(z))

    r_d, _ = quad(cs_over_H, zdrag, np.inf, limit=400)

    def DM(z):
        val, _ = quad(lambda x: 1.0 / E(x), 0.0, z, limit=200)
        return C / H0 * val

    def DH(z):
        return C / (H0 * E(z))

    def DV(z):
        return (z * DM(z) ** 2 * DH(z)) ** (1.0 / 3.0)

    return dict(r_d=r_d, DM=DM, DH=DH, DV=DV, Om=Om, Ob=Ob, H0=H0, wm=wm, wb=wb, zdrag=zdrag)


def evaluate(name, cos):
    print(f"\n  [{name}]")
    print(f"    Om = {cos['Om']:.6f}   Ob = {cos['Ob']:.6f}   H0 = {cos['H0']:.2f}")
    print(f"    wm = {cos['wm']:.5f}   wb = {cos['wb']:.6f}   z_drag = {cos['zdrag']:.1f}")
    print(f"    r_d = {cos['r_d']:.2f} Mpc")
    print(f"\n    {'tracer':<10} {'z_eff':>6} {'obs':>4} {'DESI':>9} {'SAM':>9} "
          f"{'(o-m)':>9} {'sigma':>6} {'(o-m)/sigma':>12}")
    print(f"    {'-'*10} {'-'*6} {'-'*4} {'-'*9} {'-'*9} {'-'*9} {'-'*6} {'-'*12}")
    chi2 = 0.0
    for tr, z, obs, val, sig in DESI:
        f = {"DM": cos["DM"], "DH": cos["DH"], "DV": cos["DV"]}[obs]
        m = f(z) / cos["r_d"]
        s = (val - m) / sig
        chi2 += s * s
        print(f"    {tr:<10} {z:>6.3f} {obs:>4} {val:>9.2f} {m:>9.2f} "
              f"{val-m:>+9.3f} {sig:>6.2f} {s:>+12.2f}")
    print(f"\n    chi^2 (diagonal-error approx) = {chi2:.2f}  over {len(DESI)} points")
    print(f"    chi^2 / n                       = {chi2/len(DESI):.3f}")
    return chi2


def main():
    print("=" * 78)
    print("BAO scratch -- parameter-free SAM cosmology vs DESI DR1 (PROVISIONAL)")
    print("=" * 78)

    Om_s, Ob_s, chi = sam_omegas()
    print(f"\nSubstrate identities (Section 7):")
    print(f"  A_0 = 1/(12 pi)            = {1.0/(12.0*PI):.6f}")
    print(f"  Omega_m = A_inf = R*A_0    = 1/pi = {Om_s:.6f}")
    print(f"  chi = (2^D/D) * A_0        = 2/(9 pi) = {chi:.6f}")
    print(f"  Omega_b = 2*A_0*(1 - chi)  = {Ob_s:.6f}")
    print(f"  Omega_b (Planck reference)            ~ 0.04930 (Section 7 match within rounding)")

    print()
    print("=" * 78)
    print("SAM zero-parameter @ H_0 = 68.76 (SAM-CMB-preferred)")
    print("=" * 78)
    c1 = cosmology(Om_s, Ob_s, 68.76)
    chi2_1 = evaluate("SAM Omega_m=1/pi, Omega_b=Section_7, H_0=68.76", c1)

    print()
    print("=" * 78)
    print("SAM zero-parameter @ H_0 = 73.04 (SH0ES)")
    print("=" * 78)
    c2 = cosmology(Om_s, Ob_s, 73.04)
    chi2_2 = evaluate("SAM Omega_m=1/pi, Omega_b=Section_7, H_0=73.04", c2)

    print()
    print("=" * 78)
    print("Planck LCDM reference (Om=0.3153, Ob*h^2=0.02237, H_0=67.36) -- fit to CMB")
    print("=" * 78)
    c3 = cosmology(0.3153, 0.02237 / (0.6736 ** 2), 67.36)
    chi2_3 = evaluate("Planck LCDM (curve only; parameter-fit baseline)", c3)

    print()
    print("=" * 78)
    print("Headline")
    print("=" * 78)
    print(f"  SAM (Omega substrate-only) @ H_0=68.76   chi^2 = {chi2_1:.2f} / {len(DESI)} = {chi2_1/len(DESI):.3f}")
    print(f"  SAM (Omega substrate-only) @ H_0=73.04   chi^2 = {chi2_2:.2f} / {len(DESI)} = {chi2_2/len(DESI):.3f}")
    print(f"  Planck LCDM (parameter-fit reference)    chi^2 = {chi2_3:.2f} / {len(DESI)} = {chi2_3/len(DESI):.3f}")
    print()
    print("  Delta chi^2:")
    print(f"    SAM(68.76) - Planck LCDM = {chi2_1 - chi2_3:+.2f}")
    print(f"    SAM(73.04) - Planck LCDM = {chi2_2 - chi2_3:+.2f}")
    print()
    print("  Catalog-fit parameters in SAM:      0")
    print("  Catalog-fit parameters in LCDM(ref): 5+ (Om, Ob*h^2, H_0, ns, As; CMB-fit)")
    print()
    print("(DESI values hardcoded from DR1 public release; errors independent; r_d carries")
    print(" ~2% EH fitting-formula systematic — SAM-vs-LCDM relative comparison cancels it.)")


if __name__ == "__main__":
    main()
