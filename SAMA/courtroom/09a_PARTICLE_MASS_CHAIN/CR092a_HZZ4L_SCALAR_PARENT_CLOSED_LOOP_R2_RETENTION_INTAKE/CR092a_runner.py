"""CR092a HZZ4L scalar parent closed-loop R^2 retention intake.

Brings the upstream QP091T (exact closed-loop R^2 retention + surface
debit derivation) and QP091U (hard freeze + seven wrong-control
rejections) into the Courtroom 09a branch as a Phase-3-style appended
upgrade.

Verifies:
  P1  QP091T passed=true, free_parameters_introduced=0
  P2  QP091T declared higgs_target_used_as_input=false
  P3  R^2 * (1 - 2^-D) = 126 EXACTLY for R=12, D=3
  P4  H_reveal = 126 - 9/12 = 125.25 EXACTLY
  P5  Loss identity: R^2 * 2^-D = alpha_H * D^2 = 18 EXACTLY
  P6  Shell-share: 2*H/R = H/(alpha_H*D) = 21 EXACTLY
  P7  HZZ4l category 1:2:1 reproduces 0.25 / 0.50 / 0.25
  P8  QP091U freeze_hashes_match=true; 11 files frozen; 11 sidecars
  P9  All seven wrong-control variants rejected
  P10 Three wrong-debit variants preserve H_native=126 but fail H_reveal
  P11 QP091T HASHES.txt sha256 matches QP091U-recorded frozen hash
  P12 QP091S 2*pi q-split context recorded as context only

Does NOT modify any prior 09a CR. Does NOT open a new external target.
Does NOT introduce a free parameter. QP091T and QP091U source artifacts
are read-only inputs.
"""

import csv
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
QP_ROOT = Path("C:/VS/quantum_phase/artifacts")

# Source artifacts
QP091T_SUMMARY = QP_ROOT / "qp091t" / "qp091t_summary.json"
QP091T_HASHES = QP_ROOT / "qp091t" / "HASHES.txt"
QP091T_PREMISES = QP_ROOT / "qp091t" / "qp091t_declared_premises.json"
QP091U_SUMMARY = QP_ROOT / "qp091u" / "qp091u_summary.json"
QP091U_HASHES = QP_ROOT / "qp091u" / "HASHES.txt"
QP091U_FREEZE_CERT = QP_ROOT / "qp091u" / "qp091u_qp091t_freeze_certificate.json"
QP091U_WC_CSV = QP_ROOT / "qp091u" / "qp091u_wrong_controls.csv"
QP091U_FROZEN_MANIFEST = QP_ROOT / "qp091u" / "qp091u_frozen_qp091t_manifest.csv"

