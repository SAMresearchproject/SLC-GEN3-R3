# SAM Language v0.6 — exact SLC C1 simulator candidate

This candidate makes SAM Language itself the SLC C1 simulator kernel. A `.sam`
program is parsed, type-checked, authorized, and executed through the same
runtime that already carries the core and QP grammar. There is no sidecar
amplitude evaluator and no source-text dispatch.

The new formal profile executes an exact real 12-lebit state. Every amplitude
is stored as a signed integer divided by one power of `sqrt(2)`, so gate
execution, normalization, equality, and state hashing use integer arithmetic.

```sam
let s0: SLCState12 = SLC_ZERO_REGISTER()
let s1: SLCState12 = SLC_PREPARE_REQUEST(s0, L0)
let s2: SLCState12 = SLC_X1_RESPONSE(s1, L0, L1)
return s2
```

Run it with:

```powershell
sam run examples/slc_bell.sam --slc-c1-formal
```

## Installed formal surface

- `SLC_L0` through `SLC_L11`, with aliases `L0` through `L11`
- `SLC_ZERO_REGISTER()`
- `SLC_BINARY_FLIP(state, site)` — the current SLC binary B operation
- `SLC_PREPARE_REQUEST(state, site)` — the frozen real balanced request
- `SLC_X1_RESPONSE(state, control, target)` — the frozen ordered response
- `SLC_INSPECT_STATE(state)` — exact, read-only state and route dossier

The result contains separate hashes for state and route history. Star and chain
programs that reach the same GHZ vector therefore share a state hash while
retaining different history hashes. Inspection reports exact support,
normalization, site marginals, parity components, GHZ-like component structure,
and the ordered response route.

## Preserved frontier

The executable candidate is deliberately the complete *real two-operation*
formal C1 kernel inherited from SLCX002/SLCX003. Complex phase, publication and
Born sampling, physical connectivity, coupling cost, and hardware realization
remain separate interfaces; none is fabricated by the simulator.

The sealed source and semantic contract is `V0_6_SLC_C1_PRECOMMIT.md`. The
immutable parent is `SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE`.

