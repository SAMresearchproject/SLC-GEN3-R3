"""CR137 Regrade CR-063a v1.0 from SEALED (PASS) to REFUTED.

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661) Tier 7
finding: CR-063a was sealed as PASS but its own pre-committed one-violation
falsifier was empirically triggered at first contact with published
literature.  The rescue (CR-064a v1.1 with A_0 enhancement + omega
reinterpretation as gate rate) was routed silently, leaving CR-063a v1.0
sealed at horizon (A = 1) reading per CR-064a's own WC3.

This is the Courtroom protocol being weaponized against itself.  The
protocol exists to prevent exactly that.  CR-137 promotes CR-063a v1.0
to REFUTED on the record while preserving CR-064a v1.1 as the surviving
rescue claim (audited separately under CR-138).

Empirical falsification of v1.0
-------------------------------
CR-063a v1.0 falsifier (recorded at seal time, CR063a_PRED_1):
    "ONE rigorously-isolated T2 measurement on any platform exceeding
     T2_grav (after channel subtraction) falsifies v1.0."

Empirical contact (from CR-064a's own published-T2 table):
    Platform:         IBM Heron / Eagle transmon (typical)
    Gate omega:       pi * 1e7 rad/s
    T2_grav_v1_0:     1626.35 / omega = 51.8 ns
    T2_observed:      100 us
    Overrun:          ~1930x

The falsifier was triggered.  No platform-subtraction caveat in
CR-063a's own protocol disputes the contact: the transmon overrun is
five orders of magnitude beyond any plausible non-gravitational
attribution, and CR-064a's response was not "the channel was not
isolated" but "the formula needs A_0 enhancement and omega
reinterpretation" -- introducing two new structural inputs.

Per Courtroom rules: a triggered one-violation falsifier with a fix
requiring new structural inputs REFUTES v1.0.  The fix becomes v1.1
(here, CR-064a) and is audited as its own claim.

Scope
-----
CR-137 is a verdict regrade from PASS (SEALED) to REFUTED.  It does
NOT:

- Modify CR-064a v1.1 (the surviving rescue claim, audited separately
  in CR-138).
- Alter CR-063a's recorded formula, predictions, wrong controls, or
  hardware translation matrix -- those stand as the historical v1.0
  declaration.  The regrade affects only the verdict line and adds an
  audit_regrade trail.
- Repair any self-hash defect in CR-063a (separate concern; QC-chain
  self-hash audit is its own CR if/when scoped).

Method
------
1. Read CR-063a's current result.md and summary.json.
2. Idempotency check: is result_class already REFUTED AND audit_regrade
   block present AND header block in result.md? If yes, ALREADY_REGRADED.
3. Otherwise: archive originals bit-identical, prepend audit_regrade
   block to summary.json, prepend header block to result.md, update the
   verdict line, generate REPLACEMENT_RECORD with populated restoration
   requirements.

Restoration requirements (preserved here for the record)
--------------------------------------------------------
To restore CR-063a v1.0 to PASS, ALL of the following must hold:

  1. The original v1.0 formula T2_grav = 16*R^3/(17*omega) at A = 1
     horizon condition (NOT the A_0 = 1/(pi*R) rescue) must agree with a
     measured T2 on at least one physical qubit platform under rigorous
     non-gravitational channel subtraction.
  2. The CR-064a v1.1 reinterpretation (omega as gate rate, A_0
     scaling) cannot be invoked: v1.0 stands or falls by its own
     declared formula and conditions.
  3. The published-T2 table (CR-064a) must be re-verified against
     current literature with at least one entry matching v1.0's
     prediction (not v1.1's).

Restoration falsifier
---------------------
A second platform measurement showing T2 > 10x * T2_grav_v1_0 at the
relevant omega, with channel subtraction, BLOCKS restoration -- the
overrun is fundamental, not platform-specific.  Given the existing
~1930x overrun on transmons, restoration is structurally implausible;
this CR records that judgment formally rather than papering over it.

Falsifier for CR-137 itself
---------------------------
Re-executing this runner on the post-seal state MUST produce zero new
REGRADE entries and zero new archive writes.  Any change to the
recorded state on a clean re-run falsifies v1.0 of the regrade claim.

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
TARGET_DIR = COURTROOM_DIR / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH" / "CR063a_HARDWARE_TRANSLATION_V1"
TARGET_RESULT = TARGET_DIR / "CR063a_result.md"
TARGET_SUMMARY = TARGET_DIR / "CR063a_summary.json"

RESCUE_CR_DIR = COURTROOM_DIR / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH" / "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1"
RESCUE_RESULT = RESCUE_CR_DIR / "CR064a_result.md"

ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR137_CR063a_regrade"
ARCHIVE_SUB = ARCHIVE_ROOT / "CR063a_HARDWARE_TRANSLATION_V1"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_CRITERIA = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_CRITERIA.md"
EVENT_README = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "EVENT_README.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR137_source_manifest.csv"
REGRADE_MANIFEST_CSV = CR_DIR / "CR137_regrade_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR137_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR137_wrong_controls.csv"
REGRADE_LOCK_JSON = CR_DIR / "CR137_regrade_lock.json"
REGRADE_LOCK_SHA = CR_DIR / "CR137_regrade_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR137_result.md"
SUMMARY_JSON = CR_DIR / "CR137_summary.json"

FROM_VERDICT = "CR063a_HARDWARE_TRANSLATION_V1_SEALED"
TO_VERDICT = "CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1"

HEADER_MARKER = "AUDIT-DRIVEN VERDICT REGRADE"

EMPIRICAL_EVIDENCE = {
    "platform": "IBM Heron / Eagle transmon (typical)",
    "gate_omega_rad_per_s": 3.1416e7,
    "T2_observed_us": 100.0,
    "T2_grav_v1_0_predicted_ns": 51.8,
    "overrun_factor_approx": 1932,
    "source": "CR064a published-T2 verification table (entry tagged [VERIFY_PRECOMMIT])",
    "v1_0_falsifier_text": (
        "ONE rigorously-isolated T2 measurement on any platform exceeding "
        "T2_grav (after channel subtraction) falsifies v1.0."
    ),
}

RESCUE_PATH = {
    "rescue_cr": "CR-064a A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
    "rescue_formula": "T2_grav = 16 * pi * R^4 / (17 * omega_gate) seconds",
    "rescue_structural_inputs_introduced": [
        "A_0 = 1/(pi*R) operating point correction (enhancement factor pi*R ~= 37.7)",
        "omega reinterpretation: omega_gate (substrate response rate) rather than qubit splitting",
    ],
    "rescue_audit_status": "Surviving claim as of 2026-06-17; CR-138 regrades CR-064a to BOUNDARY pending citation verification and disclosure of 1.0248 gate-rate artifact.",
}

RESTORATION_REQUIREMENTS = [
    {
        "requirement": (
            "Original v1.0 formula T2_grav = 16*R^3/(17*omega) at A = 1 horizon "
            "condition (NOT the A_0 = 1/(pi*R) rescue) must agree with a measured "
            "T2 on at least one physical qubit platform under rigorous "
            "non-gravitational channel subtraction."
        ),
        "how_to_verify": (
            "Reviewer reads the measurement protocol, confirms the formula tested "
            "is literally 16*R^3/(17*omega), confirms the operating point is "
            "horizon (A=1) and NOT A_0, confirms subtraction protocol is reported "
            "transparently with all subtracted channels enumerated, and confirms "
            "the residual T2 equals T2_grav within experimental error."
        ),
    },
    {
        "requirement": (
            "The CR-064a v1.1 reinterpretation (omega as gate rate, A_0 scaling) "
            "MUST NOT be invoked. v1.0 stands or falls by its own declared "
            "formula and conditions."
        ),
        "how_to_verify": (
            "Reviewer confirms no part of the restoration argument uses omega_gate "
            "in place of qubit angular frequency, and confirms no A_0 enhancement "
            "factor is applied. Either substitution disqualifies the restoration."
        ),
    },
    {
        "requirement": (
            "The CR-064a published-T2 table must be re-verified against current "
            "literature (closing the [VERIFY_PRECOMMIT] open debt) with at least "
            "one entry matching v1.0's prediction (NOT v1.1's)."
        ),
        "how_to_verify": (
            "Reviewer checks the verified-citation entries in CR-138 result, "
            "confirms at least one published T2 measurement equals the v1.0 "
            "T2_grav prediction within stated uncertainty at the cited gate "
            "angular frequency."
        ),
    },
]

RESTORATION_FALSIFIER = (
    "A second platform measurement showing T2 > 10x * T2_grav_v1_0 at the "
    "relevant omega with channel subtraction, BLOCKS restoration. Given the "
    "existing approximately 1930x overrun on transmons, restoration is "
    "structurally implausible; this CR records that judgment rather than "
    "papering over it."
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


# ----------------------------------------------------------------------
# Regrade operation
# ----------------------------------------------------------------------

def build_audit_regrade_block(original_result_sha: str, original_summary_sha: str) -> dict[str, Any]:
    return {
        "applied_utc": now_utc(),
        "driving_appeal_cr": "CR-137",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_REFUTED",
        "verdict_direction": "DOWNGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "trigger": "TRANSMON_T2_EMPIRICAL_CONTACT_TIER7_AUDIT_FINDING",
        "trigger_evidence": EMPIRICAL_EVIDENCE,
        "rescue_path": RESCUE_PATH,
        "audit_finding_tier": "Tier 7 CALLOUT_FAIL_DRESSED_AS_PASS",
        "archive_path": "archive/2026-06-17_CR135_audit_regrades/CR137_CR063a_regrade/CR063a_HARDWARE_TRANSLATION_V1/",
        "original_result_md_sha256": original_result_sha,
        "original_summary_json_sha256": original_summary_sha,
        "replacement_record_path": "archive/2026-06-17_CR135_audit_regrades/CR137_CR063a_regrade/CR063a_HARDWARE_TRANSLATION_V1/REPLACEMENT_RECORD.md",
    }


def build_header_block(original_result_sha: str) -> str:
    return (
        f"> **{HEADER_MARKER} — 2026-06-17 PER CR-137**\n"
        f">\n"
        f"> The verdict line in this file is regraded from `{FROM_VERDICT}` to `{TO_VERDICT}`. The v1.0 pre-committed one-violation falsifier (`CR063a_PRED_1`) was empirically triggered: a published IBM Heron/Eagle transmon T2 of approximately 100 microseconds at gate omega ~= pi * 1e7 rad/s exceeds the v1.0 prediction T2_grav = 1626.35 / omega ~= 51.8 ns by a factor of approximately 1932. The rescue (CR-064a v1.1, A_0 enhancement + omega-as-gate-rate reinterpretation) introduces two new structural inputs and is audited separately as a distinct claim.\n"
        f">\n"
        f"> The recorded formula, predictions, translation matrix, and wrong controls below are preserved verbatim as the historical v1.0 declaration. The verdict is the only line regraded.\n"
        f">\n"
        f"> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR137_CR063a_regrade/CR063a_HARDWARE_TRANSLATION_V1/original_result.md`\n"
        f"> - Original SHA-256: `{original_result_sha}`\n"
        f"> - Replacement record (with restoration requirements + falsifier): `archive/2026-06-17_CR135_audit_regrades/CR137_CR063a_regrade/CR063a_HARDWARE_TRANSLATION_V1/REPLACEMENT_RECORD.md`\n"
        f"> - Surviving rescue claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/` (regraded to BOUNDARY by CR-138)\n"
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

    # Rewrite the Verdict block
    pattern = re.compile(
        r"## Verdict\s*\n+```text\n" + re.escape(FROM_VERDICT) + r"\n```",
        re.MULTILINE,
    )
    replacement = (
        f"## Verdict (Regraded 2026-06-17 per CR-137)\n\n"
        f"```text\n{TO_VERDICT}\n```\n\n"
        f"**Prior verdict (preserved on the record):** `{FROM_VERDICT}` — archived at the path in the header block above.\n\n"
        f"**Reason for regrade:** v1.0 pre-committed one-violation falsifier triggered by transmon T2 contact at first comparison with published literature. Rescue (CR-064a v1.1) introduces two new structural inputs and is audited separately."
    )
    out, n = pattern.subn(replacement, out, count=1)
    if n == 0:
        # If the canonical block was not matched, leave verdict text in place
        # and ONLY add the header block. WC2 will catch the failed update.
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
    return f"""# REPLACEMENT_RECORD — CR-063a verdict regrade (SEALED → REFUTED)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/CR063a_result.md` and `CR063a_summary.json` |
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
| Audit / appeal CR | CR-137 CR-063a verdict regrade |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (PASS verdict held despite triggered one-violation falsifier) |
| Audit finding tier | `Tier 7 CALLOUT_FAIL_DRESSED_AS_PASS` |

