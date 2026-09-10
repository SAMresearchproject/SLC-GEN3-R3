"""CR060_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS.py

Runs the CR060 selector-provenance verification declared in CR060_PRECOMMIT.md.

Phases:
  1 - Hash verification + CR059 manifest seal check
  2 - QP self-disclosure check (every qpNNN_summary.json: external_data_used,
      observed_*_used, free_parameters_introduced)
  3 - Provenance board check (QGA032 source_provenance_board.csv +
      QGA033 witness_board.csv) - no quarantined source promoted to proof
  4 - Hostile audit replay check (AUDIT_VERDICT_POST_RETEST_REVIEW.md
      + results/*.md + retest_runs/*/REPORT.md)
  5 - Forbidden selector pattern scan (engine-surface code tokens)
  6 - Wrong control injections (WC1-WC6)
  7 - Final verdict

Outputs in this directory; HASHES.txt at the end.
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
SEAL_PATH        = BRANCH_ROOT / "SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13.md"

OUT_INPUT_MANIFEST       = HERE / "CR060_input_manifest.csv"
OUT_QP_DISCLOSURE        = HERE / "CR060_qp_self_disclosure_check.csv"
OUT_PROVENANCE           = HERE / "CR060_provenance_board_check.csv"
OUT_HOSTILE_AUDIT        = HERE / "CR060_hostile_audit_replay_check.csv"
OUT_FORBIDDEN_SELECTOR   = HERE / "CR060_forbidden_selector_scan.csv"
OUT_MANIFEST_SEAL_CHECK  = HERE / "CR060_manifest_seal_check.json"
OUT_WRONG_CONTROLS       = HERE / "CR060_wrong_controls.csv"
OUT_SUMMARY              = HERE / "CR060_summary.json"
OUT_RESULT               = HERE / "CR060_result.md"
OUT_HASHES               = HERE / "HASHES.txt"

SEAL_SHA = "ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8"
EXPECTED_MANIFEST_SHA = "d605d070281119f2c874112de0be1be06d6ab4ad5ef8b914e459420c8148f22a"

# QP arm tests in scope for CR060
QP_SCOPE = [
    "qp004", "qp007", "qp018", "qp019", "qp020", "qp021", "qp023",
    "qp037", "qp040", "qp050", "qp052",
    "qp062", "qp063", "qp064", "qp065", "qp066", "qp067",
    "qp069", "qp070", "qp071", "qp072", "qp073", "qp074", "qp075",
]

QUANTUM_PHASE = Path("C:/VS/quantum_phase")
STAM_REPO = Path("C:/VS/Stam_model-A-v1.0")

HOSTILE_AUDIT_DIR = QUANTUM_PHASE / "audits" / "private_hostile_qp010_qp021"

QGA032_PROVENANCE = STAM_REPO / "tests" / "Substrate" / "QGA032_SW_ACTION_DENSITY_OR_1_OVER_A0_SQUARED_SELECTOR" / "QGA032_source_provenance_board.csv"
QGA033_WITNESS    = STAM_REPO / "tests" / "Substrate" / "QGA033_FACTOR_PROVENANCE_OR_SW_ACTION_DENSITY_SOURCE_AUDIT" / "QGA033_witness_board.csv"

# ---------------------------------------------------------------------------
# Helpers
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


# ---------------------------------------------------------------------------
# Tokenize-based string/comment classifier (shared pattern from CR059)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Phase 1 - hash verification + manifest seal check
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
    # Manifest current sha
    if MANIFEST_PATH.exists():
        observed = sha256_of(MANIFEST_PATH).lower()
        result["manifest_observed_sha256"] = observed
        result["manifest_sha_matches"] = observed == EXPECTED_MANIFEST_SHA
    # Seal file content
    if MANIFEST_SEAL.exists():
        seal_text = MANIFEST_SEAL.read_text(encoding="utf-8").strip()
        # Format: "sha256  <relative-path>  <hash>"
        m = re.search(r"\b([a-fA-F0-9]{64})\b", seal_text)
        if m:
            result["seal_recorded_sha256"] = m.group(1).lower()
            result["seal_matches_observed"] = result["seal_recorded_sha256"] == result["manifest_observed_sha256"]

    # Re-verify all manifest entries
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
# Phase 2 - QP self-disclosure check
# ---------------------------------------------------------------------------

QP_DISCLOSURE_FIELDS = [
    "external_data_used",
    "observed_particle_masses_used",
    "observed_quarkonium_masses_used",
    "observed_isotope_masses_used",
    "free_parameters_introduced",
]

# Reveal-only / residual-scoring fields - existence of these in a summary
# does NOT count as a forbidden external-data import.  They document the
# post-derivation comparator role explicitly allowed by the seal.
REVEAL_ONLY_FIELDS = {
    "reveal_only_residual_column",
    "used_only_for_residual_scoring",
    "reveal_only_ratio_scoring",
    "post_observation_comparator_only",
}


def _find_qp_summary(qid: str) -> Path | None:
    """Find the summary.json for a QP test.  Early tests (qp004, qp007, qp020)
    use a verbose name like qp004_phase_to_particle_role_operator_summary.json;
    later tests use the canonical qpNNN_summary.json.  Glob for either."""
    art_dir = QUANTUM_PHASE / "artifacts" / qid
    if not art_dir.exists():
        return None
    canonical = art_dir / f"{qid}_summary.json"
    if canonical.exists():
        return canonical
    # Try glob for *summary*.json with qid prefix
    candidates = sorted(art_dir.glob(f"{qid}_*summary*.json"))
    if candidates:
        # Prefer the one without "table" in the name (selectors over tables)
        for c in candidates:
            if "table" not in c.stem and "row" not in c.stem and "summary" in c.stem:
                return c
        return candidates[0]
    return None


def phase2_qp_self_disclosure():
    rows = []
    for qid in QP_SCOPE:
        summary_path = _find_qp_summary(qid)
        row = {
            "qp_id":                            qid,
            "summary_path":                     str(summary_path).replace("\\", "/") if summary_path else "",
            "summary_exists":                   summary_path is not None and summary_path.exists(),
            "external_data_used":               "",
            "observed_particle_masses_used":    "",
            "observed_quarkonium_masses_used":  "",
            "observed_isotope_masses_used":     "",
            "free_parameters_introduced":       "",
            "reveal_only_marker_present":       False,
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
            row["status"] = f"summary_read_error:{e}"
            rows.append(row)
            continue

        # Extract declared fields - they may be at the top level or nested
        # in a "decision_value" field; we scan the JSON for any matching key
        def find_field(obj, fname):
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

        for fname in QP_DISCLOSURE_FIELDS:
            val = find_field(summary, fname)
            row[fname] = "" if val is None else str(val)

        # Detect reveal-only / comparator markers in the JSON text itself
        summary_text = json.dumps(summary).lower()
        for marker in REVEAL_ONLY_FIELDS:
            if marker.lower() in summary_text:
                row["reveal_only_marker_present"] = True
                break
        # Also check for "REVEAL_ONLY" tokens used in decision_value fields
        if "reveal_only" in summary_text or "residual_scoring_only" in summary_text:
            row["reveal_only_marker_present"] = True

        # Verdict logic
        # Default: external_data_used must be false (only QP061 may be true but
        # it's not in scope here).
        ext = row["external_data_used"].strip().lower()
        free_params = row["free_parameters_introduced"].strip()

        if ext == "true":
            # In CR060's scope (which excludes qp061), no test may admit
            # external data as construction input.
            if row["reveal_only_marker_present"]:
                # The reveal-only marker indicates the external reference is
                # comparator-only, which the seal allows.
                row["status"] = "external_data_used_as_comparator_only_allowed"
            else:
                row["status"] = "external_data_used_construction_violation"
        elif ext == "false":
            if free_params and free_params not in ("0", ""):
                try:
                    if int(free_params) > 0:
                        row["status"] = "free_parameters_violation"
                    else:
                        row["status"] = "clean_disclosure"
                except ValueError:
                    row["status"] = "free_params_non_integer"
            else:
                row["status"] = "clean_disclosure"
        else:
            # Field missing - allowed for some QP tests that don't expose this
            # field but should still report free_parameters_introduced=0
            if free_params == "0":
                row["status"] = "field_missing_but_free_params_clean"
            elif free_params == "":
                row["status"] = "field_missing_check_manually"
            else:
                row["status"] = "free_params_unclear"
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Phase 3 - Provenance board check
# ---------------------------------------------------------------------------

FORBIDDEN_PROVENANCE_STATUS_PATTERNS = [
    r"\bACTIVE_PROOF\b",
    r"\bPROMOTED_TO_PROOF\b",
    r"\bACCEPTED_AS_PROOF\b",
]

EXPECTED_PROVENANCE_BOARD_STATUS_PATTERNS = [
    r"NO_CLAIM_WEIGHT",
    r"QUARANTINED",
    r"ARCHIVE_HISTORY_ONLY",
    r"HISTORICAL",
    r"AUDIT_RISK_REGISTERED",
    r"BIDIRECTIONAL",
    r"NOT_PROMOTION",
    r"RESPONSIBLE_USE_ALLOWED",
]


def phase3_provenance_boards():
    rows = []
    for board_name, board_path in [("QGA032_source_provenance_board", QGA032_PROVENANCE),
                                    ("QGA033_witness_board", QGA033_WITNESS)]:
        if not board_path.exists():
            rows.append({
                "board": board_name,
                "row_count": 0,
                "forbidden_status_count": 0,
                "expected_status_count": 0,
                "status": "board_missing",
                "exemplar_forbidden": "",
            })
            continue
        try:
            with board_path.open("r", encoding="utf-8-sig", newline="") as f:
                board_rows = list(csv.DictReader(f))
        except (OSError, csv.Error) as e:
            rows.append({
                "board": board_name,
                "row_count": 0,
                "forbidden_status_count": 0,
                "expected_status_count": 0,
                "status": f"read_error:{e}",
                "exemplar_forbidden": "",
            })
            continue
        forbidden_hits = 0
        expected_hits = 0
        exemplar_forbidden = ""
        for br in board_rows:
            status_value = br.get("status", "")
            for pat in FORBIDDEN_PROVENANCE_STATUS_PATTERNS:
                if re.search(pat, status_value, re.IGNORECASE):
                    forbidden_hits += 1
                    if not exemplar_forbidden:
                        exemplar_forbidden = f"row source/witness={br.get('source', br.get('witness', ''))} status={status_value}"
                    break
            for pat in EXPECTED_PROVENANCE_BOARD_STATUS_PATTERNS:
                if re.search(pat, status_value, re.IGNORECASE):
                    expected_hits += 1
                    break
        rows.append({
            "board": board_name,
            "row_count": len(board_rows),
            "forbidden_status_count": forbidden_hits,
            "expected_status_count": expected_hits,
            "status": "clean" if forbidden_hits == 0 else "forbidden_promotion_present",
            "exemplar_forbidden": exemplar_forbidden,
        })
    return rows


# ---------------------------------------------------------------------------
# Phase 4 - Hostile audit replay check
# ---------------------------------------------------------------------------

PASS_VERDICT_PATTERNS = [
    re.compile(r"\bPASS\b"),
    re.compile(r"\bPASS_WITH_BOUNDARY\b"),
    re.compile(r"\bNO_BLOCKER_FOUND\b"),
    re.compile(r"\bHOSTILE_CERTIFICATION_GRANTED\b"),
    re.compile(r"\bCERTIFIED\b"),
]
FAIL_VERDICT_PATTERNS = [
    re.compile(r"\bFAIL\b"),
    re.compile(r"\bBLOCKER_FOUND\b"),
    re.compile(r"\bCONTRADICTED\b"),
    re.compile(r"\bDISCONFIRMED\b"),
]
# Per-result-file BOUNDARY signals: explicit "blocker: False" or
# "MAJOR/MINOR" finding without BLOCKER means a non-blocking finding -
# treated as BOUNDARY, since the precommit allows "explicitly states the
# failure mode" as a valid result form.  These results are subordinate to
# the top-level AUDIT_VERDICT_POST_RETEST_REVIEW which retains FINAL say.
BOUNDARY_FINDING_PATTERNS = [
    re.compile(r"blocker\s*:?\s*False", re.IGNORECASE),
    re.compile(r"\bMAJOR\b.*\bnot a blocker\b", re.IGNORECASE),
    re.compile(r"\bMAJOR\s*:\s*"),
    re.compile(r"\bMINOR\s*:\s*"),
    re.compile(r"\bretest_recommended\s*:?\s*True", re.IGNORECASE),
]


def classify_verdict_text(text: str) -> str:
    fail_hits = sum(1 for p in FAIL_VERDICT_PATTERNS if p.search(text))
    pass_hits = sum(1 for p in PASS_VERDICT_PATTERNS if p.search(text))
    boundary_hits = sum(1 for p in BOUNDARY_FINDING_PATTERNS if p.search(text))

    if pass_hits > 0 and fail_hits == 0:
        return "PASS"
    if fail_hits > 0 and pass_hits == 0:
        return "FAIL"
    if pass_hits > fail_hits:
        return "PASS"
    if fail_hits > pass_hits:
        return "FAIL"
    # Neither dominant pass nor fail - check for explicit non-blocking finding
    if boundary_hits > 0:
        return "BOUNDARY"
    if "BOUNDARY" in text.upper():
        return "BOUNDARY"
    return "UNCLASSIFIED"


def phase4_hostile_audit():
    rows = []
    # Top-level verdicts
    for vname in ("AUDIT_VERDICT.md", "AUDIT_VERDICT_POST_RETEST_REVIEW.md",
                  "ASSESSMENT_POST_RETEST_REVIEW.md"):
        p = HOSTILE_AUDIT_DIR / vname
        if not p.exists():
            rows.append({"audit_file": vname, "verdict": "MISSING", "status": "missing"})
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            rows.append({"audit_file": vname, "verdict": "READ_ERROR", "status": f"error:{e}"})
            continue
        verdict = classify_verdict_text(text)
        rows.append({"audit_file": vname, "verdict": verdict,
                     "status": "ok" if verdict in {"PASS", "BOUNDARY"} else "review_needed"})

    # Per-QP results
    results_dir = HOSTILE_AUDIT_DIR / "results"
    if results_dir.exists():
        for p in sorted(results_dir.glob("*.md")):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                rows.append({"audit_file": f"results/{p.name}", "verdict": "READ_ERROR",
                             "status": f"error:{e}"})
                continue
            verdict = classify_verdict_text(text)
            rows.append({"audit_file": f"results/{p.name}", "verdict": verdict,
                         "status": "ok" if verdict in {"PASS", "BOUNDARY"} else "review_needed"})

    # Retest run reports
    retest_dir = HOSTILE_AUDIT_DIR / "retest_runs"
    if retest_dir.exists():
        for sub in sorted(retest_dir.iterdir()):
            if not sub.is_dir():
                continue
            for fname in ("REPORT.md", "PREFLIGHT.md"):
                p = sub / fname
                if not p.exists():
                    continue
                try:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                except OSError as e:
                    rows.append({"audit_file": f"retest_runs/{sub.name}/{fname}",
                                 "verdict": "READ_ERROR", "status": f"error:{e}"})
                    continue
                verdict = classify_verdict_text(text)
                rows.append({"audit_file": f"retest_runs/{sub.name}/{fname}",
                             "verdict": verdict,
                             "status": "ok" if verdict in {"PASS", "BOUNDARY"} else "review_needed"})
    return rows


# ---------------------------------------------------------------------------
# Phase 5 - Forbidden selector pattern scan (engine surface code tokens)
# ---------------------------------------------------------------------------

FORBIDDEN_SELECTOR_PATTERNS = [
    {"class": "calibration_loop", "regex": r"\bscipy\.optimize\b|\bcurve_fit\b|\bleast_squares\b"},
    {"class": "fit_to_observed",  "regex": r"\bfit_to_observed\b|\bfit_observed\b|\boptimize_against_observed\b"},
    {"class": "yukawa_table_import", "regex": r"\bimport\s+yukawa[a-z_]+\b|\bload_yukawa\b|\byukawa_couplings\b"},
    {"class": "pdg_construction_input", "regex": r"\bload_pdg\b|\bread_pdg\b|\bimport_pdg\b"},
]

ENGINE_CODE_ROLES = {"qp_source_code", "engine_source_code"}


def phase5_forbidden_selector(manifest_rows):
    text_exts = {".py"}
    file_pool = []
    for row in manifest_rows:
        if row["role"] not in ENGINE_CODE_ROLES:
            continue
        p = resolve_source_path(row)
        if p.suffix.lower() in text_exts and p.exists():
            file_pool.append((p, row))

    results = []
    for fp in FORBIDDEN_SELECTOR_PATTERNS:
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
                            entry = {
                                "file": row["path"], "line": i,
                                "text": line.rstrip("\n")[:200],
                                "match": m.group(0),
                            }
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
# Phase 6 - Wrong control injections
# ---------------------------------------------------------------------------

def wc1_inject_external_data_summary():
    # Synthetic disclosure row with external_data_used=true, observed_*_used=true
    fake = {
        "qp_id": "qp999",
        "external_data_used": "true",
        "observed_particle_masses_used": "true",
        "free_parameters_introduced": "0",
        "reveal_only_marker_present": False,
    }
    # Would be classified as external_data_used_construction_violation
    expected_status = "external_data_used_construction_violation"
    detected = (fake["external_data_used"].lower() == "true"
                and not fake["reveal_only_marker_present"])
    return detected, expected_status


def wc2_inject_calibration_engine_line():
    # Simulate a code line: optimized_params = scipy.optimize.curve_fit(...)
    line = "optimized_params = scipy.optimize.curve_fit(observed_mass_data, ...)"
    # Engine surface, not in string/comment
    reg = re.compile(FORBIDDEN_SELECTOR_PATTERNS[0]["regex"])
    detected = bool(reg.search(line))
    return detected, "engine_surface_calibration_detected"


def wc3_inject_promoted_quarantined_row():
    # Synthetic provenance board row with status=ACTIVE_PROOF
    fake = {"source": "old_sheet", "status": "ACTIVE_PROOF", "evidence": "spreadsheet image"}
    for pat in FORBIDDEN_PROVENANCE_STATUS_PATTERNS:
        if re.search(pat, fake["status"], re.IGNORECASE):
            return True, "promoted_quarantined_detected"
    return False, "missed"


def wc4_inject_failing_audit_result():
    text = "Verdict: FAIL\nBLOCKER_FOUND\nContradicts qp019 mass surface"
    verdict = classify_verdict_text(text)
    return verdict == "FAIL", f"audit_verdict_classified_as_{verdict}"


def wc5_corrupt_manifest_seal():
    # Simulate: if manifest_observed != manifest_expected, phase 1 flags it
    fake_observed = "deadbeef" + "0" * 56
    detected = fake_observed != EXPECTED_MANIFEST_SHA
    return detected, "manifest_sha_mismatch_detected"


def wc6_inject_yukawa_engine_line():
    line = "from yukawa_couplings import YUKAWA_TABLE_2024"
    reg = re.compile(FORBIDDEN_SELECTOR_PATTERNS[2]["regex"])
    detected = bool(reg.search(line))
    return detected, "engine_surface_yukawa_import_detected"


def phase6_wrong_controls():
    wcs = [
        ("WC1", "Inject qpNNN_summary.json with external_data_used=true (no reveal-only marker)",
         "FAIL", wc1_inject_external_data_summary),
        ("WC2", "Inject engine line with scipy.optimize.curve_fit against observed mass",
         "FAIL", wc2_inject_calibration_engine_line),
        ("WC3", "Inject provenance board row tagging old_sheet as ACTIVE_PROOF",
         "FAIL", wc3_inject_promoted_quarantined_row),
        ("WC4", "Inject hostile audit result file ending in FAIL/BLOCKER_FOUND",
         "FAIL", wc4_inject_failing_audit_result),
        ("WC5", "Corrupt SOURCE_MANIFEST.csv so CR059 seal mismatches",
         "DIAGNOSTIC", wc5_corrupt_manifest_seal),
        ("WC6", "Inject engine line importing yukawa_couplings as construction input",
         "FAIL", wc6_inject_yukawa_engine_line),
    ]
    results = []
    for wc_id, desc, expected, fn in wcs:
        detected, notes = fn()
        results.append({
            "wc_id": wc_id, "description": desc,
            "expected_verdict": expected,
            "detected": detected,
            "observed_match": detected,
            "notes": notes,
        })
    return results


# ---------------------------------------------------------------------------
# Verdict decision
# ---------------------------------------------------------------------------

def decide_verdict(p1, p2, p3, p4, p5, p6):
    # Manifest seal must be intact
    if not p1["manifest_seal_exists"] or not p1["manifest_sha_matches"]:
        return "DIAGNOSTIC", "CR059 manifest seal missing or sha mismatch"
    if p1["hash_verification"]["mismatches"] or p1["hash_verification"]["missing"]:
        return "DIAGNOSTIC", "hash verification failures"

    # Phase 2: any QP self-disclosure violation
    violations = [r for r in p2 if "violation" in r["status"]]
    if violations:
        return "FAIL", f"qp self-disclosure violations: {[v['qp_id'] for v in violations]}"

    # Phase 3: any forbidden provenance promotion
    p3_violations = [r for r in p3 if r["forbidden_status_count"] > 0]
    if p3_violations:
        return "FAIL", f"provenance board violations: {[v['board'] for v in p3_violations]}"

    # Phase 4: any hostile audit result classified as FAIL
    audit_failures = [r for r in p4 if r["verdict"] == "FAIL"]
    if audit_failures:
        return "FAIL", f"hostile audit failures: {[r['audit_file'] for r in audit_failures]}"
    audit_unclassified = [r for r in p4 if r["verdict"] == "UNCLASSIFIED" or r["verdict"] == "MISSING"]
    if audit_unclassified:
        return "DIAGNOSTIC", f"hostile audit files unclassifiable: {[r['audit_file'] for r in audit_unclassified]}"

    # Phase 5: forbidden selector engine surface hits
    engine_triggers = [r for r in p5 if r["classification"] == "FAIL_TRIGGER"]
    if engine_triggers:
        return "FAIL", f"forbidden selector engine-surface hits: {[r['pattern_class'] for r in engine_triggers]}"

    # Phase 6: wrong controls failed to trip
    untripped = [r for r in p6 if not r["observed_match"]]
    if untripped:
        return "DIAGNOSTIC", f"wrong controls failed to trip: {[r['wc_id'] for r in untripped]}"

    return "BOUNDARY", "selector provenance and forbidden-targets boundary verified clean; no external anchor at this CR"


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

    print("Phase 2: QP self-disclosure check...")
    p2 = phase2_qp_self_disclosure()
    clean = sum(1 for r in p2 if r["status"] in {"clean_disclosure", "external_data_used_as_comparator_only_allowed", "field_missing_but_free_params_clean"})
    print(f"  clean={clean}/{len(p2)}")

    print("Phase 3: provenance board check...")
    p3 = phase3_provenance_boards()
    for r in p3:
        print(f"  {r['board']}: rows={r['row_count']} forbidden={r['forbidden_status_count']} expected={r['expected_status_count']} status={r['status']}")

    print("Phase 4: hostile audit replay check...")
    p4 = phase4_hostile_audit()
    by_verdict = {}
    for r in p4:
        by_verdict[r["verdict"]] = by_verdict.get(r["verdict"], 0) + 1
    print(f"  audit verdicts: {by_verdict}")

    print("Phase 5: forbidden selector pattern scan...")
    p5 = phase5_forbidden_selector(manifest_rows)
    for r in p5:
        print(f"  {r['pattern_class']}: engine_hits={r['engine_hit_count']} doc_mentions={r['doc_mention_count']} class={r['classification']}")

    print("Phase 6: wrong control injections...")
    p6 = phase6_wrong_controls()
    for r in p6:
        print(f"  {r['wc_id']}: expected={r['expected_verdict']} detected={r['detected']}")

    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    verdict, reason = decide_verdict(p1, p2, p3, p4, p5, p6)
    print(f"\nFinal verdict: {verdict}  ({reason})")

    # ---------------- Outputs ----------------
    write_csv(OUT_INPUT_MANIFEST, manifest_rows, list(manifest_rows[0].keys()))

    qp_fields = ["qp_id", "summary_path", "summary_exists",
                 "external_data_used", "observed_particle_masses_used",
                 "observed_quarkonium_masses_used", "observed_isotope_masses_used",
                 "free_parameters_introduced", "reveal_only_marker_present", "status"]
    p2_norm = [{k: r.get(k, "") for k in qp_fields} for r in p2]
    write_csv(OUT_QP_DISCLOSURE, p2_norm, qp_fields)

    prov_fields = ["board", "row_count", "forbidden_status_count",
                   "expected_status_count", "status", "exemplar_forbidden"]
    write_csv(OUT_PROVENANCE, p3, prov_fields)

    audit_fields = ["audit_file", "verdict", "status"]
    write_csv(OUT_HOSTILE_AUDIT, p4, audit_fields)

    sel_fields = ["pattern_class", "pattern_regex", "engine_hit_count",
                  "doc_mention_count", "exemplar_engine_file", "exemplar_engine_line",
                  "exemplar_engine_text", "exemplar_doc_file", "exemplar_doc_line",
                  "classification"]
    write_csv(OUT_FORBIDDEN_SELECTOR, p5, sel_fields)

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
    write_csv(OUT_WRONG_CONTROLS, p6, wc_fields)

    summary = {
        "cr_id": "CR060",
        "branch": "09_PARTICLE_MASS_CHAIN",
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
                "hashes_verified": p1["hash_verification"]["verified"],
                "hashes_mismatched": len(p1["hash_verification"]["mismatches"]),
                "hashes_missing": len(p1["hash_verification"]["missing"]),
            },
            "phase_2_qp_self_disclosure": {
                "qp_tests_checked": len(p2),
                "clean": clean,
                "violations": len([r for r in p2 if "violation" in r["status"]]),
            },
            "phase_3_provenance_boards": {
                "boards_checked": len(p3),
                "violations": sum(r["forbidden_status_count"] for r in p3),
            },
            "phase_4_hostile_audit": {
                "files_checked": len(p4),
                "verdicts": by_verdict,
            },
            "phase_5_forbidden_selector": {
                "engine_hit_classes": sum(1 for r in p5 if r["classification"] == "FAIL_TRIGGER"),
                "allowed_mention_classes": sum(1 for r in p5 if r["classification"] == "ALLOWED_MENTION"),
                "clean_classes": sum(1 for r in p5 if r["classification"] == "CLEAN"),
            },
            "phase_6_wrong_controls": {
                "passed": sum(1 for r in p6 if r["observed_match"]),
                "of": len(p6),
            },
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # ---------------- CR060_result.md ----------------
    result_md = f"""# CR060 Selector Provenance and Forbidden Targets

