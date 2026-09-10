# CR006 Precommit

## Test ID

```text
CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT
```

## Test Type

```text
Fresh Courtroom branch test.
Not a confirmation audit of an old result.
Legacy G372/G343/G376/G510A entries are provenance only, not computed inputs.
```

## Question

```text
Does SAM's photon-road exposure T_A^gamma=(1/c)integral A ds recover the
first-order solar-system Shapiro delay with the correct external Cassini gamma
coefficient and impact-parameter dependence?
```

## Frozen Formula Set

```text
A(r) = 2GM/(c^2 r)
T_A^gamma = (1/c) integral A ds
r(x) = sqrt(x^2 + b^2)
integral A ds = r_s * [asinh(x_1/b) + asinh(x_2/b)]
Delta t_log = (r_s/c) * log((r_1+r_2+R)/(r_1+r_2-R))
gamma_eff = 2*A_scale - 1
```

## External Anchors

```text
Cassini PPN gamma bound: |gamma - 1| <= 2.3e-5
one-way Earth-to-Cassini-style solar-grazing delay window: [130, 132] microseconds
```

## Pass Conditions

```text
no_older_test_outputs_used = true
external_data_required = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
sam_gamma_within_cassini_bound = true
sam_delay_in_geometry_window = true
sam_integral_matches_log_law = true
impact_dependence_matches_log_shape = true
endpoint_clock_only_rejected = true
wrong_controls_do_not_match_full_packet = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's photon-road exposure
T_A^gamma=(1/c)integral A ds, using A(r)=r_s/r, recovers the first-order
Shapiro logarithmic delay with Cassini-bounded PPN gamma = 1 and the correct
impact-parameter dependence without fitted parameters.
```
