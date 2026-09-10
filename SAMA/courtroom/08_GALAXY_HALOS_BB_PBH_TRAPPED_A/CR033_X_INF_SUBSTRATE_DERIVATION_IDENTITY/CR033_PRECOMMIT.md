# CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY Precommit

## Verdict Ladder

```text
PASS:
  P1 holds.

BOUNDARY:
  P1 holds, but the raw-SPARC parser produces an implementation anomaly,
  sample anomaly, or data-validity issue that prevents a clean sealed
  comparison.

FAIL:
  P1 fails.
```

P1 is the single load-bearing scientific claim. All reported evidence,
algebra checks, and wrong controls are sensitivity evidence only and do
not gate the verdict.

## Test Type

```text
Fresh Courtroom branch test in:
  08_GALAXY_HALOS_BB_PBH_TRAPPED_A

External anchor:
  Raw SPARC mass-model catalog, Lelli et al. 2016c.

Substrate input:
  X_inf,SAM computed from substrate atoms only.

Prior-CR exclusion:
  No CR025, CR031b, CR032, CR205, or prior branch result file may be
  read by the runner, used as an input, used as a comparison gate, used
  as a sensitivity benchmark, used as a class split, or used to set any
  numerical threshold.
```

## Why This Test Matters

```text
Branch 08 has already shown that the SPARC halo residual organizes around
an outer saturation coordinate. CR033 asks whether the outer bound-halo
ratio can be supplied directly from substrate atoms rather than from any
empirical halo anchor.

The candidate identity is:

  X_inf,SAM = (R - alpha_H) * Omega_m
            = (R - alpha_H) / pi
            = 10 / pi

where:
  R       = 12
  alpha_H = 2
  A_0     = 1/(12*pi)
  Omega_m = R*A_0 = 1/pi

The test is not allowed to import the previous empirical outer-halo
result. It must compute the halo-mass comparison fresh from raw SPARC
measurements and the substrate identity alone.

CR033 is therefore a fresh raw-data sufficiency test of one specific
closed-form identity:

  Can X_inf,SAM = 10/pi, with no fitted halo-scale constant and no
  empirical X_inf anchor, reproduce the raw-SPARC outer-radius
  halo-mass population median within the predeclared tolerance?

This is not a forward-prediction test outside SPARC. A non-SPARC catalog
test is deferred to CR034.
```

## Question

```text
Does the substrate identity

  X_inf,SAM = (R - alpha_H) * Omega_m = 10/pi

when used in the halo-mass formula

  M_halo,SAM(<R_outer) =
    R_outer * X_inf,SAM * V_bar^2(R_outer) / G

and evaluated fresh against raw SPARC outer-radius measurements,
reproduce the population median halo-mass agreement within:

  |median(log10(M_halo,SAM / M_halo,measured))| <= 0.05

with zero free parameters, zero empirical X_inf input, and no prior-CR
result files?
```

## Substrate Identity Under Test

```text
The candidate identity is:

  X_inf,SAM = (R - alpha_H) * Omega_m
            = (R - alpha_H) / pi
            = (12 - 2) / pi
            = 10 / pi
            = 3.183098861837907...

The halo-fraction form is:

  f_halo,inf,SAM = X_inf,SAM / (1 + X_inf,SAM)
                 = (10/pi) / (1 + 10/pi)
                 = 10 / (pi + 10)
                 = 0.760942776389...

Equivalent substrate forms for the numerator:

  R - alpha_H = 12 - 2 = 10
  S + alpha_H = 8  + 2 = 10
  Theta - S   = 18 - 8 = 10

These equivalent forms are algebraic evidence only. The canonical input is:

  X_inf,SAM = 10/pi
```

## Strict Input Discipline

```text
The CR033 runner may use only the following inputs.

External raw data
  MassModels_Lelli2016c.mrt

Fixed mass-to-light choices
  Upsilon_disk = 0.5
  Upsilon_bul  = 0.7

Physical constant
  G = 4.30091e-6 kpc (km/s)^2 / M_sun

Substrate constants
  R       = 12
  D       = 3
  S       = 8
  Theta   = 18
  alpha_H = 2
  A_0     = 1/(12*pi)
  Omega_m = R*A_0 = 1/pi
  X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi
```

