# CR005d Continuous Starbreaker Flow and Carrier-QNM Source Bridge Precommit

Campaign: `CR005d_STARBREAKER_CONTINUOUS_FLOW_AND_CARRIER_QNM_SOURCE_BRIDGE`  
Classification: `CONSTRUCTIVE_CONTINUOUS_DYNAMICS_AND_SOURCE_BRIDGE`  
Same-run repair: `PROHIBITED`

## Frozen question

CR005c found a stable local ordering on affine paths, but explicitly left open
whether that ordering survives a prospective continuous Starbreaker evolution.
This campaign takes the larger step:

> Does a zero-fit continuous spherical flow preserve
> `tau_Theta_escape < tau_closure`, and do the separated carrier histories
> construct a coherent trace-free source that can drive the sealed SAM QNM
> response without pretending that the result is physical strain?

The continuous rule, source tensor, gates, populations, grids, and verdict
ladder are frozen here before any CR005d result is opened.

## Continuous kinematic law

The clock is structural phase time, not seconds. For one atom, convert the
frozen source positions to spherical coordinates.

Collapse, `0 <= t <= 1`:

```text
r(t)     = r0 exp[t ln(rc/r0)]
theta(t) = theta0
phi(t)   = phi0
```

The exact zero-radius limit is handled continuously. Source custody must show
that collapse is radial before this law is accepted.

Release, `s=t-1`, `0 <= s <= 1`:

```text
r(s)     = rc + s (r1-rc)
theta(s) = thetac + s (theta1-thetac)
phi(s)   = phic + s wrap(phi1-phic)
```

`wrap` is the unique shortest branch in `[-pi,pi)`. The velocity change at
`t=1` is an explicit bounce impulse. This is a prospective continuous
kinematic lift of the frozen Starbreaker displacement budgets; it is not a
derived force field or hydrodynamic solution.

The lift has zero fitted parameters and must reproduce all source endpoints to
`1e-12`.

## Contact clock and primary inequality

The source-native local relation surface remains:

```text
d_carrier,matter = 0.076
```

For each transition relation, CR005d selects the earliest direction-compatible
crossing on a frozen 32-bin scan, then executes 40 bisection steps. A prefix of
up to 256 transitions per scenario is repeated at 64 bins and must agree to
`1e-9`.

The primary unit is one unique `(scenario_id, carrier_atom_index)`. For each
carrier:

```text
tau_escape  = earliest outward 010/110 crossing
tau_closure = earliest inward 101 crossing
margin      = tau_closure - tau_escape
```

The same discovery, validation, and final seed doors as CR005c remain frozen.
Strong timing support requires all six geometry-by-door cells above `0.50`
with positive median margins. Directional support retains the CR005c aggregate
rule. No threshold may be changed after execution begins.

## Carrier source tensor

Every typed carrier occurrence receives unit structural weight. No carrier is
assigned a physical mass or energy. On the post-bounce flow:

```text
Q_ab(t) = sum_i [x_i,a x_i,b - delta_ab r_i^2/3]
S_ab(t) = d^2 Q_ab/dt^2
P_Q     = integral ||d^3 Q/dt^3||_F^2 dt
```

The mutually exclusive source populations are `escape_only`, `return_only`,
and `dual`; `all_carriers` is also reported. Coherence is frozen as:

```text
C_Q = P_Q(sum of carriers) / sum_i P_Q(single carrier i)
```

The denominator equals the expectation under independent Rademacher sign
scrambling and therefore supplies a no-fit incoherent null.

Primary derivatives use `2L=324` equal intervals. The `L=162` interval grid is
the convergence control. The all-carrier median power and QNM-response
differences must remain within five percent.

## Sealed ringdown response

CR005 and CR005b are inputs only. Their exact coefficients are frozen as:

```text
omega_R M = 3/8
omega_I M = 4/45
g(u)      = exp[-(4/45)u] sin[(3/8)u] / (3/8)
```

CR005d causally convolves `S_ab` with this kernel. The response is explicitly a
dimensionless unit-clock candidate. The Starbreaker phase clock has not been
derived as mass-scaled physical time, so the response is not strain, a
frequency in hertz, luminosity, or a detector forecast.

## Evidence ladder

The full bridge verdict requires:

1. all construction, custody, endpoint, root, trace, convergence, and QNM
   kernel gates pass;
2. strong six-cell continuous-flow timing support;
3. `escape_only` median coherence exceeds one in both geometries and at least
   four of six frozen geometry-by-door cells;
4. `escape_only` median per-carrier source power exceeds `return_only` in at
   least four cells where both populations exist.

If timing is strong and the source is cleanly constructed but these directional
source-separation conditions are not met, the timing result and source
construction may still pass with source separation left open. If timing is only
directional, it receives the directional verdict. A construction failure is a
FAIL; a stable construction without stable timing is a BOUNDARY.

## Wrong and invariant controls

1. Verify every frozen source hash before and after execution.
2. Reconstruct 96 scenarios, 482,112 atoms, all complete ledgers, and the exact
   carrier-matter history census.
3. Verify all three stored endpoints and transition-root directions.
4. Repeat deterministic timing prefixes under rigid rotation and translation.
5. Require source azimuthal motion to differ from a radial-only control where
   azimuth changes.
6. Require `trace(Q)=0` numerically.
7. Require coarse/fine source and response convergence.
8. Require a zero source to produce zero response and a unit impulse to
   reproduce the sealed QNM kernel.
9. Read `3/8` and `4/45` exactly from the frozen source records; no coefficient
   search or fitting is allowed.
10. Emit no seconds, strain, luminosity, distance, signal speed, detector
    observable, or SAM registry mutation.

Stop after one complete frozen-door release. No same-run repair.
