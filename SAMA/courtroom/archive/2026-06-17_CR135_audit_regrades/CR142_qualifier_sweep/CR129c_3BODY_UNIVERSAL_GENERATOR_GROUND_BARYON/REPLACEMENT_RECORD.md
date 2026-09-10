# REPLACEMENT_RECORD -- CR129c in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_result.md` and `CR129c_summary.json` |
| Pre-qualifier result.md SHA-256 | `7d9f2c7342252a9b60d63086400fe8153f71fec41ec9953852ba0760a2333a6a` |
| Pre-qualifier summary.json SHA-256 | `e5d597a13d89a444f51e25550e564d75b958ca08a329969a95fcb0dd6c75079d` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/`) |
| Post-qualifier result.md SHA-256 | `924e7eedf5ea097bdda2891589d4c209df74d53d5d479802e67515eb74ad0d5b` |
| Post-qualifier summary.json SHA-256 | `5de2f436e9920a610d4a0ef464535a5c099c8779330893305def3a96470b6fac` |
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

CR129c's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR129c_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR129c_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR129c is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR129c scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR129c runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `7d9f2c73...2333a6a` / summary.json `e5d597a1...c75079d` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `924e7eed...4ad0d5b` / summary.json `5de2f436...70b6fac` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
