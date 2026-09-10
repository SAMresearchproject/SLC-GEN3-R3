# AUDIT — CR061a Ideal Qubit Selection within 3-Body Standard Letter Tier v1.0

**Auditor stance:** hostile.

## Tier verdict

**Tier 2 — PASS_WITH_REWORD**

CR061a is the cleanest of the eight in this cluster. The three filters (q=0, distinct slots, promoted) are upstream-defined; the cascade is deterministic; the output (two rows: (1,2,4) and (2,4,8)) is a derivation, not a fit. The α_H ladder OBSERVATION is correctly framed as a consequence, not an axiom (WC5). Pass; demand only one sharpening.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR119 (5b93...), CR060a alphabet_lock_json (d5d3...), CR129b magnitude_lock_json (8c3d...) all resolve inside The_Courtroom. Note: this CR consistently cites the d5d3... CR060a lock — see CR060a finding on the dual hashes.

### C2 — FALSIFIER_PRECOMMITTED: PASS

PRED_1: "(a) such a row whose S_debit deviates from (17/16)·M/R³ kills the slot decomposition; (b) discovery of a non-α_H-ladder all-distinct triple at q=0 with promoted status would extend (not falsify) the candidate set."

Falsifier (a) IS a concrete one-violation falsifier: if a future q=0, all-distinct, promoted row exists with S_debit ≠ (17/16)·M/R³, the slot decomposition dies. Acceptable.

**Caveat:** (b) is an extension hatch, but it's narrowly scoped (it would extend the candidate count, not rescue a structural failure). Acceptable.

### C3 — WRONG_CONTROLS_LOAD_BEARING: WEAK PASS

WC1–WC6 are mostly read-only assertions + scope clarifications, NOT load-bearing deletions. WC4 ("other qubit candidates NOT excluded as non-qubits") is a structural-honesty disclosure. WC5 (the α_H-ladder observation is not an axiom) is the strongest WC — it isolates an emergent property and refuses to use it.

**Demand:** add WC7 deleting one of the filters (e.g., filter 2 distinct slots) and demonstrate the candidate count explodes from 2 → 17, confirming filter 2 is load-bearing.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: PASS

The three filters are all upstream-derived: q_abs=0 from CR129b's slot decomposition, distinct-slots from CR051's no-clone separation, promoted from CR060a's tier rule. No filter was hand-picked to land on 2 candidates.

### C5 — IN_SAMPLE_DISCLOSED: PASS

WC5 is explicit: the α_H-ladder is OBSERVED, not imposed. The selection is a filter cascade, not a fit. Clean disclosure.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: PASS

P1–P6 verify the count (107 → 17 → 2) and identify the two candidates. The verdict is structural identification, not a hardware claim. Matches evidence.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: PASS

Falsifier (a) draws a bright line. Extension via (b) is narrowly scoped and does not erase the falsifier.

### C8 — TEXT_MATCHES_VERDICT: PASS

Two candidates, both α_H ladders. The arithmetic (M = 756 for (1,2,4), M = 3024 for (2,4,8), α_H² ratio) is correctly stated and trivially verifiable.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: PASS (subject to CR060a/CR129b seal-time verification)

The filters and the S_debit = (17/16)·M/R³ formula are upstream; if CR060a and CR129b were sealed before CR061a's first cascade run, ordering holds. No `lock_committed_utc` in result.md; demand inclusion for clarity.

## Specific demands

1. **REWORD:** add a `lock_committed_utc` field for audit clarity.
2. **RETEST:** show the filter-deletion cascade (e.g., dropping filter 2 yields 17 candidates, not 2) to load-bear the WCs.
3. **OPEN DEBT:** the open debt "First-principles derivation of why structural ideality selects pure alpha_H ladders is open" is honestly disclosed. Acceptable.

## Quoted evidence

> "**[PASS]** WC5_alpha_H_ladder_observation_NOT_axiomatic -- The fact that both candidates are pure alpha_H ladders is an OBSERVATION from the filter outcome, not an axiom."

Correct framing. Credit.

> "**Falsifier:** (a) such a row whose S_debit deviates from (17/16)·M/R³ kills the slot decomposition"

Concrete, one-violation falsifier. Acceptable.
