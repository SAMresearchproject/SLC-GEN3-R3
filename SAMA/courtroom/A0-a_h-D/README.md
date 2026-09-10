# Courtroom Derivation Record: `A0`, `α_h = 2`, and `D = 3`

## Purpose

This record is a courtroom-ready derivation chain for three load-bearing SAM quantities:

```text
α_h = 2
D   = 3
A0  = 1/(12π)
```

The goal is not to argue from downstream empirical fit. The goal is to document how these quantities enter SAM as native framework structure before downstream comparison tests.

## Courtroom Summary

| Quantity | SAM Status | Strongest Claim | Primary Test Chain |
|---|---|---|---|
| `α_h = 2` | Derived structural-argument grade | Horizon/worldsheet pair count is structurally forced by the loop/worldsheet pair route and matter-inheritance checks. | `G229B`, `G230`, `G238` |
| `D = 3` | Derived structural-theorem grade inside SAM | Persistent matter identity requires stable loop/twist/intersection topology; the obstruction selector closes only at `D = 3`. | `G347` → `G348` → `G349` → `G350` → `G352` → `G354` → `G355` |
| `A0 = 1/(12π)` | Composed from derived SAM structure and `π` | Base accumulation unit is composed from the `2π` compact phase cycle, `α_h = 2`, and `D = 3`. | `G277`, `G324`, `G356`, `G357` |

## Vocabulary Note

SAM’s internal vocabulary distinguishes **derived** from **composed**.

- `α_h = 2` is treated as **derived**.
- `D = 3` is treated as **derived**.
- `A0 = 1/(12π)` is best courtroom-labeled as **composed from derived structure and π**.

In ordinary language, `A0` is “derived from SAM structure.” In strict repo vocabulary, it is a **composed framework constant**, not a fitted parameter and not an independent empirical prediction by itself.

---

# 1. `α_h = 2` Derivation Chain

## Claim

```text
α_h = 2
```

`α_h` is the horizon/worldsheet pair count used throughout SAM. It is not introduced as a fit number.

## Main Derivation Path

### `G229B` — `α_h` multiroute derivation

**What it did:**  
`G229B` records the closed-loop substrate route for `α_h = 2`, including the worldsheet pair / null-branch structure.

**Courtroom role:**  
Primary closed-substrate derivation source for `α_h = 2`.

**Source path:**

```text
tests/Substrate/G229B_alpha_H_multiroute_derivation/
tests/Substrate/G229B_alpha_H_multiroute_derivation/results/G229B_summary.md
```

### `G230` — Holographic emergence joint derivation of `α_h = 2` and `D = 3`

**What it did:**  
`G230` gives a joint geometric route: two 2D substrate worldsheets are required for holographic interference. The intersection structure selects the pair count and the ambient dimension together.

Core identity:

```text
α_h · d_worldsheet − d_intersection = D
2   · 2             − 1              = 3
```

**Courtroom role:**  
Unifies the `α_h = 2` and `D = 3` routes into one holographic-emergence principle.

**Source path:**

```text
tests/Substrate/G230_holographic_emergence_joint_derivation_package/
tests/Substrate/G230_holographic_emergence_joint_derivation_package/G230_holographic_emergence_joint_derivation/results/G230_summary.md
tests/Substrate/G230_holographic_emergence_joint_derivation_package/G230_holographic_emergence_joint_derivation/results/G230_symbolic_derivation.txt
```

### `G238` — Matter-side inheritance of `α_h = 2`

**What it did:**  
`G238 v2` verifies that the matter-side route inherits `α_h = 2` through three scoped routes:

```text
Route A — Z2 boundary / endpoint pair symmetry
Route B — holographic emergence identity extension
Route C — information-theoretic Bernoulli minimum
```

Matter-side identity:

```text
closed: α_h · d_worldsheet − d_intersection = D
        2   · 2             − 1              = 3

open:   α_h · d_worldsheet − d_boundary = D
        2   · 2             − 1          = 3
```

Wrong-control scan:

```text
α_h = 1 -> D_implied = 1
α_h = 2 -> D_implied = 3
α_h = 3 -> D_implied = 5
α_h = 4 -> D_implied = 7
```

Only `α_h = 2` gives the required `D = 3` emergence under the declared matter-boundary structure.

