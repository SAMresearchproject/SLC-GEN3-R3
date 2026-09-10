# CR247 SOB Inverse Second-Layer Decomposition — Result

## Verdict

```text
CR247_STRONG_PASS_SOB_INVERSE_SECOND_LAYER__
FOUR_OF_FIVE_FATALITY_CONSTRAINT_GROUPS_EXACT__
Z_BALANCED_PLUS_NminusZ_EXCESS_DECOMP_REPRODUCES_SOB_TARGET__
ZERO_FREE_PARAMETERS__ALL_WC_BREAK_AS_PREDICTED
```

`execution_status   = CLEAN`
`scientific_verdict = STRONG_PASS`
`classification     = SECOND_LAYER_INVERSE_DECOMPOSITION (downstream of CR238/CR239/CR240/CR243/CR244/CR245)`
`precommit_sha      = 4e8a25d205713918470231cfcccb30ad8b1932c49089f09fc10e7d31a6117e2b`

## Plain-English Summary

Per Sean's fatality.pdf working-backwards approach, the second-layer
inverse decomposition

```text
n_balanced(Z, N)        = Z
n_excess_neutron(Z, N)  = N − Z         (for N ≥ Z)
```

with per-position basis vectors

```text
balanced position phi_b  = (u=3, d=3, e=1, Q_mass=8κ, Q_sub=8κ,   dQ=0)
excess neutron  phi_e   = (u=1, d=2, e=0, Q_mass=4κ, Q_sub=1/8,  dQ=4κ − 1/8)
```

**reproduces the sealed SOB target vector**

```text
Phi(Z, N) = (u=2Z+N, d=Z+2N, e=Z,
             Q_mass = 4·A·κ,
             Q_sub  = 8Zκ + (N−Z)/8,
             dQ     = (N−Z)·(4κ − 1/8) = (N−Z)·7093/192)
```

**EXACTLY on every test row, under Fraction arithmetic. Zero free
parameters. 69/69 rows match all six identity components.**

Test corpus: 69 rows with N ≥ Z (49 CR239 Lane A non-anchor + 20 CR241
holdout); two N < Z rows (H-1, He-3) excluded from scope (CR247 covers the
N ≥ Z case; the symmetric N < Z variant is reserved).

All three fatality.pdf anchor cases pass with exact Fraction matches:

| Case  | Z, N  | n_b, n_e | Q_mass | Q_sub | dQ |
|---|---|---|---|---|---|
| C-12  | 6, 6  | 6, 0  | 7117/16 = 444.8125 | 7117/16 = 444.8125 | 0 |
| C-13  | 6, 7  | 6, 1  | 92521/192 = 481.880208 | 7119/16 = 444.9375 | 7093/192 = 36.942708 |
| Au-197| 79, 118 | 79, 39 | 1402049/192 = 7302.338542 | 562711/96 = 5861.572917 | 92209/64 = 1440.765625 |

The **Au-197 dQ value 1440.765625 matches fatality.pdf exactly** —
`39·(4κ − 1/8) = 39·7093/192 = 276627/192 = 1440.765625`.

This closes **four of the five fatality.pdf constraint groups** (source
u/d/e + mass + substrate + channel-gap = 6 component identities verified)
**from CR238 substrate atoms alone, with no free parameter**. The fifth
constraint (surface-debit / B_u closure `Σ n_j·s_debit_j ≈ B_u`) requires
the third-layer micro-channel decomposition (an integer linear program over
the CR243/CR244 substrate ledger) and is reserved for a future CR.

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : 4e8a25d205713918470231cfcccb30ad8b1932c49089f09fc10e7d31a6117e2b
Train SHA-256           : 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
Test SHA-256            : 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8

Substrate atoms (read-only from CR238):
  kappa = 7117/768   g = 1/64    S = 8
Derived:
  8·kappa = 7117/96       (Q_mass and Q_sub contribution per balanced position)
  4·kappa = 7117/192      (Q_mass contribution per excess neutron)
  S·g     = 1/8           (Q_sub contribution per excess neutron)
  4κ − S·g = 7093/192     (dQ contribution per excess neutron)
