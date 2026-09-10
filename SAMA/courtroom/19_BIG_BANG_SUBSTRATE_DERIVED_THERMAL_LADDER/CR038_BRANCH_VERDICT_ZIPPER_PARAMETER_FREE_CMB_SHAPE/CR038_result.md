# CR038 -- Branch 19 Verdict Zipper -- Parameter-Free CMB Shape -- RESULT

```text
verdict           : PASS
classification    : BRANCH_VERDICT_ZIPPER_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : 13789eabc06abba59d5fc2668b4f04a97080e808a6415b1f8717f48bbb420e89
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

Six sealed PASS CRs constitute the parameter-free CMB shape chain in
branch 19, with chain-level invariants (substrate atoms, H_0 propagation,
perturbation triplet propagation, external-instrument independence) all
satisfied. The chain reproduces Planck PR3 full per-multipole TT
bandpowers at TT chi^2/dof = 1.0339 (CR037B) and ACT DR4
cleaned-CMB bandpowers at full chi^2/dof = 1.1218 and TT
chi^2/dof = 1.2996 (CR037C) with zero free parameters in
each CR.

CR037B is the live citation target for "SAM reproduces Planck CMB shape
parameter-free."
CR037C is the live citation target for "SAM cosmology is not a Planck
artifact -- it matches an independent ground-based instrument with the
same atoms."
CR038 is the chain closure record.

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| G1 | each-CR predicate (PASS, fp=0, no prior CR inputs, CLEAN, no forbidden opens) for CR035A2, CR036, CR036B, CR037A, CR037B, CR037C | PASS |
| G2 | chain substrate invariant (Omega_m, Omega_b, Omega_c) | PASS |
| G3 | chain H_0 invariant (67.2503751950 across CR036/CR036B/CR037B/CR037C) | PASS |
| G4 | chain perturbation invariant (CR037A triplet propagated to CR037B and CR037C) | PASS |
| G5 | CR037B Planck TT chi^2/dof <= 2.0 | PASS |
| G6 | CR037C ACT TT and full chi^2/dof <= 2.0 | PASS |
| G7 | CR037C external-instrument independence (ACT data only; no Planck files) | PASS |
| G8 | precommit hash verified | PASS |
| G9 | forbidden-file open() guard not tripped | PASS |

## The chain

| CR | Status | Live numbers |
| --- | --- | --- |
| CR035A | preserved FAIL audit trail | original peak-finder spec falsified; superseded by CR035A2 |
| CR035A2 | PASS | SAM density spine + Planck-centroid perturbations reproduce Planck PR3 TT shape at peak-finder audit-corrected tolerances |
| CR036 | PASS | eta_SAM = 6.096e-10 (-0.06% from BBN consensus); H_0_SAM = 67.2504 km/s/Mpc (-0.16% from Planck reference) |
| CR036B | PASS | SAM densities + H_0_SAM + Planck-centroid perturbations -> Planck PR3 TT chi^2/dof = 1.04 |
| CR037A | PASS | SAM perturbation triplet A_s = eta_SAM*sqrt(R); n_s = 1 - chi/2; tau = 2*A_0; all inside Planck posterior at STRONG_CONTACT |
| CR037B | PASS | full SAM cosmology -> Planck PR3 full per-multipole TT chi^2/dof = 1.03393370270937 |
| CR037C | PASS | full SAM cosmology -> ACT DR4 cleaned-CMB bandpowers TT chi^2/dof = 1.2996, full chi^2/dof = 1.1218; yp2 fixed = 1.0; ACT only (no Planck file at runtime) |

## Chain identities (machine-precision)

```text
Substrate spine (CR018b / CR036 / inherited by CR036B, CR037B, CR037C):
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0      = 1/(12*pi)
  chi      = (S/D) * A_0 = 2/(9*pi)
  Omega_m  = R*A_0       = 1/pi      ~= 0.31831
  Omega_b  = 2*A_0*(1-chi)            ~= 0.04930
  Omega_c  = Omega_m - Omega_b        ~= 0.26901

Dimensional bridge (CR036; FIRAS T_CMB + CODATA 2018 / SI fixed):
  eta_SAM   = 6.0960895e-10
  H_0_SAM   = 67.2503751950 km/s/Mpc

Perturbation triplet (CR037A; CR037B and CR037C consume by value):
  A_s_SAM   = eta_SAM * sqrt(R)  = 2.1117473568e-9
  n_s_SAM   = 1 - chi/2           = 0.9646322349
  tau_SAM   = 2 * A_0             = 0.0530516477
```

## Open items (verbatim from CR038 precommit)

```text
O1. Branch 19 also carries CR001/CR001b sealed FAIL and CR001c sealed
    PASS for substrate-DERIVED recombination physics. The derived
    recombination gives 100*theta_* off Planck by +1.71%, ell_A by
    -1.68%, r_d by -1.55%. The CR037 chain uses CAMB's standard
    recombination (RECFAST default), not SAM-derived. The structural
    tension between "SAM-derived recombination at ~1.5-1.7% from
    Planck" and "SAM-cosmology + CAMB-recombination at sub-percent
    from Planck and ACT" is named, not closed, by CR038.

O2. ACT DR4 cleaned-CMB bandpowers are experiment-marginalized
    (SZ + radio + dust + tSZxCIB removed by ACT pipeline). SAM does
    not derive the foreground spectra independently.

O3. yp2 (polarization-efficiency calibration) is fixed at 1.0 in
    CR037C. CR037D placeholder covers the yp2-marginalized version.

O4. Forward CMB experiments (SPT-3G high-ell, Simons Observatory,
    CMB-S4) covered by CR037E/F placeholders when releases are
    available.

O5. CR035A is preserved bit-for-bit at sealed FAIL as the audit-trail
    record of the original peak-finder spec corrected in CR035A2.
```

## What this CR seals

The parameter-free CMB shape arc of branch 19 is closed at chain level.

Citation surface:
  - CR037B: live "SAM matches Planck PR3" citation
  - CR037C: live "SAM cosmology generalizes off Planck (ACT DR4)" citation
  - CR038:  chain closure record + open-items honest ledger

## Verdict statement

CR038 PASS (branch zipper). The six PASS CRs CR035A2, CR036, CR036B,
CR037A, CR037B, CR037C constitute a zero-free-parameter CMB shape
closure in branch 19, satisfying all chain-level invariants
(substrate, H_0, perturbations) and both external-data shape bounds
(Planck PR3 PASS at TT chi^2/dof = 1.03393370270937; ACT DR4 PASS at
TT chi^2/dof = 1.2996 and full chi^2/dof = 1.1218).
Open items O1-O5 itemized verbatim above.

`CR038_PASS_BRANCH_19_PARAMETER_FREE_CMB_SHAPE_CHAIN_CLOSED_AT_PLANCK_PR3_AND_ACT_DR4_BOTH_AT_CHI2_DOF_LT_2_ZERO_FREE_PARAMETERS_FIVE_OPEN_ITEMS_ITEMIZED`
