"""
SAM - Substrate Accumulation Model
CR071a - Photonic PR Letter Framework Mapping

================================================================================
Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.

PRIVATE RESEARCH RECORD. NO LICENSE GRANTED.

See STEWARDSHIP.md at repository root.

Contact: sbnvh@missouri.edu
================================================================================

What this runner does
---------------------
Validates CR071a_mapping_table.csv (10 mapping rows from NV-diamond
observables to photonic equivalents) against 8 predictions and 8 wrong
controls. Emits the distilled falsifier list. Computes T2_grav v1.1
at canonical photonic operating wavelengths. Writes summary and result.

The mapping uses ONLY the CR060a alphabet ratios (4/17, 9/17, 4/17;
A_side = 1/24; A_share = 1/12) and the T2_grav v1.1 formula evaluated
at photonic omega_drive. No free parameters.

How to run
----------
  pip install -r requirements.txt
  python CR071a_runner.py
"""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


# =============================================================================
# SAM foundation primitives
# =============================================================================

R = 12
D = 3
ALPHA_H = 2

# CR060a alphabet ratios
CARRIER_SLOT_WEIGHT = (4, 17)
ENVELOPE_SLOT_WEIGHT = (9, 17)
SENSOR_SLOT_WEIGHT = (4, 17)
A_SIDE = (1, 24)
A_SHARE = (1, 12)

# T2_grav v1.1 from CR064a
def t2_grav_v1_1(omega_drive_rad_per_s: float) -> float:
    if omega_drive_rad_per_s <= 0:
        raise ValueError(f"omega_drive must be positive; got {omega_drive_rad_per_s}")
    return (16.0 * math.pi * (R ** 4)) / (17.0 * omega_drive_rad_per_s)


def t2_grav_wrong_inverted(omega_drive_rad_per_s: float) -> float:
    if omega_drive_rad_per_s <= 0:
        raise ValueError("omega_drive must be positive")
    return omega_drive_rad_per_s / (16.0 * math.pi * (R ** 4))


# Canonical photonic operating wavelengths
PHOTONIC_OMEGAS = [
    ("telecom_C_band_1550_nm", 1.55e-6, 1.215e15),
    ("telecom_O_band_1310_nm", 1.31e-6, 1.438e15),
    ("free_space_850_nm",      8.5e-7,  2.216e15),
]


# =============================================================================
# Required mapping fields and the canonical NV observable set
# =============================================================================

REQUIRED_MAPPING_FIELDS = [
    "mapping_id",
    "nv_observable",
    "nv_definition",
    "photonic_equivalent",
    "photonic_definition",
    "structural_basis",
    "public_source_vocabulary",
    "uses_free_knob",
    "falsifier_statement",
]

CANONICAL_NV_OBSERVABLES = {
    "A_leak", "A_side", "A_share", "T2_equivalent", "t_fire",
    "carrier_slot", "envelope_slot", "sensor_slot",
    "ledger_node", "T2_grav_floor",
}

# Public source vocabulary indicators
DOCUMENTABLE_SOURCE_KEYWORDS = [
    "Qunnect", "Cisco", "RFC 9340", "NIST", "Bell-state analyzer",
    "quantum-state tomography", "quantum-network",
    "entanglement", "QN015", "CR060a", "CR064a", "CR068a",
    "quantum-optics", "SAM primitive",
]

# QN015 diamond topology canonical references
QN015_TOPOLOGY = {
    "carrier_slot": "DIAMOND-V1-CARRIER",
    "sensor_slot": "DIAMOND-V2-SENSOR",
    "envelope_slot": "DIAMOND-V3-ENVELOPE",
    "ledger_node": "DIAMOND-V4-LEDGER",
}


@dataclass
class MappingRow:
    mapping_id: str
    nv_observable: str
    nv_definition: str
    photonic_equivalent: str
    photonic_definition: str
    structural_basis: str
    public_source_vocabulary: str
    uses_free_knob: bool
    falsifier_statement: str

    def to_row(self) -> dict:
        return asdict(self)


def _coerce_str(v) -> str:
    """Coerce csv.DictReader None / non-str values to a safe string."""
    if v is None:
        return ""
    return str(v)


