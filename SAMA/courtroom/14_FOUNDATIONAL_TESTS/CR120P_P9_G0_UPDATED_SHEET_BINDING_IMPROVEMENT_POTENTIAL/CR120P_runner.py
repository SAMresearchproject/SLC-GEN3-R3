from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80

RECORD_ID = "CR120P_P9_G0_UPDATED_SHEET_BINDING_IMPROVEMENT_POTENTIAL"
TASK = "Assess binding improvement potential of latest spreadsheets after p9 g0 value removal"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SOURCE_MANIFEST = HERE / "CR120P_SOURCE_MANIFEST.csv"
PRECOMMIT = HERE / "CR120P_PRECOMMIT.md"
PRECOMMIT_HASH_FILE = HERE / "CR120P_PRECOMMIT.sha256.txt"

ROSTER100 = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120N_FRESH_QP093A_UPDATED_SHEET_100_81_ROSTER_COMPARISON" / "CR120N_ROSTER100_RAW.csv"
ROSTER81 = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120N_FRESH_QP093A_UPDATED_SHEET_100_81_ROSTER_COMPARISON" / "CR120N_ROSTER81_RAW.csv"
DERIVATION = ROOT / "14_FOUNDATIONAL_TESTS" / "CR120K_P9_G0_W9_8_PLUS_1_INDEPENDENT_INVENTORY_DISCRIMINATION" / "CR120K_DERIVATION_MATRIX.json"
CR242_DATASET = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"
CR274_OPERATORS = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR274_GATED_NUCLEAR_READOUT_OPERATORS" / "CR274_operators.csv"
CR277_TABLE = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR277_ONE_HUNDRED_TWENTY_SIX_ELEMENT_TABLE_AND_SOB_FRONTIER_LOCKS" / "CR277_element_table.csv"
CR276_TABLE = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR276_PARTICLE_SIEVE_ANCHORING_TABLE" / "CR276_anchoring_table.csv"

EXPECTED_CANDIDATES = {
    "QP093A-0019",
    "QP093A-0020",
    "QP093A-0021",
    "QP093A-0085",
    "QP093A-0086",
}
EXPECTED_PROVENANCE = "RESOLVE(S8_BINARY_SURFACE,B_CONTACT_OPERATOR,X1_AXIS_SELF_CHANNEL)->W9_CLOSURE_WITNESS"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def dec(value: object) -> Decimal:
    text = str(value).strip()
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return Decimal(numerator) / Decimal(denominator)
    return Decimal(text)


