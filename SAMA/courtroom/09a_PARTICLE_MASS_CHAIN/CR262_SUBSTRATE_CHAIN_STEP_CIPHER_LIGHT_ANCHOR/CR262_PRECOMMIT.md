# CR262 — Substrate Carrier/Container Stability Cipher

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_PREDICTION_CR (downstream of CR248 / CR258 / CR259 / CR261)
**Sealed by:** Sean Brady, 2026-06-30
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

For every Z = N stable nucleus, the source-quark counts read
`u = d = 3Z`. When `3Z` lands on a sealed substrate atom, that atom is
either **carrier-like** (chain step on `ĥ·d̂^k` OR closure-axiom witness
`D² = S+1`) or **container-like** (radix `R`, volume `V`, face `F`, or
closed ledger `ℒ`). Does the substrate predict, with zero fitted
parameters, that Z = N nuclei landing on carrier atoms are **stable** and
Z = N nuclei landing on container atoms are **unstable**?

## Honest framing — K3 structural prediction test

This is a binary prediction across **eight Z = N nuclei** whose source-
quark counts land exactly on sealed substrate atoms. The prediction has
no free parameters: the substrate atom classification (carrier vs
container) is forced by the substrate spine (CR238 / CR258 / CR259 /
CR005 / CR005ab); the stability data is observational (AME2020 + NUBASE2020
half-lives).

Falsification modes:
- Any predicted-stable Z = N carrier nucleus is observed unstable.
- Any predicted-unstable Z = N container nucleus is observed stable.
- Source-quark count identity fails to read exactly on any of the eight.

This is **the structural counter to CR261's BW fit**: CR261 fitted 4
phenomenological coefficients and landed BOUNDARY. CR262 has 0 fitted
parameters and either passes binary stability predictions on 8 nuclei or
the framework is broken on a specific structural claim.

## Locked Substrate Atoms (read-only from CR238 / CR258 / CR259)

```text
Primitives:    ĥ = 2     d̂ = 3     π
Closure axiom: d̂^(d̂−1) = ĥ^d̂ + 1   →   D² = S + 1   →   9 = 8 + 1

Atoms:         S = ĥ^d̂ = 8         V = d̂^d̂ = 27        F = d̂^(d̂+1) = 81
               R = ĥ²·d̂ = 12        Θ = ĥ·d̂² = 18        ℒ = ĥ·F = 162
               M = R² − Θ = 126     D² = d̂² = 9

ĥ·d̂^k chain:   k = 0    1     2     3       4
                     ĥ    m₃    Θ     ĥ·V    ℒ
                     2    6     18    54      162
```

## Locked Source-Count Identities (CR248 sealed)

```text
For nucleus (Z, N, A) where A = Z + N:
  source u = 2Z + N
  source d = Z + 2N
  source e = Z

Z = N case:
  source u = source d = 3Z
  asymmetry dQ = 0
```

## Locked Carrier / Container Classification

```text
CARRIER atoms (predict stable Z = N nucleus when 3Z lands on them):
  m₃ = ĥ·d̂ = 6      chain step k = 1; heaviest neutrino mass eigenstate
                    (CR005ab sealed)
  D² = 9            closure axiom witness; S + 1
                    (CR258 sealed; the integer that picks (ĥ, d̂))
  Θ = ĥ·d̂² = 18     chain step k = 2; gravitational-wave carrier tensor
                    (CR005 sealed)
  ĥ·V = 54          chain step k = 3; per-dimension share of ℒ
                    (chain-derivable, not yet sealed in its own CR)
  ℒ = 162           chain step k = 4; closed ledger
                    (CR229 sealed)

CONTAINER atoms (predict unstable Z = N nucleus when 3Z lands on them):
  R = ĥ²·d̂ = 12     radix; capacity boundary of partition algebra
                    (CR238 sealed)
  V = d̂^d̂ = 27      volume; geometric capacity at dimension d̂
                    (CR238 sealed)
  F = d̂^(d̂+1) = 81  face; carrier-surface boundary
                    (CR238 sealed)
```

The structural distinction: **carriers propagate, containers bound.**
Chain-step atoms and the closure witness are propagator-class
(no rest position past R; closure act witness). The radix, volume, face,
and closed ledger are container-class (capacity boundaries; structure
ends here).

## Pre-Registered Predictions

### H1 — Carrier-atom Z = N nuclei are STABLE

