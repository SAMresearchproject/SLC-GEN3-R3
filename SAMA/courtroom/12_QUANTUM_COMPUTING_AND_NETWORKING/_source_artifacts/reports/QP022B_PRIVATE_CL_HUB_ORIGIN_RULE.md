# QP022B - Private CL Hub Origin Rule

## Verdict

`QP022B_CL_HUB_ORIGIN_RULE_SELECTED`

QP022B asks why `QUBIT-CL-001` is the hub recovered by QP022A.

## Selector Inputs

```text
artifacts/qp001/qp001_qubit_phase_functional_table.csv
artifacts/qp003/qp003_interference_bounce_coupling_table.csv
artifacts/qp022a/qp022a_route_inventory_table.csv
```

No QP004 role labels are used as selector inputs.

## Main Result

```text
selected_hub_route = QUBIT-CL-001
hub_origin_rule_unique = True
selected_hub_endpoint_routes_covered = 6
selected_hub_endpoint_role_families_covered = 3
selector_used_qp004_labels = False
free_parameters_introduced = 0
```

## Hub Candidate Table

| Route | Native Hub Class | A-share Reorg | Endpoint Routes | Role Families | Selected |
| --- | --- | --- | --- | --- | --- |
| QUBIT-BN-001 | False | False | 0 | 0 | False |
| QUBIT-CL-001 | True | True | 6 | 3 | True |
| QUBIT-COLOR-001 | False | False | 0 | 0 | False |
| QUBIT-NL-001 | False | False | 0 | 0 | False |
| QUBIT-TM-001 | False | False | 0 | 0 | False |
| QUBIT-TP-001 | False | False | 0 | 0 | False |
| QUBIT-UNK-001 | False | False | 0 | 0 | False |

## Selected Hub Support

| Hub | Endpoint | Endpoint Family | Role Family | Pair | Bounce |
| --- | --- | --- | --- | --- | --- |
| QUBIT-CL-001 | QUBIT-BN-001 | NEUTRAL_BINARY_IDENTITY_ENDPOINT | DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-BN-001<->QUBIT-CL-001 | True |
| QUBIT-CL-001 | QUBIT-COLOR-001 | TRANSITION_OWNER_COLOR_ENDPOINT | DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-CL-001<->QUBIT-COLOR-001 | True |
| QUBIT-CL-001 | QUBIT-NL-001 | NEUTRAL_BINARY_IDENTITY_ENDPOINT | DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-CL-001<->QUBIT-NL-001 | True |
| QUBIT-CL-001 | QUBIT-TM-001 | CHARGED_TRIADIC_MINUS_ENDPOINT | DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-CL-001<->QUBIT-TM-001 | True |
| QUBIT-CL-001 | QUBIT-TP-001 | CHARGED_TRIADIC_PLUS_ENDPOINT | DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-CL-001<->QUBIT-TP-001 | True |
| QUBIT-CL-001 | QUBIT-UNK-001 | TRANSITION_8_4_ENDPOINT | DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-CL-001<->QUBIT-UNK-001 | True |

## Meaning

`QUBIT-CL-001` is selected because it is the only route that is both:

```text
INTEGER_WINDING_NEG_FULL on the alpha_H^2*D single-block route
and
the A-share reorganization center with bounce contact to every endpoint family.
```

This moves the CL hub from observed graph fact to a lower SAM/QP rule.

## Next Frontier

`QP022C_PRIVATE_LANE_SEPARATION_RULE`

Generated at UTC: `2026-06-07T19:34:27.767465+00:00`
