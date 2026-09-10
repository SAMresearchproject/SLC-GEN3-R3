# CR216 Carrier Duplicate Retirement

Result: **CR216_PASS_DUP_CARRIER_ONLY_ROWS_01_RESOLVED__KEEP_QP093A-0301__RETIRE_QP093A-0305__FOOTPRINT_IDENTITY_PLUS_LOWER_ID_TIEBREAK__ACTIVE_COMPLEMENT_194__SEALED_INPUTS_UNMODIFIED**

## Direct Answer

The CR215 carrier-only duplicate pair is resolved by courtroom evidence,
not by physics interpretation:

- **KEEP** `QP093A-0301` (ROAD_LIGHT_CARRIER / photon_road_carrier / transverse_vector)
- **RETIRE** `QP093A-0305` (A_FIELD_CARRIER / a_kernel_support / environmental_A_support)

The CR214 195-row complement is retained as a sealed historical artifact
at its original sha256. The active de-duplicated complement going forward
is the 194-row CSV produced by CR216.

## Input Verification

All six sealed inputs re-hashed at runtime; all six matches confirmed.

| Input | Sealed sha256 (head) | Match |
|---|---|---|
| `CR214_particle_complement_195.csv` | `e41016b5...` | yes |
| `CR215_numeric_duplicate_groups.csv` | `8d8f0461...` | yes |
| `CR132_verification.csv` | `9937d79e...` | yes |
| `CR124_crosswalk.csv` | `0c8f8b10...` | yes |
| `CR119_vault_identity_assignments.csv` | `99d37c17...` | yes |
| `CR060a_alphabet.csv` | `33f5c1f0...` | yes |

## External Footprint Evidence

For each of the two candidates, CR216 extracted the consumer row in four
downstream sealed CRs and compared *behavior* payloads (excluding the
candidate_id and any descriptor-only label columns). All four consumers
return identical behavior payloads for QP093A-0301 and QP093A-0305:

### CR132 — 1-body carrier lattice law verification

Behavior columns: `partition, lattice_i, lattice_j, structural, M_native_predicted, M_native_observed, diff, S_debit_observed, S_debit_zero, match`.

Identical for both: `1, massless, massless, 0 (massless), 0, 0, 0, 0, True, True`.

Only descriptor difference: operator_class (ROAD_LIGHT_CARRIER vs A_FIELD_CARRIER), spin_class (transverse_vector vs environmental_A_support).

### CR124 — CERN gap crosswalk on the 321-particle list

Behavior columns include the external anchor mapping (`nearest_anchor_id`,
`nearest_anchor_observable`, `nearest_anchor_experiment`,
`nearest_anchor_M_MeV`, `rel_dist`, `anchor_class_crosswalk`, `cern_reach`,
etc.).

Both candidates map to the same external anchor `EXO003` (Tcc+(3875) mass
relative to D*+ D0 threshold, LHCb), same `nearest_anchor_M_MeV = -0.273`,
same `rel_dist = 0.273`, same `GAP_REGION`.

### CR119 — vault identity assignments

Behavior columns: `identity_assignment_status, known_identity_label,
known_symbol, known_name, known_label_used_as_construction_input,
matter_row_allowed, promotion_status, qA_source_support,
tensor_carrier_support, retained_write_support, source_known_match, layer`.

Identical for both: `NATIVE_PARTICLE_IDENTITY_ASSIGNED_NO_KNOWN_LABEL`,
no external label bound, `matter_row_allowed=no`,
`promotion_status=REJECT_MATTER_PROMOTION_CARRIER_ONLY`, all support
counters zero.

### CR060a — Paul Revere 1-body carrier alphabet

Behavior columns: `partition, tier, role, M_native, q_abs, q_sign,
closure_depth, stability_status`.

Identical for both: `partition=1, tier=1body_carrier, role=1-body boson carrier (gauge/substrate-field broadcast), M_native=0, q_abs=0, q_sign=neutral, closure_depth=3, stability_status=CARRIER_ONLY_NOT_MATTER`.

