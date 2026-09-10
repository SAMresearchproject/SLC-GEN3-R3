# CR005c Starbreaker Escape / Closure Observability Gate — Precommit

Campaign: `CR005c_STARBREAKER_ESCAPE_CLOSURE_OBSERVABILITY_GATE`  
Classification: `CONSTRUCTIVE_OBSERVABILITY_AND_SEMANTICS_GATE`  
Same-run repair: `PROHIBITED`

## Frozen question

Can the current frozen Starbreaker record support the proposed ordering

\[
\tau_{\Theta\text{-escape}} < \tau_{\rm closure}
\]

as an observed, non-tautological statement, and can returned `101` carrier
relations be distinguished operationally from ending-zero escape histories?

The gravitational-wave branch supplies the hypothesis only. Definitions of
closure, release surface, and escape time must come from Starbreaker’s stored
state. They may not be imported from the GW framing.

## Frozen semantic firewall

The current three-bit relation history has the stage order:

```text
seed -> collapse -> final
```

The bits mean geometric proximity at the frozen radius `0.076`. They do not,
without additional evidence, mean horizon state, Home closure, information
resolution, gravitational-wave release, or physical time.

The exact operational distinction to be tested is:

```text
101 : contact -> open -> returned contact
010 : open -> transient contact -> open
100 : contact -> open -> open
110 : contact -> contact -> open
```

`101` is therefore a returned relation and `010/100/110` are ending-zero
relations. That stage distinction is admissible. A physical timing law is not.

## Affine diagnostic frozen before execution

For each frozen `101` relation, the runner may use only the stored Cartesian
positions at seed, collapse, and final. On each leg it solves the exact roots of

```text
norm(relative_start + s*(relative_end-relative_start)) = 0.076
```

for `s in [0,1]`. The seed-to-collapse outward root is reported as
`lambda_release`; the collapse-to-final inward root is reported as
`lambda_return = 1+s`.

This is a piecewise-affine event coordinate, not a physical clock. Because a
`101` relation is inside at seed, outside at collapse, and inside at final, the
ordering `lambda_release < lambda_return` is entailed by its history code. The
runner must explicitly mark that inequality as tautological with respect to the
same pair’s return.

## Independent closure requirement

Promotion to a GW timing bridge requires a scenario-level closure observable
independent of the tested dyad, such as a future Home-seal state emitted by a
time-resolved Starbreaker engine. The following are rejected as substitutes:

1. the `101` pair’s own inward recrossing;
2. final `source_final_contact` selection;
3. final-fate labels;
4. the local `0.076` contact radius relabeled as a horizon;
5. an assumed physical duration between seed, collapse, and final.

## Frozen verdict rule

`PASS_GW_TIMING_BRIDGE_READY` requires an explicit cadence, an independent
event-closure state, an independently justified release surface, and a
non-tautological comparison on both returned `101` and ending-zero histories.

If the record supplies only the three ordered stages and local contact
crossings, the verdict is:

`BOUNDARY_STAGE_ORDERING_ONLY__PHYSICAL_ESCAPE_BEFORE_CLOSURE_NOT_IDENTIFIABLE__EVENT_CLOCK_REQUIRED`

Construction failure, source drift, or history misclassification returns the
FAIL verdict.

## Required next instrumentation if boundary is reached

- solver step or cadence;
- independent `home_seal_state` or equivalent scenario closure field;
- release-surface signed distance;
- carrier crossing direction and crossing step;
- returned and ending-zero populations evaluated on the same clock.

No Starbreaker engine or SAM registry mutation is allowed in this campaign.
