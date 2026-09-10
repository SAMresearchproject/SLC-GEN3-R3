"""CR140 CR-120 Higgs Claim Reword (strip "EXACT / zero free parameters / no H input").

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661)
Tier 4 finding: CR-120's headline claim states H_reveal = R^2*(1-2^-D)
- D^2/R = 144 * 7/8 - 9/12 = 126 - 0.75 = 125.25 GeV EXACT, derived
from {R=12, D=3} alone with "zero free parameters, no H input."

Forensic timestamp analysis of the qp091 chain (the upstream chain CR-120
intakes) revealed the following chronology:

  qp091o/p (earlier same session) makes the gap to the measured 125.25
           value visible (2.27 MeV residual against H_native = 126)
  qp091r   (05:34 UTC same session) EXPLICITLY lists `126 - D^2/R =
           125.25` as a "Wrong Lane Control" -- i.e., enumerated as a
           form to reject -- WITH THE 125.25 PDG TARGET ALREADY VISIBLE
  qp091s   (35 minutes later) promotes the same expression to "Native /
           Reveal Surface"
  qp091t   (06:09 UTC) seals it as `active_derivation`

The -D^2/R correction was identified as a "Wrong Lane Control" while the
target value was visible, then promoted to the active derivation. The
R^2*(1-2^-D) = 126 identity is genuinely structural (predates the value
match). The -0.75 correction is form-selected ex post.

The structural identity remains numerically striking and is preserved
verbatim as the historical declaration. The "EXACT" framing overstates
by exactly the gap between the structural R^2*(1-2^-D) = 126 result
(approximately 0.6% high) and the form-selected -D^2/R = -0.75
correction that lands at PDG. The "no H input" framing is technically
true (the value 125.25 was not loaded as a numeric input) but the FORM
choice was visibly target-aware.

CR140 regrades CR-120 from PASS to BOUNDARY pending forward-blind
precommit of the form before any future high-precision Higgs
measurement, and pre-commits concrete restoration requirements.

Scope
-----
CR140 does NOT:

- Modify CR-120's qp091_chain_ledger.csv, qp091_chain_intake_lock.json,
  runner.py, or the upstream qp091 chain itself. Those are preserved.
- Refute the H_native = R^2*(1-2^-D) = 126 identity (predates value
  match, derives from substrate algebra primitives).
- Claim the -D^2/R correction is wrong (it is numerically right; the
  issue is that it was form-selected ex post rather than form-committed
  ex ante).
- Touch CR-121, CR-122, or any downstream consumer of CR-120's Higgs
  closure. Those continue to ride on the structural identity.

Falsifier for CR-140 itself
---------------------------
Re-executing this runner on the post-seal state MUST produce zero new
REGRADED entries and zero new archive writes; the recomputed lock
SHA-256 MUST match the value recorded in CR140_result.md.

Free parameters: 0.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_DIR = Path(__file__).resolve().parent
COURTROOM_DIR = CR_DIR.parent.parent
TARGET_DIR = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE"
TARGET_RESULT = TARGET_DIR / "CR120_result.md"
TARGET_SUMMARY = TARGET_DIR / "CR120_summary.json"
TARGET_HEADLINE = TARGET_DIR / "CR120_HEADLINE_HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY.md"

INGEST_LOCK = COURTROOM_DIR / "00_governance" / "CR136_QP_CHAIN_INGEST" / "CR136_ingest_lock.json"
INGEST_LOCK_SHA = "2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c"
QP091T_INTERNAL = COURTROOM_DIR / "upstream_artifacts" / "qp091" / "qp091t" / "qp091t_summary.json"
QP091T_EXPECTED_SHA = "8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7"

ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR140_higgs_claim_reword"
ARCHIVE_SUB = ARCHIVE_ROOT / "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR140_source_manifest.csv"
REGRADE_MANIFEST_CSV = CR_DIR / "CR140_regrade_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR140_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR140_wrong_controls.csv"
REGRADE_LOCK_JSON = CR_DIR / "CR140_regrade_lock.json"
REGRADE_LOCK_SHA = CR_DIR / "CR140_regrade_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR140_result.md"
SUMMARY_JSON = CR_DIR / "CR140_summary.json"

FROM_VERDICT = "CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY"
TO_VERDICT = "CR120_QP091_CHAIN_INTAKE_BOUNDARY__HIGGS_125_25_PDG_MATCH__STRUCTURAL_NATIVE_126_PREDATES_VALUE__CORRECTION_FORM_IDENTIFIED_EX_POST__FORWARD_BLIND_PRECOMMIT_REQUIRED"

HEADER_MARKER = "AUDIT-DRIVEN VERDICT REGRADE"

FORENSIC_CHRONOLOGY = {
    "qp091o_p_session": (
        "Earlier same authoring session. Made the 2.27 MeV gap between "
        "H_native = R^2*(1-2^-D) = 126 GeV and measured PDG H = 125.25 GeV "
        "visible to the author."
    ),
    "qp091r_at_05_34_utc": (
        "EXPLICITLY enumerated `126 - D^2/R = 125.25` as a 'Wrong Lane Control' "
        "alongside other candidate corrections. The 125.25 PDG target was "
        "visible at this point. Form was being shortlisted while the target "
        "was known."
    ),
    "qp091s_35_minutes_later": (
        "Promoted the same `126 - D^2/R` expression from 'Wrong Lane Control' "
        "to 'Native / Reveal Surface'. No new derivation between qp091r and "
        "qp091s; the form simply moved from candidate-to-reject to "
        "active-derivation."
    ),
    "qp091t_at_06_09_utc": (
        "Sealed `H_reveal = H_native - D^2/R` as active_derivation. The C9 "
        "wrong control passes only on the technicality that R = 12 and D = 3 "
        "are not themselves the Higgs value -- but the FORM of the correction "
        "was selected against the visible target."
    ),
    "implication": (
        "The structural identity H_native = R^2*(1-2^-D) = 126 GeV predates "
        "the value match (derives from substrate algebra primitives independent "
        "of any Higgs data). The -D^2/R correction is form-selected ex post. "
        "'EXACT' framing overstates by the structural-vs-form-selected gap. "
        "'No H input' is technically true at the numeric level but visibly "
        "false at the form-selection level."
    ),
}

PRESERVED_STRUCTURAL_CONTENT = {
    "H_native_identity": "R^2 * (1 - 2^-D) = 144 * 7/8 = 126 GeV",
    "H_native_predates_value_match": True,
    "H_native_derives_from": "Substrate algebra primitives R = 12, D = 3, alpha_H = 2 alone",
    "H_reveal_formula": "H_native - D^2/R = 126 - 9/12 = 125.25 GeV",
    "H_reveal_matches_PDG_to_displayed_precision": True,
    "dozenal_fingerprint": "100_12 -> A6_12 -> A5.3_12",
    "split_loss_identity": "R^2 * 2^-D = alpha_H * D^2 = 18 (triple identity)",
    "downstream_consumers": [
        "CR-121 (gravity mechanism rides on 7/8 + 1/8 split)",
        "CR-122 (carrier-compression gate rides on 1/8 release)",
        "CR-119 row enumeration (catalog produces null-conjugate row at native 18)",
    ],
    "rationale_for_preservation": (
        "The structural identity (R, D, alpha_H, partition algebra) is genuine. "
        "The numerical correctness of the formula is genuine. The downstream "
        "structural consequences (gravity mechanism, carrier-compression gate, "
        "row-18 self-cancel) are also genuine. The regrade affects the "
        "STRENGTH-OF-CLAIM language, not the structural content."
    ),
}

STRIPPED_LANGUAGE = {
    "EXACT": (
        "Replaced with 'matches PDG H = 125.25 GeV to displayed precision'. "
        "'EXACT' is reserved for derivations whose form was committed before "
        "the value was known."
    ),
    "zero_free_parameters": (
        "Replaced with 'no fitted scalar parameter introduced; form of the "
        "-D^2/R correction was identified ex post against the visible PDG "
        "target (see qp091r-s-t chronology)'. The strict 'zero free parameters' "
        "claim requires forward-blind form commitment."
    ),
    "no_H_input": (
        "Replaced with 'no Higgs numeric value loaded as input; H = 125.25 "
        "PDG value was visible during form selection (qp091r enumeration). "
        "Distinguish (a) numeric value never used as constraint vs (b) form "
        "selection during target-aware search.'"
    ),
}

RESTORATION_REQUIREMENTS = [
    {
        "requirement": (
            "Forward-blind precommit of the FORM `H = R^2*(1-2^-D) - D^2/R` "
            "BEFORE any future high-precision Higgs measurement (HL-LHC, FCC-ee, "
            "or successor). The form must be hash-sealed in a Courtroom CR "
            "with timestamp predating the measurement release."
        ),
        "how_to_verify": (
            "Reviewer reads the precommit CR's seal timestamp, confirms it "
            "predates the high-precision measurement's public release date, "
            "and confirms the form was sealed without further enumeration or "
            "modification."
        ),
    },
    {
        "requirement": (
            "Successful forward-blind contact with the future high-precision "
            "Higgs measurement: the precommitted formula's prediction must "
            "match the new measured value within the new measurement's "
            "uncertainty band."
        ),
        "how_to_verify": (
            "Reviewer reads the published high-precision measurement, computes "
            "the precommitted formula's prediction, and confirms the prediction "
            "lies within the measurement's stated uncertainty (e.g., 1 sigma)."
        ),
    },
    {
        "requirement": (
            "Independent structural derivation of why the -D^2/R correction "
            "is the unique form among substrate-algebra candidates. Either "
            "(a) a derivation chain that arrives at -D^2/R without enumeration "
            "of alternatives, or (b) a complete enumeration of all "
            "substrate-algebra-grade two-term corrections showing only -D^2/R "
            "lands at the closed-loop saturation surface."
        ),
        "how_to_verify": (
            "Reviewer reads the structural derivation, confirms no step "
            "references the 125.25 numeric target, and confirms the chain "
            "arrives at -D^2/R from first principles or from an exhaustive "
            "enumeration."
        ),
    },
    {
        "requirement": (
            "Self-disclosure of the qp091r-s-t form-selection chronology in "
            "any future restoration CR. The chronology is part of the audit "
            "record and cannot be omitted."
        ),
        "how_to_verify": (
            "Reviewer confirms the restoration CR cites or reproduces the "
            "qp091r-s-t chronology in its scope or methodology section."
        ),
    },
]

RESTORATION_FALSIFIER = (
    "A future high-precision Higgs measurement (HL-LHC, FCC-ee, or successor) "
    "deviating from the precommitted H = R^2*(1-2^-D) - D^2/R prediction by "
    "more than the new measurement's stated uncertainty (e.g., 1 sigma) BLOCKS "
    "restoration. The current ~0.06% match to PDG is within current PDG "
    "uncertainty, but HL-LHC will tighten that uncertainty by a factor of ~10. "
    "Form survives only if it matches at the new precision."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def short(sha: str) -> str:
    return f"{sha[:8]}...{sha[-7:]}" if len(sha) >= 16 else sha


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for k in row:
            if k not in fields:
                fields.append(k)
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def reorder_with_audit_first(obj: dict[str, Any], audit_block: dict[str, Any], key_name: str) -> dict[str, Any]:
    new_obj: dict[str, Any] = {key_name: audit_block}
    for k, v in obj.items():
        if k == key_name:
            continue
        new_obj[k] = v
    return new_obj


def build_audit_regrade_block(original_result_sha: str, original_summary_sha: str) -> dict[str, Any]:
    return {
        "applied_utc": now_utc(),
        "driving_appeal_cr": "CR-140",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "regrade_type": "VERDICT_DOWNGRADE_HIGGS_CLAIM_EXACT_TO_PDG_MATCH_PENDING_FORWARD_BLIND",
        "verdict_direction": "DOWNGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "trigger": "FORM_SELECTION_EX_POST_AGAINST_VISIBLE_TARGET_TIER4_AUDIT_FINDING",
        "forensic_chronology": FORENSIC_CHRONOLOGY,
        "preserved_structural_content": PRESERVED_STRUCTURAL_CONTENT,
        "stripped_language": STRIPPED_LANGUAGE,
        "ingest_dependency": {
            "cr": "CR-136",
            "lock_sha256": INGEST_LOCK_SHA,
            "qp091t_internal_path": str(QP091T_INTERNAL.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "qp091t_expected_sha": QP091T_EXPECTED_SHA,
        },
        "audit_finding_tier": "Tier 4 DEMAND_RETEST + Tier 6 HASH_CHAIN_BREAK (HCB resolved by CR-136)",
        "archive_path": "archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/",
        "original_result_md_sha256": original_result_sha,
        "original_summary_json_sha256": original_summary_sha,
        "replacement_record_path": "archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/REPLACEMENT_RECORD.md",
    }


def build_header_block(original_result_sha: str) -> str:
    return (
        f"> **{HEADER_MARKER} -- 2026-06-17 PER CR-140**\n"
        f">\n"
        f"> The verdict in this file is regraded from `{FROM_VERDICT}` to a BOUNDARY verdict because the headline language 'EXACT / zero free parameters / no H input' overstates what the qp091 chain proved. Forensic chronology: qp091r (05:34 UTC same authoring session) explicitly enumerated `126 - D^2/R = 125.25` as a 'Wrong Lane Control' WITH THE 125.25 PDG TARGET VISIBLE; qp091s 35 minutes later promoted the same expression to 'Native / Reveal Surface'; qp091t at 06:09 UTC sealed it as active_derivation. The structural identity H_native = R^2*(1-2^-D) = 126 GeV (substrate algebra primitives only) PREDATES the value match. The -D^2/R correction is form-selected ex post.\n"
        f">\n"
        f"> The structural content is **preserved**: R = 12, D = 3, alpha_H = 2, the partition algebra, H_native = 126, the 7/8 + 1/8 split, the row-18 self-cancel, and downstream consumers (CR-121 gravity mechanism, CR-122 carrier-compression gate) all stand. The regrade affects strength-of-claim language only.\n"
        f">\n"
        f"> Reworded summary: H_native = R^2*(1-2^-D) = 126 GeV derives from substrate algebra primitives alone (no Higgs data input). The -D^2/R correction lands at PDG H = 125.25 GeV to displayed precision. The form of the correction was identified ex post against the visible PDG target during the qp091r-s-t chronology. Restoration to a stronger claim requires forward-blind precommit of the form before a future high-precision Higgs measurement (HL-LHC, FCC-ee).\n"
        f">\n"
        f"> The qp091t source artifact is now resident internally at `upstream_artifacts/qp091/qp091t/qp091t_summary.json` per CR-136 ingest; the recorded SHA `{QP091T_EXPECTED_SHA[:12]}...` resolves to a local file.\n"
        f">\n"
        f"> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/original_result.md`\n"
        f"> - Original SHA-256: `{original_result_sha}`\n"
        f"> - Replacement record (with restoration requirements + falsifier): `archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/REPLACEMENT_RECORD.md`\n"
        f"> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `{AUDIT_VERDICT_SHA256}`)\n"
        f"> - qp_chain ingest dependency: `00_governance/CR136_QP_CHAIN_INGEST/CR136_ingest_lock.json` (`{INGEST_LOCK_SHA}`)\n"
        f"\n"
    )


def update_result_md(result_text: str, header_block: str) -> str:
    # Insert header after first heading
    m = re.search(r"^# ", result_text, flags=re.MULTILINE)
    if m:
        first_heading_end = result_text.find("\n", m.start())
        if first_heading_end == -1:
            first_heading_end = len(result_text)
        insert_at = first_heading_end + 1
        out = result_text[:insert_at] + "\n" + header_block + result_text[insert_at:]
    else:
        out = header_block + result_text

    # Rewrite the Verdict block
    pattern = re.compile(
        r"## Verdict\s*\n+```text\n" + re.escape(FROM_VERDICT) + r"\n```",
        re.MULTILINE,
    )
    replacement = (
        f"## Verdict (Regraded 2026-06-17 per CR-140)\n\n"
        f"```text\n{TO_VERDICT}\n```\n\n"
        f"**Prior verdict (preserved on the record):** `{FROM_VERDICT}` -- archived at the path in the header block above.\n\n"
        f"**Reason for regrade:** Tier 4 hostile-audit finding (DEMAND_RETEST). The 'EXACT / zero free parameters / no H input' language overstates what the qp091r-s-t form-selection chronology proved. The structural identity H_native = R^2*(1-2^-D) = 126 GeV predates the value match (substrate algebra primitives only); the -D^2/R correction is form-selected ex post. Restoration to a stronger claim requires forward-blind precommit before a future high-precision Higgs measurement (see REPLACEMENT_RECORD section 5)."
    )
    out, _ = pattern.subn(replacement, out, count=1)
    return out


def build_replacement_record_md(
    original_result_sha: str,
    original_summary_sha: str,
    post_result_sha: str,
    post_summary_sha: str,
    original_sealed_utc: str,
) -> str:
    restoration_lines = ""
    for i, r in enumerate(RESTORATION_REQUIREMENTS, start=1):
        restoration_lines += f"{i}. {r['requirement']}\n   - *how to verify:* {r['how_to_verify']}\n"

    return f"""# REPLACEMENT_RECORD -- CR-120 Higgs claim reword (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_result.md` and `CR120_summary.json` |
