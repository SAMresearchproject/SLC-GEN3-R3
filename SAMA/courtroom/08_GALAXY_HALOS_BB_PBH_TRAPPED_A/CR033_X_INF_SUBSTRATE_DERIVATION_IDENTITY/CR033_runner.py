"""
CR033 runner: X_inf substrate-derivation identity test.

Implements the test specified in CR033_PRECOMMIT.md
(SHA-256 fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810).

Substrate identity under test:
    X_inf,SAM = (R - alpha_H) * Omega_m
              = (R - alpha_H) / pi
              = 10 / pi

with substrate atoms R=12, alpha_H=2, Omega_m = R*A_0 = 1/pi.

Load-bearing prediction:
    P1: |median( log10( M_halo_SAM / M_halo_measured ) )| <= 0.05
        across all SPARC galaxies with M_halo_measured > 0.

Strict input discipline:
    - Allowed external file: MassModels_Lelli2016c.mrt
    - Forbidden: every prior CR result/summary/evidence file in
      branch 08; CR205 files; any prior empirical X_inf value;
      any prior outer-dark-fraction median.
    - The runner installs a forbidden-file open() guard that aborts
      execution if any forbidden path is accessed.

Outputs:
    CR033_summary.json
    CR033_evidence_rows.csv
    CR033_result.md
    CR033_null_WC1_random_xinf.csv
    CR033_null_WC2_vbar_shuffle.csv
"""

from __future__ import annotations

import builtins
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np


# =====================================================================
# Strict input discipline: forbidden-file open() guard
# =====================================================================

CR033_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR033_DIR.parent

FORBIDDEN_PATTERNS = [
    re.compile(r"CR025_summary\.json$",        re.IGNORECASE),
    re.compile(r"CR025_result\.md$",           re.IGNORECASE),
    re.compile(r"CR025_evidence_rows\.csv$",   re.IGNORECASE),
    re.compile(r"CR031b?_summary\.json$",      re.IGNORECASE),
    re.compile(r"CR031b?_result\.md$",         re.IGNORECASE),
    re.compile(r"CR031b?_evidence_rows\.csv$", re.IGNORECASE),
    re.compile(r"CR032_summary\.json$",        re.IGNORECASE),
    re.compile(r"CR032_result\.md$",           re.IGNORECASE),
    re.compile(r"CR032_evidence_rows\.csv$",   re.IGNORECASE),
    re.compile(r"CR032.*per_galaxy.*\.csv$",   re.IGNORECASE),
    re.compile(r"CR205.*",                     re.IGNORECASE),
    re.compile(r"galaxy_mass_derivation.*\.csv$", re.IGNORECASE),
    re.compile(r"x_radial_per_galaxy\.csv$",   re.IGNORECASE),
    re.compile(r"x_population_per_galaxy_binned\.csv$", re.IGNORECASE),
]

OPENED_PATHS: list[str] = []
_orig_open = builtins.open


def _guarded_open(file, *args, **kwargs):
    p = os.fspath(file) if not isinstance(file, int) else str(file)
    OPENED_PATHS.append(p)
    base = os.path.basename(p)
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(base):
            raise RuntimeError(
                f"CR033 forbidden-file guard tripped: attempted to open {p!r}"
            )
    return _orig_open(file, *args, **kwargs)


builtins.open = _guarded_open


# =====================================================================
# Frozen substrate constants (zero empirical input)
# =====================================================================

R       = 12
D       = 3
S       = 8
THETA   = 18
ALPHA_H = 2

PI      = math.pi
A_0     = 1.0 / (12.0 * PI)
OMEGA_M = R * A_0
CHI     = (S / D) * A_0
OMEGA_B = 2.0 * A_0 * (1.0 - CHI)

X_INF_SAM      = (R - ALPHA_H) * OMEGA_M         # = 10/pi
F_HALO_INF_SAM = X_INF_SAM / (1.0 + X_INF_SAM)   # = 10/(pi+10)

UPSILON_DISK = 0.5
UPSILON_BUL  = 0.7

G_KPC_KMS2_PER_MSUN = 4.30091e-6

