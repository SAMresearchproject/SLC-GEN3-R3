# REPLACEMENT_RECORD — CR130 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_result.md` and `CR130_summary.json` |
| Original result.md SHA-256 | `3be27eb9191028b68e734d9749e38b9c96c8f0ea08ff186bcc55bfad2310c9a3` |
| Original summary.json SHA-256 | `22928c5fdde7cc9cbd9cc8f59a2f7dab392dcc03e1b5507e964904763931ad0f` |
| Original verdict | `PASS — CR130_2BODY_3BODY_STRUCTURAL_BRIDGE_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `d798ea72439606b0ddb5b241e30ea0555cd04a8ee6ff605357dc6c03184e498a` |
| Replacement summary.json SHA-256 | `8189ad23dc91047cfddf8a8b63b45e62ed80af94868e966c77b3de1f27c08eea` |
| Replacement verdict | `PASS — CR130_2BODY_3BODY_STRUCTURAL_BRIDGE_SEALED` (unchanged) |
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

The `CR130_bridge_lock_sha256` field recorded in both `CR130_result.md` and `CR130_summary.json` cited the value `906a527afd2ba5ad5f8cd1187c0aea03d03c9e03b2891c64b6b836ce23478c29`. The actual SHA-256 of the corresponding lock JSON on disk is `0a40209bc4c564a6437e8c1d01df2b294e35c7459340c244e28c3448bf73549c`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR130_result.md):
> CR130_bridge_lock_sha256                     = 906a527afd2ba5ad5f8cd1187c0aea03d03c9e03b2891c64b6b836ce23478c29

Replacement line:
> CR130_bridge_lock_sha256                     = 0a40209bc4c564a6437e8c1d01df2b294e35c7459340c244e28c3448bf73549c
```

```text
Original field (in CR130_summary.json, "bridge_lock_sha256"):
> "bridge_lock_sha256": "906a527afd2ba5ad5f8cd1187c0aea03d03c9e03b2891c64b6b836ce23478c29"

Replacement field:
> "bridge_lock_sha256": "0a40209bc4c564a6437e8c1d01df2b294e35c7459340c244e28c3448bf73549c"
```

Additionally, an audit-trail header block is prepended to `CR130_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR130_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR130_2BODY_3BODY_STRUCTURAL_BRIDGE_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR130 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR130 scope. The original "What CR130 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-15T22:59:47Z | result.md `3be27eb9...310c9a3` / summary.json `22928c5f...931ad0f` | CR130 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `d798ea72...84e498a` / summary.json `8189ad23...7c08eea` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR130_2BODY_3BODY_STRUCTURAL_BRIDGE.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