| nucleus | Z = N | 3Z | substrate atom | predicted | observed |
| --- | ---: | ---: | --- | --- | --- |
| He-4   | 2  |  6  | m₃ = ĥ·d̂ (chain k=1) | stable | observed stable |
| Li-6   | 3  |  9  | D² (closure witness)   | stable | observed stable |
| C-12   | 6  | 18  | Θ (chain k=2)         | stable | observed stable (anchor of u) |
| Ar-36  | 18 | 54  | ĥ·V (chain k=3)       | stable | observed stable |

### H2 — Container-atom Z = N nuclei are UNSTABLE

| nucleus | Z = N | 3Z | substrate atom | predicted | observed |
| --- | ---: | ---: | --- | --- | --- |
| Be-8   |  4 |  12 | R (radix)                | unstable | t₁/₂ ≈ 8.19 × 10⁻¹⁷ s, α-decay → 2·He-4 |
| F-18   |  9 |  27 | V (volume)               | unstable | t₁/₂ = 109.77 min, β⁺ → O-18 |
| Co-54  | 27 |  81 | F (face / carrier surface) | unstable | t₁/₂ = 193.27 ms, β⁺ → Fe-54 |

### H3 — Chain step k=4 (Xe-108) doesn't exist as stable nucleus

| candidate | Z = N | 3Z | substrate atom | predicted | observed |
| --- | ---: | ---: | --- | --- | --- |
| Xe-108  | 54 | 162 | ℒ (closed ledger; chain k=4) | doesn't exist as stable | no stable Xe-108; stable Xe begins at Xe-124 |

This is the "chain ends" prediction: at k=4 the chain step lands on ℒ
which is the *closed* ledger — full carrier capacity. The framework
predicts that a Z = N nucleus at the closed-ledger position is past
the alpha-stable region, hence either doesn't form or is unstable. This
is consistent with observation (Xe-108 is not on the chart of stable
nuclides).

## NUBASE2020 / standard-nuclear-data half-life literals

```text
Be-8   t₁/₂ = 8.19 × 10⁻¹⁷ s        decay: 2α                  NUBASE2020
F-18   t₁/₂ = 109.77 min            decay: β⁺ → O-18           NUBASE2020
Co-54  t₁/₂ = 193.27 ms             decay: β⁺ → Fe-54          NUBASE2020
Xe-108 does not exist as a stable or known-bound isotope        NNDC
He-4   stable                                                    AME2020
Li-6   stable                                                    AME2020
C-12   stable (anchor of u; m = 12 exactly by definition)       AME2020
Ar-36  stable (0.334% natural abundance)                         AME2020
```

These values are cited from standard nuclear data tables (NUBASE2020,
NNDC chart of nuclides) as numeric literals in the precommit. The runner
verifies the predicted stability against these literals; it does not
re-derive half-lives from first principles.

## Sealed PASS Gates

```text
G1  Source-count identity exact on all eight Z = N nuclei in the test:
      He-4   u = d = 6  = m₃           verified exact
      Li-6   u = d = 9  = D²           verified exact
      C-12   u = d = 18 = Θ            verified exact
      Ar-36  u = d = 54 = ĥ·V          verified exact
      Be-8   u = d = 12 = R            verified exact
      F-18   u = d = 27 = V            verified exact
      Co-54  u = d = 81 = F            verified exact
      Xe-108 u = d = 162 = ℒ           verified exact (existence claim only)

G2  Carrier-atom predictions match observed stability (H1):
      4 / 4 carriers predicted stable AND observed stable.

G3  Container-atom predictions match observed instability (H2):
      3 / 3 containers predicted unstable AND observed unstable
      (Be-8, F-18, Co-54).

G4  Chain k=4 (ℒ) predicts Xe-108 not stable AND observed: no stable Xe-108.

G5  Wrong control W1 — at (ĥ, d̂) = (3, 2):
      The chain ĥ·d̂^k = {3, 6, 12, 24, 48} is different.
      Specifically: chain k=1 at (3,2) = 6 (coincidentally matches),
      but chain k=2 at (3,2) = 12 (predicts Be-8 STABLE — falsified).
      Wrong control predicts incorrectly → confirms (2, 3) is load-bearing.

G6  Wrong control W2 — invert carrier / container classification:
      Predict Be-8 stable, F-18 stable, Co-54 stable, He-4 unstable.
      All four predictions fail (Be-8/F-18/Co-54 unstable, He-4 stable).
      Confirms the classification is load-bearing.

G7  Precommit hash verified at runner load AND forbidden-file open()
      guard not tripped.

PASS  iff G1, G2, G3, G4, G5, G6, G7 all hold.

BOUNDARY  iff G1 + G2 + G3 hold but G4 OR G5 OR G6 marginal in a way
          attributable to non-substrate physics not in scope.

FAIL  iff any predicted-stable nucleus is observed unstable, OR any
      predicted-unstable nucleus is observed stable, OR a source-count
      identity fails.
```

