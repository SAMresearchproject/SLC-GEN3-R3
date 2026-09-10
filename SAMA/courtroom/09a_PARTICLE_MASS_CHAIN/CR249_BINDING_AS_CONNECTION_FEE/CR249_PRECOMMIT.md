# CR249 — Binding as Substrate-Atom Connection-Fee Sum

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-24
**Input dataset:** [CR242_binding_dataset.csv](../CR242_SAM_BINDING_CURVATURE_DERIVATION/CR242_binding_dataset.csv) (71 nuclei)
**Provenance backing:** CR009 PASS (charged-triadic + charged-pair connection-fee form), CR247 STRONG_PASS (Z·phi_b + (N−Z)·phi_e), CR248 BOUNDARY (4-particle Phase A theorem-grade)
**Open finish:** CR242 BOUNDARY (BW fit, no derivation), CR245 BOUNDARY (asymmetry derived, other 4 BW shapes phenomenological), CR248 BOUNDARY (linear B_u insufficient)

---

## Question

Does the substrate-atom **connection-fee** structure verified at the particle
level by CR009 (= CR244 unequal-pair form `sign(a−b)·(|a−b|+D)/R⁴` and the
charged-triadic `(R+q+D)/R` form) extend to the **nuclear binding curvature**?

Specifically: can `B_u(Z, N) = A·u − m_measured` be derived as a **sum of
tensor-carrier mass-lifts** over the substrate-atom connections in the nucleus,
with **zero free parameters**, matching the 71-nucleus AME2020 dataset to
**within 0.005 MeV maximum discrepancy**?

```text
Per Sean's 2026-06-24 framing:

  "Tensor carriers are substrate atoms — they carry zero mass but have a
   mass lift. This masslift is 'taken' from the total MeV.
   I think this is binding."

  "For every MeV+1 there is a carrier tensor to connect the stable particles.
   The formula uses the MeV to calculate the shape, number and type of
   connections and perfectly calculates M_observed back to M_native."

CR249 tests whether candidate carrier-counting + connection-fee rules
reproduce the per-nucleus B_u to Sean's 0.005 MeV maximum target.
```

## Honest framing

- CR009 sealed the particle-level formula: `M_obs = M_nat · (R + sign·(q+D)) / R`
  for triadic, `(q+D)/R⁴` for charged pair, exact at K1 across the qp093a catalog.
- CR247 sealed the nucleon-decomposition: `Phi(Z,N) = Z·phi_balanced + (N−Z)·phi_excess`.
- CR248 sealed the four-particle Phase A identity; Phase B linear B_u failed (24.5 MeV RMS).
- CR245 derived the BW asymmetry shape; the other 4 BW shapes remain phenomenological.

**This CR's structural move:** abandon the BW decomposition; treat B_u as the
total **substrate-atom connection-fee charge** across the nucleus, with the
fee structure inherited from CR009/CR244 and the connection topology derived
from CR247/CR248 nucleon decomposition.

If a candidate rule matches all 71 nuclei to ≤ 0.005 MeV with zero free
parameters, the SOB block closes — every quantity in the substrate order
block is derived.

## Locked candidate rules (above the line)

Each rule expresses `B_u(Z, N)` as a sum over substrate-atom connections.
All constants are CR238 atoms or named derived rationals. Zero fitted
parameters in any rule.

### Substrate constants

```text
R = 12       (CR238)
D = 3        (CR238)
S = 8        (CR238)
alpha_H = 2  (CR238)
Theta = 18   (CR238)
F = 81       (CR238)
V = 27       (CR238)
M = 126      (CR238)
L = 162      (CR238)
kappa = 7117/768 = κ                        (CR221)
g = 1/64                                    (CR221)
mu_Q = 192/7117 u                           (CR240; Q→u conversion)
R4 = R^4 = 20736
```

### Rule R1 — Per-excess-neutron uniform fee (Au-197 anchor)

```text
B_u(Z, N) = (N − Z) · fee_per_excess
fee_per_excess = (F·S − 1 + D) / R^4 · mu_Q
             = (647 + 3) / 20736 · 192/7117
             = 650 · 192 / (20736 · 7117)
             ≈ 0.0008460 u
             ≈ 0.7881 MeV per excess neutron
```

Derivation: matches Au-197 B_u = 0.033 u exactly (39 × 0.000846).
**Prediction:** B_u(Z,N) = 0.000846 · (N − Z) u for every nucleus.

