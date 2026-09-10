# AUDIT: CR133 OUTER_BINARY_NEUTRAL Neutral-Fermion Ladder Law v1.0

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** 24/24 in-sample match for `M = partition · R^depth / 8` with full coverage of {1,2,3,4,6,8,9,12} × {0,1,2} = 24 cells is genuinely impressive — but the test set EXACTLY equals the 24-cell lookup, leaving zero residual degrees of freedom and zero genuine test rows; the K=1/8 is admitted to have been hypothesized AFTER asking "do we get lucky with C1=1?" then pivoted; result.md self-hash is wrong.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | CR119 + CR131 upstream hashes verified. Self-cited `CR133_law_lock_sha256 = 3adf93b8…` does NOT match actual `1e7e08d8…`. |
| C2 FALSIFIER_PRECOMMITTED | PASS | "ONE future OUTER_BINARY_NEUTRAL row whose M_native deviates" — concrete. |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | WC3 is the C1 pivot history (1 → 1/8). WC4–WC6 are scope statements. None destructively tests the law. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | PARTIAL FAIL | Once K=1/8 is set, the formula has 0 free parameters and predicts all 24 cells exactly. But K=1/8 was fit AFTER C1=1 didn't reproduce the data (line 12, WC3). The form `partition · R^depth · K` is shared with CR131 but K is per-class. So at the family level, K is the free parameter. |
| C5 IN_SAMPLE_DISCLOSED | PASS | WC5: "Formula was derived from the 24-row ratio table". WC3: explicit pivot history. Honest. |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | 24-cell test on a 24-cell lookup is exhaustive in-sample but zero out-of-sample. SEALED overstates the evidence. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS WITH NIT | Charged OUTER_BINARY rows would warrant extension; partition-algebra extension warrants appeal. Clean. |
| C8 TEXT_MATCHES_VERDICT | PASS WITH NIT | Lines 10–13 ("Do we get lucky with the same C1 = 1? NO -- we get lucky with the same architecture but K = 1/8") is honest. The unified-ladder framing (CR131+CR133) is a regularity claim, not over-stated. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | C1 was iterated. K=1/8 is the third choice (after C1=1 and presumably others). `law_committed_utc = 2026-06-16T00:28:35Z`. No precommit. |

## Specific demands

- REWORD line 6: `_SEALED` → `_SEALED_FULL_LATTICE_COVERAGE_FORWARD_BLIND_PENDING`.
- REWORD line 96: `CR133_law_lock_sha256 = 3adf93b8…` → actual `1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4`.
- REWORD the "unified fermion ladder" section: 3 K families across 114 rows is description, not derivation. Currently framed as a unifying insight.
- RETEST: forward-blind on future OUTER_BINARY_NEUTRAL rows; full in-sample coverage means there is no held-out data.
- RETEST: precommit K from first principles; "1/8 = 2^-D" is a unit-pegging after fit.
- APPEAL_CR: derive K=2^-D from SAM algebra. The K shape across V4_1 and OUTER_BINARY is described but not derived.

## Quoted evidence

> "User asked: 'do we get lucky with the same C1=1?' Answer: NO -- the OUTER_BINARY_NEUTRAL K = 1/8 = 2^-D, not C1 = 1"

> "Formula was derived from the 24-row ratio table (M_native/partition = 1/8, 3/2, 18 for depths 0, 1, 2)"

> "Closure depths observed: {0: 8, 1: 8, 2: 8}" (8 partitions × 3 depths = 24, exhaustively populated)

> "CR133_law_lock_sha256 = 3adf93b81f23c0c3b943fda9dcde947aeb96ac0e01162813b37a40163f0f8cee" (actual: 1e7e08d8…)

## Verdict text

CR133 is the most "complete" in-sample fit (24/24 on a 24-cell lookup) but that completeness is exactly its weakness: nothing is held out. The K=1/8 was the third attempt after C1=1, so the form was iterated against the data. Tier 2. Manuscript: cite as "OUTER_BINARY_NEUTRAL obeys partition·R^depth/8 exactly across the 8×3 lattice; K shared family with V4_1 is observed regularity."
