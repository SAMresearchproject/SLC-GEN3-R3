# CR240 Rest-Mass Channel Identification + Binding-Energy Axis — Precommit

**Date:** 2026-06-23
**Classification:** REST_MASS_CHANNEL_IDENTIFICATION (downstream of CR238 substrate spine + CR239 native mass / gravity bridge)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-23 ("lets go option 1" — CR240 neutron-mass channel derivation per the CR239-result next-CR target)
**Status:** PRECOMMITTED before runner execution.

## Scope

> **CR240 tests whether the CR238 typed substrate Q(P) admits a separable rest-mass channel `Q_mass(Z, N) = 4·A·κ` (each nucleon contributing equally), and whether the residual `m_measured − μ_Q·Q_mass` is structurally the C-12-relative binding-energy curve along known nuclear axes.**

The CR239 result identified a single dominant residual axis (`ρ_S(N−Z) = +0.984`) and showed that the `A = Z + N` baseline beats the CR238 substrate Q(P) by 90×. CR240 reads that result structurally:

```text
WC9 in CR239 was not a "trivial baseline beating Q."
WC9 was the typed rest-mass channel that CR238 had left implicit.
```

The CR238 substrate kernel `G(Z, N) = Z·κ + (N − Z)·g` is the **gravitational source-coupling channel** (q_A). The CR240-proposed extension `G_mass(Z, N) = A·κ/α_H = A·κ/2` is the **rest-mass channel**. They are different physical quantities and must use different kernels.

Under this reading:

```text
Q_mass(Z, N)    =  S · G_mass(Z, N)      =  4 · A · κ
m_SAM(P)        =  μ_Q · Q_mass(P)        =  A · u  (exactly, anchored at C-12)
```

CR240 verifies (a) that this kernel reproduces measured atomic mass within sub-percent on the AME2020 Lane A test set, and (b) that the residual `Δm(P) = m_measured(P) − A · u` is structured as the C-12-relative binding-energy curve along known nuclear axes (volume, surface, Coulomb, asymmetry, pairing).

> **CR240 does not modify CR238. The substrate Q kernel remains correct for the gravitational source-coupling channel. CR240 adds a separate, complementary rest-mass kernel.**

## Locked Native Inputs (Inherited; Read-Only)

```text
CR238 substrate spine (read-only):
  ℱ = 81, S = 8, α_H = 2 → D = 3, R = 12
  κ = 7117/768, g = 1/64
  Substrate G(Z, N) = Z·κ + (N − Z)·g  (gravitational source-coupling kernel; unchanged)
  Substrate Q(Z, N) = S · G(Z, N)        (CR238 typed; unchanged)

CR239 anchor (read-only):
  Anchor isotope:  C-12, m = 12.000…u exact (AME definition)
  μ_Q          :  192 u / 7117  (exact rational, derived from C-12 anchor)
```

New kernel introduced in CR240 (the only structural addition):

```text
G_mass(Z, N)   =  A · κ / α_H   =  A · κ / 2     rest-mass carrier kernel
Q_mass(Z, N)   =  S · G_mass(Z, N)               =  4·A·κ
m_SAM(P)       =  μ_Q · Q_mass(P)                =  A · u  (anchored, exact)
```

## Hypothesis Chain Under Test

```text
H1 — Rest-mass kernel identification:
       Q_mass(Z, N) = 4·A·κ reproduces measured atomic mass within precommitted tolerance.

H2 — Substrate-channel separation:
       The CR238 substrate Q(P) and the CR240 rest-mass Q_mass(P) are
       structurally distinct quantities, each measuring a different SAM channel:
         Q(P)      → gravitational source-coupling (q_A)
         Q_mass(P) → inertial / gravitational rest mass
       The difference per nucleon at fixed Z:
         ΔQ(per excess neutron) = Q_mass per excess N − Q_substrate per excess N
                                = 4κ − S·g
                                = 4κ − 1/8
                                = 7093/192   (exact rational)
         after μ_Q             = 7093/7117 u ≈ 0.99663 u

H3 — Binding-energy residual:
       The residual under H1, Δm(P) = m_measured(P) − A · u,
       is structurally the C-12-relative binding-energy curve and tracks
       known nuclear axes (volume, surface, Coulomb, asymmetry, pairing).

H4 — Neutron rest-mass typed expression:
       m_n ≈ μ_Q · 4κ ≈ 1u with a small typed correction.
       Specifically, m_n in u-units lies between
         μ_Q · (4κ − 8g) = 7093/7117 u ≈ 0.99663 u   (substrate-replaced limit)
       and
         μ_Q · 4κ        = 1u                        (rest-mass-only limit)
       with measured m_n = 1.00866 u showing the C-12 binding shift.
```

