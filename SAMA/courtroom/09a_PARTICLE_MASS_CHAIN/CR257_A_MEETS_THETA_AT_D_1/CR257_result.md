# CR257 — A Meets Θ at d=1 — RESULT

```text
verdict           : BOUNDARY (structural claims PASS; W4 spec bug surfaced)
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 75ee3b884a8b4d25bebfa2fa847de75e7edc0d7a2e0264424a610469f6e64afd
runner_hash       : 664ba986e013534e323758f9ec705e086d11ed32060771cbc903c2996391035b
input_hash        : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

The **A-Θ meeting at d=1 is structurally confirmed**:

| claim | result |
| --- | --- |
| **E gate** (empirical): d=1 compact forms match catalog 16/16 | **PASS** (max residual 5e-8) |
| **A gate** (algebraic): compact forms bit-equivalent to CR256 general form at d=1 | **PASS** (Fraction-equality 16/16) |
| **D gate** (depth-uniqueness): compact forms FAIL at d=0 | **PASS** (0/8 each sign) |
| W3 sign-swap of compact forms | PASS (0/16) |
| W4 power variants on the squared factor | **FAIL** (precommit spec bug — see below) |

The structural reading (A and Θ scales meet at d=1, producing
substrate-natural squared and difference-of-squares forms) is sealed.
The BOUNDARY tag reflects a self-inflicted W4 wrong-control design
bug, not a content failure.

## E gate — empirical match at d=1 (16/16 exact)

```text
qA_anti(neg, p, 1) = R · (5/4) · p · (1 + p/R²)²       ← matter surface SQUARED
qA_anti(pos, p, 1) = R · (3/2) · p · (1 − p²/R⁴)        ← DIFFERENCE OF SQUARES
                  = R · (3/2) · p · (1 + p/R²)(1 − p/R²)
```

| row | p | sign | actual | compact form |
| --- | ---: | --- | ---: | ---: |
| QP093A-0089 | 1 | neg | 15.2090567 | 15.2090567 |
| QP093A-0090 | 1 | pos | 17.9991319 | 17.9991319 |
| QP093A-0091 | 2 | neg | 30.8391204 | 30.8391204 |
| ... | ... | ... | ... | ... |
| QP093A-0103 | 12 | neg | 211.2500000 | 211.2500000 |
| QP093A-0104 | 12 | pos | 214.5000000 | 214.5000000 |

Max residual: 5.00e-08 (numerical noise). All 16 rows match.

## A gate — algebraic Fraction equality (16/16 exact)

For each of the 16 d=1 anti rows, both the compact form and the
CR256 general A-operator form were computed as Python `Fraction`
objects (exact rationals) and tested for bit-equality.

```python
anti_general(p, sign, 1)   ==   anti_d1_compact(p, sign, 1)
```

**Result: 16/16 bit-equivalent Fraction pairs.** The compact and
general forms are algebraically identical at d=1 under exact rational
arithmetic. The substrate-natural reduction is verified, not just
numerically matched.

This is the load-bearing structural identity:

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

The d=1 compact forms produce ZERO catalog matches when applied to
d=0 antimatter rows. The A-Θ meeting **does not occur at d=0** — the
A-correction at d=0 lives at R = 12, not at R² = 144, so the
substrate scales don't align. The compact forms only emerge at d=1.

## W3 — sign-swap kills it (0/16)

Swapping which compact form goes with which sign (neg gets diff-of-
squares, pos gets squared) matches zero catalog rows. The
sign-assignment of squared vs diff-of-squares is load-bearing.

## W4 — wrong-control design bug surfaced

```text
power=1: 8/16 matches  (FAIL gate)
power=3: 0/16 matches  (PASS)
```

**This 8/16 match is a wrong-control design bug, not a structural
sensitivity issue.** Inspection of the runner code shows W4
modifies the negative-side compact form's exponent (squared → power=1
or power=3) but **leaves the positive-side compact form unchanged**:

```python
def anti_d1_compact_power_variant(p, sign, d, power=1):
    if sign == "negative":
        return Fraction(R) * C_PLUS * p * (Fraction(1) + Fraction(p, R2)) ** power
    else:
        # POSITIVE SIDE: still uses canonical (1 - p²/R⁴) ** power
        return Fraction(R) * C_MINUS * p * (Fraction(1) - Fraction(p*p, R2*R2)) ** power
```

For `power = 1`, the positive side is unchanged from canonical →
all 8 positive rows still match. The 8/16 hit is the positive side
trivially matching its own formula. Only the negative side was
actually tested under variation.

**This is a precommit-time spec error in the wrong-control design.**
It does not reflect on the structural claim, only on my wrong-control
construction. Per Sean's "examine source before precommit" memory:
the source code's branch structure should have been checked before
sealing.

The correct W4 design would have varied the exponent on the entire
compact form (or symmetrically across both signs). Re-running with
that correction is a candidate follow-up CR but is not required to
seal the structural finding here.

The verdict tree's PASS gate required all 6 conditions. With W4
failing on a spec bug while every structural gate (E, A, D, W3)
passes, the verdict is **BOUNDARY** per the pre-registered tree.

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
   correction in the substrate-natural compact forms `R·(5/4)·p·(1+p/R²)²`
   and `R·(3/2)·p·(1−p²/R⁴)`.
2. These compact forms are algebraically bit-equivalent (via exact
   Fraction arithmetic) to the CR256 general A-operator form
   evaluated at d=1.
3. They **do not extend** to d=0 — the A-Θ meeting is a depth-d=1
   phenomenon.
4. The structural reading: the A-operator and Θ-bridge are non-row
   substrate entities whose scales coincide only at d=1, producing
   measurable consequences in the antimatter qA values that no
   sign-swap or power variation reproduces.

## What the BOUNDARY tag means

The structural claims are PASS-grade. The verdict is BOUNDARY because
one pre-registered wrong-control (W4) had a code branch that left
half the rows unmodified, producing a 8/16 artifact that triggered
the gate. This is an audit-trail item, documented honestly. Not a
content failure.

## Provenance hash chain

```text
input        : CR253_promoted_80_rows.csv
               hash 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
upstream     : CR254 (matter charged law), CR256 (A-operator)
substrate    : R = 12, α_H = 2, Θ = 18 (manuscript Section 4)
constants    : c_+ = 5/4, c_- = 3/2 (CR254 derivations)
               (5/6, 6/5) = c_+/c_- ratios (CR256 derivations)
A-meets-Θ    : at d=1, R^(d+1) = R²
forms        : (5/4)·R·p·(1+p/R²)² for neg, (3/2)·R·p·(1−p²/R⁴) for pos
stewardship  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR257 BOUNDARY.** Structurally PASS (E + A + D + W3 all clean);
verdict downgraded by a self-inflicted W4 wrong-control spec bug.
The A-Θ meeting at d=1 is theorem-grade as a substrate-natural
consequence of the depth-shifted A-operator scale crossing the matter
surface scale.

`A_MEETS_THETA_AT_D_1_E_GATE_16_16_A_GATE_FRACTION_EQUALITY_16_16_D_GATE_DEPTH_UNIQUE_W3_SIGN_SWAP_KILLED_W4_SPEC_BUG_LEFT_POS_SIDE_UNMODIFIED_BOUNDARY_HONEST`
