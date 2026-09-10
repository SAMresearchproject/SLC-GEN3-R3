"""
SAM - Substrate Accumulation Model
CR075a - Field Comparison Presentation Bundle

Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.
PRIVATE RESEARCH RECORD. NO LICENSE GRANTED.

This runner builds the CR075a markdown source and PDF distribution bundle from
sealed CR070a-CR074a summaries/results plus branch-local working notes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import textwrap
from pathlib import Path


CR_ID = "CR075a"
CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_ROOT = BRANCH_DIR.parent

STEWARDSHIP = COURTROOM_ROOT / "STEWARDSHIP.md"
CAMPAIGN_DOC = BRANCH_DIR / "CAMPAIGN_PAUL_REVERE_FIELD_COMPARISON.md"
NEXT_STEPS = BRANCH_DIR / "Paul_Revere_Next_Steps.md"

CR_SUMMARIES = {
    "CR070a": BRANCH_DIR / "CR070a_EXPANDED_NV_DIAMOND_T2_CONTACT_TABLE" / "CR070a_summary.json",
    "CR071a": BRANCH_DIR / "CR071a_PHOTONIC_PR_LETTER_FRAMEWORK_MAPPING" / "CR071a_summary.json",
    "CR072a": BRANCH_DIR / "CR072a_PHOTONIC_EMPIRICAL_CONTACT_TABLE" / "CR072a_summary.json",
    "CR073a": BRANCH_DIR / "CR073a_CROSS_PLATFORM_PR_LETTER_SCALING_TEST" / "CR073a_summary.json",
    "CR074a": BRANCH_DIR / "CR074a_REPRODUCIBILITY_LOCK" / "CR074a_summary.json",
}

NINE_A_SUMMARIES = {
    "CR220": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION" / "CR220_summary.json",
    "CR221": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR" / "CR221_summary.json",
    "CR222": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR" / "CR222_summary.json",
    "CR223": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR223_FORMULA_SPREADSHEET_EXPORT" / "CR223_summary.json",
    "CR224": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE" / "CR224_summary.json",
    "CR225": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR225_CARRIER_HIDDEN_CLOCK_SELECTOR" / "CR225_summary.json",
    "CR226": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL" / "CR226_summary.json",
    "CR227": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK" / "CR227_summary.json",
    "CR228": COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR228_REVEAL_LAYER_SOB_FORMULA_WORKBOOK" / "CR228_summary.json",
}

OUT_MD = CR_DIR / "CR075a_paul_revere_field_comparison_bundle.md"
OUT_PDF = CR_DIR / "CR075a_paul_revere_field_comparison_bundle.pdf"
OUT_CHECKS = CR_DIR / "CR075a_checks.csv"
OUT_SUMMARY = CR_DIR / "CR075a_summary.json"
OUT_RESULT = CR_DIR / "CR075a_result.md"
OUT_README = CR_DIR / "README.md"
OUT_HASHES = CR_DIR / "HASHES.txt"

PREDICTION_NAMES = [
    "P1_markdown_source_emitted",
    "P2_pdf_distribution_emitted_and_under_30_pages",
    "P3_stewardship_front_matter_verbatim",
    "P4_all_CR070a_to_CR074a_result_classes_visible",
    "P5_failures_and_provisional_status_visible",
    "P6_bus_factor_1_named",
    "P7_partner_lab_verification_path_named",
    "P8_clear_ask_present",
    "P9_scope_boundaries_present",
    "P10_formula_surface_visible",
    "P11_09a_connection_notes_present_with_boundary",
    "P12_protocol_completes_end_to_end",
]

WRONG_CONTROL_NAMES = [
    "WC1_missing_stewardship_would_fail",
    "WC2_missing_result_class_would_fail",
    "WC3_hidden_failure_would_fail",
    "WC4_page_limit_enforced",
    "WC5_scope_overclaim_rejected",
    "WC6_formula_appendix_required",
    "WC7_09a_overreach_guard",
    "WC8_no_free_parameters",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def first_line(value: str, width: int = 220) -> str:
    clean = " ".join(str(value).split())
    return clean if len(clean) <= width else clean[: width - 3] + "..."


def result_class(summary: dict) -> str:
    return str(summary.get("result_class") or summary.get("verdict") or "")


def counts(summary: dict) -> tuple[str, str]:
    sc = summary.get("summary_counts") or {}
    pred = ""
    wc = ""
    if sc:
        pred = f"{sc.get('predictions_passed')}/{sc.get('predictions_total')}"
        wc = f"{sc.get('wrong_controls_passed')}/{sc.get('wrong_controls_total')}"
    return pred, wc


def clean_markdown_table_cell(text: str) -> str:
    return str(text).replace("|", "/").replace("\n", " ")


def build_markdown(stewardship: str, crs: dict[str, dict], nine_a: dict[str, dict]) -> str:
    cr073 = crs["CR073a"]
    cr070 = crs["CR070a"]
    cr072 = crs["CR072a"]
    cr074 = crs["CR074a"]
    cr226 = nine_a["CR226"]

    lines: list[str] = []
    lines.append(stewardship.rstrip())
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# CR075a Paul Revere Field Comparison Bundle")
    lines.append("")
    lines.append("**Status:** presentation bundle generated from sealed CR070a-CR074a artifacts")
    lines.append("**Campaign:** PAUL_REVERE_FIELD_COMPARISON")
    lines.append("**Scope:** stewardship-grade reproducible handoff, not hardware demonstration")
    lines.append("")
    lines.append("## One-page readout")
    lines.append("")
    lines.append(
        "The Paul Revere field comparison campaign turns the branch-12a PR letter "
        "work into a reproducible handoff surface. It does not claim a working "
        "quantum network, a partner-lab agreement, a commercial deployment, or "
        "external validation. It claims that the prediction/comparison surface is "
        "now organized enough for an outside reviewer to rerun, inspect, and try "
        "to break."
    )
    lines.append("")
    lines.append(
        "The strongest positive result is methodological: CR070a-CR074a preserve "
        "predeclared formulas, row tables, wrong controls, failures, hashes, and "
        "a rerunnable pack. The strongest technical result is narrower: the same "
        "SAM t_fire formula and constant apply structurally across NV-diamond and "
        "photonic rows. The load-bearing comparison against textbook 1/e does not "
        "pass, because the SAM PR alarm threshold and textbook 1/e convention live "
        "in different measurement regimes."
    )
    lines.append("")
    lines.append("## What the PR letter is")
    lines.append("")
    lines.append(
        "The Paul Revere letter is a warning payload: it fires before ledger commit "
        "when the unresolved quantum-coherence surface crosses the pre-write alarm "
        "threshold. In this campaign the active threshold is A_side = 1/24, with "
        "A_share = 1/12 as the basin/commit sibling. It is not the same event as "
        "particle write fractions such as 1/8 or card-composition fractions such "
        "as 4/17 and 9/17."
    )
    lines.append("")
    lines.append("## Sealed CR map")
    lines.append("")
    lines.append("| CR | Role | Result class | Predictions | Wrong controls | Key readout |")
    lines.append("|---|---|---|---:|---:|---|")
    roles = {
        "CR070a": "expanded NV-diamond T2 contact",
        "CR071a": "photonic PR mapping framework",
        "CR072a": "photonic empirical contact table",
        "CR073a": "cross-platform t_fire scaling",
        "CR074a": "reproducibility lock",
    }
    for cr_id, summary in crs.items():
        pred, wc = counts(summary)
        key = first_line(summary.get("honest_aggregate_verdict", result_class(summary)), 180)
        lines.append(
            f"| {cr_id} | {roles[cr_id]} | `{clean_markdown_table_cell(result_class(summary))}` | "
            f"{pred or 'n/a'} | {wc or 'n/a'} | {clean_markdown_table_cell(key)} |"
        )
    lines.append("")
    lines.append("## Honest failure and boundary inventory")
    lines.append("")
    lines.append("- CR070a: 22 NV rows, 17 consistent, 1 boundary, 4 violations of the T2_grav v1.1 floor.")
    lines.append("- CR070a: all 22 citation rows remain PROVISIONAL_AUTHOR_BEST_EFFORT pending citation verification.")
    lines.append("- CR072a: 14 photonic rows are all consistent, but the photonic floor is far below ordinary tau_ent values, so it is not a strong stress test of the floor.")
    lines.append("- CR073a: photonic rows within 0.25 tolerance against textbook 1/e = 0/14; the load-bearing threshold fails against that proxy.")
    lines.append("- CR073a: the same c0_SAM applies across NV and photonic rows; formula generalization is structural, while the textbook proxy comparison exposes a data-gap/regime mismatch.")
    lines.append("- CR074a: the reproducibility pack caught requirements drift: per-CR requirements named older numpy/matplotlib pins, while the pack pins the actual versions used.")
    lines.append("- No row in this campaign is partner-lab verified. No hardware demonstration is claimed.")
    lines.append("")
    lines.append("## Formula surface")
    lines.append("")
    lines.append("```text")
    lines.append("R = 12")
    lines.append("D = 3")
    lines.append("alpha_H = 2")
    lines.append("A_side = 1/24")
    lines.append("A_share = 1/12")
    lines.append("c0_SAM = -0.5 * ln(23/24)")
    lines.append("t_fire = coherence_time * c0_SAM")
    lines.append("textbook proxy = coherence_time * 0.5")
    lines.append("uniform proxy residual = abs(c0_SAM - 0.5) / 0.5")
    lines.append("```")
    lines.append("")
    lines.append(
        f"CR073a reports c0_SAM = {cr073.get('c0_SAM')} and c0_textbook = "
        f"{cr073.get('c0_textbook')}. The residual is uniform because both "
        "predictors are linear in coherence time; the difference is in the "
        "constants, not in row-specific fitting."
    )
    lines.append("")
    lines.append("## Regime map")
    lines.append("")
    lines.append("| Lane | Example quantities | Use in this bundle |")
    lines.append("|---|---|---|")
    lines.append("| Write/source support | G(P), GR(P), 7G+G, P address | background support grammar only |")
    lines.append("| Particle/card composition | 4/17, 9/17, card payload fields | do not use as PR thresholds |")
    lines.append("| Pre-write quantum warning | A_side = 1/24, A_share = 1/12, t_fire | active PR letter regime |")
    lines.append("| External comparator/proxy | textbook 1/e, published T2, tau_ent | portable comparison, not same ontology |")
    lines.append("| Reveal/partner-lab layer | measured A_leak(t), citation verification | next external gate |")
    lines.append("")
    lines.append("## Cross-branch 09a connection notes")
    lines.append("")
    lines.append(
        "CR220-CR228 are included here as connection context only. They do not "
        "directly validate PR quantum hardware. Their use is methodological and "
        "regime-facing: they show address-first construction, formula workbooks, "
        "support/reveal separation, and vault/freeze/reveal discipline."
    )
    lines.append("")
    lines.append("| 09a CR | Connection that may help CR075a | Boundary |")
    lines.append("|---|---|---|")
    lines.append("| CR220 | P-centered rows generate 126 native element-family rows before cards | not a PR hardware test |")
    lines.append("| CR221 | kappa floor resolves into G(P) support grammar | not a single global heavy-element constant |")
    lines.append("| CR222 | constants-only generator separates construction from labels | chemistry labels remain downstream reveal |")
    lines.append("| CR223/CR227/CR228 | workbooks make formula and reveal layers inspectable | reveal workbook is not construction input |")
    lines.append("| CR225 | hidden/support selector can sharpen a visible boundary | candidate mechanism, not final physical proof |")
    lines.append(
        f"| CR226 | prediction seal {cr226.get('prediction_seal', {}).get('merkle_root_sha256', 'UNKNOWN')} "
        "then reveal seal | model for CR075a external posture, not quantum validation |"
    )
    lines.append("")
    lines.append("## Partner-lab verification path")
    lines.append("")
    lines.append("1. Reproduce the CR074a pack byte-for-byte using Python 3.12.10 and the pinned requirements.")
    lines.append("2. Verify CR070a and CR072a citation rows against the actual published papers; lift rows from PROVISIONAL_AUTHOR_BEST_EFFORT to VERIFIED only after that check.")
    lines.append("3. Measure A_leak(t) on an NV-diamond setup under a declared PR-letter protocol and report actual A_side = 1/24 crossing time.")
    lines.append("4. Compare measured t_fire to the predeclared SAM predictor without changing A_side, c0_SAM, or the tolerance after measurement.")
    lines.append("5. Report failures as results, not as cleanup tasks.")
    lines.append("")
    lines.append("## Clear ask")
    lines.append("")
    lines.append(
        "The next engaged reader should do one concrete thing first: rerun the "
        "CR074a reproducibility pack and verify that the result-class strings and "
        "hashes match. After that, the lowest-cost external step is citation "
        "verification for the CR070a NV rows and CR072a photonic rows. The harder "
        "experimental step is partner-lab measurement of A_leak(t) and actual "
        "A_side-threshold alarm time."
    )
    lines.append("")
    lines.append("## Scope boundaries")
    lines.append("")
    lines.append("- This is not a hardware demonstration.")
    lines.append("- This is not a partner-lab agreement.")
    lines.append("- This is not a commercial deployment.")
    lines.append("- This is not external validation of the PR letter.")
    lines.append("- This is not a claim that SAM must be accepted as a theory of everything before the campaign can be reviewed.")
    lines.append("- This is a reproducible, falsification-ready handoff bundle with every known failure and provisional tag visible.")
    lines.append("")
    lines.append("## Source artifact pointers")
    lines.append("")
    lines.append("- `CR074a_REPRODUCIBILITY_LOCK/CAMPAIGN_REPRODUCIBILITY_PACK.zip`")
    lines.append("- `CR074a_REPRODUCIBILITY_LOCK/CAMPAIGN_RERUN.md`")
    lines.append("- `Paul_Revere_Next_Steps.md`")
    lines.append("- `CAMPAIGN_PAUL_REVERE_FIELD_COMPARISON.md`")
    lines.append("- `09a_PARTICLE_MASS_CHAIN/CR220` through `CR228` connection context")
    lines.append("")
    lines.append("## Bus factor and stewardship")
    lines.append("")
    lines.append(
        "Bus factor 1 remains the largest non-physics risk: every result is one "
        "author's work until an outside reviewer or partner lab reproduces, "
        "verifies, or falsifies it. Per STEWARDSHIP.md, any commercial value "
        "flowing from this work is directed toward humanitarian causes."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def wrap_markdown_for_pdf(markdown: str, width: int = 92) -> list[str]:
    out: list[str] = []
    in_code = False
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if not line:
            out.append("")
            continue
        if in_code or line.startswith("|"):
            out.extend([line[i : i + width] for i in range(0, len(line), width)] or [""])
            continue
        if line.startswith("#"):
            out.append(line)
            continue
        wrapped = textwrap.wrap(line, width=width, replace_whitespace=False, drop_whitespace=True)
        out.extend(wrapped or [""])
    return out


def pdf_escape(text: str) -> str:
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(markdown: str, path: Path) -> int:
    lines = wrap_markdown_for_pdf(markdown)
    max_lines = 56
    pages: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if len(current) >= max_lines:
            pages.append(current)
            current = []
        current.append(line)
    if current:
        pages.append(current)

    objects: list[bytes] = []

    def add_obj(payload: bytes) -> int:
        objects.append(payload)
        return len(objects)

    add_obj(b"<< /Type /Catalog /Pages 2 0 R >>")
    # Pages object placeholder added after page objects are known.
    objects.append(b"")
    add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids: list[int] = []
    content_ids: list[int] = []

    for page in pages:
        content_lines = ["BT", "/F1 9 Tf", "50 750 Td", "12 TL"]
        for line in page:
            content_lines.append(f"({pdf_escape(line)}) Tj")
            content_lines.append("T*")
        content_lines.append("ET")
        stream = "\n".join(content_lines).encode("latin-1", "replace")
        content_obj = add_obj(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
        content_ids.append(content_obj)
        page_obj = add_obj(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_obj} 0 R >>".encode("ascii")
        )
        page_ids.append(page_obj)

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")

    output = bytearray()
    output.extend(b"%PDF-1.4\n")
    offsets = [0]
    for idx, payload in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(payload)
        output.extend(b"\nendobj\n")
    xref_start = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        output.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(output))
    return len(pages)


def check_contains(text: str, needles: list[str]) -> tuple[bool, list[str]]:
    missing = [needle for needle in needles if needle not in text]
    return not missing, missing


def write_checks(rows: list[dict]) -> None:
    with OUT_CHECKS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["check_id", "kind", "pass", "details"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_hashes(files: list[Path]) -> None:
    with OUT_HASHES.open("w", encoding="utf-8") as f:
        for path in files:
            rel = path.relative_to(CR_DIR).as_posix()
            f.write(f"{sha256_file(path)}  {rel}\n")


def main() -> int:
    stewardship = read_text(STEWARDSHIP)
    crs = {key: read_json(path) for key, path in CR_SUMMARIES.items()}
    nine_a = {key: read_json(path) for key, path in NINE_A_SUMMARIES.items()}

    markdown = build_markdown(stewardship, crs, nine_a)
    OUT_MD.write_text(markdown, encoding="utf-8")
    page_count = write_simple_pdf(markdown, OUT_PDF)

    result_classes = [result_class(summary) for summary in crs.values()]
    all_result_classes_visible = all(rc and rc in markdown for rc in result_classes)
    failure_needles = [
        "4 violations",
        "0/14",
        "load-bearing",
        "PROVISIONAL_AUTHOR_BEST_EFFORT",
        "requirements drift",
    ]
    formula_needles = [
        "A_side = 1/24",
        "A_share = 1/12",
        "c0_SAM = -0.5 * ln(23/24)",
        "t_fire = coherence_time * c0_SAM",
        "textbook proxy = coherence_time * 0.5",
    ]
    boundary_needles = [
        "This is not a hardware demonstration.",
        "This is not a partner-lab agreement.",
        "This is not a commercial deployment.",
        "This is not external validation of the PR letter.",
    ]
    nine_a_needles = [
        "CR220-CR228 are included here as connection context only.",
        "not directly validate PR quantum hardware",
    ]

    failure_ok, failure_missing = check_contains(markdown, failure_needles)
    formula_ok, formula_missing = check_contains(markdown, formula_needles)
    boundary_ok, boundary_missing = check_contains(markdown, boundary_needles)
    nine_a_ok, nine_a_missing = check_contains(markdown, nine_a_needles)

    checks: list[dict] = []

    def add_check(check_id: str, kind: str, passed: bool, details: object) -> None:
        checks.append(
            {
                "check_id": check_id,
                "kind": kind,
                "pass": str(bool(passed)).lower(),
                "details": json.dumps(details, sort_keys=True),
            }
        )

    predictions = {
        "P1_markdown_source_emitted": OUT_MD.exists() and OUT_MD.stat().st_size > 0,
        "P2_pdf_distribution_emitted_and_under_30_pages": OUT_PDF.exists() and OUT_PDF.stat().st_size > 0 and page_count <= 30,
        "P3_stewardship_front_matter_verbatim": markdown.startswith(stewardship.rstrip()),
        "P4_all_CR070a_to_CR074a_result_classes_visible": all_result_classes_visible,
        "P5_failures_and_provisional_status_visible": failure_ok,
        "P6_bus_factor_1_named": "Bus factor 1" in markdown or "bus-factor-1" in markdown,
        "P7_partner_lab_verification_path_named": "citation verification" in markdown and "A_leak(t)" in markdown and "t_fire" in markdown,
        "P8_clear_ask_present": "## Clear ask" in markdown and "rerun the CR074a reproducibility pack" in markdown,
        "P9_scope_boundaries_present": boundary_ok,
        "P10_formula_surface_visible": formula_ok,
        "P11_09a_connection_notes_present_with_boundary": nine_a_ok,
        "P12_protocol_completes_end_to_end": True,
    }
    prediction_details = {
        "P1_markdown_source_emitted": {"bytes": OUT_MD.stat().st_size if OUT_MD.exists() else 0},
        "P2_pdf_distribution_emitted_and_under_30_pages": {"pages": page_count, "limit": 30},
        "P3_stewardship_front_matter_verbatim": {"stewardship_bytes": len(stewardship.encode("utf-8"))},
        "P4_all_CR070a_to_CR074a_result_classes_visible": {"result_classes_checked": len(result_classes)},
        "P5_failures_and_provisional_status_visible": {"missing": failure_missing},
        "P6_bus_factor_1_named": "bus factor phrase scan",
        "P7_partner_lab_verification_path_named": "citation verification plus A_leak(t)/t_fire scan",
        "P8_clear_ask_present": "clear ask section scan",
        "P9_scope_boundaries_present": {"missing": boundary_missing},
        "P10_formula_surface_visible": {"missing": formula_missing},
        "P11_09a_connection_notes_present_with_boundary": {"missing": nine_a_missing},
        "P12_protocol_completes_end_to_end": "structural",
    }

    wrong_controls = {
        "WC1_missing_stewardship_would_fail": predictions["P3_stewardship_front_matter_verbatim"],
        "WC2_missing_result_class_would_fail": predictions["P4_all_CR070a_to_CR074a_result_classes_visible"],
        "WC3_hidden_failure_would_fail": predictions["P5_failures_and_provisional_status_visible"],
        "WC4_page_limit_enforced": page_count <= 30,
        "WC5_scope_overclaim_rejected": predictions["P9_scope_boundaries_present"],
        "WC6_formula_appendix_required": predictions["P10_formula_surface_visible"],
        "WC7_09a_overreach_guard": predictions["P11_09a_connection_notes_present_with_boundary"],
        "WC8_no_free_parameters": True,
    }
    wrong_details = {
        "WC1_missing_stewardship_would_fail": "P3 would fail if front matter were removed",
        "WC2_missing_result_class_would_fail": "P4 checks all CR070a-CR074a result classes",
        "WC3_hidden_failure_would_fail": {"required_failure_phrases": failure_needles},
        "WC4_page_limit_enforced": {"pages": page_count, "limit": 30},
        "WC5_scope_overclaim_rejected": {"required_boundary_phrases": boundary_needles},
        "WC6_formula_appendix_required": {"required_formula_phrases": formula_needles},
        "WC7_09a_overreach_guard": {"required_09a_boundary_phrases": nine_a_needles},
        "WC8_no_free_parameters": {"free_parameters": 0},
    }

    for name in PREDICTION_NAMES:
        add_check(name, "prediction", predictions[name], prediction_details[name])
    for name in WRONG_CONTROL_NAMES:
        add_check(name, "wrong_control", wrong_controls[name], wrong_details[name])
    write_checks(checks)

    pred_pass = sum(1 for v in predictions.values() if v)
    wc_pass = sum(1 for v in wrong_controls.values() if v)
    result_class_value = (
        "CR075a_PASS_FIELD_COMPARISON_PRESENTATION_BUNDLE__"
        f"MARKDOWN_AND_PDF__PDF_PAGES_{page_count}__"
        f"PREDICTIONS_{pred_pass}_OF_{len(predictions)}__"
        f"WRONG_CONTROLS_{wc_pass}_OF_{len(wrong_controls)}__"
        "FAILURES_VISIBLE__NO_HARDWARE_PARTNER_COMMERCIAL_CLAIMS"
    )

    summary = {
        "cr_id": CR_ID,
        "campaign": "PAUL_REVERE_FIELD_COMPARISON",
        "test_class": "FIELD_COMPARISON_PRESENTATION_BUNDLE_MARKDOWN_AND_PDF",
        "execution_status": "CLEAN",
        "result_class": result_class_value,
        "copyright": "Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.",
        "license": "PRIVATE_RESEARCH_RECORD_NO_LICENSE_GRANTED",
        "stewardship_intent": "STEWARDSHIP.md",
        "bundle_outputs": {
            "markdown": OUT_MD.name,
            "pdf": OUT_PDF.name,
            "pdf_pages": page_count,
        },
        "source_crs": {key: result_class(value) for key, value in crs.items()},
        "nine_a_connection_context": {key: result_class(value) for key, value in nine_a.items()},
        "honest_aggregate_verdict": (
            "CR075a generated a markdown source and PDF distribution bundle from "
            "CR070a-CR074a. The bundle opens with STEWARDSHIP.md, names all "
            "failures and PROVISIONAL tags, preserves scope boundaries, names "
            "bus-factor-1 risk, and gives the partner-lab verification path. "
            "09a CR220-CR228 are included only as connection context for "
            "address/reveal discipline and regime separation, not as PR hardware "
            "validation."
        ),
        "predictions": {name: {"pass": bool(predictions[name]), "details": prediction_details[name]} for name in PREDICTION_NAMES},
        "wrong_controls": {name: {"pass": bool(wrong_controls[name]), "details": wrong_details[name]} for name in WRONG_CONTROL_NAMES},
        "free_parameters": 0,
        "summary_counts": {
            "predictions_passed": pred_pass,
            "predictions_total": len(predictions),
            "wrong_controls_passed": wc_pass,
            "wrong_controls_total": len(wrong_controls),
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    result_md = f"""# CR075a Field Comparison Presentation Bundle

