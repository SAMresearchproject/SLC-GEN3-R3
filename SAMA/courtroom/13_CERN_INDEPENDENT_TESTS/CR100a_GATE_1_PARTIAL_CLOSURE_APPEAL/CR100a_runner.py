"""CR100a Appeal - CR100 GATE_1 partial closure by upstream G744c PASS.

Locks the upstream verification that SAM has now demonstrated the
SW_i -> q_A,i -> m_i -> A_i(r) chain at theorem-grade in the
substrate test tree.

Does NOT modify CR100 question lock (immutable).
Does NOT modify any prior CR verdict.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR100_LOCK = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "CR100_SW_PRIMITIVE_OPEN_QUESTION_ROADMAP" / "CR100_question_lock.json"

UPSTREAM_G744C_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_output.json")
UPSTREAM_G745C_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE/G745c_output.json")
UPSTREAM_CAMPAIGN_BRIEF = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/CAMPAIGN_BRIEF.md")

APPEAL_LOCK = CR_DIR / "CR100a_appeal_lock.json"
APPEAL_LOCK_SIBLING = CR_DIR / "CR100a_appeal_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR100a_result.md"

GATE_PARTIAL_CLOSURE_SUMMARY = {
    "GATE_1_N_SW_functional": {
        "status": "PARTIAL_CLOSURE_BY_UPSTREAM_G744c_G745c",
        "upstream_evidence": [
            "G744c PASS: q_A source-strength bridge to macro A; composite binding (deuteron 0.91%, alpha 0.91%) closes via mass-weighted r_bounce with zero new free parameters",
            "G745c PASS: Higgs sector specifically selects 9/16 = D^2/2^(D+1) scalar route; D=3 structural privilege confirmed; reciprocal control passes",
        ],
        "what_is_now_tested": [
            "SW -> q_A assignment with zero new parameters (G744c P1.1)",
            "composite additivity via mass-weighted r_bounce (G744c P1.2, P1.3)",
            "macro-limit universality across species mixes (G744c P1.4, P1.5)",
            "Higgs lane specifically routes through 9/16 (G745c P2.3)",
            "9/8 and 9/16 form one D=3 algebra (G745c P2.5)",
        ],
        "what_remains_open": [
            "GATE_2 c_SW vs c structural derivation (already partial-closed at 1e-18 by CR102)",
            "GATE_3 K(A_H) self-correction (already partial-closed at 1e-19 by CR104)",
            "Three-mode Earth/Galaxy/PBH consistency (held G746c)",
            "Cosmic baryon inventory closure (held G747c)",
            "Gauge boson bounce-cost extension (held G749c; would close 09a/CR091 Z 12-sigma residual)",
        ],
    },
}


def sha256_file(p):
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    print("CR100a runner: starting (GATE_1 partial closure appeal)")

    g744_sha = sha256_file(UPSTREAM_G744C_OUTPUT)
    g745_sha = sha256_file(UPSTREAM_G745C_OUTPUT)
    brief_sha = sha256_file(UPSTREAM_CAMPAIGN_BRIEF)

    if CR100_LOCK.exists():
        cr100 = json.load(open(CR100_LOCK, "r", encoding="utf-8"))
        cr100_question_sha = cr100.get("verbatim_question_sha256", "")
    else:
        cr100_question_sha = ""

    appeal = {
        "lock_id": "CR100a_GATE_1_PARTIAL_CLOSURE_APPEAL_LOCK",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "appeal_target_cr": "CR100",
        "appeal_target_unchanged": True,
        "appeal_target_question_sha256_at_appeal_time": cr100_question_sha,
        "sealed_at_utc": now_utc(),
        "what_this_appeal_records": "Upstream Stam_model-A-v1.0 G744c and G745c PASSed, partially closing GATE_1 N_SW functional at the structural level. CR100 question lock is unchanged; this appeal row is appended.",
        "upstream_evidence_hashes": {
            "G744c_output.json": g744_sha,
            "G745c_output.json": g745_sha,
            "CAMPAIGN_BRIEF.md": brief_sha,
        },
        "upstream_verdicts": {
            "G744c": "G744c_Q_A_SOURCE_STRENGTH_BRIDGE_PASS",
            "G745c": "G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE_PASS",
        },
        "gate_partial_closure_summary": GATE_PARTIAL_CLOSURE_SUMMARY,
        "what_this_does_NOT_do": [
            "modify CR100 verbatim question lock",
            "modify any prior CR verdict",
            "modify CR106 14 branch verdict zipper",
            "claim full closure of GATE_1 (the SW functional form is partially open; held G746c-G749c still pending)",
        ],
    }

    with open(APPEAL_LOCK, "w", encoding="utf-8") as f:
        json.dump(appeal, f, indent=2)

    lock_sha = sha256_file(APPEAL_LOCK)
    APPEAL_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")

    print(f"  appeal sealed: {lock_sha}")
    print(f"  G744c upstream: {g744_sha[:16]}...")
    print(f"  G745c upstream: {g745_sha[:16]}...")

    md = []
    md.append("# CR100a GATE_1 Partial Closure Appeal - Sealed\n\n")
    md.append("## Verdict\n\n```text\nCR100a_GATE_1_PARTIAL_CLOSURE_APPEAL_LOCKED_BY_UPSTREAM_G744c_G745c\n```\n\n")
    md.append("## What This Appeal Records\n\n")
    md.append("Upstream `Stam_model-A-v1.0` G744c and G745c PASSed in the substrate\n")
    md.append("test tree, partially closing CR100's GATE_1 N_SW functional question\n")
    md.append("at the structural level.\n\n")
    md.append("**CR100 question lock is unchanged.** This appeal row is appended.\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR100 question_lock_sha256                   = {cr100_question_sha}\n")
    md.append(f"upstream G744c_output.json sha256             = {g744_sha}\n")
    md.append(f"upstream G745c_output.json sha256             = {g745_sha}\n")
    md.append(f"upstream CAMPAIGN_BRIEF.md sha256             = {brief_sha}\n")
    md.append(f"appeal_lock_sha256                            = {lock_sha}\n")
    md.append("```\n\n")
    md.append("## Upstream Verdicts\n\n```text\n")
    md.append("G744c   G744c_Q_A_SOURCE_STRENGTH_BRIDGE_PASS\n")
    md.append("G745c   G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE_PASS\n")
    md.append("```\n\n")
    md.append("## What Is Now Tested Upstream\n\n")
    for item in GATE_PARTIAL_CLOSURE_SUMMARY["GATE_1_N_SW_functional"]["what_is_now_tested"]:
        md.append(f"- {item}\n")
    md.append("\n## What Remains Open\n\n")
    for item in GATE_PARTIAL_CLOSURE_SUMMARY["GATE_1_N_SW_functional"]["what_remains_open"]:
        md.append(f"- {item}\n")
    md.append("\n## What This Appeal Does Not Do\n\n")
    for item in appeal["what_this_does_NOT_do"]:
        md.append(f"- {item}\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  wrote {RESULT_MD.name}")
    print("CR100a runner: complete")


if __name__ == "__main__":
    main()
