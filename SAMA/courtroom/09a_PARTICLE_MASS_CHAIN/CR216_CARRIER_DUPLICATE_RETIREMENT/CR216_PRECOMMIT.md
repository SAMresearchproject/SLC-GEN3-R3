# CR216 Carrier Duplicate Retirement

## Task

Use the CR215 numeric-duplicate finding to resolve the carrier_only_rows
collision between QP093A-0301 (ROAD_LIGHT_CARRIER / photon_road_carrier /
transverse_vector) and QP093A-0305 (A_FIELD_CARRIER / a_kernel_support /
environmental_A_support). Decide which row is original and which is
duplicate using courtroom evidence, retire the duplicate from the active
working set, and emit a new de-duplicated active complement spreadsheet
without altering any sealed prior artifact.

## Origin

CR215 proved that QP093A-0301 and QP093A-0305 share an identical numeric
signature across the 14 numeric columns of the CR214 195-row complement,
distinguished only by three text-descriptor columns. CR215 deliberately
did not promote either of two interpretations. CR216 makes the call.

## Classification

Audit + retirement. CR216 does not regrade CR119, CR132, CR124, CR060a, or
CR214. It reads their sealed surfaces as evidence inputs. It produces a
new active spreadsheet (194 rows) and a retirement ledger (1 row). It does
not modify any sealed input file.

## Inputs (all hash-verified at runtime)

- `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv` (sealed; expected sha256 `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`)
- `09a_PARTICLE_MASS_CHAIN/CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT/CR215_numeric_duplicate_groups.csv` (sealed; expected sha256 `8d8f0461d2e54df89a57cc1d16a886efa792fa8b900c38b0c083c717bc8d8f98`)
- `13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_verification.csv` (sealed; expected sha256 `9937d79e790c08d7a7230d1d5f20409ae28542a5aed8d944c3ddbe1716715bee`)
- `13_CERN_INDEPENDENT_TESTS/CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST/CR124_crosswalk.csv` (sealed; expected sha256 `0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca`)
- `09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_vault_identity_assignments.csv` (sealed; expected sha256 `99d37c178188599c611179ae1e35a2113f378d6d79d8cbc89881598e1842816c`)
- `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1/CR060a_alphabet.csv` (sealed; expected sha256 `33f5c1f05bb23a69556d9c68f219a2515ddcd394c0310c85b5427e25bc341cdd`)

## External Footprint Evidence

For each candidate in `DUP-carrier_only_rows-01`, CR216 records the row
that downstream CR consumes:

- `CR132_verification.csv` payload (lattice-law verification columns)
- `CR124_crosswalk.csv` payload (CERN gap mapping)
- `CR119_vault_identity_assignments.csv` payload (vault identity assignment)
- `CR060a_alphabet.csv` payload (Paul Revere 1-body carrier role)

CR216 marks the candidate as `EXTERNAL_FOOTPRINT_IDENTICAL` when the
payloads in all four consumers match string-for-string between the two
candidates (after excluding the candidate_id column and any pure label
columns).

## Tiebreak Rule

When external footprint is identical:

`KEEP_LOWER_CANDIDATE_ID__RETIRE_HIGHER_CANDIDATE_ID`

The lower candidate_id is the first-enumerated entry; the higher
candidate_id is the later addition. This rule is deterministic and
content-independent. CR216 records the rule explicitly so reviewers can
re-derive the verdict without inspecting the underlying physics.

## Physics Rationale (descriptive, not load-bearing)

In standard QED the electromagnetic four-potential A_mu and the photon
quantum field are the same object. A row labeled `ROAD_LIGHT_CARRIER /
transverse_vector` and a row labeled `A_FIELD_CARRIER /
environmental_A_support` carrying identical p, d, q, M, S signatures
matches the QED identification A_mu == photon. CR216 records this as
context. The ruling is driven by the courtroom evidence and the tiebreak
rule, not by physics reasoning.

## Pass Conditions

- Every declared input csv matches its expected sha256.
- CR215's `DUP-carrier_only_rows-01` group exists and has exactly two
  members: QP093A-0301 and QP093A-0305.
- External footprint for both candidates is identical across CR132,
  CR124, CR119 vault, and CR060a (after candidate_id stripped).
- Tiebreak rule selects QP093A-0301 as KEEP and QP093A-0305 as RETIRE.
- Active output csv has exactly 194 data rows.
- Active output csv has the same column set as the sealed 195-row csv
  plus the original column order preserved.
- Retirement ledger has exactly one row keyed to QP093A-0305 with
  `replacement_candidate_id = QP093A-0301`.
- 194 + 1 == 195 (count reconciliation).

## Non-Destructive Rule

No sealed input file is modified. The CR214 195-row csv remains
referenceable at its sealed sha256 as the historical artifact and the
input record under audit. The active spreadsheet going forward is
`CR216_particle_complement_194_active.csv`.

## Outputs

- `CR216_runner.py`
- `CR216_declared_premises.json`
- `CR216_input_manifest.csv`
- `CR216_external_footprint.csv`
- `CR216_retirement_ledger.csv`
- `CR216_particle_complement_194_active.csv`
- `CR216_summary.json`
- `CR216_result.md`
- `HASHES.txt`
