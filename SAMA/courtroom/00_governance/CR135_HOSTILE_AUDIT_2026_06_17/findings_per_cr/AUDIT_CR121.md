# AUDIT_CR121 — Hostile Findings

**CR:** `CR121_SAM_GRAVITY_MECHANISM_INTAKE`
**Sealed lock sha256:** `01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469`
**Sealed at:** `2026-06-15T18:32:34Z`
**Headline under attack:** Gravity = matter ledger compression via 1/8 unresolved tensor carrier + qA → A field update; "weak-field gravity readouts recovered, zero free parameters."
**Auditor stance:** adversarial; no benefit of the doubt.

---

## Tier Verdict

**TIER 6 — HASH_CHAIN_BREAK** (primary)
**TIER 5 — REQUIRES_APPEAL_CR** (secondary, C7 appeal-vs-falsifier line on qA-as-mass is permissive)

Less hostile than CR120 because (a) the falsifiers are concrete and (b) the chain content is genuinely connected to existing branch 11/CR076 scope. But the gravity mechanism is structurally aggressive enough that the audit must demand both a chain-of-custody fix and a refinement of how "qA-as-mass rejected" is operationalized.

---

## Pass/Fail per Criterion (C1–C9)

| # | Criterion | Verdict | Notes |
|---|---|---|---|
| C1 | HASH_CHAIN_INTEGRITY | **FAIL** | All 9 qp092 artifact summaries (`qp092a_split_loss_summary.json`, `qp092b…h_summary.json`) live in `C:/VS/quantum_phase/artifacts/qp092*/`. Confirmed by glob: zero `qp092*` paths inside `C:/VS/The_Courtroom`. Same orphan-reference structure as CR120. |
| C2 | FALSIFIER_PRECOMMITTED | PASS | Four predictions (`CR121_PRED_1/2/3/4`) each carry concrete one-violation falsifiers: GW third polarization or v≠c (PRED_1); A-dependent clock shift not predicted by per-body A (PRED_2); discovery of a stable particle near 18 GeV with the right tensor quantum numbers (PRED_3); strong-field behavior requiring graviton mass or extra parameter (PRED_4). PRED_1 and PRED_3 are the strongest. |
| C3 | WRONG_CONTROLS_LOAD_BEARING | PARTIAL FAIL | WC1–WC8 in CR121 are scope guards ("does not claim graviton particle discovery," "does not promote tensor carrier to matter row") — they reject overclaims, not the mechanism. The load-bearing wrong control is "direct qA-as-mass" inside qp092a/b/c/d/e/f/g/h. That IS a real WC and it does break (rejected in all 8). Credit given here, but the CR's local WC list is procedural theater. |
| C4 | FREE_PARAMETERS_HONESTLY_ZERO | PARTIAL FAIL | The R²=144, D=3, 1/8 split inherit from qp091t; CR121 adds no new tunable parameters. However the *mechanism* `qA → 1/8 carrier → ledger compression → A field update` introduces several named structural pieces (the carrier coupling rule, the ledger compression rule, the A-kernel recovery at point/multi/extended) which were derived in qp092c hard-freeze. None of these has a SAM first-principles derivation cited; they are stipulated as the route. "Zero free parameters" is technically true (no numeric knobs) but obscures the structural choices made when constructing the chain. |
| C5 | IN_SAMPLE_DISCLOSED | PASS (with caveat) | The G-clock path delay recovered at qp092e is openly described as "recovered from the tensor-carrier mechanism," matching CR005 (GPS) and CR006 (Shapiro) at standard precision. This is honestly in-sample: weak-field GR is the input the SAM mechanism was constructed to reproduce. The CR does not, however, label it that way; it reads as if a derivation gave you weak-field GR rather than the other way around. Reword needed. |
| C6 | VERDICT_GRADE_MATCHES_EVIDENCE | PASS | The verdict explicitly says `NOT_GRAVITON_NOT_FULL_QG_THEOREM`. Strong-field and graviton claims are not made. Scope is honest. This is the cleanest criterion for CR121. |
| C7 | APPEAL_VS_FALSIFICATION_BRIGHT_LINE | **FAIL — SUBTLE** | The "qA-as-mass REJECTED" boundary is enforced as a hard wrong control. But the rejection criterion is "direct qA-as-mass gives a 0.66–0.99% overread vs Planck Ω_b h²." The same numbers are quoted three times across the chain (qp091t/qp092h/CR122). If a future measurement falsified CR121_PRED_2 (clock shifts) or PRED_4 (strong-field), the chain can route the failure to the "carrier compression" side rather than to the gravity mechanism itself. The bright line between (a) "carrier compression rule needs revision" (appeal) and (b) "the 1/8 + qA gravity mechanism is wrong" (falsification) is not drawn. Every failure mode currently maps to (a). |
| C8 | TEXT_MATCHES_VERDICT | PASS (weak) | Headline says "weak-field gravity readouts recovered," correctly scoped. But the closing sentence "no graviton particle, no free parameter, weak-field gravity readouts recovered" implies more than the chain delivers: the chain *replays* GR's weak-field signature; it does not generate new predictions there. Minor reword would tighten this. |
| C9 | TIMESTAMP_ORDERING_FORMULA_THEN_DATA | PASS | Unlike CR120, the qp092 mechanism does not target a specific numeric value that could be retro-fit. The "1/8" split is inherited from qp091t, not chosen to land on a gravity number. The mechanism reproduces (does not predict) GR's weak-field structure, which is in-sample but not target-fit. |

