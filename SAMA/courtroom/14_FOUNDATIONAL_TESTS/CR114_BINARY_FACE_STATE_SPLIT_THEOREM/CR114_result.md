# CR114 Binary Face-State Split Theorem

## Verdict

```text
CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM
```

## Theorem Statement

For a closed scalar loop with D independent binary closure axes, the loop has 2^D face-states. Exactly one face-state is unresolved tensor-carrier support, so the carrier fraction is 1/2^D and the retained scalar fraction is 1-2^-D. With D=3 and R=12 this gives R^2/2^D=18=alpha_H*D^2 and R^2*(1-2^-D)=126. The carrier is then packetized by alpha_H=2 into plus/cross 1/16+1/16 support; it is not matter and not the D^2/R observed-surface debit.

## Derived Chain

```text
D binary axes                    = 3
closed-loop face-states          = 2^D = 8
unresolved carrier states        = 1
carrier fraction                 = 1/8
retained scalar fraction         = 7/8
R^2                              = 144
split loss                       = R^2/2^D = 18
tensor identity                  = alpha_H*D^2 = 18
retained parent                  = R^2*(1-2^-D) = 126
surface debit                    = D^2/R = 3/4
observed surface                 = 126 - 3/4 = 125.25
plus/cross carrier packet        = 1/16 + 1/16
A=1 boundary support             = 7/8 + 1/16 + 1/16 = 1
```

## Load-Bearing Source Chain

