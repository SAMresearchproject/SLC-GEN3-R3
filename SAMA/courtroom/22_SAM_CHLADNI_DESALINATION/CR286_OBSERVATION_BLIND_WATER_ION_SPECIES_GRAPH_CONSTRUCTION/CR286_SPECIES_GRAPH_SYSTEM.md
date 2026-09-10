# CR286 Observation-Blind Species Graph System

## Purpose

Create the species-side graph inventory required by the CR285 coefficient-free
compatibility operator without using the membrane/hydration observations that
the campaign is supposed to predict.

## Two Layers

Each graph has two separately typed layers:

1. `CHEMICAL_CORE`: formula atoms and declared connectivity without bond order,
   length, angle, partial charge, or force-field parameters.
2. `ENVELOPE_HYPOTHESIS`: a common coarse-grained hydration-support envelope
   applied identically to all species.

A virtual `SPECIES_FRAME` holds total formal charge and joins the core atoms to
the envelope. It is bookkeeping, not a physical particle.

## Primary and Controls

`OCT6_PRIMARY` is the only primary hypothesis because it is the latest
source-native CR120U shape. It is applied to every species without adjustment.

Both tetrahedral parities remain controls because CR120U explicitly leaves
tetrahedral physical realization open. `CORE_ONLY_CONTROL` measures how much of
a later comparison is supplied by the hydration-envelope assumption itself.

## Built-In Limitation

CR286 has no source-complete rule connecting element identity to one of the 120
QP triad templates. It therefore does not select a CR285 gate.

The construction is expected to preserve at least these charge-typed topology
ties:

```text
Na+  ~ K+
Mg2+ ~ Ca2+
```

If later selectivity requires those pairs to separate, the separation must come
from a pre-reveal sourced operator or from conventional physical inputs such as
size and chemistry. It may not be inserted after observing the answer and
called SAM-derived.

## Output Boundary

CR286 outputs graph candidates and structural degeneracy only. It does not
output preferred physical coordination, hydration number, pore compatibility,
de-coordination cost, permeability, rejection, or selectivity.
