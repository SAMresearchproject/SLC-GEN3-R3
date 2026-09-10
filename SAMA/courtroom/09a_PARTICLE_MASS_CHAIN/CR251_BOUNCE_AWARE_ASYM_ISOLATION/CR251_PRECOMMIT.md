# CR251 Bounce-Aware Asymmetry Coefficient Isolation — Precommit

## Question (round6.pdf)

CR250 confirmed `c_A = 1/(S·L) = 1/1296` is structurally real (locked
fit indistinguishable from free fit) but found that the alternative
`c_A = 1/(S·R²) = 1/1152` was a near-degenerate WC because the
4-coefficient refit absorbs the 12.5% perturbation. The two candidates
differ by exactly the CR222 carrier-bounce factor `9/8 = L/R²`.

**CR251 asks whether the data can statistically discriminate `1/(S·L)`
from `1/(S·R²)`** through three tests that strip away the parameter-
degeneracy that hid the discrimination in CR250:

```text
Phase A: ORTHOGONALIZED ISOLATION (Frisch-Waugh-Lovell)
  Project both B_u and X_A = (Q_mass-Q_sub)^2/Q_mass away from the
  non-asymmetry design matrix X_0 = [A, A^(2/3), Z(Z-1)/A^(1/3), delta_pair].
  Compute the isolated c_A_orth = (X_A_perp . B_perp) / (X_A_perp . X_A_perp).
  Report the OLS standard error SE(c_A_orth) and test whether 1/(S*L)
  and 1/(S*R^2) lie inside the SE band.

Phase B: ISOBARIC CONTRASTS (same-A pairs)
  For pairs with the same A but different (Z, N), volume and surface
  cancel.  Fit Delta_B = -c_C*Delta(Z(Z-1)/A^(1/3)) - c_A*Delta(X_A).
  Compare fitted c_A to 1/(S*L) and 1/(S*R^2).

Phase C: LARGE |N-Z| STRESS LANE
  Filter to rows with |N-Z| above a precommitted threshold (>= 20).
  Re-run Phase A orthogonalized isolation on this subset where the
  asymmetry term has maximum leverage.
```

If `1/(S·L)` lies inside the SE band on all three tests and `1/(S·R²)`
lies outside, the discrimination is statistically real, not just
structurally preferred.

## K3 framing

K3 status: PASS. The orthogonalization, isobaric contrast, and large
|N-Z| stress are standard statistical isolation techniques; their use
here was specified in round6.pdf above the line. The two typed
candidates `1/(S·L)` and `1/(S·R²)` are the locked comparison targets;
no fitted value can change them. The test reports which (if either)
is inside the data-driven SE band.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   M = 126   L = 162   V = 27   Theta = 18
kappa = 7117/768   g = 1/64
L = R^2 * 9/8 = 162   (CR217/CR222/CR229 closed-ledger identity)

1/(S*L)  = 1/(8*162) = 1/1296 = 7.71604938e-4 u  (0.7188 MeV)  [closed-ledger, bounce-aware]
1/(S*R^2)= 1/(8*144) = 1/1152 = 8.68055556e-4 u  (0.8086 MeV)  [bare capacity, no bounce]
Ratio 1/(S*L) : 1/(S*R^2)  =  R^2/L  =  144/162  =  8/9
```

## Locked binding form

```text
B_SAM(Z, N) = c_V * A
            - c_S * A^(2/3)
            - c_C * Z*(Z-1) / A^(1/3)
            - c_A * (Q_mass - Q_sub)^2 / Q_mass
            + c_P * delta_pair

Target:  B_u = A - m_measured
```

The non-asymmetry design matrix `X_0` for orthogonalization:

```text
X_0 = [A, A^(2/3), Z*(Z-1)/A^(1/3), delta_pair]   (4 columns)
X_A = (Q_mass - Q_sub)^2 / Q_mass                  (1 column, asymmetry feature)
```

Note: signs on `X_0` columns are dropped because OLS is sign-symmetric;
the orthogonalization is on the column subspace, not the signed form.

## Test corpus

```text
All N >= Z rows from CR239 Lane A + CR241 holdout = 69 rows
For Phase A, restrict to A >= 16 to match CR249/CR250 (n = 55)
For Phase B (isobaric), enumerate all (i, j) with A_i = A_j (any A)
For Phase C, restrict to |N - Z| >= 20 (subset of Phase A corpus)
```

## Phase A — Orthogonalized Coefficient Isolation

```text
Build X_0 (4 cols) and X_A (1 col) for the A >= 16 corpus.
Compute the projection matrix P_0 = X_0 (X_0^T X_0)^(-1) X_0^T
Compute B_perp = (I - P_0) B_u
Compute X_A_perp = (I - P_0) X_A
Compute c_A_orth = (X_A_perp . B_perp) / (X_A_perp . X_A_perp)

Standard error:
  residuals = B_perp - c_A_orth * X_A_perp
  dof = n - 5  (5 = 4 non-asym + 1 asym coefficient)
  sigma2_hat = sum(residuals^2) / dof
  SE(c_A_orth) = sqrt( sigma2_hat / (X_A_perp . X_A_perp) )

t-tests:
  t_SL  = (c_A_orth - 1/(S*L)) / SE(c_A_orth)
  t_SR2 = (c_A_orth - 1/(S*R^2)) / SE(c_A_orth)
  p-values (two-sided) reported

