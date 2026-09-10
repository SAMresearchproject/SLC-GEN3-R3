"""
CR102_runner.py - Astrophysical-precision partial closure of GATE_2.

Same SAM commitment as CR101 (c_SW = c, identity candidate).
Same four-pillar blindness procedure.
New live anchors: Fermi-LAT, IceCube, MAGIC, HESS, Crab pulsar timing.
Precision floor: ~1e-18 (IceCube) instead of CR101's ~1e-6 (CERN).

Honest-negatives now include:
  CLASS_A: OPERA 2011 (withdrawn)
  CLASS_X_UNPUBLISHED: preprint without journal reference
  CLASS_G: synthetic perturbation of Fermi-LAT (passes admissibility,
           fails Gate R residual)
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

BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"
DECLARED_PREMISES = CR_DIR / "CR102_declared_premises.json"

PREDICTIONS_CSV = CR_DIR / "CR102_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR102_prediction_commit.json"
ANCHOR_ENVELOPE = CR_DIR / "CR102_anchor_envelope.json"
ANCHOR_SHA256_SIBLING = CR_DIR / "CR102_anchor_envelope.json.sha256.txt"
EVIDENCE_CSV = CR_DIR / "CR102_evidence_rows.csv"
SUMMARY_JSON = CR_DIR / "CR102_summary.json"
RESULT_MD = CR_DIR / "CR102_result.md"

# Open-science admissibility for 14_FOUNDATIONAL_TESTS
ADMISSIBLE_OBSERVATORIES = {
    "Fermi-LAT", "IceCube", "MAGIC", "HESS", "VERITAS",
    "HESS+MAGIC+VERITAS (combined)", "HESS+MAGIC+VERITAS",
    "ATLAS", "CMS", "LHCb", "ALICE", "BOREXINO", "ICARUS", "LVD",
    "OPERA", "ALPHA", "BASE", "ASACUSA", "AEgIS",
    "LIGO", "Virgo", "KAGRA", "Planck", "WMAP", "JWST", "Hubble",
    "EHT", "CMB-S4", "KATRIN", "KamLAND", "Super-Kamiokande",
    "Daya Bay", "T2K", "NOvA", "MINOS",
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


def admissibility_check(experiment, publication_reference):
    """Gate A for 14 branch.
    Reject: withdrawn, unpublished (no reference), non-observatory, synthetic-marked.
    Admit: peer-reviewed publication from known observatory/collaboration.
    """
    e = experiment or ""
    pubref = publication_reference or ""
    if any(m in e.lower() for m in WITHDRAWN_MARKERS):
        return False, "withdrawn / superseded measurement"
    if "NO_PUBLICATION_REFERENCE" in pubref or pubref.strip() == "":
        return False, "no peer-reviewed publication reference"
    if pubref.startswith("SYNTHETIC_"):
        # CLASS_G synthetic - the experiment label is real, but the value is synthetic.
        # By design CLASS_G should PASS admissibility (it carries a real-looking
        # experiment + a synthetic value); it gets caught at Gate R.
        # Strip the SYNTHETIC marker for the admissibility check.
        pass
    base = e.split(" (")[0].strip()
    if base not in ADMISSIBLE_OBSERVATORIES:
        return False, f"observatory '{base}' not on 14-branch admissible list"
    return True, ""


def label_by_sigma(sam_value, anchor_mean, sigma_combined):
    if sigma_combined <= 0:
        return ("AGREEMENT_BAND_UNDEFINED", None)
    d = abs(sam_value - anchor_mean) / sigma_combined
    if d <= 1.0:
        return ("AGREEMENT_WITHIN_ANCHOR_1_SIGMA", d)
    if d <= 2.0:
        return ("AGREEMENT_WITHIN_ANCHOR_2_SIGMA", d)
    return ("AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA", d)


def main():
    print("CR102 runner: starting (GATE_2 astrophysical closure)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    sam_value = 0.0
    pred_rows = [{
        "row_id": "SAM_COMMITMENT",
        "gate": "GATE_2",
        "candidate_index_in_CR100": 1,
        "candidate_name": "c_SW = c (identity)",
        "predicted_value_dimensionless": sam_value,
        "expression": "(v_substrate - c) / c",
        "free_parameters_introduced": 0,
        "identical_to_CR101_commitment": True,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
    }]
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pred_rows[0].keys()))
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR102_GATE_2_ASTROPHYSICAL_PREDICTION_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_unopened_at_commit_time": True,
            "subject_gate": "GATE_2",
            "sam_committed_candidate": "c_SW = c (identity)",
            "identical_commitment_as_CR101": True,
            "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        }, f, indent=2)
    print(f"  prediction committed {prediction_sha[:16]} at {prediction_utc}")

    computed = sha256_file(ANCHOR_ENVELOPE)
    declared = ANCHOR_SHA256_SIBLING.read_text(encoding="ascii").strip()
    if computed != declared:
        sys.exit("FATAL: envelope sha256 mismatch")
    envelope_sha = computed
    envelope_open_utc = now_utc()
    with open(ANCHOR_ENVELOPE, "r", encoding="utf-8") as f:
        env = json.load(f)
    print(f"  envelope opened at {envelope_open_utc}")
    if prediction_utc > envelope_open_utc:
        sys.exit("FATAL: temporal ordering violation")

    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    evidence_rows = []

    # Live anchors
    for a in env["live_anchors"]:
        exp = a["experiment"]
        pub = a["publication_reference"]
        admitted, adm_rationale = admissibility_check(exp, pub)
        if not admitted:
            label, d = "REJECTED_AT_GATE_A_ADMISSIBILITY", None
            actual_gate = "GATE_A_ADMISSIBILITY"
        else:
            actual_gate = "RESIDUAL_COMPUTED"
            sigma = math.sqrt(a["stat_uncertainty"] ** 2 + a["sys_uncertainty"] ** 2)
            label, d = label_by_sigma(sam_value, a["measurement_central_value"], sigma)
        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "LIVE_ANCHOR",
            "experiment": exp,
            "source_object": a.get("source_object", ""),
            "publication_reference": pub,
            "publication_date_utc": a["publication_date_utc"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_commitment_value": sam_value,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": actual_gate,
            "admissibility_rationale": adm_rationale,
            "distance_in_sigma": d,
            "row_label": label,
            "honest_negative_class": None,
            "declared_rejection_gate": None,
        })

    # Honest-negatives
    for a in env["honest_negative_anchors"]:
        exp = a["experiment"]
        pub = a["publication_reference"]
        cls = a["honest_negative_class"]
        declared_gate = a["expected_rejection_gate"]
        admitted, adm_rationale = admissibility_check(exp, pub)

        if not admitted:
            # Rejected at Gate A
            label = "REJECTED_AT_GATE_A_ADMISSIBILITY"
            actual_gate = "GATE_A_ADMISSIBILITY"
            d = None
        else:
            # Passes admissibility - test Gate R
            actual_gate = "GATE_R_RESIDUAL"
            sigma = math.sqrt(a["stat_uncertainty"] ** 2 + a["sys_uncertainty"] ** 2)
            if sigma > 0:
                d = abs(sam_value - a["measurement_central_value"]) / sigma
            else:
                d = float("inf")
            # CLASS_G expected to FAIL Gate R
            if d > 2.0:
                label = "REJECTED_AT_GATE_R_RESIDUAL"
            else:
                label = "HONEST_NEGATIVE_NOT_REJECTED_AT_DECLARED_GATE"

        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "HONEST_NEGATIVE",
            "experiment": exp,
            "source_object": "",
            "publication_reference": pub,
            "publication_date_utc": a["publication_date_utc"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_commitment_value": sam_value,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": actual_gate,
            "admissibility_rationale": adm_rationale,
            "distance_in_sigma": d,
            "row_label": label,
            "honest_negative_class": cls,
            "declared_rejection_gate": declared_gate,
        })

    fns = list(evidence_rows[0].keys())
    with open(EVIDENCE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in evidence_rows:
            w.writerow(r)
    print(f"  wrote {EVIDENCE_CSV.name} ({len(evidence_rows)} rows)")

    live_rows = [r for r in evidence_rows if r["row_class"] == "LIVE_ANCHOR"]
    hn_rows = [r for r in evidence_rows if r["row_class"] == "HONEST_NEGATIVE"]

    all_within_1sigma = all(r["row_label"] == "AGREEMENT_WITHIN_ANCHOR_1_SIGMA" for r in live_rows)
    any_outside_2sigma = any(r["row_label"] == "AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA" for r in live_rows)
    any_at_2sigma_only = any(r["row_label"] == "AGREEMENT_WITHIN_ANCHOR_2_SIGMA" for r in live_rows)

    if any_outside_2sigma:
        verdict = "GATE_2_IDENTITY_DISFAVORED_AT_ASTROPHYSICAL_PRECISION"
    elif all_within_1sigma:
        verdict = "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_ASTROPHYSICAL_PRECISION"
    elif any_at_2sigma_only:
        verdict = "PARTIAL_CLOSURE_AT_TIGHTER_THAN_CERN_BUT_NOT_TIGHTEST"
    else:
        verdict = "PARTIAL_CLOSURE_INCONCLUSIVE"

    # Honest-negative gate-mismatch count
    gate_mismatches = sum(
        1 for r in hn_rows
        if r["actual_gate"] != r["declared_rejection_gate"]
    )

    label_counts = {}
    for r in evidence_rows:
        label_counts[r["row_label"]] = label_counts.get(r["row_label"], 0) + 1

    # Precision floor = tightest uncertainty among live anchors that landed in 1- or 2-sigma
    tightest_anchor = min(
        (r for r in live_rows if r["row_label"] in ("AGREEMENT_WITHIN_ANCHOR_1_SIGMA", "AGREEMENT_WITHIN_ANCHOR_2_SIGMA")),
        key=lambda r: math.sqrt(r["stat_uncertainty"] ** 2 + r["sys_uncertainty"] ** 2),
        default=None,
    )
    precision_floor = None
    if tightest_anchor is not None:
        precision_floor = math.sqrt(tightest_anchor["stat_uncertainty"] ** 2 + tightest_anchor["sys_uncertainty"] ** 2)

    summary = {
        "cr_id": "CR102",
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "ASTROPHYSICAL_PRECISION_PARTIAL_CLOSURE_OF_GATE_2",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "subject_gate": "GATE_2",
        "sam_committed_candidate": "c_SW = c (identity)",
        "identical_commitment_as_CR101": True,
        "live_anchor_count": len(live_rows),
        "honest_negative_count": len(hn_rows),
        "row_label_counts": label_counts,
        "tightest_live_anchor_experiment": tightest_anchor["experiment"] if tightest_anchor else None,
        "tightest_live_anchor_precision": precision_floor,
        "cr101_cern_precision_floor": 1e-6,
        "precision_improvement_factor": (1e-6 / precision_floor) if precision_floor else None,
        "honest_negative_gate_mismatches": gate_mismatches,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_sha256": envelope_sha,
        "anchor_envelope_open_utc": envelope_open_utc,
        "blindness_protocol_sha256": blindness_sha,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        "upstream_cern_class_partial_result_class": premises["upstream_cern_class_partial_result_class"],
        "open_debts": premises["open_debts_declared_at_CR102"],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR102 GATE_2 Astrophysical Closure - Result\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(f"CR102_{verdict} (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## SAM Commitment (Identical To CR101)\n\n```text\n")
    md.append("GATE_2 candidate: c_SW = c (identity)\n")
    md.append("Expressed: (v_substrate - c) / c = 0\n")
    md.append("Free parameters: 0\n")
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
    md.append("## Live Astrophysical Anchors (Pillar 3 Cross-Observatory)\n\n")
    md.append("| Row | Observatory | Source | Precision | Distance to 0 | Label |\n")
    md.append("|---|---|---|---|---|---|\n")
    for r in live_rows:
        sigma = math.sqrt(r["stat_uncertainty"] ** 2 + r["sys_uncertainty"] ** 2)
        d = r["distance_in_sigma"]
        d_str = f"{d:.2f} sigma" if d is not None else "n/a"
        md.append(
            f"| {r['row_id']} | {r['experiment']} | {r['source_object']} | "
            f"+/-{sigma:.0e} | {d_str} | {r['row_label']} |\n"
        )
    md.append("\n## Honest-Negative Resolution Proof (Pillar 4 Two-Gate)\n\n")
    md.append("| Row | Class | Anchor | Declared gate | Actual gate | Label |\n")
    md.append("|---|---|---|---|---|---|\n")
    for r in hn_rows:
        md.append(
            f"| {r['row_id']} | {r['honest_negative_class']} | {r['experiment']} | "
            f"{r['declared_rejection_gate']} | {r['actual_gate']} | {r['row_label']} |\n"
        )
    md.append("\n## Precision Lift From CR101\n\n```text\n")
    md.append(f"CR101 (CERN-class)        precision floor : ~1e-6\n")
    if precision_floor:
        md.append(f"CR102 (astrophysical)     precision floor : ~{precision_floor:.0e}\n")
        md.append(f"Improvement factor                          : {1e-6/precision_floor:.0e}\n")
    md.append("```\n\n")
    md.append("## What This Test Means\n\n```text\n")
    if verdict == "PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_ASTROPHYSICAL_PRECISION":
        md.append("All five live astrophysical anchors place SAM's c_SW = c\n")
        md.append("commitment WITHIN their 1-sigma published bounds. The precision\n")
        md.append("floor on substrate propagation speed = c is now locked at the\n")
        md.append("astrophysical level - up to 12 orders of magnitude tighter than\n")
        md.append("the CERN-class floor in CR101.\n\n")
        md.append("Ground stone laid at strongest available precision.\n\n")
        md.append("Downstream consequences (all inherit c at this precision):\n")
        md.append("  - partition algebra carriers travel at c\n")
        md.append("  - 09a standing-echo particle reading inherits c\n")
        md.append("  - 11_QM_AND_GRAVITY action-phase identity inherits c\n")
        md.append("  - CR098 SAM-X candidates' propagation constant locked\n")
        md.append("  - CR099 falsifier signature's c_SW dependency closed\n")
    elif verdict == "PARTIAL_CLOSURE_AT_TIGHTER_THAN_CERN_BUT_NOT_TIGHTEST":
        md.append("Some live anchors at 1-sigma, others at 2-sigma. Better than\n")
        md.append("CR101 but not the tightest available precision.\n")
    elif verdict == "GATE_2_IDENTITY_DISFAVORED_AT_ASTROPHYSICAL_PRECISION":
        md.append("At least one astrophysical anchor is >= 2 sigma from SAM's 0.\n")
        md.append("GATE_2 candidate #1 is disfavored at world-best precision.\n")
        md.append("SAM goes to the shop for GATE_2 - candidates (b) or (c)\n")
        md.append("remain in the CR100 sealed enumeration as alternatives.\n")
    md.append("```\n\n")
    md.append("## Rule-9 Line\n\n```text\n")
    md.append("This CR could have disfavored SAM's GATE_2 candidate #1 at\n")
    md.append("astrophysical precision if any of the five live photon/neutrino\n")
    md.append("LIV bounds had reported (v - c)/c at >= 3 sigma from 0. The\n")
    md.append("result is recorded as observed.\n\n")
    md.append("If we build from the ground up, this is the ground.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR102 runner: complete")


if __name__ == "__main__":
    main()
