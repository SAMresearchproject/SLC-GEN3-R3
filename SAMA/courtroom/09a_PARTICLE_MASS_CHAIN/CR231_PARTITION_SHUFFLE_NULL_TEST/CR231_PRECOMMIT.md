# CR231 Partition-Shuffle Null Test — Precommit

**Date:** 2026-06-22
**Classification:** STRUCTURAL_NULL_TEST (Monte Carlo against random partition assignment)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("I'll let you go ahead and start the next test")
**Source:** `C:\Users\drwho\OneDrive\Desktop\Tests.docx` Test 2 ("Partition-shuffle null test")
**Part of:** Seven-test ownership arc (CR230-CR236)
**Arc position:** Test 2 of 7 — null-hypothesis statistical test on the substrate structural numbers verified in CR230.
**Status:** PRECOMMITTED, runner execution scheduled for next session.

## Scope

Answer Sean's question: *"Did this only appear because I sorted the rows nicely?"*

Take the 139 active particle rows (the post-CR216-dedup table — `126 matter-allowed rows + 13 blocked non-matter rows` per CR222d's promotion gate). Randomly shuffle the partition-signature labels thousands of times. Score each shuffled assignment against the four target structural numbers (CR230 verified) and compare the true table's score against the null distribution.

## The 139 Rows (Identification at Execution)

The runner must first locate the canonical 139-row source. Most likely candidates (must verify at execution):

1. **CR222d_ROW_TAXONOMY_PROMOTION_GATE** in 12a — explicitly says "139 rows split as 126 matter allowed + 13 blocked non-matter"
2. **CR119@09a** vault reveal — 321 particles, of which 126 matter + 195 complement; the 139 likely cuts to active rows only after CR216 dedup
3. **CR216_particle_complement_194_active.csv** — 194 rows post-dedup; the 139 is a subset

Runner precommit step: identify the canonical 139-row file, lock its SHA, freeze before any shuffle.

## Target Structural Numbers (from CR230, hash-locked)

```text
T1: 12-mode closure  =  81    (12 unpacked carrier elements sum, verified CR230 step 6)
T2: 0303 mirror      =  81    (D^(D+1) mirror sum, verified CR230 step 7)
T3: closed ledger    =  162   (81 + 81 = R²·9/8, verified CR230 step 8)
T4: write-rate       =  27    (81·4/R = D³, verified CR230 step 9)
```

These four are the targets the shuffled assignments must NOT hit (or must hit only at rate `p < 0.001`).

## Shuffle Design (Precommitted Before Execution)

```text
For each trial i in [1, 10000]:
  1. Take the 139 rows with their original (id, M_native, S_debit, q, q_sign, etc.) columns
  2. Randomly permute the partition labels (the p values: {1, 2, 3, 4, 6, 8, 9, 12} and the
     larger lifted values 18, 81, etc.) across the rows. Permutation must be uniform and
     full (every label assigned once, no duplicates introduced).
  3. Recompute the four target sums under the shuffled assignment:
       - 12-mode closure
       - 0303 mirror
       - closed ledger
       - write-rate
  4. Record whether ALL FOUR target values are simultaneously reproduced.
  5. Record the per-target distance from each target value (for distribution analysis).

After 10000 trials, compute:
  - Empirical probability of reproducing all four targets simultaneously
  - Per-target empirical distribution
  - p-value for the true table's score against the empirical distribution
```

## Pass Condition (Precommitted)

```text
PASS  if  p_value < 0.001 against random partition assignment
       (true table reproduces all four targets simultaneously;
        fewer than 10 of 10000 random shuffles do)

BOUNDARY  if  0.001 ≤ p_value < 0.05
       (weakly significant; suggests structural pattern but not conclusive)

FAIL  if  p_value ≥ 0.05
       (random shuffles reproduce the targets at comparable rate;
        the substrate's structural pattern is statistical coincidence)
```

## Why This Test Matters

CR230 verified that `{R, D, α_H}` algebraically produce the structural numbers, but a skeptic could ask: "What if the table is arranged so that ANY partition assignment of comparable values would produce closures like these?" CR231 answers by showing that random shuffles do NOT produce the same closures — the structural signal beats the null distribution by 1000:1 or stronger.

If CR231 PASSES, the substrate's structural pattern is shown to be statistically robust against the "you arranged it" objection.

If CR231 FAILS or BOUNDARIES, that's a real signal that the structural reading may be weaker than CR230 alone suggests. (Honest discipline: report whatever the runner finds; don't suppress.)

