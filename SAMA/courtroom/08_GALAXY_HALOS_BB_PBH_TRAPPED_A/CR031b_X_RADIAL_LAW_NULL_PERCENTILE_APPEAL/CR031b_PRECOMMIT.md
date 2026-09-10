# CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL Precommit

## Test Type

```text
Appeal CR (Deferred-Support / Methodology-Correction Appeal pattern,
CR120 -> CR120b precedent in this same branch).
Re-tests the same canonical scientific question as CR031 with corrected
wrong-control methodology. CR031 remains sealed and unchanged in its own
folder; CR031b supersedes it for downstream citation per branch discipline.
```

## Appeal Basis

```text
CR031 used a binary kill-fraction threshold (>= 95% of shuffle/randomization
trials failing the same coarse predicate) on its WC3 and WC4 wrong controls.
This is statistically backward. The correct analysis scores the canonical
observed statistic against the null distribution of the same statistic
across the trials, expressed as a percentile or one-sided exact permutation
p-value. CR031 discarded the magnitude information from 1000 seeded trials
and produced an undeserved BOUNDARY verdict.
CR031b retests cleanly with null-distribution percentile scoring.
```

## Question

```text
Same as CR031: does X(r) = V_dark^2(r) / V_bar^2(r), computed at every
measured SPARC radius across all 175 galaxies and binned in r/R_outer, rise
monotonically from a baryon-dominated inner regime to a bound-halo plateau
matching the sealed CR025 reference, with cross-galaxy convergence at the
outer edge, under canonical Lelli mass-to-light ratios and zero per-galaxy
fitting?
```

## Sealed Predictions

### P1 — Monotonic rise (load-bearing)

```text
Same conditions as CR031 P1:
  median X(0.8-1.0) - median X(0.0-0.2) > 0
  Spearman rank correlation between bin index and median X > 0
  at least 3 of 4 adjacent bin pairs show rise

Falsifier: endpoint_diff <= 0, OR Spearman <= 0, OR fewer than 3 adjacent rises.
```

### P2 — Outer plateau matches CR025 and stays below cosmic

```text
Same conditions as CR031 P2:
  median X(0.8-1.0) in [2.5, 4.5]
  median X(0.8-1.0) < 4.56  (= 0.85 * cosmic-X 5.36 from CR023)

Falsifier: outer median outside [2.5, 4.5], OR median >= 4.56.
```

### P3 — Cross-galaxy convergence at outer edge

```text
Same conditions as CR031 P3:
  spread(0.8-1.0) < spread(0.0-0.2)
  at least 3 of 4 adjacent bin pairs show spread decrease

Falsifier: outer spread >= inner spread, OR fewer than 3 adjacent decreases.
```

### P4 — Within-galaxy radial-shuffle null significance

```text
WC3 null distribution test (replaces CR031 WC3 binary kill threshold):
  For each of 1000 seeded within-galaxy shuffles, compute endpoint_diff =
  median X(0.8-1.0) - median X(0.0-0.2) under canonical Upsilon.
  This forms a null distribution of endpoint_diff under destroyed radial
  ordering.

  Let n_extreme = number of null trials with endpoint_diff >= canonical
  observed endpoint_diff.
  One-sided exact permutation p-value:
    p_WC3 = (n_extreme + 1) / (n_trials + 1)

  Pass condition: p_WC3 < 0.01
  i.e., canonical endpoint_diff is at or above the 99th percentile of the
  null distribution.

  Falsifier: p_WC3 >= 0.01.
```

### P5 — Galaxy-randomized rho null significance

```text
WC4 null distribution test (replaces CR031 WC4 binary kill threshold):
  For each of 1000 seeded galaxy-randomized rho trials, compute
  spread_endpoint_diff = log10_spread(0.8-1.0) - log10_spread(0.0-0.2)
  under canonical Upsilon.
  This forms a null distribution of spread_endpoint_diff under destroyed
  radial bin assignment.

  Let n_extreme = number of null trials with spread_endpoint_diff <=
  canonical observed spread_endpoint_diff (canonical is more negative
  = more convergent).
  One-sided exact permutation p-value:
    p_WC4 = (n_extreme + 1) / (n_trials + 1)

  Pass condition: p_WC4 < 0.01
  i.e., canonical spread_endpoint_diff is at or below the 1st percentile
  of the null distribution (more negative).

  Falsifier: p_WC4 >= 0.01.
```

## Soft Controls (WC1, WC2)

```text
WC1: Upsilon_disk = 0.3, Upsilon_bul = 0.7. P1 and P3 must hold.
WC2: Upsilon_disk = 0.7, Upsilon_bul = 0.7. P1 and P3 must hold.
Falsifier: P1 or P3 fails under WC1 or WC2.
```