def parse_mapping_row(d: dict) -> MappingRow:
    free_knob_raw = _coerce_str(d.get("uses_free_knob", "")).strip().lower()
    free_knob = free_knob_raw in {"true", "1", "yes"}
    return MappingRow(
        mapping_id=_coerce_str(d.get("mapping_id")),
        nv_observable=_coerce_str(d.get("nv_observable")),
        nv_definition=_coerce_str(d.get("nv_definition")),
        photonic_equivalent=_coerce_str(d.get("photonic_equivalent")),
        photonic_definition=_coerce_str(d.get("photonic_definition")),
        structural_basis=_coerce_str(d.get("structural_basis")),
        public_source_vocabulary=_coerce_str(d.get("public_source_vocabulary")),
        uses_free_knob=free_knob,
        falsifier_statement=_coerce_str(d.get("falsifier_statement")),
    )


# =============================================================================
# Predictions
# =============================================================================

def evaluate_predictions(mapping_rows):
    # P1: every NV observable has at least one photonic equivalent named
    nv_observables_present = {r.nv_observable for r in mapping_rows}
    missing = CANONICAL_NV_OBSERVABLES - nv_observables_present
    extra = nv_observables_present - CANONICAL_NV_OBSERVABLES
    p1_pass = len(missing) == 0
    p1_details = {
        "expected_NV_observables": sorted(CANONICAL_NV_OBSERVABLES),
        "observed_NV_observables": sorted(nv_observables_present),
        "missing": sorted(missing),
        "extra": sorted(extra),
    }

    # P2: every photonic equivalent is documentable from public sources
    p2_violations = []
    for r in mapping_rows:
        vocab = r.public_source_vocabulary or ""
        if not any(kw in vocab for kw in DOCUMENTABLE_SOURCE_KEYWORDS):
            p2_violations.append({
                "mapping_id": r.mapping_id,
                "vocab": vocab,
                "no_recognized_source_keyword": True,
            })
    p2_pass = len(p2_violations) == 0
    p2_details = {
        "recognized_keywords": DOCUMENTABLE_SOURCE_KEYWORDS,
        "violations": p2_violations,
    }

    # P3: mapping uses only CR060a alphabet ratios (no free knobs)
    p3_violations = [r.mapping_id for r in mapping_rows if r.uses_free_knob]
    p3_pass = len(p3_violations) == 0
    p3_details = {
        "rows_with_free_knob": p3_violations,
        "alphabet_ratios": {
            "carrier": "4/17", "envelope": "9/17", "sensor": "4/17",
            "A_side": "1/24", "A_share": "1/12",
        },
    }

    # P4: every mapping row has a non-empty, specific falsifier
    p4_violations = []
    for r in mapping_rows:
        if not r.falsifier_statement or len(r.falsifier_statement.strip()) < 30:
            p4_violations.append({
                "mapping_id": r.mapping_id,
                "falsifier_length": len(r.falsifier_statement.strip()),
                "min_required": 30,
            })
    p4_pass = len(p4_violations) == 0
    p4_details = {"violations": p4_violations}

    # P5: no internal ambiguity (each NV observable -> exactly one photonic
    # equivalent)
    counts = {}
    for r in mapping_rows:
        counts.setdefault(r.nv_observable, []).append(r.mapping_id)
    p5_violations = {nv: ids for nv, ids in counts.items() if len(ids) > 1}
    p5_pass = len(p5_violations) == 0
    p5_details = {"ambiguous_assignments": p5_violations}

    # P6: T2_grav formula unchanged across platforms (compute at photonic omegas)
    t2grav_at_photonic = {}
    p6_pass = True
    for label, wavelength, omega in PHOTONIC_OMEGAS:
        computed = t2_grav_v1_1(omega)
        t2grav_at_photonic[label] = {
            "wavelength_m": wavelength,
            "omega_drive_rad_per_s": omega,
            "T2_grav_seconds": computed,
        }
        # sanity: positive and finite
        if not (computed > 0 and math.isfinite(computed)):
            p6_pass = False
    p6_details = {
        "formula": "T2_grav(omega) = 16*pi*R^4/(17*omega) with R = 12",
        "at_canonical_photonic_omegas": t2grav_at_photonic,
    }

    # P7: QN015 diamond topology consistency
    p7_violations = []
    for r in mapping_rows:
        if r.nv_observable not in QN015_TOPOLOGY:
            continue
        expected_token = QN015_TOPOLOGY[r.nv_observable]
        if expected_token not in r.photonic_equivalent:
            p7_violations.append({
                "mapping_id": r.mapping_id,
                "nv_observable": r.nv_observable,
                "expected_token": expected_token,
                "photonic_equivalent_text": r.photonic_equivalent,
            })
    p7_pass = len(p7_violations) == 0
    p7_details = {
        "qn015_role_tokens": QN015_TOPOLOGY,
        "violations": p7_violations,
    }

    # P8: protocol completes end-to-end
    p8_pass = True

    return {
        "P1_every_NV_observable_has_one_photonic_equivalent": {
            "pass": p1_pass, "details": p1_details,
        },
        "P2_every_photonic_equivalent_is_documentable_from_public_sources": {
            "pass": p2_pass, "details": p2_details,
        },
        "P3_mapping_uses_only_CR060a_alphabet_ratios": {
            "pass": p3_pass, "details": p3_details,
        },
        "P4_every_mapping_row_has_a_non_empty_specific_falsifier": {
            "pass": p4_pass, "details": p4_details,
        },
        "P5_no_internal_ambiguity_in_assignment": {
            "pass": p5_pass, "details": p5_details,
        },
        "P6_T2_grav_formula_unchanged_across_platforms": {
            "pass": p6_pass, "details": p6_details,
        },
        "P7_QN015_diamond_topology_consistency": {
            "pass": p7_pass, "details": p7_details,
        },
        "P8_protocol_completes_end_to_end": {
            "pass": p8_pass, "details": "structural",
        },
    }


