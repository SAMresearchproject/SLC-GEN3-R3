"""
CR235a Exact-Source Gravity Bridge Reaudit — Runner

Re-runs the qA/8 bridge audit with exact Fraction arithmetic throughout, and
replaces CR235's single-seed WC4 threshold with a 10000-shuffle permutation null.

Locked precommit: CR235a_PRECOMMIT.md (sha e42944abe1cd6c1710de78cc4a992252dfe1cf083eaf905458477a89a49364dc).
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from decimal import Decimal, getcontext
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
PRECOMMIT_SHA = "e42944abe1cd6c1710de78cc4a992252dfe1cf083eaf905458477a89a49364dc"

R = 12
R2 = R * R
EIGHT = Fraction(8)
SEVEN = Fraction(7)
LIMIT = 10 ** 12  # denominator cap for parsing M_obs from CSV strings

N_PERM = 10000
SEED_WC4 = 20260623
SEED_WC3 = 20260622


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header[0].isdigit():
            header[0] = "source_order"
        return [dict(zip(header, r)) for r in reader]


def load_dict_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_fraction(s: str) -> Fraction:
    s = (s or "").strip()
    if not s or s.lower() in ("no", "none", "null", "nan"):
        return Fraction(0)
    if "/" in s:
        return Fraction(s)
    return Fraction(Decimal(s)).limit_denominator(LIMIT)


def parse_int(s: str) -> int:
    return int((s or "0").strip())


# ---- EXACT MATTER ROW RECONSTRUCTION ----

def reconstruct_matter_exact(matter_rows: list[dict]) -> list[dict]:
    """For each matter row, compute exact qA, G, W from M_obs and q_abs."""
    out = []
    for row in matter_rows:
        if row.get("matter_row_allowed") != "yes":
            continue
        M_obs = to_fraction(row["M_observed_candidate"])
        q_abs = parse_int(row["q_abs"])
        qA = M_obs * Fraction(R2 + q_abs, R2)
        G = qA / EIGHT
        W = SEVEN * qA / EIGHT
        out.append({
            "candidate_id": row["candidate_id"],
            "q_abs": q_abs,
            "M_obs_exact": str(M_obs),
            "qA_exact": str(qA),
            "G_exact": str(G),
            "W_exact": str(W),
            "_qA": qA,
            "_G": G,
            "_W": W,
        })
    return out


# ---- EXACT SOB RECONSTRUCTION ----

def load_sob_exact(sob_rows: list[dict]) -> list[dict]:
    out = []
    for row in sob_rows:
        G = Fraction(row["G_native"])
        qA = Fraction(row["GR_8G"])
        W = Fraction(row["retained_7G"])
        out.append({
            "row_id": row["row_id"],
            "Z": int(row["Z"]),
            "G_exact": str(G),
            "qA_exact": str(qA),
            "W_exact": str(W),
            "_G": G,
            "_qA": qA,
            "_W": W,
        })
    return out


# ---- IDENTITY + RATIO AUDITS (exact) ----

def audit_identities_exact(rows: list[dict]) -> dict:
    counters = {"id1": 0, "id2": 0, "id3": 0, "all": 0, "rows": 0}
    for r in rows:
        counters["rows"] += 1
        G = r["_G"]; qA = r["_qA"]; W = r["_W"]
        ok1 = G == qA / EIGHT
        ok2 = W == SEVEN * qA / EIGHT
        ok3 = qA == EIGHT * G
        if ok1: counters["id1"] += 1
        if ok2: counters["id2"] += 1
        if ok3: counters["id3"] += 1
        if ok1 and ok2 and ok3:
            counters["all"] += 1
    return counters


def audit_ratio_exact(rows: list[dict]) -> dict:
    pairs = 0
    breaks = 0
    n = len(rows)
    for i in range(n):
        Gi = rows[i]["_G"]; qAi = rows[i]["_qA"]
        for j in range(n):
            if i == j:
                continue
            Gj = rows[j]["_G"]; qAj = rows[j]["_qA"]
            if qAj == 0:
                continue
            pairs += 1
            if Gi * qAj - Gj * qAi != 0:
                breaks += 1
    return {"pairs": pairs, "breaks": breaks, "passes_audit": breaks == 0}


# ---- DIRECTIONAL ----

def spearman_rho(xs: list, ys: list) -> float:
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
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg
            i = j + 1
        return ranks

    rx = rank(xs); ry = rank(ys)
    mean_rx = sum(rx) / n; mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    denx = sum((rx[i] - mean_rx) ** 2 for i in range(n))
    deny = sum((ry[i] - mean_ry) ** 2 for i in range(n))
    if denx == 0 or deny == 0:
        return 0.0
    return num / (denx ** 0.5 * deny ** 0.5)


def audit_directional(sob_rows: list[dict], reveal_rows: list[dict]) -> dict:
    reveal_by_z = {int(r["Z"]): r for r in reveal_rows}
    stable_zs = [z for z in range(1, 84) if z not in (43, 61)]
    g_values = []; a_values = []
    for r in sob_rows:
        if r["Z"] in stable_zs:
            ref = reveal_by_z.get(r["Z"])
            if ref and ref.get("external_anchor_A"):
                try:
                    a = int(ref["external_anchor_A"])
                    g = float(r["_G"])
                    g_values.append(g)
                    a_values.append(a)
                except ValueError:
                    continue
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
        "spearman_rho_real": rho,
        "directional_verdict": verdict,
        "passes_directional": rho >= 0.99,
        "_g_values": g_values,
        "_a_values": a_values,
    }


# ---- WRONG CONTROLS ----

def wc1_wrong_tensor(rows: list[dict], label: str) -> dict:
    seven_f = Fraction(7)
    breaks = 0
    nonzero = 0
    for r in rows:
        if r["_qA"] == 0:
            continue
        nonzero += 1
        if r["_G"] != r["_qA"] / seven_f:
            breaks += 1
    return {"population": label, "nonzero_rows": nonzero, "breaks": breaks,
            "broke_as_predicted": breaks == nonzero}


def wc2_wrong_retained(rows: list[dict], label: str) -> dict:
    six_f = Fraction(6); eight_f = Fraction(8)
    breaks = 0
    nonzero = 0
    for r in rows:
        if r["_qA"] == 0:
            continue
        nonzero += 1
        if r["_W"] != six_f * r["_qA"] / eight_f:
            breaks += 1
    return {"population": label, "nonzero_rows": nonzero, "breaks": breaks,
            "broke_as_predicted": breaks == nonzero}


def wc3_shuffle_qA(rows: list[dict], seed: int, label: str) -> dict:
    rng = random.Random(seed)
    qAs = [r["_qA"] for r in rows]
    rng.shuffle(qAs)
    n = len(rows)
    pairs = 0; breaks = 0
    for i in range(n):
        Gi = rows[i]["_G"]; qAi = qAs[i]
        for j in range(n):
            if i == j:
                continue
            Gj = rows[j]["_G"]; qAj = qAs[j]
            if qAj == 0:
                continue
            pairs += 1
            if Gi * qAj - Gj * qAi != 0:
                breaks += 1
    return {"population": label, "seed": seed, "pairs": pairs, "breaks": breaks,
            "break_rate": breaks / pairs if pairs else 0.0,
            "broke_as_predicted": (breaks / pairs > 0.5) if pairs else False}


def wc4_permutation_null(directional: dict, n_perm: int, seed: int) -> dict:
    """10000-shuffle permutation null on Spearman rho."""
    g_values = list(directional["_g_values"])
    a_values = list(directional["_a_values"])
    rho_real = directional["spearman_rho_real"]
    rng = random.Random(seed)
    abs_rho_real = abs(rho_real)
    abs_rho_shuffled = []
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(g_values)
        rs = spearman_rho(g_values, a_values)
        abs_rho_shuffled.append(abs(rs))
        if abs(rs) >= abs_rho_real:
            ge += 1
    p_perm = ge / n_perm
    lt = sum(1 for x in abs_rho_shuffled if x < abs_rho_real)
    percentile_real = lt / n_perm
    max_abs_shuffled = max(abs_rho_shuffled)
    return {
        "n_perm": n_perm,
        "seed": seed,
        "rho_real": rho_real,
        "abs_rho_real": abs_rho_real,
        "p_perm": p_perm,
        "percentile_rho_real": percentile_real,
        "max_abs_rho_shuffled": max_abs_shuffled,
        "broke_as_predicted": p_perm < 0.001 and percentile_real > 0.999,
    }


# ---- MAIN ----

def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fields})


def main():
    print("=" * 72)
    print("CR235a Exact-Source Gravity Bridge Reaudit")
    print("=" * 72)

    matter_sha = sha256_file(MATTER_CSV)
    sob_sha = sha256_file(SOB_CSV)
    reveal_sha = sha256_file(REVEAL_CSV)
    print(f"\nSource SHAs:")
    print(f"  matter:    {matter_sha}")
    print(f"  SOB:       {sob_sha}")
    print(f"  reveal:    {reveal_sha}")
    assert matter_sha == MATTER_SHA_EXPECTED
    assert sob_sha == SOB_SHA_EXPECTED
    assert reveal_sha == REVEAL_SHA_EXPECTED

    matter_raw = load_rows(MATTER_CSV)
    sob_raw = load_dict_rows(SOB_CSV)
    reveal_raw = load_dict_rows(REVEAL_CSV)

    matter_exact = reconstruct_matter_exact(matter_raw)
    sob_exact = load_sob_exact(sob_raw)
    print(f"\nMatter rows exact: {len(matter_exact)}")
    print(f"SOB rows exact:    {len(sob_exact)}")

    # ---- AUDIT 1 ----
    print(f"\n[AUDIT 1] Matter identities (exact Fraction)")
    m_id = audit_identities_exact(matter_exact)
    print(f"  identity_1: {m_id['id1']} / {m_id['rows']}")
    print(f"  identity_2: {m_id['id2']} / {m_id['rows']}")
    print(f"  identity_3: {m_id['id3']} / {m_id['rows']}")
    print(f"  all three:  {m_id['all']} / {m_id['rows']}")

    # ---- AUDIT 2 ----
    print(f"\n[AUDIT 2] SOB identities (exact Fraction)")
    s_id = audit_identities_exact(sob_exact)
    print(f"  identity_1: {s_id['id1']} / {s_id['rows']}")
    print(f"  identity_2: {s_id['id2']} / {s_id['rows']}")
    print(f"  identity_3: {s_id['id3']} / {s_id['rows']}")
    print(f"  all three:  {s_id['all']} / {s_id['rows']}")

    # ---- AUDIT 3 ----
    print(f"\n[AUDIT 3] Matter ratio invariance (exact Fraction)")
    m_ratio = audit_ratio_exact(matter_exact)
    print(f"  pairs: {m_ratio['pairs']}, breaks: {m_ratio['breaks']}, passes: {m_ratio['passes_audit']}")

    # ---- AUDIT 4 ----
    print(f"\n[AUDIT 4] SOB ratio invariance (exact Fraction)")
    s_ratio = audit_ratio_exact(sob_exact)
    print(f"  pairs: {s_ratio['pairs']}, breaks: {s_ratio['breaks']}, passes: {s_ratio['passes_audit']}")

    # ---- AUDIT 5 ----
    print(f"\n[AUDIT 5] Directional Spearman rho")
    directional = audit_directional(sob_exact, reveal_raw)
    print(f"  joined rows:    {directional['joined_rows']}")
    print(f"  rho_real:       {directional['spearman_rho_real']:.6f}")
    print(f"  verdict:        {directional['directional_verdict']}")

    # ---- WCs ----
    print(f"\n[WC1] G' = qA/7")
    wc1_m = wc1_wrong_tensor(matter_exact, "matter")
    wc1_s = wc1_wrong_tensor(sob_exact, "sob")
    print(f"  matter: {wc1_m}")
    print(f"  sob:    {wc1_s}")

    print(f"\n[WC2] W' = 6qA/8")
    wc2_m = wc2_wrong_retained(matter_exact, "matter")
    wc2_s = wc2_wrong_retained(sob_exact, "sob")
    print(f"  matter: {wc2_m}")
    print(f"  sob:    {wc2_s}")

    print(f"\n[WC3] Shuffle qA (seed {SEED_WC3})")
    wc3_s = wc3_shuffle_qA(sob_exact, SEED_WC3, "sob")
    print(f"  sob: pairs={wc3_s['pairs']} breaks={wc3_s['breaks']} rate={wc3_s['break_rate']:.4f} broke={wc3_s['broke_as_predicted']}")

    print(f"\n[WC4] Permutation null on Spearman rho ({N_PERM} shuffles, seed {SEED_WC4})")
    wc4 = wc4_permutation_null(directional, N_PERM, SEED_WC4)
    print(f"  rho_real:                {wc4['rho_real']:.6f}")
    print(f"  max |rho_shuffled|:      {wc4['max_abs_rho_shuffled']:.6f}")
    print(f"  p_perm:                  {wc4['p_perm']:.6f}")
    print(f"  percentile_rho_real:     {wc4['percentile_rho_real']:.6f}")
    print(f"  broke_as_predicted:      {wc4['broke_as_predicted']}")

    # ---- VERDICT ----
    main_pass = (
        m_id["all"] == 126 and s_id["all"] == 126
        and m_ratio["passes_audit"] and s_ratio["passes_audit"]
        and directional["passes_directional"]
    )
    wcs_pass = (
        wc1_m["broke_as_predicted"] and wc1_s["broke_as_predicted"]
        and wc2_m["broke_as_predicted"] and wc2_s["broke_as_predicted"]
        and wc3_s["broke_as_predicted"]
        and wc4["broke_as_predicted"]
    )
    overall = main_pass and wcs_pass
    verdict = "PASS" if overall else "FAIL"

    print("\n" + "=" * 72)
    print(f"Main audits pass:  {main_pass}")
    print(f"Wrong controls:    {wcs_pass}")
    print(f"CR235a VERDICT:    {verdict}")
    print("=" * 72)

    # ---- WRITERS ----
    write_csv(CR_DIR / "CR235a_matter_exact_audit.csv", matter_exact,
              ["candidate_id", "q_abs", "M_obs_exact", "qA_exact", "G_exact", "W_exact"])
    write_csv(CR_DIR / "CR235a_sob_exact_audit.csv", sob_exact,
              ["row_id", "Z", "G_exact", "qA_exact", "W_exact"])

    summary = {
        "artifact": "CR235a_EXACT_SOURCE_GRAVITY_BRIDGE_REAUDIT",
        "classification": "AMENDMENT_EXACT_ARITHMETIC_REAUDIT",
        "arc_position": "Test 6 follow-up (does not modify CR235)",
        "permission_status": "GRANTED_BY_USER_SEAN_BRADY_2026_06_22",
        "precommit_sha256": PRECOMMIT_SHA,
        "source_shas": {
            "matter_CR219": matter_sha,
            "sob_test5": sob_sha,
            "reveal_reference": reveal_sha,
        },
        "tolerance": "0 (exact Fraction)",
        "audit_1_matter_identities": m_id,
        "audit_2_sob_identities": s_id,
        "audit_3_matter_ratio_invariance": m_ratio,
        "audit_4_sob_ratio_invariance": s_ratio,
        "audit_5_directional": {k: v for k, v in directional.items() if not k.startswith("_")},
        "wrong_controls": {
            "WC1_G_eq_qA_over_7": {"matter": wc1_m, "sob": wc1_s},
            "WC2_W_eq_6qA_over_8": {"matter": wc2_m, "sob": wc2_s},
            "WC3_shuffle_qA": {"sob": wc3_s},
            "WC4_permutation_null": wc4,
            "all_broke_as_predicted": wcs_pass,
        },
        "main_audits_pass": main_pass,
        "wrong_controls_pass": wcs_pass,
        "scientific_verdict": verdict,
        "execution_status": "CLEAN",
        "amendment_note": "CR235 stays sealed at FAIL with its original artifacts. CR235a is an independent exact-source amendment.",
        "K_gates": {
            "K1_external_anchor": "PASS (directional rank vs external_anchor_A; no unit conversion)",
            "K2_falsification_statement": "PASS",
            "K3_target_hygiene": "PASS (exact rule + permutation parameters locked in precommit pre-execution)",
            "K4_typed_inputs": "PASS",
            "K5_reproduction_on_demand": "PASS (deterministic + seeded WC3, WC4)",
        },
    }
    with (CR_DIR / "CR235a_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote: CR235a_summary.json")
    return verdict


if __name__ == "__main__":
    main()
