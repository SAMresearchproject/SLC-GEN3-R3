# CR248 SOB Micro-Channel Debit Occupancy Map — Precommit

## Question

Per Sean's fatality.pdf third layer: given (Z, N), find the integer-occupancy
vector `n_j` over a typed micro-channel basis such that the sum reproduces
the sealed SOB target vector AND closes the surface-debit / binding target
`Sum_j n_j * s_debit_j ~ B_u(Z, N)`.

This CR extends CR247's two-particle decomposition (balanced + excess) to a
four-particle decomposition (proton + balanced neutron + excess neutron +
electron). It then attempts to close the FIFTH fatality.pdf constraint
(surface debit / B_u) by fitting per-particle s_debit values on Lane A
train and reporting whether the linear closure suffices.

## Honest framing

K3 status: STRUCTURAL PREDICTION TEST.

- Phase A (algebraic): the four-particle basis vectors are derived from
  CR238/CR240 by particle-level disaggregation of CR247's two-particle
  basis. Per-particle (u, d, e, Q_mass, Q_sub, dQ) values are forced by
  the source/mass/substrate identity formulas and must close exactly.
- Phase B (B_u closure): per-particle surface-debit s_p, s_n_b, s_n_e, s_e
  are fitted on CR239 Lane A train, then evaluated on CR241 holdout. The
  hypothesis is that linear per-particle debits suffice. The expected
  outcome is BOUNDARY because binding energy is non-linear in Z and N - Z;
  per-particle constants cannot capture A^(2/3) surface, Z(Z-1)/A^(1/3)
  Coulomb, or (N-Z)^2/A asymmetry shapes. The CR reports this honestly.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   alpha_H = 2
M = 126  L = 162  V = 27  Theta = 18
kappa = 7117/768   g = 1/64
mu_Q = 192/7117 u
```

## Locked four-particle basis

Per-particle vectors derived by disaggregating CR247's two-particle basis
to the per-nucleon-plus-electron level:

```text
proton            phi_p = (u=2, d=1, e=0, Q_mass=4*kappa, Q_sub=8*kappa, dQ = -4*kappa)
balanced neutron  phi_n_b = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=0,       dQ =  4*kappa)
excess neutron    phi_n_e = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=1/8,     dQ = 4*kappa - 1/8 = 7093/192)
electron          phi_e   = (u=0, d=0, e=1, Q_mass=0,        Q_sub=0,       dQ = 0)
```

Justification of disaggregation:

- `phi_p + phi_n_b + phi_e = (3, 3, 1, 8*kappa, 8*kappa, 0)` = CR247 phi_balanced.
- `phi_n_e = (1, 2, 0, 4*kappa, 1/8, 7093/192)` = CR247 phi_excess_neutron.

So `Z * (phi_p + phi_n_b + phi_e) + (N-Z) * phi_n_e = Z * phi_balanced + (N-Z) * phi_excess_neutron` reproduces CR247.

## Locked occupancy

```text
For N >= Z (CR248 scope):
  n_proton(Z, N)             = Z
  n_balanced_neutron(Z, N)   = Z
  n_excess_neutron(Z, N)     = N - Z
  n_electron(Z, N)           = Z
```

## Locked Phase A — algebraic identity verification

For every test row (N >= Z), verify all six identities exactly (Fraction):

```text
Sum_j n_j u_j      = 2*Z + N         (source u)
Sum_j n_j d_j      = Z + 2*N         (source d)
Sum_j n_j e_j      = Z               (source e)
Sum_j n_j Q_mass_j = 4*A*kappa       (mass channel)
Sum_j n_j Q_sub_j  = 8*Z*kappa + (N-Z)/8 (substrate channel)
Sum_j n_j dQ_j     = (N-Z) * 7093/192   (channel gap)
```

Match tolerance: 0 (exact Fraction equality).

## Locked Phase B — linear surface-debit B_u closure attempt

Linear model:

```text
B_u_predicted(Z, N) = Z * s_p + Z * s_n_b + (N - Z) * s_n_e + Z * s_e
                    = Z * (s_p + s_n_b + s_e) + (N - Z) * s_n_e
```

Note: s_p, s_n_b, s_e always appear together in this model (Z multiplies
the sum). The fit only identifies (s_p + s_n_b + s_e) jointly and s_n_e
separately. Fit is performed as:

```text
B_u = alpha * Z + beta * (N - Z)
where alpha = s_p + s_n_b + s_e (combined per-electron-paired-position)
      beta  = s_n_e (per excess neutron)
```

OLS on Lane A train (CR239 49 rows minus C-12 anchor minus any A < 16);
then evaluated on full Lane A train and CR241 holdout test.

Anchor case prediction:
- C-12 (Z=6, N=6): B_u_pred = 6*alpha + 0*beta = 6*alpha
- C-13 (Z=6, N=7): B_u_pred = 6*alpha + 1*beta
- Au-197 (Z=79, N=118): B_u_pred = 79*alpha + 39*beta

Report fitted (alpha, beta), train RMS, test RMS, per-anchor predicted vs
observed B_u.

## Wrong controls

```text
WC-1   Disaggregation check: verify (phi_p + phi_n_b + phi_e) equals
       CR247 phi_balanced componentwise. Algebraic check; should pass.
