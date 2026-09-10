"""CR142 Row-Generator In-Sample Qualifier Sweep.

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661)
finding: across the row-generator suite (CR-128 through CR-134), the
"zero free parameters" rhetoric appears at the headline level but the
honest in-sample disclosure (each law was extracted inductively from
the CR-119 catalog) lives further down inside wrong-controls (WC3 in
most cases).  A reviewer skimming the headline sees "zero free
parameters" without immediately seeing the qualifier that the
generator-consistency claim is in-sample.

Note: WC3-type disclosure passes 10/10 in CR-135's audit -- the
disclosure IS there.  The issue is headline-level visibility, not
omission.  CR-142 surfaces the qualifier to the top of each result.md
with a dedicated header block that names the in-sample status explicitly
and points the reader at the existing WC3 disclosure for full context.

Scope
-----
CR-142 is a HEADLINE QUALIFICATION; not a verdict change, not a content
modification beyond the prepended header block.  The PASS verdicts on
the 10 target CRs survive unchanged.  The formulas, in-sample matches,
partition algebras, predictions, and existing wrong controls all stand
verbatim.  Only an additional CR-142 header block is added on top of
each result.md (alongside the existing CR-141 header block), and a
companion `audit_qualifier` field is added to summary.json.

Idempotency
-----------
Re-execution on the post-seal state sees the CR-142 header marker
already present and skips, reporting ALREADY_QUALIFIED.

Falsifier
---------
Re-executing this runner on the post-seal state MUST produce zero new
QUALIFIED entries and zero new archive writes; the recomputed lock
SHA-256 MUST match the value recorded in CR142_result.md.

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
TARGETS_DIR = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS"
ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR142_qualifier_sweep"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR142_source_manifest.csv"
QUALIFIER_MANIFEST_CSV = CR_DIR / "CR142_qualifier_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR142_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR142_wrong_controls.csv"
QUALIFIER_LOCK_JSON = CR_DIR / "CR142_qualifier_lock.json"
QUALIFIER_LOCK_SHA = CR_DIR / "CR142_qualifier_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR142_result.md"
SUMMARY_JSON = CR_DIR / "CR142_summary.json"

TARGETS: list[tuple[str, str]] = [
    ("CR128_BOUND_COLOR_PAIR_MASS_LAW_V1",                "CR128"),
    ("CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1",            "CR128b"),
    ("CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1",           "CR129"),
    ("CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1",             "CR129b"),
    ("CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON",    "CR129c"),
    ("CR130_2BODY_3BODY_STRUCTURAL_BRIDGE",               "CR130"),
    ("CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1",     "CR131"),
    ("CR132_1BODY_CARRIER_LATTICE_LAW_V1",                "CR132"),
    ("CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1",  "CR133"),
    ("CR134_SOURCE_SUPPORT_PACKET_LAW_V1",                "CR134"),
]

CR142_HEADER_MARKER = "IN-SAMPLE QUALIFIER -- 2026-06-17 PER CR-142"


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


def reorder_with_audit_first(obj: dict[str, Any], block: dict[str, Any], key_name: str) -> dict[str, Any]:
    new_obj: dict[str, Any] = {key_name: block}
    for k, v in obj.items():
        if k == key_name:
            continue
        new_obj[k] = v
    return new_obj


def build_qualifier_header(cr_id: str, dir_name: str, pre_qualifier_result_sha: str) -> str:
    return (
        f"> **{CR142_HEADER_MARKER}**\n"
        f">\n"
        f"> Headline rhetoric in this CR uses 'zero free parameters' / 'free_parameters = 0' "
        f"language. That language is technically accurate in the strict sense (no scalar "
        f"parameter fitted post-hoc) but requires the following qualifier at the headline "
        f"level for honest interpretation:\n"
        f">\n"
        f"> **In-sample qualifier:** The {cr_id} law was extracted inductively from the "
        f"CR-119 catalog (via cluster inspection in CR-127 for some, direct row analysis "
        f"for others). The reported in-sample match (e.g., 36/36 for CR-128) is therefore "
        f"GENERATOR CONSISTENCY against the training data, NOT first-principles derivation. "
        f"The forward-blind falsifier (the `CR<N>_PRED_1` sub-prediction) commits the law "
        f"to FORWARD-BLIND testing on FUTURE rows; overfit cannot operate there. The "
        f"existing wrong control `WC3_law_derived_from_data_not_first_principles` (or "
        f"equivalent) carries the full disclosure; this header surfaces it to the top.\n"
        f">\n"
        f"> The PASS verdict on this CR survives the qualifier. The framework's structural "
        f"content (cross-class regularity across 10 operator classes from {{R=12, D=3, "
        f"alpha_H=2, partition algebra}}) is the substantive signal; the in-sample status "
        f"affects how the headline should be read, not whether the underlying claim holds.\n"
        f">\n"
        f"> - Pre-qualifier state archived at: `archive/2026-06-17_CR135_audit_regrades/"
        f"CR142_qualifier_sweep/{dir_name}/pre_qualifier_result.md`\n"
        f"> - Pre-qualifier SHA-256: `{pre_qualifier_result_sha}`\n"
        f"> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR142_qualifier_sweep/"
        f"{dir_name}/REPLACEMENT_RECORD.md`\n"
        f"> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` "
        f"(verdict SHA-256 `{AUDIT_VERDICT_SHA256}`)\n"
        f"\n"
    )


def build_audit_qualifier_block(cr_id: str, dir_name: str, pre_result_sha: str, pre_summary_sha: str) -> dict[str, Any]:
    return {
        "applied_utc": now_utc(),
        "driving_appeal_cr": "CR-142",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "qualifier_type": "HEADLINE_IN_SAMPLE_DISCLOSURE",
        "verdict_unchanged": True,
        "qualifier_summary": (
            "Law extracted inductively from CR-119 catalog; reported in-sample match "
            "is GENERATOR CONSISTENCY against training data, not first-principles "
            "derivation. Forward-blind falsifier (PRED_1) commits the law to "
            "forward-blind testing on future rows. Existing WC3-equivalent wrong "
            "control carries the full disclosure; this qualifier surfaces it to the "
            "headline level."
        ),
        "audit_finding_tier": "Tier 2 PASS_WITH_REWORD (headline visibility of in-sample qualifier)",
        "archive_path": f"archive/2026-06-17_CR135_audit_regrades/CR142_qualifier_sweep/{dir_name}/",
        "pre_qualifier_result_md_sha256": pre_result_sha,
        "pre_qualifier_summary_json_sha256": pre_summary_sha,
        "predecessor_appeal_cr": "CR-141 (self-hash repair; pre-qualifier state is the post-CR141 state)",
    }


def qualify_one(dir_name: str, cr_id: str) -> dict[str, Any]:
    target_dir = TARGETS_DIR / dir_name
    result_path = target_dir / f"{cr_id}_result.md"
    summary_path = target_dir / f"{cr_id}_summary.json"
    if not result_path.exists() or not summary_path.exists():
        return {"cr_id": cr_id, "dir_name": dir_name, "status": "MISSING_TARGET"}

    archive_dir = ARCHIVE_ROOT / dir_name
    archive_dir.mkdir(parents=True, exist_ok=True)

    result_text = result_path.read_text(encoding="utf-8")
    summary_obj = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    header_present = CR142_HEADER_MARKER in result_text
    qualifier_block_present = "audit_qualifier" in summary_obj

    if header_present and qualifier_block_present:
        archived_pre = archive_dir / "pre_qualifier_result.md"
        return {
            "cr_id": cr_id,
            "dir_name": dir_name,
            "status": "ALREADY_QUALIFIED",
            "result_md_sha256": sha256_file(result_path),
            "summary_json_sha256": sha256_file(summary_path),
            "archived_pre_result_sha256": sha256_file(archived_pre) if archived_pre.exists() else "",
        }

    # Archive the PRE-qualifier (i.e., post-CR141) state
    archived_result = archive_dir / "pre_qualifier_result.md"
    archived_summary = archive_dir / "pre_qualifier_summary.json"
    if not archived_result.exists():
        shutil.copy2(result_path, archived_result)
    if not archived_summary.exists():
        shutil.copy2(summary_path, archived_summary)
    pre_result_sha = sha256_file(archived_result)
    pre_summary_sha = sha256_file(archived_summary)
    (archive_dir / "pre_qualifier_sha256.txt").write_text(
        f"pre_qualifier_{cr_id}_result_md_sha256 = {pre_result_sha}\n"
        f"pre_qualifier_{cr_id}_summary_json_sha256 = {pre_summary_sha}\n",
        encoding="utf-8",
    )

    # Add qualifier block to summary.json (prepended)
    qualifier_block = build_audit_qualifier_block(cr_id, dir_name, pre_result_sha, pre_summary_sha)
    new_summary = reorder_with_audit_first(summary_obj, qualifier_block, "audit_qualifier")
    summary_path.write_text(json.dumps(new_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Add qualifier header to result.md (after first heading, alongside any CR-141 header)
    header_block = build_qualifier_header(cr_id, dir_name, pre_result_sha)
    m = re.search(r"^# ", result_text, flags=re.MULTILINE)
    if m:
        first_heading_end = result_text.find("\n", m.start())
        if first_heading_end == -1:
            first_heading_end = len(result_text)
        # Insert after first heading line
        insert_at = first_heading_end + 1
        new_result_text = result_text[:insert_at] + "\n" + header_block + result_text[insert_at:]
    else:
        new_result_text = header_block + result_text
    result_path.write_text(new_result_text, encoding="utf-8")

    post_result_sha = sha256_file(result_path)
    post_summary_sha = sha256_file(summary_path)

    # REPLACEMENT_RECORD
    record_md = f"""# REPLACEMENT_RECORD -- {cr_id} in-sample qualifier addition

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original (pre-CR142) path | `13_CERN_INDEPENDENT_TESTS/{dir_name}/{cr_id}_result.md` and `{cr_id}_summary.json` |
| Pre-qualifier result.md SHA-256 | `{pre_result_sha}` |
| Pre-qualifier summary.json SHA-256 | `{pre_summary_sha}` |
| Predecessor state | post-CR-141 self-hash repair (see `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/{dir_name}/`) |
| Post-qualifier result.md SHA-256 | `{post_result_sha}` |
| Post-qualifier summary.json SHA-256 | `{post_summary_sha}` |
| Verdict | unchanged |
| Verdict direction | `QUALIFIER_ADDITION` (headline visibility correction; no verdict change) |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-142 row-generator in-sample qualifier sweep |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion partially addressed | `C5 IN_SAMPLE_DISCLOSED` (was passing in WC3 but lacked headline visibility) |
| Audit finding tier | `Tier 2 PASS_WITH_REWORD` |

