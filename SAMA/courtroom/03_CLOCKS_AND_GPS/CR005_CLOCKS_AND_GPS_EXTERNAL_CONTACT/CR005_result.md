# CR005 Clock and GPS External Contact

## Verdict

```text
CR005_PASS_SCOPED_CLOCKS_GPS_EXTERNAL_CONTACT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_CLOCKS_GPS
```

## Branch Claim Tested

```text
A(r) = r_s/r = 2GM/(c^2 r)
dtau/dt = sqrt(1 - A)
GPS gravity gain + declared SR orbital motion loss -> net correction
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| external_data_required | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_gravity_gain_in_external_range | true |
| sam_sr_loss_in_external_range | true |
| sam_net_correction_in_external_range | true |
| sam_factory_frequency_in_external_range | true |
| exact_and_weak_limits_agree | true |
| wrong_controls_do_not_match_full_packet | true |

## SAM Packet

| quantity | value |
|---|---:|
| A_ground | 1.390697013601e-09 |
| A_orbit | 3.339629547528e-10 |
| gps_orbit_speed_m_s | 3873.957505513 |
| gravity_exact_us_day | 45.650919844320 |
| sr_exact_us_day | -7.213602515321 |
| net_exact_us_day | 38.437317328999 |
| factory_frequency_hz | 10229999.995448915288 |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM weak-field A-clock readout from A(r)=r_s/r recovers the GPS gravitational clock gain, and that the declared SR orbital motion correction yields the observed net GPS daily correction and factory frequency offset without fitted parameters.
```

## Courtroom Reading

CR005 gives the clocks/GPS branch an external-contact PASS in a scoped
GPS clock-correction lane. It does not claim Shapiro delay, full GPS
engineering, full GR, or an independent derivation of SR.
