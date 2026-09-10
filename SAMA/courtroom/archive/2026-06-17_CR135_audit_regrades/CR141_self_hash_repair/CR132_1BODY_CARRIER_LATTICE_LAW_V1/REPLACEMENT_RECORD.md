# REPLACEMENT_RECORD — CR132 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_result.md` and `CR132_summary.json` |
| Original result.md SHA-256 | `6897acca61d2407e8b1dc5ee36922be15e949ab1f37d8d6839d8c47d928ba078` |
| Original summary.json SHA-256 | `4495b9d557717bc67a309c5bccaeb6b159514c589041095b7bc9caed0c721145` |
| Original verdict | `PASS — CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `10a1ce00fd74287ecad702a2f78170ba206c315862357ad60fda3fc361c622df` |
| Replacement summary.json SHA-256 | `66899ba8825f63c8825c5db6c6757160deac5eacb47ddc0479a7d1b47f7801a9` |
| Replacement verdict | `PASS — CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED` (unchanged) |
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

The `CR132_law_lock_sha256` field recorded in both `CR132_result.md` and `CR132_summary.json` cited the value `f4811aa11df61be7a9fa01d09dc15775f816ab153313dccda022a3b92491ec17`. The actual SHA-256 of the corresponding lock JSON on disk is `fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR132_result.md):
> CR132_law_lock_sha256                     = f4811aa11df61be7a9fa01d09dc15775f816ab153313dccda022a3b92491ec17

Replacement line:
> CR132_law_lock_sha256                     = fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32
```

```text
Original field (in CR132_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "f4811aa11df61be7a9fa01d09dc15775f816ab153313dccda022a3b92491ec17"

Replacement field:
> "law_lock_sha256": "fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32"
```

Additionally, an audit-trail header block is prepended to `CR132_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR132_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR132 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR132 scope. The original "What CR132 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T00:22:22Z | result.md `6897acca...28ba078` / summary.json `4495b9d5...c721145` | CR132 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `10a1ce00...1c622df` / summary.json `66899ba8...f7801a9` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR132_1BODY_CARRIER_LATTICE_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
