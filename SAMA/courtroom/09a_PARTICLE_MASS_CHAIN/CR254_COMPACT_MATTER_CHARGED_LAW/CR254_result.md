# CR254 — Compact Matter Charged-Row Law — RESULT

```text
verdict           : PASS
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 23b94d10bba93c4622b03dead10b8bfb4759649bf1056d5ae489734d3f679c2f
runner_hash       : 391ee6ec1372ad3fdb8ea7ce7cc1eae1bb9a2c9d15bffe4e5702a842718e6b5b
input_hash        : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

```text
qA(p, sign, d)  =  R^d · c_s · p · (1 + p / R²)

c_+ = 1 + 1/α_H² = 5/4
c_- = 1 + 1/α_H  = 3/2
```

**Generates the catalog `qA_source_support` value EXACTLY for all 32
matter charged rows in CR253's sealed 80-row surface. Zero free
parameters. Max residual 3.33e-08.**

All four substrate atoms in the formula `(R = 12, α_H = 2, p ∈ bigrade,
d ∈ {0, 1})` are sealed independently upstream. The two constants
`c_+, c_-` reduce to pure α_H expressions. The law uses no calibration
constants and no fits.

## Verdict conditions

| condition | observed | verdict |
| --- | --- | --- |
| (1) canonical 32/32 exact (abs_tol 1e-7) | 32 / 32 | PASS |
| (2) W1 only canonical (5/4, 3/2) achieves 32/32 from 7×7 rational pool | 1 of 49 = only canonical | PASS |
| (3) W2 every dimensional-exponent variant ≤ 16/32 | max 16/32 | PASS |
| (4) W3 every surface-scale variant ≤ 16/32 | max 4/32 | PASS |
| (5) W4 every functional-form variant ≤ 4/32 | max 4/32 | PASS |
| (6) W5 zero of 1000 random `(c_+, c_-)` draws reproduce 32/32 | 0 / 1000 | PASS |

## Per-row predictions — 32 / 32 exact

| p | sign | d | actual | predicted | match |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | pos | 0 | 1.2586806 | 1.2586806 | OK |
| 1 | neg | 0 | 1.5104167 | 1.5104167 | OK |
| 2 | pos | 0 | 2.5347222 | 2.5347222 | OK |
| ... | ... | ... | ... | ... | ... |
| 12 | pos | 1 | 195.0000000 | 195.0000000 | OK |
| 12 | neg | 1 | 234.0000000 | 234.0000000 | OK |

Full table in `CR254_per_row_predictions.csv`. Max residual across 32
rows: **3.33e-08** (numerical-precision noise; well inside 1e-7).

## Wrong control summary

### W1 — Rational-pool `(c_+, c_-)` sweep (49 pairs)

Pool: `{1, 5/4, 4/3, 3/2, 5/3, 7/4, 2}`. The canonical pair `(5/4, 3/2)`
sits inside this pool. Result:

- Pairs achieving 32/32: **exactly 1 — the canonical (5/4, 3/2)**.
- Top 3 non-canonical pairs by match count:
  - `(1, 3/2)`: 16 / 32 (matches negatives only)
  - `(5/4, 1)`: 16 / 32 (matches positives only)
  - `(5/4, 5/4)`: 16 / 32 (matches positives only)

The pair structure is fully load-bearing. Swapping either constant
to any neighboring substrate-natural rational loses 16 rows.

### W2 — Dimensional exponent variants

| variant | matches |
| --- | ---: |
| `R^(d-1)` | 0 / 32 |
| `R^(d+1)` | 0 / 32 |
| `(d+1)^d` | 16 / 32 (matches d=0 rows where (1)^0 = 1 = R^0) |

`R^d` is the unique exponent that produces 32 / 32.

### W3 — Surface scale variants

| variant | matches |
| --- | ---: |
| `(1 + p/R)` | 0 / 32 |
| `(1 + p/R³)` | 0 / 32 |
| `(1 + p²/R²)` | 4 / 32 (accidental hits at low p) |
| `(1 − p/R²)` | 0 / 32 |

The surface correction `(1 + p/R²)` is unique.

### W4 — Functional form variants

| variant | matches |
| --- | ---: |
| `R^d + c_s · p · (1 + p/R²)` (additive) | 0 / 32 |
| `R^d · c_s · (1 + p/R²)` (no p factor) | 4 / 32 |

The multiplicative form `R^d · c_s · p · (1 + p/R²)` is unique.

### W5 — Continuous random `(c_+, c_-)` from `[1, 2]²`

1000 random draws from uniform on `[1.0, 2.0] × [1.0, 2.0]`.

- Draws achieving 32 / 32 exact match: **0 / 1000**
- **Best random draw match count: 0 / 32**

The canonical pair `(5/4, 3/2)` sits on a measure-zero set in the
continuous null. No random `(c_+, c_-)` pair in the unit square
reproduces even a single row's qA value to numerical precision.

## Notes on the wrong-control design

Per CR253's finding (filter subsumption under bin + h_T), this CR
trimmed the rule-relaxation wrong-controls and replaced them with
sharp structural challenges. The 5 wrong-controls here each test a
specific axis of the structural claim:

1. **Constants** (W1): rational-pool sweep, then continuum sweep (W5)
2. **Dimensional structure** (W2): R^d exponent
3. **Surface correction structure** (W3): functional form of the
   correction factor
4. **Overall composition** (W4): multiplicative vs additive,
   p-dependence

All 5 surface as load-bearing. The law is over-determined: no single
component can be perturbed without breaking the row count.

## What this CR seals

The compact matter-charged-row law is sealed at PASS-grade with:

- 32 / 32 exact matches on the CR253 promoted matter charged surface
- All structural wrong-controls confirming sensitivity
- Zero free parameters

Downstream consumers (CR256 A-operator antimatter transform, branch-09a
particle-mass derivations) can reference this CR as the sealed M_native
generator for the matter-charged sector.

## Provenance

```text
input        : CR253_promoted_80_rows.csv
                  hash 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
filter       : bin == 'stable_matter_rows' AND q_abs != '0'
filtered N   : 32
substrate    : R = 12 (radix), α_H = 2 (binary readout)
               from Section 4.2 / 4.3 of the manuscript
constants    : c_+ = 1 + 1/α_H² = 5/4, c_- = 1 + 1/α_H = 3/2
               (zero free parameters; reductions of α_H = 2)
formula      : qA = R^d · c_s · p · (1 + p/R²)
               (1 + p/R²) surface correction tied to Θ/R² = 1/8
               (tensor share, Section 9.1)
stewardship  : SAM Foundation declaration sealed 2026-06-25
                  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR254 PASS.** The compact charged law is theorem-grade for the
matter sector at h_T ∈ {0, 1}. The law's substrate-specificity is
load-bearing on every structural axis tested (constants, exponent,
surface, composition). The catalog and the law agree to numerical
precision across 32 / 32 rows with zero free parameters.

`MATTER_CHARGED_LAW_qA_EQ_R_TO_D_TIMES_C_S_TIMES_P_TIMES_1_PLUS_P_OVER_R_SQUARED_PASS_32_32_W1_THROUGH_W5_ALL_LOAD_BEARING`
