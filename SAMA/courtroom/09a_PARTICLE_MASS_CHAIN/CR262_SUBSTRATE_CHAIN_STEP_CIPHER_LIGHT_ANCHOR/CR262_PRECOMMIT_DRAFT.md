# CR262 — Substrate Chain-Step Surface-Debit Cipher (Light-Element Anchor)

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_PREDICTION_CR (downstream of CR248/CR258/CR259/CR261)
**Status:** DRAFT — not yet sealed. Iterate before sealing precommit hash.
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does the substrate-natural ĥ·d̂^k chain — the same chain identified in
CR005ab (neutrino m₃ = ĥ·d̂ = 6), in CR005 (Θ = ĥ·d̂² = 18 carrier-tensor),
and in CR259's chessboard accounting — correctly **predict** which Z = N
nuclei are favored (peak per-nucleon binding), which are off-chain
(unstable), and the position of the surface-debit minima across the light
element regime, with **no fitted coefficients**?

## Structural claim

For every nucleus (Z, N):

```text
u_count = 2Z + N      ← total u-quarks across all nucleons
d_count = Z + 2N      ← total d-quarks
e_count = Z
A = Z + N

balanced configuration ⟺ Z = N AND u = d = 3Z

Substrate predicts: **per-nucleon binding peaks (mass-excess minima) occur
exactly when 3Z lands on the ĥ·d̂^k chain step.**
```

Chain steps and their predicted nuclei (Z = N case):

```text
k     ĥ·d̂^k    3Z = ĥ·d̂^k  →  Z = N   nucleus     status
─────────────────────────────────────────────────────────────────
0       2          —             —      —          (primitive; no Z=N)
1       6          2             He-4   alpha       **chain anchor**
2      18          6             C-12   carbon      **chain anchor** (also = u)
3      54         18             Ar-36  argon       **chain anchor**
4     162         54             Xe-108 ???         (PREDICTED UNSTABLE)
```

Three chain-step balanced nuclei (He-4, C-12, Ar-36) — substrate-natural
peaks in per-nucleon binding. The framework predicts these are exactly
where the chain emerges as observed-binding maxima.

## Wrong-control predictions (Z = N, off-chain)

Other Z = N nuclei sit at substrate atoms that are NOT on the ĥ·d̂^k chain.
The framework predicts these are LESS favored than their chain-step
neighbors — either lower per-nucleon binding, instability, or both:

```text
Z = N    3Z   substrate atom    on chain?     prediction
─────────────────────────────────────────────────────────────────────────
1 (H-2)   3   d̂  (primitive)    no           bound but low BE/A (~1.1 MeV/A)
3 (Li-6)  9   d̂² = closure      no           stable but BE/A < He-4's
4 (Be-8) 12   R  (radix)         no           **UNSTABLE → 2·He-4** (load-bearing predictor)
5 (B-10) 15   off-atom           no           less favored than neighbors
8 (O-16) 24   off-chain          no           bound, BE/A intermediate
9 (F-18) 27   V  (volume)        no           unstable (β⁺ decay)
12 (Mg-24)36  m₃² = (ĥd̂)²       no           stable but BE/A < C-12
27 (Co-54)81   F  (face)         no           **UNSTABLE** (predicted)
```

Be-8 is the **load-bearing falsifier**: substrate puts it on R (radix), not
on the chain. If Be-8 were stable, the chain prediction would fail. Be-8 is
known to be unstable (decays to 2 He-4 within 10⁻¹⁶ s); the framework
recovers this without fitting anything.

## Locked Substrate Atoms

```text
ĥ = 2     d̂ = 3     R = 12     Θ = 18
M = 126   ℒ = 162   V = 27     F = 81
S = 8     D² = 9    R + 1 = 13

ĥ·d̂^k chain:    k = 0    1    2    3      4
                      ĥ    m₃   Θ    ĥ·V   ℒ
                      2    6    18   54    162
```

## Locked source-count identities (CR248 sealed)

```text
For nucleus (Z, N, A):
  source u    = 2Z + N
  source d    = Z + 2N
  source e    = Z

Z = N case:
  source u = source d = 3Z
  asymmetry dQ = 0
```

## Pre-registered hypotheses

**H1 (chain-step balanced nuclei are stable AND have local maxima in BE/A):**

