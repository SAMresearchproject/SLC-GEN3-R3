# CR257b — A Meets Θ at d=1 — W4 Correction Re-Run

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** CR253 (80-row surface), CR254 (matter charged law),
CR256 (A-operator antimatter transform)
**Supersedes:** CR257 (BOUNDARY) — W4 runner implementation had a
spec/code mismatch on the positive side; structural claim was PASS.

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Why CR257b

CR257 v1 sealed BOUNDARY because the W4 wrong-control runner code branched
on `sign` and applied the power variant to both negative and positive
forms. On the positive side, the "canonical" form `(1 − p²/R⁴)` raised to
power=1 is bit-identical to canonical, so 8 positive rows matched
trivially. That collapsed W4 to 8/16 instead of the precommit-specified
0/8 each.

The CR257 v1 precommit spec already scopes W4 correctly:

> **W4 — Replace squared factor**. For neg side at d=1, replace
> `(1 + p/R²)²` with `(1 + p/R²)¹` (single power) or `(1 + p/R²)³`
> (cubed). Expected: 0 / 8 each.

CR257b runs the same load-bearing test under that exact spec, with
the runner implementation corrected to honor the "**neg side at d=1**"
scope. No structural claim changes. CR257 v1 stays sealed as audit
trail with a SUPERSEDED banner on its result.md.

## Question (verbatim from CR257)

The A-operator route scale (CR256) is `R^(d+1)`.
The matter-surface scale (CR254) is `R²`.
These coincide **only at d=1** (since `R^(d+1) = R²` ⇒ `d = 1`).

**Does the d=1 antimatter law factor through the matter surface
correction in the substrate-natural compact forms below — and do
these forms FAIL to extend to d ≠ 1 — empirically verifying the
A-Θ meeting point as a structural feature of the antimatter
sector?**

```text
Claim at d=1:
  qA_anti(neg, p, 1)  =  R · (5/4) · p · (1 + p/R²)²
  qA_anti(pos, p, 1)  =  R · (3/2) · p · (1 − p²/R⁴)
                      =  R · (3/2) · p · (1 + p/R²)(1 − p/R²)

Derivation (algebraic identity at d=1 only):
  qA_anti(neg, p, d)   =  qA_matter(neg, p, d) · (5/6) · (1 + p/R^(d+1))
                        =  [R^d · (3/2) · p · (1 + p/R²)] · (5/6) · (1 + p/R^(d+1))

  at d=1, R^(d+1) = R²:
                        =  R · (3/2)(5/6) · p · (1 + p/R²) · (1 + p/R²)
                        =  R · (5/4) · p · (1 + p/R²)²        ← compact form

  qA_anti(pos, p, d)   =  qA_matter(pos, p, d) · (6/5) · (1 − p/R^(d+1))
                        =  [R^d · (5/4) · p · (1 + p/R²)] · (6/5) · (1 − p/R^(d+1))

  at d=1, R^(d+1) = R²:
                        =  R · (5/4)(6/5) · p · (1 + p/R²) · (1 − p/R²)
                        =  R · (3/2) · p · (1 − p²/R⁴)        ← compact form
```

The constants `(3/2)(5/6) = 5/4 = c_+` and `(5/4)(6/5) = 3/2 = c_-`
both **swap** the matter `c_s`. The factor `(1 + p/R²)` from the
matter surface correction appears SQUARED for the negative side and
in the difference-of-squares form `(1 − p²/R⁴)` for the positive side.
**Both consequences exist only at d=1** because that's where the
A-operator scale meets the matter-surface scale.

## What the CR tests

1. **Empirical match (E)**: at d=1, both compact forms match the
   catalog `qA_source_support` exactly for all 16 antimatter charged
   rows at d=1 (8 negative + 8 positive).

2. **Algebraic identity (A)**: the d=1 compact forms are
   bit-equivalent under exact rational arithmetic (Fraction class)
   to the CR256 general A-operator forms evaluated at d=1.

3. **Depth uniqueness (D)**: the same compact forms applied at d=0
   do NOT match the catalog's d=0 antimatter rows (the A-Θ meeting
   does NOT occur at d=0).

## Source boundary

```text
input artifact : 09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/
                 CR253_promoted_80_rows.csv
input hash     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
filter         : antimatter charged subset at d = 1
                   bin == 'antimatter_conjugate_rows'
                   q_abs != '0'
                   closure_depth == '1'
expected count : 16 antimatter charged d=1 rows
                   (8 negative + 8 positive across 8 partitions)
secondary set  : antimatter charged at d = 0 (16 rows)
                   used to verify depth-uniqueness wrong-control
```

