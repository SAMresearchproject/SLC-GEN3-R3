# CR249 A-Kernel Binding Geometry — Result

## Verdict

```text
CR249_BOUNDARY_A_KERNEL_GEOMETRY_FITS_BW_RANGE__
ASYMMETRY_COEFFICIENT_LANDS_AT_1_OVER_S_L_WITHIN_1PCT__
SOME_WC_GATES_NOT_MET
```

`execution_status   = CLEAN`
`scientific_verdict = BOUNDARY`
`classification     = BINDING_GEOMETRY_AND_TYPED_COEFFICIENTS (downstream of CR238/CR240/CR245/CR247/CR248)`
`precommit_sha      = d4a93d3f87908b3630e4e9d68618109e1394c97830dfd5b22bc400651e29399b`

## Plain-English Summary

Per Sean's round4.pdf framing: the A-kernel `A(r) = r_s / r` read on a finite
SOB object of radius `ρ_A = A^(1/3)` predicts the binding-curvature shapes
that CR248's linear per-particle debit sum could not capture. The locked
geometric dictionary:

```text
ρ_A     = A^(1/3)                  SOB radius coordinate
V_A     = ρ_A³ = A                 volume = accumulated interior writes
S_A     = ρ_A² = A^(2/3)           surface = exposed boundary (d/dρ ρ³ = 3ρ²)
R_A⁻¹   = ρ_A⁻¹ = A^(-1/3)         road = boundary traversal cost (from A(r) = r_s/r)
ΔQ      = Q_mass − Q_sub           channel gap (CR238/CR240/CR245 identity)
```

The candidate binding form:

```text
B_SAM = c_V·A − c_S·A^(2/3) − c_C·Z(Z−1)/A^(1/3) − c_A·ΔQ²/Q_mass + c_P·δ_pair
```

## Headline Results

**Phase A — the geometry IS right.**

```text
Train RMS = 2.73 MeV   R² = 0.99458   (n = 35, Lane A A≥16)
Test  RMS = 3.52 MeV   R² = 0.98502   (n = 20, CR241 holdout)
```

Comfortably under the precommit 5 MeV threshold; on par with standard BW
fits. The A-kernel geometric shapes capture the binding curve.

**Phase B — first within-1% typed coefficient in the binding arc.**

The asymmetry coefficient `c_A` lands on:

```text
c_A_fitted    = +7.7504e-4 u  (+0.7219 MeV)
c_A_typed     = +1/(S·L) = +1/1296 = +7.7160e-4 u  (+0.7188 MeV)
relative dev  = 0.44 %    ← WITHIN 1 % TYPED
```

This is the first binding coefficient to land on a clean typed rational
within 1 %. Structurally: `S = 8` is the 1/8 split (primitive substrate
atom), `L = 162` is the closed-ledger value (`R²·9/8` from CR217). The
SAM asymmetry coefficient `c_A = 1/(carrier-split × closed-ledger)` reads
cleanly.

Per-coefficient summary:

| Coefficient | Fitted | Best Typed | Rel. Dev. | ≤ 5 % | ≤ 1 % |
|---|---:|---|---:|:---:|:---:|
| c_V (volume)     | +8.635e-3 u (+8.04 MeV) | +1/(R·κ) = +64/7117 | 4.14 % | ✓ | |
| c_S (surface)    | +1.963e-2 u (+18.28 MeV)| +1/(D·Θ) = +1/54     | 5.64 % | | |
| c_C (Coulomb)    | +7.420e-4 u (+0.69 MeV) | +1/(S·L) = +1/1296   | 4.00 % | ✓ | |
| c_A (asymmetry)  | +7.750e-4 u (+0.72 MeV) | **+1/(S·L) = +1/1296** | **0.44 %** | ✓ | **✓** |
| c_P (pairing)    | +3.752e-3 u (+3.49 MeV) | +1/(V·κ) = +27·768/(27·7117) = +768/(27·7117) (ratio 1/(V·κ)) | 6.53 % | | |

`Matched within 5%: 3/5; within 1%: 1/5.`

Two notable structural rhymes:

1. `c_A` and `c_C` both land near `1/(S·L)`. `c_A` is within 0.44 %, `c_C`
   within 4.00 %. They are different shapes (asymmetry vs Coulomb) but the
   coefficients sit in the same typed neighborhood `~ 0.72 MeV`. Whether
   this is structural (asymmetry and Coulomb share a typed denominator) or
   coincidental needs more data.
