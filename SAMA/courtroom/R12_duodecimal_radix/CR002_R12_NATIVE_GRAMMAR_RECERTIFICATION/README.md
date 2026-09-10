# CR002 R12 Native Grammar Recertification

## Preflight Target

```text
test_id = CR002_R12_NATIVE_GRAMMAR_RECERTIFICATION
branch_id = R12_duodecimal_radix
older_test_outputs_allowed = false
external_data_required = false
expected_verdict_ceiling = BOUNDARY
```

## Question

Can `R=12` be recertified from native SAM grammar without looking back at older
test outputs?

## Required Design

The test should declare premises before execution and then evaluate candidate
radices against native grammar selectors.

Minimum candidate set:

```text
R in {2, 3, 4, 6, 8, 10, 12, 16, 20, 24}
```

Minimum selector lanes:

```text
half_write_admissible
six_contact_route_admissible
third_partition_admissible
fourth_partition_admissible
sixth_partition_admissible
twelfth_partition_admissible
integer_closure_score
propagation_mode_support
```

## Falsification Line

```text
This test could have falsified: the claim that R=12 is selected by native SAM write/exposure grammar rather than inherited preference or later downstream fit.
```

## Expected Output Files

```text
CR002_PRECOMMIT.md
CR002_declared_premises.json
CR002_R12_native_grammar_recertification.py
CR002_candidate_rows.csv
CR002_wrong_controls.csv
CR002_summary.json
CR002_result.md
```
