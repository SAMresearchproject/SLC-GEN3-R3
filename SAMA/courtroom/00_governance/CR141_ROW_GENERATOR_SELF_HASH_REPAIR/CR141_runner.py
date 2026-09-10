"""CR141 Row-Generator Self-Hash Repair v1.0.

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661) found a
universal recorded-provenance defect in the row-generator suite: every
``*_result.md`` and ``*_summary.json`` in CR-128 through CR-134 cites a
``*_lock_sha256`` value that does NOT match the actual SHA-256 of the
corresponding ``*_lock.json`` on disk.

Root cause: the original row-generator runners computed the lock SHA-256
*before* embedding that hash into the lock JSON, then wrote the hash field
into the JSON.  The recorded value was therefore of the
lock-without-its-own-hash, while the on-disk file is the
lock-with-the-hash-embedded.  Downstream CRs (notably CR-060a) externally
re-hashed the lock and got the correct current-file values, so the
cross-CR chain is intact.  The defect is confined to the per-CR
self-citation.

Scope
-----
CR-141 is a recorded-provenance defect correction.  PASS verdicts on the
10 target CRs survive unchanged; only the recorded ``*_lock_sha256``
fields are corrected to match the on-disk lock files.

CR-141 is NOT a verdict change.  No claim is downgraded.  The forward-
looking structural fix to the row-generator runner template (so future
CRs do not have this artifact) is tracked separately as CR-141b.

Method
------
For each of the 10 target row-generator CRs:

  1. Compute the current SHA-256 of the lock JSON file.
  2. Read the recorded ``*_lock_sha256`` from result.md and summary.json.
  3. If recorded == actual AND the audit header block is present, mark
     the target ALREADY_REPAIRED and skip.
  4. Otherwise, copy result.md and summary.json bit-identical into
     archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/<NAME>/
     with original_sha256.txt recording their pre-repair hashes.
  5. Inject an audit-header block at the top of result.md and an
     ``audit_correction`` field at the top of summary.json.
  6. Replace every occurrence of the old hash with the new hash inside
     both files (including any echo in predictions / wrong controls).
  7. Generate the REPLACEMENT_RECORD.md in the archive folder.

After the per-target pass:

  8. Run the 7 wrong controls (each fails on a load-bearing deletion).
  9. Run the 6 predictions.
  10. Write source_manifest.csv, repair_manifest.csv,
      repair_lock.json + sibling sha256, result.md, summary.json.

Falsifier
---------
Re-executing this runner on the post-seal state MUST produce zero new
repairs and zero new archive entries.  Any change to the recorded state
on a clean re-run falsifies the v1.0 repair claim.

Free parameters: 0.  No fitted scores, no choice of which hash to record
beyond ``sha256(lock_json)``.

CR-141 is itself sealed under the same Courtroom discipline applied to
CR-128 through CR-134 by the CR-135 audit: declared formula, hashed
inputs, wrong controls, one-violation falsifier, archive of every
replaced artifact, and explicit restoration requirements where verdicts
change (N/A here -- this CR does not change verdicts).
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
ARCHIVE_ROOT = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "CR141_self_hash_repair"
AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_CRITERIA = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_CRITERIA.md"
ARCHIVE_README = COURTROOM_DIR / "archive" / "README.md"
TEMPLATE_PATH = COURTROOM_DIR / "archive" / "REPLACEMENT_RECORD_TEMPLATE.md"
EVENT_README = COURTROOM_DIR / "archive" / "2026-06-17_CR135_audit_regrades" / "EVENT_README.md"

AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR141_source_manifest.csv"
REPAIR_MANIFEST_CSV = CR_DIR / "CR141_repair_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR141_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR141_wrong_controls.csv"
REPAIR_LOCK_JSON = CR_DIR / "CR141_repair_lock.json"
REPAIR_LOCK_SHA = CR_DIR / "CR141_repair_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR141_result.md"
SUMMARY_JSON = CR_DIR / "CR141_summary.json"


# The 10 row-generator CRs the audit identified as carrying the
# self-hash defect.  Each entry: (directory_name, cr_id).  Lock file
# names and JSON field names are auto-discovered.
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


AUDIT_HEADER_MARKER = "AUDIT-DRIVEN DEFECT CORRECTION"


# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------

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


def find_lock_file(target_dir: Path) -> Path:
    locks = list(target_dir.glob("*lock*.json"))
    locks = [p for p in locks if "sha256" not in p.name.lower()]
    if len(locks) != 1:
        raise RuntimeError(f"expected exactly one lock json in {target_dir}, got {len(locks)}: {locks}")
    return locks[0]


def find_self_hash_field(summary_obj: dict[str, Any]) -> str:
    """Find the top-level field name ending in '_lock_sha256' that holds
    the self-hash of this CR's lock JSON."""
    candidates = [k for k in summary_obj.keys() if k.endswith("_lock_sha256")]
    if len(candidates) != 1:
        raise RuntimeError(f"expected exactly one *_lock_sha256 field, got {candidates}")
    return candidates[0]


def deep_replace_string(obj: Any, old: str, new: str) -> Any:
    if isinstance(obj, dict):
        return {k: deep_replace_string(v, old, new) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_replace_string(x, old, new) for x in obj]
    if isinstance(obj, str):
        return obj.replace(old, new)
    return obj


def reorder_with_audit_first(obj: dict[str, Any], audit_block: dict[str, Any]) -> dict[str, Any]:
    """Return a new dict with audit_correction first, then existing keys in order."""
    new_obj: dict[str, Any] = {"audit_correction": audit_block}
    for k, v in obj.items():
        if k == "audit_correction":
            continue  # we just placed it
        new_obj[k] = v
    return new_obj


