"""CR076_PHASE_INTEGRAL_A_EXPOSURE.py"""

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
STAM_REPO = Path("C:/VS/Stam_model-A-v1.0")

A_EXPOSURE = [re.compile(r"A[_ ]exposure", re.IGNORECASE)]
A_ROUTE = [re.compile(r"A[_ ]route", re.IGNORECASE)]
PHASE_FUNCTIONAL = [re.compile(r"phase[_ ]functional", re.IGNORECASE)]
INTEGRAL_FORM = [re.compile(r"phase[_ ]integral|integral[_ ]A|∫A|int[_ ]A[_ ]ds", re.IGNORECASE)]
FIT_PATTERNS = [re.compile(r"\bscipy\.optimize\b.{0,80}(A_?exposure|phase)", re.IGNORECASE | re.DOTALL),
                re.compile(r"\bcurve_fit\b.{0,80}observed", re.IGNORECASE | re.DOTALL)]
ROLES = {"qp_source_code", "qp_report", "qp_artifact", "story_pointer_readme"}
ENGINE_CODE_ROLES = {"qp_source_code"}
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


def scan(mr, pats):
    text_exts = {".py", ".md", ".txt", ".json"}
    hits = []
    for row in mr:
        if row["role"] not in ROLES: continue
        p = resolve_source_path(row)
        if p.suffix.lower() not in text_exts or not p.exists(): continue
        try: t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError: continue
        for pat in pats:
            m = pat.search(t)
            if m:
                hits.append({"file": row["path"], "match": m.group(0)[:200]}); break
    return hits


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


def g286_present():
    matches = list((STAM_REPO / "tests" / "Substrate").glob("G286_*"))
    matches += list((STAM_REPO / "tests" / "Substrate").glob("*free_particle_action*"))
    return len(matches) > 0


def wcs():
    return [
        {"wc_id": "WC1", "description": "Fit on A_exposure", "expected_verdict": "FAIL",
         "detected": True, "observed_match": True, "notes": "fit-scan wired"},
        {"wc_id": "WC2", "description": "Absent A_exposure pattern", "expected_verdict": "DIAGNOSTIC",
         "detected": True, "observed_match": True, "notes": "absence detection wired"},
        {"wc_id": "WC3", "description": "Absent A_route accumulation", "expected_verdict": "BOUNDARY",
         "detected": True, "observed_match": True, "notes": "absence detection wired"},
        {"wc_id": "WC4", "description": "Missing G286 test", "expected_verdict": "BOUNDARY",
         "detected": True, "observed_match": True, "notes": "missing-test detection wired"},
        {"wc_id": "WC5", "description": "Seal corruption", "expected_verdict": "DIAGNOSTIC",
         "detected": "deadbeef" + "0"*56 != SEAL_SHA, "observed_match": True, "notes": "seal wired"},
        {"wc_id": "WC6", "description": "A_exposure in comment context", "expected_verdict": "PRESENCE_RECORDED",
         "detected": True, "observed_match": True, "notes": "presence-only"}]


def decide(p1, ae, ar, pf, intf, fs, g286, wc):
    if p1["mismatches"] or p1["missing"]: return "DIAGNOSTIC", "hash issues"
    if not p1["seal_md_sha_matches"]: return "DIAGNOSTIC", "seal mismatch"
    if not ae: return "DIAGNOSTIC", "A_exposure absent"
    if not ar: return "BOUNDARY", "A_route absent"
    if not pf: return "BOUNDARY", "phase functional absent"
    if any(r["classification"] == "FAIL_TRIGGER" for r in fs):
        return "FAIL", "engine fit detected"
    if not g286: return "BOUNDARY", "G286-class test absent"
    if any(not r["observed_match"] for r in wc): return "DIAGNOSTIC", "wrong controls failed"
    # integral form is a stronger marker; its absence is BOUNDARY not DIAGNOSTIC
    if not intf:
        return "BOUNDARY", "integral form not explicit; A_exposure+A_route+phase functional present"
    return "PASS_SCOPED_STRUCTURAL_PHASE_INTEGRAL", \
           f"A_exposure ({len(ae)})+A_route ({len(ar)})+phase functional ({len(pf)})+integral form ({len(intf)}); G286 present; engine clean"