**Courtroom role:**  
Matter-inheritance check. It explicitly does **not** claim Standard Model content, generations, color, chirality, hypercharge, matter masses, or Yukawa couplings.

**Source path:**

```text
tests/Matter/M001_matter_mode_endpoint_topology/README_G238.md
tests/Matter/M001_matter_mode_endpoint_topology/results/G238_summary.md
tests/Matter/M001_matter_mode_endpoint_topology/results/G238_symbolic_derivation.txt
```

## Strongest Surviving `α_h` Claim

```text
α_h = 2 is derived at structural-argument grade from the loop/worldsheet pair structure, with matter-side inheritance verified by G238.
```

## Scope Boundary

```text
This derives the pair count α_h = 2.
It does not by itself derive SU(2), weak gauge structure, Standard Model generations, color, hypercharge, matter masses, or a full particle spectrum.
```

---

# 2. `D = 3` Derivation Chain

## Claim

```text
D = 3
```

`D` is the dimensional support count used in SAM. In the current framework, `D = 3` is no longer treated as a mere input; it is recorded as derived inside SAM at structural-theorem grade.

## Earlier Joint Route

### `G230` — Holographic emergence cross-route

`G230` gives the earlier joint geometric route:

```text
α_h · d_worldsheet − d_intersection = D
2   · 2             − 1              = 3
```

This shows that `D = 3` is selected by the two-worldsheet holographic emergence picture.

**Courtroom role:**  
Important joint derivation / cross-route. The stricter current D-theorem closure is the later `G347`→`G355` chain.

---

## D-Theorem Tightening Chain

### `G347` — D=3 theorem route audit

**What it did:**  
`G347` audited live routes for deriving `D = 3`. It did **not** close the theorem. It identified Route C, the loop-topology route, as the strongest candidate.

Core selector:

```text
obstruction_dim = 3 − D
```

At `G347`, the route was still conditional: stable loop/link topology uniquely points to `D = 3`, but the necessity of that identity carrier had not yet been proven.

**Verdict recorded:**

```text
G347_D3_THEOREM_ROUTE_AUDIT_CONDITIONAL_ONLY
```

**Courtroom role:**  
Honest narrowing audit. It prevented premature promotion of `D = 3`.

**Source path:**

```text
tests/Substrate/G347_d3_theorem_route_audit/
tests/Substrate/G347_d3_theorem_route_audit/G347_output.txt
```

### `G348` — Loop topology identity premise audit

**What it did:**  
`G348` tested whether loop/link topology could carry persistent identity. It found that loop/link topology is a sufficient `D = 3`-only identity carrier, but not yet necessary because alternate carriers remained live.

Obstruction table:

```text
D = 1 -> obstruction = 2 -> overconstrained
D = 2 -> obstruction = 1 -> overconstrained
D = 3 -> obstruction = 0 -> stable point obstruction
D = 4 -> obstruction = -1 -> topology unstable / unwinds or slides
```

**Verdict recorded:**

```text
G348_LOOP_TOPOLOGY_IDENTITY_PREMISE_NOT_CLOSED
```

**Courtroom role:**  
Preserves honesty: `D = 3` was not yet theorem-grade here.

**Source path:**

```text
tests/Substrate/G348_loop_topology_identity_premise/
tests/Substrate/G348_loop_topology_identity_premise/G348_output.txt
```

### `G349` — Worldsheet identity reduction audit

**What it did:**  
`G349` reduced the alternate identity carriers from `G348` into extended worldline/worldsheet-like support. It showed that point-like escape routes were not enough, but topology necessity still required further work.

**Verdict recorded:**

```text
G349_WORLDSHEET_IDENTITY_REDUCTION_CANDIDATE_PASS
```

**Courtroom role:**  
Narrowed the live identity-carrier alternatives.

**Source path:**

```text
tests/Substrate/G349_worldsheet_identity_reduction/
tests/Substrate/G349_worldsheet_identity_reduction/G349_output.txt
```

### `G350` — Identity deformation quotient audit

**What it did:**  
`G350` showed that raw ledger histories, endpoint labels, open phases, and standalone spectra do not survive as persistent identity carriers by themselves. They survive only as deformation classes such as closed-loop transport, holonomy, or operator-domain class spectra.

The stable-loop selector remains:

```text
obstruction_dim = 3 − D
```

Stable hit:

```text
D = 3
```

**Verdict recorded:**

```text
G350_IDENTITY_DEFORMATION_QUOTIENT_THEOREM_CANDIDATE
```

**Courtroom role:**  
Turns the route from “topology is sufficient” toward “persistent identity reduces to deformation-invariant loop/holonomy classes.”

**Source path:**

```text
tests/Substrate/G350_identity_deformation_quotient/
tests/Substrate/G350_identity_deformation_quotient/G350_output.txt
```

### `G352` — Self-contained holonomy/topology separation audit

**What it did:**  
`G352` separated external-background holonomy from self-contained matter identity. It found that a self-contained nontrivial holonomy must reduce to a stable source/topological sector.

Stable loop/link dimensions:

```text
D = 1 -> unstable
D = 2 -> unstable
D = 3 -> stable
D = 4 -> unstable
D = 5+ -> unstable
```

**Verdict recorded:**

```text
G352_SELF_CONTAINED_HOLONOMY_REDUCES_TO_STABLE_TOPOLOGY
```

**Courtroom role:**  
Strengthens the necessity chain: intrinsic identity requires a stable topological sector, and the stable 1D loop/link sector occurs only at `D = 3`.

**Source path:**

```text
tests/Substrate/G352_self_contained_holonomy_topology/
tests/Substrate/G352_self_contained_holonomy_topology/G352_output.txt
```

### `G354` — Displacement-response matter identity audit

**What it did:**  
`G354` formalized matter identity as substrate-internal invariant response to disturbance:

```text
no disturbance -> no physical interaction channel -> no ledger write -> no matter identity
physical interaction -> substrate displacement response -> invariant response class
```

It also confirmed that stable twisted/intersection identity selects `D = 3`.

**Verdict recorded:**

```text
G354_DISPLACEMENT_RESPONSE_IDENTITY_PRINCIPLE_PASS
```

**Courtroom role:**  
This supplies the physical premise needed to close the D theorem: matter identity is not an external label; it is the invariant substrate response to disturbance.

**Source path:**

```text
tests/Substrate/G354_displacement_response_identity/
tests/Substrate/G354_displacement_response_identity/G354_output.txt
```

### `G355` — D=3 displacement-response theorem

**What it did:**  
`G355` closes the route and promotes `D = 3` to derived status inside SAM.

The theorem chain recorded in the test:

```text
matterless_undisturbed_no_write
interaction_displacement_write
identity_is_invariant_response_class
extended_carrier_reduction
deformation_quotient
self_contained_holonomy_stable_source
stable_loop_twist_only_D3
extreme_A_reorganizes
```

Dimension scan:

```text
D = 1 -> obstruction = 2  -> stable = false
D = 2 -> obstruction = 1  -> stable = false
D = 3 -> obstruction = 0  -> stable = true
D = 4 -> obstruction = -1 -> stable = false
D = 5+ -> obstruction < 0 -> stable = false
```

**Verdict recorded:**

```text
G355_D3_DISPLACEMENT_RESPONSE_THEOREM_PASS
```

**Grade recorded:**

```text
Derived inside SAM at structural-theorem grade
```

**Courtroom role:**  
Load-bearing D=3 derivation closure.

**Source path:**

```text
tests/Substrate/G355_d3_displacement_response_theorem/
tests/Substrate/G355_d3_displacement_response_theorem/G355_output.txt
```

## Strongest Surviving `D` Claim

```text
D = 3 is derived inside SAM at structural-theorem grade from displacement-response matter identity and the stable loop/twist obstruction selector obstruction_dim = 3 − D.
```

## Scope Boundary

```text
This is a SAM-internal structural theorem. It does not claim external peer-review closure, independent empirical proof by itself, imported string-theory critical dimensions, literal Higgs emission per event, or direct derivation of the entire matter spectrum.
```

---

# 3. `A0 = 1/(12π)` Derivation / Composition Chain

## Claim

```text
A0 = 1/(12π)
```

## Formula

The strict SAM composition is:

```text
A0 = 1 / [(2π phase cycle) · (α_h worldsheet pair) · (D matter identity)]
```

With:

```text
α_h = 2
D   = 3
```

this gives:

```text
A0 = 1 / (2π · 2 · 3)
A0 = 1 / (12π)
```

Equivalently, after the native radix is introduced:

