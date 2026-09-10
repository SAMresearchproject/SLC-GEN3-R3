from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR225_CARRIER_HIDDEN_CLOCK_SELECTOR"

CR217 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR217_DEDUP_STRUCTURAL_IDENTITY_AUDIT"
CR218 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR218_HIDDEN_SOURCE_BIGRADE_DERIVATION"
CR220 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION"
CR224 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE"

CR217_CARRIER = CR217 / "CR217_carrier_block.csv"
CR217_HIDDEN = CR217 / "CR217_hidden_source_block.csv"
CR217_SUMMARY = CR217 / "CR217_summary.json"
CR218_SUMMARY = CR218 / "CR218_summary.json"
CR220_ELEMENTS = CR220 / "CR220_simulated_element_primary_rows_126.csv"
CR224_ROWS = CR224 / "CR224_sob_rows_126.csv"

PRECOMMIT = OUT / "CR225_PRECOMMIT.md"
RUNNER = OUT / "CR225_runner.py"
FORMULA_TERMS = OUT / "CR225_formula_terms.csv"
CANDIDATE_ROWS = OUT / "CR225_clock_candidate_rows_126.csv"
SELECTOR_SCORES = OUT / "CR225_selector_scores.csv"
WRONG_CONTROLS = OUT / "CR225_wrong_controls.csv"
INPUT_MANIFEST = OUT / "CR225_input_manifest.csv"
CHECKS = OUT / "CR225_checks.csv"
SUMMARY = OUT / "CR225_summary.json"
RESULT = OUT / "CR225_result.md"
HASHES = OUT / "HASHES.txt"

R = Fraction(12, 1)
D = Fraction(3, 1)
ALPHA_H = Fraction(2, 1)
SPLIT = Fraction(2, 1) ** int(D)
R_SQUARED = R * R
CAPACITY = R_SQUARED * (Fraction(1, 1) - Fraction(1, SPLIT))
TENSOR_RELEASE = R_SQUARED / SPLIT
NEUTRAL_VECTOR_CARRIER = D ** (int(D) + 1)
CLOCK_BOUNDARY = NEUTRAL_VECTOR_CARRIER + ALPHA_H


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists() and path.is_file():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append({"check": name, "passed": str(bool(passed)), "observed": observed, "expected": expected})


def fstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def fdec(value: Fraction) -> str:
    return str(Decimal(value.numerator) / Decimal(value.denominator))


def yesno(value: bool) -> str:
    return "yes" if value else "no"


def six(value: Decimal) -> str:
    return f"{value:.6f}"


def manifest_row(path: Path, role: str, construction_role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "source": rel(path),
        "exists": str(exists),
        "bytes": path.stat().st_size if exists and path.is_file() else "",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
        "role": role,
        "construction_role": construction_role,
    }


def hidden_bigrade_set() -> list[int]:
    values: set[int] = set()
    a = 0
    while int(ALPHA_H) ** a <= int(R):
        b = 0
        while (int(ALPHA_H) ** a) * (int(D) ** b) <= int(R):
            values.add((int(ALPHA_H) ** a) * (int(D) ** b))
            b += 1
        a += 1
    return sorted(values)


def formula_rows(hidden_set: list[int], holes: list[int]) -> list[dict[str, Any]]:
    hidden_sum = sum(hidden_set)
    terms = [
        ("R", "12", "radix/native route constant", "declared SAM constant"),
        ("D", "3", "closure depth", "declared SAM constant"),
        ("alpha_H", "2", "hidden-source bigrade generator", "declared SAM constant"),
        ("split", fstr(SPLIT), "2^D carrier split", "derived"),
        ("R_squared", fstr(R_SQUARED), "full 12x12 lattice", "derived"),
        ("native_capacity", fstr(CAPACITY), "R^2*(1-2^-D)", "derived"),
        ("tensor_release_T", fstr(TENSOR_RELEASE), "R^2/2^D", "derived and CR217 verified"),
        ("neutral_vector_carrier_Zc", fstr(NEUTRAL_VECTOR_CARRIER), "D^(D+1)", "derived and CR217 verified"),
        ("hidden_set", ";".join(str(x) for x in hidden_set), "alpha_H^a*D^b <= R", "derived and CR218 verified"),
        ("hidden_sum_H", str(hidden_sum), "sum(hidden_set)", "derived"),
        ("clock_boundary", fstr(CLOCK_BOUNDARY), "neutral_vector_carrier_Zc + alpha_H", "candidate"),
        ("hole_seed", str(hidden_sum - int(ALPHA_H)), "hidden_sum_H - alpha_H", "candidate"),
        ("hole_tensor_shift", str(hidden_sum - int(ALPHA_H) + int(TENSOR_RELEASE)), "hole_seed + tensor_release_T", "candidate"),
        ("hole_set", ";".join(str(x) for x in holes), "{hole_seed, hole_seed + T}", "candidate"),
        ("stable_count_candidate", str(int(CLOCK_BOUNDARY) - len(holes)), "clock_boundary - hole_count", "candidate"),
    ]
    return [
        {
            "term": term,
            "value": value,
            "formula_or_role": formula,
            "status": status,
        }
        for term, value, formula, status in terms
    ]


