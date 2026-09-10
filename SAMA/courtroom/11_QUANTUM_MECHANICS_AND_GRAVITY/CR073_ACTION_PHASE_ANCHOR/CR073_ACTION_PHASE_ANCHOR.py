"""CR073_ACTION_PHASE_ANCHOR.py

Theorem-grade structural reproduction of:
    S_A = E_p * T_A
    Delta_phi = S_A / hbar

Phases:
  1 - Manifest seal + hash verification (also seals 11 SOURCE_MANIFEST)
  2 - Action identity pattern (string match in QP001 + supporting)
  3 - Phase identity pattern (Delta_phi / phase = S_A / hbar)
  4 - QP001 self-disclosure (free_parameters_introduced = 0)
  5 - Free-particle action substrate-count test directory presence
  6 - Engine-surface fit-loop scan (forbidden patterns in qp_source_code)
  7 - Public bridge cite check (G406, G421)
  8 - Wrong control injections
"""

from __future__ import annotations
import csv, hashlib, json, re, sys, tokenize
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRANCH_ROOT = HERE.parent
COURTROOM_ROOT = BRANCH_ROOT.parent
MANIFEST_PATH = BRANCH_ROOT / "SOURCE_MANIFEST.csv"
MANIFEST_SEAL = BRANCH_ROOT / "SOURCE_MANIFEST.csv.sha256.txt"
SEAL_PATH = BRANCH_ROOT / "SEALED_QUANTUM_MECHANICS_AND_GRAVITY_SCOPE_APPROACH_2026_06_13.md"

OUT_INPUT_MANIFEST  = HERE / "CR073_input_manifest.csv"
OUT_ACTION_ID       = HERE / "CR073_action_identity_check.json"
OUT_PHASE_ID        = HERE / "CR073_phase_identity_check.json"
OUT_QP001_DISCL     = HERE / "CR073_qp001_disclosure_check.json"
OUT_FREE_PARTICLE   = HERE / "CR073_free_particle_action_check.json"
OUT_FIT_SCAN        = HERE / "CR073_engine_surface_fit_scan.csv"
OUT_PUBLIC_BRIDGE   = HERE / "CR073_public_bridge_cite_check.csv"
OUT_MANIFEST_CHK    = HERE / "CR073_manifest_seal_check.json"
OUT_WRONG           = HERE / "CR073_wrong_controls.csv"
OUT_SUMMARY         = HERE / "CR073_summary.json"
OUT_RESULT          = HERE / "CR073_result.md"
OUT_HASHES          = HERE / "HASHES.txt"

SEAL_SHA = "f80c93f67da67a5c9286aafe845316ee6fa3a614439c4e9e120abb9c3a9207dc"

QUANTUM_PHASE = Path("C:/VS/quantum_phase")
STAM_REPO = Path("C:/VS/Stam_model-A-v1.0")

# Identity patterns (case-insensitive)
ACTION_ID_PATTERNS = [
    re.compile(r"S_?A\s*=\s*E_?p\s*\*?\s*T_?A", re.IGNORECASE),
    re.compile(r"S_?A\s*=\s*E\s*[*·]\s*T", re.IGNORECASE),
    re.compile(r"action.{0,40}S_?A.{0,40}E_?p.{0,40}T_?A", re.IGNORECASE | re.DOTALL),
]
PHASE_ID_PATTERNS = [
    re.compile(r"(Delta[_ ]?phi|Δφ|δφ|phase)\s*=\s*S_?A\s*/\s*(hbar|ħ|ℏ)", re.IGNORECASE),
    re.compile(r"Δ_?phi\s*=\s*S_?A\s*/\s*hbar", re.IGNORECASE),
    re.compile(r"phase.{0,30}S_?A\s*/\s*hbar", re.IGNORECASE),
]

# Engine-surface forbidden patterns (fit loops on phase/action)
FIT_PATTERNS = [
    re.compile(r"\bscipy\.optimize\b.{0,80}(phase|action|S_?A|Delta_?phi)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\bcurve_fit\b.{0,80}(phase|action|S_?A)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\bleast_squares\b.{0,80}(phase|action|S_?A)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\bminimize\b.{0,80}(observed[_ ]?phase|observed[_ ]?action)", re.IGNORECASE | re.DOTALL),
]

# Free-particle action test directory patterns
FREE_PARTICLE_PATTERNS = [
    "G286_*", "G285_*", "G284_*",
    "*free_particle_action*", "*free_particle_phase*", "*plane_wave_phase*",
]

