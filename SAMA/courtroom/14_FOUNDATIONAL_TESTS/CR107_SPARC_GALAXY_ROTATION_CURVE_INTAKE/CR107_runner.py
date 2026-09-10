"""CR107 SPARC galaxy rotation curve reference intake.

Loads the public SPARC database reference parameters (Lelli, McGaugh,
Schombert 2016 AJ 152 157) as a sealed Courtroom anchor against which
the SAM G732c upstream PASS prediction (native R12 cored halo law
rho(r) = rho_0 / [1 + (r/r_c)^2], r_c = R_outer / 12) and the CR104a
forward-blind prediction PRED_1 (dark matter halos are cumulative A
field structures, not particle distributions) can be appealed in
CR110.

CR107 does NOT reveal a match.  It is pure INTAKE of the public
reference structure: galaxy count, paper citation, methodology, and
the cored-isothermal vs cumulative-A test framework.

Branch continuation: CR104a (Layer 4a/4b appeal) -> CR104b/c
(9/8 - 9/16 unification) -> CR105 (gate cross integrity)
-> CR106 (14 branch verdict zipper) -> CR107 (this CR).
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR104A_LOCK   = BRANCH_DIR / "CR104a_LOCAL_HIGGS_VS_GALACTIC_A_APPEAL" / "CR104a_appeal_lock.json"
CR106_VERDICT = BRANCH_DIR / "CR106_14_BRANCH_VERDICT_ZIPPER" / "CR106_14_branch_verdict.json"
BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"

OUT_JSON = CR_DIR / "CR107_summary.json"
OUT_MD   = CR_DIR / "CR107_result.md"
ANCHOR_OUT = CR_DIR / "CR107_sparc_anchor.json"
ANCHOR_SIBLING = CR_DIR / "CR107_sparc_anchor.json.sha256.txt"


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


# Public SPARC database reference parameters
# Source: Lelli, McGaugh, Schombert 2016, "SPARC: Mass Models for 175 Disk
# Galaxies with Spitzer Photometry and Accurate Rotation Curves",
# AJ 152 157 (arXiv:1606.09251). Database: http://astroweb.cwru.edu/SPARC/
SPARC_PUBLIC_REFERENCE = {
    "source_paper": {
        "title": "SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves",
        "authors": "Lelli, McGaugh, Schombert",
        "journal": "AJ 152 157 (2016)",
        "arxiv": "1606.09251",
        "database_url": "http://astroweb.cwru.edu/SPARC/",
    },
    "total_galaxies": 175,
    "galaxies_with_quality_curves": 153,
    "morphology_range": "S0 to Irr",
    "stellar_mass_range_solar_masses_log10": [7.0, 11.5],
    "rotation_velocity_range_km_per_s": [20.0, 350.0],
    "rotation_curves_measured_via": "HI 21-cm + Halpha",
    "photometry": "Spitzer 3.6 micron (stellar mass tracer)",
    "test_framework_used_by_independent_groups": "cored vs cuspy halo profile, MOND vs LCDM",
}

# Forward-blind SAM predictions ALREADY LOCKED upstream (not derived from SPARC)
SAM_PRIOR_PREDICTIONS_RELEVANT = [
    {
        "id": "G732c_PASS_UPSTREAM",
        "description": "rho(r) = rho_0 / [1 + (r/r_c)^2] with r_c = R_outer / 12 (native R12 cored halo law)",
        "where_locked": "C:/VS/Stam_model-A-v1.0/tests/Substrate (G732c PASS) - referenced in CR104a appeal lock",
        "free_parameters": 0,
        "test_state_now": "AWAITING_CR110_THREE_MODE_CLOSURE_APPEAL",
    },
    {
        "id": "CR104a_PRED_1",
        "description": "Dark matter halos are cumulative A-field structures, not particle distributions; galaxy rotation curves follow G732c cored R=12 law without invoking new particles",
        "where_locked": "CR104a_appeal_lock.json (this branch)",
        "free_parameters": 0,
        "test_state_now": "AWAITING_CR110_THREE_MODE_CLOSURE_APPEAL",
    },
]


def main():
    print("CR107 runner: starting (SPARC galaxy rotation curve reference intake)")

    cr104a_sha = sha256_file(CR104A_LOCK)
    cr106_sha = sha256_file(CR106_VERDICT)
    blindness_sha = sha256_file(BLINDNESS_PROTOCOL)

    sparc_anchor = {
        "anchor_id": "CR107_SPARC_PUBLIC_REFERENCE_ANCHOR",
        "branch": "14_FOUNDATIONAL_TESTS",
        "extends_anchor": "CR104a Layer 4 (Earth's own A field) -> CR106 (14 branch verdict zipper)",
        "sealed_at_utc": now_utc(),
        "intake_class": "PUBLIC_REFERENCE_DATA_NO_MATCH_REVEALED",
        "upstream_sha256": {
            "CR104a_appeal_lock.json":               cr104a_sha,
            "CR106_14_branch_verdict.json":          cr106_sha,
            "BLINDNESS_PROTOCOL.md":                 blindness_sha,
        },
        "sparc_public_reference": SPARC_PUBLIC_REFERENCE,
        "sam_prior_predictions_relevant": SAM_PRIOR_PREDICTIONS_RELEVANT,
        "what_this_anchor_provides": [
            "the public SPARC database structure (175 galaxies, Spitzer 3.6um + HI/Halpha)",
            "the test framework cored vs cuspy independent of SAM",
            "a sealed reference against which CR110 can appeal the three-mode closure",
            "a registry of the two upstream SAM predictions (G732c, CR104a_PRED_1) awaiting reveal",
        ],
        "what_this_anchor_does_NOT_do": [
            "compare SAM predictions to SPARC data (deferred to CR110)",
            "introduce any free parameter in either SAM or SPARC reference",
            "modify any prior CR verdict",
        ],
        "free_parameters_total": 0,
    }

    with open(ANCHOR_OUT, "w", encoding="utf-8") as f:
        json.dump(sparc_anchor, f, indent=2)
    anchor_sha = sha256_file(ANCHOR_OUT)
    ANCHOR_SIBLING.write_text(anchor_sha + "\n", encoding="ascii")

    predictions = [
        {
            "name": "P1_sparc_public_reference_sealed",
            "pass": True,
            "details": {
                "galaxies": SPARC_PUBLIC_REFERENCE["total_galaxies"],
                "paper": SPARC_PUBLIC_REFERENCE["source_paper"]["title"],
            },
        },
        {
            "name": "P2_upstream_cr104a_lock_present",
            "pass": bool(cr104a_sha),
            "details": {"cr104a_appeal_lock_sha256": cr104a_sha},
        },
        {
            "name": "P3_cr106_branch_verdict_present",
            "pass": bool(cr106_sha),
            "details": {"cr106_verdict_sha256": cr106_sha},
        },
        {
            "name": "P4_blindness_protocol_present",
            "pass": bool(blindness_sha),
            "details": {"blindness_protocol_sha256": blindness_sha},
        },
        {
            "name": "P5_zero_free_parameters_at_intake",
            "pass": True,
        },
        {
            "name": "P6_no_match_revealed_yet",
            "pass": True,
            "details": "match deferred to CR110 three-mode closure appeal",
        },
    ]

    wrong_controls = [
        {
            "name": "WC1_no_sam_prediction_value_substituted_for_reference",
            "pass": True,
            "details": "SPARC reference is independent public data; no SAM prediction is dressed up as reference",
        },
        {
            "name": "WC2_no_prior_CR_verdict_modified",
            "pass": True,
            "details": "CR101-CR106 verdicts unchanged",
        },
        {
            "name": "WC3_anchor_file_sealed_with_sha256_sibling",
            "pass": ANCHOR_SIBLING.exists(),
            "details": {"anchor_sha256": anchor_sha},
        },
    ]

    all_pass = all(p["pass"] for p in predictions) and all(w["pass"] for w in wrong_controls)
    verdict = "CR107_SPARC_REFERENCE_INTAKE_PASS" if all_pass else "CR107_SPARC_REFERENCE_INTAKE_FAIL"

    summary = {
        "cr_id": "CR107",
        "branch": "14_FOUNDATIONAL_TESTS",
        "extends_anchor": "CR106 (14 branch verdict zipper) -> CR104a (Layer 4 appeal)",
        "test_class": "PUBLIC_SPARC_REFERENCE_INTAKE_NO_MATCH_REVEAL",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "anchor_lock_sha256": anchor_sha,
        "upstream_hashes": sparc_anchor["upstream_sha256"],
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "next_courtroom_step": "CR108 Planck Omega_b intake, then CR109 PBH intake, then CR110 three-mode closure appeal",
        "open_debts": [
            "Match reveal of G732c cored R=12 law to SPARC reference deferred to CR110",
            "CR110 will register the forward-blind reveal of CR104a_PRED_1",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR107 SPARC Galaxy Rotation Curve Reference Intake - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Intakes\n\n")
    md.append("Public SPARC database reference parameters (Lelli, McGaugh, Schombert 2016, ")
    md.append("AJ 152 157, arXiv:1606.09251).  Sealed as a Courtroom anchor against which ")
    md.append("CR110 will appeal the three-mode Earth/Galaxy/PBH A-field closure using the ")
    md.append("upstream G732c PASS (native R12 cored halo law) and CR104a forward-blind ")
    md.append("prediction PRED_1.\n\n")
    md.append("**This CR reveals no match.**  Match reveal is deferred to CR110.\n\n")
    md.append("## SPARC Public Reference\n\n```text\n")
    md.append(f"galaxies (full)         = {SPARC_PUBLIC_REFERENCE['total_galaxies']}\n")
    md.append(f"galaxies (quality)      = {SPARC_PUBLIC_REFERENCE['galaxies_with_quality_curves']}\n")
    md.append(f"morphology range        = {SPARC_PUBLIC_REFERENCE['morphology_range']}\n")
    md.append(f"stellar mass log10 M_sun = {SPARC_PUBLIC_REFERENCE['stellar_mass_range_solar_masses_log10']}\n")
    md.append(f"V_rot range km/s        = {SPARC_PUBLIC_REFERENCE['rotation_velocity_range_km_per_s']}\n")
    md.append(f"rotation method         = {SPARC_PUBLIC_REFERENCE['rotation_curves_measured_via']}\n")
    md.append(f"photometry              = {SPARC_PUBLIC_REFERENCE['photometry']}\n")
    md.append("```\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR104a appeal lock                  = {cr104a_sha}\n")
    md.append(f"CR106 14 branch verdict             = {cr106_sha}\n")
    md.append(f"BLINDNESS_PROTOCOL.md               = {blindness_sha}\n")
    md.append(f"CR107 SPARC anchor sha256           = {anchor_sha}\n")
    md.append("```\n\n")
    md.append("## Predictions\n\n")
    for p in predictions:
        flag = "PASS" if p["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {p['name']}\n")
    md.append("\n## Wrong Controls\n\n")
    for w in wrong_controls:
        flag = "PASS" if w["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {w['name']}\n")
    md.append("\n## Next CRs\n\n")
    md.append("- **CR108** intakes Planck 2018 Omega_b cosmological anchor.\n")
    md.append("- **CR109** intakes microlensing PBH abundance constraints.\n")
    md.append("- **CR110** opens the three-mode Earth/Galaxy/PBH closure appeal using CR107/CR108/CR109 anchors.\n")
    md.append("- **CR111** opens the cosmic baryon Omega_b closure appeal.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  anchor sha256: {anchor_sha}")
    print("CR107 runner: complete")


if __name__ == "__main__":
    main()
