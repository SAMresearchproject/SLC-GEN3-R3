# CR072a - Photonic Empirical Contact Table - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR072a/6)
**Test class:** PHOTONIC_EMPIRICAL_CONTACT_TABLE_AGAINST_T2_GRAV_V1_1_AT_PHOTONIC_OMEGA
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR072a populates a photonic-platform empirical contact table using
the CR071a mapping (NV-diamond -> photonic). Each row carries a
published-literature value for tau_ent (the photonic T2-equivalent
per CR071a M04), the row's photonic omega_drive (from the operating
wavelength), citation tag, conditions, and verify status. Rows are
classified against T2_grav v1.1 evaluated at the row's photonic
omega using the SAME formula as CR069a/CR070a — only the omega
substitution changes.

CR072a does NOT test cross-platform scaling (that is CR073a's
load-bearing role). CR072a does NOT test or refine the CR071a
mapping itself — it consumes the mapping read-only.

Honest expected outcome: T2_grav at telecom 1550 nm is ~50 ps, far
below typical reported tau_ent values (microseconds to seconds).
Most populated rows are expected to be CONSISTENT_WITH_FLOOR with
large margins. The discipline is to populate and report honestly,
not to engineer near-floor rows.

## Inputs

```text
CR071a (photonic mapping table)         - upstream, not modified
                                          mapping row M04 defines
                                          tau_ent as the photonic
                                          T2-equivalent
CR071a (T2_grav at photonic omega)      - upstream, not modified
                                          provides canonical T2_grav
                                          values at 1550/1310/850 nm
CR064a (T2_grav v1.1 formula)           - upstream, not modified
CR069a (T2 contact table discipline)    - template; CR072a uses the
                                          same classification logic
                                          shape
Published photonic-platform literature   - additional rows tagged
                                          PROVISIONAL_AUTHOR_BEST_EFFORT
                                          (entanglement distribution,
                                          memory T2, link stability,
                                          QKD coherence references)
```

Foundation primitives (unchanged):

```text
R       = 12
D       = 3
alpha_H = 2
```

## The classification rule (identical shape to CR069a/CR070a)

```text
T2_grav(omega) = 16 * pi * R^4 / (17 * omega)
ratio = tau_ent / T2_grav
classification:
  ratio < 1.0                  -> VIOLATION_OF_FLOOR
  1.0 <= ratio < 2.0           -> BOUNDARY_AT_FLOOR
  ratio >= 2.0                 -> CONSISTENT_WITH_FLOOR
```

Same formula, same boundary tolerance (factor 2), same row-level
classifications as CR069a/CR070a. The only thing that changes is
the omega value per row (photonic, not NV-resonant).

## Predictions

- **P1_table_well_formed**
  Each row has all required fields (row_id, platform, citation_tag,
  operating_wavelength_nm, omega_drive_rad_per_s, tau_ent_observed_s,
  conditions, link_class, verify_status, notes).

- **P2_no_current_measurement_violates_T2_grav_at_photonic_omega**
  For every populated row, tau_ent > T2_grav at the row's photonic
  omega. (Floor not currently violated at photonic frequencies.)
  Expected PASS: photonic T2_grav is ~50 ps at 1550 nm and typical
  tau_ent values are microseconds to seconds.

- **P3_margin_distribution_consistent_with_environmental_dominance**
  Median margin (tau_ent / T2_grav) across populated rows is >> 1.
  Confirms photonic measurements are environmental/source-noise-
  limited, not at the gravitational floor.

- **P4_row_count_meets_campaign_threshold**
  Total photonic rows >= 10 (campaign-doc threshold). PASS at 10+,
  BLOCKER below 10. Honest report of actual count in result_class.

- **P5_no_free_parameters_in_contact_analysis**
  T2_grav is computed only from R, D, alpha_H per the v1.1 formula.
  tau_ent comes from published measurements (tagged). No fitting
  parameter introduced.

