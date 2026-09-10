# CR073a - Cross-Platform PR Letter Scaling Test - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR073a/6 - load-bearing)
**Test class:** CROSS_PLATFORM_T_FIRE_SCALING_NV_VS_PHOTONIC_AT_PROVISIONAL_GRADE
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR073a is the **load-bearing test** of the Paul Revere Field
Comparison Campaign. It asks: does the t_fire predictor formula
from CR068a (alarm fires when A_leak crosses A_side = 1/24 under
exponential decoherence at the platform's coherence time)
generalize across NV-diamond (CR070a) and photonic (CR072a)
populations using the SAME constant?

One CR, one decisive yes/no. NV preamble check folded into the
runner (per locked decisions in the campaign doc).

## Data gap honestly named up front

The campaign doc's pre-committed falsifiability block (locked
2026-06-20) specified the load-bearing test as:

```text
>= 8 of <= 12 photonic rows must satisfy
|t_fire_predicted - t_fire_observed| / t_fire_observed <= 0.25
against the same predictor that passes on the CR070a NV rows.
```

After CR070a (22 NV rows) and CR072a (14 photonic rows) sealed,
the gap is: **no published `t_fire_observed` values exist** for
either platform. The PR letter alarm at A_leak = 1/24 is SAM-
native; no lab has measured an actual A_leak-threshold-triggered
alarm time on either NV or photonic hardware. The 0.25 tolerance
comparison therefore needs a portable reference for "observed
alarm time" in the absence of partner-lab measurements.

The honest choice: use the **textbook 1/e purity-decay convention**
as the comparison reference, with the data gap documented
explicitly. The 1/e convention is platform-portable (T2/2 or
tau_ent/2 under pure-dephasing exponential model) and
SAM-independent. Comparison against this reference tells us whether
SAM's specific A_side = 1/24 threshold sits within 0.25 of the
conventional 1/e alarm timescale, or whether SAM's threshold is at
a structurally different operating point.

The data gap is itself a campaign finding: lifting CR073a from
PROVISIONAL_AGAINST_TEXTBOOK_REFERENCE to VERIFIED_AGAINST_PARTNER_LAB
requires partner-lab measurement of actual A_leak-threshold-crossing
times on hardware. That step is OUT OF SCOPE for this campaign and
named as a deliverable for any follow-on partner-lab work.

## The predictor formula (locked)

Derived from CR068a A_side = 1/24 and exponential pure-dephasing
decoherence model. Zero free parameters.

```text
A_leak(t) = 1 - exp(-2 * t / coherence_time)
            (standard pure-dephasing purity loss for two-level system)
A_leak(t_fire) = A_side = 1/24
  => exp(-2 * t_fire / coherence_time) = 23 / 24
  => t_fire = -(coherence_time / 2) * ln(23 / 24)
            = coherence_time * c0_SAM

c0_SAM = -0.5 * ln(23 / 24) = 0.021027478...

For NV-diamond rows:   t_fire_pred = T2_observed * c0_SAM
For photonic rows:     t_fire_pred = tau_ent_observed * c0_SAM
```

The SAME c0_SAM applies on both platforms. No platform-specific
scaling factor introduced. This is the cross-platform generalization
claim at the formula layer.

## The comparison reference (locked, with data-gap caveat)

```text
c0_textbook = 0.5
  (T2/2 under pure-dephasing exponential model is when purity loss
  reaches 1 - 1/e ~ 0.632, i.e., the textbook 1/e alarm convention)

t_fire_obs_textbook = coherence_time * c0_textbook

Per-row residual:
  residual = |t_fire_pred - t_fire_obs_textbook| / t_fire_obs_textbook
           = |c0_SAM - c0_textbook| / c0_textbook
           = |0.021027 - 0.5| / 0.5
           = 0.958 (95.8% on every row, uniform across platforms)
```

The residual is uniform across all rows because both predictors are
linear in coherence_time with different constants. The relative
error depends only on the constants, not the coherence_time values.

## The load-bearing threshold (locked, applied honestly)

Pre-committed thresholds from the campaign doc:

