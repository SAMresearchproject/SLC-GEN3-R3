# CR285 Passive Octahedral Membrane Construction Grammar Result

## Verdict

```text
CR285_PASS_PASSIVE_OCTAHEDRAL_MEMBRANE_CONSTRUCTION_GRAMMAR__960_DIRECTED_GATES__NO_SPECIES_SELECTIVITY_OR_PHYSICAL_PROMOTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASSIVE_MEMBRANE_TOPOLOGY_GRAMMAR
```

## Positive Readout

CR285 constructed 960 directed complementary-face gates and
480 undirected gate pairs from all 120 frozen CR120U
octahedral cell templates. Every gate has disjoint entry/exit vertices and
edges, complete source provenance, no acoustic dependency, and no Starbreaker
dependency.

The source `107` allowed / `13` surface-rejected split is preserved as source
metadata. No source template was silently deleted, and that particle-surface
label was not promoted into membrane performance.

## New Passive System

```text
QP093A triad template
-> CR120U V6/E12/F8 octahedral cell
-> signed triangular entry face
-> exact complementary exit face
-> optional complete face-shared chain
```

For a linear chain of `C` cells:

```text
I = C - 1
exposed_faces = 6C + 2
external_flow_ports = 2
```

## Scientific Boundary

This is a topology-grammar PASS. It emits no water-ion species graph, hydrated
radius, de-coordination barrier, compatibility score, pore size, membrane
material, flux, rejection, specific energy, fabricated hardware, or physical
desalination evidence. Equal future compatibility vectors must remain tied.

## Acoustic Status

The acoustic lane is preserved as `SHELVED_NOT_RETIRED`. It is not load-bearing
in SPSM-01 and can return only after a passive baseline exists and a complete
incremental energy/cost gate is passed.

## Rule-9 Line

This test could have falsified passive membrane construction through source
drift, incomplete cells, non-complementary ports, shared port incidence,
unresolved-role dependence, acoustic dependence, target leakage, or physical
unit invention.

## Next Gate

`CR286_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_CONSTRUCTION`
