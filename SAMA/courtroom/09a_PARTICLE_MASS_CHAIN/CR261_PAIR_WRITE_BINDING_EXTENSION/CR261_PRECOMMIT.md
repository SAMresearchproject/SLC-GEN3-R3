# CR261 — Pair-Write Binding Extension

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** BINDING_CLOSURE_EXTENSION_CR (downstream of CR245 + CR248)
**Sealed by:** Sean Brady, 2026-06-30
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

CR248 sealed BOUNDARY: the four-particle algebraic decomposition (proton +
balanced neutron + excess neutron + electron) closes 69/69 rows exact at
Phase A, but the linear `B_u = α·Z + β·(N−Z)` model in Phase B leaves
24.5 MeV RMS — ~7× CR245's BW-shape fit (2.78 MeV). CR248 explicitly named
the obstacle as **non-linear pair-write terms from BW phenomenology** —
the surface, Coulomb, asymmetry, and pairing shapes that linear-in-(Z, N−Z)
cannot capture.

Does extending CR248's four-particle decomposition with the BW pair-write
terms — using CR245's structurally-derived asymmetry-term identity at exact
arithmetic — close the binding residual to within CR245-grade precision
(Lane A train RMS ≤ 4 MeV) across the test holdout and propagate cleanly
to the full SOB126 ledger (126 elements, Z = 1 to Z = 126)?

## Honest Framing

K3 status: STRUCTURAL CLOSURE EXTENSION TEST.

- **Phase A** (regression): CR248's four-particle algebraic identity (six
  components: u, d, e, Q_mass, Q_sub, dQ) must still close exact on every
  row in the train + test sets. This is a regression check — CR248 stays
  sealed; we verify the spine carries forward unchanged.

- **Phase B** (the named extension): five-term BW model with the asymmetry
  coefficient locked from CR245 (theorem-grade, derived from substrate
  atoms via `(Q_mass − Q_sub)²/Q_mass = (N−Z)²/A · 7093²/(192·7117)`); the
  remaining four coefficients (volume `a`, surface `b`, Coulomb `c`,
  pairing `e`) fitted by OLS on Lane A train, then evaluated on Lane B
  holdout and the full 126-element ledger.

- **Phase C** (propagation): apply the fitted BW form to the SOB126 ledger,
  reporting per-element residuals and the Z = 119–126 frontier predictions.

The CR is an extension of CR248 — it does not retract CR245 (which already
established the BW shapes admit typed-rational candidates) and does not
retract CR248 (which sealed the algebraic spine). It closes the named gap
that prevented CR248 from reaching PASS by adding the pair-write terms
CR248 itself identified as required.

## Locked Substrate Atoms (read-only from CR238)

```text
R = 12     D = 3     S = 8     alpha_H = 2
M = 126    L = 162   V = 27    Theta = 18
kappa = 7117/768      g = 1/64
mu_Q  = 192/7117 u
asymmetry_identity_coefficient = 7093²/(192·7117) = 50310649/1366464
                                                  ≈ 36.8242 ...
```

## Locked Model — Five-Term BW with Asymmetry Theorem-Grade

```text
B_u(Z, N, A) = a · A
              − b · A^(2/3)
              − c · Z(Z−1) / A^(1/3)
              − d_locked · (N−Z)² / A
              − e · δ_pair(Z, N) · A^(−1/2)

where
  d_locked = 7093² / (192 · 7117)        (CR245 derived; not fit)
  δ_pair(Z, N) = +1   if Z even AND N even
                 −1   if Z odd  AND N odd
                  0   otherwise (odd-A nuclei)
```

The asymmetry term's coefficient is forced by CR245's structural derivation
and verified at exact Fraction precision on every row before fitting begins.
Only `(a, b, c, e)` are fit by OLS.

## Locked Phase A — Regression of CR248 Four-Particle Algebra

For each row in train + test (excluding rows with N < Z, per CR248 scope):

```text
n_p = Z          n_balanced_neutron = Z
n_excess_n = N − Z   n_electron = Z

Sum_j n_j · u_j        = 2Z + N
Sum_j n_j · d_j        = Z + 2N
Sum_j n_j · e_j        = Z
Sum_j n_j · Q_mass_j   = 4·A·κ
Sum_j n_j · Q_sub_j    = 8Z·κ + (N−Z)/8
Sum_j n_j · dQ_j       = (N−Z) · 7093/192
```

All six identities must close at exact Fraction equality on every row.

## Locked Phase B — Fit Protocol

