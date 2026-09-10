"""
CR101_runner.py - First gate partial-closure test: GATE_2 c_SW vs c.

SAM commits c_SW = c (identity), the simplest of the three GATE_2
candidates sealed in CR100. The runner hashes the commitment BEFORE
opening the anchor envelope, then compares against four independent
CERN-class CNGS-baseline neutrino time-of-flight measurements:

  ICARUS, OPERA (corrected 2012), BOREXINO, LVD

and verifies the two-gate honest-negative discipline by rejecting:

  HN1 OPERA 2011 original (CLASS_A withdrawn) at Gate A
  HN2 synthetic Fermilab-coded (CLASS_B Tevatron) at Gate A
  HN3 Fermi-LAT GRB (CLASS_E non-CERN astrophysical) at Gate A

Per-row labels:
  AGREEMENT_WITHIN_ANCHOR_1_SIGMA
  AGREEMENT_WITHIN_ANCHOR_2_SIGMA
  AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA
  REJECTED_AT_GATE_A_ADMISSIBILITY (honest-negative rows)

Partial-closure verdict per CR101 precommit's "Possible Outcomes" list.
"""
import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"
DECLARED_PREMISES = CR_DIR / "CR101_declared_premises.json"
CR100_QUESTION_LOCK = BRANCH_DIR / "CR100_SW_PRIMITIVE_OPEN_QUESTION_ROADMAP" / "CR100_question_lock.json"

PREDICTIONS_CSV = CR_DIR / "CR101_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR101_prediction_commit.json"
ANCHOR_ENVELOPE = CR_DIR / "CR101_cern_anchor_envelope.json"
ANCHOR_SHA256_SIBLING = CR_DIR / "CR101_cern_anchor_envelope.json.sha256.txt"
EVIDENCE_CSV = CR_DIR / "CR101_evidence_rows.csv"
SUMMARY_JSON = CR_DIR / "CR101_summary.json"
RESULT_MD = CR_DIR / "CR101_result.md"

CERN_ALLOW_LIST = {
    "ATLAS", "CMS", "LHCb", "ALICE", "ICARUS", "OPERA", "BOREXINO", "LVD",
    "ALPHA", "BASE", "ASACUSA", "AEgIS",
}
WITHDRAWN_MARKERS = ("withdrawn", "superseded")


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def admissibility_check(experiment):
    """Gate A: returns (admitted: bool, rationale: str)."""
    e = experiment or ""
    if any(m in e.lower() for m in WITHDRAWN_MARKERS):
        return False, "withdrawn / superseded measurement"
    if "PDG" in e or "world average" in e.lower():
        return False, "PDG world-average is not an individual CERN measurement"
    # strip parenthetical qualifiers when matching the allow-list
    base = e.split(" (")[0].strip()
    if base not in CERN_ALLOW_LIST:
        return False, f"experiment '{base}' not on CERN allow-list"
    return True, ""


def label_by_sigma(sam_value, anchor_mean, anchor_sigma_combined):
    """Per-row label based on how many sigma SAM commitment is from anchor mean."""
    if anchor_sigma_combined <= 0:
        return "AGREEMENT_BAND_UNDEFINED"
    distance_in_sigma = abs(sam_value - anchor_mean) / anchor_sigma_combined
    if distance_in_sigma <= 1.0:
        return "AGREEMENT_WITHIN_ANCHOR_1_SIGMA"
    if distance_in_sigma <= 2.0:
        return "AGREEMENT_WITHIN_ANCHOR_2_SIGMA"
    return "AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA"


