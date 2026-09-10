# CR092a HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE

## Test Class

```text
COURTROOM_INTAKE_OF_QP091T_AND_QP091U
exact closed-loop R^2 retention parent derivation +
freeze-and-wrong-control survival certificate
no external Higgs mass target opened or used as input
```

## Preflight

```text
Upstream quantum_phase has produced two new sealed artifacts that
extend the QP084-QP091 forward-frozen chain previously intaken by
CR065a (HIGGS_ZZ4L_PREDICTION_INTAKE):

  QP091T  exact closed-loop R^2 retention + surface debit derivation
          of the H -> ZZ* -> 4l scalar parent at H_native = 126 GeV,
          H_reveal = 125.25 GeV, with QP091S (2*pi q-split, prior
          near-lock context) demoted from exact parent to context.

  QP091U  hard-freeze of QP091T + seven wrong-control attempts
          (D=2, D=4, R=10, R=24, no surface debit, D/R debit,
          D^2/R^2 debit). All seven rejected. Freeze hashes match
          QP091T HASHES.txt byte-for-byte.

CR092a brings both into the Courtroom 09a branch as a Phase-2/3
extension of the 35-row particle mass chain. It does NOT open a
new external CERN target. The 125.25 GeV reveal value matches the
HZZ4l reference already cited inside the 09_PARTICLE_MASS_CHAIN
CR062 row-by-row ledger; CR092a does not re-open that target.
It does NOT modify CR064a (the branch verdict) or any 09a CR.
```

## Question

Does the upstream QP091T derivation chain (R^2 closed loop, 2^-D
split loss, D^2/R surface debit) produce the H -> ZZ* -> 4l scalar
parent at H_native = 126 GeV exact and H_reveal = 125.25 GeV exact
from R, D, alpha_H alone (zero free parameters, no Higgs target
used as input), and does the QP091U freeze + seven wrong-control
table confirm the derivation is structurally locked?

## Pass Conditions

```text
P1  QP091T summary.json reports passed=true and
    free_parameters_introduced=0
P2  QP091T declared_premises.json reports
    higgs_target_used_as_input=false
P3  R=12, D=3, alpha_H=2 reproduce H_native = R^2 * (1 - 2^-D) = 126
    exactly to 30 decimal places
P4  D^2/R = 9/12 = 0.75 reproduces H_reveal = 126 - 0.75 = 125.25
    exactly
P5  Loss identity holds: R^2 * 2^-D = alpha_H * D^2 = 18 exactly
P6  Shell-share identity holds: 2 * H_native / R = H_native / (alpha_H * D)
    = 21 exactly
P7  HZZ4l category projection 4e:2e2mu:4mu = 1:2:1 reproduces
    (0.25 / 0.50 / 0.25)
P8  QP091U summary.json reports passed=true, freeze_hashes_match=true,
    frozen_files_total=11, sidecars_written=11
P9  QP091U all seven wrong-control variants report rejected=true
    (D=2, D=4, R=10, R=24, no surface debit, D/R debit, D^2/R^2 debit)
P10 QP091U separates parent retention from surface debit: the three
    wrong-debit controls preserve H_native=126 but fail H_reveal=125.25
P11 The recomputed QP091T HASHES.txt SHA256 matches the QP091U-recorded
    frozen hash
P12 QP091S 2*pi q-split context value 126.001639... is recorded as
    context only, not the exact parent
```

## Wrong Controls

```text
WC1 any source artifact missing or hash-mismatched aborts the intake
WC2 any free parameter introduced anywhere in QP091T or QP091U fails P1
WC3 modifying any QP091T or QP091U source artifact during the intake is
    a protocol violation
WC4 the recomputed H_native must equal 126.000000... exactly, not just
    within tolerance; any drift fails P3
WC5 the recomputed H_reveal must equal 125.250000... exactly; any drift
    fails P4
WC6 if ANY of the seven wrong-control variants would have passed
    (smaller residual from 126.001639 or matching observed 125.25
    by accident), QP091U should have flagged it; failure to flag
    fails P9
WC7 opening a new CERN four-lepton measurement inside CR092a is a
    scope violation (that was CR066a's role)
WC8 claiming CR092a supersedes any prior 09a CR is a scope violation;
    this is a Phase-2/3 appended-upgrade intake, not a replacement
```

## K Conditions (Retroactive Grading Standard v1.0)

```text
K1  External anchor       125.25 GeV reveal anchored to CR062 row in
                          09_PARTICLE_MASS_CHAIN ledger and the LHC
                          HZZ4l reference cited there; could have
                          come out otherwise from any wrong R,D,debit
                          combination per QP091U
K2  Falsification line    "this test could have falsified: the closed-
                          loop R^2 retention derivation if the upstream
                          QP091T or QP091U hash chain failed, if any
                          wrong-control variant survived, or if the
                          recomputed H_native/H_reveal differed from
                          the QP091T-claimed exact values"
K3  Target hygiene        QP091T declared_premises explicitly records
                          higgs_target_used_as_input=false; the
                          derivation uses only R, D, alpha_H
K4  Typed inputs          R=12 from R12 duodecimal radix (closed
                          Courtroom tooth); D=3 from displacement-
                          response theorem (G355 priority record);
                          alpha_H=2 from worldsheet wave-operator
                          factorization (priority record 2.3)
K5  Reproduction on demand The Courtroom runner.py re-executes the
                          chain in-repo from R, D, alpha_H and verifies
                          QP091T/U source hashes byte-for-byte
```

## Branch Continuation Rule

```text
09a Phase-2 chain extension (chronological):
  CR065a HIGGS_ZZ4L_PREDICTION_INTAKE              (forward-frozen QP084-QP091)
  CR066a HIGGS_ZZ4L_CERN_REVEAL_MAP                (reveal targets)
  CR067a WZH_BOUNCE_SUBSLOT_INTAKE                 (G435 grid)
  CR068a QUARK_LINEAGE_9_8_RECIPROCAL_CONTROL
  CR069a 09A_PHASE_2_BRANCH_VERDICT_ZIPPER         (Phase-2 verdict)
  CR091a Z_RESIDUAL_CLOSURE_APPEAL                 (Z 12-sigma residual closed at q=-1/6)
  CR092a HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE   (this CR)

CR064a (09a branch verdict) remains immutable. CR069a (Phase-2
zipper) remains immutable. CR092a is a Phase-3-style appended
upgrade that brings the exact closed-loop derivation forward.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
