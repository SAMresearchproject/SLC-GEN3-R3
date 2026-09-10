"""
CR253 — Particle Promoter (80-Row Stable Matter Set).

Applies the QP098/QP106 stability filter to the corrected 299-row
QP093A catalog under CR-class hostile-environment discipline.

precommit  : a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461
catalog    : 33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c
"""

import csv
import hashlib
import itertools
import json
import os
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR253_PRECOMMIT.md")
PRECOMMIT_HASH = "a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461"
CATALOG_PATH = os.path.join(HERE, "CR253_input_catalog_299.csv")
CATALOG_HASH = "33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c"

# Locked promoter parameters
H_ALLOWED = {0, 1}
Q_ALLOWED = {0, 1, 2, 3, 4, 6, 8, 9, 12}
B_ALLOWED = {"stable_matter_rows", "antimatter_conjugate_rows"}

# T13 tensor lanes (CR238)
T13_VALUES = [1, 1, 2, 3, 4, 6, 8, 8, 9, 9, 12, 18, 81]
T13_DISTINCT = sorted(set(T13_VALUES))

# Expected outputs (locked in precommit)
EXPECTED_TOTAL = 80
EXPECTED_MATTER = 48
EXPECTED_ANTI = 32
EXPECTED_CONJUGATE_PARTNERS = 32
EXPECTED_MAJORANA_EXCEPTIONS = 16  # 14 NHP + 2 neutrino

CLASS_EXPECTED = {
    "electron_like_minus":                {"matter": 1, "anti": 1},
    "positron_substrate_slot":            {"matter": 1, "anti": 1},
    "heavier_charged_lepton_minus":       {"matter": 1, "anti": 1},
    "heavier_positron_substrate_slot":    {"matter": 1, "anti": 1},
    "neutrino_like":                      {"matter": 2, "anti": 0},
    "quark_like_charged":                 {"matter": 28, "anti": 28},
    "neutral_higher_partition":           {"matter": 14, "anti": 0},
}


# ----------------------------------------------------------------------
# Hash verification (hostile-environment protocol)
# ----------------------------------------------------------------------

def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_inputs():
    for path, locked in [(PRECOMMIT_PATH, PRECOMMIT_HASH),
                         (CATALOG_PATH, CATALOG_HASH)]:
        h = file_sha256(path)
        if h != locked:
            raise SystemExit(f"hash mismatch on {path}:\n  got    {h}\n  locked {locked}")


# ----------------------------------------------------------------------
# Promoter rule
# ----------------------------------------------------------------------

def parse_partition(sig):
    if not sig:
        return []
    out = []
    for piece in str(sig).split("+"):
        piece = piece.strip()
        if not piece:
            continue
        try:
            out.append(int(piece))
        except ValueError:
            pass
    return out


def legal_ports(p_components, q):
    out = set()
    for v_j in T13_DISTINCT:
        if v_j == 0:
            continue
        if q > 0 and q % v_j == 0:
            out.add(v_j); continue
        if any(p > 0 and p % v_j == 0 for p in p_components):
            out.add(v_j); continue
        if v_j == 1 and q == 0:
            out.add(v_j); continue
        if v_j == 18 and (18 in p_components or q == 18):
            out.add(v_j); continue
    return sorted(out)