Decision:
  STRONG isolation if |t_SL| < 1.96 AND |t_SR2| >= 2.58
    (1/(S*L) inside 95% CI; 1/(S*R^2) outside 99% CI)
  WEAK isolation if |t_SL| < 1.96 AND |t_SR2| < 1.96
    (both inside 95% CI; cannot discriminate)
  REJECT if |t_SL| >= 2.58
    (1/(S*L) outside 99% CI; the structural identification is wrong)
```

## Phase B — Isobaric Contrasts

```text
Enumerate all pairs (i, j) with A_i = A_j (i < j) over the full N >= Z corpus.
For each pair, compute:
  Delta_B    = B_u_i - B_u_j
  Delta_Coul = Z_i(Z_i-1)/A_i^(1/3) - Z_j(Z_j-1)/A_j^(1/3)
  Delta_X_A  = X_A_i - X_A_j

Fit 2-parameter OLS on pair-differences:
  Delta_B = -c_C * Delta_Coul - c_A * Delta_X_A
  (volume and surface differences are zero by construction since A_i = A_j;
   pairing difference is identically 0 if both pair-class match, else +/-2)

Compute fitted c_A_isobaric and its SE; report t-tests vs 1/(S*L) and 1/(S*R^2).
If no isobaric pairs exist in the corpus, this phase reports "INSUFFICIENT_DATA".
```

## Phase C — Large |N-Z| Stress Lane

```text
Filter the A >= 16 corpus to rows with |N-Z| >= 20.
Re-run Phase A orthogonalized isolation on this filtered subset.
Report c_A_orth_stress, SE, t-tests vs 1/(S*L) and 1/(S*R^2).
```

## Wrong controls

```text
WC-1   Shuffle B_u labels (seed 20260623), re-run Phase A.
       c_A_orth should be near zero with large SE.

WC-2   Use only N = Z rows (X_A ~ 0 for symmetric).
       Phase A should be ill-conditioned or return c_A near 0.

WC-3   Add a random feature to X_0 (Gaussian noise, seed 20260623);
       repeat Phase A.  c_A_orth should be essentially unchanged
       (proves orthogonalization is selective).

WC-4   Permute X_A across rows (seed 20260623), re-run Phase A.
       c_A_orth should be near zero (no real asymmetry-binding correlation).
```

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Phase A: |t_SL| < 1.96 AND |t_SR2| >= 2.58
      (1/(S*L) inside 95% CI; 1/(S*R^2) outside 99% CI)
  S2  Phase C (large |N-Z| stress): |t_SL_stress| < 2.58 AND |t_SR2_stress| >= 1.96
      (1/(S*L) inside 99% CI; 1/(S*R^2) outside 95% CI in the high-leverage subset)
  S3  Phase B (isobaric): if pairs available, |t_SL_iso| < 1.96 AND
      |t_SR2_iso| >= 1.96; else skip (INSUFFICIENT_DATA does not block)
  S4  All wrong controls pass (WC-1, WC-2, WC-4 give c_A_orth near zero;
      WC-3 gives c_A_orth essentially unchanged)

BOUNDARY conditions:
  B1  Phase A: |t_SL| < 1.96 AND |t_SR2| < 2.58
      (1/(S*L) inside 95% CI but 1/(S*R^2) is not clearly excluded)

FAIL conditions:
  F1  Phase A: |t_SL| >= 2.58
      (1/(S*L) outside 99% CI; structural identification rejected)
  F2  Phase A: |t_SR2| < |t_SL|
      (1/(S*R^2) is closer to the data than 1/(S*L); bounce-aware reading wrong)
```

## Outputs (locked file shape)

```text
CR251_summary.json                       — full readout, verdict
CR251_phase_a_orthogonalized.csv         — Phase A c_A_orth, SE, t-tests
CR251_phase_b_isobaric.csv               — Phase B isobaric pair list and fit
CR251_phase_c_stress.csv                 — Phase C large |N-Z| subset fit
CR251_wrong_controls.csv                 — per-WC c_A_orth, SE
CR251_input_manifest.csv                 — input SHAs + row counts
HASHES.txt                               — SHA-256 of all CR251 artifacts
```

## Cryptographic chain (inputs)

```text
CR217_result.md  = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md  = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md  = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md  = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR245_result.md  = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR249_result.md  = 101e39c660138ecad23573c7eaae57b0a5dada60f86c7b73ea57976b073c55bb
CR250_result.md  = 84d6aa32436da9657108eb707983fb3166f7d0674c90d9bf2b8d63c0527fa643
CR251_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR251_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1   Phase A places 1/(S*L) outside 99% CI: the structural identification
     is statistically rejected.
F2   |t_SR2| < |t_SL| (Phase A): 1/(S*R^2) is statistically closer to the
     data than 1/(S*L); bounce-aware reading is wrong.
F3   Phase C (large |N-Z|) reverses Phase A: high-leverage subset prefers
     1/(S*R^2) over 1/(S*L); the bounce-aware reading does not survive
     the stress lane.
F4   Phase B isobaric contrasts (if available) strongly prefer
     1/(S*R^2): isobaric discrimination is unambiguous and against
     the bounce-aware reading.
F5   WC-3 (random feature added to X_0) changes c_A_orth substantially:
     the orthogonalization is not selective and the c_A estimate is
     unstable.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, binding form, projection
matrix, t-test thresholds, isobaric-pair fit, large |N-Z| stress lane,
wrong controls, verdict gates, falsifiers all locked above the line.