```text
Train set:  CR248_train_lane_a.csv          (51 rows; AME2020 hard-measured)
            Lane A subset: A ≥ 16 AND N ≥ Z (matches CR245 / CR248 protocol)

Test set:   CR248_test_holdout.csv          (20 rows; holdout)
            Lane A subset: A ≥ 16 AND N ≥ Z

Asymmetry coefficient: locked = 7093²/(192·7117)

Fit (a, b, c, e) by OLS on train, predicting:
  B_u_residual_target = B_u_observed + d_locked · (N−Z)²/A
                      (the asymmetry term is moved to the predictor side
                       since it is locked; OLS recovers the remaining four)

Equivalently, regress B_u_observed against
  [A, A^(2/3), Z(Z−1)/A^(1/3), δ_pair·A^(−1/2)]
with the asymmetry term carried by d_locked, then back out (a, b, c, e).
```

B_u observed values come from AME2020 atomic-mass-excess (Δ = m_measured − A
in u) via standard convention. Coefficients reported in MeV; intermediate
arithmetic in u.

## Sealed PASS Gates

```text
G1  Asymmetry identity verified exact on all 51 train + 20 test rows
    (Fraction equality at the (Q_mass − Q_sub)² / Q_mass level).

G2  Lane A train RMS  ≤ 4.0 MeV   (CR245 reached 2.78 MeV; this is a
                                   modest target consistent with a
                                   regression on the same data)

G3  Lane A test  RMS  ≤ 5.0 MeV

G4  ≥ 5× improvement over CR248 Phase B linear closure (24.52 MeV train RMS):
    that is, train_RMS ≤ 24.52 / 5 = 4.904 MeV
    (subsumed by G2; written here as the explicit "CR248 gap closes" gate)

G5  Anchor cases predicted within 5 MeV residual:
    C-12 (Z=6, N=6, A=12)
    C-13 (Z=6, N=7, A=13)
    Au-197 (Z=79, N=118, A=197)

G6  Precommit hash verified at runner load AND forbidden-file open() guard
    not tripped. Whitelist: this precommit, the runner source, the two
    CR248 data files (by hash), the SOB126 ledger (by hash), the CR261
    output files.

PASS  iff G1 AND G2 AND G3 AND G4 AND G5 AND G6 all hold.

BOUNDARY  iff G1 holds AND (G2 OR G3 misses by ≤ 2 MeV; or anchor case
          misses by ≤ 10 MeV) — closes the CR248 gap structurally but
          falls short of full CR245-grade precision.

FAIL  iff G1 fails (asymmetry identity broken) or G2 misses by > 2 MeV
      or precommit/forbidden-file gate trips.
```

## Reported Evidence (not gated)

```text
E1  Phase A regression: 69/69 four-particle identities match exact.
E2  Fitted coefficients (a, b, c, e) with standard errors and R² (train/test).
E3  Per-row residuals at fitted BW for train + test.
E4  Propagation to SOB126 ledger: residual mean, RMS, distribution.
E5  Jerroldium frontier predictions: B_u for Z = 119, 120, 121, 122, 123,
    124, 125, 126 under the fitted BW form (no observation to compare).
E6  Comparison to CR245's fit: are the (a, b, c, e) values consistent
    within standard errors? (Replication check; not gated.)
```

## Pre-Registered Frozen Inputs

| field | sha256 | description |
| --- | --- | --- |
| CR248_train_lane_a.csv | `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc` | 51-row Lane A AME2020 train (hash-locked in CR248) |
| CR248_test_holdout.csv | `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8` | 20-row Lane A holdout |
| SOB126_ledger.csv (CR250) | `3bfdd083457b187c156bf331b2997bb904be1f45adb335a724c12100d9c6e72b` | 126-element substrate ledger |

The runner whitelists exactly these three input paths plus this precommit
and the runner source.

## Rule-9 Line

```text
This test could have falsified the claim that extending CR248's four-
particle algebraic decomposition with the BW pair-write terms — using
CR245's structurally-derived asymmetry-term identity at exact arithmetic
precision — reduces the binding closure residual to within CR245-grade
precision (Lane A train RMS ≤ 4 MeV) and propagates cleanly to the full
126-element SOB ledger. It could have failed by: (i) the asymmetry
identity breaking on any row, (ii) Lane A train RMS exceeding 4 MeV,
(iii) Lane A test RMS exceeding 5 MeV, (iv) anchor cases exceeding 5 MeV
residual, or (v) failure to improve on CR248's linear closure by at
least 5×.
```

## What This CR Seals

If PASS: the named gap CR248 identified (linear B_u model insufficient for
binding curvature) is closed by adding the BW pair-write terms with CR245's
asymmetry identity carried theorem-grade. The four-particle algebraic
spine plus five-term BW closure reproduces binding across the 126-element
SOB ledger at CR245-grade precision. The Jerroldium frontier (Z = 119–126)
predictions are emitted under the fitted form for later forecast-lock
sealing.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR248@09a (algebraic spine sealed BOUNDARY) | precommit `7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa` |
| CR245@09a (BW fit + asymmetry identity sealed) | per branch HASHES |
| CR247@09a (SOB inverse decomp STRONG_PASS) | per branch HASHES |
| CR250@09a (SOB126 ledger) | per branch HASHES |
| CR238@09a (substrate spine compaction) | per branch HASHES |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
