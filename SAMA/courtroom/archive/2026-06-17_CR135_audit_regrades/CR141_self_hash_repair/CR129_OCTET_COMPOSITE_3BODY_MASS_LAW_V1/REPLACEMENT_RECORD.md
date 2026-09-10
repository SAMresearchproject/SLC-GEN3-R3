# REPLACEMENT_RECORD — CR129 self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_result.md` and `CR129_summary.json` |
| Original result.md SHA-256 | `836e8fbcfa1209d3dda1bc3947f684d65a613001282472392e397a84e3f2cbf4` |
| Original summary.json SHA-256 | `30e12eb8bfc6d404541a9748c2c6357244352dc8823c0e7827a3db3a0cdb4aae` |
| Original verdict | `PASS — CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `fdac1eabf889c094d44d6c12bf0b592306f7786f74a52a3c11223120ddf354e9` |
| Replacement summary.json SHA-256 | `505e2aa33eac613928f74852afc9b01b2eebbbb2963cbd563641fcbbca58a78e` |
| Replacement verdict | `PASS — CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED` (unchanged) |
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

The `CR129_law_lock_sha256` field recorded in both `CR129_result.md` and `CR129_summary.json` cited the value `210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360`. The actual SHA-256 of the corresponding lock JSON on disk is `041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in CR129_result.md):
> CR129_law_lock_sha256                     = 210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360

Replacement line:
> CR129_law_lock_sha256                     = 041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710
```

```text
Original field (in CR129_summary.json, "law_lock_sha256"):
> "law_lock_sha256": "210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360"

Replacement field:
> "law_lock_sha256": "041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710"
```

Additionally, an audit-trail header block is prepended to `CR129_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `CR129_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying CR129 law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original CR129 scope. The original "What CR129 Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-15T22:50:14Z | result.md `836e8fbc...3f2cbf4` / summary.json `30e12eb8...cdb4aae` | CR129 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `fdac1eab...df354e9` / summary.json `505e2aa3...a58a78e` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
