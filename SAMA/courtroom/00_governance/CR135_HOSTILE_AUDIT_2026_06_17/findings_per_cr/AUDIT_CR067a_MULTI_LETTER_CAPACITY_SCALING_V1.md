# AUDIT — CR067a Multi-Letter Capacity Scaling and the Gravity Channel Ceiling v1.0

**Auditor stance:** hostile.

## Tier verdict

**Tier 4 — DEMAND_RETEST**

CR067a is an inductive scaling law identified by elimination: three candidates (linear, parallel-sharing, geometric) are listed; two are rejected on hand-waving grounds; the geometric is locked. The geometric scaling 2^-(D+N) is a clean algebraic series that asymptotes to 1/8 — but this is constructed to match the CR121 gravity ceiling, not derived from an independent principle. Forward-blind falsifiers are real but the in-sample construction is not disclosed.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR060a (d5d3...), CR065a (38d7...), CR066a (5eb9...), CR066b (f864...), CR121 (01e4...), CR129b (8c3d...) all resolve inside The_Courtroom.

### C2 — FALSIFIER_PRECOMMITTED: PASS

Three falsifiers:
- per-letter capacity ≠ 2^-(D+N) → kills geometric subdivision
- cumulative > 1/8 → kills gravity ceiling
- asymptote ≠ 1/8 → kills the identification

Three concrete one-violation falsifiers. Acceptable.

### C3 — WRONG_CONTROLS_LOAD_BEARING: WEAK PASS

WC1 (linear rejected because of gravity ceiling violation) and WC2 (parallel-sharing rejected because no scaling) are partial load-bearing rejections — they identify alternatives and reject on stated grounds. But:
- WC1's rejection is circular: "violates gravity channel ceiling" — but the gravity ceiling identification is what CR067a is trying to establish. Circular.
- WC2's rejection ("doesn't scale") is a definitional choice: if "scaling" means "per-letter capacity grows," then parallel-sharing isn't scaling by definition. Not a real rejection.

The only genuine load-bearing rejection is the geometric vs other-shape comparison, which is not surfaced.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: FAIL

The choice of 2^-(D+N) is asserted. Alternatives like 2^-N · 1/16, or 1/(D·N·α_H), or any other function asymptoting to 1/8, were not enumerated. The geometric form was CHOSEN to:
1. Match the 1/16 first-letter content (so per-letter at N=1 = 2^-(D+1) = 2^-4 = 1/16). ✓
2. Asymptote to 2^-D = 1/8 (the Higgs-released fraction). ✓

These two constraints force a specific 1-parameter family of functions, of which 2^-(D+N) is one. The choice of geometric (vs other 1-param families) is a hidden DoF.

### C5 — IN_SAMPLE_DISCLOSED: FAIL

The result.md presents the geometric subdivision as if derived. It's not — it's identified by matching the asymptote to a desired target (1/8, from CR121). This is an in-sample construction that should be disclosed as such (per C5 rule).

The "Information-Theoretic Connection (Kraft)" section observes that the Kraft sum equals 1/8 — but this is a tautological consequence of the geometric structure with depth D+N. It's not independent evidence; it's the same fact restated.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: WEAK PASS

The verdict is "scaling law identified." Predictions (P1–P8) are arithmetic checks. Acceptable as identification, but C5 demands the framing be "in-sample identification" not "first-principles derivation."

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: PASS

Three falsifiers, all concrete. WC6 notes that high-N implementations exceed practical NV gate fidelity — this is a scope limitation, not an appeal hatch.

### C8 — TEXT_MATCHES_VERDICT: WEAK PASS

The text correctly states that the asymptote IS 1/8 (the gravity-released fraction). Predictions are stated as exact rationals. Acceptable.

**Minor:** the text "Each new letter takes half of what remains in the gravity channel" is suggestive language that anthropomorphizes the scaling. Demand: replace with neutral algebraic statement.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: WEAK PASS

No `lock_committed_utc` in result.md. The formula 2^-(D+N) is declared before any test. The "test" is purely arithmetic (no measurement), so timestamp ordering is degenerate.

## Specific demands

1. **DISCLOSE C5:** the geometric scaling 2^-(D+N) was chosen to asymptote to 1/8 (the CR121 gravity ceiling). State explicitly that this is an inductive construction, not a derivation.
2. **ENUMERATE ALTERNATIVES:** beyond linear and parallel-sharing, what OTHER scaling forms asymptote to 1/8 and start at 1/16 for N=1? If multiple exist, the geometric choice has unexplored DoF.
3. **DECOUPLE WC1 FROM THE CIRCULAR ARGUMENT:** rejecting linear scaling on "violates gravity ceiling" grounds is circular when CR067a is establishing the gravity ceiling identification. Provide an independent rejection ground.
4. **REWORD ANTHROPOMORPHIC LANGUAGE:** "Each new letter takes half of what remains" → neutral algebraic statement.

## Quoted evidence

> "WC1_linear_scaling_explicitly_rejected -- Linear scaling N * 1/16 grows without bound and violates the gravity channel ceiling identified in CR121."

Circular: the gravity ceiling identification at 1/8 is what CR067a is establishing. Rejecting alternatives on "they violate the thing we are trying to establish" is not a valid wrong control.

> "Per-letter capacity: c_N = 1 / α_H^(D+N) = 2^-(D+N)"

The functional form is asserted, not derived. Multiple 1-parameter families satisfy the same boundary conditions; the geometric was chosen.
