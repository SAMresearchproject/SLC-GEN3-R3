# CR001@19_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN Precommit

## Verdict Ladder (shown first per the precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold under canonical substrate inputs.

FAIL:
  At least one of P1, P2, P3 fails.

BOUNDARY:
  Reserved for cases where P1, P2, or P3 is marginally passing (within 20%
  of its threshold) with an explicit scope caveat required. NOT used for
  schematic-BBN deviations, fitting-formula intermediates, or null-
  distribution percentiles.
```

P1, P2, and P3 are the load-bearing scientific claims. They are the three
acoustic-geometry observables that the CMB power spectrum directly measures
(100*theta_*, ell_A, r_d), evaluated with z_* and z_d DERIVED from plasma
physics (Saha ionization + Thomson optical depth for z_*; baryon-drag
optical depth for z_d). All other quantities computed by this runner
(z_eq, k_eq, derived z_*, derived z_d, r_s(z_*), D_M(z_*), schematic-BBN
T_f, (n/p)_freeze, (n/p)_BBN, Y_p, eta_10, D/H) are reported sensitivity
evidence and do not gate the verdict.

## Test Type

```text
Fresh Courtroom branch test in 19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER.
External anchor: Planck 2018 base-LambdaCDM (TT,TE,EE+lowE+lensing)
compressed CMB acoustic geometry.

Substrate inputs: Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi). Sealed
identities, not parameters; same identities used in CR018b (SN/BAO),
CR019 (compressed CMB via fit formulae), CR025 (halo profile), CR031b
(radial law), CR032 (per-galaxy halo mass).

Distinction from CR019: CR019 used Hu-Sugiyama (z_*) and Eisenstein-Hu
(z_drag) fitting formulae. CR001@19 DERIVES z_* and z_d from plasma
physics: Saha ionization + Thomson optical depth integral.
```

## Why This Test Matters

```text
CR019 showed the substrate spine reproduces the Planck compressed CMB
geometry to ~0.6% with fit-formula epochs. The harder test is whether the
same substrate inputs reproduce the geometry when z_* and z_d are derived
from plasma physics directly. The full ladder per the PDF:

  A_0, alpha_H, D
     -> Omega_m, Omega_b
     -> H(a), T(a)
     -> z_eq
     -> z_*       via Saha + tau_Thomson(a_*) = 1
     -> r_s(z_*), D_M(z_*), theta_*, ell_A
     -> z_d       via tau_drag(a_d) = 1
     -> r_d
     -> eta, Y_p, D/H (BBN, schematic)

Saha-only recombination is a "first clean approximation" per the PDF; it
differs from the true Peebles non-equilibrium recombination by ~few-percent
in the integrated geometric observables. CR001@19 PASS at 5% would
demonstrate that the substrate's matter and baryon inventory survives the
physics-derived epoch transition with no catalog fit and no fit-formula
crutch.

CR001@19 does NOT claim:
  - Full nucleosynthesis network match (PDF defers this to the "serious version")
  - Resolution of the H_0 tension
  - Fit to the full CMB power spectrum (compressed geometry only)
```

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics (Saha + Thomson optical depth
and baryon-drag optical depth respectively), reproduce the Planck 2018
base-LambdaCDM compressed CMB acoustic geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 5% under canonical substrate inputs?
```

## Substrate Inputs (zero catalog fit)

```text
Native ledger (manuscript Section 4):
  A_0      = 1/(12*pi)                       (accumulation floor)
  alpha_H  = 2                                (binary readout)
  D        = 3                                (dimension)
  R        = 2*alpha_H*D = 12                 (radix)
  S        = 2^D = 8                          (split count)
  Theta    = alpha_H*D^2 = 18                 (tensor bridge)

Derived densities (sealed identities):
  Omega_m  = R*A_0 = 1/pi              = 0.318310
  chi      = (S/D)*A_0 = (8/3)/(12*pi) = 2/(9*pi) = 0.070736
  Omega_b  = 2*A_0*(1-chi)             = 0.049299
  Omega_c  = Omega_m - Omega_b         = 0.269011
```

## Measurement Inputs (external, not catalog fit)

```text
H_0      = 68.76 km/s/Mpc         (BAO-side anchor; same as CR018b, CR019)
T_CMB    = T_0 = 2.7255 K         (FIRAS measurement)
N_eff    = 3.046                  (standard-model neutrino background)

Omega_gamma   from rho_gamma_0 = (pi^2/15)*(k_B*T_0)^4 / (hbar^3 * c^5)
                                  divided by c^2 to get mass density
                                  divided by rho_c,0 = 3*H_0^2/(8*pi*G_N)
Omega_r       = Omega_gamma * (1 + (7/8)*(4/11)^(4/3) * N_eff)
              = Omega_gamma * (1 + 0.2271 * N_eff)
Omega_Lambda  = 1 - Omega_m - Omega_r
```

## Thermal Clock

```text
a(z)   = 1/(1+z)
T(a)   = T_0/a                  (adiabatic photon cooling)
E(a)   = sqrt( Omega_r/a^4 + Omega_m/a^3 + Omega_Lambda )
H(a)   = H_0 * E(a)
```

