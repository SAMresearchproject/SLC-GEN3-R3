"""
CR004 -- SAM vs GR / Standard Discrimination Map

Tabulates substrate-derived numerical predictions against standard
theory values (GR, Planck, PDG, SPARC, etc.) and computes testability
scores per the precommit formula.

precommit : e519e7c5b8be99540c5c6984079e91f4e56b524d9b9c87e43baabd3f5f61933a
"""

import csv
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR004_PRECOMMIT.md")
PRECOMMIT_HASH = "e519e7c5b8be99540c5c6984079e91f4e56b524d9b9c87e43baabd3f5f61933a"


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


# Substrate atoms (CR258 sealed)
h_, d_ = 2, 3
S = h_**d_
V = d_**d_
F = d_**(d_+1)
R = h_**2 * d_
R2 = R*R
Theta = h_ * d_**2
L = h_ * F
M = R2 - Theta
PI = math.pi

# ---------------------------------------------------------------------
# Predictions table.
# Each row:
#   domain, quantity, sam_form, sam_value, standard_value, std_label,
#   current_sigma_pct, future_sigma_pct, future_detector, timeline
# All percent values are RELATIVE (% of standard value).
# Use None where no current measurement / no future detector projection.
# ---------------------------------------------------------------------

ROWS = [
    # ============ GW BRANCH ============
    # Schwarzschild QNM fundamental, l=m=2 n=0 (CR003)
    {
        "domain": "GW",
        "quantity": "Schwarzschild fundamental ω_R·M (l=m=2 n=0)",
        "sam_form": "d̂/S",
        "sam_value": d_/S,
        "standard_value": 0.37367168,
        "std_label": "GR (Berti+2009)",
        "current_sigma_pct": 5.0,        # current LIGO ringdown σ ~ few percent
        "future_sigma_pct": 0.1,         # LISA SNR > 1000 projected
        "future_detector": "LISA",
        "timeline": "~2035",
    },
    {
        "domain": "GW",
        "quantity": "Schwarzschild fundamental ω_I·M (l=m=2 n=0)",
        "sam_form": "R/(R²−d̂²)",
        "sam_value": R/(R2 - d_*d_),
        "standard_value": 0.08896232,
        "std_label": "GR (Berti+2009)",
        "current_sigma_pct": 15.0,       # damping is harder, current σ ~ 10-20%
        "future_sigma_pct": 0.5,         # LISA projected on damping
        "future_detector": "LISA",
        "timeline": "~2035",
    },
    {
        "domain": "GW",
        "quantity": "Schwarzschild fundamental Q factor",
        "sam_form": "135/64",
        "sam_value": 135/64,
        "standard_value": 0.37367168 / (2 * 0.08896232),
        "std_label": "GR derived",
        "current_sigma_pct": 10.0,
        "future_sigma_pct": 0.6,
        "future_detector": "LISA",
        "timeline": "~2035",
    },
    # CR003b higher modes (top 5 best matches as forecasts)
    {
        "domain": "GW",
        "quantity": "Schwarzschild ω_R·M (l=2 n=1, first overtone)",
        "sam_form": "𝒱/(F−π)",
        "sam_value": V/(F - PI),
        "standard_value": 0.34671,
        "std_label": "GR (Berti+2009)",
        "current_sigma_pct": 20.0,
        "future_sigma_pct": 0.5,
        "future_detector": "LISA + ET (joint)",
        "timeline": "~2035",
    },
    {
        "domain": "GW",
        "quantity": "Schwarzschild ω_R·M (l=3 n=0)",
        "sam_form": "F/(ℒ−𝒱)",
        "sam_value": F/(L - V),
        "standard_value": 0.59944,
        "std_label": "GR (Berti+2009)",
        "current_sigma_pct": 30.0,
        "future_sigma_pct": 1.0,
        "future_detector": "ET / CE",
        "timeline": "~2035",
    },
    {
        "domain": "GW",
        "quantity": "Schwarzschild ω_R·M (l=5 n=0)",
        "sam_form": "(ℒ+ĥ)/ℒ",
        "sam_value": (L + h_)/L,
        "standard_value": 1.01229,
        "std_label": "GR (Berti+2009)",
        "current_sigma_pct": 50.0,
        "future_sigma_pct": 2.0,
        "future_detector": "ET / CE",
        "timeline": "~2035",
    },
    # GW emission cap (CR001)
    {
        "domain": "GW",
        "quantity": "Max radiated fraction E_GW/(M·c²)",
        "sam_form": "Θ/R² = 1/8",
        "sam_value": 0.125,
        "standard_value": 0.1227,        # Hemberger 2013 NR extremal-spin equal-mass BBH
        "std_label": "NR (Hemberger+2013)",
        "current_sigma_pct": 5.0,        # NR computation precision
        "future_sigma_pct": 1.0,         # next-gen NR + observed events approaching cap
        "future_detector": "GWTC-N high-spin events",
        "timeline": "~2030",
    },

    # ============ COSMOLOGY ============
    {
        "domain": "Cosmology",
        "quantity": "Matter density Ω_m",
        "sam_form": "1/π",
        "sam_value": 1/PI,
        "standard_value": 0.315,
        "std_label": "Planck 2018",
        "current_sigma_pct": 2.2,        # σ ≈ 0.007/0.315
        "future_sigma_pct": 0.5,
        "future_detector": "CMB-S4 + DESI",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Baryon density Ω_b",
        "sam_form": "2·A_0·(1−χ)",
        "sam_value": 0.04929901,
        "standard_value": 0.0493,
        "std_label": "Planck 2018",
        "current_sigma_pct": 1.2,        # σ ≈ 0.0006/0.0493
        "future_sigma_pct": 0.3,
        "future_detector": "CMB-S4",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Hubble constant H_0 (CMB anchor)",
        "sam_form": "100·sqrt(ω_b_SAM/Ω_b)",
        "sam_value": 67.2503752,
        "standard_value": 67.36,
        "std_label": "Planck 2018",
        "current_sigma_pct": 0.8,        # σ ≈ 0.54/67.36
        "future_sigma_pct": 0.2,
        "future_detector": "CMB-S4",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Hubble constant H_0 (distance ladder)",
        "sam_form": "100·sqrt(ω_b_SAM/Ω_b)",
        "sam_value": 67.2503752,
        "standard_value": 73.04,
        "std_label": "SH0ES 2022",
        "current_sigma_pct": 1.4,        # σ ≈ 1.04/73.04
        "future_sigma_pct": 0.5,
        "future_detector": "JWST / Carnegie-Chicago",
        "timeline": "~2028",
    },
    {
        "domain": "Cosmology",
        "quantity": "Baryon-photon ratio η",
        "sam_form": "7/(4·(12π)^6)",
        "sam_value": 6.09609e-10,
        "standard_value": 6.119e-10,
        "std_label": "Planck 2018 (CMB)",
        "current_sigma_pct": 1.0,
        "future_sigma_pct": 0.5,
        "future_detector": "CMB-S4 + BBN consensus",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Scalar amplitude A_s",
        "sam_form": "η_SAM·√R",
        "sam_value": 2.1117e-9,
        "standard_value": 2.100e-9,
        "std_label": "Planck 2018",
        "current_sigma_pct": 1.4,
        "future_sigma_pct": 0.5,
        "future_detector": "CMB-S4",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Spectral index n_s",
        "sam_form": "1 − χ/2",
        "sam_value": 0.9646322349,
        "standard_value": 0.9649,
        "std_label": "Planck 2018",
        "current_sigma_pct": 0.45,       # σ ≈ 0.0044
        "future_sigma_pct": 0.15,
        "future_detector": "CMB-S4",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "Optical depth τ",
        "sam_form": "2·A_0",
        "sam_value": 0.0530516477,
        "standard_value": 0.0544,
        "std_label": "Planck 2018",
        "current_sigma_pct": 13.0,       # σ ≈ 0.0073
        "future_sigma_pct": 5.0,
        "future_detector": "CMB-S4 polarization",
        "timeline": "~2030",
    },
    {
        "domain": "Cosmology",
        "quantity": "CMB 100·θ_*",
        "sam_form": "100·r_s(z_*)/D_M(z_*)",
        "sam_value": 1.04740,
        "standard_value": 1.04110,
        "std_label": "Planck 2018",
        "current_sigma_pct": 0.029,      # σ ≈ 0.0003
        "future_sigma_pct": 0.01,
        "future_detector": "CMB-S4",
        "timeline": "~2030",
    },

    # ============ PARTICLE PHYSICS ============
    {
        "domain": "Particle",
        "quantity": "Higgs mass m_H",
        "sam_form": "R²·(1−2⁻ᴰ) − d̂²/R",
        "sam_value": 125.25,
        "standard_value": 125.20,
        "std_label": "PDG 2024",
        "current_sigma_pct": 0.088,      # σ ≈ 0.11 / 125.20
        "future_sigma_pct": 0.04,        # HL-LHC σ ~ 50 MeV
        "future_detector": "ATLAS/CMS HL-LHC",
        "timeline": "~2030",
    },
    {
        "domain": "Particle",
        "quantity": "Proton mass m_p (connection-fee)",
        "sam_form": "(R+q+d̂)/R triadic lift",
        "sam_value": 937.96,
        "standard_value": 938.272,
        "std_label": "PDG 2024",
        "current_sigma_pct": 1e-7,       # PDG essentially exact
        "future_sigma_pct": 1e-8,
        "future_detector": "g-factor measurements",
        "timeline": "now",
    },

    # ============ NEUTRINO ============
    {
        "domain": "Neutrino",
        "quantity": "Splitting ratio Δm²₃₁/Δm²₂₁",
        "sam_form": "((ĥ·d̂)²−1)/(ĥ−1) = 35",
        "sam_value": 35.0,
        "standard_value": 33.895,
        "std_label": "NuFit 5.2",
        "current_sigma_pct": 2.0,        # σ ≈ 0.7 / 33.9
        "future_sigma_pct": 0.5,
        "future_detector": "DUNE + Hyper-K",
        "timeline": "~2030",
    },
    {
        "domain": "Neutrino",
        "quantity": "Sum of neutrino masses Σm_ν",
        "sam_form": "m_1·(1 + √ĥ + ĥ·d̂)",
        "sam_value": 0.0713,            # eV
        "standard_value": 0.120,         # eV (Planck upper bound, not detection)
        "std_label": "Planck 2018 upper bound",
        "current_sigma_pct": None,       # upper bound, not measurement
        "future_sigma_pct": 25.0,        # CMB-S4 σ ~ 30 meV ≈ 25% at 120 meV
        "future_detector": "CMB-S4 + DESI",
        "timeline": "~2028-2030",
    },

    # ============ GALAXY HALOS ============
    {
        "domain": "Galaxy",
        "quantity": "Halo asymptote X_∞",
        "sam_form": "(R−ĥ)·Ω_m = 10/π",
        "sam_value": 10/PI,
        "standard_value": 3.18,
        "std_label": "SPARC sample median",
        "current_sigma_pct": 1.0,        # SPARC sample σ
        "future_sigma_pct": 0.5,
        "future_detector": "next-gen rotation curve surveys",
        "timeline": "~2030",
    },
]


