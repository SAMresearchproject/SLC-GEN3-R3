from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK"

CR223_RUNNER = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR223_FORMULA_SPREADSHEET_EXPORT" / "CR223_runner.py"
CR225_SUMMARY = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR225_CARRIER_HIDDEN_CLOCK_SELECTOR" / "CR225_summary.json"
CR226_SUMMARY = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL" / "CR226_summary.json"

PRECOMMIT = OUT / "CR227_PRECOMMIT.md"
RUNNER = OUT / "CR227_runner.py"
WORKBOOK = OUT / "CR227_no_free_input_sob_formula_workbook.xlsx"
FORMULA_MAP = OUT / "CR227_formula_map.csv"
INPUT_MANIFEST = OUT / "CR227_input_manifest.csv"
CHECKS = OUT / "CR227_checks.csv"
SUMMARY = OUT / "CR227_summary.json"
RESULT = OUT / "CR227_result.md"
HASHES = OUT / "HASHES.txt"

R = Fraction(12, 1)
D = Fraction(3, 1)
ALPHA_H = Fraction(2, 1)
SPLIT = Fraction(2, 1) ** int(D)
CAPACITY = R * R * (Fraction(1, 1) - Fraction(1, SPLIT))
KAPPA_FLOOR = Fraction(7117, 768)
NEUTRON_G_UNIT = Fraction(1, 64)
TENSOR_RELEASE = R * R / SPLIT
NEUTRAL_VECTOR = D ** (int(D) + 1)
HIDDEN_ROWS = [(a, b, int(ALPHA_H) ** a * int(D) ** b) for a in range(4) for b in range(3)]
HIDDEN_SET = sorted(p for _, _, p in HIDDEN_ROWS if p <= int(R))
HIDDEN_SUM = sum(HIDDEN_SET)
CLOCK_BOUNDARY = int(NEUTRAL_VECTOR + ALPHA_H)
CLOCK_HOLE_1 = HIDDEN_SUM - int(ALPHA_H)
CLOCK_HOLE_2 = CLOCK_HOLE_1 + int(TENSOR_RELEASE)
FRONTIER_START = int(CAPACITY - SPLIT + 1)


