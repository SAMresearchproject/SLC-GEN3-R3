# CR013 Collapse-Condition Candidate Sweep — ADDENDUM (framing correction)

**Purpose.** Correct a framing error in
`CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP.md` and
`CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP_QP_STAM.md`. Sean flagged
2026-07-03:

> "I requested a scan after the cleanroom was produced, the point of
> which was not a factor in the drafting. I think we are confusing
> audits with progress- what are we doing here if we find a prior
> test that answers a question we are not allowed to use it?"

## The framing error

Both prior sweeps applied CR013's anti-retrofit forbidden-string
discipline to interpretation as well as drafting. That was wrong.

The cleanroom purpose was **drafting blindness**: the DERIVER worked
against a whitelist scrubbed of the target and produced
UNDERDETERMINED CLEAN. That seal stands. **Interpreting an
UNDERDETERMINED verdict against the broader sealed record is
exactly what the sealed record is for.** Prior CRs that bear on the
four collapse conditions are legitimate evidence, not tainted content.

Sub-agent dismissals to unwind:

- Sub-agent 3 dismissed the wrong CR005 as "dimensionless / can't
  fix absolute length." The intended CR005 is CR005@21 (Θ Carrier
  Overflow and QNM Derivation), not the CR005 in the neutrino
  branch. See Condition 4 below.
- Sub-agent 2 dismissed QP091Y as "different context (surface debit
  / matter-branch), doesn't apply to SLC." Wrong. QP091Y and the
  CR245/CR278 surface-debit / binding arc are the sealed working
  examples of how R-power dressings appear in SAM coupling laws.
  They are the paradigm for how Condition 2 gets closed.
- Sub-agent 1 correctly flagged QP038 + CR103a for Condition 1;
  that stands.

## Corrected read — CR005@21 for Condition 4

**Location.** `21_GRAVITATIONAL_WAVES/CR005_THETA_CARRIER_OVERFLOW_
AND_QNM_DERIVATION/CR005_result.md`, sealed 2026-06-29 PASS,
precommit sha `624f0c26…`.

**Headline structural identity.**

```text
ω_R · M  =  (Θ · d̂) / R²  =  d̂ / S  =  d̂ / (d̂^(d̂−1) − 1)  =  3 / 8
```

Derived from CR229 inclusion-exclusion (Θ = 18 as first partition-
algebra overflow), CR238 closure axiom (`S = d̂^(d̂−1) − 1`), CR218
bigrade alphabet, and Sean's identity `Θ + M = R² = ℒ − Θ`. All 26
pre-registered claims verify to exact rational arithmetic. Zero
free parameters. Zero enumeration.

**Bearing on Condition 4.**

Sub-agent 3 was technically correct that `ω_R·M` is dimensionless
(mass × angular frequency = angular). But that misses the point:
**CR005@21 seals the discipline for how SAM produces absolute
observables**. The pattern:

```text
absolute observable  =  substrate-atom ratio  ×  external scale
```

For a Schwarzschild BH of mass M, the absolute ringdown angular
frequency is `ω_R = (3/8) / M`, and any external mass yields an
absolute frequency at zero free parameters. LISA-testable at ~3σ
discrimination vs GR's `0.37367168`.

For CR013's Condition 4 (absolute-d_ref observable), this bears
directly: **d_ref is not a free-parameter length; it is a
substrate-atom ratio times an external scale.** The external scale
is λ_spaghettio (loop scale) or an analogous SI-anchored primitive.
The question is which substrate-atom ratio.

**Analogous ratios already sealed in the SAM record:**

- `Θ / R² = 1/8` — tensor share of capacity, appears in CR001@21
  cap AND CR005 QNM (multiplied by d̂ to give 3/8)
- `d̂ / S = 3/8` — QNM ratio
- `1 / (R·D) = 1/36` — CR245 asymmetry-coefficient candidate
  (structurally clean, 1.9% off fitted)
- `1 / (S·L) = 1/1296` — CR245 Coulomb-coefficient candidate
- `M / Θ = 7`, `R² / Θ = 8`, `ℒ / Θ = 9` — Θ-unit counts from
  Sean's identity

Any of these applied to λ_spaghettio = 3.877 μm produces an
admissible-family d_ref value. **The DERIVER's Candidate B family
`R^N · λ_spaghettio` is only one of the possible ratio families.**
The blind DERIVER did not have the broader sealed record's
ratio-identification methodology visible; the CR013 whitelist by
design excluded it.

**Structural note.** CR005@21 opens explicit next-CR items in its
"What CR005 opens" §, including *"apply the partition-algebra +
Θ-unit framework to other items in the CR004 discrimination map"* —
Higgs, proton, neutrino splitting are named. **d_ref belongs in
that same list.** Not queued at time of CR005 seal because CR013
did not yet exist.