P1_LOG_THRESHOLD = 0.05
P1_LOWER_LINEAR  = 10.0 ** (-P1_LOG_THRESHOLD)   # 0.8912509381
P1_UPPER_LINEAR  = 10.0 ** ( P1_LOG_THRESHOLD)   # 1.1220184543

N_TRIALS = 1000

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)


# =====================================================================
# Raw SPARC parser (fresh; no per-galaxy file imports)
# =====================================================================

def parse_mrt_raw(path: Path) -> dict[str, list[dict]]:
    """Parse MassModels_Lelli2016c.mrt fresh from raw rows."""
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
            R_kpc = float(line[19:25])
            Vobs  = float(line[26:32])
            Vgas  = float(line[39:45])
            Vdisk = float(line[46:52])
            Vbul  = float(line[53:59])
        except ValueError:
            continue
        vgas_signed = (1.0 if Vgas >= 0 else -1.0) * Vgas * Vgas
        vbar2 = vgas_signed + UPSILON_DISK * Vdisk ** 2 + UPSILON_BUL * Vbul ** 2
        vobs2 = Vobs * Vobs
        vdark2 = max(vobs2 - vbar2, 0.0)
        galaxies.setdefault(gid, []).append(dict(
            R=R_kpc, Vobs=Vobs, Vbar2=vbar2, Vobs2=vobs2, Vdark2=vdark2,
        ))
    return galaxies


def outer_features(galaxies: dict[str, list[dict]]):
    """Apply sample rule and extract per-galaxy outer-radius features."""
    eligible = []
    excluded_lt3 = 0
    for gid, rows in galaxies.items():
        if len(rows) < 3:
            excluded_lt3 += 1
            continue
        rows_sorted = sorted(rows, key=lambda r: r["R"])
        outer = rows_sorted[-1]
        if outer["R"] <= 0:
            continue
        if not (outer["Vbar2"] is not None and outer["Vbar2"] > -1e30):
            continue
        eligible.append(dict(
            galaxy=gid,
            n_points=len(rows),
            R_outer=outer["R"],
            Vbar2_outer=outer["Vbar2"],
            Vobs2_outer=outer["Vobs2"],
            Vdark2_outer=outer["Vdark2"],
        ))
    return eligible, excluded_lt3


# =====================================================================
# Halo mass evaluation
# =====================================================================

def compute_per_galaxy(features: list[dict], x_inf: float):
    """Compute M_halo_measured and M_halo_SAM per galaxy."""
    rows = []
    for f in features:
        M_meas = f["R_outer"] * f["Vdark2_outer"] / G_KPC_KMS2_PER_MSUN
        M_sam  = f["R_outer"] * x_inf * f["Vbar2_outer"] / G_KPC_KMS2_PER_MSUN
        rows.append(dict(
            galaxy=f["galaxy"],
            n_points=f["n_points"],
            R_outer_kpc=f["R_outer"],
            Vbar2_outer=f["Vbar2_outer"],
            Vobs2_outer=f["Vobs2_outer"],
            Vdark2_outer=f["Vdark2_outer"],
            M_halo_measured=M_meas,
            M_halo_SAM=M_sam,
        ))
    return rows


def median_log_ratio(rows: list[dict]) -> tuple[float, float, int]:
    """Return (median_log10_ratio, median_linear_ratio, n_in_stat)."""
    ratios = []
    for r in rows:
        if r["M_halo_measured"] > 0 and r["M_halo_SAM"] > 0:
            ratios.append(r["M_halo_SAM"] / r["M_halo_measured"])
    ratios = np.array(ratios, dtype=float)
    log_ratios = np.log10(ratios)
    return float(np.median(log_ratios)), float(np.median(ratios)), int(len(ratios))


# =====================================================================
# Wrong controls
# =====================================================================

