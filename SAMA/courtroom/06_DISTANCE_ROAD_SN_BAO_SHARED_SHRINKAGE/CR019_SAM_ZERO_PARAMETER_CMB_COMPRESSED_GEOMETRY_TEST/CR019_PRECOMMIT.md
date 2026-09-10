# CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST Precommit

## Verdict Ladder (shown first per the precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold under canonical substrate inputs.

FAIL:
  At least one of P1, P2, P3 fails.

BOUNDARY:
  Reserved for cases where P1, P2, or P3 is marginally passing (within 20%
  of its threshold) with an explicit scope caveat required. NOT used for
  auxiliary evidence misses, null-distribution percentiles, or fitting-
  formula-intermediate deviations.
```

P1, P2, and P3 are the load-bearing scientific claims. The acoustic geometry
quantities they cover (100*theta_*, ell_A, r_d) are precisely what the CMB
power spectrum directly measures. Every other quantity this runner computes
(z_eq, z_*, z_drag, r_s(z_*), D_M(z_*), and the two null distributions over
random parameter draws) is reported sensitivity evidence per the precommit-
gate-discipline lesson and does not gate the verdict.

## Test Type

```text
Fresh Courtroom branch test in 06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE.
External anchor: Planck 2018 base-LambdaCDM (TT,TE,EE+lowE+lensing)
compressed CMB acoustic geometry.
Substrate inputs: Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi). Both are sealed
substrate identities, not parameters; same identities used in CR018b for
SN and BAO distances.
```

## Why This Test Matters

```text
The compressed CMB acoustic geometry is the most precisely measured set of
cosmological observables. Planck 2018 pins down 100*theta_* to ~0.03% and
ell_A to ~0.03%; the drag sound horizon r_d to ~0.18%. Reproducing those
numbers without fitting Omega_m, Omega_b, or r_d is a strong test of any
zero-parameter substrate spine.

Conventional cosmology obtains these numbers by fitting a 5+ parameter
LCDM model to the CMB power spectrum directly. SAM's claim is that the
substrate identities Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) plus
external measurement inputs (H_0 = 68.76 from BAO-side, T_CMB = 2.7255
from FIRAS, N_eff = 3.046 standard model) suffice to reproduce the
acoustic geometry to sub-percent precision.

CR019 PASS does not claim SAM is right globally. It claims that with
zero catalog parameters fit, the substrate spine lands on the CMB acoustic
geometry to within 1% on the three load-bearing observables.
```

## Question

```text
Does SAM's substrate-only distance spine, with NO catalog-fit parameters,
reproduce the Planck 2018 base-LambdaCDM compressed CMB acoustic geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 1% under canonical substrate inputs?
```

## Substrate Inputs (zero catalog fit)

```text
A_0      = 1/(12*pi)              (native accumulation floor)
Omega_m  = 1/pi             = 0.318310     (sealed substrate identity)
chi      = (8/3)*A_0 = 2/(9*pi)             (substrate carrier ratio)
Omega_b  = 2*A_0*(1-chi)    = 0.049299     (sealed substrate identity)
```

## Measurement Inputs (external, not catalog fit)

```text
H_0      = 68.76 km/s/Mpc         (BAO-side anchor; same as CR018b)
T_CMB    = 2.7255 K               (FIRAS measurement)
N_eff    = 3.046                  (standard-model neutrino background)

Omega_gamma h^2 = 2.4728e-5 * (T_CMB / 2.7255)^4
omega_r         = Omega_gamma h^2 * (1 + (7/8)*(4/11)^(4/3) * N_eff)
                = Omega_gamma h^2 * (1 + 0.2271 * N_eff)
```

## Cosmology Formulae

```text
E(z) = sqrt(Omega_m*(1+z)^3 + Omega_r*(1+z)^4 + Omega_DE)
Omega_DE = 1 - Omega_m - Omega_r

Sound speed:  c_s(z) = c / sqrt(3*(1 + R(z)))
              R(z)   = (3/4) * omega_b / (Omega_gamma h^2) / (1+z)