def tensor_defect(q, port_values):
    """Bigrade-multiplicity closure defect; same rule as QP097."""
    if q == 0:
        return 0
    distinct = sorted(set(v for v in port_values if v > 0))
    if not distinct:
        return q
    best = q

    def rec(remaining, idx):
        nonlocal best
        if best == 0:
            return
        if remaining == 0:
            best = 0
            return
        if idx >= len(distinct):
            if remaining < best:
                best = remaining
            return
        v = distinct[idx]
        max_n = min(12, remaining // v)
        for n in range(max_n + 1):
            rec(remaining - n * v, idx + 1)

    rec(q, 0)
    return best


def is_promoted(row, h_allowed=H_ALLOWED, q_allowed=Q_ALLOWED, b_allowed=B_ALLOWED,
                require_I_T_zero=True):
    try:
        h_T = int(row.get("closure_depth", -1))
    except (ValueError, TypeError):
        return False
    try:
        q = int(row.get("q_abs", -1))
    except (ValueError, TypeError):
        return False
    bin_ = row.get("bin", "")
    if h_T not in h_allowed:
        return False
    if q not in q_allowed:
        return False
    if bin_ not in b_allowed:
        return False
    if require_I_T_zero:
        p_comp = parse_partition(row.get("partition_signature", ""))
        ports = legal_ports(p_comp, q)
        if tensor_defect(q, ports) != 0:
            return False
    return True


def classify_identity(row):
    """Pre-registered identity rules from precommit class table."""
    p = row.get("partition_signature", "")
    try:
        q = int(row["q_abs"])
    except (ValueError, TypeError):
        q = 0
    try:
        d = int(row["closure_depth"])
    except (ValueError, TypeError):
        d = 0
    sign = row.get("q_sign", "")
    is_anti = (row.get("bin") == "antimatter_conjugate_rows")

    if p == "1" and q == 1 and sign == "negative" and d == 0:
        return "electron_like_minus"
    if p == "1" and q == 1 and sign == "positive" and d == 0:
        return "positron_substrate_slot"
    if p == "1" and q == 1 and sign == "negative" and d >= 1:
        return "heavier_charged_lepton_minus"
    if p == "1" and q == 1 and sign == "positive" and d >= 1:
        return "heavier_positron_substrate_slot"
    if p == "1" and q == 0:
        return "neutrino_like"
    if p in {"2", "3", "4", "6", "8", "9", "12"} and q in {1, 2, 3, 4, 6, 8, 9, 12}:
        return "quark_like_charged"
    if p in {"2", "3", "4", "6", "8", "9", "12"} and q == 0:
        return "neutral_higher_partition"
    return "unclassified"


def find_conjugate_partner(row, all_rows):
    route = row.get("route_combination", "")
    if not route:
        return None
    bin_ = row.get("bin")
    if bin_ == "antimatter_conjugate_rows":
        if route.startswith("anti(") and route.endswith(")"):
            inner = route[5:-1]
            for r in all_rows:
                if (r.get("bin") != "antimatter_conjugate_rows"
                        and r.get("route_combination") == inner):
                    return r["candidate_id"]
        return None
    # matter side
    target = f"anti({route})"
    for r in all_rows:
        if (r.get("bin") == "antimatter_conjugate_rows"
                and r.get("route_combination") == target):
            return r["candidate_id"]
    return None


# ----------------------------------------------------------------------
# Wrong controls
# ----------------------------------------------------------------------

def wrong_control_W1_include_composite(rows):
    """Include bound_composite_rows."""
    b = B_ALLOWED | {"bound_composite_rows"}
    return sum(1 for r in rows if is_promoted(r, b_allowed=b))


def wrong_control_W2_include_depth_2(rows):
    """Include h_T = 2."""
    h = H_ALLOWED | {2}
    return sum(1 for r in rows if is_promoted(r, h_allowed=h))


def wrong_control_W3_drop_bigrade(rows):
    """Drop the q bigrade restriction (allow q in [0, 12])."""
    q = set(range(0, 13))
    return sum(1 for r in rows if is_promoted(r, q_allowed=q))


def wrong_control_W4_allow_I_T_positive(rows):
    """Include I_T > 0 rows."""
    return sum(1 for r in rows if is_promoted(r, require_I_T_zero=False))


def wrong_control_W5_random_bin_permutation(rows, n_trials=1000, seed=20260628):
    """Shuffle bin labels across the catalog, re-apply promoter."""
    rng = random.Random(seed)
    bins_orig = [r.get("bin") for r in rows]
    n_eq = 0
    counts = []
    for _ in range(n_trials):
        bins_shuf = list(bins_orig)
        rng.shuffle(bins_shuf)
        n_pass = 0
        for r, b in zip(rows, bins_shuf):
            r2 = dict(r)
            r2["bin"] = b
            if is_promoted(r2):
                n_pass += 1
        counts.append(n_pass)
        if n_pass == EXPECTED_TOTAL:
            n_eq += 1
    return n_eq, counts


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    verify_inputs()
    print(f"CR253 — Particle Promoter (80-row stable matter set)")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print(f"catalog hash   : {CATALOG_HASH}")
    print()

    rows = list(csv.DictReader(open(CATALOG_PATH, "r", encoding="utf-8")))
    print(f"Loaded {len(rows)} catalog rows (expected 299)")
    if len(rows) != 299:
        print(f"  *** catalog row count mismatch ***")
    print()

    # Apply promoter
    promoted = [r for r in rows if is_promoted(r)]
    n_promoted = len(promoted)
    n_matter = sum(1 for r in promoted if r.get("bin") == "stable_matter_rows")
    n_anti = sum(1 for r in promoted if r.get("bin") == "antimatter_conjugate_rows")

    print(f"Promoted row count: {n_promoted} (expected {EXPECTED_TOTAL})")
    print(f"  stable_matter_rows:        {n_matter} (expected {EXPECTED_MATTER})")
    print(f"  antimatter_conjugate_rows: {n_anti} (expected {EXPECTED_ANTI})")
    print()

    # Conjugate parity check
    anti_rows = [r for r in promoted if r.get("bin") == "antimatter_conjugate_rows"]
    n_partners = 0
    no_partner_list = []
    for r in anti_rows:
        partner = find_conjugate_partner(r, promoted)
        if partner:
            n_partners += 1
        else:
            no_partner_list.append(r["candidate_id"])
    print(f"Antimatter rows with matter conjugate partner: {n_partners}/{n_anti}")
    if no_partner_list:
        print(f"  no-partner anti rows: {no_partner_list[:10]}")
    print()

    # Matter rows without anti mirror (Majorana exceptions)
    matter_rows = [r for r in promoted if r.get("bin") == "stable_matter_rows"]
    no_mirror = []
    for r in matter_rows:
        partner = find_conjugate_partner(r, promoted)
        if partner is None:
            no_mirror.append(r)
    n_no_mirror = len(no_mirror)
    print(f"Matter rows without antimatter mirror (Majorana exceptions): "
          f"{n_no_mirror} (expected {EXPECTED_MAJORANA_EXCEPTIONS})")
    print()

    # Class breakdown
    class_obs = defaultdict(lambda: {"matter": 0, "anti": 0})
    for r in promoted:
        ident = classify_identity(r)
        if r.get("bin") == "antimatter_conjugate_rows":
            class_obs[ident]["anti"] += 1
        else:
            class_obs[ident]["matter"] += 1

    print(f"Class breakdown (matter / anti):")
    print(f"  {'class':>34s}  {'M_obs':>5s} {'M_exp':>5s}  {'A_obs':>5s} {'A_exp':>5s}  match")
    class_pass = True
    for cls, exp in CLASS_EXPECTED.items():
        obs = class_obs[cls]
        ok = (obs["matter"] == exp["matter"] and obs["anti"] == exp["anti"])
        print(f"  {cls:>34s}  {obs['matter']:>5d} {exp['matter']:>5d}  "
              f"{obs['anti']:>5d} {exp['anti']:>5d}  {'OK' if ok else 'MISS'}")
        if not ok:
            class_pass = False
    n_unclassified = class_obs.get("unclassified", {"matter": 0, "anti": 0})
    if n_unclassified["matter"] or n_unclassified["anti"]:
        print(f"  {'unclassified':>34s}  {n_unclassified['matter']:>5d}     -  "
              f"{n_unclassified['anti']:>5d}     -  MISS")
        class_pass = False
    print()

    # Wrong controls
    print(f"Wrong controls:")
    W1 = wrong_control_W1_include_composite(rows)
    W2 = wrong_control_W2_include_depth_2(rows)
    W3 = wrong_control_W3_drop_bigrade(rows)
    W4 = wrong_control_W4_allow_I_T_positive(rows)
    print(f"  W1 (include bound_composite_rows): {W1} rows   "
          f"(canonical={EXPECTED_TOTAL}; "
          f"{'sensitive' if W1 != EXPECTED_TOTAL else 'NOT_SENSITIVE'})")
    print(f"  W2 (include h_T = 2):              {W2} rows   "
          f"({'sensitive' if W2 != EXPECTED_TOTAL else 'NOT_SENSITIVE'})")
    print(f"  W3 (drop bigrade q-rule):          {W3} rows   "
          f"({'sensitive' if W3 != EXPECTED_TOTAL else 'NOT_SENSITIVE'})")
    print(f"  W4 (allow I_T > 0):                {W4} rows   "
          f"({'sensitive' if W4 != EXPECTED_TOTAL else 'NOT_SENSITIVE'})")

    print(f"  W5 (random bin permutation, 1000 trials)...")
    W5_eq, W5_counts = wrong_control_W5_random_bin_permutation(rows)
    W5_p = W5_eq / 1000
    print(f"      trials reproducing 80 exactly: {W5_eq}/1000 = {W5_p:.4f}")
    print(f"      null mean count: {sum(W5_counts)/len(W5_counts):.2f}")
    print()

    # Verdict
    cond_1 = (n_promoted == EXPECTED_TOTAL)
    cond_2 = (n_matter == EXPECTED_MATTER and n_anti == EXPECTED_ANTI)
    cond_3 = (n_partners == EXPECTED_ANTI)
    cond_4 = class_pass
    cond_5 = (W1 != EXPECTED_TOTAL and W2 != EXPECTED_TOTAL
              and W3 != EXPECTED_TOTAL and W4 != EXPECTED_TOTAL)
    cond_6 = (W5_p < 0.05)
    all_pass = cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6
    delta_from_expected = abs(n_promoted - EXPECTED_TOTAL)
    parity_broken = (n_partners < EXPECTED_ANTI)

    if all_pass:
        verdict = "PASS"
    elif delta_from_expected <= 2 and not parity_broken:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"Verdict conditions:")
    print(f"  (1) 80 rows exact         : {'PASS' if cond_1 else 'FAIL'}")
    print(f"  (2) 48/32 split exact     : {'PASS' if cond_2 else 'FAIL'}")
    print(f"  (3) 32/32 conjugate parity: {'PASS' if cond_3 else 'FAIL'}")
    print(f"  (4) class breakdown exact : {'PASS' if cond_4 else 'FAIL'}")
    print(f"  (5) W1-W4 each sensitive  : {'PASS' if cond_5 else 'FAIL'}")
    print(f"  (6) W5 p < 0.05           : {'PASS' if cond_6 else 'FAIL'}")
    print()
    print(f"CR253 VERDICT: {verdict}")
    print()

    # ----- Emit outputs -----
    promoted_csv = os.path.join(HERE, "CR253_promoted_80_rows.csv")
    with open(promoted_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "bin", "partition_signature", "q_abs", "q_sign",
                    "closure_depth", "qA_source_support", "identity_rule",
                    "conjugate_partner"])
        for r in promoted:
            ident = classify_identity(r)
            partner = find_conjugate_partner(r, promoted) or ""
            w.writerow([r["candidate_id"], r["bin"], r["partition_signature"],
                        r["q_abs"], r["q_sign"], r["closure_depth"],
                        r.get("qA_source_support", ""), ident, partner])

    wc_csv = os.path.join(HERE, "CR253_wrong_controls.csv")
    with open(wc_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "description", "rows_observed", "expected_canonical",
                    "sensitive"])
        w.writerow(["W1", "include bound_composite_rows", W1, EXPECTED_TOTAL,
                    W1 != EXPECTED_TOTAL])
        w.writerow(["W2", "include h_T = 2", W2, EXPECTED_TOTAL,
                    W2 != EXPECTED_TOTAL])
        w.writerow(["W3", "drop bigrade q-rule", W3, EXPECTED_TOTAL,
                    W3 != EXPECTED_TOTAL])
        w.writerow(["W4", "allow I_T > 0", W4, EXPECTED_TOTAL,
                    W4 != EXPECTED_TOTAL])
        w.writerow(["W5_p", "random bin permutation p", f"{W5_p:.4f}",
                    "< 0.05", W5_p < 0.05])
        w.writerow(["W5_null_mean", "null mean count under permutation",
                    f"{sum(W5_counts)/len(W5_counts):.2f}", "", ""])

    summary = {
        "artifact": "CR253_PARTICLE_PROMOTER_80_ROW",
        "precommit_hash": PRECOMMIT_HASH,
        "catalog_hash": CATALOG_HASH,
        "verdict": verdict,
        "n_loaded": len(rows),
        "n_promoted": n_promoted,
        "n_matter": n_matter,
        "n_anti": n_anti,
        "n_conjugate_partners": n_partners,
        "n_majorana_exceptions": n_no_mirror,
        "class_observed": {k: dict(v) for k, v in class_obs.items()},
        "class_expected": CLASS_EXPECTED,
        "wrong_controls": {
            "W1_include_composite": W1,
            "W2_include_depth_2": W2,
            "W3_drop_bigrade": W3,
            "W4_allow_I_T_positive": W4,
            "W5_random_perm_p": W5_p,
            "W5_null_mean": sum(W5_counts) / len(W5_counts),
        },
        "verdict_conditions": {
            "exactly_80": cond_1,
            "48_32_split": cond_2,
            "32_32_parity": cond_3,
            "class_breakdown_exact": cond_4,
            "W1_W4_sensitive": cond_5,
            "W5_p_lt_05": cond_6,
        },
    }
    with open(os.path.join(HERE, "CR253_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