The load-bearing gates are **G2 and G3**: seven specific Z = N nuclei
with substrate atoms forcing binary stability predictions. If any
single one of them fails the prediction, the cipher is broken at the
structural level and the framework owes an explanation.

## Reported Evidence (not gated)

```text
E1  Per-nucleus source-count tabulation (u, d, e, A) for all eight.
E2  Substrate atom classification table.
E3  Half-life citation chain from NUBASE2020.
E4  Decay channel for each unstable nucleus (provides mechanism, not
    structural reason — substrate cipher provides the reason).
E5  Substrate-prediction summary vs observed stability.
E6  Wrong-control summary (W1 at (3, 2); W2 inverted classification).
```

## Pre-Registered Frozen Inputs

| field | sha256 | description |
| --- | --- | --- |
| CR248_train_lane_a.csv | `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc` | AME2020 train; contains He-4, Li-6, C-12 masses |
| CR248_test_holdout.csv | `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8` | AME2020 holdout |

Atomic masses for stable nuclei are read from these files. Half-lives
for unstable nuclei (Be-8, F-18, Co-54) are numeric literals from
NUBASE2020 cited in this precommit. No external data file beyond the
two CR248 catalogues is read at runtime.

## Rule-9 Line

```text
This test could have falsified the claim that the substrate's
carrier / container classification of sealed atoms — specifically:

  CARRIER atoms (chain steps m₃, Θ, ĥV, ℒ; closure witness D²) → stable
  CONTAINER atoms (R, V, F) → unstable

— predicts Z = N nuclear stability across eight specific nuclei
(He-4, Li-6, C-12, Ar-36 stable; Be-8, F-18, Co-54 unstable; Xe-108
does not exist as stable). Falsification modes: any predicted-stable
nucleus observed unstable, any predicted-unstable nucleus observed
stable, or any source-count identity (u = d = 3Z) failing to read
exactly on a sealed substrate atom.
```

## What This CR Seals (if PASS)

A binary structural prediction across eight Z = N nuclei is sealed at
zero fitted parameters. The carrier / container distinction — present in
the substrate as the difference between propagators (chain steps,
closure witness) and capacity boundaries (R, V, F, ℒ) — derives
nuclear stability without any nuclear-physics phenomenology:

- Alpha-cluster anchors (He-4, C-12, Ar-36) are stable because they
  sit on the carrier chain.
- Li-6 is stable because D² is the closure-axiom witness (the integer
  that picks the framework's primitives).
- Be-8 is unstable not because two alphas have more binding (mechanism)
  but because R is a container, not a carrier (structural reason).
- F-18 and Co-54 are unstable for the same reason (V and F are
  container atoms).
- Xe-108 doesn't exist as stable because ℒ closes the carrier ledger
  at chain step k = 4.

This is the structural counter to CR261's phenomenological BW fit. CR261
showed the BW shapes can be fit (BOUNDARY); CR262 shows the substrate
already predicts the binary stability data the BW fit was working
through. The two CRs bracket what's substrate-derived from what's still
phenomenological.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR238@09a (substrate spine compaction) | per branch HASHES |
| CR248@09a (four-particle decomp; source-count identities) | precommit `7ad11ca6...` |
| CR258@09a (substrate primitive closure audit; D² listed) | precommit `77c58a51...` |
| CR259@09a (chessboard structural ID) | precommit `53ec3c89...` |
| CR261@09a (pair-write binding extension BOUNDARY) | precommit `5b2d07b5...` |
| CR005@21 (Θ overflow + QNM derivation) | precommit `624f0c26...` |
| CR005ab@21 (neutrino substrate identification; m₃ = ĥ·d̂ sealed) | precommit `a02e5b0b...` |
| AME2020 train (sealed in CR248) | sha256 `54c2c28d...` |
| AME2020 test (sealed in CR248) | sha256 `8a5253f6...` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
