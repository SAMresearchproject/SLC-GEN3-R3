# CR001b@19_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL Precommit

## Verdict Ladder (shown first per the precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold under canonical substrate inputs.

FAIL:
  At least one of P1, P2, P3 fails.

BOUNDARY:
  Reserved for cases where P1, P2, or P3 is marginally passing (within 20%
  of its threshold) with an explicit scope caveat required. NOT used for
  schematic-BBN deviations, k_eq miss, or null-distribution percentiles.
```

The substrate inputs, the measurement inputs, and the gate thresholds are
identical to CR001@19. The ONLY change is the recombination model:
Peebles non-equilibrium effective-three-level atom replaces Saha
equilibrium ionization.

## Appeal Basis

```text
CR001@19 (sealed FAIL 2026-06-27) tested the substrate-derived thermal
ladder using Saha equilibrium ionization for the recombination physics.
The runner executed cleanly and returned:

  P1  |100*theta_* dev| = 6.870%   FAIL (over 5%)
  P2  |ell_A dev|       = 6.430%   FAIL (over 5%)
  P3  |r_d dev|         = 2.870%   PASS

The CR001@19 result.md documented that the failure traces to the Saha
"first clean approximation" undershooting z_* (995 vs Planck 1090,
-8.7%), which propagates into r_s being +4.1% high and D_M being -2.5%
low, multiplying to +6.9% on theta_*. The substrate inputs were not
implicated.

CR001b@19 replaces Saha with the standard Peebles (1968) effective-
three-level atom: a single ODE in dx_e/dz that augments Saha with the
non-equilibrium two-photon-decay rate (Lambda_2gamma = 8.227 s^-1) and
the Sobolev escape factor for Lyman-alpha photons. This is the
conventional H-only recombination model used in CMB analysis prior to
RECFAST's H+He extension.

