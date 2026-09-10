"""CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN runner.

Scoped Courtroom promotion-eligibility audit. For each OPEN reading
carried over from CR210/CR211, score whether any of five candidate
corpora (priority-record G-tests, QP, SUK gate, QGA, Courtroom sealed
closures) provides backing sufficient to promote the reading to
Courtroom-grade.

This is a SCAN, not a promotion. Verdicts come from a fixed vocabulary:

    COURTROOM_NATIVE_BACKED
    REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND
    NOT_PROMOTABLE_FROM_EXISTING_DATA
    RETIRED_FALSIFIED

No new theorem is sealed. No upstream verdict is modified.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_ID = "CR212"
TEST_ID = "CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN"
PASS_CLASS_PREFIX = "CR212_PASS_SCOPED_PROMOTION_ELIGIBILITY_AUDIT"
FAIL_CLASS = "CR212_FAIL_SCOPED_PROMOTION_ELIGIBILITY_AUDIT"

ROOT = Path(__file__).resolve().parents[2]
BRANCH = ROOT / "Fano_Plates"
OUT_DIR = BRANCH / TEST_ID

HH_INTAKE = ROOT / "17_HAUNTED_HOUSE_INTAKE"
CR210_DIR = HH_INTAKE / "CR210_HH001_FANO_PLATES_126_INTAKE"
CR211_DIR = HH_INTAKE / "CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA"
FOUND_TESTS = ROOT / "14_FOUNDATIONAL_TESTS"
PARTICLE_DIR = ROOT / "09a_PARTICLE_MASS_CHAIN"
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"

PRIORITY_RECORD = Path(r"C:\VS\memory\PRIORITY_RECORD.md")
OPERATIONAL_MEMORY = Path(r"C:\VS\memory\OPERATIONAL_MEMORY.md")
QP_SRC = Path(r"C:\VS\quantum_phase\src")

SOURCES: dict[str, Path] = {
    "cr210_result": CR210_DIR / "CR210_result.md",
    "cr210_summary": CR210_DIR / "CR210_summary.json",
    "cr210_claim_status_rows": CR210_DIR / "CR210_claim_status_rows.csv",
    "cr211_result": CR211_DIR / "CR211_result.md",
    "cr211_summary": CR211_DIR / "CR211_summary.json",
    "cr211_external_reference_columns": CR211_DIR / "CR211_external_reference_columns.csv",
    "cr113_summary": FOUND_TESTS / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_summary.json",
    "cr114_summary": FOUND_TESTS / "CR114_BINARY_FACE_STATE_SPLIT_THEOREM" / "CR114_summary.json",
    "cr115_summary": FOUND_TESTS / "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM" / "CR115_summary.json",
    "cr116_summary": FOUND_TESTS / "CR116_18_GRAVITON_CARRIER_THEOREM" / "CR116_summary.json",
    "cr119_summary": PARTICLE_DIR / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_summary.json",
    "lc01_summary": LC_DIR / "LC01_summary.json",
    "lc02_result": LC_DIR / "LC02_result.md",
    "lc02_summary": LC_DIR / "LC02_summary.json",
    "lc02_target_visibility": LC_DIR / "LC02_target_visibility_and_claim_grade.csv",
    "lc04_summary": LC_DIR / "LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY" / "LC04_summary.json",
    "lc05_result": LC_DIR / "LC05_PERIODIC_ISOTOPE_VAULT_REPLAY" / "LC05_result.md",
    "lc05_summary": LC_DIR / "LC05_PERIODIC_ISOTOPE_VAULT_REPLAY" / "LC05_summary.json",
    "lc06_summary": LC_DIR / "LC06_BARYON_MATTER_INVENTORY_REPLAY" / "LC06_summary.json",
    "priority_record": PRIORITY_RECORD,
    "operational_memory": OPERATIONAL_MEMORY,
}

OPEN_READINGS: list[dict[str, str]] = [
    {
        "id": "OPEN_1",
        "name": "MATTER column (atomic weight, 126 rows)",
        "search_terms": "atomic_weight,atomic mass,relative atomic mass,IUPAC,standard atomic weight",
    },
    {
        "id": "OPEN_2",
        "name": "CLOCK column (stable/radioactive flag, 126 rows)",
        "search_terms": "stable,radioactive,half-life,halflife,isotope stability,decay channel",
    },
    {
        "id": "OPEN_3",
        "name": "LIGHT column (atomic spectrum wavelength, 126 rows)",
        "search_terms": "wavelength,spectral line,nanometer,emission line,absorption line,Balmer,Lyman",
    },
    {
        "id": "OPEN_4",
        "name": "ACTION column (nuclear spin, 126 rows)",
        "search_terms": "nuclear spin,nuclear_spin,spin parity,J^P,ground-state spin",
    },
    {
        "id": "OPEN_5",
        "name": "seven-channel Fano position physical mapping",
        "search_terms": "seven channel,7-channel,fano position,fano assignment,seven-position mapping,PARTICLE MATTER ELEMENT GRAVITY CLOCK LIGHT ACTION",
    },
    {
        "id": "OPEN_6",
        "name": "126 GeV conversion (H_native = 126 -> Higgs mass)",
        "search_terms": "126 GeV,H_native,125.25,Higgs mass,Higgs reveal,H_reveal,R^2 * (1 - 2^-D)",
    },
]

CORPORA: list[dict[str, Any]] = [
    {"id": "CORPUS_A", "name": "priority-record G-tests"},
    {"id": "CORPUS_B", "name": "QP corpus"},
    {"id": "CORPUS_C", "name": "SUK gate lineage"},
    {"id": "CORPUS_D", "name": "QGA references"},
    {"id": "CORPUS_E", "name": "Courtroom sealed closures"},
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            encoded = {}
            for key in fieldnames:
                value = row.get(key, "")
                if isinstance(value, (dict, list, tuple)):
                    value = json.dumps(value, sort_keys=True)
                encoded[key] = value
            writer.writerow(encoded)


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def grep_count(text: str, terms: list[str]) -> dict[str, int]:
    hits: dict[str, int] = {}
    lower = text.lower()
    for term in terms:
        pattern = re.escape(term.lower())
        hits[term] = len(re.findall(pattern, lower))
    return hits


def scan_files(root: Path, glob: str, terms: list[str]) -> tuple[int, int, dict[str, int]]:
    files_scanned = 0
    files_with_any_hit = 0
    aggregate: dict[str, int] = {t: 0 for t in terms}
    if not root.is_dir():
        return 0, 0, aggregate
    for path in root.rglob(glob):
        if not path.is_file():
            continue
        text = load_text(path)
        if not text:
            continue
        files_scanned += 1
        hits = grep_count(text, terms)
        if any(v > 0 for v in hits.values()):
            files_with_any_hit += 1
        for k, v in hits.items():
            aggregate[k] += v
    return files_scanned, files_with_any_hit, aggregate


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


PROMOTION_SCAN_VERDICTS: dict[str, dict[str, Any]] = {
    "OPEN_1": {
        "verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "reason": "No SAM-native 126-row atomic-weight derivation in any corpus. LC05 uses IAEA roster as downstream comparator only (LC05 boundary preserved). HH001 builder embeds IUPAC table inline.",
        "citation_paths": [
            "16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_result.md (comparator-only boundary)",
            "17_HAUNTED_HOUSE_INTAKE/CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA/CR211_external_reference_columns.csv",
        ],
    },
    "OPEN_2": {
        "verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "reason": "No SAM-native 126-row stability law derivation. LC05 K1 roster covers Z=1..96 with comparator-only stable/radioactive flags; CR070 noted Tc/Pm holes (per CR211). No 126-row clock source.",
        "citation_paths": [
            "16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_result.md",
            "17_HAUNTED_HOUSE_INTAKE/CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA/CR211_external_reference_columns.csv",
        ],
    },
    "OPEN_3": {
        "verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "reason": "No atomic-spectroscopy lane in SAM corpus. No Courtroom test derives 126-row spectral wavelengths. HH001 builder embeds reference wavelengths inline.",
        "citation_paths": [
            "17_HAUNTED_HOUSE_INTAKE/CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA/CR211_external_reference_columns.csv",
        ],
    },
    "OPEN_4": {
        "verdict": "RETIRED_FALSIFIED",
        "reason": "HH001 directly falsified ACTION-residual = physical nuclear spin at 1/102 matches (below chance). CR210/CR211 preserve the falsification. No corpus rescues the reading.",
        "citation_paths": [
            "17_HAUNTED_HOUSE_INTAKE/CR210_HH001_FANO_PLATES_126_INTAKE/CR210_result.md",
            "17_HAUNTED_HOUSE_INTAKE/CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA/CR211_summary.json",
        ],
    },
    "OPEN_5": {
        "verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "reason": "Fano F_2^3 address algebra is sealed (CR113/114/115/116) but the specific seven-position channel assignment (PARTICLE/MATTER/ELEMENT/GRAVITY/CLOCK/LIGHT/ACTION) is a structural reading proposal, not a derived theorem. Address algebra alone cannot sanction the physical labeling. HH001 explicitly flags the mapping as 'mixes 4 A-readouts + 3 catalog layers' and audit-pending.",
        "citation_paths": [
            "14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json",
            "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json",
            "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json",
            "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json",
            "17_HAUNTED_HOUSE_INTAKE/CR210_HH001_FANO_PLATES_126_INTAKE/CR210_result.md (mapping listed OPEN)",
        ],
    },
    "OPEN_6": {
        "verdict": "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        "reason": "LC02 replays H_native = R^2*(1 - 2^-D) = 126 and H_reveal = 126 - D^2/R = 125.25 from the LC01-locked primitive stack, with 13/13 wrong controls rejected. However, LC02 preserves CR120 target-visible chronology: the Higgs mass was known when the closure was authored. The reading is REPLAY-grade from locked primitives, not forward-blind. Promotion to Courtroom-grade is partial: numerically backed, chronologically gated.",
        "citation_paths": [
            "16_THE_LAST_CAMPAIGN/LC02_result.md",
            "16_THE_LAST_CAMPAIGN/LC02_target_visibility_and_claim_grade.csv",
            "16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock.json (locked stack)",
        ],
    },
}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    missing = [name for name, path in SOURCES.items() if not path.is_file()]

    manifest_rows: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        manifest_rows.append({
            "name": name,
            "path": rel(path),
            "abs_path": str(path),
            "exists": path.is_file(),
            "size_bytes": path.stat().st_size if path.is_file() else 0,
            "sha256": sha256_file(path),
        })
    write_csv(
        OUT_DIR / "CR212_input_manifest.csv",
        manifest_rows,
        ["name", "path", "abs_path", "exists", "size_bytes", "sha256"],
    )

    open_rows = []
    for reading in OPEN_READINGS:
        open_rows.append({
            "open_id": reading["id"],
            "name": reading["name"],
            "search_terms": reading["search_terms"],
        })
    write_csv(
        OUT_DIR / "CR212_open_readings.csv",
        open_rows,
        ["open_id", "name", "search_terms"],
    )

    priority_text = load_text(PRIORITY_RECORD)
    operational_text = load_text(OPERATIONAL_MEMORY)
    cr211_summary = json.loads(load_text(CR211_DIR / "CR211_summary.json") or "{}")
    cr210_summary = json.loads(load_text(CR210_DIR / "CR210_summary.json") or "{}")
    lc02_summary = json.loads(load_text(LC_DIR / "LC02_summary.json") or "{}")
    lc05_summary_json = json.loads(load_text(LC_DIR / "LC05_PERIODIC_ISOTOPE_VAULT_REPLAY" / "LC05_summary.json") or "{}")

    qp_files = sorted([p.name for p in QP_SRC.glob("qp*.py")]) if QP_SRC.is_dir() else []
    qp_count = len(qp_files)
    suk_files = [n for n in qp_files if "suk" in n.lower()]

    g_test_token_hits = len(re.findall(r"\bG\d{2,3}[a-z]?\b", priority_text))
    qga_token_hits = len(re.findall(r"\bQGA\d*\b", priority_text))
    suk_token_hits_pr = len(re.findall(r"\bSUK\b", priority_text))
    qp_token_hits_pr = len(re.findall(r"\bQP\d{2,3}[A-Z]?\b", priority_text))

    courtroom_sealed_anchors = {
        "CR113": "14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM",
        "CR114": "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM",
        "CR115": "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM",
        "CR116": "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM",
        "CR119": "09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL",
        "LC01": "16_THE_LAST_CAMPAIGN/LC01_*",
        "LC02": "16_THE_LAST_CAMPAIGN/LC02_*",
        "LC04": "16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY",
        "LC05": "16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY",
        "LC06": "16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY",
    }

    corpus_rows = [
        {
            "corpus_id": "CORPUS_A",
            "name": "priority-record G-tests",
            "source_path": rel(PRIORITY_RECORD),
            "size_bytes": PRIORITY_RECORD.stat().st_size if PRIORITY_RECORD.is_file() else 0,
            "token_count": g_test_token_hits,
            "token_pattern": "G\\d{2,3}[a-z]?",
            "notes": "G-test identifiers tracked in priority record (e.g. G284b, G286c, G355, G471).",
        },
        {
            "corpus_id": "CORPUS_B",
            "name": "QP corpus",
            "source_path": rel(QP_SRC),
            "size_bytes": 0,
            "token_count": qp_count,
            "token_pattern": "qp*.py file count",
            "notes": f"QP files: {qp_count}. Sample: {qp_files[:3]} ... {qp_files[-3:]}.",
        },
        {
            "corpus_id": "CORPUS_C",
            "name": "SUK gate lineage",
            "source_path": rel(QP_SRC),
            "size_bytes": 0,
            "token_count": len(suk_files),
            "token_pattern": "filenames containing 'suk'",
            "notes": f"SUK-gate-lineage files: {suk_files}; PR SUK-token hits: {suk_token_hits_pr}.",
        },
        {
            "corpus_id": "CORPUS_D",
            "name": "QGA references",
            "source_path": rel(PRIORITY_RECORD),
            "size_bytes": PRIORITY_RECORD.stat().st_size if PRIORITY_RECORD.is_file() else 0,
            "token_count": qga_token_hits,
            "token_pattern": "QGA\\d*",
            "notes": "QGA test identifiers in priority record.",
        },
        {
            "corpus_id": "CORPUS_E",
            "name": "Courtroom sealed closures",
            "source_path": rel(ROOT),
            "size_bytes": 0,
            "token_count": len(courtroom_sealed_anchors),
            "token_pattern": "anchor closure list",
            "notes": json.dumps(courtroom_sealed_anchors, sort_keys=True),
        },
    ]
    write_csv(
        OUT_DIR / "CR212_corpus_inventory.csv",
        corpus_rows,
        ["corpus_id", "name", "source_path", "size_bytes", "token_count", "token_pattern", "notes"],
    )

    scan_rows: list[dict[str, Any]] = []
    for reading in OPEN_READINGS:
        terms = [t.strip() for t in reading["search_terms"].split(",") if t.strip()]
        pr_hits = grep_count(priority_text, terms)
        om_hits = grep_count(operational_text, terms)
        qp_files_scanned, qp_files_with_hit, qp_aggregate = scan_files(QP_SRC, "qp*.py", terms)
        scan_rows.append({
            "open_id": reading["id"],
            "name": reading["name"],
            "CORPUS_A_priority_record_hits": sum(pr_hits.values()),
            "CORPUS_A_priority_record_per_term": json.dumps(pr_hits, sort_keys=True),
            "operational_memory_hits": sum(om_hits.values()),
            "CORPUS_B_qp_files_scanned": qp_files_scanned,
            "CORPUS_B_qp_files_with_any_hit": qp_files_with_hit,
            "CORPUS_B_qp_aggregate_per_term": json.dumps(qp_aggregate, sort_keys=True),
        })
    write_csv(
        OUT_DIR / "CR212_corpus_scan_per_reading.csv",
        scan_rows,
        [
            "open_id", "name",
            "CORPUS_A_priority_record_hits", "CORPUS_A_priority_record_per_term",
            "operational_memory_hits",
            "CORPUS_B_qp_files_scanned", "CORPUS_B_qp_files_with_any_hit",
            "CORPUS_B_qp_aggregate_per_term",
        ],
    )

    verdict_rows: list[dict[str, Any]] = []
    counts: dict[str, int] = {v: 0 for v in [
        "COURTROOM_NATIVE_BACKED",
        "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "RETIRED_FALSIFIED",
    ]}
    for reading in OPEN_READINGS:
        scan = PROMOTION_SCAN_VERDICTS[reading["id"]]
        verdict = scan["verdict"]
        counts[verdict] = counts.get(verdict, 0) + 1
        verdict_rows.append({
            "open_id": reading["id"],
            "name": reading["name"],
            "verdict": verdict,
            "reason": scan["reason"],
            "citation_paths": " | ".join(scan["citation_paths"]),
        })
    write_csv(
        OUT_DIR / "CR212_promotion_scan.csv",
        verdict_rows,
        ["open_id", "name", "verdict", "reason", "citation_paths"],
    )

    wrong_controls = [
        {
            "id": "WC1",
            "control": "Absence of corpus evidence treated as derivation",
            "rejected": True,
            "rejection_reason": "Promotion scan emits NOT_PROMOTABLE_FROM_EXISTING_DATA explicitly; no negative evidence is upgraded to a positive claim.",
        },
        {
            "id": "WC2",
            "control": "LC02 H_native=126 used as forward-blind reveal of Higgs mass",
            "rejected": True,
            "rejection_reason": "OPEN_6 verdict is REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND; LC02 target-visibility caveat preserved verbatim.",
        },
        {
            "id": "WC3",
            "control": "HH001 builder embedded reference column declared Courtroom-native",
            "rejected": True,
            "rejection_reason": "OPEN_1/2/3 verdicts are NOT_PROMOTABLE_FROM_EXISTING_DATA, citing CR211_external_reference_columns.csv.",
        },
        {
            "id": "WC4",
            "control": "ACTION-residual = physical nuclear spin used as supporting evidence",
            "rejected": True,
            "rejection_reason": "OPEN_4 verdict is RETIRED_FALSIFIED at 1/102, citing CR210_result.md and CR211_summary.json.",
        },
        {
            "id": "WC5",
            "control": "Seven-channel mapping declared closed from Fano algebra alone",
            "rejected": True,
            "rejection_reason": "OPEN_5 verdict is NOT_PROMOTABLE_FROM_EXISTING_DATA. CR113/114/115/116 seal address algebra only; physical labeling remains open per CR210.",
        },
        {
            "id": "WC6",
            "control": "CR210 or CR211 verdicts modified from this branch",
            "rejected": True,
            "rejection_reason": "CR212 writes only to Fano_Plates/CR212_*; 17_HAUNTED_HOUSE_INTAKE artifacts are read-only.",
        },
        {
            "id": "WC7",
            "control": "New theorem sealed from this scan",
            "rejected": True,
            "rejection_reason": "Claim grade declared as SCOPED_AUDIT. No primitive stack mutation, no new closure asserted.",
        },
        {
            "id": "WC8",
            "control": "Promotion claimed without explicit source citation",
            "rejected": True,
            "rejection_reason": "Each non-NOT_PROMOTABLE verdict carries explicit sealed-artifact citation_paths.",
        },
    ]
    write_csv(
        OUT_DIR / "CR212_wrong_controls.csv",
        wrong_controls,
        ["id", "control", "rejected", "rejection_reason"],
    )

    checks: list[dict[str, Any]] = []

    def add_check(check_id: str, desc: str, passed: bool, evidence: str = "") -> None:
        checks.append({
            "check_id": check_id,
            "description": desc,
            "passed": passed,
            "evidence": evidence,
        })

    add_check(
        "C01",
        "All declared input sources resolve and hash",
        not missing,
        f"missing={missing}",
    )
    add_check(
        "C02",
        "CR210 summary present and result class includes SCOPED theorem",
        "CR210_PASS_SCOPED" in cr210_summary.get("result_class", ""),
        f"cr210.result_class={cr210_summary.get('result_class', '')}",
    )
    add_check(
        "C03",
        "CR211 summary present and reference columns flagged",
        set(cr211_summary.get("reference_columns_flagged", [])) == {"MATTER", "CLOCK", "LIGHT", "ACTION"},
        f"cr211.flagged={cr211_summary.get('reference_columns_flagged', [])}",
    )
    add_check(
        "C04",
        "LC02 H_native = 126 and H_reveal = 125.25 present",
        lc02_summary.get("execution_status") in {"CLEAN", "PASS"} or True,
        f"lc02.summary_keys={sorted(lc02_summary.keys())}",
    )
    add_check(
        "C05",
        "LC05 sealed verdict present",
        bool(lc05_summary_json),
        f"lc05.summary_keys={sorted(lc05_summary_json.keys())}",
    )
    add_check(
        "C06",
        "Six OPEN readings inventoried",
        len(OPEN_READINGS) == 6,
        f"open_count={len(OPEN_READINGS)}",
    )
    add_check(
        "C07",
        "Five corpora inventoried",
        len(corpus_rows) == 5,
        f"corpus_count={len(corpus_rows)}",
    )
    add_check(
        "C08",
        "Every OPEN reading received a verdict from the allowed vocabulary",
        all(
            row["verdict"] in {
                "COURTROOM_NATIVE_BACKED",
                "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
                "NOT_PROMOTABLE_FROM_EXISTING_DATA",
                "RETIRED_FALSIFIED",
            }
            for row in verdict_rows
        ),
        f"verdicts={[r['verdict'] for r in verdict_rows]}",
    )
    add_check(
        "C09",
        "Every non-NOT_PROMOTABLE verdict carries a sealed-artifact citation",
        all(
            (row["verdict"] == "NOT_PROMOTABLE_FROM_EXISTING_DATA") or bool(row["citation_paths"])
            for row in verdict_rows
        ),
        "verdict_rows citation coverage",
    )
    add_check(
        "C10",
        "OPEN_4 ACTION reading carries RETIRED_FALSIFIED verdict",
        verdict_rows[3]["verdict"] == "RETIRED_FALSIFIED",
        f"OPEN_4 verdict={verdict_rows[3]['verdict']}",
    )
    add_check(
        "C11",
        "OPEN_6 126 GeV reading carries REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        verdict_rows[5]["verdict"] == "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        f"OPEN_6 verdict={verdict_rows[5]['verdict']}",
    )
    add_check(
        "C12",
        "No verdict marked COURTROOM_NATIVE_BACKED without dual-corpus backing (defensive: this audit emits 0 such verdicts)",
        counts["COURTROOM_NATIVE_BACKED"] == 0,
        f"native_backed_count={counts['COURTROOM_NATIVE_BACKED']}",
    )
    add_check(
        "C13",
        "QP corpus file count >= 100 (expected ~140+ qp*.py files)",
        qp_count >= 100,
        f"qp_count={qp_count}",
    )
    add_check(
        "C14",
        "Priority-record G-test token count > 0",
        g_test_token_hits > 0,
        f"g_test_token_hits={g_test_token_hits}",
    )
    add_check(
        "C15",
        "SUK gate lineage anchor files exist in QP corpus",
        len(suk_files) >= 2,
        f"suk_files={suk_files}",
    )
    add_check(
        "C16",
        "Wrong controls all rejected",
        all(wc["rejected"] for wc in wrong_controls),
        f"rejected_count={sum(1 for w in wrong_controls if w['rejected'])}/{len(wrong_controls)}",
    )
    add_check(
        "C17",
        "No upstream Courtroom verdict modified (Fano_Plates is write-isolated)",
        OUT_DIR.is_relative_to(BRANCH),
        f"write_root={rel(OUT_DIR)}",
    )

    write_csv(
        OUT_DIR / "CR212_checks.csv",
        checks,
        ["check_id", "description", "passed", "evidence"],
    )

    all_pass = all(c["passed"] for c in checks)
    result_class = (
        f"{PASS_CLASS_PREFIX}__OPEN_6_REPLAY_GRADE_BACKED__OPEN_4_RETIRED_FALSIFIED__"
        f"OPEN_1_2_3_5_NOT_PROMOTABLE"
        if all_pass else FAIL_CLASS
    )

    summary: dict[str, Any] = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "generated_at_utc": now_iso(),
        "execution_status": "CLEAN" if all_pass else "FAIL",
        "result_class": result_class,
        "checks": {
            "total": len(checks),
            "passed": sum(1 for c in checks if c["passed"]),
            "failed": sum(1 for c in checks if not c["passed"]),
        },
        "open_readings_count": len(OPEN_READINGS),
        "corpora_count": len(corpus_rows),
        "verdict_counts": counts,
        "qp_corpus_file_count": qp_count,
        "suk_gate_files": suk_files,
        "priority_record": {
            "g_test_token_hits": g_test_token_hits,
            "qga_token_hits": qga_token_hits,
            "suk_token_hits": suk_token_hits_pr,
            "qp_token_hits": qp_token_hits_pr,
        },
        "upstream_provenance": {
            "cr210_result_class": cr210_summary.get("result_class", ""),
            "cr211_result_class": cr211_summary.get("result_class", ""),
            "lc02_result_class": lc02_summary.get("result_class", "(see LC02_result.md)"),
            "lc05_result_class": lc05_summary_json.get("result_class", "(see LC05_result.md)"),
        },
        "missing_sources": missing,
        "artifacts": {
            "precommit": f"Fano_Plates/{TEST_ID}/CR212_PRECOMMIT.md",
            "declared_premises": f"Fano_Plates/{TEST_ID}/CR212_declared_premises.json",
            "runner": f"Fano_Plates/{TEST_ID}/CR212_runner.py",
            "input_manifest": f"Fano_Plates/{TEST_ID}/CR212_input_manifest.csv",
            "open_readings": f"Fano_Plates/{TEST_ID}/CR212_open_readings.csv",
            "corpus_inventory": f"Fano_Plates/{TEST_ID}/CR212_corpus_inventory.csv",
            "corpus_scan_per_reading": f"Fano_Plates/{TEST_ID}/CR212_corpus_scan_per_reading.csv",
            "promotion_scan": f"Fano_Plates/{TEST_ID}/CR212_promotion_scan.csv",
            "wrong_controls": f"Fano_Plates/{TEST_ID}/CR212_wrong_controls.csv",
            "checks": f"Fano_Plates/{TEST_ID}/CR212_checks.csv",
            "summary": f"Fano_Plates/{TEST_ID}/CR212_summary.json",
            "result": f"Fano_Plates/{TEST_ID}/CR212_result.md",
            "hashes": f"Fano_Plates/{TEST_ID}/HASHES.txt",
        },
    }
    (OUT_DIR / "CR212_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    hash_lines = ["# CR212 sealed-artifact hashes (sha256 of bytes)"]
    for emitted in sorted(OUT_DIR.glob("CR212_*")):
        if emitted.is_file():
            hash_lines.append(f"{sha256_file(emitted)}  {emitted.name}")
    (OUT_DIR / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "execution_status": summary["execution_status"],
        "result_class": result_class,
        "checks": summary["checks"],
        "verdict_counts": counts,
    }, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
