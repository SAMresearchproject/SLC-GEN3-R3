"""CR240 Rest-Mass Channel Identification + Binding-Energy Axis — Runner.

Sealed precommit SHA-256:
    3b6d4aa0102580c693bba9ba7a635d7654328bc632b1d34e7dc3cfbc7efc85cb

Hypothesis chain under test (from CR238 + CR239 + CR240 lock):
    Q(P)        = S · [Z·κ + (N − Z)·g]       (CR238 substrate channel; untouched)
    Q_mass(P)   = 4 · A · κ                    (CR240 rest-mass channel; new)
    m_SAM(P)    = μ_Q · Q_mass(P) = A · u      (anchored at C-12 = 12u exact)

Four gates:
    Gate 1 — algebraic identities G1.1–G1.5 (exact rationals)
    Gate 2 — Lane A mass prediction m_SAM = A·u
    Gate 3 — residual-structure on 10 axes (Spearman ρ_S)
    Gate 4 — nine typed candidates C0–C8 against m_p, m_n, m(H-1), avg per-nucleon
             (C0–C7 nucleon-mass candidates; C8 splitting diagnostic)

Six wrong controls:
    WC1 — substrate kernel as rest-mass kernel
    WC2 — He-4 anchor swap
    WC3 — random per-nucleon mass scale
    WC4 — m = A·c for c ∈ {0.5u, 1.5u, 2u}
    WC5 — Z·m_p + N·m_n no-binding kernel (residual = binding energy)
    WC6 — random axis-label shuffle (Gate 3 integrity check)

Verdict spectrum (precedence STRONG > BOUNDARY > FAIL):
    STRONG_PASS    — rest-mass channel identified, binding axis found, ≥1 typed candidate
                     clears C-strict (< 0.1 %) for m_p, m_n, H-1, or avg per-nucleon
    BOUNDARY_PASS  — kernel + axis identified; candidate clearance is next-CR target
    FAIL           — extended kernel does not close, OR residual unstructured,
                     OR μ_Q drifts > 5 % under anchor swap

Candidate-scoring rule (locked): all C0–C8 reported; lowest-residual identified;
NO candidate promoted to theorem-grade from this dataset; CR241 holdout required.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.stats import spearmanr


# CR238_LITERAL_SCAN: INPUT_BOUNDARY_BEGIN
F_INPUT = 81
S_INPUT = 8
ALPHA_H_INPUT = 2
ANCHOR_ISOTOPE = "C-12"
ANCHOR_MASS_U = sp.Rational(12)
SECONDARY_ANCHOR_ISOTOPE = "He-4"
SECONDARY_ANCHOR_MASS_U_STR = "4.00260325413"
M_PROTON_MEASURED_U = sp.Rational("1.00727646693")
M_NEUTRON_MEASURED_U = sp.Rational("1.00866491595")
M_HYDROGEN1_MEASURED_U = sp.Rational("1.00782503207")
RANDOM_SCALE_SEED = 20260623
AXIS_SHUFFLE_SEED = 20260624
MAGIC_NUMBERS = (2, 8, 20, 28, 50, 82, 126)
# CR238_LITERAL_SCAN: INPUT_BOUNDARY_END


SCRIPT_DIR = Path(__file__).parent
SCRIPT_PATH = Path(__file__).resolve()
CR240_PRECOMMIT = SCRIPT_DIR / "CR240_PRECOMMIT.md"
CR238_DIR = SCRIPT_DIR.parent / "CR238_SUBSTRATE_SPINE_COMPACTION"
CR239_DIR = SCRIPT_DIR.parent / "CR239_NATIVE_MASS_GRAVITY_BRIDGE"
CR238_PRECOMMIT = CR238_DIR / "CR238_PRECOMMIT.md"
CR238_RESULT = CR238_DIR / "CR238_result.md"
CR239_PRECOMMIT = CR239_DIR / "CR239_PRECOMMIT.md"
CR239_RESULT = CR239_DIR / "CR239_result.md"
INPUT_CSV = CR239_DIR / "CR239_measured_isotope_masses.csv"

EXPECTED_CR240_PRECOMMIT_SHA = (
    "3b6d4aa0102580c693bba9ba7a635d7654328bc632b1d34e7dc3cfbc7efc85cb"
)
EXPECTED_CR238_PRECOMMIT_SHA = (
    "5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293"
)
EXPECTED_CR238_RESULT_SHA = (
    "7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef"
)
EXPECTED_CR239_PRECOMMIT_SHA = (
    "52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7"
)
EXPECTED_CR239_RESULT_SHA = (
    "55928fd97b56bb8ae965bbdcd3c3d7a51891d792ed4eab8dd75f1a2394be411b"
)
EXPECTED_INPUT_CSV_SHA = (
    "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
)


# ------------------------------------------------------------
# SHA verification
# ------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_input_shas() -> dict[str, str]:
    pairs = {
        "cr240_precommit": (CR240_PRECOMMIT, EXPECTED_CR240_PRECOMMIT_SHA),
        "cr238_precommit": (CR238_PRECOMMIT, EXPECTED_CR238_PRECOMMIT_SHA),
        "cr238_result": (CR238_RESULT, EXPECTED_CR238_RESULT_SHA),
        "cr239_precommit": (CR239_PRECOMMIT, EXPECTED_CR239_PRECOMMIT_SHA),
        "cr239_result": (CR239_RESULT, EXPECTED_CR239_RESULT_SHA),
        "cr239_input_csv": (INPUT_CSV, EXPECTED_INPUT_CSV_SHA),
    }
    shas: dict[str, str] = {}
    for name, (path, expected) in pairs.items():
        got = sha256_file(path)
        if got != expected:
            sys.exit(
                f"FAIL: {name} sha mismatch at {path}\n"
                f"  expected {expected}\n"
                f"  got      {got}"
            )
        shas[name] = got
    return shas


# ------------------------------------------------------------
# CR238 typed spine
# ------------------------------------------------------------
def cr238_spine() -> dict[str, sp.Rational]:
    F = sp.Rational(F_INPUT)
    S = sp.Rational(S_INPUT)
    aH = sp.Rational(ALPHA_H_INPUT)
    L = aH * F
    D_sq = sp.Rational(F, S + 1)
    D = sp.sqrt(D_sq)
    D = sp.simplify(D)
    V = F / D
    Theta = aH * D ** 2
    R = aH * L / V
    M = L - 2 * Theta
    kappa = (R - sp.Rational(1)) * (F * S - sp.Rational(1)) / (D * aH ** S)
    g = sp.Rational(1) / S ** 2
    return {
        "F": F, "S": S, "alpha_H": aH, "L": L, "D": D, "V": V, "Theta": Theta,
        "R": R, "M": M,
        "kappa": sp.simplify(kappa), "g": sp.simplify(g),
    }


def Q_substrate(Z: int, N: int, spine: dict[str, sp.Rational]) -> sp.Rational:
    Z_r = sp.Rational(Z)
    N_r = sp.Rational(N)
    G = Z_r * spine["kappa"] + (N_r - Z_r) * spine["g"]
    return sp.simplify(spine["S"] * G)


def Q_mass(Z: int, N: int, spine: dict[str, sp.Rational]) -> sp.Rational:
    """CR240 rest-mass kernel: Q_mass(Z, N) = 4·A·κ."""
    A_r = sp.Rational(Z + N)
    return sp.simplify(sp.Rational(4) * A_r * spine["kappa"])


# ------------------------------------------------------------
# Load isotopes
# ------------------------------------------------------------
def load_isotopes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(INPUT_CSV, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(
                {
                    "isotope": r["isotope"],
                    "Z": int(r["Z"]),
                    "N": int(r["N"]),
                    "A": int(r["A"]),
                    "atomic_mass_u": sp.Rational(r["atomic_mass_u"]),
                    "atomic_mass_u_float": float(r["atomic_mass_u"]),
                    "mass_uncertainty_u": float(r["mass_uncertainty_u"]),
                    "confidence_lane": r["confidence_lane"],
                }
            )
    return rows


# ------------------------------------------------------------
# Anchor μ_Q for the extended kernel
# ------------------------------------------------------------
def anchor_mu_Q_mass(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    anchor_isotope: str,
    anchor_mass_u: sp.Rational,
) -> tuple[sp.Rational, sp.Rational]:
    anchor_row = next(r for r in isotopes if r["isotope"] == anchor_isotope)
    Q_anchor = Q_mass(anchor_row["Z"], anchor_row["N"], spine)
    mu_Q = anchor_mass_u / Q_anchor
    return mu_Q, Q_anchor


# ------------------------------------------------------------
# Gate 1 — algebraic identities
# ------------------------------------------------------------
def gate_1_algebraic(spine: dict[str, sp.Rational]) -> dict[str, Any]:
    F = spine["F"]
    S = spine["S"]
    aH = spine["alpha_H"]
    D = spine["D"]
    kappa = spine["kappa"]
    g = spine["g"]
    L = spine["L"]
    M = spine["M"]
    R = spine["R"]

    # G1.1 — Q_mass(C-12) = 4·12·κ = 48·κ = 7117/16
    Z, N = 6, 6
    Q_mass_anchor = Q_mass(Z, N, spine)
    G1_1 = sp.simplify(Q_mass_anchor - sp.Rational(7117, 16)) == 0

    # G1.2 — m_SAM(C-12) = μ_Q · Q_mass(C-12) = 12 u
    mu_Q = sp.Rational(12) / Q_mass_anchor
    m_SAM_anchor = mu_Q * Q_mass_anchor
    G1_2 = sp.simplify(m_SAM_anchor - sp.Rational(12)) == 0

    # G1.3 — m_SAM(P) = A·u for every (Z, N) test sample
    samples = [(1, 0), (2, 2), (6, 6), (6, 7), (8, 8), (26, 30), (92, 146)]
    G1_3_passes = []
    for z, n in samples:
        Q_m = Q_mass(z, n, spine)
        m_pred = mu_Q * Q_m
        A_val = sp.Rational(z + n)
        ok = sp.simplify(m_pred - A_val) == 0
        G1_3_passes.append({"Z": z, "N": n, "A": z + n,
                            "m_pred": str(m_pred), "passed": bool(ok)})

    # G1.4 — Q_mass(Z, N) − Q_substrate(Z, N) = (N − Z) · 7093/192
    Z_sym = sp.Symbol("Z", integer=True)
    N_sym = sp.Symbol("N", integer=True)
    Q_sub_expr = S * (Z_sym * kappa + (N_sym - Z_sym) * g)
    Q_mass_expr = sp.Rational(4) * (Z_sym + N_sym) * kappa
    diff = sp.simplify(Q_mass_expr - Q_sub_expr)
    expected = (N_sym - Z_sym) * sp.Rational(7093, 192)
    G1_4 = sp.simplify(diff - expected) == 0

    # G1.5 — μ_Q · (Q_mass − Q_sub) per excess neutron = 7093/7117 u
    per_excess = sp.Rational(7093, 192)
    G1_5 = sp.simplify(mu_Q * per_excess - sp.Rational(7093, 7117)) == 0

    return {
        "G1_1_Q_mass_C12_eq_7117_over_16": bool(G1_1),
        "G1_1_value": str(Q_mass_anchor),
        "G1_2_m_SAM_C12_eq_12u": bool(G1_2),
        "G1_3_m_SAM_eq_A_u_samples": G1_3_passes,
        "G1_3_all_pass": all(s["passed"] for s in G1_3_passes),
        "G1_4_Q_mass_minus_Q_sub_eq_NminusZ_7093_192": bool(G1_4),
        "G1_5_mu_Q_per_excess_eq_7093_7117": bool(G1_5),
        "all_pass": (
            bool(G1_1) and bool(G1_2) and all(s["passed"] for s in G1_3_passes)
            and bool(G1_4) and bool(G1_5)
        ),
        "mu_Q": str(mu_Q),
        "mu_Q_float": float(mu_Q),
    }


# ------------------------------------------------------------
# Gate 2 — Lane A mass prediction under extended kernel
# ------------------------------------------------------------
def gate_2_extended_kernel(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    mu_Q: sp.Rational,
) -> dict[str, Any]:
    row_results: list[dict[str, Any]] = []
    for r in isotopes:
        Q_m = Q_mass(r["Z"], r["N"], spine)
        m_pred = mu_Q * Q_m
        m_meas = r["atomic_mass_u"]
        if m_meas == 0:
            eps = float("nan")
        else:
            eps = float((m_meas - m_pred) / m_meas)
        row_results.append({
            "isotope": r["isotope"],
            "Z": r["Z"],
            "N": r["N"],
            "A": r["A"],
            "Q_mass": float(Q_m),
            "m_meas_u": float(m_meas),
            "m_pred_u": float(m_pred),
            "delta_m_u": float(m_meas - m_pred),
            "eps": eps,
            "abs_eps": abs(eps),
            "confidence_lane": r["confidence_lane"],
        })
    lane_a_non_anchor = [
        r for r in row_results
        if r["confidence_lane"] == "LANE_A_HARD_MEASURED"
        and r["isotope"] != ANCHOR_ISOTOPE
    ]
    eps_arr = np.array([r["abs_eps"] for r in lane_a_non_anchor])
    sym = [r for r in lane_a_non_anchor if r["Z"] == r["N"]]
    asym = [r for r in lane_a_non_anchor if r["Z"] != r["N"]]
    return {
        "row_results": row_results,
        "n_lane_a_non_anchor": len(lane_a_non_anchor),
        "rms_eps_lane_a": float(np.sqrt(np.mean(eps_arr ** 2))),
        "max_eps_lane_a": float(eps_arr.max()),
        "median_eps_lane_a": float(np.median(eps_arr)),
        "frac_lt_0p001": float(np.mean(eps_arr < 0.001)),
        "frac_lt_0p005": float(np.mean(eps_arr < 0.005)),
        "frac_lt_0p01": float(np.mean(eps_arr < 0.01)),
        "n_symmetric": len(sym),
        "n_asymmetric": len(asym),
        "rms_eps_symmetric": _rms([r["abs_eps"] for r in sym]),
        "rms_eps_asymmetric": _rms([r["abs_eps"] for r in asym]),
    }


def _rms(values: list[float]) -> float:
    if not values:
        return float("nan")
    return math.sqrt(sum(v * v for v in values) / len(values))


# ------------------------------------------------------------
# Gate 3 — residual-axis structure
# ------------------------------------------------------------
def magic_distance(value: int) -> int:
    return min(abs(value - m) for m in MAGIC_NUMBERS)


def pairing_proxy(Z: int, N: int) -> int:
    """Bethe-Weizsäcker pairing-term proxy: +1 (e-e), 0 (mixed), -1 (o-o)."""
    z_even = Z % 2 == 0
    n_even = N % 2 == 0
    if z_even and n_even:
        return 1
    if (not z_even) and (not n_even):
        return -1
    return 0


def gate_3_residual_axes(
    row_results: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
) -> dict[str, Any]:
    R_radix = int(spine["R"])
    lane_a_non_anchor = [
        r for r in row_results
        if r["confidence_lane"] == "LANE_A_HARD_MEASURED"
        and r["isotope"] != ANCHOR_ISOTOPE
    ]
    delta_m = np.array([r["delta_m_u"] for r in lane_a_non_anchor])
    A_arr = np.array([r["A"] for r in lane_a_non_anchor])
    Z_arr = np.array([r["Z"] for r in lane_a_non_anchor])
    N_arr = np.array([r["N"] for r in lane_a_non_anchor])
    NmZ = N_arr - Z_arr

    axes = {
        "A": A_arr,
        "Z": Z_arr,
        "N": N_arr,
        "N_minus_Z": NmZ,
        "asymmetry_NmZ_squared_over_A": (NmZ ** 2) / A_arr,
        "surface_A_to_two_thirds": A_arr ** (2.0 / 3.0),
        "coulomb_Z_squared_over_A_third": (Z_arr ** 2) / (A_arr ** (1.0 / 3.0)),
        "coulomb_ZZminus1_over_A_third": (Z_arr * (Z_arr - 1)) / (A_arr ** (1.0 / 3.0)),
        "pairing_proxy": np.array([pairing_proxy(r["Z"], r["N"]) for r in lane_a_non_anchor]),
        "magic_min_distance": np.array(
            [min(magic_distance(r["Z"]), magic_distance(r["N"])) for r in lane_a_non_anchor]
        ),
    }

    results: dict[str, Any] = {}
    for name, axis in axes.items():
        if len(set(axis.tolist())) <= 1:
            results[name] = {
                "spearman_rho": float("nan"),
                "p_value": float("nan"),
                "note": "axis constant",
            }
            continue
        rho_result = spearmanr(delta_m, axis)
        rho = float(getattr(rho_result, "statistic", rho_result[0]))
        pv = float(getattr(rho_result, "pvalue", rho_result[1]))
        results[name] = {"spearman_rho": rho, "p_value": pv}

    abs_rhos = [
        abs(v["spearman_rho"]) for v in results.values()
        if isinstance(v["spearman_rho"], float) and not math.isnan(v["spearman_rho"])
    ]
    max_abs_rho = max(abs_rhos) if abs_rhos else float("nan")
    structured = max_abs_rho > 0.5

    # Specifically: BW axes flagged
    bw_axes = ["asymmetry_NmZ_squared_over_A", "surface_A_to_two_thirds",
               "coulomb_Z_squared_over_A_third", "coulomb_ZZminus1_over_A_third"]
    bw_structured = any(abs(results[a]["spearman_rho"]) > 0.5 for a in bw_axes
                        if a in results and not math.isnan(results[a]["spearman_rho"]))

    return {
        "axis_correlations": results,
        "max_abs_spearman": max_abs_rho,
        "structured_residual": structured,
        "bw_axis_structured": bw_structured,
    }


# ------------------------------------------------------------
# Gate 4 — typed candidates C0–C8
# ------------------------------------------------------------
def gate_4_candidates(
    spine: dict[str, sp.Rational],
    mu_Q: sp.Rational,
    avg_lane_a_per_A: sp.Rational,
) -> dict[str, Any]:
    kappa = spine["kappa"]
    g = spine["g"]
    aH = spine["alpha_H"]
    D = spine["D"]
    S = spine["S"]
    R = spine["R"]
    L = spine["L"]
    M = spine["M"]

    base = mu_Q * sp.Rational(4) * kappa  # = 1 u exactly
    candidates: list[dict[str, Any]] = [
        {
            "id": "C0", "formula": "μ_Q · 4κ",
            "typed_source": "anchor identity 4κ·μ_Q = 1 u",
            "value": base,
        },
        {
            "id": "C1", "formula": "μ_Q · (4κ − 8g)",
            "typed_source": "substrate-replaced excess-neutron: 7093/7117 u",
            "value": mu_Q * (sp.Rational(4) * kappa - sp.Rational(8) * g),
        },
        {
            "id": "C2", "formula": "μ_Q · (4κ + 8g)",
            "typed_source": "substrate-additive excess-neutron: 7141/7117 u",
            "value": mu_Q * (sp.Rational(4) * kappa + sp.Rational(8) * g),
        },
        {
            "id": "C3", "formula": "μ_Q · 4κ · (1 + g)",
            "typed_source": "binding correction at g (neutron-unit coupling)",
            "value": base * (sp.Rational(1) + g),
        },
        {
            "id": "C4", "formula": "μ_Q · 4κ · (1 + 1/(D²·S))",
            "typed_source": "binding correction at 1/(D²·S) = 1/72",
            "value": base * (sp.Rational(1) + sp.Rational(1) / (D ** 2 * S)),
        },
        {
            "id": "C5", "formula": "μ_Q · 4κ · (1 + 1/R²)",
            "typed_source": "cycle-budget surface unit 1/R² = 1/144",
            "value": base * (sp.Rational(1) + sp.Rational(1) / R ** 2),
        },
        {
            "id": "C6", "formula": "μ_Q · 4κ · (1 + g/α_H)",
            "typed_source": "face-halved neutron-unit g/α_H = 1/128",
            "value": base * (sp.Rational(1) + g / aH),
        },
        {
            "id": "C7", "formula": "μ_Q · 4κ · (1 + 1/M)",
            "typed_source": "matter-capacity reciprocal 1/M = 1/126",
            "value": base * (sp.Rational(1) + sp.Rational(1) / M),
        },
    ]

    # C8 — diagnostic
    c8 = {
        "id": "C8",
        "formula": "μ_Q · 4κ · 1/(S·ℒ)",
        "typed_source": "closed-ledger split diagnostic 1/(S·ℒ) = 1/1296",
        "value": base * (sp.Rational(1) / (S * L)),
        "diagnostic": True,
    }

    # Compute residuals for C0–C7 against four targets
    targets = {
        "m_p": M_PROTON_MEASURED_U,
        "m_n": M_NEUTRON_MEASURED_U,
        "H_1": M_HYDROGEN1_MEASURED_U,
        "avg_lane_a_per_nucleon": avg_lane_a_per_A,
    }
    STRICT = sp.Rational("0.001")
    LOOSE = sp.Rational("0.01")

    out_rows: list[dict[str, Any]] = []
    for cand in candidates:
        row = {
            "candidate_id": cand["id"],
            "formula": cand["formula"],
            "typed_source": cand["typed_source"],
            "canonical_value_u": float(cand["value"]),
            "canonical_value_rational": str(cand["value"]),
            "diagnostic": False,
        }
        for tname, tval in targets.items():
            dev = abs((cand["value"] - tval) / tval)
            row[f"residual_vs_{tname}"] = float(dev)
            row[f"strict_pass_{tname}"] = bool(dev < STRICT)
            row[f"loose_pass_{tname}"] = bool(dev < LOOSE)
        out_rows.append(row)

    # C8 — diagnostic against splittings
    splittings = {
        "m_n_minus_m_p": M_NEUTRON_MEASURED_U - M_PROTON_MEASURED_U,
        "H1_minus_m_p": M_HYDROGEN1_MEASURED_U - M_PROTON_MEASURED_U,
        "one_u_minus_substrate_excess": sp.Rational(1) - mu_Q * sp.Rational(24, 7117) * sp.Rational(7117, 24),
    }
    # Fix: one_u_minus_substrate_excess = 1 − μ_Q · (24/7117 · 7117/24) is wrong.
    # The CR240 precommit says: "1u − μ_Q · (4κ − 8g)" — but actually it's just the substrate per-excess-neutron contribution.
    # Substrate per excess neutron in u: μ_Q · S · g = (192/7117) · (1/8) = 24/7117 u.
    # So "1u − substrate_excess" = 1 − 24/7117 = 7093/7117 u.
    # That's the C1 value. So:
    splittings["one_u_minus_substrate_excess"] = sp.Rational(1) - sp.Rational(24, 7117)
    c8_row: dict[str, Any] = {
        "candidate_id": c8["id"],
        "formula": c8["formula"],
        "typed_source": c8["typed_source"],
        "canonical_value_u": float(c8["value"]),
        "canonical_value_rational": str(c8["value"]),
        "diagnostic": True,
    }
    for sname, sval in splittings.items():
        dev = abs((c8["value"] - sval) / sval)
        c8_row[f"residual_vs_{sname}"] = float(dev)
    out_rows.append(c8_row)

    # Aggregate: which candidates clear C-strict for any nucleon-mass target?
    cstrict_passes = []
    cloose_passes = []
    for row in out_rows[:-1]:  # exclude C8
        for tname in targets:
            if row.get(f"strict_pass_{tname}"):
                cstrict_passes.append((row["candidate_id"], tname,
                                       row[f"residual_vs_{tname}"]))
            if row.get(f"loose_pass_{tname}"):
                cloose_passes.append((row["candidate_id"], tname,
                                      row[f"residual_vs_{tname}"]))

    # Identify lowest-residual per target (across C0–C7)
    lowest_per_target = {}
    for tname in targets:
        best = min(out_rows[:-1], key=lambda r: r[f"residual_vs_{tname}"])
        lowest_per_target[tname] = {
            "candidate_id": best["candidate_id"],
            "residual": best[f"residual_vs_{tname}"],
            "value_u": best["canonical_value_u"],
        }

    return {
        "rows": out_rows,
        "strict_passes": cstrict_passes,
        "loose_passes": cloose_passes,
        "lowest_per_target": lowest_per_target,
        "any_strict_pass": len(cstrict_passes) > 0,
    }


# ------------------------------------------------------------
# Wrong controls
# ------------------------------------------------------------
def wc1_substrate_as_rest_mass(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
) -> dict[str, Any]:
    """Re-run Gate 2 with Q_substrate as the rest-mass kernel."""
    anchor_row = next(r for r in isotopes if r["isotope"] == ANCHOR_ISOTOPE)
    Q_anchor = Q_substrate(anchor_row["Z"], anchor_row["N"], spine)
    mu_Q_wc = sp.Rational(12) / Q_anchor
    eps_list = []
    for r in isotopes:
        if (r["confidence_lane"] != "LANE_A_HARD_MEASURED"
                or r["isotope"] == ANCHOR_ISOTOPE):
            continue
        Q_sub = Q_substrate(r["Z"], r["N"], spine)
        m_pred = mu_Q_wc * Q_sub
        eps = float(abs((r["atomic_mass_u"] - m_pred) / r["atomic_mass_u"]))
        eps_list.append(eps)
    return {
        "wc_id": "WC1",
        "perturbation": "substrate-as-rest-mass kernel",
        "mu_Q": str(mu_Q_wc),
        "n_rows": len(eps_list),
        "rms_eps": _rms(eps_list),
    }


def wc2_he4_anchor(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    mu_Q_canonical: sp.Rational,
) -> dict[str, Any]:
    """Re-anchor at He-4. μ_Q should be invariant up to binding-energy difference."""
    mu_Q_he4, Q_anchor_he4 = anchor_mu_Q_mass(
        isotopes, spine, SECONDARY_ANCHOR_ISOTOPE,
        sp.Rational(SECONDARY_ANCHOR_MASS_U_STR)
    )
    drift = float(abs(mu_Q_he4 / mu_Q_canonical - 1))
    return {
        "wc_id": "WC2",
        "perturbation": "He-4 anchor swap",
        "mu_Q_canonical": str(mu_Q_canonical),
        "mu_Q_he4": str(sp.simplify(mu_Q_he4)),
        "mu_Q_he4_float": float(mu_Q_he4),
        "abs_relative_drift": drift,
        "passes_strong": drift < 0.005,
        "passes_boundary": drift < 0.01,
    }


def wc3_random_per_nucleon_scale(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    mu_Q: sp.Rational,
    seed: int,
) -> dict[str, Any]:
    """Perturb per-nucleon mass scale: m(P) = A · (1 + δ_P) · u, seeded random δ."""
    rng = np.random.default_rng(seed)
    eps_list = []
    for r in isotopes:
        if (r["confidence_lane"] != "LANE_A_HARD_MEASURED"
                or r["isotope"] == ANCHOR_ISOTOPE):
            continue
        delta = rng.normal(0.0, 0.05)
        m_pred = r["A"] * (1.0 + delta)
        eps = abs(float(r["atomic_mass_u"]) - m_pred) / float(r["atomic_mass_u"])
        eps_list.append(eps)
    return {
        "wc_id": "WC3",
        "perturbation": f"random per-nucleon scale, seed={seed}",
        "n_rows": len(eps_list),
        "rms_eps": _rms(eps_list),
    }


def wc4_constant_per_nucleon(
    isotopes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Test m = A · c for c ∈ {0.5, 1.5, 2.0} (u-units). c=1 is canonical."""
    out = {}
    for c in (0.5, 1.5, 2.0):
        eps_list = []
        for r in isotopes:
            if (r["confidence_lane"] != "LANE_A_HARD_MEASURED"
                    or r["isotope"] == ANCHOR_ISOTOPE):
                continue
            m_pred = r["A"] * c
            eps = abs(float(r["atomic_mass_u"]) - m_pred) / float(r["atomic_mass_u"])
            eps_list.append(eps)
        out[f"c_{c}"] = {"n_rows": len(eps_list), "rms_eps": _rms(eps_list)}
    return {
        "wc_id": "WC4",
        "perturbation": "constant per-nucleon scale m=A·c, c∈{0.5,1.5,2.0}",
        "results": out,
    }


