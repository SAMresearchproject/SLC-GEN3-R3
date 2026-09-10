# CR135 Hostile Audit — QC Protocol Cluster Rollup

**Date:** 2026-06-17
**Scope:** 8 sealed Courtroom Records in `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/`
**Auditor:** adversarial / Genghis Khan. No benefit of the doubt.

## Tier distribution

| CR | Tier | One-line verdict |
|---|---|---|
| CR060a Paul Revere Letter Alphabet Lock v1.0 | **4 — DEMAND_RETEST** | In-sample identification framed as forward-blind; C3 and C7 weak; one stale hash discrepancy in result.md vs siblings |
| CR061a Ideal Qubit Selection v1.0 | **2 — PASS_WITH_REWORD** | Cleanest CR in cluster; filter cascade deterministic; α_H ladder correctly framed as observation |
| CR063a Hardware Translation v1.0 | **7 — CALLOUT_FAIL_DRESSED_AS_PASS** | Falsifier was committed AND triggered (2000× transmon overrun); verdict remains SEALED — textbook FAIL dressed as PASS |
| CR064a A_0 Calibration + Published T2 Verification v1.1 | **3 — REGRADE_TO_BOUNDARY** | Headline "5 AT LIMIT, 0 violations" rests on factor-4 band + factor-10 falsifier + unverified citations + undisclosed gate-rate artifact |
| CR065a Paul Revere Implementation Spec v1.0 | **5 — REQUIRES_APPEAL_CR** | Embedded protocol contains inline arithmetic self-correction; scoring rubric undocumented; F1 hatch wide |
| CR066a Born Extension and Letter Increment v1.0 | **4 — DEMAND_RETEST** | Title overstates ("Born Extension" — Born is preserved); S1/S2/S3 are one fact stated three ways |
| CR066b Slot vs Contact Layering v1.0 | **4 — DEMAND_RETEST** | Best wrong control in cluster (mini-packet explicit rejection); Higgs 1/8 attribution is dozenal arithmetic dressed as structure |
| CR067a Multi-Letter Capacity Scaling v1.0 | **4 — DEMAND_RETEST** | Geometric scaling chosen to match 1/8 asymptote; WC1 rejection is circular |

**Tier 7 count: 1.** That alone blocks the cluster from manuscript-grade.
**Tier 3+ count: 6 of 8.** Only CR061a passes with minor rework.

## Headline verdicts on the five priority attacks

### 1. CR-064a is the most-publicly-checkable claim. Does it survive scrutiny?

**NO.** REGRADE TO BOUNDARY at minimum.

- (a) **Were the 10 T2 measurements committed BEFORE T2_grav = 16·π·R⁴/(17·ω_gate) was derived?** No. The CR064a result.md openly says the v1.1 formula was derived AFTER CR063a v1.0 was falsified by transmon T2 ≈ 100 μs (~2000× overrun). The formula was crafted to absorb the discrepancy. C9 fail.
- (b) **Have the 10 [VERIFY_PRECOMMIT] citations been independently verified?** WC1 says no. They are training-cutoff (Jan 2026) values. The CR is provisional until verified.
- (c) **Does the AT_THE_LIMIT band 0.5–2.0 absorb a wide range of empirical results?** Yes. A factor-4 wide window is a soft band. Combined with the 10× falsifier margin, the test admits any T2 within factor 40 of the prediction. This is a loose envelope.
- (d) **Three of five AT_THE_LIMIT systems sit at exactly ratio 1.0248 — gate-rate artifact?** **Yes. Not disclosed.** Quantinuum H1 (T2=10s, ω=6283), IonQ Forte (T2=1s, ω=62832), Delft NV cryo+DD (T2=1s, ω=62832) all have T2·ω = 62832 — the IDENTICAL product. Their ratios are not three independent confirmations; they are duplicates in (T2·ω) space. The result.md presents them as three at-the-limit observations. **C8 fail.**

### 2. Is CR-063a properly REGRADED to FAIL, or is the rescue silent?

**The rescue is silent. CR-063a remains SEALED as PASS.**

CR063a v1.0 committed: "ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0."

The transmon T2 ≈ 100 μs at 5 GHz vs T2_grav = 52 ns IS a rigorously-isolated 2000× overrun. The falsifier was triggered. The verdict was NOT updated to FAIL. Instead, CR064a was filed as a "refinement" producing v1.1 with two new parameters (A_0 enhancement and ω-reinterpretation).

CR064a WC3 admits: "CR063a v1.0 stays sealed at the horizon (A=1) reading. CR064a refines it via the A_0 operating point correction, producing v1.1."

