# AUDIT: CR130 2-Body / 3-Body Structural Bridge + 4-Body Conjecture

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** The Newton-identity rewriting is mathematically tautological (it MUST hold by algebra; "76/76 match" is meaningless), the symmetric-group argument for "no linear antisymmetric at n≥3" is genuinely load-bearing — but the 4-body conjecture `M_4 = 48·Σa²` rests on extrapolating one of multiple possible prefactor patterns (R*n, R*D, etc.) explicitly conceded in WC4; the result.md cites the wrong self-hash.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream verified. Self-cited `CR130_bridge_lock_sha256 = 906a527a…` does NOT match actual `0a40209b…`. |
| C2 FALSIFIER_PRECOMMITTED | PASS WITH NIT | 4-body falsifier is concrete IF a 4-body row ever appears. The conjecture is "forward-blind only" with no in-sample data. This is genuinely the cleanest possible precommit because nothing is currently in-sample. |
| C3 WRONG_CONTROLS_LOAD_BEARING | WEAK | WC4 explicitly flags the prefactor scaling as unresolved. WC5 cleanly excludes n=2. WC3 separates structural argument from data. These are honest scope statements but not destructive controls. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | The 4-body prefactor is one of "R*n vs R*D vs other" (line 58 admits this). The conjecture picks R*n = 48 by extrapolation, not derivation. That is a parameter choice from a discrete set — a hidden DOF. |
| C5 IN_SAMPLE_DISCLOSED | PASS | WC6 explicitly: "CR130_PRED_1 is explicitly marked FORWARD_BLIND_NO_IN_SAMPLE_DATA. The conjecture rests on extrapolation, not derivation." |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | The in-sample bit (Newton identity) is trivially true; the structural-symmetry argument is novel and load-bearing; the 4-body conjecture is speculative. "SEALED" bundles all three. Should be split. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS | 4-body absence is explicitly non-falsifying; falsification triggers appeal CR. Clean. |
| C8 TEXT_MATCHES_VERDICT | FAIL | Line 67: "the Newton identity is an algebraic theorem, so it MUST hold for every row -- this is a sanity check, not a hypothesis test." Yet the result.md lists 76/76 Newton matches as a "prediction check" P1 PASS. Reporting a tautology as a PASS inflates the evidence count. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | PASS WITH NIT | The symmetric-group argument is genuinely independent of CR119 data (representation theory pre-exists). The 4-body conjecture is forward-blind. The 3-body rewriting depends on CR129's form, which depends on CR119 data. |

## Specific demands

- REWORD line 6: `_SEALED` → `_SEALED_REWRITING_AND_STRUCTURAL_ARGUMENT_FORWARD_BLIND_4BODY_CONJECTURE`.
- REWORD line 98: `CR130_bridge_lock_sha256 = 906a527a…` → actual `0a40209bc4c564a6437e8c1d01df2b294e35c7459340c244e28c3448bf73549c`.
- REWORD P1 in Predictions Checks: do not report the Newton identity match as a PASS — it is a tautology by line 67's own admission. Move it to a "sanity check" section.
- REWORD line 58: explicitly enumerate competing prefactor candidates {R*n, R*D, R²/D, …} and state which one is conjectured.
- RETEST: derive prefactor pattern from SAM dozenal algebra before promoting M_4 conjecture to a generator. Currently it is one extrapolation among many.
- APPEAL_CR: when (if) a 4-body partition row appears, run CR130-test; if fail, demote to per-n separately.

## Quoted evidence

> "the Newton identity is an algebraic theorem, so it MUST hold for every row -- this is a sanity check, not a hypothesis test."

> "**[PASS]** P1_newton_identity_holds_for_all_3body_rows" (tautology reported as a passing prediction)

> "Open question: the prefactor at n = 3 is R*D = 36, the conjectured n = 4 prefactor is R*α_H² = 48. These can be reconciled as R*n … but that is not the only possibility."

> "CR130_bridge_lock_sha256 = 906a527afd2ba5ad5f8cd1187c0aea03d03c9e03b2891c64b6b836ce23478c29" (actual: 0a40209b…)

## Verdict text

CR130's structural argument (linear-antisymmetric forbidden at n≥3 by S_n action on multisets) is the strongest piece of derivation in the suite — it actually justifies the 2→3 form change. But it is bundled with a Newton-identity tautology reported as a passing prediction (inflating the evidence count) and a 4-body conjecture with an admitted prefactor ambiguity. Tier 2. Manuscript can cite the structural argument freely; must cite the 4-body conjecture as "extrapolation, no in-sample data."
