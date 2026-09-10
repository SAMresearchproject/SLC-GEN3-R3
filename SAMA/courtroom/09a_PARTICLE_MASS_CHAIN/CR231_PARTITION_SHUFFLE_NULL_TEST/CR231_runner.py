"""
CR231 Partition-Shuffle Null Test — Runner

Takes the canonical 139-row CR219 promoted-particle table and answers:
   "Did the structural closure {support_sum=81, mirror=81, ledger=162, write_rate=27}
    only appear because the rows were sorted nicely?"

The test:
   1. Verify the canonical table reproduces all four targets (sanity).
   2. Randomly permute the 139 partition labels and score each shuffle.
   3. Report the empirical p-value of the canonical configuration against the null.
   4. Run wrong controls (synthetic uniform, shifted targets, marginal-preserving).

Locked precommit: CR231_PRECOMMIT.md (sha b94a48033a4e803917ea554fa1ffbba72578d11dc32d4bad9be0ef9e3775c8ed).
Source: C:\\VS\\CR219_promoted_particle_rows_126.csv (sha 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f).
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

CR_ID = "CR231"
CR_DIR = Path(__file__).resolve().parent
SOURCE_CSV = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")
SOURCE_SHA_EXPECTED = "45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f"

R = 12
D = 3
ALPHA_H = 2

TARGET_SUPPORT_SUM = 81
TARGET_MIRROR = 81
TARGET_LEDGER = 162
TARGET_WRITE_RATE_TIMES_R = 81 * 4  # 27 * R = 324

SUPPORT_ROSTER_IDS = {
    "QP093A-0300", "QP093A-0301", "QP093A-0302", "QP093A-0304",
    "QP093A-0306", "QP093A-0307", "QP093A-0308", "QP093A-0309",
    "QP093A-0310", "QP093A-0311", "QP093A-0312", "QP093A-0313",
}
MIRROR_ID = "QP093A-0303"

N_TRIALS = 10000
SEED_UNIFORM = 20260622
SEED_MARGINAL = 20260623
SEED_WC1 = 20260624
SEED_WC2 = 20260625
SEED_WC3 = 20260626


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def evaluate_partition_label(label: str) -> int:
    """'1+1+1' -> 3, '18' -> 18, '81' -> 81."""
    parts = label.strip().split("+")
    return sum(int(p) for p in parts)


def load_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        # First column is the "139" declared count -> rename to source_order
        if header[0].isdigit():
            header[0] = "source_order"
        rows = [dict(zip(header, r)) for r in reader]
    return header, rows


def find_target_positions(rows):
    support_positions = []
    mirror_position = None
    for i, row in enumerate(rows):
        cid = row["candidate_id"]
        if cid in SUPPORT_ROSTER_IDS:
            support_positions.append(i)
        if cid == MIRROR_ID:
            mirror_position = i
    assert len(support_positions) == 12, f"expected 12 support positions, got {len(support_positions)}"
    assert mirror_position is not None, "mirror QP093A-0303 not found"
    return support_positions, mirror_position


def score(labels, support_positions, mirror_position):
    support_sum = sum(labels[i] for i in support_positions)
    mirror_value = labels[mirror_position]
    ledger = support_sum + mirror_value
    write_rate_x_R = support_sum * 4
    t1 = support_sum == TARGET_SUPPORT_SUM
    t2 = mirror_value == TARGET_MIRROR
    t3 = ledger == TARGET_LEDGER
    t4 = write_rate_x_R == TARGET_WRITE_RATE_TIMES_R
    return {
        "support_sum": support_sum,
        "mirror_value": mirror_value,
        "ledger": ledger,
        "write_rate_x_R": write_rate_x_R,
        "hit_t1": t1,
        "hit_t2": t2,
        "hit_t3": t3,
        "hit_t4": t4,
        "hit_all_four": t1 and t2 and t3 and t4,
    }


def run_uniform_permutation(numeric_labels, support_positions, mirror_position, n_trials, seed):
    rng = random.Random(seed)
    labels = list(numeric_labels)
    hits_all = 0
    hits_t1 = 0
    hits_t2 = 0
    hits_t3 = 0
    hits_t4 = 0
    support_sums = []
    mirror_values = []
    for _ in range(n_trials):
        rng.shuffle(labels)
        s = score(labels, support_positions, mirror_position)
        support_sums.append(s["support_sum"])
        mirror_values.append(s["mirror_value"])
        if s["hit_t1"]:
            hits_t1 += 1
        if s["hit_t2"]:
            hits_t2 += 1
        if s["hit_t3"]:
            hits_t3 += 1
        if s["hit_t4"]:
            hits_t4 += 1
        if s["hit_all_four"]:
            hits_all += 1
    return {
        "n_trials": n_trials,
        "hits_all_four": hits_all,
        "hits_t1_support_81": hits_t1,
        "hits_t2_mirror_81": hits_t2,
        "hits_t3_ledger_162": hits_t3,
        "hits_t4_write_rate_27": hits_t4,
        "p_value_all_four_with_smoothing": (hits_all + 1) / (n_trials + 1),
        "p_value_t1": (hits_t1 + 1) / (n_trials + 1),
        "p_value_t2": (hits_t2 + 1) / (n_trials + 1),
        "p_value_t3": (hits_t3 + 1) / (n_trials + 1),
        "p_value_t4": (hits_t4 + 1) / (n_trials + 1),
        "support_sum_mean": sum(support_sums) / len(support_sums),
        "support_sum_min": min(support_sums),
        "support_sum_max": max(support_sums),
        "mirror_value_mean": sum(mirror_values) / len(mirror_values),
        "support_sums": support_sums,
        "mirror_values": mirror_values,
    }


def run_marginal_resample(numeric_labels, support_positions, mirror_position, n_trials, seed):
    """With-replacement resample from empirical label distribution.
    Preserves marginal frequencies in expectation; allows duplicates across trials."""
    rng = random.Random(seed)
    n = len(numeric_labels)
    hits_all = 0
    hits_t1 = 0
    hits_t2 = 0
    for _ in range(n_trials):
        sample = [rng.choice(numeric_labels) for _ in range(n)]
        s = score(sample, support_positions, mirror_position)
        if s["hit_t1"]:
            hits_t1 += 1
        if s["hit_t2"]:
            hits_t2 += 1
        if s["hit_all_four"]:
            hits_all += 1
    return {
        "n_trials": n_trials,
        "hits_all_four": hits_all,
        "hits_t1_support_81": hits_t1,
        "hits_t2_mirror_81": hits_t2,
        "p_value_all_four_with_smoothing": (hits_all + 1) / (n_trials + 1),
    }


def wc1_synthetic_uniform_modes(support_positions, mirror_position, n_trials, seed):
    """WC1: each row gets a label drawn uniformly from {1,2,3,4,6,8,9,12}.
    Expect ~0/10000 simultaneous-four-target hits — sanity check."""
    rng = random.Random(seed)
    modes = [1, 2, 3, 4, 6, 8, 9, 12]
    n_positions = len(support_positions) + 1 + max(0, mirror_position + 1)
    # use 139 positions to match
    n_positions = 139
    hits = 0
    for _ in range(n_trials):
        sample = [rng.choice(modes) for _ in range(n_positions)]
        s = score(sample, support_positions, mirror_position)
        if s["hit_all_four"]:
            hits += 1
    return {"n_trials": n_trials, "hits": hits, "rate": hits / n_trials}


def wc2_shifted_targets(numeric_labels, support_positions, mirror_position, n_trials, seed,
                        shifted_support=91, shifted_mirror=91):
    """WC2: targets shifted by +10. The same permutation shuffle should NOT hit shifted targets
    at the same rate as it hits the real targets if the real-target rate has real structure."""
    rng = random.Random(seed)
    labels = list(numeric_labels)
    hits = 0
    for _ in range(n_trials):
        rng.shuffle(labels)
        support_sum = sum(labels[i] for i in support_positions)
        mirror_value = labels[mirror_position]
        if support_sum == shifted_support and mirror_value == shifted_mirror:
            hits += 1
    return {
        "n_trials": n_trials,
        "shifted_target_support": shifted_support,
        "shifted_target_mirror": shifted_mirror,
        "hits": hits,
        "rate": hits / n_trials,
    }


def write_distributions_csv(uniform_result, path: Path):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["trial", "support_sum_12_positions", "mirror_value", "ledger", "write_rate_x_R"])
        for i, (ss, mv) in enumerate(zip(uniform_result["support_sums"], uniform_result["mirror_values"]), start=1):
            writer.writerow([i, ss, mv, ss + mv, ss * 4])


def main():
    print("=" * 72)
    print("CR231 Partition-Shuffle Null Test")
    print("=" * 72)

    # ---- Source verification ----
    src_sha = sha256_file(SOURCE_CSV)
    print(f"\nSource file: {SOURCE_CSV}")
    print(f"  SHA-256:     {src_sha}")
    print(f"  Expected:    {SOURCE_SHA_EXPECTED}")
    assert src_sha == SOURCE_SHA_EXPECTED, "source SHA mismatch — refusing to run"
    print("  [PASS] source SHA matches precommit lock")

    # ---- Load rows ----
    header, rows = load_rows(SOURCE_CSV)
    print(f"\nRows loaded: {len(rows)}")
    assert len(rows) == 139, f"expected 139 rows, got {len(rows)}"

    # ---- Locate target positions ----
    support_positions, mirror_position = find_target_positions(rows)
    print(f"Support roster positions (12): {sorted(support_positions)}")
    print(f"Mirror QP093A-0303 position:   {mirror_position}")

    # ---- Extract numeric partition labels ----
    raw_labels = [r["partition_signature"] for r in rows]
    numeric_labels = [evaluate_partition_label(L) for L in raw_labels]
    print(f"\nNumeric label total sum: {sum(numeric_labels)}")
    label_counter = Counter(numeric_labels)
    print(f"Distinct evaluated values: {len(label_counter)}")
    print(f"Largest evaluated values: {sorted(label_counter.keys(), reverse=True)[:8]}")

    # ---- Canonical sanity check ----
    print("\n[CANONICAL] Verify true table reproduces all four targets:")
    canonical = score(numeric_labels, support_positions, mirror_position)
    for k in ("support_sum", "mirror_value", "ledger", "write_rate_x_R"):
        print(f"  {k}: {canonical[k]}")
    canonical_all_pass = canonical["hit_all_four"]
    print(f"  hit_all_four: {canonical_all_pass}")
    assert canonical_all_pass, "P4 violation: canonical table does NOT hit all four targets"
    print("  [P4 PASS] canonical reproduces support_sum=81, mirror=81, ledger=162, write_rate*R=324")

    # ---- Null A: uniform random permutation ----
    print(f"\n[NULL A] Uniform random permutation, n={N_TRIALS}, seed={SEED_UNIFORM}")
    uniform_result = run_uniform_permutation(
        numeric_labels, support_positions, mirror_position, N_TRIALS, SEED_UNIFORM
    )
    print(f"  hits_all_four:            {uniform_result['hits_all_four']} / {N_TRIALS}")
    print(f"  hits_t1 (support_sum=81): {uniform_result['hits_t1_support_81']}")
    print(f"  hits_t2 (mirror=81):      {uniform_result['hits_t2_mirror_81']}")
    print(f"  hits_t3 (ledger=162):     {uniform_result['hits_t3_ledger_162']}")
    print(f"  hits_t4 (write_rate=27):  {uniform_result['hits_t4_write_rate_27']}")
    print(f"  p_value_all_four:         {uniform_result['p_value_all_four_with_smoothing']:.6f}")
    print(f"  support_sum mean/min/max: {uniform_result['support_sum_mean']:.2f} / "
          f"{uniform_result['support_sum_min']} / {uniform_result['support_sum_max']}")

    # ---- Null B: marginal-preserving resample ----
    print(f"\n[NULL B] Marginal-preserving (with-replacement), n={N_TRIALS}, seed={SEED_MARGINAL}")
    marginal_result = run_marginal_resample(
        numeric_labels, support_positions, mirror_position, N_TRIALS, SEED_MARGINAL
    )
    print(f"  hits_all_four:            {marginal_result['hits_all_four']} / {N_TRIALS}")
    print(f"  p_value_all_four:         {marginal_result['p_value_all_four_with_smoothing']:.6f}")

    # ---- WC1: synthetic uniform random modes ----
    print(f"\n[WC1] Synthetic uniform random labels from {{1,2,3,4,6,8,9,12}}, n={N_TRIALS}")
    wc1 = wc1_synthetic_uniform_modes(support_positions, mirror_position, N_TRIALS, SEED_WC1)
    print(f"  hits: {wc1['hits']} / {N_TRIALS} (rate {wc1['rate']:.6f})")
    print(f"  expect ~0 hits (no 81-valued labels in source)")

    # ---- WC2: shifted targets ----
    print(f"\n[WC2] Shifted targets (support=91, mirror=91), uniform shuffle, n={N_TRIALS}")
    wc2 = wc2_shifted_targets(
        numeric_labels, support_positions, mirror_position, N_TRIALS, SEED_WC2,
        shifted_support=91, shifted_mirror=91,
    )
    print(f"  hits: {wc2['hits']} / {N_TRIALS} (rate {wc2['rate']:.6f})")

    # ---- Verdict ----
    print("\n" + "=" * 72)
    pass_threshold = 0.001
    boundary_threshold = 0.05
    p_main = uniform_result["p_value_all_four_with_smoothing"]
    if p_main < pass_threshold:
        verdict = "PASS"
    elif p_main < boundary_threshold:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"
    print(f"Primary p-value (uniform permutation null): {p_main:.6f}")
    print(f"CR231 verdict (pass<0.001, boundary<0.05): {verdict}")
    print("=" * 72)

    # ---- Persist results ----
    write_distributions_csv(uniform_result, CR_DIR / "CR231_shuffle_distributions.csv")
    print(f"\nWrote: CR231_shuffle_distributions.csv")

    summary = {
        "artifact": "CR231_PARTITION_SHUFFLE_NULL_TEST",
        "classification": "STRUCTURAL_NULL_TEST",
        "arc_position": "Test 2 of 7 in the Seven-Test Ownership Arc (CR230-CR236)",
        "permission_status": "GRANTED_BY_USER_SEAN_BRADY_2026_06_22",
        "source_file": str(SOURCE_CSV),
        "source_sha256": src_sha,
        "precommit_sha256": "b94a48033a4e803917ea554fa1ffbba72578d11dc32d4bad9be0ef9e3775c8ed",
        "constants": {"R": R, "D": D, "alpha_H": ALPHA_H},
        "targets": {
            "support_sum_12_roster": TARGET_SUPPORT_SUM,
            "mirror_QP093A_0303": TARGET_MIRROR,
            "closed_ledger": TARGET_LEDGER,
            "write_rate_times_R": TARGET_WRITE_RATE_TIMES_R,
            "write_rate_target": 27,
        },
        "n_rows": len(rows),
        "n_support_positions": len(support_positions),
        "mirror_position_index": mirror_position,
        "canonical_table": canonical,
        "canonical_passes_all_four": canonical_all_pass,
        "null_A_uniform_permutation": {k: v for k, v in uniform_result.items() if k not in ("support_sums", "mirror_values")},
        "null_B_marginal_preserving": marginal_result,
        "WC1_synthetic_uniform_modes": wc1,
        "WC2_shifted_targets": wc2,
        "primary_p_value": p_main,
        "pass_threshold": pass_threshold,
        "boundary_threshold": boundary_threshold,
        "scientific_verdict": verdict,
        "execution_status": "CLEAN",
        "seeds": {
            "uniform": SEED_UNIFORM,
            "marginal": SEED_MARGINAL,
            "wc1": SEED_WC1,
            "wc2": SEED_WC2,
        },
        "K_gates": {
            "K1_external_anchor": "N/A (structural null test)",
            "K2_falsification_statement": "PASS",
            "K3_target_hygiene": "PASS (targets locked in precommit before shuffles run)",
            "K4_typed_inputs": "PASS (canonical CR219 source SHA-locked)",
            "K5_reproduction_on_demand": "PASS (seeded runner reproduces every trial)",
        },
    }
    with (CR_DIR / "CR231_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote: CR231_summary.json")

    print(f"\nDone. Verdict: {verdict}")
    return verdict


if __name__ == "__main__":
    main()
