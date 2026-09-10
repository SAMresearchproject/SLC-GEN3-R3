# CR003 — QGC Phase 2: Joint Figure 𝒞 Correlation End-to-End

**Branch:** 18_SAM_NATIVE_QC
**Phase:** 2 (first multi-site / joint composition test; extends CR001)
**Sealed by:** Sean Brady, 2026-06-24

---

## Question

Does the QGC's joint figure `𝒞` from LCQC003 v2 §3.3 produce
correctly-correlated joint state when composed with the binary flip
`B` and publication primitives from LCQC008 v2? Specifically:

```text
   Does the program

      INIT site_A (face=9,  α_H=0, resolved)
      INIT site_B (face=4,  α_H=0, resolved)
      → B(site_A)                  (α_H_A: 0 → 1; site_A label flipped)
      → 𝒞(control=A, target=B)    (control α_H=1 → target gets B; α_H_B: 0 → 1)
      → PUBLISH(site_A)
      → PUBLISH(site_B)

   produce the correlated output (α_H_A=1, α_H_B=1) — confirming that
   `𝒞` successfully transferred the control's label-1 condition into a
   correlated flip on the target — with all 7 ops (5 figures + 2
   publications) consuming budgets per site well below N_max = 61,312?
```

This is the QGC's first joint-composition operational test. CR001
verified single-site composition (`𝒢_sub² ∘ B²` involution). CR003
verifies that the joint figure `𝒞` extends composition to two
participating sites with the predicted correlation behavior.

## Honest framing

CR003 verifies the **substrate-native correlation primitive** —
LCQC003 v2's joint figure `𝒞` — composes correctly with B and PUBLISH
on two abstract sites. This is the smallest meaningful multi-site
operational test.

What CR003 deliberately DOES NOT yet test (deferred to subsequent CRs):

- Physical distance effects (LCQC006 v2 1/r A-kernel coupling) —
  abstract two-site model treats sites as logically distinct without
  spatial-distance interference
- Multi-site coherence budget interaction (LCQC006a Rule #12
  T_ring(K) sharing) — each site has independent N_max budget
- Ring topology composition / cyclic phrase — no playhead / cycle
- Born-rule superposition statistics — deterministic-prep states only
  (consistent with CR001 framing)
- Per-isotope variation — balanced anchor implicit
- Substrate gate `𝒢_sub` in joint composition (CR001 covered this on
  single site; multi-site `𝒢_sub` is later)

Each of those is a separate CR (CR004+) as the operational stack
scales one dimension at a time.

## Locked substrate atoms (read-only from CR238 + LCQC004a)

```text
   S² = 64                       writes per figure (LCQC004a)
   N_max = 61,312                per-site coherence ceiling (LCQC004)
   α_H = 2                       binary readout atom
```

## Locked LCQC primitives (per LCQC003 v2 + LCQC008 v2)

### State (per LCQC001)

```text
   𝒲 = (face_index ∈ {1..81}, α_H_label ∈ {0,1,?}, status ∈ {resolved, unresolved})
```

### Joint figure `𝒞` (per LCQC003 v2 §3.3)

```text
   𝒞 :  𝒲_c ⊗ 𝒲_t  →  𝒲_c ⊗ (B(𝒲_t) if label(𝒲_c) = 1 else 𝒲_t)

   Requirement: control 𝒲_c must be RESOLVED (status = resolved)
                target 𝒲_t may be resolved or unresolved (only
                resolved is used in CR003)

   Properties: 𝒞 is its own inverse on the joint state when
               control is unchanged between applications;
               𝒞 is asymmetric — control's label determines whether
               target gets flipped, not vice versa

   Cost (per LCQC004a / Rule #11): one joint figure consumes S² = 64
        substrate writes at the control site AND S² writes at the
        target site (each participating site sees gate-equivalent
        substrate activity)
```

### Other primitives (already verified in CR001)

```text
   INIT       : set initial (face, α_H_label, status); 0 writes
   B          : flip α_H label 0↔1 (resolved state); S² writes at site
   PUBLISH    : G_matter promotion event; commits α_H label;
                S² writes at site (per LCQC008 v2 / Rule #15)
```