def wc5_no_binding_kernel(
    isotopes: list[dict[str, Any]],
) -> dict[str, Any]:
    """m_no_binding(P) = Z·m_p + N·m_n. Residual = -binding energy."""
    m_p = float(M_PROTON_MEASURED_U)
    m_n = float(M_NEUTRON_MEASURED_U)
    rows = []
    for r in isotopes:
        if (r["confidence_lane"] != "LANE_A_HARD_MEASURED"
                or r["isotope"] == ANCHOR_ISOTOPE):
            continue
        m_pred = r["Z"] * m_p + r["N"] * m_n
        delta = float(r["atomic_mass_u"]) - m_pred
        rows.append({
            "isotope": r["isotope"],
            "Z": r["Z"],
            "N": r["N"],
            "A": r["A"],
            "m_no_binding_u": m_pred,
            "m_measured_u": float(r["atomic_mass_u"]),
            "binding_residual_u": delta,
        })
    # Residual structure check via Spearman
    deltas = np.array([r["binding_residual_u"] for r in rows])
    NmZ_sq_over_A = np.array(
        [((r["N"] - r["Z"]) ** 2) / r["A"] for r in rows]
    )
    A_arr = np.array([r["A"] for r in rows])
    rho_asym = spearmanr(deltas, NmZ_sq_over_A)
    rho_asym_val = float(getattr(rho_asym, "statistic", rho_asym[0]))
    rho_A = spearmanr(deltas, A_arr)
    rho_A_val = float(getattr(rho_A, "statistic", rho_A[0]))
    return {
        "wc_id": "WC5",
        "perturbation": "Z·m_p + N·m_n no-binding kernel",
        "n_rows": len(rows),
        "rms_residual_u": _rms([abs(r["binding_residual_u"]) for r in rows]),
        "spearman_residual_vs_asymmetry": rho_asym_val,
        "spearman_residual_vs_A": rho_A_val,
        "bw_asymmetry_structured": abs(rho_asym_val) > 0.5,
    }


