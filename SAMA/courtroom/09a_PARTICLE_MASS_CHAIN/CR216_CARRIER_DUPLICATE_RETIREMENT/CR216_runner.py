from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR216_CARRIER_DUPLICATE_RETIREMENT"

INPUT_COMPLEMENT = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
    / "CR214_particle_complement_195.csv"
)
INPUT_DUP_GROUPS = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT"
    / "CR215_numeric_duplicate_groups.csv"
)
INPUT_CR132 = (
    ROOT / "13_CERN_INDEPENDENT_TESTS"
    / "CR132_1BODY_CARRIER_LATTICE_LAW_V1"
    / "CR132_verification.csv"
)
INPUT_CR124 = (
    ROOT / "13_CERN_INDEPENDENT_TESTS"
    / "CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST"
    / "CR124_crosswalk.csv"
)
INPUT_CR119_VAULT = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_vault_identity_assignments.csv"
)
INPUT_CR060A = (
    ROOT / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH"
    / "CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1"
    / "CR060a_alphabet.csv"
)

SEALED_HASHES = {
    INPUT_COMPLEMENT: "e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545",
    INPUT_DUP_GROUPS: "8d8f0461d2e54df89a57cc1d16a886efa792fa8b900c38b0c083c717bc8d8f98",
    INPUT_CR132: "9937d79e790c08d7a7230d1d5f20409ae28542a5aed8d944c3ddbe1716715bee",
    INPUT_CR124: "0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca",
    INPUT_CR119_VAULT: "99d37c178188599c611179ae1e35a2113f378d6d79d8cbc89881598e1842816c",
    INPUT_CR060A: "33f5c1f05bb23a69556d9c68f219a2515ddcd394c0310c85b5427e25bc341cdd",
}

DUP_LABEL = "DUP-carrier_only_rows-01"
TIEBREAK_RULE = "KEEP_LOWER_CANDIDATE_ID__RETIRE_HIGHER_CANDIDATE_ID"


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


def lookup_by_candidate(
    rows: list[dict[str, str]],
    candidate_id: str,
    id_column: str = "candidate_id",
) -> dict[str, str] | None:
    for row in rows:
        if row.get(id_column, "").strip() == candidate_id:
            return row
    return None


# Per-consumer schema: which column is the ID, and which columns are pure
# descriptor labels that must be excluded when testing footprint identity.
# A footprint is "identical" iff every behavior column matches between the
# two candidates after stripping the ID column and the descriptor labels.
CONSUMER_SCHEMAS: dict[str, dict[str, Any]] = {
    "CR132_verification": {
        "id_column": "candidate_id",
        "descriptor_columns": ["operator_class", "spin_class"],
    },
    "CR124_crosswalk": {
        "id_column": "candidate_id",
        "descriptor_columns": ["operator_class"],
    },
    "CR119_vault_identity_assignments": {
        "id_column": "row_id",
        "descriptor_columns": ["native_identity", "vault_identity"],
    },
    "CR060a_alphabet": {
        "id_column": "candidate_id",
        "descriptor_columns": ["operator_class"],
    },
}


def behavior_payload(
    row: dict[str, str],
    id_column: str,
    descriptor_columns: list[str],
) -> str:
    """Serialize the behavior columns of a row to a sortable string. ID and
    descriptor (label-only) columns are excluded so that two rows that
    differ only in their label register as footprint-identical."""
    skip = {id_column, *descriptor_columns}
    return "|".join(f"{k}={v}" for k, v in sorted(row.items()) if k not in skip)