```text
R  = α_h² · D = 2² · 3 = 12_dec = 10_doz
A0 = 1/(πR)
A0 = 1/(12π)
```

These are equivalent because `α_h = 2`, so:

```text
2π · α_h · D = π · α_h² · D = πR
```

## Phase-Cycle / Compact-Cycle Chain

### `G277` — Substrate-native QM phase / compact-cycle branch

**What it did:**  
`G277` forced the compact-cycle interpretation for `A0` toward the substrate Hamiltonian / unitary phase branch under substrate-only ontology and rejected the separate geometric/spatial branch.

Relevant structural reading:

```text
Substrate accumulation ∫A ds
-> Wick continuation τ -> it
-> exp(i · κ · ∫A ds)
```

**Courtroom role:**  
Supports the phase-cycle reading of the `2π` component in `A0`.

**Source path:**

```text
tests/Substrate/G277_substrate_QM_phase/
tests/Substrate/G277_substrate_QM_phase/G277_output.txt
```

### `G324` — Full-cycle action quantum from phase periodicity

**What it did:**  
`G324` derives the primitive full cycle:

```text
exp(iQ/ℏ) = 1
Q_n = 2πnℏ
minimal positive full cycle = 2πℏ
```

Wrong controls reject:

```text
Q = ℏ as full cycle
Q = πℏ as full cycle
Q = 4πℏ as primitive cycle
real exponential cycle
dimensionless-only ℏ magnitude derivation
```

**Verdict recorded:**

```text
G324_FULL_CYCLE_ACTION_QUANTUM_DERIVED_FROM_PHASE_PERIODICITY
```

**Scope boundary:**  
This derives the `2π` phase cycle, not the magnitude of `ℏ`.

**Source path:**

```text
tests/Substrate/G324_full_cycle_action_quantum/
tests/Substrate/G324_full_cycle_action_quantum/G324_output.txt
```

### `G356` — A0 foundation status after D theorem

**What it did:**  
`G356` records the foundation status after `D = 3` was promoted by `G355`.

It verifies:

```text
D derived by G355: true
α_h derived structural-argument: true
A0 numerical value unchanged
```

and records:

```text
A0 = 0.026525823848649224
```

But it also honestly says that at `G356`, compact-cycle `2π` provenance remained open.

**Verdict recorded:**

```text
G356_A0_FOUNDATION_TIGHTENED_COMPACT_CYCLE_REMAINS
```

**Courtroom role:**  
A0 was tightened because the `D` slot was no longer an input, but the compact-cycle source still needed closure.

**Source path:**

```text
tests/Substrate/G356_a0_foundation_status_after_d_theorem/
tests/Substrate/G356_a0_foundation_status_after_d_theorem/G356_output.txt
```

### `G357` — A0 compact-cycle phase provenance

**What it did:**  
`G357` locks the compact-cycle provenance of `A0`.

Recorded decomposition:

```text
A0 = 1 / [(phase cycle 2π) · α_h · D]
phase cycle = 6.2831853071795862
α_h = 2
D = 3
A0 = 0.026525823848649224
```

It explicitly distinguishes the two in `2π` from `α_h = 2`:

```text
U(1) phase-cycle two != worldsheet pair α_h two
```

and rejects wrong controls such as:

```text
π as full cycle
4π as primitive cycle
real exponential periodicity
ℏ magnitude derived
A0 as independent empirical evidence
full TOE closure
```

**Verdict recorded:**

```text
G357_A0_COMPACT_CYCLE_PHASE_PROVENANCE_LOCKED
```

**Grade recorded:**

```text
structural-argument / theorem-boundary provenance closure
```

**Courtroom role:**  
Closes the compact-cycle provenance target for `A0`.

**Source path:**

```text
tests/Substrate/G357_a0_compact_cycle_phase_provenance/
tests/Substrate/G357_a0_compact_cycle_phase_provenance/G357_output.txt
audit/audits/PROPOSED_PRIORITY_RECORD_G357_A0_COMPACT_CYCLE_2026_05_25.md
```

## Strongest Surviving `A0` Claim

```text
A0 = 1/(12π) is a composed SAM-native base accumulation unit. It follows from the locked 2π compact phase cycle, derived α_h = 2, derived D = 3, and π.
```

## Scope Boundary

