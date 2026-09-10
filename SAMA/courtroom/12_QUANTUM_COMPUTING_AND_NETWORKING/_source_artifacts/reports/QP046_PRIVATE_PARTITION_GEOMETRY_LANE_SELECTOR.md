# QP046 - Private Partition Geometry Lane Selector

## Preflight

```text
test_id = QP046
test_name = PRIVATE_PARTITION_GEOMETRY_LANE_SELECTOR
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
free_parameters_introduced = 0
```

## Result

```text
QP046_PARTITION_GEOMETRY_LANE_SELECTOR_SELECTED
```

QP045 showed that every uniform divisor partition of `R=12` carries the same
total A-share:

```text
sum(partition)=R
A_total = A_SHARE = 1/12
```

QP046 selects the next rule:

```text
lane = f(group_count, group_size)
total A-share magnitude does not select the lane by itself
```

## Lane Table

| partition | geometry | A total | selected lane | selector | status | particles | unknowns |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| (1,1,1,1,1,1,1,1,1,1,1,1) | 12x1 | 1/12 | MICROCELL_FLOOR_LANE | R_BY_ONE_A_SHARE_MICROCELL_FLOOR_SELECTOR | SELECTED_NATIVE_NONPARTICLE_LANE |  | SAM-UNK-050 |
| (2,2,2,2,2,2) | 6x2 | 1/12 | SIX_HALF_CONTACT_WRITE_ROUTE | HALF_CONTACT_ROUTE_SELECTOR | SELECTED_NATIVE_NONPARTICLE_LANE |  | SAM-UNK-026 |
| (3,3,3,3) | 4x3 | 1/12 | D_PLUS_ONE_PROPAGATION_LANE | D_PLUS_ONE_PART_COUNT_PROPAGATION_SELECTOR | SELECTED_NATIVE_PROPAGATION_LANE |  | SAM-UNK-008 |
| (4,4,4) | 3x4 | 1/12 | TRIADIC_PARTICLE_SCREEN_LANE | D_AXIS_WITH_D_PLUS_ONE_BLOCK_SCREEN_SELECTOR | SELECTED_FILLED_PARTICLE_LANE | u;d;s;c;b;t |  |
| (6,6) | 2x6 | 1/12 | OUTER_BINARY_SCALAR_RETURN_LANE | OUTER_BINARY_RETURN_SELECTOR | SELECTED_FILLED_PARTICLE_LANE | H |  |
| (12,) | 1x12 | 1/12 | SINGLE_BLOCK_INTEGER_WINDING_LANE | FULL_RADIX_INTEGER_WINDING_SELECTOR | SELECTED_FILLED_PARTICLE_LANE | e;mu;tau;nu_e;nu_mu;nu_tau |  |

## Axis Duality

| pair | left lane | right lane | why distinct |
| --- | --- | --- | --- |
| 12x1 <-> 1x12 | MICROCELL_FLOOR_LANE | SINGLE_BLOCK_INTEGER_WINDING_LANE | microcell floor versus full-radix integer winding |
| 6x2 <-> 2x6 | SIX_HALF_CONTACT_WRITE_ROUTE | OUTER_BINARY_SCALAR_RETURN_LANE | half-contact write route versus outer binary scalar return |
| 4x3 <-> 3x4 | D_PLUS_ONE_PROPAGATION_LANE | TRIADIC_PARTICLE_SCREEN_LANE | D+1 propagation part count versus triadic particle screen |

## Key Fields

```text
selected_lane_rows = 6
filled_particle_lane_rows = 3
native_nonparticle_lane_rows = 2
propagation_lane_rows = 1
axis_duality_pairs = 3
free_parameters_introduced = 0
observed_masses_used = false
next_frontier = QP047_PRIVATE_NUCLEAR_BINDING_ISOTOPE_A_ROAD_SELECTOR
```

## Interpretation

This closes the immediate ambiguity opened by QP045. `A_SHARE=1/12` is the
shared amount, but the shape of the share determines the lane. In particular,
`(4,4,4)` and `(3,3,3,3)` are not interchangeable:

```text
(4,4,4)   = 3 x 4 = D axes with D+1 block width -> triadic particle screen
(3,3,3,3) = 4 x 3 = D+1 part count over D blocks -> propagation lane
```

So SAM-UNK-050 is not a hidden particle slot. It is the 12x1 microcell floor
that lets the other one-share geometries be read as different lane families.
