# CR241 Rest-Mass Candidate Holdout and Structural-Uniqueness Scan - PRECOMMIT

**Date:** 2026-06-23
**Classification:** HOLDOUT_AND_STRUCTURAL_UNIQUENESS_SCAN
**Status:** PRECOMMIT PACKET CANDIDATE - not yet run
**Branch:** 09a_PARTICLE_MASS_CHAIN
**Upstream:** CR238 substrate spine compaction; CR239 native mass/gravity bridge; CR240 rest-mass channel identification and binding-energy axis

## Scope

CR241 tests whether the CR240 rest-mass channel and strict-pass typed nucleon-scale candidates survive three anti-overfit gates:

1. Pure isotope holdout outside the CR239/CR240 curated 51-row isotope set.
2. Cross-anchor stability under a He-4 stress anchor.
3. Structural-uniqueness scan of a finite typed-expression grammar.

The controlling question is:

```text
Do the CR240 rest-mass channel and candidate typed scales survive holdout,
anchor swap, and typed-expression uniqueness scanning without post-data
expansion?
```

CR241 does not modify CR238, CR239, or CR240. It tests downstream stability of the CR240 extension.

## Execution Gate

This repository is preflight locked. The runner must not be executed directly.

Required execution form:

```powershell
python tools\run_sam_test.py --task "CR241 rest mass holdout and uniqueness scan" --script 09a_PARTICLE_MASS_CHAIN\CR241_REST_MASS_HOLDOUT_UNIQUENESS\CR241_runner.py
```

No CR241 result-producing script has been run as part of this precommit packet.

## Locked Upstream Spine

CR241 inherits the CR238/CR240 typed structure:

```text
F = 81
S = 8
alpha_H = 2
D = 3
R = 12
L = 162
V = 27
Theta = 18
M = 126
kappa = 7117/768
g = 1/64
```

Rest-mass channel from CR240:

```text
G_mass(Z, N) = A * kappa / alpha_H = A * kappa / 2
Q_mass(Z, N) = S * G_mass(Z, N) = 4 * A * kappa
mu_Q = 192u / 7117
m_SAM(P) = mu_Q * Q_mass(P) = A * u
```

Substrate/source-coupling channel remains unchanged:

```text
G_substrate(Z, N) = Z*kappa + (N-Z)*g
Q_substrate(Z, N) = S * G_substrate(Z, N)
```

## Live CR240 Candidate Inputs

CR240 sealed the candidate list C0-C8 and returned:

```text
CR240 verdict = STRONG_PASS_CR240_REST_MASS_CHANNEL_IDENTIFIED
CR240 Lane A RMS epsilon = 0.0020244110920340556
CR240 He-4 anchor abs relative drift = 0.0006508135325
CR240 strict-pass free-mass candidates:
  C5 strict vs m_p and H-1
  C6 strict vs m_p, m_n, and H-1
  C7 strict vs m_p, m_n, and H-1
```

CR241 may weaken or falsify the downstream candidate-survival and uniqueness claims. It may not promote any candidate to theorem grade.

## Guardrail

CR241 may falsify or weaken a proposed:

```text
rest-mass channel
free-nucleon candidate
binding-residual model
candidate uniqueness claim
```

It does not falsify the CR238 substrate kernel unless a CR238 typed identity, CR221 bit-identical match, CR232 matter-gate regrade, or CR233 role identity is contradicted.

Disallowed wording:

```text
CR241 falsifies the CR238 substrate kernel.
```

Allowed wording if CR241 fails:

```text
CR241 falsified the specific CR240 candidate extension or uniqueness claim
under holdout or grammar scan.
```

## Layer 1 - Pure Isotope Holdout

### Locked Holdout Set

The holdout input file is:

```text
09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/CR241_holdout_isotope_input.csv
```

The locked holdout list is:

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

The draft list previously named Pb-208 and U-235. They are explicitly excluded because both appear in the CR239/CR240 curated isotope set. They are replaced by Pb-206 and U-234.

### Holdout Collision Guard

The runner must load:

