"""CR245 — Binding-Curvature from Typed Substrate runner.

Stage 1: verify asymmetry identity (Q_mass-Q_sub)^2/Q_mass = (N-Z)^2/A *
         7093^2/(192*7117) exactly (Fraction arithmetic).
Stage 2: fit BW form on Lane A train (A >= 16).
Stage 3: search typed-rational candidates for each fitted coefficient.
Stage 4: build zero-free typed candidate, evaluate train + holdout.
Stage 5: wrong controls.
Verdict by precommit gates.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).parent
TRAIN_CSV = HERE / "CR245_train_lane_a.csv"
TEST_CSV = HERE / "CR245_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR245_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "a4274eb1af0ae4310629072dc530e4518d705218371f9aa8a716123fbf1b97d4"

# Locked substrate atoms
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R, D, S, M_LEDGER, L_LEDGER, V_LEDGER, THETA = 12, 3, 8, 126, 162, 27, 18

# Derived exact constants
KAPPA_MINUS_2G = KAPPA - 2 * G       # 7093/768
ASYM_CONST = Fraction(7093 * 7093, 192 * 7117)  # exact = 7093^2/(192*7117)

# u <-> MeV conversion (informational only)
U_TO_MEV = 931.49410242


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def read_isotope_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open() as f:
        for row in csv.DictReader(f):
            row["Z"] = int(row["Z"])
            row["N"] = int(row["N"])
            row["A"] = int(row["A"])
            row["atomic_mass_u"] = float(row["atomic_mass_u"])
            rows.append(row)
    return rows


def expand_sob(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compute Q_mass, Q_sub, dQ, B_u, asym_lhs, asym_rhs per row."""
    for r in rows:
        A = r["A"]; Z = r["Z"]; N = r["N"]
        Q_mass = 4 * Fraction(A) * KAPPA
        G_sub = Fraction(Z) * KAPPA + Fraction(N - Z) * G
        Q_sub = Fraction(S) * G_sub
        dQ = Q_mass - Q_sub
        if Q_mass == 0:
            asym_lhs = None
            asym_rhs = None
            asym_match = None
        else:
            asym_lhs = dQ * dQ / Q_mass
            asym_rhs = Fraction((N - Z) ** 2, A) * ASYM_CONST if A > 0 else None
            asym_match = (asym_lhs == asym_rhs)
        r["Q_mass_frac"] = Q_mass
        r["G_sub_frac"] = G_sub
        r["Q_sub_frac"] = Q_sub
        r["dQ_frac"] = dQ
        r["Q_mass"] = float(Q_mass)
        r["Q_sub"] = float(Q_sub)
        r["dQ"] = float(dQ)
        r["B_u"] = A - r["atomic_mass_u"]
        r["asym_lhs"] = float(asym_lhs) if asym_lhs is not None else None
        r["asym_rhs"] = float(asym_rhs) if asym_rhs is not None else None
        r["asym_match"] = asym_match
    return rows


def design_matrix(rows: list[dict[str, Any]]) -> np.ndarray:
    """BW design matrix using (N-Z)^2/A asymmetry term (equivalent to
    (Q_mass-Q_sub)^2/Q_mass after the structural identity factor)."""
    X = []
    for r in rows:
        A, Z, N = r["A"], r["Z"], r["N"]
        if A == 0:
            asym = 0.0
        else:
            asym = (N - Z) ** 2 / A
        if Z % 2 == 0 and N % 2 == 0:
            delta = +1.0
        elif Z % 2 == 1 and N % 2 == 1:
            delta = -1.0
        else:
            delta = 0.0
        X.append([
            A,                          # +a*A
            -A ** (2.0 / 3),            # -b*A^(2/3)
            -Z * (Z - 1) / A ** (1.0 / 3),  # -c*Z(Z-1)/A^(1/3)
            -asym,                      # -d_raw*(N-Z)^2/A (raw, before rescale)
            delta / A ** 0.5,           # +e*pair/sqrt(A)
        ])
    return np.array(X)


