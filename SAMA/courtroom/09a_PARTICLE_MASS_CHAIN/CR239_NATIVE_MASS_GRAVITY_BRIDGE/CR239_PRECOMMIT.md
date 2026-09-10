# CR239 Native Mass / Gravity Bridge — Precommit

**Date:** 2026-06-23
**Classification:** NATIVE_MASS_GRAVITY_BRIDGE (downstream of CR238 substrate spine compaction)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-23 ("Next test" + safer-design scaffold at `c:/VS/The_Courtroom/CR239_SAFER_NATIVE_MASS_GRAVITY_BRIDGE_DESIGN.md`)
**Status:** PRECOMMITTED before runner execution.

## Scope

> **CR239 tests whether the CR238 completed source write `Q(P)` can be bridged to measured inertial / gravitational mass with one global dimensional bridge μ_Q, while protecting SAM from unfairly failing against low-confidence evaluated or extrapolated mass values.**

CR238 compacted the substrate spine to two foundational atoms `{ℱ, S}` with `κ = 7117/768`, `g = 1/64`, `Q(Z, N) = S · [Z·κ + (N − Z)·g]`. CR239 asks the immediate downstream question:

```text
Can one global μ_Q convert native Q(P) into measured inertial / gravitational mass?
```

The test must distinguish three outcomes — **direct bridge**, **structured residual**, or **fail** — and must not conflate disagreement with AME-evaluated or AME-extrapolated rows with rejection of the bridge.

> **CR239 does not modify upstream CRs. It tests one new structural constant — μ_Q — against measured atomic-mass data, with confidence-lane separation.**

## Locked Native Inputs (Inherited From CR238, Read-Only)

```text
Foundational atoms (CR238)    :  ℱ = 81, S = 8
Structural constant (CR238)   :  α_H = 2 (binary readout)
Derived (CR238)               :  D = 3, R = 12
                                 κ = 7117/768 (= 9.266927083…)
                                 g = 1/64 (= 0.015625)
Element / source engine:
  N(Z)    =  Z + ⌊(Z/R)·⌊(Z−1)/R⌋⌋
  G(Z, N) =  Z·κ + (N − Z)·g
  Q(Z, N) =  S · G(Z, N) = 8 · G(Z, N) = 7·G + G
```

New constant introduced (the only one in CR239):

```text
μ_Q  =  m_anchor / Q(P_anchor)         dimensional bridge, atomic mass units per Q-unit
```

The hypothesis under test:

```text
m_i(P) = m_g(P)  =  μ_Q · Q(P)
A_P(r)           =  2 · G_N · μ_Q · Q(P) / (c² · r)
```

## Measurement-Layer Warning (Locked Rule)

AME2020 and NUBASE-style mass tables are **reveal / evaluation layers**, not unquestionable authority layers. The runner must respect:

```text
HARD-FAIL is allowed only against Lane A high-confidence directly measured masses.
Evaluated / extrapolated rows produce residual maps or prediction conflicts, NOT automatic failure.
```

## Atomic vs Nuclear Mass Rule (Locked)

SAM's P-address contains Z electrons:

```text
P_{Z, N}  =  Z·p + N·n + Z·e
```

Therefore the CR239 comparison uses **atomic** masses (which include the electrons). Any later nuclear-mass lane must explicitly subtract `Z·m_e` and the electron-binding correction. Atomic and nuclear masses must never be mixed in the same score.

## Inputs (Hash-Locked at Execution)

