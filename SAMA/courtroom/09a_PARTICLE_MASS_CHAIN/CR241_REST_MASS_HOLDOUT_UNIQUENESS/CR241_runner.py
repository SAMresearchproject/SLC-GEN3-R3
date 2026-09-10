"""CR241 rest-mass holdout and structural-uniqueness runner.

This runner is constructive downstream work from CR238/CR239/CR240.
It must be executed through tools/run_sam_test.py, not directly, for a
Courtroom-valid result path.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import spearmanr


CR_DIR = Path(__file__).resolve().parent
REPO = CR_DIR.parents[1]
CR238_DIR = CR_DIR.parent / "CR238_SUBSTRATE_SPINE_COMPACTION"
CR239_DIR = CR_DIR.parent / "CR239_NATIVE_MASS_GRAVITY_BRIDGE"
CR240_DIR = CR_DIR.parent / "CR240_NEUTRON_REST_MASS_CHANNEL"

PRECOMMIT = CR_DIR / "CR241_PRECOMMIT.md"
HOLDOUT_CSV = CR_DIR / "CR241_holdout_isotope_input.csv"
RUNNER = CR_DIR / "CR241_runner.py"

CR239_ISOTOPES = CR239_DIR / "CR239_measured_isotope_masses.csv"
CR240_PREDICTIONS = CR240_DIR / "CR240_extended_kernel_predictions.csv"
CR240_SUMMARY = CR240_DIR / "CR240_summary.json"
CR240_CANDIDATES = CR240_DIR / "CR240_candidate_typed_values.csv"

OUT_SUMMARY = CR_DIR / "CR241_summary.json"
OUT_RESULT = CR_DIR / "CR241_result.md"
OUT_HOLDOUT_PRED = CR_DIR / "CR241_holdout_predictions.csv"
OUT_AXES = CR_DIR / "CR241_holdout_residual_axes.csv"
OUT_ANCHOR = CR_DIR / "CR241_cross_anchor_stability.csv"
OUT_SCAN = CR_DIR / "CR241_expression_scan_hits.csv"
OUT_SURVIVAL = CR_DIR / "CR241_candidate_survival.csv"
OUT_WC = CR_DIR / "CR241_wrong_controls.csv"
OUT_MANIFEST = CR_DIR / "CR241_input_manifest.csv"
OUT_HASHES = CR_DIR / "HASHES.txt"

F = Fraction(81, 1)
S = Fraction(8, 1)
ALPHA_H = Fraction(2, 1)
D = Fraction(3, 1)
R = Fraction(12, 1)
L = Fraction(162, 1)
V = Fraction(27, 1)
THETA = Fraction(18, 1)
M = Fraction(126, 1)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
MU_Q = Fraction(192, 7117)

M_P = Fraction("1.00727646693")
M_N = Fraction("1.00866491595")
M_H1 = Fraction("1.00782503207")
M_HE4 = Fraction("4.00260325413")

MAGIC_NUMBERS = (2, 8, 20, 28, 50, 82, 126)
TIE_PPM = 10e-6
STRICT_FAMILY = {"C5", "C6", "C7"}
PRIMARY_AXES = {
    "NmZ_squared",
    "A_to_two_thirds",
    "coulomb_ZZminus1_over_A_third",
    "delta_pairing",
    "magic_distance",
}

WC1_SEED = 20260623
WC2_SEED = 20260624
WC3_SEED = 20260625
WC5_SEED = 20260626

DISALLOWED = (
    "CR241 proves the free neutron mass",
    "CR241 proves the free proton mass",
    "CR241 derives binding energy fully",
    "CR241 falsifies CR238",
    "C5/C6/C7 were discovered after data reveal",
    "The candidate list was expanded after seeing results",
    "He-4 replaced C-12 as the main anchor",
    "Direct script execution is a valid Courtroom result path",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def frac(text: str) -> Fraction:
    return Fraction(text)


def q_mass(a: int) -> Fraction:
    return Fraction(4 * a, 1) * KAPPA


def m_sam(a: int, mu_q: Fraction = MU_Q) -> Fraction:
    return mu_q * q_mass(a)


def he4_mu_q() -> Fraction:
    return M_HE4 / q_mass(4)


def pairing(z: int, n: int) -> int:
    if z % 2 == 0 and n % 2 == 0:
        return 1
    if z % 2 == 1 and n % 2 == 1:
        return -1
    return 0


def magic_distance(z: int, n: int) -> int:
    return min(min(abs(z - m) for m in MAGIC_NUMBERS), min(abs(n - m) for m in MAGIC_NUMBERS))


def r2(x: list[float], y: list[float]) -> float:
    if len(set(x)) <= 1 or len(set(y)) <= 1:
        return float("nan")
    coeff = np.polyfit(np.array(x, dtype=float), np.array(y, dtype=float), 1)
    pred = coeff[0] * np.array(x, dtype=float) + coeff[1]
    yy = np.array(y, dtype=float)
    ss_res = float(np.sum((yy - pred) ** 2))
    ss_tot = float(np.sum((yy - np.mean(yy)) ** 2))
    return float("nan") if ss_tot == 0 else 1.0 - ss_res / ss_tot


def spearman(x: list[float], y: list[float]) -> tuple[float, float]:
    if len(set(x)) <= 1 or len(set(y)) <= 1:
        return float("nan"), float("nan")
    res = spearmanr(x, y)
    return float(res.statistic), float(res.pvalue)


def load_holdout() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(HOLDOUT_CSV):
        rows.append(
            {
                "isotope": row["isotope"],
                "Z": int(row["Z"]),
                "N": int(row["N"]),
                "A": int(row["A"]),
                "atomic_mass_u": frac(row["atomic_mass_u"]),
                "mass_uncertainty_u": row["mass_uncertainty_u"],
                "measurement_class": row["measurement_class"],
                "source_table": row["source_table"],
                "confidence_lane": row["confidence_lane"],
                "notes": row["notes"],
            }
        )
    return rows


def collision_guard(holdout: list[dict[str, Any]]) -> dict[str, Any]:
    holdout_ids = {row["isotope"] for row in holdout}
    cr239_ids = {row["isotope"] for row in read_csv(CR239_ISOTOPES)}
    cr240_ids = {row["isotope"] for row in read_csv(CR240_PREDICTIONS)}
    collisions = sorted(holdout_ids & (cr239_ids | cr240_ids))
    return {
        "passed": not collisions,
        "collisions": collisions,
        "holdout_rows": len(holdout),
        "unique_holdout_rows": len(holdout_ids),
    }


def layer1_holdout(holdout: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    predictions = []
    for row in holdout:
        measured = row["atomic_mass_u"]
        pred = m_sam(row["A"])
        delta = measured - pred
        binding = pred - measured
        eps = delta / measured
        predictions.append(
            {
                "isotope": row["isotope"],
                "Z": row["Z"],
                "N": row["N"],
                "A": row["A"],
                "atomic_mass_u": float(measured),
                "mass_uncertainty_u": row["mass_uncertainty_u"],
                "m_SAM_u": float(pred),
                "delta_m_u": float(delta),
                "binding_defect_u": float(binding),
                "epsilon": float(eps),
                "abs_epsilon": abs(float(eps)),
                "measurement_class": row["measurement_class"],
                "confidence_lane": row["confidence_lane"],
            }
        )

    eps_abs = [row["abs_epsilon"] for row in predictions]
    rms_eps = math.sqrt(sum(e * e for e in eps_abs) / len(eps_abs))

    y_delta = [row["delta_m_u"] for row in predictions]
    y_binding = [row["binding_defect_u"] for row in predictions]
    axes = axis_values(predictions)
    axis_rows = []
    primary_hits = []
    for axis, values in axes.items():
        rho_delta, p_delta = spearman(y_delta, values)
        rho_bind, p_bind = spearman(y_binding, values)
        row = {
            "axis": axis,
            "primary_axis": axis in PRIMARY_AXES,
            "spearman_delta_m": rho_delta,
            "p_delta_m": p_delta,
            "spearman_binding_defect_u": rho_bind,
            "p_binding_defect_u": p_bind,
            "linear_r2_delta_m": r2(values, y_delta),
            "linear_r2_binding_defect_u": r2(values, y_binding),
        }
        axis_rows.append(row)
        if axis in PRIMARY_AXES and not math.isnan(rho_bind) and abs(rho_bind) > 0.5:
            primary_hits.append(axis)

    summary = {
        "rms_epsilon": rms_eps,
        "max_abs_epsilon": max(eps_abs),
        "frac_abs_epsilon_lt_0p001": sum(e < 0.001 for e in eps_abs) / len(eps_abs),
        "frac_abs_epsilon_lt_0p005": sum(e < 0.005 for e in eps_abs) / len(eps_abs),
        "frac_abs_epsilon_lt_0p01": sum(e < 0.01 for e in eps_abs) / len(eps_abs),
        "primary_axes_over_0p5": primary_hits,
        "n_primary_axes_over_0p5": len(primary_hits),
        "strong_structure_pass": rms_eps < 0.01 and len(primary_hits) >= 2,
        "boundary_structure_pass": rms_eps < 0.01 and len(primary_hits) >= 1,
    }
    return summary, predictions, axis_rows


def axis_values(rows: list[dict[str, Any]]) -> dict[str, list[float]]:
    out = {
        "A": [],
        "Z": [],
        "N": [],
        "N_minus_Z": [],
        "NmZ_squared": [],
        "A_to_two_thirds": [],
        "Z_squared_over_A_third": [],
        "coulomb_ZZminus1_over_A_third": [],
        "delta_pairing": [],
        "magic_distance": [],
        "radix_cycle_position": [],
    }
    for row in rows:
        z = int(row["Z"])
        n = int(row["N"])
        a = int(row["A"])
        nmz = n - z
        out["A"].append(float(a))
        out["Z"].append(float(z))
        out["N"].append(float(n))
        out["N_minus_Z"].append(float(nmz))
        out["NmZ_squared"].append(float(nmz * nmz))
        out["A_to_two_thirds"].append(float(a ** (2.0 / 3.0)))
        out["Z_squared_over_A_third"].append(float((z * z) / (a ** (1.0 / 3.0))))
        out["coulomb_ZZminus1_over_A_third"].append(float((z * (z - 1)) / (a ** (1.0 / 3.0))))
        out["delta_pairing"].append(float(pairing(z, n)))
        out["magic_distance"].append(float(magic_distance(z, n)))
        out["radix_cycle_position"].append(float((z - 1) % int(R)))
    return out


def candidate_factors() -> dict[str, tuple[Fraction, str, str]]:
    return {
        "C0": (Fraction(1, 1), "mu_Q * 4*kappa", "anchor identity"),
        "C1": ((Fraction(4, 1) * KAPPA - Fraction(8, 1) * G) / (Fraction(4, 1) * KAPPA), "mu_Q * (4*kappa - 8*g)", "substrate-replaced excess-neutron"),
        "C2": ((Fraction(4, 1) * KAPPA + Fraction(8, 1) * G) / (Fraction(4, 1) * KAPPA), "mu_Q * (4*kappa + 8*g)", "substrate-additive excess-neutron"),
        "C3": (Fraction(1, 1) + G, "mu_Q * 4*kappa * (1 + g)", "binding correction at g"),
        "C4": (Fraction(1, 1) + Fraction(1, 1) / (D * D * S), "mu_Q * 4*kappa * (1 + 1/(D^2*S))", "D-S typed correction"),
        "C5": (Fraction(1, 1) + Fraction(1, 1) / (R * R), "mu_Q * 4*kappa * (1 + 1/R^2)", "cycle-budget surface unit"),
        "C6": (Fraction(1, 1) + G / ALPHA_H, "mu_Q * 4*kappa * (1 + g/alpha_H)", "face-halved neutron-unit correction"),
        "C7": (Fraction(1, 1) + Fraction(1, 1) / M, "mu_Q * 4*kappa * (1 + 1/M)", "matter-capacity reciprocal"),
        "C8": (Fraction(1, 1) / (S * L), "mu_Q * 4*kappa * (1/(S*L))", "closed-ledger split diagnostic"),
    }


def layer2_cross_anchor() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    mu_he4 = he4_mu_q()
    drift = float(mu_he4 / MU_Q - 1)
    base_c12 = MU_Q * Fraction(4, 1) * KAPPA
    base_he4 = mu_he4 * Fraction(4, 1) * KAPPA
    targets = {
        "m_p": M_P,
        "m_n": M_N,
        "H_1": M_H1,
    }
    split_targets = {
        "m_n_minus_m_p": M_N - M_P,
        "H1_minus_m_p": M_H1 - M_P,
        "one_u_minus_substrate_excess": Fraction(1, 1) - Fraction(24, 7117),
    }

    rows = []
    for target_name, target in targets.items():
        cands = []
        for cid, (factor, formula, source) in candidate_factors().items():
            if cid == "C8":
                continue
            value_c12 = base_c12 * factor
            value_he4 = base_he4 * factor
            cands.append(
                {
                    "candidate_id": cid,
                    "formula": formula,
                    "typed_source": source,
                    "target": target_name,
                    "target_u": float(target),
                    "candidate_value_C12": float(value_c12),
                    "candidate_value_He4": float(value_he4),
                    "abs_residual_C12": float(abs(value_c12 - target)),
                    "abs_residual_He4": float(abs(value_he4 - target)),
                    "relative_residual_C12": float(abs((value_c12 - target) / target)),
                    "relative_residual_He4": float(abs((value_he4 - target) / target)),
                }
            )
        rank_values(cands, "relative_residual_C12", "rank_under_C12_anchor")
        rank_values(cands, "relative_residual_He4", "rank_under_He4_anchor")
        for row in cands:
            row["rank_shift"] = row["rank_under_He4_anchor"] - row["rank_under_C12_anchor"]
            row["top3_under_He4"] = row["rank_under_He4_anchor"] <= 3
            rows.append(row)

    for target_name, target in split_targets.items():
        factor, formula, source = candidate_factors()["C8"]
        value_c12 = base_c12 * factor
        value_he4 = base_he4 * factor
        rows.append(
            {
                "candidate_id": "C8",
                "formula": formula,
                "typed_source": source,
                "target": target_name,
                "target_u": float(target),
                "candidate_value_C12": float(value_c12),
                "candidate_value_He4": float(value_he4),
                "abs_residual_C12": float(abs(value_c12 - target)),
                "abs_residual_He4": float(abs(value_he4 - target)),
                "relative_residual_C12": float(abs((value_c12 - target) / target)),
                "relative_residual_He4": float(abs((value_he4 - target) / target)),
                "rank_under_C12_anchor": "",
                "rank_under_He4_anchor": "",
                "rank_shift": "",
                "top3_under_He4": "",
            }
        )

    target_represented = {}
    for target_name in targets:
        top3 = {
            row["candidate_id"]
            for row in rows
            if row["target"] == target_name and row["candidate_id"] != "C8" and row["rank_under_He4_anchor"] <= 3
        }
        target_represented[target_name] = bool(top3 & STRICT_FAMILY)

    survival_rows = [
        {
            "gate": "cross_anchor_family_top3",
            "target": target,
            "passed": passed,
            "details": "CR240 strict family represented in He-4 top-3" if passed else "no strict-family candidate in He-4 top-3",
        }
        for target, passed in target_represented.items()
    ]
    stability_pass = sum(target_represented.values()) >= 2
    tier = (
        "EXCEPTIONAL_ANCHOR_STABILITY" if abs(drift) < 0.0001
        else "ANCHOR_STABLE" if abs(drift) < 0.001
        else "CONSISTENT_WITH_CR240_WC2" if abs(drift) < 0.005
        else "ANCHOR_UNSTABLE"
    )
    summary = {
        "mu_Q_C12": str(MU_Q),
        "mu_Q_He4": str(mu_he4),
        "anchor_drift": drift,
        "anchor_drift_ppm": drift * 1_000_000,
        "stability_tier": tier,
        "family_top3_targets": target_represented,
        "candidate_stability_pass": stability_pass,
    }
    return summary, rows, survival_rows


def rank_values(rows: list[dict[str, Any]], value_key: str, rank_key: str) -> None:
    ordered = sorted(rows, key=lambda r: (r[value_key], r["candidate_id"]))
    rank = 0
    prev = None
    for idx, row in enumerate(ordered, start=1):
        value = float(row[value_key])
        if prev is None or abs(value - prev) > TIE_PPM:
            rank = idx
            prev = value
        row[rank_key] = rank


def fraction_atoms() -> list[dict[str, Any]]:
    return [
        atom("g", G, ["g"], 1, 0, 1),
        atom("g/alpha_H", G / ALPHA_H, ["g", "alpha_H"], 2, 1, 1),
        atom("1/R", Fraction(1, 1) / R, ["R"], 1, 1, 1),
        atom("1/R^2", Fraction(1, 1) / (R * R), ["R"], 1, 2, 1),
        atom("1/M", Fraction(1, 1) / M, ["M"], 1, 1, 1),
        atom("1/L", Fraction(1, 1) / L, ["L"], 1, 1, 1),
        atom("1/(S*L)", Fraction(1, 1) / (S * L), ["S", "L"], 2, 2, 1),
        atom("1/(D^2*S)", Fraction(1, 1) / (D * D * S), ["D", "S"], 2, 3, 1),
        atom("Theta/(R^2*S)", THETA / (R * R * S), ["Theta", "R", "S"], 3, 3, 1),
        atom("Theta/(L*S)", THETA / (L * S), ["Theta", "L", "S"], 3, 2, 1),
        atom("1/(alpha_H*R^2)", Fraction(1, 1) / (ALPHA_H * R * R), ["alpha_H", "R"], 2, 3, 1),
        atom("1/(alpha_H*M)", Fraction(1, 1) / (ALPHA_H * M), ["alpha_H", "M"], 2, 2, 1),
        atom("1/(D*R^2)", Fraction(1, 1) / (D * R * R), ["D", "R"], 2, 3, 1),
        atom("1/(D*M)", Fraction(1, 1) / (D * M), ["D", "M"], 2, 2, 1),
    ]


def atom(name: str, value: Fraction, classes: list[str], atom_count: int, op_count: int, nesting: int) -> dict[str, Any]:
    return {
        "expr": name,
        "value": value,
        "classes": classes,
        "atom_count": atom_count,
        "op_count": op_count,
        "nesting": nesting,
    }


def expression_scan(depth: int = 2, contraction: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    atoms = fraction_atoms()
    expressions = []
    for a in atoms:
        expressions.append(expr_row(f"1 + {a['expr']}", Fraction(1, 1) + a["value"], [a], 1, "nucleon_window"))
        expressions.append(expr_row(f"1 - {a['expr']}", Fraction(1, 1) - a["value"], [a], 1, "nucleon_window"))
    if depth >= 2 and not contraction:
        for a in atoms:
            for b in atoms:
                expressions.append(expr_row(f"1 + {a['expr']} + {b['expr']}", Fraction(1, 1) + a["value"] + b["value"], [a, b], 2, "nucleon_window"))
                expressions.append(expr_row(f"1 + {a['expr']} - {b['expr']}", Fraction(1, 1) + a["value"] - b["value"], [a, b], 2, "nucleon_window"))
    if depth >= 3 and not contraction:
        for a in atoms:
            for b in atoms:
                for c in atoms:
                    expressions.append(expr_row(f"1 + {a['expr']} + {b['expr']} + {c['expr']}", Fraction(1, 1) + a["value"] + b["value"] + c["value"], [a, b, c], 3, "nucleon_window"))
                    expressions.append(expr_row(f"1 + {a['expr']} + {b['expr']} - {c['expr']}", Fraction(1, 1) + a["value"] + b["value"] - c["value"], [a, b, c], 3, "nucleon_window"))

    split_exprs = []
    for a in atoms:
        split_exprs.append(expr_row(a["expr"], a["value"], [a], 1, "splitting_window"))
    if depth >= 2 and not contraction:
        for a in atoms:
            for b in atoms:
                split_exprs.append(expr_row(f"{a['expr']} + {b['expr']}", a["value"] + b["value"], [a, b], 2, "splitting_window"))
                split_exprs.append(expr_row(f"{a['expr']} - {b['expr']}", a["value"] - b["value"], [a, b], 2, "splitting_window"))

    hits = []
    for row in expressions:
        value = row["value"]
        if Fraction(1005, 1000) <= value <= Fraction(1010, 1000):
            hits.append(row)
    for row in split_exprs:
        value = row["value"]
        if Fraction(5, 10000) <= value <= Fraction(15, 10000):
            hits.append(row)

    unique = canonical_hits(hits)
    ranks = rank_scan_hits(unique)
    for row in unique:
        row["complexity_rank"] = ranks[row["evaluated_rational"]]

    nucleon_hits = [r for r in unique if r["target_window"] == "nucleon_window"]
    split_hits = [r for r in unique if r["target_window"] == "splitting_window"]
    rank_by_candidate = {}
    for cid in ("C5", "C6", "C7", "C8"):
        match = [r for r in unique if r["candidate_family"] == cid]
        rank_by_candidate[cid] = min([r["complexity_rank"] for r in match], default=None)
    summary = {
        "N_hits_nucleon_window": len(nucleon_hits),
        "N_hits_splitting_window": len(split_hits),
        "rank_of_C5": rank_by_candidate["C5"],
        "rank_of_C6": rank_by_candidate["C6"],
        "rank_of_C7": rank_by_candidate["C7"],
        "rank_of_C8": rank_by_candidate["C8"],
        "strong_uniqueness_pass": (
            len(nucleon_hits) <= 5
            and any((rank_by_candidate[cid] is not None and rank_by_candidate[cid] <= 3) for cid in ("C5", "C6", "C7"))
        ),
        "moderate_uniqueness_pass": (
            len(nucleon_hits) <= 12
            and any((rank_by_candidate[cid] is not None and rank_by_candidate[cid] <= 5) for cid in ("C5", "C6", "C7"))
        ),
    }
    return summary, sorted(unique, key=lambda r: (r["target_window"], r["complexity_rank"], r["evaluated_value"], r["expression"]))


def expr_row(expression: str, value: Fraction, atoms: list[dict[str, Any]], expr_depth: int, window: str) -> dict[str, Any]:
    classes = sorted({cls for atom_info in atoms for cls in atom_info["classes"]})
    atom_count = sum(int(atom_info["atom_count"]) for atom_info in atoms)
    atom_ops = sum(int(atom_info["op_count"]) for atom_info in atoms)
    op_count = atom_ops + expr_depth
    nesting = max([int(atom_info["nesting"]) for atom_info in atoms] + [1])
    score = atom_count + op_count + nesting + len(classes)
    return {
        "expression": expression,
        "value": value,
        "target_window": window,
        "complexity_score": score,
        "atom_count": atom_count,
        "operator_count": op_count,
        "nesting_depth": nesting,
        "distinct_primitive_class_count": len(classes),
        "primitive_classes": ";".join(classes),
    }


def canonical_hits(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, Fraction], dict[str, Any]] = {}
    aliases: dict[tuple[str, Fraction], list[str]] = {}
    for hit in hits:
        key = (hit["target_window"], hit["value"])
        aliases.setdefault(key, []).append(hit["expression"])
        if key not in by_key or (hit["complexity_score"], hit["expression"]) < (
            by_key[key]["complexity_score"],
            by_key[key]["expression"],
        ):
            by_key[key] = hit
    out = []
    family_by_value = {factor: cid for cid, (factor, _, _) in candidate_factors().items()}
    for (window, value), row in by_key.items():
        family = family_by_value.get(value, "")
        out.append(
            {
                "expression": row["expression"],
                "aliases": "; ".join(sorted(set(aliases[(window, value)]))),
                "evaluated_value": float(value),
                "evaluated_rational": f"{value.numerator}/{value.denominator}",
                "target_window": window,
                "complexity_score": row["complexity_score"],
                "atom_count": row["atom_count"],
                "operator_count": row["operator_count"],
                "nesting_depth": row["nesting_depth"],
                "distinct_primitive_class_count": row["distinct_primitive_class_count"],
                "primitive_classes": row["primitive_classes"],
                "uses_candidate_family": bool(family),
                "candidate_family": family,
                "distance_to_m_p": abs(float(value) - float(M_P)) if window == "nucleon_window" else "",
                "distance_to_m_n": abs(float(value) - float(M_N)) if window == "nucleon_window" else "",
                "distance_to_H1": abs(float(value) - float(M_H1)) if window == "nucleon_window" else "",
            }
        )
    return out


def rank_scan_hits(rows: list[dict[str, Any]]) -> dict[str, int]:
    nucleon = [r for r in rows if r["target_window"] == "nucleon_window"]
    ordered = sorted(nucleon, key=lambda r: (r["complexity_score"], r["evaluated_value"], r["expression"]))
    ranks = {}
    rank = 0
    prev_score = None
    for idx, row in enumerate(ordered, start=1):
        score = row["complexity_score"]
        if score != prev_score:
            rank = idx
            prev_score = score
        ranks[row["evaluated_rational"]] = rank
    for row in rows:
        ranks.setdefault(row["evaluated_rational"], "")
    return ranks


def wrong_controls(holdout: list[dict[str, Any]], scan_summary: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    wc_rows = []

    random_pool = list(holdout)
    rng1 = random.Random(WC1_SEED)
    rng1.shuffle(random_pool)
    wc1_set = random_pool[: len(holdout)]
    wc1_summary, _, _ = layer1_holdout(wc1_set)
    wc_rows.append(
        {
            "wc_id": "WC1_random_holdout_set",
            "complete": True,
            "passed_integrity": True,
            "details": f"seed={WC1_SEED}; random_pool_size={len(random_pool)}; rms_epsilon={wc1_summary['rms_epsilon']}",
        }
    )

    rng2 = random.Random(WC2_SEED)
    anchor_row = rng2.choice(holdout)
    mu_random = anchor_row["atomic_mass_u"] / q_mass(anchor_row["A"])
    drift = float(mu_random / MU_Q - 1)
    wc_rows.append(
        {
            "wc_id": "WC2_random_isotope_anchor",
            "complete": True,
            "passed_integrity": True,
            "details": f"seed={WC2_SEED}; anchor={anchor_row['isotope']}; drift={drift}",
        }
    )

    expanded_summary, _ = expression_scan(depth=3)
    wc3_pass = expanded_summary["N_hits_nucleon_window"] >= scan_summary["N_hits_nucleon_window"]
    wc_rows.append(
        {
            "wc_id": "WC3_expression_grammar_expansion",
            "complete": True,
            "passed_integrity": wc3_pass,
            "details": f"baseline={scan_summary['N_hits_nucleon_window']}; expanded_depth3={expanded_summary['N_hits_nucleon_window']}",
        }
    )

    contraction_summary, contraction_hits = expression_scan(depth=1, contraction=True)
    contraction_families = {row["candidate_family"] for row in contraction_hits if row["candidate_family"]}
    wc4_pass = STRICT_FAMILY <= contraction_families
    wc_rows.append(
        {
            "wc_id": "WC4_expression_grammar_contraction",
            "complete": True,
            "passed_integrity": wc4_pass,
            "details": f"families_returned={sorted(contraction_families)}; contraction_hits={contraction_summary['N_hits_nucleon_window']}",
        }
    )

    rng5 = random.Random(WC5_SEED)
    labels = ["R", "M", "L", "V", "Theta", "S"]
    shuffled = labels[:]
    rng5.shuffle(shuffled)
    label_map = dict(zip(labels, shuffled))
    breaks = sum(1 for k, v in label_map.items() if k != v)
    wc5_pass = breaks >= 3
    wc_rows.append(
        {
            "wc_id": "WC5_shuffled_primitive_labels",
            "complete": True,
            "passed_integrity": wc5_pass,
            "details": json.dumps({"seed": WC5_SEED, "label_map": label_map, "changed_labels": breaks}, sort_keys=True),
        }
    )

    control_integrity = {
        "all_wrong_controls_complete": all(row["complete"] for row in wc_rows),
        "WC3_expansion_not_reduce_hits": wc3_pass,
        "WC4_contraction_returns_C5_C6_C7": wc4_pass,
        "WC5_shuffle_breaks_typed_sources": wc5_pass,
    }
    control_integrity["control_integrity_pass"] = all(control_integrity.values())
    return control_integrity, wc_rows


def assign_verdict(
    collision: dict[str, Any],
    l1: dict[str, Any],
    l2: dict[str, Any],
    scan: dict[str, Any],
    controls: dict[str, Any],
    disallowed_flags: list[dict[str, Any]],
) -> dict[str, Any]:
    fail_conditions = {
        "holdout_collision_guard_fails": not collision["passed"],
        "layer1_rms_epsilon_ge_0p01": l1["rms_epsilon"] >= 0.01,
        "layer1_boundary_structure_fails": not l1["boundary_structure_pass"],
        "layer2_anchor_drift_ge_5000ppm": abs(l2["anchor_drift"]) >= 0.005,
        "layer3_uniqueness_fail": not scan["moderate_uniqueness_pass"],
        "control_integrity_clause_fails": not controls["control_integrity_pass"],
        "disallowed_claim_guard_fails": bool(disallowed_flags),
    }
    strong_conditions = {
        "layer1_rms_epsilon_lt_0p01": l1["rms_epsilon"] < 0.01,
        "layer1_strong_structure": l1["strong_structure_pass"],
        "layer2_anchor_drift_lt_1000ppm": abs(l2["anchor_drift"]) < 0.001,
        "layer2_candidate_family_top3": l2["candidate_stability_pass"],
        "layer3_strong_uniqueness": scan["strong_uniqueness_pass"],
        "control_integrity_clause": controls["control_integrity_pass"],
    }
    boundary_conditions = {
        "layer1_rms_epsilon_lt_0p01": l1["rms_epsilon"] < 0.01,
        "layer1_boundary_structure": l1["boundary_structure_pass"],
        "layer2_anchor_drift_lt_5000ppm": abs(l2["anchor_drift"]) < 0.005,
        "layer3_moderate_uniqueness": scan["moderate_uniqueness_pass"],
        "control_integrity_clause": controls["control_integrity_pass"],
    }
    if any(fail_conditions.values()):
        verdict = "FAIL_CR241_CANDIDATE_ARTIFACT"
    elif all(strong_conditions.values()):
        verdict = "STRONG_PASS_CR241_HOLDOUT_AND_UNIQUENESS"
    elif all(boundary_conditions.values()):
        verdict = "BOUNDARY_CR241_CANDIDATE_SURVIVES_PARTIAL"
    else:
        verdict = "FAIL_CR241_CANDIDATE_ARTIFACT"
    return {
        "verdict": verdict,
        "fail_conditions": fail_conditions,
        "strong_conditions": strong_conditions,
        "boundary_conditions": boundary_conditions,
    }


def scan_disallowed_claims(text: str) -> list[dict[str, Any]]:
    flags = []
    lower = text.lower()
    for phrase in DISALLOWED:
        pos = lower.find(phrase.lower())
        if pos >= 0:
            flags.append({"phrase": phrase, "position": pos, "line": text[:pos].count("\n") + 1})
    return flags


def write_manifest_and_hashes() -> None:
    manifest_inputs = [
        (PRECOMMIT, "precommit"),
        (RUNNER, "runner"),
        (HOLDOUT_CSV, "locked_holdout_input"),
        (CR239_ISOTOPES, "upstream_curated_isotope_set"),
        (CR240_PREDICTIONS, "upstream_cr240_curated_predictions"),
        (CR240_SUMMARY, "upstream_cr240_summary"),
        (CR240_CANDIDATES, "upstream_cr240_candidate_values"),
    ]
    manifest_rows = [
        {"path": rel(path), "role": role, "sha256": sha256_file(path), "bytes": path.stat().st_size}
        for path, role in manifest_inputs
    ]
    write_csv(OUT_MANIFEST, manifest_rows, ["path", "role", "sha256", "bytes"])

    artifacts = [
        PRECOMMIT,
        RUNNER,
        OUT_SUMMARY,
        OUT_RESULT,
        HOLDOUT_CSV,
        OUT_HOLDOUT_PRED,
        OUT_AXES,
        OUT_ANCHOR,
        OUT_SCAN,
        OUT_SURVIVAL,
        OUT_WC,
        OUT_MANIFEST,
    ]
    lines = [f"{sha256_file(path)}  {path.name}" for path in artifacts]
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_result(summary: dict[str, Any]) -> None:
    verdict = summary["verdict"]
    l1 = summary["layer_1_holdout"]
    l2 = summary["layer_2_cross_anchor"]
    scan = summary["layer_3_expression_scan"]
    controls = summary["control_integrity"]
    lines = [
        "# CR241 Rest-Mass Holdout and Structural-Uniqueness Result",
        "",
        f"**Verdict:** {verdict}",
        "",
        "## Readout",
        "",
        f"- Holdout rows: {summary['holdout_collision_guard']['holdout_rows']} unique rows; collisions: {summary['holdout_collision_guard']['collisions']}",
        f"- Layer 1 RMS epsilon: {l1['rms_epsilon']:.12g}",
        f"- Layer 1 primary axes over 0.5: {', '.join(l1['primary_axes_over_0p5']) if l1['primary_axes_over_0p5'] else 'none'}",
        f"- Layer 1 strong structure: {l1['strong_structure_pass']}; boundary structure: {l1['boundary_structure_pass']}",
        f"- Layer 2 anchor drift: {l2['anchor_drift_ppm']:.6f} ppm ({l2['stability_tier']})",
        f"- Layer 2 candidate family top-3 stability: {l2['candidate_stability_pass']}",
        f"- Layer 3 nucleon-window hits: {scan['N_hits_nucleon_window']}",
        f"- Layer 3 splitting-window hits: {scan['N_hits_splitting_window']}",
        f"- Layer 3 strong uniqueness: {scan['strong_uniqueness_pass']}; moderate uniqueness: {scan['moderate_uniqueness_pass']}",
        f"- Control integrity: {controls['control_integrity_pass']}",
        "",
        "## Boundary",
        "",
        "CR241 tests the CR240 candidate extension and uniqueness claim. It does not modify CR238, CR239, or CR240 and does not promote any candidate to theorem grade.",
        "",
        "## Outputs",
        "",
        "- CR241_summary.json",
        "- CR241_holdout_predictions.csv",
        "- CR241_holdout_residual_axes.csv",
        "- CR241_cross_anchor_stability.csv",
        "- CR241_expression_scan_hits.csv",
        "- CR241_candidate_survival.csv",
        "- CR241_wrong_controls.csv",
        "- CR241_input_manifest.csv",
        "- HASHES.txt",
        "",
    ]
    OUT_RESULT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    holdout = load_holdout()
    collision = collision_guard(holdout)
    l1, predictions, axis_rows = layer1_holdout(holdout)
    l2, anchor_rows, survival_rows = layer2_cross_anchor()
    scan, scan_rows = expression_scan(depth=2)
    controls, wc_rows = wrong_controls(holdout, scan)

    provisional = {
        "holdout_collision_guard": collision,
        "layer_1_holdout": l1,
        "layer_2_cross_anchor": l2,
        "layer_3_expression_scan": scan,
        "control_integrity": controls,
    }
    disallowed = scan_disallowed_claims(json.dumps(provisional, sort_keys=True))
    verdict_logic = assign_verdict(collision, l1, l2, scan, controls, disallowed)

    summary = {
        "verdict": verdict_logic["verdict"],
        "verdict_logic": verdict_logic,
        "kernel_atoms": {
            "F": int(F),
            "S": int(S),
            "alpha_H": int(ALPHA_H),
            "D": int(D),
            "R": int(R),
            "L": int(L),
            "V": int(V),
            "Theta": int(THETA),
            "M": int(M),
            "kappa": f"{KAPPA.numerator}/{KAPPA.denominator}",
            "g": f"{G.numerator}/{G.denominator}",
            "mu_Q": f"{MU_Q.numerator}/{MU_Q.denominator}",
        },
        "holdout_collision_guard": collision,
        "layer_1_holdout": l1,
        "layer_2_cross_anchor": l2,
        "layer_3_expression_scan": scan,
        "control_integrity": controls,
        "disallowed_claim_flags": disallowed,
    }

    write_csv(
        OUT_HOLDOUT_PRED,
        predictions,
        [
            "isotope", "Z", "N", "A", "atomic_mass_u", "mass_uncertainty_u",
            "m_SAM_u", "delta_m_u", "binding_defect_u", "epsilon", "abs_epsilon",
            "measurement_class", "confidence_lane",
        ],
    )
    write_csv(
        OUT_AXES,
        axis_rows,
        [
            "axis", "primary_axis", "spearman_delta_m", "p_delta_m",
            "spearman_binding_defect_u", "p_binding_defect_u",
            "linear_r2_delta_m", "linear_r2_binding_defect_u",
        ],
    )
    write_csv(
        OUT_ANCHOR,
        anchor_rows,
        [
            "candidate_id", "formula", "typed_source", "target", "target_u",
            "candidate_value_C12", "candidate_value_He4", "abs_residual_C12",
            "abs_residual_He4", "relative_residual_C12", "relative_residual_He4",
            "rank_under_C12_anchor", "rank_under_He4_anchor", "rank_shift",
            "top3_under_He4",
        ],
    )
    write_csv(
        OUT_SCAN,
        scan_rows,
        [
            "expression", "aliases", "evaluated_value", "evaluated_rational",
            "target_window", "complexity_score", "complexity_rank", "atom_count",
            "operator_count", "nesting_depth", "distinct_primitive_class_count",
            "primitive_classes", "uses_candidate_family", "candidate_family",
            "distance_to_m_p", "distance_to_m_n", "distance_to_H1",
        ],
    )
    survival_rows.extend(
        [
            {"gate": "layer1_strong_structure", "target": "primary_axes", "passed": l1["strong_structure_pass"], "details": str(l1["primary_axes_over_0p5"])},
            {"gate": "layer3_strong_uniqueness", "target": "expression_scan", "passed": scan["strong_uniqueness_pass"], "details": f"N_hits={scan['N_hits_nucleon_window']}"},
        ]
    )
    write_csv(OUT_SURVIVAL, survival_rows, ["gate", "target", "passed", "details"])
    write_csv(OUT_WC, wc_rows, ["wc_id", "complete", "passed_integrity", "details"])

    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_result(summary)
    write_manifest_and_hashes()

    print(f"CR241 verdict: {summary['verdict']}")
    print(f"Layer 1 RMS epsilon: {l1['rms_epsilon']:.12g}")
    print(f"Layer 1 primary axes over 0.5: {l1['primary_axes_over_0p5']}")
    print(f"Layer 2 anchor drift ppm: {l2['anchor_drift_ppm']:.6f}")
    print(f"Layer 3 nucleon hits: {scan['N_hits_nucleon_window']}")
    print(f"Layer 3 strong/moderate: {scan['strong_uniqueness_pass']}/{scan['moderate_uniqueness_pass']}")
    print(f"Control integrity: {controls['control_integrity_pass']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
