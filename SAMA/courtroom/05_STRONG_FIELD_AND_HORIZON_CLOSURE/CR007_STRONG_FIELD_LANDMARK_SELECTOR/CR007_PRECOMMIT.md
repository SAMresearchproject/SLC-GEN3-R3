# CR007 Precommit

## Test ID

```text
CR007_STRONG_FIELD_LANDMARK_SELECTOR
```

## Test Type

```text
Fresh Courtroom branch test.
Not a confirmation audit of an old result.
Legacy G338 and related strong-field entries are provenance only, not computed inputs.
```

## Question

```text
Does the SAM A-profile A(r)=r_s/r organize the first Schwarzschild
strong-field landmark ladder as native A-values 1, 2/3, and 1/3?
```

## Frozen Formula Set

```text
A(r) = r_s/r
r_s = 2GM/c^2

horizon        r/r_s = 1
photon sphere  r/r_s = 3/2
ISCO           r/r_s = 3
```

## Expected Landmark Readout

```text
horizon        A = 1
photon sphere  A = 2/3
ISCO           A = 1/3
```

## Expected Verdict Discipline

```text
CR007 may succeed structurally but still receive scientific_verdict=BOUNDARY.
CR007 does not claim full empirical strong-field closure by itself.
Downstream CR008-CR010 may later provide deferred support.
```

## Pass Conditions

```text
no_older_test_outputs_used = true
sealed_scope_predates_test = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
sam_landmark_tuple_exact = true
landmark_order_preserved = true
mass_scale_invariance = true
wrong_controls_do_not_match_full_packet = true
empirical_overclaim_rejected = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's strong-field root
A(r)=r_s/r places the horizon, photon sphere, and ISCO at the ordered native
A-values 1, 2/3, and 1/3 without a new parameter or a landmark-specific rule.
```
