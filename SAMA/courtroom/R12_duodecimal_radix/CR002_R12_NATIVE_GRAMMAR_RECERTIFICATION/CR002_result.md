# CR002 R12 Native Grammar Recertification

## Verdict

```text
CR002_BOUNDARY_NATIVE_GRAMMAR_RECERTIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
```

## Selected Packet

```text
selected_R = 12
route_kernel = 12
partition_top = 12
A_share = 1/12
A_side = 1/24
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| trace_ascii_clean | true |
| route_kernel_equals_partition_top | true |
| unique_full_packet_selector | true |
| selected_R_is_12 | true |
| wrong_controls_do_not_match_full_packet | true |

## Wrong Controls

| control | R | full_packet | selector_score | fail_reasons |
|---|---:|---:|---:|---|
| decimal_convenience_R10 | 10 | false | 2 | route_kernel_equality;partition_top_equality;third_partition_admissible;fourth_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible;no_new_prime_axis;radix_wall_rejection |
| binary_expansion_R8 | 8 | false | 5 | route_kernel_equality;partition_top_equality;third_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible |
| side_count_as_completed_share_R24 | 24 | false | 8 | route_kernel_equality;partition_top_equality |
| half_route_only_R6 | 6 | false | 6 | route_kernel_equality;partition_top_equality;fourth_partition_admissible;twelfth_closure_admissible |
| prime_wall_R5 | 5 | false | 1 | route_kernel_equality;partition_top_equality;half_write_admissible;third_partition_admissible;fourth_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible;no_new_prime_axis;radix_wall_rejection |
| prime_wall_R7 | 7 | false | 1 | route_kernel_equality;partition_top_equality;half_write_admissible;third_partition_admissible;fourth_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible;no_new_prime_axis;radix_wall_rejection |
| prime_wall_R11 | 11 | false | 1 | route_kernel_equality;partition_top_equality;half_write_admissible;third_partition_admissible;fourth_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible;no_new_prime_axis;radix_wall_rejection |
| binary_square_R16 | 16 | false | 5 | route_kernel_equality;partition_top_equality;third_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible |
| decimal_twenty_R20 | 20 | false | 3 | route_kernel_equality;partition_top_equality;third_partition_admissible;six_contact_route_admissible;twelfth_closure_admissible;no_new_prime_axis;radix_wall_rejection |

## Rule-9 Line

```text
This test could have falsified: the claim that R=12 is selected by native SAM write/exposure grammar rather than inherited preference or later downstream fit.
```

## Courtroom Reading

CR002 is a clean native grammar recertification. It selects R=12 from
declared SAM grammar premises and rejects the wrong controls. It does not
supply an external downstream datum by itself, so the strict Courtroom
scientific verdict remains BOUNDARY.
