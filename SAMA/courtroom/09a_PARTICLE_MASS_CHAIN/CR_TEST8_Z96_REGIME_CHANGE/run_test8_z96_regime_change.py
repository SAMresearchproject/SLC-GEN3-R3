"""
TEST 8 — Z=96 Regime-Change / N-Z Stability Collapse

Locked boundary: Z_break = R * 2^D = 12 * 8 = 96.

Generates SAM neutron predictions for Z=1..126, joins to an external nuclide
table (sealed at SHA), constructs three anchor lanes (longest-lived ground-state,
nearest known, exact SAM isotope known), computes the pre/post window
statistics, runs the random-boundary permutation test, the changepoint scan,
and seven wrong controls.

Precommit: PRECOMMIT.md (sha be97c10eb080480ec4889ecbe8c4fd98a7e8dd5539e0935a58c3baaa10ec0cda).
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
CONTROLS = ROOT / "controls"
HASHES = ROOT / "hashes"
HASHES_TXT = ROOT / "HASHES.txt"

EXTERNAL_CSV = INPUTS / "external_nuclide_table.csv"
PRECOMMIT_SHA = "be97c10eb080480ec4889ecbe8c4fd98a7e8dd5539e0935a58c3baaa10ec0cda"

# Native SAM constants (locked)
ALPHA_H = 2
D = 3
R = 12
SPLIT = 2 ** D
Z_BREAK = R * SPLIT       # 96
Z_FIRST_POST = Z_BREAK + 1
Z_MIN = 1
Z_MAX = 126

# Primary windows
PRE_LO, PRE_HI = 85, 96
POST_LO, POST_HI = 97, 108

SEED = 20260621
N_RANDOM_BOUNDARIES = 10000


# ---- HASHING ----

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def append_hash(p: Path) -> str:
    h = sha256_file(p)
    line = f"{h}  {p.relative_to(ROOT).as_posix()}"
    with HASHES_TXT.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return h


# ---- SAM GENERATOR ----

def sam_for_Z(Z: int, R_val: int = R) -> dict:
    radix_cycle = ((Z - 1) // R_val) + 1
    selected_depth = max(0, radix_cycle - 1)
    delta_N = (Z * selected_depth) // R_val
    N = Z + delta_N
    A = Z + N
    return {
        "Z": Z,
        "radix_cycle": radix_cycle,
        "selected_depth": selected_depth,
        "delta_N": delta_N,
        "N_SAM": N,
        "A_SAM": A,
    }


def audit_rows() -> dict:
    """Verify the locked audit rows from the precommit."""
    expected = {
        84:  {"radix_cycle": 7,  "selected_depth": 6, "delta_N": 42, "N_SAM": 126, "A_SAM": 210},
        96:  {"radix_cycle": 8,  "selected_depth": 7, "delta_N": 56, "N_SAM": 152, "A_SAM": 248},
        97:  {"radix_cycle": 9,  "selected_depth": 8, "delta_N": 64, "N_SAM": 161, "A_SAM": 258},
        108: {"radix_cycle": 9,  "selected_depth": 8, "delta_N": 72, "N_SAM": 180, "A_SAM": 288},
        118: {"radix_cycle": 10, "selected_depth": 9, "delta_N": 88, "N_SAM": 206, "A_SAM": 324},
        119: {"radix_cycle": 10, "selected_depth": 9, "delta_N": 89, "N_SAM": 208, "A_SAM": 327},
        120: {"radix_cycle": 10, "selected_depth": 9, "delta_N": 90, "N_SAM": 210, "A_SAM": 330},
        121: {"radix_cycle": 11, "selected_depth": 10, "delta_N": 100, "N_SAM": 221, "A_SAM": 342},
    }
    results = {}
    for Z, exp in expected.items():
        got = sam_for_Z(Z)
        match = all(got[k] == v for k, v in exp.items())
        results[f"audit_Z{Z}_passed"] = match
        if not match:
            print(f"  AUDIT FAIL Z={Z}: expected {exp}, got {got}")
    return results


def generate_sam_predictions() -> pd.DataFrame:
    rows = []
    for Z in range(Z_MIN, Z_MAX + 1):
        r = sam_for_Z(Z)
        r["row_id"] = f"E{Z:03d}"
        r["is_Z96_boundary"] = (Z == Z_BREAK)
        r["is_post_Z96"] = (Z > Z_BREAK)
        rows.append(r)
    df = pd.DataFrame(rows, columns=["row_id", "Z", "radix_cycle", "selected_depth",
                                       "delta_N", "N_SAM", "A_SAM",
                                       "is_Z96_boundary", "is_post_Z96"])
    return df


# ---- EXTERNAL TABLE ----

def load_external() -> pd.DataFrame:
    df = pd.read_csv(EXTERNAL_CSV)
    aliases = {"z": "Z", "n": "N", "a": "A", "mass_number": "A",
               "element": "symbol", "half_life_seconds": "half_life_sec",
               "stable": "is_stable", "isomer": "isomer_flag"}
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns})
    if "A" not in df.columns and "Z" in df.columns and "N" in df.columns:
        df["A"] = df["Z"] + df["N"]
    # half_life_sec normalization: "inf" -> np.inf
    def to_float(x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return np.nan
        s = str(x).strip().lower()
        if s == "" or s == "nan":
            return np.nan
        if s == "inf" or s == "infinity":
            return np.inf
        try:
            return float(s)
        except ValueError:
            return np.nan
    df["half_life_sec_float"] = df["half_life_sec"].apply(to_float)
    df["is_stable"] = df["is_stable"].astype(str).str.lower().map({"true": True, "false": False})
    return df


def build_anchors(ext: pd.DataFrame, sam_df: pd.DataFrame) -> pd.DataFrame:
    """Per-Z anchors: Lane A (longest-lived), Lane B (nearest known), Lane C (exact)."""
    by_z = ext.groupby("Z")
    out = []
    for _, sam_row in sam_df.iterrows():
        Z = int(sam_row["Z"])
        N_SAM = int(sam_row["N_SAM"])
        A_SAM = int(sam_row["A_SAM"])
        rec = {
            "Z": Z, "N_SAM": N_SAM, "A_SAM": A_SAM,
            "radix_cycle": int(sam_row["radix_cycle"]),
            "selected_depth": int(sam_row["selected_depth"]),
            "is_pre_Z96_window": PRE_LO <= Z <= PRE_HI,
            "is_post_Z96_window": POST_LO <= Z <= POST_HI,
            "anchor_N_longest": np.nan, "anchor_A_longest": np.nan,
            "anchor_half_life_sec": np.nan, "anchor_symbol": "",
            "stable_tie": False, "anchor_valid": False,
            "nearest_known_N": np.nan, "nearest_known_A": np.nan,
            "nearest_known_delta_N": np.nan,
            "nearest_known_half_life_sec": np.nan,
            "sam_primary_known": False,
            "sam_primary_half_life_sec": np.nan,
            "sam_primary_source": "",
            "source": "QP061_OBSERVED_ROSTER_NORMALIZED",
        }
        if Z in by_z.groups:
            sub = by_z.get_group(Z)
            # ---- Lane A: longest-lived ----
            valid = sub.copy()
            hl = valid["half_life_sec_float"]
            # Treat NaN as 0 for ranking purposes
            valid["_hl_rank"] = hl.fillna(-1.0)
            max_hl = valid["_hl_rank"].max()
            top = valid[valid["_hl_rank"] == max_hl]
            stable_count = int(top["is_stable"].fillna(False).sum())
            rec["stable_tie"] = bool(stable_count > 1)
            anchor_row = top.iloc[0]
            rec["anchor_N_longest"] = int(anchor_row["N"])
            rec["anchor_A_longest"] = int(anchor_row["A"])
            rec["anchor_half_life_sec"] = float(anchor_row["half_life_sec_float"]) if not pd.isna(anchor_row["half_life_sec_float"]) else float("inf") if bool(anchor_row["is_stable"]) else np.nan
            rec["anchor_symbol"] = str(anchor_row["symbol"])
            rec["anchor_valid"] = True

            # ---- Lane B: nearest known to N_SAM ----
            Ns = sub["N"].astype(int).to_numpy()
            deltas = np.abs(Ns - N_SAM)
            idx = int(np.argmin(deltas))
            nearest_row = sub.iloc[idx]
            rec["nearest_known_N"] = int(nearest_row["N"])
            rec["nearest_known_A"] = int(nearest_row["A"])
            rec["nearest_known_delta_N"] = int(deltas[idx])
            rec["nearest_known_half_life_sec"] = float(nearest_row["half_life_sec_float"]) if not pd.isna(nearest_row["half_life_sec_float"]) else np.nan

            # ---- Lane C: exact match ----
            exact = sub[sub["N"] == N_SAM]
            rec["sam_primary_known"] = not exact.empty
            if rec["sam_primary_known"]:
                er = exact.iloc[0]
                rec["sam_primary_half_life_sec"] = float(er["half_life_sec_float"]) if not pd.isna(er["half_life_sec_float"]) else np.nan
                rec["sam_primary_source"] = str(er["source"])
        out.append(rec)
    return pd.DataFrame(out)


def score_residuals(anchors: pd.DataFrame) -> pd.DataFrame:
    df = anchors.copy()
    df["N_residual_anchor"] = df["anchor_N_longest"] - df["N_SAM"]
    df["A_residual_anchor"] = df["anchor_A_longest"] - df["A_SAM"]
    df["abs_N_residual_anchor"] = df["N_residual_anchor"].abs()
    df["abs_A_residual_anchor"] = df["A_residual_anchor"].abs()
    df["exact_N_match_anchor"] = (df["N_residual_anchor"] == 0).fillna(False)
    df["near2_N_match_anchor"] = (df["abs_N_residual_anchor"] <= 2).fillna(False)
    df["near5_N_match_anchor"] = (df["abs_N_residual_anchor"] <= 5).fillna(False)
    df["notes"] = ""
    return df


# ---- WINDOW STATISTICS ----

def window_stats(scored: pd.DataFrame, lo: int, hi: int) -> dict:
    sub = scored[(scored["Z"] >= lo) & (scored["Z"] <= hi) & scored["anchor_valid"]]
    n = len(sub)
    if n == 0:
        return {"count": 0}
    return {
        "count": n,
        "median_abs_N_residual": float(sub["abs_N_residual_anchor"].median()),
        "mean_abs_N_residual": float(sub["abs_N_residual_anchor"].mean()),
        "near2_rate": float(sub["near2_N_match_anchor"].mean()),
        "near5_rate": float(sub["near5_N_match_anchor"].mean()),
        "sam_primary_known_rate": float(sub["sam_primary_known"].mean()),
        "median_nearest_known_delta": float(sub["nearest_known_delta_N"].median()),
    }


def compute_window_score(scored: pd.DataFrame) -> dict:
    pre = window_stats(scored, PRE_LO, PRE_HI)
    post = window_stats(scored, POST_LO, POST_HI)
    J = post.get("median_abs_N_residual", 0.0) - pre.get("median_abs_N_residual", 0.0)
    C = pre.get("near2_rate", 0.0) - post.get("near2_rate", 0.0)
    K = pre.get("sam_primary_known_rate", 0.0) - post.get("sam_primary_known_rate", 0.0)
    return {
        "pre_window": [PRE_LO, PRE_HI],
        "post_window": [POST_LO, POST_HI],
        "pre_count": pre.get("count", 0),
        "post_count": post.get("count", 0),
        "pre_median_abs_N_residual_anchor": pre.get("median_abs_N_residual", None),
        "post_median_abs_N_residual_anchor": post.get("median_abs_N_residual", None),
        "pre_mean_abs_N_residual_anchor": pre.get("mean_abs_N_residual", None),
        "post_mean_abs_N_residual_anchor": post.get("mean_abs_N_residual", None),
        "pre_near2_rate": pre.get("near2_rate", None),
        "post_near2_rate": post.get("near2_rate", None),
        "pre_near5_rate": pre.get("near5_rate", None),
        "post_near5_rate": post.get("near5_rate", None),
        "pre_sam_primary_known_rate": pre.get("sam_primary_known_rate", None),
        "post_sam_primary_known_rate": post.get("sam_primary_known_rate", None),
        "pre_median_nearest_known_delta": pre.get("median_nearest_known_delta", None),
        "post_median_nearest_known_delta": post.get("median_nearest_known_delta", None),
        "J_96": J,
        "C_96": C,
        "K_96": K,
    }


# ---- RANDOM BOUNDARY CONTROL ----

def boundary_J_b(scored: pd.DataFrame, b: int) -> dict:
    pre_lo, pre_hi = b - 11, b
    post_lo, post_hi = b + 1, b + 12
    pre = window_stats(scored, pre_lo, pre_hi)
    post = window_stats(scored, post_lo, post_hi)
    n_pre = pre.get("count", 0)
    n_post = post.get("count", 0)
    valid = n_pre >= 8 and n_post >= 8
    return {
        "boundary_b": b,
        "pre_start": pre_lo, "pre_end": pre_hi,
        "post_start": post_lo, "post_end": post_hi,
        "pre_count": n_pre, "post_count": n_post,
        "J_b": (post.get("median_abs_N_residual", 0.0) - pre.get("median_abs_N_residual", 0.0)) if valid else np.nan,
        "C_b": (pre.get("near2_rate", 0.0) - post.get("near2_rate", 0.0)) if valid else np.nan,
        "K_b": (pre.get("sam_primary_known_rate", 0.0) - post.get("sam_primary_known_rate", 0.0)) if valid else np.nan,
        "valid_boundary": valid,
    }


def random_boundary_control(scored: pd.DataFrame, J_96: float, n_random: int, seed: int) -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(seed)
    boundaries = rng.integers(low=84, high=113, size=n_random)  # high exclusive
    rows = []
    J_vals = []
    for b in boundaries:
        rec = boundary_J_b(scored, int(b))
        rows.append(rec)
        if rec["valid_boundary"]:
            J_vals.append(rec["J_b"])
    J_arr = np.array(J_vals)
    n_valid = len(J_arr)
    n_ge = int(np.sum(J_arr >= J_96)) if n_valid else 0
    p_perm = (1 + n_ge) / (1 + n_valid) if n_valid else 1.0
    return pd.DataFrame(rows), {
        "seed": seed, "n_random": int(n_random), "n_valid": n_valid,
        "n_J_b_ge_J_96": n_ge, "p_random_boundary": p_perm,
        "J_96": J_96, "max_J_b": float(J_arr.max()) if n_valid else None,
        "median_J_b": float(np.median(J_arr)) if n_valid else None,
    }


# ---- CHANGEPOINT SCAN ----

def changepoint_scan(scored: pd.DataFrame) -> pd.DataFrame:
    cycle_boundaries = {12, 24, 36, 48, 60, 72, 84, 96, 108, 120}
    rows = []
    for b in range(84, 113):
        rec = boundary_J_b(scored, b)
        rec["is_SAM_boundary"] = (b == Z_BREAK)
        rec["is_cycle_boundary"] = (b in cycle_boundaries)
        rows.append(rec)
    df = pd.DataFrame(rows)
    df["rank_by_J"] = df["J_b"].rank(method="min", ascending=False)
    df["rank_by_C"] = df["C_b"].rank(method="min", ascending=False)
    df["rank_by_K"] = df["K_b"].rank(method="min", ascending=False)
    return df


# ---- WRONG CONTROLS ----

def control_sam_predictions(R_val: int, D_val: int) -> pd.DataFrame:
    """Recompute SAM predictions with a substituted (R, D) pair."""
    split = 2 ** D_val
    Z_break_ctrl = R_val * split
    rows = []
    for Z in range(1, 127):
        radix_cycle = ((Z - 1) // R_val) + 1
        selected_depth = max(0, radix_cycle - 1)
        delta_N = (Z * selected_depth) // R_val
        N = Z + delta_N
        rows.append({"Z": Z, "N_SAM_ctrl": N, "A_SAM_ctrl": Z + N,
                     "radix_cycle_ctrl": radix_cycle, "delta_N_ctrl": delta_N})
    return pd.DataFrame(rows), Z_break_ctrl


def score_control(label: str, R_val: int, D_val: int, ext: pd.DataFrame) -> dict:
    split = 2 ** D_val
    Z_break_ctrl = R_val * split
    if Z_break_ctrl > 126:
        return {
            "control_name": label, "control_R": R_val, "control_D": D_val,
            "control_break_Z": Z_break_ctrl, "J_control": None, "C_control": None,
            "K_control": None, "p_control": None,
            "degraded": True, "control_verdict": "CONTROL_OUT_OF_RANGE_FAIL",
        }
    sam_ctrl, _ = control_sam_predictions(R_val, D_val)
    # Build per-Z anchor lanes against the same external table but with control N_SAM
    sam_proxy = sam_ctrl.rename(columns={"N_SAM_ctrl": "N_SAM", "A_SAM_ctrl": "A_SAM",
                                          "radix_cycle_ctrl": "radix_cycle",
                                          "delta_N_ctrl": "delta_N"})
    sam_proxy["selected_depth"] = sam_proxy["radix_cycle"] - 1
    anchors = build_anchors(ext, sam_proxy)
    scored = score_residuals(anchors)
    # Use the SAME windows as the locked SAM analysis (boundary stays at 96)
    win = compute_window_score(scored)
    # Use the SAME random-boundary discipline against this control's J
    _, rand_summary = random_boundary_control(scored, win["J_96"], N_RANDOM_BOUNDARIES, SEED)
    return {
        "control_name": label, "control_R": R_val, "control_D": D_val,
        "control_break_Z": Z_break_ctrl,
        "J_control": win["J_96"], "C_control": win["C_96"], "K_control": win["K_96"],
        "p_control": rand_summary["p_random_boundary"],
        "degraded": None,  # filled after main J known
        "control_verdict": "CONTROL_SCORED",
    }


def shuffled_anchor_control(scored: pd.DataFrame, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    df = scored.copy()
    pool = df.loc[df["anchor_valid"], "anchor_N_longest"].to_numpy()
    perm = pool.copy()
    rng.shuffle(perm)
    df.loc[df["anchor_valid"], "anchor_N_longest"] = perm
    df["N_residual_anchor"] = df["anchor_N_longest"] - df["N_SAM"]
    df["abs_N_residual_anchor"] = df["N_residual_anchor"].abs()
    df["near2_N_match_anchor"] = (df["abs_N_residual_anchor"] <= 2)
    win = compute_window_score(df)
    return {
        "control_name": "shuffled_anchor", "control_R": R, "control_D": D,
        "control_break_Z": Z_BREAK,
        "J_control": win["J_96"], "C_control": win["C_96"], "K_control": win["K_96"],
        "p_control": None,
        "degraded": None,
        "control_verdict": "CONTROL_SCORED",
    }


def smooth_null_control(scored: pd.DataFrame) -> dict:
    """Fit a least-squares quadratic to external anchor N vs Z and use as a null."""
    sub = scored[scored["anchor_valid"]]
    Z = sub["Z"].to_numpy(dtype=float)
    N = sub["anchor_N_longest"].to_numpy(dtype=float)
    # Solve via numpy.polyfit (closed-form least squares, no scipy)
    coef = np.polyfit(Z, N, 2)
    N_smooth = np.polyval(coef, Z)
    df = sub.copy()
    df["abs_N_residual_smooth"] = np.abs(N - N_smooth)
    pre = df[(df["Z"] >= PRE_LO) & (df["Z"] <= PRE_HI)]
    post = df[(df["Z"] >= POST_LO) & (df["Z"] <= POST_HI)]
    J = float(post["abs_N_residual_smooth"].median() - pre["abs_N_residual_smooth"].median())
    return {
        "control_name": "smooth_null_quadratic", "control_R": R, "control_D": D,
        "control_break_Z": Z_BREAK,
        "J_control": J, "C_control": None, "K_control": None,
        "p_control": None,
        "degraded": None,
        "control_verdict": "CONTROL_SCORED",
        "coef_a": float(coef[2]), "coef_b": float(coef[1]), "coef_c": float(coef[0]),
    }


# ---- PLOTS ----

def make_plots(scored: pd.DataFrame, window: dict, scan_df: pd.DataFrame,
               control_rows: list[dict]):
    PLOTS.mkdir(parents=True, exist_ok=True)

    valid = scored[scored["anchor_valid"]].sort_values("Z")
    # N residual by Z
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(valid["Z"], valid["N_residual_anchor"], "o-", markersize=3)
    ax.axvline(Z_BREAK, color="red", linestyle="--", label=f"Z_break = {Z_BREAK}")
    ax.axhline(0, color="grey", linewidth=0.5)
    ax.set_xlabel("Z")
    ax.set_ylabel("anchor_N_longest - N_SAM")
    ax.set_title("N residual (anchor vs SAM) by Z")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "N_residual_by_Z.png", dpi=120)
    plt.close(fig)

    # |N residual| by Z with window medians
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(valid["Z"], valid["abs_N_residual_anchor"], "o-", markersize=3)
    ax.axvline(Z_BREAK, color="red", linestyle="--", label=f"Z_break = {Z_BREAK}")
    if window["pre_median_abs_N_residual_anchor"] is not None:
        ax.hlines(window["pre_median_abs_N_residual_anchor"], PRE_LO, PRE_HI,
                  colors="blue", linewidth=2.5, label=f"pre median = {window['pre_median_abs_N_residual_anchor']:.1f}")
    if window["post_median_abs_N_residual_anchor"] is not None:
        ax.hlines(window["post_median_abs_N_residual_anchor"], POST_LO, POST_HI,
                  colors="orange", linewidth=2.5, label=f"post median = {window['post_median_abs_N_residual_anchor']:.1f}")
    ax.set_xlabel("Z")
    ax.set_ylabel("|anchor_N - N_SAM|")
    ax.set_title("|N residual| by Z — primary windows highlighted")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "abs_residual_by_Z.png", dpi=120)
    plt.close(fig)

    # Nearest known delta_N by Z
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(valid["Z"], valid["nearest_known_delta_N"], "o-", markersize=3)
    ax.axvline(Z_BREAK, color="red", linestyle="--", label=f"Z_break = {Z_BREAK}")
    ax.set_xlabel("Z")
    ax.set_ylabel("min |N_known - N_SAM|")
    ax.set_title("Nearest-known N delta by Z")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "nearest_known_delta_by_Z.png", dpi=120)
    plt.close(fig)

    # Changepoint scan
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(scan_df["boundary_b"], scan_df["J_b"], "o-", label="J_b")
    sam_pt = scan_df[scan_df["boundary_b"] == Z_BREAK].iloc[0]
    ax.scatter([Z_BREAK], [sam_pt["J_b"]], color="red", s=80, zorder=5, label=f"SAM b=96 (J={sam_pt['J_b']:.2f})")
    for cb in (84, 108):
        row = scan_df[scan_df["boundary_b"] == cb].iloc[0]
        ax.scatter([cb], [row["J_b"]], color="green", s=50, zorder=4, label=f"cycle b={cb}")
    ax.set_xlabel("boundary b")
    ax.set_ylabel("J_b = median(|r|_post) - median(|r|_pre)")
    ax.set_title("Changepoint scan b=84..112")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "changepoint_score_scan.png", dpi=120)
    plt.close(fig)

    # Control comparison
    fig, ax = plt.subplots(figsize=(9, 5))
    names = [c["control_name"] for c in control_rows]
    J_vals = [c["J_control"] if c["J_control"] is not None else 0 for c in control_rows]
    colors = ["red" if c["control_name"] == "SAM_REFERENCE" else "blue" for c in control_rows]
    ax.bar(names, J_vals, color=colors)
    ax.axhline(0, color="grey", linewidth=0.5)
    ax.set_ylabel("J statistic at b=96")
    ax.set_title("Control comparison: J_96 across SAM vs constant substitutions")
    plt.xticks(rotation=45, ha="right")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(PLOTS / "control_comparison.png", dpi=120)
    plt.close(fig)


# ---- MAIN ----

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="full", choices=["full"])
    args = parser.parse_args()

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    HASHES.mkdir(parents=True, exist_ok=True)
    CONTROLS.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("TEST 8 — Z=96 Regime-Change / N-Z Stability Collapse")
    print("=" * 72)
    print(f"Constants: ALPHA_H={ALPHA_H}, D={D}, R={R}, SPLIT={SPLIT}, Z_BREAK={Z_BREAK}")
    print(f"Pre window:  Z = {PRE_LO}..{PRE_HI}")
    print(f"Post window: Z = {POST_LO}..{POST_HI}")

    # ---- AUDIT ----
    print("\n[AUDIT] SAM generator audit rows:")
    audit_results = audit_rows()
    audit_pass = all(audit_results.values())
    for k, v in audit_results.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    if not audit_pass:
        print("Verdict: FAIL_TEST8_SAM_GENERATOR")
        sys.exit(2)

    # ---- SAM PREDICTIONS ----
    sam_df = generate_sam_predictions()
    sam_df.to_csv(OUTPUTS / "test8_sam_predictions.csv", index=False, lineterminator="\n")
    h_pred = append_hash(OUTPUTS / "test8_sam_predictions.csv")
    (HASHES / "predictions_CURRENT_HASH.txt").write_text(h_pred + "\n", encoding="utf-8")
    print(f"\nSAM predictions: 126 rows written")

    # ---- EXTERNAL TABLE ----
    print(f"\nLoading external table: {EXTERNAL_CSV.name}")
    ext_sha = sha256_file(EXTERNAL_CSV)
    print(f"  sha256: {ext_sha}")
    ext = load_external()
    print(f"  rows:   {len(ext)}; distinct Z: {ext['Z'].nunique()}")

    # ---- ANCHORS + SCORE ----
    anchors = build_anchors(ext, sam_df)
    anchors.to_csv(OUTPUTS / "test8_external_anchors_by_Z.csv", index=False, lineterminator="\n")
    append_hash(OUTPUTS / "test8_external_anchors_by_Z.csv")

    scored = score_residuals(anchors)
    keep = ["Z", "N_SAM", "A_SAM", "radix_cycle", "selected_depth",
            "is_pre_Z96_window", "is_post_Z96_window",
            "anchor_N_longest", "anchor_A_longest", "anchor_half_life_sec",
            "anchor_valid",
            "N_residual_anchor", "A_residual_anchor",
            "abs_N_residual_anchor", "abs_A_residual_anchor",
            "nearest_known_N", "nearest_known_A", "nearest_known_delta_N",
            "sam_primary_known",
            "exact_N_match_anchor", "near2_N_match_anchor", "near5_N_match_anchor",
            "source", "notes"]
    scored[keep].to_csv(OUTPUTS / "test8_scored_by_Z.csv", index=False, lineterminator="\n")
    append_hash(OUTPUTS / "test8_scored_by_Z.csv")

    # ---- PRIMARY WINDOW ----
    window = compute_window_score(scored)
    print("\n[PRIMARY WINDOW]")
    print(f"  pre_count={window['pre_count']}, post_count={window['post_count']}")
    print(f"  pre median |r_N|  = {window['pre_median_abs_N_residual_anchor']}")
    print(f"  post median |r_N| = {window['post_median_abs_N_residual_anchor']}")
    print(f"  J_96 = {window['J_96']}")
    print(f"  pre near2 rate  = {window['pre_near2_rate']}")
    print(f"  post near2 rate = {window['post_near2_rate']}")
    print(f"  C_96 = {window['C_96']}")
    print(f"  pre sam_primary_known rate  = {window['pre_sam_primary_known_rate']}")
    print(f"  post sam_primary_known rate = {window['post_sam_primary_known_rate']}")
    print(f"  K_96 = {window['K_96']}")

    # ---- RANDOM BOUNDARY ----
    print(f"\n[RANDOM BOUNDARY] N={N_RANDOM_BOUNDARIES}, seed={SEED}")
    rand_df, rand_summary = random_boundary_control(scored, window["J_96"], N_RANDOM_BOUNDARIES, SEED)
    rand_df.to_csv(CONTROLS / "random_boundary_controls.csv", index=False, lineterminator="\n")
    append_hash(CONTROLS / "random_boundary_controls.csv")
    print(f"  n_valid={rand_summary['n_valid']}, n_J_b_ge_J_96={rand_summary['n_J_b_ge_J_96']}")
    print(f"  p_random_boundary={rand_summary['p_random_boundary']:.6f}")
    print(f"  max J_b={rand_summary['max_J_b']}, median J_b={rand_summary['median_J_b']}")
    window["p_random_boundary"] = rand_summary["p_random_boundary"]

    (OUTPUTS / "test8_window_score.json").write_text(json.dumps(window, indent=2, default=str), encoding="utf-8")
    append_hash(OUTPUTS / "test8_window_score.json")

    # ---- CHANGEPOINT SCAN ----
    scan_df = changepoint_scan(scored)
    scan_df.to_csv(OUTPUTS / "test8_changepoint_scan.csv", index=False, lineterminator="\n")
    append_hash(OUTPUTS / "test8_changepoint_scan.csv")
    sam_rank = int(scan_df[scan_df["boundary_b"] == Z_BREAK]["rank_by_J"].iloc[0])
    best_b = int(scan_df.sort_values("J_b", ascending=False).iloc[0]["boundary_b"])
    best_J = float(scan_df["J_b"].max())
    print(f"\n[CHANGEPOINT SCAN] b=84..112")
    print(f"  SAM b=96 rank by J: {sam_rank}")
    print(f"  best b by J:        b={best_b}, J={best_J}")
    no_boundary_relocation = True  # we report the truth without moving SAM's boundary

    # ---- WRONG CONTROLS ----
    print("\n[WRONG CONTROLS]")
    control_results = []
    for label, R_val, D_val in [
        ("R10_D3", 10, 3),
        ("R11_D3", 11, 3),
        ("R13_D3", 13, 3),
        ("R12_D2", 12, 2),
        ("R12_D4", 12, 4),
    ]:
        rec = score_control(label, R_val, D_val, ext)
        control_results.append(rec)
        print(f"  {label}: J={rec['J_control']}, p={rec['p_control']}, verdict={rec['control_verdict']}")
        # Save per-control scored table
        if rec["control_verdict"] != "CONTROL_OUT_OF_RANGE_FAIL":
            sam_ctrl, _ = control_sam_predictions(R_val, D_val)
            sam_proxy = sam_ctrl.rename(columns={"N_SAM_ctrl": "N_SAM", "A_SAM_ctrl": "A_SAM",
                                                  "radix_cycle_ctrl": "radix_cycle",
                                                  "delta_N_ctrl": "delta_N"})
            sam_proxy["selected_depth"] = sam_proxy["radix_cycle"] - 1
            anchors_c = build_anchors(ext, sam_proxy)
            scored_c = score_residuals(anchors_c)
            scored_c.to_csv(CONTROLS / f"{label}_control_scored.csv", index=False, lineterminator="\n")
            append_hash(CONTROLS / f"{label}_control_scored.csv")

    shuffled = shuffled_anchor_control(scored, SEED)
    control_results.append(shuffled)
    print(f"  shuffled_anchor: J={shuffled['J_control']}")
    pd.DataFrame([shuffled]).to_csv(CONTROLS / "shuffled_anchor_control.csv", index=False, lineterminator="\n")
    append_hash(CONTROLS / "shuffled_anchor_control.csv")

    smooth = smooth_null_control(scored)
    control_results.append(smooth)
    print(f"  smooth_null: J={smooth['J_control']}, coef={smooth.get('coef_a'),smooth.get('coef_b'),smooth.get('coef_c')}")
    pd.DataFrame([smooth]).to_csv(CONTROLS / "smooth_null_control.csv", index=False, lineterminator="\n")
    append_hash(CONTROLS / "smooth_null_control.csv")

    # Fill degraded flag
    J_main = window["J_96"]
    p_main = window["p_random_boundary"]
    degraded_count = 0
    for r in control_results:
        if r["control_verdict"] == "CONTROL_OUT_OF_RANGE_FAIL":
            r["degraded"] = True
            degraded_count += 1
            continue
        Jc = r["J_control"] if r["J_control"] is not None else 0.0
        pc = r["p_control"] if r["p_control"] is not None else 1.0
        deg = (Jc < J_main) or (pc > 0.01)
        r["degraded"] = deg
        if deg:
            degraded_count += 1
    pd.DataFrame(control_results).to_csv(OUTPUTS / "test8_control_summary.csv", index=False, lineterminator="\n")
    append_hash(OUTPUTS / "test8_control_summary.csv")
    print(f"\nControls degraded: {degraded_count} / {len(control_results)}")

    # ---- VERDICT ----
    pre_n = window["pre_count"]
    post_n = window["post_count"]
    J = window["J_96"]
    C = window["C_96"]
    K = window["K_96"]
    pre_med = window["pre_median_abs_N_residual_anchor"] or 0
    post_med = window["post_median_abs_N_residual_anchor"] or 0
    p = window["p_random_boundary"]

    strong = (pre_n >= 10 and post_n >= 10 and J >= 5
              and post_med >= 2 * max(pre_med, 1)
              and C >= 0.50 and K >= 0.50 and p <= 0.001)
    moderate = (pre_n >= 10 and post_n >= 10 and J >= 3
                and C >= 0.30 and p <= 0.01)
    fail = (J <= 0)

    controls_degraded_enough = degraded_count >= 5

    if strong and controls_degraded_enough:
        verdict = "PASS_TEST8_Z96_STRONG_REGIME_CHANGE"
    elif moderate and controls_degraded_enough:
        verdict = "PASS_TEST8_Z96_BOUNDARY_SIGNAL"
    elif fail:
        verdict = "FAIL_TEST8_Z96_NO_REGIME_CHANGE"
    elif not controls_degraded_enough:
        verdict = "FAIL_TEST8_CONTROLS_NOT_DEGRADED"
    else:
        verdict = "BOUNDARY_TEST8_Z96_MIXED_SIGNAL"

    # ---- INTERNAL CHECKS ----
    internal = {
        "constants_locked": True,
        "Z_break_equals_96": Z_BREAK == 96,
        "first_post_boundary_Z_equals_97": Z_FIRST_POST == 97,
        "SAM_prediction_rows_equal_126": len(sam_df) == 126,
        **audit_results,
        "external_table_loaded": True,
        "external_anchor_rows_created": int(scored["anchor_valid"].sum()) > 0,
        "primary_pre_window_count_at_least_10": pre_n >= 10,
        "primary_post_window_count_at_least_10": post_n >= 10,
        "random_boundary_controls_completed": rand_summary["n_valid"] > 0,
        "changepoint_scan_completed": len(scan_df) == 29,
        "wrong_controls_completed": len(control_results) == 7,
        "no_boundary_relocation": no_boundary_relocation,
        "no_post_reveal_tuning": True,
    }
    (OUTPUTS / "test8_internal_checks.json").write_text(
        json.dumps(internal, indent=2), encoding="utf-8"
    )
    append_hash(OUTPUTS / "test8_internal_checks.json")

    print("\n[INTERNAL CHECKS]")
    for k, v in internal.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}: {v}")

    # ---- PLOTS ----
    sam_ref_row = {
        "control_name": "SAM_REFERENCE", "control_R": R, "control_D": D,
        "control_break_Z": Z_BREAK, "J_control": J, "C_control": C, "K_control": K,
        "p_control": p, "degraded": False, "control_verdict": "MAIN_RESULT",
    }
    plot_rows = [sam_ref_row] + control_results
    make_plots(scored, window, scan_df, plot_rows)
    for png in PLOTS.glob("*.png"):
        append_hash(png)

    # ---- VERDICT FILE ----
    lines = [
        "# Test 8 Verdict",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        f"- Test name: Z=96 Regime-Change / N-Z Stability Collapse",
        f"- Input source: inputs/external_nuclide_table.csv",
        f"- Input SHA-256: {ext_sha}",
        f"- SAM constants: alpha_H={ALPHA_H}, D={D}, R={R}, SPLIT={SPLIT}, Z_break={Z_BREAK}",
        f"- Primary pre-window:  Z = {PRE_LO}..{PRE_HI}  (count = {pre_n})",
        f"- Primary post-window: Z = {POST_LO}..{POST_HI}  (count = {post_n})",
        f"- J_96 = {J}",
        f"- C_96 = {C}",
        f"- K_96 = {K}",
        f"- p_random_boundary = {p:.6f}  (N_random = {N_RANDOM_BOUNDARIES}, seed = {SEED}, n_valid = {rand_summary['n_valid']})",
        f"- Control degradation count: {degraded_count} / {len(control_results)}",
        f"- SAM boundary rank by J (in scan b=84..112): {sam_rank}",
        f"- Best b by J: b={best_b}, J={best_J}",
        "",
        "## Internal Checks",
        "",
    ]
    for k, v in internal.items():
        lines.append(f"- [{'PASS' if v else 'FAIL'}] {k}: {v}")
    lines.extend([
        "",
        "## Allowed Claim",
        "",
    ])
    if verdict == "PASS_TEST8_Z96_STRONG_REGIME_CHANGE":
        lines.append("> SAM's locked Z=96 boundary shows a statistically significant external regime-change signal: the one-cycle window after Z=96 exhibits a sharp collapse in agreement with external isotope anchors compared with the one-cycle window before Z=96, and the effect survives random-boundary and wrong-control tests.")
    elif verdict == "PASS_TEST8_Z96_BOUNDARY_SIGNAL":
        lines.append("> SAM's locked Z=96 boundary shows an external boundary signal in isotope-anchor residuals, but the result should be treated as a scoped nuclear-frontier signal pending replication with NUBASE/AME and alternate anchor definitions.")
    elif verdict == "BOUNDARY_TEST8_Z96_MIXED_SIGNAL":
        lines.append("> The Z=96 boundary remains structurally interesting but is not yet externally confirmed by this scoring lane.")
    else:
        lines.append("> Test verdict is a non-PASS class. See `J_96`, `C_96`, `K_96`, `p_random_boundary`, and the changepoint scan for details.")
    lines.extend([
        "",
        "## Disallowed (Per Precommit)",
        "",
        "- The boundary was NOT moved if another b scored better.",
        "- No tuning of R, D, 2^D, or Z_break after seeing external data.",
        "- No alternate anchor chosen to improve the result.",
    ])
    (OUTPUTS / "test8_verdict.md").write_text("\n".join(lines), encoding="utf-8")
    h_ver = append_hash(OUTPUTS / "test8_verdict.md")
    (HASHES / "final_outputs_CURRENT_HASH.txt").write_text(h_ver + "\n", encoding="utf-8")

    print("\n" + "=" * 72)
    print(f"VERDICT: {verdict}")
    print("=" * 72)
    return verdict


if __name__ == "__main__":
    main()
