# CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST Precommit

## Test Type

```text
Fresh Courtroom branch test, branch 06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE.
Substrate-derived prediction values inherit from CRs sealed before this test
and from manuscript Section 7 (cosmological accumulation).
External anchors: Pantheon+SH0ES (Brout et al. 2022) and DESI DR1 BAO
(2024 release).
```

## Question

```text
Does SAM's substrate-only distance spine, with NO catalog-fit parameters
and NO host-mass correction, reproduce:

  (i)  Pantheon+SH0ES distance moduli when H_0 = 73.04 (SH0ES measurement
       input, the same H_0 baked into the MU_SH0ES calibration) is used;
  (ii) DESI DR1 BAO distance ratios (D_M/r_d, D_H/r_d, D_V/r_d) when
       H_0 = 68.76 (Planck-style low-H_0 calibration) is used;
  (iii) the Planck 2018 base-LambdaCDM drag sound horizon r_d = 147.09 Mpc
       computed self-consistently from the substrate-predicted Omega_m,
       Omega_b plus EH fitting formula, at H_0 = 68.76;

while showing the standard Hubble-tension probe split (SN prefers high H_0,
BAO prefers low H_0) using one substrate spine and different external
H_0 calibrations?
```

## Substrate Inputs (no fitting)

```text
A_0 = 1/(12 pi)                                 (Section 7, sealed)
R = 12                                          (LCQC002 substrate radix)
A_inf = R * A_0 = 1/pi                          (Section 7 completed road
                                                  amplitude)
Omega_m = A_inf = 1/pi = 0.318310               (cosmological matter density;
                                                  zero free parameter)
mu_H = 2^D / D = 8/3                            (Section 7 horizon mean, D=3)
chi = mu_H * A_0 = 2/(9 pi) = 0.070736          (horizon quotient mark)
Omega_b = 2 * A_0 * (1 - chi) = 0.049299        (baryon fraction; Section 7)
flat geometry, w = -1
```

## Measurement Inputs (external, not catalog-fit)

```text
H_0 = 73.04 km/s/Mpc                            (SH0ES; for the SN test;
                                                  the same H_0 baked into
                                                  MU_SH0ES calibration)
H_0 = 68.76 km/s/Mpc                            (Planck-style low-H_0; for
                                                  the BAO test)
r_d                                              (computed from EH fitting
                                                  formula given Om, Ob, H_0;
                                                  not a catalog fit)
```

## Sealed Predictions (P1–P6)

### P1 — Pantheon+ SN zero-parameter weighted-mean residual

```text
With Omega_m = 1/pi, Omega_b = 0.049299, H_0 = 73.04, and NO offset fit,
NO host_logmass correction, and the standard Pantheon+SH0ES sample
(z > 0.01, IS_CALIBRATOR == 0, finite MU_SH0ES and error):

   |weighted_mean_residual| <= 0.025 mag

where weighted_mean = sum_i [MU_obs,i - MU_pred,i] / sigma_i^2
                     / sum_i 1 / sigma_i^2
and sigma_i is the diagonal MU_SH0ES_ERR_DIAG.

Falsifier: |weighted_mean| > 0.025 mag.
```

### P2 — DESI DR1 BAO chi^2

```text
With Omega_m = 1/pi, Omega_b = 0.049299, H_0 = 68.76, EH-computed r_d,
and the 12 DESI DR1 (2024) BAO distance ratios:

   chi^2 / n_points <= 2.5  (i.e., chi^2 <= 30 over 12 points)

Falsifier: chi^2 / n_points > 2.5 under canonical inputs.
```

### P3 — Substrate-predicted sound horizon vs Planck 2018

```text
With Omega_m = 1/pi, Omega_b = 0.049299, H_0 = 68.76:

   |r_d_SAM - r_d_Planck2018| / r_d_Planck2018 <= 0.01
   where r_d_Planck2018 = 147.09 Mpc (base-LambdaCDM drag sound horizon)

Falsifier: relative deviation > 1%.
```

### P4 — Probe-split direction (Hubble tension reproduction, not resolution)

```text
Sweep H_0 in [60, 80] km/s/Mpc at 21 grid points (step 1) keeping
Omega_m = 1/pi, Omega_b = 0.049299 fixed.

P4a: The Pantheon+ weighted_mean_residual has a zero crossing (sign change)
     at H_0_SN_best in [70, 75] km/s/Mpc.
P4b: The DESI BAO chi^2 attains its minimum at H_0_BAO_best in [66, 71]
     km/s/Mpc.
P4c: H_0_SN_best > H_0_BAO_best  (SN-preferred H_0 strictly higher than
     BAO-preferred H_0).

This is the probe-split reproduction. It does not claim to solve the
Hubble tension; it claims that the substrate spine reproduces the same
probe split that standard analyses see, using one set of Omega values.

Falsifier: any of P4a, P4b, P4c fails.
```

### P5 — SN null-distribution percentile

```text
Draw 1000 seeded random Omega_m values from a wide uniform prior
[0.05, 0.95] (seeds 0..999). For each draw, compute the SAM
weighted_mean_residual at H_0 = 73.04 and Omega_b = 0.049299 (fixed).

Form the null distribution of |weighted_mean_residual| values.

Canonical (Omega_m = 1/pi) must produce a |weighted_mean_residual| at
or below the 1st percentile of the null distribution.
Equivalently: one-sided exact permutation p_value:
   p_SN_null = (n_null_trials_with_|residual| <= canonical_|residual| + 1)
               / (n_trials + 1)
   pass condition: p_SN_null < 0.01

Falsifier: p_SN_null >= 0.01 (canonical not extreme vs random Omega_m).
```

