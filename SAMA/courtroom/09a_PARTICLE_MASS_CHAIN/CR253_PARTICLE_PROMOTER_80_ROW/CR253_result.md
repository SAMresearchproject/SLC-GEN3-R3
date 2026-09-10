# CR253 — Particle Promoter (80-Row Stable Matter Set) — RESULT

```text
verdict           : BOUNDARY (core finding EXACT; 2 of 4 binary wrong-controls
                              not sensitive due to upstream filter subsumption)
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461
catalog_hash      : 33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c
runner_hash       : 81fcf14e75966c516eb34fd92cf8b32e91f776e718c359354543bed56b9b3b3e
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

**The promoter produces exactly 80 rows. The 48/32 matter/antimatter
split is exact. Conjugate parity closes 32/32. The class-by-class
breakdown matches the 7 pre-registered substrate-natural classes
row-for-row.**

Two of the four binary wrong-controls (W3 dropping bigrade
q-rule, W4 allowing `I_T > 0`) return the same 80 rows as canonical
— but **this is structural sensitivity surfacing, not a failure**.
The `bin ∈ {stable_matter, antimatter_conjugate}` and
`h_T ∈ {0, 1}` filters already exclude any row that would gain entry
under those relaxations. W3 and W4 are redundant given the other two
filters.

The statistical wrong-control W5 (random bin permutation, 1000 trials)
reproduces 80 rows in **0 / 1000** trials. p < 0.001.

Per the pre-registered verdict tree, BOUNDARY because the W1–W4
sensitivity condition fails on W3 and W4. The core promoter finding
itself is PASS-grade.

## Verdict conditions

| condition | observed | verdict |
| --- | --- | --- |
| (1) exactly 80 rows | 80 / 80 | PASS |
| (2) 48 / 32 matter / anti split | 48 / 32 | PASS |
| (3) 32 / 32 conjugate parity | 32 / 32 | PASS |
| (4) class breakdown exact across 7 classes | 7 / 7 | PASS |
| (5) W1, W2, W3, W4 all sensitive | W1 ✓, W2 ✓, W3 ✗, W4 ✗ | **FAIL** |
| (6) W5 p < 0.05 random bin permutation | 0 / 1000 < 0.05 | PASS |

Verdict per tree: BOUNDARY (condition 5 fails but no row-count delta
and no parity break).

## Class-by-class breakdown — 7 / 7 match

| class | matter obs / exp | anti obs / exp |
| --- | ---: | ---: |
| electron_like_minus | 1 / 1 | 1 / 1 |
| positron_substrate_slot | 1 / 1 | 1 / 1 |
| heavier_charged_lepton_minus | 1 / 1 | 1 / 1 |
| heavier_positron_substrate_slot | 1 / 1 | 1 / 1 |
| neutrino_like | 2 / 2 | 0 / 0 |
| quark_like_charged | 28 / 28 | 28 / 28 |
| neutral_higher_partition | 14 / 14 | 0 / 0 |
| **TOTAL** | **48 / 48** | **32 / 32** |

Zero unclassified rows. Zero off-class assignments.

## Wrong controls (with structural reading)

| control | rows | expected | verdict |
| --- | ---: | ---: | --- |
| W1 (include bound_composite_rows in B_allowed) | **116** | ≠ 80 | sensitive ✓ |
| W2 (include h_T = 2 in H_allowed) | **105** | ≠ 80 | sensitive ✓ |
| W3 (drop bigrade q-rule, allow q ∈ [0, 12]) | 80 | ≠ 80 | **NOT sensitive** |
| W4 (allow I_T > 0) | 80 | ≠ 80 | **NOT sensitive** |
| W5 random bin permutation, 1000 trials | 0 / 1000 = p < 0.001 | < 0.05 | sensitive ✓ |
| W5 null mean count | 41.25 | reference only | — |

### Why W3 and W4 are not sensitive

The pre-registered Q_allowed set is `{0, 1, 2, 3, 4, 6, 8, 9, 12}`.
Q_allowed_relaxed for W3 is `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}`.
The catalog's `stable_matter_rows` and `antimatter_conjugate_rows` bins
contain **no rows with q ∈ {5, 7, 10, 11}** at `h_T ≤ 1`. So dropping
the bigrade restriction doesn't admit any new rows — they don't exist
in the catalog at that depth and bin.

For W4: the canonical bigrade q-rule combined with the connection
rule (any v_j ∈ T13 that divides q OR p) guarantees `I_T = 0` for any
row with q in the bigrade alphabet. The bin and h_T filters already
ensure all surviving rows have q ∈ bigrade. So requiring `I_T = 0`
does no additional filtering after the bin+h_T+q filters apply.

**Structural conclusion**: the four pre-registered filters
`(I_T = 0, h_T ∈ {0,1}, q ∈ bigrade, bin ∈ matter/anti)` are NOT
independent. The bin + h_T pair subsumes the q-bigrade and I_T
conditions on this catalog. The minimal sufficient set is
`(bin, h_T)`.

This is a structural finding worth documenting. It does not weaken
the promoter — the SAME 80 rows are produced. It tightens the rule:
`(bin ∈ {stable_matter, antimatter_conjugate}) AND (h_T ∈ {0, 1})`
is the necessary-and-sufficient promoter rule on this catalog.

### W5 is the load-bearing statistical wrong-control

W5 (random bin permutation, 1000 trials) is the only statistical
wrong-control in the precommit. Per the methodology memory
(`feedback_wrong_control_methodology`), statistical wrong-controls
score canonical against the null distribution.

- Canonical: 80 rows
- Null mean under bin shuffle: 41.25 rows
- Trials reproducing canonical exactly: 0 / 1000
- p < 0.001

This is the rigorous wrong-control. The bin assignment in QP093A IS
load-bearing for the 80-row count.

## Provenance chain (HASHES.txt)

```text
33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c  CR253_input_catalog_299.csv
a7ecd0a4718c3cda2252d44faceb33f72fdc1214679630a722d354a7d47f5461  CR253_PRECOMMIT.md
81fcf14e75966c516eb34fd92cf8b32e91f776e718c359354543bed56b9b3b3e  CR253_runner.py
(result hash recorded in HASHES.txt sibling file)
```

## What this CR seals for downstream consumption

The **80-row stable matter set** is now CR-class. Branch 09a particle
identity work that previously consumed the QP106 80-row signatures
table can now reference this CR's `CR253_promoted_80_rows.csv` with
full hostile-environment provenance.

The minimal sufficient promoter rule is:

```text
promoted(r) iff (bin(r) ∈ {stable_matter_rows, antimatter_conjugate_rows})
            AND (h_T(r) ∈ {0, 1})