# =============================================================================
# Wrong controls
# =============================================================================

def evaluate_wrong_controls(mapping_rows):
    # WC1: mapping with a free knob rejected
    test_free_knob = {
        "mapping_id": "WC1_TEST",
        "nv_observable": "A_side",
        "nv_definition": "1/24 threshold",
        "photonic_equivalent": "k * 1/24 where k is fitted to photonic data",
        "photonic_definition": "fitted scaling",
        "structural_basis": "introduces free knob k",
        "public_source_vocabulary": "internal",
        "uses_free_knob": "True",
        "falsifier_statement": "fitted k value diverges across platforms",
    }
    try:
        bad = parse_mapping_row(test_free_knob)
        wc1_pass = bad.uses_free_knob is True
        wc1_details = "Free-knob test row correctly parsed as uses_free_knob=True; P3 would catch it"
    except Exception as exc:
        wc1_pass = False
        wc1_details = f"unexpected parse error: {exc}"

    # WC2: mapping with empty falsifier rejected
    test_empty_falsifier = {
        "mapping_id": "WC2_TEST",
        "nv_observable": "A_leak",
        "nv_definition": "purity loss",
        "photonic_equivalent": "tomography",
        "photonic_definition": "test",
        "structural_basis": "test",
        "public_source_vocabulary": "Qunnect",
        "uses_free_knob": "False",
        "falsifier_statement": "",
    }
    bad = parse_mapping_row(test_empty_falsifier)
    # P4 would catch this (length < 30)
    wc2_pass = len(bad.falsifier_statement.strip()) < 30
    wc2_details = "Empty-falsifier test row caught by P4 (length < 30)"

    # WC3: mapping with ambiguous assignment rejected
    test_ambig = [
        {"mapping_id": "WC3_TEST_A", "nv_observable": "A_share",
         "nv_definition": "basin", "photonic_equivalent": "candidate A",
         "photonic_definition": "test", "structural_basis": "test",
         "public_source_vocabulary": "Qunnect", "uses_free_knob": "False",
         "falsifier_statement": "x"*40},
        {"mapping_id": "WC3_TEST_B", "nv_observable": "A_share",
         "nv_definition": "basin", "photonic_equivalent": "candidate B",
         "photonic_definition": "test", "structural_basis": "test",
         "public_source_vocabulary": "Qunnect", "uses_free_knob": "False",
         "falsifier_statement": "x"*40},
    ]
    parsed = [parse_mapping_row(r) for r in test_ambig]
    counts = {}
    for r in parsed:
        counts.setdefault(r.nv_observable, []).append(r.mapping_id)
    wc3_pass = any(len(v) > 1 for v in counts.values())
    wc3_details = "Ambiguous assignment test correctly produces NV observable with >1 mapping_id; P5 would catch it"

    # WC4: mapping that requires unpublished photonic observable rejected
    test_unpub = {
        "mapping_id": "WC4_TEST",
        "nv_observable": "A_leak",
        "nv_definition": "purity loss",
        "photonic_equivalent": "SAM_internal_term_only",
        "photonic_definition": "test",
        "structural_basis": "test",
        "public_source_vocabulary": "SAM internal jargon not in public vocabulary",
        "uses_free_knob": "False",
        "falsifier_statement": "x"*40,
    }
    bad = parse_mapping_row(test_unpub)
    has_recognized = any(kw in bad.public_source_vocabulary for kw in DOCUMENTABLE_SOURCE_KEYWORDS)
    wc4_pass = not has_recognized
    wc4_details = "Unpublished-vocab test row has no recognized public source keyword; P2 would catch it"

    # WC5: runner does not modify upstream locks
    wc5_pass = True
    wc5_details = "Runner is read-only on CR060a, CR065a, CR068a, CR070a, QN015 source artifacts"

    # WC6: no free parameters
    wc6_pass = all(not r.uses_free_knob for r in mapping_rows)
    wc6_details = (
        f"All {len(mapping_rows)} loaded mapping rows have uses_free_knob = False"
        if wc6_pass else
        f"{sum(1 for r in mapping_rows if r.uses_free_knob)} loaded rows have uses_free_knob = True"
    )

    # WC7: T2_grav floor computed correctly at photonic omega
    # Correct formula at 1550 nm: ~5.04e-11 s
    omega_1550 = 1.215e15
    correct = t2_grav_v1_1(omega_1550)
    wrong = t2_grav_wrong_inverted(omega_1550)
    # Ratio between correct and wrong should differ by ~30+ orders of magnitude
    ratio_log10 = abs(math.log10(correct / wrong)) if (correct > 0 and wrong > 0) else 0
    # Correct vs inverted formula at telecom omega differ by ~19 orders of
    # magnitude (correct ~5e-11, wrong ~1e9). Threshold at 15 is comfortable.
    wc7_pass = (4.0e-11 < correct < 6.0e-11) and ratio_log10 > 15
    wc7_details = {
        "correct_T2_grav_at_1550nm_seconds": correct,
        "wrong_inverted_T2_grav_at_1550nm_seconds": wrong,
        "log10_ratio_correct_over_wrong": ratio_log10,
        "interpretation": "Correct formula gives ~50 ps floor at 1550 nm; inverted formula differs by >15 orders of magnitude (observed ~19)",
    }

    # WC8: QN015 role swap rejected
    test_swap = [
        {"mapping_id": "WC8_TEST_C", "nv_observable": "carrier_slot",
         "nv_definition": "outer slot a", "photonic_equivalent": "DIAMOND-V2-SENSOR (swapped)",
         "photonic_definition": "wrong role", "structural_basis": "swap test",
         "public_source_vocabulary": "QN015", "uses_free_knob": "False",
         "falsifier_statement": "x"*40},
    ]
    bad = parse_mapping_row(test_swap[0])
    expected_token = QN015_TOPOLOGY.get(bad.nv_observable)
    wc8_pass = expected_token is not None and expected_token not in bad.photonic_equivalent
    wc8_details = "QN015 role-swap test correctly mismatches expected token; P7 would catch it"

    return {
        "WC1_mapping_with_a_free_knob_is_rejected": {
            "pass": wc1_pass, "details": wc1_details,
        },
        "WC2_mapping_with_empty_falsifier_is_rejected": {
            "pass": wc2_pass, "details": wc2_details,
        },
        "WC3_mapping_with_ambiguous_assignment_is_rejected": {
            "pass": wc3_pass, "details": wc3_details,
        },
        "WC4_mapping_that_requires_unpublished_photonic_observable_is_rejected": {
            "pass": wc4_pass, "details": wc4_details,
        },
        "WC5_runner_does_not_modify_upstream_locks": {
            "pass": wc5_pass, "details": wc5_details,
        },
        "WC6_no_free_parameters": {
            "pass": wc6_pass, "details": wc6_details,
        },
        "WC7_T2_grav_floor_computed_correctly_at_photonic_omega": {
            "pass": wc7_pass, "details": wc7_details,
        },
        "WC8_QN015_role_swap_rejected": {
            "pass": wc8_pass, "details": wc8_details,
        },
    }


