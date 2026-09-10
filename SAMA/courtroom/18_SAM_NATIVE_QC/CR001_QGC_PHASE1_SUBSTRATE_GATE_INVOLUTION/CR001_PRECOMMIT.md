# CR001 — QGC Phase 1: Substrate Gate Involution End-to-End

**Branch:** 18_SAM_NATIVE_QC
**Phase:** 1 (Operational foundation; first CR in branch 18)
**Sealed by:** Sean Brady, 2026-06-24

---

## Question

Do the QGC operational primitives defined in LCQC000–LCQC008 compose
end-to-end to execute a complete program (initialize → gate sequence
→ measurement → expected output) within the substrate coherence
budget, with each LCQC-specified state transition observable at each
step, and with every wrong-control perturbation producing the
predicted broken output?

Specifically:

```text
   Does the program

      INIT(face=9, α_H=0)
      → 𝒢_sub                  (face: 9 → 12; α_H unchanged)
      → B                       (α_H: 0 → 1; face unchanged)
      → 𝒢_sub                  (face: 12 → 9; α_H unchanged)
      → B                       (α_H: 1 → 0; face unchanged)
      → MEASURE

   return the measurement output (face=9, α_H=0) corresponding to the
   composition 𝒢_sub² ∘ B² = identity acting on the initial state,
   with all 6 ops (5 gates + 1 measurement) consuming
   6 × S² = 384 substrate writes well below the per-site coherence
   ceiling N_max ≈ 61,312?
```

This is the QGC's operational sanity test — the smallest program that
exercises all the LCQC008 primitives (state, gate algebra, measurement)
in one end-to-end composition.

## Honest framing

CR001 verifies **composition correctness** of the LCQC008-defined
operational stack, NOT new structural identities. Each individual
LCQC layer has already verified its primitive in isolation:

```text
   LCQC001     — state object 𝒲 = (face, label, status) verified
   LCQC003     — gate algebra B, 𝒢_sub verified as group / partial algebra
   LCQC004     — coherence ceiling N_max verified
   LCQC004a    — ε_per_gate · N_max = S² invariant verified
   LCQC008     — measurement = G_matter promotion verified
```

The genuinely new claim CR001 tests: **these layers compose**. The
result of running the program above through a substrate-write
simulation should match the algebraic prediction (face=9, α_H=0) AND
each per-step intermediate state should match the LCQC003 / LCQC008
specification.

CR001 deliberately stays inside the substrate-internal simulation.
There is no external-data comparison (R-3 discipline); the verdict is
substrate-internal consistency only.

## Locked substrate atoms (read-only from CR238)

```text
   R = 12              register radix
   D = 3               substrate dimension
   S = 8               foundational carrier-slot atom (α_H^D)
   α_H = 2             binary readout atom
   S² = 64             gate-size from LCQC004a (writes per gate-equivalent)
   N_max = 61,312      per-site coherence ceiling (16πR⁴/17 from LCQC004)
```

## Locked LCQC primitives

### State object (from LCQC001)

```text
   𝒲 = (face_index, α_H_label, status)
       face_index  ∈ {1, ..., 81}     (CR114 ledger face position)
       α_H_label   ∈ {0, 1, "?"}      ("?" = unresolved)
       status      ∈ {resolved, unresolved}
```

### Gate primitives (from LCQC003)

```text
   𝒯_I  (identity) :  𝒲 → 𝒲              (no change)

   B    (binary flip) :  for resolved state, swap label 0 ↔ 1
                        for unresolved state, identity

   𝒢_sub (substrate gate / pair-exchange on residual pair) :
        face_index = 9   →   face_index = 12
        face_index = 12  →   face_index = 9
        face_index ∉ {9, 12}  →  identity
        α_H_label  →  unchanged
        status     →  unchanged
```

### MEASURE primitive (from LCQC008)

```text
   MEASURE(𝒲) :
        cost = S² = 64 substrate writes (one gate-equivalent)
        if status = "unresolved" :
           α_H_label resolves to a definite value in {0, 1}
           (Born-rule statistics; for deterministically-prepared
            states the resolved value matches the prepared amplitude)
           status → "resolved"
        if status = "resolved" :
           idempotent — return current α_H_label, no state change
        result returned to classical control system via G_matter=1
           observable channel (per CR232)
```

## Locked program (the main test)

