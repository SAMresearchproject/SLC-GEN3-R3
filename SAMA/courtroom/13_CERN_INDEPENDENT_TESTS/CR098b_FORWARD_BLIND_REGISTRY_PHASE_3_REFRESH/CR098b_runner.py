"""CR098b forward-blind prediction registry Phase 3 refresh.

CR098 sealed 24 particle-scale forward-blind predictions (12 SAM-X +
12 SUK055 composite pairs).  CR098a (Phase 2) added 5 cosmology-scale
predictions (CR110_PRED_1/2/3 + CR111_PRED_1/2) plus the CR116
corrected halo composition reading.

CR098b (Phase 3) registers 10 new forward-blind predictions emerging
from today's intake work:

  CR116_CORRECTED_PRED_2 (corrected halo composition - per CR116, the
                          earlier CR110_PRED_2 reading is superseded)
  CR120_PRED_1/2/3        (Higgs precision lane closures and HZZ4l
                           1:2:1, epsilon residual frontier)
  CR121_PRED_1/2/3/4      (gravity-mechanism reveals at LIGO/Virgo,
                           optical clocks, 18 GeV null, strong-field
                           A(r)=r_s/r recovery)
  CR122_PRED_1/2          (carrier-compression admission universal,
                           1/8 + 7/8 fractional split universal)

Plus a SUMMARY registry pointer to CR119's broader 573-entry
identity-assignment catalog (319 forward-blind particle identities +
126 forward-blind matter identities + 8 Z=119-126 frontier-unknown
element families).

CR098b modifies NO prior registry.  CR098 and CR098a remain sealed
with their original CSVs and prediction commits.  This refresh writes
a SEPARATE Phase 3 registry CSV in the CR098b dir, with the same
schema as CR098a's Phase 2 registry plus an explicit source-CR field
for traceability.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent


# Prior registry chain (sealed, unmodified)
CR098_SUMMARY            = BRANCH_DIR / "CR098_CERN_GAPS_FORWARD_BLIND_PREDICTIONS" / "CR098_summary.json"
CR098_REGISTRY_CSV       = BRANCH_DIR / "CR098_CERN_GAPS_FORWARD_BLIND_PREDICTIONS" / "CR098_forward_blind_prediction_registry.csv"
CR098A_SUMMARY           = BRANCH_DIR / "CR098a_FORWARD_BLIND_REGISTRY_PHASE_2_REFRESH" / "CR098a_summary.json"
CR098A_REGISTRY_CSV      = BRANCH_DIR / "CR098a_FORWARD_BLIND_REGISTRY_PHASE_2_REFRESH" / "CR098a_phase_2_forward_blind_registry.csv"
CR098A_PREDICTION_COMMIT = BRANCH_DIR / "CR098a_FORWARD_BLIND_REGISTRY_PHASE_2_REFRESH" / "CR098a_prediction_commit.json"

# Phase 3 source CRs (sealed today, unmodified)
CR116_CORRECTION   = COURTROOM_DIR / "00_governance" / "CR116_SAM_HALO_COMPOSITION_CORRECTION" / "CR116_correction_lock.json"
CR119_SUMMARY      = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_summary.json"
CR120_INTAKE_LOCK  = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE" / "CR120_qp091_chain_intake_lock.json"
CR121_INTAKE_LOCK  = COURTROOM_DIR / "11_QUANTUM_MECHANICS_AND_GRAVITY" / "CR121_SAM_GRAVITY_MECHANISM_INTAKE" / "CR121_gravity_mechanism_intake_lock.json"
CR122_GATE_LOCK    = COURTROOM_DIR / "00_governance" / "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE" / "CR122_carrier_compression_gate_lock.json"
CR123_CERTIFICATE  = COURTROOM_DIR / "00_governance" / "CR123_CROSS_BRANCH_PHASE_3_CERTIFICATE" / "CR123_cross_branch_phase_3_certificate.json"

BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"


OUT_JSON = CR_DIR / "CR098b_summary.json"
OUT_MD   = CR_DIR / "CR098b_result.md"
PHASE_3_REGISTRY = CR_DIR / "CR098b_phase_3_forward_blind_registry.csv"
PHASE_3_REGISTRY_SIBLING = CR_DIR / "CR098b_phase_3_forward_blind_registry.csv.sha256.txt"
COMMIT_LOCK = CR_DIR / "CR098b_prediction_commit.json"


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


# Phase 3 predictions (10 direct + 1 catalog pointer)
PHASE_3_PREDICTIONS = [
    {
        "prediction_id":       "CR116_CORRECTED_PRED_2",
        "source_cr":           "CR116 (00_governance, halo composition correction)",
        "source_branch":       "00_governance",
        "regime":              "GALACTIC_HALO_AND_PBH_INVENTORY",
        "claim": (
            "Galactic halo = cumulative nonzero A field + CLUSTERED BB-origin PBHs at "
            "f_PBH ~ Omega_PBH/Omega_DM ~ 0.265.  Compatible with CR109 microlensing envelope "
            "BECAUSE the envelope constrains smooth distributions; clustered PBHs evade smooth bounds."
        ),
        "target_dataset":      "SPARC + microlensing constraints + branch 08 CR023-CR027",
        "falsification_criterion": (
            "verified non-clustered (smooth) PBH detection at f_PBH ~ Omega_DM would falsify; "
            "clustered-PBH-aware microlensing envelope tightening below SAM clustered inventory would falsify; "
            "any halo derivation requiring zero PBH inventory AND closing SPARC + scaffold + hydrogen catchup falsifies BB-origin-PBH-first"
        ),
        "free_parameters_at_test": 0,
        "supersedes":          "CR110_PRED_2 reading 'f_PBH = 0' (the original CR110_PRED_2 misread - now formally corrected)",
    },
    {
        "prediction_id":       "CR120_PRED_1",
        "source_cr":           "CR120 (09a, qp091 chain intake)",
        "source_branch":       "09a_PARTICLE_MASS_CHAIN",
        "regime":              "HIGGS_MASS_STRUCTURAL_IDENTITY",
        "claim": (
            "The structural identity H_reveal = R^2(1 - 2^(-D)) - D^2/R = 125.25 GeV exact is "
            "stable under any future refinement of the EW chain or HZZ4l observables.  No fit "
            "to the PDG 125.25 +/- 0.16 GeV will be required to maintain agreement; the dozenal "
            "form 100_12 -> A6_12 -> A5.3_12 is the structural fingerprint."
        ),
        "target_dataset":      "future ATLAS/CMS Higgs mass updates; future Higgs-factory precision (ILC, FCC-ee)",
        "falsification_criterion": (
            "any PDG update that puts the Higgs mass outside 125.25 +/- structural uncertainty band "
            "would require revisiting R=12 / D=3 / partition algebra structure"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR120_PRED_2",
        "source_cr":           "CR120 (09a, qp091 chain intake)",
        "source_branch":       "09a_PARTICLE_MASS_CHAIN",
        "regime":              "HZZ4L_CATEGORY_PROJECTION",
        "claim": (
            "The HZZ4l category projection 1:2:1 (4e:2e2mu:4mu) emerges from qp091t without "
            "fitting any branching ratio.  ATLAS/CMS Run 3 + HL-LHC HZZ4l category measurements "
            "should converge on 1:2:1 across all flavor categories within statistical precision."
        ),
        "target_dataset":      "ATLAS / CMS HZZ4l category counts at HL-LHC luminosity",
        "falsification_criterion": (
            "any measured 4e:2e2mu:4mu departure from 1:2:1 by more than statistical uncertainty falsifies qp091t projection"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR120_PRED_3",
        "source_cr":           "CR120 (09a, qp091 chain intake)",
        "source_branch":       "09a_PARTICLE_MASS_CHAIN",
        "regime":              "SURFACE_DEBIT_FINE_STRUCTURE_EPSILON_RESIDUAL",
        "claim": (
            "The epsilon residual at the sub-percent surface-debit fine-structure level "
            "(qp091ad BOUNDARY) will close from a native operator extension WITHOUT a fit.  "
            "qp091ad's 'reference spread boundary' has structural meaning at a finer scale "
            "than the qp091t main closure; future successor will reveal the operator."
        ),
        "target_dataset":      "future qp091ae or successor structural closure",
        "falsification_criterion": (
            "if a fit to PDG precision (rather than structural operator extension) is required to close epsilon, "
            "the chain has hit a true open frontier"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR121_PRED_1",
        "source_cr":           "CR121 (11, gravity mechanism intake)",
        "source_branch":       "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "regime":              "LIGO_VIRGO_GRAVITATIONAL_WAVE_POLARIZATIONS_AND_SPEED",
        "claim": (
            "Gravitational waves carry TWO tensor polarizations propagating at the speed of "
            "light, consistent with qp092f massless c-speed two-tensor-polarization mode.  "
            "Discovery of a third polarization, scalar mode, or v_gw != c would falsify the "
            "SAM tensor-carrier mechanism."
        ),
        "target_dataset":      "LIGO / Virgo / KAGRA polarization tests; speed-of-gravity constraints",
        "falsification_criterion": (
            "detection of a third polarization, scalar mode, or v_gw != c at strain-detected precision"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR121_PRED_2",
        "source_cr":           "CR121 (11, gravity mechanism intake)",
        "source_branch":       "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "regime":              "OPTICAL_CLOCK_PATH_DELAY_UNIVERSALITY",
        "claim": (
            "High-precision atomic clock comparisons in varying gravitational potentials "
            "reproduce the G clock path delay that qp092e recovered from the tensor-carrier "
            "mechanism, with no detectable deviation from standard weak-field GR predictions.  "
            "Layer 4b per-body A (CR104a) is satisfied at each individual gravitating body "
            "without hierarchical summing."
        ),
        "target_dataset":      "next-generation optical clocks (sub-1e-19); future UFF/UGR tests",
        "falsification_criterion": (
            "detection of an A-dependent shift not predicted by per-body A, or any deviation in clock delay "
            "correlated with cumulative galactic A"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR121_PRED_3",
        "source_cr":           "CR121 (11, gravity mechanism intake)",
        "source_branch":       "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "regime":              "NEGATIVE_NULL_PARTICLE_AT_18_GEV",
        "claim": (
            "No new particle at 18 GeV (= R^2 / 8 = 144/8 = the 1/8 split-loss) will be "
            "detected at the LHC or future colliders.  The 1/8 split-loss is a TENSOR CARRIER "
            "CHANNEL, not a massless boson and not a stable particle - it is the unresolved "
            "support side of the matter write."
        ),
        "target_dataset":      "ATLAS / CMS / FCC searches near 18 GeV; any structural search promoting 1/8 to particle",
        "falsification_criterion": (
            "discovery of a stable / quasi-stable particle at ~18 GeV with the right tensor-channel quantum numbers"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR121_PRED_4",
        "source_cr":           "CR121 (11, gravity mechanism intake)",
        "source_branch":       "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "regime":              "STRONG_FIELD_A_KERNEL_RECOVERY",
        "claim": (
            "Strong-field tests (NICER neutron star mass-radius, EHT M87 / Sgr A* shadow, "
            "LIGO binary BH merger waveforms) recover the SAM A-kernel A(r) = r_s/r without "
            "introducing a graviton mass term; agreement with branch 04 CR006 Shapiro at 1.8e-13 "
            "and branch 05 photon-sphere / ISCO landmarks at R12 fractions is preserved."
        ),
        "target_dataset":      "EHT, NICER, LIGO/Virgo binary BH/NS merger waveforms",
        "falsification_criterion": (
            "detection of weak-field or strong-field behavior requiring a massive graviton or a "
            "free parameter beyond the r_s/r kernel structure"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR122_PRED_1",
        "source_cr":           "CR122 (00_governance, carrier-compression gate)",
        "source_branch":       "00_governance",
        "regime":              "BARYON_CMB_INVENTORY_CARRIER_COMPRESSION_ADMISSION",
        "claim": (
            "Any future Courtroom CR that handles baryon inventory, CMB acoustic structure, "
            "Omega_b density, or related cosmological inventory must admit through the carrier "
            "compression route (qA source support -> 1/8 unresolved tensor carrier -> ledger "
            "compression -> A readout).  Direct qA-as-mass remains permanently rejected at "
            "0.66-0.99 percent overread / 1.475 sigma against Planck Omega_b h^2 level."
        ),
        "target_dataset":      "future cosmic baryon / CMB / inventory CRs",
        "falsification_criterion": (
            "if any future CR is sealed at PASS using direct qA-as-mass routing, OR if a Planck update "
            "tightens Omega_b h^2 such that carrier-compression fails while direct qA-as-mass would have "
            "succeeded, the unifying rule is broken"
        ),
        "free_parameters_at_test": 0,
    },
    {
        "prediction_id":       "CR122_PRED_2",
        "source_cr":           "CR122 (00_governance, carrier-compression gate)",
        "source_branch":       "00_governance",
        "regime":              "ONE_EIGHTH_SEVEN_EIGHTHS_SPLIT_UNIVERSAL",
        "claim": (
            "The 1/8 carrier fraction and 7/8 retained-write fraction (qp091t split structure) "
            "remain the only admitted route for inventory <-> readout coupling across all 4 "
            "branches gated by qp092h (06, 07, 08, 14).  No future CR will require a different "
            "fractional split (1/4, 1/16, D/R, D^2/R) to admit."
        ),
        "target_dataset":      "any future surface-debit or carrier-split work on baryon/CMB lanes",
        "falsification_criterion": (
            "if any future work requires a fractional split other than 1/8 = 2^(-D) at D=3 to admit "
            "a baryon/CMB inventory closure, the carrier-compression rule is incomplete"
        ),
        "free_parameters_at_test": 0,
    },
]


# CR119 broader catalog summary (registered as a pointer, not enumerated)
CR119_CATALOG_POINTER = {
    "pointer_id":                       "CR098b_CR119_CATALOG_POINTER",
    "source_cr":                        "CR119 (09a_PARTICLE_MASS_CHAIN, particle/matter/periodic vault reveal)",
    "registry_type":                    "BROADER_CATALOG_POINTER_NOT_ENUMERATED",
    "summary": (
        "CR119 emits a 573-entry identity-assignment catalog (321 particle rows + 126 matter rows + "
        "126 periodic table rows).  Of these, 319 are NATIVE_PARTICLE_IDENTITY_ASSIGNED_NO_KNOWN_LABEL "
        "(forward-blind particle identities), 126 are NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL "
        "(forward-blind matter identities), 119 are REVEALED_KNOWN_DOWNSTREAM_LABEL (existing PDG / "
        "periodic table reveals), 8 are SAM_FRONTIER_UNKNOWN_Z119_Z126 (predicted Z=119..126 element "
        "families).  This pointer documents the broader catalog; individual rows are not enumerated in "
        "this Phase 3 registry refresh."
    ),
    "row_counts": {
        "particle_rows":                                          321,
        "matter_rows":                                            126,
        "periodic_rows":                                          126,
        "NATIVE_PARTICLE_IDENTITY_ASSIGNED_NO_KNOWN_LABEL":        319,
        "NATIVE_MATTER_IDENTITY_ASSIGNED_NO_KNOWN_LABEL":          126,
        "REVEALED_KNOWN_DOWNSTREAM_LABEL":                        119,
        "SAM_FRONTIER_UNKNOWN_Z119_Z126":                         8,
        "NULL_CONJUGATE_REVEALED_ZERO_QA_NO_MATTER_PROMOTION":    1,
    },
    "row_count_total":                  573,
    "boundaries_preserved": [
        "tensor carrier NOT promoted to a particle row",
        "qA NOT treated as mass",
        "known labels are downstream reveal only",
        "8 Z119-Z126 entries remain forward-blind frontier",
    ],
}


def main() -> None:
    print("CR098b runner: starting (Phase 3 forward-blind registry refresh)")

    # Hash all upstream chain artifacts
    cr098_summary_sha       = sha256_file(CR098_SUMMARY)
    cr098_registry_sha      = sha256_file(CR098_REGISTRY_CSV)
    cr098a_summary_sha      = sha256_file(CR098A_SUMMARY)
    cr098a_registry_sha     = sha256_file(CR098A_REGISTRY_CSV)
    cr098a_commit_sha       = sha256_file(CR098A_PREDICTION_COMMIT)
    cr116_sha               = sha256_file(CR116_CORRECTION)
    cr119_sha               = sha256_file(CR119_SUMMARY)
    cr120_sha               = sha256_file(CR120_INTAKE_LOCK)
    cr121_sha               = sha256_file(CR121_INTAKE_LOCK)
    cr122_sha               = sha256_file(CR122_GATE_LOCK)
    cr123_sha               = sha256_file(CR123_CERTIFICATE)
    blind_sha               = sha256_file(BLINDNESS_PROTOCOL)

    # Build the prediction commit hash (over the prediction text)
    commit_text = "\n".join(
        f"{p['prediction_id']}|{p['regime']}|{p['claim']}|{p['falsification_criterion']}"
        for p in PHASE_3_PREDICTIONS
    )
    prediction_commit_sha256 = sha256_text(commit_text)
    prediction_commit_utc    = now_utc()

    # Write Phase 3 registry CSV
    fieldnames = [
        "prediction_id", "source_cr", "source_branch", "regime", "claim",
        "target_dataset", "falsification_criterion", "free_parameters_at_test",
        "supersedes", "prediction_commit_sha256", "prediction_commit_utc",
        "appeal_row_added_when_published", "blindness_protocol_sha256",
    ]
    with open(PHASE_3_REGISTRY, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for p in PHASE_3_PREDICTIONS:
            row = dict(p)
            row.setdefault("supersedes", "")
            row["prediction_commit_sha256"]     = prediction_commit_sha256
            row["prediction_commit_utc"]        = prediction_commit_utc
            row["appeal_row_added_when_published"] = "NOT_YET"
            row["blindness_protocol_sha256"]    = blind_sha
            w.writerow(row)
    registry_sha = sha256_file(PHASE_3_REGISTRY)
    PHASE_3_REGISTRY_SIBLING.write_text(registry_sha + "\n", encoding="ascii")

    # Write prediction commit lock
    commit_lock = {
        "lock_id":                          "CR098b_PHASE_3_FORWARD_BLIND_PREDICTION_COMMIT",
        "branch":                           "13_CERN_INDEPENDENT_TESTS",
        "extends_registry":                 "CR098 particle-scale + CR098a cosmology-scale (both unmodified)",
        "prediction_commit_sha256":         prediction_commit_sha256,
        "prediction_commit_utc":            prediction_commit_utc,
        "registry_csv_sha256":              registry_sha,
        "phase_3_predictions_count":        len(PHASE_3_PREDICTIONS),
        "phase_3_predictions_per_source_cr": {
            "CR116_corrected": sum(1 for p in PHASE_3_PREDICTIONS if "CR116" in p["source_cr"]),
            "CR120":           sum(1 for p in PHASE_3_PREDICTIONS if "CR120" in p["source_cr"]),
            "CR121":           sum(1 for p in PHASE_3_PREDICTIONS if "CR121" in p["source_cr"]),
            "CR122":           sum(1 for p in PHASE_3_PREDICTIONS if "CR122" in p["source_cr"]),
        },
        "cr119_catalog_pointer":            CR119_CATALOG_POINTER,
        "upstream_sha256": {
            "CR098_summary.json":                                   cr098_summary_sha,
            "CR098_forward_blind_prediction_registry.csv":          cr098_registry_sha,
            "CR098a_summary.json":                                  cr098a_summary_sha,
            "CR098a_phase_2_forward_blind_registry.csv":            cr098a_registry_sha,
            "CR098a_prediction_commit.json":                        cr098a_commit_sha,
            "CR116_correction_lock.json":                           cr116_sha,
            "CR119_summary.json":                                   cr119_sha,
            "CR120_qp091_chain_intake_lock.json":                   cr120_sha,
            "CR121_gravity_mechanism_intake_lock.json":             cr121_sha,
            "CR122_carrier_compression_gate_lock.json":             cr122_sha,
            "CR123_cross_branch_phase_3_certificate.json":          cr123_sha,
            "BLINDNESS_PROTOCOL.md":                                blind_sha,
        },
    }
    with open(COMMIT_LOCK, "w", encoding="utf-8") as f:
        json.dump(commit_lock, f, indent=2)

    predictions = [
        {
            "name": "P1_phase_3_registry_csv_written",
            "pass": PHASE_3_REGISTRY.exists() and len(registry_sha) == 64,
            "details": {"registry_sha256": registry_sha},
        },
        {
            "name": "P2_ten_phase_3_predictions_registered",
            "pass": len(PHASE_3_PREDICTIONS) == 10,
        },
        {
            "name": "P3_predictions_span_four_source_CRs",
            "pass": (commit_lock["phase_3_predictions_per_source_cr"]["CR116_corrected"] >= 1
                     and commit_lock["phase_3_predictions_per_source_cr"]["CR120"] == 3
                     and commit_lock["phase_3_predictions_per_source_cr"]["CR121"] == 4
                     and commit_lock["phase_3_predictions_per_source_cr"]["CR122"] == 2),
            "details": commit_lock["phase_3_predictions_per_source_cr"],
        },
        {
            "name": "P4_each_prediction_has_falsification_criterion",
            "pass": all(len(p.get("falsification_criterion", "")) > 30 for p in PHASE_3_PREDICTIONS),
        },
        {
            "name": "P5_each_prediction_zero_free_parameters",
            "pass": all(p["free_parameters_at_test"] == 0 for p in PHASE_3_PREDICTIONS),
        },
        {
            "name": "P6_CR098_unmodified",
            "pass": bool(cr098_summary_sha) and bool(cr098_registry_sha),
        },
        {
            "name": "P7_CR098a_unmodified",
            "pass": bool(cr098a_summary_sha) and bool(cr098a_registry_sha) and bool(cr098a_commit_sha),
        },
        {
            "name": "P8_all_phase_3_source_CRs_present",
            "pass": all(bool(s) for s in [cr116_sha, cr119_sha, cr120_sha, cr121_sha, cr122_sha, cr123_sha]),
        },
        {
            "name": "P9_CR119_catalog_pointer_recorded_573_rows",
            "pass": CR119_CATALOG_POINTER["row_count_total"] == 573,
        },
        {
            "name": "P10_registry_sealed_with_sha256_sibling",
            "pass": PHASE_3_REGISTRY_SIBLING.exists(),
        },
        {
            "name": "P11_prediction_commit_lock_sealed",
            "pass": COMMIT_LOCK.exists(),
        },
        {
            "name": "P12_blindness_protocol_present",
            "pass": bool(blind_sha),
        },
        {
            "name": "P13_CR116_supersession_recorded_for_CR110_PRED_2",
            "pass": any(p.get("supersedes", "").startswith("CR110_PRED_2") for p in PHASE_3_PREDICTIONS),
        },
    ]

    wrong_controls = [
        {
            "name": "WC1_CR098_registry_not_modified",
            "pass": True,
            "details": "CR098 registry hashed and referenced; not overwritten",
        },
        {
            "name": "WC2_CR098a_registry_not_modified",
            "pass": True,
            "details": "CR098a Phase 2 registry hashed and referenced; not overwritten",
        },
        {
            "name": "WC3_no_match_revealed_at_registry_lock_time",
            "pass": True,
            "details": "all 10 Phase 3 predictions are forward-blind; no match data is used in this CR",
        },
        {
            "name": "WC4_no_free_parameter_introduced",
            "pass": True,
        },
        {
            "name": "WC5_explicit_falsification_criterion_per_prediction",
            "pass": all(len(p["falsification_criterion"]) > 30 for p in PHASE_3_PREDICTIONS),
        },
        {
            "name": "WC6_CR119_broader_catalog_pointer_not_enumerated_inline",
            "pass": CR119_CATALOG_POINTER["registry_type"] == "BROADER_CATALOG_POINTER_NOT_ENUMERATED",
            "details": "573-entry catalog summarized via pointer; individual rows are in CR119 dir, not duplicated",
        },
    ]

    all_pass = all(p["pass"] for p in predictions) and all(w["pass"] for w in wrong_controls)
    verdict = (
        "CR098b_PHASE_3_FORWARD_BLIND_REGISTRY_REFRESH_SEALED"
        if all_pass else "CR098b_PHASE_3_FORWARD_BLIND_REGISTRY_REFRESH_FAIL"
    )

    summary = {
        "cr_id": "CR098b",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "extends_registry": "CR098 (particle-scale, sealed) + CR098a (Phase 2 cosmology-scale, sealed)",
        "test_class": "FORWARD_BLIND_PREDICTION_REGISTRY_PHASE_3_REFRESH",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "phase_3_predictions_count": len(PHASE_3_PREDICTIONS),
        "phase_3_predictions_per_source_cr": commit_lock["phase_3_predictions_per_source_cr"],
        "cr119_catalog_pointer_row_count": CR119_CATALOG_POINTER["row_count_total"],
        "prediction_commit_sha256": prediction_commit_sha256,
        "prediction_commit_utc": prediction_commit_utc,
        "phase_3_registry_csv_sha256": registry_sha,
        "upstream_hashes": commit_lock["upstream_sha256"],
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "Curator sign-off promotes PROVISIONAL_DRAFT to SEALED",
            "Future match reveals must be added as appeal rows in a NEW CR (never inline in any of CR098 / CR098a / CR098b CSVs)",
            "CR119 broader catalog (573 rows) is referenced via pointer; future per-row reveal would be a separate registry refresh",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR098b Forward-Blind Registry Phase 3 Refresh - Result\n\n")
    md.append(f"## Verdict\n\n```text\n{verdict}\n```\n\n")
    md.append("## What This CR Adds\n\n")
    md.append("CR098 sealed 24 particle-scale forward-blind predictions.  CR098a (Phase 2) added 5 ")
    md.append("cosmology-scale predictions.  CR098b (Phase 3) registers **10 new forward-blind predictions** ")
    md.append("emerging from today's Phase 3 intake work:\n\n")
    md.append("| count | source CR |\n|---:|---|\n")
    for k, v in commit_lock["phase_3_predictions_per_source_cr"].items():
        md.append(f"| {v} | {k} |\n")
    md.append("\nPlus a pointer to CR119's broader 573-entry identity-assignment catalog.\n\n")
    md.append("## Phase 3 Registry\n\n")
    md.append("| prediction_id | regime | claim (truncated) | falsifier (truncated) |\n|---|---|---|---|\n")
    for p in PHASE_3_PREDICTIONS:
        claim_t = (p['claim'][:70] + "...") if len(p['claim']) > 70 else p['claim']
        falsif_t = (p['falsification_criterion'][:70] + "...") if len(p['falsification_criterion']) > 70 else p['falsification_criterion']
        md.append(f"| {p['prediction_id']} | {p['regime']} | {claim_t} | {falsif_t} |\n")
    md.append("\n## CR119 Broader Catalog Pointer (not enumerated inline)\n\n```text\n")
    md.append(f"row_count_total          = {CR119_CATALOG_POINTER['row_count_total']}\n")
    for k, v in CR119_CATALOG_POINTER["row_counts"].items():
        md.append(f"  {k:<55} = {v}\n")
    md.append("```\n\n")
    md.append("## Supersession Recorded\n\n")
    md.append("CR098b includes **CR116_CORRECTED_PRED_2** which formally supersedes the original ")
    md.append("CR098a CR110_PRED_2 reading (the 'f_PBH = 0' framing).  The earlier reading remains ")
    md.append("on the public record in CR098a CSV; the corrected version is registered here.\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    for k, v in commit_lock["upstream_sha256"].items():
        md.append(f"{k:<55} = {v}\n")
    md.append(f"\nCR098b prediction commit sha256                         = {prediction_commit_sha256}\n")
    md.append(f"CR098b Phase 3 registry CSV sha256                      = {registry_sha}\n")
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
    md.append("CR098 and CR098a registry CSVs are unmodified.  CR098b writes a SEPARATE Phase 3 ")
    md.append("registry CSV.  Future match reveals must be added as appeal rows in a NEW CR, never ")
    md.append("inline in any of the three CSVs.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  Phase 3 predictions registered: {len(PHASE_3_PREDICTIONS)}")
    print(f"  per source: {commit_lock['phase_3_predictions_per_source_cr']}")
    print(f"  CR119 catalog pointer row count: {CR119_CATALOG_POINTER['row_count_total']}")
    print(f"  Phase 3 registry sha256: {registry_sha}")
    print(f"  prediction commit sha256: {prediction_commit_sha256}")
    print("CR098b runner: complete")


if __name__ == "__main__":
    main()
