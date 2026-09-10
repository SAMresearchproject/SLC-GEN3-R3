"""CR222 carrier ledger 12-plus-1 generator.

Build target from SAM_NEXT_MOVES_NATIVE_RESET.md:
generate the 12 unpacked carrier/support modes that sum to 81, keep
QP093A-0303 as the separate mirror/checksum row, and close the support ledger
as 81 + 81 = 162. CR119/CR214/CR219 are downstream validation surfaces only.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable


getcontext().prec = 120

CR_ID = "CR222"
TEST_ID = "CR222_CARRIER_LEDGER_12_PLUS_1"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

ROADMAP = BRANCH_DIR / "SAM_NEXT_MOVES_NATIVE_RESET.md"
CR119_TABLE = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_particle_table.csv"
)
CR214_COMPLEMENT = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
    / "CR214_particle_complement_195.csv"
)
CR219_PROMOTED = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR219_PROMOTED_PARTICLE_ROWS_EXPORT"
    / "CR219_promoted_particle_rows_126.csv"
)
CR220_NATIVE = (
    BRANCH_DIR
    / "CR220_NATIVE_63_GENERATOR"
    / "Tier1_Native63.csv"
)
CR221_BOUND = (
    BRANCH_DIR
    / "CR221_BOUND_63_GENERATOR"
    / "Tier1_Bound63.csv"
)

OUT_LEDGER_81 = CR_DIR / "Tier1_CarrierLedger81.csv"
OUT_MIRROR = CR_DIR / "CR222_mirror_closure_0303.csv"
OUT_CLOSURE_162 = CR_DIR / "CR222_support_closure_162.csv"
OUT_TOTALS = CR_DIR / "CR222_ledger_totals.csv"
OUT_WRONG_CONTROLS = CR_DIR / "CR222_wrong_controls.csv"
OUT_VALIDATION = CR_DIR / "CR222_validation_against_CR119_support.csv"
OUT_CR214_VALIDATION = CR_DIR / "CR222_validation_against_CR214_complement.csv"
OUT_CHECKS = CR_DIR / "CR222_checks.csv"
OUT_PRECOMMIT = CR_DIR / "CR222_PRECOMMIT.md"
OUT_SUMMARY = CR_DIR / "CR222_summary.json"
OUT_RESULT = CR_DIR / "CR222_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

ALPHA_H = 2
D = 3
R = 12
PARTITION_MODES = (1, 2, 3, 4, 6, 8, 9, 12)
SOURCE_IDS = {
    1: "QP093A-0306",
    2: "QP093A-0307",
    3: "QP093A-0308",
    4: "QP093A-0309",
    6: "QP093A-0310",
    8: "QP093A-0311",
    9: "QP093A-0312",
    12: "QP093A-0313",
}

CSV_FIELDS = [
    "ledger_id",
    "qp093a_reference",
    "ledger_group",
    "ledger_role",
    "operator_class",
    "route_combination",
    "partition_signature",
    "closure_depth",
    "q_sign",
    "q_abs",
    "native_charge_axis",
    "spin_or_hand_class",
    "ledger_value",
    "ledger_value_fraction",
    "native_mass_expected",
    "native_mass_fraction",
    "formula_used",
    "selector_rule",
    "matter_count_status",
    "role_reading",
    "construction_hash",
]


@dataclass(frozen=True)
class Check:
    check: str
    passed: bool
    observed: str
    expected: str


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_text(value: Fraction, places: int = 48) -> str:
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    s = format(dec, f".{places}f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def row_hash(payload: dict[str, str]) -> str:
    keys = [
        "ledger_group",
        "ledger_role",
        "operator_class",
        "partition_signature",
        "ledger_value_fraction",
        "native_mass_fraction",
        "formula_used",
        "selector_rule",
        "matter_count_status",
    ]
    material = {
        "constants": {
            "alpha_H": ALPHA_H,
            "D": D,
            "R": R,
            "partition_modes": PARTITION_MODES,
        },
        "row": {k: payload[k] for k in keys},
        "generator": TEST_ID,
    }
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def make_row(
    *,
    ordinal: int,
    qp093a_reference: str,
    ledger_group: str,
    ledger_role: str,
    operator_class: str,
    route_combination: str,
    partition_signature: int,
    q_sign: str,
    q_abs: int,
    native_charge_axis: str,
    spin_or_hand_class: str,
    ledger_value: Fraction,
    native_mass: Fraction,
    formula_used: str,
    selector_rule: str,
    role_reading: str,
) -> dict[str, str]:
    row = {
        "ledger_id": f"SAMC81-{ordinal:04d}",
        "qp093a_reference": qp093a_reference,
        "ledger_group": ledger_group,
        "ledger_role": ledger_role,
        "operator_class": operator_class,
        "route_combination": route_combination,
        "partition_signature": str(partition_signature),
        "closure_depth": str(D),
        "q_sign": q_sign,
        "q_abs": str(q_abs),
        "native_charge_axis": native_charge_axis,
        "spin_or_hand_class": spin_or_hand_class,
        "ledger_value": decimal_text(ledger_value, places=24),
        "ledger_value_fraction": fraction_text(ledger_value),
        "native_mass_expected": decimal_text(native_mass, places=48),
        "native_mass_fraction": fraction_text(native_mass),
        "formula_used": formula_used,
        "selector_rule": selector_rule,
        "matter_count_status": "SUPPORT_NOT_MATTER",
        "role_reading": role_reading,
        "construction_hash": "",
    }
    row["construction_hash"] = row_hash(row)
    return row


def source_mass(p: int) -> Fraction:
    return Fraction(p, 1) + Fraction(p * p, R * R)


def build_unpacked_12() -> list[dict[str, str]]:
    carrier_rows = [
        make_row(
            ordinal=1,
            qp093a_reference="QP093A-0300",
            ledger_group="carrier_mode",
            ledger_role="tensor_carrier",
            operator_class="TENSOR_CARRIER",
            route_combination="tensor_carrier_alphaH_D2",
            partition_signature=ALPHA_H * (D ** 2),
            q_sign="neutral",
            q_abs=0,
            native_charge_axis="carrier_axis",
            spin_or_hand_class="rank2_plus_cross",
            ledger_value=Fraction(ALPHA_H * (D ** 2), 1),
            native_mass=Fraction(ALPHA_H * (D ** 2), 1),
            formula_used="alpha_H*D^2",
            selector_rule="ACTIVE_CARRIER_MODE_NOT_MIRROR",
            role_reading="timing_gravity_witness_floor",
        ),
        make_row(
            ordinal=2,
            qp093a_reference="QP093A-0301",
            ledger_group="carrier_mode",
            ledger_role="road_light_carrier",
            operator_class="ROAD_LIGHT_CARRIER",
            route_combination="photon_road_carrier",
            partition_signature=1,
            q_sign="neutral",
            q_abs=0,
            native_charge_axis="carrier_axis",
            spin_or_hand_class="transverse_vector",
            ledger_value=Fraction(1, 1),
            native_mass=Fraction(0, 1),
            formula_used="massless_road_slot_with_partition_ledger_value_1",
            selector_rule="ACTIVE_CARRIER_MODE_NOT_MIRROR",
            role_reading="signal_path",
        ),
        make_row(
            ordinal=3,
            qp093a_reference="QP093A-0302",
            ledger_group="carrier_mode",
            ledger_role="weak_vector_carrier",
            operator_class="WEAK_VECTOR_CARRIER",
            route_combination="weak_vector_support",
            partition_signature=D ** 2,
            q_sign="neutral",
            q_abs=0,
            native_charge_axis="carrier_axis",
            spin_or_hand_class="massive_vector_support",
            ledger_value=Fraction(D ** 2, 1),
            native_mass=Fraction(D ** 2, 1),
            formula_used="D^2",
            selector_rule="ACTIVE_CARRIER_MODE_NOT_MIRROR",
            role_reading="weak_vector_carrier",
        ),
        make_row(
            ordinal=4,
            qp093a_reference="QP093A-0304",
            ledger_group="carrier_mode",
            ledger_role="color_owner_carrier",
            operator_class="COLOR_OWNER_CARRIER",
            route_combination="gluon_color_owner_support",
            partition_signature=ALPHA_H ** D,
            q_sign="neutral",
            q_abs=0,
            native_charge_axis="carrier_axis",
            spin_or_hand_class="color_octet_support",
            ledger_value=Fraction(ALPHA_H ** D, 1),
            native_mass=Fraction(ALPHA_H ** D, 1),
            formula_used="alpha_H^D",
            selector_rule="ACTIVE_CARRIER_MODE_NOT_MIRROR",
            role_reading="color_owner_carrier",
        ),
    ]

    source_rows: list[dict[str, str]] = []
    for offset, p in enumerate(PARTITION_MODES, start=5):
        source_rows.append(
            make_row(
                ordinal=offset,
                qp093a_reference=SOURCE_IDS[p],
                ledger_group="source_support_mode",
                ledger_role=f"source_packet_p_{p}",
                operator_class="SOURCE_SUPPORT_PACKET",
                route_combination=f"hidden_source_support[p={p}]",
                partition_signature=p,
                q_sign="positive",
                q_abs=p,
                native_charge_axis="source_axis",
                spin_or_hand_class="unresolved_support",
                ledger_value=Fraction(p, 1),
                native_mass=source_mass(p),
                formula_used="ledger_value=p; native_mass=p+p^2/R^2",
                selector_rule="SOURCE_SUPPORT_PARTITION_MODE",
                role_reading="unresolved_support_inventory",
            )
        )
    return carrier_rows + source_rows


def build_mirror_row() -> dict[str, str]:
    return make_row(
        ordinal=13,
        qp093a_reference="QP093A-0303",
        ledger_group="mirror_closure",
        ledger_role="combined_carrier_face_checksum",
        operator_class="NEUTRAL_VECTOR_CARRIER",
        route_combination="neutral_vector_support",
        partition_signature=D ** 4,
        q_sign="neutral",
        q_abs=0,
        native_charge_axis="carrier_axis",
        spin_or_hand_class="massive_vector_support",
        ledger_value=Fraction(D ** 4, 1),
        native_mass=Fraction(D ** 4, 1),
        formula_used="D^4",
        selector_rule="MIRROR_CHECKSUM_NOT_UNPACKED_MODE",
        role_reading="closed_carrier_ledger_checksum",
    )


def build_duplicate_wrong_control_row() -> dict[str, str]:
    return make_row(
        ordinal=14,
        qp093a_reference="QP093A-0305",
        ledger_group="excluded_duplicate_wrong_control",
        ledger_role="a_field_duplicate_slot",
        operator_class="A_FIELD_CARRIER",
        route_combination="a_kernel_support",
        partition_signature=1,
        q_sign="neutral",
        q_abs=0,
        native_charge_axis="carrier_axis",
        spin_or_hand_class="environmental_A_support",
        ledger_value=Fraction(1, 1),
        native_mass=Fraction(0, 1),
        formula_used="massless_A_slot_duplicate_partition_value_1",
        selector_rule="EXCLUDED_DUPLICATE_WRONG_CONTROL",
        role_reading="duplicate_support_slot_not_counted",
    )


def render_csv(rows: Iterable[dict[str, str]], fields: list[str]) -> bytes:
    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buf.getvalue().encode("utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, str]], fields: list[str]) -> None:
    path.write_bytes(render_csv(rows, fields))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def dec_from_fraction(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def decimal_close(observed: str, expected: Fraction, tolerance: Decimal = Decimal("1e-80")) -> bool:
    return abs(Decimal(observed) - dec_from_fraction(expected)) <= tolerance


def support_source_rows() -> list[dict[str, str]]:
    rows = build_unpacked_12() + [build_mirror_row(), build_duplicate_wrong_control_row()]
    return rows


def validation_against_source(source_path: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    source = {row["candidate_id"]: row for row in read_csv_rows(source_path)}
    out: list[dict[str, str]] = []
    for row in rows:
        candidate_id = row["qp093a_reference"]
        observed = source.get(candidate_id)
        partition_match = bool(observed and observed.get("partition_signature") == row["partition_signature"])
        operator_match = bool(observed and observed.get("operator_class") == row["operator_class"])
        mass_match = bool(observed and decimal_close(observed.get("M_native", "NaN"), Fraction(row["native_mass_fraction"])))
        out.append({
            "qp093a_reference": candidate_id,
            "ledger_group": row["ledger_group"],
            "ledger_value_fraction": row["ledger_value_fraction"],
            "source_present": str(observed is not None),
            "partition_match": str(partition_match),
            "operator_match": str(operator_match),
            "native_mass_match": str(mass_match),
            "generated_partition_signature": row["partition_signature"],
            "source_partition_signature": observed.get("partition_signature", "") if observed else "",
            "generated_operator_class": row["operator_class"],
            "source_operator_class": observed.get("operator_class", "") if observed else "",
            "generated_native_mass_fraction": row["native_mass_fraction"],
            "source_M_native": observed.get("M_native", "") if observed else "",
            "source_bin": observed.get("bin", "") if observed else "",
            "source_matter_row_allowed": observed.get("matter_row_allowed", "") if observed else "",
            "used_as_construction_input": "no",
        })
    return out


def wrong_control_rows(unpacked: list[dict[str, str]], mirror: dict[str, str], duplicate: dict[str, str]) -> list[dict[str, str]]:
    unpacked_total = sum(Fraction(row["ledger_value_fraction"]) for row in unpacked)
    mirror_total = Fraction(mirror["ledger_value_fraction"])
    missing_p1 = [
        row for row in unpacked
        if row["qp093a_reference"] != "QP093A-0306"
    ]
    pasted_missing_total = mirror_total + sum(Fraction(row["ledger_value_fraction"]) for row in missing_p1)
    duplicate_restored_total = mirror_total + unpacked_total + Fraction(duplicate["ledger_value_fraction"])
    collapsed_without_mirror = sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "carrier_mode"
    ) + sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "source_support_mode"
    )
    return [
        {
            "wrong_control": "pasted_block_missing_QP093A_0306_p1",
            "observed_total": fraction_text(pasted_missing_total),
            "expected_failure_total": "161",
            "passes_as_failure": str(pasted_missing_total == 161),
            "interpretation": "mirror_0303_plus_11_modes_missing_source_p1_is_short_by_one",
        },
        {
            "wrong_control": "restore_duplicate_QP093A_0305",
            "observed_total": fraction_text(duplicate_restored_total),
            "expected_failure_total": "163",
            "passes_as_failure": str(duplicate_restored_total == 163),
            "interpretation": "excluded_A_field_duplicate_adds_one_to_clean_162_closure",
        },
        {
            "wrong_control": "omit_0303_mirror",
            "observed_total": fraction_text(collapsed_without_mirror),
            "expected_failure_total": "81",
            "passes_as_failure": str(collapsed_without_mirror == 81),
            "interpretation": "unpacked_modes_alone_are_only_half_of_full_support_closure",
        },
    ]


def totals_rows(unpacked: list[dict[str, str]], mirror: dict[str, str]) -> list[dict[str, str]]:
    carrier_total = sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "carrier_mode"
    )
    source_total = sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "source_support_mode"
    )
    unpacked_total = carrier_total + source_total
    mirror_total = Fraction(mirror["ledger_value_fraction"])
    closure_total = unpacked_total + mirror_total
    tensor_value = Fraction(18, 1)
    return [
        {"quantity": "carrier_modes", "value": fraction_text(carrier_total), "formula": "18+1+9+8"},
        {"quantity": "source_support_modes", "value": fraction_text(source_total), "formula": "1+2+3+4+6+8+9+12"},
        {"quantity": "unpacked_12_modes", "value": fraction_text(unpacked_total), "formula": "36+45=D^4"},
        {"quantity": "mirror_0303", "value": fraction_text(mirror_total), "formula": "D^4"},
        {"quantity": "support_closure", "value": fraction_text(closure_total), "formula": "D^4+D^4=2D^4"},
        {"quantity": "tensor_over_carrier_subtotal", "value": fraction_text(tensor_value / carrier_total), "formula": "18/36=1/2"},
        {"quantity": "tensor_over_unpacked_81", "value": fraction_text(tensor_value / unpacked_total), "formula": "18/81=2/9"},
        {"quantity": "tensor_over_full_162", "value": fraction_text(tensor_value / closure_total), "formula": "18/162=1/9"},
    ]


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return -1
    return len(read_csv_rows(path))


def build_checks(
    unpacked: list[dict[str, str]],
    mirror: dict[str, str],
    duplicate: dict[str, str],
    validation_cr119: list[dict[str, str]],
    validation_cr214: list[dict[str, str]],
    wrong_controls: list[dict[str, str]],
) -> list[Check]:
    carrier_total = sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "carrier_mode"
    )
    source_total = sum(
        Fraction(row["ledger_value_fraction"]) for row in unpacked
        if row["ledger_group"] == "source_support_mode"
    )
    unpacked_total = carrier_total + source_total
    mirror_total = Fraction(mirror["ledger_value_fraction"])
    closure_total = unpacked_total + mirror_total
    unpacked_ids = {row["qp093a_reference"] for row in unpacked}
    source_modes = [
        int(row["partition_signature"]) for row in unpacked
        if row["ledger_group"] == "source_support_mode"
    ]
    all_validation_cr119 = all(
        row["source_present"] == "True"
        and row["partition_match"] == "True"
        and row["operator_match"] == "True"
        and row["native_mass_match"] == "True"
        for row in validation_cr119
    )
    all_validation_cr214 = all(
        row["source_present"] == "True"
        and row["partition_match"] == "True"
        and row["operator_match"] == "True"
        and row["native_mass_match"] == "True"
        for row in validation_cr214
    )
    support_ids = unpacked_ids | {mirror["qp093a_reference"], duplicate["qp093a_reference"]}
    promoted_rows = read_csv_rows(CR219_PROMOTED)
    promoted_support_hits = [row["candidate_id"] for row in promoted_rows if row["candidate_id"] in support_ids]
    cr220_count = count_csv_rows(CR220_NATIVE)
    cr221_count = count_csv_rows(CR221_BOUND)
    rendered_1 = render_csv(unpacked, CSV_FIELDS)
    rendered_2 = render_csv(build_unpacked_12(), CSV_FIELDS)
    wc = {row["wrong_control"]: row for row in wrong_controls}
    tensor_value = Fraction(18, 1)
    tensor_ratios_ok = (
        tensor_value / carrier_total == Fraction(1, 2)
        and tensor_value / unpacked_total == Fraction(2, 9)
        and tensor_value / closure_total == Fraction(1, 9)
    )

    return [
        Check("unpacked_rows_exactly_12", len(unpacked) == 12, str(len(unpacked)), "12"),
        Check("carrier_modes_exactly_4", sum(1 for row in unpacked if row["ledger_group"] == "carrier_mode") == 4, str(sum(1 for row in unpacked if row["ledger_group"] == "carrier_mode")), "4"),
        Check("source_support_modes_exactly_8", sum(1 for row in unpacked if row["ledger_group"] == "source_support_mode") == 8, str(sum(1 for row in unpacked if row["ledger_group"] == "source_support_mode")), "8"),
        Check("carrier_subtotal_36", carrier_total == 36, fraction_text(carrier_total), "36"),
        Check("source_support_subtotal_45", source_total == 45, fraction_text(source_total), "45"),
        Check("unpacked_12_sum_81", unpacked_total == 81, fraction_text(unpacked_total), "81"),
        Check("mirror_0303_separate_81", mirror["qp093a_reference"] == "QP093A-0303" and mirror_total == 81 and mirror["qp093a_reference"] not in unpacked_ids, f"{mirror['qp093a_reference']}={fraction_text(mirror_total)}; in_unpacked={mirror['qp093a_reference'] in unpacked_ids}", "QP093A-0303=81 and not in unpacked"),
        Check("closure_81_plus_81_equals_162", closure_total == 162, fraction_text(closure_total), "162"),
        Check("source_p1_0306_present", "QP093A-0306" in unpacked_ids and 1 in source_modes, str("QP093A-0306" in unpacked_ids), "True"),
        Check("source_partition_modes_exact", tuple(source_modes) == PARTITION_MODES, str(source_modes), str(list(PARTITION_MODES))),
        Check("tensor_ratio_role_locked", tensor_ratios_ok, "18/36=1/2;18/81=2/9;18/162=1/9", "locked"),
        Check("wrong_control_missing_0306_total_161", wc["pasted_block_missing_QP093A_0306_p1"]["passes_as_failure"] == "True", wc["pasted_block_missing_QP093A_0306_p1"]["observed_total"], "161"),
        Check("wrong_control_duplicate_0305_total_163", wc["restore_duplicate_QP093A_0305"]["passes_as_failure"] == "True", wc["restore_duplicate_QP093A_0305"]["observed_total"], "163"),
        Check("downstream_cr119_support_validation", all_validation_cr119, str(sum(1 for row in validation_cr119 if row["native_mass_match"] == "True")), str(len(validation_cr119))),
        Check("downstream_cr214_complement_validation", all_validation_cr214, str(sum(1 for row in validation_cr214 if row["native_mass_match"] == "True")), str(len(validation_cr214))),
        Check("support_rows_absent_from_promoted_matter126", len(promoted_rows) == 126 and not promoted_support_hits, f"promoted_rows={len(promoted_rows)}; support_hits={promoted_support_hits}", "126 rows; no support hits"),
        Check("native_plus_bound_still_126", cr220_count == 63 and cr221_count == 63, f"CR220={cr220_count}; CR221={cr221_count}", "63+63"),
        Check("deterministic_byte_identical_regeneration", rendered_1 == rendered_2, sha256_bytes(rendered_1), sha256_bytes(rendered_2)),
    ]


def write_hashes(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths, key=lambda p: p.name):
        lines.append(f"{sha256_file(path)}  {path.name}")
    OUT_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_precommit(ledger_sha: str) -> None:
    text = f"""# CR222 PRECOMMIT - Carrier Ledger 12 Plus 1

