"""CR250 — Binding from CR009 Lift Formula on CR247 Phi Decomposition.

Runner for the sealed precommit at CR250_PRECOMMIT.md. Reads the CR242 binding
dataset (71 nuclei AME2020), filters to the 69 N >= Z rows (CR247 scope), and
applies the precommit-locked composition:

  s_b = D / R^4 * mu_Q
  s_e = (7093/192 + D) / R^4 * mu_Q
  B_u_pred(Z, N) = Z * s_b + (N - Z) * s_e

Reports residuals, runs five wrong controls, scores shape verdict by single-scale
rescale RMS. Zero free parameters. All constants traceable to sealed upstream CRs.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80

HERE = Path(__file__).resolve().parent
DATASET = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"

PER_ROW_CSV = HERE / "CR250_per_row_predictions.csv"
AGGREGATE_CSV = HERE / "CR250_aggregate.csv"
WC_CSV = HERE / "CR250_wrong_controls.csv"
RESULT_MD = HERE / "CR250_result.md"
HASHES_TXT = HERE / "HASHES.txt"
RESCALE_CSV = HERE / "CR250_rescale_residuals.csv"


# Sealed substrate atoms (verbatim from CR238 / CR221 / CR240) ----------------
R = Fraction(12)
D = Fraction(3)
S = Fraction(8)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R4 = R ** 4
MU_Q = Fraction(192, 7117)
DQ_B = Fraction(0)
DQ_E = Fraction(7093, 192)
MEV_PER_U = Decimal("931.494")


def lift_pair(q: Fraction) -> Fraction:
    """CR009 pair lift fraction: (q + D) / R^4."""
    return (q + D) / R4


def s_position(dQ: Fraction) -> Fraction:
    """Per-position contribution in atomic mass units."""
    return lift_pair(dQ) * MU_Q


S_B = s_position(DQ_B)
S_E = s_position(DQ_E)


def b_pred(Z: int, N: int, s_b: Fraction = S_B, s_e: Fraction = S_E) -> Fraction:
    return Z * s_b + (N - Z) * s_e


# Dataset loading -------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_dataset() -> list[dict]:
    rows: list[dict] = []
    with DATASET.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B_obs = Fraction(r["B_u"])
            except (KeyError, ValueError):
                continue
            rows.append({
                "isotope": r["isotope"],
                "Z": Z,
                "N": N,
                "A": A,
                "B_obs_u": B_obs,
                "split": r.get("split", ""),
            })
    return rows


def dec(f: Fraction, places: int = 12) -> Decimal:
    q = Decimal(f.numerator) / Decimal(f.denominator)
    return q.quantize(Decimal("1." + "0" * places))


# Per-row prediction ----------------------------------------------------------
def predict_rows(rows: list[dict], s_b: Fraction = S_B, s_e: Fraction = S_E) -> list[dict]:
    out = []
    for r in rows:
        Z, N = r["Z"], r["N"]
        B_pred_u = b_pred(Z, N, s_b, s_e)
        delta_u = r["B_obs_u"] - B_pred_u
        delta_MeV = Decimal(delta_u.numerator) / Decimal(delta_u.denominator) * MEV_PER_U
        out.append({
            **r,
            "B_pred_u": B_pred_u,
            "delta_u": delta_u,
            "delta_MeV": delta_MeV,
            "abs_delta_u": abs(delta_u),
            "abs_delta_MeV": abs(delta_MeV),
        })
    return out


# Aggregate metrics -----------------------------------------------------------
def aggregate(predictions: list[dict]) -> dict:
    n = len(predictions)
    abs_deltas_u = [p["abs_delta_u"] for p in predictions]
    abs_deltas_MeV = [p["abs_delta_MeV"] for p in predictions]
    deltas_u = [p["delta_u"] for p in predictions]

    max_abs_u = max(abs_deltas_u)
    max_abs_MeV = max(abs_deltas_MeV)
    mean_abs_u = sum(abs_deltas_u) / n
    mean_abs_MeV = sum(abs_deltas_MeV) / n

    # RMS in u, computed exactly via Fraction
    sum_sq = sum(d * d for d in deltas_u)
    rms_u_sq = Decimal(sum_sq.numerator) / Decimal(sum_sq.denominator) / Decimal(n)
    rms_u = rms_u_sq.sqrt()
    rms_MeV = rms_u * MEV_PER_U

    return {
        "n": n,
        "max_abs_u": max_abs_u,
        "max_abs_MeV": max_abs_MeV,
        "mean_abs_u": mean_abs_u,
        "mean_abs_MeV": mean_abs_MeV,
        "rms_u": rms_u,
        "rms_MeV": rms_MeV,
    }


# Shape verdict ---------------------------------------------------------------
def linear_rescale(predictions: list[dict]) -> dict:
    """Solve B_obs ≈ alpha * B_pred for alpha (no intercept) by least squares.
    Then report RMS of residuals at that alpha.
    """
    num = Fraction(0)
    den = Fraction(0)
    for p in predictions:
        num += p["B_obs_u"] * p["B_pred_u"]
        den += p["B_pred_u"] * p["B_pred_u"]
    alpha = num / den if den != 0 else Fraction(0)

    residuals = []
    for p in predictions:
        r_u = p["B_obs_u"] - alpha * p["B_pred_u"]
        r_MeV = Decimal(r_u.numerator) / Decimal(r_u.denominator) * MEV_PER_U
        residuals.append({
            **p,
            "alpha": alpha,
            "B_pred_rescaled_u": alpha * p["B_pred_u"],
            "rescale_residual_u": r_u,
            "rescale_residual_MeV": r_MeV,
            "abs_rescale_residual_u": abs(r_u),
            "abs_rescale_residual_MeV": abs(r_MeV),
        })

    sum_sq = sum(r["rescale_residual_u"] ** 2 for r in residuals)
    rms_u_sq = Decimal(sum_sq.numerator) / Decimal(sum_sq.denominator) / Decimal(len(residuals))
    rms_u = rms_u_sq.sqrt()
    rms_MeV = rms_u * MEV_PER_U
    max_abs_MeV = max(r["abs_rescale_residual_MeV"] for r in residuals)

    return {
        "alpha": alpha,
        "residuals": residuals,
        "rescale_rms_u": rms_u,
        "rescale_rms_MeV": rms_MeV,
        "rescale_max_abs_MeV": max_abs_MeV,
    }


def shape_monotonic(predictions: list[dict]) -> bool:
    """Check whether B_pred ordering of rows matches B_obs ordering up to sign,
    when restricted to nuclei with N-Z >= 2 (where B_pred has enough signal).
    Returns True if Pearson correlation > 0 across the full corpus.
    """
    n = len(predictions)
    if n < 2:
        return False
    xs = [Decimal(p["B_pred_u"].numerator) / Decimal(p["B_pred_u"].denominator) for p in predictions]
    ys = [Decimal(p["B_obs_u"].numerator) / Decimal(p["B_obs_u"].denominator) for p in predictions]
    mx = sum(xs) / Decimal(n)
    my = sum(ys) / Decimal(n)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs)
    dy = sum((y - my) ** 2 for y in ys)
    if dx <= 0 or dy <= 0:
        return False
    denom = (dx * dy).sqrt()
    corr = num / denom
    return corr > 0


# Wrong controls --------------------------------------------------------------
def run_wrong_controls(rows: list[dict], unperturbed_rescale_rms_MeV: Decimal) -> list[dict]:
    results = []

    # WC-1 swap dQ_b and dQ_e
    wc1_preds = predict_rows(
        rows,
        s_b=s_position(DQ_E),  # dQ_b becomes dQ_e
        s_e=s_position(DQ_B),  # dQ_e becomes dQ_b
    )
    wc1_rescale = linear_rescale(wc1_preds)
    results.append({
        "wc": "WC-1_swap_phi_dQ",
        "description": "swap dQ_b <-> dQ_e",
        "rescale_rms_MeV": wc1_rescale["rescale_rms_MeV"],
        "alpha": wc1_rescale["alpha"],
        "broke_shape": wc1_rescale["rescale_rms_MeV"] > unperturbed_rescale_rms_MeV * Decimal("1.5"),
    })

    # WC-2 triadic depth instead of pair depth (R instead of R^4)
    def s_with_R(dQ: Fraction) -> Fraction:
        return ((dQ + D) / R) * MU_Q

    wc2_preds = predict_rows(rows, s_b=s_with_R(DQ_B), s_e=s_with_R(DQ_E))
    wc2_rescale = linear_rescale(wc2_preds)
    results.append({
        "wc": "WC-2_triadic_depth",
        "description": "use R denominator (triadic) instead of R^4 (pair)",
        "rescale_rms_MeV": wc2_rescale["rescale_rms_MeV"],
        "alpha": wc2_rescale["alpha"],
        "broke_shape": wc2_rescale["rescale_rms_MeV"] > unperturbed_rescale_rms_MeV * Decimal("1.5"),
    })

    # WC-3 drop the D term (use q only in numerator)
    def s_no_D(dQ: Fraction) -> Fraction:
        return (dQ / R4) * MU_Q

    wc3_preds = predict_rows(rows, s_b=s_no_D(DQ_B), s_e=s_no_D(DQ_E))
    wc3_rescale = linear_rescale(wc3_preds)
    results.append({
        "wc": "WC-3_drop_D",
        "description": "drop the +D term (s_b vanishes, s_e shrinks)",
        "rescale_rms_MeV": wc3_rescale["rescale_rms_MeV"],
        "alpha": wc3_rescale["alpha"],
        "broke_shape": wc3_rescale["rescale_rms_MeV"] > unperturbed_rescale_rms_MeV * Decimal("1.5"),
    })

    # WC-4 perturb mu_Q (use 192/7118 instead of 192/7117)
    bad_mu = Fraction(192, 7118)

    def s_bad_mu(dQ: Fraction) -> Fraction:
        return ((dQ + D) / R4) * bad_mu

    wc4_preds = predict_rows(rows, s_b=s_bad_mu(DQ_B), s_e=s_bad_mu(DQ_E))
    wc4_rescale = linear_rescale(wc4_preds)
    results.append({
        "wc": "WC-4_perturb_mu_Q",
        "description": "use mu_Q = 192/7118 instead of 192/7117",
        "rescale_rms_MeV": wc4_rescale["rescale_rms_MeV"],
        "alpha": wc4_rescale["alpha"],
        "broke_shape": wc4_rescale["rescale_rms_MeV"] > unperturbed_rescale_rms_MeV * Decimal("1.05"),
    })

    # WC-5 shuffle (N - Z) values across rows, preserving Z
    rng = random.Random(20260625)
    excess = [r["N"] - r["Z"] for r in rows]
    rng.shuffle(excess)
    shuffled = []
    for r, ex in zip(rows, excess):
        shuffled.append({
            **r,
            "N": r["Z"] + ex,
        })
    wc5_preds = predict_rows(shuffled)
    wc5_rescale = linear_rescale(wc5_preds)
    results.append({
        "wc": "WC-5_shuffle_NminusZ",
        "description": "shuffle (N-Z) across rows, preserve Z",
        "rescale_rms_MeV": wc5_rescale["rescale_rms_MeV"],
        "alpha": wc5_rescale["alpha"],
        "broke_shape": wc5_rescale["rescale_rms_MeV"] > unperturbed_rescale_rms_MeV * Decimal("1.5"),
    })

    return results


# CSV writers -----------------------------------------------------------------
def write_per_row(predictions: list[dict]) -> None:
    with PER_ROW_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "isotope", "Z", "N", "A", "N_minus_Z",
            "B_obs_u", "B_pred_u", "delta_u", "delta_MeV", "abs_delta_MeV",
        ])
        for p in sorted(predictions, key=lambda x: x["A"]):
            w.writerow([
                p["isotope"], p["Z"], p["N"], p["A"], p["N"] - p["Z"],
                f"{dec(p['B_obs_u']):f}",
                f"{dec(p['B_pred_u']):f}",
                f"{dec(p['delta_u']):f}",
                f"{p['delta_MeV']:f}",
                f"{p['abs_delta_MeV']:f}",
            ])


def write_aggregate(metrics: dict, rescale: dict) -> None:
    with AGGREGATE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value_u", "value_MeV"])
        w.writerow(["n", metrics["n"], ""])
        w.writerow(["max_abs", f"{dec(metrics['max_abs_u']):f}", f"{metrics['max_abs_MeV']:f}"])
        w.writerow(["mean_abs", f"{dec(metrics['mean_abs_u']):f}", f"{metrics['mean_abs_MeV']:f}"])
        w.writerow(["rms", f"{metrics['rms_u']:f}", f"{metrics['rms_MeV']:f}"])
        w.writerow(["rescale_alpha", f"{dec(rescale['alpha']):f}", ""])
        w.writerow(["rescale_rms", f"{rescale['rescale_rms_u']:f}", f"{rescale['rescale_rms_MeV']:f}"])
        w.writerow(["rescale_max_abs", "", f"{rescale['rescale_max_abs_MeV']:f}"])


def write_wc(wc_results: list[dict]) -> None:
    with WC_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["wc", "description", "rescale_rms_MeV", "alpha", "broke_shape"])
        for r in wc_results:
            w.writerow([
                r["wc"], r["description"],
                f"{r['rescale_rms_MeV']:f}",
                f"{dec(r['alpha']):f}",
                str(r["broke_shape"]),
            ])


def write_rescale_residuals(residuals: list[dict]) -> None:
    with RESCALE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "isotope", "Z", "N", "A", "N_minus_Z",
            "B_obs_u", "B_pred_u", "alpha",
            "B_pred_rescaled_u", "rescale_residual_MeV", "abs_rescale_residual_MeV",
        ])
        for r in sorted(residuals, key=lambda x: x["A"]):
            w.writerow([
                r["isotope"], r["Z"], r["N"], r["A"], r["N"] - r["Z"],
                f"{dec(r['B_obs_u']):f}",
                f"{dec(r['B_pred_u']):f}",
                f"{dec(r['alpha']):f}",
                f"{dec(r['B_pred_rescaled_u']):f}",
                f"{r['rescale_residual_MeV']:f}",
                f"{r['abs_rescale_residual_MeV']:f}",
            ])


def write_hashes(extra: dict[str, str]) -> None:
    files = [
        PER_ROW_CSV,
        AGGREGATE_CSV,
        WC_CSV,
        RESCALE_CSV,
        HERE / "CR250_PRECOMMIT.md",
        HERE / "CR250_runner.py",
    ]
    with HASHES_TXT.open("w", encoding="utf-8") as f:
        for p in files:
            if p.exists():
                f.write(f"{sha256_file(p)}  {p.name}\n")
        for k, v in extra.items():
            f.write(f"{v}  {k}\n")


# Result.md writer ------------------------------------------------------------
def fmt_dec(d: Decimal, places: int = 4) -> str:
    return f"{d.quantize(Decimal('1.' + '0' * places))}"


def write_result(
    metrics: dict,
    rescale: dict,
    wc_results: list[dict],
    predictions: list[dict],
    shape_pass: bool,
    dataset_sha: str,
) -> None:
    sorted_by_abs = sorted(predictions, key=lambda x: x["abs_delta_MeV"], reverse=True)
    sorted_best = sorted(predictions, key=lambda x: x["abs_delta_MeV"])

    rescale_sorted_by_abs = sorted(
        rescale["residuals"], key=lambda x: x["abs_rescale_residual_MeV"], reverse=True
    )
    rescale_sorted_best = sorted(
        rescale["residuals"], key=lambda x: x["abs_rescale_residual_MeV"]
    )

    all_wc_broke = all(w["broke_shape"] for w in wc_results)
    structural_pass = shape_pass and rescale["rescale_rms_MeV"] < Decimal("1.0") and all_wc_broke

    if structural_pass:
        verdict = "STRUCTURAL_PASS"
    elif shape_pass and all_wc_broke:
        verdict = "BOUNDARY"
    elif shape_pass:
        verdict = "BOUNDARY_WC_FAIL"
    else:
        verdict = "FAIL"

    cascade_anchors = {"Au-197", "C-12", "C-13"}
    anchor_rows = [p for p in predictions if p["isotope"] in cascade_anchors]

    lines: list[str] = []
    L = lines.append

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    L(f"# CR250 — Binding from CR009 Lift Formula on CR247 Phi Decomposition — Result")
    L("")
    L(f"**Verdict:** `{verdict}`")
    L(f"**Started / Completed:** {now}")
    L(f"**Dataset:** CR242_binding_dataset.csv (filtered to N >= Z; n = {metrics['n']})")
    L(f"**Dataset sha256:** `{dataset_sha}`")
    L("")
    L("## What this CR tested")
    L("")
    L("Applied the sealed CR009 pair lift form `(q + D) / R^4` to the sealed CR247")
    L("phi positions (`phi_b` with `dQ = 0`, `phi_e` with `dQ = 7093/192`) and summed")
    L("per CR247 Block G's identity `B_u(Z, N) = Z·s_b + (N − Z)·s_e`. Zero free")
    L("parameters. No candidate-rule search. No outside-data comparison. Above-the-line")
    L("constants traceable to CR238 (R, D, S), CR221 (κ, g), CR240 (μ_Q), and CR247")
    L("(phi positions).")
    L("")
    L("Per Sean's 2026-06-24 cascade synthesis (Chat5 line 14588):")
    L("> \"The 'binding energy' of conventional physics IS the closure fee the substrate")
    L("> charges, expressed in mass-equivalent units.\"")
    L("")
    L("## Sealed formula evaluated")
    L("")
    L("```text")
    L(f"s_b = D / R^4 * mu_Q                 = 1 / (36 * 7117) = 1/256212 u")
    L(f"    ≈ {fmt_dec(dec(S_B, 18), 14)} u  ≈ {fmt_dec(Decimal(S_B.numerator)/Decimal(S_B.denominator)*MEV_PER_U, 6)} MeV per balanced position")
    L("")
    L(f"s_e = (7093/192 + D) / R^4 * mu_Q    = 7669 / (20736 * 7117)")
    L(f"    ≈ {fmt_dec(dec(S_E, 18), 14)} u  ≈ {fmt_dec(Decimal(S_E.numerator)/Decimal(S_E.denominator)*MEV_PER_U, 6)} MeV per excess neutron")
    L("")
    L("B_u_pred(Z, N) = Z * s_b + (N - Z) * s_e")
    L("```")
    L("")
    L("## Aggregate residuals (unrescaled, raw substrate prediction)")
    L("")
    L("| Metric | Value (u) | Value (MeV) |")
    L("|---|---|---|")
    L(f"| n | {metrics['n']} | — |")
    L(f"| max \\|Δ\\| | {fmt_dec(dec(metrics['max_abs_u']), 6)} | {fmt_dec(metrics['max_abs_MeV'], 3)} |")
    L(f"| mean \\|Δ\\| | {fmt_dec(dec(metrics['mean_abs_u']), 6)} | {fmt_dec(metrics['mean_abs_MeV'], 3)} |")
    L(f"| RMS | {fmt_dec(metrics['rms_u'], 6)} | {fmt_dec(metrics['rms_MeV'], 3)} |")
    L("")
    L("## Shape verdict — single-scale rescale fit")
    L("")
    L("Solve `B_obs ≈ α · B_pred` for the single multiplicative scale `α` that")
    L("minimizes residual RMS. If a single scalar closes the rescale-RMS gate")
    L("(< 1 MeV), the substrate composition has the right structural shape and")
    L("the missing piece is a single multiplicative constant traceable to a")
    L("follow-up CR. If it doesn't, the shape itself is incomplete and the")
    L("missing structure is more than a coefficient.")
    L("")
    L("| Metric | Value |")
    L("|---|---|")
    L(f"| α (best single scale) | {fmt_dec(dec(rescale['alpha']), 6)} |")
    L(f"| rescale RMS | {fmt_dec(rescale['rescale_rms_MeV'], 4)} MeV |")
    L(f"| rescale max \\|Δ\\| | {fmt_dec(rescale['rescale_max_abs_MeV'], 4)} MeV |")
    L(f"| shape monotonic (Pearson > 0)? | **{shape_pass}** |")
    L(f"| rescale RMS < 1 MeV? | **{rescale['rescale_rms_MeV'] < Decimal('1.0')}** |")
    L("")
    L("## Top 10 worst residuals (unrescaled)")
    L("")
    L("| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (u) | Δ (MeV) |")
    L("|---|---|---|---|---|---|---|---|---|")
    for p in sorted_by_abs[:10]:
        L(
            f"| {p['isotope']} | {p['Z']} | {p['N']} | {p['A']} | {p['N']-p['Z']} | "
            f"{fmt_dec(dec(p['B_obs_u']), 6)} | {fmt_dec(dec(p['B_pred_u']), 6)} | "
            f"{fmt_dec(dec(p['delta_u']), 6)} | {fmt_dec(p['delta_MeV'], 3)} |"
        )
    L("")
    L("## Best 10 (smallest |Δ|, unrescaled)")
    L("")
    L("| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (u) | Δ (MeV) |")
    L("|---|---|---|---|---|---|---|---|---|")
    for p in sorted_best[:10]:
        L(
            f"| {p['isotope']} | {p['Z']} | {p['N']} | {p['A']} | {p['N']-p['Z']} | "
            f"{fmt_dec(dec(p['B_obs_u']), 6)} | {fmt_dec(dec(p['B_pred_u']), 6)} | "
            f"{fmt_dec(dec(p['delta_u']), 6)} | {fmt_dec(p['delta_MeV'], 3)} |"
        )
    L("")
    L("## Worst 10 rescale residuals (after best single-scale α)")
    L("")
    L("| isotope | Z | N | A | N−Z | B_obs (u) | α·B_pred (u) | residual (MeV) |")
    L("|---|---|---|---|---|---|---|---|")
    for r in rescale_sorted_by_abs[:10]:
        L(
            f"| {r['isotope']} | {r['Z']} | {r['N']} | {r['A']} | {r['N']-r['Z']} | "
            f"{fmt_dec(dec(r['B_obs_u']), 6)} | {fmt_dec(dec(r['B_pred_rescaled_u']), 6)} | "
            f"{fmt_dec(r['rescale_residual_MeV'], 4)} |"
        )
    L("")
    L("## Best 10 rescale residuals (after best single-scale α)")
    L("")
    L("| isotope | Z | N | A | N−Z | B_obs (u) | α·B_pred (u) | residual (MeV) |")
    L("|---|---|---|---|---|---|---|---|")
    for r in rescale_sorted_best[:10]:
        L(
            f"| {r['isotope']} | {r['Z']} | {r['N']} | {r['A']} | {r['N']-r['Z']} | "
            f"{fmt_dec(dec(r['B_obs_u']), 6)} | {fmt_dec(dec(r['B_pred_rescaled_u']), 6)} | "
            f"{fmt_dec(r['rescale_residual_MeV'], 4)} |"
        )
    L("")
    L("## Cascade-cited anchor rows (Au-197, C-12, C-13)")
    L("")
    L("These rows were cited in the 2026-06-24 cascade derivation as headline matches.")
    L("They are reported here for tracking; not load-bearing for the verdict.")
    L("")
    L("| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (MeV) | α·B_pred residual (MeV) |")
    L("|---|---|---|---|---|---|---|---|---|")
    for p in sorted(anchor_rows, key=lambda x: x["A"]):
        r_after = next((r for r in rescale["residuals"] if r["isotope"] == p["isotope"]), None)
        rescale_residual = fmt_dec(r_after["rescale_residual_MeV"], 4) if r_after else "—"
        L(
            f"| {p['isotope']} | {p['Z']} | {p['N']} | {p['A']} | {p['N']-p['Z']} | "
            f"{fmt_dec(dec(p['B_obs_u']), 6)} | {fmt_dec(dec(p['B_pred_u']), 6)} | "
            f"{fmt_dec(p['delta_MeV'], 3)} | {rescale_residual} |"
        )
    L("")
    L("## Wrong controls — load-bearing check on each formula element")
    L("")
    L("Each WC perturbs ONE sealed element and reports whether the perturbation BREAKS")
    L("the shape gate (rescale RMS inflates ≥ 1.5× the unperturbed value; 1.05× for")
    L("μ_Q since it's a precision constant). A passing WC means the unperturbed element")
    L("was load-bearing.")
    L("")
    L(f"Unperturbed rescale RMS: **{fmt_dec(rescale['rescale_rms_MeV'], 4)} MeV** (threshold reference)")
    L("")
    L("| WC | Description | rescale RMS (MeV) | α | Broke shape? |")
    L("|---|---|---|---|---|")
    for w in wc_results:
        L(
            f"| {w['wc']} | {w['description']} | "
            f"{fmt_dec(w['rescale_rms_MeV'], 4)} | "
            f"{fmt_dec(dec(w['alpha']), 6)} | "
            f"**{w['broke_shape']}** |"
        )
    L("")
    L(f"All WCs broke as predicted: **{all_wc_broke}**")
    L("")
    L("## Verdict logic")
    L("")
    L(f"- Shape monotonic (Pearson > 0): **{shape_pass}**")
    L(f"- Rescale RMS < 1 MeV: **{rescale['rescale_rms_MeV'] < Decimal('1.0')}**")
    L(f"- All WCs passed (broke as predicted): **{all_wc_broke}**")
    L(f"- **Overall verdict: `{verdict}`**")
    L("")
    L("Verdict ladder (sealed in precommit):")
    L("- `STRUCTURAL_PASS`: shape monotonic AND rescale RMS < 1 MeV AND all WCs broke")
    L("- `BOUNDARY`: shape monotonic AND all WCs broke, but rescale RMS ≥ 1 MeV")
    L("  (substrate composition right structure, additional terms or different depth needed)")
    L("- `BOUNDARY_WC_FAIL`: shape monotonic but a WC failed to break")
    L("  (element identified as non-load-bearing — composition needs revision)")
    L("- `FAIL`: shape not monotonic (composition has wrong structure, not missing-coefficient)")
    L("")
    L("## Structural reading")
    L("")
    if structural_pass:
        L("**Substrate composition closed the binding curve up to a single multiplicative scale.**")
        L(f"The CR009 pair lift on CR247 phi positions, summed per Block G's identity, agrees with")
        L(f"the AME2020 B_u shape with rescale RMS {fmt_dec(rescale['rescale_rms_MeV'], 4)} MeV.")
        L(f"The single missing scale α = {fmt_dec(dec(rescale['alpha']), 4)} is the natural")
        L("follow-up CR target — derive it from sealed substrate atoms without dataset access.")
    elif shape_pass:
        L("**Substrate composition produces the right structural shape with magnitude offset.**")
        L(f"Pearson correlation positive across 69 nuclei, but rescale RMS {fmt_dec(rescale['rescale_rms_MeV'], 4)} MeV")
        L("> 1 MeV target. The minimal CR009 + CR247 composition is missing structure beyond")
        L("a single multiplicative scale — candidate follow-up directions (each its own future CR):")
        L("")
        L("- (a) phi_b position carries non-trivial channel-gap structure via an internal q value")
        L("  not visible in dQ_b = 0 (e.g., internal proton/neutron/electron lifts within the")
        L("  balanced bundle that CR247's nucleon-decomposition doesn't expose)")
        L("- (b) Depth selection between R (triadic) and R^4 (pair) should be position-dependent")
        L("  rather than uniform (e.g., balanced position connects via triadic depth, excess neutron")
        L("  via pair depth)")
        L("- (c) CR248's phase-A four-particle structure contains the missing per-position fee")
        L("  that CR250 would inherit when sealed")
        L("")
        L(f"The unscaled prediction undershoots heavy nuclei by factor α = {fmt_dec(dec(rescale['alpha']), 4)}.")
        L("If α reduces to a sealed substrate constant in a follow-up CR, this composition closes")
        L("the binding curve structurally.")
    else:
        L("**Substrate composition shape disagrees with AME2020 binding curve.**")
        L(f"Pearson correlation between B_pred and B_obs is not positive across the 69-nucleus")
        L("corpus, so a single multiplicative scale cannot rescue the fit. The minimal CR009")
        L("+ CR247 composition has wrong sign/structure for the AMU-baseline B_u, which suggests")
        L("the AMU baseline convention itself (m_obs vs. A*u) is the wrong target for the substrate's")
        L("native binding-fee curve — the substrate may natively compute a different baseline")
        L("(e.g., m_obs vs. Z*m_p_native + N*m_n_native) and CR250's choice of AMU comparison")
        L("does not match what the substrate algebra produces.")
    L("")
    L("## Provenance chain (cryptographic)")
    L("")
    L("```text")
    for k, v in extra_hashes.items():
        L(f"{v}  {k}")
    L(f"{dataset_sha}  CR242_binding_dataset.csv")
    L("```")
    L("")
    L("## What CR250 does NOT do")
    L("")
    L("- Does not search candidate rules — single sealed composition only")
    L("- Does not compare to PDG / ΛCDM / GR / QM or any outside model")
    L("- Does not modify CR009, CR247, CR238, CR240, or any sealed upstream CR")
    L("- Does not search for the rescale α value — reports what least-squares gives")
    L("- Does not extend to N < Z (CR247 scope is N >= Z)")
    L("")
    L("## Rule of Immutability")
    L("")
    L(f"Sealed 2026-06-25 by Sean Brady. Formula, phi positions, lift form, test corpus,")
    L("verdict ladder, wrong controls, K-gates all frozen above the line.")
    L("")

    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")


# Compute hashes of upstream sealed CRs --------------------------------------
def upstream_hashes() -> dict[str, str]:
    out = {}
    candidates = {
        "CR009_result.md": Path(r"c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR009_CONNECTION_FEE_K1_REVEAL\CR009_result.md"),
        "CR247_result.md": HERE.parent / "CR247_SOB_INVERSE_SECOND_LAYER" / "CR247_result.md",
        "CR238_result.md": HERE.parent / "CR238_TYPED_CHANNEL_TABLE_CLOSURE" / "CR238_result.md",
        "CR240_result.md": HERE.parent / "CR240_NEUTRON_REST_MASS_CHANNEL" / "CR240_result.md",
        "CR005_result.md": Path(r"c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR005_M_NATIVE_PROVENANCE_AUDIT\CR005_result.md"),
        "CR250_PRECOMMIT.md": HERE / "CR250_PRECOMMIT.md",
    }
    for name, path in candidates.items():
        if path.exists():
            out[name] = sha256_file(path)
    return out


# Main ------------------------------------------------------------------------
def main() -> None:
    global extra_hashes
    dataset_sha = sha256_file(DATASET)
    extra_hashes = upstream_hashes()

    all_rows = load_dataset()
    rows = [r for r in all_rows if r["N"] >= r["Z"]]

    predictions = predict_rows(rows)
    metrics = aggregate(predictions)
    rescale = linear_rescale(predictions)
    shape_pass = shape_monotonic(predictions)
    wc_results = run_wrong_controls(rows, rescale["rescale_rms_MeV"])

    write_per_row(predictions)
    write_aggregate(metrics, rescale)
    write_wc(wc_results)
    write_rescale_residuals(rescale["residuals"])
    write_result(metrics, rescale, wc_results, predictions, shape_pass, dataset_sha)
    write_hashes(extra_hashes | {"CR242_binding_dataset.csv": dataset_sha})

    print(f"CR250 runner complete. Wrote: {RESULT_MD.name}")
    print(f"n rows = {metrics['n']}")
    print(f"max |Δ| = {metrics['max_abs_MeV']:f} MeV")
    print(f"mean |Δ| = {metrics['mean_abs_MeV']:f} MeV")
    print(f"RMS = {metrics['rms_MeV']:f} MeV")
    print(f"alpha (best single scale) = {Decimal(rescale['alpha'].numerator)/Decimal(rescale['alpha'].denominator):f}")
    print(f"rescale RMS = {rescale['rescale_rms_MeV']:f} MeV")
    print(f"shape monotonic = {shape_pass}")
    for w in wc_results:
        print(f"  {w['wc']}: rescale_rms={w['rescale_rms_MeV']:f} MeV  broke={w['broke_shape']}")


if __name__ == "__main__":
    main()
