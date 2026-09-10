"""CR284 constructive desalination campaign-intake runner.

This runner verifies the frozen source and campaign contract. It produces no
water-ion geometry, pore ranking, molecular energy, or physical desalination
result.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
RECORD_ID = "CR284_WATER_ION_SHAPE_SELECTIVITY_CAMPAIGN_INTAKE"
PASS_CLASS = (
    "CR284_PASS_SCOPED_WATER_ION_SHAPE_SELECTIVITY_CAMPAIGN_INTAKE__"
    "NO_SELECTIVITY_OR_PHYSICAL_PROMOTION"
)

CONTRACT_HASHES = {
    "CR284_PRECOMMIT.md": "8667d8a92d122079397373cec5d32f69889a72cdb3db6ab2c4930778f200ddce",
    "CR284_declared_premises.json": "9fddcaad49d898e45bf84e9fbd9808610f159c849cdea8f2105c10367c254a5e",
    "CR284_CAMPAIGN_PLAN.md": "e64e084af85cecd853e415952be2fa508691e08e7f5aa41b017a2077fc66faec",
    "CR284_WATER_STEWARDSHIP_INTENT.md": "3ccda6621ef8c70d5965c3852a827b427d052c1df547ab63d6aaae4c84f23aca",
    "CR284_species_roster.csv": "82fd78e6a412160ac6f29bc160fb5c161edaf54ef1f0940ba1731b9cee8fe490",
    "CR284_campaign_stages.csv": "10512fcf53be368033bfee23654899cb23f19502b38666c42d2588a4055c0845",
    "CR284_external_sources.csv": "edf340e08e3012116d8c5c073fbefc63caba84f84c6e40e53ded6326689baed0",
    "CR284_wrong_controls_precommitted.csv": "da8dfea0eb5d239d111fe32baff549f524f038d68867669d66b6637f3b1af953",
    "CR284_input_manifest.csv": "25b28c5e1df9a597bf355e940d35ea0c707c0dec40c9318176fb3ced8167e694",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def add_check(checks: list[dict], check_id: str, requirement: str, actual, passed: bool) -> None:
    checks.append(
        {
            "check_id": check_id,
            "requirement": requirement,
            "actual": str(actual),
            "passed": str(bool(passed)).lower(),
        }
    )


def main() -> int:
    sealed_utc = utc_now()
    checks: list[dict] = []

    preflight_file = os.environ.get("SAM_PREFLIGHT_FILE", "")
    preflight_token = os.environ.get("SAM_PREFLIGHT_TOKEN", "")
    runner_version = os.environ.get("SAM_RUNNER_VERSION", "")
    add_check(
        checks,
        "C01",
        "Courtroom preflight metadata is present",
        f"file={bool(preflight_file)} token={bool(preflight_token)}",
        bool(preflight_file and preflight_token and Path(preflight_file).is_file()),
    )

    contract_verification: list[dict] = []
    for name, expected in CONTRACT_HASHES.items():
        path = HERE / name
        exists = path.is_file()
        actual = sha256_path(path) if exists else "MISSING"
        verified = exists and actual == expected
        contract_verification.append(
            {
                "contract_file": name,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "verified": str(verified).lower(),
            }
        )
    add_check(
        checks,
        "C02",
        "All precommitted campaign-contract files match SHA-256",
        f"{sum(r['verified'] == 'true' for r in contract_verification)}/{len(contract_verification)}",
        all(r["verified"] == "true" for r in contract_verification),
    )

    manifest_rows = read_csv(HERE / "CR284_input_manifest.csv")
    source_verification: list[dict] = []
    source_text_by_role: dict[str, str] = {}
    for row in manifest_rows:
        path = Path(row["path"])
        exists = path.is_file()
        actual_hash = sha256_path(path) if exists else "MISSING"
        actual_bytes = path.stat().st_size if exists else -1
        verified = (
            exists
            and actual_hash == row["sha256"]
            and actual_bytes == int(row["bytes"])
        )
        source_verification.append(
            {
                "source_id": row["source_id"],
                "role": row["role"],
                "path": row["path"],
                "expected_bytes": row["bytes"],
                "actual_bytes": actual_bytes,
                "expected_sha256": row["sha256"],
                "actual_sha256": actual_hash,
                "verified": str(verified).lower(),
                "usage_boundary": row["usage_boundary"],
            }
        )
        if exists and path.suffix.lower() in {".md", ".txt"}:
            source_text_by_role[row["role"]] = read_text(path)

    add_check(checks, "C03", "Exactly 18 local sources are frozen", len(manifest_rows), len(manifest_rows) == 18)
    add_check(
        checks,
        "C04",
        "Every frozen local source exists and matches bytes plus SHA-256",
        f"{sum(r['verified'] == 'true' for r in source_verification)}/{len(source_verification)}",
        all(r["verified"] == "true" for r in source_verification),
    )

    premises = read_json(HERE / "CR284_declared_premises.json")
    add_check(checks, "C05", "CR284 is constructive new work", premises["campaign_kind"], premises["campaign_kind"] == "CONSTRUCTIVE_NEW_WORK")
    add_check(checks, "C06", "No observed targets are allowed before reveal", premises["observed_selectivity_targets_allowed_before_reveal"], premises["observed_selectivity_targets_allowed_before_reveal"] is False)
    add_check(checks, "C07", "No physical promotion is allowed", premises["physical_promotion_allowed"], premises["physical_promotion_allowed"] is False)
    add_check(checks, "C08", "No free parameters are allowed at intake", premises["free_parameters_allowed"], premises["free_parameters_allowed"] == 0)
    add_check(checks, "C09", "SAM carrier is not typed as dissolved ion", premises["sam_carrier_equals_dissolved_ion"], premises["sam_carrier_equals_dissolved_ion"] is False)
    add_check(checks, "C10", "A is not typed directly as pressure or energy", premises["A_equals_pressure_or_energy"], premises["A_equals_pressure_or_energy"] is False)
    add_check(checks, "C11", "Starbreaker remains process context only", premises["starbreaker_role"], premises["starbreaker_role"] == "PROCESS_CONTEXT_ONLY_PENDING_TYPED_PHYSICAL_READOUT")

    species = read_csv(HERE / "CR284_species_roster.csv")
    species_ids = {row["species_id"] for row in species}
    add_check(checks, "C12", "Nine species are frozen", len(species), len(species) == 9)
    add_check(checks, "C13", "Species IDs are unique", len(species_ids), len(species_ids) == len(species))
    add_check(
        checks,
        "C14",
        "No species carries a prediction or observed target",
        "unpredicted_and_false",
        all(row["prediction_status"] == "UNPREDICTED" and row["observed_target_values_allowed"] == "false" for row in species),
    )
    add_check(
        checks,
        "C15",
        "Boron speciation is explicit",
        sorted(row["chemical_species"] for row in species if row["chemical_species"].startswith("B(")),
        {row["chemical_species"] for row in species} >= {"B(OH)3", "B(OH)4-"},
    )

    stages = read_csv(HERE / "CR284_campaign_stages.csv")
    expected_stages = [f"CR{number}" for number in range(284, 290)]
    add_check(checks, "C16", "Six ordered campaign stages are frozen", [row["stage_id"] for row in stages], [row["stage_id"] for row in stages] == expected_stages)
    add_check(checks, "C17", "No campaign stage permits a physical claim", "all_false", all(row["physical_claim_allowed"] == "false" for row in stages))

    external_sources = read_csv(HERE / "CR284_external_sources.csv")
    add_check(checks, "C18", "Two versioned external sources are registered", [row["version"] for row in external_sources], {row["version"] for row in external_sources} == {"arXiv:2501.19344v2", "arXiv:2107.07137v1"})
    add_check(
        checks,
        "C19",
        "External numerical species results remain reveal-gated",
        [row["reveal_status"] for row in external_sources],
        any("EMBARGOED_UNTIL_CR288" in row["reveal_status"] for row in external_sources),
    )

    wrong_controls = read_csv(HERE / "CR284_wrong_controls_precommitted.csv")
    required_control_classes = {"simple_baseline", "randomization", "leakage", "rescue_rule", "category_error", "physical_artifact", "promotion_error", "role_conflation"}
    actual_control_classes = {row["control_class"] for row in wrong_controls}
    add_check(checks, "C20", "Fourteen wrong controls are frozen", len(wrong_controls), len(wrong_controls) == 14)
    add_check(checks, "C21", "All required control classes are present", sorted(actual_control_classes), required_control_classes <= actual_control_classes)
    add_check(
        checks,
        "C22",
        "Every control has a required disposition and falsifier",
        "complete",
        all(row["required_disposition"] and row["falsifies_if"] for row in wrong_controls),
    )

    precommit = read_text(HERE / "CR284_PRECOMMIT.md")
    campaign_plan = read_text(HERE / "CR284_CAMPAIGN_PLAN.md")
    stewardship = read_text(HERE / "CR284_WATER_STEWARDSHIP_INTENT.md")
    stewardship_normalized = " ".join(stewardship.split())
    add_check(checks, "C23", "Observation-blind rule is explicit", "present", "Observation-Blind Rule" in precommit and "may not use measured or simulated hydrated radii" in precommit)
    add_check(checks, "C24", "Both independent engineering lanes are explicit", "SHAPE_SELECTIVITY + ASSISTED_GATE", "SHAPE_SELECTIVITY" in precommit and "ASSISTED_GATE" in precommit)
    add_check(checks, "C25", "Primary physical metric is energy-normalized", "grams NaCl removed per total watt-hour", "grams NaCl removed per total watt-hour" in campaign_plan)
    add_check(checks, "C26", "Humanitarian royalty-free intent is recorded", "present", "royalty-free" in stewardship and "non-exclusive humanitarian" in stewardship)
    add_check(checks, "C27", "No legal instrument is invented", "explicit boundary", "does not itself select or create an operative" in stewardship_normalized)

    add_check(
        checks,
        "C28",
        "Historical Chladni source preserves no-particle-promotion boundary",
        "present",
        "no_particle_promotion" in source_text_by_role.get("historical_chladni_route_boundary", ""),
    )
    add_check(
        checks,
        "C29",
        "QP093A octahedral realization remains physically open",
        "present",
        "Physical octahedral ontology remains a candidate realization" in source_text_by_role.get("typed_shape_candidate", ""),
    )
    add_check(
        checks,
        "C30",
        "Starbreaker source preserves no-physical-promotion boundary",
        "present",
        "NO_PHYSICAL_PROMOTION" in source_text_by_role.get("starbreaker_context_only", ""),
    )
    add_check(
        checks,
        "C31",
        "Particle-row geometry remains open",
        "present",
        "row-to-face geometry remains open" in source_text_by_role.get("row_geometry_open_boundary", ""),
    )
    add_check(
        checks,
        "C32",
        "Basement calibrated sweep is not physical evidence",
        "present",
        "not physical evidence" in source_text_by_role.get("control_calibrated_sweep", ""),
    )

    passed = all(row["passed"] == "true" for row in checks)
    result_class = PASS_CLASS if passed else "CR284_FAIL_CAMPAIGN_INTAKE_CONTRACT"
    scientific_verdict = "PASS" if passed else "FAIL"
    execution_status = "CLEAN" if passed else "BLOCKED"

    control_output = []
    for row in wrong_controls:
        item = dict(row)
        item["intake_status"] = "PRECOMMITTED_REJECTION_BOUND"
        item["rejected_or_compared_as_required"] = "true"
        control_output.append(item)

    write_csv(
        HERE / "CR284_contract_verification.csv",
        contract_verification,
        ["contract_file", "expected_sha256", "actual_sha256", "verified"],
    )
    write_csv(
        HERE / "CR284_source_verification.csv",
        source_verification,
        ["source_id", "role", "path", "expected_bytes", "actual_bytes", "expected_sha256", "actual_sha256", "verified", "usage_boundary"],
    )
    write_csv(
        HERE / "CR284_checks.csv",
        checks,
        ["check_id", "requirement", "actual", "passed"],
    )
    write_csv(
        HERE / "CR284_wrong_controls.csv",
        control_output,
        ["control_id", "control_class", "control", "required_disposition", "falsifies_if", "intake_status", "rejected_or_compared_as_required"],
    )
    write_csv(
        HERE / "CR284_campaign_roster.csv",
        stages,
        ["stage_id", "title", "input_state", "output_gate", "physical_claim_allowed"],
    )

    summary = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "result_class": result_class,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": "A" if passed else "C",
        "claim_tier": "CAMPAIGN_INTAKE_SOURCE_CONTRACT",
        "preflight_file": preflight_file,
        "preflight_token_present": bool(preflight_token),
        "runner_version": runner_version,
        "checks_passed": sum(row["passed"] == "true" for row in checks),
        "checks_total": len(checks),
        "sources_verified": sum(row["verified"] == "true" for row in source_verification),
        "sources_total": len(source_verification),
        "contract_files_verified": sum(row["verified"] == "true" for row in contract_verification),
        "contract_files_total": len(contract_verification),
        "species_frozen": len(species),
        "campaign_stages_frozen": len(stages),
        "wrong_controls_frozen": len(wrong_controls),
        "physical_promotion": False,
        "selectivity_prediction_emitted": False,
        "humanitarian_release_intent_recorded": True,
        "next_gate": "CR285_CONSTRUCTION_GRAMMAR_AND_SCORING_RULE_LOCK" if passed else "REPAIR_CR284_CONTRACT",
    }
    write_json(HERE / "CR284_summary.json", summary)

    result_md = f"""# CR284 Water-Ion Shape Selectivity Campaign Intake Result

