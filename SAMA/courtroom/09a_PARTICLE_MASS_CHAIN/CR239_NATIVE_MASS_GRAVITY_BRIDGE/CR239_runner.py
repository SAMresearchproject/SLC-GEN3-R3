"""CR239 Native Mass / Gravity Bridge — Runner.

Sealed precommit SHA-256:
    52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7

Hypothesis under test (from CR238 + CR239 lock):
    Q(P)  =  S · G(Z, N)  =  8 · [ Z·κ + (N − Z)·g ]
    m_i(P) = m_g(P)        =  μ_Q · Q(P)
    A_P(r)                 =  2 · G_N · μ_Q · Q(P) / (c² · r)

The runner asks whether one global μ_Q (anchored at C-12 = 12u exactly) converts
the CR238 typed Q(P) into measured atomic mass.

Five gates:
    Gate 1 — ratio test (no μ_Q): m_i/m_j ?= Q_i/Q_j
    Gate 2 — one-anchor unit bridge: μ_Q = 12u / Q(C-12); predict every other row
    Gate 3 — isotope increment: Δm per neutron = μ_Q · S·g = μ_Q / 8
    Gate 4 — residual structure: Spearman ρ_S of Δm vs (N−Z), A, Z,
             magic-shell distance, radix-cycle position, parity
    Gate 5 — gravitational-source readout (documented; NOT RUN in v1)

Four confidence lanes:
    Lane A — hard-measured (only lane where hard-fail is allowed)
    Lane B — evaluated (uncertainty-weighted z-scores)
    Lane C — extrapolated / frontier (forward predictions; not a hard-fail lane)
    Lane D — post-evaluation challenge (reserved; not run in v1)

Nine wrong controls:
    WC1–WC3 — R = 10, 11, 13 (kernel-radix perturbation)
    WC4–WC5 — S = 7, 9 (split perturbation)
    WC6     — shuffled N(Z) with seed 20260621
    WC7     — shuffled Q(P) with seed 20260621
    WC8     — monotone random ladder
    WC9     — A = Z + N baseline (most important practical control)

Verdict spectrum (precedence STRONG > BOUNDARY > PREDICTION > FAIL):
    STRONG_PASS    : direct bridge holds
    BOUNDARY_PASS  : source skeleton + structured residual
    PREDICTION     : forward-prediction conflict with evaluated/extrapolated layer
    FAIL           : Q(P) does not beat A = Z + N, OR residual unstructured,
                     OR μ_Q drifts under shuffle re-anchor

All arithmetic uses sympy.Rational for exact rationals where possible (Q, κ, g, μ_Q).
Statistical aggregates use float64 (numpy / scipy.stats).
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
SHUFFLE_SEED = 20260621
MAGIC_NUMBERS = (2, 8, 20, 28, 50, 82, 126)
# CR238_LITERAL_SCAN: INPUT_BOUNDARY_END


SCRIPT_DIR = Path(__file__).parent
SCRIPT_PATH = Path(__file__).resolve()
INPUT_CSV = SCRIPT_DIR / "CR239_measured_isotope_masses.csv"
PRECOMMIT_PATH = SCRIPT_DIR / "CR239_PRECOMMIT.md"
CR238_PRECOMMIT = SCRIPT_DIR.parent / "CR238_SUBSTRATE_SPINE_COMPACTION" / "CR238_PRECOMMIT.md"
CR238_RESULT = SCRIPT_DIR.parent / "CR238_SUBSTRATE_SPINE_COMPACTION" / "CR238_result.md"
DESIGN_DOC = SCRIPT_DIR.parent.parent / "CR239_SAFER_NATIVE_MASS_GRAVITY_BRIDGE_DESIGN.md"

EXPECTED_INPUT_CSV_SHA = (
    "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
)
EXPECTED_CR239_PRECOMMIT_SHA = (
    "52c9475bbe06b87de620aa42d89fff069dc4cb7473136d300d603d865afdd0d7"
)
EXPECTED_CR238_PRECOMMIT_SHA = (
    "5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293"
)
EXPECTED_CR238_RESULT_SHA = (
    "7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef"
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
        "cr239_input_csv": (INPUT_CSV, EXPECTED_INPUT_CSV_SHA),
        "cr239_precommit": (PRECOMMIT_PATH, EXPECTED_CR239_PRECOMMIT_SHA),
        "cr238_precommit": (CR238_PRECOMMIT, EXPECTED_CR238_PRECOMMIT_SHA),
        "cr238_result": (CR238_RESULT, EXPECTED_CR238_RESULT_SHA),
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
# CR238 typed spine — read-only inputs to CR239
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
    kappa = (R - sp.Rational(1)) * (F * S - sp.Rational(1)) / (D * aH ** S)
    g = sp.Rational(1) / S ** 2
    return {
        "F": F,
        "S": S,
        "alpha_H": aH,
        "L": L,
        "D": D,
        "V": V,
        "Theta": Theta,
        "R": R,
        "kappa": sp.simplify(kappa),
        "g": sp.simplify(g),
    }


def Q_canonical(Z: int, N: int, spine: dict[str, sp.Rational]) -> sp.Rational:
    """Canonical Q(Z, N) = S · [Z·κ + (N−Z)·g] from the CR238 typed spine."""
    Z_r = sp.Rational(Z)
    N_r = sp.Rational(N)
    G = Z_r * spine["kappa"] + (N_r - Z_r) * spine["g"]
    return sp.simplify(spine["S"] * G)


# ------------------------------------------------------------
# Load measured isotopes
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
                    "measurement_class": r["measurement_class"],
                    "source_table": r["source_table"],
                    "confidence_lane": r["confidence_lane"],
                    "notes": r["notes"],
                }
            )
    return rows


# ------------------------------------------------------------
# Q with arbitrary R and S (for wrong controls)
# ------------------------------------------------------------
def Q_with_R_S(
    Z: int, N: int, R_val: int, S_val: int, F: sp.Rational, aH: sp.Rational, D: sp.Rational
) -> sp.Rational:
    """Recompute Q(Z, N) under perturbed R and/or S.

    κ' = (R' − 1)(ℱ·S' − 1) / (D · α_H^S')
    g' = 1 / S'²
    Q' = S' · [Z·κ' + (N − Z)·g']
    """
    R_r = sp.Rational(R_val)
    S_r = sp.Rational(S_val)
    kappa_p = (R_r - 1) * (F * S_r - 1) / (D * aH ** S_r)
    g_p = sp.Rational(1) / S_r ** 2
    Z_r = sp.Rational(Z)
    N_r = sp.Rational(N)
    G_p = Z_r * kappa_p + (N_r - Z_r) * g_p
    return sp.simplify(S_r * G_p)


# ------------------------------------------------------------
# Anchor μ_Q
# ------------------------------------------------------------
def anchor_mu_Q(
    isotopes: list[dict[str, Any]],
    Q_func,
    anchor_isotope: str = ANCHOR_ISOTOPE,
    anchor_mass_u: sp.Rational = ANCHOR_MASS_U,
) -> tuple[sp.Rational, sp.Rational]:
    """Return (μ_Q, Q_anchor) for the given Q function on the canonical
    isotope row. Q_func takes (Z, N) and returns a sympy Rational.
    """
    anchor_row = next(r for r in isotopes if r["isotope"] == anchor_isotope)
    Q_anchor = Q_func(anchor_row["Z"], anchor_row["N"])
    mu_Q = anchor_mass_u / Q_anchor
    return mu_Q, Q_anchor


# ------------------------------------------------------------
# Predict masses + residuals
# ------------------------------------------------------------
def predict_masses(
    isotopes: list[dict[str, Any]],
    Q_func,
    mu_Q: sp.Rational,
) -> list[dict[str, Any]]:
    """For each isotope, predict m_SAM and ε; return per-row results."""
    out: list[dict[str, Any]] = []
    for r in isotopes:
        Z, N = r["Z"], r["N"]
        Q = Q_func(Z, N)
        m_pred = mu_Q * Q
        m_meas = r["atomic_mass_u"]
        if m_meas == 0:
            eps = float("nan")
        else:
            eps = float((m_meas - m_pred) / m_meas)
        out.append(
            {
                "isotope": r["isotope"],
                "Z": Z,
                "N": N,
                "A": r["A"],
                "Q": float(Q),
                "Q_rational": str(Q),
                "m_meas_u": r["atomic_mass_u_float"],
                "m_pred_u": float(m_pred),
                "eps": eps,
                "abs_eps": abs(eps),
                "delta_m_u": float(m_meas - m_pred),
                "confidence_lane": r["confidence_lane"],
                "mass_uncertainty_u": r["mass_uncertainty_u"],
            }
        )
    return out


# ------------------------------------------------------------
# Aggregate statistics
# ------------------------------------------------------------
def rms(values: list[float]) -> float:
    if not values:
        return float("nan")
    return math.sqrt(sum(v * v for v in values) / len(values))


def safe_div(a: float, b: float) -> float:
    return a / b if b != 0 else float("inf")


# ------------------------------------------------------------
# Gate 1 — Ratio test
# ------------------------------------------------------------
def gate_1_ratio_test(
    isotopes: list[dict[str, Any]],
    Q_func,
) -> dict[str, Any]:
    """For all Lane A pairs, compute ε^ratio = |(m_i/m_j)/(Q_i/Q_j) − 1|."""
    lane_a = [r for r in isotopes if r["confidence_lane"] == "LANE_A_HARD_MEASURED"]
    pair_results: list[dict[str, Any]] = []
    eps_values: list[float] = []
    for i in range(len(lane_a)):
        for j in range(i + 1, len(lane_a)):
            P_i = lane_a[i]
            P_j = lane_a[j]
            m_i = P_i["atomic_mass_u"]
            m_j = P_j["atomic_mass_u"]
            Q_i = Q_func(P_i["Z"], P_i["N"])
            Q_j = Q_func(P_j["Z"], P_j["N"])
            if m_j == 0 or Q_j == 0 or Q_i == 0:
                continue
            ratio_m = m_i / m_j
            ratio_Q = Q_i / Q_j
            eps = abs(float(ratio_m / ratio_Q - 1))
            eps_values.append(eps)
            pair_results.append(
                {
                    "isotope_i": P_i["isotope"],
                    "isotope_j": P_j["isotope"],
                    "m_ratio": float(ratio_m),
                    "Q_ratio": float(ratio_Q),
                    "eps_ratio": eps,
                }
            )
    n = len(eps_values)
    eps_arr = np.array(eps_values)
    return {
        "n_pairs": n,
        "rms_eps": float(np.sqrt(np.mean(eps_arr ** 2))),
        "median_eps": float(np.median(eps_arr)),
        "max_eps": float(np.max(eps_arr)),
        "frac_lt_0p01": float(np.mean(eps_arr < 0.01)),
        "frac_lt_0p05": float(np.mean(eps_arr < 0.05)),
        "frac_lt_0p10": float(np.mean(eps_arr < 0.10)),
        "pair_results": pair_results,
    }


# ------------------------------------------------------------
# Gate 2 — One-anchor unit bridge
# ------------------------------------------------------------
def gate_2_anchor_bridge(
    isotopes: list[dict[str, Any]],
    Q_func,
    mu_Q: sp.Rational,
) -> dict[str, Any]:
    """Anchor at C-12, predict every Lane A row, report residuals."""
    rows = predict_masses(isotopes, Q_func, mu_Q)
    lane_a_rows = [
        r for r in rows
        if r["confidence_lane"] == "LANE_A_HARD_MEASURED"
        and r["isotope"] != ANCHOR_ISOTOPE
    ]
    abs_eps_a = [r["abs_eps"] for r in lane_a_rows]
    sym = [r for r in lane_a_rows if r["Z"] == r["N"]]
    asym = [r for r in lane_a_rows if r["Z"] != r["N"]]
    sym_rms = rms([r["abs_eps"] for r in sym])
    asym_rms = rms([r["abs_eps"] for r in asym])
    eps_arr = np.array(abs_eps_a)
    return {
        "n_lane_a_non_anchor": len(lane_a_rows),
        "rms_eps_lane_a": rms(abs_eps_a),
        "max_eps_lane_a": float(eps_arr.max()),
        "median_eps_lane_a": float(np.median(eps_arr)),
        "frac_lt_0p01": float(np.mean(eps_arr < 0.01)),
        "frac_lt_0p05": float(np.mean(eps_arr < 0.05)),
        "n_symmetric": len(sym),
        "n_asymmetric": len(asym),
        "rms_eps_symmetric": sym_rms,
        "rms_eps_asymmetric": asym_rms,
        "row_results": rows,
    }


# ------------------------------------------------------------
# Gate 3 — Isotope increment
# ------------------------------------------------------------
def gate_3_isotope_increment(
    isotopes: list[dict[str, Any]],
    Q_func,
    mu_Q: sp.Rational,
) -> dict[str, Any]:
    """For fixed Z varying N by one in Lane A, compare Δm_measured to Δm_SAM."""
    lane_a = [r for r in isotopes if r["confidence_lane"] == "LANE_A_HARD_MEASURED"]
    # Index by Z
    by_Z: dict[int, list[dict[str, Any]]] = {}
    for r in lane_a:
        by_Z.setdefault(r["Z"], []).append(r)
    spine = cr238_spine()
    dm_SAM_per_neutron = mu_Q * spine["S"] * spine["g"]
    pair_results: list[dict[str, Any]] = []
    R_values: list[float] = []
    for Z, members in by_Z.items():
        if len(members) < 2:
            continue
        members_sorted = sorted(members, key=lambda r: r["N"])
        for k in range(len(members_sorted) - 1):
            r_i = members_sorted[k]
            r_j = members_sorted[k + 1]
            dN = r_j["N"] - r_i["N"]
            dm_measured = r_j["atomic_mass_u"] - r_i["atomic_mass_u"]
            dm_predicted = dN * dm_SAM_per_neutron
            R = float(dm_measured / dm_predicted) if dm_predicted != 0 else float("inf")
            R_values.append(R)
            pair_results.append(
                {
                    "isotope_i": r_i["isotope"],
                    "isotope_j": r_j["isotope"],
                    "Z": Z,
                    "dN": dN,
                    "dm_measured_u": float(dm_measured),
                    "dm_SAM_predicted_u": float(dm_predicted),
                    "R": R,
                    "abs_R_minus_1": abs(R - 1),
                }
            )
    R_arr = np.array(R_values)
    return {
        "n_pairs": len(R_values),
        "mean_R": float(np.mean(R_arr)),
        "median_R": float(np.median(R_arr)),
        "std_R": float(np.std(R_arr)),
        "frac_R_within_0p05": float(np.mean(np.abs(R_arr - 1) < 0.05)),
        "frac_R_within_0p50": float(np.mean(np.abs(R_arr - 1) < 0.50)),
        "dm_SAM_per_neutron_u": float(dm_SAM_per_neutron),
        "dm_SAM_per_neutron_rational": str(dm_SAM_per_neutron),
        "pair_results": pair_results,
    }


# ------------------------------------------------------------
# Gate 4 — Residual-structure test
# ------------------------------------------------------------
def magic_shell_distance(value: int) -> int:
    """Minimum distance from value to the nearest magic number."""
    return min(abs(value - m) for m in MAGIC_NUMBERS)


def gate_4_residual_structure(
    gate_2_rows: list[dict[str, Any]],
    R_radix: int,
) -> dict[str, Any]:
    """Compute Spearman rank correlation between Δm(P) and six structural axes."""
    lane_a_non_anchor = [
        r for r in gate_2_rows
        if r["confidence_lane"] == "LANE_A_HARD_MEASURED"
        and r["isotope"] != ANCHOR_ISOTOPE
    ]
    delta_m = np.array([r["delta_m_u"] for r in lane_a_non_anchor])
    N_minus_Z = np.array([r["N"] - r["Z"] for r in lane_a_non_anchor])
    A_arr = np.array([r["A"] for r in lane_a_non_anchor])
    Z_arr = np.array([r["Z"] for r in lane_a_non_anchor])
    magic_Z_dist = np.array([magic_shell_distance(r["Z"]) for r in lane_a_non_anchor])
    magic_N_dist = np.array([magic_shell_distance(r["N"]) for r in lane_a_non_anchor])
    magic_min_dist = np.minimum(magic_Z_dist, magic_N_dist)
    radix_cycle = np.array([(r["Z"] - 1) % R_radix for r in lane_a_non_anchor])
    parity = np.array([(r["N"] - r["Z"]) % 2 for r in lane_a_non_anchor])

    axes = {
        "N_minus_Z": N_minus_Z,
        "A": A_arr,
        "Z": Z_arr,
        "magic_Z_distance": magic_Z_dist,
        "magic_N_distance": magic_N_dist,
        "magic_min_distance": magic_min_dist,
        "radix_cycle_position": radix_cycle,
        "N_minus_Z_parity": parity,
    }

    results: dict[str, Any] = {}
    for name, axis in axes.items():
        if len(set(axis.tolist())) <= 1:
            results[name] = {
                "spearman_rho": float("nan"),
                "p_value": float("nan"),
                "note": "axis is constant; correlation undefined",
            }
            continue
        rho_result = spearmanr(delta_m, axis)
        # scipy returns SignificanceResult with .statistic, .pvalue (newer)
        rho = float(getattr(rho_result, "statistic", rho_result[0]))
        pv = float(getattr(rho_result, "pvalue", rho_result[1]))
        results[name] = {
            "spearman_rho": rho,
            "p_value": pv,
        }

    # Sym vs asym RMS comparison
    sym = [r for r in lane_a_non_anchor if r["Z"] == r["N"]]
    asym = [r for r in lane_a_non_anchor if r["Z"] != r["N"]]
    sym_rms_delta = rms([r["delta_m_u"] for r in sym])
    asym_rms_delta = rms([r["delta_m_u"] for r in asym])
    sym_asym_ratio = safe_div(sym_rms_delta, asym_rms_delta)

    # Structured residual flag
    max_abs_rho = max(
        abs(v["spearman_rho"]) for v in results.values()
        if isinstance(v["spearman_rho"], float) and not math.isnan(v["spearman_rho"])
    )
    structured_by_axis = max_abs_rho > 0.5
    structured_by_sym_asym = sym_asym_ratio < 0.5

    return {
        "axis_correlations": results,
        "max_abs_spearman": float(max_abs_rho),
        "rms_delta_m_symmetric": sym_rms_delta,
        "rms_delta_m_asymmetric": asym_rms_delta,
        "sym_asym_ratio": float(sym_asym_ratio),
        "structured_by_axis_rho": structured_by_axis,
        "structured_by_sym_asym": structured_by_sym_asym,
        "structured_residual": structured_by_axis or structured_by_sym_asym,
    }


# ------------------------------------------------------------
# Lane B — uncertainty-weighted z-score
# ------------------------------------------------------------
def lane_b_z_scores(
    isotopes: list[dict[str, Any]],
    Q_func,
    mu_Q: sp.Rational,
) -> dict[str, Any]:
    lane_b = [r for r in isotopes if r["confidence_lane"] == "LANE_B_EVALUATED"]
    if not lane_b:
        return {"n_rows": 0, "rows": []}
    out_rows: list[dict[str, Any]] = []
    for r in lane_b:
        Q = Q_func(r["Z"], r["N"])
        m_pred = float(mu_Q * Q)
        m_meas = r["atomic_mass_u_float"]
        sigma = r["mass_uncertainty_u"]
        z = (m_meas - m_pred) / sigma if sigma > 0 else float("inf")
        out_rows.append(
            {
                "isotope": r["isotope"],
                "Z": r["Z"],
                "N": r["N"],
                "m_meas_u": m_meas,
                "m_pred_u": m_pred,
                "sigma_u": sigma,
                "z_score": z,
                "abs_z": abs(z),
            }
        )
    frac_within_2 = sum(1 for r in out_rows if r["abs_z"] < 2) / len(out_rows)
    return {
        "n_rows": len(lane_b),
        "rows": out_rows,
        "frac_abs_z_lt_2": frac_within_2,
    }


# ------------------------------------------------------------
# Wrong controls
# ------------------------------------------------------------
def wc_R_perturbation(
    R_val: int,
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
) -> dict[str, Any]:
    """Re-derive Q with perturbed R; anchor and report Lane A RMS."""
    F = spine["F"]
    aH = spine["alpha_H"]
    D = spine["D"]
    S_val = int(spine["S"])

    def Q_func(Z: int, N: int) -> sp.Rational:
        return Q_with_R_S(Z, N, R_val, S_val, F, aH, D)

    mu_Q, Q_anchor = anchor_mu_Q(isotopes, Q_func)
    g2 = gate_2_anchor_bridge(isotopes, Q_func, mu_Q)
    return {
        "perturbation": f"R={R_val}",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_Q),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


def wc_S_perturbation(
    S_val: int,
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
) -> dict[str, Any]:
    F = spine["F"]
    aH = spine["alpha_H"]
    D = spine["D"]
    R_val = int(spine["R"])

    def Q_func(Z: int, N: int) -> sp.Rational:
        return Q_with_R_S(Z, N, R_val, S_val, F, aH, D)

    mu_Q, Q_anchor = anchor_mu_Q(isotopes, Q_func)
    g2 = gate_2_anchor_bridge(isotopes, Q_func, mu_Q)
    return {
        "perturbation": f"S={S_val}",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_Q),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


def wc_shuffled_N(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    seed: int,
) -> dict[str, Any]:
    """Shuffle N values across rows; recompute Q with shuffled N at each Z."""
    rng = np.random.default_rng(seed)
    N_values = np.array([r["N"] for r in isotopes])
    perm = rng.permutation(len(N_values))
    N_shuffled = N_values[perm]
    # Build a temp isotope list with shuffled N values (same row order, just N replaced)
    isotopes_shuf: list[dict[str, Any]] = []
    for i, r in enumerate(isotopes):
        new_r = dict(r)
        new_r["N"] = int(N_shuffled[i])
        new_r["A"] = new_r["Z"] + new_r["N"]
        isotopes_shuf.append(new_r)

    def Q_func(Z: int, N: int) -> sp.Rational:
        return Q_canonical(Z, N, spine)

    mu_Q, Q_anchor = anchor_mu_Q(isotopes_shuf, Q_func)
    g2 = gate_2_anchor_bridge(isotopes_shuf, Q_func, mu_Q)
    return {
        "perturbation": f"shuffled_N(Z) seed={seed}",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_Q),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


def wc_shuffled_Q(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    seed: int,
) -> dict[str, Any]:
    """Shuffle canonical Q values across rows; anchor; predict."""
    rng = np.random.default_rng(seed)
    canonical_Qs = [Q_canonical(r["Z"], r["N"], spine) for r in isotopes]
    perm = rng.permutation(len(canonical_Qs))
    Q_shuffled = [canonical_Qs[i] for i in perm]
    # Build a dict from isotope name to Q
    Q_map: dict[str, sp.Rational] = {
        isotopes[i]["isotope"]: Q_shuffled[i] for i in range(len(isotopes))
    }

    def Q_func(Z: int, N: int) -> sp.Rational:
        # Find row matching (Z, N) — there should be exactly one
        for r in isotopes:
            if r["Z"] == Z and r["N"] == N:
                return Q_map[r["isotope"]]
        raise ValueError(f"row not found Z={Z}, N={N}")

    mu_Q, Q_anchor = anchor_mu_Q(isotopes, Q_func)
    g2 = gate_2_anchor_bridge(isotopes, Q_func, mu_Q)
    return {
        "perturbation": f"shuffled_Q seed={seed}",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_Q),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


def wc_monotone_random(
    isotopes: list[dict[str, Any]],
    spine: dict[str, sp.Rational],
    seed: int,
) -> dict[str, Any]:
    """Generate a monotone random Q ladder with the same endpoint range."""
    rng = np.random.default_rng(seed)
    canonical_Qs = [float(Q_canonical(r["Z"], r["N"], spine)) for r in isotopes]
    Q_min = min(canonical_Qs)
    Q_max = max(canonical_Qs)
    n = len(canonical_Qs)
    # Generate n positive random increments summing to Q_max - Q_min
    raw = rng.random(n)
    raw = raw / raw.sum() * (Q_max - Q_min)
    sorted_Qs = [Q_min]
    for d in raw[:-1]:
        sorted_Qs.append(sorted_Qs[-1] + d)
    sorted_Qs.append(Q_max)
    # Assign each row's Q_rand by rank in canonical Q ordering
    ranks = np.argsort(np.argsort(canonical_Qs))
    Q_rand_map: dict[str, float] = {}
    for i, r in enumerate(isotopes):
        Q_rand_map[r["isotope"]] = sorted_Qs[ranks[i]]

    def Q_func(Z: int, N: int) -> sp.Rational:
        for r in isotopes:
            if r["Z"] == Z and r["N"] == N:
                return sp.Rational(Q_rand_map[r["isotope"]]).limit_denominator(10 ** 12)
        raise ValueError(f"row not found Z={Z}, N={N}")

    mu_Q, Q_anchor = anchor_mu_Q(isotopes, Q_func)
    g2 = gate_2_anchor_bridge(isotopes, Q_func, mu_Q)
    return {
        "perturbation": f"monotone_random_ladder seed={seed}",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_Q),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


def wc_A_baseline(isotopes: list[dict[str, Any]]) -> dict[str, Any]:
    """A = Z + N baseline. Anchor at A(C-12)=12 with m=12u gives μ_A = 1u/A-unit."""
    def Q_func(Z: int, N: int) -> sp.Rational:
        return sp.Rational(Z + N)

    mu_A, Q_anchor = anchor_mu_Q(isotopes, Q_func)
    g2 = gate_2_anchor_bridge(isotopes, Q_func, mu_A)
    return {
        "perturbation": "A=Z+N baseline",
        "Q_anchor": str(Q_anchor),
        "mu_Q": str(mu_A),
        "rms_eps_lane_a": g2["rms_eps_lane_a"],
        "max_eps_lane_a": g2["max_eps_lane_a"],
        "frac_lt_0p01": g2["frac_lt_0p01"],
    }


# ------------------------------------------------------------
# Disallowed-claim scan
# ------------------------------------------------------------
DISALLOWED_PHRASES = (
    "SAM failed because",
    "SAM proved",
    "row-by-row fitted",
    "interchangeably",
)


def scan_disallowed_claims(text: str) -> list[dict[str, Any]]:
    """Case-insensitive substring scan for disallowed claim patterns."""
    flags: list[dict[str, Any]] = []
    lower = text.lower()
    for phrase in DISALLOWED_PHRASES:
        idx = 0
        while True:
            pos = lower.find(phrase.lower(), idx)
            if pos < 0:
                break
            # find line number
            line_no = text[:pos].count("\n") + 1
            flags.append({"phrase": phrase, "position": pos, "line": line_no})
            idx = pos + len(phrase)
    return flags


# ------------------------------------------------------------
# Verdict assignment
# ------------------------------------------------------------
def assign_verdict(
    gate_1: dict[str, Any],
    gate_2: dict[str, Any],
    gate_3: dict[str, Any],
    gate_4: dict[str, Any],
    wcs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Apply locked verdict-spectrum thresholds with precedence
    STRONG > BOUNDARY > PREDICTION > FAIL.
    """
    canonical_rms = gate_2["rms_eps_lane_a"]
    wc9_rms = wcs["WC9"]["rms_eps_lane_a"]
    # Q "beats" WCx by 2x if RMS_Q < RMS_WCx / 2
    beats_wc9_2x = canonical_rms < wc9_rms / 2 if wc9_rms > 0 else False
    # Beats all WC1-WC8 by 1.5x
    wc1_8_rms = [wcs[f"WC{i}"]["rms_eps_lane_a"] for i in range(1, 9)]
    beats_wc1_8_1p5x = all(canonical_rms < r / 1.5 for r in wc1_8_rms if r > 0)

    # WC6 μ_Q drift check — μ_Q from shuffled-N anchor
    wc6_mu_str = wcs["WC6"]["mu_Q"]
    wc6_mu = float(sp.Rational(wc6_mu_str))
    canonical_mu_Q = 192 / 7117
    mu_drift_wc6 = abs(wc6_mu / canonical_mu_Q - 1)

    # Gate condition flags
    g1_S1 = gate_1["frac_lt_0p01"] >= 0.95 and gate_1["median_eps"] < 0.005
    g2_S2 = gate_2["frac_lt_0p01"] >= 0.95 and gate_2["rms_eps_lane_a"] < 0.01
    g3_S3 = (
        gate_3["frac_R_within_0p05"] >= 0.80
        and abs(gate_3["median_R"] - 1) < 0.10
    )

    strong = g1_S1 and g2_S2 and g3_S3 and beats_wc9_2x and beats_wc1_8_1p5x

    boundary_b1 = beats_wc9_2x
    boundary_b2 = not (g1_S1 and g2_S2 and g3_S3)  # at least one strong-pass condition fails
    boundary_b3 = gate_4["structured_residual"]
    boundary = boundary_b1 and boundary_b2 and boundary_b3 and not strong

    fail_F1 = not beats_wc9_2x
    fail_F2 = (
        gate_4["max_abs_spearman"] < 0.3
        and gate_4["sym_asym_ratio"] > 0.8
    )
    fail_F3 = mu_drift_wc6 > 0.05
    fail = (fail_F1 or fail_F2 or fail_F3) and not strong and not boundary

    # Prediction-conflict: not present in v1 (no Lane C rows)
    prediction_conflict = False

    if strong:
        verdict = "STRONG_PASS_CR239_DIRECT_MASS_GRAVITY_BRIDGE"
    elif boundary:
        verdict = "BOUNDARY_CR239_SOURCE_SKELETON_WITH_STRUCTURED_RESIDUAL"
    elif prediction_conflict:
        verdict = "PREDICTION_CR239_FRONTIER_CONFLICT_WITH_EVALUATED_TABLE"
    else:
        verdict = "FAIL_CR239_DIRECT_BRIDGE"

    return {
        "verdict": verdict,
        "STRONG_conditions": {
            "S1_gate1": g1_S1,
            "S2_gate2": g2_S2,
            "S3_gate3": g3_S3,
            "S4_beats_wc9_2x": beats_wc9_2x,
            "S5_beats_wc1_8_1p5x": beats_wc1_8_1p5x,
        },
        "BOUNDARY_conditions": {
            "B1_beats_wc9_2x": boundary_b1,
            "B2_strong_failed": boundary_b2,
            "B3_structured_residual": boundary_b3,
        },
        "FAIL_conditions": {
            "F1_does_not_beat_wc9_2x": fail_F1,
            "F2_unstructured_residual": fail_F2,
            "F3_mu_Q_drift_under_wc6_gt_5pct": fail_F3,
        },
        "mu_drift_wc6": mu_drift_wc6,
        "canonical_rms_lane_a": canonical_rms,
        "wc9_rms_lane_a": wc9_rms,
        "rms_ratio_wc9_over_canonical": (
            wc9_rms / canonical_rms if canonical_rms > 0 else float("inf")
        ),
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
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})


