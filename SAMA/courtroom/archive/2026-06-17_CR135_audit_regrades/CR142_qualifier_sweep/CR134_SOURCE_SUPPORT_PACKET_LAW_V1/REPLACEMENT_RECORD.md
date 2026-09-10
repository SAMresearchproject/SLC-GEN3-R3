# REPLACEMENT_RECORD -- CR134 in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_result.md` and `CR134_summary.json` |
| Pre-qualifier result.md SHA-256 | `d2fba3206f8810617a843faacac1a6804884cc647fc6dc2bac09bfd990191785` |
| Pre-qualifier summary.json SHA-256 | `35ce15eb9f9842777b778d169d1b1eeb9820ebc0bb6a857573274a6d476d4ecc` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/`) |
| Post-qualifier result.md SHA-256 | `46c77cd912b932125228c8923e4705c4d36d0c1e2df14294f44d086d37856aff` |
| Post-qualifier summary.json SHA-256 | `cd43d402f6306e955a955281fa4d04e7165c2d31938d09fbfc9255fd185877e4` |
| Verdict | unchanged |
| Verdict direction | `QUALIFIER_ADDITION` (headline visibility correction; no verdict change) |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-142 row-generator in-sample qualifier sweep |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion partially addressed | `C5 IN_SAMPLE_DISCLOSED` (was passing in WC3 but lacked headline visibility) |
| Audit finding tier | `Tier 2 PASS_WITH_REWORD` |

## 3. Defect summary

CR134's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR134_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR134_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR134 is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR134 scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR134 runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `d2fba320...0191785` / summary.json `35ce15eb...76d4ecc` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `46c77cd9...7856aff` / summary.json `cd43d402...85877e4` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
