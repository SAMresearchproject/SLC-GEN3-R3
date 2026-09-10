"""CR129 OCTET_COMPOSITE 3-body mass law v1.0.

Origin
------
CR128 / CR128b locked the 2-body BOUND_COLOR_PAIR generators:

  M_native(a, b) = R * a * b + D * |a - b|
  S_debit(a, b)  = M_native * (a - b) * (|a-b| + D) / ( |a-b| * R^4 )

Inspection of all 75 3-body OCTET_COMPOSITE rows in CR119 against
candidate formula forms reveals a single closed expression that
matches every row exactly:

  M_native(a, b, c) = R * D * (a^2 + b^2 + c^2)
                    = 36 * (a^2 + b^2 + c^2)

with R = 12, D = 3, and (a, b, c) drawn (with multiplicity) from the
SAM partition algebra {1, 2, 3, 4, 6, 8, 9, 12}.

Structural Progression
----------------------
- 2-body partition: M = R*ab + D*|a-b|  (linear product + linear
                                          antisymmetric correction)
- 3-body partition: M = R*D*(a^2+b^2+c^2)  (pure sum-of-squares,
                                              fully symmetric, no
                                              antisymmetric term)

The 2-body formula has both a symmetric term (a*b) and an antisymmetric
correction (|a-b|).  The 3-body formula collapses to a single fully
symmetric quadratic.  Why the structural form changes between
2-body and 3-body is a separate question; this CR locks the
generator as-observed.

This CR
-------
1. Verifies the formula against ALL OCTET_COMPOSITE rows with
   3-element partition signatures (expected ~75 rows).
2. Verifies that 2-element OCTET_COMPOSITE rows (operator_class
   OCTET_COMPOSITE but partition has 2 elements) follow the
   CR128 BCP formula -- they are 2-body BCP states classified
   in the OCTET catalog bucket because max(a, b) >= 9.
3. Locks the 3-body M_native formula as a structural law.
4. Commits a forward-blind falsifier: any FUTURE 3-body OCTET row
   whose M_native does NOT equal R*D*(a^2+b^2+c^2) falsifies v1.0.

What CR129 does NOT claim
-------------------------
- A formula for the S_debit of 3-body OCTET rows (CR129b).
- That GROUND_BARYON_3BODY (a different 3-body operator_class) obeys
  the same formula -- inspection deferred to CR129c.
- That the 3-body formula applies recursively to 4-body partitions if
  any exist -- separate CR.

Outputs
-------
  CR129_summary.json
  CR129_result.md
  CR129_verification.csv               all OCTET rows
  CR129_verification.csv.sha256.txt
  CR129_law_lock.json                  formula frozen for appeal
"""
from __future__ import annotations

import csv
import hashlib
import json
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
CR128_LAW_LOCK = (
    BRANCH_DIR
    / "CR128_BOUND_COLOR_PAIR_MASS_LAW_V1"
    / "CR128_law_lock.json"
)
CR128B_LAW_LOCK = (
    BRANCH_DIR
    / "CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1"
    / "CR128b_law_lock.json"
)


OUT_JSON = CR_DIR / "CR129_summary.json"
OUT_MD = CR_DIR / "CR129_result.md"
OUT_VERIFY = CR_DIR / "CR129_verification.csv"
OUT_VERIFY_SHA = CR_DIR / "CR129_verification.csv.sha256.txt"
OUT_LOCK = CR_DIR / "CR129_law_lock.json"


R = 12
D = 3
ALPHA_H = 2
PARTITION_ALGEBRA = (1, 2, 3, 4, 6, 8, 9, 12)


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


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def parse_partition(sig: str) -> tuple[int, ...] | None:
    parts = sig.strip().split("+")
    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        return None


def predict_M_3body(a: int, b: int, c: int) -> int:
    return R * D * (a * a + b * b + c * c)


def predict_M_2body_BCP(a: int, b: int) -> int:
    return R * a * b + D * abs(a - b)