def fit_bw(rows: list[dict[str, Any]]) -> dict[str, Any]:
    X = design_matrix(rows)
    y = np.array([r["B_u"] for r in rows])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    residual = pred - y
    rms_u = float(np.sqrt(np.mean(residual ** 2)))
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    # Rescale d from (N-Z)^2/A representation to (Q_mass-Q_sub)^2/Q_mass
    # representation: (N-Z)^2/A = ((Q_mass-Q_sub)^2/Q_mass) / 36.8242
    # so d_dQ * 36.8242 = d_raw, i.e., d_dQ = d_raw / 36.8242
    asym_const_float = float(ASYM_CONST)
    d_raw = coef[3]
    d_dQ = d_raw / asym_const_float
    return {
        "coef_in_u": {
            "a_volume": float(coef[0]),
            "b_surface": float(coef[1]),
            "c_coulomb": float(coef[2]),
            "d_asym_NmZ2_over_A": float(coef[3]),
            "d_asym_dQ2_over_Qmass": float(d_dQ),
            "e_pair": float(coef[4]),
        },
        "coef_in_MeV": {
            "a_volume": float(coef[0]) * U_TO_MEV,
            "b_surface": float(coef[1]) * U_TO_MEV,
            "c_coulomb": float(coef[2]) * U_TO_MEV,
            "d_asym_NmZ2_over_A": float(coef[3]) * U_TO_MEV,
            "d_asym_dQ2_over_Qmass": float(d_dQ) * U_TO_MEV,
            "e_pair": float(coef[4]) * U_TO_MEV,
        },
        "design_matrix_basis": "[A, -A^(2/3), -Z(Z-1)/A^(1/3), -(N-Z)^2/A, delta/sqrt(A)]",
        "rms_u": rms_u,
        "rms_MeV": rms_u * U_TO_MEV,
        "R2": r2,
        "n_rows": len(rows),
    }


def evaluate_with_coef(rows: list[dict[str, Any]], coef: list[float]) -> dict[str, Any]:
    X = design_matrix(rows)
    y = np.array([r["B_u"] for r in rows])
    pred = X @ np.array(coef)
    residual = pred - y
    rms_u = float(np.sqrt(np.mean(residual ** 2)))
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    per_row = []
    for r, p in zip(rows, pred):
        per_row.append({
            "isotope": r.get("isotope"),
            "Z": r["Z"], "N": r["N"], "A": r["A"],
            "B_u_observed": r["B_u"],
            "B_u_predicted": float(p),
            "residual_u": float(p - r["B_u"]),
        })
    return {
        "rms_u": rms_u, "rms_MeV": rms_u * U_TO_MEV, "R2": r2,
        "n_rows": len(rows), "per_row": per_row,
    }


def typed_candidates() -> dict[str, Fraction]:
    """Locked finite candidate set built deterministically from precommit list."""
    atoms = {
        "R": Fraction(R), "D": Fraction(D), "S": Fraction(S),
        "M": Fraction(M_LEDGER), "L": Fraction(L_LEDGER),
        "V": Fraction(V_LEDGER), "Theta": Fraction(THETA),
        "kappa": KAPPA, "g": G, "kappa-2g": KAPPA_MINUS_2G,
    }
    out: dict[str, Fraction] = {}
    # Reciprocals
    for name, v in atoms.items():
        if v != 0:
            out[f"1/{name}"] = Fraction(1) / v
    # Atom values directly
    for name, v in atoms.items():
        out[name] = v
    # Simple atom*atom and 1/(atom*atom)
    names = list(atoms.items())
    for i, (n1, v1) in enumerate(names):
        for j, (n2, v2) in enumerate(names):
            if i > j:
                continue
            prod = v1 * v2
            if prod != 0:
                out[f"1/({n1}*{n2})"] = Fraction(1) / prod
                # Also include kappa/atom and g/atom
            if n1 == "kappa" or n2 == "kappa":
                if v1 * v2 != 0 and not (n1 == "kappa" and n2 == "kappa"):
                    pass  # already covered
    # kappa/R, kappa/M, etc.
    for n, v in atoms.items():
        if v != 0 and n != "kappa":
            out[f"kappa/{n}"] = KAPPA / v
        if v != 0 and n != "g":
            out[f"g/{n}"] = G / v
    # Atom/atom ratios (small set)
    for n1, v1 in atoms.items():
        for n2, v2 in atoms.items():
            if n1 == n2 or v2 == 0:
                continue
            if n1 in ("kappa", "g") or n2 in ("kappa", "g"):
                continue
            out[f"{n1}/{n2}"] = v1 / v2
    # Special families: (kappa-2g)/atom, kappa^2, g^2
    for n, v in atoms.items():
        if v != 0 and n not in ("kappa", "g", "kappa-2g"):
            out[f"(kappa-2g)/{n}"] = KAPPA_MINUS_2G / v
    out["kappa^2"] = KAPPA * KAPPA
    out["g^2"] = G * G
    out["kappa*g"] = KAPPA * G
    # Locked channel-form values (CR243/244 results)
    out["(D+2)/(R*(D+1))"] = Fraction(D + 2, R * (D + 1))         # 5/48
    out["(D^2+S)/(D*S^2)"] = Fraction(D * D + S, D * S * S)       # 17/192
    out["7093^2/(192*7117)"] = ASYM_CONST                          # exact asymmetry constant
    return out


