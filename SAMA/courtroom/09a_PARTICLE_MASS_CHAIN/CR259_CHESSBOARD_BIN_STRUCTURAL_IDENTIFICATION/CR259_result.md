# CR259 -- Chessboard Bin Structural Identification -- RESULT

```text
verdict           : PASS
classification    : STRUCTURAL_IDENTIFICATION_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-30
precommit_hash    : 53ec3c8912e31d109767d080953088b8677cdd27836b75cc818a8c54222eb660
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
free_parameters_introduced : 0
prior_CR_result_inputs     : false
catalog_fit_parameters     : 0
```

## Headline

The seven QP093A enumerator bin counts and the CR253 80-row promoter
decomposition reduce to closed-form integer compositions of (ĥ = 2,
d̂ = 3) under the substrate atoms (S, R, R+1, ĥ+d̂, d̂²). Ten load-
bearing identities verify exactly; two wrong controls confirm
specificity at the canonical primitives.

The 169 bound composites is the T13 chessboard `(R+1)² = 13²`. The
80-row promoter is `d̂⁴ − 1 = ĥ⁴(ĥ+d̂)`, one closure-act below F. The
matter:antimatter ratio is `d̂:ĥ = 3:2` in both the QP093A enumeration
and the CR253 strict promoter set. The matter-antimatter asymmetry
(16) equals the neutral-matter count `ĥ⁴`.

## QP093A bin counts (read by hash; not re-derived)

| bin | catalog count | substrate identity | value | match |
| --- | ---: | --- | ---: | :---: |
| stable_matter      | 63  | d̂²·(S−1)        | 63  | OK |
| antimatter_conj    | 42  | ĥ·d̂·(S−1)       | 42  | OK |
| bound_composite    | 169 | (R+1)² = T13²    | 169 | OK |
| unstable_resonance | 25  | (ĥ+d̂)²          | 25  | OK |
| **catalog total**  | **299** | **I1+I2+I3+I4**  | **299** | **OK** |

## CR253 80-row promoter decomposition (cited by sealed precommit; numeric literals)

| sub-class | count | substrate identity | value |
| --- | ---: | --- | ---: |
| charged matter      | 32 | ĥ⁵                | 32 |
| neutral matter      | 16 | ĥ⁴                | 16 |
| charged antimatter  | 32 | ĥ⁵                | 32 |
| neutral antimatter  |  0 | —                  |  0 |
| **promoter total**  | **80** | **d̂⁴ − 1 = ĥ⁴(ĥ+d̂)** | **80** |

## Structural ratios (reported; not gated)

```text
QP093A matter:antimatter     63 : 42  =  d̂ : ĥ  =  3 : 2
CR253 matter:antimatter      48 : 32  =  d̂ : ĥ  =  3 : 2
promoter_80 / F               80 / 81 =  one closure-act below the carrier surface

matter − antimatter (CR253)  =  48 − 32 = 16  =  ĥ⁴  =  neutral_matter_count
```

The matter-antimatter asymmetry equals the neutral-matter count
because neutral rows have no A-operator mirror under charge conjugation
(QP109@QP-vault confirmed this in the antimatter-conjugate route test).

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| G1 | ten identities I1–I10 at (ĥ, d̂) = (2, 3) | PASS |
| G2 | closure axiom d̂^(d̂−1) = ĥ^d̂ + 1 | PASS |
| G3 | wrong control at (ĥ, d̂) = (3, 2): zero matches | PASS |
| G4 | wrong control: any bin perturbation breaks identity | PASS |
| G5 | precommit hash verified at runner load | PASS |
| G6 | forbidden-file open() guard not tripped | PASS |

## Closure axiom cross-reads (informational)

```text
The closure axiom d̂^(d̂−1) = ĥ^d̂ + 1  (→ 9 = 8 + 1) picks (ĥ, d̂) = (2, 3)
at primitive selection.  The SAME equation re-appears in the bin
decompositions:

  bound_composite = (R + 1)²                    R + 1 = closure-act shift above R
  promoter_80     = d̂⁴ − 1 = (S+1)² − 1         squared closure axiom minus closure act
  ℒ               = d̂² · Θ                       carrier × closure witness
  M               = (S − 1) · Θ                  matter capacity below the witness
```

## Verdict statement

CR259 PASS. The QP093A catalog enumeration and the CR253 promoter
decomposition are structurally identified as closed-form integer
compositions of (ĥ = 2, d̂ = 3) under the listed substrate identities,
with zero fitted parameters. The chessboard structure (13×13 T13
lattice) is sealed; the matter-antimatter asymmetry as neutral-matter
count is sealed; the matter:antimatter ratio as d̂:ĥ is sealed.

`CR259_PASS_CHESSBOARD_BIN_STRUCTURAL_IDENTIFICATION_TEN_IDENTITIES_VERIFY_QP093A_AND_CR253_DECOMPOSITIONS_AS_PURE_H_D_INTEGER_COMPOSITIONS_AT_2_3_MATTER_ANTI_RATIO_D_OVER_H_ASYMMETRY_EQUALS_NEUTRAL_COUNT_BOUND_COMPOSITE_EQUALS_T13_SQUARED`
