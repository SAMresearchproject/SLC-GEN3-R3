# AUDIT — CR064a A_0 Calibration + Published T2 Verification v1.0 (v1.1 formula)

**Auditor stance:** hostile. This is the most publicly-checkable claim in the cluster, and the headline does not survive scrutiny.

## Tier verdict

**Tier 3 — REGRADE_TO_BOUNDARY (verging on Tier 4 / DEMAND_RETEST)**

The corrected formula `T2_grav_at_A_0 = 16·π·R⁴ / (17·ω_gate)` is a post-hoc rescue of CR063a v1.0 with two newly introduced degrees of freedom (the A_0 factor and the ω = gate-rate reinterpretation). The "zero violations" headline is purchased by:
1. A factor-of-10 falsifier band (not factor 1.1 or 1.5).
2. An AT_THE_LIMIT band of 0.5–2.0 (factor of 4 width).
3. A gate-rate artifact that puts three of the five AT_THE_LIMIT systems at exactly the same ratio 1.0248.
4. All 10 T2 citations tagged [VERIFY_PRECOMMIT] (unverified at seal time).

Each of those four design choices is independently defensible; together they reduce the test to: "no published T2 value can be more than 10× above 61295.49 / ω_gate for any reasonable ω_gate." The falsifier is real but soft.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR060a (d5d3...), CR061a (c011...), CR063a (f884...), CR121 (01e4...), CR129b (8c3d...) all resolve inside The_Courtroom.

### C2 — FALSIFIER_PRECOMMITTED: WEAK PASS

> "**Falsifier:** ONE rigorously-reported T2 measurement exceeding T2_grav by more than **10×** at its gate rate, with non-gravitational channels fully subtracted, kills v1.1."

The 10× margin is large. The result.md WC5 explicitly defends it:

> "WC5_falsifier_threshold_10x_not_1_1x -- Falsifier requires T2_observed > 10 * T2_grav at the same omega_gate. A factor of 10 above the predicted floor is much larger than published-value uncertainty, ensuring the falsifier is unambiguous when triggered."

**Counter:** a factor-10 margin is convenient AFTER seeing that no current measurement exceeds T2_grav by less than 10×. The original CR063a falsifier had NO multiplier (any rigorous overrun → FAIL). The introduction of the 10× cushion is itself a post-hoc choice. The "soft tension" band (1× to 10×) is a new gray zone that didn't exist at CR063a v1.0 seal time.

### C3 — WRONG_CONTROLS_LOAD_BEARING: FAIL

WC1–WC7 are all disclaimers / scope-clarifications:
- WC1 admits all 10 citations are [VERIFY_PRECOMMIT] (unverified).
- WC2 admits ω_gate is an "engineering input" (parameter), not a SAM prediction.
- WC3 preserves CR063a v1.0 as sealed (this is the silent overwrite issue).
- WC4 defines the AT_THE_LIMIT band as 0.5–2.0 with no derivation of the band width.
- WC5 defends the 10× falsifier threshold.
- WC6 introduces "soft tension" as a non-violation status.
- WC7 traces A_0 to SAM glossary G:A0 (a definition reference, not a control).

**No wrong control deletes a load-bearing input.** Demand: a real WC that removes the A_0 enhancement and shows the prediction returns to v1.0's falsified state — which is exactly the point of A_0; but the result.md does not document this comparison explicitly.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: FAIL

`free_parameters_at_test: 0` is claimed. Two parameters were introduced relative to CR063a v1.0:
1. **A_0 = 1/(π·R)** — a NEW structural input declared in WC7 as "accepted as SAM glossary input from G:A0." Glossary acceptance does not equal derivation. The introduction of A_0 enhancement was triggered by the v1.0 failure; the structural input is real but its DEPLOYMENT here is post-hoc.
2. **ω = gate operating rate, not splitting frequency** — a substantive reinterpretation. CR064a WC2 admits ω_gate is an "engineering input" whose definition varies by protocol (raw, DD, echo-corrected). This is a functional-form choice made after seeing v1.0 fail.

Two free parameters, both chosen after the target was inspected.

### C5 — IN_SAMPLE_DISCLOSED: FAIL

The 10 published T2 measurements were KNOWN before the formula was tuned. WC1 admits this:

> "All citations are tagged [VERIFY_PRECOMMIT] reflecting training-cutoff (Jan 2026) knowledge."

This means the formula `16·π·R⁴ / (17·ω_gate)` was tuned to a known dataset. The result.md does not characterize the in-sample match as "generator consistency" — it presents it as "no outright violations" (P4), which is the language of forward-blind validation, not in-sample fit.

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: FAIL (REGRADE_TO_BOUNDARY)

P4: "no outright violations" / P5: "three at the limit" (label says three, value is 5 — see C8).

The headline "5 of 10 published T2 measurements sit AT THE LIMIT, zero violations" oversells. The AT_THE_LIMIT band is a factor-4 wide window; landing inside it is NOT a confirmation. Five of ten falling inside a factor-4 band with a factor-10 falsifier is consistent with the formula and the data being roughly the same order of magnitude — no more.

Evidence supports BOUNDARY, not PASS. **Demand: regrade to BOUNDARY.**

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: WEAK

WC6 explicitly creates "soft tension" — a third category between consistent and violation. This is an appeal hatch by design. The bright line exists at factor 10×, but the gray zone (1× to 10×) admits any future measurement that lands between T2_grav and 10·T2_grav as "soft tension, prompts v1.2 refinement." That's an appeal hatch, not a falsifier.

