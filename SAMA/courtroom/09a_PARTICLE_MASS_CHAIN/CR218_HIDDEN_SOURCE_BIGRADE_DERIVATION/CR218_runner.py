from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR218_HIDDEN_SOURCE_BIGRADE_DERIVATION"

INPUT_SEALED_195 = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
    / "CR214_particle_complement_195.csv"
)
INPUT_ACTIVE = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR216_CARRIER_DUPLICATE_RETIREMENT"
    / "CR216_particle_complement_194_active.csv"
)
INPUT_CR217 = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR217_DEDUP_STRUCTURAL_IDENTITY_AUDIT"
    / "CR217_summary.json"
)
INPUT_ALPHA_H = ROOT / "02_A_KERNEL_WEAK_FIELD" / "README.md"

SEALED_HASHES = {
    INPUT_SEALED_195: "e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545",
    INPUT_ACTIVE:     "01e780c0fbb315d0aaf93cc6b060ffc4c9cfd0da29ab7155b4da8ca40d444179",
    INPUT_CR217:      "375e458b34e215b5ff500e9da3305286df8b9634dcc5388ed018ba762a8ee06d",
    INPUT_ALPHA_H:    "317081ed0425f71cf885bf024aadae1ee4ab8abb7a217cec8b6de419f84cc6cc",
}

ALPHA_H = 2
D = 3
R = 12
R_SQUARED = R * R  # 144

EXPECTED_OBSERVED = {1, 2, 3, 4, 6, 8, 9, 12}
EXPECTED_PREDICTED = {1, 2, 3, 4, 6, 8, 9, 12}
EXPECTED_WC1_EXTRAS = {16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81, 96, 108, 128, 144}
EXPECTED_WC2_EXTRAS = {5, 7, 10, 11}
EXPECTED_WC3_OMISSIONS = {12}


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
        return list(reader.fieldnames or []), list(reader)


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