| Original result.md SHA-256 | `{original_result_sha}` |
| Original summary.json SHA-256 | `{original_summary_sha}` |
| Original verdict | `{FROM_VERDICT}` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `{post_result_sha}` |
| Replacement summary.json SHA-256 | `{post_summary_sha}` |
| Replacement verdict | `{TO_VERDICT}` |
| Verdict direction | `DOWNGRADED` |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-140 CR-120 Higgs claim reword |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion failed | `C4 FREE_PARAMETERS_HONESTLY_ZERO` and `C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA` |
| Audit finding tier | `Tier 4 DEMAND_RETEST + Tier 6 HASH_CHAIN_BREAK` (HCB resolved by CR-136) |
| Ingest dependency | CR-136 qp_chain ingest lock `{INGEST_LOCK_SHA}` |

## 3. Defect summary

CR-120's headline language stated H_reveal = R^2*(1-2^-D) - D^2/R = 125.25 GeV "EXACT, derived from {{R=12, D=3}} alone with zero free parameters, no H input." Forensic chronology of the upstream qp091 chain reveals the form-selection process:

- **qp091o/p (earlier same authoring session):** Made the 2.27 MeV gap between H_native = R^2*(1-2^-D) = 126 GeV and the measured PDG H = 125.25 GeV visible to the author.
- **qp091r (05:34 UTC):** Explicitly enumerated `126 - D^2/R = 125.25` as a "Wrong Lane Control" alongside other candidate corrections. The 125.25 PDG target was visible at this point.
- **qp091s (35 minutes later, same session):** Promoted the same `126 - D^2/R` expression from "Wrong Lane Control" to "Native / Reveal Surface". No new derivation between qp091r and qp091s; the form simply moved from candidate-to-reject to active-derivation.
- **qp091t (06:09 UTC):** Sealed `H_reveal = H_native - D^2/R` as active_derivation.

