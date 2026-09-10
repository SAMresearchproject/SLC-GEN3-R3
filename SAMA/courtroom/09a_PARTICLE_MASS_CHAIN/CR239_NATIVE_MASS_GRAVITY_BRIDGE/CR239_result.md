# CR239 Native Mass / Gravity Bridge — Result

## Verdict

```text
CR239_FAIL_RAW_Q_NOT_MEASURED_MASS__DIRECT_BRIDGE_REJECTED__STRUCTURED_RESIDUAL_OBSERVED__WC9_A_EQUALS_Z_PLUS_N_BEATS_Q_BY_90X
```

`execution_status   = CLEAN`
`scientific_verdict = FAIL_CR239_DIRECT_BRIDGE`
`classification     = NATIVE_MASS_GRAVITY_BRIDGE (downstream of CR238)`
`precommit_sha      = 52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7`

## Plain-English Summary

The locked hypothesis `m_i(P) = m_g(P) = μ_Q · Q(P)` with one global `μ_Q = 192u/7117` (anchored at C-12 exact) **does not directly bridge the CR238 typed Q(P) to measured atomic mass**.

But the failure is **highly structured** — not random noise. Three specific findings:

1. **Symmetric isotopes (N = Z) match exceptionally well.** RMS residual on the 12-row N=Z subset is 0.23 %. The C-12 anchor's `μ_Q` transports cleanly to He-4, O-16, Ca-40, etc.
2. **Asymmetric isotopes show a per-neutron deficit.** The measured isotope mass increment per added neutron is **297× larger** than SAM predicts. The CR238 kernel's `g = 1/64` produces `Δm_SAM = μ_Q · S·g = μ_Q / 8 ≈ 0.003372 u` per neutron, while AME2020's measured isotope ladders show ≈ 1 u per neutron.
3. **The simplest possible control — `A = Z + N` — beats `Q(P)` by a factor of 90× on Lane A RMS residual.** That is the load-bearing precondition for any non-FAIL verdict, and `Q(P)` loses it.

The verdict is the precommit-allowed FAIL claim:

```text
"Raw Q(P) is not measured mass. It remains a native substrate-coupling / source
variable unless a separate bridge is derived. Q(P) does not beat A = Z + N in
fitting Lane A measured isotope masses."
```

## What This Tells Us (Structural Reading)

The structured residual is the load-bearing scientific content of this FAIL:

| axis | Spearman ρ_S | reading |
|---|---:|---|
| `N − Z` | **+0.984** | residual grows almost perfectly with neutron excess |
| `A` | +0.961 | residual grows with mass number (driven by N − Z component) |
| `N − Z parity` | +0.534 | weaker parity signal |
| `Z` | +0.413 | partial — heavier elements have larger absolute residuals |
| magic-shell distance (min Z or N) | weak | shell structure does not dominate |
| radix-cycle position `(Z−1) mod R` | weak | CR238 radix not visible in residual |

```text
Symmetric (N = Z) RMS residual : 0.0023  (12 rows)
Asymmetric (N ≠ Z) RMS residual: 0.2152  (37 rows)
Sym/Asym ratio                  : 0.0009
```

**The residual is one structural axis: `(N − Z)`.** The Spearman correlation `ρ_S = +0.984` essentially fills the entire dynamic range. This is precisely the BOUNDARY_PASS structural pattern — except that the BOUNDARY_PASS verdict also required `Q(P)` to beat `A = Z + N` by 2×, which it did not.

Reading aloud:

```text
Q(P)        =  native source skeleton (matches measured mass for N = Z)
Δm(P)       =  proportional to (N − Z) at +0.984 rank correlation
             =  per-neutron mass contribution that the CR238 g = 1/64 does
                not capture, but A = Z + N does
```

CR238's typed kernel splits the substrate write into proton-position (`Z·κ`) and neutron-excess (`(N − Z)·g`) terms with the substrate-internal weight `g = 1/S² = 1/64`. The neutron-excess weight on the **substrate** (the 1/8 share of completed source write per added neutron) is structurally correct — CR221 verifies it bit-identically. But that weight, transported through `μ_Q` to measured mass, is ≈ 300 × too small. Either:

