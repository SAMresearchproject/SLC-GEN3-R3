# AUDIT_CR122 — Hostile Findings

**CR:** `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE`
**Sealed lock sha256:** `26b4ea2cf3cc6dd89bd47e392e23d3dd600776e9cc14a081a1b0dc81663ad27a`
**Sealed at:** `2026-06-15T19:38:00Z`
**Headline under attack:** qp092h retroactively gates 10 sealed Courtroom CRs across 4 branches through ONE structural rule; direct qA-as-mass overreads Planck Ω_b h² by 0.66–0.99% (max 1.475σ) — REJECTED everywhere.
**Auditor stance:** adversarial; no benefit of the doubt.

---

## Tier Verdict

**TIER 3 — REGRADE_TO_BOUNDARY** (primary)
**TIER 6 — HASH_CHAIN_BREAK** (secondary — qp092h source is external)

CR122 has the most aggressive and load-bearing claim of the three (retroactive structural unification across four branches). The audit will not allow that claim at PASS strength on a 1.475-σ wrong-control rejection. This is a boundary-grade gate, not a structural unification verdict.

---

## Pass/Fail per Criterion (C1–C9)

| # | Criterion | Verdict | Notes |
|---|---|---|---|
| C1 | HASH_CHAIN_INTEGRITY | **FAIL (partial)** | qp092h source: `5b8139aa90883b8b3ac210fdad44055fc9cbf23c6f4e16dbef58668a8d2bda49` lives at `C:/VS/quantum_phase/artifacts/qp092h_baryon_cmb_carrier_gate/qp092h_summary.json` — outside the Courtroom. The 11 gated CRs are themselves inside the Courtroom and properly sha-256 fingerprinted. Mixed: gated targets PASS C1; the gate's source artifact FAILs C1. |
| C2 | FALSIFIER_PRECOMMITTED | PASS (weak) | Two predictions with falsifiers. `CR122_PRED_1` falsifies if any future CR is sealed at PASS using direct qA-as-mass routing — this depends on future curator behaviour, not on a physical measurement. `CR122_PRED_2` falsifies if any future work requires a split other than 1/8 = 2⁻ᴰ — same self-referential dependency. Neither falsifier points to a single observable measurement that could decide it. They are governance falsifiers, not physical ones. |
| C3 | WRONG_CONTROLS_LOAD_BEARING | **FAIL — SEVERE** | The headline wrong-control "direct qA-as-mass" is rejected at a *max* of 1.475σ vs Planck Ω_b h². 1.475σ is well within the noise band of a "WC didn't actually fail." A 1.475σ tension is roughly p=0.14 two-sided. This is a sanity-check signal, not a falsification of the alternative. Calling direct-qA-as-mass "REJECTED everywhere" is overclaim. Honest verdict: "disfavored at ~1.5σ." |
| C4 | FREE_PARAMETERS_HONESTLY_ZERO | PASS | CR122 adds no numerical parameters; it inherits 1/8 from qp091t. |
| C5 | IN_SAMPLE_DISCLOSED | **FAIL** | The 10 gated CRs were sealed *before* the carrier-compression gate existed. The "carrier compression admitted route" was constructed to match what those 10 CRs already did. This is the textbook definition of a retroactive in-sample unification. The CR explicitly says so ("RETROACTIVELY documents one structural rule") — credit for honesty in the lock — but the result.md headline reads "REJECTED everywhere" with no in-sample qualifier. |
| C6 | VERDICT_GRADE_MATCHES_EVIDENCE | **FAIL** | The verdict `TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED` is sealed at PASS. The evidence supports only BOUNDARY: (a) retroactive structural fit, (b) 1.475σ rejection of the alternative, (c) gate construction in the same week as the gated CRs (qp091/qp092 chain ran 2026-06-14 through 2026-06-15; CR122 sealed 2026-06-15T19:38Z). This is "structural overlay discovered ex post," not "unification proven." Regrade to BOUNDARY. |
| C7 | APPEAL_VS_FALSIFICATION_BRIGHT_LINE | **FAIL** | "Direct qA-as-mass REJECTED" is the gate. But what would falsify the *carrier compression rule* itself? CR122_PRED_2 says "if any future work requires a fractional split other than 1/8 = 2⁻ᴰ at D=3 to admit a baryon/CMB inventory closure." This is unfalsifiable in practice: if a future CR uses a different split, the carrier-compression-gate is "incomplete and needs structural revision" (= appeal CR). The escape hatch is the whole gate. The gate cannot be falsified, only revised. |
| C8 | TEXT_MATCHES_VERDICT | **FAIL** | Headline: "Direct qA-as-mass would overread Planck Ω_b h² by 0.66–0.99 percent (max 1.475 sigma) — REJECTED everywhere." 1.475σ ≈ p=0.14. "REJECTED everywhere" is overstatement. Defensible reword: "disfavored at ≲1.5σ; carrier-compression route preferred." |
| C9 | TIMESTAMP_ORDERING_FORMULA_THEN_DATA | **FAIL** | qp092h (the rule source) was sealed 2026-06-15T09:13:04Z. CR122 lock sealed 2026-06-15T19:38:00Z (10 hours later). The 10 gated CRs (CR016, CR018–023, CR111, CR114, CR117) were sealed days to weeks earlier. The rule was extracted *from* the existing CRs and then declared as gating them. This is the in-sample structural overlay caught by C9. The rule was not declared before the data it now gates. |