def classify(gap_pct, cur_sig, fut_sig):
    """Apply the precommit classification logic."""
    if cur_sig is not None:
        score_current = gap_pct / cur_sig
    else:
        score_current = float('inf')   # no current measurement (upper bound)
    score_future = gap_pct / fut_sig if fut_sig else 0

    if cur_sig is not None and score_current > 3.0:
        status = "ALREADY DISCRIMINATING"
    elif cur_sig is not None and gap_pct < cur_sig:
        status = "ALREADY TESTED PASS"
    elif score_future > 3.0:
        status = "FUTURE-TESTABLE"
    elif score_future < 1.0:
        status = "BELOW MEASUREMENT FLOOR"
    else:
        status = "MARGINAL"
    return score_current, score_future, status


def main():
    verify_precommit()
    print("CR004 -- SAM vs GR / Standard Discrimination Map")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print(f"Rows tabulated: {len(ROWS)}")
    print()

    # Compute per-row metrics
    enriched = []
    for r in ROWS:
        gap_abs = abs(r["sam_value"] - r["standard_value"])
        gap_pct = 100.0 * gap_abs / abs(r["standard_value"])
        sc, sf, status = classify(gap_pct, r["current_sigma_pct"], r["future_sigma_pct"])
        enriched.append({
            **r,
            "gap_abs": gap_abs,
            "gap_pct": gap_pct,
            "score_current": sc,
            "score_future": sf,
            "status": status,
        })

    # Print full table
    print(f"  {'domain':<10s} {'quantity':<48s} {'SAM':>14s} {'std':>14s} "
          f"{'gap %':>8s} {'cur σ%':>8s} {'fut σ%':>8s} {'sc_cur':>7s} "
          f"{'sc_fut':>7s}  status")
    print(f"  {'-'*10} {'-'*48} {'-'*14} {'-'*14} {'-'*8} "
          f"{'-'*8} {'-'*8} {'-'*7} {'-'*7}  {'-'*20}")
    for r in enriched:
        cs_str = f"{r['current_sigma_pct']:.3g}" if r['current_sigma_pct'] is not None else "n/a"
        fs_str = f"{r['future_sigma_pct']:.3g}" if r['future_sigma_pct'] else "n/a"
        sc_str = f"{r['score_current']:.2f}" if math.isfinite(r['score_current']) else "n/a"
        sf_str = f"{r['score_future']:.2f}" if r['score_future'] else "n/a"
        print(f"  {r['domain']:<10s} {r['quantity'][:48]:<48s} "
              f"{r['sam_value']:>14.6g} {r['standard_value']:>14.6g} "
              f"{r['gap_pct']:>8.3f} {cs_str:>8s} {fs_str:>8s} "
              f"{sc_str:>7s} {sf_str:>7s}  {r['status']}")
    print()

    # Group by status
    by_status = {}
    for r in enriched:
        by_status.setdefault(r["status"], []).append(r)

    print("=" * 78)
    print("RANKED BY STATUS")
    print("=" * 78)
    for status in ["ALREADY DISCRIMINATING", "FUTURE-TESTABLE", "MARGINAL",
                   "ALREADY TESTED PASS", "BELOW MEASUREMENT FLOOR"]:
        group = by_status.get(status, [])
        if not group:
            continue
        print()
        print(f"--- {status} ({len(group)} rows) ---")
        # rank by score_future descending within each group
        for r in sorted(group, key=lambda x: -x["score_future"]):
            print(f"  [{r['domain']:>9s}] {r['quantity']:<46s} | "
                  f"gap {r['gap_pct']:.3f}% vs fut σ {r['future_sigma_pct'] or 0:.2f}% "
                  f"({r['future_detector']}, {r['timeline']})")

    print()
    print("=" * 78)
    print("TOP SAM-1919 CANDIDATES (FUTURE-TESTABLE, ranked by score_future)")
    print("=" * 78)
    future_testable = sorted(by_status.get("FUTURE-TESTABLE", []),
                             key=lambda x: -x["score_future"])
    for i, r in enumerate(future_testable[:10], start=1):
        print(f"\n#{i}: {r['quantity']}")
        print(f"     SAM         = {r['sam_value']:.6g}  ({r['sam_form']})")
        print(f"     {r['std_label']:<11s} = {r['standard_value']:.6g}")
        print(f"     gap         = {r['gap_pct']:.3f}%")
        print(f"     current σ   = {r['current_sigma_pct']}%")
        print(f"     future σ    = {r['future_sigma_pct']}%  ({r['future_detector']}, {r['timeline']})")
        print(f"     score future = {r['score_future']:.2f}  (>3 = clean test)")

    # Verdict = clean table generation
    verdict = "PASS"   # synthesis CR; output is the table

    # ===== Outputs =====
    csv_path = os.path.join(HERE, "CR004_discrimination_map.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "quantity", "sam_form", "sam_value",
                    "standard_value", "std_label", "gap_abs", "gap_pct",
                    "current_sigma_pct", "future_sigma_pct",
                    "future_detector", "timeline",
                    "score_current", "score_future", "status"])
        for r in enriched:
            w.writerow([r["domain"], r["quantity"], r["sam_form"],
                        r["sam_value"], r["standard_value"], r["std_label"],
                        r["gap_abs"], r["gap_pct"],
                        r["current_sigma_pct"], r["future_sigma_pct"],
                        r["future_detector"], r["timeline"],
                        r["score_current"], r["score_future"], r["status"]])

    summary = {
        "artifact": "CR004_SAM_VS_GR_DISCRIMINATION_MAP",
        "mode": "EXPLORATORY",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "rows_tabulated": len(enriched),
        "by_status": {k: len(v) for k, v in by_status.items()},
        "top_future_testable": [
            {
                "rank": i,
                "quantity": r["quantity"],
                "sam_form": r["sam_form"],
                "sam_value": r["sam_value"],
                "standard_value": r["standard_value"],
                "gap_pct": r["gap_pct"],
                "future_detector": r["future_detector"],
                "future_sigma_pct": r["future_sigma_pct"],
                "score_future": r["score_future"],
                "timeline": r["timeline"],
            }
            for i, r in enumerate(future_testable[:10], start=1)
        ],
    }
    with open(os.path.join(HERE, "CR004_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print()
    print(f"CR004 VERDICT: {verdict}")
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
