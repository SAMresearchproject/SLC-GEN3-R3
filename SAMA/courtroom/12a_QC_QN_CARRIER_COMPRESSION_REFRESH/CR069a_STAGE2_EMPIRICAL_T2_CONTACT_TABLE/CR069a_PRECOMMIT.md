# CR069a — Stage 2: Empirical T2 Contact Table — PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-18
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Test class:** STAGE2_EMPIRICAL_T2_CONTACT_TABLE_AGAINST_T2_GRAV_V1_1
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repository root.

---

## Scope

CR069a is the **Stage 2 empirical contact** for the T2_grav v1.1 prediction sealed at CR064a. It is the framework + initial population of a contact table comparing **published T2 measurements** from quantum hardware platforms (NV centers, transmons, trapped ions, optical clocks) against the T2_grav floor predicted by:

```text
T2_grav(omega_drive) = 16 * pi * R^4 / (17 * omega_drive)
```

CR069a is what lifts CR064a v1.1 from **BOUNDARY** to a stronger verdict. It does so by establishing whether the floor is **consistent with** existing published measurements (necessary condition) or **violated by** any of them (sufficient to refute).

## What the T2_grav prediction actually says

The T2_grav formula sets a **lower bound** on quantum coherence times. The substrate cannot be silenced beyond this floor — every completed write releases its 1/8 carrier (CR-121), and that release is what couples matter to the A field. The prediction is:

```text
T2_observed >= T2_grav   for any quantum system at drive frequency omega_drive
```

A measurement that falls **below** T2_grav after rigorous channel subtraction would falsify CR064a v1.1.

A measurement **above** T2_grav is consistent with the floor but does not validate it — current published measurements are typically dominated by environmental noise (phonons, spin baths, field drift) that leave T2_observed far above T2_grav. The interesting test happens when environmental engineering pushes T2_observed close to T2_grav and we ask whether it saturates at the floor.

**Therefore CR069a's null-result expectation is:** all current published measurements should sit ABOVE T2_grav with significant margin. A measurement below T2_grav would be a major finding *against* the framework. A measurement at T2_grav (within experimental uncertainty) would be a major finding *for* the framework. Most measurements are expected in the "above with margin" regime.

## Honest scope of CR069a

CR069a IS:
- The framework for ongoing empirical contact: takes (T2_observed, omega_drive, apparatus context, citation) and emits residual analysis
- The initial population with literature values I (the runner author) can cite from published NV / superconducting / trapped-ion T2 literature, **tagged for partner-lab citation verification**
- A demonstration that no current published measurement falsifies CR064a v1.1
- The deliverable that lifts CR064a v1.1 from BOUNDARY in the direction of PASS, conditional on the citation verification step

CR069a IS NOT:
- A validation that the T2_grav floor exists in nature (that requires environmental-engineering improvements that drive T2_observed close to T2_grav, which is years away)
- A claim that any specific citation is verified — citations are tagged `[VERIFY_PRECOMMIT_AGAINST_PUBLISHED_PAPER]` and require partner-lab confirmation before the row counts toward CR064a's upgrade
- A claim about platforms I cannot competently cite (e.g., neutral-atom clocks beyond representative ranges)

## Upstream dependencies (hash-locked typed premises)

```text
A0-a_h-D foundation
CR060a_alphabet_lock.json                d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock.json               c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock.json          38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock.json          c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9
CR067a_result_md_sha256                  da44a9cb33bb756d408efad91e86ce7344191f5fa329ffdbb2ff8359b8e9b1cf
CR067b_result_md_sha256                  8b98dff7e6b02c7f5b301d85c086c34ea7c18dc9ca8f478b7b8aaf278bba3ddb
CR068a_result_md_sha256                  aed3e4cca2fa5cd4a6e78d003aa617c71eead4ba18d8f2a3324ad9be8f8e9ba9
CR121_gravity_mechanism_intake_lock      01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469
CR129b_magnitude_lock                    8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd
```

## Foundation primitives

```text
R       = 12
D       = 3
alpha_H = 2
```

## The T2_grav v1.1 formula

```text
T2_grav(omega) = 16 * pi * R^4 / (17 * omega) = 16 * pi * 20736 / (17 * omega)
              ~= 6.13e4 / omega seconds      (with omega in rad/s)
```

At representative drive frequencies:

