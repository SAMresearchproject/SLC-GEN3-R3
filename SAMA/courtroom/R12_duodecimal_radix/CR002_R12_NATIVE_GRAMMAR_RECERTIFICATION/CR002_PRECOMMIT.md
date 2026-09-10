# CR002 Precommit: R12 Native Grammar Recertification

## Test ID

```text
CR002_R12_NATIVE_GRAMMAR_RECERTIFICATION
```

## Branch

```text
R12_duodecimal_radix
```

## Question

Can `R=12` be selected as SAM's native write radix from declared native grammar
premises, without using older G-test outputs as inputs?

## Declared Premises

```text
outer_binary_split = 2
alpha_h = 2
D = 3
half_side_per_share = 2
primitive_phase_cycle_units = 2
```

## Candidate Radices

```text
R in {2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 16, 20, 24}
```

## Selectors

```text
route_kernel_equality: R == outer_binary_split * alpha_h * D
partition_top_equality: R == alpha_h^2 * D
half_write_admissible: R divisible by 2
third_partition_admissible: R divisible by D
fourth_partition_admissible: R divisible by alpha_h^2
six_contact_route_admissible: R divisible by alpha_h * D
twelfth_closure_admissible: R divisible by outer_binary_split * alpha_h * D
side_share_conservation: 2R half-sides collapse to R completed shares
no_new_prime_axis: prime factors of R are only drawn from {2, 3}
radix_wall_rejection: 5, 7, 10, 11 are not full-packet candidates
```

## Falsification Line

```text
This test could have falsified: the claim that R=12 is selected by native SAM write/exposure grammar rather than inherited preference or later downstream fit.
```

## Expected Verdict Ceiling

```text
scientific_verdict <= BOUNDARY
```

Reason: this is a native grammar recertification. It can certify typed SAM
structure, but it does not supply external downstream data by itself.
