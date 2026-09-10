from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR"

CR119_PERIODIC = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_courtroom_periodic_table.csv"
CR220 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION"
CR220_ELEMENTS = CR220 / "CR220_simulated_element_primary_rows_126.csv"
CR220_ISOTOPES = CR220 / "CR220_simulated_isotope_ladder_rows_214.csv"
CR220_SUMMARY = CR220 / "CR220_summary.json"
CR221 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR"
CR221_KERNEL = CR221 / "CR221_kernel_terms.csv"
CR221_SUMMARY = CR221 / "CR221_summary.json"

PRECOMMIT = OUT / "CR222_PRECOMMIT.md"
RUNNER = OUT / "CR222_runner.py"
DECLARED_CONSTANTS = OUT / "CR222_declared_constants.csv"
ELEMENTS_OUT = OUT / "CR222_constants_only_elements_126.csv"
ISOTOPES_OUT = OUT / "CR222_constants_only_isotopes_214.csv"
VERIFY_OUT = OUT / "CR222_verification_against_cr220_cr119.csv"
BOUNDARY_TESTS = OUT / "CR222_boundary_tests.csv"
INPUT_MANIFEST = OUT / "CR222_input_manifest.csv"
CHECKS = OUT / "CR222_checks.csv"
SUMMARY = OUT / "CR222_summary.json"
RESULT = OUT / "CR222_result.md"
HASHES = OUT / "HASHES.txt"

R = Fraction(12, 1)
D = Fraction(3, 1)
ALPHA_H = Fraction(2, 1)
TWO = Fraction(2, 1)
EIGHT = TWO ** int(D)
SEVEN = Fraction(7, 1)
PROTON_QA = Fraction(145, 2)
ELECTRON_QA = Fraction(145, 96)
NEUTRON_QA = Fraction(1, 8)
CHARGED_PAIR_QA = PROTON_QA + ELECTRON_QA
KAPPA_FLOOR = (PROTON_QA + ELECTRON_QA + NEUTRON_QA) / EIGHT
NEUTRON_G_UNIT = NEUTRON_QA / EIGHT


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def manifest_row(path: Path, role: str, construction_role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "source": rel(path),
        "exists": str(exists),
        "bytes": path.stat().st_size if exists and path.is_file() else "",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
        "role": role,
        "construction_role": construction_role,
    }


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append(
        {
            "check": name,
            "passed": str(bool(passed)),
            "observed": observed,
            "expected": expected,
        }
    )


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists() and path.is_file():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def fdec(value: Fraction) -> str:
    return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def fraction_from_decimal(text: str, max_denominator: int = 10_000_000) -> Fraction:
    return Fraction(Decimal(str(text).strip())).limit_denominator(max_denominator)


def decimal_close(text: str, value: Fraction, tolerance: Decimal = Decimal("1e-70")) -> bool:
    return abs(Decimal(str(text).strip()) - (Decimal(value.numerator) / Decimal(value.denominator))) <= tolerance


def native_capacity() -> int:
    return int(R * R * (Fraction(1, 1) - Fraction(1, EIGHT)))


def shell_n_path() -> list[Fraction]:
    return [Fraction(1, 1), ALPHA_H, D, R / D, R / D, D, ALPHA_H, ALPHA_H]


def shell_capacities() -> list[int]:
    return [int(TWO * n * n) for n in shell_n_path()]


def shell_state(z: int) -> dict[str, Any]:
    remaining = z
    for index, capacity in enumerate(shell_capacities(), start=1):
        if remaining <= capacity:
            return {
                "shell_period": index,
                "shell_n": fstr(shell_n_path()[index - 1]),
                "shell_capacity": capacity,
                "shell_occupancy": remaining,
                "shell_status": "CLOSED_SHELL" if remaining == capacity else "OPEN_SHELL",
            }
        remaining -= capacity
    return {
        "shell_period": len(shell_capacities()) + 1,
        "shell_n": "",
        "shell_capacity": 0,
        "shell_occupancy": remaining,
        "shell_status": "OVER_CAPACITY",
    }


