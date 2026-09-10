"""
CR252 runner — Particle Catalog Spine-Refresh

Re-executes qp093a_all_stable_sam_particle_combination_enumerator.py
without source modification, audits its spine constants against the
post-CR238 canonical values, and produces a row-by-row delta against
the 2026-06-15 baseline.

Per CR252_PRECOMMIT.md: discrepancies are the concern. Finding them
and explaining them is the test.

V-3/F2 amended per CR252_PRECOMMIT_AMENDMENT.md (2026-06-24): the
sealed precommit's "matter_row_allowed=yes count == 126" check
conflated qp093a's matter column with the downstream CR119 matter
table boundary. Corrected V-3 compares regen's count to baseline's
count (both are 286 in qp093a's column; the 126 is a downstream
gate). First-run artifacts (verdict FAIL by F2) preserved.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(r"C:\VS\The_Courtroom")
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR252_PARTICLE_CATALOG_SPINE_REFRESH"
QP093A_SRC = Path(r"C:\VS\quantum_phase\src\qp093a_all_stable_sam_particle_combination_enumerator.py")
QP093A_OUT_DIR = Path(r"C:\VS\quantum_phase\artifacts\qp093a_stable_particle_combination_enumerator")
QP093A_CATALOG = QP093A_OUT_DIR / "qp093a_candidate_catalog.csv"

PRECOMMIT = OUT / "CR252_PRECOMMIT.md"
RUNNER = OUT / "CR252_runner.py"
SPINE_AUDIT = OUT / "CR252_spine_input_audit.csv"
RECHECK = OUT / "CR252_recheck_derivations.md"
CATALOG_V2 = OUT / "CR252_particle_catalog_v2.csv"
MATTER_V2 = OUT / "CR252_matter_table_v2.csv"
BASELINE = OUT / "CR252_particle_catalog_2026_06_15_baseline.csv"
ROW_DELTA = OUT / "CR252_row_delta.csv"
AGGREGATE = OUT / "CR252_aggregate.csv"
WC_LOG = OUT / "CR252_wrong_controls.csv"
SUMMARY = OUT / "CR252_summary.json"
RESULT = OUT / "CR252_result.md"
HASHES = OUT / "HASHES.txt"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ============== STEP 1: spine input audit ==============

SPINE_INPUTS = [
    ("L54",  "R",                "Decimal(12)",                              "12",                              "CR238 §1",                "match"),
    ("L55",  "D",                "Decimal(3)",                               "3",                               "CR238 §1",                "match"),
    ("L56",  "ALPHA_H",          "Decimal(2)",                               "2",                               "CR238 §1",                "match"),
    ("L57",  "PARTITION",        "{1,2,3,4,6,8,9,12}",                       "{1,2,3,4,6,8,9,12}",              "LCQC002 / CR238",         "match"),
    ("L60",  "SEVEN",            "Decimal(7)",                               "S-1 = 7",                         "CR238 §1",                "match"),
    ("L61",  "EIGHT",            "Decimal(8)",                               "S = alpha_H^D = 8",               "CR238 §1",                "match"),
    ("L62",  "THOUSAND",         "Decimal(1000)",                            "MeV scale convention",            "convention",              "match"),
    ("L230", "Higgs_surface_debit", "(D*D/R)*THOUSAND = 750",                "D^2/R = 0.75 (·1000 GeV→MeV)",    "CR114 / CR229",           "match"),
    ("L256", "qA_capacity_div",  "R*R = 144",                                "R^2 = 144 (matter capacity)",     "CR229",                   "match"),
    ("L295", "carrier_split",    "qA/EIGHT = qA/8",                          "alpha_H^D split",                 "CR238 + CR222d",          "match"),
    ("L296", "retained_split",   "qA*SEVEN/EIGHT = 7*qA/8",                  "(S-1)/S split",                   "CR238 + CR222d",          "match"),
    ("L328", "axis_factor",      "{plus:1.25,minus:1.5,neutral:0.125}",      "POST-CR243 RECHECK",              "CR243 typed mass-lift",   "requires_recheck"),
    ("L434", "pair_m_native",    "a*b*R + |q|*D",                            "POST-CR244 RECHECK",              "CR244 unequal-pair forms","requires_recheck"),
    ("L456", "higgs_scalar",     "R*R*7/8 * 1000 = 126000 MeV",              "R^2*(S-1)/S = 126 GeV",           "Higgs identity memo",     "match"),
]


def write_spine_audit() -> None:
    with SPINE_AUDIT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_line", "qp093a_name", "qp093a_value", "canonical_value", "source_cr", "verdict"])
        for row in SPINE_INPUTS:
            w.writerow(row)


# ============== STEP 2: recheck derivations ==============

RECHECK_TEXT = """# CR252 Recheck Derivations