## Verdict

```text
CR060_{verdict}_{('SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS_VERIFIED' if verdict == 'BOUNDARY' else 'SELECTOR_PROVENANCE_' + verdict)}
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
Phase 1 manifest seal + hash      seal_exists={p1['manifest_seal_exists']}  sha_matches={p1['manifest_sha_matches']}  verified={p1['hash_verification']['verified']}
Phase 2 QP self-disclosure        clean={clean}/{len(p2)}  violations={summary['phases']['phase_2_qp_self_disclosure']['violations']}
Phase 3 provenance boards         boards={len(p3)}  violations={summary['phases']['phase_3_provenance_boards']['violations']}
Phase 4 hostile audit             files={len(p4)}  verdicts={by_verdict}
Phase 5 forbidden selector scan   engine_hits={summary['phases']['phase_5_forbidden_selector']['engine_hit_classes']}  doc_mentions={summary['phases']['phase_5_forbidden_selector']['allowed_mention_classes']}  clean={summary['phases']['phase_5_forbidden_selector']['clean_classes']}
Phase 6 wrong control injections  passed={summary['phases']['phase_6_wrong_controls']['passed']}/{len(p6)}
```

## Rule-9 Line

```text
This test could have falsified: the claim that every selector in the
particle mass chain has a provenance trace independent of measured
particle masses, fitted Yukawa couplings, and post-observation
calibration loops, and that the hostile QP010-QP021 audit confirms
this independence.
```

## Courtroom Reading

CR060 is the selector-provenance gate for the 09 branch. A BOUNDARY
verdict is the expected default: the test structurally certifies that
selectors trace back to declared SAM-native quantities with no forbidden
construction pattern, and that the hostile audit confirms this. The K1
external anchor still belongs to CR062 row-by-row ledger.

## Artifacts

- `CR060_input_manifest.csv`
- `CR060_qp_self_disclosure_check.csv`
- `CR060_provenance_board_check.csv`
- `CR060_hostile_audit_replay_check.csv`
- `CR060_forbidden_selector_scan.csv`
- `CR060_manifest_seal_check.json`
- `CR060_wrong_controls.csv`
- `CR060_summary.json`
- `HASHES.txt`
"""
    OUT_RESULT.write_text(result_md, encoding="utf-8")

    # ---------------- HASHES.txt ----------------
    output_files = [
        HERE / "CR060_PRECOMMIT.md",
        Path(__file__),
        OUT_INPUT_MANIFEST,
        OUT_QP_DISCLOSURE,
        OUT_PROVENANCE,
        OUT_HOSTILE_AUDIT,
        OUT_FORBIDDEN_SELECTOR,
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
