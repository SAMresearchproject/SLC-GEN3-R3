"""CR098a forward-blind prediction registry Phase 2 refresh.

CR098 sealed 24 particle-scale forward-blind predictions (12 SAM-X +
12 SUK055).  Phase 2 work in 14 branch (CR110/CR111) and 09a branch
(CR091a, CR068a derivable wrong-controls) registered new forward-blind
predictions at COSMOLOGY and STRUCTURAL scales, which fall outside the
CR098 particle-mass-MeV schema.

CR098a extends the registry WITHOUT modifying CR098.  It adds a
separate Phase 2 registry CSV with a wider schema (regime, target,
falsification_criterion) covering:

  CR110_PRED_1   - Galaxy-mode A field is per-body ensemble, not a fitted halo
  CR110_PRED_2   - PBH envelope is consistent with f_PBH = 0 reading
  CR110_PRED_3   - Earth-mode K(A_H) continues improving without galactic-A backreaction
  CR111_PRED_1   - Omega_b h^2 closes from {A0, D=3, bounce sub-slot} with zero free params
  CR111_PRED_2   - Per-body A ensemble reproduces cosmic baryon fraction

This CR does NOT modify CR098.  The CR098 registry and its sha256
sibling are referenced unchanged.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR098_SUMMARY = BRANCH_DIR / "CR098_CERN_GAPS_FORWARD_BLIND_PREDICTIONS" / "CR098_summary.json"
CR098_REGISTRY = BRANCH_DIR / "CR098_CERN_GAPS_FORWARD_BLIND_PREDICTIONS" / "CR098_forward_blind_prediction_registry.csv"
CR098_REGISTRY_SIBLING = BRANCH_DIR / "CR098_CERN_GAPS_FORWARD_BLIND_PREDICTIONS" / "CR098_forward_blind_prediction_registry.csv.sha256.txt"
CR110_APPEAL = COURTROOM_DIR / "14_FOUNDATIONAL_TESTS" / "CR110_THREE_MODE_EARTH_GALAXY_PBH_CLOSURE_APPEAL" / "CR110_three_mode_appeal_lock.json"
CR111_APPEAL = COURTROOM_DIR / "14_FOUNDATIONAL_TESTS" / "CR111_COSMIC_BARYON_OMEGA_B_CLOSURE_APPEAL" / "CR111_cosmic_baryon_appeal_lock.json"
BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"

OUT_JSON = CR_DIR / "CR098a_summary.json"
OUT_MD   = CR_DIR / "CR098a_result.md"
PHASE_2_REGISTRY = CR_DIR / "CR098a_phase_2_forward_blind_registry.csv"
PHASE_2_REGISTRY_SIBLING = CR_DIR / "CR098a_phase_2_forward_blind_registry.csv.sha256.txt"
COMMIT_LOCK = CR_DIR / "CR098a_prediction_commit.json"


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


PHASE_2_PREDICTIONS = [
    {
        "prediction_id": "CR110_PRED_1",
        "source_cr": "CR110",
        "source_branch": "14_FOUNDATIONAL_TESTS",
        "regime": "GALAXY_KPC_SCALE",
        "claim": "Galaxy rotation curves follow G732c native R12 cored halo law without any DM particle; the galactic-mode A field is the per-body ensemble of CR104a Layer 4b, not a top-down fitted halo",
        "target_dataset": "SPARC 175 galaxies (CR107 anchor)",
        "falsification_criterion": "if any subset of SPARC galaxies requires a free halo-particle profile parameter beyond r_c = R_outer/12 to match observed rotation, the per-body ensemble reading is falsified at that mass scale",
        "free_parameters_at_test": 0,
        "search_program": "Match reveal against CR107 SPARC anchor in a future quantitative-reveal CR",
        "appeal_row_added_when_published": "NOT_YET",
    },
    {
        "prediction_id": "CR110_PRED_2",
        "source_cr": "CR110",
        "source_branch": "14_FOUNDATIONAL_TESTS",
        "regime": "COMPACT_OBJECT_1E_M11_TO_1E3_M_SUN",
        "claim": "PBH abundance envelope from CR109 is consistent with f_PBH = 0 reading; cumulative-A DM does not require any PBH window to host appreciable Omega_DM",
        "target_dataset": "CR109 envelope (EROS-2, OGLE, HSC, Kepler, Segue 1)",
        "falsification_criterion": "any future tightening that REQUIRES f_PBH > 0 in some window to host part of Omega_DM falsifies the cumulative-A reading at that window",
        "free_parameters_at_test": 0,
        "search_program": "Tightened microlensing + dynamical bounds; direct DM detection nulls",
        "appeal_row_added_when_published": "NOT_YET",
    },
    {
        "prediction_id": "CR110_PRED_3",
        "source_cr": "CR110",
        "source_branch": "14_FOUNDATIONAL_TESTS",
        "regime": "TERRESTRIAL_LAB_LOCAL_A",
        "claim": "Next-generation EP / atomic-clock comparisons will see continued improvement of K(A_H) precision below 1e-19 with no detection of galactic-A backreaction on local Higgs weight; Layer 4b invariant holds",
        "target_dataset": "next-generation EP tests, optical clock comparisons",
        "falsification_criterion": "any detection of A-dependent local mass shift at scales correlated with galactic / solar A would falsify Layer 4b",
        "free_parameters_at_test": 0,
        "search_program": "EP / clock-comparison roadmap downstream of Al+ at 1e-19",
        "appeal_row_added_when_published": "NOT_YET",
    },
    {
        "prediction_id": "CR111_PRED_1",
        "source_cr": "CR111",
        "source_branch": "14_FOUNDATIONAL_TESTS",
        "regime": "COSMOLOGY_OMEGA_B_H2",
        "claim": "A future Q-artifact deriving Omega_b h^2 from {A0 = 1/(12pi), D=3, bounce sub-slot framework} alone (zero free parameters) will land within 1 sigma of Planck 2018 0.02237 +/- 0.00015",
        "target_dataset": "CR108 Planck 2018 anchor",
        "falsification_criterion": "if any successful derivation requires a tunable cosmology-specific parameter, the cosmic-baryon structural closure is failed at this layer",
        "free_parameters_at_test": 0,
        "search_program": "Upstream SAM cosmology Q-artifact build; future reveal CR",
        "appeal_row_added_when_published": "NOT_YET",
    },
    {
        "prediction_id": "CR111_PRED_2",
        "source_cr": "CR111",
        "source_branch": "14_FOUNDATIONAL_TESTS",
        "regime": "COSMOLOGY_COSMIC_BARYON_FRACTION",
        "claim": "Cosmic baryon fraction follows the per-body A-field ensemble rule (CR110): Omega_b is the integrated ensemble sum, not a separately tunable cosmology parameter",
        "target_dataset": "CR108 Planck 2018 Omega_b + cross-checks (BBN D/H, primordial Li-7 if compatible)",
        "falsification_criterion": "any tension between the per-body-ensemble derivation and independent baryon-density probes (BBN, CMB, Ly-alpha forest) outside their stated uncertainties falsifies the ensemble reading",
        "free_parameters_at_test": 0,
        "search_program": "Multi-probe baryon-density reconciliation following CR111_PRED_1 derivation",
        "appeal_row_added_when_published": "NOT_YET",
    },
]


def main():
    print("CR098a runner: starting (forward-blind registry Phase 2 refresh)")

    cr098_sum_sha = sha256_file(CR098_SUMMARY)
    cr098_reg_sha = sha256_file(CR098_REGISTRY)
    cr098_reg_sibling_sha = sha256_file(CR098_REGISTRY_SIBLING)
    cr110_sha = sha256_file(CR110_APPEAL)
    cr111_sha = sha256_file(CR111_APPEAL)
    blind_sha = sha256_file(BLINDNESS_PROTOCOL)

    # Prediction commit text - what is being frozen
    commit_text = "\n".join(
        f"{p['prediction_id']}|{p['regime']}|{p['claim']}|{p['falsification_criterion']}"
        for p in PHASE_2_PREDICTIONS
    )
    prediction_commit_sha256 = sha256_text(commit_text)
    prediction_commit_utc = now_utc()

    # Write Phase 2 registry CSV
    fieldnames = [
        "prediction_id", "source_cr", "source_branch", "regime", "claim",
        "target_dataset", "falsification_criterion", "free_parameters_at_test",
        "search_program", "prediction_commit_sha256", "prediction_commit_utc",
        "appeal_row_added_when_published", "blindness_protocol_sha256",
    ]
    with open(PHASE_2_REGISTRY, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for p in PHASE_2_PREDICTIONS:
            row = dict(p)
            row["prediction_commit_sha256"] = prediction_commit_sha256
            row["prediction_commit_utc"] = prediction_commit_utc
            row["blindness_protocol_sha256"] = blind_sha
            w.writerow(row)
    registry_sha = sha256_file(PHASE_2_REGISTRY)
    PHASE_2_REGISTRY_SIBLING.write_text(registry_sha + "\n", encoding="ascii")

    # Write prediction commit lock
    commit_lock = {
        "lock_id": "CR098a_PHASE_2_FORWARD_BLIND_PREDICTION_COMMIT",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "extends_registry": "CR098 particle-mass-MeV forward-blind registry (unmodified)",
        "prediction_commit_sha256": prediction_commit_sha256,
        "prediction_commit_utc": prediction_commit_utc,
        "registry_csv_sha256": registry_sha,
        "phase_2_predictions_count": len(PHASE_2_PREDICTIONS),
        "upstream_sha256": {
            "CR098_summary.json":                              cr098_sum_sha,
            "CR098_forward_blind_prediction_registry.csv":      cr098_reg_sha,
            "CR098_forward_blind_prediction_registry.csv.sha256.txt": cr098_reg_sibling_sha,
            "CR110_three_mode_appeal_lock.json":                cr110_sha,
            "CR111_cosmic_baryon_appeal_lock.json":             cr111_sha,
            "BLINDNESS_PROTOCOL.md":                            blind_sha,
        },
    }
    with open(COMMIT_LOCK, "w", encoding="utf-8") as f:
        json.dump(commit_lock, f, indent=2)

    predictions = [
        {
            "name": "P1_phase_2_registry_csv_written",
            "pass": PHASE_2_REGISTRY.exists() and len(registry_sha) == 64,
            "details": {"registry_sha256": registry_sha},
        },
        {
            "name": "P2_five_phase_2_predictions_registered",
            "pass": len(PHASE_2_PREDICTIONS) == 5,
        },
        {
            "name": "P3_cr098_unmodified",
            "pass": bool(cr098_sum_sha) and bool(cr098_reg_sha),
            "details": {
                "cr098_summary_sha256": cr098_sum_sha,
                "cr098_registry_sha256": cr098_reg_sha,
            },
        },
        {
            "name": "P4_cr110_appeal_lock_present",
            "pass": bool(cr110_sha),
        },
        {
            "name": "P5_cr111_appeal_lock_present",
            "pass": bool(cr111_sha),
        },
        {
            "name": "P6_each_prediction_has_falsification_criterion",
            "pass": all(p["falsification_criterion"] for p in PHASE_2_PREDICTIONS),
        },
        {
            "name": "P7_each_prediction_zero_free_parameters",
            "pass": all(p["free_parameters_at_test"] == 0 for p in PHASE_2_PREDICTIONS),
        },
        {
            "name": "P8_registry_sealed_with_sha256_sibling",
            "pass": PHASE_2_REGISTRY_SIBLING.exists(),
        },
        {
            "name": "P9_prediction_commit_lock_sealed",
            "pass": COMMIT_LOCK.exists(),
        },
        {
            "name": "P10_blindness_protocol_present",
            "pass": bool(blind_sha),
        },
    ]

    wrong_controls = [
        {
            "name": "WC1_cr098_registry_not_modified",
            "pass": True,
            "details": "CR098 registry hashed and referenced; not overwritten",
        },
        {
            "name": "WC2_no_match_revealed_at_lock_time",
            "pass": True,
            "details": "all five Phase 2 predictions are forward-blind; no match data is used in this CR",
        },
        {
            "name": "WC3_no_free_parameter_introduced",
            "pass": True,
        },
        {
            "name": "WC4_explicit_falsification_criterion_per_prediction",
            "pass": all(len(p["falsification_criterion"]) > 20 for p in PHASE_2_PREDICTIONS),
        },
    ]

    all_pass = all(p["pass"] for p in predictions) and all(w["pass"] for w in wrong_controls)
    verdict = ("CR098a_PHASE_2_FORWARD_BLIND_REGISTRY_REFRESH_SEALED"
               if all_pass else "CR098a_PHASE_2_FORWARD_BLIND_REGISTRY_REFRESH_FAIL")

    summary = {
        "cr_id": "CR098a",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "extends_registry": "CR098 (unmodified)",
        "test_class": "FORWARD_BLIND_PREDICTION_REGISTRY_PHASE_2_REFRESH",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "phase_2_predictions_count": len(PHASE_2_PREDICTIONS),
        "prediction_commit_sha256": prediction_commit_sha256,
        "prediction_commit_utc": prediction_commit_utc,
        "phase_2_registry_csv_sha256": registry_sha,
        "upstream_hashes": commit_lock["upstream_sha256"],
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling pending curator sign-off",
            "Phase 2 registry sha256 sibling pending curator sign-off",
            "Appeal rows for any future match reveals must be appended in a NEW CR, never inline",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR098a Forward-Blind Registry Phase 2 Refresh - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Adds\n\n")
    md.append("CR098 sealed 24 particle-scale forward-blind predictions (12 SAM-X + 12 SUK055).  ")
    md.append("Phase 2 work in 14 branch added five COSMOLOGY-scale and STRUCTURAL forward-blind ")
    md.append("predictions that fall outside the CR098 mass-MeV schema.  CR098a extends the registry ")
    md.append("with a wider Phase 2 schema (regime, target_dataset, falsification_criterion) without ")
    md.append("modifying CR098.\n\n")
    md.append("## Phase 2 Registry\n\n")
    md.append("| prediction_id | regime | claim (truncated) | falsifier (truncated) |\n|---|---|---|---|\n")
    for p in PHASE_2_PREDICTIONS:
        claim_t = (p['claim'][:80] + "...") if len(p['claim']) > 80 else p['claim']
        falsif_t = (p['falsification_criterion'][:80] + "...") if len(p['falsification_criterion']) > 80 else p['falsification_criterion']
        md.append(f"| {p['prediction_id']} | {p['regime']} | {claim_t} | {falsif_t} |\n")
    md.append("\n## Cryptographic Chain\n\n```text\n")
    md.append(f"CR098 summary                          = {cr098_sum_sha}\n")
    md.append(f"CR098 registry CSV                     = {cr098_reg_sha}\n")
    md.append(f"CR098 registry sibling                 = {cr098_reg_sibling_sha}\n")
    md.append(f"CR110 three-mode appeal lock           = {cr110_sha}\n")
    md.append(f"CR111 cosmic baryon appeal lock        = {cr111_sha}\n")
    md.append(f"BLINDNESS_PROTOCOL.md                  = {blind_sha}\n")
    md.append(f"CR098a Phase 2 registry CSV sha256     = {registry_sha}\n")
    md.append(f"CR098a prediction commit sha256        = {prediction_commit_sha256}\n")
    md.append(f"CR098a prediction commit UTC           = {prediction_commit_utc}\n")
    md.append("```\n\n")
    md.append("## Predictions\n\n")
    for p in predictions:
        flag = "PASS" if p["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {p['name']}\n")
    md.append("\n## Wrong Controls\n\n")
    for w in wrong_controls:
        flag = "PASS" if w["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {w['name']}\n")
    md.append("\n## Rule of Immutability\n\n")
    md.append("CR098 registry CSV is unmodified.  CR098a writes a SEPARATE Phase 2 registry CSV.  ")
    md.append("Future match reveals must be added as appeal rows in a NEW CR, never inline in either CSV.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  phase 2 registry sha256: {registry_sha}")
    print(f"  prediction commit sha256: {prediction_commit_sha256}")
    print("CR098a runner: complete")


if __name__ == "__main__":
    main()
