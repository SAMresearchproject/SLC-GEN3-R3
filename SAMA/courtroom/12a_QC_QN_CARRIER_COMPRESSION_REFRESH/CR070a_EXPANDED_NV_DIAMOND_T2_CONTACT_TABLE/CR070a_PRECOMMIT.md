# CR070a - Expanded NV-Diamond T2 Contact Table - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR070a is the first CR in the campaign)
**Test class:** EXPANDED_NV_DIAMOND_T2_CONTACT_TABLE_AGAINST_T2_GRAV_V1_1
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR070a expands the CR069a 8-row T2 contact table by **deepening the
NV-diamond population**. CR069a had 4 NV-diamond rows mixed with 4
other-platform rows (transmon, ion, optical clock); CR070a is
NV-diamond-only, targeting 20-30 rows from a deeper literature pass.

This CR is **the first of six** in the Paul Revere Field Comparison
Campaign (see
`../CAMPAIGN_PAUL_REVERE_FIELD_COMPARISON.md` for the full campaign
scope, locked decisions, and per-CR roles).

CR070a does NOT introduce any new prediction beyond the CR064a/CR069a
T2_grav v1.1 floor. It expands the empirical surface against which
the floor is tested. Other-platform rows from CR069a are not carried
forward into this CR; they belong to CR072a (photonic) or to later
campaigns (trapped-ion, superconducting).

## The T2_grav v1.1 formula (inherited from CR064a, unchanged)

```text
T2_grav(omega) = 16 * pi * R^4 / (17 * omega) = 16 * pi * 20736 / (17 * omega)
              ~= 6.13e4 / omega seconds      (with omega in rad/s)
```

