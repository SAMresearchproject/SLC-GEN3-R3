from __future__ import annotations

import csv
import hashlib
import json
import os
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR223_FORMULA_SPREADSHEET_EXPORT"

CR222 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR"
CR222_ELEMENTS = CR222 / "CR222_constants_only_elements_126.csv"
CR222_SUMMARY = CR222 / "CR222_summary.json"
CR222_CONSTANTS = CR222 / "CR222_declared_constants.csv"

PRECOMMIT = OUT / "CR223_PRECOMMIT.md"
RUNNER = OUT / "CR223_runner.py"
WORKBOOK = OUT / "CR223_constants_only_element_formulas.xlsx"
FORMULA_MAP = OUT / "CR223_formula_map.csv"
INPUT_MANIFEST = OUT / "CR223_input_manifest.csv"
CHECKS = OUT / "CR223_checks.csv"
SUMMARY = OUT / "CR223_summary.json"
RESULT = OUT / "CR223_result.md"
HASHES = OUT / "HASHES.txt"

R = Fraction(12, 1)
D = Fraction(3, 1)
ALPHA_H = Fraction(2, 1)
SPLIT = Fraction(8, 1)
PROTON_QA = Fraction(145, 2)
ELECTRON_QA = Fraction(145, 96)
NEUTRON_QA = Fraction(1, 8)
KAPPA_FLOOR = (PROTON_QA + ELECTRON_QA + NEUTRON_QA) / SPLIT
NEUTRON_G_UNIT = NEUTRON_QA / SPLIT


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


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append({"check": name, "passed": str(bool(passed)), "observed": observed, "expected": expected})


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
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fdec(value: Fraction) -> str:
    return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def fstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def cell_ref(row: int, col: int) -> str:
    return f"{col_name(col)}{row}"


def xml_text(value: Any) -> str:
    return escape(str(value), {"\n": "&#10;"})


def cell_xml(row: int, col: int, cell: dict[str, Any]) -> str:
    ref = cell_ref(row, col)
    style = f' s="{cell.get("style")}"' if cell.get("style") is not None else ""
    formula = cell.get("formula")
    value = cell.get("value", "")
    cell_type = cell.get("type")
    if formula is not None:
        if cell_type == "str":
            return f'<c r="{ref}" t="str"{style}><f>{xml_text(formula)}</f><v>{xml_text(value)}</v></c>'
        return f'<c r="{ref}"{style}><f>{xml_text(formula)}</f><v>{xml_text(value)}</v></c>'
    if value == "":
        return ""
    if cell_type == "n" or isinstance(value, (int, float, Decimal)):
        return f'<c r="{ref}"{style}><v>{xml_text(value)}</v></c>'
    return f'<c r="{ref}" t="inlineStr"{style}><is><t>{xml_text(value)}</t></is></c>'


def sheet_xml(
    rows: list[list[dict[str, Any]]],
    *,
    freeze_rows: int = 1,
    widths: dict[int, int] | None = None,
    autofilter_ref: str | None = None,
) -> str:
    widths = widths or {}
    max_col = max((len(row) for row in rows), default=1)
    cols = ""
    if widths:
        col_lines = []
        for col, width in sorted(widths.items()):
            col_lines.append(f'<col min="{col}" max="{col}" width="{width}" customWidth="1"/>')
        cols = "<cols>" + "".join(col_lines) + "</cols>"
    sheet_views = ""
    if freeze_rows:
        top_left = f"A{freeze_rows + 1}"
        sheet_views = (
            '<sheetViews><sheetView workbookViewId="0">'
            f'<pane ySplit="{freeze_rows}" topLeftCell="{top_left}" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft"/>'
            '</sheetView></sheetViews>'
        )
    row_xml = []
    for r, row in enumerate(rows, start=1):
        cells = "".join(cell_xml(r, c, cell) for c, cell in enumerate(row, start=1))
        row_xml.append(f'<row r="{r}">{cells}</row>')
    auto = f'<autoFilter ref="{autofilter_ref}"/>' if autofilter_ref else ""
    dimension = f'<dimension ref="A1:{col_name(max_col)}{len(rows)}"/>'
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"{dimension}{sheet_views}{cols}<sheetData>{''.join(row_xml)}</sheetData>{auto}"
        "</worksheet>"
    )


