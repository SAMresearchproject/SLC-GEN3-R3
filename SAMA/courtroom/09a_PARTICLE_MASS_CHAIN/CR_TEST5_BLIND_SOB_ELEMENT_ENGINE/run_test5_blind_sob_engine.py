"""
TEST 5 - BLIND SOB ELEMENT ENGINE

Two modes:
    --mode generate           : produce no-name 126-row predictions from native constants only
    --mode reveal --reveal-csv: score sealed predictions against an external reveal reference

Generate mode contains NO element name dictionary, NO measured masses, NO half-lives, NO
external stability labels. The row IDs are E001..E126 only.

Reveal mode refuses to run unless hashes/no_name_predictions_CURRENT_HASH.txt exists.

Locked precommit: PRECOMMIT.md (sha bfc632ac4e9537e42c32c45edd229c0cf0cbe5aaa2eafa9aee8d1076cefbfcb4).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
CONTROLS = ROOT / "controls"
HASHES = ROOT / "hashes"
HASHES_TXT = ROOT / "HASHES.txt"

NO_NAME_CSV = OUTPUTS / "test5_no_name_predictions.csv"
INTERNAL_CHECKS = OUTPUTS / "test5_internal_checks.json"
INTERNAL_VERDICT = OUTPUTS / "test5_internal_verdict.md"
NO_NAME_HASH_TXT = HASHES / "no_name_predictions_CURRENT_HASH.txt"
REVEAL_SCORED = OUTPUTS / "test5_reveal_scored.csv"
REVEAL_SUMMARY = OUTPUTS / "test5_reveal_score_summary.json"
REVEAL_VERDICT = OUTPUTS / "test5_reveal_verdict.md"
REVEAL_HASH_TXT = HASHES / "reveal_outputs_CURRENT_HASH.txt"

# Native constants (the ONLY engine inputs)
ALPHA_H = 2
D = 3
R = 12
PI_LANES = (1, 2, 3, 4, 6, 8, 9, 12)
KAPPA_FLOOR = Fraction(7117, 768)
G_N = Fraction(1, 64)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def append_hash(path: Path):
    h = sha256_file(path)
    line = f"{h}  {path.relative_to(ROOT).as_posix()}"
    with HASHES_TXT.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return h


def derived_constants(R_val: int, D_val: int, alpha_H_val: int = ALPHA_H):
    split = 2 ** D_val
    R2 = R_val * R_val
    native_capacity = (R2 * (split - 1)) // split  # = R^2 * (1 - 1/2^D)
    frontier_start = native_capacity - 8 + 1
    T = R2 // split
    Zc = D_val ** (D_val + 1)
    hidden_set = (1, 2, 3, 4, 6, 8, 9, 12)
    H = sum(hidden_set)  # 45 by definition of the bigrade set
    clock_boundary = Zc + alpha_H_val
    clock_hole_1 = H - alpha_H_val
    clock_hole_2 = clock_hole_1 + T
    return {
        "R": R_val,
        "D": D_val,
        "alpha_H": alpha_H_val,
        "split": split,
        "R2": R2,
        "native_capacity": native_capacity,
        "frontier_start": frontier_start,
        "T": T,
        "Zc": Zc,
        "H": H,
        "clock_boundary": clock_boundary,
        "clock_hole_1": clock_hole_1,
        "clock_hole_2": clock_hole_2,
    }


def neutron_for_Z(Z: int, R_val: int) -> dict:
    radix_cycle = ((Z - 1) // R_val) + 1
    selected_depth = max(0, radix_cycle - 1)
    delta_N = (Z * selected_depth) // R_val
    N = Z + delta_N
    A = Z + N
    return {
        "radix_cycle": radix_cycle,
        "selected_depth": selected_depth,
        "delta_N": delta_N,
        "N_pred": N,
        "A_pred": A,
    }


def quark_counts(Z: int, N: int) -> dict:
    return {
        "u_count": 2 * Z + N,
        "d_count": Z + 2 * N,
        "e_count": Z,
    }


def native_binding(Z: int, N: int) -> dict:
    G = Fraction(Z) * KAPPA_FLOOR + Fraction(N - Z) * G_N
    GR = 8 * G
    retained_7G = 7 * G
    released_1G = G
    split_check_error = abs(GR - (retained_7G + released_1G))
    return {
        "kappa_floor": str(KAPPA_FLOOR),
        "neutron_G_unit": str(G_N),
        "G_native": str(G),
        "GR_8G": str(GR),
        "retained_7G": str(retained_7G),
        "released_1G": str(released_1G),
        "split_check_error": str(split_check_error),
        "_G_frac": G,
        "_GR_frac": GR,
        "_retained_frac": retained_7G,
        "_released_frac": released_1G,
    }


def lane_stack(G_frac: Fraction, R_val: int) -> dict:
    lanes = {}
    for p in PI_LANES:
        lanes[f"lane_{p}G"] = str(p * G_frac)
    lanes["_lane_8G_frac"] = 8 * G_frac
    lanes["_lane_12G_frac"] = 12 * G_frac
    lanes["_R_times_G_frac"] = Fraction(R_val) * G_frac
    return lanes


def clock_state(Z: int, consts: dict) -> str:
    if Z in (consts["clock_hole_1"], consts["clock_hole_2"]):
        return "CLOCK_HOLE"
    if Z >= consts["frontier_start"]:
        return "FRONTIER"
    if Z <= consts["clock_boundary"]:
        return "CLOCK_CLOSED"
    return "RADIOACTIVE_OPEN"


def shell_fill(Z: int) -> dict:
    """Standard 2n^2 shells filled sequentially. C_n = 2n^2 for n=1,2,3,..."""
    caps = []
    fills = []
    n = 1
    remaining = Z
    while remaining > 0 or n <= 6:
        cap = 2 * n * n
        if remaining <= 0 and n > 6:
            break
        if remaining >= cap:
            fills.append(cap)
            caps.append(cap)
            remaining -= cap
        elif remaining > 0:
            fills.append(remaining)
            caps.append(cap)
            remaining = 0
        else:
            fills.append(0)
            caps.append(cap)
        n += 1
        if n > 12:
            break
    while len(caps) < 6:
        n_extra = len(caps) + 1
        caps.append(2 * n_extra * n_extra)
        fills.append(0)
    outer_idx = max((i + 1 for i, f in enumerate(fills) if f > 0), default=0)
    outer_occ = fills[outer_idx - 1] if outer_idx > 0 else 0
    return {
        "shell_capacity_vector": "|".join(str(c) for c in caps),
        "shell_fill_vector": "|".join(str(f) for f in fills),
        "outer_shell_index": outer_idx,
        "outer_shell_occupancy": outer_occ,
    }


def generate_rows(R_val: int = R, D_val: int = D, alpha_H_val: int = ALPHA_H,
                  custom_clock_holes: tuple | None = None) -> tuple[list[dict], dict]:
    consts = derived_constants(R_val, D_val, alpha_H_val)
    if custom_clock_holes is not None:
        consts["clock_hole_1"], consts["clock_hole_2"] = custom_clock_holes
    cap = consts["native_capacity"]
    rows = []
    for Z in range(1, cap + 1):
        row = {"row_id": f"E{Z:03d}", "Z": Z}
        n = neutron_for_Z(Z, R_val)
        row.update(n)
        row["protons"] = Z
        row["neutrons"] = n["N_pred"]
        row["electrons"] = Z
        q = quark_counts(Z, n["N_pred"])
        row.update(q)
        row["source_address_nucleon"] = f"{Z}p + {n['N_pred']}n + {Z}e"
        row["source_address_quark"] = f"{q['u_count']}u + {q['d_count']}d + {Z}e"
        b = native_binding(Z, n["N_pred"])
        row.update({k: v for k, v in b.items() if not k.startswith("_")})
        lanes = lane_stack(b["_G_frac"], R_val)
        row.update({k: v for k, v in lanes.items() if not k.startswith("_")})
        row["lane_8G_equals_GR"] = (lanes["_lane_8G_frac"] == b["_GR_frac"])
        row["lane_12G_equals_R_times_G"] = (lanes["_lane_12G_frac"] == lanes["_R_times_G_frac"])
        row["clock_boundary"] = consts["clock_boundary"]
        row["clock_hole_1"] = consts["clock_hole_1"]
        row["clock_hole_2"] = consts["clock_hole_2"]
        row["frontier_start"] = consts["frontier_start"]
        row["clock_state"] = clock_state(Z, consts)
        sh = shell_fill(Z)
        row.update(sh)
        rows.append(row)
    return rows, consts


def write_predictions_csv(rows: list[dict], path: Path):
    fields = [
        "row_id", "Z",
        "radix_cycle", "selected_depth", "delta_N", "N_pred", "A_pred",
        "protons", "neutrons", "electrons",
        "u_count", "d_count", "e_count",
        "source_address_nucleon", "source_address_quark",
        "kappa_floor", "neutron_G_unit",
        "G_native", "GR_8G", "retained_7G", "released_1G", "split_check_error",
        "lane_1G", "lane_2G", "lane_3G", "lane_4G",
        "lane_6G", "lane_8G", "lane_9G", "lane_12G",
        "lane_8G_equals_GR", "lane_12G_equals_R_times_G",
        "clock_boundary", "clock_hole_1", "clock_hole_2", "frontier_start", "clock_state",
        "shell_capacity_vector", "shell_fill_vector",
        "outer_shell_index", "outer_shell_occupancy",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def run_internal_checks(rows: list[dict], consts: dict) -> dict:
    counts = {"CLOCK_CLOSED": 0, "CLOCK_HOLE": 0, "RADIOACTIVE_OPEN": 0, "FRONTIER": 0}
    for r in rows:
        counts[r["clock_state"]] += 1
    hole_zs = sorted([r["Z"] for r in rows if r["clock_state"] == "CLOCK_HOLE"])
    E001 = next((r for r in rows if r["row_id"] == "E001"), None)
    E079 = next((r for r in rows if r["row_id"] == "E079"), None)

    reveal_columns_forbidden = {"symbol", "name", "external_anchor_A", "external_anchor_N",
                                "external_stability_label", "measured_mass_u"}
    no_reveal_present = all(c not in r for r in rows for c in reveal_columns_forbidden)

    checks = {
        "row_count_is_126": len(rows) == 126,
        "native_capacity_is_126": consts["native_capacity"] == 126,
        "frontier_start_is_119": consts["frontier_start"] == 119,
        "clock_closed_count_is_81": counts["CLOCK_CLOSED"] == 81,
        "clock_hole_count_is_2": counts["CLOCK_HOLE"] == 2,
        "radioactive_open_count_is_35": counts["RADIOACTIVE_OPEN"] == 35,
        "frontier_count_is_8": counts["FRONTIER"] == 8,
        "clock_holes_are_43_and_61": hole_zs == [43, 61],
        "all_A_equal_Z_plus_N": all(r["A_pred"] == r["Z"] + r["N_pred"] for r in rows),
        "all_quark_counts_match_formula": all(
            r["u_count"] == 2 * r["Z"] + r["N_pred"]
            and r["d_count"] == r["Z"] + 2 * r["N_pred"]
            and r["e_count"] == r["Z"]
            for r in rows
        ),
        "all_GR_equal_8G": all(r["lane_8G"] == r["GR_8G"] for r in rows),
        "all_retained_plus_released_equal_GR": all(
            Decimal(r["split_check_error"]) < Decimal("1e-9") for r in rows
        ),
        "all_lane8_equal_GR": all(r["lane_8G_equals_GR"] for r in rows),
        "all_lane12_equal_R_times_G": all(r["lane_12G_equals_R_times_G"] for r in rows),
        "E079_N_A_quark_check": (
            E079 is not None
            and E079["N_pred"] == 118 and E079["A_pred"] == 197
            and E079["u_count"] == 276 and E079["d_count"] == 315 and E079["e_count"] == 79
        ),
        "E001_Z_N_A_quark_check": (
            E001 is not None
            and E001["N_pred"] == 1 and E001["A_pred"] == 2
            and E001["u_count"] == 3 and E001["d_count"] == 3 and E001["e_count"] == 1
        ),
        "no_reveal_columns_present": no_reveal_present,
        "_counts": counts,
        "_hole_zs": hole_zs,
    }
    return checks


def write_internal_verdict(checks: dict, consts: dict, path: Path) -> str:
    excluding = {k for k in checks if k.startswith("_")}
    bool_checks = {k: v for k, v in checks.items() if k not in excluding}
    all_pass = all(bool_checks.values())

    if all_pass:
        verdict = "PASS_TEST5_INTERNAL_BLIND_SOB_ENGINE"
    else:
        if not checks["row_count_is_126"]:
            verdict = "FAIL_TEST5_ROW_COUNT"
        elif not checks["native_capacity_is_126"]:
            verdict = "FAIL_TEST5_NATIVE_CAPACITY"
        elif not (checks["all_A_equal_Z_plus_N"] and checks["E079_N_A_quark_check"] and checks["E001_Z_N_A_quark_check"]):
            verdict = "FAIL_TEST5_NEUTRON_RULE"
        elif not checks["all_quark_counts_match_formula"]:
            verdict = "FAIL_TEST5_SOURCE_ADDRESS"
        elif not (checks["clock_closed_count_is_81"] and checks["clock_hole_count_is_2"]
                  and checks["radioactive_open_count_is_35"] and checks["frontier_count_is_8"]
                  and checks["clock_holes_are_43_and_61"]):
            verdict = "FAIL_TEST5_CLOCK_RULE"
        elif not (checks["all_GR_equal_8G"] and checks["all_retained_plus_released_equal_GR"]):
            verdict = "FAIL_TEST5_BINDING_SPLIT"
        elif not (checks["all_lane8_equal_GR"] and checks["all_lane12_equal_R_times_G"]):
            verdict = "FAIL_TEST5_LANE_STACK"
        elif not checks["no_reveal_columns_present"]:
            verdict = "FAIL_TEST5_REVEAL_LEAKAGE"
        else:
            verdict = "FAIL_TEST5_AUDIT_ROW"

    lines = [
        f"# Test 5 Internal Verdict",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        "## Internal Checks",
        "",
    ]
    for k, v in bool_checks.items():
        mark = "PASS" if v else "FAIL"
        lines.append(f"- [{mark}] {k}: {v}")
    lines.extend([
        "",
        f"## Derived Constants (from R=12, D=3, alpha_H=2)",
        "",
        f"- native_capacity = {consts['native_capacity']}",
        f"- frontier_start = {consts['frontier_start']}",
        f"- T = {consts['T']}",
        f"- Zc = {consts['Zc']}",
        f"- H = {consts['H']}",
        f"- clock_boundary = {consts['clock_boundary']}",
        f"- clock_hole_1 = {consts['clock_hole_1']}",
        f"- clock_hole_2 = {consts['clock_hole_2']}",
        "",
        f"## Clock State Counts",
        "",
    ])
    for k, v in checks["_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return verdict


# ---- WRONG CONTROLS ----

def run_wrong_control(label: str, R_val: int, D_val: int, alpha_H_val: int = ALPHA_H,
                      out_path: Path = None):
    try:
        rows, consts = generate_rows(R_val, D_val, alpha_H_val)
        checks = run_internal_checks(rows, consts)
        broke = not all(v for k, v in checks.items() if not k.startswith("_"))
    except Exception as exc:
        rows, consts = [], derived_constants(R_val, D_val, alpha_H_val)
        checks = {"_exception": str(exc), "row_count_is_126": False, "native_capacity_is_126": False}
        broke = True

    summary = {
        "control": label,
        "R": R_val,
        "D": D_val,
        "alpha_H": alpha_H_val,
        "native_capacity": consts["native_capacity"],
        "row_count": len(rows),
        "expected_row_count": 126,
        "row_count_matches_126": len(rows) == 126,
        "clock_closed_count_is_81": checks.get("clock_closed_count_is_81", False),
        "broke_as_predicted": broke,
        "details_first_check_failed": next(
            (k for k, v in checks.items() if not k.startswith("_") and not v),
            "no_failures",
        ),
    }

    fields = ["control", "R", "D", "alpha_H", "native_capacity", "row_count",
              "expected_row_count", "row_count_matches_126", "clock_closed_count_is_81",
              "broke_as_predicted", "details_first_check_failed"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    return summary


def run_shuffled_z_control(real_rows: list[dict], seed: int, reveal_path: Path | None,
                            out_path: Path):
    rng = random.Random(seed)
    z_labels = [r["Z"] for r in real_rows]
    rng.shuffle(z_labels)
    shuffled_clock_match = 0
    shuffled_N_A_match_count = 0
    reveal_map = {}
    if reveal_path and reveal_path.exists():
        with reveal_path.open("r", encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                z = int(r["Z"])
                reveal_map[z] = r
    for original_row, shuffled_z in zip(real_rows, z_labels):
        ref = reveal_map.get(shuffled_z)
        if ref:
            clock_pred = original_row["clock_state"]
            label = (ref.get("external_stability_label") or "").lower().strip()
            pred_is_stable = clock_pred == "CLOCK_CLOSED"
            ref_is_stable = label == "stable"
            if pred_is_stable == ref_is_stable:
                shuffled_clock_match += 1
            try:
                if int(ref["external_anchor_N"]) == original_row["N_pred"]:
                    shuffled_N_A_match_count += 1
            except (ValueError, KeyError):
                pass

    summary = {
        "control": "shuffled_Z",
        "seed": seed,
        "rows": len(real_rows),
        "shuffled_clock_match": shuffled_clock_match,
        "shuffled_N_match_against_external": shuffled_N_A_match_count,
        "expected_outcome": "reveal metrics degrade vs unshuffled",
    }
    fields = list(summary.keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    return summary


def run_random_clock_holes_control(seed: int, out_path: Path):
    rng = random.Random(seed)
    candidates = [z for z in range(1, 84) if z not in (43, 61)]
    rng.shuffle(candidates)
    new_holes = tuple(sorted(candidates[:2]))
    rows, consts = generate_rows(R, D, ALPHA_H, custom_clock_holes=new_holes)
    checks = run_internal_checks(rows, consts)
    broke = not checks["clock_holes_are_43_and_61"]
    summary = {
        "control": "random_clock_holes",
        "seed": seed,
        "new_holes": list(new_holes),
        "expected_holes": [43, 61],
        "clock_holes_are_43_and_61": checks["clock_holes_are_43_and_61"],
        "broke_as_predicted": broke,
    }
    fields = list(summary.keys())
    fields[2] = "new_holes"  # ensure ordering safe
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["control", "seed", "new_holes",
                                                "expected_holes",
                                                "clock_holes_are_43_and_61",
                                                "broke_as_predicted"],
                                lineterminator="\n")
        writer.writeheader()
        writer.writerow({k: summary[k] for k in writer.fieldnames})
    return summary


# ---- REVEAL MODE ----

def reveal_mode(reveal_csv: Path):
    if not NO_NAME_HASH_TXT.exists():
        print("ERROR: no-name predictions hash not recorded. Run generate first and hash.")
        sys.exit(2)
    if not NO_NAME_CSV.exists():
        print("ERROR: no-name predictions CSV not found.")
        sys.exit(2)
    if not reveal_csv.exists():
        print(f"ERROR: reveal csv not found: {reveal_csv}")
        sys.exit(2)

    print(f"Reading sealed no-name predictions: {NO_NAME_CSV}")
    with NO_NAME_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        preds = list(csv.DictReader(f))
    print(f"Reading reveal reference: {reveal_csv}")
    with reveal_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reveal_rows = list(csv.DictReader(f))
    reveal_by_z = {int(r["Z"]): r for r in reveal_rows}

    scored = []
    counts = {
        "N_match": 0, "A_match": 0, "clock_match": 0,
        "CLOCK_CLOSED_pred": 0, "CLOCK_HOLE_pred": 0,
        "RADIOACTIVE_OPEN_pred": 0, "FRONTIER_pred": 0,
    }
    for p in preds:
        Z = int(p["Z"])
        ref = reveal_by_z.get(Z, {})
        N_pred = int(p["N_pred"])
        A_pred = int(p["A_pred"])
        clock_pred = p["clock_state"]
        counts[f"{clock_pred}_pred"] += 1

        symbol = ref.get("symbol", "")
        name = ref.get("name", "")
        try:
            ext_A = int(ref["external_anchor_A"]) if ref.get("external_anchor_A") else None
        except ValueError:
            ext_A = None
        try:
            ext_N = int(ref["external_anchor_N"]) if ref.get("external_anchor_N") else None
        except ValueError:
            ext_N = None
        ext_stab = (ref.get("external_stability_label") or "").lower().strip()
        meas_mass = ref.get("measured_mass_u", "")

        N_match = ext_N is not None and ext_N == N_pred
        A_match = ext_A is not None and ext_A == A_pred

        if clock_pred == "CLOCK_CLOSED":
            pred_stab = "stable"
        elif clock_pred == "CLOCK_HOLE":
            pred_stab = "radioactive"
        elif clock_pred == "RADIOACTIVE_OPEN":
            pred_stab = "radioactive"
        elif clock_pred == "FRONTIER":
            pred_stab = "frontier"
        else:
            pred_stab = "unknown"
        clock_match = (pred_stab == ext_stab) or (
            pred_stab == "radioactive" and ext_stab in ("radioactive", "unstable", "synthetic")
        ) or (pred_stab == "frontier" and ext_stab in ("frontier", "predicted", ""))

        if N_match:
            counts["N_match"] += 1
        if A_match:
            counts["A_match"] += 1
        if clock_match:
            counts["clock_match"] += 1

        scored.append({
            "row_id": p["row_id"], "Z": Z, "N_pred": N_pred, "A_pred": A_pred,
            "clock_pred": clock_pred,
            "symbol": symbol, "name": name,
            "external_anchor_A": ext_A if ext_A is not None else "",
            "external_anchor_N": ext_N if ext_N is not None else "",
            "external_stability_label": ext_stab,
            "measured_mass_u": meas_mass,
            "N_match": N_match, "A_match": A_match, "clock_match": clock_match,
            "mass_reveal_only": "yes (not scored as derived)",
        })

    fields = ["row_id", "Z", "N_pred", "A_pred", "clock_pred",
              "symbol", "name", "external_anchor_A", "external_anchor_N",
              "external_stability_label", "measured_mass_u",
              "N_match", "A_match", "clock_match", "mass_reveal_only"]
    with REVEAL_SCORED.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in scored:
            writer.writerow(row)

    summary = {
        "rows_scored": len(scored),
        "N_match_count": counts["N_match"],
        "A_match_count": counts["A_match"],
        "clock_match_count": counts["clock_match"],
        "clock_closed_pred_count": counts["CLOCK_CLOSED_pred"],
        "clock_hole_pred_count": counts["CLOCK_HOLE_pred"],
        "radioactive_open_pred_count": counts["RADIOACTIVE_OPEN_pred"],
        "frontier_pred_count": counts["FRONTIER_pred"],
        "stable_clock_holes": [43, 61],
        "measured_mass_used_as_input": False,
        "measured_mass_scored_as_derived": False,
        "reveal_csv": str(reveal_csv),
        "reveal_csv_sha256": sha256_file(reveal_csv),
    }
    REVEAL_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    n_frac = summary["N_match_count"] / max(1, summary["rows_scored"])
    a_frac = summary["A_match_count"] / max(1, summary["rows_scored"])
    c_frac = summary["clock_match_count"] / max(1, summary["rows_scored"])
    if c_frac >= 0.95 and n_frac >= 0.95 and a_frac >= 0.95:
        verdict = "PASS_TEST5_REVEAL_STRONG_MATCH"
    elif c_frac >= 0.90:
        verdict = "PASS_TEST5_REVEAL_PARTIAL_MATCH"
    else:
        verdict = "FAIL_TEST5_REVEAL_WEAK_MATCH"

    lines = [
        "# Test 5 Reveal Verdict",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        f"- rows_scored: {summary['rows_scored']}",
        f"- clock_match: {summary['clock_match_count']} / {summary['rows_scored']} ({c_frac:.4f})",
        f"- N_match: {summary['N_match_count']} / {summary['rows_scored']} ({n_frac:.4f})",
        f"- A_match: {summary['A_match_count']} / {summary['rows_scored']} ({a_frac:.4f})",
        f"- clock_closed_predicted: {summary['clock_closed_pred_count']}",
        f"- clock_hole_predicted: {summary['clock_hole_pred_count']} (at Z={summary['stable_clock_holes']})",
        f"- radioactive_open_predicted: {summary['radioactive_open_pred_count']}",
        f"- frontier_predicted: {summary['frontier_pred_count']}",
        f"- reveal_csv: {summary['reveal_csv']}",
        f"- reveal_csv_sha256: {summary['reveal_csv_sha256']}",
        "",
        "Measured mass is reveal-only and was not used as a SAM input.",
    ]
    REVEAL_VERDICT.write_text("\n".join(lines), encoding="utf-8")

    h_scored = append_hash(REVEAL_SCORED)
    h_summary = append_hash(REVEAL_SUMMARY)
    h_verdict = append_hash(REVEAL_VERDICT)
    REVEAL_HASH_TXT.write_text(
        f"reveal_scored.csv  {h_scored}\nreveal_summary.json  {h_summary}\nreveal_verdict.md  {h_verdict}\n",
        encoding="utf-8",
    )
    print(f"Reveal verdict: {verdict}")
    print(f"  clock_match: {summary['clock_match_count']}/{summary['rows_scored']}")
    print(f"  N_match:     {summary['N_match_count']}/{summary['rows_scored']}")
    print(f"  A_match:     {summary['A_match_count']}/{summary['rows_scored']}")
    return verdict


# ---- GENERATE MODE ----

def generate_mode():
    print("=" * 72)
    print("TEST 5 - GENERATE MODE (blind)")
    print("=" * 72)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    CONTROLS.mkdir(parents=True, exist_ok=True)
    HASHES.mkdir(parents=True, exist_ok=True)

    rows, consts = generate_rows()
    write_predictions_csv(rows, NO_NAME_CSV)
    print(f"Wrote: {NO_NAME_CSV.relative_to(ROOT)}  ({len(rows)} rows)")

    checks = run_internal_checks(rows, consts)
    serializable_checks = {k: v for k, v in checks.items() if not k.startswith("_")}
    INTERNAL_CHECKS.write_text(json.dumps(serializable_checks, indent=2), encoding="utf-8")
    print(f"Wrote: {INTERNAL_CHECKS.relative_to(ROOT)}")

    verdict = write_internal_verdict(checks, consts, INTERNAL_VERDICT)
    print(f"Wrote: {INTERNAL_VERDICT.relative_to(ROOT)}  verdict={verdict}")

    print("\nAudit rows:")
    for rid in ["E001", "E043", "E061", "E079", "E083", "E084", "E118", "E119"]:
        r = next((x for x in rows if x["row_id"] == rid), None)
        if r:
            print(f"  {rid}: Z={r['Z']} N={r['N_pred']} A={r['A_pred']} "
                  f"u={r['u_count']} d={r['d_count']} e={r['e_count']} "
                  f"clock={r['clock_state']}")

    # Hash sealed outputs
    h_pred = append_hash(NO_NAME_CSV)
    h_chk = append_hash(INTERNAL_CHECKS)
    h_ver = append_hash(INTERNAL_VERDICT)
    NO_NAME_HASH_TXT.write_text(
        f"no_name_predictions.csv  {h_pred}\ninternal_checks.json  {h_chk}\ninternal_verdict.md  {h_ver}\n",
        encoding="utf-8",
    )
    print(f"\nSealed hashes:\n  predictions: {h_pred}\n  checks: {h_chk}\n  verdict: {h_ver}")

    # ---- Wrong controls (write after the real sealed outputs) ----
    print("\n[CONTROLS]")
    rA = run_wrong_control("R10", 10, D, ALPHA_H, CONTROLS / "R10_control.csv")
    rB = run_wrong_control("R11", 11, D, ALPHA_H, CONTROLS / "R11_control.csv")
    rC = run_wrong_control("R13", 13, D, ALPHA_H, CONTROLS / "R13_control.csv")
    rD = run_wrong_control("D2", R, 2, ALPHA_H, CONTROLS / "D2_control.csv")
    rE = run_wrong_control("D4", R, 4, ALPHA_H, CONTROLS / "D4_control.csv")
    for c in [rA, rB, rC, rD, rE]:
        print(f"  {c['control']}: rows={c['row_count']} (expected 126={c['row_count_matches_126']}) "
              f"broke={c['broke_as_predicted']}")

    # Control G (random clock holes) doesn't depend on reveal
    rG = run_random_clock_holes_control(20260621, CONTROLS / "random_clock_holes_control.csv")
    print(f"  random_clock_holes: new_holes={rG['new_holes']} broke={rG['broke_as_predicted']}")

    # Control F (shuffled Z) needs reveal CSV — produce placeholder until reveal reference is in hand
    # We'll let the operator re-run with --mode reveal-controls --reveal-csv to fill in.
    placeholder_path = CONTROLS / "shuffled_Z_control.csv"
    if not placeholder_path.exists():
        with placeholder_path.open("w", encoding="utf-8", newline="") as f:
            f.write("control,note\nshuffled_Z,run with reveal-controls mode after reveal csv is known\n")
    return verdict


def reveal_controls_mode(reveal_csv: Path):
    """Run reveal-dependent controls (F: shuffled Z) after reveal is sealed."""
    if not reveal_csv.exists():
        print(f"ERROR: reveal csv not found: {reveal_csv}")
        sys.exit(2)
    if not NO_NAME_CSV.exists():
        print("ERROR: no-name predictions CSV not found.")
        sys.exit(2)
    with NO_NAME_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = []
        for r in csv.DictReader(f):
            r["Z"] = int(r["Z"])
            r["N_pred"] = int(r["N_pred"])
            r["A_pred"] = int(r["A_pred"])
            rows.append(r)
    rF = run_shuffled_z_control(rows, 20260621, reveal_csv, CONTROLS / "shuffled_Z_control.csv")
    print(f"shuffled_Z control: clock_match={rF['shuffled_clock_match']} N_match={rF['shuffled_N_match_against_external']}")


def main(argv: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True,
                        choices=["generate", "reveal", "reveal-controls"])
    parser.add_argument("--reveal-csv", type=Path, default=None)
    args = parser.parse_args(argv)
    if args.mode == "generate":
        generate_mode()
    elif args.mode == "reveal":
        if args.reveal_csv is None:
            print("ERROR: --mode reveal requires --reveal-csv")
            sys.exit(2)
        reveal_mode(args.reveal_csv)
    elif args.mode == "reveal-controls":
        if args.reveal_csv is None:
            print("ERROR: --mode reveal-controls requires --reveal-csv")
            sys.exit(2)
        reveal_controls_mode(args.reveal_csv)


if __name__ == "__main__":
    main(sys.argv[1:])