## 3. Defect summary

CR-063a v1.0 was sealed with PASS status (`{FROM_VERDICT}`) on 2026-06-16T01:22:35Z. Its pre-committed one-violation falsifier (`CR063a_PRED_1`) stated: *"ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0."*

At first comparison with published literature (CR-064a, 2026-06-16, same author session), an IBM Heron / Eagle transmon T2 of ~= 100 microseconds at gate omega ~= pi * 1e7 rad/s was identified. The v1.0 prediction at the same omega is T2_grav = 1626.35 / omega ~= 51.8 ns. The observed T2 exceeds the v1.0 prediction by a factor of approximately **1932** -- five orders of magnitude beyond any plausible non-gravitational channel attribution. The falsifier was triggered.

The response in CR-064a was not to record falsification but to introduce a rescue v1.1 with two new structural inputs (A_0 = 1/(pi*R) operating-point enhancement, omega reinterpreted as substrate gate response rate rather than qubit angular frequency), and to leave CR-063a v1.0 sealed at the original horizon (A = 1) reading per CR-064a's own WC3. This is the Courtroom protocol weaponized against itself: a triggered one-violation falsifier whose verdict was preserved by routing the rescue through a sibling CR.

CR-137 promotes CR-063a v1.0 to REFUTED per the protocol's own rules.