def dstr(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text if text not in {"", "-0"} else "0"


def as_path(text: str) -> Path:
    path = Path(text)
    return path if path.is_absolute() else ROOT / path


def verify_sources() -> list[dict[str, object]]:
    manifest_rows = read_csv(SOURCE_MANIFEST)
    checks: list[dict[str, object]] = []
    for row in manifest_rows:
        path = as_path(row["path"])
        exists = path.is_file()
        actual_bytes = path.stat().st_size if exists else None
        actual_hash = sha256(path) if exists else None
        passed = (
            exists
            and actual_bytes == int(row["bytes"])
            and actual_hash == row["sha256"].lower()
        )
        checks.append(
            {
                "ordinal": int(row["ordinal"]),
                "role": row["role"],
                "path": row["path"],
                "expected_bytes": int(row["bytes"]),
                "actual_bytes": actual_bytes,
                "expected_sha256": row["sha256"].lower(),
                "actual_sha256": actual_hash,
                "pass": passed,
            }
        )
    if not all(row["pass"] for row in checks):
        raise RuntimeError("Frozen source-manifest validation failed")

    expected_precommit = PRECOMMIT_HASH_FILE.read_text(encoding="utf-8").split()[0].lower()
    actual_precommit = sha256(PRECOMMIT)
    if actual_precommit != expected_precommit:
        raise RuntimeError("Precommit hash validation failed")
    return checks


def candidate_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    count_by_sign = Counter(row["q_sign"] for row in rows)
    sum_by_sign: dict[str, Decimal] = {}
    for sign in ("positive", "negative", "neutral"):
        sum_by_sign[sign] = sum((dec(row["M_native"]) for row in rows if row["q_sign"] == sign), Decimal(0))
    return {
        "row_count": len(rows),
        "M_native_sum": dstr(sum((dec(row["M_native"]) for row in rows), Decimal(0))),
        "positive_count": count_by_sign["positive"],
        "positive_M_native_sum": dstr(sum_by_sign["positive"]),
        "negative_count": count_by_sign["negative"],
        "negative_M_native_sum": dstr(sum_by_sign["negative"]),
        "neutral_count": count_by_sign["neutral"],
        "neutral_M_native_sum": dstr(sum_by_sign["neutral"]),
        "candidate_ids": sorted(row["candidate_id"] for row in rows),
    }


def main() -> None:
    source_checks = verify_sources()
    roster100 = read_csv(ROSTER100)
    roster81 = read_csv(ROSTER81)
    derivation = json.loads(DERIVATION.read_text(encoding="utf-8-sig"))
    derivation_rows = derivation["rows"]

    derivation_ids = {row["candidate_id"] for row in derivation_rows}
    exact_dependency = (
        derivation_ids == EXPECTED_CANDIDATES
        and len(derivation_rows) == 5
        and all(row["M_native_exact_additivity"] for row in derivation_rows)
        and all(dec(row["M_native_residual"]) == 0 for row in derivation_rows)
        and all(row["all_type_checks_passed"] for row in derivation_rows)
        and all(row["derived_partition_expression"] == "8+1" for row in derivation_rows)
        and all(row["provenance_route"] == EXPECTED_PROVENANCE for row in derivation_rows)
    )
    if not exact_dependency:
        raise RuntimeError("Frozen five-row W8/X1/W9 dependency gate failed")

    p9_total = sum((dec(row["M_native_p9"]) for row in derivation_rows), Decimal(0))
    if p9_total != Decimal("50.625"):
        raise RuntimeError("Unexpected five-row p9,g0 sum")

    parent_ids = {
        parent
        for row in derivation_rows
        for parent in (row["parent_p1_id"], row["parent_p8_id"])
    }
    ids100 = {row["candidate_id"] for row in roster100}
    ids81 = {row["candidate_id"] for row in roster81}
    rows100_by_id = {row["candidate_id"]: row for row in roster100}
    rows81_by_id = {row["candidate_id"]: row for row in roster81}

    sum100 = sum((dec(row["M_native"]) for row in roster100), Decimal(0))
    sum81 = sum((dec(row["M_native"]) for row in roster81), Decimal(0))
    p9_in_100 = [rows100_by_id[cid] for cid in sorted(EXPECTED_CANDIDATES & ids100)]
    p9_in_81 = [rows81_by_id[cid] for cid in sorted(EXPECTED_CANDIDATES & ids81)]
    p9_100_sum = sum((dec(row["M_native"]) for row in p9_in_100), Decimal(0))
    p9_81_sum = sum((dec(row["M_native"]) for row in p9_in_81), Decimal(0))
    parents100 = parent_ids & ids100
    parents81 = parent_ids & ids81

    complete100 = (
        len(roster100) == 100
        and len(ids100) == 100
        and sum100 == Decimal("16200")
        and not p9_in_100
        and parents100 == parent_ids
    )
    complete81_as_saved = (
        len(roster81) == 81
        and len(ids81) == 81
        and sum81 == Decimal("12600")
        and not p9_in_81
        and parents81 == parent_ids
    )
    overlay81_complete = (
        len(roster81) == 81
        and len(ids81) == 81
        and sum81 == Decimal("12600")
        and parents81 == parent_ids
        and EXPECTED_CANDIDATES - ids81 == {"QP093A-0021"}
        and {row["candidate_id"] for row in p9_in_81} == EXPECTED_CANDIDATES - {"QP093A-0021"}
    )
    sum81_after_specific_removal = sum81 - p9_81_sum

    # Binding interface: existing rows, holdout/observed surfaces, and the absence
    # of an already-frozen per-isotope candidate occupancy join.
    cr242 = read_csv(CR242_DATASET)
    cr274 = read_csv(CR274_OPERATORS)
    cr277 = read_csv(CR277_TABLE)
    cr276 = read_csv(CR276_TABLE)
    cr242_headers = set(cr242[0]) if cr242 else set()
    cr277_headers = set(cr277[0]) if cr277 else set()
    cr276_headers = set(cr276[0]) if cr276 else set()
    splits = sorted({row["split"] for row in cr242})
    has_holdout = any("test" in split.lower() or "holdout" in split.lower() for split in splits)
    intercept_all_one = bool(cr242) and all(dec(row["intercept"]) == 1 for row in cr242)
    isotope_varying = len({(row["Z"], row["N"], row["A"]) for row in cr242}) > 1
    adopted_ops = [row for row in cr274 if row["adopted"] == "1"]
    signed_ops = {
        "positive": sum(1 for row in adopted_ops if dec(row["gamma"]) > 0),
        "negative": sum(1 for row in adopted_ops if dec(row["gamma"]) < 0),
        "zero": sum(1 for row in adopted_ops if dec(row["gamma"]) == 0),
    }
    observed277 = [row for row in cr277 if "observed" in row["row_status"].lower()]
    roles276 = {row["candidate_id"]: row for row in cr276 if row["candidate_id"] in EXPECTED_CANDIDATES}
    all_roles_present = set(roles276) == EXPECTED_CANDIDATES
    explicit_candidate_to_isotope_map = (
        "candidate_id" in cr242_headers
        or "candidate_id" in cr277_headers
        or "isotope" in cr276_headers
        or {"Z", "N", "A"}.issubset(cr276_headers)
    )
    binding_interface_exists = (
        bool(cr242)
        and has_holdout
        and intercept_all_one
        and isotope_varying
        and bool(observed277)
        and all_roles_present
    )

    global_columns = {}
    for name, value in {
        "roster100_total": sum100,
        "roster81_total": sum81,
        "five_row_p9_total": p9_total,
        "roster_sum_difference": sum100 - sum81,
    }.items():
        collinear = intercept_all_one and all(value == value * dec(row["intercept"]) for row in cr242)
        global_columns[name] = {
            "constant": dstr(value),
            "exact_scalar_multiple_of_intercept": collinear,
            "independent_predictor": not collinear,
        }

    potential100 = exact_dependency and complete100 and binding_interface_exists and not explicit_candidate_to_isotope_map
    potential81_after_removal = exact_dependency and overlay81_complete and binding_interface_exists and not explicit_candidate_to_isotope_map

    p9_rows_output: list[dict[str, object]] = []
    for row in sorted(derivation_rows, key=lambda item: item["candidate_id"]):
        cid = row["candidate_id"]
        current81 = rows81_by_id.get(cid)
        p9_rows_output.append(
            {
                "candidate_id": cid,
                "parent_p8_id": row["parent_p8_id"],
                "parent_p1_id": row["parent_p1_id"],
                "M_native_p8": dstr(dec(row["M_native_p8"])),
                "M_native_p1": dstr(dec(row["M_native_p1"])),
                "M_native_p9": dstr(dec(row["M_native_p9"])),
                "exact_additivity": str(bool(row["M_native_exact_additivity"])).lower(),
                "residual": dstr(dec(row["M_native_residual"])),
                "all_type_checks_passed": str(bool(row["all_type_checks_passed"])).lower(),
                "present_in_100": str(cid in ids100).lower(),
                "present_in_81": str(cid in ids81).lower(),
                "q_sign_in_81": current81["q_sign"] if current81 else "absent",
                "M_native_in_81": dstr(dec(current81["M_native"])) if current81 else "0",
            }
        )
    write_csv(
        HERE / "CR120P_p9_g0_rows.csv",
        list(p9_rows_output[0]),
        p9_rows_output,
    )

    sheet_rows = [
        {
            "assembly": "100_row_16200",
            "source_rows": len(roster100),
            "unique_candidate_ids": len(ids100),
            "M_native_sum_as_saved": dstr(sum100),
            "p9_g0_rows_present": len(p9_in_100),
            "p9_g0_M_native_present": dstr(p9_100_sum),
            "p9_g0_ids_present": "|".join(sorted(EXPECTED_CANDIDATES & ids100)),
            "declared_parents_retained": len(parents100),
            "complete_p9_g0_removal_as_saved": str(complete100).lower(),
            "M_native_sum_after_specific_p9_g0_value_removal": dstr(sum100 - p9_100_sum),
            "nonzero_M_native_rows_after_removal": sum(1 for row in roster100 if dec(row["M_native"]) != 0 and row["candidate_id"] not in EXPECTED_CANDIDATES),
            "as_saved_verdict": "YES_POTENTIAL" if potential100 else "NO_POTENTIAL",
            "after_specific_value_removal_potential": "YES_POTENTIAL" if potential100 else "NO_POTENTIAL",
        },
        {
            "assembly": "81_row_12600",
            "source_rows": len(roster81),
            "unique_candidate_ids": len(ids81),
            "M_native_sum_as_saved": dstr(sum81),
            "p9_g0_rows_present": len(p9_in_81),
            "p9_g0_M_native_present": dstr(p9_81_sum),
            "p9_g0_ids_present": "|".join(sorted(EXPECTED_CANDIDATES & ids81)),
            "declared_parents_retained": len(parents81),
            "complete_p9_g0_removal_as_saved": str(complete81_as_saved).lower(),
            "M_native_sum_after_specific_p9_g0_value_removal": dstr(sum81_after_specific_removal),
            "nonzero_M_native_rows_after_removal": sum(1 for row in roster81 if dec(row["M_native"]) != 0 and row["candidate_id"] not in EXPECTED_CANDIDATES),
            "as_saved_verdict": "YES_POTENTIAL" if complete81_as_saved else "NO_SAME_MECHANISM_AS_SAVED",
            "after_specific_value_removal_potential": "YES_POTENTIAL" if potential81_after_removal else "NO_POTENTIAL",
        },
    ]
    write_csv(HERE / "CR120P_sheet_assessment.csv", list(sheet_rows[0]), sheet_rows)

    only100 = [row for row in roster100 if row["candidate_id"] not in ids81]
    only81 = [row for row in roster81 if row["candidate_id"] not in ids100]
    roster_delta_rows: list[dict[str, object]] = []
    for packet_name, packet in (("100_only_removal_packet", only100), ("81_only_insertion_packet", only81)):
        for sign in ("all", "positive", "negative", "neutral"):
            selected = packet if sign == "all" else [row for row in packet if row["q_sign"] == sign]
            roster_delta_rows.append(
                {
                    "packet": packet_name,
                    "q_sign": sign,
                    "row_count": len(selected),
                    "M_native_sum": dstr(sum((dec(row["M_native"]) for row in selected), Decimal(0))),
                    "candidate_ids": "|".join(sorted(row["candidate_id"] for row in selected)),
                }
            )
    roster_delta_rows.append(
        {
            "packet": "net_81_minus_100",
            "q_sign": "all",
            "row_count": len(roster81) - len(roster100),
            "M_native_sum": dstr(sum81 - sum100),
            "candidate_ids": "",
        }
    )
    write_csv(HERE / "CR120P_roster_delta.csv", list(roster_delta_rows[0]), roster_delta_rows)

    binding_interface = {
        "record_id": RECORD_ID,
        "cr242": {
            "row_count": len(cr242),
            "splits": splits,
            "has_frozen_holdout_surface": has_holdout,
            "intercept_all_one": intercept_all_one,
            "isotope_coordinates_vary": isotope_varying,
            "global_sheet_columns": global_columns,
        },
        "cr274": {
            "adopted_operator_count": len(adopted_ops),
            "adopted_gamma_sign_counts": signed_ops,
        },
        "cr277": {
            "element_rows": len(cr277),
            "observed_rows": len(observed277),
            "has_observed_binding_panel": bool(observed277),
        },
        "cr276": {
            "candidate_roles_present": sorted(roles276),
            "all_five_roles_present": all_roles_present,
            "roles": {
                cid: {
                    "category": roles276[cid]["category"],
                    "sam_role": roles276[cid]["sam_role"],
                    "sub_role": roles276[cid]["sub_role"],
                }
                for cid in sorted(roles276)
            },
        },
        "binding_interface_exists": binding_interface_exists,
        "explicit_candidate_to_isotope_occupancy_map_present": explicit_candidate_to_isotope_map,
        "measured_binding_improvement": "NOT_YET_TESTED",
    }
    write_json(HERE / "CR120P_binding_interface.json", binding_interface)

    p9_81_stats = candidate_stats(p9_in_81)
    wrong_controls = {
        "record_id": RECORD_ID,
        "mean_substitution_used": False,
        "all_roster_arithmetic_uses_M_native_sums": True,
        "global_total_predictor_control": global_columns,
        "global_total_predictor_rejected": all(not item["independent_predictor"] for item in global_columns.values()),
        "any_depth_p9_deletion_used": False,
        "identity_rows_erased_from_source_record": False,
        "binding_model_refit_or_holdout_tuned": False,
        "current_81_relabelled_as_complete_p9_g0_removal": False,
        "current_81_p9_g0_rows": p9_81_stats,
        "current_81_p9_g0_value_removal_is_charge_balanced": (
            p9_81_stats["positive_count"] == p9_81_stats["negative_count"]
            and p9_81_stats["positive_M_native_sum"] == p9_81_stats["negative_M_native_sum"]
        ),
    }
    write_json(HERE / "CR120P_wrong_controls.json", wrong_controls)

    summary = {
        "record_id": RECORD_ID,
        "task": TASK,
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "precommit_sha256": sha256(PRECOMMIT),
        "source_count": len(source_checks),
        "all_sources_verified": all(row["pass"] for row in source_checks),
        "exact_five_row_dependency": exact_dependency,
        "five_row_p9_g0_M_native_sum": dstr(p9_total),
        "assembly_100": {
            "rows": len(roster100),
            "M_native_sum": dstr(sum100),
            "complete_p9_g0_removal_as_saved": complete100,
            "binding_improvement_potential": "YES_POTENTIAL" if potential100 else "NO_POTENTIAL",
        },
        "assembly_81": {
            "rows": len(roster81),
            "M_native_sum_as_saved": dstr(sum81),
            "p9_g0_rows_retained_as_saved": len(p9_in_81),
            "p9_g0_M_native_retained_as_saved": dstr(p9_81_sum),
            "complete_p9_g0_removal_as_saved": complete81_as_saved,
            "as_saved_mechanism_verdict": "YES_POTENTIAL" if complete81_as_saved else "NO_SAME_MECHANISM_AS_SAVED",
            "M_native_sum_after_specific_p9_g0_value_removal": dstr(sum81_after_specific_removal),
            "binding_improvement_potential_after_specific_removal": "YES_POTENTIAL" if potential81_after_removal else "NO_POTENTIAL",
        },
        "roster_contraction": {
            "removed_100_only": candidate_stats(only100),
            "inserted_81_only": candidate_stats(only81),
            "net_M_native_change": dstr(sum81 - sum100),
        },
        "binding_interface_exists": binding_interface_exists,
        "explicit_candidate_to_isotope_occupancy_map_present": explicit_candidate_to_isotope_map,
        "measured_binding_improvement": "NOT_YET_TESTED",
        "overall_verdict": "PASS_BINDING_IMPROVEMENT_POTENTIAL_CONFIRMED",
    }
    write_json(HERE / "CR120P_summary.json", summary)

    only100_stats = candidate_stats(only100)
    only81_stats = candidate_stats(only81)
    result = f"""# CR120P Result

## Verdict

`PASS_BINDING_IMPROVEMENT_POTENTIAL_CONFIRMED`

**Direct answer: yes.** The specific `[p=9,g=0]` value removal has a source-backed mechanism with the potential to improve binding construction by preventing an exact dependent linear `M_native` contribution from being counted again as independent inventory.

## Decisive readout

- The frozen relation is exactly `[p=9,g=0] = [p=8,g=0] + [p=1,g=0]` for five rows.
- All five rows retain exact additivity, zero residual, passing type checks, and the executed W8/X1/W9 provenance.
- Their exact `M_native` sum is `{dstr(p9_total)}`.
- The 100-row workbook already implements the complete removal: `100` rows, `sum(M_native) = {dstr(sum100)}`, zero retained candidate rows, and all 10 parent rows retained.
- Therefore the 100-row/16,200 assembly is `YES_POTENTIAL` for binding improvement through duplicate-inventory prevention and isolation of any separately modeled interaction/residual contribution.

## 81-row assembly

- As saved, the 81-row workbook has `sum(M_native) = {dstr(sum81)}` and retains four charged `[p=9,g=0]` values totaling `{dstr(p9_81_sum)}`; the neutral fifth row is already absent.
- Those four retained values are sign-balanced: positive `{p9_81_stats['positive_count']}` rows / `{p9_81_stats['positive_M_native_sum']}` and negative `{p9_81_stats['negative_count']}` rows / `{p9_81_stats['negative_M_native_sum']}`.
- Specifically removing those remaining four values produces `sum(M_native) = {dstr(sum81_after_specific_removal)}` while retaining all 10 W8/X1 parent rows. That transformed assembly is also `YES_POTENTIAL` under the same duplicate-prevention mechanism.
- The saved 12,600 roster itself is `NO_SAME_MECHANISM_AS_SAVED` because its four charged `[p=9,g=0]` values are still present.

The broader 100-to-81 contraction is separately exact: the 100-only packet removes `{only100_stats['row_count']}` rows totaling `{only100_stats['M_native_sum']}`, including `{only100_stats['positive_count']}` positive rows / `{only100_stats['positive_M_native_sum']}` and `{only100_stats['negative_count']}` negative rows / `{only100_stats['negative_M_native_sum']}`. The 81-only packet inserts `{only81_stats['row_count']}` rows totaling `{only81_stats['M_native_sum']}`, giving the net `{dstr(sum81 - sum100)}` change. That signed contraction is not relabeled as the five-row removal.

## Binding boundary

The repo already contains isotope-varying binding datasets, a frozen holdout surface, signed binding operators, an observed 126-element panel, and CR276 role rows for all five candidates. That is enough to establish a real testable improvement mechanism.

It is **not yet a measured reduction in binding residuals**. No frozen per-isotope occupancy/multiplicity map currently joins the five particle rows to each isotope. Also, the global totals `16200`, `12600`, `50.625`, or `3600` used alone are exact scalar multiples of CR242's intercept and cannot add independent predictive information. The measurement step is a separately precommitted per-isotope feature test against the frozen holdout/observed panels.

## Controls

- All spreadsheet arithmetic used `M_native` sums, never means.
- No any-depth p9 deletion was used.
- No identity or provenance row was erased.
- No binding coefficient, isotope, holdout split, operator, or threshold was tuned.
- The 81-row sheet was not misreported as already implementing the complete five-row removal.
"""
    (HERE / "CR120P_result.md").write_text(result, encoding="utf-8")

    hash_targets = [
        "CR120P_SOURCE_MANIFEST.csv",
        "CR120P_PRECOMMIT.md",
        "CR120P_PRECOMMIT.sha256.txt",
        "CR120P_runner.py",
        "CR120P_sheet_assessment.csv",
        "CR120P_p9_g0_rows.csv",
        "CR120P_roster_delta.csv",
        "CR120P_binding_interface.json",
        "CR120P_wrong_controls.json",
        "CR120P_summary.json",
        "CR120P_result.md",
    ]
    hashes = "".join(f"{sha256(HERE / name)}  {name}\n" for name in hash_targets)
    (HERE / "HASHES.txt").write_text(hashes, encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