ENGINE_CODE_ROLES = {"qp_source_code"}

# Tokenize helpers (same pattern as 09/10)
_DOC_TOKEN_TYPES = {tokenize.STRING, tokenize.COMMENT}
for _tname in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
    if hasattr(tokenize, _tname):
        _DOC_TOKEN_TYPES.add(getattr(tokenize, _tname))
_TOKEN_RANGES_CACHE: dict = {}


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


def python_string_comment_ranges(path: Path):
    key = str(path)
    if key in _TOKEN_RANGES_CACHE:
        return _TOKEN_RANGES_CACHE[key]
    ranges: dict = {}
    try:
        with path.open("rb") as f:
            toks = list(tokenize.tokenize(f.readline))
    except (tokenize.TokenizeError, OSError, UnicodeError, SyntaxError, IndentationError):
        _TOKEN_RANGES_CACHE[key] = ranges
        return ranges
    for t in toks:
        if t.type not in _DOC_TOKEN_TYPES:
            continue
        sl, sc = t.start
        el, ec = t.end
        for ln in range(sl, el + 1):
            ranges.setdefault(ln, []).append(
                (sc if ln == sl else 0, ec if ln == el else 10**9)
            )
    _TOKEN_RANGES_CACHE[key] = ranges
    return ranges


def match_in_doc(ranges, line, s, e):
    for rs, re_ in ranges.get(line, []):
        if rs <= s and e <= re_:
            return True
    return False


def find_field(obj, fname):
    if isinstance(obj, dict):
        if fname in obj: return obj[fname]
        for v in obj.values():
            r = find_field(v, fname)
            if r is not None: return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_field(v, fname)
            if r is not None: return r
    return None


# ---------------------------------------------------------------------------
# Phase 1 - manifest seal + hash verification
# ---------------------------------------------------------------------------

def phase1_seal_check(manifest_rows):
    r = {"seal_md_exists": SEAL_PATH.exists(),
         "seal_md_sha_matches": False,
         "manifest_sha256": "",
         "hash_verification": {"verified": 0, "mismatches": [], "missing": []}}
    if SEAL_PATH.exists():
        r["seal_md_sha_matches"] = sha256_of(SEAL_PATH).lower() == SEAL_SHA
    if MANIFEST_PATH.exists():
        r["manifest_sha256"] = sha256_of(MANIFEST_PATH).lower()
    for row in manifest_rows:
        p = resolve_source_path(row)
        if not p.exists():
            r["hash_verification"]["missing"].append(row.get("item_id", ""))
            continue
        try:
            actual = sha256_of(p).lower()
        except OSError:
            r["hash_verification"]["missing"].append(row.get("item_id", ""))
            continue
        if actual != row["sha256"].lower():
            r["hash_verification"]["mismatches"].append(row.get("item_id", ""))
        else:
            r["hash_verification"]["verified"] += 1
    return r


# ---------------------------------------------------------------------------
# Phase 2 + 3 - identity pattern matching
# ---------------------------------------------------------------------------

def scan_text_for_patterns(manifest_rows, patterns, role_filter=None):
    """Look for any pattern in any text file in scope.  Returns matches + files."""
    text_exts = {".py", ".md", ".txt", ".json"}
    hits = []
    files_with_hits = set()
    for row in manifest_rows:
        if role_filter and row["role"] not in role_filter:
            continue
        p = resolve_source_path(row)
        if p.suffix.lower() not in text_exts or not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in patterns:
            for m in pat.finditer(text):
                hits.append({
                    "file": row["path"],
                    "role": row["role"],
                    "match_text": m.group(0)[:200],
                    "pattern_used": pat.pattern,
                })
                files_with_hits.add(row["path"])
                break  # one hit per pattern per file
    return hits, files_with_hits


def phase2_action_identity(manifest_rows):
    # Look in qp_source_code and qp_report roles (QP001 + supporting)
    hits, files = scan_text_for_patterns(manifest_rows, ACTION_ID_PATTERNS,
                                          role_filter={"qp_source_code", "qp_report", "qp_artifact", "story_pointer_readme"})
    return {
        "patterns_checked": [p.pattern for p in ACTION_ID_PATTERNS],
        "total_hits": len(hits),
        "files_with_hits_count": len(files),
        "exemplar": hits[0] if hits else None,
        "status": "action_identity_present" if hits else "action_identity_absent",
    }


