# CR067b — Paul Revere NV-Center Simulator V1.0 — CRYO+DD — PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-18
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Test class:** PAUL_REVERE_PROTOCOL_NV_CENTER_CLASSICAL_SIMULATOR_V1_CRYO_DD
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repository root.

---

## Scope

CR067b is the **cryogenic + dynamical decoupling** version of the Paul Revere self-correction simulator. Architecturally identical to CR067a; only the NV operating-point parameters change:

```text
CR067a (room temperature):   T1 = T2 = 1 ms       (limited by phonons and spin bath)
CR067b (cryo + DD):           T1 = T2 = 1 s        (Hanson group operating regime)
```

This CR exists because CR067a recorded a near-miss on P3 (sensor population preservation) at room-temperature parameters: the 100 us open window is 10% of T1 = 1 ms, so T1 relaxation moved ~10% of the |m_s = -1> sensor population to |m_s = 0>, putting the sensor preservation ratio at 0.905 vs the 0.95 threshold. The near-miss was honest physics, not a protocol bug.

CR067b runs the same architecture at cryo+DD parameters where the same 100 us window is 0.01% of T1. Sensor relaxation is negligible. All 10 predictions are expected to pass cleanly. If they do, CR067b becomes the partner-lab-reference operating-point characterization.

## Architectural relationship to CR067a

```text
CR067a  =  same protocol, same code architecture, room-temp parameters  (9/10 + 7/7)
CR067b  =  same protocol, same code architecture, cryo+DD parameters    (expected 10/10 + 7/7)
```

CR067b does NOT supersede CR067a. CR067a stays sealed as the room-temperature characterization (useful in its own right — many academic NV groups operate at room temp). CR067b adds the cryo+DD reference point.

## Upstream dependencies (hash-locked typed premises)

```text
A0-a_h-D foundation
CR060a_alphabet_lock.json              d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock.json             c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock.json        38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock.json        c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9
CR067a_result_md_sha256                da44a9cb33bb756d408efad91e86ce7344191f5fa329ffdbb2ff8359b8e9b1cf
CR068a_result_md_sha256                aed3e4cca2fa5cd4a6e78d003aa617c71eead4ba18d8f2a3324ad9be8f8e9ba9
CR121_gravity_mechanism_intake_lock.json  01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469
CR129b_magnitude_lock.json             8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd
```

## NV center cryo+DD parameters

```text
T1_cryo_dd_s     = 1.0          (1 second; Hanson group typical at 4 K, isotopically purified)
T2_cryo_dd_s     = 1.0          (1 second; CPMG/KDD dynamical decoupling at 4 K)
open_window_s    = 1.0e-4       (same 100 us window as CR067a)
drift_angle_rad  = 0.5          (same drift injection as CR067a)
omega_drive_test = 2 * pi * 2.87e9 rad/s  (same as CR067a)
```

Operating-point source: Bar-Gill et al. ¹²C-enriched NV with KDD; Maurer et al. NV nuclear-coupled T2 ~ 1 s at 4 K [VERIFY_PRECOMMIT_FOR_PARTNER_LAB_HAND_OFF].

## Foundation primitives (frozen at A0-a_h-D)

```text
R       = 12
D       = 3
alpha_H = 2
A_0     = 1/(12*pi)
A_share = 1/12
A_side  = 1/24
```

## Loaded state target (per CR066a, same as CR067a)

```text
|psi_loaded> = sqrt(4/17) |m_s = 0>     (carrier)
             + sqrt(9/17) |m_s = +1>    (envelope, the letter)
             + sqrt(4/17) |m_s = -1>    (sensor)
```

## Predictions (same as CR067a — frozen before runner execution)

- **P1_loaded_state_amplitudes_correct** — populations match (4/17, 9/17, 4/17) within 1e-6
- **P2_carrier_population_preserved_through_correction** — carrier P >= 0.95 * loaded
- **P3_sensor_population_preserved_through_correction** — sensor P >= 0.95 * loaded **[the CR067a near-miss; expected to clean-pass here]**
- **P4_envelope_drift_correction_reduces_drift_by_at_least_50_percent**
- **P5_no_clone_attempt_returns_invalid_state**
- **P6_premature_commit_returns_refused_flag**
- **P7_T2_grav_floor_consistency**
- **P8_3_level_qutrit_dynamics_unitary_in_no_decoherence_limit**
- **P9_decoherence_recovered_when_T1_T2_finite** **[the purity decay will be much smaller at cryo; verify decoherence is still detected]**
- **P10_protocol_completes_end_to_end**

## Wrong controls (same as CR067a)

- **WC1_wrong_loaded_state_amplitudes_produce_different_populations**
- **WC2_swapped_slot_assignment_violates_protocol_structure**
- **WC3_zero_decoherence_gives_perfect_coherence**
- **WC4_clone_attempt_reduces_purity**
- **WC5_premature_read_before_selected_write_returns_no_logical_outcome**
- **WC6_runner_does_not_modify_upstream_locks**
- **WC7_no_free_parameters_introduced**

## Outputs (committed before runner execution)

```text
CR067b_simulator_lock.json
CR067b_runner.py  (paul_revere_nv_simulator_v1_cryo.py)
CR067b_results.csv
CR067b_summary.json
CR067b_evolution_plot.png
CR067b_result.md
HASHES.txt
```

## Falsifiers

Same as CR067a. If P3 fails at cryo+DD parameters with sensor preservation < 0.95, that is structurally different from the CR067a near-miss and indicates a real protocol issue (not a parameter-regime issue). Either falsification would trigger structural diagnosis, not threshold adjustment.

## Free parameters

```text
free_parameters = 0
```

## Scope boundary

CR067b IS:
- Classical software simulation of CR067a's self-correction architecture at Hanson-group operating-point parameters
- Reference characterization for partner-lab hand-off
- Cryo-regime data point in the CR067 series

CR067b IS NOT:
- A claim that real cryo+DD NV hardware will reproduce these specific numbers (requires Stage 4)
- A supersession of CR067a (the room-temp record stands on its own)
- A claim of quantum advantage

## Pre-execution seal

PRECOMMIT.md is hash-sealed before runner execution. The predictions and wrong controls are identical to CR067a; only the operating-point parameters change.