## Wrong Controls / Sanity Checks (Precommitted)

- **WC1:** Run the shuffle on a synthetic table where the partition labels are uniformly random by construction. Expect ~0/10000 hit rate (sanity check that the runner's shuffle is actually random).
- **WC2:** Run the shuffle on the canonical 139-row table but with the targets shifted by ±10 (e.g., target 91 instead of 81). Expect the same hit rate as random — confirms the test's discriminative power comes from the specific target values, not from any quirk of the shuffle.
- **WC3:** Run the shuffle preserving only the marginal distribution of partition labels (each label appears the same number of times as in the real table). This is a stronger null — closer to the real structural constraint. The expected significance should be weaker than WC2's uniform shuffle but still strong if the pattern is real.

## Precommitted Predictions

- **P1:** Locate canonical 139-row file and verify SHA-locked before any shuffle
- **P2:** Run 10000 uniform random shuffles
- **P3:** Run 10000 marginal-preserving shuffles (stronger null)
- **P4:** True table reproduces all four target values (sanity check — must)
- **P5:** Uniform-random null: p < 0.001 for simultaneous four-target closure
- **P6:** Marginal-preserving null: p-value reported honestly (could be weaker)
- **P7:** Per-target distributions are reported in `CR231_shuffle_distributions.csv`
- **P8:** WC1-WC3 sanity checks all behave as predicted

## Upstream Sources (Hash-Locked, Read-Only)

```text
CR230_result.md (target structural numbers verified algebraically) = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR229_result.md (inclusion-exclusion identity)                      = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR222_result.md (carrier ledger 12+1 = 81+81 = 162)                 = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR216_result.md (carrier duplicate retirement, 194 active rows)     = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
```

Plus: the canonical 139-row source file (to be located and SHA-locked at execution time).

## Falsifier

If the runner finds that random partition shuffles reproduce all four target values at rate `≥ 5%`, this CR's verdict falsifies and the substrate's structural pattern must be reconsidered as potentially editorial.

## What Next Session Needs to Do

1. Locate the canonical 139-row source file. Most likely `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR222d_ROW_TAXONOMY_PROMOTION_GATE/` or `09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/` — verify which.
2. Lock its SHA-256 in the runner.
3. Write `CR231_runner.py` that implements the shuffle design above with 10000 trials each for uniform and marginal-preserving nulls.
4. Run and record results in `CR231_summary.json` + `CR231_shuffle_distributions.csv`.
5. Write `CR231_result.md` honoring the precommit. Whatever p-values come back, report them honestly.
6. Compute SHAs and write HASHES.txt.
7. Update TEST_INDEX.csv with the actual result.

## Honest Note

This precommit was sealed in a session with very limited remaining budget. The shuffle design, target values, pass conditions, and wrong controls are locked here BEFORE any actual Monte Carlo run. That's the K3 (target hygiene) discipline at work — the runner inherits a precommit it cannot tune. Next session executes against this locked frame.

If next session finds the precommit needs refinement (e.g., the 139-row source is different than assumed; the marginal-preserving null needs a more sophisticated construction), the refinement is itself a precommit-level decision that should be documented in `CR231_PRECOMMIT_v2.md` rather than baked into the executor.

## Sequence Reminder

CR231 is **Test 2 of 7** in the Seven-Test Ownership Arc. Tests 3-7 remain:

- CR232 (Test 3): Matter/support promotion gate audit
- CR233 (Test 4): 18 / 81 / 27 tensor-substrate role-separation test
- CR234 (Test 5): Blind SOB element engine (Z-only input)
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.
