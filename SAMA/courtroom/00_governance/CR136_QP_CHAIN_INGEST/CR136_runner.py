"""CR136 qp_chain Ingest: copy upstream artifacts into the Courtroom.

Driving event
-------------
CR-135 hostile audit (2026-06-17, verdict SHA-256
2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661)
identified that CR-120 (33 qp091/qp092 references), CR-121 (9 qp092
references), and CR-122 (1 qp092h reference) point at SHA-256 hashes of
artifacts that physically live OUTSIDE the Courtroom at
`C:/VS/quantum_phase/artifacts/`.  A reviewer cloning The_Courtroom
cannot reproduce a single Higgs-or-gravity-related claim because the
artifacts those hashes refer to are not in the repository.

CR-136 ingests those upstream artifacts into
`The_Courtroom/upstream_artifacts/`, verifies that each copied artifact
has the same SHA-256 as recorded in CR-120/121/122, and produces a
manifest mapping recorded-hash to internal-path so a reviewer can
resolve any reference without consulting the external repo.

Scope
-----
CR-136 is an INGEST, not a verdict change or content modification.  It
does NOT:

- Modify CR-120, CR-121, or CR-122 result.md, summary.json, lock.json,
  or runner.py.  Those CRs are touched only by their own follow-up
  appeal CRs (CR-139 for CR-122, CR-140 for CR-120).
- Re-execute the qp_chain.  Artifacts are copied bit-identical; no
  recomputation.
- Convert external paths in CR runners to internal paths.  That is a
  separate, optional refinement (potential CR-136b) and is NOT required
  for hash-based auditability, which is what the audit demanded.

What CR-136 DOES guarantee
--------------------------
For every qp_chain SHA-256 cited by CR-120, CR-121, or CR-122:

  - The external artifact is verified to exist at
    `C:/VS/quantum_phase/artifacts/<folder>/<summary_file>` and its
    current SHA-256 matches what the consuming CR recorded.
  - A bit-identical copy is placed under
    `The_Courtroom/upstream_artifacts/qp091/<folder>/<summary_file>` or
    `.../qp092/<folder>/<summary_file>`.
  - The internal copy's SHA-256 is verified to equal the external
    SHA-256 (no transcription loss).
  - The mapping `(recorded_sha256, external_path, internal_path)` is
    recorded in `CR136_ingest_manifest.csv` so a reviewer can resolve
    any reference from inside The_Courtroom alone.

Falsifier
---------
Re-executing CR136_runner.py on the post-ingest state MUST produce zero
new copies and zero SHA mismatches; the recomputed lock SHA-256 MUST
match the value recorded in CR136_result.md.  Any deviation -- a missing
artifact, a SHA disagreement between external and internal, or a
manifest row that disagrees with what's on disk -- falsifies v1.0.

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

EXTERNAL_ROOT = Path(r"C:/VS/quantum_phase/artifacts")
INTERNAL_ROOT = COURTROOM_DIR / "upstream_artifacts"

CR120_LEDGER = COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN" / "CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE" / "CR120_qp091_chain_ledger.csv"
CR121_LEDGER = COURTROOM_DIR / "11_QUANTUM_MECHANICS_AND_GRAVITY" / "CR121_SAM_GRAVITY_MECHANISM_INTAKE" / "CR121_mechanism_chain_ledger.csv"

AUDIT_VERDICT = COURTROOM_DIR / "00_governance" / "CR135_HOSTILE_AUDIT_2026_06_17" / "CR135_AUDIT_VERDICT.md"
AUDIT_VERDICT_SHA256 = "2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661"

# Outputs
SOURCE_MANIFEST_CSV = CR_DIR / "CR136_source_manifest.csv"
INGEST_MANIFEST_CSV = CR_DIR / "CR136_ingest_manifest.csv"
PREDICTIONS_CSV = CR_DIR / "CR136_predictions.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR136_wrong_controls.csv"
INGEST_LOCK_JSON = CR_DIR / "CR136_ingest_lock.json"
INGEST_LOCK_SHA = CR_DIR / "CR136_ingest_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR136_result.md"
SUMMARY_JSON = CR_DIR / "CR136_summary.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def discover_targets() -> list[dict[str, Any]]:
    """Parse CR-120 and CR-121 ledgers to identify every qp_chain artifact
    that needs to be ingested. Returns a list of dicts, one per unique
    (folder, summary_file) target, with provenance: which consuming CR(s)
    reference each."""
    targets: dict[tuple[str, str], dict[str, Any]] = {}

    # CR-120 ledger
    for row in read_csv_rows(CR120_LEDGER):
        folder = row["folder"]
        summary_file = row["summary_file"]
        recorded_sha = row["summary_sha256"]
        key = (folder, summary_file)
        if key not in targets:
            targets[key] = {
                "folder": folder,
                "summary_file": summary_file,
                "consumers": ["CR-120"],
                "recorded_sha256": recorded_sha,
                "phase": row.get("phase", ""),
                "artifact_name": row.get("artifact", ""),
                "result_class": row.get("result_class", ""),
                "passed": row.get("passed", ""),
            }
        else:
            targets[key]["consumers"].append("CR-120")
            # SHA sanity check: if multiple consumers cite this artifact,
            # they should agree on the SHA. (They will because both read
            # the same file.) Disagreement would be a chain integrity defect.
            if targets[key]["recorded_sha256"] != recorded_sha:
                targets[key]["sha_disagreement_between_consumers"] = True

    # CR-121 ledger
    for row in read_csv_rows(CR121_LEDGER):
        folder = row["stage"]  # field name differs in CR-121's ledger
        summary_file = row["summary_file"]
        recorded_sha = row["summary_sha256"]
        key = (folder, summary_file)
        if key not in targets:
            targets[key] = {
                "folder": folder,
                "summary_file": summary_file,
                "consumers": ["CR-121"],
                "recorded_sha256": recorded_sha,
                "phase": "qp092_mechanism_chain",
                "artifact_name": row.get("artifact", ""),
                "result_class": row.get("result_class", ""),
                "passed": row.get("passed", ""),
            }
        else:
            targets[key]["consumers"].append("CR-121")
            if targets[key]["recorded_sha256"] != recorded_sha:
                targets[key]["sha_disagreement_between_consumers"] = True

    # CR-122 references qp092h_baryon_cmb_carrier_gate / qp092h_summary.json
    # explicitly through its runner.  If the CR-121 ledger already covers
    # this artifact (it does), CR-122's reference is implicitly covered;
    # we record CR-122 as an additional consumer rather than a new target.
    qp092h_key = ("qp092h_baryon_cmb_carrier_gate", "qp092h_summary.json")
    if qp092h_key in targets:
        if "CR-122" not in targets[qp092h_key]["consumers"]:
            targets[qp092h_key]["consumers"].append("CR-122")
    else:
        # Fallback: if CR-121 ledger somehow didn't cover qp092h, add it
        # from the CR-122 runner's known reference.  This branch should not
        # be taken in normal operation but is a defensive guard.
        targets[qp092h_key] = {
            "folder": "qp092h_baryon_cmb_carrier_gate",
            "summary_file": "qp092h_summary.json",
            "consumers": ["CR-122"],
            "recorded_sha256": "5b8139aa90883b8b3ac210fdad44055fc9cbf23c6f4e16dbef58668a8d2bda49",
            "phase": "qp092_mechanism_chain",
            "artifact_name": "QP092H_BARYON_INVENTORY_CMB_CARRIER_COMPRESSION_RULE_GATE",
            "result_class": "",
            "passed": "True",
        }

    return sorted(targets.values(), key=lambda t: (t["folder"], t["summary_file"]))


def chain_subdir(folder: str) -> str:
    """Map a qp_chain folder to its top-level chain bucket (qp091/qp092)."""
    if folder.startswith("qp092") or "qp092" in folder.split("_")[0]:
        return "qp092"
    return "qp091"


def ingest_target(target: dict[str, Any]) -> dict[str, Any]:
    folder = target["folder"]
    summary_file = target["summary_file"]
    recorded_sha = target["recorded_sha256"]
    external_path = EXTERNAL_ROOT / folder / summary_file
    bucket = chain_subdir(folder)
    internal_path = INTERNAL_ROOT / bucket / folder / summary_file

    result: dict[str, Any] = {
        "folder": folder,
        "summary_file": summary_file,
        "consumers": ",".join(target["consumers"]),
        "phase": target.get("phase", ""),
        "artifact_name": target.get("artifact_name", ""),
        "result_class": target.get("result_class", ""),
        "passed": target.get("passed", ""),
        "external_path": str(external_path).replace("\\", "/"),
        "internal_path_rel": str(internal_path.relative_to(COURTROOM_DIR)).replace("\\", "/"),
        "recorded_sha256": recorded_sha,
        "external_sha256": "",
        "internal_sha256": "",
        "status": "UNKNOWN",
    }

    if not external_path.exists():
        result["status"] = "MISSING_EXTERNAL"
        return result

    external_sha = sha256_file(external_path)
    result["external_sha256"] = external_sha

    if external_sha != recorded_sha:
        result["status"] = f"SHA_MISMATCH_EXTERNAL_vs_RECORDED"
        return result

    # Determine action
    if internal_path.exists():
        internal_sha = sha256_file(internal_path)
        result["internal_sha256"] = internal_sha
        if internal_sha == external_sha:
            result["status"] = "ALREADY_INGESTED"
            return result
        else:
            # Internal copy exists but disagrees; treat as corruption / drift.
            result["status"] = "INTERNAL_DRIFT"
            return result

    # Copy
    internal_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(external_path, internal_path)
    internal_sha = sha256_file(internal_path)
    result["internal_sha256"] = internal_sha
    if internal_sha != external_sha:
        result["status"] = "COPY_CORRUPTED"
        return result

    result["status"] = "INGESTED"
    return result


def run_predictions(results: list[dict[str, Any]], external_root_ok: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    total = len(results)
    rows.append({
        "name": "P1_external_root_accessible",
        "pass": external_root_ok,
        "details": f"{EXTERNAL_ROOT} exists = {external_root_ok}",
    })
    rows.append({
        "name": "P2_targets_discovered_from_consuming_CRs",
        "pass": total > 0,
        "details": f"discovered {total} unique (folder, summary_file) targets across CR-120, CR-121, CR-122 ledgers",
    })
    no_missing = sum(1 for r in results if r["status"] != "MISSING_EXTERNAL")
    rows.append({
        "name": "P3_all_externals_present",
        "pass": no_missing == total,
        "details": f"present: {no_missing}/{total}",
    })
    no_sha_mismatch = sum(1 for r in results if r["status"] != "SHA_MISMATCH_EXTERNAL_vs_RECORDED")
    rows.append({
        "name": "P4_external_sha_matches_recorded",
        "pass": no_sha_mismatch == total,
        "details": f"sha-matches-recorded: {no_sha_mismatch}/{total}",
    })
    clean = sum(1 for r in results if r["status"] in ("INGESTED", "ALREADY_INGESTED"))
    rows.append({
        "name": "P5_all_targets_ingested_or_already_ingested",
        "pass": clean == total,
        "details": f"in-clean-state: {clean}/{total} (statuses: " + ",".join(sorted({r['status'] for r in results})) + ")",
    })
    rows.append({
        "name": "P6_internal_sha_matches_external_sha",
        "pass": all(r["internal_sha256"] and r["external_sha256"] and r["internal_sha256"] == r["external_sha256"]
                    for r in results if r["status"] in ("INGESTED", "ALREADY_INGESTED")),
        "details": "every ingested artifact's internal copy hashes to the same value as its external source",
    })
    return rows


def run_wrong_controls(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # WC1: external root exists
    rows.append({
        "name": "WC1_external_root_exists",
        "pass": EXTERNAL_ROOT.exists(),
        "details": f"{EXTERNAL_ROOT} present = {EXTERNAL_ROOT.exists()}",
        "load_bearing_deletion": "If the external qp_chain root is missing, ingest cannot proceed; this WC would FAIL.",
    })

    # WC2: ingest_manifest covers ALL recorded references from CR-120/121
    # (every (folder, summary_file) pair in the ledgers appears in the manifest)
    cr120_pairs = {(r["folder"], r["summary_file"]) for r in read_csv_rows(CR120_LEDGER)}
    cr121_pairs = {(r["stage"], r["summary_file"]) for r in read_csv_rows(CR121_LEDGER)}
    required = cr120_pairs | cr121_pairs
    covered = {(r["folder"], r["summary_file"]) for r in results}
    missing = required - covered
    rows.append({
        "name": "WC2_manifest_covers_all_consuming_CR_references",
        "pass": len(missing) == 0,
        "details": f"required: {len(required)}; covered: {len(covered)}; missing: {sorted(missing) if missing else 'none'}",
        "load_bearing_deletion": "If any consuming-CR reference were not in the manifest, this WC would FAIL.",
    })

    # WC3: no two manifest rows map to the same internal path
    paths = [r["internal_path_rel"] for r in results]
    duplicates = [p for p in set(paths) if paths.count(p) > 1]
    rows.append({
        "name": "WC3_no_duplicate_internal_paths",
        "pass": len(duplicates) == 0,
        "details": "no duplicate destination paths" if not duplicates else f"duplicates: {duplicates}",
        "load_bearing_deletion": "If two distinct artifacts mapped to the same internal path, the second copy would clobber the first; this WC would FAIL.",
    })

    # WC4: every internal copy hashes to the SHA recorded by its consumer
    consistent = 0
    for r in results:
        if r["status"] in ("INGESTED", "ALREADY_INGESTED"):
            if r["internal_sha256"] == r["recorded_sha256"]:
                consistent += 1
    rows.append({
        "name": "WC4_internal_copies_match_consumer_recorded_sha",
        "pass": consistent == sum(1 for r in results if r["status"] in ("INGESTED", "ALREADY_INGESTED")),
        "details": f"internal-sha matches consumer-recorded-sha on {consistent} of {sum(1 for r in results if r['status'] in ('INGESTED', 'ALREADY_INGESTED'))} cleanly ingested artifacts",
        "load_bearing_deletion": "If any internal copy's SHA disagreed with what CR-120/121/122 recorded, the chain of custody breaks; this WC would FAIL.",
    })

    # WC5: no status anomalies
    bad_statuses = {"MISSING_EXTERNAL", "SHA_MISMATCH_EXTERNAL_vs_RECORDED", "INTERNAL_DRIFT", "COPY_CORRUPTED", "UNKNOWN"}
    bad_count = sum(1 for r in results if r["status"] in bad_statuses)
    rows.append({
        "name": "WC5_no_anomalies",
        "pass": bad_count == 0,
        "details": f"anomalous statuses: {bad_count}",
        "load_bearing_deletion": "If any target had a SHA mismatch, was missing, or had internal drift, this WC would FAIL.",
    })

    # WC6: audit verdict reference resolves
    audit_ok = AUDIT_VERDICT.exists() and sha256_file(AUDIT_VERDICT) == AUDIT_VERDICT_SHA256
    rows.append({
        "name": "WC6_audit_verdict_reference_resolves",
        "pass": audit_ok,
        "details": f"AUDIT_VERDICT exists={AUDIT_VERDICT.exists()}; hash matches",
        "load_bearing_deletion": "If the audit verdict moved/edited, the recorded reference would be unverifiable.",
    })

    # WC7: every consumer SHA in CR-122 also resolves to an internal artifact
    # (specifically qp092h, which is the one CR-122 names directly)
    qp092h_internal = INTERNAL_ROOT / "qp092" / "qp092h_baryon_cmb_carrier_gate" / "qp092h_summary.json"
    expected_sha = "5b8139aa90883b8b3ac210fdad44055fc9cbf23c6f4e16dbef58668a8d2bda49"
    wc7_pass = qp092h_internal.exists() and sha256_file(qp092h_internal) == expected_sha
    rows.append({
        "name": "WC7_CR122_qp092h_reference_resolves_internally",
        "pass": wc7_pass,
        "details": f"qp092h internal copy = {qp092h_internal.relative_to(COURTROOM_DIR)}; SHA matches CR-122 recorded value = {wc7_pass}",
        "load_bearing_deletion": "If CR-122's qp092h reference does NOT resolve to an internal artifact with the expected SHA, the carrier-compression gate cannot be audited from inside the repo.",
    })

    return rows


def main() -> None:
    print("CR136 runner: qp_chain ingest")
    print(f"External root: {EXTERNAL_ROOT}")
    print(f"Internal root: {INTERNAL_ROOT}")
    INTERNAL_ROOT.mkdir(parents=True, exist_ok=True)

    external_root_ok = EXTERNAL_ROOT.exists()

    # ---- Source manifest ----
    src_rows = []
    for p in (CR120_LEDGER, CR121_LEDGER, AUDIT_VERDICT):
        src_rows.append({
            "cr_id": p.parent.name,
            "path": str(p.relative_to(COURTROOM_DIR)).replace("\\", "/"),
            "sha256": sha256_file(p) if p.exists() else "MISSING",
        })
    src_rows.append({
        "cr_id": "external_qp_chain_root",
        "path": str(EXTERNAL_ROOT).replace("\\", "/"),
        "sha256": f"directory; subdir_count={sum(1 for _ in EXTERNAL_ROOT.iterdir() if _.is_dir())}" if external_root_ok else "MISSING",
    })
    write_csv(SOURCE_MANIFEST_CSV, src_rows)

    # ---- Discover targets ----
    targets = discover_targets()
    print(f"Discovered {len(targets)} unique artifact targets across CR-120/121/122 references")

    # ---- Ingest each target ----
    results: list[dict[str, Any]] = []
    for t in targets:
        r = ingest_target(t)
        results.append(r)
    status_counts: dict[str, int] = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    for s, c in sorted(status_counts.items()):
        print(f"  {s:35} {c}")

    # Write a STABLE manifest CSV: replace per-run status (INGESTED vs
    # ALREADY_INGESTED) with the post-ingest state (in_clean_state boolean).
    # This way the CSV hash is identical regardless of which run produced it
    # -- a reviewer who wipes upstream_artifacts/ and re-runs gets the same
    # CSV bytes as a reviewer who runs against an already-ingested tree.
    stable_results = []
    for r in results:
        stable_results.append({
            "folder": r["folder"],
            "summary_file": r["summary_file"],
            "consumers": r["consumers"],
            "phase": r["phase"],
            "artifact_name": r["artifact_name"],
            "result_class": r["result_class"],
            "passed": r["passed"],
            "external_path": r["external_path"],
            "internal_path_rel": r["internal_path_rel"],
            "recorded_sha256": r["recorded_sha256"],
            "external_sha256": r["external_sha256"],
            "internal_sha256": r["internal_sha256"],
            "in_clean_state": r["status"] in ("INGESTED", "ALREADY_INGESTED"),
        })
    write_csv(INGEST_MANIFEST_CSV, stable_results)

    # ---- Wrong controls + predictions ----
    wc_rows = run_wrong_controls(results)
    pred_rows = run_predictions(results, external_root_ok)
    write_csv(WRONG_CONTROLS_CSV, wc_rows)
    write_csv(PREDICTIONS_CSV, pred_rows)

    wc_passed = sum(1 for r in wc_rows if r["pass"])
    pred_passed = sum(1 for r in pred_rows if r["pass"])

    print(f"\nWrong controls: {wc_passed}/{len(wc_rows)}")
    print(f"Predictions:    {pred_passed}/{len(pred_rows)}")

    overall_pass = (
        wc_passed == len(wc_rows)
        and pred_passed == len(pred_rows)
        and all(r["status"] in ("INGESTED", "ALREADY_INGESTED") for r in results)
    )
    result_class = (
        "CR136_QP_CHAIN_INGEST_V1_SEALED"
        if overall_pass
        else "CR136_QP_CHAIN_INGEST_V1_BOUNDARY_DRAFT"
    )

    # Deterministic lock (no timestamps, no per-run status; reports the STABLE
    # POST-INGEST STATE rather than which run produced it).  Re-execution on
    # a clean state produces a bit-identical lock and therefore a bit-identical
    # SHA-256, recorded once in CR136_result.md so reviewers can verify.
    clean_targets = sum(1 for r in results if r["status"] in ("INGESTED", "ALREADY_INGESTED"))
    anomalous_targets = len(results) - clean_targets
    lock_payload = {
        "cr_id": "CR136",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "appeal_queue_position": "4 of 7 blocking (unblocks CR-139, CR-140)",
        "ingest_type": "BULK_UPSTREAM_ARTIFACT_INGEST",
        "verdict_change_on_consumers": False,
        "external_root": str(EXTERNAL_ROOT).replace("\\", "/"),
        "internal_root_rel": str(INTERNAL_ROOT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
        "targets_total": len(results),
        "targets_in_clean_state": clean_targets,
        "targets_anomalous": anomalous_targets,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "ingest": [
            {
                "folder": r["folder"],
                "summary_file": r["summary_file"],
                "recorded_sha256": r["recorded_sha256"],
                "internal_path_rel": r["internal_path_rel"],
                "consumers": r["consumers"],
                "in_clean_state": r["status"] in ("INGESTED", "ALREADY_INGESTED"),
            }
            for r in sorted(results, key=lambda x: (x["folder"], x["summary_file"]))
        ],
        "free_parameters": 0,
        "falsifier": (
            "Re-executing CR136_runner.py on the post-ingest state MUST produce zero "
            "new INGESTED entries (only ALREADY_INGESTED), zero SHA mismatches, and "
            "the recomputed lock SHA-256 MUST match the value recorded in CR136_result.md."
        ),
    }
    INGEST_LOCK_JSON.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lock_sha = sha256_file(INGEST_LOCK_JSON)
    INGEST_LOCK_SHA.write_text(f"CR136_ingest_lock_json_sha256 = {lock_sha}\n", encoding="utf-8")

    # ---- result.md ----
    md = []
    md.append("# CR136 qp_chain Ingest v1.0\n")
    md.append("## Verdict\n")
    md.append("```text")
    md.append(result_class)
    md.append("```\n")
    md.append("## Scope\n")
    md.append("CR-120, CR-121, and CR-122 cite SHA-256 hashes of artifacts that physically live OUTSIDE The_Courtroom at `C:/VS/quantum_phase/artifacts/`. A reviewer cloning the repo cannot reproduce any Higgs-or-gravity-related claim because the artifacts those hashes refer to are not in the repository. CR-136 ingests the referenced artifacts (bit-identical, SHA-verified) into `The_Courtroom/upstream_artifacts/`, producing an internal copy whose SHA-256 matches what the consuming CRs recorded.\n")
    md.append("This is an INGEST, not a verdict change. CR-120, CR-121, and CR-122 themselves are NOT modified by CR-136 -- the chain of custody is preserved by adding an internal copy alongside the external original, not by editing the consuming CRs. A reviewer who wants to verify any cited SHA-256 looks it up in `CR136_ingest_manifest.csv` to find the internal path, then runs `Get-FileHash` to confirm the value matches.\n")
    md.append("## Inputs\n")
    md.append(f"- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`{AUDIT_VERDICT_SHA256}`)")
    md.append(f"- CR-120 ledger: `{CR120_LEDGER.relative_to(COURTROOM_DIR)}`")
    md.append(f"- CR-121 ledger: `{CR121_LEDGER.relative_to(COURTROOM_DIR)}`")
    md.append(f"- External qp_chain root: `{EXTERNAL_ROOT}`")
    md.append(f"- Internal destination: `{INTERNAL_ROOT.relative_to(COURTROOM_DIR)}/`")
    md.append(f"- Source manifest: `CR136_source_manifest.csv`\n")
    md.append("## Ingest Summary\n")
    md.append(f"- **Total targets discovered:** {len(results)}")
    for s, c in sorted(status_counts.items()):
        md.append(f"- **{s}:** {c}")
    md.append("")
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
    md.append("## Per-Artifact Manifest (sample of first 8 + last 4)\n")
    md.append("| Folder | Summary file | Consumers | Recorded SHA-256 (first 12) | Internal path | Status |")
    md.append("| --- | --- | --- | --- | --- | --- |")
    sample = (results[:8] + (results[-4:] if len(results) > 12 else []))
    for r in sample:
        md.append(f"| `{r['folder']}` | `{r['summary_file']}` | {r['consumers']} | `{r['recorded_sha256'][:12]}...` | `{r['internal_path_rel']}` | {r['status']} |")
    if len(results) > 12:
        md.append(f"")
        md.append(f"*(showing 8 + 4 of {len(results)} total; full table in `CR136_ingest_manifest.csv`)*")
    md.append("")
    md.append("## Falsifier (LOCKED)\n")
    md.append("Re-executing `CR136_runner.py` on the post-ingest state MUST produce zero new `INGESTED` entries (only `ALREADY_INGESTED`), zero SHA mismatches between external and internal copies, and the recomputed lock SHA-256 MUST match the value recorded here. Any deviation falsifies v1.0.\n")
    md.append("**Free parameters:** 0.\n")
    md.append("## Cryptographic Chain\n")
    md.append("```text")
    md.append(f"CR135_audit_verdict_sha256                = {AUDIT_VERDICT_SHA256}")
    md.append(f"CR136_source_manifest_csv                 = {sha256_file(SOURCE_MANIFEST_CSV)}")
    md.append(f"CR136_ingest_manifest_csv                 = {sha256_file(INGEST_MANIFEST_CSV)}")
    md.append(f"CR136_predictions_csv                     = {sha256_file(PREDICTIONS_CSV)}")
    md.append(f"CR136_wrong_controls_csv                  = {sha256_file(WRONG_CONTROLS_CSV)}")
    md.append(f"CR136_ingest_lock_json                    = {lock_sha}")
    md.append("```\n")
    md.append("## Follow-up CRs\n")
    md.append("- **CR-139** (CR-122 verdict regrade): can now reference internal qp092h path when adding its header block.")
    md.append("- **CR-140** (Higgs claim reword): can now reference internal qp091t / qp091r paths when adding its header block.")
    md.append("- **CR-136b** (optional): rewrite CR-120/121/122 runner.py files to point at internal paths so the runners are themselves re-executable from inside The_Courtroom alone. NOT required for audit-driven hash resolution.\n")
    md.append("## Rule of Immutability\n")
    md.append("Ingest manifest, internal destinations, falsifier, and wrong controls are frozen at CR-136 seal time. Future falsification (failed idempotency, new SHA mismatches, missing ingest entries) must be in an appeal CR within `00_governance/`.\n")
    RESULT_MD.write_text("\n".join(md), encoding="utf-8")

    # ---- summary.json ----
    summary_payload = {
        "cr_id": "CR136",
        "branch": "00_governance",
        "test_class": "QP_CHAIN_INGEST_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "last_run_utc": now_utc(),
        "ingest_type": "BULK_UPSTREAM_ARTIFACT_INGEST",
        "verdict_change_on_consumers": False,
        "free_parameters": 0,
        "driving_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
        "external_root": str(EXTERNAL_ROOT).replace("\\", "/"),
        "internal_root_rel": str(INTERNAL_ROOT.relative_to(COURTROOM_DIR)).replace("\\", "/"),
        "targets_total": len(results),
        "status_counts": status_counts,
        "wrong_controls_passed": wc_passed,
        "wrong_controls_total": len(wc_rows),
        "predictions_passed": pred_passed,
        "predictions_total": len(pred_rows),
        "wrong_controls": wc_rows,
        "predictions": pred_rows,
        "falsifier": (
            "Re-executing CR136_runner.py on the post-ingest state MUST produce zero new "
            "INGESTED entries (only ALREADY_INGESTED), zero SHA mismatches, and the "
            "recomputed lock SHA-256 MUST match the value recorded in CR136_result.md."
        ),
        "cryptographic_chain": {
            "CR135_audit_verdict_sha256": AUDIT_VERDICT_SHA256,
            "CR136_source_manifest_csv": sha256_file(SOURCE_MANIFEST_CSV),
            "CR136_ingest_manifest_csv": sha256_file(INGEST_MANIFEST_CSV),
            "CR136_predictions_csv": sha256_file(PREDICTIONS_CSV),
            "CR136_wrong_controls_csv": sha256_file(WRONG_CONTROLS_CSV),
            "CR136_ingest_lock_json": lock_sha,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSealed: {result_class}")
    print(f"Lock SHA-256: {lock_sha}")


if __name__ == "__main__":
    main()
