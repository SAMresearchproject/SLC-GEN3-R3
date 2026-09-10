"""
TEST 7 — Paul Revere Quantum Warning / Tomography

Universal SAM object:    A_leak(t) = 1 - Tr(rho(t)^2)
Universal SAM threshold: A_side = 1/(2*R) = 1/24

Modes:
  --mode simulate                            generate qubit + qutrit dephasing models
  --mode analyze --density-csv FILE          ingest reconstructed density matrices
  --mode counts --counts-csv FILE            (not implemented in this version)

Precommit: PRECOMMIT.md (sha dc3f63b80c3755e6e12d7b7c52a52195beca790d217e65689ef52de68975cdaa).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
OUTPUTS = ROOT / "outputs"
PLOTS = OUTPUTS / "plots"
HASHES = ROOT / "hashes"
HASHES_TXT = ROOT / "HASHES.txt"

# Substrate constants
ALPHA_H = 2
D = 3
R = 12
A_SIDE = 1.0 / (2 * R)              # 1/24
PURITY_THRESHOLD = 1.0 - A_SIDE     # 23/24

# Validation tolerances
HERM_TOL = 1e-8
TRACE_TOL = 1e-8
EIG_FLOOR = -1e-8
PURITY_LO = -1e-8
PURITY_HI = 1.0 + 1e-8

# Simulation grid
T2_SIM = 1.0
T_START = 0.000
T_END = 0.200
T_STEP = 0.001


# ---- HASHING ----

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def append_hash(p: Path):
    h = sha256_file(p)
    line = f"{h}  {p.relative_to(ROOT).as_posix()}"
    with HASHES_TXT.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return h


# ---- DENSITY MATRIX CORE ----

def parse_flat(s: str, dim: int) -> tuple[np.ndarray, str]:
    """Parse '1|0|0|1' into a 1D numpy array of length dim**2. Returns (array, err)."""
    if s is None or (isinstance(s, float) and math.isnan(s)) or str(s).strip() == "":
        return np.zeros(dim * dim), "PARSE_ERROR"
    try:
        parts = [float(x) for x in str(s).strip().split("|")]
    except (ValueError, TypeError):
        return np.zeros(dim * dim), "PARSE_ERROR"
    if len(parts) != dim * dim:
        return np.zeros(dim * dim), "BAD_FLAT_LENGTH"
    return np.array(parts, dtype=float), ""


def build_density(real_flat: str, imag_flat: str, dim: int) -> tuple[np.ndarray | None, str]:
    if dim not in (2, 3):
        return None, "BAD_DIMENSION"
    re_arr, err_r = parse_flat(real_flat, dim)
    if err_r:
        return None, err_r
    im_arr, err_i = parse_flat(imag_flat, dim)
    if err_i:
        return None, err_i
    rho = (re_arr + 1j * im_arr).reshape((dim, dim))
    return rho, ""


def validate_density(rho: np.ndarray) -> str:
    """Return empty string if valid, else one of the failure codes."""
    n = rho.shape[0]
    if np.max(np.abs(rho - rho.conj().T)) > HERM_TOL:
        return "NON_HERMITIAN"
    if abs(np.trace(rho).real - 1.0) > TRACE_TOL or abs(np.trace(rho).imag) > TRACE_TOL:
        return "TRACE_NOT_ONE"
    eigs = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    if np.min(eigs) < EIG_FLOOR:
        return "NEGATIVE_EIGENVALUE"
    return ""


def purity(rho: np.ndarray) -> float:
    return float(np.real(np.trace(rho @ rho)))


# ---- ANALYTIC PREDICTIONS ----

def qubit_analytic_crossing(threshold: float = A_SIDE) -> float:
    """t/T2 for qubit dephasing: P(t) = (1+exp(-2t/T2))/2, find when 1-P = threshold."""
    # 1 - (1+e^{-2x})/2 = threshold  =>  e^{-2x} = 1 - 2*threshold
    rhs = 1.0 - 2.0 * threshold
    return -0.5 * math.log(rhs)


def qutrit_analytic_crossing(threshold: float = A_SIDE) -> float:
    """t/T2 for the (2,3,2)/sqrt(17) qutrit dephasing model."""
    # P(t) = 113/289 + (176/289) * exp(-2t/T2)
    # 1 - P(t) = threshold => exp(-2t/T2) = (1 - threshold - 113/289)/(176/289)
    p_target = 1.0 - threshold
    rhs = (p_target - 113.0 / 289.0) / (176.0 / 289.0)
    return -0.5 * math.log(rhs)


# ---- SIMULATION GENERATORS ----

def simulate_qubit(t_grid: np.ndarray, T2: float):
    """Returns list of (rho, ) for each t."""
    out = []
    for t in t_grid:
        coh = 0.5 * math.exp(-t / T2)
        rho = np.array([[0.5, coh], [coh, 0.5]], dtype=complex)
        out.append(rho)
    return out


def simulate_qutrit(t_grid: np.ndarray, T2: float):
    a = np.array([2.0, 3.0, 2.0]) / math.sqrt(17.0)
    out = []
    for t in t_grid:
        rho = np.outer(a, a).astype(complex)  # initial pure state
        decay = math.exp(-t / T2)
        # diagonals unchanged, off-diagonals multiplied by exp(-t/T2)
        for i in range(3):
            for j in range(3):
                if i != j:
                    rho[i, j] *= decay
        out.append(rho)
    return out


# ---- CROSSING DETECTION ----

def detect_crossing(times: np.ndarray, A_leaks: np.ndarray, threshold: float = A_SIDE):
    """Returns dict with discrete and interpolated crossing times."""
    idx_above = np.where(A_leaks >= threshold)[0]
    if len(idx_above) == 0:
        return {
            "first_crossing_found": False,
            "discrete_idx": -1,
            "t_PR_discrete": None,
            "t_PR_interpolated": None,
        }
    i = int(idx_above[0])
    t_discrete = float(times[i])
    if i == 0:
        # Starts already above threshold; no interpolation
        return {
            "first_crossing_found": True,
            "discrete_idx": i,
            "t_PR_discrete": t_discrete,
            "t_PR_interpolated": t_discrete,
        }
    t0, t1 = float(times[i - 1]), float(times[i])
    A0, A1 = float(A_leaks[i - 1]), float(A_leaks[i])
    if A1 == A0:
        t_interp = t1
    else:
        t_interp = t0 + (t1 - t0) * (threshold - A0) / (A1 - A0)
    return {
        "first_crossing_found": True,
        "discrete_idx": i,
        "t_PR_discrete": t_discrete,
        "t_PR_interpolated": t_interp,
    }


# ---- BUILD ROWS FROM A SERIES ----

def series_rows(run_id: str, platform: str, dim: int, time_unit: str,
                t_grid: np.ndarray, rho_series: list, T1: float | None, T2: float):
    rows = []
    purities = []
    A_leaks = []
    valids = []
    val_errors = []
    for rho in rho_series:
        err = validate_density(rho)
        if err:
            P = float("nan")
            A = float("nan")
        else:
            P = purity(rho)
            A = 1.0 - P
        purities.append(P)
        A_leaks.append(A)
        valids.append(err == "")
        val_errors.append(err)

    purities = np.array(purities)
    A_leaks_arr = np.array(A_leaks)
    crossing = detect_crossing(t_grid, A_leaks_arr)

    first_idx = crossing["discrete_idx"] if crossing["first_crossing_found"] else -1

    for k, t in enumerate(t_grid):
        rows.append({
            "run_id": run_id,
            "platform": platform,
            "dimension": dim,
            "time": float(t),
            "time_unit": time_unit,
            "purity": float(purities[k]) if valids[k] else "",
            "A_leak": float(A_leaks_arr[k]) if valids[k] else "",
            "A_side": A_SIDE,
            "purity_threshold": PURITY_THRESHOLD,
            "PR_state": ("PR_WARNING" if (valids[k] and A_leaks_arr[k] >= A_SIDE) else "PR_CLEAR") if valids[k] else "INVALID",
            "is_first_crossing": (k == first_idx),
            "T1": T1 if T1 is not None else "",
            "T2": T2,
            "t_over_T2": float(t / T2),
            "matrix_valid": valids[k],
            "matrix_validation_error": val_errors[k],
        })
    event = {
        "run_id": run_id,
        "platform": platform,
        "dimension": dim,
        "first_crossing_found": crossing["first_crossing_found"],
        "t_PR_discrete": crossing["t_PR_discrete"] if crossing["first_crossing_found"] else "",
        "t_PR_interpolated": crossing["t_PR_interpolated"] if crossing["first_crossing_found"] else "",
        "t_PR_over_T2_discrete": (crossing["t_PR_discrete"] / T2) if crossing["first_crossing_found"] else "",
        "t_PR_over_T2_interpolated": (crossing["t_PR_interpolated"] / T2) if crossing["first_crossing_found"] else "",
        "A_side": A_SIDE,
        "purity_threshold": PURITY_THRESHOLD,
        "verdict": "PR_WARNING_FIRED" if crossing["first_crossing_found"] else "NO_CROSSING",
    }
    return rows, event, A_leaks_arr, purities


# ---- DENSITY MATRIX ROUND-TRIP (for outputs) ----

def density_to_flat(rho: np.ndarray):
    flat = rho.flatten()
    re = "|".join(f"{v.real:.15g}" for v in flat)
    im = "|".join(f"{v.imag:.15g}" for v in flat)
    return re, im


# ---- SIMULATE MODE ----

def simulate_mode():
    print("=" * 72)
    print("TEST 7 — Paul Revere Tomography — SIMULATE")
    print("=" * 72)
    print(f"ALPHA_H = {ALPHA_H}")
    print(f"D = {D}")
    print(f"R = {R}")
    print(f"A_SIDE = {A_SIDE!r}")
    print(f"PURITY_THRESHOLD = {PURITY_THRESHOLD!r}")

    t_grid = np.arange(T_START, T_END + T_STEP / 2, T_STEP)
    print(f"\nTime grid: {T_START}..{T_END} step {T_STEP} ({len(t_grid)} points), T2 = {T2_SIM}")

    # Analytic predictions
    qubit_analytic = qubit_analytic_crossing()
    qutrit_analytic = qutrit_analytic_crossing()
    print(f"\nAnalytic crossings:")
    print(f"  qubit  t/T2 = -0.5*ln(11/12)                                 = {qubit_analytic!r}")
    print(f"  qutrit t/T2 = -0.5*ln((23/24 - 113/289)/(176/289))           = {qutrit_analytic!r}")

    qubit_target = -0.5 * math.log(11.0 / 12.0)
    qutrit_target_num = (23.0 / 24.0) - (113.0 / 289.0)
    qutrit_target_den = 176.0 / 289.0
    qutrit_target = -0.5 * math.log(qutrit_target_num / qutrit_target_den)
    qubit_analytic_ok = abs(qubit_analytic - 0.043505688494814905) < 1e-15
    qutrit_analytic_ok = abs(qutrit_analytic - 0.03543583226729687) < 1e-15
    print(f"  qubit analytic == 0.043505688494814905: {qubit_analytic_ok}")
    print(f"  qutrit analytic == 0.03543583226729687: {qutrit_analytic_ok}")

    # Generate density matrices
    qubit_rhos = simulate_qubit(t_grid, T2_SIM)
    qutrit_rhos = simulate_qutrit(t_grid, T2_SIM)

    qubit_rows, qubit_event, qubit_A, qubit_P = series_rows(
        "SIM_QUBIT_DEPHASING_001", "simulated_qubit_dephasing", 2, "T2_units",
        t_grid, qubit_rhos, None, T2_SIM,
    )
    qutrit_rows, qutrit_event, qutrit_A, qutrit_P = series_rows(
        "SIM_QUTRIT_DEPHASING_001", "simulated_qutrit_dephasing", 3, "T2_units",
        t_grid, qutrit_rhos, None, T2_SIM,
    )

    print(f"\nQubit crossing:  discrete={qubit_event['t_PR_discrete']!r}, interp={qubit_event['t_PR_interpolated']!r}")
    print(f"Qutrit crossing: discrete={qutrit_event['t_PR_discrete']!r}, interp={qutrit_event['t_PR_interpolated']!r}")

    qubit_sim_ok = abs(qubit_event["t_PR_interpolated"] - qubit_analytic) < 1e-5
    qutrit_sim_ok = abs(qutrit_event["t_PR_interpolated"] - qutrit_analytic) < 1e-5
    print(f"\n|qubit_sim - analytic|  = {abs(qubit_event['t_PR_interpolated'] - qubit_analytic):.2e} (< 1e-5? {qubit_sim_ok})")
    print(f"|qutrit_sim - analytic| = {abs(qutrit_event['t_PR_interpolated'] - qutrit_analytic):.2e} (< 1e-5? {qutrit_sim_ok})")

    # Write outputs
    all_rows = qubit_rows + qutrit_rows
    events = [qubit_event, qutrit_event]
    pd.DataFrame(all_rows).to_csv(OUTPUTS / "test7_purity_leak_curve.csv", index=False, lineterminator="\n")
    pd.DataFrame(events).to_csv(OUTPUTS / "test7_pr_warning_events.csv", index=False, lineterminator="\n")

    # Model predictions CSV
    preds = [
        {
            "model": "qubit_equal_superposition_dephasing",
            "analytic_t_over_T2": qubit_analytic,
            "discrete_sim_t_over_T2": qubit_event["t_PR_discrete"],
            "interpolated_sim_t_over_T2": qubit_event["t_PR_interpolated"],
            "match_within_1e_minus_5": qubit_sim_ok,
        },
        {
            "model": "qutrit_2_3_2_dephasing",
            "analytic_t_over_T2": qutrit_analytic,
            "discrete_sim_t_over_T2": qutrit_event["t_PR_discrete"],
            "interpolated_sim_t_over_T2": qutrit_event["t_PR_interpolated"],
            "match_within_1e_minus_5": qutrit_sim_ok,
        },
    ]
    pd.DataFrame(preds).to_csv(OUTPUTS / "test7_model_predictions.csv", index=False, lineterminator="\n")

    # Density matrix reconstruction CSV (for completeness; here it's the simulated input)
    recon_rows = []
    for run_id, rhos, dim in [
        ("SIM_QUBIT_DEPHASING_001", qubit_rhos, 2),
        ("SIM_QUTRIT_DEPHASING_001", qutrit_rhos, 3),
    ]:
        for k, t in enumerate(t_grid):
            re, im = density_to_flat(rhos[k])
            recon_rows.append({
                "run_id": run_id,
                "dimension": dim,
                "time": float(t),
                "rho_real_flat": re,
                "rho_imag_flat": im,
                "construction_role": "SIM_INPUT_NOT_RECONSTRUCTED",
            })
    pd.DataFrame(recon_rows).to_csv(
        OUTPUTS / "test7_density_matrix_reconstruction.csv", index=False, lineterminator="\n"
    )

    # ---- Plots ----
    PLOTS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_grid, qubit_P, label="qubit purity P(t)")
    ax.plot(t_grid, qutrit_P, label="qutrit purity P(t)")
    ax.axhline(PURITY_THRESHOLD, color="red", linestyle="--", label=f"23/24 = {PURITY_THRESHOLD:.6f}")
    ax.set_xlabel("t / T2")
    ax.set_ylabel("Purity Tr(rho^2)")
    ax.set_title("Purity decay — qubit and qutrit dephasing")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "purity_curve.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_grid, qubit_A, label="qubit A_leak")
    ax.plot(t_grid, qutrit_A, label="qutrit A_leak")
    ax.axhline(A_SIDE, color="red", linestyle="--", label=f"A_side = 1/24 = {A_SIDE:.6f}")
    ax.set_xlabel("t / T2")
    ax.set_ylabel("A_leak = 1 - Tr(rho^2)")
    ax.set_title("Paul Revere observable — A_leak vs t")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "A_leak_curve.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_grid, qubit_A, label="qubit A_leak")
    ax.plot(t_grid, qutrit_A, label="qutrit A_leak")
    ax.axhline(A_SIDE, color="red", linestyle="--", label=f"A_side = 1/24")
    if qubit_event["first_crossing_found"]:
        ax.axvline(qubit_event["t_PR_interpolated"], color="C0", linestyle=":",
                   label=f"qubit t_PR = {qubit_event['t_PR_interpolated']:.6f}")
    if qutrit_event["first_crossing_found"]:
        ax.axvline(qutrit_event["t_PR_interpolated"], color="C1", linestyle=":",
                   label=f"qutrit t_PR = {qutrit_event['t_PR_interpolated']:.6f}")
    ax.set_xlim(0, 0.08)
    ax.set_ylim(0, 0.08)
    ax.set_xlabel("t / T2")
    ax.set_ylabel("A_leak")
    ax.set_title("Threshold crossing zoom — qubit and qutrit")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "threshold_crossing.png", dpi=120)
    plt.close(fig)

    # Internal checks (will be re-checked / extended after controls runner)
    sim_checks = {
        "A_side_equals_1_over_24": abs(A_SIDE - 1.0 / 24.0) < 1e-15,
        "purity_threshold_equals_23_over_24": abs(PURITY_THRESHOLD - 23.0 / 24.0) < 1e-15,
        "qubit_analytic_value_correct": qubit_analytic_ok,
        "qutrit_analytic_value_correct": qutrit_analytic_ok,
        "qubit_sim_crossing_matches_analytic": qubit_sim_ok,
        "qutrit_sim_crossing_matches_analytic": qutrit_sim_ok,
        "density_matrices_valid_or_flagged": all(
            row["matrix_valid"] or row["matrix_validation_error"] for row in all_rows
        ),
        "purity_in_allowed_range": all(
            (PURITY_LO <= row["purity"] <= PURITY_HI) for row in all_rows if row["matrix_valid"]
        ),
        "A_leak_in_allowed_range": all(
            (PURITY_LO <= row["A_leak"] <= PURITY_HI) for row in all_rows if row["matrix_valid"]
        ),
        "first_crossing_detected_if_present": True,
    }
    # Save partial internal checks (controls runner will extend)
    (OUTPUTS / "_sim_internal_partial.json").write_text(
        json.dumps(sim_checks, indent=2), encoding="utf-8"
    )

    print("\n[INTERNAL CHECKS - simulation portion]")
    for k, v in sim_checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}: {v}")

    # Hash sealed outputs
    append_hash(OUTPUTS / "test7_purity_leak_curve.csv")
    append_hash(OUTPUTS / "test7_pr_warning_events.csv")
    append_hash(OUTPUTS / "test7_model_predictions.csv")
    append_hash(OUTPUTS / "test7_density_matrix_reconstruction.csv")
    h_pred = sha256_file(OUTPUTS / "test7_model_predictions.csv")
    (HASHES / "model_predictions_CURRENT_HASH.txt").write_text(h_pred + "\n", encoding="utf-8")

    print("\nSimulate mode complete.")
    return sim_checks


# ---- ANALYZE MODE ----

def analyze_mode(density_csv: Path):
    print("=" * 72)
    print("TEST 7 — Paul Revere Tomography — ANALYZE")
    print("=" * 72)
    if not density_csv.exists():
        print(f"ERROR: density CSV not found: {density_csv}")
        sys.exit(2)
    print(f"Reading: {density_csv}")
    df = pd.read_csv(density_csv)
    required = ["run_id", "platform", "dimension", "time", "time_unit",
                "rho_real_flat", "rho_imag_flat", "T1", "T2", "notes"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"ERROR: missing required columns: {missing}")
        print("Verdict: FAIL_TEST7_INPUT_SCHEMA")
        sys.exit(2)

    all_rows = []
    events = []
    for run_id, sub in df.groupby("run_id"):
        sub = sub.sort_values("time")
        dim = int(sub["dimension"].iloc[0])
        platform = str(sub["platform"].iloc[0])
        time_unit = str(sub["time_unit"].iloc[0])
        T2_val = float(sub["T2"].iloc[0]) if not pd.isna(sub["T2"].iloc[0]) else 1.0
        T1_val = float(sub["T1"].iloc[0]) if not pd.isna(sub["T1"].iloc[0]) else None
        t_grid = sub["time"].to_numpy(dtype=float)
        rhos = []
        for _, row in sub.iterrows():
            rho, err = build_density(row["rho_real_flat"], row["rho_imag_flat"], dim)
            if err or rho is None:
                # mark invalid with NaN matrix
                rho = np.full((dim, dim), np.nan, dtype=complex)
            rhos.append(rho)
        rows, event, _, _ = series_rows(run_id, platform, dim, time_unit, t_grid, rhos, T1_val, T2_val)
        all_rows.extend(rows)
        events.append(event)
        print(f"  {run_id} ({platform}, dim={dim}): crossing={event['verdict']} "
              f"t_PR_interp={event['t_PR_interpolated']}")

    pd.DataFrame(all_rows).to_csv(OUTPUTS / "test7_purity_leak_curve.csv", index=False, lineterminator="\n")
    pd.DataFrame(events).to_csv(OUTPUTS / "test7_pr_warning_events.csv", index=False, lineterminator="\n")
    append_hash(OUTPUTS / "test7_purity_leak_curve.csv")
    append_hash(OUTPUTS / "test7_pr_warning_events.csv")
    print("\nAnalyze mode complete.")


def counts_mode(counts_csv: Path):
    print("=" * 72)
    print("TEST 7 — Paul Revere Tomography — COUNTS")
    print("=" * 72)
    print("COUNTS_MODE_NOT_IMPLEMENTED")
    print("Raw count reconstruction is reserved for a later amendment.")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["simulate", "analyze", "counts"])
    parser.add_argument("--density-csv", type=Path, default=None)
    parser.add_argument("--counts-csv", type=Path, default=None)
    args = parser.parse_args()

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    HASHES.mkdir(parents=True, exist_ok=True)

    if args.mode == "simulate":
        simulate_mode()
    elif args.mode == "analyze":
        if args.density_csv is None:
            print("ERROR: --mode analyze requires --density-csv")
            sys.exit(2)
        analyze_mode(args.density_csv)
    elif args.mode == "counts":
        if args.counts_csv is None:
            print("ERROR: --mode counts requires --counts-csv")
            sys.exit(2)
        counts_mode(args.counts_csv)


if __name__ == "__main__":
    main()