def wc6_axis_shuffle(
    row_results: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    seed: int,
) -> dict[str, Any]:
    """Shuffle one axis label vs delta_m. Spearman should drop to noise."""
    rng = np.random.default_rng(seed)
    lane_a_non_anchor = [
        r for r in row_results
        if r["confidence_lane"] == "LANE_A_HARD_MEASURED"
        and r["isotope"] != ANCHOR_ISOTOPE
    ]
    delta_m = np.array([r["delta_m_u"] for r in lane_a_non_anchor])
    NmZ = np.array([r["N"] - r["Z"] for r in lane_a_non_anchor])
    NmZ_sq_over_A = (NmZ ** 2) / np.array([r["A"] for r in lane_a_non_anchor])
    # Shuffle NmZ_sq_over_A
    perm = rng.permutation(len(NmZ_sq_over_A))
    shuffled = NmZ_sq_over_A[perm]
    rho_result = spearmanr(delta_m, shuffled)
    rho_shuffled = float(getattr(rho_result, "statistic", rho_result[0]))
    rho_orig_result = spearmanr(delta_m, NmZ_sq_over_A)
    rho_orig = float(getattr(rho_orig_result, "statistic", rho_orig_result[0]))
    return {
        "wc_id": "WC6",
        "perturbation": f"random axis-label shuffle, seed={seed}",
        "rho_original_asymmetry": rho_orig,
        "rho_shuffled_asymmetry": rho_shuffled,
        "shuffled_drops_to_noise": abs(rho_shuffled) < 0.3,
    }


