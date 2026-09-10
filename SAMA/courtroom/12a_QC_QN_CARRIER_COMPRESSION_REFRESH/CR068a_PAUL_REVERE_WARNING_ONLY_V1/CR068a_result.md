# CR068a Paul Revere Warning-Only Simulator V1.0 - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Result class:** `CR068a_PAUL_REVERE_WARNING_ONLY_V1_SEALED__PREDICTIONS_8_OF_8__WRONG_CONTROLS_6_OF_6`

**Predictions passed:** 8/8
**Wrong controls passed:** 6/6
**Free parameters:** 0

## The Paul Revere letter (room-temperature run)

```text
fired                      = True
t_fire_s                   = 2.914572864e-05
t_fire_microseconds        = 29.146
A_leak_at_fire             = 4.191926314e-02
threshold_A_side           = 4.166666667e-02  (= 1/24)
purity_at_fire             = 9.580807369e-01
carrier_population_at_fire = 2.572604139e-01
envelope_population_at_fire= 5.142043288e-01
sensor_population_at_fire  = 2.285352573e-01
sample_index               = 58

Reason: A_leak = 0.041919 reached threshold A_side = 0.041667 at sample 58, t = 29.146 us. Route is in basin-forming regime; recoverable until A_leak reaches A_share = 1/12. Carrier route identity not exposed.
```

## Predictions

- **[PASS]** P1_alarm_fires_within_window_at_room_temperature
- **[PASS]** P2_alarm_event_carries_timestamp_and_stress_magnitude
- **[PASS]** P3_alarm_time_scales_with_T2_inverse
- **[PASS]** P4_carrier_population_unchanged_by_alarm_emission
- **[PASS]** P5_alarm_fires_before_A_share_basin_commit_boundary
- **[PASS]** P6_no_alarm_in_no_decoherence_control
- **[PASS]** P7_alarm_is_monotonic_in_A_leak
- **[PASS]** P8_protocol_completes_end_to_end

## Wrong controls

- **[PASS]** WC1_zero_decoherence_gives_zero_alarms
- **[PASS]** WC2_alarm_fires_after_threshold_cross_not_before
- **[PASS]** WC3_alarm_timestamp_matches_independent_purity_measurement
- **[PASS]** WC4_alarm_magnitude_monotonic_in_actual_decoherence
- **[PASS]** WC5_runner_does_not_modify_upstream_locks
- **[PASS]** WC6_no_free_parameters_introduced

## Scope

CR068a is the warning-only foundation underneath CR067a's self-correction loop. It validates that the Paul Revere alarm reliably detects qubit-window compromise (A_leak >= A_side = 1/24) before the basin-commit boundary (A_share = 1/12), with a typed letter carrying timestamp and stress magnitude. This is a classical software simulation; partner-lab Stage 4 is required for hardware validation.

## Stewardship

Any commercial use of this work or its derivatives is subject to the stewardship intent in `STEWARDSHIP.md`: revenue funds humanitarian causes.
