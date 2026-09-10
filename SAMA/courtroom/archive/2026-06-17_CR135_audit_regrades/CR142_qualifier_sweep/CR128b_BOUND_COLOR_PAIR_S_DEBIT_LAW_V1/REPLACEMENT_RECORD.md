# REPLACEMENT_RECORD -- CR128b in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/CR128b_result.md` and `CR128b_summary.json` |
| Pre-qualifier result.md SHA-256 | `bd985cefbb3def3b436ebf5274d73919f707c99252284d64d492a755e104040d` |
| Pre-qualifier summary.json SHA-256 | `64a1776d914db8b333d004e73ec6fb8d3027efc9f9026206b3ac2fd56d5a8eb6` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/`) |
| Post-qualifier result.md SHA-256 | `e6028e172a82db19457df93475a8b70797188c747f299e616f4a9e7172a33549` |
| Post-qualifier summary.json SHA-256 | `9bd613c3b4d6db390d35afa2250f9f34aadc9e42f7c7382dd204369ce9f8b192` |
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

CR128b's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR128b_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR128b_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR128b is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR128b scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR128b runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `bd985cef...104040d` / summary.json `64a1776d...d5a8eb6` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `e6028e17...2a33549` / summary.json `9bd613c3...9f8b192` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
