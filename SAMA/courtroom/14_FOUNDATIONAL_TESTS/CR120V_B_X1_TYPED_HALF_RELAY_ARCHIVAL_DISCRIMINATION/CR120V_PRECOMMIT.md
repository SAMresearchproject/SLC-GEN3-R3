# CR120V precommit — B/X1 typed half-relay archival discrimination

record_id: `CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION`  
classification: `CONSTRUCTIVE_NEW_WORK / ARCHIVAL_DISCOVERY`  
proposal_id: `sam2p-378de6a78a8c2bd479b1`  
same_run_repair: `PROHIBITED`

## Question

Does the frozen Courtroom record support the literal expression

```text
B = 1/2 request
X1 = 1/2 response
B + X1 = one completed relay
```

or does it support only a typed-interface interpretation in which distinct
`B_CONTACT_OPERATOR` and `X1_AXIS_SELF_CHANNEL` participate in a larger
outward/return route?

## Frozen baseline

```text
RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)
  -> W9_CLOSURE_WITNESS
```

`S8_BINARY_SURFACE` remains the canonical source entity. `W8` is not introduced
as an alias. `B_CONTACT_OPERATOR`, `X1_AXIS_SELF_CHANNEL`, and
`W9_CLOSURE_WITNESS` remain distinct typed entities.

## Candidate interpretations

1. `LITERAL_TWO_HALF`
   - B is one scalar half.
   - X1 is one scalar half.
   - Their scalar addition creates the completed X1/W9 relay.
2. `TYPED_INTERFACE_RELAY`
   - B and X1 remain distinct types.
   - B may be the contact/request interface and X1 the axis/response interface
     of the already sourced outward/return route.
   - This candidate does not claim B creates X1 or that either entity is a
     half-scalar.
3. `STATIC_RUNTIME_ONLY`
   - The installed language exposes a fixed typed route with one immutable X1
     entity and a singleton W9 output.
   - This candidate makes no claim about physical relay dynamics.
4. `B_CREATES_X1`
   - A B intervention dynamically creates or changes X1.

## Exact arithmetic gate

The active V4.2 route is frozen as six half-slots:

```text
1/2 SW_out | 1/2 WRITE_out | 1/2 OUTSIDE |
1/2 INSIDE | 1/2 WRITE_in | 1/2 SW_in
```

The runner must compute with exact rational arithmetic:

```text
outward_weight = 3/2
inward_weight  = 3/2
total_weight   = 3 = D
half_slot_count = 6 = alpha_H * D
```

It must not collapse this sourced six-slot shell into two half-slots.

## Frozen evidence gates

1. Verify every source SHA-256 in `CR120V_SOURCE_MANIFEST.json`.
2. Confirm the registered types and the explicit inequality `B != X1`.
3. Confirm B is a non-scalar operator and X1 has registered scalar value 1.
4. Confirm the V4.2 six-half-slot outward/return route and exact arithmetic.
5. Confirm that no sourced record maps B uniquely to one outward half-slot or
   X1 uniquely to one inward half-slot.
6. Confirm CR120D's runtime boundary: no X1 intervention surface, singleton W9
   output, and physical perturbability unresolved rather than falsified.
7. Confirm QP035: half-write/information split alone does not close an open
   slot.
8. Confirm QP036: a local information-return correction was selected.
9. Confirm QP037: one identity promoted only after applying the selected return
   correction; the remaining seven stayed open.
10. Preserve the distinction between an archival structural contact and a
    causal physical weld.

## Candidate decision rules

- `LITERAL_TWO_HALF` is rejected if B is non-scalar, X1 is registered as 1, or
  the sourced route contains six rather than two half-slots.
- `TYPED_INTERFACE_RELAY` receives `SUPPORTED_AS_ARCHIVAL_HYPOTHESIS` if typed
  separation, an outward/return route, and return-required closure all hold.
  It cannot receive a causal PASS unless a source explicitly welds B=request
  and X1=response.
- `STATIC_RUNTIME_ONLY` receives `PASS_IN_RUNTIME_SCOPE` if CR120D's exact
  runtime findings reproduce.
- `B_CREATES_X1` remains `UNTESTABLE_IN_CURRENT_RUNTIME` if there is no X1
  intervention surface. Absence of that surface is not a physical falsifier.

## Wrong controls

- Alias W8 to S8.
- Merge B and X1 because a proposed contribution is equal.
- Assign scalar 1/2 to B.
- Replace X1's registered scalar 1 with 1/2.
- Collapse six half-slots to two.
- Treat half-write alone as closure.
- Treat fixed W9 output as evidence against all auxiliary physical dynamics.
- Treat CR120D as a physical null experiment.
- Claim QP036 proves B=request or X1=response.

## Verdict vocabulary

The primary result must be one of:

```text
PASS_RECIPROCAL_HALF_SLOT_RELAY_EXISTS__BOUNDARY_B_REQUEST_X1_RESPONSE_WELD__LITERAL_TWO_HALF_REJECTED
BOUNDARY_ARCHIVAL_RELAY_INCOMPLETE
FAIL_SOURCE_OR_ARITHMETIC_REPRODUCTION
```

The first verdict means the outward/return grammar is source-backed and return
is closure-relevant, while the specific B/request and X1/response assignment is
still an open weld. It does not register an operator or claim physical identity.

## Stop rule

Run one deterministic archival discrimination. Do not create synthetic
interventions, mutate SAM Language, open a cosmological bridge, or repair the
candidate after seeing the result.
