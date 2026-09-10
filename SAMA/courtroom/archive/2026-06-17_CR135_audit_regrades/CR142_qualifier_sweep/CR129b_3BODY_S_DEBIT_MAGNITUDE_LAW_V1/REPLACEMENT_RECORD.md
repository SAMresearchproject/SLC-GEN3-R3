# REPLACEMENT_RECORD -- CR129b in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_result.md` and `CR129b_summary.json` |
| Pre-qualifier result.md SHA-256 | `be49c1e301a1741e4daa9350db10eb36ce61c02f462271690ecdad1e73c4b715` |
| Pre-qualifier summary.json SHA-256 | `d68ac1673043bafe3431c57c515220ee3e6903d85a1eb17a8a0c125a29f858ca` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/`) |
| Post-qualifier result.md SHA-256 | `be3e314b46c5532b8be755ebbb0b699b8c55fbb872bb9cad96e4b06f2c765efc` |
| Post-qualifier summary.json SHA-256 | `57396c8ac8d63b9e67af6de28f2a839e2940feec532a2a9f896399296dcccf80` |
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

CR129b's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR129b_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR129b_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR129b is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR129b scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR129b runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `be49c1e3...3c4b715` / summary.json `d68ac167...9f858ca` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `be3e314b...c765efc` / summary.json `57396c8a...dcccf80` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
