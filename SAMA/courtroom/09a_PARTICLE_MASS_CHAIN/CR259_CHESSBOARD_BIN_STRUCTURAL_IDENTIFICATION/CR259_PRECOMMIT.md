# CR259 — Chessboard Bin Structural Identification

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_IDENTIFICATION_CR
**Sealed by:** Sean Brady, 2026-06-30
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Structural-identification CR. Reads only the frozen QP093A catalog
statistics file by sha256 and applies pure (ĥ, d̂) integer arithmetic
to verify that the seven QP093A bin counts (and the CR253 / QP106
80-row promoter decomposition derived from them) match closed-form
substrate identities in two primitives.

No measurement, no fit, no catalog data re-processing, no new external
input. The runner reads exactly one input file (the catalog stats
JSON) and emits a verdict based on integer-identity matching.

Same shape as CR033@08 (X∞ substrate-identification): the catalog has
already been enumerated, sealed, and audited; this CR reads its
summary numbers and names which substrate identities they satisfy.
```

## Question

```text
Do the seven QP093A enumerator bin counts and the CR253 80-row promoter
decomposition reduce to closed-form integer compositions of (ĥ = 2,
d̂ = 3) under the substrate atoms

  S = ĥ^d̂ = 8           R = ĥ²·d̂ = 12
  d̂² = 9                  R + 1 = 13 (chessboard side = bigrade + carriers)
  ĥ + d̂ = 5

with no fitted coefficient, no free parameter, and no external scale?
```

## Sealed Identities Under Test

```text
QP093A bin counts (corrected; A-field row removed per QP103/QP104):

  I1.  stable_matter      = d̂² · (S − 1)                 = 9 · 7   = 63
  I2.  antimatter_conj    = ĥ · d̂ · (S − 1)              = 6 · 7   = 42
  I3.  bound_composite    = (R + 1)²                      = 13²     = 169
  I4.  unstable_resonance = (ĥ + d̂)²                     = 5²      = 25
  I5.  catalog_corrected  = I1 + I2 + I3 + I4              = 105 + 169 + 25  = 299

CR253 / QP106 80-row promoter decomposition (also pure ĥ, d̂):

  I6.  promoter_80         = d̂⁴ − 1                       = 81 − 1  = 80
  I7.  promoter_80_alt     = ĥ⁴ · (ĥ + d̂)                 = 16 · 5  = 80
  I8.  promoter_charged    = 2 · ĥ⁵                        = 64      = 32 (matter)  + 32 (anti)
  I9.  promoter_neutral    = ĥ⁴                            = 16
  I10. matter_anti_asym    = ĥ⁴                            = 16     (= neutral count)

CR253 sub-class identities (from the sealed 80-row breakdown):

  I11. charged_matter      = ĥ⁵                            = 32
  I12. neutral_matter      = ĥ⁴                            = 16
  I13. charged_antimatter  = ĥ⁵                            = 32
  I14. neutral_antimatter  = 0
  I15. matter_total        = ĥ⁴ · (ĥ + 1)                  = 48
  I16. anti_total          = ĥ⁵                            = 32

Structural ratios (read but not gated):

  R1.  QP093A matter:anti  = 63 : 42 = d̂ : ĥ              = 3 : 2
  R2.  CR253 matter:anti   = 48 : 32 = d̂ : ĥ              = 3 : 2
  R3.  promoter_80 / F     = (d̂⁴ − 1) / d̂⁴ = 80/81        = closure-act-below-F
```

## Closure Axiom Cross-Reads (informational; not gated)

```text
The closure axiom d̂^(d̂−1) = ĥ^d̂ + 1 (which picks (ĥ, d̂) = (2, 3) at
primitive selection) re-appears in the bin decompositions:

  bound_composite = (R + 1)² where R + 1 is the squared closure-act
                                       shift above R.
  promoter_80     = d̂⁴ − 1   where d̂⁴ = (d̂²)² = (S + 1)² is the
                                       squared closure axiom.
  catalog_corrected expansion:
    299 = (ĥ + d̂) · d̂ · (S − 1)  +  (R + 1)²  +  (ĥ + d̂)²
        =     105                 +     169    +      25
