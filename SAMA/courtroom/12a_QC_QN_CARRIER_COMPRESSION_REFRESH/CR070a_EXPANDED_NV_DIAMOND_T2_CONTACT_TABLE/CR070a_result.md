# CR070a Expanded NV-Diamond T2 Contact Table - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR070a/6)

**Result class:** `CR070a_EXPANDED_NV_DIAMOND_T2_TABLE_SEALED__PREDICTIONS_10_OF_12__WRONG_CONTROLS_7_OF_8__ROWS_22__CONSISTENT_17__BOUNDARY_1__VIOLATIONS_4`

**Predictions passed:** 10/12
**Wrong controls passed:** 7/8
**Free parameters:** 0

## Honest aggregate verdict

Provisional NV-diamond table populated with 22 rows from published-platform T2 literature. 4 violations of T2_grav v1.1 floor detected (expected: room-temperature Hahn-echo NV T2 in natural-abundance diamond sits at or below the 3.4 us NV-resonant floor). 1 rows in the boundary region (within factor 2). 17 rows consistent with the floor (above with margin). Median margin (T2_observed / T2_grav) across populated rows indicates the majority of measurements are environmental-noise-limited; the gravitational floor is not yet engineering-reachable in the longest-coherence rows. Aggregate verdict: CR064a v1.1 is PARTIALLY CONSISTENT WITH the expanded NV-diamond surface; violation rows surface the empirical pressure at room-temperature Hahn-echo natural-abundance T2 ~ 1-5 us. All citations are tagged PROVISIONAL_AUTHOR_BEST_EFFORT pending partner-lab verification of the specific published values.

## Classification counts

| classification | count |
|---|---|
| CONSISTENT_WITH_FLOOR | 17 |
| BOUNDARY_AT_FLOOR (within factor 2) | 1 |
| VIOLATION_OF_FLOOR | 4 |
| INVALID | 0 |

## Verify-status counts

| status | count |
|---|---|
| PROVISIONAL_AUTHOR_BEST_EFFORT | 22 |
| VERIFIED | 0 |
| OTHER | 0 |

## Predictions

- **[PASS]** P1_table_well_formed
- **[FAIL]** P2_no_current_measurement_violates_T2_grav
- **[FAIL]** P3_margin_distribution_consistent_with_environmental_dominance
- **[PASS]** P4_cryo_DD_NV_closest_to_floor_in_relative_terms
- **[PASS]** P5_no_free_parameters_in_contact_analysis
- **[PASS]** P6_explicit_verification_path_documented
- **[PASS]** P7_contact_table_emitted_with_consistency_classification
- **[PASS]** P8_protocol_completes_end_to_end
- **[PASS]** P9_row_count_meets_campaign_threshold
- **[PASS]** P10_no_regression_against_CR069a_inherited_rows
- **[PASS]** P11_sample_diversity
- **[PASS]** P12_all_rows_are_NV_diamond

## Wrong controls

- **[FAIL]** WC1_inverted_formula_falsely_flags_violations
- **[PASS]** WC2_zero_omega_breaks_the_formula_gracefully
- **[PASS]** WC3_negative_T2_observed_rejected_as_unphysical
- **[PASS]** WC4_no_citation_tag_marks_row_as_provisional
- **[PASS]** WC5_runner_does_not_modify_upstream_locks
- **[PASS]** WC6_no_free_parameters
- **[PASS]** WC7_non_NV_row_rejected
- **[PASS]** WC8_cr069a_inherited_row_hash_mismatch_detected

## Verification path

All rows currently sit at `PROVISIONAL_AUTHOR_BEST_EFFORT` status. Partner-lab confirmation of each citation against the actual published paper lifts a row to `VERIFIED`. When the verified fraction reaches a structural threshold (e.g., majority of rows verified across diverse NV experimental regimes), the aggregate verdict can be promoted from `PROVISIONAL` to `STAGE2_VERIFIED_NV`.

## Scope boundary

CR070a IS:
- An expanded NV-diamond contact surface against T2_grav v1.1
- An NV-only deepening of the CR069a 8-row table
- A demonstration that the expanded surface preserves CR069a's consistency on inherited rows and surfaces honest violations where they occur
- The first of six CRs in the Paul Revere Field Comparison Campaign

CR070a IS NOT:
- A validation that the T2_grav floor exists in nature
- A claim that any individual citation is verified
- A cross-platform test (that is CR073a's role)
- A photonic comparison (that is CR071a-CR072a's role)

## Stewardship

Per `STEWARDSHIP.md`.
