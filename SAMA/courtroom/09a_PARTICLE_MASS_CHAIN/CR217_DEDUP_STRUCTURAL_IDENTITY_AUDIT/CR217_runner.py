from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 200


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR217_DEDUP_STRUCTURAL_IDENTITY_AUDIT"

INPUT_ACTIVE = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR216_CARRIER_DUPLICATE_RETIREMENT"
    / "CR216_particle_complement_194_active.csv"
)
INPUT_SEALED_195 = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
    / "CR214_particle_complement_195.csv"
)
INPUT_DUP_GROUPS = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT"
    / "CR215_numeric_duplicate_groups.csv"
)
INPUT_RETIREMENT = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR216_CARRIER_DUPLICATE_RETIREMENT"
    / "CR216_retirement_ledger.csv"
)
INPUT_CR060A = (
    ROOT / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH"
    / "CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1"
    / "CR060a_result.md"
)
INPUT_CR066A = (
    ROOT / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH"
    / "CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1"
    / "CR066a_runner.py"
)
INPUT_LC11 = (
    ROOT / "16_THE_LAST_CAMPAIGN"
    / "LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY"
    / "LC11_formula_manifest.csv"
)

SEALED_HASHES = {
    INPUT_SEALED_195:  "e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545",
    INPUT_DUP_GROUPS:  "8d8f0461d2e54df89a57cc1d16a886efa792fa8b900c38b0c083c717bc8d8f98",
    INPUT_ACTIVE:      "01e780c0fbb315d0aaf93cc6b060ffc4c9cfd0da29ab7155b4da8ca40d444179",
    INPUT_RETIREMENT:  "c85b1b766435c33504ad6004f44f9aef35cf95614a78216f164b3d9ab0647610",
    INPUT_CR060A:      "4ac273e8ca5539876886550590cdf7d81b776108fdef1ed9eba1adf8105d6ee8",
    INPUT_CR066A:      "3672beb257ea228c7f991bb33922db3e060e445a55a3238a113f7804149e24c7",
    INPUT_LC11:        "a0c3eb030a7b55edf0b4fc5a28788a6560e323a4ab17611667979b917dba8069",
}

R = Fraction(12)
R_SQUARED = R * R  # 144
D = 3
TWO_TO_MINUS_D = Fraction(1, 2 ** D)  # 1/8
ONE_PLUS_TWO_MINUS_D = Fraction(1) + TWO_TO_MINUS_D  # 9/8
D_SQUARED_OVER_2D = Fraction(D * D, 2 ** D)  # 9/8

EXPECTED_CARRIERS = {
    "QP093A-0300": {"role": "graviton", "partition": 18, "M_native": 18, "operator_class": "TENSOR_CARRIER"},
    "QP093A-0301": {"role": "photon",   "partition": 1,  "M_native": 0,  "operator_class": "ROAD_LIGHT_CARRIER"},
    "QP093A-0302": {"role": "W",        "partition": 9,  "M_native": 9,  "operator_class": "WEAK_VECTOR_CARRIER"},
    "QP093A-0303": {"role": "Z",        "partition": 81, "M_native": 81, "operator_class": "NEUTRAL_VECTOR_CARRIER"},
    "QP093A-0304": {"role": "gluon",    "partition": 8,  "M_native": 8,  "operator_class": "COLOR_OWNER_CARRIER"},
}

EXPECTED_HIDDEN_P = {1, 2, 3, 4, 6, 8, 9, 12}

# Generous decimal-equality tolerance for sealed strings that may have a
# single-digit rounding tail beyond ~90 places.
MASS_EPSILON = Decimal("1e-80")


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
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


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


def to_decimal(value: str) -> Decimal:
    return Decimal(value.strip())


def fraction_to_decimal(f: Fraction) -> Decimal:
    return Decimal(f.numerator) / Decimal(f.denominator)


