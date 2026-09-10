# QN005 - Private Network Born Surface

## Result

```text
QN005_NETWORK_BORN_SURFACE_SELECTED
```

QN005 carries the QP014 Born-style route surface through the QN002-QN004
network chain.

## Main Readout

```text
network_route_rows = 49
multi_node_rows = 84
open_surface_samples = 5
closed_surface_samples = 2
network_available_routes = QUBIT-CL-001;QUBIT-NL-001;QUBIT-UNK-001
top_open_route = QUBIT-NL-001
top_open_probability = 0.9654196547077734
check_passes = 6/6
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Formula

| term | formula | source |
| --- | --- | --- |
| open_window_gate | 1 if QP014 and QN004 both keep the pre-resolution window open else 0 | QP014 + QN004 |
| route_born_probability | QP014 latent_probability | QP014 |
| controlled_route_probability | QP014 controlled_probability | QP014 |
| segment_survival | QN002 segment_survival_score | QN002 |
| relay_viability | QN003 relay_viability_score | QN003 |
| timing_headroom | QN004 timing_headroom | QN004 |
| network_route_weight | open_window_gate * route_born_probability * segment_survival * relay_viability * timing_headroom | QP014 + QN002 + QN003 + QN004 |
| network_controlled_weight | open_window_gate * controlled_route_probability * segment_survival * relay_viability * timing_headroom | QP014 + QN002 + QN003 + QN004 |
| network_probability | network_route_weight / sum(network_route_weight over network-available unresolved routes) | QN005 |

## Sample Surface Summary

| sample_id | surface_state | open_network_routes | network_probability_sum | top_network_route | top_network_probability |
| --- | --- | --- | --- | --- | --- |
| ONE_T_SW | NETWORK_BORN_SURFACE_OPEN | 3 | 1.0 | QUBIT-NL-001 | 0.9654196547077734 |
| QUARTER_A_SIDE | NETWORK_BORN_SURFACE_OPEN | 3 | 1.0 | QUBIT-NL-001 | 0.9654178422029319 |
| HALF_A_SIDE | NETWORK_BORN_SURFACE_OPEN | 3 | 1.0 | QUBIT-NL-001 | 0.9654178422029319 |
| A_SIDE_BOUNDARY | NETWORK_BORN_SURFACE_OPEN | 3 | 1.0 | QUBIT-NL-001 | 0.9654178422029319 |
| MID_A_SIDE_TO_A_SHARE | NETWORK_BORN_SURFACE_OPEN | 3 | 1.0 | QUBIT-NL-001 | 0.9654178422029319 |
| A_SHARE_BOUNDARY | NETWORK_BORN_SURFACE_CLOSED | 0 | 0.0 |  | 0.0 |
| WRITE_MIDPOINT | NETWORK_BORN_SURFACE_CLOSED | 0 | 0.0 |  | 0.0 |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN005_CHECK_01 | open pre-resolution samples normalize to one | True | ONE_T_SW:1.0;QUARTER_A_SIDE:1.0;HALF_A_SIDE:1.0;A_SIDE_BOUNDARY:1.0;MID_A_SIDE_TO_A_SHARE:1.0 |
| QN005_CHECK_02 | closed samples carry zero network probability | True | A_SHARE_BOUNDARY:0.0;WRITE_MIDPOINT:0.0 |
| QN005_CHECK_03 | multi-node stage surfaces normalize or close cleanly | True | 0 |
| QN005_CHECK_04 | protected neutral carrier remains top open route | True | QUBIT-NL-001 |
| QN005_CHECK_05 | surface uses only QN002 network object routes | True | QUBIT-CL-001;QUBIT-NL-001;QUBIT-UNK-001 |
| QN005_CHECK_06 | forbidden final ledger fields are not used | True | False |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN005_WC_01 | closed A_SHARE/WRITE windows receive network probability | False | False | True |
| QN005_WC_02 | support-only non-network routes enter the network denominator | False | False | True |
| QN005_WC_03 | charged envelope becomes top network Born carrier | False | False | True |
| QN005_WC_04 | boundary sensor becomes top network Born carrier | False | False | True |
| QN005_WC_05 | network probability uses final ledger fields | False | False | True |

## Interpretation

QN005 gives the network a SAM-native Born surface:

```text
start with QP014 latent unresolved route probability
restrict to QN002 network object routes
carry those routes through segment survival, relay viability, and QN004 timing headroom
normalize only over routes still open before A_SHARE
close the surface when the pre-resolution window closes
carry the QP014 controlled/write surface as a secondary diagnostic
```

The result is a route-probability surface for network motion before ledger
resolution.

## Outputs

```text
artifacts/qn005/qn005_preflight.md
artifacts/qn005/qn005_input_manifest.csv
artifacts/qn005/network_route_weight_surface.csv
artifacts/qn005/multi_node_probability_surface.csv
artifacts/qn005/network_born_sample_summary.csv
artifacts/qn005/network_born_formula.csv
artifacts/qn005/qn005_checks.csv
artifacts/qn005/qn005_wrong_controls.csv
artifacts/qn005/qn005_summary.json
artifacts/qn005/qn005_next_frontier.csv
```

## Next Frontier

```text
QN006_PRIVATE_ERROR_CORRECTION_AS_LETTER_MANAGEMENT
```