## Inputs (Hash-Locked at Execution)

```text
CR238 typed spine (read-only):
  CR238_PRECOMMIT.md           =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
  CR238_result.md              =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef

CR239 read-only context (anchor + structural finding):
  CR239_PRECOMMIT.md           =  52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7
  CR239_result.md              =  55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b

CR240 measured isotope masses (re-used from CR239, SHA-locked):
  CR239_measured_isotope_masses.csv  =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
  rows                                 =  51 isotopes (Lane A scored)
  anchor                               =  C-12, m = 12.000…u exact

Free-nucleon rest masses (AME2020 / CODATA, used only in H4 verification):
  m_p_measured  =  1.00727646693 u     (free proton, AME2020)
  m_n_measured  =  1.00866491595 u     (free neutron, AME2020)
  These enter as Lane A reveal-against-frozen-envelope; they do not shape the kernel.
```

## Gate 1 — Rest-Mass Kernel Identification (Algebraic)

Verify the typed identities forced by the locked CR238 spine + C-12 anchor:

```text
G1.1   Q_mass(C-12)  =  4 · 12 · κ          =  48 · 7117 / 768   =  7117/16
G1.2   m_SAM(C-12)   =  μ_Q · Q_mass(C-12)  =  12 u
G1.3   m_SAM(P)      =  μ_Q · 4·A·κ          =  A · u  for every P
G1.4   ΔQ per excess neutron between substrate and rest-mass kernels:
         Q_mass(Z, N) − Q(Z, N) =
            4·A·κ − [Z·8κ + (N−Z)·8g]
          = (Z + N)·4κ − 8Z·κ − 8(N−Z)g
          = (4N − 4Z)κ − 8(N−Z)g
          = (N − Z) · 4·(κ − 2g)
          = (N − Z) · 7093/192    (exact rational)
G1.5   After μ_Q: per excess neutron differential = 7093/7117 u ≈ 0.99663 u
```

Pass condition: all identities hold as exact rationals.

## Gate 2 — Lane A Mass Prediction Under Extended Kernel

Predict `m_SAM(P) = A · u` for every Lane A row in the SHA-locked AME2020 subset. Compute residuals:

```text
Δm(P)  =  m_measured(P)  −  A · u
ε(P)   =  Δm(P) / m_measured(P)
```

Aggregate:

```text
RMS residual ε(P)
Max |ε(P)|
Fraction with |ε| < 0.001     (0.1 %)
Fraction with |ε| < 0.005     (0.5 %)
Fraction with |ε| < 0.01      (1 %)
Subset stats: symmetric (N=Z) vs asymmetric (N≠Z)
```

This is operationally identical to CR239's WC9 with the canonical anchor and μ_Q already locked.

## Gate 3 — Binding-Energy Axis Identification

The residual Δm(P) should track the C-12-relative binding-energy curve. Test Spearman rank correlation `ρ_S` and linear fit between `Δm(P)` and each of the following nuclear-structure axes:

```text
(a) A             total nucleon count
(b) Z             proton count
(c) N             neutron count
(d) N − Z         neutron excess
(e) (N − Z)²      asymmetry squared (Bethe-Weizsäcker asymmetry term)
(f) A^(2/3)       Bethe-Weizsäcker surface term
(g) Z² / A^(1/3)  Bethe-Weizsäcker Coulomb term
(h) Z(Z−1) / A^(1/3)   Coulomb (more standard form)
(i) δ_pairing     pairing term proxy: +1 (Z even, N even), 0 (Z+N odd), −1 (Z odd, N odd)
(j) magic_distance distance to nearest doubly-magic configuration
```