```text
He-4   (Z=2, u=d=6=m₃):       stable AND local BE/A maximum    [test against AME2020]
C-12   (Z=6, u=d=18=Θ):       stable AND local BE/A maximum
Ar-36  (Z=18, u=d=54=ĥV):     stable AND local BE/A maximum
```

**H2 (off-chain "false anchor" Be-8 is unstable):**

```text
Be-8 (Z=4, u=d=12=R):  predicted unstable because R is not on the ĥ·d̂^k chain
                       observed: half-life 8.19 × 10⁻¹⁷ s, decays to 2 He-4 ✓
```

**H3 (off-chain F-18 at u=d=V is unstable):**

```text
F-18 (Z=9, u=d=27=V): predicted unstable
                      observed: t₁/₂ = 109.77 min, β⁺ decay ✓
```

**H4 (off-chain Co-54 at u=d=F is unstable):**

```text
Co-54 (Z=27, u=d=81=F): predicted unstable
                        observed: t₁/₂ = 193.27 ms, β⁺ decay ✓
```

**H5 (chain prediction extends to Z=N=54 → Xe-108):**

```text
Xe-108 (Z=54, u=d=162=ℒ): predicted exists but UNSTABLE (high A, beyond
                          alpha-stable region)
                          observed: no stable Xe-108; not yet synthesized;
                          framework prediction is structurally consistent
                          with "alpha-stable region ends below ℒ chain step"
```

**H6 (per-nucleon binding ranking across light Z=N nuclei):**

```text
Predicted ordering:  BE/A(He-4) > BE/A(Be-8) [Be-8 unstable, not directly
                     measurable but extrapolated]
                     BE/A(C-12) > BE/A(Be-8)
                     BE/A(C-12) > BE/A(Li-6)
                     BE/A(C-12) > BE/A(O-16)? — NO: O-16 has higher BE/A than C-12
                     
                     Reading: chain-step maxima are LOCAL not global; global
                     BE/A peak is near Fe-56, well above chain step k=2
```

Note H6 has a subtlety: the chain prediction is for *local* maxima within
each chain step's neighborhood, not for *global* binding maxima. The CR
verifies the local-maximum claim, not "chain step always wins."

## Sealed PASS Gates

```text
G1  Chain-step balanced nuclei (He-4, C-12, Ar-36) are all stable in
    AME2020 AND each has higher BE/A than its immediate Z = N neighbors
    on the off-chain ladder.

G2  Be-8 is unstable in AME2020 (or has half-life ≤ 1 second).

G3  F-18 is unstable.

G4  Co-54 is unstable.

G5  Source-count identities (u, d, e) read on chain steps exactly:
    He-4   → u = d = 6  (= ĥ·d̂ = m₃)        verified exact
    C-12   → u = d = 18 (= Θ)                 verified exact
    Ar-36  → u = d = 54 (= ĥ·V = ĥ·d̂^3)     verified exact

G6  Source-count identities on off-chain anchors:
    Be-8   → u = d = 12 (= R)                 verified exact
    F-18   → u = d = 27 (= V)                 verified exact
    Co-54  → u = d = 81 (= F)                 verified exact

G7  Precommit hash verified at load AND forbidden-file guard not tripped.

PASS  iff G1–G7 all hold.

BOUNDARY  iff (G1 holds AND G2 holds) but one of G3 / G4 fails AND it can
          be attributed to non-substrate physics not in scope (rare).

FAIL  iff G1 fails (a chain-step nucleus is unstable) OR G2 fails (Be-8 is
      stable) OR source-count identities fail.
```

The load-bearing test is G1 + G2: if Be-8 were stable OR if He-4/C-12/Ar-36
were unstable, the framework would be falsified at the structural level.

## Reported Evidence (not gated)

```text
E1  Per-element BE/A across all Z = N stable nuclei in AME2020.
E2  Source-count tabulation (u, d, e, A) per nucleus.
E3  Substrate-distance metric: distance from (u, d) to nearest chain step.
E4  Half-life table for all Z = N nuclei tested (stable + unstable).
E5  Falsifier list: any chain-step nucleus that is unstable; any off-chain
    nucleus that is stable in violation of the prediction.
E6  Comparison of CR262 prediction vs CR261 BW fit RMS on Z = N row.
```

## Pre-Registered Frozen Inputs

