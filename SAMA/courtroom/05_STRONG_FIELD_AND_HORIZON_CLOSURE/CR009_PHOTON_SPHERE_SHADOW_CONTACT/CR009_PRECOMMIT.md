# CR009 Precommit

## Test ID

```text
CR009_PHOTON_SPHERE_SHADOW_CONTACT
```

## Test Type

```text
Fresh Courtroom 05-branch subtest.
Not a confirmation audit of an old result.
Legacy G412/G57/G272/SUK034 entries are provenance only, not computed inputs.
```

## Question

```text
Given the CR007 photon-sphere landmark A=2/3, does the declared strong-field
photon lane recover the standard Schwarzschild photon sphere and shadow
critical-impact invariant without a new parameter?
```

## Frozen Formula Set

```text
x = r/r_s
A = 1/x
h(A) = 1 - A

b/r_s = x / sqrt(h)
       = x / sqrt(1 - 1/x)
```

The photon sphere / shadow contact requires:

```text
minimum of b/r_s occurs at x = 3/2
A = 2/3
b_crit/r_s = 3*sqrt(3)/2
shadow_diameter/r_s = 3*sqrt(3)
```

## Expected Verdict Discipline

```text
CR009 may earn scoped external-contact PASS for the Schwarzschild photon
sphere / shadow-invariant lane.
CR009 does not claim full EHT image modeling, Kerr shadow modeling, accretion
physics, or full strong-field metric closure.
```

## Pass Conditions

```text
no_older_test_outputs_used = true
sealed_scope_predates_test = true
cr007_typed_premise_present = true
cr008_typed_boundary_present = true
external_reference_required = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
sam_photon_sphere_x_exact = true
sam_photon_sphere_A_exact = true
sam_shadow_bcrit_exact = true
sam_shadow_diameter_exact = true
sam_minimum_is_local = true
wrong_controls_do_not_match_full_packet = true
eht_image_overclaim_rejected = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that the CR007 A=2/3 photon-sphere
landmark carries the standard Schwarzschild photon critical-impact/shadow
invariant b_crit/r_s=3*sqrt(3)/2, rather than being only an internal A-label or
a horizon-preserving but shadow-wrong construction.
```
