# Exact operator-logarithmic capabilities

Installed build GEN3-CERTIFIEDLOG1-20260915, global SLC-GEN3-R4 / SLC-GEN3-CEV1-R4.
These preserved operator-logarithmic operations run in the current R4 generation;
their original GEN3-OPERATORLOG1-20260915 implementation provenance remains retained.
The shared warm C++/GMP consumer calculates exact rational-polynomial matrix
results. Python validates source metadata and retains complete input/output
records in the existing authenticated R4 checkpoint.

| Operation | Payload fields | Result |
|---|---|---|
| GEN3_OPERATOR_OBSTRUCTION | name, source_binding, context, P, Q, phase_generator | Ordered cubic jet of log(L R^-1) |
| GEN3_COMMUTING_LOG | name, source_binding, context, order, moments | Exact log coefficients C1..C_order |
| GEN3_OPERATOR_EXPORT | name, source_binding | Complete retained record and its hash, without recomputation |

ATOM3D exposes aliases `ATOM3D_OPERATOR_OBSTRUCTION`, `ATOM3D_COMMUTING_LOG`
and `ATOM3D_OPERATOR_EXPORT`. These aliases reject calls in other domains.
The generic GEN3 operations remain available through the shared CE runtime.

## Types and admission

`name` is a new nonempty string of at most128 characters. Reusing it rejects;
choose a successor name when inputs change. `source_binding` is a nonempty
object identifying the actual source. Export requires its exact original value.

`context` has exactly these fields:

```json
{
  "basis": ["state0"],
  "coefficient_parameter": "g",
  "expansion_variables": ["s"],
  "normalization": "IDENTITY_AT_ZERO",
  "units": {"operator": "dimensionless", "s": "declared source coordinate"},
  "history": {"source": "explicit original history or reference"}
}
```

The basis has1..16 distinct string or integer identities. Obstruction variables
are exactly `["u","v"]`; recurrence variables are exactly `["s"]`. The
coefficient parameter is a separate named formal indeterminate. Units and source
history must be explicitly supplied; the implementation retains their declared
meaning and does not infer a physical unit assignment.

A matrix is a square JSON array matching the basis. Every scalar cell is an
object mapping polynomial degree0..8 to an exact integer or rational string:
`{"0":"3/2","1":"-2"}` means 3/2-2g when the parameter is g. `{}` is exact
zero. Missing rows/cells, floating operands and zero denominators reject.
All coefficient products are exact and untruncated; the degree limit applies
to inputs, not to intermediate or returned polynomials.

## Cubic obstruction

`P` and `Q` are permutation arrays: entry j identifies the output basis index
of input j. The native worker checks bijection, involution and the braid relation.
`phase_generator` is the complete polynomial matrix A; source factors such as
64 ell V must already be explicitly incorporated by the caller.

    S_P(w)=exp(w A)(I+w P)exp(w A),
    L=S_P(u)S_Q(u+v)S_P(v),
    R=S_Q(v)S_P(u+v)S_Q(u),
    Omega=log(L R^-1).

Every coefficient through total degree3 is returned, with remainder order4
and the first nonzero total degree, if present. A zero jet reports only the
computed order. It does not infer an all-order compatibility identity.
The signed mixed coefficient [P,Q]/2 of the bare ordered log is also returned.

## Commuting recurrence

Supply `order` in1..8 and exactly that many nonconstant moments plus M0.
The native worker checks M0=I and all pairwise moment commutators before
computing

    F(s)=I+sum_(n=1)^order s^n M_n+O(s^(order+1)),
    C_n=M_n-(1/n)sum_(k=1)^(n-1) k C_k M_(n-k).

The output is log F through the declared order. Noncommuting moments reject;
this operation does not silently substitute a commuting formula. Higher source
moments and global analytic branches are unspecified.

For the Li-6 Gaudin family, use F(s)=T(1/s)/s and M_n=sum_i e_i^n Q_i.
That normalization has M0=I and C1=H+gI on active three-state blocks.

## Example: scalar family and exact recovery

This payload computes log(1/(1-2s)) through degree3:

```json
{
  "name": "scalar-example",
  "source_binding": {"example": "F(s)=1/(1-2s)"},
  "context": {
    "basis": ["scalar"],
    "coefficient_parameter": "g",
    "expansion_variables": ["s"],
    "normalization": "IDENTITY_AT_ZERO",
    "units": {"operator": "dimensionless", "s": "dimensionless"},
    "history": {"formula": "F(s)=1/(1-2s)"}
  },
  "order": 3,
  "moments": [ [[{"0":"1"}]], [[{"0":"2"}]], [[{"0":"4"}]], [[{"0":"8"}]] ]
}
```

Call `GEN3_COMMUTING_LOG` through an active DomainSession or the normal project
CLI. The returned coefficients are2,2,8/3. Reopen that same current-generation
session and call `GEN3_OPERATOR_EXPORT` with the original name/source binding.
Export returns the exact saved inputs, context, source history and result without
starting the native worker. Successful calls share ordinary managed checkpoints.

## Preservation and generation

Operator records use the existing immutable origins map. No new checkpoint
schema is introduced. The declared authenticated predecessor bindings remain
eligible for additive recovery; source state, histories, learned models and
original checkpoint roots are retained. New-generation research starts a fresh
DomainSession. The source operator is a readout alongside retained histories;
equal operator images do not merge histories. Existing source models, physical
assignments and owner pauses retain their scope.
