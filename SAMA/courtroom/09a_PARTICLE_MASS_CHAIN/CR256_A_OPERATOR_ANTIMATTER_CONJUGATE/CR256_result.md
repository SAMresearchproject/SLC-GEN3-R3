# CR256 — A-Operator Antimatter Conjugate Transform — RESULT

```text
verdict           : PASS
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 25654e6e3f1e3863f096e997326eaf3036cd5c9b2cb0436ed83f651c37a0b382
runner_hash       : 6cb9c5f83fe42e2812266e42d0f61442ee489e5de016a9cead658e280d72eac7
input_hash        : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

```text
qA_anti(p, sign, d)  =  qA_matter(p, sign, d)  ·  A_conjugate(sign, p, d)

  A_conjugate(neg, p, d)  =  (5/6) · (1 + p / R^(d+1))
  A_conjugate(pos, p, d)  =  (6/5) · (1 − p / R^(d+1))
```

**32 / 32 antimatter charged rows match catalog to abs_tol 1e-7. Max
residual 5.00e-08.**

**HARD-ZERO sub-gate PASSES**: `QP093A-0088` (p=12, d=0, pos) has
actual `qA = 0.0` exactly. The pre-registered single-row falsifier
holds: the catalog confirms the substrate prediction `(6/5)(1−12/12) = 0`.

The A-field is a **non-row substrate operator** (sealed at QP102 +
QP103) that performs the antimatter conjugate transform via a
depth-dependent route-scale correction at `R^(d+1)`. T13 ledger
closure `L = 162` preserved.

## Verdict conditions

| condition | observed | verdict |
| --- | --- | --- |
| (1) canonical 32/32 exact (abs_tol 1e-7) | 32/32, max residual 5e-8 | PASS |
| (2) **HARD-ZERO sub-gate** at QP093A-0088 | actual qA = 0.0 (abs_tol 1e-9) | **PASS** |
| (3) W1 wrong-exponent variants ≤ 16/32 | max 0/32 | PASS |
| (4) W2 wrong-coefs variants ≤ 16/32 | max 1/32 (hard-zero artifact) | PASS |
| (5) W3 sign-swap ≤ 16/32 AND kills hard-zero | 0/32 + swap gives 39.0 ≠ 0 | PASS |
| (6) W4 continuous random 0/1000 full match | 0/1000, best 1/32 | PASS |

## The hard-zero — sealed prediction confirmed

```text
A_conjugate(pos, p=12, d=0)  =  (6/5) · (1 − 12/12)  =  (6/5) · 0  =  0
prediction:  qA_anti(12, pos, 0) = qA_matter(12, pos, 0) · 0 = 0 exactly
catalog:     QP093A-0088  qA_source_support = 0.0
```

**The catalog row holds the exact zero.** This is the single-row
falsifiable structural prediction the A-operator hypothesis makes
that no alternative formulation (sign-swap, no-conjugation, off-
substrate coefs) can match. If `QP093A-0088`'s qA ever updated to
anything other than 0, the A-operator hypothesis would fail on this
row alone. It doesn't.

## Per-row predictions — 32 / 32 exact

Sample rows:

| row | p | sign | d | actual | predicted |
| --- | ---: | --- | ---: | ---: | ---: |
| QP093A-0073 | 1 | neg | 0 | 1.3635706 | 1.3635706 |
| QP093A-0074 | 1 | pos | 0 | 1.3845486 | 1.3845486 |
| QP093A-0076 | 2 | pos | 0 | 2.5347222 | 2.5347222 |
| ... | | | | | |
| **QP093A-0088** | **12** | **pos** | **0** | **0.0000000** | **0.0000000** ← hard zero |
| QP093A-0090 | 1 | pos | 1 | 17.9991319 | 17.9991319 |
| ... | | | | | |
| QP093A-0104 | 12 | pos | 1 | 214.5000000 | 214.5000000 |

Max residual across 32 rows: **5.00e-08** (numerical noise from
floating-point evaluation of exact rationals).

Full table in `CR256_per_row_predictions.csv`.

## Wrong-control summary

### W1 — Wrong R^(d+1) exponent (0/32 each)

| variant | matches |
| --- | ---: |
| `R^d` (depth-independent) | 0 / 32 |
| `R^(d+2)` | 0 / 32 |
| `R^(d-1)` clamped | 0 / 32 |

The R^(d+1) lift is unique. No simpler depth-coupling produces a
single matching row.

### W2 — Wrong coefficient pair (max 1/32)

| variant | matches |
| --- | ---: |
| `(1, 1)` no conjugation | 1 / 32 |
| `(6/5, 5/6)` swapped | 1 / 32 |
| `(7/8, 8/7)` off-substrate | 1 / 32 |

The 1/32 match in each wrong variant is the **hard-zero row
QP093A-0088 itself** — when the route factor multiplies by 0 (from
the `1 − p/R^(d+1)` term at p=12, d=0), the wrong coefficient
becomes irrelevant. ANY coefficient × 0 = 0. The hard-zero row
matches by structural artifact, not by the wrong coefficient being
correct. Pre-registered tolerance ≤ 16/32 holds with margin.

### W3 — Sign-swap convention (0/32, plus kills the hard-zero)

| metric | result |
| --- | --- |
| sign-swap rows matching catalog | 0 / 32 |
| sign-swap predicts QP093A-0088 as | **39.0** (≠ 0) |

The sign-swap variant (neg uses `1 − p/R^(d+1)`, pos uses
`1 + p/R^(d+1)`) matches zero rows AND specifically kills the
hard-zero — predicting qA = 39.0 for p=12, d=0, pos instead of 0.
The sign convention is load-bearing AND the hard-zero is uniquely
predicted by the canonical sign assignment.

### W4 — Continuous random (c_neg, c_pos, R_exp) draws (0/1000)

1000 draws: `c_neg ∈ Uniform(0.5, 1.5)`, `c_pos ∈ Uniform(0.5, 2.0)`,
`R_exp ∈ {12, 144, 1728}`.

- Draws achieving 32/32: **0 / 1000**
- Best random draw match count: **1 / 32** (the hard-zero row again)

No random parameter combination in the unit box reproduces more than
the hard-zero artifact match. The canonical `(5/6, 6/5, R^(d+1))`
triple sits on a measure-zero set in the continuous null.

## Substrate provenance of the A-operator coefficients

The route-scale coefficients are not free — they are reductions of
the matter c_s constants from CR254:

```text
(5/6)  =  (5/4) / (3/2)  =  c_+ / c_-       (negative side conjugation factor)
(6/5)  =  (3/2) / (5/4)  =  c_- / c_+       (positive side conjugation factor)
```

The A-operator "swaps" the matter c_s constants under conjugation and
applies them as the route factor. Combined with the `R^(d+1)` route
scale, this is zero additional free parameters beyond what CR254
sealed.

## What this CR seals

The A-field non-row operator hypothesis is theorem-grade with a
single-row falsifiable hard-zero prediction. The matter sector
(CR254, CR255) combined with the antimatter sector (CR256) closes
the 80-row stable matter surface from CR253 with **80 / 80 generated
by compact substrate-atom expressions**:

```text
matter charged (32):  qA = R^d · c_s · p · (1 + p/R²)
matter neutral (16):  qA = (p/8) · R^d
anti charged   (32):  qA = qA_matter · (5/6 or 6/5) · (1 ± p/R^(d+1))
```

Zero free parameters across the entire trio. All substrate atoms
`(R, α_H, D, Θ)` sealed independently upstream. The compact-law family
is now CR-class theorem-grade.

## Out of scope

- A-Θ scale meeting at d=1 (CR257; the squared-and-difference-of-
  squares forms at d=1 are downstream consequences of this CR's
  R^(d+1) lift)
- h_T = 2 antimatter rows (CR253 capped at h_T ≤ 1; QP110 has the
  d=2 verification)
- A-field-as-row reasoning (ruled out at QP102 + QP103)
- PDG named-particle assignment

## Verdict statement

**CR256 PASS.** The A-operator antimatter conjugate transform is
theorem-grade. The hard-zero single-row falsifiable prediction at
`QP093A-0088` is confirmed exactly. All structural axes tested
(exponent, coefficient pair, sign convention, continuous null) are
load-bearing.

The A-field as non-row substrate operator is now CR-sealed as the
antimatter conjugation mechanism on stable charged matter rows.

`A_OPERATOR_ANTIMATTER_CONJUGATE_TRANSFORM_PASS_32_32_HARD_ZERO_AT_P12_D0_POS_CONFIRMED_EXACTLY_R_D_PLUS_1_ROUTE_LIFT_LOAD_BEARING`
