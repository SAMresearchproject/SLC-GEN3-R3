# AUDIT: CR129c 3-Body Universal Generator (GROUND_BARYON_3BODY Extension)

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** 44/44 GROUND_BARYON match including 13/13 REJECTED_FAKE_CLOSURE rows is genuinely impressive in-sample evidence for operator-class universality of `M = 36*Σa²` — but the result.md still cites the wrong self-hash, "universal" is overclaim from 2 operator classes, and the generator/filter separation is post-hoc interpretation, not a falsifiable claim.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream CR119 + CR129 verified. Self-cited `CR129c_universal_lock_sha256 = d823faba…` does NOT match actual `bfd5ab8c…`. |
| C2 FALSIFIER_PRECOMMITTED | PASS | "ONE single future 3-body row whose M_native differs from the formula by any non-zero integer" — concrete. |
| C3 WRONG_CONTROLS_LOAD_BEARING | WEAK PASS | WC3 (REJECTED rows included rather than filtered out) IS a genuine wrong-control gesture — if generator were entangled with filter, including REJECTED would have surfaced violations; it did not (13/13 match). This is the strongest wrong-control in the suite. WC4 (formula NOT promoted to other body counts) is correct scope discipline. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | PARTIAL FAIL | Form-choice is inherited from CR129. CR129c does no independent derivation. The "universal" promotion is observational; it doesn't add new derivation, only new data. |
| C5 IN_SAMPLE_DISCLOSED | PASS | WC5 admits "derived from 120 in-sample rows … CR129c_PRED_1 commits the law for forward-blind testing on FUTURE 3-body rows where overfit cannot operate." |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | "UNIVERSAL 3-BODY" is too strong from 2 operator classes (120 rows). If a 3rd 3-body operator class ever appears and fails, the "universal" claim collapses to per-class. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS | Cleanly states one violation demotes to per-class. |
| C8 TEXT_MATCHES_VERDICT | BOUNDARY | "UNIVERSAL" is a strong word for "two operator classes tested in-sample." Manuscript should say "operator-class agnostic across 2 tested classes." |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | The form was set by CR129 by inspecting OCTET data. CR129c's contribution is to test on GROUND_BARYON — but the inspector knew the formula already worked on OCTET 3-body. There is no precommit BEFORE looking at GROUND_BARYON masses. The test is "in-sample" in the sense that all GROUND_BARYON masses were observable before CR129c. |

## Specific demands

- REWORD line 6: `_SEALED` → `_PROMOTED_PROVISIONAL` until forward-blind row in a 3rd 3-body operator class confirms.
- REWORD lines 96–97: `CR129c_universal_lock_sha256 = d823faba…` → actual `bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090`.
- REWORD "UNIVERSAL" → "OPERATOR-CLASS AGNOSTIC ACROSS 2 TESTED CLASSES" throughout.
- REWORD the generator/filter framing (lines 42–49): qualify as "observed structural separation" not "structurally separable" (which sounds like a derivation).
- RETEST: when CR119 gains a 3rd 3-body operator class, the universal claim is properly tested. Currently it is "universal" only in a population of 2.
- APPEAL_CR: derive why M_native is filter-independent. The structural observation is striking but not derived.

## Quoted evidence

> "the M_native formula is the GENERATOR; stability is the FILTER" (presented as derived; actually observed)

> "13 of 13 REJECTED_FAKE_CLOSURE rows in GROUND_BARYON_3BODY match the formula. This is the structural reveal" (in-sample observation)

> "Universal 3-body M_native generator … REGARDLESS of operator_class or stability_status" (from N=2 classes)

> "CR129c_universal_lock_sha256 = d823fabac81e11cff2e97c5ea7c7b47019c6f3c123f40f82e8fb367868263d34" (actual: bfd5ab8c…)

## Verdict text

CR129c earns the strongest wrong-control in the suite (REJECTED rows would have flagged generator/filter entanglement; they did not). That is genuine evidence. But "universal" from 2 operator classes is overreach, the result.md cites the wrong self-hash, and the generator/filter separation is an interpretation, not a derivation. Tier 2. Manuscript: cite as "operator-class agnostic in 2/2 tested 3-body classes; generator/filter separation observed".