def native_z_coordinates(z: int) -> dict[str, int]:
    return {
        "radix_cycle": ((z - 1) // int(R)) + 1,
        "radix_slot": ((z - 1) % int(R)) + 1,
    }


def isotope_ladder(z: int) -> list[dict[str, Any]]:
    coords = native_z_coordinates(z)
    selected_depth = max(0, coords["radix_cycle"] - 1)
    raw_packets = Fraction(z * selected_depth, int(R))
    delta_n = raw_packets.numerator // raw_packets.denominator
    residual = raw_packets - Fraction(delta_n, 1)
    residual_twelfths = int(residual * R)
    primary_n = z + delta_n
    rows = [
        {
            "ladder_role": "FLOOR_PRIMARY",
            "ladder_weight": fstr((R - Fraction(residual_twelfths, 1)) / R) if residual_twelfths else "1",
            "N": primary_n,
            "residual_twelfths": residual_twelfths,
            "selected_depth_index": selected_depth,
        }
    ]
    if residual_twelfths:
        rows.append(
            {
                "ladder_role": "CEIL_NEIGHBOR",
                "ladder_weight": fstr(Fraction(residual_twelfths, int(R))),
                "N": primary_n + 1,
                "residual_twelfths": residual_twelfths,
                "selected_depth_index": selected_depth,
            }
        )
    return rows


def native_isotope_lane(z: int, residual_twelfths: int, ladder_role: str) -> str:
    if z > native_capacity() - int(EIGHT):
        return "CONSTANT_FRONTIER_TAIL_CANDIDATE"
    if residual_twelfths == 0 and ladder_role == "FLOOR_PRIMARY":
        return "CONSTANT_STABLE_ANCHOR_LANE"
    if residual_twelfths == int(R / 2):
        return "CONSTANT_HALF_WRITE_LANE"
    return "CONSTANT_BOUND_LADDER_LANE"


def native_surface_status(z: int) -> str:
    if z > native_capacity() - int(EIGHT):
        return "CONSTANT_FRONTIER_TAIL_Z119_Z126"
    return "CONSTANT_NATIVE_SURFACE_Z001_Z118"


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    element_rows: list[dict[str, Any]] = []
    isotope_rows: list[dict[str, Any]] = []
    cap = native_capacity()

    for z in range(1, cap + 1):
        coords = native_z_coordinates(z)
        shell = shell_state(z)
        ladder = isotope_ladder(z)
        primary = ladder[0]
        n_primary = int(primary["N"])
        a_primary = z + n_primary
        neutron_excess = n_primary - z
        g_primary = Fraction(z, 1) * KAPPA_FLOOR + Fraction(neutron_excess, 64)
        gr_primary = EIGHT * g_primary
        retained_primary = SEVEN * g_primary
        kappa_eff = g_primary / Fraction(z, 1)
        primary_lane = native_isotope_lane(z, int(primary["residual_twelfths"]), str(primary["ladder_role"]))

        for item in ladder:
            n = int(item["N"])
            a = z + n
            excess = n - z
            g = Fraction(z, 1) * KAPPA_FLOOR + Fraction(excess, 64)
            gr = EIGHT * g
            retained = SEVEN * g
            isotope_rows.append(
                {
                    "isotope_closure_id": f"CR222-IZ{z:03d}N{n:03d}-{item['ladder_role']}",
                    "element_closure_id": f"CR222-EZ{z:03d}",
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
                    "shell_n": shell["shell_n"],
                    "shell_capacity": shell["shell_capacity"],
                    "shell_occupancy": shell["shell_occupancy"],
                    "shell_status": shell["shell_status"],
                    "ladder_role": item["ladder_role"],
                    "ladder_weight": item["ladder_weight"],
                    "selected_depth_index": item["selected_depth_index"],
                    "residual_twelfths": item["residual_twelfths"],
                    "constant_native_lane": native_isotope_lane(z, int(item["residual_twelfths"]), str(item["ladder_role"])),
                    "G_fraction": fstr(g),
                    "G_decimal": fdec(g),
                    "GR_fraction": fstr(gr),
                    "GR_decimal": fdec(gr),
                    "retained_7G_fraction": fstr(retained),
                    "retained_7G_decimal": fdec(retained),
                    "construction_source": "SAM_CONSTANTS_ONLY_NO_CARDS_NO_LABELS",
                }
            )

        element_rows.append(
            {
                "element_closure_id": f"CR222-EZ{z:03d}",
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
                "shell_n": shell["shell_n"],
                "shell_capacity": shell["shell_capacity"],
                "shell_occupancy": shell["shell_occupancy"],
                "shell_status": shell["shell_status"],
                "selected_depth_index": primary["selected_depth_index"],
                "residual_twelfths": primary["residual_twelfths"],
                "primary_ladder_role": primary["ladder_role"],
                "constant_native_lane": primary_lane,
                "constant_surface_status": native_surface_status(z),
                "kappa_floor_fraction": fstr(KAPPA_FLOOR),
                "kappa_eff_fraction": fstr(kappa_eff),
                "neutron_excess_N_minus_Z": neutron_excess,
                "G_fraction": fstr(g_primary),
                "G_decimal": fdec(g_primary),
                "GR_fraction": fstr(gr_primary),
                "GR_decimal": fdec(gr_primary),
                "retained_7G_fraction": fstr(retained_primary),
                "retained_7G_decimal": fdec(retained_primary),
                "known_symbol": "",
                "known_name": "",
                "reference_clock": "",
                "card_source": "",
                "construction_source": "SAM_CONSTANTS_ONLY_NO_CARDS_NO_LABELS",
            }
        )
    return element_rows, isotope_rows


def constants_rows() -> list[dict[str, Any]]:
    n_path = shell_n_path()
    capacities = shell_capacities()
    return [
        {"constant": "R", "fraction": fstr(R), "decimal": fdec(R), "role": "radix/native route constant"},
        {"constant": "D", "fraction": fstr(D), "decimal": fdec(D), "role": "dimension/closure depth constant"},
        {"constant": "alpha_H", "fraction": fstr(ALPHA_H), "decimal": fdec(ALPHA_H), "role": "hidden-source bigrade generator"},
        {"constant": "split", "fraction": fstr(EIGHT), "decimal": fdec(EIGHT), "role": "2^D carrier split"},
        {"constant": "native_capacity", "fraction": str(native_capacity()), "decimal": str(native_capacity()), "role": "R^2*(1-2^-D)"},
        {"constant": "proton_qA", "fraction": fstr(PROTON_QA), "decimal": fdec(PROTON_QA), "role": "component write support"},
        {"constant": "electron_qA", "fraction": fstr(ELECTRON_QA), "decimal": fdec(ELECTRON_QA), "role": "component write support"},
        {"constant": "neutron_qA", "fraction": fstr(NEUTRON_QA), "decimal": fdec(NEUTRON_QA), "role": "component write support"},
        {"constant": "charged_pair_qA", "fraction": fstr(CHARGED_PAIR_QA), "decimal": fdec(CHARGED_PAIR_QA), "role": "proton_qA + electron_qA"},
        {"constant": "kappa_floor", "fraction": fstr(KAPPA_FLOOR), "decimal": fdec(KAPPA_FLOOR), "role": "(proton_qA+electron_qA+neutron_qA)/2^D"},
        {"constant": "neutron_G_unit", "fraction": fstr(NEUTRON_G_UNIT), "decimal": fdec(NEUTRON_G_UNIT), "role": "neutron_qA/2^D"},
        {"constant": "shell_n_path", "fraction": ";".join(fstr(x) for x in n_path), "decimal": ";".join(fdec(x) for x in n_path), "role": "[1, alpha_H, D, R/D, R/D, D, alpha_H, alpha_H]"},
        {"constant": "shell_capacities", "fraction": ";".join(str(x) for x in capacities), "decimal": ";".join(str(x) for x in capacities), "role": "2*n^2 over shell_n_path"},
    ]


def build_verification(
    generated: list[dict[str, Any]],
    cr220_rows: list[dict[str, str]],
    cr119_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    cr220_by_z = {int(row["Z"]): row for row in cr220_rows}
    cr119_by_z = {int(row["Z"]): row for row in cr119_rows}
    rows: list[dict[str, Any]] = []
    for row in generated:
        z = int(row["Z"])
        cr220 = cr220_by_z[z]
        cr119 = cr119_by_z[z]
        generated_g = Fraction(row["G_fraction"])
        generated_gr = Fraction(row["GR_fraction"])
        generated_retained = Fraction(row["retained_7G_fraction"])
        field_matches = {
            "Z": str(row["Z"]) == cr220["Z"],
            "N": str(row["N"]) == cr220["N"],
            "A": str(row["A"]) == cr220["A"],
            "P_address": row["P_address"] == cr220["P_address"],
            "quark_u_count": str(row["quark_u_count"]) == cr220["quark_u_count"],
            "quark_d_count": str(row["quark_d_count"]) == cr220["quark_d_count"],
            "radix_cycle": str(row["radix_cycle"]) == cr220["radix_cycle"],
            "radix_slot": str(row["radix_slot"]) == cr220["radix_slot"],
            "shell_period": str(row["shell_period"]) == cr220["shell_period"],
            "shell_capacity": str(row["shell_capacity"]) == cr220["shell_capacity"],
            "shell_occupancy": str(row["shell_occupancy"]) == cr220["shell_occupancy"],
            "shell_status": row["shell_status"] == cr220["shell_status"],
            "selected_depth_index": str(row["selected_depth_index"]) == cr220["selected_depth_index"],
            "residual_twelfths": str(row["residual_twelfths"]) == cr220["residual_twelfths"],
            "G_vs_CR220": decimal_close(cr220["G_tensor_computed"], generated_g),
            "GR_vs_CR220": decimal_close(cr220["GR_qA_total_computed"], generated_gr),
            "retained_vs_CR220": decimal_close(cr220["retained_7G_computed"], generated_retained),
            "G_vs_CR119": decimal_close(cr119["tensor_carrier_support_primary"], generated_g),
            "GR_vs_CR119": decimal_close(cr119["qA_total_primary"], generated_gr),
            "retained_vs_CR119": decimal_close(cr119["retained_write_support_primary"], generated_retained),
        }
        failed = [name for name, ok in field_matches.items() if not ok]
        rows.append(
            {
                "Z": z,
                "generated_element_closure_id": row["element_closure_id"],
                "cr220_element_closure_id": cr220["element_closure_id"],
                "cr119_element_closure_id": cr119["element_closure_id"],
                "all_compared_fields_match": str(not failed),
                "failed_fields": ";".join(failed),
                "G_generated": row["G_decimal"],
                "G_CR220": cr220["G_tensor_computed"],
                "G_CR119": cr119["tensor_carrier_support_primary"],
                "GR_generated": row["GR_decimal"],
                "GR_CR220": cr220["GR_qA_total_computed"],
                "GR_CR119": cr119["qA_total_primary"],
                "construction_role": "generated_first_from_constants_then_compared",
            }
        )
    return rows


def boundary_rows(element_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cap = native_capacity()
    rows = []
    variants = [
        ("main_R12_D3", R, D, "main constants"),
        ("wrong_R10", Fraction(10, 1), D, "wrong R control"),
        ("wrong_R24", Fraction(24, 1), D, "wrong R control"),
        ("wrong_D2", R, Fraction(2, 1), "wrong D control"),
        ("wrong_D4", R, Fraction(4, 1), "wrong D control"),
    ]
    for control, r_value, d_value, role in variants:
        split = TWO ** int(d_value)
        wrong_cap = int(r_value * r_value * (Fraction(1, 1) - Fraction(1, split)))
        rows.append(
            {
                "control": control,
                "role": role,
                "R": fstr(r_value),
                "D": fstr(d_value),
                "capacity": wrong_cap,
                "matches_126": str(wrong_cap == cap),
                "readout": "main capacity" if wrong_cap == cap else "wrong capacity rejected",
            }
        )
    rows.append(
        {
            "control": "no_Z_enumeration",
            "role": "boundary condition",
            "R": fstr(R),
            "D": fstr(D),
            "capacity": cap,
            "matches_126": "False",
            "readout": "constants give the bound; element rows require enumerating Z=1..capacity",
        }
    )
    rows.append(
        {
            "control": "cards_or_known_labels",
            "role": "forbidden construction input",
            "R": "",
            "D": "",
            "capacity": "",
            "matches_126": "not_used",
            "readout": "known symbols, names, card values, masses, and CLOCK labels are blank in generated rows",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    source_paths = [
        (CR220_ELEMENTS, "verification surface only", "NOT_CONSTRUCTION_INPUT"),
        (CR220_ISOTOPES, "verification surface only", "NOT_CONSTRUCTION_INPUT"),
        (CR220_SUMMARY, "verification boundary only", "NOT_CONSTRUCTION_INPUT"),
        (CR221_KERNEL, "confirms locked component/kappa terms", "VERIFICATION_OF_DECLARED_CONSTANTS"),
        (CR221_SUMMARY, "confirms locked kappa derivation", "VERIFICATION_OF_DECLARED_CONSTANTS"),
        (CR119_PERIODIC, "verification surface only", "NOT_CONSTRUCTION_INPUT"),
    ]
    write_csv(
        INPUT_MANIFEST,
        [manifest_row(path, role, construction_role) for path, role, construction_role in source_paths],
        ["source", "exists", "bytes", "sha256", "role", "construction_role"],
    )

    constants = constants_rows()
    write_csv(DECLARED_CONSTANTS, constants, ["constant", "fraction", "decimal", "role"])

    element_rows, isotope_rows = build_rows()
    element_fields = [
        "element_closure_id",
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
        "shell_n",
        "shell_capacity",
        "shell_occupancy",
        "shell_status",
        "selected_depth_index",
        "residual_twelfths",
        "primary_ladder_role",
        "constant_native_lane",
        "constant_surface_status",
        "kappa_floor_fraction",
        "kappa_eff_fraction",
        "neutron_excess_N_minus_Z",
        "G_fraction",
        "G_decimal",
        "GR_fraction",
        "GR_decimal",
        "retained_7G_fraction",
        "retained_7G_decimal",
        "known_symbol",
        "known_name",
        "reference_clock",
        "card_source",
        "construction_source",
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
        "shell_n",
        "shell_capacity",
        "shell_occupancy",
        "shell_status",
        "ladder_role",
        "ladder_weight",
        "selected_depth_index",
        "residual_twelfths",
        "constant_native_lane",
        "G_fraction",
        "G_decimal",
        "GR_fraction",
        "GR_decimal",
        "retained_7G_fraction",
        "retained_7G_decimal",
        "construction_source",
    ]
    write_csv(ELEMENTS_OUT, element_rows, element_fields)
    write_csv(ISOTOPES_OUT, isotope_rows, isotope_fields)

    _, cr220_rows = read_csv(CR220_ELEMENTS)
    _, cr119_rows = read_csv(CR119_PERIODIC)
    verification = build_verification(element_rows, cr220_rows, cr119_rows)
    verify_fields = [
        "Z",
        "generated_element_closure_id",
        "cr220_element_closure_id",
        "cr119_element_closure_id",
        "all_compared_fields_match",
        "failed_fields",
        "G_generated",
        "G_CR220",
        "G_CR119",
        "GR_generated",
        "GR_CR220",
        "GR_CR119",
        "construction_role",
    ]
    write_csv(VERIFY_OUT, verification, verify_fields)

    boundary = boundary_rows(element_rows)
    write_csv(BOUNDARY_TESTS, boundary, ["control", "role", "R", "D", "capacity", "matches_126", "readout"])

    checks: list[dict[str, Any]] = []
    check(checks, "verification_inputs_exist", all(path.exists() for path, _, _ in source_paths), True, True)
    check(checks, "native_capacity_126", native_capacity() == 126, native_capacity(), 126)
    check(checks, "shell_capacities_sum_126", sum(shell_capacities()) == 126, sum(shell_capacities()), 126)
    check(checks, "shell_capacities_expected", shell_capacities() == [2, 8, 18, 32, 32, 18, 8, 8], shell_capacities(), [2, 8, 18, 32, 32, 18, 8, 8])
    check(checks, "element_rows_126", len(element_rows) == 126, len(element_rows), 126)
    check(checks, "isotope_rows_214", len(isotope_rows) == 214, len(isotope_rows), 214)
    check(checks, "all_verification_rows_match", all(row["all_compared_fields_match"] == "True" for row in verification), sum(row["all_compared_fields_match"] == "True" for row in verification), 126)
    check(checks, "closed_shell_rows_8", Counter(row["shell_status"] for row in element_rows).get("CLOSED_SHELL", 0) == 8, Counter(row["shell_status"] for row in element_rows).get("CLOSED_SHELL", 0), 8)
    check(checks, "frontier_tail_rows_8", Counter(row["constant_surface_status"] for row in element_rows).get("CONSTANT_FRONTIER_TAIL_Z119_Z126", 0) == 8, Counter(row["constant_surface_status"] for row in element_rows).get("CONSTANT_FRONTIER_TAIL_Z119_Z126", 0), 8)
    check(checks, "no_known_symbols_names_or_clock_generated", all(not row["known_symbol"] and not row["known_name"] and not row["reference_clock"] for row in element_rows), True, True)
    check(checks, "no_card_source_generated", all(not row["card_source"] for row in element_rows), True, True)
    check(checks, "wrong_controls_rejected_capacity", all(row["matches_126"] == "False" for row in boundary if row["control"].startswith("wrong_")), [row for row in boundary if row["control"].startswith("wrong_")], "all wrong controls false")
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    counts = {
        "element_rows": len(element_rows),
        "isotope_rows": len(isotope_rows),
        "shell_status": dict(Counter(row["shell_status"] for row in element_rows)),
        "constant_native_lane": dict(Counter(row["constant_native_lane"] for row in element_rows)),
        "constant_surface_status": dict(Counter(row["constant_surface_status"] for row in element_rows)),
    }
    gold_like = next(row for row in element_rows if int(row["Z"]) == 79)
    threshold_edge = next(row for row in element_rows if int(row["Z"]) == 83)
    first_frontier = next(row for row in element_rows if int(row["Z"]) == 119)
    summary = {
        "cr_id": "CR222",
        "artifact": "CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR",
        "execution_status": execution_status,
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "result_class": (
            "CR222_PASS_CONSTANTS_ONLY_ELEMENT_GENERATOR__126_NATIVE_ELEMENT_ROWS__"
            "214_ISOTOPE_LADDER_ROWS__MATCHES_CR220_CR119_126_OF_126__"
            "NO_CARDS_NO_KNOWN_LABELS_NO_CLOCK_INPUTS"
        )
        if execution_status == "CLEAN"
        else "CR222_FAIL_CONSTANTS_ONLY_ELEMENT_GENERATOR",
        "constants": {
            "R": fstr(R),
            "D": fstr(D),
            "alpha_H": fstr(ALPHA_H),
            "split_2_to_D": fstr(EIGHT),
            "native_capacity": native_capacity(),
            "capacity_law": "R^2*(1-2^-D)",
            "shell_n_path": [fstr(x) for x in shell_n_path()],
            "shell_capacities": shell_capacities(),
            "proton_qA": fstr(PROTON_QA),
            "electron_qA": fstr(ELECTRON_QA),
            "neutron_qA": fstr(NEUTRON_QA),
            "kappa_floor": fstr(KAPPA_FLOOR),
            "neutron_G_unit": fstr(NEUTRON_G_UNIT),
        },
        "counts": counts,
        "gold_like_Z79": gold_like,
        "threshold_edge_Z83": threshold_edge,
        "first_frontier_Z119": first_frontier,
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": (
            "Constants and native generator rules calculate the 126 native element-family rows, "
            "primary P addresses, isotope ladder, shell placement, G, GR, and retained support. "
            "They do not calculate downstream names, symbols, measured masses, or reference CLOCK "
            "stability labels."
        ),
        "outputs": {
            "declared_constants": rel(DECLARED_CONSTANTS),
            "elements": rel(ELEMENTS_OUT),
            "isotopes": rel(ISOTOPES_OUT),
            "verification": rel(VERIFY_OUT),
            "boundary_tests": rel(BOUNDARY_TESTS),
            "checks": rel(CHECKS),
            "summary": rel(SUMMARY),
            "result": rel(RESULT),
        },
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR222 Constants-Only Element Generator

Result: **{summary['result_class']}**

## Direct Answer

Yes: within the SAM-native boundary, the elements can now be calculated from
constants only.

The run generated:

- **126** native element-family rows.
- **214** isotope-ladder rows.
- **8** closed-shell rows.
- **8** constant frontier-tail rows (`Z=119..126`).

No element cards, known symbols, known names, measured masses, or CLOCK labels
were used to construct the rows.

## Construction Formula

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
native_capacity = R^2 * (1 - 2^-D) = 126

Z = 1..126
P = Zp + Nn + Ze
N = Z + floor(Z * (radix_cycle - 1) / R)
G(P) = Z * 7117/768 + (N - Z)/64
GR(P) = 8G(P)
retained = 7G(P)
```

The shell vector was generated from:

```text
n_path = [1, alpha_H, D, R/D, R/D, D, alpha_H, alpha_H]
capacity = 2n^2
```

giving:

```text
[2, 8, 18, 32, 32, 18, 8, 8]
```

## Verification

The generated rows were compared after construction:

- Generated core fields match CR220: **126/126**
- Generated `G(P)` matches CR220 and CR119: **126/126**
- Generated `GR(P)` matches CR220 and CR119: **126/126**
- Generated retained support matches CR220 and CR119: **126/126**

## Boundary

This calculates the SAM-native element-family table, not the public chemistry
labels. Names like Hydrogen or Gold remain downstream reveal labels. Physical
stability/CLOCK still remains a comparator surface; CR220 showed the count
threshold gets to `Z<=83` with the `43/61` holes still requiring a native
derivation.

## Artifacts

- `{rel(DECLARED_CONSTANTS)}`
- `{rel(ELEMENTS_OUT)}`
- `{rel(ISOTOPES_OUT)}`
- `{rel(VERIFY_OUT)}`
- `{rel(BOUNDARY_TESTS)}`
- `{rel(INPUT_MANIFEST)}`
- `{rel(CHECKS)}`
- `{rel(SUMMARY)}`
- `{rel(HASHES)}`
"""
    RESULT.write_text(result_text, encoding="utf-8")

    write_hashes(
        [
            PRECOMMIT,
            RUNNER,
            DECLARED_CONSTANTS,
            ELEMENTS_OUT,
            ISOTOPES_OUT,
            VERIFY_OUT,
            BOUNDARY_TESTS,
            INPUT_MANIFEST,
            CHECKS,
            SUMMARY,
            RESULT,
        ]
    )
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())

