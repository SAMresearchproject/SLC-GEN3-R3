"""CR139 CR-122 Verdict Language Regrade ("REJECTED" -> "DISFAVORED at 1.475 sigma").

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661)
Tier 3 finding: CR-122's headline claim states that direct qA-as-mass
is "REJECTED everywhere" at a max sigma of 1.475 against Planck
Omega_b h^2.  In standard inferential statistics, 1.475 sigma
corresponds to a one-sided p-value of approximately 0.14 -- a result
that DISFAVORS the alternative but does NOT reject it at any
conventional threshold (typically 2 sigma for "tension" or 3 sigma for
"strong tension").

The "REJECTED" framing is a categorical claim the evidence does not
support.  The underlying carrier-compression mechanism (1/8 unresolved
tensor carrier + 7/8 retained-write fraction; qA gates baryon/CMB
inventory through ledger compression rather than direct mass-routing)
is itself unaffected by this regrade -- the issue is the linguistic
strength of the rejection claim, not the structural content of CR-122.

Scope
-----
CR-139 regrades CR-122 from PASS to BOUNDARY, replacing "REJECTED
everywhere" language with "DISFAVORED at 1.475 sigma (p ~= 0.14)" and
documenting concrete restoration requirements for promoting to a
genuine rejection (Planck precision improvement, independent dataset
convergence, or theoretical structural argument).

CR-139 does NOT:

- Modify CR-122's runner.py, carrier_compression_gate_lock.json, or
  gated_cr_table.csv -- those are preserved verbatim.
- Refute the carrier-compression rule itself.
- Re-evaluate any of the 10 gated downstream CRs (CR016, CR018, CR019,
  CR020, CR021, CR022, CR023 in 07 and 08, CR111, CR114, CR117).  Those
  remain sealed with their original verdicts.
- Touch the qp092h source artifact (now resident at
  upstream_artifacts/qp092/qp092h_baryon_cmb_carrier_gate/ per CR-136).

Falsifier for CR-139 itself
---------------------------
Re-executing this runner on the post-seal state MUST produce zero new
REGRADED entries and zero new archive writes; the recomputed lock
SHA-256 MUST match the value recorded in CR139_result.md.

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
TARGET_DIR = COURTROOM_DIR / "00_governance" / "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE"
TARGET_RESULT = TARGET_DIR / "CR122_result.md"
TARGET_SUMMARY = TARGET_DIR / "CR122_summary.json"

INGEST_LOCK = COURTROOM_DIR / "00_governance" / "CR136_QP_CHAIN_INGEST" / "CR136_ingest_lock.json"
INGEST_LOCK_SHA = "2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c"
QP092H_INTERNAL = COURTROOM_DIR / "upstream_artifacts" / "qp092" / "qp092h_baryon_cmb_carrier_gate" / "qp092h_summary.json"
QP092H_EXPECTED_SHA = "5b8139aa90883b8b3ac210fdad44055fc9cbf23c6f4e16dbef58668a8d2bda49"

ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR139_CR122_regrade"
ARCHIVE_SUB = ARCHIVE_ROOT / "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR139_source_manifest.csv"
REGRADE_MANIFEST_CSV = CR_DIR / "CR139_regrade_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR139_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR139_wrong_controls.csv"
REGRADE_LOCK_JSON = CR_DIR / "CR139_regrade_lock.json"
REGRADE_LOCK_SHA = CR_DIR / "CR139_regrade_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR139_result.md"
SUMMARY_JSON = CR_DIR / "CR139_summary.json"

FROM_VERDICT = "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED"
TO_VERDICT = "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED"

HEADER_MARKER = "AUDIT-DRIVEN VERDICT REGRADE"

STATISTICAL_EVIDENCE = {
    "max_sigma_vs_planck": 1.4753,
    "approx_one_sided_p_value": 0.0701,
    "approx_two_sided_p_value": 0.1402,
    "overread_min_percent": 0.6631,
    "overread_mean_percent": 0.8808,
    "overread_max_percent": 0.9947,
    "conventional_rejection_threshold_sigma": 3.0,
    "conventional_tension_threshold_sigma": 2.0,
    "conclusion": (
        "1.475 sigma corresponds to a one-sided p-value of approximately 0.07 "
        "(two-sided ~0.14), which DISFAVORS direct qA-as-mass but does not "
        "REJECT it at conventional thresholds (typically 2-sigma for 'tension' "
        "and 3-sigma for 'strong tension')."
    ),
}

PRESERVED_MECHANISM = {
    "carrier_compression_rule": (
        "qA source support -> 1/8 unresolved tensor carrier -> ledger "
        "compression -> A readout (admitted route)"
    ),
    "rejected_alternative": "qA -> mass -> baryon/CMB readout (DIRECT_qA_AS_MASS)",
    "carrier_fraction": "1/8 (the unresolved tensor carrier from the closed-loop split)",
    "retained_fraction": "7/8 (visible mass identity from the closed-loop write)",
    "gated_downstream_crs": [
        "CR016 (CMB acoustic ruler photon road ratio)",
        "CR018 (A_0 * chi baryon inventory derivation)",
        "CR019 (effective matter inventory refinement)",
        "CR020 (CMB boundary + acoustic concept chain)",
        "CR021 (Planck-lite CMB density + BBN contact)",
        "CR022 (native A many-nonzero accumulation kernel; 08 branch)",
        "CR023 (baryon cosmology branch verdict; 07 branch)",
        "CR023 (BB-PBH / trapped-A inventory; 08 branch)",
        "CR111 (cosmic baryon Omega_b closure appeal)",
        "CR114 (cosmic baryon bridge reveal)",
        "CR117 (SAM/CMB methodological scope boundary)",
    ],
    "downstream_verdicts_unchanged": True,
    "rationale": (
        "The mechanism (carrier compression) is a structural framing of how "
        "qA enters inventory readouts; it is conceptually independent of the "
        "statistical strength of the rejection claim against direct-qA-as-mass. "
        "Even if direct-qA-as-mass is only DISFAVORED at 1.475 sigma rather "
        "than REJECTED, the carrier-compression route remains the SAM-native "
        "admission gate. The regrade is linguistic and statistical, not "
        "mechanistic."
    ),
}

RESTORATION_REQUIREMENTS = [
    {
        "requirement": (
            "Improved Planck-lite (or successor) precision on Omega_b h^2 such "
            "that the 0.66-0.99% overread interval corresponds to >= 3 sigma "
            "(conventional 'strong tension' threshold), promoting the disfavoring "
            "to a genuine rejection."
        ),
        "how_to_verify": (
            "Reviewer reads the Planck-lite (or successor) reported sigma on "
            "Omega_b h^2 in the current verified data release, computes "
            "0.66-0.99% as a sigma multiple, and confirms it crosses 3 sigma. "
            "Source verification (peer-reviewed paper or Planck Collaboration "
            "release) required."
        ),
    },
    {
        "requirement": (
            "Independent dataset (DES, SPT, ACT, or successor) reaching the same "
            "0.66-0.99% overread interval at >= 3 sigma significance, confirming "
            "the disfavoring is not Planck-specific."
        ),
        "how_to_verify": (
            "Reviewer reads the independent-dataset result, confirms a comparable "
            "overread is reported, confirms the sigma significance is >= 3, and "
            "confirms the dataset is genuinely independent of Planck (not a "
            "re-analysis of the same data)."
        ),
    },
    {
        "requirement": (
            "OR a theoretical structural argument internal to SAM that forbids "
            "direct-qA-as-mass independent of Planck contact (e.g., from CR-121's "
            "1/8 release mechanism plus a no-double-counting axiom). If "
            "structurally forbidden, the 1.475 sigma empirical contact is "
            "supporting evidence rather than the sole basis for rejection."
        ),
        "how_to_verify": (
            "Reviewer reads the structural argument, confirms it does not depend "
            "on the Planck-Omega_b comparison, and confirms it explicitly forbids "
            "the rejected route at the level of SAM's substrate-write grammar."
        ),
    },
]

RESTORATION_FALSIFIER = (
    "A high-precision dataset (Planck successor, joint Planck+DES, or any "
    "independent CMB+LSS combination) reaching the same 0.66-0.99% overread "
    "interval at LOWER sigma significance than current Planck-lite (e.g., 1.0 "
    "sigma) would BLOCK restoration, because the disfavoring would be weaker "
    "rather than stronger. Empirical regression of the disfavoring level is a "
    "blocking condition."
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
        "driving_appeal_cr": "CR-139",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "regrade_type": "VERDICT_DOWNGRADE_LANGUAGE_REJECTED_TO_DISFAVORED",
        "verdict_direction": "DOWNGRADED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "trigger": "CATEGORICAL_REJECTION_LANGUAGE_UNSUPPORTED_AT_1_475_SIGMA_TIER3_AUDIT_FINDING",
        "statistical_evidence": STATISTICAL_EVIDENCE,
        "preserved_mechanism": PRESERVED_MECHANISM,
        "ingest_dependency": {
            "cr": "CR-136",
            "lock_sha256": INGEST_LOCK_SHA,
            "qp092h_internal_path": str(QP092H_INTERNAL.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "qp092h_expected_sha": QP092H_EXPECTED_SHA,
        },
        "audit_finding_tier": "Tier 3 REGRADE_TO_BOUNDARY",
        "archive_path": "archive/2026-06-17_CR135_audit_regrades/CR139_CR122_regrade/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/",
        "original_result_md_sha256": original_result_sha,
        "original_summary_json_sha256": original_summary_sha,
        "replacement_record_path": "archive/2026-06-17_CR135_audit_regrades/CR139_CR122_regrade/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/REPLACEMENT_RECORD.md",
    }


def build_header_block(original_result_sha: str) -> str:
    return (
        f"> **{HEADER_MARKER} -- 2026-06-17 PER CR-139**\n"
        f">\n"
        f"> The verdict in this file is regraded from `{FROM_VERDICT}` to a BOUNDARY verdict because the headline language 'REJECTED everywhere' overstates the statistical evidence. The recorded max sigma vs Planck Omega_b h^2 is 1.4753, which corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14) -- a result that DISFAVORS direct qA-as-mass but does NOT reject it at conventional thresholds (typically 2 sigma for 'tension', 3 sigma for 'strong tension').\n"
        f">\n"
        f"> The underlying carrier-compression mechanism (1/8 unresolved tensor carrier + 7/8 retained-write fraction; qA gates baryon/CMB inventory through ledger compression rather than direct mass-routing) is **preserved**. So are the 10 gated downstream CRs (CR016, CR018-CR023, CR111, CR114, CR117). The regrade is linguistic and statistical, not mechanistic.\n"
        f">\n"
        f"> The qp092h source artifact is now resident internally at `upstream_artifacts/qp092/qp092h_baryon_cmb_carrier_gate/qp092h_summary.json` per CR-136 ingest; the recorded SHA `{QP092H_EXPECTED_SHA[:12]}...` resolves to a local file rather than to an external repository.\n"
        f">\n"
        f"> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR139_CR122_regrade/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/original_result.md`\n"
        f"> - Original SHA-256: `{original_result_sha}`\n"
        f"> - Replacement record (with restoration requirements + falsifier): `archive/2026-06-17_CR135_audit_regrades/CR139_CR122_regrade/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/REPLACEMENT_RECORD.md`\n"
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

    # Rewrite verdict
    pattern = re.compile(
        r"## Verdict\s*\n+```text\n" + re.escape(FROM_VERDICT) + r"\n```",
        re.MULTILINE,
    )
    replacement = (
        f"## Verdict (Regraded 2026-06-17 per CR-139)\n\n"
        f"```text\n{TO_VERDICT}\n```\n\n"
        f"**Prior verdict (preserved on the record):** `{FROM_VERDICT}` -- archived at the path in the header block above.\n\n"
        f"**Reason for regrade:** Tier 3 hostile-audit finding. The 'REJECTED everywhere' language describing direct qA-as-mass at 1.475 sigma overstates the statistical evidence; 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14), which DISFAVORS rather than rejects at conventional thresholds. The underlying carrier-compression mechanism and all 10 gated downstream CR verdicts are preserved."
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

    return f"""# REPLACEMENT_RECORD -- CR-122 verdict language regrade (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `00_governance/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/CR122_result.md` and `CR122_summary.json` |
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
| Audit / appeal CR | CR-139 CR-122 verdict language regrade |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (categorical rejection language unsupported by 1.475 sigma) |
| Audit finding tier | `Tier 3 REGRADE_TO_BOUNDARY` |
| Ingest dependency | CR-136 qp_chain ingest lock `{INGEST_LOCK_SHA}` |

