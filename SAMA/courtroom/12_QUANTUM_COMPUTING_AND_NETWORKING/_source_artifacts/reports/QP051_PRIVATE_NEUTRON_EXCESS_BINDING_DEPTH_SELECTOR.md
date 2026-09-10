# QP051 - Private Neutron Excess Binding Depth Selector

## Preflight

```text
test_id = QP051
test_name = PRIVATE_NEUTRON_EXCESS_BINDING_DEPTH_SELECTOR
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
observed_isotope_masses_used = false
free_parameters_introduced = 0
```

## Result

```text
QP051_NEUTRON_EXCESS_BINDING_DEPTH_LANES_SELECTED
```

QP051 selects a native lane for neutron-excess and binding-depth ownership for
all 118 element seed rows.

The selector uses two existing SAM-native handles:

```text
A-road band depth from QP047
R=12 radix stack depth from QP049
```

and attaches the QP040 nuclear residue operator:

```text
alpha stack rows -> alpha terminal operator
odd residual rows -> deuteron terminal operator
```

## Band Summary

| A band | rows | selected depth range | lanes present |
| --- | ---: | --- | --- |
| A_LOCAL_NOT_PRESENT | 91 | 0..9 | FIRST_NEUTRON_EXCESS_WRITE_LANE;NEUTRON_RESERVOIR_REORGANIZATION_LANE;STACKED_NEUTRON_RESERVOIR_LANE;SYMMETRIC_SEED_DOMINANT_LANE |
| A_SHARE_TO_QG_REORGANIZATION | 5 | 3..6 | NEUTRON_RESERVOIR_REORGANIZATION_LANE;STACKED_NEUTRON_RESERVOIR_LANE |
| A_SIDE_TO_A_SHARE_FUSION_ACCESS | 6 | 1..2 | FIRST_NEUTRON_EXCESS_WRITE_LANE;NEUTRON_RESERVOIR_REORGANIZATION_LANE |
| BELOW_A_SIDE_COHERENT_FORMATION | 12 | 0..4 | NEUTRON_RESERVOIR_REORGANIZATION_LANE;STACKED_NEUTRON_RESERVOIR_LANE;SYMMETRIC_SEED_DOMINANT_LANE |
| QG_TO_WRITE_MIDPOINT_DENSE_CONTEXT | 4 | 6..7 | STACKED_NEUTRON_RESERVOIR_LANE |

## Operator Summary

| operator source | rows | selected depth range | lanes present |
| --- | ---: | --- | --- |
| ALPHA_STACK_TERMINAL_OPERATOR | 59 | 0..9 | FIRST_NEUTRON_EXCESS_WRITE_LANE;NEUTRON_RESERVOIR_REORGANIZATION_LANE;STACKED_NEUTRON_RESERVOIR_LANE;SYMMETRIC_SEED_DOMINANT_LANE |
| DEUTERON_RESIDUAL_TERMINAL_OPERATOR | 59 | 0..9 | FIRST_NEUTRON_EXCESS_WRITE_LANE;NEUTRON_RESERVOIR_REORGANIZATION_LANE;STACKED_NEUTRON_RESERVOIR_LANE;SYMMETRIC_SEED_DOMINANT_LANE |

## Key Counts

```text
lane_rows_emitted = 118
selected_lane_count = 4
rows_with_positive_depth = 106
rows_seed_depth_zero = 12
observed_isotope_masses_used = false
free_parameters_introduced = 0
next_frontier = QP052_PRIVATE_NUMERIC_DELTA_N_AND_BINDING_MASS_SELECTOR
```

## Interpretation

QP051 fills the ownership layer between symmetric isotope seed mass and final
isotope mass. The table now says which native lane carries neutron-excess and
binding-depth pressure for each element row. The next gate can turn this lane
depth into a numeric DeltaN and mass correction.