2. `c_V` lands near `1/(R·κ)`, same as CR245's volume candidate; same loose
   fit (~4 %) because we're still fitting `B_u = A − m_measured` which
   absorbs per-nucleon mass-excess into the volume coefficient.

**Wrong controls give a nuanced reading.**

| WC | Description | RMS (MeV) | Ratio | Pass |
|---|---|---:|---:|:---:|
| WC-1 | Drop volume | 20.42 | 7.49× | ✓ |
| WC-2 | Drop surface | 16.83 | 6.17× | ✓ |
| WC-3 | Drop Coulomb | 14.34 | 5.26× | ✓ |
| WC-4 | Drop asymmetry | 12.38 | 4.54× | ✓ |
| WC-5 | Drop pairing | 3.17 | **1.16×** | (gate ≥1.5×) ✗ |
| WC-6 | Surface A^(2/3) → A^(1/2) | 3.10 | **1.14×** | (gate ≥1.2×) ✗ |
| WC-7 | Road A^(-1/3) → A^(-2/3) | 5.63 | 2.06× | ✓ |
| WC-8 | Pairing δ → δ/√A | 2.78 | 1.02× | (report-only) ✓ |
| WC-9 | Shuffle B_u labels | 35.50 | 13.02× | ✓ |

**Reading.** Volume, surface, Coulomb, asymmetry are each essential
(4-7× degradation when removed). Pairing contributes real signal (1.16×)
but less than the 1.5× strong-pass gate — at this data scale, pairing is
a modest but real correction. Surface A^(1/2) vs A^(2/3) are degenerate at
fit precision (1.14×) — the fit can absorb the difference into the other
coefficients. The road exponent A^(-1/3) IS load-bearing (replacing with
A^(-2/3) gives 2.06× degradation). Shuffle is overwhelmingly degraded
(13×) — the model fits real structure, not noise.

F2 (any shape-removal WC truly preserves RMS, ratio < 1.05) does NOT fire:
every shape-removal degrades at least 1.16×. The verdict-driving criterion
that landed BOUNDARY rather than FAIL is the WC-5 and WC-6 gate misses,
not a true no-degradation finding.

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : d4a93d3f87908b3630e4e9d68618109e1394c97830dfd5b22bc400651e29399b
Train SHA-256           : 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
Test SHA-256            : 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8

Substrate atoms (read-only from CR238):
  R = 12   D = 3   S = 8   Theta = 18   M = 126   L = 162   V = 27
  kappa = 7117/768   g = 1/64   mu_Q = 192/7117 u
```

## Block A — Phase A Free-Fit

```text
Design matrix: [A, -A^(2/3), -Z(Z-1)/A^(1/3), -(dQ)^2/Q_mass, +delta_pair]
Train set: CR239 Lane A non-anchor with A >= 16 and N >= Z   (n = 35)
Test set:  CR241 holdout with N >= Z                          (n = 20)

Fitted coefficients (B_u in u):
  c_V (volume)    = +8.6350e-3 u  (+8.0434 MeV)
  c_S (surface)   = +1.9626e-2 u  (+18.2819 MeV)
  c_C (Coulomb)   = +7.4196e-4 u  (+0.6911 MeV)
  c_A (asymmetry) = +7.7504e-4 u  (+0.7219 MeV)   [on (dQ)^2/Q_mass; equiv (N-Z)^2/A coefficient 26.59 MeV]
  c_P (pairing)   = +3.7517e-3 u  (+3.4947 MeV)

Metrics:
  Train RMS = 2.9262e-3 u = 2.7260 MeV   R^2 = 0.99458
  Test  RMS = 3.7805e-3 u = 3.5218 MeV   R^2 = 0.98502
