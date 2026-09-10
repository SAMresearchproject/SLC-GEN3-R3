# REPLACEMENT_RECORD — CR128 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_result.md` and `CR128_summary.json` |
| Original result.md SHA-256 | `0a4ebfe6c3a17f10f03909d1b5dfc4c9532b34132c9e306dfd9fa1b724970e10` |
| Original summary.json SHA-256 | `6c7b50f2bd04e80014a7bc0c875ca0267dd2e6dbd7244a721fcd31a23bd06649` |
| Original verdict | `PASS — CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `4fca02422c0302712d1cfb1c4e34a93fabeba9651b11d3c2f52d77fb04f40b1f` |
| Replacement summary.json SHA-256 | `ef0ab18c554b327c8c7a822671dc8fa2ecb7c74b59e2e1d00e7b432e5ce438aa` |
| Replacement verdict | `PASS — CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED` (unchanged) |
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

The `CR128_law_lock_sha256` field recorded in both `CR128_result.md` and `CR128_summary.json` cited the value `d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a`. The actual SHA-256 of the corresponding lock JSON on disk is `0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR128_result.md):
> CR128_law_lock_sha256                     = d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a

Replacement line:
> CR128_law_lock_sha256                     = 0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871
```

```text
Original field (in CR128_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a"

Replacement field:
> "law_lock_sha256": "0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871"
```

Additionally, an audit-trail header block is prepended to `CR128_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR128_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR128 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR128 scope. The original "What CR128 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-15T22:29:48Z | result.md `0a4ebfe6...4970e10` / summary.json `6c7b50f2...bd06649` | CR128 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `4fca0242...4f40b1f` / summary.json `ef0ab18c...ce438aa` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR128_BOUND_COLOR_PAIR_MASS_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
