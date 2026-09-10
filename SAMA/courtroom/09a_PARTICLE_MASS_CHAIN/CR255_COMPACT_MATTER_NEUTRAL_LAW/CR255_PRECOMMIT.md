# CR255 — Compact Matter Neutral-Row Law

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** consumes CR253's sealed 80-row promoted matter surface

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does the compact substrate law

```text
qA(p, d) = (p / 8) · R^d

  with    1/8 = Θ / R² = 18 / 144 (tensor share, Section 9.1)
          R = 12
          p ∈ partition
          d ∈ closure depth ∈ {0, 1}
```

reproduce the catalog `qA_source_support` value **exactly** for every
one of the 16 matter neutral rows in CR253's sealed 80-row surface,
with the divisor `1/8` derived from substrate atoms (NOT a free
parameter)?

## Source boundary

```text
input artifact : 09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/
                 CR253_promoted_80_rows.csv
input hash     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
filter         : matter neutral subset
                   bin == 'stable_matter_rows'
                   q_abs == '0'
expected count : 16 matter neutral rows
                   2 neutrino_like (p = 1, q = 0, d ∈ {0, 1})
                   14 neutral_higher_partition (p ∈ {2, 3, 4, 6, 8, 9, 12}, q = 0,
                       d ∈ {0, 1})
```

## The `1/8` divisor is derived, not a free parameter

```text
1/8 = 2^(-D)              where D = 3
1/8 = Θ / R²              where Θ = 18 (carrier-tensor overlap)
                          and R² = 144 (writable capacity)
1/8 = (1 - 7/8)           the tensor share of the 1:7 matter/tensor split
                          per Volume II Section 9.1
```

So the law has **zero free parameters**. The divisor `8` is the binary
split count `2^D` from the dimensional readout, and the resulting
fraction `1/8` is the tensor share of the closed substrate ledger.

## Wrong-control design — sharp structural challenges

Per CR253's filter-subsumption finding (carried into CR254), this CR
uses sharp structural challenges, not rule-relaxation wrong-controls.

**W1 — Wrong divisor from substrate-natural rational pool**.
Replace `1/8` with each of:
`{1/2, 1/3, 1/4, 1/6, 1/9, 1/12, 1/18, 1/24, 1/27, 1/36, 1/81, 1/144}`
(substrate-derivable fractions from R, D, α_H, Θ, F, R²).
Canonical `1/8` not in this pool; count matches for each variant.
Expected: every variant ≤ 8 / 16 (at best half-matches).

**W2 — Wrong dimensional exponent**. Replace `R^d` with each of
`R^(d-1)`, `R^(d+1)`, `R^(2d)`, `(d+1)^d`. Expected: each ≤ 8 / 16.

**W3 — Wrong p dependence**. Replace `p` with each of
`p²`, `√p · √p` (trivially same as p; sanity), `p · D`, `constant p_mean`.
Expected: each ≤ 8 / 16 (canonical p is unique).

**W4 — Continuous random divisor**. Monte Carlo: 1000 draws of random
divisor `δ ∈ Uniform(2, 50)`. Compute `qA_random = (p/δ) · R^d` for
each draw; count rows matching to abs_tol 1e-7. Fraction reaching 16/16.
Expected: 0 / 1000 (canonical sits on a measure-zero substrate-derived
value).

## Verdict tree

```text
PASS:
  (1) all 16 matter neutral rows match canonical law to abs_tol 1e-7
  (2) W1: zero non-canonical divisor pool members achieve 16/16
  (3) W2: every dimensional-exponent variant ≤ 8 / 16
  (4) W3: every p-dependence variant ≤ 8 / 16 (and 'p^2' = canonical
      at p=1 only, so should be 2 / 16 not more)
  (5) W4: continuous random divisor draws reproduce 16/16 in 0/1000

BOUNDARY:
  conditions (2)-(5) each within 2 rows of expectation but (1) PASS

FAIL:
  condition (1) fails: less than 14 / 16 exact matches
```

## What this CR seals

The compact matter-neutral-row law sealed at theorem-grade. The
divisor `1/8` is derived from substrate atoms with zero free
parameters. Downstream consumers (branch-09a particle work,
neutrino-mass derivations) can reference this CR as the sealed
M_native generator for the matter-neutral sector.

## Out of scope

- charged rows (sealed at CR254)
- antimatter rows (no neutral antimatter rows in CR253-promoted set;
  the catalog encodes neutral rows matter-only by Majorana convention)
- h_T = 2 neutral rows (CR253 caps at h_T ≤ 1; the QP110 work at d=2
  is upstream verification)

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR253 promoted 80 rows | `59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b` |
| CR253 input catalog 299 (transitively) | `33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |

Runner SHA-256 sealed in HASHES.txt before execution.
