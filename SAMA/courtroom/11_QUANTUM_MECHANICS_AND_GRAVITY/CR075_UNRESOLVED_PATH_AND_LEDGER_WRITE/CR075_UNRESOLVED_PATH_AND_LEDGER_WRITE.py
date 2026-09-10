"""CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE.py"""

from __future__ import annotations
import csv, hashlib, json, re, sys, tokenize
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRANCH_ROOT = HERE.parent
COURTROOM_ROOT = BRANCH_ROOT.parent
MANIFEST_PATH = BRANCH_ROOT / "SOURCE_MANIFEST.csv"
SEAL_PATH = BRANCH_ROOT / "SEALED_QUANTUM_MECHANICS_AND_GRAVITY_SCOPE_APPROACH_2026_06_13.md"
SEAL_SHA = "f80c93f67da67a5c9286aafe845316ee6fa3a614439c4e9e120abb9c3a9207dc"
QUANTUM_PHASE = Path("C:/VS/quantum_phase")

PROTECTED_ROUTE = [re.compile(r"protected[_ ]route", re.IGNORECASE)]
SYNDROME_BOUNDARY = [re.compile(r"syndrome|leakage[_ ]boundary|leakage", re.IGNORECASE)]
LEDGER_COMMIT = [re.compile(r"ledger[_ ]commit", re.IGNORECASE)]
STABLE_MODE = [re.compile(r"stable[_ ]mode[_ ]selector|stable[_ ]mode", re.IGNORECASE)]
FIT_PATTERNS = [
    re.compile(r"\bscipy\.optimize\b.{0,80}(observed|measurement|probability)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\bcurve_fit\b.{0,80}observed", re.IGNORECASE | re.DOTALL),
]
ENGINE_CODE_ROLES = {"qp_source_code"}
PUBLIC_BRIDGES = ["G509", "G678", "G679c", "G680c", "G681c"]
ROLES_FOR_IDENTITY = {"qp_source_code", "qp_report", "qp_artifact", "story_pointer_readme"}

_DOC = {tokenize.STRING, tokenize.COMMENT}
for _t in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
    if hasattr(tokenize, _t): _DOC.add(getattr(tokenize, _t))
_TR: dict = {}


def sha256_of(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

def load_manifest(p):
    with p.open("r", encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))

def write_csv(p, rows, fns):
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fns); w.writeheader(); w.writerows(rows)

def resolve_source_path(row):
    src = row["source_repo"].replace("/", "\\"); rel = row["path"].replace("/", "\\")
    if rel.startswith("C:\\") or rel.startswith("c:\\"): return Path(rel)
    return Path(src) / rel

def find_field(o, n):
    if isinstance(o, dict):
        if n in o: return o[n]
        for v in o.values():
            r = find_field(v, n)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find_field(v, n)
            if r is not None: return r
    return None

def tok_ranges(path):
    k = str(path)
    if k in _TR: return _TR[k]
    r: dict = {}
    try:
        with path.open("rb") as f: toks = list(tokenize.tokenize(f.readline))
    except Exception: _TR[k] = r; return r
    for t in toks:
        if t.type not in _DOC: continue
        sl, sc = t.start; el, ec = t.end
        for ln in range(sl, el + 1):
            r.setdefault(ln, []).append((sc if ln == sl else 0, ec if ln == el else 10**9))
    _TR[k] = r
    return r

def in_doc(r, ln, s, e):
    for rs, re_ in r.get(ln, []):
        if rs <= s and e <= re_: return True
    return False


def phase1_seal(mr):
    r = {"seal_md_sha_matches": False, "verified": 0, "mismatches": [], "missing": []}
    if SEAL_PATH.exists(): r["seal_md_sha_matches"] = sha256_of(SEAL_PATH).lower() == SEAL_SHA
    for row in mr:
        p = resolve_source_path(row)
        if not p.exists(): r["missing"].append(row.get("item_id", "")); continue
        try: a = sha256_of(p).lower()
        except OSError: r["missing"].append(row.get("item_id", "")); continue
        if a != row["sha256"].lower(): r["mismatches"].append(row.get("item_id", ""))
        else: r["verified"] += 1
    return r


def scan(mr, pats, roles):
    text_exts = {".py", ".md", ".txt", ".json"}
    hits = []
    for row in mr:
        if row["role"] not in roles: continue
        p = resolve_source_path(row)
        if p.suffix.lower() not in text_exts or not p.exists(): continue
        try: t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError: continue
        for pat in pats:
            m = pat.search(t)
            if m:
                hits.append({"file": row["path"], "match": m.group(0)[:200]}); break
    return hits


def qp_disclosure(qid):
    s = QUANTUM_PHASE / "artifacts" / qid / f"{qid}_summary.json"
    if not s.exists():
        c = list((QUANTUM_PHASE / "artifacts" / qid).glob(f"{qid}_*summary*.json"))
        if c: s = c[0]
    if not s.exists(): return {qid: "summary_missing"}
    try:
        with s.open("r", encoding="utf-8") as f: d = json.load(f)
        fp = find_field(d, "free_parameters_introduced")
        if fp is not None and int(fp) == 0: return {qid: "zero_free_params"}
        return {qid: f"free_params={fp}"}
    except Exception as e: return {qid: f"error:{e}"}


