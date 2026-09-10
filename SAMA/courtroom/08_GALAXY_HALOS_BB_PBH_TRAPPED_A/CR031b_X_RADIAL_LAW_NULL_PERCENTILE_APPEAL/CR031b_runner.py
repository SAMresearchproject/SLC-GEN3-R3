"""
CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL runner.

Implements the test specified in CR031b_PRECOMMIT.md (SHA-256
52e724ab54c7254716553408744871004219d399f90a2fdbef7769b40a0ad20c).

Methodology correction relative to CR031: WC3 and WC4 supply null
distributions; canonical observed statistics are scored against those
distributions as one-sided exact permutation p-values. Binary
kill-fraction thresholds (CR031's mistake) are not used.

Outputs:
  CR031b_summary.json
  CR031b_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

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

RHO_EDGES_LOW  = [0.0, 0.2, 0.4, 0.6, 0.8]
RHO_EDGES_HIGH = [0.2, 0.4, 0.6, 0.8, 1.0]
RHO_BIN_LABELS = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]

REF_COSMIC_X     = 5.364
REF_OUTER_MEDIAN = 3.18
P2_OUTER_LOW     = 2.5
P2_OUTER_HIGH    = 4.5
P2_OUTER_CAP     = 0.85 * REF_COSMIC_X

P4_P_THRESHOLD = 0.01
P5_P_THRESHOLD = 0.01

N_TRIALS = 1000


# -- Parsers ------------------------------------------------------------------


def parse_mrt(path):
    galaxies = {}
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


def load_quality_map(path):
    qmap = {}
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


def bin_index(rho):
    if 0.8 <= rho <= 1.0:
        return 4
    for i in range(4):
        if RHO_EDGES_LOW[i] <= rho < RHO_EDGES_HIGH[i]:
            return i
    return None


def compute_X(Vobs, Vgas, Vdisk, Vbul, upsilon_disk, upsilon_bul):
    vbar2 = Vgas * abs(Vgas) + upsilon_disk * Vdisk ** 2 + upsilon_bul * Vbul ** 2
    if vbar2 <= 0:
        return None
    vdark2 = Vobs ** 2 - vbar2
    return vdark2 / vbar2


def galaxy_bin_medians(rows, upsilon_disk, upsilon_bul, rho_override=None):
    if not rows:
        return [None] * 5, [0] * 5, [0] * 5, [0] * 5
    R_outer = max(r[0] for r in rows)
    if R_outer <= 0:
        return [None] * 5, [0] * 5, [0] * 5, [0] * 5

    per_bin = [[] for _ in range(5)]
    raw_nonpos = [0] * 5
    raw_total = [0] * 5

    for i, (R, Vobs, Vgas, Vdisk, Vbul) in enumerate(rows):
        rho = rho_override[i] if rho_override is not None else R / R_outer
        b = bin_index(rho)
        if b is None:
            continue
        x = compute_X(Vobs, Vgas, Vdisk, Vbul, upsilon_disk, upsilon_bul)
        if x is None:
            continue
        raw_total[b] += 1
        if x <= 0:
            raw_nonpos[b] += 1
        per_bin[b].append(x)

    medians = [float(np.median(v)) if v else None for v in per_bin]
    has_value = [1 if v else 0 for v in per_bin]
    return medians, has_value, raw_nonpos, raw_total


def population_stats(galaxies, upsilon_disk, upsilon_bul, rho_overrides=None):
    per_galaxy_bins = [[] for _ in range(5)]
    total_raw_nonpos = [0] * 5
    total_raw_count = [0] * 5
    n_galaxies_with_bin = [0] * 5

    for gid, rows in galaxies.items():
        rho_override = (rho_overrides or {}).get(gid)
        medians, has_value, raw_nonpos, raw_total = galaxy_bin_medians(
            rows, upsilon_disk, upsilon_bul, rho_override
        )
        for b in range(5):
            if has_value[b]:
                per_galaxy_bins[b].append(medians[b])
                n_galaxies_with_bin[b] += 1
            total_raw_nonpos[b] += raw_nonpos[b]
            total_raw_count[b] += raw_total[b]

    pop_median = [float(np.median(v)) if v else None for v in per_galaxy_bins]

    log_spread = []
    n_pos_galaxy_bin = [0] * 5
    n_nonpos_galaxy_bin = [0] * 5
    for b, vals in enumerate(per_galaxy_bins):
        pos_vals = [v for v in vals if v > 0]
        n_pos_galaxy_bin[b] = len(pos_vals)
        n_nonpos_galaxy_bin[b] = n_galaxies_with_bin[b] - len(pos_vals)
        if len(pos_vals) >= 2:
            logs = np.log10(pos_vals)
            log_spread.append(float(np.std(logs, ddof=0)))
        else:
            log_spread.append(None)

    return dict(
        pop_median=pop_median,
        log_spread=log_spread,
        n_galaxies_per_bin=n_galaxies_with_bin,
        n_pos_galaxy_bin_per_bin=n_pos_galaxy_bin,
        n_nonpos_galaxy_bin_per_bin=n_nonpos_galaxy_bin,
        total_raw_nonpos_per_bin=total_raw_nonpos,
        total_raw_count_per_bin=total_raw_count,
    )


def endpoint_diff(values):
    if values[0] is None or values[4] is None:
        return None
    return values[4] - values[0]


def spearman_rank_corr(y):
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


def adjacent_changes(vals):
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


# -- Predictions --------------------------------------------------------------


def evaluate_p1(pop_median):
    out = dict(name="P1", passed=False, reason="")
    if pop_median[0] is None or pop_median[4] is None:
        out["reason"] = "endpoint missing"
        return out
    ed = pop_median[4] - pop_median[0]
    sp = spearman_rank_corr(pop_median)
    n_rise, _, _ = adjacent_changes(pop_median)
    out.update(endpoint_diff=ed, spearman=sp, adjacent_rises_of_4=n_rise)
    if ed <= 0:
        out["reason"] = f"endpoint_diff {ed:.4f} <= 0"
        return out
    if sp is None or sp <= 0:
        out["reason"] = f"spearman {sp} <= 0"
        return out
    if n_rise < 3:
        out["reason"] = f"adjacent rises {n_rise}/4 < 3"
        return out
    out["passed"] = True
    out["reason"] = "P1 holds"
    return out


def evaluate_p2(pop_median):
    out = dict(name="P2", passed=False, reason="")
    outer = pop_median[4]
    if outer is None:
        out["reason"] = "outer bin missing"
        return out
    out.update(outer_median=outer, low_bound=P2_OUTER_LOW,
               high_bound=P2_OUTER_HIGH, cosmic_cap=P2_OUTER_CAP)
    if outer < P2_OUTER_LOW or outer > P2_OUTER_HIGH:
        out["reason"] = f"outer {outer:.4f} outside [{P2_OUTER_LOW},{P2_OUTER_HIGH}]"
        return out
    if outer >= P2_OUTER_CAP:
        out["reason"] = f"outer {outer:.4f} >= cosmic cap {P2_OUTER_CAP:.4f}"
        return out
    out["passed"] = True
    out["reason"] = "P2 holds"
    return out


def evaluate_p3(log_spread):
    out = dict(name="P3", passed=False, reason="")
    if log_spread[0] is None or log_spread[4] is None:
        out["reason"] = "spread endpoint missing"
        return out
    ed = log_spread[4] - log_spread[0]
    _, n_fall, _ = adjacent_changes(log_spread)
    out.update(
        spread_inner=log_spread[0],
        spread_outer=log_spread[4],
        spread_endpoint_diff=ed,
        adjacent_decreases_of_4=n_fall,
    )
    if ed >= 0:
        out["reason"] = f"outer spread {log_spread[4]:.4f} >= inner {log_spread[0]:.4f}"
        return out
    if n_fall < 3:
        out["reason"] = f"adjacent decreases {n_fall}/4 < 3"
        return out
    out["passed"] = True
    out["reason"] = "P3 holds"
    return out


# -- Wrong-control trial generators -------------------------------------------


def shuffle_within_galaxy(rows, rng):
    if len(rows) < 2:
        return list(rows)
    Rs = [r[0] for r in rows]
    vel_tuples = [(r[1], r[2], r[3], r[4]) for r in rows]
    perm = rng.permutation(len(vel_tuples))
    shuffled = [vel_tuples[perm[i]] for i in range(len(vel_tuples))]
    return [(Rs[i], *shuffled[i]) for i in range(len(Rs))]


def random_rho_overrides(galaxies, rng):
    return {
        gid: rng.uniform(0.0, 1.0, size=len(rows)).tolist()
        for gid, rows in galaxies.items()
    }


def collect_wc3_null(galaxies, n_trials):
    """Return list of endpoint_diff values from n_trials within-galaxy shuffles."""
    null_vals = []
    for seed in range(n_trials):
        rng = np.random.default_rng(seed)
        shuffled = {gid: shuffle_within_galaxy(rows, rng)
                    for gid, rows in galaxies.items()}
        stats = population_stats(shuffled, UPSILON_DISK_CANONICAL, UPSILON_BUL)
        ed = endpoint_diff(stats["pop_median"])
        null_vals.append(ed if ed is not None else 0.0)
    return null_vals


def collect_wc4_null(galaxies, n_trials):
    """Return list of spread_endpoint_diff values from n_trials randomized-rho trials."""
    null_vals = []
    for seed in range(n_trials):
        rng = np.random.default_rng(seed)
        rho_over = random_rho_overrides(galaxies, rng)
        stats = population_stats(
            galaxies, UPSILON_DISK_CANONICAL, UPSILON_BUL, rho_overrides=rho_over
        )
        ed = endpoint_diff(stats["log_spread"])
        null_vals.append(ed if ed is not None else 0.0)
    return null_vals


def exact_perm_pvalue(canonical, null_vals, more_extreme):
    """One-sided exact permutation p-value.

    more_extreme: callable (canonical, null_val) -> bool.
    Counts how many null values are at least as extreme as canonical
    in the substrate-predicted direction.
    Returns (p_value, n_extreme, n_trials).
    """
    n = len(null_vals)
    n_extreme = sum(1 for v in null_vals if more_extreme(canonical, v))
    p = (n_extreme + 1) / (n + 1)
    return p, n_extreme, n


# -- Main ---------------------------------------------------------------------


def main():
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
    print("  n_pos_galaxy_bin_per_bin:", canon["n_pos_galaxy_bin_per_bin"])
    print("  n_nonpos_galaxy_bin_per_bin:", canon["n_nonpos_galaxy_bin_per_bin"])
    print("  total_raw_nonpos_per_bin:", canon["total_raw_nonpos_per_bin"])
    print("  total_raw_count_per_bin:", canon["total_raw_count_per_bin"])

    p1 = evaluate_p1(canon["pop_median"])
    p2 = evaluate_p2(canon["pop_median"])
    p3 = evaluate_p3(canon["log_spread"])
    print(f"\n  P1: {'PASS' if p1['passed'] else 'FAIL'} -- {p1['reason']}")
    print(f"  P2: {'PASS' if p2['passed'] else 'FAIL'} -- {p2['reason']}")
    print(f"  P3: {'PASS' if p3['passed'] else 'FAIL'} -- {p3['reason']}")

    canonical_endpoint_diff = p1.get("endpoint_diff")
    canonical_spread_endpoint_diff = p3.get("spread_endpoint_diff")

    # --- WC1 ---
    print("\n--- WC1 Upsilon_disk=0.3 ---")
    wc1 = population_stats(galaxies, UPSILON_DISK_WC1, UPSILON_BUL)
    wc1_p1 = evaluate_p1(wc1["pop_median"])
    wc1_p3 = evaluate_p3(wc1["log_spread"])
    print("  bin_medians:", [f"{m:.4f}" if m else "--" for m in wc1["pop_median"]])
    print(f"  P1 holds under WC1? {wc1_p1['passed']} -- {wc1_p1['reason']}")
    print(f"  P3 holds under WC1? {wc1_p3['passed']} -- {wc1_p3['reason']}")

    # --- WC2 ---
    print("\n--- WC2 Upsilon_disk=0.7 ---")
    wc2 = population_stats(galaxies, UPSILON_DISK_WC2, UPSILON_BUL)
    wc2_p1 = evaluate_p1(wc2["pop_median"])
    wc2_p3 = evaluate_p3(wc2["log_spread"])
    print("  bin_medians:", [f"{m:.4f}" if m else "--" for m in wc2["pop_median"]])
    print(f"  P1 holds under WC1? {wc2_p1['passed']} -- {wc2_p1['reason']}")
    print(f"  P3 holds under WC1? {wc2_p3['passed']} -- {wc2_p3['reason']}")

    # --- P4: WC3 null distribution ---
    print("\n--- P4 WC3 null (within-galaxy shuffle, 1000 trials) ---")
    wc3_null = collect_wc3_null(galaxies, N_TRIALS)
    null_arr = np.array(wc3_null)
    canonical_more_extreme = lambda canon, null: null >= canon
    p_wc3, n_extreme_wc3, _ = exact_perm_pvalue(
        canonical_endpoint_diff, wc3_null, canonical_more_extreme
    )
    print(f"  canonical endpoint_diff:           {canonical_endpoint_diff:.4f}")
    print(f"  null distribution stats:")
    print(f"    n_trials                = {N_TRIALS}")
    print(f"    null mean               = {null_arr.mean():.4f}")
    print(f"    null std                = {null_arr.std(ddof=0):.4f}")
    print(f"    null min                = {null_arr.min():.4f}")
    print(f"    null max                = {null_arr.max():.4f}")
    print(f"    null median             = {float(np.median(null_arr)):.4f}")
    print(f"    null 90th percentile    = {float(np.percentile(null_arr, 90)):.4f}")
    print(f"    null 95th percentile    = {float(np.percentile(null_arr, 95)):.4f}")
    print(f"    null 99th percentile    = {float(np.percentile(null_arr, 99)):.4f}")
    print(f"  n_null_trials_at_least_as_extreme = {n_extreme_wc3}")
    print(f"  exact permutation p_value         = {p_wc3:.6f}")
    p4_pass = p_wc3 < P4_P_THRESHOLD
    print(f"  P4 (p_WC3 < {P4_P_THRESHOLD})? {p4_pass}")

    # --- P5: WC4 null distribution ---
    print("\n--- P5 WC4 null (galaxy-randomized rho, 1000 trials) ---")
    wc4_null = collect_wc4_null(galaxies, N_TRIALS)
    null_arr = np.array(wc4_null)
    # For convergence: canonical spread_endpoint_diff is NEGATIVE. More extreme = more negative.
    canonical_more_negative = lambda canon, null: null <= canon
    p_wc4, n_extreme_wc4, _ = exact_perm_pvalue(
        canonical_spread_endpoint_diff, wc4_null, canonical_more_negative
    )
    print(f"  canonical spread_endpoint_diff:    {canonical_spread_endpoint_diff:.4f}")
    print(f"  null distribution stats:")
    print(f"    n_trials                = {N_TRIALS}")
    print(f"    null mean               = {null_arr.mean():.4f}")
    print(f"    null std                = {null_arr.std(ddof=0):.4f}")
    print(f"    null min                = {null_arr.min():.4f}")
    print(f"    null max                = {null_arr.max():.4f}")
    print(f"    null median             = {float(np.median(null_arr)):.4f}")
    print(f"    null 1st percentile     = {float(np.percentile(null_arr, 1)):.4f}")
    print(f"    null 5th percentile     = {float(np.percentile(null_arr, 5)):.4f}")
    print(f"    null 10th percentile    = {float(np.percentile(null_arr, 10)):.4f}")
    print(f"  n_null_trials_at_least_as_extreme = {n_extreme_wc4}")
    print(f"  exact permutation p_value         = {p_wc4:.6f}")
    p5_pass = p_wc4 < P5_P_THRESHOLD
    print(f"  P5 (p_WC4 < {P5_P_THRESHOLD})? {p5_pass}")

    # --- VERDICT ---
    print("\n=== VERDICT ===")
    pass_conditions = {
        "P1_canonical": p1["passed"],
        "P2_canonical": p2["passed"],
        "P3_canonical": p3["passed"],
        "P4_p_WC3_lt_0.01": p4_pass,
        "P5_p_WC4_lt_0.01": p5_pass,
        "WC1_P1": wc1_p1["passed"],
        "WC1_P3": wc1_p3["passed"],
        "WC2_P1": wc2_p1["passed"],
        "WC2_P3": wc2_p3["passed"],
    }
    for k, v in pass_conditions.items():
        print(f"  {k:24s}  {'PASS' if v else 'FAIL'}")

    if not p1["passed"]:
        verdict = "FAIL"
        verdict_reason = "P1 fails under canonical Upsilon"
    elif all(pass_conditions.values()):
        verdict = "PASS"
        verdict_reason = "all sealed conditions hold"
    else:
        failed = [k for k, v in pass_conditions.items() if not v]
        verdict = "BOUNDARY"
        verdict_reason = f"P1 holds but failed conditions: {failed}"
    print(f"\n  CR031b verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # --- WRITE outputs ---
    out_dir = Path(__file__).parent
    summary = dict(
        precommit_sha256="52e724ab54c7254716553408744871004219d399f90a2fdbef7769b40a0ad20c",
        appeal_of="CR031",
        appeal_basis="binary kill-fraction methodology replaced with null-distribution percentile",
        n_galaxies_loaded=n_gal,
        n_radial_points_loaded=n_pts,
        canonical=dict(
            upsilon_disk=UPSILON_DISK_CANONICAL,
            upsilon_bul=UPSILON_BUL,
            pop_median=canon["pop_median"],
            log_spread=canon["log_spread"],
            n_galaxies_per_bin=canon["n_galaxies_per_bin"],
            n_pos_galaxy_bin_per_bin=canon["n_pos_galaxy_bin_per_bin"],
            n_nonpos_galaxy_bin_per_bin=canon["n_nonpos_galaxy_bin_per_bin"],
            total_raw_nonpos_per_bin=canon["total_raw_nonpos_per_bin"],
            total_raw_count_per_bin=canon["total_raw_count_per_bin"],
            P1=p1, P2=p2, P3=p3,
        ),
        WC1=dict(upsilon_disk=UPSILON_DISK_WC1, upsilon_bul=UPSILON_BUL,
                 pop_median=wc1["pop_median"], log_spread=wc1["log_spread"],
                 P1=wc1_p1, P3=wc1_p3),
        WC2=dict(upsilon_disk=UPSILON_DISK_WC2, upsilon_bul=UPSILON_BUL,
                 pop_median=wc2["pop_median"], log_spread=wc2["log_spread"],
                 P1=wc2_p1, P3=wc2_p3),
        P4_WC3_null=dict(
            n_trials=N_TRIALS,
            canonical_endpoint_diff=canonical_endpoint_diff,
            null_mean=float(np.mean(wc3_null)),
            null_std=float(np.std(wc3_null, ddof=0)),
            null_min=float(np.min(wc3_null)),
            null_max=float(np.max(wc3_null)),
            null_median=float(np.median(wc3_null)),
            null_p90=float(np.percentile(wc3_null, 90)),
            null_p95=float(np.percentile(wc3_null, 95)),
            null_p99=float(np.percentile(wc3_null, 99)),
            n_extreme=n_extreme_wc3,
            p_value=p_wc3,
            passed=p4_pass,
        ),
        P5_WC4_null=dict(
            n_trials=N_TRIALS,
            canonical_spread_endpoint_diff=canonical_spread_endpoint_diff,
            null_mean=float(np.mean(wc4_null)),
            null_std=float(np.std(wc4_null, ddof=0)),
            null_min=float(np.min(wc4_null)),
            null_max=float(np.max(wc4_null)),
            null_median=float(np.median(wc4_null)),
            null_p1=float(np.percentile(wc4_null, 1)),
            null_p5=float(np.percentile(wc4_null, 5)),
            null_p10=float(np.percentile(wc4_null, 10)),
            n_extreme=n_extreme_wc4,
            p_value=p_wc4,
            passed=p5_pass,
        ),
        pass_conditions=pass_conditions,
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR031b_summary.json").write_text(
        json.dumps(summary, indent=2, default=str)
    )

    # Evidence rows
    evidence = []
    for i, lbl in enumerate(RHO_BIN_LABELS):
        evidence.append(dict(
            item=f"canonical_median_X_bin_{lbl}",
            value=canon["pop_median"][i] if canon["pop_median"][i] is not None else "",
            passes=True))
        evidence.append(dict(
            item=f"canonical_log10X_spread_bin_{lbl}",
            value=canon["log_spread"][i] if canon["log_spread"][i] is not None else "",
            passes=True))
        evidence.append(dict(
            item=f"canonical_n_nonpos_galaxy_bin_{lbl}",
            value=canon["n_nonpos_galaxy_bin_per_bin"][i],
            passes=True))
    evidence.append(dict(item="P1_endpoint_diff", value=p1.get("endpoint_diff", ""), passes=p1["passed"]))
    evidence.append(dict(item="P1_spearman", value=p1.get("spearman", ""), passes=p1["passed"]))
    evidence.append(dict(item="P1_adjacent_rises_of_4", value=p1.get("adjacent_rises_of_4", ""), passes=p1["passed"]))
    evidence.append(dict(item="P2_outer_median", value=p2.get("outer_median", ""), passes=p2["passed"]))
    evidence.append(dict(item="P3_spread_endpoint_diff", value=p3.get("spread_endpoint_diff", ""), passes=p3["passed"]))
    evidence.append(dict(item="P3_adjacent_decreases_of_4", value=p3.get("adjacent_decreases_of_4", ""), passes=p3["passed"]))
    evidence.append(dict(item="P4_WC3_null_p_value", value=p_wc3, passes=p4_pass))
    evidence.append(dict(item="P4_WC3_null_n_extreme", value=n_extreme_wc3, passes=p4_pass))
    evidence.append(dict(item="P5_WC4_null_p_value", value=p_wc4, passes=p5_pass))
    evidence.append(dict(item="P5_WC4_null_n_extreme", value=n_extreme_wc4, passes=p5_pass))
    evidence.append(dict(item="WC1_P1_passed", value=wc1_p1["passed"], passes=wc1_p1["passed"]))
    evidence.append(dict(item="WC2_P1_passed", value=wc2_p1["passed"], passes=wc2_p1["passed"]))
    evidence.append(dict(item="verdict", value=verdict, passes=(verdict == "PASS")))

    with (out_dir / "CR031b_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