```text
CR238 typed spine (read-only):
  CR238_PRECOMMIT.md           =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
  CR238_result.md              =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef

CR239 measured isotope masses (AME2020 curated subset with confidence lanes):
  CR239_measured_isotope_masses.csv  =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
  rows                                =  51 isotopes
  span                                =  H-1 (Z=1, N=0) through U-238 (Z=92, N=146)
  anchor                              =  C-12, m = 12.00000000000 u (exact AME definition)
  required columns:
    isotope, Z, N, A, atomic_mass_u, mass_uncertainty_u,
    measurement_class, source_table, confidence_lane, notes
  confidence-lane counts:
    LANE_A_HARD_MEASURED          : 50 rows (high-confidence direct atomic mass)
    LANE_B_EVALUATED              :  1 row (Be-8: short-lived, network-evaluated)
    LANE_C_EXTRAPOLATED_FRONTIER  :  0 rows in this curated subset
    LANE_D_POST_EVAL_CHALLENGE    :  reserved (not populated in v1)
```

## Confidence-Lane Definitions (Locked)

### Lane A — Hard-Measured

High-confidence direct atomic-mass measurements (Penning-trap, cyclotron, etc.) with small reported uncertainty. **Hard-fail is allowed only in Lane A.**

### Lane B — Evaluated

AME-style network-recommended values with uncertainty weighting. For each Lane B row the per-row score is:

```text
z(P)  =  ( m_measured(P) − μ_Q · Q(P) ) / σ_measured(P)
```

Allowed verdicts inside Lane B:

```text
PASS_LANE_B_WITHIN_UNCERTAINTY                |z| < 2 for ≥ 80 % of rows
BOUNDARY_LANE_B_STRUCTURED_RESIDUAL           |z| > 2 with structured pattern
FAIL_LANE_B_SYSTEMATIC_MISMATCH               unstructured large |z|
```

### Lane C — Extrapolated / Frontier

Rows marked as extrapolated, estimated, or weakly constrained. **Not a hard-fail lane.** SAM's prediction here is recorded as a forward prediction, not a verdict against SAM.

Allowed verdicts inside Lane C:

```text
PREDICTION_CONFLICT_WITH_EVALUATOR
BOUNDARY_FRONTIER_ROW
SAM_FORWARD_PREDICTION_RECORDED
```

### Lane D — Post-Evaluation Challenge

Freeze SAM against the prior evaluated table, then compare to later direct measurements. Question: does SAM predict the later direct measurement better than the prior evaluated table did? Pass condition:

```text
median( |m_new − m_SAM| )  <  median( |m_new − m_prior_eval| )
```

Lane D is reserved for v2 (not run in v1). The runner records but does not score Lane D.

## Gate 1 — Ratio-Only Test (No μ_Q, No Rescue Parameter)

For each Lane A pair `(P_i, P_j)`:

```text
ε^ratio(i, j)  =  | ( m(P_i)/m(P_j) ) / ( Q(P_i)/Q(P_j) )  −  1 |
```

Aggregate:

```text
RMS  ε^ratio across all Lane A pairs
Median ε^ratio
Fraction with ε^ratio < 0.01
Fraction with ε^ratio < 0.05
```

This gate uses no μ_Q. **If it fails badly in Lane A, one global μ_Q cannot rescue the direct bridge.**

## Gate 2 — One-Anchor Unit Bridge

```text
Anchor:               C-12
                      m(C-12) = 12.00000000000 u  (exact AME definition)

Compute:              Q(C-12) = 8 · [ 6·κ + 0·g ] = 48 · κ = 7117/16

Anchor μ_Q:           μ_Q = m(C-12) / Q(C-12) = 192 u / 7117  (exact rational)
                          ≈ 0.026977658…  u per Q-unit

Freeze μ_Q.

For every other P in the test set:
  m_SAM(P) = μ_Q · Q(P)
  ε(P)     = ( m_measured(P) − m_SAM(P) ) / m_measured(P)
```

Report on Lane A only (hard scoring):

```text
RMS residual
Max |ε(P)|
Fraction with |ε| < 0.01
Subset stats: symmetric (N=Z) vs asymmetric (N≠Z)
Residual pattern vs (N − Z), Z, A
```

**No row-by-row correction is allowed.** μ_Q is anchored once and frozen.

## Gate 3 — Isotope Increment Test (Sean's "Brutal" Gate)

