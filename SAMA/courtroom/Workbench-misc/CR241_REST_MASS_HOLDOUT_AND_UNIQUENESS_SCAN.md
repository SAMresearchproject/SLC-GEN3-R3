# CR241 — Rest-Mass Candidate Holdout and Structural-Uniqueness Scan

**Date:** 2026-06-23  
**Classification:** HOLDOUT_AND_STRUCTURAL_UNIQUENESS_SCAN  
**Status:** DRAFT / PRECOMMIT SCAFFOLD — to be sealed before runner execution  
**Upstream:** CR238 substrate spine compaction; CR239 native mass/gravity bridge; CR240 rest-mass channel identification + binding-energy axis

---

## Purpose

CR241 tests whether the CR240 rest-mass channel and its typed nucleon-scale candidates survive three anti-overfit gates:

1. **Pure isotope holdout:** re-run the rest-mass and binding-residual tests on isotopes not used in the CR239 / CR240 curated 51-row set.
2. **Cross-anchor stability:** re-anchor the rest-mass channel at He-4 instead of C-12 and test whether the ranked typed candidates remain stable.
3. **Structural-uniqueness scan:** search the allowed typed-expression grammar to determine whether C5 / C6 / C7 are rare low-complexity hits or merely members of a crowded formula space.

The central question is:

```text
Do the CR240 rest-mass channel and candidate typed scales survive holdout, anchor swap, and typed-expression uniqueness scanning without post-data expansion?
```

---

## Locked upstream spine

CR241 inherits the CR238 / CR240 typed structure:

```text
ℱ = 81
S = 8
α_H = 2
D = 3
R = 12
ℒ = 162
V = 27
Θ = 18
M = 126
κ = 7117/768
g = 1/64
```

Rest-mass channel from CR240:

```text
G_mass(Z, N) = A · κ / α_H = A · κ / 2
Q_mass(Z, N) = S · G_mass(Z, N) = 4 · A · κ
μ_Q = 192u / 7117
m_SAM(P) = μ_Q · Q_mass(P) = A · u
```

Substrate/source-coupling channel remains unchanged:

```text
G_substrate(Z, N) = Z·κ + (N−Z)·g
Q_substrate(Z, N) = S · G_substrate(Z, N)
```

CR241 does **not** modify CR238, CR239, or CR240. It tests holdout stability and structural uniqueness.

---

## Core guardrail

CR241 may falsify or weaken a proposed:

```text
rest-mass channel
free-nucleon candidate
binding-residual model
candidate uniqueness claim
```

It does **not** falsify the CR238 substrate kernel unless one of the CR238 typed identities, CR221 bit-identical match, CR232 matter-gate regrade, or CR233 role identity is contradicted.

Disallowed wording:

```text
"CR241 falsifies the CR238 substrate kernel."
```

Allowed wording if CR241 fails:

```text
"CR241 falsified the specific CR240 candidate extension / uniqueness claim under holdout or grammar scan."
```

---

# Layer 1 — Pure isotope holdout

## Purpose

Test the CR240 rest-mass baseline and binding-residual axis on isotopes outside the CR239 / CR240 51-row curated subset.

The holdout test must not re-anchor:

```text
μ_Q = 192u / 7117
```

remains fixed.

The holdout test must not add new candidates after reveal.

---

## Suggested frozen holdout list

Use approximately 20 isotopes not present in the CR239 curated subset. Suggested holdout set:

```text
Ti-46
Cr-52
Mn-55
Co-59
Y-89
Zr-90
Ba-138
Nd-142
Sm-152
Gd-158
Dy-162
Er-166
Yb-172
Hf-178
W-184
Os-190
Pt-194
Hg-202
Pb-206
U-234
```

The draft list previously named `Pb-208` and `U-235`. Those are excluded from
the CR241 holdout because both appear in the CR239 / CR240 curated isotope set.
They are replaced by `Pb-206` and `U-234`.

The final list must be written and hash-sealed before runner execution. In the
branch-local packet this is locked as:

```text
09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/CR241_holdout_isotope_input.csv
```

Required columns:

```text
isotope
Z
N
A
atomic_mass_u
mass_uncertainty_u
measurement_class
source_table
confidence_lane
notes
```

---

## Layer 1 calculations

For every holdout isotope:

```text
m_SAM(P) = A · u
Δm(P) = m_measured(P) − A · u
B_u(P) = A · u − m_measured(P)
ε(P) = Δm(P) / m_measured(P)
```

