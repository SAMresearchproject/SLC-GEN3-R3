# QP056 - Private Residual Stability Decay Pressure Selector

## Preflight

```text
test_id = QP056
test_name = PRIVATE_RESIDUAL_STABILITY_DECAY_PRESSURE_SELECTOR
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
observed_isotope_masses_used = false
observed_half_lives_used = false
observed_abundance_used_as_selector = false
free_parameters_introduced = 0
```

## Result

```text
QP056_RESIDUAL_STABILITY_DECAY_PRESSURE_SELECTED
```

QP056 classifies native stability/decay pressure from residual twelfths,
ladder preference, and formation routing.

## Decay Pressure Summary

| pressure lane | rows | A candidate range | preferences |
| --- | ---: | --- | --- |
| ACTINIDE_ALPHA_CHAIN_PRESSURE | 13 | 210..236 | NATIVE_PREFERRED_BRANCH;NATIVE_SECONDARY_BRANCH;NATIVE_STABILITY_ANCHOR |
| DENSE_CONTEXT_LONG_ANCHOR_PRESSURE | 5 | 195..233 | NATIVE_HALF_WRITE_COANCHOR;NATIVE_STABILITY_ANCHOR |
| EXACT_CLOSURE_STABILITY_PRESSURE | 27 | 2..205 | NATIVE_STABILITY_ANCHOR |
| HALF_WRITE_BALANCE_PRESSURE | 24 | 37..208 | NATIVE_HALF_WRITE_COANCHOR |
| OFF_AXIS_HIGH_REBALANCE_PRESSURE | 16 | 27..172 | NATIVE_PREFERRED_BRANCH;NATIVE_SECONDARY_BRANCH |
| QUARTER_BRANCH_REBALANCE_PRESSURE | 20 | 31..167 | NATIVE_PREFERRED_BRANCH;NATIVE_SECONDARY_BRANCH |
| SIXTH_BRANCH_REBALANCE_PRESSURE | 16 | 29..170 | NATIVE_PREFERRED_BRANCH;NATIVE_SECONDARY_BRANCH |
| SYNTHETIC_HIGH_DECAY_PRESSURE | 45 | 240..325 | TRANSIENT_ROUTE_CANDIDATE |
| TRIADIC_BRANCH_DECAY_PRESSURE | 34 | 33..238 | NATIVE_PREFERRED_BRANCH;NATIVE_SECONDARY_BRANCH |

## Native Preference Summary

| native preference | rows | A candidate range |
| --- | ---: | --- |
| NATIVE_HALF_WRITE_COANCHOR | 28 | 37..233 |
| NATIVE_PREFERRED_BRANCH | 49 | 27..238 |
| NATIVE_SECONDARY_BRANCH | 49 | 28..237 |
| NATIVE_STABILITY_ANCHOR | 29 | 2..210 |
| TRANSIENT_ROUTE_CANDIDATE | 45 | 240..325 |

## Key Counts

```text
pressure_rows_emitted = 200
element_primary_rows = 118
decay_pressure_lane_count = 9
native_preference_count = 5
observed_isotope_masses_used = false
observed_half_lives_used = false
free_parameters_introduced = 0
next_frontier = QP057_PRIVATE_DECAY_DIRECTION_AND_CHAIN_SELECTOR
```

## Interpretation

QP056 says the leftover twelfths are not only isotope-neighbor structure. They
also carry native pressure: exact closure, half-write balance, triadic branch,
quarter/sixth rebalance, off-axis rebalance, dense-context anchor, actinide
chain pressure, and synthetic transient pressure.