## Corrected read — CR245 + CR278 for Condition 2

**Locations.**
- `09a_PARTICLE_MASS_CHAIN/CR245_BINDING_CURVATURE_FROM_TYPED_
  SUBSTRATE/CR245_result.md` — sealed 2026-06-23 BOUNDARY,
  precommit sha `a4274eb1…`
- `09a_PARTICLE_MASS_CHAIN/CR278_NEUTRON_RULE_CONSOLIDATION/
  CR278_result.md` — sealed BOUNDARY (H-3 gauge-symmetry point),
  precommit sha `725307f5…`

**CR245 headline structural identity (theorem-grade).**

```text
(Q_mass − Q_sub)² / Q_mass  ≡  (N − Z)²/A · 7093² / (192 · 7117)
```

Verified EXACT on 71/71 rows under Fraction arithmetic. Zero free
parameters. Derives the Bethe-Weizsäcker asymmetry-term shape from
the SAM two-kernel structure.

**CR245 typed-candidate coefficient search (the load-bearing bit
for CR013 Condition 2).** For each BW-fit coefficient, CR245 built
a **finite deterministic candidate family** of typed rationals in
`{R, D, S, M, L, V, Θ, κ, g}` — atoms, reciprocals, products,
ratios — and reported nearest candidate per coefficient:

| Coefficient | Fitted (u) | Best typed | Value | Rel. dev. | ≤5% | ≤1% |
|---|---:|---|---:|---:|:---:|:---:|
| d (asymmetry) | 2.83e-2 | **1/(R·D) = 1/36** | 2.78e-2 | **1.91%** | ✓ | |
| c (coulomb)   | 7.57e-4 | 1/(S·L) = 1/1296 | 7.72e-4 | 1.90% | ✓ | |
| a (volume)    | 8.78e-3 | 1/(R·κ) = 64/7117 | 8.99e-3 | 2.48% | ✓ | |

CR245 identifies `d_asym = 1/(R·D)` as *"the single structurally
clean typed candidate — smallest possible denominator from
primitive atoms, both R and D primitives, no derived constants."*

**CR278 Rule 5.**

```text
Q_sub  =  8·Z·κ  +  (N − Z)·(1/8)
```

The excess-neutron source-support fee is `1/8 = Θ/R²` — the same
tensor share appearing in CR005@21's QNM derivation. One sealed
worked example of an R⁻² dressing (specifically Θ/R²) in a
coupling-law channel.

**Bearing on Condition 2.**

CR010 §3 S6 stipulated: *"R-power dressings in downstream coupling
laws are structural consequences of Home-nesting projection levels,
not device parameters."* The prior sweep tiered this as STIPULATED
because it declared existence without instantiation.

**CR245 + CR278 are the sealed instantiations.** In two independent
coupling contexts (nuclear binding asymmetry, nuclear
source-coupling excess-neutron fee), the structural dressings are:

- `1/(R·D) = R⁻¹·D⁻¹` — nuclear asymmetry curvature (CR245)
- `Θ/R² = R⁻²·Θ¹` — excess-neutron source-support (CR278)

Both are specific substrate-atom ratios, not free R^N with N chosen.

Applied to CR013's Condition 2 (`d_ref = R^N · λ_spaghettio` from
CR010 §1.8 Home-nesting family): the sealed pattern says **d_ref is
a specific substrate-atom ratio times the loop scale, and the
specific ratio is derived from the SLC coupling context**. The
DERIVER left this UNDERDETERMINED because the CR013 whitelist did
not include the CR245/CR278/CR005@21 discipline.

**Concrete methodology from CR245 applicable to d_ref:**

1. Pre-commit a finite deterministic candidate family for d_ref of
   the form `d_ref = (typed rational in CR238 atoms) × λ_spaghettio`
2. Compute nearest structural clean candidate per selection
   criterion (smallest denominator, primitives only, etc.)
3. Report tier per candidate; identify structurally clean matches
4. Run wrong controls (perturbing R, D, S, Θ) as CR245 did

This is a directly buildable structural CR that inherits CR245's
sealed methodology. Not option E's G-series companion; a Courtroom-
native structural CR.

## Corrected read — QP091Y as SAM's paradigm, not "different context"

The QP-sweep sub-agent tiered QP091Y as *"different coupling
context (surface debit / matter-branch), doesn't close CR013
Condition 2 which specifically asks about the write-to-read
pop-bounce-intersect mechanism."* That framing was wrong.

**QP091Y is not "different"; it is the QP-side sister of CR245**:

- QP091Y searches for R^n structural exponents in surface-debit
  coefficient laws
- CR245 searches for R-power ratios in nuclear binding coefficients
- Both use the same substrate-atom family `{R, D, S, ...}`
- Both find "structurally clean, coefficient closure open" state

