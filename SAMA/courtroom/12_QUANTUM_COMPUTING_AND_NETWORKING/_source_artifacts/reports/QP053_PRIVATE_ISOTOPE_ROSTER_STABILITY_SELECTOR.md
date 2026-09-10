# QP053 - Private Isotope Roster Stability Selector

## Preflight

```text
test_id = QP053
test_name = PRIVATE_ISOTOPE_ROSTER_STABILITY_SELECTOR
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
QP053_ISOTOPE_ROSTER_STABILITY_LANES_SELECTED
```

QP053 converts the QP052 fractional packet residual into R=12 roster lanes:

```text
residual_twelfths = round(deltaN_fractional_residual * 12)
```

The split uses exact closure, half-write, triadic, quarter, sixth, and off-axis
residual classes, with formation-lane routing for synthetic and actinide
terminus rows.

## Residual Summary

| residual twelfths | rows | A candidate range | anchor statuses |
| ---: | ---: | --- | --- |
| 0 | 36 | 2..319 | ANCHOR_CANDIDATE;BRANCH_CANDIDATE |
| 1 | 3 | 27..235 | BRANCH_CANDIDATE |
| 10 | 5 | 45..242 | BRANCH_CANDIDATE |
| 11 | 3 | 47..229 | BRANCH_CANDIDATE |
| 2 | 5 | 29..222 | BRANCH_CANDIDATE |
| 3 | 8 | 31..316 | BRANCH_CANDIDATE |
| 4 | 13 | 33..285 | BRANCH_CANDIDATE |
| 5 | 3 | 35..245 | BRANCH_CANDIDATE |
| 6 | 17 | 37..324 | ANCHOR_CANDIDATE;BRANCH_CANDIDATE |
| 7 | 3 | 39..219 | BRANCH_CANDIDATE |
| 8 | 13 | 41..282 | BRANCH_CANDIDATE |
| 9 | 9 | 43..321 | BRANCH_CANDIDATE |

## Roster Lane Summary

| roster lane | rows | A candidate range | anchor statuses |
| --- | ---: | --- | --- |
| ACTINIDE_TERMINUS_ROSTER_LANE | 7 | 210..235 | BRANCH_CANDIDATE |
| DENSE_CONTEXT_ANCHOR_ROSTER_LANE | 3 | 195..232 | ANCHOR_CANDIDATE |
| EXACT_CLOSURE_ANCHOR_ROSTER_LANE | 27 | 2..205 | ANCHOR_CANDIDATE |
| HALF_WRITE_ANCHOR_ROSTER_LANE | 12 | 37..207 | ANCHOR_CANDIDATE |
| OFF_AXIS_BRANCH_ROSTER_LANE | 8 | 27..171 | BRANCH_CANDIDATE |
| QUARTER_BRANCH_ROSTER_LANE | 10 | 31..166 | BRANCH_CANDIDATE |
| SIXTH_BRANCH_ROSTER_LANE | 8 | 29..169 | BRANCH_CANDIDATE |
| SYNTHETIC_TRANSIENT_ROSTER_LANE | 26 | 240..324 | BRANCH_CANDIDATE |
| TRIADIC_BRANCH_ROSTER_LANE | 17 | 33..237 | BRANCH_CANDIDATE |

## Key Counts

```text
roster_rows_emitted = 118
anchor_candidate_rows = 42
branch_candidate_rows = 76
roster_lane_count = 9
observed_isotope_masses_used = false
free_parameters_introduced = 0
next_frontier = QP054_PRIVATE_ISOTOPE_NEIGHBOR_LADDER_SELECTOR
```

## Interpretation

QP053 fills the first isotope roster/stability layer. QP052 produced a single
candidate isotope surface; QP053 now marks whether each row is an exact/half
anchor candidate, a structured residual branch, or a synthetic/transient route.