## Wrong controls (W4 implementation corrected)

**W1 — Depth-uniqueness on negative side**. Apply the compact form
`qA = R · (5/4) · p · (1 + p/R²)²` to the 8 antimatter d=0 negative
rows. Count matches. Expected: 0 / 8 (compact form valid only at d=1).

**W2 — Depth-uniqueness on positive side**. Apply
`qA = R · (3/2) · p · (1 − p²/R⁴)` to 8 d=0 positive antimatter rows.
Expected: 0 / 8.

**W3 — Sign-swap of the compact forms**. Swap: neg gets the
diff-of-squares, pos gets the squared. Apply to d=1 rows. Expected:
≤ 4 / 16 (small accidental at low p).

**W4 — Replace squared factor on neg side**. *Runner corrected:
scope strictly to negative side at d=1.* Replace `(1 + p/R²)²` with
`(1 + p/R²)¹` (single power) or `(1 + p/R²)³` (cubed). Apply to the
8 d=1 negative rows only; the positive form is not modified in W4.
Expected: 0 / 8 each.

**W5 — Algebraic identity check (exact)**. For every d=1 anti row,
compute the d=1 compact form AND the CR256 general A-operator form
using exact Fraction arithmetic. Verify they are bit-equivalent
(not floating-point match — actual Fraction equality). Expected:
16 / 16 identical.

## Verdict tree

```text
PASS:
  (1) E gate: both compact forms match catalog 16/16 (neg 8/8 + pos 8/8)
      at abs_tol 1e-7
  (2) A gate: W5 — algebraic Fraction equality of compact and general
      forms at d=1 for all 16 rows
  (3) D gate: W1 + W2 — neither compact form matches more than 0/8 at d=0
  (4) W3 sign-swap of compact forms ≤ 4/16 at d=1
  (5) W4 power-variants on neg-side squared factor 0/8 each

BOUNDARY:
  conditions (3)-(5) each within 2 rows of expectation but (1)+(2) PASS

FAIL:
  E gate fails (≤ 14/16 catalog match) OR
  A gate fails (compact and general forms not bit-equivalent at d=1)
```

## What this CR seals

Same structural content as CR257 v1 (A-Θ meeting at d=1 is theorem-
grade), now with the W4 wrong-control producing the precommit-
specified 0/8 sensitivity on the negative-side power variants — no
trivial positive-side carry-over.

This is a formality re-run. The verdict is expected PASS; no
structural claim changes.

## Substrate provenance summary

```text
A-operator scale     = R^(d+1)    (from CR256 R^(d+1) route lift)
Θ-derived surface    = R²         (matter law (1 + p/R²) factor)
A meets Θ            at d=1       (R^(d+1) = R² when d = 1)

constants from CR254:
  c_+ = 5/4 = 1 + 1/α_H²
  c_- = 3/2 = 1 + 1/α_H

constants from CR256 (matter ratios):
  (5/6) = c_+ / c_-
  (6/5) = c_- / c_+

product identities at d=1:
  c_- · (5/6) = (3/2)(5/6) = 15/12 = 5/4 = c_+   (neg side, squared)
  c_+ · (6/5) = (5/4)(6/5) = 30/20 = 3/2 = c_-   (pos side, diff of sq)
```

## Out of scope

- h_T = 2 antimatter rows (CR253 caps at h_T ≤ 1; QP110 has them)
- d=0 and d=2 antimatter law content (CR256 covers all depths in the
  general form)
- A-field-as-row reasoning (ruled out at QP102 + QP103)
- PDG named-particle assignment

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR253 promoted 80 rows | `59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b` |
| CR257 v1 precommit (lineage reference) | `75ee3b884a8b4d25bebfa2fa847de75e7edc0d7a2e0264424a610469f6e64afd` |
| CR257 v1 runner (with W4 bug)         | `664ba986e013534e323758f9ec705e086d11ed32060771cbc903c2996391035b` |
| CR257 v1 result (BOUNDARY, SUPERSEDED) | `eea3b57db301562992502c1b8ac76f7176b2f6cb64ac46338c2824e5961eb9b4` |
| CR254 / CR256 (transitively sealed) | per their HASHES.txt |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
