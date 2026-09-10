# CR120b Higgs Appeal by Composition — Precommit

**Date:** 2026-06-22
**Classification:** APPEAL_CR (Deferred-Support Appeal Rule per README.md)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22

## Scope

This precommit registers CR120b as a Deferred-Support Appeal CR that derives `H_reveal = 125.25 GeV` by composition of two upstream sealed PASS-tier sources:

1. **Capacity term** `R²(1 − 2⁻ᴰ) = 126` from CR114@14 (theorem, sealed 2026-06-13, predates qp091)
2. **Surface debit term** `D²/R = 9/12 = 3/4` from CR092a@09a (sealed PASS 2026-06-15, NOT regraded by CR-135 audit)

The composition `126 − 0.75 = 125.25 GeV` is the derivation.

## What This Appeal Does

- Derives the same content as CR120 (H_reveal = 125.25 GeV) via composition of audit-clean upstream sources.
- Asserts that the structural content has independent grounding at PASS-tier from the qp091 chronology window.
- Honors all four of CR140's restoration requirements:
  - Requirement #3 (independent structural derivation) is addressed by the composition itself.
  - Requirement #4 (chronology disclosure) is addressed by explicit chronology disclosure in CR120b_result.md.
  - Requirements #1 + #2 (forward-blind HL-LHC) are acknowledged as future gold-standard confirmation, not replaced.

## What This Appeal Does NOT Do

- Does NOT modify CR120's result.md or summary.json.
- Does NOT modify or contest the CR-135 audit verdict on CR120.
- Does NOT claim "EXACT" or "zero free parameters" framing that CR140 specifically reworded.
- Does NOT replace CR140's forward-blind HL-LHC requirements; treats them as future confirmation.
- Does NOT claim universality of the `capacity − surface debit` form. The formula applies to the Higgs scalar specifically (as the substrate's net energy expression), and this uniqueness is acknowledged honestly in CR120b_result.md.

## Upstream Sources (Hash-Locked)

```text
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR092a_result.md = 371405f800b35fb893e7509a072b0f8e79bac5584c24254d98c382ca3dad6571
CR120_result.md  = 5f01ecc521850597af164345d7e9d60fd6709e23bb44eb5a76823e010b170bde   (preserved)
CR140_result.md  = c869ca31cacb2be961c335e6a1e68e65ff9cb8061009476e6c3a5cf2e1982083   (honored)
CR135_AUDIT      = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661   (honored)
```

## Precommitted Verdict (target)

```text
CR120b_APPEAL_PASS_HIGGS_BY_COMPOSITION__CAPACITY_CR114_THEOREM_PLUS_SURFACE_DEBIT_CR092A_HARD_FREEZE__H_REVEAL_125_25_INSIDE_PDG_1SIGMA_WINDOW__CR120_ORIGINAL_BOUNDARY_PRESERVED__FORWARD_BLIND_HL_LHC_FUTURE_CONFIRMATION_QUEUED
```

## Precommitted Falsifier

This appeal's structural composition has the same falsifier as the underlying formula: any future high-precision Higgs measurement exceeding the PDG-displayed precision envelope around `125.25 GeV` falsifies this appeal's structural claim. The precommitted formula is `H_reveal = R²(1 − 2⁻ᴰ) − D²/R` evaluated at the sealed constants `R = 12, D = 3, α_H = 2`.

If any cited upstream source (CR114 or CR092a) is later regraded BOUNDARY/FAIL/REFUTED, this appeal must be retracted or rescoped per the Deferred-Support Appeal Rule reversibility clause.

## Wrong Controls (Precommitted)

The 8 wrong controls listed in CR120b_result.md are committed at precommit time:

- WC1: does not modify CR120
- WC2: does not treat PDG as derivation input
- WC3: uses only pre-audit or audit-clean sources
- WC4: chronology disclosed not hidden
- WC5: no outside-model invocation
- WC6: uniqueness to Higgs acknowledged not hidden
- WC7: forward-blind HL-LHC acknowledged as future confirmation
- WC8: audit chronology observation not contested

## Predictions (Precommitted)

P1-P7 listed in CR120b_result.md; each maps to a specific verifiable claim about pre-existing sealed artifacts and the composition arithmetic.