def enumerate_bigrade(upper_bound: int) -> list[tuple[int, int, int]]:
    """Return list of (a, b, p=alpha_H^a * D^b) with p <= upper_bound."""
    out = []
    a = 0
    while ALPHA_H ** a <= upper_bound:
        b = 0
        while (ALPHA_H ** a) * (D ** b) <= upper_bound:
            p = (ALPHA_H ** a) * (D ** b)
            out.append((a, b, p))
            b += 1
        a += 1
    return sorted(out, key=lambda t: (t[2], t[0], t[1]))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Verify sealed input hashes.
    input_observed: dict[Path, str] = {}
    input_match: dict[Path, bool] = {}
    for path, expected in SEALED_HASHES.items():
        observed = sha256_file(path)
        input_observed[path] = observed
        input_match[path] = observed == expected
    all_inputs_verified = all(input_match.values())

    # 2. Read CR214 hidden_source partition values.
    _, sealed_rows = read_csv(INPUT_SEALED_195)
    hidden_source_partitions = sorted(
        int(r["partition_signature"])
        for r in sealed_rows
        if r.get("bin") == "hidden_source_support_rows"
    )
    observed_set = set(hidden_source_partitions)

    # 3. Apply main rule: p = alpha_H^a * D^b AND p <= R.
    main_entries = [(a, b, p) for (a, b, p) in enumerate_bigrade(R)]
    predicted_set = {p for (_, _, p) in main_entries}

    # 4. WC1: p = alpha_H^a * D^b AND p <= R^2 = 144.
    wc1_entries = [(a, b, p) for (a, b, p) in enumerate_bigrade(R_SQUARED)]
    wc1_set = {p for (_, _, p) in wc1_entries}

    # 5. WC2: drop bigrade constraint, use p <= R.
    wc2_set = set(range(1, R + 1))

    # 6. WC3: bigrade AND p < R (strict).
    wc3_set = {p for (_, _, p) in enumerate_bigrade(R) if p < R}

    # 7. Compare predicted_set vs observed_set.
    main_extras = predicted_set - observed_set
    main_omissions = observed_set - predicted_set
    main_match = (predicted_set == observed_set)

    # 8. Wrong control comparisons (each WC should FAIL set-equality).
    wc1_extras = wc1_set - observed_set
    wc1_omissions = observed_set - wc1_set
    wc1_distinct = (wc1_set != observed_set)

    wc2_extras = wc2_set - observed_set
    wc2_omissions = observed_set - wc2_set
    wc2_distinct = (wc2_set != observed_set)

    wc3_extras = wc3_set - observed_set
    wc3_omissions = observed_set - wc3_set
    wc3_distinct = (wc3_set != observed_set)

    # 9. Emit the bigrade enumeration table (up to R^2 so WC1 is covered).
    enum_rows = []
    for (a, b, p) in wc1_entries:
        lift = Fraction(p * p, R_SQUARED)
        enum_rows.append({
            "a_exponent_alpha_H": a,
            "b_exponent_D": b,
            "p_value": p,
            "p_form": f"{ALPHA_H}^{a} * {D}^{b}",
            "lift_p_squared_over_R_squared": str(lift),
            "lift_as_decimal": f"{float(lift):.10f}",
            "in_main_rule_p_le_R": p <= R,
            "in_WC1_p_le_R_squared": p <= R_SQUARED,
            "in_WC3_strict_p_lt_R": p < R,
            "in_observed_hidden_source_set": p in observed_set,
        })
    write_csv(
        OUT / "CR218_bigrade_enumeration.csv",
        enum_rows,
        [
            "a_exponent_alpha_H",
            "b_exponent_D",
            "p_value",
            "p_form",
            "lift_p_squared_over_R_squared",
            "lift_as_decimal",
            "in_main_rule_p_le_R",
            "in_WC1_p_le_R_squared",
            "in_WC3_strict_p_lt_R",
            "in_observed_hidden_source_set",
        ],
    )

    # 10. Set comparison side-by-side.
    all_relevant = sorted(predicted_set | observed_set)
    set_compare_rows = []
    for p in all_relevant:
        in_predicted = p in predicted_set
        in_observed = p in observed_set
        set_compare_rows.append({
            "p_value": p,
            "in_predicted_main_rule": in_predicted,
            "in_observed_hidden_source": in_observed,
            "agreement": "MATCH" if (in_predicted == in_observed) else "MISMATCH",
        })
    write_csv(
        OUT / "CR218_set_comparison.csv",
        set_compare_rows,
        ["p_value", "in_predicted_main_rule", "in_observed_hidden_source", "agreement"],
    )

    # 11. Wrong controls CSV.
    wc_rows = [
        {
            "wrong_control_id": "WC1",
            "rule_description": "p = 2^a * 3^b AND p <= R^2 = 144",
            "predicted_size": len(wc1_set),
            "observed_size": len(observed_set),
            "extras_vs_observed": ";".join(str(x) for x in sorted(wc1_extras)),
            "omissions_vs_observed": ";".join(str(x) for x in sorted(wc1_omissions)),
            "distinct_from_observed": wc1_distinct,
            "expected_extras_match": wc1_extras == EXPECTED_WC1_EXTRAS,
            "pass": wc1_distinct and (wc1_extras == EXPECTED_WC1_EXTRAS) and (len(wc1_set) == 23),
        },
        {
            "wrong_control_id": "WC2",
            "rule_description": "p in Z_{>0} AND p <= R (no bigrade constraint)",
            "predicted_size": len(wc2_set),
            "observed_size": len(observed_set),
            "extras_vs_observed": ";".join(str(x) for x in sorted(wc2_extras)),
            "omissions_vs_observed": ";".join(str(x) for x in sorted(wc2_omissions)),
            "distinct_from_observed": wc2_distinct,
            "expected_extras_match": wc2_extras == EXPECTED_WC2_EXTRAS,
            "pass": wc2_distinct and (wc2_extras == EXPECTED_WC2_EXTRAS) and (len(wc2_set) == 12),
        },
        {
            "wrong_control_id": "WC3",
            "rule_description": "p = 2^a * 3^b AND p < R (strict)",
            "predicted_size": len(wc3_set),
            "observed_size": len(observed_set),
            "extras_vs_observed": ";".join(str(x) for x in sorted(wc3_extras)),
            "omissions_vs_observed": ";".join(str(x) for x in sorted(wc3_omissions)),
            "distinct_from_observed": wc3_distinct,
            "expected_omissions_match": wc3_omissions == EXPECTED_WC3_OMISSIONS,
            "pass": wc3_distinct and (wc3_omissions == EXPECTED_WC3_OMISSIONS) and (len(wc3_set) == 7),
        },
    ]
    write_csv(
        OUT / "CR218_wrong_controls.csv",
        wc_rows,
        [
            "wrong_control_id",
            "rule_description",
            "predicted_size",
            "observed_size",
            "extras_vs_observed",
            "omissions_vs_observed",
            "distinct_from_observed",
            "expected_extras_match",
            "expected_omissions_match",
            "pass",
        ],
    )

    # 12. Pass / fail summary checks.
    checks = {
        "all_inputs_verified": all_inputs_verified,
        "observed_set_equals_expected_8_rows": observed_set == EXPECTED_OBSERVED,
        "observed_set_size_is_8": len(observed_set) == 8,
        "predicted_set_equals_expected": predicted_set == EXPECTED_PREDICTED,
        "predicted_set_size_is_8": len(predicted_set) == 8,
        "predicted_set_equals_observed_set": main_match,
        "no_extras_in_predicted_vs_observed": len(main_extras) == 0,
        "no_omissions_in_predicted_vs_observed": len(main_omissions) == 0,
        "WC1_distinct_from_observed_and_size_23": (
            wc1_distinct and (len(wc1_set) == 23) and (wc1_extras == EXPECTED_WC1_EXTRAS)
        ),
        "WC2_distinct_from_observed_and_size_12": (
            wc2_distinct and (len(wc2_set) == 12) and (wc2_extras == EXPECTED_WC2_EXTRAS)
        ),
        "WC3_distinct_from_observed_and_size_7": (
            wc3_distinct and (len(wc3_set) == 7) and (wc3_omissions == EXPECTED_WC3_OMISSIONS)
        ),
    }

    summary = {
        "cr_id": "CR218",
        "test_id": "CR218_HIDDEN_SOURCE_BIGRADE_DERIVATION",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "input_hash_verification": {
            rel(p): {
                "expected_sha256": SEALED_HASHES[p],
                "observed_sha256": input_observed[p],
                "match": input_match[p],
            }
            for p in SEALED_HASHES
        },
        "all_inputs_verified": all_inputs_verified,
        "sealed_primitives": {"alpha_H": ALPHA_H, "D": D, "R": R, "R_squared": R_SQUARED},
        "observed_hidden_source_partitions_from_CR214": sorted(observed_set),
        "predicted_partitions_main_rule": sorted(predicted_set),
        "main_rule": "p = alpha_H^a * D^b for a,b >= 0 AND p <= R",
        "main_extras_predicted_minus_observed": sorted(main_extras),
        "main_omissions_observed_minus_predicted": sorted(main_omissions),
        "main_predicted_equals_observed": main_match,
        "wrong_controls": {
            "WC1_p_le_R_squared": {
                "predicted_size": len(wc1_set),
                "predicted_set": sorted(wc1_set),
                "extras_vs_observed": sorted(wc1_extras),
                "distinct_from_observed": wc1_distinct,
            },
            "WC2_no_bigrade": {
                "predicted_size": len(wc2_set),
                "predicted_set": sorted(wc2_set),
                "extras_vs_observed": sorted(wc2_extras),
                "distinct_from_observed": wc2_distinct,
            },
            "WC3_strict_lift_less_than_1": {
                "predicted_size": len(wc3_set),
                "predicted_set": sorted(wc3_set),
                "omissions_vs_observed": sorted(wc3_omissions),
                "distinct_from_observed": wc3_distinct,
            },
        },
        "checks": checks,
        "checks_passed": sum(1 for v in checks.values() if v),
        "checks_total": len(checks),
        "execution_status": "CLEAN" if all(checks.values()) else "FAIL",
        "result_class": (
            "CR218_PASS_HIDDEN_SOURCE_SET_DERIVED_FROM_BIGRADE_LATTICE_BOUNDED_BY_R__"
            "8_OF_8_OBSERVED_EQUALS_PREDICTED__"
            "WC1_WC2_WC3_ALL_FAIL_AS_REQUIRED"
            if all(checks.values())
            else "CR218_FAIL"
        ),
        "non_promotion_rule": (
            "The match between the lift unity-line (p = R when p^2/R^2 = 1) and the "
            "bigrade-lattice cutoff is recorded as a backed coincidence on the sealed "
            "set. CR218 does not derive why the upstream enumerator selected this "
            "lattice or this bound; those remain open."
        ),
    }
    write_json(OUT / "CR218_summary.json", summary)

    # 13. Input manifest.
    manifest_rows = [
        {
            "artifact": rel(p),
            "sealed_sha256": SEALED_HASHES[p],
            "observed_sha256": input_observed[p],
            "match": "yes" if input_match[p] else "no",
            "role": "sealed_input",
        }
        for p in SEALED_HASHES
    ]
    write_csv(
        OUT / "CR218_input_manifest.csv",
        manifest_rows,
        ["artifact", "sealed_sha256", "observed_sha256", "match", "role"],
    )

    # 14. HASHES.txt.
    hash_targets = list(SEALED_HASHES.keys()) + [
        OUT / "CR218_PRECOMMIT.md",
        OUT / "CR218_declared_premises.json",
        OUT / "CR218_runner.py",
        OUT / "CR218_input_manifest.csv",
        OUT / "CR218_bigrade_enumeration.csv",
        OUT / "CR218_set_comparison.csv",
        OUT / "CR218_wrong_controls.csv",
        OUT / "CR218_summary.json",
        OUT / "CR218_result.md",
    ]
    lines = ["artifact,sha256"]
    for target in hash_targets:
        if target.exists():
            lines.append(f"{rel(target)},{sha256_file(target)}")
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
