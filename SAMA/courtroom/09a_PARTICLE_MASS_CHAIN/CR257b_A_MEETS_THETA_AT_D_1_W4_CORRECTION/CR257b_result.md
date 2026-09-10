# CR257b — A Meets Θ at d=1 — W4 Correction Re-Run — RESULT

```text
verdict           : PASS
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 3a3b301d45d4573845f6744f315ff4ef6278e9ece0ccf314724f109ee41c9fe7
runner_hash       : 73b7553b95c193efa1bb968b9ebf2b69d03737ffec2f7d4e2643614e72d4d7bc
input_hash        : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
supersedes        : CR257_A_MEETS_THETA_AT_D_1 (BOUNDARY — W4 runner bug)
```

## Headline

The **A-Θ meeting at d=1 is sealed PASS** with all five precommit
conditions satisfied:

| claim | result |
| --- | --- |
| **E gate** (empirical): d=1 compact forms match catalog 16/16 | **PASS** (max residual 5e-8) |
| **A gate** (algebraic): compact forms bit-equivalent to CR256 general form at d=1 | **PASS** (Fraction-equality 16/16) |
| **D gate** (depth-uniqueness): compact forms FAIL at d=0 | **PASS** (0/8 each sign) |
| **W3** sign-swap of compact forms | **PASS** (0/16) |
| **W4** power variants on the neg-side squared factor (scope-corrected) | **PASS** (0/8 each at power=1 and power=3) |

CR257 v1 sealed BOUNDARY on the same structural content because of a
self-inflicted W4 scope bug. CR257b runs the identical E/A/D/W3 logic
(bit-identical outputs on those gates) plus the corrected W4 that
honors the precommit's "**neg side at d=1**" scope. Verdict: PASS.

## E gate — empirical match at d=1 (16/16 exact)

```text
qA_anti(neg, p, 1) = R · (5/4) · p · (1 + p/R²)²       ← matter surface SQUARED
qA_anti(pos, p, 1) = R · (3/2) · p · (1 − p²/R⁴)        ← DIFFERENCE OF SQUARES
                   = R · (3/2) · p · (1 + p/R²)(1 − p/R²)
```

All 16 anti charged d=1 rows match the compact forms to within
abs_tol = 1e-7 (max observed residual: 5.0e-8, numerical noise).

| row | p | sign | actual | compact form |
| --- | ---: | --- | ---: | ---: |
| QP093A-0089 | 1 | neg | 15.2090567 | 15.2090567 |
| QP093A-0090 | 1 | pos | 17.9991319 | 17.9991319 |
| QP093A-0091 | 2 | neg | 30.8391204 | 30.8391204 |
| QP093A-0092 | 2 | pos | 35.9930556 | 35.9930556 |
| QP093A-0093 | 3 | neg | 46.8945312 | 46.8945312 |
| QP093A-0094 | 3 | pos | 53.9765625 | 53.9765625 |
| QP093A-0095 | 4 | neg | 63.3796296 | 63.3796296 |
| QP093A-0096 | 4 | pos | 71.9444444 | 71.9444444 |
| QP093A-0097 | 6 | neg | 97.6562500 | 97.6562500 |
| QP093A-0098 | 6 | pos | 107.8125000 | 107.8125000 |
| QP093A-0099 | 8 | neg | 133.7037037 | 133.7037037 |
| QP093A-0100 | 8 | pos | 143.5555556 | 143.5555556 |
| QP093A-0101 | 9 | neg | 152.4023438 | 152.4023438 |
| QP093A-0102 | 9 | pos | 161.3671875 | 161.3671875 |
| QP093A-0103 | 12 | neg | 211.2500000 | 211.2500000 |
| QP093A-0104 | 12 | pos | 214.5000000 | 214.5000000 |

## A gate — algebraic Fraction equality (16/16 exact)

For each of the 16 d=1 anti rows, both the compact form and the
CR256 general A-operator form were computed as Python `Fraction`
objects (exact rationals) and tested for bit-equality:

```python
anti_general(p, sign, 1)   ==   anti_d1_compact(p, sign, 1)
```

**Result: 16/16 bit-equivalent Fraction pairs.** Substrate-natural
reduction verified at exact rational arithmetic, not just numerical
match.

```text
(general at d=1)  qA_anti(neg, p, 1) = R · c_- · p · (1 + p/R²) · (5/6)(1 + p/R²)
                                      = R · (3/2)(5/6) · p · (1 + p/R²)²
                                      = R · (5/4) · p · (1 + p/R²)²
                                      = (compact form at d=1)

(general at d=1)  qA_anti(pos, p, 1) = R · c_+ · p · (1 + p/R²) · (6/5)(1 − p/R²)
                                      = R · (5/4)(6/5) · p · (1 + p/R²)(1 − p/R²)
                                      = R · (3/2) · p · (1 − p²/R⁴)
                                      = (compact form at d=1)
```

The c_s constants swap under A-conjugation; the matter surface factor
appears a second time from the A-operator route correction (which
lives at R² = R^(d+1) at d=1).