## 3. Defect summary

CR-122's headline claim stated that direct qA-as-mass is "REJECTED everywhere" at a maximum significance of 1.4753 sigma against Planck Omega_b h^2. In conventional inferential statistics, 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14) -- a result that DISFAVORS the alternative but does NOT reject it. Conventional rejection thresholds are typically 2 sigma ("tension") or 3 sigma ("strong tension"); 1.475 sigma is below both.

The categorical "REJECTED" framing is a stronger statement than the 1.475 sigma evidence supports. The underlying carrier-compression mechanism (1/8 + qA = gravity path through ledger compression) is structurally meaningful and is **preserved** by this regrade. So are the 10 gated downstream CRs that ride on the mechanism. The regrade affects the linguistic strength of the rejection claim, not the structural content of CR-122.

## 4. What changed

- The verdict line in `CR122_result.md` is regraded from `{FROM_VERDICT}` to `{TO_VERDICT}`.
- The `result_class` field in `CR122_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR122_summary.json` documenting the statistical evidence, the preserved mechanism, and the CR-136 ingest dependency.
- A header block is prepended to `CR122_result.md` linking to this archive entry and explaining the disfavoring vs rejection distinction.
- The headline language inside the result.md (`Direct qA-as-mass would overread Planck Omega_b h^2 by 0.66-0.99 percent (max 1.475 sigma) - REJECTED everywhere.`) is **preserved verbatim as the historical declaration** so the regrade is auditable rather than silent. The header block + new verdict line provide the corrected interpretation.

