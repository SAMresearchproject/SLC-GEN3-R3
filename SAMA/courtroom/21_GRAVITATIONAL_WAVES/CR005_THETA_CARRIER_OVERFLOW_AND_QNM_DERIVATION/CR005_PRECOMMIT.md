# CR005 — Θ Carrier Overflow and Schwarzschild QNM Derivation

**Branch:** 21_GRAVITATIONAL_WAVES
**Classification:** STRUCTURAL_IDENTIFICATION_CR (substrate-physics derivation)
**Sealed by:** Sean Brady, 2026-06-29
**Upstream:** CR229@09a (inclusion-exclusion), CR238@09a (closure axiom + typed spine), CR218@09a (bigrade alphabet), CR001@21 (cap), CR003@21 (QNM match), CR004@21 (discrimination map)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## What this CR seals

The Schwarzschild fundamental quasi-normal mode dimensionless real
frequency `ω_R · M = d̂ / (d̂^(d̂−1) − 1) = d̂/S = 3/8` is derived
from substrate-physics, not identified by enumeration. The
derivation chain uses three load-bearing structural facts:

1. **Partition algebra and overflow** — the bounded partition algebra
   `{ ĥ^i · d̂^j : i ∈ {0..d̂}, j ∈ {0..d̂−1} }` contains 12 products
   at the canonical substrate `(ĥ, d̂) = (2, 3)`. Exactly 8 of them
   fit inside `R = ĥ²·d̂`. The smallest product that exceeds `R` is
   `ĥ · d̂² = 18 = Θ` — the carrier tensor.
2. **Θ has no rest position** — by (1), Θ is the first element of the
   typed partition algebra that does not fit inside the route radix.
   It cannot occupy a substrate position at rest. Therefore it must
   propagate as the carrier.
3. **Substrate accounting in Θ-units** — Sean's identity
   `Θ + M = R² = ℒ − Θ` rewrites the closed-ledger atoms as integer
   multiples of Θ: `M = (S−1)·Θ`, `R² = S·Θ`, `ℒ = (S+1)·Θ`. The
   unit-counts `{7, 8, 9}` are exactly `{ĥ^d̂−1, ĥ^d̂, d̂^(d̂−1)}`,
   the closure-axiom values of CR238.

From (1)+(2)+(3), the QNM dimensionless real frequency is:

```text
ω_R · M  =  (Θ · d̂) / R²                       [Θ-overflow propagates in d̂ dims, normalized to capacity]
         =  d̂ / S                                [Sean's identity: R² = S·Θ; the Θs cancel]
         =  d̂ / (d̂^(d̂−1) − 1)                   [closure axiom: S = ℒ/Θ − 1 = d̂^(d̂−1) − 1]
         =  3 / (9 − 1)
         =  3 / 8
         =  0.375
```

The substrate-physics reading: **one Θ-unit per inventory capacity,
per spatial dimension**. The overflow propagates in d̂ dimensions;
the substrate's inventory contains exactly S = ĥ^d̂ Θ-units; the
dimensionless frequency is the propagation rate per dimension per
Θ-unit of inventory.

The empirical confirmation from CR003 is `ω_R · M = 0.37500` vs GR's
numerical `0.37367168`, gap 0.36%. CR005 elevates this match from
"closed-form substrate atom that hits within 0.36%" to "substrate-
physics derivation that produces 3/8 from the closure axiom and the
partition-algebra overflow."

## What this CR does NOT seal

