from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


TEST_ID = "CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT"
HERE = Path(__file__).resolve().parent
BRANCH = HERE.parent
ROOT = BRANCH.parent
README = BRANCH / "README.md"
PRECOMMIT = HERE / "CR004_PRECOMMIT.md"
PREMISES = HERE / "CR004_declared_premises.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve()))


def in_range(value: float, bounds: list[float]) -> bool:
    return float(bounds[0]) <= value <= float(bounds[1])


def candidate_values(candidate: str, mu: float, radius: float, c: float) -> dict[str, float]:
    r_s = 2.0 * mu / c**2
    if candidate == "sam_A_kernel":
        A = r_s / radius
        phi = -c**2 * A / 2.0
        g = c**2 * r_s / (2.0 * radius**2)
        v_escape = c * math.sqrt(A)
    elif candidate == "half_A":
        A = mu / (c**2 * radius)
        phi = -c**2 * A / 2.0
        g = c**2 * (mu / c**2) / (2.0 * radius**2)
        v_escape = c * math.sqrt(A)
    elif candidate == "double_A":
        A = 4.0 * mu / (c**2 * radius)
        phi = -c**2 * A / 2.0
        g = c**2 * (4.0 * mu / c**2) / (2.0 * radius**2)
        v_escape = c * math.sqrt(A)
    elif candidate == "inverse_square_A":
        A = (r_s / radius) ** 2
        phi = -c**2 * A / 2.0
        g = c**2 * (2.0 * r_s**2 / radius**3) / 2.0
        v_escape = c * math.sqrt(A)
    elif candidate == "potential_no_half":
        A = r_s / radius
        phi = -c**2 * A
        g = c**2 * r_s / radius**2
        v_escape = c * math.sqrt(A)
    elif candidate == "gravity_missing_half":
        A = r_s / radius
        phi = -c**2 * A / 2.0
        g = c**2 * r_s / radius**2
        v_escape = c * math.sqrt(A)
    elif candidate == "escape_missing_factor":
        A = r_s / radius
        phi = -c**2 * A / 2.0
        g = c**2 * r_s / (2.0 * radius**2)
        v_escape = c * math.sqrt(A / 2.0)
    else:
        raise ValueError(candidate)

    return {
        "A": A,
        "Phi": phi,
        "g": g,
        "v_escape": v_escape,
        "newton_g": mu / radius**2,
        "newton_phi": -mu / radius,
        "newton_escape": math.sqrt(2.0 * mu / radius),
    }


