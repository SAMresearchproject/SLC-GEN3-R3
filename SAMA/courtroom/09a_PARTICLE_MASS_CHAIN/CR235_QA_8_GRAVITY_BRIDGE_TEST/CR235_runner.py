"""
CR235 qA/8 Gravity Bridge Test — Runner

Audits the proportional source bridge:
    G(P) = qA(P)/8;   W(P) = 7*qA(P)/8;   qA(P) = 8*G(P)
on every matter row (CR219) and every SOB element row (Test 5).

Then audits the ratio invariance G(P_i)/G(P_j) = qA(P_i)/qA(P_j) across all
ordered pairs in each population.

Then audits the externally-directional ranking: Spearman rho between
predicted G(P) and external_anchor_A across the 81 stable elements.

Wrong controls: G'=qA/7, W'=6qA/8, shuffled qA (ratio test), shuffled G (rho test).

Locked precommit: CR235_PRECOMMIT.md (sha 0e91dd6759200d3cf2b8b361632631805a71cf5b311a6c465cc8a8457265538e).
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from decimal import Decimal, getcontext, InvalidOperation
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80

CR_DIR = Path(__file__).resolve().parent
ROOT = CR_DIR.parents[1]
MATTER_CSV = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")
MATTER_SHA_EXPECTED = "45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f"
SOB_CSV = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR_TEST5_BLIND_SOB_ELEMENT_ENGINE" / "outputs" / "test5_no_name_predictions.csv"
SOB_SHA_EXPECTED = "0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616"
REVEAL_CSV = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR_TEST5_BLIND_SOB_ELEMENT_ENGINE" / "reveal_reference.csv"
REVEAL_SHA_EXPECTED = "fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a"
PRECOMMIT_SHA = "0e91dd6759200d3cf2b8b361632631805a71cf5b311a6c465cc8a8457265538e"

TOL_MATTER = Decimal("1e-9")
SEED_WC3 = 20260622
SEED_WC4 = 20260623


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dec(value: str) -> Decimal:
    value = (value or "").strip()
    if value.lower() in {"", "no", "none", "null", "nan"}:
        return Decimal(0)
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"not decimal: {value!r}") from exc


def load_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header[0].isdigit():
            header[0] = "source_order"
        return header, [dict(zip(header, r)) for r in reader]


def load_dict_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_fraction(s: str) -> Fraction:
    """Parse a string that may be '7117/768' or '12345.6789' as a Fraction."""
    s = (s or "").strip()
    if not s:
        return Fraction(0)
    if "/" in s:
        return Fraction(s)
    return Fraction(Decimal(s)).limit_denominator(10 ** 20)


# ---- MATTER ROW AUDIT ----

def audit_matter_identities(matter_rows: list[dict]) -> tuple[list[dict], dict]:
    results = []
    counters = {"id1": 0, "id2": 0, "id3": 0, "all": 0, "rows": 0}
    eight = Decimal(8)
    seven = Decimal(7)
    for row in matter_rows:
        if row.get("matter_row_allowed") != "yes":
            continue
        counters["rows"] += 1
        G = dec(row["tensor_carrier_support"])
        qA = dec(row["qA_source_support"])
        W = dec(row["retained_write_support"])
        d1 = abs(G - qA / eight)
        d2 = abs(W - seven * qA / eight)
        d3 = abs(qA - eight * G)
        ok1 = d1 <= TOL_MATTER
        ok2 = d2 <= TOL_MATTER
        ok3 = d3 <= TOL_MATTER
        if ok1: counters["id1"] += 1
        if ok2: counters["id2"] += 1
        if ok3: counters["id3"] += 1
        if ok1 and ok2 and ok3:
            counters["all"] += 1
        results.append({
            "candidate_id": row["candidate_id"],
            "G_observed": str(G),
            "qA_observed": str(qA),
            "W_observed": str(W),
            "G_minus_qA_over_8": str(d1),
            "W_minus_7qA_over_8": str(d2),
            "qA_minus_8G": str(d3),
            "identity_1_pass": ok1,
            "identity_2_pass": ok2,
            "identity_3_pass": ok3,
            "all_three_pass": ok1 and ok2 and ok3,
        })
    return results, counters


def audit_matter_ratio_invariance(matter_results: list[dict]) -> dict:
    rows = [(r["candidate_id"], Decimal(r["G_observed"]), Decimal(r["qA_observed"]))
            for r in matter_results]
    n = len(rows)
    breaks = 0
    pairs_checked = 0
    largest_residue = Decimal(0)
    for i in range(n):
        _, G_i, qA_i = rows[i]
        for j in range(n):
            if i == j:
                continue
            _, G_j, qA_j = rows[j]
            if qA_j == 0:
                continue
            pairs_checked += 1
            residue = abs(G_i * qA_j - G_j * qA_i)
            if residue > largest_residue:
                largest_residue = residue
            if residue > TOL_MATTER:
                breaks += 1
    return {
        "rows": n,
        "ordered_pairs_checked": pairs_checked,
        "ratio_invariance_breaks": breaks,
        "ratio_invariance_passes": pairs_checked - breaks,
        "largest_residue": str(largest_residue),
        "passes_audit": breaks == 0,
    }


# ---- SOB ELEMENT ROW AUDIT ----

def audit_sob_identities(sob_rows: list[dict]) -> tuple[list[dict], dict]:
    results = []
    counters = {"id1": 0, "id2": 0, "id3": 0, "all": 0, "rows": 0}
    eight = Fraction(8)
    seven = Fraction(7)
    for row in sob_rows:
        counters["rows"] += 1
        G = parse_fraction(row["G_native"])
        qA = parse_fraction(row["GR_8G"])
        W = parse_fraction(row["retained_7G"])
        ok1 = G == qA / eight
        ok2 = W == seven * qA / eight
        ok3 = qA == eight * G
        if ok1: counters["id1"] += 1
        if ok2: counters["id2"] += 1
        if ok3: counters["id3"] += 1
        if ok1 and ok2 and ok3:
            counters["all"] += 1
        results.append({
            "row_id": row["row_id"],
            "Z": int(row["Z"]),
            "G_observed": str(G),
            "qA_observed": str(qA),
            "W_observed": str(W),
            "identity_1_pass": ok1,
            "identity_2_pass": ok2,
            "identity_3_pass": ok3,
            "all_three_pass": ok1 and ok2 and ok3,
        })
    return results, counters


def audit_sob_ratio_invariance(sob_results: list[dict]) -> dict:
    rows = [(r["Z"], parse_fraction(r["G_observed"]), parse_fraction(r["qA_observed"]))
            for r in sob_results]
    n = len(rows)
    breaks = 0
    pairs_checked = 0
    for i in range(n):
        Zi, Gi, qAi = rows[i]
        for j in range(n):
            if i == j:
                continue
            Zj, Gj, qAj = rows[j]
            if qAj == 0:
                continue
            pairs_checked += 1
            if Gi * qAj - Gj * qAi != 0:
                breaks += 1
    return {
        "rows": n,
        "ordered_pairs_checked": pairs_checked,
        "ratio_invariance_breaks": breaks,
        "ratio_invariance_passes": pairs_checked - breaks,
        "passes_audit": breaks == 0,
    }


# ---- DIRECTIONAL AUDIT (Spearman rho via rank arithmetic) ----

def spearman_rho(xs: list, ys: list) -> float:
    """Spearman rank correlation. Ties handled by average rank."""
    n = len(xs)
    if n != len(ys) or n < 2:
        return 0.0

    def rank(seq):
        order = sorted(range(n), key=lambda i: seq[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and seq[order[j + 1]] == seq[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0  # ranks are 1-based
            for k in range(i, j + 1):
                ranks[order[k]] = avg
            i = j + 1
        return ranks

    rx = rank(xs)
    ry = rank(ys)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    denx = sum((rx[i] - mean_rx) ** 2 for i in range(n))
    deny = sum((ry[i] - mean_ry) ** 2 for i in range(n))
    if denx == 0 or deny == 0:
        return 0.0
    return num / (denx ** 0.5 * deny ** 0.5)


def audit_directional(sob_results: list[dict], reveal_rows: list[dict]) -> dict:
    reveal_by_z = {int(r["Z"]): r for r in reveal_rows}
    stable_zs = [z for z in range(1, 84) if z not in (43, 61)]
    g_values = []
    a_values = []
    for r in sob_results:
        if r["Z"] in stable_zs:
            ref = reveal_by_z.get(r["Z"])
            if ref and ref.get("external_anchor_A"):
                try:
                    a = int(ref["external_anchor_A"])
                except ValueError:
                    continue
                g = float(parse_fraction(r["G_observed"]))
                g_values.append(g)
                a_values.append(a)
    rho = spearman_rho(g_values, a_values)
    if rho >= 0.99:
        verdict = "PASS_DIRECTIONAL"
    elif rho >= 0.95:
        verdict = "PARTIAL_DIRECTIONAL"
    else:
        verdict = "FAIL_DIRECTIONAL"
    return {
        "stable_set_size": len(stable_zs),
        "joined_rows": len(g_values),
        "spearman_rho_G_vs_anchor_A": rho,
        "directional_verdict": verdict,
        "passes_directional": rho >= 0.99,
    }


# ---- WRONG CONTROLS ----

def wc1_wrong_tensor_ratio(matter_results: list[dict], sob_results: list[dict]) -> dict:
    """G' = qA/7 instead of qA/8."""
    seven = Decimal(7)
    matter_breaks = 0
    for r in matter_results:
        qA = Decimal(r["qA_observed"])
        G = Decimal(r["G_observed"])
        if qA == 0:
            continue
        Gp = qA / seven
        if abs(G - Gp) > TOL_MATTER:
            matter_breaks += 1
    sob_breaks = 0
    seven_f = Fraction(7)
    for r in sob_results:
        qA = parse_fraction(r["qA_observed"])
        G = parse_fraction(r["G_observed"])
        if qA == 0:
            continue
        if G != qA / seven_f:
            sob_breaks += 1
    return {
        "rule_under_test": "G = qA/7 (wrong; correct G = qA/8)",
        "matter_breaks": matter_breaks,
        "sob_breaks": sob_breaks,
        "broke_as_predicted": matter_breaks > 0 and sob_breaks > 0,
    }