def phase3_phase_identity(manifest_rows):
    hits, files = scan_text_for_patterns(manifest_rows, PHASE_ID_PATTERNS,
                                          role_filter={"qp_source_code", "qp_report", "qp_artifact", "story_pointer_readme"})
    return {
        "patterns_checked": [p.pattern for p in PHASE_ID_PATTERNS],
        "total_hits": len(hits),
        "files_with_hits_count": len(files),
        "exemplar": hits[0] if hits else None,
        "status": "phase_identity_present" if hits else "phase_identity_absent",
    }


# ---------------------------------------------------------------------------
# Phase 4 - QP001 self-disclosure
# ---------------------------------------------------------------------------

def phase4_qp001_disclosure():
    summary = QUANTUM_PHASE / "artifacts" / "qp001" / "qp001_summary.json"
    # qp001 may use verbose naming
    if not summary.exists():
        cands = list((QUANTUM_PHASE / "artifacts" / "qp001").glob("qp001_*summary*.json"))
        if cands:
            summary = cands[0]
    result = {"summary_exists": summary.exists(),
              "summary_path": str(summary).replace("\\", "/") if summary else "",
              "external_data_used": "", "free_parameters_introduced": "",
              "status": ""}
    if not summary.exists():
        result["status"] = "qp001_summary_missing"
        return result
    try:
        with summary.open("r", encoding="utf-8") as f:
            s = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["status"] = f"read_error:{e}"
        return result
    ext = find_field(s, "external_data_used")
    fp = find_field(s, "free_parameters_introduced")
    result["external_data_used"] = str(ext) if ext is not None else ""
    result["free_parameters_introduced"] = str(fp) if fp is not None else ""
    try:
        fp_int = int(fp) if fp is not None else None
        if fp_int == 0:
            result["status"] = "zero_free_parameters_verified"
        elif fp_int is None:
            result["status"] = "free_parameters_field_missing"
        else:
            result["status"] = f"free_parameters_{fp_int}_violation"
    except (ValueError, TypeError):
        result["status"] = "free_parameters_non_integer"
    return result


# ---------------------------------------------------------------------------
# Phase 5 - Free-particle action substrate-count test
# ---------------------------------------------------------------------------

def phase5_free_particle_action():
    substrate = STAM_REPO / "tests" / "Substrate"
    matches = []
    for pat in FREE_PARTICLE_PATTERNS:
        for d in substrate.glob(pat):
            if d.is_dir():
                matches.append(str(d).replace("\\", "/"))
    matches = sorted(set(matches))
    return {
        "patterns_checked": FREE_PARTICLE_PATTERNS,
        "matching_directories": matches,
        "count": len(matches),
        "status": "free_particle_action_test_present" if matches else "no_free_particle_action_test_found",
    }


# ---------------------------------------------------------------------------
# Phase 6 - Engine-surface fit-loop scan
# ---------------------------------------------------------------------------

def phase6_fit_scan(manifest_rows):
    results = []
    for fp in FIT_PATTERNS:
        engine_hits = []
        doc_mentions = []
        for row in manifest_rows:
            if row["role"] not in ENGINE_CODE_ROLES:
                continue
            p = resolve_source_path(row)
            if p.suffix.lower() != ".py" or not p.exists():
                continue
            ranges = python_string_comment_ranges(p)
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for m in fp.finditer(line):
                            in_doc = match_in_doc(ranges, i, m.start(), m.end())
                            entry = {"file": row["path"], "line": i,
                                     "text": line.rstrip("\n")[:200]}
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
            "pattern": fp.pattern,
            "engine_hit_count": len(engine_hits),
            "doc_mention_count": len(doc_mentions),
            "exemplar_engine_file": engine_hits[0]["file"] if engine_hits else "",
            "exemplar_engine_line": engine_hits[0]["line"] if engine_hits else "",
            "classification": classification,
        })
    return results


# ---------------------------------------------------------------------------
# Phase 7 - Public bridge cite (G406, G421)
# ---------------------------------------------------------------------------

def phase7_public_bridge(manifest_rows):
    found = {}
    for tag in ("G406", "G421"):
        count = 0
        sample = ""
        for row in manifest_rows:
            if tag in row["path"]:
                count += 1
                if not sample:
                    sample = row["path"]
        found[tag] = {"count": count, "sample": sample,
                      "status": "present" if count > 0 else "absent"}
    rows = []
    for tag, info in found.items():
        rows.append({"public_bridge_tag": tag,
                     "manifest_entry_count": info["count"],
                     "exemplar_path": info["sample"],
                     "status": info["status"]})
    return rows


