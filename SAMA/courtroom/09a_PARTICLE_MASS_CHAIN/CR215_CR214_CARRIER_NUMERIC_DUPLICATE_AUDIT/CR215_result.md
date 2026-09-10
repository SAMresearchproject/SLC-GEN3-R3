# CR215 CR214 Carrier Numeric Duplicate Audit

Result: **CR215_FINDING_NUMERIC_DUPLICATE_PRESENT__2_GROUP__10_ROWS__ALL_INPUT_ROWS_PRESERVED__SEALED_INPUT_UNMODIFIED**

## Direct Answer

The CR214 195-row complement spreadsheet contains numeric-duplicate rows.
Two duplicate groups exist across the 195 rows, covering 10 rows in total.
Only one is a substantive collision; the other is an expected reject-sentinel pattern.

## Input Verification

- Input CSV: `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv`
- Sealed sha256: `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`
- Observed sha256 at CR215 read: `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`
- Match: yes
- Input row count: 195

## Numeric Signature Definition

A row's numeric signature is the tuple of values in these 14 columns:

`bin, partition_signature, closure_depth, q_sign, q_abs, native_charge_axis,
M_native, surface_sign, surface_depth, S_debit_or_credit,
M_observed_candidate, qA_source_support, tensor_carrier_support,
retained_write_support`

Two rows are numeric duplicates when their signature tuples are
string-equal. Descriptor columns (`route_combination`, `operator_class`,
`spin_or_hand_class`, etc.) are excluded from the signature on purpose so
that label-only differences are detected.

## Findings

### Group 1 — `DUP-carrier_only_rows-01` (substantive)

| Row | candidate_id | route_combination | operator_class | spin_or_hand_class |
|---|---|---|---|---|
| 176 | QP093A-0301 | photon_road_carrier | ROAD_LIGHT_CARRIER | transverse_vector |
| 180 | QP093A-0305 | a_kernel_support    | A_FIELD_CARRIER    | environmental_A_support |

Shared signature: `carrier_only_rows | p=1 | d=3 | q=neutral:0 | carrier_axis | M_native=0 | M_obs=0 | S=0 | all support columns = 0`.

This pair occupies the same numeric address in the carrier_only_rows bin
and is distinguished only by three text-descriptor columns. CR215 records
the collision and preserves both rows. Interpretation is deferred to a
follow-up CR.

### Group 2 — `DUP-rejected_fake_closures-01` (sentinel, expected)

All eight rejected_fake_closures rows (QP093A-0314 through QP093A-0321)
share a single null/sentinel numeric signature:
`rejected_fake_closures | p=1 | d=0 | q=neutral:0 | fake_axis | M_native=0 | spin=fake_spin | ...`.

This is the expected shape of a labeled reject-sentinel bin: each row's
content is its descriptor (`fake_direct_qA_as_mass`,
`fake_random_route_closure`, etc.), and its numerics are deliberately
null. CR215 reports the group for completeness but flags it as a
sentinel-pattern duplicate, not a structural collision.

## Per-Bin Summary

| bin | total_rows | duplicate_group_count | rows_in_a_duplicate_group | singleton_rows |
|---|---:|---:|---:|---:|
| antimatter_conjugate_rows | 42 | 0 | 0 | 42 |
| bound_composite_rows | 106 | 0 | 0 | 106 |
| carrier_only_rows | 6 | 1 | 2 | 4 |
| hidden_source_support_rows | 8 | 0 | 0 | 8 |
| rejected_fake_closures | 8 | 1 | 8 | 0 |
| unstable_resonance_rows | 25 | 0 | 0 | 25 |

## Non-Destructive Annotation

The sealed CR214 CSV is unmodified (verified by sha256 match above).

CR215 produces a parallel annotated copy
`CR215_particle_complement_195_annotated.csv` with:

- 195 rows in original order
- All 36 original columns preserved at their original positions
- Exactly one new trailing column `numeric_duplicate_class`
  - value `DUP-carrier_only_rows-01` on rows 176 and 180
  - value `DUP-rejected_fake_closures-01` on the eight rejected_fake_closures rows
  - value `none` on the remaining 185 rows

No row was added, deleted, reordered, renumbered, or had its existing
numeric values rewritten. The annotation is additive only.

## Pass Conditions

| Check | Result |
|---|---|
| input_sha256_matches_sealed | PASS |
| input_row_count_is_195 | PASS |
| annotated_row_count_matches_input | PASS |
| annotated_has_added_column | PASS |
| annotated_added_exactly_one_column | PASS |
| duplicate_class_singleton_label_is_none | PASS |

6 of 6 checks passed. Execution status: CLEAN.

## Open Leads (Not Promoted)

- The carrier_only_rows photon-vs-A-field collision suggests one of two
  reads, both worth a separate CR: (a) the two labels are descriptor
  aliases for a single carrier slot; or (b) two distinct carriers
  legitimately occupy a degenerate numeric address and the signature
  scheme is missing one or more columns that would separate them. CR215
  does not promote either reading.
- The carrier_only_rows bin total of 6 includes one numeric-duplicate
  pair. If interpretation (a) is later adopted, the effective carrier
  count is 5 and the headline 195-row total would be revisited in a
  separate CR. CR215 does not perform that revision.

## Artifacts

- `CR215_PRECOMMIT.md`
- `CR215_declared_premises.json`
- `CR215_runner.py`
- `CR215_input_manifest.csv`
- `CR215_numeric_signature_keys.csv`
- `CR215_numeric_duplicate_groups.csv`
- `CR215_per_bin_duplicate_summary.csv`
- `CR215_particle_complement_195_annotated.csv`
- `CR215_summary.json`
- `HASHES.txt`
