# QP057 - Private Decay Direction Chain Selector

## Preflight

```text
test_id = QP057
test_name = PRIVATE_DECAY_DIRECTION_AND_CHAIN_SELECTOR
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
observed_decay_modes_used = false
observed_half_lives_used = false
observed_isotope_masses_used = false
free_parameters_introduced = 0
```

## Result

```text
QP057_DECAY_DIRECTION_AND_CHAIN_SELECTED
```

QP057 selects native rebalance direction and first chain-step candidates from
QP056 pressure lanes.

## Direction Summary

| direction | rows | A candidate range |
| --- | ---: | --- |
| ALPHA_CHAIN_DOWNSTEP | 13 | 210..236 |
| CEILWARD_NEUTRON_PACKET_COMPLETION | 22 | 40..238 |
| DENSE_CONTEXT_LONG_ANCHOR_HOLD | 5 | 195..233 |
| FLOORWARD_NEUTRON_PACKET_REJECTION | 21 | 27..169 |
| HALF_WRITE_BIDIRECTIONAL_BALANCE | 24 | 37..208 |
| NO_REBALANCE_STABLE_ANCHOR | 27 | 2..205 |
| RETURN_TO_PREFERRED_NEIGHBOR | 43 | 28..237 |
| SYNTHETIC_DOWNCHAIN_CASCADE | 45 | 240..325 |

## Chain Step Summary

| chain step | rows | A candidate range |
| --- | ---: | --- |
| ALPHA_MINUS_2Z_MINUS_4A | 13 | 210..236 |
| HEAVY_DOWNSTEP | 45 | 240..325 |
| MINUS_RESIDUAL | 21 | 27..169 |
| PAIR | 24 | 37..208 |
| PAIR_RETURN | 43 | 28..237 |
| PLUS_ONE_N | 22 | 40..238 |
| SELF | 27 | 2..205 |
| SELF_OR_HALF_WRITE_PAIR | 5 | 195..233 |

## Key Counts

```text
direction_rows_emitted = 200
rebalance_direction_count = 8
chain_step_count = 8
observed_decay_modes_used = false
observed_half_lives_used = false
free_parameters_introduced = 0
next_frontier = QP058_PRIVATE_PHASE5_PRESSURE_FREEZE
```

## Interpretation

QP057 turns pressure into direction. Exact closures hold, half-write lanes
balance, preferred branches point toward floor or ceil packet completion, and
actinide/synthetic high-pressure lanes point into down-chain steps.