## z_eq and k_eq (matter-radiation equality)

```text
a_eq = Omega_r / Omega_m
z_eq = 1/a_eq - 1
k_eq = a_eq * H(a_eq) / c
     = (H_0/c) * sqrt( 2*Omega_m / a_eq )    (per PDF section 3)
```

## Recombination DERIVED (Saha + optical depth)

```text
Baryon number density:
  n_b(a) = Omega_b * rho_c,0 / (m_p * a^3)

Hydrogen Saha ionization fraction (single-fluid, hydrogen-dominated):
  x_e^2 / (1 - x_e) = (1/n_b) * (m_e * k_B * T / (2*pi*hbar^2))^(3/2)
                       * exp( -E_ion / (k_B * T) )
                                       with E_ion = 13.6 eV, T = T_0/a

Free-electron density:
  n_e(a) = x_e(a) * n_b(a)

Thomson optical depth integral:
  tau(a) = integral from a to 1 of  n_e(a') * sigma_T * c / (a'^2 * H(a'))  da'

Last scattering surface:
  a_*  found by:  tau(a_*) = 1
  z_*  = 1/a_*  -  1

Planck 2018 reference:  z_*  = 1089.92
```

## Sound Horizon and Acoustic Angle

```text
Baryon-photon momentum ratio:
  R_b(a) = (3/4) * (Omega_b/Omega_gamma) * a

Sound speed:
  c_s(a) = c / sqrt(3 * (1 + R_b(a)))

Sound horizon at last scattering:
  r_s(a_*) = integral from 0 to a_* of  c_s(a) / (a^2 * H(a))  da

Comoving distance to last scattering:
  D_M(a_*) = c * integral from a_* to 1 of  da / (a^2 * H(a))

Acoustic angle and peak multipole:
  theta_*       = r_s(a_*) / D_M(a_*)
  100 * theta_* = 100 * theta_*
  ell_A         = pi / theta_*
```

## Drag Epoch DERIVED (baryon-drag optical depth)

```text
tau_d(a) = integral from a to 1 of  n_e(a') * sigma_T * c
                                    / (a'^2 * H(a') * R_b(a'))  da'

Drag epoch:
  a_d found by:  tau_d(a_d) = 1
  z_d = 1/a_d - 1

Sound horizon at drag:
  r_d = r_s(a_d) = integral from 0 to a_d of  c_s(a) / (a^2 * H(a))  da

Planck 2018 reference:  r_d = 147.09 Mpc
```

## P1 — Acoustic Angular Scale (load-bearing)

```text
SAM-predicted 100*theta_*(canonical), with DERIVED z_*, reproduces Planck
2018 base-LCDM acoustic angular scale 1.04110 to within 5%:

  | 100*theta_*^SAM - 1.04110 | / 1.04110 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## P2 — Acoustic Peak Multipole (load-bearing)

```text
SAM-predicted ell_A(canonical), with DERIVED z_*, reproduces Planck 2018
base-LCDM acoustic peak multipole 301.76 to within 5%:

  | ell_A^SAM - 301.76 | / 301.76 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## P3 — Drag Sound Horizon (load-bearing)

```text
SAM-predicted r_d(canonical), with DERIVED z_d, reproduces Planck 2018
base-LCDM drag sound horizon 147.09 Mpc to within 5%:

  | r_d^SAM - 147.09 | / 147.09 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## Reported Evidence (not gates)

```text
E1: z_eq                  (SAM vs Planck 2018 reference 3402)
E2: z_*    DERIVED        (SAM Saha-tau vs Planck 2018 reference 1089.92)
E3: z_d    DERIVED        (SAM tau-drag vs Planck 2018 reference 1059.94)
E4: r_s(z_*) Mpc          (SAM vs Planck 2018 reference 144.43)
E5: D_M(z_*) Mpc          (SAM vs Planck 2018 reference 13869.6)
E6: k_eq 1/Mpc            (matter-radiation equality horizon turnover)

BBN evidence (schematic Wagoner two-state freeze-out, per PDF section 7;
the PDF acknowledges that a full nucleosynthesis network is the proper
"serious version" of this test):
E7: eta_10                          (baryon-to-photon ratio; from substrate identity)
E8: T_f      MeV                    (weak freeze-out temperature)
E9: (n/p)_f                         (frozen neutron-to-proton ratio)
E10: (n/p)_BBN                      (after neutron decay through Delta-t)
E11: Y_p     schematic              (primordial helium mass fraction; expected ~0.33)
E12: D/H     schematic              (deuterium abundance from eta^-1.6 scaling)
```

## Wrong Controls (REPORTED null distributions, not gates)

```text
Per the wrong-control-methodology lesson, null distributions are reported
as percentile-against-null with one-sided exact permutation p-value. They
support the headline but do not gate the verdict.

