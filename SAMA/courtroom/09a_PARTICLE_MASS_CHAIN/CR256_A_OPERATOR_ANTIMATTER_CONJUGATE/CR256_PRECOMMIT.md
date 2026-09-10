# CR256 — A-Operator Antimatter Conjugate Transform

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** consumes CR253's sealed 80-row promoted matter surface
**Downstream of:** CR254 (matter charged law) — uses qA_matter as base

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does the **A-operator antimatter conjugate transform**

```text
qA_anti(p, sign, d)  =  qA_matter(p, sign, d)  ·  A_conjugate(sign, p, d)

  A_conjugate(neg, p, d)  =  (5/6) · (1 + p / R^(d+1))
  A_conjugate(pos, p, d)  =  (6/5) · (1 − p / R^(d+1))
```

reproduce the catalog `qA_source_support` for all 32 antimatter
charged rows in CR253's sealed 80-row surface, **including the
single-row hard-zero prediction at p=12, d=0, positive**?

The A-operator is a NON-ROW substrate entity (verified at QP102 +
QP103: a partition-1 A_FIELD_CARRIER row would push L from 162 to
163, breaking ledger closure). It acts as the antimatter conjugate
transform via a depth-dependent route-scale correction at `R^(d+1)`.

## The hard-zero prediction (load-bearing sub-gate)

At `p = R = 12, d = 0, sign = positive`:

```text
A_conjugate(pos, 12, 0)  =  (6/5) · (1 − 12/12)  =  (6/5) · 0  =  0
qA_anti(12, pos, 0)      =  qA_matter(12, pos, 0) · 0  =  0  EXACTLY
```

The catalog row `QP093A-0088` is the structurally-falsifiable test.
If its `qA_source_support` value is anything other than 0, the
A-operator hypothesis fails on a single row. Pre-registered.

## Source boundary

```text
input artifact : 09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/
                 CR253_promoted_80_rows.csv
input hash     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
filter         : antimatter charged subset
                   bin == 'antimatter_conjugate_rows'
                   q_abs != '0'
expected count : 32 antimatter charged rows
                   (28 antiquark_like_charged + 4 anti-lepton charged)
hard-zero row  : QP093A-0088 (p=12, d=0, q_sign=positive)
                   expected qA = 0.0 exactly
matter base    : CR254 compact charged law
                   qA_matter(p, sign, d) = R^d · c_s · p · (1 + p/R²)
                   c_+ = 5/4, c_- = 3/2
```

## Substrate provenance of the A-operator coefficients

The route-scale correction factors are substrate-derived:

```text
(5/6) = (5/4) / (3/2) = c_+ / c_-          (negative side picks up c_+/c_-)
(6/5) = (3/2) / (5/4) = c_- / c_+          (positive side picks up c_-/c_+)
1 ± p/R^(d+1)                              route correction at R^(d+1)
```

The pair `(5/6, 6/5)` are reciprocal; the A-operator factors are the
charge-conjugate ratios of the matter c_s constants. Zero free
parameters beyond the matter law constants sealed at CR254.

## Wrong-control design

Per CR253/CR254 trim: sharp structural challenges, not rule-relaxation.

**W1 — Wrong R^(d+1) exponent**. Replace `R^(d+1)` with each of
`R^d` (depth-independent), `R^(d+2)`, `R^(d-1)` (only well-defined for
d ≥ 1). Count matches across 32 rows. Expected: each ≤ 16/32.

**W2 — Wrong route coefficient pair**. Replace `(5/6, 6/5)` with each
of `(1, 1)` (no conjugation), `(6/5, 5/6)` (swap), `(7/8, 8/7)` (off by
one step in the substrate ratios). Expected: each ≤ 16/32.

**W3 — Wrong sign convention**. Swap `+` and `−` in the route
correction: `(5/6)(1 - p/R^(d+1))` for neg and `(6/5)(1 + p/R^(d+1))`
for pos. Expected: ≤ 16/32 (this kills the hard-zero — pos at p=12
won't be zero).

**W4 — Continuous random `(c_neg_coef, c_pos_coef, R_exp_factor)`**.
1000 draws: `c_neg ∈ Uniform(0.5, 1.5)`, `c_pos ∈ Uniform(0.5, 2.0)`,
exponent factor ∈ {12, 144, 1728} (R, R², R³). Count draws achieving
32/32. Expected: 0 / 1000.

**H — Hard-zero sub-gate**. Row `QP093A-0088`: actual qA must equal 0
to abs_tol 1e-9. Single-row falsifiable prediction. If the catalog
ever updates and this value becomes non-zero, the A-operator
hypothesis fails on this row alone.

## Verdict tree

```text
PASS:
  (1) all 32 antimatter charged rows match canonical law to abs_tol 1e-7
  (2) HARD-ZERO sub-gate: QP093A-0088 qA == 0.0 (abs_tol 1e-9)
  (3) W1: every wrong-exponent variant ≤ 16/32
  (4) W2: every wrong-coefficient-pair variant ≤ 16/32
  (5) W3: sign-swap variant ≤ 16/32 AND hard-zero would be 24/12,
      not 0/12 — sign swap kills the hard-zero
  (6) W4: zero of 1000 random draws reproduce 32/32

BOUNDARY:
  conditions (3)-(6) within 2 rows of expectation but (1) and (2) PASS

FAIL:
  condition (1) fails by >2 rows OR
  condition (2) HARD-ZERO sub-gate fails (single-row falsification)
```

## What this CR seals

The A-field non-row operator hypothesis sealed at theorem-grade
with single-row falsifiable hard-zero prediction. Downstream
consumers:

- branch-09a particle work on antimatter: this CR provides the sealed
  qA_anti generator
- CR257 (A meets Θ at d=1): downstream from this CR; the d=1
  squared-and-difference-of-squares forms are consequences of the
  R^(d+1) lift sealed here

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR253 promoted 80 rows | `59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b` |
| CR254 matter charged law (transitively the base) | (CR254 precommit + runner sealed) |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |

## Out of scope

- matter rows (CR254, CR255)
- A-Θ scale meeting at d=1 (CR257; this CR's R^(d+1) finding is the
  upstream)
- h_T = 2 antimatter rows (CR253 caps at h_T ≤ 1; QP110 has them as
  upstream verification)
- A-field-as-row reasoning (sealed at QP102 + QP103 as ruled out;
  this CR consumes the consequence)
- PDG named-particle assignment
