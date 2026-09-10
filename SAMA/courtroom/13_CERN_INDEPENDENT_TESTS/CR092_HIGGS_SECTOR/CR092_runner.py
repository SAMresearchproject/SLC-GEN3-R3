"""
CR092_runner.py - Higgs mass slice. Same blindness procedure as CR091.
"""
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

EVIDENCE_09A = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR062a_ROW_BY_ROW_PARTICLE_LEDGER" / "CR062a_evidence_rows.csv"
BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"

PREDICTIONS_CSV = CR_DIR / "CR092_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR092_prediction_commit.json"
ANCHOR_ENVELOPE = CR_DIR / "CR092_cern_anchor_envelope.json"
ANCHOR_SHA256_SIBLING = CR_DIR / "CR092_cern_anchor_envelope.json.sha256.txt"
EVIDENCE_CSV = CR_DIR / "CR092_evidence_rows.csv"
SUMMARY_JSON = CR_DIR / "CR092_summary.json"
RESULT_MD = CR_DIR / "CR092_result.md"

OBSERVATION_BANDS = {"Higgs boson mass": 300.0}
PREDICTION_MAP = {"Higgs boson mass": ("09a/CR062a row 15 (Higgs boson)", 15)}


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_predictions():
    with open(EVIDENCE_09A, newline="", encoding="utf-8") as f:
        by_order = {int(r["order"]): r for r in csv.DictReader(f) if r.get("order", "").isdigit()}
    out = {}
    for obs, (label, idx) in PREDICTION_MAP.items():
        r = by_order[idx]
        out[obs] = {
            "predicted_value": float(r["predicted_mass_MeV"]),
            "sam_prediction_source": label,
            "source_row_symbol": r["symbol_or_carrier"],
        }
    return out


def main():
    print("CR092 runner: starting")
    preds = load_predictions()
    print(f"  loaded {len(preds)} 09a predictions")

    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["observable_name", "sam_prediction_value_MeV", "sam_prediction_source", "source_row_symbol", "free_parameters_introduced"])
        for obs, p in preds.items():
            w.writerow([obs, f"{p['predicted_value']:.6g}", p["sam_prediction_source"], p["source_row_symbol"], 0])

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR092_PREDICTION_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_unopened_at_commit_time": True,
            "blindness_pillar": "PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH",
        }, f, indent=2)
    print(f"  prediction committed sha256={prediction_sha[:16]}... utc={prediction_utc}")

    computed = sha256_file(ANCHOR_ENVELOPE)
    declared = ANCHOR_SHA256_SIBLING.read_text(encoding="ascii").strip()
    if computed != declared:
        sys.exit(f"FATAL: envelope sha256 mismatch declared={declared} computed={computed}")
    envelope_sha = computed

    envelope_open_utc = now_utc()
    with open(ANCHOR_ENVELOPE, "r", encoding="utf-8") as f:
        env = json.load(f)
    print(f"  envelope opened at {envelope_open_utc}")

    if prediction_utc > envelope_open_utc:
        sys.exit("FATAL: prediction_commit_utc must precede anchor_envelope_open_utc")

    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    rows = []
    for a in env["anchors"]:
        obs = a["observable_name"]
        p = preds.get(obs)
        if p is None:
            label = "INFORMATION_INSUFFICIENT_AT_THIS_CR"
            rv = rp = sv = ss = ob = None
        else:
            sv = p["predicted_value"]
            ss = p["sam_prediction_source"]
            av = float(a["measurement_central_value"])
            rv = sv - av
            rp = rv / av * 100.0
            ob = OBSERVATION_BANDS.get(obs)
            label = "AGREEMENT_WITHIN_DECLARED_BAND" if (ob is not None and abs(rv) <= ob) else "AGREEMENT_OUTSIDE_DECLARED_BAND"
        rows.append({
            "row_id": a["row_id"],
            "observable_name": obs,
            "experiment": a["experiment"],
            "publication_reference": a["publication_reference"],
            "publication_date_utc": a["publication_date_utc"],
            "measurement_central_value": a["measurement_central_value"],
            "stat_uncertainty": a["stat_uncertainty"],
            "sys_uncertainty": a["sys_uncertainty"],
            "units": a["units"],
            "sam_prediction_value": sv,
            "sam_prediction_source": ss,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "anchor_envelope_sha256": envelope_sha,
            "anchor_envelope_open_utc": envelope_open_utc,
            "blindness_protocol_sha256": blindness_sha,
            "residual_value_in_units": rv,
            "residual_percent": rp,
            "observation_band_value_in_units": ob,
            "cross_source_status": a.get("cross_source_status"),
            "row_label": label,
        })

    fns = list(rows[0].keys()) if rows else []
    with open(EVIDENCE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    counts = {}
    for r in rows:
        counts[r["row_label"]] = counts.get(r["row_label"], 0) + 1

    summary = {
        "cr_id": "CR092",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "OBSERVATIONAL_COMPARISON_OF_LOCKED_09A_PREDICTION_AGAINST_CERN_HIGGS_MASS_ANCHORS",
        "execution_status": "CLEAN",
        "result_class": "OBSERVATIONAL_COMPARISON_REPORT_BUILT",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "anchor_rows_total": len(rows),
        "row_label_counts": counts,
        "observation_bands_MeV": OBSERVATION_BANDS,
        "blindness_protocol_sha256": blindness_sha,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_sha256": envelope_sha,
        "anchor_envelope_open_utc": envelope_open_utc,
        "open_debts": ["BLINDNESS_PROTOCOL sha256 sibling pending", "seal sha256 sibling pending", "citation_verification PENDING"],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR092 Higgs Sector (Mass Slice) - Provisional Result\n\n")
    md.append("## Verdict\n\n```text\nCR092_OBSERVATIONAL_COMPARISON_REPORT_BUILT (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n\n")
    md.append("## Blindness Proof\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"anchor_envelope_sha256   = {envelope_sha}\n")
    md.append(f"anchor_envelope_open_utc = {envelope_open_utc}\n")
    md.append("temporal_ordering        = OK\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## Per-Row Comparison\n\n")
    md.append("| Row | Observable | Experiment | CERN value | 09a prediction | Residual | Band | Label |\n")
    md.append("|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        pred = f"{r['sam_prediction_value']:.1f} {r['units']}" if r["sam_prediction_value"] else "n/a"
        band = f"+/- {r['observation_band_value_in_units']:.0f} {r['units']}" if r["observation_band_value_in_units"] else "n/a"
        cern = f"{r['measurement_central_value']:.1f} +/- {r['stat_uncertainty']:.1f} (stat) +/- {r['sys_uncertainty']:.1f} (sys) {r['units']}"
        resid = f"{r['residual_value_in_units']:+.2f} {r['units']} ({r['residual_percent']:+.4f}%)" if r["residual_value_in_units"] is not None else "n/a"
        md.append(f"| {r['row_id']} | {r['observable_name']} | {r['experiment']} | {cern} | {pred} | {resid} | {band} | {r['row_label']} |\n")
    md.append("\n## Row Label Counts\n\n```text\n")
    for k, v in counts.items():
        md.append(f"{k:45s} {v}\n")
    md.append("```\n\n## Rule-9 Reminder\n\n```text\nThis CR does not falsify 09a. 09a's exemplary verdict is preserved\nregardless of where each residual lands.\n```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print("CR092 runner: complete")


if __name__ == "__main__":
    main()
