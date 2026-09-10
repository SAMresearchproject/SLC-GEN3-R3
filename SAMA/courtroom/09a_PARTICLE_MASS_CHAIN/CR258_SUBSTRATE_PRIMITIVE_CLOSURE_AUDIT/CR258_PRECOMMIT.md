# CR258 — Substrate Primitive Closure Audit

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** CR253-CR257 matter-sector closure campaign + Volume I §4
substrate spine + Volume II.1 §11A-§11D compact laws
**Reference:** `docs/SAM_UNIFICATION_NOTE_2026_06_28.md`

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does **every numerical quantity** appearing in any sealed SAM artifact
across Volume I §4 (substrate atoms) and CR253-CR257 (matter sector
compact laws) reduce to a finite integer or rational expression in
the primitive base `(α_H = 2, D = 3)`, with the transcendental π
appearing **only** in accumulation-floor accounting? And is the
primitive base `(α_H, D)` **minimal** — i.e., does no smaller
primitive set (just α_H, just D) suffice?

## The unification claim (from SAM_UNIFICATION_NOTE)

```text
CLAIM:
  Every numerical quantity in any sealed SAM law reduces to:
    (a) primitive integer α_H = 2
    (b) primitive integer D = 3
    (c) finite integer/rational expression in (a) and (b)
    (d) the transcendental π (route-completion only)

  No other primitives. No free parameters. The set of "substrate
  atoms" and the set of "law constants" are one category.
```

CR258 audits this claim by enumeration: for every named constant in
the manuscript and CR campaign, write its closed-form reduction in
(α_H, D), evaluate numerically, and verify equality.

## Registry of constants to audit

Each entry: name, expected numerical value, reduction expression,
source artifact.

```text
PRIMITIVES
  α_H              = 2                    primitive (Volume I §4.2/4.3)
  D                = 3                    primitive (Volume I §4.1)

DERIVED COUNTS (Volume I §4)
  S                = α_H^D            = 8        split inventory
  D²               = D · D            = 9        dimensional square
  D³ = V           = D · D · D        = 27       write cell
  D⁴ = F           = D · D · D · D    = 81       carrier face
  R                = α_H² · D         = 12       route radix
  R²               = α_H⁴ · D²        = 144      writable capacity
  Θ                = α_H · D²         = 18       tensor bridge
  L                = α_H · F          = 162      closed ledger
  M                = α_H · D² · (α_H³ − 1) = 126 matter capacity
  S + 1            = α_H^D + 1        = 9        completed split count

BIGRADE ALPHABET
  P_le_R           = {α_H^a · D^b : (α_H^a·D^b)² ≤ R²}
                                      = {1, 2, 3, 4, 6, 8, 9, 12}
  bigrade_sum      = 1+2+3+4+6+8+9+12 = 45
  bigrade_max      = 12 (= R)

LIFTED CONNECTORS L_p (Volume II §13.3)
  L_1   = 1 + 1/R²                    = 1.006944...
  L_2   = 2 + 4/R²                    = 2.027778...
  L_3   = 3 + 9/R²                    = 3.0625
  L_4   = 4 + 16/R²                   = 4.111111...
  L_6   = 6 + 36/R²                   = 6.25
  L_8   = 8 + 64/R²                   = 8.444444...
  L_9   = 9 + 81/R²                   = 9.5625
  L_12  = 12 + 144/R²                 = 13
  L_18  = 18 + 324/R²                 = 20.25 (FORBIDDEN as local fee)

T13 LANE STRUCTURE (CR238)
  T13 multiset     = {1, 1, 2, 3, 4, 6, 8, 8, 9, 9, 12, 18, 81}
  T13 partition sum = α_H · F         = 162 = L
  non-Z T13 sum    = L − F            = 81 = F

MATTER CHARGED LAW (CR254)
  c_+              = 1 + α_H^(−2)     = 5/4
  c_-              = 1 + α_H^(−1)     = 3/2
  matter surface   = 1 + p/R²         (function of p)
  depth lift       = R^d              (function of d)

MATTER NEUTRAL LAW (CR255)
  tensor share     = α_H^(−D)         = 1/8
  retained share   = 1 − α_H^(−D)     = 7/8

A-OPERATOR (CR256)
  A neg coef       = c_+ / c_-        = 5/6
  A pos coef       = c_- / c_+        = 6/5
  route scale      = R^(d+1)          (depth-dependent)

A MEETS Θ (CR257)
  d=1 neg form     = R · c_+ · p · (1 + p/R²)²
  d=1 pos form     = R · c_- · p · (1 − p²/R⁴)

INCLUSION-EXCLUSION (Section 4)
  R² + Θ           = L                = 144 + 18 = 162
  R² − Θ           = M                = 144 − 18 = 126
  L − M            = 2Θ               = 36
  M / R²           = 7/8              (retained share at row level)
  Θ / R²           = 1/8              (tensor share at row level)

ACCUMULATION (Section 4.7) — contains π
  A_0              = 1 / (π · R)      = 1 / (12π)        accumulation floor
  A_share          = 1 / R            = 1/12             completed share
  A_side           = 1 / (2R)         = 1/24             half-side
```

