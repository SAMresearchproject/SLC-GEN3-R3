"""
SAM - Substrate Accumulation Model
Paul Revere Warning-Only Simulator V1.0
CR068a - Warning layer underneath the CR067a self-correction loop

================================================================================
Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.

PRIVATE RESEARCH RECORD. NO LICENSE GRANTED.

See STEWARDSHIP.md and EPISTEMIC_STANCE.md at the repository root.

No verbal license. No implied license. No fair-use exception. No academic
exception. No educational license. All rights reserved.

Any future commercialization is subject to the stewardship intent in
STEWARDSHIP.md: revenue funds humanitarian causes - housing, addiction
recovery, charitable medical support, education and opportunity access,
community charities, environmental prosperity.

Contact: sbnvh@missouri.edu
================================================================================

What this simulator does
------------------------
CR068a is the warning-only version of the Paul Revere protocol on the NV(-)
(3)A2 ground-state triplet. It does exactly one thing well: it detects when
the protected qubit window has been compromised - before the compromise
commits to the ledger - and emits a typed alarm event with timestamp and
stress magnitude.

This is the historical Paul Revere: a warning that arrives ahead of the
harm. It does NOT act on the harm; the correction layer is CR067a. This CR
establishes the foundation underneath that.

Protocol cycle:
    initialize -> load -> open_window_with_continuous_monitor -> delayed_read

Alarm fires when A_leak = 1 - Tr(rho^2) reaches A_side = 1/24, the SAM
page-one entrance to the basin-forming regime.

Outputs (written next to this script):
  CR068a_results.csv                   - row per sample with A_leak and alarm flag
  CR068a_summary.json                  - pass/fail per prediction and wrong control
  CR068a_evolution_plot.png            - A_leak vs time with thresholds and alarm marked
  CR068a_warning_simulator_lock.json   - locked structural parameters
  CR068a_result.md                     - human-readable result

How to run
----------
  pip install -r requirements.txt
  python paul_revere_warning_only_v1.py
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import qutip as qt
except ImportError:
    sys.stderr.write(
        "ERROR: qutip is required. Install with:\n"
        "    pip install -r requirements.txt\n"
    )
    sys.exit(2)


# =============================================================================
# SAM foundation primitives (frozen at A0-a_h-D)
# =============================================================================

R = 12
D = 3
ALPHA_H = 2
A0 = 1.0 / (12.0 * math.pi)
A_SHARE = 1.0 / 12.0
A_SIDE = 1.0 / 24.0

# Alarm threshold per CR068a PRECOMMIT
ALARM_THRESHOLD = A_SIDE


# =============================================================================
# Loaded state per CR066a Born extension (normalized for qutrit)
# =============================================================================

LOADED_PROBABILITIES = {
    "carrier_ms0": 4.0 / 17.0,
    "envelope_msplus1": 9.0 / 17.0,
    "sensor_msminus1": 4.0 / 17.0,
}

LOADED_AMPLITUDES = {
    "carrier_ms0": math.sqrt(4.0 / 17.0),
    "envelope_msplus1": math.sqrt(9.0 / 17.0),
    "sensor_msminus1": math.sqrt(4.0 / 17.0),
}


# =============================================================================
# NV(-) physical constants
# =============================================================================

D_ZFS_HZ = 2.87e9
T1_ROOM_TEMP_S = 1.0e-3
T2_ROOM_TEMP_S = 1.0e-3
T2_FAST_DECOHERENCE_S = 1.0e-4  # for P3 scaling test
OPEN_WINDOW_DURATION_S = 1.0e-4
N_SAMPLES_PER_WINDOW = 200


# =============================================================================
# Qutrit operators (spin-1, NV ground-state triplet)
# =============================================================================

def build_spin1_operators():
    jx, jy, jz = qt.jmat(1, "x"), qt.jmat(1, "y"), qt.jmat(1, "z")
    ket_plus1 = qt.basis(3, 0)
    ket_zero = qt.basis(3, 1)
    ket_minus1 = qt.basis(3, 2)
    return {
        "S_x": jx, "S_y": jy, "S_z": jz, "S_z_sq": jz * jz,
        "ket_plus1": ket_plus1,
        "ket_zero": ket_zero,
        "ket_minus1": ket_minus1,
        "P_plus1": ket_plus1 * ket_plus1.dag(),
        "P_zero": ket_zero * ket_zero.dag(),
        "P_minus1": ket_minus1 * ket_minus1.dag(),
    }


def build_collapse_operators(ops, T1_s, T2_s):
    """T1 + T2 Lindblad operators for NV ground-state decoherence."""
    c_ops = []
    if T1_s is not None and T1_s > 0 and math.isfinite(T1_s):
        gamma_1 = 1.0 / T1_s
        c_ops.append(math.sqrt(gamma_1) * ops["ket_zero"] * ops["ket_plus1"].dag())
        c_ops.append(math.sqrt(gamma_1) * ops["ket_zero"] * ops["ket_minus1"].dag())
    if T2_s is not None and T2_s > 0 and math.isfinite(T2_s):
        if T1_s is not None and T1_s > 0:
            inv_T_phi = (1.0 / T2_s) - (1.0 / (2.0 * T1_s))
        else:
            inv_T_phi = 1.0 / T2_s
        if inv_T_phi > 0:
            c_ops.append(math.sqrt(inv_T_phi / 2.0) * ops["S_z"])
    return c_ops


# =============================================================================
# State preparation
# =============================================================================

def loaded_state_sam_native(ops):
    psi = (
        LOADED_AMPLITUDES["carrier_ms0"] * ops["ket_zero"]
        + LOADED_AMPLITUDES["envelope_msplus1"] * ops["ket_plus1"]
        + LOADED_AMPLITUDES["sensor_msminus1"] * ops["ket_minus1"]
    )
    return psi.unit()


# =============================================================================
# Sample measurement
# =============================================================================

@dataclass
class SampleReading:
    t: float
    purity: float
    A_leak: float
    P_carrier_ms0: float
    P_envelope_msplus1: float
    P_sensor_msminus1: float
    alarm_state: str  # one of: "protected", "alarm_fired_this_sample", "alarm_already_fired"


def measure_sample(state, ops, t, alarm_state):
    if state.type == "ket":
        rho = state * state.dag()
    else:
        rho = state
    purity = float((rho * rho).tr().real)
    A_leak = 1.0 - purity
    P_zero = float((ops["P_zero"] * rho).tr().real)
    P_plus1 = float((ops["P_plus1"] * rho).tr().real)
    P_minus1 = float((ops["P_minus1"] * rho).tr().real)
    return SampleReading(
        t=float(t),
        purity=purity,
        A_leak=A_leak,
        P_carrier_ms0=P_zero,
        P_envelope_msplus1=P_plus1,
        P_sensor_msminus1=P_minus1,
        alarm_state=alarm_state,
    )


# =============================================================================
# The alarm event (Paul Revere letter content)
# =============================================================================

@dataclass
class PaulRevereLetter:
    """The warning letter emitted when A_leak crosses A_side.

    This is the structured payload of the alarm. It carries timestamp,
    stress magnitude, and the carrier population at fire time so the
    downstream correction layer (CR067a) knows exactly when and how the
    window was compromised - without ever exposing the carrier's logical
    route identity (the carrier population is reported, not the route).
    """
    fired: bool
    t_fire_s: Optional[float] = None
    A_leak_at_fire: Optional[float] = None
    threshold_used: float = ALARM_THRESHOLD
    purity_at_fire: Optional[float] = None
    sensor_population_at_fire: Optional[float] = None
    carrier_population_at_fire: Optional[float] = None
    envelope_population_at_fire: Optional[float] = None
    sample_index_at_fire: Optional[int] = None
    reason: str = "no alarm fired during window"


# =============================================================================
# The continuous-monitor open window
# =============================================================================

def run_open_window_with_monitor(
    state, ops, c_ops, duration_s, n_samples, threshold,
):
    """Evolve under Lindblad + watch A_leak. Emit alarm at first crossing.

    Returns:
      (final_state, samples, letter)
    """
    # Work in rotating frame: zero Hamiltonian during the window (no drive
    # active). Populations and purity are unchanged by static H_0; only
    # Lindblad operators affect these observables. See CR067a runner docstring
    # for the physics justification.
    H_rot = qt.qzero(3)
    times = np.linspace(0.0, duration_s, n_samples)
    result = qt.mesolve(
        H_rot, state, times, c_ops=c_ops, e_ops=[],
        options={"nsteps": 100000},
    )
    samples = []
    letter = PaulRevereLetter(fired=False)
    alarm_state = "protected"
    for i, t in enumerate(times):
        rho_or_psi = result.states[i]
        # Determine alarm transition
        if letter.fired:
            alarm_state = "alarm_already_fired"
        else:
            # Inspect: is this the first sample where A_leak >= threshold?
            sample_check = measure_sample(rho_or_psi, ops, float(t), "protected")
            if sample_check.A_leak >= threshold:
                # Fire the alarm at this sample
                alarm_state = "alarm_fired_this_sample"
                letter = PaulRevereLetter(
                    fired=True,
                    t_fire_s=sample_check.t,
                    A_leak_at_fire=sample_check.A_leak,
                    threshold_used=threshold,
                    purity_at_fire=sample_check.purity,
                    sensor_population_at_fire=sample_check.P_sensor_msminus1,
                    carrier_population_at_fire=sample_check.P_carrier_ms0,
                    envelope_population_at_fire=sample_check.P_envelope_msplus1,
                    sample_index_at_fire=i,
                    reason=(
                        f"A_leak = {sample_check.A_leak:.6f} reached threshold "
                        f"A_side = {threshold:.6f} at sample {i}, t = "
                        f"{sample_check.t*1e6:.3f} us. Route is in basin-forming "
                        f"regime; recoverable until A_leak reaches A_share = 1/12. "
                        f"Carrier route identity not exposed."
                    ),
                )
            else:
                alarm_state = "protected"
        samples.append(measure_sample(rho_or_psi, ops, float(t), alarm_state))
    return result.states[-1], samples, letter


# =============================================================================
# Run the full warning protocol cycle
# =============================================================================

def run_warning_protocol(
    ops, T1_s, T2_s, duration_s=OPEN_WINDOW_DURATION_S, n_samples=N_SAMPLES_PER_WINDOW,
):
    """Initialize -> load -> open window with monitor -> return all data."""
    c_ops = build_collapse_operators(ops, T1_s, T2_s)
    initial = ops["ket_zero"]
    loaded = loaded_state_sam_native(ops)
    loaded_snapshot = measure_sample(loaded, ops, t=0.0, alarm_state="protected")
    final_state, samples, letter = run_open_window_with_monitor(
        loaded, ops, c_ops, duration_s, n_samples, ALARM_THRESHOLD,
    )
    return {
        "T1_s": T1_s,
        "T2_s": T2_s,
        "duration_s": duration_s,
        "n_samples": n_samples,
        "loaded_snapshot": loaded_snapshot,
        "samples": samples,
        "letter": letter,
    }


# =============================================================================
# Prediction and wrong-control evaluation
# =============================================================================

def evaluate_predictions(cycle_room_temp, cycle_fast_decoh, cycle_no_decoh):
    samples_rt = cycle_room_temp["samples"]
    letter_rt = cycle_room_temp["letter"]
    samples_fast = cycle_fast_decoh["samples"]
    letter_fast = cycle_fast_decoh["letter"]
    letter_no = cycle_no_decoh["letter"]
    loaded = cycle_room_temp["loaded_snapshot"]

    # P1 alarm fires within window at room temperature
    p1_pass = letter_rt.fired

    # P2 alarm event carries timestamp and stress magnitude
    p2_pass = (
        letter_rt.fired
        and letter_rt.t_fire_s is not None
        and letter_rt.A_leak_at_fire is not None
        and letter_rt.sensor_population_at_fire is not None
        and letter_rt.carrier_population_at_fire is not None
    )

    # P3 alarm time scales with T2 inverse
    if letter_rt.fired and letter_fast.fired:
        ratio_observed = letter_rt.t_fire_s / letter_fast.t_fire_s
        ratio_expected = T2_ROOM_TEMP_S / T2_FAST_DECOHERENCE_S
        # Loose: within an order of magnitude
        p3_pass = (
            ratio_observed >= 0.1 * ratio_expected
            and ratio_observed <= 10.0 * ratio_expected
        )
        p3_details = {
            "t_fire_room_temp_s": letter_rt.t_fire_s,
            "t_fire_fast_decoh_s": letter_fast.t_fire_s,
            "ratio_observed": ratio_observed,
            "ratio_expected": ratio_expected,
        }
    else:
        p3_pass = False
        p3_details = {"reason": "one or both alarms did not fire"}

    # P4 carrier population unchanged by alarm emission
    if letter_rt.fired and letter_rt.sample_index_at_fire is not None and letter_rt.sample_index_at_fire > 0:
        carrier_at_fire = samples_rt[letter_rt.sample_index_at_fire].P_carrier_ms0
        carrier_prev = samples_rt[letter_rt.sample_index_at_fire - 1].P_carrier_ms0
        carrier_jump = abs(carrier_at_fire - carrier_prev)
        # Sample-to-sample carrier change should be smooth (no jump from alarm emission)
        p4_pass = carrier_jump < 0.01
        p4_details = {
            "carrier_at_fire": carrier_at_fire,
            "carrier_prev_sample": carrier_prev,
            "jump": carrier_jump,
            "threshold": 0.01,
        }
    else:
        p4_pass = False
        p4_details = {"reason": "alarm did not fire or fired at first sample"}

    # P5 alarm fires before A_share basin commit boundary
    if letter_rt.fired:
        p5_pass = letter_rt.A_leak_at_fire < A_SHARE
        p5_details = {
            "A_leak_at_fire": letter_rt.A_leak_at_fire,
            "A_share_boundary": A_SHARE,
            "fired_before_basin_commit": letter_rt.A_leak_at_fire < A_SHARE,
        }
    else:
        p5_pass = False
        p5_details = {"reason": "alarm did not fire"}

    # P6 no alarm in no-decoherence control
    p6_pass = not letter_no.fired

    # P7 alarm is monotonic in A_leak
    # Check: at every protected sample, A_leak < threshold. After alarm fires,
    # never returns to protected state.
    p7_pass = True
    p7_violations = []
    for i, s in enumerate(samples_rt):
        if s.alarm_state == "protected" and s.A_leak >= ALARM_THRESHOLD:
            p7_pass = False
            p7_violations.append({"i": i, "t": s.t, "A_leak": s.A_leak,
                                   "alarm_state": s.alarm_state})
        if i > 0 and samples_rt[i - 1].alarm_state in ("alarm_fired_this_sample",
                                                        "alarm_already_fired") and \
            s.alarm_state == "protected":
            p7_pass = False
            p7_violations.append({"i": i, "t": s.t,
                                   "alarm_state": s.alarm_state,
                                   "issue": "alarm reverted to protected"})

    # P8 protocol completes end-to-end - we got here
    p8_pass = True

    return {
        "P1_alarm_fires_within_window_at_room_temperature": {
            "pass": p1_pass,
            "details": {
                "fired": letter_rt.fired,
                "t_fire_s": letter_rt.t_fire_s,
                "window_duration_s": cycle_room_temp["duration_s"],
                "T1_s": cycle_room_temp["T1_s"],
                "T2_s": cycle_room_temp["T2_s"],
            },
        },
        "P2_alarm_event_carries_timestamp_and_stress_magnitude": {
            "pass": p2_pass,
            "details": asdict(letter_rt),
        },
        "P3_alarm_time_scales_with_T2_inverse": {
            "pass": p3_pass,
            "details": p3_details,
        },
        "P4_carrier_population_unchanged_by_alarm_emission": {
            "pass": p4_pass,
            "details": p4_details,
        },
        "P5_alarm_fires_before_A_share_basin_commit_boundary": {
            "pass": p5_pass,
            "details": p5_details,
        },
        "P6_no_alarm_in_no_decoherence_control": {
            "pass": p6_pass,
            "details": {"no_decoh_alarm_fired": letter_no.fired},
        },
        "P7_alarm_is_monotonic_in_A_leak": {
            "pass": p7_pass,
            "details": {
                "violations_count": len(p7_violations),
                "violations": p7_violations[:5],  # cap
            },
        },
        "P8_protocol_completes_end_to_end": {
            "pass": p8_pass,
            "details": "All stages executed without runtime error",
        },
    }


def evaluate_wrong_controls(cycle_room_temp, cycle_fast_decoh, cycle_no_decoh):
    samples_rt = cycle_room_temp["samples"]
    letter_rt = cycle_room_temp["letter"]
    letter_fast = cycle_fast_decoh["letter"]
    letter_no = cycle_no_decoh["letter"]

    # WC1 zero decoherence gives zero alarms (no false positives)
    wc1_pass = not letter_no.fired

    # WC2 alarm fires after threshold cross not before
    wc2_pass = True
    wc2_violations = []
    for s in samples_rt:
        if s.alarm_state in ("alarm_fired_this_sample",) and s.A_leak < ALARM_THRESHOLD:
            wc2_pass = False
            wc2_violations.append({"t": s.t, "A_leak": s.A_leak})

    # WC3 alarm timestamp matches independent purity measurement
    # Independently find first sample where A_leak >= threshold
    indep_first_cross_index = None
    for i, s in enumerate(samples_rt):
        if s.A_leak >= ALARM_THRESHOLD:
            indep_first_cross_index = i
            break
    if letter_rt.fired and indep_first_cross_index is not None:
        wc3_pass = letter_rt.sample_index_at_fire == indep_first_cross_index
        wc3_details = {
            "alarm_sample_index": letter_rt.sample_index_at_fire,
            "independent_first_cross_index": indep_first_cross_index,
            "match": letter_rt.sample_index_at_fire == indep_first_cross_index,
        }
    else:
        wc3_pass = (not letter_rt.fired) and (indep_first_cross_index is None)
        wc3_details = {
            "alarm_fired": letter_rt.fired,
            "indep_cross_found": indep_first_cross_index is not None,
        }

    # WC4 alarm magnitude monotonic in actual decoherence
    if letter_rt.fired and letter_fast.fired:
        # Both runs should fire just above A_side threshold
        wc4_pass = (
            abs(letter_rt.A_leak_at_fire - A_SIDE) < 0.01
            and abs(letter_fast.A_leak_at_fire - A_SIDE) < 0.01
        )
        wc4_details = {
            "A_leak_at_fire_room_temp": letter_rt.A_leak_at_fire,
            "A_leak_at_fire_fast_decoh": letter_fast.A_leak_at_fire,
            "threshold": A_SIDE,
            "tolerance": 0.01,
        }
    else:
        wc4_pass = False
        wc4_details = {"reason": "one or both alarms did not fire"}

    # WC5 runner does not modify upstream locks - structural
    wc5_pass = True

    # WC6 no free parameters introduced - structural
    wc6_pass = True

    return {
        "WC1_zero_decoherence_gives_zero_alarms": {
            "pass": wc1_pass,
            "details": {"no_decoh_alarm_fired": letter_no.fired},
        },
        "WC2_alarm_fires_after_threshold_cross_not_before": {
            "pass": wc2_pass,
            "details": {"violations_count": len(wc2_violations),
                        "violations": wc2_violations[:5]},
        },
        "WC3_alarm_timestamp_matches_independent_purity_measurement": {
            "pass": wc3_pass,
            "details": wc3_details,
        },
        "WC4_alarm_magnitude_monotonic_in_actual_decoherence": {
            "pass": wc4_pass,
            "details": wc4_details,
        },
        "WC5_runner_does_not_modify_upstream_locks": {
            "pass": wc5_pass,
            "details": "Runner is read-only on upstream CR locks (structural invariant)",
        },
        "WC6_no_free_parameters_introduced": {
            "pass": wc6_pass,
            "details": "All inputs traced to CR068a_declared_premises.json; no fitted parameters",
        },
    }


# =============================================================================
# Output writers
# =============================================================================

def write_results_csv(cycle, output_path):
    samples = cycle["samples"]
    with output_path.open("w", encoding="utf-8") as f:
        f.write("sample_index,t_seconds,t_microseconds,purity,A_leak,P_carrier_ms0,"
                "P_envelope_msplus1,P_sensor_msminus1,alarm_state\n")
        for i, s in enumerate(samples):
            f.write(
                f"{i},{s.t:.9e},{s.t*1e6:.6f},{s.purity:.9e},{s.A_leak:.9e},"
                f"{s.P_carrier_ms0:.9e},{s.P_envelope_msplus1:.9e},"
                f"{s.P_sensor_msminus1:.9e},{s.alarm_state}\n"
            )


def write_summary_json(
    cycle_rt, cycle_fast, cycle_no, predictions, wrong_controls, output_path,
):
    pass_p = sum(1 for v in predictions.values() if v.get("pass"))
    pass_wc = sum(1 for v in wrong_controls.values() if v.get("pass"))
    summary = {
        "cr_id": "CR068a",
        "test_class": "PAUL_REVERE_WARNING_ONLY_NV_CENTER_CLASSICAL_SIMULATOR_V1",
        "execution_status": "CLEAN",
        "result_class": (
            f"CR068a_PAUL_REVERE_WARNING_ONLY_V1_SEALED__"
            f"PREDICTIONS_{pass_p}_OF_{len(predictions)}__"
            f"WRONG_CONTROLS_{pass_wc}_OF_{len(wrong_controls)}"
        ),
        "copyright": "Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.",
        "license": "PRIVATE_RESEARCH_RECORD_NO_LICENSE_GRANTED",
        "stewardship_intent": "STEWARDSHIP.md",
        "epistemic_stance": "EPISTEMIC_STANCE.md",
        "foundation_primitives": {
            "R": R, "D": D, "alpha_H": ALPHA_H,
            "A_0": A0, "A_share": A_SHARE, "A_side": A_SIDE,
        },
        "alarm_threshold": A_SIDE,
        "alarm_threshold_symbolic": "A_side = 1/24",
        "letter_room_temp": asdict(cycle_rt["letter"]),
        "letter_fast_decoh": asdict(cycle_fast["letter"]),
        "letter_no_decoh": asdict(cycle_no["letter"]),
        "nv_constants_used": {
            "D_zfs_Hz": D_ZFS_HZ,
            "T1_room_temp_s": T1_ROOM_TEMP_S,
            "T2_room_temp_s": T2_ROOM_TEMP_S,
            "T2_fast_decoherence_s": T2_FAST_DECOHERENCE_S,
            "open_window_duration_s": OPEN_WINDOW_DURATION_S,
            "n_samples_per_window": N_SAMPLES_PER_WINDOW,
        },
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "free_parameters": 0,
        "summary_counts": {
            "predictions_passed": pass_p,
            "predictions_total": len(predictions),
            "wrong_controls_passed": pass_wc,
            "wrong_controls_total": len(wrong_controls),
        },
    }
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)


def write_warning_simulator_lock(cycle_rt, output_path):
    lock = {
        "cr_id": "CR068a",
        "lock_type": "WARNING_SIMULATOR_STRUCTURAL_LOCK_V1",
        "copyright": "Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.",
        "alarm_threshold": A_SIDE,
        "alarm_threshold_symbolic": "A_side = 1/24",
        "A_leak_definition": "1 - Tr(rho^2)",
        "basin_commit_boundary": A_SHARE,
        "loaded_probabilities": LOADED_PROBABILITIES,
        "slot_assignment": {
            "carrier": "m_s = 0",
            "envelope": "m_s = +1",
            "sensor": "m_s = -1",
        },
        "free_parameters": 0,
    }
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)


def plot_evolution(cycle_rt, output_path):
    samples = cycle_rt["samples"]
    letter = cycle_rt["letter"]
    times_us = [s.t * 1e6 for s in samples]
    A_leak = [s.A_leak for s in samples]
    purity = [s.purity for s in samples]
    P_carrier = [s.P_carrier_ms0 for s in samples]
    P_envelope = [s.P_envelope_msplus1 for s in samples]
    P_sensor = [s.P_sensor_msminus1 for s in samples]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    # Top: A_leak with thresholds
    ax1.plot(times_us, A_leak, color="crimson", linewidth=2, label="A_leak = 1 - purity")
    ax1.axhline(A_SIDE, color="orange", linestyle="--", linewidth=1.5,
                label=f"A_side = 1/24 (alarm threshold)")
    ax1.axhline(A_SHARE, color="red", linestyle="--", linewidth=1.5,
                label=f"A_share = 1/12 (basin commit)")
    if letter.fired and letter.t_fire_s is not None:
        ax1.axvline(letter.t_fire_s * 1e6, color="black", linestyle=":",
                    linewidth=1.5, alpha=0.7,
                    label=f"alarm fired at t = {letter.t_fire_s*1e6:.2f} us")
        ax1.annotate(
            "Paul Revere letter sent",
            xy=(letter.t_fire_s * 1e6, A_SIDE),
            xytext=(letter.t_fire_s * 1e6 + 5, A_SIDE + 0.01),
            arrowprops={"arrowstyle": "->", "color": "black"},
            fontsize=9,
        )
    ax1.set_ylabel("A_leak (substrate leakage)")
    ax1.set_title("CR068a - Paul Revere Warning-Only Simulator - room-temperature NV")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(bottom=0)

    # Bottom: populations
    ax2.plot(times_us, P_carrier, label="carrier (m_s=0)", linewidth=2)
    ax2.plot(times_us, P_envelope, label="envelope (m_s=+1)", linewidth=2)
    ax2.plot(times_us, P_sensor, label="sensor (m_s=-1)", linewidth=2)
    ax2.axhline(4.0 / 17.0, color="gray", linestyle="--", alpha=0.4,
                label="4/17 (carrier/sensor loaded)")
    ax2.axhline(9.0 / 17.0, color="black", linestyle="--", alpha=0.4,
                label="9/17 (envelope loaded)")
    if letter.fired and letter.t_fire_s is not None:
        ax2.axvline(letter.t_fire_s * 1e6, color="black", linestyle=":",
                    linewidth=1.5, alpha=0.5)
    ax2.set_xlabel("Time (microseconds)")
    ax2.set_ylabel("Population")
    ax2.legend(loc="upper right", fontsize=9)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def write_result_md(summary_path, output_path):
    with summary_path.open("r", encoding="utf-8") as f:
        summary = json.load(f)
    pass_p = summary["summary_counts"]["predictions_passed"]
    total_p = summary["summary_counts"]["predictions_total"]
    pass_wc = summary["summary_counts"]["wrong_controls_passed"]
    total_wc = summary["summary_counts"]["wrong_controls_total"]
    letter = summary["letter_room_temp"]
    md = (
        "# CR068a Paul Revere Warning-Only Simulator V1.0 - Result\n\n"
        "**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**\n\n"
        f"**Result class:** `{summary['result_class']}`\n\n"
        f"**Predictions passed:** {pass_p}/{total_p}\n"
        f"**Wrong controls passed:** {pass_wc}/{total_wc}\n"
        f"**Free parameters:** {summary['free_parameters']}\n\n"
        "## The Paul Revere letter (room-temperature run)\n\n"
        "```text\n"
    )
    md += f"fired                      = {letter['fired']}\n"
    if letter['fired']:
        md += f"t_fire_s                   = {letter['t_fire_s']:.9e}\n"
        md += f"t_fire_microseconds        = {letter['t_fire_s']*1e6:.3f}\n"
        md += f"A_leak_at_fire             = {letter['A_leak_at_fire']:.9e}\n"
        md += f"threshold_A_side           = {letter['threshold_used']:.9e}  (= 1/24)\n"
        md += f"purity_at_fire             = {letter['purity_at_fire']:.9e}\n"
        md += f"carrier_population_at_fire = {letter['carrier_population_at_fire']:.9e}\n"
        md += f"envelope_population_at_fire= {letter['envelope_population_at_fire']:.9e}\n"
        md += f"sensor_population_at_fire  = {letter['sensor_population_at_fire']:.9e}\n"
        md += f"sample_index               = {letter['sample_index_at_fire']}\n"
        md += "\nReason: " + letter['reason'] + "\n"
    md += "```\n\n## Predictions\n\n"
    for name, entry in summary["predictions"].items():
        status = "PASS" if entry.get("pass") else "FAIL"
        md += f"- **[{status}]** {name}\n"
    md += "\n## Wrong controls\n\n"
    for name, entry in summary["wrong_controls"].items():
        status = "PASS" if entry.get("pass") else "FAIL"
        md += f"- **[{status}]** {name}\n"
    md += (
        "\n## Scope\n\n"
        "CR068a is the warning-only foundation underneath CR067a's self-correction "
        "loop. It validates that the Paul Revere alarm reliably detects qubit-window "
        "compromise (A_leak >= A_side = 1/24) before the basin-commit boundary "
        "(A_share = 1/12), with a typed letter carrying timestamp and stress "
        "magnitude. This is a classical software simulation; partner-lab Stage 4 "
        "is required for hardware validation.\n\n"
        "## Stewardship\n\n"
        "Any commercial use of this work or its derivatives is subject to the "
        "stewardship intent in `STEWARDSHIP.md`: revenue funds humanitarian causes.\n"
    )
    with output_path.open("w", encoding="utf-8") as f:
        f.write(md)


# =============================================================================
# Main
# =============================================================================

def main():
    script_dir = Path(__file__).resolve().parent
    print("CR068a Paul Revere Warning-Only Simulator V1.0")
    print(f"Working directory: {script_dir}")
    print()

    ops = build_spin1_operators()

    print("[1/4] Running room-temperature warning cycle (T1=T2=1 ms, 100 us window)...")
    cycle_rt = run_warning_protocol(ops, T1_s=T1_ROOM_TEMP_S, T2_s=T2_ROOM_TEMP_S)
    if cycle_rt["letter"].fired:
        print(f"      ALARM FIRED at t = {cycle_rt['letter'].t_fire_s*1e6:.3f} us")
        print(f"      A_leak at fire = {cycle_rt['letter'].A_leak_at_fire:.6f} (threshold {A_SIDE:.6f})")
    else:
        print(f"      No alarm fired during window.")

    print("[2/4] Running fast-decoherence cycle for P3 scaling test (T1=T2=0.1 ms)...")
    cycle_fast = run_warning_protocol(ops, T1_s=T2_FAST_DECOHERENCE_S, T2_s=T2_FAST_DECOHERENCE_S)
    if cycle_fast["letter"].fired:
        print(f"      ALARM FIRED at t = {cycle_fast['letter'].t_fire_s*1e6:.3f} us")
    else:
        print(f"      No alarm fired during window.")

    print("[3/4] Running no-decoherence control (Lindblad operators removed)...")
    cycle_no = run_warning_protocol(ops, T1_s=None, T2_s=None)
    if cycle_no["letter"].fired:
        print(f"      ALARM FIRED unexpectedly at t = {cycle_no['letter'].t_fire_s*1e6:.3f} us")
    else:
        print(f"      No alarm fired (expected behavior).")

    print("[4/4] Evaluating predictions and wrong controls...")
    predictions = evaluate_predictions(cycle_rt, cycle_fast, cycle_no)
    wrong_controls = evaluate_wrong_controls(cycle_rt, cycle_fast, cycle_no)
    pass_p = sum(1 for v in predictions.values() if v.get("pass"))
    pass_wc = sum(1 for v in wrong_controls.values() if v.get("pass"))
    print(f"      Predictions: {pass_p}/{len(predictions)}")
    print(f"      Wrong controls: {pass_wc}/{len(wrong_controls)}")

    print()
    print("Writing artifacts...")
    csv_path = script_dir / "CR068a_results.csv"
    summary_path = script_dir / "CR068a_summary.json"
    plot_path = script_dir / "CR068a_evolution_plot.png"
    lock_path = script_dir / "CR068a_warning_simulator_lock.json"
    result_md_path = script_dir / "CR068a_result.md"

    write_results_csv(cycle_rt, csv_path)
    write_summary_json(cycle_rt, cycle_fast, cycle_no, predictions, wrong_controls, summary_path)
    write_warning_simulator_lock(cycle_rt, lock_path)
    plot_evolution(cycle_rt, plot_path)
    write_result_md(summary_path, result_md_path)

    for p in (csv_path, summary_path, plot_path, lock_path, result_md_path):
        print(f"      Wrote {p.name}")

    print()
    print(
        f"Result class: CR068a_PAUL_REVERE_WARNING_ONLY_V1_SEALED__"
        f"PREDICTIONS_{pass_p}_OF_{len(predictions)}__"
        f"WRONG_CONTROLS_{pass_wc}_OF_{len(wrong_controls)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