## Locked program

```text
   step    op                          site_A             site_B           writes (A, B)
   ──────────────────────────────────────────────────────────────────────────────────────
   0       INIT site_A                 (9, 0, resolved)   —                    (0, 0)
   0       INIT site_B                 (9, 0, resolved)   (4, 0, resolved)     (0, 0)
   1       B(site_A)                   (9, 1, resolved)   (4, 0, resolved)     (S², 0)
   2       𝒞(control=A, target=B)     (9, 1, resolved)   (4, 1, resolved)     (S², S²)
                                        ↑ control unchanged   ↑ target flipped
                                        because A's α_H=1
   3       PUBLISH(site_A)              (9, 1, resolved)   (4, 1, resolved)     (S², 0)
   4       PUBLISH(site_B)              (9, 1, resolved)   (4, 1, resolved)     (0, S²)
   ──────────────────────────────────────────────────────────────────────────────────────
   total writes consumed                                                         3·S²    2·S²
                                                                                 = 192   = 128
   N_max per site                                                                 61,312  61,312
   utilization per site                                                            0.31%   0.21%
```

## Locked expected per-step state

```text
   step    op                   face_A α_HA  status_A      face_B α_HB  status_B    cum_writes_A  cum_writes_B
   ────────────────────────────────────────────────────────────────────────────────────────────────────────────
   0       INIT_A               9      0     resolved      —      —     —             0              —
   0       INIT_B               9      0     resolved      4      0     resolved      0              0
   1       B(A)                 9      1     resolved      4      0     resolved      S²             0
   2       𝒞(A→B)               9      1     resolved      4      1     resolved      2·S²           S²
   3       PUB(A)               9      1     resolved      4      1     resolved      3·S²           S²
   4       PUB(B)               9      1     resolved      4      1     resolved      3·S²           2·S²

   FINAL EXPECTED:              9      1     resolved      4      1     resolved      192            128

   Correlation: (α_H_A=1, α_H_B=1) — 𝒞 transferred A's flip to B
```

## Locked verification

```text
V-1  After each step, per-site (face, α_H, status, cumulative_writes)
     matches the locked expected state exactly.
V-2  Cumulative writes per site stay ≤ N_max = 61,312 throughout.
V-3  Final state: site_A α_H = 1 AND site_B α_H = 1 (correlated).
V-4  Final faces unchanged from INIT (face_A=9, face_B=4) since
     𝒞 acts on labels not faces.
V-5  Final cumulative writes: site_A = 3·S² = 192, site_B = 2·S² = 128.
```

## Wrong controls

```text
WC-1   (skip B on control)       Omit step 1 (don't flip site_A).
                                 Expected: 𝒞 reads control α_H=0, target
                                  unchanged. Final: site_A α_H=0,
                                  site_B α_H=0. NO correlation.

WC-2   (B after 𝒞)               Apply 𝒞 first, then B on site_A.
                                 𝒞 reads control α_H=0 (initial),
                                  target unchanged at 0. Then B flips
                                  site_A to 1. Final: A=1, B=0.
                                 (Tests temporal ordering — 𝒞 reads
                                  control AT FIRE TIME, not later.)

WC-3   (swap control/target)     𝒞(control=B, target=A) instead of
                                  𝒞(control=A, target=B).
                                 With control_B α_H=0, target_A
                                  unchanged at 1 (from B(A) at step 1).
                                 Final: A=1, B=0. (Tests asymmetry —
                                  𝒞 with control_B reads B's label,
                                  not A's.)

WC-4   (apply 𝒞 twice)           𝒞(A→B) applied twice consecutively.
                                 First 𝒞: control=1, target 0→1.
                                  Second 𝒞: control=1, target 1→0.
                                 Final: A=1, B=0. (Tests 𝒞² = identity
                                  on joint state when control fixed.)
```

