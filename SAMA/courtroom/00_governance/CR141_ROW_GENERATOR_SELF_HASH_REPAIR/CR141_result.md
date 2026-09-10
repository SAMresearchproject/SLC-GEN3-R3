# CR141 Row-Generator Self-Hash Repair v1.0


## Verdict


```text
CR141_ROW_GENERATOR_SELF_HASH_REPAIR_V1_SEALED
```

## Scope


Recorded-provenance defect correction across the 10 row-generator CRs (CR-128 through CR-134) identified by the CR-135 hostile audit. Each target carried a `*_lock_sha256` field that did NOT match the actual SHA-256 of its lock JSON on disk; the cross-CR chain via CR-060a was intact, but each CR's self-citation was inconsistent. Root cause: runner self-reference artifact (lock hash computed before being embedded in the lock JSON).

This CR is a DEFECT_CORRECTION. No verdict on any target CR is changed. The underlying claims, in-sample matches, partition algebras, forward-blind sub-predictions, and wrong controls all stand verbatim.

## Inputs (audit-verified)


- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
- Targets: 10 row-generator CRs in `13_CERN_INDEPENDENT_TESTS/CR12[8-9]*/` and `CR13[0-4]*/`
- Source manifest: `CR141_source_manifest.csv`

## Per-Target Outcome


| CR | Status | Field | Actual lock SHA-256 (first 12) | Result-class preserved |
| --- | --- | --- | --- | --- |
| CR128 | ALREADY_REPAIRED | `law_lock_sha256` | `0f62d6b4e942...` | `CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED` |
| CR128b | ALREADY_REPAIRED | `law_lock_sha256` | `fb9287cd6c79...` | `CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED` |
| CR129 | ALREADY_REPAIRED | `law_lock_sha256` | `041a487c30a8...` | `CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED` |
| CR129b | ALREADY_REPAIRED | `magnitude_lock_sha256` | `8c3d0eb78b46...` | `CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1_SEALED` |
| CR129c | ALREADY_REPAIRED | `universal_lock_sha256` | `bfd5ab8c3256...` | `CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED` |
| CR130 | ALREADY_REPAIRED | `bridge_lock_sha256` | `0a40209bc4c5...` | `CR130_2BODY_3BODY_STRUCTURAL_BRIDGE_SEALED` |
| CR131 | ALREADY_REPAIRED | `law_lock_sha256` | `2aef1403da7f...` | `CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED` |
| CR132 | ALREADY_REPAIRED | `law_lock_sha256` | `fbc25a887e01...` | `CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED` |
| CR133 | ALREADY_REPAIRED | `law_lock_sha256` | `1e7e08d8764e...` | `CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED` |
| CR134 | ALREADY_REPAIRED | `law_lock_sha256` | `6ab494427853...` | `CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED` |

Targets in repaired state: **10 / 10**.  Anomalies: **0**.  (Run-time split — repaired now: 0; already repaired: 10.)

## Predictions


- **[PASS]** P1_ten_targets_identified — len(targets) = 10 (expected 10)
- **[PASS]** P2_all_lock_jsons_exist — Each target directory contains exactly one *lock*.json file.
- **[PASS]** P3_all_result_md_exist — All 10 *_result.md files exist at expected paths.
- **[PASS]** P4_all_summary_json_parse — All 10 *_summary.json files exist and parse as JSON dicts.
- **[PASS]** P5_all_targets_repaired_or_already_repaired — Every target has status REPAIRED or ALREADY_REPAIRED (no anomalies, no errors).
- **[PASS]** P6_all_recorded_hashes_match_actual_lock_hashes — Post-repair recorded *_lock_sha256 fields match SHA-256 of their lock JSON for all 10 CRs.

## Wrong Controls


- **[PASS]** WC1_verdict_line_preserved — All 10 target result_class fields preserved bit-identical from archived originals.
    - load-bearing deletion: If any result_class value were altered, this WC would FAIL.
