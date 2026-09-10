# CR135 Hostile Audit — Criteria

**Audit date:** 2026-06-17
**Auditor:** adversarial reading; no benefit of the doubt
**Scope:** manuscript-critical chain (Higgs-gravity bridge + row-generator suite + QC protocol)
**Verdict pathway:** Courtroom rules; appeals allowed; one-violation falsifiers respected

## Nine Audit Criteria

A CR is courtroom-grade if and only if **every** criterion below passes. Failure on any one criterion triggers a finding tier (see below).

### C1 — HASH_CHAIN_INTEGRITY

Every cited upstream hash MUST resolve to an artifact in `The_Courtroom`. References to artifacts in external repos (`C:/VS/quantum_phase/artifacts/qp*`) without a corresponding intake CR that hashes them into the Courtroom are a chain break.

**Failure:** any upstream cited by SHA-256 hash that cannot be located inside The_Courtroom.

### C2 — FALSIFIER_PRECOMMITTED

A concrete, one-violation falsifier must be locked AT seal time. Vague falsifiers ("if the framework is wrong it will fail") do not count. Falsifiers retrofitted after data inspection do not count.

**Failure:** no falsifier, or falsifier so vague it cannot be falsified by a single observation.

### C3 — WRONG_CONTROLS_LOAD_BEARING

Wrong controls must actually fail when load-bearing pieces are removed. A WC that "passes trivially because nothing is being tested" is not a wrong control.

**Failure:** any WC that does not concretely delete a load-bearing input and show the test fails on that deletion.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO

`free_parameters = 0` must mean zero. Functional-form choices (which equation, which decomposition, which slot weighting) count as hidden degrees of freedom if not derived independently from the data being matched.

**Failure:** functional form was selected after inspecting target; or multiple plausible forms exist and the chosen one wasn't independently derived.

### C5 — IN_SAMPLE_DISCLOSED

If a law was extracted inductively from the catalog data, the CR must say so explicitly and characterize the in-sample match as **generator consistency**, not first-principles derivation.

**Failure:** law derived from data presented as if it were derived from principles; or in-sample 100 % match presented as predictive validation without forward-blind committed test.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE

A PASS verdict requires (a) precommitted falsifier survived, (b) wrong controls fail, (c) prediction matches without post-hoc tuning. A BOUNDARY verdict must be at-boundary, not a failure dressed up. A FAIL must be called FAIL.

**Failure:** PASS where evidence supports only BOUNDARY; BOUNDARY where evidence supports FAIL.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE

The CR must distinguish (a) what would falsify the rule from (b) what would trigger an appeal CR with a refined version. This line cannot be drawable post-hoc to avoid embarrassment.

**Failure:** appeal escape hatch wide enough that no concrete observation could ever falsify.

### C8 — TEXT_MATCHES_VERDICT

The result.md must accurately summarize the test outcome without overselling. Headline claims must be defensible by the recorded numbers.

**Failure:** result.md text exceeds the evidence; headline numbers cherry-picked from a wider distribution.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA

The formula or rule must be declared, hashed, and timestamped BEFORE the data check. If the formula was crafted to match a specific target value (Higgs at 125.25, Ω_b at 0.04930, T2 at 10 s), the construction order must be auditable.

**Failure:** no timestamp evidence the form preceded the value; OR form modified after first comparison.

## Finding Tiers

For each CR, assign one tier:

| Tier | Code | Meaning |
|---|---|---|
| 1 | PASS_COURTROOM_GRADE | All 9 criteria pass; submission-ready |
| 2 | PASS_WITH_REWORD | Verdict OK; result.md text needs sharpening (C8) |
| 3 | REGRADE_TO_BOUNDARY | Sealed as pass; evidence supports only boundary (C6) |
| 4 | DEMAND_RETEST | In-sample derivation needs forward-blind precommit before claim stands (C4, C5) |
| 5 | REQUIRES_APPEAL_CR | Structural defect; needs follow-up CR with refinement |
| 6 | HASH_CHAIN_BREAK | Upstream references unresolvable inside The_Courtroom (C1) |
| 7 | CALLOUT_FAIL_DRESSED_AS_PASS | Severe; rule claims more than evidence supports |

## Rule of Hostile Engagement

- Give no benefit of the doubt
- If a defense is available but not stated in the CR, the CR fails until the defense is documented
- "We meant to test that" does not count as "we tested that"
- A wrong control that doesn't break the rule isn't a wrong control, it's a sanity check
- The forward-blind protocol is genuinely strong; don't penalize CRs for honestly committing forward-blind falsifiers
- The carrier-compression gate (CR-122) is load-bearing; check it especially carefully
- "Algebra extension warrants an appeal, not a violation" must not be wider than the algebra it protects
- Self-reference (CR cites itself or sibling for derivation) is not a derivation

## Output

Per-CR finding files under `findings_per_cr/`, each containing:
- Tier verdict
- Pass/fail per criterion (1-9)
- Specific demands: REWORD lines, RETEST anchors, APPEAL_CR scopes
- Quoted evidence from the CR's result.md or lock file

Master summary in `CR135_AUDIT_VERDICT.md` with prioritized action list.
