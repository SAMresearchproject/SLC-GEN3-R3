# CR005 Precommit

## Test ID

```text
CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT
```

## Test Type

```text
Fresh Courtroom branch test.
Not a confirmation audit of an old result.
Legacy G284c/G373/G376 entries are provenance only, not computed inputs.
```

## Question

```text
Does the SAM weak-field A-clock lane recover the GPS gravitational clock gain,
and does the declared SR orbital motion correction recover the observed net GPS
clock correction and factory offset?
```

## Frozen Formula Set

```text
A(r) = 2GM/(c^2 r)
clock(A) = sqrt(1 - A)
gravity_fraction_exact = sqrt(1-A_orbit)/sqrt(1-A_ground) - 1
gravity_fraction_weak = (A_ground - A_orbit)/2
sr_fraction_exact = sqrt(1 - v^2/c^2) - 1
sr_fraction_weak = -v^2/(2c^2)
net_fraction = gravity_fraction_exact + sr_fraction_exact
factory_frequency = nominal_frequency * (1 - net_fraction)
```

## External Anchors

```text
gravitational gain range: [45.4, 45.9] microseconds/day
SR motion loss range: [-7.4, -7.0] microseconds/day
net correction range: [38.0, 39.0] microseconds/day
factory frequency range: [10229999.9952, 10229999.9957] Hz
```

## Pass Conditions

```text
no_older_test_outputs_used = true
external_data_required = true
free_parameters_introduced_zero = true
trace_ascii_clean = true
sam_gravity_gain_in_external_range = true
sam_sr_loss_in_external_range = true
sam_net_correction_in_external_range = true
sam_factory_frequency_in_external_range = true
exact_and_weak_limits_agree = true
wrong_controls_do_not_match_full_packet = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that the SAM weak-field A-clock
readout from A(r)=r_s/r recovers the GPS gravitational clock gain, and that the
declared SR orbital motion correction yields the observed net GPS daily
correction and factory frequency offset without fitted parameters.
```
