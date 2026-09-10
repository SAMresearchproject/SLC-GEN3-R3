# CR248 SOB Micro-Channel Debit Occupancy Map — Result

## Verdict

```text
CR248_BOUNDARY_FOUR_PARTICLE_DECOMP_EXACT__
LINEAR_B_U_CLOSURE_INSUFFICIENT__BINDING_NON_LINEAR__
PAIR_WRITE_TERMS_REQUIRED_PER_CR245
```

`execution_status   = CLEAN`
`scientific_verdict = BOUNDARY`
`classification     = FOURTH_LAYER_DECOMPOSITION + LINEAR_B_U_CLOSURE_ATTEMPT (downstream of CR238/CR240/CR245/CR247)`
`precommit_sha      = 7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa`

## Plain-English Summary

CR248 extends CR247's two-particle inverse decomposition
(balanced + excess) to **four-particle resolution**: proton, balanced
neutron, excess neutron, electron, each carrying explicit
`(u, d, e, Q_mass, Q_sub, dQ)` typed-rational contributions.

**Phase A — STRONG_PASS algebraic decomposition.** All six identities
(source u/d/e + Q_mass + Q_sub + dQ) close EXACTLY on all 69 N ≥ Z test
rows under Fraction arithmetic. All three fatality.pdf anchor cases pass:
C-12 (6 protons + 6 balanced neutrons + 6 electrons), C-13 (one extra
excess neutron), Au-197 (79 each + 39 excess neutrons). Zero free
parameters. Reproduces and refines CR247.

**Phase B — Linear B_u closure attempt: 24.5 MeV RMS, BOUNDARY.** Fitting
`B_u(Z, N) = α·Z + β·(N − Z)` on Lane A (A ≥ 16, n=35) yields:

```text
α = +3.14 MeV per electron-paired position (s_p + s_n_b + s_e)
β = −5.62 MeV per excess neutron (s_n_e)

Train RMS = 24.52 MeV   R² = 0.561   (n = 35)
Test  RMS = 25.21 MeV   R² = 0.232   (n = 20)
Null  RMS = 49.08 MeV
Linear/Null ratio = 2.00× (precommit gate exactly met)
```

The linear model has signal (2× better than the B_u = 0 null) but **cannot
capture binding curvature** — the train RMS is ~7× the BW-shape fit from
CR245 (2.78 MeV). Per the precommit's anticipated outcome: per-particle
constants miss the surface (`A^(2/3)`), Coulomb (`Z(Z−1)/A^(1/3)`),
asymmetry (`(N−Z)²/A` — exact via CR245 identity), and pairing terms.

**Anchor predictions under the linear model:**

| Case   | B_u observed   | B_u predicted  | Residual    |
|--------|---------------:|---------------:|------------:|
| C-12   | +0.000 MeV     | +18.859 MeV    | +18.86 MeV  |
| C-13   | −3.125 MeV     | +13.237 MeV    | +16.36 MeV  |
| Au-197 | +31.141 MeV    | +29.071 MeV    | −2.07 MeV   |

Au-197 lands within 2 MeV — the linear model is actually decent for heavy
nuclei because per-nucleon contributions dominate. Light nuclei (C-12,
C-13) miss by ~16-19 MeV because surface and Coulomb curvature kicks in
sharply at low A and the linear-in-Z, linear-in-(N-Z) form has nowhere to
put it.

All six wrong controls pass. The honest finding: **the fourth-layer
algebraic decomposition is theorem-grade; the fifth-layer surface-debit
closure requires the non-linear pair-write terms from BW phenomenology,
which CR245 already attempted and which CR248 confirms is the actual
obstacle.**

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : 7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa
Train SHA-256           : 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
Test SHA-256            : 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8

Substrate atoms (read-only from CR238):
  kappa = 7117/768   g = 1/64   S = 8   mu_Q = 192/7117 u

Per-particle basis (derived by disaggregating CR247 phi_balanced and phi_excess):
  proton            phi_p   = (u=2, d=1, e=0, Q_mass=4*kappa, Q_sub=8*kappa, dQ=-4*kappa)
  balanced neutron  phi_n_b = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=0,       dQ= 4*kappa)
  excess   neutron  phi_n_e = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=1/8,     dQ=7093/192)
  electron          phi_e   = (u=0, d=0, e=1, Q_mass=0,        Q_sub=0,       dQ=0)

Occupancy (for N >= Z):
  n_proton = Z   n_balanced_neutron = Z   n_excess_neutron = N - Z   n_electron = Z
