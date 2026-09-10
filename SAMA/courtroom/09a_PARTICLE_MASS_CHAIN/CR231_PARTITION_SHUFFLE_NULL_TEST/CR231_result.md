# CR231 Partition-Shuffle Null Test — Result

## Verdict

```text
CR231_PASS_PARTITION_SHUFFLE_NULL_TEST__P_0_0003_AT_10000_TRIALS_UNIFORM_PERMUTATION__P_0_0002_MARGINAL_PRESERVING__BOTH_NULLS_BEAT_PASS_THRESHOLD_0_001__CANONICAL_TABLE_HITS_FOUR_FOUR_TARGETS__WC1_WC2_SANITY_BEHAVE_AS_PREDICTED__SUBSTRATE_STRUCTURAL_CLOSURE_NOT_EDITORIAL_ARRANGEMENT
```

`execution_status   = CLEAN`
`scientific_verdict = PASS`
`classification     = STRUCTURAL_NULL_TEST (Monte Carlo against random partition assignment)`
`arc_position       = Test 2 of 7 in the Seven-Test Ownership Arc`
`precommit_locked   = b94a48033a4e803917ea554fa1ffbba72578d11dc32d4bad9be0ef9e3775c8ed`

## Sean's Question (Answered)

> *"Did this only appear because I sorted the rows nicely?"*

**No.** Random permutations of the 139-row partition-signature multiset reproduce
the structural closure `{support_sum=81, mirror=81, ledger=162, write_rate=27}`
in **2 of 10000** uniform shuffles and **1 of 10000** marginal-preserving shuffles.
Both nulls beat the precommitted pass threshold of `p < 0.001` by 3×–5×. The
substrate's four-target closure is a property of the row identifications, not a
side-effect of how the rows are listed.

## Inputs (Hash-Locked)

```text
Source CSV:        C:\VS\CR219_promoted_particle_rows_126.csv
Source SHA-256:    45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Row count:         139
Support roster:    12 IDs (QP093A-0300/0301/0302/0304/0306..0313)
Mirror duplicate:  QP093A-0303 (row index 138)
Targets:           support_sum=81, mirror=81, ledger=162, write_rate=27 (CR230 verified)
```

## Canonical Table Sanity (Precommit P4)

```text
support_sum at 12 support-roster row positions  = 81  [hit T1 = True]
mirror_value at QP093A-0303 position             = 81  [hit T2 = True]
closed_ledger (support_sum + mirror)              = 162 [hit T3 = True]
write_rate_x_R (support_sum × 4)                  = 324 [hit T4 = True, write_rate = 27]
hit_all_four                                      = True
```

**[P4 PASS]** The true table reproduces all four targets simultaneously.

## Null A — Uniform Random Permutation (Primary)

```text
n_trials              = 10000
seed                  = 20260622
hits_all_four         = 2     (≤9 expected if p < 0.001)
p_value_all_four      = 0.000300  (with Laplace +1 smoothing)
```

**Per-target breakdown:**

| Target | What it tests | Hits | Empirical p | Notes |
|---|---|---|---|---|
| T1 | support_sum at 12 positions = 81 | 251 / 10000 | 0.0251 | mean support_sum = 95.4 (canonical 81 sits in left tail) |
| T2 | mirror value = 81 | 70 / 10000 | 0.0070 | matches the expected 1/139 = 0.0072 (only one 81 in multiset) |
| T3 | ledger = 162 | 24 / 10000 | 0.0024 | constrained sum 81+81=162 |
| T4 | write_rate = 27 (i.e., support_sum × 4 = 324) | 251 / 10000 | 0.0251 | mathematically equivalent to T1 |
| **All four jointly** | **support_sum=81 AND mirror=81 (T3, T4 follow)** | **2 / 10000** | **0.000300** | **primary p-value** |

T1 and T4 are mathematically equivalent (write_rate*R = support_sum*4; 81×4=324 only iff sum=81), so the four targets reduce to two independent events under permutation. T1×T2 ≈ 251×70/10⁸ = 1.76 expected joint hits if independent; observed 2 (within Poisson noise of independence). The joint p of 0.000300 is therefore consistent with two approximately-independent rare events.

**Support-sum distribution from 10000 shuffles:**

```text
mean = 95.38, min = 38, max = 206
canonical 81 is in the lower left tail
```

## Null B — Marginal-Preserving Resample (Stronger Null per Precommit WC3)

```text
n_trials              = 10000
seed                  = 20260623
method                = with-replacement bootstrap from empirical 139-label distribution
hits_all_four         = 1
p_value_all_four      = 0.000200
```

The marginal-preserving null is independently consistent with the uniform-permutation null. Both beat `p < 0.001`.

## Wrong Controls / Sanity Checks (Precommitted)

### WC1 — Synthetic Uniform Modes (Precommit WC1)

Each of 139 positions gets a label drawn uniformly from `{1,2,3,4,6,8,9,12}` (the bigrade-lattice partition modes). Since no `81` exists in the synthetic distribution, mirror can never = 81.

```text
n_trials = 10000, seed = 20260624
hits     = 0 / 10000 (rate 0.000000)
expected = 0 (no 81-valued labels available)
[WC1 PASS] sanity confirmed
```

### WC2 — Shifted Targets (Precommit WC2)

Same uniform permutation null as Null A, but score against shifted targets `support_sum = 91` and `mirror = 91` (true targets ±10).