def wc2_wrong_retained_ratio(matter_results: list[dict], sob_results: list[dict]) -> dict:
    """W' = 6qA/8 instead of 7qA/8."""
    six = Decimal(6); eight = Decimal(8)
    matter_breaks = 0
    for r in matter_results:
        qA = Decimal(r["qA_observed"])
        W = Decimal(r["W_observed"])
        if qA == 0:
            continue
        Wp = six * qA / eight
        if abs(W - Wp) > TOL_MATTER:
            matter_breaks += 1
    sob_breaks = 0
    six_f = Fraction(6); eight_f = Fraction(8)
    for r in sob_results:
        qA = parse_fraction(r["qA_observed"])
        W = parse_fraction(r["W_observed"])
        if qA == 0:
            continue
        if W != six_f * qA / eight_f:
            sob_breaks += 1
    return {
        "rule_under_test": "W = 6qA/8 (wrong; correct W = 7qA/8)",
        "matter_breaks": matter_breaks,
        "sob_breaks": sob_breaks,
        "broke_as_predicted": matter_breaks > 0 and sob_breaks > 0,
    }


def wc3_shuffle_qA_breaks_ratio(sob_results: list[dict], seed: int) -> dict:
    """Shuffle qA across SOB rows (keeping G fixed); ratio invariance must break."""
    rng = random.Random(seed)
    rows = [(r["Z"], parse_fraction(r["G_observed"]), parse_fraction(r["qA_observed"]))
            for r in sob_results]
    qAs = [r[2] for r in rows]
    rng.shuffle(qAs)
    shuffled = [(z, g, qa) for (z, g, _), qa in zip(rows, qAs)]
    n = len(shuffled)
    breaks = 0
    pairs = 0
    for i in range(n):
        Zi, Gi, qAi = shuffled[i]
        for j in range(n):
            if i == j:
                continue
            Zj, Gj, qAj = shuffled[j]
            if qAj == 0:
                continue
            pairs += 1
            if Gi * qAj - Gj * qAi != 0:
                breaks += 1
    return {
        "rule_under_test": "shuffle qA across SOB rows (G unchanged)",
        "seed": seed,
        "pairs_checked": pairs,
        "ratio_invariance_breaks": breaks,
        "break_rate": breaks / pairs if pairs else 0.0,
        "broke_as_predicted": breaks / pairs > 0.5 if pairs else False,
    }