# ------------------------------------------------------------
# Disallowed-claim scan
# ------------------------------------------------------------
DISALLOWED_PHRASES = (
    "CR240 falsifies the CR238 substrate kernel",
    "CR240 derives m_n exactly",
    "Q(P) and Q_mass(P) are the same quantity",
    "Binding energy is reduced to typed primitives",
    "A candidate was discovered after seeing the data",
)


def scan_disallowed_claims(text: str) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []
    lower = text.lower()
    for phrase in DISALLOWED_PHRASES:
        idx = 0
        while True:
            pos = lower.find(phrase.lower(), idx)
            if pos < 0:
                break
            line_no = text[:pos].count("\n") + 1
            flags.append({"phrase": phrase, "position": pos, "line": line_no})
            idx = pos + len(phrase)
    return flags


# ------------------------------------------------------------
# Verdict
# ------------------------------------------------------------
def assign_verdict(
    gate_1: dict[str, Any],
    gate_2: dict[str, Any],
    gate_3: dict[str, Any],
    gate_4: dict[str, Any],
    wcs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    # STRONG
    S1 = gate_1["all_pass"]
    S2 = gate_2["rms_eps_lane_a"] < 0.005
    S3 = gate_3["bw_axis_structured"]
    S4 = gate_4["any_strict_pass"]
    S5 = wcs["WC2"]["passes_strong"]

    strong = S1 and S2 and S3 and S4 and S5

    # BOUNDARY
    B1 = gate_1["all_pass"]
    B2 = gate_2["rms_eps_lane_a"] < 0.01
    B3 = gate_3["structured_residual"] and not S4
    B4 = wcs["WC2"]["passes_boundary"]
    boundary = B1 and B2 and B3 and B4 and not strong

    # FAIL
    F1 = not gate_1["all_pass"]
    F2 = gate_2["rms_eps_lane_a"] > 0.05
    F3 = not gate_3["structured_residual"]
    F4 = wcs["WC2"]["abs_relative_drift"] > 0.05
    fail = (F1 or F2 or F3 or F4) and not strong and not boundary

    if strong:
        verdict = "STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED"
    elif boundary:
        verdict = "BOUNDARY_CR240_REST_MASS_CHANNEL_WITH_BINDING_CURVE"
    elif fail:
        verdict = "FAIL_CR240_REST_MASS_CHANNEL"
    else:
        verdict = "UNCLASSIFIED"

    return {
        "verdict": verdict,
        "STRONG": {"S1": S1, "S2": S2, "S3": S3, "S4": S4, "S5": S5,
                   "all": strong},
        "BOUNDARY": {"B1": B1, "B2": B2, "B3": B3, "B4": B4, "all": boundary},
        "FAIL": {"F1": F1, "F2": F2, "F3": F3, "F4": F4, "any": fail},
    }


# ------------------------------------------------------------
# Output emission
# ------------------------------------------------------------
def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})