```text
n_trials = 10000, seed = 20260625
hits     = 0 / 10000 (rate 0.000000)
[WC2 PASS] discriminative power confirmed — wrong targets are not hit
```

### WC3 — Marginal-Preserving Null

Implemented as Null B above. Reports `p = 0.000200`, slightly stronger than Null A. **[WC3 PASS]**.

## Predictions Checks (vs. Precommit)

- **[PASS]** P1: Canonical 139-row file located and SHA-locked (`45a8e7d2…`).
- **[PASS]** P2: 10000 uniform random shuffles executed.
- **[PASS]** P3: 10000 marginal-preserving shuffles executed.
- **[PASS]** P4: True table reproduces all four target values (sanity).
- **[PASS]** P5: Uniform-random null p_value `= 0.000300 < 0.001` — simultaneous four-target closure.
- **[PASS]** P6: Marginal-preserving null p_value `= 0.000200` reported honestly (slightly stronger than P5; both pass).
- **[PASS]** P7: Per-target distributions written to `CR231_shuffle_distributions.csv`.
- **[PASS]** P8: WC1 (0 hits) and WC2 (0 hits) behave as predicted; WC3 reported above.

## Falsifier Status

Precommit falsifier: *"If random partition shuffles reproduce all four target values at rate ≥ 5%, this CR's verdict falsifies."*

Observed rate: **0.02%** (2/10000). Margin to falsification threshold: ~250×.

## K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 external anchor | N/A | Structural null test; no external data anchor |
| K2 falsification | PASS | Pre-stated falsifier (rate ≥ 5%) with explicit threshold |
| K3 target hygiene | PASS | Targets `{81,81,162,27}` locked in PRECOMMIT (sha `b94a48…`) before any shuffle ran; runner inherits a frame it cannot tune |
| K4 typed inputs | PASS | Source CSV SHA-locked; target values inherited from sealed CR230 (sha `3c1fd16…`) |
| K5 reproduction on demand | PASS | Seeded runner — every trial reproducible with `python CR231_runner.py` |

## Upstream Sources (Hash-Locked)

```text
CR230_result.md  = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR229_result.md  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR216_result.md  = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR219_promoted_particle_rows_126.csv = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
CR231_PRECOMMIT.md = b94a48033a4e803917ea554fa1ffbba72578d11dc32d4bad9be0ef9e3775c8ed
```

## Interpretation

CR230 established that the substrate's structural number set `{126, 81, 81, 162, 27}` is derivable from `{R, D, α_H}` alone via a 9-step algebraic chain. A skeptic could still ask:

> *Even if the algebra closes, maybe ANY arrangement of comparable partition values across 139 rows would produce these specific closures — the closure is in the algebra, not in the actual row identifications.*

CR231 forecloses that objection at `p = 0.000300` (uniform null) / `p = 0.000200` (marginal-preserving null):

- The 12-support-roster sum hits 81 in only **2.51%** of random permutations.
- The mirror position hits 81 in only **0.70%** (matching the 1/139 baseline since there is exactly one `81` in the multiset).
- The joint event hits in only **0.03%** of permutations.

The canonical row identifications — not the row ordering — carry the structural pattern. The mirror's 81 must specifically land on QP093A-0303, AND the 12 support roster IDs must hold partition values summing to exactly 81. Random reassignment breaks this `~3000:1` of the time.

## Honest Notes

1. **T1 and T4 are mathematically equivalent under integer arithmetic** (write_rate_x_R = support_sum × 4; equals 324 iff support_sum = 81). They are not independent targets; the precommit's "four targets" reduces to two effective Bernoulli events plus two derived. This was not anticipated in the precommit, but it does not change the verdict: the joint hit rate `2/10000` remains the primary evidence.

2. **T2 = 0.0070 ≈ 1/139 = 0.00719**: under a uniform permutation, the probability that the unique `81` lands at the mirror position is exactly 1/139. The observed empirical rate matches the analytic baseline within Monte Carlo noise, which is a runner-correctness check.

3. **Marginal-preserving with replacement allows duplicate `81` labels** — yet still hit rate 1/10000. This is consistent with: the joint event needs BOTH support_sum=81 AND a specific value at the mirror; replacement only weakly affects support_sum statistics.

4. **The precommit was sealed in a low-budget session** with the shuffle design, targets, pass conditions, and wrong controls fixed before any data run. The runner inherited a frame it could not tune. This is K3 (target hygiene) discipline at work.

## Sequence in the Seven-Test Arc

CR231 is **Test 2 of 7**. Tests 3-7 remain:

- CR232 (Test 3): Matter/support promotion gate audit
- CR233 (Test 4): 18 / 81 / 27 tensor-substrate role-separation test
- CR234 (Test 5): Blind SOB element engine (Z + constants only)
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.

## Rule of Immutability

Sealed 2026-06-22 by Sean Brady. Inputs hash-locked. Precommit frame, seeds (`20260622`, `20260623`, `20260624`, `20260625`), runner, and the empirical distributions are frozen.

If `CR219_promoted_particle_rows_126.csv` is later regraded or supersedes its current SHA, this CR must be re-examined.

---

**Sealed by:** Sean Brady, 2026-06-22
**Runner verified:** All 4 targets hit on canonical; 2/10000 uniform hits; 1/10000 marginal hits; WC1 0/10000; WC2 0/10000
**Arc position:** Test 2 of 7 (statistical confirmation that CR230's structural closure is not editorial)