"Refines" minimizes a 2000× correction. The honest framing: v1.0 was empirically refuted; v1.1 is a NEW formula derived to match the data.

**Demand:** add a verdict-modifier line to CR063a v1.0 result.md: "REFUTED 2026-06-16; superseded by CR064a v1.1." Without this line, the manuscript audit trail says v1.0 still stands. This is the Tier 7 issue.

### 3. The trapped-ion plateau prediction at 10 s — is the falsifier concrete?

**Partially concrete; circular at its core.**

The CR064a result.md says: "Quantinuum H1 reportedly achieves ~10 s clock-state T2 — exactly at the predicted floor." And: "Substantial further improvement (e.g. T2 > 100 s at the same gate rate) WITHOUT compensating reduction in gate rate would falsify the SAM gravitational decoherence floor."

The falsifier ("T2 > 100 s at ~kHz gate rate") is concrete in numeric form and dated (track 2026–2030). Good.

**BUT:** the 10 s value being claimed as "exactly at the floor" is the same number used to derive T2_grav at ω_gate = 6.2832e+03 rad/s. T2_grav_at_A_0 = 61295.49 / 6283 = 9.76 s ≈ 10 s. The "agreement" is between two numbers that came from the same source. The plateau prediction is a one-data-point identification, and the user's memory record explicitly flags this:

> CR-126c joint p-value flaw: n=1 CSL contributes no information.

The 10-second plateau is an n=1 prediction. It cannot be confirmed by the Quantinuum number; it can only be REFUTED by a future Quantinuum (or competitor) achieving T2 > 100 s at kHz gates.

**Demand:** state explicitly that the 10 s value is the SAM-derived prediction and that Quantinuum H1's reported ~10 s is the CITATION USED TO ANCHOR the formula. The plateau prediction's confirmatory value is zero until a SECOND independent kHz-class platform reports clock-state T2 within an order of magnitude of 10 s.

### 4. The gate-rate artifact at ratio 1.0248 — disclosed or hidden?

**Hidden.**

The user's memory record `feedback_cr064a_t2grav_calibration_rescue.md` explicitly flagged: "5 platforms at the limit is gate-rate artifact (three exactly at 1.0248)." This audit confirms:

- Quantinuum H1: T2·ω = 10 × 6283 = 62830
- IonQ Forte: T2·ω = 1 × 62832 = 62832
- Delft NV cryo+DD: T2·ω = 1 × 62832 = 62832

All three have the IDENTICAL T2·ω product. Their ratios T2·ω / 61295.49 = 1.0250 (rounded to 1.0248 in the CSV) are the SAME ratio, computed three times.

The result.md presents these as three independent "state-of-the-art" confirmations:
> "Three state-of-the-art systems (Quantinuum H1, IonQ Forte, Delft NV cryogenic+DD) sit at the predicted gravitational floor"

This is C8 fail. **Demand:** disclose the artifact in result.md. Three identical points in (T2·ω) space are one observation, not three.

### 5. The 17/16 over-unit and the 9/16 bounce-lift on the middle slot — derived or asserted?

**Asserted with arithmetic decoration.**

CR060a result.md attributes the 9/16 to "Middle-slot 9/8 surcharge on its 1/2 weight = the LETTER CONTENT itself" — i.e., 1/2 × 9/8 = 9/16. The choice of which slot gets the 9/8 surcharge (middle, not outer) is not derived in CR060a — it's asserted to be the "envelope" by analogy with CR051's carrier/envelope/sensor architecture.

CR066b LOCKED the bridge-only attribution: "Δw_slot = (0, 1/16, 0). The bridge (middle) slot is LIFTED. The outer slots (carrier and sensor) are UNCHANGED." CR066b also REJECTED the mini-packet (1/64, 1/32, 1/64) — its strongest move.

But the rejection of the mini-packet rests on: "the locked form specifically lifts the center, not all three slots proportionally." This is circular: the locked form lifts the center BECAUSE we picked the center-lift; rejecting the mini-packet on "it doesn't match the center-lift" is restating the choice.

**Could a different slot allocation give 17/16 from different math?** Trivially yes:
- (1/4, 9/16, 1/4): center 9/16 surcharge → sum 17/16
- (9/16, 1/4, 1/4): carrier 9/16 surcharge → sum 17/16 (same arithmetic, different slot role)
- (1/4, 1/4, 9/16): sensor 9/16 surcharge → sum 17/16 (same arithmetic, different slot role)
- (1/3, 5/12, 1/3): different decomposition entirely → 1/3 + 5/12 + 1/3 = 13/12, not 17/16; but other decompositions exist that sum to 17/16