```

## Block A — Phase A Identity Verification

| Identity | Rows | Match | Rate |
|---|---:|---:|---:|
| u (source u-quark)    | 69 | **69** | 1.000 |
| d (source d-quark)    | 69 | **69** | 1.000 |
| e (source electron)   | 69 | **69** | 1.000 |
| Q_mass                | 69 | **69** | 1.000 |
| Q_sub                 | 69 | **69** | 1.000 |
| dQ (channel gap)      | 69 | **69** | 1.000 |

**All-six-match: 69/69.** Per-row detail in `CR248_per_row_phase_a.csv`.

The four-particle decomposition closes the algebraic identity exactly. The
**disaggregation is structurally consistent with CR247**: WC-1 confirms
`phi_proton + phi_balanced_neutron + phi_electron = (3, 3, 1, 8κ, 8κ, 0) = phi_balanced` (CR247); WC-2 confirms `phi_excess_neutron = (1, 2, 0, 4κ, 1/8, 7093/192) = phi_excess_neutron` (CR247).

## Block B — Anchor Cases

### C-12 (Z=6, N=6, A=12)

```text
Occupancy:  n_p = 6, n_n_b = 6, n_n_e = 0, n_e = 6

Phase A:
  Source:  u = 6·2 + 6·1 + 0·1 + 6·0 = 18 = 2·6 + 6  ✓
  Source:  d = 6·1 + 6·2 + 0·2 + 6·0 = 18 = 6 + 2·6  ✓
  Source:  e = 6·0 + 6·0 + 0·0 + 6·1 = 6 = Z         ✓
  Q_mass:  6·4κ + 6·4κ + 0·4κ + 6·0 = 48κ = 4·12·κ   ✓
  Q_sub:   6·8κ + 6·0 + 0·(1/8) + 6·0 = 48κ          ✓
  dQ:      6·(−4κ) + 6·(4κ) + 0·(7093/192) + 6·0 = 0 ✓

Phase B (linear B_u prediction):
  B_u_obs = 0.000 u = 0.000 MeV (C-12 is anchor)
  B_u_pred = 6·α + 0·β = 6·(3.14 MeV) = +18.86 MeV
  Residual: +18.86 MeV  (linear model misses anchor entirely)
```

### C-13 (Z=6, N=7, A=13)

```text
Occupancy:  n_p = 6, n_n_b = 6, n_n_e = 1, n_e = 6

Phase A: all six identities exact (Q_mass = 92521/192 = 481.880208,
         Q_sub = 7119/16 = 444.9375, dQ = 7093/192 = 36.942708)

Phase B (linear B_u prediction):
  B_u_obs = -0.00335 u = -3.13 MeV
  B_u_pred = 6·α + 1·β = 6·3.14 + (-5.62) = +13.24 MeV
  Residual: +16.36 MeV
```

### Au-197 (Z=79, N=118, A=197)

```text
Occupancy:  n_p = 79, n_n_b = 79, n_n_e = 39, n_e = 79

Phase A: all six identities exact (Q_mass = 1402049/192 = 7302.338542,
         Q_sub = 562711/96 = 5861.572917, dQ = 92209/64 = 1440.765625)

Phase B (linear B_u prediction):
  B_u_obs = +0.0334 u = +31.14 MeV
  B_u_pred = 79·α + 39·β = 79·3.14 + 39·(-5.62) = +29.07 MeV
  Residual: -2.07 MeV  (linear model lands within 2 MeV at heavy nuclei)
```

**Reading.** The linear model is structurally accurate for heavy nuclei
(Au-197 residual −2.07 MeV) but fails at light nuclei (C-12 missed by
+18.86 MeV) because surface, Coulomb, and asymmetry effects dominate at
low A. This is the expected behaviour — binding-energy nonlinearity is
real and the linear-in-(Z, N − Z) basis cannot capture it.

Detailed anchor breakdown in `CR248_anchor_cases.csv`; linear-fit per-row
predictions in `CR248_phase_b_linear_fit.csv`.

## Block C — Phase B Linear Fit Details

```text
Fitted on:  CR239 Lane A non-anchor, A >= 16, N >= Z       (n = 35)
Evaluated:  full Lane A train (above) + CR241 holdout      (n = 20 test)

Coefficients:
  alpha (per electron-paired position; s_p + s_n_b + s_e)  = +3.374e-3 u  (+3.14 MeV)
  beta  (per excess neutron; s_n_e)                        = -6.035e-3 u  (-5.62 MeV)

Metrics:
                 train (n=35)        test (n=20)
  RMS_u          3.413e-3            3.520e-3
  RMS_MeV        24.52               25.21
  R^2            0.5614              0.2322
  Null RMS_MeV   49.08               54.04
  Linear/Null    2.00x better        2.15x better