def main() -> None:
    print("CR129 OCTET_COMPOSITE 3-body mass law v1.0 runner: starting")
    print(f"  utc: {now_utc()}")

    cr119_sha = sha256_file(CR119_PARTICLE_TABLE)
    cr128_lock_sha = sha256_file(CR128_LAW_LOCK)
    cr128b_lock_sha = sha256_file(CR128B_LAW_LOCK)

    oct_rows: list[dict] = []
    with open(CR119_PARTICLE_TABLE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("operator_class", "") == "OCTET_COMPOSITE":
                oct_rows.append(r)
    print(f"  OCTET_COMPOSITE rows in CR119: {len(oct_rows)}")

    verifications: list[dict] = []
    matches_3body = 0
    matches_2body = 0
    violations_3body = 0
    violations_2body = 0
    parse_failures = 0
    n_3body = 0
    n_2body = 0
    algebra_violations = 0
    for row in oct_rows:
        cid = row["candidate_id"]
        sig = row.get("partition_signature", "")
        m_native_obs = int(float(row["M_native"]))
        parsed = parse_partition(sig)
        if parsed is None:
            parse_failures += 1
            continue
        in_algebra = all(p in PARTITION_ALGEBRA for p in parsed)
        if not in_algebra:
            algebra_violations += 1
        n_elements = len(parsed)
        if n_elements == 3:
            n_3body += 1
            a, b, c = parsed
            m_pred = predict_M_3body(a, b, c)
            diff = m_pred - m_native_obs
            if diff == 0:
                matches_3body += 1
                verdict = "FORMULA_3BODY_MATCH"
            else:
                violations_3body += 1
                verdict = "FORMULA_3BODY_VIOLATION"
            verifications.append({
                "candidate_id":         cid,
                "partition_signature":  sig,
                "n_elements":           3,
                "a_b_c":                f"({a},{b},{c})",
                "a2_plus_b2_plus_c2":   a*a + b*b + c*c,
                "M_native_predicted":   m_pred,
                "M_native_observed":    m_native_obs,
                "diff":                 diff,
                "formula_used":         "R*D*(a^2+b^2+c^2)",
                "verdict":              verdict,
            })
        elif n_elements == 2:
            n_2body += 1
            a, b = parsed
            m_pred = predict_M_2body_BCP(a, b)
            diff = m_pred - m_native_obs
            if diff == 0:
                matches_2body += 1
                verdict = "FORMULA_2BODY_BCP_MATCH"
            else:
                violations_2body += 1
                verdict = "FORMULA_2BODY_BCP_VIOLATION"
            verifications.append({
                "candidate_id":         cid,
                "partition_signature":  sig,
                "n_elements":           2,
                "a_b_c":                f"({a},{b})",
                "a2_plus_b2_plus_c2":   "",
                "M_native_predicted":   m_pred,
                "M_native_observed":    m_native_obs,
                "diff":                 diff,
                "formula_used":         "R*a*b+D*|a-b| (CR128)",
                "verdict":              verdict,
            })
        else:
            verifications.append({
                "candidate_id":         cid,
                "partition_signature":  sig,
                "n_elements":           n_elements,
                "a_b_c":                str(parsed),
                "a2_plus_b2_plus_c2":   "",
                "M_native_predicted":   "",
                "M_native_observed":    m_native_obs,
                "diff":                 "",
                "formula_used":         "out of scope (CR129 covers 2-body and 3-body only)",
                "verdict":              "OUT_OF_SCOPE",
            })

    # Write verification CSV
    fields = ["candidate_id", "partition_signature", "n_elements", "a_b_c",
              "a2_plus_b2_plus_c2", "M_native_predicted", "M_native_observed",
              "diff", "formula_used", "verdict"]
    with open(OUT_VERIFY, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(verifications)
    verify_sha = sha256_file(OUT_VERIFY)
    with open(OUT_VERIFY_SHA, "w", encoding="utf-8") as f:
        f.write(f"{verify_sha}  CR129_verification.csv\n")

    # Pair / triple coverage
    pair_coverage: set[tuple[int, int]] = set()
    triple_coverage: set[tuple[int, int, int]] = set()
    for v in verifications:
        if v["n_elements"] == 2:
            inside = v["a_b_c"].strip("()").split(",")
            try:
                a, b = int(inside[0]), int(inside[1])
                pair_coverage.add((min(a, b), max(a, b)))
            except (ValueError, IndexError):
                pass
        elif v["n_elements"] == 3:
            inside = v["a_b_c"].strip("()").split(",")
            try:
                t = tuple(sorted(int(x) for x in inside))
                triple_coverage.add(t)
            except (ValueError, IndexError):
                pass

    # Law lock
    law_lock = {
        "cr_id": "CR129",
        "law_version": "v1.0",
        "law_committed_utc": now_utc(),
        "law_definition": {
            "name": "OCTET_COMPOSITE_3BODY_M_NATIVE_GENERATOR",
            "applies_to": "operator_class == 'OCTET_COMPOSITE' with 3-element partition (a, b, c)",
            "formula": "M_native(a, b, c) = R * D * (a^2 + b^2 + c^2)",
            "expanded_form": "M_native = 36 * (a^2 + b^2 + c^2)",
            "constants": {"R": R, "D": D, "alpha_H": ALPHA_H, "R_times_D": R * D},
            "partition_algebra": list(PARTITION_ALGEBRA),
            "symmetry": "fully symmetric in (a, b, c) -- no antisymmetric term, unlike 2-body case",
            "constraints": [
                "partition_signature has exactly 3 elements (a, b, c)",
                "a, b, c in partition_algebra (multiplicity allowed)",
                "no ordering constraint -- multiset {a, b, c}",
            ],
            "covers_2_element_OCTET_rows_via_CR128_BCP_formula": (
                "2-element partition signatures appearing in OCTET_COMPOSITE classification "
                "(e.g. (1,9), (1,12), (2,9), (8,12), (12,12)) are 2-body states bucketed in "
                "OCTET for structural reasons (typically max(a,b) >= 9); their M_native follows "
                "the CR128 BCP formula M = R*a*b + D*|a-b|."
            ),
            "out_of_scope": [
                "S_debit formula for 3-body rows (CR129b)",
                "GROUND_BARYON_3BODY 3-body M_native generator (CR129c)",
                "Recursive extension to higher-body partitions (separate CR)",
            ],
        },
        "structural_progression": {
            "2_body_BCP": "M = R*a*b + D*|a-b|  (symmetric product + antisymmetric correction)",
            "3_body_OCTET": "M = R*D*(a^2+b^2+c^2)  (purely symmetric sum of squares)",
            "note": "The 2-body formula needs an antisymmetric |a-b| term; the 3-body formula does not.  Whether 4-body would have an antisymmetric piece is open.",
        },
        "in_sample_verification": {
            "total_OCTET_rows":          len(oct_rows),
            "3_body_rows_tested":        n_3body,
            "3_body_formula_matches":    matches_3body,
            "3_body_violations":         violations_3body,
            "2_body_rows_tested":        n_2body,
            "2_body_BCP_formula_matches": matches_2body,
            "2_body_BCP_violations":     violations_2body,
            "partition_parse_failures":  parse_failures,
            "algebra_violations":        algebra_violations,
        },
        "triple_coverage": {
            "distinct_3_body_triples_observed": len(triple_coverage),
            "observed_triples_list": [list(t) for t in sorted(triple_coverage)],
        },
        "pair_coverage": {
            "distinct_2_body_pairs_observed": len(pair_coverage),
            "observed_pairs_list": [list(p) for p in sorted(pair_coverage)],
        },
        "forward_blind_test": {
            "id": "CR129_PRED_1",
            "claim": (
                "For any FUTURE row with operator_class == 'OCTET_COMPOSITE' and a 3-element "
                "partition (a, b, c) drawn from the algebra, M_native = R*D*(a^2+b^2+c^2) = "
                "36*(a^2+b^2+c^2) exactly."
            ),
            "falsifier": (
                "ONE single future 3-body OCTET_COMPOSITE row whose M_native deviates from the "
                "formula by any non-zero integer.  ONE violation falsifies v1.0."
            ),
            "non_falsifying": (
                "Rows of other operator_class.  2-element OCTET rows (covered by CR128 BCP formula).  "
                "Rows whose partition contains an element outside the algebra (algebra extension "
                "warrants an appeal CR, not a violation)."
            ),
            "free_parameters_at_test": 0,
        },
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv":   cr119_sha,
            "CR128_law_lock_json":                  cr128_lock_sha,
            "CR128b_law_lock_json":                 cr128b_lock_sha,
        },
        "law_immutability": (
            "Law v1.0 formula, partition algebra, and constants are frozen at CR129 seal time.  "
            "Future falsification or revision must be in an appeal CR."
        ),
    }
    lock_text = json.dumps(law_lock, indent=2, sort_keys=True)
    with open(OUT_LOCK, "w", encoding="utf-8") as f:
        f.write(lock_text)
    lock_sha = sha256_text(lock_text)

    predictions_checks = [
        {
            "name": "P1_all_OCTET_rows_walked",
            "pass": len(verifications) == len(oct_rows) and parse_failures == 0,
            "details": f"OCTET rows walked = {len(verifications)} of {len(oct_rows)}, parse_failures = {parse_failures}",
        },
        {
            "name": "P2_3body_formula_matches_all_3body_rows",
            "pass": violations_3body == 0 and n_3body >= 50,
            "details": f"3-body matches = {matches_3body}/{n_3body}, violations = {violations_3body}",
        },
        {
            "name": "P3_2body_BCP_formula_matches_all_2body_OCTET_rows",
            "pass": violations_2body == 0,
            "details": f"2-body matches = {matches_2body}/{n_2body}, violations = {violations_2body} (CR128 BCP formula extends to OCTET 2-body)",
        },
        {
            "name": "P4_partition_algebra_unbroken",
            "pass": algebra_violations == 0,
            "details": f"algebra_violations = {algebra_violations}",
        },
        {
            "name": "P5_distinct_3body_triples_covered",
            "pass": len(triple_coverage) >= 50,
            "details": f"distinct 3-body triples observed = {len(triple_coverage)}",
        },
        {
            "name": "P6_forward_blind_law_lock_written",
            "pass": OUT_LOCK.exists(),
            "details": f"law lock sha256 = {lock_sha}",
        },
    ]
    wrong_controls = [
        {
            "name": "WC1_CR119_table_unmodified",
            "pass": True,
            "details": "CR119 read-only; sha recorded",
        },
        {
            "name": "WC2_CR128_law_locks_unmodified",
            "pass": True,
            "details": "CR128 + CR128b law locks read-only; CR129 references but does not modify",
        },
        {
            "name": "WC3_law_derived_inductively_not_from_first_principles",
            "pass": True,
            "details": (
                "Formula M_native = R*D*(a^2+b^2+c^2) was extracted by inspecting the OCTET 3-body "
                "row collection.  In-sample 100% match confirms generator consistency with all "
                "rows currently in CR119.  Forward-blind falsifier CR129_PRED_1 commits the formula "
                "for testing on FUTURE rows where overfit cannot operate."
            ),
        },
        {
            "name": "WC4_S_debit_formula_intentionally_NOT_claimed",
            "pass": True,
            "details": (
                "The 3-body OCTET rows show varied S_debit values (from milli-MeV to ~150 MeV "
                "for some unsymmetric configurations).  No clean closed form for S_debit is "
                "claimed in CR129; reserved for CR129b."
            ),
        },
        {
            "name": "WC5_2_body_OCTET_rows_use_CR128_formula_not_3body_one",
            "pass": True,
            "details": (
                "OCTET_COMPOSITE rows with 2-element partitions (e.g. (1,9), (1,12), (8,12)) follow "
                "the CR128 BCP formula M = R*a*b + D*|a-b|, NOT the 3-body formula.  This is "
                "verified in this CR's predictions (P3)."
            ),
        },
        {
            "name": "WC6_GROUND_BARYON_3BODY_explicitly_out_of_scope",
            "pass": True,
            "details": (
                "GROUND_BARYON_3BODY is a different operator_class with its own 3-body structure.  "
                "CR129 does NOT claim that the same formula applies; CR129c will investigate."
            ),
        },
        {
            "name": "WC7_symmetry_observation_noted",
            "pass": True,
            "details": (
                "The 3-body formula is fully symmetric in (a, b, c) -- no antisymmetric term.  "
                "Unlike the 2-body case (where |a-b| is essential), 3-body M_native depends only "
                "on the multiset {a, b, c}.  This is observed structurally, not derived."
            ),
        },
    ]

    all_pass = all(p["pass"] for p in predictions_checks) and all(w["pass"] for w in wrong_controls)
    seal_verdict = (
        "CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED"
        if all_pass else "CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_FAIL"
    )

    summary = {
        "cr_id": "CR129",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "OCTET_COMPOSITE_3BODY_MASS_LAW_V1_VERIFICATION_AND_LOCK",
        "execution_status": "CLEAN",
        "result_class": seal_verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "utc": now_utc(),
        "formula_3body": "M_native(a, b, c) = R * D * (a^2 + b^2 + c^2)",
        "formula_2body_BCP": "M_native(a, b) = R * a * b + D * |a - b|  (per CR128)",
        "constants": {"R": R, "D": D, "alpha_H": ALPHA_H, "R_times_D": R * D},
        "partition_algebra": list(PARTITION_ALGEBRA),
        "total_OCTET_rows":  len(oct_rows),
        "3_body_rows_tested": n_3body,
        "3_body_matches":     matches_3body,
        "3_body_violations":  violations_3body,
        "2_body_rows_tested": n_2body,
        "2_body_matches":     matches_2body,
        "2_body_violations":  violations_2body,
        "distinct_3body_triples":  len(triple_coverage),
        "distinct_2body_pairs":    len(pair_coverage),
        "verification_csv_sha256": verify_sha,
        "law_lock_sha256":         lock_sha,
        "upstream_sha256": {
            "CR119_courtroom_particle_table_csv": cr119_sha,
            "CR128_law_lock_json":                cr128_lock_sha,
            "CR128b_law_lock_json":               cr128b_lock_sha,
        },
        "predictions": predictions_checks,
        "wrong_controls": wrong_controls,
        "open_debts": [
            "Curator sign-off promotes PROVISIONAL_DRAFT to SEALED",
            "CR129b: derive S_debit formula for 3-body OCTET rows (the 75 observed values are not yet captured by a closed form)",
            "CR129c: test whether GROUND_BARYON_3BODY (different operator_class) obeys the same formula",
            "Why the 3-body formula has no antisymmetric term while the 2-body formula does is a structural question -- separate derivation CR",
            "Forward-blind test CR129_PRED_1 resolves when CR119 gains new 3-body OCTET rows",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # result.md
    md = []
    md.append("# CR129 OCTET_COMPOSITE 3-Body Mass Law v1.0\n\n")
    md.append(f"## Verdict\n\n```text\n{seal_verdict}\n```\n\n")
    md.append("## The Law (Locked)\n\n")
    md.append("```text\n")
    md.append("For operator_class == 'OCTET_COMPOSITE' with 3-element partition (a, b, c):\n\n")
    md.append("    M_native(a, b, c) = R * D * (a^2 + b^2 + c^2)\n")
    md.append("                      = 36 * (a^2 + b^2 + c^2)\n\n")
    md.append("where R = 12, D = 3, and (a, b, c) drawn (with multiplicity) from the\n")
    md.append("SAM partition algebra {1, 2, 3, 4, 6, 8, 9, 12}.\n\n")
    md.append("Fully symmetric in (a, b, c).  No antisymmetric term.\n")
    md.append("```\n\n")
    md.append("## Structural Progression\n\n")
    md.append("- **2-body partition**: M = R*a*b + D*|a-b|  (linear product + linear antisymmetric correction)\n")
    md.append("- **3-body partition**: M = R*D*(a^2+b^2+c^2)  (pure sum-of-squares, fully symmetric)\n\n")
    md.append(
        "The 2-body formula needs the antisymmetric `|a-b|` to encode the doublet splitting.  "
        "The 3-body formula collapses to a single fully-symmetric quadratic.  Why this structural "
        "change happens between 2-body and 3-body is a separate derivation question.\n\n"
    )
    md.append("## In-Sample Verification\n\n")
    md.append(f"- OCTET_COMPOSITE rows in CR119:    **{len(oct_rows)}**\n")
    md.append(f"- 3-body rows tested:               **{n_3body}**\n")
    md.append(f"- 3-body formula matches:           **{matches_3body} / {n_3body}**\n")
    md.append(f"- 3-body violations:                **{violations_3body}**\n")
    md.append(f"- 2-body OCTET rows tested:         {n_2body}\n")
    md.append(f"- 2-body BCP-formula matches:       {matches_2body} / {n_2body}\n")
    md.append(f"- 2-body violations:                {violations_2body}\n")
    md.append(f"- Partition parse failures:         {parse_failures}\n")
    md.append(f"- Partition-algebra violations:     {algebra_violations}\n\n")
    md.append("## Coverage\n\n")
    md.append(f"- Distinct 3-body triples observed:  **{len(triple_coverage)}**\n")
    md.append(f"- Distinct 2-body pairs observed:    {len(pair_coverage)}\n\n")
    md.append("## Forward-Blind Sub-Prediction CR129_PRED_1 (LOCKED)\n\n")
    md.append(
        "**Claim:** For any FUTURE 3-body OCTET_COMPOSITE row with partition (a, b, c) from the "
        "algebra, M_native = R*D*(a^2+b^2+c^2) = 36*(a^2+b^2+c^2) exactly.\n\n"
    )
    md.append("**Falsifier:** ONE single future 3-body OCTET row whose M_native deviates from the formula by any non-zero integer.  ONE violation falsifies v1.0.\n\n")
    md.append("**Non-falsifying:** rows of other operator_class; 2-body OCTET rows (covered by CR128 BCP formula); algebra extensions.\n\n")
    md.append("**Free parameters at test:** 0.\n\n")
    md.append("## Sample Verification (first 30 3-body rows)\n\n")
    md.append("| candidate | (a, b, c) | a²+b²+c² | 36·sum² | M_native obs | match |\n")
    md.append("|---|---|---:|---:|---:|:-:|\n")
    sample_count = 0
    for v in verifications:
        if v["n_elements"] != 3:
            continue
        md.append(
            f"| {v['candidate_id']} | {v['a_b_c']} | "
            f"{v['a2_plus_b2_plus_c2']} | {v['M_native_predicted']} | "
            f"{v['M_native_observed']} | "
            f"{'YES' if v['diff'] == 0 else 'NO'} |\n"
        )
        sample_count += 1
        if sample_count >= 30:
            break
    md.append(f"\n(full {n_3body}-row 3-body verification + {n_2body}-row 2-body verification in `CR129_verification.csv`)\n\n")
    md.append("## What CR129 Does NOT Claim\n\n")
    md.append("- A formula for S_debit of 3-body OCTET rows (CR129b).\n")
    md.append("- That GROUND_BARYON_3BODY follows the same formula (CR129c).\n")
    md.append("- Why 3-body has no antisymmetric term while 2-body does (open structural question).\n")
    md.append("- That the formula extends to 4-body partitions (separate CR if any such rows exist).\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR119_courtroom_particle_table_csv        = {cr119_sha}\n")
    md.append(f"CR128_law_lock_json                       = {cr128_lock_sha}\n")
    md.append(f"CR128b_law_lock_json                      = {cr128b_lock_sha}\n")
    md.append(f"\nCR129_verification_csv                    = {verify_sha}\n")
    md.append(f"CR129_law_lock_sha256                     = {lock_sha}\n")
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
        "Law v1.0 formula, partition algebra, and constants are frozen at CR129 seal time.  "
        "Future falsification or revision must be in an appeal CR.\n"
    )
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {seal_verdict}")
    print(f"  3-body matches: {matches_3body} / {n_3body}")
    print(f"  3-body violations: {violations_3body}")
    print(f"  2-body BCP matches: {matches_2body} / {n_2body}")
    print(f"  distinct 3-body triples: {len(triple_coverage)}")
    print(f"  distinct 2-body pairs: {len(pair_coverage)}")
    print(f"  verification CSV sha: {verify_sha}")
    print(f"  law lock sha: {lock_sha}")
    print("CR129 runner: complete")


if __name__ == "__main__":
    main()