WC1: Random Omega_m in [0.05, 0.95] over 1000 seeded trials (seeds 0..999).
     For each draw, recompute the full thermal ladder and the geometric
     observables. Statistic: |100*theta_*^random - 1.04110| / 1.04110.
     Report null distribution stats, canonical percentile, p-value.

WC2: Random (Omega_m, Omega_b) joint draws over 1000 seeded trials
     (seeds 10000..10999). Omega_m ~ uniform[0.05, 0.95];
     Omega_b ~ uniform[0.005, 0.15]. Same statistic.
     Report null distribution stats, canonical percentile, p-value.
```

## Implementation Discipline

```text
Saha equation solved per-a as quadratic:
  x_e^2 + S*x_e - S = 0
  x_e = ( -S + sqrt(S^2 + 4*S) ) / 2

Optical depth integration via scipy.integrate.quad with limit=400.
Root-finding for a_* and a_d via scipy.optimize.brentq.

R_b uses Omega_gamma derived from FIRAS T_0 = 2.7255 (not Omega_r).

Sound horizon r_s(a_*) and r_s(a_d) computed as separate integrals
from a=0 to the respective limit; the inner integrand uses the
substrate-derived Omega_r in H(a).

Schematic BBN uses:
  Gamma_weak(T) = (7*pi/60) * (1 + 3*g_A^2) * G_F^2 * T^5
                  with g_A = 1.27 (axial coupling)
  H(T)          = 1.66 * sqrt(g_*) * T^2 / M_Pl
                  with g_* = 10.75 at T ~ 1 MeV
  T_BBN         = 0.073 MeV (deuterium bottleneck reference temperature)

Seed discipline:
  WC1 seeds 0..999      (numpy default_rng)
  WC2 seeds 10000..10999

p-value formula: one-sided exact permutation
  p = (n_null_at_least_as_extreme + 1) / (n_trials + 1)

Extreme direction: |100*theta_*^random - 1.04110| <= canonical
  (random draws produce theta_* at least as close to Planck as canonical)
```

## Frozen Sources

```text
External (Planck 2018 base-LCDM):
  Reference values quoted directly in this precommit. No catalog data file
  is read by the runner. Planck reference values are hard-coded constants
  matched against runtime SAM outputs.

BBN observational reference:
  Y_p   ~ 0.245   (Aver et al 2015; Planck BBN consistency)
  D/H   ~ 2.527e-5 (Cooke et al 2018)
  eta_10 ~ 6.10   (Planck CMB-inferred)

Branch-local cross-checks (sealed):
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL\CR018b_summary.json
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST\CR019_summary.json

Substrate (read-only):
  manuscript Section 4 derived native quantities (A_0, R, Theta, Omega_m, Omega_b)
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine,
with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and z_* / z_d
DERIVED from Saha ionization plus Thomson and baryon-drag optical depth
integrals (i.e. zero catalog fit AND zero fit-formula crutch), reproduces
the Planck 2018 base-LambdaCDM compressed CMB acoustic geometry to within
5% on 100*theta_*, ell_A, and r_d.

It could have failed if any of the three acoustic-geometry observables
deviated from the Planck reference by more than 5%, i.e.:
  - 100*theta_* outside [0.989, 1.093]
  - ell_A outside [286.7, 316.8]
  - r_d outside [139.7, 154.4] Mpc
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM compressed
CMB acoustic geometry to within 5% on all three load-bearing observables
when the recombination redshift z_* and drag epoch z_d are derived from
plasma physics (Saha + Thomson and baryon-drag optical depth) rather than
from fitting formulae. Substrate identities Omega_m = 1/pi and Omega_b =
2*A_0*(1-chi) are sealed from the native ledger. External measurement
inputs are H_0 = 68.76 (BAO-side anchor), T_CMB = 2.7255 (FIRAS), and
N_eff = 3.046 (standard-model). Zero catalog parameters fit.

The substrate's matter and baryon inventory survives the physics-derived
epoch transition, confirming the substrate-only thermal ladder from A_0,
alpha_H, D down to the CMB acoustic geometry.
```

## Connection to CR019 (Branch 06)

```text
CR019 (sealed PASS 2026-06-27) tested the same compressed CMB acoustic
geometry using Hu-Sugiyama (z_*) and Eisenstein-Hu (z_drag) fitting
formulae. It returned:
  100*theta_*  +0.605% deviation from Planck
  ell_A        -0.602%
  r_d          +0.461%

CR001@19 is a strictly harder version: same substrate, same measurement
inputs, but z_* and z_d derived from plasma physics. CR001@19 expected
deviations are wider than CR019 (Saha is a first-clean-approximation;
real recombination involves Peebles non-equilibrium two-photon decay)
but should remain within 5% to confirm the substrate inventory.
```

## Connection to CR018b (Branch 06)

```text
CR018b's r_d = 147.769 Mpc at H_0 = 68.76 is computed using Eisenstein-Hu
fit formula for z_drag. CR001@19's r_d (DERIVED via tau_drag) is
expected to deviate from CR018b's r_d by a few percent because the drag
epoch is now derived from physics. Both should land within 5% of
Planck's r_d = 147.09 Mpc.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