### Footprint conclusion

`external_footprint_identical_overall = true` across all four sealed
consumers. No downstream test in the courtroom distinguishes the two
candidates by anything other than descriptor labels.

## Tiebreak Rule and Verdict

Rule (declared in CR216_declared_premises.json before execution):
`KEEP_LOWER_CANDIDATE_ID__RETIRE_HIGHER_CANDIDATE_ID` when external
footprint is identical, group size is two, and members share a bin.

Preconditions satisfied:
- external_footprint_identical_overall: true
- group_size: 2
- members in same bin (carrier_only_rows): true

Rule fires:
- keep: QP093A-0301
- retire: QP093A-0305

This matches the verdict pre-declared in `CR216_declared_premises.json`.

## Physics Rationale (descriptive, not load-bearing)

In standard QED the electromagnetic four-potential A_mu is the photon
field; the photon is the quantized excitation of A_mu. A
`ROAD_LIGHT_CARRIER / transverse_vector` row and an `A_FIELD_CARRIER /
environmental_A_support` row carrying identical numeric signature is
consistent with one carrier enumerated twice under two related labels:
the propagating photon view (ROAD_LIGHT_CARRIER) and the gauge potential
view (A_FIELD_CARRIER).

CR216 records this as physical context for the reader. The actual ruling
is driven by the courtroom-internal footprint evidence and the
deterministic tiebreak rule above.

## Row Reconciliation

| Quantity | Value |
|---|---:|
| Sealed CR214 complement rows | 195 |
| Active CR216 complement rows | 194 |
| Retired rows | 1 |
| 194 + 1 == 195 | true |

## Pass Conditions

| Check | Result |
|---|---|
| all_inputs_verified | PASS |
| group_size_is_two | PASS |
| members_in_same_bin | PASS |
| external_footprint_identical_overall | PASS |
| verdict_matches_predeclared | PASS |
| active_complement_row_count_is_194 | PASS |
| retired_row_count_is_one | PASS |
| row_reconciliation | PASS |
| active_csv_preserves_original_column_order | PASS |

9 of 9 checks passed. Execution status: CLEAN.

## Implications and Open Leads

- The sealed 321-particle catalog in CR119 still contains QP093A-0305 as a
  row. Going forward, queries that need the de-duplicated active set
  should consume `CR216_particle_complement_194_active.csv` and consult
  `CR216_retirement_ledger.csv` to translate any reference to QP093A-0305
  into a reference to QP093A-0301. CR216 does not modify the CR119
  catalog. A separate follow-up CR (CR217 candidate) could publish a
  matching 320-row active particle catalog if downstream tooling needs it.

- The headline 195-row count cited in `SEANBRADY_195_PARTICLE_INSPECTION`
  should now be footnoted: 195 is the sealed CR214 count; 194 is the
  CR216 active count after the photon/A-field collision is resolved.
  CR216 does not edit that inspection doc.

- The other duplicate group identified by CR215
  (`DUP-rejected_fake_closures-01`, 8 reject sentinels sharing a null
  signature) is by-design and is not retired. The rejected_fake_closures
  bin's payload is its descriptor, and its numerics are intentionally
  null; CR216 leaves all 8 rows active.

## Artifacts

- `CR216_PRECOMMIT.md`
- `CR216_declared_premises.json`
- `CR216_runner.py`
- `CR216_input_manifest.csv`
- `CR216_external_footprint.csv`
- `CR216_retirement_ledger.csv`
- `CR216_particle_complement_194_active.csv`  *(active spreadsheet going forward)*
- `CR216_summary.json`
- `HASHES.txt`

## Chain of Custody

- `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv` — sealed historical artifact, sha256 `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`, untouched by CR215 and CR216.
- `09a_PARTICLE_MASS_CHAIN/CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT/` — non-destructive annotation; identified the duplicate group without modifying the sealed input.
- `09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/` — formal retirement; produced active 194-row spreadsheet and retirement ledger without modifying any sealed input.