---

## Specific Demands

### DEMAND-CR121-A (hash-chain break, blocks manuscript)
**Required:** Same as CR120-A. The 9 qp092 `summary.json` files must be ingested into a `The_Courtroom/upstream_artifacts/qp092_chain/` directory or the intake must be clearly relabelled as a "fingerprint manifest" of files living outside the Courtroom immutability boundary.

### DEMAND-CR121-B (C7 appeal-vs-falsification line on qA-as-mass)
**Required:** A separate CR that documents what observation would falsify the *gravity mechanism* — distinct from what would prompt an appeal to the carrier-compression rule. As written, every clock-shift or strong-field failure can be re-routed to "ledger compression rule needs revision," which makes the mechanism unfalsifiable. Specifically: state whether `CR121_PRED_2`'s falsification kills the mechanism or only the per-body A interpretation. State whether `CR121_PRED_4`'s failure (strong-field deviation) is a falsifier or an appeal.

### DEMAND-CR121-C (C4 mechanism stipulation)
**Required:** Each of the four mechanism rules introduced in stages 3–6 of qp092 (qA loads 1/8 carrier; ledger compression updates A; A(r) = r_s/r kernel recovery at point/multi/extended; conservation across particle/macro/propagation) needs a SAM first-principles derivation citation. Currently they are "frozen by qp092X PASS" — which is self-reference. SAM principle X demands result Y is the structure missing here.

### DEMAND-CR121-D (manuscript framing)
**Required:** Frame CR121 in the manuscript explicitly as "consistency with weak-field GR plus a mechanism story that explains why" rather than "derivation of weak-field GR from SAM first principles." The chain achieves the first; it does not achieve the second. The "no free parameter" claim is consistent with the first framing but not the second.

### DEMAND-CR121-E (PRED_3 18 GeV scope)
**Required:** Tighten `CR121_PRED_3`. "No new particle at 18 GeV" is testable but the qualifier "with the right tensor-channel quantum numbers" is open enough that any observed 18 GeV resonance can be reclassified. State the quantum numbers explicitly.

---

## Quoted Evidence

From `CR121_gravity_mechanism_intake_lock.json`:

> `"qp092_chain_summary_hashes": { "qp092a_split_loss_summary.json": "649e61e0…", … }` — hash list only; no copy of the files inside the Courtroom.

From CR121 runner-equivalent (the lock):

> `"frozen_by": "qp092c PASS + qp092c hard freeze"` (stage 4 of mechanism chain)

This is self-reference. The chain freezes itself.

From `CR121_result.md`:

> "No graviton particle, no free parameter, weak-field gravity readouts recovered."

The first two clauses are honest. The third oversells — weak-field readouts are *reproduced*, not predicted. For the manuscript this matters.

From CR121_PRED_3:

> "No new particle at 18 GeV (= R² · 1/8 = 144/8) will be detected at the LHC or future colliders."

This is a good forward-blind null prediction. The 18 GeV mass is fully derivable from the structural inputs, not a free choice. Credit on this one — it is genuinely courtroom-quality if the qualifier on quantum numbers is tightened.

---

## What CR121 does right

- Honest scope ("NOT graviton, NOT full QG theorem")
- Four concrete falsifiers, one of which (`PRED_3`) is a clean null prediction at a structurally derived mass
- Branch-11 CR076 BOUNDARY is preserved unmodified
- CR104a Layer 4b per-body A is genuinely connected as the mechanism for "each body has its own A"

These are not nothing. CR121 is not a "fail dressed as a pass" — it is an honestly scoped mechanism intake with a hash-custody hole and a not-fully-drawn falsification line.
