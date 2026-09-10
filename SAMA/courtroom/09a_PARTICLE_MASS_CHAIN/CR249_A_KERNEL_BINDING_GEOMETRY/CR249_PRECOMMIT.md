# CR249 A-Kernel Binding Geometry — Precommit

## Question (round4.pdf)

Does the SAM A-kernel `A(r) = r_s / r`, read on a finite SOB object of radius
`rho_A = A^(1/3)`, generate the binding-curvature shapes that CR248's linear
per-particle debit sum could not capture?

CR249 has two phases:

```text
Phase A: Prove the GEOMETRY is right.  Free-fit the five-shape model
   B_SAM = c_V * A
         - c_S * A^(2/3)
         - c_C * Z*(Z-1)/A^(1/3)
         - c_A * (Q_mass - Q_sub)^2 / Q_mass
         + c_P * delta_pair
   on Lane A train (A >= 16) and verify RMS is in the standard BW range
   (<= 5 MeV) with R^2 >= 0.95.

Phase B: Test typed-coefficient reduction.  Search typed-rational candidates
   for (c_V, c_S, c_C, c_A, c_P) over the CR238 atom family
   {R, D, S, Theta, M, L, V, kappa, g} at 5% and 1% tolerance.  Build the
   zero-free typed candidate and report train + test RMS.
```

The user's stated framing is "But first, prove the geometry is the right
one." Phase A is therefore the verdict-driving criterion; Phase B is
reported but does not by itself trigger FAIL.

## Geometric dictionary (round4.pdf)

```text
rho_A   = A^(1/3)                  (SOB radius coordinate)
V_A     = rho_A^3 = A              (volume = accumulated interior writes)
S_A     = rho_A^2 = A^(2/3)        (surface = exposed boundary, d/d_rho rho^3 = 3 rho^2)
R_A^-1  = rho_A^-1 = A^(-1/3)      (road / boundary traversal cost, from A(r) = r_s/r)
dQ      = Q_mass - Q_sub           (channel gap, from CR238/CR240)
```

Mapping to BW-shape interpretation in SAM language:

```text
B_V_SAM      ~ A             interior write accumulation
B_S_SAM      ~ A^(2/3)       under-coordinated boundary writes
B_C_SAM      ~ Z*(Z-1)/A^(1/3)   proton-pair pressure x 1/r boundary road
B_asym_SAM   ~ (dQ)^2 / Q_mass   channel gap squared per CR245 identity
                                = (N-Z)^2/A * 7093^2/(192*7117)
B_pair_SAM   ~ delta_pair    even-even / odd-odd parity term
```

## K3 framing

K3 status: PASS. The five shapes are derived structurally from the
A-kernel geometric reading specified in round4.pdf. The asymmetry shape is
already theorem-grade derived in CR245. The other four shapes are imported
from BW phenomenology AND independently motivated by the A-kernel
geometric reading (V from rho^3, S from rho^2, C from 1/rho, pair from
parity). Phase A tests whether these shapes fit B_u observed.

The fit method is OLS on a fixed feature basis; Phase A's gates are on
fit quality (train RMS, R^2). Phase B's gates are on typed-coefficient
recovery.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   alpha_H = 2
M = 126  L = 162  V = 27  Theta = 18
kappa = 7117/768   g = 1/64
mu_Q = 192/7117 u
```

## Locked binding form

```text
B_SAM(Z, N) = c_V * A
            - c_S * A^(2/3)
            - c_C * Z*(Z-1) / A^(1/3)
            - c_A * (Q_mass - Q_sub)^2 / Q_mass
            + c_P * delta_pair

where:
  A = Z + N
  Q_mass = 4 * A * kappa
  Q_sub  = 8 * (Z*kappa + (N-Z)*g)
  dQ     = Q_mass - Q_sub = (N-Z) * 7093/192   (CR245 exact identity)
  (dQ)^2 / Q_mass = (N-Z)^2 / A * 7093^2 / (192 * 7117)   (CR245 exact identity)

  delta_pair = +1  if (Z even AND N even)
             = -1  if (Z odd  AND N odd)
             =  0  if A odd (one even, one odd)

Target:  B_u = A - m_measured
```

Note: the asymmetry term is written in the user's preferred
`(Q_mass - Q_sub)^2 / Q_mass` form, which equals `(N-Z)^2 / A` times the
typed constant `7093^2 / (192 * 7117) ~ 36.8242`.  The fit operates on
the `(Q_mass - Q_sub)^2 / Q_mass` column directly to preserve the SAM
framing; coefficients are reported in atomic mass units (u).

## Test set

```text
Train: CR239 Lane A non-anchor, A >= 16, N >= Z
Test:  CR241 holdout, N >= Z
Anchors (reported separately): C-12, C-13, Au-197
Total: 71 isotopes; train fit on 35; test eval on 20; anchor reporting on 3
```

## Phase A — free-fit BW + SAM-asymmetry

```text
Fit method: ordinary least squares (numpy lstsq)
Design matrix columns: [A, -A^(2/3), -Z(Z-1)/A^(1/3), -(dQ)^2/Q_mass, +delta_pair]
Coefficients to fit: (c_V, c_S, c_C, c_A, c_P)
Report: fitted values in u and MeV; train RMS, R^2, n;
        test RMS (CR241 holdout), R^2, n;
        per-anchor B_u prediction and residual
