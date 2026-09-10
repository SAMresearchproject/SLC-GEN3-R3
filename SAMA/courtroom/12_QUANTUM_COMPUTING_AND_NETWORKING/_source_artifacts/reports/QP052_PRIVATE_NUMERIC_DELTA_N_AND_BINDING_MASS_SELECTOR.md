# QP052 - Private Numeric DeltaN and Binding Mass Selector

## Preflight

```text
test_id = QP052
test_name = PRIVATE_NUMERIC_DELTA_N_AND_BINDING_MASS_SELECTOR
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
QP052_NUMERIC_DELTA_N_AND_BINDING_MASS_SELECTED
```

QP052 turns the QP051 depth lane into closed neutron packets:

```text
DeltaN = floor(Z * selected_depth_index / R)
R = 12
```

and emits a native isotope mass candidate:

```text
M_candidate = M_seed + DeltaN*M_neutron - DeltaN*M_neutron*(R_bind - 1)
```

The floor operation is the packet-closure rule: fractional exposure remains a
residual lane until a whole neutron packet closes.

## Depth Summary

| selected depth | rows | DeltaN range | mass candidate range MeV |
| ---: | ---: | --- | --- |
| 0 | 12 | 0..0 | 1.875576e+03..2.235463e+04 |
| 1 | 12 | 1..2 | 2.514481e+04..4.655155e+04 |
| 2 | 12 | 4..6 | 5.024327e+04..7.259076e+04 |
| 3 | 12 | 9..12 | 7.717095e+04..1.004723e+05 |
| 4 | 12 | 16..20 | 1.059279e+05..1.301960e+05 |
| 5 | 12 | 25..30 | 1.365140e+05..1.617621e+05 |
| 6 | 12 | 36..42 | 1.689293e+05..1.951705e+05 |
| 7 | 12 | 49..56 | 2.031739e+05..2.304212e+05 |
| 8 | 12 | 64..72 | 2.392477e+05..2.675141e+05 |
| 9 | 10 | 81..88 | 2.771507e+05..3.008813e+05 |

## Lane Summary

| selected lane | rows | DeltaN range | mass candidate range MeV |
| --- | ---: | --- | --- |
| FIRST_NEUTRON_EXCESS_WRITE_LANE | 12 | 1..2 | 2.514481e+04..4.655155e+04 |
| NEUTRON_RESERVOIR_REORGANIZATION_LANE | 24 | 4..12 | 5.024327e+04..1.004723e+05 |
| STACKED_NEUTRON_RESERVOIR_LANE | 70 | 16..88 | 1.059279e+05..3.008813e+05 |
| SYMMETRIC_SEED_DOMINANT_LANE | 12 | 0..0 | 1.875576e+03..2.235463e+04 |

## Key Counts

```text
mass_candidate_rows_emitted = 118
positive_deltaN_rows = 106
zero_deltaN_rows = 12
max_deltaN_closed_packets = 88
observed_isotope_masses_used = false
free_parameters_introduced = 0
next_frontier = QP053_PRIVATE_ISOTOPE_ROSTER_STABILITY_SELECTOR
```

## Interpretation

QP052 fills the first full numeric isotope readout layer: each element row now
has a SAM-native DeltaN packet count, candidate N/A, and mass candidate derived
from the seed surface, neutron support mass, and QP040 binding residue operator.