```text
09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_measured_isotope_masses.csv
09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL/CR240_extended_kernel_predictions.csv
CR241_holdout_isotope_input.csv
```

The runner must fail before scoring if any CR241 holdout isotope appears in either CR239/CR240 curated isotope surface.

Precommit orientation found:

```text
holdout collisions = []
```

### Holdout Source

The holdout atomic masses are copied into the CSV from:

```text
AME2020 mass_1.mas20 via AMDC/IAEA
https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt
```

The CSV hash seals the exact values used by CR241. The runner must use the CSV as authority, not fetch fresh values during execution.

### Calculations

For every holdout isotope:

```text
m_SAM(P) = A * u
delta_m(P) = m_measured(P) - A * u
binding_defect_u(P) = A * u - m_measured(P)
epsilon(P) = delta_m(P) / m_measured(P)
```

`delta_m(P)` is usually negative for bound nuclei. `binding_defect_u(P)` is the positive binding-defect version and is reported for interpretability.

Aggregate:

```text
RMS epsilon
Max |epsilon|
Fraction with |epsilon| < 0.001
Fraction with |epsilon| < 0.005
Fraction with |epsilon| < 0.01
```

Residual axes:

```text
A
Z
N
N-Z
(N-Z)^2
A^(2/3)
Z^2 / A^(1/3)
Z(Z-1) / A^(1/3)
delta_pairing
magic_distance
radix_cycle_position = (Z-1) mod R
```

Primary nuclear axes for Layer 1 structure:

```text
(N-Z)^2
A^(2/3)
Z(Z-1) / A^(1/3)
delta_pairing
magic_distance
```

For each axis:

```text
Spearman rho_S(delta_m, axis)
Spearman rho_S(binding_defect_u, axis)
linear r^2(delta_m, axis)
linear r^2(binding_defect_u, axis)
```

Layer 1 strong structure passes if:

```text
RMS epsilon < 0.01
and at least two primary nuclear axes have |rho_S(binding_defect_u, axis)| > 0.5
```

Layer 1 boundary structure passes if:

```text
RMS epsilon < 0.01
and at least one primary nuclear axis has |rho_S(binding_defect_u, axis)| > 0.5
```

Layer 1 must not require C5/C6/C7 to match bound-isotope m/A directly. Those candidates are free-nucleon/typed-scale candidates, while bound isotopes carry binding-energy depression.

## Layer 2 - Cross-Anchor Stability

Re-anchor at He-4:

```text
mu_Q_He4 = m(He-4) / Q_mass(He-4)
Q_mass(He-4) = 4 * A * kappa = 16*kappa
anchor_drift = mu_Q_He4 / mu_Q - 1
```

Then recompute C0-C8 without changing candidate formulas.

Report for every candidate:

```text
candidate_id
candidate_value_C12
candidate_value_He4
rank_under_C12_anchor
rank_under_He4_anchor
rank_shift
```

Candidate rank is by absolute residual. Candidates within 10 ppm of each other share rank.

C0-C7 are evaluated against:

```text
m_p_measured
m_n_measured
m(H-1)_measured
average Lane A per-nucleon baseline
```

C8 is evaluated only against splittings:

```text
m_n - m_p
m(H-1) - m_p
1u - mu_Q * (4*kappa - 8*g)
```

Stability tiers:

```text
EXCEPTIONAL_ANCHOR_STABILITY: |drift| < 100 ppm
ANCHOR_STABLE:                |drift| < 1000 ppm
CONSISTENT_WITH_CR240_WC2:    |drift| < 5000 ppm
ANCHOR_UNSTABLE:              |drift| >= 5000 ppm
```

Candidate stability pass:

```text
The CR240 strict-pass family {C5, C6, C7} remains represented in the top 3
for at least two of the free-mass reveal targets {m_p, m_n, H-1}, and no
new unprecommitted candidate is introduced.
```

Target-specific CR240 baselines:

```text
m_p winner under C-12 = C5
m_n winner under C-12 = C7
H-1 winner under C-12 = C6
avg Lane A winner under C-12 = C0
```

