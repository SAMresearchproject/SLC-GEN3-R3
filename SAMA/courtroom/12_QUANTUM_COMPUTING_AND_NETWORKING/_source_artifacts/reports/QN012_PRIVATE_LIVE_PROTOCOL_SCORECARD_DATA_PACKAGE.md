# QN012 - Private Live Protocol Scorecard and Data Package

## Result

```text
QN012_LIVE_PROTOCOL_SCORECARD_DATA_PACKAGE_BUILT
```

QN012 converts QN011 into a live lab scorecard and blank data package for
testing self-correction by pre-resolution Paul Revere letters.

## Main Readout

```text
data_package_files = 8
trial_role_rows = 6
pre_resolution_log_rows = 8
paul_revere_letter_rows = 6
route_stability_rows = 4
leakage_firewall_rows = 12
scorecard_rows = 14
check_passes = 9/9
wrong_control_passes = 5/5
free_parameters_introduced = 0
```

## Paul Revere Self-Correction Map

| letter_id | warning_letter | allowed_control_action | expected_self_correction_effect | forbidden_payload |
| --- | --- | --- | --- | --- |
| PR-LETTER-01 | polarization drift | update polarization compensation command | preserve carrier link before endpoint resolution | final_ledger_outcome;logical_route_identity |
| PR-LETTER-02 | phase drift | adjust phase stabilization envelope | reduce route instability without selecting final result | selected_final_result;ledger_commit_result |
| PR-LETTER-03 | timing headroom | delay, advance, or hold relay attempt inside open window | keep Paul Revere letter ahead of write closure | force_pre_resolution_route_after_A_SHARE |
| PR-LETTER-04 | failed-link notice | retry source/link preparation while other open links remain guarded | repair route opportunity without copying final outcome | clone_final_outcome;copy_logical_route_identity |
| PR-LETTER-05 | window-open flag | permit active correction only while pre-resolution window is open | stop route forcing when write window closes | premature_selected_write;selected_final_result |
| PR-LETTER-06 | syndrome_signal | apply letter-safe correction command | correct apparatus state from allowed syndrome content | final_ledger_outcome;logical_route_identity |

## Data Package

| package_file | role | required_for_qn012 |
| --- | --- | --- |
| trial_role_map_template.csv | map physical lab apparatus to SAM roles | True |
| pre_resolution_trial_log_template.csv | capture allowed warning letters before final write | True |
| paul_revere_self_correction_map.csv | map warning letters to allowed self-correction actions | True |
| allowed_letter_correction_log_template.csv | record actual corrections driven by warning letters | True |
| route_stability_surface_input_template.csv | build blinded route-stability surface before final labels join | True |
| leakage_firewall_report_template.csv | prove forbidden final content is absent before write | True |
| post_write_join_manifest_template.csv | join final logs only after pre-resolution hash freeze | True |
| sam_qn_live_protocol_scorecard.csv | score PASS/PARTIAL/NOT_READY/SAM_BLOCKER without fitted weights | True |

## Scorecard Surface

| scorecard_id | scorecard_target | target_type | required_evidence_artifact | pass_condition |
| --- | --- | --- | --- | --- |
| QN012-SCORE-01 | QN011-REQ-01 | REQUIREMENT | trial_role_map_template.csv | A candidate trial log can identify each SAM role without using final outcome labels. |
| QN012-SCORE-02 | QN011-REQ-02 | REQUIREMENT | pre_resolution_trial_log_template.csv | Carrier-preservation decisions are explainable from allowed link letters only. |
| QN012-SCORE-03 | QN011-REQ-03 | REQUIREMENT | pre_resolution_trial_log_template.csv | Relay records do not contain endpoint final outcomes or selected route identity before write closure. |
| QN012-SCORE-04 | QN011-REQ-04 | REQUIREMENT | paul_revere_self_correction_map.csv;allowed_letter_correction_log_template.csv | The warning channel changes controls without carrying final result content. |
| QN012-SCORE-05 | QN011-REQ-05 | REQUIREMENT | route_stability_surface_input_template.csv | The route-stability surface is computed from open-window route records only. |
| QN012-SCORE-06 | QN011-REQ-06 | REQUIREMENT | allowed_letter_correction_log_template.csv | Correction commands are reproducible from allowed letters and do not require endpoint final outcomes. |
| QN012-SCORE-07 | QN011-REQ-07 | REQUIREMENT | trial_role_map_template.csv | Every active control requirement has an apparatus-supplied mechanism. |
| QN012-SCORE-08 | QN011-REQ-08 | REQUIREMENT | leakage_firewall_report_template.csv;post_write_join_manifest_template.csv | No pre-resolution control row contains final outcome, logical identity, or selected-write fields. |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN012_CHECK_01 | QN011 protocol translation selected before scorecard package | True | Qunnect_Cisco_metro_photonic_entanglement_swap |
| QN012_CHECK_02 | trial role map covers all six SAM apparatus roles | True | 6 |
| QN012_CHECK_03 | Paul Revere self-correction map has multiple allowed warning letters | True | failed-link notice;phase drift;polarization drift;syndrome_signal;timing headroom;window-open flag |
| QN012_CHECK_04 | pre-resolution log template blocks final outcome and route identity | True | 8 |
| QN012_CHECK_05 | route-stability template stays blinded before final label join | True | 4 |
| QN012_CHECK_06 | leakage firewall makes forbidden fields hard blockers | True | 12 |
| QN012_CHECK_07 | post-write join requires pre-resolution hash freeze | True | 1 |
| QN012_CHECK_08 | scorecard introduces no fitted weights or performance scores | True | 14 |
| QN012_CHECK_09 | data package manifest contains all required template files | True | 8 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN012_WC_01 | Paul Revere letter carries final answer | False | False | True |
| QN012_WC_02 | pre-resolution trial log allows final outcome | False | False | True |
| QN012_WC_03 | leakage firewall treats forbidden content as soft penalty | False | False | True |
| QN012_WC_04 | post-write join does not require pre-resolution hash | False | False | True |
| QN012_WC_05 | live scorecard introduces fitted numeric ranking | False | False | True |

## Interpretation

QN012 is the bite:

```text
the network can self-correct from Paul Revere letters
the letter is allowed to steer apparatus controls
the letter is forbidden from carrying the final answer
the pre-resolution log freezes before the final measurement log joins
```

The package is ready for a lab-facing QN013 live-data ingestion pass.

## Outputs

```text
artifacts/qn012/trial_role_map_template.csv
artifacts/qn012/pre_resolution_trial_log_template.csv
artifacts/qn012/paul_revere_self_correction_map.csv
artifacts/qn012/allowed_letter_correction_log_template.csv
artifacts/qn012/route_stability_surface_input_template.csv
artifacts/qn012/leakage_firewall_report_template.csv
artifacts/qn012/post_write_join_manifest_template.csv
artifacts/qn012/sam_qn_live_protocol_scorecard.csv
artifacts/qn012/sam_qn_live_data_package_manifest.csv
```

## Next Frontier

```text
QN013_PRIVATE_LIVE_DATA_INGESTION_AND_SCORING_PROTOCOL
```
