# CR255 — Compact Matter Neutral-Row Law — RESULT

```text
verdict           : PASS
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 567e4683112c245f065205ac98695bc15a03db0b7730782c59c8e6e4c214752a
runner_hash       : 195ffa107016b1b92325793b5560dc5f741c9cc1c842183a3fa30d3bcbad7d20
input_hash        : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

```text
qA(p, d)  =  (p / 8) · R^d

with  1/8 = Θ/R² = 2^(-D)   (tensor share, Section 9.1)
      R = 12, D = 3
```

**Generates the catalog `qA_source_support` value EXACTLY for all 16
matter neutral rows in CR253's sealed 80-row surface. Zero free
parameters. Max residual 0.00 (exact rationals).**

The divisor `1/8` is derived from substrate atoms three ways:

```text
1/8 = 2^(-D)              D = 3 dimensional readout
1/8 = Θ/R²                = 18/144 (tensor share, Section 9.1)
1/8 = R²/Θ inverse        the matter/tensor 7:1 split
```

The law has the same depth lift `R^d` as the matter-charged law
(CR254), with the partition `p` scaled by the substrate tensor share
instead of the charge-sign factor `c_s`.

## Verdict conditions

| condition | observed | verdict |
| --- | --- | --- |
| (1) canonical 16/16 exact | 16 / 16, max residual 0.00 | PASS |
| (2) W1 zero non-canonical divisors achieve 16/16 | 0 of 12 pool members | PASS |
| (3) W2 every dimensional-exponent variant ≤ 8/16 | max 8/16 (R^(2d) at d=0) | PASS |
| (4) W3 every non-sanity p-dependence variant ≤ 8/16 | max 2/16 (p² at p=1) | PASS |
| (5) W4 zero of 1000 continuous random divisor draws reproduce 16/16 | 0 / 1000 | PASS |

## Per-row predictions — 16 / 16 exact

| row | p | d | actual | predicted |
| --- | ---: | ---: | ---: | ---: |
| QP093A-0003 | 1 | 0 | 0.125 | 0.125 |
| QP093A-0006 | 2 | 0 | 0.250 | 0.250 |
| QP093A-0009 | 3 | 0 | 0.375 | 0.375 |
| QP093A-0012 | 4 | 0 | 0.500 | 0.500 |
| QP093A-0015 | 6 | 0 | 0.750 | 0.750 |
| QP093A-0018 | 8 | 0 | 1.000 | 1.000 |
| QP093A-0021 | 9 | 0 | 1.125 | 1.125 |
| QP093A-0024 | 12 | 0 | 1.500 | 1.500 |
| QP093A-0027 | 1 | 1 | 1.500 | 1.500 |
| QP093A-0030 | 2 | 1 | 3.000 | 3.000 |
| QP093A-0033 | 3 | 1 | 4.500 | 4.500 |
| QP093A-0036 | 4 | 1 | 6.000 | 6.000 |
| QP093A-0039 | 6 | 1 | 9.000 | 9.000 |
| QP093A-0042 | 8 | 1 | 12.000 | 12.000 |
| QP093A-0045 | 9 | 1 | 13.500 | 13.500 |
| QP093A-0048 | 12 | 1 | 18.000 | 18.000 |

All 16 are exact rationals. The catalog and the law agree to literal
bit-equality, not even floating-point tolerance.

## Wrong control summary

### W1 — Substrate-derivable wrong-divisor pool

Pool: `{2, 3, 4, 6, 9, 12, 18, 24, 27, 36, 81, 144}` (canonical 8 NOT
in pool). Each draws from named substrate atoms (R, D powers, Θ, F,
R², bigrade values).

**Zero of 12 wrong divisors achieve 16/16.** Top by match count: all
0/16 (the wrong divisors produce predictions that don't match ANY
catalog value). Sensitivity is total — the divisor `1/8` is unique
even among substrate-derivable alternatives.

### W2 — Dimensional exponent variants

| variant | matches |
| --- | ---: |
| `R^(d-1)` | 0 / 16 |
| `R^(d+1)` | 0 / 16 |
| `R^(2d)` | 8 / 16 (matches d=0 rows where R^0 = R^(2·0) = 1) |
| `(d+1)^d` | 8 / 16 (matches d=0 rows where (1)^0 = 1 = R^0) |

`R^d` is unique. The 8/16 hits are exactly the d=0 rows where ANY
exponent variant that evaluates to 1 at d=0 will match by coincidence.

### W3 — p-dependence variants

| variant | matches | note |
| --- | ---: | --- |
| `p²` | 2 / 16 | matches p=1 trivially (1² = 1 = p) |
| `p · D` | 0 / 16 | |
| `constant p_mean = 45/8` | 0 / 16 | |
| `√p · √p` | 16 / 16 | (sanity check — trivially equals p; exempt from gate) |

Linear `p` is unique. The p² hits at p=1 are arithmetic coincidence.

### W4 — Continuous random divisor

1000 draws from `Uniform(2, 50)`:

- Draws achieving 16/16 exact match: **0 / 1000**
- **Best random draw match count: 0 / 16**

No random divisor in `(2, 50)` reproduces even a single row's qA value
to numerical precision. The canonical divisor `8` sits on a
measure-zero set in the continuous null.

## Provenance and substrate derivation of 1/8

The `1/8` divisor is over-determined by substrate atoms:

```text
1/8  =  2^(-D)        (D = 3 from Section 4.1 dimensional readout)
1/8  =  Θ / R²        (Section 9.1 tensor share; Θ = 18, R² = 144)
1/8  =  1 - 7/8       (matter/tensor split, with 7/8 = M/R² retained)
```

All three reductions appear in the manuscript. The law's only
content beyond substrate atoms is the multiplicative composition
`p · (1/8) · R^d` — and that composition is what CR255 tests.

## What this CR seals

The compact matter-neutral-row law is theorem-grade sealed.
Combined with CR254 (matter charged law), the matter sector at
h_T ∈ {0, 1} is now fully described by two compact substrate-atom
laws:

```text
matter charged (32 rows):  qA = R^d · c_s · p · (1 + p/R²)
                                where c_+ = 5/4, c_- = 3/2
matter neutral (16 rows):  qA = (p/8) · R^d
                                where 1/8 = Θ/R²
```

48 / 48 matter rows generated. Zero free parameters across both laws.

The antimatter charged sector (32 rows) is the next CR (CR256: the
A-operator antimatter conjugate transform).

## Out of scope

- antimatter rows (CR256)
- charged rows (sealed at CR254)
- h_T = 2 neutral rows (CR253 caps at h_T ≤ 1; QP110 has the d=2
  verification as upstream)

## Verdict statement

**CR255 PASS.** The compact matter-neutral-row law is theorem-grade.
The divisor `1/8` is substrate-derived three ways. All 16 catalog
values agree to bit-equality. Every structural axis tested
(divisor pool, dimensional exponent, p-dependence, continuous null)
is load-bearing.

`MATTER_NEUTRAL_LAW_qA_EQ_P_OVER_8_TIMES_R_TO_D_PASS_16_16_EXACT_RATIONALS_1_OVER_8_DERIVED_AS_TENSOR_SHARE_THETA_OVER_R_SQUARED`
