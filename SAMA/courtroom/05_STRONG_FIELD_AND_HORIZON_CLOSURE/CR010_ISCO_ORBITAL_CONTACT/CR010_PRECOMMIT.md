# CR010 Precommit

## Test ID

```text
CR010_ISCO_ORBITAL_CONTACT
```

## Test Type

```text
Fresh Courtroom 05-branch subtest.
Not a confirmation audit of an old result.
Legacy strong-field notes are provenance only, not computed inputs.
```

## Question

```text
Given the CR007 ISCO landmark A = 1/3 at r/r_s=3, does the declared
strong-field timelike circular-orbit lane show that the SAM A-kernel naturally
indexes the standard ISCO contact without a new parameter?
```

## Frozen Formula Set

```text
x = r/r_s
A = 1/x
h(A) = 1 - A

timelike circular-orbit lane:
E/c^2 = (1 - 1/x) / sqrt(1 - 3/(2x))
L/(m c r_s) = x / sqrt(2x - 3)
Omega r_s/c = 1 / sqrt(2 x^3)
```

The ISCO contact requires:

```text
x_ISCO = r/r_s = 3
A_ISCO = 1/3
E_ISCO/c^2 = sqrt(8/9)
L_ISCO/(m c r_s) = sqrt(3)
Omega_ISCO r_s/c = 1/sqrt(54)
L^2 has its circular-orbit stability minimum at x=3
```

## Expected Verdict Discipline

```text
CR010 may earn scoped external-contact PASS as a strong-field landmark contact
for the SAM A-kernel ISCO indexing lane.
CR010 records the declared ISCO packet, wrong-control rejection, and artifact
hashes needed for the CR011 deferred-support ledger.
```

## Pass Conditions

```text
no_older_test_outputs_used = true
sealed_scope_predates_test = true
cr007_typed_premise_present = true
cr008_typed_boundary_present = true
cr009_typed_photon_contact_present = true
external_reference_required = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
sam_isco_x_exact = true
sam_isco_A_exact = true
sam_isco_energy_exact = true
sam_isco_angular_momentum_exact = true
sam_isco_frequency_exact = true
sam_isco_is_local_stability_minimum = true
wrong_controls_do_not_match_full_packet = true
declared_readout_preserved = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that the CR007 A = 1/3 ISCO landmark
naturally indexes the standard strong-field timelike circular-orbit ISCO
contact r/r_s=3 with E/c^2=sqrt(8/9), L/(m c r_s)=sqrt(3), and
Omega r_s/c=1/sqrt(54), rather than being only an internal A-label or an
orbit-wrong construction that preserves a nearby landmark.
```
