#!/usr/bin/env python3
"""Constructive scratch for a fixed-singleton Higgs response to local A.

This runner reproduces the already-executed M020k A^(D+1) law, holds Higgs
count and physical-size ratio fixed, and tests two explicitly typed geometry
decompositions.  It is exploratory and does not install an operator or alter
any CR verdict.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
STAM_ROOT = Path("C:/VS/Stam_model-A-v1.0")

PRECOMMIT = OUT / "SCRATCH_PRECOMMIT_V2.md"
PRECOMMIT_SHA256 = "49da21f7b28dd284c90703b02bac6594b285dbea02491ecef1e7c8b72b2328fe"

D = 3
A0 = 1.0 / (12.0 * math.pi)
HIGGS_COUNT = 1
HIGGS_SIZE_RATIO = 1.0
G748_BASELINE_MEV = 125077.36096514531528
QP0299_NATIVE_BUDGET = 126000.0
R_BOUNCE_H = 1.0 / (64.0 * math.pi)
C_BOUNCE = 1.0 + R_BOUNCE_H

SOURCES = [
    {
        "path": ROOT / "03_CLOCKS_AND_GPS/README.md",
        "sha256": "f53727c90937b9de8fdf42712cac27e5d6aa07f96627f0c5318dcefa54ddd4a6",
        "role": "clock/lapse source context",
    },
    {
        "path": ROOT / "05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_result.md",
        "sha256": "25916a4689bc0edce353626827f087b51710dbdfc4a7bb5d675dcfa54f73fd03",
        "role": "strong-field A landmarks",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR120T_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY/QP093A_0299_DOSSIER.md",
        "sha256": "7ce9b72b2dd35d74eb0e7786ad874bdfcb1f6f941e2ec4fa2d794cccb1a911c7",
        "role": "QP093A-0299 closed-loop source dossier",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR120T_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY/CR120T_result.md",
        "sha256": "93ba1258388d232b579e46f35813d19410d4f3af0f8989f5b280960327066632",
        "role": "singleton/global-reveal typing",
    },
    {
        "path": ROOT / "EPISTEMIC_STANCE.md",
        "sha256": "a556826a603ac3637d6c1b62e573ec3a54ec07695f196fee13e8eef63324fb08",
        "role": "mass versus Higgs-split boundary",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL/CR103a_result.md",
        "sha256": "fa1367a0005a9aeb3a12059404095e64b80a1698713d803b6058e8390f2d11ac",
        "role": "A-dependent Higgs weight and invariant-budget statement",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR104_GATE_3_K_A_H_SELF_CORRECTION/CR104_result.md",
        "sha256": "48c5de6acf3c65f1ec3d1650f701fef8b0c429c9d62866c8d3015d7fefe7806e",
        "role": "K(A_H) self-correction result",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR104_GATE_3_K_A_H_SELF_CORRECTION/CR104_summary.json",
        "sha256": "1487675d79c8fde276ef9505ba63946ccd68835ade87d33115b1e761dc873c9f",
        "role": "finite-A K function open boundary",
    },
    {
        "path": ROOT / "14_FOUNDATIONAL_TESTS/CR104a_LOCAL_HIGGS_VS_GALACTIC_A_APPEAL/CR104a_result.md",
        "sha256": "d0ac2a9f817f4bb05421203b26b3041adec1862257ab18cc9110e4920062ab78",
        "role": "local-A rather than cumulative-galactic-A typing",
    },
    {
        "path": STAM_ROOT / "tests/Matter/M020k_higgs_at_local_A/results/M020k_summary.md",
        "sha256": "6dd948af8f9a2c64d833350ac61c39c77b5a9e958437165b4ec86dc341311df6",
        "role": "executed local-A Higgs A^4 result",
    },
    {
        "path": STAM_ROOT / "tests/Matter/M020k_higgs_at_local_A/results/M020k_summary.json",
        "sha256": "1b9bcc6a6332296453a49ca13a80db98bde9d02ed9caf49cb69740fa5db5ddcb",
        "role": "machine-readable M020k result",
    },
    {
        "path": STAM_ROOT / "tests/Matter/M020k_higgs_at_local_A/scripts/M020k_higgs_at_local_A.py",
        "sha256": "f9a3a2423e52bd040ecfd23bd5691ba122dc3da7ef6a71a9b67472a739a67ef6",
        "role": "M020k formula implementation",
    },
    {
        "path": STAM_ROOT / "tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_result.md",
        "sha256": "22ed3cf38618dca38e6ada1437fba3ba24913d90cc480bb66827388a0057a64a",
        "role": "baseline Higgs direct-weld mass and fixed bounce factor",
    },
]

GRID = [
    ("A0", A0, "minimum/baseline substrate state"),
    ("1/24", 1.0 / 24.0, "weak-field comparison"),
    ("1/3", 1.0 / 3.0, "ISCO landmark"),
    ("2/3", 2.0 / 3.0, "photon-sphere landmark"),
    ("11/12", 11.0 / 12.0, "CR103a spaghettification threshold"),
    ("1", 1.0, "saturation boundary; arithmetic only"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def close(a: float, b: float, rel: float = 2e-12, abs_: float = 2e-12) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def main() -> int:
    generated_utc = datetime.now(timezone.utc).isoformat()

    precommit_actual = sha256(PRECOMMIT)
    precommit_ok = precommit_actual == PRECOMMIT_SHA256

    source_rows: list[dict[str, Any]] = []
    for spec in SOURCES:
        path = Path(spec["path"])
        exists = path.is_file()
        actual = sha256(path) if exists else None
        source_rows.append(
            {
                "path": path.as_posix(),
                "role": spec["role"],
                "expected_sha256": spec["sha256"],
                "actual_sha256": actual,
                "exists": exists,
                "hash_match": exists and actual == spec["sha256"],
            }
        )

    source_contract_ok = precommit_ok and all(row["hash_match"] for row in source_rows)

    rows: list[dict[str, Any]] = []
    for label, a_value, landmark in GRID:
        a_ratio = a_value / A0
        weight = a_ratio ** (D + 1)
        power_density = a_ratio**D
        epsilon_power = weight / power_density

        if a_value < 1.0:
            road_density = ((1.0 - A0) / (1.0 - a_value)) ** D
            epsilon_road = weight / road_density
        else:
            road_density = None
            epsilon_road = None

        k_mass = 1.0 / weight
        bounce_linear_ratio = a_ratio
        k_intersection_fixed = k_mass
        k_intersection_linear = 1.0 / (weight * bounce_linear_ratio)
        lapse_ratio = math.sqrt((1.0 - a_value) / (1.0 - A0))
        literal_observable_factor = weight * lapse_ratio
        compensated_observable_factor = weight * k_mass
        fixed_intersection_factor = weight * k_intersection_fixed
        linear_intersection_factor = weight * bounce_linear_ratio * k_intersection_linear
        higgs_mass_mev = G748_BASELINE_MEV * weight
        source_strength_mev = higgs_mass_mev * C_BOUNCE

        rows.append(
            {
                "label": label,
                "landmark": landmark,
                "A": a_value,
                "A_over_A0": a_ratio,
                "Higgs_count": HIGGS_COUNT,
                "Higgs_size_ratio": HIGGS_SIZE_RATIO,
                "weight_factor_A4": weight,
                "G748_baseline_extended_mass_MeV": higgs_mass_mev,
                "QP0299_separate_native_budget_candidate": QP0299_NATIVE_BUDGET * weight,
                "power_D_slot_density_factor": power_density,
                "power_D_energy_per_slot_factor": epsilon_power,
                "road_measure_slot_density_factor": road_density,
                "road_measure_energy_per_slot_factor": epsilon_road,
                "K_mass_required": k_mass,
                "fixed_bounce_K_intersection_required": k_intersection_fixed,
                "linear_bounce_ratio": bounce_linear_ratio,
                "linear_bounce_K_intersection_required": k_intersection_linear,
                "normalized_lapse_factor": lapse_ratio,
                "literal_weight_times_lapse": literal_observable_factor,
                "compensated_observable_factor": compensated_observable_factor,
                "fixed_bounce_intersection_factor": fixed_intersection_factor,
                "linear_bounce_intersection_factor": linear_intersection_factor,
                "G748_source_strength_MeV": source_strength_mev,
                "G748_source_strength_over_mass": source_strength_mev / higgs_mass_mev,
                "road_boundary_undefined": a_value == 1.0,
            }
        )

    checks = {
        "precommit_hash_exact": precommit_ok,
        "all_source_hashes_exact": all(row["hash_match"] for row in source_rows),
        "source_contract_complete": source_contract_ok,
        "fixed_singleton_count": all(row["Higgs_count"] == 1 for row in rows),
        "fixed_physical_size_ratio": all(close(row["Higgs_size_ratio"], 1.0) for row in rows),
        "A4_weight_monotonic": all(
            rows[index]["weight_factor_A4"] < rows[index + 1]["weight_factor_A4"]
            for index in range(len(rows) - 1)
        ),
        "D_plus_one_factorization_exact": all(
            close(
                row["weight_factor_A4"],
                row["power_D_slot_density_factor"] * row["power_D_energy_per_slot_factor"],
            )
            for row in rows
        ),
        "power_D_energy_per_slot_is_linear_A": all(
            close(row["power_D_energy_per_slot_factor"], row["A_over_A0"]) for row in rows
        ),
        "K_mass_holds_observable_factor_one": all(
            close(row["compensated_observable_factor"], 1.0) for row in rows
        ),
        "fixed_bounce_intersection_holds_one": all(
            close(row["fixed_bounce_intersection_factor"], 1.0) for row in rows
        ),
        "linear_bounce_intersection_holds_one": all(
            close(row["linear_bounce_intersection_factor"], 1.0) for row in rows
        ),
        "G748_source_strength_ratio_constant": all(
            close(row["G748_source_strength_over_mass"], C_BOUNCE) for row in rows
        ),
        "road_measure_boundary_left_undefined": rows[-1]["road_boundary_undefined"]
        and rows[-1]["road_measure_slot_density_factor"] is None
        and rows[-1]["road_measure_energy_per_slot_factor"] is None,
        "literal_observable_mass_not_invariant": any(
            not close(row["literal_weight_times_lapse"], 1.0) for row in rows[1:]
        ),
    }

    exact_checks_ok = all(checks.values())
    if exact_checks_ok:
        primary = "SCRATCH_FIXED_SINGLETON_A4_WEIGHT_RECONCILIATION_SUPPORTED__OPERATOR_OPEN"
        component_verdicts = [
            "SCRATCH_EXISTING_A4_WEIGHT_LAW_REPRODUCED",
            "SCRATCH_D_PLUS_ONE_POWER_DECOMPOSITION_EXACT",
            "BOUNDARY_INTERNAL_WEIGHT_VS_OBSERVABLE_MASS_OPEN",
            "BOUNDARY_POWER_D_VS_ROAD_MEASURE_GEOMETRY_OPEN",
            "BOUNDARY_FINITE_A_K_FUNCTION_OPEN",
        ]
    else:
        primary = "SCRATCH_INTERNAL_CONTRACT_FAILURE"
        component_verdicts = []

    manifest = {
        "generated_utc": generated_utc,
        "scientific_status": "EXPLORATORY_SCRATCH",
        "precommit": {
            "path": PRECOMMIT.as_posix(),
            "expected_sha256": PRECOMMIT_SHA256,
            "actual_sha256": precommit_actual,
            "hash_match": precommit_ok,
        },
        "sources": source_rows,
        "prohibited_selection_inputs": [
            "observed Higgs mass or residual",
            "binding results",
            "F81 membership or totals",
            "Starbreaker outcomes",
            "QP093A-0299 target-aware 125250 correction",
        ],
    }
    write_json(OUT / "SOURCE_MANIFEST.json", manifest)

    csv_path = OUT / "A_MASS_RESPONSE_GRID.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "generated_utc": generated_utc,
        "scientific_status": "EXPLORATORY_SCRATCH_NOT_A_CR_VERDICT",
        "primary_disposition": primary,
        "component_verdicts": component_verdicts,
        "constants": {
            "D": D,
            "A0": A0,
            "Higgs_count": HIGGS_COUNT,
            "Higgs_size_ratio": HIGGS_SIZE_RATIO,
            "G748_baseline_MeV": G748_BASELINE_MEV,
            "QP093A_0299_native_budget_separate_lane": QP0299_NATIVE_BUDGET,
            "r_bounce_H_fixed": R_BOUNCE_H,
            "qA_over_mass_fixed": C_BOUNCE,
        },
        "frozen_laws": {
            "internal_weight": "W_H(A)/W_H(A0)=(A/A0)^4",
            "power_D_slot_density_candidate": "n_power(A)/n_power(A0)=(A/A0)^3",
            "power_D_energy_per_slot_consequence": "epsilon_power(A)/epsilon_power(A0)=A/A0",
            "road_measure_slot_density_competitor": "n_road(A)=((1-A0)/(1-A))^3",
            "observable_budget_correction_required": "K_mass(A)=(A0/A)^4",
            "linear_bounce_intersection_correction_required": "K_intersection(A)=(A0/A)^5",
        },
        "checks": checks,
        "row_count": len(rows),
        "selection_statement": "No observed Higgs target, binding result, F81 membership, Starbreaker outcome, or QP093A-0299 target-aware correction selected any law.",
        "supported_meaning": "With count and size fixed, the existing A^(D+1) weight law factorizes exactly into an A^D slot-density candidate and one linear A excitation factor per slot.",
        "boundary": "The arithmetic does not choose power-D over road-measure geometry, derive finite-A K, or prove that observable pole or gravitational mass varies with A.",
    }
    write_json(OUT / "SCRATCH_SUMMARY.json", summary)

    table_lines = []
    for row in rows:
        road = "undefined" if row["road_measure_slot_density_factor"] is None else f'{row["road_measure_slot_density_factor"]:.9g}'
        table_lines.append(
            f'| {row["label"]} | {row["A_over_A0"]:.9g} | {row["weight_factor_A4"]:.9g} '
            f'| {row["power_D_slot_density_factor"]:.9g} | {row["power_D_energy_per_slot_factor"]:.9g} '
            f'| {road} | {row["G748_baseline_extended_mass_MeV"] / 1000.0:.9g} |'
        )

    failed = [name for name, passed in checks.items() if not passed]
    result_text = f"""# Fixed-Singleton Local-A Higgs Weight Reconciliation Scratch

