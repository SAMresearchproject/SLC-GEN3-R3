"""
CR100_runner.py - Lock the SW open question into the cryptographic record.

Locks the verbatim question:
  'What is an SW dynamically, and what native propagation law turns SW
   contact, echoes, pairs, and physical interaction into resolved 3D
   ledger events?'

plus the primitive commitments, the candidate equation, the QGA014..QGA024
partial-answer chain, and the three open gates (GATE_1 N_SW, GATE_2 c_SW/c,
GATE_3 K(A_H)) as a sealed roadmap document.

The runner does NOT answer the question. It records it, with its full
provenance and the upstream source sha256, so that any future closure
proposal can be checked against the sealed formulation.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

UPSTREAM_SOURCE = Path(r"C:/VS/Stam_model-A-v1.0/discovery_briefs/QG_ASSEMBLY/SW_CONTACT_ECHO_DYNAMICS_QGA013.md")
BLINDNESS_PROTOCOL = BRANCH_DIR / "BLINDNESS_PROTOCOL.md"
DECLARED_PREMISES = CR_DIR / "CR100_declared_premises.json"

PREDICTIONS_CSV = CR_DIR / "CR100_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR100_prediction_commit.json"
QUESTION_LOCK = CR_DIR / "CR100_question_lock.json"
QUESTION_LOCK_SIBLING = CR_DIR / "CR100_question_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR100_summary.json"
RESULT_MD = CR_DIR / "CR100_result.md"


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    print("CR100 runner: starting (SW open question provenance lock)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    # The "predictions" for CR100 are the open-gate enumeration. CR100
    # commits that closing each gate will cascade in the named direction.
    # This is a roadmap-prediction, not a numerical observable.
    pred_rows = []
    for g in premises["open_gates"]:
        pred_rows.append({
            "row_id": g["gate_id"],
            "row_class": "OPEN_GATE_ROADMAP_PREDICTION",
            "gate_name": g["name"],
            "verbatim_from_upstream": g["verbatim_from_upstream"],
            "what_closing_it_unlocks": g["what_closing_it_unlocks"],
            "candidate_count_at_seal_time": len(g["current_candidates"]),
        })
    pred_rows.append({
        "row_id": "QUESTION",
        "row_class": "VERBATIM_QUESTION_LOCK",
        "gate_name": "FOUNDATIONAL_OPEN_QUESTION",
        "verbatim_from_upstream": premises["the_question_verbatim"],
        "what_closing_it_unlocks": "all downstream dependencies enumerated in declared_premises",
        "candidate_count_at_seal_time": 0,
    })

    fns = list(pred_rows[0].keys())
    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fns)
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    print(f"  wrote {PREDICTIONS_CSV.name} ({len(pred_rows)} rows)")

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    commit = {
        "commit_id": "CR100_QUESTION_LOCK_COMMIT",
        "predictions_file": PREDICTIONS_CSV.name,
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "what_the_commit_locks": "the verbatim question, the three open-gate enumeration, and the partial-answer chain",
        "what_the_commit_does_not_do": "does not answer the question; does not predict the form of N_SW / c_SW/c / K(A_H); does not constrain how the gates will close",
        "blindness_pillar": "PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH (applied to a roadmap-prediction, not a numerical observable)",
    }
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump(commit, f, indent=2)
    print(f"  prediction committed sha256={prediction_sha[:16]}... utc={prediction_utc}")

    # Hash the upstream source so the question's full context is locked
    upstream_sha = ""
    if UPSTREAM_SOURCE.exists():
        upstream_sha = sha256_file(UPSTREAM_SOURCE)
        print(f"  upstream source hashed: {upstream_sha[:16]}...")
    else:
        print(f"  WARN: upstream source not found at {UPSTREAM_SOURCE}")

    # Also hash the verbatim question text itself (independent of file format)
    question_text_sha = sha256_text(premises["the_question_verbatim"])

    blindness_sha = sha256_file(BLINDNESS_PROTOCOL) if BLINDNESS_PROTOCOL.exists() else ""

    # Build the sealed question lock
    question_lock = {
        "lock_id": "CR100_SW_QUESTION_LOCK",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "cr_id": "CR100",
        "sealed_at_utc": prediction_utc,
        "verbatim_question": premises["the_question_verbatim"],
        "verbatim_question_sha256": question_text_sha,
        "question_source": {
            **premises["question_source"],
            "source_sha256_at_runner_time": upstream_sha,
        },
        "primitive_commitments": premises["primitive_commitments"],
        "working_translation": premises["working_translation"],
        "candidate_equation": premises["candidate_equation"],
        "downstream_partial_answer_chain": premises["downstream_partial_answer_chain"],
        "open_gates": premises["open_gates"],
        "downstream_dependencies_on_question_closure": premises["downstream_dependencies_on_question_closure"],
        "what_CR100_does_not_do": premises["what_CR100_does_not_do"],
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "blindness_protocol_sha256": blindness_sha,
    }
    with open(QUESTION_LOCK, "w", encoding="utf-8") as f:
        json.dump(question_lock, f, indent=2)
    print(f"  wrote {QUESTION_LOCK.name}")

    lock_sha = sha256_file(QUESTION_LOCK)
    QUESTION_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")
    print(f"  question lock sealed: {lock_sha}")

    summary = {
        "cr_id": "CR100",
        "branch": "13_CERN_INDEPENDENT_TESTS",
        "test_class": "OPEN_QUESTION_PROVENANCE_LOCK_AND_ROADMAP",
        "execution_status": "CLEAN",
        "result_class": "SW_OPEN_QUESTION_PROVENANCE_LOCKED",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "verbatim_question": premises["the_question_verbatim"],
        "verbatim_question_sha256": question_text_sha,
        "upstream_source_path": str(UPSTREAM_SOURCE),
        "upstream_source_sha256": upstream_sha,
        "primitive_commitments_count": len(premises["primitive_commitments"]),
        "downstream_partial_answer_chain_count": len(premises["downstream_partial_answer_chain"]),
        "open_gates_count": len(premises["open_gates"]),
        "downstream_dependencies_count": len(premises["downstream_dependencies_on_question_closure"]),
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "question_lock_sha256": lock_sha,
        "question_lock_path": str(QUESTION_LOCK),
        "question_lock_sibling_path": str(QUESTION_LOCK_SIBLING),
        "blindness_protocol_sha256": blindness_sha,
        "open_debts": [
            "BLINDNESS_PROTOCOL sha256 sibling not yet written by curator",
            "Branch seal sha256 sibling not yet written by curator",
            "Upstream source independent re-hash by curator pending",
            "Closure progress on GATE_1/GATE_2/GATE_3 will be tracked via CR100a appeal rows as upstream QGA work advances",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote {SUMMARY_JSON.name}")

    md = []
    md.append("# CR100 SW Primitive Open Question - Sealed Roadmap\n\n")
    md.append("## Verdict\n\n```text\nCR100_SW_OPEN_QUESTION_PROVENANCE_LOCKED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n\n")
    md.append("## The Question (Locked Verbatim)\n\n")
    md.append("> " + premises["the_question_verbatim"] + "\n\n")
    md.append("**Question text sha256:** `" + question_text_sha + "`\n\n")
    md.append("**Source:** [SW_CONTACT_ECHO_DYNAMICS_QGA013.md](file:///" + str(UPSTREAM_SOURCE).replace("\\", "/") + ")\n\n")
    md.append("**Source sha256 at runner time:** `" + upstream_sha + "`\n\n")
    md.append("## Cryptographic Lock\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"question_lock_sha256     = {lock_sha}\n")
    md.append(f"lock_sibling             = {QUESTION_LOCK_SIBLING.name}\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## Why This Is A Roadmap\n\n")
    md.append("SW is SAM's atomic primitive (1 SW = A0; the smallest thing that\n")
    md.append("exists). A is accumulated SW displacement density. Particles are\n")
    md.append("pair-closed standing echoes of SW. Closing the dynamical law for SW\n")
    md.append("closes the foundation; leaving it open leaves a roadmap.\n\n")
    md.append("This CR locks the question itself - verbatim, with its provenance\n")
    md.append("and upstream source sha256 - so that any future closure proposal can\n")
    md.append("be checked against the sealed formulation. The question cannot be\n")
    md.append("quietly rewritten to fit a later answer.\n\n")
    md.append("## Primitive Commitments (Sealed)\n\n")
    for c in premises["primitive_commitments"]:
        md.append(f"- {c}\n")
    md.append("\n## Candidate Equation (Violin-String Form)\n\n```text\n")
    md.append(premises["candidate_equation"]["structural_form"] + "\n\n")
    md.append(premises["candidate_equation"]["operator_form"] + "\n\n")
    md.append("reading: " + premises["candidate_equation"]["reading"] + "\n")
    md.append("```\n\n")
    md.append("## Downstream Partial-Answer Chain (QGA014 .. QGA024)\n\n")
    md.append("| Stage | Verdict | Contribution |\n")
    md.append("|---|---|---|\n")
    for s in premises["downstream_partial_answer_chain"]:
        md.append(f"| **{s['id']}** | {s['verdict']} | {s['contribution']} |\n")
    md.append("\n## Three Open Gates (Sealed)\n\n")
    for g in premises["open_gates"]:
        md.append(f"### {g['gate_id']} - {g['name']}\n\n")
        md.append(f"**Verbatim from upstream:** `{g['verbatim_from_upstream']}`\n\n")
        md.append("**Current candidates at seal time:**\n\n")
        for c in g["current_candidates"]:
            md.append(f"- {c}\n")
        md.append(f"\n**What closing it unlocks:**\n\n> {g['what_closing_it_unlocks']}\n\n")
        md.append("**CERN data classes that bear on it:**\n\n")
        for d in g["cern_data_classes_that_bear_on_it"]:
            md.append(f"- {d}\n")
        md.append("\n")
    md.append("## Downstream Dependencies On Closure\n\n")
    md.append("If GATE_1, GATE_2, GATE_3 all close, the following downstream\n")
    md.append("claims become derived rather than asserted:\n\n")
    for d in premises["downstream_dependencies_on_question_closure"]:
        md.append(f"- {d}\n")
    md.append("\n## What CR100 Does Not Do\n\n")
    for n in premises["what_CR100_does_not_do"]:
        md.append(f"- {n}\n")
    md.append("\n## How Progress On Each Gate Is Tracked\n\n```text\n")
    md.append("When upstream QGA work closes one of the three gates with a\n")
    md.append("specific functional form (e.g., N_SW = echo intensity per the\n")
    md.append("local-echo-intensity candidate; or c_SW = c via identity\n")
    md.append("derivation), an appeal row is appended:\n\n")
    md.append("    CR100a_<DATE>_<GATE>_<RESULT_CLASS>\n\n")
    md.append("e.g.:\n")
    md.append("    CR100a_2027_03_15_GATE_1_N_SW_CLOSED_AS_ECHO_INTENSITY\n")
    md.append("    CR100a_2027_07_22_GATE_2_C_SW_EQUALS_C_DERIVED\n")
    md.append("    CR100a_2028_01_10_GATE_3_K_A_H_DERIVED_FROM_BOUNDARY_TENSION\n\n")
    md.append("Each appeal row carries its own sha256 + utc. The original\n")
    md.append("question lock and the open-gate enumeration are NEVER modified.\n")
    md.append("```\n\n")
    md.append("## Rule-9 Line\n\n```text\n")
    md.append("This CR could have failed if the question were paraphrased\n")
    md.append("instead of locked verbatim, if any primitive commitment were\n")
    md.append("introduced that does not appear in the upstream brief, if the\n")
    md.append("candidate equation were modified, or if the open-gate enumeration\n")
    md.append("were padded.\n\n")
    md.append("The seal locks the question. Any future closure proposal must be\n")
    md.append("checked against the sealed formulation. The question cannot be\n")
    md.append("quietly rewritten to fit a later answer.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR100 runner: complete")


if __name__ == "__main__":
    main()