`Δm(P)` is usually negative for bound nuclei. `B_u(P)` is the positive binding-defect version and is reported for interpretability.

Aggregate:

```text
RMS ε
Max |ε|
Fraction with |ε| < 0.001
Fraction with |ε| < 0.005
Fraction with |ε| < 0.01
```

Then test residual axes:

```text
A
Z
N
N−Z
(N−Z)^2
A^(2/3)
Z^2 / A^(1/3)
Z(Z−1) / A^(1/3)
δ_pairing
magic_distance
radix_cycle_position = (Z−1) mod R
```

Primary nuclear axes for Layer 1 structure:

```text
(N−Z)^2
A^(2/3)
Z(Z−1) / A^(1/3)
δ_pairing
magic_distance
```

For each axis:

```text
Spearman ρ_S(Δm, axis)
Spearman ρ_S(B_u, axis)
linear r²(Δm, axis)
linear r²(B_u, axis)
```

---

## Layer 1 pass condition

Layer 1 strong structure passes if:

```text
RMS ε < 0.01
and at least two primary nuclear axes have |ρ_S(B_u, axis)| > 0.5
```

Layer 1 boundary structure passes if:

```text
RMS ε < 0.01
and at least one primary nuclear axis has |ρ_S(B_u, axis)| > 0.5
```

Preferred result:

```text
asymmetry, surface, Coulomb, pairing, or magic-distance axes remain dominant.
```

Layer 1 should not require C5 / C6 / C7 to match bound-isotope `m/A` directly. Those candidates are free-nucleon / typed scale candidates, while bound isotopes carry binding-energy depression.

---

# Layer 2 — Cross-anchor stability

## Purpose

Test whether the rest-mass channel and typed candidate rankings are artifacts of the C-12 anchor.

Re-anchor at He-4:

```text
μ_Q^He4 = m(He-4) / Q_mass(He-4)
```

where:

```text
Q_mass(He-4) = 4 · A · κ = 16κ
```

Then recompute the candidate numerical values under:

```text
μ_Q^He4
```

without changing candidate formulas.

---

## Cross-anchor calculations

Compute:

```text
anchor_drift = μ_Q^He4 / μ_Q − 1
```

Then for each candidate C0–C8:

```text
candidate_value_C12
candidate_value_He4
rank_under_C12_anchor
rank_under_He4_anchor
rank_shift
```

Candidate rank is by absolute residual. Candidates within 10 ppm of each other share rank.

For C0–C7, evaluate against:

```text
m_p_measured
m_n_measured
m(H-1)_measured
average Lane A per-nucleon baseline
```

For C8, evaluate against splittings:

```text
m_n − m_p
m(H-1) − m_p
1u − μ_Q · (4κ − 8g)
```

---

## Cross-anchor stability tiers

Do not use a single harsh ppm threshold. Use tiers:

```text
EXCEPTIONAL_ANCHOR_STABILITY:      |drift| < 100 ppm
ANCHOR_STABLE:                     |drift| < 1000 ppm
CONSISTENT_WITH_CR240_WC2:         |drift| < 5000 ppm
ANCHOR_UNSTABLE:                   |drift| ≥ 5000 ppm
```

Candidate stability pass:

```text
The best or top-3 candidate under C-12 remains best or top-3 under He-4.
```

A candidate that clears under C-12 but loses rank severely under He-4 is treated as an anchor artifact unless a structural explanation is predeclared.

---

# Layer 3 — Structural-uniqueness scan

## Purpose

Test whether C5 / C6 / C7 are structurally rare low-complexity hits, or whether many typed expressions land in the same nucleon-mass window.

No new candidate may be added after the runner sees data.

---

## Allowed atoms

The scan may use only typed atoms/readouts from the CR238 / CR240 spine:

```text
ℱ
S
α_H
D
R
M
ℒ
V
Θ
g
κ
```

Evaluated canonical values:

```text
ℱ = 81
S = 8
α_H = 2
D = 3
R = 12
M = 126
ℒ = 162
V = 27
Θ = 18
g = 1/64
κ = 7117/768
```

---

## Allowed small fractions

The scan grammar must be finite and predeclared. Allowed fractions:

```text
g
g/α_H
1/R
1/R²
1/M
1/ℒ
1/(S·ℒ)
1/(D²·S)
Θ/(R²·S)
Θ/(ℒ·S)
1/(α_H·R²)
1/(α_H·M)
1/(D·R²)
1/(D·M)
```

