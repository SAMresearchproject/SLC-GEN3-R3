"""
CR103_runner.py - GATE_1 N_SW multiplicity-scaling test.

SAM commitment: GATE_1 candidate #4 (paired source/recoil count) under
its simplest reading predicts N_ch(s) proportional to sqrt(s), i.e.,
alpha_SAM = 1.0 where N_ch proportional to s^(alpha/2).

Procedure (four-pillar blindness):
  step 1 lock SAM exponent alpha_SAM = 1.0
  step 2 write predictions; hash; commit BEFORE envelope opens
  step 3 open envelope; verify sha256
  step 4 normalize against lowest-sqrt(s) live anchor (ATLAS 0.9 TeV)
  step 5 predict N_ch at each higher anchor using N_pred(s) = N_anchor * sqrt(s/s_0)
  step 6 compute per-anchor residual percent and combined-sigma distance
  step 7 from cross-source pairs, compute alpha_obs and compare to 1.0
  step 8 verdict per outcome enumeration in PRECOMMIT
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
DECLARED_PREMISES = CR_DIR / "CR103_declared_premises.json"

PREDICTIONS_CSV = CR_DIR / "CR103_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR103_prediction_commit.json"
ANCHOR_ENVELOPE = CR_DIR / "CR103_anchor_envelope.json"
ANCHOR_SHA256_SIBLING = CR_DIR / "CR103_anchor_envelope.json.sha256.txt"
EVIDENCE_CSV = CR_DIR / "CR103_evidence_rows.csv"
SUMMARY_JSON = CR_DIR / "CR103_summary.json"
RESULT_MD = CR_DIR / "CR103_result.md"

ADMISSIBLE_OBSERVATORIES = {"ATLAS", "CMS", "LHCb", "ALICE"}
WITHDRAWN_MARKERS = ("withdrawn", "superseded")

ALPHA_SAM = 1.0  # SAM's simplest-reading exponent


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def admissibility_check(experiment, publication_reference):
    e = experiment or ""
    pubref = publication_reference or ""
    if any(m in e.lower() for m in WITHDRAWN_MARKERS):
        return False, "withdrawn / superseded"
    if "WITHDRAWN" in pubref:
        return False, "withdrawn / superseded"
    if "NO_PUBLICATION_REFERENCE" in pubref or pubref.strip() == "":
        return False, "no peer-reviewed publication reference"
    if pubref.startswith("SYNTHETIC_"):
        pass  # Class_G passes admissibility intentionally
    base = e.split(" (")[0].strip()
    if base not in ADMISSIBLE_OBSERVATORIES:
        return False, f"observatory '{base}' not on 14-branch admissible list"
    return True, ""


def predicted_n_ch(sqrt_s, sqrt_s_0, n_ch_0):
    """SAM linear-in-energy prediction: N_pred(s) = N_0 * sqrt(s/s_0)"""
    return n_ch_0 * math.sqrt(sqrt_s / sqrt_s_0)


def observed_alpha(s_high, s_low, n_high, n_low):
    """Pairwise observed scaling exponent: N proportional to s^(alpha/2)"""
    if n_low <= 0 or s_low <= 0 or s_high <= 0:
        return None
    return 2.0 * math.log(n_high / n_low) / math.log(s_high / s_low)


def main():
    print("CR103 runner: starting (GATE_1 N_SW multiplicity-scaling test)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    # Step 1-2: lock SAM commitment.
    pred_rows = [{
        "row_id": "SAM_COMMITMENT",
        "gate": "GATE_1",
        "candidate_index_in_CR100": 4,
        "candidate_name": "paired source/recoil count",
        "reading": "simplest (linear in collision available energy)",
        "predicted_scaling_law": "N_ch(s) = K * s^(alpha_SAM/2)",
        "alpha_SAM": ALPHA_SAM,
        "free_parameters_in_exponent": 0,
        "free_parameters_in_normalization": 1,
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
            "commit_id": "CR103_GATE_1_PREDICTION_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_unopened_at_commit_time": True,
            "subject_gate": "GATE_1",
            "sam_committed_candidate": "candidate #4 simplest reading",
            "alpha_SAM": ALPHA_SAM,
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

    # Step 4: normalization anchor = ATLAS at 0.9 TeV (A1)
    norm_anchor = next(a for a in env["live_anchors"] if a["row_id"] == "A1")
    sqrt_s_0 = norm_anchor["sqrt_s_TeV"]
    n_ch_0 = norm_anchor["measurement_central_value"]
    s_0 = sqrt_s_0 ** 2
    print(f"  normalization anchor: ATLAS at sqrt(s)={sqrt_s_0} TeV, <dN_ch/d_eta>={n_ch_0}")

    evidence_rows = []

    # Live anchors
    for a in env["live_anchors"]:
        exp = a["experiment"]
        pub = a["publication_reference"]
        admitted, adm_rationale = admissibility_check(exp, pub)
        if not admitted:
            evidence_rows.append({
                "row_id": a["row_id"],
                "row_class": "LIVE_ANCHOR",
                "experiment": exp,
                "sqrt_s_TeV": a["sqrt_s_TeV"],
                "measurement_central_value": a["measurement_central_value"],
                "stat_uncertainty": a["stat_uncertainty"],
                "sys_uncertainty": a["sys_uncertainty"],
                "units": a["units"],
                "sam_predicted_n_ch": None,
                "residual_value": None,
                "residual_percent": None,
                "distance_in_sigma": None,
                "prediction_commit_sha256": prediction_sha,
                "prediction_commit_utc": prediction_utc,
                "anchor_envelope_sha256": envelope_sha,
                "anchor_envelope_open_utc": envelope_open_utc,
                "blindness_protocol_sha256": blindness_sha,
                "actual_gate": "GATE_A_ADMISSIBILITY",
                "admissibility_rationale": adm_rationale,
                "row_label": "REJECTED_AT_GATE_A_ADMISSIBILITY",
                "honest_negative_class": None,
                "declared_rejection_gate": None,
                "publication_reference": pub,
            })
            continue

        n_pred = predicted_n_ch(a["sqrt_s_TeV"], sqrt_s_0, n_ch_0)
        n_meas = a["measurement_central_value"]
        sigma_combined = math.sqrt(a["stat_uncertainty"] ** 2 + a["sys_uncertainty"] ** 2)
        residual = n_pred - n_meas
        residual_pct = (residual / n_meas) * 100.0 if n_meas != 0 else None
        distance_sigma = abs(residual) / sigma_combined if sigma_combined > 0 else None

        if a["row_id"] == "A1":
            # Normalization anchor - by construction n_pred = n_meas
            row_label = "NORMALIZATION_ANCHOR_BY_CONSTRUCTION"
        elif distance_sigma is None:
            row_label = "BAND_UNDEFINED"
        elif distance_sigma <= 1.0:
            row_label = "AGREEMENT_WITHIN_ANCHOR_1_SIGMA"
        elif distance_sigma <= 2.0:
            row_label = "AGREEMENT_WITHIN_ANCHOR_2_SIGMA"
        elif distance_sigma <= 3.0:
            row_label = "AGREEMENT_WITHIN_ANCHOR_3_SIGMA"
        else:
            row_label = "AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA"

        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "LIVE_ANCHOR",
            "experiment": exp,
            "sqrt_s_TeV": a["sqrt_s_TeV"],
            "measurement_central_value": n_meas,
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_predicted_n_ch": n_pred,
            "residual_value": residual,
            "residual_percent": residual_pct,
            "distance_in_sigma": distance_sigma,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": "RESIDUAL_COMPUTED",
            "admissibility_rationale": "",
            "row_label": row_label,
            "honest_negative_class": None,
            "declared_rejection_gate": None,
            "publication_reference": pub,
        })

    # Honest-negatives
    for a in env["honest_negative_anchors"]:
        exp = a["experiment"]
        pub = a["publication_reference"]
        cls = a["honest_negative_class"]
        declared_gate = a["expected_rejection_gate"]
        admitted, adm_rationale = admissibility_check(exp, pub)

        if not admitted:
            actual_gate = "GATE_A_ADMISSIBILITY"
            row_label = "REJECTED_AT_GATE_A_ADMISSIBILITY"
            n_pred = None
            residual = None
            residual_pct = None
            distance_sigma = None
        else:
            n_pred = predicted_n_ch(a["sqrt_s_TeV"], sqrt_s_0, n_ch_0)
            n_meas = a["measurement_central_value"]
            sigma_combined = math.sqrt(a["stat_uncertainty"] ** 2 + a["sys_uncertainty"] ** 2)
            residual = n_pred - n_meas
            residual_pct = (residual / n_meas) * 100.0 if n_meas != 0 else None
            distance_sigma = abs(residual) / sigma_combined if sigma_combined > 0 else None
            actual_gate = "GATE_R_RESIDUAL"
            if distance_sigma is not None and distance_sigma > 3.0:
                row_label = "REJECTED_AT_GATE_R_RESIDUAL"
            else:
                row_label = "HONEST_NEGATIVE_NOT_REJECTED_AT_DECLARED_GATE"

        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "HONEST_NEGATIVE",
            "experiment": exp,
            "sqrt_s_TeV": a["sqrt_s_TeV"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_predicted_n_ch": n_pred,
            "residual_value": residual,
            "residual_percent": residual_pct,
            "distance_in_sigma": distance_sigma,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "actual_gate": actual_gate,
            "admissibility_rationale": adm_rationale,
            "row_label": row_label,
            "honest_negative_class": cls,
            "declared_rejection_gate": declared_gate,
            "publication_reference": pub,
        })

    fns = list(evidence_rows[0].keys())
    with open(EVIDENCE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in evidence_rows:
            w.writerow(r)
    print(f"  wrote {EVIDENCE_CSV.name} ({len(evidence_rows)} rows)")

    # Cross-source observed alpha pairs
    live_rows = [r for r in evidence_rows if r["row_class"] == "LIVE_ANCHOR" and r["actual_gate"] == "RESIDUAL_COMPUTED"]
    # Sort by sqrt_s
    live_rows_sorted = sorted(live_rows, key=lambda r: r["sqrt_s_TeV"])
    alpha_pairs = []
    for i, r_low in enumerate(live_rows_sorted):
        for r_high in live_rows_sorted[i + 1:]:
            if r_high["sqrt_s_TeV"] <= r_low["sqrt_s_TeV"]:
                continue
            s_low = r_low["sqrt_s_TeV"] ** 2
            s_high = r_high["sqrt_s_TeV"] ** 2
            alpha = observed_alpha(s_high, s_low,
                                   r_high["measurement_central_value"],
                                   r_low["measurement_central_value"])
            if alpha is not None:
                alpha_pairs.append({
                    "low_anchor": r_low["row_id"],
                    "low_experiment": r_low["experiment"],
                    "low_sqrt_s_TeV": r_low["sqrt_s_TeV"],
                    "high_anchor": r_high["row_id"],
                    "high_experiment": r_high["experiment"],
                    "high_sqrt_s_TeV": r_high["sqrt_s_TeV"],
                    "alpha_obs": alpha,
                })

    median_alpha_obs = None
    if alpha_pairs:
        alphas = sorted(p["alpha_obs"] for p in alpha_pairs)
        median_alpha_obs = alphas[len(alphas) // 2]

    # Per-anchor verdict tally
    label_counts = {}
    for r in evidence_rows:
        label_counts[r["row_label"]] = label_counts.get(r["row_label"], 0) + 1

    # Verdict
    live_non_norm = [r for r in live_rows if r["row_id"] != "A1"]
    any_outside_3sigma = any(r["row_label"] == "AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA" for r in live_non_norm)
    all_within_2sigma = all(r["row_label"] in ("AGREEMENT_WITHIN_ANCHOR_1_SIGMA", "AGREEMENT_WITHIN_ANCHOR_2_SIGMA") for r in live_non_norm)

    if any_outside_3sigma:
        verdict = "CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC"
    elif all_within_2sigma:
        verdict = "CANDIDATE_4_SIMPLE_READING_CONFIRMED"
    else:
        verdict = "VERDICT_INCONCLUSIVE"

    # Honest-negative gate-mismatch count
    hn_rows = [r for r in evidence_rows if r["row_class"] == "HONEST_NEGATIVE"]
    hn_correctly_gated = sum(1 for r in hn_rows if r["actual_gate"] == r["declared_rejection_gate"])

    summary = {
        "cr_id": "CR103",
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "MULTIPLICITY_SCALING_EXPONENT_TEST_FOR_GATE_1_SIMPLEST_READING",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "subject_gate": "GATE_1",
        "sam_committed_candidate": "paired source/recoil count (simplest reading)",
        "alpha_SAM": ALPHA_SAM,
        "median_alpha_observed_cross_source": median_alpha_obs,
        "alpha_pairs_count": len(alpha_pairs),
        "alpha_SAM_minus_median_alpha_obs": (ALPHA_SAM - median_alpha_obs) if median_alpha_obs is not None else None,
        "live_anchor_count": len(live_rows),
        "honest_negative_count": len(hn_rows),
        "honest_negative_correctly_gated_count": hn_correctly_gated,
        "row_label_counts": label_counts,
        "alpha_pairs": alpha_pairs,
        "normalization_anchor": "ATLAS at sqrt(s)=0.9 TeV (A1)",
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_sha256": envelope_sha,
        "anchor_envelope_open_utc": envelope_open_utc,
        "blindness_protocol_sha256": blindness_sha,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        "open_debts": premises["open_debts_declared_at_CR103"],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # result.md
    md = []
    md.append("# CR103 GATE_1 N_SW Multiplicity Scaling - Result\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(f"CR103_{verdict} (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## SAM Commitment (Locked Before Anchor Open)\n\n```text\n")
    md.append("GATE_1 candidate: paired source/recoil count (#4 from CR100 enumeration)\n")
    md.append("Reading: simplest (one source-recoil pair = one produced particle;\n")
    md.append("          total pairs linear in collision available energy)\n")
    md.append(f"Predicted scaling: N_ch(s) = K * s^(alpha_SAM/2)\n")
    md.append(f"alpha_SAM = {ALPHA_SAM}\n")
    md.append("Free parameters in exponent: 0\n")
    md.append("Free parameters in normalization: 1 (anchored at lowest sqrt(s))\n")
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
    md.append("## Per-Anchor Prediction vs Measurement\n\n")
    md.append("| Row | Experiment | sqrt(s) TeV | Measured | SAM predicted | Residual | %  | Sigma | Label |\n")
    md.append("|---|---|---|---|---|---|---|---|---|\n")
    for r in [r for r in evidence_rows if r["row_class"] == "LIVE_ANCHOR"]:
        n_pred = f"{r['sam_predicted_n_ch']:.2f}" if r['sam_predicted_n_ch'] else "n/a"
        res = f"{r['residual_value']:+.2f}" if r['residual_value'] is not None else "n/a"
        res_pct = f"{r['residual_percent']:+.1f}%" if r['residual_percent'] is not None else "n/a"
        sigma = f"{r['distance_in_sigma']:.1f}" if r['distance_in_sigma'] is not None else "n/a"
        md.append(
            f"| {r['row_id']} | {r['experiment']} | {r['sqrt_s_TeV']} | "
            f"{r['measurement_central_value']:.2f} +/- {math.sqrt(r['stat_uncertainty']**2+r['sys_uncertainty']**2):.2f} | "
            f"{n_pred} | {res} | {res_pct} | {sigma} | {r['row_label']} |\n"
        )
    md.append("\n## Cross-Source Observed Scaling Exponents\n\n")
    md.append("| Low anchor | High anchor | alpha_obs |\n")
    md.append("|---|---|---|\n")
    for p in alpha_pairs:
        md.append(
            f"| {p['low_experiment']} at {p['low_sqrt_s_TeV']} TeV ({p['low_anchor']}) | "
            f"{p['high_experiment']} at {p['high_sqrt_s_TeV']} TeV ({p['high_anchor']}) | "
            f"{p['alpha_obs']:.3f} |\n"
        )
    md.append(f"\n**Median alpha_obs:** `{median_alpha_obs:.3f}` if cross-source pairs available.\n\n")
    md.append("## Exponent Comparison\n\n```text\n")
    md.append(f"SAM alpha_SAM (simple reading)   = {ALPHA_SAM:.3f}\n")
    if median_alpha_obs is not None:
        md.append(f"median alpha_obs (LHC data)      = {median_alpha_obs:.3f}\n")
        md.append(f"difference alpha_SAM - alpha_obs = {ALPHA_SAM - median_alpha_obs:+.3f}\n")
    md.append("```\n\n")
    md.append("## Honest-Negative Resolution Proof\n\n")
    md.append("| Row | Class | Anchor | Declared gate | Actual gate | Label |\n")
    md.append("|---|---|---|---|---|---|\n")
    for r in hn_rows:
        md.append(
            f"| {r['row_id']} | {r['honest_negative_class']} | {r['experiment']} | "
            f"{r['declared_rejection_gate']} | {r['actual_gate']} | {r['row_label']} |\n"
        )
    md.append(f"\nHonest-negatives correctly gated: {hn_correctly_gated} / {len(hn_rows)}\n\n")
    md.append("## What This Test Means\n\n```text\n")
    if verdict == "CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC":
        md.append("LHC pp data scales much more slowly with collision energy than\n")
        md.append("SAM's simplest reading of GATE_1 candidate #4 predicts. The naive\n")
        md.append("linear-in-energy mapping from 'paired source/recoil count' to\n")
        md.append("'particle multiplicity' is firmly disfavored at LHC precision.\n\n")
        md.append("This does NOT close GATE_1 against candidate #4 entirely - it\n")
        md.append("closes the SIMPLEST READING of that candidate. A non-trivial\n")
        md.append("N_SW -> multiplicity mapping where each particle uses many SWs\n")
        md.append("(more SWs per particle at higher energy) could in principle\n")
        md.append("reproduce the observed s^0.11 scaling.\n\n")
        md.append("The other three candidates (local echo intensity, signed contact\n")
        md.append("count, closed-loop intersection count) remain in CR100's sealed\n")
        md.append("enumeration. CR103 has narrowed the closure space by one\n")
        md.append("specific reading.\n\n")
        md.append("Upstream consequence: SAM needs a multi-SW-per-particle scaling\n")
        md.append("law to make any of the four N_SW candidates reproduce the\n")
        md.append("observed slow multiplicity growth.\n")
    elif verdict == "CANDIDATE_4_SIMPLE_READING_CONFIRMED":
        md.append("SAM's simplest reading of N_SW = paired source/recoil count\n")
        md.append("matches LHC multiplicity scaling. GATE_1 candidate #4 partially\n")
        md.append("closed under this reading.\n")
    else:
        md.append("Cross-source variance exceeds what the comparison can constrain.\n")
        md.append("Recorded inconclusively.\n")
    md.append("```\n\n")
    md.append("## Rule-9 Line\n\n```text\n")
    md.append("This CR tested ONE specific reading of ONE specific candidate\n")
    md.append("(candidate #4 simplest reading). It does not falsify GATE_1\n")
    md.append("candidate #4 in general; it does not exclude candidates 1-3;\n")
    md.append("it does not modify CR100's sealed open-gate enumeration.\n\n")
    md.append("What it does: narrow the closure space by recording on the\n")
    md.append("public sealed record that one specific naive reading does not\n")
    md.append("match world-class LHC multiplicity measurements. That is real\n")
    md.append("progress toward GATE_1 closure - even when the news is bad,\n")
    md.append("the bad news points SAM to where the next derivation must do\n")
    md.append("more work.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR103 runner: complete")


if __name__ == "__main__":
    main()