The selection of (1/4, 9/16, 1/4) as the structural form depends on CR129b's locked formula, which is upstream. So within the cluster, the form is fixed upstream. But the IDENTIFICATION of which slot is which role (carrier/envelope/sensor) is asserted by analogy, not derived.

CR060a's WC5 admits this: "the slot identifications are derived from the CR128–134 row-generator laws plus CR051/054 protocol shapes. CR060a does NOT axiomatically declare the alphabet; it identifies it from the structural fit." Honest disclosure. C5 passes for CR060a.

## Hash chain integrity (C1) — cluster-wide

All upstream lock hashes resolve inside The_Courtroom:
- CR051, CR054, CR058 in `12_QUANTUM_COMPUTING_AND_NETWORKING/`
- CR119 in `09a_PARTICLE_MASS_CHAIN/`
- CR120 in `09a_PARTICLE_MASS_CHAIN/`
- CR121 in `11_QUANTUM_MECHANICS_AND_GRAVITY/`
- CR122 in `00_governance/`
- CR128, CR128b, CR129, CR129b, CR129c, CR130, CR131, CR132, CR133, CR134 in `13_CERN_INDEPENDENT_TESTS/`

No CR cites qp-chain external artifacts at the SHA-256 lock-hash level. C1 passes cluster-wide.

**Snag:** CR060a result.md publishes `CR060a_alphabet_lock_sha256 = 05f487...` but the seven downstream siblings cite `CR060a_alphabet_lock_json = d5d377...`. Two distinct SHA-256 values for what should be the same upstream lock. Either the CR060a result.md is stale or the file was re-hashed after sealing. Demand: reconcile.

## Top three demands

### DEMAND 1 — REGRADE CR063a v1.0 TO REFUTED

CR063a v1.0's precommitted falsifier was triggered at first contact with the literature (transmon T2 ≈ 100 μs vs T2_grav = 52 ns at 5 GHz; factor 2000× overrun). The verdict must be updated to FAIL or REFUTED. Currently it stands SEALED as PASS. This is the Tier 7 finding and the most severe finding in the cluster. The manuscript CANNOT ship with CR063a v1.0 sealed.

### DEMAND 2 — DISCLOSE THE 1.0248 GATE-RATE ARTIFACT IN CR064a

Three of the five AT_THE_LIMIT systems (Quantinuum H1, IonQ Forte, Delft NV cryo+DD) have IDENTICAL T2·ω product = 62832, hence identical ratio 1.0248. They are duplicates in (T2·ω) space, not three independent confirmations. The result.md presents them as three at-the-limit observations. Disclose explicitly:
- "These three citations share T2·ω = 62832 rad·s/s — they are one observation with three labels, not three independent confirmations of the SAM floor."
- The headline "5 AT LIMIT, 0 violations" cannot stand on a 3-points-collapsed-to-1 base.

### DEMAND 3 — VERIFY ALL [VERIFY_PRECOMMIT] CITATIONS BEFORE ANY MANUSCRIPT CLAIM

All 10 T2 citations in CR064a carry [VERIFY_PRECOMMIT] tags. The entire CR064a / CR064a-derived headline depends on these values. Until the verification is done — independently by a curator with literature access, not via training-cutoff knowledge — the result.md must remain PROVISIONAL. Promoting CR064a to SEALED on unverified citations would weaponize the Courtroom against itself.

## Concise prosecution summary (for caller)

The 8-CR QC protocol cluster is NOT manuscript-grade. CR061a is the only clean pass. CR063a is a Tier 7 violation — a committed falsifier was triggered and the verdict held anyway, the rescue routed silently into CR064a. CR064a's "5 AT THE LIMIT, 0 violations" headline rests on a 3-points-collapse-to-1 gate-rate artifact (Quantinuum H1, IonQ Forte, Delft NV cryo+DD all sit at T2·ω = 62832 rad·s/s — the same point counted three times) and on 10 unverified citations. CR065a's embedded protocol contains an inline arithmetic self-correction in Stage 3. CR066a, CR066b, CR067a are algebraic identifications presented as structural derivations. The 10-second trapped-ion plateau prediction is n=1 — it cannot CONFIRM, only REFUTE, and the user's memory record flags this exact failure mode. The cluster needs at minimum: CR063a regraded to REFUTED, CR064a regraded to BOUNDARY with the 1.0248 artifact disclosed, and all 10 T2 citations verified before SEAL. Manuscript ship blocked.