def wc1_random_xinf(rows: list[dict], seed_base: int = 0, n: int = N_TRIALS):
    """WC1: random X_inf in [0.1, 10.0]; report distribution of |median log10|."""
    stats = []
    Vbar2  = np.array([r["Vbar2_outer"] for r in rows])
    Mmeas  = np.array([r["M_halo_measured"] for r in rows])
    R_out  = np.array([r["R_outer_kpc"] for r in rows])
    mask   = Mmeas > 0
    for i in range(n):
        rng = np.random.default_rng(seed_base + i)
        x_rand = float(rng.uniform(0.1, 10.0))
        M_rand = R_out * x_rand * Vbar2 / G_KPC_KMS2_PER_MSUN
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(mask & (M_rand > 0), M_rand / Mmeas, np.nan)
            log_r = np.log10(ratio)
        stats.append(dict(
            trial=i,
            seed=seed_base + i,
            X_inf_random=x_rand,
            median_log10_ratio=float(np.nanmedian(log_r)),
            abs_median_log10=float(np.abs(np.nanmedian(log_r))),
        ))
    return stats


def wc2_vbar_shuffle(rows: list[dict], x_inf: float,
                     seed_base: int = 1000, n: int = N_TRIALS):
    """WC2: shuffle V_bar^2 across galaxies; keep everything else fixed."""
    stats = []
    Vbar2  = np.array([r["Vbar2_outer"] for r in rows])
    Mmeas  = np.array([r["M_halo_measured"] for r in rows])
    R_out  = np.array([r["R_outer_kpc"] for r in rows])
    mask   = Mmeas > 0
    for i in range(n):
        rng = np.random.default_rng(seed_base + i)
        perm = rng.permutation(len(Vbar2))
        Vbar2_shuf = Vbar2[perm]
        M_shuf = R_out * x_inf * Vbar2_shuf / G_KPC_KMS2_PER_MSUN
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(mask & (M_shuf > 0), M_shuf / Mmeas, np.nan)
            log_r = np.log10(ratio)
        stats.append(dict(
            trial=i,
            seed=seed_base + i,
            median_log10_ratio=float(np.nanmedian(log_r)),
            abs_median_log10=float(np.abs(np.nanmedian(log_r))),
        ))
    return stats


def percentile_below(values: list[float], canonical: float) -> tuple[int, int, float]:
    n = len(values)
    k = int(sum(1 for v in values if v <= canonical))
    p_exact = (k + 1) / (n + 1)
    return k, n, p_exact


# =====================================================================
# E3, E5 reported evidence
# =====================================================================

def e3_outer_dark_fraction(features: list[dict]) -> dict:
    """Fresh raw-SPARC outer dark-fraction median."""
    f_halo_vals = []
    for f in features:
        Vobs2 = f["Vobs2_outer"]
        Vdark2 = f["Vdark2_outer"]
        if Vobs2 > 0 and Vdark2 >= 0:
            f_halo_vals.append(Vdark2 / Vobs2)
    f_halo_arr = np.array(f_halo_vals, dtype=float)
    median_raw = float(np.median(f_halo_arr))
    diff_abs = median_raw - F_HALO_INF_SAM
    diff_rel = diff_abs / median_raw if median_raw != 0 else float("nan")
    return dict(
        n_galaxies_used=int(len(f_halo_vals)),
        median_f_halo_outer_raw=median_raw,
        f_halo_inf_SAM_predicted=F_HALO_INF_SAM,
        difference=diff_abs,
        relative_difference=diff_rel,
    )


def e5_cosmic_vs_bound() -> dict:
    """Cosmic-vs-bound ratio identity."""
    X_cosmic_num = R - 2.0 + 2.0 * CHI
    X_cosmic_den = 2.0 - 2.0 * CHI
    X_cosmic = X_cosmic_num / X_cosmic_den
    ratio = X_cosmic / X_INF_SAM
    ratio_check = PI * (R - 2.0 + 2.0 * CHI) / ((R - ALPHA_H) * (2.0 - 2.0 * CHI))
    return dict(
        Omega_m=OMEGA_M,
        Omega_b=OMEGA_B,
        chi=CHI,
        X_cosmic=X_cosmic,
        X_inf_SAM=X_INF_SAM,
        X_cosmic_over_X_inf=ratio,
        X_cosmic_over_X_inf_check=ratio_check,
    )


# =====================================================================
# Outputs
# =====================================================================

