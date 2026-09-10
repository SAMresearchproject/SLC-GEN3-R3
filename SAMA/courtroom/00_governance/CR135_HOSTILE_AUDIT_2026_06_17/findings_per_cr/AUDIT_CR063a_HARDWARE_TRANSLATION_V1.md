# AUDIT — CR063a Hardware Translation Document v1.0

**Auditor stance:** hostile. This CR is the audit's smoking gun.

## Tier verdict

**Tier 7 — CALLOUT_FAIL_DRESSED_AS_PASS**

CR063a v1.0 made a concrete numerical claim — `T2_grav = 1626.35 / ω seconds` — and that claim was empirically falsified within hours by ANY transmon measurement (T2 ≈ 100 μs vs T2_grav ≈ 52 ns at 5 GHz = factor 2000× overrun). CR064a's first sentence concedes this:

> "CR063a v1.0 used `T2_grav = 16·R³/(17·ω)` at horizon condition A = 1 with ω = qubit splitting frequency. Under that reading, transmon T2 ≈ 100 μs already exceeds T2_grav ≈ 52 ns by ~2000× — apparent falsification."

Per CR063a's own falsifier text:

> "**Falsifier:** ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0."

A 2000× overrun on transmon T2 (a measurement that has been reproduced in dozens of labs over a decade) IS a rigorously-isolated falsification. CR063a should have been REGRADED TO FAIL. Instead it remains SEALED as v1.0 with the "rescue" silently routed downstream into CR064a v1.1.

This is the textbook definition of FAIL dressed as PASS.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR060a (d5d3...), CR061a (c011...), CR121 (01e4...), CR129b (8c3d...) all resolve inside The_Courtroom. Hash chain intact.

### C2 — FALSIFIER_PRECOMMITTED: PASS (the falsifier WAS precommitted)

> "**Falsifier:** ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0."

This is a clean, concrete, one-violation falsifier. CR063a deserves credit for committing it.

**BUT:** the falsifier WAS triggered (transmon T2 ≈ 100 μs at 5 GHz vs T2_grav = 52 ns; factor ~2000 overrun) and the verdict was NOT updated to FAIL. The CR-064a rescue note says channel subtraction is needed, but 100 μs vs 52 ns is not a subtraction problem — no realistic channel subtraction multiplies T2 by 2000.

### C3 — WRONG_CONTROLS_LOAD_BEARING: FAIL

WC1–WC6 are scope-clarifications and disclaimers:
- WC1: "no hardware demonstration claimed" — scope.
- WC2: "M_native NOT calibrated as energy splitting" — disclaimer.
- WC3: "gravitational channel identification rests on CR121" — dependency note.
- WC4: "T2 floor formula FALSIFIABLE" — assertion of the falsifier; NOT a WC.
- WC5: "inconclusive outcome documented" — admits outcome C, which is itself an escape hatch (see C7).
- WC6: "platform recommendations are NOT endorsements" — disclaimer.

NO wrong control deletes a load-bearing input and shows the test breaks. None.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: FAIL (after the rescue)

`free_parameters_at_test: 0` claimed at v1.0. But the rescue in CR064a introduces:
1. The `A_0 = 1/(π·R)` factor (a new structural input not declared at CR063a seal time).
2. The reinterpretation of ω from "qubit splitting frequency" → "gate operating angular frequency" — a substantive change in operational meaning.

The choice to apply A_0 enhancement AND switch ω after seeing the 2000× discrepancy is exactly the C4 violation: "functional form was selected after inspecting target."

### C5 — IN_SAMPLE_DISCLOSED: N/A → FAIL via C6

CR063a is a prediction CR, not a fit CR. C5 isn't directly applicable to v1.0. But the v1.1 rescue is a post-hoc fit to known T2 values — C5 violation by proxy.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: FAIL

v1.0 is sealed as SEALED. Evidence supports FAIL. The cited rescue (CR064a) is a NEW formula, not a refinement of v1.0. The fact that CR064a notes "v1.0 is preserved for the audit record" (WC3 of CR064a) is honesty about the historical record but does NOT change the fact that v1.0's PRED_1 was falsified.

**Demand:** CR063a v1.0 should carry a verdict-modifier line: "REFUTED 2026-06-16; superseded by CR064a v1.1." Without that line the audit trail says v1.0 still stands.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: FAIL

The three-outcome framework (CONFIRMING / FALSIFYING / INCONCLUSIVE) builds an escape hatch:

> "**Outcome C (INCONCLUSIVE):** Other channels dominate; no clean residual → status quo, no information."

This means: any T2 measurement that exceeds T2_grav can be attributed to "channel subtraction not isolated" → outcome C → v1.0 untested. The falsifier text says "after channel subtraction," which makes outcome C trivially reachable for any unfavorable measurement.

The bright line cannot be drawn post-hoc to absorb a 2000× overrun.

### C8 — TEXT_MATCHES_VERDICT: FAIL

The text:
> "**T2_grav = 1626.35 / ω seconds**"
> "SC transmon (5 GHz) | T2_grav 51.8 ns"

These are concrete numerical predictions. The matching literature value (transmon T2 ~100 μs) is publicly available and was at the time of seal. The text headline does not square with the verdict (SEALED).

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: NOT VERIFIABLE FROM RESULT.MD

Result.md doesn't carry `lock_committed_utc`. CR064a lock_committed_utc = 2026-06-16T01:45:29Z. Presumably CR063a was sealed earlier on 2026-06-15 or 2026-06-16. The formula DID precede the comparison. But the comparison was unfavorable, and the response was to introduce a new formula (v1.1) rather than declare FAIL.

This is the heart of the indictment: the timestamp ordering is fine, but the post-comparison BEHAVIOR was to invent a rescue rather than honor the falsifier.

## Specific demands

1. **REGRADE TO FAIL:** CR063a v1.0 must be re-verdicted as FAIL or REFUTED, with the v1.1 successor explicitly noted in the v1.0 header. Currently the audit trail says v1.0 still stands SEALED.
2. **DISCLOSE THE RESCUE PATH:** CR063a result.md must carry a modifier line: "Superseded by CR064a v1.1 (A_0 calibration); v1.0 falsified by transmon T2 ≈ 100 μs vs predicted 52 ns at 5 GHz."
3. **C7 REPAIR:** delete or sharpen Outcome C. It is currently wide enough to absorb any unfavorable measurement.
4. **APPEAL_CR scope:** CR064a should EXPLICITLY be filed as an appeal to CR063a, not as a sibling extension. The phrase "CR063a v1.0 stays sealed at the horizon (A=1) reading. CR064a refines it via the A_0 operating point correction, producing v1.1" (CR064a WC3) is too gentle. v1.0 was wrong by 2000×; v1.1 isn't a refinement, it's a replacement.

## Quoted evidence

> "**[PASS]** WC4_T2_floor_formula_FALSIFIABLE -- T2_grav = 1626.35 / omega is a CONCRETE NUMERIC FORMULA. One platform measurement exceeding it under rigorous channel subtraction falsifies the universality claim."

A concrete formula that was falsified at first contact with published transmon data, by factor 2000×. Yet sealed as PASS.

> CR064a v1.1: "Under that reading, transmon T2 ≈ 100 μs already exceeds T2_grav ≈ 52 ns by ~2000× — apparent falsification."

CR064a admits the falsification. CR063a does not.

## Severity

This is the most severe finding in the cluster. CR063a is the case study for "rule claims more than evidence supports" (Tier 7). If left as PASS, it weaponizes the Courtroom against itself: a falsifier was committed, was triggered, and the verdict held anyway. The manuscript cannot ship with CR063a sealed as PASS.