def find_best_typed_candidate(fitted: float, candidates: dict[str, Fraction],
                              tol_pct: float = 5.0) -> dict[str, Any]:
    """Find nearest typed-rational candidate at absolute value, allowing sign."""
    best: dict[str, Any] | None = None
    for name, frac in candidates.items():
        for sign in (+1, -1):
            cv = sign * float(frac)
            if fitted == 0:
                rel = 1.0 if cv != 0 else 0.0
            else:
                rel = abs((fitted - cv) / fitted)
            if best is None or rel < best["rel_dev"]:
                best = {
                    "name": ("+" if sign > 0 else "-") + name,
                    "value": cv,
                    "fraction": f"{(sign * frac.numerator)}/{frac.denominator}",
                    "rel_dev": rel,
                }
    if best is None:
        best = {"name": None, "value": None, "fraction": None, "rel_dev": float("inf")}
    best["within_5pct"] = best["rel_dev"] <= 0.05
    best["within_1pct"] = best["rel_dev"] <= 0.01
    return best


def search_typed_for_all(fit: dict[str, Any]) -> dict[str, Any]:
    cands = typed_candidates()
    results = {}
    for key in ("a_volume", "b_surface", "c_coulomb", "d_asym_NmZ2_over_A", "e_pair"):
        fitted = fit["coef_in_u"][key]
        results[key] = {
            "fitted_u": fitted,
            "fitted_MeV": fitted * U_TO_MEV,
            "best_candidate": find_best_typed_candidate(fitted, cands),
        }
    return results


def build_zero_free_coef(fit: dict[str, Any], typed_search: dict[str, Any]) -> dict[str, Any]:
    """Replace fitted coef with nearest typed-rational at <=5%; else keep fitted."""
    keys = ("a_volume", "b_surface", "c_coulomb", "d_asym_NmZ2_over_A", "e_pair")
    coef = []
    substitutions = {}
    for key in keys:
        best = typed_search[key]["best_candidate"]
        fitted = fit["coef_in_u"][key]
        if best["within_5pct"]:
            coef.append(best["value"])
            substitutions[key] = {
                "substituted": True,
                "typed_name": best["name"],
                "typed_value": best["value"],
                "fitted_value": fitted,
                "rel_dev": best["rel_dev"],
            }
        else:
            coef.append(fitted)
            substitutions[key] = {
                "substituted": False,
                "typed_name": None,
                "typed_value": None,
                "fitted_value": fitted,
                "rel_dev": best["rel_dev"],
                "best_attempt_name": best["name"],
                "best_attempt_rel_dev": best["rel_dev"],
            }
    return {"coef": coef, "substitutions": substitutions}


