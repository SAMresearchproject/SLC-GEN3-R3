# REPLACEMENT_RECORD — CR133 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_result.md` and `CR133_summary.json` |
| Original result.md SHA-256 | `8b02eb267930bd04ab7500ec54395dc26e50d060e8e20c43594152066c1861bf` |
| Original summary.json SHA-256 | `82fa822aadf0b40042beec57c3626daf5ce4310040ac7ffd0399c4a336e341d7` |
| Original verdict | `PASS — CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `b6f50720a523a24e17400c1d49bb0351bdb7dd7f43bf7cade104967dfba7543d` |
| Replacement summary.json SHA-256 | `f1d1d24cec80168fc37dad9905cd6eac6dd51049fe55c052aadabe8963fa17fb` |
| Replacement verdict | `PASS — CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED` (unchanged) |
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

The `CR133_law_lock_sha256` field recorded in both `CR133_result.md` and `CR133_summary.json` cited the value `3adf93b81f23c0c3b943fda9dcde947aeb96ac0e01162813b37a40163f0f8cee`. The actual SHA-256 of the corresponding lock JSON on disk is `1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR133_result.md):
> CR133_law_lock_sha256                     = 3adf93b81f23c0c3b943fda9dcde947aeb96ac0e01162813b37a40163f0f8cee

Replacement line:
> CR133_law_lock_sha256                     = 1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4
```

```text
Original field (in CR133_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "3adf93b81f23c0c3b943fda9dcde947aeb96ac0e01162813b37a40163f0f8cee"

Replacement field:
> "law_lock_sha256": "1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4"
```

Additionally, an audit-trail header block is prepended to `CR133_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR133_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR133 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR133 scope. The original "What CR133 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T00:28:35Z | result.md `8b02eb26...c1861bf` / summary.json `82fa822a...6e341d7` | CR133 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `b6f50720...ba7543d` / summary.json `f1d1d24c...3fa17fb` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