---

## Allowed expression forms

Primary nucleon-window expressions:

```text
C = 1 + f
C = 1 − f
C = 1 + f1 + f2
C = 1 + f1 − f2
```

Maximum expression depth:

```text
2
```

No arbitrary multiplication chains. No floating decimal constants. No post-reveal expression expansion.

Diagnostic splitting-window expressions:

```text
C_delta = f
C_delta = f1 ± f2
```

Maximum expression depth:

```text
2
```

---

## Target windows

Nucleon-mass candidate window:

```text
[1.005, 1.010]
```

This window contains the free proton / neutron / hydrogen atomic mass neighborhood.

Splitting diagnostic window:

```text
[0.0005, 0.0015]
```

This window contains small proton-neutron / hydrogen-proton scale differences.

---

## Structural uniqueness metrics

For each expression that lands in a target window, report:

```text
expression
evaluated_value
target_window
complexity_score
uses_candidate_family
distance_to_m_p
distance_to_m_n
distance_to_m(H-1)
```

Complexity score:

```text
1 point per atom
1 point per operator
1 point per nesting level
1 point per distinct primitive class used
```

Report:

```text
N_hits_nucleon_window
N_hits_splitting_window
lowest_complexity_hits
rank_of_C5
rank_of_C6
rank_of_C7
rank_of_C8
```

---

## Structural uniqueness pass condition

Strong uniqueness:

```text
N_hits_nucleon_window ≤ 5
```

and at least one of:

```text
C5, C6, C7
```

is among the top 3 lowest-complexity hits.

Moderate uniqueness:

```text
N_hits_nucleon_window ≤ 12
```

and at least one of:

```text
C5, C6, C7
```

is among the top 5 lowest-complexity hits.

Uniqueness fail:

```text
N_hits_nucleon_window > 12
```

or C5 / C6 / C7 do not rank as low-complexity hits.

---

# Candidate handling

Candidates inherited from CR240:

```text
C0 = μ_Q · 4κ
C1 = μ_Q · (4κ − 8g)
C2 = μ_Q · (4κ + 8g)
C3 = μ_Q · 4κ · (1 + g)
C4 = μ_Q · 4κ · (1 + 1/(D²·S))
C5 = μ_Q · 4κ · (1 + 1/R²)
C6 = μ_Q · 4κ · (1 + g/α_H)
C7 = μ_Q · 4κ · (1 + 1/M)
C8 = μ_Q · 4κ · (1/(S·ℒ))
```

No candidate may be promoted to theorem-grade in CR241.

Allowed output:

```text
CANDIDATE_SURVIVES_HOLDOUT
CANDIDATE_ANCHOR_STABLE
CANDIDATE_STRUCTURALLY_UNIQUE
```

Disallowed output:

```text
CANDIDATE_PROVEN
THEOREM_GRADE_NUCLEON_MASS
```

A candidate can become a CR242 target only if it survives CR241 and then passes a separate holdout or post-evaluation challenge.

---

# Handling m_p and m_n

The free proton and neutron masses are reveal positions only.

They may be used in:

```text
Gate 4 candidate deviations
WC no-binding kernel
candidate scoring
splitting diagnostics
```

They may not shape:

```text
μ_Q
κ
g
Q_mass
candidate generation
candidate list expansion
```

C-12 remains the only shaping anchor unless the layer explicitly enters cross-anchor mode, where He-4 is used only as a stability stress test.

---

# Wrong controls

## WC1 — random holdout isotope set

Replace the frozen holdout list with a seeded random list of equal size from the available isotope pool.

Expected:

```text
qualitative residual-axis structure may remain,
but candidate survival / isotope-specific claims should not improve artificially.
```

## WC2 — re-anchor at a random isotope

Re-anchor at one seeded random isotope rather than C-12 or He-4.

Expected:

```text
anchor stability degrades or candidate ranking changes.
```

## WC3 — expression grammar expansion

Allow expression depth 3.

Expected:

```text
N_hits_nucleon_window increases.
```

This tests whether the uniqueness claim is sensitive to grammar size.

## WC4 — expression grammar contraction

Allow only:

```text
C = 1 ± f
```

Expected:

```text
C5, C6, C7 should still appear if they are truly low-complexity.
```

