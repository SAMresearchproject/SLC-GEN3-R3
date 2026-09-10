# CR005c Starbreaker escape-before-closure timing operationalization precommit

Campaign: `CR005c_STARBREAKER_ESCAPE_CLOSURE_TIMING_OPERATIONALIZATION`  
Classification: `CONSTRUCTIVE_TIMING_OPERATIONALIZATION`  
Same-run repair: `PROHIBITED`

## Frozen question

The gravitational-wave branch proposes that carrier escape must outrun closure,
but its records do not define either time on the Starbreaker state surface.
This campaign asks the source-side question first:

> On the frozen Starbreaker three-stage carrier trajectories, do local
> carrier-matter ending-zero releases occur before returned `101` contacts
> close, and is that ordering stable across the frozen geometry and seed doors?

The gravitational-wave record supplies only the hypothesis. It supplies no
timing formula, threshold, or adjudication rule.

## Operational dictionary frozen before execution

Starbreaker stores seed, collapse, and final coordinates. They are assigned the
dimensionless affine parameters `0`, `1`, and `2`. Relative position is
piecewise-linearly interpolated between those stored states. This parameter is
not seconds and is not asserted to be physical continuous time.

The only source-native release surface available is the frozen relation surface:

```text
d_carrier,matter = r_contact = 0.076
```

- An outward crossing is a local contact release.
- An inward crossing is a local contact closure.
- This surface is not called a horizon.
- `100`, `010`, and `110` are ending-zero release histories.
- `101` is the returned-contact closure history.

For one segment, with relative endpoint vectors `a` and `b`, crossing time is
the root in `s in [0,1]` of:

```text
norm(a + s*(b-a))^2 = r_contact^2
```

The global stored-stage parameter is the segment start plus `s`.

## Primary unit and inequality

The primary unit is one unique `(scenario_id, carrier_atom_index)` occurrence,
not one relation edge. For each carrier:

```text
tau_escape      = earliest outward crossing among ending-zero relations
tau_escape_post = earliest outward crossing among 010 and 110 relations
tau_closure     = earliest inward crossing among 101 relations
margin          = tau_closure - tau_escape_post
```

The primary population contains carriers with both a post-collapse escape and
a `101` closure in the same scenario. The tested inequality is `margin > 0`.
Pre-collapse `100` exits are reported separately because their ordering before a
post-collapse `101` closure follows from the stored-stage labels and cannot be
used as the primary discovery.

## Frozen doors

```text
discovery:  seeds 910001 and 910002
validation: seed 910003
final:      seed 910004
geometries: localized_ledger_cells and dispersed_slots
```

No metric, threshold, population, exclusion, or definition may change after a
door is opened.

## Evidence ladder

`STRONG` requires all six geometry-by-door cells to contain primary carriers,
to have more than `0.50` of them satisfying `tau_escape_post < tau_closure`,
and to have positive median margin.

`DIRECTIONAL` requires:

```text
overall inequality fraction > 0.50
positive median margin in both geometries
at least four of six geometry-by-door cells above 0.50
```

Otherwise a source-reconciled construction is `BOUNDARY`. Any source,
enumeration, crossing, typing, or invariant failure is `FAIL`.

Scenario closure-front diagnostics are frozen at the `10th`, `50th`, and `90th`
percentiles of unique-carrier `101` closure times. They are descriptive and
cannot replace the primary carrier-occurrence comparison.

## Controls

1. Reconstruct the exact carrier-matter history census from the frozen atom
   roster and match the frozen aggregate.
2. Preserve the exact 96 scenarios, 482,112 atoms, 162-slot ledgers, and
   `18 carrier + 126 matter + 18 ledger_shadow` typing.
3. Require one valid crossing root and the correct normal-velocity sign for
   every transition.
4. Exchange pair endpoints; crossing times must remain invariant.
5. Apply a fixed translation and rigid rotation; crossing times must remain
   invariant.
6. Verify analytic synthetic inward and outward crossings.
7. Half-radius and double-radius controls must not reproduce the frozen census.
8. A wrong bit-order reading must not reproduce the asymmetric history census.
9. Emit no physical time, horizon, strain, luminosity, distance, signal speed,
   fitted parameter, or registry mutation.

## Interpretation ceiling

A positive result promotes a dimensionless, local, source-side timing interface
for a later GW bridge. It does not establish a physical time law. The next
physical step would require a genuine time-resolved Starbreaker evolution rule,
not interpolation dressed up as dynamics.

Stop after one complete frozen-door report. No same-run repair.
