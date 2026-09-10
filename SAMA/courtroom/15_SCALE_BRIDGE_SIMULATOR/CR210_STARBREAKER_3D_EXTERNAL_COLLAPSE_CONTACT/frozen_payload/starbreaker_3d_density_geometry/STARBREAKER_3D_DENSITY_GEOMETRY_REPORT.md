# Starbreaker 3D Carrier-Density Geometry Gate v0.1

Status: `PASS_INTERNAL_3D_GEOMETRY_GATE__EXTERNAL_PHYSICS_VALIDATION_OPEN`

Effect survival: `SURVIVES_3D_AND_LEDGER_LOCALIZATION_CONTROL`

## What changed

The prior complete-ledger allocations now inhabit true spherical-shell volume. Collapse radii and neighbor distances use `(x, y, z)`. The frozen neutral coefficients, anchors, seeds, typing rules, thresholds, and tensor accounting did not change.

Two geometries were locked before execution:

- `localized_ledger_cells`: each complete ledger is a fixed-radius spatial packet.
- `dispersed_slots`: the same complete ledger inventories are spread through the shell, removing packet localization.

## Locked result

The inward p=3 density allocation raises mean remnant fraction from 0.494604 to 0.788339 in localized ledger cells (delta +0.293735), and from 0.555535 to 0.819046 in dispersed slots (delta +0.263511). Both signs are stable in all 21 locked anchor/seed runs.

The collapse direction therefore survives 3D and does not require treating a ledger as a localized packet. The ejecta-residue mechanism does depend on localization: localized packets bind substantial residues that are suppressed by inward packing, while dispersed slots form almost no residue at either p=0 or p=3.

The wave readout is also geometry-sensitive. Localized p=3 is weak-leakage in all 21 runs. Dispersed p=3 reduces mean unlinked-tensor fraction by -0.282258, but remains above the burst threshold in all 21 runs. Numeric leakage suppression survives; the categorical wave transition does not survive the localization null.

## p=0 to p=3 effect inside each 3D geometry

Means cover three locked mechanism-audit anchors and seven locked holdout seeds.

| geometry | p | ledgers | localization radius | remnant delta | residue delta | unlinked-tensor delta | edges/atom delta | classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| localized_ledger_cells | 0 | 14 | 0.039365 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | geometry_baseline_null |
| localized_ledger_cells | 1 | 21 | 0.039413 | +0.100396 | -0.087281 | -0.006070 | -0.386145 | robust_internal_3d_effect |
| localized_ledger_cells | 2 | 33 | 0.039625 | +0.209955 | -0.182727 | -0.025886 | -0.764207 | robust_internal_3d_effect |
| localized_ledger_cells | 3 | 56 | 0.039771 | +0.293735 | -0.259348 | -0.033004 | -1.108177 | robust_internal_3d_effect |
| dispersed_slots | 0 | 14 | 0.623784 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | geometry_baseline_null |
| dispersed_slots | 1 | 21 | 0.558582 | +0.083095 | +0.000567 | -0.067410 | +0.001715 | robust_internal_3d_effect |
| dispersed_slots | 2 | 33 | 0.481313 | +0.191655 | +0.001085 | -0.188982 | +0.000928 | robust_internal_3d_effect |
| dispersed_slots | 3 | 56 | 0.422041 | +0.263511 | +0.001491 | -0.282258 | -0.000903 | robust_internal_3d_effect |

## Same-total p=3 control

### localized_ledger_cells

| metric | inward p=3 | uniform same-total | inward - uniform |
| --- | ---: | ---: | ---: |
| remnant_fraction | 0.788339 | 0.498431 | +0.289908 |
| residue_fraction | 0.176635 | 0.427359 | -0.250724 |
| ejecta_fraction | 0.211661 | 0.501569 | -0.289908 |
| unlinked_tensor_fraction | 0.068727 | 0.099957 | -0.031230 |
| edges_per_atom | 0.732001 | 1.748551 | -1.016550 |
| residue_clusters_per_1000_atoms | 3.558831 | 7.600571 | -4.041740 |
| mean_residue_size | 54.192113 | 61.948645 | -7.756532 |
| mapped_ringdown_carrier_exposure | 0.008591 | 0.012495 | -0.003904 |

### dispersed_slots

| metric | inward p=3 | uniform same-total | inward - uniform |
| --- | ---: | ---: | ---: |
| remnant_fraction | 0.819046 | 0.551026 | +0.268020 |
| residue_fraction | 0.001680 | 0.020188 | -0.018508 |
| ejecta_fraction | 0.180954 | 0.448974 | -0.268020 |
| unlinked_tensor_fraction | 0.354731 | 0.590574 | -0.235843 |
| edges_per_atom | 0.007433 | 0.045383 | -0.037950 |
| residue_clusters_per_1000_atoms | 0.524901 | 6.272571 | -5.747669 |
| mean_residue_size | 3.060984 | 3.205406 | -0.144422 |
| mapped_ringdown_carrier_exposure | 0.044341 | 0.073822 | -0.029480 |

## Exhaustive 3D radial-permutation position

### localized_ledger_cells

| metric | aligned p=3 | permutation min | permutation max | lower percentile |
| --- | ---: | ---: | ---: | ---: |
| remnant_fraction | 0.788339 | 0.429385 | 0.788339 | 100.0% |
| residue_fraction | 0.176635 | 0.176635 | 0.485245 | 4.2% |
| ejecta_fraction | 0.211661 | 0.211661 | 0.570615 | 4.2% |
| unlinked_tensor_fraction | 0.068727 | 0.068022 | 0.106622 | 8.3% |
| edges_per_atom | 0.732001 | 0.732001 | 1.977524 | 4.2% |
| residue_clusters_per_1000_atoms | 3.558831 | 3.558831 | 8.886579 | 4.2% |
| mean_residue_size | 54.192113 | 52.539677 | 62.947847 | 12.5% |
| mapped_ringdown_carrier_exposure | 0.008591 | 0.008503 | 0.013328 | 8.3% |

### dispersed_slots

| metric | aligned p=3 | permutation min | permutation max | lower percentile |
| --- | ---: | ---: | ---: | ---: |
| remnant_fraction | 0.819046 | 0.482626 | 0.819046 | 100.0% |
| residue_fraction | 0.001680 | 0.001680 | 0.032087 | 4.2% |
| ejecta_fraction | 0.180954 | 0.180954 | 0.517374 | 4.2% |
| unlinked_tensor_fraction | 0.354731 | 0.350863 | 0.628107 | 8.3% |
| edges_per_atom | 0.007433 | 0.007433 | 0.060064 | 4.2% |
| residue_clusters_per_1000_atoms | 0.524901 | 0.524901 | 9.437726 | 4.2% |
| mean_residue_size | 3.060984 | 3.054669 | 3.417643 | 12.5% |
| mapped_ringdown_carrier_exposure | 0.044341 | 0.043858 | 0.078513 | 8.3% |

## Responsible boundary

This is a stronger geometry test, not a physical stellar simulation. The ledger packet radius and kinematic shell A proxy remain hypotheses; no hydrodynamic or relativistic field solution has been introduced.

Next gate: only if the effect survives both 3D geometries and same-total/permutation controls, compare the locked qualitative direction against one external collapse signature without fitting Starbreaker to it.