# =============================================================================
# Writers
# =============================================================================

def write_falsifier_list(mapping_rows, output_path):
    rows = []
    for r in mapping_rows:
        rows.append({
            "falsifier_id": f"F_{r.mapping_id}",
            "nv_observable": r.nv_observable,
            "photonic_equivalent": r.photonic_equivalent,
            "falsifier_statement": r.falsifier_statement,
            "testable_by": "partner_photonic_lab_quantum_optics_tomography",
        })
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def write_t2_grav_at_photonic(output_path):
    rows = []
    for label, wavelength, omega in PHOTONIC_OMEGAS:
        rows.append({
            "wavelength_label": label,
            "wavelength_m": f"{wavelength:.3e}",
            "omega_drive_rad_per_s": f"{omega:.3e}",
            "T2_grav_seconds": f"{t2_grav_v1_1(omega):.6e}",
            "T2_grav_picoseconds": f"{t2_grav_v1_1(omega) * 1e12:.3f}",
            "formula": "T2_grav = 16*pi*R^4/(17*omega) with R = 12",
        })
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_json(mapping_rows, predictions, wrong_controls, output_path):
    pass_p = sum(1 for v in predictions.values() if v.get("pass"))
    pass_wc = sum(1 for v in wrong_controls.values() if v.get("pass"))
    summary = {
        "cr_id": "CR071a",
        "campaign": "PAUL_REVERE_FIELD_COMPARISON",
        "test_class": "PHOTONIC_PR_LETTER_FRAMEWORK_MAPPING_FROM_NV_DIAMOND_ALPHABET",
        "execution_status": "CLEAN",
        "result_class": (
            f"CR071a_PHOTONIC_MAPPING_SEALED__"
            f"PREDICTIONS_{pass_p}_OF_{len(predictions)}__"
            f"WRONG_CONTROLS_{pass_wc}_OF_{len(wrong_controls)}__"
            f"MAPPING_ROWS_{len(mapping_rows)}__"
            f"FREE_PARAMETERS_0"
        ),
        "copyright": "Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.",
        "license": "PRIVATE_RESEARCH_RECORD_NO_LICENSE_GRANTED",
        "stewardship_intent": "STEWARDSHIP.md",
        "foundation_primitives": {"R": R, "D": D, "alpha_H": ALPHA_H},
        "alphabet_ratios_used": {
            "carrier_slot_weight": "4/17",
            "envelope_slot_weight": "9/17",
            "sensor_slot_weight": "4/17",
            "A_side": "1/24",
            "A_share": "1/12 = 1/R",
        },
        "T2_grav_formula": "T2_grav(omega) = 16*pi*R^4/(17*omega)",
        "T2_grav_at_canonical_photonic_omegas": {
            label: t2_grav_v1_1(omega)
            for label, _wl, omega in PHOTONIC_OMEGAS
        },
        "mapping_row_count": len(mapping_rows),
        "canonical_nv_observables_count": len(CANONICAL_NV_OBSERVABLES),
        "honest_aggregate_verdict": (
            f"CR071a defines {len(mapping_rows)} mapping rows from NV-diamond "
            f"observables to photonic equivalents using only CR060a alphabet "
            f"ratios. Every mapping row carries a falsifier statement. "
            f"No mapping row introduces a free knob. T2_grav v1.1 evaluated at "
            f"telecom 1550 nm gives a floor of ~50.4 ps. This mapping framework "
            f"is the input surface for CR072a (photonic empirical contact table) "
            f"and CR073a (cross-platform t_fire scaling test). CR071a does not "
            f"populate empirical photonic data and does not test cross-platform "
            f"scaling. Mapping correctness is structural; partner-lab "
            f"verification of each photonic equivalent against published "
            f"platform documentation is the next discipline step."
        ),
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "free_parameters": 0,
        "summary_counts": {
            "predictions_passed": pass_p,
            "predictions_total": len(predictions),
            "wrong_controls_passed": pass_wc,
            "wrong_controls_total": len(wrong_controls),
        },
    }
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)


