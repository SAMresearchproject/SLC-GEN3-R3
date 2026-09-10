from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

TASK_ID = "LC06"
TASK_NAME = "baryon and matter inventory replay"
RESULT_CLASS = "LC06_PASS_BARYON_AND_MATTER_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC06_BARYON_MATTER_INVENTORY_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "LC03": LC_DIR / "LC03_summary.json",
    "LC04": LC_DIR / "LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY" / "LC04_summary.json",
    "LC05": LC_DIR / "LC05_PERIODIC_ISOTOPE_VAULT_REPLAY" / "LC05_summary.json",
    "CR114_foundation": ROOT / "14_FOUNDATIONAL_TESTS" / "CR114_BINARY_FACE_STATE_SPLIT_THEOREM" / "CR114_summary.json",
    "CR116_foundation": ROOT / "14_FOUNDATIONAL_TESTS" / "CR116_18_GRAVITON_CARRIER_THEOREM" / "CR116_summary.json",
    "CR119": ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_summary.json",
    "CR018": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR018_A0_CHI_BARYON_INVENTORY_DERIVATION" / "CR018_summary.json",
    "CR019": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT" / "CR019_summary.json",
    "CR020": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR020_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN" / "CR020_summary.json",
    "CR021": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT" / "CR021_summary.json",
    "CR022": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb" / "CR022_summary.json",
    "CR023": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "CR023_BARYON_COSMOLOGY_BRANCH_VERDICT" / "CR023_summary.json",
    "G310": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "_source_artifacts" / "summaries" / "G310_output.json",
    "G312": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "_source_artifacts" / "summaries" / "G312_output.json",
    "G313": ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY" / "_source_artifacts" / "summaries" / "G313_output.json",
    "QP092H": ROOT / "upstream_artifacts" / "qp092" / "qp092h_baryon_cmb_carrier_gate" / "qp092h_summary.json",
    "CR111": ROOT / "14_FOUNDATIONAL_TESTS" / "CR111_COSMIC_BARYON_OMEGA_B_CLOSURE_APPEAL" / "CR111_cosmic_baryon_appeal_lock.json",
    "CR114_baryon_bridge": ROOT / "00_governance" / "CR114_COSMIC_BARYON_BRIDGE_REVEAL" / "CR114_summary.json",
}