At NV-resonant drive (omega = 2*pi*2.87 GHz = 1.8033e10 rad/s),
T2_grav ~= 3.40 us. The expanded NV-diamond population will sit
across the floor: ultralong-coherence cryo+isotopically-purified rows
deep above the floor, room-temperature Hahn-echo natural-abundance
rows at or near the floor, with some likely VIOLATION rows reported
honestly (matching CR069a's pattern where row 4 violated).

## Inputs

```text
CR064a (T2_grav v1.1 formula)        - upstream lock, not modified
CR069a (initial 8-row table)         - source of the 4 inherited NV
                                       rows; runner reads CR069a
                                       hashes and re-uses the 4 NV
                                       rows verbatim
Published NV-diamond T2 literature   - additional rows tagged
                                       PROVISIONAL_AUTHOR_BEST_EFFORT
```

Foundation primitives (unchanged):

```text
R       = 12
D       = 3
alpha_H = 2
```

## Predictions

- **P1_table_well_formed**
  Each row has all required fields (row_id, platform, citation_tag,
  drive_frequency_label, omega_drive_rad_per_s, T2_observed_s,
  conditions, verify_status, notes, plus the NV-diamond-specific
  fields sample_type, decoupling_protocol, temperature_K).

- **P2_no_current_measurement_violates_T2_grav**
  For every populated row, T2_observed > T2_grav at the row's
  omega_drive. (Floor not currently violated.) Likely to fail
  honestly: room-temperature Hahn-echo NV T2 in natural-abundance
  diamond typically sits at 1-5 us, near or below the 3.4 us
  NV-resonant floor. CR069a's Childress 2006 row already fired this
  failure; CR070a's expanded NV population is expected to surface
  more such rows.

- **P3_margin_distribution_consistent_with_environmental_dominance**
  Median margin (T2_observed / T2_grav) across populated rows is
  >> 1. Confirms most current measurements are environmental-noise-
  limited, not at the gravitational floor.

- **P4_cryo_DD_NV_closest_to_floor_in_relative_terms**
  Of the populated rows, cryo + DD + isotopically-purified rows
  (Bar-Gill 2013, Abobeih 2018 class) should have the highest
  absolute T2 but are still many orders of magnitude above the
  floor, indicating engineering distance from the gravitational
  limit.

- **P5_no_free_parameters_in_contact_analysis**
  T2_grav is computed only from R, D, alpha_H per the v1.1 formula.
  T2_observed comes from published measurements (tagged). No fitting
  parameter introduced.

- **P6_explicit_verification_path_documented**
  Every row carries a citation tag and a verify_status field
  PROVISIONAL_AUTHOR_BEST_EFFORT. Partner-lab confirmation of each
  citation lifts the row to VERIFIED.

- **P7_contact_table_emitted_with_consistency_classification**
  CSV output groups rows by status (CONSISTENT_WITH_FLOOR /
  VIOLATION_OF_FLOOR / BOUNDARY_AT_FLOOR / INVALID).

- **P8_protocol_completes_end_to_end**
  Runner reads input table, computes T2_grav per row, emits
  residuals, writes outputs without runtime error.

- **P9_row_count_meets_campaign_threshold**
  Total NV-diamond rows >= 15 (the campaign-doc threshold). PASS at
  15+, BLOCKER below 15. Honest report of actual count in
  result_class.

- **P10_no_regression_against_CR069a_inherited_rows**
  The 4 NV-diamond rows inherited from CR069a produce identical
  classifications (CONSISTENT / BOUNDARY / VIOLATION) in CR070a as
  they did in CR069a. Any difference signals an upstream change or
  runner discrepancy.

- **P11_sample_diversity**
  The populated NV-diamond rows cover at least 3 of these
  categories: {natural-abundance 13C, isotopically-purified 12C,
  ensemble vs single, cryogenic, room-temperature, distinct
  dynamical-decoupling protocols, shallow/surface vs bulk,
  nanodiamond vs bulk}. Demonstrates the expanded surface tests the
  floor across NV experimental regimes, not just one slice.

- **P12_all_rows_are_NV_diamond**
  Every row's platform field is NV_center_diamond. CR070a is
  NV-only; non-NV rows belong to CR072a (photonic) or later
  campaigns.

## Wrong controls

- **WC1_inverted_formula_falsely_flags_violations**
  Same as CR069a WC1: confirm real T2_grav has discriminating power
  vs inverted formula.

- **WC2_zero_omega_breaks_the_formula_gracefully**
  Same as CR069a WC2.

- **WC3_negative_T2_observed_rejected_as_unphysical**
  Same as CR069a WC3.

- **WC4_no_citation_tag_marks_row_as_provisional**
  Same as CR069a WC4.

- **WC5_runner_does_not_modify_upstream_locks**
  Same as CR069a WC5. CR069a is read-only; CR064a is read-only.

- **WC6_no_free_parameters**
  Same as CR069a WC6.

- **WC7_non_NV_row_rejected**
  CR070a is NV-diamond-only per campaign scope. A test row with
  platform != "NV_center_diamond" is rejected at input
  validation, not silently passed through.

- **WC8_cr069a_inherited_row_hash_mismatch_detected**
  If any of the 4 inherited NV rows from CR069a are loaded with
  values that differ from CR069a's frozen table, runner halts with
  a structured error rather than producing inconsistent output.

## Outputs

```text
CR070a_expanded_nv_t2_table.csv   - input: 20-30 NV-diamond rows (tagged PROVISIONAL)
CR070a_contact_analysis.csv       - output: per-row T2_grav + classification
CR070a_contact_plot.png           - log-log scatter T2_observed vs T2_grav
CR070a_runner.py                  - the contact analyzer
CR070a_summary.json               - pass/fail per prediction and wrong control
CR070a_result.md                  - human-readable
HASHES.txt
```

## Falsifiers

- Inability to populate >= 15 NV-diamond rows from published
  literature would force CR070a to remain at BLOCKER status until
  the input table is expanded.
- Any inherited CR069a NV row producing a classification change in
  CR070a would force a CR069a vs CR070a runner reconciliation
  before CR070a can be sealed.
- Any populated row with platform != "NV_center_diamond" would be
  rejected and the row count would not include it; CR070a is
  NV-diamond-only.

## Free parameters

```text
free_parameters = 0
```

## Honest expected outcome at CR070a seal

CR070a is expected to surface multiple VIOLATION rows because
room-temperature Hahn-echo NV T2 in natural-abundance diamond
naturally sits at or below the 3.4 us T2_grav floor. The honest
aggregate verdict will likely be "PARTIAL CONSISTENCY: most rows
sit far above the floor; a non-trivial subset of room-temperature
Hahn-echo rows fall at or below the floor, indicating either (a)
the T2_grav floor is environmentally accessible at room temperature
without dynamical decoupling, or (b) the published Hahn-echo T2
values do not represent the strict T2 in the SAM-floor sense."

This is the honest reading. CR070a does not pass the table; it
populates the table and reports what's there.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution.
Modifications to predictions, wrong controls, or scope after runner
output require a new CR.
