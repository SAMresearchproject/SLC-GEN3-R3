"""
CR249 runner — Binding as Substrate-Atom Connection-Fee Sum

Per CR249_PRECOMMIT.md: tests six candidate connection-counting rules
against the 71-nucleus CR242 binding dataset. Each rule predicts B_u
from substrate atoms with zero free parameters; runner reports max |Δ|
per rule against Sean's 0.005 MeV target.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80

ROOT = Path(r"C:\VS\The_Courtroom")
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR249_BINDING_AS_CONNECTION_FEE"
DATASET = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"

PRECOMMIT = OUT / "CR249_PRECOMMIT.md"
RUNNER = OUT / "CR249_runner.py"
PER_ROW = OUT / "CR249_per_row_predictions.csv"
RULE_COMP = OUT / "CR249_rule_comparison.csv"
WC_LOG = OUT / "CR249_wrong_controls.csv"
SUMMARY = OUT / "CR249_summary.json"
RESULT = OUT / "CR249_result.md"
HASHES = OUT / "HASHES.txt"

# Substrate atoms (Decimal for high-precision computation)
R = Decimal(12)
D = Decimal(3)
S = Decimal(8)
ALPHA_H = Decimal(2)
THETA = Decimal(18)
F_ATOM = Decimal(81)
V = Decimal(27)
M_CAP = Decimal(126)
L = Decimal(162)
KAPPA_NUM = Decimal(7117)
KAPPA_DEN = Decimal(768)
G_UNIT_DEN = Decimal(64)
MU_Q_NUM = Decimal(192)   # μ_Q = 192/7117 u
MU_Q_DEN = Decimal(7117)
R4 = R ** 4               # = 20736
MEV_PER_U = Decimal("931.494")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def to_dec(s: str) -> Decimal:
    return Decimal(str(s).strip())


# =================== Candidate rules ===================

def rule_R1_per_excess(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = (N-Z) · (F·S - 1 + D) / R^4 · μ_Q  in u"""
    NmZ = N - Z
    fee_per_excess = (F_ATOM * S - 1 + D) * MU_Q_NUM / (R4 * MU_Q_DEN)
    return NmZ * fee_per_excess


def rule_R2_per_A(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = A · D / R^4 · μ_Q  in u"""
    fee_per_nucleon = D * MU_Q_NUM / (R4 * MU_Q_DEN)
    return A * fee_per_nucleon


def rule_R3_per_pn_pair(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = Z·N · (1 + D) / R^4 · μ_Q  in u"""
    fee_per_pair = (Decimal(1) + D) * MU_Q_NUM / (R4 * MU_Q_DEN)
    return Z * N * fee_per_pair


def rule_R4_channel_gap(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = (N-Z) · 7093 / (7117 · R^4)  in u"""
    NmZ = N - Z
    return NmZ * Decimal(7093) / (KAPPA_NUM * R4)


def rule_R5_asymmetry_sq(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = (N-Z)^2 / A · 1/(R·D) · K_asym  in u
    K_asym = 7093^2 / 7117^2"""
    NmZ = N - Z
    K_asym = Decimal(7093) ** 2 / KAPPA_NUM ** 2
    return NmZ * NmZ / A * Decimal(1) / (R * D) * K_asym


def rule_R6_volume_plus_asym(Z: Decimal, N: Decimal, A: Decimal) -> Decimal:
    """B_u = R2 + R5  in u"""
    return rule_R2_per_A(Z, N, A) + rule_R5_asymmetry_sq(Z, N, A)


CANDIDATE_RULES = [
    ("R1_per_excess_neutron",     rule_R1_per_excess,        "(N-Z)·(F·S-1+D)/R^4·μ_Q"),
    ("R2_per_A_volume",            rule_R2_per_A,             "A·D/R^4·μ_Q"),
    ("R3_per_pn_pair",             rule_R3_per_pn_pair,       "Z·N·(1+D)/R^4·μ_Q"),
    ("R4_channel_gap_linear",      rule_R4_channel_gap,       "(N-Z)·7093/(7117·R^4)"),
    ("R5_asymmetry_squared",       rule_R5_asymmetry_sq,      "(N-Z)^2/A·1/(R·D)·7093^2/7117^2"),
    ("R6_volume_plus_asym_squared",rule_R6_volume_plus_asym,  "R2 + R5"),
]


# =================== Main analysis ===================

def load_dataset() -> list[dict]:
    rows = []
    with DATASET.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "isotope": row["isotope"],
                "Z": to_dec(row["Z"]),
                "N": to_dec(row["N"]),
                "A": to_dec(row["A"]),
                "N_minus_Z": to_dec(row["N_minus_Z"]),
                "B_u_obs": to_dec(row["B_u"]),
                "split": row["split"],
            })
    return rows