def wrong_control_asym_identity(rows: list[dict[str, Any]], R_: int) -> dict[str, Any]:
    """WC-R*: re-derive asymmetry identity at R_ != 12 and check identity breaks."""
    kappa_pert = Fraction(7117, 768)  # CR238 kappa is fixed by foundational atoms;
    # under R perturbation, we're testing whether the (Q_mass - Q_sub) algebra
    # still uses kappa = 7117/768.  The identity LHS depends on Q_mass = 4*A*kappa
    # and Q_sub = S*(Z*kappa + (N-Z)*g) which use *atomic* kappa and g.
    # The RHS constant 7093^2/(192*7117) is fixed by the algebra.
    # The WC tests R as if R appeared in the identity factor: specifically,
    # if we mis-identify the identity factor as 7093^2/(R_*7117) for some R_,
    # the predicted RHS changes and the identity should break.
    break_count = 0
    total = 0
    nontrivial_total = 0
    nontrivial_break = 0
    for r in rows:
        if r["asym_lhs"] is None or r["A"] == 0:
            continue
        total += 1
        # Perturbed RHS using R_ in the structural-identity factor:
        rhs_pert = Fraction((r["N"] - r["Z"]) ** 2, r["A"]) * Fraction(7093 * 7093, 16 * R_ * 7117)
        identity_breaks = (float(rhs_pert) != r["asym_lhs"])
        if identity_breaks:
            break_count += 1
        # Non-trivial rows: where (N-Z) != 0 (symmetric rows have both sides = 0
        # regardless of the constant, so they trivially satisfy any identity)
        if r["N"] != r["Z"]:
            nontrivial_total += 1
            if identity_breaks:
                nontrivial_break += 1
    return {
        "label": f"WC-R{R_}_asym_identity_factor",
        "R_perturbation": R_,
        "total": total,
        "break_count": break_count,
        "nontrivial_total": nontrivial_total,
        "nontrivial_break_count": nontrivial_break,
        "breaks_all_nontrivial_rows": nontrivial_break == nontrivial_total and nontrivial_total > 0,
    }


