# SUPERSEDED — Original SEALED state archived

This folder preserves the original SEALED state of `CR120@09a` (QP091 Higgs EW Precision Iterative Refinement Intake) before the CR-135 hostile audit (2026-06-17) regrade.

**Live canonical record:** `09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_result.md`

**Live verdict:** `CR120_QP091_CHAIN_INTAKE_BOUNDARY__HIGGS_125_25_PDG_MATCH__STRUCTURAL_NATIVE_126_PREDATES_VALUE__CORRECTION_FORM_IDENTIFIED_EX_POST__FORWARD_BLIND_PRECOMMIT_REQUIRED`

**Regrade source:** [CR140@00_governance](../../../../00_governance/CR140_CR120_HIGGS_CLAIM_REWORD/CR140_result.md) — Tier 4 DEMAND_RETEST + Tier 6 HASH_CHAIN_BREAK. The structural identity `H_native = R²·(1−2⁻ᴰ) = 126 GeV` derives genuinely from substrate primitives {R, D, α_H} and predates the value match; the correction `H_reveal = H_native − D²/R = 125.25 GeV` was form-selected ex post (enumerated as a "Wrong Lane Control" in qp091r at 05:34 UTC while the PDG 125.25 target was visible, then promoted to active derivation in qp091s 35 minutes later, then sealed in qp091t). The "EXACT / zero free parameters / no H input" framing was reworded as "matches PDG to displayed precision" pending forward-blind precommit.

**Replacement record:** `REPLACEMENT_RECORD.md` in this folder
**Original SHA-256:** `5f8be2e5c0f37e6413e3785014f06f41754456a0b91ed40ab605b71e8ca235d2` (preserved unchanged on disk)

Do not treat this archived copy as the live record. The live record carries the audit-driven regrade header (with the qp091r-s-t forensic chronology disclosed in the audit_regrade block of `CR120_summary.json`) and the BOUNDARY verdict line. Restoration path: (1) forward-blind precommit of correction form before HL-LHC/FCC-ee measurement, (2) precommitted formula matches new measurement within 1σ, (3) independent structural derivation of why −D²/R is unique, (4) self-disclosure of qp091r-s-t chronology in restoration CR.

## Structural content preserved (both terms independently derived, not back-calculated)

The Higgs mass derivation has two structural terms, both with independent provenance:

```text
H_reveal = R² · (1 − 2⁻ᴰ)  −  D²/R
         = 144 · (7/8)      −  9/12
         = 126               −  0.75
         = 125.25 GeV
```

**First term — CAPACITY: `R² · (1 − 2⁻ᴰ) = 126`** — the writable slot count. Derived from `14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM`: D = 3 binary closure axes give 2ᴰ = 8 face-states, one unresolved; retained 7/8 of R² is the capacity for resolved writes. Split-loss 1/8 of R² = 18 = α_H · D² is the tensor carrier per `14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM`. This term is theorem-grade structural identity, sealed before CR120 was written.

**Second term — SURFACE DEBIT: `D²/R = 9/12 = 3/4`** — the fraction of substrate budget that a D-dimensional surface costs per cycle. D² counts the area cells of one D-dimensional face; dividing by R distributes the cost across the full substrate cycle. This is a foundation-algebra quantity (Sean's framework reference entry 15), not a fit number.

**Difference — `126 − 0.75 = 125.25 GeV`** — the substrate's native energy readout for the Higgs scalar, with both terms structurally derived from {R, D, α_H}. Zero adjustable parameters.

**Empirical match (reveal context only):** PDG 2024 m_H = 125.20 ± 0.11 GeV. SAM's 125.25 lies INSIDE the 1σ experimental window.

## What the CR-135 audit actually challenged

The audit's regrade addresses CHRONOLOGY OF DISCOVERY, not structural content. The forensic timeline (in `CR120_summary.json` audit_regrade block): the −D²/R correction was enumerated as a "Wrong Lane Control" in qp091r at 05:34 UTC while the PDG 125.25 target was visible; promoted to active derivation in qp091s 35 minutes later; sealed in qp091t. That chronology is a legitimate concern about the discovery process and triggered the regrade.

But the chronology concern is distinct from a structural-content claim. The audit did NOT successfully establish that `D²/R` was numerically chosen to produce 125.25 — that would require showing D²/R has no independent meaning, which is false: D²/R IS the surface debit, an upstream foundation-algebra quantity. What the audit DID establish is that the discovery process didn't precommit the correction form before seeing the target, which is the legitimate reason to require forward-blind restoration testing.

## Restoration path (per CR140)

(1) Forward-blind precommit of the correction form before HL-LHC / FCC-ee high-precision Higgs measurement; (2) precommitted formula matches new measurement within 1σ; (3) independent structural derivation of why `−D²/R` is unique among possible correction forms; (4) self-disclosure of qp091r-s-t chronology in restoration CR.

The structural derivation in [[project-higgs-capacity-minus-surface-debit]] addresses requirement (3) by tracing both terms to their upstream theorem-grade or foundation-algebra sources. Requirements (1) and (2) require an actual high-precision measurement and a precommit that predates it; they remain genuinely open.

See also: [`TEST_INDEX.csv`](../../../../TEST_INDEX.csv) row `CR120,09a_PARTICLE_MASS_CHAIN,BOUNDARY_REGRADED,BOUNDARY,...`