def main() -> int:
    shas = assert_input_shas()
    spine = cr238_spine()

    # Verify CR238 kernel constants
    assert spine["kappa"] == sp.Rational(7117, 768), f"κ mismatch: {spine['kappa']}"
    assert spine["g"] == sp.Rational(1, 64), f"g mismatch: {spine['g']}"
    assert spine["S"] == sp.Rational(8)
    assert spine["R"] == sp.Rational(12)
    assert spine["D"] == sp.Rational(3)

    isotopes = load_isotopes()

    # Canonical Q for each isotope (closures over spine)
    def Q_canon(Z: int, N: int) -> sp.Rational:
        return Q_canonical(Z, N, spine)

    # Anchor μ_Q
    mu_Q, Q_anchor = anchor_mu_Q(isotopes, Q_canon)
    assert Q_anchor == sp.Rational(7117, 16), f"Q(C-12) mismatch: {Q_anchor}"
    assert mu_Q == sp.Rational(192, 7117), f"μ_Q mismatch: {mu_Q}"

    # Gates
    gate_1 = gate_1_ratio_test(isotopes, Q_canon)
    gate_2 = gate_2_anchor_bridge(isotopes, Q_canon, mu_Q)
    gate_3 = gate_3_isotope_increment(isotopes, Q_canon, mu_Q)
    gate_4 = gate_4_residual_structure(gate_2["row_results"], int(spine["R"]))
    lane_b = lane_b_z_scores(isotopes, Q_canon, mu_Q)

    # Wrong controls
    wcs: dict[str, dict[str, Any]] = {}
    wcs["WC1"] = wc_R_perturbation(10, isotopes, spine)
    wcs["WC2"] = wc_R_perturbation(11, isotopes, spine)
    wcs["WC3"] = wc_R_perturbation(13, isotopes, spine)
    wcs["WC4"] = wc_S_perturbation(7, isotopes, spine)
    wcs["WC5"] = wc_S_perturbation(9, isotopes, spine)
    wcs["WC6"] = wc_shuffled_N(isotopes, spine, SHUFFLE_SEED)
    wcs["WC7"] = wc_shuffled_Q(isotopes, spine, SHUFFLE_SEED)
    wcs["WC8"] = wc_monotone_random(isotopes, spine, SHUFFLE_SEED)
    wcs["WC9"] = wc_A_baseline(isotopes)

    # Verdict
    verdict_info = assign_verdict(gate_1, gate_2, gate_3, gate_4, wcs)

    # Write per-row / per-pair outputs
    out_dir = SCRIPT_DIR
    write_csv(
        out_dir / "CR239_ratio_test.csv",
        [{k: str(v) for k, v in r.items()} for r in gate_1["pair_results"]],
    )
    write_csv(
        out_dir / "CR239_one_anchor_bridge.csv",
        [{k: str(v) for k, v in r.items()} for r in gate_2["row_results"]],
    )
    write_csv(
        out_dir / "CR239_isotope_increment_test.csv",
        [{k: str(v) for k, v in r.items()} for r in gate_3["pair_results"]],
    )
    # Gate 4 axis correlations
    g4_rows = []
    for axis, info in gate_4["axis_correlations"].items():
        g4_rows.append(
            {
                "axis": axis,
                "spearman_rho": info.get("spearman_rho", ""),
                "p_value": info.get("p_value", ""),
                "note": info.get("note", ""),
            }
        )
    g4_rows.append(
        {
            "axis": "AGGREGATE",
            "spearman_rho": gate_4["max_abs_spearman"],
            "p_value": "",
            "note": f"sym/asym ratio={gate_4['sym_asym_ratio']:.4f}; "
            f"structured={gate_4['structured_residual']}",
        }
    )
    write_csv(
        out_dir / "CR239_residual_structure.csv",
        [{k: str(v) for k, v in r.items()} for r in g4_rows],
    )

    # Lane A / B / C / D CSVs
    lane_a_rows = [r for r in gate_2["row_results"] if r["confidence_lane"] == "LANE_A_HARD_MEASURED"]
    write_csv(
        out_dir / "CR239_lane_a_hard_measured.csv",
        [{k: str(v) for k, v in r.items()} for r in lane_a_rows],
    )
    write_csv(
        out_dir / "CR239_lane_b_evaluated.csv",
        [{k: str(v) for k, v in r.items()} for r in lane_b["rows"]],
    )
    # Lane C and Lane D empty in v1
    (out_dir / "CR239_lane_c_extrapolated_frontier.csv").write_text(
        "isotope,Z,N,A,note\n# Lane C empty in v1; reserved for frontier predictions\n",
        encoding="utf-8",
    )
    (out_dir / "CR239_lane_d_post_evaluation_challenge.csv").write_text(
        "isotope,Z,N,A,note\n# Lane D reserved for v2 (post-evaluation challenge)\n",
        encoding="utf-8",
    )

    # Wrong controls CSV
    wc_rows = []
    for wc_id, info in wcs.items():
        wc_rows.append(
            {
                "wc_id": wc_id,
                "perturbation": info["perturbation"],
                "Q_anchor": info["Q_anchor"],
                "mu_Q": info["mu_Q"],
                "rms_eps_lane_a": info["rms_eps_lane_a"],
                "max_eps_lane_a": info["max_eps_lane_a"],
                "frac_lt_0p01": info["frac_lt_0p01"],
                "rms_ratio_vs_canonical": (
                    info["rms_eps_lane_a"] / gate_2["rms_eps_lane_a"]
                    if gate_2["rms_eps_lane_a"] > 0 else float("inf")
                ),
            }
        )
    write_csv(
        out_dir / "CR239_wrong_controls.csv",
        [{k: str(v) for k, v in r.items()} for r in wc_rows],
    )

    # Summary JSON
    summary = {
        "verdict": verdict_info["verdict"],
        "input_shas": shas,
        "kernel_atoms": {
            "F": int(spine["F"]),
            "S": int(spine["S"]),
            "alpha_H": int(spine["alpha_H"]),
            "D": int(spine["D"]),
            "R": int(spine["R"]),
            "kappa": str(spine["kappa"]),
            "g": str(spine["g"]),
        },
        "anchor": {
            "isotope": ANCHOR_ISOTOPE,
            "mass_u": str(ANCHOR_MASS_U),
            "Q_anchor": str(Q_anchor),
            "mu_Q": str(mu_Q),
            "mu_Q_float": float(mu_Q),
        },
        "gate_1_ratio_test": {
            "n_pairs": gate_1["n_pairs"],
            "rms_eps": gate_1["rms_eps"],
            "median_eps": gate_1["median_eps"],
            "max_eps": gate_1["max_eps"],
            "frac_lt_0p01": gate_1["frac_lt_0p01"],
            "frac_lt_0p05": gate_1["frac_lt_0p05"],
        },
        "gate_2_anchor_bridge": {
            "n_lane_a_non_anchor": gate_2["n_lane_a_non_anchor"],
            "rms_eps_lane_a": gate_2["rms_eps_lane_a"],
            "max_eps_lane_a": gate_2["max_eps_lane_a"],
            "median_eps_lane_a": gate_2["median_eps_lane_a"],
            "frac_lt_0p01": gate_2["frac_lt_0p01"],
            "frac_lt_0p05": gate_2["frac_lt_0p05"],
            "n_symmetric": gate_2["n_symmetric"],
            "n_asymmetric": gate_2["n_asymmetric"],
            "rms_eps_symmetric": gate_2["rms_eps_symmetric"],
            "rms_eps_asymmetric": gate_2["rms_eps_asymmetric"],
        },
        "gate_3_isotope_increment": {
            "n_pairs": gate_3["n_pairs"],
            "mean_R": gate_3["mean_R"],
            "median_R": gate_3["median_R"],
            "std_R": gate_3["std_R"],
            "frac_R_within_0p05": gate_3["frac_R_within_0p05"],
            "frac_R_within_0p50": gate_3["frac_R_within_0p50"],
            "dm_SAM_per_neutron_u": gate_3["dm_SAM_per_neutron_u"],
            "dm_SAM_per_neutron_rational": gate_3["dm_SAM_per_neutron_rational"],
        },
        "gate_4_residual_structure": {
            "max_abs_spearman": gate_4["max_abs_spearman"],
            "rms_delta_m_symmetric": gate_4["rms_delta_m_symmetric"],
            "rms_delta_m_asymmetric": gate_4["rms_delta_m_asymmetric"],
            "sym_asym_ratio": gate_4["sym_asym_ratio"],
            "structured_by_axis_rho": gate_4["structured_by_axis_rho"],
            "structured_by_sym_asym": gate_4["structured_by_sym_asym"],
            "structured_residual": gate_4["structured_residual"],
            "axis_correlations": {
                k: {kk: vv for kk, vv in v.items()}
                for k, v in gate_4["axis_correlations"].items()
            },
        },
        "lane_b": {
            "n_rows": lane_b["n_rows"],
            "frac_abs_z_lt_2": lane_b.get("frac_abs_z_lt_2", None),
        },
        "wrong_controls": {
            wc_id: {
                "perturbation": info["perturbation"],
                "rms_eps_lane_a": info["rms_eps_lane_a"],
                "rms_ratio_vs_canonical": (
                    info["rms_eps_lane_a"] / gate_2["rms_eps_lane_a"]
                    if gate_2["rms_eps_lane_a"] > 0 else float("inf")
                ),
            }
            for wc_id, info in wcs.items()
        },
        "verdict_logic": verdict_info,
    }

    # Disallowed-claim scan over summary text
    summary_text = json.dumps(summary, indent=2, sort_keys=True)
    flagged = scan_disallowed_claims(summary_text)
    summary["disallowed_claim_flags"] = flagged

    # Write summary
    with open(out_dir / "CR239_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True, default=str)

    # Print verdict line
    print(f"CR239 verdict: {verdict_info['verdict']}")
    print(
        f"  Gate 1 ratio test: n={gate_1['n_pairs']}, "
        f"RMS={gate_1['rms_eps']:.6f}, "
        f"median={gate_1['median_eps']:.6f}, "
        f"frac<1%={gate_1['frac_lt_0p01']:.3f}"
    )
    print(
        f"  Gate 2 anchor bridge: n={gate_2['n_lane_a_non_anchor']}, "
        f"RMS_eps={gate_2['rms_eps_lane_a']:.6f}, "
        f"max={gate_2['max_eps_lane_a']:.6f}, "
        f"frac<1%={gate_2['frac_lt_0p01']:.3f}"
    )
    print(
        f"  Gate 2 split: sym RMS={gate_2['rms_eps_symmetric']:.6f}, "
        f"asym RMS={gate_2['rms_eps_asymmetric']:.6f}"
    )
    print(
        f"  Gate 3 isotope increment: n={gate_3['n_pairs']}, "
        f"median R={gate_3['median_R']:.4f}, "
        f"mean R={gate_3['mean_R']:.4f}"
    )
    print(
        f"  Gate 4 residual structure: max|ρ_S|={gate_4['max_abs_spearman']:.4f}, "
        f"sym/asym={gate_4['sym_asym_ratio']:.4f}, "
        f"structured={gate_4['structured_residual']}"
    )
    print("  Wrong control RMS comparison (lower is better):")
    print(f"    canonical Q  : RMS={gate_2['rms_eps_lane_a']:.6f}")
    for wc_id, info in wcs.items():
        ratio = info["rms_eps_lane_a"] / gate_2["rms_eps_lane_a"] if gate_2["rms_eps_lane_a"] > 0 else float("inf")
        print(
            f"    {wc_id} ({info['perturbation']:<30}): "
            f"RMS={info['rms_eps_lane_a']:.6f} (× canonical: {ratio:.3f})"
        )
    print(f"  Disallowed-claim flags: {len(flagged)}")

    # Exit code 0 for STRONG/BOUNDARY/PREDICTION; 1 for FAIL
    overall_ok = verdict_info["verdict"] != "FAIL_CR239_DIRECT_BRIDGE"
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
