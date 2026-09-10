# CR006 Photon Road Shapiro External Contact

## Verdict

```text
CR006_PASS_SCOPED_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_PHOTON_ROAD_SHAPIRO
```

## Branch Claim Tested

```text
A(r) = r_s/r = 2GM/(c^2 r)
T_A^gamma = (1/c) integral A ds
Photon road integral -> first-order Shapiro logarithmic delay
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| external_data_required | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_gamma_within_cassini_bound | true |
| sam_delay_in_geometry_window | true |
| sam_integral_matches_log_law | true |
| impact_dependence_matches_log_shape | true |
| endpoint_clock_only_rejected | true |
| wrong_radial_shape_rejected | true |
| wrong_controls_do_not_match_full_packet | true |

## SAM Packet

| quantity | value |
|---|---:|
| impact_over_R_sun | 1.600000 |
| impact_m | 1113120000.000000 |
| r_s_m | 2953.339382066878 |
| integral_A_ds_m | 39337.432118325312 |
| delay_us | 131.215549519679 |
| standard_log_delay_us | 131.215549519703 |
| log_relative_diff | 1.790952533800e-13 |
| gamma_eff | 1.000000000000 |

## Shape Check

| quantity | value |
|---|---:|
| max_shape_relative_diff | 3.520710828705e-13 |
| wrong_shape_max_relative_diff | 7.823263434636e-01 |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's photon-road exposure T_A^gamma=(1/c)integral A ds, using A(r)=r_s/r, recovers the first-order Shapiro logarithmic delay with Cassini-bounded PPN gamma = 1 and the correct impact-parameter dependence without fitted parameters.
```

## Courtroom Reading

CR006 gives the photon-road Shapiro branch an external-contact PASS in a
scoped first-order solar-system lane. It does not claim full null-geodesic
derivation, full PPN closure, strong-field photon propagation, cosmological
lensing-time delay closure, a new light-speed law, or full GR.