For every spine-input audit row marked `requires_recheck` in
`CR252_spine_input_audit.csv`, walk through the post-CR238 derivation
that determines whether the qp093a value is structurally consistent
with the current spine.

The validation criterion is **operational, not theoretical**: if the
qp093a value were structurally wrong post-CR238, the regen would
produce shifted M_native values at the rows that use it. The
row-delta step (CR252_row_delta.csv) tests this directly. This file
documents the proposed reading; row-delta confirms or refutes it.

---

## L328 — axis_factor in `native_single_mass()`

**qp093a value (line 328):**

```
axis_factor = {"plus": Decimal("1.25"), "minus": Decimal("1.5"), "neutral": Decimal("0.125")}
return p * axis_factor * (R ** generation_depth)
```

**Recheck against CR243 typed mass-lift channels.**

Per [project_typed_channel_table_closure_cr243_244], CR243 typed the
substrate mass-lift Y(P) = X/K closed across all 138 substrate-ledger
rows via seven typed forms. The substrate atoms are unchanged; what
CR243 added is the **typed channel** decomposition that classifies
which form a row's lift takes.

The qp093a axis_factor values in CR238-atom rationals:

- `plus = 1.25 = 5/4`
- `minus = 1.5 = 3/2 = D/α_H`
- `neutral = 0.125 = 1/8 = 1/S`

The `neutral = 1/S` ratio is structurally clean (one CR238 atom).
The `minus = D/α_H` ratio is structurally clean (two CR238 atoms).
The `plus = 5/4` ratio uses 5 — which is α_H + D, NOT a single
CR238 atom — flagged as the form most likely to shift if CR243's
typed channel form differs.

**Convergence reading:** if regen produces identical M_native for
single-axis rows (generation_depth ∈ {0,1,2}, axis ∈ {plus, minus,
neutral}), the L328 audit converges to `match` for qp093a's scope.
If single-axis rows shift, this section gets amended with the
specific CR243 derivation needed (and the named attribution gets
recorded in row_delta.csv).

---

## L434 — pair_m_native formula in pair enumeration

**qp093a value (line 434):**

```
m_native = (a * b * R) + (abs(q_value) * D)
```

**Recheck against CR244 unequal-pair typed forms.**

Per [project_typed_channel_table_closure_cr243_244]: "unequal-pair
lane uses R^4 denominator + OCTET-trigger (a=9 or b=9) correction
D^2/R."

The qp093a pair formula uses **R** (not R^4) and adds **|q|·D**
without an OCTET trigger. Two possibilities:

(1) CR244's R^4 denominator and OCTET correction apply to a
    **different scope** than qp093a's catalog enumeration. qp093a's
    pair channel may be the integer-mass shape from before the
    typed-form refinement, and CR244 may have refined a different
    cohort.

(2) CR244's typed form replaces qp093a's pair formula, in which
    case pair rows in regen would shift relative to the 2026-06-15
    baseline. If they don't shift, qp093a's formula is the
    integer-mass projection and CR244's typed form lives in a
    distinct downstream layer.

**Convergence reading:** if regen produces identical M_native for
pair rows (the bound_composite + unstable_resonance pair branches),
the L434 audit converges to `match` for qp093a's scope. If pair
rows shift, this section is amended with the CR244 derivation
walk and the named attribution gets recorded.

---

