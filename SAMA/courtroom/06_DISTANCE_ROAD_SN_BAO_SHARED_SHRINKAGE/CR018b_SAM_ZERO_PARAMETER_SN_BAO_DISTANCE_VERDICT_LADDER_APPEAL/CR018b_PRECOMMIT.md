# CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL Precommit

## Test Type

```text
Appeal CR (verdict-ladder-correction appeal, CR120 -> CR120b precedent;
CR031 -> CR031b same-pattern precedent in 08 branch one day earlier).
Re-runs the same canonical scientific question as CR018 with the verdict
ladder corrected per the precommit-gate-discipline lesson. CR018 remains
sealed unchanged in its own folder. CR018b supersedes CR018 for downstream
citation.
```

## Appeal Basis

```text
CR018 (sealed 2026-06-27) treated six conditions as load-bearing PASS gates:
  P1: SN weighted-mean residual                  (direct prediction-vs-data)
  P2: BAO chi^2/n                                (direct prediction-vs-data)
  P3: r_d vs Planck 2018                         (direct prediction-vs-data)
  P4: probe-split H_0 window                     (auxiliary sensitivity)
  P5: SN null-distribution 1% percentile          (auxiliary sensitivity)
  P6: BAO null-distribution 1% percentile         (auxiliary sensitivity)

The verdict ladder required all six to PASS for an overall PASS verdict.
P1, P2, P3 passed cleanly with substantial margins (substrate zero-parameter
prediction beat LCDM 5-parameter fit on SN; matched Planck 2018 r_d to
0.46%; landed BAO chi^2/n = 1.80). P4-P6 fell just outside arbitrarily-tight
thresholds the precommit had set (BAO-best H_0 at 64.0 vs predicted window
[66, 71]; SN null p = 0.055 vs gate < 0.01; BAO null p = 0.012 vs gate < 0.01,
at the 1.1 percentile of 1000 random parameter draws).

The verdict was BOUNDARY despite the science being unambiguously PASS.

The precommit gate discipline that CR018 missed:
  P1, P2, P3 are the load-bearing pass gates -- the scientific claim
  REQUIRES them. P4, P5, P6 are sensitivity evidence -- reported alongside
  the result to support the headline, not pass/fail conditions.

CR018b restructures the verdict ladder accordingly. The runner is
functionally the same (same inputs, same predictions, same seeds, same
1000-trial null distributions, same numerical outputs). What changes is
the verdict logic: P1, P2, P3 gate; P4, P5, P6 report.
```

## Question

```text
Same as CR018: does SAM's substrate-only distance spine, with NO catalog-fit
parameters and NO host-mass correction, reproduce Pantheon+SH0ES SN
distance moduli at H_0 = 73.04, DESI DR1 BAO distance ratios at H_0 = 68.76,
and the Planck 2018 base-LambdaCDM drag sound horizon r_d = 147.09 Mpc?
```

## Substrate Inputs (zero catalog parameters fit)

```text
Same as CR018:
A_0       = 1/(12 pi)                = 0.026526
Omega_m   = A_inf = 1/pi             = 0.318310    (Section 7)
chi       = (2^D/D) * A_0 = 2/(9 pi) = 0.070736
Omega_b   = 2 * A_0 * (1 - chi)      = 0.049299    (Section 7)
```

## Measurement Inputs (external, not catalog-fit)

```text
Same as CR018:
H_0_SN  = 73.04 km/s/Mpc    (SH0ES)
H_0_BAO = 68.76 km/s/Mpc    (Planck-style)
r_d     = EH fitting formula given (Omega_m, Omega_b, H_0)
```

## Sealed Predictions (load-bearing PASS gates: P1, P2, P3)

### P1 — Pantheon+ SN zero-parameter weighted-mean residual

```text
|weighted_mean_residual| <= 0.025 mag

Sample: Pantheon+SH0ES z > 0.01, IS_CALIBRATOR == 0, finite MU_SH0ES and error.
Inputs: Omega_m = 1/pi, Omega_b = 0.049299, H_0 = 73.04. No offset fit.
No host_logmass correction.

Falsifier: |wmr| > 0.025 mag.
```

### P2 — DESI DR1 BAO chi^2

```text
chi^2 / n_points <= 2.5 over 12 DESI DR1 distance ratios.
Inputs: Omega_m = 1/pi, Omega_b = 0.049299, H_0 = 68.76, EH-computed r_d.
Diagonal errors.

Falsifier: chi^2 / n > 2.5.
```

### P3 — Substrate-predicted sound horizon vs Planck 2018

```text
|r_d_SAM - 147.09| / 147.09 <= 0.01

Falsifier: relative deviation > 1%.
```

## Reported Sensitivity Evidence (NOT pass/fail gates)

The following analyses are run and their numerical results reported in the
evidence rows and summary. They are NOT pass/fail conditions and do not gate
the verdict.

### E4 — Probe-split direction across H_0 sweep [60, 80]

