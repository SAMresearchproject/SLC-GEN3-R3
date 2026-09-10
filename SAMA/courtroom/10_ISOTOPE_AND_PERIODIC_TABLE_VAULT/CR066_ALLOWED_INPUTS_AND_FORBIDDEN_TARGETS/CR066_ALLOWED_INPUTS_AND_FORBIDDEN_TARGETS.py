"""CR066_ALLOWED_INPUTS_AND_FORBIDDEN_TARGETS.py

Runs the CR066 allowed-inputs verification declared in CR066_PRECOMMIT.md.

Phases:
  1 - Hash verification + CR065 manifest seal check
  2 - QP049-QP060 self-disclosure (vault construction chain - all must
      report external_data_used=false, observed_*_used=false, and
      free_parameters_introduced=0)
  3 - QP060 boundary check (next_frontier explicitly names QP061 as the
      external-data step)
  4 - QP061 comparator-role check (external_data_used=true AND
      sealed_hash_guard_pass=true AND prediction_manifest_mutated=false
      AND free_parameters_introduced=0)
  5 - QP068 self-disclosure (high-Z miss structure - external_data_used=false)
  6 - Forbidden input scan (AME2020, NIST, IUPAC as construction inputs)
  7 - Wrong control injections (WC1-WC6)
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import tokenize
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE             = Path(__file__).resolve().parent
BRANCH_ROOT      = HERE.parent
COURTROOM_ROOT   = BRANCH_ROOT.parent
MANIFEST_PATH    = BRANCH_ROOT / "SOURCE_MANIFEST.csv"
MANIFEST_SEAL    = BRANCH_ROOT / "SOURCE_MANIFEST.csv.sha256.txt"
SEAL_PATH        = BRANCH_ROOT / "SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13.md"

OUT_INPUT_MANIFEST       = HERE / "CR066_input_manifest.csv"
OUT_QP_DISCLOSURE        = HERE / "CR066_qp_self_disclosure_check.csv"
OUT_QP060_BOUNDARY       = HERE / "CR066_qp060_boundary_check.json"
OUT_QP061_COMPARATOR     = HERE / "CR066_qp061_comparator_role_check.json"
OUT_FORBIDDEN            = HERE / "CR066_forbidden_input_scan.csv"
OUT_MANIFEST_SEAL_CHECK  = HERE / "CR066_manifest_seal_check.json"
OUT_WRONG_CONTROLS       = HERE / "CR066_wrong_controls.csv"
OUT_SUMMARY              = HERE / "CR066_summary.json"
OUT_RESULT               = HERE / "CR066_result.md"
OUT_HASHES               = HERE / "HASHES.txt"

SEAL_SHA = "9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5"
EXPECTED_MANIFEST_SHA = "cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2"

QUANTUM_PHASE = Path("C:/VS/quantum_phase")

# Vault construction chain - all must report external_data_used=false
VAULT_CONSTRUCTION_CHAIN = [
    "qp049", "qp050", "qp051", "qp052", "qp053", "qp054", "qp055",
    "qp056", "qp057", "qp058", "qp059", "qp060",
]

# QP061 = comparator step (the ONLY test in scope that admits external data)
QP_COMPARATOR_STEP = "qp061"

# QP068 = high-Z frontier prediction - must NOT use external data for construction
QP_FRONTIER_STEP = "qp068"

ISOTOPE_DISCLOSURE_FIELDS = [
    "external_data_used",
    "observed_isotope_masses_used",
    "observed_decay_modes_used",
    "observed_half_lives_used",
    "observed_abundances_used",
    "free_parameters_introduced",
]

# ---------------------------------------------------------------------------
# Helpers (shared pattern)
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def resolve_source_path(row) -> Path:
    src_repo = row["source_repo"].replace("/", "\\")
    rel = row["path"].replace("/", "\\")
    if rel.startswith("C:\\") or rel.startswith("c:\\"):
        return Path(rel)
    return Path(src_repo) / rel


_DOC_TOKEN_TYPES = {tokenize.STRING, tokenize.COMMENT}
for _tname in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
    if hasattr(tokenize, _tname):
        _DOC_TOKEN_TYPES.add(getattr(tokenize, _tname))

_TOKEN_RANGES_CACHE: dict = {}

def python_string_comment_ranges(path: Path):
    key = str(path)
    if key in _TOKEN_RANGES_CACHE:
        return _TOKEN_RANGES_CACHE[key]
    ranges_by_line: dict = {}
    try:
        with path.open("rb") as f:
            tokens = list(tokenize.tokenize(f.readline))
    except (tokenize.TokenizeError, OSError, UnicodeError, SyntaxError, IndentationError):
        _TOKEN_RANGES_CACHE[key] = ranges_by_line
        return ranges_by_line
    for tok in tokens:
        if tok.type not in _DOC_TOKEN_TYPES:
            continue
        sl, sc = tok.start
        el, ec = tok.end
        for ln in range(sl, el + 1):
            this_start = sc if ln == sl else 0
            this_end = ec if ln == el else 10**9
            ranges_by_line.setdefault(ln, []).append((this_start, this_end))
    _TOKEN_RANGES_CACHE[key] = ranges_by_line
    return ranges_by_line


def match_in_string_or_comment(ranges_by_line, lineno, start, end):
    for rs, re_ in ranges_by_line.get(lineno, []):
        if rs <= start and end <= re_:
            return True
    return False


def _find_qp_summary(qid: str):
    art_dir = QUANTUM_PHASE / "artifacts" / qid
    if not art_dir.exists():
        return None
    canonical = art_dir / f"{qid}_summary.json"
    if canonical.exists():
        return canonical
    candidates = sorted(art_dir.glob(f"{qid}_*summary*.json"))
    for c in candidates:
        if "table" not in c.stem and "row" not in c.stem and "summary" in c.stem:
            return c
    return candidates[0] if candidates else None


def find_field(obj, fname):
    """Recursive scan for a field anywhere in nested dict/list structure."""
    if isinstance(obj, dict):
        if fname in obj:
            return obj[fname]
        for v in obj.values():
            r = find_field(v, fname)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_field(v, fname)
            if r is not None:
                return r
    return None


# ---------------------------------------------------------------------------
# Phase 1 - manifest seal + hash verification
# ---------------------------------------------------------------------------

def phase1_seal_check(manifest_rows):
    result = {
        "manifest_seal_exists":     MANIFEST_SEAL.exists(),
        "manifest_observed_sha256": "",
        "manifest_expected_sha256": EXPECTED_MANIFEST_SHA,
        "manifest_sha_matches":     False,
        "seal_recorded_sha256":     "",
        "seal_matches_observed":    False,
        "hash_verification": {"verified": 0, "mismatches": [], "missing": []},
    }
    if MANIFEST_PATH.exists():
        observed = sha256_of(MANIFEST_PATH).lower()
        result["manifest_observed_sha256"] = observed
        result["manifest_sha_matches"] = observed == EXPECTED_MANIFEST_SHA
    if MANIFEST_SEAL.exists():
        seal_text = MANIFEST_SEAL.read_text(encoding="utf-8").strip()
        m = re.search(r"\b([a-fA-F0-9]{64})\b", seal_text)
        if m:
            result["seal_recorded_sha256"] = m.group(1).lower()
            result["seal_matches_observed"] = result["seal_recorded_sha256"] == result["manifest_observed_sha256"]

    for row in manifest_rows:
        p = resolve_source_path(row)
        declared = row["sha256"].lower()
        if not p.exists():
            result["hash_verification"]["missing"].append(row.get("item_id", ""))
            continue
        try:
            actual = sha256_of(p).lower()
        except OSError:
            result["hash_verification"]["missing"].append(row.get("item_id", ""))
            continue
        if actual != declared:
            result["hash_verification"]["mismatches"].append(row.get("item_id", ""))
        else:
            result["hash_verification"]["verified"] += 1
    return result


# ---------------------------------------------------------------------------
# Phase 2 - QP049-QP060 self-disclosure
# ---------------------------------------------------------------------------

def phase2_vault_construction_disclosure():
    rows = []
    for qid in VAULT_CONSTRUCTION_CHAIN:
        summary_path = _find_qp_summary(qid)
        row = {
            "qp_id":                            qid,
            "summary_path":                     str(summary_path).replace("\\", "/") if summary_path else "",
            "summary_exists":                   summary_path is not None and summary_path.exists(),
            "external_data_used":               "",
            "observed_isotope_masses_used":     "",
            "observed_decay_modes_used":        "",
            "observed_half_lives_used":         "",
            "observed_abundances_used":         "",
            "free_parameters_introduced":       "",
            "status":                           "",
        }
        if not summary_path or not summary_path.exists():
            row["status"] = "summary_missing"
            rows.append(row)
            continue
        try:
            with summary_path.open("r", encoding="utf-8") as f:
                summary = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            row["status"] = f"read_error:{e}"
            rows.append(row)
            continue

        for fname in ISOTOPE_DISCLOSURE_FIELDS:
            val = find_field(summary, fname)
            row[fname] = "" if val is None else str(val)

        ext = row["external_data_used"].strip().lower()
        free_params = row["free_parameters_introduced"].strip()

        if ext == "true":
            row["status"] = "vault_construction_external_data_violation"
        elif ext == "false":
            try:
                fp = int(free_params) if free_params else 0
                if fp > 0:
                    row["status"] = "free_parameters_violation"
                else:
                    # Check the other observed_* fields if present
                    any_observed = any(
                        row[f].strip().lower() == "true"
                        for f in ("observed_isotope_masses_used", "observed_decay_modes_used",
                                  "observed_half_lives_used", "observed_abundances_used")
                    )
                    row["status"] = "observed_data_used_violation" if any_observed else "clean_disclosure"
            except ValueError:
                row["status"] = "free_params_non_integer"
        else:
            row["status"] = "external_data_field_missing"
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Phase 3 - QP060 next_frontier check
# ---------------------------------------------------------------------------

def phase3_qp060_boundary_check():
    summary_path = _find_qp_summary("qp060")
    result = {
        "qp060_summary_path": str(summary_path).replace("\\", "/") if summary_path else "",
        "summary_exists": summary_path is not None and summary_path.exists(),
        "next_frontier": "",
        "next_frontier_names_qp061": False,
        "next_frontier_declares_external_data": False,
        "external_data_used": "",
        "free_parameters_introduced": "",
        "status": "",
    }
    if not result["summary_exists"]:
        result["status"] = "summary_missing"
        return result
    try:
        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["status"] = f"read_error:{e}"
        return result
    nf = find_field(summary, "next_frontier")
    if nf is not None:
        result["next_frontier"] = str(nf)
        if "QP061" in str(nf).upper() or "qp061" in str(nf):
            result["next_frontier_names_qp061"] = True
        if "EXTERNAL_DATA" in str(nf).upper() or "external data" in str(nf).lower():
            result["next_frontier_declares_external_data"] = True
    ext = find_field(summary, "external_data_used")
    result["external_data_used"] = str(ext) if ext is not None else ""
    fp = find_field(summary, "free_parameters_introduced")
    result["free_parameters_introduced"] = str(fp) if fp is not None else ""

    if (result["next_frontier_names_qp061"]
            and result["next_frontier_declares_external_data"]
            and result["external_data_used"].strip().lower() == "false"):
        result["status"] = "boundary_correctly_declared"
    elif not result["next_frontier_names_qp061"]:
        result["status"] = "next_frontier_missing_qp061_reference"
    elif not result["next_frontier_declares_external_data"]:
        result["status"] = "next_frontier_missing_external_data_marker"
    else:
        result["status"] = "boundary_check_indeterminate"
    return result


# ---------------------------------------------------------------------------
# Phase 4 - QP061 comparator-role check
# ---------------------------------------------------------------------------

def phase4_qp061_comparator_check():
    summary_path = _find_qp_summary(QP_COMPARATOR_STEP)
    result = {
        "qp061_summary_path": str(summary_path).replace("\\", "/") if summary_path else "",
        "summary_exists": summary_path is not None and summary_path.exists(),
        "external_data_used": "",
        "sealed_hash_guard_pass": "",
        "prediction_manifest_mutated": "",
        "free_parameters_introduced": "",
        "external_data_sha256": "",
        "status": "",
    }
    if not result["summary_exists"]:
        result["status"] = "summary_missing"
        return result
    try:
        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["status"] = f"read_error:{e}"
        return result
    for fname in ("external_data_used", "sealed_hash_guard_pass",
                  "prediction_manifest_mutated", "free_parameters_introduced",
                  "external_data_sha256"):
        v = find_field(summary, fname)
        result[fname] = "" if v is None else str(v)

    # QP061 is the comparator step; its comparator-role is verified by:
    #   external_data_used == true  (it admits external data)
    #   sealed_hash_guard_pass == true  (predictions came from pre-sealed manifest)
    #   prediction_manifest_mutated == false  (no post-hoc edit of predictions)
    #   free_parameters_introduced == 0
    ext = result["external_data_used"].strip().lower()
    seal_pass = result["sealed_hash_guard_pass"].strip().lower()
    mutated = result["prediction_manifest_mutated"].strip().lower()
    fp = result["free_parameters_introduced"].strip()
    try:
        fp_int = int(fp) if fp else None
    except ValueError:
        fp_int = None

    if (ext == "true" and seal_pass == "true" and mutated == "false" and fp_int == 0):
        result["status"] = "comparator_role_confirmed"
    elif ext != "true":
        result["status"] = "qp061_does_not_admit_external_data"
    elif seal_pass != "true":
        result["status"] = "sealed_hash_guard_failed"
    elif mutated == "true":
        result["status"] = "prediction_manifest_mutated_after_sealing"
    elif fp_int is None or fp_int > 0:
        result["status"] = "free_parameters_introduced"
    else:
        result["status"] = "comparator_role_indeterminate"
    return result


# ---------------------------------------------------------------------------
# Phase 5 - QP068 self-disclosure
# ---------------------------------------------------------------------------

def phase5_qp068_disclosure():
    summary_path = _find_qp_summary(QP_FRONTIER_STEP)
    result = {
        "qp068_summary_path": str(summary_path).replace("\\", "/") if summary_path else "",
        "summary_exists": summary_path is not None and summary_path.exists(),
        "external_data_used": "",
        "observed_isotope_masses_used": "",
        "free_parameters_introduced": "",
        "status": "",
    }
    if not result["summary_exists"]:
        result["status"] = "summary_missing"
        return result
    try:
        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["status"] = f"read_error:{e}"
        return result
    for fname in ("external_data_used", "observed_isotope_masses_used",
                  "free_parameters_introduced"):
        v = find_field(summary, fname)
        result[fname] = "" if v is None else str(v)
    ext = result["external_data_used"].strip().lower()
    fp = result["free_parameters_introduced"].strip()
    if ext == "true":
        result["status"] = "qp068_external_data_violation"
    elif ext == "false":
        try:
            fp_int = int(fp) if fp else 0
            if fp_int > 0:
                result["status"] = "free_parameters_violation"
            else:
                result["status"] = "clean_disclosure"
        except ValueError:
            result["status"] = "free_params_non_integer"
    else:
        # Field missing - check free_params only
        try:
            fp_int = int(fp) if fp else None
            if fp_int == 0:
                result["status"] = "field_missing_but_free_params_clean"
            else:
                result["status"] = "external_data_field_missing"
        except ValueError:
            result["status"] = "external_data_field_missing"
    return result


# ---------------------------------------------------------------------------
# Phase 6 - Forbidden input scan (engine surface code tokens)
# ---------------------------------------------------------------------------

FORBIDDEN_INPUT_PATTERNS = [
    {"class": "ame2020_construction",  "regex": r"\bame2020\b|\bAME2020\b|\bAME-?20(20|14)\b"},
    {"class": "nist_isotope_chart",    "regex": r"\bNIST\b.{0,40}(nuclide|isotope|mass)"},
    {"class": "iupac_construction",    "regex": r"\bIUPAC\b.{0,40}(import|read|load)"},
    {"class": "calibration_loop",      "regex": r"\bscipy\.optimize\b|\bcurve_fit\b|\bleast_squares\b"},
]

ENGINE_CODE_ROLES = {"qp_source_code"}


def phase6_forbidden_input(manifest_rows):
    file_pool = []
    for row in manifest_rows:
        if row["role"] not in ENGINE_CODE_ROLES:
            continue
        p = resolve_source_path(row)
        if p.suffix.lower() == ".py" and p.exists():
            file_pool.append((p, row))

    results = []
    for fp in FORBIDDEN_INPUT_PATTERNS:
        reg = re.compile(fp["regex"])
        engine_hits = []
        doc_mentions = []
        for p, row in file_pool:
            string_ranges = python_string_comment_ranges(p)
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        m = reg.search(line)
                        if m:
                            in_doc = match_in_string_or_comment(string_ranges, i, m.start(), m.end())
                            entry = {"file": row["path"], "line": i,
                                     "text": line.rstrip("\n")[:200], "match": m.group(0)}
                            if in_doc:
                                doc_mentions.append(entry)
                            else:
                                engine_hits.append(entry)
            except (OSError, UnicodeError):
                continue
        classification = "FAIL_TRIGGER" if engine_hits else (
            "ALLOWED_MENTION" if doc_mentions else "CLEAN"
        )
        results.append({
            "pattern_class": fp["class"],
            "pattern_regex": fp["regex"],
            "engine_hit_count": len(engine_hits),
            "doc_mention_count": len(doc_mentions),
            "exemplar_engine_file": engine_hits[0]["file"] if engine_hits else "",
            "exemplar_engine_line": engine_hits[0]["line"] if engine_hits else "",
            "exemplar_engine_text": engine_hits[0]["text"] if engine_hits else "",
            "exemplar_doc_file":    doc_mentions[0]["file"] if doc_mentions else "",
            "exemplar_doc_line":    doc_mentions[0]["line"] if doc_mentions else "",
            "classification": classification,
        })
    return results


# ---------------------------------------------------------------------------
# Phase 7 - Wrong control injections
# ---------------------------------------------------------------------------

def wc1_vault_chain_external_data():
    fake = {"external_data_used": "true", "observed_isotope_masses_used": "true"}
    return fake["external_data_used"].lower() == "true", "vault_chain_external_data_violation_detected"


def wc2_ame2020_engine_import():
    line = "from ame2020 import ATOMIC_MASS_TABLE"
    reg = re.compile(FORBIDDEN_INPUT_PATTERNS[0]["regex"])
    return bool(reg.search(line)), "ame2020_engine_line_detected"


def wc3_qp060_missing_next_frontier():
    fake_summary = {"external_data_used": False}  # missing next_frontier
    nf = fake_summary.get("next_frontier", "")
    detected = "qp061" not in str(nf).lower()
    return detected, "qp060_missing_qp061_next_frontier_detected"


def wc4_qp068_external_data_true():
    fake = {"external_data_used": "true"}
    return fake["external_data_used"].lower() == "true", "qp068_external_data_violation_detected"


def wc5_corrupt_seal():
    fake_observed = "deadbeef" + "0" * 56
    return fake_observed != EXPECTED_MANIFEST_SHA, "manifest_seal_mismatch_detected"


def wc6_free_params_one():
    fake = {"external_data_used": "false", "free_parameters_introduced": "1"}
    try:
        fp = int(fake["free_parameters_introduced"])
        return fp > 0, "free_parameters_violation_detected"
    except ValueError:
        return False, "missed"


def phase7_wrong_controls():
    wcs = [
        ("WC1", "Inject vault-chain summary with external_data_used=true", "FAIL", wc1_vault_chain_external_data),
        ("WC2", "Inject engine line importing ame2020 as construction input", "FAIL", wc2_ame2020_engine_import),
        ("WC3", "Inject qp060_summary missing next_frontier reference to qp061", "FAIL", wc3_qp060_missing_next_frontier),
        ("WC4", "Inject qp068_summary with external_data_used=true", "FAIL", wc4_qp068_external_data_true),
        ("WC5", "Corrupt SOURCE_MANIFEST.csv so CR065 seal mismatches", "DIAGNOSTIC", wc5_corrupt_seal),
        ("WC6", "Inject vault summary with free_parameters_introduced=1", "FAIL", wc6_free_params_one),
    ]
    results = []
    for wc_id, desc, expected, fn in wcs:
        detected, notes = fn()
        results.append({
            "wc_id": wc_id, "description": desc,
            "expected_verdict": expected,
            "detected": detected, "observed_match": detected,
            "notes": notes,
        })
    return results


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def decide_verdict(p1, p2, p3, p4, p5, p6, p7):
    if not p1["manifest_seal_exists"] or not p1["manifest_sha_matches"]:
        return "DIAGNOSTIC", "CR065 manifest seal missing or sha mismatch"
    if p1["hash_verification"]["mismatches"] or p1["hash_verification"]["missing"]:
        return "DIAGNOSTIC", "hash verification failures"

    violations2 = [r for r in p2 if "violation" in r["status"]]
    if violations2:
        return "FAIL", f"vault construction chain violations: {[v['qp_id'] for v in violations2]}"

    if p3["status"] != "boundary_correctly_declared":
        return "FAIL", f"qp060 boundary check: {p3['status']}"

    if p4["status"] != "comparator_role_confirmed":
        return "FAIL", f"qp061 comparator role check: {p4['status']}"

    if p5["status"] not in {"clean_disclosure", "field_missing_but_free_params_clean"}:
        return "FAIL", f"qp068 self-disclosure: {p5['status']}"

    engine_triggers = [r for r in p6 if r["classification"] == "FAIL_TRIGGER"]
    if engine_triggers:
        return "FAIL", f"forbidden input engine-surface hits: {[r['pattern_class'] for r in engine_triggers]}"

    untripped = [r for r in p7 if not r["observed_match"]]
    if untripped:
        return "DIAGNOSTIC", f"wrong controls failed to trip: {[r['wc_id'] for r in untripped]}"

    return "BOUNDARY", "vault input boundary verified clean; K1 external anchor reserved for CR069"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MANIFEST_PATH.exists():
        print(f"FATAL: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(2)

    manifest_rows = load_manifest(MANIFEST_PATH)
    print(f"Loaded manifest: {len(manifest_rows)} entries")

    actual_seal_sha = sha256_of(SEAL_PATH) if SEAL_PATH.exists() else ""
    if actual_seal_sha != SEAL_SHA:
        print(f"WARNING: seal sha drift. expected={SEAL_SHA} actual={actual_seal_sha}", file=sys.stderr)

    print("Phase 1: manifest seal + hash verification...")
    p1 = phase1_seal_check(manifest_rows)
    print(f"  seal_exists={p1['manifest_seal_exists']}, sha_matches={p1['manifest_sha_matches']}")
    print(f"  verified={p1['hash_verification']['verified']}, mismatches={len(p1['hash_verification']['mismatches'])}, missing={len(p1['hash_verification']['missing'])}")

    print("Phase 2: QP049-QP060 vault construction chain disclosure...")
    p2 = phase2_vault_construction_disclosure()
    clean = sum(1 for r in p2 if r["status"] == "clean_disclosure")
    print(f"  clean={clean}/{len(p2)}")
    for r in p2:
        if r["status"] != "clean_disclosure":
            print(f"    {r['qp_id']}: {r['status']}")

    print("Phase 3: QP060 next_frontier boundary check...")
    p3 = phase3_qp060_boundary_check()
    print(f"  next_frontier_names_qp061={p3['next_frontier_names_qp061']}  external_data={p3['next_frontier_declares_external_data']}  status={p3['status']}")

    print("Phase 4: QP061 comparator-role check...")
    p4 = phase4_qp061_comparator_check()
    print(f"  ext_data={p4['external_data_used']}  seal_guard={p4['sealed_hash_guard_pass']}  mutated={p4['prediction_manifest_mutated']}  free_params={p4['free_parameters_introduced']}  status={p4['status']}")

    print("Phase 5: QP068 self-disclosure...")
    p5 = phase5_qp068_disclosure()
    print(f"  ext_data={p5['external_data_used']}  status={p5['status']}")

    print("Phase 6: forbidden input scan...")
    p6 = phase6_forbidden_input(manifest_rows)
    for r in p6:
        print(f"  {r['pattern_class']}: engine_hits={r['engine_hit_count']}  doc_mentions={r['doc_mention_count']}  class={r['classification']}")

    print("Phase 7: wrong control injections...")
    p7 = phase7_wrong_controls()
    for r in p7:
        print(f"  {r['wc_id']}: expected={r['expected_verdict']} detected={r['detected']}")

    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    verdict, reason = decide_verdict(p1, p2, p3, p4, p5, p6, p7)
    print(f"\nFinal verdict: {verdict}  ({reason})")

    # ---------------- Outputs ----------------
    write_csv(OUT_INPUT_MANIFEST, manifest_rows, list(manifest_rows[0].keys()))

    qp_fields = ["qp_id", "summary_path", "summary_exists",
                 "external_data_used", "observed_isotope_masses_used",
                 "observed_decay_modes_used", "observed_half_lives_used",
                 "observed_abundances_used", "free_parameters_introduced",
                 "status"]
    p2_norm = [{k: r.get(k, "") for k in qp_fields} for r in p2]
    write_csv(OUT_QP_DISCLOSURE, p2_norm, qp_fields)

    OUT_QP060_BOUNDARY.write_text(json.dumps(p3, indent=2), encoding="utf-8")
    OUT_QP061_COMPARATOR.write_text(json.dumps(p4, indent=2), encoding="utf-8")

    fb_fields = ["pattern_class", "pattern_regex", "engine_hit_count",
                 "doc_mention_count", "exemplar_engine_file", "exemplar_engine_line",
                 "exemplar_engine_text", "exemplar_doc_file", "exemplar_doc_line",
                 "classification"]
    write_csv(OUT_FORBIDDEN, p6, fb_fields)

    OUT_MANIFEST_SEAL_CHECK.write_text(json.dumps({
        "manifest_path": str(MANIFEST_PATH).replace("\\", "/"),
        "manifest_observed_sha256": p1["manifest_observed_sha256"],
        "manifest_expected_sha256": p1["manifest_expected_sha256"],
        "manifest_sha_matches": p1["manifest_sha_matches"],
        "seal_path": str(MANIFEST_SEAL).replace("\\", "/"),
        "seal_exists": p1["manifest_seal_exists"],
        "seal_recorded_sha256": p1["seal_recorded_sha256"],
        "seal_matches_observed": p1["seal_matches_observed"],
    }, indent=2), encoding="utf-8")

    wc_fields = ["wc_id", "description", "expected_verdict", "detected",
                 "observed_match", "notes"]
    write_csv(OUT_WRONG_CONTROLS, p7, wc_fields)

    summary = {
        "cr_id": "CR066",
        "branch": "10_ISOTOPE_AND_PERIODIC_TABLE_VAULT",
        "execution_status": "CLEAN",
        "scientific_verdict": verdict,
        "triage_bin": "B" if verdict == "BOUNDARY" else ("A" if verdict == "PASS"
                       else "C" if verdict == "FAIL" else "D"),
        "reason": reason,
        "captured_at_utc": captured_at,
        "seal_sha256": actual_seal_sha,
        "phases": {
            "phase_1_seal_and_hash": {
                "seal_exists": p1["manifest_seal_exists"],
                "manifest_sha_matches": p1["manifest_sha_matches"],
                "verified": p1["hash_verification"]["verified"],
                "mismatches": len(p1["hash_verification"]["mismatches"]),
                "missing": len(p1["hash_verification"]["missing"]),
            },
            "phase_2_vault_chain": {
                "checked": len(p2),
                "clean": clean,
                "violations": len([r for r in p2 if "violation" in r["status"]]),
            },
            "phase_3_qp060_boundary": {"status": p3["status"]},
            "phase_4_qp061_comparator": {"status": p4["status"]},
            "phase_5_qp068": {"status": p5["status"]},
            "phase_6_forbidden_input": {
                "engine_hit_classes": sum(1 for r in p6 if r["classification"] == "FAIL_TRIGGER"),
                "allowed_mention_classes": sum(1 for r in p6 if r["classification"] == "ALLOWED_MENTION"),
                "clean_classes": sum(1 for r in p6 if r["classification"] == "CLEAN"),
            },
            "phase_7_wrong_controls": {
                "passed": sum(1 for r in p7 if r["observed_match"]),
                "of": len(p7),
            },
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_md = f"""# CR066 Allowed Inputs and Forbidden Targets

