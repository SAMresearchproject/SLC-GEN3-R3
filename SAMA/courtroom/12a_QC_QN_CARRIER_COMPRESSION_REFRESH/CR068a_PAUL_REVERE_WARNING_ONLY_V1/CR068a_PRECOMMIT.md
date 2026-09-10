# CR068a — Paul Revere Warning-Only Simulator V1.0 — PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-17
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Test class:** PAUL_REVERE_WARNING_ONLY_NV_CENTER_CLASSICAL_SIMULATOR_V1
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repository root.

---

## Scope

CR068a implements the **warning-only** version of the Paul Revere protocol on the NV⁻ ³A₂ ground-state triplet — the foundation that the self-correction version (CR067a) builds on. The warning-only version does exactly one thing well: it detects when the protected qubit window has been compromised, before the compromise commits to the ledger, and emits a typed alarm event with timestamp and stress magnitude.

This is the historical Paul Revere — *"the British are coming"* — a warning that arrives ahead of the harm. It does not act on the harm. The correction layer that acts on the warning is CR067a; this CR establishes the foundation underneath it.

CR068a is structurally simpler than CR067a:
- No drift gate
- No letter-preserving correction gate
- One observable (`A_leak = 1 − purity`)
- One threshold (`A_side = 1/24` per page-one SAM thresholds)
- One event (the alarm)

## Upstream dependencies (hash-locked typed premises)

```text
A0-a_h-D foundation                    (R = 12, D = 3, alpha_H = 2, A_0 = 1/(12*pi))
CR060a_alphabet_lock.json              d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock.json             c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock.json        38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock.json        c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9
CR067a_simulator_result_sha256         da44a9cb33bb756d408efad91e86ce7344191f5fa329ffdbb2ff8359b8e9b1cf
```

## SAM threshold hierarchy (page-one)

```text
A_leak < 1/24      ->  protected unresolved route                    (no alarm)
1/24 <= A_leak < 1/12  ->  write-candidacy / basin forming           (ALARM fires)
A_leak >= 1/12     ->  uncontrolled write - route is gone            (too late)
```

The warning fires at A_leak >= A_side = 1/24 — the entrance to the basin-forming regime, *before* the route commits. This is the structural job of the Paul Revere letter: arrive at the alarm boundary, not at the commit boundary.

## A_leak definition

```text
A_leak = 1 - Tr(rho^2)   = 1 - purity
```

A pure state has purity = 1 and A_leak = 0 (no leakage). Decoherence reduces purity; the leak is the loss. The alarm fires when accumulated leak reaches the structural A_side threshold.

This is the literal substrate-leak interpretation of decoherence per SAM §10.1 — *"decoherence is uncontrolled A leakage through the ledger-cell boundary."*

## Loaded state (per CR066a)

```text
|psi_loaded> = sqrt(4/17) |m_s = 0>     (carrier)
             + sqrt(9/17) |m_s = +1>    (envelope, the letter)
             + sqrt(4/17) |m_s = -1>    (sensor)
```

Sensor (m_s = -1) holds the boundary stress readout. The alarm monitor watches the global state purity, but the sensor slot is the physical boundary observer — when the alarm fires, the sensor is what reads out the stress.

## Predictions (frozen before runner execution)

- **P1_alarm_fires_within_window_at_room_temperature**
  With T1 = T2 = 1 ms and a 100 us open window, A_leak reaches A_side = 1/24 within the window. Alarm fires before t = 100 us.

- **P2_alarm_event_carries_timestamp_and_stress_magnitude**
  The alarm event payload contains `(t_fire, A_leak_at_fire, sensor_population_at_fire, carrier_population_at_fire)`. The letter delivers structure, not just a flag.

- **P3_alarm_time_scales_with_T2_inverse**
  Running at T2 = 0.1 ms and T2 = 1 ms (10x difference in decoherence rate), the alarm time should differ by approximately the same factor (within order-of-magnitude). Faster decoherence -> earlier alarm.

- **P4_carrier_population_unchanged_by_alarm_emission**
  Comparing carrier (m_s = 0) population at the alarm-fire sample vs the previous sample shows no jump attributable to the alarm itself. The alarm is a sensor-side / global-purity event; it does not perturb the carrier directly.

- **P5_alarm_fires_before_A_share_basin_commit_boundary**
  Alarm at A_side = 1/24 is recorded earlier than A_leak reaching A_share = 1/12. The protected route is still recoverable at alarm time.

