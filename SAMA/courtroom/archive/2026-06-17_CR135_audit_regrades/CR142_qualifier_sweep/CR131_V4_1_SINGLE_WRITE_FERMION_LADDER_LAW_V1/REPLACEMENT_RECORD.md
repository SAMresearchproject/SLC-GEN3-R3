# REPLACEMENT_RECORD -- CR131 in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_result.md` and `CR131_summary.json` |
| Pre-qualifier result.md SHA-256 | `bddf0562c5bdd7bb0b0f4371ddbf7a3dc800d7e31be9ca95e7a7a22b1cf63cd6` |
| Pre-qualifier summary.json SHA-256 | `180eb2e8f8dbe12dbe87b2f641cd1e035239e30f5babf88e73b995e6ab3fee3d` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/`) |
| Post-qualifier result.md SHA-256 | `388a4029f0621d89234598cc6d1ee604e078700238e0271a6f8e816110e1d123` |
| Post-qualifier summary.json SHA-256 | `022db0daad533007756162351727cd583d9e4feeaa6e5d0c8abc3d7927978a1a` |
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

CR131's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR131_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR131_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR131 is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR131 scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR131 runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `bddf0562...cf63cd6` / summary.json `180eb2e8...b3fee3d` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `388a4029...0e1d123` / summary.json `022db0da...7978a1a` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