## Frozen Sources

```text
External (SPARC):
  C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt

Branch-local (sealed):
  CR023_summary.json  (cosmic-X reference 5.364)
  CR025_summary.json  (SPARC outer-median reference 3.18)
  G392_sparc_galaxy_residuals.csv  (quality flags, secondary audit)
  CR031_PRECOMMIT.md      (sealed predecessor; SHA-256 01797081...42b05)
  CR031_result.md         (sealed predecessor verdict BOUNDARY)
  CR031_summary.json      (sealed predecessor data; the 1000-trial seeds and
                            null distributions are the same here)

Substrate spine (read-only):
  CR240 forced N=Z identity, CR238 substrate atoms
```

## Mass-to-Light Discipline

```text
Canonical: Upsilon_disk = 0.5, Upsilon_bul = 0.7 (Lelli 2016c).
WC bracket: Upsilon_disk in {0.3, 0.7}; Upsilon_bul = 0.7 held.
No per-galaxy Upsilon adjustment under any condition.
```

## Implementation Discipline

```text
For each galaxy, R_outer is the largest measured SPARC radius retained for
that galaxy. Normalized radius rho = R / R_outer. Bin rho into:
  [0.0, 0.2), [0.2, 0.4), [0.4, 0.6), [0.6, 0.8), [0.8, 1.0]

Baryonic velocity squared:
  V_bar^2 = V_gas * |V_gas| + Upsilon_disk * V_disk^2 + Upsilon_bul * V_bul^2

Dark residual:
  V_dark^2 = V_obs^2 - V_bar^2

Radial halo ratio:
  X = V_dark^2 / V_bar^2
```

```text
Primary statistic (galaxy-equal):
For each galaxy and each rho-bin, compute the median X over that galaxy's
measured points in the bin. The bin "median X" is the population median
across galaxy-bin medians.

Log-spread:
Use only positive galaxy-bin X values for log10(X) std-dev. The substitute
Y = 1 + X is NOT declared in this precommit and may not be used.

Nonpositive accounting:
Report at the galaxy-bin level directly:
  nonpositive_galaxy_bin_count[b] = n_galaxies_with_X_in_bin[b]
                                  - n_galaxies_with_positive_X_in_bin[b]
Reported per bin alongside the raw-point nonpositive count.

Primary sample:
All 175 SPARC galaxies. Quality flags secondary audit only.
```

```text
Null-distribution discipline (P4 and P5):
WC3 null = 1000 seeded within-galaxy shuffles (seeds 0..999).
WC4 null = 1000 seeded galaxy-randomized rho trials (seeds 0..999).
Same seed sequence as CR031 to inherit deterministic reproducibility.

For each trial, the runner stores the relevant CONTINUOUS statistic:
  WC3 trial -> endpoint_diff value (median X(0.8-1.0) - median X(0.0-0.2))
  WC4 trial -> spread_endpoint_diff value
              (log10_spread(0.8-1.0) - log10_spread(0.0-0.2))

One-sided exact permutation p-value:
  p = (n_null_trials_at_least_as_extreme + 1) / (n_trials + 1)
  PASS criterion: p < 0.01 (canonical at or beyond 99th percentile of null
  in the direction of the substrate-predicted effect).
```

## Verdict Ladder

```text
PASS:
  P1, P2, P3 hold under canonical Upsilon
  P4 holds: p_WC3 < 0.01
  P5 holds: p_WC4 < 0.01
  WC1 preserves P1 and P3
  WC2 preserves P1 and P3

BOUNDARY:
  P1 holds (canonical rise direction) but at least one of P2, P3, P4, P5,
  WC1, WC2 fails against prediction

FAIL:
  P1 fails under canonical Upsilon
```

## Pass Discipline

```text
free_parameters_introduced = 0
execution_status = CLEAN
no per-galaxy fitting
no Upsilon adjustment to match references
trial seeds 0..999 inherited from CR031 (deterministic)
```

## Rule-9 Line

```text
This test could have falsified the claim that X(r) rises monotonically with
radius across the 175-galaxy SPARC population to a bound-halo plateau
matching the CR025 sealed reference, with cross-galaxy convergence at the
outer edge, under canonical Lelli mass-to-light ratios, AND that this
canonical signal is significantly more extreme than the null distribution
generated by within-galaxy radial shuffles and galaxy-randomized normalized
radius assignments.
```

## Connection to CR031

```text
CR031 is preserved unchanged in its own folder. CR031b supersedes CR031
for downstream citation per the branch's appeal-CR pattern. The supersession
record (this file plus CR031b_result.md after running) cites CR031's
methodology error explicitly: binary kill-fraction discipline instead of
null-distribution percentile.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