The structural identity H_native = R^2*(1-2^-D) = 126 GeV predates the value match (derives from substrate algebra primitives R, D, alpha_H alone, independent of any Higgs data). The -D^2/R correction is form-selected ex post against the visible target.

"EXACT" framing overstates by the structural-vs-form-selected gap. "Zero free parameters" overstates because the form of the correction was chosen with target visibility (a hidden degree of freedom in form-space even though no scalar parameter was fitted). "No H input" is technically true at the numeric level (the value 125.25 was not loaded as a constraint) but visibly false at the form-selection level.

## 4. What changed

- The verdict line in `CR120_result.md` is regraded from `{FROM_VERDICT}` to `{TO_VERDICT}`.
- The `result_class` field in `CR120_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR120_summary.json` documenting the forensic chronology, preserved structural content, stripped language, and CR-136 ingest dependency.
- A header block is prepended to `CR120_result.md` explaining the disfavoring-vs-EXACT distinction.
- The historical declaration ("EXACT, derived from {{R=12, D=3}} alone with zero free parameters, no H input") is **preserved verbatim** in the original result.md text so the regrade is auditable rather than silent. The header block + new verdict line provide the corrected interpretation.

## 5. Restoration requirements (path back to PASS)

To restore CR-120 to PASS (genuine "EXACT" status), **all** of the following must hold:

