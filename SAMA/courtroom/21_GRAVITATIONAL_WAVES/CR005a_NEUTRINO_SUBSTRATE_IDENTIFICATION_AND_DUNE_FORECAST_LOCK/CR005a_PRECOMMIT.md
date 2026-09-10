# CR005a — Neutrino Mass Spectrum Substrate Identification + DUNE Forecast Lock

**Branch:** 21_GRAVITATIONAL_WAVES (cross-domain — neutrino sector via partition-algebra framework)
**Classification:** STRUCTURAL_IDENTIFICATION_CR + FORECAST_LOCK_CR
**Sealed by:** Sean Brady, 2026-06-29
**Upstream:** CR001@20 (sealed PASS; mass pattern locked + empirical verification), CR005@21 (Θ-overflow + partition-algebra + closure-axiom framework), CR004@21 (discrimination map ranking)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## What this CR seals

Two things, neither of which is in CR001@20 already:

1. **Substrate-physics identification of the three neutrino mass-squared
   eigenvalues** in CR005's partition-algebra and Θ-unit framework:
   - `m₁² = 1` at partition-algebra position `(i, j) = (0, 0)` (ground)
   - `m₂² = ĥ = 2` at position `(1, 0)` (binary readout / bigrade)
   - `m₃² = (ĥ·d̂)² = 36 = ĥ·Θ = 2Θ` at position `(2, 2)` — **the second
     element of the partition-algebra overflow set `{18, 24, 36, 72}`**

   The heaviest neutrino mass-squared is identified as `2Θ` — exactly
   twice the GW carrier overflow. The neutrino sector and the GW
   sector share the same load-bearing Θ structure across two different
   branches.

2. **Formal forecast lock for DUNE + Hyper-K precision measurement of
   `Δm²₃₁/Δm²₂₁`.** SAM commits to the value `35` exactly. Current best
   fit `33.895 ± ~0.70` (NuFit 5.2; σ ≈ 2.06%) puts SAM at ~1.6σ from
   measurement today. DUNE + Hyper-K projected σ ≈ 0.5% on the ratio →
   ~6σ discrimination of SAM's `35` vs current fit `33.895`. The
   discrimination resolves by approximately 2030.

## What this CR does NOT seal

- A first-principles derivation of WHY those three specific partition-
  algebra positions correspond to the three neutrino mass eigenstates.
  CR001@20 locked the substrate scaling rule `m_i ∝ {1, √ĥ, ĥ·d̂}` by
  declaration and verified empirically. CR005a places this in the
  CR005 framework and identifies cross-branch structural connections,
  but does not derive the position selection from first principles.
- Mass mechanism (Dirac vs Majorana). Deferred until 0νββ experiments
  decide.
- PMNS mixing angles. CR002@20 / CR003@20 territory.
- Mass ordering selector. CR002@20 territory.
- Absolute eV scale of the lightest mass. Anchored from external
  `Δm²₃₁ = 2.515e-3 eV²` (PDG 2024); not an internal SAM derivation.

## Inputs (read-only, sealed upstream)

```text
CR001@20 sealed PASS:
  m_1 / base_eV = 1
  m_2 / base_eV = √ĥ = √2
  m_3 / base_eV = ĥ·d̂ = 6
  Δm²₃₁ / Δm²₂₁ = (m_3² − m_1²) / (m_2² − m_1²) = 35 (closed form)
  measured = 33.895 (PDG 2024 / NuFit 5.2)
  3.26% deviation → PASS @ 10% gate
  Σmν = 71.3 meV < 0.12 eV Planck bound → PASS

CR005@21 sealed PASS:
  Bounded partition algebra: { ĥ^i · d̂^j : i ∈ [0..d̂], j ∈ [0..d̂−1] }
  At (ĥ, d̂) = (2, 3): 12 grid cells
  Inside R = 12: bigrade alphabet {1, 2, 3, 4, 6, 8, 9, 12} (CR218 sealed)
  Overflow set: {18, 24, 36, 72}
  First overflow = Θ = 18 (the carrier; CR229 sealed)
  Substrate measured in Θ-units: M = 7Θ, R² = 8Θ = SΘ, ℒ = 9Θ = (S+1)Θ
  Closure axiom: d̂^(d̂−1) = S+1 = 9 at d̂=3 unique (CR238 sealed)

External anchors (numeric literals, declared):
  Δm²₃₁_PDG = 2.515e-3 eV²  (PDG 2024 normal ordering)
  Δm²₂₁_PDG = 7.42e-5 eV²   (PDG 2024 global fit)
  ratio_measured = 2.515e-3 / 7.42e-5 = 33.895 (PDG)
  current σ_ratio ≈ 0.70  (~2.06% relative; NuFit 5.2)
  DUNE projected σ_ratio ≈ 0.17  (~0.5% relative; DUNE TDR 2020)
  Hyper-K projected similar; joint σ slightly tighter
  Σmν Planck bound = 0.12 eV (P2 falsifier from CR001@20)
```

