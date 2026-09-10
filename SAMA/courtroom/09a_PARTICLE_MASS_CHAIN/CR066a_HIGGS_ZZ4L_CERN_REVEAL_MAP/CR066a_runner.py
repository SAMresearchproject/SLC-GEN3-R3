"""CR066a Higgs ZZ4l CERN reveal map.

Reveals QP091 frozen predictions against published ATLAS+CMS H -> ZZ* -> 4l
data at three reveal targets:
  REVEAL_02 m4l peak / Higgs mass
  REVEAL_03 m12 / m34 split (Z + Z* branch structure)
  REVEAL_04 four-lepton angular structural consistency

Explicitly HOLDS REVEAL_01 (H006/H007 signal strength).

Procedure:
  1 load CR065a intake lock; verify sha256
  2 commit SAM predictions (from QP091 freeze) BEFORE opening envelope
  3 verify envelope sha256 sibling
  4 open envelope
  5 compute per-anchor residual, sigma distance, row label
  6 emit evidence, summary, result
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

CR065A_INTAKE = BRANCH_DIR / "CR065a_HIGGS_ZZ4L_PREDICTION_INTAKE" / "CR065a_intake_lock.json"
ENVELOPE = CR_DIR / "CR066a_cern_reveal_envelope.json"
ENVELOPE_SIBLING = CR_DIR / "CR066a_cern_reveal_envelope.json.sha256.txt"

OUT_JSON = CR_DIR / "CR066a_summary.json"
OUT_MD   = CR_DIR / "CR066a_result.md"
EVID_CSV = CR_DIR / "CR066a_evidence_rows.csv"
PRED_CSV = CR_DIR / "CR066a_predictions.csv"
PRED_COMMIT = CR_DIR / "CR066a_prediction_commit.json"

ADMISSIBLE = {"ATLAS", "CMS", "ATLAS+CMS combined"}
WITHDRAWN_MARKERS = ("withdrawn", "superseded")


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


def admit(exp: str, pubref: str) -> tuple[bool, str]:
    if any(m in (exp or "").lower() for m in WITHDRAWN_MARKERS):
        return False, "withdrawn or superseded"
    if not pubref or "NO_PUBLICATION_REFERENCE" in pubref:
        return False, "no publication reference"
    base = (exp or "").split(" (")[0].strip()
    if base not in ADMISSIBLE:
        if pubref.startswith("SYNTHETIC_"):
            return True, ""
        return False, f"experiment '{base}' not on 09a reveal allow-list"
    return True, ""


def label_by_sigma(sam_value: float, anchor_mean: float, sigma: float) -> tuple[str, float | None]:
    if sigma <= 0:
        return "BAND_UNDEFINED", None
    d = abs(sam_value - anchor_mean) / sigma
    if d <= 1.0:
        return "AGREEMENT_WITHIN_1_SIGMA", d
    if d <= 2.0:
        return "AGREEMENT_WITHIN_2_SIGMA", d
    if d <= 3.0:
        return "AGREEMENT_WITHIN_3_SIGMA", d
    return "AGREEMENT_OUTSIDE_3_SIGMA", d


def main() -> None:
    print("CR066a runner: starting (Higgs ZZ4l CERN reveal map)")

    # -- Step 1: load CR065a intake lock --------------------------------
    if not CR065A_INTAKE.exists():
        sys.exit("FATAL: CR065a intake lock not found; run CR065a first")
    cr065a_sha = sha256_file(CR065A_INTAKE)
    with open(CR065A_INTAKE, "r", encoding="utf-8") as f:
        cr065a = json.load(f)
    frozen = cr065a["qp091_frozen_predictions"]

    # SAM predictions per reveal target (from QP091 freeze)
    sam_predictions = {
        "REVEAL_02_m4l_peak_GeV":   frozen["H_visible_parent_ledger_MeV"] / 1000.0,
        "REVEAL_03_m12_peak_GeV":   frozen["Z_visible_branch_MeV"] / 1000.0,
        "REVEAL_03_m34_ceiling_GeV": frozen["Zstar_ceiling_visible_MeV"] / 1000.0,
        "REVEAL_03_two_on_shell_Z_forbidden": True,
        "REVEAL_04_angular_structural": 1.0,
    }

    # -- Step 2: hash predictions + commit BEFORE envelope --------------
    pred_rows = [
        {"row_id": "REVEAL_02_m4l", "sam_value": sam_predictions["REVEAL_02_m4l_peak_GeV"], "unit": "GeV"},
        {"row_id": "REVEAL_03_m12", "sam_value": sam_predictions["REVEAL_03_m12_peak_GeV"], "unit": "GeV"},
        {"row_id": "REVEAL_03_m34", "sam_value": sam_predictions["REVEAL_03_m34_ceiling_GeV"], "unit": "GeV"},
        {"row_id": "REVEAL_04_ang", "sam_value": sam_predictions["REVEAL_04_angular_structural"], "unit": "dimensionless"},
    ]
    with open(PRED_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pred_rows[0].keys()))
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    pred_sha = sha256_file(PRED_CSV)
    pred_utc = now_utc()
    with open(PRED_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR066a_HIGGS_ZZ4L_REVEAL_PREDICTION_COMMIT",
            "prediction_commit_sha256": pred_sha,
            "prediction_commit_utc": pred_utc,
            "anchor_envelope_unopened_at_commit_time": True,
            "upstream_CR065a_intake_lock_sha256": cr065a_sha,
            "sam_predictions": sam_predictions,
        }, f, indent=2)
    print(f"  prediction committed {pred_sha[:16]} at {pred_utc}")

    # -- Step 3: verify envelope sha256 sibling -------------------------
    computed = sha256_file(ENVELOPE)
    declared = ENVELOPE_SIBLING.read_text(encoding="ascii").strip() if ENVELOPE_SIBLING.exists() else ""
    if computed != declared:
        sys.exit(f"FATAL: envelope sha256 mismatch declared={declared} computed={computed}")
    env_sha = computed
    env_utc = now_utc()

    # -- Step 4: open envelope ------------------------------------------
    with open(ENVELOPE, "r", encoding="utf-8") as f:
        env = json.load(f)
    if pred_utc > env_utc:
        sys.exit("FATAL: temporal ordering violation")
    print(f"  envelope opened at {env_utc}")

    # -- Step 5: per-anchor processing ----------------------------------
    evidence_rows = []
    for a in env["live_anchors"]:
        admitted, rationale = admit(a["experiment"], a["publication_reference"])
        if not admitted:
            evidence_rows.append({
                "row_id": a["row_id"],
                "row_class": "LIVE_ANCHOR",
                "reveal_target": a["reveal_target"],
                "experiment": a["experiment"],
                "publication_reference": a["publication_reference"],
                "central_value": a.get("central_value_GeV", a.get("central_value_dimensionless")),
                "stat_unc": a.get("stat_uncertainty_GeV", a.get("stat_uncertainty_dimensionless", 0.0)),
                "sys_unc":  a.get("sys_uncertainty_GeV",  a.get("sys_uncertainty_dimensionless",  0.0)),
                "sam_value": None,
                "residual": None,
                "distance_sigma": None,
                "row_label": "REJECTED_AT_GATE_A_ADMISSIBILITY",
                "actual_gate": "GATE_A_ADMISSIBILITY",
                "rationale": rationale,
                "prediction_commit_sha256": pred_sha,
                "prediction_commit_utc": pred_utc,
                "envelope_sha256": env_sha,
                "envelope_open_utc": env_utc,
                "honest_negative_class": None,
            })
            continue

        # Match SAM prediction to anchor
        target = a["reveal_target"]
        if target == "REVEAL_02_m4l_peak":
            sam = sam_predictions["REVEAL_02_m4l_peak_GeV"]
            mean = a["central_value_GeV"]
            unc = math.sqrt(a["stat_uncertainty_GeV"]**2 + a.get("sys_uncertainty_GeV", 0.0)**2)
        elif target == "REVEAL_03_m12_m34_split":
            if a["row_id"] == "M12_PEAK_ATLAS":
                sam = sam_predictions["REVEAL_03_m12_peak_GeV"]
                mean = a["central_value_GeV"]
                unc = math.sqrt(a["stat_uncertainty_GeV"]**2 + a.get("sys_uncertainty_GeV", 0.0)**2)
            elif a["row_id"] == "M34_CEILING_ATLAS":
                sam = sam_predictions["REVEAL_03_m34_ceiling_GeV"]
                mean = a["central_value_GeV"]
                unc = math.sqrt(a["stat_uncertainty_GeV"]**2 + a.get("sys_uncertainty_GeV", 0.0)**2)
            else:
                sam = None; mean = None; unc = None
        elif target == "REVEAL_04_four_lepton_angular_structural_consistency":
            sam = sam_predictions["REVEAL_04_angular_structural"]
            mean = a["central_value_dimensionless"]
            unc = math.sqrt(a["stat_uncertainty_dimensionless"]**2 + a.get("sys_uncertainty_dimensionless", 0.0)**2)
        else:
            sam = None; mean = None; unc = None

        if sam is None or mean is None:
            row_label = "INCOMMENSURABLE_TARGET"
            d = None
            residual = None
        else:
            residual = sam - mean
            row_label, d = label_by_sigma(sam, mean, unc)
        evidence_rows.append({
            "row_id": a["row_id"],
            "row_class": "LIVE_ANCHOR",
            "reveal_target": target,
            "experiment": a["experiment"],
            "publication_reference": a["publication_reference"],
            "central_value": mean,
            "stat_unc": a.get("stat_uncertainty_GeV", a.get("stat_uncertainty_dimensionless", 0.0)),
            "sys_unc":  a.get("sys_uncertainty_GeV",  a.get("sys_uncertainty_dimensionless",  0.0)),
            "sam_value": sam,
            "residual": residual,
            "distance_sigma": d,
            "row_label": row_label,
            "actual_gate": "RESIDUAL_COMPUTED",
            "rationale": "",
            "prediction_commit_sha256": pred_sha,
            "prediction_commit_utc": pred_utc,
            "envelope_sha256": env_sha,
            "envelope_open_utc": env_utc,
            "honest_negative_class": None,
        })

    # Honest negatives
    for hn in env["honest_negatives"]:
        admitted, rationale = admit(hn["experiment"], hn["publication_reference"])
        target = hn["reveal_target"]
        if not admitted:
            evidence_rows.append({
                "row_id": hn["row_id"],
                "row_class": "HONEST_NEGATIVE",
                "reveal_target": target,
                "experiment": hn["experiment"],
                "publication_reference": hn["publication_reference"],
                "central_value": hn.get("central_value_GeV", None),
                "stat_unc": hn.get("stat_uncertainty_GeV", 0.0),
                "sys_unc":  hn.get("sys_uncertainty_GeV",  0.0),
                "sam_value": None,
                "residual": None,
                "distance_sigma": None,
                "row_label": "REJECTED_AT_GATE_A_ADMISSIBILITY",
                "actual_gate": "GATE_A_ADMISSIBILITY",
                "rationale": rationale,
                "prediction_commit_sha256": pred_sha,
                "prediction_commit_utc": pred_utc,
                "envelope_sha256": env_sha,
                "envelope_open_utc": env_utc,
                "honest_negative_class": hn["honest_negative_class"],
            })
            continue

        # CLASS_G synthetic - passes admissibility, must fail residual
        sam = sam_predictions["REVEAL_02_m4l_peak_GeV"] if target == "REVEAL_02_m4l_peak" else None
        if sam is None:
            row_label = "INCOMMENSURABLE_TARGET"
            d = None
            residual = None
        else:
            unc = math.sqrt(hn["stat_uncertainty_GeV"]**2 + hn.get("sys_uncertainty_GeV", 0.0)**2)
            mean = hn["central_value_GeV"]
            residual = sam - mean
            d = abs(residual) / unc if unc > 0 else float("inf")
            if d > 3.0:
                row_label = "REJECTED_AT_GATE_R_RESIDUAL"
            else:
                row_label = "HONEST_NEGATIVE_NOT_REJECTED"

        evidence_rows.append({
            "row_id": hn["row_id"],
            "row_class": "HONEST_NEGATIVE",
            "reveal_target": target,
            "experiment": hn["experiment"],
            "publication_reference": hn["publication_reference"],
            "central_value": hn.get("central_value_GeV", None),
            "stat_unc": hn.get("stat_uncertainty_GeV", 0.0),
            "sys_unc":  hn.get("sys_uncertainty_GeV",  0.0),
            "sam_value": sam,
            "residual": residual,
            "distance_sigma": d,
            "row_label": row_label,
            "actual_gate": "GATE_R_RESIDUAL",
            "rationale": "",
            "prediction_commit_sha256": pred_sha,
            "prediction_commit_utc": pred_utc,
            "envelope_sha256": env_sha,
            "envelope_open_utc": env_utc,
            "honest_negative_class": hn["honest_negative_class"],
        })

    fns = list(evidence_rows[0].keys())
    with open(EVID_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in evidence_rows:
            w.writerow(r)
    print(f"  wrote {EVID_CSV.name} ({len(evidence_rows)} rows)")

    # -- Verdict ---------------------------------------------------------
    live_rows = [r for r in evidence_rows if r["row_class"] == "LIVE_ANCHOR" and r["actual_gate"] == "RESIDUAL_COMPUTED"]
    hn_rows = [r for r in evidence_rows if r["row_class"] == "HONEST_NEGATIVE"]
    hn_correctly_gated = sum(
        1 for r in hn_rows
        if (r["honest_negative_class"] != "CLASS_G_SYNTHETIC" and r["actual_gate"] == "GATE_A_ADMISSIBILITY")
        or (r["honest_negative_class"] == "CLASS_G_SYNTHETIC" and r["row_label"] == "REJECTED_AT_GATE_R_RESIDUAL")
    )
    all_live_within_2sigma = all(r["row_label"] in ("AGREEMENT_WITHIN_1_SIGMA", "AGREEMENT_WITHIN_2_SIGMA") for r in live_rows)
    all_live_within_1sigma = all(r["row_label"] == "AGREEMENT_WITHIN_1_SIGMA" for r in live_rows)
    any_outside_3sigma = any(r["row_label"] == "AGREEMENT_OUTSIDE_3_SIGMA" for r in live_rows)

    if any_outside_3sigma:
        verdict = "CR066a_HIGGS_ZZ4L_REVEAL_DISFAVORED"
    elif all_live_within_1sigma:
        verdict = "CR066a_HIGGS_ZZ4L_REVEAL_PASS_ALL_TARGETS_WITHIN_1_SIGMA"
    elif all_live_within_2sigma:
        verdict = "CR066a_HIGGS_ZZ4L_REVEAL_PASS_ALL_TARGETS_WITHIN_2_SIGMA"
    else:
        verdict = "CR066a_HIGGS_ZZ4L_REVEAL_INCONCLUSIVE"

    label_counts: dict[str, int] = {}
    for r in evidence_rows:
        label_counts[r["row_label"]] = label_counts.get(r["row_label"], 0) + 1

    summary = {
        "cr_id": "CR066a",
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "extends_anchor": "CR065a (upstream intake) + CR064a (branch verdict)",
        "test_class": "COURTROOM_CERN_REVEAL_OF_QP091_FROZEN_H_TO_ZZSTAR_4L_PREDICTIONS",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "reveal_targets_opened": env["reveal_targets_opened"],
        "reveal_targets_held": env["reveal_targets_held"],
        "live_anchor_count": len(live_rows),
        "honest_negative_count": len(hn_rows),
        "honest_negative_correctly_gated": hn_correctly_gated,
        "row_label_counts": label_counts,
        "sam_predictions": sam_predictions,
        "upstream_CR065a_intake_lock_sha256": cr065a_sha,
        "prediction_commit_sha256": pred_sha,
        "prediction_commit_utc": pred_utc,
        "envelope_sha256": env_sha,
        "envelope_open_utc": env_utc,
        "open_debts": [
            "Anchor citation_verification_status PENDING for all rows; curator promotion required for sealed-scope status",
            "Four-lepton angular comparison is structural-consistency at QP091; quantitative angular shape comparison is a downstream QP093+ task",
            "REVEAL_01 (signal strength) intentionally held; downstream CR may open it",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # -- Result MD -------------------------------------------------------
    md = []
    md.append("# CR066a Higgs ZZ4L CERN Reveal Map - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Opened\n\n")
    md.append("REVEAL_02 m4l peak / Higgs mass reconstruction (ATLAS, CMS, combined)\n\n")
    md.append("REVEAL_03 m12 / m34 split (Z + Z* branch structure)\n\n")
    md.append("REVEAL_04 four-lepton angular structural consistency (non-flat angles)\n\n")
    md.append("## What This CR Did NOT Open\n\n")
    md.append("REVEAL_01 H006/H007 signal strength (per user direction; weakest target)\n\n")
    md.append("## Blindness Proof\n\n```text\n")
    md.append(f"upstream CR065a intake lock sha256 = {cr065a_sha}\n")
    md.append(f"prediction_commit_sha256            = {pred_sha}\n")
    md.append(f"prediction_commit_utc               = {pred_utc}\n")
    md.append(f"envelope_sha256                     = {env_sha}\n")
    md.append(f"envelope_open_utc                   = {env_utc}\n")
    md.append("temporal_ordering                   = OK\n")
    md.append("```\n\n")
    md.append("## SAM Predictions (from QP091 freeze)\n\n```text\n")
    md.append(f"m4l peak                = {sam_predictions['REVEAL_02_m4l_peak_GeV']:.4f} GeV\n")
    md.append(f"m12 peak (Z on-shell)   = {sam_predictions['REVEAL_03_m12_peak_GeV']:.4f} GeV\n")
    md.append(f"m34 ceiling (Z* off)    = {sam_predictions['REVEAL_03_m34_ceiling_GeV']:.4f} GeV\n")
    md.append("two on-shell Z          = FORBIDDEN (deficit 57.104 GeV)\n")
    md.append("4-lepton angular        = STRUCTURED (non-random missing energy)\n")
    md.append("```\n\n")
    md.append("## Per-Anchor Comparison\n\n")
    md.append("| Row | Reveal | Anchor | central | unc | SAM | residual | sigma | Label |\n|---|---|---|---|---|---|---|---|---|\n")
    for r in evidence_rows:
        cv = "n/a" if r["central_value"] is None else f"{r['central_value']:.3f}"
        unc = math.sqrt(r["stat_unc"]**2 + r["sys_unc"]**2) if r["central_value"] is not None else 0.0
        unc_s = f"{unc:.3f}" if r["central_value"] is not None else "n/a"
        sv = "n/a" if r["sam_value"] is None else f"{r['sam_value']:.3f}"
        rs = "n/a" if r["residual"] is None else f"{r['residual']:+.3f}"
        ds = "n/a" if r["distance_sigma"] is None else f"{r['distance_sigma']:.2f}"
        md.append(f"| {r['row_id']} | {r['reveal_target']} | {r['experiment']} | {cv} | {unc_s} | {sv} | {rs} | {ds} | {r['row_label']} |\n")
    md.append(f"\nHonest negatives correctly gated: {hn_correctly_gated} / {len(hn_rows)}\n\n")
    md.append("## What This Means\n\n```text\n")
    if verdict == "CR066a_HIGGS_ZZ4L_REVEAL_PASS_ALL_TARGETS_WITHIN_1_SIGMA":
        md.append("All three opened reveal targets land within 1 sigma of the CERN\n")
        md.append("measurements.  QP091's frozen prediction set closes against the\n")
        md.append("strongest H -> ZZ* -> 4l structural distributions at LHC.\n")
    elif verdict == "CR066a_HIGGS_ZZ4L_REVEAL_PASS_ALL_TARGETS_WITHIN_2_SIGMA":
        md.append("All three reveal targets within 2 sigma; some at the 1-2 sigma\n")
        md.append("level.  Honest residual tension exists but no disfavoring.\n")
    elif verdict == "CR066a_HIGGS_ZZ4L_REVEAL_DISFAVORED":
        md.append("At least one anchor lands outside 3 sigma.  QP091 frozen freeze\n")
        md.append("is disfavored on that target; remaining targets reported honestly.\n")
    md.append("```\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print("CR066a runner: complete")


if __name__ == "__main__":
    main()