```text
   step 0   :  INIT(face=9, α_H=0, status=resolved)
   step 1   :  apply 𝒢_sub
   step 2   :  apply B
   step 3   :  apply 𝒢_sub
   step 4   :  apply B
   step 5   :  apply MEASURE
```

Note: status is initialized to "resolved" (definite α_H = 0) so the
test isolates COMPOSITION OF DETERMINISTIC GATES from Born-rule
statistical behavior. Phase 2+ CRs can test superposition / Born-rule
explicitly.

## Locked expected per-step state

```text
   step    op           face_index    α_H_label    status      budget
   ──────────────────────────────────────────────────────────────────────
   0       INIT             9             0        resolved        0
   1       𝒢_sub           12             0        resolved       S²
   2       B               12             1        resolved      2·S²
   3       𝒢_sub            9             1        resolved      3·S²
   4       B                9             0        resolved      4·S²
   5       MEASURE          9             0        resolved      5·S²

   FINAL  expected         9             0        resolved      5·S²
                                                                = 320 writes
                                                                ≪ N_max = 61,312
```

## Locked simulation model

The runner simulates the substrate-write model per LCQC006a's exact
derivation, restricted to single-site for CR001:

```text
   For a single-site register (K=1), there is no ring topology;
   per-site budget = N_max writes per coherence cycle.

   Each gate operation = S² writes at the target site (LCQC004a).
   Each MEASURE operation = S² writes at the target site (LCQC008).

   Cumulative budget consumed = (number of ops) · S²
   Budget ceiling = N_max

   The runner tracks (face_index, α_H_label, status, cumulative_writes)
   after each operation and verifies match against the locked
   per-step expected state above.
```

## Locked verification (per-step and final)

```text
V-1  After each gate/measure step, the runner records the resulting
     (face_index, α_H_label, status, cumulative_writes) tuple.
V-2  Each recorded tuple must match the locked expected per-step
     state above exactly.
V-3  Cumulative budget at end of step 5 must equal 5·S² = 320 writes.
V-4  Cumulative budget must remain ≤ N_max = 61,312 throughout.
V-5  Final MEASURE must return α_H_label = 0 deterministically.
V-6  Final face_index must be 9 (involution check).
```

## Wrong controls

```text
WC-1   (drop one 𝒢_sub) : Run program omitting step 3 (second 𝒢_sub).
       Expected: final face_index = 12, α_H_label = 0.
       Confirms involution requires the second swap.

WC-2   (extra 𝒢_sub) : Run program with an extra 𝒢_sub after step 4.
       Expected: final face_index = 12 (odd swap count), α_H_label = 0.
       Confirms odd vs even swap count distinction.

WC-3   (non-residual face) : Initialize face=4 (NOT in {9, 12}) and
       run the same program. Expected: face stays at 4 throughout
       (𝒢_sub is identity on non-residual-pair); α_H still flips
       2x to net 0. Final: face_index = 4, α_H_label = 0.
       Confirms 𝒢_sub's domain restriction to {9, 12}.

WC-4   (measure-first) : MEASURE before applying any gates.
       Expected: returns α_H_label = 0 (the initialized value);
       face_index = 9 (initial); subsequent gates act on resolved
       state.
       Confirms MEASURE on initialized-resolved state is idempotent.

WC-5   (drop second B) : Run program omitting step 4.
       Expected: final α_H_label = 1 (not 0), face_index = 9.
       Confirms B² = identity requires the second flip.
```

Each WC produces a deterministic wrong answer that should differ
from the main test's expected output in at least one field. The
runner verifies each WC produces its predicted broken output.

## Verdict gates

```text
PASS conditions (all required):
  P1  V-1 through V-6 all hold for the main program
  P2  Each wrong control WC-1 through WC-5 produces its predicted
      broken output
  P3  No exceptions / runtime errors during execution
  P4  Per-step trace CSV produced with all 6 expected rows
  P5  Wrong control CSV produced with all 5 WC outcomes
  P6  Cumulative budget tracking matches predicted values exactly

BOUNDARY conditions:
  B1  Main program passes but one or two WCs produce unexpected
      (non-broken) output that needs investigation
  B2  Main program passes but cumulative budget tracking is off by
      a constant factor consistent with normalization-convention
      discrepancy (then mark as B2 and document)

FAIL conditions:
  F1  Main program produces wrong final state
      (face ≠ 9 OR α_H ≠ 0)
  F2  Any per-step state mismatch with locked expected
  F3  Cumulative budget exceeds N_max during execution (unexpected)
  F4  Any wrong control fails to produce its predicted broken output
  F5  Runner crashes or reports infrastructure error
```