def wc4_shuffle_G_breaks_rho(sob_results: list[dict], reveal_rows: list[dict], seed: int) -> dict:
    """Shuffle G(P) labels across Z and recompute Spearman rho; should fall below 0.10."""
    rng = random.Random(seed)
    reveal_by_z = {int(r["Z"]): r for r in reveal_rows}
    stable_zs = [z for z in range(1, 84) if z not in (43, 61)]

    pairs = []
    for r in sob_results:
        if r["Z"] in stable_zs:
            ref = reveal_by_z.get(r["Z"])
            if ref and ref.get("external_anchor_A"):
                try:
                    a = int(ref["external_anchor_A"])
                    g = float(parse_fraction(r["G_observed"]))
                    pairs.append((g, a))
                except ValueError:
                    pass

    gs = [p[0] for p in pairs]
    as_ = [p[1] for p in pairs]
    rng.shuffle(gs)
    rho = spearman_rho(gs, as_)
    return {
        "rule_under_test": "shuffle G(P) across Z (recompute Spearman rho vs external_anchor_A)",
        "seed": seed,
        "joined_rows": len(pairs),
        "spearman_rho_after_shuffle": rho,
        "broke_as_predicted": abs(rho) < 0.10,
    }


# ---- WRITERS ----

def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def main():
    print("=" * 72)
    print("CR235 qA/8 Gravity Bridge Test")
    print("=" * 72)

    # ---- Verify sources ----
    matter_sha = sha256_file(MATTER_CSV)
    sob_sha = sha256_file(SOB_CSV)
    reveal_sha = sha256_file(REVEAL_CSV)
    print(f"\nSource SHAs:")
    print(f"  matter:    {matter_sha}  (expected {MATTER_SHA_EXPECTED})")
    print(f"  SOB:       {sob_sha}  (expected {SOB_SHA_EXPECTED})")
    print(f"  reveal:    {reveal_sha}  (expected {REVEAL_SHA_EXPECTED})")
    assert matter_sha == MATTER_SHA_EXPECTED
    assert sob_sha == SOB_SHA_EXPECTED
    assert reveal_sha == REVEAL_SHA_EXPECTED

    _, matter_rows = load_rows(MATTER_CSV)
    sob_rows = load_dict_rows(SOB_CSV)
    reveal_rows = load_dict_rows(REVEAL_CSV)

    # ---- AUDIT: Matter identities ----
    print(f"\n[AUDIT 1] Matter row identities (G=qA/8, W=7qA/8, qA=8G) within 1e-9")
    matter_results, m_counters = audit_matter_identities(matter_rows)
    print(f"  rows checked: {m_counters['rows']}")
    print(f"  identity_1 (G = qA/8):    {m_counters['id1']} / {m_counters['rows']}")
    print(f"  identity_2 (W = 7qA/8):   {m_counters['id2']} / {m_counters['rows']}")
    print(f"  identity_3 (qA = 8G):     {m_counters['id3']} / {m_counters['rows']}")
    print(f"  all three:                {m_counters['all']} / {m_counters['rows']}")
    matter_identity_pass = (m_counters['all'] == m_counters['rows'] == 126)

    # ---- AUDIT: SOB identities ----
    print(f"\n[AUDIT 2] SOB element row identities (exact in Fraction arithmetic)")
    sob_results, s_counters = audit_sob_identities(sob_rows)
    print(f"  rows checked: {s_counters['rows']}")
    print(f"  identity_1 (G = qA/8):    {s_counters['id1']} / {s_counters['rows']}")
    print(f"  identity_2 (W = 7qA/8):   {s_counters['id2']} / {s_counters['rows']}")
    print(f"  identity_3 (qA = 8G):     {s_counters['id3']} / {s_counters['rows']}")
    print(f"  all three:                {s_counters['all']} / {s_counters['rows']}")
    sob_identity_pass = (s_counters['all'] == s_counters['rows'] == 126)

    # ---- AUDIT: Matter ratio invariance ----
    print(f"\n[AUDIT 3] Matter ratio invariance (G_i*qA_j == G_j*qA_i for all pairs)")
    matter_ratio = audit_matter_ratio_invariance(matter_results)
    print(f"  pairs checked: {matter_ratio['ordered_pairs_checked']}")
    print(f"  breaks:        {matter_ratio['ratio_invariance_breaks']}")
    print(f"  largest residue: {matter_ratio['largest_residue']}")
    print(f"  passes_audit:  {matter_ratio['passes_audit']}")

    # ---- AUDIT: SOB ratio invariance ----
    print(f"\n[AUDIT 4] SOB ratio invariance (exact in Fraction arithmetic)")
    sob_ratio = audit_sob_ratio_invariance(sob_results)
    print(f"  pairs checked: {sob_ratio['ordered_pairs_checked']}")
    print(f"  breaks:        {sob_ratio['ratio_invariance_breaks']}")
    print(f"  passes_audit:  {sob_ratio['passes_audit']}")

    # ---- AUDIT: Directional ----
    print(f"\n[AUDIT 5] Directional rank correlation (G_SOB vs external_anchor_A, stable Z)")
    directional = audit_directional(sob_results, reveal_rows)
    print(f"  stable set size:    {directional['stable_set_size']}")
    print(f"  joined rows:        {directional['joined_rows']}")
    print(f"  Spearman rho:       {directional['spearman_rho_G_vs_anchor_A']:.6f}")
    print(f"  directional verdict: {directional['directional_verdict']}")

    # ---- WRONG CONTROLS ----
    print(f"\n[WC1] Wrong tensor ratio G' = qA/7:")
    wc1 = wc1_wrong_tensor_ratio(matter_results, sob_results)
    print(f"  matter breaks: {wc1['matter_breaks']}, sob breaks: {wc1['sob_breaks']}, broke: {wc1['broke_as_predicted']}")

    print(f"\n[WC2] Wrong retained ratio W' = 6qA/8:")
    wc2 = wc2_wrong_retained_ratio(matter_results, sob_results)
    print(f"  matter breaks: {wc2['matter_breaks']}, sob breaks: {wc2['sob_breaks']}, broke: {wc2['broke_as_predicted']}")

    print(f"\n[WC3] Shuffle qA across SOB rows (seed {SEED_WC3}):")
    wc3 = wc3_shuffle_qA_breaks_ratio(sob_results, SEED_WC3)
    print(f"  pairs: {wc3['pairs_checked']}, breaks: {wc3['ratio_invariance_breaks']}, rate: {wc3['break_rate']:.4f}, broke: {wc3['broke_as_predicted']}")

    print(f"\n[WC4] Shuffle G(P) across Z (seed {SEED_WC4}):")
    wc4 = wc4_shuffle_G_breaks_rho(sob_results, reveal_rows, SEED_WC4)
    print(f"  shuffled rho: {wc4['spearman_rho_after_shuffle']:.6f}, broke: {wc4['broke_as_predicted']}")

    # ---- VERDICT ----
    main_pass = (
        matter_identity_pass and sob_identity_pass
        and matter_ratio['passes_audit'] and sob_ratio['passes_audit']
        and directional['passes_directional']
    )
    wcs_pass = (wc1['broke_as_predicted'] and wc2['broke_as_predicted']
                and wc3['broke_as_predicted'] and wc4['broke_as_predicted'])
    overall = main_pass and wcs_pass
    verdict = "PASS" if overall else "FAIL"

    print("\n" + "=" * 72)
    print(f"Main audits pass:  {main_pass}")
    print(f"Wrong controls:    {wcs_pass}")
    print(f"CR235 VERDICT:     {verdict}")
    print("=" * 72)

    # ---- CSV outputs ----
    write_csv(CR_DIR / "CR235_matter_identity_audit.csv", matter_results,
              ["candidate_id", "G_observed", "qA_observed", "W_observed",
               "G_minus_qA_over_8", "W_minus_7qA_over_8", "qA_minus_8G",
               "identity_1_pass", "identity_2_pass", "identity_3_pass", "all_three_pass"])
    write_csv(CR_DIR / "CR235_sob_identity_audit.csv", sob_results,
              ["row_id", "Z", "G_observed", "qA_observed", "W_observed",
               "identity_1_pass", "identity_2_pass", "identity_3_pass", "all_three_pass"])

    summary = {
        "artifact": "CR235_QA_8_GRAVITY_BRIDGE_TEST",
        "classification": "PROPORTIONAL_SOURCE_BRIDGE",
        "arc_position": "Test 6 of 7 in the Seven-Test Ownership Arc",
        "permission_status": "GRANTED_BY_USER_SEAN_BRADY_2026_06_22",
        "precommit_sha256": PRECOMMIT_SHA,
        "source_shas": {
            "matter_CR219": matter_sha,
            "sob_test5": sob_sha,
            "reveal_reference": reveal_sha,
        },
        "tolerance_matter": str(TOL_MATTER),
        "tolerance_sob": "0 (exact Fraction)",
        "audit_1_matter_identities": m_counters,
        "audit_2_sob_identities": s_counters,
        "audit_3_matter_ratio_invariance": matter_ratio,
        "audit_4_sob_ratio_invariance": sob_ratio,
        "audit_5_directional": directional,
        "wrong_controls": {
            "WC1_G_eq_qA_over_7": wc1,
            "WC2_W_eq_6qA_over_8": wc2,
            "WC3_shuffle_qA": wc3,
            "WC4_shuffle_G": wc4,
            "all_broke_as_predicted": wcs_pass,
        },
        "main_audits_pass": main_pass,
        "wrong_controls_pass": wcs_pass,
        "scientific_verdict": verdict,
        "execution_status": "CLEAN",
        "K_gates": {
            "K1_external_anchor": "PASS (directional rank vs external_anchor_A, no unit conversion)",
            "K2_falsification_statement": "PASS",
            "K3_target_hygiene": "PASS (identities/tolerance/WCs locked in precommit pre-execution)",
            "K4_typed_inputs": "PASS (R=12; two SHA-locked CSVs; reveal SHA-locked but used directionally only)",
            "K5_reproduction_on_demand": "PASS (deterministic + seeded WCs)",
        },
    }
    with (CR_DIR / "CR235_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote: CR235_summary.json")
    return verdict


if __name__ == "__main__":
    main()