## D gate — depth uniqueness PASS

```text
compact(neg) applied to d=0 negative rows: 0/8
compact(pos) applied to d=0 positive rows: 0/8
```

The d=1 compact forms produce zero catalog matches when applied to
d=0 antimatter rows. The A-Θ meeting **does not occur at d=0** — the
A-correction at d=0 lives at R = 12, not at R² = 144, so the
substrate scales don't align. The compact forms only emerge at d=1.

## W3 — sign-swap kills it (0/16)

Swapping which compact form goes with which sign (neg gets diff-of-
squares, pos gets squared) matches zero catalog rows. Sign-assignment
of squared vs diff-of-squares is load-bearing.

## W4 — power variants on the squared factor (corrected scope: neg only)

```text
scope: 8 negative d=1 rows
power=1: 0/8  (linear instead of squared — kills the match)
power=3: 0/8  (cubed instead of squared — kills the match)
```

The squared exponent on `(1 + p/R²)` is load-bearing on the negative
side. No nearby power reproduces the catalog values.

**Implementation note vs CR257 v1:** the v1 runner applied the power
variant to both sign branches, but its positive branch used
`(1 - p²/R⁴)^power` — and the canonical positive form is itself
`(1 - p²/R⁴)^1`, so power=1 returned the canonical value and matched
all 8 positive rows trivially. That produced a 8/16 W4 hit that
flipped the verdict to BOUNDARY. CR257b scopes W4 strictly to the
negative side (per the precommit text "For neg side at d=1") via
`anti_d1_neg_power_variant` returning `None` for positive rows, which
the counter excludes from the denominator.

## Substrate provenance summary

```text
A-operator scale         = R^(d+1)
matter surface scale     = R²
A meets Θ                at d = 1 (where R^(d+1) = R²)

constants at d=1:
  c_- · (5/6) = (3/2)(5/6) = 5/4 = c_+   (neg side, squared)
  c_+ · (6/5) = (5/4)(6/5) = 3/2 = c_-   (pos side, diff of sq)

The c_s constants swap under conjugation, and the matter surface
correction (1+p/R²) appears a second time at d=1 from the A-operator
route correction.

Zero new free parameters beyond CR254 (matter c_s) and CR256 (A-op
ratios).
```

## What this CR seals

1. The d=1 antimatter law factors through the matter surface
   correction in the substrate-natural compact forms
   `R·(5/4)·p·(1+p/R²)²` and `R·(3/2)·p·(1−p²/R⁴)`.
2. These compact forms are algebraically bit-equivalent (via exact
   Fraction arithmetic) to the CR256 general A-operator form
   evaluated at d=1.
3. They **do not extend** to d=0 — the A-Θ meeting is a depth-d=1
   phenomenon.
4. The squared exponent on `(1 + p/R²)` on the negative side is
   load-bearing; nearby powers (1, 3) produce zero matches.
5. The sign-assignment of squared vs diff-of-squares is load-bearing
   (W3 0/16).

## What CR257 v1 (BOUNDARY) and CR257b (PASS) together mean

CR257 v1 demonstrated the structural finding is robust to a buggy
wrong-control — the structural gates (E, A, D, W3) sealed clean on
their own. CR257b confirms that with W4 correctly scoped per the
precommit text, the verdict tree returns PASS as designed. Both CRs
stay sealed; their cross-reference is the audit trail.

## Provenance hash chain

```text
input        : CR253_promoted_80_rows.csv
               hash 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
v1 (BOUNDARY): CR257_A_MEETS_THETA_AT_D_1
               precommit 75ee3b884a8b4d25bebfa2fa847de75e7edc0d7a2e0264424a610469f6e64afd
               runner    664ba986e013534e323758f9ec705e086d11ed32060771cbc903c2996391035b
               result    eea3b57db301562992502c1b8ac76f7176b2f6cb64ac46338c2824e5961eb9b4
upstream     : CR254 (matter charged law), CR256 (A-operator)
substrate    : R = 12, α_H = 2, Θ = 18 (manuscript Section 4)
constants    : c_+ = 5/4, c_- = 3/2 (CR254 derivations)
               (5/6, 6/5) = c_+/c_- ratios (CR256 derivations)
A-meets-Θ    : at d=1, R^(d+1) = R²
forms        : (5/4)·R·p·(1+p/R²)² for neg, (3/2)·R·p·(1−p²/R⁴) for pos
stewardship  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR257b PASS.** The A-Θ meeting at d=1 is sealed as a structural
feature of the antimatter sector under the precommit's full verdict
tree (E + A + D + W3 + W4 all clean). Re-run formality completed; the
W4 wrong-control implementation is now consistent with its precommit
specification.

`A_MEETS_THETA_AT_D_1_E_GATE_16_16_A_GATE_FRACTION_EQUALITY_16_16_D_GATE_DEPTH_UNIQUE_W3_SIGN_SWAP_0_16_W4_NEG_POWER_VARIANTS_0_8_EACH_PASS`
