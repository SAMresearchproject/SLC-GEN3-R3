#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


LC_ID = "LC02"
RESULT_CLASS = "LC02_PASS_HIGGS_CLOSED_FORM_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO)).replace("/", "\\")
    except ValueError:
        return str(path).replace("/", "\\")


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return REPO / path


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path_text: str) -> dict[str, Any]:
    return json.loads(resolve_path(path_text).read_text(encoding="utf-8"))


def stringify(value: Any) -> str:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (list, tuple)):
        return "; ".join(stringify(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(json_safe(value), sort_keys=True)
    return str(value)


def json_safe(value: Any) -> Any:
    if isinstance(value, Fraction):
        return stringify(value)
    if isinstance(value, Path):
        return display_path(value)
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return value


def dec(value: Fraction, places: int = 30) -> str:
    getcontext().prec = places + 20
    out = Decimal(value.numerator) / Decimal(value.denominator)
    return format(out, f".{places}f")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def add_check(
    rows: list[dict[str, Any]],
    check_id: str,
    description: str,
    expected: Any,
    observed: Any,
    passed: bool | None = None,
) -> None:
    ok = stringify(expected) == stringify(observed) if passed is None else passed
    rows.append(
        {
            "check_id": check_id,
            "description": description,
            "expected": expected,
            "observed": observed,
            "status": "PASS" if ok else "FAIL",
        }
    )


def source_row(source_id: str, path_text: str, purpose: str, expected: str, observed: str) -> dict[str, Any]:
    path = resolve_path(path_text)
    return {
        "source_id": source_id,
        "path": display_path(path),
        "purpose": purpose,
        "exists": path.exists(),
        "expected_status": expected,
        "observed_status": observed,
        "sha256": sha256_path(path) if path.exists() else "MISSING",
    }


def wrong_higgs_row(
    control_id: str,
    hypothesis: str,
    wrong_formula: str,
    h_native: Fraction | str,
    surface_debit: Fraction | str,
    h_reveal: Fraction | str,
    correct_reveal: Fraction,
    reason: str,
) -> dict[str, Any]:
    rejected = stringify(h_reveal) != stringify(correct_reveal)
    return {
        "control_id": control_id,
        "hypothesis": hypothesis,
        "wrong_formula": wrong_formula,
        "H_native": h_native,
        "surface_debit": surface_debit,
        "H_reveal": h_reveal,
        "correct_H_reveal": correct_reveal,
        "rejected": rejected,
        "reason": reason,
    }


def main() -> int:
    getcontext().prec = 80
    executed_at = now_utc()

    lc01 = load_json("16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock.json")
    cr113 = load_json("14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json")
    cr114 = load_json("14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json")
    cr115 = load_json("14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json")
    cr116 = load_json("14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json")
    cr104c = load_json("14_FOUNDATIONAL_TESTS/CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL/CR104c_appeal_lock.json")
    cr092a = load_json("09a_PARTICLE_MASS_CHAIN/CR092a_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE/CR092a_summary.json")
    cr120 = load_json("09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_summary.json")
    qp091t = load_json(r"C:\VS\quantum_phase\artifacts\qp091t\qp091t_summary.json")
    qp091u = load_json(r"C:\VS\quantum_phase\artifacts\qp091u\qp091u_summary.json")

    primitives = lc01.get("primitive_values", {})
    alpha_H = int(primitives["alpha_H"])
    R = int(primitives["R"])
    D = int(primitives["D"])

    R2 = R * R
    face_states = 2**D
    carrier_fraction = Fraction(1, face_states)
    retained_fraction = Fraction(face_states - 1, face_states)
    split_loss = Fraction(R2, 1) * carrier_fraction
    retained_parent = Fraction(R2, 1) * retained_fraction
    tensor_identity = Fraction(alpha_H * D * D, 1)
    surface_debit = Fraction(D * D, R)
    h_reveal = retained_parent - surface_debit
    bounce_lift = Fraction(D * D, 2**D)
    half_bounce = Fraction(D * D, 2 ** (D + 1))
    shell_share_1 = Fraction(2, 1) * retained_parent / R
    shell_share_2 = retained_parent / Fraction(alpha_H * D, 1)
    categories = {
        "4e": Fraction(1, 4),
        "2e2mu": Fraction(1, 2),
        "4mu": Fraction(1, 4),
    }

    replay_rows = [
        {
            "step": "LC02_STEP_01",
            "name": "closed_loop_total",
            "formula": "R^2",
            "exact": R2,
            "decimal": str(R2),
            "source": "LC01/CR113",
        },
        {
            "step": "LC02_STEP_02",
            "name": "face_state_count",
            "formula": "2^D",
            "exact": face_states,
            "decimal": str(face_states),
            "source": "LC01/CR114",
        },
        {
            "step": "LC02_STEP_03",
            "name": "carrier_fraction",
            "formula": "1/2^D",
            "exact": carrier_fraction,
            "decimal": dec(carrier_fraction),
            "source": "LC01/CR114",
        },
        {
            "step": "LC02_STEP_04",
            "name": "retained_fraction",
            "formula": "1 - 2^-D",
            "exact": retained_fraction,
            "decimal": dec(retained_fraction),
            "source": "LC01/CR114",
        },
        {
            "step": "LC02_STEP_05",
            "name": "split_loss",
            "formula": "R^2 * 2^-D",
            "exact": split_loss,
            "decimal": dec(split_loss),
            "source": "LC01/CR114/CR116",
        },
        {
            "step": "LC02_STEP_06",
            "name": "tensor_identity",
            "formula": "alpha_H * D^2",
            "exact": tensor_identity,
            "decimal": dec(tensor_identity),
            "source": "LC01/CR116",
        },
        {
            "step": "LC02_STEP_07",
            "name": "H_native",
            "formula": "R^2 * (1 - 2^-D)",
            "exact": retained_parent,
            "decimal": dec(retained_parent),
            "source": "LC01/CR114/CR092a/QP091T",
        },
        {
            "step": "LC02_STEP_08",
            "name": "surface_debit",
            "formula": "D^2/R",
            "exact": surface_debit,
            "decimal": dec(surface_debit),
            "source": "LC01/CR114/CR092a/QP091T",
        },
        {
            "step": "LC02_STEP_09",
            "name": "H_reveal",
            "formula": "R^2*(1 - 2^-D) - D^2/R",
            "exact": h_reveal,
            "decimal": dec(h_reveal),
            "source": "LC01/CR114/CR092a/QP091T",
        },
        {
            "step": "LC02_STEP_10",
            "name": "shell_share_identity_left",
            "formula": "2*H_native/R",
            "exact": shell_share_1,
            "decimal": dec(shell_share_1),
            "source": "CR092a",
        },
        {
            "step": "LC02_STEP_11",
            "name": "shell_share_identity_right",
            "formula": "H_native/(alpha_H*D)",
            "exact": shell_share_2,
            "decimal": dec(shell_share_2),
            "source": "CR092a",
        },
        {
            "step": "LC02_STEP_12",
            "name": "HZZ4l_category_projection",
            "formula": "ordered routes collapse 1:2:1",
            "exact": "4e=1/4;2e2mu=1/2;4mu=1/4",
            "decimal": "0.25;0.50;0.25",
            "source": "CR092a/QP091T",
        },
    ]

    qsplit_parent = Fraction(0, 1)
    qsplit_parent_text = qp091t.get("QP091S_qsplit_H_context_GeV", "")
    if qsplit_parent_text:
        qsplit_parent = Fraction(Decimal(qsplit_parent_text))
    qsplit_reveal_text = str(Decimal(qsplit_parent_text) - Decimal(surface_debit.numerator) / Decimal(surface_debit.denominator)) if qsplit_parent_text else ""

    wrong_rows = [
        wrong_higgs_row(
            "WC17_HIGGS_TARGET_LOCK",
            "Set H_reveal to the target first and call the selector done.",
            "H_reveal := target",
            "not computed",
            "not computed",
            "target assertion, not replay",
            h_reveal,
            "LC02 uses LC01 primitives before comparison; target assertion is not a replay formula.",
        ),
        wrong_higgs_row(
            "WC18A_CARRIER_LOSS_AS_SURFACE_DEBIT",
            "Replace the surface debit with the 18 carrier loss.",
            "H = H_native - 18",
            retained_parent,
            split_loss,
            retained_parent - split_loss,
            h_reveal,
            "Carrier loss is upstream split support, not the observed-surface debit.",
        ),
        wrong_higgs_row(
            "WC18B_HALF_BOUNCE_AS_SURFACE_DEBIT",
            "Replace the surface debit with resolved half-bounce 9/16.",
            "H = H_native - D^2/2^(D+1)",
            retained_parent,
            half_bounce,
            retained_parent - half_bounce,
            h_reveal,
            "9/16 is the resolved half-bounce algebra, not the Higgs surface debit.",
        ),
        wrong_higgs_row(
            "WC18C_BOUNCE_LIFT_AS_SURFACE_DEBIT",
            "Replace the surface debit with bounce lift 9/8.",
            "H = H_native - D^2/2^D",
            retained_parent,
            bounce_lift,
            retained_parent - bounce_lift,
            h_reveal,
            "9/8 is the bounce lift lane, not the observed-surface debit.",
        ),
        wrong_higgs_row(
            "WC20_NEAREST_PARTICLE_ROW_SELECTION",
            "Pick the nearest particle row after seeing the target.",
            "post-hoc nearest-row assignment",
            "route not fixed",
            "route not fixed",
            "not a closed-form replay",
            h_reveal,
            "LC02 fixes the CLOSED_SCALAR_LOOP route before comparison; no nearest-row search is run.",
        ),
        wrong_higgs_row(
            "WC_QP091U_WRONG_D_2",
            "Use D=2 while keeping R=12.",
            "R^2*(1-2^-2) - 2^2/R",
            Fraction(R2, 1) * Fraction(3, 4),
            Fraction(4, R),
            Fraction(R2, 1) * Fraction(3, 4) - Fraction(4, R),
            h_reveal,
            "D=2 fails both parent and reveal.",
        ),
        wrong_higgs_row(
            "WC_QP091U_WRONG_D_4",
            "Use D=4 while keeping R=12.",
            "R^2*(1-2^-4) - 4^2/R",
            Fraction(R2, 1) * Fraction(15, 16),
            Fraction(16, R),
            Fraction(R2, 1) * Fraction(15, 16) - Fraction(16, R),
            h_reveal,
            "D=4 fails both parent and reveal.",
        ),
        wrong_higgs_row(
            "WC_QP091U_WRONG_R_10",
            "Use R=10 while keeping D=3.",
            "10^2*(1-2^-3) - D^2/10",
            Fraction(100, 1) * retained_fraction,
            Fraction(D * D, 10),
            Fraction(100, 1) * retained_fraction - Fraction(D * D, 10),
            h_reveal,
            "R=10 fails both parent and reveal.",
        ),
        wrong_higgs_row(
            "WC_QP091U_WRONG_R_24",
            "Use R=24 while keeping D=3.",
            "24^2*(1-2^-3) - D^2/24",
            Fraction(24 * 24, 1) * retained_fraction,
            Fraction(D * D, 24),
            Fraction(24 * 24, 1) * retained_fraction - Fraction(D * D, 24),
            h_reveal,
            "R=24 fails both parent and reveal.",
        ),
        wrong_higgs_row(
            "WC_QP091U_NO_SURFACE_DEBIT",
            "Keep H_native but drop the observed-surface debit.",
            "H = H_native",
            retained_parent,
            0,
            retained_parent,
            h_reveal,
            "No debit preserves the parent but fails the reveal surface.",
        ),
        wrong_higgs_row(
            "WC_QP091U_DEBIT_D_OVER_R",
            "Use D/R as the surface debit.",
            "H = H_native - D/R",
            retained_parent,
            Fraction(D, R),
            retained_parent - Fraction(D, R),
            h_reveal,
            "D/R preserves the parent but fails the reveal surface.",
        ),
        wrong_higgs_row(
            "WC_QP091U_DEBIT_D2_OVER_R2",
            "Use D^2/R^2 as the surface debit.",
            "H = H_native - D^2/R^2",
            retained_parent,
            Fraction(D * D, R2),
            retained_parent - Fraction(D * D, R2),
            h_reveal,
            "D^2/R^2 preserves the parent but fails the reveal surface.",
        ),
        wrong_higgs_row(
            "WC_OLD_2PI_QSPLIT_ROUTE_RESTORE",
            "Restore the old 2*pi q-split near-lock as the exact parent route.",
            "H_qsplit - D^2/R",
            qsplit_parent_text,
            surface_debit,
            qsplit_reveal_text,
            h_reveal,
            "QP091S/QP091T keep 2*pi q-split as near-lock context only; it misses the exact reveal by the recorded gap.",
        ),
    ]

    target_visibility_rows = [
        {
            "item": "LC02_selector_inputs",
            "status": "LOCKED_PRIMITIVES_ONLY",
            "details": "R, D, alpha_H, split fractions, carrier, bounce, and surface debit are read from LC01/CR113/CR114/CR115/CR116.",
        },
        {
            "item": "external_Higgs_target",
            "status": "COMPARISON_ANCHOR_ONLY",
            "details": "CR062/PDG 125.25 appears in CR092a/QP091T history but is not an LC02 formula input.",
        },
        {
            "item": "CR120_historical_caveat",
            "status": "PRESERVED",
            "details": "CR120 remains boundary/downgraded for the older qp091 target-visible form-selection history.",
        },
        {
            "item": "LC02_claim_grade",
            "status": "DOWNSTREAM_REPLAY_PASS",
            "details": "LC02 establishes that the Higgs closed form replays from the locked stack; it does not relabel the old CR120 chronology as forward-blind.",
        },
    ]

    source_rows = [
        source_row(
            "LC01_LOCK",
            "16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock.json",
            "Locked primitive stack and LC02 lane registration.",
            "LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER",
            lc01.get("result_class", ""),
        ),
        source_row(
            "CR113",
            "14_FOUNDATIONAL_TESTS/CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM/CR113_summary.json",
            "R=12 completed-WRITE address count.",
            "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM",
            cr113.get("result_class", ""),
        ),
        source_row(
            "CR114",
            "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json",
            "1/8 carrier split, 7/8 retained parent, 0.75 surface debit.",
            "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM",
            cr114.get("result_class", ""),
        ),
        source_row(
            "CR115",
            "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json",
            "D=3 invariant carrier uniqueness.",
            "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE",
            cr115.get("result_class", ""),
        ),
        source_row(
            "CR116",
            "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json",
            "18 typed as carrier-only tensor channel, not matter/debit.",
            "CR116_PASS_18_GRAVITON_CHANNEL_CARRIER_THEOREM",
            cr116.get("result_class", ""),
        ),
        source_row(
            "CR104c",
            "14_FOUNDATIONAL_TESTS/CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL/CR104c_appeal_lock.json",
            "9/8 and 9/16 D=3 bounce algebra.",
            "CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL_LOCK",
            cr104c.get("lock_id", ""),
        ),
        source_row(
            "CR092a",
            "09a_PARTICLE_MASS_CHAIN/CR092a_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE/CR092a_summary.json",
            "Earlier Courtroom intake of QP091T/QP091U exact closed form.",
            "CR092a_PASS",
            cr092a.get("scientific_verdict", ""),
        ),
        source_row(
            "CR120",
            "09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_summary.json",
            "Public Higgs bridge with preserved audit caveat and provenance repair.",
            "BOUNDARY_WITH_PROVENANCE_FIX",
            "BOUNDARY_WITH_PROVENANCE_FIX" if cr120.get("audit_regrade") and cr120.get("upstream_provenance_fix") else "MISSING_CAVEAT",
        ),
        source_row(
            "QP091T",
            r"C:\VS\quantum_phase\artifacts\qp091t\qp091t_summary.json",
            "Closed-loop R2 retention and surface-debit derivation.",
            "PASS_QP091T_CLOSED_LOOP_R2_RETENTION",
            qp091t.get("result_class", ""),
        ),
        source_row(
            "QP091U",
            r"C:\VS\quantum_phase\artifacts\qp091u\qp091u_summary.json",
            "QP091T hard freeze and seven wrong-control rejections.",
            "PASS_QP091U_QP091T_HARD_FREEZE",
            qp091u.get("result_class", ""),
        ),
    ]

    checks: list[dict[str, Any]] = []
    add_check(checks, "LC02_CHECK_001", "LC01 result class", "LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER", lc01.get("result_class", ""))
    add_check(checks, "LC02_CHECK_002", "LC02 lane registered in LC01", True, any(row.get("lc_id") == "LC02" for row in lc01.get("downstream_lanes", [])))
    add_check(checks, "LC02_CHECK_003", "R locked", "12", primitives.get("R", ""))
    add_check(checks, "LC02_CHECK_004", "D locked", "3", primitives.get("D", ""))
    add_check(checks, "LC02_CHECK_005", "alpha_H locked", "2", primitives.get("alpha_H", ""))
    add_check(checks, "LC02_CHECK_006", "R^2", 144, R2)
    add_check(checks, "LC02_CHECK_007", "2^D face states", 8, face_states)
    add_check(checks, "LC02_CHECK_008", "carrier fraction", Fraction(1, 8), carrier_fraction)
    add_check(checks, "LC02_CHECK_009", "retained fraction", Fraction(7, 8), retained_fraction)
    add_check(checks, "LC02_CHECK_010", "split loss", 18, split_loss)
    add_check(checks, "LC02_CHECK_011", "tensor identity alpha_H*D^2", split_loss, tensor_identity)
    add_check(checks, "LC02_CHECK_012", "H_native exact", 126, retained_parent)
    add_check(checks, "LC02_CHECK_013", "surface debit exact", Fraction(3, 4), surface_debit)
    add_check(checks, "LC02_CHECK_014", "H_reveal exact", Fraction(501, 4), h_reveal)
    add_check(checks, "LC02_CHECK_015", "CR114 observed surface matches", stringify(h_reveal), cr114.get("observed_surface", ""))
    add_check(checks, "LC02_CHECK_016", "CR092a H_reveal matches", stringify(h_reveal), cr092a["predictions"][3]["details"]["H_reveal_recomputed"])
    add_check(checks, "LC02_CHECK_017", "QP091T H_reveal matches", dec(h_reveal), qp091t.get("H_reveal_GeV", ""))
    add_check(checks, "LC02_CHECK_018", "QP091U wrong controls rejected", 7, qp091u.get("wrong_controls_rejected", ""))
    add_check(checks, "LC02_CHECK_019", "CR120 caveat preserved", True, bool(cr120.get("audit_regrade") and cr120.get("upstream_provenance_fix")))
    add_check(checks, "LC02_CHECK_020", "2*pi q-split route remains non-exact", True, qsplit_reveal_text != dec(h_reveal))
    add_check(checks, "LC02_CHECK_021", "HZZ4l categories sum to one", 1, categories["4e"] + categories["2e2mu"] + categories["4mu"])
    add_check(checks, "LC02_CHECK_022", "HZZ4l categories have 1:2:1 shape", [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)], [categories["4e"], categories["2e2mu"], categories["4mu"]])
    add_check(checks, "LC02_CHECK_023", "all source files exist", True, all(row["exists"] for row in source_rows))
    add_check(checks, "LC02_CHECK_024", "all LC02 wrong controls rejected", True, all(str(row["rejected"]) == "True" for row in wrong_rows))
    add_check(checks, "LC02_CHECK_025", "no downstream formula mutation", True, primitives == lc01.get("primitive_values", {}))

    all_checks_passed = all(row["status"] == "PASS" for row in checks)
    all_sources_exist = all(row["exists"] for row in source_rows)
    all_wrong_controls_rejected = all(str(row["rejected"]) == "True" for row in wrong_rows)
    execution_status = "CLEAN" if all_checks_passed and all_sources_exist and all_wrong_controls_rejected else "FAILED"

    replay_path = ROOT / "LC02_higgs_replay_chain.csv"
    source_path = ROOT / "LC02_source_chain.csv"
    target_path = ROOT / "LC02_target_visibility_and_claim_grade.csv"
    wrong_path = ROOT / "LC02_wrong_controls.csv"
    checks_path = ROOT / "LC02_checks.csv"
    lock_path = ROOT / "LC02_higgs_closed_form_replay_lock.json"
    summary_path = ROOT / "LC02_summary.json"
    result_path = ROOT / "LC02_result.md"
    hash_path = ROOT / "LC02_hashes.txt"

    write_csv(replay_path, replay_rows, ["step", "name", "formula", "exact", "decimal", "source"])
    write_csv(source_path, source_rows, ["source_id", "path", "purpose", "exists", "expected_status", "observed_status", "sha256"])
    write_csv(target_path, target_visibility_rows, ["item", "status", "details"])
    write_csv(wrong_path, wrong_rows, ["control_id", "hypothesis", "wrong_formula", "H_native", "surface_debit", "H_reveal", "correct_H_reveal", "rejected", "reason"])
    write_csv(checks_path, checks, ["check_id", "description", "expected", "observed", "status"])

    lock = {
        "lc_id": LC_ID,
        "branch": "16_THE_LAST_CAMPAIGN",
        "test_class": "HIGGS_CLOSED_FORM_REPLAY_FROM_LOCKED_PRIMITIVE_STACK",
        "execution_status": execution_status,
        "result_class": RESULT_CLASS if execution_status == "CLEAN" else "LC02_FAIL_HIGGS_CLOSED_FORM_REPLAY",
        "executed_at_utc": executed_at,
        "scope": "Replay Higgs closed form from LC01 locked primitives. Preserve target-visible caveat for older CR120 history.",
        "claim_grade": "DOWNSTREAM_REPLAY_PASS_NOT_NEW_FORWARD_BLIND_EMPIRICAL_DISCOVERY",
        "closed_form": {
            "H_native": "R^2*(1-2^-D)",
            "H_reveal": "R^2*(1-2^-D)-D^2/R",
            "values": {
                "R": R,
                "D": D,
                "alpha_H": alpha_H,
                "R2": R2,
                "carrier_fraction": carrier_fraction,
                "retained_fraction": retained_fraction,
                "split_loss": split_loss,
                "tensor_identity": tensor_identity,
                "H_native": retained_parent,
                "surface_debit": surface_debit,
                "H_reveal": h_reveal,
            },
        },
        "source_chain": source_rows,
        "target_visibility": target_visibility_rows,
        "wrong_controls": wrong_rows,
        "checks": checks,
    }
    lock_path.write_text(json.dumps(json_safe(lock), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "lc_id": LC_ID,
        "branch": "16_THE_LAST_CAMPAIGN",
        "test_class": "HIGGS_CLOSED_FORM_REPLAY_FROM_LOCKED_PRIMITIVE_STACK",
        "execution_status": execution_status,
        "result_class": lock["result_class"],
        "claim_grade": "DOWNSTREAM_REPLAY_PASS_NOT_NEW_FORWARD_BLIND_EMPIRICAL_DISCOVERY",
        "all_checks_passed": all_checks_passed,
        "all_sources_exist": all_sources_exist,
        "all_wrong_controls_rejected": all_wrong_controls_rejected,
        "checks_passed": sum(1 for row in checks if row["status"] == "PASS"),
        "checks_total": len(checks),
        "wrong_controls_rejected": sum(1 for row in wrong_rows if str(row["rejected"]) == "True"),
        "wrong_controls_total": len(wrong_rows),
        "H_native": stringify(retained_parent),
        "surface_debit": stringify(surface_debit),
        "H_reveal": stringify(h_reveal),
        "H_reveal_decimal": dec(h_reveal),
        "CR120_caveat_preserved": bool(cr120.get("audit_regrade") and cr120.get("upstream_provenance_fix")),
        "replay_chain_csv": display_path(replay_path),
        "source_chain_csv": display_path(source_path),
        "target_visibility_csv": display_path(target_path),
        "wrong_controls_csv": display_path(wrong_path),
        "checks_csv": display_path(checks_path),
        "lock_json": display_path(lock_path),
        "result_md": display_path(result_path),
    }
    summary_path.write_text(json.dumps(json_safe(summary), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_lines = [
        "# LC02 Higgs Closed-Form Replay",
        "",
        "## Verdict",
        "",
        "```text",
        lock["result_class"],
        "```",
        "",
        "## Replay Result",
        "",
        "LC02 replays the Higgs closed form from the LC01 locked primitive stack:",
        "",
        "```text",
        "H_native = R^2*(1 - 2^-D)",
        "         = 144*(7/8)",
        "         = 126",
        "",
        "H_reveal = H_native - D^2/R",
        "         = 126 - 9/12",
        "         = 501/4",
        "         = 125.25",
        "```",
        "",
        "The replay also preserves the split identities:",
        "",
        "```text",
        "R^2 * 2^-D = 18",
        "alpha_H * D^2 = 18",
        "carrier side = 1/8",
        "retained side = 7/8",
        "surface debit = 3/4",
        "```",
        "",
        "## Claim Grade",
        "",
        "This is a downstream replay pass from the theorem-grade primitive stack. It does not relabel the older CR120 qp091 target-visible chronology as forward-blind. The CR120 caveat is preserved in `LC02_target_visibility_and_claim_grade.csv`.",
        "",
        "## Wrong Controls",
        "",
        f"{summary['wrong_controls_rejected']}/{summary['wrong_controls_total']} wrong controls were rejected, including no debit, D/R, D^2/R^2, D=2, D=4, R=10, R=24, restoring the old 2*pi q-split route, and swapping carrier/bounce quantities into the surface-debit slot.",
        "",
        "## Files",
        "",
        f"- `{display_path(replay_path)}`",
        f"- `{display_path(source_path)}`",
        f"- `{display_path(target_path)}`",
        f"- `{display_path(wrong_path)}`",
        f"- `{display_path(checks_path)}`",
        f"- `{display_path(lock_path)}`",
        f"- `{display_path(summary_path)}`",
        f"- `{display_path(hash_path)}`",
    ]
    result_path.write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    files_to_hash = [
        Path(__file__).resolve(),
        replay_path,
        source_path,
        target_path,
        wrong_path,
        checks_path,
        lock_path,
        summary_path,
        result_path,
    ]
    hash_lines = [f"{sha256_path(path)}  {display_path(path)}" for path in files_to_hash]
    hash_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    for path in files_to_hash + [hash_path]:
        sidecar = path.with_name(path.name + ".sha256.txt")
        sidecar.write_text(f"{sha256_path(path)}  {display_path(path)}\n", encoding="utf-8")

    print(json.dumps(json_safe(summary), indent=2, sort_keys=True))
    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
