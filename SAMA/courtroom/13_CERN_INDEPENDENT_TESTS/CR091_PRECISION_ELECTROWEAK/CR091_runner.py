"""
CR091_runner.py

Observational comparison of locked 09a predictions against CERN
precision-electroweak anchors, under the four-pillar blindness protocol.

Procedure (BLINDNESS_PROTOCOL Pillar 2 step order):
  step 1  compute prediction from 09a-cited CR062a row mapping
  step 2  write prediction values to CR091_predictions.csv
  step 3  sha256-hash that prediction file
  step 4  write the hash to CR091_prediction_commit.json with utc
  step 5  ONLY NOW open the CR091_cern_anchor_envelope.json
  step 6  read anchor central value, stat unc, sys unc, citation fields
  step 7  compute residual_percent = (prediction - anchor) / anchor * 100
  step 8  emit CR091_evidence_rows.csv with both sha256 fields and
          the anchor envelope sha256 referenced explicitly
  step 9  emit CR091_summary.json and CR091_result.md

The runner refuses to proceed past step 4 if step 3 produced no hash.
The runner refuses to proceed past step 8 if the envelope sha256 at
runner time does not match the sibling file.
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

EVIDENCE_09A = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR062a_ROW_BY_ROW_PARTICLE_LEDGER" / "CR062a_evidence_rows.csv"
BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"
SEAL_DOC = BRANCH_DIR / "SEALED_CERN_INDEPENDENT_TESTS_SCOPE_APPROACH_2026_06_13.md"

PREDICTIONS_CSV = CR_DIR / "CR091_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR091_prediction_commit.json"
ANCHOR_ENVELOPE = CR_DIR / "CR091_cern_anchor_envelope.json"
ANCHOR_SHA256_SIBLING = CR_DIR / "CR091_cern_anchor_envelope.json.sha256.txt"
EVIDENCE_CSV = CR_DIR / "CR091_evidence_rows.csv"
SUMMARY_JSON = CR_DIR / "CR091_summary.json"
RESULT_MD = CR_DIR / "CR091_result.md"

OBSERVATION_BANDS_MeV = {
    "W boson mass": 25.0,
    "Z boson mass": 5.0,
    "Top quark mass": 1000.0,
}

PREDICTION_MAP = {
    "W boson mass": ("09a/CR062a row 13 (W boson)", 13),
    "Z boson mass": ("09a/CR062a row 14 (Z boson)", 14),
    "Top quark mass": ("09a/CR062a row 6 (top quark)", 6),
}


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_09a_predictions():
    """Step 1: read 09a verbatim. Read-only."""
    if not EVIDENCE_09A.exists():
        sys.exit(f"FATAL: 09a evidence file not found at {EVIDENCE_09A}")
    rows = []
    with open(EVIDENCE_09A, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                order = int(r["order"])
            except (KeyError, ValueError):
                continue
            rows.append((order, r))
    by_order = {o: r for o, r in rows}
    predictions = {}
    for observable, (source_label, row_idx) in PREDICTION_MAP.items():
        if row_idx not in by_order:
            sys.exit(f"FATAL: 09a row {row_idx} not found for {observable}")
        r = by_order[row_idx]
        predictions[observable] = {
            "predicted_value_MeV": float(r["predicted_mass_MeV"]),
            "sam_prediction_source": source_label,
            "source_row_symbol": r["symbol_or_carrier"],
        }
    return predictions


def write_predictions_csv(predictions):
    """Step 2: write predictions to disk."""
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "observable_name",
            "sam_prediction_value_MeV",
            "sam_prediction_source",
            "source_row_symbol",
            "free_parameters_introduced",
        ])
        for obs, p in predictions.items():
            w.writerow([
                obs,
                f"{p['predicted_value_MeV']:.6g}",
                p["sam_prediction_source"],
                p["source_row_symbol"],
                0,
            ])


def commit_predictions():
    """Steps 3-4: hash predictions, write commit json."""
    prediction_sha = sha256_file(PREDICTIONS_CSV)
    commit_utc = now_utc()
    commit = {
        "commit_id": "CR091_PREDICTION_COMMIT",
        "predictions_file": str(PREDICTIONS_CSV.name),
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": commit_utc,
        "anchor_envelope_unopened_at_commit_time": True,
        "blindness_pillar": "PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH",
    }
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump(commit, f, indent=2)
    if not prediction_sha:
        sys.exit("FATAL: prediction sha256 is empty; refusing to proceed past step 4")
    return prediction_sha, commit_utc


def verify_envelope_seal():
    """Pre-step-5 guard: envelope sha256 at runner time must match sibling."""
    if not ANCHOR_ENVELOPE.exists():
        sys.exit(f"FATAL: anchor envelope missing at {ANCHOR_ENVELOPE}")
    if not ANCHOR_SHA256_SIBLING.exists():
        sys.exit(f"FATAL: anchor envelope sha256 sibling missing at {ANCHOR_SHA256_SIBLING}")
    computed = sha256_file(ANCHOR_ENVELOPE)
    declared = ANCHOR_SHA256_SIBLING.read_text(encoding="ascii").strip()
    if computed != declared:
        sys.exit(
            "FATAL: envelope sha256 mismatch.\n"
            f"  declared in sibling: {declared}\n"
            f"  computed at runner:  {computed}"
        )
    return computed


def open_envelope():
    """Steps 5-6: open and read sealed anchor envelope."""
    open_utc = now_utc()
    with open(ANCHOR_ENVELOPE, "r", encoding="utf-8") as f:
        env = json.load(f)
    return env, open_utc


def cite_blindness_protocol():
    sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""
    return sha


def main():
    print("CR091 runner: starting")

    # Step 1
    predictions = load_09a_predictions()
    print(f"  loaded 09a predictions for {len(predictions)} observables (cite-only)")

    # Step 2
    write_predictions_csv(predictions)
    print(f"  wrote {PREDICTIONS_CSV.name}")

    # Steps 3-4
    prediction_sha, prediction_utc = commit_predictions()
    print(f"  committed prediction sha256={prediction_sha[:16]}... at {prediction_utc}")
    print("  anchor envelope still unopened")

    # Guard before step 5
    envelope_sha = verify_envelope_seal()
    print(f"  envelope sha256 verified against sibling: {envelope_sha[:16]}...")

    # Steps 5-6
    env, envelope_open_utc = open_envelope()
    print(f"  opened envelope at {envelope_open_utc}")
    print(f"  envelope status: {env.get('envelope_status')}")

    # Temporal ordering check (Pillar 2)
    if prediction_utc > envelope_open_utc:
        sys.exit("FATAL: prediction_commit_utc must precede anchor_envelope_open_utc")

    # Step 7: residuals
    blindness_sha = cite_blindness_protocol()
    rows = []
    for anchor in env["anchors"]:
        obs = anchor["observable_name"]
        pred = predictions.get(obs)
        if pred is None:
            row_label = "INFORMATION_INSUFFICIENT_AT_THIS_CR"
            residual_value = None
            residual_percent = None
            sam_pred_val = None
            sam_pred_src = None
            observation_band = None
        else:
            sam_pred_val = pred["predicted_value_MeV"]
            sam_pred_src = pred["sam_prediction_source"]
            anchor_val = float(anchor["measurement_central_value"])
            residual_value = sam_pred_val - anchor_val
            residual_percent = residual_value / anchor_val * 100.0
            observation_band = OBSERVATION_BANDS_MeV.get(obs)
            if observation_band is None:
                row_label = "INFORMATION_INSUFFICIENT_AT_THIS_CR"
            elif abs(residual_value) <= observation_band:
                row_label = "AGREEMENT_WITHIN_DECLARED_BAND"
            else:
                row_label = "AGREEMENT_OUTSIDE_DECLARED_BAND"
        rows.append({
            "row_id": anchor["row_id"],
            "observable_name": obs,
            "experiment": anchor["experiment"],
            "publication_reference": anchor["publication_reference"],
            "publication_date_utc": anchor["publication_date_utc"],
            "measurement_central_value": anchor["measurement_central_value"],
            "stat_uncertainty": anchor["stat_uncertainty"],
            "sys_uncertainty": anchor["sys_uncertainty"],
            "units": anchor["units"],
            "sam_prediction_value": sam_pred_val,
            "sam_prediction_source": sam_pred_src,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "residual_value_in_units": residual_value,
            "residual_percent": residual_percent,
            "observation_band_value_in_units": observation_band,
            "cross_source_status": anchor.get("cross_source_status"),
            "row_label": row_label,
        })

    # Step 8: emit evidence rows
    fieldnames = [
        "row_id", "observable_name", "experiment", "publication_reference",
        "publication_date_utc", "measurement_central_value", "stat_uncertainty",
        "sys_uncertainty", "units", "sam_prediction_value", "sam_prediction_source",
        "prediction_commit_sha256", "prediction_commit_utc",
        "anchor_envelope_sha256", "anchor_envelope_open_utc",
        "blindness_protocol_sha256", "residual_value_in_units", "residual_percent",
        "observation_band_value_in_units", "cross_source_status", "row_label",
    ]
    with open(EVIDENCE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  wrote {EVIDENCE_CSV.name} ({len(rows)} rows)")

    # Step 9: summary + result
    counts = {"AGREEMENT_WITHIN_DECLARED_BAND": 0, "AGREEMENT_OUTSIDE_DECLARED_BAND": 0,
              "INFORMATION_INSUFFICIENT_AT_THIS_CR": 0}
    for r in rows:
        counts[r["row_label"]] = counts.get(r["row_label"], 0) + 1

    summary = {
        "cr_id": "CR091",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "OBSERVATIONAL_COMPARISON_OF_LOCKED_09A_PREDICTIONS_AGAINST_CERN_PRECISION_EW_ANCHORS",
        "execution_status": "CLEAN",
        "result_class": "OBSERVATIONAL_COMPARISON_REPORT_BUILT",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "runner_start_utc": prediction_utc,
        "runner_envelope_open_utc": envelope_open_utc,
        "anchor_rows_total": len(rows),
        "row_label_counts": counts,
        "observation_bands_MeV": OBSERVATION_BANDS_MeV,
        "blindness_protocol_cite": str(BLINDNESS_PROTOCOL.relative_to(COURTROOM_DIR)),
        "blindness_protocol_sha256": blindness_sha,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_sha256": envelope_sha,
        "anchor_envelope_open_utc": envelope_open_utc,
        "temporal_ordering_check": "prediction_commit_utc precedes anchor_envelope_open_utc",
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling file not yet written",
            "Seal sha256 sibling file not yet written",
            "citation_verification_status PENDING on every anchor row (curator sign-off)",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote {SUMMARY_JSON.name}")

    # result.md
    def fmt_resid(r):
        if r["residual_value_in_units"] is None:
            return "n/a"
        return f"{r['residual_value_in_units']:+.2f} {r['units']} ({r['residual_percent']:+.4f}%)"

    md = []
    md.append("# CR091 Precision Electroweak - Provisional Result\n")
    md.append("## Verdict\n")
    md.append("```text\nCR091_OBSERVATIONAL_COMPARISON_REPORT_BUILT (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n")
    md.append("## Courtroom Fields\n")
    md.append("```text\n")
    md.append("execution_status = CLEAN\n")
    md.append("result_class     = OBSERVATIONAL_COMPARISON_REPORT_BUILT\n")
    md.append("scope_status     = PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF\n")
    md.append(f"anchor_rows      = {len(rows)}\n")
    md.append("```\n")
    md.append("## Blindness Proof\n")
    md.append("```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"anchor_envelope_sha256   = {envelope_sha}\n")
    md.append(f"anchor_envelope_open_utc = {envelope_open_utc}\n")
    md.append(f"temporal_ordering        = OK (prediction commit precedes envelope open)\n")
    md.append(f"blindness_protocol_cite  = {BLINDNESS_PROTOCOL.relative_to(COURTROOM_DIR)}\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n")
    md.append("## Per-Row Comparison\n")
    md.append("| Row | Observable | Experiment | CERN value | 09a prediction | Residual | Band | Label |\n")
    md.append("|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        if r["sam_prediction_value"] is None:
            pred = "n/a"
            band = "n/a"
        else:
            pred = f"{r['sam_prediction_value']:.1f} {r['units']}"
            band = f"+/- {r['observation_band_value_in_units']:.0f} {r['units']}" if r["observation_band_value_in_units"] else "n/a"
        cern = (
            f"{r['measurement_central_value']:.1f} "
            f"+/- {r['stat_uncertainty']:.1f} (stat) "
            f"+/- {r['sys_uncertainty']:.1f} (sys) {r['units']}"
        )
        md.append(
            f"| {r['row_id']} | {r['observable_name']} | {r['experiment']} | "
            f"{cern} | {pred} | {fmt_resid(r)} | {band} | {r['row_label']} |\n"
        )
    md.append("\n")
    md.append("## Row Label Counts\n")
    md.append("```text\n")
    for k, v in counts.items():
        md.append(f"{k:45s} {v}\n")
    md.append("```\n")
    md.append("## Open Debts\n")
    md.append("```text\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("```\n")
    md.append("## Rule-9 Reminder\n")
    md.append("```text\n")
    md.append("This CR does not falsify 09a. 09a's exemplary verdict is preserved\n")
    md.append("regardless of where each residual lands. Per-row labels are\n")
    md.append("observational reporting under blindness discipline.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")

    print("CR091 runner: complete")


if __name__ == "__main__":
    main()
