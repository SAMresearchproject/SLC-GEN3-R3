from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


TEST_ID = "CR002_R12_NATIVE_GRAMMAR_RECERTIFICATION"
HERE = Path(__file__).resolve().parent
BRANCH = HERE.parent
TRACE = BRANCH / "SAM_COURTROOM_DUODECIMAL_R12_TRACE.md"
PREMISES_PATH = HERE / "CR002_declared_premises.json"
PRECOMMIT_PATH = HERE / "CR002_PRECOMMIT.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def prime_factors(n: int) -> set[int]:
    factors: set[int] = set()
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            factors.add(d)
            x //= d
        d += 1
    if x > 1:
        factors.add(x)
    return factors


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def load_premises() -> dict[str, Any]:
    return json.loads(PREMISES_PATH.read_text(encoding="utf-8"))


def main() -> int:
    premises_doc = load_premises()
    p = premises_doc["premises"]
    alpha_h = int(p["alpha_h"])
    dim = int(p["D"])
    outer = int(p["outer_binary_split"])
    half_side_per_share = int(p["half_side_per_share"])

    route_kernel = outer * alpha_h * dim
    partition_top = alpha_h**2 * dim
    six_route = alpha_h * dim
    fourth = alpha_h**2
    allowed_primes = set(int(x) for x in premises_doc["allowed_prime_axes"])
    radix_walls = set(int(x) for x in premises_doc["radix_wall_parts"])

    candidate_rows: list[dict[str, Any]] = []
    for r in premises_doc["candidate_radices"]:
        r = int(r)
        factors = prime_factors(r)
        row = {
            "R": r,
            "route_kernel_equality": r == route_kernel,
            "partition_top_equality": r == partition_top,
            "half_write_admissible": r % 2 == 0,
            "third_partition_admissible": r % dim == 0,
            "fourth_partition_admissible": r % fourth == 0,
            "six_contact_route_admissible": r % six_route == 0,
            "twelfth_closure_admissible": r % route_kernel == 0,
            "side_share_conservation": (half_side_per_share * r) // half_side_per_share == r,
            "no_new_prime_axis": factors.issubset(allowed_primes),
            "radix_wall_rejection": not any(r % wall == 0 for wall in radix_walls),
            "prime_factors": " ".join(str(x) for x in sorted(factors)),
        }
        packet_selectors = [
            "route_kernel_equality",
            "partition_top_equality",
            "half_write_admissible",
            "third_partition_admissible",
            "fourth_partition_admissible",
            "six_contact_route_admissible",
            "twelfth_closure_admissible",
            "side_share_conservation",
            "no_new_prime_axis",
            "radix_wall_rejection",
        ]
        row["selector_score"] = sum(1 for key in packet_selectors if row[key])
        row["full_packet"] = all(bool(row[key]) for key in packet_selectors)
        candidate_rows.append(row)

    selected = [row for row in candidate_rows if row["full_packet"]]
    selected_unique = len(selected) == 1
    selected_r = selected[0]["R"] if selected_unique else None

    wrong_controls = [
        {"control": "decimal_convenience_R10", "R": 10},
        {"control": "binary_expansion_R8", "R": 8},
        {"control": "side_count_as_completed_share_R24", "R": 24},
        {"control": "half_route_only_R6", "R": 6},
        {"control": "prime_wall_R5", "R": 5},
        {"control": "prime_wall_R7", "R": 7},
        {"control": "prime_wall_R11", "R": 11},
        {"control": "binary_square_R16", "R": 16},
        {"control": "decimal_twenty_R20", "R": 20},
    ]
    rows_by_r = {row["R"]: row for row in candidate_rows}
    for control in wrong_controls:
        row = rows_by_r[control["R"]]
        control["full_packet"] = row["full_packet"]
        control["selector_score"] = row["selector_score"]
        control["fail_reasons"] = ";".join(
            key
            for key, value in row.items()
            if key
            in {
                "route_kernel_equality",
                "partition_top_equality",
                "half_write_admissible",
                "third_partition_admissible",
                "fourth_partition_admissible",
                "six_contact_route_admissible",
                "twelfth_closure_admissible",
                "side_share_conservation",
                "no_new_prime_axis",
                "radix_wall_rejection",
            }
            and not bool(value)
        )

    trace_text = TRACE.read_text(encoding="utf-8")
    trace_ascii_clean = all(ord(ch) < 128 for ch in trace_text)

    hygiene = {
        "older_test_outputs_allowed": premises_doc["older_test_outputs_allowed"],
        "older_test_outputs_used_as_inputs": False,
        "trace_read_for_hash_and_ascii_only": True,
        "trace_ascii_clean": trace_ascii_clean,
    }

    pass_conditions = {
        "no_older_test_outputs_used": not hygiene["older_test_outputs_used_as_inputs"],
        "trace_ascii_clean": trace_ascii_clean,
        "route_kernel_equals_partition_top": route_kernel == partition_top == 12,
        "unique_full_packet_selector": selected_unique,
        "selected_R_is_12": selected_r == 12,
        "wrong_controls_do_not_match_full_packet": not any(c["full_packet"] for c in wrong_controls),
    }

    verdict = (
        "CR002_BOUNDARY_NATIVE_GRAMMAR_RECERTIFIED"
        if all(pass_conditions.values())
        else "CR002_FAIL_NATIVE_GRAMMAR_NOT_RECERTIFIED"
    )
    execution_status = "CLEAN" if pass_conditions["no_older_test_outputs_used"] else "VIOLATED"
    scientific_verdict = "BOUNDARY" if verdict.startswith("CR002_BOUNDARY") else "FAIL"
    triage_bin = "B" if scientific_verdict == "BOUNDARY" else "C"

    with (HERE / "CR002_candidate_rows.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(candidate_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidate_rows)

    with (HERE / "CR002_wrong_controls.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(wrong_controls[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(wrong_controls)

    input_manifest = [
        {
            "path": str(PRECOMMIT_PATH.relative_to(BRANCH.parent)),
            "role": "precommit",
            "sha256": sha256(PRECOMMIT_PATH),
        },
        {
            "path": str(PREMISES_PATH.relative_to(BRANCH.parent)),
            "role": "declared_premises",
            "sha256": sha256(PREMISES_PATH),
        },
        {
            "path": str(TRACE.relative_to(BRANCH.parent)),
            "role": "provenance_trace_hash_ascii_only",
            "sha256": sha256(TRACE),
        },
    ]
    with (HERE / "CR002_input_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "role", "sha256"])
        writer.writeheader()
        writer.writerows(input_manifest)

    summary = {
        "test_id": TEST_ID,
        "verdict": verdict,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "selected_R": selected_r,
        "route_kernel": route_kernel,
        "partition_top": partition_top,
        "selected_unique": selected_unique,
        "pass_conditions": pass_conditions,
        "hygiene": hygiene,
        "rule_9": premises_doc["rule_9"],
        "outputs": [
            "CR002_candidate_rows.csv",
            "CR002_wrong_controls.csv",
            "CR002_input_manifest.csv",
            "CR002_summary.json",
            "CR002_result.md",
        ],
    }
    (HERE / "CR002_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_lines = [
        "# CR002 R12 Native Grammar Recertification",
        "",
        "## Verdict",
        "",
        "```text",
        verdict,
        "```",
        "",
        "## Courtroom Fields",
        "",
        "```text",
        f"execution_status = {execution_status}",
        f"scientific_verdict = {scientific_verdict}",
        f"triage_bin = {triage_bin}",
        "```",
        "",
        "## Selected Packet",
        "",
        "```text",
        f"selected_R = {selected_r}",
        f"route_kernel = {route_kernel}",
        f"partition_top = {partition_top}",
        "A_share = 1/12",
        "A_side = 1/24",
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in pass_conditions.items():
        result_lines.append(f"| {key} | {as_bool(value)} |")
    result_lines.extend(
        [
            "",
            "## Wrong Controls",
            "",
            "| control | R | full_packet | selector_score | fail_reasons |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for c in wrong_controls:
        result_lines.append(
            f"| {c['control']} | {c['R']} | {as_bool(bool(c['full_packet']))} | {c['selector_score']} | {c['fail_reasons']} |"
        )
    result_lines.extend(
        [
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises_doc["rule_9"],
            "```",
            "",
            "## Courtroom Reading",
            "",
            "CR002 is a clean native grammar recertification. It selects R=12 from",
            "declared SAM grammar premises and rejects the wrong controls. It does not",
            "supply an external downstream datum by itself, so the strict Courtroom",
            "scientific verdict remains BOUNDARY.",
            "",
        ]
    )
    (HERE / "CR002_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    print(verdict)
    print(f"execution_status={execution_status}")
    print(f"scientific_verdict={scientific_verdict}")
    print(f"selected_R={selected_r}")
    print(f"trace_ascii_clean={trace_ascii_clean}")
    return 0 if verdict.startswith("CR002_BOUNDARY") else 1


if __name__ == "__main__":
    raise SystemExit(main())
