# CR120Q Precommit — Updated-Sheet Binding-Magnitude Holdout Sensitivity

## Record

- Test ID: `CR120Q_P9_G0_UPDATED_SHEET_BINDING_MAGNITUDE_HOLDOUT_SENSITIVITY`
- Task: `Measure binding residual improvement from updated p9 g0 spreadsheet assemblies`
- Class: constructive new work
- Preflight: `artifacts/preflight_filled/PREFLIGHT_20260714_045036_no_script.md`
- Frozen source manifest: `CR120Q_SOURCE_MANIFEST.csv`
- Frozen source-manifest SHA256: `31ed59a0f6b7cb52e7e448ef97dee60d74500bc63e006e489953c960972c436e`

## Question

When the new spreadsheet **sums** are placed directly into the `M`-bearing CR242 binding features as scale-substitution challenges, do the frozen 20-isotope holdout residual magnitudes improve?

This is a numerical sensitivity test. It does not declare that a spreadsheet sum is the registered `M = 126`, does not alter CR242, and does not create an isotope-to-QP093A occupancy map.

## Controlling p9 scope

The only removal relation used is:

```text
[p=9,g=0] = [p=1,g=0] + [p=8,g=0]
```

for the five CR120O-scope-correction rows only. No `g=1`, `g=2`, composite, W9-identity, qA, or all-depth relation enters this test.

## Frozen spreadsheet sums

All values below are whole-roster `M_native` **sums**, never means:

| scenario | sum | status |
|---|---:|---|
| `BASELINE_REGISTERED_M126` | 126 | frozen CR242 baseline only |
| `SHEET81_AS_SAVED_12600` | 12600 | current 81-row workbook control; four charged p9,g0 values retained |
| `SHEET81_P9G0_REMOVED_12550P5` | 12550.5 | 81-row workbook after specifically zeroing/removing the remaining four charged p9,g0 values totaling 49.5 |
| `SHEET100_P9G0_REMOVED_16200` | 16200 | current 100-row workbook with all five p9,g0 values absent |

The runner must reconstruct the three spreadsheet sums from the hash-matched row extractions and fail closed on disagreement.

## Frozen binding data and split

Input: `CR242_binding_dataset.csv`.

- Training: exactly the existing `train_cr240_lane_a_non_anchor` rows.
- Holdout: exactly the existing `test_cr241_holdout` rows.
- No holdout target may enter coefficient fitting, scenario selection, signs, thresholds, or feature construction.
- Binding target remains `B_u = A - m_measured` in atomic-mass units.
- Magnitudes are also reported in MeV using the frozen CR277 conversion `1 u = 931.49410242 MeV`.

## Frozen CR242 typed basis

For each scenario value `M_s`, recompute exactly:

```text
1
A / (S M_s)
A^(2/3) / (R V)
Z(Z - 1) / (A^(1/3) S M_s V)
(N - Z)^2 / (A S Theta)
pairing_sign / (M_s sqrt(A))
((Z - 1) mod R) / (R M_s)
abs(N - Z) / (A R)
```

with frozen `R=12`, `S=8`, `Theta=18`, and `V=27`.

## Three predeclared evaluation surfaces

### Surface A — frozen-coefficient transfer

Use the existing CR242 `SAM_TYPED_BASIS_FIT` coefficients unchanged. Only the `M`-bearing feature magnitudes are recomputed for each scenario. This directly measures what happens if the new sums are substituted into the existing fitted surface without compensation.

### Surface B — training-only refit

Fit the same eight CR242 typed-basis coefficients by ordinary least squares on the frozen 49-row training set separately for each scenario, then score the untouched holdout. This determines whether a new sum supplies any new predictive shape after coefficient scaling is allowed.

### Surface C — fixed zero-free magnitude surface

Evaluate the existing CR242 diagnostic without fitted coefficients:

```text
B_zero(M_s) =
  A / (S M_s)
  - A^(2/3) / (R V)
  - Z(Z - 1) / (A^(1/3) S M_s V)
  - (N - Z)^2 / (A S Theta)
  + pairing_sign / (M_s sqrt(A))
```

This is a magnitude sensitivity control, not a promoted binding model.

## Metrics

For training and holdout, report:

- RMS residual in `u` and MeV;
- MAE in `u` and MeV;
- maximum absolute residual in `u` and MeV;
- signed bias in `u` and MeV;
- holdout delta relative to the same surface at `M=126`.

Direction classification uses holdout RMS MeV:

- `IMPROVED` if `baseline_RMS_MeV - candidate_RMS_MeV > 1e-9`;
- `UNCHANGED` if the absolute delta is at most `1e-9`;
- `WORSE` otherwise.

`material_improvement = true` requires both:

1. holdout RMS improvement of at least `0.01 MeV`; and
2. holdout MAE no worse than the same surface at `M=126` by more than `1e-9 MeV`.

Every scenario is reported. No best-scenario selection may suppress an adverse result.

## Reproduction and rank gates

1. The `M=126` training-only refit must reproduce CR242's published SAM typed train and holdout RMS within `1e-12 u`.
2. The `M=126` zero-free surface must reproduce CR242's published zero-free train and holdout RMS within `1e-12 u`.
3. The training and holdout row counts must remain 49 and 20.
4. For each refit scenario, report design rank and predictions.
5. A global column containing only `16200`, `12600`, `12550.5`, `50.625`, `49.5`, or `3600` on every isotope is an exact scalar multiple of the intercept and is rejected as an independent feature.

## Wrong controls

The following fail the test:

1. dividing a roster sum by any row count and using the result as the tested figure;
2. using the word mean or silently normalizing `16200`, `12600`, or `12550.5`;
3. fitting any coefficient on the holdout;
4. choosing only favorable isotopes, residual signs, mass regions, or scenarios;
5. inventing nuclear multiplicities or an isotope-to-QP093A map;
6. using qA, `1/9`, W9 identity, all-depth p9, or any relation outside the five-row `g=0` scope;
7. treating the as-saved 12600 roster as if its four charged p9,g0 values were already removed;
8. changing the existing CR242 result, coefficients, dataset, split, or verdict;
9. calling a rescaled fitted coefficient a new physical binding magnitude;
10. claiming improvement from training error alone.

## Verdict grammar

Each scenario/surface receives `IMPROVED`, `UNCHANGED`, or `WORSE`, plus a material-improvement flag.

Overall:

- `PASS_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT` if either p9,g0-removed scenario (`12550.5` or `16200`) achieves material holdout improvement on Surface A or Surface C;
- `PASS_NO_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT` if neither does and every gate passes;
- `BOUNDARY_MIXED_BINDING_MAGNITUDE_RESPONSE` if RMS and MAE criteria conflict materially;
- `FAIL_INVALID_BINDING_MAGNITUDE_COMPARISON` if a source, split, reproduction, scope, or leakage gate fails.

Surface B is an invariance/information diagnostic and cannot by itself earn the positive overall verdict.

## Fixed outputs

- `CR120Q_scale_scenarios.csv`
- `CR120Q_metrics.csv`
- `CR120Q_predictions.csv`
- `CR120Q_coefficients.csv`
- `CR120Q_rank_controls.json`
- `CR120Q_wrong_controls.json`
- `CR120Q_summary.json`
- `CR120Q_result.md`
- `HASHES.txt`

No CR120Q runner output was consulted in freezing this precommit.