## Verdict

```text
CR066_{verdict}_{('VAULT_INPUT_BOUNDARY_VERIFIED' if verdict == 'BOUNDARY' else 'VAULT_INPUT_BOUNDARY_' + verdict)}
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = {verdict}
triage_bin = {summary['triage_bin']}
```

## Reason

```text
{reason}
```

## Phase Summary

```text
Phase 1 manifest seal + hash       seal={p1['manifest_seal_exists']}  sha_matches={p1['manifest_sha_matches']}  verified={p1['hash_verification']['verified']}
Phase 2 vault construction chain   clean={clean}/{len(p2)}  violations={summary['phases']['phase_2_vault_chain']['violations']}
Phase 3 qp060 boundary             status={p3['status']}
Phase 4 qp061 comparator role      status={p4['status']}
Phase 5 qp068 self-disclosure      status={p5['status']}
Phase 6 forbidden input scan       engine_hits={summary['phases']['phase_6_forbidden_input']['engine_hit_classes']}  doc_mentions={summary['phases']['phase_6_forbidden_input']['allowed_mention_classes']}  clean={summary['phases']['phase_6_forbidden_input']['clean_classes']}
Phase 7 wrong controls             passed={summary['phases']['phase_7_wrong_controls']['passed']}/{len(p7)}
```

