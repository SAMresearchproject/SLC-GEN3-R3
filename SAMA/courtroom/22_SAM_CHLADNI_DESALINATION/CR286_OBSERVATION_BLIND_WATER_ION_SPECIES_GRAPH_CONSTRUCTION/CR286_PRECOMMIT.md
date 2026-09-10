# CR286 Precommit - Observation-Blind Water-Ion Species Graph Construction

Record ID: `CR286_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_CONSTRUCTION`

## Question

Can the nine CR284 water/ion identities be converted into complete typed graph
families for the CR285 passive-membrane comparison without opening or encoding
hydrated radii, preferred coordination measurements, dehydration energies,
transport barriers, membrane flux, rejection, or selectivity?

## Allowed Chemical Inputs

CR286 may use only:

- the frozen CR284 species identity and total formal charge;
- declared atom inventory and formula connectivity in the CR286 contract;
- a species-level virtual frame carrying total formal charge;
- one common CR120U-derived six-contact octahedral envelope hypothesis;
- two tetrahedral parity controls because CR120U does not globally exclude
  tetrahedral realization;
- one core-only control.

No bond order, bond angle, partial atomic charge, physical size, hydration
number, interaction energy, or membrane result is an allowed construction
input.

## Common Envelope Rule

Every species receives the same four variants:

```text
OCT6_PRIMARY       : -x, +x, -y, +y, -z, +z
TET4_EVEN_CONTROL  : 000, 011, 101, 110
TET4_ODD_CONTROL   : 001, 010, 100, 111
CORE_ONLY_CONTROL  : no hydration-support ports
```

The OCT6 primary is a common source-native hypothesis, not a measured
coordination assignment. Applying the same variants to all species prevents a
species-by-species rescue rule.

## Graph Construction

Each graph contains:

- the frozen core atoms;
- declared formula-connectivity edges without bond order;
- one virtual `SPECIES_FRAME` node carrying the total formal charge;
- one `FRAME_MEMBERSHIP` edge from each core atom to the frame;
- zero, four, or six coarse-grained `HYDRATION_WATER` nodes;
- one `HYDRATION_SUPPORT` edge per envelope port.

The frame is an accounting device. It is not a physical atom, carrier,
membrane site, or energy source.

## Precommitted Inventory

The fixed source contracts imply:

```text
species                  = 9
envelope variants        = 4 per species
graph candidates         = 36
primary OCT6 graphs      = 9
core atoms               = 29 per single roster traversal
core connectivity edges  = 20 per single roster traversal
all graph nodes           = 278
all graph edges           = 322
```

## Degeneracy Rule

CR286 may not invent an element-to-QP-triad selector. Species with identical
core topology and formal charge remain charge-typed topology ties:

```text
Na+  ~ K+
Mg2+ ~ Ca2+
```

Element symbols remain provenance labels, but they do not create a physical
shape difference by themselves. Candidate IDs may stabilize output order and
may not break a scientific tie.

## Explicitly Excluded

- observed or simulated coordination numbers;
- bare or hydrated radius;
- hydration/de-coordination free energy;
- bond lengths or angles;
- partial charges or force-field parameters;
- atomic-number modulo rules or isotope selectors;
- measured flux, rejection, selectivity, fouling, or specific energy;
- acoustic variables;
- Starbreaker variables;
- `M_native` as a physical dimension or energy;
- wall chemistry or pore functionalization;
- a claim that OCT6 is the physical hydration ontology.

## Pass Conditions

CR286 passes only if:

- every frozen source and contract file matches its SHA-256 digest;
- all nine species and all four common variants construct;
- the exact node/edge inventories close;
- every node and edge carries source provenance;
- no observed-target or physical-unit field appears in the graph schema;
- all primary graphs use the same OCT6 rule;
- both tetrahedral parities and the core-only control remain present;
- Na/K and Mg/Ca charge-typed topology ties remain explicit;
- no specific CR285 gate is selected;
- all wrong controls are rejected;
- no selectivity or physical membrane claim is emitted.

## Rule-9 Line

This test could have falsified observation-blind species construction through
an incomplete formula graph, species-specific envelope tuning, target leakage,
an invented element-to-triad map, broken provenance, hidden physical units, or
suppression of a topology tie.

## Expected Result Class

```text
CR286_PASS_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_FAMILY__36_CANDIDATES__COMMON_OCT6_PRIMARY__NO_GATE_RANKING_OR_PHYSICAL_PROMOTION
```
