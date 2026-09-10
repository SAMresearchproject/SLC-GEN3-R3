# CR067a — Paul Revere NV-Center Simulator V1.0 — PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-17
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Test class:** PAUL_REVERE_PROTOCOL_NV_CENTER_CLASSICAL_SIMULATOR_V1
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

This artifact is part of the SAM private research record. No license is granted for use, copying, modification, distribution, or commercialization. Read access for independent verification may be requested under written terms. All commercial use is prohibited. See `STEWARDSHIP.md` in repository root for the stewardship intent that governs any future commercial licensing.

---

## Scope

CR067a implements the **Paul Revere protocol** (CR065a_implementation_lock) as a faithful classical simulation on the NV⁻ ³A₂ ground-state triplet, using realistic NV-center physics (zero-field splitting D_zfs ≈ 2.87 GHz, microwave drive on |0⟩↔|±1⟩ transitions, Lindblad-form T1/T2 decoherence). The simulator runs the loading → open-window → letter-preserving drift correction → delayed-read protocol cycle and demonstrates the refusal stack.

This is a **classical software simulation**, not a hardware demonstration. It validates protocol self-consistency on a physics-faithful model; it does not validate that real NV hardware will reproduce predicted behavior.

## Upstream dependencies (hash-locked typed premises)

```text
CR060a_alphabet_lock.json              d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock.json             c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock.json        38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock.json        c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9
CR121_gravity_mechanism_intake_lock.json  01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469
CR129b_magnitude_lock.json             8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd
```

## Foundation primitives (frozen at A0-a_h-D)

```text
R       = 12
D       = 3
alpha_H = 2
A_0     = 1 / (12 * pi)
A_share = 1/12
A_side  = 1/24
```

## NV center physical parameters

```text
spin             = 1                          (NV ground state triplet)
basis            = {|m_s = -1>, |m_s = 0>, |m_s = +1>}
D_zfs            = 2.87e9 Hz                  (zero-field splitting)
T1_room_temp     = 1e-3 s                     (representative)
T2_room_temp     = 1e-3 s                     (Hahn echo, no DD)
T2_cryo_DD       = 1.0 s                      (CPMG/KDD, Hanson group)
omega_drive_test = 2 * pi * 2.87e9 rad/s      (resonant microwave drive)
```

## Loaded state target (per CR066a Born extension)

The CR066a structural slot weights are `(1/4, 9/16, 1/4)` summing to `17/16`. As a normalized quantum state on the qutrit, the loaded probabilities are `(4/17, 9/17, 4/17)` with amplitudes:

```text
|psi_loaded> = sqrt(4/17) |m_s = 0>     (carrier)
             + sqrt(9/17) |m_s = +1>    (envelope, the letter)
             + sqrt(4/17) |m_s = -1>    (sensor)
```

The 1/16 letter increment is structural; the renormalized amplitudes are the physically realizable state on the qutrit.

## Slot assignment (frozen at CR065a hardware spec)

```text
slot_a_carrier   <-> m_s = 0       (route identity, protected pre-commit)
slot_b_envelope  <-> m_s = +1      (letter content / 9/8 surcharge)
slot_c_sensor    <-> m_s = -1      (boundary stress readout)
```

## Predictions (frozen before runner execution)

- **P1_loaded_state_amplitudes_correct**
  After loading pulse, populations on (|0>, |+1>, |-1>) match (4/17, 9/17, 4/17) within 1e-6 absolute error.

- **P2_carrier_population_preserved_through_correction**
  After one full correction-loop cycle (window open → drift gate applied → window close), carrier population P(|0>) >= 0.95 * P_initial(|0>).

- **P3_sensor_population_preserved_through_correction**
  After one full correction-loop cycle, sensor population P(|-1>) >= 0.95 * P_initial(|-1>).

- **P4_envelope_drift_correction_reduces_drift_by_at_least_50_percent**
  Apply controlled drift on envelope (|+1>), then apply letter-preserving drift gate. Net envelope deviation reduced by >= 50% vs no-correction control.

- **P5_no_clone_attempt_returns_invalid_state**
  Attempting to copy the carrier amplitude into another qutrit register returns a state with purity < 1 (mixed) and trace_distance > 0.1 from the intended clone.

- **P6_premature_commit_returns_refused_flag**
  Attempting to read out the final ledger before the selected-write hash boundary returns a structured `RefusedCommit` exception or refusal flag.

- **P7_T2_grav_floor_consistency**
  At drive frequency omega_drive_test, the simulator's effective T2 floor (post-correction-loop) is consistent with the CR064a v1.1 prediction `T2_grav = 16 * pi * R^4 / (17 * omega_drive)` within order of magnitude.

- **P8_3_level_qutrit_dynamics_unitary_in_no_decoherence_limit**
  With T1=infinity and T2=infinity, the protocol evolves unitarily (state purity stays = 1 within 1e-12).