---

## Specific Demands

### DEMAND-CR122-A (regrade verdict)
**Required:** Regrade CR122 from `SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED` to `BOUNDARY__TEN_PRIOR_CRS_RETROACTIVELY_OVERLAID_BY_CARRIER_COMPRESSION_RULE__GATE_DISFAVORS_DIRECT_QA_AS_MASS_AT_ONE_POINT_FIVE_SIGMA`. The "UNIFIED" claim must come down to "OVERLAID."

### DEMAND-CR122-B (1.475σ rhetoric)
**Required:** Strike "REJECTED everywhere" from result.md and the lock. Replace with "disfavored at ≲1.5σ." A 1.475σ tension is not a rejection by any conventional standard. This is the single most important text change CR122 needs.

### DEMAND-CR122-C (hash chain)
**Required:** Same as CR120-A / CR121-A. Ingest qp092h into a Courtroom-internal upstream-artifact directory or relabel as a fingerprint reference.

### DEMAND-CR122-D (falsification of the rule itself)
**Required:** A separate prediction with a physical falsifier — not a governance falsifier ("if a future CR uses a different split"). For example: "if Planck PR5 or future CMB-S4 measurements bring Ω_b h² to a value that direct-qA-as-mass would now hit better than carrier-compression, the gate is broken." That at least depends on a measurement.

### DEMAND-CR122-E (manuscript framing)
**Required:** Do NOT cite CR122 in the manuscript as a "unification CR." Cite it as a "carrier-compression bookkeeping rule that retroactively organises 10 sealed Courtroom verdicts." That is true. The current framing is not.

---

## Quoted Evidence

From `CR122_carrier_compression_gate_lock.json`:

> `"gate_class": "RETROACTIVE_STRUCTURAL_UNIFICATION_NO_VERDICT_INVALIDATED"`

The word "RETROACTIVE" is in the gate class. Credit for honesty. But the result.md headline does not carry that qualifier through.

From `CR122_summary.json`:

> `"rejected_route_max_sigma_vs_planck_h2": 1.4752660465073755`

This is the number being called "REJECTED."

From qp092h source (`qp092h_summary.json`):

> `"direct_qA_max_sigma_against_planck_h2": 1.4752660465...`
> `"direct_qA_overread_min": 0.00663…`
> `"direct_qA_overread_max": 0.00994…`

The CR faithfully copies these numbers; the audit failure is in the interpretation, not the arithmetic.

From CR122 lock, `what_this_gate_does`:

> "RETROACTIVELY documents one structural rule that unifies 10 sealed Courtroom CRs"

Honest description in the lock. Not carried through to the result.md headline.

From CR122_PRED_2:

> "if any future work requires a fractional split other than 1/8 = 2⁻ᴰ at D=3 to admit a baryon/CMB inventory closure, the carrier-compression rule is incomplete and needs structural revision"

"Incomplete and needs structural revision" = appeal, not falsification. The appeal-escape-hatch is the rule.

---

## Where CR122 succeeds

The arithmetic is clean. The 10 gated CRs are correctly identified. The qp092h source is properly hashed. The structural narrative (qA → 1/8 carrier → ledger compression → A readout) is internally consistent with CR121 and CR120. As a *bookkeeping* artifact it is well-built. As a *unification verdict* it overstates by exactly one σ-grade.
