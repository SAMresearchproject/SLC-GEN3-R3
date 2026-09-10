# CR013 Precommit

## Test ID

```text
CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE
```

## Test Type

```text
Fresh Courtroom branch test.
Not a pointer to a G-test verdict.
The G688c row artifact is used as source data rows, not as a pass verdict.
```

## Question

```text
Does the SN luminosity/clock/flux route reduce to the settled A_los photon-road
kernel without BAO inputs?
```

## Frozen Formula Set

```text
A0 = 1/(pi*R)
A_los(z) = A0*R*(1-(1+z)^(-D))
c_eff(z) = c*(1-A_los(z))
d_native = d_readout*(1-A_los(z))
mu_native = mu_obs + 5*log10(1-A_los(z))
```

## Wrong Controls

```text
no_shrink
half_A
constant_median_A
D2_power
linear_z_clipped
```

## Pass Conditions

```text
no_older_test_verdicts_used = true
free_parameters_introduced_zero = true
sn_source_rows_present = true
bao_inputs_not_loaded = true
A_los_row_identity = true
c_eff_row_identity = true
native_distance_row_identity = true
native_mu_row_identity = true
low_z_shrink_near_zero = true
high_z_shrink_larger_than_low_z = true
wrong_controls_do_not_match_packet = true
```

## Rule-9 Line

```text
This test could have falsified: the SN ledger claim if Pantheon SN rows did not
recompute from A_los(z), if the luminosity-distance shrink failed row identity,
if BAO inputs were needed, or if wrong controls matched the packet.
```