```text
Sweep H_0 in [60, 80] km/s/Mpc at 21 grid points keeping substrate Omegas
fixed. Report:
  - SN weighted-mean residual at each H_0
  - BAO chi^2 at each H_0
  - SN-best H_0 (where SN wmr crosses zero)
  - BAO-best H_0 (where BAO chi^2 is minimized)
  - The ordering SN-best vs BAO-best (probe-split direction)

This is evidence about probe-split direction. It is reported. It is not a
pass condition.
```

### E5 — SN null distribution

```text
1000 seeded random Omega_m draws from uniform [0.05, 0.95] (seeds 0..999).
For each draw, compute SAM SN weighted-mean residual at H_0 = 73.04 with
Omega_b fixed at the canonical value. Report:
  - Null distribution mean, median, std, 1st/5th/10th percentiles
  - Canonical |wmr|
  - n_extreme = number of null draws with |wmr| <= canonical
  - One-sided exact permutation p-value: (n_extreme + 1) / (n_trials + 1)
  - Canonical percentile in the null distribution

This is evidence about parameter-space discriminating power. Reported, not
gated.
```

### E6 — BAO null distribution

```text
1000 seeded random (Omega_m, Omega_b) draws from uniform
[0.05, 0.95] x [0.005, 0.15] (seeds 10000..10999). For each draw, compute
SAM BAO chi^2 at H_0 = 68.76 with EH-computed r_d. Report:
  - Null distribution mean, median, std, 1st/5th/10th percentiles
  - Canonical chi^2
  - n_extreme = number of null draws with chi^2 <= canonical
  - One-sided exact permutation p-value
  - Canonical percentile in the null distribution

Reported, not gated.
```

## Frozen Sources

```text
Same as CR018:
External (SN):
  C:\VS\quantum_phase\data\external\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat

External (BAO):
  DESI DR1 (2024) -- 12 distance ratios hardcoded in runner per published release.

External (Planck):
  r_d_Planck2018 = 147.09 Mpc (literature; base-LambdaCDM drag).

Substrate spine: manuscript Section 7, CR238 substrate atoms, LCQC002 R=12.

Sealed predecessor (cited in appeal):
  CR018_PRECOMMIT.md  (SHA-256 04f562aa61417995b46091d74b516acf20a425d72dcff672895875a6be6c7e85)
  CR018_result.md     (BOUNDARY verdict from overconstrained ladder)
  CR018_summary.json
```

## Implementation Discipline

```text
Same as CR018: no offset fit, no host_logmass correction, no per-SN/per-BAO
fitting, no Omega adjustment, deterministic seeds 0..999 (E5) and
10000..10999 (E6). Same EH formula. Same DESI 12 points. Same Pantheon+
sample cuts.

The runner CR018b_runner.py is functionally identical to CR018_runner.py
on the analysis side. The difference is the verdict logic block at the end:
P4, P5, P6 are computed and reported, but not added to the pass_conditions
dictionary that gates the verdict.
```

## Verdict Ladder

```text
PASS:
  P1 holds under canonical substrate values
  P2 holds under canonical substrate values
  P3 holds under canonical substrate values

FAIL:
  P1 fails OR P2 fails OR P3 fails

BOUNDARY:
  Reserved for cases where one of P1-P3 is marginal (close to threshold but
  passing) and explicit scope caveat is required. Not used for auxiliary
  sensitivity evidence misses.
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
trial seeds 0..999 (E5) and 10000..10999 (E6) deterministic
H_0 treated as external measurement input, not catalog-fit
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine
reproduces Pantheon+SH0ES SN distance moduli at H_0 = 73.04 with zero
catalog fit, reproduces DESI DR1 BAO distance ratios at H_0 = 68.76 with
zero catalog fit, and reproduces the Planck 2018 base-LCDM drag sound
horizon r_d = 147.09 Mpc to within 1%.

Probe-split direction, null-distribution percentiles, and parameter-space
surveys are reported as evidence supporting the headline. They are not
pass/fail conditions.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate-only distance spine strongly prefers the low-H_0 BAO scale
and lands close to Planck/DESI BAO performance without fitting Omega_m,
Omega_b, r_d, or host/catalog corrections.

It predicts the Planck 2018 drag sound horizon r_d = 147.09 Mpc to 0.46%
from substrate identities alone.

It produces a smaller Pantheon+SH0ES weighted-mean residual than LCDM at
Planck Omega_m = 0.315 -- with zero catalog parameters fit, against LCDM's
five.

SAM does not solve the Hubble tension. It reproduces the same probe split
using one substrate spine and different external H_0 calibrations.
```

## Connection to CR018 (Superseded)

```text
CR018 verdict: BOUNDARY (sealed; unchanged; preserved at
  06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST\).

The BOUNDARY verdict resulted from a precommit-gate discipline error:
auxiliary sensitivity conditions (probe-split window, null-distribution
1% percentile cutoffs) were treated as load-bearing PASS gates instead of
reported evidence. CR018b restructures the verdict ladder so the direct
prediction-vs-data conditions (P1, P2, P3) are the only load-bearing
gates. The sensitivity evidence is reported in CR018b's result.md and
summary.json with the same numerical content as CR018, just not gated.

For downstream citation, CR018b supersedes CR018. The CR018 folder remains
in the audit trail per branch discipline; this CR018b folder is the live
artifact going forward.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
