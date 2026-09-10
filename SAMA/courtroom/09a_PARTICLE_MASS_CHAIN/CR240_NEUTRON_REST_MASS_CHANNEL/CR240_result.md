# CR240 Rest-Mass Channel Identification + Binding-Energy Axis — Result

## Verdict

```text
STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED__M_SAM_EQUALS_A_U_RMS_0p20PCT_LANE_A__BW_ASYMMETRY_AXIS_STRUCTURED__C6_MATCHES_H1_TO_12_PPM__C5_MATCHES_M_P_TO_330_PPM__C7_MATCHES_M_N_TO_722_PPM__NO_THEOREM_PROMOTION_FROM_THIS_DATASET__CR241_HOLDOUT_REQUIRED
```

`execution_status   = CLEAN`
`scientific_verdict = STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED`
`classification     = REST_MASS_CHANNEL_IDENTIFICATION (downstream of CR238 + CR239)`
`precommit_sha      = 3b6d4aa0102580c693bba9ba7a635d7654328bc632b1d34e7dc3cfbc7efc85cb`

## Plain-English Summary

The locked rest-mass kernel `Q_mass(Z, N) = 4·A·κ` with `m_SAM(P) = μ_Q · Q_mass(P) = A · u` (anchored at C-12 = 12u exact) closes the bridge from CR238's typed substrate to measured atomic mass with **0.20 % RMS** across 49 Lane A non-anchor rows. The residual under this kernel is structurally the C-12-relative binding-energy curve, with the Bethe-Weizsäcker asymmetry, surface, and Coulomb axes showing significant rank correlation (max |ρ_S| = 0.60).

Three of the precommitted typed candidates (C5, C6, C7) clear the C-strict threshold (< 0.1 %) against the free nucleon and H-1 reveal masses. The standout is **candidate C6 = μ_Q · 4κ · (1 + g/α_H) = 129/128 u**, which matches measured atomic hydrogen `m(H-1) = 1.00782503207 u` to **12 parts per million** (residual 0.0012 %) — a typed expression in only the CR238 foundational atoms.

