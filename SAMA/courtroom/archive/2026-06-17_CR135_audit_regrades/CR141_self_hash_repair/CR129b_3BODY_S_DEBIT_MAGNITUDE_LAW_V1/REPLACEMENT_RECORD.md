# REPLACEMENT_RECORD — CR129b self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_result.md` and `CR129b_summary.json` |
| Original result.md SHA-256 | `2eb5e87a920b60f989f2dd39f4efb0ea356eeadbc70803eac47db0904200fb22` |
| Original summary.json SHA-256 | `98c90e831e9586e2ea092190c1af95e045cc601558c0841499fd494f5114d58a` |
| Original verdict | `PASS — CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `be49c1e301a1741e4daa9350db10eb36ce61c02f462271690ecdad1e73c4b715` |
| Replacement summary.json SHA-256 | `d68ac1673043bafe3431c57c515220ee3e6903d85a1eb17a8a0c125a29f858ca` |
| Replacement verdict | `PASS — CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1_SEALED` (unchanged) |
| Verdict direction | `DEFECT_CORRECTION` (recorded-provenance correction; no change to verdict or claim) |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-141 row-generator self-hash repair |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion failed | `C1 HASH_CHAIN_INTEGRITY` (self-citation defect) |
| Audit finding tier | Tier 2 PASS_WITH_REWORD (defect at the recorded-self-hash level; cross-CR chain intact) |

## 3. Defect summary

The `CR129b_magnitude_lock_sha256` field recorded in both `CR129b_result.md` and `CR129b_summary.json` cited the value `c5751756c5e90e7f14e7254e8df95b32d01ba56a1876d7a4d8d12170ad13a112`. The actual SHA-256 of the corresponding lock JSON on disk is `8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR129b_result.md):
> CR129b_magnitude_lock_sha256                     = c5751756c5e90e7f14e7254e8df95b32d01ba56a1876d7a4d8d12170ad13a112

Replacement line:
> CR129b_magnitude_lock_sha256                     = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd
```

```text
Original field (in CR129b_summary.json, "magnitude_lock_sha256"):
> "magnitude_lock_sha256": "c5751756c5e90e7f14e7254e8df95b32d01ba56a1876d7a4d8d12170ad13a112"

Replacement field:
> "magnitude_lock_sha256": "8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd"
```

Additionally, an audit-trail header block is prepended to `CR129b_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR129b_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR129b law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR129b scope. The original "What CR129b Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T00:03:35Z | result.md `2eb5e87a...200fb22` / summary.json `98c90e83...114d58a` | CR129b runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `be49c1e3...3c4b715` / summary.json `d68ac167...9f858ca` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