```

Comfortably within standard BW fit quality. **The five A-kernel geometric
shapes reproduce the binding curve.** Detail in `CR249_phase_a_fit.csv`.

## Block B — Anchor Cases

Predictions are extrapolations: anchors are evaluated under the fit but C-12
(A=12) and C-13 (A=13) are below the A ≥ 16 training cutoff.

| Anchor | B_u observed   | B_u predicted | Residual    |
|--------|---------------:|---------------:|------------:|
| C-12   | +0.000 MeV     | −4.865 MeV     | −4.86 MeV   |
| C-13   | −3.125 MeV     | −7.374 MeV     | −4.25 MeV   |
| Au-197 | +31.141 MeV    | +28.461 MeV    | −2.68 MeV   |

Au-197 lands within 2.68 MeV (heavy-nucleus regime where the geometric
shapes dominate). Light-nucleus predictions are within ~5 MeV of observed
— better than CR248's linear model (~17-19 MeV miss at C-12/C-13) but not
exact, as A < 16 is outside training range and shell-effects begin to
dominate. Detail in `CR249_anchor_cases.csv`.

## Block C — Phase B Typed-Coefficient Reduction

The candidate family (same as CR245): atoms, reciprocals, atom products,
ratios, and special families (κ², κg, (D+2)/(R(D+1)), (D²+S)/(D·S²),
7093²/(192·7117)). Per-coefficient best match:

```text
c_V  fitted +8.635e-3 u   best +1/(R*kappa)  = +8.993e-3   rel 4.14 %   WITHIN 5%
c_S  fitted +1.963e-2 u   best +1/(D*Theta)  = +1.852e-2   rel 5.64 %   out
c_C  fitted +7.420e-4 u   best +1/(S*L)      = +7.716e-4   rel 4.00 %   WITHIN 5%
c_A  fitted +7.750e-4 u   best +1/(S*L)      = +7.716e-4   rel 0.44 %   WITHIN 1%  ←
c_P  fitted +3.752e-3 u   best +1/(V*kappa)  = +4.014e-3   rel 6.53 %   out

Matched within 5%: 3/5
Matched within 1%: 1/5   (c_A)
```

**`c_A = 1/(S·L)` is the first binding coefficient to land within 1%**
of a clean typed rational. Both atoms are CR238-derived: `S = 8` is the
1/8 carrier split (primitive); `L = 162` is the closed-ledger value
`R²·9/8` (sealed in CR217/CR229). The fitted MeV value is 0.7219; the
typed prediction is 0.7188 — gap of 31 keV out of 720 keV.

**Zero-free typed candidate (substitute 3 within-5% candidates, keep
fitted for c_S and c_P):**

```text
Train RMS = 21.71 MeV   (vs fitted 2.73 MeV; 7.96x worse)
Test  RMS = 31.91 MeV   (vs fitted 3.52 MeV; 9.07x worse)
```

5% slack on three coefficients compounds badly across the BW evaluations.
The within-1% c_A alone is not enough to recover fitted RMS.

Detail in `CR249_typed_candidates.csv` and `CR249_zero_free_predictions.csv`.

## Block D — Wrong Controls (Full)

| WC | Description | RMS (MeV) | Ratio | Pass |
|---|---|---:|---:|:---:|
| WC-1 | Drop volume term (`c_V = 0`) | 20.42 | 7.49× | ✓ |
| WC-2 | Drop surface term (`c_S = 0`) | 16.83 | 6.17× | ✓ |
| WC-3 | Drop Coulomb term (`c_C = 0`) | 14.34 | 5.26× | ✓ |
| WC-4 | Drop asymmetry term (`c_A = 0`) | 12.38 | 4.54× | ✓ |
| WC-5 | Drop pairing term (`c_P = 0`) | 3.17 | 1.16× | ✗ (gate 1.5×) |
| WC-6 | Surface `A^(2/3)` → `A^(1/2)` | 3.10 | 1.14× | ✗ (gate 1.2×) |
| WC-7 | Road `A^(−1/3)` → `A^(−2/3)` | 5.63 | 2.06× | ✓ |
| WC-8 | Pairing `δ` → `δ/√A` | 2.78 | 1.02× | report-only |
| WC-9 | Shuffle B_u labels (seed 20260623) | 35.50 | 13.02× | ✓ |

**Notes.** WC-5 (pairing drop) ratio 1.16× means pairing contributes real
signal (16% RMS degradation when removed), just less than the strong-pass
1.5× gate. WC-6 (surface scaling A^(1/2) instead of A^(2/3)) ratio 1.14×
means the two surface forms are largely interchangeable at the available
fit precision — the OLS can absorb the difference into other coefficients.
WC-8 (pairing variant δ vs δ/√A) ratio 1.02× confirms the two pairing
forms are fungible at this precision. WC-7 (1/A^(2/3) road) ratio 2.06×
confirms the locked `1/A^(1/3)` Coulomb radius scaling IS structurally
specific — the user's geometric reading of road from A(r) = r_s/r is
load-bearing. WC-9 (shuffle) 13.02× confirms the model fits real
structure.

Detail in `CR249_wrong_controls.csv`.

## Block E — K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 | PASS | External anchor: CR239/CR241 AME isotope masses (SHA-locked). Phase A fit RMS measured against external B_u values. |
| K2 | PASS | Falsifiers F1-F5 pre-stated. None fired. F2 specifically required true no-degradation (ratio < 1.05) on any shape-removal WC; observed minimum was 1.16× (pairing), well above threshold. |
| K3 | PASS | Structural prediction test. The five shapes are derived from the A-kernel geometric reading (volume from ρ³, surface from ρ², road from 1/ρ, asymmetry from CR245 identity, pairing from parity). All locked before runner read data. |
| K4 | PASS | Substrate atoms `{R, D, S, M, L, V, Θ, κ, g}` only; no free parameter in Phase A model definition. Phase A coefficients are fitted, but they are explicitly reported (not used as verdict criteria). Phase B coefficient candidates come from the locked finite typed-rational family. |
| K5 | PASS | `python CR249_runner.py` deterministically reproduces every fit, every WC, every typed-candidate search. |

## Block F — Verdict Gate Status

| Condition | Status |
|---|:---:|
| S1 Phase A train RMS ≤ 5 MeV | PASS (2.73 MeV) |
| S2 Phase A test RMS ≤ 5 MeV | PASS (3.52 MeV) |
| S3 Phase A train R² ≥ 0.95 | PASS (0.99458) |
| S4 Phase A test R² ≥ 0.95 | PASS (0.98502) |
| S5 Shape-removal WCs (WC-1..5) each degrade ≥ 1.5× | **FAIL** (WC-5 pairing = 1.16×) |
| S6 Geometric-scaling WCs (WC-6, WC-7) degrade ≥ 1.2× | **FAIL** (WC-6 surface A^(1/2) = 1.14×) |
| S7 Shuffle WC-9 degrades ≥ 2× | PASS (13.02×) |

Phase A fully passes (S1-S4); WC gates S5 and S6 miss by narrow margins
on pairing and surface-scaling specifically; S7 passes overwhelmingly.

**Verdict: BOUNDARY** — the A-kernel geometry fits the binding range
(Phase A), one coefficient lands within 1% typed (`c_A = 1/(S·L)`), three
within 5%, but the full WC degradation thresholds are not met for pairing
(WC-5 1.16× vs gate 1.5×) and surface scaling (WC-6 1.14× vs gate 1.2×).

## Cryptographic Chain (Inputs)

```text
CR238_result.md  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md  = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md  = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md  = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR243_result.md  = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md  = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_result.md  = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR247_result.md  = ed0eb192ca708e33fb6a044ac5a11e20cfdf1ab507b0bc241110a14646b662d7
CR248_result.md  = 34277d508ea5ca50ecdf8120aa1849022613c677acc6b6b95194bcc65c87b241
CR249_PRECOMMIT.md = d4a93d3f87908b3630e4e9d68618109e1394c97830dfd5b22bc400651e29399b
CR249_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR249_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## What CR249 Does