def write_evidence_csv(rows: list[dict], path: Path):
    fields = ["galaxy", "n_points", "R_outer_kpc",
              "Vbar2_outer", "Vobs2_outer", "Vdark2_outer",
              "M_halo_measured", "M_halo_SAM",
              "ratio", "log10_ratio"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            ratio = (r["M_halo_SAM"] / r["M_halo_measured"]
                     if r["M_halo_measured"] > 0 else None)
            log10r = math.log10(ratio) if ratio and ratio > 0 else None
            w.writerow(dict(
                galaxy=r["galaxy"],
                n_points=r["n_points"],
                R_outer_kpc=r["R_outer_kpc"],
                Vbar2_outer=r["Vbar2_outer"],
                Vobs2_outer=r["Vobs2_outer"],
                Vdark2_outer=r["Vdark2_outer"],
                M_halo_measured=r["M_halo_measured"],
                M_halo_SAM=r["M_halo_SAM"],
                ratio=ratio if ratio is not None else "",
                log10_ratio=log10r if log10r is not None else "",
            ))


def write_null_csv(stats: list[dict], path: Path, extra_field: str | None = None):
    if extra_field:
        fields = ["trial", "seed", extra_field,
                  "median_log10_ratio", "abs_median_log10"]
    else:
        fields = ["trial", "seed",
                  "median_log10_ratio", "abs_median_log10"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in stats:
            w.writerow({k: s.get(k, "") for k in fields})


def main() -> int:
    print(f"CR033 runner — X_inf,SAM = 10/pi = {X_INF_SAM:.15g}")
    print(f"               f_halo,inf,SAM = 10/(pi+10) = {F_HALO_INF_SAM:.15g}")

    # Parse raw SPARC
    galaxies_raw = parse_mrt_raw(MRT_PATH)
    n_raw_galaxies = len(galaxies_raw)

    eligible, excluded_lt3 = outer_features(galaxies_raw)
    n_eligible = len(eligible)

    rows = compute_per_galaxy(eligible, X_INF_SAM)
    n_with_measured_zero = sum(1 for r in rows if r["M_halo_measured"] <= 0)
    n_in_stat = n_eligible - n_with_measured_zero

    # P1
    med_log_ratio, med_lin_ratio, _n_stat = median_log_ratio(rows)
    abs_med_log = abs(med_log_ratio)
    p1_pass = abs_med_log <= P1_LOG_THRESHOLD
    margin_ratio = abs_med_log / P1_LOG_THRESHOLD

    print(f"\nSample:")
    print(f"  raw galaxies loaded         : {n_raw_galaxies}")
    print(f"  excluded for <3 points      : {excluded_lt3}")
    print(f"  galaxies passing parser     : {n_eligible}")
    print(f"  excluded zero measured halo : {n_with_measured_zero}")
    print(f"  galaxies in P1 statistic    : {n_in_stat}")
    print(f"\nP1:")
    print(f"  median(log10 ratio)         : {med_log_ratio:+.12f}")
    print(f"  abs(median log10)           : {abs_med_log:.12f}")
    print(f"  threshold                   : {P1_LOG_THRESHOLD}")
    print(f"  margin (|med_log|/thresh)   : {margin_ratio:.6f}")
    print(f"  median linear ratio         : {med_lin_ratio:.12f}")
    print(f"  linear bound                : [{P1_LOWER_LINEAR:.10f}, "
          f"{P1_UPPER_LINEAR:.10f}]")
    print(f"  pass                        : {p1_pass}")

    # E2 statistics
    ratios_lin = np.array([
        r["M_halo_SAM"] / r["M_halo_measured"]
        for r in rows if r["M_halo_measured"] > 0
    ])
    log_ratios = np.log10(ratios_lin)
    e2 = dict(
        median_linear_ratio=float(np.median(ratios_lin)),
        median_log10_ratio=float(np.median(log_ratios)),
        abs_median_log10=float(np.abs(np.median(log_ratios))),
        abs_median_log10_over_threshold=float(
            np.abs(np.median(log_ratios)) / P1_LOG_THRESHOLD
        ),
        mean_log10_ratio=float(np.mean(log_ratios)),
        std_log10_ratio=float(np.std(log_ratios, ddof=1)),
        min_linear_ratio=float(np.min(ratios_lin)),
        max_linear_ratio=float(np.max(ratios_lin)),
        p25_linear_ratio=float(np.percentile(ratios_lin, 25)),
        p75_linear_ratio=float(np.percentile(ratios_lin, 75)),
    )

    # E3
    e3 = e3_outer_dark_fraction(eligible)

    # E4 — algebra check
    e4 = dict(
        R_minus_alpha=R - ALPHA_H,
        S_plus_alpha=S + ALPHA_H,
        Theta_minus_S=THETA - S,
        all_three_equal_10=(R - ALPHA_H == 10
                            and S + ALPHA_H == 10
                            and THETA - S == 10),
        X_inf_via_R_alpha_times_Omega_m=(R - ALPHA_H) * OMEGA_M,
        X_inf_via_R_alpha_over_pi=(R - ALPHA_H) / PI,
        X_inf_via_10_over_pi=10.0 / PI,
        machine_precision_check=abs(
            (R - ALPHA_H) * OMEGA_M - 10.0 / PI
        ) < 1e-15,
    )

    # E5
    e5 = e5_cosmic_vs_bound()

    print(f"\nE3 fresh raw-SPARC outer dark-fraction consistency check:")
    print(f"  median f_halo,outer,raw     : {e3['median_f_halo_outer_raw']:.12f}")
    print(f"  f_halo,inf,SAM (predicted)  : {e3['f_halo_inf_SAM_predicted']:.12f}")
    print(f"  difference                  : {e3['difference']:+.12f}")
    print(f"  relative difference         : {e3['relative_difference']:+.6%}")

    print(f"\nE4 algebraic substrate-equivalence check:")
    print(f"  R-alpha = S+alpha = Theta-S = 10 : "
          f"{e4['all_three_equal_10']}")
    print(f"  machine-precision identity ok    : "
          f"{e4['machine_precision_check']}")

    print(f"\nE5 cosmic-vs-bound ratio identity:")
    print(f"  X_cosmic                    : {e5['X_cosmic']:.12f}")
    print(f"  X_inf,SAM                   : {e5['X_inf_SAM']:.12f}")
    print(f"  X_cosmic / X_inf,SAM        : {e5['X_cosmic_over_X_inf']:.12f}")

    # WC1
    print(f"\nWC1 random X_inf null (n={N_TRIALS}) ...")
    wc1_stats = wc1_random_xinf(rows, seed_base=0, n=N_TRIALS)
    wc1_abs = [s["abs_median_log10"] for s in wc1_stats]
    wc1_k, wc1_n, wc1_p = percentile_below(wc1_abs, abs_med_log)
    wc1 = dict(
        n_trials=wc1_n,
        canonical_abs_median_log10=abs_med_log,
        null_mean=float(np.mean(wc1_abs)),
        null_std=float(np.std(wc1_abs, ddof=1)),
        null_min=float(np.min(wc1_abs)),
        null_max=float(np.max(wc1_abs)),
        null_median=float(np.median(wc1_abs)),
        n_null_at_least_as_extreme=wc1_k,
        canonical_percentile=wc1_k / wc1_n,
        exact_p_value=wc1_p,
    )
    print(f"  null mean / median / std    : "
          f"{wc1['null_mean']:.6f} / {wc1['null_median']:.6f} / "
          f"{wc1['null_std']:.6f}")
    print(f"  canonical percentile in null: {wc1['canonical_percentile']:.4f}")
    print(f"  exact (k+1)/(N+1) p-value   : {wc1['exact_p_value']:.6f}")

    # WC2
    print(f"\nWC2 V_bar permutation null (n={N_TRIALS}) ...")
    wc2_stats = wc2_vbar_shuffle(rows, X_INF_SAM, seed_base=1000, n=N_TRIALS)
    wc2_abs = [s["abs_median_log10"] for s in wc2_stats]
    wc2_k, wc2_n, wc2_p = percentile_below(wc2_abs, abs_med_log)
    wc2 = dict(
        n_trials=wc2_n,
        canonical_abs_median_log10=abs_med_log,
        null_mean=float(np.mean(wc2_abs)),
        null_std=float(np.std(wc2_abs, ddof=1)),
        null_min=float(np.min(wc2_abs)),
        null_max=float(np.max(wc2_abs)),
        null_median=float(np.median(wc2_abs)),
        n_null_at_least_as_extreme=wc2_k,
        canonical_percentile=wc2_k / wc2_n,
        exact_p_value=wc2_p,
    )
    print(f"  null mean / median / std    : "
          f"{wc2['null_mean']:.6f} / {wc2['null_median']:.6f} / "
          f"{wc2['null_std']:.6f}")
    print(f"  canonical percentile in null: {wc2['canonical_percentile']:.4f}")
    print(f"  exact (k+1)/(N+1) p-value   : {wc2['exact_p_value']:.6f}")

    # ----- Emit artifacts -----

    summary = dict(
        precommit_sha256="fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810",
        execution_status="CLEAN",
        scientific_verdict="PASS" if p1_pass else "FAIL",
        triage_bin="A",
        free_parameters_introduced=0,
        per_galaxy_fitting=False,
        catalog_fit_parameters=0,
        empirical_X_inf_input=False,
        prior_CR_result_inputs=False,
        # Substrate identity
        substrate=dict(
            R=R, D=D, S=S, Theta=THETA, alpha_H=ALPHA_H,
            A_0=A_0, Omega_m=OMEGA_M, Omega_b=OMEGA_B, chi=CHI,
            X_inf_SAM=X_INF_SAM,
            f_halo_inf_SAM=F_HALO_INF_SAM,
            X_inf_SAM_formula="(R - alpha_H) * Omega_m = 10/pi",
        ),
        # Sample
        sample=dict(
            n_raw_galaxies=n_raw_galaxies,
            n_excluded_lt3=excluded_lt3,
            n_eligible=n_eligible,
            n_excluded_zero_measured=n_with_measured_zero,
            n_in_P1_statistic=n_in_stat,
        ),
        # P1
        P1=dict(
            median_log10_ratio=med_log_ratio,
            abs_median_log10=abs_med_log,
            threshold=P1_LOG_THRESHOLD,
            margin_abs_median_over_threshold=margin_ratio,
            median_linear_ratio=med_lin_ratio,
            linear_lower_bound=P1_LOWER_LINEAR,
            linear_upper_bound=P1_UPPER_LINEAR,
            pass_=p1_pass,
        ),
        E2=e2,
        E3=e3,
        E4=e4,
        E5=e5,
        WC1=wc1,
        WC2=wc2,
        external_inputs=dict(
            MassModels_Lelli2016c=str(MRT_PATH),
        ),
        forbidden_files_opened=False,
        opened_paths_count=len(OPENED_PATHS),
    )

    out_summary = CR033_DIR / "CR033_summary.json"
    out_evidence = CR033_DIR / "CR033_evidence_rows.csv"
    out_result = CR033_DIR / "CR033_result.md"
    out_wc1 = CR033_DIR / "CR033_null_WC1_random_xinf.csv"
    out_wc2 = CR033_DIR / "CR033_null_WC2_vbar_shuffle.csv"

    out_summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_evidence_csv(rows, out_evidence)
    write_null_csv(wc1_stats, out_wc1, extra_field="X_inf_random")
    write_null_csv(wc2_stats, out_wc2)

    # Result markdown
    verdict = "PASS" if p1_pass else "FAIL"
    verdict_token = (
        "CR033_PASS_X_INF_SUBSTRATE_IDENTITY_10_OVER_PI"
        "_REPRODUCES_RAW_SPARC_OUTER_HALO_MASS_POPULATION_MEDIAN"
        if p1_pass else
        "CR033_FAIL_X_INF_SUBSTRATE_IDENTITY_10_OVER_PI"
        "_OUTSIDE_PREDECLARED_P1_BAND"
    )
    pass_summary_line = (
        "CR033 PASS confirms that X_inf,SAM = 10/pi, computed from substrate "
        "atoms only, reproduces the raw-SPARC outer-radius halo-mass "
        "population median within the predeclared +/- 12% tolerance."
        if p1_pass else
        "CR033 FAIL rejects X_inf,SAM = 10/pi as a sufficient raw-SPARC "
        "replacement for the outer halo-saturation coordinate under the "
        "predeclared P1 gate."
    )

    result_md = f"""# CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY

## Verdict

```text
{verdict_token}
```

## Courtroom Fields

```text
execution_status            = CLEAN
scientific_verdict          = {verdict}
triage_bin                  = A
free_parameters_introduced  = 0
per_galaxy_fitting          = false
catalog_fit_parameters      = 0
empirical_X_inf_input       = false
prior_CR_result_inputs      = false
precommit_sha256            = fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810
```

## Summary

```text
{pass_summary_line}

This is a retrospective substrate-identification, not a prospective
pre-measurement prediction. The runner did not read CR025, CR031b,
CR032, CR205, or any prior branch result file. The forbidden-file
open() guard installed at runner startup did not trip
(opened_paths_count = {len(OPENED_PATHS)}; forbidden_files_opened = false).
```

## Substrate Identity Under Test

| symbol | value |
|---|---:|
| R | {R} |
| alpha_H | {ALPHA_H} |
| Omega_m = R*A_0 = 1/pi | {OMEGA_M:.15g} |
| X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi | {X_INF_SAM:.15g} |
| f_halo,inf,SAM = 10/(pi+10) | {F_HALO_INF_SAM:.15g} |

## Sample

| field | value |
|---|---:|
| raw galaxies loaded | {n_raw_galaxies} |
| excluded for fewer than 3 radial points | {excluded_lt3} |
| galaxies passing parser validity | {n_eligible} |
| excluded for zero measured halo mass | {n_with_measured_zero} |
| galaxies in P1 statistic | {n_in_stat} |

## P1 — Load-Bearing Result

| statistic | value |
|---|---:|
| median(log10(M_halo,SAM / M_halo,measured)) | {med_log_ratio:+.12f} |
| abs(median log10) | {abs_med_log:.12f} |
| threshold | {P1_LOG_THRESHOLD} |
| margin = abs(med log10) / threshold | {margin_ratio:.6f} |
| median linear ratio | {med_lin_ratio:.12f} |
| linear lower bound 10^-0.05 | {P1_LOWER_LINEAR:.10f} |
| linear upper bound 10^+0.05 | {P1_UPPER_LINEAR:.10f} |
| **pass** | **{p1_pass}** |

## E2 — Population Agreement Statistics

| stat | value |
|---|---:|
| median linear ratio | {e2['median_linear_ratio']:.12f} |
| median log10 ratio | {e2['median_log10_ratio']:+.12f} |
| abs(median log10) | {e2['abs_median_log10']:.12f} |
| abs(median log10) / 0.05 | {e2['abs_median_log10_over_threshold']:.6f} |
| mean log10 ratio | {e2['mean_log10_ratio']:+.12f} |
| std log10 ratio | {e2['std_log10_ratio']:.12f} |
| min linear ratio | {e2['min_linear_ratio']:.6e} |
| max linear ratio | {e2['max_linear_ratio']:.6e} |
| 25th percentile linear | {e2['p25_linear_ratio']:.6f} |
| 75th percentile linear | {e2['p75_linear_ratio']:.6f} |

## E3 — Fresh Raw-SPARC Outer Dark-Fraction Consistency

| field | value |
|---|---:|
| n galaxies used | {e3['n_galaxies_used']} |
| median(f_halo,outer,raw) | {e3['median_f_halo_outer_raw']:.12f} |
| f_halo,inf,SAM = 10/(pi+10) | {e3['f_halo_inf_SAM_predicted']:.12f} |
| difference | {e3['difference']:+.12f} |
| relative difference | {e3['relative_difference']:+.6%} |

This is computed inside CR033 from raw SPARC V_dark^2/V_obs^2 at R_outer.
No prior summary or measurement was imported.

## E4 — Algebraic Substrate-Equivalence Check

| identity | value |
|---|---:|
| R - alpha_H | {e4['R_minus_alpha']} |
| S + alpha_H | {e4['S_plus_alpha']} |
| Theta - S | {e4['Theta_minus_S']} |
| (R - alpha_H) * Omega_m | {e4['X_inf_via_R_alpha_times_Omega_m']:.15g} |
| (R - alpha_H) / pi | {e4['X_inf_via_R_alpha_over_pi']:.15g} |
| 10 / pi | {e4['X_inf_via_10_over_pi']:.15g} |
| all three forms equal 10 | {e4['all_three_equal_10']} |
| machine-precision identity holds | {e4['machine_precision_check']} |

## E5 — Cosmic-vs-Bound Ratio Identity

| field | value |
|---|---:|
| Omega_m | {e5['Omega_m']:.12f} |
| Omega_b | {e5['Omega_b']:.12f} |
| chi | {e5['chi']:.12f} |
| X_cosmic | {e5['X_cosmic']:.12f} |
| X_inf,SAM | {e5['X_inf_SAM']:.12f} |
| X_cosmic / X_inf,SAM | {e5['X_cosmic_over_X_inf']:.12f} |
| analytic check pi*(R - 2 + 2chi) / ((R - alpha_H)*(2 - 2chi)) | {e5['X_cosmic_over_X_inf_check']:.12f} |

## WC1 — Random X_inf Null (1000 trials, seeds 0..999)

| field | value |
|---|---:|
| n trials | {wc1['n_trials']} |
| canonical abs(median log10) | {wc1['canonical_abs_median_log10']:.12f} |
| null mean | {wc1['null_mean']:.12f} |
| null median | {wc1['null_median']:.12f} |
| null std | {wc1['null_std']:.12f} |
| null min / max | {wc1['null_min']:.6f} / {wc1['null_max']:.6f} |
| n null at-least-as-extreme | {wc1['n_null_at_least_as_extreme']} |
| canonical percentile | {wc1['canonical_percentile']:.6f} |
| exact (k+1)/(N+1) p-value | {wc1['exact_p_value']:.6f} |

## WC2 — V_bar Permutation Null (1000 trials, seeds 1000..1999)

| field | value |
|---|---:|
| n trials | {wc2['n_trials']} |
| canonical abs(median log10) | {wc2['canonical_abs_median_log10']:.12f} |
| null mean | {wc2['null_mean']:.12f} |
| null median | {wc2['null_median']:.12f} |
| null std | {wc2['null_std']:.12f} |
| null min / max | {wc2['null_min']:.6f} / {wc2['null_max']:.6f} |
| n null at-least-as-extreme | {wc2['n_null_at_least_as_extreme']} |
| canonical percentile | {wc2['canonical_percentile']:.6f} |
| exact (k+1)/(N+1) p-value | {wc2['exact_p_value']:.6f} |

## Chronology

```text
CR033 is a retrospective substrate-identification test. The candidate
identity X_inf,SAM = (R - alpha_H)*Omega_m = 10/pi was recognized after
earlier Branch 08 halo-saturation work had already been performed.

The runner did not import or read CR025, CR031b, CR032, CR205, or any
prior branch result file. The forbidden-file open() guard was installed
at module load and did not trip. The raw-SPARC mass-model catalog
(MassModels_Lelli2016c.mrt) was the only external input.

Prospective confirmation requires a fresh non-SPARC rotation-curve
catalog. That test is deferred to CR034.
```

## Rule-9 Line

```text
This test could have falsified the claim that X_inf,SAM = 10/pi
reproduces the raw-SPARC outer-radius halo-mass population median to
within +/- 12% of unity using only raw SPARC measurements and substrate
constants.

It {"did not falsify it" if p1_pass else "falsified it"}: median linear ratio = {med_lin_ratio:.6f}, abs(median
log10) = {abs_med_log:.6f}, threshold = {P1_LOG_THRESHOLD}.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit             = fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810
External data         = MassModels_Lelli2016c.mrt (raw SPARC)
Forbidden CR025/CR031b/CR032/CR205 files not opened.
```

---

**Sealed by:** CR033 runner, 2026-06-27.
"""
    out_result.write_text(result_md, encoding="utf-8")

    print(f"\nWrote:")
    print(f"  {out_summary}")
    print(f"  {out_evidence}")
    print(f"  {out_result}")
    print(f"  {out_wc1}")
    print(f"  {out_wc2}")
    print(f"\nVerdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
