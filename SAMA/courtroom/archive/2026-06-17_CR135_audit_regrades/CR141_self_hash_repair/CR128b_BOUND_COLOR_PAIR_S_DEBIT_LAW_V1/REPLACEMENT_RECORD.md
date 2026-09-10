# REPLACEMENT_RECORD — CR128b self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/CR128b_result.md` and `CR128b_summary.json` |
| Original result.md SHA-256 | `8dd3042c74952cb4b17ea700fe4db2e122d6913241f0b19ed817027be657fe08` |
| Original summary.json SHA-256 | `8cfa8eba2cee3c984c3a2629e52955cf8577411b38f50e0610eb2c02324155d1` |
| Original verdict | `PASS — CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `bd985cefbb3def3b436ebf5274d73919f707c99252284d64d492a755e104040d` |
| Replacement summary.json SHA-256 | `64a1776d914db8b333d004e73ec6fb8d3027efc9f9026206b3ac2fd56d5a8eb6` |
| Replacement verdict | `PASS — CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED` (unchanged) |
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

The `CR128b_law_lock_sha256` field recorded in both `CR128b_result.md` and `CR128b_summary.json` cited the value `9336468a668131f1ed4a1a9d1af61ebf9b019349709a750ee7359f94bdd26964`. The actual SHA-256 of the corresponding lock JSON on disk is `fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR128b_result.md):
> CR128b_law_lock_sha256                     = 9336468a668131f1ed4a1a9d1af61ebf9b019349709a750ee7359f94bdd26964

Replacement line:
> CR128b_law_lock_sha256                     = fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467
```

```text
Original field (in CR128b_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "9336468a668131f1ed4a1a9d1af61ebf9b019349709a750ee7359f94bdd26964"

Replacement field:
> "law_lock_sha256": "fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467"
```

Additionally, an audit-trail header block is prepended to `CR128b_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR128b_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR128b law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR128b scope. The original "What CR128b Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-15T22:39:56Z | result.md `8dd3042c...657fe08` / summary.json `8cfa8eba...24155d1` | CR128b runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `bd985cef...104040d` / summary.json `64a1776d...d5a8eb6` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
