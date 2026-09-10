# CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY

## Verdict

```text
CR033_PASS_X_INF_SUBSTRATE_IDENTITY_10_OVER_PI_REPRODUCES_RAW_SPARC_OUTER_HALO_MASS_POPULATION_MEDIAN
```

## Courtroom Fields

```text
execution_status            = CLEAN
scientific_verdict          = PASS
triage_bin                  = A
free_parameters_introduced  = 0
per_galaxy_fitting          = false
catalog_fit_parameters      = 0
empirical_X_inf_input       = false
prior_CR_result_inputs      = false
precommit_sha256            = fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810
```

## Summary

```text
CR033 PASS confirms that X_inf,SAM = 10/pi, computed from substrate atoms only, reproduces the raw-SPARC outer-radius halo-mass population median within the predeclared +/- 12% tolerance.

This is a retrospective substrate-identification, not a prospective
pre-measurement prediction. The runner did not read CR025, CR031b,
CR032, CR205, or any prior branch result file. The forbidden-file
open() guard installed at runner startup did not trip
(opened_paths_count = 0; forbidden_files_opened = false).
```

## Substrate Identity Under Test

| symbol | value |
|---|---:|
| R | 12 |
| alpha_H | 2 |
| Omega_m = R*A_0 = 1/pi | 0.318309886183791 |
| X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi | 3.18309886183791 |
| f_halo,inf,SAM = 10/(pi+10) | 0.760942776389312 |

## Sample

| field | value |
|---|---:|
| raw galaxies loaded | 175 |
| excluded for fewer than 3 radial points | 0 |
| galaxies passing parser validity | 175 |
| excluded for zero measured halo mass | 2 |
| galaxies in P1 statistic | 173 |

## P1 — Load-Bearing Result

| statistic | value |
|---|---:|
| median(log10(M_halo,SAM / M_halo,measured)) | -0.000311275416 |
| abs(median log10) | 0.000311275416 |
| threshold | 0.05 |
| margin = abs(med log10) / threshold | 0.006226 |
| median linear ratio | 0.999283518662 |
| linear lower bound 10^-0.05 | 0.8912509381 |
| linear upper bound 10^+0.05 | 1.1220184543 |
| **pass** | **True** |

## E2 — Population Agreement Statistics

| stat | value |
|---|---:|
| median linear ratio | 0.999283518662 |
| median log10 ratio | -0.000311275416 |
| abs(median log10) | 0.000311275416 |
| abs(median log10) / 0.05 | 0.006226 |
| mean log10 ratio | +0.043009608663 |
| std log10 ratio | 0.380177831121 |
| min linear ratio | 2.117252e-01 |
| max linear ratio | 3.471870e+01 |
| 25th percentile linear | 0.642807 |
| 75th percentile linear | 1.541000 |

## E3 — Fresh Raw-SPARC Outer Dark-Fraction Consistency

| field | value |
|---|---:|
| n galaxies used | 175 |
| median(f_halo,outer,raw) | 0.760699023483 |
| f_halo,inf,SAM = 10/(pi+10) | 0.760942776389 |
| difference | -0.000243752907 |
| relative difference | -0.032043% |

This is computed inside CR033 from raw SPARC V_dark^2/V_obs^2 at R_outer.
No prior summary or measurement was imported.

## E4 — Algebraic Substrate-Equivalence Check

| identity | value |
|---|---:|
| R - alpha_H | 10 |
| S + alpha_H | 10 |
| Theta - S | 10 |
| (R - alpha_H) * Omega_m | 3.18309886183791 |
| (R - alpha_H) / pi | 3.18309886183791 |
| 10 / pi | 3.18309886183791 |
| all three forms equal 10 | True |
| machine-precision identity holds | True |

## E5 — Cosmic-vs-Bound Ratio Identity

| field | value |
|---|---:|
| Omega_m | 0.318309886184 |
| Omega_b | 0.049299011266 |
| chi | 0.070735530263 |
| X_cosmic | 5.456719475887 |
| X_inf,SAM | 3.183098861838 |
| X_cosmic / X_inf,SAM | 1.714278981815 |
| analytic check pi*(R - 2 + 2chi) / ((R - alpha_H)*(2 - 2chi)) | 1.714278981815 |

## WC1 — Random X_inf Null (1000 trials, seeds 0..999)

| field | value |
|---|---:|
| n trials | 1000 |
| canonical abs(median log10) | 0.000311275416 |
| null mean | 0.323288868909 |
| null median | 0.308775824557 |
| null std | 0.225052104382 |
| null min / max | 0.000236 / 1.454656 |
| n null at-least-as-extreme | 1 |
| canonical percentile | 0.001000 |
| exact (k+1)/(N+1) p-value | 0.001998 |

## WC2 — V_bar Permutation Null (1000 trials, seeds 1000..1999)

| field | value |
|---|---:|
| n trials | 1000 |
| canonical abs(median log10) | 0.000311275416 |
| null mean | 0.037382699485 |
| null median | 0.031744339214 |
| null std | 0.027588107031 |
| null min / max | 0.000001 / 0.159628 |
| n null at-least-as-extreme | 4 |
| canonical percentile | 0.004000 |
| exact (k+1)/(N+1) p-value | 0.004995 |

## Chronology

```text
CR033 is a retrospective substrate-identification test. The candidate
identity X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi was recognized after
earlier Branch 08 halo-saturation work had already been performed.

The runner did not import or read CR025, CR031b, CR032, CR205, or any
prior branch result file. The forbidden-file open() guard was installed
at module load and did not trip. The raw-SPARC mass-model catalog
(MassModels_Lelli2016c.mrt) was the only external input.

Prospective confirmation requires a fresh non-SPARC rotation-curve
catalog. That test is deferred to CR034.
```

## Rule-9 Line

```text
This test could have falsified the claim that X_inf,SAM = 10/pi
reproduces the raw-SPARC outer-radius halo-mass population median to
within +/- 12% of unity using only raw SPARC measurements and substrate
constants.

It did not falsify it: median linear ratio = 0.999284, abs(median
log10) = 0.000311, threshold = 0.05.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit             = fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810
External data         = MassModels_Lelli2016c.mrt (raw SPARC)
Forbidden CR025/CR031b/CR032/CR205 files not opened.
```

---

**Sealed by:** CR033 runner, 2026-06-27.
