# AUDIT — CR060a Paul Revere Letter Alphabet Lock v1.0

**Auditor stance:** hostile / Genghis Khan. No benefit of the doubt.

## Tier verdict

**Tier 4 — DEMAND_RETEST (with C5 caveat verging on Tier 3)**

PRED_1 is an in-sample identification dressed as a forward-blind claim. Pass on C1, C8. Weak on C2, C4, C5. Marginal on C7.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS (with one snag)

All 16 cited upstream hashes (CR119, CR121, CR122, CR128, CR128b, CR129, CR129b, CR129c, CR130, CR131, CR132, CR133, CR134, CR051, CR054, CR058) resolve to artifacts located inside The_Courtroom. No qp-chain external references at the SHA-256 cite level.

**Snag (REWORD demand):** the result.md publishes `CR060a_alphabet_lock_sha256 = 05f487835689e39477a4da1476f6796960108fbf56e921859e3a87f25616af17`, but every downstream sibling CR (CR061a, CR063a, CR064a, CR065a, CR066a, CR066b, CR067a) cites `CR060a_alphabet_lock_json = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0`. Different SHA-256 strings. Either the CR060a result.md publishes a stale hash, or the file was re-hashed after sealing. Demand: disclose which file was hashed (`*_lock_sha256` vs `*_lock_json`) and reconcile the two values.

### C2 — FALSIFIER_PRECOMMITTED: WEAK PASS

PRED_1 falsifier: "one future row that violates tier-assignment semantics triggers an appeal CR with an extended tier definition." This is structurally a tier-redefinition escape hatch, NOT a falsifier. The "non-falsifying" clause explicitly says "catalog additions within documented tiers extend (do not falsify) the alphabet." Demand: identify ONE concrete row outcome (e.g., a CR119 amendment that promoted a stability=REJECTED row, or a new 3-body row that violates the q=0 slot decomposition) that would force a FAIL verdict, not an appeal.

### C3 — WRONG_CONTROLS_LOAD_BEARING: FAIL

All 7 wrong controls (WC1–WC7) are sanity-checks, not load-bearing deletions:
- WC1, WC2, WC3, WC6, WC7 — read-only documentation assertions ("CRxxx unmodified," "cross-link explicit"). Nothing is being tested by removing a load-bearing input.
- WC4 — "no hardware claim" — a scope assertion, not a control.
- WC5 — "alphabet derivation inductive not axiomatic" — a disclaimer in the form of a WC; this is C5 disclosure, NOT a wrong control.

**Demand:** add a real WC. Example: "WC8 — if the row-generator law CR-129b's q=0 slot decomposition is replaced by an alternate (1/8, 6/8, 1/8) decomposition, do CR060a's tier assignments break?" The current set lets the CR pass C3 by trivial assertion.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: WEAK PASS

`free_parameters_at_test: 0` is reported. The choice of "promoted" vs "rejected" inherits from CR119's stability_status field, which is upstream. Tier definitions (3body_standard, 2body_short, etc.) are functional-form choices inherited from CR051/054 architecture. Acceptable.

**Concern:** the partition between "3body_standard = canonical letter" and "1body_carrier = gauge broadcast" is an architectural assignment, not a derivation. If an alternate tier partition existed that produced different letter counts but same 300 total, would it have been adopted? Not addressed.

### C5 — IN_SAMPLE_DISCLOSED: PASS (this is the strongest criterion in this CR)

WC5 explicitly states: "The alphabet tier structure and slot identifications are derived from the CR128-134 row-generator laws plus CR051/054 protocol shapes. CR060a does NOT axiomatically declare the alphabet; it identifies it from the structural fit." This is the correct disclosure. Credit.

However, PRED_1 then frames the in-sample identification as a forward-blind claim ("for any future CR119 row..."). This is inconsistent: an inductive identification cannot generate a forward-blind prediction without an independently committed test set. The "future row" is the test set, but no such rows exist yet — so PRED_1 is unfalsifiable until CR119 is amended.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: PASS

Verdict is SEALED, six predictions are P-style structural checks (catalog count, alphabet size, tier populated). Each is a counting verification, appropriate to the claim. No overselling at the verdict level.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: WEAK

PRED_1 says: "one future row that violates tier-assignment semantics triggers an appeal CR with an extended tier definition." This appeal escape hatch is wide enough that ANY future-row deviation can be absorbed by extending the tier set. The bright line is not drawn. Demand: pre-commit a specific row outcome (e.g., promotion of a fake_spin row to non-null tier) that would falsify rather than appeal.

### C8 — TEXT_MATCHES_VERDICT: PASS

Headline numbers (300 promoted, 21 wrong controls, 5 tiers) match the prediction-check counts. Capacity (8.2288 bits) is `log2(300)` exact. No overselling at the text level.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: NOT VERIFIABLE FROM RESULT.MD

The result.md doesn't carry a lock_committed_utc field (CR064a does). The slot weights (1/4, 9/16, 1/4) summing to 17/16 are claimed to come from CR129b's locked formula. As long as CR129b was sealed before CR060a, the formula-then-data ordering holds upstream. Verifiable through CR129b's seal timestamp.

**Demand:** include `lock_committed_utc` in CR060a result.md for audit clarity.

## Specific demands

1. **REWORD:** reconcile the two distinct CR060a hash strings (alphabet_lock_sha256 vs alphabet_lock_json) — one of them is misleading downstream consumers.
2. **APPEAL_CR scope:** sharpen PRED_1 with a concrete one-violation falsifier that triggers FAIL, not an appeal. The current "appeal extends the tier definition" is C7-fail.
3. **RETEST anchor:** the 1/4, 9/16, 1/4 slot decomposition is asserted to be UNIQUE for the carrier/envelope/sensor mapping. Demonstrate uniqueness or document the alternatives that were considered and rejected. (See ROLLUP for the 17/16 over-unit discussion.)
4. **WC replacement:** swap one of WC1–WC7 (the read-only assertions) for a real load-bearing deletion test.

## Quoted evidence

> "WC5_alphabet_derivation_inductive_not_axiomatic -- The alphabet tier structure and slot identifications are derived from the CR128-134 row-generator laws plus CR051/054 protocol shapes. CR060a does NOT axiomatically declare the alphabet; it identifies it from the structural fit."

This is good C5 disclosure but does not rescue C3 or C7.

> "**Falsifier:** one future row that violates tier-assignment semantics triggers an appeal CR with an extended tier definition."

This is an appeal hatch, not a falsifier. C2 weak / C7 fail.