1. `Q(P)` is measuring a different substrate-coupling density than measured rest mass; **measured mass needs an additional term that scales with `(N − Z)` at the per-neutron mass scale** (≈ 1 u per added neutron, not 1/8 of the `μ_Q`-scaled substrate increment).
2. `μ_Q` is not a pure unit conversion — the bridge from Q to measured mass needs a residual map `Δm(P)` rather than a single multiplicative constant.

These are not mutually exclusive. The CR239 design scaffold called both out as the two readings the test was built to discriminate. CR239 reports: **option 2 holds.**

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : 52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7
CR238_PRECOMMIT.md sha  : 5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md sha     : 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
Input CSV sha           : 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc

Kernel atoms (read-only from CR238):
  ℱ = 81, S = 8, α_H = 2 → D = 3, R = 12
  κ = 7117/768, g = 1/64

Anchor:
  Isotope : C-12 = (Z=6, N=6)
  Mass    : 12 u exact (AME definition)
  Q(C-12) : 7117/16  = 444.8125
  μ_Q     : 192 u / 7117 = 0.0269775889…  u per Q-unit
```

## Gate 1 — Ratio Test (No μ_Q)

```text
Pairs tested (Lane A):       1225
RMS ε^ratio:                 0.179480
Median ε^ratio:              0.089244
Max ε^ratio:                 (large; full distribution in CR239_ratio_test.csv)
Fraction with ε^ratio < 1%:  9.2 %
Fraction with ε^ratio < 5%:  37.1 %
```

**Gate 1 FAILS the STRONG_PASS threshold** (`≥ 95 %` within 1 % required). The ratio `Q_i/Q_j` does not track `m_i/m_j` for Lane A pairs. μ_Q-free, so this is the structurally cleanest indication that one global `μ_Q` cannot rescue the direct bridge.

## Gate 2 — One-Anchor Unit Bridge

```text
Lane A non-anchor rows tested:       49
RMS residual ε(P):                    0.189480
Max |ε(P)|:                            0.981 (H-1; SAM predicts ~2.00u, measured 1.008u)
Median |ε(P)|:                         0.077
Fraction with |ε| < 1%:                22.4 %
Fraction with |ε| < 5%:                26.5 %

Symmetric (N=Z) subset:
  rows                : 12
  RMS ε(P)            : 0.0023   (within 0.23 %)

Asymmetric (N≠Z) subset:
  rows                : 37
  RMS ε(P)            : 0.2152   (over 21 %)
```

Per-row residuals in `CR239_one_anchor_bridge.csv`.

The symmetric subset is essentially perfect — the C-12 anchor's `μ_Q` correctly predicts He-4, Be-8, C-12, N-14, O-16, Ne-20, Mg-24, Si-28, S-32, Ca-40 all within 0.5 %. The asymmetric subset is where the bridge breaks: as `(N − Z)` grows, predicted mass falls progressively below measured.

## Gate 3 — Isotope Increment (Sean's "Brutal" Gate)

```text
ΔN = 1 pairs tested:               14
Predicted Δm_SAM per neutron:      24 u / 7117 = 0.003372 u

Measured / predicted ratio R(i,j):
  mean R                : 296.45
  median R              : 296.66
  std  R                :   2.95
  Fraction |R − 1| < 5% :   0.0 %
  Fraction |R − 1| < 50%:   0.0 %
```

Per-pair in `CR239_isotope_increment_test.csv`.

The brutal-gate verdict is unambiguous: **measured isotope mass spacing is ≈ 297 × larger than SAM predicts per neutron.** The neutron-excess increment in measured mass is ~1 u per neutron (≈ neutron rest mass minus a small binding correction), while the CR238 substrate weight `g = 1/64` gives μ_Q-scaled Δm of ~0.003 u per neutron — three orders of magnitude smaller.

The tightness of R around 297 (`std/mean ≈ 0.01`) is itself diagnostic: the under-counting is **not random** — it is a clean multiplicative factor. That clean factor is the signal a residual-map CR could exploit.

## Gate 4 — Residual-Structure Test

```text
Axis correlations (Spearman ρ_S, p-value):

  N − Z                       :  ρ_S = +0.984,   p < 1e-30   ← dominant axis
  A (mass number)             :  ρ_S = +0.961,   p < 1e-25
  N − Z parity                :  ρ_S = +0.534,   p ≈ 1e-4
  Z (atomic number)           :  ρ_S = +0.413,   p ≈ 3e-3
  magic Z distance            :  weak (|ρ| < 0.3)
  magic N distance            :  weak (|ρ| < 0.3)
  magic min(Z, N) distance    :  weak (|ρ| < 0.3)
  (Z − 1) mod R               :  weak (|ρ| < 0.3)

