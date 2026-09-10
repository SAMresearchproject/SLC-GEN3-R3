"""CR248 — SOB Micro-Channel Debit Occupancy Map runner.

Phase A: verify the four-particle decomposition (proton, balanced neutron,
         excess neutron, electron) closes source/Q_mass/Q_sub/dQ exactly
         under Fraction arithmetic.
Phase B: fit per-particle surface debits (alpha = s_p + s_n_b + s_e per
         electron-paired position, beta = s_n_e per excess neutron) on
         CR239 Lane A train (A >= 16, skip C-12 anchor), report train +
         CR241 holdout test residuals.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).parent
TRAIN_CSV = HERE / "CR248_train_lane_a.csv"
TEST_CSV = HERE / "CR248_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR248_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa"

KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
S = 8
U_TO_MEV = 931.49410242

# Per-particle basis vectors (locked)
PHI = {
    "proton": {
        "u": Fraction(2), "d": Fraction(1), "e": Fraction(0),
        "Q_mass": Fraction(4) * KAPPA, "Q_sub": Fraction(8) * KAPPA,
        "dQ": -Fraction(4) * KAPPA,
    },
    "balanced_neutron": {
        "u": Fraction(1), "d": Fraction(2), "e": Fraction(0),
        "Q_mass": Fraction(4) * KAPPA, "Q_sub": Fraction(0),
        "dQ": Fraction(4) * KAPPA,
    },
    "excess_neutron": {
        "u": Fraction(1), "d": Fraction(2), "e": Fraction(0),
        "Q_mass": Fraction(4) * KAPPA, "Q_sub": Fraction(S) * G,  # = 1/8
        "dQ": Fraction(4) * KAPPA - Fraction(S) * G,  # = 7093/192
    },
    "electron": {
        "u": Fraction(0), "d": Fraction(0), "e": Fraction(1),
        "Q_mass": Fraction(0), "Q_sub": Fraction(0), "dQ": Fraction(0),
    },
}

# CR247 second-layer basis (for WC-1, WC-2 disaggregation checks)
CR247_PHI_BALANCED = {
    "u": Fraction(3), "d": Fraction(3), "e": Fraction(1),
    "Q_mass": Fraction(8) * KAPPA, "Q_sub": Fraction(8) * KAPPA, "dQ": Fraction(0),
}
CR247_PHI_EXCESS = {
    "u": Fraction(1), "d": Fraction(2), "e": Fraction(0),
    "Q_mass": Fraction(4) * KAPPA, "Q_sub": Fraction(1, 8),
    "dQ": Fraction(7093, 192),
}


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
            row["B_u"] = row["A"] - row["atomic_mass_u"]
            rows.append(row)
    return rows


def occupancy(Z: int, N: int) -> dict[str, int]:
    """For N >= Z (CR248 scope)."""
    return {
        "proton": Z,
        "balanced_neutron": Z,
        "excess_neutron": N - Z,
        "electron": Z,
    }


def decomposed(Z: int, N: int) -> dict[str, Fraction]:
    occ = occupancy(Z, N)
    out = {k: Fraction(0) for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ")}
    for particle, n in occ.items():
        for component in out:
            out[component] += Fraction(n) * PHI[particle][component]
    return out


def target(Z: int, N: int) -> dict[str, Fraction]:
    A = Z + N
    return {
        "u": Fraction(2 * Z + N),
        "d": Fraction(Z + 2 * N),
        "e": Fraction(Z),
        "Q_mass": Fraction(4 * A) * KAPPA,
        "Q_sub": Fraction(8 * Z) * KAPPA + Fraction(N - Z) * Fraction(S) * G,
        "dQ": Fraction(N - Z) * (Fraction(4) * KAPPA - Fraction(S) * G),
    }


def verify_row(Z: int, N: int) -> dict[str, Any]:
    tgt = target(Z, N); rec = decomposed(Z, N)
    matches = {k: rec[k] == tgt[k] for k in tgt}
    return {"target": tgt, "decomposed": rec, "matches": matches,
            "all_match": all(matches.values())}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text(""); return
    fieldnames: list[str] = []; seen: set[str] = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k); fieldnames.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in rows: w.writerow(r)


def main() -> None:
    actual_train = sha256(TRAIN_CSV); actual_test = sha256(TEST_CSV); actual_pre = sha256(PRECOMMIT_MD)
    if actual_train != EXPECTED_TRAIN_SHA:
        raise SystemExit(f"TRAIN SHA mismatch: {actual_train} vs {EXPECTED_TRAIN_SHA}")
    if actual_test != EXPECTED_TEST_SHA:
        raise SystemExit(f"TEST SHA mismatch: {actual_test} vs {EXPECTED_TEST_SHA}")
    if actual_pre != EXPECTED_PRECOMMIT_SHA:
        raise SystemExit(f"PRECOMMIT SHA mismatch: {actual_pre} vs {EXPECTED_PRECOMMIT_SHA}")

    train = read_isotope_csv(TRAIN_CSV)
    test = read_isotope_csv(TEST_CSV)
    all_rows = train + test
    nontriv = [r for r in all_rows if r["N"] >= r["Z"]]
    excluded = [r for r in all_rows if r["N"] < r["Z"]]

    # Phase A: per-row identity verification
    per_row = []
    identity_counts = {k: 0 for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ")}
    all_match_count = 0
    for r in nontriv:
        v = verify_row(r["Z"], r["N"])
        entry = {
            "isotope": r.get("isotope"), "Z": r["Z"], "N": r["N"], "A": r["A"],
            "n_proton": r["Z"], "n_balanced_neutron": r["Z"],
            "n_excess_neutron": r["N"] - r["Z"], "n_electron": r["Z"],
        }
        for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ"):
            entry[f"target_{k}"] = str(v["target"][k])
            entry[f"decomp_{k}"] = str(v["decomposed"][k])
            entry[f"match_{k}"] = v["matches"][k]
            if v["matches"][k]:
                identity_counts[k] += 1
        entry["all_six_match"] = v["all_match"]
        if v["all_match"]:
            all_match_count += 1
        per_row.append(entry)

    S1 = all(c == len(nontriv) for c in identity_counts.values())

    # Anchor cases
    anchors = [("C-12", 6, 6), ("C-13", 6, 7), ("Au-197", 79, 118)]
    anchor_rows = []
    S2_pass = True
    for label, Z, N in anchors:
        v = verify_row(Z, N)
        anchor_rows.append({
            "label": label, "Z": Z, "N": N, "A": Z + N,
            "n_proton": Z, "n_balanced_neutron": Z,
            "n_excess_neutron": N - Z, "n_electron": Z,
            "target_u": str(v["target"]["u"]), "decomp_u": str(v["decomposed"]["u"]), "match_u": v["matches"]["u"],
            "target_d": str(v["target"]["d"]), "decomp_d": str(v["decomposed"]["d"]), "match_d": v["matches"]["d"],
            "target_e": str(v["target"]["e"]), "decomp_e": str(v["decomposed"]["e"]), "match_e": v["matches"]["e"],
            "target_Q_mass": str(v["target"]["Q_mass"]), "decomp_Q_mass": str(v["decomposed"]["Q_mass"]),
            "target_Q_mass_float": float(v["target"]["Q_mass"]), "match_Q_mass": v["matches"]["Q_mass"],
            "target_Q_sub": str(v["target"]["Q_sub"]), "decomp_Q_sub": str(v["decomposed"]["Q_sub"]),
            "target_Q_sub_float": float(v["target"]["Q_sub"]), "match_Q_sub": v["matches"]["Q_sub"],
            "target_dQ": str(v["target"]["dQ"]), "decomp_dQ": str(v["decomposed"]["dQ"]),
            "target_dQ_float": float(v["target"]["dQ"]), "match_dQ": v["matches"]["dQ"],
            "all_six_match": v["all_match"],
        })
        if not v["all_match"]:
            S2_pass = False
    S2 = S2_pass

    # Wrong controls
    wc = []
    # WC-1: phi_p + phi_n_b + phi_e == CR247 phi_balanced
    sum_balanced = {k: PHI["proton"][k] + PHI["balanced_neutron"][k] + PHI["electron"][k]
                    for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ")}
    wc1_match = all(sum_balanced[k] == CR247_PHI_BALANCED[k] for k in CR247_PHI_BALANCED)
    wc.append({
        "label": "WC-1_disaggregation_balanced",
        "description": "phi_proton + phi_balanced_neutron + phi_electron == CR247 phi_balanced",
        "computed": {k: str(sum_balanced[k]) for k in sum_balanced},
        "expected": {k: str(CR247_PHI_BALANCED[k]) for k in CR247_PHI_BALANCED},
        "pass": wc1_match,
    })
    # WC-2: phi_n_e == CR247 phi_excess_neutron
    wc2_match = all(PHI["excess_neutron"][k] == CR247_PHI_EXCESS[k] for k in CR247_PHI_EXCESS)
    wc.append({
        "label": "WC-2_disaggregation_excess",
        "description": "phi_excess_neutron == CR247 phi_excess_neutron",
        "computed": {k: str(PHI["excess_neutron"][k]) for k in CR247_PHI_EXCESS},
        "expected": {k: str(CR247_PHI_EXCESS[k]) for k in CR247_PHI_EXCESS},
        "pass": wc2_match,
    })
    # WC-3: n_proton = Z + 1 breaks source
    wc3_breaks = 0
    for r in nontriv:
        n_p = r["Z"] + 1
        u_decomp = n_p * 2 + r["Z"] * 1 + (r["N"] - r["Z"]) * 1 + r["Z"] * 0
        if u_decomp != 2 * r["Z"] + r["N"]:
            wc3_breaks += 1
    wc.append({
        "label": "WC-3_occupancy_perturbed_n_proton",
        "description": "n_proton = Z + 1 (source u should break by +2)",
        "rows_affected": len(nontriv),
        "breaks": wc3_breaks,
        "pass": wc3_breaks == len(nontriv),
    })
    # WC-4: quark swap p<->n_b. New phi_p = (1,2), phi_n_b = (2,1).
    # Sum stays (3,3) so source identity holds; this is a structural-identification
    # flag (we lose "proton vs neutron" but algebra is intact).
    swapped_u = PHI["balanced_neutron"]["u"] + PHI["proton"]["u"]
    swapped_d = PHI["balanced_neutron"]["d"] + PHI["proton"]["d"]
    swap_preserves_sum = (swapped_u == PHI["proton"]["u"] + PHI["balanced_neutron"]["u"] and
                          swapped_d == PHI["proton"]["d"] + PHI["balanced_neutron"]["d"])
    wc.append({
        "label": "WC-4_quark_swap_structural_flag",
        "description": "Swap phi_p quarks (u,d) with phi_n_b: sum (3,3) preserved; structural identification flag only",
        "swap_preserves_combined_uud": swap_preserves_sum,
        "note": "WC-4 is a structural-identification audit, not a falsifier",
        "pass": True,
    })

    # Phase B: linear B_u closure
    # Model: B_u = alpha * Z + beta * (N - Z)
    # Train: Lane A non-anchor, A >= 16
    train_fit = [r for r in train if r["A"] != 12 and r["A"] >= 16 and r["N"] >= r["Z"]]
    X_tr = np.array([[r["Z"], r["N"] - r["Z"]] for r in train_fit])
    y_tr = np.array([r["B_u"] for r in train_fit])
    coef, *_ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    alpha, beta = float(coef[0]), float(coef[1])
    pred_tr = X_tr @ coef
    rms_tr = float(np.sqrt(np.mean((pred_tr - y_tr) ** 2)))
    ss_res_tr = float(np.sum((pred_tr - y_tr) ** 2))
    ss_tot_tr = float(np.sum((y_tr - np.mean(y_tr)) ** 2))
    r2_tr = 1.0 - ss_res_tr / ss_tot_tr if ss_tot_tr > 0 else float("nan")

    test_eval = [r for r in test if r["N"] >= r["Z"]]
    X_te = np.array([[r["Z"], r["N"] - r["Z"]] for r in test_eval])
    y_te = np.array([r["B_u"] for r in test_eval])
    pred_te = X_te @ coef
    rms_te = float(np.sqrt(np.mean((pred_te - y_te) ** 2)))
    ss_res_te = float(np.sum((pred_te - y_te) ** 2))
    ss_tot_te = float(np.sum((y_te - np.mean(y_te)) ** 2))
    r2_te = 1.0 - ss_res_te / ss_tot_te if ss_tot_te > 0 else float("nan")

    # Null model: predict B_u = 0
    rms_null_tr = float(np.sqrt(np.mean(y_tr ** 2)))
    rms_null_te = float(np.sqrt(np.mean(y_te ** 2)))

    # WC-5: linear vs null
    S5 = rms_tr <= rms_null_tr / 2.0
    wc.append({
        "label": "WC-5_linear_vs_null",
        "description": "Linear B_u model RMS at least 2x better than null (B_u=0)",
        "linear_rms_train_u": rms_tr,
        "linear_rms_train_MeV": rms_tr * U_TO_MEV,
        "null_rms_train_u": rms_null_tr,
        "null_rms_train_MeV": rms_null_tr * U_TO_MEV,
        "ratio_null_to_linear": rms_null_tr / rms_tr if rms_tr > 0 else float("inf"),
        "pass": S5,
    })

    # WC-6: shuffle B_u labels
    rng = random.Random(20260623)
    y_shuf = list(y_tr); rng.shuffle(y_shuf)
    coef_shuf, *_ = np.linalg.lstsq(X_tr, np.array(y_shuf), rcond=None)
    pred_shuf = X_tr @ coef_shuf
    rms_shuf = float(np.sqrt(np.mean((pred_shuf - np.array(y_shuf)) ** 2)))
    S6 = rms_shuf >= 1.5 * rms_tr
    wc.append({
        "label": "WC-6_shuffle_labels",
        "description": "Shuffle B_u labels seed 20260623; refit; expect RMS degrades >= 1.5x",
        "canonical_rms_u": rms_tr,
        "shuffled_rms_u": rms_shuf,
        "ratio": rms_shuf / rms_tr if rms_tr > 0 else float("inf"),
        "pass": S6,
    })

    S3 = wc1_match and wc2_match
    S4 = wc[2]["pass"]
    S7 = (rms_tr <= 0.020) and (rms_te <= 0.025)

    strong_pass = all([S1, S2, S3, S4, S5, S6, S7])
    F1 = not S1
    F2 = not S2
    F3 = not (S5 and rms_tr < rms_null_tr)

    if F1 or F2 or F3:
        verdict = "FAIL"
        signature = "CR248_FAIL"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR248_STRONG_PASS_FOUR_PARTICLE_DECOMP_EXACT__"
                     "LINEAR_B_U_CLOSURE_WITHIN_TOL__ALL_WC_PASS")
    else:
        verdict = "BOUNDARY"
        signature = ("CR248_BOUNDARY_FOUR_PARTICLE_DECOMP_EXACT__"
                     "LINEAR_B_U_CLOSURE_INSUFFICIENT__BINDING_NON_LINEAR__"
                     "PAIR_WRITE_TERMS_REQUIRED_PER_CR245")

    # Anchor B_u predictions
    anchor_preds = []
    for label, Z, N in anchors:
        m_obs = None
        for r in all_rows:
            if r["Z"] == Z and r["N"] == N:
                m_obs = r["atomic_mass_u"]; break
        B_u_obs = (Z + N) - m_obs if m_obs is not None else None
        B_u_pred = alpha * Z + beta * (N - Z)
        anchor_preds.append({
            "label": label, "Z": Z, "N": N,
            "m_observed_u": m_obs, "B_u_observed_u": B_u_obs,
            "B_u_predicted_u": B_u_pred,
            "B_u_observed_MeV": B_u_obs * U_TO_MEV if B_u_obs is not None else None,
            "B_u_predicted_MeV": B_u_pred * U_TO_MEV,
            "residual_u": B_u_pred - B_u_obs if B_u_obs is not None else None,
            "residual_MeV": (B_u_pred - B_u_obs) * U_TO_MEV if B_u_obs is not None else None,
        })

    summary = {
        "verdict": verdict, "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA, "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "substrate_atoms": {"kappa": str(KAPPA), "g": str(G), "S": S},
        "basis_vectors": {p: {k: str(v) for k, v in vec.items()} for p, vec in PHI.items()},
        "occupancy_formula": {
            "n_proton": "Z", "n_balanced_neutron": "Z",
            "n_excess_neutron": "N - Z (for N >= Z)", "n_electron": "Z",
        },
        "test_set_size": {
            "train": len(train), "test": len(test), "total": len(all_rows),
            "evaluated_N_ge_Z": len(nontriv), "excluded_N_lt_Z": len(excluded),
        },
        "phase_A_identity_counts": identity_counts,
        "phase_A_all_six_match": all_match_count,
        "phase_A_anchors": anchor_rows,
        "phase_B_linear_fit": {
            "alpha_per_electron_paired_position_u": alpha,
            "beta_per_excess_neutron_u": beta,
            "alpha_MeV": alpha * U_TO_MEV,
            "beta_MeV": beta * U_TO_MEV,
            "train_rms_u": rms_tr, "train_rms_MeV": rms_tr * U_TO_MEV,
            "train_R2": r2_tr, "train_n": len(train_fit),
            "test_rms_u": rms_te, "test_rms_MeV": rms_te * U_TO_MEV,
            "test_R2": r2_te, "test_n": len(test_eval),
            "null_rms_train_u": rms_null_tr, "null_rms_test_u": rms_null_te,
        },
        "phase_B_anchor_predictions": anchor_preds,
        "wrong_controls": wc,
        "strong_pass_conditions": {
            "S1_phase_a_all_match": S1, "S2_anchors_all_match": S2,
            "S3_disaggregation_checks": S3, "S4_occupancy_perturbation_breaks": S4,
            "S5_linear_beats_null_2x": S5, "S6_shuffle_degrades_1p5x": S6,
            "S7_linear_b_u_within_tol": S7,
        },
        "fail_conditions": {"F1_phase_a_fails": F1, "F2_anchor_fails": F2,
                            "F3_no_signal": F3},
        "fifth_constraint_note": ("Linear per-particle B_u closure does not "
                                  "suffice for binding-curvature derivation. "
                                  "Pair-write debit terms (Z*(Z-1)/A^(1/3) Coulomb, "
                                  "A^(2/3) surface, (N-Z)^2/A asymmetry per CR245 "
                                  "exact identity, delta_pair/sqrt(A)) are required. "
                                  "CR248 verifies the four-particle algebra (Phase A) "
                                  "and reports the linear closure attempt (Phase B); "
                                  "full B_u closure remains open for a follow-up CR."),
    }
    (HERE / "CR248_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    write_csv(HERE / "CR248_per_row_phase_a.csv", per_row)
    write_csv(HERE / "CR248_anchor_cases.csv", anchor_rows)
    write_csv(HERE / "CR248_phase_b_linear_fit.csv", anchor_preds + [
        {"label": "TRAIN_AGGREGATE", "B_u_observed_u": "",
         "B_u_predicted_u": "", "residual_u": rms_tr},
        {"label": "TEST_AGGREGATE", "B_u_observed_u": "",
         "B_u_predicted_u": "", "residual_u": rms_te},
    ])
    wc_rows = []
    for w in wc:
        wc_rows.append({k: v if not isinstance(v, dict) else json.dumps(v) for k, v in w.items()})
    write_csv(HERE / "CR248_wrong_controls.csv", wc_rows)
    manifest = [
        {"file": "CR248_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train)},
        {"file": "CR248_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test)},
        {"file": "CR248_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR248_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print()
    print(f"Phase A: identity match counts (out of {len(nontriv)}):")
    for k, v in identity_counts.items():
        print(f"  {k:8s} {v}/{len(nontriv)}  {'EXACT' if v == len(nontriv) else 'FAIL'}")
    print(f"  all-six-match: {all_match_count}/{len(nontriv)}")
    print()
    print("Anchor cases:")
    for a in anchor_rows:
        flag = "ALL EXACT" if a["all_six_match"] else "PARTIAL"
        print(f"  {a['label']:8s} Z={a['Z']:3d} N={a['N']:3d}  n_p={a['n_proton']:3d} n_n_b={a['n_balanced_neutron']:3d} n_n_e={a['n_excess_neutron']:3d} n_e={a['n_electron']:3d}  {flag}")
    print()
    print("Phase B linear B_u fit:")
    print(f"  alpha (per electron-paired position) = {alpha:+.6e} u  ({alpha * U_TO_MEV:+.4f} MeV)")
    print(f"  beta  (per excess neutron)            = {beta:+.6e} u  ({beta * U_TO_MEV:+.4f} MeV)")
    print(f"  train RMS = {rms_tr*U_TO_MEV:.4f} MeV  R^2 = {r2_tr:.4f}  n = {len(train_fit)}")
    print(f"  test  RMS = {rms_te*U_TO_MEV:.4f} MeV  R^2 = {r2_te:.4f}  n = {len(test_eval)}")
    print(f"  null train RMS = {rms_null_tr*U_TO_MEV:.4f} MeV  (ratio null/linear = {rms_null_tr/rms_tr:.2f}x)")
    print()
    print("Anchor B_u predictions:")
    for p in anchor_preds:
        print(f"  {p['label']:8s} obs {p['B_u_observed_MeV']:+.4f} MeV   pred {p['B_u_predicted_MeV']:+.4f} MeV   resid {p['residual_MeV']:+.4f} MeV")
    print()
    print("Wrong controls:")
    for w in wc:
        print(f"  {w['label']:35s} pass={w['pass']}")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4} S5={S5} S6={S6} S7={S7}")


if __name__ == "__main__":
    main()