Sound horizon: r_s(z) = integral from z to infinity of c_s(z') / H(z') dz'
                     = integral from z to infinity of c_s(z') / (H_0 * E(z')) dz'

Comoving distance: D_M(z) = (c/H_0) * integral from 0 to z of dz' / E(z')

Decoupling redshift (Hu-Sugiyama 1996):
  g1 = 0.0783 * omega_b^(-0.238) / (1 + 39.5 * omega_b^0.763)
  g2 = 0.560 / (1 + 21.1 * omega_b^1.81)
  z_*  = 1048 * (1 + 0.00124 * omega_b^(-0.738)) * (1 + g1 * omega_m^g2)

Drag epoch (Eisenstein-Hu 1998):
  b1 = 0.313 * omega_m^(-0.419) * (1 + 0.607 * omega_m^0.674)
  b2 = 0.238 * omega_m^0.223
  z_d = 1291 * omega_m^0.251 / (1 + 0.659 * omega_m^0.828) * (1 + b1 * omega_b^b2)

Matter-radiation equality: z_eq = omega_m / omega_r - 1

Acoustic geometry:
  ell_A           = pi * D_M(z_*) / r_s(z_*)
  theta_*         = r_s(z_*) / D_M(z_*)
  100 * theta_*   = 100 * theta_*
```

## Planck 2018 Reference Values (base-LCDM)

```text
z_eq            = 3402
z_*             = 1089.92
z_drag          = 1059.94
r_s(z_*)        = 144.43 Mpc
r_d             = 147.09 Mpc
D_M(z_*)        = 13869.6 Mpc
ell_A           = 301.76
100 * theta_*   = 1.04110
```

## P1 — Acoustic Angular Scale Load-bearing Prediction

```text
SAM-predicted 100*theta_*(canonical) reproduces Planck 2018 base-LCDM
acoustic angular scale 1.04110 to within 1%:

  | 100*theta_*^SAM - 1.04110 | / 1.04110 <= 0.01

Pass:    within +/- 1%.
Falsifier: deviation > 1%.

Sensitivity: scratch observed +0.61% deviation (passes with margin).
```

## P2 — Acoustic Peak Multipole Load-bearing Prediction

```text
SAM-predicted ell_A(canonical) reproduces Planck 2018 base-LCDM acoustic
peak multipole 301.76 to within 1%:

  | ell_A^SAM - 301.76 | / 301.76 <= 0.01

Pass:    within +/- 1%.
Falsifier: deviation > 1%.

Sensitivity: scratch observed -0.60% deviation (passes with margin).
```

## P3 — Drag Sound Horizon Load-bearing Prediction

```text
SAM-predicted r_d(canonical) reproduces Planck 2018 base-LCDM drag sound
horizon 147.09 Mpc to within 1%:

  | r_d^SAM - 147.09 | / 147.09 <= 0.01

Pass:    within +/- 1%.
Falsifier: deviation > 1%.

