# CR229 Carrier-Tensor Inclusion-Exclusion Identity — Precommit

**Date:** 2026-06-22
**Classification:** STRUCTURAL_IDENTITY_CR (unification of three previously-sealed identities)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("let's see what happens")

## Scope

This precommit registers CR229 as a structural-identity CR that formalizes the set-theoretic inclusion-exclusion identity on the closed carrier-tensor ledger. The identity unifies three previously-sealed independent structural facts:

- `R² = 144` (capacity, CR114@14)
- `R²(1 − 2⁻ᴰ) = 126` (H_native, CR114@14 + CR092a@09a)
- `162 = R²·9/8` (closed carrier-tensor ledger, CR217@09a + CR222@12a)

as the single inclusion-exclusion identity:

```
With A, B = two sides of the closed carrier-tensor ledger:
  |A| = |B| = 81
  |A ∩ B| = 18 = α_H · D² (the tensor carrier / graviton)

Then:
  |A ∪ B|       = 144 = R²              (capacity)
  |A Δ B|       = 126 = R²(1 − 2⁻ᴰ)     (H_native)
  |A| + |B|     = 162 = R²·9/8           (closed ledger)
```

## What This CR Does

- Formalizes the set-theoretic identity that derives all three previously-independent structural facts from one underlying decomposition.
- Identifies the substrate structurally with the closed carrier-tensor ledger.
- Identifies the graviton structurally with the shared overlap |A ∩ B|.
- Identifies matter-energy structurally with the symmetric difference |A Δ B|.

## What This CR Does NOT Do

- Does NOT modify any upstream CR (CR114, CR116, CR217, CR218, CR222, CR132, CR092a, CR120b).
- Does NOT introduce new free parameters.
- Does NOT claim to derive the upstream identities — it unifies them.
- Does NOT replace CR140's forward-blind HL-LHC restoration requirement on CR120 (Higgs).
- Does NOT extend the inclusion-exclusion reading to non-Higgs particles.

## Upstream Sources (Hash-Locked, Read-Only)

```text
CR114_result.md       = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR116_result.md       = 4385529ee82f863e5c2ac40ad2ce0114b71c84e3720d09d96d1fdde79bf07464
CR217_result.md       = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR218_result.md       = c2552aa075ba989e0c6c30c658aa109ab005aed0df9cbf419de71779fbe8bf6e
CR092a_result.md      = 371405f800b35fb893e7509a072b0f8e79bac5584c24254d98c382ca3dad6571
CR132_result.md       = 09fb22d1c13c44025f540f5134658ecca81cf62c67c6ce1c15cea751adfed2d6
CR222_result.md       = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR120b_result.md      = e60ac0371443b6d839a1018ccdf371b86d7a78627ea8fd1c919733fedb1b9574
```

## Precommitted Verdict

```text
CR229_PASS_CARRIER_TENSOR_INCLUSION_EXCLUSION_IDENTITY__SUBSTRATE_IS_CLOSED_CARRIER_TENSOR_LEDGER__THREE_UPSTREAM_IDENTITIES_UNIFIED__CAPACITY_144_HNATIVE_126_CLOSED_LEDGER_162_ALL_FOLLOW_FROM_SET_THEORETIC_INCLUSION_EXCLUSION_ON_TWO_81_SIDES_WITH_18_OVERLAP
```

## Precommitted Predictions (P1-P10)

P1-P10 listed in CR229_result.md. All are algebraic identities verifiable by inspection from the upstream-sealed constraints |A| = |B| = 81 and |A ∩ B| = 18.

## Precommitted Wrong Controls (WC1-WC10)

WC1-WC10 listed in CR229_result.md. They test the structural-uniqueness of |A| = |B| = 81 and |A ∩ B| = 18 (varying these values breaks the upstream identities), confirm the inclusion-exclusion identity is standard set theory, and verify the graviton-as-overlap interpretation is consistent with upstream sealings.

## Precommitted Falsifier

If any of the upstream sealed identities (CR114 capacity R² = 144; CR114+CR092a H_native = 126; CR217+CR222 closed ledger = 162; CR114+CR116+CR132 graviton = 18) is later regraded, this CR's inclusion-exclusion identity must be re-examined and either retracted or rescoped per the reversibility clause.

If a counter-derivation shows the substrate has structural content NOT captured by the closed carrier-tensor ledger (i.e., if the 162 ledger turns out to be a partial inventory rather than the complete substrate), this CR's "substrate IS carrier-tensor ledger" ontological claim falsifies.

## Reversibility Clause

This CR's structural-identification claim depends on the upstream sealed values remaining sealed at PASS. If any upstream source is regraded BOUNDARY/FAIL/REFUTED, this CR's verdict must be retracted or rescoped accordingly. The arithmetic identity (`144 = 81+81−18`, etc.) survives any regrade, but the structural interpretation as "substrate IS carrier-tensor ledger" depends on the upstream sealed identifications.
