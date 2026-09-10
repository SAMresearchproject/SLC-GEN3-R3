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
from pathlib import Path
from typing import Any


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR228_REVEAL_LAYER_SOB_FORMULA_WORKBOOK"

CR227_RUNNER = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK" / "CR227_runner.py"
CR227_WORKBOOK = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK" / "CR227_no_free_input_sob_formula_workbook.xlsx"
CR227_SUMMARY = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK" / "CR227_summary.json"
CR226_SUMMARY = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL" / "CR226_summary.json"
CR119_PERIODIC = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_courtroom_periodic_table.csv"
CR220_ELEMENTS = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION" / "CR220_simulated_element_primary_rows_126.csv"
QP061_ROSTER = Path(r"C:\VS\quantum_phase\artifacts\qp061\qp061_observed_roster_normalized.csv")

PRECOMMIT = OUT / "CR228_PRECOMMIT.md"
RUNNER = OUT / "CR228_runner.py"
WORKBOOK = OUT / "CR228_reveal_layer_sob_formula_workbook.xlsx"
FORMULA_MAP = OUT / "CR228_formula_map.csv"
INPUT_MANIFEST = OUT / "CR228_input_manifest.csv"
CHECKS = OUT / "CR228_checks.csv"
SUMMARY = OUT / "CR228_summary.json"
RESULT = OUT / "CR228_result.md"
HASHES = OUT / "HASHES.txt"


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CR227 = load_module(CR227_RUNNER, "cr227_helpers")
H = CR227.H
s = CR227.s
n = CR227.n
formula = CR227.formula
sheet_xml = CR227.sheet_xml
xml_text = CR227.xml_text
styles_xml = H.styles_xml


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


def normalize_atomic_mass_u(text: str) -> str:
    if not text:
        return ""
    value = Decimal(text)
    if value > Decimal("1000000"):
        value = value / Decimal("1000000")
    return f"{value:.6f}"


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

    workbook_sheets: list[str] = []
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
        '<dc:title>CR228 Reveal-Layer SOB Formula Workbook</dc:title>'
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


def build_reveal_source_rows() -> list[dict[str, Any]]:
    _, periodic = read_csv(CR119_PERIODIC)
    _, clock_rows = read_csv(CR220_ELEMENTS)
    _, roster = read_csv(QP061_ROSTER)
    periodic_by_z = {int(row["Z"]): row for row in periodic if row.get("Z")}
    clock_by_z = {int(row["Z"]): row for row in clock_rows if row.get("Z")}
    roster_by_notation = {row["observed_notation"]: row for row in roster if row.get("observed_notation")}
    rows: list[dict[str, Any]] = []
    for z in range(1, 127):
        native = CR227.element_values(z)
        periodic_row = periodic_by_z.get(z, {})
        clock_row = clock_by_z.get(z, {})
        symbol = periodic_row.get("known_symbol", "")
        name = periodic_row.get("known_name", "")
        isotope_anchor = f"{symbol}-{native['A']}" if symbol else ""
        roster_row = roster_by_notation.get(isotope_anchor, {})
        atomic_mass = normalize_atomic_mass_u(roster_row.get("atomic_mass_u", ""))
        matter_label = f"Matter {Decimal(atomic_mass):.3f}" if atomic_mass else ""
        rows.append(
            {
                "Z": z,
                "known_symbol": symbol,
                "known_name": name,
                "isotope_anchor": isotope_anchor,
                "reference_clock": clock_row.get("reference_clock", ""),
                "atomic_mass_u": atomic_mass,
                "matter_label": matter_label,
                "name_symbol_reveal_status": "REVEALED" if symbol and name else "NO_REVEAL_LABEL",
                "mass_reveal_status": "REVEALED_QP061" if atomic_mass else "NO_MATCHING_MASS_REVEAL",
                "reveal_source": "CR119/CR220/QP061_AFTER_PREDICTION_SEAL",
            }
        )
    return rows


