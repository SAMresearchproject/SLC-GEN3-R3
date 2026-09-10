# CR250 c_A Lock-and-Refit — Precommit

## Question (round5.pdf)

CR249 identified `c_A = 1/(S·L) = 1/1296` as the asymmetry coefficient at
0.44% relative deviation from the free-fit value — the first within-1%
typed binding coefficient. **CR250 tests whether `1/(S·L)` is structurally
real**: lock `c_A` at exactly `1/1296`, refit the remaining four
coefficients (`c_V, c_S, c_C, c_P`), and measure whether the locked-c_A
model retains BW-grade performance versus the free-c_A baseline.

If `1/(S·L)` is the real structural coefficient, the locked fit should be
essentially indistinguishable from the free fit. Wrong-control typed
alternatives should noticeably degrade.

## K3 framing

K3 status: PASS. `1/(S·L)` was identified in CR249 via a finite-candidate
search at 1% tolerance. CR250 tests its structural status: locking the
coefficient and observing fit retention is a structural prediction test
(not a fit). The wrong controls are precommitted typed alternatives that
test whether the choice of `1/(S·L)` over neighboring typed values is
uniquely supported.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   alpha_H = 2
M = 126  L = 162  V = 27  Theta = 18
kappa = 7117/768   g = 1/64

1/(S*L) = 1/(8*162) = 1/1296 = 7.71604938...e-4 u  (the locked c_A)
```

## Locked binding form

```text
B_SAM(Z, N) = c_V * A
            - c_S * A^(2/3)
            - c_C * Z * (Z - 1) / A^(1/3)
            - (1 / (S * L)) * (Q_mass - Q_sub)^2 / Q_mass
            + c_P * delta_pair

where Q_mass = 4*A*kappa, Q_sub = 8*(Z*kappa + (N-Z)*g),
      delta_pair = +1 if Z, N both even; -1 if both odd; 0 if A odd

Free coefficients to fit: c_V, c_S, c_C, c_P  (4 parameters)
Locked coefficient: c_A = 1/(S*L) = 1/1296 (substrate-typed value)
```

## Test set

```text
Train: CR239 Lane A non-anchor, A >= 16, N >= Z   (n = 35)
Test:  CR241 holdout, N >= Z                      (n = 20)
Anchors: C-12, C-13, Au-197 (reported separately)
```

## Baseline (free-c_A reference)

The free-c_A baseline is the CR249 Phase A fit on the same train set:
all 5 coefficients fitted by OLS.

```text
CR249 free fit (reproduced as CR250 baseline):
  c_V = +8.6350e-3 u
  c_S = +1.9626e-2 u
  c_C = +7.4196e-4 u
  c_A = +7.7504e-4 u  (free; close to 1/1296 = 7.7160e-4)
  c_P = +3.7517e-3 u

  Train RMS = 2.726 MeV   R^2 = 0.99458
  Test  RMS = 3.522 MeV   R^2 = 0.98502
```

## Locked test (c_A = 1/(S·L))

Fit `c_V, c_S, c_C, c_P` by OLS with the asymmetry term hard-coded to
`(1/(S*L)) * (Q_mass - Q_sub)^2 / Q_mass`. The asymmetry contribution is
subtracted from B_u observed before fitting the remaining 4-term model:

```text
B_u_residual_for_fit(P) = B_u_obs(P) + (1/(S*L)) * (Q_mass(P) - Q_sub(P))^2 / Q_mass(P)
                       (note: asymmetry enters with negative sign in B_SAM,
                        so we ADD it back to the LHS to fit the remaining terms)