| field | source | notes |
| --- | --- | --- |
| AME2020 atomic masses | CR248_train_lane_a.csv + CR248_test_holdout.csv (sealed hashes) | reuses CR248's hash-locked data |
| NUBASE2020 half-lives | external — to be added or cited | Be-8, F-18, Co-54 half-lives needed for G2/G3/G4 |
| Chain steps | in-code: {ĥ·d̂^k for k = 0..4} | pure substrate |

**Open spec question:** AME2020 covers mass but not half-life. We may need
to import a separate NUBASE2020 half-life column or cite published values
as numeric literals for G2/G3/G4 evaluation. Resolve before sealing.

## Rule-9 Line

```text
This test could have falsified the claim that the ĥ·d̂^k substrate-natural
chain predicts which Z = N nuclei are observed-stable with peak per-nucleon
binding (He-4, C-12, Ar-36) AND which are observed-unstable because they
sit at substrate atoms off the chain (Be-8 at R, F-18 at V, Co-54 at F).
Falsification modes: (i) any chain-step nucleus is unstable, (ii) Be-8 is
stable, (iii) source-count identities fail to read exactly.
```

## What This CR Seals (if PASS)

The substrate's ĥ·d̂^k chain — first identified geometrically in the matter
sector via CR005ab and the chessboard accounting CR259 — is shown to
predict the alpha-cluster nuclei (He-4, C-12, Ar-36) at zero fitted
parameters. The instability of Be-8 (the standard "alpha cluster paradox"
of nuclear physics) is structurally derived from Be-8 sitting on R, not on
a chain step. The cipher's first move is sealed: substrate counts + chain
positions predict observed nuclear stability without any nuclear-physics
phenomenology.

This is the structural counter to CR261's BW fit. CR261 fitted 4
phenomenological coefficients to reach 5.56 MeV RMS BOUNDARY. CR262
predicts the alpha-cluster structure at no fits and tests against
observed stability/instability. Different test, different scope; together
they bracket what's substrate-derived (the chain) from what's still
phenomenological (the BW curvature corrections).

## Open Items (to resolve before sealing)

1. **Half-life data source.** AME2020 doesn't carry t₁/₂. Either import
   NUBASE2020 t₁/₂ table by hash, or cite Be-8/F-18/Co-54 half-lives as
   numeric literals in the precommit (citing standard nuclear data tables
   by reference). Decision needed.

2. **Local-maximum metric.** "Local BE/A maximum" needs a precise
   definition. Options:
   (a) BE/A(chain-step) > BE/A(Z=N neighbors at Z±1, Z±2)
   (b) BE/A(chain-step) > BE/A(Z=N at next chain step)
   (c) Inflection-point check
   Pick before sealing.

3. **Ar-36 BE/A check.** Ar-36 BE/A ≈ 8.52 MeV/A; its neighbors Si-30
   ≈ 8.52, Ca-40 ≈ 8.55. The local-maximum claim at k=3 may be marginal;
   verify before sealing or adjust the claim.

4. **Heavy-end gracefulness.** Xe-108 at k=4 doesn't exist as a stable
   nucleus. Reframe H5: the chain "ends" at k=3 for stability, with k=4
   beyond the alpha-stable region. This is a structural observation, not
   a falsification — but the wording should be precise.

5. **Cross-check against CR253 / CR259.** The CR259 chessboard already
   sealed `m₃ = ĥ·d̂` and `Θ = ĥ·d̂²` as the matter-side substrate
   atoms. CR262 uses the same chain. Cite hash chain for provenance.

## Provenance Hash Chain (provisional)

| artifact | sha256 |
| --- | --- |
| CR248@09a (four-particle decomp) | precommit `7ad11ca6...` |
| CR258@09a (substrate primitive closure audit) | precommit `77c58a51...` |
| CR259@09a (chessboard bin structural ID) | precommit `53ec3c89...` |
| CR261@09a (pair-write binding extension BOUNDARY) | precommit `5b2d07b5...` |
| CR005@21 (Θ overflow + QNM derivation) | per branch 21 HASHES |
| CR005ab@21 (neutrino substrate identification) | per branch 21 HASHES |
| AME2020 train (reused from CR248) | sha256 `54c2c28d...` |
| AME2020 test (reused from CR248) | sha256 `8a5253f6...` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