- CR114_RUNNER: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR114_BINARY_FACE_STATE_SPLIT_THEOREM\CR114_runner.py` sha256 `6f3ecd7f02fce652629820817f8299b7de5067e81a89c3585d08b077a5d77796`
- CR113_SUMMARY: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM\CR113_summary.json` sha256 `2c2a1a33c9b29d17b002a25d4cd8432691875098a60cd2fa3f1ff5864ea7664e`
- CR113_LOCK: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM\CR113_completed_write_address_count_lock.json` sha256 `6892987bdd978f03fa42cb7d0ef14e24cdd08e11e154ef8ced5cd5ede3fd15b4`
- QP091T_SUMMARY: `C:\VS\quantum_phase\artifacts\qp091t\qp091t_summary.json` sha256 `8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7`
- QP091T_RESULT: `C:\VS\quantum_phase\artifacts\qp091t\QP091T_result.md` sha256 `f4c4d5aadaddc80e5e20899b62289ed686d0eee668b1ac15f93d69fff06697a5`
- QP091T_PREMISES: `C:\VS\quantum_phase\artifacts\qp091t\qp091t_declared_premises.json` sha256 `476d96c06b64ab352c5142b075558528d5904037420a42650a6c552e9604aad4`
- QP091T_RETENTION_ROWS: `C:\VS\quantum_phase\artifacts\qp091t\qp091t_closed_loop_r2_retention.csv` sha256 `4c3cb310496910d94be3bd25a3ebe3ec667dc8b6698f80ee8171d9096a394c56`
- QP091T_CONTROLS: `C:\VS\quantum_phase\artifacts\qp091t\qp091t_controls.csv` sha256 `103b1ccab0cac2c3c5294a9c71cc5460bca4a623e6db6202b0af8b8ae4d13acc`
- QP091U_SUMMARY: `C:\VS\quantum_phase\artifacts\qp091u\qp091u_summary.json` sha256 `b87d85be2149f4bd51daa70bcfe39f7e14fe033fb6c21d50e441a037f8b27ee1`
- QP091U_WRONG_CONTROLS: `C:\VS\quantum_phase\artifacts\qp091u\qp091u_wrong_controls.csv` sha256 `64154cf5af11e14f6111a40d2ed2527d0c14c36972850765a4402bde80c35f40`
- QP091U_FROZEN_MANIFEST: `C:\VS\quantum_phase\artifacts\qp091u\qp091u_frozen_qp091t_manifest.csv` sha256 `71e528cc81383276d7f459a2b1d77af4126772b882fc124801dff41b63bea0b8`
- QP092A_SUMMARY: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_split_loss_summary.json` sha256 `649e61e0ca47d715e526738bf867f8e57aab1bad6d46974b201fd57c2b4ceaca`
- QP092A_PREMISES: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_split_loss_declared_premises.json` sha256 `e6aaa5c8d11181fec7327eae4c2c660d35ff35ec0b6786095ebd555e6efe6b46`
- QP092A_IDENTITY: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_split_loss_tensor_identity.csv` sha256 `55ffed24918dc7eff7a1d4054a4ea0a08fb7fe450037e3e37c9e3a58e362d96f`
- QP092A_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_controls.csv` sha256 `320df1dba79f92f54a0436ffeec2d5df119822d5d367fb03a10250e466e1a708`
- QP092A_WRONG_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_wrong_split_loss_controls.csv` sha256 `d34139a7edcfc243178b729a7c41ca4607632439ef5cd7583f26e06e391a57a0`
- QP092A_CLASSIFICATION: `C:\VS\quantum_phase\artifacts\qp092a_split_loss_tensor_carrier\qp092a_graviton_channel_classification.csv` sha256 `36662611762cbe0dd3e31d8b9d29dde67f4ebe0188e6742221593746a78543f7`
- QP092F_SUMMARY: `C:\VS\quantum_phase\artifacts\qp092f_tensor_carrier_wave_mode\qp092f_summary.json` sha256 `b122cec6fd334a73a59b280bbf137b3a76a7b588e30e609b81dfeb92f5369536`
- QP092F_PREMISES: `C:\VS\quantum_phase\artifacts\qp092f_tensor_carrier_wave_mode\qp092f_declared_premises.json` sha256 `8c323e767b94e6c2d03841bf2b9d2d00902ae1a1f7d47663b8b68e7cdc7b7586`
- QP092F_TENSOR_BASIS: `C:\VS\quantum_phase\artifacts\qp092f_tensor_carrier_wave_mode\qp092f_tensor_basis.csv` sha256 `1abeed6db780f1770bafbb5c722923d2a5480885c58a2ee708cf3e08058d5492`
- QP092F_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092f_tensor_carrier_wave_mode\qp092f_controls.csv` sha256 `3677b34aa9cdd30aaa2c7b69aa10b354242e99eec390ed2f225e7f66a7b5fc92`
- QP092F_WRONG_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092f_tensor_carrier_wave_mode\qp092f_wrong_controls.csv` sha256 `f648c56fa750ec239fbea6e31ff1b939d4ccef85eb837706d025e1d687466a27`
- QP092G_SUMMARY: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_summary.json` sha256 `b5ee2482db3c4fda01e26359feb3a65089c136a3e038947730f11d9e51b79841`
- QP092G_PREMISES: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_declared_premises.json` sha256 `444e8161cbe38852fda51a2b056c06e79f278f7f73c20716ebf553f5bcdec5ec`
- QP092G_STRONG_BOUNDARY: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_strong_boundary_rows.csv` sha256 `86d87194d7db86c80994b7cde8ee601e3a57b2979c4796e6fa0adea4723c6629`
- QP092G_BRIDGE_PACKET: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_bridge_packet.csv` sha256 `bad793840ec4b68518fc134b2b9191e6b6e5010dd5fbaee3fc8ec08659d11516`
- QP092G_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_controls.csv` sha256 `8efa3c666fd5be03436591b672be863209f60c56caaf61c6934e9e376e06770b`
- QP092G_WRONG_CONTROLS: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_wrong_controls.csv` sha256 `b422bf52db9904aaf0811f947437fa09525f3d7de2f284b0506455d2fe3826e7`
- QP092G_FROZEN_SPINE: `C:\VS\quantum_phase\artifacts\qp092g_tensor_carrier_bridge_packet\qp092g_frozen_spine.csv` sha256 `5146f9f91c5a40fb6f33bfe8f81ee9a1f8210178ff5d94f1b22354d82360c8a2`

## Pass Checks