```text
omega = 2 * pi * 2.87 GHz   (NV resonant)         T2_grav ~= 3.40 us
omega = 2 * pi * 5 GHz      (transmon typical)    T2_grav ~= 1.95 us
omega = 2 * pi * 10 MHz     (ion hyperfine)       T2_grav ~= 975 us
omega = 2 * pi * 200 THz    (optical clock)       T2_grav ~= 4.88e-11 s
```

## Predictions

- **P1_table_well_formed**
  Each row has all required fields (platform, citation_tag, omega_drive, T2_observed, conditions, [VERIFY_PRECOMMIT_AGAINST_PUBLISHED_PAPER] flag).

- **P2_no_current_measurement_violates_T2_grav**
  For every populated row, T2_observed > T2_grav at the row's omega_drive. (Floor is not currently violated.)

- **P3_margin_distribution_consistent_with_environmental_dominance**
  Median margin (T2_observed / T2_grav) across populated rows is >> 1. Confirms current measurements are environmental-noise-limited, not at the gravitational floor.

- **P4_cryo_DD_NV_closest_to_floor_in_relative_terms**
  Of the platforms in the table, cryo+DD NV with isotopic purification (Hanson-class) should have the smallest T2_observed / T2_grav margin — the platform engineered closest to the floor. (Still expected to be >> 1.)

- **P5_no_free_parameters_in_contact_analysis**
  T2_grav is computed only from R, D, alpha_H per the v1.1 formula. T2_observed comes from published measurements (tagged). No fitting parameter introduced.

- **P6_explicit_verification_path_documented**
  Every row carries a citation tag and a `[VERIFY_PRECOMMIT_AGAINST_PUBLISHED_PAPER]` field. Partner-lab confirmation of each citation lifts the row from PROVISIONAL to VERIFIED, and the table aggregate from PROVISIONAL to VERIFIED.

- **P7_contact_table_emitted_with_consistency_classification**
  CSV output groups rows by status (CONSISTENT_WITH_FLOOR / VIOLATION_OF_FLOOR / BOUNDARY_AT_FLOOR / UNVERIFIED_PROVISIONAL).

- **P8_protocol_completes_end_to_end**
  Runner reads input table, computes T2_grav per row, emits residuals, writes outputs without runtime error.

## Wrong controls

- **WC1_inverted_formula_falsely_flags_violations**
  Compute with the inverted formula T2_grav_wrong = omega / (16 * pi * R^4). At GHz drive this gives nanosecond floors that EVERY measurement exceeds trivially; rows trivially "consistent" with the wrong formula confirms that the real formula has discriminating power (the real formula's floor is sometimes within an order of magnitude of measured T2, which means it CAN be violated; the wrong formula's floor cannot).

- **WC2_zero_omega_breaks_the_formula_gracefully**
  T2_grav at omega = 0 diverges. Runner emits explicit divide-by-zero handling, not silent NaN.

- **WC3_negative_T2_observed_rejected_as_unphysical**
  Any input row with T2_observed <= 0 is rejected with a structured error, not silently passed through.

- **WC4_no_citation_tag_marks_row_as_provisional**
  Rows without a citation tag are flagged PROVISIONAL_NO_CITATION and excluded from the consistency aggregate.

- **WC5_runner_does_not_modify_upstream_locks**
  Runner is read-only on upstream CR locks.

- **WC6_no_free_parameters**
  All structural inputs traced to CR069a_declared_premises.json.

## Outputs

```text
CR069a_published_t2_table.csv         - input: literature T2 measurements (tagged)
CR069a_contact_analysis.csv           - output: per-row residual + status
CR069a_contact_plot.png               - log-log scatter of T2_observed vs T2_grav
CR069a_runner.py                      - the contact analyzer
CR069a_summary.json                   - pass/fail per prediction and wrong control
CR069a_result.md                      - human-readable
HASHES.txt
```

## Falsifiers

- Any row with `[VERIFIED]` citation and T2_observed clearly below T2_grav refutes CR064a v1.1. CR069a flips to REFUTED status, CR-121 mechanism rides into BOUNDARY/REFUTED triage.
- Inability to populate any literature rows confidently would force CR069a to remain at SCAFFOLD-only status until partner-lab verification supplies the data.

## Free parameters

```text
free_parameters = 0
```

## Stewardship

Per `STEWARDSHIP.md`.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution. Modifications to predictions, wrong controls, or scope after runner output require a new CR.
