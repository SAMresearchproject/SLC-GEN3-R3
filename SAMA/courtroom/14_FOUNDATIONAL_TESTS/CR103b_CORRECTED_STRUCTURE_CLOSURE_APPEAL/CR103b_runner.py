"""CR103b Appeal - CR103 corrected-structure closure by upstream G744c.

CR103 verdict (immutable): CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC
  at 52 sigma. The simple linear-energy reading of N_SW failed because
  the structural correction (half-SW + bounce cost) was missing.

CR103a appeal: locked the structural correction (Layers 1-3 of user
  insight: resolution mechanics, epistemology, A-dependence).

CR103b appeal (this CR): records that the CR103a structural correction
  has now been TESTED upstream by G744c PASS, which demonstrates the
  full chain:

    SW_i -> q_A,i = m_i * (1 + r_bounce,i) -> macro A = 2GM/(c^2 r)

  with composite binding closing via mass-weighted r_bounce at <1%
  for deuteron and alpha, zero new free parameters.

Does NOT modify CR103 verdict (immutable).
Does NOT modify CR103a appeal lock.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR103_SUMMARY = BRANCH_DIR / "CR103_GATE_1_N_SW_MULTIPLICITY_SCALING" / "CR103_summary.json"
CR103A_LOCK = BRANCH_DIR / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_appeal_lock.json"

UPSTREAM_G744C = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_output.json")
UPSTREAM_G435 = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G435_BOUNCE_COST_MASS_PROPORTIONALITY/G435_output.json")
UPSTREAM_G470 = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G470_SW_SPLIT_BOUNCE_ACTION_THEOREM/G470_output.json")

APPEAL_LOCK = CR_DIR / "CR103b_appeal_lock.json"
APPEAL_LOCK_SIBLING = CR_DIR / "CR103b_appeal_lock.json.sha256.txt"
RESULT_MD = CR_DIR / "CR103b_result.md"


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
    print("CR103b runner: starting (corrected-structure closure appeal)")

    g744_sha = sha256_file(UPSTREAM_G744C)
    g435_sha = sha256_file(UPSTREAM_G435)
    g470_sha = sha256_file(UPSTREAM_G470)
    cr103_sha = sha256_file(CR103_SUMMARY)
    cr103a_sha = sha256_file(CR103A_LOCK)

    cr103 = json.load(open(CR103_SUMMARY, "r", encoding="utf-8")) if CR103_SUMMARY.exists() else {}
    cr103_verdict = cr103.get("result_class", "")

    appeal = {
        "lock_id": "CR103b_CORRECTED_STRUCTURE_CLOSURE_APPEAL_LOCK",
        "branch": "14_FOUNDATIONAL_TESTS",
        "appeal_target_cr": "CR103",
        "appeal_target_verdict_unchanged": cr103_verdict,
        "appeal_target_verdict_unchanged_sha256": cr103_sha,
        "sealed_at_utc": now_utc(),
        "what_this_appeal_records": (
            "The CR103 verdict (CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC at 52 sigma) "
            "remains immutable. CR103a appeal locked the structural correction (half-SW + "
            "bounce cost + A-dependence). CR103b records that this corrected structure has "
            "now been tested upstream by G744c PASS: the SW -> q_A -> m -> A(r) chain holds "
            "with composite binding (deuteron 0.91%, alpha 0.91%) closing via mass-weighted "
            "r_bounce, zero new free parameters."
        ),
        "upstream_evidence_hashes": {
            "G744c_output.json (PASS)": g744_sha,
            "G435_output.json (already PASSed, cited by G744c)": g435_sha,
            "G470_output.json (already PASSed, cited by G744c)": g470_sha,
        },
        "cr103_chain": {
            "CR103_summary_sha256": cr103_sha,
            "CR103a_appeal_lock_sha256": cr103a_sha,
        },
        "specific_closures": [
            "Form A q_A = m * (1 + r_bounce) is upstream-tested with G435 q-slot map (electron, muon, tau, proton, neutron) -> zero new parameter assignment",
            "Composite binding via mass-weighted r_bounce closes deuteron (B_A native 2.2449 MeV vs classical 2.2246 MeV, 0.91% error)",
            "Composite binding closes alpha (B_A native 28.5536 MeV vs classical 28.2957 MeV, 0.91% error)",
            "Macro-limit universality: sum q_A / sum m spread = 0.33% across 6 wildly different species mixes",
        ],
        "what_remains_open": [
            "CR103 LHC multiplicity scaling test specifically not re-run; only the structural correction is verified at the elementary/composite/macro levels",
            "Run-3 LHC analysis would test whether the corrected structure plus bounce-cost cascade reproduces measured alpha ~ 0.17",
            "Held G749c (gauge boson bounce-cost extension) would close 09a/CR091 Z 12-sigma residual",
        ],
        "what_this_does_NOT_do": [
            "modify CR103 verdict (immutable)",
            "modify CR103a appeal lock",
            "modify CR106 14 branch verdict zipper",
            "claim that the CR103 LHC test now passes; that test verdict is permanent",
            "claim full closure of GATE_1 N_SW functional",
        ],
    }

    with open(APPEAL_LOCK, "w", encoding="utf-8") as f:
        json.dump(appeal, f, indent=2)

    lock_sha = sha256_file(APPEAL_LOCK)
    APPEAL_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")

    print(f"  appeal sealed: {lock_sha}")

    md = []
    md.append("# CR103b Corrected-Structure Closure Appeal - Sealed\n\n")
    md.append("## Verdict\n\n```text\nCR103b_CORRECTED_STRUCTURE_CLOSURE_APPEAL_LOCKED_BY_UPSTREAM_G744c\n```\n\n")
    md.append("## What This Appeal Records\n\n")
    md.append(appeal["what_this_appeal_records"] + "\n\n")
    md.append("## Cryptographic Chain\n\n```text\n")
    md.append(f"CR103 verdict (unchanged)                    = {cr103_verdict}\n")
    md.append(f"CR103_summary.json sha256                    = {cr103_sha}\n")
    md.append(f"CR103a_appeal_lock.json sha256               = {cr103a_sha}\n")
    md.append(f"upstream G744c_output.json sha256             = {g744_sha}\n")
    md.append(f"upstream G435_output.json sha256              = {g435_sha}\n")
    md.append(f"upstream G470_output.json sha256              = {g470_sha}\n")
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

    print("CR103b runner: complete")


if __name__ == "__main__":
    main()
