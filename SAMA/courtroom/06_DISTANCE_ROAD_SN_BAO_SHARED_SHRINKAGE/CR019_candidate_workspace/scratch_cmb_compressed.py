"""
Scratch: CMB compressed acoustic geometry from sealed substrate inputs.

Layer 1 of the CMB test stack. Inputs are entirely sealed; no catalog fit.

Inputs (sealed substrate):
  Omega_m = 1/pi
  Omega_b = 2 * A_0 * (1 - chi)        A_0 = 1/(12*pi),  chi = (8/3)*A_0 = 2/(9*pi)
  H_0     = 68.76 km/s/Mpc             (BAO-side anchor used in CR018b)
  T_CMB   = 2.7255 K                   (FIRAS measurement input)
  N_eff   = 3.046                      (standard-model neutrino background)

Outputs (compressed CMB geometry):
  z_eq            matter-radiation equality
  z_star          photon decoupling (Hu-Sugiyama 1996 fit)
  z_drag          drag epoch (Eisenstein-Hu 1998 fit)
  r_s(z_star)     sound horizon at last scattering
  r_d             sound horizon at drag epoch
  D_M(z_star)     comoving angular diameter distance to last scattering
  ell_A           acoustic peak multipole = pi * D_M(z_star) / r_s(z_star)
  100 * theta_*   acoustic angular scale

Reference: Planck 2018 base-LambdaCDM (TT,TE,EE+lowE+lensing).
"""

import math
import numpy as np
from scipy.integrate import quad

PI = math.pi
C_KMS = 299792.458

# -------- substrate inputs (sealed identities) --------
A_0 = 1.0 / (12.0 * PI)
OMEGA_M = 1.0 / PI
CHI = (8.0 / 3.0) * A_0
OMEGA_B = 2.0 * A_0 * (1.0 - CHI)

# -------- measurement inputs (external, not catalog fit) --------
H0 = 68.76
T_CMB = 2.7255
N_EFF = 3.046

# -------- radiation --------
OMEGA_GAMMA_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4
REL_FACTOR = 1.0 + (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * N_EFF

h = H0 / 100.0
wm = OMEGA_M * h * h
wb = OMEGA_B * h * h
wr = OMEGA_GAMMA_H2 * REL_FACTOR
OMEGA_R = wr / (h * h)
OMEGA_DE = 1.0 - OMEGA_M - OMEGA_R

print("=" * 74)
print("Substrate inputs (sealed)")
print("=" * 74)
print(f"  A_0      = 1/(12*pi)        = {A_0:.8f}")
print(f"  Omega_m  = 1/pi             = {OMEGA_M:.6f}")
print(f"  chi      = 2/(9*pi)         = {CHI:.6f}")
print(f"  Omega_b  = 2*A_0*(1-chi)    = {OMEGA_B:.6f}")
print(f"  H_0      = {H0}")
print(f"  T_CMB    = {T_CMB}")
print(f"  N_eff    = {N_EFF}")
print()
print(f"  omega_m  = Omega_m * h^2    = {wm:.6f}")
print(f"  omega_b  = Omega_b * h^2    = {wb:.6f}")
print(f"  omega_gamma h^2             = {OMEGA_GAMMA_H2:.4e}")
print(f"  omega_r  (gamma + nu)       = {wr:.4e}")
print(f"  Omega_DE = 1 - Omega_m - Omega_r = {OMEGA_DE:.6f}")

# -------- z_eq --------
z_eq = wm / wr - 1.0

# -------- z_star (Hu-Sugiyama 1996) --------
g1 = 0.0783 * wb ** (-0.238) / (1.0 + 39.5 * wb ** 0.763)
g2 = 0.560 / (1.0 + 21.1 * wb ** 1.81)
z_star = 1048.0 * (1.0 + 0.00124 * wb ** (-0.738)) * (1.0 + g1 * wm ** g2)

# -------- z_drag (Eisenstein-Hu 1998) --------
b1 = 0.313 * wm ** (-0.419) * (1.0 + 0.607 * wm ** 0.674)
b2 = 0.238 * wm ** 0.223
z_drag = 1291.0 * wm ** 0.251 / (1.0 + 0.659 * wm ** 0.828) * (1.0 + b1 * wb ** b2)

# -------- cosmology functions --------
def E(z):
    return math.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_R * (1.0 + z) ** 4 + OMEGA_DE)

def cs_kms(z):
    # R = 3 rho_b / (4 rho_gamma), with rho_b ~ (1+z)^3, rho_gamma ~ (1+z)^4
    R = 0.75 * wb / OMEGA_GAMMA_H2 / (1.0 + z)
    return C_KMS / math.sqrt(3.0 * (1.0 + R))

def rs_integrand(z):
    return cs_kms(z) / (H0 * E(z))

rs_zstar, _ = quad(rs_integrand, z_star, np.inf, limit=400)
rs_zd, _    = quad(rs_integrand, z_drag, np.inf, limit=400)

def DM(z):
    val, _ = quad(lambda x: 1.0 / E(x), 0.0, z, limit=400)
    return C_KMS / H0 * val

DM_zstar = DM(z_star)

ell_A = PI * DM_zstar / rs_zstar
theta_star = rs_zstar / DM_zstar
hundred_theta_star = 100.0 * theta_star

# -------- report --------
print()
print("=" * 74)
print("SAM outputs vs Planck 2018 base-LCDM reference")
print("=" * 74)
ref = [
    ("z_eq",            z_eq,                3402.0),
    ("z_star",          z_star,              1089.92),
    ("z_drag",          z_drag,              1059.94),
    ("r_s(z_star) Mpc", rs_zstar,            144.43),
    ("r_d Mpc",         rs_zd,               147.09),
    ("D_M(z_star) Mpc", DM_zstar,            13869.6),
    ("ell_A",           ell_A,               301.76),
    ("100*theta_*",     hundred_theta_star,  1.04110),
]
print(f"{'observable':<18s} {'SAM':>14s}    {'Planck 2018':>14s}    {'dev':>10s}")
print("-" * 74)
for name, sam, planck in ref:
    dev = (sam - planck) / planck * 100.0
    print(f"{name:<18s} {sam:14.4f}    {planck:14.4f}    {dev:+9.3f}%")

print()
print("Layer 1 verdict question:")
print("  Does SAM land on the CMB acoustic geometry without fitting")
print("  Omega_m, Omega_b, or r_d?")
print()
print("  Substrate fits: 0   (Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi)")
print("                       are sealed identities, not parameters)")
