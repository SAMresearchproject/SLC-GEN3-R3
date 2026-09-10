"""
CR031_X_RADIAL_LAW_POPULATION_TEST runner.

Implements the test specified in CR031_PRECOMMIT.md (SHA-256
01797081265fdc072b233dfed413c38374a8a27f4ef6c02bcf1740623ea42b05).

All inputs, predictions, wrong controls, mass-to-light values, binning, random
seed sequence, and verdict ladder are frozen in the precommit. This script only
executes; it does not redefine any test condition.

Outputs:
  CR031_summary.json
  CR031_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math
from typing import Iterable

import numpy as np

# -- Frozen sources -----------------------------------------------------------

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)
G392_RESIDUALS = Path(
    r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST\G392_sparc_galaxy_residuals.csv"
)

# -- Frozen test parameters per precommit -------------------------------------

UPSILON_BUL = 0.7
UPSILON_DISK_CANONICAL = 0.5
UPSILON_DISK_WC1 = 0.3
UPSILON_DISK_WC2 = 0.7

# rho-bin edges per precommit Implementation Discipline:
# [0.0,0.2), [0.2,0.4), [0.4,0.6), [0.6,0.8), [0.8,1.0]
RHO_EDGES_LOW  = [0.0, 0.2, 0.4, 0.6, 0.8]
RHO_EDGES_HIGH = [0.2, 0.4, 0.6, 0.8, 1.0]
RHO_BIN_LABELS = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]

# P2 / cosmic separation
REF_COSMIC_X     = 5.364   # CR023 sealed Omega_PBH/Omega_b
REF_OUTER_MEDIAN = 3.18    # CR025 sealed SPARC outer median
P2_OUTER_LOW     = 2.5
P2_OUTER_HIGH    = 4.5
P2_OUTER_CAP     = 0.85 * REF_COSMIC_X  # 4.5594

# WC trial discipline
N_TRIALS = 1000


# -- Parsers ------------------------------------------------------------------


def parse_mrt(path: Path) -> dict[str, list[tuple[float, float, float, float, float]]]:
    """Return {galaxy: [(R, Vobs, Vgas, Vdisk, Vbul), ...]}."""
    galaxies: dict[str, list] = {}
    with path.open("r") as f:
        lines = f.readlines()
    in_data = False
    sep = 0
    for line in lines:
        if line.startswith("---"):
            sep += 1
            if sep == 3:
                in_data = True
            continue
        if not in_data or not line.strip():
            continue
        gid = line[0:11].strip()
        try:
            R     = float(line[19:25])
            Vobs  = float(line[26:32])
            Vgas  = float(line[39:45])
            Vdisk = float(line[46:52])
            Vbul  = float(line[53:59])
        except ValueError:
            continue
        galaxies.setdefault(gid, []).append((R, Vobs, Vgas, Vdisk, Vbul))
    return galaxies


def load_quality_map(path: Path) -> dict[str, int]:
    qmap: dict[str, int] = {}
    if not path.exists():
        return qmap
    with path.open("r") as f:
        for row in csv.DictReader(f):
            try:
                qmap[row["galaxy"]] = int(row["quality"])
            except (KeyError, ValueError):
                pass
    return qmap


# -- Core computation ---------------------------------------------------------


def bin_index(rho: float) -> int | None:
    """Bin index 0..4 per precommit; last bin closed at 1.0."""
    if 0.8 <= rho <= 1.0:
        return 4
    for i in range(4):
        if RHO_EDGES_LOW[i] <= rho < RHO_EDGES_HIGH[i]:
            return i
    return None


def compute_X(Vobs: float, Vgas: float, Vdisk: float, Vbul: float,
              upsilon_disk: float, upsilon_bul: float) -> float | None:
    """Return X = V_dark^2 / V_bar^2 (signed), or None if V_bar^2 <= 0."""
    vbar2 = Vgas * abs(Vgas) + upsilon_disk * Vdisk ** 2 + upsilon_bul * Vbul ** 2
    if vbar2 <= 0:
        return None
    vdark2 = Vobs ** 2 - vbar2
    return vdark2 / vbar2  # may be negative if V_obs^2 < V_bar^2


def galaxy_bin_medians(rows: list[tuple], upsilon_disk: float, upsilon_bul: float,
                       rho_override: list[float] | None = None) -> tuple[list[float | None], list[int], list[int]]:
    """
    For one galaxy, return:
      (median_X_per_bin: list[5] of float or None,
       nonpos_count_per_bin: list[5] of int,
       total_count_per_bin: list[5] of int)
    """
    if not rows:
        return [None] * 5, [0] * 5, [0] * 5
    R_outer = max(r[0] for r in rows)
    if R_outer <= 0:
        return [None] * 5, [0] * 5, [0] * 5

    per_bin: list[list[float]] = [[] for _ in range(5)]
    nonpos = [0] * 5
    total = [0] * 5

    for i, (R, Vobs, Vgas, Vdisk, Vbul) in enumerate(rows):
        rho = rho_override[i] if rho_override is not None else R / R_outer
        b = bin_index(rho)
        if b is None:
            continue
        x = compute_X(Vobs, Vgas, Vdisk, Vbul, upsilon_disk, upsilon_bul)
        if x is None:
            continue
        total[b] += 1
        if x <= 0:
            nonpos[b] += 1
        per_bin[b].append(x)

    medians: list[float | None] = []
    for vals in per_bin:
        if not vals:
            medians.append(None)
        else:
            medians.append(float(np.median(vals)))
    return medians, nonpos, total


def population_stats(galaxies: dict[str, list], upsilon_disk: float, upsilon_bul: float,
                     rho_overrides: dict[str, list[float]] | None = None) -> dict:
    """Compute population median X and log-spread per bin (galaxy-equal)."""
    per_galaxy_bins: list[list[float]] = [[] for _ in range(5)]
    total_nonpos = [0] * 5
    total_count = [0] * 5
    n_galaxies_per_bin = [0] * 5

    for gid, rows in galaxies.items():
        rho_override = (rho_overrides or {}).get(gid)
        medians, nonpos, total = galaxy_bin_medians(
            rows, upsilon_disk, upsilon_bul, rho_override
        )
        for b in range(5):
            if medians[b] is not None:
                per_galaxy_bins[b].append(medians[b])
                n_galaxies_per_bin[b] += 1
            total_nonpos[b] += nonpos[b]
            total_count[b] += total[b]

    pop_median = [float(np.median(v)) if v else None for v in per_galaxy_bins]

    log_spread = []
    n_pos_per_bin = [0] * 5
    for b, vals in enumerate(per_galaxy_bins):
        pos_vals = [v for v in vals if v > 0]
        n_pos_per_bin[b] = len(pos_vals)
        if len(pos_vals) >= 2:
            logs = np.log10(pos_vals)
            log_spread.append(float(np.std(logs, ddof=0)))
        else:
            log_spread.append(None)

    return dict(
        pop_median=pop_median,
        log_spread=log_spread,
        n_galaxies_per_bin=n_galaxies_per_bin,
        n_pos_per_bin=n_pos_per_bin,
        total_nonpos_per_bin=total_nonpos,
        total_count_per_bin=total_count,
    )


# -- Predictions --------------------------------------------------------------


def spearman_rank_corr(y: list[float | None]) -> float | None:
    """Spearman rank correlation between bin index (0..4) and y values."""
    pairs = [(i, v) for i, v in enumerate(y) if v is not None]
    if len(pairs) < 2:
        return None
    xs = np.array([p[0] for p in pairs], dtype=float)
    ys = np.array([p[1] for p in pairs], dtype=float)
    rx = np.argsort(np.argsort(xs))
    ry = np.argsort(np.argsort(ys))
    if np.std(rx) == 0 or np.std(ry) == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def adjacent_changes(vals: list[float | None]) -> tuple[int, int, int]:
    """Return (n_rise, n_fall, n_total_adjacent_with_both_defined)."""
    n_rise = n_fall = n_total = 0
    for i in range(4):
        a, b = vals[i], vals[i + 1]
        if a is None or b is None:
            continue
        n_total += 1
        if b > a:
            n_rise += 1
        elif b < a:
            n_fall += 1
    return n_rise, n_fall, n_total


def evaluate_p1(pop_median: list[float | None]) -> dict:
    """P1 monotonic rise."""
    out = dict(name="P1", passed=False, reason="")
    if pop_median[0] is None or pop_median[4] is None:
        out["reason"] = "endpoint missing"
        return out
    endpoint_diff = pop_median[4] - pop_median[0]
    spearman = spearman_rank_corr(pop_median)
    n_rise, _, _ = adjacent_changes(pop_median)
    out.update(
        endpoint_diff=endpoint_diff,
        spearman=spearman,
        adjacent_rises_of_4=n_rise,
    )
    if endpoint_diff <= 0:
        out["reason"] = f"endpoint_diff {endpoint_diff:.4f} <= 0"
        return out
    if spearman is None or spearman <= 0:
        out["reason"] = f"spearman {spearman} <= 0"
        return out
    if n_rise < 3:
        out["reason"] = f"adjacent rises {n_rise}/4 < 3"
        return out
    out["passed"] = True
    out["reason"] = "P1 holds"
    return out


def evaluate_p2(pop_median: list[float | None]) -> dict:
    """P2 outer plateau matches CR025 and stays below cosmic."""
    out = dict(name="P2", passed=False, reason="")
    outer = pop_median[4]
    if outer is None:
        out["reason"] = "outer bin missing"
        return out
    out.update(outer_median=outer, low_bound=P2_OUTER_LOW,
               high_bound=P2_OUTER_HIGH, cosmic_cap=P2_OUTER_CAP)
    if outer < P2_OUTER_LOW or outer > P2_OUTER_HIGH:
        out["reason"] = (
            f"outer {outer:.4f} outside [{P2_OUTER_LOW},{P2_OUTER_HIGH}]"
        )
        return out
    if outer >= P2_OUTER_CAP:
        out["reason"] = f"outer {outer:.4f} >= cosmic cap {P2_OUTER_CAP:.4f}"
        return out
    out["passed"] = True
    out["reason"] = "P2 holds"
    return out


def evaluate_p3(log_spread: list[float | None]) -> dict:
    """P3 cross-galaxy convergence at outer edge."""
    out = dict(name="P3", passed=False, reason="")
    if log_spread[0] is None or log_spread[4] is None:
        out["reason"] = "spread endpoint missing"
        return out
    endpoint_diff = log_spread[4] - log_spread[0]
    _, n_fall, _ = adjacent_changes(log_spread)
    out.update(
        spread_inner=log_spread[0],
        spread_outer=log_spread[4],
        spread_endpoint_diff=endpoint_diff,
        adjacent_decreases_of_4=n_fall,
    )
    if endpoint_diff >= 0:
        out["reason"] = (
            f"outer spread {log_spread[4]:.4f} >= inner {log_spread[0]:.4f}"
        )
        return out
    if n_fall < 3:
        out["reason"] = f"adjacent decreases {n_fall}/4 < 3"
        return out
    out["passed"] = True
    out["reason"] = "P3 holds"
    return out


# -- Wrong controls -----------------------------------------------------------


def shuffle_within_galaxy(rows: list[tuple], rng: np.random.Generator) -> list[tuple]:
    """WC3: keep R per row; shuffle (Vobs,Vgas,Vdisk,Vbul) tuples across R."""
    if len(rows) < 2:
        return list(rows)
    Rs = [r[0] for r in rows]
    vel_tuples = [(r[1], r[2], r[3], r[4]) for r in rows]
    perm = rng.permutation(len(vel_tuples))
    shuffled = [vel_tuples[perm[i]] for i in range(len(vel_tuples))]
    return [(Rs[i], *shuffled[i]) for i in range(len(Rs))]


def random_rho_overrides(galaxies: dict[str, list],
                          rng: np.random.Generator) -> dict[str, list[float]]:
    """WC4: replace rho with uniform random [0,1] for every measurement."""
    return {
        gid: rng.uniform(0.0, 1.0, size=len(rows)).tolist()
        for gid, rows in galaxies.items()
    }


def run_wc3_trials(galaxies: dict[str, list], n_trials: int) -> dict:
    """1000 seeded trials of within-galaxy shuffle; count P1 failures."""
    p1_fail_count = 0
    p1_fail_endpoint = 0
    p1_fail_spearman = 0
    p1_fail_rises = 0
    for seed in range(n_trials):
        rng = np.random.default_rng(seed)
        shuffled = {
            gid: shuffle_within_galaxy(rows, rng)
            for gid, rows in galaxies.items()
        }
        stats = population_stats(shuffled, UPSILON_DISK_CANONICAL, UPSILON_BUL)
        p1 = evaluate_p1(stats["pop_median"])
        if not p1["passed"]:
            p1_fail_count += 1
            r = p1.get("reason", "")
            if "endpoint_diff" in r:
                p1_fail_endpoint += 1
            elif "spearman" in r:
                p1_fail_spearman += 1
            elif "adjacent" in r:
                p1_fail_rises += 1
    return dict(
        n_trials=n_trials,
        p1_fail_count=p1_fail_count,
        p1_fail_fraction=p1_fail_count / n_trials,
        p1_fail_endpoint=p1_fail_endpoint,
        p1_fail_spearman=p1_fail_spearman,
        p1_fail_rises=p1_fail_rises,
        passes_as_negative_control=(p1_fail_count / n_trials) >= 0.95,
    )


def run_wc4_trials(galaxies: dict[str, list], n_trials: int) -> dict:
    """1000 seeded trials of galaxy-randomized rho; count P3 failures."""
    p3_fail_count = 0
    for seed in range(n_trials):
        rng = np.random.default_rng(seed)
        rho_over = random_rho_overrides(galaxies, rng)
        stats = population_stats(
            galaxies, UPSILON_DISK_CANONICAL, UPSILON_BUL, rho_overrides=rho_over
        )
        p3 = evaluate_p3(stats["log_spread"])
        if not p3["passed"]:
            p3_fail_count += 1
    return dict(
        n_trials=n_trials,
        p3_fail_count=p3_fail_count,
        p3_fail_fraction=p3_fail_count / n_trials,
        passes_as_negative_control=(p3_fail_count / n_trials) >= 0.95,
    )


# -- Main ---------------------------------------------------------------------


def main() -> None:
    galaxies = parse_mrt(MRT_PATH)
    n_gal = len(galaxies)
    n_pts = sum(len(rs) for rs in galaxies.values())
    print(f"Loaded {n_gal} galaxies, {n_pts} radial points")

    # --- CANONICAL ---
    print("\n--- canonical Upsilon_disk=0.5 ---")
    canon = population_stats(galaxies, UPSILON_DISK_CANONICAL, UPSILON_BUL)
    print("  bin_medians:", [f"{m:.4f}" if m else "--" for m in canon["pop_median"]])
    print("  log_spread:", [f"{s:.4f}" if s else "--" for s in canon["log_spread"]])
    print("  n_galaxies_per_bin:", canon["n_galaxies_per_bin"])
    print("  n_pos_per_bin (for log_spread):", canon["n_pos_per_bin"])
    print("  total_nonpos_per_bin (X <= 0):", canon["total_nonpos_per_bin"])
    print("  total_count_per_bin (raw points):", canon["total_count_per_bin"])

    p1 = evaluate_p1(canon["pop_median"])
    p2 = evaluate_p2(canon["pop_median"])
    p3 = evaluate_p3(canon["log_spread"])
    print(f"\n  P1: {'PASS' if p1['passed'] else 'FAIL'} -- {p1['reason']}")
    print(f"  P2: {'PASS' if p2['passed'] else 'FAIL'} -- {p2['reason']}")
    print(f"  P3: {'PASS' if p3['passed'] else 'FAIL'} -- {p3['reason']}")

    # --- WC1 (low Upsilon) ---
    print("\n--- WC1 Upsilon_disk=0.3 ---")
    wc1 = population_stats(galaxies, UPSILON_DISK_WC1, UPSILON_BUL)
    wc1_p1 = evaluate_p1(wc1["pop_median"])
    wc1_p3 = evaluate_p3(wc1["log_spread"])
    print("  bin_medians:", [f"{m:.4f}" if m else "--" for m in wc1["pop_median"]])
    print(f"  P1 holds under WC1? {wc1_p1['passed']} -- {wc1_p1['reason']}")
    print(f"  P3 holds under WC1? {wc1_p3['passed']} -- {wc1_p3['reason']}")

    # --- WC2 (high Upsilon) ---
    print("\n--- WC2 Upsilon_disk=0.7 ---")
    wc2 = population_stats(galaxies, UPSILON_DISK_WC2, UPSILON_BUL)
    wc2_p1 = evaluate_p1(wc2["pop_median"])
    wc2_p3 = evaluate_p3(wc2["log_spread"])
    print("  bin_medians:", [f"{m:.4f}" if m else "--" for m in wc2["pop_median"]])
    print(f"  P1 holds under WC2? {wc2_p1['passed']} -- {wc2_p1['reason']}")
    print(f"  P3 holds under WC2? {wc2_p3['passed']} -- {wc2_p3['reason']}")

    # --- WC3 (within-galaxy shuffle, 1000 trials) ---
    print("\n--- WC3 within-galaxy shuffle, 1000 trials ---")
    wc3 = run_wc3_trials(galaxies, N_TRIALS)
    print(f"  P1 fail fraction: {wc3['p1_fail_fraction']:.3f} "
          f"({wc3['p1_fail_count']}/{wc3['n_trials']})")
    print(f"  pass as negative control (>=0.95 fail)? {wc3['passes_as_negative_control']}")

    # --- WC4 (random rho, 1000 trials) ---
    print("\n--- WC4 galaxy-randomized rho, 1000 trials ---")
    wc4 = run_wc4_trials(galaxies, N_TRIALS)
    print(f"  P3 fail fraction: {wc4['p3_fail_fraction']:.3f} "
          f"({wc4['p3_fail_count']}/{wc4['n_trials']})")
    print(f"  pass as negative control (>=0.95 fail)? {wc4['passes_as_negative_control']}")

    # --- VERDICT ---
    print("\n=== VERDICT ===")
    pass_conditions = {
        "P1_canonical": p1["passed"],
        "P2_canonical": p2["passed"],
        "P3_canonical": p3["passed"],
        "WC1_P1": wc1_p1["passed"],
        "WC1_P3": wc1_p3["passed"],
        "WC2_P1": wc2_p1["passed"],
        "WC2_P3": wc2_p3["passed"],
        "WC3_kill": wc3["passes_as_negative_control"],
        "WC4_kill": wc4["passes_as_negative_control"],
    }
    for k, v in pass_conditions.items():
        print(f"  {k:20s}  {'PASS' if v else 'FAIL'}")

    if not p1["passed"]:
        verdict = "FAIL"
        verdict_reason = "P1 fails under canonical Upsilon (no monotonic rise)"
    elif all(pass_conditions.values()):
        verdict = "PASS"
        verdict_reason = "all sealed conditions hold"
    else:
        failed = [k for k, v in pass_conditions.items() if not v]
        verdict = "BOUNDARY"
        verdict_reason = f"P1 holds but failed conditions: {failed}"
    print(f"\n  CR031 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # --- WRITE outputs ---
    out_dir = Path(__file__).parent
    summary = dict(
        precommit_sha256="01797081265fdc072b233dfed413c38374a8a27f4ef6c02bcf1740623ea42b05",
        n_galaxies_loaded=n_gal,
        n_radial_points_loaded=n_pts,
        canonical=dict(
            upsilon_disk=UPSILON_DISK_CANONICAL,
            upsilon_bul=UPSILON_BUL,
            pop_median=canon["pop_median"],
            log_spread=canon["log_spread"],
            n_galaxies_per_bin=canon["n_galaxies_per_bin"],
            n_pos_per_bin=canon["n_pos_per_bin"],
            total_nonpos_per_bin=canon["total_nonpos_per_bin"],
            total_count_per_bin=canon["total_count_per_bin"],
            P1=p1, P2=p2, P3=p3,
        ),
        WC1=dict(
            upsilon_disk=UPSILON_DISK_WC1, upsilon_bul=UPSILON_BUL,
            pop_median=wc1["pop_median"], log_spread=wc1["log_spread"],
            P1=wc1_p1, P3=wc1_p3,
        ),
        WC2=dict(
            upsilon_disk=UPSILON_DISK_WC2, upsilon_bul=UPSILON_BUL,
            pop_median=wc2["pop_median"], log_spread=wc2["log_spread"],
            P1=wc2_p1, P3=wc2_p3,
        ),
        WC3=wc3,
        WC4=wc4,
        pass_conditions=pass_conditions,
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR031_summary.json").write_text(
        json.dumps(summary, indent=2, default=str)
    )

    # Evidence rows for CR031_evidence_rows.csv
    evidence = []
    for i, lbl in enumerate(RHO_BIN_LABELS):
        evidence.append(dict(
            item=f"canonical_median_X_bin_{lbl}",
            value=canon["pop_median"][i] if canon["pop_median"][i] is not None else "",
            pass_field=True,
        ))
        evidence.append(dict(
            item=f"canonical_log10X_spread_bin_{lbl}",
            value=canon["log_spread"][i] if canon["log_spread"][i] is not None else "",
            pass_field=True,
        ))
        evidence.append(dict(
            item=f"canonical_nonpos_X_count_bin_{lbl}",
            value=canon["total_nonpos_per_bin"][i],
            pass_field=True,
        ))
    evidence.append(dict(item="P1_endpoint_diff", value=p1.get("endpoint_diff", ""), pass_field=p1["passed"]))
    evidence.append(dict(item="P1_spearman", value=p1.get("spearman", ""), pass_field=p1["passed"]))
    evidence.append(dict(item="P1_adjacent_rises_of_4", value=p1.get("adjacent_rises_of_4", ""), pass_field=p1["passed"]))
    evidence.append(dict(item="P2_outer_median", value=p2.get("outer_median", ""), pass_field=p2["passed"]))
    evidence.append(dict(item="P3_spread_endpoint_diff", value=p3.get("spread_endpoint_diff", ""), pass_field=p3["passed"]))
    evidence.append(dict(item="P3_adjacent_decreases_of_4", value=p3.get("adjacent_decreases_of_4", ""), pass_field=p3["passed"]))
    evidence.append(dict(item="WC1_P1_passed", value=wc1_p1["passed"], pass_field=wc1_p1["passed"]))
    evidence.append(dict(item="WC2_P1_passed", value=wc2_p1["passed"], pass_field=wc2_p1["passed"]))
    evidence.append(dict(item="WC3_P1_fail_fraction", value=wc3["p1_fail_fraction"], pass_field=wc3["passes_as_negative_control"]))
    evidence.append(dict(item="WC4_P3_fail_fraction", value=wc4["p3_fail_fraction"], pass_field=wc4["passes_as_negative_control"]))
    evidence.append(dict(item="verdict", value=verdict, pass_field=(verdict == "PASS")))

    with (out_dir / "CR031_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow(dict(item=e["item"], value=e["value"], **{"pass": e["pass_field"]}))


if __name__ == "__main__":
    main()