For each axis, report `ρ_S` and `r²`. The binding-energy curve is **structured** if multiple axes show `|ρ_S| > 0.5` consistent with the Bethe-Weizsäcker form (especially asymmetry `(N − Z)²` and surface `A^(2/3)`).

## Gate 4 — Per-Nucleon Free Mass Derivation Attempt

Test the precommitted typed candidate expressions for the per-nucleon free mass scale (`m_p_native`, `m_n_native`, `m(H-1)`) and the small-splitting diagnostic scale (`m_n − m_p` and related splittings) against AME2020 measured values. **The candidate set is locked here; the runner does NOT add, remove, or promote candidates after seeing the data.**

### Candidate set (locked)

| ID | Candidate (typed) | Numerical value (u) | Targeted measurement |
|---|---|---|---|
| C0 | `μ_Q · 4κ` | 1.0000000000 | per-nucleon scale at C-12 anchor |
| C1 | `μ_Q · (4κ − 8g)` | 7093/7117 ≈ 0.9966281 | substrate-replaced excess-neutron |
| C2 | `μ_Q · (4κ + 8g)` | 7141/7117 ≈ 1.0033720 | substrate-additive excess-neutron |
| C3 | `μ_Q · 4κ · (1 + g)` | 65/64 = 1.0156250 | binding-curvature linear-in-g |
| C4 | `μ_Q · 4κ · (1 + 1/(D²·S))` | 73/72 ≈ 1.0138889 | binding-curvature D-S typed |
| C5 | `μ_Q · 4κ · (1 + 1/R²)` | 145/144 ≈ 1.0069444 | **cycle-budget surface unit** |
| C6 | `μ_Q · 4κ · (1 + g/α_H)` | 129/128 = 1.0078125 | **face-halved neutron-unit correction** |
| C7 | `μ_Q · 4κ · (1 + 1/M)` | 127/126 ≈ 1.0079365 | **matter-capacity reciprocal correction** |
| C8 | `μ_Q · 4κ · (1/(S·ℒ))` | 1/1296 ≈ 0.0007716 | **closed-ledger split diagnostic scale** (not a standalone nucleon-mass candidate; compared to small splittings such as m_n − m_p) |

### Structural sources

```text
C0 — C-12 per-nucleon scale (anchor identity)
C1 — substrate-channel value if rest-mass channel replaces substrate per excess neutron
C2 — substrate-channel value if rest-mass channel adds to substrate per excess neutron
C3 — binding correction at the neutron-unit substrate-coupling g
C4 — binding correction at the dimensional / split-typed scale 1/(D²·S) = 1/72
C5 — binding correction at the cycle-budget surface scale 1/R² = 1/144
       (R² = 144 is the typed cycle budget; smallest typed surface correction)
C6 — binding correction at the face-halved neutron-unit g/α_H = 1/(2·S²) = 1/128
       (assigns the neutron-unit per face — tests whether the lift is a face-halved
        neutron-unit effect)
C7 — binding correction at the matter-capacity reciprocal 1/M = 1/126
       (M = ℒ − 2Θ = 126 is the typed matter capacity from CR229 / CR238;
        tests whether the lift is distributed across full retained matter)
C8 — split-weighted closed-ledger diagnostic 1/(S·ℒ) = 1/1296
       (diagnostic scale for proton/neutron or hydrogen/neutron small splittings;
        must NOT be used to tune μ_Q or alter the mass baseline)
```

### Reveal targets

For each candidate `Cx` ∈ {C0, ..., C7} (the standalone nucleon-mass candidates) compute residuals against:

```text
m_p_measured           =  1.00727646693 u   (free proton, AME2020 / CODATA)
m_n_measured           =  1.00866491595 u   (free neutron, AME2020 / CODATA)
m(H-1)_measured        =  1.00782503207 u   (hydrogen-1 atomic mass, AME2020)
m_avg_lane_a_per_A     =  mean( m_measured(P) / A(P) ) over Lane A non-anchor
```

