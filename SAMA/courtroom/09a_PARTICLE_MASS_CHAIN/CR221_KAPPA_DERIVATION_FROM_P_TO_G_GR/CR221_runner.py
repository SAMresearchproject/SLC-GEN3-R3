from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR"

CR220 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION"
CR220_COMPONENTS = CR220 / "CR220_component_selector.csv"
CR220_ELEMENTS = CR220 / "CR220_simulated_element_primary_rows_126.csv"
CR220_SUMMARY = CR220 / "CR220_summary.json"
CR119_PERIODIC = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_courtroom_periodic_table.csv"

PRECOMMIT = OUT / "CR221_PRECOMMIT.md"
RUNNER = OUT / "CR221_runner.py"
INPUT_MANIFEST = OUT / "CR221_input_manifest.csv"
KERNEL_TERMS = OUT / "CR221_kernel_terms.csv"
KAPPA_ROWS = OUT / "CR221_element_kappa_rows_126.csv"
CHECKS = OUT / "CR221_checks.csv"
SUMMARY = OUT / "CR221_summary.json"
RESULT = OUT / "CR221_result.md"
HASHES = OUT / "HASHES.txt"

EIGHT = Fraction(8, 1)


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


def manifest_row(path: Path, role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "source": rel(path),
        "exists": str(exists),
        "bytes": path.stat().st_size if exists and path.is_file() else "",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
        "role": role,
    }


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append(
        {
            "check": name,
            "passed": str(bool(passed)),
            "observed": observed,
            "expected": expected,
        }
    )


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in paths:
        if path.exists() and path.is_file():
            lines.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dec_fraction(text: str, max_denominator: int = 1_000_000) -> Fraction:
    return Fraction(Decimal(str(text).strip())).limit_denominator(max_denominator)