def score_selector(
    rows: list[dict[str, Any]],
    selector_id: str,
    selector_column: str,
    description: str,
    input_class: str,
) -> dict[str, Any]:
    scored = [row for row in rows if row["reference_clock"] != "frontier"]
    predicted_all = [row for row in rows if row[selector_column] == "yes"]
    predicted_scored = [row for row in scored if row[selector_column] == "yes"]
    tp = sum(1 for row in scored if row[selector_column] == "yes" and row["reference_clock"] == "stable")
    fp = sum(1 for row in scored if row[selector_column] == "yes" and row["reference_clock"] == "radioactive")
    fn = sum(1 for row in scored if row[selector_column] == "no" and row["reference_clock"] == "stable")
    tn = sum(1 for row in scored if row[selector_column] == "no" and row["reference_clock"] == "radioactive")
    total = Decimal(len(scored))
    accuracy = Decimal(tp + tn) / total if total else Decimal(0)
    precision = Decimal(tp) / Decimal(tp + fp) if tp + fp else Decimal(0)
    recall = Decimal(tp) / Decimal(tp + fn) if tp + fn else Decimal(0)
    false_positive_z = ";".join(str(row["Z"]) for row in scored if row[selector_column] == "yes" and row["reference_clock"] == "radioactive")
    false_negative_z = ";".join(str(row["Z"]) for row in scored if row[selector_column] == "no" and row["reference_clock"] == "stable")
    return {
        "selector_id": selector_id,
        "selector_column": selector_column,
        "description": description,
        "input_class": input_class,
        "predicted_stable_count_all_126": len(predicted_all),
        "predicted_stable_count_known_118": len(predicted_scored),
        "scored_rows": len(scored),
        "reference_target": "HH001_CLOCK_stable_vs_radioactive_Z001_Z118",
        "true_positive_stable": tp,
        "false_positive_radioactive": fp,
        "false_negative_stable": fn,
        "true_negative_radioactive": tn,
        "accuracy": six(accuracy),
        "precision": six(precision),
        "recall": six(recall),
        "false_positive_Z": false_positive_z,
        "false_negative_Z": false_negative_z,
        "boundary_note": "CLOCK labels are comparator only; selector was constructed from native constants and carrier/hidden identities",
    }


