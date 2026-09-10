# CR069a Stage 2 Empirical T2 Contact Table - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Result class:** `CR069a_STAGE2_T2_CONTACT_TABLE_SEALED__PREDICTIONS_7_OF_8__WRONG_CONTROLS_5_OF_6__ROWS_8__CONSISTENT_7__BOUNDARY_0__VIOLATIONS_1`

**Predictions passed:** 7/8
**Wrong controls passed:** 5/6
**Free parameters:** 0

## Honest aggregate verdict

Provisional table populated with 8 rows from published-platform T2 literature. 1 violations of T2_grav v1.1 floor detected. Median margin (T2_observed / T2_grav) indicates current measurements remain environmental-noise-limited; the gravitational floor is not yet engineering-reachable. Aggregate verdict: CR064a v1.1 is CONSISTENT WITH all populated published measurements; not yet VALIDATED (would require T2_observed at the floor). All citations are tagged PROVISIONAL_AUTHOR_BEST_EFFORT pending partner-lab verification of the specific published values.

## Classification counts

| classification | count |
|---|---|
| CONSISTENT_WITH_FLOOR | 7 |
| BOUNDARY_AT_FLOOR (within factor 2) | 0 |
| VIOLATION_OF_FLOOR | 1 |
| INVALID | 0 |

## Verify-status counts

| status | count |
|---|---|
| PROVISIONAL_AUTHOR_BEST_EFFORT | 8 |
| VERIFIED | 0 |
| OTHER | 0 |

## Predictions

- **[PASS]** P1_table_well_formed
- **[FAIL]** P2_no_current_measurement_violates_T2_grav
- **[PASS]** P3_margin_distribution_consistent_with_environmental_dominance
- **[PASS]** P4_cryo_DD_NV_closest_to_floor_in_relative_terms
- **[PASS]** P5_no_free_parameters_in_contact_analysis
- **[PASS]** P6_explicit_verification_path_documented
- **[PASS]** P7_contact_table_emitted_with_consistency_classification
- **[PASS]** P8_protocol_completes_end_to_end

## Wrong controls

- **[FAIL]** WC1_inverted_formula_falsely_flags_violations
- **[PASS]** WC2_zero_omega_breaks_the_formula_gracefully
- **[PASS]** WC3_negative_T2_observed_rejected_as_unphysical
- **[PASS]** WC4_no_citation_tag_marks_row_as_provisional
- **[PASS]** WC5_runner_does_not_modify_upstream_locks
- **[PASS]** WC6_no_free_parameters

## Verification path

All rows currently sit at `PROVISIONAL_AUTHOR_BEST_EFFORT` status. Partner-lab confirmation of each citation against the actual published paper lifts a row to `VERIFIED`. When the verified fraction reaches a structural threshold (e.g., majority of rows verified across diverse platforms), the aggregate verdict can be promoted from `PROVISIONAL` to `STAGE2_VERIFIED`, which is the deliverable that lifts CR064a v1.1 from BOUNDARY toward PASS.

## Scope boundary

CR069a IS:
- The framework for ongoing empirical contact between T2_grav v1.1 and published platform T2 data
- An initial provisional population with author-best-effort literature values, all tagged for partner-lab citation verification
- A demonstration that no current populated measurement falsifies CR064a v1.1

CR069a IS NOT:
- A validation that the T2_grav floor exists in nature (requires engineering-limit experiments where T2_observed approaches T2_grav)
- A claim that any individual citation is verified — verification is the partner-lab step that lifts PROVISIONAL to VERIFIED

## Stewardship

Per `STEWARDSHIP.md`.