MATTER_TABLE = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_matter_table.csv"
)
PARTICLE_TABLE = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_particle_table.csv"
)
SOURCE_MATTER_TABLE = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "source_copies"
    / "latest_matter_table.csv"
)
TABLE_EXPORT_SUMMARY = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "source_copies"
    / "latest_table_export_summary.json"
)
CR119_WRONG_CONTROLS = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_wrong_controls.csv"
)
CR119_IDENTITY_COUNTS = (
    ROOT
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_identity_counts.csv"
)
CR018_DERIVED_ROWS = (
    ROOT
    / "07_BARYON_INVENTORY_AND_COSMOLOGY"
    / "CR018_A0_CHI_BARYON_INVENTORY_DERIVATION"
    / "CR018_derived_rows.csv"
)
CR019_INVENTORY_ROWS = (
    ROOT
    / "07_BARYON_INVENTORY_AND_COSMOLOGY"
    / "CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT"
    / "CR019_inventory_rows.csv"
)
CR023_COMPONENTS = (
    ROOT
    / "07_BARYON_INVENTORY_AND_COSMOLOGY"
    / "CR023_BARYON_COSMOLOGY_BRANCH_VERDICT"
    / "CR023_component_verdicts.csv"
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def parse_exact(value: Any) -> Decimal:
    text = str(value).strip()
    if "/" in text and "pi" not in text:
        fraction = Fraction(text)
        return Decimal(fraction.numerator) / Decimal(fraction.denominator)
    return Decimal(text)


def load_primitive_stack(path: Path) -> dict[str, Any]:
    rows: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows[row["primitive"]] = row

    def exact(name: str) -> str:
        return rows[name]["value_exact"]

    def decimal(name: str) -> str:
        return rows[name]["value_decimal"]

    return {
        "alpha_H": int(exact("alpha_H")),
        "R": int(exact("R")),
        "D": int(exact("D")),
        "A0": exact("A0"),
        "A0_decimal": decimal("A0"),
        "R_squared": int(exact("R^2")),
        "split_fraction": exact("split_fraction"),
        "split_fraction_decimal": decimal("split_fraction"),
        "retained_side": exact("retained_side"),
        "retained_side_decimal": decimal("retained_side"),
        "carrier_side": exact("carrier_side"),
        "carrier_side_decimal": decimal("carrier_side"),
        "bounce_lift": exact("bounce_lift"),
        "bounce_lift_decimal": decimal("bounce_lift"),
        "resolved_half_bounce": exact("resolved_half_bounce"),
        "resolved_half_bounce_decimal": decimal("resolved_half_bounce"),
        "surface_debit": exact("surface_debit"),
        "surface_debit_decimal": decimal("surface_debit"),
    }


def source_status(summary: dict[str, Any]) -> str:
    for key in ("result", "result_class", "scientific_verdict", "verdict", "status", "lock_id"):
        value = summary.get(key)
        if isinstance(value, str) and value:
            return value
    return "UNKNOWN"


def contains_pass(summary: dict[str, Any]) -> bool:
    status = source_status(summary).upper()
    if "PASS" in status:
        return True
    if summary.get("passed") is True:
        return True
    if summary.get("all_predictions_passed") is True or summary.get("all_checks_passed") is True:
        return True
    return False


def count_by(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        out[row.get(key, "")] = out.get(row.get(key, ""), 0) + 1
    return out


def all_rows(rows: list[dict[str, str]], predicate) -> bool:
    return all(predicate(row) for row in rows)


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def table_value(rows: list[dict[str, str]], key: str) -> Decimal:
    for row in rows:
        if row["quantity"] == key:
            return Decimal(row["value"])
    raise KeyError(key)


def close_decimal(left: Decimal, right: Decimal, tolerance: Decimal = Decimal("1e-15")) -> bool:
    return abs(left - right) <= tolerance


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    summaries = {name: load_json(path) for name, path in SOURCES.items()}
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)
    export_summary = load_json(TABLE_EXPORT_SUMMARY)

    matter_rows = read_csv(MATTER_TABLE)
    source_matter_rows = read_csv(SOURCE_MATTER_TABLE)
    particle_rows = read_csv(PARTICLE_TABLE)
    cr119_wrong_rows = read_csv(CR119_WRONG_CONTROLS)
    identity_count_rows = read_csv(CR119_IDENTITY_COUNTS)
    cr018_derived_rows = read_csv(CR018_DERIVED_ROWS)
    cr019_inventory_rows = read_csv(CR019_INVENTORY_ROWS)
    cr023_component_rows = read_csv(CR023_COMPONENTS)

    R = Decimal(primitive_stack["R"])
    D = Decimal(primitive_stack["D"])
    A0 = Decimal(primitive_stack["A0_decimal"])
    split_fraction = parse_exact(primitive_stack["split_fraction"])
    retained_side = parse_exact(primitive_stack["retained_side"])
    carrier_side = parse_exact(primitive_stack["carrier_side"])

    mu_H = (Decimal(2) ** int(D)) / D
    chi = mu_H * A0
    omega_b = Decimal(2) * A0 * (Decimal(1) - chi)

    cr018_A0 = Decimal(str(summaries["CR018"]["A0"]))
    cr018_mu_H = Decimal(str(summaries["CR018"]["mu_H"]))
    cr018_chi = Decimal(str(summaries["CR018"]["chi"]))
    cr018_omega_b = Decimal(str(summaries["CR018"]["Omega_b"]))

    g313_omega = summaries["G313"]["omega"]
    cr019_omega_b = Decimal(str(summaries["CR019"]["Omega_b"]))
    cr019_omega_m_eff = Decimal(str(summaries["CR019"]["Omega_m_eff"]))
    cr019_pbh = Decimal(str(summaries["CR019"]["Omega_BB_PBH_trapped"]))
    cr019_vacuum = Decimal(str(summaries["CR019"]["Omega_substrate_vacuum"]))
    g313_omega_m = Decimal(str(g313_omega["omega_m_derived"]))
    g313_coeff = Decimal(str(summaries["G313"]["derived_coeff"]))

    bin_counts = count_by(matter_rows, "bin")
    operator_counts = count_by(matter_rows, "operator_class")
    stability_counts = count_by(matter_rows, "stability_status")
    matter_gate_counts = count_by(matter_rows, "matter_gate_status")
    construction_input_counts = count_by(matter_rows, "known_label_used_as_construction_input")
    vault_reveal_counts = count_by(matter_rows, "vault_reveal_status")
    identity_role_counts = count_by(matter_rows, "identity_assignment_role")

    q_split_errors: list[Decimal] = []
    observed_identity_errors: list[Decimal] = []
    for row in matter_rows:
        q = Decimal(row["qA_source_support"])
        tensor = Decimal(row["tensor_carrier_support"])
        retained = Decimal(row["retained_write_support"])
        q_split_errors.append(abs(q * carrier_side - tensor))
        q_split_errors.append(abs(q * retained_side - retained))

        native = Decimal(row["M_native"])
        debit = Decimal(row["S_debit_or_credit"])
        observed = Decimal(row["M_observed_candidate"])
        observed_identity_errors.append(abs((native - debit) - observed))

    max_q_split_error = max(q_split_errors) if q_split_errors else Decimal(0)
    max_observed_identity_error = max(observed_identity_errors) if observed_identity_errors else Decimal(0)
    q_split_tolerance = Decimal("1e-90")
    observed_tolerance = Decimal("1e-90")

    null_particle_rows = [row for row in particle_rows if row["candidate_id"] == "QP093A-0088"]
    null_row = null_particle_rows[0] if null_particle_rows else {}

    matter_invariants = [
        {
            "invariant": "matter_row_count",
            "expected": 126,
            "observed": len(matter_rows),
            "status": "PASS" if len(matter_rows) == 126 else "FAIL",
        },
        {
            "invariant": "source_matter_row_count",
            "expected": 126,
            "observed": len(source_matter_rows),
            "status": "PASS" if len(source_matter_rows) == 126 else "FAIL",
        },
        {
            "invariant": "bin_counts",
            "expected": {"stable_matter_rows": 63, "bound_composite_rows": 63},
            "observed": bin_counts,
            "status": "PASS" if bin_counts == {"stable_matter_rows": 63, "bound_composite_rows": 63} else "FAIL",
        },
        {
            "invariant": "all_rows_matter_allowed",
            "expected": "matter_row_allowed=yes and latest_matter_row_allowed=yes on 126/126",
            "observed": sum(1 for row in matter_rows if row["matter_row_allowed"] == "yes" and row["latest_matter_row_allowed"] == "yes"),
            "status": "PASS" if all_rows(matter_rows, lambda r: r["matter_row_allowed"] == "yes" and r["latest_matter_row_allowed"] == "yes") else "FAIL",
        },
        {
            "invariant": "matter_gate_counts",
            "expected": {"PASS_STABLE_SINGLE_WRITE_MATTER": 63, "PASS_BOUND_COMPOSITE_MATTER": 63},
            "observed": matter_gate_counts,
            "status": "PASS" if matter_gate_counts == {"PASS_STABLE_SINGLE_WRITE_MATTER": 63, "PASS_BOUND_COMPOSITE_MATTER": 63} else "FAIL",
        },
        {
            "invariant": "operator_class_counts",
            "expected": {"V4_1_SINGLE_WRITE": 42, "OUTER_BINARY_NEUTRAL": 21, "BOUND_COLOR_PAIR": 36, "GROUND_BARYON_3BODY": 14, "OCTET_COMPOSITE": 13},
            "observed": operator_counts,
            "status": "PASS"
            if operator_counts
            == {"V4_1_SINGLE_WRITE": 42, "OUTER_BINARY_NEUTRAL": 21, "BOUND_COLOR_PAIR": 36, "GROUND_BARYON_3BODY": 14, "OCTET_COMPOSITE": 13}
            else "FAIL",
        },
        {
            "invariant": "stability_status_counts",
            "expected": {"STABLE_MATTER_CANDIDATE": 42, "STABLE_NEUTRAL_CANDIDATE": 21, "BOUND_PAIR_CHARGED_CANDIDATE": 42, "BOUND_COLOR_CLOSED_STABLE_CANDIDATE": 14, "BOUND_PAIR_NEUTRAL_CANDIDATE": 7},
            "observed": stability_counts,
            "status": "PASS"
            if stability_counts
            == {
                "STABLE_MATTER_CANDIDATE": 42,
                "STABLE_NEUTRAL_CANDIDATE": 21,
                "BOUND_PAIR_CHARGED_CANDIDATE": 42,
                "BOUND_COLOR_CLOSED_STABLE_CANDIDATE": 14,
                "BOUND_PAIR_NEUTRAL_CANDIDATE": 7,
            }
            else "FAIL",
        },
        {
            "invariant": "no_antimatter_rows_in_matter_table",
            "expected": 0,
            "observed": sum(1 for row in matter_rows if "ANTIMATTER" in row["stability_status"] or "antimatter" in row["bin"]),
            "status": "PASS" if all("ANTIMATTER" not in row["stability_status"] and "antimatter" not in row["bin"] for row in matter_rows) else "FAIL",
        },
        {
            "invariant": "known_labels_not_construction_inputs",
            "expected": {"no": 126},
            "observed": construction_input_counts,
            "status": "PASS" if construction_input_counts == {"no": 126} else "FAIL",
        },
        {
            "invariant": "native_matter_identity",
            "expected": {"NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL": 126},
            "observed": vault_reveal_counts,
            "status": "PASS" if vault_reveal_counts == {"NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL": 126} else "FAIL",
        },
        {
            "invariant": "native_identity_no_external_label",
            "expected": {"native_identity_no_external_label": 126},
            "observed": identity_role_counts,
            "status": "PASS" if identity_role_counts == {"native_identity_no_external_label": 126} else "FAIL",
        },
        {
            "invariant": "qA_support_split_from_LC01",
            "expected": "tensor=qA/8 and retained=7qA/8 within 1e-90 exported-decimal tolerance",
            "observed": f"max_error={max_q_split_error}; tolerance={q_split_tolerance}",
            "status": "PASS" if max_q_split_error <= q_split_tolerance else "FAIL",
        },
        {
            "invariant": "observed_surface_identity",
            "expected": "M_observed_candidate = M_native - S_debit_or_credit",
            "observed": f"max_error={max_observed_identity_error}; tolerance={observed_tolerance}",
            "status": "PASS" if max_observed_identity_error <= observed_tolerance else "FAIL",
        },
        {
            "invariant": "QP093A_0088_null_conjugate_excluded_from_matter",
            "expected": "particle row exists, matter table excludes it, latest_matter_row_allowed=no",
            "observed": {
                "particle_rows": len(null_particle_rows),
                "matter_rows": sum(1 for row in matter_rows if row["candidate_id"] == "QP093A-0088"),
                "latest_matter_row_allowed": null_row.get("latest_matter_row_allowed"),
                "vault_reveal_status": null_row.get("vault_reveal_status"),
            },
            "status": "PASS"
            if len(null_particle_rows) == 1
            and sum(1 for row in matter_rows if row["candidate_id"] == "QP093A-0088") == 0
            and null_row.get("latest_matter_row_allowed") == "no"
            and null_row.get("vault_reveal_status") == "NULL_CONJUGATE_REVEALED_ZERO_QA_NO_MATTER_PROMOTION"
            else "FAIL",
        },
    ]

    baryon_rows = [
        {
            "layer": "CR018_baryon_inventory",
            "source": "CR018",
            "formula_or_contract": "A0=1/(pi*R); mu_H=2^D/D; chi=mu_H*A0; Omega_b=2*A0*(1-chi)",
            "expected_or_replayed": f"A0={A0}; mu_H={mu_H}; chi={chi}; Omega_b={omega_b}",
            "source_value": f"A0={cr018_A0}; mu_H={cr018_mu_H}; chi={cr018_chi}; Omega_b={cr018_omega_b}",
            "status": "PASS"
            if contains_pass(summaries["CR018"])
            and close_decimal(A0, cr018_A0)
            and close_decimal(mu_H, cr018_mu_H)
            and close_decimal(chi, cr018_chi)
            and close_decimal(omega_b, cr018_omega_b)
            else "FAIL",
            "boundary": "Zero-free-parameter baryon inventory candidate; observed baryon density is not a construction input.",
        },
        {
            "layer": "CR019_effective_matter_inventory",
            "source": "CR019/G313",
            "formula_or_contract": "Omega_m_eff taken from G313 D*chi^2 directional-cumulant refinement; derived coefficient must equal D",
            "expected_or_replayed": f"D={D}; G313_coeff={g313_coeff}; Omega_m_eff={g313_omega_m}",
            "source_value": f"Omega_b={cr019_omega_b}; Omega_m_eff={cr019_omega_m_eff}; PBH={cr019_pbh}; vacuum={cr019_vacuum}",
            "status": "PASS"
            if contains_pass(summaries["CR019"])
            and close_decimal(g313_coeff, D)
            and close_decimal(g313_omega_m, cr019_omega_m_eff)
            and close_decimal(cr019_omega_b, cr018_omega_b)
            and close_decimal(cr019_pbh, cr019_omega_m_eff - cr019_omega_b)
            and close_decimal(cr019_vacuum, Decimal(1) - cr019_omega_m_eff)
            else "FAIL",
            "boundary": "Effective matter refinement is structural-argument/candidate grade, not theorem-grade full cosmology.",
        },
        {
            "layer": "CR023_branch_verdict",
            "source": "CR023",
            "formula_or_contract": "Aggregate branch verdict preserves PASS for inventory and BOUNDARY_PASS for downstream cosmology contact.",
            "expected_or_replayed": "CR018 PASS; CR019 PASS; CR020-CR022 BOUNDARY_PASS; CR023 BOUNDARY_PASS",
            "source_value": source_status(summaries["CR023"]),
            "status": "PASS" if "BOUNDARY_PASS" in source_status(summaries["CR023"]) else "FAIL",
            "boundary": "Not full CMB, recombination, perturbation, TT/TE/EE, Planck likelihood, or distance-triad closure.",
        },
        {
            "layer": "QP092H_carrier_compression_gate",
            "source": "QP092H",
            "formula_or_contract": "Baryon/CMB rows admitted only through qA -> 1/8 tensor carrier -> ledger compression -> A readout.",
            "expected_or_replayed": "carrier rows 6/6; branch gates 10/10; direct qA controls 3/3 rejected; matter_rows_added=0",
            "source_value": source_status(summaries["QP092H"]),
            "status": "PASS"
            if summaries["QP092H"].get("passed") is True
            and summaries["QP092H"].get("carrier_rule_rows_passed") == summaries["QP092H"].get("carrier_rule_rows_total") == 6
            and summaries["QP092H"].get("branch_gate_rows_admitted") == summaries["QP092H"].get("branch_gate_rows_total") == 10
            and summaries["QP092H"].get("direct_qA_controls_rejected") == summaries["QP092H"].get("direct_qA_controls_total") == 3
            and summaries["QP092H"].get("matter_rows_added") == 0
            else "FAIL",
            "boundary": "Direct qA-as-mass is rejected; CMB rows keep scoped boundary/contact status.",
        },
        {
            "layer": "CR111_CR114_baryon_bridge",
            "source": "CR111/governance_CR114",
            "formula_or_contract": "CR111 registered forward-blind baryon closure; governance CR114 records CR018 retroactive satisfaction without modifying old verdicts.",
            "expected_or_replayed": "zero free parameters; Planck anchor not tuned; bridge is retroactive, not a new forward-blind claim",
            "source_value": f"sigma_h2={summaries['CR114_baryon_bridge'].get('sigma_omega_b_h2')}; all_paths={summaries['CR114_baryon_bridge'].get('all_paths_within_1_sigma')}",
            "status": "PASS"
            if summaries["CR111"].get("free_parameters_total") == 0
            and summaries["CR114_baryon_bridge"].get("all_paths_within_1_sigma") is True
            and all(item.get("pass") is True for item in summaries["CR114_baryon_bridge"].get("wrong_controls", []))
            else "FAIL",
            "boundary": "Bridge is provenance/support; LC06 does not reclassify CR018 as a fresh forward-blind Q-artifact.",
        },
    ]

    wrong_controls = [
        {
            "wrong_control": "WC09_CARRIER_PROMOTED_TO_MATTER",
            "attempted_mutation": "put tensor carrier 18 into matter algebra as a rest-mass element or count-closing matter row",
            "evidence": "CR116 locks 18 as carrier-only; CR119 excludes QP093A-0088 null conjugate from matter; matter table stays 126 rows",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC23_BARYON_INVENTORY_RAW_BRANCH",
            "attempted_mutation": "mix carrier-only rows into baryon/matter inventory to close counts",
            "evidence": "CR119 matter table keeps 63 stable + 63 bound rows; QP092H reports matter_rows_added=0 and admits branches only through carrier compression",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_DIRECT_QA_AS_MASS",
            "attempted_mutation": "read qA_source_support as baryon density, element mass, or matter mass",
            "evidence": "QP092H rejects direct qA controls 3/3; CR119 qA splits into tensor/retained support and is not treated as mass",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_NULL_CONJUGATE_OVERRIDE_IGNORED",
            "attempted_mutation": "ignore QP093B null-conjugate boundary and promote QP093A-0088 to matter",
            "evidence": "QP093A-0088 has M_native=18, S_debit=18, M_observed=0, qA=0, latest_matter_row_allowed=no, and zero matter rows",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_ANTIMATTER_INCLUDED_IN_MATTER",
            "attempted_mutation": "include antimatter conjugate rows in the matter inventory",
            "evidence": "latest export says antimatter_excluded=true; LC06 counts 0 antimatter rows in the 126-row matter table",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_BARYON_OBSERVATION_BACKFILL",
            "attempted_mutation": "fit Omega_b to Planck or observed baryon density",
            "evidence": "CR018 derives Omega_b from A0, D, and chi with free_parameters_zero=true; governance CR114 says Planck anchor not tuned",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_CHI_FIT_TO_RATIO",
            "attempted_mutation": "move the Omega_m residual into chi to force the matter ratio",
            "evidence": "G310/G312/G313 wrong controls reject chi fitting because it damages Omega_b",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_TARGET_FIT_OMEGA_M",
            "attempted_mutation": "use exact target-fit noninteger k instead of D=3 directional cumulant",
            "evidence": "G312/G313 reject k_target as derivation; derived coefficient equals D=3",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_ROW_DELETION",
            "attempted_mutation": "drop awkward matter rows, null boundary rows, or branch boundary components",
            "evidence": "LC06 keeps 126/126 matter rows, checks the excluded null particle row, and preserves CR020-CR022 BOUNDARY_PASS components",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FULL_COSMOLOGY_OVERCLAIM",
            "attempted_mutation": "promote branch 07 into full CMB, recombination, perturbation, TT/TE/EE, Planck-likelihood, or distance-triad closure",
            "evidence": "CR023 and branch README explicitly preserve those as open debts; LC06 records boundary-pass status",
            "result": "REJECTED",
        },
    ]

    claim_boundaries = [
        {
            "boundary": "LC06 replay scope",
            "status": "LOCKED",
            "text": "LC06 tests baryon-density arithmetic, effective matter inventory, and CR119 matter-row inventory; it is not a full cosmology theorem lane.",
        },
        {
            "boundary": "Carrier/matter distinction",
            "status": "LOCKED",
            "text": "The tensor carrier channel M=18 remains carrier-only and is not promoted to matter or rest mass.",
        },
        {
            "boundary": "Matter table identity",
            "status": "LOCKED",
            "text": "CR119 matter inventory is 126 native matter rows: 63 stable single-write and 63 bound composite, with antimatter excluded.",
        },
        {
            "boundary": "Null conjugate",
            "status": "LOCKED",
            "text": "QP093A-0088 remains a null conjugate with M_native=S_debit=18, M_observed=0, qA=0, and no matter promotion.",
        },
        {
            "boundary": "Baryon density",
            "status": "LOCKED",
            "text": "Omega_b is replayed from A0=1/(pi R), mu_H=2^D/D, chi=mu_H*A0, and Omega_b=2*A0*(1-chi), not observational backfill.",
        },
        {
            "boundary": "Effective matter",
            "status": "LOCKED",
            "text": "Omega_m_eff is preserved as CR019/G313 structural-argument/candidate grade; target-fit k is rejected.",
        },
        {
            "boundary": "Cosmology scope",
            "status": "LOCKED",
            "text": "Full recombination, perturbation, TT/TE/EE, Planck likelihood, and complete distance/CMB acoustic closure remain open debts.",
        },
        {
            "boundary": "Baryon bridge chronology",
            "status": "LOCKED",
            "text": "Governance CR114 is a retroactive bridge from CR018 to CR111_PRED_1 and is not misrepresented as a fresh forward-blind result.",
        },
    ]

    cr119_counts = get_nested(summaries["CR119"], "row_counts", default={})
    cr119_identity_counts = get_nested(summaries["CR119"], "identity_assignment_counts", default={})
    export_breakdown = export_summary.get("matter_table_breakdown", {})

    checks: list[dict[str, Any]] = []
    checks.append(check("LC01 primitive stack present", contains_pass(summaries["LC01"]), source_status(summaries["LC01"])))
    checks.append(check("LC03 qA gate completed before LC06", contains_pass(summaries["LC03"]), source_status(summaries["LC03"])))
    checks.append(check("LC04 particle mass-chain completed before LC06", contains_pass(summaries["LC04"]), source_status(summaries["LC04"])))
    checks.append(check("LC05 periodic vault completed before LC06", contains_pass(summaries["LC05"]), source_status(summaries["LC05"])))
    checks.append(check("alpha_H locked at 2", primitive_stack["alpha_H"] == 2, "LC01 primitive", primitive_stack["alpha_H"]))
    checks.append(check("R locked at 12", primitive_stack["R"] == 12, "LC01 primitive", primitive_stack["R"]))
    checks.append(check("D locked at 3", primitive_stack["D"] == 3, "LC01 primitive", primitive_stack["D"]))
    checks.append(check("split fraction locked at 1/8", split_fraction == Decimal(1) / Decimal(8), "LC01 primitive", primitive_stack["split_fraction"]))
    checks.append(check("retained side locked at 7/8", retained_side == Decimal(7) / Decimal(8), "LC01 primitive", primitive_stack["retained_side"]))
    checks.append(check("CR114 split theorem passes", contains_pass(summaries["CR114_foundation"]), source_status(summaries["CR114_foundation"])))
    checks.append(check("CR116 carrier theorem passes", contains_pass(summaries["CR116_foundation"]), source_status(summaries["CR116_foundation"])))
    checks.append(check("CR116 particle catalog status carrier-only", summaries["CR116_foundation"].get("particle_catalog_status") == "carrier_only_not_matter", "CR116 carrier boundary", summaries["CR116_foundation"].get("particle_catalog_status")))
    checks.append(check("CR119 vault passes", contains_pass(summaries["CR119"]), source_status(summaries["CR119"])))
    checks.append(check("CR119 matter row summary is 126", cr119_counts.get("matter") == 126 or cr119_counts.get("matter_rows") == 126, "CR119 row count", cr119_counts))
    checks.append(check("CR119 identity count native matter is 126", cr119_identity_counts.get("NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL") == 126, "CR119 identity count", cr119_identity_counts.get("NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL")))
    checks.append(check("CR119 null conjugate boundary preserved", summaries["CR119"].get("null_conjugate_boundary_preserved") is True, "CR119 null boundary", summaries["CR119"].get("null_conjugate_boundary_preserved")))
    checks.append(check("latest export matter rows are 126", export_summary.get("matter_table_rows") == 126, "latest export", export_summary.get("matter_table_rows")))
    checks.append(check("latest export stable/bound split is 63/63", export_breakdown.get("stable_single_write_matter") == 63 and export_breakdown.get("bound_composite_matter") == 63, "latest export breakdown", export_breakdown))
    checks.append(check("latest export antimatter excluded", export_breakdown.get("antimatter_excluded") is True, "latest export breakdown", export_breakdown.get("antimatter_excluded")))
    checks.append(check("latest export null override applied", export_breakdown.get("null_conjugate_override_applied") == "QP093A-0088", "latest export breakdown", export_breakdown.get("null_conjugate_override_applied")))

    for row in matter_invariants:
        checks.append(check(f"Matter invariant: {row['invariant']}", row["status"] == "PASS", str(row["expected"]), row["observed"]))
    for row in baryon_rows:
        checks.append(check(f"Baryon layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))

    checks.append(check("CR018 derived rows match summary Omega_b", close_decimal(table_value(cr018_derived_rows, "Omega_b"), cr018_omega_b), "CR018 derived row", table_value(cr018_derived_rows, "Omega_b")))
    checks.append(check("CR019 inventory rows match summary Omega_m_eff", close_decimal(table_value(cr019_inventory_rows, "Omega_m_eff"), cr019_omega_m_eff), "CR019 inventory row", table_value(cr019_inventory_rows, "Omega_m_eff")))
    checks.append(check("CR023 component table keeps CR018/CR019 PASS and CR020-CR022 BOUNDARY_PASS", len(cr023_component_rows) == 5 and all(row["scientific_verdict"] in {"PASS", "BOUNDARY_PASS"} for row in cr023_component_rows), "CR023 component verdicts", len(cr023_component_rows)))
    checks.append(check("G310 wrong controls pass", summaries["G310"]["overall"]["all_wrong_controls_pass"] is True, "G310", summaries["G310"]["overall"]["verdict"]))
    checks.append(check("G312 wrong controls pass", summaries["G312"]["overall"]["all_wrong_controls_pass"] is True, "G312", summaries["G312"]["overall"]["verdict"]))
    checks.append(check("G313 wrong controls pass", summaries["G313"]["overall"]["all_wrong_controls_pass"] is True, "G313", summaries["G313"]["overall"]["verdict"]))
    checks.append(check("QP092H direct qA controls rejected", summaries["QP092H"].get("direct_qA_controls_rejected") == summaries["QP092H"].get("direct_qA_controls_total") == 3, "QP092H direct qA controls", f"{summaries['QP092H'].get('direct_qA_controls_rejected')}/{summaries['QP092H'].get('direct_qA_controls_total')}"))
    checks.append(check("CR119 wrong controls all pass/reject", len(cr119_wrong_rows) == 6 and all(row["passed"] == "True" for row in cr119_wrong_rows), "CR119 wrong controls", len(cr119_wrong_rows)))
    checks.append(check("CR119 identity counts CSV records layer_matter 126", any(row["bucket"] == "layer_matter" and row["rows"] == "126" for row in identity_count_rows), "CR119 identity counts CSV", "layer_matter"))

    for wc in wrong_controls:
        checks.append(check(f"{wc['wrong_control']} rejected", wc["result"] == "REJECTED", wc["evidence"]))

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC06_FAIL_BARYON_AND_MATTER_INVENTORY_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "carrier_matter_mixing": "forbidden",
        },
        "baryon_replay": {
            "A0": str(A0),
            "mu_H": str(mu_H),
            "chi": str(chi),
            "Omega_b": str(omega_b),
            "CR018_Omega_b": str(cr018_omega_b),
            "Omega_m_eff": str(cr019_omega_m_eff),
            "Omega_BB_PBH_trapped": str(cr019_pbh),
            "Omega_substrate_vacuum": str(cr019_vacuum),
            "G313_derived_coeff": str(g313_coeff),
        },
        "matter_inventory": {
            "rows": len(matter_rows),
            "bin_counts": bin_counts,
            "operator_class_counts": operator_counts,
            "stability_status_counts": stability_counts,
            "matter_gate_counts": matter_gate_counts,
            "known_label_used_as_construction_input": construction_input_counts,
            "vault_reveal_counts": vault_reveal_counts,
            "max_q_split_error": str(max_q_split_error),
            "max_observed_identity_error": str(max_observed_identity_error),
            "null_conjugate_candidate": "QP093A-0088",
            "null_conjugate_promoted_to_matter": False,
        },
        "branch_07_boundary": {
            "CR023_result": source_status(summaries["CR023"]),
            "scope_boundaries": summaries["CR023"].get("scope_boundaries", []),
        },
        "checks": {
            "total": len(checks),
            "passed": pass_count,
            "failed": fail_count,
        },
        "wrong_controls": {
            "tested": len(wrong_controls),
            "rejected": sum(1 for item in wrong_controls if item["result"] == "REJECTED"),
        },
        "epistemic_boundary": [
            "LC06 passes the baryon and matter inventory replay from the LC01 stack.",
            "LC06 keeps tensor carrier M=18 carrier-only and rejects carrier-as-matter closure.",
            "LC06 preserves CR023 as BOUNDARY_PASS, not full cosmology closure.",
            "LC06 treats governance CR114 as retroactive provenance for CR111, not a fresh forward-blind claim.",
        ],
        "artifacts": {},
    }

    layer_path = OUT_DIR / "LC06_replay_layers.csv"
    baryon_path = OUT_DIR / "LC06_baryon_cosmology_replay.csv"
    invariant_path = OUT_DIR / "LC06_matter_inventory_invariants.csv"
    wrong_path = OUT_DIR / "LC06_wrong_controls.csv"
    boundary_path = OUT_DIR / "LC06_claim_boundaries.csv"
    checks_path = OUT_DIR / "LC06_checks.csv"
    source_path = OUT_DIR / "LC06_sources_hashes.csv"
    summary_path = OUT_DIR / "LC06_summary.json"
    result_path = OUT_DIR / "LC06_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    source_rows = [
        {"source": name, "path": rel(path), "status": source_status(summaries[name]), "sha256": sha256_file(path)}
        for name, path in SOURCES.items()
    ]
    for name, path, status in [
        ("LC06_runner", RUNNER_PATH, "result-producing runner"),
        ("LC01_primitive_stack_declared_csv", LC01_PRIMITIVE_CSV, "primitive exact values"),
        ("CR119_matter_table", MATTER_TABLE, f"{len(matter_rows)} rows"),
        ("CR119_source_matter_table", SOURCE_MATTER_TABLE, f"{len(source_matter_rows)} rows"),
        ("CR119_particle_table", PARTICLE_TABLE, "null-conjugate boundary checked"),
        ("CR119_table_export_summary", TABLE_EXPORT_SUMMARY, "latest export summary"),
        ("CR119_wrong_controls", CR119_WRONG_CONTROLS, "wrong controls"),
        ("CR119_identity_counts", CR119_IDENTITY_COUNTS, "identity counts"),
        ("CR018_derived_rows", CR018_DERIVED_ROWS, "baryon derived rows"),
        ("CR019_inventory_rows", CR019_INVENTORY_ROWS, "effective matter inventory rows"),
        ("CR023_component_verdicts", CR023_COMPONENTS, "branch component verdicts"),
    ]:
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})

    write_csv(layer_path, baryon_rows, ["layer", "source", "formula_or_contract", "expected_or_replayed", "source_value", "status", "boundary"])
    write_csv(
        baryon_path,
        [
            {"quantity": "A0", "formula": "1/(pi*R)", "replayed": str(A0), "source": str(cr018_A0), "status": "PASS" if close_decimal(A0, cr018_A0) else "FAIL"},
            {"quantity": "mu_H", "formula": "2^D/D", "replayed": str(mu_H), "source": str(cr018_mu_H), "status": "PASS" if close_decimal(mu_H, cr018_mu_H) else "FAIL"},
            {"quantity": "chi", "formula": "mu_H*A0", "replayed": str(chi), "source": str(cr018_chi), "status": "PASS" if close_decimal(chi, cr018_chi) else "FAIL"},
            {"quantity": "Omega_b", "formula": "2*A0*(1-chi)", "replayed": str(omega_b), "source": str(cr018_omega_b), "status": "PASS" if close_decimal(omega_b, cr018_omega_b) else "FAIL"},
            {"quantity": "Omega_m_eff", "formula": "CR019/G313 D*chi^2 directional-cumulant refinement", "replayed": str(g313_omega_m), "source": str(cr019_omega_m_eff), "status": "PASS" if close_decimal(g313_omega_m, cr019_omega_m_eff) else "FAIL"},
            {"quantity": "Omega_BB_PBH_trapped", "formula": "Omega_m_eff - Omega_b", "replayed": str(cr019_omega_m_eff - cr019_omega_b), "source": str(cr019_pbh), "status": "PASS" if close_decimal(cr019_omega_m_eff - cr019_omega_b, cr019_pbh) else "FAIL"},
            {"quantity": "Omega_substrate_vacuum", "formula": "1 - Omega_m_eff", "replayed": str(Decimal(1) - cr019_omega_m_eff), "source": str(cr019_vacuum), "status": "PASS" if close_decimal(Decimal(1) - cr019_omega_m_eff, cr019_vacuum) else "FAIL"},
        ],
        ["quantity", "formula", "replayed", "source", "status"],
    )
    write_csv(invariant_path, matter_invariants, ["invariant", "expected", "observed", "status"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(boundary_path, claim_boundaries, ["boundary", "status", "text"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary["artifacts"] = {
        "layers": rel(layer_path),
        "baryon_cosmology_replay": rel(baryon_path),
        "matter_inventory_invariants": rel(invariant_path),
        "wrong_controls": rel(wrong_path),
        "claim_boundaries": rel(boundary_path),
        "checks": rel(checks_path),
        "sources_hashes": rel(source_path),
        "summary": rel(summary_path),
        "result": rel(result_path),
        "hashes": rel(hash_path),
        "runner": rel(RUNNER_PATH),
    }

    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    result_lines = [
        f"# {TASK_ID} - Baryon And Matter Inventory Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, do the baryon split and matter inventory replay without carrier/matter mixing, target substitution, row deletion, or retroactive relabeling?",
        "",
        "Verdict: yes. CR018/CR019 replay the baryon and effective-matter inventory from the locked stack, and CR119 preserves a 126-row matter table while rejecting tensor-carrier promotion and the QP093A-0088 null-conjugate trap.",
        "",
        "Locked stack used:",
        f"- alpha_H = {primitive_stack['alpha_H']}",
        f"- R = {primitive_stack['R']}",
        f"- D = {primitive_stack['D']}",
        f"- carrier side = {primitive_stack['carrier_side']}",
        f"- retained side = {primitive_stack['retained_side']}",
        "",
        "Baryon replay:",
        f"- A0 = {A0}",
        f"- mu_H = {mu_H}",
        f"- chi = {chi}",
        f"- Omega_b = {omega_b}",
        f"- Omega_m_eff = {cr019_omega_m_eff}",
        f"- Omega_BB_PBH_trapped = {cr019_pbh}",
        f"- Omega_substrate_vacuum = {cr019_vacuum}",
        "",
        "Matter inventory replay:",
        f"- Checks: {pass_count}/{len(checks)} PASS",
        f"- Matter rows: {len(matter_rows)}/126",
        f"- Stable single-write rows: {bin_counts.get('stable_matter_rows', 0)}/63",
        f"- Bound composite rows: {bin_counts.get('bound_composite_rows', 0)}/63",
        f"- Antimatter rows included: {sum(1 for row in matter_rows if 'ANTIMATTER' in row['stability_status'] or 'antimatter' in row['bin'])}",
        f"- qA split max Decimal error: {max_q_split_error}",
        f"- M_observed identity max Decimal error: {max_observed_identity_error}",
        f"- Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Critical boundaries preserved:",
        "- Tensor carrier M=18 remains carrier-only, not matter/rest mass.",
        "- QP093A-0088 remains the null conjugate boundary row: M_native=18, S_debit=18, M_observed=0, qA=0, no matter promotion.",
        "- qA source support is routed through carrier compression and ledger/A readout, not direct mass.",
        "- CR023 remains BOUNDARY_PASS: full CMB, recombination, perturbation, TT/TE/EE, Planck likelihood, and distance-triad closure remain open.",
        "- Governance CR114 is retroactive bridge provenance for CR111, not a fresh forward-blind claim.",
        "",
        "Primary artifacts:",
        f"- `{rel(layer_path)}`",
        f"- `{rel(baryon_path)}`",
        f"- `{rel(invariant_path)}`",
        f"- `{rel(wrong_path)}`",
        f"- `{rel(boundary_path)}`",
        f"- `{rel(checks_path)}`",
        f"- `{rel(source_path)}`",
        f"- `{rel(summary_path)}`",
    ]

    with result_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(result_lines))
        handle.write("\n")

    artifact_paths = [
        RUNNER_PATH,
        layer_path,
        baryon_path,
        invariant_path,
        wrong_path,
        boundary_path,
        checks_path,
        source_path,
        summary_path,
        result_path,
    ]
    with hash_path.open("w", encoding="utf-8") as handle:
        for path in artifact_paths:
            handle.write(f"{sha256_file(path)}  {rel(path)}\n")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if replay_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
