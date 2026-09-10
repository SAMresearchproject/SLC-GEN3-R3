# QP022A - Private Route-Role Topology Inventory

## Verdict

`QP022A_DERIVED_TOPOLOGY_MATCHES_QP004_EXACTLY`

QP022A starts phase 2 from the hostile-audit launchpad. It asks whether QP004's
route-role topology can be reconstructed from lower artifacts before QP004 role
labels are read.

## Selector Inputs

```text
artifacts/qp001/qp001_qubit_phase_functional_table.csv
artifacts/qp003/qp003_interference_bounce_coupling_table.csv
```

## Comparison Target

```text
artifacts/qp004/qp004_phase_role_operator_rules.csv
```

QP004 is used only after the lower-only topology is derived.

## Main Result

```text
derived_hub_route = QUBIT-CL-001
derived_role_families = 3
exact_qp004_rule_matches = 3/3
selector_used_qp004_labels = False
free_parameters_introduced = 0
```

## Derived Edges

| Derived Family | Route Pair | Endpoint Family | A-share Bounce |
| --- | --- | --- | --- |
| DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-CL-001<->QUBIT-TM-001 | CHARGED_TRIADIC_MINUS_ENDPOINT | True |
| DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-CL-001<->QUBIT-TP-001 | CHARGED_TRIADIC_PLUS_ENDPOINT | True |
| DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-BN-001<->QUBIT-CL-001 | NEUTRAL_BINARY_IDENTITY_ENDPOINT | True |
| DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-CL-001<->QUBIT-NL-001 | NEUTRAL_BINARY_IDENTITY_ENDPOINT | True |
| DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-CL-001<->QUBIT-COLOR-001 | TRANSITION_OWNER_COLOR_ENDPOINT | True |
| DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-CL-001<->QUBIT-UNK-001 | TRANSITION_8_4_ENDPOINT | True |

## QP004 Comparison

| Derived Family | Derived Pairs | Matched QP004 Operator | Exact Match |
| --- | --- | --- | --- |
| DERIVED_DUAL_POLARITY_CHARGED_TOPOLOGY | QUBIT-CL-001<->QUBIT-TM-001;QUBIT-CL-001<->QUBIT-TP-001 | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | True |
| DERIVED_NEUTRAL_BINARY_MIXING_TOPOLOGY | QUBIT-BN-001<->QUBIT-CL-001;QUBIT-CL-001<->QUBIT-NL-001 | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | True |
| DERIVED_TRANSITION_COLOR_COUPLED_TOPOLOGY | QUBIT-CL-001<->QUBIT-COLOR-001;QUBIT-CL-001<->QUBIT-UNK-001 | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | True |

## Meaning

The lower phase route grammar plus A-share bounce topology recovers the same
CL-centered role topology that QP017B used as its audited selector.

This does not yet derive the full downstream particle table. It does move the
QP017B topology input upstream: QP004's required edge topology is recovered as
a lower SAM/QP structure rather than only imported as a bridge table.

## Next Frontier

`QP022B_PRIVATE_CL_HUB_ORIGIN_RULE`

Generated at UTC: `2026-06-07T19:09:12.566625+00:00`