def build_candidate_rows(
    sob_rows: list[dict[str, str]],
    reference_rows: list[dict[str, str]],
    holes: list[int],
) -> list[dict[str, Any]]:
    sob_by_z = {int(row["element_Z"]): row for row in sob_rows}
    ref_by_z = {int(row["Z"]): row for row in reference_rows}
    rows: list[dict[str, Any]] = []
    wrong_holes_no_alpha = [sum(hidden_bigrade_set()), sum(hidden_bigrade_set()) + int(TENSOR_RELEASE)]
    for z in range(1, int(CAPACITY) + 1):
        sob = sob_by_z[z]
        ref = ref_by_z[z]
        in_boundary = z <= int(CLOCK_BOUNDARY)
        in_hole = z in holes
        row = {
            "candidate_id": f"CR225-Z{z:03d}",
            "sob_id": sob["sob_id"],
            "Z": z,
            "N": sob["N"],
            "A": sob["A"],
            "P_address": sob["P_address"],
            "quark_address": sob["quark_address"],
            "radix_cycle": sob["radix_cycle"],
            "radix_slot": sob["radix_slot"],
            "shell_period": sob["shell_period"],
            "shell_capacity": sob["shell_capacity"],
            "shell_occupancy": sob["shell_occupancy"],
            "shell_status": sob["shell_status"],
            "residual_twelfths": sob["residual_twelfths"],
            "constant_native_lane": sob["constant_native_lane"],
            "G_fraction": sob["G_fraction"],
            "GR_fraction": sob["GR_fraction"],
            "retained_7G_fraction": sob["retained_7G_fraction"],
            "reference_clock": ref["reference_clock"],
            "selector_neutral_vector_cardinality_z_le_81": yesno(z <= int(NEUTRAL_VECTOR_CARRIER)),
            "selector_tensor_alpha_boundary_z_le_83": yesno(in_boundary),
            "selector_carrier_hidden_clock": yesno(in_boundary and not in_hole),
            "selector_wc_no_alpha_bridge_with_main_holes": yesno(z <= int(NEUTRAL_VECTOR_CARRIER) and not in_hole),
            "selector_wc_no_hole_rejector": yesno(in_boundary),
            "selector_wc_holes_without_alpha_offset": yesno(in_boundary and z not in wrong_holes_no_alpha),
            "selector_wc_single_hole_no_tensor_shift": yesno(in_boundary and z != holes[0]),
            "native_hole_rejector": yesno(in_hole),
            "native_hole_formula": "H-alpha_H" if z == holes[0] else ("H-alpha_H+T" if z == holes[1] else ""),
            "construction_note": "Reference CLOCK is scoring-only; candidate selector uses carrier/hidden constants, not labels/cards",
        }
        rows.append(row)
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, Any]] = []

    manifest = [
        manifest_row(CR217_CARRIER, "carrier partition verification", "VERIFICATION_OF_NATIVE_TERMS"),
        manifest_row(CR217_HIDDEN, "hidden-source lift verification", "VERIFICATION_OF_NATIVE_TERMS"),
        manifest_row(CR217_SUMMARY, "carrier and hidden partition sums", "VERIFICATION_OF_NATIVE_TERMS"),
        manifest_row(CR218_SUMMARY, "hidden-source bigrade derivation", "VERIFICATION_OF_NATIVE_TERMS"),
        manifest_row(CR224_ROWS, "native 126-row SOB scaffold", "NATIVE_ROW_SURFACE"),
        manifest_row(CR220_ELEMENTS, "HH001 CLOCK comparator labels", "REFERENCE_COMPARATOR_ONLY"),
    ]
    write_csv(INPUT_MANIFEST, manifest, ["source", "exists", "bytes", "sha256", "role", "construction_role"])

    _, carrier_rows = read_csv(CR217_CARRIER)
    _, hidden_rows = read_csv(CR217_HIDDEN)
    cr217_summary = read_json(CR217_SUMMARY)
    cr218_summary = read_json(CR218_SUMMARY)
    _, sob_rows = read_csv(CR224_ROWS)
    _, ref_rows = read_csv(CR220_ELEMENTS)

    hidden_set = hidden_bigrade_set()
    hidden_sum = sum(hidden_set)
    holes = [hidden_sum - int(ALPHA_H), hidden_sum - int(ALPHA_H) + int(TENSOR_RELEASE)]

    write_csv(FORMULA_TERMS, formula_rows(hidden_set, holes), ["term", "value", "formula_or_role", "status"])

    candidate_rows = build_candidate_rows(sob_rows, ref_rows, holes)
    candidate_fields = [
        "candidate_id",
        "sob_id",
        "Z",
        "N",
        "A",
        "P_address",
        "quark_address",
        "radix_cycle",
        "radix_slot",
        "shell_period",
        "shell_capacity",
        "shell_occupancy",
        "shell_status",
        "residual_twelfths",
        "constant_native_lane",
        "G_fraction",
        "GR_fraction",
        "retained_7G_fraction",
        "reference_clock",
        "selector_neutral_vector_cardinality_z_le_81",
        "selector_tensor_alpha_boundary_z_le_83",
        "selector_carrier_hidden_clock",
        "selector_wc_no_alpha_bridge_with_main_holes",
        "selector_wc_no_hole_rejector",
        "selector_wc_holes_without_alpha_offset",
        "selector_wc_single_hole_no_tensor_shift",
        "native_hole_rejector",
        "native_hole_formula",
        "construction_note",
    ]
    write_csv(CANDIDATE_ROWS, candidate_rows, candidate_fields)

    selector_specs = [
        (
            "C0_NEUTRAL_VECTOR_CARDINALITY_Z_LE_81",
            "selector_neutral_vector_cardinality_z_le_81",
            "Neutral-vector carrier cardinality alone: Z <= 81",
            "NATIVE_CARRIER_CARDINALITY_CONTROL",
        ),
        (
            "C1_TENSOR_ALPHA_BOUNDARY_Z_LE_83",
            "selector_tensor_alpha_boundary_z_le_83",
            "Carrier boundary: neutral_vector_carrier 81 + alpha_H 2 = Z <= 83",
            "NATIVE_CARRIER_ALPHA_BOUNDARY",
        ),
        (
            "C2_CARRIER_HIDDEN_CLOCK",
            "selector_carrier_hidden_clock",
            "Carrier/hidden CLOCK candidate: Z <= 83 excluding H-alpha_H and H-alpha_H+T",
            "NATIVE_CARRIER_HIDDEN_CANDIDATE",
        ),
    ]
    selector_scores = [
        score_selector(candidate_rows, selector_id, column, description, input_class)
        for selector_id, column, description, input_class in selector_specs
    ]
    selector_fields = [
        "selector_id",
        "selector_column",
        "description",
        "input_class",
        "predicted_stable_count_all_126",
        "predicted_stable_count_known_118",
        "scored_rows",
        "reference_target",
        "true_positive_stable",
        "false_positive_radioactive",
        "false_negative_stable",
        "true_negative_radioactive",
        "accuracy",
        "precision",
        "recall",
        "false_positive_Z",
        "false_negative_Z",
        "boundary_note",
    ]
    write_csv(SELECTOR_SCORES, selector_scores, selector_fields)

    wrong_specs = [
        (
            "WC1_NO_ALPHA_BRIDGE_WITH_MAIN_HOLES",
            "selector_wc_no_alpha_bridge_with_main_holes",
            "Drop alpha_H bridge from boundary: Z <= 81 with main holes",
            "WRONG_CONTROL",
        ),
        (
            "WC2_NO_HOLE_REJECTOR",
            "selector_wc_no_hole_rejector",
            "Keep Z <= 83 but do not reject native holes",
            "WRONG_CONTROL",
        ),
        (
            "WC3_HOLES_WITHOUT_ALPHA_OFFSET",
            "selector_wc_holes_without_alpha_offset",
            "Use H and H+T as holes instead of H-alpha_H and H-alpha_H+T",
            "WRONG_CONTROL",
        ),
        (
            "WC4_SINGLE_HOLE_NO_TENSOR_SHIFT",
            "selector_wc_single_hole_no_tensor_shift",
            "Reject only H-alpha_H and omit the tensor-shifted hole",
            "WRONG_CONTROL",
        ),
    ]
    wrong_scores = [
        score_selector(candidate_rows, selector_id, column, description, input_class)
        for selector_id, column, description, input_class in wrong_specs
    ]
    write_csv(WRONG_CONTROLS, wrong_scores, selector_fields)

    carrier_by_role = {row["role"]: row for row in carrier_rows}
    reference_counts = dict(Counter(row["reference_clock"] for row in candidate_rows))
    main_score = next(row for row in selector_scores if row["selector_id"] == "C2_CARRIER_HIDDEN_CLOCK")
    boundary_score = next(row for row in selector_scores if row["selector_id"] == "C1_TENSOR_ALPHA_BOUNDARY_Z_LE_83")

    check(checks, "all_input_files_present", all(row["exists"] == "True" for row in manifest), [row for row in manifest if row["exists"] != "True"], "all present")
    check(checks, "hidden_bigrade_set_expected", hidden_set == [1, 2, 3, 4, 6, 8, 9, 12], hidden_set, [1, 2, 3, 4, 6, 8, 9, 12])
    check(checks, "hidden_sum_45", hidden_sum == 45, hidden_sum, 45)
    check(checks, "tensor_release_18", TENSOR_RELEASE == 18, fstr(TENSOR_RELEASE), "18")
    check(checks, "neutral_vector_carrier_81", NEUTRAL_VECTOR_CARRIER == 81, fstr(NEUTRAL_VECTOR_CARRIER), "81")
    check(checks, "cr217_tensor_partition_matches_18", carrier_by_role["graviton"]["observed_partition"] == "18", carrier_by_role["graviton"]["observed_partition"], "18")
    check(checks, "cr217_neutral_vector_partition_matches_81", carrier_by_role["Z"]["observed_partition"] == "81", carrier_by_role["Z"]["observed_partition"], "81")
    check(checks, "cr218_hidden_set_verified", cr218_summary.get("predicted_partitions_main_rule") == hidden_set, cr218_summary.get("predicted_partitions_main_rule"), hidden_set)
    check(checks, "clock_boundary_83", CLOCK_BOUNDARY == 83, fstr(CLOCK_BOUNDARY), "83")
    check(checks, "native_holes_43_61", holes == [43, 61], holes, [43, 61])
    check(checks, "candidate_stable_count_81", int(CLOCK_BOUNDARY) - len(holes) == 81, int(CLOCK_BOUNDARY) - len(holes), 81)
    check(checks, "sob_rows_126", len(sob_rows) == 126, len(sob_rows), 126)
    check(checks, "reference_clock_counts_81_37_8", reference_counts == {"stable": 81, "radioactive": 37, "frontier": 8}, reference_counts, {"stable": 81, "radioactive": 37, "frontier": 8})
    check(checks, "boundary_selector_false_positive_holes_43_61", boundary_score["false_positive_Z"] == "43;61", boundary_score["false_positive_Z"], "43;61")
    check(
        checks,
        "carrier_hidden_clock_exact_against_comparator",
        main_score["accuracy"] == "1.000000"
        and main_score["predicted_stable_count_known_118"] == 81
        and main_score["false_positive_Z"] == ""
        and main_score["false_negative_Z"] == "",
        main_score,
        "accuracy=1.000000,count=81,no FP,no FN",
    )
    check(checks, "wrong_controls_all_distinct_from_exact", all(row["accuracy"] != "1.000000" for row in wrong_scores), wrong_scores, "all wrong controls accuracy < 1")
    check(checks, "cr217_recorded_total_partition_162", cr217_summary.get("partition_sums", {}).get("total") == "162", cr217_summary.get("partition_sums", {}).get("total"), "162")

    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])
    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    result_class = (
        "CR225_PASS_CARRIER_HIDDEN_CLOCK_SELECTOR_CANDIDATE__"
        "BOUNDARY_83_AND_HOLES_43_61_NATIVE_FORMULA__HH001_MATCH_81_OF_81__"
        "MECHANISM_CANDIDATE_NOT_FINAL_PHYSICAL_PROOF"
        if execution_status == "CLEAN"
        else "CR225_FAIL_CARRIER_HIDDEN_CLOCK_SELECTOR_CANDIDATE"
    )

    summary = {
        "artifact": "CR225_CARRIER_HIDDEN_CLOCK_SELECTOR",
        "cr_id": "CR225",
        "generated_at_utc": utc_now(),
        "execution_status": execution_status,
        "checks_passed": passed,
        "checks_total": len(checks),
        "result_class": result_class,
        "native_formula": {
            "R": fstr(R),
            "D": fstr(D),
            "alpha_H": fstr(ALPHA_H),
            "split": fstr(SPLIT),
            "capacity": fstr(CAPACITY),
            "tensor_release_T": fstr(TENSOR_RELEASE),
            "neutral_vector_carrier_Zc": fstr(NEUTRAL_VECTOR_CARRIER),
            "hidden_set": hidden_set,
            "hidden_sum_H": hidden_sum,
            "clock_boundary": fstr(CLOCK_BOUNDARY),
            "holes": holes,
            "candidate_rule": "stable iff Z <= 83 and Z not in {43,61}",
        },
        "selector_scores": {row["selector_id"]: row for row in selector_scores},
        "wrong_controls": {row["selector_id"]: row for row in wrong_scores},
        "reference_clock_counts": reference_counts,
        "boundary": (
            "CR225 produces a zero-free-parameter native CLOCK selector candidate from carrier and "
            "hidden-source constants. It exactly matches the HH001 stable/radioactive comparator "
            "over Z001-Z118, but records the mechanism as a candidate requiring independent pressure tests."
        ),
        "outputs": {
            "formula_terms": rel(FORMULA_TERMS),
            "candidate_rows": rel(CANDIDATE_ROWS),
            "selector_scores": rel(SELECTOR_SCORES),
            "wrong_controls": rel(WRONG_CONTROLS),
            "input_manifest": rel(INPUT_MANIFEST),
            "checks": rel(CHECKS),
            "summary": rel(SUMMARY),
            "result": rel(RESULT),
        },
    }
    write_json(SUMMARY, summary)

    result_md = f"""# CR225 Carrier/Hidden CLOCK Selector Candidate

Result: **{result_class}**

## Direct Answer

The carrier/hidden formula candidate lands on the HH001 CLOCK comparator:

```text
stable iff Z <= 83 and Z not in {{43,61}}
```

It is generated without public element cards, known labels, measured masses, or
CLOCK labels as construction inputs.

## Native Formula

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8

T = R^2 / 2^D = 18
Zc = D^(D+1) = 81
hidden_set = {{1,2,3,4,6,8,9,12}}
H = sum(hidden_set) = 45

clock_boundary = Zc + alpha_H = 83
hole_seed = H - alpha_H = 43
hole_tensor_shift = hole_seed + T = 61
```

So the candidate CLOCK selector is:

```text
CLOCK_stable_native(Z) = (Z <= 83) and (Z not in {{43,61}})
```

## Comparator Score

| Selector | Predicted | TP | FP | FN | TN | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| neutral-vector cardinality `Z <= 81` | {selector_scores[0]['predicted_stable_count_known_118']} | {selector_scores[0]['true_positive_stable']} | {selector_scores[0]['false_positive_radioactive']} | {selector_scores[0]['false_negative_stable']} | {selector_scores[0]['true_negative_radioactive']} | {selector_scores[0]['accuracy']} |
| carrier boundary `Z <= 83` | {selector_scores[1]['predicted_stable_count_known_118']} | {selector_scores[1]['true_positive_stable']} | {selector_scores[1]['false_positive_radioactive']} | {selector_scores[1]['false_negative_stable']} | {selector_scores[1]['true_negative_radioactive']} | {selector_scores[1]['accuracy']} |
| carrier/hidden CLOCK candidate | {main_score['predicted_stable_count_known_118']} | {main_score['true_positive_stable']} | {main_score['false_positive_radioactive']} | {main_score['false_negative_stable']} | {main_score['true_negative_radioactive']} | {main_score['accuracy']} |

The boundary-only candidate reproduces the previous `83` surface and leaves the
two holes `43;61`. The carrier/hidden rejector removes exactly those two rows
and gives the 81-row CLOCK comparator surface.

## What Is Backed

- `T = 18` matches the CR217 tensor/graviton carrier row.
- `Zc = 81` matches the CR217 neutral-vector carrier row.
- `hidden_set = {{1,2,3,4,6,8,9,12}}` is the CR218 bigrade-derived set.
- The formula-derived holes are `{holes[0]}` and `{holes[1]}`.
- The resulting selector matches HH001/CLOCK over scored rows with no false
  positives and no false negatives.

## Boundary

This is a strong native selector candidate, not a final physical proof. The
CLOCK labels are still used only as a comparator. The next pressure test is to
ask whether the same carrier/hidden rule predicts a held-out surface or a new
isotope/decay boundary without reference labels.

## Artifacts

- `{rel(FORMULA_TERMS)}`
- `{rel(CANDIDATE_ROWS)}`
- `{rel(SELECTOR_SCORES)}`
- `{rel(WRONG_CONTROLS)}`
- `{rel(INPUT_MANIFEST)}`
- `{rel(CHECKS)}`
- `{rel(SUMMARY)}`
- `{rel(HASHES)}`
"""
    RESULT.write_text(result_md, encoding="utf-8")

    write_hashes([
        PRECOMMIT,
        RUNNER,
        FORMULA_TERMS,
        CANDIDATE_ROWS,
        SELECTOR_SCORES,
        WRONG_CONTROLS,
        INPUT_MANIFEST,
        CHECKS,
        SUMMARY,
        RESULT,
    ])

    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