Fit: B_u_residual = c_V*A - c_S*A^(2/3) - c_C*Z(Z-1)/A^(1/3) + c_P*delta_pair
```

## Wrong controls (round5.pdf)

Each WC re-runs the lock-and-refit with `c_A` set to a different typed
value:

```text
WC-A1   c_A = 1/L           = 1/162   = 6.173e-3   u   (about 8x too large)
WC-A2   c_A = 1/(S*M)       = 1/1008  = 9.921e-4   u   (about 28% too large)
WC-A3   c_A = 1/(S*R^2)     = 1/1152  = 8.681e-4   u   (about 13% too large)
WC-A4   c_A = 1/(R*L)       = 1/1944  = 5.144e-4   u   (about 33% too small)
WC-A5   c_A = 2/(S*L)       = 2/1296  = 1.543e-3   u   (2x too large)
WC-A6   c_A = (1/2)/(S*L)   = 1/2592  = 3.858e-4   u   (2x too small)
```

For each WC, fit the remaining 4 coefficients and report train + test RMS.
Pass condition per WC: WC train RMS > 1.20x the locked-c_A=1/(S*L) train RMS
(i.e., the alternative typed candidate degrades noticeably vs the locked
1/(S*L)).

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Locked train RMS <= 1.10x free train RMS
  S2  Locked test  RMS <= 1.10x free test  RMS
  S3  Locked train R^2 >= 0.95
  S4  Locked test  R^2 >= 0.95
  S5  All 6 wrong controls produce train RMS > 1.20x locked train RMS
  S6  Locked train RMS <= 5.0 MeV (still within BW range)

BOUNDARY conditions:
  B1  Locked retains BW-range fit (S3, S4, S6) but at least one WC
      fails the 1.20x degradation gate

FAIL conditions:
  F1  Locked train RMS > 1.10x free  (1/(S*L) is NOT the real value)
  F2  Locked test  RMS > 1.30x free  (1/(S*L) overfits train, fails holdout)
  F3  Locked train RMS > 10 MeV      (locked model blows up)
  F4  WC-A5 (2/(S*L)) OR WC-A6 (1/2 of 1/(S*L)) does NOT degrade by 1.20x
      (the specific scale of 1/(S*L) is not actually load-bearing)
```

Verdict precedence: STRONG_PASS > BOUNDARY > FAIL.

Expected outcome: STRONG_PASS. CR249 already showed the free-fit `c_A`
lands at `7.7504e-4 u`, only 0.44% above `1/(S*L) = 7.7160e-4 u`. Locking
at `1/(S*L)` should give essentially the same fit (within ~0.5% RMS shift)
and all wrong controls should significantly degrade.

## Outputs (locked file shape)

```text
CR250_summary.json                  — full readout, verdict
CR250_baseline_free_fit.csv         — CR249 free fit reproduction
CR250_locked_c_A_fit.csv            — locked-c_A=1/(S*L) fit
CR250_wrong_controls.csv            — per-WC fit + RMS comparison
CR250_anchor_cases.csv              — C-12, C-13, Au-197 predictions under locked model
CR250_input_manifest.csv            — input SHAs + row counts
HASHES.txt                          — SHA-256 of all CR250 artifacts
```

## Cryptographic chain (inputs)

```text
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md  = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR240_result.md  = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md  = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR243_result.md  = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md  = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_result.md  = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR247_result.md  = ed0eb192ca708e33fb6a044ac5a11e20cfdf1ab507b0bc241110a14646b662d7
CR248_result.md  = 34277d508ea5ca50ecdf8120aa1849022613c677acc6b6b95194bcc65c87b241
CR249_result.md  = 101e39c660138ecad23573c7eaae57b0a5dada60f86c7b73ea57976b073c55bb
CR250_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR250_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1   Locked train RMS exceeds 1.10x free fit train RMS: 1/(S*L) is not
     the structurally correct asymmetry coefficient at the precision the
     fit requires.
F2   Locked test RMS exceeds 1.30x free fit test RMS: the locked
     coefficient overfits train and fails on holdout.
F3   The model with locked c_A blows up (train RMS > 10 MeV).
F4   WC-A5 (2/(S*L)) or WC-A6 (1/2 of 1/(S*L)) does not degrade vs
     locked: the specific scale of 1/(S*L) is unidentifiable from the data.
F5   All alternative typed candidates (WC-A1..A4) fit comparably well:
     the typed-candidate search at 1% was a coincidence and the
     coefficient is not uniquely identifiable as 1/(S*L).
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, binding form, locked c_A value,
wrong controls, verdict gates, falsifiers all locked above the line.
