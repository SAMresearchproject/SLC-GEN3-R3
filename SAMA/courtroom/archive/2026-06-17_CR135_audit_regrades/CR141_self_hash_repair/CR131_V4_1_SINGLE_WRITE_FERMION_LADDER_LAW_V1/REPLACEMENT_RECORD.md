# REPLACEMENT_RECORD — CR131 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_result.md` and `CR131_summary.json` |
| Original result.md SHA-256 | `5c3c148c7cfe0d64260ee16b4762d5d67256234d2af243a27e9856f220a0e213` |
| Original summary.json SHA-256 | `e90bb5848949ef1713e9df0abb6b6f4d9ea83c1a19399fde95bef9de3988fce7` |
| Original verdict | `PASS — CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `bddf0562c5bdd7bb0b0f4371ddbf7a3dc800d7e31be9ca95e7a7a22b1cf63cd6` |
| Replacement summary.json SHA-256 | `180eb2e8f8dbe12dbe87b2f641cd1e035239e30f5babf88e73b995e6ab3fee3d` |
| Replacement verdict | `PASS — CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED` (unchanged) |
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

The `CR131_law_lock_sha256` field recorded in both `CR131_result.md` and `CR131_summary.json` cited the value `9fb532810bcc97a3f6c18ca176f2000fa3ad1c9534badeab61a7e6212f9e8765`. The actual SHA-256 of the corresponding lock JSON on disk is `2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR131_result.md):
> CR131_law_lock_sha256                     = 9fb532810bcc97a3f6c18ca176f2000fa3ad1c9534badeab61a7e6212f9e8765

Replacement line:
> CR131_law_lock_sha256                     = 2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb
```

```text
Original field (in CR131_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "9fb532810bcc97a3f6c18ca176f2000fa3ad1c9534badeab61a7e6212f9e8765"

Replacement field:
> "law_lock_sha256": "2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb"
```

Additionally, an audit-trail header block is prepended to `CR131_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR131_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR131 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR131 scope. The original "What CR131 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T00:14:20Z | result.md `5c3c148c...0a0e213` / summary.json `e90bb584...988fce7` | CR131 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `bddf0562...cf63cd6` / summary.json `180eb2e8...b3fee3d` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