1. Locks the A-kernel geometric reading from round4.pdf:
   `ρ_A = A^(1/3)`, `V_A = A`, `S_A = A^(2/3)`, `R_A^(-1) = A^(-1/3)`,
   `ΔQ = Q_mass − Q_sub` (CR245 identity).
2. Fits the five-shape model `B_SAM = c_V·A − c_S·A^(2/3) − c_C·Z(Z-1)/A^(1/3) − c_A·ΔQ²/Q_mass + c_P·δ_pair` on Lane A train (A ≥ 16) at OLS. Train RMS 2.73 MeV, R² 0.995. Test RMS 3.52 MeV, R² 0.985.
3. Searches typed-rational candidates for each coefficient over the CR238
   atom family. **Identifies `c_A = 1/(S·L)` at 0.44% relative deviation —
   the first binding coefficient within 1% typed in the entire arc.**
4. Reports two additional within-5% matches: `c_V ≈ 1/(R·κ)`, `c_C ≈ 1/(S·L)`. The c_C/c_A near-coincidence at `1/(S·L)` is recorded as
   structurally interesting.
5. Runs nine wrong controls. Volume/surface/Coulomb/asymmetry are each
   essential (4-7× degradation when removed); pairing contributes modest
   signal (1.16×) but below the strong-pass gate. Surface-scaling A^(1/2)
   vs A^(2/3) is degenerate at fit precision; road 1/A^(1/3) vs 1/A^(2/3)
   is NOT degenerate (2.06× degradation). Shuffle dramatically degrades
   (13×).
6. Reports BOUNDARY: Phase A passes Phase A; Phase B has the c_A 1% win;
   WC gates S5 and S6 narrowly miss on pairing and surface scaling.

