# CR031_X_RADIAL_LAW_POPULATION_TEST Precommit

## Test Type

```text
Fresh Courtroom branch test, branch 08_GALAXY_HALOS_BB_PBH_TRAPPED_A.
External anchor: SPARC Lelli 2016c.
Substrate-derived prediction values inherit from CRs sealed before this test.
```

## Question

```text
Does X(r) = V_dark^2(r) / V_bar^2(r), computed at every measured SPARC radius
across all 175 galaxies and binned in r/R_outer, rise monotonically from a
baryon-dominated inner regime to a bound-halo plateau matching the sealed
CR025 reference, with cross-galaxy convergence at the outer edge, under
canonical Lelli mass-to-light ratios and zero per-galaxy fitting?
```

## Sealed Predictions

### P1 — Monotonic rise (load-bearing)

```text
median X(0.8-1.0) - median X(0.0-0.2) > 0
Spearman rank correlation between bin index and median X > 0
at least 3 of 4 adjacent bin pairs show rise

Falsifier: endpoint difference <= 0, OR Spearman <= 0, OR fewer than 3
adjacent rises.
```

### P2 — Outer plateau matches CR025 and stays below cosmic

```text
median X(0.8-1.0) in [2.5, 4.5]
median X(0.8-1.0) < 4.56  (= 0.85 * cosmic-X 5.36 from CR023)

Falsifier: outer median outside [2.5, 4.5], OR median >= 4.56.
```

### P3 — Cross-galaxy convergence at outer edge

```text
spread(0.8-1.0) < spread(0.0-0.2)
where spread = std-dev of log10(X) across galaxies in the bin
at least 3 of 4 adjacent bin pairs show spread decrease

Falsifier: outer spread >= inner spread, OR fewer than 3 adjacent decreases.
```

## Wrong Controls

### WC1 — Low mass-to-light (Upsilon_disk = 0.3)

```text
Repeat the full analysis with Upsilon_disk = 0.3, Upsilon_bul = 0.7.
P1 and P3 must hold.

Falsifier: P1 or P3 fails under WC1.
```

### WC2 — High mass-to-light (Upsilon_disk = 0.7)

```text
Repeat with Upsilon_disk = 0.7, Upsilon_bul = 0.7.
P1 and P3 must hold.

Falsifier: P1 or P3 fails under WC2.
```

### WC3 — Within-galaxy radius shuffle

```text
Within each galaxy, randomly permute (Vobs, Vgas, Vdisk, Vbul) across the
measured R values. Recompute X(r) and bin medians.
P1 must FAIL under WC3.

Falsifier: P1 holds under WC3 (the rise survives radial shuffling).
```

### WC4 — Galaxy-randomized normalized radius

```text
For each galaxy, replace r/R_outer with a uniform random draw in [0,1].
Recompute bin medians.
P3 must FAIL under WC4.

Falsifier: P3 holds under WC4 (the convergence survives random radius assignment).
```

## Frozen Sources

```text
External (SPARC, Lelli et al. 2016c):
  C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt

Branch-local (sealed):
  CR023_summary.json (cosmic-X reference = 5.364)
  CR025_summary.json (SPARC outer-median reference = 3.18)
  G392_sparc_galaxy_residuals.csv (per-galaxy quality flags)

Substrate spine (read-only):
  CR240 forced N=Z identity (R_sub = 1 at N = Z)
  CR238 substrate atoms
```

## Mass-to-Light Discipline

```text
Canonical: Upsilon_disk = 0.5, Upsilon_bul = 0.7 (Lelli 2016c).
WC bracket: Upsilon_disk in {0.3, 0.7}; Upsilon_bul held at 0.7.
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
across galaxy-bin medians. Each galaxy contributes at most one value per bin.

Log-spread convergence:
Use only positive galaxy-bin X values for log10(X) std-dev. The substitute
Y = 1 + X = V_obs^2 / V_bar^2 may NOT be used unless declared in this
precommit before execution; it is not declared here. The number of
nonpositive galaxy-bin X values is reported in every bin and cannot be
changed after seeing the result.

Primary sample discipline:
All 175 SPARC galaxies are included in the primary result. Quality flags
are reported only as a secondary audit and do not alter PASS/BOUNDARY/FAIL.
```

```text
Random-control discipline:
WC3 and WC4 are evaluated over 1000 seeded random trials each.
  WC3 passes as a negative control only if P1 fails in at least 95%
    of within-galaxy-shuffled trials.
  WC4 passes as a negative control only if P3 fails in at least 95%
    of galaxy-randomized rho trials.
The trial seed sequence is the first 1000 nonnegative integers
(seeds 0..999) for each control. The runner is deterministic given seeds.
```

## Verdict Ladder

```text
PASS:
  P1 holds under canonical Upsilon
  P2 holds
  P3 holds
  WC1 holds P1 and P3
  WC2 holds P1 and P3
  WC3 fails P1 (rise destroyed)
  WC4 fails P3 (convergence destroyed)

BOUNDARY:
  P1 holds under canonical Upsilon
  but at least one of P2, P3, WC1, WC2, WC3, WC4 fails against prediction

FAIL:
  P1 fails under canonical Upsilon
```

## Pass Discipline

```text
free_parameters_introduced = 0
execution_status = CLEAN
no per-galaxy fitting under any condition
no Upsilon adjustment to match references
```

## Rule-9 Line

```text
This test could have falsified the claim that X(r) rises monotonically with
radius across the 175-galaxy SPARC population to a bound-halo plateau matching
the CR025 sealed reference, with cross-galaxy convergence at the outer edge,
under canonical Lelli mass-to-light ratios.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
STEWARDSHIP_DECLARATION.md at repo root.
```