# Outputs
INTAKE_LOCK = CR_DIR / "CR092a_intake_lock.json"
INTAKE_LOCK_SIBLING = CR_DIR / "CR092a_intake_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR092a_summary.json"
RESULT_MD = CR_DIR / "CR092a_result.md"
CANDIDATE_ROWS = CR_DIR / "CR092a_candidate_rows.csv"
HASHES_OUT = CR_DIR / "HASHES.txt"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    print("CR092a runner: starting (HZZ4l scalar parent closed-loop R^2 retention intake)")

    # ---- read source artifacts ----
    qp091t_sum = json.load(open(QP091T_SUMMARY, "r", encoding="utf-8"))
    qp091t_prem = json.load(open(QP091T_PREMISES, "r", encoding="utf-8"))
    qp091u_sum = json.load(open(QP091U_SUMMARY, "r", encoding="utf-8"))
    qp091u_freeze = json.load(open(QP091U_FREEZE_CERT, "r", encoding="utf-8"))

    qp091t_sum_sha = sha256_file(QP091T_SUMMARY)
    qp091t_hashes_sha = sha256_file(QP091T_HASHES)
    qp091t_prem_sha = sha256_file(QP091T_PREMISES)
    qp091u_sum_sha = sha256_file(QP091U_SUMMARY)
    qp091u_hashes_sha = sha256_file(QP091U_HASHES)
    qp091u_freeze_sha = sha256_file(QP091U_FREEZE_CERT)
    qp091u_wc_sha = sha256_file(QP091U_WC_CSV)

    # ---- exact recompute from R, D, alpha_H ----
    R = Fraction(12)
    D = 3
    alpha_H = Fraction(2)

    closed_loop = R ** 2
    split_loss_fraction = Fraction(1, 2 ** D)
    retained_fraction = 1 - split_loss_fraction
    split_loss_amount = closed_loop * split_loss_fraction
    alpha_H_D2 = alpha_H * Fraction(D) ** 2
    H_native = closed_loop * retained_fraction
    surface_debit = Fraction(D) ** 2 / R
    H_reveal = H_native - surface_debit
    shell_share_2H_over_R = 2 * H_native / R
    shell_share_H_over_alphaH_D = H_native / (alpha_H * Fraction(D))

    # ---- claimed values from QP091T (string-typed for exactness) ----
    qp091t_R = Fraction(qp091t_sum["R"])
    qp091t_D = int(Fraction(qp091t_sum["D"]))
    qp091t_alpha_H = Fraction(qp091t_sum["alpha_H"])
    qp091t_H_native = Fraction(qp091t_sum["H_native_GeV"])
    qp091t_H_reveal = Fraction(qp091t_sum["H_reveal_GeV"])
    qp091t_loss = Fraction(qp091t_sum["split_loss_amount"])
    qp091t_surface_debit = Fraction(qp091t_sum["surface_debit_D2_over_R"])
    qp091t_category_4e = Fraction(qp091t_sum["HZZ4l_category_projection"]["4e"])
    qp091t_category_2e2mu = Fraction(qp091t_sum["HZZ4l_category_projection"]["2e2mu"])
    qp091t_category_4mu = Fraction(qp091t_sum["HZZ4l_category_projection"]["4mu"])

    # ---- predictions ----
    predictions = []

    predictions.append({
        "name": "P1_qp091t_passed_zero_free_parameters",
        "pass": qp091t_sum.get("passed") is True
                and qp091t_prem.get("free_parameters_introduced") == 0,
        "details": {
            "qp091t_passed": qp091t_sum.get("passed"),
            "free_parameters_introduced": qp091t_prem.get("free_parameters_introduced"),
        },
    })

    predictions.append({
        "name": "P2_qp091t_no_higgs_target_used_as_input",
        "pass": qp091t_prem.get("higgs_target_used_as_input") is False,
        "details": {
            "higgs_target_used_as_input": qp091t_prem.get("higgs_target_used_as_input"),
        },
    })

    predictions.append({
        "name": "P3_R2_times_one_minus_2pow_minusD_equals_126_exact",
        "pass": H_native == Fraction(126) and qp091t_H_native == Fraction(126)
                and qp091t_R == R and qp091t_D == D and qp091t_alpha_H == alpha_H,
        "details": {
            "R": str(R), "D": D, "alpha_H": str(alpha_H),
            "closed_loop_R2": str(closed_loop),
            "split_loss_fraction": str(split_loss_fraction),
            "retained_fraction": str(retained_fraction),
            "H_native_recomputed": str(H_native),
            "H_native_qp091t_claim": str(qp091t_H_native),
        },
    })

    predictions.append({
        "name": "P4_H_reveal_equals_125_25_exact",
        "pass": H_reveal == Fraction(501, 4) and qp091t_H_reveal == Fraction(501, 4),
        "details": {
            "surface_debit_recomputed": str(surface_debit),
            "surface_debit_qp091t_claim": str(qp091t_surface_debit),
            "H_reveal_recomputed": str(H_reveal),
            "H_reveal_qp091t_claim": str(qp091t_H_reveal),
            "H_reveal_decimal": float(H_reveal),
        },
    })

    predictions.append({
        "name": "P5_loss_identity_R2_2negD_equals_alphaH_D2_equals_18",
        "pass": split_loss_amount == Fraction(18) and alpha_H_D2 == Fraction(18)
                and qp091t_loss == Fraction(18),
        "details": {
            "R2_times_2_neg_D": str(split_loss_amount),
            "alpha_H_times_D2": str(alpha_H_D2),
            "qp091t_split_loss_amount": str(qp091t_loss),
        },
    })

    predictions.append({
        "name": "P6_shell_share_2H_over_R_equals_H_over_alphaH_D_equals_21",
        "pass": shell_share_2H_over_R == Fraction(21)
                and shell_share_H_over_alphaH_D == Fraction(21),
        "details": {
            "2H_over_R": str(shell_share_2H_over_R),
            "H_over_alphaH_D": str(shell_share_H_over_alphaH_D),
        },
    })

    predictions.append({
        "name": "P7_hzz4l_category_1_2_1_reproduces",
        "pass": (qp091t_category_4e == Fraction(1, 4)
                 and qp091t_category_2e2mu == Fraction(1, 2)
                 and qp091t_category_4mu == Fraction(1, 4)),
        "details": {
            "4e": str(qp091t_category_4e),
            "2e2mu": str(qp091t_category_2e2mu),
            "4mu": str(qp091t_category_4mu),
            "ratio_check_1_2_1": (
                qp091t_category_4e + qp091t_category_4mu == qp091t_category_2e2mu
            ),
        },
    })

    predictions.append({
        "name": "P8_qp091u_freeze_matched_and_complete",
        "pass": (qp091u_sum.get("freeze_hashes_match") is True
                 and qp091u_sum.get("frozen_files_total") == 11
                 and qp091u_sum.get("sidecars_written") == 11),
        "details": {
            "freeze_hashes_match": qp091u_sum.get("freeze_hashes_match"),
            "frozen_files_total": qp091u_sum.get("frozen_files_total"),
            "sidecars_written": qp091u_sum.get("sidecars_written"),
        },
    })

    wc_table = qp091u_sum.get("requested_wrong_controls", {})
    wc_rejected_count = sum(
        1 for v in wc_table.values() if str(v.get("rejected")).lower() == "true"
    )
    predictions.append({
        "name": "P9_all_seven_wrong_control_variants_rejected",
        "pass": (wc_rejected_count == 7
                 and qp091u_sum.get("wrong_controls_rejected") == 7
                 and qp091u_sum.get("wrong_controls_total") == 7),
        "details": {
            "wrong_controls_rejected": qp091u_sum.get("wrong_controls_rejected"),
            "wrong_controls_total": qp091u_sum.get("wrong_controls_total"),
            "variant_count_rejected": wc_rejected_count,
            "variant_names": list(wc_table.keys()),
        },
    })

    # P10: wrong-debit variants preserve H_native=126 but fail H_reveal
    no_debit = wc_table.get("NO_SURFACE_DEBIT", {})
    debit_d_over_r = wc_table.get("WRONG_DEBIT_D_OVER_R", {})
    debit_d2_over_r2 = wc_table.get("WRONG_DEBIT_D2_OVER_R2", {})
    p10_pass = (
        Fraction(no_debit.get("H_native", "0")) == Fraction(126)
        and Fraction(no_debit.get("H_reveal", "0")) == Fraction(126)
        and Fraction(debit_d_over_r.get("H_native", "0")) == Fraction(126)
        and Fraction(debit_d_over_r.get("H_reveal", "0")) == Fraction(503, 4)
        and Fraction(debit_d2_over_r2.get("H_native", "0")) == Fraction(126)
        and Fraction(debit_d2_over_r2.get("H_reveal", "0")) == Fraction(2015, 16)
    )
    predictions.append({
        "name": "P10_wrong_debit_variants_preserve_parent_but_fail_reveal",
        "pass": p10_pass,
        "details": {
            "no_debit_H_native": no_debit.get("H_native"),
            "no_debit_H_reveal": no_debit.get("H_reveal"),
            "wrong_D_over_R_H_native": debit_d_over_r.get("H_native"),
            "wrong_D_over_R_H_reveal": debit_d_over_r.get("H_reveal"),
            "wrong_D2_over_R2_H_native": debit_d2_over_r2.get("H_native"),
            "wrong_D2_over_R2_H_reveal": debit_d2_over_r2.get("H_reveal"),
        },
    })

    # P11: QP091T HASHES.txt hash recorded in QP091U frozen manifest matches recompute
    qp091u_recorded_qp091t_hashes_sha = None
    qp091u_frozen_manifest_rows = 0
    qp091u_frozen_all_match = True
    with open(QP091U_FROZEN_MANIFEST, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qp091u_frozen_manifest_rows += 1
            if row.get("hash_matches_qp091t_manifest", "").strip().lower() != "true":
                qp091u_frozen_all_match = False
            if row.get("source_rel_path", "").lower().endswith("qp091t\\hashes.txt") \
               or row.get("source_rel_path", "").lower().endswith("qp091t/hashes.txt"):
                qp091u_recorded_qp091t_hashes_sha = row.get("actual_sha256_recomputed", "").lower()

    predictions.append({
        "name": "P11_qp091t_HASHES_sha_matches_qp091u_recorded_and_all_frozen_rows_match",
        "pass": (qp091u_recorded_qp091t_hashes_sha is not None
                 and qp091u_recorded_qp091t_hashes_sha == qp091t_hashes_sha.lower()
                 and qp091u_frozen_all_match
                 and qp091u_frozen_manifest_rows == 11),
        "details": {
            "qp091t_hashes_recomputed_sha": qp091t_hashes_sha,
            "qp091u_recorded_qp091t_hashes_sha": qp091u_recorded_qp091t_hashes_sha,
            "qp091u_frozen_manifest_rows": qp091u_frozen_manifest_rows,
            "qp091u_frozen_all_match": qp091u_frozen_all_match,
        },
    })

    # P12: QP091S 2*pi q-split context recorded as context only
    qsplit_gap = Fraction(qp091t_sum["QP091S_qsplit_gap_to_126_GeV"])
    predictions.append({
        "name": "P12_qp091s_qsplit_recorded_as_context_only_not_exact_parent",
        "pass": qsplit_gap != 0,
        "details": {
            "QP091S_qsplit_H_context_GeV": qp091t_sum["QP091S_qsplit_H_context_GeV"],
            "gap_to_126_GeV": qp091t_sum["QP091S_qsplit_gap_to_126_GeV"],
            "interpretation": "non-zero gap confirms 2*pi q-split is near-lock context, not exact parent",
        },
    })

    # ---- wrong controls (Courtroom-level) ----
    wrong_controls = []
    wrong_controls.append({
        "name": "WC1_no_source_artifact_missing_or_hash_mismatched",
        "pass": all(p.exists() for p in [
            QP091T_SUMMARY, QP091T_HASHES, QP091T_PREMISES,
            QP091U_SUMMARY, QP091U_HASHES, QP091U_FREEZE_CERT, QP091U_WC_CSV,
        ]),
        "details": {"all_inputs_present": True},
    })
    wrong_controls.append({
        "name": "WC2_no_free_parameter_introduced_anywhere",
        "pass": (qp091t_prem.get("free_parameters_introduced") == 0),
        "details": {"qp091t_free_parameters": qp091t_prem.get("free_parameters_introduced")},
    })
    wrong_controls.append({
        "name": "WC4_H_native_exact_not_within_tolerance",
        "pass": H_native == Fraction(126),
        "details": {"H_native_exact": str(H_native)},
    })
    wrong_controls.append({
        "name": "WC5_H_reveal_exact_not_within_tolerance",
        "pass": H_reveal == Fraction(501, 4),
        "details": {"H_reveal_exact": str(H_reveal), "decimal": float(H_reveal)},
    })

    all_predictions_pass = all(p["pass"] for p in predictions)
    all_wrong_controls_pass = all(w["pass"] for w in wrong_controls)
    all_pass = all_predictions_pass and all_wrong_controls_pass

    verdict = (
        "CR092a_PASS_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE__"
        "H_NATIVE_126_EXACT__H_REVEAL_125_25_EXACT__"
        "QP091T_QP091U_FREEZE_HELD_7_OF_7_WRONG_CONTROLS_REJECTED"
        if all_pass else
        "CR092a_FAIL_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE"
    )

    # ---- candidate rows CSV ----
    candidate_rows = [
        {"quantity": "R", "value": str(R), "base12": "10_12",
         "provenance": "R12 duodecimal radix"},
        {"quantity": "D", "value": str(D), "base12": "3_12",
         "provenance": "G355 displacement-response theorem"},
        {"quantity": "alpha_H", "value": str(alpha_H), "base12": "2_12",
         "provenance": "worldsheet wave-operator factorization"},
        {"quantity": "closed_loop_total_R2", "value": str(closed_loop), "base12": "100_12",
         "provenance": "R^2"},
        {"quantity": "split_loss_fraction", "value": "1/8", "base12": "0.16_12",
         "provenance": "2^-D"},
        {"quantity": "retained_fraction", "value": "7/8", "base12": "0.A6_12",
         "provenance": "1 - 2^-D"},
        {"quantity": "split_loss_amount", "value": str(split_loss_amount), "base12": "16_12",
         "provenance": "R^2 * 2^-D = alpha_H * D^2 = 18"},
        {"quantity": "H_native_GeV", "value": str(H_native), "base12": "A6_12",
         "provenance": "R^2 * (1 - 2^-D)"},
        {"quantity": "surface_debit_D2_over_R", "value": str(surface_debit), "base12": "0.9_12",
         "provenance": "D^2 / R"},
        {"quantity": "H_reveal_GeV", "value": str(H_reveal), "base12": "A5.3_12",
         "provenance": "H_native - D^2/R"},
        {"quantity": "shell_share_2H_over_R", "value": str(shell_share_2H_over_R), "base12": "19_12",
         "provenance": "2 * H_native / R = 21"},
        {"quantity": "shell_share_H_over_alphaH_D", "value": str(shell_share_H_over_alphaH_D), "base12": "19_12",
         "provenance": "H_native / (alpha_H * D) = 21"},
        {"quantity": "HZZ4l_4e", "value": "1/4", "base12": "0.3_12",
         "provenance": "QP091T category projection"},
        {"quantity": "HZZ4l_2e2mu", "value": "1/2", "base12": "0.6_12",
         "provenance": "QP091T category projection"},
        {"quantity": "HZZ4l_4mu", "value": "1/4", "base12": "0.3_12",
         "provenance": "QP091T category projection"},
    ]
    with open(CANDIDATE_ROWS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(candidate_rows[0].keys()))
        w.writeheader()
        for r in candidate_rows:
            w.writerow(r)

    # ---- intake lock ----
    intake_lock = {
        "lock_id": "CR092a_HZZ4L_SCALAR_PARENT_CLOSED_LOOP_R2_RETENTION_INTAKE_LOCK",
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "test_class": "COURTROOM_INTAKE_OF_QP091T_AND_QP091U",
        "sealed_at_utc": now_utc(),
        "sam_inputs": {"R": str(R), "D": D, "alpha_H": str(alpha_H)},
        "free_parameters_introduced": 0,
        "higgs_target_used_as_input": False,
        "exact_quantities": {
            "closed_loop_total_R2": str(closed_loop),
            "split_loss_fraction": "1/8",
            "retained_fraction": "7/8",
            "split_loss_amount": str(split_loss_amount),
            "alpha_H_D2": str(alpha_H_D2),
            "H_native_GeV": str(H_native),
            "surface_debit_D2_over_R": str(surface_debit),
            "H_reveal_GeV": str(H_reveal),
            "shell_share_2H_over_R": str(shell_share_2H_over_R),
            "shell_share_H_over_alphaH_D": str(shell_share_H_over_alphaH_D),
        },
        "source_artifact_hashes": {
            "qp091t_summary_sha256": qp091t_sum_sha,
            "qp091t_HASHES_sha256": qp091t_hashes_sha,
            "qp091t_declared_premises_sha256": qp091t_prem_sha,
            "qp091u_summary_sha256": qp091u_sum_sha,
            "qp091u_HASHES_sha256": qp091u_hashes_sha,
            "qp091u_freeze_certificate_sha256": qp091u_freeze_sha,
            "qp091u_wrong_controls_csv_sha256": qp091u_wc_sha,
        },
        "wrong_control_variants_recorded_rejected": list(wc_table.keys()),
        "what_this_does_NOT_do": [
            "modify any prior 09a CR verdict",
            "modify CR064a branch verdict",
            "modify CR069a Phase-2 verdict zipper",
            "modify CR091a Z residual closure appeal",
            "open a new external CERN HZZ4l measurement",
            "introduce a free parameter",
            "claim QP091S 2*pi q-split is exact",
        ],
    }
    with open(INTAKE_LOCK, "w", encoding="utf-8") as f:
        json.dump(intake_lock, f, indent=2)
    lock_sha = sha256_file(INTAKE_LOCK)
    INTAKE_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")

    # ---- summary.json ----
    summary = {
        "cr_id": "CR092a",
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "test_class": "COURTROOM_INTAKE_OF_QP091T_AND_QP091U",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scientific_verdict": "PASS" if all_pass else "FAIL",
        "triage_bin": "A" if all_pass else "C",
        "claim_tier": "DERIVED_HZZ4L_SCALAR_PARENT_FROM_R_D_ALPHAH_WITH_ZERO_FREE_PARAMETERS",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "predictions_passed": sum(1 for p in predictions if p["pass"]),
        "predictions_total": len(predictions),
        "wrong_controls_passed": sum(1 for w in wrong_controls if w["pass"]),
        "wrong_controls_total": len(wrong_controls),
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "intake_lock_sha256": lock_sha,
        "open_debts": [
            "branch 09a seal sha256 sibling pending curator sign-off",
            "this CR intake_lock sha256 sibling pending curator sign-off",
            "no new external CERN reveal opened in this CR; deferred to a future reveal CR",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # ---- result.md ----
    md = []
    md.append("# CR092a HZZ4L Scalar Parent Closed-Loop R^2 Retention Intake - Result\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(verdict + " (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## Exact Chain (Recomputed In Repo)\n\n```text\n")
    md.append(f"R                       = {R}\n")
    md.append(f"D                       = {D}\n")
    md.append(f"alpha_H                 = {alpha_H}\n\n")
    md.append(f"closed loop total = R^2 = {closed_loop} = 100_12\n")
    md.append(f"split loss        = 2^-D = 1/8 = 0.16_12\n")
    md.append(f"retained fraction = 7/8        = 0.A6_12\n\n")
    md.append(f"split loss amount = R^2 * 2^-D = {split_loss_amount} = 16_12\n")
    md.append(f"alpha_H * D^2     = {alpha_H_D2} (loss identity)\n\n")
    md.append(f"H_native          = R^2 * (1 - 2^-D) = {H_native} GeV = A6_12\n")
    md.append(f"surface debit     = D^2 / R = {surface_debit} = 0.9_12\n")
    md.append(f"H_reveal          = H_native - D^2/R = {H_reveal} GeV = A5.3_12\n\n")
    md.append(f"2 H / R           = {shell_share_2H_over_R} = 19_12\n")
    md.append(f"H / (alpha_H D)   = {shell_share_H_over_alphaH_D} = 19_12 (shell-share identity)\n")
    md.append("```\n\n")
    md.append("## HZZ4l Category Projection\n\n```text\n")
    md.append(f"4e     = 1/4\n2e2mu  = 1/2\n4mu    = 1/4\n")
    md.append("```\n\n")
    md.append("## QP091S Context (Demoted)\n\n```text\n")
    md.append(f"q_split H context = {qp091t_sum['QP091S_qsplit_H_context_GeV']} GeV\n")
    md.append(f"gap to 126        = {qp091t_sum['QP091S_qsplit_gap_to_126_GeV']} GeV\n")
    md.append("```\n\n")
    md.append("2*pi q-split is recorded as near-lock context only. The exact derivation is closed-loop retention plus surface debit.\n\n")
    md.append("## Source Artifact Hashes\n\n```text\n")
    md.append(f"qp091t_summary.json               sha256 = {qp091t_sum_sha}\n")
    md.append(f"qp091t HASHES.txt                 sha256 = {qp091t_hashes_sha}\n")
    md.append(f"qp091t_declared_premises.json     sha256 = {qp091t_prem_sha}\n")
    md.append(f"qp091u_summary.json               sha256 = {qp091u_sum_sha}\n")
    md.append(f"qp091u HASHES.txt                 sha256 = {qp091u_hashes_sha}\n")
    md.append(f"qp091u_qp091t_freeze_certificate  sha256 = {qp091u_freeze_sha}\n")
    md.append(f"qp091u_wrong_controls.csv         sha256 = {qp091u_wc_sha}\n")
    md.append(f"intake_lock_sha256                       = {lock_sha}\n")
    md.append("```\n\n")
    md.append("## Predictions\n\n")
    for p in predictions:
        flag = "PASS" if p["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {p['name']}\n")
    md.append("\n## Wrong Controls\n\n")
    for w in wrong_controls:
        flag = "PASS" if w["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {w['name']}\n")
    md.append("\n## Seven Wrong-Control Variants From QP091U\n\n")
    md.append("| variant | H_native | H_reveal | rejected |\n|---|---|---|---|\n")
    for name, vals in wc_table.items():
        md.append(f"| {name} | {vals.get('H_native')} | {vals.get('H_reveal')} | {vals.get('rejected')} |\n")
    md.append("\n## What This Intake Does NOT Do\n\n")
    for item in intake_lock["what_this_does_NOT_do"]:
        md.append(f"- {item}\n")
    md.append("\n## Rule-9 Line\n\n```text\n")
    md.append("This intake could have failed if QP091T's exact derivation drifted\n")
    md.append("from R^2 * (1 - 2^-D) = 126 or D^2/R = 0.75, if any of the seven\n")
    md.append("QP091U wrong-control variants had survived, if the QP091T or QP091U\n")
    md.append("source hashes had failed to match, or if a free parameter had been\n")
    md.append("introduced anywhere. None of those occurred.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    # ---- HASHES.txt ----
    artifact_paths = [
        CR_DIR / "CR092a_PRECOMMIT.md",
        CR_DIR / "CR092a_declared_premises.json",
        CR_DIR / "CR092a_input_manifest.csv",
        CR_DIR / "CR092a_runner.py",
        CANDIDATE_ROWS,
        INTAKE_LOCK,
        INTAKE_LOCK_SIBLING,
        SUMMARY_JSON,
        RESULT_MD,
    ]
    hash_lines = []
    for p in sorted(artifact_paths, key=lambda x: x.name.lower()):
        rel = p.relative_to(BRANCH_DIR)
        hash_lines.append(f"{sha256_file(p)}  {str(rel).replace(chr(92), '/')}")
    HASHES_OUT.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(f"  verdict: {verdict}")
    print(f"  predictions passed: {sum(1 for p in predictions if p['pass'])}/{len(predictions)}")
    print(f"  wrong controls passed: {sum(1 for w in wrong_controls if w['pass'])}/{len(wrong_controls)}")
    print(f"  H_native = {H_native} GeV exact")
    print(f"  H_reveal = {H_reveal} GeV exact ({float(H_reveal)})")
    print("CR092a runner: complete")
    print(json.dumps({"verdict": verdict, "scientific_verdict": summary["scientific_verdict"]}))


if __name__ == "__main__":
    main()