For C8 compute residual against splittings:

```text
m_n − m_p              =  0.00138844902 u
m(H-1) − m_p           =  0.00054856514 u  (≈ electron mass + binding)
1u − μ_Q · (4κ − 8g)   =  24/7117 u ≈ 0.00337 u  (CR239 per-excess-neutron substrate contribution)
```

### Deviation metric

```text
deviation(Cx, target)  =  | Cx_value − target_value | / target_value
```

### Pass thresholds (locked)

- **C-strict**: deviation < 0.001 (0.1 %)
- **C-loose**:  deviation < 0.01  (1 %)

For each candidate–target pair, report whether C-strict and C-loose clear.

### Candidate-scoring rule (Locked Hygiene)

```text
1. All candidates C0–C8 must be scored and reported in CR240_candidate_typed_values.csv.
2. The runner may identify the lowest-residual candidate per target, but
   NO candidate may be promoted to theorem-grade solely from this dataset.
3. A candidate becomes a CR241 target only if (a) it is selected by CR240,
   AND (b) it survives a separate holdout or post-evaluation challenge run as
   a downstream CR (CR241+).
4. The result text and summary JSON must NOT claim that a candidate was
   discovered after seeing the data. Candidates are precommitted here.
```

### Required reporting columns (Locked)

`CR240_candidate_typed_values.csv` must contain at minimum:

```text
candidate_id
formula
typed_source
canonical_value_u
residual_vs_m_p
residual_vs_m_n
residual_vs_H1
residual_vs_avg_lane_a_nucleon
strict_pass_m_p, strict_pass_m_n, strict_pass_H1, strict_pass_avg
loose_pass_m_p, loose_pass_m_n, loose_pass_H1, loose_pass_avg
```

For C8 (diagnostic), substitute splitting-target columns:

```text
residual_vs_m_n_minus_m_p
residual_vs_H1_minus_m_p
residual_vs_one_u_minus_substrate_excess
```

## Wrong Controls (Precommitted)

### WC1 — Substrate kernel as rest-mass kernel (the failed baseline)

Re-run Gate 2 with `Q_mass(P) := Q_substrate(P) = S·[Z·κ + (N−Z)·g]`. This is the CR239 baseline. Expected: degradation by ~90× vs the CR240 extended kernel (matching the CR239 result).

### WC2 — He-4 anchor instead of C-12

Recompute μ_Q from He-4 anchor: `μ_Q^He4 = m(He-4) / Q_mass(He-4) = 4.00260325413 u / 16κ`. Then run Gate 2 with `μ_Q^He4`. Compare RMS to canonical μ_Q. If the rest-mass kernel is correct, μ_Q should be (nearly) invariant under anchor swap. Expected: `|μ_Q^He4 / μ_Q − 1| < 0.001` to within C-12 vs He-4 binding-energy difference.

### WC3 — Random per-nucleon mass scale

Set each nucleon's mass to `(1 + δ) · u` where `δ` is a seeded random perturbation (seed 20260623) with mean 0, std 0.05. Predict masses. Expected: degradation — the structurally locked C-12-anchored 1u scale should beat random perturbations.

### WC4 — Per-nucleon mass = constant ≠ u

Test `m = A · c` for `c ∈ {0.5u, 1.5u, 2u}`. Expected: degradation — only c=u (anchored at C-12) matches.

### WC5 — Mixed kernel: m = Z·m_p + N·m_n (no binding)

Use experimental m_p and m_n: predict `m_no_binding(P) = Z · m_p + N · m_n`. Compare to measured. Residual = binding energy (negative). Expected: residual to track Bethe-Weizsäcker form with `ρ_S(asymmetry) > 0.5` etc. — This wrong control is actually a check that the binding-energy axis IS the residual structure (since WC5 makes binding explicit).

### WC6 — Random axis label shuffle

Shuffle the axis labels in Gate 3 (e.g., feed (N−Z) values where A is expected). The reported Spearman `ρ_S` for each "axis" should drop to noise (|ρ_S| < 0.3). This tests Gate 3's axis-attribution integrity.