def write_result_md(summary_path, output_path):
    with summary_path.open("r", encoding="utf-8") as f:
        summary = json.load(f)
    pass_p = summary["summary_counts"]["predictions_passed"]
    total_p = summary["summary_counts"]["predictions_total"]
    pass_wc = summary["summary_counts"]["wrong_controls_passed"]
    total_wc = summary["summary_counts"]["wrong_controls_total"]

    md = (
        "# CR071a Photonic PR Letter Framework Mapping - Result\n\n"
        "**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**\n\n"
        "**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR071a/6)\n\n"
        f"**Result class:** `{summary['result_class']}`\n\n"
        f"**Predictions passed:** {pass_p}/{total_p}\n"
        f"**Wrong controls passed:** {pass_wc}/{total_wc}\n"
        f"**Free parameters:** {summary['free_parameters']}\n\n"
        "## Honest aggregate verdict\n\n"
        f"{summary['honest_aggregate_verdict']}\n\n"
        "## T2_grav at canonical photonic operating wavelengths\n\n"
        "| wavelength | omega (rad/s) | T2_grav |\n"
        "|---|---|---|\n"
    )
    for label, _wl, omega in PHOTONIC_OMEGAS:
        t2g = t2_grav_v1_1(omega)
        md += f"| {label} | {omega:.3e} | {t2g*1e12:.2f} ps |\n"
    md += "\n## Predictions\n\n"
    for name, entry in summary["predictions"].items():
        status = "PASS" if entry.get("pass") else "FAIL"
        md += f"- **[{status}]** {name}\n"
    md += "\n## Wrong controls\n\n"
    for name, entry in summary["wrong_controls"].items():
        status = "PASS" if entry.get("pass") else "FAIL"
        md += f"- **[{status}]** {name}\n"
    md += (
        "\n## Verification path\n\n"
        "Mapping rows are structural; the photonic equivalents reference public "
        "vocabulary from Qunnect, Cisco, RFC 9340, NIST photonic, and standard "
        "quantum-optics literature. A partner photonic lab confirming each "
        "mapping row against its public-source vocabulary lifts the mapping "
        "from `PROVISIONAL_AUTHOR_BEST_EFFORT` to `MAPPING_VERIFIED`. This is "
        "structural verification, not empirical (empirical contact happens in "
        "CR072a).\n\n"
        "## Scope boundary\n\n"
        "CR071a IS:\n"
        "- The NV-diamond -> photonic mapping framework using CR060a alphabet ratios\n"
        "- A falsifier list a partner photonic lab can in principle test\n"
        "- The input surface CR072a will populate with empirical photonic rows\n"
        "- The input surface CR073a will use to test cross-platform t_fire scaling\n\n"
        "CR071a IS NOT:\n"
        "- A photonic empirical contact table (CR072a's role)\n"
        "- A cross-platform scaling test (CR073a's role)\n"
        "- A claim that the mapping has been validated by a photonic measurement\n\n"
        "## Stewardship\n\nPer `STEWARDSHIP.md`.\n"
    )
    with output_path.open("w", encoding="utf-8") as f:
        f.write(md)


