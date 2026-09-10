from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION"

CR119 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
CR119_PERIODIC = CR119 / "CR119_courtroom_periodic_table.csv"
CR119_MATTER = CR119 / "CR119_courtroom_matter_table.csv"
CR119_SUMMARY = CR119 / "CR119_summary.json"
ROW_ORDER_V1 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR219_PROMOTED_PARTICLE_ROWS_EXPORT" / "roworderv1.md"
CR218_RESULT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR218_HIDDEN_SOURCE_BIGRADE_DERIVATION" / "CR218_result.md"
CR211_RESULT = ROOT / "17_DISCOVERY_INTAKE" / "CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA" / "CR211_result.md"
HH001_BUILDER = ROOT / "17_DISCOVERY_INTAKE" / "CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA" / "source_copies" / "HH001_build_sis_table.py"

QP094A_SRC = Path("C:/VS/quantum_phase/src/qp094a_element_isotope_closure_generator.py")
QP094A_SUMMARY = Path("C:/VS/quantum_phase/artifacts/qp094a_element_isotope_closure_generator/qp094a_summary.json")
QP094A_COMPONENTS = Path("C:/VS/quantum_phase/artifacts/qp094a_element_isotope_closure_generator/qp094a_component_selector.csv")

PRECOMMIT = OUT / "CR220_PRECOMMIT.md"
RUNNER = OUT / "CR220_runner.py"
COMPONENTS_OUT = OUT / "CR220_component_selector.csv"
ELEMENT_ROWS_OUT = OUT / "CR220_simulated_element_primary_rows_126.csv"
ISOTOPE_ROWS_OUT = OUT / "CR220_simulated_isotope_ladder_rows_214.csv"
SELECTOR_SCORES_OUT = OUT / "CR220_selector_scores.csv"
THRESHOLD_SEARCH_OUT = OUT / "CR220_threshold_search.csv"
COUNT_THRESHOLD_CANDIDATES_OUT = OUT / "CR220_particle_count_threshold_candidates_83.csv"
INPUT_MANIFEST_OUT = OUT / "CR220_input_manifest.csv"
CHECKS_OUT = OUT / "CR220_checks.csv"
SUMMARY_OUT = OUT / "CR220_summary.json"
RESULT_OUT = OUT / "CR220_result.md"
HASHES_OUT = OUT / "HASHES.txt"

R = Decimal(12)
D = Decimal(3)
ALPHA_H = Decimal(2)
ONE = Decimal(1)
SEVEN = Decimal(7)
EIGHT = Decimal(8)
ZERO = Decimal(0)
SHELL_CAPACITIES = [2, 8, 18, 32, 32, 18, 8, 8]
ROW_ORDER_SKELETON = {1, 2, 3, 4, 6, 8, 9, 12}
REFERENCE_CLOCK_HOLES = {43, 61}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def dec(value: Any) -> Decimal:
    text = str(value).strip()
    if not text:
        return ZERO
    return Decimal(text)


def dstr(value: Decimal) -> str:
    return format(value, "f") if value == value.normalize() else str(value)


def bool_text(value: bool) -> str:
    return "yes" if value else "no"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append(
        {
            "check": name,
            "passed": str(bool(passed)),
            "observed": observed,
            "expected": expected,
        }
    )


def manifest_row(path: Path, role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "source": rel(path),
        "exists": str(exists),
        "bytes": path.stat().st_size if exists and path.is_file() else "",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
        "role": role,
    }


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists() and path.is_file():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def positive_decimal(row: dict[str, str], key: str) -> bool:
    return dec(row.get(key, "0")) > ZERO


def passes_matter_gate(row: dict[str, str]) -> bool:
    return (
        row.get("matter_row_allowed") == "yes"
        and row.get("bin") not in {
            "carrier_only_rows",
            "hidden_source_support_rows",
            "rejected_fake_closures",
            "antimatter_conjugate_rows",
        }
        and row.get("closure_status", "").startswith("CLOSED")
        and positive_decimal(row, "M_observed_candidate")
        and positive_decimal(row, "qA_source_support")
    )


def lightest(rows: list[dict[str, str]]) -> dict[str, str]:
    if not rows:
        raise RuntimeError("component selector returned no rows")
    return sorted(rows, key=lambda row: (dec(row["M_observed_candidate"]), row["candidate_id"]))[0]


