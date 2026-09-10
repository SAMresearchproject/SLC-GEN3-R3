# CR001c@19_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL Precommit

## Verdict Ladder (shown first per the precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold under canonical substrate inputs.

FAIL:
  At least one of P1, P2, P3 fails.

BOUNDARY:
  Reserved for cases where P1, P2, or P3 is marginally passing (within
  20% of its threshold) with an explicit scope caveat required. NOT used
  for schematic-BBN deviations, k_eq miss, or null-distribution
  percentiles.
```

Substrate inputs, measurement inputs, and gate thresholds are identical
to CR001@19 and CR001b@19. The ONLY changes are TWO arithmetic
corrections to the precommit text that surfaced during CR001b@19:

  Bug A (Peebles RHS Boltzmann factor): corrected from exp(-3.4 eV/kT)
        to exp(-13.6 eV/kT) in the effective ionization rate.
  Bug B (Thomson optical-depth integrand): corrected from 1/(a^2 * H)
        to 1/(a * H), with the same correction applied to the baryon-
        drag optical depth.

Both corrections are arithmetic; neither changes substrate identities,
gate thresholds, or the appeal discipline. CR001b@19 sealed FAIL with
Bug B honored per appeal-discipline; CR001c@19 corrects both bugs in
the precommit text and runner.

## Appeal Basis

```text
CR001@19 (sealed FAIL): Saha + buggy tau (1/(a^2*H))         -> theta_* +6.87%
CR001b@19 (sealed FAIL): Peebles + buggy tau (1/(a^2*H))     -> theta_* +142.25%

In CR001b@19's result.md, two arithmetic precommit bugs were named:
  Bug A: Peebles RHS missing the exp(-h*nu_alpha/(kT)) Lyman-alpha
         Boltzmann factor; the runner had to depart from precommit to
         get any recombination at all.
  Bug B: Thomson optical-depth integrand 1/(a^2 H) over-counted by a
         factor 1/a at small a, pushing the tau=1 surface to too-late
         times (smaller z_*).

CR001c@19 retests with both arithmetic corrections written into the
precommit text and consistently implemented in the runner. The Peebles
non-equilibrium effective-three-level atom (corrected RHS) is the
recombination model; the corrected tau integrand is the optical-depth
operator. Expected: theta_* and ell_A within 1-2% of Planck, r_d within
0.5-1% of Planck, all three gates pass at 5%.
```

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics using Peebles non-equilibrium
recombination (textbook-corrected Boltzmann factor) plus Thomson and
baryon-drag optical-depth integrals (textbook-corrected integrand
1/(a*H)), reproduce the Planck 2018 base-LCDM compressed CMB acoustic
geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 5% under canonical substrate inputs?
```

## Substrate Inputs (zero catalog fit; identical to CR001@19, CR001b@19)

```text
A_0       = 1/(12*pi)
alpha_H   = 2
D         = 3
R         = 2*alpha_H*D = 12
S         = 2^D = 8
Theta     = alpha_H*D^2 = 18

Omega_m   = R*A_0 = 1/pi              = 0.318310
chi       = (S/D)*A_0 = 2/(9*pi)      = 0.070736
Omega_b   = 2*A_0*(1-chi)             = 0.049299
Omega_c   = Omega_m - Omega_b         = 0.269011
```

## Measurement Inputs (external, not catalog fit; identical)

```text
H_0       = 68.76 km/s/Mpc        (BAO-side anchor; same as CR018b, CR019)
T_0       = 2.7255 K              (FIRAS)
N_eff     = 3.046                 (standard-model)
```

## Recombination Model (Bug A corrected)

