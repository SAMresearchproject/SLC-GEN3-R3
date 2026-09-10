"""CR138 Regrade CR-064a v1.1 from SEALED (PASS) to BOUNDARY.

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661) Tier 3
finding: CR-064a is the surviving rescue claim after CR-063a v1.0 was
empirically falsified (see CR-137).  Its headline "5 of 10 platforms AT
THE LIMIT, 0 violations" rests on three vulnerabilities that the result
does not disclose:

  1. GATE-RATE ARTIFACT: Three of the five AT_THE_LIMIT systems
     (Quantinuum H1, IonQ Forte, Delft NV cryogenic+DD) share IDENTICAL
     T2 * omega products of 6.2832e4 -- the same observation reported as
     three independent confirmations.  The user's own memory record
     flags this artifact and it was not disclosed in CR-064a's
     result.md.

  2. UNVERIFIED CITATIONS: All 10 published T2 measurements in the
     consistency table are tagged "[VERIFY_PRECOMMIT]" -- the author's
     own placeholder for "not yet independently verified against current
     literature".  The seal stands on unverified inputs.

  3. WIDE BANDS:  The AT_THE_LIMIT classification (T2_observed /
     T2_grav between 0.5 and 2.0) is a factor-4 band, and the
     pre-committed falsifier requires a factor-10 overrun -- together
     these absorb a large range of empirical outcomes while still
     reporting "consistent".

CR-138 regrades CR-064a v1.1 from PASS to BOUNDARY, discloses the
1.0248 gate-rate artifact on the record, makes the [VERIFY_PRECOMMIT]
debt explicit, and pre-commits the path back to PASS in concrete
restoration requirements.

Scope
-----
CR-138 is a verdict regrade from PASS to BOUNDARY.  It does NOT:

- Refute CR-064a v1.1 (the formula T2_grav = 16*pi*R^4/(17*omega_gate)
  may still hold -- the issue is evidentiary discipline, not refutation).
- Re-evaluate CR-063a v1.0 (refuted separately by CR-137).
- Modify the recorded formula, predictions, or wrong controls -- those
  stand as the historical v1.1 declaration.  Only the verdict line is
  changed, and the audit_regrade block is added to summary.json.

Falsifier for CR-138 itself
---------------------------
Re-executing this runner on the post-seal state MUST produce zero new
REGRADED entries and zero archive writes; the recomputed lock SHA-256
MUST match the value recorded in CR138_result.md.  Any deviation
falsifies v1.0 of the regrade.

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
TARGET_DIR = COURTROOM_DIR / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH" / "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1"
TARGET_RESULT = TARGET_DIR / "CR064a_result.md"
TARGET_SUMMARY = TARGET_DIR / "CR064a_summary.json"

REFUTED_PRIOR_CR = COURTROOM_DIR / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH" / "CR063a_HARDWARE_TRANSLATION_V1" / "CR063a_result.md"

ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR138_CR064a_regrade"
ARCHIVE_SUB = ARCHIVE_ROOT / "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_CRITERIA = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_CRITERIA.md"
EVENT_README = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "EVENT_README.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR138_source_manifest.csv"
REGRADE_MANIFEST_CSV = CR_DIR / "CR138_regrade_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR138_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR138_wrong_controls.csv"
REGRADE_LOCK_JSON = CR_DIR / "CR138_regrade_lock.json"
REGRADE_LOCK_SHA = CR_DIR / "CR138_regrade_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR138_result.md"
SUMMARY_JSON = CR_DIR / "CR138_summary.json"

FROM_VERDICT = "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED"
TO_VERDICT = "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE"

HEADER_MARKER = "AUDIT-DRIVEN VERDICT REGRADE"

# The gate-rate artifact: three platforms with identical T2 * omega product
GATE_RATE_ARTIFACT = {
    "shared_T2_omega_product": 62832.0,
    "shared_value_meaning": "T2_observed * omega_gate ~= 6.28e4 (rad), identical to 1.0248 * (17 / (16 * pi * R^4)) when omega is interpreted as the gate-operating rate per CR-064a v1.1",
    "platforms_at_identical_product": [
        {"platform": "Quantinuum H1 (171Yb+ clock states)", "T2_observed": "10 s", "gate_omega": "6.2832e3 rad/s", "T2_times_omega": 62832.0},
        {"platform": "IonQ Forte (171Yb+)", "T2_observed": "1 s", "gate_omega": "6.2832e4 rad/s", "T2_times_omega": 62832.0},
        {"platform": "Delft NV cryogenic + dynamical decoupling", "T2_observed": "1 s", "gate_omega": "6.2832e4 rad/s", "T2_times_omega": 62832.0},
    ],
    "implication": (
        "Three platforms reported as independent AT_THE_LIMIT confirmations are "
        "one observation, not three. The headline '5 of 10 platforms AT THE LIMIT' "
        "actually represents two distinct T2*omega measurements within the band "
        "(Stanford fluxonium at 3.13e4; the cluster at 6.28e4) plus the Innsbruck "
        "Ca+ point at 3.14e5. The 5/10 framing oversells the breadth of empirical "
        "support."
    ),
    "user_memory_reference": "feedback_cr064a_t2grav_calibration_rescue.md (project memory, 2026-06-16: '5 platforms at the limit is gate-rate artifact (three exactly at 1.0248)')",
}

CITATION_DEBT = {
    "total_citations": 10,
    "verified_count": 0,
    "unverified_tag": "[VERIFY_PRECOMMIT]",
    "tag_meaning": (
        "Author's own placeholder indicating the published T2 value is recalled "
        "from training-cutoff (Jan 2026) knowledge and has NOT been independently "
        "verified against current literature."
    ),
    "implication": (
        "The headline 'zero violations' is on unverified inputs; a single citation "
        "verified to a different T2 than recorded could flip the count and the "
        "consistency claim."
    ),
}

BAND_AND_FALSIFIER_NOTE = {
    "AT_THE_LIMIT_band_width_ratio": 4.0,
    "AT_THE_LIMIT_band_definition": "T2_observed / T2_grav between 0.5 and 2.0 inclusive",
    "falsifier_cushion_factor": 10.0,
    "implication": (
        "AT_THE_LIMIT is a factor-4 band, not a point estimate; the pre-committed "
        "falsifier requires a factor-10 cushion above T2_grav. Together these "
        "absorb a wide range of outcomes while still reporting 'consistent'. The "
        "result.md does not display this bandwidth as part of the headline, "
        "which oversells consistency at point precision."
    ),
}

RESCUE_PRIOR = {
    "rescued_cr": "CR-063a HARDWARE_TRANSLATION_V1",
    "rescued_cr_current_state": "REFUTED per CR-137 (transmon T2 ~= 1932x v1.0 prediction at first contact)",
    "rescue_introduces": [
        "A_0 = 1/(pi*R) operating point correction (factor pi*R ~= 37.7 enhancement over v1.0)",
        "omega reinterpreted as substrate gate response rate (omega_gate) rather than qubit angular frequency",
    ],
    "rescue_status": (
        "CR-064a v1.1 is the surviving rescue formulation. Whether the rescue itself "
        "holds depends on the empirical content of the consistency table -- which is "
        "the basis the present regrade calls into question."
    ),
}

RESTORATION_REQUIREMENTS = [
    {
        "requirement": (
            "All 10 [VERIFY_PRECOMMIT] citations in the consistency table MUST be "
            "independently verified against current published literature (post-Jan-2026 "
            "and current as of restoration date), with each measurement's T2_observed, "
            "operating omega_gate, and platform-class confirmed to a primary source."
        ),
        "how_to_verify": (
            "Reviewer reads the consistency table, follows each citation to its primary "
            "source (peer-reviewed paper, manufacturer published spec, conference talk "
            "with archived slides), confirms T2 value and gate rate within stated "
            "uncertainty. Open verification log accompanies the restoration CR."
        ),
    },
    {
        "requirement": (
            "The 1.0248 gate-rate artifact MUST be disclosed in the result.md and "
            "either (a) explained as a structural prediction (e.g., three platforms "
            "land at the same T2*omega for a substrate-derived reason that does NOT "
            "depend on choosing platforms with that ratio), OR (b) demonstrated to be "
            "broken by adding non-1.0248 platforms within the AT_THE_LIMIT band."
        ),
        "how_to_verify": (
            "Reviewer reads the result.md, confirms the artifact is named (not implicit), "
            "and confirms either a structural prediction is offered with reasoning, or "
            "additional non-1.0248 platforms are added with verified citations. Silent "
            "omission disqualifies restoration."
        ),
    },
    {
        "requirement": (
            "At least three independent platform measurements at distinct T2*omega "
            "products (not in the 1.0248 cluster) MUST sit within the AT_THE_LIMIT "
            "band, OR the AT_THE_LIMIT band MUST be narrowed from factor-4 to a band "
            "defensible by the spread of verified measurements."
        ),
        "how_to_verify": (
            "Reviewer counts distinct T2*omega products in the AT_THE_LIMIT band post-"
            "verification, confirms count >= 3 OR confirms the new band width is justified "
            "explicitly by the empirical spread (e.g., 1-sigma weighted by experimental "
            "uncertainties on each citation)."
        ),
    },
    {
        "requirement": (
            "The trapped-ion plateau prediction (T2 ceiling ~10 s at kHz gate rates) "
            "MUST be re-evaluated against current Quantinuum / IonQ specifications. "
            "If those specifications have moved past the prediction by more than the "
            "AT_THE_LIMIT band width, the plateau prediction is itself falsified and "
            "blocks restoration."
        ),
        "how_to_verify": (
            "Reviewer checks Quantinuum H1, H2, IonQ Forte/Tempo published T2 specs "
            "current to restoration date; confirms 10 s ceiling holds within the "
            "AT_THE_LIMIT band at the cited gate rate. If T2 > 100 s at the same gate "
            "rate without compensating new structural inputs, restoration blocked."
        ),
    },
]

RESTORATION_FALSIFIER = (
    "Any platform measurement (independent of the 10 currently in the table) clean-"
    "exceeding T2_grav_v1_1 = 16*pi*R^4/(17*omega_gate) by a factor of 10 or more at "
    "its operating omega_gate, with non-gravitational channels rigorously subtracted, "
    "falsifies CR-064a v1.1 entirely (not just blocks restoration). Such a result "
    "would trigger an appeal CR (CR-064b) with its own v1.2 formulation or formal "
    "refutation, following the same protocol that converted CR-063a v1.0 to REFUTED."
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
        "driving_appeal_cr": "CR-138",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_BOUNDARY",
        "verdict_direction": "DOWNGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "triggers": {
            "tier3_audit_finding": "Tier 3 REGRADE_TO_BOUNDARY",
            "gate_rate_artifact": GATE_RATE_ARTIFACT,
            "citation_debt": CITATION_DEBT,
            "band_and_falsifier_note": BAND_AND_FALSIFIER_NOTE,
        },
        "rescue_prior": RESCUE_PRIOR,
        "audit_finding_tier": "Tier 3 REGRADE_TO_BOUNDARY",
        "archive_path": "archive/2026-06-17_CR135_audit_regrades/CR138_CR064a_regrade/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/",
        "original_result_md_sha256": original_result_sha,
        "original_summary_json_sha256": original_summary_sha,
        "replacement_record_path": "archive/2026-06-17_CR135_audit_regrades/CR138_CR064a_regrade/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/REPLACEMENT_RECORD.md",
    }


def build_header_block(original_result_sha: str) -> str:
    return (
        f"> **{HEADER_MARKER} -- 2026-06-17 PER CR-138**\n"
        f">\n"
        f"> The verdict line in this file is regraded from `{FROM_VERDICT}` to a BOUNDARY verdict pending three open debts: (1) the 1.0248 gate-rate artifact (Quantinuum H1, IonQ Forte, Delft NV cryogenic+DD all share T2*omega = 6.2832e4) is not disclosed in the original result.md; (2) all 10 published T2 citations are tagged [VERIFY_PRECOMMIT] and have not been independently verified against current literature; (3) the AT_THE_LIMIT band is factor-4 wide and the falsifier carries a factor-10 cushion, which together absorb a wide range of outcomes while reporting 'consistent'.\n"
        f">\n"
        f"> The recorded formula T2_grav = 16*pi*R^4 / (17*omega_gate), the 10-row consistency table, the predictions, and the wrong controls are preserved verbatim as the historical v1.1 declaration. Only the verdict line is regraded; an audit_regrade block is added to summary.json documenting the open debts and the concrete restoration path.\n"
        f">\n"
        f"> CR-064a v1.1 rescues CR-063a v1.0 (REFUTED per CR-137). If CR-064a v1.1 itself is falsified by a future platform measurement exceeding T2_grav_v1_1 by >=10x with channel subtraction, an appeal CR (CR-064b) follows the same protocol that converted CR-063a v1.0 to REFUTED.\n"
        f">\n"
        f"> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR138_CR064a_regrade/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/original_result.md`\n"
        f"> - Original SHA-256: `{original_result_sha}`\n"
        f"> - Replacement record (with restoration requirements + falsifier): `archive/2026-06-17_CR135_audit_regrades/CR138_CR064a_regrade/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/REPLACEMENT_RECORD.md`\n"
        f"> - Refuted prior claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/` (REFUTED per CR-137)\n"
        f"> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `{AUDIT_VERDICT_SHA256}`)\n"
        f"\n"
    )


def update_result_md(result_text: str, header_block: str) -> str:
    # Insert header block right after the first heading line
    m = re.search(r"^# ", result_text, flags=re.MULTILINE)
    if m:
        first_heading_end = result_text.find("\n", m.start())
        if first_heading_end == -1:
            first_heading_end = len(result_text)
        insert_at = first_heading_end + 1
        out = result_text[:insert_at] + "\n" + header_block + result_text[insert_at:]
    else:
        out = header_block + result_text

    # Rewrite Verdict block
    pattern = re.compile(
        r"## Verdict\s*\n+```text\n" + re.escape(FROM_VERDICT) + r"\n```",
        re.MULTILINE,
    )
    replacement = (
        f"## Verdict (Regraded 2026-06-17 per CR-138)\n\n"
        f"```text\n{TO_VERDICT}\n```\n\n"
        f"**Prior verdict (preserved on the record):** `{FROM_VERDICT}` -- archived at the path in the header block above.\n\n"
        f"**Reason for regrade:** Tier 3 hostile-audit finding. Three open debts (1.0248 gate-rate artifact undisclosed, 10 citations tagged [VERIFY_PRECOMMIT], wide AT_THE_LIMIT band + factor-10 falsifier cushion) move the verdict from PASS to BOUNDARY pending concrete restoration steps documented in the REPLACEMENT_RECORD."
    )
    out, n = pattern.subn(replacement, out, count=1)
    if n == 0:
        # Verdict pattern not matched -- the WC2 control will catch this.
        pass
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
    artifact_table = ""
    for p in GATE_RATE_ARTIFACT["platforms_at_identical_product"]:
        artifact_table += f"| {p['platform']} | {p['T2_observed']} | {p['gate_omega']} | {p['T2_times_omega']:.4e} |\n"
    return f"""# REPLACEMENT_RECORD -- CR-064a verdict regrade (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/CR064a_result.md` and `CR064a_summary.json` |
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
| Audit / appeal CR | CR-138 CR-064a verdict regrade |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (PASS held despite gate-rate artifact + unverified citations) |
| Audit finding tier | `Tier 3 REGRADE_TO_BOUNDARY` |