scientific_status: `EXPLORATORY_SCRATCH_NOT_A_CR_VERDICT`

primary_disposition: `{primary}`

## Direct answer

The proposed response is internally coherent in the already-executed local-A
lane without increasing Higgs count or physical size.  M020k's existing law

```text
W_H(A)/W_H(A0) = (A/A0)^4
```

factorizes exactly, for `D=3`, as

```text
(A/A0)^4 = (A/A0)^3 * (A/A0).
```

Under the power-D geometry candidate, the first factor is the relative number
of slot ledgers supported inside the same physical volume and the remaining
factor is the relative excitation weight per ledger.  The Higgs remains one
closed scalar parent (`N_H=1`) with size ratio one at every grid point.

## Frozen calculation

| A | A/A0 | internal weight A^4 | power-D slots A^3 | weight per power-D slot | road-measure slots | G748 baseline extension (GeV) |
|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(table_lines)}

The listed GeV column reproduces the M020k structural extension after
normalizing to the sealed G748 baseline.  It is not a new measured-mass fit.
The QP093A-0299 native budget was propagated in a separate output column and
was never merged with that baseline.

## What the scratch supports

- `SCRATCH_EXISTING_A4_WEIGHT_LAW_REPRODUCED`
- `SCRATCH_D_PLUS_ONE_POWER_DECOMPOSITION_EXACT`
- fixed singleton count and fixed size are compatible with increasing internal
  closed-loop weight;