- **The imaginary-part / damping rate.** CR003's match `ω_I · M =
  R/(R²−d̂²) = 4/45` is a structural identity but does not reduce
  cleanly to Θ-units (the factor `R²−d̂² = (15/2)·Θ` is half-integer
  in Θ-units). The damping rate is held as a sealed CR003 identity
  pending future substrate-physics work; CR005 does not claim a
  first-principles derivation of the imaginary part.
- **Higher Schwarzschild modes** (CR003b). The substrate-grammar
  matches for l ∈ {2..5}, n ∈ {0,1} stand as sealed enumerations;
  CR005 does not generalize the derivation to those modes.
- **The Kerr spinning case.** Continuous spin parameter `a/M` has no
  obvious substrate-atom encoding; CR005 stays within the
  Schwarzschild (non-spinning) framework.

## Verifiable claims (pre-registered)

The runner shall verify each of these to exact arithmetic equality.
A failure on any single claim flips the CR to FAIL — these are not
gates with tolerance; they are derivation-chain self-checks.

### A. Bounded partition algebra and overflow

**A1.** Enumerate `ĥ^i · d̂^j` for `i ∈ {0, 1, ..., d̂}` and
`j ∈ {0, 1, ..., d̂−1}` at `(ĥ, d̂) = (2, 3)`. Total grid cells = 12.

**A2.** Exactly 8 products satisfy `ĥ^i · d̂^j ≤ R = 12`. The set of
values is `{1, 2, 3, 4, 6, 8, 9, 12}` — bit-identical to CR218@09a's
sealed bigrade alphabet.

**A3.** Of the 4 products that exceed `R`, the smallest value equals
`Θ = 18` and corresponds to `(i, j) = (1, 2)` (i.e., `ĥ · d̂²`). The
remaining three overflows are `{24, 36, 72}`.

**A4.** `ĥ · d̂² = Θ` algebraically (already sealed in CR229 via
`Θ = α_H · D²`).

### B. Substrate-in-Θ-units identities

**B1.** `Θ = 18`, `M = 126`, `R² = 144`, `ℒ = 162` (sealed atoms; quoted).

**B2.** `M / Θ = 7` exact integer.

**B3.** `R² / Θ = 8 = S` exact integer.

**B4.** `ℒ / Θ = 9` exact integer.

**B5.** `Θ + M = R²` exact (Sean's identity, additive form).

**B6.** `ℒ − Θ = R²` exact (Sean's identity, subtractive form).

**B7.** `R² = S · Θ` exact (multiplicative form).

**B8.** `M = (S − 1) · Θ` exact.

**B9.** `ℒ = (S + 1) · Θ` exact.

### C. Closure-axiom connections

**C1.** `S = ĥ^d̂ = 8` (CR238 typed spine).

**C2.** `S + 1 = d̂^(d̂−1) = 9` at `d̂ = 3` (CR238 Block E closure
axiom; d̂ = 3 is the unique positive integer solution).

**C3.** Therefore `ℒ / Θ = S + 1 = d̂^(d̂−1)` — the closed ledger in
Θ-units is the closure-axiom number.

**C4.** `S − 1 = M / Θ = 7 = ĥ³ − 1 = α_H³ − 1` — matter capacity in
Θ-units is the same `7` that appears in CR221's `κ = 7117/768`
(where `7117 = α_H³ · ...` traces upstream to this 7).

### D. QNM derivation chain

**D1.** Define `ω_R_M_substrate = d̂ / (d̂^(d̂−1) − 1)`.

**D2.** Verify `ω_R_M_substrate = 3/8 = 0.375` exact rational.

**D3.** Verify `ω_R_M_substrate = d̂ / S` (using closure axiom).

**D4.** Verify `ω_R_M_substrate = (Θ · d̂) / R²` (using Sean's identity).

**D5.** All three forms are bit-identical fractions.

**D6.** Compare to GR Berti+2009 value `ω_R_M_GR = 0.37367168`:
gap = `(0.375 − 0.37367168) / 0.37367168 = +0.356%` — matches CR003's
sealed empirical residual to the digit.

### E. Falsification controls

**E1.** Enumerate `ĥ^i · d̂^j` over the wider grid `i ∈ {0..d̂+1}`,
`j ∈ {0..d̂}`. Confirm that `Θ = 18` remains the smallest overflow
WITHIN the typed-spine bounded grid `(i ≤ d̂, j ≤ d̂−1)`. In the wider
unbounded grid, `ĥ^(d̂+1) = 16 < Θ` would be a smaller overflow, but
`ĥ^(d̂+1)` lies OUTSIDE the typed partition algebra (the substrate
typed spine bounds `i ≤ d̂` because `ĥ^d̂ = S` is the maximum binary
power that the typed kernel uses).

**E2.** Verify the bound `j ≤ d̂ − 1` is the closure-axiom bound:
`d̂^(d̂−1) = S + 1` (the largest dimensional power that participates
in the closure identity).

**E3.** Verify that NO substitute candidate for the carrier in the
bounded partition algebra has the same overflow property as Θ.
Specifically: there is exactly one smallest overflow, it is `ĥ·d̂² = 18`,
and any other candidate (`d̂^d̂ = 27`, `ĥ^(d̂+1) = 16`, etc.) either
lies outside the bounded grid or has a different role in CR229's
inclusion-exclusion identity.

## Verdict tree

```text
PASS:
  every claim A1-A4, B1-B9, C1-C4, D1-D6, E1-E3 verified to exact
  arithmetic equality. The substrate-physics derivation chain is
  self-consistent and produces ω_R·M = 3/8 from the closure axiom +
  partition-algebra overflow + Θ-unit accounting.