def select_components(matter_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    gated = [row for row in matter_rows if passes_matter_gate(row)]
    proton_candidates = [
        row
        for row in gated
        if row["operator_class"] == "GROUND_BARYON_3BODY"
        and row["q_sign"] == "positive"
        and dec(row["q_abs"]) == ONE
    ]
    neutron_candidates = [row for row in gated if row["q_sign"] == "neutral"]
    electron_candidates = [
        row
        for row in gated
        if row["operator_class"] == "V4_1_SINGLE_WRITE"
        and row["q_sign"] == "negative"
        and dec(row["q_abs"]) == ONE
    ]
    return {
        "proton_write": lightest(proton_candidates),
        "neutron_write": lightest(neutron_candidates),
        "electron_write": lightest(electron_candidates),
    }


def component_output_rows(components: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    selectors = {
        "proton_write": "lightest positive q_abs=1 GROUND_BARYON_3BODY matter-gated row",
        "neutron_write": "lightest neutral matter-gated row",
        "electron_write": "lightest negative q_abs=1 V4_1_SINGLE_WRITE matter-gated row",
    }
    rows: list[dict[str, Any]] = []
    for role in ["proton_write", "neutron_write", "electron_write"]:
        source = components[role]
        rows.append(
            {
                "component_role": role,
                "source_candidate_id": source["candidate_id"],
                "selector": selectors[role],
                "route_combination": source["route_combination"],
                "operator_class": source["operator_class"],
                "q_sign": source["q_sign"],
                "q_abs": source["q_abs"],
                "M_native": source["M_native"],
                "M_observed_candidate": source["M_observed_candidate"],
                "qA_source_support": source["qA_source_support"],
                "tensor_carrier_support": source["tensor_carrier_support"],
                "retained_write_support": source["retained_write_support"],
                "construction_role": "SAM_NATIVE_COMPONENT_SELECTOR_FROM_CR119_MATTER_ROWS",
            }
        )
    return rows


def element_capacity() -> int:
    return int(R * R * (ONE - (ONE / (Decimal(2) ** int(D)))))


def native_z_coordinates(z: int) -> dict[str, int]:
    return {
        "radix_cycle": ((z - 1) // int(R)) + 1,
        "radix_slot": ((z - 1) % int(R)) + 1,
    }


def shell_state(z: int) -> dict[str, Any]:
    remaining = z
    for index, capacity in enumerate(SHELL_CAPACITIES, start=1):
        if remaining <= capacity:
            return {
                "shell_period": index,
                "shell_capacity": capacity,
                "shell_occupancy": remaining,
                "shell_status": "CLOSED_SHELL" if remaining == capacity else "OPEN_SHELL",
                "electron_shell_status": "FILLED_ELECTRON_SHELL_CLOSURE"
                if remaining == capacity
                else "PARTIAL_ELECTRON_SHELL_CLOSURE",
            }
        remaining -= capacity
    return {
        "shell_period": len(SHELL_CAPACITIES) + 1,
        "shell_capacity": 0,
        "shell_occupancy": remaining,
        "shell_status": "OVER_CAPACITY",
        "electron_shell_status": "REJECT_OVER_NATIVE_ELEMENT_CAPACITY",
    }


def isotope_ladder(z: int) -> list[dict[str, Any]]:
    coords = native_z_coordinates(z)
    selected_depth = max(0, coords["radix_cycle"] - 1)
    raw_packets = Decimal(z) * Decimal(selected_depth) / R
    delta_n = int(raw_packets)
    residual = raw_packets - Decimal(delta_n)
    residual_twelfths = int((residual * R).to_integral_value())
    primary_n = z + delta_n
    rows = [
        {
            "ladder_role": "FLOOR_PRIMARY",
            "ladder_weight": dstr((R - Decimal(residual_twelfths)) / R) if residual_twelfths else "1",
            "N": primary_n,
            "residual_twelfths": residual_twelfths,
            "selected_depth_index": selected_depth,
        }
    ]
    if residual_twelfths:
        rows.append(
            {
                "ladder_role": "CEIL_NEIGHBOR",
                "ladder_weight": dstr(Decimal(residual_twelfths) / R),
                "N": primary_n + 1,
                "residual_twelfths": residual_twelfths,
                "selected_depth_index": selected_depth,
            }
        )
    return rows


def isotope_status(z: int, residual_twelfths: int, ladder_role: str) -> str:
    if z > 118:
        return "UNKNOWN_FRONTIER_ISOTOPE_CLOSURE_CANDIDATE"
    if z > 96:
        return "KNOWN_SURFACE_FRONTIER_BOUNDARY_DOWNSTREAM"
    if residual_twelfths == 0 and ladder_role == "FLOOR_PRIMARY":
        return "STABLE_ANCHOR_ISOTOPE_CLOSURE"
    if residual_twelfths == 6:
        return "HALF_WRITE_BOUND_ISOTOPE_CLOSURE"
    return "BOUND_ISOTOPE_LADDER_CLOSURE"


def natural_boundary_status(z: int) -> str:
    if z > 118:
        return "SAM_FRONTIER_UNKNOWN_Z119_Z126"
    if z > 96:
        return "KNOWN_SYNTHETIC_FRONTIER_DOWNSTREAM"
    if z in REFERENCE_CLOCK_HOLES:
        return "KNOWN_LONG_LIVED_HOLE_DOWNSTREAM"
    if z <= 82:
        return "KNOWN_NATURAL_SURFACE_DOWNSTREAM"
    return "KNOWN_RADIOACTIVE_HEAVY_SURFACE_DOWNSTREAM"


def reference_clock(z: int) -> str:
    if z in REFERENCE_CLOCK_HOLES:
        return "radioactive"
    if z >= 84 and z <= 118:
        return "radioactive"
    if 1 <= z <= 118:
        return "stable"
    return "frontier"


def dec_close(left: Any, right: Any, tolerance: Decimal = Decimal("1e-70")) -> bool:
    return abs(dec(left) - dec(right)) <= tolerance


def score_selector(
    rows: list[dict[str, Any]],
    selector_id: str,
    column: str,
    description: str,
    input_class: str,
) -> dict[str, Any]:
    scored = [row for row in rows if row["reference_clock"] != "frontier"]
    predicted_all = [row for row in rows if row[column] == "yes"]
    predicted_scored = [row for row in scored if row[column] == "yes"]
    tp = sum(1 for row in scored if row[column] == "yes" and row["reference_clock"] == "stable")
    fp = sum(1 for row in scored if row[column] == "yes" and row["reference_clock"] == "radioactive")
    fn = sum(1 for row in scored if row[column] == "no" and row["reference_clock"] == "stable")
    tn = sum(1 for row in scored if row[column] == "no" and row["reference_clock"] == "radioactive")
    precision = Decimal(tp) / Decimal(tp + fp) if (tp + fp) else ZERO
    recall = Decimal(tp) / Decimal(tp + fn) if (tp + fn) else ZERO
    accuracy = Decimal(tp + tn) / Decimal(len(scored)) if scored else ZERO
    false_positive_z = ";".join(str(row["Z"]) for row in scored if row[column] == "yes" and row["reference_clock"] == "radioactive")
    false_negative_z = ";".join(str(row["Z"]) for row in scored if row[column] == "no" and row["reference_clock"] == "stable")
    return {
        "selector_id": selector_id,
        "selector_column": column,
        "description": description,
        "input_class": input_class,
        "predicted_stable_count_all_126": len(predicted_all),
        "predicted_stable_count_known_118": len(predicted_scored),
        "scored_rows": len(scored),
        "reference_target": "HH001_CLOCK_stable_vs_radioactive_Z001_Z118",
        "true_positive_stable": tp,
        "false_positive_radioactive": fp,
        "false_negative_stable": fn,
        "true_negative_radioactive": tn,
        "accuracy": f"{accuracy:.6f}",
        "precision": f"{precision:.6f}",
        "recall": f"{recall:.6f}",
        "false_positive_Z": false_positive_z,
        "false_negative_Z": false_negative_z,
        "boundary_note": "CLOCK is a reference comparator, not a construction input",
    }


def threshold_search(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    features = [
        ("Z", "Z"),
        ("N_primary", "N"),
        ("A_primary", "A"),
        ("total_particle_count", "total_particle_count"),
        ("radix_cycle", "radix_cycle"),
        ("radix_slot", "radix_slot"),
        ("shell_period", "shell_period"),
        ("shell_occupancy", "shell_occupancy"),
        ("selected_depth_index", "selected_depth_index"),
        ("residual_twelfths", "residual_twelfths"),
        ("GR_qA_total_computed", "GR_qA_total_computed"),
        ("G_tensor_computed", "G_tensor_computed"),
    ]
    scored = [row for row in rows if row["reference_clock"] != "frontier"]
    out: list[dict[str, Any]] = []
    for feature_id, key in features:
        values = sorted({dec(row[key]) for row in scored})
        best: dict[str, Any] | None = None
        for value in values:
            tp = fp = fn = tn = 0
            predicted_all = 0
            for row in rows:
                predicted = dec(row[key]) <= value
                if predicted:
                    predicted_all += 1
                if row["reference_clock"] == "frontier":
                    continue
                target_stable = row["reference_clock"] == "stable"
                if predicted and target_stable:
                    tp += 1
                elif predicted and not target_stable:
                    fp += 1
                elif not predicted and target_stable:
                    fn += 1
                else:
                    tn += 1
            accuracy = Decimal(tp + tn) / Decimal(len(scored))
            precision = Decimal(tp) / Decimal(tp + fp) if (tp + fp) else ZERO
            recall = Decimal(tp) / Decimal(tp + fn) if (tp + fn) else ZERO
            row_out = {
                "feature": feature_id,
                "operator": "<=",
                "threshold": dstr(value),
                "predicted_stable_count_all_126": predicted_all,
                "predicted_stable_count_known_118": tp + fp,
                "true_positive_stable": tp,
                "false_positive_radioactive": fp,
                "false_negative_stable": fn,
                "true_negative_radioactive": tn,
                "accuracy": f"{accuracy:.6f}",
                "precision": f"{precision:.6f}",
                "recall": f"{recall:.6f}",
                "reference_target": "HH001_CLOCK_stable_vs_radioactive_Z001_Z118",
                "boundary_note": "single-feature threshold search; target labels used for scoring only",
            }
            if best is None:
                best = row_out
            else:
                old_key = (Decimal(str(best["accuracy"])), Decimal(str(best["precision"])), Decimal(str(best["recall"])), -abs(int(best["predicted_stable_count_known_118"]) - 81))
                new_key = (accuracy, precision, recall, -abs((tp + fp) - 81))
                if new_key > old_key:
                    best = row_out
        if best is not None:
            out.append(best)
    return sorted(
        out,
        key=lambda row: (
            Decimal(str(row["accuracy"])),
            Decimal(str(row["precision"])),
            Decimal(str(row["recall"])),
            -abs(int(row["predicted_stable_count_known_118"]) - 81),
        ),
        reverse=True,
    )


def build_simulation(
    periodic_rows: list[dict[str, str]],
    components: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_z = {int(row["Z"]): row for row in periodic_rows}
    cap = element_capacity()
    proton = components["proton_write"]
    neutron = components["neutron_write"]
    electron = components["electron_write"]

    proton_qA = dec(proton["qA_source_support"])
    neutron_qA = dec(neutron["qA_source_support"])
    electron_qA = dec(electron["qA_source_support"])
    proton_native = dec(proton["M_native"])
    neutron_native = dec(neutron["M_native"])
    electron_native = dec(electron["M_native"])
    proton_obs = dec(proton["M_observed_candidate"])
    neutron_obs = dec(neutron["M_observed_candidate"])
    electron_obs = dec(electron["M_observed_candidate"])

    element_rows: list[dict[str, Any]] = []
    isotope_rows: list[dict[str, Any]] = []

    for z in range(1, cap + 1):
        coords = native_z_coordinates(z)
        shell = shell_state(z)
        ladder_rows = isotope_ladder(z)
        primary = ladder_rows[0]
        n_primary = int(primary["N"])
        a_primary = z + n_primary
        source_row = by_z[z]
        natural_status = natural_boundary_status(z)
        ref_clock = reference_clock(z)

        for item in ladder_rows:
            n = int(item["N"])
            a = z + n
            gr = Decimal(z) * (proton_qA + electron_qA) + Decimal(n) * neutron_qA
            m_native = Decimal(z) * (proton_native + electron_native) + Decimal(n) * neutron_native
            m_observed = Decimal(z) * (proton_obs + electron_obs) + Decimal(n) * neutron_obs
            status = isotope_status(z, int(item["residual_twelfths"]), str(item["ladder_role"]))
            isotope_rows.append(
                {
                    "isotope_closure_id": f"CR220-IZ{z:03d}N{n:03d}-{item['ladder_role']}",
                    "element_closure_id": f"CR220-EZ{z:03d}",
                    "Z": z,
                    "N": n,
                    "A": a,
                    "proton_count": z,
                    "neutron_count": n,
                    "electron_count": z,
                    "total_particle_count": (2 * z) + n,
                    "quark_u_count": (2 * z) + n,
                    "quark_d_count": z + (2 * n),
                    "quark_e_count": z,
                    "P_address": f"{z}p+{n}n+{z}e",
                    "quark_address": f"{(2 * z) + n}u+{z + (2 * n)}d+{z}e",
                    "radix_cycle": coords["radix_cycle"],
                    "radix_slot": coords["radix_slot"],
                    "shell_period": shell["shell_period"],
                    "shell_capacity": shell["shell_capacity"],
                    "shell_occupancy": shell["shell_occupancy"],
                    "shell_status": shell["shell_status"],
                    "ladder_role": item["ladder_role"],
                    "ladder_weight": item["ladder_weight"],
                    "selected_depth_index": item["selected_depth_index"],
                    "residual_twelfths": item["residual_twelfths"],
                    "native_isotope_status": status,
                    "M_native_total_computed": dstr(m_native),
                    "M_observed_total_computed": dstr(m_observed),
                    "GR_qA_total_computed": dstr(gr),
                    "G_tensor_computed": dstr(gr / EIGHT),
                    "retained_7G_computed": dstr(gr * SEVEN / EIGHT),
                    "natural_synthetic_boundary_status": natural_status,
                    "reference_clock": ref_clock,
                }
            )

        gr_primary = Decimal(z) * (proton_qA + electron_qA) + Decimal(n_primary) * neutron_qA
        g_primary = gr_primary / EIGHT
        retained_primary = gr_primary * SEVEN / EIGHT
        native_status = isotope_status(z, int(primary["residual_twelfths"]), str(primary["ladder_role"]))
        stable_anchor = native_status == "STABLE_ANCHOR_ISOTOPE_CLOSURE"
        anchor_or_half = native_status in {"STABLE_ANCHOR_ISOTOPE_CLOSURE", "HALF_WRITE_BOUND_ISOTOPE_CLOSURE"}
        closed_shell = shell["shell_status"] == "CLOSED_SHELL"
        skeleton_slot = coords["radix_slot"] in ROW_ORDER_SKELETON
        z_le_83 = z <= 83
        z_le_83_without_reference_holes = z <= 83 and z not in REFERENCE_CLOCK_HOLES
        natural_surface = natural_status == "KNOWN_NATURAL_SURFACE_DOWNSTREAM"
        element_rows.append(
            {
                "element_closure_id": f"CR220-EZ{z:03d}",
                "CR119_element_closure_id": source_row["element_closure_id"],
                "Z": z,
                "N": n_primary,
                "A": a_primary,
                "proton_count": z,
                "neutron_count_primary": n_primary,
                "electron_count": z,
                "total_particle_count": (2 * z) + n_primary,
                "quark_u_count": (2 * z) + n_primary,
                "quark_d_count": z + (2 * n_primary),
                "quark_e_count": z,
                "P_address": f"{z}p+{n_primary}n+{z}e",
                "quark_address": f"{(2 * z) + n_primary}u+{z + (2 * n_primary)}d+{z}e",
                "native_element_capacity": cap,
                "radix_cycle": coords["radix_cycle"],
                "radix_slot": coords["radix_slot"],
                "shell_period": shell["shell_period"],
                "shell_capacity": shell["shell_capacity"],
                "shell_occupancy": shell["shell_occupancy"],
                "shell_status": shell["shell_status"],
                "selected_depth_index": primary["selected_depth_index"],
                "residual_twelfths": primary["residual_twelfths"],
                "primary_ladder_role": primary["ladder_role"],
                "native_primary_isotope_status": native_status,
                "GR_qA_total_computed": dstr(gr_primary),
                "G_tensor_computed": dstr(g_primary),
                "retained_7G_computed": dstr(retained_primary),
                "CR119_qA_total_primary": source_row["qA_total_primary"],
                "CR119_tensor_carrier_support_primary": source_row["tensor_carrier_support_primary"],
                "CR119_retained_write_support_primary": source_row["retained_write_support_primary"],
                "GR_matches_CR119_qA": bool_text(dec_close(gr_primary, source_row["qA_total_primary"])),
                "G_matches_CR119_tensor": bool_text(dec_close(g_primary, source_row["tensor_carrier_support_primary"])),
                "retained_matches_CR119": bool_text(dec_close(retained_primary, source_row["retained_write_support_primary"])),
                "natural_synthetic_boundary_status": natural_status,
                "CR119_natural_synthetic_boundary_status": source_row["natural_synthetic_boundary_status"],
                "reference_clock": ref_clock,
                "known_symbol_downstream": source_row.get("known_symbol", ""),
                "known_name_downstream": source_row.get("known_name", ""),
                "known_label_used_as_construction_input": source_row.get("known_label_used_as_construction_input", "no"),
                "selector_all_native_126": "yes",
                "selector_known_z_118": bool_text(z <= 118),
                "selector_z_le_83_count_threshold": bool_text(z_le_83),
                "selector_z_le_83_reference_holes_removed": bool_text(z_le_83_without_reference_holes),
                "selector_qp094a_stable_anchor": bool_text(stable_anchor),
                "selector_qp094a_anchor_or_half": bool_text(anchor_or_half),
                "selector_closed_shell": bool_text(closed_shell),
                "selector_roworder_skeleton_slot": bool_text(skeleton_slot),
                "selector_roworder_skeleton_or_closed_shell": bool_text(skeleton_slot or closed_shell),
                "selector_roworder_skeleton_and_z_le_83": bool_text(skeleton_slot and z_le_83),
                "selector_downstream_natural_surface": bool_text(natural_surface),
                "construction_note": "P-centered simulation row; CLOCK and known labels are scoring/reference only",
            }
        )

    return element_rows, isotope_rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    source_paths = [
        (CR119_PERIODIC, "locked_126_native_element_family_surface"),
        (CR119_MATTER, "locked_126_matter_rows_for_component_selection"),
        (CR119_SUMMARY, "CR119 result summary"),
        (ROW_ORDER_V1, "row-order skeleton note"),
        (CR218_RESULT, "hidden-source bigrade derivation"),
        (CR211_RESULT, "HH001 verification and reference-column boundary"),
        (HH001_BUILDER, "HH001 reference CLOCK rule source copy"),
        (QP094A_SRC, "QP094A generator source for formulas"),
        (QP094A_SUMMARY, "QP094A summary constants and counts"),
        (QP094A_COMPONENTS, "QP094A component selector comparator"),
    ]
    write_csv(
        INPUT_MANIFEST_OUT,
        [manifest_row(path, role) for path, role in source_paths],
        ["source", "exists", "bytes", "sha256", "role"],
    )

    _, periodic_rows = read_csv(CR119_PERIODIC)
    _, matter_rows = read_csv(CR119_MATTER)
    qp094a_summary = read_json(QP094A_SUMMARY) if QP094A_SUMMARY.exists() else {}
    components = select_components(matter_rows)
    component_rows = component_output_rows(components)
    write_csv(
        COMPONENTS_OUT,
        component_rows,
        [
            "component_role",
            "source_candidate_id",
            "selector",
            "route_combination",
            "operator_class",
            "q_sign",
            "q_abs",
            "M_native",
            "M_observed_candidate",
            "qA_source_support",
            "tensor_carrier_support",
            "retained_write_support",
            "construction_role",
        ],
    )

    element_rows, isotope_rows = build_simulation(periodic_rows, components)
    element_fields = [
        "element_closure_id",
        "CR119_element_closure_id",
        "Z",
        "N",
        "A",
        "proton_count",
        "neutron_count_primary",
        "electron_count",
        "total_particle_count",
        "quark_u_count",
        "quark_d_count",
        "quark_e_count",
        "P_address",
        "quark_address",
        "native_element_capacity",
        "radix_cycle",
        "radix_slot",
        "shell_period",
        "shell_capacity",
        "shell_occupancy",
        "shell_status",
        "selected_depth_index",
        "residual_twelfths",
        "primary_ladder_role",
        "native_primary_isotope_status",
        "GR_qA_total_computed",
        "G_tensor_computed",
        "retained_7G_computed",
        "CR119_qA_total_primary",
        "CR119_tensor_carrier_support_primary",
        "CR119_retained_write_support_primary",
        "GR_matches_CR119_qA",
        "G_matches_CR119_tensor",
        "retained_matches_CR119",
        "natural_synthetic_boundary_status",
        "CR119_natural_synthetic_boundary_status",
        "reference_clock",
        "known_symbol_downstream",
        "known_name_downstream",
        "known_label_used_as_construction_input",
        "selector_all_native_126",
        "selector_known_z_118",
        "selector_z_le_83_count_threshold",
        "selector_z_le_83_reference_holes_removed",
        "selector_qp094a_stable_anchor",
        "selector_qp094a_anchor_or_half",
        "selector_closed_shell",
        "selector_roworder_skeleton_slot",
        "selector_roworder_skeleton_or_closed_shell",
        "selector_roworder_skeleton_and_z_le_83",
        "selector_downstream_natural_surface",
        "construction_note",
    ]
    isotope_fields = [
        "isotope_closure_id",
        "element_closure_id",
        "Z",
        "N",
        "A",
        "proton_count",
        "neutron_count",
        "electron_count",
        "total_particle_count",
        "quark_u_count",
        "quark_d_count",
        "quark_e_count",
        "P_address",
        "quark_address",
        "radix_cycle",
        "radix_slot",
        "shell_period",
        "shell_capacity",
        "shell_occupancy",
        "shell_status",
        "ladder_role",
        "ladder_weight",
        "selected_depth_index",
        "residual_twelfths",
        "native_isotope_status",
        "M_native_total_computed",
        "M_observed_total_computed",
        "GR_qA_total_computed",
        "G_tensor_computed",
        "retained_7G_computed",
        "natural_synthetic_boundary_status",
        "reference_clock",
    ]
    write_csv(ELEMENT_ROWS_OUT, element_rows, element_fields)
    write_csv(ISOTOPE_ROWS_OUT, isotope_rows, isotope_fields)

    selector_specs = [
        (
            "S0_ALL_NATIVE_ELEMENT_FAMILY",
            "selector_all_native_126",
            "All 126 rows generated by native element-family capacity",
            "SAM_NATIVE_CAPACITY_AND_CLOSURE",
        ),
        (
            "S1_KNOWN_Z_118_BOUNDARY",
            "selector_known_z_118",
            "Known-Z boundary, included as a non-native downstream comparison",
            "DOWNSTREAM_BOUNDARY_COMPARATOR",
        ),
        (
            "S2_Z_LE_83_COUNT_THRESHOLD",
            "selector_z_le_83_count_threshold",
            "Particle-count threshold: Z/proton/electron count <= 83",
            "COUNT_ONLY_THRESHOLD_SEARCH",
        ),
        (
            "S3_Z_LE_83_WITH_REFERENCE_HOLES_REMOVED",
            "selector_z_le_83_reference_holes_removed",
            "Z <= 83 with Tc/Pm holes removed; perfect comparator but reference-patched",
            "REFERENCE_PATCHED_NOT_SAM_NATIVE",
        ),
        (
            "S4_QP094A_STABLE_ANCHOR",
            "selector_qp094a_stable_anchor",
            "QP094A residual-twelfths stable anchor lane",
            "SAM_NATIVE_ISOTOPE_LADDER_SELECTOR",
        ),
        (
            "S5_QP094A_ANCHOR_OR_HALF",
            "selector_qp094a_anchor_or_half",
            "QP094A stable anchor plus half-write bound lane",
            "SAM_NATIVE_ISOTOPE_LADDER_SELECTOR",
        ),
        (
            "S6_CLOSED_SHELL",
            "selector_closed_shell",
            "Closed electron shell only",
            "SAM_NATIVE_SHELL_SELECTOR",
        ),
        (
            "S7_ROWORDER_SKELETON_SLOT",
            "selector_roworder_skeleton_slot",
            "Radix slot in roworder skeleton {1,2,3,4,6,8,9,12}",
            "SAM_NATIVE_ROWORDER_SELECTOR",
        ),
        (
            "S8_ROWORDER_SKELETON_OR_CLOSED_SHELL",
            "selector_roworder_skeleton_or_closed_shell",
            "Roworder skeleton slot or closed shell",
            "SAM_NATIVE_ROWORDER_AND_SHELL_SELECTOR",
        ),
        (
            "S9_ROWORDER_SKELETON_AND_Z_LE_83",
            "selector_roworder_skeleton_and_z_le_83",
            "Roworder skeleton inside the Z<=83 count threshold",
            "MIXED_NATIVE_AND_COUNT_THRESHOLD",
        ),
        (
            "S10_DOWNSTREAM_NATURAL_SURFACE",
            "selector_downstream_natural_surface",
            "CR119 natural-surface downstream status",
            "DOWNSTREAM_STATUS_COMPARATOR",
        ),
    ]
    selector_scores = [
        score_selector(element_rows, selector_id, column, description, input_class)
        for selector_id, column, description, input_class in selector_specs
    ]
    selector_fields = [
        "selector_id",
        "selector_column",
        "description",
        "input_class",
        "predicted_stable_count_all_126",
        "predicted_stable_count_known_118",
        "scored_rows",
        "reference_target",
        "true_positive_stable",
        "false_positive_radioactive",
        "false_negative_stable",
        "true_negative_radioactive",
        "accuracy",
        "precision",
        "recall",
        "false_positive_Z",
        "false_negative_Z",
        "boundary_note",
    ]
    write_csv(SELECTOR_SCORES_OUT, selector_scores, selector_fields)

    thresholds = threshold_search(element_rows)
    threshold_fields = [
        "feature",
        "operator",
        "threshold",
        "predicted_stable_count_all_126",
        "predicted_stable_count_known_118",
        "true_positive_stable",
        "false_positive_radioactive",
        "false_negative_stable",
        "true_negative_radioactive",
        "accuracy",
        "precision",
        "recall",
        "reference_target",
        "boundary_note",
    ]
    write_csv(THRESHOLD_SEARCH_OUT, thresholds, threshold_fields)

    count_candidates = [row for row in element_rows if row["selector_z_le_83_count_threshold"] == "yes"]
    write_csv(COUNT_THRESHOLD_CANDIDATES_OUT, count_candidates, element_fields)

    counts = {
        "element_rows": len(element_rows),
        "isotope_rows": len(isotope_rows),
        "reference_clock": dict(Counter(row["reference_clock"] for row in element_rows)),
        "native_primary_isotope_status": dict(Counter(row["native_primary_isotope_status"] for row in element_rows)),
        "shell_status": dict(Counter(row["shell_status"] for row in element_rows)),
        "natural_synthetic_boundary_status": dict(Counter(row["natural_synthetic_boundary_status"] for row in element_rows)),
    }
    selector_counts = {
        spec[0]: sum(1 for row in element_rows if row[spec[1]] == "yes")
        for spec in selector_specs
    }
    best_threshold = thresholds[0] if thresholds else {}
    z_threshold_score = next((row for row in thresholds if row["feature"] == "Z"), {})

    checks: list[dict[str, Any]] = []
    manifest_rows = [manifest_row(path, role) for path, role in source_paths]
    check(checks, "all_required_inputs_exist", all(row["exists"] == "True" for row in manifest_rows[:9]), [row for row in manifest_rows if row["exists"] != "True"], "first 9 required inputs exist")
    check(checks, "cr119_periodic_rows_126", len(periodic_rows) == 126, len(periodic_rows), 126)
    check(checks, "cr119_matter_rows_126", len(matter_rows) == 126, len(matter_rows), 126)
    check(checks, "native_capacity_126", element_capacity() == 126, element_capacity(), 126)
    check(checks, "qp094a_summary_capacity_126", str(qp094a_summary.get("native_element_capacity", "")) == "126", qp094a_summary.get("native_element_capacity", ""), 126)
    check(checks, "component_proton_qp093a_0115", components["proton_write"]["candidate_id"] == "QP093A-0115", components["proton_write"]["candidate_id"], "QP093A-0115")
    check(checks, "component_neutron_qp093a_0003", components["neutron_write"]["candidate_id"] == "QP093A-0003", components["neutron_write"]["candidate_id"], "QP093A-0003")
    check(checks, "component_electron_qp093a_0002", components["electron_write"]["candidate_id"] == "QP093A-0002", components["electron_write"]["candidate_id"], "QP093A-0002")
    check(checks, "simulated_primary_rows_126", len(element_rows) == 126, len(element_rows), 126)
    check(checks, "simulated_isotope_rows_214", len(isotope_rows) == 214, len(isotope_rows), 214)
    check(checks, "all_GR_match_CR119_qA", all(row["GR_matches_CR119_qA"] == "yes" for row in element_rows), sum(row["GR_matches_CR119_qA"] == "yes" for row in element_rows), 126)
    check(checks, "all_G_match_CR119_tensor", all(row["G_matches_CR119_tensor"] == "yes" for row in element_rows), sum(row["G_matches_CR119_tensor"] == "yes" for row in element_rows), 126)
    check(checks, "all_retained_match_CR119", all(row["retained_matches_CR119"] == "yes" for row in element_rows), sum(row["retained_matches_CR119"] == "yes" for row in element_rows), 126)
    check(checks, "closed_shell_rows_8", counts["shell_status"].get("CLOSED_SHELL", 0) == 8, counts["shell_status"].get("CLOSED_SHELL", 0), 8)
    check(checks, "reference_clock_counts_81_37_8", counts["reference_clock"] == {"stable": 81, "radioactive": 37, "frontier": 8}, counts["reference_clock"], {"stable": 81, "radioactive": 37, "frontier": 8})
    check(checks, "z_le_83_count_threshold_candidates_83", selector_counts["S2_Z_LE_83_COUNT_THRESHOLD"] == 83, selector_counts["S2_Z_LE_83_COUNT_THRESHOLD"], 83)
    s2 = next(row for row in selector_scores if row["selector_id"] == "S2_Z_LE_83_COUNT_THRESHOLD")
    check(checks, "z_le_83_false_positive_holes_43_61", s2["false_positive_Z"] == "43;61", s2["false_positive_Z"], "43;61")
    s3 = next(row for row in selector_scores if row["selector_id"] == "S3_Z_LE_83_WITH_REFERENCE_HOLES_REMOVED")
    check(checks, "reference_patched_81_perfect", s3["accuracy"] == "1.000000" and s3["predicted_stable_count_known_118"] == 81, {"accuracy": s3["accuracy"], "count": s3["predicted_stable_count_known_118"]}, "accuracy=1.000000,count=81")
    check(checks, "known_labels_not_construction_inputs", all(row["known_label_used_as_construction_input"] in {"no", ""} for row in element_rows), dict(Counter(row["known_label_used_as_construction_input"] for row in element_rows)), "all no/blank")

    write_csv(CHECKS_OUT, checks, ["check", "passed", "observed", "expected"])
    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"

    summary = {
        "cr_id": "CR220",
        "artifact": "CR220_PARTICLE_COUNT_STABILITY_SIMULATION",
        "execution_status": execution_status,
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "result_class": (
            "CR220_PASS_PARTICLE_COUNT_STABILITY_SIMULATION__126_NATIVE_ELEMENT_FAMILIES__"
            "P_TO_G_AND_GR_REPRODUCES_CR119__Z_LE_83_PRODUCES_83_WITH_43_61_HOLES__"
            "REFERENCE_PATCH_PRODUCES_81__SAM_CLOCK_SELECTOR_REMAINS_OPEN"
        )
        if execution_status == "CLEAN"
        else "CR220_FAIL_PARTICLE_COUNT_STABILITY_SIMULATION",
        "constants": {
            "R": str(R),
            "D": str(D),
            "alpha_H": str(ALPHA_H),
            "native_element_capacity_law": "R^2*(1-2^-D)",
            "native_element_capacity": element_capacity(),
            "shell_capacities": SHELL_CAPACITIES,
            "roworder_skeleton": sorted(ROW_ORDER_SKELETON),
        },
        "component_selector": {
            role: row["candidate_id"] for role, row in components.items()
        },
        "counts": counts,
        "selector_counts": selector_counts,
        "best_threshold": best_threshold,
        "z_threshold_score": z_threshold_score,
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": (
            "The run produces 126 native element-family rows and reproduces CR119 GR/G values "
            "from P-centered particle counts. HH001 CLOCK is only a comparator. The exact 81-row "
            "stable physical clock match requires removing Z=43 and Z=61 as reference holes, so "
            "the SAM-native isotope stability selector remains open."
        ),
        "outputs": {
            "component_selector": rel(COMPONENTS_OUT),
            "element_rows": rel(ELEMENT_ROWS_OUT),
            "isotope_rows": rel(ISOTOPE_ROWS_OUT),
            "selector_scores": rel(SELECTOR_SCORES_OUT),
            "threshold_search": rel(THRESHOLD_SEARCH_OUT),
            "count_threshold_candidates": rel(COUNT_THRESHOLD_CANDIDATES_OUT),
            "checks": rel(CHECKS_OUT),
            "summary": rel(SUMMARY_OUT),
            "result": rel(RESULT_OUT),
        },
    }
    write_json(SUMMARY_OUT, summary)

    s4 = next(row for row in selector_scores if row["selector_id"] == "S4_QP094A_STABLE_ANCHOR")
    s7 = next(row for row in selector_scores if row["selector_id"] == "S7_ROWORDER_SKELETON_SLOT")
    s8 = next(row for row in selector_scores if row["selector_id"] == "S8_ROWORDER_SKELETON_OR_CLOSED_SHELL")
    result_text = f"""# CR220 Particle Count Stability Simulation

Result: **{summary['result_class']}**

## Direct Answer

The simulation produced the full **126-row native element-family surface** from
particle counts centered on `P -> G(P) -> GR(P)`.

For every generated primary row:

```text
P = Zp + Nn + Ze
quark address = (2Z+N)u + (Z+2N)d + Ze
GR(P) = Z*(proton_qA + electron_qA) + N*neutron_qA
G(P) = GR(P) / 8
retained = 7G(P)
```

The computed values match CR119 row-by-row:

- `GR(P)` matches `qA_total_primary`: 126/126
- `G(P)` matches `tensor_carrier_support_primary`: 126/126
- `7G(P)` matches `retained_write_support_primary`: 126/126

## What Stable Counts Produced

The run separates native production from reference CLOCK scoring:

- Native element-family closure produces **126/126** rows.
- HH001 reference CLOCK has **81 stable**, **37 radioactive**, and **8 frontier**
  rows.
- The best simple count threshold is **`Z <= 83`**, which produces **83**
  stable candidates. It matches all 81 reference-stable rows but also includes
  two reference-radioactive holes: `Z=43` and `Z=61`.
- Removing `Z=43` and `Z=61` produces exactly **81** and scores perfectly, but
  that is a **reference-patched** selector, not yet a SAM-native derivation.

## Native Selector Readout

- QP094A residual stable-anchor selector produced
  **{s4['predicted_stable_count_all_126']}** candidates.
- Roworder skeleton radix-slot selector produced
  **{s7['predicted_stable_count_all_126']}** candidates.
- Roworder skeleton-or-closed-shell selector produced
  **{s8['predicted_stable_count_all_126']}** candidates.
- Closed shell alone produced **{selector_counts['S6_CLOSED_SHELL']}** candidates.

These are real native structure selectors, but none is the completed physical
CLOCK/stability selector by itself.

## Interpretation

The cards are not needed for the engine. This run shows the engine layer:

```text
particle counts -> P address -> G/GR support -> 126 native element families
```

The strongest physical-stability clue from particle counts is the **83-count
threshold with two holes**. That gives a sharp next target: derive the `43/61`
holes natively, or show why they remain downstream exceptions.

## Boundary

This CR does **not** claim that SAM constants alone have derived the known
physical stable-isotope table. It shows that the P-centered count engine
reproduces the 126 element-family surface and that a simple count threshold gets
to 83 with exactly two reference holes before the 81-row CLOCK surface appears.

## Artifacts

- `{rel(COMPONENTS_OUT)}`
- `{rel(ELEMENT_ROWS_OUT)}`
- `{rel(ISOTOPE_ROWS_OUT)}`
- `{rel(SELECTOR_SCORES_OUT)}`
- `{rel(THRESHOLD_SEARCH_OUT)}`
- `{rel(COUNT_THRESHOLD_CANDIDATES_OUT)}`
- `{rel(INPUT_MANIFEST_OUT)}`
- `{rel(CHECKS_OUT)}`
- `{rel(SUMMARY_OUT)}`
- `{rel(HASHES_OUT)}`
"""
    RESULT_OUT.write_text(result_text, encoding="utf-8")

    write_hashes(
        [
            PRECOMMIT,
            RUNNER,
            COMPONENTS_OUT,
            ELEMENT_ROWS_OUT,
            ISOTOPE_ROWS_OUT,
            SELECTOR_SCORES_OUT,
            THRESHOLD_SEARCH_OUT,
            COUNT_THRESHOLD_CANDIDATES_OUT,
            INPUT_MANIFEST_OUT,
            CHECKS_OUT,
            SUMMARY_OUT,
            RESULT_OUT,
        ]
    )
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())

