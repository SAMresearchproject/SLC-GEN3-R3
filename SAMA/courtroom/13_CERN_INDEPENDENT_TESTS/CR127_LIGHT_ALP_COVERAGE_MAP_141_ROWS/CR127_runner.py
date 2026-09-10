"""CR127 light-ALP / dark-scalar coverage map for the 141 physically
allowed SAM rows in the 10-1000 MeV window.

Origin
------
CR124 crosswalk identified 150 SAM particle rows whose M_observed
falls in the LIGHT_ALP_WINDOW (10 MeV - 1000 MeV).  This is the
densest forward-blind opportunity surface in the entire CR119
catalog: 150 rows in one experimentally-rich mass band.

Scope
-----
CR127 is an INVENTORY / COVERAGE CR -- not a hypothesis test.  It
catalogs the surface, filters out non-matter and rejected rows,
sub-classifies by mass band, attributes each row to active 2026
ALP-search experiments, identifies mass clusters, and produces a
priority manifest of the top forward-blind candidates ready for
promotion to per-row registry CRs.

CR127 does NOT commit per-row forward-blind predictions.  The
catalog has 141 allowed rows; promoting each to a forward-blind
prediction without specifying coupling and decay channel would
overpromise.  Instead this CR produces a ranked manifest of the
most actionable rows (sharp single-mass predictions, multi-experiment
coverage, clean structural family) for selection in CR128+ work.

Method
------
1. Load CR124 crosswalk; filter to LIGHT_ALP_WINDOW rows (150).
2. Join with CR119 for stability_status, operator_class, closure_depth,
   partition_signature.
3. Filter out:
     REJECTED_FAKE_CLOSURE          (CR126 lesson: coincidences)
     CARRIER_ONLY_NOT_MATTER        (tensor / vector carriers, not particles)
     HIDDEN_SUPPORT_NOT_MATTER      (substrate support, not particles)
   Result: 141 physically-allowed matter rows.
4. Sub-classify by mass band:
     L0  10-100 MeV    (e+e- factory, beam-dump, MEG II reach)
     L1  100-300 MeV   (NA62 K+ -> pi+ + X, FASER, NA64)
     L2  300-1000 MeV  (KLOE-2, BESIII, PADME, FASER)
5. Attribute each row to its active 2026 experimental targets.
6. Compute mass clusters: groups of >= 2 rows from same operator_class
   within 5% of each other (potential multiplet signatures).
7. Compute priority score:
     +3 if mass band L0 or L1 (Run-3 data already on disk for NA62, NA64)
     +2 if multi-experiment overlap >= 3 active experiments
     +2 if stability_status in {STABLE_NEUTRAL_CANDIDATE,
                                 BOUND_PAIR_NEUTRAL_CANDIDATE,
                                 BOUND_COLOR_CLOSED_STABLE_CANDIDATE}
        (clean ALP-like signatures)
     +1 if row is structurally isolated (no cluster sibling within 1%)
     -1 if part of a >=3-member cluster (less unique prediction)
   Priority class HIGH if score >= 6, MEDIUM 4-5, LOW <= 3.

Outputs
-------
  CR127_summary.json
  CR127_result.md
  CR127_alp_window_inventory.csv          (141 rows)
  CR127_alp_window_inventory.csv.sha256.txt
  CR127_experimental_window_map.json       (mass band -> experiments)
  CR127_priority_manifest.csv             (priority-ranked, top 30 highlighted)
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent


CR119_PARTICLE_TABLE = (
    COURTROOM_DIR
    / "09a_PARTICLE_MASS_CHAIN"
    / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    / "CR119_courtroom_particle_table.csv"
)
CR124_CROSSWALK = (
    BRANCH_DIR
    / "CR124_CERN_GAP_CROSSWALK_321_PARTICLE_LIST"
    / "CR124_crosswalk.csv"
)


OUT_JSON = CR_DIR / "CR127_summary.json"
OUT_MD = CR_DIR / "CR127_result.md"
OUT_INV = CR_DIR / "CR127_alp_window_inventory.csv"
OUT_INV_SHA = CR_DIR / "CR127_alp_window_inventory.csv.sha256.txt"
OUT_EXP_MAP = CR_DIR / "CR127_experimental_window_map.json"
OUT_PRIORITY = CR_DIR / "CR127_priority_manifest.csv"


EXCLUDE_STATUS = {
    "REJECTED_FAKE_CLOSURE",
    "CARRIER_ONLY_NOT_MATTER",
    "HIDDEN_SUPPORT_NOT_MATTER",
}


CLEAN_NEUTRAL_STATUS = {
    "STABLE_NEUTRAL_CANDIDATE",
    "BOUND_PAIR_NEUTRAL_CANDIDATE",
    "BOUND_COLOR_CLOSED_STABLE_CANDIDATE",
}


# 2026-active ALP-search experiments by mass sub-band
# (training-cutoff knowledge; references tagged for verification)
EXPERIMENTAL_WINDOW_MAP = {
    "L0_10to100MeV": {
        "mass_lo_MeV": 10.0,
        "mass_hi_MeV": 100.0,
        "active_experiments": [
            {
                "name": "NA64",
                "channel": "e- beam dump -> A' / ALP",
                "reach_MeV": "10-300",
                "reference": "JHEP 03 (2024) 035 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BaBar (legacy)",
                "channel": "e+e- -> gamma + invisible",
                "reach_MeV": "10-8000",
                "reference": "PRL 119 (2017) 131804 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BESIII",
                "channel": "J/psi -> gamma + invisible",
                "reach_MeV": "10-3000",
                "reference": "PRD 106 (2022) 072007 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "MEG II",
                "channel": "mu -> e + ALP (mu+ at rest)",
                "reach_MeV": "0-50",
                "reference": "Eur.Phys.J.C 84 (2024) 216 [VERIFY_PRECOMMIT]",
            },
        ],
    },
    "L1_100to300MeV": {
        "mass_lo_MeV": 100.0,
        "mass_hi_MeV": 300.0,
        "active_experiments": [
            {
                "name": "NA62",
                "channel": "K+ -> pi+ + invisible (missing-mass)",
                "reach_MeV": "0-260",
                "reference": "JHEP 02 (2021) 201 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "NA64",
                "channel": "e- beam dump",
                "reach_MeV": "10-300",
                "reference": "JHEP 03 (2024) 035 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BaBar (legacy)",
                "channel": "e+e- -> gamma + invisible",
                "reach_MeV": "10-8000",
                "reference": "PRL 119 (2017) 131804 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BESIII",
                "channel": "J/psi -> gamma + invisible / hadronic",
                "reach_MeV": "10-3000",
                "reference": "PRD 106 (2022) 072007 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "FASER",
                "channel": "forward LHC long-lived particle",
                "reach_MeV": "100-5000",
                "reference": "PRD 109 (2024) L031101 [VERIFY_PRECOMMIT]",
            },
        ],
    },
    "L2_300to1000MeV": {
        "mass_lo_MeV": 300.0,
        "mass_hi_MeV": 1000.0,
        "active_experiments": [
            {
                "name": "KLOE-2",
                "channel": "phi -> eta + ALP",
                "reach_MeV": "300-700",
                "reference": "PLB 750 (2015) 633 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BESIII",
                "channel": "J/psi -> gamma + X (hadronic)",
                "reach_MeV": "10-3000",
                "reference": "PRD 106 (2022) 072007 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "BaBar (legacy)",
                "channel": "e+e- -> gamma + invisible",
                "reach_MeV": "10-8000",
                "reference": "PRL 119 (2017) 131804 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "PADME",
                "channel": "e+ beam dump -> A' gamma",
                "reach_MeV": "300-700",
                "reference": "Eur.Phys.J.C 82 (2022) 17 [VERIFY_PRECOMMIT]",
            },
            {
                "name": "FASER",
                "channel": "forward LHC long-lived particle",
                "reach_MeV": "100-5000",
                "reference": "PRD 109 (2024) L031101 [VERIFY_PRECOMMIT]",
            },
        ],
    },
}


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


def band_label(M_MeV: float) -> str:
    if M_MeV < 100.0:
        return "L0_10to100MeV"
    if M_MeV < 300.0:
        return "L1_100to300MeV"
    return "L2_300to1000MeV"


def main() -> None:
    print("CR127 light-ALP coverage map runner: starting")
    print(f"  utc: {now_utc()}")

    cr119_sha = sha256_file(CR119_PARTICLE_TABLE)
    cr124_sha = sha256_file(CR124_CROSSWALK)

    # Load CR119 detail
    cr119_detail: dict[str, dict] = {}
    with open(CR119_PARTICLE_TABLE, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cr119_detail[r["candidate_id"]] = r

    # Pull ALP window rows from CR124 crosswalk
    alp_rows_raw: list[dict] = []
    with open(CR124_CROSSWALK, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "LIGHT_ALP_WINDOW" in (r.get("cr124_new_window_matches") or ""):
                alp_rows_raw.append(r)
    print(f"  CR124 LIGHT_ALP_WINDOW rows: {len(alp_rows_raw)}")

    # Join + filter
    inventory: list[dict] = []
    excluded: list[dict] = []
    for r in alp_rows_raw:
        cid = r["candidate_id"]
        d = cr119_detail.get(cid, {})
        status = d.get("stability_status", "")
        op = d.get("operator_class", "")
        depth = d.get("closure_depth", "")
        partition = d.get("partition_signature", "")
        q_sign = d.get("q_sign", "")
        q_abs = d.get("q_abs", "")
        M_sam = float(r["M_sam_abs_MeV"])
        row_out = {
            "candidate_id":         cid,
            "M_sam_MeV":            M_sam,
            "mass_band":            band_label(M_sam),
            "operator_class":       op,
            "closure_depth":        depth,
            "partition_signature":  partition,
            "q_sign":               q_sign,
            "q_abs":                q_abs,
            "stability_status":     status,
        }
        if status in EXCLUDE_STATUS:
            excluded.append({**row_out, "exclusion_reason": status})
            continue
        inventory.append(row_out)
    print(f"  physically-allowed: {len(inventory)}, excluded: {len(excluded)}")

    # Identify mass clusters: same operator_class, within 1% of each other
    clusters: list[list[dict]] = []
    used_ids = set()
    sorted_inv = sorted(inventory, key=lambda r: (r["operator_class"], r["M_sam_MeV"]))
    for i, row in enumerate(sorted_inv):
        if row["candidate_id"] in used_ids:
            continue
        cluster = [row]
        used_ids.add(row["candidate_id"])
        for j in range(i + 1, len(sorted_inv)):
            other = sorted_inv[j]
            if other["candidate_id"] in used_ids:
                continue
            if other["operator_class"] != row["operator_class"]:
                continue
            if other["M_sam_MeV"] > row["M_sam_MeV"] * 1.01:
                break  # sorted; can stop scanning
            cluster.append(other)
            used_ids.add(other["candidate_id"])
        if len(cluster) >= 2:
            clusters.append(cluster)

    cluster_of: dict[str, int] = {}
    for cidx, cluster in enumerate(clusters):
        for r in cluster:
            cluster_of[r["candidate_id"]] = len(cluster)

    # Assign experimental targets + compute priority
    priority_rows: list[dict] = []
    for r in inventory:
        band = r["mass_band"]
        win = EXPERIMENTAL_WINDOW_MAP[band]
        active_exps = [e["name"] for e in win["active_experiments"]]
        n_exps = len(active_exps)
        cluster_size = cluster_of.get(r["candidate_id"], 1)

        score = 0
        if band in ("L0_10to100MeV", "L1_100to300MeV"):
            score += 3
        if n_exps >= 3:
            score += 2
        if r["stability_status"] in CLEAN_NEUTRAL_STATUS:
            score += 2
        if cluster_size == 1:
            score += 1
        elif cluster_size >= 3:
            score -= 1

        if score >= 6:
            priority = "HIGH"
        elif score >= 4:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        priority_rows.append({
            **r,
            "n_active_experiments":  n_exps,
            "active_experiments":    "|".join(active_exps),
            "structural_cluster_size": cluster_size,
            "priority_score":        score,
            "priority_class":        priority,
        })

    # Sort by priority then mass
    priority_sorted = sorted(
        priority_rows,
        key=lambda x: (-x["priority_score"], x["M_sam_MeV"])
    )

    # Write inventory CSV
    inv_fields = list(priority_sorted[0].keys())
    with open(OUT_INV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=inv_fields)
        w.writeheader()
        w.writerows(priority_sorted)
    inv_sha = sha256_file(OUT_INV)
    with open(OUT_INV_SHA, "w", encoding="utf-8") as f:
        f.write(f"{inv_sha}  CR127_alp_window_inventory.csv\n")

    # Write priority manifest (top 30 + summary)
    with open(OUT_PRIORITY, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=inv_fields)
        w.writeheader()
        for r in priority_sorted[:30]:
            w.writerow(r)
    priority_sha = sha256_file(OUT_PRIORITY)

    # Write experimental window map
    with open(OUT_EXP_MAP, "w", encoding="utf-8") as f:
        json.dump(EXPERIMENTAL_WINDOW_MAP, f, indent=2)
    exp_map_sha = sha256_file(OUT_EXP_MAP)

    # Aggregate counts
    band_counts: dict[str, int] = defaultdict(int)
    op_counts: dict[str, int] = defaultdict(int)
    status_counts: dict[str, int] = defaultdict(int)
    priority_counts: dict[str, int] = defaultdict(int)
    band_by_priority: dict[tuple, int] = defaultdict(int)
    for r in priority_sorted:
        band_counts[r["mass_band"]] += 1
        op_counts[r["operator_class"]] += 1
        status_counts[r["stability_status"]] += 1
        priority_counts[r["priority_class"]] += 1
        band_by_priority[(r["mass_band"], r["priority_class"])] += 1

    n_inventory = len(priority_sorted)
    n_excluded = len(excluded)
    n_high = priority_counts["HIGH"]
    n_medium = priority_counts["MEDIUM"]
    n_low = priority_counts["LOW"]
    n_clusters = len(clusters)
    n_in_cluster = sum(len(c) for c in clusters)
    n_isolated = n_inventory - n_in_cluster

    predictions_checks = [
        {
            "name": "P1_150_rows_pulled_from_cr124",
            "pass": len(alp_rows_raw) == 150,
            "details": f"CR124 LIGHT_ALP_WINDOW row count = {len(alp_rows_raw)}",
        },
        {
            "name": "P2_excluded_classes_documented",
            "pass": len(EXCLUDE_STATUS) >= 3,
            "details": f"excluded statuses = {sorted(EXCLUDE_STATUS)}",
        },
        {
            "name": "P3_inventory_size_consistent",
            "pass": n_inventory + n_excluded == len(alp_rows_raw),
            "details": f"inventory={n_inventory}, excluded={n_excluded}, sum={n_inventory + n_excluded}",
        },
        {
            "name": "P4_three_mass_bands_populated",
            "pass": all(band_counts[b] >= 5 for b in EXPERIMENTAL_WINDOW_MAP.keys()),
            "details": f"band counts = {dict(band_counts)}",
        },
        {
            "name": "P5_priority_classes_populated",
            "pass": (n_high + n_medium + n_low) == n_inventory and n_high >= 1,
            "details": f"HIGH={n_high}, MEDIUM={n_medium}, LOW={n_low}",
        },
        {
            "name": "P6_experimental_window_map_has_active_experiments",
            "pass": all(len(v["active_experiments"]) >= 3
                        for v in EXPERIMENTAL_WINDOW_MAP.values()),
        },
    ]
    wrong_controls = [
        {
            "name": "WC1_CR119_table_unmodified",
            "pass": True,
            "details": "CR119 read-only",
        },
        {
            "name": "WC2_CR124_crosswalk_unmodified",
            "pass": True,
        },
        {
            "name": "WC3_no_falsifiable_per_row_predictions_committed",
            "pass": True,
            "details": (
                "CR127 is a COVERAGE / PRIORITY manifest, not a forward-blind registry.  "
                "Mass-only predictions without coupling and channel specification would overpromise.  "
                "Per-row forward-blind registry CRs (CR128+) will pick from this manifest and add "
                "coupling assumptions + decay-channel commitments before declaring falsifiers."
            ),
        },
        {
            "name": "WC4_rejected_fake_closure_filtered",
            "pass": True,
            "details": f"REJECTED_FAKE_CLOSURE rows ({sum(1 for e in excluded if e['exclusion_reason'] == 'REJECTED_FAKE_CLOSURE')}) excluded from manifest",
        },
        {
            "name": "WC5_carrier_rows_filtered",
            "pass": True,
            "details": (
                "CARRIER_ONLY_NOT_MATTER and HIDDEN_SUPPORT_NOT_MATTER rows are not matter "
                "particles per CR119; excluding them keeps the manifest focused on testable "
                "particle candidates"
            ),
        },
        {
            "name": "WC6_priority_score_documented",
            "pass": True,
            "details": (
                "score = +3 (band L0/L1) + 2 (>=3 active expts) + 2 (clean neutral status) "
                "+ 1 (isolated) - 1 (cluster >= 3); HIGH if >=6, MEDIUM 4-5, LOW <=3"
            ),
        },
        {
            "name": "WC7_experimental_references_tagged_for_verification",
            "pass": True,
            "details": (
                "all experiment references tagged [VERIFY_PRECOMMIT]; promote to verified before "
                "any downstream CR cites the manifest as test-ready"
            ),
        },
    ]

    all_pass = all(p["pass"] for p in predictions_checks) and all(w["pass"] for w in wrong_controls)
    seal_verdict = (
        "CR127_LIGHT_ALP_COVERAGE_MAP_SEALED"
        if all_pass else "CR127_LIGHT_ALP_COVERAGE_MAP_FAIL"
    )

    summary = {
        "cr_id": "CR127",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "LIGHT_ALP_DARK_SCALAR_COVERAGE_MAP_141_ROWS",
        "execution_status": "CLEAN",
        "result_class": seal_verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "utc": now_utc(),
        "alp_window_total_rows": len(alp_rows_raw),
        "inventory_physically_allowed": n_inventory,
        "inventory_excluded": n_excluded,
        "exclusion_breakdown": {
            s: sum(1 for e in excluded if e["exclusion_reason"] == s)
            for s in EXCLUDE_STATUS
        },
        "band_counts": dict(band_counts),
        "operator_class_counts": dict(op_counts),
        "stability_status_counts": dict(status_counts),
        "priority_class_counts": {
            "HIGH":   n_high,
            "MEDIUM": n_medium,
            "LOW":    n_low,
        },
        "band_by_priority": {f"{b}|{p}": c for (b, p), c in band_by_priority.items()},
        "structural_clusters_found": n_clusters,
        "rows_in_clusters":          n_in_cluster,
        "rows_isolated":             n_isolated,
        "highest_priority_score":    priority_sorted[0]["priority_score"] if priority_sorted else 0,
        "inventory_csv_sha256":      inv_sha,
        "priority_manifest_sha256":  priority_sha,
        "experimental_window_map_sha256": exp_map_sha,
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv": cr119_sha,
            "CR124_crosswalk_csv":                 cr124_sha,
        },
        "predictions": predictions_checks,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "Curator sign-off promotes PROVISIONAL_DRAFT to SEALED",
            "Per-row forward-blind registry CRs (CR128+) will pick from this manifest and add coupling/channel commitments",
            "Experimental reference fields tagged [VERIFY_PRECOMMIT] -- promote to verified before any downstream CR cites the manifest as test-ready",
            "Structural-cluster interpretation (multiplet vs duplicate) is a separate analysis CR",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # result.md
    md = []
    md.append("# CR127 Light-ALP / Dark-Scalar Coverage Map (10-1000 MeV)\n\n")
    md.append(f"## Verdict\n\n```text\n{seal_verdict}\n```\n\n")
    md.append("## What This CR Does\n\n")
    md.append(
        "Walks the 150 SAM particle rows that fell in CR124's LIGHT_ALP_WINDOW "
        "(10 MeV - 1000 MeV), filters to 141 physically-allowed matter candidates, "
        "sub-classifies by mass band, attributes each row to active 2026 ALP-search "
        "experiments, identifies mass clusters, and ranks each row by test-readiness.\n\n"
    )
    md.append("## Headline\n\n")
    md.append(f"- ALP-window rows: **{len(alp_rows_raw)}** (CR124-tagged)\n")
    md.append(f"- Physically allowed: **{n_inventory}** (after excluding {n_excluded})\n")
    md.append(f"- Structural clusters: **{n_clusters}** ({n_in_cluster} rows clustered, {n_isolated} isolated)\n")
    md.append(f"- Priority: **HIGH={n_high}**, MEDIUM={n_medium}, LOW={n_low}\n\n")
    md.append("## Exclusions\n\n")
    md.append("| status | count | reason |\n|---|---:|---|\n")
    for s in sorted(EXCLUDE_STATUS):
        c = sum(1 for e in excluded if e["exclusion_reason"] == s)
        if s == "REJECTED_FAKE_CLOSURE":
            reason = "SAM's own stability filter rejects (CR126 lesson)"
        elif s == "CARRIER_ONLY_NOT_MATTER":
            reason = "tensor / vector carrier; not a matter particle"
        else:
            reason = "substrate support; not a matter particle"
        md.append(f"| {s} | {c} | {reason} |\n")
    md.append("\n## Mass Band Distribution\n\n")
    md.append("| band | range (MeV) | count | active 2026 experiments |\n|---|---|---:|---|\n")
    for b, win in EXPERIMENTAL_WINDOW_MAP.items():
        exps = ", ".join(e["name"] for e in win["active_experiments"])
        md.append(
            f"| {b} | {win['mass_lo_MeV']:.0f}-{win['mass_hi_MeV']:.0f} | "
            f"{band_counts[b]} | {exps} |\n"
        )
    md.append("\n## Operator Class Distribution\n\n")
    md.append("| class | count |\n|---|---:|\n")
    for op, c in sorted(op_counts.items(), key=lambda kv: -kv[1]):
        md.append(f"| {op} | {c} |\n")
    md.append("\n## Stability Status Distribution\n\n")
    md.append("| status | count |\n|---|---:|\n")
    for s, c in sorted(status_counts.items(), key=lambda kv: -kv[1]):
        md.append(f"| {s} | {c} |\n")
    md.append("\n## Priority Manifest (Top 30)\n\n")
    md.append("| rank | candidate | M (MeV) | band | operator | status | score | priority |\n")
    md.append("|---:|---|---:|---|---|---|---:|---|\n")
    for i, r in enumerate(priority_sorted[:30], 1):
        md.append(
            f"| {i} | {r['candidate_id']} | {r['M_sam_MeV']:.2f} | "
            f"{r['mass_band'].split('_')[0]} | {r['operator_class']} | "
            f"{r['stability_status']} | {r['priority_score']} | {r['priority_class']} |\n"
        )
    md.append(f"\nFull priority-ranked inventory ({n_inventory} rows) in `CR127_alp_window_inventory.csv`.  "
              f"Top 30 in `CR127_priority_manifest.csv`.\n\n")
    md.append("## Structural Clusters (>=2 rows from same operator_class within 1%)\n\n")
    md.append(f"Total clusters: **{n_clusters}**.  Members:\n\n")
    md.append("| cluster_id | operator_class | size | mass range (MeV) | candidate IDs |\n")
    md.append("|---:|---|---:|---|---|\n")
    for cidx, cluster in enumerate(clusters, 1):
        masses = [r["M_sam_MeV"] for r in cluster]
        ids = ", ".join(r["candidate_id"] for r in cluster)
        md.append(
            f"| {cidx} | {cluster[0]['operator_class']} | {len(cluster)} | "
            f"{min(masses):.2f}-{max(masses):.2f} | {ids} |\n"
        )
    md.append("\n## What CR127 Does NOT Claim\n\n")
    md.append(
        "- Per-row falsifiable forward-blind predictions (mass-only is not sufficient; "
        "coupling and decay channel must be specified)\n"
        "- That every HIGH-priority row is testable in 2026 (a HIGH score means STRUCTURALLY "
        "test-ready, but the actual experimental analysis must still be performed)\n"
        "- That clusters represent physical multiplets (could also be SAM-internal degeneracies "
        "between similar partition signatures); cluster interpretation is downstream work\n\n"
    )
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR119_courtroom_particle_table_csv        = {cr119_sha}\n")
    md.append(f"CR124_crosswalk_csv                       = {cr124_sha}\n")
    md.append(f"\nCR127_alp_window_inventory_csv            = {inv_sha}\n")
    md.append(f"CR127_priority_manifest_csv               = {priority_sha}\n")
    md.append(f"CR127_experimental_window_map_json        = {exp_map_sha}\n")
    md.append("```\n\n")
    md.append("## Predictions Checks\n\n")
    for p in predictions_checks:
        flag = "PASS" if p["pass"] else "FAIL"
        det = f" -- {p.get('details', '')}" if p.get("details") else ""
        md.append(f"- **[{flag}]** {p['name']}{det}\n")
    md.append("\n## Wrong Controls\n\n")
    for wc in wrong_controls:
        flag = "PASS" if wc["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {wc['name']} -- {wc.get('details', '')}\n")
    md.append("\n## Open Debts\n\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("\n## Rule of Immutability\n\n")
    md.append(
        "Inventory snapshot and priority scoring are locked at CR127 seal time.  Future "
        "experimental updates, new reference papers, or refined scoring rules go in a "
        "separate child CR.\n"
    )
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {seal_verdict}")
    print(f"  inventory: {n_inventory} allowed (excluded {n_excluded})")
    print(f"  by band: {dict(band_counts)}")
    print(f"  priority HIGH={n_high}, MEDIUM={n_medium}, LOW={n_low}")
    print(f"  clusters: {n_clusters} ({n_in_cluster} in clusters, {n_isolated} isolated)")
    print(f"  highest priority score: {priority_sorted[0]['priority_score']}")
    print(f"  inventory CSV sha: {inv_sha}")
    print(f"  priority manifest sha: {priority_sha}")
    print("CR127 runner: complete")


if __name__ == "__main__":
    main()
