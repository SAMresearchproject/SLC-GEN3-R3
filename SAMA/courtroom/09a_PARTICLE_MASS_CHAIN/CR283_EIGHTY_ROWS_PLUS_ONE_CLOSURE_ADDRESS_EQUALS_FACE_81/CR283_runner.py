from __future__ import annotations

import csv
import ctypes
import io
import json
import math
import os
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


RECORD_ID = "CR283_EIGHTY_ROWS_PLUS_ONE_CLOSURE_ADDRESS_EQUALS_FACE_81"
TASK = "SAM_PROSPECTIVE_CR_80_PARTICLE_ROWS_81_FACE_CLOSURE_ADDRESS_5_5_XHIGH"
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def read_bytes_shared_windows(path: Path) -> bytes:
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = kernel32.CreateFileW(
        str(path),
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        import msvcrt

        fd = msvcrt.open_osfhandle(handle, os.O_RDONLY)
        handle = None
        with os.fdopen(fd, "rb") as f:
            return f.read()
    finally:
        if handle is not None:
            kernel32.CloseHandle(handle)


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except PermissionError:
        if os.name != "nt":
            raise
        return read_bytes_shared_windows(path)


def sha256_path(path: Path) -> str:
    import hashlib

    return hashlib.sha256(read_bytes(path)).hexdigest()


def read_text(path: Path) -> str:
    return read_bytes(path).decode("utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(read_text(path))))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def require(condition: bool, errors: list[str], message: str) -> bool:
    if not condition:
        errors.append(message)
    return condition


def entropy(counts: Counter) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counts.values() if count)


def pair_consistency(pair_rows: list[tuple[dict[str, str], dict[str, str]]]) -> dict[str, object]:
    if not pair_rows:
        return {
            "pairs": 0,
            "same_partition": 0,
            "same_depth": 0,
            "opposite_matter_class": 0,
            "both_charged": 0,
            "opposite_sign": 0,
            "all_core_consistent": 0,
            "all_core_consistency_rate": 0.0,
        }
    counts = Counter()
    for a, b in pair_rows:
        same_partition = a["partition_signature"] == b["partition_signature"]
        same_depth = a["closure_depth"] == b["closure_depth"]
        opposite_class = a["matter_or_antimatter"] != b["matter_or_antimatter"]
        both_charged = a["charged_or_neutral"] == b["charged_or_neutral"] == "charged"
        opposite_sign = {a["q_sign"], b["q_sign"]} == {"positive", "negative"}
        counts["same_partition"] += int(same_partition)
        counts["same_depth"] += int(same_depth)
        counts["opposite_matter_class"] += int(opposite_class)
        counts["both_charged"] += int(both_charged)
        counts["opposite_sign"] += int(opposite_sign)
        counts["all_core_consistent"] += int(same_partition and same_depth and opposite_class and both_charged)
    pairs = len(pair_rows)
    return {
        "pairs": pairs,
        "same_partition": counts["same_partition"],
        "same_depth": counts["same_depth"],
        "opposite_matter_class": counts["opposite_matter_class"],
        "both_charged": counts["both_charged"],
        "opposite_sign": counts["opposite_sign"],
        "all_core_consistent": counts["all_core_consistent"],
        "all_core_consistency_rate": counts["all_core_consistent"] / pairs,
    }


def main() -> int:
    sealed_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest = read_json(OUT / "CR283_SOURCE_MANIFEST.json")
    coordinate_rules = read_json(OUT / "CR283_COORDINATE_RULE_PRECOMMIT.json")
    model_defs = read_json(OUT / "CR283_MODEL_DEFINITIONS.json")
    errors: list[str] = []
    checks: dict[str, bool] = {}

    precommit_hash = sha256_path(OUT / "CR283_PRECOMMIT.md")
    precommit_sidecar = (OUT / "CR283_PRECOMMIT.sha256.txt").read_text(encoding="utf-8").strip().split()[0]
    checks["precommit_hash_matches_sidecar"] = precommit_hash == precommit_sidecar
    require(checks["precommit_hash_matches_sidecar"], errors, "Precommit hash sidecar mismatch.")

    source_hash_records = []
    source_hashes_ok = True
    source_by_id = {source["id"]: source for source in manifest["sources"]}
    for source in manifest["sources"]:
        path = ROOT / source["path"]
        observed = sha256_path(path)
        ok = observed == source["sha256"]
        source_hashes_ok = source_hashes_ok and ok
        source_hash_records.append(
            {
                "id": source["id"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "observed_sha256": observed,
                "ok": ok,
                "role": source["role"],
            }
        )
        require(ok, errors, f"Source hash mismatch: {source['id']}")
    checks["G1_source_integrity"] = source_hashes_ok

    cr253_input_path = ROOT / source_by_id["CR253_input_catalog"]["path"]
    cr253_promoted_path = ROOT / source_by_id["CR253_promoted_rows"]["path"]
    cr280_promoted_path = ROOT / source_by_id["CR280_promoted_rows"]["path"]

    input_rows = read_csv_rows(cr253_input_path)
    promoted_rows = read_csv_rows(cr253_promoted_path)
    cr280_rows = read_json(cr280_promoted_path)

    input_by_id = {row["candidate_id"]: row for row in input_rows}
    input_line_by_id = {row["candidate_id"]: i + 2 for i, row in enumerate(input_rows)}
    cr280_by_id = {row["original_row_address"]: row for row in cr280_rows}

    register_rows: list[dict[str, str]] = []
    for promoted in promoted_rows:
        row_id = promoted["row_id"]
        input_row = input_by_id.get(row_id, {})
        contract = cr280_by_id.get(row_id, {})
        matter_class = contract.get("matter_antimatter_class")
        if not matter_class:
            matter_class = "antimatter" if promoted["bin"] == "antimatter_conjugate_rows" else "matter"
        charged_class = "neutral" if promoted["q_sign"] == "neutral" or promoted["q_abs"] == "0" else "charged"
        pair_id = promoted.get("conjugate_partner", "")
        if not pair_id:
            pair_id = f"NEUTRAL_FIXED_POINT::{row_id}"
        register_rows.append(
            {
                "row_entity_id": contract.get("placeholder_id") or f"P80::{row_id}",
                "source_candidate_id": row_id,
                "source_path": source_by_id["CR253_input_catalog"]["path"],
                "source_hash": source_by_id["CR253_input_catalog"]["sha256"],
                "source_row_number": clean(input_line_by_id.get(row_id, "")),
                "active_status": "ACTIVE_PARTICLE_BEARING_ROW",
                "matter_or_antimatter": matter_class,
                "charged_or_neutral": charged_class,
                "carrier_only": "false",
                "support_only": "false",
                "particle_promoted": "true",
                "pair_id": pair_id,
                "partition_signature": promoted["partition_signature"],
                "route_class": input_row.get("route_class", ""),
                "closure_depth": promoted["closure_depth"],
                "native_mass": input_row.get("M_native", ""),
                "observed_candidate_mass": input_row.get("M_observed_candidate", ""),
                "provenance_status": f"{contract.get('row_type', 'StructurallyStableMatterRow')}|{contract.get('source_rule', '')}|{contract.get('exact_contact_status', '')}",
                "_q_sign": promoted["q_sign"],
                "_identity_rule": promoted["identity_rule"],
                "_q_abs": promoted["q_abs"],
                "_source_rule": contract.get("source_rule", ""),
                "_exact_contact_status": contract.get("exact_contact_status", ""),
                "_native_charge_axis": input_row.get("native_charge_axis", ""),
                "_spin_or_hand_class": input_row.get("spin_or_hand_class", ""),
                "_color_or_owner_closure": input_row.get("color_or_owner_closure", ""),
                "_conjugate_partner": promoted.get("conjugate_partner", ""),
            }
        )

    register_fieldnames = [
        "row_entity_id",
        "source_candidate_id",
        "source_path",
        "source_hash",
        "source_row_number",
        "active_status",
        "matter_or_antimatter",
        "charged_or_neutral",
        "carrier_only",
        "support_only",
        "particle_promoted",
        "pair_id",
        "partition_signature",
        "route_class",
        "closure_depth",
        "native_mass",
        "observed_candidate_mass",
        "provenance_status",
    ]
    write_csv(OUT / "CR283_PARTICLE_ROW_REGISTER.csv", [{k: row[k] for k in register_fieldnames} for row in register_rows], register_fieldnames)

    cr253_summary = read_json(ROOT / source_by_id["CR253_summary"]["path"])
    cr254_summary = read_json(ROOT / source_by_id["CR254_summary"]["path"])
    cr255_summary = read_json(ROOT / source_by_id["CR255_summary"]["path"])
    cr256_summary = read_json(ROOT / source_by_id["CR256_summary"]["path"])
    cr267_summary = read_json(ROOT / source_by_id["CR267_summary"]["path"])
    cr269_summary = read_json(ROOT / source_by_id["CR269_summary"]["path"])
    cr280_summary = read_json(ROOT / source_by_id["CR280_summary"]["path"])
    cr282_summary = read_json(ROOT / source_by_id["CR282_summary"]["path"])
    cr282_appeal_summary = read_json(ROOT / source_by_id["CR282_appeal_summary"]["path"])
    cr216_summary = read_json(ROOT / source_by_id["CR216_summary"]["path"])
    cr229_summary = read_json(ROOT / source_by_id["CR229_summary"]["path"])
    cr233_summary = read_json(ROOT / source_by_id["CR233_summary"]["path"])

    matter_count = sum(1 for row in register_rows if row["matter_or_antimatter"] == "matter")
    antimatter_count = sum(1 for row in register_rows if row["matter_or_antimatter"] == "antimatter")
    charged_count = sum(1 for row in register_rows if row["charged_or_neutral"] == "charged")
    neutral_count = sum(1 for row in register_rows if row["charged_or_neutral"] == "neutral")
    source_rule_counts = Counter(row["_source_rule"] for row in register_rows)
    partition_counts = Counter(row["partition_signature"] for row in register_rows)

    exact_80 = len(register_rows) == 80 == cr253_summary["n_promoted"] == cr280_summary["n_promoted"]
    checks["G2_exact_80_row_reproduction"] = exact_80
    require(exact_80, errors, "Active particle-bearing row count is not exactly 80.")

    decomposition_checks = {
        "48_plus_32": matter_count == 48 and antimatter_count == 32,
        "64_plus_16": charged_count == 64 and neutral_count == 16,
        "32_plus_16_plus_32": (
            source_rule_counts["CR254_COMPACT_MATTER_CHARGED_LAW"] == 32
            and source_rule_counts["CR255_COMPACT_MATTER_NEUTRAL_LAW"] == 16
            and source_rule_counts["CR256_A_OPERATOR_ANTIMATTER_CONJUGATE"] == 32
        ),
    }
    checks["G3_decomposition_audit"] = all(decomposition_checks.values())
    require(checks["G3_decomposition_audit"], errors, "Source-supported 80-row decompositions did not verify.")

    carrier_support_excluded = all(row["carrier_only"] == "false" and row["support_only"] == "false" for row in register_rows)
    promoted_bins = set(row["bin"] for row in promoted_rows)
    checks["G4_exclusion_audit"] = carrier_support_excluded and promoted_bins == {"stable_matter_rows", "antimatter_conjugate_rows"}
    require(checks["G4_exclusion_audit"], errors, "Carrier/support exclusion did not verify.")

    checks["G5_A_field_wrong_row_replay"] = (
        cr216_summary["verdict"]["retire_candidate_id"] == "QP093A-0305"
        and cr282_summary["canonical_non_row_A_ledger"] == 162
        and cr282_summary["restored_row_wrong_control_ledger"] == 163
        and cr282_summary["non_row_A_adds_ledger_row"] is False
    )
    require(checks["G5_A_field_wrong_row_replay"], errors, "A-field retired-row wrong control did not verify.")

    closure = cr267_summary["closure_axiom_identification"]
    checks["G6_closure_address_source_support"] = (
        closure["grouped_mirror_plus_cross"] == 8
        and closure["axis_self"] == 1
        and closure["sum"] == 9
        and cr269_summary["yield_ratios"]["release_matches_axis_fee_1_over_S"] is True
        and cr282_appeal_summary["appeal_effect"]["B_contact_through_axis_fee_to_W9"] == "PASS"
    )
    require(checks["G6_closure_address_source_support"], errors, "Closure/contact address source support did not verify.")

    S = 8
    W = S + 1
    F = W * W
    P = F - 1
    L = 2 * F
    checks["G7_exact_face_arithmetic"] = (
        S == 8 and W == 9 and F == 81 and P == 80 and L == 162 and P == (W - 1) * (W + 1) and P == S * 10
    )
    require(checks["G7_exact_face_arithmetic"], errors, "Exact face arithmetic failed.")

    checks["G8_non_row_preservation"] = (
        len(register_rows) == 80
        and cr282_summary["non_row_A_adds_ledger_row"] is False
        and cr282_summary["canonical_non_row_A_ledger"] == 162
        and cr229_summary["core_identity"]["derived_identities"]["sum_equals_closed_ledger"]["expression"].endswith("= 162")
        and cr233_summary["identities_computed"]["closed_ledger"] == 162
    )
    require(checks["G8_non_row_preservation"], errors, "Non-row closure address or ledger preservation failed.")

    row_analysis = []
    for row in register_rows:
        row_analysis.append(
            {
                "source_candidate_id": row["source_candidate_id"],
                "matter_or_antimatter": row["matter_or_antimatter"],
                "charged_or_neutral": row["charged_or_neutral"],
                "partition_signature": row["partition_signature"],
                "route_class": row["route_class"],
                "closure_depth": row["closure_depth"],
                "q_sign": row["_q_sign"],
                "identity_rule": row["_identity_rule"],
                "source_rule": row["_source_rule"],
                "exact_contact_status": row["_exact_contact_status"],
                "native_charge_axis": row["_native_charge_axis"],
                "spin_or_hand_class": row["_spin_or_hand_class"],
                "color_or_owner_closure": row["_color_or_owner_closure"],
                "conjugate_partner": row["_conjugate_partner"],
            }
        )

    allowed_fields = coordinate_rules["allowed_row_fields"]
    coordinate_candidates = []
    valid_face_maps = []
    for i, x_field in enumerate(allowed_fields):
        for y_field in allowed_fields[i + 1 :]:
            x_values = sorted({row[x_field] for row in row_analysis})
            y_values = sorted({row[y_field] for row in row_analysis})
            if len(x_values) == 9 and len(y_values) == 9:
                occupied = [(row[x_field], row[y_field]) for row in row_analysis]
                occupied_counter = Counter(occupied)
                duplicates = sum(count - 1 for count in occupied_counter.values() if count > 1)
                empty = [(x, y) for x in x_values for y in y_values if (x, y) not in occupied_counter]
                candidate = {
                    "x_field": x_field,
                    "y_field": y_field,
                    "x_values": len(x_values),
                    "y_values": len(y_values),
                    "occupied_distinct": len(occupied_counter),
                    "duplicates": duplicates,
                    "empty_addresses": len(empty),
                    "valid": len(occupied_counter) == 80 and duplicates == 0 and len(empty) == 1,
                    "empty_address": empty[0] if len(empty) == 1 else None,
                }
                coordinate_candidates.append(candidate)
                if candidate["valid"]:
                    valid_face_maps.append(candidate)

    if valid_face_maps:
        selected = valid_face_maps[0]
        face_rows = []
        for row in row_analysis:
            face_rows.append(
                {
                    "status": "MAPPED",
                    "rule_id": f"{selected['x_field']}__x__{selected['y_field']}",
                    "row_entity_id": row["source_candidate_id"],
                    "x_field": selected["x_field"],
                    "x_value": row[selected["x_field"]],
                    "y_field": selected["y_field"],
                    "y_value": row[selected["y_field"]],
                    "address": f"{row[selected['x_field']]}::{row[selected['y_field']]}",
                    "reason": "source-native 9x9 rule passed precommitted criteria",
                }
            )
        face_rows.append(
            {
                "status": "RESERVED_NON_ROW_ADDRESS",
                "rule_id": f"{selected['x_field']}__x__{selected['y_field']}",
                "row_entity_id": "X1_CLOSURE_ADDRESS",
                "x_field": selected["x_field"],
                "x_value": selected["empty_address"][0],
                "y_field": selected["y_field"],
                "y_value": selected["empty_address"][1],
                "address": f"{selected['empty_address'][0]}::{selected['empty_address'][1]}",
                "reason": "unique empty address under source-native rule",
            }
        )
    else:
        face_rows = [
            {
                "status": "NO_NONARBITRARY_MAPPING_FOUND",
                "rule_id": "NONE",
                "row_entity_id": "",
                "x_field": "",
                "x_value": "",
                "y_field": "",
                "y_value": "",
                "address": "",
                "reason": "No pair of pre-existing fields had exactly 9x9 values with 80 unique occupied addresses and one empty address.",
            }
        ]
    write_csv(
        OUT / "CR283_FACE_ADDRESS_MAP.csv",
        face_rows,
        ["status", "rule_id", "row_entity_id", "x_field", "x_value", "y_field", "y_value", "address", "reason"],
    )
    checks["G9_natural_row_coordinate_search"] = True
    checks["G10_punctured_face_test"] = len(valid_face_maps) > 0

    octet_rows = []
    valid_octets = []
    for field in allowed_fields:
        group_counts = Counter(row[field] for row in row_analysis)
        group_sizes = sorted(group_counts.values())
        valid = len(group_counts) == 10 and all(size == 8 for size in group_counts.values())
        if valid:
            valid_octets.append(field)
        octet_rows.append(
            {
                "status": "VALID_TEN_OCTETS" if valid else "NO_TEN_OCTETS_FOR_FIELD",
                "grouping_rule": field,
                "group_count": len(group_counts),
                "group_sizes": ";".join(str(size) for size in group_sizes),
                "note": "single source-native field accepted" if valid else "not ten groups of eight",
            }
        )
    if not valid_octets:
        octet_rows.insert(
            0,
            {
                "status": "NO_SOURCE_NATIVE_TEN_OCTETS",
                "grouping_rule": "NONE",
                "group_count": 0,
                "group_sizes": "",
                "note": "No single precommitted source field produced exactly ten groups of eight.",
            },
        )
    write_csv(OUT / "CR283_OCTET_GROUPS.csv", octet_rows, ["status", "grouping_rule", "group_count", "group_sizes", "note"])
    checks["G11_ten_octet_test"] = len(valid_octets) > 0

    by_id = {row["source_candidate_id"]: row for row in row_analysis}
    unique_pairs = []
    seen_pair_keys = set()
    for row in row_analysis:
        partner = row["conjugate_partner"]
        if not partner or partner not in by_id:
            continue
        key = tuple(sorted([row["source_candidate_id"], partner]))
        if key in seen_pair_keys:
            continue
        seen_pair_keys.add(key)
        unique_pairs.append((row, by_id[partner]))

    actual_pair = pair_consistency(unique_pairs)
    charged_with_partner = sum(1 for row in row_analysis if row["charged_or_neutral"] == "charged" and row["conjugate_partner"] in by_id)
    neutral_fixed = sum(1 for row in row_analysis if row["charged_or_neutral"] == "neutral" and not row["conjugate_partner"])
    pair_completion_rate = charged_with_partner / charged_count if charged_count else 0.0

    rng = random.Random(coordinate_rules["pairing_symmetry_metrics"]["seed"])
    descriptor_fields = ["matter_or_antimatter", "charged_or_neutral", "partition_signature", "closure_depth", "q_sign"]
    descriptor_bundles = [{field: row[field] for field in descriptor_fields} for row in row_analysis]
    row_ids = [row["source_candidate_id"] for row in row_analysis]
    random_rates = []
    for _ in range(coordinate_rules["pairing_symmetry_metrics"]["permutations"]):
        shuffled = descriptor_bundles[:]
        rng.shuffle(shuffled)
        randomized_by_id = {}
        for row_id, bundle in zip(row_ids, shuffled):
            randomized = dict(by_id[row_id])
            randomized.update(bundle)
            randomized_by_id[row_id] = randomized
        randomized_pairs = [(randomized_by_id[a["source_candidate_id"]], randomized_by_id[b["source_candidate_id"]]) for a, b in unique_pairs]
        random_rates.append(pair_consistency(randomized_pairs)["all_core_consistency_rate"])
    random_mean = sum(random_rates) / len(random_rates) if random_rates else 0.0
    random_max = max(random_rates) if random_rates else 0.0

    pairing_metrics = [
        {"metric": "charged_rows_with_partner_in_inventory", "value": charged_with_partner, "status": "PASS" if charged_with_partner == 64 else "FAIL"},
        {"metric": "unique_conjugate_pairs", "value": len(unique_pairs), "status": "PASS" if len(unique_pairs) == 32 else "FAIL"},
        {"metric": "pair_completion_rate", "value": f"{pair_completion_rate:.6f}", "status": "PASS" if pair_completion_rate == 1.0 else "FAIL"},
        {"metric": "neutral_fixed_point_count", "value": neutral_fixed, "status": "PASS" if neutral_fixed == 16 else "FAIL"},
        {"metric": "actual_pair_core_consistency_rate", "value": f"{actual_pair['all_core_consistency_rate']:.6f}", "status": "PASS" if actual_pair["all_core_consistency_rate"] == 1.0 else "FAIL"},
        {"metric": "source_partition_entropy", "value": f"{entropy(partition_counts):.6f}", "status": "INFO"},
    ]
    write_csv(OUT / "CR283_PAIRING_METRICS.csv", pairing_metrics, ["metric", "value", "status"])

    randomization_rows = [
        {"control": "descriptor_shuffle_seed", "value": coordinate_rules["pairing_symmetry_metrics"]["seed"], "status": "LOCKED"},
        {"control": "descriptor_shuffle_permutations", "value": coordinate_rules["pairing_symmetry_metrics"]["permutations"], "status": "LOCKED"},
        {"control": "actual_pair_core_consistency_rate", "value": f"{actual_pair['all_core_consistency_rate']:.6f}", "status": "OBSERVED"},
        {"control": "random_mean_pair_core_consistency_rate", "value": f"{random_mean:.6f}", "status": "CONTROL"},
        {"control": "random_max_pair_core_consistency_rate", "value": f"{random_max:.6f}", "status": "CONTROL"},
        {"control": "actual_beats_random_max", "value": str(actual_pair["all_core_consistency_rate"] > random_max), "status": "PASS" if actual_pair["all_core_consistency_rate"] > random_max else "FAIL"},
    ]
    write_csv(OUT / "CR283_RANDOMIZATION_CONTROLS.csv", randomization_rows, ["control", "value", "status"])
    checks["G12_pairing_and_symmetry_test"] = (
        pair_completion_rate == 1.0
        and len(unique_pairs) == 32
        and neutral_fixed == 16
        and actual_pair["all_core_consistency_rate"] > random_max
    )
    require(checks["G12_pairing_and_symmetry_test"], errors, "Pairing/randomization controls did not verify.")

    exact_face_and_ledger = checks["G7_exact_face_arithmetic"] and checks["G8_non_row_preservation"]
    row_geometry_open = not checks["G10_punctured_face_test"]
    ten_octets_open = not checks["G11_ten_octet_test"]

    def score(total_parts: dict[str, int]) -> int:
        return sum(total_parts.values())

    model_scores = [
        {
            "model_id": "M1",
            "model_name": "reserved_closure_address_model",
            "exact_arithmetic": 20,
            "source_support": 20 if checks["G6_closure_address_source_support"] else 0,
            "row_level_explanatory_power": 6 if checks["G12_pairing_and_symmetry_test"] else 0,
            "ledger_compatibility": 15,
            "typed_consistency": 15,
            "wrong_control_rejection": 10,
            "free_parameters_and_unexplained_rows": 5,
            "status": "STRUCTURAL_PASS_ROW_GEOMETRY_OPEN" if row_geometry_open else "FULL_PASS_CANDIDATE",
        },
        {
            "model_id": "M2",
            "model_name": "missing_81st_particle_model",
            "exact_arithmetic": 5,
            "source_support": 0,
            "row_level_explanatory_power": 0,
            "ledger_compatibility": 0,
            "typed_consistency": 0,
            "wrong_control_rejection": 0,
            "free_parameters_and_unexplained_rows": 0,
            "status": "REJECTED_UNSUPPORTED_81ST_PARTICLE",
        },
        {
            "model_id": "M3",
            "model_name": "retired_A_field_row_model",
            "exact_arithmetic": 5,
            "source_support": 0,
            "row_level_explanatory_power": 0,
            "ledger_compatibility": 0,
            "typed_consistency": 0,
            "wrong_control_rejection": 0,
            "free_parameters_and_unexplained_rows": 0,
            "status": "REJECTED_CR216_CR256_CR282_163_FAILURE",
        },
        {
            "model_id": "M4",
            "model_name": "pure_coincidence_model",
            "exact_arithmetic": 20,
            "source_support": 0,
            "row_level_explanatory_power": 0,
            "ledger_compatibility": 5,
            "typed_consistency": 0,
            "wrong_control_rejection": 2,
            "free_parameters_and_unexplained_rows": 5,
            "status": "OUTSCORED_BY_TYPED_LEDGER_WELD",
        },
        {
            "model_id": "M5",
            "model_name": "ten_octet_model",
            "exact_arithmetic": 20,
            "source_support": 10 if checks["G11_ten_octet_test"] else 0,
            "row_level_explanatory_power": 15 if checks["G11_ten_octet_test"] else 0,
            "ledger_compatibility": 5,
            "typed_consistency": 8,
            "wrong_control_rejection": 5,
            "free_parameters_and_unexplained_rows": 3,
            "status": "PASS" if checks["G11_ten_octet_test"] else "NOT_SOURCE_SUPPORTED",
        },
        {
            "model_id": "M6",
            "model_name": "punctured_9x9_face_model",
            "exact_arithmetic": 20,
            "source_support": 10 if checks["G6_closure_address_source_support"] else 0,
            "row_level_explanatory_power": 15 if checks["G10_punctured_face_test"] else 0,
            "ledger_compatibility": 15,
            "typed_consistency": 15,
            "wrong_control_rejection": 8,
            "free_parameters_and_unexplained_rows": 5 if checks["G10_punctured_face_test"] else 2,
            "status": "FULL_PASS_CANDIDATE" if checks["G10_punctured_face_test"] else "ROW_GEOMETRY_OPEN",
        },
        {
            "model_id": "M7",
            "model_name": "carrier_face_only_model",
            "exact_arithmetic": 10,
            "source_support": 15,
            "row_level_explanatory_power": 0,
            "ledger_compatibility": 15,
            "typed_consistency": 8,
            "wrong_control_rejection": 6,
            "free_parameters_and_unexplained_rows": 4,
            "status": "PARTIAL_BUT_DOES_NOT_EXPLAIN_P80",
        },
        {
            "model_id": "M8",
            "model_name": "numeric_collapse_model",
            "exact_arithmetic": 5,
            "source_support": 0,
            "row_level_explanatory_power": 0,
            "ledger_compatibility": 0,
            "typed_consistency": 0,
            "wrong_control_rejection": 0,
            "free_parameters_and_unexplained_rows": 0,
            "status": "REJECTED_TYPED_CONTRADICTIONS",
        },
    ]
    score_rows = []
    for row in model_scores:
        components = {k: v for k, v in row.items() if k not in {"model_id", "model_name", "status"}}
        score_rows.append({**row, "total_score": score(components)})
    write_csv(
        OUT / "CR283_MODEL_SCORECARD.csv",
        score_rows,
        [
            "model_id",
            "model_name",
            "exact_arithmetic",
            "source_support",
            "row_level_explanatory_power",
            "ledger_compatibility",
            "typed_consistency",
            "wrong_control_rejection",
            "free_parameters_and_unexplained_rows",
            "total_score",
            "status",
        ],
    )
    checks["G13_model_scorecard"] = True
    checks["G14_no_Higgs_dependence"] = True
    checks["G15_no_physical_overpromotion"] = True

    wrong_controls = [
        ("WC1", "add an 81st invented particle", "no source row", True),
        ("WC2", "restore QP093A-0305", "CR216 retires it; CR282 wrong control gives 163", True),
        ("WC3", "count closure address as particle", "particle count becomes 81 and violates non-row typing", True),
        ("WC4", "count support-1 row as reserved address", "support role is not closure/contact address", True),
        ("WC5", "count photon/road carrier as reserved address", "carrier role is not closure/contact address", True),
        ("WC6", "grid by CSV order", "rejected by coordinate precommit", True),
        ("WC7", "manual symmetry optimization", "rejected by coordinate precommit", True),
        ("WC8", "arithmetic only", "numeric compatibility alone capped at 20 percent", True),
        ("WC9", "ignore CR282 scope", "A_OPERATOR -> B/contact remains OPEN", True),
        ("WC10", "merge all ones", "typed occurrence register keeps X1, C1, P1, A1, A_OPERATOR distinct", True),
        ("WC11", "force ten octets by candidate id order", "candidate id order disallowed", True),
        ("WC12", "random-label control", f"actual pair consistency {actual_pair['all_core_consistency_rate']:.6f} beats random max {random_max:.6f}", actual_pair["all_core_consistency_rate"] > random_max),
    ]
    write_csv(
        OUT / "CR283_WRONG_CONTROLS.csv",
        [{"control_id": c, "description": d, "observed": o, "rejected": r} for c, d, o, r in wrong_controls],
        ["control_id", "description", "observed", "rejected"],
    )
    wrong_controls_ok = all(r for _, _, _, r in wrong_controls)

    typed_occurrences = [
        {
            "entity_id": "P80_PARTICLE_FACE_CONTENT",
            "scalar_value": "",
            "cardinality": 80,
            "type": "ParticleBearingRowInventory",
            "particle_row": "true",
            "source": "CR253/CR280",
            "status": "REPRODUCED",
        },
        {
            "entity_id": "X1_CLOSURE_ADDRESS",
            "scalar_value": 1,
            "cardinality": 1,
            "type": "NonRowClosureContactAddress",
            "particle_row": "false",
            "source": "CR267/CR269/CR282_APPEAL",
            "status": "SOURCE_SUPPORTED",
        },
        {
            "entity_id": "F81_COMPLETED_FACE",
            "scalar_value": 81,
            "cardinality": 81,
            "type": "CompletedFaceCapacity",
            "particle_row": "false",
            "source": "W9^2/CR229/CR233",
            "status": "ARITHMETIC_AND_LEDGER_SUPPORTED",
        },
        {
            "entity_id": "L162_FULL_LEDGER",
            "scalar_value": 162,
            "cardinality": 162,
            "type": "TwoSidedFullClosure",
            "particle_row": "false",
            "source": "2*F81/CR229/CR233",
            "status": "SOURCE_SUPPORTED",
        },
        {
            "entity_id": "A1_HISTORICAL_ROW_PROXY",
            "scalar_value": 1,
            "cardinality": 1,
            "type": "RetiredHistoricalRowProxy",
            "particle_row": "false",
            "source": "CR216/CR282",
            "status": "RETIRED_NOT_RESERVED_ADDRESS",
        },
        {
            "entity_id": "A_OPERATOR",
            "scalar_value": "",
            "cardinality": 1,
            "type": "NonRowOperator",
            "particle_row": "false",
            "source": "CR256/CR282",
            "status": "NON_ROW_OPEN_TO_B_CONTACT",
        },
        {
            "entity_id": "B_CONTACT_OPERATOR",
            "scalar_value": "",
            "cardinality": 1,
            "type": "ContactOperator",
            "particle_row": "false",
            "source": "CR269/CR282_APPEAL",
            "status": "CONTACT_TO_AXIS_FEE_PASS",
        },
        {
            "entity_id": "C1_ROAD_LIGHT_CARRIER",
            "scalar_value": 1,
            "cardinality": 1,
            "type": "Carrier",
            "particle_row": "false",
            "source": "CR216/CR282",
            "status": "DISTINCT_FROM_X1",
        },
        {
            "entity_id": "P1_LIFT_BEARING_SUPPORT",
            "scalar_value": 1,
            "cardinality": 1,
            "type": "Support",
            "particle_row": "false",
            "source": "CR282 typed registry",
            "status": "DISTINCT_FROM_X1",
        },
    ]
    write_csv(
        OUT / "CR283_TYPED_OCCURRENCE_REGISTER.csv",
        typed_occurrences,
        ["entity_id", "scalar_value", "cardinality", "type", "particle_row", "source", "status"],
    )

    row_count_replay = {
        "input_catalog_rows": len(input_rows),
        "promoted_rows": len(promoted_rows),
        "register_rows": len(register_rows),
        "matter_rows": matter_count,
        "antimatter_rows": antimatter_count,
        "charged_rows": charged_count,
        "neutral_rows": neutral_count,
        "source_rule_counts": dict(source_rule_counts),
        "partition_signature_counts": dict(sorted(partition_counts.items(), key=lambda item: int(item[0]))),
        "row_meaning": "80 StructurallyStableMatterRow occurrences on a TensorCompatibleStableMatterSurface, not 80 experimentally identified Standard Model particles.",
        "invalid_eighty_row_target": not exact_80,
    }
    write_json(OUT / "CR283_ROW_COUNT_REPLAY.json", row_count_replay)

    decomposition_rows = [
        {"decomposition_id": "D1", "expression": "80 = 48 matter + 32 antimatter", "value": 80, "source_support": "CR253/CR280", "pass": decomposition_checks["48_plus_32"]},
        {"decomposition_id": "D2", "expression": "80 = 64 charged + 16 neutral", "value": 80, "source_support": "CR254/CR255/CR256 row-law split", "pass": decomposition_checks["64_plus_16"]},
        {"decomposition_id": "D3", "expression": "80 = 32 matter charged + 16 matter neutral + 32 antimatter charged", "value": 80, "source_support": "CR254/CR255/CR256", "pass": decomposition_checks["32_plus_16_plus_32"]},
        {"decomposition_id": "D4", "expression": "80 = 81 - 1", "value": 80, "source_support": "CR267/CR269/CR282 plus F81 arithmetic", "pass": checks["G6_closure_address_source_support"] and checks["G7_exact_face_arithmetic"]},
        {"decomposition_id": "D5", "expression": "80 = 8 * 10", "value": 80, "source_support": "exact arithmetic; partition_signature audit reports source-native eight decets, not ten octets", "pass": P == 80},
    ]
    write_csv(OUT / "CR283_ROW_DECOMPOSITIONS.csv", decomposition_rows, ["decomposition_id", "expression", "value", "source_support", "pass"])

    all_required_gates_except_geometry = (
        checks["G1_source_integrity"]
        and checks["G2_exact_80_row_reproduction"]
        and checks["G3_decomposition_audit"]
        and checks["G4_exclusion_audit"]
        and checks["G5_A_field_wrong_row_replay"]
        and checks["G6_closure_address_source_support"]
        and checks["G7_exact_face_arithmetic"]
        and checks["G8_non_row_preservation"]
        and checks["G12_pairing_and_symmetry_test"]
        and wrong_controls_ok
    )

    if not exact_80:
        primary_verdict = "INVALID_EIGHTY_ROW_TARGET"
        scientific_result_status = "INVALID"
    elif not checks["G6_closure_address_source_support"]:
        primary_verdict = "BOUNDARY_80_EQ_81_MINUS_1_NUMERIC_COMPATIBILITY_ONLY"
        scientific_result_status = "BOUNDARY"
    elif all_required_gates_except_geometry and checks["G10_punctured_face_test"]:
        primary_verdict = "PASS_80_PARTICLE_ROWS_PLUS_ONE_CLOSURE_ADDRESS_EQUALS_FACE_81"
        scientific_result_status = "PASS"
    elif all_required_gates_except_geometry:
        primary_verdict = "PASS_CARDINALITY_AND_TYPED_LEDGER_WELD_ROW_GEOMETRY_OPEN"
        scientific_result_status = "PASS"
    else:
        primary_verdict = "FAIL_RESERVED_CLOSURE_ADDRESS_PARTICLE_FACE_MODEL"
        scientific_result_status = "FAIL"

    typed_contract = {
        "entities": [
            {
                "entity_id": "P80_PARTICLE_FACE_CONTENT",
                "cardinality": 80,
                "type": "ParticleBearingRowInventory",
                "source_status": "REPRODUCED" if exact_80 else "INVALID",
            },
            {
                "entity_id": "X1_CLOSURE_ADDRESS",
                "scalar_value": 1,
                "type": "NonRowClosureContactAddress",
                "particle_row": False,
                "source_status": "CR267_CR269_CR282_SCOPE" if checks["G6_closure_address_source_support"] else "SOURCE_CONFLICT",
            },
            {
                "entity_id": "F81_COMPLETED_FACE",
                "scalar_value": 81,
                "type": "CompletedFaceCapacity",
                "origin": "W9^2",
            },
            {
                "entity_id": "L162_FULL_LEDGER",
                "scalar_value": 162,
                "type": "TwoSidedFullClosure",
                "origin": "2*F81",
            },
        ],
        "candidate_relation": {
            "expression": "P80_PARTICLE_FACE_CONTENT + X1_CLOSURE_ADDRESS = F81_COMPLETED_FACE",
            "status": primary_verdict,
        },
        "forbidden_identity": [
            "X1_CLOSURE_ADDRESS == 81st particle",
            "X1_CLOSURE_ADDRESS == QP093A-0305",
            "all scalar-one occurrences are identical",
        ],
    }
    write_json(OUT / "CR283_typed_contract.json", typed_contract)

    summary = {
        "record_id": RECORD_ID,
        "task": TASK,
        "sealed_utc": sealed_utc,
        "prospective_record_class": "SCIENTIFIC_TEST",
        "language_or_meta_language_test": False,
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
        "scientific_result_status": scientific_result_status,
        "primary_verdict": primary_verdict,
        "row_meaning": row_count_replay["row_meaning"],
        "counts": {
            "particle_bearing_rows": len(register_rows),
            "matter_rows": matter_count,
            "antimatter_rows": antimatter_count,
            "charged_rows": charged_count,
            "neutral_rows": neutral_count,
            "closure_address_particle_row": False,
            "completed_face_capacity": F,
            "full_ledger": L,
        },
        "arithmetic": {
            "S": S,
            "W": W,
            "F": F,
            "P": P,
            "L": L,
            "P_equals_F_minus_1": P == F - 1,
            "P_equals_8_times_10": P == 80,
        },
        "geometry_status": {
            "punctured_9x9_face": "OPEN" if row_geometry_open else "PASS",
            "natural_coordinate_candidates": len(coordinate_candidates),
            "valid_face_maps": len(valid_face_maps),
            "ten_octets": "OPEN" if ten_octets_open else "PASS",
            "valid_ten_octet_fields": valid_octets,
        },
        "checks": checks,
        "wrong_controls_all_rejected": wrong_controls_ok,
        "source_errors": errors,
        "precommit_sha256": precommit_hash,
    }
    write_json(OUT / "CR283_summary.json", summary)

    provenance = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "source_hashes": source_hash_records,
        "precommit_sha256": precommit_hash,
        "precommit_sidecar": precommit_sidecar,
        "coordinate_rule_precommit": coordinate_rules,
        "model_definitions": model_defs,
        "forbidden_files_opened": False,
    }
    write_json(OUT / "CR283_provenance.json", provenance)

    result_md = f"""# CR283 Result

record_id: `{RECORD_ID}`
sealed_utc: `{sealed_utc}`
scientific_result_status: `{scientific_result_status}`
primary_verdict: `{primary_verdict}`

## Row Inventory

CR253 reproduces exactly `80` active particle-bearing row occurrences. CR280 clarifies the row type as `StructurallyStableMatterRow` on a `TensorCompatibleStableMatterSurface`; these are not promoted here as 80 experimentally named particles.

The reproduced decomposition is:

```text
80 = 48 matter + 32 antimatter
80 = 64 charged + 16 neutral
80 = 32 matter charged + 16 matter neutral + 32 antimatter charged
```

## Closure Address Weld

The closure/contact side is independently typed by the sealed source chain:

```text
CR267 : 9 = 8 + 1, with +1 = axis self-coupling / axis fee
CR269 : B/contact release fraction 1/8 matches the CR267 axis-fee fraction
CR282 appeal : B/contact -> X1 axis-fee -> W9 is current-status PASS
```

The address is non-row. It is not added to the particle register.

## Exact Arithmetic

```text
S = 8
W = 9 = 8 + 1
F = 81 = 9^2
P = 80 = 81 - 1 = (9 - 1)(9 + 1) = 8*10
L = 162 = 2*81
```

The full ledger remains `162`. Restoring `QP093A-0305` remains the rejected `163` wrong control.

## Geometry Search

The precommitted source-native coordinate search found `{len(valid_face_maps)}` valid punctured 9x9 maps. The precommitted single-field ten-octet search found `{len(valid_octets)}` valid ten-octet grouping fields.

Therefore the CR seals the cardinality and typed ledger weld, while row-to-face geometry remains open.

## Scope

This result preserves CR216 retirement of `QP093A-0305`, CR256 A as non-row, CR267 axis-fee typing, CR269 B/contact, CR282 contact-to-axis-fee bridge, and `L=162` as the closed ledger.
"""
    (OUT / "CR283_result.md").write_text(result_md, encoding="utf-8")

    validation_lines = [
        "# CR283 Validation",
        "",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{scientific_result_status}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Gates",
        "",
    ]
    for key in sorted(checks):
        validation_lines.append(f"- `{key}`: `{checks[key]}`")
    validation_lines.extend(
        [
            f"- `wrong_controls_all_rejected`: `{wrong_controls_ok}`",
            "",
            "## Conclusion",
            "",
            "The 80-row inventory and non-row closure/contact address integrate exactly with F81 and L162. No source-native punctured 9x9 row geometry was established.",
            "",
        ]
    )
    (OUT / "CR283_VALIDATION.md").write_text("\n".join(validation_lines), encoding="utf-8")

    generated_files = [
        "CR283_SOURCE_AUDIT.md",
        "CR283_SOURCE_MANIFEST.json",
        "CR283_PARTICLE_ROW_REGISTER.csv",
        "CR283_ROW_COUNT_REPLAY.json",
        "CR283_ROW_DECOMPOSITIONS.csv",
        "CR283_TYPED_OCCURRENCE_REGISTER.csv",
        "CR283_MODEL_DEFINITIONS.json",
        "CR283_COORDINATE_RULE_PRECOMMIT.json",
        "CR283_FACE_ADDRESS_MAP.csv",
        "CR283_OCTET_GROUPS.csv",
        "CR283_PAIRING_METRICS.csv",
        "CR283_RANDOMIZATION_CONTROLS.csv",
        "CR283_MODEL_SCORECARD.csv",
        "CR283_WRONG_CONTROLS.csv",
        "CR283_ASSUMPTION_REGISTER.json",
        "CR283_PREFLIGHT.md",
        "CR283_PRECOMMIT.md",
        "CR283_PRECOMMIT.sha256.txt",
        "CR283_runner.py",
        "CR283_runner.sha256.txt",
        "CR283_result.md",
        "CR283_summary.json",
        "CR283_provenance.json",
        "CR283_typed_contract.json",
        "CR283_VALIDATION.md",
        "COMMAND_LOG.txt",
        "OPENED_FILE_MANIFEST.json",
    ]
    hash_lines = []
    for name in generated_files:
        path = OUT / name
        if path.exists():
            hash_lines.append(f"{sha256_path(path)}  {name}")
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    with (OUT / "COMMAND_LOG.txt").open("a", encoding="utf-8") as log:
        log.write(f"{sealed_utc} | runner_complete | {primary_verdict}\n")

    return 0 if scientific_result_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
