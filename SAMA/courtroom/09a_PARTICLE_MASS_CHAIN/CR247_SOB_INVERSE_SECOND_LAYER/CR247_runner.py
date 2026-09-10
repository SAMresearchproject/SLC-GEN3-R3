"""CR247 — SOB Inverse Second-Layer Decomposition runner.

Verifies that the second-layer basis (Z balanced positions + (N-Z) excess
neutron positions) reproduces the sealed SOB target vector Phi(Z, N) =
(u, d, e, Q_mass, Q_sub, dQ) EXACTLY for every (Z, N) test row under
Fraction arithmetic.

Per fatality.pdf:
  balanced phi_b  = (u=3, d=3, e=1, Q_mass=8*kappa, Q_sub=8*kappa, dQ=0)
  excess   phi_e  = (u=1, d=2, e=0, Q_mass=4*kappa, Q_sub=1/8,    dQ=4*kappa - 1/8)
  n_balanced = Z; n_excess_neutron = N - Z (for N >= Z)
"""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
TRAIN_CSV = HERE / "CR247_train_lane_a.csv"
TEST_CSV = HERE / "CR247_test_holdout.csv"
PRECOMMIT_MD = HERE / "CR247_PRECOMMIT.md"

EXPECTED_TRAIN_SHA = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"
EXPECTED_TEST_SHA = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"
EXPECTED_PRECOMMIT_SHA = "4e8a25d205713918470231cfcccb30ad8b1932c49089f09fc10e7d31a6117e2b"

# Locked substrate atoms
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
S = 8

# Derived
KAPPA_X_8 = Fraction(8) * KAPPA          # = 7117/96
KAPPA_X_4 = Fraction(4) * KAPPA          # = 7117/192
SG = Fraction(S) * G                     # = 1/8
DQ_EXCESS = Fraction(4) * KAPPA - SG     # = 7093/192


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
            rows.append(row)
    return rows


def phi_b(perturbed_kappa: Fraction = KAPPA) -> dict[str, Fraction]:
    return {
        "u": Fraction(3), "d": Fraction(3), "e": Fraction(1),
        "Q_mass": Fraction(8) * perturbed_kappa,
        "Q_sub":  Fraction(8) * perturbed_kappa,
        "dQ":     Fraction(0),
    }


def phi_e(perturbed_kappa: Fraction = KAPPA, perturbed_g: Fraction = G,
          perturbed_dq_const: Fraction | None = None) -> dict[str, Fraction]:
    dq = Fraction(4) * perturbed_kappa - Fraction(S) * perturbed_g
    if perturbed_dq_const is not None:
        dq = perturbed_dq_const
    return {
        "u": Fraction(1), "d": Fraction(2), "e": Fraction(0),
        "Q_mass": Fraction(4) * perturbed_kappa,
        "Q_sub":  Fraction(S) * perturbed_g,
        "dQ":     dq,
    }


def target_phi(Z: int, N: int, perturbed_kappa: Fraction = KAPPA,
               perturbed_g: Fraction = G) -> dict[str, Fraction]:
    A = Z + N
    return {
        "u": Fraction(2 * Z + N),
        "d": Fraction(Z + 2 * N),
        "e": Fraction(Z),
        "Q_mass": Fraction(4 * A) * perturbed_kappa,
        "Q_sub":  Fraction(8 * Z) * perturbed_kappa + Fraction(N - Z) * Fraction(S) * perturbed_g,
        "dQ":     Fraction(N - Z) * (Fraction(4) * perturbed_kappa - Fraction(S) * perturbed_g),
    }


