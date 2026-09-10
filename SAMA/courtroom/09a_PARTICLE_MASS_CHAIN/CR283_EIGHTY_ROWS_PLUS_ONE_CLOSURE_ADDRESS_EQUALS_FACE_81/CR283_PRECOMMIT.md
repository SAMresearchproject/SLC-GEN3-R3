# CR283 Precommit -- Eighty Rows Plus One Closure Address Equals Face 81

record_id: `CR283_EIGHTY_ROWS_PLUS_ONE_CLOSURE_ADDRESS_EQUALS_FACE_81`
task: `SAM_PROSPECTIVE_CR_80_PARTICLE_ROWS_81_FACE_CLOSURE_ADDRESS_5_5_XHIGH`
classification: `SCIENTIFIC_TEST`
preflight_report: `artifacts/preflight_filled/PREFLIGHT_20260712_033523_no_script.md`

## Target Claim

```text
80 active particle-bearing row occurrences
+ 1 non-row closure/contact address
= 81 completed face capacity
```

Exact arithmetic to replay:

```text
S = 8
W = 9 = 8 + 1
F = 81 = 9^2
P = 80 = 81 - 1 = (9 - 1)(9 + 1) = 8*10
L = 162 = 2*81
```

## Source Contract

The locked source manifest is `CR283_SOURCE_MANIFEST.json`. The controlling 80-row inventory is CR253, with semantic clarification from CR280. Closure/contact provenance is CR267, CR269, and the CR282 appeal. Ledger capacity is CR229/CR233. A-field row retirement is CR216, and non-row A is CR256/CR282.

## Frozen Tests

1. Verify every source hash before interpretation.
2. Reproduce `80` rows from `CR253_promoted_80_rows.csv`.
3. Build `CR283_PARTICLE_ROW_REGISTER.csv` by joining the promoted rows to the CR253 input catalog and CR280 row-contract data.
4. Reproduce source-supported decompositions: `48 + 32`, `64 + 16`, and row-law split `32 + 16 + 32`.
5. Replay wrong controls for the retired A-field row, missing 81st particle, closure address counted as row, support/carrier collapse, CSV-order grid, manual grid, arithmetic-only, CR282 scope violation, numeric-one collapse, forced ten octets, and random-label descriptors.
6. Search for a source-native 9x9 coordinate rule exactly as frozen in `CR283_COORDINATE_RULE_PRECOMMIT.json`.
7. Search for a single-field source-native ten-octet grouping exactly as frozen in `CR283_COORDINATE_RULE_PRECOMMIT.json`.
8. Score the eight competing models using `CR283_MODEL_DEFINITIONS.json`.

## Verdict Rule

Full PASS requires exact 80 rows, exact 81/162 arithmetic, independent closure-address support, and a natural row-level organization for the face or ten-octet interpretation.

Structural PASS is required when the 80 rows, non-row closure address, and ledger arithmetic integrate cleanly but no unique row-to-face geometry is established:

```text
PASS_CARDINALITY_AND_TYPED_LEDGER_WELD_ROW_GEOMETRY_OPEN
```

## Firewall Metadata

```text
prospective_record_class = "SCIENTIFIC_TEST"
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

No SAM Language path, contract, candidate implementation, holdout queue, forecast gate, or language output is an input to this CR.
