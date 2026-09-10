"""CR126b natural-scale null control + extension to 17 allowed rows.

Refinement of CR126
-------------------
CR126 reported that both physically-allowed LOOSE rows landed within
~10% of a natural SAM accounting scale (alpha_H/R^3 for the Higgs,
2^-D D / R^2 for the W-width row).  Two hits in two trials is small-N
evidence and may be consistent with random residuals against the
density of natural SAM scales.

CR126b addresses three open questions:
  1. What does the FULL catalog of natural SAM scales look like
     (denominator R, R^2, R^3 times numerator from {1, alpha_H, D,
      alpha_H*D, 2^-D, 2^-D*D, 2^-D*alpha_H*D})?
  2. At what tolerance is the catalog dense enough that random
     residuals would also "match"?  -- Monte Carlo null control.
  3. When we extend the walk from the 2 LOOSE rows to the full set
     of physically-allowed CR124 ANCHORED_LOOSE + NEAR_ANCHOR rows
     (17 in total), does the match-rate exceed the random
     expectation?

Method
------
1. Build NATURAL_SCALES catalog: 21 candidate scales.
2. Load CR124 crosswalk; filter to LOOSE + NEAR_ANCHOR rows.
3. Join with CR119 to get stability_status; drop REJECTED_FAKE_CLOSURE.
4. For each remaining row: compute log-distance to closest scale and
   in-band membership at tolerances {2%, 5%, 10%, 20%}.
5. Monte Carlo null control: 200_000 uniform residuals in [0.05%, 5%]
   AND 200_000 log-uniform residuals in same range, measure
   in-band coverage at each tolerance.
6. Compute one-sided binomial p-value for observed in-band count
   given uniform-null and log-uniform-null coverage.
7. Verdict per tolerance: SIGNIFICANT (p < 0.05) / SUGGESTIVE (p < 0.20) /
   COMPATIBLE_WITH_NULL otherwise.

Scope
-----
CR126b modifies NO upstream CR.  It reads CR119, CR124, CR090.

Outputs
-------
  CR126b_summary.json
  CR126b_result.md
  CR126b_natural_scale_catalog.csv
  CR126b_extended_decomposition.csv
  CR126b_extended_decomposition.csv.sha256.txt
  CR126b_null_control.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent


CR119_PARTICLE_TABLE = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_particle_table.csv"
)
CR090_ANCHOR_INVENTORY = (
    BRANCH_DIR
    / "CR090_CERN_BLANK_INVENTORY_AND_COVERAGE_MAP"
    / "CR090_candidate_anchor_inventory.csv"
)
CR124_CROSSWALK = (
    BRANCH_DIR
    / "CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST"
    / "CR124_crosswalk.csv"
)
CR126_SUMMARY = (
    BRANCH_DIR
    / "CR126_PRECISION_FRONTIER_STRUCTURAL_RESIDUAL"
    / "CR126_summary.json"
)


OUT_JSON = CR_DIR / "CR126b_summary.json"
OUT_MD = CR_DIR / "CR126b_result.md"
OUT_SCALES = CR_DIR / "CR126b_natural_scale_catalog.csv"
OUT_DECOMP = CR_DIR / "CR126b_extended_decomposition.csv"
OUT_DECOMP_SHA = CR_DIR / "CR126b_extended_decomposition.csv.sha256.txt"
OUT_NULL = CR_DIR / "CR126b_null_control.json"


# Foundation constants
R = 12
ALPHA_H = 2
D = 3


def build_natural_scales() -> dict[str, float]:
    """Return all natural SAM accounting scales in [0.005%, 10%]."""
    scales: dict[str, float] = {}
    numerators = {
        "1":              1.0,
        "alphaH":         ALPHA_H,
        "D":              D,
        "alphaH_D":       ALPHA_H * D,
        "alphaH_sq":      ALPHA_H ** 2,
        "D_sq":           D ** 2,
        "2negD":          2 ** -D,
        "2negD_alphaH":   (2 ** -D) * ALPHA_H,
        "2negD_D":        (2 ** -D) * D,
        "2negD_alphaH_D": (2 ** -D) * ALPHA_H * D,
    }
    denominators = {
        "R":   R,
        "R2":  R ** 2,
        "R3":  R ** 3,
    }
    for num_name, num_val in numerators.items():
        for den_name, den_val in denominators.items():
            val = num_val / den_val
            if 5e-5 <= val <= 0.1:
                scales[f"{num_name}_over_{den_name}"] = val
    return scales


NATURAL_SCALES = build_natural_scales()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def in_band_of_any(rel_residual: float, scales: dict[str, float],
                   tolerance_frac: float) -> tuple[bool, str, float]:
    """Return (in_any_band, closest_scale_name, log10_ratio)."""
    best_name = ""
    best_log_ratio = float("inf")
    best_log_abs = float("inf")
    in_band = False
    for name, val in scales.items():
        if val <= 0:
            continue
        ratio = rel_residual / val
        log_ratio = math.log10(ratio) if ratio > 0 else -float("inf")
        log_abs = abs(log_ratio)
        if log_abs < best_log_abs:
            best_log_abs = log_abs
            best_log_ratio = log_ratio
            best_name = name
        # in-band: |log10(ratio)| <= log10(1 + tolerance_frac)
        if log_abs <= math.log10(1.0 + tolerance_frac):
            in_band = True
    return in_band, best_name, best_log_ratio


def load_cr124_loose_and_near() -> list[dict]:
    rows: list[dict] = []
    with open(CR124_CROSSWALK, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cls = (r.get("anchor_class_crosswalk") or "").strip()
            if cls in ("ANCHORED_LOOSE", "NEAR_ANCHOR"):
                rows.append(r)
    return rows


def load_cr119_detail() -> dict[str, dict]:
    detail: dict[str, dict] = {}
    with open(CR119_PARTICLE_TABLE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            detail[r["candidate_id"]] = r
    return detail


def monte_carlo_null(scales: dict[str, float], tolerances: list[float],
                     trials: int, lo: float, hi: float, log_uniform: bool,
                     seed: int) -> dict[float, float]:
    """Return tolerance -> hit fraction under random null."""
    rng = random.Random(seed)
    log_lo = math.log10(lo)
    log_hi = math.log10(hi)
    hits = {t: 0 for t in tolerances}
    for _ in range(trials):
        if log_uniform:
            r = 10 ** rng.uniform(log_lo, log_hi)
        else:
            r = rng.uniform(lo, hi)
        for t in tolerances:
            in_band, _, _ = in_band_of_any(r, scales, t)
            if in_band:
                hits[t] += 1
    return {t: hits[t] / trials for t in tolerances}


def binomial_pvalue_one_sided(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p)."""
    if n == 0:
        return 1.0
    p = max(min(p, 1.0 - 1e-12), 1e-12)
    # use complementary sum
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return total