QP091Y's next-frontier note *"freeze n, then derive native menu/
value selection"* is the same discipline CR245 applies at BOUNDARY.
The two form one arc; both are the SAM way of asking Condition 2's
question in specific coupling contexts.

For CR013, this means the sealed toolkit for closing Condition 2 is
already available and battle-tested across matter-branch and
QP-side. **The write-to-read pop-bounce-intersect mechanism is not
a special case exempt from that toolkit; it is the next context
awaiting the same treatment.**

## Consolidated corrected picture

| Condition | Previous read | Corrected read |
|---|---|---|
| 1 — Regime ID | Strong candidate (QP038 + CR103a) needs bridge | **Unchanged.** Prior read was correct. |
| 2 — Projection N | Partial, weak | **Instantiated by CR245/CR278/QP091Y.** The R-power-dressing pattern is sealed in multiple contexts; d_ref simply needs its own CR245-style typed-candidate search. |
| 3 — Mean-free-path | Open, contingent bypass via Cond. 1 | **Unchanged.** Still open. |
| 4 — Absolute observable | Open, no candidate in Courtroom | **Instantiated by CR005@21.** SAM does absolute observables via substrate-atom ratio × external scale, at zero free parameters. d_ref is the same structural pattern awaiting its ratio identification. |

## Updated ranked options

**Option F (new, promoted to top rank) — CR245-methodology d_ref
typed-candidate search.**

Draft a Courtroom-native structural CR that applies CR245's sealed
methodology to d_ref:

- Precommit a finite deterministic candidate family:
  `d_ref = (typed rational in {R, D, S, M, L, V, Θ, κ, g, ĥ, d̂}) × λ_spaghettio`
- The candidate family is chosen from the sealed CR238 atom set,
  not tuned; the CR245 precommit's family is the template
- Selection criteria: primitives-only preferred, smallest
  denominator preferred, structural context justified per candidate
- Wrong-controls perturb R, D, S, Θ (as CR245 did)
- Report structurally clean candidates by tier; the CR does NOT
  assert d_ref equals any of them — it seals the typed-family
  landscape that CR011 originally computed informally

**Anti-retrofit under this option.** The candidate FAMILY is
pre-committed (finite, deterministic, drawn from sealed CR238
atoms). The output is a ranked list, not a chosen value. That is
the CR245 discipline exactly. Anti-retrofit is honored by the
family being sealed before the search runs.

**Expected outcome.** CR245 landed BOUNDARY: theorem-grade structure
plus multiple within-5% candidates plus one structurally clean
match (`1/(R·D)`). A d_ref version would likely land similarly —
one to a few structurally clean candidates, no unique closure but
now-sealed candidate landscape. That is real structural progress
even without unique closure, and it upgrades Condition 2 from
"UNDERDETERMINED with 4 admissible candidates enumerated
informally" to "UNDERDETERMINED with N admissible candidates
sealed with tier tags and wrong-controls."

**Option G (new) — CR005@21-methodology "d_ref is a substrate
ratio × loop scale" derivation attempt.**

Analogous to how CR005@21 derived `ω_R·M = 3/8` from partition-
algebra overflow + closure axiom + Θ-unit accounting, attempt a
first-principles derivation of the substrate-atom ratio that
governs write-to-read reach. If a specific partition-algebra
argument closes at a specific ratio (e.g., `Θ/R²` if the tensor-
share is the right substrate quantity, or `d̂/S` if the QNM-family
is), that would be theorem-grade Condition 2 closure.

Higher risk than Option F. Higher reward.

**Options A / B / C / D / E** (from prior sweeps) remain admissible
but Options F and G now rank ahead of A and B given the sealed
CR245 + CR005@21 methodology precedent.

## Framing lesson for future sweeps

The cleanroom's purpose is derivation blindness during drafting.
Once a cleanroom CR seals, interpretation returns to the full
sealed record. Any prior sealed CR that bears on the result is
legitimate evidence. Applying cleanroom quarantine rules to
interpretation is the mistake this addendum corrects.

If a specific downstream apparatus CR is later drafted, IT should
be drafted under cleanroom discipline (per the CR012 lesson), but
the interpretive scan around CR013's result is not the same
activity.

## Change log

```text
v1.0  2026-07-03  Addendum written by SCRUBBER-lineage session
                  ("big-brother", session id 0ea2cc6e…) after Sean
                  flagged the framing error and pointed at CR005@21
                  QNM derivation and the CR245/CR278/binding arc.
                  Prior CRs read directly: CR005@21_result.md,
                  CR245_result.md, CR278_result.md. Findings
                  integrated with the sub-agent sweeps. Supersedes
                  the strict "different context, doesn't apply"
                  read of QP091Y and the misdirected CR005 dismissal
                  in the earlier sweep artifacts. Prior sweep
                  artifacts left in place per repo discipline
                  "never rewrite sealed; use sidecar."
```