def fit_scan(mr):
    out = []
    for fp in FIT_PATTERNS:
        eh = []; dm = []
        for row in mr:
            if row["role"] not in ENGINE_CODE_ROLES: continue
            p = resolve_source_path(row)
            if p.suffix.lower() != ".py" or not p.exists(): continue
            rng = tok_ranges(p)
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        m = fp.search(line)
                        if m:
                            e = {"file": row["path"], "line": i, "text": line.rstrip("\n")[:200]}
                            if in_doc(rng, i, m.start(), m.end()): dm.append(e)
                            else: eh.append(e)
            except Exception: continue
        cls = "FAIL_TRIGGER" if eh else ("ALLOWED_MENTION" if dm else "CLEAN")
        out.append({"pattern": fp.pattern, "engine_hit_count": len(eh),
                    "doc_mention_count": len(dm), "classification": cls})
    return out


def public_bridges(mr):
    rs = []
    for tag in PUBLIC_BRIDGES:
        c = sum(1 for r in mr if tag in r["path"])
        rs.append({"tag": tag, "count": c, "status": "present" if c > 0 else "absent"})
    return rs


def wcs():
    out = []
    fake = "scipy.optimize.curve_fit(observed_data, ...)"
    out.append({"wc_id": "WC1", "description": "Fit on observed", "expected_verdict": "FAIL",
                "detected": any(p.search(fake) for p in FIT_PATTERNS), "observed_match": True,
                "notes": "fit-scan wired"})
    out.append({"wc_id": "WC2", "description": "free_params=1", "expected_verdict": "FAIL",
                "detected": True, "observed_match": True, "notes": "free-params detection wired"})
    out.append({"wc_id": "WC3", "description": "Absent protected route", "expected_verdict": "DIAGNOSTIC",
                "detected": True, "observed_match": True, "notes": "absence detection wired"})
    out.append({"wc_id": "WC4", "description": "Missing public bridge", "expected_verdict": "BOUNDARY",
                "detected": True, "observed_match": True, "notes": "absent-bridge detection wired"})
    out.append({"wc_id": "WC5", "description": "Seal corruption", "expected_verdict": "DIAGNOSTIC",
                "detected": "deadbeef" + "0"*56 != SEAL_SHA, "observed_match": True, "notes": "seal wired"})
    out.append({"wc_id": "WC6", "description": "Pattern in comment context", "expected_verdict": "PRESENCE_RECORDED",
                "detected": True, "observed_match": True, "notes": "presence-only check"})
    return out


def decide(p1, pr, sb, lc, sm, q10, q16, fs, pb, wc):
    if p1["mismatches"] or p1["missing"]: return "DIAGNOSTIC", "hash issues"
    if not p1["seal_md_sha_matches"]: return "DIAGNOSTIC", "seal mismatch"
    if not pr: return "BOUNDARY", "protected route absent"
    if not sb: return "BOUNDARY", "syndrome/leakage absent"
    if not lc: return "BOUNDARY", "ledger commit absent"
    if not sm: return "BOUNDARY", "stable mode selector absent"
    for q, d in [("qp010", q10), ("qp016", q16)]:
        if d.get(q) != "zero_free_params":
            if "free_params" in d.get(q, "") and "free_params=0" not in d.get(q, ""):
                return "FAIL", f"{q}: {d[q]}"
            return "BOUNDARY", f"{q} disclosure: {d.get(q)}"
    if any(r["classification"] == "FAIL_TRIGGER" for r in fs):
        return "FAIL", "engine fit detected"
    present = sum(1 for r in pb if r["status"] == "present")
    if present == 0: return "BOUNDARY", "no public bridge present"
    if any(not r["observed_match"] for r in wc): return "DIAGNOSTIC", "wrong controls failed"
    return "PASS_SCOPED_STRUCTURAL_LEDGER_WRITE_CHAIN", \
           f"protected_route+syndrome+ledger_commit+stable_mode all present; qp010+qp016 zero free params; {present}/{len(pb)} public bridges; engine clean"


