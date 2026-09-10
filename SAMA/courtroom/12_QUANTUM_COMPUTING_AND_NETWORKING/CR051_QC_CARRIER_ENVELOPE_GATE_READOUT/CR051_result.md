# CR051 QC Carrier / Envelope / Gate / Readout

## Verdict

```text
CR051_PASS_QC_CARRIER_ENVELOPE_GATE_READOUT
```

## Scope Boundary

```text
Protocol construction only. This does not prove hardware implementation.
```

## Key Rows

See `CR051_rows.csv`.

## Pass Conditions

| condition | pass |
|---|---:|
| QC001_free_parameters_zero | true |
| QC001_no_external_hardware | true |
| QC002_checks_pass | true |
| QC002_wrong_controls_pass | true |
| QC003_native_gates_positive | true |
| QC003_checks_pass | true |
| QC004_paul_revere_selected | true |
| QC004_checks_pass | true |
| all_free_parameters_zero | true |
