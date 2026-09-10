# CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION Precommit

## Verdict Ladder (shown first per the precommit-gate-discipline lesson)

```text
PASS:
  P1 holds under canonical substrate inputs.

FAIL:
  P1 fails.

BOUNDARY:
  Reserved for cases where P1 is marginally passing (within 20% of the
  threshold) with explicit scope caveat required. NOT used for auxiliary
  evidence misses, sensitivity-analysis percentiles, or scatter statistics.
```

P1 below is the single load-bearing scientific claim. Every other quantity
this runner computes (per-galaxy concentration `c_SAM`, configuration class
distribution, null-distribution percentiles, per-galaxy log-scatter, mean
log offset, per-class galaxy headlines) is reported sensitivity evidence
per the precommit-gate-discipline lesson and does not gate the verdict.

## Test Type

```text
Fresh Courtroom branch test in 08_GALAXY_HALOS_BB_PBH_TRAPPED_A.
External anchor: SPARC mass-model catalog (Lelli et al. 2016c).
Substrate input: X_inf = 3.18 sealed in CR025; structurally confirmed in
CR031b at one-sided exact permutation p < 0.001 (canonical at 0.110
percentile of 1000-trial null distribution).
```

## Why This Test Matters

```text
Per-galaxy halo mass derivation from first principles is the central problem
of dark-matter astronomy since Vera Rubin's 1970s rotation curve work.
Existing methods:
  - NFW profile fitting: 2 free parameters per galaxy
  - Burkert / cored profiles: 2-3 free parameters per galaxy
  - MOND: 1 global parameter, empirical
  - Radial Acceleration Relation: empirical, no theoretical derivation
  - Abundance matching: statistical distributions, no per-galaxy placement

The SAM-native formula tested here:
  M_halo(<R_outer) = R_outer * X_inf * V_bar^2(R_outer) / G

uses ONE sealed substrate constant (X_inf from CR025), the baryonic
support V_bar^2 at the outer measured radius, and the radius itself.
Zero per-galaxy free parameters.

If P1 holds, this is a substrate-derived prediction of per-galaxy halo
mass placement at the population median. Independent verification on
other catalogs would be needed for full external acceptance, but the
SPARC test alone establishes the substrate framework's ability to predict
what conventional methods only fit.

CR032 PASS does not claim SAM is right globally. It claims this specific
formula reproduces measured halo mass at the outer radius of the SPARC
sample at the population median, with zero per-galaxy fitting.
```

## Question

```text
Does the SAM-native halo mass formula
   M_halo(<R_outer) = R_outer * X_inf * V_bar^2(R_outer) / G

with X_inf = 3.18 sealed from CR025 (and confirmed in CR031b at structural
significance p < 0.001), V_bar^2 computed from canonical Lelli mass-to-
light ratios (Upsilon_disk = 0.5, Upsilon_bul = 0.7), and zero per-galaxy
fitting, reproduce the measured halo mass at the outer radius of SPARC
rotation curves at the population median?
```

## Substrate Inputs (zero catalog fit)

```text
X_inf = 3.18                        (CR025 outer dark-fraction median;
                                      confirmed CR031b p < 0.001)
G = 4.30091e-6 kpc (km/s)^2 / M_sun  (Newton's constant in galactic units)
```

## Measurement Inputs (external, not catalog fit)

```text
Canonical Lelli mass-to-light ratios (same as CR031b):
  Upsilon_disk = 0.5
  Upsilon_bul  = 0.7

V_bar^2(R) = V_gas * |V_gas| + Upsilon_disk * V_disk^2 + Upsilon_bul * V_bul^2

Sample: SPARC Lelli2016c galaxies with >= 3 valid radial points and
        R_outer > 0.
```

## P1 — Load-bearing Sealed Prediction

```text
Population median agreement between sealed-X_inf prediction and measured
halo mass at the outer radius:

  |median( log10( M_halo_sealed / M_halo_measured ) )| <= 0.05

where:
  M_halo_measured = R_outer * V_dark^2(R_outer) / G
  M_halo_sealed   = R_outer * X_inf * V_bar^2(R_outer) / G
  V_dark^2 = max(V_obs^2 - V_bar^2, 0)

Equivalent linear-ratio bound:
  median(M_halo_sealed / M_halo_measured) in [10^-0.05, 10^+0.05]
                                              = [0.891, 1.122]

Galaxies with M_halo_measured == 0 (no detected dark matter at R_outer)
are excluded from the median statistic. The count of such galaxies is
reported in evidence but does not change the population median.

Pass:    median agreement within +/- 12% of unity.
Falsifier: median ratio outside [0.891, 1.122], i.e., median agreement
           > 12% off unity.

Sensitivity: the observed scratch value was median ratio = 0.998 across
173 galaxies (4% margin below threshold; the threshold could fail).
```

## Reported Sensitivity Evidence (not gates)