## Forbidden Inputs

```text
The CR033 runner must not read, import, parse, compare against, or use:

  CR025_summary.json
  CR031b_summary.json
  CR032_summary.json
  CR205 files or summaries
  any prior CR result.md file
  any prior CR summary.json file
  any prior CR evidence_rows.csv file
  any prior empirical X_inf value
  any prior outer dark-fraction median
  any prior population median ratio
  any prior margin statistic
  any prior null percentile
  any prior per-galaxy configuration class file
  any prior CR032 per-galaxy halo-mass table
  any value copied from an earlier branch result

Prior CRs may be discussed only in post-run chronology/provenance language.
They may not supply any runner input, gate, class split, comparison
benchmark, or sensitivity number.
```

## Measurement Construction From Raw SPARC

```text
For each galaxy, CR033 shall parse the raw SPARC mass-model rows and
compute the outer-radius quantities directly.

The canonical baryonic velocity-squared term is:

  V_bar^2(R) =
      V_gas(R) * abs(V_gas(R))
    + Upsilon_disk * V_disk(R)^2
    + Upsilon_bul  * V_bul(R)^2

with:
  Upsilon_disk = 0.5
  Upsilon_bul  = 0.7

The dark residual is:

  V_dark^2(R) = max(V_obs(R)^2 - V_bar^2(R), 0)

For each galaxy, define:

  R_outer = largest valid measured radius for that galaxy

Then compute:

  M_halo,measured(<R_outer) =
    R_outer * V_dark^2(R_outer) / G

and

  M_halo,SAM(<R_outer) =
    R_outer * (10/pi) * V_bar^2(R_outer) / G

All quantities must be computed from the raw SPARC table and the
substrate identity. No prior per-galaxy files may be used.
```

## Sample Rule

```text
The eligible galaxy sample is determined fresh inside CR033.

A galaxy is eligible for parsing if:
  it has at least 3 valid radial points,
  R_outer > 0,
  V_obs is valid at R_outer,
  and V_bar^2 can be computed at R_outer.

A galaxy is eligible for the P1 median statistic if additionally:
  M_halo,measured(<R_outer) > 0

Galaxies with:
  M_halo,measured(<R_outer) == 0

are excluded from the P1 median statistic and counted separately.

The runner must report:
  raw galaxies loaded
  galaxies passing parser validity
  galaxies excluded for zero measured halo mass
  galaxies entering the P1 median statistic

No prior CR sample count is imported.
```

## P1 — Load-Bearing Sealed Prediction

```text
Population median agreement between the substrate-derived prediction and
measured halo mass at the outer radius:

  |median(log10(M_halo,SAM / M_halo,measured))| <= 0.05

Equivalent linear-ratio bound:

  median(M_halo,SAM / M_halo,measured) in [10^-0.05, 10^+0.05]

Numerically:

  [0.8912509381, 1.1220184543]

Pass condition:
  median agreement within +/- 12% of unity.

Falsifier:
  median ratio outside [0.8912509381, 1.1220184543]

P1 is the only verdict gate.
```

## Reported Evidence, Not Gates