WC-2   Disaggregation check: verify phi_n_e equals CR247 phi_excess_neutron
       componentwise. Algebraic check; should pass.
WC-3   Occupancy perturbation: n_proton = Z + 1. Source identity breaks
       by (+2, +1, 0).
WC-4   Quark assignment swap: swap phi_p quarks (u, d) with phi_n_b
       quarks. New phi_p = (1, 2, 0, ...), new phi_n_b = (2, 1, 0, ...).
       Sum stays (3, 3) so source identity holds, but quark assignment
       loses the "proton vs neutron" distinction. Reported as a
       structural-identification flag, not a falsifier.
WC-5   B_u linear-closure null: predict B_u = 0 for every row, compare RMS
       to fitted linear model. Pass iff fitted model RMS is at least 2x
       better than null (i.e., the linear model has SOME signal).
WC-6   B_u shuffle: shuffle B_u labels across train (seed 20260623), refit
       alpha and beta. Compare to canonical fit. Pass iff shuffled RMS is
       at least 1.5x worse.
```

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Phase A: all six identities exact on every test row (N >= Z)
  S2  Anchors C-12, C-13, Au-197 all six Phase A identities exact
  S3  WC-1, WC-2 algebraic disaggregation checks pass
  S4  WC-3 occupancy perturbation breaks source identity
  S5  WC-5: linear B_u model RMS at least 2x better than null
  S6  WC-6: shuffled fit RMS at least 1.5x worse than canonical
  S7  Linear B_u closure: train RMS <= 0.020 u (~20 MeV; standard BW range)
      AND test RMS <= 0.025 u

BOUNDARY conditions:
  B1  Phase A passes (S1, S2, S3, S4) — algebraic identity holds
  B2  Linear B_u closure does NOT close to STRONG threshold but is non-trivial
  B3  Wrong controls WC-5, WC-6 pass

FAIL conditions:
  F1  Phase A identity fails on any row (other than impossible Fraction rounding)
  F2  Anchor case Q_mass or Q_sub does not match exactly
  F3  Linear B_u model RMS is no better than the null (the per-particle
      basis is not capturing any binding signal at all)
```

Expected outcome: BOUNDARY. Phase A (algebraic) will pass exactly because
the disaggregation is mathematically forced by CR247. Phase B (linear B_u
closure) will likely fail STRONG_PASS thresholds because binding energy is
non-linear in (Z, N). Per-particle constants capture only the linear
component; surface (A^(2/3)), Coulomb (Z(Z-1)/A^(1/3)), asymmetry
((N-Z)^2/A), and pairing terms are missing.

The honest BOUNDARY closes the FOURTH layer (per-particle) of the fatality.pdf
inverse decomposition while leaving the FIFTH (full B_u closure with pair-
write debits) for future work. The relationship to CR245 is explicit: CR245
attempted the BW form directly with typed-coefficient candidates and landed
at BOUNDARY; CR248 confirms that even with per-particle structural
identification at zero free parameters in Phase A, the FIFTH-layer closure
requires the pair-write terms CR245's BW form already imports.

## Outputs (locked file shape)

```text
CR248_summary.json                       — full readout, verdict
CR248_per_row_phase_a.csv                — Phase A per-row identity verification
CR248_anchor_cases.csv                   — C-12, C-13, Au-197 detailed breakdown
CR248_phase_b_linear_fit.csv             — fitted (alpha, beta), train + test residuals
CR248_wrong_controls.csv                 — per-WC results
CR248_input_manifest.csv                 — input SHAs + row counts
HASHES.txt                               — SHA-256 of all CR248 artifacts
```

## Cryptographic chain (inputs)

```text
CR238_result.md  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md  = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md  = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md  = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR243_result.md  = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md  = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_result.md  = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR247_result.md  = ed0eb192ca708e33fb6a044ac5a11e20cfdf1ab507b0bc241110a14646b662d7
CR248_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR248_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1  Phase A: any of the six identities fails on any row.
F2  Phase A: the disaggregated phi_p + phi_n_b + phi_e does not equal
    CR247 phi_balanced componentwise.
F3  Phase A: phi_n_e does not equal CR247 phi_excess_neutron componentwise.
F4  Phase B: the linear B_u model performs no better than the null model
    (B_u = 0 everywhere). Per-particle basis is structureless for binding.
F5  WC-3 (occupancy perturbation) does not break source identity.
F6  WC-6 (label shuffle) does not degrade fit.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, four-particle basis, occupancy
formulas, Phase A identity verifications, Phase B linear-closure model,
wrong controls, verdict gates, falsifiers all locked above the line.