A candidate that clears under C-12 but loses rank severely under He-4 is treated as an anchor artifact unless a structural explanation was predeclared here. No such exception is predeclared.

## Layer 3 - Structural-Uniqueness Scan

The scan may use only typed atoms/readouts from the CR238/CR240 spine:

```text
F, S, alpha_H, D, R, M, L, V, Theta, g, kappa
```

Canonical values:

```text
F = 81
S = 8
alpha_H = 2
D = 3
R = 12
M = 126
L = 162
V = 27
Theta = 18
g = 1/64
kappa = 7117/768
```

Allowed small fractions:

```text
g
g/alpha_H
1/R
1/R^2
1/M
1/L
1/(S*L)
1/(D^2*S)
Theta/(R^2*S)
Theta/(L*S)
1/(alpha_H*R^2)
1/(alpha_H*M)
1/(D*R^2)
1/(D*M)
```

Primary nucleon-window expressions:

```text
C = 1 + f
C = 1 - f
C = 1 + f1 + f2
C = 1 + f1 - f2
```

Diagnostic splitting-window expressions:

```text
C_delta = f
C_delta = f1 + f2
C_delta = f1 - f2
```

Maximum expression depth is 2. No arbitrary multiplication chains, no floating decimal constants, and no post-reveal expression expansion are allowed.

Target windows:

```text
nucleon-mass candidate window = [1.005, 1.010]
splitting diagnostic window   = [0.0005, 0.0015]
```

Canonicalization:

```text
Equivalent rational values are counted once per expression family.
When multiple expressions evaluate to the same rational, retain the lowest
complexity expression and keep aliases in an aliases column.
```

Complexity score:

```text
complexity_score = atom_count + operator_count + nesting_depth + distinct_primitive_class_count
```

Report:

```text
expression
evaluated_value
target_window
complexity_score
uses_candidate_family
distance_to_m_p
distance_to_m_n
distance_to_H1
N_hits_nucleon_window
N_hits_splitting_window
lowest_complexity_hits
rank_of_C5
rank_of_C6
rank_of_C7
rank_of_C8
```

Strong uniqueness:

```text
N_hits_nucleon_window <= 5
and at least one of C5, C6, C7 is among the top 3 lowest-complexity hits.
```

Moderate uniqueness:

```text
N_hits_nucleon_window <= 12
and at least one of C5, C6, C7 is among the top 5 lowest-complexity hits.
```

Uniqueness fail:

```text
N_hits_nucleon_window > 12
or C5/C6/C7 do not rank as low-complexity hits.
```

## Candidate Set

Candidates inherited from CR240:

```text
C0 = mu_Q * 4*kappa
C1 = mu_Q * (4*kappa - 8*g)
C2 = mu_Q * (4*kappa + 8*g)
C3 = mu_Q * 4*kappa * (1 + g)
C4 = mu_Q * 4*kappa * (1 + 1/(D^2*S))
C5 = mu_Q * 4*kappa * (1 + 1/R^2)
C6 = mu_Q * 4*kappa * (1 + g/alpha_H)
C7 = mu_Q * 4*kappa * (1 + 1/M)
C8 = mu_Q * 4*kappa * (1/(S*L))
```

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

## Wrong Controls

WC seeds are locked here:

```text
WC1 random holdout isotope set seed = 20260623
WC2 random isotope anchor seed = 20260624
WC3 expression grammar expansion seed/tie order = 20260625
WC5 primitive-label shuffle seed = 20260626
```

### WC1 - Random Holdout Isotope Set

Replace the frozen holdout list with a seeded random list of equal size from the available isotope pool, excluding CR239/CR240 curated rows.

Expected:

```text
qualitative residual-axis structure may remain,
but candidate survival or isotope-specific claims should not improve artificially.
```

### WC2 - Random Isotope Anchor

Re-anchor at one seeded random isotope rather than C-12 or He-4.

Expected:

```text
anchor stability degrades or candidate ranking changes.
```

### WC3 - Expression Grammar Expansion

Allow expression depth 3.

Expected:

```text
N_hits_nucleon_window increases.
```

### WC4 - Expression Grammar Contraction

Allow only:

