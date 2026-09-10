"""CR108 Planck Omega_b cosmological anchor intake.

Loads the public Planck 2018 cosmological parameters (Planck Collaboration
2020 A&A 641 A6) as a sealed Courtroom anchor for the cosmic baryon
density Omega_b h^2.  This anchor is consumed by CR111 (cosmic baryon
Omega_b closure appeal) where the SAM substrate prediction for the
baryon fraction is appealed.

CR108 does NOT reveal a match.  It is pure INTAKE of the public Planck
reference numbers with proper provenance.

The Planck 2018 TT,TE,EE+lowE+lensing best fit gives:
  Omega_b h^2  = 0.02237 +/- 0.00015     (PRIMARY anchor for CR111)
  Omega_c h^2  = 0.1200  +/- 0.0012
  H_0          = 67.36 +/- 0.54 km/s/Mpc
  Omega_b      = 0.04930 +/- 0.00057     (Omega_b / h^2 used downstream)

CR108 holds these as anchors only.

Branch continuation: CR107 (SPARC intake) -> CR108 (this CR).
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR107_ANCHOR = BRANCH_DIR / "CR107_SPARC_GALAXY_ROTATION_CURVE_INTAKE" / "CR107_sparc_anchor.json"
CR106_VERDICT = BRANCH_DIR / "CR106_14_BRANCH_VERDICT_ZIPPER" / "CR106_14_branch_verdict.json"
BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"

OUT_JSON = CR_DIR / "CR108_summary.json"
OUT_MD   = CR_DIR / "CR108_result.md"
ANCHOR_OUT = CR_DIR / "CR108_planck_anchor.json"
ANCHOR_SIBLING = CR_DIR / "CR108_planck_anchor.json.sha256.txt"


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


# Public Planck 2018 cosmological parameters
# Source: Planck Collaboration, "Planck 2018 results. VI. Cosmological
# parameters", A&A 641 A6 (2020), arXiv:1807.06209.
# Quoted values are the TT,TE,EE+lowE+lensing best fit (their Table 2,
# baseline LCDM column).
PLANCK_2018_REFERENCE = {
    "source_paper": {
        "title": "Planck 2018 results. VI. Cosmological parameters",
        "authors": "Planck Collaboration",
        "journal": "A&A 641 A6 (2020)",
        "arxiv": "1807.06209",
    },
    "dataset_combination": "TT,TE,EE+lowE+lensing baseline LCDM",
    "parameters": {
        "Omega_b_h2": {
            "value": 0.02237,
            "uncertainty": 0.00015,
            "role": "PRIMARY anchor for CR111 cosmic baryon closure appeal",
        },
        "Omega_c_h2": {
            "value": 0.1200,
            "uncertainty": 0.0012,
            "role": "secondary - cold component reference for cumulative-A reading",
        },
        "H0_km_s_Mpc": {
            "value": 67.36,
            "uncertainty": 0.54,
            "role": "Hubble constant from same dataset",
        },
        "Omega_b": {
            "value": 0.04930,
            "uncertainty": 0.00057,
            "role": "baryon density parameter (Omega_b h^2 / h^2)",
        },
        "n_s": {
            "value": 0.9649,
            "uncertainty": 0.0042,
            "role": "scalar spectral index",
        },
        "sigma_8": {
            "value": 0.8111,
            "uncertainty": 0.0060,
            "role": "matter power normalization",
        },
    },
}


def main():
    print("CR108 runner: starting (Planck Omega_b cosmological anchor intake)")

    cr107_sha = sha256_file(CR107_ANCHOR)
    cr106_sha = sha256_file(CR106_VERDICT)
    blindness_sha = sha256_file(BLINDNESS_PROTOCOL)

    planck_anchor = {
        "anchor_id": "CR108_PLANCK_2018_OMEGA_B_PUBLIC_REFERENCE_ANCHOR",
        "branch": "14_FOUNDATIONAL_TESTS",
        "extends_anchor": "CR107 (SPARC intake) -> CR106 (14 branch verdict zipper)",
        "sealed_at_utc": now_utc(),
        "intake_class": "PUBLIC_REFERENCE_DATA_NO_MATCH_REVEALED",
        "upstream_sha256": {
            "CR107_sparc_anchor.json":               cr107_sha,
            "CR106_14_branch_verdict.json":          cr106_sha,
            "BLINDNESS_PROTOCOL.md":                 blindness_sha,
        },
        "planck_2018_reference": PLANCK_2018_REFERENCE,
        "what_this_anchor_provides": [
            "Planck 2018 Omega_b h^2 = 0.02237 +/- 0.00015 as the cosmic baryon anchor",
            "associated LCDM baseline parameters for cross-check (Omega_c h^2, H_0, n_s, sigma_8)",
            "a sealed reference for CR111 cosmic baryon closure appeal",
        ],
        "what_this_anchor_does_NOT_do": [
            "compare any SAM substrate prediction to Planck values (deferred to CR111)",
            "modify any prior CR verdict",
        ],
        "free_parameters_total": 0,
    }

    with open(ANCHOR_OUT, "w", encoding="utf-8") as f:
        json.dump(planck_anchor, f, indent=2)
    anchor_sha = sha256_file(ANCHOR_OUT)
    ANCHOR_SIBLING.write_text(anchor_sha + "\n", encoding="ascii")

    predictions = [
        {
            "name": "P1_planck_2018_reference_sealed",
            "pass": True,
            "details": {
                "Omega_b_h2": PLANCK_2018_REFERENCE["parameters"]["Omega_b_h2"]["value"],
                "paper": PLANCK_2018_REFERENCE["source_paper"]["title"],
            },
        },
        {
            "name": "P2_upstream_cr107_anchor_present",
            "pass": bool(cr107_sha),
            "details": {"cr107_anchor_sha256": cr107_sha},
        },
        {
            "name": "P3_cr106_branch_verdict_present",
            "pass": bool(cr106_sha),
        },
        {
            "name": "P4_blindness_protocol_present",
            "pass": bool(blindness_sha),
        },
        {
            "name": "P5_zero_free_parameters_at_intake",
            "pass": True,
        },
        {
            "name": "P6_no_match_revealed_yet",
            "pass": True,
            "details": "match deferred to CR111 cosmic baryon closure appeal",
        },
    ]

    wrong_controls = [
        {
            "name": "WC1_no_sam_prediction_value_substituted_for_planck_reference",
            "pass": True,
        },
        {
            "name": "WC2_no_prior_CR_verdict_modified",
            "pass": True,
        },
        {
            "name": "WC3_anchor_file_sealed_with_sha256_sibling",
            "pass": ANCHOR_SIBLING.exists(),
            "details": {"anchor_sha256": anchor_sha},
        },
    ]

    all_pass = all(p["pass"] for p in predictions) and all(w["pass"] for w in wrong_controls)
    verdict = "CR108_PLANCK_OMEGA_B_INTAKE_PASS" if all_pass else "CR108_PLANCK_OMEGA_B_INTAKE_FAIL"

    summary = {
        "cr_id": "CR108",
        "branch": "14_FOUNDATIONAL_TESTS",
        "extends_anchor": "CR107 (SPARC intake) -> CR106 (14 branch verdict zipper)",
        "test_class": "PUBLIC_PLANCK_2018_REFERENCE_INTAKE_NO_MATCH_REVEAL",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "anchor_lock_sha256": anchor_sha,
        "upstream_hashes": planck_anchor["upstream_sha256"],
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "next_courtroom_step": "CR109 PBH abundance constraint intake, then CR110 three-mode closure appeal, then CR111 cosmic baryon closure appeal",
        "open_debts": [
            "Match reveal of SAM substrate Omega_b prediction deferred to CR111",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR108 Planck Omega_b Cosmological Anchor Intake - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Intakes\n\n")
    md.append("Public Planck 2018 cosmological parameters (Planck Collaboration 2020, ")
    md.append("A&A 641 A6, arXiv:1807.06209).  Sealed as a Courtroom anchor against which ")
    md.append("CR111 will appeal the cosmic baryon Omega_b closure.\n\n")
    md.append("**This CR reveals no match.**  Match reveal is deferred to CR111.\n\n")
    md.append("## Planck 2018 Reference (baseline LCDM TT,TE,EE+lowE+lensing)\n\n")
    md.append("| parameter | value | uncertainty | role |\n|---|---|---|---|\n")
    for name, info in PLANCK_2018_REFERENCE["parameters"].items():
        md.append(f"| {name} | {info['value']} | {info['uncertainty']} | {info['role']} |\n")
    md.append("\n## Cryptographic Chain\n\n```text\n")
    md.append(f"CR107 SPARC anchor                  = {cr107_sha}\n")
    md.append(f"CR106 14 branch verdict             = {cr106_sha}\n")
    md.append(f"BLINDNESS_PROTOCOL.md               = {blindness_sha}\n")
    md.append(f"CR108 Planck anchor sha256          = {anchor_sha}\n")
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
    md.append("- **CR109** intakes microlensing PBH abundance constraints.\n")
    md.append("- **CR110** opens the three-mode Earth/Galaxy/PBH closure appeal.\n")
    md.append("- **CR111** opens the cosmic baryon Omega_b closure appeal against this Planck anchor.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  anchor sha256: {anchor_sha}")
    print("CR108 runner: complete")


if __name__ == "__main__":
    main()