## Pre-registered verifiable claims

### A. Substrate identification of mass-squared eigenvalues

**A1.** `m₁² = base_eV² · 1`. Partition-algebra position `(0, 0)`.
The substrate quantity is the unit ground (smallest bigrade element).

**A2.** `m₂² = base_eV² · ĥ = 2·base_eV²`. Partition-algebra position
`(1, 0)`. The substrate quantity is the binary readout (second-smallest
bigrade element).

**A3.** `m₃² = base_eV² · (ĥ·d̂)² = 36·base_eV²`. Partition-algebra
position `(2, 2)`. The substrate quantity is the square of position
`(1, 1)`. The numerical value `36` is the second element of the
partition-algebra overflow set `{18, 24, 36, 72}`.

**A4.** Cross-branch identity: `m₃² = 36 = 2Θ = ĥ · Θ`. The heaviest
neutrino mass-squared is exactly twice the GW carrier Θ — direct
structural connection across CR001@20 (neutrino) and CR229@09a /
CR001@21 (GW carrier).

### B. Mass-squared progression as substrate multiplicative chain

**B1.** Define the substrate-quantity sequence `s = {1, ĥ, ĥ·Θ}`.
The three neutrino mass-squareds equal `base_eV² · s`.

**B2.** Each step in the sequence multiplies by one primitive factor:
- Step 1→2: multiply by ĥ (introduces binary readout)
- Step 2→3: multiply by Θ (introduces carrier overflow)

**B3.** The denominator structure of the closure-axiom comparison:
`m₃²/m₂² = Θ` and `m₂²/m₁² = ĥ`. Substrate reading: the neutrino mass
ladder rises by one binary-readout factor and one carrier factor.

### C. Splittings derivation in Θ-unit form

**C1.** `Δm²₂₁ = m₂² − m₁² = base_eV² · (ĥ − 1) = base_eV² · 1` at ĥ=2.

**C2.** `Δm²₃₁ = m₃² − m₁² = base_eV² · ((ĥ·d̂)² − 1) = base_eV² · 35`
at canonical substrate.

**C3.** **Splitting ratio in Θ-unit form**:
```text
Δm²₃₁ / Δm²₂₁  =  ((ĥ·d̂)² − 1) / (ĥ − 1)
                =  (ĥ·Θ − 1) / (ĥ − 1)               [Sean's identity: (ĥ·d̂)² = ĥ·Θ]
                =  (2Θ − 1) / (ĥ − 1)                  [at ĥ = 2]
                =  35 / 1
                =  35
```

**C4.** Bit-identical to CR001@20 sealed value `35`.

### D. eV scale anchor (external; inherited from CR001@20)

**D1.** `base_eV = sqrt(Δm²₃₁_PDG / 35) = sqrt(2.515e-3 / 35)
= sqrt(7.1857e-5) = 0.0084768 eV`.

**D2.** Mass eigenstates:
- `m₁ = 0.008477 eV`
- `m₂ = base_eV · √ĥ = 0.011988 eV`
- `m₃ = base_eV · ĥ·d̂ = 0.050861 eV`

**D3.** Total `Σmν = m₁ + m₂ + m₃ = 0.07133 eV ≈ 71.33 meV`. Below
Planck 0.12 eV bound (per CR001@20 P2 falsifier).

### E. Cross-check against CR001@20 sealed values

**E1.** `ratio_SAM = 35` matches CR001@20 sealed.
**E2.** `Σmν_SAM = 71.33 meV` matches CR001@20 sealed.
**E3.** `m₁, m₂, m₃` values match CR001@20 sealed to 4 decimal places.

### F. Forecast lock (the load-bearing new content)

**F1.** SAM commits to `Δm²₃₁/Δm²₂₁ = 35` with zero substrate-side
uncertainty (closed-form rational).

