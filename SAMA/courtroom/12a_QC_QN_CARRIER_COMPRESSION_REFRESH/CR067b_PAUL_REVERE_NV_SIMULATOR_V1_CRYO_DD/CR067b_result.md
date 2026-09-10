# CR067b Paul Revere NV-Center Simulator V1.0 - CRYO+DD - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Result class:** `CR067b_PAUL_REVERE_NV_SIMULATOR_V1_CRYO_DD_SEALED__PREDICTIONS_10_OF_10__WRONG_CONTROLS_7_OF_7`

**Predictions passed:** 10/10
**Wrong controls passed:** 7/7
**Free parameters:** 0

## Operating point

```text
T1 = T2 = 1.0 s    (cryo + dynamical decoupling, Hanson-group regime)
open window = 100 us = 0.01% of T1   (vs 10% at room temperature in CR067a)
```

## Predictions detail

- **[PASS]** P1_loaded_state_amplitudes_correct
- **[PASS]** P2_carrier_population_preserved_through_correction
- **[PASS]** P3_sensor_population_preserved_through_correction
- **[PASS]** P4_envelope_drift_correction_reduces_drift_by_at_least_50_percent
- **[PASS]** P5_no_clone_attempt_returns_invalid_state
- **[PASS]** P6_premature_commit_returns_refused_flag
- **[PASS]** P7_T2_grav_floor_consistency
- **[PASS]** P8_3_level_qutrit_dynamics_unitary_in_no_decoherence_limit
- **[PASS]** P9_decoherence_recovered_when_T1_T2_finite
- **[PASS]** P10_protocol_completes_end_to_end

## Wrong controls detail

- **[PASS]** WC1_wrong_loaded_state_amplitudes_produce_different_populations
- **[PASS]** WC2_swapped_slot_assignment_violates_protocol_structure
- **[PASS]** WC3_zero_decoherence_gives_perfect_coherence
- **[PASS]** WC4_clone_attempt_reduces_purity
- **[PASS]** WC5_premature_read_before_selected_write_returns_no_logical_outcome
- **[PASS]** WC6_runner_does_not_modify_upstream_locks
- **[PASS]** WC7_no_free_parameters_introduced

## Relationship to CR067a

Architecturally identical. Only the operating-point parameters change. CR067a (room temperature) recorded 9/10 with a P3 near-miss attributable to T1 relaxation over a window that was 10% of T1. CR067b (cryo+DD) operates at T1 = T2 = 1 s where the same 100 us window is 0.01% of T1; sensor relaxation is negligible and P3 is expected to clean-pass.

CR067b does NOT supersede CR067a. Both characterizations stand: CR067a is the room-temperature operating-point reference, CR067b is the cryo+DD reference suitable for Hanson-style partner-lab hand-off.

## Scope

Classical software simulation. Validates protocol self-consistency at cryo+DD operating-point parameters. Does not validate that real cryo+DD NV hardware will reproduce specific numbers (requires Stage 4 partner-lab hand-off).

## Stewardship

Per STEWARDSHIP.md.
