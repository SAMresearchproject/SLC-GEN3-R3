# AUDIT: CR128 BOUND_COLOR_PAIR Mass Law v1.0

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** The law is a 36/36 in-sample retrofit dressed up with a clean forward-blind falsifier; honest about its inductive origin, but the result.md cites the wrong self-hash for the law-lock file, the partition algebra is asserted not derived, and the functional form `R*a*b + D*|a-b|` is one of several plausible 2-parameter quadratics that could have fit 21 distinct pairs.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream CR119/CR127 SHAs verify against artifacts inside The_Courtroom. BUT the self-cited `CR128_law_lock_sha256 = d8ed19c1…` does NOT match the actual file hash `0f62d6b4…`. Downstream CRs (CR128b/CR129) use the actual `0f62d6b4…`, so the chain is intact for users — but the result.md is internally inconsistent with itself. |
| C2 FALSIFIER_PRECOMMITTED | PASS | "ONE single future BCP row whose M_native deviates from the formula by any non-zero integer" is concrete and one-violation. |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | All 7 WCs are either sanity checks (CR119 read-only) or descriptive scope statements. None DELETE a load-bearing input and demonstrate the test breaks. WC3 ("law derived from data not first principles") is a confession, not a control. No WC tests, e.g., randomized partition labels, alternate algebras, or alternate functional forms. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | `free_parameters_at_test = 0` is technically true post-lock, but the functional form `R*a*b + D*|a-b|` was selected after inspecting the catalog. Plausible alternatives that could have fit 21 pairs: `R*(a*b + |a-b|*k)` for various k; `R*a*b + D*(a+b-2*min(a,b))`; piecewise rules. Selection from a family of forms is itself a hidden degree of freedom. |
| C5 IN_SAMPLE_DISCLOSED | PASS (rare) | Explicit honesty: "Law v1.0 was derived inductively by inspecting BOUND_COLOR_PAIR cluster centers in CR127… could in principle have been overfit to 36 data points." WC3 repeats this. This is courtroom-grade disclosure. |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | Verdict text says "SEALED" without qualifier. Evidence supports "SEALED_AS_GENERATOR_CONSISTENCY_PENDING_FORWARD_BLIND" — the actual test resolves only when CR119 gains new BCP rows. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | BOUNDARY | "algebra extension warrants an appeal CR, not a violation of v1.0" is potentially wide: any future row failing the formula could be reclassified as an "algebra extension" if the partition contains a new element. The bright line is drawn around the current 8-element algebra; if any 9th element appears, the falsifier is silently demoted. |
| C8 TEXT_MATCHES_VERDICT | PASS WITH NIT | Headline numbers are defensible. But the pair-coverage table shows 21/36 distinct pairs — 15 algebra pairs are UNTESTED in-sample. Result.md does not flag that 42% of the algebra is unverified. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | `law_committed_utc = 2026-06-15T22:29:48Z`. No precommit timestamp BEFORE the data check. The formula was derived from CR127 inspection (WC3) — so the form post-dates the data. No precommit hash predating the inspection exists. The 0-parameter claim is honest only on a forward-blind basis, not on construction order. |

## Specific demands

- REWORD line 6: `CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED` → `CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED_AS_GENERATOR_CONSISTENCY (in-sample retrofit; forward-blind test pending)`.
- REWORD line 89: `CR128_law_lock_sha256 = d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a` → actual `0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871`.
- REWORD pair-coverage section: add explicit "15 of 36 algebra pairs unobserved; formula is uncrossed there".
- RETEST: a true wrong-control where the functional form is randomized (e.g., try `R*(a+b)^2 + D*|a-b|` and report it fails 36/36). Currently no alternate-form WC exists.
- RETEST: forward-blind run on a held-out subset (e.g., re-derive form on 20 rows; verify match on remaining 16) before claiming generator status.
- APPEAL_CR: bound the algebra-extension escape: precommit which classes of future deviation are "extension" vs "violation". Currently the line is post-hoc.

## Quoted evidence

> "Law v1.0 was derived inductively by inspecting BOUND_COLOR_PAIR cluster centers in CR127."

> "WC3_law_derived_from_data_not_first_principles … in-sample 100% match does not prove first-principles derivation, only generator consistency."

> "Distinct (a, b) pairs observed: **21** … Total possible unordered pairs in algebra: 36"

> "CR128_law_lock_sha256 = d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a" (does not match actual file hash 0f62d6b4…)

> "rows containing an algebra extension (which warrants an appeal CR, not a violation)"

## Verdict text

CR128 is the courtroom's most honest in-sample retrofit so far — it explicitly disclaims first-principles derivation and locks a concrete forward-blind falsifier. Tier 2 instead of Tier 1 because (a) the self-hash citation in the result.md is wrong, (b) no real wrong control attacks the functional-form choice, and (c) the algebra-extension escape hatch is wide enough that a contrary future row could be sidestepped. Manuscript may cite the formula but must label it "generator-consistency v1.0, forward-blind test pending."