Each WC produces a deterministic broken output (≠ main's (1,1)).

## Verdict gates

```text
PASS conditions (all required):
  P1  V-1 through V-5 all hold for main program
  P2  Each WC produces its predicted broken output
  P3  Runner reports per-step trace CSV with all 5 expected rows
  P4  Wrong control CSV produced with all 4 WC outcomes
  P5  Cumulative budget per site matches predicted exactly
  P6  No exceptions during execution

BOUNDARY conditions:
  B1  Main program passes but one or two WCs produce unexpected
      output (joint algebra has unforeseen edge case)
  B2  Main program passes but budget accounting is off by a constant
      consistent with figure-cost normalization choice (then mark and
      document)

FAIL conditions:
  F1  Main program produces wrong final state (any field mismatch)
  F2  Any per-step state mismatch
  F3  Cumulative budget exceeds N_max during execution (unexpected)
  F4  Any WC fails to produce its predicted broken output
  F5  Runner crashes
```

Expected outcome: **PASS**. The joint figure `𝒞` per LCQC003 v2's
specification should deterministically produce the correlated final
state. The wrong controls test specific specification claims
(temporal ordering, asymmetry, involution).

## What CR003 DOES NOT close

- Does NOT test physical-distance effects between sites. Abstract
  model assumes sites interact only via the `𝒞` operation, with no
  1/r A-kernel cross-coupling.
- Does NOT test Born-rule statistics on superposition (control is
  resolved throughout).
- Does NOT test ring topology composition.
- Does NOT test per-isotope variation.
- Does NOT test substrate gate `𝒢_sub` in joint composition (could
  be CR004 — `𝒢_sub` on one site combined with `𝒞` between sites).

## Outputs (locked file shape)

```text
   CR003_PRECOMMIT.md                  this file
   CR003_runner.py                     Python runner
   CR003_per_step_trace.csv            per-step joint state + budget
   CR003_wrong_controls.csv            per-WC outcome
   CR003_summary.json                  verdict + verification
   CR003_result.md                     verdict markdown
   HASHES.txt                          SHA-256 of all CR003 artifacts
```

## Cryptographic chain (inputs)

```text
   LCQC000_NATIVE_QC_CHARTER.md                  (branch 18)
   LCQC001_NATIVE_STATE_ONTOLOGY.md              (branch 18)
   LCQC003_TRANSITIONS_AND_GATES_v2.md           (branch 18)
   LCQC004_COHERENCE_FLOOR.md                     (branch 18)
   LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md  (branch 18)
   LCQC008_NATIVE_MEASUREMENT_OPERATION_v2.md     (branch 18)
   CR001_result.md  =  c7a0d0eb5a1af9b69ea3300dda1d29399e9a297c9006e7e09a08d576e116b472

   Upstream sealed CRs (read-only):
   CR114, CR222, CR229, CR232, CR238
```

## Falsifiers

```text
F-MAIN-CORR   Main program returns (α_H_A, α_H_B) ≠ (1, 1): the joint
              figure 𝒞 doesn't compose correctly with B; either the
              control-reads-label-at-fire-time semantics or the
              target-receives-B semantics is wrong in the
              implementation.

F-MAIN-FACE   Final faces ≠ (9, 4): 𝒞 affected face indices, which
              it should NOT — 𝒞 acts only on α_H labels per spec.

F-MAIN-BUDGET  Cumulative writes per site != predicted (3·S² for A,
              2·S² for B): figure-cost accounting wrong, OR 𝒞's joint
              figure cost interpretation differs from "S² per
              participating site."

F-WC-1        WC-1 returns (0, 1): implementation flipped target B
              without seeing control's label-0; 𝒞 broken.

F-WC-3        WC-3 returns (anything, 1) where site_B ends at 1:
              𝒞 is treating both sites symmetrically rather than
              asymmetrically by control/target role.

F-WC-4        WC-4 returns (1, 1) instead of (1, 0): 𝒞² did not
              return target to original; involution broken.
```

## Sealed

Sean Brady, 2026-06-24. Substrate atoms, LCQC primitive specs (joint
figure 𝒞 cost and semantics), program steps, expected per-step state,
verification gates, wrong controls, verdict thresholds, falsifiers
all locked above the line.