- **P6_explicit_verification_path_documented**
  Every row carries a citation_tag and verify_status field
  PROVISIONAL_AUTHOR_BEST_EFFORT.

- **P7_contact_table_emitted_with_consistency_classification**
  CSV output groups rows by status (CONSISTENT_WITH_FLOOR /
  VIOLATION_OF_FLOOR / BOUNDARY_AT_FLOOR / INVALID).

- **P8_protocol_completes_end_to_end**
  Runner reads input table, computes T2_grav per row, emits
  residuals, writes outputs without runtime error.

- **P9_all_rows_use_CR071a_T2_equivalent_definition**
  Each row's tau_ent column is the photonic T2-equivalent per
  CR071a mapping row M04 (entanglement coherence time at photonic
  omega), not some other timescale.

- **P10_omega_values_derived_from_documented_wavelengths**
  Each row's omega_drive_rad_per_s is computed from its
  operating_wavelength_nm via omega = 2*pi*c/lambda; no fitted
  omega values.

- **P11_platform_diversity**
  Populated rows cover at least 3 distinct photonic-platform
  categories: {fiber_entanglement_distribution, free_space_satellite,
  atomic_memory, single_atom_node, on_chip_silicon_photonic,
  TF_QKD_or_DI_QKD, ensemble_quantum_memory, industry_metro_demo}.

## Wrong controls

- **WC1_inverted_formula_falsely_flags_violations**
  Same as CR069a WC1: confirm real T2_grav has discriminating power.
  (Expected to fail logically like CR069a/CR070a — inherited
  pattern.)

- **WC2_zero_omega_breaks_the_formula_gracefully**
  Same as CR069a/CR070a WC2.

- **WC3_negative_tau_ent_rejected_as_unphysical**
  Same shape as CR069a/CR070a WC3 (negative T2 rejected).

- **WC4_no_citation_tag_marks_row_as_provisional**
  Same as CR069a/CR070a WC4.

- **WC5_runner_does_not_modify_upstream_locks**
  Read-only on CR071a, CR064a, CR069a/CR070a.

- **WC6_no_free_parameters**
  All inputs traced to declared premises.

- **WC7_non_photonic_row_rejected**
  CR072a is photonic-only. A test row with operating_wavelength_nm
  outside the photonic range (e.g., 100 micron MW range) is
  rejected at input validation.

- **WC8_omega_derivation_consistency**
  For every populated row, computed omega from wavelength matches
  the row's recorded omega within rounding tolerance (no fitted
  omega).

## Outputs

```text
CR072a_photonic_empirical_table.csv  - input: 10-15 photonic rows (tagged PROVISIONAL)
CR072a_contact_analysis.csv          - output: per-row T2_grav + classification
CR072a_contact_plot.png              - log-log scatter tau_ent vs T2_grav
CR072a_runner.py                     - the contact analyzer
CR072a_summary.json                  - pass/fail per prediction and WC
CR072a_result.md                     - human-readable
HASHES.txt
```

## Falsifiers

- Any populated row with citation_tag = VERIFIED and tau_ent below
  T2_grav at that row's photonic omega would refute the T2_grav
  floor at photonic frequencies (currently no VERIFIED rows; all
  PROVISIONAL).
- Inability to populate >= 10 photonic rows would force CR072a to
  remain at BLOCKER status until the input table is expanded.
- A populated row with platform tau_ent that does not match the
  CR071a M04 definition (e.g., reporting laser linewidth in Hz
  instead of entanglement coherence in seconds) would force a
  per-row scope clarification.

## Free parameters

```text
free_parameters = 0
```

## Honest expected outcome

CR072a is expected to PASS with all populated rows in
CONSISTENT_WITH_FLOOR. The interesting cross-platform discrimination
happens in CR073a, where t_fire scaling is tested across NV and
photonic populations. CR072a's role is to load the photonic surface
honestly and report.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution.
Modifications to predictions, wrong controls, or scope after runner
output require a new CR.
