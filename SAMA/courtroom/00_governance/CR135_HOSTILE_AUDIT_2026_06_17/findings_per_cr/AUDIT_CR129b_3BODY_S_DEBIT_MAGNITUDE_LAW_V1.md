# AUDIT: CR129b 3-Body S_debit Magnitude Law v1.0

**Tier verdict:** 3 — REGRADE_TO_BOUNDARY
**Headline finding:** This is the WORST in-sample retrofit in the suite — three failed hypotheses (pure pairwise → 1/8 surcharge → 9/8 surcharge) were tried, all rejected after data inspection, and the final form `|S| = M·(4q_eff+D)/(4R⁴)` with `q_eff = R if q=0 else q_abs` was hand-tuned with a special-case branch for q=0; the `17/16` coefficient is a post-hoc unit-pegged decomposition `(R+D+α_H)/α_H⁴` that emerged AFTER user-directed exploration; the sign rule for q≥1 is explicitly OPEN.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream hashes verify. Self-cited `CR129b_magnitude_lock_sha256 = c5751756…` does NOT match actual `8c3d0eb7…`. |
| C2 FALSIFIER_PRECOMMITTED | BOUNDARY | Magnitude and q=0 sign falsifiers are concrete. But the sign rule for q≥1 is explicitly OPEN (WC5), so the law has a hole the size of 59 of 76 rows that future contrary data cannot falsify cleanly. |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | WC3 and WC4 are confessions of failed hypotheses (pairwise rejected, 1/8 rejected). These are not wrong-controls — they are the iteration history. A wrong-control would delete the q_eff branch and show the formula fails on q=0 rows; not demonstrated. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | The `q_eff = R if q_abs == 0 else q_abs` switch is a piecewise branch — it is by inspection a 1-parameter choice (the threshold and the substitute value), tuned to match the 17 q=0 rows. The "17/16 = (R+D+α_H)/α_H⁴" decomposition is a numerology fit: 17 has exactly the algebra constants summing to it (12+3+2). This is post-hoc pattern matching, not zero-parameter derivation. The Stage 2' (9/8) result "OVERSHOOTS by 18/17 uniformly" is a smoking gun: a constant 18/17 ratio between proposed and actual demands a coefficient adjustment of exactly 17/18 — i.e., the 17/16 was reverse-engineered. |
| C5 IN_SAMPLE_DISCLOSED | PASS WITH NIT | Stage-decomposition table (lines 12–17) is candid that the final form was the 4th attempt. Explicit "USER-DIRECTED LOCK" annotation. But the result.md frames this as "honest forensics" when it is iterative curve-fitting. |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | FAIL | SEALED is wrong. This is at best a BOUNDARY result: 76/76 magnitude match with branch, but the q≥1 sign rule is "open." A pass requires a closed rule; an open rule is a hole, not a victory. The CR is honest about the hole but seals anyway. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | FAIL | "Sign rule for q_abs >= 1 is OPEN; observation of any sign for q>=1 rows is consistent with v1.0" — this is the broadest escape hatch in the suite. Any future row with wrong sign at q≥1 cannot falsify the law because v1.0 explicitly doesn't claim. The "free_parameters = 0" claim is technically true only because the sign for 59/76 rows is unconstrained. |
| C8 TEXT_MATCHES_VERDICT | FAIL | Line 124: "S_debit is FULLY DETERMINED (both magnitude and sign) by (M_native, q_abs, q_sign) and the constants R, D, alpha_H. Zero free parameters per row." — This is overstated. The sign for q≥1 is NOT determined by the law itself; it is read from q_sign in the data row. That is data, not a derivation. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | The whole stage-decomposition table proves the formula was iterated against the data 4 times. `law_committed_utc = 2026-06-16T00:03:35Z` is post-iteration. |

## Specific demands

- REWORD line 6: `_SEALED` → `_PROVISIONAL_BOUNDARY_q0_LOCKED_qge1_SIGN_OPEN`.
- REWORD line 124 ("FULLY DETERMINED"): replace with "magnitude fully determined for 76/76; sign locked for q=0 (17 rows); sign for q≥1 (59 rows) is read from input q_sign, not predicted."
- REWORD line 144: `CR129b_magnitude_lock_sha256 = c5751756…` → actual `8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd`.
- REWORD line 14 ("user proposal"): manuscript must NOT cite this as a derivation. The "user-directed" annotation is a tell that the form was suggested, not derived.
- RETEST: forward-blind test of the q=0 17/16 claim on a freshly-generated q=0 OCTET row not in CR119. Until then, the closed-form claim is in-sample only.
- RETEST: derive the sign rule for q≥1 BEFORE sealing. Currently it is an open hole large enough to drive a truck through.
- APPEAL_CR: CR129b-v1.1 with a closed sign rule for all q values, and a first-principles derivation of why `q_eff = R` at q=0 rather than another constant.

## Quoted evidence

> "Stage 1 (pure pairwise): INSUFFICIENT. Stage 2 (1/8 global surcharge): INSUFFICIENT -- WRONG SCALE. Stage 2-refined (9/8 surcharge as user proposed): OVERSHOOTS by exact factor 18/17 uniformly. Stage 3 (q_abs slot relative to mass): DECISIVE."

> "S(q=0) = (17/16) * M / R^3 -- user pointed directly to this clean ratio after the 9/8 was found to overshoot."

> "Sign rule for q_abs >= 1 is OPEN; observation of any sign for q>=1 rows is consistent with v1.0."

> "USER-DIRECTED LOCK: this is the cleanest closed form for the q=0 case."

## Verdict text

CR129b is the suite's most honest about its iteration but also its most retrofit. Four hypotheses were tried; the final one needs a piecewise q_eff branch and a special q=0 coefficient that aligns with the algebra constants only after the data forced the value. The "0 free parameters" claim is materially overstated because the sign at q≥1 is supplied by the data, and the q=0 coefficient was reverse-engineered from the 18/17 overshoot. Regrade to Tier 3 — BOUNDARY at best. Manuscript MUST NOT cite the universal sign rule or the 17/16 closed form as a prediction; cite them as observed regularities pending forward-blind test.