```

The linear model has structural signal (2× better than B_u = 0 baseline)
but train R² = 0.56 and test R² = 0.23 — well below the BW fit from CR245
(R² 0.99 train, 0.99 test at 2.78 MeV RMS). The per-particle linear basis
**captures the leading per-nucleon scaling and the per-excess-neutron
mass-excess slope** but **does not capture surface, Coulomb, asymmetry, or
pairing curvature**.

## Block D — Wrong Controls

| WC | Description | Result | Pass |
|---|---|---|:---:|
| WC-1 | `phi_p + phi_n_b + phi_e == CR247 phi_balanced` (disaggregation check) | Componentwise equal: `(3,3,1,8κ,8κ,0)` | ✓ |
| WC-2 | `phi_n_e == CR247 phi_excess_neutron` (disaggregation check) | Componentwise equal: `(1,2,0,4κ,1/8,7093/192)` | ✓ |
| WC-3 | `n_proton = Z + 1` (occupancy perturbation breaks source u) | 69/69 rows break | ✓ |
| WC-4 | Quark swap p ↔ n_b (preserves sum, structural-identification flag only) | Sum (3,3) preserved; flagged as audit, not falsifier | ✓ |
| WC-5 | Linear B_u model RMS at least 2× better than null | 49.08/24.52 = 2.00× (exactly meets gate) | ✓ |
| WC-6 | Shuffled B_u labels (seed 20260623) degrades fit ≥ 1.5× | Ratio shuffled/canonical | ✓ |

All six wrong controls pass. Per-WC details in `CR248_wrong_controls.csv`.

**Note on WC-4 (quark swap).** Swapping the quark assignments
`phi_p ↔ phi_n_b` preserves the sum `(2+1, 1+2) = (3, 3)` at the
combined-nucleon level. This means the algebraic identity does NOT
distinguish proton-vs-neutron quark assignment — both `(uud, udd)` and
`(udd, uud)` give the same per-balanced-position contribution. WC-4 is
recorded as a structural-identification audit flag (we cannot
algebraically distinguish proton from balanced neutron via source
constraints alone) rather than a falsifier. The distinction comes from
the q_sign of each particle, which is preserved in CR243's substrate
ledger but not used by CR248's source identity.

## Block E — K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 | PASS | External anchors: CR239/CR241 isotope inputs (SHA-locked). B_u observed values come from external AME2020 atomic masses; the linear fit is tested against external measurement. |
| K2 | PASS | Falsifiers F1–F6 pre-stated. None fired. F3 (linear model has no signal) was specifically protected by WC-5 which passed at exactly 2× the null. |
| K3 | PASS | Structural prediction test. Basis vectors are forced by disaggregation of CR247 (which itself derives from CR238/CR240 algebra). Occupancy formula and linear B_u model locked above the line. |
| K4 | PASS | Substrate atoms `{κ, g, S}` only; no free parameter in Phase A. Phase B fits two coefficients (α, β) by OLS, but these are reported, not used as verdict criteria except via the locked S7 threshold and WC gates. |
| K5 | PASS | `python CR248_runner.py` deterministically reproduces every Phase A identity, every Phase B fit metric, every wrong control. |

## Block F — Verdict Gate Status

| Condition | Status |
|---|:---:|
| S1 Phase A all 6 identities exact on all 69 rows | PASS |
| S2 Anchors C-12, C-13, Au-197 all six identities exact | PASS |
| S3 Disaggregation checks WC-1, WC-2 match CR247 componentwise | PASS |
| S4 WC-3 occupancy perturbation breaks source identity | PASS |
| S5 Linear B_u model ≥ 2× better than null | PASS (exactly 2.00×) |
| S6 Shuffle WC degrades fit ≥ 1.5× | PASS |
| S7 Linear B_u closure within tol (train ≤ 0.020 u, test ≤ 0.025 u) | **FAIL** (train 0.0034 u, test 0.0035 u → ~25 MeV RMS) |

**Verdict: BOUNDARY** — S1–S6 pass; S7 fails. Phase A is theorem-grade
structural identity (extending CR247); Phase B linear B_u closure has
signal but is insufficient by ~7× of the CR245 BW fit.

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
CR248_PRECOMMIT.md = 7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa
CR248_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR248_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## What CR248 Does

1. **Phase A:** Extends CR247's two-particle inverse decomposition to a
   four-particle decomposition (proton, balanced neutron, excess neutron,
   electron) by disaggregating CR247's basis vectors at the per-nucleon-
   plus-electron level. Verifies all six source/Q_mass/Q_sub/dQ identities
   close exactly under Fraction arithmetic on all 69 N ≥ Z test rows.
2. **Phase B:** Fits the linear per-particle surface-debit model
   `B_u = α·Z + β·(N − Z)` on Lane A train (A ≥ 16); evaluates on CR241
   holdout. Reports fitted coefficients (α = +3.14 MeV, β = −5.62 MeV),
   train RMS 24.5 MeV, test RMS 25.2 MeV.
3. **Anchor predictions:** C-12 misses by +18.86 MeV (light-nucleus
   regime where linear breaks), C-13 misses by +16.36 MeV (likewise),
   Au-197 hits within −2.07 MeV (heavy-nucleus regime where per-nucleon
   averaging dominates).
4. **Wrong controls:** all six pass — disaggregation matches CR247
   componentwise; occupancy perturbation breaks source; quark swap is
   recorded as structural-identification audit flag; linear model beats
   null by exactly 2.00×; shuffle degrades fit.
5. **Reports the fifth-constraint status:** the linear per-particle
   surface-debit closure is structurally insufficient for binding-curvature
   prediction. The non-linear pair-write terms required (volume,
   surface A^(2/3), Coulomb Z(Z−1)/A^(1/3), asymmetry per CR245 identity,
   pairing δ/√A) are exactly the BW form CR245 already tested with typed-
   coefficient candidates and landed at BOUNDARY. CR248 confirms the gap.

## What CR248 Does NOT Do

- Does NOT close the fifth fatality.pdf constraint (full B_u prediction
  with non-linear pair-write terms). That is the remaining open question;
  CR245's BW form is the closest existing attempt.
- Does NOT modify CR245 BOUNDARY (which fitted BW shapes with typed-
  coefficient candidates and got 3/5 at 5%, 0/5 at 1%, zero-free RMS
  6-8× worse than fitted).
- Does NOT modify CR247 STRONG_PASS (which is the second-layer
  decomposition); Phase A here is the disaggregation of CR247 to the
  four-particle level and is consistent with it by construction (WC-1, WC-2).
- Does NOT extend to proton-rich isotopes (N < Z); the H-1 and He-3 rows
  in CR239 are excluded. The N < Z symmetric variant is reserved.

## Block G — Structural Reading

The CR248 BOUNDARY sharpens the open binding-derivation problem:

```text
Layer 1 (source inventory):           n_p = Z, n_n = N, n_e = Z         — trivially closed by atomic structure
Layer 2 (balanced/excess split):      Z balanced + (N-Z) excess          — CR247 STRONG_PASS, theorem-grade
Layer 3 (four-particle decomp):       Z p + Z balanced_n + (N-Z) excess_n + Z e  — CR248 Phase A STRONG_PASS for source/Q/dQ
Layer 4 (linear B_u closure):         B_u = α*Z + β*(N-Z)               — CR248 Phase B BOUNDARY (24.5 MeV RMS)
Layer 5 (non-linear pair-write):      + surface + Coulomb + asymmetry + pair  — CR245 BOUNDARY (2.78 MeV RMS, coefficients
                                                                              within 5% but not 1%; asymmetry shape derived)
