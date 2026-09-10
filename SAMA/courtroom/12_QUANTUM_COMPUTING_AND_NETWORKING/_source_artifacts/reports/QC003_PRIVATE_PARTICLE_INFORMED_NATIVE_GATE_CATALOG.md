# QC003 - Particle-Informed Native Gate Catalog

## Result

```text
QC003_PARTICLE_INFORMED_NATIVE_GATE_CATALOG_SELECTED
```

## Main Readout

```text
native_gates = 5
operation_rows = 20
call_surface_rows = 5
check_passes = 8/8
wrong_control_passes = 6/6
free_parameters_introduced = 0
```

## Native Gate Catalog

| native_gate_id | native_gate | allowed_pre_write_letters | carrier_operation | envelope_operation | commit_rule |
| --- | --- | --- | --- | --- | --- |
| QC003-NG-01 | shielded_no_write_wait | window-open flag | preserve unresolved carrier in open no-write window | hold carrier inside open no-write window | NO_COMMIT_PRE_WRITE |
| QC003-NG-02 | letter_preserving_drift_gate | phase drift;polarization drift | keep final route unresolved while drift letter corrects envelope | phase and polarization compensation | NO_COMMIT_PRE_WRITE |
| QC003-NG-03 | basin_bias_steering_gate | syndrome_signal;basin_bias;boundary_stress | steer basin pressure without exposing logical route identity | apply letter-safe correction from sensor stress | NO_COMMIT_PRE_WRITE |
| QC003-NG-04 | controlled_A_contact_gate | window-open flag;phase drift;polarization drift;timing headroom | hold unresolved carrier while charged envelope modulates contact pressure | bounded A-contact steering and timing control | NO_COMMIT_PRE_WRITE |
| QC003-NG-05 | delayed_resolution_read_gate | timing headroom | remain unresolved until selected write | allow final read only after selected write and hash boundary | COMMIT_ALLOWED_ONLY_AFTER_SELECTED_WRITE_AND_HASH_FREEZE |

## Call Surface

| native_gate_id | native_gate | required_input | score_if_complete | score_if_missing_surface | score_if_leakage |
| --- | --- | --- | --- | --- | --- |
| QC003-NG-01 | shielded_no_write_wait | window-open flag | PASS | PARTIAL | SAM_BLOCKER |
| QC003-NG-02 | letter_preserving_drift_gate | phase drift;polarization drift | PASS | PARTIAL | SAM_BLOCKER |
| QC003-NG-03 | basin_bias_steering_gate | syndrome_signal;basin_bias;boundary_stress | PASS | PARTIAL | SAM_BLOCKER |
| QC003-NG-04 | controlled_A_contact_gate | window-open flag;phase drift;polarization drift;timing headroom | PASS | PARTIAL | SAM_BLOCKER |
| QC003-NG-05 | delayed_resolution_read_gate | timing headroom | PASS | PARTIAL | SAM_BLOCKER |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QC003_CHECK_01 | QC002 dependency is selected | True | QC002_CARRIER_ENVELOPE_SEPARATION_LAW_SELECTED |
| QC003_CHECK_02 | five native gates selected | True | 5 |
| QC003_CHECK_03 | every gate preserves carrier pre-write | True | carrier unresolved before write |
| QC003_CHECK_04 | controlled A-contact gate is present | True | controlled_A_contact_gate |
| QC003_CHECK_05 | delayed read requires hash/final boundary | True | delayed_resolution_read_gate |
| QC003_CHECK_06 | operation table has four layers per gate | True | 20 |
| QC003_CHECK_07 | call surface imports QN013 score vocabulary | True | NOT_READY;PARTIAL;PASS;SAM_BLOCKER |
| QC003_CHECK_08 | no gate allows final payload before write | True | 5 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QC003_WC_01 | native gate catalog omits protected carrier | False | False | True |
| QC003_WC_02 | native gate catalog omits charged envelope | False | False | True |
| QC003_WC_03 | native gate catalog omits boundary sensor | False | False | True |
| QC003_WC_04 | a pre-write call surface scores leakage as pass | False | False | True |
| QC003_WC_05 | controlled A-contact gate is missing | False | False | True |
| QC003_WC_06 | unsupported native gate status appears | False | False | True |

## Interpretation

QC003 is the callable gate layer. QC002 separated carrier, envelope, and sensor.
QC003 names the gates that can be invoked without opening the protected carrier
early.

## Next Frontier

```text
QC004_PRIVATE_PAUL_REVERE_READOUT_PROTOCOL
```
