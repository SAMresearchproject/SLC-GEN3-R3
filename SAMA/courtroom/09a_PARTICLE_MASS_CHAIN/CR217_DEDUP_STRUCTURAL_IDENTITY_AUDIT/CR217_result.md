# CR217 Dedup Structural Identity Audit

Result: **CR217_PASS_DEDUP_STRUCTURAL_IDENTITY_AUDIT__162_EQ_R2_NINE_EIGHTHS__163.4652778_EQ_162_PLUS_211_OVER_144__PHOTON_FALSIFIER_HOLDS__BACKED_ARITHMETIC_NOT_DERIVED_MECHANISM**

## Direct Answer

After CR216 retired the photon/A-field duplicate, the partition and mass
columns of CR214's complement bin close into a clean structural identity:

```
99 + 45      = 144 = R^2
            +18  = R^2 / 8         (graviton = R^2 * 2^-D at D=3)
TOTAL    = 162 = R^2 * (9/8)
```

```
MASS = PARTITION + 211/R^2
163.4652778 = 162 + 211/144
```

CR217 verifies every sum, ratio, and per-row lift directly from sealed
inputs in exact rational arithmetic. All 25 identity checks pass. All 5
carriers match expected values. All 8 hidden-source rows satisfy the lift
formula `m(p) = p + p^2/R^2` to within sealed-string rounding tail
(differences ≤ 1e-98).

## Honest Framing

This CR establishes that the dedup'd 194-row complement carries a clean
arithmetic identity tied to `R^2 = 144`, `D = 3`, and the ratio `9/8`. It
does *not* derive the identity from a deeper law. Specifically:

- The hidden-source p-value set `{1,2,3,4,6,8,9,12}` is what CR119's
  sealed enumerator produced. CR217 verifies the algebra on this set; it
  does not derive the set.
- `R^2 = 144` is a sealed constant imported from upstream (SAMs_TOE
  glossary, CR213, CR214). CR217 uses it; it does not justify it.
- The structural narrative — "closed loop on the gauge-boson side plus
  bigrade lattice on the source side plus carrier release on top" — is a
  scientific reading consistent with the arithmetic. It is not
  independently tested in CR217.

The audit-appeal posture is the standard CR214 idiom: tested arithmetic
on sealed inputs, honest about what is observed vs. derived. The
identities are strong on a bad day because they are closed-form
rationals on hash-anchored data, not fits or approximations.

## Input Verification

All seven sealed inputs re-hashed at runtime. All matches confirmed.

| Input | Sealed sha256 head | Match |
|---|---|---|
| `CR214_particle_complement_195.csv`           | `e41016b5...` | yes |
| `CR215_numeric_duplicate_groups.csv`          | `8d8f0461...` | yes |
| `CR216_particle_complement_194_active.csv`    | `01e780c0...` | yes |
| `CR216_retirement_ledger.csv`                 | `c85b1b76...` | yes |
| `CR060a_result.md`                            | `4ac273e8...` | yes |
| `CR066a_runner.py`                            | `3672beb2...` | yes |
| `LC11_formula_manifest.csv`                   | `a0c3eb03...` | yes |

## The 5-Row Carrier Block (after dedup)

| candidate_id | role | operator_class | partition | M_native |
|---|---|---|---:|---:|
| QP093A-0300 | graviton | TENSOR_CARRIER | 18 | 18 |
| QP093A-0301 | photon | ROAD_LIGHT_CARRIER | 1 | **0** |
| QP093A-0302 | W | WEAK_VECTOR_CARRIER | 9 | 9 |
| QP093A-0303 | Z | NEUTRAL_VECTOR_CARRIER | 81 | 81 |
| QP093A-0304 | gluon | COLOR_OWNER_CARRIER | 8 | 8 |

Sum check: partition `18+1+9+81+8 = 117`. Mass `18+0+9+81+8 = 116`.
Difference exactly 1, entirely due to the photon row (partition 1, mass 0).

## The 8-Row Hidden-Source Block (lift formula `m(p) = p + p^2/R^2`)

| candidate_id | p | expected `m(p)` | observed M_native | match |
|---|---:|---|---|:---:|
| QP093A-0306 | 1  | 145/144  = 1.00694...    | sealed value matches to 1e-100 | ✓ |
| QP093A-0307 | 2  | 73/36    = 2.02777...    | sealed value matches to 1e-100 | ✓ |
| QP093A-0308 | 3  | 49/16    = 3.0625        | sealed value matches to 1e-99  | ✓ |
| QP093A-0309 | 4  | 37/9     = 4.11111...    | sealed value matches to 1e-100 | ✓ |
| QP093A-0310 | 6  | 25/4     = 6.25          | sealed value matches to 1e-99  | ✓ |
| QP093A-0311 | 8  | 76/9     = 8.44444...    | sealed value matches to 1e-99  | ✓ |
| QP093A-0312 | 9  | 153/16   = 9.5625        | sealed value matches exactly   | ✓ |
| QP093A-0313 | 12 | 13       = **13.00000…** | sealed value matches exactly   | ✓ |

The `p = R` landmark holds: for `p = 12 = R`, the lift is exactly `R^2/R^2 = 1`, so `m(R) = R + 1 = 13`. The sealed row reads M_native = 13.0000…, which is what CR214 published before any of this analysis existed.

