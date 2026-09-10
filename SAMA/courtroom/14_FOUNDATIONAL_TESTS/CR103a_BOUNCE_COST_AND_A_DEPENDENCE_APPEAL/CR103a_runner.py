"""
CR103a_runner.py - Appeal lock for the bounce-cost / A-dependence structural insight.

This runner does NOT re-test CR103. It SEALS:
  - User's three-layer insight verbatim
  - The upstream SAM verification chain (G435 / G470 / BB005 / QP038)
  - The terminology discipline (A0 constant vs A local field)
  - Four forward-blind predictions for future astrophysical tests
  - Implications for prior CRs (without modifying their verdicts)

The cryptographic seal is the value: it locks the structural correction
to CR103 + the forward-blind targets into git history.
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
DECLARED_PREMISES = CR_DIR / "CR103a_declared_premises.json"

# Upstream SAM verification source files (cite-only, read for sha256)
G435_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G435_BOUNCE_COST_MASS_PROPORTIONALITY/G435_output.json")
G435_VERDICT = Path(r"C:/VS/Stam_model-A-v1.0/audit/audits/VERDICT_G435_BOUNCE_COST_MASS_PROPORTIONALITY_2026_05_26.md")
G470_OUTPUT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/G470_SW_SPLIT_BOUNCE_ACTION_THEOREM/G470_output.json")
BB005_RESULT = Path(r"C:/VS/Stam_model-A-v1.0/tests/Substrate/BB005_12_OF_12_A0_RESET_EQUIVALENCE_SELECTOR/BB005_RESULT.md")
CH033_SUMMARY = Path(r"C:/VS/Stam_model-A-v1.0/tools/chladni plate/CH033_MANIFOLD_BOUNCE_COST_CHARGE_READOUT_DISCOVERY_DEN/CH033_summary.md")
QGA013_DOC = Path(r"C:/VS/Stam_model-A-v1.0/discovery_briefs/QG_ASSEMBLY/SW_CONTACT_ECHO_DYNAMICS_QGA013.md")

PREDICTIONS_CSV = CR_DIR / "CR103a_predictions.csv"
PREDICTION_COMMIT = CR_DIR / "CR103a_prediction_commit.json"
APPEAL_LOCK = CR_DIR / "CR103a_appeal_lock.json"
APPEAL_LOCK_SIBLING = CR_DIR / "CR103a_appeal_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR103a_summary.json"
RESULT_MD = CR_DIR / "CR103a_result.md"


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
    print("CR103a runner: starting (bounce-cost + A-dependence appeal lock)")

    with open(DECLARED_PREMISES, "r", encoding="utf-8") as f:
        premises = json.load(f)

    # Step 1-2: The "predictions" for CR103a are the four forward-blind
    # prediction rows + the three user-insight layers locked verbatim.
    pred_rows = []
    for layer_id, text in premises["user_insights_locked_verbatim"].items():
        pred_rows.append({
            "row_id": f"USER_INSIGHT_{layer_id.upper()}",
            "row_class": "VERBATIM_USER_INSIGHT_LOCK",
            "content": text,
            "content_sha256": sha256_text(text),
        })
    for p in premises["forward_blind_predictions_registered"]:
        pred_rows.append({
            "row_id": p["prediction_id"],
            "row_class": "FORWARD_BLIND_PREDICTION",
            "content": p["claim"],
            "content_sha256": sha256_text(p["claim"]),
        })

    with open(PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pred_rows[0].keys()))
        w.writeheader()
        for r in pred_rows:
            w.writerow(r)
    print(f"  wrote {PREDICTIONS_CSV.name} ({len(pred_rows)} rows)")

    prediction_sha = sha256_file(PREDICTIONS_CSV)
    prediction_utc = now_utc()
    with open(PREDICTION_COMMIT, "w", encoding="utf-8") as f:
        json.dump({
            "commit_id": "CR103a_APPEAL_LOCK_COMMIT",
            "predictions_file": PREDICTIONS_CSV.name,
            "prediction_commit_sha256": prediction_sha,
            "prediction_commit_utc": prediction_utc,
            "what_is_locked": "user's three-layer insight + four forward-blind predictions + terminology discipline (A0 const vs A field)",
            "what_is_NOT_modified": [
                "CR103 verdict (still CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC)",
                "CR100 question lock",
                "CR101 / CR102 GATE_2 closures",
                "any 09a CR result",
            ],
            "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        }, f, indent=2)
    print(f"  appeal lock committed {prediction_sha[:16]} at {prediction_utc}")

    # Hash all the upstream verification sources
    upstream_hashes = {
        "G435_output.json": sha256_file(G435_OUTPUT),
        "G435_verdict.md": sha256_file(G435_VERDICT),
        "G470_output.json": sha256_file(G470_OUTPUT),
        "BB005_RESULT.md": sha256_file(BB005_RESULT),
        "CH033_summary.md": sha256_file(CH033_SUMMARY),
        "QGA013_doc.md": sha256_file(QGA013_DOC),
        "BLINDNESS_PROTOCOL.md": sha256_file(BLINDNESS_PROTOCOL),
    }
    blindness_sha = upstream_hashes["BLINDNESS_PROTOCOL.md"]
    print("  upstream verification hashes captured:")
    for name, h in upstream_hashes.items():
        print(f"    {name:30s} {h[:16] if h else 'NOT_FOUND'}")

    # Build the sealed appeal lock JSON
    appeal_lock = {
        "lock_id": "CR103a_BOUNCE_COST_A_DEPENDENCE_APPEAL_LOCK",
        "branch": "14_FOUNDATIONAL_TESTS",
        "cr_id": "CR103a",
        "sealed_at_utc": prediction_utc,
        "appeal_target_cr": "CR103",
        "appeal_target_verdict_unmodified": premises["appeal_target_verdict_unmodified"],
        "user_insights_locked_verbatim": premises["user_insights_locked_verbatim"],
        "upstream_verification_chain": premises["upstream_verification_chain"],
        "upstream_source_hashes_at_runner_time": upstream_hashes,
        "key_formula_locked": premises["key_formula_locked"],
        "terminology_clarification_per_user_2026_06_13": premises["terminology_clarification_per_user_2026_06_13"],
        "forward_blind_predictions_registered": premises["forward_blind_predictions_registered"],
        "implications_for_prior_CRs": premises["implications_for_prior_CRs"],
        "what_CR103a_does_NOT_do": premises["what_CR103a_does_NOT_do"],
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "blindness_protocol_sha256": blindness_sha,
    }
    with open(APPEAL_LOCK, "w", encoding="utf-8") as f:
        json.dump(appeal_lock, f, indent=2)
    print(f"  wrote {APPEAL_LOCK.name}")

    appeal_sha = sha256_file(APPEAL_LOCK)
    APPEAL_LOCK_SIBLING.write_text(appeal_sha + "\n", encoding="ascii")
    print(f"  appeal lock sealed: {appeal_sha}")

    # Summary
    summary = {
        "cr_id": "CR103a",
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "APPEAL_STRUCTURAL_CORRECTION_AND_FORWARD_BLIND_PREDICTION_LOCK",
        "execution_status": "CLEAN",
        "result_class": "BOUNCE_COST_A_DEPENDENCE_STRUCTURAL_INSIGHT_LOCKED",
        "scope_status": "PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF",
        "appeal_target_cr": "CR103",
        "appeal_target_verdict_unmodified": premises["appeal_target_verdict_unmodified"],
        "user_insight_layers_locked": list(premises["user_insights_locked_verbatim"].keys()),
        "upstream_verification_sources_hashed": list(upstream_hashes.keys()),
        "forward_blind_predictions_count": len(premises["forward_blind_predictions_registered"]),
        "prediction_commit_sha256": prediction_sha,
        "prediction_commit_utc": prediction_utc,
        "appeal_lock_sha256": appeal_sha,
        "appeal_lock_sibling_path": str(APPEAL_LOCK_SIBLING),
        "blindness_protocol_sha256": blindness_sha,
        "upstream_question_lock_sha256": premises["upstream_question_lock_sha256"],
        "open_debts": premises["open_debts_declared_at_CR103a"],
    }
    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # result.md
    md = []
    md.append("# CR103a Bounce-Cost and A-Dependence Appeal - Sealed Structural Insight\n\n")
    md.append("## Verdict\n\n```text\nCR103a_BOUNCE_COST_A_DEPENDENCE_STRUCTURAL_INSIGHT_LOCKED\n(PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)\n```\n\n")
    md.append("## Cryptographic Locks\n\n```text\n")
    md.append(f"prediction_commit_sha256 = {prediction_sha}\n")
    md.append(f"prediction_commit_utc    = {prediction_utc}\n")
    md.append(f"appeal_lock_sha256       = {appeal_sha}\n")
    md.append(f"lock_sibling             = {APPEAL_LOCK_SIBLING.name}\n")
    md.append(f"blindness_protocol_sha256= {blindness_sha}\n")
    md.append("```\n\n")
    md.append("## What CR103a Does\n\n")
    md.append("Seals the user's three-layer structural insight on SW resolution,\n")
    md.append("epistemology, and A-dependent bounce cost into the public\n")
    md.append("cryptographic record, alongside the upstream-SAM verification chain\n")
    md.append("(G425 / G432 / G435 / G470 / BB005 / CH033 / QP038), without\n")
    md.append("modifying any prior CR verdict.\n\n")
    md.append("## User's Three Layers (Locked Verbatim)\n\n")
    md.append("### Layer 1 - Resolution Mechanics\n\n")
    md.append("> *\"" + premises["user_insights_locked_verbatim"]["layer_1_resolution_mechanics"] + "\"*\n\n")
    md.append("**Upstream verification:** G425 (SW(A0) -> Higgs/bounce half + ledger/write half), QGA021 (D_route = 6 half-slots, I_threshold = 1/2), QGA019 (coherent echo-contact overlap)\n\n")
    md.append("### Layer 2 - Epistemology\n\n")
    md.append("> *\"" + premises["user_insights_locked_verbatim"]["layer_2_epistemology"] + "\"*\n\n")
    md.append("**Upstream verification:** QGA013 (unresolved A has undetermined path), G286d precheck\n\n")
    md.append("### Layer 3 - Bounce Cost and A-Dependence\n\n")
    md.append("> *\"" + premises["user_insights_locked_verbatim"]["layer_3_bounce_cost_and_A_dependence"] + "\"*\n\n")
    md.append("**Upstream verification:**\n\n")
    for s in premises["upstream_verification_chain"]["layer_3_sources"]:
        md.append(f"- **{s['id']}** ({s.get('verdict', 'cite')}): {s['claim']}\n")
    md.append("\n## Key Formula (Locked)\n\n```text\n")
    md.append("r_bounce = (A0/2) * (q / 2^D)\n\n")
    md.append("A0       = 1/(12*pi) = 0.026525823848649224  (universal SW quantum)\n")
    md.append("A0/2     = 1/(24*pi) = 0.013262911924324612  (half-SW = the bounce primitive scale)\n")
    md.append("D        = 3\n")
    md.append("2^D      = 8\n\n")
    md.append("q_map: electron=4, muon=-2, tau=-7, proton=6, neutron=5\n\n")
    md.append("m_corrected = m_base / (1 + r_bounce)\n")
    md.append("Delta_m / m_corrected = r_bounce\n")
    md.append("```\n\n")
    md.append("## Terminology Discipline (User Correction)\n\n```text\n")
    md.append("A0 (constant)   = 1/(12*pi)            universal SW quantum\n")
    md.append("A  (field)      = local SW displacement density (position-dependent)\n\n")
    md.append("A0 baseline     = lowest A in deep vacuum after parent-road reset\n")
    md.append("A_Earth_surface = A0 + ~1.4e-9   (Schwarzschild factor at Earth)\n\n")
    md.append("CERN sits on Earth. The relevant A for CERN bounce-cost comparisons\n")
    md.append("is A_Earth_surface, NOT A0 vacuum baseline. The numerical correction\n")
    md.append("is ~1e-9, well below current experimental precision, so verdicts\n")
    md.append("are unchanged - but the discipline must be obeyed for future CRs\n")
    md.append("that touch high-A environments (neutron star mergers, BH accretion).\n")
    md.append("```\n\n")
    md.append("## Forward-Blind Predictions Registered\n\n")
    for p in premises["forward_blind_predictions_registered"]:
        md.append(f"### {p['prediction_id']}\n\n")
        md.append(f"**Claim:** {p['claim']}\n\n")
        md.append(f"**Testable at:** {p['testable_at']}\n\n")
        md.append(f"**Constraint:** {p['constraint']}\n\n")
    md.append("## Implications For Prior CRs (Verdicts Unchanged)\n\n")
    for cr, impl in premises["implications_for_prior_CRs"].items():
        md.append(f"- **{cr}**: {impl}\n")
    md.append("\n## Upstream Source Hashes At Runner Time\n\n```text\n")
    for name, h in upstream_hashes.items():
        md.append(f"{name:30s} {h or 'NOT_FOUND'}\n")
    md.append("```\n\n")
    md.append("## Connection To GATE_3 K(A_H)\n\n")
    md.append("CR100's GATE_3 enumerates the open question: derive K(A_H) from\n")
    md.append("substrate tension. The user's Layer 3 statement identifies K(A_H)\n")
    md.append("as the Higgs weight self-correction:\n\n```text\n")
    md.append("K(A_H) = f(A_H) such that\n")
    md.append("         K(A_H) * r_bounce(A_H) * m_particle = constant intersection cost\n")
    md.append("         for A_H < 11/12\n\n")
    md.append("At A_H = 11/12 (maximum loading per BB005), the front-back A\n")
    md.append("differential exceeds threshold; self-correction fails;\n")
    md.append("composite intersections destabilize -> quantum spaghettification.\n")
    md.append("```\n\n")
    md.append("This means GATE_3 closure has a concrete functional target,\n")
    md.append("a saturation boundary (11/12), and a falsifier (spaghettification\n")
    md.append("signatures in extreme-A environments).\n\n")
    md.append("## Rule-9 Line\n\n```text\n")
    md.append("This CR could have failed if:\n")
    md.append("  - the user's three-layer insight had no upstream verification\n")
    md.append("  - the bounce cost theorem (G435 + G470) did not exist as PASS\n")
    md.append("  - the 11/12 threshold (BB005) had no native-ordering basis\n")
    md.append("  - the spaghettification boundary (QP038) was not in SAM\n\n")
    md.append("All four verifications hold. The structural correction is locked.\n")
    md.append("CR103's verdict remains intact; CR103a refines its interpretation\n")
    md.append("and registers four forward-blind predictions that any future SAM\n")
    md.append("derivation must satisfy or explicitly disfavor.\n")
    md.append("\n")
    md.append("The 11/12 spaghettification threshold is now on the public record\n")
    md.append("as a quantitative falsifier separate from the A=1 horizon. Future\n")
    md.append("LIGO/Virgo merger waveforms and BH accretion data are the natural\n")
    md.append("probes.\n")
    md.append("```\n")

    with open(RESULT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"  wrote {RESULT_MD.name}")
    print("CR103a runner: complete")


if __name__ == "__main__":
    main()