# ----------------------------------------------------------------------
# Per-target repair
# ----------------------------------------------------------------------

def build_audit_header_md(
    cr_id: str,
    dir_name: str,
    field_name: str,
    old_hash: str,
    new_hash: str,
    result_class: str,
    original_result_sha: str,
) -> str:
    full_field = f"{cr_id}_{field_name}"
    return (
        f"> **{AUDIT_HEADER_MARKER} — 2026-06-17 PER CR-141**\n"
        f">\n"
        f"> The `{full_field}` field in this file was corrected from `{short(old_hash)}` to `{short(new_hash)}` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.\n"
        f">\n"
        f"> The verdict `{result_class}` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.\n"
        f">\n"
        f"> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/{dir_name}/original_result.md`\n"
        f"> - Original SHA-256: `{original_result_sha}`\n"
        f"> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/{dir_name}/REPLACEMENT_RECORD.md`\n"
        f"> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `{AUDIT_VERDICT_SHA256}`)\n"
        f"\n"
    )


def build_audit_correction_block(
    cr_id: str,
    dir_name: str,
    field_name: str,
    old_hash: str,
    new_hash: str,
    original_result_sha: str,
    original_summary_sha: str,
) -> dict[str, Any]:
    return {
        "applied_utc": now_utc(),
        "driving_appeal_cr": "CR-141",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "correction_type": "DEFECT_CORRECTION_RECORDED_PROVENANCE",
        "verdict_unchanged": True,
        "field_corrected": field_name,
        "old_value": old_hash,
        "new_value": new_hash,
        "root_cause": (
            "Runner self-reference artifact: lock SHA-256 was computed "
            "before being embedded in the lock JSON; recorded hash was "
            "therefore of the lock-without-its-own-hash while the on-disk "
            "file is the lock-with-the-hash-embedded."
        ),
        "archive_path": f"archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/{dir_name}/",
        "original_result_md_sha256": original_result_sha,
        "original_summary_json_sha256": original_summary_sha,
    }


def build_replacement_record_md(
    cr_id: str,
    dir_name: str,
    field_name: str,
    old_hash: str,
    new_hash: str,
    result_class: str,
    original_result_sha: str,
    original_summary_sha: str,
    post_result_sha: str,
    post_summary_sha: str,
    original_sealed_utc: str,
) -> str:
    full_field = f"{cr_id}_{field_name}"
    return f"""# REPLACEMENT_RECORD — {cr_id} self-hash defect repair

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `13_CERN_INDEPENDENT_TESTS/{dir_name}/{cr_id}_result.md` and `{cr_id}_summary.json` |
| Original result.md SHA-256 | `{original_result_sha}` |
| Original summary.json SHA-256 | `{original_summary_sha}` |
| Original verdict | `PASS — {result_class}` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `{post_result_sha}` |
| Replacement summary.json SHA-256 | `{post_summary_sha}` |
| Replacement verdict | `PASS — {result_class}` (unchanged) |
| Verdict direction | `DEFECT_CORRECTION` (recorded-provenance correction; no change to verdict or claim) |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-141 row-generator self-hash repair |
| Audit verdict SHA-256 | `{AUDIT_VERDICT_SHA256}` |
| Date | 2026-06-17 |
| Criterion failed | `C1 HASH_CHAIN_INTEGRITY` (self-citation defect) |
| Audit finding tier | Tier 2 PASS_WITH_REWORD (defect at the recorded-self-hash level; cross-CR chain intact) |

## 3. Defect summary

The `{full_field}` field recorded in both `{cr_id}_result.md` and `{cr_id}_summary.json` cited the value `{old_hash}`. The actual SHA-256 of the corresponding lock JSON on disk is `{new_hash}`.

**Root cause:** self-reference artifact in the runner. The runner computed the lock SHA-256 before writing the hash field into the lock JSON, then wrote the hash into the lock JSON. The recorded hash is therefore of the lock-without-its-own-hash; the file as it stands now is the lock-with-the-hash-embedded. Downstream CRs (notably CR-060a) that externally re-hashed the lock got the current actual value and chain correctly to it.

The defect does NOT invalidate the PASS verdict. The underlying claim, the in-sample matches, the forward-blind sub-predictions, and the wrong-controls all stand unchanged.

## 4. What changed

```text
Original line (in {cr_id}_result.md):
> {full_field}                     = {old_hash}

Replacement line:
> {full_field}                     = {new_hash}
```

```text
Original field (in {cr_id}_summary.json, "{field_name}"):
> "{field_name}": "{old_hash}"

Replacement field:
> "{field_name}": "{new_hash}"
```

Additionally, an audit-trail header block is prepended to `{cr_id}_result.md` linking to this archive entry, and an `audit_correction` object is prepended to `{cr_id}_summary.json`. Any echoed occurrence of the old hash inside predictions or wrong-controls strings is also replaced.

## 5. Restoration requirements (path back to prior grade)

`N/A — verdict unchanged`. This is a defect correction. The PASS verdict for `{result_class}` is preserved through the correction. No restoration is needed because nothing was downgraded.

### Forward-looking follow-up (NOT a restoration requirement, but a structural fix)

To prevent recurrence in future CRs, the runner pattern should be changed so that either:

1. **Option A (preferred):** the lock JSON does not contain its own SHA-256 — the hash is recorded only in the result.md and summary.json after the lock has been finalized; or
2. **Option B:** the runner computes the lock hash AFTER all writes including the self-hash embedding, then re-writes the lock once more with the final hash.

Either option eliminates the self-reference artifact at runtime. This is tracked as **CR-141b** (structural fix) and does NOT block the current repair.

### 5a. Restoration falsifier

`N/A — verdict unchanged`.

### 5b. Restoration CR forward-link

`N/A — verdict unchanged`. If the underlying {cr_id} law is ever falsified by a forward-blind violation per its own pre-committed sub-prediction, that triggers an *appeal* CR per the law's own falsifier — separate from this defect-correction event.

## 6. What this artifact still does NOT do

Unchanged from the original {cr_id} scope. The original "What {cr_id} Does NOT Claim" section in the result.md is preserved verbatim.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | {original_sealed_utc} | result.md `{short(original_result_sha)}` / summary.json `{short(original_summary_sha)}` | {cr_id} runner |
| Audit finding | 2026-06-17 | audit verdict `{short(AUDIT_VERDICT_SHA256)}` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `{short(post_result_sha)}` / summary.json `{short(post_summary_sha)}` | CR-141 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- Audit finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_{dir_name}.md`
- Event README: `../EVENT_README.md`
- CR-141 result: `00_governance/CR141_ROW_GENERATOR_SELF_HASH_REPAIR/CR141_result.md`
"""


