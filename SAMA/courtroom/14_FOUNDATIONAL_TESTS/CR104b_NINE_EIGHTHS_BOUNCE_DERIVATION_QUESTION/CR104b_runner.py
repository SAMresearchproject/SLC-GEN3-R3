"""CR104b 9/8 bounce factor derivation question lock.

Locks the user's question and candidate derivation forms into the
cryptographic record. Does NOT derive 9/8. Does NOT modify any prior
CR. Records DS014 upstream verification and the four candidate
derivation forms sketched in conversation.

User authorization 2026-06-13: "Fortune favors the bold- keep it in
the courtroom. Any failure can provide extremely valuable breadcrumbs
downstream- success would be a provincial hole in one."
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

BLINDNESS_PROTOCOL = COURTROOM_DIR / "13_CERN_INDEPENDENT_TESTS" / "BLINDNESS_PROTOCOL.md"
DS014_SUMMARY = Path(r"C:/VS/Stam_model-A-v1.0/discovery_briefs/DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX/DS014_summary.json")
DS014_RECIPROCAL = Path(r"C:/VS/Stam_model-A-v1.0/discovery_briefs/DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX/DS014_reciprocal_control.py")
G435_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G435_BOUNCE_COST_MASS_PROPORTIONALITY/G435_output.json")
G432_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G432_BOUNCE_COST_EIGHTH_SLOT_CORRECTION/G432_output.json")
G470_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G470_SW_SPLIT_BOUNCE_ACTION_THEOREM/G470_output.json")

PREDICTIONS_CSV = CR_DIR / "CR104b_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR104b_prediction_commit.json"
QUESTION_LOCK = CR_DIR / "CR104b_question_lock.json"
QUESTION_LOCK_SIBLING = CR_DIR / "CR104b_question_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR104b_summary.json"
RESULT_MD = CR_DIR / "CR104b_result.md"

USER_QUESTION_VERBATIM = (
    "And the 9/8 might be the native resolved-bounce correction, not a fit, "
    "if we can connect it to R=12 / D=3 / 1/2 write geometry. This is the "
    "big question now: Can SAM derive the 9/8 bounce factor from resolved "
    "half-write geometry?"
)

USER_AUTHORIZATION_BOLD = (
    "Fortune favors the bold- keep it in the courtroom. Any failure can "
    "provide extremely valuable breadcrumbs downstream- success would be "
    "a provincial hole in one."
)

CANDIDATE_DERIVATIONS = [
    {
        "form_id": "FORM_1",
        "name": "binary_cells_plus_center_over_binary_cells",
        "formula": "(2^D + 1) / 2^D",
        "value_at_D_3": "9/8",
        "value_at_D_2": "5/4",
        "value_at_D_4": "17/16",
        "structural_reading": "2^D spatial octants plus one central write event, normalized by spatial octants",
    },
    {
        "form_id": "FORM_2",
        "name": "dimension_squared_over_binary_cell",
        "formula": "D^2 / 2^D",
        "value_at_D_3": "9/8",
        "value_at_D_2": "4/4 = 1 (no correction)",
        "value_at_D_4": "16/16 = 1 (no correction)",
        "structural_reading": "Only D=3 gives a non-trivial ratio greater than 1; D=2 and D=4 collapse to identity. Would single out 3D world as structurally privileged.",
    },
    {
        "form_id": "FORM_3",
        "name": "radix_minus_dim_over_binary_cell",
        "formula": "(R - D) / 2^D",
        "value_at_D_3": "(12-3)/8 = 9/8",
        "value_at_D_2": "n/a (R is native to D=3)",
        "value_at_D_4": "n/a",
        "structural_reading": "Uses R=12 explicitly; connects to substrate algebra denominator",
    },
    {
        "form_id": "FORM_4",
        "name": "cube_topology_corners_plus_interior_over_corners",
        "formula": "(2^D corners + 1 interior) / 2^D corners",
        "value_at_D_3": "9/8 (cube: 8 corners + 1 volume)",
        "value_at_D_2": "5/4 (square: 4 corners + 1 face)",
        "value_at_D_4": "17/16 (tesseract: 16 corners + 1 volume)",
        "structural_reading": "Topological reading; bounce normalizes by spatial corners; write event lives at interior",
    },
]

DERIVATION_PATH_REQUIRED_FOR_THEOREM_CLOSURE = [
    "QGA021 half-write route (1/2 SW | 1/2 W | 1/2 OUT | 1/2 IN | 1/2 W | 1/2 SW) maps onto edges of the D=3 binary cell, not just abstract sequence",
    "WRITE event lives at interior volume of the cube (resolved 3D ledger event)",
    "Bounce energy normalizes by corners (octants = 2^D = 8)",
    "Resulting (8 + 1)/8 = 9/8 emerges as the UNIQUE non-trivial bounce correction at D=3",
    "DS014 reciprocal control confirms 9/8 improves d/b only, not u/s/c/t (already in upstream as control test)",
]

POSSIBLE_OUTCOMES = {
    "QUESTION_CLOSED_BY_UPSTREAM_THEOREM": "SAM upstream produces theorem-grade PASS deriving 9/8 from D=3 half-write geometry; appeal row CR104b-1 records closure; hole in one",
    "QUESTION_DISFAVORED_BY_RECIPROCAL_CONTROL_FAILURE": "DS014 reciprocal control finds 9/8 improves u/s/c/t too; reduces to fit; G435 bounce cost loses theorem-grade status for d/b corrections; substantial breadcrumb downstream",
    "QUESTION_REMAINS_OPEN": "no upstream derivation, no reciprocal control failure; question stays sealed for next attempt",
}


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    print("CR104b runner: starting (9/8 bounce derivation question lock)")

    pred_rows = [
        {"row_id": "USER_QUESTION_VERBATIM", "row_class": "VERBATIM_USER_INSIGHT_LOCK",
         "content": USER_QUESTION_VERBATIM, "content_sha256": sha256_text(USER_QUESTION_VERBATIM)},
        {"row_id": "USER_AUTHORIZATION_BOLD", "row_class": "AUTHORIZATION_LOCK",
         "content": USER_AUTHORIZATION_BOLD, "content_sha256": sha256_text(USER_AUTHORIZATION_BOLD)},
    ]
    for f in CANDIDATE_DERIVATIONS:
        s = json.dumps(f, sort_keys=True)
        pred_rows.append({"row_id": f["form_id"], "row_class": "CANDIDATE_DERIVATION_NOTE",
                          "content": s, "content_sha256": sha256_text(s)})

    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pred_rows[0].keys()))
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR104b_QUESTION_LOCK_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "what_is_locked": "user question + bold-authorization + four candidate derivation forms + required derivation path + DS014 upstream reference",
            "what_is_NOT_claimed": "no derivation, no modification of prior CR verdicts, no theorem-grade promotion",
            "upstream_question_lock_sha256": "fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867",
        }, f, indent=2)
    print(f"  question lock committed {prediction_sha[:16]} at {prediction_utc}")

    upstream_hashes = {
        "DS014_summary.json": sha256_file(DS014_SUMMARY),
        "DS014_reciprocal_control.py": sha256_file(DS014_RECIPROCAL),
        "G435_output.json (bounce mass proportionality PASS)": sha256_file(G435_OUTPUT),
        "G432_output.json (bounce eighth-slot correction)": sha256_file(G432_OUTPUT),
        "G470_output.json (SW split bounce action theorem PASS)": sha256_file(G470_OUTPUT),
        "BLINDNESS_PROTOCOL.md": sha256_file(BLINDNESS_PROTOCOL),
    }
    blindness_sha = upstream_hashes["BLINDNESS_PROTOCOL.md"]
    print("  upstream verification hashes:")
    for name, h in upstream_hashes.items():
        print(f"    {name[:42]:44s} {h[:16] if h else 'NOT_FOUND'}")

    question_lock = {
        "lock_id": "CR104b_NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION_LOCK",
        "branch": "14_FOUNDATIONAL_TESTS",
        "cr_id": "CR104b",
        "sealed_at_utc": prediction_utc,
        "user_question_verbatim": USER_QUESTION_VERBATIM,
        "user_question_sha256": sha256_text(USER_QUESTION_VERBATIM),
        "user_authorization_bold_verbatim": USER_AUTHORIZATION_BOLD,
        "user_authorization_bold_sha256": sha256_text(USER_AUTHORIZATION_BOLD),
        "upstream_verification": {
            "DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX": "uses 9/8 layered_fraction with value 1.125 to improve d and b quark mass predictions to ~3% relative error; DS014_reciprocal_control.py tests fit-vs-structural dichotomy",
            "G432_BOUNCE_COST_EIGHTH_SLOT_CORRECTION": "the '8' in 9/8 connects to 2^D = 8 slot_denominator",
            "G435_BOUNCE_COST_MASS_PROPORTIONALITY_PASS": "r_bounce = (A0/2) * (q / 2^D); 8/8 predictions PASS, 7/7 wrong controls PASS",
            "G470_SW_SPLIT_BOUNCE_ACTION_THEOREM_PASS": "combines G425 + Gate-7/Gate-8 + G435 into one action theorem",
        },
        "upstream_source_hashes_at_runner_time": upstream_hashes,
        "candidate_derivation_forms": CANDIDATE_DERIVATIONS,
        "derivation_path_required_for_theorem_closure": DERIVATION_PATH_REQUIRED_FOR_THEOREM_CLOSURE,
        "possible_outcomes_forward_blind": POSSIBLE_OUTCOMES,
        "what_CR104b_does_not_do": [
            "does not claim to derive 9/8",
            "does not modify CR100 question lock, CR103a appeal lock, CR104 verdict, CR104a Layer 4 lock",
            "does not commit SAM to any specific candidate derivation form",
            "does not promote DS014 layered_fraction beyond its current status",
            "does not modify any 09a CR result",
        ],
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "blindness_protocol_sha256": blindness_sha,
    }
    with open(QUESTION_LOCK, "w", encoding="utf-8") as f:
        json.dump(question_lock, f, indent=2)

    lock_sha = sha256_file(QUESTION_LOCK)
    QUESTION_LOCK_SIBLING.write_text(lock_sha + "\n", encoding="ascii")
    print(f"  question lock sealed: {lock_sha}")

    summary = {
        "cr_id": "CR104b",
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "APPEAL_FORWARD_RESEARCH_QUESTION_LOCK_FOR_UPSTREAM_DERIVATION",
        "execution_status": "CLEAN",
        "result_class": "NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION_LOCKED_PENDING_UPSTREAM_CLOSURE",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "user_question_sha256": sha256_text(USER_QUESTION_VERBATIM),
        "candidate_derivation_count": len(CANDIDATE_DERIVATIONS),
        "upstream_verification_count": len(upstream_hashes),
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "question_lock_sha256": lock_sha,
        "blindness_protocol_sha256": blindness_sha,
        "open_debts": [
            "Upstream SAM has not yet derived 9/8 from D=3 half-write geometry; this CR locks the target",
            "DS014_reciprocal_control.py outcome not re-verified by Courtroom; pending upstream confirmation",
            "BLINDNESS_PROTOCOL sha256 sibling pending curator sign-off",
            "14 branch seal sha256 sibling pending curator sign-off",
        ],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR104b 9/8 Bounce Factor Derivation Question - Sealed\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append("CR104b_NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION_LOCKED_PENDING_UPSTREAM_CLOSURE\n")
    md.append("(PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n")
    md.append("```\n\n")
    md.append("## Cryptographic Locks\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"question_lock_sha256     = {lock_sha}\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## User Question (Locked Verbatim)\n\n")
    md.append("> *\"" + USER_QUESTION_VERBATIM + "\"*\n\n")
    md.append("**Question sha256:** `" + sha256_text(USER_QUESTION_VERBATIM) + "`\n\n")
    md.append("## User Bold Authorization (Also Locked)\n\n")
    md.append("> *\"" + USER_AUTHORIZATION_BOLD + "\"*\n\n")
    md.append("## Upstream Verification\n\n")
    md.append("```text\n")
    md.append("DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX uses 9/8 = 1.125 as a\n")
    md.append("layered_fraction multiplier on d and b quark mass predictions.\n")
    md.append("Includes explicit DS014_reciprocal_control.py testing whether\n")
    md.append("9/8 is structural (d/b only) or fit (improves u/s/c/t too).\n")
    md.append("\n")
    md.append("The '8' in 9/8 connects to 2^D = 8 = slot_denominator in\n")
    md.append("G432/G435/G470 bounce cost theorem chain. The '9' has no\n")
    md.append("current upstream derivation - this is the open question.\n")
    md.append("```\n\n")
    md.append("## Four Candidate Derivation Forms (Courtroom Note)\n\n")
    md.append("| Form | Formula | D=3 | D=2 | D=4 |\n|---|---|---|---|---|\n")
    for f in CANDIDATE_DERIVATIONS:
        md.append(f"| {f['form_id']} | `{f['formula']}` | **{f['value_at_D_3']}** | {f['value_at_D_2']} | {f['value_at_D_4']} |\n")
    md.append("\nForm 2 (`D^2 / 2^D`) is the only candidate giving non-trivial > 1 at D=3 and collapsing to 1 at D=2 and D=4. Would single out 3D world as structurally privileged.\n\n")
    md.append("## Derivation Path Required For Theorem-Grade Closure\n\n")
    for i, step in enumerate(DERIVATION_PATH_REQUIRED_FOR_THEOREM_CLOSURE, 1):
        md.append(f"{i}. {step}\n")
    md.append("\n## Possible Forward-Blind Outcomes\n\n")
    for cls, desc in POSSIBLE_OUTCOMES.items():
        md.append(f"- **{cls}**: {desc}\n")
    md.append("\n## Upstream Source Hashes At Runner Time\n\n```text\n")
    for name, h in upstream_hashes.items():
        md.append(f"{name:55s} {h or 'NOT_FOUND'}\n")
    md.append("```\n\n")
    md.append("## What CR104b Does NOT Do\n\n")
    for n in question_lock["what_CR104b_does_not_do"]:
        md.append(f"- {n}\n")
    md.append("\n## Rule-9 Line\n\n```text\n")
    md.append("This CR could have been generated unverifiably if no upstream\n")
    md.append("SAM work used 9/8 anywhere. DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX\n")
    md.append("demonstrates upstream use of the exact 9/8 = 1.125 layered_fraction\n")
    md.append("on d/b masses with an explicit reciprocal control. The question is\n")
    md.append("real, the derivation target is concrete, and the cryptographic\n")
    md.append("lock prevents quiet rewriting later.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR104b runner: complete")


if __name__ == "__main__":
    main()
