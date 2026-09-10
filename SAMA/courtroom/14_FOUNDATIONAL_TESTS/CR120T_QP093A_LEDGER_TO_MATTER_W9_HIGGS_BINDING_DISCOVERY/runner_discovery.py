"""CR120T discovery runner.

This process is intentionally target-aware for workbook/F81 discovery and
observation-blind to CR261 test observations. It emits candidates but does not
freeze or validate them.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRECOMMIT = HERE / "PRECOMMIT_DISCOVERY.md"
PRECOMMIT_HASH = "9fde0cc6781ddd35e418ca14bbfbb3d44b2e10435bf7f5be587e48150107337c"
MANIFEST = HERE / "SOURCE_MANIFEST.json"
MANIFEST_HASH = "b1eee6ab1603c7a3ed5995afb5e1b3061b17f1c8aafce11d7db0f675a7769451"

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": NS_MAIN, "r": NS_REL_DOC}

PARSED_INPUTS: set[str] = set()
HASHED_INPUTS: set[str] = set()


def sha256(path: Path) -> str:
    HASHED_INPUTS.add(str(path.resolve()))
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    PARSED_INPUTS.add(str(path.resolve()))
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def source_path(entry: dict) -> Path:
    p = Path(entry["path"])
    return p if p.is_absolute() else ROOT / p


def dump_json(name: str, obj) -> None:
    (HERE / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(name: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)
    with (HERE / name).open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def frac(value) -> Fraction:
    if value is None or value == "":
        return Fraction(0)
    return Fraction(str(value))


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def decimal_str(value: Fraction, places: int = 12) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    s = f"{float(value):.{places}f}".rstrip("0").rstrip(".")
    return s


def col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def normalize_target(target: str) -> str:
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return target.lstrip("/")
    return target if target.startswith("xl/") else "xl/" + target


def cell_value(cell: ET.Element, shared: list[str]) -> tuple[str, str]:
    t = cell.attrib.get("t", "")
    formula = cell.findtext(f"{{{NS_MAIN}}}f") or ""
    v = cell.findtext(f"{{{NS_MAIN}}}v")
    if t == "inlineStr":
        texts = [x.text or "" for x in cell.findall(f".//{{{NS_MAIN}}}t")]
        return "".join(texts), formula
    if v is None:
        return "", formula
    if t == "s":
        try:
            return shared[int(v)], formula
        except (ValueError, IndexError):
            return v, formula
    if t == "b":
        return "TRUE" if v == "1" else "FALSE", formula
    return v, formula


def parse_workbook(path: Path) -> dict:
    PARSED_INPUTS.add(str(path.resolve()))
    out = {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "package_entries": 0,
        "macro_or_binary_parts": [],
        "sheets": {},
        "tables": [],
        "comments_parts": [],
    }
    with zipfile.ZipFile(path, "r") as z:
        names = z.namelist()
        out["package_entries"] = len(names)
        out["macro_or_binary_parts"] = [n for n in names if n.endswith(("vbaProject.bin", ".bin"))]
        out["comments_parts"] = [n for n in names if "comments" in n.lower()]

        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join((t.text or "") for t in si.findall(".//m:t", NS)))

        wb = ET.fromstring(z.read("xl/workbook.xml"))
        relroot = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rels = {
            r.attrib["Id"]: normalize_target(r.attrib["Target"])
            for r in relroot.findall(f"{{{NS_REL_PKG}}}Relationship")
        }
        for s in wb.findall("m:sheets/m:sheet", NS):
            name = s.attrib["name"]
            rid = s.attrib[f"{{{NS_REL_DOC}}}id"]
            xml_path = rels[rid]
            root = ET.fromstring(z.read(xml_path))
            dim_node = root.find("m:dimension", NS)
            dim = dim_node.attrib.get("ref", "") if dim_node is not None else ""
            cells: dict[str, dict[str, str]] = {}
            rows: dict[int, dict[int, str]] = defaultdict(dict)
            hidden_rows: list[int] = []
            hidden_cols: list[str] = []
            for cnode in root.findall("m:cols/m:col", NS):
                if cnode.attrib.get("hidden") == "1":
                    hidden_cols.append(f"{cnode.attrib.get('min')}:{cnode.attrib.get('max')}")
            for rnode in root.findall("m:sheetData/m:row", NS):
                rnum = int(rnode.attrib.get("r", "0"))
                if rnode.attrib.get("hidden") == "1":
                    hidden_rows.append(rnum)
                for cnode in rnode.findall("m:c", NS):
                    ref = cnode.attrib["r"]
                    value, formula = cell_value(cnode, shared)
                    cells[ref] = {"value": value, "formula": formula, "type": cnode.attrib.get("t", "")}
                    rows[rnum][col_index(ref)] = value
            out["sheets"][name] = {
                "state": s.attrib.get("state", "visible"),
                "dimension": dim,
                "xml_path": xml_path,
                "cells": cells,
                "rows": {str(k): v for k, v in rows.items()},
                "hidden_rows": hidden_rows,
                "hidden_columns": hidden_cols,
                "formula_count": sum(1 for x in cells.values() if x["formula"]),
                "nonempty_cell_count": sum(1 for x in cells.values() if x["value"] != "" or x["formula"]),
            }
        for n in names:
            if n.startswith("xl/tables/table") and n.endswith(".xml"):
                t = ET.fromstring(z.read(n))
                cols = [x.attrib.get("name", "") for x in t.findall("m:tableColumns/m:tableColumn", NS)]
                out["tables"].append({"part": n, "name": t.attrib.get("name"), "ref": t.attrib.get("ref"), "columns": cols})
    return out


def sheet_headers(sheet: dict) -> tuple[int | None, dict[int, str]]:
    rows = sheet["rows"]
    for rtxt in sorted(rows, key=lambda x: int(x)):
        vals = rows[rtxt]
        normalized = {str(v).strip().lower() for v in vals.values()}
        if "candidate_id" in normalized or "row_id" in normalized:
            return int(rtxt), {int(k): str(v).strip() for k, v in vals.items()}
    return None, {}


def candidate_rows(workbook: dict) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for sname, sheet in workbook["sheets"].items():
        hrow, headers = sheet_headers(sheet)
        if hrow is None:
            continue
        id_col = next((c for c, h in headers.items() if h.lower() in {"candidate_id", "row_id"}), None)
        if id_col is None:
            continue
        rows = []
        for rtxt, vals in sheet["rows"].items():
            rnum = int(rtxt)
            if rnum <= hrow:
                continue
            cid = str(vals.get(id_col, ""))
            if not re.fullmatch(r"QP093A-\d{4}", cid):
                continue
            row = {headers.get(c, f"COL_{c}"): v for c, v in vals.items() if c in headers}
            row["_sheet"] = sname
            row["_row"] = rnum
            rows.append(row)
        if rows:
            result[sname] = rows
    return result


def find_occurrences(rows_by_sheet: dict[str, list[dict]], cid: str) -> list[dict]:
    out = []
    for sname, rows in rows_by_sheet.items():
        for row in rows:
            actual = row.get("candidate_id", row.get("row_id", ""))
            if actual == cid:
                out.append({"sheet": sname, "row": row["_row"], "values": {k: v for k, v in row.items() if not k.startswith("_")}})
    return out


def workbook_diff(w1: dict, w2: dict) -> list[dict]:
    rows = []
    all_sheets = sorted(set(w1["sheets"]) | set(w2["sheets"]))
    for sname in all_sheets:
        a = w1["sheets"].get(sname, {}).get("cells", {})
        b = w2["sheets"].get(sname, {}).get("cells", {})
        for ref in sorted(set(a) | set(b), key=lambda x: (int(re.search(r"\d+", x).group()), col_index(x))):
            ca = a.get(ref, {"value": "", "formula": "", "type": ""})
            cb = b.get(ref, {"value": "", "formula": "", "type": ""})
            if ca != cb:
                status = "changed" if ref in a and ref in b else "only_workbook_1" if ref in a else "only_workbook_2"
                rows.append({
                    "sheet": sname,
                    "cell": ref,
                    "status": status,
                    "workbook1_value": ca["value"],
                    "workbook1_formula": ca["formula"],
                    "workbook1_type": ca["type"],
                    "workbook2_value": cb["value"],
                    "workbook2_formula": cb["formula"],
                    "workbook2_type": cb["type"],
                })
    return rows


def load_csv(path: Path) -> list[dict]:
    PARSED_INPUTS.add(str(path.resolve()))
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def route_key(row: dict) -> tuple[int | None, int | None, str]:
    route = row.get("route_combination", "")
    m = re.search(r"p=(\d+),g=(\d+)", route)
    if not m:
        return None, None, "non_single_write"
    p, g = int(m.group(1)), int(m.group(2))
    if route.startswith("anti(plus"):
        role = "antimatter_plus_source_role"
    elif route.startswith("anti(minus"):
        role = "antimatter_minus_source_role"
    elif "neutral_single_write" in route:
        role = "neutral"
    elif "plus_single_write" in route:
        role = "matter_plus"
    elif "minus_single_write" in route:
        role = "matter_minus"
    else:
        role = "other"
    return p, g, role


ARITH_FIELDS = [
    "M_native",
    "M_observed_candidate",
    "qA_source_support",
    "tensor_carrier_support",
    "retained_write_support",
    "S_debit_or_credit",
]


def triad_tests(catalog: list[dict], left_a: int, left_b: int, right: int) -> list[dict]:
    index = {}
    for row in catalog:
        p, g, role = route_key(row)
        if p is not None:
            index[(p, g, role)] = row
    out = []
    keys = sorted({(g, role) for (p, g, role) in index if p == right}, key=lambda x: (x[0], x[1]))
    for g, role in keys:
        ra, rb, rr = index.get((left_a, g, role)), index.get((left_b, g, role)), index.get((right, g, role))
        if not all((ra, rb, rr)):
            continue
        for field in ARITH_FIELDS:
            va, vb, vr = frac(ra.get(field)), frac(rb.get(field)), frac(rr.get(field))
            out.append({
                "depth_g": g,
                "role": role,
                "field": field,
                "left_a_candidate": ra["candidate_id"],
                "left_b_candidate": rb["candidate_id"],
                "right_candidate": rr["candidate_id"],
                "left_a": decimal_str(va),
                "left_b": decimal_str(vb),
                "sum": decimal_str(va + vb),
                "right": decimal_str(vr),
                "deviation_fraction": fstr(va + vb - vr),
                "exact_pass": va + vb == vr,
            })
    return out


def canonical_feature_row(row: dict, membership81: set[str], domain100: set[str]) -> dict:
    p, g, role = route_key(row)
    return {
        "candidate_id": row["candidate_id"],
        "member_100": row["candidate_id"] in domain100,
        "member_81": row["candidate_id"] in membership81,
        "p": "" if p is None else p,
        "g": "" if g is None else g,
        "same_role": role,
        "bin": row.get("bin", ""),
        "operator_class": row.get("operator_class", ""),
        "route_class": row.get("route_class", ""),
        "q_sign": row.get("q_sign", ""),
        "q_abs": row.get("q_abs", ""),
        "closure_status": row.get("closure_status", ""),
        "stability_status": row.get("stability_status", ""),
        "matter_row_allowed": row.get("matter_row_allowed", ""),
        "promotion_status": row.get("promotion_status", ""),
        "M_native": row.get("M_native", ""),
        "qA_source_support": row.get("qA_source_support", ""),
        "tensor_carrier_support": row.get("tensor_carrier_support", ""),
        "retained_write_support": row.get("retained_write_support", ""),
    }


TREE_FEATURES = ["bin", "operator_class", "route_class", "q_sign", "closure_status", "stability_status", "matter_row_allowed", "same_role", "p", "g"]


def gini(labels: list[int]) -> float:
    if not labels:
        return 0.0
    p = sum(labels) / len(labels)
    return 2 * p * (1 - p)


def predicates(rows: list[dict]) -> list[tuple[str, str, object]]:
    out = []
    for feature in TREE_FEATURES:
        values = sorted({r[feature] for r in rows if r[feature] != ""}, key=str)
        if feature in {"p", "g"}:
            nums = sorted({float(v) for v in values})
            for a, b in zip(nums, nums[1:]):
                out.append((feature, "<=", (a + b) / 2))
        elif len(values) <= 18:
            for v in values:
                out.append((feature, "==", v))
    return out


def pred_eval(row: dict, pred: tuple[str, str, object]) -> bool:
    feature, op, value = pred
    if op == "==":
        return row[feature] == value
    if row[feature] == "":
        return False
    return float(row[feature]) <= float(value)


def build_tree(rows: list[dict], depth: int, max_depth: int) -> dict:
    labels = [1 if r["member_81"] else 0 for r in rows]
    positives = sum(labels)
    node = {"n": len(rows), "positives": positives, "prediction": positives * 2 >= len(rows)}
    if depth >= max_depth or positives in {0, len(rows)} or len(rows) < 4:
        node["leaf"] = True
        return node
    base = gini(labels)
    best = None
    for pred in predicates(rows):
        left = [r for r in rows if pred_eval(r, pred)]
        right = [r for r in rows if not pred_eval(r, pred)]
        if not left or not right:
            continue
        score = base - (len(left) * gini([int(r["member_81"]) for r in left]) + len(right) * gini([int(r["member_81"]) for r in right])) / len(rows)
        key = (round(score, 15), -len(str(pred)), str(pred))
        if best is None or key > best[0]:
            best = (key, pred, left, right)
    if best is None or best[0][0] <= 0:
        node["leaf"] = True
        return node
    _, pred, left, right = best
    node.update({"leaf": False, "predicate": {"feature": pred[0], "operator": pred[1], "value": pred[2]}})
    node["true"] = build_tree(left, depth + 1, max_depth)
    node["false"] = build_tree(right, depth + 1, max_depth)
    return node


def apply_tree(tree: dict, row: dict) -> bool:
    node = tree
    while not node.get("leaf", False):
        p = node["predicate"]
        node = node["true"] if pred_eval(row, (p["feature"], p["operator"], p["value"])) else node["false"]
    return bool(node["prediction"])


def tree_nodes(tree: dict) -> int:
    return 1 if tree.get("leaf") else 1 + tree_nodes(tree["true"]) + tree_nodes(tree["false"])


def candidate_score(tree: dict, rows: list[dict], catalog_map: dict[str, dict]) -> dict:
    preds = {r["candidate_id"]: apply_tree(tree, r) for r in rows}
    errors = [r["candidate_id"] for r in rows if preds[r["candidate_id"]] != bool(r["member_81"])]
    selected = [r for r in rows if preds[r["candidate_id"]]]
    nodes = tree_nodes(tree)
    # Conjugate symmetry is evaluated where the source route is explicitly anti(...).
    matter_by_signature = {}
    anti_pairs = []
    for r in rows:
        src = catalog_map[r["candidate_id"]]
        route = src.get("route_combination", "")
        if route.startswith("anti("):
            inner = route[5:-1]
            mate = matter_by_signature.get(inner)
            if mate:
                anti_pairs.append((mate, r["candidate_id"]))
        else:
            matter_by_signature[route] = r["candidate_id"]
    sym_ok = sum(1 for a, b in anti_pairs if preds.get(a) == preds.get(b))
    sym_frac = sym_ok / len(anti_pairs) if anti_pairs else 1.0
    accuracy = 1 - len(errors) / len(rows)
    score = 100 * accuracy + 5 * sym_frac - 0.25 * nodes
    total = sum((frac(catalog_map[r["candidate_id"]].get("M_native")) for r in selected), Fraction(0))
    return {
        "accuracy": accuracy,
        "exceptions": len(errors),
        "exception_ids_discovery_only": errors,
        "selected_rows_reported_after_rule": len(selected),
        "selected_M_native_sum_reported_after_rule": decimal_str(total),
        "tree_nodes": nodes,
        "conjugate_symmetry_fraction": sym_frac,
        "description_score": score,
        "uses_candidate_ids": False,
        "uses_target_count_or_sum": False,
        "uses_M_native": False,
    }


MAGIC = [2, 8, 20, 28, 50, 82, 126]
MAGIC_SET = set(MAGIC)
D_LOCKED = (7093 * 7093) / (192 * 7117)


def dist_magic(x: int) -> int:
    return min(abs(x - m) for m in MAGIC)


def find_shell(x: int) -> tuple[int, int]:
    lower, upper = 0, 200
    for m in MAGIC:
        if m <= x and m > lower:
            lower = m
        if m > x and m < upper:
            upper = m
    return lower, upper


def base_features(Z: int, N: int, A: int) -> dict[str, float]:
    delta = 1.0 if Z % 2 == 0 and N % 2 == 0 else -1.0 if Z % 2 == 1 and N % 2 == 1 else 0.0
    dZ, dN = dist_magic(Z), dist_magic(N)
    lz, uz = find_shell(Z)
    ln, un = find_shell(N)
    nZ, nN = Z - lz, N - ln
    spZ, spN = uz - lz, un - ln
    qz, qn = nZ * (spZ - nZ), nN * (spN - nN)
    f_alpha = A // 4 if N == Z and A % 4 == 0 else 0.0
    if 50 < Z < 82 and 82 < N < 126:
        zt = (Z - 50) * (82 - Z) / 16**2
        nt = (N - 82) * (126 - N) / 22**2
        reonset = -zt * nt
    else:
        reonset = 0.0
    return {
        "vol": A,
        "surf": -A ** (2 / 3),
        "coul": -Z * (Z - 1) / A ** (1 / 3),
        "asym": -((N - Z) ** 2) / A,
        "pair": -delta * A ** -0.5,
        "quadZ_A": -qz / A,
        "quadN_A": -qn / A,
        "quad_cross_A2": -qz * qn / (A * A),
        "shell_prox": -math.exp(-dZ / 3) - math.exp(-dN / 3),
        "lightodd": 1.0 if A < 40 and A % 2 == 1 else 0.0,
        "alpha": f_alpha,
        "reonset": reonset,
        "doubmag": 1.0 if Z in MAGIC_SET and N in MAGIC_SET else 0.0,
    }


def op_features(Z: int, N: int, A: int) -> dict[str, float]:
    ln, _ = find_shell(N)
    nN = N - ln
    return {
        "op_82pre": (Z - 56) ** 2 if N == 82 and Z > 56 else 0.0,
        "op_3d_odd": 1.0 if Z % 2 == 1 and 20 < Z < 30 else 0.0,
        "op_dm_sat": 1.0 if Z in MAGIC_SET and N in MAGIC_SET and A >= 100 else 0.0,
        "op_ms_fill": nN if 28 < Z <= 50 and 50 < N < 82 else 0.0,
    }


def predict_cr274(row: dict, beta: dict[str, float], gammas: dict[str, float]) -> tuple[float, dict[str, float]]:
    Z, N, A = row["Z"], row["N"], row["A"]
    bf = base_features(Z, N, A)
    base = sum(beta[k] * bf[k] for k in beta)
    of = op_features(Z, N, A)
    contrib = {k: gammas[k] * of[k] for k in gammas}
    return base + sum(contrib.values()), contrib


def metrics(obs: list[float], pred: list[float]) -> dict:
    res = [o - p for o, p in zip(obs, pred)]
    return {
        "n": len(res),
        "RMS_MeV": math.sqrt(sum(x * x for x in res) / len(res)),
        "mean_residual_MeV": sum(res) / len(res),
        "MAE_MeV": sum(abs(x) for x in res) / len(res),
        "within_5": sum(abs(x) <= 5 for x in res),
        "within_8": sum(abs(x) <= 8 for x in res),
        "max_abs_MeV": max(abs(x) for x in res),
    }


def binding_discovery(binding_path: Path, cr274_summary: dict) -> tuple[dict, dict, list[dict]]:
    # The set field is checked before B_u_obs_MeV is parsed. Test observations
    # remain unread by candidate-selection logic in this process.
    PARSED_INPUTS.add(str(binding_path.resolve()))
    train = []
    set_counts = Counter()
    with binding_path.open("r", newline="", encoding="utf-8-sig") as f:
        for raw in csv.DictReader(f):
            set_counts[raw["set"]] += 1
            if raw["set"] != "train":
                continue
            train.append({
                "isotope": raw["isotope"],
                "Z": int(raw["Z"]),
                "N": int(raw["N"]),
                "A": int(raw["A"]),
                "obs": float(raw["B_u_obs_MeV"]),
            })
    beta = {k: float(v) for k, v in cr274_summary["beta_K"].items()}
    gammas = {k: float(v["gamma"]) for k, v in cr274_summary["operators"].items()}
    baseline_pred, contribs = [], []
    for r in train:
        p, c = predict_cr274(r, beta, gammas)
        baseline_pred.append(p)
        contribs.append(c)
    obs = [r["obs"] for r in train]
    baseline_metrics = metrics(obs, baseline_pred)

    definitions = {
        "forbidden_fitted_coefficients": [126, 144, 162, 12600, 16200],
        "fee_candidates": {
            "F1": "qA_source_support - M_native",
            "F2": "qA_source_support - retained_write_support",
            "F3": "tensor_carrier_support",
            "F4": "surface debit/credit only",
            "F5": "no direct row fee; geometry and frozen operators only",
        },
        "algebraic_dependence": "F2 == F3 wherever qA = tensor + retained by column construction; count once.",
        "typed_zero_rules": {
            "neutral_W9_witness_local_count": 0,
            "QP093A_0066_Theta_local_fee": 0,
            "QP093A_0299_repeated_constituent_count": 0,
        },
        "geometry_features": {
            "linear_excess_traffic": "abs(N-Z)",
            "surface_normalized_excess_traffic": "abs(N-Z)/A^(1/3)",
        },
        "parameter_policy": "A new traffic coefficient must replace one frozen tiny-family operator coefficient; free-parameter delta = 0.",
    }

    results = []
    results.append({"candidate_id": "B0_CR274_FROZEN", "eligible": True, "formula": "frozen CR274", "removed_operator": "", "gamma": "", "free_parameter_delta": 0, **baseline_metrics, "discovery_status": "BASELINE"})
    results.append({"candidate_id": "B1_TYPED_ZERO_FEE_CLEANUP", "eligible": True, "formula": "CR274 with W9 witness, Theta carrier, and Higgs reveal repeated counts fixed at zero", "removed_operator": "", "gamma": "0", "free_parameter_delta": 0, **baseline_metrics, "discovery_status": "ACCOUNTING_CHANGE_NUMERICALLY_IDENTICAL"})

    candidate_specs = [
        ("B2_LINEAR_EXCESS_REPLACES_DM", "op_dm_sat", lambda r: abs(r["N"] - r["Z"]), "abs(N-Z)"),
        ("B3_SURFACE_EXCESS_REPLACES_82", "op_82pre", lambda r: abs(r["N"] - r["Z"]) / (r["A"] ** (1 / 3)), "abs(N-Z)/A^(1/3)"),
    ]
    for cid, removed, feature_fn, formula in candidate_specs:
        base_without = [p - c[removed] for p, c in zip(baseline_pred, contribs)]
        feature = [feature_fn(r) for r in train]
        den = sum(x * x for x in feature)
        gamma = sum((o - p) * x for o, p, x in zip(obs, base_without, feature)) / den if den else 0.0
        pred = [p + gamma * x for p, x in zip(base_without, feature)]
        m = metrics(obs, pred)
        results.append({"candidate_id": cid, "eligible": True, "formula": formula, "removed_operator": removed, "gamma": gamma, "free_parameter_delta": 0, **m, "discovery_status": "TRAIN_ONLY_CANDIDATE"})

    results.extend([
        {"candidate_id": "B4_ASYMMETRY_DUPLICATE", "eligible": False, "formula": "(N-Z)^2/A", "removed_operator": "", "gamma": "", "free_parameter_delta": 0, "discovery_status": "REJECT_ALGEBRAICALLY_DEPENDENT_ON_LOCKED_ASYM"},
        {"candidate_id": "B5_REPEAT_HIGGS_ROW", "eligible": False, "formula": "repeat QP093A-0299 per isotope", "removed_operator": "", "gamma": "", "free_parameter_delta": 0, "discovery_status": "REJECT_GLOBAL_REVEAL_NOT_CONSTITUENT"},
        {"candidate_id": "B6_CHARGE_THETA", "eligible": False, "formula": "charge tensor support locally", "removed_operator": "", "gamma": "", "free_parameter_delta": 0, "discovery_status": "REJECT_THETA_ZERO_FEE"},
    ])
    baseline = {
        "controlling_CR274": cr274_summary,
        "CR261_split_counts": dict(set_counts),
        "candidate_selection_rows": len(train),
        "test_observations_scored": 0,
        "extended_observations_scored": 0,
        "train_metrics_frozen_CR274": baseline_metrics,
        "preserved_dead_ends": {
            "CR249": "linear connection-fee sum failed",
            "CR250": "single global rescale did not repair shape",
        },
    }
    return baseline, definitions, results


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    manifest = read_json(MANIFEST)
    source_by_id = {x["source_id"]: x for x in manifest["sources"]}

    hash_checks = {}
    for entry in manifest["sources"]:
        p = source_path(entry)
        if entry["verify_mode"] == "prior_frozen_hash_plus_saved_excel_capture_cell_reconciliation":
            hash_checks[entry["source_id"]] = {
                "exists": p.exists(),
                "bytes_match": p.exists() and p.stat().st_size == entry["bytes"],
                "sha256_match": "DEFERRED_TO_PRIOR_FROZEN_HASH_AND_CELL_RECONCILIATION",
            }
            continue
        actual = sha256(p)
        hash_checks[entry["source_id"]] = {"exists": True, "bytes_match": p.stat().st_size == entry["bytes"], "sha256_match": actual == entry["sha256"], "actual_sha256": actual}
    precommit_ok = sha256(PRECOMMIT) == PRECOMMIT_HASH
    manifest_ok = sha256(MANIFEST) == MANIFEST_HASH

    w1_path = source_path(source_by_id["UPDATED_WORKBOOK_100_CAPTURE"])
    w2_path = source_path(source_by_id["UPDATED_WORKBOOK_81_CAPTURE"])
    w1 = parse_workbook(w1_path)
    w2 = parse_workbook(w2_path)
    w1_rows = candidate_rows(w1)
    w2_rows = candidate_rows(w2)
    diff_rows = workbook_diff(w1, w2)
    write_csv("WORKBOOK_DIFF.csv", diff_rows)

    roster100 = load_csv(source_path(source_by_id["CR120N_ROSTER100"]))
    roster81 = load_csv(source_path(source_by_id["CR120N_ROSTER81"]))
    catalog = load_csv(source_path(source_by_id["QP093A_CANONICAL_299"]))
    catalog_map = {r["candidate_id"]: r for r in catalog}
    ids100 = {r["candidate_id"] for r in roster100}
    ids81 = {r["candidate_id"] for r in roster81}
    packet_ids = {"QP093A-0019", "QP093A-0020", "QP093A-0021", "QP093A-0085", "QP093A-0086"}
    ids105 = ids100 | packet_ids
    sum100 = sum((frac(r["M_native"]) for r in roster100), Fraction(0))
    sum81 = sum((frac(r["M_native"]) for r in roster81), Fraction(0))
    sum105 = sum((frac(catalog_map[i]["M_native"]) for i in ids105), Fraction(0))
    packet_sum = sum((frac(catalog_map[i]["M_native"]) for i in packet_ids), Fraction(0))

    # Reconcile the SaveCopyAs logical capture to the prior extraction.
    main1_name, main1_rows = max(w1_rows.items(), key=lambda kv: len({r.get("candidate_id", r.get("row_id")) for r in kv[1]}))
    # The workbook's saved-table projection is the explicit count=1 lane.
    # The same sheet also carries non-projected catalog rows; training a rule
    # on all of them would change the discovery domain from 126 to 299+.
    saved_main1_rows = [r for r in main1_rows if str(r.get("count", "")).strip() in {"1", "1.0", "TRUE", "true"}]
    main1_ids = {r.get("candidate_id", r.get("row_id")) for r in main1_rows}
    capture_has_105 = ids105 <= main1_ids
    logical_capture_reconciled = capture_has_105 and len(ids100) == 100 and sum100 == 16200
    hash_checks["UPDATED_WORKBOOK_100_ORIGINAL"]["logical_capture_reconciled"] = logical_capture_reconciled

    write_csv("ROSTER_100.csv", roster100)
    write_csv("ROSTER_81.csv", roster81)
    delta = []
    for cid in sorted(ids100 | ids81):
        c = catalog_map[cid]
        transition = "retained" if cid in ids100 and cid in ids81 else "removed_from_100" if cid in ids100 else "introduced_in_81"
        p, g, role = route_key(c)
        delta.append({
            "candidate_id": cid,
            "present_in_100": cid in ids100,
            "present_in_81": cid in ids81,
            "transition": transition,
            "row_type": c.get("bin", ""),
            "p": "" if p is None else p,
            "g": "" if g is None else g,
            "same_role": role,
            "sign": c.get("q_sign", ""),
            "matter_antimatter_neutral": "antimatter" if c.get("bin") == "antimatter_conjugate_rows" else "neutral" if c.get("q_sign") == "neutral" else "matter",
            "M_native": c.get("M_native", ""),
            "qA_source_support": c.get("qA_source_support", ""),
            "tensor_carrier_support": c.get("tensor_carrier_support", ""),
            "retained_write_support": c.get("retained_write_support", ""),
            "source_status": c.get("stability_status", ""),
            "user_reclassified_status": next((r.get("promotion_status", "") for r in roster81 if r["candidate_id"] == cid), ""),
        })
    write_csv("ROSTER_100_TO_81_DELTA.csv", delta)

    domain_rows = saved_main1_rows
    domain_ids = {r.get("candidate_id", r.get("row_id")) for r in domain_rows}
    occurrence_rows = []
    for cid in sorted(domain_ids):
        if cid not in catalog_map:
            continue
        c = catalog_map[cid]
        p, g, role = route_key(c)
        occurrence_rows.append({
            "candidate_id": cid,
            "entity_type": "QP093A_COORDINATE_OCCURRENCE",
            "typed_scalar_occurrence": "QP_P1" if p == 1 else "QP_P8" if p == 8 else "QP_P9" if p == 9 else "OTHER_QP_COORDINATE",
            "not_equal_to": "X1_AXIS_SELF_CHANNEL" if p == 1 else "S8_BINARY_SURFACE/C8/P8" if p == 8 else "W9_CLOSURE_WITNESS/C9/P9" if p == 9 else "",
            "p": "" if p is None else p,
            "g": "" if g is None else g,
            "same_role": role,
            "bin": c.get("bin", ""),
            "operator_class": c.get("operator_class", ""),
            "route_class": c.get("route_class", ""),
            "q_sign": c.get("q_sign", ""),
            "M_native": c.get("M_native", ""),
            "qA_source_support": c.get("qA_source_support", ""),
            "tensor_carrier_support": c.get("tensor_carrier_support", ""),
            "retained_write_support": c.get("retained_write_support", ""),
            "present_in_100": cid in ids100,
            "present_in_81": cid in ids81,
        })
    write_csv("ROW_OCCURRENCE_REGISTER.csv", occurrence_rows)

    p819 = triad_tests(catalog, 8, 1, 9)
    p639 = triad_tests(catalog, 6, 3, 9)
    write_csv("P1_P8_P9_SAME_ROLE_TEST.csv", p819)
    write_csv("P6_P3_P9_CONTROL.csv", p639)

    triad_ids = ["QP093A-0051", "QP093A-0066", "QP093A-0069"]
    triad_rows = []
    for cid in triad_ids:
        r = catalog_map[cid]
        triad_rows.append({k: r.get(k, "") for k in ["candidate_id", "route_combination", "partition_signature", "closure_depth", "q_sign", "M_native", "M_observed_candidate", "qA_source_support", "tensor_carrier_support", "retained_write_support", "stability_status", "promotion_status"]} | {"present_in_100": cid in ids100, "present_in_81": cid in ids81})
    write_csv("QP093A_0051_0066_0069_TRIAD.csv", triad_rows)

    occ66_1 = find_occurrences(w1_rows, "QP093A-0066")
    occ66_2 = find_occurrences(w2_rows, "QP093A-0066")
    occ299_1 = find_occurrences(w1_rows, "QP093A-0299")
    occ299_2 = find_occurrences(w2_rows, "QP093A-0299")
    canonical299 = catalog_map["QP093A-0299"]
    conflict = {
        "candidate_id": "QP093A-0299",
        "canonical_source": {"path": source_by_id["QP093A_CANONICAL_299"]["path"], "sha256": source_by_id["QP093A_CANONICAL_299"]["sha256"], "M_native": canonical299["M_native"], "controlling": True},
        "workbook_1_occurrences": occ299_1,
        "workbook_2_occurrences": occ299_2,
        "workbook_1_file_hash": w1["sha256"],
        "workbook_2_file_hash": w2["sha256"],
        "disposition": "CANONICAL_126000_CONTROLS; workbook changes without sealed typed authorization are target-aware overlay evidence only",
    }
    dump_json("HIGGS_WORKBOOK_SOURCE_CONFLICT.json", conflict)

    ledger = {
        "Theta": 18,
        "M": 126,
        "N": 144,
        "L": 162,
        "100L": 16200,
        "100N": 14400,
        "100M": 12600,
        "identities": {
            "L=N+Theta": 162 == 144 + 18,
            "M=N-Theta": 126 == 144 - 18,
            "midpoint": (16200 + 12600) // 2 == 14400,
            "half_difference": (16200 - 12600) // 2 == 1800,
            "N=Theta+M": 144 == 18 + 126,
        },
        "observations": {"rows105": len(ids105), "sum105": decimal_str(sum105), "packet_rows": len(packet_ids), "packet_sum": decimal_str(packet_sum), "rows100": len(ids100), "sum100": decimal_str(sum100), "mean100": decimal_str(sum100 / len(ids100)), "rows81": len(ids81), "sum81": decimal_str(sum81)},
        "evidence_class": "EXACT_NUMERIC_COMPATIBILITY; projection law requires frozen validation",
    }
    dump_json("LEDGER_IDENTITIES.json", ledger)
    (HERE / "LEDGER_IDENTITIES.md").write_text(
        "# CR120T Ledger Identities\n\n"
        f"- `105 - 5 = {len(ids100)}`; removed packet sum `{decimal_str(packet_sum)}`.\n"
        f"- `sum_100(M_native) = {decimal_str(sum100)}`; mean `{decimal_str(sum100/len(ids100))} = L`.\n"
        f"- `sum_81(M_native) = {decimal_str(sum81)} = 100*M`.\n"
        "- `100L=16200`, `100N=14400`, `100M=12600`; `L=N+Theta`, `M=N-Theta`.\n\n"
        "These are exact accounting compatibilities. The discovery phase does not promote them to an F81 physical selector.\n",
        encoding="utf-8",
    )

    # Dossiers.
    r66 = catalog_map["QP093A-0066"]
    (HERE / "QP093A_0066_DOSSIER.md").write_text(
        "# QP093A-0066 Dossier\n\n"
        f"Canonical source: `{source_by_id['QP093A_CANONICAL_299']['path']}` (`{source_by_id['QP093A_CANONICAL_299']['sha256']}`).\n\n"
        f"- route: `{r66['route_combination']}`; canonical stability: `{r66['stability_status']}`.\n"
        f"- `M_native=qA={r66['M_native']}=N`; tensor `{r66['tensor_carrier_support']}=Theta`; retained `{r66['retained_write_support']}=M`.\n"
        "- Exact: `144 = 18 + 126`; the p1/p8/p9 g=2 neutral triad also closes every audited support column.\n"
        f"- present in 100: `{str('QP093A-0066' in ids100).lower()}`; present in 81: `{str('QP093A-0066' in ids81).lower()}`.\n"
        f"- workbook-1 occurrences: `{len(occ66_1)}`; workbook-2 occurrences: `{len(occ66_2)}`.\n\n"
        "Source-typed reading: closure-budget unit cell / neutral ledger cell is supported structurally. The workbook-only stable reclassification is not canonical physical-identity authority. Its exclusion from F81 is compatible with template non-payload and global-accounting hypotheses, but this discovery data alone cannot distinguish those from target-aware manual omission.\n",
        encoding="utf-8",
    )
    r299 = canonical299
    (HERE / "QP093A_0299_DOSSIER.md").write_text(
        "# QP093A-0299 Dossier\n\n"
        f"Canonical route: `{r299['route_combination']}`; status `{r299['stability_status']}`; known match `{r299['known_match']}`.\n\n"
        f"- `126000 - {r299['S_debit_or_credit']} = {r299['M_observed_candidate']}`.\n"
        f"- `{r299['M_observed_candidate']}/8 = {r299['tensor_carrier_support']}`.\n"
        f"- `7*{r299['M_observed_candidate']}/8 = {r299['retained_write_support']}`.\n"
        "- The native/debit/reveal operations are source-authorized by the canonical row and CR267/CR269 chain. The post-reveal 1/8 and 7/8 columns are support allocations, not asserted decay products.\n"
        "- QP093A-0299 is a closed-loop reveal parent and is not merged with QP093A-0066's row-local closure-budget unit cell.\n"
        "- `12600 = 126000/10` has no frozen factor-10 source role in the opened chain and is classified `NUMERIC_SCALE_COMPATIBILITY_ONLY`.\n",
        encoding="utf-8",
    )

    charged_p9g0 = {"QP093A-0019", "QP093A-0020", "QP093A-0085", "QP093A-0086"}
    neutral_p9g0 = "QP093A-0021"
    packet_report = (
        "# Witness Packet versus Witness Occurrence\n\n"
        f"- CR120R global overlay excludes all five p=9,g=0 occurrences: `{sorted(packet_ids)}`.\n"
        f"- F81 retains charged/conjugate occurrences `{sorted(charged_p9g0 & ids81)}` and excludes neutral `{neutral_p9g0}`.\n"
        "- Therefore the two workbooks do not implement one universal 'remove every p9' law.\n"
        "- Best discovery reading: CR120R is a global accounting packet overlay; F81 is role-sensitive and treats the neutral occurrence as the row-level W9 witness candidate. This reading remains candidate status until frozen validation.\n"
    )
    (HERE / "WITNESS_PACKET_VS_OCCURRENCE_REPORT.md").write_text(packet_report, encoding="utf-8")

    # F81 feature table and target-aware decision-tree candidates.
    feature_rows = [canonical_feature_row(catalog_map[cid], ids81, ids100) for cid in sorted(domain_ids) if cid in catalog_map]
    write_csv("F81_DISCOVERY_FEATURES.csv", feature_rows)
    candidate_rules = []
    score_rows = []
    for depth in [2, 3, 4, 5, 6]:
        tree = build_tree(feature_rows, 0, depth)
        score = candidate_score(tree, feature_rows, catalog_map)
        rid = f"F81_TREE_DEPTH_{depth}"
        candidate_rules.append({"rule_id": rid, "family": "source_typed_decision_tree", "max_depth": depth, "allowed_features": TREE_FEATURES, "tree": tree, "score": score, "discovery_target_aware": True})
        score_rows.append({"rule_id": rid, "max_depth": depth, **{k: v for k, v in score.items() if k != "exception_ids_discovery_only"}})
    candidate_rules.sort(key=lambda x: x["score"]["description_score"], reverse=True)
    dump_json("F81_CANDIDATE_RULES.json", {"domain": f"{main1_name}: count=1 saved-table lane", "domain_rows": len(feature_rows), "membership_used_for_discovery": True, "rules": candidate_rules, "recommended_for_freeze_review": candidate_rules[0]["rule_id"]})
    write_csv("F81_CANDIDATE_RULE_SCORECARD.csv", score_rows)

    # Binding discovery: CR277 contents are hash-verified but not parsed here.
    cr274_summary = read_json(source_path(source_by_id["CR274_SUMMARY"]))
    baseline, feature_defs, binding_results = binding_discovery(source_path(source_by_id["CR261_BINDING_35_20"]), cr274_summary)
    dump_json("BINDING_BASELINE.json", baseline)
    dump_json("BINDING_FEATURE_DEFINITIONS.json", feature_defs)
    write_csv("BINDING_DISCOVERY_RESULTS.csv", binding_results)

    # Workbook summaries after all extractions.
    inv = {}
    for label, wb_obj, rows_obj in [("workbook_1", w1, w1_rows), ("workbook_2", w2, w2_rows)]:
        inv[label] = {
            "path": wb_obj["path"], "bytes": wb_obj["bytes"], "sha256": wb_obj["sha256"],
            "package_entries": wb_obj["package_entries"], "macro_or_binary_parts": wb_obj["macro_or_binary_parts"],
            "comments_parts": wb_obj["comments_parts"], "tables": wb_obj["tables"],
            "sheets": {n: {k: v for k, v in s.items() if k not in {"cells", "rows", "xml_path"}} | {"candidate_rows": len(rows_obj.get(n, [])), "saved_count_rows": sum(str(r.get('count', '')).strip() in {'1', '1.0', 'TRUE', 'true'} for r in rows_obj.get(n, [])), "duplicate_candidate_ids": [x for x, c in Counter(r.get('candidate_id', r.get('row_id')) for r in rows_obj.get(n, [])).items() if c > 1], "annotation_columns": sorted({k for r in rows_obj.get(n, []) for k in r if any(t in k.lower() for t in ('promotion', 'reclass', 'known_match', 'observed_identity'))})} for n, s in wb_obj["sheets"].items()},
        }
    annotation_changes = [r for r in diff_rows if any(x in (r["workbook1_value"] + r["workbook2_value"]).lower() for x in ("reclass", "promotion", "known_match", "stable_user"))]
    summary_md = ["# Workbook Diff Summary", "", f"Workbook 1 capture SHA-256: `{w1['sha256']}`", f"Workbook 2 SHA-256: `{w2['sha256']}`", "", f"Cell-level differences: `{len(diff_rows)}`", f"Annotation-related changed cells: `{len(annotation_changes)}`", "", "## Inventory", ""]
    for label in ("workbook_1", "workbook_2"):
        summary_md.append(f"### {label}")
        for sname, s in inv[label]["sheets"].items():
            summary_md.append(f"- `{sname}`: dimension `{s['dimension']}`, candidate rows `{s['candidate_rows']}`, formulas `{s['formula_count']}`, hidden rows `{len(s['hidden_rows'])}`, hidden columns `{s['hidden_columns']}`")
        summary_md.append("")
    summary_md.extend(["## QP093A-0299", "", f"Canonical `M_native=126000`; workbook-1 occurrences `{len(occ299_1)}`; workbook-2 occurrences `{len(occ299_2)}`. Exact cells and values are in `HIGGS_WORKBOOK_SOURCE_CONFLICT.json`.", "", "The canonical source row controls. A workbook-only change cannot be used as scientific evidence without a sealed typed authorization."])
    (HERE / "WORKBOOK_DIFF_SUMMARY.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")
    (HERE / "ROW_SCHEMA_AND_UNITS.md").write_text(
        "# Row Schema and Units\n\n"
        "The canonical QP093A CSV supplies row identity, type, and numeric authority. Workbook columns are research-overlay occurrences.\n\n"
        "- `M_native`, `M_observed_candidate`, `qA_source_support`, `tensor_carrier_support`, `retained_write_support`, and `S_debit_or_credit` are preserved in source ledger units.\n"
        "- No conversion to MeV is made except where the source row itself labels the normalized Higgs comparison.\n"
        "- `tensor_carrier_support + retained_write_support = qA_source_support` is a column-construction identity and is counted once.\n"
        "- `candidate_id` identifies a QP occurrence; equal scalars do not merge QP coordinates, typed surfaces, axes, witnesses, carriers, or supports.\n"
        "- Workbook formulas are reported with cached stored values; no workbook code or formulas are executed.\n",
        encoding="utf-8",
    )

    all_hash_strict = all(v.get("sha256_match") is True and v.get("bytes_match") is True for k, v in hash_checks.items() if k != "UPDATED_WORKBOOK_100_ORIGINAL")
    d0 = precommit_ok and manifest_ok and all_hash_strict and logical_capture_reconciled
    d1 = bool(diff_rows) and len(w1["sheets"]) > 0 and len(w2["sheets"]) > 0
    d2 = len(ids105) == 105 and len(packet_ids) == 5 and len(ids100) == 100 and sum100 == 16200 and len(ids81) == 81 and sum81 == 12600
    d3 = bool(p819) and bool(p639)
    d4 = r66["M_native"] == "144" and r299["M_native"] == "126000"
    d5 = len(feature_rows) == 126 and len(candidate_rules) == 5
    d6 = baseline["candidate_selection_rows"] == 35 and baseline["test_observations_scored"] == 0 and baseline["extended_observations_scored"] == 0
    validation = {
        "execution_status": "CLEAN" if all((d0, d1, d2, d3, d4, d5, d6)) else "DISCOVERY_INCOMPLETE",
        "gates": {"D0_SOURCE_HASHES": d0, "D1_WORKBOOK_AUDIT": d1, "D2_LEDGER_REPRODUCTION": d2, "D3_TYPED_ROW_AUDIT": d3, "D4_ROW_DOSSIERS": d4, "D5_RULE_DISCOVERY": d5, "D6_BINDING_DISCOVERY_FIREWALL": d6},
        "source_hash_checks": hash_checks,
        "precommit_sha256_match": precommit_ok,
        "source_manifest_sha256_match": manifest_ok,
        "workbook_inventory": inv,
        "workbooks_mutated": False,
        "CR120R_modified": False,
        "CR120S_modified": False,
        "validation_run": False,
    }
    dump_json("DISCOVERY_REPORT.json", validation)
    opened = []
    for p in sorted(HASHED_INPUTS | PARSED_INPUTS):
        opened.append({"path": p, "mode": "PARSED" if p in PARSED_INPUTS else "HASH_ONLY", "sha256": sha256(Path(p)) if Path(p).exists() and Path(p).is_file() else None})
    dump_json("OPENED_FILE_MANIFEST.json", {"phase": "discovery", "files": opened})
    (HERE / "COMMAND_LOG.txt").write_text(
        f"{started} PRECOMMIT_DISCOVERY sha256={PRECOMMIT_HASH}\n"
        f"{datetime.now(timezone.utc).isoformat()} runner={' '.join(sys.argv)}\n"
        "WORKBOOK_FORMULA_EXECUTION: no\nVALIDATION_EXECUTED: no\n",
        encoding="utf-8",
    )
    print(json.dumps({"execution_status": validation["execution_status"], "gates": validation["gates"], "rows100": len(ids100), "sum100": decimal_str(sum100), "rows81": len(ids81), "sum81": decimal_str(sum81), "recommended_F81": candidate_rules[0]["rule_id"], "binding_candidates": [{"id": r["candidate_id"], "RMS": r.get("RMS_MeV"), "status": r["discovery_status"]} for r in binding_results]}, indent=2))
    return 0 if validation["execution_status"] == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