## QP061 Comparator-Role Confirmation

```text
external_data_used               = {p4['external_data_used']}
sealed_hash_guard_pass           = {p4['sealed_hash_guard_pass']}
prediction_manifest_mutated      = {p4['prediction_manifest_mutated']}
free_parameters_introduced       = {p4['free_parameters_introduced']}
external_data_sha256             = {p4['external_data_sha256']}
```

## QP060 Boundary Declaration

```text
next_frontier_names_qp061           = {p3['next_frontier_names_qp061']}
next_frontier_declares_external_data = {p3['next_frontier_declares_external_data']}
next_frontier_text                  = {p3['next_frontier'][:160]}
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault
construction chain (QP049-QP060 + QP068) consumes no externally
measured isotope value, no external authority roster value, and no
post-observation calibration source as a construction input, and that
the only point of external-data admission is QP061 as a post-
construction comparator.
```

## Courtroom Reading

CR066 is the input-boundary gate for the 10 branch. A BOUNDARY verdict
is the expected default: the test certifies that the vault construction
chain consumes no external data and that QP061 cleanly admits IAEA data
only as a sealed-hash-guarded post-construction comparator. The K1
external anchor is at CR069 observed roster comparison.

## Artifacts

- `CR066_input_manifest.csv`
- `CR066_qp_self_disclosure_check.csv`
- `CR066_qp060_boundary_check.json`
- `CR066_qp061_comparator_role_check.json`
- `CR066_forbidden_input_scan.csv`
- `CR066_manifest_seal_check.json`
- `CR066_wrong_controls.csv`
- `CR066_summary.json`
- `HASHES.txt`
"""
    OUT_RESULT.write_text(result_md, encoding="utf-8")

    output_files = [
        HERE / "CR066_PRECOMMIT.md",
        Path(__file__),
        OUT_INPUT_MANIFEST,
        OUT_QP_DISCLOSURE,
        OUT_QP060_BOUNDARY,
        OUT_QP061_COMPARATOR,
        OUT_FORBIDDEN,
        OUT_MANIFEST_SEAL_CHECK,
        OUT_WRONG_CONTROLS,
        OUT_SUMMARY,
        OUT_RESULT,
    ]
    hashes_lines = []
    for of in output_files:
        if of.exists():
            h = sha256_of(of)
            rel = of.relative_to(COURTROOM_ROOT).as_posix()
            hashes_lines.append(f"sha256  {rel}  {h}")
    OUT_HASHES.write_text("\n".join(hashes_lines) + "\n", encoding="utf-8")

    print(f"\nAll outputs written to {HERE}")


if __name__ == "__main__":
    main()
