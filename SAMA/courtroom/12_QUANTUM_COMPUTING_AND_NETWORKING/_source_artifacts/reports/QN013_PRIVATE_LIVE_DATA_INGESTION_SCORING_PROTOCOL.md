# QN013 - Private Live Data Ingestion and Scoring Protocol

## Result

```text
QN013_LIVE_DATA_INGESTION_SCORING_PROTOCOL_BUILT
```

QN013 builds the scorer for QN012-style lab data.

## Main Readout

```text
demo_trials = 3
pass_trials = 1
partial_trials = 1
blocker_trials = 1
validation_rule_rows = 6
score_rule_rows = 4
check_passes = 8/8
wrong_control_passes = 5/5
free_parameters_introduced = 0
```

## Demo Scorecard

| trial_id | trial_class | expected_status | scored_status | score_reason |
| --- | --- | --- | --- | --- |
| DEMO-PASS-001 | CLEAN_SELF_CORRECTION | PASS | PASS | self-correction by allowed Paul Revere letters with clean leakage boundary |
| DEMO-PARTIAL-001 | PARTIAL_ROUTE_SURFACE | PARTIAL | PARTIAL | one required live package field is missing |
| DEMO-BLOCK-001 | FORBIDDEN_EARLY_FINAL_ANSWER | SAM_BLOCKER | SAM_BLOCKER | forbidden final content appeared before selected write |

## Validation Rules

| rule_id | rule | failure_status | hard_blocker |
| --- | --- | --- | --- |
| QN013-VAL-01 | required package file is present | NOT_READY | False |
| QN013-VAL-02 | pre-resolution rows contain trial_id, timestamp, allowed letter value, control command, and hash input | NOT_READY | False |
| QN013-VAL-03 | pre-resolution rows do not contain final_ledger_outcome, logical_route_identity, or selected_final_result | SAM_BLOCKER | True |
| QN013-VAL-04 | Paul Revere warning letter maps to an allowed control action | PARTIAL | False |
| QN013-VAL-05 | route-stability rows are computed before final-label join | PARTIAL | False |
| QN013-VAL-06 | post-write join occurs only after pre-resolution hash freeze | SAM_BLOCKER | True |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN013_CHECK_01 | QN012 live data package exists before scorer | True | Qunnect_Cisco_metro_photonic_entanglement_swap |
| QN013_CHECK_02 | ingestion schema covers every QN012 package file | True | 8 |
| QN013_CHECK_03 | demo scorer produces PASS/PARTIAL/SAM_BLOCKER coverage | True | PARTIAL;PASS;SAM_BLOCKER |
| QN013_CHECK_04 | demo scored statuses match expected fixture statuses | True | PARTIAL;PASS;SAM_BLOCKER |
| QN013_CHECK_05 | self-correction pass trial has no final leakage and has correction | True | DEMO-PASS-001 |
| QN013_CHECK_06 | forbidden early final answer becomes SAM_BLOCKER | True | forbidden final content appeared before selected write |
| QN013_CHECK_07 | pre-resolution rows carry hashes before final join | True | 3 |
| QN013_CHECK_08 | route and correction demo tables cover all trials | True | 3 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN013_WC_01 | leakage trial is scored as non-blocker | False | False | True |
| QN013_WC_02 | clean self-correction trial does not pass | False | False | True |
| QN013_WC_03 | partial route-surface trial is scored as full pass | False | False | True |
| QN013_WC_04 | pre-resolution hash is missing | False | False | True |
| QN013_WC_05 | unsupported score status appears | False | False | True |

## Interpretation

QN013 makes the Paul Revere idea executable:

```text
PASS means a warning letter changed apparatus controls without carrying the answer
PARTIAL means the trial is clean but one live evidence surface is incomplete
SAM_BLOCKER means the final answer leaked into the pre-write channel
```

## Outputs

```text
artifacts/qn013/sam_qn_ingestion_schema.csv
artifacts/qn013/sam_qn_live_data_validation_rules.csv
artifacts/qn013/sam_qn_trial_score_rules.csv
artifacts/qn013/sam_qn_ingestion_demo_scorecard.csv
artifacts/qn013/sam_qn_trial_score_output_template.csv
```

## Next Frontier

```text
QN014_PRIVATE_LAB_HANDOFF_PACKET_AND_EXTERNAL_TRIAL_READINESS
```