```text
Predicted per added neutron at fixed Z:
  ΔG       =  g           =  1/64
  ΔQ       =  S · g       =  1/8
  Δm_SAM   =  μ_Q · ΔQ    =  μ_Q / 8  =  24 u / 7117  ≈ 0.003372 u

Measured pairs (ΔN = 1) in Lane A:
  (H-1, H-2), (H-2, H-3), (He-3, He-4),
  (Li-6, Li-7), (Be-9 — Be-8 is Lane B, exclude pair from hard score),
  (B-10, B-11),
  (C-12, C-13), (C-13, C-14),
  (N-14, N-15),
  (O-16, O-17), (O-17, O-18),
  (Mg-24, Mg-25), (Mg-25, Mg-26)

Per-pair score:
  R(i, j) = Δm_measured(i, j) / (ΔN_(i,j) · Δm_SAM)
```

Aggregate:

```text
mean(R), median(R), std(R)
Fraction with |R − 1| < 0.05
Fraction with |R − 1| < 0.50
```

Outcome reading:

```text
R ≈ 1 broadly                     →  direct bridge is very strong
R systematically far from 1, but
  structured by (N−Z) or shell    →  source-skeleton + binding residual
R random / unstructured            →  direct mass bridge likely fails
```

## Gate 4 — Residual-Structure Test (Boundary Discriminator)

If the direct bridge does not close at Gate 2 / Gate 3 hard tolerance, do NOT discard. Test whether the Gate 2 residual

```text
Δm(P)  =  m_measured(P) − μ_Q · Q(P)
```

tracks any of the following structural axes:

```text
(a) neutron excess (N − Z)
(b) mass number A
(c) atomic number Z
(d) shell-closure proximity (distance to magic Z or magic N: 2, 8, 20, 28, 50, 82, 126)
(e) SAM radix-cycle position ((Z − 1) mod R)
(f) stability / clock state (proxy via N − Z parity here; full clock state in v2)
```

Score per axis: Spearman rank correlation `ρ_S` between `Δm(P)` and the axis variable, plus linear correlation `r²`. A **structured residual** is declared if `|ρ_S| > 0.5` for any axis, OR if RMS Δm on symmetric (N = Z) rows is < 0.5 × RMS Δm on asymmetric rows.

Allowed structural reading under structured residual:

```text
Q(P)        =  native source skeleton
Δm(P)       =  binding / readout correction candidate
```

## Gate 5 — Gravitational Source Readout (DOWNSTREAM; NOT RUN IN v1)

If Gate 2 closes (STRONG_PASS) or Gate 4 reveals a clean structured residual (BOUNDARY_PASS), the exterior accumulation field becomes:

```text
A_P(r)  =  2 · G_N · μ_Q · Q(P) / (c² · r)
```

Composition-level test (reserved for v2):

```text
Q_sample = Σ_k n_k · Q(P_k)
M_SAM    = μ_Q · Q_sample
```

compared against bulk inertial and gravitational measurements. **Gate 5 is not run in CR239 v1.** It is documented here so the chain `Q → m → A(r)` is visible, but the composition test depends on Gate 2 / Gate 4 closing first.

## Wrong Controls (Precommitted)

Each wrong control re-runs Gate 2 (anchor + predict) under a perturbed kernel and asks: does the perturbed kernel beat canonical Q(P) on Lane A RMS residual?

### WC1 — R = 10

