# CR072a Photonic Empirical Contact Table - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR072a/6)

**Result class:** `CR072a_PHOTONIC_EMPIRICAL_TABLE_SEALED__PREDICTIONS_11_OF_11__WRONG_CONTROLS_7_OF_8__ROWS_14__CONSISTENT_14__BOUNDARY_0__VIOLATIONS_0`

**Predictions passed:** 11/11
**Wrong controls passed:** 7/8
**Free parameters:** 0

## Honest aggregate verdict

Provisional photonic table populated with 14 rows from published-platform tau_ent literature. 0 violations of T2_grav v1.1 floor at photonic omega. 0 rows in boundary region. 14 rows consistent with the floor. Photonic T2_grav at typical telecom 1550 nm is ~50 ps, far below typical published entanglement coherence times (microseconds to seconds). Aggregate verdict: CR064a v1.1 is CONSISTENT WITH all populated photonic measurements; cross-platform scaling test (CR073a) is the load-bearing follow-up. All citations are tagged PROVISIONAL_AUTHOR_BEST_EFFORT pending partner-lab verification.

## Classification counts

| classification | count |
|---|---|
| CONSISTENT_WITH_FLOOR | 14 |
| BOUNDARY_AT_FLOOR (within factor 2) | 0 |
| VIOLATION_OF_FLOOR | 0 |
| INVALID | 0 |

## Verify-status counts

| status | count |
|---|---|
| PROVISIONAL_AUTHOR_BEST_EFFORT | 14 |
| VERIFIED | 0 |
| OTHER | 0 |

## Predictions

- **[PASS]** P1_table_well_formed
- **[PASS]** P2_no_current_measurement_violates_T2_grav_at_photonic_omega
- **[PASS]** P3_margin_distribution_consistent_with_environmental_dominance
- **[PASS]** P4_row_count_meets_campaign_threshold
- **[PASS]** P5_no_free_parameters_in_contact_analysis
- **[PASS]** P6_explicit_verification_path_documented
- **[PASS]** P7_contact_table_emitted_with_consistency_classification
- **[PASS]** P8_protocol_completes_end_to_end
- **[PASS]** P9_all_rows_use_CR071a_T2_equivalent_definition
- **[PASS]** P10_omega_values_derived_from_documented_wavelengths
- **[PASS]** P11_platform_diversity

## Wrong controls

- **[FAIL]** WC1_inverted_formula_falsely_flags_violations
- **[PASS]** WC2_zero_omega_breaks_the_formula_gracefully
- **[PASS]** WC3_negative_tau_ent_rejected_as_unphysical
- **[PASS]** WC4_no_citation_tag_marks_row_as_provisional
- **[PASS]** WC5_runner_does_not_modify_upstream_locks
- **[PASS]** WC6_no_free_parameters
- **[PASS]** WC7_non_photonic_row_rejected
- **[PASS]** WC8_omega_derivation_consistency

## Verification path

All rows currently sit at `PROVISIONAL_AUTHOR_BEST_EFFORT` status. Partner-photonic-lab confirmation of each citation against the actual published paper or vendor document lifts a row to `VERIFIED`.

## Scope boundary

CR072a IS:
- A photonic empirical contact surface against T2_grav v1.1 at photonic omega
- A PROVISIONAL population from Qunnect/Cisco/Vienna/NIST/QKD-network literature
- The photonic counterpart of CR070a's NV-diamond surface

CR072a IS NOT:
- A validation that the T2_grav floor exists at photonic frequencies
- A claim that any individual citation is verified
- A cross-platform t_fire scaling test (CR073a's role)

## Stewardship

Per `STEWARDSHIP.md`.