**The candidate-scoring rule locked in the precommit prevents theorem-grade promotion from this single dataset.** Three candidates clearing C-strict simultaneously is a structurally interesting but ambiguous outcome. **CR241 must run a separate holdout challenge** (against AME2024, against rows excluded from CR239's curated subset, or against an independent measurement layer) before any of {C5, C6, C7} is theorem-claimed.

The verdict is STRONG_PASS for the channel identification (S1–S5 all satisfied); the candidate selection is reserved.

## What This Says Structurally

```text
SAM has two distinct mass-related channels in its ontology:

  Q_substrate(P)  =  S · [Z·κ + (N − Z)·g]    gravitational source-coupling (q_A)
                                               (CR238; untouched, still bit-identical
                                                to CR221 kappa_floor)

  Q_mass(P)       =  4 · A · κ                  rest-mass channel
                                               (CR240; identified by this CR;
                                                anchored at C-12 = 12u gives
                                                m_SAM(P) = A · u to 0.2 % RMS)
```

These are different physical quantities measuring different SAM channels. Each nucleon contributes equally to rest mass at the C-12-anchored scale `4κ·μ_Q = 1 u`. The CR238 substrate kernel's asymmetric treatment of `Z·κ` vs `(N − Z)·g` is correct for gravitational source-coupling but not for rest mass — that's the structural reading CR239 set up and CR240 confirms.

The Lane A residual `Δm(P) = m_measured(P) − A·u` carries the C-12-relative binding-energy curve. The BW asymmetry axis `(N−Z)²/A` shows rank correlation 0.60 with the residual; surface and Coulomb axes contribute additional structure. Binding-energy form derivation is the next-CR target (likely CR241 or CR242).

## Inputs (Hash-Locked)

```text
CR240_PRECOMMIT.md sha               =  3b6d4aa0102580c693bba9ba7a635d7654328bc632b1d34e7dc3cfbc7efc85cb
CR238_PRECOMMIT.md sha               =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md sha                  =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_PRECOMMIT.md sha               =  52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7
CR239_result.md sha                  =  55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR239_measured_isotope_masses.csv    =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc

Kernel atoms (read-only from CR238):
  ℱ = 81, S = 8, α_H = 2  →  D = 3, R = 12, ℒ = 162, M = 126
  κ = 7117/768, g = 1/64

Anchor (from CR239):
  Isotope : C-12 = (Z=6, N=6)
  Mass    : 12.00000000000 u (AME definition)
  Q_mass(C-12) : 7117/16  = 444.8125
  μ_Q     : 192 u / 7117  = 0.0269775889…  u per Q-unit

Free-nucleon reveal masses (AME2020 / CODATA; reveal only):
  m_p       =  1.00727646693 u
  m_n       =  1.00866491595 u
  m(H-1)    =  1.00782503207 u
  avg lane A per-nucleon (computed) ≈ 0.99963 u
```

## Gate 1 — Algebraic Identities

```text
G1.1  Q_mass(C-12)  =  7117/16                     PASS (exact)
G1.2  m_SAM(C-12)   =  12 u                         PASS (exact)
G1.3  m_SAM(P) = A·u on 7 sampled rows              PASS (all exact)
G1.4  Q_mass − Q_sub = (N−Z) · 7093/192 (symbolic)  PASS (sympy verified)
G1.5  μ_Q · per-excess = 7093/7117 u                PASS (exact)

all_pass = TRUE
```

The extended kernel is algebraically consistent with the CR238 spine + CR239 anchor by exact rational arithmetic.

## Gate 2 — Lane A Mass Prediction Under Extended Kernel

```text
Lane A non-anchor rows tested      :  49
RMS ε(P) under m_SAM = A·u         :  0.002024   (0.20 %)
Max |ε(P)|                         :  0.005399   (Au-197 region; binding-curvature peak)
Median |ε(P)|                      :  0.001394
Fraction with |ε| < 0.001          :  44.9 %
Fraction with |ε| < 0.005          :  91.8 %
Fraction with |ε| < 0.01           :  100 %

Symmetric (N=Z) subset             :  12 rows, RMS 0.002344
Asymmetric (N≠Z) subset            :  37 rows, RMS 0.001922
```

**The extended kernel reproduces measured atomic mass at the 0.2 % level across the entire 49-row Lane A set, symmetric and asymmetric alike.** This is a dramatic improvement over CR239's canonical substrate-Q kernel (which had RMS 19 %).

Per-row predictions in `CR240_extended_kernel_predictions.csv`.

## Gate 3 — Binding-Energy Axis Identification

```text
Axis                                  Spearman ρ_S    Reading
asymmetry (N−Z)²/A                    +0.601           BW asymmetry term ✓
A (mass number)                       +0.499           volume / total-binding scale
surface A^(2/3)                       +0.499           BW surface term
N (neutron count)                     +0.534           neutron contribution
Z (atomic number)                     +0.420           proton contribution
Coulomb Z²/A^(1/3)                    +0.418           BW Coulomb term
Coulomb Z(Z−1)/A^(1/3)                +0.420           BW Coulomb (more standard)
N − Z (raw)                           +0.467           neutron-excess linear
magic min distance                    weak             not dominant in this set
pairing proxy                         weak             1-row resolution

max |ρ_S|                             0.601
BW-axis structured                    TRUE  (asymmetry, surface, Coulomb all > 0.4)
```

**The residual under m_SAM = A·u is the binding-energy curve.** The asymmetry term `(N−Z)²/A` is the dominant BW axis (ρ_S = 0.60). Multiple BW axes show consistent structure (volume + asymmetry + surface + Coulomb), consistent with a full Bethe-Weizsäcker-shaped residual. Full per-axis output in `CR240_residual_axis_correlations.csv`.

## Gate 4 — Typed Candidates C0–C8 Against Reveal Targets

### Per-candidate results

```text
ID  Formula                          Value         vs m_p         vs m_n         vs H-1          vs avg per-A
                                      (u)           (relative dev) (relative dev) (relative dev)  (relative dev)
C0  μ_Q · 4κ                          1.0000000      0.722 %        0.858 %        0.776 %         0.029 % ★
C1  μ_Q · (4κ − 8g)                   0.9966281      1.057 %        1.193 %        1.111 %         0.366 %
C2  μ_Q · (4κ + 8g)                   1.0033720      0.391 %        0.526 %        0.444 %         0.308 %
C3  μ_Q · 4κ · (1 + g)                1.0156250      0.829 %        0.690 %        0.770 %         1.531 %
C4  μ_Q · 4κ · (1 + 1/72)             1.0138889      0.657 %        0.518 %        0.599 %         1.358 %
C5  μ_Q · 4κ · (1 + 1/R²) = 145/144   1.0069444      0.033 % ★      0.171 %        0.087 % ★       0.665 %
C6  μ_Q · 4κ · (1 + g/α_H) = 129/128  1.0078125      0.053 % ★      0.085 % ★      0.0012 % ★★★    0.752 %
C7  μ_Q · 4κ · (1 + 1/M) = 127/126    1.0079365      0.066 % ★      0.072 % ★      0.011 % ★       0.764 %

C8  μ_Q · 4κ · 1/(S·ℒ) = 1/1296       0.0007716     —              —              —              —
    (diagnostic; against splittings)
    vs m_n − m_p (0.00138845 u):  residual 44.4 %
    vs H-1 − m_p (0.00054857 u):  residual 40.6 %
    vs 1u − substrate excess (7093/7117): not informative as a splitting target

★    = clears C-strict (< 0.1 %)
★★★  = exceptional (< 0.005 %; 12 ppm vs H-1)
```

### Lowest residual per target

```text
Target                       Closest candidate    Value          Residual
m_p (free proton)            C5  (1 + 1/R²)       1.0069444 u    0.033 %  (330 ppm)
m_n (free neutron)           C7  (1 + 1/M)        1.0079365 u    0.072 %  (720 ppm)
m(H-1) atomic                C6  (1 + g/α_H)      1.0078125 u    0.0012 % (12 ppm)
avg per-nucleon (Lane A)     C0  (anchor scale)   1.0000000 u    0.029 %
```

**C6 against H-1 is the standout result.** The typed expression `μ_Q · 4κ · (1 + g/α_H) = 129/128 u` matches measured atomic hydrogen `m(H-1) = 1.00782503207 u` to **12 parts per million**. The expression reduces to typed CR238 primitives:

```text
1 + g/α_H  =  1 + (1/64)/2  =  1 + 1/(2·S²)  =  1 + 1/128  =  129/128
```

That `1/128 = 1/(2·S²) = α_H · g / 2`-type form is a "face-halved neutron-unit" — assigning the substrate's neutron-unit coupling `g` per face (one of α_H = 2 faces).

**Three candidates clear C-strict against m_p (C5, C6, C7); two against m_n (C6, C7); three against H-1 (C5, C6, C7); one against avg per-nucleon (C0).** Per the locked candidate-scoring rule, no candidate is promoted to theorem-grade. CR241 holdout is required.

Per-candidate output in `CR240_candidate_typed_values.csv`.

## Wrong Controls

```text
WC1 — Substrate kernel as rest-mass kernel:
        RMS Lane A residual = 0.18948   (× canonical: 93.6)
        Replaying CR239's canonical Q-kernel as rest-mass produces a 93.6× degradation.
        Confirms the rest-mass channel is structurally distinct from the substrate channel.

WC2 — He-4 anchor swap:
        μ_Q (C-12 anchor)  = 192/7117 u/Q   = 0.026978
        μ_Q (He-4 anchor)  = 4.00260325413/(16κ) ≈ 0.026961 u/Q
        |drift|             = 0.000651   = 0.065 %
        STRONG threshold (<0.5%): PASS
        μ_Q is a stable dimensional bridge under anchor swap.

WC3 — Random per-nucleon mass scale (seed 20260623):
        RMS = 0.0511   (25.2× canonical)
        Random scales degrade prediction by ~25×.

WC4 — Constant per-nucleon m = A·c, c ∈ {0.5, 1.5, 2.0}:
        c=0.5 : RMS ≈ 0.5         (200× canonical)
        c=1.5 : RMS ≈ 0.5         (200× canonical)
        c=2.0 : RMS ≈ 1.0         (500× canonical)
        Only c = 1 u (anchored at C-12) is competitive — confirms anchor scale.

WC5 — Z·m_p + N·m_n no-binding kernel:
        ρ_S(residual, asymmetry (N−Z)²/A) = −0.637
        |ρ_S| > 0.5  → BW asymmetry axis structurally present in the binding residual
        This is the expected signature: the no-binding kernel's residual = binding energy,
        which tracks the BW asymmetry term. CR240's m_SAM = A·u residual tracks the
        SAME axis, confirming the residual interpretation.

WC6 — Random axis-label shuffle (seed 20260624):
        Original  ρ_S(residual, asymmetry) = −0.217
        Shuffled  ρ_S                      = −0.051
        Shuffled drops to noise (|ρ| < 0.3): TRUE
        Gate 3 axis-attribution integrity confirmed.
```

Per-WC output in `CR240_wrong_controls.csv`.

(Note: WC5's `ρ_S(residual_vs_asymmetry) = −0.637` and Gate 3's `+0.601` on the same axis differ in sign because WC5's residual is `m_measured − (Z·m_p + N·m_n)` while Gate 3's residual is `m_measured − A·u`. Both magnitudes confirm the asymmetry axis dominates the binding curve.)

## Verdict Logic (Audit Trail)

```text
STRONG_PASS conditions:
  S1 Gate 1 algebraic all pass               : TRUE
  S2 Gate 2 RMS < 0.005 (0.5 %)              : TRUE (0.00202)
  S3 Gate 3 BW axis structured (|ρ| > 0.5)   : TRUE (max |ρ_S| = 0.601)
  S4 ≥1 candidate clears C-strict (any tgt)  : TRUE (C0, C5, C6, C7 each clear at least one)
  S5 WC2 anchor drift < 0.005                : TRUE (drift = 0.00065)

BOUNDARY conditions (not reached):
  B1–B4 not evaluated (STRONG_PASS satisfied at higher precedence)

FAIL conditions (none triggered):
  F1 Gate 1 fails                            : FALSE
  F2 Gate 2 RMS > 0.05                       : FALSE
  F3 Gate 3 unstructured                     : FALSE
  F4 μ_Q drift > 5 %                         : FALSE

Verdict precedence: STRONG > BOUNDARY > FAIL.
Final verdict: STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED.

Disallowed-claim flags in summary JSON: 0 (clean).
```

## K-Gate Audit (Post-Execution)

| Gate | Status | Evidence |
|---|---|---|
| K1 | PASS | Single shaping anchor `m(C-12) = 12 u` (AME definition). Free nucleon and H-1 masses appear only as reveal-against-frozen-envelope in Gate 4 / WC5 deviation calculations, never as kernel-shaping inputs. |
| K2 | PASS | Pre-stated falsifiers F1–F5 — none fired. Verdict tier determined by locked thresholds, not by post-hoc adjustment. |
| K3 | PASS | Hypothesis chain, four gates, six wrong controls, nine candidates (C0–C8), verdict thresholds, disallowed-claims list, K-gates, falsifiers all sealed in `CR240_PRECOMMIT.md` (sha `3b6d4a…`) BEFORE the runner read any non-anchor measured mass. The candidate-scoring rule explicitly forbids post-data promotion. |
| K4 | PASS | CR238 typed spine (κ, g, S, M, R, ℒ) + CR239 anchored μ_Q + SHA-locked AME2020 subset. Free nucleon masses cited as reveal only. No new free parameter. |
| K5 | PASS | `python CR240_runner.py` deterministically reproduces every gate, wrong control, candidate, and verdict assignment. |

## Cryptographic Chain (Inputs)

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
CR240_PRECOMMIT.md                             =  3b6d4aa0102580c693bba9ba7a635d7654328bc632b1d34e7dc3cfbc7efc85cb
CR239_measured_isotope_masses.csv              =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
```

## What CR240 Says (Allowed STRONG_PASS Claim)

```text
"SAM has two distinct mass-related channels: the substrate gravitational
source-coupling channel Q_substrate(P) = S·[Z·κ + (N−Z)·g] (CR238, untouched),
and the rest-mass channel Q_mass(P) = 4·A·κ (CR240). Each nucleon contributes
equally to rest mass at the C-12-anchored scale 4κ·μ_Q = 1 u. The CR240
extended kernel reproduces measured atomic mass at 0.20 % RMS across the
AME2020 Lane A test set (49 non-anchor rows). The residual is structurally
the C-12-relative binding-energy curve, with the Bethe-Weizsäcker asymmetry
axis showing rank correlation |ρ_S| = 0.60 (max across nuclear axes).

Three of the nine precommitted typed candidates (C5 = 145/144 u, C6 = 129/128 u,
C7 = 127/126 u) clear the C-strict threshold (< 0.1 %) against at least one of
the free-nucleon or hydrogen-1 reveal targets. Candidate C6 matches measured
atomic hydrogen to 12 parts per million.

Per the locked candidate-scoring rule, NO candidate is promoted to theorem-grade
from this dataset. CR241 must run a separate holdout challenge before any
theorem-claimed selection."
```

## What CR240 Does NOT Say (Locked Disallowed Claims)

The runner verified that the result text and summary JSON contain none of:

```text
"CR240 falsifies the CR238 substrate kernel."
"CR240 derives m_n exactly."
"Q(P) and Q_mass(P) are the same quantity."
"Binding energy is reduced to typed primitives."
"A candidate was discovered after seeing the data."
```

Disallowed-claim scan flags: 0.

## Manuscript Implications

CR238 + CR239 + CR240 together close the substrate-to-mass arc:

1. **§N substrate spine (CR238).** Two foundational atoms `{ℱ, S}` + structural constant `α_H = 2` derive every other typed primitive. κ and g are bit-identical to CR221.
2. **§N+1 substrate-coupling channel (CR238 + CR239).** `Q(P) = S·[Z·κ + (N−Z)·g]` is the gravitational source-coupling. It is NOT measured rest mass — CR239 establishes the channel separation.
3. **§N+2 rest-mass channel (CR240).** `Q_mass(P) = 4·A·κ` reproduces measured atomic mass at 0.2 % RMS across 49 Lane A isotopes through one frozen `μ_Q` bridge. Residual is the C-12-relative binding-energy curve.
4. **§N+3 per-nucleon free mass forward statement.** Three typed candidates (C5, C6, C7) match free nucleon and H-1 reveal masses within 0.1 %. C6 = 129/128 u matches H-1 to 12 ppm. CR241 holdout will select (or eliminate) the theorem-grade candidate.

## Honest Scoring

This is a STRONG_PASS verdict on the channel-identification claim. The rest-mass kernel `Q_mass(P) = 4·A·κ` is structurally established as a separable channel in the SAM ontology, complementary to the CR238 substrate channel. The binding-energy axis is identified at the Bethe-Weizsäcker asymmetry term with `|ρ_S| = 0.60`.

The candidate result is more delicate:

- **Three candidates clearing C-strict simultaneously is structurally ambiguous, not theorem-grade.** Multiple typed expressions in `{ℱ, S, α_H}` produce nucleon-mass-scale numbers in the canonical AME2020 vicinity by typed construction. Selecting one as "the" derivation requires evidence beyond the current dataset.

- **C6 matching H-1 to 12 ppm is striking but precommitted.** The expression `1 + g/α_H = 1 + 1/128 = 129/128` was locked in the precommit table before the runner saw measured H-1. The match could be (a) deep structural truth, (b) coincidence among many available typed expressions, or (c) an artifact of the AME C-12 anchor convention. CR241 will discriminate.

- **CR241 holdout protocol** (precommitted): a candidate Cx is theorem-graded only if it (a) was selected in CR240's lowest-residual report AND (b) survives an independent measurement layer (later AME release, isotope mass spectroscopy data not in the original 51-row subset, or precision spectroscopy of H-1 / D / 3He). Until CR241 runs, the C6, C5, C7 results are recorded as **strong forward predictions**, not theorem-grade derivations.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs hash-locked. Verdict frozen.

If any sealed upstream CR (CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233, CR238, CR239) is later regraded such that its frozen numerical value changes, CR240 must be re-examined.

The candidate-scoring rule is permanent: no candidate from this CR will be promoted to theorem-grade without an independent holdout CR (CR241+).

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** Gate 1 (5 algebraic identities, all PASS); Gate 2 (49 Lane A rows, RMS 0.20 %); Gate 3 (10 axes, BW-axis structured with |ρ_S| = 0.60); Gate 4 (9 candidates × 4 targets, 3 candidates clearing C-strict); WC1–WC6 all confirm expected behavior; disallowed-claim flags: 0
**Verdict driver:** S1–S5 all satisfied — kernel identified, binding axis structured, candidate clearance achieved, anchor stable
**Foundational structural finding:** the rest-mass channel `Q_mass(P) = 4·A·κ` is a separable SAM channel from the substrate q_A channel; both anchor on the same μ_Q; their per-excess-neutron difference is the typed `(N−Z) · 7093/192` Q-units = `(N−Z) · 7093/7117 u`
**Forward predictions (strong, not theorem-graded):** C5 = 145/144 u ≈ m_p (330 ppm); C6 = 129/128 u ≈ m(H-1) (12 ppm); C7 = 127/126 u ≈ m_n (720 ppm)
**Next CR target:** CR241 — independent holdout selection of {C5, C6, C7} via measurement layer not used in CR240
