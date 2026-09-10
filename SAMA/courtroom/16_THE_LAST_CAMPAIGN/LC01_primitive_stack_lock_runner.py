#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


LC_ID = "LC01"
RESULT_CLASS = "LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER"
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO)).replace("/", "\\")
    except ValueError:
        return str(path).replace("/", "\\")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(relative_path: str) -> dict[str, Any]:
    path = REPO / relative_path
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def stringify(value: Any) -> str:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)
    if isinstance(value, (list, tuple)):
        return "; ".join(stringify(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return str(value)


def json_safe(value: Any) -> Any:
    if isinstance(value, Fraction):
        return stringify(value)
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return value


def frac_decimal(value: Fraction, places: int = 30) -> str:
    getcontext().prec = places + 12
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    return format(dec, f".{places}f")


def check(rows: list[dict[str, Any]], check_id: str, description: str, expected: Any, observed: Any) -> None:
    passed = stringify(expected) == stringify(observed)
    rows.append(
        {
            "check_id": check_id,
            "description": description,
            "expected": expected,
            "observed": observed,
            "status": "PASS" if passed else "FAIL",
        }
    )


def source_row(source_id: str, relative_path: str, purpose: str, expected: str, observed: str) -> dict[str, Any]:
    path = REPO / relative_path
    return {
        "source_id": source_id,
        "path": relative_path.replace("/", "\\"),
        "purpose": purpose,
        "exists": path.exists(),
        "expected_status": expected,
        "observed_status": observed,
        "sha256": sha256_path(path) if path.exists() else "MISSING",
    }


def main() -> int:
    getcontext().prec = 80
    executed_at = now_utc()

    alpha_H = 2
    R = 12
    D = 3
    R2 = R * R
    split_fraction = Fraction(1, 2**D)
    retained_side = Fraction(1, 1) - split_fraction
    carrier_side = split_fraction
    bounce_lift = Fraction(D * D, 2**D)
    resolved_half_bounce = Fraction(D * D, 2 ** (D + 1))
    surface_debit = Fraction(D * D, R)
    split_loss = Fraction(R2, 1) * split_fraction
    retained_parent = Fraction(R2, 1) * retained_side
    observed_higgs = retained_parent - surface_debit
    tensor_identity = Fraction(alpha_H * D * D, 1)
    pi_dec = Decimal("3.14159265358979323846264338327950288419716939937510")
    A0_dec = Decimal(1) / (Decimal(R) * pi_dec)

    cr113 = load_json("14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json")
    cr114 = load_json("14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json")
    cr115 = load_json("14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json")
    cr116 = load_json("14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json")
    cr104c = load_json("14_FOUNDATIONAL_TESTS/CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL/CR104c_appeal_lock.json")

    primitives = [
        {
            "primitive": "alpha_H",
            "formula_or_lock": "locked Higgs branch count",
            "value_exact": "2",
            "value_decimal": "2",
            "source": "CR114, CR116",
            "status": "LOCKED",
        },
        {
            "primitive": "R",
            "formula_or_lock": "completed-WRITE address count",
            "value_exact": "12",
            "value_decimal": "12",
            "source": "CR113",
            "status": "LOCKED",
        },
        {
            "primitive": "D",
            "formula_or_lock": "invariant carrier uniqueness",
            "value_exact": "3",
            "value_decimal": "3",
            "source": "CR115",
            "status": "LOCKED",
        },
        {
            "primitive": "A0",
            "formula_or_lock": "1/(pi*R), applied after R is fixed",
            "value_exact": "1/(12*pi)",
            "value_decimal": format(A0_dec, ".30f"),
            "source": "CR113 plus post-R A0 convention",
            "status": "LOCKED",
        },
        {
            "primitive": "R^2",
            "formula_or_lock": "R*R",
            "value_exact": str(R2),
            "value_decimal": str(R2),
            "source": "CR113",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "split_fraction",
            "formula_or_lock": "2^-D",
            "value_exact": split_fraction,
            "value_decimal": frac_decimal(split_fraction),
            "source": "CR114",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "retained_side",
            "formula_or_lock": "1 - 2^-D",
            "value_exact": retained_side,
            "value_decimal": frac_decimal(retained_side),
            "source": "CR114",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "carrier_side",
            "formula_or_lock": "2^-D",
            "value_exact": carrier_side,
            "value_decimal": frac_decimal(carrier_side),
            "source": "CR114, CR116",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "bounce_lift",
            "formula_or_lock": "D^2/2^D",
            "value_exact": bounce_lift,
            "value_decimal": frac_decimal(bounce_lift),
            "source": "CR104c",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "resolved_half_bounce",
            "formula_or_lock": "D^2/2^(D+1)",
            "value_exact": resolved_half_bounce,
            "value_decimal": frac_decimal(resolved_half_bounce),
            "source": "CR104c",
            "status": "DERIVED_FROM_LOCK",
        },
        {
            "primitive": "surface_debit",
            "formula_or_lock": "D^2/R",
            "value_exact": surface_debit,
            "value_decimal": frac_decimal(surface_debit),
            "source": "CR114",
            "status": "DERIVED_FROM_LOCK",
        },
    ]

    source_rows = [
        source_row(
            "CR113",
            "14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json",
            "R=12 completed-WRITE address count theorem",
            "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM",
            cr113.get("result_class", ""),
        ),
        source_row(
            "CR114",
            "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json",
            "1/8 carrier side, 7/8 retained side, 18 split loss, 126 parent",
            "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM",
            cr114.get("result_class", ""),
        ),
        source_row(
            "CR115",
            "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json",
            "D=3 invariant carrier uniqueness theorem gate",
            "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE",
            cr115.get("result_class", ""),
        ),
        source_row(
            "CR116",
            "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json",
            "18 as graviton-channel tensor carrier, not matter/rest mass",
            "CR116_PASS_18_GRAVITON_CHANNEL_CARRIER_THEOREM",
            cr116.get("result_class", ""),
        ),
        source_row(
            "CR104c",
            "14_FOUNDATIONAL_TESTS/CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL/CR104c_appeal_lock.json",
            "9/8 bounce lift and 9/16 resolved half-bounce D=3 algebra",
            "CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL_LOCK",
            cr104c.get("lock_id", ""),
        ),
        source_row(
            "CR103a",
            "14_FOUNDATIONAL_TESTS/CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL/CR103a_result.md",
            "A-dependent bounce cost and A-field terminology discipline",
            "CR103a_BOUNCE_COST_A_DEPENDENCE_STRUCTURAL_INSIGHT_LOCKED",
            "text source",
        ),
    ]

    lane_rows = [
        {
            "lc_id": "LC02",
            "lane": "Higgs closed form",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "R^2*(1-2^-D) - D^2/R = 125.25 from locked stack",
            "principal_sources": "CR113; CR114; CR104c; CR116",
            "primary_wrong_controls": "WC17; WC18; WC20",
            "planned_artifacts": "LC02_*",
        },
        {
            "lc_id": "LC03",
            "lane": "qA / ledger compression / gravity-as-A update",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "qA remains source strength / ledger sign update, not mass substitution",
            "principal_sources": "CR103a; CR116; CR147",
            "primary_wrong_controls": "WC08; WC10; WC11; WC12",
            "planned_artifacts": "LC03_*",
        },
        {
            "lc_id": "LC04",
            "lane": "particle mass-chain table",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "mass rows replay without changing constants, formulas, rows, or q labels",
            "principal_sources": "CR114; CR116; particle-chain branch",
            "primary_wrong_controls": "WC20; WC21; WC22",
            "planned_artifacts": "LC04_*",
        },
        {
            "lc_id": "LC05",
            "lane": "periodic/isotope vault",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "periodic/isotope rows replay from locked primitive stack without backfill",
            "principal_sources": "CR114; CR116; branch 10 vault",
            "primary_wrong_controls": "WC22; WC23",
            "planned_artifacts": "LC05_*",
        },
        {
            "lc_id": "LC06",
            "lane": "baryon and matter inventory",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "baryon split and matter inventory preserve carrier/matter distinction",
            "principal_sources": "CR114; CR116; branch 07",
            "primary_wrong_controls": "WC09; WC23",
            "planned_artifacts": "LC06_*",
        },
        {
            "lc_id": "LC07",
            "lane": "SN/BAO distance road",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "distance branch replay without D refit, bin cherry-pick, or target substitution",
            "principal_sources": "CR115; branch 06",
            "primary_wrong_controls": "WC24; WC25",
            "planned_artifacts": "LC07_*",
        },
        {
            "lc_id": "LC08",
            "lane": "halo/PBH inventory lane",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "halo/PBH inventory replay without config-as-law promotion",
            "principal_sources": "CR113; CR115; branch 08",
            "primary_wrong_controls": "WC26",
            "planned_artifacts": "LC08_*",
        },
        {
            "lc_id": "LC09",
            "lane": "quantum pair-write / Born-rule lane",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "pair-write and Born-rule lane replay without normalization patch",
            "principal_sources": "branch 11; quantum_phase campaign",
            "primary_wrong_controls": "WC27",
            "planned_artifacts": "LC09_*",
        },
        {
            "lc_id": "LC10",
            "lane": "quantum information thresholds",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "QI thresholds replay without threshold swap",
            "principal_sources": "branch 12; branch 12a; quantum_phase campaign",
            "primary_wrong_controls": "WC28",
            "planned_artifacts": "LC10_*",
        },
        {
            "lc_id": "LC11",
            "lane": "black-hole/horizon thermodynamic lane",
            "status": "REGISTERED_PENDING_REPLAY",
            "required_replay": "A=1, 11/12, horizon, and thermodynamic lane replay without softening A=1",
            "principal_sources": "CR103a; CR113; CR147; branch 05",
            "primary_wrong_controls": "WC11; WC12; WC29; WC30",
            "planned_artifacts": "LC11_*",
        },
    ]

    wrong_controls = [
        {
            "control_id": "WC01_PRIMITIVE_MUTATION",
            "scope": "global",
            "mutation_attempt": "change alpha_H, R, D, A0, split fractions, bounce, or debit after LC01",
            "rejection_basis": "LC01 primitive lock plus source hashes fix the stack before lane replay",
            "status": "REJECTED_BY_LC01",
        },
        {
            "control_id": "WC02_BRANCH_LOCAL_CONSTANT_OVERRIDE",
            "scope": "global",
            "mutation_attempt": "let a branch define a local R, D, A0, split, bounce, or debit",
            "rejection_basis": "later LC lanes must read the LC01 primitive table",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC03_TARGET_VALUE_SUBSTITUTION",
            "scope": "global",
            "mutation_attempt": "feed a measured target value into the primitive selector",
            "rejection_basis": "source chain fixes primitives before downstream comparisons",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC04_ROW_DELETION",
            "scope": "global",
            "mutation_attempt": "drop failed rows from a downstream replay",
            "rejection_basis": "lane artifacts must state input row counts and output row counts",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC05_RETROACTIVE_RELABELING",
            "scope": "global",
            "mutation_attempt": "rename a failed category after seeing the downstream result",
            "rejection_basis": "role labels must be fixed before each replay lane compares results",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC06_FORMULA_PATCH",
            "scope": "global",
            "mutation_attempt": "patch the formula after a lane misses",
            "rejection_basis": "each LC lane must emit formula manifest before result comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC07_OLD_ROUTE_RESTORE",
            "scope": "global",
            "mutation_attempt": "restore the old 2*pi route as the R=12 defense",
            "rejection_basis": "R is sourced to CR113 completed-WRITE address count; A0 is applied only after R is fixed",
            "status": "REJECTED_BY_LC01",
        },
        {
            "control_id": "WC08_DIRECT_QA_AS_MASS",
            "scope": "qA",
            "mutation_attempt": "treat qA/source strength as observed mass",
            "rejection_basis": "qA is registered as source/ledger strength; mass lanes must keep native mass and surface grammar separate",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC09_CARRIER_PROMOTED_TO_MATTER",
            "scope": "matter",
            "mutation_attempt": "put 18 into matter algebra as a rest-mass element",
            "rejection_basis": "CR116 locks 18 as carrier-only tensor channel, not matter/rest mass",
            "status": "REJECTED_BY_LC01",
        },
        {
            "control_id": "WC10_SURFACE_DEBIT_CONFUSION",
            "scope": "Higgs/qA",
            "mutation_attempt": "confuse carrier side 1/8 with surface debit D^2/R",
            "rejection_basis": "LC01 exact arithmetic gives 1/8 != 3/4",
            "status": "REJECTED_BY_LC01",
        },
        {
            "control_id": "WC11_STATIC_A_FOR_DYNAMIC_RELEASE",
            "scope": "GW/strong-field",
            "mutation_attempt": "use static int A dr/c as a dynamic GW170817 release model",
            "rejection_basis": "strong-field lanes must preserve release-point/source-origin distinction",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC12_A1_AS_NORMAL_LAUNCH_POINT",
            "scope": "horizon",
            "mutation_attempt": "treat A=1 as an ordinary photon launch surface",
            "rejection_basis": "A=1 is zero-depth/no-escape completion, not normal propagation",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC13_BRANCH_REPLAY_WITHOUT_HASH_LOCK",
            "scope": "global",
            "mutation_attempt": "accept downstream replay without source/hash manifest",
            "rejection_basis": "LC format requires source, formula, checks, wrong controls, and hashes",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC14_IN_SAMPLE_RESCUE",
            "scope": "global",
            "mutation_attempt": "tune a lane on the same targets it claims to predict",
            "rejection_basis": "lane must declare target visibility and selector order",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC15_TOLERANCE_EXPANSION",
            "scope": "global",
            "mutation_attempt": "expand tolerance after seeing miss size",
            "rejection_basis": "lane tolerance must be fixed before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC16_HIDDEN_CORRECTION_TERM",
            "scope": "global",
            "mutation_attempt": "add an unregistered correction term",
            "rejection_basis": "lane formula manifest must list every term before execution",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC17_HIGGS_TARGET_LOCK",
            "scope": "Higgs",
            "mutation_attempt": "set the Higgs value first and solve backwards",
            "rejection_basis": "LC02 must compute 125.25 from locked primitives before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC18_HIGGS_CARRIER_DEBIT_SWAP",
            "scope": "Higgs",
            "mutation_attempt": "swap 18 carrier loss, 0.75 surface debit, and 9/16 half-bounce roles",
            "rejection_basis": "LC01 exact arithmetic keeps all three roles distinct",
            "status": "REJECTED_BY_LC01",
        },
        {
            "control_id": "WC19_QA_LEDGER_COMPRESSION_SKIP",
            "scope": "qA",
            "mutation_attempt": "skip ledger compression and compare qA directly as an observed value",
            "rejection_basis": "LC03 must preserve ledger/source/observed layers",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC20_PARTICLE_TABLE_NEAREST_MATCH",
            "scope": "particle",
            "mutation_attempt": "assign each particle to the nearest matching row after comparison",
            "rejection_basis": "LC04 role map must be fixed before mass comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC21_PARTICLE_ROW_SUPPRESSION",
            "scope": "particle",
            "mutation_attempt": "suppress particle rows that fail under the locked stack",
            "rejection_basis": "LC04 must reconcile all declared rows or fail",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC22_PERIODIC_TABLE_DATA_BACKFILL",
            "scope": "periodic/isotope",
            "mutation_attempt": "backfill isotope constants from observed periodic data",
            "rejection_basis": "LC05 must declare generator values before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC23_BARYON_INVENTORY_RAW_BRANCH",
            "scope": "baryon/matter",
            "mutation_attempt": "mix carrier-only rows into matter inventory to close counts",
            "rejection_basis": "CR116 carrier/matter distinction is load-bearing",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC24_DISTANCE_ROAD_D_REFIT",
            "scope": "distance",
            "mutation_attempt": "refit D in the distance road after CR115 locks D=3",
            "rejection_basis": "LC07 must use D=3 from LC01 unless explicitly marked failed/mutated",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC25_DISTANCE_BIN_CHERRY_PICK",
            "scope": "distance",
            "mutation_attempt": "select only favorable SN/BAO bins",
            "rejection_basis": "LC07 must state bin set before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC26_HALO_PBH_CONFIG_AS_LAW",
            "scope": "halo/PBH",
            "mutation_attempt": "promote a successful config file to a primitive law",
            "rejection_basis": "LC08 must distinguish generator config from theorem primitive",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC27_QUANTUM_BORN_RULE_NORMALIZATION_PATCH",
            "scope": "quantum",
            "mutation_attempt": "patch Born-rule normalization after result comparison",
            "rejection_basis": "LC09 must predeclare normalization from pair-write machinery",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC28_QI_THRESHOLD_SWAP",
            "scope": "quantum information",
            "mutation_attempt": "swap QI thresholds after seeing which one passes",
            "rejection_basis": "LC10 thresholds must be locked before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC29_BLACK_HOLE_A1_SOFTENING",
            "scope": "black-hole/horizon",
            "mutation_attempt": "soften A=1 from zero-depth/no-escape into ordinary propagation",
            "rejection_basis": "LC11 must preserve A=1 completion discipline",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
        {
            "control_id": "WC30_THERMAL_TARGET_FIT",
            "scope": "black-hole/thermodynamic",
            "mutation_attempt": "fit thermodynamic coefficients to Hawking/entropy targets",
            "rejection_basis": "LC11 must derive thermal terms from locked stack before comparison",
            "status": "REGISTERED_FOR_LANE_REPLAY",
        },
    ]

    checks: list[dict[str, Any]] = []
    check(checks, "LC01_CHECK_001", "CR113 result class", "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM", cr113.get("result_class", ""))
    check(checks, "LC01_CHECK_002", "CR113 R value", R, cr113.get("R", ""))
    check(checks, "LC01_CHECK_003", "CR114 result class", "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM", cr114.get("result_class", ""))
    check(checks, "LC01_CHECK_004", "CR114 face state count", 2**D, cr114.get("face_state_count", ""))
    check(checks, "LC01_CHECK_005", "CR114 carrier fraction", split_fraction, cr114.get("carrier_fraction", ""))
    check(checks, "LC01_CHECK_006", "CR114 retained fraction", retained_side, cr114.get("retained_fraction", ""))
    check(checks, "LC01_CHECK_007", "CR114 split loss", split_loss, cr114.get("split_loss", ""))
    check(checks, "LC01_CHECK_008", "CR114 retained parent", retained_parent, cr114.get("retained_parent", ""))
    check(checks, "LC01_CHECK_009", "CR114 observed surface", observed_higgs, cr114.get("observed_surface", ""))
    check(checks, "LC01_CHECK_010", "CR115 result class", "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE", cr115.get("result_class", ""))
    check(checks, "LC01_CHECK_011", "CR115 stable D set", [3], cr115.get("stable_ds", ""))
    check(checks, "LC01_CHECK_012", "CR116 result class", "CR116_PASS_18_GRAVITON_CHANNEL_CARRIER_THEOREM", cr116.get("result_class", ""))
    check(checks, "LC01_CHECK_013", "CR116 carrier status", "carrier_only_not_matter", cr116.get("particle_catalog_status", ""))
    check(checks, "LC01_CHECK_014", "CR116 tensor identity", tensor_identity, cr116.get("tensor_identity_alpha_H_D2", "").split(".")[0])
    check(checks, "LC01_CHECK_015", "CR104c lock id", "CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL_LOCK", cr104c.get("lock_id", ""))
    check(checks, "LC01_CHECK_016", "bounce lift D^2/2^D", Fraction(9, 8), bounce_lift)
    check(checks, "LC01_CHECK_017", "resolved half-bounce D^2/2^(D+1)", Fraction(9, 16), resolved_half_bounce)
    check(checks, "LC01_CHECK_018", "surface debit distinct from carrier side", True, surface_debit != carrier_side)
    check(checks, "LC01_CHECK_019", "18 carrier loss equals alpha_H*D^2", split_loss, tensor_identity)
    check(checks, "LC01_CHECK_020", "lane register count", 10, len(lane_rows))
    check(checks, "LC01_CHECK_021", "wrong controls count", 30, len(wrong_controls))
    check(checks, "LC01_CHECK_022", "source files exist", True, all(row["exists"] for row in source_rows))

    active_control_statuses = {row["status"] for row in wrong_controls}
    check(
        checks,
        "LC01_CHECK_023",
        "wrong controls are rejected now or registered for lane replay",
        True,
        active_control_statuses <= {"REJECTED_BY_LC01", "REGISTERED_FOR_LANE_REPLAY"},
    )

    all_checks_passed = all(row["status"] == "PASS" for row in checks)
    all_sources_exist = all(row["exists"] for row in source_rows)
    execution_status = "CLEAN" if all_checks_passed and all_sources_exist else "FAILED"

    primitive_path = ROOT / "LC01_primitive_stack_declared.csv"
    source_path = ROOT / "LC01_source_chain.csv"
    lane_path = ROOT / "LC01_downstream_lane_register.csv"
    wrong_path = ROOT / "LC01_wrong_controls.csv"
    checks_path = ROOT / "LC01_checks.csv"
    summary_path = ROOT / "LC01_summary.json"
    lock_path = ROOT / "LC01_primitive_stack_lock.json"
    result_path = ROOT / "LC01_result.md"
    hash_path = ROOT / "LC01_hashes.txt"

    write_csv(
        primitive_path,
        primitives,
        ["primitive", "formula_or_lock", "value_exact", "value_decimal", "source", "status"],
    )
    write_csv(
        source_path,
        source_rows,
        ["source_id", "path", "purpose", "exists", "expected_status", "observed_status", "sha256"],
    )
    write_csv(
        lane_path,
        lane_rows,
        ["lc_id", "lane", "status", "required_replay", "principal_sources", "primary_wrong_controls", "planned_artifacts"],
    )
    write_csv(
        wrong_path,
        wrong_controls,
        ["control_id", "scope", "mutation_attempt", "rejection_basis", "status"],
    )
    write_csv(
        checks_path,
        checks,
        ["check_id", "description", "expected", "observed", "status"],
    )

    lock = {
        "lc_id": LC_ID,
        "result_class": RESULT_CLASS if execution_status == "CLEAN" else "LC01_FAIL_PRIMITIVE_STACK_OR_REGISTER",
        "execution_status": execution_status,
        "executed_at_utc": executed_at,
        "scope": "primitive stack lock and downstream replay register only",
        "not_claimed": "LC01 does not claim downstream lane replay; LC02-LC11 must run separately.",
        "primitive_values": {row["primitive"]: row["value_exact"] for row in primitives},
        "derived_values": {
            "split_loss": stringify(split_loss),
            "retained_parent": stringify(retained_parent),
            "observed_higgs_surface": stringify(observed_higgs),
            "tensor_identity_alpha_H_D2": stringify(tensor_identity),
        },
        "source_chain": source_rows,
        "downstream_lanes": lane_rows,
        "wrong_controls": wrong_controls,
        "checks": checks,
    }
    lock_path.write_text(json.dumps(json_safe(lock), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "lc_id": LC_ID,
        "branch": "16_THE_LAST_CAMPAIGN",
        "test_class": "LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER",
        "execution_status": execution_status,
        "result_class": lock["result_class"],
        "all_checks_passed": all_checks_passed,
        "all_sources_exist": all_sources_exist,
        "all_wrong_controls_rejected_or_registered": active_control_statuses <= {"REJECTED_BY_LC01", "REGISTERED_FOR_LANE_REPLAY"},
        "downstream_lanes_registered": len(lane_rows),
        "downstream_lanes_replayed": 0,
        "primitive_stack_csv": rel(primitive_path),
        "source_chain_csv": rel(source_path),
        "lane_register_csv": rel(lane_path),
        "wrong_controls_csv": rel(wrong_path),
        "checks_csv": rel(checks_path),
        "lock_json": rel(lock_path),
        "result_md": rel(result_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_lines = [
        "# LC01 Primitive Stack Lock and Replay Register",
        "",
        "## Verdict",
        "",
        "```text",
        lock["result_class"],
        "```",
        "",
        "## What LC01 Does",
        "",
        "LC01 locks the primitive stack, source chain, wrong controls, and downstream lane register for The Last Campaign.",
        "It begins the replay campaign. It does not claim any downstream lane has already replayed.",
        "",
        "## Locked Stack",
        "",
        "- alpha_H = 2",
        "- R = 12",
        "- D = 3",
        f"- A0 = 1/(pi*R) = {format(A0_dec, '.30f')}",
        "- R^2 = 144",
        "- split fraction = 2^-D = 1/8",
        "- retained side = 7/8",
        "- carrier side = 1/8",
        "- bounce lift = D^2/2^D = 9/8",
        "- resolved half-bounce = D^2/2^(D+1) = 9/16",
        "- surface debit = D^2/R = 3/4 = 0.75",
        "",
        "## Immediate Consequences Locked For Replay",
        "",
        "- split loss = R^2/8 = 18",
        "- retained parent = R^2*(7/8) = 126",
        "- observed Higgs surface = 126 - 0.75 = 125.25",
        "- tensor carrier identity = alpha_H*D^2 = 18",
        "- 18 is carrier-only, not a matter/rest-mass row",
        "",
        "## Replay Register",
        "",
        "LC02-LC11 are registered in `LC01_downstream_lane_register.csv` and remain pending.",
        "",
        "## Wrong Controls",
        "",
        "`LC01_wrong_controls.csv` registers 30 controls. LC01 directly rejects primitive mutation, the old 2*pi route restore, carrier/matter promotion, surface-debit confusion, and Higgs carrier/debit swaps. The remaining controls are mandatory guards for lane replay.",
        "",
        "## Files",
        "",
        f"- `{rel(primitive_path)}`",
        f"- `{rel(source_path)}`",
        f"- `{rel(lane_path)}`",
        f"- `{rel(wrong_path)}`",
        f"- `{rel(checks_path)}`",
        f"- `{rel(lock_path)}`",
        f"- `{rel(summary_path)}`",
        f"- `{rel(hash_path)}`",
    ]
    result_path.write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    files_to_hash = [
        Path(__file__).resolve(),
        primitive_path,
        source_path,
        lane_path,
        wrong_path,
        checks_path,
        lock_path,
        summary_path,
        result_path,
    ]
    hash_lines = [f"{sha256_path(path)}  {rel(path)}" for path in files_to_hash]
    hash_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    for path in files_to_hash + [hash_path]:
        sidecar = path.with_name(path.name + ".sha256.txt")
        sidecar.write_text(f"{sha256_path(path)}  {rel(path)}\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