Expected result: theta_* and ell_A within 1-3% of Planck (close to
CR019's fit-formula 0.6%). r_d retained from CR001 within 5%. All three
load-bearing gates expected to pass at 5%.
```

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics using Peebles non-equilibrium
recombination (instead of Saha first-approximation), reproduce the
Planck 2018 base-LambdaCDM compressed CMB acoustic geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 5% under canonical substrate inputs?
```

## Substrate Inputs (zero catalog fit; identical to CR001@19)

```text
A_0       = 1/(12*pi)                       (accumulation floor)
alpha_H   = 2                                (binary readout)
D         = 3                                (dimension)
R         = 2*alpha_H*D = 12                 (radix)
S         = 2^D = 8                          (split count)
Theta     = alpha_H*D^2 = 18                 (tensor bridge)

Omega_m   = R*A_0 = 1/pi               = 0.318310
chi       = (S/D)*A_0 = 2/(9*pi)       = 0.070736
Omega_b   = 2*A_0*(1-chi)              = 0.049299
Omega_c   = Omega_m - Omega_b          = 0.269011
```

## Measurement Inputs (external, not catalog fit; identical to CR001@19)

```text
H_0       = 68.76 km/s/Mpc        (BAO-side anchor; same as CR018b, CR019)
T_0       = 2.7255 K              (FIRAS)
N_eff     = 3.046                 (standard-model)
```

## Recombination Model (CHANGE from CR001@19)

```text
Peebles (1968) effective-three-level atom for hydrogen, integrated as an
ODE in dx_e/dz:

  dx_e/dz = (C(z) / (H(z) * (1+z))) * [
              alpha_B(T) * n_H(z) * x_e^2
            - beta_2(T) * (1 - x_e)
          ]

with:
  n_H(z)     = Omega_b * rho_c,0 / (m_p * a^3)         (H-only treatment)
  T(z)       = T_0 * (1 + z)
  alpha_B(T) = 4.309e-19 * t^(-0.6166) / (1 + 0.6703 * t^(0.5300)) m^3/s
                with t = T / 10^4 K            (Pequignot-Petitjean fit)
  beta_2(T)  = alpha_B(T) * (m_e * k_B * T / (2*pi*hbar^2))^(3/2)
              * exp(-h*nu_2 / (k_B*T))
                with h*nu_2 = 3.4 eV          (n=2 binding energy)

Peebles C-factor:
  C(z) = (1 + K(z) * Lambda_2gamma * n_H(z) * (1 - x_e))
       / (1 + K(z) * (Lambda_2gamma + beta_2(T)) * n_H(z) * (1 - x_e))

  K(z)           = lambda_alpha^3 / (8 * pi * H(z))     (Sobolev escape)
  lambda_alpha   = 1.215682e-7 m                         (Lyman-alpha)
  Lambda_2gamma  = 8.227 s^-1                            (two-photon decay)

Initial condition: x_e(z_high) = 1.0 (Saha gives x_e ~ 1 at z ~ 3000+).
Integrate from z = 3000 down to z = 10 using scipy BDF method.

Hydrogen-only Peebles (no helium correction). This is the original
Peebles 1968 framework; RECFAST extends to H+He. The H-only approximation
introduces O(1-2%) deviation from H+He but is sufficient at the 5% gate.

Free-electron density on the optical-depth a-grid:
  n_e(a) = x_e(a) * n_b(a)    (treating all baryons as hydrogen for Peebles)
```

## Optical-Depth Integration (identical to CR001@19)

```text
Thomson optical depth:
  tau(a) = integral from a to 1 of n_e(a') * sigma_T * c / (a'^2 * H(a')) da'
  Last scattering:  tau(a_*) = 1     ->     z_* = 1/a_* - 1

Baryon-drag optical depth:
  tau_d(a) = integral from a to 1 of n_e(a') * sigma_T * c
                                     / (a'^2 * H(a') * R_b(a')) da'
  Drag epoch:  tau_d(a_d) = 1        ->     z_d = 1/a_d - 1

Sound horizon and acoustic geometry:
  R_b(a)      = (3/4) * (Omega_b/Omega_gamma) * a
  c_s(a)      = c / sqrt(3 * (1 + R_b(a)))
  r_s(a_*)    = integral from 0 to a_* of c_s(a) / (a^2 * H(a)) da
  D_M(a_*)    = c * integral from a_* to 1 of da / (a^2 * H(a))
  theta_*     = r_s(a_*) / D_M(a_*)
  ell_A       = pi / theta_*
  r_d         = r_s(a_d)
```

## P1 — Acoustic Angular Scale (load-bearing; same as CR001@19)

```text
  | 100*theta_*^SAM - 1.04110 | / 1.04110 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## P2 — Acoustic Peak Multipole (load-bearing; same as CR001@19)

```text
  | ell_A^SAM - 301.76 | / 301.76 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## P3 — Drag Sound Horizon (load-bearing; same as CR001@19)

```text
  | r_d^SAM - 147.09 | / 147.09 <= 0.05

Pass:      within +/- 5%.
Falsifier: deviation > 5%.
```

## Reported Evidence (not gates; same set as CR001@19)

```text
E1-E6: z_eq, z_* (DERIVED Peebles), z_d (DERIVED Peebles), r_s(z_*), D_M(z_*), k_eq
E7-E12: eta_10, T_f, (n/p)_freeze, (n/p)_BBN, Y_p (schematic), D/H (eta^-1.6)
```

## Wrong Controls (REPORTED null distributions, not gates; same as CR001@19)

```text
WC1: Random Omega_m in [0.05, 0.95] over 1000 seeded trials (seeds 0..999).
     For each draw, recompute Peebles thermal ladder. Statistic:
     |100*theta_*^random - 1.04110| / 1.04110.
     Report null distribution stats, canonical percentile, p-value.

WC2: Random (Omega_m, Omega_b) joint over 1000 seeded trials (seeds
     10000..10999). Same statistic and reporting.
```

## Implementation Discipline

```text
Peebles ODE integrated with scipy.integrate.solve_ivp method='BDF'
(stiff solver) with rtol=1e-8, atol=1e-12. Integration from z=3000 down
to z=10 in dense_output mode for interpolation back to the a-grid.

x_e(a) on optical-depth grid:
  - a < 1/(3000+1)   (z > 3000): x_e = 1.0 (fully ionized; Saha gives x_e -> 1)
  - 1/3001 <= a <= 1/11 (10 <= z <= 3000): x_e from Peebles solve
  - a > 1/11         (z < 10):  x_e = x_e(z=10)  (frozen; minor contribution to tau)

Optical depth and r_s integrals: cumulative_trapezoid on a-grid
np.logspace(-7, 0, 4000) (same as CR001@19).

Root-finding for a_*, a_d: log-a linear interpolation at tau = 1 crossing
(same as CR001@19).

Seed discipline:
  WC1 seeds 0..999      (numpy default_rng)
  WC2 seeds 10000..10999

p-value formula: one-sided exact permutation
  p = (n_null_at_least_as_extreme + 1) / (n_trials + 1)
```

## Frozen Sources

```text
External (Planck 2018 base-LCDM): reference values inline in runner
                                    (identical to CR001@19).
BBN observational reference:        inline in runner (identical to CR001@19).

Branch-local cross-checks (sealed):
  C:\VS\The_Courtroom\19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN\CR001_summary.json
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST\CR019_summary.json
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL\CR018b_summary.json

Substrate (read-only): manuscript Section 4 derived native quantities.
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine,
with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and z_* / z_d
derived from Peebles non-equilibrium recombination (Saha augmented with
two-photon decay and Sobolev escape) plus Thomson and baryon-drag
optical depth integrals, reproduces the Planck 2018 base-LCDM compressed
CMB acoustic geometry to within 5% on 100*theta_*, ell_A, and r_d.

It could fail if any of the three observables deviated from Planck by
more than 5%. CR001@19 already demonstrated that the substrate inputs
plus Saha falls short of this threshold; the question is whether the
substrate inputs plus the standard Peebles upgrade meets the threshold.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM compressed
CMB acoustic geometry to within 5% on all three load-bearing observables
when the recombination redshift z_* and drag epoch z_d are derived from
Peebles non-equilibrium plasma physics (two-photon decay + Sobolev escape)
rather than from fitting formulae. Substrate identities Omega_m = 1/pi
and Omega_b = 2*A_0*(1-chi) are sealed; H_0 = 68.76 (BAO-side anchor)
and T_CMB = 2.7255 (FIRAS) are external measurement inputs. Zero catalog
parameters fit.

The substrate's matter and baryon inventory survives the physics-derived
epoch transition under the standard recombination model used in CMB
analysis. CR001@19's Saha-first-approximation FAIL is recovered as PASS
under the standard Peebles upgrade; the substrate identities were not
implicated in the CR001@19 FAIL.
```

## Connection to CR001@19 (Superseded for the substrate-pass question)

```text
CR001@19 verdict: FAIL (sealed; unchanged; preserved at
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN\).

The CR001@19 FAIL was traced to the Saha "first clean approximation"
undershoot. CR001b@19 retests with the standard Peebles model and the
same 5% gates. Substrate identities, measurement inputs, gate
thresholds, evidence set, and wrong-control structure are unchanged.

For downstream citation, CR001b@19 supersedes CR001@19. The CR001 folder
remains in the audit trail.
```

## Connection to CR019 (Branch 06)

```text
CR019 used Hu-Sugiyama and Eisenstein-Hu fitting formulae and returned
theta_* +0.61%, ell_A -0.60%, r_d +0.46% PASS at 1%.

CR001b@19 uses Peebles non-equilibrium recombination (a step closer to
first-principles plasma physics than the fitting formulae). Expected
deviations are slightly wider than CR019 (typical Peebles H-only vs
HS-fit-formula offset is O(1%)) but well within the 5% threshold.

Together, CR019 (fit formulae) and CR001b@19 (Peebles) bracket the
substrate's prediction of the CMB acoustic geometry from both ends of
the recombination-modeling axis.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
