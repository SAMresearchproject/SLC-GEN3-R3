# CR215 CR214 Carrier Numeric Duplicate Audit

## Task

Audit the sealed CR214 195-row complement spreadsheet for numeric-duplicate
rows: rows that share an identical numeric signature across the whole sheet
(partition_signature, closure_depth, q_sign, q_abs, native_charge_axis,
M_native, surface_sign, surface_depth, S_debit_or_credit,
M_observed_candidate, qA_source_support, tensor_carrier_support,
retained_write_support) while differing only on text descriptors
(route_combination, operator_class, spin_or_hand_class).

## Origin

Reviewer flagged that file-line 176 (`QP093A-0301`, photon road carrier) and
file-line 180 (`QP093A-0305`, A-field carrier) appeared to enumerate
identical numbers across the sheet, distinguished only by label. CR215 makes
that observation formal, machine-checked, and bin-wide.

## Classification

This is a readout audit over the sealed CR214 artifact surface. CR215 does
not re-grade CR119 or CR214. It does not delete, renumber, or rewrite any
existing row. It produces a parallel annotated CSV with one new column
appended; the sealed CR214 CSV is read-only.

## Inputs

- `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv`
- Sealed sha256 of that input must equal the value recorded in
  `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/HASHES.txt`.

## Pass Conditions

- Input CSV sha256 matches the CR214 sealed value
  (`e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`).
- Input CSV has exactly 195 data rows.
- Numeric signature grouping is computed for every row.
- Every group with size > 1 is reported in
  `CR215_numeric_duplicate_groups.csv` with full member candidate_id list
  and the differing text descriptors.
- Annotated output CSV has exactly 195 data rows (no deletions).
- Annotated output CSV preserves the original column order and adds exactly
  one new trailing column `numeric_duplicate_class`.
- `numeric_duplicate_class` values follow the form
  `DUP-<bin>-<seq>` for members of a duplicate group, and `none` otherwise.
- Per-bin duplicate counts are reported, including the count of singleton
  rows that are not duplicates.

## Non-Promotion Rule

CR215 records the existence of numeric-duplicate groups. It does not
collapse, retire, or renumber any row. Whether a duplicate group represents
a single physical carrier written twice with different labels, or two
distinct carriers that share a degenerate numeric address, is an
interpretation question deferred to a follow-up CR. CR215 only proves that
the collision exists and pins down which rows are involved.

## Outputs

- `CR215_runner.py`
- `CR215_declared_premises.json`
- `CR215_input_manifest.csv`
- `CR215_numeric_signature_keys.csv`        (per-row signature key, all 195)
- `CR215_numeric_duplicate_groups.csv`      (one row per duplicate group)
- `CR215_per_bin_duplicate_summary.csv`     (bin level counts)
- `CR215_particle_complement_195_annotated.csv`
- `CR215_summary.json`
- `CR215_result.md`
- `HASHES.txt`