- **P9_decoherence_recovered_when_T1_T2_finite**
  With realistic NV T1/T2 values, state purity decreases monotonically during open windows; verify Lindblad evolution is correctly applied.

- **P10_protocol_completes_end_to_end**
  The full sequence `initialize -> load -> open_window -> drift -> correct -> delayed_read` runs to completion without numerical error and emits a typed `ProtocolResult` object.

## Wrong controls (frozen before runner execution)

- **WC1_wrong_loaded_state_amplitudes_produce_different_populations**
  Loading with amplitudes summing to a different value (e.g., uniform 1/3, 1/3, 1/3) should produce populations distinct from (4/17, 9/17, 4/17). Confirms loading pulse is doing real work.

- **WC2_swapped_slot_assignment_violates_protocol_structure**
  Assigning carrier <-> m_s = +1 (instead of m_s = 0) should fail the letter-preserving drift gate (the gate is structurally tied to acting on m_s = +1 as envelope). Confirms slot assignment is load-bearing.

- **WC3_zero_decoherence_gives_perfect_coherence**
  With Lindblad operators removed, state purity must stay at 1.0 to within numerical precision. Confirms decoherence injection is the only source of impurity in the with-decoherence run.

- **WC4_clone_attempt_reduces_purity**
  A successful attempt to copy the carrier amplitude into a second qutrit and measure it would produce a partial trace with purity < 1 on the original. Confirms no-cloning is enforced by quantum mechanics (and that the protocol's no-clone guard is consistent with that, not contradicting it).

- **WC5_premature_read_before_selected_write_returns_no_logical_outcome**
  Reading the carrier before the selected-write commit must return either a random measurement collapse or a `RefusedCommit` flag — NOT the logical route identity. Confirms delayed-resolution discipline.

- **WC6_runner_does_not_modify_upstream_locks**
  No upstream CR lock (CR060a, CR061a, CR065a, CR066a, CR121, CR129b) is modified during runner execution. Confirms the simulator is read-only with respect to upstream artifacts.

- **WC7_no_free_parameters_introduced**
  All NV physical constants (D_zfs, T1, T2) are sourced from published NV literature or marked `[VERIFY_PRECOMMIT]`. No SAM-side parameter is fitted to make the simulator produce a target output. Confirms zero_free_parameters = 0 inside this CR.

## Outputs (committed before runner execution)

```text
CR067a_simulator_lock.json        — locked structural parameters + slot assignment + predictions
CR067a_runner.py                  — executable simulator (this is paul_revere_nv_simulator_v1.py)
CR067a_results.csv                — row per protocol stage with populations, purity, residuals
CR067a_summary.json               — pass/fail per prediction, pass/fail per wrong control
CR067a_evolution_plot.png         — population vs time plot for the full protocol cycle
HASHES.txt                        — sha256 of all CR067a artifacts
CR067a_result.md                  — human-readable result document
```

## Falsifiers

This CR could falsify if:

1. Any of P1-P10 fails (the protocol math doesn't close on a faithful NV simulator) → the protocol architecture has a bug.
2. Any of WC1-WC7 fails to fail as expected → the simulator is not actually testing what it claims to test.
3. Wrong control WC1 returns populations matching (4/17, 9/17, 4/17) for a uniform input → the loading pulse is not implementing what it claims.
4. WC3 produces decoherence with no Lindblad operator → numerical error or wrong simulator construction.

Any falsification triggers a runner pause and a `BOUNDARY` verdict until the failure mode is structurally diagnosed.

## Free parameters

```text
free_parameters = 0
```

All structural inputs (R, D, alpha_H, A_0, slot weights, q-alphabet) come from upstream hash-locked CRs. All NV physical constants come from published literature with `[VERIFY_PRECOMMIT]` tags. No tuning parameter is introduced inside CR067a to make the simulator produce a target output.

## Scope boundary

CR067a IS:
- A classical-software simulation of the Paul Revere protocol on NV physics
- A self-consistency check on CR065a + CR066a
- A demonstration vehicle for investor / partner-lab / foundation evaluation

CR067a IS NOT:
- A hardware demonstration
- A validation of the T2_grav physical floor (that requires Stage 2: empirical contact with published NV measurements)
- A proof that any real NV center will behave as simulated
- A patentable claim on its own (the patentable claims are the protocol architecture itself, in CR065a)
- A claim of quantum advantage over existing platforms

## Reproduction-on-demand

This CR is reproducible by:

1. Installing the dependencies in `requirements.txt`
2. Running `python paul_revere_nv_simulator_v1.py`
3. Comparing the emitted `CR067a_summary.json` and `CR067a_results.csv` against this PRECOMMIT's declared predictions and wrong controls

All randomness (if any) is seeded; deterministic re-runs must produce byte-identical output.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before the runner is permitted to execute. Any modification to predictions, wrong controls, or scope after the runner produces output requires a new CR (CR067b or CR068) and explicit reason for change.