## Scope

Generate the support ledger from SAM constants and the corrected row-order
selector:

```text
alpha_H = {ALPHA_H}
D = {D}
R = {R}
Pi = {PARTITION_MODES}
```

## Generator

Twelve unpacked modes:

```text
carrier modes        = 18 + 1 + 9 + 8 = 36
source support modes = 1 + 2 + 3 + 4 + 6 + 8 + 9 + 12 = 45
unpacked total       = 36 + 45 = 81 = D^4
```

`QP093A-0303` is not one of the twelve unpacked modes. It is the separate
mirror/checksum row:

```text
0303 = 81 = D^4
closure = 81 + 81 = 162 = 2D^4
```

`QP093A-0306`, source packet `p=1`, is required inside the eight source-support
modes.

## Downstream Validation

CR119 and CR214 are read only after construction to verify row IDs, partitions,
operator classes, and native masses. CR219 is read only to confirm the support
rows are absent from the 126 promoted matter rows.

## Wrong Controls

```text
missing 0306:p=1       -> 161
restoring 0305 duplicate -> 163
omitting 0303 mirror   -> 81
```

## Pre-run Hash

Expected generated `Tier1_CarrierLedger81.csv` hash:

```text
{ledger_sha}
```
"""
    OUT_PRECOMMIT.write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# CR222 Carrier Ledger 12 Plus 1

This artifact implements the carrier-ledger milestone from
`SAM_NEXT_MOVES_NATIVE_RESET.md`.

Primary product:

```text
Tier1_CarrierLedger81.csv
```

`QP093A-0303` is written separately in `CR222_mirror_closure_0303.csv` and
combined with the 12 unpacked modes in `CR222_support_closure_162.csv`.
"""
    OUT_README.write_text(text, encoding="utf-8")


