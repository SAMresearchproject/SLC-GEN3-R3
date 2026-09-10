"""CR104c Appeal - 9/16 + 9/8 unification via upstream G745c PASS.

CR104b locked the open question:
  "Can SAM derive the 9/8 bounce factor from resolved half-write geometry?"

CR104b candidate Form 2 was:
  D^2 / 2^D = 9/8 at D=3 (only D=3 gives non-trivial value among {2,3,4})

CR104c records that upstream G745c PASSed showing:
  - 9/8  = D^2 / 2^D       (full-cell ratio)
  - 9/16 = D^2 / 2^(D+1)   (half-write-side residue)
  Both non-trivial only at D=3 in the physical dimension range {2,3,4}
  The Higgs (D+1) exponent decomposes as 9/16 + 7/16 = 1 cleanly
  Reciprocal control passes: 9/16 degrades all fermion fits

This is a STRUCTURAL closure of CR104b's question for Form 2.
Application to DS014 d/b quark masses remains an upstream open task.

Does NOT modify CR104b question lock (immutable).
Does NOT modify CR104, CR104a, or any prior CR verdict.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR104B_LOCK = BRANCH_DIR / "CR104b_NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION" / "CR104b_question_lock.json"

UPSTREAM_G745C = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE/G745c_output.json")
UPSTREAM_G744C = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_output.json")
UPSTREAM_DS014 = Path(r"C:/VS/Stam_model-A-v1.0/discovery_briefs/DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX/DS014_summary.json")

APPEAL_LOCK = CR_DIR / "CR104c_appeal_lock.json"
APPEAL_LOCK_SIBLING = CR_DIR / "CR104c_appeal_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR104c_result.md"


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
    print("CR104c runner: starting (9/16 + 9/8 unification appeal)")

    g745_sha = sha256_file(UPSTREAM_G745C)
    g744_sha = sha256_file(UPSTREAM_G744C)
    ds014_sha = sha256_file(UPSTREAM_DS014)
    cr104b_sha = sha256_file(CR104B_LOCK)

    cr104b = json.load(open(CR104B_LOCK, "r", encoding="utf-8")) if CR104B_LOCK.exists() else {}
    cr104b_question_sha = cr104b.get("user_question_sha256", "")

    appeal = {
        "lock_id": "CR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL_LOCK",
        "branch": "14_FOUNDATIONAL_TESTS",
        "appeal_target_cr": "CR104b",
        "appeal_target_question_unchanged_sha256": cr104b_question_sha,
        "sealed_at_utc": now_utc(),
        "what_this_appeal_records": (
            "CR104b locked the question: can SAM derive 9/8 from D=3 half-write "
            "geometry? CR104b candidate Form 2 was D^2/2^D = 9/8 at D=3. "
            "Upstream G745c PASSed showing both 9/8 = D^2/2^D (full-cell) and "
            "9/16 = D^2/2^(D+1) (half-write-side residue) are non-trivial only "
            "at D=3 in the physical dimension range {2,3,4}; the Higgs (D+1) "
            "exponent decomposes as 9/16 + 7/16 = 1 cleanly. CR104b Form 2 is "
            "structurally closed."
        ),
        "upstream_evidence_hashes": {
            "G745c_output.json (PASS)": g745_sha,
            "G744c_output.json (PASS)": g744_sha,
            "DS014_summary.json (existing 9/8 d/b application)": ds014_sha,
        },
        "cr104b_chain": {
            "CR104b_question_lock_sha256": cr104b_sha,
            "CR104b_user_question_sha256": cr104b_question_sha,
        },
        "specific_closures": [
            "Form 2 D^2/2^D = 9/8 at D=3 is upstream-verified (G745c P2.5)",
            "Companion Form D^2/2^(D+1) = 9/16 at D=3 is also upstream-verified (G745c P2.1)",
            "9/8 and 9/16 form one D=3 algebra: shared numerator D^2 = 9, denominators 2^D = 8 and 2^(D+1) = 16 (G745c P2.5)",
            "9/16 + 7/16 = 1 decomposition of the Higgs (D+1) exponent at D=3 (G745c P2.3)",
            "Reciprocal control: 9/16 universally degrades fermion mass predictions (electron through charm), confirming structural-not-fit role (G745c P2.4)",
            "D=3 unique among physical dimensions {2,3,4}: D=2 and D=4 collapse to trivial values 1 and 1/2 (G745c P2.1)",
        ],
        "what_remains_open": [
            "DS014 d/b quark mass application: 9/8 multiplier on d and b base masses needs the same structural derivation that the Higgs scalar lane now has",
            "DS014_reciprocal_control.py outcome on whether 9/8 improves u/s/c/t too has not been re-verified by Courtroom; pending upstream",
            "Whether the SAM-X-007 (-3/4) and SAM-X-008 (+1/3 primary) forward-blind predictions (CR098) use the same D=3 algebra structure",
        ],
        "what_this_does_NOT_do": [
            "modify CR104b question lock (immutable)",
            "modify CR104 GATE_3 partial closure verdict",
            "modify CR104a Layer 4a/4b appeal lock",
            "modify CR106 14 branch verdict zipper",
            "claim 9/8 is fully derived for DS014 d/b application; that step remains open",
        ],
    }

    with open(APPEAL_LOCK, "w", encoding="utf-8") as f:
        json.dump(appeal, f, indent=2)

    lock_sha = sha256_file(APPEAL_LOCK)
    APPEAL_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")

    print(f"  appeal sealed: {lock_sha}")

    md = []
    md.append("# CR104c 9/16 + 9/8 Unification Appeal - Sealed\n\n")
    md.append("## Verdict\n\n```text\nCR104c_NINE_SIXTEENTHS_AND_NINE_EIGHTHS_UNIFICATION_APPEAL_LOCKED\n```\n\n")
    md.append("## What This Appeal Records\n\n")
    md.append(appeal["what_this_appeal_records"] + "\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR104b question_lock_sha256                   = {cr104b_sha}\n")
    md.append(f"CR104b user_question_sha256                   = {cr104b_question_sha}\n")
    md.append(f"upstream G745c_output.json sha256             = {g745_sha}\n")
    md.append(f"upstream G744c_output.json sha256             = {g744_sha}\n")
    md.append(f"upstream DS014_summary.json sha256            = {ds014_sha}\n")
    md.append(f"appeal_lock_sha256                            = {lock_sha}\n")
    md.append("```\n\n")
    md.append("## Specific Upstream Closures\n\n")
    for item in appeal["specific_closures"]:
        md.append(f"- {item}\n")
    md.append("\n## What Remains Open\n\n")
    for item in appeal["what_remains_open"]:
        md.append(f"- {item}\n")
    md.append("\n## What This Appeal Does Not Do\n\n")
    for item in appeal["what_this_does_NOT_do"]:
        md.append(f"- {item}\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print("CR104c runner: complete")


if __name__ == "__main__":
    main()