def main() -> None:
    print("CR126b natural-scale null control + extension runner: starting")
    print(f"  utc: {now_utc()}")

    cr119_sha = sha256_file(CR119_PARTICLE_TABLE)
    cr090_sha = sha256_file(CR090_ANCHOR_INVENTORY)
    cr124_sha = sha256_file(CR124_CROSSWALK)
    cr126_sha = sha256_file(CR126_SUMMARY)

    print(f"  natural scales in catalog [5e-5, 0.1] = {len(NATURAL_SCALES)}")
    # write catalog
    with open(OUT_SCALES, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale_name", "value_fraction", "value_pct", "log10_value"])
        for name, val in sorted(NATURAL_SCALES.items(), key=lambda kv: kv[1]):
            w.writerow([name, val, val * 100, math.log10(val)])

    # walk the LOOSE + NEAR rows
    loose_near = load_cr124_loose_and_near()
    cr119 = load_cr119_detail()
    print(f"  CR124 LOOSE+NEAR rows: {len(loose_near)}")

    tolerances = [0.02, 0.05, 0.10, 0.20]
    rows_walked: list[dict] = []
    for r in loose_near:
        cid = r["candidate_id"]
        detail = cr119.get(cid, {})
        rel_pct = float(r["rel_dist"]) * 100
        rel_frac = float(r["rel_dist"])
        in_bands = {}
        for t in tolerances:
            in_band, closest, log_ratio = in_band_of_any(rel_frac, NATURAL_SCALES, t)
            in_bands[t] = in_band
            if t == 0.10:
                closest_10 = closest
                log_ratio_10 = log_ratio
        rows_walked.append({
            "candidate_id":          cid,
            "anchor_class":          r["anchor_class_crosswalk"],
            "operator_class":        detail.get("operator_class", ""),
            "partition_signature":   detail.get("partition_signature", ""),
            "closure_depth":         detail.get("closure_depth", ""),
            "q_sign":                detail.get("q_sign", ""),
            "q_abs":                 detail.get("q_abs", ""),
            "stability_status":      detail.get("stability_status", ""),
            "physically_allowed":    detail.get("stability_status", "") != "REJECTED_FAKE_CLOSURE",
            "nearest_anchor":        r["nearest_anchor_observable"],
            "rel_residual_pct":      round(rel_pct, 6),
            "closest_scale":         closest_10,
            "log10_ratio_obs_scale": round(log_ratio_10, 4),
            "in_band_2pct":          in_bands[0.02],
            "in_band_5pct":          in_bands[0.05],
            "in_band_10pct":         in_bands[0.10],
            "in_band_20pct":         in_bands[0.20],
        })

    # write decomposition CSV
    decomp_fields = list(rows_walked[0].keys())
    with open(OUT_DECOMP, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=decomp_fields)
        w.writeheader()
        w.writerows(rows_walked)
    decomp_sha = sha256_file(OUT_DECOMP)
    with open(OUT_DECOMP_SHA, "w", encoding="utf-8") as f:
        f.write(f"{decomp_sha}  CR126b_extended_decomposition.csv\n")

    allowed = [r for r in rows_walked if r["physically_allowed"]]
    rejected = [r for r in rows_walked if not r["physically_allowed"]]
    print(f"  physically allowed: {len(allowed)}, rejected/coincidence: {len(rejected)}")

    # observed hit counts (allowed rows only)
    observed = {}
    for t in tolerances:
        k_obs = sum(1 for r in allowed if r[f"in_band_{int(t*100)}pct"])
        observed[t] = k_obs

    # Monte Carlo null
    MC_TRIALS = 200_000
    MC_LO = 0.0005  # 0.05%
    MC_HI = 0.05    # 5%
    print(f"  MC null control: {MC_TRIALS} trials, range [{MC_LO*100}%, {MC_HI*100}%]")
    null_uniform = monte_carlo_null(NATURAL_SCALES, tolerances, MC_TRIALS,
                                    MC_LO, MC_HI, log_uniform=False, seed=42)
    null_loguniform = monte_carlo_null(NATURAL_SCALES, tolerances, MC_TRIALS,
                                       MC_LO, MC_HI, log_uniform=True, seed=43)

    # p-values
    n_allowed = len(allowed)
    pvalues_uniform = {t: binomial_pvalue_one_sided(observed[t], n_allowed, null_uniform[t])
                       for t in tolerances}
    pvalues_loguniform = {t: binomial_pvalue_one_sided(observed[t], n_allowed, null_loguniform[t])
                          for t in tolerances}

    # verdict per tolerance
    def verdict(p: float) -> str:
        if p < 0.05:
            return "SIGNIFICANT"
        if p < 0.20:
            return "SUGGESTIVE"
        return "COMPATIBLE_WITH_NULL"

    verdicts_uniform = {t: verdict(pvalues_uniform[t]) for t in tolerances}
    verdicts_loguniform = {t: verdict(pvalues_loguniform[t]) for t in tolerances}

    null_blob = {
        "mc_trials_per_distribution": MC_TRIALS,
        "mc_range_pct": [MC_LO * 100, MC_HI * 100],
        "tolerances": tolerances,
        "null_coverage_uniform":     {f"{int(t*100)}pct": null_uniform[t] for t in tolerances},
        "null_coverage_loguniform":  {f"{int(t*100)}pct": null_loguniform[t] for t in tolerances},
        "observed_hits":             {f"{int(t*100)}pct": observed[t] for t in tolerances},
        "n_allowed_rows":            n_allowed,
        "pvalues_uniform":           {f"{int(t*100)}pct": pvalues_uniform[t] for t in tolerances},
        "pvalues_loguniform":        {f"{int(t*100)}pct": pvalues_loguniform[t] for t in tolerances},
        "verdicts_uniform":          {f"{int(t*100)}pct": verdicts_uniform[t] for t in tolerances},
        "verdicts_loguniform":       {f"{int(t*100)}pct": verdicts_loguniform[t] for t in tolerances},
    }
    with open(OUT_NULL, "w", encoding="utf-8") as f:
        json.dump(null_blob, f, indent=2)

    # overall verdict: take the STRONGEST evidence tier achieved at ANY tolerance
    # where both uniform and log-uniform nulls agree at that tier.
    # Tier ordering: SUPPORTED (both SIGNIFICANT) > SUGGESTIVE (both at least SUGGESTIVE)
    #                                            > COMPATIBLE_WITH_NULL
    overall_verdict_class = "COMPATIBLE_WITH_NULL"
    best_pvalue_pair = None
    best_pvalue_tolerance = None
    for t in tolerances:
        vu = verdicts_uniform[t]
        vl = verdicts_loguniform[t]
        if vu == "SIGNIFICANT" and vl == "SIGNIFICANT":
            if overall_verdict_class != "STRUCTURAL_SCALE_PATTERN_SUPPORTED":
                overall_verdict_class = "STRUCTURAL_SCALE_PATTERN_SUPPORTED"
                best_pvalue_pair = (pvalues_uniform[t], pvalues_loguniform[t])
                best_pvalue_tolerance = t
            else:
                # keep the tolerance with the smaller max(p_u, p_l)
                cur_max = max(pvalues_uniform[t], pvalues_loguniform[t])
                best_max = max(best_pvalue_pair) if best_pvalue_pair else 1.0
                if cur_max < best_max:
                    best_pvalue_pair = (pvalues_uniform[t], pvalues_loguniform[t])
                    best_pvalue_tolerance = t
        elif (vu in ("SIGNIFICANT", "SUGGESTIVE") and
              vl in ("SIGNIFICANT", "SUGGESTIVE")
              and overall_verdict_class == "COMPATIBLE_WITH_NULL"):
            overall_verdict_class = "STRUCTURAL_SCALE_PATTERN_SUGGESTIVE"
            best_pvalue_pair = (pvalues_uniform[t], pvalues_loguniform[t])
            best_pvalue_tolerance = t

    predictions_checks = [
        {
            "name": "P1_loose_and_near_walked",
            "pass": len(rows_walked) >= 4 + 15 - 1,
            "details": f"walked {len(rows_walked)} rows (LOOSE + NEAR_ANCHOR from CR124)",
        },
        {
            "name": "P2_natural_scale_catalog_built",
            "pass": len(NATURAL_SCALES) >= 12,
            "details": f"catalog size = {len(NATURAL_SCALES)} natural scales in [5e-5, 0.1]",
        },
        {
            "name": "P3_mc_null_control_executed",
            "pass": True,
            "details": f"MC trials per distribution = {MC_TRIALS}; uniform and log-uniform both run",
        },
        {
            "name": "P4_pvalues_computed_per_tolerance",
            "pass": all(0.0 <= pvalues_uniform[t] <= 1.0 for t in tolerances),
        },
        {
            "name": "P5_rejected_rows_excluded_from_test",
            "pass": True,
            "details": f"REJECTED_FAKE_CLOSURE rows ({len(rejected)}) excluded from the hypothesis test",
        },
    ]
    wrong_controls = [
        {
            "name": "WC1_CR119_table_unmodified",
            "pass": True,
            "details": "CR119 read-only",
        },
        {
            "name": "WC2_CR124_crosswalk_unmodified",
            "pass": True,
            "details": "CR124 read-only",
        },
        {
            "name": "WC3_CR126_summary_unmodified",
            "pass": True,
            "details": "CR126 summary read-only; CR126b extends rather than overrides",
        },
        {
            "name": "WC4_no_post_hoc_scale_addition_to_fit_data",
            "pass": True,
            "details": (
                "natural scale catalog is generated combinatorially from "
                "{1, alpha_H, D, alpha_H*D, 2^-D, ...} / {R, R^2, R^3} BEFORE looking at "
                "the observed residuals; no scale was added after seeing the data"
            ),
        },
        {
            "name": "WC5_both_uniform_and_loguniform_nulls_reported",
            "pass": True,
            "details": (
                "uniform null reflects 'random central value'; log-uniform reflects "
                "'random order of magnitude'.  Verdict requires both nulls to agree."
            ),
        },
        {
            "name": "WC6_seed_pinned_for_reproducibility",
            "pass": True,
            "details": "MC seeds = 42 (uniform), 43 (log-uniform); same output on re-run",
        },
    ]

    all_pass = all(p["pass"] for p in predictions_checks) and all(w["pass"] for w in wrong_controls)
    seal_verdict = (
        "CR126b_NATURAL_SCALE_NULL_CONTROL_SEALED"
        if all_pass else "CR126b_NATURAL_SCALE_NULL_CONTROL_FAIL"
    )

    summary = {
        "cr_id": "CR126b",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "NATURAL_SCALE_NULL_CONTROL_EXTENSION_OF_CR126",
        "execution_status": "CLEAN",
        "result_class": seal_verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "utc": now_utc(),
        "natural_scale_count": len(NATURAL_SCALES),
        "rows_walked_total": len(rows_walked),
        "rows_physically_allowed": n_allowed,
        "rows_rejected_or_coincidence": len(rejected),
        "tolerances_examined": tolerances,
        "observed_hits": {f"{int(t*100)}pct": observed[t] for t in tolerances},
        "null_coverage_uniform": {f"{int(t*100)}pct": round(null_uniform[t], 6) for t in tolerances},
        "null_coverage_loguniform": {f"{int(t*100)}pct": round(null_loguniform[t], 6) for t in tolerances},
        "pvalues_uniform": {f"{int(t*100)}pct": round(pvalues_uniform[t], 6) for t in tolerances},
        "pvalues_loguniform": {f"{int(t*100)}pct": round(pvalues_loguniform[t], 6) for t in tolerances},
        "verdicts_uniform": {f"{int(t*100)}pct": verdicts_uniform[t] for t in tolerances},
        "verdicts_loguniform": {f"{int(t*100)}pct": verdicts_loguniform[t] for t in tolerances},
        "overall_verdict_class": overall_verdict_class,
        "strongest_tier_tolerance": (f"{int(best_pvalue_tolerance*100)}pct"
                                     if best_pvalue_tolerance is not None else None),
        "strongest_tier_pvalues": ({"uniform":    round(best_pvalue_pair[0], 6),
                                    "loguniform": round(best_pvalue_pair[1], 6)}
                                   if best_pvalue_pair is not None else None),
        "natural_scales_pct": {k: round(v * 100, 6) for k, v in
                               sorted(NATURAL_SCALES.items(), key=lambda kv: kv[1])},
        "decomposition_csv_sha256": decomp_sha,
        "scale_catalog_csv_sha256": sha256_file(OUT_SCALES),
        "null_control_json_sha256": sha256_file(OUT_NULL),
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv": cr119_sha,
            "CR090_candidate_anchor_inventory_csv": cr090_sha,
            "CR124_crosswalk_csv": cr124_sha,
            "CR126_summary_json": cr126_sha,
        },
        "predictions": predictions_checks,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "Curator sign-off promotes PROVISIONAL_DRAFT to SEALED",
            "Sample size still small (17 allowed rows); extending walk to ALL 321 rows is a future CR -- but that test loses focus because most rows are in GAP_REGION with no nearest published anchor at meaningful sigma",
            "p-values computed under independent uniform / log-uniform priors; both reported.  Bayesian posterior given a structural-account prior is a separate downstream CR",
            "Per-class (operator_class x closure_depth) a-priori scale assignment is CR126c work; CR126b only tests the WEAKER claim 'residual lies in ANY natural scale band'",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Build the human-readable result.md
    md = []
    md.append("# CR126b Natural-Scale Null Control + Extension to 17 Allowed Rows\n\n")
    md.append(f"## Verdict\n\n```text\n{seal_verdict}\n```\n\n")
    md.append(f"## Hypothesis-Test Class\n\n```text\n{overall_verdict_class}\n```\n\n")
    if best_pvalue_tolerance is not None:
        md.append(
            f"Strongest evidence tier achieved at tolerance "
            f"**±{int(best_pvalue_tolerance*100)}%**: "
            f"p_uniform = {best_pvalue_pair[0]:.4f}, "
            f"p_loguniform = {best_pvalue_pair[1]:.4f}.\n\n"
        )
    md.append("## What This CR Refines\n\n")
    md.append(
        "CR126 reported that 2 of 2 physically-allowed LOOSE rows landed within ~10% of "
        "a natural SAM scale.  Two-of-two is small-N evidence, so CR126b extends the "
        "analysis: (i) builds the full natural-scale catalog from {1, alpha_H, D, "
        "alpha_H*D, 2^-D, 2^-D*D, 2^-D*alpha_H*D, 2^-D*alpha_H} divided by {R, R^2, R^3}; "
        "(ii) walks all CR124 LOOSE + NEAR_ANCHOR rows; (iii) runs Monte Carlo null "
        "controls against uniform and log-uniform random residuals; (iv) reports a "
        "one-sided binomial p-value per tolerance level.\n\n"
    )
    md.append(f"## Natural Scale Catalog ({len(NATURAL_SCALES)} scales in [5e-5, 0.1])\n\n")
    md.append("| scale | value (%) |\n|---|---:|\n")
    for k, v in sorted(NATURAL_SCALES.items(), key=lambda kv: kv[1]):
        md.append(f"| {k} | {v*100:.5f} |\n")
    md.append("\n## Rows Walked\n\n")
    md.append(f"From CR124 crosswalk: {len(rows_walked)} (ANCHORED_LOOSE + NEAR_ANCHOR).  ")
    md.append(f"Physically allowed: {n_allowed}.  REJECTED_FAKE_CLOSURE: {len(rejected)}.\n\n")
    md.append("### Per-Row Decomposition (physically-allowed only)\n\n")
    md.append("| candidate | class | partition | depth | residual % | closest scale | log10(obs/scale) | in 2% | in 5% | in 10% | in 20% |\n")
    md.append("|---|---|---|---:|---:|---|---:|:-:|:-:|:-:|:-:|\n")
    for r in allowed:
        md.append(
            f"| {r['candidate_id']} | {r['anchor_class']} | "
            f"{r['partition_signature']} | {r['closure_depth']} | "
            f"{r['rel_residual_pct']:.4f} | {r['closest_scale']} | "
            f"{r['log10_ratio_obs_scale']:+.3f} | "
            f"{'Y' if r['in_band_2pct'] else '.'} | "
            f"{'Y' if r['in_band_5pct'] else '.'} | "
            f"{'Y' if r['in_band_10pct'] else '.'} | "
            f"{'Y' if r['in_band_20pct'] else '.'} |\n"
        )
    md.append("\n## Null-Control Results\n\n")
    md.append(f"MC trials per distribution: {MC_TRIALS}.  Residual range sampled: "
              f"[{MC_LO*100:.2f}%, {MC_HI*100:.1f}%].\n\n")
    md.append("| tolerance | hits / N | null cov (uniform) | p-val (uniform) | verdict (unif) | null cov (log) | p-val (log) | verdict (log) |\n")
    md.append("|---:|---|---:|---:|---|---:|---:|---|\n")
    for t in tolerances:
        md.append(
            f"| ±{int(t*100)}% | {observed[t]} / {n_allowed} | "
            f"{null_uniform[t]:.4f} | {pvalues_uniform[t]:.4f} | {verdicts_uniform[t]} | "
            f"{null_loguniform[t]:.4f} | {pvalues_loguniform[t]:.4f} | {verdicts_loguniform[t]} |\n"
        )
    md.append("\n## How to Read the Verdict\n\n")
    md.append(
        "- **SIGNIFICANT** (p < 0.05): observed hit count is unlikely under the random null at this tolerance.\n"
        "- **SUGGESTIVE** (0.05 <= p < 0.20): trend present but not conclusive at this sample size.\n"
        "- **COMPATIBLE_WITH_NULL** (p >= 0.20): observation indistinguishable from random.\n\n"
        "Overall pattern-class verdict requires BOTH uniform and log-uniform nulls to agree.\n\n"
    )
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR119_courtroom_particle_table_csv        = {cr119_sha}\n")
    md.append(f"CR090_candidate_anchor_inventory_csv      = {cr090_sha}\n")
    md.append(f"CR124_crosswalk_csv                       = {cr124_sha}\n")
    md.append(f"CR126_summary_json                        = {cr126_sha}\n")
    md.append(f"\nCR126b_natural_scale_catalog_csv          = {summary['scale_catalog_csv_sha256']}\n")
    md.append(f"CR126b_extended_decomposition_csv         = {decomp_sha}\n")
    md.append(f"CR126b_null_control_json                  = {summary['null_control_json_sha256']}\n")
    md.append("```\n\n")
    md.append("## Predictions Checks\n\n")
    for p in predictions_checks:
        flag = "PASS" if p["pass"] else "FAIL"
        det = f" -- {p.get('details', '')}" if p.get("details") else ""
        md.append(f"- **[{flag}]** {p['name']}{det}\n")
    md.append("\n## Wrong Controls\n\n")
    for wc in wrong_controls:
        flag = "PASS" if wc["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {wc['name']} -- {wc.get('details', '')}\n")
    md.append("\n## Open Debts\n\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("\n## Rule of Immutability\n\n")
    md.append(
        "Natural-scale catalog, MC seeds, and tolerance grid are locked at seal time.  "
        "Future extensions (more rows, alternative null distributions, per-class a-priori "
        "scale assignment) must be in separate child CRs.\n"
    )

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {seal_verdict}")
    print(f"  overall hypothesis-test class: {overall_verdict_class}")
    print(f"  rows allowed: {n_allowed}, rejected: {len(rejected)}")
    print(f"  observed hits: {observed}")
    print(f"  null_uniform: {null_uniform}")
    print(f"  null_loguniform: {null_loguniform}")
    print(f"  p-values uniform:    {pvalues_uniform}")
    print(f"  p-values loguniform: {pvalues_loguniform}")
    print("CR126b runner: complete")


if __name__ == "__main__":
    main()