## Predictions (Precommitted)

### Block A — Deterministic algebraic identities

- **P1**: `Q_mass(C-12) = 7117/16` (exact).
- **P2**: `m_SAM(C-12) = 12 u` (exact, anchor identity).
- **P3**: `Q_mass(Z, N) − Q_substrate(Z, N) = (N − Z) · 7093/192` for every (Z, N) (exact rational identity).
- **P4**: `m_SAM(P) = A · u` for every Lane A row (exact, anchored).

### Block B — Empirical regrade (outcome NOT precommitted; methodology is)

- **P5**: Lane A residual `ε(P)` distribution under the extended kernel. Expected outcome (NOT a verdict trigger): RMS ε ≈ 0.002 (matching CR239 WC9).
- **P6**: Gate 3 Spearman correlations on 10 axes. Expected (NOT a verdict trigger): at least one Bethe-Weizsäcker axis (asymmetry, surface, or Coulomb) shows |ρ_S| > 0.5.
- **P7**: Gate 4 candidate-vs-measured deviations for **C0–C8** against m_p, m_n, m(H-1), and the average Lane A per-nucleon baseline (C8 against splittings). Recorded; no verdict-trigger requirement that any candidate clear C-strict. The candidate-scoring rule prevents any post-data promotion.
- **P8**: WC1 (substrate kernel as rest mass) degrades by ≥ 50× on Lane A RMS vs extended kernel.
- **P9**: WC2 (He-4 anchor) `|μ_Q^He4 / μ_Q − 1| < 0.005`.
- **P10**: WC5 (Z·m_p + N·m_n no-binding kernel) residual tracks Bethe-Weizsäcker asymmetry term with `|ρ_S((N−Z)², residual)| > 0.5`.

## Pass Condition (Precommitted Verdict Spectrum)

```text
STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED  iff  ALL of:
  (S1)  Gate 1 algebraic identities all hold exactly.
  (S2)  Gate 2 Lane A RMS ε < 0.005 (0.5 %) on the extended kernel.
  (S3)  Gate 3: at least one of {asymmetry (N−Z)², surface A^(2/3), Coulomb Z²/A^(1/3)}
        has |ρ_S| > 0.5 — the residual is the binding-energy curve.
  (S4)  Gate 4: at least one candidate Cx ∈ {C0, C1, C2, C3, C4, C5, C6, C7}
        clears C-strict (< 0.1 %) for at least one of {m_p, m_n, m(H-1), avg per-nucleon}.
        C8 is a diagnostic scale and does NOT participate in S4 (it is reported only against splittings).
  (S5)  WC2 (He-4 anchor) gives |μ_Q^He4 / μ_Q − 1| < 0.005.

BOUNDARY_CR240_REST_MASS_CHANNEL_WITH_BINDING_CURVE  iff  ALL of:
  (B1)  Gate 1 algebraic identities all hold exactly.
  (B2)  Gate 2 Lane A RMS ε < 0.01 (1 %) on the extended kernel.
  (B3)  Gate 3 residual is structurally identified (≥ 1 axis with |ρ_S| > 0.5),
        but Gate 4 STRONG_PASS condition (S4) is NOT met —
        meaning the rest-mass channel is identified, but the per-nucleon free mass
        and binding-curve form are next-CR targets.
  (B4)  WC2 (He-4 anchor) gives |μ_Q^He4 / μ_Q − 1| < 0.01.

FAIL_CR240_REST_MASS_CHANNEL  iff  ANY of:
  (F1)  Gate 1 algebraic identity fails.
  (F2)  Gate 2 Lane A RMS ε > 0.05 (5 %) — extended kernel does not close.
  (F3)  Gate 3: NO axis has |ρ_S| > 0.5 — residual is unstructured.
  (F4)  WC2: anchor swap shifts μ_Q by > 5 % — μ_Q is not a stable bridge.
```

Verdict precedence: STRONG > BOUNDARY > FAIL.

## Disallowed Claims (Locked)

The runner / result must NOT claim any of:

```text
"CR240 falsifies the CR238 substrate kernel."  (it does not; CR238's substrate Q kernel is
                                                left untouched. CR240 adds a separate,
                                                complementary rest-mass channel.)
"CR240 derives m_n exactly."                    (it does not; at most one precommitted candidate
                                                 may match within C-strict, and even then the
                                                 candidate must survive a separate holdout
                                                 challenge before any theorem-grade claim.)
"Q(P) and Q_mass(P) are the same quantity."    (they are not — substrate-coupling channel vs
                                                 rest-mass channel.)
"Binding energy is reduced to typed primitives."  (CR240 only identifies the axis; full
                                                   derivation is future CR work.)
"A candidate was discovered after seeing the data."  (the candidate set C0–C8 is locked in this
                                                       precommit; no post-data promotion is allowed
                                                       per the candidate-scoring rule.)
```

## K-Gate Audit (Precommitted Pre-Execution)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | EXPLICIT + CONTAINED. Single shaping anchor `m(C-12) = 12 u`. AME2020 measured masses are the reveal-against-frozen-envelope. Free nucleon masses (m_p, m_n) appear only in Gate 4 / WC5 reveal positions. |
| K2 | Falsification | Pre-stated falsifiers F1–F4 (below) and verdict tier thresholds. |
| K3 | Target hygiene | Hypothesis chain, four gates, six wrong controls, three verdict tiers, disallowed-claims list committed BEFORE the runner reads measured masses. |
| K4 | Typed inputs | CR238 typed spine (κ, g, S) + CR239 anchored μ_Q + SHA-locked AME2020 subset. Free nucleon masses cited as Lane A reveal only. No new free parameter. |
| K5 | Reproduction on demand | `python CR240_runner.py` deterministically reproduces every gate, wrong control, candidate test, and verdict assignment. |

## Falsifiers (Made Explicit)

- **F1**: Algebraic identity G1.1 — G1.5 fails as an exact rational (test design itself broken).
- **F2**: Gate 2 extended-kernel RMS residual on Lane A is > 5 % — rest-mass-channel identification is wrong.
- **F3**: Gate 3 finds no axis with |ρ_S| > 0.5 — the residual is unstructured (no binding-energy curve identified).
- **F4**: WC2 anchor swap (C-12 vs He-4) shifts μ_Q by > 5 % — μ_Q is not a stable dimensional constant; the bridge is a soft fit.
- **F5**: Any disallowed claim appears in result.md or summary.json (locked-claim violation).

## Allowed Claims Under Each Verdict Tier

```text
STRONG_PASS allowed claim:
  "SAM has two distinct mass-related channels: the substrate gravitational
  source-coupling channel Q_substrate(P) = S·[Z·κ + (N−Z)·g] (CR238, untouched),
  and the rest-mass channel Q_mass(P) = 4·A·κ (CR240). Each nucleon contributes
  equally to rest mass at the C-12-anchored scale 4κ·μ_Q = 1u. The CR240 extended
  kernel reproduces measured atomic mass within 0.5 % across the AME2020 Lane A
  test set, the residual is structurally the C-12-relative binding-energy curve,
  and the per-nucleon free mass m_p or m_n is reproduced by a typed expression
  in {ℱ, S, α_H} within 0.1 %."

BOUNDARY_PASS allowed claim:
  "SAM has two distinct mass-related channels: the CR238 substrate Q(P) for
  gravitational source-coupling and the CR240 rest-mass channel Q_mass(P) = 4·A·κ
  for inertial / gravitational rest mass. The rest-mass kernel reproduces measured
  atomic mass within 1 % across AME2020 Lane A. The Lane A residual under this
  kernel is structurally the C-12-relative binding-energy curve, with at least
  one Bethe-Weizsäcker axis showing |ρ_S| > 0.5. The per-nucleon free mass
  (m_p, m_n) and the explicit binding-energy form are the next-CR targets;
  CR240 identifies the channel and the axis, not the full derivation."

FAIL allowed claim:
  "The proposed CR240 extended kernel Q_mass(P) = 4·A·κ does not close the
  rest-mass bridge to AME2020 within the precommitted tolerance, OR the residual
  is unstructured (no Bethe-Weizsäcker axis identified), OR the anchor swap
  shifts μ_Q substantively. The substrate-vs-rest-mass channel separation
  proposed in CR240 is not supported by the test."
```