```text
E1 — Substrate identity values

Report:
  X_inf,SAM      = 10/pi
  f_halo,inf,SAM = 10/(pi + 10)

These are computed directly from substrate atoms and pi.


E2 — Population agreement statistics

Report:
  median(M_halo,SAM / M_halo,measured)
  median(log10(M_halo,SAM / M_halo,measured))
  abs(median(log10 ratio))
  abs(median(log10 ratio)) / 0.05
  mean(log10 ratio)
  std(log10 ratio)
  min/max linear ratio
  25/75 percentile linear ratio


E3 — Fresh raw-SPARC outer dark-fraction consistency check

Independently compute the raw-SPARC outer dark-fraction median inside
CR033:

  f_halo,outer,raw =
    V_dark^2(R_outer) / V_obs^2(R_outer)

for all eligible galaxies with valid positive terms.

Then report:
  median(f_halo,outer,raw)
  f_halo,inf,SAM = 10/(pi + 10)
  difference
  relative difference

This is a fresh CR033 internal consistency check from raw SPARC only.
It must not read CR025 or any prior summary.


E4 — Algebraic substrate-equivalence check

Verify:
  R - alpha_H = 10
  S + alpha_H = 10
  Theta - S   = 10

Verify:
  (R - alpha_H)*Omega_m = (R - alpha_H)/pi = 10/pi

to machine precision.

This is a structural algebra check, not a wrong control and not a
verdict gate.


E5 — Cosmic-vs-bound ratio identity

Report the cosmic dark/baryon ratio:

  X_cosmic = (Omega_m - Omega_b) / Omega_b

where:
  Omega_m = R*A_0 = 1/pi
  chi     = (S/D)*A_0 = 2/(9*pi)
  Omega_b = 2*A_0*(1 - chi)

Then report:

  X_cosmic / X_inf,SAM =
    pi*(R - 2 + 2*chi) / ((R - alpha_H)*(2 - 2*chi))

This is reported evidence for the separation between cosmic dark/baryon
inventory and bound-halo saturation. It is not a P1 gate.
```

## Wrong Controls

```text
Wrong controls are reported null distributions only. They do not gate
the verdict.


WC1 — Random X_inf null

Generate 1000 seeded random values:

  X_inf_random ~ Uniform(0.1, 10.0)
  seeds = 0..999
  numpy default_rng

For each value, compute:

  M_halo,random(<R_outer) =
    R_outer * X_inf_random * V_bar^2(R_outer) / G

and the statistic:

  abs(median(log10(M_halo,random / M_halo,measured)))

Report:
  null mean
  null std
  null min/max
  canonical statistic
  canonical percentile
  number of null trials beating or matching canonical
  exact percentile using (k + 1)/(N + 1)


WC2 — V_bar permutation null

Generate 1000 seeded permutations:

  seeds = 1000..1999
  numpy default_rng

Shuffle:
  V_bar^2(R_outer)

across galaxies while keeping each galaxy's:
  R_outer
  V_dark^2(R_outer)
  M_halo,measured

fixed.

Use the canonical:
  X_inf,SAM = 10/pi

Recompute the median log-ratio statistic for each shuffle.

Report:
  null mean
  null std
  null min/max
  canonical statistic
  canonical percentile
  number of null trials beating or matching canonical
  exact percentile using (k + 1)/(N + 1)
```

## Implementation Discipline

```text
The CR033 runner shall:

1. Compute X_inf,SAM = 10 / math.pi as the only canonical X_inf input.
2. Parse only raw MassModels_Lelli2016c.mrt for galaxy data.
3. Compute V_bar^2, V_dark^2, R_outer, M_halo,measured, and M_halo,SAM
   fresh inside CR033.
4. Apply the sample rule fresh inside CR033.
5. Compute P1.
6. Compute reported evidence E1-E5.
7. Execute WC1 and WC2 with deterministic seeds.
8. Emit:
     CR033_summary.json
     CR033_evidence_rows.csv
     CR033_result.md
     CR033_null_WC1_random_xinf.csv
     CR033_null_WC2_vbar_shuffle.csv

Precision requirements:
  pi = math.pi double precision
  reported X_inf,SAM with at least 12 significant digits
  reported median/log stats with at least 12 significant digits

Dark residual discipline:
  V_dark^2 = max(V_obs^2 - V_bar^2, 0)

No fitting:
  free_parameters_introduced = 0
  per_galaxy_fitting         = false
  catalog_fit_parameters     = 0
  empirical_X_inf_input      = false
  prior_CR_result_inputs     = false
```

## Frozen Sources

