# QP054 - Private Isotope Neighbor Ladder Selector

## Preflight

```text
test_id = QP054
test_name = PRIVATE_ISOTOPE_NEIGHBOR_LADDER_SELECTOR
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
QP054_ISOTOPE_NEIGHBOR_LADDER_SELECTED
```

QP054 generates a native isotope neighbor ladder from the QP053 residual:

```text
floor row weight = (12 - residual_twelfths) / 12
ceil row weight  = residual_twelfths / 12
```

Exact residual rows keep one floor candidate. Nonzero residual rows add one
ceil-neighbor candidate with one bound-neutron increment.

## Role Summary

| ladder role | rows | A candidate range | preferences |
| --- | ---: | --- | --- |
| CEIL_NEIGHBOR | 82 | 28..325 | BALANCED_HALF_WRITE;CEIL_PREFERRED;UPPER_BRANCH |
| FLOOR_PRIMARY | 118 | 2..324 | BALANCED_HALF_WRITE;LOWER_BRANCH;PRIMARY_EXACT;PRIMARY_PREFERRED |

## Roster Summary

| roster lane | rows | A candidate range | preferences |
| --- | ---: | --- | --- |
| ACTINIDE_TERMINUS_ROSTER_LANE | 13 | 210..236 | CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_EXACT;PRIMARY_PREFERRED;UPPER_BRANCH |
| DENSE_CONTEXT_ANCHOR_ROSTER_LANE | 5 | 195..233 | BALANCED_HALF_WRITE;PRIMARY_EXACT |
| EXACT_CLOSURE_ANCHOR_ROSTER_LANE | 27 | 2..205 | PRIMARY_EXACT |
| HALF_WRITE_ANCHOR_ROSTER_LANE | 24 | 37..208 | BALANCED_HALF_WRITE |
| OFF_AXIS_BRANCH_ROSTER_LANE | 16 | 27..172 | CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_PREFERRED;UPPER_BRANCH |
| QUARTER_BRANCH_ROSTER_LANE | 20 | 31..167 | CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_PREFERRED;UPPER_BRANCH |
| SIXTH_BRANCH_ROSTER_LANE | 16 | 29..170 | CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_PREFERRED;UPPER_BRANCH |
| SYNTHETIC_TRANSIENT_ROSTER_LANE | 45 | 240..325 | BALANCED_HALF_WRITE;CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_EXACT;PRIMARY_PREFERRED;UPPER_BRANCH |
| TRIADIC_BRANCH_ROSTER_LANE | 34 | 33..238 | CEIL_PREFERRED;LOWER_BRANCH;PRIMARY_PREFERRED;UPPER_BRANCH |

## Key Counts

```text
ladder_rows_emitted = 200
floor_primary_rows = 118
ceil_neighbor_rows = 82
balanced_half_write_pairs = 34
observed_isotope_masses_used = false
free_parameters_introduced = 0
next_frontier = QP055_PRIVATE_PHASE5_ISOTOPE_FREEZE
```

## Interpretation

QP054 turns the single QP052 isotope surface into a native isotope ladder. The
residual twelfths now decide whether the floor candidate stands alone, the
floor candidate dominates, the upper neighbor dominates, or both share the
half-write balance.