## Output Files (Locked Manifest)

```text
CR240_NEUTRON_REST_MASS_CHANNEL/
  CR240_PRECOMMIT.md                          (this file)
  CR240_runner.py                             (deterministic runner)
  CR240_summary.json                          (machine-readable verdict)
  CR240_result.md                             (human-readable result)
  CR240_extended_kernel_predictions.csv       (Gate 2 per-row output)
  CR240_residual_axis_correlations.csv        (Gate 3 Spearman per axis)
  CR240_candidate_typed_values.csv            (Gate 4 candidates vs measured)
  CR240_wrong_controls.csv                    (WC1–WC6 results)
  CR240_input_manifest.csv                    (file SHAs)
  HASHES.txt                                  (final all-artifact SHAs)
```

## Upstream Sources (Hash-Locked)

```text
CR114_result.md                                =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md                                =  635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR221_result.md                                =  2fc932adda9df4e3002b6a996d321a072a009722801099747fae552c393fbeef
CR222_result.md                                =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md                                =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR230_result.md                                =  3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR232_result.md                                =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
CR233_result.md                                =  55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895
CR238_PRECOMMIT.md                             =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md                                =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_PRECOMMIT.md                             =  52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7
CR239_result.md                                =  55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR239_measured_isotope_masses.csv              =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
```

## What CR240 Does

1. Locks the rest-mass kernel proposal: `Q_mass(Z, N) = 4 · A · κ`, `m_SAM(P) = μ_Q · Q_mass(P) = A · u`.
2. Gate 1: verifies the algebraic identities G1.1–G1.5 as exact rationals.
3. Gate 2: predicts measured atomic mass under the extended kernel for the 50 non-anchor Lane A rows; reports residuals.
4. Gate 3: tests the residual against 10 nuclear-structure axes (Bethe-Weizsäcker volume, surface, Coulomb, asymmetry, pairing, magic-distance, A, Z, N, N−Z) via Spearman rank correlation.
5. Gate 4: tests **9 precommitted typed candidates C0–C8** against AME2020 measured values for `m_p`, `m_n`, `m(H-1)`, the average Lane A per-nucleon baseline (C0–C7), and small splittings such as `m_n − m_p` (C8 diagnostic only). The candidate-scoring rule prevents any post-data promotion to theorem-grade; CR241 must run a separate holdout challenge before any candidate is theorem-claimed.
6. Runs 6 wrong controls.
7. Assigns verdict tier per locked thresholds.

## What CR240 Does NOT Do

- Does NOT modify CR238's substrate Q kernel; the substrate channel is left untouched.
- Does NOT row-by-row fit m_n or m_p.
- Does NOT introduce binding-energy free parameters; it only identifies the axis the binding-energy term must run on.
- Does NOT extend to a full Bethe-Weizsäcker derivation (next CR territory if BOUNDARY_PASS).
- Does NOT touch composition-level gravity (Gate 5 of CR239 remains reserved).

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. The hypothesis chain, four gates, six wrong controls, nine precommitted typed candidates (C0–C8), verdict thresholds, disallowed-claims list, K-gates, and falsifiers are frozen before runner execution.

If any sealed upstream CR is later regraded, CR240 must be re-examined.

---

**Precommit drafted by:** Claude (Opus 4.7, 1M context), at Sean's direction, following the CR239 result's next-CR target
**Sealed by:** Sean Brady, 2026-06-23 [pending Sean's seal]
**Arc relation:** Downstream of CR238 + CR239; identifies a separable rest-mass channel in the SAM ontology
**New kernel introduced:** Q_mass(Z, N) = 4·A·κ (rest-mass carrier; complementary to CR238 substrate Q)
**Verdict spectrum:** STRONG_PASS / BOUNDARY_PASS / FAIL