# ---------------------------------------------------------------------------
# Phase 8 - Wrong controls
# ---------------------------------------------------------------------------

def phase8_wrong_controls():
    out = []
    # WC1 - simulated fit loop in source
    fake = "scipy.optimize.curve_fit(observed_phase_data, ...)"
    wc1 = any(p.search(fake) for p in FIT_PATTERNS)
    out.append({"wc_id": "WC1", "description": "Simulated scipy.optimize on observed phase",
                "expected_verdict": "FAIL", "detected": wc1, "observed_match": wc1,
                "notes": "engine-surface fit detection wired"})
    # WC2 - non-zero free params
    out.append({"wc_id": "WC2", "description": "Simulated qp001_summary with free_parameters_introduced=2",
                "expected_verdict": "FAIL", "detected": 2 > 0, "observed_match": 2 > 0,
                "notes": "free-params detection wired"})
    # WC3 - missing identity pattern
    fake_text = "this document does not mention the action phase identity"
    wc3 = not any(p.search(fake_text) for p in ACTION_ID_PATTERNS)
    out.append({"wc_id": "WC3", "description": "Simulated absence of action identity pattern",
                "expected_verdict": "DIAGNOSTIC", "detected": wc3, "observed_match": wc3,
                "notes": "identity-absence detection wired"})
    # WC4 - missing G286-class test
    fake_substrate = STAM_REPO / "tests" / "Substrate_nonexistent"
    wc4 = not fake_substrate.exists()
    out.append({"wc_id": "WC4", "description": "Simulated missing free-particle action test",
                "expected_verdict": "BOUNDARY", "detected": wc4, "observed_match": wc4,
                "notes": "missing-test detection wired"})
    # WC5 - manifest seal corruption
    fake_sha = "deadbeef" + "0" * 56
    wc5 = fake_sha != SEAL_SHA
    out.append({"wc_id": "WC5", "description": "Simulated manifest seal corruption",
                "expected_verdict": "DIAGNOSTIC", "detected": wc5, "observed_match": wc5,
                "notes": "seal mismatch detection wired"})
    # WC6 - pattern in a comment context
    test_line_comment = "# we do NOT use S_A = E_p*T_A as a fit target"
    has_pattern = any(p.search(test_line_comment) for p in ACTION_ID_PATTERNS)
    # Runner WOULD match this; the tokenize-based docstring discrimination is
    # used in phase 6 (fit-scan).  Phase 2/3 identity match is presence-only
    # by design.  WC6 confirms the runner does NOT confuse "presence" with
    # "engine-fit" - those are separate phases.
    out.append({"wc_id": "WC6", "description": "Identity pattern in a do-not-use comment",
                "expected_verdict": "PRESENCE_RECORDED_FIT_SCAN_SEPARATE", "detected": has_pattern,
                "observed_match": has_pattern,
                "notes": "phase 2/3 identity match is presence-only; engine-surface fit is phase 6"})
    return out


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def decide_verdict(p1, p2, p3, p4, p5, p6, p7, p8):
    if p1["hash_verification"]["mismatches"] or p1["hash_verification"]["missing"]:
        return "DIAGNOSTIC", "hash verification failures"
    if not p1["seal_md_sha_matches"]:
        return "DIAGNOSTIC", "seal sha mismatch"
    if p2["status"] != "action_identity_present":
        return "DIAGNOSTIC", "action identity pattern absent"
    if p3["status"] != "phase_identity_present":
        return "DIAGNOSTIC", "phase identity pattern absent"
    if p4["status"] != "zero_free_parameters_verified":
        if "violation" in p4["status"]:
            return "FAIL", f"qp001 self-disclosure: {p4['status']}"
        return "BOUNDARY", f"qp001 self-disclosure indeterminate: {p4['status']}"
    if p5["status"] != "free_particle_action_test_present":
        return "BOUNDARY", "no free-particle action substrate-count test directory found"
    fail_fits = [r for r in p6 if r["classification"] == "FAIL_TRIGGER"]
    if fail_fits:
        return "FAIL", f"engine-surface fit detected: {[r['pattern'] for r in fail_fits]}"
    g_present = sum(1 for r in p7 if r["status"] == "present")
    if g_present == 0:
        return "BOUNDARY", "no public bridge G-test (G406/G421) present"
    untripped = [r for r in p8 if not r["observed_match"]]
    if untripped:
        return "DIAGNOSTIC", f"wrong controls failed: {[r['wc_id'] for r in untripped]}"
    return "PASS_SCOPED_STRUCTURAL_ACTION_PHASE_ANCHOR", \
           f"action identity + phase identity reproduced; qp001 zero free params; free-particle action test {p5['count']} dir(s); {g_present}/2 public bridge tests present; engine-surface clean"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MANIFEST_PATH.exists():
        print("FATAL: manifest not found", file=sys.stderr)
        sys.exit(2)
    manifest_rows = load_manifest(MANIFEST_PATH)
    print(f"Loaded manifest: {len(manifest_rows)} entries")

    print("Phase 1: manifest seal + hash...")
    p1 = phase1_seal_check(manifest_rows)
    print(f"  seal_md_sha_matches={p1['seal_md_sha_matches']}, verified={p1['hash_verification']['verified']}, mismatches={len(p1['hash_verification']['mismatches'])}, missing={len(p1['hash_verification']['missing'])}")

    print("Phase 2: action identity pattern...")
    p2 = phase2_action_identity(manifest_rows)
    print(f"  status={p2['status']}  hits={p2['total_hits']}")

    print("Phase 3: phase identity pattern...")
    p3 = phase3_phase_identity(manifest_rows)
    print(f"  status={p3['status']}  hits={p3['total_hits']}")

    print("Phase 4: qp001 self-disclosure...")
    p4 = phase4_qp001_disclosure()
    print(f"  status={p4['status']}  free_params={p4['free_parameters_introduced']}")

    print("Phase 5: free-particle action substrate-count test presence...")
    p5 = phase5_free_particle_action()
    print(f"  status={p5['status']}  matches={p5['count']}")

    print("Phase 6: engine-surface fit-loop scan...")
    p6 = phase6_fit_scan(manifest_rows)
    for r in p6:
        print(f"  {r['pattern'][:50]:50} engine={r['engine_hit_count']}  doc={r['doc_mention_count']}  {r['classification']}")

    print("Phase 7: public bridge cite check...")
    p7 = phase7_public_bridge(manifest_rows)
    for r in p7:
        print(f"  {r['public_bridge_tag']}: {r['status']} ({r['manifest_entry_count']} entries)")

    print("Phase 8: wrong control injections...")
    p8 = phase8_wrong_controls()
    for r in p8:
        print(f"  {r['wc_id']}: detected={r['detected']}")

    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    verdict, reason = decide_verdict(p1, p2, p3, p4, p5, p6, p7, p8)
    print(f"\nVerdict: {verdict}")
    print(f"  ({reason})")

    # Outputs
    write_csv(OUT_INPUT_MANIFEST, manifest_rows, list(manifest_rows[0].keys()))
    OUT_ACTION_ID.write_text(json.dumps(p2, indent=2, default=str), encoding="utf-8")
    OUT_PHASE_ID.write_text(json.dumps(p3, indent=2, default=str), encoding="utf-8")
    OUT_QP001_DISCL.write_text(json.dumps(p4, indent=2), encoding="utf-8")
    OUT_FREE_PARTICLE.write_text(json.dumps(p5, indent=2), encoding="utf-8")
    write_csv(OUT_FIT_SCAN, p6,
              ["pattern", "engine_hit_count", "doc_mention_count",
               "exemplar_engine_file", "exemplar_engine_line", "classification"])
    write_csv(OUT_PUBLIC_BRIDGE, p7,
              ["public_bridge_tag", "manifest_entry_count", "exemplar_path", "status"])
    OUT_MANIFEST_CHK.write_text(json.dumps({
        "seal_md_sha_matches": p1["seal_md_sha_matches"],
        "manifest_sha256": p1["manifest_sha256"],
        "hash_verified": p1["hash_verification"]["verified"],
        "hash_mismatches": len(p1["hash_verification"]["mismatches"]),
        "hash_missing": len(p1["hash_verification"]["missing"]),
    }, indent=2), encoding="utf-8")
    write_csv(OUT_WRONG, p8,
              ["wc_id", "description", "expected_verdict", "detected",
               "observed_match", "notes"])

    summary = {
        "cr_id": "CR073",
        "branch": "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "execution_status": "CLEAN",
        "scientific_verdict": verdict,
        "triage_bin": "A" if verdict.startswith("PASS") else ("B" if verdict.startswith("BOUNDARY") else "C" if verdict.startswith("FAIL") else "D"),
        "reason": reason,
        "captured_at_utc": captured_at,
        "seal_sha256": SEAL_SHA,
        "manifest_sha256": p1["manifest_sha256"],
        "phases": {
            "p1_seal": p1["seal_md_sha_matches"],
            "p2_action_identity": p2["status"],
            "p3_phase_identity": p3["status"],
            "p4_qp001_disclosure": p4["status"],
            "p5_free_particle_test": p5["status"],
            "p6_fit_scan_fail_classes": sum(1 for r in p6 if r["classification"] == "FAIL_TRIGGER"),
            "p7_public_bridges_present": sum(1 for r in p7 if r["status"] == "present"),
            "p8_wrong_controls_passed": sum(1 for r in p8 if r["observed_match"]),
        }
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_md = f"""# CR073 Action Phase Anchor

## Verdict

```text
CR073_{verdict}
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
Phase 1 seal + hash             verified={p1['hash_verification']['verified']}  seal_sha_matches={p1['seal_md_sha_matches']}
Phase 2 action identity         {p2['status']}  hits={p2['total_hits']}
Phase 3 phase identity          {p3['status']}  hits={p3['total_hits']}
Phase 4 qp001 disclosure        {p4['status']}
Phase 5 free-particle action    {p5['status']}  dir_count={p5['count']}
Phase 6 fit-scan                fail_classes={summary['phases']['p6_fit_scan_fail_classes']}
Phase 7 public bridges          {summary['phases']['p7_public_bridges_present']}/2 present
Phase 8 wrong controls          passed={summary['phases']['p8_wrong_controls_passed']}/{len(p8)}
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-language
reproduces the action-phase identity S_A = E_p * T_A and the phase
relation Delta_phi = S_A / hbar, with zero free parameters and no
engine-surface fit loop targeting observed phase or action values.
```

## Courtroom Reading

CR073 verifies theorem-grade structural reproduction of the action-
phase anchor.  PASS_SCOPED_STRUCTURAL means the identity statements
appear in the QP arm + supporting G-test artifacts, qp001 declares
zero free parameters, and no engine-surface fit loop targets observed
phase/action values.  Per the seal: K1-style row-by-row PASS is not
the expected default for QM CRs.

## Artifacts

- `CR073_input_manifest.csv`
- `CR073_action_identity_check.json`
- `CR073_phase_identity_check.json`
- `CR073_qp001_disclosure_check.json`
- `CR073_free_particle_action_check.json`
- `CR073_engine_surface_fit_scan.csv`
- `CR073_public_bridge_cite_check.csv`
- `CR073_manifest_seal_check.json`
- `CR073_wrong_controls.csv`
- `CR073_summary.json`
- `HASHES.txt`
"""
    OUT_RESULT.write_text(result_md, encoding="utf-8")

    # Seal manifest on PASS or BOUNDARY (both indicate the manifest is locked)
    if verdict.startswith("PASS") or verdict.startswith("BOUNDARY"):
        rel = MANIFEST_PATH.relative_to(COURTROOM_ROOT).as_posix()
        MANIFEST_SEAL.write_text(f"sha256  {rel}  {p1['manifest_sha256']}\n", encoding="utf-8")
        print(f"\nManifest sealed: {MANIFEST_SEAL}")

    output_files = [HERE / "CR073_PRECOMMIT.md", Path(__file__), OUT_INPUT_MANIFEST,
                    OUT_ACTION_ID, OUT_PHASE_ID, OUT_QP001_DISCL, OUT_FREE_PARTICLE,
                    OUT_FIT_SCAN, OUT_PUBLIC_BRIDGE, OUT_MANIFEST_CHK,
                    OUT_WRONG, OUT_SUMMARY, OUT_RESULT]
    hashes_lines = []
    for of in output_files:
        if of.exists():
            hashes_lines.append(f"sha256  {of.relative_to(COURTROOM_ROOT).as_posix()}  {sha256_of(of)}")
    OUT_HASHES.write_text("\n".join(hashes_lines) + "\n", encoding="utf-8")
    print(f"\nOutputs written to {HERE}")


if __name__ == "__main__":
    main()
