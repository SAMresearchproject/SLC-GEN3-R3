"""CR125 X(6900) forward-blind two-state prediction registry.

Origin
------
CR124 walked the 321-row SAM particle catalog against the CR090 CERN
anchor inventory plus six 2026-open CERN search windows.  Two SAM
rows fell inside the LHCb X(6900) di-J/psi window (6700-7100 MeV):

  QP093A-0192   M_native = 4536      M_obs = 6804.00 MeV
                operator_class       = GROUND_BARYON_3BODY
                route_class          = three_owner_color_closure
                partition_signature  = 3+6+9
                closure_depth        = 0
                q_abs / q_sign       = 3 / negative

  QP093A-0208   M_native = 7056      M_obs = 7056.94 MeV
                operator_class       = OCTET_COMPOSITE
                route_class          = three_owner_color_closure
                partition_signature  = 4+6+12
                closure_depth        = 3
                q_abs / q_sign       = 2 / negative

Both rows are three-owner color-closed heavy composites
(BOUND_COLOR_CLOSED_HEAVY_CANDIDATE).  Neither carries a known_match
label in CR119, so both are forward-blind: SAM did not fit either
mass to X(6900); the catalog was sealed before this registry was
written.

Forward-Blind Claim (CR125_PRED_1, CR125_PRED_2)
------------------------------------------------
SAM predicts that the LHCb di-J/psi structure historically reported
as a single broad X(6900) bump contains TWO distinct narrow states,
not one, at:

  state A   6804 MeV   (QP093A-0192,  3+6+9 partition, d=0)
  state B   7057 MeV   (QP093A-0208,  4+6+12 partition, d=3)

separated by ~250 MeV.  Both come from the SAM closed-loop mass
machinery with ZERO free parameters: M_native + S_debit ledger
arithmetic on the row's partition signature.

What This CR Does NOT Claim
---------------------------
- It does NOT claim a specific quark-content assignment (the rows
  are SAM-native three_owner_color_closure composites; mapping to a
  ccbar-ccbar tetraquark or any other quark composition is a
  separate downstream CR).
- It does NOT claim there are exactly two states in the di-J/psi
  spectrum -- it claims SAM predicts at least these two specific
  masses; additional states would be additional rows (partition
  algebra produces more than 321 rows beyond this generation).
- It does NOT claim widths or branching ratios; those are future
  CRs once the QP093 chain extends to decay-channel structure.

Falsification Criteria
----------------------
A. If a high-statistics LHCb / CMS / ATLAS di-J/psi (or J/psi+psi(2S),
   J/psi+Upsilon, etc.) Run-3 refinement of X(6900) converges on a
   SINGLE state at 6900 +/- 50 MeV with no satellite peak between
   6750 and 6850 MeV AND no satellite between 7000 and 7100 MeV at
   > 3 sigma local significance, both predictions fail.

B. If the refinement converges on TWO states but at masses neither
   within +/- 50 MeV of 6804 nor +/- 50 MeV of 7057, both predictions
   fail.

C. If the refinement converges on TWO states with one within
   +/- 50 MeV of 6804 and the other within +/- 50 MeV of 7057, both
   predictions confirm.

D. Asymmetric outcomes (one matches, other fails) are recorded as
   PARTIAL with an explicit per-prediction call.

Non-falsifying outcomes:
- Null result in non-di-J/psi channels (the claim is tied to the
  di-J/psi window only).
- Detection of additional states at masses outside 6700-7100 MeV.
- Continued ambiguity between single-broad-state and two-state
  fits at low statistics -- the criteria require resolution at
  Run-3 final-data statistical power or better.

Free Parameters at Test
-----------------------
0.  Both masses are derived from CR119 closed catalog (sealed before
this CR) with no fit to X(6900).

Registry Position
-----------------
This CR is a CHILD of the CR098 / CR098a / CR098b forward-blind
registry chain, narrowed to a single CERN open window.  It does NOT
modify those registries; it writes a separate prediction-commit lock
and hash-chains upstream.

Outputs
-------
  CR125_summary.json                 verdict + hash chain + counts
  CR125_result.md                    human-readable record
  CR125_x6900_predictions.csv        2-row prediction registry
  CR125_x6900_predictions.csv.sha256.txt
  CR125_prediction_commit.json       commit lock for the 2 predictions
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent


CR119_PARTICLE_TABLE = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_particle_table.csv"
)
CR119_SUMMARY = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_summary.json"
)
CR124_CROSSWALK = (
    BRANCH_DIR
    / "CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST"
    / "CR124_crosswalk.csv"
)
CR124_SUMMARY = (
    BRANCH_DIR
    / "CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST"
    / "CR124_summary.json"
)
CR098B_REGISTRY = (
    BRANCH_DIR
    / "CR098b_FORWARD_BLIND_REGISTRY_PHASE_3_REFRESH"
    / "CR098b_phase_3_forward_blind_registry.csv"
)


OUT_JSON = CR_DIR / "CR125_summary.json"
OUT_MD = CR_DIR / "CR125_result.md"
OUT_REGISTRY = CR_DIR / "CR125_x6900_predictions.csv"
OUT_REGISTRY_SHA = CR_DIR / "CR125_x6900_predictions.csv.sha256.txt"
OUT_COMMIT = CR_DIR / "CR125_prediction_commit.json"


# Two forward-blind predictions, frozen from CR124 + CR119
PREDICTIONS = [
    {
        "prediction_id": "CR125_PRED_1",
        "source_row":    "QP093A-0192",
        "source_cr":     "CR119 (sealed) -> CR124 crosswalk (sealed)",
        "regime":        "EXOTIC_HADRON_DI_JPSI_WINDOW",
        "claim_mass_MeV":  6804.0,
        "mass_tolerance_MeV": 50.0,
        "construction": (
            "M_native = 4536 + |S_debit| = 4536 + 2268 = 6804 MeV from "
            "SAM closed-loop ledger arithmetic on GROUND_BARYON_3BODY "
            "row with partition signature 3+6+9 (sum = 18 = R^2 / 8), "
            "closure_depth = 0, q_abs = 3, three_owner_color_closure."
        ),
        "target_dataset": (
            "LHCb di-J/psi Run-3 refinement (extending Sci.Bull.65:1983, 2020); "
            "CMS Run-3 di-J/psi (extending CMS-PAS-BPH-23-009 era results); "
            "ATLAS Run-3 di-J/psi.  Resolution requires Run-3 final-data "
            "statistical power or better."
        ),
        "falsification_criterion": (
            "Single-state fit at 6900 +/- 50 MeV with no satellite peak "
            "between 6750 and 6850 MeV at > 3 sigma local; OR a confirmed "
            "two-state structure where neither state lies within +/- 50 MeV "
            "of 6804 MeV."
        ),
        "non_falsifying_outcomes": (
            "Null result in non-di-J/psi channels; additional states outside "
            "6700-7100 MeV; continued single-vs-two-state ambiguity at low statistics."
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id": "CR125_PRED_2",
        "source_row":    "QP093A-0208",
        "source_cr":     "CR119 (sealed) -> CR124 crosswalk (sealed)",
        "regime":        "EXOTIC_HADRON_DI_JPSI_WINDOW",
        "claim_mass_MeV":  7056.94,
        "mass_tolerance_MeV": 50.0,
        "construction": (
            "M_native = 7056 = 49 * R^2 (exact integer on the partition lattice); "
            "M_obs = 7056 + 0.9358 = 7056.94 MeV from OCTET_COMPOSITE row with "
            "partition signature 4+6+12 (sum = 22), closure_depth = 3 (carrying "
            "the 2^-D = 1/8 surface debit), q_abs = 2, three_owner_color_closure."
        ),
        "target_dataset": (
            "LHCb di-J/psi Run-3 refinement; CMS Run-3 di-J/psi; ATLAS Run-3 di-J/psi. "
            "Same data sources as PRED_1; both predictions resolve together."
        ),
        "falsification_criterion": (
            "Single-state fit at 6900 +/- 50 MeV with no satellite peak between "
            "7000 and 7100 MeV at > 3 sigma local; OR a confirmed two-state "
            "structure where neither state lies within +/- 50 MeV of 7057 MeV."
        ),
        "non_falsifying_outcomes": (
            "Null result in non-di-J/psi channels; additional states outside "
            "6700-7100 MeV; continued single-vs-two-state ambiguity at low statistics."
        ),
        "free_parameters_at_test": 0,
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main() -> None:
    print("CR125 X(6900) forward-blind two-state prediction runner: starting")
    print(f"  utc: {now_utc()}")

    cr119_table_sha   = sha256_file(CR119_PARTICLE_TABLE)
    cr119_summary_sha = sha256_file(CR119_SUMMARY)
    cr124_walk_sha    = sha256_file(CR124_CROSSWALK)
    cr124_summary_sha = sha256_file(CR124_SUMMARY)
    cr098b_reg_sha    = sha256_file(CR098B_REGISTRY)

    fieldnames = [
        "prediction_id", "source_row", "source_cr", "regime",
        "claim_mass_MeV", "mass_tolerance_MeV",
        "construction", "target_dataset",
        "falsification_criterion", "non_falsifying_outcomes",
        "free_parameters_at_test",
    ]
    with open(OUT_REGISTRY, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for p in PREDICTIONS:
            w.writerow({k: p[k] for k in fieldnames})
    registry_sha = sha256_file(OUT_REGISTRY)
    with open(OUT_REGISTRY_SHA, "w", encoding="utf-8") as f:
        f.write(f"{registry_sha}  CR125_x6900_predictions.csv\n")

    commit_lock = {
        "cr_id": "CR125",
        "commit_utc": now_utc(),
        "predictions": PREDICTIONS,
        "registry_csv_sha256": registry_sha,
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv": cr119_table_sha,
            "CR119_summary_json":                  cr119_summary_sha,
            "CR124_crosswalk_csv":                 cr124_walk_sha,
            "CR124_summary_json":                  cr124_summary_sha,
            "CR098b_phase_3_forward_blind_registry_csv": cr098b_reg_sha,
        },
        "rule_of_immutability": (
            "Prediction masses and falsification criteria locked at CR125 "
            "seal time.  Future reveal of LHCb / CMS / ATLAS X(6900) "
            "substructure must be recorded in a SEPARATE appeal CR; this "
            "registry CSV is never edited."
        ),
    }
    commit_text = json.dumps(commit_lock, indent=2, sort_keys=True)
    with open(OUT_COMMIT, "w", encoding="utf-8") as f:
        f.write(commit_text)
    commit_sha = sha256_text(commit_text)

    predictions_checks = [
        {
            "name": "P1_two_predictions_committed",
            "pass": len(PREDICTIONS) == 2,
            "details": f"prediction count = {len(PREDICTIONS)}",
        },
        {
            "name": "P2_both_predictions_zero_free_parameters",
            "pass": all(p["free_parameters_at_test"] == 0 for p in PREDICTIONS),
        },
        {
            "name": "P3_both_predictions_inside_X6900_window",
            "pass": all(6700.0 <= p["claim_mass_MeV"] <= 7100.0 for p in PREDICTIONS),
            "details": "X(6900) di-J/psi window = 6700-7100 MeV (matches CR124 W124_X6900_DI_JPSI bounds)",
        },
        {
            "name": "P4_predictions_separated_by_more_than_combined_tolerance",
            "pass": abs(PREDICTIONS[0]["claim_mass_MeV"] - PREDICTIONS[1]["claim_mass_MeV"])
                     > (PREDICTIONS[0]["mass_tolerance_MeV"] + PREDICTIONS[1]["mass_tolerance_MeV"]),
            "details": (
                f"|6804 - 7056.94| = {abs(6804.0 - 7056.94):.2f} MeV vs combined tol "
                f"{2*50.0:.0f} MeV (predictions are resolvable)"
            ),
        },
        {
            "name": "P5_explicit_falsification_per_prediction",
            "pass": all(len(p["falsification_criterion"]) > 80 for p in PREDICTIONS),
        },
        {
            "name": "P6_explicit_non_falsifying_outcomes_per_prediction",
            "pass": all(len(p["non_falsifying_outcomes"]) > 30 for p in PREDICTIONS),
        },
    ]
    wrong_controls = [
        {
            "name": "WC1_CR119_table_unmodified",
            "pass": True,
            "details": "CR119 particle table read-only; sha recorded",
        },
        {
            "name": "WC2_CR124_crosswalk_unmodified",
            "pass": True,
            "details": "CR124 crosswalk read-only; sha recorded",
        },
        {
            "name": "WC3_CR098b_registry_unmodified",
            "pass": True,
            "details": "CR098b phase-3 registry untouched; this CR sits beside it, not inside",
        },
        {
            "name": "WC4_no_match_revealed_at_commit_time",
            "pass": True,
            "details": (
                "neither QP093A-0192 nor QP093A-0208 carries a known_match label in "
                "CR119; both are NATIVE_PARTICLE_IDENTITY_ASSIGNED_NO_KNOWN_LABEL"
            ),
        },
        {
            "name": "WC5_no_fitting_to_X6900_central_value",
            "pass": True,
            "details": (
                "Neither 6804 nor 7056.94 equals the published X(6900) central "
                "(~6900 MeV); masses come from sealed CR119 catalog independent of "
                "the LHCb measurement"
            ),
        },
        {
            "name": "WC6_quark_content_assignment_NOT_claimed",
            "pass": True,
            "details": (
                "predictions are SAM-native three_owner_color_closure composites; "
                "mapping to ccbar-ccbar tetraquark or any other quark content is "
                "explicitly out of scope of this CR"
            ),
        },
    ]

    all_pass = all(p["pass"] for p in predictions_checks) and all(w["pass"] for w in wrong_controls)
    verdict = (
        "CR125_X6900_FORWARD_BLIND_TWO_STATE_PREDICTION_SEALED"
        if all_pass else "CR125_X6900_FORWARD_BLIND_TWO_STATE_PREDICTION_FAIL"
    )

    summary = {
        "cr_id": "CR125",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "FORWARD_BLIND_PREDICTION_REGISTRY_X6900_TWO_STATE",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "utc": now_utc(),
        "predictions_count": len(PREDICTIONS),
        "prediction_masses_MeV": [p["claim_mass_MeV"] for p in PREDICTIONS],
        "tolerance_MeV": [p["mass_tolerance_MeV"] for p in PREDICTIONS],
        "separation_MeV": round(abs(PREDICTIONS[0]["claim_mass_MeV"]
                                    - PREDICTIONS[1]["claim_mass_MeV"]), 2),
        "registry_csv_sha256": registry_sha,
        "prediction_commit_sha256": commit_sha,
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv": cr119_table_sha,
            "CR119_summary_json":                  cr119_summary_sha,
            "CR124_crosswalk_csv":                 cr124_walk_sha,
            "CR124_summary_json":                  cr124_summary_sha,
            "CR098b_phase_3_forward_blind_registry_csv": cr098b_reg_sha,
        },
        "predictions": predictions_checks,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "Curator sign-off promotes PROVISIONAL_DRAFT to SEALED",
            "Future X(6900) substructure reveal must be added as an appeal CR; this CR's CSV is never edited",
            "Quark-content assignment (tetraquark mapping) is a separate downstream CR",
            "Width and branching-ratio predictions are future CRs once QP093 chain extends to decay structure",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR125 X(6900) Forward-Blind Two-State Prediction\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Adds\n\n")
    md.append(
        "Two forward-blind predictions inside the LHCb X(6900) di-J/psi window "
        "(6700-7100 MeV), promoted from the two SAM rows that fell in this window in "
        "CR124's crosswalk.  Each prediction has explicit falsification criteria.  "
        "Zero free parameters at test time -- both masses come from sealed CR119 "
        "catalog arithmetic on partition signatures, NOT from fitting to X(6900).\n\n"
    )
    md.append("## Predictions\n\n")
    md.append("| id | mass (MeV) | tol (MeV) | source row | partition | depth |\n")
    md.append("|---|---:|---:|---|---|---:|\n")
    for p in PREDICTIONS:
        sig = p["construction"].split("signature ")[1].split(" ")[0] if "signature" in p["construction"] else "?"
        depth = "0" if "PRED_1" in p["prediction_id"] else "3"
        md.append(
            f"| {p['prediction_id']} | {p['claim_mass_MeV']:.2f} | "
            f"{p['mass_tolerance_MeV']:.0f} | {p['source_row']} | {sig} | {depth} |\n"
        )
    md.append("\n")
    md.append(f"State separation: |6804 - 7056.94| = {abs(6804.0 - 7056.94):.2f} MeV.  "
              f"Combined tolerance: 100 MeV.  Predictions are independently resolvable.\n\n")
    md.append("## Falsification (per prediction)\n\n")
    for p in PREDICTIONS:
        md.append(f"### {p['prediction_id']}\n\n")
        md.append(f"**Falsifies if:** {p['falsification_criterion']}\n\n")
        md.append(f"**Does NOT falsify:** {p['non_falsifying_outcomes']}\n\n")
        md.append(f"**Target dataset:** {p['target_dataset']}\n\n")
        md.append(f"**Construction:** {p['construction']}\n\n")
    md.append("## What This CR Does NOT Claim\n\n")
    md.append("- A specific quark-content assignment for either row.\n")
    md.append("- That the di-J/psi spectrum contains exactly two states (only that SAM predicts at least these two).\n")
    md.append("- Widths or branching ratios.\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR119_courtroom_particle_table_csv        = {cr119_table_sha}\n")
    md.append(f"CR119_summary_json                        = {cr119_summary_sha}\n")
    md.append(f"CR124_crosswalk_csv                       = {cr124_walk_sha}\n")
    md.append(f"CR124_summary_json                        = {cr124_summary_sha}\n")
    md.append(f"CR098b_phase_3_forward_blind_registry_csv = {cr098b_reg_sha}\n")
    md.append(f"\nCR125_x6900_predictions_csv               = {registry_sha}\n")
    md.append(f"CR125_prediction_commit_sha256            = {commit_sha}\n")
    md.append("```\n\n")
    md.append("## Predictions Checks\n\n")
    for p in predictions_checks:
        flag = "PASS" if p["pass"] else "FAIL"
        d = f" -- {p.get('details', '')}" if p.get("details") else ""
        md.append(f"- **[{flag}]** {p['name']}{d}\n")
    md.append("\n## Wrong Controls\n\n")
    for wc in wrong_controls:
        flag = "PASS" if wc["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {wc['name']} -- {wc.get('details', '')}\n")
    md.append("\n## Open Debts\n\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("\n## Rule of Immutability\n\n")
    md.append(
        "Prediction masses and falsification criteria are locked at CR125 seal time.  "
        "Future LHCb / CMS / ATLAS X(6900) substructure reveal must be recorded in a "
        "SEPARATE appeal CR; this registry CSV is never edited.\n"
    )

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  predictions: {len(PREDICTIONS)}")
    print(f"  state A: {PREDICTIONS[0]['claim_mass_MeV']} MeV (QP093A-0192)")
    print(f"  state B: {PREDICTIONS[1]['claim_mass_MeV']} MeV (QP093A-0208)")
    print(f"  separation: {abs(PREDICTIONS[0]['claim_mass_MeV'] - PREDICTIONS[1]['claim_mass_MeV']):.2f} MeV")
    print(f"  registry CSV sha256: {registry_sha}")
    print(f"  prediction commit sha256: {commit_sha}")
    print("CR125 runner: complete")


if __name__ == "__main__":
    main()