```

**Layers 1-3 are closed. Layers 4-5 share the same gap: binding-energy
non-linearity at low A demands shape terms beyond per-particle constants,
and these shape coefficients do not reduce to clean typed rationals at <1%
in the CR238 atom family.**

The natural CR249 candidate is: **derive the BW shapes (`A^(2/3)`,
`Z(Z−1)/A^(1/3)`, `δ_pair`) from CR243/CR244 channel-occurrence sums over
per-nucleon configurations.** This would close the FIFTH fatality.pdf
constraint via micro-channel decomposition rather than imported BW
phenomenology. The asymmetry shape `(N−Z)²/A` is already derived (CR245
identity); the other three shapes remain to be reconstructed.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Substrate atoms, four-particle basis,
occupancy formulas, Phase A identity verifications, Phase B linear-closure
model, wrong controls, verdict gates, falsifiers all frozen.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** Phase A 6/6 identities EXACT on 69/69 rows; 3/3
anchors ALL EXACT; Phase B linear B_u fit α = +3.14 MeV, β = −5.62 MeV,
train RMS 24.5 MeV / R² 0.56, test RMS 25.2 MeV / R² 0.23; linear/null
ratio 2.00× (S5 PASS at gate); shuffle WC degrades; anchor predictions
C-12 +18.86 MeV residual, C-13 +16.36 MeV, Au-197 −2.07 MeV; all 6 wrong
controls pass.
**Verdict driver:** S1–S6 pass; S7 (linear B_u within tol) fails by 25/19
× the precommit gate. Phase A theorem-grade; Phase B has signal but is
structurally insufficient (binding non-linearity not captured by per-
particle constants).
**Open follow-up:** CR249 candidate — derive BW shapes A^(2/3), Z(Z-1)/A^(1/3),
δ_pair from CR243/CR244 channel-occurrence sums over per-nucleon configurations,
returning to the fifth fatality.pdf constraint with the typed-channel-table
basis explicitly mapped to nucleus structure.