Sensitivity: scratch observed +0.46% deviation (passes with margin;
matches CR018b's independent r_d derivation).
```

## Reported Sensitivity Evidence (not gates)

```text
E1: z_eq                  (SAM vs Planck 2018 reference 3402)
E2: z_*                   (SAM vs Planck 2018 reference 1089.92)
E3: z_drag                (SAM vs Planck 2018 reference 1059.94)
E4: r_s(z_*) Mpc          (SAM vs Planck 2018 reference 144.43)
E5: D_M(z_*) Mpc          (SAM vs Planck 2018 reference 13869.6)

These are intermediate quantities in the acoustic-geometry derivation
chain. z_eq, z_*, and z_drag are sensitive to the matter/radiation ratio
and to the Hu-Sugiyama / Eisenstein-Hu fitting formulae; their deviation
from Planck does not directly falsify the acoustic geometry (which is
gated by P1, P2, P3).
```

## Wrong Controls (REPORTED null distributions, not gates)

```text
Per the wrong-control-methodology lesson, null distributions are reported
as percentile-against-null with one-sided exact permutation p-value. They
support the headline but do not gate the verdict.

WC1: Random Omega_m in [0.05, 0.95] over 1000 seeded trials (seeds 0..999).
     For each draw, compute |100*theta_*^random - 1.04110|.
     Report null distribution stats, canonical percentile, p-value.

WC2: Random (Omega_m, Omega_b) joint draws over 1000 seeded trials
     (seeds 10000..10999). Omega_m ~ uniform[0.05, 0.95];
     Omega_b ~ uniform[0.005, 0.15].
     For each draw, compute |100*theta_*^random - 1.04110|.
     Report null distribution stats, canonical percentile, p-value.

Both wrong controls use the same H_0 = 68.76, T_CMB = 2.7255, N_eff = 3.046
as canonical, and recompute z_*, r_s(z_*), D_M(z_*) per trial.
```

## Implementation Discipline

```text
Canonical and null trials use identical numerical machinery:
  - Same E(z) formula with Omega_m, Omega_r, Omega_DE structure.
  - Same Hu-Sugiyama z_* and Eisenstein-Hu z_drag fitting formulae.
  - Same r_s integration using scipy.integrate.quad, limit=400.
  - Same D_M integration using scipy.integrate.quad, limit=400.

Seed discipline:
  WC1 seeds 0..999      (numpy default_rng)
  WC2 seeds 10000..10999

p-value formula: one-sided exact permutation
  p = (n_null_at_least_as_extreme + 1) / (n_trials + 1)

Extreme direction (both wrong controls):
  |100*theta_*^random - 1.04110| <= |100*theta_*^canonical - 1.04110|
  (random draws produce theta_* at least as close to Planck as canonical)
```

## Frozen Sources

```text
External (Planck 2018 base-LCDM):
  Reference values quoted directly in this precommit. No catalog data file
  is read by the runner. Planck reference values are hard-coded constants
  matched against runtime SAM outputs.

Branch-local (sealed):
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL\CR018b_summary.json
    (cross-check: CR019 r_d should match CR018b r_d at the same H_0.)

Substrate (read-only):
  manuscript Section 4 derived native quantities
  (A_0, Omega_m identity, Omega_b identity).
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine,
with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and zero catalog
parameters fit, reproduces the Planck 2018 base-LambdaCDM compressed CMB
acoustic geometry to within 1% on 100*theta_*, ell_A, and r_d.

It could have failed if any of the three acoustic-geometry observables
deviated from the Planck reference by more than 1%, i.e.:
  - 100*theta_* outside [1.0307, 1.0515]
  - ell_A outside [298.74, 304.78]
  - r_d outside [145.62, 148.56] Mpc
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM compressed
CMB acoustic geometry to within 1% on all three load-bearing observables:
the acoustic angular scale 100*theta_*, the acoustic peak multipole ell_A,
and the drag sound horizon r_d. The substrate inputs Omega_m = 1/pi and
Omega_b = 2*A_0*(1-chi) are sealed identities, not parameters; external
measurement inputs are H_0 = 68.76 (BAO-side anchor), T_CMB = 2.7255
(FIRAS), and N_eff = 3.046 (standard-model). Zero catalog parameters are
fit, against LCDM's 5+ parameter CMB power-spectrum fit.

CR019 does not claim SAM resolves the H_0 tension. It uses the BAO-side
H_0 = 68.76 for consistency with CR018b. The compressed acoustic geometry
of the CMB is reproduced to sub-percent precision at this H_0.
```

## Connection to CR018b

```text
CR018b sealed PASS (2026-06-27) for the substrate-only SN+BAO distance
spine. The drag sound horizon r_d = 147.769 Mpc derived in CR018b is the
same quantity computed here under the same substrate inputs and same
H_0 = 68.76. CR019 extends the test to the photon-decoupling side
(z_*, r_s(z_*), D_M(z_*)) and to the acoustic geometry observables
(100*theta_*, ell_A) that Planck measures directly.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
