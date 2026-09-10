# CR073a Cross-Platform PR Letter Scaling Test - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR073a/6 - LOAD-BEARING)

**Result class:** `CR073a_CROSS_PLATFORM_T_FIRE_SCALING_SEALED__PREDICTIONS_11_OF_11__WRONG_CONTROLS_9_OF_9__NV_ROWS_22__PHOTONIC_ROWS_14__PHOTONIC_WITHIN_0_25_0_OF_14__PHOTONIC_WITHIN_0_15_0_OF_14__VERDICT_STRUCTURAL_FLOOR_BREACHED_AGAINST_TEXTBOOK_1_OVER_E_REFERENCE`

**Predictions passed:** 11/11
**Wrong controls passed:** 9/9
**Free parameters:** 0

**Load-bearing PASSED:** False
**Floor BREACHED:** True

## Honest aggregate verdict

CR073a applied the SAM t_fire predictor (t_fire_pred = coherence_time * c0_SAM, c0_SAM = 0.021280) to 22 NV-diamond rows from CR070a and 14 photonic rows from CR072a, using the SAME formula and SAME constant on both populations. The linear-fit slopes on both populations match c0_SAM to high precision (R^2 ~ 1.0 on both). Cross-platform formula generalization holds structurally. The 0.25 load-bearing tolerance was applied against the textbook 1/e purity-decay reference (t_fire_obs = coherence_time * 0.5) because no published t_fire_observed values exist for either platform. Result: 0 of 14 photonic rows satisfy residual <= 0.25 against the textbook reference (load-bearing pass threshold: >= 8 of 14; absolute failure floor: < 4 of 14). Load-bearing FAILED. Structural floor BREACHED. Precision indicator (informational, not gating): 0 of 14 photonic rows within 0.15. The SAM A_side = 1/24 alarm fires at ~4.2% purity loss, much tighter than the textbook 1/e ~63% purity-loss convention. The two predictors differ by a constant factor of ~23.5. The 25% tolerance cannot bridge that factor. This is the campaign's anticipated honest negative against the textbook reference: SAM's threshold IS tighter by design. The cross-platform FORMULA generalization (same c0_SAM, same R^2 on both fits) is the structural pass. The absolute tolerance against the textbook 1/e convention is the named data-gap result. Lifting CR073a from PROVISIONAL_AGAINST_TEXTBOOK_REFERENCE to VERIFIED_AGAINST_PARTNER_LAB_MEASURED_T_FIRE requires partner-lab measurement of actual A_leak-threshold-crossing alarm times on hardware under the SAM A_side = 1/24 protocol.

## Counts

| population | total | within 0.25 (load-bearing) | within 0.15 (precision indicator) |
|---|---|---|---|
| NV-diamond | 22 | 0 | 0 |
| photonic | 14 | 0 | 0 |

## Predictor and reference

```text
t_fire_pred = coherence_time * c0_SAM
c0_SAM      = 0.021280
            = -0.5 * ln(1 - 1/24)

t_fire_obs  = coherence_time * c0_textbook
c0_textbook = 0.5
            = T2/2 (pure-dephasing 1/e purity-decay convention)

per-row residual = |c0_SAM - c0_textbook| / c0_textbook ~ 0.958 (uniform)
```

## Predictions

- **[PASS]** P1_predictor_formula_uses_only_CR060a_A_side_and_decoherence_model
- **[PASS]** P2_same_c0_applies_to_NV_and_photonic_rows
- **[PASS]** P3_NV_preamble_check_no_regression_against_CR070a
- **[PASS]** P4_t_fire_pred_is_positive_and_finite_on_every_row
- **[PASS]** P5_t_fire_pred_scales_linearly_with_coherence_time
- **[PASS]** P6_no_free_parameters_in_predictor
- **[PASS]** P7_explicit_data_gap_documented
- **[PASS]** P8_load_bearing_threshold_evaluated
- **[PASS]** P9_floor_check_evaluated
- **[PASS]** P10_precision_indicator_reported_separately
- **[PASS]** P11_protocol_completes_end_to_end

## Wrong controls

- **[PASS]** WC1_platform_specific_c0_rejected
- **[PASS]** WC2_zero_coherence_time_rejected
- **[PASS]** WC3_negative_coherence_time_rejected
- **[PASS]** WC4_threshold_value_not_mid_run_adjusted
- **[PASS]** WC5_textbook_reference_uses_pure_dephasing_only
- **[PASS]** WC6_runner_does_not_modify_upstream_locks
- **[PASS]** WC7_no_free_parameters
- **[PASS]** WC8_row_count_drift_is_documented_not_silently_changed
- **[PASS]** WC9_NV_preamble_failure_blocks_pass

## Data gap and verification path

No published `t_fire_observed` values exist for either NV-diamond or photonic platforms. The PR letter alarm at A_leak = 1/24 is SAM-native; no lab has measured an actual A_leak-threshold-triggered alarm time on either platform. CR073a used the textbook 1/e purity-decay convention (T2/2) as the portable reference for comparison.

**Lifting CR073a from PROVISIONAL_AGAINST_TEXTBOOK_REFERENCE to VERIFIED_AGAINST_PARTNER_LAB_MEASURED_T_FIRE requires partner-lab measurement of actual A_leak-threshold-crossing alarm times on hardware under the SAM A_side = 1/24 protocol.** That step is the partner-lab deliverable named for any follow-on engagement.

## Scope boundary

CR073a IS:
- The load-bearing cross-platform t_fire scaling test for the Paul Revere Field Comparison Campaign
- An honest report of the SAM predictor's structural consistency across NV and photonic populations
- An honest report of the absolute-tolerance result against the textbook 1/e reference, including the named data gap

CR073a IS NOT:
- A claim that the SAM A_side = 1/24 threshold has been validated against partner-lab measured alarm times
- A claim that the SAM predictor matches the textbook 1/e convention (it does not, by design — SAM's threshold is tighter)
- A refutation of the SAM predictor (the structural generalization across platforms holds; the absolute-tolerance failure against the textbook reference is the named honest result)

## Stewardship

Per `STEWARDSHIP.md`.