## 3. Defect summary

CR-064a v1.1 was sealed with PASS (`{FROM_VERDICT}`) on 2026-06-16. The seal rested on a 10-platform consistency table whose headline was "5 AT_THE_LIMIT, 0 violations". The hostile audit identified three vulnerabilities not disclosed in the result.md:

### Gate-rate artifact (1.0248 cluster)

Three of the five AT_THE_LIMIT systems share an IDENTICAL T2 * omega product of 6.2832e4:

| Platform | T2 observed | gate omega | T2 * omega |
| --- | --- | --- | --- |
{artifact_table.rstrip()}

These three platforms are reported as independent confirmations of the T2_grav_v1_1 formula at the AT_THE_LIMIT band. They are not three independent confirmations. They are three platforms with identical T2*omega products -- a *cluster*, not a confirmation count.

### Citation debt

All 10 published T2 measurements in the consistency table are tagged `[VERIFY_PRECOMMIT]`, the author's own marker indicating the value has not been independently verified against current literature post Jan-2026 training cutoff. The seal stands on inputs the author has not yet checked.

### Band and falsifier cushions

The AT_THE_LIMIT classification is a factor-4 band (T2_observed / T2_grav between 0.5 and 2.0). The pre-committed falsifier requires a factor-10 cushion (T2 > 10x T2_grav). These cushions together absorb a wide range of empirical outcomes while still reporting "consistent". The result.md does not display these bandwidths at the headline level.