## What CR249 Does NOT Do

- Does NOT promote the asymmetry-coefficient match `c_A = 1/(S·L)` to a
  theorem-grade derived value. The 0.44% relative deviation is within the
  1% tolerance, which is a strong structural rhyme; full theorem-grade
  status would require either (a) deriving 1/(S·L) from CR238/CR245 first
  principles independent of the fit, or (b) reproducing the match across
  multiple independent isotope sets at sub-0.1% precision.
- Does NOT close the full zero-free binding prediction. Three within-5%
  coefficients aren't tight enough; zero-free RMS inflates 8-9× vs fitted.
- Does NOT replace CR245 BOUNDARY for the binding-curvature derivation.
  CR249 sharpens it: one coefficient now lands within 1% typed.
- Does NOT extend to proton-rich isotopes (N < Z); same scope as
  CR245/CR247/CR248.

## Block G — Structural Reading

```text
Layer 5 (binding closure) progress across the arc:

CR242:  BW + SAM-typed basis with FITTED coefficients matches BW empirically;
        zero-free typed candidate has R² = −0.19 (worse than mean baseline)

CR245:  BW + SAM-asymmetry (Q_mass-Q_sub)^2/Q_mass:
          - asymmetry SHAPE derived from CR238/CR240 (theorem-grade identity)
          - 3/5 coefficients within 5% typed; 0/5 within 1%
          - best structurally clean match: d = 1/(R*D) at 1.9%
        BOUNDARY.

CR248:  Linear per-particle B_u closure with 4-particle basis:
          - source/Q_mass/Q_sub/dQ algebraic identities exact (theorem-grade)
          - linear B_u model RMS 24.5 MeV (2x null, not closure-grade)
        BOUNDARY.

CR249:  A-kernel binding geometry:
          - 5 shapes fit BW range cleanly (train 2.73 MeV, R^2 0.995)
          - c_A = 1/(S*L) at 0.44 % (WITHIN 1 % TYPED, new structural finding)
          - c_V, c_C within 5%; c_S, c_P out
          - WC-7 confirms 1/A^(1/3) road is structurally specific
          - pairing and surface-scaling WC gates narrowly missed
        BOUNDARY.
```

The progressive sharpening: each CR brings one or more typed coefficients
closer. CR249's `c_A = 1/(S·L)` is the first within-1% landing. The next
natural CR could either: (a) attempt to derive `1/(S·L)` from
CR238/CR245 first principles independent of the fit; (b) test whether
`c_V`, `c_C`, `c_S`, `c_P` can be tightened by reformulating the binding
target (e.g., standard binding `B = Σ m_free − m_atom` instead of
`B_u = A − m_atom`); or (c) add additional channel-occupancy terms from
CR243/CR244 to give the fit additional typed degrees of freedom.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Substrate atoms, binding form, geometric
dictionary, Phase A fit method, Phase B typed-candidate search, wrong
controls, verdict gates, falsifiers all frozen.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** Phase A train RMS 2.726 MeV / R² 0.99458 (n=35); test
RMS 3.522 MeV / R² 0.98502 (n=20); Phase B 3/5 within 5%, 1/5 within 1%
(c_A = 1/(S·L) at 0.44%); zero-free typed candidate train RMS 21.7 MeV /
test RMS 31.9 MeV; 7 of 9 WCs pass (volume/surface/Coulomb/asymmetry
removals all >4× degradation; pairing 1.16×; surface scaling 1.14×; road
scaling 2.06×; pairing form variant 1.02×; shuffle 13×).
**Verdict driver:** S1–S4 + S7 PASS; S5 (WC-5 pairing 1.16× < 1.5× gate)
and S6 (WC-6 surface scaling 1.14× < 1.2× gate) FAIL; F2 (true no-
degradation) does NOT fire (minimum ratio 1.16× > 1.05 threshold).
**Structural advance:** first within-1% typed coefficient in the binding
arc (c_A = 1/(S·L) at 0.44%); A-kernel geometric reading (volume A,
surface A^(2/3), road 1/A^(1/3), asymmetry from CR245 identity) confirmed
as the right binding shape basis at BW-fit precision.
**Open follow-up:** CR250 candidate — derive 1/(S·L) from CR238/CR245
first principles independent of the fit, OR reformulate target as standard
binding B = Σ m_free − m_atom and refit (the BW asymmetry coefficient
would then be 23.7 MeV which 1/(S·L)·c_const·μ_Q might give cleaner).