```

## Block A — Per-Identity Match Counts

| Identity | Rows | Match | Rate |
|---|---:|---:|---:|
| u (source u-quark)    | 69 | **69** | 1.000 |
| d (source d-quark)    | 69 | **69** | 1.000 |
| e (source electron)   | 69 | **69** | 1.000 |
| Q_mass                | 69 | **69** | 1.000 |
| Q_sub                 | 69 | **69** | 1.000 |
| dQ (channel gap)      | 69 | **69** | 1.000 |

**All-six-match count: 69/69.** Every test row passes every identity.

Per-row details in `CR247_per_row_verification.csv` with target and
decomposed values as exact rationals.

## Block B — Anchor Cases (fatality.pdf)

### C-12 (N = Z, balanced channel only, dQ = 0)

```text
Z = 6, N = 6, A = 12       n_balanced = 6, n_excess_neutron = 0

Source:
  u: target 18 = 6·3                 decomp 6·3 + 0·1 = 18    MATCH
  d: target 18 = 6·3                 decomp 6·3 + 0·2 = 18    MATCH
  e: target 6                        decomp 6·1 + 0·0 = 6     MATCH
Mass:
  Q_mass: target 4·12·κ = 48κ = 7117/16    decomp 6·8κ + 0·4κ = 48κ = 7117/16   MATCH
Substrate:
  Q_sub:  target 8·6·κ + 0 = 48κ = 7117/16  decomp 6·8κ + 0·1/8 = 48κ = 7117/16  MATCH
Channel gap:
  dQ:     target 0                   decomp 0                                    MATCH
```

C-12 isolates the balanced channel only — dQ = 0 because no excess
neutrons, and Q_mass = Q_sub because the basis values agree at 8κ.

### C-13 (N − Z = 1, isolates one excess-neutron contribution)

```text
Z = 6, N = 7, A = 13       n_balanced = 6, n_excess_neutron = 1

Source:
  u: target 19 = 2·6 + 7             decomp 6·3 + 1·1 = 19    MATCH
  d: target 20 = 6 + 2·7             decomp 6·3 + 1·2 = 20    MATCH
  e: target 6                        decomp 6·1 + 1·0 = 6     MATCH
Mass:
  Q_mass: target 4·13·κ = 52κ = 92521/192   decomp 6·8κ + 1·4κ = 52κ = 92521/192  MATCH
Substrate:
  Q_sub:  target 8·6·κ + 1·1/8 = 48κ + 1/8 = 7119/16    decomp same   MATCH
Channel gap:
  dQ:     target 1·(4κ − 1/8) = 7093/192 = 36.942708    decomp same   MATCH
```

C-13 isolates a single excess-neutron contribution. The channel-gap
contribution per excess neutron is exactly `7093/192`, the same typed
rational that appears in the CR245 asymmetry-identity constant
`7093²/(192·7117)`.

### Au-197 (N − Z = 39, stress-tests scaling)

```text
Z = 79, N = 118, A = 197    n_balanced = 79, n_excess_neutron = 39

Source:
  u: target 276 = 2·79 + 118         decomp 79·3 + 39·1 = 276  MATCH
  d: target 315 = 79 + 2·118         decomp 79·3 + 39·2 = 315  MATCH
  e: target 79                       decomp 79·1 + 39·0 = 79   MATCH
Mass:
  Q_mass: target 4·197·κ = 788κ = 1402049/192 = 7302.338542
          decomp 79·8κ + 39·4κ = (632+156)κ = 788κ  MATCH
Substrate:
  Q_sub:  target 8·79·κ + 39·1/8 = 632κ + 39/8 = 562711/96 = 5861.572917
          decomp same                                            MATCH
Channel gap:
  dQ:     target 39·(4κ − 1/8) = 39·7093/192 = 276627/192 = 92209/64 = 1440.765625
          decomp same                                            MATCH
