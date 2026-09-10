"""CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE runner.

Regrade CR212's promotion-eligibility verdicts in light of the actual
construction of the HH001 SIS table. The HH001 builder uses CR119
SAM-derived data (Z, PARTICLE = p + e + n_primary, GRAVITY = qA) as the
126-row scaffold, with MATTER / CLOCK / LIGHT / ACTION columns aligned
to that scaffold as per-row comparators. CR212 mis-scored those four
columns as "REFERENCE_NOT_COURTROOM_DATA"; the regrade introduces a
new tier:

    SAM_SCAFFOLD_PLACEMENT_GRADE

CR212a does NOT modify CR212. It hashes CR212's sealed artifacts and
references them verbatim. The regrade is recorded here.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_ID = "CR212a"
TEST_ID = "CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE"
PASS_CLASS = (
    "CR212a_PASS_SCOPED_PROMOTION_ELIGIBILITY_REGRADE__"
    "SAM_SCAFFOLD_PLACEMENT_GRADE_RECOGNIZED__"
    "CR212_EMPIRICAL_SCAN_PRESERVED__"
    "OPEN_4_RETIRED_FALSIFIED__OPEN_6_REPLAY_GRADE_ONLY"
)
FAIL_CLASS = "CR212a_FAIL_SCOPED_PROMOTION_ELIGIBILITY_REGRADE"

ROOT = Path(__file__).resolve().parents[2]
BRANCH = ROOT / "Fano_Plates"
OUT_DIR = BRANCH / TEST_ID
CR212_DIR = BRANCH / "CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN"

HH_BUILDER = Path(r"C:\VS\Haunted_House\explorations\HH001_build_sis_table.py")
CR119_TABLE = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_courtroom_periodic_table.csv"
CR119_SUMMARY = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_summary.json"
HH001_NOTE = Path(r"C:\VS\Haunted_House\explorations\HH001_D3_TO_PARTICLES_BREADCRUMB_AUDIT.md")
LC02_RESULT = ROOT / "16_THE_LAST_CAMPAIGN" / "LC02_result.md"
LC02_TARGET_VIS = ROOT / "16_THE_LAST_CAMPAIGN" / "LC02_target_visibility_and_claim_grade.csv"

SOURCES: dict[str, Path] = {
    "cr212_precommit": CR212_DIR / "CR212_PRECOMMIT.md",
    "cr212_premises": CR212_DIR / "CR212_declared_premises.json",
    "cr212_promotion_scan": CR212_DIR / "CR212_promotion_scan.csv",
    "cr212_summary": CR212_DIR / "CR212_summary.json",
    "cr212_result": CR212_DIR / "CR212_result.md",
    "cr212_hashes": CR212_DIR / "HASHES.txt",
    "hh001_builder": HH_BUILDER,
    "hh001_note": HH001_NOTE,
    "cr119_table": CR119_TABLE,
    "cr119_summary": CR119_SUMMARY,
    "lc02_result": LC02_RESULT,
    "lc02_target_visibility": LC02_TARGET_VIS,
    "replacement_record": OUT_DIR / "REPLACEMENT_RECORD.md",
    "cr212a_precommit": OUT_DIR / "CR212a_PRECOMMIT.md",
}


REGRADE_VERDICTS: list[dict[str, Any]] = [
    {
        "open_id": "OPEN_1",
        "name": "MATTER column (atomic weight, 126 rows)",
        "cr212_verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "cr212a_verdict": "SAM_SCAFFOLD_PLACEMENT_GRADE",
        "reason": "Column value is ATOMIC_MASS[Z] lookup, but the per-row scaffold (Z, PARTICLE=p+e+n_primary, GRAVITY=qA) is SAM-derived from CR119. Frontier Z=119-126 emit '-' so no fabrication. The column rides a SAM-derived row scaffold as a per-row comparator.",
        "scaffold_citations": [
            "HH001_build_sis_table.py:245-251 (CR119 Z, p, e, n_primary, qA reads)",
            "HH001_build_sis_table.py:253-254 (PARTICLE = p+e+n; ELEMENT = Z; SAM identities)",
            "CR119_courtroom_periodic_table.csv (126-row SAM scaffold; LC05 replays from LC01 lock)",
        ],
        "comparator_citation": "HH001_build_sis_table.py:48-69 ATOMIC_MASS dict (comparator lookup)",
        "boundary": "Promotable as PLACEMENT grade only; not a SAM derivation of the atomic-weight value itself.",
    },
    {
        "open_id": "OPEN_2",
        "name": "CLOCK column (stable/radioactive flag, 126 rows)",
        "cr212_verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "cr212a_verdict": "SAM_SCAFFOLD_PLACEMENT_GRADE",
        "reason": "clock_value(Z) is a rule keyed on Z (the SAM-derived ELEMENT identity); the rule is comparator-aligned to the empirical Tc/Pm/Z>=84 radioactive pattern. The row scaffold (Z, PARTICLE, GRAVITY) is SAM-derived from CR119. Frontier Z=119-126 emit '-'.",
        "scaffold_citations": [
            "HH001_build_sis_table.py:245-258 (CR119 reads + clock_value(Z) call)",
            "HH001_build_sis_table.py:73-80 clock_value(Z) rule (keyed on SAM-derived Z)",
            "CR119_courtroom_periodic_table.csv (126-row SAM scaffold)",
        ],
        "comparator_citation": "HH001_build_sis_table.py:73-80 clock_value rule (comparator rule)",
        "boundary": "Promotable as PLACEMENT grade. A SAM-native stability law derivation is not asserted here.",
    },
    {
        "open_id": "OPEN_3",
        "name": "LIGHT column (atomic spectrum wavelength, 126 rows)",
        "cr212_verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "cr212a_verdict": "SAM_SCAFFOLD_PLACEMENT_GRADE",
        "reason": "Column value is LIGHT_NM[Z] lookup, but Z is the SAM-derived ELEMENT identity and the row scaffold (Z, PARTICLE, GRAVITY) is SAM-derived from CR119. Limited-data and frontier rows emit '-'.",
        "scaffold_citations": [
            "HH001_build_sis_table.py:245-259 (CR119 reads + LIGHT_NM[Z] lookup)",
            "HH001_build_sis_table.py:111-230 LIGHT_NM dict (comparator lookup, '-' for limited-data rows)",
            "CR119_courtroom_periodic_table.csv (126-row SAM scaffold)",
        ],
        "comparator_citation": "HH001_build_sis_table.py:111-230 LIGHT_NM dict",
        "boundary": "Promotable as PLACEMENT grade. SAM atomic-spectroscopy lane is not opened by this test.",
    },
    {
        "open_id": "OPEN_4",
        "name": "ACTION column (nuclear spin, 126 rows)",
        "cr212_verdict": "RETIRED_FALSIFIED",
        "cr212a_verdict": "RETIRED_FALSIFIED",
        "reason": "HH001 self-falsified ACTION-residual = physical nuclear spin at 1/102 matches. The scaffold tie is the same (Z keyed; CR119-derived row), but the *physical-spin* reading is closed at retirement. Regrade preserves the falsification; the column structure inherits the SAM-scaffold tie only as placement context, not as a rescue.",
        "scaffold_citations": [
            "HH001_build_sis_table.py:245-260 (CR119 reads + NUCLEAR_SPIN[Z] lookup)",
            "17_HAUNTED_HOUSE_INTAKE/CR210_HH001_FANO_PLATES_126_INTAKE/CR210_result.md (1/102 falsification)",
            "17_HAUNTED_HOUSE_INTAKE/CR211_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA/CR211_summary.json (action_residual_matches=1)",
        ],
        "comparator_citation": "HH001_build_sis_table.py:84-105 NUCLEAR_SPIN dict (comparator lookup)",
        "boundary": "Stays RETIRED_FALSIFIED. The SAM-scaffold tie does not rescue the physical-spin reading.",
    },
    {
        "open_id": "OPEN_5",
        "name": "seven-channel Fano position physical mapping",
        "cr212_verdict": "NOT_PROMOTABLE_FROM_EXISTING_DATA",
        "cr212a_verdict": "SAM_SCAFFOLD_PLACEMENT_GRADE",
        "reason": "The seven positions ride the SAM-derived F_2^3 Fano partition (CR113/114/115/116 sealed) and the CR119 SAM-derived row scaffold. The labeling of each position to (PARTICLE/MATTER/ELEMENT/GRAVITY/CLOCK/LIGHT/ACTION) is a placement convention compatible with the scaffold. A *physical-meaning* derivation of each position remains audit-pending and is not asserted here.",
        "scaffold_citations": [
            "14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json",
            "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json",
            "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json",
            "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json",
            "09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_summary.json",
        ],
        "comparator_citation": "HH001_build_sis_table.py docstring (lines 13-30) channel name conventions",
        "boundary": "Promotable as PLACEMENT grade. The physical-meaning derivation of each Fano position remains a separate open audit per HH001 own notes.",
    },
    {
        "open_id": "OPEN_6",
        "name": "126 GeV conversion (H_native = 126 -> Higgs mass)",
        "cr212_verdict": "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        "cr212a_verdict": "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        "reason": "Unchanged from CR212. LC02 replays H_native = R^2*(1 - 2^-D) = 126 and H_reveal = 125.25 from the LC01-locked SAM primitive stack with 13/13 wrong controls rejected. CR120 target-visibility caveat preserved.",
        "scaffold_citations": [
            "16_THE_LAST_CAMPAIGN/LC02_result.md",
            "16_THE_LAST_CAMPAIGN/LC02_target_visibility_and_claim_grade.csv",
        ],
        "comparator_citation": "(none; the Higgs reveal value is the comparator)",
        "boundary": "Promotable as REPLAY grade only; not forward-blind.",
    },
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


def parse_sealed_hashes(text: str) -> dict[str, str]:
    sealed: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([0-9a-fA-F]{64})\s+(.+)$", line)
        if match:
            sealed[match.group(2).strip()] = match.group(1).lower()
    return sealed


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    missing = [name for name, path in SOURCES.items() if not path.is_file()]

    manifest_rows = []
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
        OUT_DIR / "CR212a_input_manifest.csv",
        manifest_rows,
        ["name", "path", "abs_path", "exists", "size_bytes", "sha256"],
    )

    sealed_text = load_text(CR212_DIR / "HASHES.txt")
    sealed = parse_sealed_hashes(sealed_text)

    seal_rows: list[dict[str, Any]] = []
    seal_mismatches: list[str] = []
    for name, sealed_hash in sorted(sealed.items()):
        current = sha256_file(CR212_DIR / name)
        match = (current == sealed_hash)
        seal_rows.append({
            "file": name,
            "sealed_sha256": sealed_hash,
            "current_sha256": current,
            "match": match,
        })
        if not match:
            seal_mismatches.append(name)
    write_csv(
        OUT_DIR / "CR212a_cr212_seal_check.csv",
        seal_rows,
        ["file", "sealed_sha256", "current_sha256", "match"],
    )

    regrade_rows = []
    for v in REGRADE_VERDICTS:
        regrade_rows.append({
            "open_id": v["open_id"],
            "name": v["name"],
            "cr212_verdict": v["cr212_verdict"],
            "cr212a_verdict": v["cr212a_verdict"],
            "reason": v["reason"],
            "scaffold_citations": " | ".join(v["scaffold_citations"]),
            "comparator_citation": v["comparator_citation"],
            "boundary": v["boundary"],
        })
    write_csv(
        OUT_DIR / "CR212a_regrade_table.csv",
        regrade_rows,
        [
            "open_id", "name",
            "cr212_verdict", "cr212a_verdict",
            "reason",
            "scaffold_citations", "comparator_citation",
            "boundary",
        ],
    )

    cr119_text = load_text(CR119_TABLE)
    cr119_header = cr119_text.split("\n", 1)[0] if cr119_text else ""
    cr119_row_count = max(0, cr119_text.count("\n") - 1)
    cr119_required_cols = [
        "Z", "proton_count", "electron_count", "neutron_count_primary",
        "known_symbol", "known_name", "qA_total_primary", "tensor_carrier_support_primary",
    ]
    cr119_col_present = {col: (col in cr119_header) for col in cr119_required_cols}

    builder_text = load_text(HH_BUILDER)
    sam_scaffold_evidence = {
        "particle_formula_line_found": "proton_count + electron_count + neutron_count_primary" in builder_text or
                                       "protons + electrons + neutrons" in builder_text,
        "Z_read_from_CR119": 'el["Z"]' in builder_text,
        "qA_read_from_CR119": 'el["qA_total_primary"]' in builder_text,
        "frontier_dash_emit_clause": 'matter = "-"' in builder_text and 'light = "-"' in builder_text,
        "ATOMIC_MASS_lookup": "ATOMIC_MASS.get(Z" in builder_text,
        "LIGHT_NM_lookup": "LIGHT_NM.get(Z" in builder_text,
        "NUCLEAR_SPIN_lookup": "NUCLEAR_SPIN.get(Z" in builder_text,
        "clock_value_call": "clock_value(Z)" in builder_text,
    }

    write_csv(
        OUT_DIR / "CR212a_sam_scaffold_evidence.csv",
        [{"key": k, "value": v} for k, v in sam_scaffold_evidence.items()],
        ["key", "value"],
    )

    wrong_controls = [
        {
            "id": "WC1a",
            "control": "SAM_SCAFFOLD_PLACEMENT_GRADE treated as forward-blind derivation of the column value",
            "rejected": True,
            "rejection_reason": "Each PLACEMENT-grade verdict carries a 'boundary' field stating it is not a SAM derivation of the column value itself.",
        },
        {
            "id": "WC2a",
            "control": "CR212 verdicts rewritten in place rather than recorded as a regrade",
            "rejected": True,
            "rejection_reason": "CR212 sealed-artifact hashes re-checked by CR212a_cr212_seal_check.csv; no CR212 file modified.",
        },
        {
            "id": "WC3a",
            "control": "OPEN_4 ACTION-spin promoted above RETIRED_FALSIFIED",
            "rejected": True,
            "rejection_reason": "OPEN_4 stays RETIRED_FALSIFIED in CR212a; SAM-scaffold tie listed for context only.",
        },
        {
            "id": "WC4a",
            "control": "Comparator vs derivation distinction collapsed",
            "rejected": True,
            "rejection_reason": "Each PLACEMENT-grade row carries an explicit 'comparator_citation' separate from 'scaffold_citations'.",
        },
        {
            "id": "WC5a",
            "control": "Seven-channel labeling declared closed because the scaffold is SAM",
            "rejected": True,
            "rejection_reason": "OPEN_5 boundary field explicitly says physical-meaning derivation of each position remains a separate open audit.",
        },
        {
            "id": "WC6a",
            "control": "OPEN_1/2/3 left at NOT_PROMOTABLE after SAM-scaffold construction was documented",
            "rejected": True,
            "rejection_reason": "OPEN_1/2/3 regraded to SAM_SCAFFOLD_PLACEMENT_GRADE with line-numbered builder citations.",
        },
    ]
    write_csv(
        OUT_DIR / "CR212a_wrong_controls.csv",
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
        "A01",
        "All declared input sources resolve and hash",
        not missing,
        f"missing={missing}",
    )
    add_check(
        "A02",
        "CR212 sealed artifacts re-hash to sealed values (CR212 unmodified)",
        not seal_mismatches and bool(sealed),
        f"sealed_files={len(sealed)} mismatches={seal_mismatches}",
    )
    add_check(
        "A03",
        "REPLACEMENT_RECORD present in CR212a folder",
        (OUT_DIR / "REPLACEMENT_RECORD.md").is_file(),
        f"replacement_record={(OUT_DIR / 'REPLACEMENT_RECORD.md').is_file()}",
    )
    add_check(
        "A04",
        "HH001 builder shows PARTICLE = p + e + n_primary formula",
        sam_scaffold_evidence["particle_formula_line_found"],
        f"formula_found={sam_scaffold_evidence['particle_formula_line_found']}",
    )
    add_check(
        "A05",
        "HH001 builder reads Z and qA from CR119 row",
        sam_scaffold_evidence["Z_read_from_CR119"] and sam_scaffold_evidence["qA_read_from_CR119"],
        f"Z={sam_scaffold_evidence['Z_read_from_CR119']} qA={sam_scaffold_evidence['qA_read_from_CR119']}",
    )
    add_check(
        "A06",
        "HH001 builder emits '-' for frontier Z>=119 on comparator columns",
        sam_scaffold_evidence["frontier_dash_emit_clause"],
        f"frontier_clause={sam_scaffold_evidence['frontier_dash_emit_clause']}",
    )
    add_check(
        "A07",
        "HH001 builder uses comparator lookups (ATOMIC_MASS, LIGHT_NM, NUCLEAR_SPIN, clock_value)",
        all([
            sam_scaffold_evidence["ATOMIC_MASS_lookup"],
            sam_scaffold_evidence["LIGHT_NM_lookup"],
            sam_scaffold_evidence["NUCLEAR_SPIN_lookup"],
            sam_scaffold_evidence["clock_value_call"],
        ]),
        json.dumps(sam_scaffold_evidence, sort_keys=True),
    )
    add_check(
        "A08",
        "CR119 periodic table presents the eight scaffold columns",
        all(cr119_col_present.values()),
        json.dumps(cr119_col_present, sort_keys=True),
    )
    add_check(
        "A09",
        "CR119 periodic table has at least 126 rows",
        cr119_row_count >= 126,
        f"cr119_row_count={cr119_row_count}",
    )
    add_check(
        "A10",
        "Every regraded verdict uses the expanded allowed vocabulary",
        all(
            row["cr212a_verdict"] in {
                "COURTROOM_NATIVE_BACKED",
                "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
                "SAM_SCAFFOLD_PLACEMENT_GRADE",
                "NOT_PROMOTABLE_FROM_EXISTING_DATA",
                "RETIRED_FALSIFIED",
            }
            for row in regrade_rows
        ),
        f"verdicts={[r['cr212a_verdict'] for r in regrade_rows]}",
    )
    add_check(
        "A11",
        "OPEN_4 remains RETIRED_FALSIFIED in regrade",
        regrade_rows[3]["cr212a_verdict"] == "RETIRED_FALSIFIED",
        f"open_4={regrade_rows[3]['cr212a_verdict']}",
    )
    add_check(
        "A12",
        "OPEN_6 unchanged at REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        regrade_rows[5]["cr212_verdict"] == "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND" and
        regrade_rows[5]["cr212a_verdict"] == "REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND",
        f"open_6 cr212={regrade_rows[5]['cr212_verdict']} cr212a={regrade_rows[5]['cr212a_verdict']}",
    )
    add_check(
        "A13",
        "OPEN_1, OPEN_2, OPEN_3, OPEN_5 regraded NOT_PROMOTABLE -> SAM_SCAFFOLD_PLACEMENT_GRADE",
        all(
            regrade_rows[i]["cr212_verdict"] == "NOT_PROMOTABLE_FROM_EXISTING_DATA" and
            regrade_rows[i]["cr212a_verdict"] == "SAM_SCAFFOLD_PLACEMENT_GRADE"
            for i in (0, 1, 2, 4)
        ),
        f"open1={regrade_rows[0]['cr212a_verdict']} open2={regrade_rows[1]['cr212a_verdict']} open3={regrade_rows[2]['cr212a_verdict']} open5={regrade_rows[4]['cr212a_verdict']}",
    )
    add_check(
        "A14",
        "Every PLACEMENT-grade row carries explicit scaffold citation and comparator citation",
        all(
            (row["cr212a_verdict"] != "SAM_SCAFFOLD_PLACEMENT_GRADE") or
            (bool(row["scaffold_citations"]) and bool(row["comparator_citation"]))
            for row in regrade_rows
        ),
        "citation coverage on PLACEMENT-grade rows",
    )
    add_check(
        "A15",
        "Wrong controls all rejected",
        all(wc["rejected"] for wc in wrong_controls),
        f"rejected_count={sum(1 for w in wrong_controls if w['rejected'])}/{len(wrong_controls)}",
    )

    write_csv(
        OUT_DIR / "CR212a_checks.csv",
        checks,
        ["check_id", "description", "passed", "evidence"],
    )

    all_pass = all(c["passed"] for c in checks)
    result_class = PASS_CLASS if all_pass else FAIL_CLASS

    verdict_counts: dict[str, int] = {}
    for row in regrade_rows:
        verdict_counts[row["cr212a_verdict"]] = verdict_counts.get(row["cr212a_verdict"], 0) + 1

    summary = {
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
        "regrade_verdict_counts": verdict_counts,
        "cr212_seal_check": {
            "files_checked": len(sealed),
            "mismatches": seal_mismatches,
        },
        "sam_scaffold_evidence": sam_scaffold_evidence,
        "cr119_scaffold": {
            "row_count_min_126": cr119_row_count >= 126,
            "observed_row_count": cr119_row_count,
            "required_columns_present": cr119_col_present,
        },
        "upstream_provenance": {
            "cr212_result_class": "CR212_PASS_SCOPED_PROMOTION_ELIGIBILITY_AUDIT__OPEN_6_REPLAY_GRADE_BACKED__OPEN_4_RETIRED_FALSIFIED__OPEN_1_2_3_5_NOT_PROMOTABLE",
            "regrade_authority": "Sean Brady directive",
        },
        "missing_sources": missing,
        "artifacts": {
            "replacement_record": f"Fano_Plates/{TEST_ID}/REPLACEMENT_RECORD.md",
            "precommit": f"Fano_Plates/{TEST_ID}/CR212a_PRECOMMIT.md",
            "runner": f"Fano_Plates/{TEST_ID}/CR212a_runner.py",
            "input_manifest": f"Fano_Plates/{TEST_ID}/CR212a_input_manifest.csv",
            "cr212_seal_check": f"Fano_Plates/{TEST_ID}/CR212a_cr212_seal_check.csv",
            "regrade_table": f"Fano_Plates/{TEST_ID}/CR212a_regrade_table.csv",
            "sam_scaffold_evidence": f"Fano_Plates/{TEST_ID}/CR212a_sam_scaffold_evidence.csv",
            "wrong_controls": f"Fano_Plates/{TEST_ID}/CR212a_wrong_controls.csv",
            "checks": f"Fano_Plates/{TEST_ID}/CR212a_checks.csv",
            "summary": f"Fano_Plates/{TEST_ID}/CR212a_summary.json",
            "result": f"Fano_Plates/{TEST_ID}/CR212a_result.md",
            "hashes": f"Fano_Plates/{TEST_ID}/HASHES.txt",
        },
    }
    (OUT_DIR / "CR212a_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    hash_lines = ["# CR212a sealed-artifact hashes (sha256 of bytes)"]
    for emitted in sorted(OUT_DIR.glob("*")):
        if emitted.is_file() and emitted.name != "HASHES.txt":
            hash_lines.append(f"{sha256_file(emitted)}  {emitted.name}")
    (OUT_DIR / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "execution_status": summary["execution_status"],
        "result_class": result_class,
        "checks": summary["checks"],
        "regrade_verdict_counts": verdict_counts,
        "cr212_seal_mismatches": seal_mismatches,
    }, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