```text
C = 1 +/- f
```

Expected:

```text
C5, C6, C7 should still appear if they are truly low-complexity.
```

### WC5 - Shuffled Primitive Labels

Shuffle labels among:

```text
R, M, L, V, Theta, S
```

while preserving numeric values in the expression generator.

Expected:

```text
typed-source explanations break even if arithmetic windows still contain hits.
```

## Control Integrity Clause

STRONG or BOUNDARY verdict requires all:

```text
all wrong controls complete
WC3 grammar expansion does not reduce N_hits_nucleon_window
WC4 contraction still returns C5, C6, and C7 if they are truly low-complexity
WC5 shuffled primitive labels breaks typed-source explanations
```

## Verdict Tiers

STRONG_PASS_CR241_HOLDOUT_AND_UNIQUENESS requires all:

```text
Layer 1 RMS epsilon < 0.01
Layer 1 strong structure passes: at least two primary axes have |rho_S(binding_defect_u, axis)| > 0.5
Layer 2 anchor drift < 1000 ppm
CR240 strict-pass family {C5, C6, C7} remains top-3 represented under He-4
Layer 3 strong uniqueness passes
Control integrity clause passes
```

BOUNDARY_CR241_CANDIDATE_SURVIVES_PARTIAL requires all:

```text
Layer 1 RMS epsilon < 0.01
Layer 1 boundary structure passes: at least one primary axis has |rho_S(binding_defect_u, axis)| > 0.5
Layer 2 anchor drift < 5000 ppm
Layer 3 moderate uniqueness passes
Control integrity clause passes
```

FAIL_CR241_CANDIDATE_ARTIFACT if any:

```text
Layer 1 RMS epsilon >= 0.01
Layer 1 boundary structure fails
Layer 2 anchor drift >= 5000 ppm
Layer 3 uniqueness fail
Holdout collision guard fails
Disallowed claim appears in result or summary
Control integrity clause fails
```

Verdict precedence:

```text
FAIL guard violations override all pass tiers.
Then STRONG > BOUNDARY > FAIL by metric tier.
```

## Disallowed Claims

The result must not claim:

```text
CR241 proves the free neutron mass.
CR241 proves the free proton mass.
CR241 derives binding energy fully.
CR241 falsifies CR238.
C5/C6/C7 were discovered after data reveal.
The candidate list was expanded after seeing results.
He-4 replaced C-12 as the main anchor.
Direct script execution is a valid Courtroom result path.
```

Allowed claim under strong pass:

```text
CR241 shows that the CR240 rest-mass channel and its typed candidate scales
survive isotope holdout, cross-anchor stress, and primitive-expression
uniqueness scanning. Candidate(s) remain targets for a separate theorem-grade CR.
```

## Output Files

```text
09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/
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

## K-Gates

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | C-12 remains the shaping anchor; He-4 is stress-test only; holdout isotopes are reveal-only CSV inputs. |
| K2 | Falsification | Layer 1, Layer 2, Layer 3, wrong-control integrity, holdout-collision guard, and disallowed-claim guard all have explicit fail modes. |
| K3 | Target hygiene | Holdout list, candidate list, expression grammar, target windows, verdict tiers, seeds, and disallowed claims are locked before runner execution. |
| K4 | Typed inputs | Uses only CR238 typed primitives and CR240 candidate set. No new free parameter. |
| K5 | Reproduction | Runner must execute through `tools/run_sam_test.py` with the CR241 task name; direct `python CR241_runner.py` is not a valid Courtroom result path. |

## Rule of Immutability

CR241 must be sealed before runner execution.

If the holdout isotope list changes, the hash changes and the test must be re-sealed.

If the expression grammar changes, the test must be re-sealed.

If any candidate is added after reveal, the result is invalid.

---

**Precommit drafted by:** ChatGPT, at Sean Brady's direction
**Sealed by:** Sean Brady, 2026-06-23 [pending Sean's seal]
**Arc relation:** Downstream of CR238, CR239, and CR240
**Verdict spectrum:** STRONG_PASS / BOUNDARY_PASS / FAIL