- PASS P1_sources_present: All load-bearing provenance artifacts are present.
- PASS P2_R12_source_locked: CR113 supplies R=12 from completed-WRITE address count, not 2pi/A0.
- PASS P3_binary_face_state_count: D independent binary closure axes give 2^D = 8 face-states.
- PASS P4_one_unresolved_state_forces_one_eighth: Exactly one unresolved carrier face-state gives carrier fraction 1/2^D = 1/8.
- PASS P5_retained_states_force_seven_eighths: The retained scalar parent has 2^D-1 = 7 states and retained fraction 7/8.
- PASS P6_closed_loop_higgs_parent_matches_QP091T: R^2*(1-2^-D) gives H_native=126 and matches frozen QP091T.
- PASS P7_split_loss_equals_tensor_identity: R^2/2^D gives 18 and equals alpha_H*D^2, matching QP092A.
- PASS P8_surface_debit_is_separate: The 1/8 carrier is not the D^2/R observed-surface debit.
- PASS P9_target_free_and_frozen: The Higgs target is not used as an input and QP091T hashes are frozen by QP091U.
- PASS P10_plus_cross_packet_closes_carrier: The one-eighth carrier splits into plus/cross tensor support, 1/16 + 1/16.
- PASS P11_A1_boundary_packet_closes: 7/8 retained plus 1/16 plus plus 1/16 cross closes A=1.
- PASS P12_carrier_is_not_matter: The 18 split-loss carrier is unresolved tensor support, not a matter row or rest mass.
- PASS P13_no_2pi_exact_parent_route: Old 2pi/q_split route remains near-lock context, not the exact parent derivation.
- PASS P14_bridge_spine_reuses_same_route: QP092G reuses the same frozen 1/8 tensor-carrier route through split-loss, weak-field, strong-boundary, and quantum layers.
- PASS P15_priority_record_tracks_nonmatter_status: Priority record already flags alpha_H*D^2=18 as split-loss/tensor-carrier support, not matter.

## Wrong Controls

- REJECTED WC1_one_quarter_loss: Use 2^(D-1)=4 face-states, giving 1/4 carrier loss.
- REJECTED WC2_one_sixteenth_total_loss: Use 2^(D+1)=16 face-states, giving 1/16 total carrier loss.
- REJECTED WC3_no_carrier: Drop the unresolved carrier state and keep the whole closed loop.
- REJECTED WC4_surface_debit_as_carrier: Replace the 1/8 carrier fraction with the D^2/R observed-surface debit.
- REJECTED WC5_raw_D2_loss: Use raw D^2=9 as the split loss.
- REJECTED WC6_raw_R_loss: Use raw R=12 as the split loss.
- REJECTED WC7_scalar_single_mode: Replace plus/cross tensor support with a single scalar mode.
- REJECTED WC8_vector_three_component_mode: Replace rank-2 tensor support with a vector three-component carrier.
- REJECTED WC9_promote_18_to_matter: Read split_loss=18 as a stable particle row, graviton rest mass, or normal matter inventory.
- REJECTED WC10_restore_2pi_qsplit_exact_route: Use the old 2pi q_split near-lock as the exact Higgs parent derivation.

## Scope

- Closes the missing 1/8 theorem layer used by QP091T/QP092A-G at structural theorem-gate grade.
- Uses R=12 from CR113; does not re-derive R in this test.
- Uses the inherited D=3 and alpha_H=2 primitives already present in the QP chain; does not re-derive them from scratch.
- Separates split-loss carrier 18 from observed surface debit D^2/R=0.75.
- Classifies 18 as unresolved tensor-carrier/source support, not matter, not graviton rest mass, and not a stable particle row.
- Keeps old 2pi/q_split route as historical near-lock context only.

## Open Debts

- Manuscript/audit prose should cite CR114 before QP092A when explaining why the carrier fraction is 1/8.
- External empirical claims remain downstream; CR114 is a framework theorem/closure gate, not a collider-data fit.

## Hash

```text
CR114_binary_face_state_split_lock.json sha256 = 4139aee463004ac2cb882e2bda0642752e0bb5dc759eace42df0351fc51686ec
```