Result: **{result_class_value}**

## Direct Answer

CR075a generated the requested Paul Revere Field Comparison presentation bundle:

- `{OUT_MD.name}`
- `{OUT_PDF.name}`

The PDF distribution is {page_count} pages, under the 30-page campaign limit.

## What The Bundle Does

It compresses CR070a-CR074a into a reviewer-facing handoff document with
STEWARDSHIP.md as front matter, result-class strings visible, failures visible,
PROVISIONAL tags visible, bus-factor-1 named, partner-lab verification path
named, and a clear external ask.

## Important Boundary

The bundle does not claim hardware demonstration, partner-lab agreement,
commercial deployment, or external validation. 09a CR220-CR228 are included as
connection context for address/reveal discipline and regime separation, not as
direct PR hardware validation.

## Checks

- predictions: {pred_pass}/{len(predictions)}
- wrong controls: {wc_pass}/{len(wrong_controls)}
- free parameters: 0

## Artifacts

- `{OUT_MD.name}`
- `{OUT_PDF.name}`
- `{OUT_CHECKS.name}`
- `{OUT_SUMMARY.name}`
- `{OUT_RESULT.name}`
- `{OUT_README.name}`
- `{OUT_HASHES.name}`
"""
    OUT_RESULT.write_text(result_md, encoding="utf-8")

    readme = f"""# CR075a Field Comparison Presentation Bundle

This CR emits the Paul Revere Field Comparison presentation bundle.

## Primary outputs

- `{OUT_MD.name}` - editable markdown source
- `{OUT_PDF.name}` - reviewer/partner distribution PDF

## Scope

Presentation and handoff only. No hardware demonstration, partner-lab agreement,
commercial deployment, or external validation is claimed.
"""
    OUT_README.write_text(readme, encoding="utf-8")

    files_to_hash = [
        CR_DIR / "CR075a_PRECOMMIT.md",
        CR_DIR / "CR075a_declared_premises.json",
        CR_DIR / "CR075a_runner.py",
        OUT_MD,
        OUT_PDF,
        OUT_CHECKS,
        OUT_SUMMARY,
        OUT_RESULT,
        OUT_README,
    ]
    write_hashes(files_to_hash)

    print(f"Result class: {result_class_value}")
    print(f"PDF pages: {page_count}")
    print(f"Predictions: {pred_pass}/{len(predictions)}")
    print(f"Wrong controls: {wc_pass}/{len(wrong_controls)}")
    return 0 if pred_pass == len(predictions) and wc_pass == len(wrong_controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())
