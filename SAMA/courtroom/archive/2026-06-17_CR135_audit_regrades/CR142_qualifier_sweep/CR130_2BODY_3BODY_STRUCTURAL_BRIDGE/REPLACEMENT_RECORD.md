# REPLACEMENT_RECORD -- CR130 in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_result.md` and `CR130_summary.json` |
| Pre-qualifier result.md SHA-256 | `d798ea72439606b0ddb5b241e30ea0555cd04a8ee6ff605357dc6c03184e498a` |
| Pre-qualifier summary.json SHA-256 | `8189ad23dc91047cfddf8a8b63b45e62ed80af94868e966c77b3de1f27c08eea` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/`) |
| Post-qualifier result.md SHA-256 | `ac38679e3c150449aa15def37a438ec6f600cd303a1969bf5faba4c29ada077a` |
| Post-qualifier summary.json SHA-256 | `21ab0933a683a54628e1bf598a9449519e129d6d2daa6bc47e8eb4fdbb2832e0` |
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

CR130's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR130_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR130_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR130 is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR130 scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR130 runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `d798ea72...84e498a` / summary.json `8189ad23...7c08eea` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `ac38679e...ada077a` / summary.json `21ab0933...b2832e0` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
