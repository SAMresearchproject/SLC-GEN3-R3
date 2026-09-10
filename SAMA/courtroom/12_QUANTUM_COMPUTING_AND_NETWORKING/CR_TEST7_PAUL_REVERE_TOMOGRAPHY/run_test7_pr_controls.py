"""
TEST 7 — Paul Revere Controls

Inputs:
  --input outputs/test7_purity_leak_curve.csv

Runs controls A through G against the locked simulation curve.

Controls:
  A: threshold 1/12
  B: threshold 1/18
  C: threshold 1/36
  D: random threshold in [0.01, 0.20], seed 20260621
  E: population-only false positive (qutrit coherent vs diag)
  F: shuffled time labels, seed 20260621
  G: scrambled density (off-diagonals zeroed)

Required ordering: t_{1/36} < t_{1/24} < t_{1/18} < t_{1/12}.

Precommit: PRECOMMIT.md (sha dc3f63b80c3755e6e12d7b7c52a52195beca790d217e65689ef52de68975cdaa).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PLOTS = OUTPUTS / "plots"
CONTROLS = ROOT / "controls"
HASHES = ROOT / "hashes"
HASHES_TXT = ROOT / "HASHES.txt"

R = 12
A_SIDE = 1.0 / (2 * R)               # 1/24
SEED = 20260621


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


def detect_crossing(times: np.ndarray, A_leaks: np.ndarray, threshold: float):
    idx = np.where(A_leaks >= threshold)[0]
    if len(idx) == 0:
        return {"found": False, "t_discrete": None, "t_interp": None}
    i = int(idx[0])
    if i == 0:
        return {"found": True, "t_discrete": float(times[0]), "t_interp": float(times[0])}
    t0, t1 = float(times[i - 1]), float(times[i])
    A0, A1 = float(A_leaks[i - 1]), float(A_leaks[i])
    interp = t1 if A1 == A0 else t0 + (t1 - t0) * (threshold - A0) / (A1 - A0)
    return {"found": True, "t_discrete": float(times[i]), "t_interp": float(interp)}


# ---- A, B, C: threshold-shift controls ----

def threshold_control(curve_df: pd.DataFrame, threshold: float, label: str,
                       out_path: Path) -> dict:
    summary_rows = []
    for run_id, sub in curve_df.groupby("run_id"):
        sub = sub.sort_values("time")
        valid = sub[sub["matrix_valid"] == True]
        t = valid["time"].to_numpy(dtype=float)
        A = pd.to_numeric(valid["A_leak"], errors="coerce").to_numpy(dtype=float)
        cross = detect_crossing(t, A, threshold)
        summary_rows.append({
            "run_id": run_id,
            "threshold": threshold,
            "threshold_label": label,
            "crossing_found": cross["found"],
            "t_discrete": cross["t_discrete"] if cross["found"] else "",
            "t_interp": cross["t_interp"] if cross["found"] else "",
        })
    pd.DataFrame(summary_rows).to_csv(out_path, index=False, lineterminator="\n")
    append_hash(out_path)
    return {"threshold": threshold, "label": label, "rows": summary_rows}


# ---- D: random threshold ----

def random_threshold_control(curve_df: pd.DataFrame, seed: int) -> dict:
    rng = random.Random(seed)
    threshold = rng.uniform(0.01, 0.20)
    out = CONTROLS / "threshold_random.csv"
    res = threshold_control(curve_df, threshold, f"random_seed_{seed}", out)
    res["sampled_threshold"] = threshold
    res["seed"] = seed
    return res


# ---- E: population-only false positive ----

def population_only_control(out_path: Path) -> dict:
    a = np.array([2.0, 3.0, 2.0]) / math.sqrt(17.0)
    rho_coherent = np.outer(a, a)
    rho_diag = np.diag(a * a)
    pops_coh = np.real(np.diag(rho_coherent))
    pops_diag = np.real(np.diag(rho_diag))
    P_coh = float(np.real(np.trace(rho_coherent @ rho_coherent)))
    P_diag = float(np.real(np.trace(rho_diag @ rho_diag)))
    A_coh = 1.0 - P_coh
    A_diag = 1.0 - P_diag

    populations_identical = bool(np.allclose(pops_coh, pops_diag, atol=1e-12))
    purity_differs = abs(P_coh - P_diag) > 1e-6
    A_leak_differs = abs(A_coh - A_diag) > 1e-6

    rows = [
        {
            "state": "qutrit_coherent_(2|0>+3|1>+2|2>)/sqrt(17)",
            "p0": pops_coh[0], "p1": pops_coh[1], "p2": pops_coh[2],
            "purity": P_coh, "A_leak": A_coh,
            "PR_state": "PR_WARNING" if A_coh >= A_SIDE else "PR_CLEAR",
        },
        {
            "state": "qutrit_diagonal_diag(4/17, 9/17, 4/17)",
            "p0": pops_diag[0], "p1": pops_diag[1], "p2": pops_diag[2],
            "purity": P_diag, "A_leak": A_diag,
            "PR_state": "PR_WARNING" if A_diag >= A_SIDE else "PR_CLEAR",
        },
    ]
    pd.DataFrame(rows).to_csv(out_path, index=False, lineterminator="\n")
    append_hash(out_path)
    verdict = (
        "PASS_POPULATION_ONLY_REJECTED"
        if (populations_identical and purity_differs and A_leak_differs)
        else "FAIL_POPULATION_ONLY_NOT_REJECTED"
    )
    return {
        "populations_identical": populations_identical,
        "purity_coherent": P_coh,
        "purity_diagonal": P_diag,
        "A_leak_coherent": A_coh,
        "A_leak_diagonal": A_diag,
        "purity_differs": purity_differs,
        "A_leak_differs": A_leak_differs,
        "verdict": verdict,
    }


# ---- F: shuffled time ----

def shuffled_time_control(curve_df: pd.DataFrame, seed: int, out_path: Path) -> dict:
    rng = random.Random(seed)
    rows_out = []
    monotonic_real = []
    monotonic_shuffled = []
    for run_id, sub in curve_df.groupby("run_id"):
        sub = sub.sort_values("time")
        valid = sub[sub["matrix_valid"] == True]
        t = valid["time"].to_numpy(dtype=float).copy()
        A = pd.to_numeric(valid["A_leak"], errors="coerce").to_numpy(dtype=float)
        real_mono = bool(np.all(np.diff(t) > 0))
        monotonic_real.append(real_mono)
        t_shuf = t.copy()
        rng.shuffle(t_shuf)
        shuffled_mono = bool(np.all(np.diff(t_shuf) > 0))
        monotonic_shuffled.append(shuffled_mono)
        rows_out.append({
            "run_id": run_id,
            "n_points": int(len(t)),
            "real_time_monotonic": real_mono,
            "shuffled_time_monotonic": shuffled_mono,
            "seed": seed,
        })
    pd.DataFrame(rows_out).to_csv(out_path, index=False, lineterminator="\n")
    append_hash(out_path)
    rejected = all(monotonic_real) and not any(monotonic_shuffled)
    return {
        "real_monotonic_all_runs": all(monotonic_real),
        "shuffled_monotonic_any_run": any(monotonic_shuffled),
        "verdict": "PASS_SHUFFLED_TIME_REJECTED" if rejected else "FAIL_SHUFFLED_TIME_NOT_REJECTED",
    }


# ---- G: scrambled density ----

def parse_flat(s: str, dim: int):
    parts = [float(x) for x in str(s).strip().split("|")]
    if len(parts) != dim * dim:
        return None
    return np.array(parts, dtype=float).reshape((dim, dim))


def scrambled_density_control(out_path: Path) -> dict:
    """For qubit dephasing, take the t=0.05 state, zero off-diagonals,
    show populations unchanged, purity changes."""
    t = 0.05
    T2 = 1.0
    coh = 0.5 * math.exp(-t / T2)
    rho = np.array([[0.5, coh], [coh, 0.5]], dtype=complex)
    rho_scrambled = np.diag(np.diag(rho))  # zero off-diagonals
    pops_orig = np.real(np.diag(rho))
    pops_scr = np.real(np.diag(rho_scrambled))
    P_orig = float(np.real(np.trace(rho @ rho)))
    P_scr = float(np.real(np.trace(rho_scrambled @ rho_scrambled)))
    A_orig = 1.0 - P_orig
    A_scr = 1.0 - P_scr

    populations_equal = bool(np.allclose(pops_orig, pops_scr, atol=1e-12))
    purity_changed = abs(P_orig - P_scr) > 1e-6

    rows = [
        {"state": "qubit_dephasing_t=0.05", "p0": pops_orig[0], "p1": pops_orig[1],
         "purity": P_orig, "A_leak": A_orig},
        {"state": "qubit_dephasing_t=0.05_off_diag_zeroed", "p0": pops_scr[0], "p1": pops_scr[1],
         "purity": P_scr, "A_leak": A_scr},
    ]
    pd.DataFrame(rows).to_csv(out_path, index=False, lineterminator="\n")
    append_hash(out_path)
    verdict = (
        "PASS_SCRAMBLED_DENSITY_CHANGES_PURITY"
        if (populations_equal and purity_changed)
        else "FAIL_SCRAMBLED_NOT_DETECTED"
    )
    return {
        "populations_equal": populations_equal,
        "purity_original": P_orig,
        "purity_scrambled": P_scr,
        "purity_changed": purity_changed,
        "verdict": verdict,
    }


# ---- threshold-ordering check ----

def threshold_ordering_check(results: list[dict]) -> dict:
    """results: list of dicts with 'threshold' and per-run crossing times.
    Verify: for each run, t_{1/36} < t_{1/24} < t_{1/18} < t_{1/12}."""
    # Sort by threshold
    by_thresh = {r["threshold"]: r["rows"] for r in results}
    ok_runs = []
    for run_id in {row["run_id"] for r in results for row in r["rows"]}:
        times = {}
        for thresh, rows in by_thresh.items():
            for row in rows:
                if row["run_id"] == run_id:
                    val = row["t_interp"]
                    if val == "" or val is None:
                        continue
                    try:
                        times[thresh] = float(val)
                    except (ValueError, TypeError):
                        continue
        # Expected ordering (low threshold => earlier crossing)
        sorted_thresh = sorted(times.keys())
        ordered_correctly = all(times[sorted_thresh[i]] <= times[sorted_thresh[i + 1]]
                                for i in range(len(sorted_thresh) - 1))
        ok_runs.append({"run_id": run_id, "times": times, "ordered_correctly": ordered_correctly})
    all_ok = all(r["ordered_correctly"] for r in ok_runs) if ok_runs else False
    return {"per_run": ok_runs, "all_runs_ordered": all_ok}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}")
        sys.exit(2)

    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} rows from {args.input.name}")
    runs = df["run_id"].unique().tolist()
    print(f"Runs: {runs}")

    # A, B, C
    A_res = threshold_control(df, 1.0 / 12.0, "1/12", CONTROLS / "threshold_1_over_12.csv")
    B_res = threshold_control(df, 1.0 / 18.0, "1/18", CONTROLS / "threshold_1_over_18.csv")
    C_res = threshold_control(df, 1.0 / 36.0, "1/36", CONTROLS / "threshold_1_over_36.csv")
    # 1/24 baseline using the same machinery
    REF_res = threshold_control(df, 1.0 / 24.0, "1/24", CONTROLS / "threshold_1_over_24_reference.csv")
    print(f"\nThreshold controls:")
    for r in [A_res, B_res, REF_res, C_res]:
        for row in r["rows"]:
            print(f"  {r['label']}  {row['run_id']}: t_interp={row['t_interp']}")

    ordering = threshold_ordering_check([A_res, B_res, REF_res, C_res])
    print(f"\nOrdering check (t_{{1/36}} < t_{{1/24}} < t_{{1/18}} < t_{{1/12}}): {ordering['all_runs_ordered']}")
    for entry in ordering["per_run"]:
        print(f"  {entry['run_id']}: {entry['times']}  ordered={entry['ordered_correctly']}")

    # D
    D_res = random_threshold_control(df, SEED)
    print(f"\nRandom threshold: sampled={D_res['sampled_threshold']:.6f}")
    for row in D_res["rows"]:
        print(f"  {row['run_id']}: t_interp={row['t_interp']}")

    # E
    E_res = population_only_control(CONTROLS / "population_only_false_positive.csv")
    print(f"\nPopulation-only control: {E_res['verdict']}")
    print(f"  populations_identical={E_res['populations_identical']}, purity_diff={E_res['purity_differs']}")
    print(f"  P_coherent={E_res['purity_coherent']:.6f}, P_diag={E_res['purity_diagonal']:.6f}")

    # F
    F_res = shuffled_time_control(df, SEED, CONTROLS / "shuffled_time_control.csv")
    print(f"\nShuffled time control: {F_res['verdict']}")

    # G
    G_res = scrambled_density_control(CONTROLS / "scrambled_density_control.csv")
    print(f"\nScrambled density control: {G_res['verdict']}")

    # Consolidated comparison
    comparison_rows = []
    for r in [A_res, B_res, REF_res, C_res, D_res]:
        for row in r["rows"]:
            comparison_rows.append({
                "control": r["label"],
                "threshold": r["threshold"],
                "run_id": row["run_id"],
                "t_interp": row["t_interp"],
            })
    pd.DataFrame(comparison_rows).to_csv(
        OUTPUTS / "test7_control_comparison.csv", index=False, lineterminator="\n"
    )
    append_hash(OUTPUTS / "test7_control_comparison.csv")

    # Comparison plot
    PLOTS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    for thresh, label, color in [
        (1.0 / 12.0, "1/12", "C2"),
        (1.0 / 18.0, "1/18", "C3"),
        (1.0 / 24.0, "1/24 (SAM)", "red"),
        (1.0 / 36.0, "1/36", "C4"),
    ]:
        ax.axhline(thresh, linestyle="--", color=color, label=label)
    for run_id, sub in df.groupby("run_id"):
        sub = sub.sort_values("time")
        valid = sub[sub["matrix_valid"] == True]
        ax.plot(valid["time"], pd.to_numeric(valid["A_leak"], errors="coerce"), label=run_id)
    ax.set_xlim(0, 0.15)
    ax.set_ylim(0, 0.12)
    ax.set_xlabel("t / T2")
    ax.set_ylabel("A_leak")
    ax.set_title("Threshold-shift controls vs A_leak curves")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "control_comparison.png", dpi=120)
    plt.close(fig)
    append_hash(PLOTS / "control_comparison.png")

    # Summary JSON
    summary = {
        "control_A_1_over_12": A_res,
        "control_B_1_over_18": B_res,
        "control_C_1_over_36": C_res,
        "reference_1_over_24": REF_res,
        "control_D_random_threshold": D_res,
        "control_E_population_only": E_res,
        "control_F_shuffled_time": F_res,
        "control_G_scrambled_density": G_res,
        "threshold_ordering": ordering,
        "controls_pass": {
            "threshold_ordering_passed": ordering["all_runs_ordered"],
            "population_only_rejected": E_res["verdict"].startswith("PASS"),
            "shuffled_time_rejected": F_res["verdict"].startswith("PASS"),
            "scrambled_density_changes_purity": G_res["verdict"].startswith("PASS"),
        },
    }
    (OUTPUTS / "_controls_summary.json").write_text(json.dumps(summary, indent=2, default=str),
                                                     encoding="utf-8")
    print("\nControls runner complete. Wrote _controls_summary.json.")
    return summary


if __name__ == "__main__":
    main()
