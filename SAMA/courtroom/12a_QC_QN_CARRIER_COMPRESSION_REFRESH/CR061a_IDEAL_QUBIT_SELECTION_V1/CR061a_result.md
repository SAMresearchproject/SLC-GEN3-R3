# CR061a Ideal Qubit Selection within 3-Body Standard Letter Tier v1.0

## Verdict

```text
CR061a_IDEAL_QUBIT_SELECTION_V1_SEALED
```

## The Two Locked Ideal Qubit Candidates

| partition | sorted (a,b,c) | M_native (MeV) | S_debit predicted (MeV) | structural form |
|---|---|---:|---:|---|
| 1+2+4 | (1,2,4) | 756 | 0.464844 | (alpha_H^0, alpha_H^1, alpha_H^2) |
| 2+4+8 | (2,4,8) | 3024 | 1.859375 | (alpha_H^1, alpha_H^2, alpha_H^3) |

Both ideal candidates are **pure α_H ladders**: successive powers of α_H = 2 in the three slots.  They form a **two-generation hierarchy** within the q = 0 subset of the 3-body standard letter tier, with the heavier candidate at α_H² × the lighter candidate's mass.

## The Three Selection Filters

```text
Filter 1: q_abs == 0       (so S_debit = (17/16)*M/R^3 with the
                            (1/4 + 9/16 + 1/4) slot decomposition)
Filter 2: a != b != c      (carrier, envelope, sensor must be
                            structurally separable identities)
Filter 3: promoted in CR060a (not REJECTED_FAKE_CLOSURE)
```

## Filter Cascade

| stage | count | filter |
|---|---:|---|
| Promoted 3-body standard letter (from CR060a) | 107 | (alphabet tier) |
| ... AND q_abs = 0                              | 17 | F1 |
| ... AND all-distinct slots                      | **2** | F1 + F2 + F3 |

Exactly **two** rows pass all three filters.

## Slot Role Map (Locked, q = 0 only)

```text
                  1     9   1     1               17
  S_debit(q=0) = (- + (-*-) + -) * M / R^3  =  (--) * M / R^3
                  4     8 2   4               16

  Slot a (outer, weight 1/4 )  ->  CARRIER  (route identity)
  Slot b (middle, weight 9/16) ->  ENVELOPE (letter content)
  Slot c (outer, weight 1/4 )  ->  SENSOR   (boundary stress)

  For (1, 2, 4):  CARRIER = alpha_H^0,  ENVELOPE = alpha_H^1,  SENSOR = alpha_H^2
  For (2, 4, 8):  CARRIER = alpha_H^1,  ENVELOPE = alpha_H^2,  SENSOR = alpha_H^3
```

## Why These Two and Not Others

- **q_abs ≥ 1** rows in the 3-body standard letter tier (90 of the 107) have an S/M coefficient (4q+D)/(4R) that does NOT decompose into (1/4 + 9/16 + 1/4) — so the carrier/envelope/sensor architectural mapping fails to fit cleanly.  Architectural ideality requires q = 0.
- **Repeated-slot rows** (15 of the 17 q=0 rows; e.g. (1,1,3), (2,2,3), (4,4,9)) collapse two of the three architectural roles into one identity, breaking the separation in CR051.
- **REJECTED rows** are filtered out by alphabet membership (CR060a).

Only **(1, 2, 4) and (2, 4, 8)** pass all three filters.  Both happen to be pure α_H ladders — that's an observed *consequence* of the structural-ideality criteria, not a separate axiom.

## Forward-Blind Sub-Prediction CR061a_PRED_1 (LOCKED)

**Claim:** Any future 3-body standard-letter row satisfying all three filters (q=0, distinct slots, promoted) carries S_debit = (17/16)·M/R³ with positive sign (per CR129b) and qualifies as an ideal Paul Revere qubit.