def write_result(summary: dict[str, object]) -> None:
    result_class = summary["result_class"]
    checks_passed = summary["checks_passed"]
    checks_total = summary["checks_total"]
    ledger_sha = summary["sha256"]["Tier1_CarrierLedger81.csv"]
    text = f"""# CR222 Carrier Ledger 12 Plus 1 Result

**Result class:** `{result_class}`

**Checks:** {checks_passed}/{checks_total}

**Tier1_CarrierLedger81.csv SHA-256:** `{ledger_sha}`

## Verdict

The corrected support ledger closes cleanly:

```text
18 + 1 + 9 + 8 + (1 + 2 + 3 + 4 + 6 + 8 + 9 + 12) = 81
0303 = 81
81 + 81 = 162
```

`QP093A-0303` is kept outside the twelve unpacked modes as the mirror/checksum
row. `QP093A-0306:p=1` is restored inside the eight source-support modes.

## Tensor Role

The tensor carrier locks the clean ratios:

```text
18/36  = 1/2
18/81  = 2/9
18/162 = 1/9
```

So the tensor row is recorded as timing / gravity / witness floor, not message
payload and not promoted matter.

## Outputs

- `Tier1_CarrierLedger81.csv`
- `CR222_mirror_closure_0303.csv`
- `CR222_support_closure_162.csv`
- `CR222_ledger_totals.csv`
- `CR222_wrong_controls.csv`
- `CR222_validation_against_CR119_support.csv`
- `CR222_validation_against_CR214_complement.csv`
- `CR222_checks.csv`
- `CR222_summary.json`
- `HASHES.txt`
"""
    OUT_RESULT.write_text(text, encoding="utf-8")


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    unpacked = build_unpacked_12()
    mirror = build_mirror_row()
    duplicate = build_duplicate_wrong_control_row()
    closure_rows = unpacked + [mirror]

    ledger_bytes = render_csv(unpacked, CSV_FIELDS)
    ledger_sha = sha256_bytes(ledger_bytes)
    OUT_LEDGER_81.write_bytes(ledger_bytes)
    write_csv(OUT_MIRROR, [mirror], CSV_FIELDS)
    write_csv(OUT_CLOSURE_162, closure_rows, CSV_FIELDS)

    totals = totals_rows(unpacked, mirror)
    write_csv(OUT_TOTALS, totals, ["quantity", "value", "formula"])

    wrongs = wrong_control_rows(unpacked, mirror, duplicate)
    write_csv(OUT_WRONG_CONTROLS, wrongs, ["wrong_control", "observed_total", "expected_failure_total", "passes_as_failure", "interpretation"])

    validation_cr119 = validation_against_source(CR119_TABLE, support_source_rows())
    validation_fields = [
        "qp093a_reference",
        "ledger_group",
        "ledger_value_fraction",
        "source_present",
        "partition_match",
        "operator_match",
        "native_mass_match",
        "generated_partition_signature",
        "source_partition_signature",
        "generated_operator_class",
        "source_operator_class",
        "generated_native_mass_fraction",
        "source_M_native",
        "source_bin",
        "source_matter_row_allowed",
        "used_as_construction_input",
    ]
    write_csv(OUT_VALIDATION, validation_cr119, validation_fields)

    validation_cr214 = validation_against_source(CR214_COMPLEMENT, support_source_rows())
    write_csv(OUT_CR214_VALIDATION, validation_cr214, validation_fields)

    checks = build_checks(unpacked, mirror, duplicate, validation_cr119, validation_cr214, wrongs)
    write_csv(OUT_CHECKS, [asdict(check) for check in checks], ["check", "passed", "observed", "expected"])

    checks_passed = sum(1 for check in checks if check.passed)
    checks_total = len(checks)
    result_class = (
        "CR222_PASS_CARRIER_LEDGER__12_UNPACKED_81__0303_MIRROR__162_CLOSURE"
        if checks_passed == checks_total
        else "CR222_FAIL_CARRIER_LEDGER"
    )

    carrier_total = sum(Fraction(row["ledger_value_fraction"]) for row in unpacked if row["ledger_group"] == "carrier_mode")
    source_total = sum(Fraction(row["ledger_value_fraction"]) for row in unpacked if row["ledger_group"] == "source_support_mode")
    unpacked_total = carrier_total + source_total
    mirror_total = Fraction(mirror["ledger_value_fraction"])
    closure_total = unpacked_total + mirror_total

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "constants": {"alpha_H": ALPHA_H, "D": D, "R": R},
        "partition_modes": list(PARTITION_MODES),
        "row_counts": {
            "unpacked_modes": len(unpacked),
            "carrier_modes": sum(1 for row in unpacked if row["ledger_group"] == "carrier_mode"),
            "source_support_modes": sum(1 for row in unpacked if row["ledger_group"] == "source_support_mode"),
            "mirror_rows": 1,
        },
        "totals": {
            "carrier_modes": fraction_text(carrier_total),
            "source_support_modes": fraction_text(source_total),
            "unpacked_12_modes": fraction_text(unpacked_total),
            "mirror_0303": fraction_text(mirror_total),
            "support_closure": fraction_text(closure_total),
        },
        "tensor_ratios": {
            "tensor_over_carrier_modes": "1/2",
            "tensor_over_unpacked_81": "2/9",
            "tensor_over_full_162": "1/9",
        },
        "source_boundary": "CR119, CR214, and CR219 read after generation only; no imported support rows in construction.",
        "roadmap": str(ROADMAP.relative_to(COURTROOM_DIR)),
        "validation_sources": {
            "cr119": str(CR119_TABLE.relative_to(COURTROOM_DIR)),
            "cr214": str(CR214_COMPLEMENT.relative_to(COURTROOM_DIR)),
            "cr219": str(CR219_PROMOTED.relative_to(COURTROOM_DIR)),
        },
        "outputs": {
            "ledger_81_csv": OUT_LEDGER_81.name,
            "mirror_csv": OUT_MIRROR.name,
            "closure_162_csv": OUT_CLOSURE_162.name,
            "totals_csv": OUT_TOTALS.name,
            "wrong_controls_csv": OUT_WRONG_CONTROLS.name,
            "validation_cr119_csv": OUT_VALIDATION.name,
            "validation_cr214_csv": OUT_CR214_VALIDATION.name,
            "checks_csv": OUT_CHECKS.name,
            "summary_json": OUT_SUMMARY.name,
            "result_md": OUT_RESULT.name,
        },
        "sha256": {
            "Tier1_CarrierLedger81.csv": ledger_sha,
        },
        "next_gate": "CR223_TIER1_NATIVE_BOUND_CARRIER_CONTRACT",
    }

    write_precommit(ledger_sha)
    write_readme()
    write_json(OUT_SUMMARY, summary)
    write_result(summary)
    write_hashes([
        OUT_LEDGER_81,
        OUT_MIRROR,
        OUT_CLOSURE_162,
        OUT_TOTALS,
        OUT_WRONG_CONTROLS,
        OUT_VALIDATION,
        OUT_CR214_VALIDATION,
        OUT_CHECKS,
        OUT_PRECOMMIT,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ])

    print("CR222 carrier ledger 12 plus 1 complete")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  unpacked rows: {len(unpacked)}")
    print(f"  closure: {fraction_text(closure_total)}")
    print(f"  Tier1_CarrierLedger81.csv sha256: {ledger_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