### Rule R2 — Per-A uniform fee (volume-only)

```text
B_u(Z, N) = A · D / R^4 · mu_Q
         = A · 3 · 192 / (20736 · 7117)
         ≈ 3.90e-6 u per nucleon
         ≈ 0.00364 MeV per nucleon
```

**Prediction:** B_u scales linearly with A, charge-independent.

### Rule R3 — Per-proton-neutron pair (Coulomb-like)

```text
B_u(Z, N) = Z · N · (|q_p − q_n| + D) / R^4 · mu_Q
         = Z · N · (1 + 3) / R^4 · mu_Q       (assuming |q_p − q_n| = 1)
         = Z · N · 4 / R^4 · mu_Q
         = Z · N · 4 · 192 / (20736 · 7117)
         ≈ 5.20e-6 · Z · N  u
```

**Prediction:** B_u scales with Z·N (proton-neutron pair count).

### Rule R4 — CR247 channel-gap (asymmetry-derived)

```text
B_u(Z, N) = (Q_mass − Q_sub) / R^4 · mu_Q · correction
         = (N − Z) · 7093/192 · 1/R^4 · mu_Q
         = (N − Z) · 7093/192 · 192/7117 · 1/R^4
         = (N − Z) · 7093 / (7117 · R^4)
         = (N − Z) · 7093 / (7117 · 20736)
         ≈ 4.808e-5 · (N − Z)  u
```

**Prediction:** B_u from the CR245-derived asymmetry channel `(Q_m − Q_s)`,
divided by R⁴ to apply the pair-connection-depth scaling.

### Rule R5 — Composite: CR247 base + asymmetry square (CR245 form)

```text
B_u(Z, N) = (N − Z)^2 / A · 1/(R·D) · K_asym
where K_asym = 7093^2 / (192·7117) · mu_Q = 7093^2/(192·7117) · 192/7117
              = 7093^2 / 7117^2
              ≈ 0.9933

         ≈ (N − Z)^2 / A · 1/36 · 0.9933  u
         ≈ (N − Z)^2 / A · 0.02759  u
         ≈ (N − Z)^2 / A · 25.69 MeV
```

**Prediction:** B_u dominated by CR245-derived asymmetry shape with typed
coefficient 1/(R·D) = 1/36. This was CR245's best typed candidate (1.9% off
fitted in BW shape; here applied directly as the only B_u contribution).

### Rule R6 — Sum: per-A volume + asymmetry square

```text
B_u(Z, N) = R2 + R5
         = A · 3·mu_Q/R^4 + (N − Z)^2/A · K_asym/(R·D)
```

**Prediction:** Volume + asymmetry combination, both substrate-typed.

## Locked tolerance ladder

Per Sean's 0.005 MeV maximum target (2026-06-24):

```text
Per-row delta in MeV: |B_u_observed - B_u_predicted| · 931.494

exact_match          : |Δ_MeV| <  0.005   (Sean's target ceiling)
close_match          : |Δ_MeV| <  0.05
approximate_match    : |Δ_MeV| <  0.5
systematic_miss      : |Δ_MeV| >= 0.5
```

## Locked verification gates

```text
V-1   All 6 candidate rules applied to every row in CR242_binding_dataset.csv
      (71 rows); per-row predicted B_u, |Δ|_u, |Δ|_MeV, classification
      reported in CR249_per_row_predictions.csv

V-2   Per-rule aggregate: max |Δ|_MeV, mean |Δ|_MeV, RMS_MeV, R²,
      classification counts, reported in CR249_rule_comparison.csv

V-3   Best-rule identified: the rule with lowest max |Δ|_MeV across all 71 nuclei

V-4   For the best rule: per-nucleus residuals reported with named rationale
      where the residual exceeds 0.005 MeV (Sean's ceiling)

V-5   Wrong-control: shuffle the (Z, N) → B_u mapping; verify max |Δ| inflates

V-6   Wrong-control: perturb R or D in the best-rule formula; verify max |Δ|
      inflates
```

## Locked verdict gates