Override `R = 10` in the κ formula. Recompute κ' and Q'(Z, N). Re-anchor at C-12 with `μ_Q' = 12u / Q'(C-12)`. Predict Lane A. Expected: **degradation** (Q(P) under R=12 should beat Q'(P) under R=10).

### WC2 — R = 11

Same as WC1 with `R = 11`. Expected: **degradation**.

### WC3 — R = 13

Same as WC1 with `R = 13`. Expected: **degradation**.

### WC4 — S = 7

Override `S = 7`. Recompute Q'(Z, N) = S' · G(Z, N). Re-anchor and predict. Expected: **degradation**.

### WC5 — S = 9

Same as WC4 with `S = 9`. Expected: **degradation**.

### WC6 — Shuffled N(Z)

Permute the N value among the same Z values using a fixed seed:

```text
seed = 20260621
```

Compute Q with the shuffled N assignments. Re-anchor and predict. Expected: **degradation** — the (Z, N) coupling is structurally informative.

### WC7 — Shuffled Q(P)

Permute Q values among rows under the same fixed seed. Re-anchor and predict. Expected: **strong degradation** — the row-to-row identity of Q is what carries the mass-bridge claim.

### WC8 — Monotone random ladder

Generate a monotone random function `Q_rand(P)` that has the same endpoint range as Q(P) but with seeded random monotonic perturbations. Re-anchor at C-12 with `μ_Q^rand = 12u / Q_rand(C-12)`, predict, score. Tests whether Q(P)'s monotonicity alone — not its structural content — is doing the work. Expected: SAM Q(P) **outperforms** WC8.

### WC9 — Simplest baseline A = Z + N

```text
Q_A(P)    =  Z + N  =  A
μ_A       =  12u / 12  =  1 u  (per A-unit)
m_A(P)    =  A · 1 u
```

Compare Lane A RMS residual of Q(P) vs Q_A. **CR239 is only impressive if Q(P) beats or structurally improves on A.** WC9 is the most important practical control.

## Predictions (Precommitted)

### Block A — Locked deterministic computations

These are forced by the CR238 kernel + AME C-12 definition; failure means the test design itself is broken.

- **P1** — `Q(C-12) = S · 6 · κ = 8 · 6 · (7117/768) = 7117/16` (exact rational).
- **P2** — `μ_Q = 12 u / Q(C-12) = 192 u / 7117` (exact rational).
- **P3** — `Δm_SAM per added neutron at fixed Z = μ_Q · S · g = μ_Q / 8 = 24 u / 7117 ≈ 0.003372 u` (exact rational).
- **P4** — For every row in the test set, `Q(P) = S · [Z·κ + (N−Z)·g]` is uniquely determined and stored.

### Block B — Empirical regrade (outcome NOT precommitted; methodology is)

Computed by the runner; verdict assigned per locked thresholds.

- **P5** — Gate 1 ε^ratio distribution across all Lane A pairs.
- **P6** — Gate 2 ε(P) distribution across Lane A non-anchor rows; symmetric vs asymmetric subset stats.
- **P7** — Gate 3 R(i, j) distribution across ΔN = 1 pairs (Lane A).
- **P8** — Gate 4 residual-structure: Spearman ρ_S between Δm(P) and each axis (N−Z, A, Z, magic-shell distance, radix-cycle position, parity).
- **P9** — Lane A RMS residual comparison: Q(P) vs WC1–WC9.
- **P10** — μ_Q stability under WC6 / WC7 shuffles (record drift; not part of hard pass / fail).

## Pass Condition (Precommitted Verdict Spectrum)

```text
STRONG_PASS_CR239_DIRECT_MASS_GRAVITY_BRIDGE  iff  ALL of:
  (S1)  Lane A Gate 1: |ε^ratio| < 0.01 for ≥ 95 % of pairs;
                       median ε^ratio < 0.005.
  (S2)  Lane A Gate 2: |ε(P)| < 0.01 for ≥ 95 % of rows;
                       RMS ε(P) < 0.01.
  (S3)  Lane A Gate 3: |R − 1| < 0.05 for ≥ 80 % of ΔN=1 increments;
                       |median R − 1| < 0.10.
  (S4)  Q(P) beats WC9 (A = Z+N) by ≥ 2× on Lane A RMS residual.
  (S5)  Q(P) beats WC1–WC8 by ≥ 1.5× on Lane A RMS residual.

BOUNDARY_CR239_SOURCE_SKELETON_WITH_STRUCTURED_RESIDUAL  iff  ALL of:
  (B1)  Q(P) beats WC9 (A = Z+N) by ≥ 2× on Lane A RMS residual.
        (Q(P) is structurally informative for mass.)
  (B2)  Gate 1, Gate 2, or Gate 3 fails the STRONG_PASS thresholds, AND
  (B3)  Gate 4 finds STRUCTURED residual — at least one axis with |ρ_S| > 0.5
        OR symmetric/asymmetric RMS-ratio condition met.
  (B4)  Lane B (if any rows scored): structured residual continues into Lane B.

PREDICTION_CR239_FRONTIER_CONFLICT_WITH_EVALUATED_TABLE  iff:
  (P1)  Lane A passes BOUNDARY_PASS conditions, AND
  (P2)  Lane C rows (if present) record SAM predictions that conflict with
        the evaluated/extrapolated table.
        (Recorded as forward predictions, not failures.)

FAIL_CR239_DIRECT_BRIDGE  iff  ANY of:
  (F1)  Q(P) does NOT beat WC9 (A = Z+N) by 2× on Lane A RMS residual, OR
  (F2)  Lane A Gate 4 residual is UNSTRUCTURED (all |ρ_S| < 0.3 across all
        tested axes AND symmetric/asymmetric RMS ratio > 0.8), OR
  (F3)  μ_Q drifts by more than 5 % under WC6 (shuffled N(Z)) re-anchor.
```

Verdict precedence (in case multiple conditions match): STRONG > BOUNDARY > PREDICTION > FAIL.

## Disallowed Claims (Locked)

The runner / result must NOT claim any of:

```text
"SAM failed because it disagreed with AME2020 extrapolated values."
"SAM proved inertial and gravitational mass are Q(P)."
"A row-by-row fitted μ_Q closes the mass bridge."
"Atomic and nuclear masses were compared interchangeably."
```

Any verdict text that contains these patterns is itself a precommit violation.

## K-Gate Audit (Precommitted Pre-Execution)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | EXPLICIT + CONTAINED. AME2020 atomic masses are the frozen external envelope. The single shaping anchor is `m(C-12) = 12 u` (AME definition). All other measured masses act as the **reveal** against the native prediction; they do NOT shape the kernel. Per `[[feedback-no-outside-model-comparison]]` this is the legitimate K1 reveal-against-frozen-envelope pattern (not outside-model "agreement" credit). |
| K2 | Falsification | Pre-stated falsifiers F1–F4 (below); verdict tier (STRONG/BOUNDARY/PREDICTION/FAIL) determined by pre-committed thresholds. |
| K3 | Target hygiene | Locked hypothesis, five gates, four lanes, atomic-vs-nuclear rule, nine wrong controls, verdict thresholds, disallowed-claims list committed BEFORE the runner reads any non-anchor measured mass or computes any non-anchor Q. |
| K4 | Typed inputs | CR238 typed spine (κ, g, S — locked at CR238 sealed SHA `5e9161…`) + SHA-locked AME2020 subset (`54c2c2…`). No free parameter except μ_Q itself, anchored once. |
| K5 | Reproduction on demand | `python CR239_runner.py` deterministically computes all gates, all wrong controls, all lanes, and assigns the verdict per locked thresholds. |

## Falsifiers (Made Explicit)

- **F1**: `Q(C-12) ≠ 7117/16` (the CR238 kernel does not pass forward into Q; test design fails).
- **F2**: `μ_Q (anchor C-12) ≠ 192 u / 7117` (anchor computation is wrong).
- **F3**: The runner reports a verdict but the locked threshold formulas don't match the precommit (audit-design failure).
- **F4**: BOUNDARY_PASS reported while WC9 (A = Z+N) RMS ≤ Q(P) RMS — i.e., the "Q(P) beats A" precondition is not honored (verdict-assignment integrity failure).
- **F5**: Any disallowed claim appears in the result text or summary JSON (locked-claim violation).

## Allowed Claims Under Each Verdict Tier

```text
STRONG_PASS allowed claim:
  "SAM's completed source write Q(P) bridges directly to measured inertial and
  gravitational mass through one dimensional constant μ_Q = 192 u / 7117. No
  row-by-row fitting; no isotope-specific correction. The locked identity
  m_i = m_g = μ_Q·Q(P) holds across the Lane A AME2020 test set within 1 % on
  ≥ 95 % of rows and within 5 % per-neutron at fixed Z. The full chain
  Q → m → A(r) closes directly with one dimensional bridge."

BOUNDARY_PASS allowed claim:
  "Q(P) behaves as a native source/coupling skeleton, but measured rest mass
  requires a binding/readout residual map. The typed kernel reproduces measured
  mass for [symmetric isotopes] and leaves structured residuals on [asymmetric
  isotopes] correlated with [identified axis — e.g., (N−Z), shell-closure
  distance, or radix-cycle position]. The native identity m_g = m_i = μ_Q·Q(P)
  holds at the skeleton level; a residual map m_residual(P) is required to
  close the bridge."

PREDICTION_CONFLICT allowed claim:
  "SAM records a forward prediction conflict with the evaluated / extrapolated
  mass layer for [listed rows]. This is not a hard failure unless later
  high-confidence direct measurements resolve against SAM."

FAIL allowed claim:
  "Raw Q(P) is not measured mass. It remains a native substrate-coupling /
  source variable unless a separate bridge is derived. Q(P) does not beat
  A = Z + N in fitting Lane A measured isotope masses."
```

## Output Files (Locked Manifest)

```text
CR239_NATIVE_MASS_GRAVITY_BRIDGE/
  CR239_PRECOMMIT.md                              (this file)
  CR239_runner.py                                 (deterministic runner)
  CR239_summary.json                              (machine-readable verdict)
  CR239_result.md                                 (human-readable result)
  CR239_measured_isotope_masses.csv               (SHA-locked input)
  CR239_lane_a_hard_measured.csv                  (per-row Lane A results)
  CR239_lane_b_evaluated.csv                      (per-row Lane B results with z-scores)
  CR239_lane_c_extrapolated_frontier.csv          (Lane C forward predictions; empty in v1)
  CR239_lane_d_post_evaluation_challenge.csv      (Lane D reserved; empty in v1)
  CR239_ratio_test.csv                            (Gate 1 per-pair output)
  CR239_one_anchor_bridge.csv                     (Gate 2 per-row output)
  CR239_isotope_increment_test.csv                (Gate 3 per-pair output)
  CR239_residual_structure.csv                    (Gate 4 axis-correlation output)
  CR239_wrong_controls.csv                        (WC1–WC9 RMS comparisons)
  CR239_input_manifest.csv                        (file SHAs)
  HASHES.txt                                      (final all-artifact SHAs)
```

## Upstream Sources (Hash-Locked)

```text
CR114_result.md (capacity R² + split-loss)                =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger)              =  635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR221_result.md (kappa_floor = 7117/768; g_n = 1/64)      =  2fc932adda9df4e3002b6a996d321a072a009722801099747fae552c393fbeef
CR222_result.md (carrier ledger 12+1 closed sum)          =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)            =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR230_result.md (raw generator test)                      =  3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR232_result.md (matter-support promotion gate)           =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
CR233_result.md (18/81/27 tensor-substrate roles)         =  55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895
CR238_PRECOMMIT.md (substrate spine compaction)           =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md (substrate spine compaction)              =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef

CR239 measured-mass input (AME2020 curated subset):
CR239_measured_isotope_masses.csv                          =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc

CR239 source-design scaffold:
CR239_SAFER_NATIVE_MASS_GRAVITY_BRIDGE_DESIGN.md           =  (to be hashed at seal time; see HASHES.txt)
```

## Sequence Position

CR239 is **not** part of the Seven-Test Ownership Arc (CR230–CR236). It is the immediate downstream measured-mass test of CR238's typed spine.

Relation to surrounding work:

- **Upstream (read-only inputs):** CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233, CR238.
- **Does NOT regrade:** any of the above.
- **Enables under STRONG_PASS:** the full SAM chain `Q → m_i = m_g → A_P(r)` closes directly with one dimensional bridge. Manuscript-grade.
- **Enables under BOUNDARY_PASS:** identifies the missing structural axis; the natural next CR (CR240?) derives the residual map.
- **Enables under PREDICTION_CONFLICT:** records SAM forward predictions against weakly-constrained rows for future direct-measurement verification.
- **Enables under FAIL:** identifies that Q(P) is a substrate-coupling quantity not a mass surface; downstream substrate-to-matter bridge requires a fundamentally different construction.

## What CR239 Does

1. Locks the hypothesis `Q = S·G, m_i = m_g = μ_Q·Q, A_P(r) = 2 G_N μ_Q Q / (c² r)`.
2. Runs Gate 1 (ratio test, no μ_Q) on Lane A pairs.
3. Anchors μ_Q at C-12 (m = 12u exact); computes μ_Q = 192u/7117 exactly.
4. Runs Gate 2 (one-anchor bridge) — predicts m_SAM(P) for Lane A non-anchor rows; reports residuals.
5. Runs Gate 3 (isotope increment) — predicts Δm_SAM = μ_Q/8 per neutron; compares to measured ΔN=1 increments.
6. Runs Gate 4 (residual-structure) — tests whether Gate 2 residuals correlate with (N−Z), Z, A, shell-closure distance, radix-cycle position, parity.
7. Runs Lane B (if any rows): uncertainty-weighted z-scores.
8. Runs nine wrong controls (R perturbations, S perturbations, shuffles, monotone random, A=Z+N baseline).
9. Assigns verdict tier per locked thresholds with verdict precedence STRONG > BOUNDARY > PREDICTION > FAIL.
10. Records Gate 5 (gravitational source readout) chain as documented but does NOT run composition-level test in v1.

## What CR239 Does NOT Do

- Does NOT modify any upstream sealed CR.
- Does NOT introduce free parameters beyond μ_Q (one anchored dimensional constant).
- Does NOT row-by-row fit μ_Q.
- Does NOT mix atomic and nuclear masses.
- Does NOT use nuclear masses in v1 (atomic only).
- Does NOT run Gate 5 (composition-level gravitational test) in v1.
- Does NOT score Lane C as a failure — Lane C is a prediction lane.
- Does NOT score Lane D in v1 (Lane D reserved for v2).
- Does NOT claim against AME extrapolated values as hard failure.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs hash-locked. The locked hypothesis, five gates, four lanes, atomic-vs-nuclear rule, nine wrong controls, verdict thresholds (STRONG / BOUNDARY / PREDICTION / FAIL), disallowed-claims list, K-gates, and falsifiers are all frozen before runner execution.

If any sealed upstream CR is later regraded such that its frozen numerical value changes, CR239 must be re-examined.

If the AME2020 input subset is updated (e.g., AME2024 release, or addition of Lane C / Lane D rows), the SHA-locked replacement requires a regrade run.

---

**Precommit drafted by:** Claude (Opus 4.7, 1M context), at Sean's direction, from `CR239_SAFER_NATIVE_MASS_GRAVITY_BRIDGE_DESIGN.md`
**Sealed by:** Sean Brady, 2026-06-23 [pending Sean's seal]
**Arc relation:** Downstream of CR238 (substrate spine compaction); independent of Seven-Test arc
**New constant introduced:** μ_Q (one — the dimensional bridge from Q-units to atomic mass units)
**Verdict spectrum:** STRONG_PASS / BOUNDARY_PASS / PREDICTION_CONFLICT / FAIL