def repair_one(dir_name: str, cr_id: str) -> dict[str, Any]:
    target_dir = TARGETS_DIR / dir_name
    result_path = target_dir / f"{cr_id}_result.md"
    summary_path = target_dir / f"{cr_id}_summary.json"
    lock_path = find_lock_file(target_dir)

    if not result_path.exists():
        raise RuntimeError(f"missing result.md: {result_path}")
    if not summary_path.exists():
        raise RuntimeError(f"missing summary.json: {summary_path}")

    # Read current state
    summary_obj = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    field_name = find_self_hash_field(summary_obj)
    recorded_hash = summary_obj[field_name]
    actual_hash = sha256_file(lock_path)
    result_class = summary_obj.get("result_class", "UNKNOWN")

    archive_dir = ARCHIVE_ROOT / dir_name
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Determine state
    result_text = result_path.read_text(encoding="utf-8")
    header_present = AUDIT_HEADER_MARKER in result_text
    audit_block_present = "audit_correction" in summary_obj

    if recorded_hash == actual_hash and header_present and audit_block_present:
        # Already repaired (idempotent re-run); verify archive exists
        original_result_sha = ""
        original_summary_sha = ""
        archived_result = archive_dir / "original_result.md"
        archived_summary = archive_dir / "original_summary.json"
        if archived_result.exists():
            original_result_sha = sha256_file(archived_result)
        if archived_summary.exists():
            original_summary_sha = sha256_file(archived_summary)
        return {
            "cr_id": cr_id,
            "dir_name": dir_name,
            "status": "ALREADY_REPAIRED",
            "field_name": field_name,
            "lock_actual_sha256": actual_hash,
            "recorded_sha256_now": recorded_hash,
            "result_md_sha256": sha256_file(result_path),
            "summary_json_sha256": sha256_file(summary_path),
            "archived_original_result_sha256": original_result_sha,
            "archived_original_summary_sha256": original_summary_sha,
            "result_class": result_class,
        }

    if recorded_hash == actual_hash and not header_present:
        # Hash already correct but never marked as audit-corrected
        # (e.g., the defect was fixed inadvertently by a non-CR141 edit).
        # Treat as anomaly so the curator can investigate.
        return {
            "cr_id": cr_id,
            "dir_name": dir_name,
            "status": "ANOMALY_HASH_OK_NO_HEADER",
            "field_name": field_name,
            "lock_actual_sha256": actual_hash,
            "recorded_sha256_now": recorded_hash,
            "result_md_sha256": sha256_file(result_path),
            "summary_json_sha256": sha256_file(summary_path),
            "archived_original_result_sha256": "",
            "archived_original_summary_sha256": "",
            "result_class": result_class,
        }

    # --------- NEEDS_REPAIR ---------

    # Capture pre-repair UTC from summary for chain of custody
    original_sealed_utc = summary_obj.get("utc", "UNKNOWN")

    # Copy bit-identical originals (only if not already archived)
    archived_result = archive_dir / "original_result.md"
    archived_summary = archive_dir / "original_summary.json"
    if not archived_result.exists():
        shutil.copy2(result_path, archived_result)
    if not archived_summary.exists():
        shutil.copy2(summary_path, archived_summary)

    original_result_sha = sha256_file(archived_result)
    original_summary_sha = sha256_file(archived_summary)
    (archive_dir / "original_sha256.txt").write_text(
        f"original_{cr_id}_result_md_sha256 = {original_result_sha}\n"
        f"original_{cr_id}_summary_json_sha256 = {original_summary_sha}\n",
        encoding="utf-8",
    )

    # Build summary.json with audit_correction prepended and hash replaced
    audit_block = build_audit_correction_block(
        cr_id=cr_id,
        dir_name=dir_name,
        field_name=field_name,
        old_hash=recorded_hash,
        new_hash=actual_hash,
        original_result_sha=original_result_sha,
        original_summary_sha=original_summary_sha,
    )
    # Order matters: replace embedded references in the BODY first
    # (predictions, wrong_controls, etc. may echo the old hash), THEN
    # prepend the audit_correction block. Otherwise the deep_replace
    # would clobber the literal old_value field inside audit_correction
    # itself, leaving old_value == new_value.
    modified_summary = deep_replace_string(summary_obj, recorded_hash, actual_hash)
    new_summary = reorder_with_audit_first(modified_summary, audit_block)
    summary_path.write_text(
        json.dumps(new_summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Build result.md with header block prepended and hash replaced
    header_block = build_audit_header_md(
        cr_id=cr_id,
        dir_name=dir_name,
        field_name=field_name,
        old_hash=recorded_hash,
        new_hash=actual_hash,
        result_class=result_class,
        original_result_sha=original_result_sha,
    )
    # Replace hash in result text first, then prepend header
    new_result_text = result_text.replace(recorded_hash, actual_hash)
    # Insert header before the first top-level heading (line starting with "# ")
    m = re.search(r"^# ", new_result_text, flags=re.MULTILINE)
    if m:
        # Place header after the first heading line (and its blank line if any)
        first_heading_end = new_result_text.find("\n", m.start())
        if first_heading_end == -1:
            first_heading_end = len(new_result_text)
        insert_at = first_heading_end + 1  # right after the newline of the heading
        new_result_text = (
            new_result_text[:insert_at]
            + "\n"
            + header_block
            + new_result_text[insert_at:]
        )
    else:
        new_result_text = header_block + new_result_text
    result_path.write_text(new_result_text, encoding="utf-8")

    # Re-hash post-repair
    post_result_sha = sha256_file(result_path)
    post_summary_sha = sha256_file(summary_path)

    # Write the per-artifact REPLACEMENT_RECORD
    record_md = build_replacement_record_md(
        cr_id=cr_id,
        dir_name=dir_name,
        field_name=field_name,
        old_hash=recorded_hash,
        new_hash=actual_hash,
        result_class=result_class,
        original_result_sha=original_result_sha,
        original_summary_sha=original_summary_sha,
        post_result_sha=post_result_sha,
        post_summary_sha=post_summary_sha,
        original_sealed_utc=original_sealed_utc,
    )
    (archive_dir / "REPLACEMENT_RECORD.md").write_text(record_md, encoding="utf-8")

    return {
        "cr_id": cr_id,
        "dir_name": dir_name,
        "status": "REPAIRED",
        "field_name": field_name,
        "lock_actual_sha256": actual_hash,
        "recorded_sha256_now": actual_hash,
        "old_recorded_sha256": recorded_hash,
        "result_md_sha256": post_result_sha,
        "summary_json_sha256": post_summary_sha,
        "archived_original_result_sha256": original_result_sha,
        "archived_original_summary_sha256": original_summary_sha,
        "result_class": result_class,
    }


# ----------------------------------------------------------------------
# Wrong controls (each one must FAIL on a load-bearing deletion)
# ----------------------------------------------------------------------

def run_wrong_controls(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # WC1: verdict line preserved across all 10 CRs.
    wc1_pass = True
    wc1_detail = ""
    for entry in manifest:
        if entry["status"] not in ("REPAIRED", "ALREADY_REPAIRED"):
            wc1_pass = False
            wc1_detail = f"{entry['cr_id']} status={entry['status']}"
            break
        # Re-read both archived original and current to confirm result_class
        target_dir = TARGETS_DIR / entry["dir_name"]
        summary_now = json.loads((target_dir / f"{entry['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
        archived_summary = ARCHIVE_ROOT / entry["dir_name"] / "original_summary.json"
        if not archived_summary.exists():
            wc1_pass = False
            wc1_detail = f"{entry['cr_id']} missing archived original"
            break
        original_summary = json.loads(archived_summary.read_text(encoding="utf-8-sig"))
        if summary_now.get("result_class") != original_summary.get("result_class"):
            wc1_pass = False
            wc1_detail = f"{entry['cr_id']} result_class changed: {original_summary.get('result_class')} -> {summary_now.get('result_class')}"
            break
    rows.append({
        "name": "WC1_verdict_line_preserved",
        "pass": wc1_pass,
        "details": wc1_detail or "All 10 target result_class fields preserved bit-identical from archived originals.",
        "load_bearing_deletion": "If any result_class value were altered, this WC would FAIL.",
    })

    # WC2: JSON parseability of all 10 summary.json files.
    wc2_pass = True
    wc2_detail = ""
    for entry in manifest:
        target_dir = TARGETS_DIR / entry["dir_name"]
        sp = target_dir / f"{entry['cr_id']}_summary.json"
        try:
            json.loads(sp.read_text(encoding="utf-8-sig"))
        except Exception as e:
            wc2_pass = False
            wc2_detail = f"{entry['cr_id']} parse error: {e}"
            break
    rows.append({
        "name": "WC2_summary_json_parseable",
        "pass": wc2_pass,
        "details": wc2_detail or "All 10 summary.json files parse as valid JSON post-repair.",
        "load_bearing_deletion": "If any summary.json were corrupted (e.g. missing brace), this WC would FAIL.",
    })

    # WC3: archived originals match recorded hash.
    wc3_pass = True
    wc3_detail = ""
    for entry in manifest:
        sha_file = ARCHIVE_ROOT / entry["dir_name"] / "original_sha256.txt"
        if not sha_file.exists():
            wc3_pass = False
            wc3_detail = f"{entry['cr_id']} missing original_sha256.txt"
            break
        text = sha_file.read_text(encoding="utf-8")
        result_match = re.search(r"original_\w+_result_md_sha256\s*=\s*([0-9a-f]{64})", text)
        summary_match = re.search(r"original_\w+_summary_json_sha256\s*=\s*([0-9a-f]{64})", text)
        if not (result_match and summary_match):
            wc3_pass = False
            wc3_detail = f"{entry['cr_id']} couldn't parse hash file"
            break
        archived_result = ARCHIVE_ROOT / entry["dir_name"] / "original_result.md"
        archived_summary = ARCHIVE_ROOT / entry["dir_name"] / "original_summary.json"
        if sha256_file(archived_result) != result_match.group(1):
            wc3_pass = False
            wc3_detail = f"{entry['cr_id']} archived result.md hash mismatch"
            break
        if sha256_file(archived_summary) != summary_match.group(1):
            wc3_pass = False
            wc3_detail = f"{entry['cr_id']} archived summary.json hash mismatch"
            break
    rows.append({
        "name": "WC3_archived_originals_hash_match",
        "pass": wc3_pass,
        "details": wc3_detail or "All 10 archived originals hash to the values recorded in their original_sha256.txt.",
        "load_bearing_deletion": "If any archived original were edited or corrupted, this WC would FAIL.",
    })

    # WC4: post-repair recorded hash matches actual lock SHA.
    wc4_pass = True
    wc4_detail = ""
    for entry in manifest:
        target_dir = TARGETS_DIR / entry["dir_name"]
        lock_path = find_lock_file(target_dir)
        actual = sha256_file(lock_path)
        summary_now = json.loads((target_dir / f"{entry['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
        recorded = summary_now.get(entry["field_name"])
        if recorded != actual:
            wc4_pass = False
            wc4_detail = f"{entry['cr_id']} recorded={recorded} actual={actual}"
            break
    rows.append({
        "name": "WC4_post_repair_self_hash_matches_actual",
        "pass": wc4_pass,
        "details": wc4_detail or "All 10 recorded *_lock_sha256 fields match the actual SHA-256 of their lock JSON.",
        "load_bearing_deletion": "If any lock JSON were modified or any recorded hash reverted, this WC would FAIL.",
    })

    # WC5: audit verdict reference resolves to a file whose SHA-256 is AUDIT_VERDICT_SHA256.
    wc5_pass = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    wc5_detail = (
        f"AUDIT_VERDICT path exists={AUDIT_VERDICT.exists()}; "
        f"hash matches expected={AUDIT_VERDICT_SHA256}"
    )
    rows.append({
        "name": "WC5_audit_verdict_reference_resolves",
        "pass": wc5_pass,
        "details": wc5_detail,
        "load_bearing_deletion": "If the audit verdict file were moved/edited, the recorded reference would be unverifiable; this WC would FAIL.",
    })

    # WC6: every REPLACEMENT_RECORD references existing files.
    wc6_pass = True
    wc6_detail = ""
    for entry in manifest:
        record = ARCHIVE_ROOT / entry["dir_name"] / "REPLACEMENT_RECORD.md"
        if not record.exists():
            wc6_pass = False
            wc6_detail = f"{entry['cr_id']} REPLACEMENT_RECORD.md missing"
            break
        # Confirm referenced cross-files exist
        for ref in [
            AUDIT_CRITERIA,
            AUDIT_VERDICT,
            EVENT_README,
        ]:
            if not ref.exists():
                wc6_pass = False
                wc6_detail = f"{entry['cr_id']} cross-reference {ref.name} missing"
                break
        if not wc6_pass:
            break
    rows.append({
        "name": "WC6_replacement_records_cross_refs_resolve",
        "pass": wc6_pass,
        "details": wc6_detail or "All 10 REPLACEMENT_RECORD.md files exist and their cross-referenced audit / event artifacts exist.",
        "load_bearing_deletion": "If any REPLACEMENT_RECORD or cross-referenced audit file were missing, this WC would FAIL.",
    })

    # WC7: post-repair audit_correction block present and well-formed.
    wc7_pass = True
    wc7_detail = ""
    required_fields = {
        "applied_utc", "driving_appeal_cr", "driving_audit_verdict_sha256",
        "correction_type", "verdict_unchanged", "field_corrected",
        "old_value", "new_value", "root_cause", "archive_path",
        "original_result_md_sha256", "original_summary_json_sha256",
    }
    for entry in manifest:
        target_dir = TARGETS_DIR / entry["dir_name"]
        summary_now = json.loads((target_dir / f"{entry['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
        ac = summary_now.get("audit_correction")
        if not isinstance(ac, dict):
            wc7_pass = False
            wc7_detail = f"{entry['cr_id']} missing audit_correction object"
            break
        missing = required_fields - set(ac.keys())
        if missing:
            wc7_pass = False
            wc7_detail = f"{entry['cr_id']} audit_correction missing fields: {sorted(missing)}"
            break
        if ac["driving_appeal_cr"] != "CR-141":
            wc7_pass = False
            wc7_detail = f"{entry['cr_id']} driving_appeal_cr != CR-141"
            break
        if ac["driving_audit_verdict_sha256"] != AUDIT_VERDICT_SHA256:
            wc7_pass = False
            wc7_detail = f"{entry['cr_id']} audit_correction verdict sha mismatch"
            break
        if ac["verdict_unchanged"] is not True:
            wc7_pass = False
            wc7_detail = f"{entry['cr_id']} audit_correction.verdict_unchanged != True"
            break
    rows.append({
        "name": "WC7_audit_correction_block_well_formed",
        "pass": wc7_pass,
        "details": wc7_detail or "All 10 audit_correction blocks present with all 12 required fields and verdict_unchanged=True.",
        "load_bearing_deletion": "If the audit_correction block were removed or any required field stripped, this WC would FAIL.",
    })

    # WC8: audit_correction.old_value != audit_correction.new_value AND
    # new_value matches the actual on-disk lock SHA-256.  Added during
    # initial seal review (2026-06-17) after a mid-seal bug-find: an
    # earlier draft of the runner applied deep_replace_string AFTER
    # prepending the audit_correction block, which clobbered the literal
    # old_value field, leaving old == new.  WC7 (field presence) did not
    # catch this because the field was present; the values were just both
    # the new hash.  WC8 catches the semantic gap WC7 missed.
    wc8_pass = True
    wc8_detail = ""
    hex64 = re.compile(r"^[0-9a-f]{64}$")
    for entry in manifest:
        target_dir = TARGETS_DIR / entry["dir_name"]
        summary_now = json.loads((target_dir / f"{entry['cr_id']}_summary.json").read_text(encoding="utf-8-sig"))
        ac = summary_now.get("audit_correction", {})
        old = ac.get("old_value", "")
        new = ac.get("new_value", "")
        if old == new:
            wc8_pass = False
            wc8_detail = f"{entry['cr_id']} audit_correction.old_value == new_value (no actual correction recorded)"
            break
        if not hex64.match(old):
            wc8_pass = False
            wc8_detail = f"{entry['cr_id']} audit_correction.old_value not 64-char hex SHA-256: {old!r}"
            break
        if not hex64.match(new):
            wc8_pass = False
            wc8_detail = f"{entry['cr_id']} audit_correction.new_value not 64-char hex SHA-256: {new!r}"
            break
        actual_lock_sha = sha256_file(find_lock_file(target_dir))
        if new != actual_lock_sha:
            wc8_pass = False
            wc8_detail = f"{entry['cr_id']} new_value {new[:12]} != actual lock SHA {actual_lock_sha[:12]}"
            break
    rows.append({
        "name": "WC8_audit_correction_records_actual_correction",
        "pass": wc8_pass,
        "details": wc8_detail or (
            "All 10 audit_correction blocks record a true correction "
            "(old_value != new_value, both valid 64-char SHA-256) and "
            "new_value matches the actual on-disk lock SHA-256."
        ),
        "load_bearing_deletion": (
            "If the runner clobbered old_value during deep_replace (the "
            "bug found mid-seal on 2026-06-17), this WC would FAIL. "
            "Closes the semantic gap WC7 missed."
        ),
    })

    return rows


# ----------------------------------------------------------------------
# Predictions (programmatic)
# ----------------------------------------------------------------------

def run_predictions(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    rows.append({
        "name": "P1_ten_targets_identified",
        "pass": len(manifest) == 10,
        "details": f"len(targets) = {len(manifest)} (expected 10)",
    })
    rows.append({
        "name": "P2_all_lock_jsons_exist",
        "pass": all((TARGETS_DIR / e["dir_name"] / f"{e['cr_id']}_law_lock.json").exists()
                    or any(p.exists() for p in (TARGETS_DIR / e["dir_name"]).glob("*lock*.json"))
                    for e in manifest),
        "details": "Each target directory contains exactly one *lock*.json file.",
    })
    rows.append({
        "name": "P3_all_result_md_exist",
        "pass": all((TARGETS_DIR / e["dir_name"] / f"{e['cr_id']}_result.md").exists() for e in manifest),
        "details": "All 10 *_result.md files exist at expected paths.",
    })
    rows.append({
        "name": "P4_all_summary_json_parse",
        "pass": all(
            (TARGETS_DIR / e["dir_name"] / f"{e['cr_id']}_summary.json").exists()
            and isinstance(
                json.loads((TARGETS_DIR / e["dir_name"] / f"{e['cr_id']}_summary.json").read_text(encoding="utf-8-sig")),
                dict,
            )
            for e in manifest
        ),
        "details": "All 10 *_summary.json files exist and parse as JSON dicts.",
    })
    rows.append({
        "name": "P5_all_targets_repaired_or_already_repaired",
        "pass": all(e["status"] in ("REPAIRED", "ALREADY_REPAIRED") for e in manifest),
        "details": "Every target has status REPAIRED or ALREADY_REPAIRED (no anomalies, no errors).",
    })
    rows.append({
        "name": "P6_all_recorded_hashes_match_actual_lock_hashes",
        "pass": all(e["recorded_sha256_now"] == e["lock_actual_sha256"] for e in manifest),
        "details": "Post-repair recorded *_lock_sha256 fields match SHA-256 of their lock JSON for all 10 CRs.",
    })

    return rows


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    print("CR141 runner: row-generator self-hash repair (idempotent)")
    print(f"Audit verdict SHA-256: {AUDIT_VERDICT_SHA256}")
    print(f"Targets: {len(TARGETS)}")
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    # ---- Source manifest ----
    # Captures the PRE-REPAIR state of each target's inputs. To keep the
    # manifest stable across re-runs, we prefer the archived original
    # SHA (which is bit-identical to the pre-repair file) when it exists;
    # we fall back to the current file SHA only when no archive exists
    # (i.e., on the very first run, before any repair has happened).
    # This way SOURCE_MANIFEST.csv is identical on every subsequent run.
    src_rows: list[dict[str, Any]] = []
    for dir_name, cr_id in TARGETS:
        target_dir = TARGETS_DIR / dir_name
        lock_path = find_lock_file(target_dir)
        result_path = target_dir / f"{cr_id}_result.md"
        summary_path = target_dir / f"{cr_id}_summary.json"

        archived_result = ARCHIVE_ROOT / dir_name / "original_result.md"
        archived_summary = ARCHIVE_ROOT / dir_name / "original_summary.json"
        pre_result_sha = sha256_file(archived_result) if archived_result.exists() else sha256_file(result_path)
        pre_summary_sha = sha256_file(archived_summary) if archived_summary.exists() else sha256_file(summary_path)

        src_rows.append({
            "cr_id": cr_id,
            "dir_name": dir_name,
            "lock_path": str(lock_path.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "lock_sha256": sha256_file(lock_path),
            "result_md_path": str(result_path.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "result_md_sha256_pre_repair": pre_result_sha,
            "summary_json_path": str(summary_path.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "summary_json_sha256_pre_repair": pre_summary_sha,
        })
    src_rows.append({
        "cr_id": "CR-135",
        "dir_name": "00_governance/CR135_HOSTILE_AUDIT_2026_06_17",
        "lock_path": str(AUDIT_VERDICT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
        "lock_sha256": sha256_file(AUDIT_VERDICT) if AUDIT_VERDICT.exists() else "",
        "result_md_path": "",
        "result_md_sha256_pre_repair": "",
        "summary_json_path": "",
        "summary_json_sha256_pre_repair": "",
    })
    write_csv(SOURCE_MANIFEST_CSV, src_rows)

    # ---- Per-target repair pass ----
    manifest: list[dict[str, Any]] = []
    for dir_name, cr_id in TARGETS:
        entry = repair_one(dir_name, cr_id)
        manifest.append(entry)
        print(f"  {cr_id:7} {entry['status']:18} lock_sha={entry['lock_actual_sha256'][:12]}...")

    # ---- Repair manifest CSV ----
    repair_rows: list[dict[str, Any]] = []
    for e in manifest:
        repair_rows.append({
            "cr_id": e["cr_id"],
            "dir_name": e["dir_name"],
            "status": e["status"],
            "field_name": e["field_name"],
            "result_class": e["result_class"],
            "lock_actual_sha256": e["lock_actual_sha256"],
            "recorded_sha256_now": e["recorded_sha256_now"],
            "old_recorded_sha256": e.get("old_recorded_sha256", ""),
            "post_result_md_sha256": e["result_md_sha256"],
            "post_summary_json_sha256": e["summary_json_sha256"],
            "archived_original_result_sha256": e["archived_original_result_sha256"],
            "archived_original_summary_sha256": e["archived_original_summary_sha256"],
        })
    write_csv(REPAIR_MANIFEST_CSV, repair_rows)

    # ---- Wrong controls + predictions ----
    wc_rows = run_wrong_controls(manifest)
    pred_rows = run_predictions(manifest)
    write_csv(WRONG_CONTROLS_CSV, wc_rows)
    write_csv(PREDICTIONS_CSV, pred_rows)

    wc_passed = sum(1 for r in wc_rows if r["pass"])
    pred_passed = sum(1 for r in pred_rows if r["pass"])
    repaired = sum(1 for e in manifest if e["status"] == "REPAIRED")
    already = sum(1 for e in manifest if e["status"] == "ALREADY_REPAIRED")
    anomalies = sum(1 for e in manifest if e["status"] not in ("REPAIRED", "ALREADY_REPAIRED"))

    print(f"\nRepaired now:        {repaired}")
    print(f"Already repaired:    {already}")
    print(f"Anomalies:           {anomalies}")
    print(f"Wrong controls:      {wc_passed}/{len(wc_rows)}")
    print(f"Predictions:         {pred_passed}/{len(pred_rows)}")

    overall_pass = (
        wc_passed == len(wc_rows)
        and pred_passed == len(pred_rows)
        and anomalies == 0
    )
    result_class = (
        "CR141_ROW_GENERATOR_SELF_HASH_REPAIR_V1_SEALED"
        if overall_pass
        else "CR141_ROW_GENERATOR_SELF_HASH_REPAIR_V1_BOUNDARY_DRAFT"
    )

    # ---- Repair lock JSON ----
    # Lock content is DETERMINISTIC by design: no timestamps, no counters
    # that depend on which run produced the repair. The lock represents
    # the *structural state* of the repair, not the runtime metadata.
    # Re-execution on the same state produces a bit-identical lock, so a
    # reviewer running the runner sees the same SHA recorded in result.md.
    # Combined "REPAIRED + ALREADY_REPAIRED" totals are reported instead
    # of the per-run split, so the count is stable across executions.
    lock_payload = {
        "cr_id": "CR141",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "1 of 7 blocking",
        "verdict_change": False,
        "correction_type": "DEFECT_CORRECTION_RECORDED_PROVENANCE",
        "targets": [{"cr_id": e["cr_id"], "dir_name": e["dir_name"],
                     "lock_actual_sha256": e["lock_actual_sha256"],
                     "result_class": e["result_class"]} for e in manifest],
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "targets_in_repaired_state": repaired + already,
        "targets_total": len(manifest),
        "anomaly_count": anomalies,
        "free_parameters": 0,
        "falsifier": (
            "Re-executing CR141_runner.py on the post-seal state of the 10 "
            "target CRs MUST produce zero new REPAIRED entries and zero "
            "new archive writes; the recomputed lock SHA-256 MUST match "
            "the value recorded in CR141_result.md. Any deviation "
            "falsifies v1.0."
        ),
    }
    REPAIR_LOCK_JSON.write_text(
        json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lock_sha = sha256_file(REPAIR_LOCK_JSON)
    REPAIR_LOCK_SHA.write_text(f"CR141_repair_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    # ---- result.md ----
    result_md_lines: list[str] = []
    result_md_lines.append("# CR141 Row-Generator Self-Hash Repair v1.0\n")
    result_md_lines.append("")
    result_md_lines.append("## Verdict\n")
    result_md_lines.append("")
    result_md_lines.append("```text")
    result_md_lines.append(result_class)
    result_md_lines.append("```\n")
    result_md_lines.append("## Scope\n")
    result_md_lines.append("")
    result_md_lines.append(
        "Recorded-provenance defect correction across the 10 row-generator CRs "
        "(CR-128 through CR-134) identified by the CR-135 hostile audit. Each "
        "target carried a `*_lock_sha256` field that did NOT match the actual "
        "SHA-256 of its lock JSON on disk; the cross-CR chain via CR-060a was "
        "intact, but each CR's self-citation was inconsistent. Root cause: "
        "runner self-reference artifact (lock hash computed before being "
        "embedded in the lock JSON).\n"
    )
    result_md_lines.append(
        "This CR is a DEFECT_CORRECTION. No verdict on any target CR is changed. "
        "The underlying claims, in-sample matches, partition algebras, "
        "forward-blind sub-predictions, and wrong controls all stand verbatim.\n"
    )
    result_md_lines.append("## Inputs (audit-verified)\n")
    result_md_lines.append("")
    result_md_lines.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    result_md_lines.append(f"- Targets: 10 row-generator CRs in `13_CERN_INDEPENDENT_TESTS/CR12[8-9]*/` and `CR13[0-4]*/`")
    result_md_lines.append(f"- Source manifest: `CR141_source_manifest.csv`\n")
    result_md_lines.append("## Per-Target Outcome\n")
    result_md_lines.append("")
    result_md_lines.append("| CR | Status | Field | Actual lock SHA-256 (first 12) | Result-class preserved |")
    result_md_lines.append("| --- | --- | --- | --- | --- |")
    for e in manifest:
        result_md_lines.append(
            f"| {e['cr_id']} | {e['status']} | `{e['field_name']}` | `{e['lock_actual_sha256'][:12]}...` | `{e['result_class']}` |"
        )
    result_md_lines.append("")
    result_md_lines.append(f"Targets in repaired state: **{repaired + already} / {len(manifest)}**.  Anomalies: **{anomalies}**.  (Run-time split — repaired now: {repaired}; already repaired: {already}.)\n")
    result_md_lines.append("## Predictions\n")
    result_md_lines.append("")
    for r in pred_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        result_md_lines.append(f"- {mark} {r['name']} — {r['details']}")
    result_md_lines.append("")
    result_md_lines.append("## Wrong Controls\n")
    result_md_lines.append("")
    for r in wc_rows:
        mark = "**[PASS]**" if r["pass"] else "**[FAIL]**"
        result_md_lines.append(f"- {mark} {r['name']} — {r['details']}")
        result_md_lines.append(f"    - load-bearing deletion: {r['load_bearing_deletion']}")
    result_md_lines.append("")
    result_md_lines.append("## Falsifier (LOCKED)\n")
    result_md_lines.append("")
    result_md_lines.append(
        "Re-executing `CR141_runner.py` on the post-seal state of the 10 target CRs "
        "MUST produce zero new `REPAIRED` entries and zero new archive writes. Any "
        "deviation (a target unexpectedly entering `REPAIRED` again, or any change to "
        "an archived original, or any mismatch between recorded and actual lock SHA-256) "
        "falsifies CR-141 v1.0 and triggers an appeal CR.\n"
    )
    result_md_lines.append("**Free parameters:** 0.\n")
    result_md_lines.append("## Restoration Requirements\n")
    result_md_lines.append("")
    result_md_lines.append(
        "N/A — CR-141 is a defect correction; no verdict is downgraded by "
        "this CR. Each target CR's underlying PASS verdict is preserved through "
        "the recorded-hash correction. Restoration paths for the underlying "
        "row-generator laws (if those laws are ever falsified by forward-blind "
        "row contact) live in each target's own pre-committed sub-prediction; "
        "they are not duplicated here.\n"
    )
    result_md_lines.append("## Cryptographic Chain\n")
    result_md_lines.append("")
    result_md_lines.append("```text")
    result_md_lines.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    result_md_lines.append(f"CR141_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    result_md_lines.append(f"CR141_repair_manifest_csv                 = {sha256_file(REPAIR_MANIFEST_CSV)}")
    result_md_lines.append(f"CR141_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    result_md_lines.append(f"CR141_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    result_md_lines.append(f"CR141_repair_lock_json                    = {lock_sha}")
    result_md_lines.append("```\n")
    result_md_lines.append("## Follow-up CRs\n")
    result_md_lines.append("")
    result_md_lines.append(
        "- **CR-141b** (structural fix): modify the row-generator runner template "
        "so that the lock JSON either omits its own self-hash, OR the runner "
        "re-hashes the lock after the self-hash field is embedded. Eliminates "
        "the self-reference artifact at the source so future CRs do not require "
        "CR-141-style repair.\n"
    )
    result_md_lines.append("## Rule of Immutability\n")
    result_md_lines.append("")
    result_md_lines.append(
        "Method, falsifier, wrong controls, and the 10-target scope are frozen at "
        "CR-141 seal time. Future falsification or refinement must be in an appeal "
        "CR within `00_governance/`.\n"
    )
    RESULT_MD.write_text("\n".join(result_md_lines), encoding="utf-8")

    # ---- summary.json ----
    # summary.json is the run-record; it carries timestamps and per-run
    # counts that are EXPECTED to drift between executions. The lock JSON
    # is the deterministic structural seal (see lock_payload above).
    summary_payload = {
        "cr_id": "CR141",
        "branch": "00_governance",
        "test_class": "ROW_GENERATOR_SELF_HASH_REPAIR_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "correction_type": "DEFECT_CORRECTION_RECORDED_PROVENANCE",
        "verdict_change": False,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "targets_total": len(manifest),
        "targets_in_repaired_state": repaired + already,
        "repaired_this_run": repaired,
        "already_repaired_this_run": already,
        "anomalies": anomalies,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "manifest": manifest,
        "predictions": pred_rows,
        "wrong_controls": wc_rows,
        "falsifier": (
            "Re-executing CR141_runner.py on the post-seal state MUST produce "
            "zero new REPAIRED entries and zero archive writes; any deviation "
            "falsifies v1.0."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR141_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR141_repair_manifest_csv": sha256_file(REPAIR_MANIFEST_CSV),
            "CR141_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR141_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR141_repair_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(
        json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
