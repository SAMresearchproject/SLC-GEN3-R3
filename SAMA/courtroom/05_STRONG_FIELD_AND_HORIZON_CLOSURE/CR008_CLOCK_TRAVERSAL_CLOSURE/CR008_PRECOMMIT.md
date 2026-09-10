# CR008 Precommit

## Test ID

```text
CR008_CLOCK_TRAVERSAL_CLOSURE
```

## Test Type

```text
Fresh Courtroom 05-branch subtest.
Not a confirmation audit of an old result.
Legacy G339 and related horizon/redshift entries are provenance only, not
computed inputs.
```

## Question

```text
Given the CR007 A=1 horizon landmark, does the declared strong-field
clock/traversal lane force operational closure as A approaches 1?
```

## Frozen Formula Set

```text
lapse(A) = sqrt(1 - A)
redshift(A) = 1/sqrt(1 - A) - 1

For outside-ledger radial photon traversal:

x = r/r_s
A = 1/x
dt * c/r_s = integral dx/(1 - 1/x)
             = integral x/(x - 1) dx
             = (x_2 - x_1) + log((x_2 - 1)/(x_1 - 1))
```

The traversal closure check uses:

```text
x_1 = 1 + epsilon
x_2 = 3
epsilon in {1e-3, 1e-6, 1e-9, 1e-12}
```

## Expected Verdict Discipline

```text
CR008 may structurally validate the clock/traversal closure behavior and still
receive scientific_verdict=BOUNDARY.
CR008 does not claim full infalling-observer physics.
CR008 does not claim full strong-field metric closure.
```

## Pass Conditions

```text
no_older_test_outputs_used = true
sealed_scope_predates_test = true
cr007_typed_premise_present = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
low_A_limit_matches_weak_clock = true
weak_clock_rejected_at_isco = true
redshift_diverges_as_A_to_1 = true
lapse_goes_to_zero_as_A_to_1 = true
outside_traversal_log_diverges = true
closure_at_A1_not_photon_or_isco = true
wrong_controls_do_not_match_full_packet = true
infalling_observer_overclaim_rejected = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that the CR007 A=1 horizon landmark
is an operational clock/traversal closure boundary under the declared
strong-field lane lapse(A)=sqrt(1-A), rather than a label that remains finite
or shifts closure to the photon sphere or ISCO.
```