def wrong_control_drop_asym(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """WC-T1: drop the asymmetry term and refit. Compare RMS."""
    # Design matrix without asymmetry column
    X = []
    for r in rows:
        A, Z, N = r["A"], r["Z"], r["N"]
        if Z % 2 == 0 and N % 2 == 0:
            delta = +1.0
        elif Z % 2 == 1 and N % 2 == 1:
            delta = -1.0
        else:
            delta = 0.0
        X.append([
            A,
            -A ** (2.0 / 3),
            -Z * (Z - 1) / A ** (1.0 / 3),
            delta / A ** 0.5,
        ])
    X = np.array(X)
    y = np.array([r["B_u"] for r in rows])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    rms = float(np.sqrt(np.mean((pred - y) ** 2)))
    return {
        "label": "WC-T1_drop_asym",
        "description": "Drop SAM asymmetry term; refit 4-term BW",
        "rms_u_dropped": rms,
        "rms_MeV_dropped": rms * U_TO_MEV,
    }


def wrong_control_shuffle_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """WC-A1: shuffle B_u labels and refit. Pass if RMS degrades."""
    rng = random.Random(20260623)
    shuffled_y = list([r["B_u"] for r in rows])
    rng.shuffle(shuffled_y)
    X = design_matrix(rows)
    y = np.array(shuffled_y)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    rms = float(np.sqrt(np.mean((pred - y) ** 2)))
    return {
        "label": "WC-A1_shuffle_B_u",
        "description": "Shuffle B_u labels (seed 20260623), refit",
        "rms_u_shuffled": rms,
        "rms_MeV_shuffled": rms * U_TO_MEV,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k); fieldnames.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    # Hash checks
    actual_train = sha256(TRAIN_CSV); actual_test = sha256(TEST_CSV); actual_pre = sha256(PRECOMMIT_MD)
    if actual_train != EXPECTED_TRAIN_SHA:
        raise SystemExit(f"TRAIN SHA mismatch: {actual_train} vs {EXPECTED_TRAIN_SHA}")
    if actual_test != EXPECTED_TEST_SHA:
        raise SystemExit(f"TEST SHA mismatch: {actual_test} vs {EXPECTED_TEST_SHA}")
    if actual_pre != EXPECTED_PRECOMMIT_SHA:
        raise SystemExit(f"PRECOMMIT SHA mismatch: {actual_pre} vs {EXPECTED_PRECOMMIT_SHA}")

    # Stage 1: expand SOB
    train_all = expand_sob(read_isotope_csv(TRAIN_CSV))
    test_all = expand_sob(read_isotope_csv(TEST_CSV))

    # Asymmetry identity check (Stage 1)
    asym_train_total = sum(1 for r in train_all if r["asym_match"] is not None)
    asym_train_match = sum(1 for r in train_all if r["asym_match"])
    asym_test_total = sum(1 for r in test_all if r["asym_match"] is not None)
    asym_test_match = sum(1 for r in test_all if r["asym_match"])
    S1 = (asym_train_match == asym_train_total) and (asym_test_match == asym_test_total) and asym_train_total > 0

    # Stage 2: fit BW form on train with A >= 16
    train_fit = [r for r in train_all if r["A"] >= 16]
    fit = fit_bw(train_fit)
    S2 = fit["rms_MeV"] <= 5.0

    # Stage 3: typed-rational candidate search
    typed_search = search_typed_for_all(fit)
    matched_5pct = sum(1 for k, v in typed_search.items() if v["best_candidate"]["within_5pct"])
    S3 = matched_5pct >= 3

    # Stage 4: zero-free typed candidate
    zf = build_zero_free_coef(fit, typed_search)
    zf_train = evaluate_with_coef(train_fit, zf["coef"])
    zf_test = evaluate_with_coef(test_all, zf["coef"])
    fitted_train = evaluate_with_coef(train_fit, [
        fit["coef_in_u"]["a_volume"], fit["coef_in_u"]["b_surface"],
        fit["coef_in_u"]["c_coulomb"], fit["coef_in_u"]["d_asym_NmZ2_over_A"],
        fit["coef_in_u"]["e_pair"],
    ])
    fitted_test = evaluate_with_coef(test_all, [
        fit["coef_in_u"]["a_volume"], fit["coef_in_u"]["b_surface"],
        fit["coef_in_u"]["c_coulomb"], fit["coef_in_u"]["d_asym_NmZ2_over_A"],
        fit["coef_in_u"]["e_pair"],
    ])
    S4 = zf_train["rms_u"] <= 1.5 * fitted_train["rms_u"]
    S5 = zf_test["rms_u"] <= 1.5 * fitted_test["rms_u"]

    # Stage 5: wrong controls
    wc_asym_R = [wrong_control_asym_identity(train_all + test_all, R_=r) for r in (10, 11, 13)]
    wc_drop = wrong_control_drop_asym(train_fit)
    wc_shuffle = wrong_control_shuffle_rows(train_fit)
    S6 = all(w["breaks_all_nontrivial_rows"] for w in wc_asym_R)
    S7 = wc_drop["rms_u_dropped"] >= 1.5 * fitted_train["rms_u"]
    S8 = wc_shuffle["rms_u_shuffled"] >= 1.5 * fitted_train["rms_u"]

    strong_pass = all([S1, S2, S3, S4, S5, S6, S7, S8])
    F1 = not S1
    F2 = (not S2) or math.isnan(fit["R2"])
    F3 = not S7

    if F1 or F2 or F3:
        verdict = "FAIL"
        signature = "CR245_FAIL_BINDING_TYPED_SUBSTRATE"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR245_STRONG_PASS_BINDING_FROM_TYPED_SUBSTRATE__"
                     "ASYMMETRY_IDENTITY_EXACT__MAJORITY_COEFS_TYPED__"
                     "ZERO_FREE_CANDIDATE_WITHIN_TOL__ALL_WC_DEGRADE")
    else:
        # Boundary: asymmetry identity exact but full typing partial
        verdict = "BOUNDARY"
        signature = ("CR245_BOUNDARY_ASYMMETRY_IDENTITY_EXACT__"
                     "BW_FIT_REASONABLE__COEFFICIENT_TYPING_PARTIAL__"
                     "SUBSTRATE_ATOMS_LOAD_BEARING_WHERE_CHECKED")

    # Write outputs
    write_csv(HERE / "CR245_expanded_sob_table.csv", [
        {k: v for k, v in r.items() if not k.endswith("_frac")} for r in (train_all + test_all)
    ])

    bw_rows = [
        {"coefficient": k,
         "fitted_u": fit["coef_in_u"][k],
         "fitted_MeV": fit["coef_in_MeV"][k],
         "best_typed_candidate": typed_search.get(k, {}).get("best_candidate", {}).get("name") if k in typed_search else "",
         "best_typed_value_u": typed_search.get(k, {}).get("best_candidate", {}).get("value") if k in typed_search else "",
         "best_typed_fraction": typed_search.get(k, {}).get("best_candidate", {}).get("fraction") if k in typed_search else "",
         "rel_dev": typed_search.get(k, {}).get("best_candidate", {}).get("rel_dev") if k in typed_search else "",
         "within_5pct": typed_search.get(k, {}).get("best_candidate", {}).get("within_5pct") if k in typed_search else "",
         "within_1pct": typed_search.get(k, {}).get("best_candidate", {}).get("within_1pct") if k in typed_search else "",
         }
        for k in ("a_volume", "b_surface", "c_coulomb", "d_asym_NmZ2_over_A", "d_asym_dQ2_over_Qmass", "e_pair")
    ]
    write_csv(HERE / "CR245_bw_fit_train.csv", bw_rows)

    cand_rows = []
    for key, info in typed_search.items():
        b = info["best_candidate"]
        cand_rows.append({
            "coefficient": key,
            "fitted_u": info["fitted_u"],
            "fitted_MeV": info["fitted_MeV"],
            "best_typed_name": b["name"],
            "best_typed_value": b["value"],
            "best_typed_fraction": b["fraction"],
            "rel_dev": b["rel_dev"],
            "within_5pct": b["within_5pct"],
            "within_1pct": b["within_1pct"],
        })
    write_csv(HERE / "CR245_typed_candidates.csv", cand_rows)

    write_csv(HERE / "CR245_zero_free_predictions.csv",
              [{**p, "split": "train"} for p in zf_train["per_row"]] +
              [{**p, "split": "test"} for p in zf_test["per_row"]])

    wc_rows = []
    for w in wc_asym_R:
        wc_rows.append({
            "label": w["label"], "kind": "asym_identity_perturbation",
            "perturbation": f"R_={w['R_perturbation']}",
            "metric_name": "nontrivial_rows_breaking_identity",
            "metric_value": w["nontrivial_break_count"],
            "total": w["nontrivial_total"],
            "pass_condition_met": w["breaks_all_nontrivial_rows"],
            "note": f"trivial (N=Z) rows: {w['total'] - w['nontrivial_total']} match trivially under any R",
        })
    wc_rows.append({
        "label": wc_drop["label"], "kind": "term_removal",
        "perturbation": "drop SAM asymmetry term",
        "metric_name": "rms_MeV_dropped",
        "metric_value": wc_drop["rms_MeV_dropped"],
        "total": "",
        "pass_condition_met": S7,
    })
    wc_rows.append({
        "label": wc_shuffle["label"], "kind": "row_shuffle",
        "perturbation": "shuffle B_u labels seed 20260623",
        "metric_name": "rms_MeV_shuffled",
        "metric_value": wc_shuffle["rms_MeV_shuffled"],
        "total": "",
        "pass_condition_met": S8,
    })
    write_csv(HERE / "CR245_wrong_controls.csv", wc_rows)

    summary = {
        "verdict": verdict,
        "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA,
        "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "substrate_atoms": {"R": R, "D": D, "S": S, "Theta": THETA,
                            "M": M_LEDGER, "L": L_LEDGER, "V": V_LEDGER,
                            "kappa": str(KAPPA), "g": str(G),
                            "kappa-2g": str(KAPPA_MINUS_2G),
                            "asym_identity_constant": f"{ASYM_CONST.numerator}/{ASYM_CONST.denominator}",
                            "asym_identity_constant_float": float(ASYM_CONST)},
        "stage_1_asymmetry_identity": {
            "train_total": asym_train_total,
            "train_match": asym_train_match,
            "test_total": asym_test_total,
            "test_match": asym_test_match,
            "all_exact": S1,
        },
        "stage_2_bw_fit_A_ge_16": fit,
        "stage_2_train_fitted": {"rms_u": fitted_train["rms_u"], "rms_MeV": fitted_train["rms_MeV"], "R2": fitted_train["R2"]},
        "stage_2_test_fitted": {"rms_u": fitted_test["rms_u"], "rms_MeV": fitted_test["rms_MeV"], "R2": fitted_test["R2"]},
        "stage_3_typed_search": typed_search,
        "stage_3_summary": {
            "matched_within_5pct": matched_5pct,
            "matched_within_1pct": sum(1 for k, v in typed_search.items() if v["best_candidate"]["within_1pct"]),
            "total_coefs": 5,
        },
        "stage_4_zero_free": {
            "substitutions": zf["substitutions"],
            "train_rms_u": zf_train["rms_u"], "train_rms_MeV": zf_train["rms_MeV"], "train_R2": zf_train["R2"],
            "test_rms_u": zf_test["rms_u"], "test_rms_MeV": zf_test["rms_MeV"], "test_R2": zf_test["R2"],
        },
        "wrong_controls_asym_R": wc_asym_R,
        "wrong_control_drop_asym": wc_drop,
        "wrong_control_shuffle": wc_shuffle,
        "strong_pass_conditions": {
            "S1_asymmetry_identity_exact": S1, "S2_bw_fit_rms_under_5MeV": S2,
            "S3_at_least_3_coefs_typed_5pct": S3, "S4_zero_free_train_within_1p5x": S4,
            "S5_zero_free_test_within_1p5x": S5, "S6_R_perturbations_break_identity": S6,
            "S7_asym_removal_degrades": S7, "S8_row_shuffle_degrades": S8,
        },
        "fail_conditions": {"F1_identity_fails": F1, "F2_fit_blows_up": F2, "F3_asym_removal_no_op": F3},
    }
    (HERE / "CR245_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    manifest = [
        {"file": "CR245_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train_all)},
        {"file": "CR245_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test_all)},
        {"file": "CR245_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR245_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print()
    print(f"Stage 1 — Asymmetry identity exact: train {asym_train_match}/{asym_train_total}, test {asym_test_match}/{asym_test_total}")
    print(f"Stage 2 — BW fit (A>=16):  RMS={fit['rms_MeV']:.4f} MeV  R^2={fit['R2']:.5f}  n={fit['n_rows']}")
    print("Stage 3 — Typed coefficient candidates:")
    for key in ("a_volume", "b_surface", "c_coulomb", "d_asym_NmZ2_over_A", "e_pair"):
        info = typed_search[key]; b = info["best_candidate"]
        flag = "WITHIN_5PCT" if b["within_5pct"] else "out of band"
        flag1 = "  WITHIN_1PCT" if b["within_1pct"] else ""
        print(f"  {key:24s} fitted={info['fitted_u']:+.5e} u  ({info['fitted_MeV']:+.4f} MeV)  best={b['name']:20s}={b['value']:+.5e}  rel={b['rel_dev']:.4f}  {flag}{flag1}")
    print(f"  Matched within 5%: {matched_5pct}/5; within 1%: {sum(1 for k,v in typed_search.items() if v['best_candidate']['within_1pct'])}/5")
    print(f"Stage 4 — Zero-free typed candidate: train RMS={zf_train['rms_MeV']:.4f} MeV; test RMS={zf_test['rms_MeV']:.4f} MeV")
    print(f"        Fitted               train RMS={fitted_train['rms_MeV']:.4f} MeV; test RMS={fitted_test['rms_MeV']:.4f} MeV")
    print(f"Stage 5 — WCs:")
    for w in wc_asym_R:
        print(f"  {w['label']}  R={w['R_perturbation']}  breaks {w['nontrivial_break_count']}/{w['nontrivial_total']} nontrivial rows ({w['total']-w['nontrivial_total']} N=Z rows trivial)  pass={w['breaks_all_nontrivial_rows']}")
    print(f"  {wc_drop['label']}  drop-asym RMS={wc_drop['rms_MeV_dropped']:.4f} MeV  (fitted {fit['rms_MeV']:.4f})  S7={S7}")
    print(f"  {wc_shuffle['label']}  shuffle RMS={wc_shuffle['rms_MeV_shuffled']:.4f} MeV  (fitted {fit['rms_MeV']:.4f})  S8={S8}")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4} S5={S5} S6={S6} S7={S7} S8={S8}")


if __name__ == "__main__":
    main()
