# QP045 - Private A-share Microcell Coarse-Grain Selector

## Preflight

```text
test_id = QP045
test_name = PRIVATE_A_SHARE_MICROCELL_COARSE_GRAIN_SELECTOR
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
QP045_A_SHARE_MICROCELL_COARSE_GRAIN_LAW_SELECTED
```

QP045 selects the pixel-scale coarse-grain law:

```text
A_cell = A_SHARE / R = 1 / R^2 = 1/144
A(N microcells) = N / R^2
```

So `SAM-UNK-050 = (1,1,1,1,1,1,1,1,1,1,1,1)` is one A-share written
pixel by pixel.

## Coarse-Grain Selector

| selector | law | A cell | cells to A-share | status |
| --- | --- | ---: | ---: | --- |
| A_SHARE_MICROCELL_COARSE_GRAIN_SELECTOR | A(N_microcells)=N_microcells/R^2 | 1/144 | 12 | SELECTED_NATIVE_COARSE_GRAIN_LAW |
| PARTITION_GEOMETRY_LANE_SELECTOR | sum(partition)=R => total A=A_SHARE; partition shape selects lane | 1/144 | 12 | SELECTED_NATIVE_GEOMETRY_SELECTOR |

## Threshold Ladder

| microcells | A | threshold | A-share units | meaning |
| ---: | ---: | --- | ---: | --- |
| 1 | 1/144 | MICROCELL_UNIT | 0.0833333333333333 | one unresolved unit cell |
| 6 | 1/24 | A_SIDE_WRITE_ONSET | 0.5 | half-share boundary; write candidacy begins |
| 12 | 1/12 | A_SHARE_WRITE_ACCESS | 1 | one full share; meaningful write structure |
| 48 | 1/3 | QG_BOUNDARY_START | 4 | QP001 qg boundary start = 1/3 |
| 72 | 1/2 | WRITE_MIDPOINT | 6 | classical ledger midpoint |
| 144 | 1 | A_FULL_CLOSURE | 12 | full closure of 12 A-share packets |

## Uniform Partition Map

| partition | grouping | role | matched particles | matched unknown |
| --- | --- | --- | --- | --- |
| (1,1,1,1,1,1,1,1,1,1,1,1) | 12 x 1 | raw_microcell_lattice |  | SAM-UNK-050 |
| (2,2,2,2,2,2) | 6 x 2 | six_half_contact_route |  | SAM-UNK-026 |
| (3,3,3,3) | 4 x 3 | D_plus_one_propagation_candidate |  | SAM-UNK-008 |
| (4,4,4) | 3 x 4 | triadic_particle_screen | u;d;s;c;b;t |  |
| (6,6) | 2 x 6 | outer_binary_scalar_return | H |  |
| (12,) | 1 x 12 | single_block_integer_winding | e;mu;tau;nu_e;nu_mu;nu_tau |  |

## Key Fields

```text
A_cell = 1/144 = 0.00694444444444444
A_SIDE_microcells = 6
A_SHARE_microcells = 12
WRITE_MIDPOINT_microcells = 72
A_FULL_microcells = 144
uniform_share_partitions_mapped = 6
next_frontier = QP046_PRIVATE_PARTITION_GEOMETRY_LANE_SELECTOR
```

## Interpretation

This is the first clean pixel-scale law in the private Phase 4 branch. It says
the total A-share is fixed by the count, while the partition geometry decides
what kind of lane the share becomes. That is why `(12,)`, `(6,6)`, `(4,4,4)`,
`(3,3,3,3)`, `(2,2,2,2,2,2)`, and the 12x1 microcell row can all be native
without being the same physical carrier.
