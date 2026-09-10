# CR254 — Compact Matter Charged-Row Law

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** consumes CR253's sealed 80-row promoted matter surface

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does the compact substrate law

```text
qA(p, sign, d) = R^d · c_s · p · (1 + p/R²)

with    c_+ = 1 + 1/α_H² = 5/4
        c_- = 1 + 1/α_H  = 3/2
        substrate atoms R = 12, α_H = 2
        and q = p (diagonal enforced on the catalog)
```

reproduce the catalog `qA_source_support` value **exactly** for every
one of the 32 matter charged rows in CR253's sealed 80-row surface,
**with zero free parameters**?

## Source boundary

```text
input artifact : 09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/
                 CR253_promoted_80_rows.csv
input hash     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
filter         : matter charged subset
                   bin == 'stable_matter_rows'
                   q_abs != '0'
                 (no re-derivation; we consume the sealed promoted surface)
expected count : 32 matter charged rows
                   16 quark-like × 2 signs (per CR253 quark_like_charged class
                     for matter side: 28 rows; wait — see correction below)
```

**Correction**: CR253 class breakdown showed 28 quark-like matter +
4 charged-lepton matter = 32 matter charged total. The 28 quark-like
matter cover p ∈ {2,3,4,6,8,9,12} × 2 signs × 2 depths = 28 rows; the
4 charged-lepton matter cover p=1 × 2 signs × 2 depths = 4 rows.
Total 32 matter charged. Same arithmetic; corrected for clarity.

## Wrong-control design — why structural challenges, not rule relaxations

**Documented finding from CR253**: the q-bigrade and `I_T = 0`
conditions are redundant given the `bin + h_T` filter. Rule-relaxation
wrong-controls of the form "drop filter X" returned the same 80 rows
as canonical, surfacing filter subsumption rather than independent
sensitivity.

**Reasoning for CR254 wrong-control redesign**: the law's
substrate-specificity is the actual claim, not the row set. We test
whether the SPECIFIC substrate atoms `(R, α_H, p)` and the SPECIFIC
functional form `R^d · c_s · p · (1 + p/R²)` are load-bearing — not
whether filter relaxations admit extra rows. The four challenges below
each test a structural axis of the claim.

## Wrong controls (4 structural challenges + 1 statistical)

**W1 — Wrong c_s constants**. Replace canonical `(c_+ = 5/4, c_- = 3/2)`
with all pairs drawn from the substrate-natural rational pool
`P = {1, 5/4, 4/3, 3/2, 5/3, 7/4, 2}`. Count, per pair, how many of 32
rows match. Canonical pair sits within P; expected to match 32/32.
All other 48 pairs should produce strictly lower match counts.

**W2 — Wrong dimensional exponent**. Replace `R^d` with each of
`R^(d-1)`, `R^(d+1)`, `(d+1)^d`. Count matches across 32 rows.
Expected: each ≤ 16/32 (depth-0 rows trivially match under R^(d-1)
since R^(-1) doesn't change at d=0... wait R^0 = 1 always, so R^(d-1)
at d=0 gives R^(-1) = 1/12 which DOES change the prediction. Expected
all variants ≤ ~16/32).

**W3 — Wrong surface scale**. Replace `(1 + p/R²)` with each of
`(1 + p/R)`, `(1 + p/R³)`, `(1 + p²/R²)`, `(1 − p/R²)`. Count matches
across 32 rows. Expected: each variant ≤ some non-canonical fraction.

**W4 — Wrong functional form**. Replace the multiplicative law with
an additive analog: `qA_additive = R^d + c_s · p · (1 + p/R²)`. Also
test no-p law: `qA_no_p = R^d · c_s · (1 + p/R²)`. Count matches.
Expected: 0 / 32 or trivially low.

**W5 — Continuous c_s null distribution**. Monte Carlo: draw 1000
random (c_+_rand, c_-_rand) pairs from uniform on `[1.0, 2.0] × [1.0, 2.0]`.
For each, compute predictions and count how many of 32 rows match within
1e-6 absolute tolerance. Report the fraction of random draws that achieve
match count ≥ 32. Expected: 0 / 1000 (canonical pair lives on a
measure-zero set in the continuous null).

## Verdict tree

```text
PASS:
  (1) all 32 matter charged rows match canonical law to abs_tol 1e-7
  (2) W1: no non-canonical (c_+, c_-) pair from the 7×7 rational pool
      matches all 32 rows
  (3) W2: every dimensional-exponent variant matches ≤ 16/32 rows
  (4) W3: every surface-scale variant matches ≤ 16/32 rows
  (5) W4: no functional-form variant matches > 4/32 rows
  (6) W5: continuous random (c_+, c_-) draws reproduce 32/32 in 0/1000

BOUNDARY:
  conditions (2)-(6) each within 2 rows of expectation but (1) PASS

FAIL:
  condition (1) fails: less than 30/32 exact matches
```

## What this CR seals

A theorem-grade match between the catalog's matter charged qA values
and a compact 4-symbol substrate-atom expression. Zero free
parameters. The compact law is then sealed for downstream consumption
by:

- CR256 (A-operator antimatter transform): the antimatter law uses
  the matter law as its base; this CR seals the base.
- Branch-09a particle-mass derivations: the connection-fee chain
  (CR009@18) is the surface-mass step; this CR seals the M_native
  step upstream of it for the matter-charged sector.

## Out of scope

- antimatter rows (CR256 will handle via A-operator transform)
- neutral matter rows (CR255 will handle via `qA = (p/8) · R^d`)
- catalog re-derivation (already sealed at CR253)
- PDG-named particle assignment (downstream)

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR253 promoted 80 rows | `59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b` |
| CR253 input catalog 299 (transitively) | `33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |

The runner SHA-256 will be sealed in HASHES.txt before execution.