## 5. Restoration requirements (path back to PASS)

To restore CR-122 to PASS (genuine "REJECTED" status), **any one** of the following must hold:

{restoration_lines}

### 5a. Restoration falsifier

{RESTORATION_FALSIFIER}

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite the specific verified dataset and confidence calculation supporting the >= 3 sigma claim

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-122 record does NOT:

- Refute the carrier-compression mechanism. The 1/8 + 7/8 split, ledger compression to A readout, and the admission gate for baryon/CMB inventory all remain SAM-native structural claims.
- Re-evaluate any of the 10 gated downstream CRs. CR016, CR018-CR023 (in 07 and 08), CR111, CR114, CR117 remain sealed with their original verdicts.
- Touch the qp092h source artifact. The internal copy at `upstream_artifacts/qp092/qp092h_baryon_cmb_carrier_gate/qp092h_summary.json` is unchanged from CR-136 ingest.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | {original_sealed_utc} | result.md `{short(original_result_sha)}` / summary.json `{short(original_summary_sha)}` | CR122 runner |
| Audit finding | 2026-06-17 | audit verdict `{short(AUDIT_VERDICT_SHA256)}` | CR-135 hostile audit |
| qp_chain ingest | 2026-06-17 | ingest lock `{short(INGEST_LOCK_SHA)}` | CR-136 ingest |
| Replacement sealed | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-139 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-122 finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR122.md`
- qp_chain ingest: `00_governance/CR136_QP_CHAIN_INGEST/CR136_result.md`
- Event README: `../EVENT_README.md`
- CR-139 result: `00_governance/CR139_CR122_REGRADE_LANGUAGE/CR139_result.md`
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
            "cr_id": "CR122",
            "dir_name": "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE",
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
            "cr_id": "CR122",
            "dir_name": "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE",
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
        f"original_CR122_result_md_sha256 = {original_result_sha}\n"
        f"original_CR122_summary_json_sha256 = {original_summary_sha}\n",
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
        "cr_id": "CR122",
        "dir_name": "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE",
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
        m_r = re.search(r"original_CR122_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        m_s = re.search(r"original_CR122_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
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
        "load_bearing_deletion": "If archived originals were edited/corrupted, this WC would FAIL.",
    })

    ar = current_summary.get("audit_regrade")
    wc4_pass = (
        isinstance(ar, dict)
        and ar.get("from_verdict") == FROM_VERDICT
        and ar.get("to_verdict") == TO_VERDICT
        and ar.get("from_verdict") != ar.get("to_verdict")
        and ar.get("driving_appeal_cr") == "CR-139"
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

    # WC6: CR-136 ingest dependency satisfied (qp092h resides internally with expected SHA)
    wc6_pass = QP092H_INTERNAL.exists() and sha256_file(QP092H_INTERNAL) == QP092H_EXPECTED_SHA
    rows.append({
        "name": "WC6_qp092h_ingest_dependency_satisfied",
        "pass": wc6_pass,
        "details": f"qp092h internal copy exists = {QP092H_INTERNAL.exists()}; SHA matches expected = {wc6_pass}",
        "load_bearing_deletion": "If qp092h were not internally ingested per CR-136, CR-139's narrative (carrier-compression mechanism preserved with internal hash resolution) would not hold.",
    })

    # WC7: statistical evidence present in audit_regrade
    se = ar.get("statistical_evidence", {}) if isinstance(ar, dict) else {}
    required_stat_fields = {"max_sigma_vs_planck", "approx_one_sided_p_value", "approx_two_sided_p_value", "conclusion"}
    missing = required_stat_fields - set(se.keys() if isinstance(se, dict) else [])
    wc7_pass = not missing and abs(se.get("max_sigma_vs_planck", 0) - 1.4753) < 0.001
    rows.append({
        "name": "WC7_statistical_evidence_documented",
        "pass": wc7_pass,
        "details": f"statistical_evidence missing = {sorted(missing)}; max_sigma_value_matches = {abs(se.get('max_sigma_vs_planck', 0) - 1.4753) < 0.001 if isinstance(se, dict) else False}",
        "load_bearing_deletion": "If statistical_evidence were stripped or sigma value altered, regrade rationale would be unsupported.",
    })

    # WC8: preserved mechanism documented and downstream verdicts marked unchanged
    pm = ar.get("preserved_mechanism", {}) if isinstance(ar, dict) else {}
    pm_ok = (
        isinstance(pm, dict)
        and pm.get("downstream_verdicts_unchanged") is True
        and isinstance(pm.get("gated_downstream_crs"), list)
        and len(pm["gated_downstream_crs"]) >= 10
    )
    rows.append({
        "name": "WC8_preserved_mechanism_and_downstream_verdicts_documented",
        "pass": pm_ok,
        "details": f"preserved_mechanism block has downstream_verdicts_unchanged=True and >= 10 gated CRs listed = {pm_ok}",
        "load_bearing_deletion": "If preserved_mechanism were stripped or downstream CR list were short, the regrade would risk being read as mechanism refutation.",
    })

    return rows


def run_predictions(entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({
        "name": "P1_CR122_target_exists",
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
        "pass": QP092H_INTERNAL.exists() and sha256_file(QP092H_INTERNAL) == QP092H_EXPECTED_SHA,
        "details": "qp092h internal copy present with expected SHA",
    })
    rows.append({
        "name": "P6_restoration_requirements_documented_with_concrete_items",
        "pass": (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").exists()
                and "Planck" in (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").read_text(encoding="utf-8")
                and "3 sigma" in (ARCHIVE_SUB / "REPLACEMENT_RECORD.md").read_text(encoding="utf-8"),
        "details": "REPLACEMENT_RECORD names Planck and 3 sigma threshold concretely.",
    })
    return rows


def main() -> None:
    print("CR139 runner: CR-122 verdict language regrade (SEALED -> BOUNDARY)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    ARCHIVE_SUB.mkdir(parents=True, exist_ok=True)

    archived_result = ARCHIVE_SUB / "original_result.md"
    archived_summary = ARCHIVE_SUB / "original_summary.json"
    pre_result_sha = sha256_file(archived_result) if archived_result.exists() else sha256_file(TARGET_RESULT)
    pre_summary_sha = sha256_file(archived_summary) if archived_summary.exists() else sha256_file(TARGET_SUMMARY)

    src_rows = [
        {
            "cr_id": "CR122",
            "dir_name": "CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE",
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
    print(f"  CR122  {entry['status']:18}  {entry['current_result_class'][:60]}...")

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
        "CR139_CR122_REGRADE_LANGUAGE_V1_SEALED"
        if overall_pass
        else "CR139_CR122_REGRADE_LANGUAGE_V1_BOUNDARY_DRAFT"
    )

    lock_payload = {
        "cr_id": "CR139",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "5 of 7 blocking",
        "regrade_type": "VERDICT_DOWNGRADE_LANGUAGE_REJECTED_TO_DISFAVORED",
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "statistical_evidence": STATISTICAL_EVIDENCE,
        "preserved_mechanism": PRESERVED_MECHANISM,
        "ingest_dependency": {
            "cr": "CR-136",
            "lock_sha256": INGEST_LOCK_SHA,
            "qp092h_internal_path": str(QP092H_INTERNAL.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "qp092h_expected_sha": QP092H_EXPECTED_SHA,
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
            "Re-executing CR139_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; the recomputed lock SHA-256 MUST "
            "match the value recorded in CR139_result.md."
        ),
    }
    REGRADE_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(REGRADE_LOCK_JSON)
    REGRADE_LOCK_SHA.write_text(f"CR139_regrade_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    md = []
    md.append("# CR139 CR-122 Verdict Language Regrade (SEALED -> BOUNDARY) v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("CR-122 sealed with the headline language 'Direct qA-as-mass would overread Planck Omega_b h^2 by 0.66-0.99 percent (max 1.475 sigma) - REJECTED everywhere.' The hostile audit identified this as a Tier 3 categorical-language overclaim: 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14), which DISFAVORS the alternative but does NOT reject it at conventional thresholds. CR-139 regrades the verdict from PASS to BOUNDARY, preserves the historical declaration verbatim for audit traceability, and adds an audit_regrade block to summary.json plus a header block to result.md documenting the disfavoring-vs-rejection distinction.\n")
    md.append("The underlying carrier-compression mechanism (1/8 + qA -> ledger compression -> A readout) is PRESERVED. The 10 gated downstream CRs (CR016, CR018-CR023 in 07 and 08, CR111, CR114, CR117) remain sealed with their original verdicts -- they ride on the mechanism, not on the statistical strength of the rejection claim.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- qp_chain ingest lock: `00_governance/CR136_QP_CHAIN_INGEST/CR136_ingest_lock.json` (`{INGEST_LOCK_SHA}`)")
    md.append(f"- Target: `00_governance/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/`")
    md.append(f"- Source manifest: `CR139_source_manifest.csv`\n")
    md.append("## Statistical Evidence\n")
    md.append("| Quantity | Value |")
    md.append("| --- | --- |")
    for k, v in STATISTICAL_EVIDENCE.items():
        if k == "conclusion":
            continue
        md.append(f"| {k} | {v} |")
    md.append("")
    md.append(f"**Conclusion:** {STATISTICAL_EVIDENCE['conclusion']}\n")
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
    md.append("## Restoration Requirements (path back to PASS for CR-122)\n")
    md.append("To restore CR-122 to PASS (genuine 'REJECTED' status), **any one** of the following must hold:\n")
    for i, r in enumerate(RESTORATION_REQUIREMENTS, start=1):
        md.append(f"{i}. {r['requirement']}")
        md.append(f"    - *how to verify:* {r['how_to_verify']}")
    md.append("")
    md.append("### Restoration Falsifier\n")
    md.append(RESTORATION_FALSIFIER + "\n")
    md.append("## CR-139 Falsifier (LOCKED)\n")
    md.append("Re-executing `CR139_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR136_ingest_lock_sha256                  = {INGEST_LOCK_SHA}")
    md.append(f"CR139_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR139_regrade_manifest_csv                = {sha256_file(REGRADE_MANIFEST_CSV)}")
    md.append(f"CR139_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR139_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR139_regrade_lock_json                   = {lock_sha}")
    md.append("```\n")
    md.append("## Rule of Immutability\n")
    md.append("Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-139 seal time. Future falsification must be in an appeal CR.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    summary_payload = {
        "cr_id": "CR139",
        "branch": "00_governance",
        "test_class": "CR122_VERDICT_LANGUAGE_REGRADE_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "regrade_type": "VERDICT_DOWNGRADE_LANGUAGE_REJECTED_TO_DISFAVORED",
        "verdict_change": True,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "from_verdict": FROM_VERDICT,
        "to_verdict": TO_VERDICT,
        "statistical_evidence": STATISTICAL_EVIDENCE,
        "preserved_mechanism": PRESERVED_MECHANISM,
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
            "Re-executing CR139_runner.py on the post-seal state MUST produce zero new "
            "REGRADED entries and zero archive writes; recomputed lock SHA-256 MUST match."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR136_ingest_lock_sha256": INGEST_LOCK_SHA,
            "CR139_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR139_regrade_manifest_csv": sha256_file(REGRADE_MANIFEST_CSV),
            "CR139_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR139_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR139_regrade_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
