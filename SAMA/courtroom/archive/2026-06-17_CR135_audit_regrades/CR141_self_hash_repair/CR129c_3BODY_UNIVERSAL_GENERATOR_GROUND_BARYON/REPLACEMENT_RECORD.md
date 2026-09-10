# REPLACEMENT_RECORD — CR129c self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_result.md` and `CR129c_summary.json` |
| Original result.md SHA-256 | `b37cb070b8880de7c8fb511e8106279dd4a1f365039262cd61592152bce80929` |
| Original summary.json SHA-256 | `5f63dcf7e3493225ed5df44141c9b0707fed0844e8c76ffe8dd994a22cbc78f7` |
| Original verdict | `PASS — CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `7d9f2c7342252a9b60d63086400fe8153f71fec41ec9953852ba0760a2333a6a` |
| Replacement summary.json SHA-256 | `e5d597a13d89a444f51e25550e564d75b958ca08a329969a95fcb0dd6c75079d` |
| Replacement verdict | `PASS — CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED` (unchanged) |
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

The `CR129c_universal_lock_sha256` field recorded in both `CR129c_result.md` and `CR129c_summary.json` cited the value `d823fabac81e11cff2e97c5ea7c7b47019c6f3c123f40f82e8fb367868263d34`. The actual SHA-256 of the corresponding lock JSON on disk is `bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR129c_result.md):
> CR129c_universal_lock_sha256                     = d823fabac81e11cff2e97c5ea7c7b47019c6f3c123f40f82e8fb367868263d34

Replacement line:
> CR129c_universal_lock_sha256                     = bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090
```

```text
Original field (in CR129c_summary.json, "universal_lock_sha256"):
> "universal_lock_sha256": "d823fabac81e11cff2e97c5ea7c7b47019c6f3c123f40f82e8fb367868263d34"

Replacement field:
> "universal_lock_sha256": "bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090"
```

Additionally, an audit-trail header block is prepended to `CR129c_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR129c_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR129c law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR129c scope. The original "What CR129c Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-15T23:04:43Z | result.md `b37cb070...ce80929` / summary.json `5f63dcf7...cbc78f7` | CR129c runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `7d9f2c73...2333a6a` / summary.json `e5d597a1...c75079d` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