def write_hashes(paths: list[Path]) -> None:
    rows = [
        "# Test Artifact Hashes",
        "algorithm = SHA256",
        "scope = branch README plus local test-folder artifacts",
        "note = HASHES.txt is excluded from its own hash",
        "",
        "path,sha256",
    ]
    for path in sorted({p.resolve() for p in paths}):
        rows.append(f"{path.relative_to(ROOT.resolve())},{sha256(path)}")
    (HERE / "HASHES.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    doc: dict[str, Any] = json.loads(PREMISES.read_text(encoding="utf-8"))
    c = float(doc["constants"]["c"])
    candidates = [
        "sam_A_kernel",
        "half_A",
        "double_A",
        "inverse_square_A",
        "potential_no_half",
        "gravity_missing_half",
        "escape_missing_factor",
    ]

    rows: list[dict[str, Any]] = []
    for body in doc["bodies"]:
        mu = float(body["mu_m3_s2"])
        radius = float(body["radius_m"])
        for candidate in candidates:
            vals = candidate_values(candidate, mu, radius, c)
            potential_identity = math.isclose(vals["Phi"], vals["newton_phi"], rel_tol=1e-12, abs_tol=1e-12)
            acceleration_identity = math.isclose(vals["g"], vals["newton_g"], rel_tol=1e-12, abs_tol=1e-12)
            escape_identity = math.isclose(vals["v_escape"], vals["newton_escape"], rel_tol=1e-12, abs_tol=1e-12)
            external_g_pass = in_range(vals["g"], body["surface_g_range_m_s2"])
            external_escape_pass = in_range(vals["v_escape"], body["escape_speed_range_m_s"])
            row = {
                "body": body["name"],
                "candidate": candidate,
                "A": vals["A"],
                "Phi": vals["Phi"],
                "g": vals["g"],
                "v_escape": vals["v_escape"],
                "potential_identity": potential_identity,
                "acceleration_identity": acceleration_identity,
                "escape_identity": escape_identity,
                "external_g_pass": external_g_pass,
                "external_escape_pass": external_escape_pass,
            }
            row["full_packet"] = all(
                [
                    potential_identity,
                    acceleration_identity,
                    escape_identity,
                    external_g_pass,
                    external_escape_pass,
                ]
            )
            rows.append(row)

    selected_rows = [row for row in rows if row["candidate"] == "sam_A_kernel" and row["full_packet"]]
    wrong_full = [row for row in rows if row["candidate"] != "sam_A_kernel" and row["full_packet"]]
    body_count = len(doc["bodies"])
    trace_ascii_clean = all(ord(ch) < 128 for ch in README.read_text(encoding="utf-8"))

    pass_conditions = {
        "no_older_test_outputs_used": not bool(doc["older_test_outputs_allowed"]),
        "external_data_required": bool(doc["external_data_required"]),
        "free_parameters_introduced_zero": int(doc["free_parameters_introduced"]) == 0,
        "trace_ascii_clean": trace_ascii_clean,
        "sam_packet_passes_all_bodies": len(selected_rows) == body_count,
        "wrong_controls_do_not_match_full_packet": len(wrong_full) == 0,
    }

    verdict = (
        "CR004_PASS_SCOPED_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT"
        if all(pass_conditions.values())
        else "CR004_FAIL_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT"
    )
    execution_status = "CLEAN"
    scientific_verdict = "PASS" if verdict.startswith("CR004_PASS") else "FAIL"
    triage_bin = "A" if scientific_verdict == "PASS" else "C"

    with (HERE / "CR004_candidate_rows.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    manifest_rows = [
        {"path": rel(PRECOMMIT), "role": "precommit", "sha256": sha256(PRECOMMIT)},
        {"path": rel(PREMISES), "role": "declared_premises_external_anchors", "sha256": sha256(PREMISES)},
        {"path": rel(README), "role": "branch_readme_trace", "sha256": sha256(README)},
    ]
    with (HERE / "CR004_input_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "role", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    summary = {
        "test_id": TEST_ID,
        "verdict": verdict,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "body_count": body_count,
        "sam_packet_pass_count": len(selected_rows),
        "wrong_control_full_packet_count": len(wrong_full),
        "pass_conditions": pass_conditions,
        "rule_9": doc["rule_9"],
    }
    (HERE / "CR004_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# CR004 Weak-Field A-Kernel External Contact",
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
        "claim_tier = PASS_SCOPED_WEAK_FIELD",
        "```",
        "",
        "## Branch Claim Tested",
        "",
        "```text",
        "A(r) = r_s/r = 2GM/(c^2 r)",
        "Phi = -c^2 A/2",
        "g = (c^2/2) |dA/dr|",
        "v_escape = c sqrt(A)",
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
            "## External Anchor Rows",
            "",
            "| body | candidate | g | v_escape | full_packet |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        if row["candidate"] == "sam_A_kernel" or row["full_packet"]:
            lines.append(
                f"| {row['body']} | {row['candidate']} | {row['g']:.12g} | {row['v_escape']:.12g} | {'true' if row['full_packet'] else 'false'} |"
            )
    lines.extend(
        [
            "",
            "## Wrong Control Summary",
            "",
            "```text",
            f"wrong_control_full_packet_count = {len(wrong_full)}",
            "```",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            doc["rule_9"],
            "```",
            "",
            "## Courtroom Reading",
            "",
            "CR004 gives the weak-field A-kernel an external-contact PASS in a",
            "scoped local weak-field lane. It does not claim GPS, Shapiro delay,",
            "strong-field closure, or full GR; those remain separate branches.",
            "",
        ]
    )
    (HERE / "CR004_result.md").write_text("\n".join(lines), encoding="utf-8")

    write_hashes(
        [
            README,
            PRECOMMIT,
            PREMISES,
            Path(__file__),
            HERE / "CR004_candidate_rows.csv",
            HERE / "CR004_input_manifest.csv",
            HERE / "CR004_summary.json",
            HERE / "CR004_result.md",
        ]
    )

    print(verdict)
    print(f"execution_status={execution_status}")
    print(f"scientific_verdict={scientific_verdict}")
    print(f"sam_packet_pass_count={len(selected_rows)}/{body_count}")
    print(f"wrong_control_full_packet_count={len(wrong_full)}")
    return 0 if verdict.startswith("CR004_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
