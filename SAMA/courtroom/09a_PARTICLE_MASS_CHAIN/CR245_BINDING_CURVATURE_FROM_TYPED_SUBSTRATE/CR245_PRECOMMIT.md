# CR245 Binding-Curvature from Typed Substrate — Precommit

## Question

Can the positive binding residual `B_u(P) = A − m_measured(P)` be expressed in
the CR238/CR240 substrate atoms with the asymmetry term derived from the
two-kernel structure `(Q_mass − Q_sub)²/Q_mass`, and how much of the
remaining BW-form coefficient set `{a, b, c, e}` reduces to typed rationals
in `{R, D, S, Θ, M, ℒ, V, κ, g}`?

## Path framing (Sean's bind.pdf plan)

```text
B_u = a·A
    − b·A^(2/3)
    − c·Z(Z−1)/A^(1/3)
    − d·(Q_mass − Q_sub)²/Q_mass
    + e·δ_pair / sqrt(A)
```

Stage 1: lock the structural asymmetry-term identity (closed form derivation
from CR238/CR240, no fit).
Stage 2: fit the remaining coefficients on Lane A train; report fitted
values + typed-rational candidate matches.
Stage 3: construct the zero-free typed candidate using typed rationals where
available; report Lane A train + CR241 holdout residual.
Stage 4: wrong controls (substrate-constant perturbation; term removal;
typed-candidate substitution).

## K3 framing — STRUCTURAL PREDICTION TEST, not blind discovery

CR245 is a structural prediction test. The asymmetry-term identity is
derived algebraically from CR238/CR240 above the line:

```text
Q_mass = 4·A·κ                                          (CR240)
Q_sub  = S·G_sub = 8·(Z·κ + (N−Z)·g)                    (CR238/CR239)
Q_mass − Q_sub = 4κ(A − 2Z) − 8(N−Z)g
              = (N−Z)·4·(κ − 2g)
              = (N−Z)·(7117 − 24)/192
              = (N−Z)·7093/192

(Q_mass − Q_sub)² / Q_mass = (N−Z)²/A · 7093²/(192·7117)
                           = (N−Z)²/A · 50310649/1366464
                           ≈ (N−Z)²/A · 36.8242
```

This is locked as a structural identity, to be verified per row at exact
arithmetic precision (Fraction). It is K3-clean: the algebraic derivation is
unconditional on the data; the per-row check is reproduction, not fit.

The BW shape (volume/surface/Coulomb/pairing) is imported phenomenology and
is acknowledged as such. The K3 framing is honest: this CR tests *whether*
the four imported BW shapes admit typed-rational coefficients in
`{R, D, S, Θ, M, ℒ, V, κ, g}` and reports the result. It does not claim
those shapes were derived blindly from SAM substrate.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   alpha_H = 2
M = 126  L = 162  Theta = 18   V = 27
kappa = 7117/768   g = 1/64
mu_Q  = 192/7117 u
```

## Locked structural identity (Stage 1)

```text
For every row P with A >= 1 and Q_mass(P) > 0:

  (Q_mass(P) − Q_sub(P))² / Q_mass(P)  ==  (N−Z)²/A · 7093²/(192·7117)

evaluated as exact Fractions on both sides.  Match tolerance: 0 (exact).
```

## Locked BW form (Stage 2 — fit on Lane A train)

```text
B_u(P) = a·A
       − b·A^(2/3)
       − c·Z·(Z−1)/A^(1/3)
       − d·(N−Z)²/A · 7093²/(192·7117)
       + e·δ_pair / sqrt(A)

where  δ_pair = +1 if (Z even AND N even)
              = -1 if (Z odd  AND N odd)
              =  0 if (A odd)

Fit is unweighted ordinary least squares on the train set.
Train set: Lane A rows with A >= 16 (skip light-nucleus regime where BW
            shape is known to break down).
Coefficients are reported in atomic mass units u.
```

Note: the asymmetry term is written equivalently in either form:
`d·(Q_mass-Q_sub)²/Q_mass`  ==  `d · 36.8242 · (N−Z)²/A`. Fit uses the
(N−Z)²/A form for numerical stability; coefficient is rescaled by 36.8242
into the (Q_mass-Q_sub)²/Q_mass form for reporting both representations.

## Typed-rational candidate family (Stage 3)

The candidate atoms and product-rationals to consider for each coefficient:

```text
Atoms:           {R=12, D=3, S=8, M=126, L=162, V=27, Theta=18}
                 plus kappa = 7117/768, g = 1/64
Operations:      reciprocals, products, sums (kappa-2g),
                 simple products of atoms (R*M, R*D, S*M, etc.)
Match tolerance: <= 5% relative for "typed coefficient match"
                 <= 1% relative for "tight typed coefficient match"