def fraction_str(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


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

    # 2. Read the active 194-row complement.
    _, active_rows = read_csv(INPUT_ACTIVE)

    # 3. Extract carrier_only and hidden_source_support blocks.
    carrier_rows = [r for r in active_rows if r.get("bin") == "carrier_only_rows"]
    hidden_rows = [r for r in active_rows if r.get("bin") == "hidden_source_support_rows"]

    # 4. Per-carrier checks.
    carrier_check_rows = []
    carrier_block_ok = True
    for cand_id, expected in EXPECTED_CARRIERS.items():
        row = next((r for r in carrier_rows if r.get("candidate_id") == cand_id), None)
        if row is None:
            carrier_block_ok = False
            carrier_check_rows.append(
                {
                    "candidate_id": cand_id,
                    "role": expected["role"],
                    "expected_operator_class": expected["operator_class"],
                    "observed_operator_class": "MISSING",
                    "expected_partition": expected["partition"],
                    "observed_partition": "MISSING",
                    "expected_M_native": expected["M_native"],
                    "observed_M_native": "MISSING",
                    "match": False,
                }
            )
            continue
        partition_obs = int(row.get("partition_signature", "-1"))
        m_native_obs = to_decimal(row.get("M_native", "0"))
        m_native_expected = Decimal(expected["M_native"])
        op_class_obs = row.get("operator_class", "")
        match = (
            partition_obs == expected["partition"]
            and abs(m_native_obs - m_native_expected) < MASS_EPSILON
            and op_class_obs == expected["operator_class"]
        )
        if not match:
            carrier_block_ok = False
        carrier_check_rows.append(
            {
                "candidate_id": cand_id,
                "role": expected["role"],
                "expected_operator_class": expected["operator_class"],
                "observed_operator_class": op_class_obs,
                "expected_partition": expected["partition"],
                "observed_partition": partition_obs,
                "expected_M_native": expected["M_native"],
                "observed_M_native": str(m_native_obs),
                "match": match,
            }
        )
    write_csv(
        OUT / "CR217_carrier_block.csv",
        carrier_check_rows,
        [
            "candidate_id",
            "role",
            "expected_operator_class",
            "observed_operator_class",
            "expected_partition",
            "observed_partition",
            "expected_M_native",
            "observed_M_native",
            "match",
        ],
    )
    carrier_count_ok = len(carrier_rows) == 5

    # 5. Hidden_source per-row lift check.
    hidden_check_rows = []
    hidden_lifts_ok = True
    observed_hidden_p = []
    hidden_p_set_ok = True
    for row in sorted(hidden_rows, key=lambda r: int(r.get("partition_signature", "0"))):
        p = int(row.get("partition_signature", "0"))
        observed_hidden_p.append(p)
        m_obs = to_decimal(row.get("M_native", "0"))
        m_expected_frac = Fraction(p) + Fraction(p * p, R_SQUARED)
        m_expected_dec = fraction_to_decimal(m_expected_frac)
        diff = m_obs - m_expected_dec
        match = abs(diff) < MASS_EPSILON
        if not match:
            hidden_lifts_ok = False
        hidden_check_rows.append(
            {
                "candidate_id": row.get("candidate_id", ""),
                "partition_p": p,
                "lift_formula": "m(p) = p + p^2/R^2 with R^2=144",
                "expected_M_native_fraction": fraction_str(m_expected_frac),
                "expected_M_native_decimal": str(m_expected_dec),
                "observed_M_native_decimal": str(m_obs),
                "abs_difference": str(abs(diff)),
                "match": match,
            }
        )
    if set(observed_hidden_p) != EXPECTED_HIDDEN_P:
        hidden_p_set_ok = False
    write_csv(
        OUT / "CR217_hidden_source_block.csv",
        hidden_check_rows,
        [
            "candidate_id",
            "partition_p",
            "lift_formula",
            "expected_M_native_fraction",
            "expected_M_native_decimal",
            "observed_M_native_decimal",
            "abs_difference",
            "match",
        ],
    )
    hidden_count_ok = len(hidden_rows) == 8

    # 6. Compute partition and mass sums in exact rational arithmetic.
    graviton_partition = Fraction(EXPECTED_CARRIERS["QP093A-0300"]["partition"])
    carrier_partition_excl_grav = Fraction(0)
    carrier_mass_incl_grav = Fraction(0)
    for cand_id, expected in EXPECTED_CARRIERS.items():
        carrier_mass_incl_grav += Fraction(expected["M_native"])
        if cand_id != "QP093A-0300":
            carrier_partition_excl_grav += Fraction(expected["partition"])
    carrier_partition_incl_grav = carrier_partition_excl_grav + graviton_partition

    hidden_partition_sum = Fraction(0)
    hidden_mass_sum = Fraction(0)
    sum_p_squared_hidden = 0
    sum_p_squared_hidden_sub_R = 0
    for p in sorted(EXPECTED_HIDDEN_P):
        hidden_partition_sum += Fraction(p)
        hidden_mass_sum += Fraction(p) + Fraction(p * p, R_SQUARED)
        sum_p_squared_hidden += p * p
        if p < R.numerator:
            sum_p_squared_hidden_sub_R += p * p

    total_partition = carrier_partition_incl_grav + hidden_partition_sum
    total_mass = carrier_mass_incl_grav + hidden_mass_sum

    # 7. Identity checks.
    checks: list[tuple[str, bool, str, str]] = []  # name, passed, expected, observed

    def check_eq(name: str, observed: Any, expected: Any) -> bool:
        passed = observed == expected
        checks.append((name, passed, str(expected), str(observed)))
        return passed

    check_eq("all_inputs_verified", all_inputs_verified, True)
    check_eq("carrier_count_after_dedup_is_5", carrier_count_ok, True)
    check_eq("hidden_source_count_is_8", hidden_count_ok, True)
    check_eq("carrier_block_per_row_match", carrier_block_ok, True)
    check_eq("hidden_p_set_matches_{1,2,3,4,6,8,9,12}", hidden_p_set_ok, True)
    check_eq("hidden_per_row_lift_match", hidden_lifts_ok, True)

    check_eq("carrier_partition_sum_excl_graviton_eq_99", carrier_partition_excl_grav, Fraction(99))
    check_eq("carrier_partition_sum_incl_graviton_eq_117", carrier_partition_incl_grav, Fraction(117))
    check_eq("hidden_partition_sum_eq_45", hidden_partition_sum, Fraction(45))
    check_eq("total_partition_eq_162", total_partition, Fraction(162))

    check_eq("carrier_mass_sum_incl_graviton_eq_116", carrier_mass_incl_grav, Fraction(116))
    check_eq("hidden_mass_sum_eq_45_plus_355_over_144", hidden_mass_sum, Fraction(45) + Fraction(355, 144))
    check_eq("total_mass_eq_162_plus_211_over_144", total_mass, Fraction(162) + Fraction(211, 144))

    check_eq("99_plus_45_eq_R_squared_144", carrier_partition_excl_grav + hidden_partition_sum, R_SQUARED)
    check_eq("graviton_over_R_squared_eq_1_over_8", graviton_partition / R_SQUARED, Fraction(1, 8))
    check_eq("graviton_over_R_squared_eq_2_to_minus_D", graviton_partition / R_SQUARED, TWO_TO_MINUS_D)
    check_eq("total_partition_over_R_squared_eq_9_over_8", total_partition / R_SQUARED, Fraction(9, 8))
    check_eq("one_plus_2_to_minus_D_eq_9_over_8_at_D3", ONE_PLUS_TWO_MINUS_D, Fraction(9, 8))
    check_eq("D_squared_over_2_to_D_eq_9_over_8_at_D3", D_SQUARED_OVER_2D, Fraction(9, 8))

    check_eq("sum_p_squared_hidden_eq_355", sum_p_squared_hidden, 355)
    check_eq("sum_p_squared_hidden_sub_R_eq_211", sum_p_squared_hidden_sub_R, 211)
    check_eq("mass_excess_over_partition_eq_211_over_144", total_mass - total_partition, Fraction(211, 144))

    # 8. Photon falsifier.
    photon_row = next((r for r in carrier_rows if r.get("candidate_id") == "QP093A-0301"), None)
    photon_partition_eq_1 = photon_row is not None and int(photon_row.get("partition_signature", "0")) == 1
    photon_mass_eq_0 = photon_row is not None and abs(to_decimal(photon_row.get("M_native", "1"))) < MASS_EPSILON
    carrier_partition_minus_carrier_mass_eq_1 = (carrier_partition_incl_grav - carrier_mass_incl_grav) == Fraction(1)
    check_eq("photon_falsifier_partition_eq_1", photon_partition_eq_1, True)
    check_eq("photon_falsifier_M_native_eq_0", photon_mass_eq_0, True)
    check_eq("photon_falsifier_carrier_partition_minus_mass_eq_1", carrier_partition_minus_carrier_mass_eq_1, True)

    # 9. Identity checks output.
    identity_rows = [
        {"check_name": name, "passed": passed, "expected": exp, "observed": obs}
        for name, passed, exp, obs in checks
    ]
    write_csv(
        OUT / "CR217_identity_checks.csv",
        identity_rows,
        ["check_name", "passed", "expected", "observed"],
    )

    # 10. Summary JSON.
    checks_passed = sum(1 for _, p, _, _ in checks if p)
    checks_total = len(checks)
    summary = {
        "cr_id": "CR217",
        "test_id": "CR217_DEDUP_STRUCTURAL_IDENTITY_AUDIT",
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
        "sealed_constants": {
            "R": 12,
            "R_squared": 144,
            "D": 3,
            "two_to_minus_D": "1/8",
            "nine_eighths_appearances_in_sealed_courtroom": [
                "CR060a Paul Revere alphabet: middle-slot 9/8 surcharge on 1/2 weight (turning into 9/16)",
                "CR066a Born extension: 9/8 SURCHARGE on the middle slot",
                "LC11 black hole horizon: bounce lift D^2/2^D = 9/8 at D=3"
            ]
        },
        "partition_sums": {
            "carrier_excl_graviton": str(carrier_partition_excl_grav),
            "carrier_incl_graviton": str(carrier_partition_incl_grav),
            "hidden_source": str(hidden_partition_sum),
            "total": str(total_partition),
        },
        "mass_sums": {
            "carrier_incl_graviton": str(carrier_mass_incl_grav),
            "hidden_source_fraction": fraction_str(hidden_mass_sum),
            "hidden_source_decimal": str(fraction_to_decimal(hidden_mass_sum)),
            "total_fraction": fraction_str(total_mass),
            "total_decimal": str(fraction_to_decimal(total_mass)),
        },
        "structural_identities": {
            "carrier_excl_graviton_plus_hidden_eq_R_squared": (carrier_partition_excl_grav + hidden_partition_sum) == R_SQUARED,
            "graviton_over_R_squared_eq_2_to_minus_D": (graviton_partition / R_SQUARED) == TWO_TO_MINUS_D,
            "total_partition_over_R_squared_eq_9_over_8": (total_partition / R_SQUARED) == Fraction(9, 8),
            "one_plus_2_to_minus_D_eq_9_over_8_at_D3": ONE_PLUS_TWO_MINUS_D == Fraction(9, 8),
            "D_squared_over_2_to_D_eq_9_over_8_at_D3": D_SQUARED_OVER_2D == Fraction(9, 8),
            "mass_excess_over_partition_eq_211_over_144": (total_mass - total_partition) == Fraction(211, 144),
            "sum_p_squared_hidden_eq_355": sum_p_squared_hidden == 355,
            "sum_p_squared_hidden_sub_R_eq_211": sum_p_squared_hidden_sub_R == 211,
        },
        "photon_falsifier": {
            "photon_partition_eq_1": photon_partition_eq_1,
            "photon_M_native_eq_0": photon_mass_eq_0,
            "carrier_partition_minus_carrier_mass_eq_1": carrier_partition_minus_carrier_mass_eq_1,
        },
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "execution_status": "CLEAN" if checks_passed == checks_total else "FAIL",
        "result_class": (
            "CR217_PASS_DEDUP_STRUCTURAL_IDENTITY_AUDIT__"
            "162_EQ_R2_NINE_EIGHTHS__"
            "163.4652778_EQ_162_PLUS_211_OVER_144__"
            "PHOTON_FALSIFIER_HOLDS__"
            "BACKED_ARITHMETIC_NOT_DERIVED_MECHANISM"
            if checks_passed == checks_total
            else "CR217_FAIL"
        ),
        "non_promotion_rule": (
            "162 = R^2 * (9/8) is recorded as a backed identity on sealed inputs. "
            "The structural narrative is recorded as scientific_reading only. "
            "The convergence of 9/8 across CR060a, CR066a, LC11, and CR217 is "
            "recorded as three independent sealed appearances of the same ratio, "
            "not as a unified derivation in this CR."
        ),
    }
    write_json(OUT / "CR217_summary.json", summary)

    # 11. Input manifest.
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
        OUT / "CR217_input_manifest.csv",
        manifest_rows,
        ["artifact", "sealed_sha256", "observed_sha256", "match", "role"],
    )

    # 12. HASHES.txt.
    hash_targets = list(SEALED_HASHES.keys()) + [
        OUT / "CR217_PRECOMMIT.md",
        OUT / "CR217_declared_premises.json",
        OUT / "CR217_runner.py",
        OUT / "CR217_input_manifest.csv",
        OUT / "CR217_carrier_block.csv",
        OUT / "CR217_hidden_source_block.csv",
        OUT / "CR217_identity_checks.csv",
        OUT / "CR217_summary.json",
        OUT / "CR217_result.md",
    ]
    lines = ["artifact,sha256"]
    for target in hash_targets:
        if target.exists():
            lines.append(f"{rel(target)},{sha256_file(target)}")
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