def load_cr223_helpers() -> Any:
    spec = importlib.util.spec_from_file_location("cr223_helpers", CR223_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load helpers from {CR223_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


H = load_cr223_helpers()
s = H.s
n = H.n
formula = H.formula
sheet_xml = H.sheet_xml
workbook_package = H.workbook_package
xml_text = H.xml_text
fstr = H.fstr


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
    rows.append({"check": name, "passed": str(bool(passed)), "observed": observed, "expected": expected})


def fdec(value: Fraction, places: int = 15) -> str:
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{dec:.{places}f}".rstrip("0").rstrip(".")


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


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists() and path.is_file():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def shell_n_path() -> list[Fraction]:
    return [Fraction(1, 1), ALPHA_H, D, R / D, R / D, D, ALPHA_H, ALPHA_H]


def shell_capacities() -> list[int]:
    return [int(Fraction(2, 1) * x * x) for x in shell_n_path()]


def element_values(z: int) -> dict[str, Any]:
    radix_cycle = ((z - 1) // int(R)) + 1
    radix_slot = ((z - 1) % int(R)) + 1
    selected_depth = max(0, radix_cycle - 1)
    raw = Fraction(z * selected_depth, int(R))
    delta_n = raw.numerator // raw.denominator
    residual_twelfths = int((raw - delta_n) * R)
    n_primary = z + delta_n
    shell_remaining = z
    shell_period = 1
    shell_n = ""
    shell_capacity = 0
    cumulative = 0
    for i, cap in enumerate(shell_capacities(), start=1):
        if shell_remaining <= cap:
            shell_period = i
            shell_capacity = cap
            shell_n = fstr(shell_n_path()[i - 1])
            break
        shell_remaining -= cap
        cumulative += cap
    g = Fraction(z, 1) * KAPPA_FLOOR + Fraction(n_primary - z, 64)
    gr = g * SPLIT
    retained = g * 7
    clock = "frontier" if z >= FRONTIER_START else ("stable" if z <= CLOCK_BOUNDARY and z not in {CLOCK_HOLE_1, CLOCK_HOLE_2} else "radioactive")
    return {
        "sob_id": f"SOB{z}",
        "Z": z,
        "N": n_primary,
        "A": z + n_primary,
        "radix_cycle": radix_cycle,
        "radix_slot": radix_slot,
        "selected_depth": selected_depth,
        "delta_n": delta_n,
        "residual_twelfths": residual_twelfths,
        "shell_period": shell_period,
        "shell_n": shell_n,
        "shell_capacity": shell_capacity,
        "shell_occupancy": shell_remaining,
        "shell_status": "CLOSED_SHELL" if shell_remaining == shell_capacity else "OPEN_SHELL",
        "P_subscript": f"P_{z},{z+n_primary}",
        "P_address": f"{z}p+{n_primary}n+{z}e",
        "quark_u": 2 * z + n_primary,
        "quark_d": z + 2 * n_primary,
        "quark_e": z,
        "quark_address": f"{2*z+n_primary}u+{z+2*n_primary}d+{z}e",
        "G": g,
        "GR": gr,
        "retained": retained,
        "clock": clock,
        "native_lane": (
            "CONSTANT_FRONTIER_TAIL_CANDIDATE"
            if z >= FRONTIER_START
            else "CONSTANT_STABLE_ANCHOR_LANE"
            if residual_twelfths == 0
            else "CONSTANT_HALF_WRITE_LANE"
            if residual_twelfths == int(R / 2)
            else "CONSTANT_BOUND_LADDER_LANE"
        ),
    }


def build_constants_sheet() -> list[list[dict[str, Any]]]:
    rows = [[s("Constant", 1), s("Value", 1), s("Formula", 1), s("Role", 1), s("Input status", 1)]]
    data = [
        ("R", 12, "declared", "radix/native route constant", "SEALED_CONSTANT"),
        ("D", 3, "declared", "closure depth", "SEALED_CONSTANT"),
        ("alpha_H", 2, "declared", "hidden-source generator", "SEALED_CONSTANT"),
        ("split", 8, "=2^D", "carrier split", "FORMULA"),
        ("R_squared", 144, "=R^2", "full lattice", "FORMULA"),
        ("native_capacity", 126, "=R^2*(1-1/split)", "SOB row count", "FORMULA"),
        ("frontier_start", 119, "=capacity-split+1", "frontier begins", "FORMULA"),
        ("kappa_floor", fdec(KAPPA_FLOOR), "=7117/768", "floor kappa", "FORMULA"),
        ("neutron_G_unit", fdec(NEUTRON_G_UNIT), "=1/64", "neutron excess G unit", "FORMULA"),
        ("tensor_release_T", 18, "=R^2/split", "carrier tensor release", "FORMULA"),
        ("neutral_vector_Zc", 81, "=D^(D+1)", "neutral vector carrier", "FORMULA"),
        ("hidden_sum_H", 45, "=SUM(Hidden_Set!D2:D13)", "hidden bigrade sum", "FORMULA"),
        ("clock_boundary", 83, "=neutral_vector_Zc+alpha_H", "stable boundary", "FORMULA"),
        ("clock_hole_1", 43, "=hidden_sum_H-alpha_H", "first hole", "FORMULA"),
        ("clock_hole_2", 61, "=clock_hole_1+tensor_release_T", "tensor-shifted hole", "FORMULA"),
        ("clock_rule", "stable iff Z<=83 and Z not in {43,61}", "formula text", "CLOCK selector", "FORMULA_TEXT"),
    ]
    for idx, (name, value, expr, role, input_status) in enumerate(data, start=2):
        if name == "split":
            value_cell = formula(value, "2^B3")
        elif name == "R_squared":
            value_cell = formula(value, "B2^2")
        elif name == "native_capacity":
            value_cell = formula(value, "B6*(1-1/B5)")
        elif name == "frontier_start":
            value_cell = formula(value, "B7-B5+1")
        elif name == "kappa_floor":
            value_cell = formula(value, "7117/768")
        elif name == "neutron_G_unit":
            value_cell = formula(value, "1/64")
        elif name == "tensor_release_T":
            value_cell = formula(value, "B6/B5")
        elif name == "neutral_vector_Zc":
            value_cell = formula(value, "B3^(B3+1)")
        elif name == "hidden_sum_H":
            value_cell = formula(value, "SUM(Hidden_Set!D2:D13)")
        elif name == "clock_boundary":
            value_cell = formula(value, "B12+B4")
        elif name == "clock_hole_1":
            value_cell = formula(value, "B13-B4")
        elif name == "clock_hole_2":
            value_cell = formula(value, "B15+B11")
        else:
            value_cell = s(value) if isinstance(value, str) else n(value)
        rows.append([s(name), value_cell, s(expr), s(role), s(input_status)])
    return rows


def build_hidden_sheet() -> list[list[dict[str, Any]]]:
    rows = [[s("a", 1), s("b", 1), s("p=alpha_H^a*D^b", 1), s("included_p", 1), s("include_rule", 1)]]
    for i, (a, b, p) in enumerate(HIDDEN_ROWS, start=2):
        rows.append(
            [
                n(a),
                n(b),
                formula(p, f"Constants!$B$4^A{i}*Constants!$B$3^B{i}"),
                formula(p if p <= int(R) else 0, f"IF(C{i}<=Constants!$B$2,C{i},0)"),
                formula("yes" if p <= int(R) else "no", f'IF(C{i}<=Constants!$B$2,"yes","no")', cell_type="str"),
            ]
        )
    rows.append([s("hidden_sum_H"), s(""), s(""), formula(HIDDEN_SUM, "SUM(D2:D13)"), s("must equal Constants!B13")])
    return rows


def build_sob_sheet() -> list[list[dict[str, Any]]]:
    headers = [
        "sob_id", "Z", "N", "A", "radix_cycle", "radix_slot", "selected_depth", "delta_n", "residual_twelfths",
        "P_subscript", "P_address", "quark_u", "quark_d", "quark_e", "quark_address", "shell_period", "shell_capacity",
        "shell_occupancy", "shell_status", "native_lane", "clock_prediction", "kappa_floor", "G(P)", "GR(P)",
        "retained_7G", "light_face", "action_face", "bottom_A_line", "construction_source",
    ]
    rows = [[s(header, 1) for header in headers]]
    for z in range(1, 127):
        v = element_values(z)
        r = z + 1
        rows.append(
            [
                formula(v["sob_id"], f'"SOB"&B{r}', cell_type="str"),
                formula(z, "ROW()-1"),
                formula(v["N"], f"B{r}+H{r}"),
                formula(v["A"], f"B{r}+C{r}"),
                formula(v["radix_cycle"], f"INT((B{r}-1)/Constants!$B$2)+1"),
                formula(v["radix_slot"], f"MOD(B{r}-1,Constants!$B$2)+1"),
                formula(v["selected_depth"], f"MAX(0,E{r}-1)"),
                formula(v["delta_n"], f"INT(B{r}*G{r}/Constants!$B$2)"),
                formula(v["residual_twelfths"], f"MOD(B{r}*G{r},Constants!$B$2)"),
                formula(v["P_subscript"], f'"P_"&B{r}&","&D{r}', cell_type="str"),
                formula(v["P_address"], f'B{r}&"p+"&C{r}&"n+"&B{r}&"e"', cell_type="str"),
                formula(v["quark_u"], f"2*B{r}+C{r}"),
                formula(v["quark_d"], f"B{r}+2*C{r}"),
                formula(v["quark_e"], f"B{r}"),
                formula(v["quark_address"], f'L{r}&"u+"&M{r}&"d+"&N{r}&"e"', cell_type="str"),
                formula(v["shell_period"], f'COUNTIF(Shells!$E$2:$E$9,"<"&B{r})+1'),
                formula(v["shell_capacity"], f"INDEX(Shells!$C$2:$C$9,P{r})"),
                formula(v["shell_occupancy"], f"B{r}-IF(P{r}=1,0,INDEX(Shells!$E$2:$E$9,P{r}-1))"),
                formula(v["shell_status"], f'IF(R{r}=Q{r},"CLOSED_SHELL","OPEN_SHELL")', cell_type="str"),
                formula(v["native_lane"], f'IF(B{r}>=Constants!$B$8,"CONSTANT_FRONTIER_TAIL_CANDIDATE",IF(I{r}=0,"CONSTANT_STABLE_ANCHOR_LANE",IF(I{r}=Constants!$B$2/2,"CONSTANT_HALF_WRITE_LANE","CONSTANT_BOUND_LADDER_LANE")))', cell_type="str"),
                formula(v["clock"], f'IF(B{r}>=Constants!$B$8,"frontier",IF(AND(B{r}<=Constants!$B$14,B{r}<>Constants!$B$15,B{r}<>Constants!$B$16),"stable","radioactive"))', cell_type="str"),
                formula(fdec(KAPPA_FLOOR), "Constants!$B$9"),
                formula(fdec(v["G"]), f"B{r}*Constants!$B$9+(C{r}-B{r})*Constants!$B$10"),
                formula(fdec(v["GR"]), f"W{r}*Constants!$B$5"),
                formula(fdec(v["retained"]), f"W{r}*7"),
                formula(f"shell {v['shell_period']} occupancy {v['shell_occupancy']}/{v['shell_capacity']}", f'"shell "&P{r}&" occupancy "&R{r}&"/"&Q{r}', cell_type="str"),
                formula("closure", '"closure"', cell_type="str"),
                formula(v["A"], f'"A=Z+N="&B{r}&"+"&C{r}&"="&D{r}', cell_type="str"),
                formula("SAM_CONSTANTS_ONLY_NO_FREE_INPUTS", '"SAM_CONSTANTS_ONLY_NO_FREE_INPUTS"', cell_type="str"),
            ]
        )
    return rows


def build_shells_sheet() -> list[list[dict[str, Any]]]:
    rows = [[s("shell_period", 1), s("n", 1), s("capacity", 1), s("start_Z", 1), s("end_Z", 1), s("n_formula", 1)]]
    formulas = ["1", "Constants!$B$4", "Constants!$B$3", "Constants!$B$2/Constants!$B$3", "Constants!$B$2/Constants!$B$3", "Constants!$B$3", "Constants!$B$4", "Constants!$B$4"]
    end = 0
    for i, n_value in enumerate(shell_n_path(), start=1):
        cap = shell_capacities()[i - 1]
        start = end + 1
        end += cap
        row = i + 1
        rows.append(
            [
                n(i),
                formula(fdec(n_value), formulas[i - 1]),
                formula(cap, f"2*B{row}^2"),
                formula(start, "1" if i == 1 else f"E{row-1}+1"),
                formula(end, f"SUM($C$2:C{row})"),
                s("=" + formulas[i - 1]),
            ]
        )
    return rows


def build_card_payloads() -> list[list[dict[str, Any]]]:
    headers = [
        "sob_id", "card_title_native", "element_face", "matter_face_native", "clock_face",
        "light_face", "action_face", "P_subscript", "P_address", "quark_address",
        "kernel_line_1", "kernel_line_2", "kernel_line_3", "bottom_A_line", "reveal_name",
        "reveal_symbol", "matter_reference_mass",
    ]
    rows = [[s(header, 1) for header in headers]]
    for z in range(1, 127):
        v = element_values(z)
        r = z + 1
        sr = z + 1
        rows.append(
            [
                formula(v["sob_id"], f"SOB_126!A{sr}", cell_type="str"),
                formula(v["sob_id"], f"SOB_126!A{sr}", cell_type="str"),
                formula(f"E Z={z}", f'"E Z="&SOB_126!B{sr}', cell_type="str"),
                formula(f"A={v['A']}", f'"A="&SOB_126!D{sr}', cell_type="str"),
                formula(v["clock"], f"SOB_126!U{sr}", cell_type="str"),
                formula(v["light_face"] if "light_face" in v else f"shell {v['shell_period']} occupancy {v['shell_occupancy']}/{v['shell_capacity']}", f"SOB_126!Z{sr}", cell_type="str"),
                formula("closure", f"SOB_126!AA{sr}", cell_type="str"),
                formula(v["P_subscript"], f"SOB_126!J{sr}", cell_type="str"),
                formula(v["P_address"], f"SOB_126!K{sr}", cell_type="str"),
                formula(v["quark_address"], f"SOB_126!O{sr}", cell_type="str"),
                formula(f"G(P)={fdec(v['G'], 6)}", f'"G(P)="&TEXT(SOB_126!W{sr},"0.000000")', cell_type="str"),
                formula(f"GR(P)=8G(P)={fdec(v['GR'], 6)}", f'"GR(P)=8G(P)="&TEXT(SOB_126!X{sr},"0.000000")', cell_type="str"),
                formula("GR(P)=7G(P)+G(P)", '"GR(P)=7G(P)+G(P)"', cell_type="str"),
                formula(v["A"], f"SOB_126!AB{sr}", cell_type="str"),
                s(""),
                s(""),
                s(""),
            ]
        )
    return rows


def build_formula_map_rows() -> list[dict[str, Any]]:
    return [
        {"sheet": "Constants", "range": "B2:B17", "purpose": "sealed constants and derived CR225 clock terms", "formula_example": "=2^B3; =B6/B5; =B13-B4"},
        {"sheet": "Hidden_Set", "range": "A2:E14", "purpose": "derive H from alpha_H^a * D^b <= R", "formula_example": "=Constants!$B$4^A2*Constants!$B$3^B2"},
        {"sheet": "Shells", "range": "B2:E9", "purpose": "derive shell path and capacities", "formula_example": "=2*B2^2"},
        {"sheet": "SOB_126", "range": "A2:AC127", "purpose": "derive all 126 SOB rows, P addresses, G/GR, and CLOCK prediction", "formula_example": '=IF(AND(B2<=Constants!$B$14,B2<>Constants!$B$15,B2<>Constants!$B$16),"stable","radioactive")'},
        {"sheet": "Card_Payloads_126", "range": "A2:Q127", "purpose": "derive card-facing text fields without reveal labels", "formula_example": '="GR(P)=8G(P)="&TEXT(SOB_126!X2,"0.000000")'},
        {"sheet": "Checks", "range": "B2:E16", "purpose": "formula checks for counts and Z79 readout", "formula_example": '=COUNTIF(SOB_126!U2:U127,"stable")'},
    ]


def build_formula_map_sheet() -> list[list[dict[str, Any]]]:
    fields = ["sheet", "range", "purpose", "formula_example"]
    rows = [[s(field, 1) for field in fields]]
    for item in build_formula_map_rows():
        rows.append([s(item[field]) for field in fields])
    return rows


def build_checks_sheet() -> list[list[dict[str, Any]]]:
    checks = [
        ("native_capacity", "Constants!B7", 126, "126"),
        ("hidden_sum_H", "Constants!B13", 45, "45"),
        ("clock_boundary", "Constants!B14", 83, "83"),
        ("clock_hole_1", "Constants!B15", 43, "43"),
        ("clock_hole_2", "Constants!B16", 61, "61"),
        ("sob_rows", "COUNTA(SOB_126!B2:B127)", 126, "126"),
        ("clock_stable_count", 'COUNTIF(SOB_126!U2:U127,"stable")', 81, "81"),
        ("clock_radioactive_count", 'COUNTIF(SOB_126!U2:U127,"radioactive")', 37, "37"),
        ("clock_frontier_count", 'COUNTIF(SOB_126!U2:U127,"frontier")', 8, "8"),
        ("closed_shell_count", 'COUNTIF(SOB_126!S2:S127,"CLOSED_SHELL")', 8, "8"),
        ("z79_N", "INDEX(SOB_126!C2:C127,79)", 118, "118"),
        ("z79_A", "INDEX(SOB_126!D2:D127,79)", 197, "197"),
        ("z79_clock", "INDEX(SOB_126!U2:U127,79)", "stable", "stable"),
        ("z79_P", "INDEX(SOB_126!K2:K127,79)", "79p+118n+79e", "79p+118n+79e"),
        ("reveal_fields_blank", "COUNTA(Card_Payloads_126!O2:Q127)", 0, "0"),
    ]
    rows = [[s("check", 1), s("formula_result", 1), s("formula", 1), s("expected", 1), s("status", 1)]]
    for idx, (name, expr, value, expected) in enumerate(checks, start=2):
        rows.append(
            [
                s(name),
                formula(value, expr, cell_type="str" if isinstance(value, str) else None),
                s("=" + expr),
                s(expected),
                formula("PASS", f'IF(B{idx}=D{idx},"PASS","FAIL")', cell_type="str"),
            ]
        )
    return rows


def workbook_formula_count(path: Path) -> int:
    count = 0
    with zipfile.ZipFile(path, "r") as zf:
        for name in zf.namelist():
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                count += zf.read(name).decode("utf-8").count("<f>")
    return count


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    input_manifest = [
        manifest_row(PRECOMMIT, "precommit declaration", "TASK_DECLARATION"),
        manifest_row(RUNNER, "reproducible workbook runner", "EXECUTION_SCRIPT"),
        manifest_row(CR223_RUNNER, "workbook XML helper implementation", "IMPLEMENTATION_HELPER"),
        manifest_row(CR225_SUMMARY, "clock selector verification reference", "VERIFICATION_ONLY_NOT_CONSTRUCTION"),
        manifest_row(CR226_SUMMARY, "vault card generation verification reference", "VERIFICATION_ONLY_NOT_CONSTRUCTION"),
    ]
    write_csv(INPUT_MANIFEST, input_manifest, ["source", "exists", "bytes", "sha256", "role", "construction_role"])

    sheets = {
        "Constants": sheet_xml(build_constants_sheet(), widths={1: 24, 2: 28, 3: 34, 4: 34, 5: 24}, autofilter_ref="A1:E17"),
        "Hidden_Set": sheet_xml(build_hidden_sheet(), widths={1: 10, 2: 10, 3: 22, 4: 14, 5: 18}, autofilter_ref="A1:E14"),
        "Shells": sheet_xml(build_shells_sheet(), widths={1: 14, 2: 12, 3: 14, 4: 12, 5: 12, 6: 34}, autofilter_ref="A1:F9"),
        "SOB_126": sheet_xml(build_sob_sheet(), widths={1: 12, 10: 14, 11: 18, 15: 22, 21: 16, 23: 18, 24: 18, 25: 18, 26: 28, 28: 24, 29: 32}, autofilter_ref="A1:AC127"),
        "Card_Payloads_126": sheet_xml(build_card_payloads(), widths={1: 12, 2: 18, 3: 16, 4: 16, 5: 16, 8: 16, 9: 18, 10: 22, 11: 22, 12: 26, 13: 22, 14: 24}, autofilter_ref="A1:Q127"),
        "Formula_Map": sheet_xml(build_formula_map_sheet(), widths={1: 20, 2: 20, 3: 62, 4: 54}, autofilter_ref="A1:D7"),
        "Checks": sheet_xml(build_checks_sheet(), widths={1: 28, 2: 24, 3: 52, 4: 24, 5: 12}, autofilter_ref="A1:E16"),
    }
    workbook_package(sheets, WORKBOOK)
    write_csv(FORMULA_MAP, build_formula_map_rows(), ["sheet", "range", "purpose", "formula_example"])

    formula_count = workbook_formula_count(WORKBOOK)
    xlsx_valid_zip = zipfile.is_zipfile(WORKBOOK)
    with zipfile.ZipFile(WORKBOOK, "r") as zf:
        parts = zf.namelist()
        workbook_xml = zf.read("xl/workbook.xml").decode("utf-8")
        sob_xml = zf.read("xl/worksheets/sheet4.xml").decode("utf-8")

    prediction_counts = Counter(element_values(z)["clock"] for z in range(1, 127))
    z79 = element_values(79)
    cr225 = read_json(CR225_SUMMARY) if CR225_SUMMARY.exists() else {}
    cr226 = read_json(CR226_SUMMARY) if CR226_SUMMARY.exists() else {}

    checks: list[dict[str, Any]] = []
    check(checks, "xlsx_written", WORKBOOK.exists() and WORKBOOK.stat().st_size > 0, WORKBOOK.stat().st_size if WORKBOOK.exists() else 0, ">0")
    check(checks, "xlsx_is_valid_zip", xlsx_valid_zip, xlsx_valid_zip, True)
    check(checks, "xlsx_has_7_sheets", sum(1 for part in parts if part.startswith("xl/worksheets/sheet")) == 7, sum(1 for part in parts if part.startswith("xl/worksheets/sheet")), 7)
    check(checks, "sheet_names_present", all(name in workbook_xml for name in sheets), list(sheets), "all sheet names in workbook.xml")
    check(checks, "formula_count_gt_5000", formula_count > 5000, formula_count, ">5000")
    check(checks, "sob_formula_rows_126", len(build_sob_sheet()) - 1 == 126, len(build_sob_sheet()) - 1, 126)
    check(checks, "card_payload_formula_rows_126", len(build_card_payloads()) - 1 == 126, len(build_card_payloads()) - 1, 126)
    check(checks, "clock_prediction_counts_81_37_8", dict(prediction_counts) == {"stable": 81, "radioactive": 37, "frontier": 8}, dict(prediction_counts), {"stable": 81, "radioactive": 37, "frontier": 8})
    check(checks, "hidden_sum_45", HIDDEN_SUM == 45, HIDDEN_SUM, 45)
    check(checks, "clock_holes_43_61", [CLOCK_HOLE_1, CLOCK_HOLE_2] == [43, 61], [CLOCK_HOLE_1, CLOCK_HOLE_2], [43, 61])
    check(checks, "z79_values", z79["N"] == 118 and z79["A"] == 197 and z79["clock"] == "stable", {"N": z79["N"], "A": z79["A"], "clock": z79["clock"]}, "N=118,A=197,stable")
    check(checks, "z79_kernel_values_match_cr226", str(cr226.get("z79", {}).get("native", {}).get("G_decimal", "")).startswith(fdec(z79["G"], 12)), {"workbook": fdec(z79["G"], 12), "cr226": cr226.get("z79", {}).get("native", {}).get("G_decimal", "")}, "G match")
    check(checks, "cr225_candidate_rule_matches", cr225.get("native_formula", {}).get("candidate_rule") == "stable iff Z <= 83 and Z not in {43,61}", cr225.get("native_formula", {}).get("candidate_rule"), "stable iff Z <= 83 and Z not in {43,61}")
    check(checks, "no_reveal_strings_in_sob_sheet", all(token not in sob_xml for token in ["Gold", "Hydrogen", "Au", "Matter 196.967"]), "checked", "no reveal labels")
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    result_class = (
        "CR227_PASS_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK__126_ROWS__CLOCK_FORMULA_INCLUDED__FORMULA_CELLS_GT_5000__NO_REVEAL_INPUTS"
        if execution_status == "CLEAN"
        else "CR227_FAIL_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK"
    )
    summary = {
        "cr_id": "CR227",
        "artifact": "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK",
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "execution_status": execution_status,
        "result_class": result_class,
        "workbook": rel(WORKBOOK),
        "formula_count": formula_count,
        "sheets": list(sheets.keys()),
        "rows": {
            "sob_formula_rows": 126,
            "card_payload_formula_rows": 126,
        },
        "prediction_counts": dict(prediction_counts),
        "z79": {
            "Z": 79,
            "N": z79["N"],
            "A": z79["A"],
            "P_address": z79["P_address"],
            "quark_address": z79["quark_address"],
            "G_decimal": fdec(z79["G"], 15),
            "GR_decimal": fdec(z79["GR"], 15),
            "clock_prediction": z79["clock"],
        },
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": "Workbook contains formula-derived SOB rows and card payloads from SAM constants only; reveal fields are blank.",
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR227 No-Free-Input SOB Formula Workbook

Result: **{result_class}**

## Direct Answer

Created the no-free-input workbook:

`{rel(WORKBOOK)}`

The workbook has formula-driven sheets for all 126 SOB rows and card payloads.
It includes the CR225 clock formula:

```text
stable iff Z <= 83 and Z not in {{43,61}}
frontier iff Z > 118
```

## Workbook

- sheets: {len(sheets)}
- formula cells: {formula_count}
- SOB rows: 126
- card payload rows: 126
- prediction counts: {dict(prediction_counts)}

Z79 readout:

```text
N={z79['N']}
A={z79['A']}
P={z79['P_address']}
quark={z79['quark_address']}
G={fdec(z79['G'], 15)}
GR={fdec(z79['GR'], 15)}
clock={z79['clock']}
```

## Boundary

No known names, symbols, measured masses, public cards, or reveal labels are
construction inputs. Reveal fields on `Card_Payloads_126` are blank.

## Artifacts

- `{rel(WORKBOOK)}`
- `{rel(FORMULA_MAP)}`
- `{rel(INPUT_MANIFEST)}`
- `{rel(CHECKS)}`
- `{rel(SUMMARY)}`
- `{rel(HASHES)}`
"""
    RESULT.write_text(result_text, encoding="utf-8")

    write_hashes([PRECOMMIT, RUNNER, WORKBOOK, FORMULA_MAP, INPUT_MANIFEST, CHECKS, SUMMARY, RESULT])
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