### C8 — TEXT_MATCHES_VERDICT: FAIL (multiple)

**1. Headline overselling:**
> "Three state-of-the-art systems (Quantinuum H1, IonQ Forte, Delft NV cryogenic+DD) sit at the predicted gravitational floor — consistent with the SAM prediction that these platforms are approaching the fundamental limit at their gate-rate class."

The three systems sit at EXACTLY ratio 1.0248. They do not "approach" anything — they hit identical values because their (T2_observed × ω_gate) products are forced to land at the same ratio by the literature numbers chosen. This is a **gate-rate artifact**, not an empirical confirmation. The result.md does not disclose this artifact.

**Arithmetic exposure:**
- Quantinuum H1: T2 = 10 s, ω = 6.2832e+03 rad/s → product = 62832
- IonQ Forte: T2 = 1 s, ω = 6.2832e+04 rad/s → product = 62832
- Delft NV cryo+DD: T2 = 1 s, ω = 6.2832e+04 rad/s → product = 62832

All three have the IDENTICAL T2·ω product. Their ratios are 62832 / 61295.49 = 1.0250 (the .0248 discrepancy is rounding). These three points are duplicates in (T2·ω) space, not three independent confirmations.

**2. Prediction-check label/value mismatch (C8 internal contradiction):**
> "**[PASS]** P5_three_at_the_limit_systems -- AT_THE_LIMIT count = 5."

Label says "three"; numeric value says 5. Minor but a literal C8 violation.

**3. The 1.0248 pattern is the gate-rate artifact** flagged in the user's memory record `feedback_cr064a_t2grav_calibration_rescue.md`. The result.md does NOT disclose this; it presents the three identical ratios as three independent at-the-limit observations. C8 fail.

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: FAIL

`lock_committed_utc = 2026-06-16T01:45:29Z`. The formula 16·π·R⁴/(17·ω_gate) was declared at v1.1 seal time. But:
- CR063a v1.0 (the predecessor) had a DIFFERENT formula.
- The change to v1.1 was triggered AFTER the v1.0 formula was empirically falsified.
- Therefore the v1.1 formula was DERIVED to match the known target data.

This is the textbook C9 failure pattern: formula crafted after the target was inspected.

CR064a WC3 admits this honestly:
> "CR063a v1.0 NOT modified -- CR063a v1.0 stays sealed at the horizon (A=1) reading. CR064a refines it via the A_0 operating point correction, producing v1.1."

But "refines it" minimizes a 2000× correction to a "refinement." The honest framing is: v1.0 was wrong; v1.1 is a new formula derived to match the data.

## Specific demands

1. **REGRADE TO BOUNDARY** at minimum. The "5 of 10 AT THE LIMIT, 0 violations" headline does not support a PASS verdict.
2. **DISCLOSE THE 1.0248 ARTIFACT** in result.md. The three identical ratios are duplicates in (T2·ω) space, not three independent at-the-limit confirmations. Demand: add a paragraph titled "The 1.0248 multiplicity" noting that Quantinuum H1, IonQ Forte, and Delft NV cryo+DD all sit at T2·ω = 62832 rad·s/s due to the literature numbers chosen, and that this is one point of evidence with three citations, not three independent confirmations.
3. **VERIFY THE 10 CITATIONS.** All carry [VERIFY_PRECOMMIT]. Until verified against current literature, the result is provisional. The result.md must NOT be promoted to SEALED until WC1's verification is complete.
4. **NARROW THE AT_THE_LIMIT BAND.** The 0.5–2.0 band is a factor-4 window; under any reasonable interpretation, landing inside a factor-4 window is not "at the limit." Demand: tighten to 0.8–1.25 or document why the wider band is necessary.
5. **DERIVE A_0 INDEPENDENTLY.** WC7 says A_0 = 1/(π·R) is "accepted as SAM glossary input." Acceptance from a glossary is not derivation. The post-hoc deployment of A_0 to rescue v1.0 must be justified by an independent derivation prior to CR063a — not by glossary citation after the fact.
6. **FIX THE P5 LABEL/VALUE CONTRADICTION** ("three" vs 5).

## Quoted evidence

> "Three state-of-the-art systems (Quantinuum H1, IonQ Forte, Delft NV cryogenic+DD) sit at the predicted gravitational floor"

These three are duplicates in (T2·ω) product = 62832 rad·s/s, not three independent confirmations. C8 fail.

> "**Falsifier:** ONE rigorously-reported T2 measurement exceeding T2_grav by more than **10×**"

10× margin is convenient cushion, introduced after v1.0 (which had no margin) failed.

> "All citations are tagged [VERIFY_PRECOMMIT] reflecting training-cutoff (Jan 2026) knowledge."

The 10 citations are unverified. The headline cannot stand on unverified citations.

## Severity

CR064a is the most publicly-checkable claim in the cluster, and the headline does not survive a single competent challenge. REGRADE TO BOUNDARY is the minimum acceptable outcome. The trapped-ion plateau prediction at 10 s is concrete and falsifiable IF the gate-rate-class framing is held constant — but as written, the 10 s value is itself derived from the same Quantinuum H1 number being claimed as confirmation. The falsifier "T2 > 100 s at kHz gate rates" is reachable but is itself a 10× cushion on a 10× cushion.
