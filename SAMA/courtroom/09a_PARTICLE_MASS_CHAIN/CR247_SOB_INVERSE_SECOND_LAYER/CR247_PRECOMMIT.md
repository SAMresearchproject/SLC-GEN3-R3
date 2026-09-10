# CR247 SOB Inverse Second-Layer Decomposition — Precommit

## Question

Per Sean's fatality.pdf working-backwards approach: does the second-layer
nucleus decomposition

```text
n_balanced(Z, N)        = Z
n_excess_neutron(Z, N)  = N - Z       (for N >= Z)
```

with the per-position basis vectors

```text
balanced position phi_b  = (u=3, d=3, e=1, Q_mass=8*kappa, Q_sub=8*kappa, dQ=0)
excess neutron  phi_e   = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=8*g=1/8,  dQ=4*kappa - 1/8)
```

reproduce the sealed SOB target vector

```text
Phi(Z, N) = (u=2Z+N, d=Z+2N, e=Z, Q_mass=4*A*kappa,
             Q_sub = S*(Z*kappa + (N-Z)*g), dQ = (N-Z)*(4*kappa - S*g))
```

EXACTLY for every test row, under Fraction arithmetic?

This is the second of three layers in the fatality.pdf "inverse ledger
decomposition" path. The first layer (n_p = Z, n_n = N, n_e = Z) is
trivially the source inventory. The third layer (per-particle-table-row
micro-channel decomposition n_j) requires integer linear programming and is
reserved for a later CR. CR247 verifies that the second layer closes
**every constraint except the surface-debit / B_u closure** exactly.

## Honest framing

The second-layer basis was specified in fatality.pdf as an inverse
decomposition. CR247 verifies it as a structural identity. The verification
is algebraic — under exact Fraction arithmetic, each of the six target
components (u, d, e, Q_mass, Q_sub, dQ) should match by construction. The
test is reproduction, not fit.

K3 status: PASS. The basis vectors and occupancy formulas are locked above
the line; the runner reads sealed CR239 and CR241 isotope data only to
enumerate (Z, N) test cases.

## Locked substrate atoms (read-only from CR238)

```text
R = 12   D = 3   S = 8   alpha_H = 2
M = 126  L = 162  V = 27  Theta = 18
kappa = 7117/768   g = 1/64
S*g = 8/64 = 1/8
4*kappa - S*g = 7117/192 - 24/192 = 7093/192
```

## Locked basis vectors

```text
balanced position phi_b:
  u_b      = 3       (= 2 + 1 for proton uud + 1 + 2 for neutron udd ... per nucleon
                       contribution: proton + neutron = 3u + 3d, divide by 1 balanced
                       position carrying both -> 3 each.  Plus electron e=1 per Z.)
  d_b      = 3
  e_b      = 1
  Q_mass_b = 8*kappa  = 7117/96
  Q_sub_b  = 8*kappa  = 7117/96
  dQ_b     = 0

excess neutron position phi_e:
  u_e      = 1       (excess neutron udd -> 1 u + 2 d, no electron)
  d_e      = 2
  e_e      = 0
  Q_mass_e = 4*kappa  = 7117/192
  Q_sub_e  = 8*g      = 1/8
  dQ_e     = 4*kappa - 1/8 = 7093/192
```

## Locked occupancy formulas

```text
For N >= Z (standard case for stable isotopes):
  n_balanced(Z, N)        = Z
  n_excess_neutron(Z, N)  = N - Z

For N < Z (proton-rich; not present in CR245 train + holdout):
  n_balanced(Z, N)        = N
  n_excess_proton(Z, N)   = Z - N
  (Symmetric variant not exercised in this CR; reserved.)
```

## Locked target vector

```text
Phi(Z, N) = (u, d, e, Q_mass, Q_sub, dQ)
where:
  u      = 2*Z + N        (total u-quark count)
  d      = Z + 2*N        (total d-quark count)
  e      = Z              (total electron count, neutral atom)
  Q_mass = 4*A*kappa = 4*(Z+N)*kappa
  Q_sub  = S*(Z*kappa + (N-Z)*g) = 8*Z*kappa + (N-Z)*S*g = 8*Z*kappa + (N-Z)/8
  dQ     = Q_mass - Q_sub = (N-Z) * (4*kappa - S*g) = (N-Z) * 7093/192
```

## Locked verification: each component

```text
For every (Z, N) test case, verify all six identities exactly (Fraction):

  Sigma_n_j u_j      = n_b * u_b + n_e * u_e      = 3Z + (N-Z) = 2Z+N        == target u
  Sigma_n_j d_j      = n_b * d_b + n_e * d_e      = 3Z + 2(N-Z) = Z+2N       == target d
  Sigma_n_j e_j      = n_b * e_b + n_e * e_e      = Z                          == target e
  Sigma_n_j Q_mass_j = n_b * 8*kappa + n_e * 4*kappa = (2Z + N-Z + Z)*4*kappa
                                                     = 4(Z+N)*kappa = 4*A*kappa == target Q_mass
                       (Wait: n_b * 8*kappa + n_e * 4*kappa
                            = Z*8*kappa + (N-Z)*4*kappa
                            = (2Z + (N-Z))*4*kappa
                            = (Z + N)*4*kappa = 4*A*kappa)
  Sigma_n_j Q_sub_j  = n_b * 8*kappa + n_e * 1/8 = 8*Z*kappa + (N-Z)/8       == target Q_sub
  Sigma_n_j dQ_j     = n_b * 0 + n_e * 7093/192 = (N-Z) * 7093/192            == target dQ

All six identities should match EXACTLY under Fraction arithmetic.
```