```

The runner builds a finite candidate set deterministically from the precommit
list and reports, for each fitted coefficient:

```text
- nearest typed-rational candidate
- relative deviation
- whether within 5% (typed match)
- whether within 1% (tight typed match)
```

## Stage 4 — Zero-Free Typed Candidate

For each fitted coefficient, substitute the nearest 5%-typed candidate if
one exists; otherwise leave the coefficient as fitted (flag substitution).
Re-evaluate B_u(P) on train + holdout with the substituted coefficients.

Report:
- per-coefficient: substitution status, typed value, fitted value, relative
  deviation
- per-row residual: B_u_observed - B_u_typed_candidate
- RMS residual on train + holdout
- comparison: typed-candidate RMS vs fitted-coefficient RMS
- "typed_pass" flag: True iff typed-candidate train RMS within 1.5x fitted
  RMS AND typed-candidate holdout RMS within 1.5x fitted holdout RMS

## Wrong Controls

```text
WC-R1   R = 10  (re-derive asymmetry identity constant: 5083^2 / (160*5083))
WC-R2   R = 11  asymmetry constant changes
WC-R3   R = 13  asymmetry constant changes
WC-D1   D = 2   no direct effect on asymmetry identity (D doesn't appear)
                but affects D-dependent coefficient candidates if used
WC-D2   D = 4   ditto
WC-T1   Remove the asymmetry term entirely (d = 0): refit other 4 coefs,
        compare RMS degradation
WC-T2   Replace SAM asymmetry term with raw (N-Z)^2/A and refit (these are
        identical up to constant, so should be equivalent)
WC-T3   Replace BW pairing form with no pairing (e=0): refit, compare
WC-A1   Shuffle isotope rows in train set (seed 20260623): refit, compare
        - degrades if shape carries signal
WC-A2   Replace volume term aA with aA^(1.1) (slight shape perturbation)
WC-CT   Constant typed-candidate substitution: replace fitted (a,b,c,e) with
        nearest typed-rational regardless of tolerance, report what happens
```

Pass condition per WC: WC degrades fit RMS or breaks structural identity
where applicable.

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Asymmetry identity exact on every train + test row
  S2  BW fit converges with train RMS <= 5 MeV (reasonable BW range)
  S3  At least 3 of 5 coefficients have typed candidates within 5%
  S4  Zero-free typed candidate train RMS within 1.5x fitted train RMS
  S5  Zero-free typed candidate holdout RMS within 1.5x fitted holdout RMS
  S6  All R-perturbation WCs break the asymmetry identity (S1)
  S7  WC-T1 (asymmetry removal) degrades fit RMS >= 50%
  S8  WC-A1 (row shuffle) degrades fit RMS substantially

BOUNDARY conditions:
  B1  S1 and S2 hold (asymmetry identity exact + reasonable BW fit)
  B2  S3 fails (fewer than 3 of 5 coefficients type within 5%)
  B3  S6, S7 hold (substrate atoms are load-bearing where they appear)

FAIL conditions:
  F1  Asymmetry identity fails on any row: the (Q_mass-Q_sub)^2/Q_mass
      structural derivation is wrong
  F2  BW fit fails to converge or train RMS > 10 MeV
  F3  WC-T1 does not degrade: the SAM asymmetry term is structurally
      irrelevant (the shape works equally well without it)
```

Verdict precedence: STRONG_PASS > BOUNDARY > FAIL.

Expected outcome (based on exploration consistent with CR242): BOUNDARY.
The asymmetry identity is exact; the other coefficients fit but do not
reduce to clean typed rationals at <= 5%.  This is honest structural
progress: one BW term is now derived from CR238/CR240 two-kernel structure;
the remaining four are phenomenological with non-typed coefficients in
this substrate atom family.

## Outputs (locked file shape)

```text
CR245_summary.json                         — full readout, verdict
CR245_expanded_sob_table.csv               — per-row Z,N,A,Q_mass,Q_sub,dQ,B_u,
                                              asym_lhs, asym_rhs, asym_match
CR245_bw_fit_train.csv                     — fitted coefficients, train residuals
CR245_typed_candidates.csv                 — per-coefficient typed-candidate search
CR245_zero_free_predictions.csv            — train + holdout zero-free predictions
CR245_wrong_controls.csv                   — per-WC degradation
CR245_input_manifest.csv                   — input SHAs + row counts
HASHES.txt                                 — SHA-256 of all CR245 artifacts
```

## Cryptographic chain (inputs)

```text
CR114_result.md (capacity R^2 + split-loss)             = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R^2 * 9/8 closed ledger)         = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md (carrier ledger 12+1 closed sum)        = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)          = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md (substrate spine compaction)            = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md (native mass / gravity FAIL)            = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md (rest-mass channel STRONG_PASS)         = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md (holdout)                               = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR242_result.md (binding-curvature BOUNDARY)            = 091397fec625d216e437a76a50670250bc47a3a97a7d10f38efab53096f18e4d
CR243_result.md (typed channel table)                   = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md (unequal-pair typed forms)              = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_train_lane_a.csv (frozen snapshot)                = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR245_test_holdout.csv (frozen snapshot)                = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1   Asymmetry identity fails on any row: the (Q_mass - Q_sub)^2 / Q_mass =
     (N-Z)^2/A * 7093^2/(192*7117) derivation is structurally wrong.
F2   No BW coefficient maps to a typed rational within 5%: SAM substrate
     atoms do not contain the coefficient structure of nuclear binding in
     this representation.
F3   Zero-free typed candidate explodes (RMS >> fitted RMS): typed
     coefficients are not even approximately right.
F4   WC-T1 (asymmetry removal) does not degrade: the asymmetry term is
     irrelevant to B_u; SAM contributes nothing structural.
F5   WC-A1 (row shuffle) does not degrade: the BW shape is fitting noise,
     not structure.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, BW form, asymmetry identity,
typed-candidate family, wrong controls, verdict gates, falsifiers all
locked above the line.
