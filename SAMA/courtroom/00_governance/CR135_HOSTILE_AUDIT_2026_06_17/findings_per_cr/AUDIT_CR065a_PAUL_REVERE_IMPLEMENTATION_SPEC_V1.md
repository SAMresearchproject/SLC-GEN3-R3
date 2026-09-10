# AUDIT — CR065a Paul Revere Letter Implementation Specification v1.0

**Auditor stance:** hostile.

## Tier verdict

**Tier 5 — REQUIRES_APPEAL_CR** (verging on Tier 2 — PASS_WITH_REWORD)

CR065a is a structural specification, not a measurement. As a SPEC it's reasonably honest: it identifies a winning pairing ((1,2,4) × NV center, score 14/15), tags all hardware parameters [EXPERT_REVIEW_REQUIRED], and admits the 17/16 sum is "the structural question CR-066a will derive." But the scoring rubric (5 criteria, scores 1–3) is opaque and the embedded protocol's Stage 3 arithmetic is incoherent.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR060a (d5d3...), CR061a (c011...), CR063a (f884...), CR064a (96b5...), CR129b (8c3d...) all resolve inside The_Courtroom.

**Caveat:** CR065a chains to CR064a (the post-rescue formula). The CR063a v1.0 issue propagates downstream silently — see ROLLUP.

### C2 — FALSIFIER_PRECOMMITTED: PASS

Three forward-blind falsifiers (F1, F2, F3):
- F1: (4/17, 9/17, 4/17) distribution not recovered → kills slot decomposition
- F2: no pre-commit boundary-stress signal → suggests NV PL doesn't realize sensor
- F3: effective T2 > 10× T2_grav_at_A_0 after subtraction → kills CR064a floor

Three concrete falsifiers. F1 is the strongest (it depends on no rescue / no glossary acceptance). F3 inherits CR064a's 10× cushion (see CR064a finding).

### C3 — WRONG_CONTROLS_LOAD_BEARING: FAIL

WC1–WC7 are scope-clarifications:
- WC1: "no hardware demonstration claimed" — scope.
- WC2: "runner-up pairings NOT excluded" — disclaimer.
- WC3: "[EXPERT_REVIEW_REQUIRED] tags explicit" — process note.
- WC4: quantum normalization clarified — disclosure.
- WC5: "falsification conditions concrete and testable" — assertion.
- WC6: "alternative platforms documented" — scope.
- WC7: "protocol writeup is document-chapter ready" — meta.

No load-bearing deletion. Demand: a real WC. Example: "WC8 — if Filter 1 (q_abs=0) is relaxed to q_abs ≤ 1, does the winning pairing change?" The scoring is opaque enough that the answer isn't obvious.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: FAIL

The scoring rubric is the C4 violation. Five criteria (slot count, sensor, T2 headroom, accessibility, mass scale), each scored 1–3 by the runner. The result.md does not document the score-assignment rule. (1,2,4) × NV center wins with 14/15; (2,4,8) × NV center is 13/15. The 1-point margin is determined by the mass-scale score (2 vs 1), but the rule for "mass-scale = 2 vs 1" is not stated.

`free_parameters_at_test: 0` is inconsistent with a 5-criterion, 1–3 score, undocumented-rule rubric. Each criterion's threshold is a hidden DoF.

### C5 — IN_SAMPLE_DISCLOSED: PASS (this is well-disclosed)

The CR explicitly notes that "Quantum State Normalization" is an issue: SAM slot weights sum to 17/16, physical probabilities sum to 1; the reconciliation is left to CR066a. This is honest framing.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: WEAK PASS

Verdict is "SPECIFICATION sealed" not "hardware demonstrated." WC1 makes this explicit. The verdict is a recommendation, not a claim about reality. As a SPEC the evidence (scoring table + protocol writeup) matches. Acceptable.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: WEAK

F1 falsifier ("(4/17, 9/17, 4/17) NOT recovered") has the appeal hatch: "Implementation failure at Stage 3 means the test was not run" (CR066a non-falsifying clause). If Stage 3 is "the most experimentally delicate" (per the protocol writeup) and standard CPMG/Knill sequences must be "modified" (per the protocol writeup), then ANY null result can be attributed to Stage 3 implementation failure. This is a wide hatch.

### C8 — TEXT_MATCHES_VERDICT: FAIL

Critical embedded error in the protocol writeup (CR065a_paul_revere_protocol.md, Stage 3):

> "1/4 + 9/16 + 1/4 = 4/16 + 9/16 + 4/16 = 17/16. This exceeds 1.
> CORRECTION: the SAM slot weights (1/4, 9/16, 1/4) summing to 17/16 are SURFACE DEBIT FRACTIONS, not quantum probabilities."

The protocol document includes a CORRECTION mid-text — i.e., the writer made an arithmetic error, then corrected it inline rather than rewriting. This is not how a sealed specification should read. A sealed protocol does not show its work in the form of "wait, I made a mistake here." Demand: REWORD Stage 3 to present the normalization (4/17, 9/17, 4/17) as the starting point with the 17/16 SAM-side noted as the unnormalized origin, without the embedded self-correction.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: N/A (specification, no data)

CR065a is a spec, not a test. The protocol's Stage 6 ("T2 saturation at T2_grav_at_A_0 = 16·π·R⁴/(17·ω_gate)") inherits CR064a's formula and its C9 issues.

## Specific demands

1. **REWORD Stage 3** of the embedded protocol to remove the inline "CORRECTION: wait, this exceeds 1" arithmetic-and-fix sequence. A sealed protocol document does not contain its own debugging.
2. **DOCUMENT THE SCORING RUBRIC.** Each of the 5 criteria's 1/2/3 thresholds must be defined. Currently the 14/15 vs 13/15 margin rests on undocumented score assignments.
3. **APPEAL_CR scope:** narrow F1's "implementation failure" hatch. Currently any null result can be dismissed as Stage 3 failure.
4. **DECLARE C7 EXPLICITLY:** state that F1 is testable only after Stage 3 envelope loading is demonstrated to produce (4/17, 9/17, 4/17) on a calibration test (a known control state). Without this calibration, the falsifier is not reachable.

## Quoted evidence

> "**Stage 3 ... normalization check: |1/2|^2 + |3/4|^2 + |1/2|^2 = 1/4 + 9/16 + 1/4 = 4/16 + 9/16 + 4/16 = 17/16. This exceeds 1.**"

A specification document does not perform mid-stage arithmetic corrections. C8 fail.

> "WC4_quantum_normalization_vs_SAM_slot_weights_clarified -- SAM slot weights (1/4, 9/16, 1/4) sum to 17/16 (surface debit fractions). Physical quantum probabilities are (4/17, 9/17, 4/17) after normalization."

The clarification is correct, but it's in a WC, not in the protocol body. The protocol body still shows the arithmetic stumble.