## WC5 — shuffled primitive labels

Shuffle labels among:

```text
R, M, ℒ, V, Θ, S
```

while preserving numeric values in the expression generator.

Expected:

```text
typed-source explanations break even if arithmetic windows still contain hits.
```

This tests typing, not just numerics.

---

# Control integrity clause

STRONG or BOUNDARY verdict requires all:

```text
all wrong controls complete
WC3 grammar expansion does not reduce N_hits_nucleon_window
WC4 contraction still returns C5, C6, and C7 if they are truly low-complexity
WC5 shuffled primitive labels breaks typed-source explanations
```

---

# Verdict tiers

## STRONG_PASS_CR241_HOLDOUT_AND_UNIQUENESS

Requires all:

```text
Layer 1 RMS ε < 0.01
Layer 1 strong structure passes: at least two primary axes have |ρ_S(B_u, axis)| > 0.5
Layer 2 anchor drift < 1000 ppm
Top candidate rank remains stable under He-4 anchor
Layer 3 strong uniqueness passes
Control integrity clause passes
```

## BOUNDARY_CR241_CANDIDATE_SURVIVES_PARTIAL

Requires all:

```text
Layer 1 RMS ε < 0.01
Layer 1 boundary structure passes: at least one primary axis has |ρ_S(B_u, axis)| > 0.5
Layer 2 anchor drift < 5000 ppm
Layer 3 moderate uniqueness passes
Control integrity clause passes
```

## FAIL_CR241_CANDIDATE_ARTIFACT

Any of:

```text
Layer 1 RMS ε ≥ 0.01
Layer 1 boundary structure fails
Layer 2 anchor drift ≥ 5000 ppm
Layer 3 uniqueness fail
Control integrity clause fails
```

---

# Disallowed claims

The result must not claim:

```text
CR241 proves the free neutron mass.
CR241 proves the free proton mass.
CR241 derives binding energy fully.
CR241 falsifies CR238.
C5/C6/C7 were discovered after data reveal.
The candidate list was expanded after seeing results.
He-4 replaced C-12 as the main anchor.
```

Allowed claim under strong pass:

```text
CR241 shows that the CR240 rest-mass channel and its typed candidate scales survive isotope holdout, cross-anchor stress, and primitive-expression uniqueness scanning. Candidate(s) remain targets for a separate theorem-grade CR.
```

---

# Output files

```text
CR241_REST_MASS_HOLDOUT_UNIQUENESS/
  CR241_PRECOMMIT.md
  CR241_runner.py
  CR241_summary.json
  CR241_result.md
  CR241_holdout_isotope_input.csv
  CR241_holdout_predictions.csv
  CR241_holdout_residual_axes.csv
  CR241_cross_anchor_stability.csv
  CR241_expression_scan_hits.csv
  CR241_candidate_survival.csv
  CR241_wrong_controls.csv
  CR241_input_manifest.csv
  HASHES.txt
```

Branch-local output path:

```text
09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/
```

---

# K-gates

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | C-12 remains the shaping anchor; He-4 is stress-test only; holdout isotopes are reveal only. |
| K2 | Falsification | Layer 1, Layer 2, Layer 3, and wrong-control integrity all have explicit fail modes. |
| K3 | Target hygiene | Holdout list, candidate list, expression grammar, target windows, verdict tiers, and disallowed claims locked before runner execution. |
| K4 | Typed inputs | Uses only CR238 typed primitives and CR240 candidate set. No new free parameter. |
| K5 | Reproduction | Runner execution must go through `python tools\run_sam_test.py --task "CR241 rest mass holdout and uniqueness scan" --script 09a_PARTICLE_MASS_CHAIN\CR241_REST_MASS_HOLDOUT_UNIQUENESS\CR241_runner.py`; direct `python CR241_runner.py` is not a valid Courtroom result path. |

---

# Rule of immutability

CR241 must be sealed before runner execution.

If the holdout isotope list changes, the hash changes and the test must be re-sealed.

If the expression grammar changes, the test must be re-sealed.

If any candidate is added after reveal, the result is invalid.

---

**Precommit drafted by:** ChatGPT, at Sean Brady’s direction  
**Sealed by:** Sean Brady, 2026-06-23 [pending Sean’s seal]  
**Arc relation:** Downstream of CR238, CR239, and CR240  
**Verdict spectrum:** STRONG_PASS / BOUNDARY_PASS / FAIL
