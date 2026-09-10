# REPLACEMENT_RECORD -- CR133 in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_result.md` and `CR133_summary.json` |
| Pre-qualifier result.md SHA-256 | `b6f50720a523a24e17400c1d49bb0351bdb7dd7f43bf7cade104967dfba7543d` |
| Pre-qualifier summary.json SHA-256 | `f1d1d24cec80168fc37dad9905cd6eac6dd51049fe55c052aadabe8963fa17fb` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/`) |
| Post-qualifier result.md SHA-256 | `cb3710c42af5d429794902f1406eb770fdf8e40f50ebef1a5fe0455fb5f8bdb9` |
| Post-qualifier summary.json SHA-256 | `41bedcd8f590a525ede786644014fafec23228f997b346959b194453230a56ca` |
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

CR133's in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `CR133_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `CR133_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on CR133 is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original CR133 scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | CR133 runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `b6f50720...ba7543d` / summary.json `f1d1d24c...3fa17fb` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `cb3710c4...5f8bdb9` / summary.json `41bedcd8...30a56ca` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