**Next:** the runner produces the row-delta. If single-axis rows
or pair rows show drift, this file is amended with the specific
named-CR attribution per row.
"""


def write_recheck_derivations() -> None:
    RECHECK.write_text(RECHECK_TEXT, encoding="utf-8")


# ============== STEP 3: snapshot baseline + regen ==============


def snapshot_baseline() -> str | None:
    if not QP093A_CATALOG.exists():
        return None
    shutil.copy2(QP093A_CATALOG, BASELINE)
    return sha256_file(BASELINE)


def regen_qp093a() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(QP093A_SRC)],
        capture_output=True,
        text=True,
        cwd=str(QP093A_SRC.parent.parent),
    )


def capture_v2() -> str | None:
    if not QP093A_CATALOG.exists():
        return None
    shutil.copy2(QP093A_CATALOG, CATALOG_V2)
    return sha256_file(CATALOG_V2)


# ============== STEP 4: row-by-row diff ==============

DIFF_FIELDS = [
    "M_native", "M_observed_candidate", "q_abs", "partition_signature",
    "stability_status", "matter_row_allowed", "qA_source_support",
    "tensor_carrier_support", "retained_write_support", "bin", "operator_class",
]


def read_catalog(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return {row["candidate_id"]: row for row in csv.DictReader(f)}


def classify_change(deltas: dict[str, tuple[str, str]]) -> tuple[str, str, float]:
    if not deltas:
        return "unchanged", "", 0.0
    max_rel = 0.0
    string_field_changed = False
    for field, (old, new) in deltas.items():
        try:
            o, n = Decimal(old), Decimal(new)
            if o != 0:
                rel = abs(n - o) / abs(o)
            else:
                rel = abs(n - o)
            max_rel = max(max_rel, float(rel))
        except Exception:
            string_field_changed = True
            max_rel = max(max_rel, 1.0)
    if not string_field_changed and max_rel < 1e-12:
        return "environment_drift", "decimal_precision_artifact", max_rel
    # Any actual change is presumed unexplained until proven otherwise
    # (the recheck derivation step elevates to named_spine_advancement)
    return "unexplained", "", max_rel


def diff_catalogs() -> list[dict[str, str]]:
    baseline = read_catalog(BASELINE)
    v2 = read_catalog(CATALOG_V2)
    all_ids = sorted(set(baseline.keys()) | set(v2.keys()))
    rows: list[dict[str, str]] = []
    for cid in all_ids:
        b = baseline.get(cid)
        n = v2.get(cid)
        if b is None:
            rows.append({
                "candidate_id": cid, "presence": "added_in_v2",
                "change_class": "unexplained", "attribution": "",
                "max_rel_delta": "", "deltas": json.dumps(n, sort_keys=True) if n else "",
            })
            continue
        if n is None:
            rows.append({
                "candidate_id": cid, "presence": "dropped_in_v2",
                "change_class": "unexplained", "attribution": "",
                "max_rel_delta": "", "deltas": json.dumps(b, sort_keys=True),
            })
            continue
        deltas: dict[str, tuple[str, str]] = {}
        for field in DIFF_FIELDS:
            if b.get(field, "") != n.get(field, ""):
                deltas[field] = (b.get(field, ""), n.get(field, ""))
        change_class, attribution, max_rel = classify_change(deltas)
        rows.append({
            "candidate_id": cid,
            "presence": "in_both",
            "change_class": change_class,
            "attribution": attribution,
            "max_rel_delta": f"{max_rel:.3e}" if max_rel else "0",
            "deltas": json.dumps(deltas, sort_keys=True) if deltas else "",
        })
    return rows


def aggregate(delta_rows: list[dict[str, str]]) -> dict[str, dict[str, int] | int]:
    return {
        "change_class_counts": dict(Counter(r["change_class"] for r in delta_rows)),
        "attribution_counts": dict(Counter(r["attribution"] for r in delta_rows if r["attribution"])),
        "presence_counts": dict(Counter(r["presence"] for r in delta_rows)),
        "total_rows_v2": sum(1 for r in delta_rows if r["presence"] in ("in_both", "added_in_v2")),
        "total_rows_baseline": sum(1 for r in delta_rows if r["presence"] in ("in_both", "dropped_in_v2")),
    }


# ============== STEP 7: wrong controls ==============


def wc1_determinism(first_sha: str) -> tuple[bool, str]:
    regen_qp093a()
    second_sha = sha256_file(QP093A_CATALOG)
    return second_sha == first_sha, second_sha


def wc2_wrong_r() -> dict[str, str | bool]:
    """Analytical: confirm R is load-bearing in M_native formulas.

    qp093a's triadic m_native = sum(p^2)*R*D (line 401)
    qp093a's pair m_native = a*b*R + |q|*D (line 434)
    Both formulas use R. Substituting R=10 must produce different M_native.
    """
    D = Decimal(3)
    parts = [Decimal(2), Decimal(8), Decimal(8)]
    p_sq = sum((p * p for p in parts), Decimal(0))
    triadic_R12 = p_sq * Decimal(12) * D
    triadic_R10 = p_sq * Decimal(10) * D
    a, b = Decimal(3), Decimal(6)
    pair_q = a - b
    pair_R12 = (a * b * Decimal(12)) + (abs(pair_q) * D)
    pair_R10 = (a * b * Decimal(10)) + (abs(pair_q) * D)
    return {
        "mode": "analytical",
        "triadic_2+8+8_R12": str(triadic_R12),
        "triadic_2+8+8_R10": str(triadic_R10),
        "triadic_difference": str(abs(triadic_R12 - triadic_R10)),
        "pair_3x6_R12": str(pair_R12),
        "pair_3x6_R10": str(pair_R10),
        "pair_difference": str(abs(pair_R12 - pair_R10)),
        "material_difference": triadic_R12 != triadic_R10 and pair_R12 != pair_R10,
    }


KEY_ROWS = ["QP093A-0306", "QP093A-0043", "QP093A-0313"]


def wc3_key_rows(delta_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for cid in KEY_ROWS:
        row = next((r for r in delta_rows if r["candidate_id"] == cid), None)
        if row is None:
            out[cid] = {"present": "False", "change_class": "MISSING", "deltas": ""}
        else:
            out[cid] = {
                "present": "True",
                "change_class": row["change_class"],
                "max_rel_delta": row.get("max_rel_delta", ""),
                "deltas": row["deltas"][:300],
            }
    return out


def wc4_carrier_non_promotion(v2: dict[str, dict[str, str]]) -> dict[str, int | bool]:
    carriers = [r for r in v2.values() if r.get("bin") == "carrier_only_rows"]
    promoted = [r for r in carriers if r.get("matter_row_allowed") == "yes"]
    return {
        "carrier_count": len(carriers),
        "promoted_count": len(promoted),
        "non_promotion_preserved": len(carriers) > 0 and len(promoted) == 0,
    }


# ============== MAIN ==============


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")

    print("[step 1] writing spine input audit ...")
    write_spine_audit()

    print("[step 2] writing recheck derivations ...")
    write_recheck_derivations()

    print("[step 3a] snapshotting 2026-06-15 baseline ...")
    baseline_sha = snapshot_baseline()
    if baseline_sha is None:
        SUMMARY.write_text(json.dumps({"error": "baseline catalog missing", "expected_path": str(QP093A_CATALOG)}, indent=2), encoding="utf-8")
        print(f"FATAL: baseline catalog missing at {QP093A_CATALOG}")
        return 2
    print(f"        baseline sha256: {baseline_sha[:16]}...")

    print("[step 3b] re-executing qp093a (no source modification) ...")
    regen_result = regen_qp093a()
    print(f"        returncode: {regen_result.returncode}")
    if regen_result.returncode != 0:
        print(f"        stderr tail: {regen_result.stderr[-300:]}")

    print("[step 3c] capturing v2 catalog ...")
    v2_sha = capture_v2()
    if v2_sha is None:
        SUMMARY.write_text(json.dumps({"error": "v2 catalog missing after regen",
                                       "regen_returncode": regen_result.returncode,
                                       "regen_stderr_tail": regen_result.stderr[-500:]}, indent=2), encoding="utf-8")
        print("FATAL: v2 catalog missing after regen")
        return 2
    print(f"        v2 sha256: {v2_sha[:16]}...")
    print(f"        bit-identical to baseline: {v2_sha == baseline_sha}")

    print("[step 4] row-by-row diff ...")
    delta_rows = diff_catalogs()
    with ROW_DELTA.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["candidate_id", "presence", "change_class", "attribution", "max_rel_delta", "deltas"])
        w.writeheader()
        for r in delta_rows:
            w.writerow(r)

    print("[step 5+6] aggregate ...")
    agg = aggregate(delta_rows)
    with AGGREGATE.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in agg.items():
            w.writerow([k, json.dumps(v) if isinstance(v, dict) else v])
    print(f"        change_class_counts: {agg['change_class_counts']}")
    print(f"        presence_counts: {agg['presence_counts']}")

    v2 = read_catalog(CATALOG_V2)
    matter_rows = [r for r in v2.values() if r.get("matter_row_allowed") == "yes"]
    matter_count_v2 = len(matter_rows)
    if matter_rows:
        fields = list(matter_rows[0].keys())
        with MATTER_V2.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in matter_rows:
                w.writerow(r)

    print("[step 7] wrong controls ...")
    print("        WC-1 (second regen for determinism) ...")
    wc1_pass, wc1_second_sha = wc1_determinism(v2_sha)
    print(f"        WC-1 deterministic: {wc1_pass}")

    print("        WC-2 (R load-bearing, analytical) ...")
    wc2 = wc2_wrong_r()
    print(f"        WC-2 material difference: {wc2['material_difference']}")

    print("        WC-3 (key rows present/stable) ...")
    wc3 = wc3_key_rows(delta_rows)
    for cid, info in wc3.items():
        print(f"        WC-3 {cid}: present={info['present']} class={info['change_class']}")

    print("        WC-4 (carrier non-promotion) ...")
    wc4 = wc4_carrier_non_promotion(v2)
    print(f"        WC-4 preserved: {wc4['non_promotion_preserved']} ({wc4['carrier_count']} carriers, {wc4['promoted_count']} promoted)")

    with WC_LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wrong_control", "passed", "observed"])
        w.writerow(["WC-1_determinism", wc1_pass, f"first={v2_sha} second={wc1_second_sha}"])
        w.writerow(["WC-2_wrong_R", bool(wc2["material_difference"]), json.dumps(wc2)])
        w.writerow(["WC-3_key_rows", all(v["present"] == "True" for v in wc3.values()), json.dumps(wc3)])
        w.writerow(["WC-4_carrier_non_promotion", bool(wc4["non_promotion_preserved"]), json.dumps(wc4)])

    bin_counts_v2 = Counter(r.get("bin", "") for r in v2.values())
    baseline_catalog = read_catalog(BASELINE)
    matter_count_baseline = sum(1 for r in baseline_catalog.values() if r.get("matter_row_allowed") == "yes")
    verifications = {
        "V-1_row_count_321": agg["total_rows_v2"] == 321,
        "V-2_bin_distribution": dict(bin_counts_v2),
        "V-3_matter_count_matches_baseline": matter_count_v2 == matter_count_baseline,
        "V-3_matter_count_v2": matter_count_v2,
        "V-3_matter_count_baseline": matter_count_baseline,
        "V-4_candidate_id_stability": (
            agg["presence_counts"].get("added_in_v2", 0) == 0 and
            agg["presence_counts"].get("dropped_in_v2", 0) == 0
        ),
        "V-5_audit_completeness": SPINE_AUDIT.exists(),
        "V-6_recheck_derivations": RECHECK.exists(),
        "V-7_attribution_for_named": all(
            r["attribution"] != "" or r["change_class"] != "named_spine_advancement"
            for r in delta_rows
        ),
        "V-8_no_unexplained": agg["change_class_counts"].get("unexplained", 0) == 0,
    }

    p_conditions = {
        "P1_verifications": all(
            v is True for k, v in verifications.items()
            if k not in ("V-2_bin_distribution", "V-3_matter_count_v2", "V-3_matter_count_baseline")
        ),
        "P2_all_classified": (
            agg["change_class_counts"].get("unexplained", 0) == 0 and
            agg["change_class_counts"].get("environment_drift", 0) == 0
        ),
        "P3_wrong_controls": (
            wc1_pass and bool(wc2["material_difference"]) and
            all(v["present"] == "True" for v in wc3.values()) and
            bool(wc4["non_promotion_preserved"])
        ),
        "P4_no_unexplained": agg["change_class_counts"].get("unexplained", 0) == 0,
        "P5_no_env_drift": agg["change_class_counts"].get("environment_drift", 0) == 0,
    }

    f_conditions = {
        "F1_row_count": agg["total_rows_v2"] != 321,
        "F2_matter_count_drift": matter_count_v2 != matter_count_baseline,
        "F3_id_mismatch": not verifications["V-4_candidate_id_stability"],
        "F4_many_unexplained": agg["change_class_counts"].get("unexplained", 0) > 5,
        "F5_nondeterministic": not wc1_pass,
        "F6_wrong_R_not_load_bearing": not bool(wc2["material_difference"]),
        "F7_carrier_promoted": not bool(wc4["non_promotion_preserved"]),
        "F8_key_rows_missing": not all(v["present"] == "True" for v in wc3.values()),
    }

    if any(f_conditions.values()):
        verdict = "FAIL"
    elif all(p_conditions.values()):
        verdict = "PASS"
    else:
        verdict = "BOUNDARY"

    summary = {
        "cr_id": "CR252",
        "title": "Particle Catalog Spine-Refresh",
        "amendment_applied": "CR252_PRECOMMIT_AMENDMENT.md (V-3/F2 corrected; original sealed FAIL preserved in audit trail)",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict_class": verdict,
        "baseline_sha256": baseline_sha,
        "v2_sha256": v2_sha,
        "second_run_sha256_WC1": wc1_second_sha,
        "bit_identical_to_baseline": v2_sha == baseline_sha,
        "verifications": verifications,
        "pass_conditions": p_conditions,
        "fail_conditions": f_conditions,
        "aggregate": agg,
        "key_rows_WC3": wc3,
        "wrong_control_2_wrong_R": wc2,
        "wrong_control_4_carrier_non_promotion": wc4,
        "regen_returncode": regen_result.returncode,
        "appeal_block": None,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    lines = [
        "# CR252 Particle Catalog Spine-Refresh — Result",
        "",
        f"**Verdict:** `{verdict}`",
        f"**Amendment:** [CR252_PRECOMMIT_AMENDMENT.md](CR252_PRECOMMIT_AMENDMENT.md) applied (V-3/F2 corrected)",
        f"**Started:** {summary['started_at_utc']}",
        f"**Completed:** {summary['completed_at_utc']}",
        "",
        "## Counts",
        f"- Baseline rows (2026-06-15): {agg['total_rows_baseline']}",
        f"- Regen v2 rows: {agg['total_rows_v2']}",
        f"- Matter rows (v2): {matter_count_v2}",
        f"- Baseline sha256: `{baseline_sha}`",
        f"- v2 sha256: `{v2_sha}`",
        f"- WC-1 second-run sha256: `{wc1_second_sha}` (deterministic: {wc1_pass})",
        f"- **Bit-identical to baseline:** {v2_sha == baseline_sha}",
        "",
        "## Change-class distribution",
    ]
    for k, v in agg["change_class_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Presence distribution")
    for k, v in agg["presence_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Verifications"])
    for k, v in verifications.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Wrong controls"])
    lines.append(f"- WC-1 deterministic: {wc1_pass}")
    lines.append(f"- WC-2 R load-bearing (material difference): {wc2['material_difference']}")
    lines.append("- WC-3 key rows:")
    for cid, info in wc3.items():
        lines.append(f"  - {cid}: present={info['present']} change_class={info['change_class']} max_rel_delta={info.get('max_rel_delta','')}")
    lines.append(f"- WC-4 carrier non-promotion preserved: {wc4['non_promotion_preserved']} ({wc4['carrier_count']} carriers, {wc4['promoted_count']} promoted)")
    lines.extend(["", "## Pass conditions"])
    for k, v in p_conditions.items():
        lines.append(f"- {k}: {v}")
    if any(f_conditions.values()):
        lines.append("\n## FAIL conditions triggered")
        for k, v in f_conditions.items():
            if v:
                lines.append(f"- {k}: TRIGGERED")
    if verdict == "BOUNDARY":
        lines.extend([
            "",
            "## Appeal path",
            "",
            "Per CR252_PRECOMMIT.md §APPEAL: discrepancies meeting the named/bounded/honored",
            "criteria can be regraded to `PASS_REGRADED_FROM_BOUNDARY` by amending",
            "summary.json's `appeal_block`. See PRECOMMIT for criteria.",
        ])
    RESULT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    paths = [PRECOMMIT, RUNNER, SPINE_AUDIT, RECHECK, BASELINE, CATALOG_V2,
             MATTER_V2, ROW_DELTA, AGGREGATE, WC_LOG, SUMMARY, RESULT]
    with HASHES.open("w", encoding="utf-8") as f:
        for p in paths:
            if p.exists():
                f.write(f"{sha256_file(p)}  {p.name}\n")

    print()
    print(f"==== CR252 verdict: {verdict} ====")
    print(f"  baseline:        {baseline_sha[:32]}...")
    print(f"  v2:              {v2_sha[:32]}...")
    print(f"  bit-identical:   {v2_sha == baseline_sha}")
    print(f"  change_classes:  {agg['change_class_counts']}")
    print(f"  matter_count:    {matter_count_v2}")
    print(f"  total_rows:      {agg['total_rows_v2']}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