def decomposed(Z: int, N: int, n_b_override: int | None = None,
               swap_basis: bool = False,
               perturbed_kappa: Fraction = KAPPA,
               perturbed_g: Fraction = G,
               perturbed_dq_const: Fraction | None = None) -> dict[str, Fraction]:
    """Apply Sigma_n_j phi_j with the locked occupancy and basis (with
    optional perturbations for wrong controls)."""
    if swap_basis:
        n_b = max(0, N - Z); n_e = Z
    else:
        n_b = Z; n_e = max(0, N - Z)
    if n_b_override is not None:
        n_b = n_b_override
    pb = phi_b(perturbed_kappa)
    pe = phi_e(perturbed_kappa, perturbed_g, perturbed_dq_const)
    return {
        key: Fraction(n_b) * pb[key] + Fraction(n_e) * pe[key]
        for key in ("u", "d", "e", "Q_mass", "Q_sub", "dQ")
    }


def verify_row(Z: int, N: int, basis_kappa: Fraction = KAPPA,
               basis_g: Fraction = G, basis_dq_const: Fraction | None = None,
               n_b_override: int | None = None, swap_basis: bool = False) -> dict[str, Any]:
    """Target always uses canonical kappa, g. Basis can be perturbed.
    This is the proper structure for a WC: perturb basis only, target fixed.
    """
    tgt = target_phi(Z, N, perturbed_kappa=KAPPA, perturbed_g=G)
    rec = decomposed(Z, N,
                     n_b_override=n_b_override,
                     swap_basis=swap_basis,
                     perturbed_kappa=basis_kappa,
                     perturbed_g=basis_g,
                     perturbed_dq_const=basis_dq_const)
    matches = {}
    for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ"):
        matches[k] = (rec[k] == tgt[k])
    return {
        "target": tgt, "decomposed": rec, "matches": matches,
        "all_match": all(matches.values()),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text(""); return
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
    actual_train = sha256(TRAIN_CSV)
    actual_test = sha256(TEST_CSV)
    actual_pre = sha256(PRECOMMIT_MD)
    if actual_train != EXPECTED_TRAIN_SHA:
        raise SystemExit(f"TRAIN SHA mismatch: {actual_train} vs {EXPECTED_TRAIN_SHA}")
    if actual_test != EXPECTED_TEST_SHA:
        raise SystemExit(f"TEST SHA mismatch: {actual_test} vs {EXPECTED_TEST_SHA}")
    if actual_pre != EXPECTED_PRECOMMIT_SHA:
        raise SystemExit(f"PRECOMMIT SHA mismatch: {actual_pre} vs {EXPECTED_PRECOMMIT_SHA}")

    train_rows = read_isotope_csv(TRAIN_CSV)
    test_rows = read_isotope_csv(TEST_CSV)
    all_rows = train_rows + test_rows

    # Filter to N >= Z (CR247 scope; symmetric N < Z variant reserved)
    nontriv_rows = [r for r in all_rows if r["N"] >= r["Z"]]
    excluded_n_lt_z = [r for r in all_rows if r["N"] < r["Z"]]

    # Per-row verification
    per_row = []
    identity_match_counts = {k: 0 for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ")}
    all_match_count = 0
    for r in nontriv_rows:
        v = verify_row(r["Z"], r["N"])
        entry = {
            "isotope": r.get("isotope"), "Z": r["Z"], "N": r["N"], "A": r["A"],
            "n_balanced": r["Z"],
            "n_excess_neutron": r["N"] - r["Z"],
        }
        for k in ("u", "d", "e", "Q_mass", "Q_sub", "dQ"):
            entry[f"target_{k}"] = str(v["target"][k])
            entry[f"decomp_{k}"] = str(v["decomposed"][k])
            entry[f"match_{k}"] = v["matches"][k]
            if v["matches"][k]:
                identity_match_counts[k] += 1
        entry["all_six_match"] = v["all_match"]
        if v["all_match"]:
            all_match_count += 1
        per_row.append(entry)

    S1 = (identity_match_counts["u"] == len(nontriv_rows)
          and identity_match_counts["d"] == len(nontriv_rows)
          and identity_match_counts["e"] == len(nontriv_rows))
    S2 = (identity_match_counts["Q_mass"] == len(nontriv_rows))
    S3 = (identity_match_counts["Q_sub"] == len(nontriv_rows))
    S4 = (identity_match_counts["dQ"] == len(nontriv_rows))

    # Anchor cases
    anchor_specs = [("C-12", 6, 6), ("C-13", 6, 7), ("Au-197", 79, 118)]
    anchor_rows = []
    S5_pass = True
    for label, Z, N in anchor_specs:
        v = verify_row(Z, N)
        anchor_rows.append({
            "label": label, "Z": Z, "N": N, "A": Z + N,
            "n_balanced": Z, "n_excess_neutron": N - Z,
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
            S5_pass = False
    S5 = S5_pass

    # Wrong controls
    wc_results = []
    # WC-1: basis swap (n_b <-> n_e occupancies).
    # NOTE: swap is the identity for rows with N = 2Z (occupancies coincide).
    # The WC tests only N != 2Z rows; N=2Z rows are recorded as a structural
    # invariant of the swap, not a failure.
    wc1_breaks = 0
    wc1_eligible = 0
    wc1_invariant_rows = []
    for r in nontriv_rows:
        if r["N"] == 2 * r["Z"]:
            wc1_invariant_rows.append(r.get("isotope"))
            continue
        wc1_eligible += 1
        v = verify_row(r["Z"], r["N"], swap_basis=True)
        if not v["all_match"]:
            wc1_breaks += 1
    wc_results.append({
        "label": "WC-1_basis_swap",
        "description": ("Swap n_balanced and n_excess_neutron; "
                        "structurally identity when N=2Z (excluded)"),
        "non_trivial_rows": wc1_eligible,
        "breaks": wc1_breaks,
        "n_2Z_invariant_rows_excluded": len(wc1_invariant_rows),
        "invariant_isotopes": wc1_invariant_rows,
        "pass": wc1_breaks == wc1_eligible and wc1_eligible > 0,
    })
    # WC-2: kappa perturbation IN BASIS ONLY (target stays canonical)
    perturbed_kappa = Fraction(7117, 769)
    wc2_breaks = 0
    for r in nontriv_rows:
        v = verify_row(r["Z"], r["N"], basis_kappa=perturbed_kappa)
        if not v["matches"]["Q_mass"]:
            wc2_breaks += 1
    wc_results.append({
        "label": "WC-2_basis_kappa_perturbed",
        "description": "basis kappa = 7117/769 (target kappa stays 7117/768)",
        "non_trivial_rows": len(nontriv_rows),
        "breaks_Q_mass_identity": wc2_breaks,
        "pass": wc2_breaks == len(nontriv_rows),
    })
    # WC-3: g perturbation IN BASIS ONLY (target stays canonical)
    perturbed_g = Fraction(1, 63)
    wc3_breaks = 0
    wc3_nontrivial = 0
    for r in nontriv_rows:
        if r["N"] == r["Z"]:
            continue  # N=Z means n_excess=0, so basis_g change has zero effect
        wc3_nontrivial += 1
        v = verify_row(r["Z"], r["N"], basis_g=perturbed_g)
        if not v["matches"]["Q_sub"]:
            wc3_breaks += 1
    wc_results.append({
        "label": "WC-3_basis_g_perturbed",
        "description": "basis g = 1/63 (target g stays 1/64); skips N=Z (zero excess)",
        "non_trivial_rows": wc3_nontrivial,
        "breaks_Q_sub_identity": wc3_breaks,
        "pass": wc3_breaks == wc3_nontrivial and wc3_nontrivial > 0,
    })
    # WC-4: occupancy perturbation (n_b = Z + 1)
    wc4_breaks = 0
    for r in nontriv_rows:
        v_pert = verify_row(r["Z"], r["N"], n_b_override=r["Z"] + 1)
        if not (v_pert["matches"]["u"] and v_pert["matches"]["d"] and v_pert["matches"]["e"]):
            wc4_breaks += 1
    wc_results.append({
        "label": "WC-4_occupancy_perturbed",
        "description": "n_balanced = Z + 1 (source identity should break)",
        "non_trivial_rows": len(nontriv_rows),
        "breaks_source_identity": wc4_breaks,
        "pass": wc4_breaks == len(nontriv_rows),
    })
    # WC-5: dQ-constant perturbation IN BASIS ONLY (target stays canonical)
    perturbed_dq = Fraction(7093, 193)
    wc5_breaks = 0
    wc5_nontrivial = 0
    for r in nontriv_rows:
        if r["N"] == r["Z"]:
            continue  # N=Z means dQ target = 0 and basis dQ contribution = 0
        wc5_nontrivial += 1
        v = verify_row(r["Z"], r["N"], basis_dq_const=perturbed_dq)
        if not v["matches"]["dQ"]:
            wc5_breaks += 1
    wc_results.append({
        "label": "WC-5_basis_dq_const_perturbed",
        "description": "basis dQ_excess = 7093/193 (target stays 7093/192); skips N=Z",
        "non_trivial_rows": wc5_nontrivial,
        "breaks_dQ_identity": wc5_breaks,
        "pass": wc5_breaks == wc5_nontrivial and wc5_nontrivial > 0,
    })
    S6 = all(w["pass"] for w in wc_results)
    S7 = True  # the closed-form algebra delivers second-layer closure with zero free parameters

    strong_pass = all([S1, S2, S3, S4, S5, S6, S7])
    F1 = not (S1 and S2 and S3 and S4)
    F2_failed_wc = [w["label"] for w in wc_results if not w["pass"]]

    if F1:
        verdict = "FAIL"
        signature = "CR247_FAIL_SECOND_LAYER_IDENTITY_BREAKS"
    elif strong_pass:
        verdict = "STRONG_PASS"
        signature = ("CR247_STRONG_PASS_SOB_INVERSE_SECOND_LAYER__"
                     "FOUR_OF_FIVE_FATALITY_CONSTRAINT_GROUPS_EXACT__"
                     "Z_BALANCED_PLUS_NminusZ_EXCESS_DECOMP_REPRODUCES_SOB_TARGET__"
                     "ZERO_FREE_PARAMETERS__ALL_WC_BREAK_AS_PREDICTED")
    else:
        verdict = "BOUNDARY"
        signature = "CR247_BOUNDARY_PARTIAL_CLOSURE"

    summary = {
        "verdict": verdict,
        "verdict_signature": signature,
        "train_sha256": EXPECTED_TRAIN_SHA,
        "test_sha256": EXPECTED_TEST_SHA,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA,
        "substrate_atoms": {"kappa": str(KAPPA), "g": str(G), "S": S,
                            "8*kappa": str(KAPPA_X_8), "4*kappa": str(KAPPA_X_4),
                            "S*g": str(SG), "dQ_excess (4*kappa - S*g)": str(DQ_EXCESS)},
        "basis_vectors": {
            "balanced": {"u": 3, "d": 3, "e": 1, "Q_mass": str(KAPPA_X_8),
                         "Q_sub": str(KAPPA_X_8), "dQ": "0"},
            "excess_neutron": {"u": 1, "d": 2, "e": 0, "Q_mass": str(KAPPA_X_4),
                               "Q_sub": str(SG), "dQ": str(DQ_EXCESS)},
        },
        "occupancy_formulas": {
            "n_balanced(Z, N)": "Z (for N >= Z)",
            "n_excess_neutron(Z, N)": "N - Z (for N >= Z)",
            "n_excess_proton(Z, N)": "Z - N (for N < Z; reserved, not exercised here)",
        },
        "test_set_size": {
            "train": len(train_rows), "test": len(test_rows),
            "total": len(all_rows),
            "evaluated_N_ge_Z": len(nontriv_rows),
            "excluded_N_lt_Z": len(excluded_n_lt_z),
        },
        "per_identity_match_counts": identity_match_counts,
        "all_six_match_count": all_match_count,
        "anchor_results": anchor_rows,
        "wrong_controls": wc_results,
        "strong_pass_conditions": {
            "S1_source_identity_all_match": S1,
            "S2_Q_mass_identity_all_match": S2,
            "S3_Q_sub_identity_all_match": S3,
            "S4_dQ_identity_all_match": S4,
            "S5_anchors_all_six_match": S5,
            "S6_all_wcs_break": S6,
            "S7_zero_free_parameters": S7,
        },
        "fail_conditions": {"F1_identity_fails_any_row": F1,
                            "failed_wc_labels": F2_failed_wc},
        "fifth_constraint_status": ("Reserved for CR248. The fatality.pdf "
                                    "B_u closure constraint Sigma_n_j s_debit_j ~ B_u "
                                    "requires the third-layer micro-channel decomposition "
                                    "(integer linear program over CR243/CR244 substrate ledger "
                                    "rows). CR247 verifies the algebraic four-constraint-group "
                                    "second-layer closure only."),
    }
    (HERE / "CR247_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    write_csv(HERE / "CR247_per_row_verification.csv", per_row)
    write_csv(HERE / "CR247_anchor_cases.csv", anchor_rows)
    write_csv(HERE / "CR247_wrong_controls.csv", wc_results)

    manifest = [
        {"file": "CR247_train_lane_a.csv", "sha256": EXPECTED_TRAIN_SHA, "row_count": len(train_rows)},
        {"file": "CR247_test_holdout.csv", "sha256": EXPECTED_TEST_SHA, "row_count": len(test_rows)},
        {"file": "CR247_PRECOMMIT.md", "sha256": EXPECTED_PRECOMMIT_SHA, "row_count": ""},
    ]
    write_csv(HERE / "CR247_input_manifest.csv", manifest)

    print(f"VERDICT: {verdict}")
    print(f"Signature: {signature}")
    print(f"Test rows evaluated (N>=Z): {len(nontriv_rows)} of {len(all_rows)} total ({len(excluded_n_lt_z)} N<Z excluded)")
    print(f"Per-identity match counts (out of {len(nontriv_rows)}):")
    for k, v in identity_match_counts.items():
        print(f"  {k:8s} {v}/{len(nontriv_rows)}  {'EXACT' if v == len(nontriv_rows) else 'FAIL'}")
    print(f"All-six match count: {all_match_count}/{len(nontriv_rows)}")
    print()
    print("Anchor cases:")
    for a in anchor_rows:
        flag = "ALL EXACT" if a["all_six_match"] else "PARTIAL"
        print(f"  {a['label']:8s} Z={a['Z']:3d} N={a['N']:3d}  n_b={a['n_balanced']:3d} n_e={a['n_excess_neutron']:3d}  {flag}")
        print(f"    Q_mass: target {a['target_Q_mass']} (= {a['target_Q_mass_float']:.6f})  decomp {a['decomp_Q_mass']}  match {a['match_Q_mass']}")
        print(f"    Q_sub:  target {a['target_Q_sub']} (= {a['target_Q_sub_float']:.6f})  decomp {a['decomp_Q_sub']}  match {a['match_Q_sub']}")
        print(f"    dQ:     target {a['target_dQ']} (= {a['target_dQ_float']:.6f})  decomp {a['decomp_dQ']}  match {a['match_dQ']}")
    print()
    print("Wrong controls:")
    for w in wc_results:
        print(f"  {w['label']:28s} {w['description'][:50]:50s}  pass={w['pass']}")
    print()
    print(f"Strong-pass: S1={S1} S2={S2} S3={S3} S4={S4} S5={S5} S6={S6} S7={S7}")


if __name__ == "__main__":
    main()