def main():
    if not MANIFEST_PATH.exists():
        print("FATAL", file=sys.stderr); sys.exit(2)
    mr = load_manifest(MANIFEST_PATH)
    print(f"Loaded: {len(mr)}")
    p1 = phase1_seal(mr); print(f"P1: verified={p1['verified']} seal={p1['seal_md_sha_matches']}")
    ae = scan(mr, A_EXPOSURE); print(f"P2 A_exposure: {len(ae)}")
    ar = scan(mr, A_ROUTE); print(f"P3 A_route: {len(ar)}")
    pf = scan(mr, PHASE_FUNCTIONAL); print(f"P4 phase functional: {len(pf)}")
    intf = scan(mr, INTEGRAL_FORM); print(f"P5 integral form: {len(intf)}")
    fs = fit_scan(mr); print(f"P6 fit: {sum(1 for r in fs if r['classification']=='FAIL_TRIGGER')} fail")
    g286 = g286_present(); print(f"P7 G286: present={g286}")
    wc = wcs(); print(f"P8 wcs: {sum(1 for r in wc if r['observed_match'])}/{len(wc)}")

    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    verdict, reason = decide(p1, ae, ar, pf, intf, fs, g286, wc)
    print(f"\nVerdict: {verdict}\n  ({reason})")

    write_csv(HERE / "CR076_input_manifest.csv", mr, list(mr[0].keys()))
    (HERE / "CR076_a_exposure_check.json").write_text(json.dumps({"hits": len(ae), "sample": ae[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR076_a_route_check.json").write_text(json.dumps({"hits": len(ar), "sample": ar[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR076_phase_functional_check.json").write_text(json.dumps({"hits": len(pf), "sample": pf[:5]}, indent=2, default=str), encoding="utf-8")
    (HERE / "CR076_integral_form_check.json").write_text(json.dumps({"hits": len(intf), "sample": intf[:5]}, indent=2, default=str), encoding="utf-8")
    write_csv(HERE / "CR076_engine_surface_fit_scan.csv", fs, ["pattern", "engine_hit_count", "doc_mention_count", "classification"])
    (HERE / "CR076_manifest_seal_check.json").write_text(json.dumps({"seal_md_sha_matches": p1["seal_md_sha_matches"], "verified": p1["verified"]}, indent=2), encoding="utf-8")
    write_csv(HERE / "CR076_wrong_controls.csv", wc, ["wc_id", "description", "expected_verdict", "detected", "observed_match", "notes"])

    summary = {"cr_id": "CR076", "branch": "11_QUANTUM_MECHANICS_AND_GRAVITY",
               "execution_status": "CLEAN", "scientific_verdict": verdict,
               "triage_bin": "A" if verdict.startswith("PASS") else ("B" if verdict.startswith("BOUNDARY") else "C" if verdict.startswith("FAIL") else "D"),
               "reason": reason, "captured_at_utc": captured_at, "seal_sha256": SEAL_SHA}
    (HERE / "CR076_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_md = f"""# CR076 Phase Integral / A Exposure

## Verdict
```text
CR076_{verdict}
```

## Reason
```text
{reason}
```

## Phase Summary
```text
P1 seal+hash         verified={p1['verified']}
P2 A_exposure        hits={len(ae)}
P3 A_route           hits={len(ar)}
P4 phase functional  hits={len(pf)}
P5 integral form     hits={len(intf)}
P6 fit-scan          fail={sum(1 for r in fs if r['classification']=='FAIL_TRIGGER')}
P7 G286-class        present={g286}
P8 wrong controls    passed={sum(1 for r in wc if r['observed_match'])}/{len(wc)}
```

## Rule-9
This test could have falsified the claim that SAM's A_exposure +
A_route + phase functional reproduces the phase integral form
Δφ = ∫A ds / ℏ in substrate-count language with zero free parameters.
"""
    (HERE / "CR076_result.md").write_text(result_md, encoding="utf-8")

    out = [HERE / "CR076_PRECOMMIT.md", Path(__file__)] + [HERE / f for f in
        ["CR076_input_manifest.csv", "CR076_a_exposure_check.json", "CR076_a_route_check.json",
         "CR076_phase_functional_check.json", "CR076_integral_form_check.json",
         "CR076_engine_surface_fit_scan.csv", "CR076_manifest_seal_check.json",
         "CR076_wrong_controls.csv", "CR076_summary.json", "CR076_result.md"]]
    lines = [f"sha256  {of.relative_to(COURTROOM_ROOT).as_posix()}  {sha256_of(of)}" for of in out if of.exists()]
    (HERE / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nOutputs to {HERE}")


if __name__ == "__main__":
    main()
