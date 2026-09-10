# CR217 Dedup Structural Identity Audit

## Task

After the CR215/CR216 carrier dedup, the active 194-row complement carries
five gauge-boson carriers (graviton, photon, W, Z, gluon), eight
hidden-source bigrade rows, and the rest of the gate residue. CR217 tests
whether the partition and mass columns close into the structural identity
SeanBrady wrote up in
`09a_PARTICLE_MASS_CHAIN/SEANBRADY_195_PARTICLE_INSPECTION.md`:

    99 + 45 = 144 = R^2
    162   = R^2 * (1 + 2^-D)  at D=3, i.e. R^2 * (9/8)
    163.4652778 = 162 + 211/144

CR217 verifies these identities by recomputing every sum, ratio, and
per-row lift directly from sealed sheets. It does not assert any of them
as a derivation; it tests whether the dedup'd data sums close to them.

## Honest Framing

CR217 makes three claims and explicitly does not make a fourth:

- CLAIM 1 (testable): the carrier+graviton partition sum is exactly 117.
- CLAIM 2 (testable): the hidden-source bigrade partition sum is exactly 45.
- CLAIM 3 (testable): 99 + 45 == 144, and 18/144 == 1/8, and 162/144 == 9/8.
- NOT A CLAIM: that any of these identities are *derived* from a deeper
  law inside CR217. The hidden-source p-value set {1,2,3,4,6,8,9,12} is
  what CR119's sealed enumerator produced; CR217 verifies the algebra
  given that set, it does not derive the set.

This is the audit-appeal posture: tested arithmetic on sealed inputs,
honest about what is observed vs. derived.

## Origin

The numeric duplicate identified in CR215 and retired in CR216 was
inflating carrier_only_rows from 5 to 6 and adding a +1 partition and a
+1.0069... mass to the totals. With the dedup applied, the sums
collapse to clean structural values consistent with three other sealed
courtroom artifacts that already carry the ratio 9/8 as a primitive.

## Classification

Audit. CR217 does not regrade CR119, CR132, CR124, CR060a, CR066a, LC11,
CR214, CR215, or CR216. It reads their sealed surfaces as evidence and
emits a verdict on the dedup'd active 194-row complement.

## Inputs (all hash-verified at runtime)

- `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv`
  sha256 `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`
- `09a_PARTICLE_MASS_CHAIN/CR215_CR214_CARRIER_NUMERIC_DUPLICATE_AUDIT/CR215_numeric_duplicate_groups.csv`
  sha256 `8d8f0461d2e54df89a57cc1d16a886efa792fa8b900c38b0c083c717bc8d8f98`
- `09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/CR216_particle_complement_194_active.csv`
  sha256 `01e780c0fbb315d0aaf93cc6b060ffc4c9cfd0da29ab7155b4da8ca40d444179`
- `09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/CR216_retirement_ledger.csv`
  sha256 `c85b1b766435c33504ad6004f44f9aef35cf95614a78216f164b3d9ab0647610`
- `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1/CR060a_result.md`
  sha256 `4ac273e8ca5539876886550590cdf7d81b776108fdef1ed9eba1adf8105d6ee8`
- `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1/CR066a_runner.py`
  sha256 `3672beb257ea228c7f991bb33922db3e060e445a55a3238a113f7804149e24c7`
- `16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_formula_manifest.csv`
  sha256 `a0c3eb030a7b55edf0b4fc5a28788a6560e323a4ab17611667979b917dba8069`

## Sealed Constants Carried In (not derived)

- `R = 12`, `R^2 = 144` (defined in upstream tests including SAMs_TOE
  glossary, CR213, CR214).
- `D = 3` (closure_depth column on every carrier and hidden_source row
  reads 3).
- `9/8` already appears as a sealed primitive in three contexts:
  - CR060a Paul Revere alphabet: middle-slot 9/8 surcharge on its 1/2
    weight, turning 1/2 into 9/16.
  - CR066a Born extension: same 9/8 SURCHARGE on the middle slot.
  - LC11 black hole horizon: `bounce lift = D^2/2^D = 9/8 at D=3`,
    locked primitive stack.

CR217 cites these as existing seal points but does not redefine them.

## Pass Conditions

### Per-row arithmetic on the active 194-row sheet

- Carrier_only_rows after dedup has exactly 5 members.
- Carrier candidate_ids are exactly:
  - QP093A-0300 TENSOR_CARRIER (graviton): partition 18, M_native 18
  - QP093A-0301 ROAD_LIGHT_CARRIER (photon): partition 1, M_native 0
  - QP093A-0302 WEAK_VECTOR_CARRIER (W): partition 9, M_native 9
  - QP093A-0303 NEUTRAL_VECTOR_CARRIER (Z): partition 81, M_native 81
  - QP093A-0304 COLOR_OWNER_CARRIER (gluon): partition 8, M_native 8
- Hidden_source_support_rows has exactly 8 members with partitions
  {1,2,3,4,6,8,9,12} in any order.
- For each hidden_source row, `M_native == p + p^2/R^2` exact in rational
  arithmetic with `R^2 = 144`.

### Partition sums

- carrier_partition_sum (incl graviton): 117
- carrier_partition_sum (excl graviton): 99
- hidden_partition_sum: 45
- total_partition: 162

### Mass sums

- carrier_mass_sum (incl graviton, photon=0): 116
- hidden_mass_sum: 45 + 355/144
- total_mass: 162 + 211/144

### Structural identities

- 99 + 45 == 144 == R^2
- 18/R^2 == 1/8 == 2^-D at D=3
- 162/R^2 == 9/8
- 1 + 2^-D == 9/8 at D=3 (algebraic form 1)
- D^2 / 2^D == 9/8 at D=3 (algebraic form 2, the LC11 bounce lift form)
- Sum p^2 for hidden_source set == 355
- Sum p^2 for hidden_source p < R == 211
- Mass excess over partition == 211/R^2

### Photon Falsifier

- photon row partition == 1
- photon row M_native == 0
- carrier_partition_sum - carrier_mass_sum (incl graviton) == 1
  - This isolates the photon as the sole carrier-side source of the
    partition-vs-mass disagreement.

If any of partition=1, M_native=0, or the difference=1 condition fails,
CR217 fails. This is the explicit falsifier for the closed identity.

## Non-Promotion Rule

- The match of 162 to R^2 * (9/8) is recorded as a backed observation.
- The structural reading "162 = closed loop + carrier release" is recorded
  as scientific_reading only, not as a derived mechanism.
- The match of 9/8 between CR217's 162/R^2, CR060a/CR066a middle-slot
  surcharge, and LC11 bounce lift is recorded as three independent
  sealed appearances of the same ratio. It is not promoted to a unified
  derivation in this CR. A unified derivation would be a follow-up CR.

## Outputs

- `CR217_runner.py`
- `CR217_declared_premises.json`
- `CR217_input_manifest.csv`
- `CR217_carrier_block.csv`             (the 5 carrier rows, sealed values)
- `CR217_hidden_source_block.csv`       (the 8 hidden source rows, lift check per row)
- `CR217_identity_checks.csv`           (one row per identity, pass/fail)
- `CR217_summary.json`
- `CR217_result.md`
- `HASHES.txt`