FAIL:
  any single arithmetic claim fails. Indicates either:
  (i) bug in the precommit's structural framing; or
  (ii) upstream sealed CR (CR229, CR238, CR218) has a value the
       precommit misquotes.
  Either way, stop and audit before proceeding to CR005b or beyond.
```

This CR has no BOUNDARY band. The claims are exact rationals; they
either hold or they don't.

## Manuscript implications (conditional on PASS)

The Schwarzschild fundamental QNM dimensionless real frequency
`ω_R · M ≈ 0.37367` becomes the first numerical coefficient in GR
that SAM provides a substrate-physics derivation for — not just a
substrate-atom closed-form match. The derivation uses only sealed
upstream identities (closure axiom CR238, inclusion-exclusion
CR229, bigrade alphabet CR218) plus Sean's `Θ + M = R²` accounting
identity (which is itself a consequence of CR229's inclusion-
exclusion under unit-counting).

The 0.36% gap between SAM's `3/8` and GR's `0.37367168` becomes a
prediction with structural justification, not a coincidence — SAM
commits to `3/8 exactly` because of the closure-axiom Θ-unit
accounting; GR computes `0.37367168` as a continuum eigenvalue.
The discrimination test becomes LISA-era ringdown spectroscopy
at SNR > 1000 on supermassive-BH events (per CR004 discrimination
map).

## What this opens

- **CR005b** — substrate-dynamics derivation of the damping rate
  `ω_I · M`. The half-integer Θ-count of `R² − d̂²` suggests the
  damping is about overflow leak-back into the inventory rather than
  pure overflow propagation; a substrate-dynamics framework is
  needed.
- **CR006** — formal forecast lock for the LISA-era discrimination,
  with explicit σ thresholds and verdict criteria for the eventual
  measurement.
- **CR-cross-domain** — extend the Θ-overflow framing to other
  numerical coefficients in the discrimination map: do they have
  analogous "first overflow of a bounded partition algebra"
  interpretations?

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR229@09a inclusion-exclusion | per HASHES.txt of 09a |
| CR238@09a typed spine + closure axiom | per HASHES.txt of 09a |
| CR218@09a bigrade alphabet | per HASHES.txt of 09a |
| CR001@21 carrier-tensor cap | precommit `1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805` |
| CR003@21 QNM fundamental match | precommit `ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3` |
| CR003b@21 QNM higher modes | precommit `9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5` |
| CR004@21 discrimination map | precommit `e519e7c5b8be99540c5c6984079e91f4e56b524d9b9c87e43baabd3f5f61933a` |
| CR258@09a primitive closure audit | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| branch README.md | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| branch GW_SUBSTRATE_FRAMING.md | `a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941` |
| branch STUDY_NOTES_FOR_QNM_DERIVATION.md | (sibling in 21 folder; pulled at runner) |
| stewardship | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