```text
PASS conditions:
  P1  V-1 through V-6 hold
  P2  At least one rule R1..R6 produces max |Δ|_MeV ≤ 0.005 across all
      71 nuclei (Sean's target)
  P3  Wrong-controls inflate best-rule max |Δ|_MeV by ≥ 100×

BOUNDARY conditions:
  B1  Best rule max |Δ|_MeV in [0.005, 0.05] — within 10× of target;
      candidate is the right structural form but needs refinement
  B2  Best rule max |Δ|_MeV in [0.05, 0.5] — candidate captures the
      shape but the constants need adjustment
  B3  All six candidates fail individually but a documented superposition
      (linear combination of two named candidates) lands within 0.005 MeV

FAIL conditions:
  F1  Best rule max |Δ|_MeV > 0.5 across the 71 nuclei
      → connection-fee framing doesn't reduce binding-curvature to substrate
      atoms in the candidate-rule family; new structural insight needed
  F2  Runner crashes or audit incomplete
  F3  Wrong-controls fail to inflate (formula not load-bearing)
```

## APPEAL — boundary regrade path

Per Sean's policy (CR252 / CR005 / CR009 precedent):

A BOUNDARY result with a **named connection-counting rule** that captures the
shape but needs structural refinement (e.g., the per-excess fee depends on
Z or A in addition to N−Z) can be regraded to `PASS_REGRADED_FROM_BOUNDARY`
if the refinement is:

1. **Named** — the structural refinement is a specific named substrate-atom
   ratio or rule, not a fitted coefficient
2. **Bounded** — refinement applies to ≤ 3 specific nuclei (e.g., light-mass
   regime where shell-geometry effects dominate)
3. **Authorized** — Sean explicitly approves the refinement

A FAIL (F1) is not appealable. If all six candidates fail, the framework
needs a different connection-counting topology — that's a new CR.

## Wrong controls

```text
WC-1  Shuffle (Z, N) → B_u mapping (seed 20260624); apply best rule;
      verify max |Δ|_MeV inflates by ≥ 100×. Confirms the best-rule fit
      isn't generic to any (Z,N,B_u) triple.

WC-2  Perturb R from 12 → 10 in best rule formula; verify max |Δ|_MeV
      inflates by ≥ 100×. Confirms R is load-bearing.

WC-3  Perturb D from 3 → 2 in best rule formula; verify max |Δ|_MeV
      inflates by ≥ 100×. Confirms D is load-bearing.

WC-4  Substrate-atom integrity: confirm μ_Q = 192/7117 (CR240),
      R⁴ = 20736 (CR238), F·S − 1 = 647 (CR238 allowed_section).
      Confirms the rules use canonical substrate atoms.
```

## Outputs

```text
   CR249_PRECOMMIT.md                this file
   CR249_runner.py                   Python runner — tests all 6 rules
   CR249_per_row_predictions.csv     per-(rule × nucleus) predicted B_u
   CR249_rule_comparison.csv         per-rule aggregate metrics
   CR249_wrong_controls.csv          WC-1 through WC-4
   CR249_summary.json                verdict + best-rule + metrics
   CR249_result.md                   substantive result with per-cohort
                                      tables, residuals, structural reading
   HASHES.txt                        SHA-256 of all CR249 artifacts
```

## Cryptographic chain (inputs)

```text
   Binding dataset (71 nuclei):
   c:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/CR242_SAM_BINDING_CURVATURE_DERIVATION/
     CR242_binding_dataset.csv

   Particle-level connection-fee formula (verified):
   c:/VS/The_Courtroom/18_SAM_NATIVE_QC/CR009_CONNECTION_FEE_K1_REVEAL/CR009_summary.json (PASS)

   Substrate atoms canonical source:
   c:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/

   Upstream chain (read-only):
   CR009, CR221, CR238, CR240, CR242, CR244, CR245, CR247, CR248, CR252
```

## What CR249 DOES NOT do

- Does NOT derive the BW shapes (volume, surface, Coulomb, pairing) as
  separate terms — it abandons the BW decomposition in favor of direct
  connection-fee sum.
- Does NOT extend to nuclei outside the CR242 dataset (71 rows).
- Does NOT modify any upstream sealed CR.
- Does NOT fit any free parameter — every coefficient in every candidate
  rule is a CR238 atom or named derived rational.

## Sealed

Sean Brady, 2026-06-24. The candidate rules R1-R6, tolerance ladder,
verdict gates P/B/F, wrong controls, falsifiers all locked above the line.
The runner's enumeration across the 71-nucleus dataset is the test. The
verdict is what the data says.
