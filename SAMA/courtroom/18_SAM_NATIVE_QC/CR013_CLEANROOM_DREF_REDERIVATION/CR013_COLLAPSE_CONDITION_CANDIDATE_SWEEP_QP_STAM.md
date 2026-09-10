# CR013 Collapse-Condition Candidate Sweep — QP + Stam companion

**Purpose.** Companion to
`CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP.md` (Courtroom sweep).
Extends the sweep to `C:\VS\quantum_phase` and
`C:\VS\Stam_model-A-v1.0\tests\Substrate\` per Sean's directive
2026-07-03.

**Scope.** Two additional repos. Same anti-retrofit discipline: no
targeting of specific d_ref values; look for sealed structural rules
that close a condition regardless of d_ref outcome.

**Executive summary.**

| Condition | QP result | Stam-substrate result | Combined status vs. Courtroom-only |
|---|---|---|---|
| 1 — Regime ID | No new candidate | No new candidate | Unchanged: QP038+CR103a 11/12 threshold remains strongest, still needs bridge |
| 2 — Projection N | QP091Y diagnostic in surface-debit context (NOT SLC coupling) | G282/G283/G284 AMETER discipline at Planck scale (not loop scale) | Improved discipline precedent, no closure |
| 3 — Mean-free-path | No candidate | No candidate | Unchanged: open |
| 4 — Absolute observable | QP091A "Courtroom Scale Bridge" alignment (FITTED, not closure) | G120a is GR Kerr QNM reference, not SAM observable | Unchanged: open |

**Bottom line.** No standalone closure candidate for any of the four
conditions in QP or Stam. Extended sweep confirms the Courtroom-only
read. Two structurally-relevant additions worth naming even though
neither closes:

1. **G282/G283/G284 AMETER discipline** — sets a methodology
   precedent for how a future closing CR should be structured.
2. **QP091Y feature-stack exponent selector** — evidence R-power
   exponents are structural in matter-branch (surface-debit) context,
   supporting CR010 §3 S6's ontological claim.

---

## Extended findings — Stam substrate G282/G283/G284 AMETER discipline

**Location.** `C:\VS\Stam_model-A-v1.0\tests\Substrate\
G282_AMETER_normalization/`,
`G283_substrate_action_from_AMETER/`,
`G284_universal_phase_promotion/` (plus `G284b_substrate_
lensing_from_L_A/` and `G284c_gate3_remaining/`).

**What is sealed jointly:**

- **G282** — derives substrate-native units from PR §2.4 symmetric
  Planck-axis scaling (recorded 2026-05-26 via G282 / Sean RULING /
  P-2026-05-26-7):
  ```
  ell_SW = A_0 · ell_P            (length axis)
  t_SW   = A_0 · t_P              (time axis)
  m_SW   = m_P · A_0              (mass axis; committed symmetrically)
  A_0    = 1/(2·π·α_H·D) = 1/(12·π)   (α_H=2, D=3)
  ```
  Load-bearing commitment: A₀ appears at exponent 1 per axis,
  symmetric across axes. Conditional PASS (per sub-agent
  characterization) with the PR §2.4 reading as the load-bearing
  condition.

- **G283** — verifies the photon-phase identity
  ```
  phi = omega · N_SW · t_SW = omega · L_A / c = omega · Δt
  ```
  reduces exactly to standard form under G282's commitments.
  Numerical Cassini X-band (L_A = 39,547.66 m, ω = 5.28e10 rad/s):
  substrate arithmetic and standard identity agree at relative
  difference 1.34e-16 (machine precision). Four wrong-controls:
  - WC1 (t_SW = t_P without A₀): fails by 1/A₀ = 12π
  - WC2 (ell_SW = ell_P without A₀): fails by A₀ = 1/(12π)
  - WC3 (A₀² per axis on both): numerically matches BUT rejected
    because "PR §2.4 commits to A_0^1 per axis, not A_0^2 —
    identity recovered for the WRONG reason"
  - WC4 (asymmetric A₀ exponents): fails by A₀
  Verdict: `G283_PHOTON_PHASE_IDENTITY_VERIFIED`, all 5 pass
  conditions PASS.

- **G284** — tests whether the same substrate-count chain
  (`omega = E/ℏ`) recovers general quantum phase (R1 photon → R2
  massive non-relativistic COW → R3 relativistic plane wave). Result
  `PROMOTION_PARTIAL`: R1 + R2 unified (no separate κ_massive), but
  R3 fails — substrate count reproduces only lab-frame temporal
  phase `E·t/ℏ`, not spatial phase `p·x/ℏ` or proper-time phase
  `m·c²·τ/ℏ`.

- **G284b** — substrate-Fermat lensing reproduces GR weak-field
  deflection `α = 4GM/(c²b)` under `n(r) = 1 + A(r)`. Weak-field
  scope only.

- **G284c** — gate 3 remaining work (unclear scope from filename;
  not read).

**Assessment for CR013.**

- **Does NOT close any condition standalone.** G282-G284 pin the
  axis-scaling exponent at A₀¹ per axis at **Planck scale** —
  `ell_SW ≈ 4.29×10⁻³⁷ m`. The CR013 write-to-read reach lives at
  **loop scale** — λ_C(m_3) ≈ 3.877 μm — which is ~31 orders of
  magnitude above ell_SW. No G-series test in Stam extends PR §2.4
  axis-scaling discipline to the loop-scale coupling context.
- **Discipline precedent.** G283's WC3 is the important lesson: an
  alternative that numerically matches can still be structurally
  wrong. The A₀² per axis reading recovers the same phase at machine
  precision but violates PR §2.4's exponent commitment and is
  rejected. This is exactly the anti-retrofit discipline CR013
  itself was built to enforce, applied at a different scale.
- **Bearing on Condition 2 (SI-anchor N=0 reading).** The CR013
  DERIVER's Candidate 2a (adopt SI-frame anchor per SAM_ON_EARTH_v1
  §3 as the operational projection with N=0) has a natural
  interpretation under G283's discipline: at Planck scale the
  substrate-to-SI mapping needs A₀¹ per axis; at loop scale, if
  λ_spaghettio = λ_C(m_3) is composed from SI-anchored ℏc and
  substrate-derived m_3, the loop-scale reach is **already in SI**
  with no additional A₀ dressing needed. This is consistent with
  N=0 SI-anchor reading at loop scale, but the identification is
  not itself sealed by G283 — G283 is a Planck-scale test.
- **Target-shape check.** G282/G283/G284 do not name d_ref, do not
  compute a loop-scale reach, and do not touch SLC-bench criteria.
  Clean anti-retrofit.

**What a G-series test that WOULD close Condition 2 would look like:**
a G-series test that verifies an SI-anchored observable at loop
scale (analogous to G283 at Planck scale) and either forces or
refuses an A₀-per-axis dressing at loop scale via wrong-control
comparison. Not present as of this sweep.

---

## Extended findings — QP091Y feature-stack exponent selector

**Location.** `C:\VS\quantum_phase\docs\reports\
QP091Y_SURFACE_DEBIT_R_POWER_EXPONENT_SELECTOR.md`

**Result field:** `PASS_QP091Y_SURFACE_DEBIT_R_POWER_EXPONENT_
SELECTOR__FEATURE_STACK_GENERATES_DIAGNOSTIC_N_23_23__COEFFICIENT_
EXACT_0_23__QABS_RPOWER_18_23_WITHIN_5PCT_RETAINED__CMAG_VALUE_LAW_
STILL_OPEN`

**What it seals.** In the surface-debit / matter-branch context
(part of the CR114 Higgs = capacity − surface debit family), the
scaffold `C_mag ≈ native_menu · |q| · R^n` is preserved, and a
feature-stack selector generates `n = n(operator, depth, |q|,
route_class)` with:
- diagnostic n hits: 23/23
- coefficient exact hits at generated n: 0/23
- coefficient within 5% at generated n: 18/23

Wrong controls (shuffled operator, shuffled |q|, wrong D=2, wrong
D=4) all degrade the diagnostic hit rate, confirming the selector
uses substrate features non-trivially.

**Assessment for CR013.**

- **Does NOT close Condition 2.** QP091Y operates in the surface-
  debit / matter-branch context, which is a different coupling
  context from the SLC pop-bounce-intersect write-to-read
  mechanism CR013 addresses. Even within its own context,
  coefficient closure is 0/23 exact — the underlying rule is not
  yet sealed. Next-frontier note: "freeze n, then derive native
  menu/value selection without nearest-menu fitting."
- **Bearing on Condition 2 (support for CR010 §3 S6).** The
  feature-stack finding — that R^n dressings are structurally
  selected by (operator, depth, |q|, route_class) — is evidence
  that CR010 §3 S6's ontological claim ("R-power dressings in
  downstream coupling laws are structural consequences of
  Home-nesting projection levels, not device parameters") is
  concretely instantiated in at least one context. That supports
  the STIPULATED-tier reading of CR010 §3 S6 in the Courtroom
  sweep from "declaration" to "declaration with one worked example
  in a neighbouring context."
- **Target-shape check.** QP091Y does not compute or touch d_ref.
  Clean anti-retrofit.

---

## Extended findings — QP091A Courtroom Scale Bridge Post-Bounce Alignment

**Location.** `C:\VS\quantum_phase\docs\reports\
QP091A_COURTROOM_SCALE_BRIDGE_POST_BOUNCE_ALIGNMENT.md`

**What it seals (per sub-agent).** Phenomenological alignment
between Courtroom scale-bridge simulator and quantum_phase
Higgs/source-pressure chain: source pressure → contact → resolved
write/bounce split → visible Z branch + constrained Z-star → four
terminal leptons → reconstructed parent.

**Assessment for CR013.**

- **Does NOT close Condition 4.** Tier FITTED. Records
  phenomenological alignment between two simulators. Does not
  identify an absolute-length observable class that fixes d_ref
  alone; does not touch the write-to-read coupling length at loop
  scale.
- **Bearing.** Interesting cross-simulator witness that pop-bounce-
  intersect ontology is coherent across horizon-extreme and
  matter-branch scales, but not closure content.

---

## Extended findings — G120a Kerr QNM calibration

**Location.** `C:\VS\Stam_model-A-v1.0\tests\Substrate\
G120a_gr_kerr_qnm_calibration/`

**What it is.** GR reference calibration for Kerr QNM eigenvalues
across five spins. Data files:
`G120a_gr_kerr_qnm_reference.csv` and `.json`.

**Assessment for CR013.**

- **Does NOT close Condition 4.** G120a is a GR-side calibration
  (baseline for ringdown eigenvalues); it does NOT derive a
  SAM-native observable that pins an absolute length scale. Any
  future SAM-vs-GR ringdown test that used G120a as reference
  could test SAM's QNM predictions but would still not fix d_ref
  alone — QNM frequencies are dimensionless products (ω·M), so any
  match constrains the ratio, not the absolute reach.
- Consistent with Courtroom sweep's Condition 4 finding: no
  observable class that fixes d_ref alone exists in the sealed
  record. Kerr QNM specifically cannot close this — dimensional
  analysis alone rules it out.

---

## Consolidated three-repo picture (Courtroom + QP + Stam)

**Condition 1 — Regime identification.** Strong candidate remains
Courtroom-side (QP038 + CR103a 11/12 threshold). QP and Stam add
no new content. Bridge from A-field 11/12 threshold to CR010 §1.5
pop-density regime split is the missing structural rule.

**Condition 2 — Projection level N.** No standalone closure across
all three repos. Discipline scaffolding improved:
- CR010 §3 S6 (Courtroom) — declares R^N exists structurally.
- QP091Y (QP) — instantiates feature-stack R^n selection in matter-
  branch surface-debit context; supports CR010 §3 S6 with one
  worked example; DOES NOT close for SLC context.
- G282/G283/G284 (Stam) — pins A₀¹ per axis at Planck scale
  structurally, rejects A₀² per axis even when numerically matching.
  Does not extend to loop scale, but sets discipline precedent for
  a future loop-scale N-pinning test.
- Branch-19 CMB shape closure (Courtroom) — indirect: closes at zero
  free parameters without needing R^N dressing on any length scale,
  weak evidence for N=0 admissibility at cosmological scale.

**Condition 3 — Mean-free-path form.** Open in all three repos. No
candidate for a functional form relating reach to pop density.
Contingent bypass remains: if Condition 1 closes to the dilute
side via QP038-CR103a bridge, Condition 3 stops mattering.

**Condition 4 — Absolute-d_ref observable.** Open in all three
repos. Extended sweep rules out Kerr QNM route explicitly (G120a
is dimensionless / mass-scaling). Contingent bypass remains: if
Condition 2 closes via SI-anchor N=0 reading, Condition 4
collapses simultaneously.

## Ranked next-step options — updated

Options A / B / C / D unchanged from Courtroom sweep. New
observation: **G283's methodology is a template for the highest-
leverage future work.** A structural CR that treats a loop-scale
identity the way G283 treats Cassini-scale photon phase — with
structural exponent pinning and wrong-controls that reject
numerically-matching but structurally-wrong alternatives — would be
the disciplined path.

**Refined recommendation (my read).** If drafting Option A or B, do
so under G283's methodology:
- Precommit the exponent structurally, do NOT fit
- Wrong-controls must include numerically-matching but structurally-
  wrong alternatives (G283 WC3 pattern)
- Numerical verification uses an existing sealed observable that
  the substrate arithmetic must recover; the observable is chosen
  BEFORE the exponent-pinning attempt is drafted (anti-retrofit)

**Option E — new.** Draft a G-series companion test (in
Stam_model-A-v1.0 substrate directory, sibling to G283) that
extends PR §2.4 axis-scaling reasoning from Planck scale to loop
scale, using a loop-scale sealed observable as the verification
target. If it PASSes, it seals a form of Condition 2 (loop-scale
projection is A₀¹ per axis at N=?) and provides G283-style
discipline evidence. If it FAILS or PROMOTION_PARTIAL, the failure
mode itself informs successor structural CR design.

Option E is more work than A but ties into an already-active
research vein in Stam and inherits G283's discipline.

## Provenance chain (all three sweeps)

```text
CR013_DERIVER_RESULT.md   sha256 514f07217fdcf7b1819c7a3bd9d5290060ddcd11405c19ee4776dcd9a3474816
CR013_VERIFIER_REPORT.md  sha256 9be2ec97e8d3165cbe1632e8aa4c19c009da697c65f4cdbc141d14590613a991
CR013_PRECOMMIT.md        sha256 17fa12eec1f1da430aebc7a011c0b3071622e47111d8666269937789f54965f3
CR012_SABOTAGE_ACCOUNTING sha256 13e81194dc4d91c00903af336568f63a47b26ff595d3e58458cf8994ff8d7a3e
STEWARDSHIP_DECLARATION   sha256 d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
SAM_LC_WORK_ASSIGNMENT_v1 sha256 3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4
SAM_ON_EARTH_v1           sha256 7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137
```

## Change log

```text
v1.0  2026-07-03  Companion sweep artifact written by SCRUBBER-
                  lineage session ("big-brother", session id
                  0ea2cc6e…) after two Explore sub-agents returned
                  QP-repo and Stam-substrate findings. G282/G283/
                  G284 folder existence verified by main-session
                  glob; QP091Y actual result field verified by
                  main-session read. Neither agent's substantive
                  read was corrected on verification. Companion
                  to CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP.md.
```