```

**The Au-197 dQ value 1440.765625 matches the fatality.pdf computation
exactly.** Verification: `7302.338542 − 5861.572917 = 1440.765625` ✓.

Detailed anchor breakdown in `CR247_anchor_cases.csv`.

## Block C — Wrong Controls

| WC | Description | Rows | Breaks | Pass |
|---|---|---:|---:|:---:|
| WC-1 | Basis swap (n_b ↔ n_e); N=2Z rows are structural invariants (excluded) | 67 (69 − 2 N=2Z) | 67 | ✓ |
| WC-2 | basis κ = 7117/769 (target κ stays 7117/768) | 69 | 69 | ✓ |
| WC-3 | basis g = 1/63 (target g stays 1/64); skips N=Z (zero excess) | 56 | 56 | ✓ |
| WC-4 | n_balanced = Z + 1 (over-counts source) | 69 | 69 | ✓ |
| WC-5 | basis dQ_excess = 7093/193 (target stays 7093/192); skips N=Z | 56 | 56 | ✓ |

**All five wrong controls pass.** Notes:

- **WC-1 structural invariant**: The basis swap is the *identity transformation* for rows with N = 2Z (because then n_b_original = Z = N − Z = n_b_swapped, n_e_original = N − Z = Z = n_e_swapped). This is a mathematical property of the swap, not a verification failure. The N = 2Z rows in our test corpus are recorded in the WC-1 invariant list (e.g., H-3 with Z=1, N=2). The WC-1 pass condition applies to the 67 eligible non-N=2Z rows, all of which break under swap.
- **WC-2, WC-5 perturb basis only**: target stays canonical. These specifically test that the BASIS values (8κ, 4κ, 1/8, 7093/192) are load-bearing — perturbing them in the decomposition breaks the identity against the canonical target.
- **WC-3 skips N=Z**: when N = Z, n_excess = 0 and basis g has no effect; the test is meaningful only for non-symmetric rows.

Per-WC counts in `CR247_wrong_controls.csv`.

## Block D — K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 | PASS | External anchors: CR239/CR241 isotope inputs (SHA-locked). Each row's (Z, N) is an external measurement; the SOB target vector is computed from sealed CR238/CR240 formulas. The identity could have failed if the basis vectors were wrong. |
| K2 | PASS | Falsifiers F1–F5 pre-stated. None fired. Specifically F1 (any identity fails on any row) did not fire — 69/69 match all six. |
| K3 | PASS | Structural identity test, not blind discovery. The basis vectors and occupancy formulas are derived in fatality.pdf and locked in the precommit before the runner ran. Verification is reproduction, not fit. |
| K4 | PASS | Two CR238 atoms `{κ, g}` only. No free parameter entered the runner. SHA-locked inputs and precommit verified at runner entry. |
| K5 | PASS | `python CR247_runner.py` deterministically reproduces every per-row identity, every anchor verification, every wrong control. |

## Block E — Strong-Pass Conditions

| Condition | Status |
|---|:---:|
| S1 Source identity (u, d, e) all 69 match | PASS |
| S2 Q_mass identity all 69 match | PASS |
| S3 Q_sub identity all 69 match | PASS |
| S4 dQ identity all 69 match | PASS |
| S5 Anchor cases (C-12, C-13, Au-197) all six identities exact | PASS |
| S6 All 5 wrong controls break as predicted | PASS |
| S7 Zero free parameters (closed-form algebraic closure) | PASS |

## Block F — What This Closes

**The second layer of the fatality.pdf inverse decomposition is now a sealed
structural identity.** For any (Z, N) with N ≥ Z, the SOB target vector
`Phi(Z, N)` reduces to a sum of integer-occupancy contributions from two
typed basis vectors in CR238 atoms:

```text
Phi(Z, N) = Z · phi_balanced + (N − Z) · phi_excess_neutron
```

This is **theorem-grade**: zero free parameters, exact Fraction arithmetic,
69/69 rows. The two basis vectors `phi_b` and `phi_e` are derived from the
sealed CR238/CR240 closed-form kernels (`Q_mass = 4Aκ`, `Q_sub = S·(Zκ +
(N−Z)·g)`), so this is reproduction-of-existing-structure, not new
empirical content. The value is in the **explicit inverse-decomposition
form**: gold (or any nucleus) is now structurally expressed as
`Z · {balanced position} + (N − Z) · {excess neutron}` with each position
contributing typed-rational amounts to every channel.

## Block G — What Remains Open

The fifth fatality.pdf constraint — `Σ n_j · s_debit_j ≈ B_u` — is the
surface-debit closure that would close the binding-curvature derivation.
It requires the **third-layer micro-channel decomposition**: given a
balanced position and an excess neutron, what specific particle-table rows
of CR243/CR244 (color triads, equal pairs, unequal pairs, OCTET, single
writes, support) do they decompose into, and what are the typed
surface-debit contributions per row?

This is an **integer linear program** over the 139-row CR244 substrate
ledger, with constraints from CR243/CR244 typed channel forms and the
known per-position (Q_mass, Q_sub, dQ) contributions from CR247. The
solution would give:

```text
phi_balanced     = Σ_j n_b_j · (CR243/CR244 row j)
phi_excess_neutron = Σ_j n_e_j · (CR243/CR244 row j)
```

and the surface-debit per position would then close `B_u(Z, N) = Z·s_b +
(N−Z)·s_e` directly. **That is the natural CR248 candidate.**

## Cryptographic Chain (Inputs)

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
CR247_PRECOMMIT.md = 4e8a25d205713918470231cfcccb30ad8b1932c49089f09fc10e7d31a6117e2b
CR247_train_lane_a.csv = 54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc
CR247_test_holdout.csv = 8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8
```