**Falsifier:** (a) such a row whose S_debit deviates from (17/16)·M/R³ kills the slot decomposition; (b) discovery of a non-α_H-ladder all-distinct triple at q=0 with promoted status would *extend* (not falsify) the candidate set.

**Non-falsifying:** additions to q≥1 or repeated-slot subsets; hardware demonstrations.

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR060a_alphabet_csv                       = 33f5c1f05bb23a69556d9c68f219a2515ddcd394c0310c85b5427e25bc341cdd
CR060a_alphabet_lock_json                 = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR129b_magnitude_lock_json                = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd

CR061a_screening_table_csv                = 589717e5d1a247eb599cb5ecf418ab497b50a5c08ee908e2c4e03038873012f1
CR061a_qubit_candidates_csv               = c2d4477060563a12e14cb967a9f1ff1d5be933aba88228dcddb991abbeec84b1
CR061a_selection_lock_sha256              = 3b1dae5922ab80e76a19c2ccac8afa2066e3fa6f2bb6355673abf84fac6d23e7
```

## Predictions Checks

- **[PASS]** P1_107_promoted_3body_rows_walked -- 3body_standard promoted rows = 107
- **[PASS]** P2_seventeen_q0_rows -- q=0 rows = 17
- **[PASS]** P3_two_ideal_candidates_selected -- q=0 AND all-distinct = 2 (expected 2: (1,2,4) and (2,4,8))
- **[PASS]** P4_both_candidates_are_alpha_H_ladders -- alpha_H ladder count = 2 / 2
- **[PASS]** P5_lighter_candidate_is_1_2_4 -- lightest candidate: (1,2,4) at M = 756 MeV
- **[PASS]** P6_selection_lock_written -- selection lock sha256 = 3b1dae5922ab80e76a19c2ccac8afa2066e3fa6f2bb6355673abf84fac6d23e7

## Wrong Controls

- **[PASS]** WC1_CR060a_alphabet_unmodified -- CR060a alphabet read-only; CR061a filters subset without reclassifying.
- **[PASS]** WC2_CR119_catalog_unmodified -- CR119 read-only.
- **[PASS]** WC3_no_hardware_claim -- CR061a is a structural-ideality selection at the protocol layer; no hardware claim made.
- **[PASS]** WC4_other_qubit_candidates_NOT_excluded_as_non_qubits -- Rows that fail one or more filters (q >= 1, repeated slots) are NOT claimed to be non-qubits.  They are claimed to lack STRUCTURAL IDEALITY in the carrier/envelope/sensor mapping.  They may still function as qubits with degraded architectural cleanliness.
- **[PASS]** WC5_alpha_H_ladder_observation_NOT_axiomatic -- The fact that both candidates are pure alpha_H ladders is an OBSERVATION from the filter outcome, not an axiom.  CR061a does not impose 'alpha_H ladder' as a fourth filter; it notes that the structural-ideality filters happen to select only alpha_H-ladder triples.
- **[PASS]** WC6_S_debit_predictions_use_CR129b_locked_formula -- S_debit = (17/16) * M / R^3 is the locked q=0 formula from CR129b.  CR061a uses it directly; predictions are not new claims.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED.
- CR062a: Paul Revere protocol sharpening with the (1/4, 9/16, 1/4) slot weights -- refine CR054's 7 correction rules using the locked ideal qubits.
- CR063a: hardware translation document -- which physical platforms can realize (1,2,4) and (2,4,8)?
- CR064a: coherence-ladder vs threshold-theorem comparison (1/12 = A_share vs ~1% fault tolerance threshold).
- Mass-to-frequency calibration: how do 756 MeV and 3024 MeV translate to physical qubit splitting frequencies?
- First-principles derivation of why structural ideality selects pure alpha_H ladders is open.

## Rule of Immutability

Selection criteria, slot role map, and the two locked ideal candidates are frozen at CR061a seal time.  Future falsification or extension must be in an appeal CR within 12a.
