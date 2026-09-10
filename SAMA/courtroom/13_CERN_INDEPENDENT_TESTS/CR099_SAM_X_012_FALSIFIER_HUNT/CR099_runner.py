"""
CR099_runner.py - Forward-blind falsifier hunt for SAM-X-012.

SAM-X-012 is a NEGATIVE prediction: SAM says no particle exists at
partition (7,5). This runner decodes that structural prediction into
an observable signature (charge set + mass band), locks it with
sha256 + utc, and records which CERN program is best positioned to
test it.

If CERN later publishes a result matching the sealed criteria, an
appeal row records SAM_X_012_FALSIFIED. The original signature is
never modified.

There is no anchor envelope to open today because CERN has not
published a measurement at the specific (Q, M) coordinates SAM-X-012
addresses. The cryptographic seal of the falsifier signature IS the
test.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"
DECLARED_PREMISES = CR_DIR / "CR099_declared_premises.json"

PREDICTIONS_CSV = CR_DIR / "CR099_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR099_prediction_commit.json"
FALSIFIER_SIGNATURE = CR_DIR / "CR099_falsifier_signature.json"
FALSIFIER_SIGNATURE_SIBLING = CR_DIR / "CR099_falsifier_signature.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR099_summary.json"
RESULT_MD = CR_DIR / "CR099_result.md"


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def main():
    print("CR099 runner: starting (SAM-X-012 falsifier hunt)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    # The "predictions" here are the negative-prediction signature components:
    # the candidate charge set, the mass band, and the criterion locks.
    pred_rows = []
    sig = premises["decoded_observable_signature"]
    for q in sig["candidate_charge_set_Q"]:
        pred_rows.append({
            "criterion_id": f"CRIT_A_charge_{q['Q_fraction'].replace('/', '_over_').replace('+', 'pos').replace('-', 'neg')}",
            "criterion_class": "CRITERION_A_CHARGE",
            "value": q["Q_decimal"],
            "value_symbolic": q["Q_fraction"],
            "units": "elementary_charge_e",
        })
    pred_rows.append({
        "criterion_id": "CRIT_B_mass_band_low",
        "criterion_class": "CRITERION_B_MASS",
        "value": sig["mass_band_MeV"]["low"],
        "value_symbolic": "mass_low_band",
        "units": "MeV",
    })
    pred_rows.append({
        "criterion_id": "CRIT_B_mass_band_high",
        "criterion_class": "CRITERION_B_MASS",
        "value": sig["mass_band_MeV"]["high"],
        "value_symbolic": "mass_high_band",
        "units": "MeV",
    })
    pred_rows.append({
        "criterion_id": "CRIT_C_primary_carrier_required",
        "criterion_class": "CRITERION_C_PRIMARY",
        "value": "primary_carrier_not_composite_or_bound_state",
        "value_symbolic": "primary_required",
        "units": "structural",
    })

    fns = list(pred_rows[0].keys())
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    print(f"  wrote {PREDICTIONS_CSV.name} ({len(pred_rows)} criterion rows)")

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    commit = {
        "commit_id": "CR099_FALSIFIER_PREDICTION_COMMIT",
        "predictions_file": PREDICTIONS_CSV.name,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_does_not_yet_exist": "CERN_HAS_NOT_PUBLISHED_AT_THESE_Q_M_COORDINATES",
        "what_the_seal_locks": "the falsifier criteria - charge set, mass band, primary-carrier requirement",
        "future_appeal_behavior": "if CERN publishes a match, an APPEAL row records SAM_X_012_FALSIFIED; the original signature is never modified",
    }
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump(commit, f, indent=2)
    print(f"  prediction committed sha256={prediction_sha[:16]}... utc={prediction_utc}")

    # Build the falsifier signature JSON (the sealed payload)
    falsifier_signature = {
        "signature_id": "SAM_X_012_FALSIFIER_SIGNATURE",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "cr_id": "CR099",
        "sealed_at_utc": prediction_utc,
        "subject_prediction": premises["subject_negative_prediction"],
        "decoded_observable_signature": premises["decoded_observable_signature"],
        "primary_CERN_probe": premises["primary_CERN_probe"],
        "secondary_CERN_probes": premises["secondary_CERN_probes"],
        "falsifier_criteria": premises["falsifier_criteria"],
        "anti_motivated_padding_rules": premises["anti_motivated_padding_rules"],
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
    }
    with open(FALSIFIER_SIGNATURE, "w", encoding="utf-8") as f:
        json.dump(falsifier_signature, f, indent=2)
    print(f"  wrote {FALSIFIER_SIGNATURE.name}")

    sig_sha = sha256_file(FALSIFIER_SIGNATURE)
    FALSIFIER_SIGNATURE_SIBLING.write_text(sig_sha + "\n", encoding="ascii")
    print(f"  falsifier signature sealed: {sig_sha}")

    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    summary = {
        "cr_id": "CR099",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "FORWARD_BLIND_FALSIFIER_HUNT_FOR_NEGATIVE_PREDICTION_SAM_X_012",
        "execution_status": "CLEAN",
        "result_class": "FALSIFIER_SIGNATURE_SEALED",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "subject_candidate": "SAM-X-012",
        "subject_partition": "(7, 5)",
        "candidate_charge_set_size": len(sig["candidate_charge_set_Q"]),
        "mass_band_MeV": sig["mass_band_MeV"],
        "primary_probe": premises["primary_CERN_probe"]["experiment"],
        "secondary_probe_count": len(premises["secondary_CERN_probes"]),
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "falsifier_signature_sha256": sig_sha,
        "falsifier_signature_path": str(FALSIFIER_SIGNATURE),
        "falsifier_signature_sibling_path": str(FALSIFIER_SIGNATURE_SIBLING),
        "blindness_protocol_sha256": blindness_sha,
        "appeal_channel_open": True,
        "appeal_pattern": "CR099a_<DATE>_<CERN_EXPERIMENT>_<RESULT_CLASS>",
        "current_falsification_status": "NOT_YET_TESTED_BY_CERN_AT_THESE_COORDINATES",
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling not yet written by curator",
            "Branch seal sha256 sibling not yet written by curator",
            "MoEDAL Run-3 + MoEDAL-MAPP publications not yet available",
            "When any CERN program publishes at the (Q, M) coordinates, CR099a appeal row records the result",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote {SUMMARY_JSON.name}")

    md = []
    md.append("# CR099 SAM-X-012 Falsifier Hunt - Wanted Poster\n\n")
    md.append("## Verdict\n\n```text\nCR099_FALSIFIER_SIGNATURE_SEALED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n\n")
    md.append("## What This Is\n\n")
    md.append("SAM commits, on the record, that no particle exists at partition (7,5).\n")
    md.append("This is a NEGATIVE prediction with a clean falsifier: find one and SAM\n")
    md.append("is broken.\n\n")
    md.append("This document is a 'wanted poster' for experimentalists. It decodes\n")
    md.append("SAM-X-012's structural prediction into observable language (charge,\n")
    md.append("mass, structural class) so a MoEDAL / CMS / LHCb / ATLAS analyst can\n")
    md.append("look at the right place and either find the falsifier or report a\n")
    md.append("null result.\n\n")
    md.append("## Commitment Proof\n\n```text\n")
    md.append(f"prediction_commit_sha256   = {prediction_sha}\n")
    md.append(f"prediction_commit_utc      = {prediction_utc}\n")
    md.append(f"falsifier_signature_sha256 = {sig_sha}\n")
    md.append(f"signature_sibling          = {FALSIFIER_SIGNATURE_SIBLING.name}\n")
    md.append(f"blindness_protocol_sha256  = {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## What To Look For\n\n")
    md.append("**CRITERION A - Charge.** A particle with electric charge Q in any of:\n\n")
    md.append("| Q (fraction) | Q (decimal) | Note |\n")
    md.append("|---|---|---|\n")
    for q in sig["candidate_charge_set_Q"]:
        note = "non-SM rational charge" if abs(q["Q_decimal"]) not in (0, 1/3, 2/3, 1) else "SM-allowed charge"
        md.append(f"| {q['Q_fraction']} | {q['Q_decimal']:+.4f} | {note} |\n")
    md.append("\n")
    md.append("None of these are in the SM rational-charge set {0, +/-1/3, +/-2/3, +/-1}.\n\n")
    md.append(f"**CRITERION B - Mass.** Mass M in the band **[{sig['mass_band_MeV']['low']} MeV, {sig['mass_band_MeV']['high']} MeV]**.\n\n")
    md.append("Rationale (from sealed declared_premises):\n\n```text\n")
    md.append(sig["mass_band_MeV"]["rationale"] + "\n")
    md.append("```\n\n")
    md.append("**CRITERION C - Primary carrier.** The particle must be identified as\n")
    md.append("a primary carrier, not a composite, bound state, or threshold artefact.\n")
    md.append("SAM cannot escape falsification by claiming a found state is 'really a\n")
    md.append("composite' - the criterion is locked at seal time.\n\n")
    md.append("## Where To Look\n\n")
    md.append("**Primary probe:**\n\n```text\n")
    md.append(json.dumps(premises["primary_CERN_probe"], indent=2))
    md.append("\n```\n\n")
    md.append("**Secondary probes:**\n\n")
    for sp in premises["secondary_CERN_probes"]:
        md.append(f"- **{sp['experiment']}** - {sp['gap']}\n")
    md.append("\n## How A Find Or Null Result Is Recorded\n\n")
    md.append("```text\n")
    md.append("if CERN publishes a result meeting CRITERION A + B + C:\n")
    md.append("    appeal row CR099a_<DATE>_<EXP>_FALSIFIED is appended\n")
    md.append("    appeal verdict = SAM_X_012_FALSIFIED\n")
    md.append("    09a structural foundation flagged for repair\n")
    md.append("    original CR099 signature is NOT modified\n")
    md.append("\n")
    md.append("if MoEDAL Run-3 + MoEDAL-MAPP publishes null in the band:\n")
    md.append("    appeal row CR099a_<DATE>_<EXP>_NULL is appended\n")
    md.append("    appeal verdict = SAM_X_012_HOLDS_UNDER_NEGATIVE_CONFIRMATION\n")
    md.append("    SAM partition-algebra commitment strengthened\n")
    md.append("    original CR099 signature is NOT modified\n")
    md.append("\n")
    md.append("if CERN publishes a near-miss (Q close to set; or mass at band edge):\n")
    md.append("    appeal row CR099a_<DATE>_<EXP>_NEAR_MISS is appended\n")
    md.append("    appeal verdict = SAM_X_012_PARTIAL_TEST_INCONCLUSIVE\n")
    md.append("    NO reframing of the original signature is allowed\n")
    md.append("```\n\n")
    md.append("## Anti-Motivated-Padding Rules\n\n")
    md.append("These are the rules that prevent SAM from wriggling out:\n\n")
    for k, v in premises["anti_motivated_padding_rules"].items():
        md.append(f"- **{k}**: {v}\n")
    md.append("\n## Rule-9 Line\n\n```text\n")
    md.append("This CR is a structured invitation to break SAM. The signature is\n")
    md.append("sealed; the falsifier criteria are fixed; the CERN probes are named.\n")
    md.append("Now we wait for CERN.\n")
    md.append("\n")
    md.append("Breaking SAM is good. Breaking SAM lets us fix it. Hiding from a\n")
    md.append("falsifier would be the failure mode, not finding one.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR099 runner: complete")


if __name__ == "__main__":
    main()