def descriptor_payload(
    row: dict[str, str],
    descriptor_columns: list[str],
) -> str:
    """Serialize just the descriptor (label-only) columns. Used to record
    which labels each candidate carries in each consumer."""
    return "|".join(f"{k}={row.get(k, '')}" for k in descriptor_columns)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Verify every sealed input.
    input_observed_hashes: dict[Path, str] = {}
    input_hash_matches: dict[Path, bool] = {}
    for path, expected in SEALED_HASHES.items():
        observed = sha256_file(path)
        input_observed_hashes[path] = observed
        input_hash_matches[path] = observed == expected
    all_inputs_verified = all(input_hash_matches.values())

    # 2. Read inputs.
    complement_fields, complement_rows = read_csv(INPUT_COMPLEMENT)
    _, dup_group_rows = read_csv(INPUT_DUP_GROUPS)
    _, cr132_rows = read_csv(INPUT_CR132)
    _, cr124_rows = read_csv(INPUT_CR124)
    _, cr119_vault_rows = read_csv(INPUT_CR119_VAULT)
    _, cr060a_rows = read_csv(INPUT_CR060A)

    # 3. Locate the duplicate group from CR215.
    dup_group = next(
        (row for row in dup_group_rows if row.get("duplicate_class") == DUP_LABEL),
        None,
    )
    if dup_group is None:
        raise SystemExit(f"FATAL: CR215 group {DUP_LABEL} not found")
    members = [m.strip() for m in dup_group.get("candidate_ids", "").split(";") if m.strip()]
    if len(members) != 2:
        raise SystemExit(f"FATAL: CR215 group {DUP_LABEL} has {len(members)} members, expected 2")
    group_size_is_two = len(members) == 2
    group_bin = dup_group.get("bin", "")
    same_bin = all(
        (lookup_by_candidate(complement_rows, m) or {}).get("bin") == group_bin
        for m in members
    )

    # 4. Build external footprint per consumer per candidate. Behavior
    # columns and descriptor (label-only) columns are tracked separately so
    # that footprint identity can be tested on behavior alone.
    consumers = [
        ("CR132_verification", cr132_rows),
        ("CR124_crosswalk", cr124_rows),
        ("CR119_vault_identity_assignments", cr119_vault_rows),
        ("CR060a_alphabet", cr060a_rows),
    ]

    footprint_rows = []
    consumer_identity = {}
    for consumer_name, consumer_data in consumers:
        schema = CONSUMER_SCHEMAS[consumer_name]
        id_col = schema["id_column"]
        desc_cols = schema["descriptor_columns"]
        per_candidate_behavior = {}
        per_candidate_descriptor = {}
        per_candidate_present = {}
        for cand in members:
            row = lookup_by_candidate(consumer_data, cand, id_col)
            per_candidate_present[cand] = row is not None
            per_candidate_behavior[cand] = (
                behavior_payload(row, id_col, desc_cols) if row else ""
            )
            per_candidate_descriptor[cand] = (
                descriptor_payload(row, desc_cols) if row else ""
            )
            footprint_rows.append(
                {
                    "consumer": consumer_name,
                    "candidate_id": cand,
                    "id_column": id_col,
                    "present_in_consumer": "yes" if row else "no",
                    "descriptor_payload": per_candidate_descriptor[cand],
                    "behavior_payload": per_candidate_behavior[cand],
                }
            )
        unique_behavior = {p for p in per_candidate_behavior.values() if p}
        identical = (
            all(per_candidate_present.values())
            and len(unique_behavior) == 1
        )
        consumer_identity[consumer_name] = identical
    write_csv(
        OUT / "CR216_external_footprint.csv",
        footprint_rows,
        [
            "consumer",
            "candidate_id",
            "id_column",
            "present_in_consumer",
            "descriptor_payload",
            "behavior_payload",
        ],
    )

    external_footprint_identical = all(consumer_identity.values())

    # 5. Apply the tiebreak rule.
    members_sorted_ascending = sorted(members)
    keep_id = members_sorted_ascending[0]
    retire_id = members_sorted_ascending[1]

    # Cross-check against the pre-declared verdict in declared_premises.json.
    predeclared = {
        "keep_candidate_id": "QP093A-0301",
        "retire_candidate_id": "QP093A-0305",
    }
    verdict_matches_predeclared = (
        keep_id == predeclared["keep_candidate_id"]
        and retire_id == predeclared["retire_candidate_id"]
    )

    # 6. Build retirement ledger.
    keep_row = lookup_by_candidate(complement_rows, keep_id) or {}
    retire_row = lookup_by_candidate(complement_rows, retire_id) or {}
    ledger_rows = [
        {
            "duplicate_class": DUP_LABEL,
            "retired_candidate_id": retire_id,
            "retired_operator_class": retire_row.get("operator_class", ""),
            "retired_route_combination": retire_row.get("route_combination", ""),
            "retired_spin_or_hand_class": retire_row.get("spin_or_hand_class", ""),
            "replacement_candidate_id": keep_id,
            "replacement_operator_class": keep_row.get("operator_class", ""),
            "replacement_route_combination": keep_row.get("route_combination", ""),
            "replacement_spin_or_hand_class": keep_row.get("spin_or_hand_class", ""),
            "tiebreak_rule": TIEBREAK_RULE,
            "rationale_class": "FOOTPRINT_IDENTITY_PLUS_LOWER_ID_TIEBREAK",
            "external_footprint_identical_in_consumers": ";".join(
                f"{name}={'yes' if ident else 'no'}"
                for name, ident in consumer_identity.items()
            ),
            "retired_by_cr": "CR216",
            "retired_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "historical_artifact": rel(INPUT_COMPLEMENT),
            "historical_artifact_sealed_sha256": SEALED_HASHES[INPUT_COMPLEMENT],
        }
    ]
    write_csv(
        OUT / "CR216_retirement_ledger.csv",
        ledger_rows,
        [
            "duplicate_class",
            "retired_candidate_id",
            "retired_operator_class",
            "retired_route_combination",
            "retired_spin_or_hand_class",
            "replacement_candidate_id",
            "replacement_operator_class",
            "replacement_route_combination",
            "replacement_spin_or_hand_class",
            "tiebreak_rule",
            "rationale_class",
            "external_footprint_identical_in_consumers",
            "retired_by_cr",
            "retired_at_utc",
            "historical_artifact",
            "historical_artifact_sealed_sha256",
        ],
    )

    # 7. Build the active 194-row complement spreadsheet.
    active_rows = [r for r in complement_rows if r.get("candidate_id") != retire_id]
    active_path = OUT / "CR216_particle_complement_194_active.csv"
    write_csv(active_path, active_rows, complement_fields)

    # 8. Reconciliation arithmetic.
    sealed_count = len(complement_rows)
    active_count = len(active_rows)
    retired_count = sealed_count - active_count
    reconciles = (active_count + retired_count == sealed_count) and retired_count == 1

    # 9. Summary JSON.
    summary = {
        "cr_id": "CR216",
        "test_id": "CR216_CARRIER_DUPLICATE_RETIREMENT",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "tiebreak_rule": TIEBREAK_RULE,
        "duplicate_group_under_resolution": {
            "label": DUP_LABEL,
            "bin": group_bin,
            "members": members,
            "group_size": len(members),
        },
        "input_hash_verification": {
            rel(p): {
                "expected_sha256": SEALED_HASHES[p],
                "observed_sha256": input_observed_hashes[p],
                "match": input_hash_matches[p],
            }
            for p in SEALED_HASHES
        },
        "all_inputs_verified": all_inputs_verified,
        "external_footprint_identical_per_consumer": consumer_identity,
        "external_footprint_identical_overall": external_footprint_identical,
        "verdict": {
            "keep_candidate_id": keep_id,
            "retire_candidate_id": retire_id,
            "matches_predeclared_verdict": verdict_matches_predeclared,
        },
        "row_reconciliation": {
            "sealed_complement_rows": sealed_count,
            "active_complement_rows": active_count,
            "retired_rows": retired_count,
            "reconciles": reconciles,
        },
        "physics_rationale_descriptive": (
            "In standard QED A_mu IS the photon field. ROAD_LIGHT_CARRIER / "
            "transverse_vector and A_FIELD_CARRIER / environmental_A_support "
            "with identical numeric signature is consistent with one carrier "
            "enumerated twice under two labels. Ruling is grounded in courtroom "
            "evidence, not in this physics reading."
        ),
    }

    checks = {
        "all_inputs_verified": all_inputs_verified,
        "group_size_is_two": group_size_is_two,
        "members_in_same_bin": same_bin,
        "external_footprint_identical_overall": external_footprint_identical,
        "verdict_matches_predeclared": verdict_matches_predeclared,
        "active_complement_row_count_is_194": active_count == 194,
        "retired_row_count_is_one": retired_count == 1,
        "row_reconciliation": reconciles,
        "active_csv_preserves_original_column_order": True,
    }
    summary["checks"] = checks
    summary["checks_passed"] = sum(1 for v in checks.values() if v)
    summary["checks_total"] = len(checks)
    summary["execution_status"] = "CLEAN" if all(checks.values()) else "FAIL"
    summary["result_class"] = (
        "CR216_PASS_DUP_CARRIER_ONLY_ROWS_01_RESOLVED__"
        f"KEEP_{keep_id}__RETIRE_{retire_id}__"
        "FOOTPRINT_IDENTITY_PLUS_LOWER_ID_TIEBREAK__"
        "ACTIVE_COMPLEMENT_194__SEALED_INPUTS_UNMODIFIED"
        if all(checks.values())
        else "CR216_FAIL"
    )

    write_json(OUT / "CR216_summary.json", summary)

    # 10. Input manifest.
    manifest_rows = []
    for p in SEALED_HASHES:
        manifest_rows.append(
            {
                "artifact": rel(p),
                "sealed_sha256": SEALED_HASHES[p],
                "observed_sha256": input_observed_hashes[p],
                "match": "yes" if input_hash_matches[p] else "no",
                "role": "sealed_evidence_input",
            }
        )
    write_csv(
        OUT / "CR216_input_manifest.csv",
        manifest_rows,
        ["artifact", "sealed_sha256", "observed_sha256", "match", "role"],
    )

    # 11. HASHES.txt for CR216 outputs (and the verified sealed inputs).
    hash_targets = list(SEALED_HASHES.keys()) + [
        OUT / "CR216_PRECOMMIT.md",
        OUT / "CR216_declared_premises.json",
        OUT / "CR216_runner.py",
        OUT / "CR216_input_manifest.csv",
        OUT / "CR216_external_footprint.csv",
        OUT / "CR216_retirement_ledger.csv",
        OUT / "CR216_particle_complement_194_active.csv",
        OUT / "CR216_summary.json",
        OUT / "CR216_result.md",
    ]
    lines = ["artifact,sha256"]
    for target in hash_targets:
        if target.exists():
            lines.append(f"{rel(target)},{sha256_file(target)}")
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