## Test set

```text
Anchor cases (fatality.pdf specifically requested):
  C-12  : Z=6,  N=6   (N=Z, isolates balanced channel only, dQ=0)
  C-13  : Z=6,  N=7   (N-Z=1, isolates one excess neutron contribution)
  Au-197: Z=79, N=118 (N-Z=39, stress-tests scaling)

Full corpus:
  CR239 Lane A (51 rows)
  CR241 holdout (20 rows)
  Total: 71 isotopes (all N >= Z; symmetric N < Z variant reserved)
```

## Wrong controls

```text
WC-1 (basis perturbation): swap phi_b and phi_e occupancies (use n_b = N-Z,
     n_e = Z). Should break all six constraints on rows where N != Z.
WC-2 (kappa perturbation): replace kappa with 7117/769 (off by 1 in
     denominator). Should break Q_mass identity.
WC-3 (g perturbation): replace g with 1/63 (off by 1 in denominator). Should
     break Q_sub identity.
WC-4 (occupancy perturbation): n_b = Z + 1. Should break source identity by
     exactly (+3, +3, +1).
WC-5 (dQ-constant perturbation): replace 7093/192 with 7093/193 in basis.
     Should break dQ identity.
```

Pass condition per WC: the perturbation breaks at least one constraint per
non-trivial row. (N=Z rows trivially satisfy excess-neutron-related
perturbations.)

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Source identity (u, d, e): 71/71 exact
  S2  Q_mass identity:           71/71 exact
  S3  Q_sub identity:            71/71 exact
  S4  dQ identity:               71/71 exact
  S5  Anchor cases (C-12, C-13, Au-197) all six constraints exact
  S6  All wrong controls break at least one constraint on non-trivial rows
  S7  Inverse-decomposition closes the second layer with zero free parameters

BOUNDARY conditions:
  B1  Most constraints close but at least one fails
  B2  Identity holds for N=Z but not N!=Z (or vice versa)

FAIL conditions:
  F1  Any of the six identities fails on any row (other than rounding artifact
      that should not occur in Fraction arithmetic)
  F2  Wrong control fails to break a constraint it was designed to break
```

Expected outcome (based on the algebraic derivation): STRONG_PASS. Each
identity reduces by Fraction arithmetic to the target formula.

## What CR247 DOES NOT close

The fifth fatality.pdf constraint — surface-debit / B_u closure
`Sigma_n_j s_debit_j ~ B_u` — requires the **third-layer** micro-channel
decomposition (which particle-table rows of CR243/244 sum to give s_debit per
balanced and per excess neutron). That decomposition is an integer linear
program over the 139-row substrate ledger and is reserved for a future CR
(CR248 candidate).

CR247 closes layers one and two: source inventory + balanced/excess split,
with 4 of the 5 fatality.pdf constraint groups (source × 3, Q_mass, Q_sub,
dQ — 6 component identities total) verified exact.

## Outputs (locked file shape)

```text
CR247_summary.json                   — full readout, verdict, per-row identity check
CR247_per_row_verification.csv       — per-isotope per-identity match status
CR247_anchor_cases.csv               — C-12, C-13, Au-197 detailed component breakdown
CR247_wrong_controls.csv             — per-WC break counts
CR247_input_manifest.csv             — input SHAs + row counts
HASHES.txt                           — SHA-256 of all CR247 artifacts
```

## Cryptographic chain (inputs)

```text
CR114_result.md (capacity R^2 + split-loss)             = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R^2 * 9/8 closed ledger)         = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md (carrier ledger)                        = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)          = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md (substrate spine compaction)            = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR239_result.md (native mass / gravity FAIL)            = 55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b
CR240_result.md (rest-mass channel STRONG_PASS)         = c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b
CR241_result.md (holdout)                               = d0c8a5688137ebdee9019563965601ca91edc74a26df69d776a10ebd6f3462d8
CR242_result.md (binding BOUNDARY at fitted-typed)      = 091397fec625d216e437a76a50670250bc47a3a97a7d10f38efab53096f18e4d
CR243_result.md (typed channel table)                   = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_result.md (unequal-pair typed forms)              = 813a37689c647bbe70184ebba16b835c0e911902ea006f3d0f06126f778afd0c
CR245_result.md (binding-curvature BOUNDARY; asymmetry identity exact) = 8531cda8ef72ab10c7bddfb7f612a168e79ade64e9e04059e67f363b8ee401fd
CR247_train_lane_a.csv                                  = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR247_test_holdout.csv                                  = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## Falsifiers

```text
F1   Any of the six identities (u, d, e, Q_mass, Q_sub, dQ) fails on any
     row: the second-layer basis vectors are wrong.
F2   N=Z anchor (C-12) fails dQ=0: balanced positions are not pure-balanced.
F3   Au-197 fails any identity: scaling breaks beyond medium-mass nuclei.
F4   WC-1 (basis swap) preserves all constraints: the basis is degenerate.
F5   WC-2 (kappa perturbation) preserves Q_mass: kappa is not actually
     load-bearing in the Q_mass formula.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, basis vectors, occupancy formulas,
target vector, six identity verifications, wrong controls, verdict gates,
falsifiers all locked above the line.