def apply_rule(rule_fn, rows: list[dict]) -> list[dict]:
    """Apply a candidate rule to every dataset row; return per-row deltas."""
    out = []
    for r in rows:
        try:
            pred = rule_fn(r["Z"], r["N"], r["A"])
        except Exception as e:
            pred = None
        if pred is None:
            out.append({"isotope": r["isotope"], "Z": r["Z"], "N": r["N"], "A": r["A"],
                          "B_u_obs_u": r["B_u_obs"], "B_u_pred_u": None,
                          "delta_u": None, "delta_MeV": None, "classification": "compute_error"})
            continue
        delta_u = r["B_u_obs"] - pred
        delta_MeV = delta_u * MEV_PER_U
        adm = abs(delta_MeV)
        if adm < Decimal("0.005"):
            cls = "exact_match"
        elif adm < Decimal("0.05"):
            cls = "close_match"
        elif adm < Decimal("0.5"):
            cls = "approximate_match"
        else:
            cls = "systematic_miss"
        out.append({"isotope": r["isotope"], "Z": r["Z"], "N": r["N"], "A": r["A"],
                      "B_u_obs_u": r["B_u_obs"], "B_u_pred_u": pred,
                      "delta_u": delta_u, "delta_MeV": delta_MeV, "abs_delta_MeV": abs(delta_MeV),
                      "classification": cls, "split": r["split"]})
    return out