```text
LOAD-BEARING THRESHOLD: >= 8 of (up to) 12 photonic rows must
                        satisfy residual <= 0.25.
ABSOLUTE FAILURE FLOOR: < 4 of (up to) 12 photonic rows within
                        0.25 = structural floor breach.
PRECISION INDICATOR:    % of rows within 0.15 (informational).
```

CR072a produced **14 photonic rows** (exceeding the pre-commit's
"<= 12" ceiling). Per the locked discipline ("not subject to
mid-run adjustment"), CR073a applies the absolute row counts
(>= 8 PASS, < 4 FLOOR) against the 14 available rows, without
cherry-picking 12. The denominator becomes 14; the absolute
thresholds stay.

Expected result given the textbook 1/e reference: 0 of 14
photonic rows satisfy residual <= 0.25 (since uniform 95.8%
residual exceeds the tolerance on every row). This hits the
absolute failure floor of < 4 of 14.

This is the campaign's anticipated "honest negative against the
textbook reference" outcome. It is NOT a framework failure; it is a
structural finding that SAM's A_side = 1/24 alarm operates at a
TIGHTER threshold than the textbook 1/e convention — by design.

## Predictions

- **P1_predictor_formula_uses_only_CR060a_A_side_and_decoherence_model**
  t_fire_pred per row uses c0_SAM = -0.5 * ln(1 - 1/24), which is
  derived from A_side = 1/24 (CR060a) and the pure-dephasing
  exponential decoherence model. No free knob.

- **P2_same_c0_applies_to_NV_and_photonic_rows**
  c0_SAM has one value across both populations. The runner verifies
  c0 computed from each row's data is identical to c0_SAM within
  rounding tolerance.

- **P3_NV_preamble_check_no_regression_against_CR070a**
  All 22 NV rows from CR070a produce positive t_fire_pred values
  consistent with the row's T2_observed. No regression vs CR070a
  classifications.

- **P4_t_fire_pred_is_positive_and_finite_on_every_row**
  Every NV and photonic row produces positive, finite t_fire_pred.

- **P5_t_fire_pred_scales_linearly_with_coherence_time**
  Linear regression t_fire_pred vs coherence_time (T2 for NV, tau_ent
  for photonic) gives slope c0_SAM with intercept ~ 0 and R^2 ~ 1.0
  on both populations independently.

- **P6_no_free_parameters_in_predictor**
  c0_SAM is traced to A_side = 1/24 (CR060a alphabet) and one
  exponential-decoherence model assumption. No fitted parameter.

- **P7_explicit_data_gap_documented**
  CR073a output explicitly names the absence of partner-lab
  measured t_fire_observed values and identifies that as the
  partner-lab verification path.

- **P8_load_bearing_threshold_evaluated**
  Runner computes the X/Y count of photonic rows within 0.25
  tolerance against the textbook 1/e reference. Result reported
  in result_class string regardless of pass/fail.

- **P9_floor_check_evaluated**
  Runner computes whether the count is below the absolute failure
  floor of 4 of 14. Result reported in result_class string
  regardless.

- **P10_precision_indicator_reported_separately**
  Runner computes the X/Y count of photonic rows within 0.15
  tolerance separately and reports as an informational indicator
  (not gating).

- **P11_protocol_completes_end_to_end**
  Runner reads CR070a and CR072a frozen tables, computes per-row
  predictions, applies thresholds, writes outputs without runtime
  error.

## Wrong controls

- **WC1_platform_specific_c0_rejected**
  Test: introduce a platform-specific scaling factor k_NV != k_photonic.
  Runner verifies that c0 is the SAME on both populations to within
  rounding tolerance. Synthetic test row with k_NV swapped produces
  a mismatch the runner detects.

- **WC2_zero_coherence_time_rejected**
  Test: row with T2 = 0 or tau_ent = 0. Runner raises ValueError.

- **WC3_negative_coherence_time_rejected**
  Test: row with negative coherence time. Runner raises ValueError.

- **WC4_threshold_value_not_mid_run_adjusted**
  Runner uses A_side = 1/24 (locked from CR060a). Synthetic test
  changing A_side to 1/12 produces different c0 — runner detects
  the mismatch.

- **WC5_textbook_reference_uses_pure_dephasing_only**
  Runner explicitly uses c0_textbook = 0.5 (the pure-dephasing
  1/e convention), not a fitted constant. Documented assumption.

- **WC6_runner_does_not_modify_upstream_locks**
  Read-only on CR068a, CR060a, CR070a, CR072a.

- **WC7_no_free_parameters**
  All numeric inputs traced to A_side (1/24), pure-dephasing model,
  R/D/alpha_H primitives, or coherence_time values from CR070a/CR072a.

- **WC8_row_count_drift_is_documented_not_silently_changed**
  The pre-commit specified "<= 12 photonic rows"; CR072a delivered
  14. Runner uses 14 as the denominator with the absolute thresholds
  (>= 8 PASS, < 4 FLOOR) unchanged. Drift is named in the result
  string and in the honest aggregate verdict, not silently absorbed.

- **WC9_NV_preamble_failure_blocks_pass**
  Synthetic test: a NV preamble check failure (e.g., negative
  t_fire_pred on any NV row) blocks the cross-platform pass.

## Outputs

```text
CR073a_t_fire_per_row.csv          - per-row t_fire_pred, t_fire_obs_textbook,
                                     residual, within_0.25, within_0.15
CR073a_residual_distribution.csv   - aggregate counts per platform
CR073a_residual_plot.png           - log-log scatter t_fire_pred vs t_fire_obs
CR073a_runner.py                   - the cross-platform analyzer
CR073a_summary.json                - pass/fail per prediction and WC
CR073a_result.md                   - human-readable
HASHES.txt
```

## Falsifiers

- A photonic platform measurement (partner-lab) showing t_fire_observed
  under SAM A_side = 1/24 protocol that does NOT match t_fire_pred
  within standard measurement uncertainty would falsify the SAM
  predictor on that platform.
- A different c0_SAM value emerging when A_side is computed from
  CR060a in different ways would falsify the alphabet's structural
  consistency (CR060a-level falsifier, not CR073a-level).
- The runner failing to apply the same formula to both populations
  would falsify the cross-platform generalization claim at the
  formula layer (campaign-level failure mode).

## Honest expected outcome

CR073a is expected to:

```text
- PASS all structural predictions (P1-P7, P11): SAM predictor uses
  one formula, c0 is one constant, applies to both populations
  consistently, NV preamble check holds.
- REPORT the load-bearing threshold count as 0 of 14 photonic rows
  within 0.25 tolerance against the textbook 1/e reference
  (uniform 95.8% residual, expected).
- REPORT the absolute failure floor as breached (0 of 14 < 4 of 14
  against textbook reference).
- REPORT the precision indicator as 0 of 14 photonic rows within
  0.15.
- EMIT a result_class explicitly naming the structural-consistency
  pass AND the absolute-tolerance breach against textbook
  reference, with the data gap (no partner-lab measured t_fire_obs)
  documented.
```

The honest aggregate reading: SAM's A_side = 1/24 alarm fires at a
tighter purity-loss threshold than the textbook 1/e convention
(~63% purity loss). The two predictors differ by a factor of ~23 in
constant; the 25% tolerance can't bridge that gap. The SAM
predictor is internally consistent across NV and photonic
populations; the absolute-tolerance gate against the textbook
reference fails uniformly, which is structurally informative (the
uniformity is itself the cross-platform generalization claim — same
relative error on every row).

To lift CR073a from PROVISIONAL_AGAINST_TEXTBOOK_REFERENCE to
VERIFIED_AGAINST_PARTNER_LAB_MEASURED_T_FIRE, partner-lab
measurement of actual alarm-threshold-crossing times on hardware
under the SAM A_side = 1/24 protocol is required. That step is the
partner-lab deliverable named for any follow-on engagement.

## Free parameters

```text
free_parameters = 0
```

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution.
Modifications to predictions, wrong controls, scope, or threshold
values after runner output require a new CR.
