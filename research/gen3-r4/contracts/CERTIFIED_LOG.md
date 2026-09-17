# R4 certified logarithmic capabilities

SLC-GEN3-R4 / SLC-GEN3-CEV1-R4, build GEN3-CERTIFIEDLOG1-20260915.
All mathematical source projection, exact rational readouts and certified log
evaluation execute in the shared warm C++/GMP capability worker. Python validates
metadata, orchestrates refinement and stores authenticated records.

## Calls

Every call supplies `name` (1..128 characters) and a nonempty `source_binding`
object. Calculation names are immutable; refinements use a new name.

| Operation | Additional required fields | Result |
|---|---|---|
| GEN3_SPECTRAL_ADMIT | source, context | Signed source moments, exact norms, weights and omitted-mode allowance |
| GEN3_LOG1P_ENCLOSURE | record | Certified enclosure of log(1+Q) |
| GEN3_SPECTRAL_LOG_PROFILE | record, tau | Source-weighted spectral log, derivative interval and coefficient intervals |
| GEN3_SPECTRAL_REFINE | record | A successor readout using retained modes and updated controls |
| GEN3_SIGNED_TRANSPORT_LOG | context, initial_energy, increments | Exact log ratios formed after signed total-energy reconstruction |
| GEN3_SPECTRAL_EXPORT | — | Original record and its source/spectral dependencies, without native recomputation |

`record` names a previously admitted source or readout in the same checkpoint.
Its source binding must agree exactly. Callers cannot inject a purported native
spectral record. Export supports source, readout and transport records.

`context` has exactly `basis`, `units`, `reference`, `history`. Units and history
are nonempty objects. Units must explicitly declare dimensionless source (or
transport energy); every supplied unit label must be dimensionless. Reference is the string `"1"`, the provider's dimensionless
reference. A source basis is either a list of distinct scalar identities matching
the source length or `{"kind":"ORDERED_INDEX","size":s}`. Original history and
coordinate ordering remain attached to the source. A transport context retains
the explicitly supplied basis of that history.

## Registered mathematical source

`MEAN_CUT_V1` admits exact rational vectors of length 1..65536:

    M = sum a_i
    Q = M²/s + sum_(r=1)^(s-1) (sum_(i<r) a_i - r M/s)²/[r(s-r)]
    lambda_0 = 1; lambda_k = 1/[k(k+1)] for k>=1
    A_k = sum a_i p_k(i); w_k = A_k² / ||p_k||²

The compact native record's `mean` field retains the signed sum M, not M/s.
For retained degrees 0..m, the exact residual mass is `sum a_i² - sum w_k`.
The remaining energy is between zero and this mass times lambda_(m+1).
At full degree the tail is exactly zero. Negative residuals reject.

This eigenvalue rule belongs to the registered mean/cut kernel. Arbitrary A3D41
exchange operators are not admitted under that rule. The installed small-matrix
operator-log API remains available separately, with its original limits.

The scalar target is `log(1+Q)`. The spectral target is
`sum w_k log(1+tau lambda_k)`. They remain distinct, and neither is log determinant.
Tau is an exact nonnegative rational. Derivative and power-series coefficient
readouts carry exact omitted-mode bounds; the formal series declares its scope.

## Controls and status

- Admission: optional `max_degree`, default 0, at most min(s-1,256).
- Scalar/profile: optional `max_degree` (default min(s-1,256)), `max_new_modes`
  (default32, range0..257), `max_terms` (default64, range1..512), positive rational
  `epsilon` (default1/1000000), and boolean `numerical` (default true).
- Scalar: `rho` >1 (default1000001/1000000) controls formal log-width ratio;
  `route` is `spectral` (default) or `direct`. Direct computes the complete Q in
  O(s) source cuts; it uses no new spectral projections.
- Profile: `coefficient_order` defaults4, range1..32.
- Refinement inherits its parent's readout and controls, with supplied overrides.
  A new tau reuses source modes. Precision can be increased with `max_terms`.
  Refined mode limits may not discard already retained modes.
- Transport: `max_terms` and `numerical` control optional numerical evaluation.

Adaptive mode refinement follows 0,1,2,4,... within the declared limits. It projects
only missing source modes. The two-row polynomial basis can be rebuilt; that work
is recorded separately. A native basis-work budget additionally limits a call.
Exhaustion returns the last valid certificate, including when no further mode fits.

`CERTIFIED_WITHIN_TOLERANCE` means the requested readout meets its criterion.
With numerical evaluation, the interval includes both omitted-mode and numerical
evaluation error and is checked against epsilon. `CERTIFIED_BUDGET_LIMITED` retains
a valid enclosure with the requested accuracy unmet. `EXACT_SYMBOLIC` identifies
an exact finite log expression when numerical evaluation is disabled. Full-degree
derivatives/coefficients can be exact rationals while the logarithm remains symbolic.

The numerical evaluator uses rational range reduction and a rational atanh series
with an explicit geometric tail. No floating approximation is labeled exact.
Overlapping numerical intervals do not imply an ordering or equality.

## Signed transport

Each increment supplies exact `E`, `R`, `J`, integer `epsilon_0` in {0,1}, and
`Q_next`. The worker checks

    Q_next = Q_current + E + R + epsilon_0 J >= 0
    ratio = (1+Q_next)/(1+Q_current).

It retains the original signed components and checks that the product of ratios
equals the endpoint ratio. Positive parts are not substituted for the increments.
The complete chain and original context survive recovery.

## Recovery, source fixtures and cost

Records use the existing authenticated origins/checkpoint store. Source vectors
and contexts are stored once per admitted source identity; child readouts link to
their source and prior spectral state. Export starts no native worker. Refinement
after reopening computes only additional work. Per-call `work` and `native_work`
separate new/reused modes, basis reconstruction, projections, direct cuts and log
series terms. Prior exact-log accounts, operator records and learned models remain.

The package's `archive_fixture.py` helper retrieves selected content-hashed native
objects from plain or zstd tar archives with explicit scan/object budgets. It never
extracts a whole archive or installs a source implicitly. Missing dependencies and
semantic admission remain explicit. The T500 sample supplies archived source
examples; frozen research fixtures remain outside model fitting.

## Minimal example

First call `GEN3_SPECTRAL_ADMIT` with

```json
{"name":"pair","source_binding":{"example":"signed pair"},"source":[1,-1],"max_degree":1,"context":{"basis":["a","b"],"units":{"source":"dimensionless"},"reference":"1","history":{"source":"ordered signed pair"}}}
```

Then `GEN3_SPECTRAL_LOG_PROFILE` with

```json
{"name":"pair-log","source_binding":{"example":"signed pair"},"record":"pair","tau":"1"}
```

The exact spectral expression is `2 log(3/2)`. The scalar expression from
`GEN3_LOG1P_ENCLOSURE` is `log(2)`. Export `pair-log` using its name and original
source binding. Existing `./r3`, `./gen3`, project and CE entry points remain
compatible routes into the selected R4 generation.
