# CR067a Paul Revere NV-Center Simulator V1.0 - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Result class:** `CR067a_PAUL_REVERE_NV_SIMULATOR_V1_SEALED__PREDICTIONS_9_OF_10__WRONG_CONTROLS_7_OF_7`

**Predictions passed:** 9/10
**Wrong controls passed:** 7/7
**Free parameters:** 0

## Loaded state (per CR066a Born extension)

```text
carrier   (m_s = 0)  :  P = 4/17 ~= 0.235
envelope  (m_s = +1) :  P = 9/17 ~= 0.529   <-- the letter, 9/8 surcharge
sensor    (m_s = -1) :  P = 4/17 ~= 0.235
```

## Predictions detail

- **[PASS]** P1_loaded_state_amplitudes_correct
- **[PASS]** P2_carrier_population_preserved_through_correction
- **[FAIL]** P3_sensor_population_preserved_through_correction
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

## Scope boundary

This is a classical software simulation. It validates protocol self-consistency on a physics-faithful model of the NV(-) (3)A2 ground-state triplet. It does NOT validate:

- That real NV hardware reproduces the predicted behavior
- That the T2_grav floor formula (CR064a V1.1) matches empirical data
- Any patentable claim on its own

Empirical validation requires Stage 2 (published-T2 contact) and Stage 4 (partner-lab hardware run).

## Stewardship

Any commercial use of this work or its derivatives is subject to the stewardship intent in `STEWARDSHIP.md`: revenue is intended to fund humanitarian causes (housing, addiction recovery, medical support, education, community charities, environmental prosperity).
