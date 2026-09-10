# AUDIT: CR128b BOUND_COLOR_PAIR S_debit Law v1.0

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** Magnitude formula `|S| = M_native * (|a-b| + D) / R^4` is a 30/30 in-sample fit derived inductively; the `(|a-b| + D)` factor is admitted (line 87) to lack first-principles derivation; result.md cites wrong self-hash; sign rule was discovered separately from magnitude but presented as if jointly committed.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream CR119 + CR128 hashes verify. Self-cited `CR128b_law_lock_sha256 = 9336468a…` does NOT match actual file `fb9287cd…`. Downstream CRs use the correct `fb9287cd…`. Internal inconsistency in result.md only. |
| C2 FALSIFIER_PRECOMMITTED | PASS | "ONE single future asymmetric BCP row whose S_debit deviates from the formula by any non-zero rational" is concrete. |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | WC1/WC2 are read-only sanity checks. WC3 (exact rational arithmetic) is a methodology note. WC4 "sign rule derived separately from magnitude" — but admits magnitude was "pattern-spotted from 8 doublet pairs" then verified on remaining 22. That is the OPPOSITE of a wrong-control; it is an admission of bootstrap fitting. None of the WCs deletes a load-bearing piece and shows the law fails. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | Two-piece form (magnitude × sign) is parametrized over a family. The `(|a-b| + D)` factor in the numerator could equally be `(|a-b| + k)` for k = 1, 2, 4, 5 — only D=3 fits because it matches what was observed. Form was selected to match. Hidden DOF. |
| C5 IN_SAMPLE_DISCLOSED | PASS | WC6 explicitly states "Like CR128, the law was derived inductively from in-sample data." Note at line 87: "the (|a-b| + D) antisymmetric factor has [no] first-principles SAM derivation -- it is observed and locked but not yet derived." Honest. |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | Same as CR128: SEALED is overstated when only generator-consistency is demonstrated. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS WITH NIT | Cleaner than CR128 because symmetric (a,a) is hard-cut at the boundary, not punted to an appeal. |
| C8 TEXT_MATCHES_VERDICT | PASS | Numbers match. "Combined zero-parameter claim" line 25 is bold but technically defensible since both forms are locked. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | `law_committed_utc = 2026-06-15T22:39:56Z`, 10 minutes after CR128. No evidence the form predates the inspection of the data. WC4's admission that the sign rule was "observed independently" places its derivation post-inspection. |

## Specific demands

- REWORD line 6: add qualifier `_SEALED_AS_GENERATOR_CONSISTENCY_PENDING_FORWARD_BLIND`.
- REWORD line 97: `CR128b_law_lock_sha256 = 9336468a…` → actual `fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467`.
- REWORD line 25 ("Combined Zero-Parameter Claim"): qualify "Zero free parameters per row, post-lock; the form itself was selected from a family after inspecting the catalog."
- RETEST: out-of-sample run: train the magnitude form on 20 rows, predict the remaining 10. Currently 30/30 is whole-sample.
- RETEST: try alternate numerators `(|a-b| + k)` for k ∈ {1, 2, 4, 5}; demonstrate none fit. This is a real wrong-control absent from the WCs.
- APPEAL_CR: derive `(|a-b| + D)` from SAM algebra (line 87 admits it isn't derived).

## Quoted evidence

> "magnitude formula was pattern-spotted from 8 doublet pairs; sign rule (sign(first - second)) was observed independently. Both verified together against all 30 rows."

> "the (|a-b| + D) antisymmetric factor has a first-principles SAM derivation -- it is observed and locked but not yet derived."

> "Like CR128, the law was derived inductively from in-sample data."

> "CR128b_law_lock_sha256 = 9336468a668131f1ed4a1a9d1af61ebf9b019349709a750ee7359f94bdd26964" (does not match actual fb9287cd…)

## Verdict text

CR128b extends CR128 with the same honesty and the same defects: clean falsifier, but pattern-spotted form, no real wrong-controls, wrong self-hash citation, and an explicit confession that the numerator factor is not derived. Tier 2 for the same reasons as CR128. Manuscript must label this "observed S_debit form, forward-blind committed; SAM-algebra derivation open."