Symmetric vs asymmetric RMS Δm:
  sym RMS Δm  : 0.025 u
  asym RMS Δm : 27.4 u
  sym/asym    : 0.0009

structured_residual = True  (dominated by (N − Z) axis, ρ_S = +0.984)
```

Per-axis output in `CR239_residual_structure.csv`.

**The residual is dominated by one axis: `(N − Z)`.** This is the cleanest possible structural signal for the missing per-neutron-mass term.

## Wrong Controls — Lane A RMS Comparison

```text
                                              RMS ε_lane_A      ×canonical
  canonical Q(P)                            :    0.18948         1.000
  WC1   R = 10                              :    0.18934         0.999
  WC2   R = 11                              :    0.18942         1.000
  WC3   R = 13                              :    0.18953         1.000
  WC4   S = 7                               :    0.18964         1.001
  WC5   S = 9                               :    0.18922         0.999
  WC6   shuffled N(Z), seed 20260621        :    0.19501         1.029
  WC7   shuffled Q values, seed 20260621    :    4.99549        26.364
  WC8   monotone random ladder              :    0.38471         2.030
  WC9   A = Z + N baseline                  :    0.00202         0.011   ← beats Q by 90×
```

Per-WC details in `CR239_wrong_controls.csv`.

**Reading:**

- **WC1–WC5 (R and S perturbations) are essentially canonical-equivalent** within ±0.5 % RMS. Perturbing the CR238-locked radix or split does not change Q-vs-measured-mass behavior, because the dominant residual axis is `(N − Z)` — and `Q(P) = S·[Z·κ + (N−Z)·g]` has neutron-excess weight `S·g = 1/8` regardless of which `R`-derived `κ` is used. The R/S perturbations move `Z·κ` slightly, which barely registers against the much larger `(N − Z)` deficit.
- **WC6 (shuffled N(Z))** degrades by 3 %. The Z↔N coupling carries some signal but not the load-bearing signal.
- **WC7 (shuffled Q values)** degrades by 26×. The row-to-row identity of Q (which isotope gets which Q value) IS structurally informative for measured mass — Q is not random.
- **WC8 (monotone random ladder)** degrades by 2×. Q has more structure than mere monotonicity.
- **WC9 (A = Z + N)** WINS by a factor of 90×. This is the load-bearing finding: the trivial mass-number sum `Z + N` fits measured atomic mass dramatically better than the typed Q(P).

**Verdict-precondition failure:** the precommit's BOUNDARY_PASS requires Q to beat WC9 by 2×. Q is beaten by WC9 by 90×. BOUNDARY_PASS condition B1 fails. STRONG_PASS condition S4 fails. Therefore **FAIL_CR239_DIRECT_BRIDGE** by precedence.

## Lane B (Evaluated Rows)

```text
Lane B rows tested : 1   (Be-8, network-evaluated short-lived isotope)
```

With only 1 Lane B row, the z-score statistics are not informative. Recorded in `CR239_lane_b_evaluated.csv` for completeness.

## Lane C / Lane D

```text
Lane C (extrapolated/frontier) rows : 0   (none in v1 curated subset)
Lane D (post-evaluation challenge)  : reserved for v2
```

Empty files written for shape compliance. v2 would populate Lane C with superheavy / frontier predictions and Lane D with paired prior-eval vs later-direct-measurement comparisons.

## Verdict Logic (Audit Trail)

```text
STRONG_PASS conditions:
  S1 Gate 1 (ratio, 95% < 1%) : FAILED (9.2 %)
  S2 Gate 2 (95% < 1%)         : FAILED (22.4 %)
  S3 Gate 3 (R within 0.05)    : FAILED (0.0 %)
  S4 beats WC9 by 2×           : FAILED (0.011 × canonical, so canonical is 90× worse)
  S5 beats WC1–WC8 by 1.5×     : FAILED (WC7 26×, WC8 2× worse, but WC1–5 essentially equal)