## What CR247 Does

1. Verifies algebraically that `Z · phi_balanced + (N − Z) · phi_excess_neutron` reproduces the sealed SOB target vector `Phi(Z, N)` exactly for every (Z, N) with N ≥ Z, across all 69 test rows.
2. Confirms the three fatality.pdf anchor cases C-12 (balanced only), C-13 (one excess neutron), Au-197 (39 excess neutrons) exactly under Fraction arithmetic.
3. Reproduces the fatality.pdf Au-197 channel-gap value 1440.765625 exactly as `92209/64 = 39 · 7093/192`.
4. Runs five wrong controls: basis swap (excluding N = 2Z structural invariants), basis-only κ perturbation, basis-only g perturbation, occupancy perturbation, basis-only dQ-constant perturbation. All five pass.
5. Reports the second-layer inverse decomposition as a closed-form structural identity in CR238 atoms with zero free parameters.

## What CR247 Does NOT Do

- Does NOT close the fifth fatality.pdf constraint (surface-debit / B_u closure). That requires third-layer micro-channel decomposition over CR243/CR244 ledger rows — reserved for CR248.
- Does NOT modify CR245 BOUNDARY on binding-curvature derivation. CR245 remains operative; CR247 provides the inverse decomposition that CR245's third-layer follow-up would build on.
- Does NOT extend to proton-rich isotopes (N < Z); the symmetric variant with `n_balanced = N` and `n_excess_proton = Z − N` is reserved.
- Does NOT modify any upstream sealed CR. CR114, CR217, CR222, CR229, CR238, CR239, CR240, CR243, CR244 all remain frozen.

## Manuscript Implications

CR247 supplies the explicit inverse-decomposition reading of the SOB target
vector:

```text
For any isotope (Z, N) with N >= Z and substrate atoms {kappa = 7117/768,
g = 1/64, S = 8} from CR238:

Phi(Z, N) = Z·(u=3, d=3, e=1, Q_mass=8*kappa, Q_sub=8*kappa, dQ=0)
          + (N − Z)·(u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=1/8,
                     dQ = 4*kappa − 1/8 = 7093/192)

reproduces every component of the sealed CR238/CR240 SOB target vector
exactly.  Zero free parameters; closed-form algebraic identity.
```

This is the second of three fatality.pdf decomposition layers, sealed.
Combined with CR238 (substrate spine compaction), CR240 (rest-mass channel
Q_mass = 4Aκ), CR238/CR239 (substrate channel Q_sub = S·G_sub), and
CR243/CR244 (typed channel-form table for the substrate ledger), the SOB
object is now structurally explicit at every layer except the surface-debit
closure.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Substrate atoms, basis vectors, occupancy
formulas, target vector, six identity verifications, wrong controls, verdict
gates, falsifiers all frozen.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** 6/6 identities EXACT on 69/69 rows; 3/3 anchor cases ALL EXACT; 5/5 wrong controls pass (WC-1 structural N=2Z invariants noted as mathematical property); Au-197 dQ = 1440.765625 = 92209/64 matches fatality.pdf exactly.
**Verdict driver:** S1–S7 all pass; second-layer inverse decomposition is a sealed structural identity in CR238 atoms with zero free parameters.
**Open follow-up:** CR248 candidate — third-layer micro-channel decomposition (integer linear program over CR243/CR244 substrate ledger) to close the fifth fatality.pdf constraint Σ n_j · s_debit_j ≈ B_u and reach a derived binding-curvature surface.
