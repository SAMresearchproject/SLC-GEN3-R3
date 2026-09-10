# REPLACEMENT_RECORD — CR134 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_result.md` and `CR134_summary.json` |
| Original result.md SHA-256 | `4b3b6bc2b478e153c506b350792cd1acd3054a783b540cc873c08903523131fd` |
| Original summary.json SHA-256 | `43381e4db213a40515479429929d64bc9a40ca70c598899349d63bc8c6ebb482` |
| Original verdict | `PASS — CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `d2fba3206f8810617a843faacac1a6804884cc647fc6dc2bac09bfd990191785` |
| Replacement summary.json SHA-256 | `35ce15eb9f9842777b778d169d1b1eeb9820ebc0bb6a857573274a6d476d4ecc` |
| Replacement verdict | `PASS — CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED` (unchanged) |
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

The `CR134_law_lock_sha256` field recorded in both `CR134_result.md` and `CR134_summary.json` cited the value `4aa8f02b1e1bfb1e3db0f92aa80ce24e098c10d7c890ed55de04504f8d48e342`. The actual SHA-256 of the corresponding lock JSON on disk is `6ab4944278530a359382303a4bacef4a1bcc8a939b7307925615a525aadcd997`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR134_result.md):
> CR134_law_lock_sha256                     = 4aa8f02b1e1bfb1e3db0f92aa80ce24e098c10d7c890ed55de04504f8d48e342

Replacement line:
> CR134_law_lock_sha256                     = 6ab4944278530a359382303a4bacef4a1bcc8a939b7307925615a525aadcd997
```

```text
Original field (in CR134_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "4aa8f02b1e1bfb1e3db0f92aa80ce24e098c10d7c890ed55de04504f8d48e342"

Replacement field:
> "law_lock_sha256": "6ab4944278530a359382303a4bacef4a1bcc8a939b7307925615a525aadcd997"
```

Additionally, an audit-trail header block is prepended to `CR134_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR134_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR134 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR134 scope. The original "What CR134 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T00:32:19Z | result.md `4b3b6bc2...23131fd` / summary.json `43381e4d...6ebb482` | CR134 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `d2fba320...0191785` / summary.json `35ce15eb...76d4ecc` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR134_SOURCE_SUPPORT_PACKET_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