## 3. Defect summary

{cr_id}'s in-sample disclosure was present in its wrong controls (WC3_law_derived_from_data_not_first_principles or equivalent) and passed CR-135's C5 check. The audit's recommendation was that the qualifier should be surfaced to the headline level so a reviewer skimming the result.md sees the in-sample status alongside the "zero free parameters" claim, not after scrolling through several sections.

## 4. What changed

- A CR-142 in-sample qualifier header block is prepended to `{cr_id}_result.md` (after any existing CR-141 header block).
- An `audit_qualifier` object is prepended to `{cr_id}_summary.json` documenting the qualifier addition and pointing at the existing WC3 disclosure.
- The original formula, in-sample matches, predictions, and existing wrong controls are preserved verbatim. The PASS verdict on {cr_id} is unchanged.

## 5. Restoration requirements

`N/A -- verdict unchanged`. This is a headline-visibility correction. The qualifier MAY be removed from the headline if and when the underlying law passes a forward-blind test against new catalog rows (resolving CR<N>_PRED_1 cleanly). At that point a new appeal CR documents the forward-blind confirmation and the qualifier can be deprecated to a footnote.

## 6. What this artifact still does NOT do

Unchanged from the original {cr_id} scope. The qualifier addition does not modify any structural claim, predictions, wrong controls, or downstream consumers.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | (predates CR-141) | (see CR-141 archive) | {cr_id} runner |
| Post-CR-141 (self-hash repair) | 2026-06-17 | result.md `{short(pre_result_sha)}` / summary.json `{short(pre_summary_sha)}` | CR-141 runner |
| Post-CR-142 (qualifier added) | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-142 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Predecessor appeal CR (self-hash repair): `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/`
- Event README: `../EVENT_README.md`
- CR-142 result: `00_governance/CR142_ROW_GEN_QUALIFIER_SWEEP/CR142_result.md`
"""
    (archive_dir / "REPLACEMENT_RECORD.md").write_text(record_md, encoding="utf-8")

    return {
        "cr_id": cr_id,
        "dir_name": dir_name,
        "status": "QUALIFIED",
        "result_md_sha256": post_result_sha,
        "summary_json_sha256": post_summary_sha,
        "archived_pre_result_sha256": pre_result_sha,
    }


def run_predictions(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({
        "name": "P1_ten_targets_identified",
        "pass": len(results) == 10,
        "details": f"len(results) = {len(results)} (expected 10)",
    })
    clean = sum(1 for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED"))
    rows.append({
        "name": "P2_all_targets_qualified_or_already_qualified",
        "pass": clean == len(results),
        "details": f"in-clean-state: {clean}/{len(results)}",
    })
    rows.append({
        "name": "P3_pre_qualifier_archive_present_per_target",
        "pass": all(r.get("archived_pre_result_sha256", "") != "" for r in results),
        "details": "every target has a pre_qualifier_result.md archived with recorded SHA",
    })
    rows.append({
        "name": "P4_summary_json_has_audit_qualifier_field",
        "pass": all(
            "audit_qualifier" in json.loads((TARGETS_DIR / r["dir_name"] / f"{r['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
            for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED")
        ),
        "details": "audit_qualifier object present in every qualified summary.json",
    })
    rows.append({
        "name": "P5_result_md_has_qualifier_header",
        "pass": all(
            CR142_HEADER_MARKER in (TARGETS_DIR / r["dir_name"] / f"{r['cr_id']}_result.md").read_text(encoding="utf-8")
            for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED")
        ),
        "details": "CR142 qualifier header marker present in every qualified result.md",
    })
    rows.append({
        "name": "P6_verdicts_unchanged",
        "pass": all(
            "_SEALED" in json.loads((TARGETS_DIR / r["dir_name"] / f"{r['cr_id']}_summary.json").read_text(encoding="utf-8-sig")).get("result_class", "")
            for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED")
        ),
        "details": "result_class on every target still contains _SEALED suffix (no verdict change)",
    })
    return rows


def run_wrong_controls(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    bad = sum(1 for r in results if r["status"] not in ("QUALIFIED", "ALREADY_QUALIFIED"))
    rows.append({
        "name": "WC1_no_anomalous_statuses",
        "pass": bad == 0,
        "details": f"anomalous: {bad}",
        "load_bearing_deletion": "If any target had MISSING_TARGET or any other anomalous status, this WC would FAIL.",
    })

    # WC2: no verdict drift (result_class still contains SEALED)
    verdict_ok = True
    detail = ""
    for r in results:
        target_dir = TARGETS_DIR / r["dir_name"]
        try:
            j = json.loads((target_dir / f"{r['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
            if "_SEALED" not in j.get("result_class", ""):
                verdict_ok = False
                detail = f"{r['cr_id']} result_class lacks _SEALED: {j.get('result_class')}"
                break
        except Exception as e:
            verdict_ok = False
            detail = f"{r['cr_id']}: {e}"
            break
    rows.append({
        "name": "WC2_no_verdict_drift",
        "pass": verdict_ok,
        "details": detail or "every target's result_class still contains _SEALED (verdict preserved)",
        "load_bearing_deletion": "If any target's verdict were altered by this sweep, this WC would FAIL.",
    })

    # WC3: pre_qualifier_sha256.txt content matches archive
    sha_ok = True
    detail = ""
    for r in results:
        if r["status"] not in ("QUALIFIED", "ALREADY_QUALIFIED"):
            continue
        sha_file = ARCHIVE_ROOT / r["dir_name"] / "pre_qualifier_sha256.txt"
        archived_result = ARCHIVE_ROOT / r["dir_name"] / "pre_qualifier_result.md"
        archived_summary = ARCHIVE_ROOT / r["dir_name"] / "pre_qualifier_summary.json"
        if not (sha_file.exists() and archived_result.exists() and archived_summary.exists()):
            sha_ok = False
            detail = f"{r['cr_id']} archive incomplete"
            break
        text = sha_file.read_text(encoding="utf-8")
        m_r = re.search(r"pre_qualifier_\w+_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        m_s = re.search(r"pre_qualifier_\w+_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
        if not (m_r and m_s and sha256_file(archived_result) == m_r.group(1) and sha256_file(archived_summary) == m_s.group(1)):
            sha_ok = False
            detail = f"{r['cr_id']} archived hash mismatch"
            break
    rows.append({
        "name": "WC3_pre_qualifier_archive_hashes_match",
        "pass": sha_ok,
        "details": detail or "every pre_qualifier archive's stored SHAs match the file content",
        "load_bearing_deletion": "If any archived pre-state were edited/corrupted, this WC would FAIL.",
    })

    # WC4: audit_qualifier blocks well-formed
    blocks_ok = True
    detail = ""
    required = {"applied_utc", "driving_appeal_cr", "driving_audit_verdict_sha256",
                "qualifier_type", "verdict_unchanged", "qualifier_summary",
                "audit_finding_tier", "archive_path"}
    for r in results:
        if r["status"] not in ("QUALIFIED", "ALREADY_QUALIFIED"):
            continue
        j = json.loads((TARGETS_DIR / r["dir_name"] / f"{r['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
        aq = j.get("audit_qualifier", {})
        missing = required - set(aq.keys() if isinstance(aq, dict) else [])
        if missing or aq.get("driving_appeal_cr") != "CR-142" or aq.get("verdict_unchanged") is not True:
            blocks_ok = False
            detail = f"{r['cr_id']}: missing={sorted(missing)}, driving_appeal_cr={aq.get('driving_appeal_cr')}, verdict_unchanged={aq.get('verdict_unchanged')}"
            break
    rows.append({
        "name": "WC4_audit_qualifier_blocks_well_formed",
        "pass": blocks_ok,
        "details": detail or "every audit_qualifier block has all required fields + driving_appeal_cr=CR-142 + verdict_unchanged=True",
        "load_bearing_deletion": "If any audit_qualifier block were stripped or fields removed, this WC would FAIL.",
    })

    # WC5: REPLACEMENT_RECORD present per target with concrete pre/post hashes
    rr_ok = True
    detail = ""
    for r in results:
        if r["status"] not in ("QUALIFIED", "ALREADY_QUALIFIED"):
            continue
        rr = ARCHIVE_ROOT / r["dir_name"] / "REPLACEMENT_RECORD.md"
        if not rr.exists():
            rr_ok = False
            detail = f"{r['cr_id']} REPLACEMENT_RECORD missing"
            break
        text = rr.read_text(encoding="utf-8")
        # Must contain pre and post SHAs
        if not re.search(r"Pre-qualifier result\.md SHA-256.+`[0-9a-f]{64}`", text):
            rr_ok = False
            detail = f"{r['cr_id']} REPLACEMENT_RECORD missing pre SHA"
            break
        if not re.search(r"Post-qualifier result\.md SHA-256.+`[0-9a-f]{64}`", text):
            rr_ok = False
            detail = f"{r['cr_id']} REPLACEMENT_RECORD missing post SHA"
            break
    rows.append({
        "name": "WC5_REPLACEMENT_RECORDs_complete_with_hashes",
        "pass": rr_ok,
        "details": detail or "every REPLACEMENT_RECORD present with pre and post SHAs",
        "load_bearing_deletion": "If any REPLACEMENT_RECORD lacked the pre or post SHA, the chain of custody would break.",
    })

    # WC6: audit verdict reference resolves
    wc6_pass = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    rows.append({
        "name": "WC6_audit_verdict_reference_resolves",
        "pass": wc6_pass,
        "details": f"AUDIT_VERDICT exists={AUDIT_VERDICT.exists()}; hash matches",
        "load_bearing_deletion": "If audit verdict moved/edited, this WC would FAIL.",
    })

    # WC7: result.md still contains the CR-141 audit header (i.e., previous appeal preserved)
    cr141_preserved = all(
        "AUDIT-DRIVEN DEFECT CORRECTION" in (TARGETS_DIR / r["dir_name"] / f"{r['cr_id']}_result.md").read_text(encoding="utf-8")
        for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED")
    )
    rows.append({
        "name": "WC7_CR141_audit_header_preserved",
        "pass": cr141_preserved,
        "details": "CR-141 'AUDIT-DRIVEN DEFECT CORRECTION' marker present in every result.md alongside CR-142 qualifier",
        "load_bearing_deletion": "If CR-142's edit removed CR-141's header, the audit chain would be broken; this WC would FAIL.",
    })

    return rows


def main() -> None:
    print("CR142 runner: row-generator in-sample qualifier sweep (10 targets)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    # ---- Source manifest ----
    src_rows = []
    for dir_name, cr_id in TARGETS:
        target_dir = TARGETS_DIR / dir_name
        result_path = target_dir / f"{cr_id}_result.md"
        summary_path = target_dir / f"{cr_id}_summary.json"
        archived_pre = ARCHIVE_ROOT / dir_name / "pre_qualifier_result.md"
        pre_sha = sha256_file(archived_pre) if archived_pre.exists() else sha256_file(result_path)
        src_rows.append({
            "cr_id": cr_id,
            "dir_name": dir_name,
            "result_md_path": str(result_path.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "pre_qualifier_result_md_sha256": pre_sha,
        })
    src_rows.append({
        "cr_id": "CR-135 (audit)",
        "dir_name": "CR135_HOSTILE_AUDIT_2026_06_17",
        "result_md_path": str(AUDIT_VERDICT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
        "pre_qualifier_result_md_sha256": sha256_file(AUDIT_VERDICT) if AUDIT_VERDICT.exists() else "",
    })
    write_csv(SOURCE_MANIFEST_CSV, src_rows)

    # ---- Per-target qualifier sweep ----
    results: list[dict[str, Any]] = []
    for dir_name, cr_id in TARGETS:
        r = qualify_one(dir_name, cr_id)
        results.append(r)
        print(f"  {cr_id:7} {r['status']:20}")

    # Stable manifest
    stable_rows = []
    for r in results:
        stable_rows.append({
            "cr_id": r["cr_id"],
            "dir_name": r["dir_name"],
            "in_clean_state": r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED"),
            "result_md_sha256_post": r.get("result_md_sha256", ""),
            "summary_json_sha256_post": r.get("summary_json_sha256", ""),
            "archived_pre_result_sha256": r.get("archived_pre_result_sha256", ""),
        })
    write_csv(QUALIFIER_MANIFEST_CSV, stable_rows)

    wc_rows = run_wrong_controls(results)
    pred_rows = run_predictions(results)
    write_csv(WRONG_CONTROLS_CSV, wc_rows)
    write_csv(PREDICTIONS_CSV, pred_rows)

    wc_passed = sum(1 for r in wc_rows if r["pass"])
    pred_passed = sum(1 for r in pred_rows if r["pass"])
    clean = sum(1 for r in results if r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED"))

    print(f"\nWrong controls: {wc_passed}/{len(wc_rows)}")
    print(f"Predictions:    {pred_passed}/{len(pred_rows)}")

    overall_pass = (
        wc_passed == len(wc_rows)
        and pred_passed == len(pred_rows)
        and clean == len(results)
    )
    result_class = (
        "CR142_ROW_GEN_QUALIFIER_SWEEP_V1_SEALED"
        if overall_pass
        else "CR142_ROW_GEN_QUALIFIER_SWEEP_V1_BOUNDARY_DRAFT"
    )

    lock_payload = {
        "cr_id": "CR142",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "7 of 7 blocking (final blocker)",
        "qualifier_type": "HEADLINE_IN_SAMPLE_DISCLOSURE_SWEEP",
        "verdict_change_on_targets": False,
        "targets_total": len(results),
        "targets_in_clean_state": clean,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "qualifiers": [
            {
                "cr_id": r["cr_id"],
                "dir_name": r["dir_name"],
                "in_clean_state": r["status"] in ("QUALIFIED", "ALREADY_QUALIFIED"),
            }
            for r in sorted(results, key=lambda x: x["cr_id"])
        ],
        "free_parameters": 0,
        "falsifier": (
            "Re-executing CR142_runner.py on the post-seal state MUST produce zero new "
            "QUALIFIED entries (only ALREADY_QUALIFIED) and zero archive writes; the "
            "recomputed lock SHA-256 MUST match the value recorded in CR142_result.md."
        ),
    }
    QUALIFIER_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(QUALIFIER_LOCK_JSON)
    QUALIFIER_LOCK_SHA.write_text(f"CR142_qualifier_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    md = []
    md.append("# CR142 Row-Generator In-Sample Qualifier Sweep v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("Sweeps the row-generator suite (CR-128 through CR-134, 10 CRs) to surface the in-sample qualifier to the headline level. Each target carries a 'zero free parameters' claim in its headline and an existing in-sample disclosure in its WC3-equivalent wrong control. CR-135's audit found C5 disclosure passes 10/10 -- the disclosure IS there -- but the headline rhetoric should reference the qualifier explicitly. CR-142 prepends an `IN-SAMPLE QUALIFIER` header block to each result.md and adds an `audit_qualifier` object to each summary.json. PASS verdicts are unchanged. The formulas, in-sample matches, predictions, and existing wrong controls all stand verbatim.\n")
    md.append("This sweep operates on the post-CR-141 state of each target. The CR-141 audit header (self-hash defect correction) is preserved; CR-142's qualifier header is added alongside it, not in place of it. A reviewer reading any row-generator result.md now sees both audit-driven corrections at the headline level.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- Targets: 10 row-generator CRs in `13_CERN_INDEPENDENT_TESTS/`")
    md.append(f"- Source manifest: `CR142_source_manifest.csv`\n")
    md.append("## Per-Target Outcome\n")
    md.append("| CR | Status |")
    md.append("| --- | --- |")
    for r in results:
        md.append(f"| {r['cr_id']} | {r['status']} |")
    md.append("")
    md.append(f"Targets in clean state: **{clean} / {len(results)}**.\n")
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
    md.append("## Falsifier (LOCKED)\n")
    md.append("Re-executing `CR142_runner.py` on the post-seal state MUST produce zero new `QUALIFIED` entries (only `ALREADY_QUALIFIED`) and zero archive writes; the recomputed lock SHA-256 MUST match the value recorded here.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Restoration Requirements\n")
    md.append("`N/A -- verdict unchanged`. The qualifier surfaces existing disclosure. It MAY be deprecated to a footnote when the underlying CR<N>_PRED_1 forward-blind test resolves cleanly against new catalog rows.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR142_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR142_qualifier_manifest_csv              = {sha256_file(QUALIFIER_MANIFEST_CSV)}")
    md.append(f"CR142_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR142_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR142_qualifier_lock_json                 = {lock_sha}")
    md.append("```\n")
    md.append("## Rule of Immutability\n")
    md.append("Qualifier wording, sweep scope, wrong controls, and falsifier are frozen at CR-142 seal time.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    summary_payload = {
        "cr_id": "CR142",
        "branch": "00_governance",
        "test_class": "ROW_GENERATOR_QUALIFIER_SWEEP_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "qualifier_type": "HEADLINE_IN_SAMPLE_DISCLOSURE_SWEEP",
        "verdict_change_on_targets": False,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "targets_total": len(results),
        "targets_in_clean_state": clean,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "wrong_controls": wc_rows,
        "predictions": pred_rows,
        "manifest": stable_rows,
        "falsifier": (
            "Re-executing CR142_runner.py on the post-seal state MUST produce zero new "
            "QUALIFIED entries (only ALREADY_QUALIFIED); recomputed lock SHA-256 MUST match."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR142_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR142_qualifier_manifest_csv": sha256_file(QUALIFIER_MANIFEST_CSV),
            "CR142_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR142_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR142_qualifier_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
