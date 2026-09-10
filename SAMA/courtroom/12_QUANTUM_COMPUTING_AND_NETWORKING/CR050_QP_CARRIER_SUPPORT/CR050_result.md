# CR050 QP Carrier Support

## Verdict

```text
CR050_PASS_QP_CARRIER_SUPPORT
```

## Scope Boundary

```text
Support artifact only. This does not prove a quantum computer or network.
```

## Key Rows

See `CR050_rows.csv`.

## Pass Conditions

| condition | pass |
|---|---:|
| QP010_free_parameters_zero | true |
| QP010_qubit_rows_positive | true |
| QP010_result_built | true |
| QP043_free_parameters_zero | true |
| QP043_unknown_modes_present | true |
| QP043_at_least_one_assigned | true |