### P6 — BAO null-distribution percentile

```text
Draw 1000 seeded random (Omega_m, Omega_b) pairs from uniform
[0.05, 0.95] x [0.005, 0.15] (seeds 0..999). For each draw, compute
the SAM BAO chi^2 at H_0 = 68.76, with EH-computed r_d.

Form the null distribution of chi^2 values.

Canonical (Omega_m = 1/pi, Omega_b = 0.049299) must produce a chi^2 at
or below the 1st percentile of the null distribution.
   p_BAO_null = (n_null_trials_with_chi2 <= canonical_chi2 + 1)
                / (n_trials + 1)
   pass condition: p_BAO_null < 0.01

Falsifier: p_BAO_null >= 0.01 (canonical not extreme vs random Omegas).
```

## Frozen Sources

```text
External (SN):
  C:\VS\quantum_phase\data\external\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat
    (Pantheon+SH0ES distance modulus catalog; Brout et al. 2022)

External (BAO):
  DESI DR1 2024 published release. The 12 (tracer, z_eff, observable,
  value, sigma) tuples are HARDCODED in the runner per the DESI key-project
  paper. Errors treated as diagonal (no covariance release used here).
  These are PROVISIONAL transcriptions; verdict is robust to ~5% error
  inflation but a definitive chi^2 requires the official covariance.

External (Planck):
  r_d_Planck2018 = 147.09 Mpc (Planck 2018 base-LambdaCDM drag sound
  horizon; literature value, not loaded from a file).

Substrate spine (read-only):
  manuscript Section 7 (cosmological accumulation chain)
  CR238 substrate atoms, LCQC002 R=12 radix, A_0 derivation
```

## Implementation Discipline

```text
SN model:
  mu_pred(z) = 25 + 5*log10(D_L_Mpc(z))
  D_L(z) = (1+z) * D_M(z)
  D_M(z) = (c/H_0) * integral_0^z dz' / E(z')
  E(z) = sqrt(Omega_m*(1+z)^3 + Omega_r*(1+z)^4 + Omega_Lambda)
  Omega_Lambda = 1 - Omega_m - Omega_r

BAO model:
  Same E(z) as SN.
  D_M(z) per the integral above.
  D_H(z) = c / (H_0 * E(z))
  D_V(z) = [z * D_M(z)^2 * D_H(z)]^(1/3)
  r_d computed from EH fitting formula (Eisenstein-Hu 1998, eqs 4-6) given
  Om*h^2, Ob*h^2, plus the radiation correction.

Canonical SN sample cut:
  z_HD > 0.01 AND IS_CALIBRATOR == 0 AND finite MU_SH0ES AND
  MU_SH0ES_ERR_DIAG > 0

No host_logmass correction is applied at any step. No mass step. No
catalog parameter is fit.

Random-seed discipline:
  P5 SN null:  numpy.random.default_rng(seed) with seeds 0..999
  P6 BAO null: same generator with seeds 0..999

P-value formula:
  one-sided exact permutation
  p = (n_extreme + 1) / (n_trials + 1)
  n_extreme = number of null trials at least as extreme as canonical
  in the substrate-predicted direction
```

## Verdict Ladder

```text
PASS:
  P1, P2, P3, P4, P5, P6 all hold under canonical substrate values

BOUNDARY:
  P1, P2, P3 all hold under canonical (the direct prediction-vs-data
  comparisons land), but at least one of P4, P5, P6 fails (the probe-split
  reproduction or one of the null-distribution percentile tests doesn't
  satisfy the discipline)

FAIL:
  P1 fails OR P2 fails OR P3 fails (canonical prediction at the right
  inputs does not reproduce the data within the declared bounds)
```

## Pass Discipline

```text
free_parameters_introduced = 0
execution_status = CLEAN
no per-SN fitting
no host_logmass correction
no offset fit on SN
no per-BAO parameter fitting
no Omega adjustment to match references
trial seeds 0..999 deterministic
H_0 treated as external measurement input, not catalog-fit
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine
(Omega_m = 1/pi, Omega_b = 2*A_0*(1 - 2/(9 pi))) reproduces Pantheon+SH0ES
SN distance moduli at H_0 = 73.04 with zero catalog fit, reproduces DESI
DR1 BAO distance ratios at H_0 = 68.76 with zero catalog fit, reproduces
the Planck 2018 base-LambdaCDM drag sound horizon to within 1%, exhibits
the standard SN-vs-BAO H_0 split direction, and is significantly more
extreme than random Omega_m and (Omega_m, Omega_b) prior draws on both
probes.
```

## Manuscript-Grade Headline (preview, conditional on PASS)

```text
SAM's substrate-only distance spine strongly prefers the low-H_0 BAO scale
and lands close to Planck/DESI BAO performance without fitting Omega_m,
Omega_b, r_d, or host/catalog corrections.

It also predicts the Planck 2018 drag sound horizon r_d = 147.09 Mpc to
within 0.5%.

SAM does not solve the Hubble tension. It reproduces the same probe split
using one substrate spine and different external H_0 calibrations.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