**F2.** Current best fit (NuFit 5.2 / PDG 2024): `33.895 ± 0.70`. SAM
deviation = `(35 − 33.895)/33.895 = 3.26%`. Current discrimination =
`|35 − 33.895|/0.70 = 1.58σ` (NOT yet discriminating).

**F3.** DUNE projected ratio σ: 0.5% relative ≈ `0.17` absolute on a
central value near 34. SAM-vs-current discrimination at DUNE precision:
`|35 − 33.895|/0.17 = 6.5σ`.

**F4.** Hyper-Kamiokande projected ratio σ: similar to DUNE; joint
DUNE+HK σ ≈ 0.3% ≈ `0.10`. SAM-vs-current discrimination at joint
precision: `|35 − 33.895|/0.10 = 11σ`.

**F5.** Falsification criteria for SAM ratio = 35:
- If DUNE measures `r_DUNE` with `|35 − r_DUNE|/σ_DUNE > 3`, **SAM is
  falsified** at the ratio level.
- If DUNE measures `r_DUNE` with `|35 − r_DUNE|/σ_DUNE < 1`, **SAM is
  strongly confirmed** at the ratio level.

**F6.** Timeline: DUNE first data ~2028, full sensitivity ~2032.
Hyper-K first data ~2027. Discrimination ~2030.

## Verdict tree

```text
PASS:
  Every claim A1-A4, B1-B3, C1-C4, D1-D3, E1-E3, F1-F6 verified to
  exact rational arithmetic and consistency with CR001@20 sealed values.
  The substrate-identification + forecast-lock content is sealed and
  ready for the DUNE measurement window.

FAIL:
  Any single arithmetic or identity claim fails. Indicates either
  (i) CR001@20 misquoted; or (ii) framework misapplication.

(No BOUNDARY band — these are exact rationals or sealed-value lookups.)
```

## Substrate-physics reading of the cross-branch connection

```text
GW sector (CR001@21):
  E_GW / (M_total · c²)  ≤  Θ / R²  =  1 / 8       (cap on radiated fraction)

GW sector (CR005@21):
  ω_R · M               =  (Θ · d̂) / R²  =  3 / 8  (ringdown freq = cap × d̂)

Neutrino sector (CR005a):
  m₃² / base_eV²       =  ĥ · Θ  =  2Θ  =  36     (heaviest mass² = ĥ × Θ)

The same Θ appears in three structurally different roles:
  - Carrier of GW radiation (Θ/R² = 1/8 cap)
  - Frequency setter for ringdown ((Θ·d̂)/R² = 3/8)
  - Mass-squared scale for heaviest neutrino (ĥ·Θ = 2Θ)

This is cross-domain atomic reuse, now extended from the GW branch
into the neutrino sector via the heaviest mass-squared. The "carrier"
identity of Θ is not exclusive to gravity — Θ enters the neutrino
mass spectrum at the heaviest eigenstate.
```

## What CR005a opens

- **CR005a-followup**: substrate-physics derivation of WHY neutrinos
  inhabit positions `(0,0)`, `(1,0)`, `(2,2)` specifically (rather than
  other triples). Open question.
- **CR006**: formal LISA forecast lock for the QNM frequency (analogous
  forecast structure to CR005a's DUNE lock). The two together — DUNE
  ~2030 and LISA ~2035 — give SAM two falsifiable forward predictions
  with confirmed test paths in the next decade.
- **CR-Θ-cross-domain**: catalog every appearance of Θ across sealed
  CRs to confirm the carrier identity holds universally. Already
  partially in CR005's structural reading.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR001@20 precommit | per HASHES.txt of 20 branch |
| CR001@20 result.md | per HASHES.txt of 20 branch |
| CR005@21 precommit (Θ-overflow + QNM derivation) | `624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b` |
| CR005@21 runner | `4276a195a37645d5f966af3a155ff4478b368057e936b485d92f1b4ff06fc424` |
| CR005@21 result | `d21c4e16b5bd4471f158c4ec19d617c11c133f89937eb33a95c0993397a1e6ec` |
| CR004@21 discrimination map | `e519e7c5b8be99540c5c6984079e91f4e56b524d9b9c87e43baabd3f5f61933a` |
| CR229@09a inclusion-exclusion | per HASHES.txt of 09a |
| CR238@09a typed spine + closure axiom | per HASHES.txt of 09a |
| Volume I substrate doc | `ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b` |
| stewardship | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