Expected outcome: **PASS**. The composition of LCQC003 gates and
LCQC008 measurement on a single-site register is algebraically
deterministic; the simulation simply applies the state-transition
rules step by step. PASS would confirm that the operational stack
composes as the layers specify.

A FAIL would indicate either (a) a layer specification is internally
inconsistent, (b) the runner mis-implements a primitive, or (c) the
algebra has a hidden coupling not accounted for. Each case has clear
next-step diagnostic.

## What CR001 DOES NOT close

- Does NOT test Born-rule statistics. The main program prepares a
  deterministic state; superposition behavior is reserved for Phase 2.
- Does NOT test multi-site ring topology composition. CR001 uses a
  single site; multi-site coherence-budget effects per LCQC006a Rule
  #12 are reserved for Phase 2.
- Does NOT test cross-site A-field interference. Single-site means
  the LCQC006a harmonic-sum dilution does not apply.
- Does NOT test per-isotope variation. Implicit assumption is
  balanced-anchor (R_sub = 1); per-isotope budget scaling per
  LCQC005 is reserved for Phase 2+.
- Does NOT establish substrate-native fault tolerance. The
  measurement-cost engineering choice from LCQC008 (A-14) is used
  as-is without challenge.
- Does NOT compare against any external benchmark (R-3 discipline).
  Verdict is substrate-internal consistency only.

## Outputs (locked file shape)

```text
   CR001_PRECOMMIT.md                  this file
   CR001_runner.py                     Python runner executing the program
   CR001_per_step_trace.csv            per-step (face, α_H, status, budget)
                                       for main program
   CR001_wrong_controls.csv            per-WC outcome (face, α_H, predicted
                                       vs observed)
   CR001_summary.json                  verdict + budget summary + WC summary
   CR001_result.md                     verdict markdown
   HASHES.txt                          SHA-256 of all CR001 artifacts
```

## Cryptographic chain (inputs)

```text
   LCQC000_NATIVE_QC_CHARTER.md                  (branch 18)
   LCQC001_NATIVE_STATE_ONTOLOGY.md              (branch 18)
   LCQC002_register_verdict.md                    (branch 18)
   LCQC003_TRANSITIONS_AND_GATES.md               (branch 18)
   LCQC004_COHERENCE_FLOOR.md                     (branch 18)
   LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md  (branch 18)
   LCQC005_MATERIALS_PALETTE.md                   (branch 18)
   LCQC006_NETWORKING_AND_RING_TOPOLOGY.md        (branch 18)
   LCQC006a_RING_AMPLIFICATION_UNDER_THE_HOOD.md  (branch 18)
   LCQC007_REGISTER_MASS_IDENTITY.md              (branch 18)
   LCQC008_NATIVE_MEASUREMENT_OPERATION.md        (branch 18)

   Upstream sealed CRs (read-only):
   CR114_result.md  =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
   CR222_result.md  =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
   CR229_result.md  =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
   CR232_result.md  =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
   CR238_result.md  =  7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
```

## Falsifiers

```text
F-MAIN-1   Main program returns face ≠ 9 at MEASURE: substrate gate
           involution failed; 𝒢_sub² ≠ identity at the implementation
           level.
F-MAIN-2   Main program returns α_H ≠ 0 at MEASURE: binary flip
           involution failed; B² ≠ identity at the implementation level.
F-MAIN-3   Budget exceeds N_max during execution: gate-cost accounting
           is wrong, OR S² ≠ 64 writes per gate at the implementation
           level.
F-WC-1     WC-1 (drop one 𝒢_sub) returns face = 9: implementation
           treats 𝒢_sub as identity (no swap).
F-WC-3     WC-3 (non-residual face) returns face ≠ initial face:
           implementation extends 𝒢_sub action beyond the residual pair.
F-WC-5     WC-5 (drop second B) returns α_H = 0: implementation
           treats B as identity (no flip).
```

## Sealed

Sean Brady, 2026-06-24. Substrate atoms, LCQC primitive specs, program
steps, expected per-step state, simulation model, verification gates,
wrong controls, verdict thresholds, falsifiers all locked above the
line.
