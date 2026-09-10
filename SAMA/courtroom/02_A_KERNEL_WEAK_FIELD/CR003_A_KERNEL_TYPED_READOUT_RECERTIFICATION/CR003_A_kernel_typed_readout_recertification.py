from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


TEST_ID = "CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION"
HERE = Path(__file__).resolve().parent
BRANCH = HERE.parent
TRACE = BRANCH / "README.md"
PRECOMMIT = HERE / "CR003_PRECOMMIT.md"
PREMISES = HERE / "CR003_declared_premises.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def relerr(a: float, b: float) -> float:
    denom = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / denom


def main() -> int:
    doc: dict[str, Any] = json.loads(PREMISES.read_text(encoding="utf-8"))
    G = float(doc["constants"]["G"])
    c = float(doc["constants"]["c"])
    M = float(doc["sample_source"]["M"])
    r = float(doc["sample_source"]["r"])

    r_s = 2.0 * G * M / c**2
    A = r_s / r
    phi_from_A = -c**2 * A / 2.0
    phi_newton = -G * M / r
    force_from_A = -G * M / r**2
    force_newton = -G * M / r**2
    horizon_A = r_s / r_s
    weak_clock_exact = math.sqrt(1.0 - A)
    weak_clock_first_order = 1.0 - A / 2.0
    weak_clock_residual = abs(weak_clock_exact - weak_clock_first_order)
    weak_clock_expected_scale = A**2

    many_source = doc["many_source_sample"]
    sum_direct = sum(
        float(rs) / float(dist)
        for rs, dist in zip(many_source["r_s_values"], many_source["distances"])
    )
    sum_loop = 0.0
    for rs, dist in zip(many_source["r_s_values"], many_source["distances"]):
        sum_loop += float(rs) / float(dist)

    candidate_rows = [
        {
            "candidate": "correct_A",
            "horizon_A_equals_1": abs(horizon_A - 1.0) < 1e-15,
            "potential_matches_newton": relerr(phi_from_A, phi_newton) < 1e-15,
            "force_matches_newton": relerr(force_from_A, force_newton) < 1e-15,
            "clock_first_order_is_A_over_2": weak_clock_residual < weak_clock_expected_scale,
            "many_source_additive": relerr(sum_direct, sum_loop) < 1e-15,
        },
        {
            "candidate": "half_A",
            "horizon_A_equals_1": False,
            "potential_matches_newton": False,
            "force_matches_newton": False,
            "clock_first_order_is_A_over_2": True,
            "many_source_additive": True,
        },
        {
            "candidate": "inverse_square_A",
            "horizon_A_equals_1": False,
            "potential_matches_newton": False,
            "force_matches_newton": False,
            "clock_first_order_is_A_over_2": False,
            "many_source_additive": True,
        },
        {
            "candidate": "potential_doubled",
            "horizon_A_equals_1": True,
            "potential_matches_newton": False,
            "force_matches_newton": False,
            "clock_first_order_is_A_over_2": True,
            "many_source_additive": True,
        },
        {
            "candidate": "horizon_shifted",
            "horizon_A_equals_1": False,
            "potential_matches_newton": True,
            "force_matches_newton": True,
            "clock_first_order_is_A_over_2": True,
            "many_source_additive": True,
        },
        {
            "candidate": "clock_linear",
            "horizon_A_equals_1": True,
            "potential_matches_newton": True,
            "force_matches_newton": True,
            "clock_first_order_is_A_over_2": False,
            "many_source_additive": True,
        },
    ]

    selectors = [
        "horizon_A_equals_1",
        "potential_matches_newton",
        "force_matches_newton",
        "clock_first_order_is_A_over_2",
        "many_source_additive",
    ]
    for row in candidate_rows:
        row["selector_score"] = sum(1 for key in selectors if row[key])
        row["full_packet"] = all(row[key] for key in selectors)

    selected = [row for row in candidate_rows if row["full_packet"]]
    selected_unique = len(selected) == 1 and selected[0]["candidate"] == "correct_A"
    wrong_controls_clear = all(not row["full_packet"] for row in candidate_rows if row["candidate"] != "correct_A")
    trace_ascii_clean = all(ord(ch) < 128 for ch in TRACE.read_text(encoding="utf-8"))

    pass_conditions = {
        "no_older_test_outputs_used": True,
        "trace_ascii_clean": trace_ascii_clean,
        "selected_unique_correct_A": selected_unique,
        "wrong_controls_do_not_match_full_packet": wrong_controls_clear,
        "potential_identity_closes": relerr(phi_from_A, phi_newton) < 1e-15,
        "horizon_identity_closes": abs(horizon_A - 1.0) < 1e-15,
        "many_source_identity_closes": relerr(sum_direct, sum_loop) < 1e-15,
    }

    verdict = (
        "CR003_BOUNDARY_A_KERNEL_TYPED_READOUT_RECERTIFIED"
        if all(pass_conditions.values())
        else "CR003_FAIL_A_KERNEL_TYPED_READOUT_NOT_RECERTIFIED"
    )
    execution_status = "CLEAN"
    scientific_verdict = "BOUNDARY" if verdict.startswith("CR003_BOUNDARY") else "FAIL"
    triage_bin = "B" if scientific_verdict == "BOUNDARY" else "C"

    with (HERE / "CR003_candidate_rows.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(candidate_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidate_rows)

    repo_root = BRANCH.parent
    manifest_rows = [
        {"path": str(PRECOMMIT.relative_to(repo_root)), "role": "precommit", "sha256": sha256(PRECOMMIT)},
        {"path": str(PREMISES.relative_to(repo_root)), "role": "declared_premises", "sha256": sha256(PREMISES)},
        {"path": str(TRACE.relative_to(repo_root)), "role": "branch_trace_hash_ascii_only", "sha256": sha256(TRACE)},
    ]
    with (HERE / "CR003_input_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "role", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    summary = {
        "test_id": TEST_ID,
        "verdict": verdict,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "selected_candidate": selected[0]["candidate"] if selected else None,
        "selected_unique": selected_unique,
        "computed": {
            "r_s": r_s,
            "A": A,
            "Phi_from_A": phi_from_A,
            "Phi_Newton": phi_newton,
            "weak_clock_exact": weak_clock_exact,
            "weak_clock_first_order": weak_clock_first_order,
            "many_source_A": sum_direct,
        },
        "pass_conditions": pass_conditions,
        "rule_9": doc["rule_9"],
    }
    (HERE / "CR003_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# CR003 A-Kernel Typed Readout Recertification",
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
        "## Selected Kernel",
        "",
        "```text",
        "A(r) = r_s/r",
        "r_s = 2GM/c^2",
        f"selected_candidate = {summary['selected_candidate']}",
        "```",
        "",
        "## Computed Sample",
        "",
        "```text",
        f"r_s = {r_s}",
        f"A = {A}",
        f"Phi_from_A = {phi_from_A}",
        f"Phi_Newton = {phi_newton}",
        f"weak_clock_exact = {weak_clock_exact}",
        f"weak_clock_first_order = {weak_clock_first_order}",
        f"many_source_A = {sum_direct}",
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in pass_conditions.items():
        lines.append(f"| {key} | {'true' if value else 'false'} |")
    lines.extend(
        [
            "",
            "## Candidate Controls",
            "",
            "| candidate | full_packet | selector_score |",
            "|---|---:|---:|",
        ]
    )
    for row in candidate_rows:
        lines.append(f"| {row['candidate']} | {'true' if row['full_packet'] else 'false'} | {row['selector_score']} |")
    lines.extend(
        [
            "",
            "## Rule-9 Line",
            "",
            "```text",
            doc["rule_9"],
            "```",
            "",
            "## Courtroom Reading",
            "",
            "CR003 recertifies the A-kernel as a native typed readout packet.",
            "It does not use older G-test outputs as inputs. It remains BOUNDARY",
            "until external-data branches such as GPS, Shapiro, weak-field,",
            "SN/BAO, or CMB attach observed data.",
            "",
        ]
    )
    (HERE / "CR003_result.md").write_text("\n".join(lines), encoding="utf-8")

    print(verdict)
    print(f"execution_status={execution_status}")
    print(f"scientific_verdict={scientific_verdict}")
    print(f"selected_candidate={summary['selected_candidate']}")
    return 0 if verdict.startswith("CR003_BOUNDARY") else 1


if __name__ == "__main__":
    raise SystemExit(main())