```

(The q-bigrade and `I_T = 0` filters are redundant given those two.)

The seven substrate-natural identity classes (electron-like,
positron-substrate-slot, heavier-charged-lepton, heavier-positron,
neutrino-like, quark-like-charged, neutral-higher-partition) provide
the matter-sector taxonomy.

## Out of scope (NOT addressed by this CR)

- T13 partition sum verification (documented at Section 4.3 + QP102)
- Compact substrate laws for q_A generation (QP108-QP110; pending CR)
- A-operator antimatter conjugate transform (QP109; pending CR)
- A meets Θ at d=1 (QP112; pending CR)
- PDG-named particle assignment

## Verdict statement

**CR253 BOUNDARY.** The 80-row stable matter set is structurally
sound. The promoter rule's exact-match outcome on row count,
matter/anti split, conjugate parity, and class breakdown is PASS-grade.
The BOUNDARY tag reflects the discovery that two of four binary
wrong-controls were redundant — a methodological finding about the
rule's filter structure, not a content failure.

The minimal sufficient promoter rule is `(bin AND h_T)`; the q-bigrade
and I_T conditions are downstream consequences on this catalog.

`80_ROW_STABLE_MATTER_SET_EXACT_48_32_SPLIT_32_32_PARITY_CLASS_BREAKDOWN_EXACT_W5_p_LT_0_001_W3_W4_REDUNDANT_DUE_TO_BIN_AND_h_T_SUBSUMPTION`