Sum checks (exact rationals): partition `Σp = 45`, mass `Σ(p + p^2/144) = 45 + 355/144 = 6835/144 ≈ 47.4653`.

## Structural Identities (all PASS)

| Identity | Form | Value |
|---|---|---|
| Closed loop | `99 + 45 = R^2` | `144` ✓ |
| Carrier release | `graviton / R^2 = 1/8 = 2^-D` at D=3 | `18/144 = 1/8` ✓ |
| Closed loop + carrier release | `total_partition / R^2 = 9/8` | `162/144 = 9/8` ✓ |
| 9/8 form 1 (additive) | `1 + 2^-D` at D=3 | `9/8` ✓ |
| 9/8 form 2 (LC11 bounce lift) | `D^2 / 2^D` at D=3 | `9/8` ✓ |
| Hidden Σp² (full) | `1+4+9+16+36+64+81+144` | `355` ✓ |
| Hidden Σp² (sub-R) | `1+4+9+16+36+64+81` | `211` ✓ |
| Mass excess over partition | `total_mass − total_partition` | `211/144` ✓ |
| Total mass | `162 + 211/144 = 23539/144` | ≈ 163.4652778 ✓ |

## The 9/8 Cross-Reference

The ratio `9/8` is not novel here. It is already sealed in three
independent courtroom contexts:

- **CR060a Paul Revere alphabet** (sha256 `4ac273e8...`):
  *"Middle-slot 9/8 surcharge on its 1/2 weight = the LETTER CONTENT itself."*
  The 9/8 is the multiplicative surcharge that turns the middle slot's
  base weight 1/2 into 9/16.
- **CR066a Born extension** (sha256 `3672beb2...`):
  *"The 9/8 SURCHARGE on the middle slot turns 1/2 into 9/16."*
  Same ratio, propagated into the Born-rule extension.
- **LC11 black hole horizon thermodynamic replay** (sha256 `a0c3eb03...`):
  formula manifest entry `bounce lift, D^2/2^D, D=3, 9/8, locked primitive stack`.

CR217 finds the same ratio sitting in `total_partition / R^2` on the
dedup'd particle complement. This is recorded as four independent sealed
appearances of `9/8` in distinct domains (alphabet lock, Born extension,
black-hole horizon, particle complement). It is not promoted to a
unified derivation. A unified derivation would be a follow-up CR.

## Photon Falsifier (explicitly embedded)

The closed-form identity `163.4652778 = 162 + 211/144` depends critically
on the photon contributing exactly `+1` to the carrier partition sum
while contributing `0` to the carrier mass sum. If CR119 ever re-grades
the photon row away from `(partition=1, M_native=0)`, the identity
breaks. CR217 tests this directly:

| Falsifier condition | Observed | Pass |
|---|---|:---:|
| `photon_row.partition == 1` | 1 | ✓ |
| `photon_row.M_native == 0` | 0 | ✓ |
| `carrier_partition_sum − carrier_mass_sum == 1` | 117 − 116 = 1 | ✓ |

All three hold. Any future failure here is a loud, immediate signal that
the entire closed-form identity needs to be revisited.

## Pass Conditions

25 of 25 checks passed. Execution status: CLEAN.

See `CR217_identity_checks.csv` for the full per-check ledger.

## What is BACKED, what is OPEN, what is NOT CLAIMED

### BACKED (closed-form arithmetic on sealed inputs)

- `99 + 45 = 144 = R^2` on the dedup'd active 194-row complement.
- `graviton partition / R^2 = 2^-D` at D=3.
- `total_partition / R^2 = 9/8` exactly.
- `total_mass − total_partition = 211/144` exactly.
- Per-row lift `m(p) = p + p^2/R^2` holds for every hidden-source p in
  `{1,2,3,4,6,8,9,12}` to within sealed-string rounding tail.
- Three sealed prior appearances of `9/8` (CR060a, CR066a, LC11).
- The photon falsifier conditions all hold.

### OPEN (count match worth follow-up)

- Four independent sealed appearances of `9/8` in distinct courtroom
  domains. CR217 records the convergence; it does not derive a unifying
  law.
- The hidden-source partition set `{1,2,3,4,6,8,9,12}` has internal
  structure (the divisors of 12 plus 8 and 9) that may admit a closed
  combinatorial description. CR217 does not test that.

### NOT CLAIMED

- That the structural narrative ("closed loop + bigrade lattice +
  carrier release") is independently derived. It is a scientific
  reading consistent with the arithmetic; it is not tested as a
  mechanism in this CR.
- That the carrier_only bin "is" exactly the SM+gravity gauge bosons
  in a model-theoretic sense. The five rows happen to map cleanly onto
  graviton/photon/W/Z/gluon by partition signature and spin class. CR217
  does not promote that mapping to a uniqueness claim.

## Artifacts

- `CR217_PRECOMMIT.md`
- `CR217_declared_premises.json`
- `CR217_runner.py`
- `CR217_input_manifest.csv`
- `CR217_carrier_block.csv`
- `CR217_hidden_source_block.csv`
- `CR217_identity_checks.csv`
- `CR217_summary.json`
- `HASHES.txt`

## Chain of Custody

CR119 → CR214 → CR215 (identified the duplicate) → CR216 (retired QP093A-0305
under documented tiebreak rule) → CR217 (verified the dedup'd identities
on closed-form arithmetic).

All upstream artifacts referenced by sha256. CR217 modifies nothing.