- **[PASS]** WC2_summary_json_parseable — All 10 summary.json files parse as valid JSON post-repair.
    - load-bearing deletion: If any summary.json were corrupted (e.g. missing brace), this WC would FAIL.
- **[PASS]** WC3_archived_originals_hash_match — All 10 archived originals hash to the values recorded in their original_sha256.txt.
    - load-bearing deletion: If any archived original were edited or corrupted, this WC would FAIL.
- **[PASS]** WC4_post_repair_self_hash_matches_actual — All 10 recorded *_lock_sha256 fields match the actual SHA-256 of their lock JSON.
    - load-bearing deletion: If any lock JSON were modified or any recorded hash reverted, this WC would FAIL.
- **[PASS]** WC5_audit_verdict_reference_resolves — AUDIT_VERDICT path exists=True; hash matches expected=2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
    - load-bearing deletion: If the audit verdict file were moved/edited, the recorded reference would be unverifiable; this WC would FAIL.
- **[PASS]** WC6_replacement_records_cross_refs_resolve — All 10 REPLACEMENT_RECORD.md files exist and their cross-referenced audit / event artifacts exist.
    - load-bearing deletion: If any REPLACEMENT_RECORD or cross-referenced audit file were missing, this WC would FAIL.
- **[PASS]** WC7_audit_correction_block_well_formed — All 10 audit_correction blocks present with all 12 required fields and verdict_unchanged=True.
    - load-bearing deletion: If the audit_correction block were removed or any required field stripped, this WC would FAIL.
- **[PASS]** WC8_audit_correction_records_actual_correction — All 10 audit_correction blocks record a true correction (old_value != new_value, both valid 64-char SHA-256) and new_value matches the actual on-disk lock SHA-256.
    - load-bearing deletion: If the runner clobbered old_value during deep_replace (the bug found mid-seal on 2026-06-17), this WC would FAIL. Closes the semantic gap WC7 missed.

## Falsifier (LOCKED)


Re-executing `CR141_runner.py` on the post-seal state of the 10 target CRs MUST produce zero new `REPAIRED` entries and zero new archive writes. Any deviation (a target unexpectedly entering `REPAIRED` again, or any change to an archived original, or any mismatch between recorded and actual lock SHA-256) falsifies CR-141 v1.0 and triggers an appeal CR.

**Free parameters:** 0.

## Restoration Requirements


N/A — CR-141 is a defect correction; no verdict is downgraded by this CR. Each target CR's underlying PASS verdict is preserved through the recorded-hash correction. Restoration paths for the underlying row-generator laws (if those laws are ever falsified by forward-blind row contact) live in each target's own pre-committed sub-prediction; they are not duplicated here.

## Cryptographic Chain


```text
CR135_audit_verdict_sha256                = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
CR141_source_manifest_csv                 = cb047c0de2faeca021ea4d4b34daf47cf01ea75ecc58159e4b487c536b6bb44d
CR141_repair_manifest_csv                 = 6d61e65e839ef833567b28b1540447c80455a75b075bd40ded20c3d491f3973a
CR141_predictions_csv                     = 44827544459952ce74f4a43b105e942e7b7e6b7729bdf622d6ef1d8251e3425d
CR141_wrong_controls_csv                  = 1a3b1ca5393b59a0c38cbc5ebe1d18f50b3a946d22ef9be9033f8bbc503d0c1f
CR141_repair_lock_json                    = f92ac88090a6927cdcdd7fb5d875708ad3c70ba071d37560b3b0b6ef71b6bc0a
```

## Follow-up CRs


- **CR-141b** (structural fix): modify the row-generator runner template so that the lock JSON either omits its own self-hash, OR the runner re-hashes the lock after the self-hash field is embedded. Eliminates the self-reference artifact at the source so future CRs do not require CR-141-style repair.

## Rule of Immutability


Method, falsifier, wrong controls, and the 10-target scope are frozen at CR-141 seal time. Future falsification or refinement must be in an appeal CR within `00_governance/`.