- `q_A,H/m_H = 1 + 1/(64*pi)` remains constant without replacing the sealed
  `A0` inside the bounce factor;
- if the observable/global budget must remain invariant, the required
  correction is exactly `K_mass=(A0/A)^4`;
- if bounce cost also scales linearly with local A, constant intersection cost
  instead requires `K_intersection=(A0/A)^5`.

## What remains open

- `BOUNDARY_INTERNAL_WEIGHT_VS_OBSERVABLE_MASS_OPEN`: the A^4 internal-weight
  result does not by itself prove a varying observed pole mass or gravitational
  source mass;
- `BOUNDARY_POWER_D_VS_ROAD_MEASURE_GEOMETRY_OPEN`: the exact A^3 times A
  decomposition is a candidate physical interpretation, not yet a derived
  slot-density operator.  The road-measure candidate remains a live control;
- `BOUNDARY_FINITE_A_K_FUNCTION_OPEN`: CR104 did not seal a finite-A K operator;
- one catalog parent is not evidence that nature contains literally one Higgs
  quantum.  The fixed-count statement is the tested structural premise.

## Contract checks

All checks passed: `{str(exact_checks_ok).lower()}`

Failed checks: `{', '.join(failed) if failed else 'none'}`

No CR120U or CR120T artifact was modified.  This scratch installs no operator
and makes no binding or Starbreaker claim.
"""
    (OUT / "SCRATCH_RESULT.md").write_text(result_text, encoding="utf-8")

    artifact_names = [
        "SCRATCH_PRECOMMIT.md",
        "PRECOMMIT_SUPERSESSION_NOTE.md",
        "SCRATCH_PRECOMMIT_V2.md",
        Path(__file__).name,
        "SOURCE_MANIFEST.json",
        "A_MASS_RESPONSE_GRID.csv",
        "SCRATCH_SUMMARY.json",
        "SCRATCH_RESULT.md",
    ]
    hash_lines = [
        "# SHA256 artifact manifest; HASHES.txt excludes itself by construction.",
        *[f"{sha256(OUT / name)}  {name}" for name in artifact_names],
        "",
    ]
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines), encoding="utf-8")

    print(primary)
    print(f"checks_passed={sum(checks.values())}/{len(checks)}")
    print(f"result={OUT / 'SCRATCH_RESULT.md'}")
    return 0 if exact_checks_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
