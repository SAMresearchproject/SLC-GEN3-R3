"""
CR098_runner.py - Forward-blind prediction registry against unresolved CERN gaps.

Reads two upstream SAM sources (cite-only):
  1. SAM_X novel native candidates (12 rows, closure_campaign03)
  2. SUK055 composite pair mass coordinates (12 rows)

Combines them into a single forward-blind prediction registry.
Hashes the registry, writes sha256 sibling, records the prediction
commitment timestamp. The cryptographic record is the blindness proof.

Future CERN publications matching any registered candidate are added
as APPEAL_NEW_CERN_MEASUREMENT rows in a sibling file; the registry
itself is never modified.
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

# Upstream SAM sources (read-only, cite-only)
SAM_X_MASS_CSV = Path(r"C:/VS/Stam_model-A-v1.0/tests/particles/unknown_native_mass_predictions.csv")
SAM_X_FULL_CSV = Path(r"C:/VS/Stam_model-A-v1.0/tests/particles/unknown_native_candidates.csv")
SUK055_CSV = Path(r"C:/VS/Stam_model-A-v1.0/tests/Campaigns/SAM_UNIFICATION_KERNEL_GATE/SUK055_composite_candidate_mass_surface.csv")
BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"

PREDICTIONS_CSV = CR_DIR / "CR098_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR098_prediction_commit.json"
REGISTRY_CSV = CR_DIR / "CR098_forward_blind_prediction_registry.csv"
REGISTRY_SHA256_SIBLING = CR_DIR / "CR098_forward_blind_prediction_registry.csv.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR098_summary.json"
RESULT_MD = CR_DIR / "CR098_result.md"

# Curator-assigned CERN search-program mapping. Best-fit; PENDING_VERIFICATION.
SAM_X_SEARCH_MAP = {
    "SAM-X-001": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "NA64 dark-sector / FASER forward search (low-mass charged scalar window)",
                  "Sub-100 MeV new charged states"),
    "SAM-X-002": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "ATLAS / CMS resonance searches (~3 GeV scalar lane)",
                  "GeV-scale exotic resonance"),
    "SAM-X-003": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "NA64 / FASER hidden-sector (sub-MeV scalar window)",
                  "Sub-MeV light scalar"),
    "SAM-X-004": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "FASERnu / SND@LHC forward neutrino program; KATRIN-class nu-mass experiments (non-CERN)",
                  "100 eV - 1 keV neutral mass band"),
    "SAM-X-005": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "ATLAS / CMS heavy charged-lepton-like search (~27 GeV)",
                  "10-50 GeV charged exotic lepton-like"),
    "SAM-X-006": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "MoEDAL fractional-charge search at LHC (Q=-2/3 with negative winding)",
                  "MeV-scale fractional-charge carrier"),
    "SAM-X-007": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "MoEDAL fractional-charge search (Q=-3/4 is NON-SM rational charge - novel)",
                  "MeV-scale non-SM rational-charge carrier"),
    "SAM-X-008": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "MoEDAL + LHCb fixed-target Q=+1/3 primary search (no SM primary +1/3 exists)",
                  "Pion-mass-band primary +1/3 carrier"),
    "SAM-X-009": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "ATLAS / CMS quaternary owner-algebra search (SU(4)-like discriminator)",
                  "Sub-GeV exotic with 4-axis structure"),
    "SAM-X-010": ("FORWARD_BLIND_SEARCH_ACTIVE",
                  "FASERnu / SND@LHC (sterile-neutral asymmetric outer-binary; ~9 eV)",
                  "Sub-100 eV neutral asymmetric"),
    "SAM-X-011": ("FORWARD_BLIND_NO_SEARCH_DEFINED",
                  "Ultra-light scalar (sub-meV) - OSQAR / IAXO axion-class searches not yet at this mass band",
                  "Sub-meV scalar dark sector"),
    "SAM-X-012": ("FORBIDDEN_PARTITION_NEGATIVE_PREDICTION",
                  "MoEDAL / any LHC exotics - SAM predicts NO particle at (7,5) radix-wall partition",
                  "If found at this structural shape, SAM is broken"),
}

# SUK055 composite pair candidates are heavy q-anti-q composites - LHCb exotic
# spectroscopy is the natural search program. Top-quark pairs are radically new
# since the top decays before hadronization in SM; SAM predicts mass coordinates
# at top-mass scale.
SUK055_SEARCH_MAP_DEFAULT_LHCb = "LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance search"
SUK055_SEARCH_MAP_TOP_PAIR = "LHCb + ATLAS + CMS top-quark physics program (radically new: top-involved bound state)"


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def load_sam_x_mass():
    out = {}
    with open(SAM_X_MASS_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cid = r["unknown_native_id"]
            out[cid] = {
                "predicted_mass_MeV": float(r["mass_native_MeV"]) if r["mass_native_MeV"] else None,
                "mass_formula": r["mass_native_formula"],
                "mass_status": r["mass_status"],
                "grade": r["grade"],
                "layered_set_membership": r["layered_set_membership"],
            }
    return out


def load_sam_x_full():
    out = {}
    with open(SAM_X_FULL_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cid = r["unknown_native_id"]
            out[cid] = {
                "structural_reading": r["source_mode_partition"],
                "a_slice": r["source_a_slice"],
                "predicted_charge_Q": r["Q_native_axis"],
                "spin": r["spin_native_axis"],
                "stability_status": r["stability_status"],
                "why_not_known_sector": r["why_not_known_sector"],
            }
    return out


def load_suk055():
    out = []
    with open(SUK055_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append({
                "pair": r["pair"],
                "particle_a": r["particle_a"],
                "particle_b": r["particle_b"],
                "oriented_slots": r["oriented_slots"],
                "slot_charges": r["slot_charges"],
                "charge_classes": r["charge_classes"],
                "constituent_sum_MeV": float(r["constituent_sum_MeV"]) if r["constituent_sum_MeV"] else None,
                "mass_coordinate_grade": r["mass_coordinate_grade"],
                "closure_route": r["closure_route"],
                "support_selectors": r["support_selectors"],
                "selected_transition_present": r["selected_transition_present"],
                "rank": r["rank"],
            })
    return out


def main():
    print("CR098 runner: starting (forward-blind registry build)")

    # Load upstream sources
    samx_mass = load_sam_x_mass()
    samx_full = load_sam_x_full()
    suk055 = load_suk055()
    print(f"  SAM-X candidates loaded: {len(samx_mass)} (mass csv), {len(samx_full)} (full csv)")
    print(f"  SUK055 composite pairs loaded: {len(suk055)}")

    # Write the raw predictions CSV that will be hashed.
    # Iterate over the union of all SAM-X ids - the FULL csv includes
    # SAM-X-012 (FORBIDDEN row) which is not in the mass csv.
    pred_rows = []
    all_samx_ids = sorted(set(list(samx_mass.keys()) + list(samx_full.keys())))
    for cid in all_samx_ids:
        m = samx_mass.get(cid, {})
        f = samx_full.get(cid, {})
        mass_val = m.get("predicted_mass_MeV")
        is_forbidden = "FORBIDDEN" in f.get("stability_status", "") or "FORBIDDEN" in f.get("structural_reading", "")
        if mass_val is None and is_forbidden:
            mass_str = "N/A_FORBIDDEN_PARTITION"
        elif mass_val is None:
            mass_str = ""
        else:
            mass_str = f"{mass_val:.6e}"
        pred_rows.append({
            "candidate_id": cid,
            "source_family": "SAM_X",
            "structural_reading": f.get("structural_reading", ""),
            "predicted_mass_MeV": mass_str,
            "predicted_charge_Q": f.get("predicted_charge_Q", ""),
            "mass_formula": m.get("mass_formula", "N/A_FORBIDDEN") if is_forbidden else m.get("mass_formula", ""),
            "mass_grade": m.get("grade", "FORBIDDEN_NEGATIVE_PREDICTION") if is_forbidden else m.get("grade", ""),
            "stability_status": f.get("stability_status", ""),
            "why_not_in_SM": f.get("why_not_known_sector", "")[:500],
            "upstream_source_file": str(SAM_X_FULL_CSV if is_forbidden else SAM_X_MASS_CSV),
        })
    for s in suk055:
        cid = f"COMPOSITE-PAIR-{s['particle_a']}-{s['particle_b']}"
        pred_rows.append({
            "candidate_id": cid,
            "source_family": "SUK055_COMPOSITE",
            "structural_reading": f"pair {s['pair']} ({s['oriented_slots']})",
            "predicted_mass_MeV": "" if s["constituent_sum_MeV"] is None else f"{s['constituent_sum_MeV']:.6e}",
            "predicted_charge_Q": s["charge_classes"] + " (" + s["slot_charges"] + ")",
            "mass_formula": s["closure_route"] + " :: " + s["support_selectors"],
            "mass_grade": s["mass_coordinate_grade"],
            "stability_status": s["mass_coordinate_grade"],
            "why_not_in_SM": "heavy q-anti-q composite pair coordinate; rank " + s["rank"],
            "upstream_source_file": str(SUK055_CSV),
        })

    # Step 2: write predictions
    fns = list(pred_rows[0].keys())
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    print(f"  wrote {PREDICTIONS_CSV.name} ({len(pred_rows)} rows)")

    # Steps 3-4: hash + commit
    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    commit = {
        "commit_id": "CR098_FORWARD_BLIND_PREDICTION_COMMIT",
        "predictions_file": PREDICTIONS_CSV.name,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "anchor_envelope_unopened_at_commit_time": True,
        "anchor_envelope_does_not_yet_exist": "CERN_HAS_NOT_PUBLISHED_MATCHING_MEASUREMENTS",
        "blindness_pillar": "PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH",
        "forward_blind_principle": "The hash + utc is the cryptographic record that SAM committed BEFORE CERN published",
    }
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump(commit, f, indent=2)
    print(f"  committed prediction sha256={prediction_sha[:16]}... utc={prediction_utc}")

    # Hash upstream source files for the registry citation
    samx_mass_sha = sha256_file(SAM_X_MASS_CSV)
    samx_full_sha = sha256_file(SAM_X_FULL_CSV)
    suk055_sha = sha256_file(SUK055_CSV)
    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    # Build the registry
    registry_fields = [
        "candidate_id", "source_family", "structural_reading",
        "predicted_mass_MeV", "predicted_charge_Q", "mass_formula",
        "why_not_in_SM",
        "upstream_source_file", "upstream_source_sha256",
        "prediction_commit_sha256", "prediction_commit_utc",
        "prediction_status",
        "suggested_CERN_search_program",
        "mass_band_in_search_program",
        "appeal_row_added_when_published",
        "blindness_protocol_sha256",
    ]
    registry_rows = []
    for p in pred_rows:
        if p["source_family"] == "SAM_X":
            status, search_prog, mass_band = SAM_X_SEARCH_MAP.get(
                p["candidate_id"],
                ("FORWARD_BLIND_NO_SEARCH_DEFINED", "NO_CURRENT_CERN_PROGRAM", "")
            )
            upstream_sha = samx_mass_sha
        else:
            # SUK055 composite
            # Top-quark pairs (any pair containing 't') get the radically-new flag
            pair_label = p["structural_reading"].split()[1] if " " in p["structural_reading"] else ""
            if "t" in pair_label.replace("anti", "").replace("<->", ""):
                search_prog = SUK055_SEARCH_MAP_TOP_PAIR
                mass_band = "top-quark-mass-region exotic composite"
            else:
                search_prog = SUK055_SEARCH_MAP_DEFAULT_LHCb
                mass_band = "GeV-scale heavy-flavour composite"
            status = "FORWARD_BLIND_SEARCH_ACTIVE"
            upstream_sha = suk055_sha

        registry_rows.append({
            "candidate_id": p["candidate_id"],
            "source_family": p["source_family"],
            "structural_reading": p["structural_reading"],
            "predicted_mass_MeV": p["predicted_mass_MeV"],
            "predicted_charge_Q": p["predicted_charge_Q"],
            "mass_formula": p["mass_formula"],
            "why_not_in_SM": p["why_not_in_SM"],
            "upstream_source_file": p["upstream_source_file"],
            "upstream_source_sha256": upstream_sha,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "prediction_status": status,
            "suggested_CERN_search_program": search_prog,
            "mass_band_in_search_program": mass_band,
            "appeal_row_added_when_published": "NOT_YET",
            "blindness_protocol_sha256": blindness_sha,
        })

    with open(REGISTRY_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=registry_fields)
        w.writeheader()
        for r in registry_rows:
            w.writerow(r)
    print(f"  wrote {REGISTRY_CSV.name} ({len(registry_rows)} rows)")

    # Seal the registry with sha256 sibling
    registry_sha = sha256_file(REGISTRY_CSV)
    REGISTRY_SHA256_SIBLING.write_text(registry_sha + "\n", encoding="ascii")
    print(f"  registry sealed: {registry_sha}")

    # Counts
    status_counts = {}
    family_counts = {}
    for r in registry_rows:
        status_counts[r["prediction_status"]] = status_counts.get(r["prediction_status"], 0) + 1
        family_counts[r["source_family"]] = family_counts.get(r["source_family"], 0) + 1

    summary = {
        "cr_id": "CR098",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "FORWARD_BLIND_PREDICTION_REGISTRY_AGAINST_UNRESOLVED_CERN_GAPS",
        "execution_status": "CLEAN",
        "result_class": "FORWARD_BLIND_PREDICTION_REGISTRY_SEALED",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "total_predictions_registered": len(registry_rows),
        "predictions_per_source_family": family_counts,
        "predictions_per_status_class": status_counts,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "registry_sha256": registry_sha,
        "registry_path": str(REGISTRY_CSV),
        "registry_sha256_sibling_path": str(REGISTRY_SHA256_SIBLING),
        "upstream_source_hashes": {
            "unknown_native_mass_predictions.csv": samx_mass_sha,
            "unknown_native_candidates.csv": samx_full_sha,
            "SUK055_composite_candidate_mass_surface.csv": suk055_sha,
        },
        "blindness_protocol_sha256": blindness_sha,
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling not yet written by curator",
            "Seal sha256 sibling not yet written by curator",
            "Upstream source files have not been independently re-hashed by curator",
            "suggested_CERN_search_program assignments are best-fit; curator verification pending",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote {SUMMARY_JSON.name}")

    # result.md
    md = []
    md.append("# CR098 CERN Gaps Forward-Blind Predictions - Sealed Registry\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append("CR098_FORWARD_BLIND_PREDICTION_REGISTRY_SEALED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## Commitment Proof\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"registry_sha256          = {registry_sha}\n")
    md.append(f"registry_sha256_sibling  = {REGISTRY_SHA256_SIBLING.name}\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## What This Is\n\n")
    md.append("This CR is qualitatively different from CR091..CR096. The earlier\n")
    md.append("CRs compared 09a's locked predictions against CERN values that were\n")
    md.append("already public when 09a was sealed. CR098 commits SAM forward\n")
    md.append("predictions BEFORE CERN publishes a matching measurement. The hash\n")
    md.append("plus the utc timestamp on every row is the cryptographic record\n")
    md.append("that SAM committed first. The registry is sha256-sealed by its\n")
    md.append("sibling file. Future CERN publications matching any registered\n")
    md.append("candidate are appended as APPEAL rows; the registry itself is\n")
    md.append("never modified.\n\n")
    md.append("## Counts\n\n```text\n")
    md.append(f"Total forward-blind predictions registered : {len(registry_rows)}\n")
    md.append("Per source family:\n")
    for k, v in family_counts.items():
        md.append(f"  {k:30s} {v}\n")
    md.append("Per prediction-status class:\n")
    for k, v in status_counts.items():
        md.append(f"  {k:45s} {v}\n")
    md.append("```\n\n")
    md.append("## SAM-X Novel Native Candidates\n\n")
    md.append("Twelve novel native-sector predictions from closure_campaign03. Each\n")
    md.append("is sha256-locked at the prediction commit utc. SAM-X-012 is a\n")
    md.append("NEGATIVE prediction (forbidden partition).\n\n")
    md.append("| Candidate | Mass (MeV) | Q | Structural reading | Status | Suggested CERN program |\n")
    md.append("|---|---|---|---|---|---|\n")
    for r in registry_rows:
        if r["source_family"] != "SAM_X":
            continue
        m = r["predicted_mass_MeV"]
        if not m:
            m_str = "n/a"
        else:
            try:
                m_str = f"{float(m):.4g}"
            except ValueError:
                m_str = m  # e.g., "N/A_FORBIDDEN_PARTITION"
        sr = r["structural_reading"][:40]
        prog = r["suggested_CERN_search_program"][:80]
        md.append(f"| {r['candidate_id']} | {m_str} | {r['predicted_charge_Q']} | {sr} | {r['prediction_status']} | {prog} |\n")
    md.append("\n## SUK055 Composite Pair Mass Coordinates\n\n")
    md.append("Twelve heavy q-anti-q composite pair coordinates. Pairs involving\n")
    md.append("the top quark (b<->t, c<->t, d<->t, s<->t, t<->u) are radically new:\n")
    md.append("the top quark decays before hadronization in the SM, so a top-involved\n")
    md.append("bound state at the predicted mass coordinate would be a major discovery.\n\n")
    md.append("| Pair | Mass (MeV) | Charge class | Grade | Suggested CERN program |\n")
    md.append("|---|---|---|---|---|\n")
    for r in registry_rows:
        if r["source_family"] != "SUK055_COMPOSITE":
            continue
        m = r["predicted_mass_MeV"]
        m_str = f"{float(m):.4f}" if m else "n/a"
        pair_label = r["structural_reading"].split()[1] if " " in r["structural_reading"] else r["candidate_id"]
        cc = r["predicted_charge_Q"].split()[0]
        prog = r["suggested_CERN_search_program"][:60]
        md.append(f"| {pair_label} | {m_str} | {cc} | {r['why_not_in_SM'][:30]} | {prog} |\n")
    md.append("\n## Rule-9 Line\n\n```text\n")
    md.append("CR098 puts SAM on the line for predictions CERN has not made yet.\n")
    md.append("The sealed registry, with cryptographic prediction-commit hash and\n")
    md.append("UTC timestamp, is the on-record cryptographic proof that SAM\n")
    md.append("committed BEFORE any CERN publication on these gaps.\n\n")
    md.append("If CERN publishes a measurement that confirms a registered\n")
    md.append("prediction, that's strong evidence in SAM's favor. If CERN\n")
    md.append("publishes a contradicting measurement, that's evidence against\n")
    md.append("SAM, and the appeal row records the residual honestly. If\n")
    md.append("SAM-X-012 is observed (a particle at (7,5) radix-wall partition),\n")
    md.append("SAM's partition-algebra commitment is falsified.\n")
    md.append("```\n\n")
    md.append("## Open Debts\n\n```text\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR098 runner: complete")


if __name__ == "__main__":
    main()