## Verification protocol

For each constant in the registry:
1. State the closed-form reduction in (α_H, D) [or (α_H, D, π) for
   accumulation entries].
2. Evaluate the reduction with α_H = 2, D = 3.
3. Compare to the declared numerical value.
4. Pass: equality to exact rational (Fraction class) for rational
   constants; equality to abs_tol 1e-12 for π-bearing constants.

Constant counts:
- **2 primitives**: α_H, D
- **22 derived rational constants** in (α_H, D)
- **3 π-bearing constants** in accumulation
- **Total: 27 named quantities**

## Minimality wrong-controls

**W1 — α_H-only base**. Attempt to express D = 3 as a finite
rational expression in α_H = 2 alone. Equivalently: is D ∈ ℚ(α_H) =
ℚ? Yes (D = 3 is an integer), but D ≠ α_H, D ≠ α_H + α_H − 1, etc.
The DERIVATION of D from α_H requires the substrate closure identity
`D^(D-1) = α_H^D + 1`, which is a transcendental equation in D not
expressible as a finite rational expression in α_H alone. So D is
not derivable from α_H alone without external input. Verify
symbolically.

**W2 — D-only base**. Attempt to express α_H = 2 as a finite rational
expression in D = 3 alone. The substrate axioms require α_H as the
binary readout independently of D. α_H ≠ D − 1, α_H ≠ D/D, etc.
α_H is not derivable from D alone. Verify.

**W3 — single integer primitive**. Attempt to express both α_H AND D
as expressions in a single primitive k. For any choice of k, either
α_H or D fails to be a rational expression in k alone (since the
two are mutually constrained by the closure identity but not
identifiable as a single integer choice). Verify by exhaustive
small-integer search over k ∈ {1, 2, 3, 4, 5, 6}.

**W4 — primitive π replacement**. The π in the accumulation chain
cannot be eliminated by rational expressions in (α_H, D). Verify by
checking A_0 = 1/(π · R) is transcendental; no rational expression
in (α_H, D) equals 1/(π · 12) exactly.

## Verdict tree

```text
PASS:
  (1) every registry entry reduces to (α_H, D)
      [or (α_H, D, π) for accumulation entries]
      with verified equality
  (2) W1 confirms D is not a finite rational expression in α_H alone
  (3) W2 confirms α_H is not a finite rational expression in D alone
  (4) W3 confirms no single integer primitive k generates both
  (5) W4 confirms π is irreducible to rational expressions in (α_H, D)

BOUNDARY:
  every entry reduces correctly but one of W1-W4 returns ambiguous

FAIL:
  any registry entry does NOT reduce to (α_H, D, π)
  [registry was incomplete or unification claim is wrong]
```

## What this CR seals

The substrate-primitive base `(α_H, D)` is sealed as the **minimal
sufficient** integer primitive set generating every rational
quantity in any sealed SAM artifact. The transcendental π is sealed
as the **irreducible** route-completion normalization required by
the accumulation chain.

The CR258 result becomes the authoritative reference for the
"zero free parameters" claim in downstream particle-mass and
chemistry derivations. The unification SAM_UNIFICATION_NOTE
becomes CR-class theorem-grade.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| SAM_UNIFICATION_NOTE_2026_06_28.md | `8c7029c607b7a1c6acf5741517e8811fab62a574e6f79bc9278c2ee3989bda28` |
| SAM_VOLUME_II_1_MATTER_UPDATE_2026_06_28.md | `0279ea3028da9785fcf22146f53a255cb0bfb68eccebc4c2f26ac0c5957a5da2` |
| CR253-CR257 sealed CRs (transitively) | per their HASHES.txt |
| stewardship | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