```

## Phase B — typed-coefficient candidate search

```text
For each fitted coefficient, search the finite typed-rational candidate
family (same family as CR245):
  atoms             : {R, D, S, M, L, V, Theta, kappa, g, kappa-2g}
  reciprocals       : {1/x for x in atoms}
  products          : {1/(x*y) for x, y in atoms}
  ratios            : {x/y for x, y in atoms (non-special)}
  special           : kappa^2, g^2, kappa*g, kappa/atom, g/atom,
                      (kappa-2g)/atom, (D+2)/(R*(D+1)), (D^2+S)/(D*S^2),
                      7093^2/(192*7117)

For each coefficient, report:
  - nearest typed candidate (any sign)
  - relative deviation
  - within 5% / within 1%

Zero-free typed candidate: replace each fitted coefficient with its nearest
within-5% typed candidate (keep fitted if none); evaluate on train + test.
```

## Wrong controls

```text
WC-1   Drop volume:   c_V = 0; refit (4-term)
WC-2   Drop surface:  c_S = 0; refit (4-term)
WC-3   Drop Coulomb:  c_C = 0; refit (4-term)
WC-4   Drop asym:     c_A = 0; refit (4-term)
WC-5   Drop pairing:  c_P = 0; refit (4-term)
WC-6   Replace surface A^(2/3) with A^(1/2) (wrong geometric scaling)
WC-7   Replace road 1/A^(1/3) with 1/A^(2/3) (wrong geometric scaling)
WC-8   Replace pairing delta_pair with delta_pair/sqrt(A) (BW form variant)
WC-9   Shuffle B_u labels (seed 20260623), refit

Pass condition per shape-removal WC (WC-1..5): RMS degrades by at least 1.5x
                                                vs canonical 5-shape fit
Pass condition for WC-6, WC-7 (geometric scaling): RMS degrades by at least 1.2x
Pass condition for WC-8 (pairing variant): REPORT both, no degradation gate
Pass condition for WC-9 (shuffle): RMS degrades by at least 2x
```

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Phase A train RMS <= 5 MeV
  S2  Phase A test RMS  <= 5 MeV
  S3  Phase A train R^2 >= 0.95
  S4  Phase A test R^2  >= 0.95
  S5  All shape-removal WCs (WC-1..5) degrade canonical RMS by >= 1.5x
  S6  Geometric-scaling WCs (WC-6, WC-7) degrade by >= 1.2x
  S7  WC-9 (shuffle) degrades by >= 2x

BOUNDARY conditions:
  B1  S1, S2, S3, S4 hold (Phase A geometry-fit close)
  B2  Some but not all of S5..S7 fail (some shapes carry less signal than threshold)

FAIL conditions:
  F1  Phase A train RMS > 10 MeV (geometry does not capture binding)
  F2  Any shape-removal WC does NOT degrade (that shape is structurally irrelevant)
  F3  Shuffle does not degrade (the model is fitting noise)
```

Phase B (typed-coefficient search) is reported but does NOT contribute to
the STRONG_PASS / BOUNDARY / FAIL decision. The user's framing is that
Phase A proves the geometry; Phase B is the follow-up question of whether
the coefficients reduce to typed rationals (which CR245 already showed
lands at "in the neighborhood, not on the dot").

## Outputs (locked file shape)

```text
CR249_summary.json                  — full readout, verdict
CR249_phase_a_fit.csv               — fitted coefficients + per-anchor predictions
CR249_typed_candidates.csv          — per-coefficient typed-rational search
CR249_zero_free_predictions.csv     — train + test residuals under zero-free typed candidate
CR249_wrong_controls.csv            — per-WC RMS comparison
CR249_anchor_cases.csv              — C-12, C-13, Au-197 detailed breakdown
CR249_input_manifest.csv            — input SHAs + row counts
HASHES.txt                          — SHA-256 of all CR249 artifacts
```

## Cryptographic chain (inputs)

```text
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md  = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md  = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md  = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md  = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR242_result.md  = 091397fec625d216e437a76a50670250bc47a3a97a7d10f38efab53096f18e4d
CR243_result.md  = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md  = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_result.md  = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR247_result.md  = ed0eb192ca708e33fb6a044ac5a11e20cfdf1ab507b0bc241110a14646b662d7
CR248_result.md  = 34277d508ea5ca50ecdf8120aa1849022613c677acc6b6b95194bcc65c87b241
CR249_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR249_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1   Phase A train RMS > 10 MeV: A-kernel geometric shapes do not capture
     binding curvature.
F2   Phase A R^2 < 0.85: shapes have insufficient explanatory power.
F3   Any shape-removal WC (WC-1..5) preserves RMS (no degradation):
     that shape is structurally irrelevant and the A-kernel reading is wrong.
F4   Geometric-scaling WCs (WC-6, WC-7) do not degrade: the specific A^(2/3)
     surface and A^(-1/3) road scalings are not load-bearing.
F5   Shuffle WC-9 does not degrade: the model is fitting noise.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, binding form, geometric dictionary,
Phase A fit method, Phase B typed-candidate search, wrong controls, verdict
gates, falsifiers all locked above the line.