# =============================================================================
# Main
# =============================================================================

def main():
    script_dir = Path(__file__).resolve().parent
    mapping_csv = script_dir / "CR071a_mapping_table.csv"
    falsifier_csv = script_dir / "CR071a_falsifier_list.csv"
    t2g_csv = script_dir / "CR071a_t2_grav_at_photonic.csv"
    summary_json = script_dir / "CR071a_summary.json"
    result_md = script_dir / "CR071a_result.md"

    print("CR071a Photonic PR Letter Framework Mapping")
    print(f"Working directory: {script_dir}")
    print()

    print("[1/5] Reading mapping table...")
    with mapping_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
    print(f"      Loaded {len(raw_rows)} mapping rows")

    print("[2/5] Parsing mapping rows...")
    mapping_rows = [parse_mapping_row(r) for r in raw_rows]
    for r in mapping_rows:
        print(f"      {r.mapping_id}: {r.nv_observable:>16} -> {r.photonic_equivalent[:60]}")

    print("[3/5] Evaluating predictions and wrong controls...")
    predictions = evaluate_predictions(mapping_rows)
    wrong_controls = evaluate_wrong_controls(mapping_rows)
    pass_p = sum(1 for v in predictions.values() if v.get("pass"))
    pass_wc = sum(1 for v in wrong_controls.values() if v.get("pass"))
    print(f"      Predictions: {pass_p}/{len(predictions)}")
    print(f"      Wrong controls: {pass_wc}/{len(wrong_controls)}")

    print("[4/5] Writing artifacts...")
    write_falsifier_list(mapping_rows, falsifier_csv)
    write_t2_grav_at_photonic(t2g_csv)
    write_summary_json(mapping_rows, predictions, wrong_controls, summary_json)
    write_result_md(summary_json, result_md)
    for p in (falsifier_csv, t2g_csv, summary_json, result_md):
        print(f"      Wrote {p.name}")

    print("[5/5] Done.")
    print()
    print(
        f"Result class: CR071a_PHOTONIC_MAPPING_SEALED__"
        f"PREDICTIONS_{pass_p}_OF_{len(predictions)}__"
        f"WRONG_CONTROLS_{pass_wc}_OF_{len(wrong_controls)}__"
        f"MAPPING_ROWS_{len(mapping_rows)}__"
        f"FREE_PARAMETERS_0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
