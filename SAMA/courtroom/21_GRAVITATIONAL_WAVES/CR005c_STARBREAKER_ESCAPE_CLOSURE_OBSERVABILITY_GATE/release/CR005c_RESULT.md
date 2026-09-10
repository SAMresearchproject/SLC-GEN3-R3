# CR005c Starbreaker Escape / Closure Observability Gate — Result

## Primary verdict

`BOUNDARY_STAGE_ORDERING_ONLY__PHYSICAL_ESCAPE_BEFORE_CLOSURE_NOT_IDENTIFIABLE__EVENT_CLOCK_REQUIRED`

## What the current record does establish

The frozen Starbreaker history grammar cleanly distinguishes returned relations
from ending-zero relations:

```text
101 -> contact, open, returned contact
010 -> open, transient contact, open
100 -> contact, open, open
110 -> contact, contact, open
```

The complete record contains **8,340** history-`101`
relations and **59,191,245** ending-zero relations.

For all **8,340** frozen `101` relations, the exact
piecewise-affine Cartesian probe found one outward crossing on the
seed-to-collapse leg and one inward crossing on the collapse-to-final leg.
The median coordinates were:

```text
lambda_release = 0.566282338
lambda_return  = 1.132859211
open interval  = 0.617486748
```

This confirms the local near-far-near geometry. It does **not** establish a
physical timing law: `lambda` is a stage-normalized affine coordinate, and
`lambda_release < lambda_return` is already entailed by the `101` history bits.

## Why the GW timing bridge remains open

The current engine and frozen roster contain no physical or solver clock, no
independent Home/horizon seal state, and no independently justified release
surface. The radius `0.076` is a local contact threshold. A pair's own inward
recrossing cannot also serve as the independent event closure against which its
escape is tested.

Therefore the proposed inequality

```text
tau_Theta_escape < tau_closure
```

is not identifiable from the current record. Promoting it now would rename
stage order as physical time.

## Smallest next instrumentation

1. emit a solver step or cadence;
2. emit a scenario-level `home_seal_state` independent of the tested dyad;
3. emit signed distance to a separately defined release surface;
4. timestamp carrier crossing direction;
5. compare returned `101` and ending-zero `010/100/110` populations on that
   same clock.

No Starbreaker engine, SAM registry, prior verdict, or GW law was changed.