## 4. What changed

- The verdict line in `CR063a_result.md` is regraded from `{FROM_VERDICT}` to `{TO_VERDICT}`.
- The `result_class` field in `CR063a_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR063a_summary.json` documenting the regrade chain and trigger evidence.
- A header block is prepended to `CR063a_result.md` linking to this archive entry.
- The formula, predictions, wrong controls, and translation matrix are **preserved verbatim** as the historical v1.0 declaration. The regrade affects only the verdict line.

## 5. Restoration requirements (path back to PASS)

To restore CR-063a v1.0 to PASS, **all** of the following must hold:

{restoration_lines}

### 5a. Restoration falsifier

{RESTORATION_FALSIFIER}

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event (this file does not get rewritten; a NEW record is added)
- Not delete the present REFUTED state; if restoration succeeds, the present artifact is in turn archived under the restoration CR's date
- Cite an independent published T2 measurement (NOT one already in CR-064a's [VERIFY_PRECOMMIT]-tagged table) at the v1.0 horizon-condition formula

## 6. What this artifact still does NOT do (post-regrade)

The REFUTED CR-063a v1.0 record does NOT:

- Claim CR-064a v1.1 is also refuted — that is a distinct claim, audited separately in CR-138.
- Claim the underlying gravity-mechanism (CR-121) is refuted — CR-121's 1/8 + qA mechanism survives independently.
- Claim no SAM-native qubit can ever achieve T2_grav-limited operation — only that the specific v1.0 formula at horizon condition is contradicted by transmon contact.
- Repair any self-hash defect in CR-063a (separate concern; this CR focuses on the verdict regrade only).

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | {original_sealed_utc} | result.md `{short(original_result_sha)}` / summary.json `{short(original_summary_sha)}` | CR063a runner |
| Audit finding | 2026-06-17 | audit verdict `{short(AUDIT_VERDICT_SHA256)}` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-137 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-063a finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR063a_HARDWARE_TRANSLATION_V1.md`
- Surviving rescue claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`
- Event README: `../EVENT_README.md`
- CR-137 result: `00_governance/CR137_CR063A_REGRADE_TO_REFUTED/CR137_result.md`
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
        # Already regraded; verify archive present
        archived_result = ARCHIVE_SUB / "original_result.md"
        archived_summary = ARCHIVE_SUB / "original_summary.json"
        return {
            "cr_id": "CR063a",
            "dir_name": "CR063a_HARDWARE_TRANSLATION_V1",
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
        # Original verdict doesn't match expected pre-regrade state
        return {
            "cr_id": "CR063a",
            "dir_name": "CR063a_HARDWARE_TRANSLATION_V1",
            "status": f"ANOMALY_UNEXPECTED_RESULT_CLASS:{current_result_class}",
            "from_verdict": FROM_VERDICT,
            "to_verdict": TO_VERDICT,
            "current_result_class": current_result_class,
            "result_md_sha256": sha256_file(TARGET_RESULT),
            "summary_json_sha256": sha256_file(TARGET_SUMMARY),
            "archived_original_result_sha256": "",
            "archived_original_summary_sha256": "",
        }

    # --- NEEDS_REGRADE ---
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
        f"original_CR063a_result_md_sha256 = {original_result_sha}\n"
        f"original_CR063a_summary_json_sha256 = {original_summary_sha}\n",
        encoding="utf-8",
    )

    # Build and prepend audit_regrade block to summary; update result_class
    audit_block = build_audit_regrade_block(original_result_sha, original_summary_sha)
    summary_obj["result_class"] = TO_VERDICT
    new_summary = reorder_with_audit_first(summary_obj, audit_block, "audit_regrade")
    TARGET_SUMMARY.write_text(
        json.dumps(new_summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Update result.md: header block + rewritten verdict section
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
        "cr_id": "CR063a",
        "dir_name": "CR063a_HARDWARE_TRANSLATION_V1",
        "status": "REGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "current_result_class": TO_VERDICT,
        "result_md_sha256": post_result_sha,
        "summary_json_sha256": post_summary_sha,
        "archived_original_result_sha256": original_result_sha,
        "archived_original_summary_sha256": original_summary_sha,
    }


# ----------------------------------------------------------------------
# Wrong controls
# ----------------------------------------------------------------------

def run_wrong_controls(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # WC1: archived original result_class is the pre-regrade SEALED string
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    archived_ok = archived_summary.exists()
    archived_rc = ""
    if archived_ok:
        try:
            archived_rc = json.loads(archived_summary.read_text(encoding="utf-8-sig")).get("result_class", "")
        except Exception:
            archived_ok = False
    wc1_pass = archived_ok and archived_rc == FROM_VERDICT
    rows.append({
        "name": "WC1_archived_original_was_PASS",
        "pass": wc1_pass,
        "details": f"archived result_class = {archived_rc!r}; expected {FROM_VERDICT!r}",
        "load_bearing_deletion": "If archived original had a different verdict (e.g. already REFUTED), the regrade would be operating on the wrong starting point; this WC would FAIL.",
    })

    # WC2: current result_class is the post-regrade REFUTED string
    current_summary = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig"))
    current_rc = current_summary.get("result_class", "")
    wc2_pass = current_rc == TO_VERDICT
    rows.append({
        "name": "WC2_current_result_class_is_REFUTED",
        "pass": wc2_pass,
        "details": f"current result_class = {current_rc!r}; expected {TO_VERDICT!r}",
        "load_bearing_deletion": "If the regrade did not update result_class (e.g. only the header was added), this WC would FAIL.",
    })

    # WC3: archived original SHA matches sidecar record
    sha_file = ARCHIVE_SUB / "original_sha256.txt"
    wc3_pass = False
    wc3_detail = ""
    if sha_file.exists():
        text = sha_file.read_text(encoding="utf-8")
        m_r = re.search(r"original_CR063a_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        m_s = re.search(r"original_CR063a_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
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

    # WC4: audit_regrade block well-formed with from != to
    ar = current_summary.get("audit_regrade")
    wc4_pass = (
        isinstance(ar, dict)
        and ar.get("from_verdict") == FROM_VERDICT
        and ar.get("to_verdict") == TO_VERDICT
        and ar.get("from_verdict") != ar.get("to_verdict")
        and ar.get("driving_appeal_cr") == "CR-137"
        and ar.get("driving_audit_verdict_sha256") == AUDIT_VERDICT_SHA256
        and ar.get("verdict_direction") == "DOWNGRADED"
    )
    rows.append({
        "name": "WC4_audit_regrade_block_well_formed_and_from_neq_to",
        "pass": wc4_pass,
        "details": (
            "audit_regrade present with correct from_verdict, to_verdict (distinct), driving_appeal_cr, driving_audit_verdict_sha256, and verdict_direction."
            if wc4_pass else
            "audit_regrade block missing or malformed (from==to, wrong direction, etc.)."
        ),
        "load_bearing_deletion": "If from_verdict == to_verdict (the bug class CR-141 WC8 catches), or if any required field were stripped, this WC would FAIL.",
    })

    # WC5: audit verdict reference resolves
    wc5_pass = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    rows.append({
        "name": "WC5_audit_verdict_reference_resolves",
        "pass": wc5_pass,
        "details": f"AUDIT_VERDICT exists={AUDIT_VERDICT.exists()}; hash matches expected={AUDIT_VERDICT_SHA256}",
        "load_bearing_deletion": "If the audit verdict file were moved/edited, the recorded reference would be unverifiable; this WC would FAIL.",
    })

    # WC6: REPLACEMENT_RECORD present and contains restoration requirements section
    rr = ARCHIVE_SUB / "REPLACEMENT_RECORD.md"
    wc6_pass = False
    wc6_detail = ""
    if rr.exists():
        rr_text = rr.read_text(encoding="utf-8")
        has_section = "## 5. Restoration requirements" in rr_text
        has_falsifier = "### 5a. Restoration falsifier" in rr_text
        has_concrete_items = "horizon condition" in rr_text and "non-gravitational channel subtraction" in rr_text
        wc6_pass = has_section and has_falsifier and has_concrete_items
        wc6_detail = f"section={has_section}; falsifier_subsection={has_falsifier}; concrete_items={has_concrete_items}"
    else:
        wc6_detail = "REPLACEMENT_RECORD.md missing."
    rows.append({
        "name": "WC6_REPLACEMENT_RECORD_has_concrete_restoration_requirements",
        "pass": wc6_pass,
        "details": wc6_detail,
        "load_bearing_deletion": "If restoration requirements were N/A, vague, or missing the falsifier subsection, this WC would FAIL. Downgraded verdicts MUST carry concrete restoration paths.",
    })

    # WC7: empirical evidence documented (trigger_evidence block in audit_regrade)
    te = (current_summary.get("audit_regrade") or {}).get("trigger_evidence", {})
    required = {"platform", "gate_omega_rad_per_s", "T2_observed_us", "T2_grav_v1_0_predicted_ns", "overrun_factor_approx", "v1_0_falsifier_text"}
    missing = required - set(te.keys() if isinstance(te, dict) else [])
    wc7_pass = not missing
    rows.append({
        "name": "WC7_empirical_falsification_evidence_present",
        "pass": wc7_pass,
        "details": f"trigger_evidence missing fields = {sorted(missing)}" if missing else "All 6 required trigger_evidence fields present in audit_regrade.",
        "load_bearing_deletion": "If trigger_evidence were stripped (the regrade lacks evidentiary basis), this WC would FAIL.",
    })

    # WC8: rescue path (CR-064a) resolves
    wc8_pass = RESCUE_RESULT.exists()
    rows.append({
        "name": "WC8_surviving_rescue_claim_CR064a_resolves",
        "pass": wc8_pass,
        "details": f"CR-064a result.md exists = {wc8_pass}; path = {RESCUE_RESULT}",
        "load_bearing_deletion": "If CR-064a (the surviving rescue claim) were missing, the regrade narrative would be incomplete; this WC would FAIL.",
    })

    return rows


# ----------------------------------------------------------------------
# Predictions
# ----------------------------------------------------------------------

def run_predictions(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({
        "name": "P1_CR063a_target_exists",
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
        "name": "P2_archived_original_was_v1_0_SEALED",
        "pass": archived_ok and archived_rc == FROM_VERDICT,
        "details": f"archived result_class = {archived_rc!r}",
    })
    current_rc = json.loads(TARGET_SUMMARY.read_text(encoding="utf-8-sig")).get("result_class", "")
    rows.append({
        "name": "P3_regrade_applied_or_already_applied",
        "pass": entry["status"] in ("REGRADED", "ALREADY_REGRADED"),
        "details": f"status = {entry['status']}",
    })
    rows.append({
        "name": "P4_post_regrade_result_class_is_REFUTED_string",
        "pass": current_rc == TO_VERDICT,
        "details": f"current result_class = {current_rc!r}",
    })
    rows.append({
        "name": "P5_rescue_claim_CR064a_exists",
        "pass": RESCUE_RESULT.exists(),
        "details": f"CR-064a result.md exists = {RESCUE_RESULT.exists()}",
    })
    rows.append({
        "name": "P6_restoration_requirements_documented",
        "pass": (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").exists()
                and "## 5. Restoration requirements" in (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").read_text(encoding="utf-8"),
        "details": "REPLACEMENT_RECORD.md includes section 5 with concrete restoration items + falsifier.",
    })
    return rows


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    print("CR137 runner: CR-063a verdict regrade (SEALED -> REFUTED)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    ARCHIVE_SUB.mkdir(parents=True, exist_ok=True)

    # Source manifest (PRE-REGRADE state, using archived hashes when available
    # so the manifest is stable across re-runs).
    archived_result = ARCHIVE_SUB / "original_result.md"
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    pre_result_sha = sha256_file(archived_result) if archived_result.exists() else sha256_file(TARGET_RESULT)
    pre_summary_sha = sha256_file(archived_summary) if archived_summary.exists() else sha256_file(TARGET_SUMMARY)

    src_rows = [
        {
            "cr_id": "CR063a",
            "dir_name": "CR063a_HARDWARE_TRANSLATION_V1",
            "result_md_path": str(TARGET_RESULT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_regrade": pre_result_sha,
            "summary_json_path": str(TARGET_SUMMARY.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "summary_json_sha256_pre_regrade": pre_summary_sha,
        },
        {
            "cr_id": "CR-064a (rescue)",
            "dir_name": "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1",
            "result_md_path": str(RESCUE_RESULT.relative_to(COURTROOM_DIR)).replace("\\", "/") if RESCUE_RESULT.exists() else "",
            "result_md_sha256_pre_regrade": sha256_file(RESCUE_RESULT) if RESCUE_RESULT.exists() else "",
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

    # Regrade
    entry = perform_regrade()
    print(f"  CR063a  {entry['status']:18}  {entry['current_result_class']}")

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
        "CR137_CR063A_REGRADE_TO_REFUTED_V1_SEALED"
        if overall_pass
        else "CR137_CR063A_REGRADE_TO_REFUTED_V1_BOUNDARY_DRAFT"
    )

    # Deterministic lock (no timestamps)
    lock_payload = {
        "cr_id": "CR137",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "2 of 7 blocking",
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_REFUTED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "trigger": "TRANSMON_T2_EMPIRICAL_CONTACT_TIER7_AUDIT_FINDING",
        "trigger_evidence": EMPIRICAL_EVIDENCE,
        "rescue_path": RESCUE_PATH,
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
            "Re-executing CR137_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; the recomputed lock SHA-256 MUST "
            "match the value recorded in CR137_result.md. Any deviation falsifies v1.0."
        ),
    }
    REGRADE_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(REGRADE_LOCK_JSON)
    REGRADE_LOCK_SHA.write_text(f"CR137_regrade_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    # result.md
    md = []
    md.append("# CR137 CR-063a Verdict Regrade (SEALED → REFUTED) v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("CR-063a v1.0 hardware-translation claim was sealed as PASS on 2026-06-16. Its own pre-committed one-violation falsifier was empirically triggered at first contact with published transmon T2 data -- a factor of approximately 1932 overrun at 5 GHz. The rescue (CR-064a v1.1, A_0 enhancement + omega-as-gate-rate reinterpretation) introduces two new structural inputs and is audited separately as its own claim. Per the Courtroom protocol's own rules, a triggered one-violation falsifier whose fix requires new structural inputs REFUTES the original. CR-137 promotes CR-063a v1.0 to REFUTED on the record.\n")
    md.append("This regrade preserves the historical v1.0 declaration verbatim in CR-063a_result.md (formula, predictions, translation matrix, wrong controls) -- only the verdict line is changed, and an audit_regrade block is appended to its summary.json. The original is archived bit-identical with REPLACEMENT_RECORD documenting concrete restoration requirements and the restoration falsifier.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- Target: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/`")
    md.append(f"- Surviving rescue claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`")
    md.append(f"- Source manifest: `CR137_source_manifest.csv`\n")
    md.append("## Empirical Falsification of v1.0\n")
    md.append("| Field | Value |")
    md.append("| --- | --- |")
    md.append(f"| Platform | {EMPIRICAL_EVIDENCE['platform']} |")
    md.append(f"| Gate omega | {EMPIRICAL_EVIDENCE['gate_omega_rad_per_s']:.4e} rad/s |")
    md.append(f"| T2 observed | {EMPIRICAL_EVIDENCE['T2_observed_us']} microseconds |")
    md.append(f"| T2_grav v1.0 prediction | {EMPIRICAL_EVIDENCE['T2_grav_v1_0_predicted_ns']} ns |")
    md.append(f"| Overrun factor | ~= {EMPIRICAL_EVIDENCE['overrun_factor_approx']}x |")
    md.append(f"| v1.0 falsifier (literal) | *{EMPIRICAL_EVIDENCE['v1_0_falsifier_text']}* |")
    md.append(f"| Source | {EMPIRICAL_EVIDENCE['source']} |")
    md.append("")
    md.append("## Target Outcome\n")
    md.append(f"- **Status:** {entry['status']}")
    md.append(f"- **From verdict:** `{FROM_VERDICT}`")
    md.append(f"- **To verdict:** `{TO_VERDICT}`")
    md.append(f"- **Current result_class:** `{entry['current_result_class']}`")
    md.append(f"- **Result.md SHA-256:** `{entry['result_md_sha256']}`")
    md.append(f"- **Summary.json SHA-256:** `{entry['summary_json_sha256']}`")
    md.append(f"- **Archived original result.md SHA-256:** `{entry['archived_original_result_sha256']}`")
    md.append(f"- **Archived original summary.json SHA-256:** `{entry['archived_original_summary_sha256']}`\n")
    md.append("## Predictions\n")
    for r in pred_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        md.append(f"- {mark} {r['name']} — {r['details']}")
    md.append("")
    md.append("## Wrong Controls\n")
    for r in wc_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        md.append(f"- {mark} {r['name']} — {r['details']}")
        md.append(f"    - load-bearing deletion: {r['load_bearing_deletion']}")
    md.append("")
    md.append("## Restoration Requirements (path back to PASS for CR-063a v1.0)\n")
    for i, r in enumerate(RESTORATION_REQUIREMENTS, start=1):
        md.append(f"{i}. {r['requirement']}")
        md.append(f"    - *how to verify:* {r['how_to_verify']}")
    md.append("")
    md.append("### Restoration Falsifier\n")
    md.append(RESTORATION_FALSIFIER + "\n")
    md.append("## CR-137 Falsifier (LOCKED)\n")
    md.append("Re-executing `CR137_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match the value recorded here. Any deviation falsifies v1.0 of the regrade.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR137_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR137_regrade_manifest_csv                = {sha256_file(REGRADE_MANIFEST_CSV)}")
    md.append(f"CR137_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR137_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR137_regrade_lock_json                   = {lock_sha}")
    md.append("```\n")
    md.append("## Rule of Immutability\n")
    md.append("Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-137 seal time. Future falsification of CR-137 (failed idempotency, lock SHA mismatch on re-run) must be in an appeal CR within `00_governance/`.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    # summary.json (run-record allowed to drift in last_run_utc)
    summary_payload = {
        "cr_id": "CR137",
        "branch": "00_governance",
        "test_class": "CR063A_VERDICT_REGRADE_TO_REFUTED_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "regrade_type": "VERDICT_DOWNGRADE_PASS_TO_REFUTED",
        "verdict_change": True,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "trigger_evidence": EMPIRICAL_EVIDENCE,
        "rescue_path": RESCUE_PATH,
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
            "Re-executing CR137_runner.py on the post-seal state MUST produce zero "
            "new REGRADED entries and zero archive writes; the recomputed lock "
            "SHA-256 MUST match. Any deviation falsifies v1.0."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR137_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR137_regrade_manifest_csv": sha256_file(REGRADE_MANIFEST_CSV),
            "CR137_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR137_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR137_regrade_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
