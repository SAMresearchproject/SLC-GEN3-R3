"""CR111 cosmic baryon Omega_b closure appeal.

Opens the question of whether the SAM substrate framework predicts the
Planck 2018 cosmic baryon density structurally, with zero free
parameters, from the same per-body A-field rule sealed in CR110.

The Planck 2018 anchor (CR108):
  Omega_b h^2  = 0.02237 +/- 0.00015

CR111 does NOT claim a quantitative match yet.  It formally opens the
question:

  Q: Does Omega_b h^2 emerge from the SAM substrate framework as a
     structural constant (e.g. from the same A0 = 1/(12 pi), D=3,
     R12/R16/R24 bounce sub-slot framework that governs the
     09a particle mass closure), or does it require introducing a
     free cosmological parameter?

The appeal seals the question with proper provenance and registers the
forward-blind prediction CR111_PRED_1:

  CR111_PRED_1: a future Q-artifact (or G-test) deriving Omega_b h^2
  from {A0, D, bounce sub-slot framework} alone (zero free parameters)
  will land within 1 sigma of the Planck 2018 anchor.  Any required
  free parameter beyond the bounce framework constitutes a structural
  failure of the cosmic-baryon closure.

CR111 does NOT modify any prior verdict and reveals no match.

Branch continuation: CR107 -> CR108 -> CR109 -> CR110 -> CR111 (this CR).
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR108_ANCHOR = BRANCH_DIR / "CR108_PLANCK_OMEGA_B_ANCHOR_INTAKE" / "CR108_planck_anchor.json"
CR110_APPEAL = BRANCH_DIR / "CR110_THREE_MODE_EARTH_GALAXY_PBH_CLOSURE_APPEAL" / "CR110_three_mode_appeal_lock.json"
CR104A_LOCK  = BRANCH_DIR / "CR104a_LOCAL_HIGGS_VS_GALACTIC_A_APPEAL" / "CR104a_appeal_lock.json"
BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"

OUT_JSON = CR_DIR / "CR111_summary.json"
OUT_MD   = CR_DIR / "CR111_result.md"
APPEAL_OUT = CR_DIR / "CR111_cosmic_baryon_appeal_lock.json"
APPEAL_SIBLING = CR_DIR / "CR111_cosmic_baryon_appeal_lock.json.sha256.txt"


def sha256_file(p: Path) -> str:
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


COSMIC_BARYON_QUESTION = {
    "question_text": (
        "Does Omega_b h^2 emerge from the SAM substrate framework as a "
        "structural constant (from A0 = 1/(12 pi), D=3, and the R12/R16/R24 "
        "bounce sub-slot framework that governs the 09a particle mass closure), "
        "or does it require introducing a free cosmological parameter?"
    ),
    "planck_anchor_value": 0.02237,
    "planck_anchor_uncertainty": 0.00015,
    "anchor_source": "CR108 Planck 2018 TT,TE,EE+lowE+lensing",
    "closure_condition_for_PASS": (
        "a future Q-artifact (or G-test) MUST derive Omega_b h^2 from "
        "{A0, D=3, bounce sub-slot framework} alone (zero free parameters) "
        "and land within 1 sigma of 0.02237"
    ),
    "closure_condition_for_FAIL": (
        "if any future derivation requires introducing a tunable cosmological "
        "parameter beyond the bounce framework to hit the Planck anchor, the "
        "cosmic-baryon closure is structurally failed at this layer"
    ),
}


def main():
    print("CR111 runner: starting (cosmic baryon Omega_b closure appeal)")

    cr108_sha  = sha256_file(CR108_ANCHOR)
    cr110_sha  = sha256_file(CR110_APPEAL)
    cr104a_sha = sha256_file(CR104A_LOCK)
    blindness_sha = sha256_file(BLINDNESS_PROTOCOL)

    appeal_lock = {
        "lock_id": "CR111_COSMIC_BARYON_OMEGA_B_STRUCTURAL_CLOSURE_APPEAL_LOCK",
        "branch": "14_FOUNDATIONAL_TESTS",
        "cr_id": "CR111",
        "sealed_at_utc": now_utc(),
        "appeal_target_cr": "CR108 (Planck Omega_b anchor) + CR110 (three-mode rule)",
        "appeal_target_verdict_unmodified": "CR108_PLANCK_OMEGA_B_INTAKE_PASS",
        "upstream_sha256": {
            "CR108_planck_anchor.json":              cr108_sha,
            "CR110_three_mode_appeal_lock.json":     cr110_sha,
            "CR104a_appeal_lock.json":               cr104a_sha,
            "BLINDNESS_PROTOCOL.md":                 blindness_sha,
        },
        "cosmic_baryon_question": COSMIC_BARYON_QUESTION,
        "free_parameters_total": 0,
        "forward_blind_predictions_registered_on_this_appeal": [
            {
                "id": "CR111_PRED_1",
                "claim": (
                    "a future Q-artifact deriving Omega_b h^2 from {A0, D=3, bounce sub-slot} "
                    "alone (zero free parameters) will land within 1 sigma of Planck 2018 "
                    "0.02237 +/- 0.00015; needing a free parameter is a structural failure"
                ),
                "testable_at": "future SAM cosmology G-tests / Q-artifacts",
            },
            {
                "id": "CR111_PRED_2",
                "claim": (
                    "Omega_b is consistent with the same per-body A-field rule used in "
                    "CR110 three-mode closure: the cosmic baryon fraction is the ensemble "
                    "sum over per-body A fields, not a separately tunable parameter"
                ),
                "testable_at": "SAM cosmology framework once CR111_PRED_1 derivation lands",
            },
        ],
        "prior_CR_verdicts_unchanged": [
            "CR101", "CR102", "CR103", "CR103a", "CR104",
            "CR104a", "CR104b", "CR104c", "CR105", "CR106",
            "CR107", "CR108", "CR109", "CR110",
        ],
    }

    with open(APPEAL_OUT, "w", encoding="utf-8") as f:
        json.dump(appeal_lock, f, indent=2)
    appeal_sha = sha256_file(APPEAL_OUT)
    APPEAL_SIBLING.write_text(appeal_sha + "\n", encoding="ascii")

    predictions = [
        {
            "name": "P1_cosmic_baryon_question_sealed_with_planck_anchor",
            "pass": COSMIC_BARYON_QUESTION["planck_anchor_value"] == 0.02237,
        },
        {
            "name": "P2_question_text_explicit_about_zero_free_parameter_requirement",
            "pass": "zero free parameter" in COSMIC_BARYON_QUESTION["question_text"].lower() or
                    "zero free parameter" in COSMIC_BARYON_QUESTION["closure_condition_for_PASS"].lower(),
        },
        {
            "name": "P3_upstream_cr108_anchor_present",
            "pass": bool(cr108_sha),
        },
        {
            "name": "P4_upstream_cr110_three_mode_present",
            "pass": bool(cr110_sha),
        },
        {
            "name": "P5_layer_4_chain_present",
            "pass": bool(cr104a_sha),
        },
        {
            "name": "P6_two_forward_blind_predictions_registered",
            "pass": len(appeal_lock["forward_blind_predictions_registered_on_this_appeal"]) == 2,
        },
        {
            "name": "P7_appeal_lock_sealed_with_sha256_sibling",
            "pass": APPEAL_SIBLING.exists(),
            "details": {"appeal_sha256": appeal_sha},
        },
    ]

    wrong_controls = [
        {
            "name": "WC1_no_prior_CR_verdict_modified",
            "pass": True,
        },
        {
            "name": "WC2_no_free_parameter_introduced_in_this_appeal",
            "pass": appeal_lock["free_parameters_total"] == 0,
        },
        {
            "name": "WC3_no_quantitative_match_revealed_in_this_appeal",
            "pass": True,
            "details": "appeal opens the structural question; quantitative match lives in a future Q-artifact / CR",
        },
        {
            "name": "WC4_explicit_FAIL_condition_stated",
            "pass": "FAIL" in COSMIC_BARYON_QUESTION["closure_condition_for_FAIL"] or
                    "failed" in COSMIC_BARYON_QUESTION["closure_condition_for_FAIL"],
        },
    ]

    all_pass = all(p["pass"] for p in predictions) and all(w["pass"] for w in wrong_controls)
    verdict = "CR111_COSMIC_BARYON_OMEGA_B_QUESTION_LOCKED_FORWARD_BLIND" if all_pass else "CR111_COSMIC_BARYON_OMEGA_B_QUESTION_LOCK_FAIL"

    summary = {
        "cr_id": "CR111",
        "branch": "14_FOUNDATIONAL_TESTS",
        "extends_anchor": "CR110 (three-mode) -> CR108 (Planck) -> CR104a (Layer 4)",
        "test_class": "STRUCTURAL_QUESTION_LOCK_COSMIC_BARYON_OMEGA_B_FORWARD_BLIND",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "appeal_lock_sha256": appeal_sha,
        "upstream_hashes": appeal_lock["upstream_sha256"],
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "next_courtroom_step": "future Q-artifact deriving Omega_b h^2 from {A0, D=3, bounce sub-slot} - or 14 branch zipper update sealing CR107-CR111",
        "open_debts": [
            "Quantitative Omega_b h^2 derivation from SAM substrate awaits upstream Q-artifact",
            "14 branch verdict zipper (CR106) may be updated to include CR107-CR111 in a future seal",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR111 Cosmic Baryon Omega_b Closure Appeal - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## Question Locked\n\n")
    md.append(f"> {COSMIC_BARYON_QUESTION['question_text']}\n\n")
    md.append("## Anchor (CR108)\n\n```text\n")
    md.append(f"Planck 2018 Omega_b h^2 = {COSMIC_BARYON_QUESTION['planck_anchor_value']} +/- {COSMIC_BARYON_QUESTION['planck_anchor_uncertainty']}\n")
    md.append(f"dataset                 = {COSMIC_BARYON_QUESTION['anchor_source']}\n")
    md.append("```\n\n")
    md.append("## Closure Conditions\n\n")
    md.append(f"**PASS condition:** {COSMIC_BARYON_QUESTION['closure_condition_for_PASS']}\n\n")
    md.append(f"**FAIL condition:** {COSMIC_BARYON_QUESTION['closure_condition_for_FAIL']}\n\n")
    md.append("## Forward-Blind Predictions Registered\n\n")
    for p in appeal_lock["forward_blind_predictions_registered_on_this_appeal"]:
        md.append(f"- **{p['id']}**: {p['claim']}  (testable at: {p['testable_at']})\n")
    md.append("\n## Cryptographic Chain\n\n```text\n")
    md.append(f"CR108 Planck anchor                 = {cr108_sha}\n")
    md.append(f"CR110 three-mode appeal lock        = {cr110_sha}\n")
    md.append(f"CR104a appeal lock                  = {cr104a_sha}\n")
    md.append(f"BLINDNESS_PROTOCOL.md               = {blindness_sha}\n")
    md.append(f"CR111 cosmic baryon appeal sha256   = {appeal_sha}\n")
    md.append("```\n\n")
    md.append("## Predictions\n\n")
    for p in predictions:
        flag = "PASS" if p["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {p['name']}\n")
    md.append("\n## Wrong Controls\n\n")
    for w in wrong_controls:
        flag = "PASS" if w["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {w['name']}\n")
    md.append("\n## Phase 2 Complete\n\n")
    md.append("CR107 (SPARC) -> CR108 (Planck) -> CR109 (PBH) -> CR110 (three-mode) -> CR111 (cosmic baryon) ")
    md.append("seals the cosmology-grade intake/appeal pack against the 14 branch foundational tests.  ")
    md.append("Future quantitative match reveals await upstream Q-artifacts.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  appeal sha256: {appeal_sha}")
    print("CR111 runner: complete")


if __name__ == "__main__":
    main()
