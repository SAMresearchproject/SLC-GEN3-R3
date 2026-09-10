"""
CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION runner.

Implements the test specified in CR032_PRECOMMIT.md (SHA-256
a0af5e891c5e8f2448e26ead9c9aa80686529f3eb8328db2e7c2b615d898533e).

Load-bearing prediction:
  P1: | median( log10( M_halo_sealed / M_halo_measured ) ) | <= 0.05
       (equivalent linear bound: median ratio in [0.891, 1.122])

Substrate input (zero catalog fit):
  X_inf = 3.18 (sealed CR025, confirmed CR031b)

E1-E6 are reported evidence (not gates).
WC1 and WC2 are reported null distributions with canonical percentile and
one-sided exact permutation p-value (not gates).

Outputs:
  CR032_summary.json
  CR032_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

import numpy as np

# -- Frozen test parameters per precommit -------------------------------------

UPSILON_DISK = 0.5
UPSILON_BUL  = 0.7
G_KPC_KMS2_PER_MSUN = 4.30091e-6
X_INF_SEALED = 3.18  # CR025 outer dark-fraction median -> X_inf
F_HALO_INF = X_INF_SEALED / (1.0 + X_INF_SEALED)  # = 0.7608

P1_LOG_THRESHOLD = 0.05
N_TRIALS = 1000

# -- Frozen sources -----------------------------------------------------------

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)


# -- Parser -------------------------------------------------------------------


def parse_mrt(path: Path) -> dict[str, list[dict]]:
    galaxies: dict[str, list[dict]] = {}
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
        vgas_signed = (1.0 if Vgas >= 0 else -1.0) * Vgas * Vgas
        vbar2 = vgas_signed + UPSILON_DISK * Vdisk ** 2 + UPSILON_BUL * Vbul ** 2
        if vbar2 <= 0:
            continue
        vobs2 = Vobs * Vobs
        vdark2 = max(vobs2 - vbar2, 0.0)
        X = vdark2 / vbar2
        f_halo = X / (1.0 + X) if (1.0 + X) > 0 else None
        galaxies.setdefault(gid, []).append(dict(
            R=R, Vobs=Vobs, Vbar2=vbar2, Vobs2=vobs2, Vdark2=vdark2,
            X=X, f_halo=f_halo,
        ))
    return galaxies


# -- Per-galaxy outer-radius extracts ----------------------------------------


def outer_features_per_galaxy(galaxies: dict[str, list[dict]]) -> list[dict]:
    """For each galaxy with >= 3 valid points, extract:
       R_outer, V_bar2(R_outer), V_dark2(R_outer), V_obs2(R_outer).
    Returns list of dicts (one per qualifying galaxy)."""
    features = []
    for gid, rows in galaxies.items():
        if len(rows) < 3:
            continue
        rows_sorted = sorted(rows, key=lambda r: r["R"])
        R_outer = rows_sorted[-1]["R"]
        if R_outer <= 0:
            continue
        features.append(dict(
            galaxy=gid,
            n_points=len(rows),
            R_outer=R_outer,
            Vbar2_outer=rows_sorted[-1]["Vbar2"],
            Vdark2_outer=rows_sorted[-1]["Vdark2"],
            Vobs2_outer=rows_sorted[-1]["Vobs2"],
            rows_sorted=rows_sorted,
        ))
    return features


def compute_halo_masses(features: list[dict], X_inf: float):
    """Compute M_halo_measured and M_halo_sealed per galaxy."""
    measured = []
    sealed = []
    for f in features:
        m_meas = f["R_outer"] * f["Vdark2_outer"] / G_KPC_KMS2_PER_MSUN
        m_seal = f["R_outer"] * X_inf * f["Vbar2_outer"] / G_KPC_KMS2_PER_MSUN
        measured.append(m_meas)
        sealed.append(m_seal)
    return np.array(measured), np.array(sealed)


def log_ratios(measured: np.ndarray, sealed: np.ndarray):
    """log10(sealed/measured), excluding rows where measured == 0."""
    mask = (measured > 0) & (sealed > 0)
    return np.log10(sealed[mask] / measured[mask]), mask


# -- Per-galaxy auxiliary (c_SAM, rho_{1/2}, config) -------------------------


def interpolate_crossing(rho_arr, a_arr, target):
    pairs = sorted(zip(rho_arr, a_arr))
    rhos = [p[0] for p in pairs]
    aas = [p[1] for p in pairs]
    for i in range(len(pairs) - 1):
        a0, a1 = aas[i], aas[i + 1]
        r0, r1 = rhos[i], rhos[i + 1]
        if (a0 <= target <= a1) or (a1 <= target <= a0):
            if a1 == a0:
                return r0
            frac = (target - a0) / (a1 - a0)
            return r0 + frac * (r1 - r0)
    if aas and aas[-1] >= target:
        return rhos[-1]
    return None


def log10_slope_outer(rho_arr, x_arr):
    pts = [(r, x) for r, x in zip(rho_arr, x_arr)
           if r is not None and x is not None and r > 0 and x > 0
           and 0.5 <= r <= 1.0]
    if len(pts) < 2:
        return None
    log_rho = [math.log10(p[0]) for p in pts]
    log_x = [math.log10(p[1]) for p in pts]
    n = len(pts)
    mr = sum(log_rho) / n
    mx = sum(log_x) / n
    num = sum((log_rho[i] - mr) * (log_x[i] - mx) for i in range(n))
    den = sum((log_rho[i] - mr) ** 2 for i in range(n))
    if den == 0:
        return None
    return num / den


def classify(rho_half, a_outer, slope_outer, f_in, f_out):
    if rho_half is None:
        return "disturbed_or_non_closed"
    if rho_half < 0.3:
        return "early_saturating_halo"
    if rho_half > 0.7:
        return "late_saturating_halo"
    if a_outer is not None and a_outer >= 0.95 and slope_outer is not None and abs(slope_outer) < 0.2:
        return "plateau_locked_halo"
    if slope_outer is not None and slope_outer > 0.5:
        return "rising_edge_halo"
    if f_in is not None and f_in < 0.2:
        return "baryon_dominated_inner_closure"
    if f_out is not None and f_out > 0.8:
        return "outer_substrate_dominated_closure"
    return "intermediate"


def per_galaxy_auxiliary(features: list[dict]):
    out = []
    for f in features:
        rows = f["rows_sorted"]
        R_outer = f["R_outer"]
        rho_arr = [r["R"] / R_outer for r in rows]
        f_halo_arr = [r["f_halo"] for r in rows]
        x_arr = [r["X"] for r in rows]
        A_halo_arr = [
            (fh / F_HALO_INF) if fh is not None else None for fh in f_halo_arr
        ]
        rho_clean = [r for r, a in zip(rho_arr, A_halo_arr) if a is not None]
        A_clean = [a for a in A_halo_arr if a is not None]

        rho_half = interpolate_crossing(rho_clean, A_clean, 0.5)
        rho_90 = interpolate_crossing(rho_clean, A_clean, 0.9)
        c_SAM = (1.0 / rho_half) if (rho_half is not None and rho_half > 0) else None
        f_halo_inner = f_halo_arr[0] if f_halo_arr else None
        f_halo_outer = f_halo_arr[-1] if f_halo_arr else None
        slope = log10_slope_outer(rho_arr, x_arr)
        a_outer = A_clean[-1] if A_clean else None
        config = classify(rho_half, a_outer, slope, f_halo_inner, f_halo_outer)
        out.append(dict(
            galaxy=f["galaxy"], rho_half=rho_half, rho_90=rho_90, c_SAM=c_SAM,
            f_halo_inner=f_halo_inner, f_halo_outer=f_halo_outer,
            slope_outer=slope, config=config,
        ))
    return out


# -- Main ---------------------------------------------------------------------


def main():
    out_dir = Path(__file__).parent

    galaxies = parse_mrt(MRT_PATH)
    print(f"Loaded {len(galaxies)} galaxies, "
          f"{sum(len(r) for r in galaxies.values())} valid radial points")
    print(f"Sealed X_inf = {X_INF_SEALED}  (CR025 outer dark-fraction median)")
    print(f"f_halo,inf   = {F_HALO_INF:.6f}\n")

    features = outer_features_per_galaxy(galaxies)
    print(f"Galaxies analyzed: {len(features)} (>= 3 radial points, R_outer > 0)")

    # --- P1 ---
    M_measured, M_sealed = compute_halo_masses(features, X_INF_SEALED)
    log_r, mask = log_ratios(M_measured, M_sealed)
    n_excluded_zero = int(np.sum(M_measured == 0))
    median_log_r = float(np.median(log_r))
    p1_passed = abs(median_log_r) <= P1_LOG_THRESHOLD
    median_ratio = float(10 ** median_log_r)

    print("\n=== P1 LOAD-BEARING PREDICTION ===")
    print(f"  n galaxies in median statistic: {int(mask.sum())}")
    print(f"  n galaxies excluded (M_halo_measured == 0): {n_excluded_zero}")
    print(f"  median log10(sealed/measured) = {median_log_r:+.5f}")
    print(f"  |median log10|                 = {abs(median_log_r):.5f}")
    print(f"  threshold                      = {P1_LOG_THRESHOLD}")
    print(f"  median linear ratio            = {median_ratio:.4f}")
    print(f"  linear bound                   = [0.891, 1.122]")
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}")

    # --- E1: mean offset, scatter ---
    mean_log = float(np.mean(log_r))
    std_log = float(np.std(log_r, ddof=0))
    print("\n=== E1 mean offset + scatter (reported, not gated) ===")
    print(f"  mean log10(ratio)              = {mean_log:+.5f}")
    print(f"  std  log10(ratio)              = {std_log:.5f}")
    print(f"  (mean = bias; std = per-galaxy scatter ~factor {10**std_log:.2f})")

    # --- E2-E6: per-galaxy auxiliary ---
    aux = per_galaxy_auxiliary(features)

    print("\n=== E2 c_SAM distribution (concentration without NFW fit) ===")
    c_vals = sorted([a["c_SAM"] for a in aux if a["c_SAM"] is not None])
    if c_vals:
        n = len(c_vals)
        print(f"  n        = {n}")
        print(f"  min      = {c_vals[0]:.3f}")
        print(f"  25%      = {c_vals[n//4]:.3f}")
        print(f"  median   = {c_vals[n//2]:.3f}")
        print(f"  75%      = {c_vals[3*n//4]:.3f}")
        print(f"  max      = {c_vals[-1]:.3f}")

    print("\n=== E3 rho_{1/2}, rho_{90} distributions ===")
    rh = sorted([a["rho_half"] for a in aux if a["rho_half"] is not None])
    r90 = sorted([a["rho_90"] for a in aux if a["rho_90"] is not None])
    if rh:
        n = len(rh)
        print(f"  rho_1/2:  n={n}  median={rh[n//2]:.3f}  25%={rh[n//4]:.3f}  75%={rh[3*n//4]:.3f}")
    if r90:
        n = len(r90)
        print(f"  rho_90:   n={n}  median={r90[n//2]:.3f}  25%={r90[n//4]:.3f}  75%={r90[3*n//4]:.3f}")

    print("\n=== E4 configuration class distribution ===")
    config_counts = {}
    for a in aux:
        config_counts[a["config"]] = config_counts.get(a["config"], 0) + 1
    for cfg, cnt in sorted(config_counts.items(), key=lambda x: -x[1]):
        print(f"  {cnt:>4}  {cfg}")

    print(f"\n=== E5 f_halo,inf identity ===")
    print(f"  X_inf / (1 + X_inf)            = {F_HALO_INF:.6f}")
    print(f"  CR025 sealed outer dark median = 0.7607")
    print(f"  difference                     = {F_HALO_INF - 0.7607:+.6f}")
    print(f"  (transformation identity; confirms saturation coordinate)")

    # --- WC1: random X_inf ---
    print("\n=== WC1 null: 1000 random X_inf in [0.1, 10.0], seeds 0..999 ===")
    null_w1 = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed)
        x_random = float(rng.uniform(0.1, 10.0))
        _, M_seal_r = compute_halo_masses(features, x_random)
        log_r_r, _ = log_ratios(M_measured, M_seal_r)
        if len(log_r_r) > 0:
            null_w1.append(abs(float(np.median(log_r_r))))
    null_w1_arr = np.array(null_w1)
    canonical_abs_w1 = abs(median_log_r)
    n_ext_w1 = int(np.sum(null_w1_arr <= canonical_abs_w1))
    p_w1 = (n_ext_w1 + 1) / (len(null_w1) + 1)
    pct_w1 = float(np.mean(null_w1_arr <= canonical_abs_w1) * 100.0)
    print(f"  canonical |median log10 ratio| = {canonical_abs_w1:.5f}")
    print(f"  null median                    = {float(np.median(null_w1_arr)):.5f}")
    print(f"  null 1st percentile            = {float(np.percentile(null_w1_arr, 1)):.5f}")
    print(f"  null 5th percentile            = {float(np.percentile(null_w1_arr, 5)):.5f}")
    print(f"  null 10th percentile           = {float(np.percentile(null_w1_arr, 10)):.5f}")
    print(f"  n null at-least-as-extreme     = {n_ext_w1} of {len(null_w1)}")
    print(f"  canonical at percentile        = {pct_w1:.2f}%")
    print(f"  one-sided permutation p        = {p_w1:.5f}")

    # --- WC2: galaxy V_bar permutation ---
    print("\n=== WC2 null: 1000 V_bar permutation trials, seeds 1000..1999 ===")
    Vbar2_outer_arr = np.array([f["Vbar2_outer"] for f in features])
    R_outer_arr = np.array([f["R_outer"] for f in features])
    Vdark2_outer_arr = np.array([f["Vdark2_outer"] for f in features])
    M_measured_arr = R_outer_arr * Vdark2_outer_arr / G_KPC_KMS2_PER_MSUN

    null_w2 = []
    for seed in range(N_TRIALS):
        rng = np.random.default_rng(seed + 1000)
        perm = rng.permutation(len(features))
        Vbar2_perm = Vbar2_outer_arr[perm]
        M_seal_perm = R_outer_arr * X_INF_SEALED * Vbar2_perm / G_KPC_KMS2_PER_MSUN
        mask_perm = (M_measured_arr > 0) & (M_seal_perm > 0)
        if mask_perm.sum() == 0:
            continue
        log_r_perm = np.log10(M_seal_perm[mask_perm] / M_measured_arr[mask_perm])
        null_w2.append(abs(float(np.median(log_r_perm))))
    null_w2_arr = np.array(null_w2)
    canonical_abs_w2 = abs(median_log_r)
    n_ext_w2 = int(np.sum(null_w2_arr <= canonical_abs_w2))
    p_w2 = (n_ext_w2 + 1) / (len(null_w2) + 1)
    pct_w2 = float(np.mean(null_w2_arr <= canonical_abs_w2) * 100.0)
    print(f"  canonical |median log10 ratio| = {canonical_abs_w2:.5f}")
    print(f"  null median                    = {float(np.median(null_w2_arr)):.5f}")
    print(f"  null 1st percentile            = {float(np.percentile(null_w2_arr, 1)):.5f}")
    print(f"  null 5th percentile            = {float(np.percentile(null_w2_arr, 5)):.5f}")
    print(f"  null 10th percentile           = {float(np.percentile(null_w2_arr, 10)):.5f}")
    print(f"  n null at-least-as-extreme     = {n_ext_w2} of {len(null_w2)}")
    print(f"  canonical at percentile        = {pct_w2:.2f}%")
    print(f"  one-sided permutation p        = {p_w2:.5f}")

    # --- VERDICT ---
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    if p1_passed:
        verdict = "PASS"
        verdict_reason = (
            f"P1 holds: |median log10(ratio)| = {abs(median_log_r):.5f} "
            f"<= {P1_LOG_THRESHOLD}"
        )
    else:
        verdict = "FAIL"
        verdict_reason = (
            f"P1 fails: |median log10(ratio)| = {abs(median_log_r):.5f} "
            f"> {P1_LOG_THRESHOLD}"
        )
    print(f"  CR032 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")

    # --- Write outputs ---
    summary = dict(
        precommit_sha256="a0af5e891c5e8f2448e26ead9c9aa80686529f3eb8328db2e7c2b615d898533e",
        substrate=dict(
            X_inf_sealed=X_INF_SEALED, f_halo_inf=F_HALO_INF,
            X_inf_source="CR025 outer dark-fraction median; confirmed CR031b",
        ),
        measurement_inputs=dict(
            Upsilon_disk=UPSILON_DISK, Upsilon_bul=UPSILON_BUL,
            G_kpc_kms2_per_Msun=G_KPC_KMS2_PER_MSUN,
        ),
        n_galaxies_loaded=len(galaxies),
        n_galaxies_analyzed=len(features),
        n_in_median=int(mask.sum()),
        n_excluded_zero=n_excluded_zero,
        P1=dict(
            median_log_ratio=median_log_r,
            abs_median_log_ratio=abs(median_log_r),
            threshold=P1_LOG_THRESHOLD,
            median_linear_ratio=median_ratio,
            linear_bound_low=10 ** -P1_LOG_THRESHOLD,
            linear_bound_high=10 ** P1_LOG_THRESHOLD,
            passed=p1_passed,
        ),
        E1=dict(mean_log_ratio=mean_log, std_log_ratio=std_log,
                scatter_factor=10**std_log),
        E2_c_SAM_distribution=dict(
            n=len(c_vals),
            min=c_vals[0] if c_vals else None,
            q25=c_vals[len(c_vals)//4] if c_vals else None,
            median=c_vals[len(c_vals)//2] if c_vals else None,
            q75=c_vals[3*len(c_vals)//4] if c_vals else None,
            max=c_vals[-1] if c_vals else None,
        ),
        E3_rho_half_distribution=dict(
            n=len(rh), median=rh[len(rh)//2] if rh else None,
        ),
        E4_configuration_classes=config_counts,
        E5_f_halo_inf_identity=dict(
            f_halo_inf=F_HALO_INF,
            CR025_sealed_dark_fraction=0.7607,
            difference=F_HALO_INF - 0.7607,
        ),
        WC1_random_X_inf=dict(
            n_trials=len(null_w1),
            canonical_abs_median_log_ratio=canonical_abs_w1,
            null_median=float(np.median(null_w1_arr)),
            null_p1=float(np.percentile(null_w1_arr, 1)),
            null_p5=float(np.percentile(null_w1_arr, 5)),
            null_p10=float(np.percentile(null_w1_arr, 10)),
            n_extreme=n_ext_w1,
            canonical_percentile=pct_w1,
            permutation_p_value=p_w1,
        ),
        WC2_galaxy_V_bar_permutation=dict(
            n_trials=len(null_w2),
            canonical_abs_median_log_ratio=canonical_abs_w2,
            null_median=float(np.median(null_w2_arr)),
            null_p1=float(np.percentile(null_w2_arr, 1)),
            null_p5=float(np.percentile(null_w2_arr, 5)),
            null_p10=float(np.percentile(null_w2_arr, 10)),
            n_extreme=n_ext_w2,
            canonical_percentile=pct_w2,
            permutation_p_value=p_w2,
        ),
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR032_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = [
        dict(item="n_galaxies_loaded", value=len(galaxies), passes=True),
        dict(item="n_galaxies_analyzed", value=len(features), passes=True),
        dict(item="n_in_median", value=int(mask.sum()), passes=True),
        dict(item="X_inf_sealed", value=X_INF_SEALED, passes=True),
        dict(item="P1_median_log_ratio", value=median_log_r, passes=p1_passed),
        dict(item="P1_median_linear_ratio", value=median_ratio, passes=p1_passed),
        dict(item="P1_threshold_log", value=P1_LOG_THRESHOLD, passes=True),
        dict(item="E1_mean_log_ratio", value=mean_log, passes=True),
        dict(item="E1_std_log_ratio", value=std_log, passes=True),
        dict(item="E2_c_SAM_median", value=c_vals[len(c_vals)//2] if c_vals else None, passes=True),
        dict(item="E3_rho_half_median", value=rh[len(rh)//2] if rh else None, passes=True),
        dict(item="E4_config_count_total", value=sum(config_counts.values()), passes=True),
        dict(item="E5_f_halo_inf", value=F_HALO_INF, passes=True),
        dict(item="WC1_canonical_percentile", value=pct_w1, passes=True),
        dict(item="WC1_p_value", value=p_w1, passes=True),
        dict(item="WC2_canonical_percentile", value=pct_w2, passes=True),
        dict(item="WC2_p_value", value=p_w2, passes=True),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    with (out_dir / "CR032_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