```text
Peebles (1968) effective-three-level atom for hydrogen, integrated as
an ODE in dx_e/dz:

  dx_e/dz = (C(z) / (H(z) * (1+z))) * [
              alpha_B(T) * n_H(z) * x_e^2
            - beta_eff(T) * (1 - x_e)
          ]

with:
  n_H(z)     = Omega_b * rho_c,0 / (m_p * a^3)            (H-only treatment)
  T(z)       = T_0 * (1 + z)
  alpha_B(T) = 4.309e-19 * t^(-0.6166) / (1 + 0.6703 * t^(0.5300)) m^3/s
                with t = T / 10^4 K           (Pequignot-Petitjean fit)

  beta_eff(T) = alpha_B(T) * (m_e * k_B * T / (2*pi*hbar^2))^(3/2)
              * exp(-13.6 eV / (k_B*T))                        (Bug A FIX)

  The exponent is 13.6 eV, not the 3.4 eV in CR001b@19's precommit text.
  This combines beta_2's 3.4 eV with the Lyman-alpha photon energy
  10.2 eV. The equilibrium x_e of this RHS is the standard Saha-13.6
  equilibrium that real hydrogen recombination tracks at high T.

Peebles C-factor (unchanged from CR001b@19):
  C(z) = (1 + K(z) * Lambda_2gamma * n_H(z) * (1 - x_e))
       / (1 + K(z) * (Lambda_2gamma + beta_2(T)) * n_H(z) * (1 - x_e))

  K(z)            = lambda_alpha^3 / (8 * pi * H(z))     (Sobolev escape)
  lambda_alpha    = 1.215682e-7 m                         (Lyman-alpha)
  Lambda_2gamma   = 8.227 s^-1                            (two-photon decay)
  beta_2(T)       = alpha_B(T) * (m_e*k_B*T/(2*pi*hbar^2))^(3/2)
                                  * exp(-3.4 eV / (k_B*T))
                                  (raw n=2 photoionization, used inside C only)

Initial condition: x_e(Z_PEEBLES_START) = Saha-13.6 value at that z.
Integrate from z = 1800 down to z = 10 using scipy LSODA (auto-stiff).

For a-grid coverage:
  a < a(Z_PEEBLES_START) (z > 1800): x_e = 1.0 (Saha equilibrium)
  a within Peebles range: x_e from solve
  a > a(Z_PEEBLES_END) (z < 10):   x_e frozen at Peebles end value

Free-electron density:
  n_e(a) = x_e(a) * n_b(a)         (all baryons treated as hydrogen)
```

## Optical-Depth Operator (Bug B corrected)

```text
Thomson optical depth:
  tau(a) = integral from a to 1 of n_e(a') * sigma_T * c / (a' * H(a')) da'
                                                       ^^^^^^^^^^^^^^^
                                                       Bug B FIX: single
                                                       power of a, not a^2

Derivation:
  tau = integral of n_e * sigma_T * c dt' (proper time)
  dt = da / (a * H)
  tau(a) = integral from a to 1 of n_e * sigma_T * c / (a * H) da'

Last scattering:
  a_*  found by:  tau(a_*) = 1
  z_*  = 1/a_* - 1

Baryon-drag optical depth (same correction):
  tau_d(a) = integral from a to 1 of n_e(a') * sigma_T * c
                                     / (a' * H(a') * R_b(a')) da'

Drag epoch:
  a_d found by:  tau_d(a_d) = 1
  z_d = 1/a_d - 1

Sound horizon and comoving distance integrals are unchanged (these use
1/(a^2 * H) correctly because they are comoving-distance integrals over
conformal time, dη = dt/a):
  c_s(a)      = c / sqrt(3 * (1 + R_b(a)))
  R_b(a)      = (3/4) * (Omega_b/Omega_gamma) * a
  r_s(a_*)    = integral from 0 to a_* of c_s(a) / (a^2 * H(a)) da
  D_M(a_*)    = c * integral from a_* to 1 of da / (a^2 * H(a))

Acoustic geometry:
  theta_*       = r_s(a_*) / D_M(a_*)
  100 * theta_* = 100 * theta_*
  ell_A         = pi / theta_*
  r_d           = r_s(a_d)
```

## P1, P2, P3 (load-bearing; identical to CR001@19 and CR001b@19)

```text
P1: | 100*theta_*^SAM - 1.04110 | / 1.04110 <= 0.05
P2: | ell_A^SAM      - 301.76  | / 301.76  <= 0.05
P3: | r_d^SAM        - 147.09  | / 147.09  <= 0.05

Falsifier: deviation > 5%.
```

## Reported Evidence (not gates; same set as CR001@19, CR001b@19)

```text
E1-E6: z_eq, z_* (DERIVED Peebles), z_d (DERIVED Peebles),
       r_s(z_*), D_M(z_*), k_eq
E7-E12: eta_10, T_f, (n/p)_freeze, (n/p)_BBN, Y_p (schematic), D/H scaled
```

## Wrong Controls (REPORTED null distributions; same as prior CRs)

```text
WC1: Random Omega_m in [0.05, 0.95] over 1000 seeded trials (seeds 0..999).
WC2: Random (Omega_m, Omega_b) joint over 1000 seeded trials
     (seeds 10000..10999).

Statistic: |100*theta_*^random - 1.04110| / 1.04110.
Extreme direction: smaller is better (closer to Planck).
p-value: (n_extreme + 1) / (n_trials + 1) one-sided exact permutation.
```