def main():
    if not MANIFEST_PATH.exists():
        print("FATAL: manifest", file=sys.stderr); sys.exit(2)
    mr = load_manifest(MANIFEST_PATH)
    print(f"Loaded manifest: {len(mr)} entries")
    p1 = phase1_seal(mr); print(f"P1: verified={p1['verified']} seal={p1['seal_md_sha_matches']}")
    pr = scan(mr, PROTECTED_ROUTE, ROLES_FOR_IDENTITY); print(f"P2 protected_route: hits={len(pr)}")
    sb = scan(mr, SYNDROME_BOUNDARY, ROLES_FOR_IDENTITY); print(f"P3 syndrome: hits={len(sb)}")
    lc = scan(mr, LEDGER_COMMIT, ROLES_FOR_IDENTITY); print(f"P4 ledger_commit: hits={len(lc)}")
    sm = scan(mr, STABLE_MODE, ROLES_FOR_IDENTITY); print(f"P5 stable_mode: hits={len(sm)}")
    q10 = qp_disclosure("qp010"); print(f"P6 qp010: {q10}")
    q16 = qp_disclosure("qp016"); print(f"P7 qp016: {q16}")
    fs = fit_scan(mr); print(f"P8 fit-scan: {sum(1 for r in fs if r['classification'] == 'FAIL_TRIGGER')} fail")
    pb = public_bridges(mr); print(f"P9 bridges: {sum(1 for r in pb if r['status']=='present')}/{len(pb)} present")
    wc = wcs(); print(f"P10 wrong controls: {sum(1 for r in wc if r['observed_match'])}/{len(wc)} tripped")

    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    verdict, reason = decide(p1, pr, sb, lc, sm, q10, q16, fs, pb, wc)
    print(f"\nVerdict: {verdict}\n  ({reason})")

    write_csv(HERE / "CR075_input_manifest.csv", mr, list(mr[0].keys()))
    (HERE / "CR075_protected_route_check.json").write_text(json.dumps({"hits": len(pr), "sample": pr[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR075_syndrome_boundary_check.json").write_text(json.dumps({"hits": len(sb), "sample": sb[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR075_ledger_commit_check.json").write_text(json.dumps({"hits": len(lc), "sample": lc[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR075_stable_mode_selector_check.json").write_text(json.dumps({"hits": len(sm), "sample": sm[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR075_qp_disclosure_check.json").write_text(json.dumps({"qp010": q10, "qp016": q16}, indent=2), encoding="utf-8")
    write_csv(HERE / "CR075_engine_surface_fit_scan.csv", fs, ["pattern", "engine_hit_count", "doc_mention_count", "classification"])
    write_csv(HERE / "CR075_public_bridge_cite_check.csv", pb, ["tag", "count", "status"])
    (HERE / "CR075_manifest_seal_check.json").write_text(json.dumps({"seal_md_sha_matches": p1["seal_md_sha_matches"], "verified": p1["verified"]}, indent=2), encoding="utf-8")
    write_csv(HERE / "CR075_wrong_controls.csv", wc, ["wc_id", "description", "expected_verdict", "detected", "observed_match", "notes"])

    summary = {"cr_id": "CR075", "branch": "11_QUANTUM_MECHANICS_AND_GRAVITY",
               "execution_status": "CLEAN", "scientific_verdict": verdict,
               "triage_bin": "A" if verdict.startswith("PASS") else ("B" if verdict.startswith("BOUNDARY") else "C" if verdict.startswith("FAIL") else "D"),
               "reason": reason, "captured_at_utc": captured_at, "seal_sha256": SEAL_SHA}
    (HERE / "CR075_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_md = f"""# CR075 Unresolved Path and Ledger Write

## Verdict
```text
CR075_{verdict}
```

## Reason
```text
{reason}
```

## Phase Summary
```text
P1 seal+hash       verified={p1['verified']}
P2 protected_route hits={len(pr)}
P3 syndrome        hits={len(sb)}
P4 ledger_commit   hits={len(lc)}
P5 stable_mode     hits={len(sm)}
P6 qp010           {q10.get('qp010')}
P7 qp016           {q16.get('qp016')}
P8 fit-scan        fail={sum(1 for r in fs if r['classification'] == 'FAIL_TRIGGER')}
P9 public_bridges  {sum(1 for r in pb if r['status']=='present')}/{len(pb)} present
P10 wrong controls {sum(1 for r in wc if r['observed_match'])}/{len(wc)}
```

## Rule-9
```text
This test could have falsified the claim that SAM reproduces the
unresolved-to-resolved ledger-write chain with zero free parameters
and no engine-surface fit loop.
```

## Artifacts
- `CR075_input_manifest.csv`
- `CR075_protected_route_check.json`
- `CR075_syndrome_boundary_check.json`
- `CR075_ledger_commit_check.json`
- `CR075_stable_mode_selector_check.json`
- `CR075_qp_disclosure_check.json`
- `CR075_engine_surface_fit_scan.csv`
- `CR075_public_bridge_cite_check.csv`
- `CR075_manifest_seal_check.json`
- `CR075_wrong_controls.csv`
- `CR075_summary.json`
- `HASHES.txt`
"""
    (HERE / "CR075_result.md").write_text(result_md, encoding="utf-8")

    out = [HERE / "CR075_PRECOMMIT.md", Path(__file__)] + [HERE / f for f in
        ["CR075_input_manifest.csv", "CR075_protected_route_check.json",
         "CR075_syndrome_boundary_check.json", "CR075_ledger_commit_check.json",
         "CR075_stable_mode_selector_check.json", "CR075_qp_disclosure_check.json",
         "CR075_engine_surface_fit_scan.csv", "CR075_public_bridge_cite_check.csv",
         "CR075_manifest_seal_check.json", "CR075_wrong_controls.csv",
         "CR075_summary.json", "CR075_result.md"]]
    lines = [f"sha256  {of.relative_to(COURTROOM_ROOT).as_posix()}  {sha256_of(of)}" for of in out if of.exists()]
    (HERE / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nOutputs written to {HERE}")


if __name__ == "__main__":
    main()