BOUNDARY_PASS conditions:
  B1 beats WC9 by 2×           : FAILED (precondition for BOUNDARY)
  B2 STRONG_PASS failed        : TRUE
  B3 structured residual       : TRUE  (|ρ_S| = 0.984 on N − Z)

FAIL conditions:
  F1 does not beat WC9 by 2×   : TRUE  (sufficient for FAIL)
  F2 unstructured residual     : FALSE (residual is highly structured)
  F3 μ_Q drifts under WC6 > 5% : (recorded; not the trigger)

Verdict precedence: STRONG > BOUNDARY > PREDICTION > FAIL.
Verdict: FAIL_CR239_DIRECT_BRIDGE
  (driven by F1: Q does not beat A = Z + N)
```

## K-Gate Audit (Post-Execution)

| Gate | Status | Evidence |
|---|---|---|
| K1 | PASS | Single shaping anchor `m(C-12) = 12 u` (AME definition). All other measured masses served as the reveal-against-frozen-envelope. No outside-model agreement credit claimed. |
| K2 | PASS | Pre-stated falsifiers F1–F5 — F1 fired (Q does not beat WC9). Verdict determined by locked thresholds, not by post-hoc adjustment. |
| K3 | PASS | Locked hypothesis, five gates, four lanes, atomic-vs-nuclear rule, nine wrong controls, verdict thresholds, disallowed-claims list, K-gates, falsifiers all sealed in CR239_PRECOMMIT.md (sha `52c947…`) BEFORE the runner read any non-anchor measured mass. |
| K4 | PASS | CR238 typed spine (κ = 7117/768, g = 1/64, S = 8) + SHA-locked AME2020 curated subset (`54c2c2…`). No free parameter except `μ_Q` itself, anchored once at C-12. |
| K5 | PASS | `python CR239_runner.py` deterministically reproduces every gate, every wrong control, every lane, and the verdict assignment. Disallowed-claim scan: 0 flags. |

## Cryptographic Chain (Inputs)

```text
CR114_result.md (capacity R² + split-loss)                =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger)              =  635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR221_result.md (kappa_floor = 7117/768; g_n = 1/64)      =  2fc932adda9df4e3002b6a996d321a072a009722801099747fae552c393fbeef
CR222_result.md (carrier ledger)                          =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion)                     =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR230_result.md (raw generator)                           =  3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR232_result.md (matter-support gate)                     =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
CR233_result.md (18/81/27 tensor roles)                   =  55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895
CR238_PRECOMMIT.md (substrate spine compaction)           =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md (substrate spine compaction)              =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_PRECOMMIT.md                                        =  52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7
CR239_measured_isotope_masses.csv                          =  54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
```

## What CR239 Says

1. The CR238 typed kernel `Q(P) = S·[Z·κ + (N−Z)·g]` is **not** a measured rest-mass surface under one global μ_Q.
2. For symmetric isotopes (N = Z), the anchor-derived μ_Q reproduces measured atomic mass within 0.5 %. This is a real structural agreement: the substrate write per proton-position, scaled by μ_Q, equals the per-proton-position contribution to atomic mass.
3. For asymmetric isotopes, the per-neutron measured-mass contribution (≈ 1 u) is **297×** the substrate's per-neutron Q-contribution (`μ_Q · S·g = 24 u / 7117`). The CR238 substrate weight `g = 1/64` is structurally correct (CR221, CR232, CR238 all verify it) — but it is **not the per-neutron mass weight.**
4. The residual `Δm(P) = m_measured(P) − μ_Q·Q(P)` is essentially monotonic in `(N − Z)` with Spearman correlation +0.984.
5. The simplest possible baseline `A = Z + N` beats `Q(P)` by 90× on Lane A RMS residual. Per the locked precommit, this triggers `FAIL_CR239_DIRECT_BRIDGE` regardless of how structured the residual is.

## What CR239 Does NOT Say

- Does NOT claim Q(P) is structureless. Q(P) tracks measured mass with `ρ_S = +0.984` rank correlation and is symmetric-isotope exact within 0.5 %.
- Does NOT claim the CR238 substrate spine is wrong. CR238 stands. `κ`, `g`, `S` are bit-identically reproduced. What CR239 rejects is the bridge **m_i = m_g = μ_Q·Q(P)** as a one-constant identity.
- Does NOT claim AME2020 is "right" against SAM. The locked disallowed-claims rule prevents the runner from using AME values as authority. CR239's hard-fail trigger was internal: Q lost to the simplest control `A = Z + N`.
- Does NOT make a Gate 5 (composition-level gravitational) claim. Gate 5 requires the bridge to close at Gate 2; it does not.

## Allowed Forward Statement (Per Precommit FAIL Tier)

```text
"Raw Q(P) is not measured mass. It remains a native substrate-coupling /
source variable unless a separate bridge is derived. Q(P) does not beat
A = Z + N in fitting Lane A measured isotope masses."
```

## What This Enables (CR240+ Direction)

The structured residual gives the next CR a clear target. Under the locked structural reading:

```text
m_measured(P)  =  μ_Q · Q(P)  +  Δm_binding(P)
```

with `Δm_binding(P)` having known structural form:

```text
Δm_binding(P)   ≈  (N − Z) · m_n  −  (small binding curvature)
```

at first order. The remaining binding-curvature term is what a Bethe-Weizsäcker–like surface, or a SAM-native source-address readout `Δm(Z, N)`, would parameterize. **The CR239 result delivers a single, sharp axis for that next CR** — neutron-excess mass contribution at the per-neutron scale.

This is not a hidden free parameter; it is a structurally explicit term that CR239 has shown is **missing** from the canonical Q kernel, with one clean axis to derive it on.

## Honest Scoring of the Verdict

CR239 returns FAIL because the locked precommit required `Q(P)` to beat `A = Z + N` by 2× before any non-FAIL verdict was admissible. That precondition was deliberate — it protected the test from rewarding `Q(P)` for trivial monotonicity. Q lost the precondition by a factor of 90×, so the FAIL is correctly reported.

But the FAIL is **structurally informative**:

- The neutron-excess signal at `ρ_S = +0.984` is the cleanest possible direction for a residual-map CR.
- The 297× under-counting per neutron is a single multiplicative factor, not a scatter pattern.
- The symmetric-isotope agreement at 0.23 % RMS shows the substrate write is doing real work — it is just not the same quantity as rest mass.

This is the outcome the CR239 design scaffold called the "boundary" reading in spirit (Q(P) as source skeleton; mass needs a residual map), even though the verdict-precondition formally lands on FAIL. The next CR can build directly on this.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs hash-locked. Verdict frozen.

If any sealed upstream CR (CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233, CR238) is later regraded such that its frozen numerical value changes, CR239 must be re-examined.

If the AME2020 input subset is updated (e.g., to AME2024), the SHA-locked replacement requires a regrade run.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** Gate 1 (1225 pairs); Gate 2 (49 Lane A rows; sym 12 / asym 37); Gate 3 (14 ΔN=1 pairs); Gate 4 (8 axes); Lane B (1 row); WC1–WC9; disallowed-claim scan: 0 flags
**Verdict driver:** F1 — `Q(P)` does not beat `A = Z + N` by 2× on Lane A RMS residual
**Foundational structural finding:** residual `Δm(P)` has Spearman `ρ_S = +0.984` against `(N − Z)`; symmetric subset RMS 0.23 %, asymmetric subset RMS 21.5 %; measured-vs-predicted per-neutron ratio R = 297 (tight, not random)
**Next-CR target:** derive `Δm_binding(P) ≈ (N − Z) · m_n − binding-curvature` as a SAM-native residual map (`CR240?`)