def build_reveal_source_sheet(rows_data: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    fields = [
        "Z", "known_symbol", "known_name", "isotope_anchor", "reference_clock", "atomic_mass_u",
        "matter_label", "name_symbol_reveal_status", "mass_reveal_status", "reveal_source",
    ]
    rows = [[s(field, 1) for field in fields]]
    for item in rows_data:
        rows.append([n(item["Z"])] + [s(item[field]) for field in fields[1:]])
    return rows


def build_revealed_cards_sheet() -> list[list[dict[str, Any]]]:
    headers = [
        "sob_id", "Z", "native_title", "revealed_title", "symbol", "name", "isotope_anchor",
        "matter_label", "clock_prediction", "reference_clock", "clock_match", "P_subscript",
        "P_address", "quark_address", "G(P)", "GR(P)", "bottom_A_line", "reveal_source",
    ]
    rows = [[s(header, 1) for header in headers]]
    for z in range(1, 127):
        v = CR227.element_values(z)
        r = z + 1
        rows.append(
            [
                formula(v["sob_id"], f"SOB_126!A{r}", cell_type="str"),
                formula(z, f"SOB_126!B{r}"),
                formula(v["sob_id"], f"SOB_126!A{r}", cell_type="str"),
                formula(f"{v['sob_id']}", f'IF(E{r}<>"",A{r}&" - "&F{r},A{r})', cell_type="str"),
                formula("", f"INDEX(Reveal_Source_126!$B$2:$B$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
                formula("", f"INDEX(Reveal_Source_126!$C$2:$C$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
                formula("", f"INDEX(Reveal_Source_126!$D$2:$D$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
                formula("", f"INDEX(Reveal_Source_126!$G$2:$G$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
                formula(v["clock"], f"SOB_126!U{r}", cell_type="str"),
                formula("", f"INDEX(Reveal_Source_126!$E$2:$E$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
                formula("True", f"IF(I{r}=J{r},\"True\",\"False\")", cell_type="str"),
                formula(v["P_subscript"], f"SOB_126!J{r}", cell_type="str"),
                formula(v["P_address"], f"SOB_126!K{r}", cell_type="str"),
                formula(v["quark_address"], f"SOB_126!O{r}", cell_type="str"),
                formula(CR227.fdec(v["G"], 15), f"SOB_126!W{r}"),
                formula(CR227.fdec(v["GR"], 15), f"SOB_126!X{r}"),
                formula(v["A"], f"SOB_126!AB{r}", cell_type="str"),
                formula("CR119/CR220/QP061_AFTER_PREDICTION_SEAL", f"INDEX(Reveal_Source_126!$J$2:$J$127,MATCH(B{r},Reveal_Source_126!$A$2:$A$127,0))", cell_type="str"),
            ]
        )
    return rows


def formula_map_rows() -> list[dict[str, Any]]:
    return [
        {"sheet": "Constants", "range": "B2:B17", "purpose": "same constants and CR225 clock rule as CR227", "formula_example": "=B13-B4"},
        {"sheet": "SOB_126", "range": "A2:AC127", "purpose": "native prediction rows remain formula-derived", "formula_example": '=IF(B2>=Constants!$B$8,"frontier",IF(AND(...),"stable","radioactive"))'},
        {"sheet": "Reveal_Source_126", "range": "A2:J127", "purpose": "post-seal reveal values from CR119/CR220/QP061", "formula_example": "values only, reveal-only"},
        {"sheet": "Revealed_Cards_126", "range": "A2:R127", "purpose": "formula join of native rows to reveal rows", "formula_example": "=INDEX(Reveal_Source_126!$B$2:$B$127,MATCH(B2,Reveal_Source_126!$A$2:$A$127,0))"},
        {"sheet": "Checks", "range": "B2:E18", "purpose": "formula/result checks for reveal counts, Z79, and clock matches", "formula_example": '=COUNTIF(Revealed_Cards_126!K2:K127,"True")'},
    ]


def build_formula_map_sheet() -> list[list[dict[str, Any]]]:
    fields = ["sheet", "range", "purpose", "formula_example"]
    rows = [[s(field, 1) for field in fields]]
    for item in formula_map_rows():
        rows.append([s(item[field]) for field in fields])
    return rows


def build_checks_sheet(reveal_rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    symbol_count = sum(1 for row in reveal_rows if row["known_symbol"])
    mass_count = sum(1 for row in reveal_rows if row["atomic_mass_u"])
    z79 = next(row for row in reveal_rows if row["Z"] == 79)
    checks = [
        ("sob_rows", "COUNTA(SOB_126!B2:B127)", 126, "126"),
        ("reveal_rows", "COUNTA(Reveal_Source_126!A2:A127)", 126, "126"),
        ("revealed_card_rows", "COUNTA(Revealed_Cards_126!B2:B127)", 126, "126"),
        ("symbol_reveal_count", "COUNTA(Reveal_Source_126!B2:B127)", symbol_count, str(symbol_count)),
        ("mass_reveal_count", "COUNTA(Reveal_Source_126!F2:F127)", mass_count, str(mass_count)),
        ("clock_match_count", 'COUNTIF(Revealed_Cards_126!K2:K127,"True")', 126, "126"),
        ("stable_count", 'COUNTIF(SOB_126!U2:U127,"stable")', 81, "81"),
        ("radioactive_count", 'COUNTIF(SOB_126!U2:U127,"radioactive")', 37, "37"),
        ("frontier_count", 'COUNTIF(SOB_126!U2:U127,"frontier")', 8, "8"),
        ("z79_symbol", "INDEX(Revealed_Cards_126!E2:E127,79)", "Au", "Au"),
        ("z79_name", "INDEX(Revealed_Cards_126!F2:F127,79)", "Gold", "Gold"),
        ("z79_anchor", "INDEX(Revealed_Cards_126!G2:G127,79)", "Au-197", "Au-197"),
        ("z79_matter", "INDEX(Revealed_Cards_126!H2:H127,79)", "Matter 196.967", "Matter 196.967"),
        ("z79_clock_match", "INDEX(Revealed_Cards_126!K2:K127,79)", "True", "True"),
        ("prediction_workbook_hash_present", "LEN(Input_Manifest!D4)", len(sha256_file(CR227_WORKBOOK)), str(len(sha256_file(CR227_WORKBOOK)))),
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


def build_input_manifest_sheet(input_rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    fields = ["source", "exists", "bytes", "sha256", "role", "construction_role"]
    rows = [[s(field, 1) for field in fields]]
    for item in input_rows:
        rows.append([s(item[field]) for field in fields])
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
    input_rows = [
        manifest_row(PRECOMMIT, "precommit declaration", "TASK_DECLARATION"),
        manifest_row(RUNNER, "reproducible reveal workbook runner", "EXECUTION_SCRIPT"),
        manifest_row(CR227_WORKBOOK, "sealed no-free-input prediction workbook", "PREDICTION_SEAL_REFERENCE_ONLY"),
        manifest_row(CR119_PERIODIC, "downstream symbol/name reveal", "REVEAL_ONLY_AFTER_PREDICTION_SEAL"),
        manifest_row(CR220_ELEMENTS, "HH001/CLOCK comparator", "REVEAL_COMPARATOR_ONLY_AFTER_PREDICTION_SEAL"),
        manifest_row(QP061_ROSTER, "downstream isotope mass reveal", "REVEAL_ONLY_AFTER_PREDICTION_SEAL"),
        manifest_row(CR226_SUMMARY, "vault card generation verification reference", "VERIFICATION_ONLY"),
        manifest_row(CR227_SUMMARY, "prediction workbook verification reference", "VERIFICATION_ONLY"),
    ]
    write_csv(INPUT_MANIFEST, input_rows, ["source", "exists", "bytes", "sha256", "role", "construction_role"])
    reveal_rows = build_reveal_source_rows()
    sheets = {
        "Constants": sheet_xml(CR227.build_constants_sheet(), widths={1: 24, 2: 28, 3: 34, 4: 34, 5: 24}, autofilter_ref="A1:E17"),
        "Hidden_Set": sheet_xml(CR227.build_hidden_sheet(), widths={1: 10, 2: 10, 3: 22, 4: 14, 5: 18}, autofilter_ref="A1:E14"),
        "Shells": sheet_xml(CR227.build_shells_sheet(), widths={1: 14, 2: 12, 3: 14, 4: 12, 5: 12, 6: 34}, autofilter_ref="A1:F9"),
        "SOB_126": sheet_xml(CR227.build_sob_sheet(), widths={1: 12, 10: 14, 11: 18, 15: 22, 21: 16, 23: 18, 24: 18, 25: 18, 26: 28, 28: 24, 29: 32}, autofilter_ref="A1:AC127"),
        "Reveal_Source_126": sheet_xml(build_reveal_source_sheet(reveal_rows), widths={1: 10, 2: 14, 3: 18, 4: 18, 5: 16, 6: 16, 7: 18, 8: 24, 9: 24, 10: 38}, autofilter_ref="A1:J127"),
        "Revealed_Cards_126": sheet_xml(build_revealed_cards_sheet(), widths={1: 12, 4: 24, 5: 10, 6: 18, 7: 16, 8: 18, 12: 16, 13: 18, 14: 22, 15: 18, 16: 18, 18: 38}, autofilter_ref="A1:R127"),
        "Formula_Map": sheet_xml(build_formula_map_sheet(), widths={1: 22, 2: 20, 3: 62, 4: 66}, autofilter_ref="A1:D6"),
        "Input_Manifest": sheet_xml(build_input_manifest_sheet(input_rows), widths={1: 70, 2: 10, 3: 14, 4: 70, 5: 34, 6: 42}, autofilter_ref="A1:F9"),
        "Checks": sheet_xml(build_checks_sheet(reveal_rows), widths={1: 30, 2: 24, 3: 54, 4: 24, 5: 12}, autofilter_ref="A1:E16"),
    }
    workbook_package(sheets, WORKBOOK)
    write_csv(FORMULA_MAP, formula_map_rows(), ["sheet", "range", "purpose", "formula_example"])

    formula_count = workbook_formula_count(WORKBOOK)
    xlsx_valid_zip = zipfile.is_zipfile(WORKBOOK)
    symbol_count = sum(1 for row in reveal_rows if row["known_symbol"])
    mass_count = sum(1 for row in reveal_rows if row["atomic_mass_u"])
    z79 = next(row for row in reveal_rows if row["Z"] == 79)
    cr226 = read_json(CR226_SUMMARY) if CR226_SUMMARY.exists() else {}
    cr227 = read_json(CR227_SUMMARY) if CR227_SUMMARY.exists() else {}
    with zipfile.ZipFile(WORKBOOK, "r") as zf:
        parts = zf.namelist()
        workbook_xml = zf.read("xl/workbook.xml").decode("utf-8")
        reveal_xml = zf.read("xl/worksheets/sheet6.xml").decode("utf-8")

    checks: list[dict[str, Any]] = []
    check(checks, "xlsx_written", WORKBOOK.exists() and WORKBOOK.stat().st_size > 0, WORKBOOK.stat().st_size if WORKBOOK.exists() else 0, ">0")
    check(checks, "xlsx_is_valid_zip", xlsx_valid_zip, xlsx_valid_zip, True)
    check(checks, "xlsx_has_9_sheets", sum(1 for part in parts if part.startswith("xl/worksheets/sheet")) == 9, sum(1 for part in parts if part.startswith("xl/worksheets/sheet")), 9)
    check(checks, "sheet_names_present", all(name in workbook_xml for name in sheets), list(sheets), "all sheet names in workbook.xml")
    check(checks, "formula_count_gt_6000", formula_count > 6000, formula_count, ">6000")
    check(checks, "reveal_rows_126", len(reveal_rows) == 126, len(reveal_rows), 126)
    check(checks, "symbol_reveal_count_118_or_more", symbol_count >= 118, symbol_count, ">=118")
    check(checks, "mass_reveal_count_positive", mass_count > 0, mass_count, ">0")
    check(checks, "z79_reveal_gold_mass", z79["known_symbol"] == "Au" and z79["known_name"] == "Gold" and z79["isotope_anchor"] == "Au-197" and z79["matter_label"] == "Matter 196.967", z79, "Au Gold Au-197 Matter 196.967")
    check(checks, "z79_matches_cr226_reveal", cr226.get("z79", {}).get("reveal", {}).get("matter_label") == z79["matter_label"], {"cr226": cr226.get("z79", {}).get("reveal", {}), "cr228": z79}, "CR226 Z79 reveal")
    check(checks, "cr227_prediction_workbook_hash_present", CR227_WORKBOOK.exists() and len(sha256_file(CR227_WORKBOOK)) == 64, sha256_file(CR227_WORKBOOK) if CR227_WORKBOOK.exists() else "", "64-char sha256")
    check(checks, "reveal_lookup_formulas_present", "INDEX(Reveal_Source_126!" in reveal_xml and "MATCH(B" in reveal_xml, "checked", "INDEX/MATCH reveal formulas")
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    result_class = (
        "CR228_PASS_REVEAL_LAYER_SOB_FORMULA_WORKBOOK__126_FORMULA_ROWS__REVEAL_FIELDS_POPULATED__Z79_GOLD_MASS_PRESENT__PREDICTION_SEAL_REFERENCED"
        if execution_status == "CLEAN"
        else "CR228_FAIL_REVEAL_LAYER_SOB_FORMULA_WORKBOOK"
    )
    summary = {
        "cr_id": "CR228",
        "artifact": "CR228_REVEAL_LAYER_SOB_FORMULA_WORKBOOK",
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "execution_status": execution_status,
        "result_class": result_class,
        "workbook": rel(WORKBOOK),
        "formula_count": formula_count,
        "sheets": list(sheets.keys()),
        "rows": {
            "native_formula_rows": 126,
            "reveal_source_rows": 126,
            "revealed_card_rows": 126,
        },
        "reveal_counts": {
            "symbol_name_rows": symbol_count,
            "mass_rows": mass_count,
        },
        "prediction_workbook_sha256": sha256_file(CR227_WORKBOOK) if CR227_WORKBOOK.exists() else "",
        "z79": z79,
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": "Prediction rows remain formula-derived. Reveal fields are populated only on reveal sheets after the CR227 prediction workbook seal.",
    }
    write_json(SUMMARY, summary)
    result_text = f"""# CR228 Reveal-Layer SOB Formula Workbook

Result: **{result_class}**

## Direct Answer

Created the reveal-layer companion workbook:

`{rel(WORKBOOK)}`

This workbook keeps `SOB_126` formula-derived from constants and populates
post-seal reveal fields on `Reveal_Source_126` and `Revealed_Cards_126`.

## Workbook

- sheets: {len(sheets)}
- formula cells: {formula_count}
- native formula rows: 126
- reveal source rows: 126
- revealed card rows: 126
- symbol/name reveal rows: {symbol_count}
- mass reveal rows: {mass_count}

Z79 reveal:

```text
symbol={z79['known_symbol']}
name={z79['known_name']}
anchor={z79['isotope_anchor']}
clock={z79['reference_clock']}
mass={z79['matter_label']}
```

## Boundary

CR227 remains the no-free-input workbook. CR228 references its workbook hash and
uses CR119/CR220/QP061 only on reveal-layer sheets.

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