## Implementation Discipline

```text
Peebles ODE integrated with scipy.integrate.solve_ivp method='LSODA'
(auto-stiff). Saha-13.6 initial condition at Z_PEEBLES_START = 1800.
Integration from z=1800 down to z=10 with t_eval on a 400-point
geomspace grid. rtol=1e-6, atol=1e-10.

x_e(a) on optical-depth grid (logspace(-7, 0, 4000)):
  - a < 1/(1800+1) (z > 1800):  x_e = 1.0
  - 1/1801 <= a <= 1/11 (10 <= z <= 1800): x_e from Peebles solve
  - a > 1/11 (z < 10):           x_e frozen at z=10 value

Thomson optical depth: cumulative_trapezoid of
  n_e * sigma_T * c / (a * H)  on the a-grid (Bug B corrected).

Drag optical depth: cumulative_trapezoid of
  n_e * sigma_T * c / (a * H * R_b)  (Bug B corrected).

Root-finding for a_*, a_d: log-a linear interpolation at tau = 1
crossing.

Sound horizon integration: cumulative_trapezoid of c_s/(a^2*H) on
a-grid. Comoving distance integration: cumulative_trapezoid of
1/(a^2*H) on a-grid. These remain 1/(a^2*H) (correct comoving-distance
operator).

Seed discipline:
  WC1 seeds 0..999      (numpy default_rng)
  WC2 seeds 10000..10999
```

## Frozen Sources

```text
External (Planck 2018 base-LCDM): reference values inline in runner
                                    (identical to CR001@19, CR001b@19).
BBN observational reference:        inline in runner (identical).

Branch-local cross-checks (sealed):
  C:\VS\The_Courtroom\19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN\CR001_summary.json
  C:\VS\The_Courtroom\19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL\CR001b_summary.json
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST\CR019_summary.json
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL\CR018b_summary.json

Substrate (read-only): manuscript Section 4 derived native quantities.
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine,
with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and z_* / z_d
derived from Peebles non-equilibrium recombination (with textbook-
corrected Boltzmann exponent 13.6 eV) plus Thomson and baryon-drag
optical-depth integrals (with textbook-corrected integrand 1/(a*H)),
reproduces the Planck 2018 base-LCDM compressed CMB acoustic geometry
to within 5% on 100*theta_*, ell_A, and r_d.

It could fail if any of the three observables deviated from Planck by
more than 5%. CR001@19 (Saha + Bug B) and CR001b@19 (Peebles + Bug B)
both failed; CR001c@19 isolates whether the substrate spine PASSes
once the two arithmetic precommit bugs are corrected.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM
compressed CMB acoustic geometry to within 5% on all three load-bearing
observables when the recombination redshift z_* and drag epoch z_d are
derived from textbook-standard Peebles non-equilibrium plasma physics
(two-photon decay + Sobolev escape, with correct Boltzmann exponent)
plus textbook-standard optical-depth operators (single power of a in
the integrand). Substrate identities Omega_m = 1/pi and Omega_b =
2*A_0*(1-chi) are sealed; H_0 = 68.76 (BAO-side anchor) and T_CMB =
2.7255 (FIRAS) are external measurement inputs. Zero catalog parameters
fit.

The CR001@19 and CR001b@19 FAILs were attributable to arithmetic
precommit bugs (Boltzmann exponent and tau integrand) rather than to
the substrate identities; once both bugs are corrected, the substrate
inventory passes the compressed CMB acoustic geometry test at the same
5% threshold under derived-from-first-principles plasma physics.
```

## Connection to CR001@19 and CR001b@19

```text
CR001@19 verdict:  FAIL (sealed). Saha + Bug B tau. theta_* +6.87%.
CR001b@19 verdict: FAIL (sealed). Peebles + Bug B tau. theta_* +142.25%.
  CR001b@19 also caught Bug A (Peebles RHS Boltzmann factor); runner
  departed from precommit on Bug A; precommit text uncorrected.

CR001c@19 supersedes CR001b@19 (and CR001@19 for the substrate-pass
question) with both bugs corrected in the precommit text and runner.
Substrate identities, measurement inputs, gate thresholds, evidence
set, and wrong-control structure are unchanged.

The CR001 and CR001b folders remain in the audit trail per branch
discipline.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