```

## Sealed PASS Gates

```text
PASS:
  G1.  I1–I10 (ten load-bearing identities) all verify as exact integer
       equality against the values read from qp093a_catalog_stats.json
       (with CR253-derived sub-classes for I8–I10).
  G2.  Closure axiom d̂^(d̂−1) = ĥ^d̂ + 1 holds at (ĥ, d̂) = (2, 3).
  G3.  Wrong control W1: at (ĥ, d̂) = (3, 2) the four asymmetric bin
       identities (I1, I2, I3 + the symmetric/asymmetric split for I4)
       distinguish the canonical primitives. Specifically:
         - I1, I2, I3 are asymmetric under primitive swap and must fail
           at (3, 2).
         - I4 = (ĥ+d̂)² is symmetric under primitive swap (since
           ĥ+d̂ = d̂+ĥ) and is expected to match at (3, 2) by symmetry.
           This is not a gate failure; it is a structural observation
           that (ĥ+d̂)² alone does not pin (2, 3) vs (3, 2).
       Gate: at most one of I1–I4 matches at (3, 2), AND I1, I2, I3
       all fail there.
  G4.  Wrong control W2: perturbing any catalog bin by +1 breaks at
       least one identity.  Confirms the identities are not algebraic
       tautologies that any nearby integers would satisfy.
  G5.  Precommit hash verified at runner load.
  G6.  Forbidden-file guard not tripped (whitelist: this precommit, the
       runner source, qp093a_catalog_stats.json, output files).

BOUNDARY:
  Any single G1 sub-check (I1–I10) fails to verify.

FAIL:
  Hash mismatch, forbidden-file guard trips, or runner spec error.
```

## Frozen Input

| field | path |
| --- | --- |
| QP093A catalog stats | `C:\VS\quantum_phase\artifacts\qp093a_stable_particle_combination_enumerator\qp093a_catalog_stats.json` |
| sha256 | `fa20decbfb70aea103953d0dff28d5b1e8445f01342c8dbca4dad6320e39c7f3` |

The CR253 80-row decomposition is cited by sealed CR (precommit
`a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461`) and
its sub-class counts are reproduced in-code as numeric literals — the
runner does NOT open CR253's result file at runtime.

## Rule-9 Line

```text
This test could have falsified the claim that the seven QP093A bin
counts and the CR253 80-row promoter decomposition are closed-form
integer compositions of (ĥ = 2, d̂ = 3) under the listed substrate
identities, by any one of identities I1–I10 not matching the catalog's
sealed value, OR by the wrong-control at (ĥ = 3, d̂ = 2) accidentally
matching the same counts.
```

## What This CR Seals

A structural-identification CR for the matter-sector enumeration. After
sealing:

- The 169 bound composites is named as `T13² = (R + 1)²` — the carrier-
  lane chessboard.
- The 80-row promoter is named as `d̂⁴ − 1`, one closure-act below F.
- The matter:antimatter ratio is named as `d̂:ĥ`.
- The matter-antimatter asymmetry (16) is named as the neutral matter
  count `ĥ⁴`, a structural identity rather than a tuned parameter.

No fitting, no new constants, no new external data. The catalog stays
sealed at its existing hash; this CR reads it and emits the substrate-
natural reading.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| QP093A catalog stats | `fa20decbfb70aea103953d0dff28d5b1e8445f01342c8dbca4dad6320e39c7f3` |
| CR253@09a 80-row promoter | precommit `a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461` |
| CR033@08 (parallel structural-ID pattern) | precommit `fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810` |
| CR258@09a substrate primitive closure audit | precommit `77c58a51d82d8eef075a75c9e37d44a9363df1bf346c35d95dc6d9410a89f447` |
| three_dimensional_binary.py (companion tool) | `46e41ff3e255c79f01f75a79510c68bd39e1d202257faeaff1e01ff018957469` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