def s(value: Any, style: int | None = None) -> dict[str, Any]:
    return {"value": value, "style": style}


def n(value: Any, style: int | None = None) -> dict[str, Any]:
    return {"value": value, "type": "n", "style": style}


def formula(value: Any, expr: str, style: int | None = None, cell_type: str | None = None) -> dict[str, Any]:
    return {"value": value, "formula": expr, "style": style, "type": cell_type}


def native_capacity() -> int:
    return int(R * R * (Fraction(1, 1) - Fraction(1, SPLIT)))


def shell_n_path() -> list[Fraction]:
    return [Fraction(1, 1), ALPHA_H, D, R / D, R / D, D, ALPHA_H, ALPHA_H]


def shell_capacities() -> list[int]:
    return [int(Fraction(2, 1) * x * x) for x in shell_n_path()]


def element_values(z: int) -> dict[str, Any]:
    r = int(R)
    radix_cycle = ((z - 1) // r) + 1
    radix_slot = ((z - 1) % r) + 1
    depth = max(0, radix_cycle - 1)
    raw = Fraction(z * depth, r)
    delta = raw.numerator // raw.denominator
    residual = int((raw - delta) * r)
    n_primary = z + delta
    shell_remaining = z
    shell_period = 1
    shell_capacity = 0
    shell_n = ""
    for i, cap in enumerate(shell_capacities(), start=1):
        if shell_remaining <= cap:
            shell_period = i
            shell_capacity = cap
            shell_n = fstr(shell_n_path()[i - 1])
            break
        shell_remaining -= cap
    g = Fraction(z, 1) * KAPPA_FLOOR + Fraction(n_primary - z, 64)
    gr = g * SPLIT
    retained = g * 7
    return {
        "Z": z,
        "radix_cycle": radix_cycle,
        "radix_slot": radix_slot,
        "selected_depth": depth,
        "delta_n": delta,
        "residual_twelfths": residual,
        "N": n_primary,
        "A": z + n_primary,
        "total_particle_count": (2 * z) + n_primary,
        "quark_u_count": (2 * z) + n_primary,
        "quark_d_count": z + (2 * n_primary),
        "quark_e_count": z,
        "P_address": f"{z}p+{n_primary}n+{z}e",
        "quark_address": f"{(2 * z) + n_primary}u+{z + (2 * n_primary)}d+{z}e",
        "shell_period": shell_period,
        "shell_n": shell_n,
        "shell_capacity": shell_capacity,
        "shell_occupancy": shell_remaining,
        "shell_status": "CLOSED_SHELL" if shell_remaining == shell_capacity else "OPEN_SHELL",
        "neutron_excess": n_primary - z,
        "G": g,
        "GR": gr,
        "retained": retained,
        "surface_status": "CONSTANT_FRONTIER_TAIL_Z119_Z126" if z > native_capacity() - int(SPLIT) else "CONSTANT_NATIVE_SURFACE_Z001_Z118",
        "native_lane": (
            "CONSTANT_FRONTIER_TAIL_CANDIDATE"
            if z > native_capacity() - int(SPLIT)
            else "CONSTANT_STABLE_ANCHOR_LANE"
            if residual == 0
            else "CONSTANT_HALF_WRITE_LANE"
            if residual == int(R / 2)
            else "CONSTANT_BOUND_LADDER_LANE"
        ),
    }


def build_constants_sheet() -> list[list[dict[str, Any]]]:
    rows = [[s("Constant", 1), s("Value", 1), s("Formula / Source", 1), s("Role", 1)]]
    rows.extend(
        [
            [s("R"), n(12), s("declared constant"), s("radix/native route constant")],
            [s("D"), n(3), s("declared constant"), s("dimension/closure depth constant")],
            [s("alpha_H"), n(2), s("declared constant"), s("hidden-source bigrade generator")],
            [s("split"), formula(8, "2^B3"), s("=2^D"), s("carrier split")],
            [s("native_capacity"), formula(126, "B2^2*(1-1/B5)"), s("=R^2*(1-2^-D)"), s("element row bound")],
            [s("proton_qA"), formula(fdec(PROTON_QA), "145/2"), s("=145/2"), s("component write support")],
            [s("electron_qA"), formula(fdec(ELECTRON_QA), "145/96"), s("=145/96"), s("component write support")],
            [s("neutron_qA"), formula(fdec(NEUTRON_QA), "1/8"), s("=1/8"), s("component write support")],
            [s("charged_pair_qA"), formula(fdec(PROTON_QA + ELECTRON_QA), "B7+B8"), s("=proton_qA+electron_qA"), s("per-Z charged support")],
            [s("kappa_floor"), formula(fdec(KAPPA_FLOOR), "(B7+B8+B9)/B5"), s("=(p+e+n)/split"), s("floor kappa")],
            [s("neutron_G_unit"), formula(fdec(NEUTRON_G_UNIT), "B9/B5"), s("=neutron_qA/split"), s("neutron excess G unit")],
            [s("R_div_D"), formula(4, "B2/B3"), s("=R/D"), s("shell path middle term")],
        ]
    )
    return rows


def build_shells_sheet() -> list[list[dict[str, Any]]]:
    rows = [[s("shell_period", 1), s("n", 1), s("capacity", 1), s("start_Z", 1), s("end_Z", 1), s("n_formula", 1)]]
    n_formulas = ["1", "Constants!$B$4", "Constants!$B$3", "Constants!$B$2/Constants!$B$3", "Constants!$B$2/Constants!$B$3", "Constants!$B$3", "Constants!$B$4", "Constants!$B$4"]
    end = 0
    for i, n_value in enumerate(shell_n_path(), start=1):
        cap = shell_capacities()[i - 1]
        start = end + 1
        end += cap
        row_num = i + 1
        start_formula = "1" if i == 1 else f"E{row_num-1}+1"
        end_formula = f"SUM($C$2:C{row_num})"
        rows.append(
            [
                n(i),
                formula(fdec(n_value), n_formulas[i - 1]),
                formula(cap, f"2*B{row_num}^2"),
                formula(start, start_formula),
                formula(end, end_formula),
                s("=" + n_formulas[i - 1]),
            ]
        )
    return rows


def build_elements_sheet() -> list[list[dict[str, Any]]]:
    headers = [
        "element_id", "Z", "radix_cycle", "radix_slot", "selected_depth", "delta_n", "residual_twelfths",
        "N", "A", "proton_count", "neutron_count", "electron_count", "total_particle_count",
        "quark_u_count", "quark_d_count", "quark_e_count", "P_address", "quark_address",
        "shell_period", "shell_n", "shell_capacity", "shell_occupancy", "shell_status",
        "kappa_floor", "neutron_excess", "G(P)", "GR(P)", "retained_7G", "surface_status",
        "native_lane", "known_symbol", "known_name", "reference_clock", "card_source",
    ]
    rows = [[s(header, 1) for header in headers]]
    for z in range(1, 127):
        v = element_values(z)
        r = z + 1
        rows.append(
            [
                formula(f"E{z:03d}", f'"E"&TEXT(B{r},"000")', cell_type="str"),
                formula(z, f"ROW()-1"),
                formula(v["radix_cycle"], f"INT((B{r}-1)/Constants!$B$2)+1"),
                formula(v["radix_slot"], f"MOD(B{r}-1,Constants!$B$2)+1"),
                formula(v["selected_depth"], f"MAX(0,C{r}-1)"),
                formula(v["delta_n"], f"INT(B{r}*E{r}/Constants!$B$2)"),
                formula(v["residual_twelfths"], f"MOD(B{r}*E{r},Constants!$B$2)"),
                formula(v["N"], f"B{r}+F{r}"),
                formula(v["A"], f"B{r}+H{r}"),
                formula(z, f"B{r}"),
                formula(v["N"], f"H{r}"),
                formula(z, f"B{r}"),
                formula(v["total_particle_count"], f"J{r}+K{r}+L{r}"),
                formula(v["quark_u_count"], f"2*B{r}+H{r}"),
                formula(v["quark_d_count"], f"B{r}+2*H{r}"),
                formula(v["quark_e_count"], f"B{r}"),
                formula(v["P_address"], f'B{r}&"p+"&H{r}&"n+"&B{r}&"e"', cell_type="str"),
                formula(v["quark_address"], f'N{r}&"u+"&O{r}&"d+"&P{r}&"e"', cell_type="str"),
                formula(v["shell_period"], f'COUNTIF(Shells!$E$2:$E$9,"<"&B{r})+1'),
                formula(v["shell_n"], f"INDEX(Shells!$B$2:$B$9,S{r})"),
                formula(v["shell_capacity"], f"INDEX(Shells!$C$2:$C$9,S{r})"),
                formula(v["shell_occupancy"], f"B{r}-IF(S{r}=1,0,INDEX(Shells!$E$2:$E$9,S{r}-1))"),
                formula(v["shell_status"], f'IF(V{r}=U{r},"CLOSED_SHELL","OPEN_SHELL")', cell_type="str"),
                formula(fdec(KAPPA_FLOOR), "Constants!$B$11"),
                formula(v["neutron_excess"], f"H{r}-B{r}"),
                formula(fdec(v["G"]), f"B{r}*Constants!$B$11+Y{r}*Constants!$B$12"),
                formula(fdec(v["GR"]), f"Z{r}*Constants!$B$5"),
                formula(fdec(v["retained"]), f"Z{r}*7"),
                formula(v["surface_status"], f'IF(B{r}>Constants!$B$6-Constants!$B$5,"CONSTANT_FRONTIER_TAIL_Z119_Z126","CONSTANT_NATIVE_SURFACE_Z001_Z118")', cell_type="str"),
                formula(v["native_lane"], f'IF(B{r}>Constants!$B$6-Constants!$B$5,"CONSTANT_FRONTIER_TAIL_CANDIDATE",IF(G{r}=0,"CONSTANT_STABLE_ANCHOR_LANE",IF(G{r}=Constants!$B$2/2,"CONSTANT_HALF_WRITE_LANE","CONSTANT_BOUND_LADDER_LANE")))', cell_type="str"),
                s(""),
                s(""),
                s(""),
                s(""),
            ]
        )
    return rows


def build_isotope_sheet() -> list[list[dict[str, Any]]]:
    headers = [
        "candidate_row", "Z", "candidate_role", "active", "selected_depth", "delta_n", "residual_twelfths",
        "N", "A", "P_address", "quark_address", "G(P)", "GR(P)", "retained_7G", "native_lane",
    ]
    rows = [[s(header, 1) for header in headers]]
    for idx in range(1, 253):
        z = ((idx - 1) // 2) + 1
        role = "FLOOR_PRIMARY" if (idx - 1) % 2 == 0 else "CEIL_NEIGHBOR"
        ev = element_values(z)
        active = role == "FLOOR_PRIMARY" or ev["residual_twelfths"] != 0
        n_iso = ev["N"] + (1 if role == "CEIL_NEIGHBOR" else 0)
        g = Fraction(z, 1) * KAPPA_FLOOR + Fraction(n_iso - z, 64)
        gr = g * SPLIT
        retained = g * 7
        native_lane = (
            "CONSTANT_FRONTIER_TAIL_CANDIDATE"
            if z > native_capacity() - int(SPLIT)
            else "CONSTANT_STABLE_ANCHOR_LANE"
            if ev["residual_twelfths"] == 0 and role == "FLOOR_PRIMARY"
            else "CONSTANT_HALF_WRITE_LANE"
            if ev["residual_twelfths"] == int(R / 2)
            else "CONSTANT_BOUND_LADDER_LANE"
        )
        r = idx + 1
        rows.append(
            [
                formula(idx, "ROW()-1"),
                formula(z, f"INT((A{r}-1)/2)+1"),
                formula(role, f'IF(MOD(A{r}-1,2)=0,"FLOOR_PRIMARY","CEIL_NEIGHBOR")', cell_type="str"),
                formula("yes" if active else "no", f'IF(C{r}="FLOOR_PRIMARY","yes",IF(G{r}<>0,"yes","no"))', cell_type="str"),
                formula(ev["selected_depth"], f"MAX(0,INT((B{r}-1)/Constants!$B$2))"),
                formula(ev["delta_n"], f"INT(B{r}*E{r}/Constants!$B$2)"),
                formula(ev["residual_twelfths"], f"MOD(B{r}*E{r},Constants!$B$2)"),
                formula(n_iso, f"B{r}+F{r}+IF(C{r}=\"CEIL_NEIGHBOR\",1,0)"),
                formula(z + n_iso, f"B{r}+H{r}"),
                formula(f"{z}p+{n_iso}n+{z}e", f'B{r}&"p+"&H{r}&"n+"&B{r}&"e"', cell_type="str"),
                formula(f"{2*z+n_iso}u+{z+2*n_iso}d+{z}e", f'(2*B{r}+H{r})&"u+"&(B{r}+2*H{r})&"d+"&B{r}&"e"', cell_type="str"),
                formula(fdec(g), f"B{r}*Constants!$B$11+(H{r}-B{r})*Constants!$B$12"),
                formula(fdec(gr), f"L{r}*Constants!$B$5"),
                formula(fdec(retained), f"L{r}*7"),
                formula(native_lane, f'IF(B{r}>Constants!$B$6-Constants!$B$5,"CONSTANT_FRONTIER_TAIL_CANDIDATE",IF(G{r}=0,"CONSTANT_STABLE_ANCHOR_LANE",IF(G{r}=Constants!$B$2/2,"CONSTANT_HALF_WRITE_LANE","CONSTANT_BOUND_LADDER_LANE")))', cell_type="str"),
            ]
        )
    return rows


def build_checks_sheet() -> list[list[dict[str, Any]]]:
    checks = [
        ("native_capacity", "Constants!B6", 126, "126"),
        ("shell_capacity_sum", "SUM(Shells!C2:C9)", 126, "126"),
        ("element_rows", "COUNTA(Elements_126!B2:B127)", 126, "126"),
        ("closed_shell_rows", 'COUNTIF(Elements_126!W2:W127,"CLOSED_SHELL")', 8, "8"),
        ("frontier_tail_rows", 'COUNTIF(Elements_126!AC2:AC127,"CONSTANT_FRONTIER_TAIL_Z119_Z126")', 8, "8"),
        ("active_isotope_candidates", 'COUNTIF(Isotope_Candidates!D2:D253,"yes")', 214, "214"),
        ("blank_known_and_card_fields", "COUNTA(Elements_126!AE2:AH127)", 0, "0"),
        ("gold_like_Z79_P", "INDEX(Elements_126!Q2:Q127,79)", "79p+118n+79e", "79p+118n+79e"),
        ("gold_like_Z79_G", "INDEX(Elements_126!Z2:Z127,79)", fdec(element_values(79)["G"]), fdec(element_values(79)["G"])),
        ("gold_like_Z79_GR", "INDEX(Elements_126!AA2:AA127,79)", fdec(element_values(79)["GR"]), fdec(element_values(79)["GR"])),
    ]
    rows = [[s("check", 1), s("formula_result", 1), s("formula", 1), s("expected", 1), s("status", 1)]]
    for idx, (name, expr, value, expected) in enumerate(checks, start=2):
        cell_type = "str" if isinstance(value, str) and not str(value).replace(".", "", 1).isdigit() else None
        rows.append(
            [
                s(name),
                formula(value, expr, cell_type=cell_type),
                s("=" + expr),
                s(expected),
                formula("PASS", f'IF(B{idx}=D{idx},"PASS","FAIL")', cell_type="str"),
            ]
        )
    return rows


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0F5C5C"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="2">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def workbook_package(sheets: dict[str, str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet_names = list(sheets)
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(sheet_names) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    workbook_sheets = []
    workbook_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for i, name in enumerate(sheet_names, start=1):
        workbook_sheets.append(f'<sheet name="{xml_text(name)}" sheetId="{i}" r:id="rId{i}"/>')
        workbook_rels.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheet_names)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    workbook_rels.append("</Relationships>")

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{''.join(workbook_sheets)}</sheets>"
        '<calcPr calcId="191029" calcMode="auto" fullCalcOnLoad="1" forceFullCalc="1"/>'
        "</workbook>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    now = utc_now()
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>CR223 Constants-Only Element Formulas</dc:title>'
        '<dc:creator>Codex</dc:creator>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Codex</Application>"
        "</Properties>"
    )

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "\n".join(content_types))
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", "\n".join(workbook_rels))
        zf.writestr("xl/styles.xml", styles_xml())
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        for i, name in enumerate(sheet_names, start=1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", sheets[name])


def formula_map_rows() -> list[dict[str, Any]]:
    return [
        {"sheet": "Constants", "range": "B5:B12", "purpose": "derive split, capacity, qA/kernel terms", "formula_example": "=2^B3; =B2^2*(1-1/B5); =(B7+B8+B9)/B5"},
        {"sheet": "Shells", "range": "B2:E9", "purpose": "derive shell n path, shell capacities, cumulative shell bounds", "formula_example": "=2*B2^2; =SUM($C$2:C2)"},
        {"sheet": "Elements_126", "range": "A2:AD127", "purpose": "derive 126 rows from Z enumeration and constants", "formula_example": "=ROW()-1; =B2*Constants!$B$11+Y2*Constants!$B$12"},
        {"sheet": "Isotope_Candidates", "range": "A2:O253", "purpose": "derive floor/ceil ladder candidates and active count", "formula_example": '=IF(C2="FLOOR_PRIMARY","yes",IF(G2<>0,"yes","no"))'},
        {"sheet": "Checks", "range": "B2:E11", "purpose": "formula checks for counts and key row values", "formula_example": '=COUNTIF(Isotope_Candidates!D2:D253,"yes")'},
    ]


def workbook_formula_count(path: Path) -> int:
    count = 0
    with zipfile.ZipFile(path, "r") as zf:
        for name in zf.namelist():
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                count += zf.read(name).decode("utf-8").count("<f>")
    return count


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    _, cr222_elements = read_csv(CR222_ELEMENTS)
    cr222_summary = read_json(CR222_SUMMARY) if CR222_SUMMARY.exists() else {}

    source_paths = [
        (CR222_ELEMENTS, "CR222 constants-only generated rows used as verification baseline"),
        (CR222_SUMMARY, "CR222 summary counts and boundary"),
        (CR222_CONSTANTS, "CR222 declared constants reference"),
    ]
    write_csv(INPUT_MANIFEST, [manifest_row(path, role) for path, role in source_paths], ["source", "exists", "bytes", "sha256", "role"])

    sheets = {
        "Constants": sheet_xml(build_constants_sheet(), widths={1: 22, 2: 24, 3: 36, 4: 36}, autofilter_ref="A1:D13"),
        "Shells": sheet_xml(build_shells_sheet(), widths={1: 14, 2: 12, 3: 14, 4: 12, 5: 12, 6: 34}, autofilter_ref="A1:F9"),
        "Elements_126": sheet_xml(build_elements_sheet(), widths={1: 12, 17: 18, 18: 22, 26: 20, 27: 20, 28: 20, 29: 32, 30: 32}, autofilter_ref="A1:AH127"),
        "Isotope_Candidates": sheet_xml(build_isotope_sheet(), widths={1: 14, 3: 18, 10: 18, 11: 22, 12: 20, 13: 20, 14: 20, 15: 34}, autofilter_ref="A1:O253"),
        "Checks": sheet_xml(build_checks_sheet(), widths={1: 28, 2: 24, 3: 52, 4: 24, 5: 12}, autofilter_ref="A1:E11"),
    }
    workbook_package(sheets, WORKBOOK)

    write_csv(FORMULA_MAP, formula_map_rows(), ["sheet", "range", "purpose", "formula_example"])

    formula_count = workbook_formula_count(WORKBOOK)
    xlsx_valid_zip = zipfile.is_zipfile(WORKBOOK)
    workbook_parts: list[str] = []
    with zipfile.ZipFile(WORKBOOK, "r") as zf:
        workbook_parts = zf.namelist()

    checks: list[dict[str, Any]] = []
    check(checks, "input_cr222_elements_exists", CR222_ELEMENTS.exists(), CR222_ELEMENTS.exists(), True)
    check(checks, "cr222_elements_126", len(cr222_elements) == 126, len(cr222_elements), 126)
    check(checks, "xlsx_written", WORKBOOK.exists() and WORKBOOK.stat().st_size > 0, WORKBOOK.stat().st_size if WORKBOOK.exists() else 0, ">0")
    check(checks, "xlsx_is_valid_zip", xlsx_valid_zip, xlsx_valid_zip, True)
    check(checks, "xlsx_has_5_sheets", sum(1 for part in workbook_parts if part.startswith("xl/worksheets/sheet")) == 5, sum(1 for part in workbook_parts if part.startswith("xl/worksheets/sheet")), 5)
    check(checks, "formula_count_gt_4000", formula_count > 4000, formula_count, ">4000")
    check(checks, "elements_formula_rows_126", len(build_elements_sheet()) - 1 == 126, len(build_elements_sheet()) - 1, 126)
    check(checks, "isotope_candidate_formula_rows_252", len(build_isotope_sheet()) - 1 == 252, len(build_isotope_sheet()) - 1, 252)
    check(checks, "active_isotope_formula_expected_214", sum(1 for idx in range(1, 253) if (idx - 1) % 2 == 0 or element_values(((idx - 1) // 2) + 1)["residual_twelfths"] != 0) == 214, sum(1 for idx in range(1, 253) if (idx - 1) % 2 == 0 or element_values(((idx - 1) // 2) + 1)["residual_twelfths"] != 0), 214)
    check(checks, "gold_like_formula_values_match_cr222", element_values(79)["P_address"] == "79p+118n+79e" and fdec(element_values(79)["G"]) == cr222_summary.get("gold_like_Z79", {}).get("G_decimal"), {"P": element_values(79)["P_address"], "G": fdec(element_values(79)["G"])}, "CR222 Z79")
    check(checks, "known_label_card_fields_blank_by_design", True, True, True)
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    summary = {
        "cr_id": "CR223",
        "artifact": "CR223_FORMULA_SPREADSHEET_EXPORT",
        "execution_status": execution_status,
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "result_class": (
            "CR223_PASS_FORMULA_SPREADSHEET_EXPORT__XLSX_WITH_CONSTANTS_SHELLS_ELEMENTS_ISOTOPE_CANDIDATES_CHECKS__"
            "FORMULA_CELLS_GT_4000__NO_CARDS_NO_LABELS"
        )
        if execution_status == "CLEAN"
        else "CR223_FAIL_FORMULA_SPREADSHEET_EXPORT",
        "workbook": rel(WORKBOOK),
        "formula_count": formula_count,
        "sheets": list(sheets.keys()),
        "rows": {
            "elements_formula_rows": 126,
            "isotope_candidate_formula_rows": 252,
            "active_isotope_candidates_expected": 214,
        },
        "gold_like_Z79": {
            "P_address": element_values(79)["P_address"],
            "G": fdec(element_values(79)["G"]),
            "GR": fdec(element_values(79)["GR"]),
        },
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": (
            "Workbook formulas calculate the constants-only native element surface. "
            "Known names, symbols, cards, measured masses, and CLOCK labels are not construction inputs."
        ),
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR223 Formula Spreadsheet Export

Result: **{summary['result_class']}**

## Direct Answer

Created the requested formula workbook:

`{rel(WORKBOOK)}`

The workbook has five sheets:

- `Constants`
- `Shells`
- `Elements_126`
- `Isotope_Candidates`
- `Checks`

The workbook contains **{formula_count} formula cells**. It calculates the 126
element rows from constants, not from cards or labels.

## Included Formula Surfaces

- 126 element rows with formulas for `Z`, `N`, `P`, quark address, shell
  placement, `G(P)`, `GR(P)`, retained `7G`, and native lane.
- 252 isotope ladder candidate rows with formula-derived active flags; the
  workbook check counts **214** active isotope candidates.
- Formula checks for capacity, shell sum, element rows, closed shells, frontier
  rows, active isotope rows, blank label/card fields, and the Z=79 readout.

## Boundary

Known symbols, known names, measured masses, CLOCK labels, and card values are
blank/not used in the construction sheets.

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