def main() -> int:
    shas = assert_input_shas()
    spine = cr238_spine()

    # Verify CR238 atoms
    assert spine["kappa"] == sp.Rational(7117, 768)
    assert spine["g"] == sp.Rational(1, 64)
    assert spine["S"] == sp.Rational(8)
    assert spine["M"] == sp.Rational(126)
    assert spine["R"] == sp.Rational(12)
    assert spine["L"] == sp.Rational(162)

    isotopes = load_isotopes()

    # Anchor μ_Q at C-12 with extended kernel
    mu_Q, Q_anchor = anchor_mu_Q_mass(isotopes, spine, ANCHOR_ISOTOPE, ANCHOR_MASS_U)
    assert mu_Q == sp.Rational(192, 7117), f"mu_Q mismatch: {mu_Q}"
    assert Q_anchor == sp.Rational(7117, 16), f"Q_anchor mismatch: {Q_anchor}"

    # Compute avg Lane A per-nucleon mass for Gate 4 target
    lane_a = [r for r in isotopes if r["confidence_lane"] == "LANE_A_HARD_MEASURED"]
    avg_per_A = sum(r["atomic_mass_u"] / sp.Rational(r["A"]) for r in lane_a) / sp.Rational(len(lane_a))

    # Run gates
    g1 = gate_1_algebraic(spine)
    g2 = gate_2_extended_kernel(isotopes, spine, mu_Q)
    g3 = gate_3_residual_axes(g2["row_results"], spine)
    g4 = gate_4_candidates(spine, mu_Q, avg_per_A)

    # Run wrong controls
    wcs: dict[str, dict[str, Any]] = {}
    wcs["WC1"] = wc1_substrate_as_rest_mass(isotopes, spine)
    wcs["WC2"] = wc2_he4_anchor(isotopes, spine, mu_Q)
    wcs["WC3"] = wc3_random_per_nucleon_scale(isotopes, spine, mu_Q, RANDOM_SCALE_SEED)
    wcs["WC4"] = wc4_constant_per_nucleon(isotopes)
    wcs["WC5"] = wc5_no_binding_kernel(isotopes)
    wcs["WC6"] = wc6_axis_shuffle(g2["row_results"], spine, AXIS_SHUFFLE_SEED)

    verdict = assign_verdict(g1, g2, g3, g4, wcs)

    # ----- Write per-row / per-pair outputs -----
    out_dir = SCRIPT_DIR

    # Gate 2 predictions
    write_csv(
        out_dir / "CR240_extended_kernel_predictions.csv",
        [{k: str(v) for k, v in r.items()} for r in g2["row_results"]],
    )
    # Gate 3 axis correlations
    g3_rows = []
    for axis, info in g3["axis_correlations"].items():
        g3_rows.append({
            "axis": axis,
            "spearman_rho": info.get("spearman_rho", ""),
            "p_value": info.get("p_value", ""),
            "note": info.get("note", ""),
        })
    g3_rows.append({
        "axis": "AGGREGATE",
        "spearman_rho": g3["max_abs_spearman"],
        "p_value": "",
        "note": f"structured_residual={g3['structured_residual']}; "
                f"bw_axis_structured={g3['bw_axis_structured']}",
    })
    write_csv(
        out_dir / "CR240_residual_axis_correlations.csv",
        [{k: str(v) for k, v in r.items()} for r in g3_rows],
    )
    # Gate 4 candidates
    write_csv(
        out_dir / "CR240_candidate_typed_values.csv",
        [{k: str(v) for k, v in r.items()} for r in g4["rows"]],
    )
    # Wrong controls flat
    wc_rows = []
    for wc_id, info in wcs.items():
        flat = {"wc_id": wc_id, "perturbation": info.get("perturbation", "")}
        for k, v in info.items():
            if k in ("wc_id", "perturbation"):
                continue
            flat[k] = str(v)
        wc_rows.append(flat)
    write_csv(
        out_dir / "CR240_wrong_controls.csv",
        wc_rows,
    )

    # ----- Summary JSON -----
    summary = {
        "verdict": verdict["verdict"],
        "input_shas": shas,
        "kernel_atoms": {
            "F": int(spine["F"]),
            "S": int(spine["S"]),
            "alpha_H": int(spine["alpha_H"]),
            "D": int(spine["D"]),
            "R": int(spine["R"]),
            "L": int(spine["L"]),
            "M": int(spine["M"]),
            "kappa": str(spine["kappa"]),
            "g": str(spine["g"]),
        },
        "anchor": {
            "isotope": ANCHOR_ISOTOPE,
            "mass_u": str(ANCHOR_MASS_U),
            "Q_mass_anchor": str(Q_anchor),
            "mu_Q": str(mu_Q),
            "mu_Q_float": float(mu_Q),
        },
        "avg_lane_a_per_nucleon_u": float(avg_per_A),
        "gate_1_algebraic": {
            "G1_1": g1["G1_1_Q_mass_C12_eq_7117_over_16"],
            "G1_2": g1["G1_2_m_SAM_C12_eq_12u"],
            "G1_3_all_pass": g1["G1_3_all_pass"],
            "G1_4": g1["G1_4_Q_mass_minus_Q_sub_eq_NminusZ_7093_192"],
            "G1_5": g1["G1_5_mu_Q_per_excess_eq_7093_7117"],
            "all_pass": g1["all_pass"],
        },
        "gate_2_extended_kernel": {
            "n_lane_a_non_anchor": g2["n_lane_a_non_anchor"],
            "rms_eps_lane_a": g2["rms_eps_lane_a"],
            "max_eps_lane_a": g2["max_eps_lane_a"],
            "median_eps_lane_a": g2["median_eps_lane_a"],
            "frac_lt_0p001": g2["frac_lt_0p001"],
            "frac_lt_0p005": g2["frac_lt_0p005"],
            "frac_lt_0p01": g2["frac_lt_0p01"],
            "n_symmetric": g2["n_symmetric"],
            "n_asymmetric": g2["n_asymmetric"],
            "rms_eps_symmetric": g2["rms_eps_symmetric"],
            "rms_eps_asymmetric": g2["rms_eps_asymmetric"],
        },
        "gate_3_residual_axes": {
            "max_abs_spearman": g3["max_abs_spearman"],
            "structured_residual": g3["structured_residual"],
            "bw_axis_structured": g3["bw_axis_structured"],
            "axis_correlations": {
                k: {kk: vv for kk, vv in v.items()}
                for k, v in g3["axis_correlations"].items()
            },
        },
        "gate_4_candidates": {
            "any_strict_pass": g4["any_strict_pass"],
            "strict_passes": [list(p) for p in g4["strict_passes"]],
            "loose_passes": [list(p) for p in g4["loose_passes"]],
            "lowest_per_target": g4["lowest_per_target"],
        },
        "wrong_controls": {wc_id: info for wc_id, info in wcs.items()},
        "verdict_logic": verdict,
    }

    summary_text = json.dumps(summary, indent=2, sort_keys=True, default=str)
    flags = scan_disallowed_claims(summary_text)
    summary["disallowed_claim_flags"] = flags

    with open(out_dir / "CR240_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True, default=str)

    # ----- Print verdict line -----
    print(f"CR240 verdict: {verdict['verdict']}")
    print(f"  Gate 1 algebraic identities: all_pass = {g1['all_pass']}")
    print(f"  Gate 2 extended kernel (m_SAM = A·u): "
          f"n={g2['n_lane_a_non_anchor']}, RMS={g2['rms_eps_lane_a']:.6f}, "
          f"frac<0.5%={g2['frac_lt_0p005']:.3f}")
    print(f"    sym RMS={g2['rms_eps_symmetric']:.6f}, "
          f"asym RMS={g2['rms_eps_asymmetric']:.6f}")
    print(f"  Gate 3 residual structure: max|ρ_S|={g3['max_abs_spearman']:.4f}, "
          f"BW-axis structured={g3['bw_axis_structured']}")
    print(f"  Gate 4 candidates (C0-C7 vs m_p, m_n, H-1, avg per-nucleon):")
    print(f"    any strict pass = {g4['any_strict_pass']}")
    if g4["strict_passes"]:
        for cid, target, dev in g4["strict_passes"]:
            print(f"      {cid} clears strict vs {target}: residual={dev:.6f}")
    print(f"    lowest residual per target:")
    for tname, info in g4["lowest_per_target"].items():
        print(f"      {tname}: {info['candidate_id']} "
              f"(residual={info['residual']:.6f})")
    print(f"  Wrong controls:")
    print(f"    WC1 substrate-as-rest-mass: RMS={wcs['WC1']['rms_eps']:.6f} "
          f"(× canonical: {wcs['WC1']['rms_eps'] / g2['rms_eps_lane_a']:.1f})")
    print(f"    WC2 He-4 anchor drift: {wcs['WC2']['abs_relative_drift']:.6f} "
          f"(strong<0.005: {wcs['WC2']['passes_strong']})")
    print(f"    WC3 random per-nucleon: RMS={wcs['WC3']['rms_eps']:.6f}")
    print(f"    WC5 no-binding residual: ρ_S(asym)={wcs['WC5']['spearman_residual_vs_asymmetry']:.4f}")
    print(f"    WC6 axis shuffle: orig ρ={wcs['WC6']['rho_original_asymmetry']:.4f}, "
          f"shuffled ρ={wcs['WC6']['rho_shuffled_asymmetry']:.4f}")
    print(f"  Disallowed-claim flags in summary: {len(flags)}")

    overall_ok = verdict["verdict"] not in ("FAIL_CR240_REST_MASS_CHANNEL",
                                              "UNCLASSIFIED")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
