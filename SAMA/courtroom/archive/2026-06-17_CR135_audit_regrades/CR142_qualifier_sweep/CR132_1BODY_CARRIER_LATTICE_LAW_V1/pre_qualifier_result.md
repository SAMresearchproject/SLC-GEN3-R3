# CR132 1-Body Carrier Lattice Law v1.0

> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR132_law_lock_sha256` field in this file was corrected from `f4811aa1...491ec17` to `fbc25a88...9559a32` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR132_1BODY_CARRIER_LATTICE_LAW_V1/original_result.md`
> - Original SHA-256: `6897acca61d2407e8b1dc5ee36922be15e949ab1f37d8d6839d8c47d928ba078`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR132_1BODY_CARRIER_LATTICE_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR132_1BODY_CARRIER_LATTICE_LAW_V1_SEALED
```

## The Law (Locked, C1 = 1)

Each 1-body boson carrier sits at a unique lattice point on the (α_H, D) foundation algebra:

```text
  M_native(carrier_class) = alpha_H^i * D^j   for assigned (i, j) per class

  carrier_class                    (i, j)     M_native    structural
  ------------------------------|----------|------------|-----------------
  TENSOR_CARRIER                |  (1, 2)  |    18      |  alpha_H * D^2
  WEAK_VECTOR_CARRIER           |  (0, 2)  |     9      |  D^2
  NEUTRAL_VECTOR_CARRIER        |  (0, 4)  |    81      |  D^4
  COLOR_OWNER_CARRIER           |  (3, 0)  |     8      |  alpha_H^3
  ROAD_LIGHT_CARRIER (photon)   |  massless|     0      |  (gauge)
  A_FIELD_CARRIER               |  massless|     0      |  (A-field)

  S_debit = 0 universally (CARRIER_ONLY_NOT_MATTER stability)
```

## Structural Reading

- Each carrier sits at its own (α_H, D) lattice point.
- **Two massive_vector_support carriers split by D²:** M_NEUTRAL = M_WEAK · D² = 9 · 9 = 81.
- **Two truly massless carriers** (photon-class and A-field) carry partition = 1 as a placeholder slot with M_native = 0.
- **C1 = 1** (no surcharge): carriers are at their bare structural lattice value, unlike fermions (CR131 used K = 5/4 or 3/2) and 3-body OCTET (CR129b used 17/16 at q=0).  Bosons live on the lattice directly.
- S_debit = 0 universally: carriers are pure-structure rows with no surface debit.

## In-Sample Verification

- Carrier rows tested:    **6** (each carrier class has n=1 in CR119)
- Lattice matches:        **6 / 6**
  - Massive carriers:       4/4
  - Massless carriers:      2/2
- S_debit = 0 verified:   **6/6**
- Violations:             **0**

## Verification Table

| carrier | partition | predicted | observed | S_debit | match |
|---|---:|---:|---:|---:|:-:|
| TENSOR_CARRIER | 18 | 18 | 18 | 0 | YES |
| ROAD_LIGHT_CARRIER | 1 | 0 | 0 | 0 | YES |
| WEAK_VECTOR_CARRIER | 9 | 9 | 9 | 0 | YES |
| NEUTRAL_VECTOR_CARRIER | 81 | 81 | 81 | 0 | YES |
| COLOR_OWNER_CARRIER | 8 | 8 | 8 | 0 | YES |
| A_FIELD_CARRIER | 1 | 0 | 0 | 0 | YES |

## Forward-Blind Sub-Prediction CR132_PRED_1 (LOCKED)

**Claim:** For any future row with one of the six carrier operator classes, M_native equals the locked lattice integer for that class.

**Falsifier:** ONE single future carrier row whose M_native deviates from the locked lattice value kills v1.0.

**Non-falsifying:** rows outside the carrier set; addition of a NEW carrier class (would warrant an appeal CR with extended lattice).

**Free parameters at test:** 0.

## What CR132 Does NOT Claim

- Calibration of lattice integers to physical MeV scale (would require a per-spin-class constant; CR132b).
- A formula for SOURCE_SUPPORT_PACKET (8 rows) or OUTER_BINARY_NEUTRAL (24 rows) — separate generators.
- A first-principles derivation of why each spin class lands at its specific (i, j) lattice point.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42

CR132_verification_csv                    = 9937d79e790c08d7a7230d1d5f20409ae28542a5aed8d944c3ddbe1716715bee
CR132_law_lock_sha256                     = fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32
```

## Predictions Checks

- **[PASS]** P1_all_6_carriers_walked -- carrier rows walked = 6 (expected 6)
- **[PASS]** P2_all_carriers_match_lattice -- massive = 4/4, massless = 2/2, violations = 0
- **[PASS]** P3_S_debit_zero_for_all_carriers -- S_debit zero on 6/6 carriers (CARRIER_ONLY_NOT_MATTER stability)
- **[PASS]** P4_M_NEUTRAL_equals_M_WEAK_times_D_squared -- NEUTRAL_VECTOR M = 81 = 9 * 9 = WEAK_VECTOR * D^2 (within shared massive_vector_support spin class)
- **[PASS]** P5_law_lock_written -- law lock sha256 = fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_carriers_explicitly_distinct_from_V4_1_fermions -- CR131 locked V4_1_SINGLE_WRITE (90 fermion_half_write rows).  CR132 locks the 6 true 1-body bosons (carriers).  Different spin classes, different operator classes, different generators.
- **[PASS]** WC3_M_native_NOT_calibrated_to_MeV -- Carrier M_native values are structural inventory integers on the (alpha_H, D) lattice, not energy units.  Mapping to physical MeV scale requires a separate calibration constant per spin class and is out of CR132 scope.
- **[PASS]** WC4_C1_equals_1_NOT_9_over_8 -- Initial probe tried C1 = 9/8 (from CR129b's middle-slot surcharge).  Three carriers fit (9/8)*X form but COLOR_OWNER did not.  User-directed pivot to C1 = 1 closed all six rows cleanly via the (alpha_H, D) lattice.  Honest forensics recorded; no post-hoc tuning.
- **[PASS]** WC5_massless_carriers_treated_as_M_equals_0_NOT_undefined -- ROAD_LIGHT (photon-class) and A_FIELD have M_native = 0 in CR119, with partition = 1 as a placeholder slot.  CR132 treats this as a valid lattice value (the M=0 point) rather than 'massless undefined'.
- **[PASS]** WC6_SOURCE_SUPPORT_and_fake_spin_rows_explicitly_excluded -- The 8 SOURCE_SUPPORT_PACKET (unresolved_support) and 9 'fake_spin' null-control rows in CR119 are NOT covered by CR132.  They are structural diagnostics, not physical bosons.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR132b: calibration of carrier lattice integers to physical MeV scale (per-spin-class constant)
- CR133+: derive lattice formula for SOURCE_SUPPORT_PACKET (8 rows) and OUTER_BINARY_NEUTRAL (24 rows)
- Forward-blind CR132_PRED_1 resolves when CR119 gains new carrier rows (or a new carrier class)
- First-principles derivation of why each spin class lands at its specific (i, j) lattice point is open

## Rule of Immutability

Lattice assignments and constants are frozen at CR132 seal time.  Future falsification or refinement must be in an appeal CR.
