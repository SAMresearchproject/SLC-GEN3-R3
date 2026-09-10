from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT"
CR214 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
INPUT_CSV = CR214 / "CR214_particle_complement_195.csv"

SEALED_INPUT_SHA256 = "e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545"

SIGNATURE_COLUMNS = [
    "bin",
    "partition_signature",
    "closure_depth",
    "q_sign",
    "q_abs",
    "native_charge_axis",
    "M_native",
    "surface_sign",
    "surface_depth",
    "S_debit_or_credit",
    "M_observed_candidate",
    "qA_source_support",
    "tensor_carrier_support",
    "retained_write_support",
]

DESCRIPTOR_DIFF_COLUMNS = [
    "route_combination",
    "operator_class",
    "spin_or_hand_class",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


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


def normalize_number(value: str) -> str:
    """Numbers in the sheet carry trailing repeating-decimal tails. Compare by
    string equality after stripping whitespace. Two cells count as equal only
    when their normalized string forms are identical."""
    return (value or "").strip()


def signature_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(normalize_number(row.get(col, "")) for col in SIGNATURE_COLUMNS)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Verify sealed input hash.
    input_hash = sha256_file(INPUT_CSV)
    hash_match = input_hash == SEALED_INPUT_SHA256

    # 2. Read input.
    fieldnames, rows = read_csv(INPUT_CSV)
    row_count = len(rows)

    # 3. Build per-row signature keys (full 195-row dump for review).
    sig_rows = []
    for idx, row in enumerate(rows, start=1):
        sig = signature_key(row)
        sig_rows.append(
            {
                "row_index": idx,
                "candidate_id": row.get("candidate_id", ""),
                "bin": row.get("bin", ""),
                "operator_class": row.get("operator_class", ""),
                "route_combination": row.get("route_combination", ""),
                "spin_or_hand_class": row.get("spin_or_hand_class", ""),
                "numeric_signature_key": "|".join(sig),
            }
        )
    write_csv(
        OUT / "CR215_numeric_signature_keys.csv",
        sig_rows,
        [
            "row_index",
            "candidate_id",
            "bin",
            "operator_class",
            "route_combination",
            "spin_or_hand_class",
            "numeric_signature_key",
        ],
    )

    # 4. Group rows by signature key.
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[signature_key(row)].append(row)

    duplicate_groups = {key: members for key, members in groups.items() if len(members) > 1}

    # 5. Assign DUP-<bin>-<seq> labels per bin.
    duplicate_class_by_row_index: dict[int, str] = {}
    per_bin_seq: dict[str, int] = defaultdict(int)
    dup_group_rows = []
    for key, members in duplicate_groups.items():
        bin_name = members[0].get("bin", "unknown_bin")
        per_bin_seq[bin_name] += 1
        label = f"DUP-{bin_name}-{per_bin_seq[bin_name]:02d}"
        member_ids = []
        descriptor_sets = {col: set() for col in DESCRIPTOR_DIFF_COLUMNS}
        for member in members:
            member_ids.append(member.get("candidate_id", ""))
            for col in DESCRIPTOR_DIFF_COLUMNS:
                descriptor_sets[col].add(member.get(col, ""))
            # Map original row index back to the duplicate label.
            for idx, original in enumerate(rows, start=1):
                if original is member:
                    duplicate_class_by_row_index[idx] = label
                    break
        dup_group_rows.append(
            {
                "duplicate_class": label,
                "bin": bin_name,
                "member_count": len(members),
                "candidate_ids": ";".join(member_ids),
                "numeric_signature_key": "|".join(key),
                "route_combinations": ";".join(sorted(descriptor_sets["route_combination"])),
                "operator_classes": ";".join(sorted(descriptor_sets["operator_class"])),
                "spin_or_hand_classes": ";".join(sorted(descriptor_sets["spin_or_hand_class"])),
            }
        )
    dup_group_rows.sort(key=lambda r: r["duplicate_class"])
    write_csv(
        OUT / "CR215_numeric_duplicate_groups.csv",
        dup_group_rows,
        [
            "duplicate_class",
            "bin",
            "member_count",
            "candidate_ids",
            "route_combinations",
            "operator_classes",
            "spin_or_hand_classes",
            "numeric_signature_key",
        ],
    )

    # 6. Per-bin summary.
    bin_total = Counter(row.get("bin", "") for row in rows)
    bin_duplicate_member_count: Counter[str] = Counter()
    for members in duplicate_groups.values():
        for member in members:
            bin_duplicate_member_count[member.get("bin", "")] += 1
    bin_duplicate_group_count: Counter[str] = Counter(
        members[0].get("bin", "") for members in duplicate_groups.values()
    )

    per_bin_rows = []
    for bin_name in sorted(bin_total):
        per_bin_rows.append(
            {
                "bin": bin_name,
                "total_rows": bin_total[bin_name],
                "duplicate_group_count": bin_duplicate_group_count.get(bin_name, 0),
                "rows_in_a_duplicate_group": bin_duplicate_member_count.get(bin_name, 0),
                "singleton_rows": bin_total[bin_name] - bin_duplicate_member_count.get(bin_name, 0),
            }
        )
    write_csv(
        OUT / "CR215_per_bin_duplicate_summary.csv",
        per_bin_rows,
        [
            "bin",
            "total_rows",
            "duplicate_group_count",
            "rows_in_a_duplicate_group",
            "singleton_rows",
        ],
    )

    # 7. Build annotated copy of the 195-row CSV (original columns + new
    # trailing numeric_duplicate_class column). No row reordering, no row
    # deletion, no value rewriting.
    annotated_fields = list(fieldnames) + ["numeric_duplicate_class"]
    annotated_rows = []
    for idx, row in enumerate(rows, start=1):
        new_row = dict(row)
        new_row["numeric_duplicate_class"] = duplicate_class_by_row_index.get(idx, "none")
        annotated_rows.append(new_row)
    annotated_path = OUT / "CR215_particle_complement_195_annotated.csv"
    write_csv(annotated_path, annotated_rows, annotated_fields)

    # 8. Summary JSON.
    summary = {
        "cr_id": "CR215",
        "test_id": "CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "input_csv": rel(INPUT_CSV),
        "input_csv_sealed_sha256": SEALED_INPUT_SHA256,
        "input_csv_observed_sha256": input_hash,
        "input_sha256_match": hash_match,
        "input_row_count": row_count,
        "numeric_signature_columns": SIGNATURE_COLUMNS,
        "descriptor_diff_columns": DESCRIPTOR_DIFF_COLUMNS,
        "duplicate_group_count": len(duplicate_groups),
        "rows_in_a_duplicate_group": sum(len(m) for m in duplicate_groups.values()),
        "per_bin_summary": per_bin_rows,
        "annotated_row_count": len(annotated_rows),
        "annotated_added_column": "numeric_duplicate_class",
        "annotated_added_column_values_used": sorted(
            {r["numeric_duplicate_class"] for r in annotated_rows}
        ),
        "row_preservation": {
            "rule": "all_input_rows_preserved_in_original_order",
            "input_rows": row_count,
            "annotated_rows": len(annotated_rows),
            "match": row_count == len(annotated_rows),
        },
        "non_destructive": {
            "rule": "sealed_CR214_csv_unmodified",
            "verified_by_hash_match": hash_match,
        },
    }

    checks = {
        "input_sha256_matches_sealed": hash_match,
        "input_row_count_is_195": row_count == 195,
        "annotated_row_count_matches_input": len(annotated_rows) == row_count,
        "annotated_has_added_column": "numeric_duplicate_class" in annotated_fields,
        "annotated_added_exactly_one_column": len(annotated_fields) == len(fieldnames) + 1,
        "duplicate_class_singleton_label_is_none": all(
            (r["numeric_duplicate_class"] == "none")
            or r["numeric_duplicate_class"].startswith("DUP-")
            for r in annotated_rows
        ),
    }
    summary["checks"] = checks
    summary["checks_passed"] = sum(1 for v in checks.values() if v)
    summary["checks_total"] = len(checks)
    summary["execution_status"] = "CLEAN" if all(checks.values()) else "FAIL"

    if duplicate_groups:
        summary["result_class"] = (
            "CR215_FINDING_NUMERIC_DUPLICATE_PRESENT__"
            f"{len(duplicate_groups)}_GROUP__"
            f"{sum(len(m) for m in duplicate_groups.values())}_ROWS__"
            "ALL_INPUT_ROWS_PRESERVED__SEALED_INPUT_UNMODIFIED"
        )
    else:
        summary["result_class"] = (
            "CR215_PASS_NO_NUMERIC_DUPLICATES_IN_195_ROW_COMPLEMENT"
        )

    write_json(OUT / "CR215_summary.json", summary)

    # 9. Hashes of all CR215 output artifacts (including the verified input).
    hash_targets = [
        INPUT_CSV,
        OUT / "CR215_PRECOMMIT.md",
        OUT / "CR215_declared_premises.json",
        OUT / "CR215_runner.py",
        OUT / "CR215_input_manifest.csv",
        OUT / "CR215_numeric_signature_keys.csv",
        OUT / "CR215_numeric_duplicate_groups.csv",
        OUT / "CR215_per_bin_duplicate_summary.csv",
        OUT / "CR215_particle_complement_195_annotated.csv",
        OUT / "CR215_summary.json",
        OUT / "CR215_result.md",
    ]
    lines = ["artifact,sha256"]
    for target in hash_targets:
        if target.exists():
            lines.append(f"{rel(target)},{sha256_file(target)}")
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 10. Input manifest.
    manifest_rows = [
        {
            "artifact": rel(INPUT_CSV),
            "sealed_sha256": SEALED_INPUT_SHA256,
            "observed_sha256": input_hash,
            "match": "yes" if hash_match else "no",
            "role": "sealed_input_under_test",
        }
    ]
    write_csv(
        OUT / "CR215_input_manifest.csv",
        manifest_rows,
        ["artifact", "sealed_sha256", "observed_sha256", "match", "role"],
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
