# CR220 Particle Count Stability Simulation

Result: **CR220_PASS_PARTICLE_COUNT_STABILITY_SIMULATION__126_NATIVE_ELEMENT_FAMILIES__P_TO_G_AND_GR_REPRODUCES_CR119__Z_LE_83_PRODUCES_83_WITH_43_61_HOLES__REFERENCE_PATCH_PRODUCES_81__SAM_CLOCK_SELECTOR_REMAINS_OPEN**

## Direct Answer

The simulation produced the full **126-row native element-family surface** from
particle counts centered on `P -> G(P) -> GR(P)`.

For every generated primary row:

```text
P = Zp + Nn + Ze
quark address = (2Z+N)u + (Z+2N)d + Ze
GR(P) = Z*(proton_qA + electron_qA) + N*neutron_qA
G(P) = GR(P) / 8
retained = 7G(P)
```

The computed values match CR119 row-by-row:

- `GR(P)` matches `qA_total_primary`: 126/126
- `G(P)` matches `tensor_carrier_support_primary`: 126/126
- `7G(P)` matches `retained_write_support_primary`: 126/126

## What Stable Counts Produced

The run separates native production from reference CLOCK scoring:

- Native element-family closure produces **126/126** rows.
- HH001 reference CLOCK has **81 stable**, **37 radioactive**, and **8 frontier**
  rows.
- The best simple count threshold is **`Z <= 83`**, which produces **83**
  stable candidates. It matches all 81 reference-stable rows but also includes
  two reference-radioactive holes: `Z=43` and `Z=61`.
- Removing `Z=43` and `Z=61` produces exactly **81** and scores perfectly, but
  that is a **reference-patched** selector, not yet a SAM-native derivation.

## Native Selector Readout

- QP094A residual stable-anchor selector produced
  **30** candidates.
- Roworder skeleton radix-slot selector produced
  **85** candidates.
- Roworder skeleton-or-closed-shell selector produced
  **87** candidates.
- Closed shell alone produced **8** candidates.

These are real native structure selectors, but none is the completed physical
CLOCK/stability selector by itself.

## Interpretation

The cards are not needed for the engine. This run shows the engine layer:

```text
particle counts -> P address -> G/GR support -> 126 native element families
```

The strongest physical-stability clue from particle counts is the **83-count
threshold with two holes**. That gives a sharp next target: derive the `43/61`
holes natively, or show why they remain downstream exceptions.

## Boundary

This CR does **not** claim that SAM constants alone have derived the known
physical stable-isotope table. It shows that the P-centered count engine
reproduces the 126 element-family surface and that a simple count threshold gets
to 83 with exactly two reference holes before the 81-row CLOCK surface appears.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_component_selector.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_simulated_element_primary_rows_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_simulated_isotope_ladder_rows_214.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_selector_scores.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_threshold_search.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_particle_count_threshold_candidates_83.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/CR220_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR220_PARTICLE_COUNT_STABILITY_SIMULATION/HASHES.txt`
