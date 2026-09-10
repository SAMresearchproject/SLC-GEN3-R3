# AUDIT — CR066a Born Rule Extension and the 1/α_H⁴ Letter Increment v1.0

**Auditor stance:** hostile.

## Tier verdict

**Tier 4 — DEMAND_RETEST**

CR066a is mathematically tidy (the algebra 17/16 = 16/16 + 1/16 is trivially correct) but structurally it is a tautological identification: it asserts that the 1/16 excess in the slot weights IS the letter content, then derives "invariants" (S1, S2, S3) that are arithmetic consequences of the slot decomposition fixed upstream. The forward-blind prediction is real but inherits the same Stage-3 envelope-loading hatch as CR065a.

The algebraic identity `17/16 = (R + D + α_H) / α_H⁴ = (12 + 3 + 2) / 16` is a numerical coincidence dressed as a structural identification.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

All cited locks (CR060a d5d3..., CR061a c011..., CR065a 38d7..., CR129b 8c3d...) resolve inside The_Courtroom.

### C2 — FALSIFIER_PRECOMMITTED: PASS (inherits from CR065a F1)

PRED_1: "ONE protocol execution on a SAM-native qubit (per CR-065a NV center specification) where the distribution clearly disagrees with (4/17, 9/17, 4/17) beyond statistical uncertainty."

This is a clean one-violation falsifier — BUT it inherits the Stage 3 envelope-loading hatch from CR065a (see CR065a C7). Until Stage 3 is calibrated, the falsifier is not reachable.

### C3 — WRONG_CONTROLS_LOAD_BEARING: FAIL

WC1–WC6 are clarifications:
- WC1: standard Born preserved.
- WC2: q=0 only.
- WC3: letter signature is exact rational.
- WC4: falsifier requires implementation correctness.
- WC5: no experimental demonstration claimed.
- WC6: Shannon/Holevo connection is open.

No load-bearing deletion. Demand: a real WC. Example: "WC7 — if the slot decomposition were (1/3, 4/9, 1/3), would the algebra still produce a recognizable 'letter increment'? Demonstrate that the 1/α_H⁴ identification is uniquely determined by (1/4, 9/16, 1/4) and not an artifact of dozenal arithmetic."

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: WEAK PASS

The decomposition 17/16 = 1 + 1/16 is arithmetic. The identification 1/16 = 1/α_H⁴ requires α_H = 2. The further identity 17/16 = (R + D + α_H)/α_H⁴ = (12+3+2)/16 requires R = 12, D = 3, α_H = 2 — all upstream constants. No free parameters at this stage.

**Concern:** the identity (R + D + α_H)/α_H⁴ = 17/16 is a numerical coincidence specific to the (R, D, α_H) = (12, 3, 2) triple. The result.md presents it as a structural meaning ("equivalent algebraic form") but does not document whether the identity is a derivation or a coincidence. Demand: explicit statement of which it is.

### C5 — IN_SAMPLE_DISCLOSED: FAIL (subtle)

The "invariants" S1, S2, S3 are PRESENTED as predictions but they are arithmetic consequences of the fixed slot decomposition:
- S1 (outer slots shift equally) follows trivially from the symmetry (4/17 - 1/4) = (4/17 - 1/4).
- S2 (middle shifts opposite) follows from sum-preservation.
- S3 (magnitude ratio 2 = α_H) is determined by (1/4, 9/16, 1/4) and α_H = 2.

These are not three independent predictions — they are one fact stated three ways. The result.md does not disclose this.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: PASS (as a derivation)

If the verdict is "structural derivation given fixed upstream inputs," the evidence (P1–P8 all arithmetic checks) matches. Acceptable as a derivation.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: WEAK

The "non-falsifying" clause: "Distributions NEAR (4/17, 9/17, 4/17) with experimental noise. Implementation failure at Stage 3 of CR-065a means the test was not run."

The "implementation failure" hatch is the same as CR065a F1. Wide hatch.

### C8 — TEXT_MATCHES_VERDICT: WEAK PASS

"The 1/α_H⁴ = 1/16 'extension' is the *fractional surface debit excess* at q = 0 above the carrier + sensor unit baseline."

The framing is honest — it's called an "extension," not a violation of Born, and the standard Born unity at measurement is preserved (WC1). Acceptable.

However the headline "Born Rule Extension" overstates: the standard Born rule is NOT extended, it is preserved. The 1/16 is a state-preparation signature, not a Born modification. The title should be "Slot-Weight Decomposition" or "Letter Increment Identification," not "Born Rule Extension."

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: N/A

CR066a is an algebraic identification. No data fit.

## Specific demands

1. **REWORD title:** "Born Rule Extension" overstates. Standard Born is preserved (per WC1). Demand: rename to "Slot Weight Decomposition and Letter Increment" or similar.
2. **DISCLOSE C5:** S1, S2, S3 are one arithmetic fact stated three ways, not three independent predictions. Demand: explicit disclosure.
3. **DERIVE OR DISCLOSE:** the identity (R+D+α_H)/α_H⁴ = 17/16 is either a derivation from R = 2·α_H·D (per upstream) or a numerical coincidence. The result.md must state which.
4. **APPEAL_CR scope:** narrow the "implementation failure at Stage 3" hatch — same demand as CR065a.

## Quoted evidence

> "Equivalent algebraic form: 17/16 = (R + D + α_H) / α_H⁴ = (12 + 3 + 2) / 16"

A numerical coincidence specific to (R, D, α_H) = (12, 3, 2). Whether this is a derivation or a coincidence is not stated.

> "**(S1)** Outer slots shift equally: Δ(carrier) = Δ(sensor) = −1/68"

S1 follows trivially from the symmetric outer slot weights. Not a prediction — an arithmetic consequence.
