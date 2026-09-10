# QP022C - Private Lane Separation Rule

## Verdict

`QP022C_LANE_SEPARATION_RULE_SELECTED`

QP022C derives neutral, charged, and transition lane separation from endpoint
route grammar plus QP022B hub support.

## Selector Inputs

```text
artifacts/qp001/qp001_qubit_phase_functional_table.csv
artifacts/qp022b/qp022b_hub_support_edges.csv
artifacts/qp022b/qp022b_summary.json
```

QP004 is comparison only.

## Main Result

```text
selected_hub_route = QUBIT-CL-001
derived_lanes = 3
lanes_with_two_endpoints = 3/3
exact_qp004_rule_matches = 3/3
selector_used_qp004_labels = False
free_parameters_introduced = 0
```

## Derived Lanes

| Derived Lane | Endpoints | Endpoint Classes | Pairs | Hub Supported |
| --- | --- | --- | --- | --- |
| DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-TM-001;QUBIT-TP-001 | CHARGED_MINUS_TRIADIC_ENDPOINT;CHARGED_PLUS_TRIADIC_ENDPOINT | QUBIT-CL-001<->QUBIT-TM-001;QUBIT-CL-001<->QUBIT-TP-001 | True |
| DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-BN-001;QUBIT-NL-001 | NEUTRAL_IDENTITY_ACTIVE_ENDPOINT;NEUTRAL_SCALAR_RETURN_ENDPOINT | QUBIT-BN-001<->QUBIT-CL-001;QUBIT-CL-001<->QUBIT-NL-001 | True |
| DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-COLOR-001;QUBIT-UNK-001 | TRANSITION_8_4_ENDPOINT;TRANSITION_OWNER_COLOR_ENDPOINT | QUBIT-CL-001<->QUBIT-COLOR-001;QUBIT-CL-001<->QUBIT-UNK-001 | True |

## QP004 Comparison

| Derived Lane | Matched QP004 Operator | Exact Match |
| --- | --- | --- |
| DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | True |
| DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | True |
| DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | True |

## Meaning

The lane split is recovered from endpoint grammar:

```text
neutral    = neutral identity active + scalar/even-return endpoint
charged    = minus triadic + plus triadic endpoint
transition = 8+4 endpoint + owner/color endpoint
```

This makes the QP004 role classes a downstream match to lower route grammar
rather than the selector source.

## Next Frontier

`QP022D_PRIVATE_DERIVED_TOPOLOGY_REPLAY`

Generated at UTC: `2026-06-07T19:38:32.978146+00:00`