def aggregate_rule_metrics(rule_name: str, formula: str, deltas: list[dict]) -> dict:
    valid = [d for d in deltas if d["delta_MeV"] is not None]
    if not valid:
        return {"rule": rule_name, "formula": formula, "n": 0,
                  "max_abs_MeV": None, "mean_abs_MeV": None, "rms_MeV": None,
                  "exact": 0, "close": 0, "approx": 0, "miss": 0}
    abs_devs = [abs(d["delta_MeV"]) for d in valid]
    sq_sum = sum(d["delta_MeV"] ** 2 for d in valid)
    rms = (sq_sum / Decimal(len(valid))).sqrt() if len(valid) > 0 else Decimal(0)
    cls_counts = Counter(d["classification"] for d in valid)
    return {
        "rule": rule_name,
        "formula": formula,
        "n": len(valid),
        "max_abs_MeV": max(abs_devs),
        "mean_abs_MeV": sum(abs_devs) / Decimal(len(valid)),
        "rms_MeV": rms,
        "exact_match": cls_counts.get("exact_match", 0),
        "close_match": cls_counts.get("close_match", 0),
        "approximate_match": cls_counts.get("approximate_match", 0),
        "systematic_miss": cls_counts.get("systematic_miss", 0),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"[step 1] loading {DATASET.name} ...")
    rows = load_dataset()
    print(f"        loaded {len(rows)} nuclei")

    print("[step 2] applying 6 candidate rules ...")
    all_per_row_records = []
    rule_metrics = []
    rule_deltas = {}
    for rule_name, rule_fn, formula in CANDIDATE_RULES:
        deltas = apply_rule(rule_fn, rows)
        rule_deltas[rule_name] = deltas
        metrics = aggregate_rule_metrics(rule_name, formula, deltas)
        rule_metrics.append(metrics)
        for d in deltas:
            rec = dict(d)
            rec["rule"] = rule_name
            all_per_row_records.append(rec)
        print(f"        {rule_name:35s} max|Δ|={metrics['max_abs_MeV']!s:>20s} MeV  "
                f"mean|Δ|={metrics['mean_abs_MeV']!s:>20s} MeV  "
                f"exact:{metrics['exact_match']}")

    # Write per-row predictions
    pr_fields = ["rule", "isotope", "Z", "N", "A", "split",
                  "B_u_obs_u", "B_u_pred_u", "delta_u", "delta_MeV", "abs_delta_MeV", "classification"]
    with PER_ROW.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pr_fields)
        w.writeheader()
        for rec in all_per_row_records:
            w.writerow({k: rec.get(k, "") for k in pr_fields})

    # Write rule comparison
    rc_fields = ["rule", "formula", "n", "max_abs_MeV", "mean_abs_MeV", "rms_MeV",
                  "exact_match", "close_match", "approximate_match", "systematic_miss"]
    with RULE_COMP.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rc_fields)
        w.writeheader()
        for m in rule_metrics:
            w.writerow({k: str(m.get(k, "")) for k in rc_fields})

    # Identify best rule by max |Δ|_MeV
    valid_metrics = [m for m in rule_metrics if m["max_abs_MeV"] is not None]
    best = min(valid_metrics, key=lambda m: m["max_abs_MeV"]) if valid_metrics else None
    print(f"\n[step 3] best rule: {best['rule'] if best else 'NONE'} "
            f"max|Δ|={best['max_abs_MeV'] if best else 'n/a'} MeV")

    # Wrong controls
    print("[step 4] wrong controls ...")
    wc_records = []

    # WC-1: shuffle B_u → Z,N mapping for best rule
    if best:
        rng = random.Random(20260624)
        shuffled_B = [r["B_u_obs"] for r in rows]
        rng.shuffle(shuffled_B)
        shuffled_rows = []
        for r, b in zip(rows, shuffled_B):
            sr = dict(r)
            sr["B_u_obs"] = b
            shuffled_rows.append(sr)
        rule_fn = dict([(n, f) for n, f, _ in CANDIDATE_RULES])[best["rule"]]
        shuffled_deltas = apply_rule(rule_fn, shuffled_rows)
        shuf_max = max((abs(d["delta_MeV"]) for d in shuffled_deltas if d["delta_MeV"] is not None), default=Decimal(0))
        ratio = shuf_max / best["max_abs_MeV"] if best["max_abs_MeV"] > 0 else Decimal("inf")
        wc1_pass = ratio >= Decimal(100) or best["max_abs_MeV"] < Decimal("1e-9")
        wc_records.append({"wc": "WC-1_shuffle_BZN", "passed": wc1_pass,
                              "shuffle_max_MeV": shuf_max, "best_max_MeV": best["max_abs_MeV"],
                              "ratio": ratio})

    # WC-2: perturb R = 10 in best rule
    if best:
        original_R = R
        # Create perturbed versions inline by overriding R locally
        def perturbed_rule_R(rule_name):
            def f(Z, N, A):
                # Re-eval rule with R=10
                # Easier: scale the formula by ratio of R_perturb^4 / R_actual^4 etc.
                # Just recompute by directly substituting
                R_p = Decimal(10)
                R4_p = R_p ** 4
                if rule_name == "R1_per_excess_neutron":
                    NmZ = N - Z
                    fee = (F_ATOM * S - 1 + D) * MU_Q_NUM / (R4_p * MU_Q_DEN)
                    return NmZ * fee
                elif rule_name == "R2_per_A_volume":
                    fee = D * MU_Q_NUM / (R4_p * MU_Q_DEN)
                    return A * fee
                elif rule_name == "R3_per_pn_pair":
                    fee = (Decimal(1) + D) * MU_Q_NUM / (R4_p * MU_Q_DEN)
                    return Z * N * fee
                elif rule_name == "R4_channel_gap_linear":
                    NmZ = N - Z
                    return NmZ * Decimal(7093) / (KAPPA_NUM * R4_p)
                elif rule_name == "R5_asymmetry_squared":
                    NmZ = N - Z
                    K_asym = Decimal(7093) ** 2 / KAPPA_NUM ** 2
                    return NmZ * NmZ / A * Decimal(1) / (R_p * D) * K_asym
                elif rule_name == "R6_volume_plus_asym_squared":
                    fee_v = D * MU_Q_NUM / (R4_p * MU_Q_DEN)
                    NmZ = N - Z
                    K_asym = Decimal(7093) ** 2 / KAPPA_NUM ** 2
                    return A * fee_v + NmZ * NmZ / A * Decimal(1) / (R_p * D) * K_asym
                return None
            return f

        pr2 = perturbed_rule_R(best["rule"])
        pr2_deltas = apply_rule(pr2, rows)
        pr2_max = max((abs(d["delta_MeV"]) for d in pr2_deltas if d["delta_MeV"] is not None), default=Decimal(0))
        ratio = pr2_max / best["max_abs_MeV"] if best["max_abs_MeV"] > 0 else Decimal("inf")
        wc2_pass = ratio >= Decimal(100) or best["max_abs_MeV"] < Decimal("1e-9")
        wc_records.append({"wc": "WC-2_perturb_R_10", "passed": wc2_pass,
                              "perturb_max_MeV": pr2_max, "best_max_MeV": best["max_abs_MeV"],
                              "ratio": ratio})

    # WC-3: perturb D = 2 in best rule
    if best:
        def perturbed_rule_D(rule_name):
            def f(Z, N, A):
                D_p = Decimal(2)
                if rule_name == "R1_per_excess_neutron":
                    NmZ = N - Z
                    fee = (F_ATOM * S - 1 + D_p) * MU_Q_NUM / (R4 * MU_Q_DEN)
                    return NmZ * fee
                elif rule_name == "R2_per_A_volume":
                    fee = D_p * MU_Q_NUM / (R4 * MU_Q_DEN)
                    return A * fee
                elif rule_name == "R3_per_pn_pair":
                    fee = (Decimal(1) + D_p) * MU_Q_NUM / (R4 * MU_Q_DEN)
                    return Z * N * fee
                elif rule_name == "R4_channel_gap_linear":
                    NmZ = N - Z
                    return NmZ * Decimal(7093) / (KAPPA_NUM * R4)
                elif rule_name == "R5_asymmetry_squared":
                    NmZ = N - Z
                    K_asym = Decimal(7093) ** 2 / KAPPA_NUM ** 2
                    return NmZ * NmZ / A * Decimal(1) / (R * D_p) * K_asym
                elif rule_name == "R6_volume_plus_asym_squared":
                    fee_v = D_p * MU_Q_NUM / (R4 * MU_Q_DEN)
                    NmZ = N - Z
                    K_asym = Decimal(7093) ** 2 / KAPPA_NUM ** 2
                    return A * fee_v + NmZ * NmZ / A * Decimal(1) / (R * D_p) * K_asym
                return None
            return f

        pr3 = perturbed_rule_D(best["rule"])
        pr3_deltas = apply_rule(pr3, rows)
        pr3_max = max((abs(d["delta_MeV"]) for d in pr3_deltas if d["delta_MeV"] is not None), default=Decimal(0))
        ratio = pr3_max / best["max_abs_MeV"] if best["max_abs_MeV"] > 0 else Decimal("inf")
        wc3_pass = ratio >= Decimal(100) or best["max_abs_MeV"] < Decimal("1e-9")
        wc_records.append({"wc": "WC-3_perturb_D_2", "passed": wc3_pass,
                              "perturb_max_MeV": pr3_max, "best_max_MeV": best["max_abs_MeV"],
                              "ratio": ratio})

    # WC-4: substrate-atom integrity (assertions)
    wc4_checks = {
        "mu_Q = 192/7117": MU_Q_NUM / MU_Q_DEN == Decimal(192) / Decimal(7117),
        "R^4 = 20736": R4 == Decimal(20736),
        "F·S - 1 = 647": F_ATOM * S - 1 == Decimal(647),
        "kappa = 7117/768": KAPPA_NUM / KAPPA_DEN == Decimal(7117) / Decimal(768),
    }
    wc4_pass = all(wc4_checks.values())
    wc_records.append({"wc": "WC-4_substrate_atom_integrity", "passed": wc4_pass,
                          "checks": wc4_checks})

    with WC_LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wc", "passed", "observed"])
        for wcr in wc_records:
            w.writerow([wcr["wc"], wcr["passed"], json.dumps({k: str(v) for k, v in wcr.items()})])

    # Verdict
    if best is None:
        verdict = "FAIL"
    elif best["max_abs_MeV"] < Decimal("0.005") and all(wcr["passed"] for wcr in wc_records):
        verdict = "PASS"
    elif best["max_abs_MeV"] < Decimal("0.05"):
        verdict = "BOUNDARY"
    elif best["max_abs_MeV"] < Decimal("0.5"):
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    summary = {
        "cr_id": "CR249",
        "title": "Binding as Substrate-Atom Connection-Fee Sum",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict_class": verdict,
        "dataset_rows": len(rows),
        "best_rule": best["rule"] if best else None,
        "best_max_abs_MeV": str(best["max_abs_MeV"]) if best else None,
        "best_mean_abs_MeV": str(best["mean_abs_MeV"]) if best else None,
        "best_rms_MeV": str(best["rms_MeV"]) if best else None,
        "target_max_MeV": "0.005",
        "rule_comparison": [{k: (str(v) if isinstance(v, Decimal) else v) for k, v in m.items()} for m in rule_metrics],
        "wrong_controls": [{"wc": r["wc"], "passed": r["passed"]} for r in wc_records],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    # Rich result.md
    def fmt_dec(v, n=4):
        if v is None:
            return "n/a"
        try:
            d = Decimal(str(v))
            if d == 0:
                return "0"
            return format(d, f".{n}g")
        except Exception:
            return str(v)[:20]

    parts = []
    parts.append("# CR249 Binding as Substrate-Atom Connection-Fee Sum — Result")
    parts.append("")
    parts.append(f"**Verdict:** `{verdict}`")
    parts.append(f"**Started:** {summary['started_at_utc']}")
    parts.append(f"**Completed:** {summary['completed_at_utc']}")
    parts.append(f"**Dataset:** CR242_binding_dataset.csv ({len(rows)} nuclei)")
    parts.append(f"**Best rule:** `{best['rule'] if best else 'NONE'}`")
    parts.append(f"**Best max |Δ|:** {fmt_dec(best['max_abs_MeV']) if best else 'n/a'} MeV "
                  f"(target: 0.005 MeV)")
    parts.append("")
    parts.append("## The question this CR answered")
    parts.append("")
    parts.append("Per Sean's 2026-06-24 framing: tensor carriers are substrate atoms that")
    parts.append("carry zero mass but produce a mass-lift, and the sum of these lifts across")
    parts.append("a nucleus's substrate-atom connections IS the binding curvature B_u.")
    parts.append("CR249 tests whether the connection-fee formula structure verified at the")
    parts.append("particle level by CR009 ((R+q+D)/R triadic, (q+D)/R⁴ pair) extends to")
    parts.append("derive B_u for all 71 nuclei in the CR242 binding dataset with zero free")
    parts.append("parameters and max |Δ| ≤ 0.005 MeV.")
    parts.append("")
    parts.append("## Candidate rules tested (all locked above the line)")
    parts.append("")
    parts.append("| Rule | Formula |")
    parts.append("|---|---|")
    for n, _, f in CANDIDATE_RULES:
        parts.append(f"| `{n}` | `{f}` |")
    parts.append("")
    parts.append("All formulas use only CR238 substrate atoms and named derived rationals.")
    parts.append("Zero fitted parameters in any rule.")
    parts.append("")
    parts.append("## Rule-by-rule comparison")
    parts.append("")
    parts.append("| Rule | n | max |Δ| MeV | mean |Δ| MeV | RMS MeV | exact | close | approx | miss |")
    parts.append("|---|---|---|---|---|---|---|---|---|")
    for m in rule_metrics:
        parts.append(f"| {m['rule']} | {m['n']} | {fmt_dec(m['max_abs_MeV'])} | "
                       f"{fmt_dec(m['mean_abs_MeV'])} | {fmt_dec(m['rms_MeV'])} | "
                       f"{m['exact_match']} | {m['close_match']} | "
                       f"{m['approximate_match']} | {m['systematic_miss']} |")
    parts.append("")
    parts.append(f"**Sean's target ceiling:** max |Δ| ≤ 0.005 MeV across all 71 nuclei.")
    parts.append("")
    parts.append("## Best rule — per-nucleus detail")
    parts.append("")
    if best:
        best_deltas = sorted(rule_deltas[best["rule"]],
                              key=lambda d: abs(d["delta_MeV"]) if d["delta_MeV"] is not None else Decimal(0),
                              reverse=True)
        parts.append(f"Best: **`{best['rule']}`** — formula `{best['formula']}`")
        parts.append("")
        parts.append("**Top 10 worst residuals (descending |Δ|):**")
        parts.append("")
        parts.append("| isotope | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (u) | Δ (MeV) | class |")
        parts.append("|---|---|---|---|---|---|---|---|---|")
        for d in best_deltas[:10]:
            parts.append(f"| {d['isotope']} | {d['Z']} | {d['N']} | {d['A']} | "
                           f"{fmt_dec(d['B_u_obs_u'], 6)} | {fmt_dec(d['B_u_pred_u'], 6)} | "
                           f"{fmt_dec(d['delta_u'], 6)} | {fmt_dec(d['delta_MeV'], 4)} | "
                           f"{d['classification']} |")
        parts.append("")
        parts.append("**Best 10 (smallest |Δ|):**")
        parts.append("")
        parts.append("| isotope | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (u) | Δ (MeV) | class |")
        parts.append("|---|---|---|---|---|---|---|---|---|")
        for d in best_deltas[-10:]:
            parts.append(f"| {d['isotope']} | {d['Z']} | {d['N']} | {d['A']} | "
                           f"{fmt_dec(d['B_u_obs_u'], 6)} | {fmt_dec(d['B_u_pred_u'], 6)} | "
                           f"{fmt_dec(d['delta_u'], 6)} | {fmt_dec(d['delta_MeV'], 4)} | "
                           f"{d['classification']} |")
        parts.append("")

    parts.append("## Cascade-cited anchor nuclei (Au-197, C-12, C-13)")
    parts.append("")
    parts.append("| isotope | rule | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (MeV) | class |")
    parts.append("|---|---|---|---|---|---|---|---|---|")
    for iso in ["Au-197", "C-12", "C-13"]:
        if best:
            for d in rule_deltas[best["rule"]]:
                if d["isotope"] == iso:
                    parts.append(f"| {iso} | {best['rule']} | {d['Z']} | {d['N']} | {d['A']} | "
                                   f"{fmt_dec(d['B_u_obs_u'], 6)} | {fmt_dec(d['B_u_pred_u'], 6)} | "
                                   f"{fmt_dec(d['delta_MeV'], 4)} | {d['classification']} |")
                    break

    parts.append("")
    parts.append("## Wrong controls")
    parts.append("")
    for wcr in wc_records:
        parts.append(f"- **{wcr['wc']}**: passed={wcr['passed']}")
        if "ratio" in wcr:
            parts.append(f"  - perturb max |Δ|: {fmt_dec(wcr.get('perturb_max_MeV') or wcr.get('shuffle_max_MeV'))} MeV "
                           f"vs best {fmt_dec(wcr['best_max_MeV'])} MeV (ratio {fmt_dec(wcr['ratio'])})")

    parts.append("")
    parts.append("## Verdict logic")
    parts.append("")
    parts.append(f"- Best rule max |Δ| MeV: {fmt_dec(best['max_abs_MeV']) if best else 'n/a'}")
    parts.append(f"- Target ceiling: 0.005 MeV")
    parts.append(f"- All WC pass: {all(wcr['passed'] for wcr in wc_records)}")
    parts.append(f"- Verdict: `{verdict}`")
    parts.append("")
    parts.append("## Provenance chain")
    parts.append("")
    parts.append("- Dataset: `CR242_binding_dataset.csv` (71 nuclei AME2020-derived)")
    parts.append("- Particle-level formula: CR009 PASS (charged-triadic + charged-pair)")
    parts.append("- Substrate atoms: CR238 (R, D, S, Θ, ℱ, V, M, κ, g)")
    parts.append("- Per-rule predictions: `CR249_per_row_predictions.csv`")
    parts.append("- Aggregate metrics: `CR249_rule_comparison.csv`")
    parts.append("- Wrong controls: `CR249_wrong_controls.csv`")
    RESULT.write_text("\n".join(parts) + "\n", encoding="utf-8")

    paths = [PRECOMMIT, RUNNER, PER_ROW, RULE_COMP, WC_LOG, SUMMARY, RESULT]
    with HASHES.open("w", encoding="utf-8") as f:
        for p in paths:
            if p.exists():
                f.write(f"{sha256_file(p)}  {p.name}\n")

    print()
    print(f"==== CR249 verdict: {verdict} ====")
    print(f"  best rule:     {best['rule'] if best else 'NONE'}")
    print(f"  best max|Δ|:   {best['max_abs_MeV'] if best else 'n/a'} MeV")
    print(f"  target:        0.005 MeV")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