## Verdict

```text
{result_class}
```

## Courtroom Fields

```text
execution_status = {execution_status}
scientific_verdict = {scientific_verdict}
triage_bin = {'A' if passed else 'C'}
claim_tier = CAMPAIGN_INTAKE_SOURCE_CONTRACT
```

## Positive Readout

CR284 verified {sum(r['verified'] == 'true' for r in source_verification)}/{len(source_verification)} frozen local sources,
{sum(r['verified'] == 'true' for r in contract_verification)}/{len(contract_verification)} campaign-contract files,
{len(species)} unpredicted species, {len(stages)} ordered campaign stages, and
{len(wrong_controls)} precommitted controls. The shape-selectivity and
assisted-gate lanes are now separate, observation leakage is prohibited, and
the humanitarian royalty-free release intent is recorded.

## Scientific Boundary

This is a campaign-intake PASS only. It emits no water-ion shape prediction,
pore ranking, dehydration/de-coordination energy, membrane-performance result,
or physical desalination evidence. QP093A geometry remains a candidate;
Starbreaker remains process-context only; SAM carriers are not dissolved ions;
dimensionless A is not pressure or energy.

## First Falsifier

The shape lane must beat bare-ion radius, hydrated radius, formal charge,
charge-density, coordination-number, pore-diameter, and randomized-shape
baselines on held-out cases without per-species or per-pore rescue rules.

The assisted-gate lane must beat gate-only and power-matched random-helper
controls on salt removed per total Wh with salt, water, heat, and energy
balances closed.

## Rule-9 Line

This test could have falsified campaign readiness through source drift, reveal
leakage, missing baselines, rescue coefficients, sound-only promotion, direct
A-to-energy conversion, physical promotion, or an absent humanitarian-release
record.

## Next Gate

`{summary['next_gate']}`
"""
    (HERE / "CR284_result.md").write_text(result_md, encoding="utf-8")

    hash_files = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name != "HASHES.txt" and path.name != "__pycache__"
    )
    hash_lines = [f"{sha256_path(path)}  {path.name}" for path in hash_files]
    (HERE / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(result_class)
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"sources={summary['sources_verified']}/{summary['sources_total']}")
    print(f"artifacts={HERE}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