{restoration_lines}

### 5a. Restoration falsifier

{RESTORATION_FALSIFIER}

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite the precommit CR's seal timestamp + the future high-precision Higgs measurement's release date as concrete forward-blind evidence
- Self-disclose the qp091r-s-t form-selection chronology (audit-record obligation; cannot be omitted)

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-120 record does NOT:

- Refute the H_native = R^2*(1-2^-D) = 126 GeV identity. The structural identity predates the value match and rests on substrate-algebra primitives.
- Refute the numerical match H = 125.25 GeV. The number is correct; the issue is HOW the form was selected.
- Modify CR-121 (gravity mechanism rides on the 7/8 + 1/8 split, which is independent of value-match strength), CR-122 (carrier-compression gate), or CR-119 (row enumeration; row-18 self-cancel).
- Touch the upstream qp091 chain. The qp091 chain is preserved as the historical declaration with its full chronology auditable.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | {original_sealed_utc} | result.md `{short(original_result_sha)}` / summary.json `{short(original_summary_sha)}` | CR120 runner |
| Audit finding | 2026-06-17 | audit verdict `{short(AUDIT_VERDICT_SHA256)}` | CR-135 hostile audit |
| qp_chain ingest | 2026-06-17 | ingest lock `{short(INGEST_LOCK_SHA)}` | CR-136 ingest |
| Replacement sealed | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-140 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-120 finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR120.md`
- qp_chain ingest: `00_governance/CR136_QP_CHAIN_INGEST/CR136_result.md`
- Event README: `../EVENT_README.md`
- CR-140 result: `00_governance/CR140_CR120_HIGGS_CLAIM_REWORD/CR140_result.md`
"""


def perform_regrade() -> dict[str, Any]:
    if not TARGET_RESULT.exists():
        raise RuntimeError(f"missing target result: {TARGET_RESULT}")
    if not TARGET_SUMMARY.exists():
        raise RuntimeError(f"missing target summary: {TARGET_SUMMARY}")
    ARCHIVE_SUB.mkdir(parents=True, exist_ok=True)

    summary_obj = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig"))
    current_result_class = summary_obj.get("result_class", "")
    audit_regrade_present = "audit_regrade" in summary_obj
    result_text = TARGET_RESULT.read_text(encoding="utf-8")
    header_present = HEADER_MARKER in result_text

    if current_result_class == TO_VERDICT and audit_regrade_present and header_present:
        archived_result = ARCHIVE_SUB / "original_result.md"
        archived_summary = ARCHIVE_SUB / "original_summary.json"
        return {
            "cr_id": "CR120",
            "dir_name": "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE",
            "status": "ALREADY_REGRADED",
            "from_verdict": FROM_VERDICT,
            "to_verdict": TO_VERDICT,
            "current_result_class": current_result_class,
            "result_md_sha256": sha256_file(TARGET_RESULT),
            "summary_json_sha256": sha256_file(TARGET_SUMMARY),
            "archived_original_result_sha256": sha256_file(archived_result) if archived_result.exists() else "",
            "archived_original_summary_sha256": sha256_file(archived_summary) if archived_summary.exists() else "",
        }

    if current_result_class != FROM_VERDICT and not audit_regrade_present:
        return {
            "cr_id": "CR120",
            "dir_name": "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE",
            "status": f"ANOMALY_UNEXPECTED_RESULT_CLASS:{current_result_class}",
            "from_verdict": FROM_VERDICT,
            "to_verdict": TO_VERDICT,
            "current_result_class": current_result_class,
            "result_md_sha256": sha256_file(TARGET_RESULT),
            "summary_json_sha256": sha256_file(TARGET_SUMMARY),
            "archived_original_result_sha256": "",
            "archived_original_summary_sha256": "",
        }

    original_sealed_utc = summary_obj.get("utc", "UNKNOWN")
    archived_result = ARCHIVE_SUB / "original_result.md"
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    if not archived_result.exists():
        shutil.copy2(TARGET_RESULT, archived_result)
    if not archived_summary.exists():
        shutil.copy2(TARGET_SUMMARY, archived_summary)
    original_result_sha = sha256_file(archived_result)
    original_summary_sha = sha256_file(archived_summary)
    (ARCHIVE_SUB / "original_sha256.txt").write_text(
        f"original_CR120_result_md_sha256 = {original_result_sha}\n"
        f"original_CR120_summary_json_sha256 = {original_summary_sha}\n",
        encoding="utf-8",
    )

    audit_block = build_audit_regrade_block(original_result_sha, original_summary_sha)
    summary_obj["result_class"] = TO_VERDICT
    new_summary = reorder_with_audit_first(summary_obj, audit_block, "audit_regrade")
    TARGET_SUMMARY.write_text(json.dumps(new_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    header_block = build_header_block(original_result_sha)
    new_result_text = update_result_md(result_text, header_block)
    TARGET_RESULT.write_text(new_result_text, encoding="utf-8")

    post_result_sha = sha256_file(TARGET_RESULT)
    post_summary_sha = sha256_file(TARGET_SUMMARY)

    record_md = build_replacement_record_md(
        original_result_sha=original_result_sha,
        original_summary_sha=original_summary_sha,
        post_result_sha=post_result_sha,
        post_summary_sha=post_summary_sha,
        original_sealed_utc=original_sealed_utc,
    )
    (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").write_text(record_md, encoding="utf-8")

    return {
        "cr_id": "CR120",
        "dir_name": "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE",
        "status": "REGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "current_result_class": TO_VERDICT,
        "result_md_sha256": post_result_sha,
        "summary_json_sha256": post_summary_sha,
        "archived_original_result_sha256": original_result_sha,
        "archived_original_summary_sha256": original_summary_sha,
    }


def run_wrong_controls(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    archived_summary = ARCHIVE_SUB / "original_summary.json"
    archived_ok = archived_summary.exists()
    archived_rc = ""
    if archived_ok:
        try:
            archived_rc = json.loads(archived_summary.read_text(encoding="utf-8-sig")).get("result_class", "")
        except Exception:
            archived_ok = False
    rows.append({
        "name": "WC1_archived_original_was_PASS",
        "pass": archived_ok and archived_rc == FROM_VERDICT,
        "details": f"archived result_class = {archived_rc!r}; expected {FROM_VERDICT!r}",
        "load_bearing_deletion": "If archived original had a different verdict, regrade would be operating on wrong starting point.",
    })

    current_summary = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig"))
    current_rc = current_summary.get("result_class", "")
    rows.append({
        "name": "WC2_current_result_class_is_BOUNDARY",
        "pass": current_rc == TO_VERDICT,
        "details": f"current result_class = {current_rc!r}; expected {TO_VERDICT!r}",
        "load_bearing_deletion": "If result_class not updated to BOUNDARY string, this WC would FAIL.",
    })

    sha_file = ARCHIVE_SUB / "original_sha256.txt"
    wc3_pass = False
    wc3_detail = ""
    if sha_file.exists():
        text = sha_file.read_text(encoding="utf-8")
        m_r = re.search(r"original_CR120_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        m_s = re.search(r"original_CR120_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
        archived_result = ARCHIVE_SUB / "original_result.md"
        if m_r and m_s and archived_result.exists() and archived_summary.exists():
            wc3_pass = sha256_file(archived_result) == m_r.group(1) and sha256_file(archived_summary) == m_s.group(1)
            wc3_detail = "Archived hashes match recorded." if wc3_pass else "Archived hashes do not match recorded."
        else:
            wc3_detail = "Missing parse or files."
    else:
        wc3_detail = "original_sha256.txt not found."
    rows.append({
        "name": "WC3_archived_originals_hash_match",
        "pass": wc3_pass,
        "details": wc3_detail,
        "load_bearing_deletion": "If archived originals edited/corrupted, this WC would FAIL.",
    })

    ar = current_summary.get("audit_regrade")
    wc4_pass = (
        isinstance(ar, dict)
        and ar.get("from_verdict") == FROM_VERDICT
        and ar.get("to_verdict") == TO_VERDICT
        and ar.get("from_verdict") != ar.get("to_verdict")
        and ar.get("driving_appeal_cr") == "CR-140"
        and ar.get("driving_audit_verdict_sha256") == AUDIT_VERDICT_SHA256
        and ar.get("verdict_direction") == "DOWNGRADED"
    )
    rows.append({
        "name": "WC4_audit_regrade_block_well_formed_and_from_neq_to",
        "pass": wc4_pass,
        "details": "audit_regrade present with correct fields and from != to." if wc4_pass else "audit_regrade block missing/malformed.",
        "load_bearing_deletion": "If from_verdict == to_verdict or required field stripped, this WC would FAIL.",
    })

    wc5_pass = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    rows.append({
        "name": "WC5_audit_verdict_reference_resolves",
        "pass": wc5_pass,
        "details": f"AUDIT_VERDICT exists={AUDIT_VERDICT.exists()}; hash matches",
        "load_bearing_deletion": "If audit verdict moved/edited, this WC would FAIL.",
    })

    wc6_pass = QP091T_INTERNAL.exists() and sha256_file(QP091T_INTERNAL) == QP091T_EXPECTED_SHA
    rows.append({
        "name": "WC6_qp091t_ingest_dependency_satisfied",
        "pass": wc6_pass,
        "details": f"qp091t internal copy exists = {QP091T_INTERNAL.exists()}; SHA matches expected = {wc6_pass}",
        "load_bearing_deletion": "If qp091t were not internally ingested per CR-136, CR-140's narrative (form-selection chronology auditable internally) would not hold.",
    })

    fc = ar.get("forensic_chronology", {}) if isinstance(ar, dict) else {}
    required_chron = {"qp091o_p_session", "qp091r_at_05_34_utc", "qp091s_35_minutes_later", "qp091t_at_06_09_utc", "implication"}
    missing = required_chron - set(fc.keys() if isinstance(fc, dict) else [])
    wc7_pass = not missing
    rows.append({
        "name": "WC7_forensic_chronology_documented",
        "pass": wc7_pass,
        "details": f"forensic_chronology missing fields = {sorted(missing)}" if missing else "All 5 required forensic_chronology fields present.",
        "load_bearing_deletion": "If forensic_chronology were stripped, regrade rationale (form-selection ex post) would be unsupported.",
    })

    psc = ar.get("preserved_structural_content", {}) if isinstance(ar, dict) else {}
    psc_ok = (
        isinstance(psc, dict)
        and psc.get("H_native_identity") == "R^2 * (1 - 2^-D) = 144 * 7/8 = 126 GeV"
        and psc.get("H_native_predates_value_match") is True
        and psc.get("H_reveal_matches_PDG_to_displayed_precision") is True
        and isinstance(psc.get("downstream_consumers"), list)
        and len(psc["downstream_consumers"]) >= 3
    )
    rows.append({
        "name": "WC8_preserved_structural_content_documented",
        "pass": psc_ok,
        "details": f"preserved_structural_content block well-formed with H_native predates value match and >= 3 downstream consumers = {psc_ok}",
        "load_bearing_deletion": "If preserved_structural_content were stripped or H_native were marked as not-predating-value-match, the regrade risks being read as structural refutation.",
    })

    return rows


def run_predictions(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({
        "name": "P1_CR120_target_exists",
        "pass": TARGET_RESULT.exists() and TARGET_SUMMARY.exists(),
        "details": f"target dir = {TARGET_DIR}",
    })
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    archived_ok = archived_summary.exists()
    archived_rc = ""
    if archived_ok:
        try:
            archived_rc = json.loads(archived_summary.read_text(encoding="utf-8-sig")).get("result_class", "")
        except Exception:
            archived_ok = False
    rows.append({
        "name": "P2_archived_original_was_SEALED",
        "pass": archived_ok and archived_rc == FROM_VERDICT,
        "details": f"archived result_class = {archived_rc!r}",
    })
    rows.append({
        "name": "P3_regrade_applied_or_already_applied",
        "pass": entry["status"] in ("REGRADED", "ALREADY_REGRADED"),
        "details": f"status = {entry['status']}",
    })
    current_rc = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig")).get("result_class", "")
    rows.append({
        "name": "P4_post_regrade_result_class_is_BOUNDARY_string",
        "pass": current_rc == TO_VERDICT,
        "details": f"current result_class = {current_rc!r}",
    })
    rows.append({
        "name": "P5_CR136_ingest_dependency_resolved",
        "pass": QP091T_INTERNAL.exists() and sha256_file(QP091T_INTERNAL) == QP091T_EXPECTED_SHA,
        "details": "qp091t internal copy present with expected SHA",
    })
    rr = ARCHIVE_SUB / "REPLACEMENT_RECORD.md"
    rr_text = rr.read_text(encoding="utf-8") if rr.exists() else ""
    rows.append({
        "name": "P6_restoration_requirements_documented_with_forward_blind",
        "pass": rr.exists() and ("Forward-blind precommit" in rr_text or "forward-blind precommit" in rr_text),
        "details": "REPLACEMENT_RECORD names Forward-blind precommit explicitly as restoration requirement",
    })
    return rows


def main() -> None:
    print("CR140 runner: CR-120 Higgs claim reword (SEALED -> BOUNDARY)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    ARCHIVE_SUB.mkdir(parents=True, exist_ok=True)

    archived_result = ARCHIVE_SUB / "original_result.md"
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    pre_result_sha = sha256_file(archived_result) if archived_result.exists() else sha256_file(TARGET_RESULT)
    pre_summary_sha = sha256_file(archived_summary) if archived_summary.exists() else sha256_file(TARGET_SUMMARY)

    src_rows = [
        {
            "cr_id": "CR120",
            "dir_name": "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE",
            "result_md_path": str(TARGET_RESULT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_regrade": pre_result_sha,
            "summary_json_path": str(TARGET_SUMMARY.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "summary_json_sha256_pre_regrade": pre_summary_sha,
        },
        {
            "cr_id": "CR-136 (ingest dependency)",
            "dir_name": "CR136_QP_CHAIN_INGEST",
            "result_md_path": str(INGEST_LOCK.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_regrade": sha256_file(INGEST_LOCK) if INGEST_LOCK.exists() else "",
            "summary_json_path": "",
            "summary_json_sha256_pre_regrade": "",
        },
        {
            "cr_id": "CR-135 (audit)",
            "dir_name": "CR135_HOSTILE_AUDIT_2026_06_17",
            "result_md_path": str(AUDIT_VERDICT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_regrade": sha256_file(AUDIT_VERDICT) if AUDIT_VERDICT.exists() else "",
            "summary_json_path": "",
            "summary_json_sha256_pre_regrade": "",
        },
    ]
    write_csv(SOURCE_MANIFEST_CSV, src_rows)

    entry = perform_regrade()
    print(f"  CR120  {entry['status']:18}")

    write_csv(REGRADE_MANIFEST_CSV, [{
        "cr_id": entry["cr_id"],
        "dir_name": entry["dir_name"],
        "status": entry["status"],
        "from_verdict": entry["from_verdict"],
        "to_verdict": entry["to_verdict"],
        "current_result_class": entry["current_result_class"],
        "result_md_sha256": entry["result_md_sha256"],
        "summary_json_sha256": entry["summary_json_sha256"],
        "archived_original_result_sha256": entry["archived_original_result_sha256"],
        "archived_original_summary_sha256": entry["archived_original_summary_sha256"],
    }])

    wc_rows = run_wrong_controls(entry)
    pred_rows = run_predictions(entry)
    write_csv(WRONG_CONTROLS_CSV, wc_rows)
    write_csv(PREDICTIONS_CSV, pred_rows)

    wc_passed = sum(1 for r in wc_rows if r["pass"])
    pred_passed = sum(1 for r in pred_rows if r["pass"])
    is_clean = entry["status"] in ("REGRADED", "ALREADY_REGRADED")

    print(f"\nStatus:              {entry['status']}")
    print(f"Wrong controls:      {wc_passed}/{len(wc_rows)}")
    print(f"Predictions:         {pred_passed}/{len(pred_rows)}")

    overall_pass = (
        wc_passed == len(wc_rows)
        and pred_passed == len(pred_rows)
        and is_clean
    )
    result_class = (
        "CR140_CR120_HIGGS_CLAIM_REWORD_V1_SEALED"
        if overall_pass
        else "CR140_CR120_HIGGS_CLAIM_REWORD_V1_BOUNDARY_DRAFT"
    )

    lock_payload = {
        "cr_id": "CR140",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "6 of 7 blocking",
        "regrade_type": "VERDICT_DOWNGRADE_HIGGS_CLAIM_EXACT_TO_PDG_MATCH",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "forensic_chronology": FORENSIC_CHRONOLOGY,
        "preserved_structural_content": PRESERVED_STRUCTURAL_CONTENT,
        "stripped_language": STRIPPED_LANGUAGE,
        "ingest_dependency": {
            "cr": "CR-136",
            "lock_sha256": INGEST_LOCK_SHA,
            "qp091t_internal_path": str(QP091T_INTERNAL.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "qp091t_expected_sha": QP091T_EXPECTED_SHA,
        },
        "restoration_requirements": RESTORATION_REQUIREMENTS,
        "restoration_falsifier": RESTORATION_FALSIFIER,
        "target": {
            "cr_id": entry["cr_id"],
            "dir_name": entry["dir_name"],
            "current_result_class": entry["current_result_class"],
        },
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "free_parameters": 0,
        "falsifier": (
            "Re-executing CR140_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; the recomputed lock SHA-256 MUST match."
        ),
    }
    REGRADE_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(REGRADE_LOCK_JSON)
    REGRADE_LOCK_SHA.write_text(f"CR140_regrade_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    md = []
    md.append("# CR140 CR-120 Higgs Claim Reword (SEALED -> BOUNDARY) v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("CR-120 sealed the Higgs claim with the language 'H_reveal = R^2*(1-2^-D) - D^2/R = 125.25 GeV EXACT, derived from {R=12, D=3} alone with zero free parameters, no H input.' The hostile audit identified this as a Tier 4 DEMAND_RETEST: the qp091r-s-t form-selection chronology shows the -D^2/R correction was explicitly enumerated as a 'Wrong Lane Control' WHILE the PDG target 125.25 was visible, then promoted to the active derivation 35 minutes later. The structural identity H_native = R^2*(1-2^-D) = 126 GeV (from substrate algebra primitives R, D, alpha_H alone) genuinely predates the value match. The -D^2/R correction is form-selected ex post.\n")
    md.append("CR-140 regrades CR-120 from PASS to BOUNDARY pending forward-blind precommit of the form before a future high-precision Higgs measurement (HL-LHC, FCC-ee). The structural content (R = 12, D = 3, partition algebra, H_native = 126, 7/8 + 1/8 split, row-18 self-cancel, downstream gravity/carrier-compression consumers) is PRESERVED. The regrade affects strength-of-claim language only.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- qp_chain ingest lock: `00_governance/CR136_QP_CHAIN_INGEST/CR136_ingest_lock.json` (`{INGEST_LOCK_SHA}`)")
    md.append(f"- Target: `09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/`")
    md.append(f"- Source manifest: `CR140_source_manifest.csv`\n")
    md.append("## Forensic Chronology (qp091r-s-t form-selection)\n")
    for k, v in FORENSIC_CHRONOLOGY.items():
        md.append(f"- **{k}:** {v}")
    md.append("")
    md.append("## Language Stripped\n")
    md.append("| Original phrase | Replacement framing |")
    md.append("| --- | --- |")
    for k, v in STRIPPED_LANGUAGE.items():
        md.append(f"| `{k}` | {v} |")
    md.append("")
    md.append("## Target Outcome\n")
    md.append(f"- **Status:** {entry['status']}")
    md.append(f"- **From verdict:** `{FROM_VERDICT}`")
    md.append(f"- **To verdict:** `{TO_VERDICT}`")
    md.append(f"- **Result.md SHA-256:** `{entry['result_md_sha256']}`")
    md.append(f"- **Summary.json SHA-256:** `{entry['summary_json_sha256']}`")
    md.append(f"- **Archived original result.md SHA-256:** `{entry['archived_original_result_sha256']}`")
    md.append(f"- **Archived original summary.json SHA-256:** `{entry['archived_original_summary_sha256']}`\n")
    md.append("## Predictions\n")
    for r in pred_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        md.append(f"- {mark} {r['name']} -- {r['details']}")
    md.append("")
    md.append("## Wrong Controls\n")
    for r in wc_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        md.append(f"- {mark} {r['name']} -- {r['details']}")
        md.append(f"    - load-bearing deletion: {r['load_bearing_deletion']}")
    md.append("")
    md.append("## Restoration Requirements (path back to PASS for CR-120)\n")
    for i, r in enumerate(RESTORATION_REQUIREMENTS, start=1):
        md.append(f"{i}. {r['requirement']}")
        md.append(f"    - *how to verify:* {r['how_to_verify']}")
    md.append("")
    md.append("### Restoration Falsifier\n")
    md.append(RESTORATION_FALSIFIER + "\n")
    md.append("## CR-140 Falsifier (LOCKED)\n")
    md.append("Re-executing `CR140_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR136_ingest_lock_sha256                  = {INGEST_LOCK_SHA}")
    md.append(f"CR140_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR140_regrade_manifest_csv                = {sha256_file(REGRADE_MANIFEST_CSV)}")
    md.append(f"CR140_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR140_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR140_regrade_lock_json                   = {lock_sha}")
    md.append("```\n")
    md.append("## Rule of Immutability\n")
    md.append("Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-140 seal time. Future falsification must be in an appeal CR.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    summary_payload = {
        "cr_id": "CR140",
        "branch": "00_governance",
        "test_class": "CR120_HIGGS_CLAIM_REWORD_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "regrade_type": "VERDICT_DOWNGRADE_HIGGS_CLAIM_EXACT_TO_PDG_MATCH",
        "verdict_change": True,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "forensic_chronology": FORENSIC_CHRONOLOGY,
        "preserved_structural_content": PRESERVED_STRUCTURAL_CONTENT,
        "stripped_language": STRIPPED_LANGUAGE,
        "ingest_dependency_cr136_lock_sha256": INGEST_LOCK_SHA,
        "restoration_requirements": RESTORATION_REQUIREMENTS,
        "restoration_falsifier": RESTORATION_FALSIFIER,
        "target": entry,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "wrong_controls": wc_rows,
        "predictions": pred_rows,
        "falsifier": (
            "Re-executing CR140_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; recomputed lock SHA-256 MUST match."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR136_ingest_lock_sha256": INGEST_LOCK_SHA,
            "CR140_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR140_regrade_manifest_csv": sha256_file(REGRADE_MANIFEST_CSV),
            "CR140_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR140_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR140_regrade_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