def fdec(value: Fraction) -> str:
    return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def fstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    source_paths = [
        (CR220_COMPONENTS, "CR220 component qA source terms"),
        (CR220_ELEMENTS, "CR220 P-centered 126 element rows"),
        (CR220_SUMMARY, "CR220 summary and boundary"),
        (CR119_PERIODIC, "CR119 comparison surface"),
    ]
    write_csv(
        INPUT_MANIFEST,
        [manifest_row(path, role) for path, role in source_paths],
        ["source", "exists", "bytes", "sha256", "role"],
    )

    _, component_rows = read_csv(CR220_COMPONENTS)
    _, element_rows = read_csv(CR220_ELEMENTS)
    cr220_summary = read_json(CR220_SUMMARY) if CR220_SUMMARY.exists() else {}

    components = {row["component_role"]: row for row in component_rows}
    proton_qA = dec_fraction(components["proton_write"]["qA_source_support"])
    neutron_qA = dec_fraction(components["neutron_write"]["qA_source_support"])
    electron_qA = dec_fraction(components["electron_write"]["qA_source_support"])

    charged_pair_qA = proton_qA + electron_qA
    charged_pair_G_per_Z = charged_pair_qA / EIGHT
    neutron_G_unit = neutron_qA / EIGHT
    kappa_floor = (proton_qA + electron_qA + neutron_qA) / EIGHT

    kernel_rows = [
        {
            "term": "proton_qA",
            "source_component": components["proton_write"]["source_candidate_id"],
            "fraction": fstr(proton_qA),
            "decimal": fdec(proton_qA),
            "role": "selected proton write qA support",
        },
        {
            "term": "electron_qA",
            "source_component": components["electron_write"]["source_candidate_id"],
            "fraction": fstr(electron_qA),
            "decimal": fdec(electron_qA),
            "role": "selected electron write qA support",
        },
        {
            "term": "neutron_qA",
            "source_component": components["neutron_write"]["source_candidate_id"],
            "fraction": fstr(neutron_qA),
            "decimal": fdec(neutron_qA),
            "role": "selected neutron write qA support",
        },
        {
            "term": "charged_pair_qA_per_Z",
            "source_component": "proton_write + electron_write",
            "fraction": fstr(charged_pair_qA),
            "decimal": fdec(charged_pair_qA),
            "role": "GR contribution per Z before neutron contribution",
        },
        {
            "term": "charged_pair_G_per_Z",
            "source_component": "(proton_qA + electron_qA) / 8",
            "fraction": fstr(charged_pair_G_per_Z),
            "decimal": fdec(charged_pair_G_per_Z),
            "role": "G contribution per Z before neutron contribution",
        },
        {
            "term": "neutron_G_unit",
            "source_component": "neutron_qA / 8",
            "fraction": fstr(neutron_G_unit),
            "decimal": fdec(neutron_G_unit),
            "role": "G contribution per neutron",
        },
        {
            "term": "kappa_floor",
            "source_component": "(proton_qA + electron_qA + neutron_qA) / 8",
            "fraction": fstr(kappa_floor),
            "decimal": fdec(kappa_floor),
            "role": "fixed floor kappa for N=Z element rows",
        },
    ]
    write_csv(KERNEL_TERMS, kernel_rows, ["term", "source_component", "fraction", "decimal", "role"])

    kappa_rows: list[dict[str, Any]] = []
    for row in element_rows:
        z = int(row["Z"])
        n = int(row["N"])
        g_observed = dec_fraction(row["G_tensor_computed"], max_denominator=10_000_000)
        gr_observed = dec_fraction(row["GR_qA_total_computed"], max_denominator=10_000_000)
        neutron_excess = n - z
        neutron_excess_term = Fraction(neutron_excess, 1) * neutron_G_unit
        g_from_floor = Fraction(z, 1) * kappa_floor + neutron_excess_term
        gr_from_floor = EIGHT * g_from_floor
        kappa_eff = g_from_floor / Fraction(z, 1)
        kappa_eff_direct = g_observed / Fraction(z, 1)
        kappa_delta_from_floor = kappa_eff - kappa_floor
        kappa_rows.append(
            {
                "Z": z,
                "N": n,
                "A": row["A"],
                "P_address": row["P_address"],
                "G_CR220": row["G_tensor_computed"],
                "GR_CR220": row["GR_qA_total_computed"],
                "kappa_floor_fraction": fstr(kappa_floor),
                "kappa_floor_decimal": fdec(kappa_floor),
                "neutron_excess_N_minus_Z": neutron_excess,
                "neutron_excess_term_fraction": fstr(neutron_excess_term),
                "neutron_excess_term_decimal": fdec(neutron_excess_term),
                "G_from_Z_kappa_floor_plus_excess_fraction": fstr(g_from_floor),
                "G_from_Z_kappa_floor_plus_excess_decimal": fdec(g_from_floor),
                "GR_from_formula_fraction": fstr(gr_from_floor),
                "GR_from_formula_decimal": fdec(gr_from_floor),
                "kappa_effective_fraction": fstr(kappa_eff),
                "kappa_effective_decimal": fdec(kappa_eff),
                "kappa_delta_from_floor_fraction": fstr(kappa_delta_from_floor),
                "kappa_delta_from_floor_decimal": fdec(kappa_delta_from_floor),
                "formula_matches_G": str(g_from_floor == g_observed),
                "formula_matches_GR": str(gr_from_floor == gr_observed),
                "kappa_eff_matches_G_over_Z": str(kappa_eff == kappa_eff_direct),
                "kappa_kind": "floor_constant" if neutron_excess == 0 else "effective_element_quotient",
            }
        )

    fields = [
        "Z",
        "N",
        "A",
        "P_address",
        "G_CR220",
        "GR_CR220",
        "kappa_floor_fraction",
        "kappa_floor_decimal",
        "neutron_excess_N_minus_Z",
        "neutron_excess_term_fraction",
        "neutron_excess_term_decimal",
        "G_from_Z_kappa_floor_plus_excess_fraction",
        "G_from_Z_kappa_floor_plus_excess_decimal",
        "GR_from_formula_fraction",
        "GR_from_formula_decimal",
        "kappa_effective_fraction",
        "kappa_effective_decimal",
        "kappa_delta_from_floor_fraction",
        "kappa_delta_from_floor_decimal",
        "formula_matches_G",
        "formula_matches_GR",
        "kappa_eff_matches_G_over_Z",
        "kappa_kind",
    ]
    write_csv(KAPPA_ROWS, kappa_rows, fields)

    kind_counts = dict(Counter(row["kappa_kind"] for row in kappa_rows))
    unique_eff = len({row["kappa_effective_fraction"] for row in kappa_rows})
    checks: list[dict[str, Any]] = []
    check(checks, "inputs_exist", all(path.exists() for path, _ in source_paths), True, True)
    check(checks, "cr220_rows_126", len(element_rows) == 126, len(element_rows), 126)
    check(checks, "proton_qA_fraction_145_over_2", proton_qA == Fraction(145, 2), fstr(proton_qA), "145/2")
    check(checks, "electron_qA_fraction_145_over_96", electron_qA == Fraction(145, 96), fstr(electron_qA), "145/96")
    check(checks, "neutron_qA_fraction_1_over_8", neutron_qA == Fraction(1, 8), fstr(neutron_qA), "1/8")
    check(checks, "charged_pair_qA_7105_over_96", charged_pair_qA == Fraction(7105, 96), fstr(charged_pair_qA), "7105/96")
    check(checks, "kappa_floor_7117_over_768", kappa_floor == Fraction(7117, 768), fstr(kappa_floor), "7117/768")
    check(checks, "neutron_G_unit_1_over_64", neutron_G_unit == Fraction(1, 64), fstr(neutron_G_unit), "1/64")
    check(checks, "all_G_formula_matches", all(row["formula_matches_G"] == "True" for row in kappa_rows), sum(row["formula_matches_G"] == "True" for row in kappa_rows), 126)
    check(checks, "all_GR_formula_matches", all(row["formula_matches_GR"] == "True" for row in kappa_rows), sum(row["formula_matches_GR"] == "True" for row in kappa_rows), 126)
    check(checks, "all_kappa_eff_matches_G_over_Z", all(row["kappa_eff_matches_G_over_Z"] == "True" for row in kappa_rows), sum(row["kappa_eff_matches_G_over_Z"] == "True" for row in kappa_rows), 126)
    check(checks, "fixed_floor_rows_12", kind_counts.get("floor_constant", 0) == 12, kind_counts.get("floor_constant", 0), 12)
    check(checks, "effective_quotient_rows_114", kind_counts.get("effective_element_quotient", 0) == 114, kind_counts.get("effective_element_quotient", 0), 114)
    check(checks, "kappa_eff_not_single_global_constant", unique_eff > 1, unique_eff, ">1")
    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])

    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"

    gold = next(row for row in kappa_rows if str(row["Z"]) == "79")
    hydrogen = next(row for row in kappa_rows if str(row["Z"]) == "1")
    summary = {
        "cr_id": "CR221",
        "artifact": "CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR",
        "execution_status": execution_status,
        "generated_at_utc": utc_now(),
        "preflight_file": os.environ.get("SAM_PREFLIGHT_FILE", ""),
        "result_class": (
            "CR221_PASS_KAPPA_DERIVATION_FROM_P_TO_G_GR__"
            "KAPPA_FLOOR_7117_OVER_768__G_EQUALS_Z_KAPPA_FLOOR_PLUS_N_MINUS_Z_OVER_64__"
            "KAPPA_EFF_IS_ELEMENT_QUOTIENT_NOT_SINGLE_GLOBAL_HEAVY_ELEMENT_CONSTANT"
        )
        if execution_status == "CLEAN"
        else "CR221_FAIL_KAPPA_DERIVATION_FROM_P_TO_G_GR",
        "component_fractions": {
            "proton_qA": fstr(proton_qA),
            "electron_qA": fstr(electron_qA),
            "neutron_qA": fstr(neutron_qA),
            "charged_pair_qA": fstr(charged_pair_qA),
            "charged_pair_G_per_Z": fstr(charged_pair_G_per_Z),
            "neutron_G_unit": fstr(neutron_G_unit),
            "kappa_floor": fstr(kappa_floor),
        },
        "component_decimals": {
            "proton_qA": fdec(proton_qA),
            "electron_qA": fdec(electron_qA),
            "neutron_qA": fdec(neutron_qA),
            "charged_pair_qA": fdec(charged_pair_qA),
            "charged_pair_G_per_Z": fdec(charged_pair_G_per_Z),
            "neutron_G_unit": fdec(neutron_G_unit),
            "kappa_floor": fdec(kappa_floor),
        },
        "row_counts": {
            "rows": len(kappa_rows),
            "kappa_kind_counts": kind_counts,
            "unique_kappa_effective_values": unique_eff,
        },
        "hydrogen": hydrogen,
        "gold": gold,
        "cr220_boundary": cr220_summary.get("boundary", ""),
        "checks_passed": passed,
        "checks_total": len(checks),
        "boundary": (
            "A floor kappa is now derived from the selected component writes. "
            "For general P, the correct kernel is kappa_eff(P)=G(P)/Z; it varies "
            "with N/Z. Heavy elements require the neutron-excess term and should "
            "not be reduced to G=Z*kappa_floor alone."
        ),
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR221 Kappa Derivation From P To G/GR

Result: **{summary['result_class']}**

## Direct Answer

Yes, `kappa` is now derivable from the P-centered component writes, but with an
important split:

```text
kappa_floor = (proton_qA + electron_qA + neutron_qA) / 8
            = (145/2 + 145/96 + 1/8) / 8
            = 7117/768
            = {fdec(kappa_floor)}
```

That floor value is exact for rows where `N = Z`.

For general element rows, the live kernel is an effective quotient:

```text
kappa_eff(P) = G(P) / Z
             = 7105/768 + (N/Z) * 1/64
```

or, equivalently:

```text
G(P) = Z * (7117/768) + (N - Z) / 64
```

## Gold Row

For `Z=79`, `N=118`:

```text
G(P) = 79 * 7117/768 + 39/64
     = {gold['G_from_Z_kappa_floor_plus_excess_decimal']}

kappa_eff(P) = G(P)/79
             = {gold['kappa_effective_fraction']}
             = {gold['kappa_effective_decimal']}
```

That is why the current Courtroom value is:

```text
G(P)  = {gold['G_from_Z_kappa_floor_plus_excess_decimal']}
GR(P) = {gold['GR_from_formula_decimal']}
```

## What Changed

Before CR220, `kappa` was only a displayed/card-style coefficient. After CR220
and CR221, the coefficient is decomposed into component-write terms:

- proton qA = `145/2`
- electron qA = `145/96`
- neutron qA = `1/8`
- `G` carrier split = divide by `8`

The fixed floor kappa is therefore backed. The heavy-element kernel is not a
single global constant; it is the floor kappa plus the native neutron-excess
term.

## Checks

- 126/126 rows satisfy `G(P) = Z*kappa_floor + (N-Z)/64`.
- 126/126 rows satisfy `GR(P) = 8G(P)`.
- 126/126 rows satisfy `kappa_eff(P) = G(P)/Z`.
- 12 rows have the floor constant exactly (`N=Z`).
- 114 rows use an element-specific effective quotient.

## Boundary

This does not use element cards or known labels. It uses CR220 component writes
and CR220 P-centered element rows. The correct current reading is:

```text
kappa_floor is derived.
kappa_eff(P) is derived row by row.
G(P) = Z*kappa_floor alone is only valid where N=Z.
```

## Artifacts

- `{rel(KERNEL_TERMS)}`
- `{rel(KAPPA_ROWS)}`
- `{rel(INPUT_MANIFEST)}`
- `{rel(CHECKS)}`
- `{rel(SUMMARY)}`
- `{rel(HASHES)}`
"""
    RESULT.write_text(result_text, encoding="utf-8")

    write_hashes([PRECOMMIT, RUNNER, INPUT_MANIFEST, KERNEL_TERMS, KAPPA_ROWS, CHECKS, SUMMARY, RESULT])
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())