```text
A0 is not a fitted parameter.
A0 is not independent empirical evidence by itself.
A0 does not derive the magnitude of ℏ.
A0’s physical force is tested downstream in branches such as baryon inventory, CMB-lite contact, distance transfer, particle/reorganization thresholds, and radix inventory closure.
```

---

# 4. Combined Derivation Tree

```text
loop/worldsheet substrate
    -> α_h = 2
       G229B, G230, G238

displacement-response matter identity
    -> stable loop/twist/intersection topology
    -> obstruction_dim = 3 − D
    -> D = 3
       G347, G348, G349, G350, G352, G354, G355

unitary phase periodicity / substrate compact cycle
    -> 2π phase cycle
       G277, G324, G357

therefore:

A0 = 1 / [(2π) · α_h · D]
A0 = 1 / [(2π) · 2 · 3]
A0 = 1 / (12π)
```

Native radix form:

```text
R = α_h² · D = 2² · 3 = 12_dec = 10_doz

A0 = 1/(πR)
A0 = 1/(12π)
```

Radix inventory and closure:

```text
A_share = 1/R = 1/12_dec = 1/10_doz
R · A0  = 12 · 1/(12π) = 1/π
A = 1   = 12/12 full displacement closure
```

---

# 5. Courtroom Status

## `α_h = 2`

```text
execution_status: CLEAN
scientific_verdict: PASS as internal structural derivation
claim_tier: structural-argument grade
primary tests: G229B, G230, G238
```

## `D = 3`

```text
execution_status: CLEAN
scientific_verdict: PASS as internal structural theorem
claim_tier: structural-theorem grade inside SAM
primary tests: G347 -> G348 -> G349 -> G350 -> G352 -> G354 -> G355
```

## `A0 = 1/(12π)`

```text
execution_status: CLEAN
scientific_verdict: PASS as framework composition / provenance closure
claim_tier: composed from derived SAM quantities and π
primary tests: G277, G324, G356, G357
```

## v1.0 Evidence Note

This record is a **foundation / derivation provenance record**, not a standalone empirical-comparison test.

Under the courtroom grading standard, downstream empirical branches must still supply their own external anchors, falsification statements, target hygiene, typed inputs, and reproduction-on-demand records.

The foundation record supplies typed SAM inputs for those branches:

```text
α_h = 2
D = 3
A0 = 1/(12π)
R = 12_dec = 10_doz
A_share = 1/12
A = 1 = 12/12 full closure
```

---

# 6. Test Index

```text
G224  — Bridge equation A = 2GM/(c²r) from loop displacement geometry; cross-checks α_h in the weak-field A-profile.
G229B — α_h multiroute derivation from closed-loop/worldsheet pair structure.
G230  — Joint holographic-emergence derivation of α_h = 2 and D = 3.
G238  — Matter-side inheritance of α_h = 2 through Z2 boundary symmetry, holographic identity, and Bernoulli minimum.

G347  — D=3 theorem-route audit; localized loop topology route but kept theorem conditional.
G348  — Loop topology identity premise audit; stable topology is D=3-only but not yet necessary.
G349  — Worldsheet identity reduction audit; alternate carriers require extended support.
G350  — Identity deformation quotient audit; raw carriers survive only as deformation classes.
G352  — Self-contained holonomy/topology audit; intrinsic identity reduces to stable topological sector.
G354  — Displacement-response identity principle; matter identity becomes invariant substrate response.
G355  — D=3 displacement-response theorem; promotes D=3 to derived structural-theorem grade.

G277  — Substrate-native QM phase; supports compact-cycle / Hamiltonian branch for A0.
G324  — Full-cycle action quantum from phase periodicity; derives primitive 2π phase cycle.
G356  — A0 foundation status after D theorem; D slot no longer input, compact-cycle remained open.
G357  — A0 compact-cycle phase provenance; locks A0 = 1/[(2π) · α_h · D].
```

---

# 7. Final Courtroom Finding

```text
α_h = 2 is derived at structural-argument grade.
D = 3 is derived inside SAM at structural-theorem grade.
A0 = 1/(12π) is composed from the locked 2π phase cycle, derived α_h, derived D, and π.

A0 is not fitted.
A0 is not an independent empirical proof by itself.
A0 is a native SAM base accumulation unit whose physical relevance is tested downstream.
```