- **P6_no_alarm_in_no_decoherence_control**
  With T1 = infinity and T2 = infinity (Lindblad operators removed), A_leak stays at 0 throughout the window. No alarm fires.

- **P7_alarm_is_monotonic_in_A_leak**
  At any sample where A_leak < 1/24, no alarm is recorded. At the first sample where A_leak >= 1/24, alarm fires. Alarm does not double-fire on subsequent samples.

- **P8_protocol_completes_end_to_end**
  Full sequence runs: initialize -> load -> open_window_with_monitor -> alarm_emission -> delayed_read. No runtime error. Typed result object emitted.

## Wrong controls (frozen before runner execution)

- **WC1_zero_decoherence_gives_zero_alarms**
  Same as P6 from the wrong-control side. With no Lindblad operators, purity stays at 1.0 to numerical precision, A_leak stays at 0, alarm count = 0. Confirms no false positives.

- **WC2_alarm_fires_after_threshold_cross_not_before**
  At every sample where the alarm flag is True, the recorded A_leak at that sample is >= A_side. At every sample where alarm is False, A_leak < A_side (or the alarm has already fired on a previous sample). Confirms no premature alarms.

- **WC3_alarm_timestamp_matches_independent_purity_measurement**
  Independently compute (without using the alarm monitor) the first time at which 1 - purity >= 1/24 in the recorded trajectory. Compare to the alarm timestamp. They must match to within one sample.

- **WC4_alarm_magnitude_monotonic_in_actual_decoherence**
  Across multiple runs with different T2 values, the recorded A_leak at alarm time is approximately equal across runs (just above 1/24 in each case). The variability is the *time* of alarm, not the *threshold* value. Confirms threshold mechanics.

- **WC5_runner_does_not_modify_upstream_locks**
  No upstream CR lock (CR060a, CR061a, CR065a, CR066a, CR067a) is modified during runner execution.

- **WC6_no_free_parameters_introduced**
  All NV physical constants traced to published literature with `[VERIFY_PRECOMMIT]` tags. All SAM thresholds traced to A0-a_h-D foundation. No tuned parameter inside CR068a.

## Outputs (committed before runner execution)

```text
CR068a_warning_simulator_lock.json       - locked parameters and threshold
CR068a_runner.py                         - the runner (paul_revere_warning_only_v1.py)
CR068a_results.csv                       - row per time sample with A_leak and alarm flag
CR068a_summary.json                      - pass/fail per prediction and wrong control
CR068a_evolution_plot.png                - A_leak vs time with threshold and alarm event marked
CR068a_result.md                         - human-readable result
HASHES.txt                               - sha256 of all CR068a artifacts
```

## Falsifiers

This CR could falsify if:

1. Alarm fails to fire within the window at room-temperature parameters (P1) — leak rate is too slow or threshold is wrong.
2. Alarm fires in the no-decoherence control (P6 / WC1) — false-positive bug in the monitor.
3. Alarm timing doesn't match independent purity measurement (WC3) — monitor logic doesn't actually track the observable it claims to.
4. Alarm magnitude varies wildly across T2 values at the same threshold (WC4) — threshold semantics inconsistent.
5. Carrier population shows a jump at alarm emission (P4) — monitor is somehow perturbing the carrier.

Any falsification triggers a runner pause and a BOUNDARY verdict pending structural diagnosis.

## Free parameters

```text
free_parameters = 0
```

## Scope boundary

CR068a IS:
- A classical software simulation of the warning layer only
- Foundation underneath CR067a's self-correction loop
- Standalone deliverable: a working alarm system for quantum-state compromise

CR068a IS NOT:
- A self-correction protocol (that is CR067a)
- A hardware demonstration (that requires partner-lab Stage 4)
- A claim that any specific alarm threshold is empirically optimal (the threshold is structurally given by SAM page-one `A_side = 1/24`)

## Reproduction-on-demand

```bash
cd 12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR068a_PAUL_REVERE_WARNING_ONLY_V1/
pip install -r requirements.txt
python paul_revere_warning_only_v1.py
```

Deterministic. Re-runs must produce byte-identical output.

## Pre-execution seal

PRECOMMIT.md is hash-sealed before runner execution. Any modification to predictions, wrong controls, or scope after runner output requires a new CR (CR068b or CR069a) with explicit reason for change.