def main():
    print("CR101 runner: starting (GATE_2 c_SW vs c partial closure)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    # Step 1-2: write the SAM commitment as the prediction.
    sam_value = 0.0  # (v_substrate - c) / c = 0 because c_SW = c
    pred_rows = [{
        "row_id": "SAM_COMMITMENT",
        "gate": "GATE_2",
        "candidate_index_in_CR100": 1,
        "candidate_name": "c_SW = c (identity)",
        "predicted_value_dimensionless": sam_value,
        "expression": "(v_substrate - c) / c",
        "free_parameters_introduced": 0,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
    }]
    fns = list(pred_rows[0].keys())
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    print(f"  wrote {PREDICTIONS_CSV.name}")

    # Step 3-4: hash predictions, write commitment.
    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR101_GATE_2_PREDICTION_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_unopened_at_commit_time": True,
            "subject_gate": "GATE_2",
            "sam_committed_candidate": "c_SW = c (identity)",
            "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
            "blindness_pillar": "PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH",
        }, f, indent=2)
    print(f"  prediction committed {prediction_sha[:16]} at {prediction_utc}")

    # Step 5: verify envelope seal and open.
    computed = sha256_file(ANCHOR_ENVELOPE)
    declared = ANCHOR_SHA256_SIBLING.read_text(encoding="ascii").strip()
    if computed != declared:
        sys.exit(f"FATAL: envelope sha256 mismatch")
    envelope_sha = computed
    envelope_open_utc = now_utc()
    with open(ANCHOR_ENVELOPE, "r", encoding="utf-8") as f:
        env = json.load(f)
    print(f"  envelope opened at {envelope_open_utc}")
    if prediction_utc > envelope_open_utc:
        sys.exit("FATAL: temporal ordering violation")

    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    # Step 6-7: per-row processing
    evidence_rows = []

    # Live anchors
    for a in env["live_anchors"]:
        exp = a["experiment"]
        admitted, adm_rationale = admissibility_check(exp)
        if not admitted:
            label = "REJECTED_AT_GATE_A_ADMISSIBILITY"
            actual_gate = "GATE_A_ADMISSIBILITY"
            distance_in_sigma = None
        else:
            actual_gate = "RESIDUAL_COMPUTED"
            mean = float(a["measurement_central_value"])
            stat = float(a["stat_uncertainty"])
            sys_unc = float(a["sys_uncertainty"])
            sigma_combined = math.sqrt(stat * stat + sys_unc * sys_unc)
            label = label_by_sigma(sam_value, mean, sigma_combined)
            distance_in_sigma = abs(sam_value - mean) / sigma_combined if sigma_combined > 0 else None
        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "LIVE_ANCHOR",
            "experiment": exp,
            "publication_reference": a["publication_reference"],
            "publication_date_utc": a["publication_date_utc"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_commitment_value": sam_value,
            "sam_commitment_expression": "(v_substrate - c) / c",
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": actual_gate,
            "admissibility_rationale": adm_rationale,
            "distance_in_sigma": distance_in_sigma,
            "row_label": label,
            "honest_negative_class": None,
            "declared_rejection_gate": None,
        })

    # Honest-negative anchors
    for a in env["honest_negative_anchors"]:
        exp = a["experiment"]
        admitted, adm_rationale = admissibility_check(exp)
        declared_gate = a.get("expected_rejection_gate", "GATE_A_ADMISSIBILITY")
        if not admitted:
            label = "REJECTED_AT_GATE_A_ADMISSIBILITY"
            actual_gate = "GATE_A_ADMISSIBILITY"
            distance_in_sigma = None
        else:
            actual_gate = "PASSED_GATE_A_UNEXPECTEDLY"
            label = "HONEST_NEGATIVE_NOT_REJECTED_AT_DECLARED_GATE"
            mean = float(a["measurement_central_value"])
            stat = float(a["stat_uncertainty"])
            sys_unc = float(a["sys_uncertainty"])
            sigma_combined = math.sqrt(stat * stat + sys_unc * sys_unc)
            distance_in_sigma = abs(sam_value - mean) / sigma_combined if sigma_combined > 0 else None
        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "HONEST_NEGATIVE",
            "experiment": exp,
            "publication_reference": a["publication_reference"],
            "publication_date_utc": a["publication_date_utc"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_commitment_value": sam_value,
            "sam_commitment_expression": "(v_substrate - c) / c",
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": actual_gate,
            "admissibility_rationale": adm_rationale,
            "distance_in_sigma": distance_in_sigma,
            "row_label": label,
            "honest_negative_class": a["honest_negative_class"],
            "declared_rejection_gate": declared_gate,
        })

    fns = list(evidence_rows[0].keys())
    with open(EVIDENCE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in evidence_rows:
            w.writerow(r)
    print(f"  wrote {EVIDENCE_CSV.name} ({len(evidence_rows)} rows)")

    # Verdict assembly
    live_rows = [r for r in evidence_rows if r["row_class"] == "LIVE_ANCHOR"]
    hn_rows = [r for r in evidence_rows if r["row_class"] == "HONEST_NEGATIVE"]

    all_within_1sigma = all(r["row_label"] == "AGREEMENT_WITHIN_ANCHOR_1_SIGMA" for r in live_rows)
    any_outside_2sigma = any(r["row_label"] == "AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA" for r in live_rows)
    any_at_2sigma_only = any(r["row_label"] == "AGREEMENT_WITHIN_ANCHOR_2_SIGMA" for r in live_rows)
    all_hn_rejected_at_gate_a = all(r["actual_gate"] == "GATE_A_ADMISSIBILITY" for r in hn_rows)

    if any_outside_2sigma:
        partial_closure_verdict = "GATE_2_IDENTITY_DISFAVORED_BY_CERN_DATA"
    elif any_at_2sigma_only:
        partial_closure_verdict = "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_2_SIGMA_ONLY"
    elif all_within_1sigma:
        partial_closure_verdict = "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_WITH_CERN_BOUNDS"
    else:
        partial_closure_verdict = "PARTIAL_CLOSURE_INCONCLUSIVE"

    label_counts = {}
    for r in evidence_rows:
        label_counts[r["row_label"]] = label_counts.get(r["row_label"], 0) + 1

    summary = {
        "cr_id": "CR101",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "FIRST_GATE_PARTIAL_CLOSURE_TEST_AGAINST_CERN_CLASS_DATA",
        "execution_status": "CLEAN",
        "result_class": partial_closure_verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "subject_gate": "GATE_2",
        "sam_committed_candidate": "c_SW = c (identity)",
        "live_anchor_count": len(live_rows),
        "honest_negative_count": len(hn_rows),
        "all_hn_rejected_at_gate_a": all_hn_rejected_at_gate_a,
        "row_label_counts": label_counts,
        "tightest_live_anchor": min(
            (r for r in live_rows),
            key=lambda r: math.sqrt(r["stat_uncertainty"] ** 2 + r["sys_uncertainty"] ** 2),
            default=None,
        )["experiment"] if live_rows else None,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_sha256": envelope_sha,
        "anchor_envelope_open_utc": envelope_open_utc,
        "blindness_protocol_sha256": blindness_sha,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        "what_this_does_not_claim": premises["what_CR101_does_and_does_not_claim"]["does_not_claim"],
        "open_debts": premises["open_debts_declared_at_CR101"],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote {SUMMARY_JSON.name}")

    # result.md
    md = []
    md.append("# CR101 GATE_2 c_SW vs c Partial Closure - Result\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(f"CR101_{partial_closure_verdict} (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## SAM Commitment (Locked Before Anchor Open)\n\n```text\n")
    md.append("GATE_2 candidate selected (from CR100 sealed enumeration):\n")
    md.append("  c_SW = c (identity)\n\n")
    md.append("Expressed as testable prediction: (v_substrate - c) / c = 0\n")
    md.append("Free parameters introduced: 0\n")
    md.append(f"Upstream CR100 question lock sha256: {premises['upstream_question_lock_sha256']}\n")
    md.append("```\n\n")
    md.append("## Blindness Proof\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"anchor_envelope_sha256   = {envelope_sha}\n")
    md.append(f"anchor_envelope_open_utc = {envelope_open_utc}\n")
    md.append("temporal_ordering        = OK\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## Live CERN-Class Anchors (Pillar 3 Cross-Source)\n\n")
    md.append("| Row | Experiment | (v-c)/c +/- combined sigma | Distance to 0 (in sigma) | Label |\n")
    md.append("|---|---|---|---|---|\n")
    for r in live_rows:
        mean = r["measurement_central_value"]
        stat = r["stat_uncertainty"]
        sigma_combined = math.sqrt(stat * stat + r["sys_uncertainty"] ** 2)
        d = r["distance_in_sigma"]
        d_str = f"{d:.2f} sigma" if d is not None else "n/a"
        md.append(
            f"| {r['row_id']} | {r['experiment']} | "
            f"{mean:+.2e} +/- {sigma_combined:.2e} | {d_str} | {r['row_label']} |\n"
        )
    md.append("\n## Honest-Negative Rejection Proof (Pillar 4)\n\n")
    md.append("| Row | Class | Experiment | Declared gate | Actual gate | Label |\n")
    md.append("|---|---|---|---|---|---|\n")
    for r in hn_rows:
        md.append(
            f"| {r['row_id']} | {r['honest_negative_class']} | {r['experiment']} | "
            f"{r['declared_rejection_gate']} | {r['actual_gate']} | {r['row_label']} |\n"
        )
    md.append("\n## What This Test Means\n\n")
    md.append("```text\n")
    if partial_closure_verdict == "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_WITH_CERN_BOUNDS":
        md.append("All four independent CERN-class CNGS-baseline neutrino time-of-flight\n")
        md.append("measurements (ICARUS, OPERA-corrected, BOREXINO, LVD) place SAM's\n")
        md.append("c_SW = c commitment WITHIN their 1-sigma bands. The CERN-class\n")
        md.append("precision floor on substrate propagation speed = c is locked at\n")
        md.append("O(1e-6) by this test.\n\n")
        md.append("GATE_2 candidate #1 is partially closed at CERN precision. The other\n")
        md.append("two candidates (c_SW = c * factor, c_SW via converter triad) remain\n")
        md.append("in the CR100 sealed enumeration and are not excluded by this test;\n")
        md.append("they would only differ from identity at precision finer than CERN\n")
        md.append("provides.\n")
    elif partial_closure_verdict == "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_2_SIGMA_ONLY":
        md.append("SAM's c_SW = c commitment is consistent with CERN-class bounds at\n")
        md.append("2-sigma only for one or more live anchors. The closure is weaker\n")
        md.append("than 1-sigma identity. Recorded honestly without changing SAM's\n")
        md.append("commitment.\n")
    elif partial_closure_verdict == "GATE_2_IDENTITY_DISFAVORED_BY_CERN_DATA":
        md.append("One or more live anchors falls outside SAM's c_SW = c commitment\n")
        md.append("at the 2-sigma level. GATE_2 candidate #1 is disfavored at CERN\n")
        md.append("precision. The other two candidates remain available; CR100's\n")
        md.append("sealed open-gate enumeration is not modified.\n")
    md.append("\n")
    md.append("Stronger bounds exist OUTSIDE the 13 branch scope:\n")
    md.append("  Fermi-LAT GRB 090510 (Vasileiou et al. 2013):     1e-15 precision\n")
    md.append("  IceCube neutrino LIV constraints:                  1e-18 precision\n")
    md.append("These are not CERN; they were excluded from live anchors at Gate A.\n")
    md.append("A future 14_FOUNDATIONAL_TESTS branch could admit them as live anchors.\n")
    md.append("```\n\n")
    md.append("## How Progress On GATE_2 Is Tracked\n\n")
    md.append("```text\n")
    md.append("CR101a appeal rows record:\n")
    md.append("  - new CERN-class measurements at tighter precision\n")
    md.append("  - non-CERN measurements admitted in a future 14_ branch\n")
    md.append("  - any future result that disfavors c_SW = c\n\n")
    md.append("Original CR101 verdict is NEVER modified.\n")
    md.append("Original CR100 GATE_2 enumeration is NEVER modified.\n")
    md.append("```\n\n")
    md.append("## What CR101 Does Not Claim\n\n")
    for n in summary["what_this_does_not_claim"]:
        md.append(f"- {n}\n")
    md.append("\n## Rule-9 Line\n\n```text\n")
    md.append("This CR could have falsified SAM's GATE_2 candidate #1 if any of\n")
    md.append("the four live CERN-class neutrino time-of-flight measurements had\n")
    md.append("reported (v_v - c)/c at >= 3-sigma after the corrected 2012 analyses.\n")
    md.append("\n")
    md.append("This is the first foundation stone. If c_SW = c holds at CERN\n")
    md.append("precision, the partition algebra inherits c as the propagation\n")
    md.append("constant, the standing-echo reading of particles inherits c, and\n")
    md.append("the action-phase identity in 11_QM_AND_GRAVITY inherits c.\n")
    md.append("If we build from the ground up, this is the ground.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR101 runner: complete")


if __name__ == "__main__":
    main()
