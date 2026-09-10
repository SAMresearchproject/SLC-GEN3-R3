# CR285 SAM Passive Shape-Selective Membrane System

## System Name

```text
SPSM-01 = SAM Passive Shape-Selective Membrane, architecture version 1
```

## Current Claim

SPSM-01 is a passive topology and comparison system. It is not yet a membrane
material, molecular-dynamics result, fabricated pore, or desalination result.

## Architecture

```text
conventional structural support
-> entry vestibule
-> signed triangular entry face
-> CR120U octahedral gate cell
-> central passive traversal
-> complementary triangular exit face
-> optional face-shared cell continuation
-> conventional collection/support layer
```

The active geometric object is one of the 120 source-complete CR120U cell
templates. Each cell supplies eight directed gates by selecting any signed face
as the entry and its exact sign complement as the exit.

## Passive Design Variables

CR285 permits only source-native topological variables:

- `triad_candidate_id`;
- `triad_signature`;
- directed entry face state;
- complementary exit face state;
- positive integer chain length `C`;
- complete face-sharing incidence between adjacent cells.

The following conventional engineering fields remain externally supplied and
must never be inferred from QP counts without a typed physical bridge:

- membrane material;
- physical pore diameter and length;
- wall functional groups and surface charge;
- wet-state swelling and pore-size distribution;
- support thickness and mechanical strength;
- pH, salinity, pressure, temperature, and flow;
- fabrication tolerance and defect density.

## Why Complementary Faces

CR120U gives eight sign-oriented faces. A face and its three-bit complement use
opposite signed vertices on all three axes. This supplies a source-native
entry/exit pairing with no fitted direction and no observed transport target.

Same-face, one-bit-flip, two-bit-flip, and arbitrary exit selections remain
wrong controls. CR285 does not claim that the complementary route is physically
optimal; it identifies the cleanest source-native candidate to test.

## Array Construction

A membrane sheet may contain many passive gate cells in parallel. Parallel
replication changes candidate pore count and area; it does not alter the
internal topology of a gate. A serial pore is a complete face-shared chain.

For a linear `C`-cell chain:

```text
interfaces = C - 1
exposed faces = 6C + 2
external flow ports = 2
```

CR285 does not select `C` or map it to a physical thickness.

## Live Boundary

The construction catalog answers:

```text
What passive gate topologies follow from the latest frozen shape grammar?
```

It does not yet answer:

```text
Which water-ion construction is correct?
Which gate passes water?
Which gate rejects a particular ion?
What is the barrier in joules or kT?
Can the topology be fabricated economically?
```

Those are later gates, beginning with the observation-blind CR286 species
construction.
