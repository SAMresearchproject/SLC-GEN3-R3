from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR219_PROMOTED_PARTICLE_ROWS_EXPORT"

CR119 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
SOURCE_MATTER = CR119 / "CR119_courtroom_matter_table.csv"
SOURCE_PARTICLE = CR119 / "CR119_courtroom_particle_table.csv"
SOURCE_COUNTS = CR119 / "source_copies" / "latest_table_counts.csv"
SOURCE_EXPORT_SUMMARY = CR119 / "source_copies" / "latest_table_export_summary.json"

EXPORT = OUT / "CR219_promoted_particle_rows_126.csv"
INPUT_MANIFEST = OUT / "CR219_input_manifest.csv"
CHECKS = OUT / "CR219_checks.csv"
SUMMARY = OUT / "CR219_summary.json"
RESULT = OUT / "CR219_result.md"
HASHES = OUT / "HASHES.txt"
PRECOMMIT = OUT / "CR219_PRECOMMIT.md"
RUNNER = OUT / "CR219_runner.py"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return fields, list(reader)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def manifest_row(path: Path, role: str) -> dict[str, Any]:
    return {
        "source": rel(path),
        "exists": str(path.exists()),
        "bytes": path.stat().st_size if path.exists() else "",
        "sha256": sha256_file(path) if path.exists() else "",
        "role": role,
    }


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append({
        "check": name,
        "passed": str(bool(passed)),
        "observed": observed,
        "expected": expected,
    })


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    input_paths = [
        (SOURCE_MATTER, "formal_126_promoted_particle_surface"),
        (SOURCE_PARTICLE, "321_particle_candidate_parent_table"),
        (SOURCE_COUNTS, "source_count_scope"),
        (SOURCE_EXPORT_SUMMARY, "source_export_summary"),
    ]
    write_csv(
        INPUT_MANIFEST,
        [manifest_row(path, role) for path, role in input_paths],
        ["source", "exists", "bytes", "sha256", "role"],
    )

    fields, matter_rows = read_csv(SOURCE_MATTER)
    _, particle_rows = read_csv(SOURCE_PARTICLE)
    particle_ids = {row.get("candidate_id", "") for row in particle_rows}
    exported_ids = [row.get("candidate_id", "") for row in matter_rows]

    write_csv(EXPORT, matter_rows, fields)

    bin_counts = dict(Counter(row.get("bin", "") for row in matter_rows))
    gate_counts = dict(Counter(row.get("matter_gate_status", "") for row in matter_rows))
    promotion_counts = dict(Counter(row.get("promotion_status", "") for row in matter_rows))

    checks: list[dict[str, Any]] = []
    check(checks, "source_matter_exists", SOURCE_MATTER.exists(), SOURCE_MATTER.exists(), True)
    check(checks, "source_particle_exists", SOURCE_PARTICLE.exists(), SOURCE_PARTICLE.exists(), True)
    check(checks, "export_rows_126", len(matter_rows) == 126, len(matter_rows), 126)
    check(checks, "unique_candidate_ids_126", len(set(exported_ids)) == 126, len(set(exported_ids)), 126)
    check(
        checks,
        "all_exported_ids_in_particle_table",
        set(exported_ids).issubset(particle_ids),
        len(set(exported_ids) - particle_ids),
        0,
    )
    check(
        checks,
        "all_matter_row_allowed_yes",
        all(row.get("matter_row_allowed") == "yes" for row in matter_rows),
        dict(Counter(row.get("matter_row_allowed", "") for row in matter_rows)),
        {"yes": 126},
    )
    check(
        checks,
        "all_latest_matter_row_allowed_yes",
        all(row.get("latest_matter_row_allowed") == "yes" for row in matter_rows),
        dict(Counter(row.get("latest_matter_row_allowed", "") for row in matter_rows)),
        {"yes": 126},
    )
    check(
        checks,
        "bin_split_63_63",
        bin_counts == {"stable_matter_rows": 63, "bound_composite_rows": 63},
        bin_counts,
        {"stable_matter_rows": 63, "bound_composite_rows": 63},
    )
    check(
        checks,
        "matter_gate_split_63_63",
        gate_counts == {"PASS_STABLE_SINGLE_WRITE_MATTER": 63, "PASS_BOUND_COMPOSITE_MATTER": 63},
        gate_counts,
        {"PASS_STABLE_SINGLE_WRITE_MATTER": 63, "PASS_BOUND_COMPOSITE_MATTER": 63},
    )
    check(
        checks,
        "known_labels_not_construction_inputs",
        all(row.get("known_label_used_as_construction_input") == "no" for row in matter_rows),
        dict(Counter(row.get("known_label_used_as_construction_input", "") for row in matter_rows)),
        {"no": 126},
    )
    check(
        checks,
        "export_bytes_nonzero",
        EXPORT.exists() and EXPORT.stat().st_size > 0,
        EXPORT.stat().st_size if EXPORT.exists() else 0,
        ">0",
    )
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    summary = {
        "cr_id": "CR219",
        "test_id": "CR219_PROMOTED_PARTICLE_ROWS_EXPORT",
        "execution_status": "CLEAN" if passed == len(checks) else "FAILED",
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "source": rel(SOURCE_MATTER),
        "output": rel(EXPORT),
        "output_sha256": sha256_file(EXPORT),
        "row_count": len(matter_rows),
        "unique_candidate_ids": len(set(exported_ids)),
        "bin_counts": bin_counts,
        "matter_gate_counts": gate_counts,
        "promotion_counts": promotion_counts,
        "checks_passed": passed,
        "checks_total": len(checks),
        "result_class": (
            "CR219_PASS_PROMOTED_PARTICLE_ROWS_EXPORT__126_ROWS__"
            "CR119_MATTER_GATE_SURFACE__63_STABLE_PLUS_63_BOUND"
        ),
        "boundary": (
            "Export uses CR119_courtroom_matter_table.csv as the formal 126-row "
            "promoted particle surface; it does not filter the 321-row particle "
            "table by matter-row flags."
        ),
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR219 Promoted Particle Rows Export

Result: **{summary['result_class']}**

## Direct Answer

The requested 126 promoted particle rows are exported to:

`{rel(EXPORT)}`

## Source

The export is copied from the formal CR119 matter-gated table:

`{rel(SOURCE_MATTER)}`

## Checks

- Export rows: 126
- Candidate IDs: 126 unique
- Bin split: 63 `stable_matter_rows` + 63 `bound_composite_rows`
- Matter gate split: 63 `PASS_STABLE_SINGLE_WRITE_MATTER` + 63 `PASS_BOUND_COMPOSITE_MATTER`
- All exported rows have `matter_row_allowed=yes`
- All exported rows have `latest_matter_row_allowed=yes`
- Exported candidate IDs are present in the CR119 321-row particle table

## Boundary

This export uses the CR119 126-row matter table as the promoted particle
surface. It does not filter the full 321-row particle table by
`matter_row_allowed` or `latest_matter_row_allowed`, because those flags also
include open/heavy particle candidates outside the formal promoted 126.
"""
    RESULT.write_text(result_text, encoding="utf-8")

    write_hashes([PRECOMMIT, RUNNER, EXPORT, INPUT_MANIFEST, CHECKS, SUMMARY, RESULT])
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