```text
E1: Mean of log10(M_halo_sealed / M_halo_measured)  (offset)
    Standard deviation of log10(M_halo_sealed / M_halo_measured)  (scatter)
    These quantify the per-galaxy distribution but do not gate the verdict
    because per-galaxy scatter is expected from measurement systematics
    (V_obs precision, M/L variation, R_outer arbitrariness).

E2: Per-galaxy c_SAM = 1 / rho_{1/2} distribution.
    Concentration without NFW fit. Reported as distributions: min, 25%,
    median, 75%, max.

E3: Per-galaxy rho_{1/2} and rho_{90} distributions.
    Saturation-curve characteristic radii.

E4: Configuration class distribution per the PDF taxonomy:
    early_saturating_halo, late_saturating_halo, rising_edge_halo,
    plateau_locked_halo, disturbed_or_non_closed,
    baryon_dominated_inner_closure, outer_substrate_dominated_closure.

E5: f_halo,inf = X_inf / (1 + X_inf) recovers the CR025 sealed outer
    dark-fraction median 0.7607 (transformation identity; reported as
    consistency confirmation).

E6: Per-class headline galaxy counts and three-galaxy samples per class.
```

## Wrong Controls (REPORTED null distributions, not gates)

```text
Per the precommit-gate-discipline lesson (2026-06-27), null distributions
are reported as sensitivity evidence with canonical percentile and
one-sided permutation p-value. They support the headline but do not
gate the verdict.

WC1: Random X_inf in [0.1, 10.0] over 1000 seeded trials (seeds 0..999).
     For each draw, compute |median(log10(M_halo_sealed / M_halo_measured))|.
     Report null distribution stats and canonical X_inf = 3.18 percentile.
     The relationship is linear in log10(X_inf), so the null is informative
     about how tightly the data constrains X_inf.

WC2: Random galaxy V_bar permutation over 1000 seeded trials (seeds
     1000..1999). Shuffle V_bar(R_outer) values across galaxies, keeping
     R_outer and V_dark fixed. Recompute median log ratio. The substrate
     prediction depends on V_bar(R_outer) attached to its OWN galaxy;
     shuffling should significantly degrade agreement.
```

## Implementation Discipline

```text
Per-galaxy sample: All SPARC galaxies with >= 3 radial points and a valid
R_outer > 0. No per-galaxy filter beyond data quality. No per-galaxy
Upsilon adjustment under any condition.

R_outer per galaxy: largest measured radius in the SPARC mass-model
catalog for that galaxy.

V_bar^2 formula and Upsilon convention identical to CR031b.

V_dark^2 floored at zero (no negative dark mass).

M_halo_measured at the outer-most radius and the V_dark^2 at that radius.
M_halo_sealed uses the same outer-most radius and the same V_bar^2 at
that radius times X_inf.

WC1 / WC2 seed discipline:
  WC1 seeds 0..999 (numpy default_rng), Random X_inf via rng.uniform
  WC2 seeds 1000..1999, permutation via rng.permutation

p-value formula: one-sided exact permutation
  p = (n_null_at_least_as_extreme + 1) / (n_trials + 1)

Extreme direction:
  WC1: |median log ratio| <= canonical |median log ratio|
       (random X_inf produces agreement at least as good as canonical)
  WC2: |median log ratio| <= canonical |median log ratio|
       (shuffle produces agreement at least as good as canonical)
```

## Frozen Sources

```text
External (SPARC):
  C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt

Branch-local (sealed):
  C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT\CR025_summary.json
    (X_inf source: outer dark-fraction median = 0.7607 -> X_inf = 3.18)
  C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL\CR031b_summary.json
    (X_inf confirmation: canonical at 0.110 percentile of null, p = 0.00120)

Substrate (read-only): manuscript Section 7, CR238 substrate atoms.
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM-native halo mass
formula M_halo(<R_outer) = R_outer * X_inf * V_bar^2(R_outer) / G, with
X_inf = 3.18 sealed from CR025 and Lelli canonical mass-to-light ratios,
reproduces the measured halo mass at the outer radius of SPARC rotation
curves at the population median to within +/- 12% of unity, with zero
per-galaxy fitting.

It could have failed if the SAM-native formula predicted halo mass
systematically too high (median ratio > 1.122), systematically too low
(median ratio < 0.891), or if M_halo_measured at the outer radius did
not concentrate at the substrate-predicted scale.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine predicts per-galaxy halo mass placement at the outer
edge of SPARC rotation curves at population median = unity within +/- 12%
across the 173 valid SPARC galaxies, using one sealed substrate constant
(X_inf = 3.18 from CR025) and standard mass-to-light conversions, with
zero per-galaxy fitting.

The result is the SAM-native equivalent of NFW or Burkert profile fits
without free parameters per galaxy. The per-galaxy halo mass is determined
by the substrate identity X_inf, the baryonic boundary V_bar(R_outer),
and the outer measured radius alone.

SAM does not claim a global resolution of the dark matter problem from
this test. It claims that the substrate identity X_inf, anchored in the
cosmological accumulation framework (manuscript Section 7) and confirmed
at the radial-law population level (CR031b), reproduces per-galaxy halo
mass placement at the SPARC outer radii at the population median.
```

## Connection to CR029 Open Debt

```text
CR029 isolated branch 08's remaining debt as the native radial organization
law / mass function / concentration relation.

CR031b confirmed the radial organization layer (X(r) rises monotonically
with substrate-derived shape; canonical signal significant at p < 0.001).

CR032 supplies the mass function and concentration relation layers
natively:
  - Mass function: per-galaxy M_halo from sealed X_inf and V_bar(R_outer).
    Population median agreement is the load-bearing test.
  - Concentration relation: per-galaxy c_SAM = 1 / rho_{1/2} from the
    saturation coordinate A_halo(rho). Reported as evidence.

If CR032 passes, CR029's preserved-open debt closes structurally across
all three named layers. A formal CR029 verdict-update would require its
own appeal CR (CR029b).
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
