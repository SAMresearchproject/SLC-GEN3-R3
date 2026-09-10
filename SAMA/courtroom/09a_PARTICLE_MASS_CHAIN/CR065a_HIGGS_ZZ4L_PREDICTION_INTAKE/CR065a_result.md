# CR065a Higgs ZZ4L Prediction Intake - Result

## Verdict

```text
CR065a_HIGGS_ZZ4L_PREDICTION_INTAKE_PASS
```

## Extends 09a Branch

CR065a continues 09a after the immutable CR064a branch verdict, intaking the upstream QP084 -> QP091 chain that derives a Higgs H -> ZZ* -> 4l prediction freeze from the QP075 35-row closure surface with zero new free parameters.

## Intake Lock

```text
intake_lock_sha256 = 11e898ca84273071096436bd52c3667dd9ec3df2a3c6b599f5a94453827582a7
intaken_at_utc     = 2026-06-14T02:13:09Z
```

## Upstream Chain (each row sha256 + verdict)

| QP | verdict | sha256 (first 16) | free params | external data |
|---|---|---|---|---|
| QP084 | PASS_QP084_RESOLVED_HALF_ROUTE_BOUNCE_GE | 90e89d809e2224fc | 0 | None |
| QP085 | PASS_QP085_HALF_BOUNCE_HIGGS_LANE_CONTAC | 9af24a5defb25581 | 0 | CR092_anchors_reveal |
| QP086 | PASS_QP086_A_DEPENDENT_HIGGS_BOUNCE_COMP | 284d64736c69418a | 0 | None |
| QP087 | PASS_QP087_WZH_RESIDUALS_ON_NATIVE_BOUNC | 5300f929afca1273 | 0 | None |
| QP088 | PASS_QP088_WZH_Q_SLOT_OWNERS_DERIVED_HIG | adc66ed1c8e64a96 | 0 | None |
| QP089 | PASS_QP089_HIGGS_A_SOURCE_TO_MACRO_ACCUM | 8ab67e691b557234 | 0 | None |
| QP090 | PASS_QP090_HIGGS_ZZ4L_VISIBLE_DAUGHTER_L | 750884277e8302cf | 0 | False |
| QP091 | PASS_QP091_HIGGS_ZZ4L_OBSERVABLE_PREDICT | aa5db648aaf644cd | 0 | False |

## QP091 Frozen Predictions

```text
H_visible_parent_ledger        = 125219.0000 MeV
H_source_hidden_budget          = 125419.116945 MeV
Z_visible_branch                = 91161.5000 MeV
two_on_shell_Z_deficit_visible  = 57104.0000 MeV  (forbidden)
Zstar_ceiling_visible           = 34057.5000 MeV
4e   threshold                  = 2.043792 MeV
2e2mu threshold                  = 212.393896 MeV
4mu  threshold                  = 422.744000 MeV
hidden_source_budget_fraction   = 0.001595586  (~0.16%)
```

## Reveal Map Status (set by QP091)

| reveal_id | future_target | qp091_status | selection_role |
|---|---|---|---|
| QP092_REVEAL_01 | H006/H007 signal strength | HELD_NOT_OPENED | post-freeze reveal only |
| QP092_REVEAL_02 | m4l distribution / Higgs mass reconstruction | HELD_NOT_OPENED | test visible parent closure |
| QP092_REVEAL_03 | m12/m34 or Z/Z* branch distributions | HELD_NOT_OPENED | test native off-shell ceiling |
| QP092_REVEAL_04 | four-lepton angular correlations | HELD_NOT_OPENED | test structured hidden-bounce/orientation handle |

## Predictions

- **[PASS]** P1_all_qp_passed
- **[PASS]** P2_all_zero_free_parameters
- **[PASS]** P3_target_blind_no_external_decay_data_in_chain
- **[PASS]** P4_qp091_frozen_observables_match_expected
- **[PASS]** P5_reveal_map_names_four_targets_three_strongest_held_for_CR066a
- **[PASS]** P6_no_cern_decay_data_opened_in_CR065a

## Wrong Controls

- **[PASS]** WC1_any_qp_failed_aborts_intake
- **[PASS]** WC2_any_free_parameter_violates_chain
- **[PASS]** WC3_no_premature_decay_data_opening
- **[PASS]** WC4_qp091_frozen_predictions_not_modified_in_intake
- **[PASS]** WC5_reveal_targets_held_at_intake_time

## Next In 09a

**CR066a** opens REVEAL_02 (m4l distribution), REVEAL_03 (m12/m34 or Z/Z* branch), REVEAL_04 (four-lepton angular correlations) against published ATLAS+CMS Run-2 H -> ZZ* -> 4l measurements.

REVEAL_01 (H006/H007 signal strength) remains HELD. Per the user direction, signal strength is the weakest of the four candidate reveal targets; the structural distributions (m4l, m12/m34, angular) carry far more information about whether the upstream prediction freeze closes.
