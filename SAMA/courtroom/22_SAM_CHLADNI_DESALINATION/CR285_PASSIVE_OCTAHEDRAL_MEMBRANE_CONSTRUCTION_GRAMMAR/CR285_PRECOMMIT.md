# CR285 Precommit - Passive Octahedral Membrane Construction Grammar

Record ID: `CR285_PASSIVE_OCTAHEDRAL_MEMBRANE_CONSTRUCTION_GRAMMAR`

## Question

Can the latest frozen QP093A/CR120U shape result generate a complete passive
membrane-pore topology catalog and a no-fit compatibility grammar without
acoustic inputs, observed ion data, physical-unit promotion, or unresolved
particle/shape assignments?

## Source-Native Construction

CR120U freezes:

```text
one QP093A triad template
-> 6 signed-axis vertices
-> 12 cross-axis edges
-> 8 sign-oriented triangular faces
```

For each cell and each three-bit face state `b`, CR285 defines the exit face as
the bit complement:

```text
exit_bits = b XOR 111_binary
```

The entry and exit faces must be disjoint and opposite. Each of 120 cells has
eight directed entry states, producing:

```text
120 * 8 = 960 directed passive gate topologies
120 * 4 = 480 undirected opposite-face pairs
```

No measured or simulated water-ion observable selects a cell or face.

## Face-Shared Pore Chain

For a linear chain of `C >= 1` complete cells with `I = C - 1` complete
face-sharing interfaces, CR120U's incidence identity gives:

```text
8C = exposed_faces + 2I
exposed_faces = 6C + 2
```

This is a topological construction only. `C` is not assigned a physical
thickness, pore length, or energetic meaning in CR285.

## Frozen Compatibility Grammar

A future species construction and a passive gate are compared as typed graphs.
The comparison vector is lexicographic and coefficient-free:

```text
K = (
  invalid_type_matches,
  broken_species_contacts,
  added_support_contacts,
  remaining_graph_edits
)
```

Lower entries are preferred in that order. Equal vectors remain tied. A file
or candidate ID may stabilize display order but may not break a physical tie.

CR285 freezes the comparison grammar but emits no species graph and no
compatibility score. CR286 must construct species graphs without observed
hydrated radii, dehydration energies, permeability, rejection, or selectivity.

## Explicitly Excluded

- acoustic frequency, mode, strength, power, or conceptual escape index;
- Starbreaker `A`, ledger density, remnant, or collapse variables;
- `M_native` interpreted as nanometres, joules, pressure, or barrier energy;
- hidden-support rows assigned to faces;
- carrier rows assigned to vertices;
- particle rows assigned to membrane atoms or ions;
- observed water-ion data used to choose a topology;
- wall chemistry, surface charge, swelling, pore diameter, material, or
  fabrication method presented as SAM-derived.

## Pass Conditions

CR285 passes only if:

- all sealed sources match their byte counts and SHA-256 digests;
- all 120 source cell templates pass their frozen topology checks;
- exactly 960 directed and 480 undirected complementary-face gates construct;
- every entry/exit pair is complementary and vertex/edge disjoint;
- every gate retains the source triad and face provenance;
- the passive system and comparison grammar contain no acoustic or Starbreaker
  selector;
- all precommitted wrong controls are rejected;
- no species ranking, selectivity, physical pore size, material, or physical
  performance is emitted.

## Failure Conditions

CR285 fails on source drift, incomplete cells, non-complementary ports,
same-face routes, shared entry/exit vertices or edges, missing provenance,
weighted rescue coefficients, acoustic dependence, observed-target leakage,
or physical promotion.

## Rule-9 Line

This test could have falsified the passive membrane construction claim by
showing that the latest shape surface cannot produce complete complementary
entry/exit gates without topology defects, unresolved role assignments,
acoustic assistance, target leakage, or physical-unit invention.

## Expected Result Class

```text
CR285_PASS_PASSIVE_OCTAHEDRAL_MEMBRANE_CONSTRUCTION_GRAMMAR__960_DIRECTED_GATES__NO_SPECIES_SELECTIVITY_OR_PHYSICAL_PROMOTION
```
