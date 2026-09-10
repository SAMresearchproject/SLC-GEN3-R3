# CR001 — QGC Phase 1: Substrate Gate Involution End-to-End — RESULT

**Verdict:** PASS
**Branch:** 18_SAM_NATIVE_QC
**Phase:** 1 (first CR in branch 18; operational foundation)
**Executed:** 2026-06-24
**Runner:** `CR001_runner.py` (Python 3.12)

---

## Headline

The QGC operational stack (LCQC000–LCQC008) composes end-to-end as
specified. The locked program

```text
   INIT(face=9, α_H=0, resolved)
     → 𝒢_sub  →  B  →  𝒢_sub  →  B  →  MEASURE
```

returns `(face=9, α_H=0)` after consuming exactly `5 · S² = 320`
substrate writes (`0.52%` of N_max = 61,312). All 6 per-step states
match the locked expected per-step state exactly. All 5 wrong
controls produce their predicted broken outputs.

## Main program — per-step trace

```text
   step    op           face    α_H     status        budget
   ────────────────────────────────────────────────────────────
   0       INIT          9       0      resolved          0
   1       𝒢_sub        12       0      resolved         64
   2       B            12       1      resolved        128
   3       𝒢_sub         9       1      resolved        192
   4       B             9       0      resolved        256
   5       MEASURE       9       0      resolved        320
```

Full trace in `CR001_per_step_trace.csv`.

## Verification gates

```text
   V-1 / V-2  all per-step (face, α_H, status, budget) match expected   PASS
   V-3        final budget = 5 · S² = 320 writes                        PASS
   V-4        budget stayed ≤ N_max throughout                          PASS
   V-5        final MEASURE returned α_H = 0 deterministically           PASS
   V-6        final face_index = 9 (substrate gate involution)          PASS
```

## Wrong controls

```text
   id     description                         expected           observed     verdict
   ─────────────────────────────────────────────────────────────────────────────────────
   WC-1   drop one 𝒢_sub (omit step 3)        face=12, α_H=0    face=12, α_H=0   PASS
   WC-2   extra 𝒢_sub (3 swaps total)         face=12, α_H=0    face=12, α_H=0   PASS
   WC-3   non-residual face (init face=4)     face= 4, α_H=0    face= 4, α_H=0   PASS
   WC-4   measure-first (before any gates)    face= 9, α_H=0    face= 9, α_H=0   PASS
   WC-5   drop second B (omit step 4)         face= 9, α_H=1    face= 9, α_H=1   PASS
```

Per-WC details in `CR001_wrong_controls.csv`.

## Verdict gates assessment

Per CR001_PRECOMMIT.md:

```text
   PASS conditions (all required):
     P1  V-1 through V-6 hold for main program                  ✓ met
     P2  WC-1 through WC-5 each produce predicted broken output ✓ met
     P3  No exceptions during execution                          ✓ met
     P4  Per-step trace CSV produced with all 6 rows             ✓ met
     P5  Wrong control CSV produced with all 5 WC outcomes       ✓ met
     P6  Cumulative budget tracking matches predicted exactly    ✓ met
```

All 6 PASS conditions met. Verdict: **PASS**.

No BOUNDARY or FAIL conditions triggered.

## What this confirms

1. **LCQC001 state object** (𝒲 = face × α_H × status) is operationally
   well-defined and tracks correctly under composition.
2. **LCQC003 substrate gate 𝒢_sub** is correctly specified: it swaps
   face_index 9 ↔ 12 (residual pair from LCQC002), is identity on
   non-residual faces, does not affect α_H label, and is an
   involution (`𝒢_sub² = identity` confirmed by WC-1 vs main).
3. **LCQC003 binary flip B** is correctly specified: it flips α_H
   label 0 ↔ 1, does not affect face index, and is an involution
   (`B² = identity` confirmed by WC-5 vs main).
4. **𝒢_sub and B commute on disjoint operands** (face vs label;
   confirmed by the swap pattern in the main program).
5. **LCQC008 MEASURE** is correctly specified: idempotent on
   resolved states (WC-4), consumes S² writes per event (budget
   accounting), preserves face_index (per-step trace), commits α_H
   label.