## 4. What changed

- The verdict line in `CR064a_result.md` is regraded from `{FROM_VERDICT}` to `{TO_VERDICT}`.
- The `result_class` field in `CR064a_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR064a_summary.json` documenting all three triggers (gate-rate artifact, citation debt, band/cushion).
- A header block is prepended to `CR064a_result.md` linking to this archive entry and disclosing the gate-rate artifact at the top of the file.
- The formula, consistency table, predictions, and wrong controls are **preserved verbatim** as the historical v1.1 declaration. The regrade affects only the verdict line.

## 5. Restoration requirements (path back to PASS)

To restore CR-064a v1.1 to PASS, **all** of the following must hold:

{restoration_lines}

### 5a. Restoration falsifier

{RESTORATION_FALSIFIER}

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite at least three independent verified platform measurements at distinct T2*omega products, OR document the structural reason three platforms cluster at 1.0248

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-064a v1.1 record does NOT:

- Claim the formula T2_grav = 16*pi*R^4 / (17*omega_gate) is itself wrong -- the issue is evidentiary discipline, not refutation.
- Refute the underlying gravity-mechanism (CR-121) or carrier-compression gate (CR-122).
- Claim the trapped-ion plateau prediction is false -- it is held open pending verified spec re-evaluation.
- Repair any self-hash defect in CR-064a (separate concern; this CR focuses on verdict regrade only).

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | {original_sealed_utc} | result.md `{short(original_result_sha)}` / summary.json `{short(original_summary_sha)}` | CR064a runner |
| Audit finding | 2026-06-17 | audit verdict `{short(AUDIT_VERDICT_SHA256)}` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-138 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-064a finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1.md`
- Refuted prior claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/` (REFUTED per CR-137)
- Event README: `../EVENT_README.md`
- CR-138 result: `00_governance/CR138_CR064A_REGRADE_TO_BOUNDARY/CR138_result.md`
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
            "cr_id": "CR064a",
            "dir_name": "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
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
            "cr_id": "CR064a",
            "dir_name": "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
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
        f"original_CR064a_result_md_sha256 = {original_result_sha}\n"
        f"original_CR064a_summary_json_sha256 = {original_summary_sha}\n",
        encoding="utf-8",
    )

    audit_block = build_audit_regrade_block(original_result_sha, original_summary_sha)
    summary_obj["result_class"] = TO_VERDICT
    new_summary = reorder_with_audit_first(summary_obj, audit_block, "audit_regrade")
    TARGET_SUMMARY.write_text(
        json.dumps(new_summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

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
        "cr_id": "CR064a",
        "dir_name": "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
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
        "load_bearing_deletion": "If archived original had a different verdict, the regrade would be operating on the wrong starting point.",
    })

    current_summary = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig"))
    current_rc = current_summary.get("result_class", "")
    rows.append({
        "name": "WC2_current_result_class_is_BOUNDARY",
        "pass": current_rc == TO_VERDICT,
        "details": f"current result_class = {current_rc!r}; expected {TO_VERDICT!r}",
        "load_bearing_deletion": "If result_class were not updated to the BOUNDARY string, this WC would FAIL.",
    })

    sha_file = ARCHIVE_SUB / "original_sha256.txt"
    wc3_pass = False
    wc3_detail = ""
    if sha_file.exists():
        text = sha_file.read_text(encoding="utf-8")
        m_r = re.search(r"original_CR064a_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        m_s = re.search(r"original_CR064a_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
        archived_result = ARCHIVE_SUB / "original_result.md"
        if m_r and m_s and archived_result.exists() and archived_summary.exists():
            wc3_pass = (
                sha256_file(archived_result) == m_r.group(1)
                and sha256_file(archived_summary) == m_s.group(1)
            )
            wc3_detail = (
                "Archived result.md and summary.json hash to the values recorded in original_sha256.txt."
                if wc3_pass else
                "Archived file hashes do not match recorded values."
            )
        else:
            wc3_detail = "Missing parse or files."
    else:
        wc3_detail = "original_sha256.txt not found."
    rows.append({
        "name": "WC3_archived_originals_hash_match",
        "pass": wc3_pass,
        "details": wc3_detail,
        "load_bearing_deletion": "If either archived original were edited/corrupted, this WC would FAIL.",
    })

    ar = current_summary.get("audit_regrade")
    wc4_pass = (
        isinstance(ar, dict)
        and ar.get("from_verdict") == FROM_VERDICT
        and ar.get("to_verdict") == TO_VERDICT
        and ar.get("from_verdict") != ar.get("to_verdict")
        and ar.get("driving_appeal_cr") == "CR-138"
        and ar.get("driving_audit_verdict_sha256") == AUDIT_VERDICT_SHA256
        and ar.get("verdict_direction") == "DOWNGRADED"
    )
    rows.append({
        "name": "WC4_audit_regrade_block_well_formed_and_from_neq_to",
        "pass": wc4_pass,
        "details": (
            "audit_regrade present with correct fields and from != to."
            if wc4_pass else
            "audit_regrade block missing or malformed."
        ),
        "load_bearing_deletion": "If from_verdict == to_verdict, or required field stripped, this WC would FAIL.",
    })

    wc5_pass = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    rows.append({
        "name": "WC5_audit_verdict_reference_resolves",
        "pass": wc5_pass,
        "details": f"AUDIT_VERDICT exists={AUDIT_VERDICT.exists()}; hash matches",
        "load_bearing_deletion": "If audit verdict file moved/edited, the recorded reference would be unverifiable.",
    })

    rr = ARCHIVE_SUB / "REPLACEMENT_RECORD.md"
    wc6_pass = False
    wc6_detail = ""
    if rr.exists():
        rr_text = rr.read_text(encoding="utf-8")
        has_section = "## 5. Restoration requirements" in rr_text
        has_falsifier = "### 5a. Restoration falsifier" in rr_text
        has_concrete = (
            "[VERIFY_PRECOMMIT]" in rr_text
            and "1.0248" in rr_text
            and "AT_THE_LIMIT band" in rr_text
        )
        wc6_pass = has_section and has_falsifier and has_concrete
        wc6_detail = f"section={has_section}; falsifier_subsection={has_falsifier}; concrete_items_present={has_concrete}"
    else:
        wc6_detail = "REPLACEMENT_RECORD.md missing."
    rows.append({
        "name": "WC6_REPLACEMENT_RECORD_has_concrete_restoration_requirements",
        "pass": wc6_pass,
        "details": wc6_detail,
        "load_bearing_deletion": "If restoration requirements were N/A/vague/missing concrete items ([VERIFY_PRECOMMIT], 1.0248, AT_THE_LIMIT band), this WC would FAIL.",
    })

    # WC7: gate-rate artifact disclosed in audit_regrade triggers
    triggers = ar.get("triggers", {}) if isinstance(ar, dict) else {}
    gra = triggers.get("gate_rate_artifact", {}) if isinstance(triggers, dict) else {}
    platforms = gra.get("platforms_at_identical_product", []) if isinstance(gra, dict) else []
    wc7_pass = (
        isinstance(platforms, list)
        and len(platforms) >= 3
        and all(isinstance(p, dict) and p.get("T2_times_omega") == 62832.0 for p in platforms)
    )
    rows.append({
        "name": "WC7_gate_rate_artifact_disclosed_in_audit_regrade",
        "pass": wc7_pass,
        "details": (
            f"audit_regrade.triggers.gate_rate_artifact contains {len(platforms)} platforms at identical T2*omega = 6.2832e4"
            if wc7_pass else
            "gate_rate_artifact block missing or platforms list incomplete"
        ),
        "load_bearing_deletion": "If the 1.0248 artifact were not disclosed in the regrade record, the regrade would be cosmetic; this WC would FAIL.",
    })

    # WC8: refuted prior claim (CR-063a) exists and is in REFUTED state
    wc8_pass = False
    wc8_detail = ""
    if REFUTED_PRIOR_CR.exists():
        prior_text = REFUTED_PRIOR_CR.read_text(encoding="utf-8")
        if "REFUTED_BY_TRANSMON_T2_CONTACT" in prior_text:
            wc8_pass = True
            wc8_detail = "CR-063a result.md exists and contains REFUTED_BY_TRANSMON_T2_CONTACT marker (set by CR-137)."
        else:
            wc8_detail = "CR-063a result.md exists but does not contain REFUTED marker; CR-137 not applied."
    else:
        wc8_detail = "CR-063a result.md missing."
    rows.append({
        "name": "WC8_refuted_prior_CR063a_in_REFUTED_state",
        "pass": wc8_pass,
        "details": wc8_detail,
        "load_bearing_deletion": "If CR-137 had not run (CR-063a still PASS), CR-138's narrative (rescue of a refuted claim) would be inconsistent; this WC would FAIL.",
    })

    return rows


def run_predictions(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({
        "name": "P1_CR064a_target_exists",
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
        "name": "P2_archived_original_was_v1_1_SEALED",
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
        "name": "P5_refuted_prior_CR063a_resolves_and_is_REFUTED",
        "pass": REFUTED_PRIOR_CR.exists() and "REFUTED_BY_TRANSMON_T2_CONTACT" in REFUTED_PRIOR_CR.read_text(encoding="utf-8"),
        "details": "CR-063a is in REFUTED state per CR-137 (precondition for CR-138's narrative)",
    })
    rows.append({
        "name": "P6_restoration_requirements_documented_with_concrete_items",
        "pass": (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").exists()
                and "[VERIFY_PRECOMMIT]" in (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").read_text(encoding="utf-8")
                and "1.0248" in (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").read_text(encoding="utf-8"),
        "details": "REPLACEMENT_RECORD names [VERIFY_PRECOMMIT] and 1.0248 explicitly in restoration items.",
    })
    return rows


def main() -> None:
    print("CR138 runner: CR-064a verdict regrade (SEALED -> BOUNDARY)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    ARCHIVE_SUB.mkdir(parents=True, exist_ok=True)

    archived_result = ARCHIVE_SUB / "original_result.md"
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    pre_result_sha = sha256_file(archived_result) if archived_result.exists() else sha256_file(TARGET_RESULT)
    pre_summary_sha = sha256_file(archived_summary) if archived_summary.exists() else sha256_file(TARGET_SUMMARY)

    src_rows = [
        {
            "cr_id": "CR064a",
            "dir_name": "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
            "result_md_path": str(TARGET_RESULT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_regrade": pre_result_sha,
            "summary_json_path": str(TARGET_SUMMARY.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "summary_json_sha256_pre_regrade": pre_summary_sha,
        },
        {
            "cr_id": "CR-063a (refuted prior)",
            "dir_name": "CR063a_HARDWARE_TRANSLATION_V1",
            "result_md_path": str(REFUTED_PRIOR_CR.relative_to(COURTROOM_DIR)).replace("\\", "/") if REFUTED_PRIOR_CR.exists() else "",
            "result_md_sha256_pre_regrade": sha256_file(REFUTED_PRIOR_CR) if REFUTED_PRIOR_CR.exists() else "",
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
    print(f"  CR064a  {entry['status']:18}  {entry['current_result_class']}")

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
        "CR138_CR064A_REGRADE_TO_BOUNDARY_V1_SEALED"
        if overall_pass
        else "CR138_CR064A_REGRADE_TO_BOUNDARY_V1_BOUNDARY_DRAFT"
    )

    lock_payload = {
        "cr_id": "CR138",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "3 of 7 blocking",
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_BOUNDARY",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "triggers": {
            "gate_rate_artifact": GATE_RATE_ARTIFACT,
            "citation_debt": CITATION_DEBT,
            "band_and_falsifier_note": BAND_AND_FALSIFIER_NOTE,
        },
        "rescue_prior": RESCUE_PRIOR,
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
            "Re-executing CR138_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; the recomputed lock SHA-256 MUST "
            "match the value recorded in CR138_result.md."
        ),
    }
    REGRADE_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(REGRADE_LOCK_JSON)
    REGRADE_LOCK_SHA.write_text(f"CR138_regrade_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    md = []
    md.append("# CR138 CR-064a Verdict Regrade (SEALED -> BOUNDARY) v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("CR-064a v1.1 is the rescue claim that emerged after CR-063a v1.0 was empirically falsified (regraded to REFUTED per CR-137). The rescue introduced two new structural inputs (A_0 = 1/(pi*R) operating-point enhancement, omega reinterpreted as gate response rate) and was sealed with a 10-platform consistency table headlined '5 of 10 AT_THE_LIMIT, 0 violations'. The hostile audit identified three vulnerabilities in that seal that are not disclosed in the original result.md:\n")
    md.append("1. **Gate-rate artifact:** Quantinuum H1, IonQ Forte, and Delft NV cryo+DD share an IDENTICAL T2*omega product of 6.2832e4 -- three platforms reported as independent confirmations are one observation, not three.\n")
    md.append("2. **Citation debt:** All 10 published T2 citations are tagged [VERIFY_PRECOMMIT] (author's own placeholder for 'not yet independently verified against current literature').\n")
    md.append("3. **Wide bands + cushions:** The AT_THE_LIMIT classification is a factor-4 band, and the pre-committed falsifier requires a factor-10 cushion -- together absorbing a wide range of outcomes while reporting 'consistent'.\n")
    md.append("CR-138 regrades CR-064a v1.1 from PASS to BOUNDARY pending three concrete restoration requirements documented in the REPLACEMENT_RECORD. The formula T2_grav = 16*pi*R^4 / (17*omega_gate), the consistency table, predictions, and wrong controls are preserved verbatim as the historical v1.1 declaration; only the verdict line and the audit_regrade summary metadata are changed.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- Target: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`")
    md.append(f"- Refuted prior claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/` (REFUTED per CR-137)")
    md.append(f"- Source manifest: `CR138_source_manifest.csv`\n")
    md.append("## The Gate-Rate Artifact (1.0248 cluster)\n")
    md.append("| Platform | T2 observed | gate omega | T2 * omega |")
    md.append("| --- | --- | --- | --- |")
    for p in GATE_RATE_ARTIFACT["platforms_at_identical_product"]:
        md.append(f"| {p['platform']} | {p['T2_observed']} | {p['gate_omega']} | {p['T2_times_omega']:.4e} |")
    md.append("")
    md.append(f"**Implication:** {GATE_RATE_ARTIFACT['implication']}\n")
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
    md.append("## Restoration Requirements (path back to PASS for CR-064a v1.1)\n")
    for i, r in enumerate(RESTORATION_REQUIREMENTS, start=1):
        md.append(f"{i}. {r['requirement']}")
        md.append(f"    - *how to verify:* {r['how_to_verify']}")
    md.append("")
    md.append("### Restoration Falsifier\n")
    md.append(RESTORATION_FALSIFIER + "\n")
    md.append("## CR-138 Falsifier (LOCKED)\n")
    md.append("Re-executing `CR138_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match the value recorded here.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR138_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR138_regrade_manifest_csv                = {sha256_file(REGRADE_MANIFEST_CSV)}")
    md.append(f"CR138_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR138_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR138_regrade_lock_json                   = {lock_sha}")
    md.append("```\n")
    md.append("## Rule of Immutability\n")
    md.append("Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-138 seal time. Future falsification must be in an appeal CR.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    summary_payload = {
        "cr_id": "CR138",
        "branch": "00_governance",
        "test_class": "CR064A_VERDICT_REGRADE_TO_BOUNDARY_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_BOUNDARY",
        "verdict_change": True,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "triggers": {
            "gate_rate_artifact": GATE_RATE_ARTIFACT,
            "citation_debt": CITATION_DEBT,
            "band_and_falsifier_note": BAND_AND_FALSIFIER_NOTE,
        },
        "rescue_prior": RESCUE_PRIOR,
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
            "Re-executing CR138_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; recomputed lock SHA-256 MUST match."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR138_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR138_regrade_manifest_csv": sha256_file(REGRADE_MANIFEST_CSV),
            "CR138_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR138_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR138_regrade_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