```text
Allowed external source
  C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt

Allowed substrate sources
  R       = 12
  D       = 3
  S       = 8
  Theta   = 18
  alpha_H = 2
  A_0     = 1/(12*pi)
  Omega_m = R*A_0 = 1/pi

Forbidden branch-local sources
  CR025_summary.json
  CR031b_summary.json
  CR032_summary.json
  CR205_summary.json
  any CR025/CR031b/CR032/CR205 result.md
  any CR025/CR031b/CR032/CR205 evidence_rows.csv
  any prior per-galaxy class file
  any prior empirical X_inf file
  any prior outer-dark-fraction file
  any prior halo-mass-placement file

The runner may check that these forbidden files were not opened,
imported, read, or parsed.
```

## Chronology and Honest Framing

```text
This precommit is retrospective relative to the earlier Branch 08 halo
work. The candidate identity:

  X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi

was recognized after earlier SPARC halo-saturation work had already been
performed. That chronology must be disclosed in CR033_result.md.

The honest framing is:

  CR033 is a retrospective substrate-identification test. It does not
  claim that X_inf = 10/pi was predicted before the first SPARC
  halo-saturation reading. It tests whether the halo-saturation value
  can be generated from substrate atoms alone and then survive a fresh
  raw-SPARC halo-mass placement test without importing any previous
  halo-anchor result.

Do not write:
  SAM predicted SPARC X_inf before measurement.

Do write:
  SAM identifies the bound-halo saturation coordinate retrospectively as
  X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi, and CR033 confirms that this
  closed-form substrate value passes a fresh raw-SPARC halo-mass placement
  test.

Prospective confirmation requires a second non-SPARC rotation-curve
catalog.
```

## Rule-9 Line

```text
This test could have falsified the claim that the substrate-atom identity:

  X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi

reproduces the raw-SPARC outer-radius halo-mass population median to
within +/- 12% of unity using only raw SPARC measurements and substrate
constants.

It fails if the SAM-derived value produces:

  median(M_halo,SAM / M_halo,measured) outside [0.8912509381, 1.1220184543]

or equivalently:

  |median(log10(M_halo,SAM / M_halo,measured))| > 0.05
```

## Result Text Requirements

```text
If P1 passes, CR033_result.md must state:

  CR033 PASS confirms that X_inf,SAM = 10/pi, computed from substrate
  atoms only, reproduces the raw-SPARC outer-radius halo-mass population
  median within the predeclared +/- 12% tolerance.

It must also state:

  This is a retrospective substrate-identification, not a prospective
  pre-measurement prediction. The runner did not read CR025, CR031b,
  CR032, CR205, or any prior branch result file.

If P1 fails, CR033_result.md must state:

  CR033 FAIL rejects X_inf,SAM = 10/pi as a sufficient raw-SPARC
  replacement for the outer halo-saturation coordinate under the
  predeclared P1 gate.

In all cases, the result must report:

  free_parameters_introduced = 0
  empirical_X_inf_input      = false
  prior_CR_result_inputs     = false
  catalog_fit_parameters     = 0
  per_galaxy_fitting         = false
  execution_status           = CLEAN or not CLEAN with reason
```

## Manuscript Headline If PASS

```text
Conditional manuscript language:

  The bound-halo saturation coordinate can be read directly from
  substrate atoms:

    X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi = 3.18309886...

  Using only raw SPARC measurements and this closed-form substrate
  value, CR033 reproduces the outer-radius halo-mass population median
  within the predeclared +/- 12% tolerance, without importing any
  empirical X_inf anchor or prior branch result.

  The corresponding halo fraction is:

    f_halo,inf,SAM = 10/(pi + 10) = 0.76094278...

  This result is a retrospective substrate identification of the
  Branch 08 halo-saturation coordinate. Prospective confirmation
  requires a fresh non-SPARC rotation-curve catalog.

Do not claim:
  predicted before measurement

until CR034 or another forward external-catalog test is sealed.
```

## Connection to Future Work

```text
CR034 placeholder

Apply:
  X_inf,SAM = 10/pi

to a second rotation-curve catalog, such as:
  THINGS
  LITTLE THINGS
  future DESI rotation work
  another independent non-SPARC rotation-curve compilation

using a precommitted parser and no SPARC-derived calibration.
CR034 is the prospective external-catalog test.


CR029b placeholder

After CR033 and CR034, update the concentration-relation debt only if
the prospective non-SPARC test supports the same identity.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