6. **LCQC004a gate-size invariant** `1 gate = S² writes` holds for
   both gates and measurements: 5 ops × 64 writes = 320 writes
   matches the predicted budget consumption to the bit.
7. **End-to-end composition under coherence budget** works: 5 gates
   + 1 measurement = 6 ops consumes 0.52% of N_max, leaving ample
   budget for non-trivial programs.

## What this does NOT close

Per CR001_PRECOMMIT.md "What CR001 DOES NOT close":

- Born-rule statistics on superposition states (Phase 2)
- Multi-site ring topology composition (Phase 2)
- Cross-site A-field interference (Phase 2)
- Per-isotope variation (Phase 2+)
- Substrate-native fault tolerance (open follow-up; LCQC004a §7)
- External-benchmark comparison (out of scope by R-3)

The measurement-cost engineering choice from LCQC008 (`S² writes per
event`) is used as-is; audit item A-14 (whether this can be derived
from a deeper substrate principle) remains open.

## Verdict signature

```text
PASS_CR001_QGC_PHASE_1_SUBSTRATE_GATE_INVOLUTION_END_TO_END__
  MAIN_PROGRAM_RETURNS_FACE_9_ALPHA_H_0_AFTER_G_SUB_B_G_SUB_B_MEASURE__
  ALL_6_PER_STEP_STATES_MATCH_LOCKED_EXPECTED_EXACTLY__
  5_GATES_PLUS_1_MEASUREMENT_CONSUMES_320_WRITES_EQ_0_52PCT_OF_N_MAX__
  ALL_5_WRONG_CONTROLS_PRODUCE_PREDICTED_BROKEN_OUTPUTS__
  WC1_DROP_GSUB_FACE_12__
  WC2_EXTRA_GSUB_FACE_12__
  WC3_NON_RESIDUAL_FACE_4_UNCHANGED__
  WC4_MEASURE_FIRST_IDEMPOTENT_ON_RESOLVED__
  WC5_DROP_B_ALPHA_H_1__
  LCQC008_OPERATIONAL_STACK_COMPOSITION_VERIFIED__
  QGC_OPERATION_PRIMITIVE_FOUNDATION_VERIFIED__
  PHASE_1_VERDICT_PASS_READY_FOR_PHASE_2_SUPERPOSITION_AND_MULTI_SITE
```

## Inputs

```text
   CR001_PRECOMMIT.md   (this CR; sealed by Sean Brady 2026-06-24)
   CR001_runner.py       (this CR; Python 3.12 simulation)

   LCQC layer dependencies (branch 18; in-tree, no SHA gate):
     LCQC000_NATIVE_QC_CHARTER.md
     LCQC001_NATIVE_STATE_ONTOLOGY.md
     LCQC002_register_verdict.md
     LCQC003_TRANSITIONS_AND_GATES.md
     LCQC004_COHERENCE_FLOOR.md
     LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md
     LCQC005_MATERIALS_PALETTE.md
     LCQC006_NETWORKING_AND_RING_TOPOLOGY.md
     LCQC006a_RING_AMPLIFICATION_UNDER_THE_HOOD.md
     LCQC007_REGISTER_MASS_IDENTITY.md
     LCQC008_NATIVE_MEASUREMENT_OPERATION.md

   Upstream sealed CRs (read-only):
     CR114, CR222, CR229, CR232, CR238
```

## Outputs

```text
   CR001_per_step_trace.csv     6 rows; main program per-step state
   CR001_wrong_controls.csv     5 rows; per-WC outcome
   CR001_summary.json           full structured verdict
   CR001_result.md              this file
   HASHES.txt                   SHA-256 of all CR001 artifacts (post-run seal)
```

## Sealed

Sean Brady, 2026-06-24. CR001 verdict PASS; the LCQC008 operational
stack composes end-to-end as specified. The QGC's operational
foundation is verified by computational simulation. Ready for Phase 2
CRs that test superposition (Born-rule on prepared mixed states),
multi-site ring composition (Rule #12 budget allocation), and
per-isotope variation.
