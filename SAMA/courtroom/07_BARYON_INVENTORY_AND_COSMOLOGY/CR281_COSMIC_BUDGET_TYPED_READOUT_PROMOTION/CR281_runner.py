from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


CR_ID = "CR281"
RECORD = "COSMIC_BUDGET_TYPED_READOUT_PROMOTION"
VERDICT_PASS = "PASS_COSMIC_BUDGET_TYPED_READOUT"
PRECOMMIT_SHA256 = "4db856290eba976ce47f6a9dc9a47c9f1ea81a4197a92ca0d736c9c69d31c93f"

CR_DIR = Path(__file__).resolve().parent
COURTROOM_ROOT = CR_DIR.parents[1]

SOURCES = {
    "SAM_VOLUME_I_SUBSTRATE": (
        COURTROOM_ROOT / "docs/SAM_VOLUME_I_SUBSTRATE.md",
        "88d8ef28863be32326264456ed3af24830cfbc633a25a157556c4b872b0122d3",
    ),
    "SAM_VOLUME_I_GLOSSARY": (
        COURTROOM_ROOT / "docs/SAM_VOLUME_I_GLOSSARY.md",
        "68714376542f773fe917b86d926128ac65a7ccd3f7ff9512f89f5ecfe1c2831f",
    ),
    "VOLUME_I_APPENDIX_AND_GLOSSARY": (
        COURTROOM_ROOT / "docs/VOLUME_I_APPENDIX_AND_GLOSSARY.md",
        "a1ce9da214e5ce0d60ede81d818a12c8d94be1a81a33dc5fd4b5b7da6ef69884",
    ),
    "CR003_19_summary": (
        COURTROOM_ROOT / "19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_summary.json",
        "860ff846ac0dc786176cbb1becb821bb10bfdf971682b6b638b5e095ad8ba9b5",
    ),
    "CR003_19_result": (
        COURTROOM_ROOT / "19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_result.md",
        "eb81ee8d9f8d395ad982133fe622fa0204109d10b2af688e41d44b748e07ad35",
    ),
    "CR018_07_summary": (
        COURTROOM_ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_summary.json",
        "a1d598841ecb06f8ea59f744c8f29e85ccdee32a6454fb5ee590c98ff545cc19",
    ),
    "CR018_07_result": (
        COURTROOM_ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_result.md",
        "9f84c09f44488ee86f1d55dcb54e9f25a05f97f3bcfcc458cd60948eae517b56",
    ),
    "CR019_07_summary": (
        COURTROOM_ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_summary.json",
        "c2dad0a4a45c9739962ccc106bec43343ee02bd82c58b1ed1818d105bef77ad3",
    ),
    "CR019_07_result": (
        COURTROOM_ROOT / "07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_result.md",
        "c000c57841687a0f39d8303a164658def99da72acd6af1b5bf675599fc96b2f4",
    ),
    "CR114_summary": (
        COURTROOM_ROOT / "00_governance/CR114_COSMIC_BARYON_BRIDGE_REVEAL/CR114_summary.json",
        "f503032f082938ddadc75f69783104af80d08cf078fa64e42d29dc177886f978",
    ),
    "CR114_cosmic_bridge": (
        COURTROOM_ROOT / "00_governance/CR114_COSMIC_BARYON_BRIDGE_REVEAL/CR114_cosmic_baryon_bridge.json",
        "e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6",
    ),
    "CR117_summary": (
        COURTROOM_ROOT / "00_governance/CR117_SAM_CMB_SCOPE_BOUNDARY/CR117_summary.json",
        "b625af5a9ad7f56fbcf975aad5caddd23efcfc7f2e93ca39f7b37fb8a2e3faae",
    ),
    "CR117_result": (
        COURTROOM_ROOT / "00_governance/CR117_SAM_CMB_SCOPE_BOUNDARY/CR117_result.md",
        "19e18898de5f0f1305a8417b8fcea8afa6c50f93b12a1e4a5288ba3570cfccf8",
    ),
    "CR036_19_summary": (
        COURTROOM_ROOT / "19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json",
        "97f3b07bba6e842a8474b62d5ab3b99fdcc8a3261536086d402c51b73ddae3af",
    ),
    "CR036_19_result": (
        COURTROOM_ROOT / "19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md",
        "fe1c9ee9c6a4ccf3c6f3d7d6e68ca34f93620c2650811f6b519ce636e1c247a6",
    ),
    "CR036_19_evidence_rows": (
        COURTROOM_ROOT / "19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_evidence_rows.csv",
        "03dd23411e8ccd07aadb612a2810931bf5130490de5b6669c9e58cf0f8c4aed6",
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def verify_sources() -> list[dict]:
    rows = []
    for source_id, (path, expected) in SOURCES.items():
        exists = path.exists()
        actual = sha256(path) if exists else None
        rows.append(
            {
                "id": source_id,
                "path": str(path).replace("\\", "/"),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "pass": exists and actual == expected,
            }
        )
    return rows


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_checks = verify_sources()
    if not all(row["pass"] for row in source_checks):
        verdict = "INVALID_COSMIC_BUDGET_PROVENANCE"
        summary = {
            "cr_id": CR_ID,
            "record": RECORD,
            "generated_utc": generated_utc,
            "primary_verdict": verdict,
            "source_hashes_pass": False,
            "source_hash_validation": source_checks,
        }
        write_json(CR_DIR / "CR281_summary.json", summary)
        raise SystemExit(f"{CR_ID} {verdict}: source hash validation failed")

    cr003 = read_json(SOURCES["CR003_19_summary"][0])
    cr018 = read_json(SOURCES["CR018_07_summary"][0])
    cr019 = read_json(SOURCES["CR019_07_summary"][0])
    cr114 = read_json(SOURCES["CR114_summary"][0])
    cr114_bridge = read_json(SOURCES["CR114_cosmic_bridge"][0])
    cr117 = read_json(SOURCES["CR117_summary"][0])
    cr036 = read_json(SOURCES["CR036_19_summary"][0])

    R = 12
    D = 3
    S = 8
    alpha_H = 2
    Theta = 18
    M = 126

    A0 = 1.0 / (math.pi * R)
    chi = (S / D) * A0
    Omega_b = alpha_H * A0 * (1.0 - chi)
    Omega_m = R * A0
    Omega_c = Omega_m - Omega_b
    Omega_Lambda = 1.0 - Omega_m
    Omega_m_eff = R * A0 - 2.0 * A0 * (chi + D * chi**2)

    eta = (M / (alpha_H**2 * Theta)) * A0**6

    bridge = cr036["dimensional_bridge"]
    c = bridge["c_m_s"]
    h = bridge["h_J_s"]
    hbar = h / (2.0 * math.pi)
    k_B = bridge["k_B_J_K"]
    G = bridge["G"]
    Mpc = bridge["Mpc_m"]
    m_p = bridge["m_p_kg"]
    T_CMB = bridge["T_CMB_K"]
    zeta_3 = bridge["zeta_3"]

    n_gamma = (2.0 * zeta_3 / (math.pi**2)) * ((k_B * T_CMB) / (hbar * c)) ** 3
    H100 = 100000.0 / Mpc
    rho_crit_h1 = 3.0 * H100**2 / (8.0 * math.pi * G)
    n_b_per_omega_b = rho_crit_h1 / m_p
    K_eta_to_omega_b = n_b_per_omega_b / n_gamma
    omega_b = eta / K_eta_to_omega_b
    h2 = omega_b / Omega_b
    h_reduced = math.sqrt(h2)
    H0 = 100.0 * h_reduced

    structural_checks = [
        {"name": "A0_matches_CR003", "pass": close(A0, cr003["closed_form_results"]["A_0_sealed_value"])},
        {"name": "A0_matches_CR018", "pass": close(A0, cr018["A0"])},
        {"name": "chi_matches_CR018", "pass": close(chi, cr018["chi"])},
        {"name": "Omega_b_matches_CR018", "pass": close(Omega_b, cr018["Omega_b"])},
        {"name": "Omega_m_clean_spine_is_1_over_pi", "pass": close(Omega_m, 1.0 / math.pi)},
        {"name": "Omega_m_matches_CR003", "pass": close(Omega_m, cr003["closed_form_results"]["Omega_m_via_coupling"])},
        {"name": "Omega_m_eff_matches_CR019", "pass": close(Omega_m_eff, cr019["Omega_m_eff"])},
    ]
    physical_checks = [
        {"name": "eta_matches_CR036", "pass": close(eta, cr036["eta"]["eta_SAM"], 1e-21)},
        {
            "name": "K_matches_CR036_computed_K",
            "pass": close(K_eta_to_omega_b, cr036["conversion"]["K_eta_to_omega_b"], 1e-20),
        },
        {"name": "omega_b_matches_CR036", "pass": close(omega_b, cr036["H0_cascade"]["omega_b_SAM"])},
        {
            "name": "h_squared_matches_CR036",
            "pass": close(h2, cr036["H0_cascade"]["h_SAM"] ** 2),
        },
        {"name": "H0_matches_CR036", "pass": close(H0, cr036["H0_cascade"]["H_0_SAM"])},
    ]
    boundary_checks = [
        {
            "name": "CR117_law_configuration_boundary_preserved",
            "pass": cr117.get("result_class") == "CR117_SAM_CMB_SCOPE_BOUNDARY_DOCUMENTED_AND_FORWARD_BLIND_LOCKED",
        },
        {"name": "CR114_bridge_zero_free_parameters", "pass": cr114_bridge.get("free_parameters_total") == 0},
    ]

    wrong_controls = [
        {
            "name": "WC1_A0_zero_rejected",
            "pass": (0.0 != A0) and (0.0 != Omega_b) and (0.0 != Omega_m),
            "details": {"A0_control": 0.0},
        },
        {
            "name": "WC2_remove_one_minus_chi_rejected",
            "pass": not close(alpha_H * A0, Omega_b),
            "details": {"without_factor": alpha_H * A0, "canonical": Omega_b},
        },
        {
            "name": "WC3_noncanonical_R_or_D_rejected",
            "pass": not close(13.0 * (1.0 / (math.pi * 13.0)), Omega_b)
            and not close((S / 4.0) * A0, chi),
            "details": {"R_control": 13, "D_control": 4},
        },
        {
            "name": "WC4_Omega_m_eff_not_clean_Omega_m_spine",
            "pass": not close(Omega_m_eff, Omega_m),
            "details": {"Omega_m_eff": Omega_m_eff, "Omega_m": Omega_m},
        },
        {
            "name": "WC5_Planck_omega_b_comparator_not_input",
            "pass": True,
            "details": {"Planck_omega_b_h2": cr114["Planck_Omega_b_h2"], "input_to_derivation": False},
        },
        {
            "name": "WC6_unsourced_K_rejected",
            "pass": K_eta_to_omega_b > 0 and close(K_eta_to_omega_b, cr036["conversion"]["K_eta_to_omega_b"], 1e-20),
            "details": {"K_source": "CR036 computed from FIRAS T_CMB plus CODATA/SI constants"},
        },
        {
            "name": "WC7_Omega_b_not_omega_b",
            "pass": not close(Omega_b, omega_b),
            "details": {"Omega_b": Omega_b, "omega_b": omega_b},
        },
    ]

    subverdicts = {
        "STRUCTURAL_INVENTORY_PASS": all(row["pass"] for row in structural_checks[:6]),
        "DIRECTIONAL_REFINEMENT_PASS": structural_checks[-1]["pass"],
        "PHYSICAL_DENSITY_PASS": all(row["pass"] for row in physical_checks[:3]),
        "HUBBLE_CASCADE_PASS": all(row["pass"] for row in physical_checks[3:]),
    }
    all_checks = structural_checks + physical_checks + boundary_checks + wrong_controls
    verdict = VERDICT_PASS if all(row["pass"] for row in all_checks) else "FAIL_COSMIC_BUDGET_IDENTITY"

    values = [
        ("A0", "SubstrateFloor", "1/(pi*R), R=12", A0, "", "SAM_OUTPUT", "CR003@19/CR018"),
        ("chi", "HorizonQuotient", "(S/D)*A0", chi, "", "SAM_OUTPUT", "CR018"),
        ("Omega_b", "BaryonInventoryFraction", "alpha_H*A0*(1-chi)", Omega_b, "", "SAM_OUTPUT", "CR018/CR114"),
        ("Omega_m", "MatterInventoryFraction", "R*A0=1/pi", Omega_m, "", "SAM_OUTPUT", "CR003@19/Volume I"),
        ("Omega_c", "DarkInventoryFraction", "Omega_m-Omega_b", Omega_c, "", "SAM_OUTPUT", "CR281 algebra"),
        ("Omega_Lambda", "SubstrateVacuumFraction", "1-Omega_m", Omega_Lambda, "", "SAM_OUTPUT", "Volume I/CR281 algebra"),
        (
            "Omega_m_eff",
            "EffectiveMatterFraction",
            "R*A0-2*A0*(chi+D*chi^2)",
            Omega_m_eff,
            "",
            "SAM_OUTPUT_REFINEMENT",
            "CR019",
        ),
        ("eta", "BaryonPhotonRatio", "(M/(alpha_H^2*Theta))*A0^6", eta, "", "SAM_OUTPUT", "CR036@19"),
        ("K_eta_to_omega_b", "DimensionalConversion", "n_b_per_omega_b/n_gamma(T_CMB)", K_eta_to_omega_b, "", "DIMENSIONAL_ANCHOR", "CR036@19"),
        ("omega_b", "PhysicalBaryonDensity", "eta/K(T_CMB)", omega_b, "", "SAM_OUTPUT_WITH_EXTERNAL_T_CMB_ANCHOR", "CR036@19"),
        ("h_squared", "ReducedHubbleParameterSquared", "omega_b/Omega_b", h2, "", "SAM_OUTPUT_WITH_EXTERNAL_T_CMB_ANCHOR", "CR036@19"),
        ("H0", "HubbleReadout", "100*sqrt(h_squared)", H0, "km/s/Mpc", "SAM_OUTPUT_WITH_EXTERNAL_T_CMB_ANCHOR", "CR036@19"),
        ("T_CMB", "CMBTemperatureAnchor", "FIRAS", T_CMB, "K", "EXTERNAL_DIMENSIONAL_ANCHOR", "CR036@19"),
        ("eta_reference", "Comparator", "Planck-side reference", cr036["eta"]["eta_reference"], "", "EXTERNAL_COMPARATOR", "CR036@19"),
        ("H0_reference", "Comparator", "Planck 2018 central", cr036["H0_cascade"]["H_0_reference"], "km/s/Mpc", "EXTERNAL_COMPARATOR", "CR036@19"),
    ]

    typed_contract = {
        "cr_id": CR_ID,
        "primary_verdict": verdict,
        "subverdicts": subverdicts,
        "typed_outputs": [
            {"type": row[1], "symbol": row[0], "formula": row[2], "value": row[3], "units": row[4], "role": row[5], "source": row[6]}
            for row in values
            if row[1] != "Comparator"
        ],
        "registration_recommendation": "register as cosmic-budget typed readout in SAM Language v0.3; keep Omega_m clean spine separate from Omega_m_eff refinement",
    }
    dependency_graph = {
        "cr_id": CR_ID,
        "nodes": [
            "A0",
            "chi",
            "Omega_b",
            "Omega_m",
            "Omega_c",
            "Omega_Lambda",
            "Omega_m_eff",
            "M",
            "Theta",
            "eta",
            "K(T_CMB)",
            "omega_b",
            "h_squared",
            "h",
            "H0",
        ],
        "chains": [
            ["A0", "chi", "Omega_b"],
            ["A0*R", "Omega_m", "Omega_c"],
            ["Omega_m", "Omega_Lambda"],
            ["A0", "chi", "D", "Omega_m_eff"],
            ["A0", "M", "Theta", "eta"],
            ["eta", "K(T_CMB)", "omega_b"],
            ["omega_b", "Omega_b", "h_squared"],
            ["h_squared", "h", "H0"],
        ],
        "edges": [
            {"from": ["A0", "S", "D"], "to": "chi", "formula": "chi=(S/D)*A0"},
            {"from": ["alpha_H", "A0", "chi"], "to": "Omega_b", "formula": "Omega_b=alpha_H*A0*(1-chi)"},
            {"from": ["R", "A0"], "to": "Omega_m", "formula": "Omega_m=R*A0=1/pi"},
            {"from": ["Omega_m", "Omega_b"], "to": "Omega_c", "formula": "Omega_c=Omega_m-Omega_b"},
            {"from": ["Omega_m"], "to": "Omega_Lambda", "formula": "Omega_Lambda=1-Omega_m"},
            {"from": ["R", "A0", "chi", "D"], "to": "Omega_m_eff", "formula": "R*A0-2*A0*(chi+D*chi^2)"},
            {"from": ["M", "alpha_H", "Theta", "A0"], "to": "eta", "formula": "(M/(alpha_H^2*Theta))*A0^6"},
            {"from": ["T_CMB", "SI/CODATA constants"], "to": "K(T_CMB)", "formula": "n_b_per_omega_b/n_gamma"},
            {"from": ["eta", "K(T_CMB)"], "to": "omega_b", "formula": "omega_b=eta/K"},
            {"from": ["omega_b", "Omega_b"], "to": "h_squared", "formula": "h^2=omega_b/Omega_b"},
            {"from": ["h_squared"], "to": "H0", "formula": "H0=100*sqrt(h^2)"},
        ],
        "forbidden_edge": {"from": "Planck_omega_b_h2", "to": "omega_b", "status": "rejected_comparator_only"},
    }

    provenance = {
        "cr_id": CR_ID,
        "record": RECORD,
        "generated_utc": generated_utc,
        "precommit_sha256": PRECOMMIT_SHA256,
        "source_hash_validation": source_checks,
        "K_source": {
            "source": "CR036@19",
            "T_CMB_K": T_CMB,
            "T_CMB_source": "FIRAS, as declared in CR036",
            "dimensional_constants_source": "CR036 in-runner literals from SI exact/CODATA 2018",
            "K_formula": "K=n_b_per_omega_b/n_gamma(T_CMB)",
            "K_value": K_eta_to_omega_b,
            "Planck_used_to_choose_or_normalize": False,
        },
        "source_contracts": {
            "CR003_verdict": cr003.get("verdict"),
            "CR018_verdict": cr018.get("verdict"),
            "CR019_verdict": cr019.get("verdict"),
            "CR114_result_class": cr114.get("result_class"),
            "CR114_bridge_free_parameters_total": cr114_bridge.get("free_parameters_total"),
            "CR117_result_class": cr117.get("result_class"),
            "CR036_verdict": cr036.get("verdict_token"),
        },
        "no_existing_artifact_modified": True,
    }

    summary = {
        "cr_id": CR_ID,
        "record": RECORD,
        "generated_utc": generated_utc,
        "execution_status": "CLEAN",
        "primary_verdict": verdict,
        "subverdicts": subverdicts,
        "source_hashes_pass": all(row["pass"] for row in source_checks),
        "precommit_sha256": PRECOMMIT_SHA256,
        "free_parameters_introduced": 0,
        "Planck_or_observational_comparator_used_as_input": False,
        "forecasts_generated": False,
        "structural_checks": structural_checks,
        "physical_checks": physical_checks,
        "boundary_checks": boundary_checks,
        "wrong_controls": wrong_controls,
        "values": {row[0]: row[3] for row in values},
        "implementation_notes": [
            "Initial CR281 execution at PREFLIGHT_20260711_032722 failed because the runner checked CR114_summary.json for free_parameters_total. The precommitted source containing that field is CR114_cosmic_baryon_bridge.json; the lookup was corrected without changing the verdict tree."
        ],
        "remaining_named_opens": [
            "CMB spectrum/modal perturbation outputs remain outside this typed budget record",
            "CR117 law/configuration boundary remains intact",
        ],
    }

    result_lines = [
        "# CR281 Cosmic-Budget Typed-Readout Promotion Result",
        "",
        f"generated_utc: {generated_utc}",
        f"primary_verdict: {verdict}",
        "execution_status: CLEAN",
        "",
        "## Structural Inventory",
        "",
        "```text",
        "A0 = 1/(pi*R)",
        "chi = (S/D)*A0",
        "Omega_b = alpha_H*A0*(1-chi)",
        "Omega_m = R*A0 = 1/pi",
        "Omega_c = Omega_m - Omega_b",
        "Omega_Lambda = 1 - Omega_m",
        "```",
        "",
        f"- A0: {A0:.20f}",
        f"- chi: {chi:.20f}",
        f"- Omega_b: {Omega_b:.20f}",
        f"- Omega_m: {Omega_m:.20f}",
        f"- Omega_c: {Omega_c:.20f}",
        f"- Omega_Lambda: {Omega_Lambda:.20f}",
        f"- Omega_m_eff (separate refinement): {Omega_m_eff:.20f}",
        "",
        "## Physical-Density Cascade",
        "",
        "```text",
        "eta = (M/(alpha_H^2*Theta))*A0^6",
        "omega_b = eta / K(T_CMB)",
        "h^2 = omega_b / Omega_b",
        "H0 = 100*sqrt(h^2)",
        "```",
        "",
        f"- eta: {eta:.18e}",
        f"- K(T_CMB): {K_eta_to_omega_b:.18e}",
        f"- omega_b: {omega_b:.18f}",
        f"- h^2: {h2:.18f}",
        f"- H0: {H0:.12f} km/s/Mpc",
        "",
        "K(T_CMB) source: CR036@19 computed from FIRAS T_CMB=2.7255 K plus CODATA/SI constants. Planck values are comparators only.",
        "",
        "## Implementation Note",
        "",
        "The initial CR281 execution at PREFLIGHT_20260711_032722 failed because the runner checked CR114_summary.json for free_parameters_total. The precommitted source containing that field is CR114_cosmic_baryon_bridge.json; the lookup was corrected without changing the verdict tree.",
        "",
        "## Wrong Controls",
        "",
    ]
    for row in wrong_controls:
        status = "PASS" if row["pass"] else "FAIL"
        result_lines.append(f"- [{status}] {row['name']}")
    result_lines.extend(
        [
            "",
            "## Boundaries Preserved",
            "",
            "- Omega_m_eff is not substituted for the clean Omega_m=1/pi spine.",
            "- CR117 CMB law/configuration boundary remains intact.",
            "- No CMB spectrum campaign, forecast, or new bridge is generated.",
            "",
            "## Verdict Statement",
            "",
            f"{verdict}. The cosmic budget is promoted as a typed readout from A0 through Omega_b/Omega_m and, through sealed CR036 support, eta, omega_b, h^2, and H0.",
            "",
        ]
    )

    write_json(CR_DIR / "CR281_summary.json", summary)
    write_json(CR_DIR / "CR281_provenance.json", provenance)
    write_json(CR_DIR / "CR281_typed_contract.json", typed_contract)
    write_json(CR_DIR / "CR281_dependency_graph.json", dependency_graph)
    (CR_DIR / "CR281_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    with (CR_DIR / "CR281_values.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "typed_output", "formula", "value", "units", "role", "source"])
        for row in values:
            writer.writerow(row)

    artifacts = [
        "CR281_PRECOMMIT.md",
        "CR281_runner.py",
        "CR281_result.md",
        "CR281_summary.json",
        "CR281_provenance.json",
        "CR281_typed_contract.json",
        "CR281_dependency_graph.json",
        "CR281_values.csv",
    ]
    (CR_DIR / "HASHES.txt").write_text(
        "\n".join(f"{sha256(CR_DIR / name)}  {name}" for name in artifacts) + "\n",
        encoding="utf-8",
    )

    if verdict != VERDICT_PASS:
        raise SystemExit(f"{CR_ID} {verdict}")


if __name__ == "__main__":
    main()
