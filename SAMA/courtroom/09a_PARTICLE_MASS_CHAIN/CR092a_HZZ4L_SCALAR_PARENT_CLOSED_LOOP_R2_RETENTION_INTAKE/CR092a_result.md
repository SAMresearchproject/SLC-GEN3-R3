# CR092a HZZ4L Scalar Parent Closed-Loop R^2 Retention Intake - Result

## Verdict

```text
CR092a_PASS_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE__H_NATIVE_126_EXACT__H_REVEAL_125_25_EXACT__QP091T_QP091U_FREEZE_HELD_7_OF_7_WRONG_CONTROLS_REJECTED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## Exact Chain (Recomputed In Repo)

```text
R                       = 12
D                       = 3
alpha_H                 = 2

closed loop total = R^2 = 144 = 100_12
split loss        = 2^-D = 1/8 = 0.16_12
retained fraction = 7/8        = 0.A6_12

split loss amount = R^2 * 2^-D = 18 = 16_12
alpha_H * D^2     = 18 (loss identity)

H_native          = R^2 * (1 - 2^-D) = 126 GeV = A6_12
surface debit     = D^2 / R = 3/4 = 0.9_12
H_reveal          = H_native - D^2/R = 501/4 GeV = A5.3_12

2 H / R           = 21 = 19_12
H / (alpha_H D)   = 21 = 19_12 (shell-share identity)
```

## HZZ4l Category Projection

```text
4e     = 1/4
2e2mu  = 1/2
4mu    = 1/4
```

## QP091S Context (Demoted)

```text
q_split H context = 126.001639700297361188599351135096 GeV
gap to 126        = 0.001639700297361188599351135096 GeV
```

2*pi q-split is recorded as near-lock context only. The exact derivation is closed-loop retention plus surface debit.

## Source Artifact Hashes

```text
qp091t_summary.json               sha256 = 8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7
qp091t HASHES.txt                 sha256 = ef67f4d99ed9b0001d54472c688d3dec0371cd1f4650fa4567d7958ffce25182
qp091t_declared_premises.json     sha256 = 476d96c06b64ab352c5142b075558528d5904037420a42650a6c552e9604aad4
qp091u_summary.json               sha256 = b87d85be2149f4bd51daa70bcfe39f7e14fe033fb6c21d50e441a037f8b27ee1
qp091u HASHES.txt                 sha256 = 9ddefb3dc837f80a4c58e7956788b9ff846a1dfb42ddc1d04c43a0c08a05427b
qp091u_qp091t_freeze_certificate  sha256 = a7ee03d2cefd19eabfcef0713622888ebf9bb3796aac5c26890d69d0a0c371a3
qp091u_wrong_controls.csv         sha256 = 64154cf5af11e14f6111a40d2ed2527d0c14c36972850765a4402bde80c35f40
intake_lock_sha256                       = f809027dd1217c7efd1606ff5ac4e6b3034fe9f8850a75b88649031517e83bb8
```

## Predictions

- **[PASS]** P1_qp091t_passed_zero_free_parameters
- **[PASS]** P2_qp091t_no_higgs_target_used_as_input
- **[PASS]** P3_R2_times_one_minus_2pow_minusD_equals_126_exact
- **[PASS]** P4_H_reveal_equals_125_25_exact
- **[PASS]** P5_loss_identity_R2_2negD_equals_alphaH_D2_equals_18
- **[PASS]** P6_shell_share_2H_over_R_equals_H_over_alphaH_D_equals_21
- **[PASS]** P7_hzz4l_category_1_2_1_reproduces
- **[PASS]** P8_qp091u_freeze_matched_and_complete
- **[PASS]** P9_all_seven_wrong_control_variants_rejected
- **[PASS]** P10_wrong_debit_variants_preserve_parent_but_fail_reveal
- **[PASS]** P11_qp091t_HASHES_sha_matches_qp091u_recorded_and_all_frozen_rows_match
- **[PASS]** P12_qp091s_qsplit_recorded_as_context_only_not_exact_parent

## Wrong Controls

- **[PASS]** WC1_no_source_artifact_missing_or_hash_mismatched
- **[PASS]** WC2_no_free_parameter_introduced_anywhere
- **[PASS]** WC4_H_native_exact_not_within_tolerance
- **[PASS]** WC5_H_reveal_exact_not_within_tolerance

## Seven Wrong-Control Variants From QP091U

| variant | H_native | H_reveal | rejected |
|---|---|---|---|
| WRONG_D_2 | 108.000000000000000000000000000000 | 107.666666666666666666666666666667 | True |
| WRONG_D_4 | 135.000000000000000000000000000000 | 133.666666666666666666666666666667 | True |
| WRONG_R_10 | 87.500000000000000000000000000000 | 86.600000000000000000000000000000 | True |
| WRONG_R_24 | 504.000000000000000000000000000000 | 503.625000000000000000000000000000 | True |
| NO_SURFACE_DEBIT | 126.000000000000000000000000000000 | 126.000000000000000000000000000000 | True |
| WRONG_DEBIT_D_OVER_R | 126.000000000000000000000000000000 | 125.750000000000000000000000000000 | True |
| WRONG_DEBIT_D2_OVER_R2 | 126.000000000000000000000000000000 | 125.937500000000000000000000000000 | True |

## What This Intake Does NOT Do

- modify any prior 09a CR verdict
- modify CR064a branch verdict
- modify CR069a Phase-2 verdict zipper
- modify CR091a Z residual closure appeal
- open a new external CERN HZZ4l measurement
- introduce a free parameter
- claim QP091S 2*pi q-split is exact

## Rule-9 Line

```text
This intake could have failed if QP091T's exact derivation drifted
from R^2 * (1 - 2^-D) = 126 or D^2/R = 0.75, if any of the seven
QP091U wrong-control variants had survived, if the QP091T or QP091U
source hashes had failed to match, or if a free parameter had been
introduced anywhere. None of those occurred.
```
