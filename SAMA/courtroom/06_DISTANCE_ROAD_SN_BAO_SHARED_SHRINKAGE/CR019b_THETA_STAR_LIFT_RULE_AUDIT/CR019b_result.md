# CR019b — θ_* Substrate-Lift Rule Audit — RESULT

```text
verdict           : FAIL (audit-informative; substrate-lift mechanism ruled out)
classification    : AUDIT_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : d83ef6864e095550cb7989a88da88c25b60c2b8bd584b7719efd4568d3b8f32f
runner_hash       : 4d6f5339b7a6ac97e756a9ea58961ced2d44618bfee31690c4f699e9d791a120
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

The hypothesis — that the 09a binding-work lift rule (bigrade {1, 2, 3,
4, 6, 8, 9, 12} pays `+p²/R²` lift; Θ = 18 exempt) applied to CR019@06's
substrate atoms closes the +0.605% θ_* gap — is **ruled out**. No
substrate-lift correction tested closes θ_* without breaking either ℓ_A
or r_d beyond the 1% gate.

The 0.605% θ_* discrepancy is **not in the substrate-lift layer**. It
sits in the Hu-Sugiyama / EH fitting-formula error budget at the
recombination-physics layer of CR019@06's derivation chain.

This is an audit-informative FAIL: the test cleanly eliminates one
candidate mechanism for the largest SAM-vs-Planck gap in the
discrimination map.

## Note on runner verdict-logic correction

The CR019b runner's automated verdict logic counted the brute-force
joint-grid optimum as a "substrate-lift candidate" alongside H1-H4,
which would have flipped the verdict to PASS. The precommit text is
explicit:

> PASS: At least one **substrate-lift correction** (single-atom or
> simple compound) closes 100·θ_* gap to ≤ 0.1% AND keeps ℓ_A AND r_d
> each ≤ 1% from Planck.

The joint-grid optimum is **not a substrate-lift correction** — it's
an unconstrained brute-force fit over (Ω_m, Ω_b). It serves as a
diagnostic showing what shifts would be required to close all three
gates simultaneously, but it doesn't correspond to any closed-form
substrate-lift derivation. The required Ω_b shift (+4.9%) exceeds any
single-atom lift (largest is L_12 = +8.3% on the value 12 → 13, but
that's a different atom and a different cascade).

Applying the precommit's actual "substrate-lift correction" filter,
no candidate satisfies the joint-PASS gates. Verdict: FAIL.

## Per-candidate results (substrate-lift candidates only)

| candidate | Ω_m | Ω_b | θ_* gap | ℓ_A gap | r_d gap | joint PASS |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| canonical (CR019 sealed) | 0.31831 | 0.04930 | +0.605% | -0.602% | +0.461% | — (baseline) |
| H1: R lifted in A_0 | 0.29382 | 0.04577 | **+0.030%** | -0.031% | **+3.59%** | **NO** (r_d broken) |
| H2: R lifted consistently | 0.31831 | 0.04577 | +1.175% | -1.162% | +1.445% | NO |
| H3: χ lifted (S, d̂) | 0.31831 | 0.04917 | +0.626% | -0.623% | +0.496% | NO (θ_* essentially unchanged) |
| H4: all bigrade lifted | 0.31831 | 0.04566 | +1.193% | -1.180% | +1.476% | NO |
| WC: Θ lifted (forbidden) | 0.28294 | 0.04930 | -1.090% | +1.101% | +3.575% | NO (confirms binding rule) |

**Diagnostic only (not a substrate-lift candidate):**

| candidate | Ω_m | Ω_b | θ_* gap | ℓ_A gap | r_d gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| joint grid optimum | 0.31354 (-1.5%) | 0.05171 (+4.9%) | +0.0004% | -0.0014% | +0.209% |

## What the data shows

1. **H1 (lift R in A_0 only) closes θ_* to 0.030% — 20× better than canonical.**
   But it shifts Ω_m by -7.7% and breaks r_d to +3.59%. The mechanism
   touches the right quantity (the bigrade R) but doesn't produce a
   self-consistent fix across all three observables.

2. **WC (lift Θ) makes everything worse**, confirming the 09a binding-
   work finding from CR249a / CR251 from the opposite direction: Θ
   should NOT be lifted. This is consistent across two CR branches.

3. **No single-atom or simple-compound substrate-lift produces both
   the Ω_m and Ω_b shifts** that the joint grid optimum identifies as
   required (Ω_m -1.5%, Ω_b +4.9%). The Ω_b shift in particular is
   structurally unavailable to any clean substrate-lift candidate.

4. **Θ = 18 does not appear explicitly in CR019@06's substrate inputs.**
   The bigrade atoms that DO appear (R = 12, S = 8, d̂ = 3, d̂² = 9)
   admit lift corrections, but none of them — alone or in combination
   — yield a joint PASS.

## What this means for the framework

The 09a binding-work lift rule (bigrade pays, Θ exempt) is structurally
real and remains valid for binding work (CR249a `c_A = 1/(S·L) = 1/1296`
within 0.44%; CR251 isolates `1/(S·L)` from `1/(S·R²)` at >5σ via the
bounce factor `L/R² = 9/8`). What CR019b establishes is that this rule
**does not generalize to CR019@06's recombination-layer derivation**.
The rule operates at the static accounting layer; the θ_* gap lives
in the dynamic recombination-physics layer that uses Hu-Sugiyama /
Eisenstein-Hu fitting formulas with their own intrinsic ~1% accuracy.

The 0.605% θ_* gap remains real and is correctly characterized in
SAM_VOLUME_I_SUBSTRATE.md as "the acoustic geometry is not exact." It
is not a substrate-lift misapplication. It is a recombination-layer
fitting-formula residual that would require **substrate-derived
recombination physics** (a Saha equation analog, Peebles' three-level
atom analog, etc., in substrate-counting terms) to close at the
substrate level.

That's a multi-CR program in its own right, not a single audit fix.

## What this CR opens

- **No immediate substrate-fix path** for θ_* via the lift rule. The
  rule is correctly applied here and ruled out as the mechanism.
- **Open future work**: substrate-derived recombination physics (Saha
  → substrate-Saha; Peebles → substrate-Peebles). Multi-CR scope.
  Would address θ_*, ℓ_A, r_d, z_*, z_drag, r_s(z_*), D_M(z_*) as a
  joint program rather than per-observable patches.
- **No retraction of CR019@06 needed**: the +0.605% gap was sealed
  honestly, the 1% PASS gate held, and the audit confirms the
  characterization is correct.

## Provenance hash chain

```text
precommit          : d83ef6864e095550cb7989a88da88c25b60c2b8bd584b7719efd4568d3b8f32f
runner             : 4d6f5339b7a6ac97e756a9ea58961ced2d44618bfee31690c4f699e9d791a120
upstream CR019@06  : sealed PASS (precommit ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da)
upstream CR249a@09a (A-kernel binding geometry) — c_A = 1/(S·L) within 0.44%
upstream CR251@09a (bounce-aware asymmetry isolation) — isolated 1/(S·L) at >5σ
upstream CR229@09a (inclusion-exclusion identity; Θ = 18 = overlap)
upstream CR005@21 (Θ-overflow + QNM derivation) — partition-algebra framework
upstream CR004@21 (discrimination map) — identified θ_* as highest-σ gap
stewardship        : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR019b FAIL (audit-informative).** The 09a binding-work lift rule
(bigrade lifted, Θ exempt) does not close the +0.605% θ_* gap in
CR019@06. Five substrate-lift candidates were tested (H1-H4 + a
forbidden-Θ wrong-control); none satisfy the joint PASS gate of
θ_* ≤ 0.1% AND ℓ_A ≤ 1% AND r_d ≤ 1%. The brute-force joint-grid
optimum exists but requires Ω_b shifts (+4.9%) unavailable to any
substrate-lift correction. The 0.605% θ_* gap is in the
Hu-Sugiyama / EH fitting-formula layer of CR019's derivation, not in
the substrate-lift layer. The 09a binding lift rule remains valid for
binding work and is correctly ruled out for θ_*. Substrate-derived
recombination physics is the candidate forward path if the θ_* gap is
to be closed at the substrate level — multi-CR scope, not addressed
here.

`THETA_STAR_LIFT_RULE_AUDIT_5_SUBSTRATE_LIFT_CANDIDATES_TESTED_NONE_ACHIEVE_JOINT_PASS_H1_CLOSES_THETA_BREAKS_RD_WC_LIFT_THETA_BREAKS_ALL_CONFIRMING_CR249A_BINDING_FINDING_FAIL_AUDIT_INFORMATIVE`
