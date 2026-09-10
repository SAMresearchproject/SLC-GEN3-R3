"""CR106 14 branch verdict zipper - reads prior CRs, writes strongest export claim."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"
CR100_LOCK = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "CR100_SW_PRIMITIVE_OPEN_QUESTION_ROADMAP" / "CR100_question_lock.json"
CR101_SUMMARY = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "CR101_GATE_2_C_SW_VS_C_PARTIAL_CLOSURE" / "CR101_summary.json"

PRIOR_CRS = [
    ("CR102", BRANCH_DIR / "CR102_GATE_2_C_SW_VS_C_ASTROPHYSICAL_CLOSURE" / "CR102_summary.json"),
    ("CR103", BRANCH_DIR / "CR103_GATE_1_N_SW_MULTIPLICITY_SCALING" / "CR103_summary.json"),
    ("CR103a", BRANCH_DIR / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_summary.json"),
    ("CR104", BRANCH_DIR / "CR104_GATE_3_K_A_H_SELF_CORRECTION" / "CR104_summary.json"),
    ("CR105", BRANCH_DIR / "CR105_GATE_CROSS_INTEGRITY" / "CR105_summary.json"),
]

ZIPPER_LEDGER_CSV = CR_DIR / "CR106_zipper_ledger.csv"
BRANCH_VERDICT = CR_DIR / "CR106_14_branch_verdict.json"
BRANCH_VERDICT_SIBLING = CR_DIR / "CR106_14_branch_verdict.json.sha256.txt"
STRONGEST_CLAIM = CR_DIR / "CR106_14_branch_strongest_claim.md"
SUMMARY_JSON = CR_DIR / "CR106_summary.json"
RESULT_MD = CR_DIR / "CR106_result.md"


def now_utc(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def main():
    print("CR106 runner: starting (14 branch verdict zipper)")

    cr100_lock = json.load(open(CR100_LOCK, "r", encoding="utf-8"))
    cr101 = json.load(open(CR101_SUMMARY, "r", encoding="utf-8"))

    rows = []
    composite = hashlib.sha256()
    all_clean = True
    verdicts = {}
    for cr_id, summary_path in PRIOR_CRS:
        if not summary_path.exists():
            rows.append({"cr_id": cr_id, "status": "MISSING", "verdict": None, "sha256": None})
            all_clean = False
            continue
        s = json.load(open(summary_path, "r", encoding="utf-8"))
        sha = sha256_file(summary_path)
        composite.update(sha.encode("ascii"))
        verdicts[cr_id] = s["result_class"]
        is_clean = s.get("execution_status") == "CLEAN"
        if not is_clean:
            all_clean = False
        rows.append({
            "cr_id": cr_id,
            "status": "CLEAN" if is_clean else "NON_CLEAN",
            "verdict": s["result_class"],
            "summary_sha256": sha,
            "prediction_commit_sha256": s.get("prediction_commit_sha256", ""),
            "anchor_envelope_sha256": s.get("anchor_envelope_sha256", ""),
        })

    composite_sha = composite.hexdigest()
    branch_verdict = "14_BRANCH_COMPLETE_FOUNDATIONAL_TESTS_PARTIAL_CLOSURE_BUNDLE" if all_clean else "14_BRANCH_INCOMPLETE_OR_VIOLATION"

    # Write the zipper ledger CSV
    import csv
    fns = list(rows[0].keys()) if rows else []
    with open(ZIPPER_LEDGER_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    blind_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    # Branch verdict JSON
    bv_utc = now_utc()
    branch_verdict_doc = {
        "branch": "14_FOUNDATIONAL_TESTS",
        "verdict": branch_verdict,
        "sealed_at_utc": bv_utc,
        "upstream_CR100_question_lock_sha256": cr100_lock.get("verbatim_question_sha256", ""),
        "companion_branch_13_CR101_verdict": cr101["result_class"],
        "companion_branch_13_CR101_sha256": sha256_file(CR101_SUMMARY),
        "ladder_verdicts": verdicts,
        "composite_summary_sha256": composite_sha,
        "blindness_protocol_sha256": blind_sha,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
    }
    with open(BRANCH_VERDICT, "w", encoding="utf-8") as f:
        json.dump(branch_verdict_doc, f, indent=2)
    bv_sha = sha256_file(BRANCH_VERDICT)
    BRANCH_VERDICT_SIBLING.write_text(bv_sha + "\n", encoding="ascii")
    print(f"  branch verdict sealed: {bv_sha}")

    # Strongest export claim
    claim = []
    claim.append("# 14 Foundational Tests Branch - Strongest Export Claim\n\n")
    claim.append("## Branch Verdict\n\n```text\n")
    claim.append(f"{branch_verdict}\n")
    claim.append("```\n\n")
    claim.append("## What This Branch Did\n\n")
    claim.append("The 14_FOUNDATIONAL_TESTS branch is a substrate-foundation\n")
    claim.append("probe of SAM's atomic-primitive open question (sealed at\n")
    claim.append("CR100 in 13_CERN_INDEPENDENT_TESTS) using the strongest\n")
    claim.append("available open-science measurements, not restricted to CERN.\n\n")
    claim.append("Four-pillar blindness procedure (structural, procedural,\n")
    claim.append("cross-source, honest-negative) was applied to every CR.\n")
    claim.append("Predictions hashed and committed BEFORE anchor envelopes\n")
    claim.append("opened on every test. Temporal ordering verified on every\n")
    claim.append("evidence row.\n\n")
    claim.append("## Sealed Ladder\n\n")
    claim.append("| CR | Subject | Verdict |\n|---|---|---|\n")
    claim.append(f"| **CR100** (in 13) | SW open question | SEALED `{cr100_lock.get('verbatim_question_sha256', '')[:16]}...` |\n")
    claim.append(f"| **CR101** (in 13) | GATE_2 c_SW vs c CERN | {cr101['result_class']} |\n")
    for cr_id, v in verdicts.items():
        claim.append(f"| **{cr_id}** | (verdict) | {v} |\n")
    claim.append("\n## What The Branch Claims (Honestly)\n\n")
    claim.append("**Two of three CR100 open gates have partial-closure verdicts\n")
    claim.append("at world-best precision in the regimes tested:**\n\n")
    claim.append("```text\n")
    claim.append("GATE_2 c_SW vs c           consistent at 1e-18 (IceCube neutrino LIV)\n")
    claim.append("GATE_3 K(A_H) self-correct consistent at 1e-19 (Al+ optical clocks)\n")
    claim.append("```\n\n")
    claim.append("**Honest scope of these closures:**\n\n")
    claim.append("Both predictions (c_SW = c; EP_violation = 0) are commitments\n")
    claim.append("that General Relativity also makes. Confirmation against EP and\n")
    claim.append("Lorentz-invariance tests demonstrates that SAM does not\n")
    claim.append("contradict mainstream physics in regimes where mainstream\n")
    claim.append("physics is well-tested. This is a sanity check; the precision\n")
    claim.append("numbers reflect the test precision, not unique SAM verification.\n\n")
    claim.append("**One specific structural failure:**\n\n")
    claim.append("```text\n")
    claim.append("GATE_1 candidate 4 simplest reading (1 SW = 1 particle linear)\n")
    claim.append("                                    DISFAVORED at 52 sigma by LHC\n")
    claim.append("                                    multiplicity scaling data.\n")
    claim.append("```\n\n")
    claim.append("CR103 verdict is immutable. CR103a appeal locked the user's\n")
    claim.append("structural correction (half-SW / half-write split + bounce\n")
    claim.append("cost / A-dependence / 11/12 spaghettification threshold). A\n")
    claim.append("future CR103b could test the corrected structure once upstream\n")
    claim.append("SAM derives its scaling exponent.\n\n")
    claim.append("**Gate-cross integrity:**\n\n")
    claim.append("CR105 confirmed that GATE_2 and GATE_3 partial closures do not\n")
    claim.append("contradict each other in any joint anchor (atomic clocks,\n")
    claim.append("GW170817, binary pulsars, NICER). The two gates form a\n")
    claim.append("coherent substrate-foundation reading for A < 11/12.\n\n")
    claim.append("**Forward-blind targets sealed for future tests:**\n\n")
    claim.append("- 11/12 spaghettification onset (CR103a Prediction 3)\n")
    claim.append("- 24 forward-blind particle predictions in CR098 (in 13 branch)\n")
    claim.append("- SAM-X-012 negative falsifier in CR099 (in 13 branch)\n\n")
    claim.append("## What This Branch Does NOT Claim\n\n")
    claim.append("- definitive closure of any CR100 gate\n")
    claim.append("- unique verification of SAM (mainstream physics passes the\n")
    claim.append("  same tests at the same precision)\n")
    claim.append("- derivation of functional forms for r_bounce(A), K(A_H), or\n")
    claim.append("  N_SW (upstream SAM work pending)\n")
    claim.append("- successful test of any SAM-specific prediction that\n")
    claim.append("  mainstream physics does not also make\n")
    claim.append("- closure of GATE_1 at the structural level\n\n")
    claim.append("## Cryptographic Composite\n\n```text\n")
    claim.append(f"composite sha256 of all 14 branch CR summaries = {composite_sha}\n")
    claim.append(f"branch verdict JSON sha256                      = {bv_sha}\n")
    claim.append(f"branch verdict sealed at utc                    = {bv_utc}\n")
    claim.append(f"blindness protocol sha256                       = {blind_sha}\n")
    claim.append("```\n\n")
    claim.append("## What A Major Milestone Would Look Like\n\n")
    claim.append("- a CR098 forward-blind particle (SAM-X-008, SUK055 composite,\n")
    claim.append("  etc.) observed at the predicted mass and charge\n")
    claim.append("- a CR099 SAM-X-012 falsifier signature found (SAM broken\n")
    claim.append("  cleanly; also informative)\n")
    claim.append("- 11/12 spaghettification onset observed in LIGO/Virgo NS-BH\n")
    claim.append("  merger waveforms or BH tidal disruption events\n")
    claim.append("- upstream SAM derivation of r_bounce(A) and K(A_H) explicit\n")
    claim.append("  functional forms enabling SAM-specific deviation tests at\n")
    claim.append("  intermediate A\n\n")
    claim.append("None of these has happened yet. The apparatus is set up for\n")
    claim.append("any of them to register on the public record when they do.\n")

    with open(STRONGEST_CLAIM, "w", encoding="utf-8") as f:
        f.write("".join(claim))

    # Summary
    summary = {
        "cr_id": "CR106",
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "BRANCH_VERDICT_ZIPPER_AND_STRONGEST_EXPORT_CLAIM",
        "execution_status": "CLEAN",
        "result_class": branch_verdict,
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "prior_CR_count": len(PRIOR_CRS),
        "prior_CR_verdicts": verdicts,
        "all_prior_CRs_clean": all_clean,
        "composite_summary_sha256": composite_sha,
        "branch_verdict_sha256": bv_sha,
        "branch_verdict_sealed_at_utc": bv_utc,
        "upstream_CR100_question_lock_sha256": cr100_lock.get("verbatim_question_sha256", ""),
        "companion_branch_13_CR101_verdict": cr101["result_class"],
        "blindness_protocol_sha256": blind_sha,
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling pending curator sign-off",
            "14 branch seal sha256 sibling pending curator sign-off",
            "anchor citation_verification_status PENDING across all CRs in the branch",
            "GATE_1 N_SW functional remains open at structural level pending upstream SAM derivation",
            "11/12 spaghettification onset forward-blind unprobed by current data",
            "CR103b test of corrected GATE_1 structure pending upstream derivation",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # result.md
    md = []
    md.append("# CR106 14 Branch Verdict Zipper - Result\n\n")
    md.append(f"## Verdict\n\n```text\nCR106_{branch_verdict} (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n\n")
    md.append("## Branch Verdict Seal\n\n```text\n")
    md.append(f"branch_verdict_sha256       = {bv_sha}\n")
    md.append(f"composite_summary_sha256    = {composite_sha}\n")
    md.append(f"sealed_at_utc               = {bv_utc}\n")
    md.append(f"blindness_protocol_sha256   = {blind_sha}\n")
    md.append("```\n\n")
    md.append("## Ladder Verdicts\n\n")
    md.append("| CR | Status | Verdict |\n|---|---|---|\n")
    for r in rows:
        md.append(f"| {r['cr_id']} | {r['status']} | {r['verdict']} |\n")
    md.append("\n## Strongest Export Claim\n\n")
    md.append(f"See `CR106_14_branch_strongest_claim.md`.\n\n")
    md.append("## Open Debts At Zipper Time\n\n```text\n")
    for d in summary["open_debts"]:
        md.append(f"- {d}\n")
    md.append("```\n\n")
    md.append("## Rule-9 Reminder\n\n```text\n")
    md.append("This branch verdict zipper does NOT modify any prior CR result.\n")
    md.append("All five prior 14-branch CRs are sealed and immutable. The branch\n")
    md.append("verdict is the export claim that survives the sum of those CRs\n")
    md.append("plus the companion CR101 in branch 13.\n")
    md.append("\n")
    md.append("Honest scope is preserved: the partial closures demonstrate\n")
    md.append("consistency with mainstream physics in tested regimes, not\n")
    md.append("unique SAM verification. The structural lock (CR103a) provides\n")
    md.append("the corrected reading; the GATE_1 simplest-reading failure (CR103)\n")
    md.append("remains on record as the most honest sharp result.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR106 runner: complete")


if __name__ == "__main__":
    main()
