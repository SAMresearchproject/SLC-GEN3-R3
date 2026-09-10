# CR120V B/X1 typed half-relay archival discrimination

## Primary verdict

`PASS_RECIPROCAL_HALF_SLOT_RELAY_EXISTS__BOUNDARY_B_REQUEST_X1_RESPONSE_WELD__LITERAL_TWO_HALF_REJECTED`

## Direct answer

The repository **does contain a reciprocal information-route structure**. The
active V4.2 chain has three outward half-slots and three inward half-slots, with
exact weights `3/2 + 3/2 = 3 = D`. QP035 independently shows that the half-write
split alone does not close an open slot; QP036 selects a local information-return
correction; QP037 promotes one identity only after that return is applied.

That is strong archival support for the user's central relay intuition:
**outward contact and inward return are both required for a completed physical
write/identity event.**

The literal formula `B=1/2` and `X1=1/2` does not survive the frozen typing:

- `B_CONTACT_OPERATOR` is a non-scalar operator;
- `X1_AXIS_SELF_CHANNEL` is an `AxisChannel` with registered scalar value 1;
- the sourced reciprocal shell contains six half-slots, not two;
- B and X1 are explicitly forbidden from collapsing into one entity.

The strongest retained formulation is therefore:

```text
R_BX1 = proposed reciprocal relay process
B_CONTACT_OPERATOR = typed contact/request-side interface candidate
X1_AXIS_SELF_CHANNEL = typed axis/response-side interface candidate

RESOLVE(S8, B, X1) -> W9
```

This is a supported archival hypothesis, not yet a causal weld. No frozen
authority source explicitly assigns `B=request` and `X1=response`.

## What CR120D means after this run

CR120D is reproduced exactly in its own scope: the installed language has one
immutable X1 object, no X1 intervention syntax, and a fixed singleton W9 output.
It is a **runtime boundary**, not a physical null experiment. Consequently it
cannot decide whether B physically activates, modulates, or creates an
X1-associated response.

## Candidate disposition

| Candidate | Result |
|---|---|
| Literal `B half + X1 half` | Rejected by frozen type, scalar, and slot-count records |
| Typed B/X1 interfaces of one relay | Supported as archival hypothesis; explicit weld open |
| Static installed runtime | Pass in runtime scope |
| B dynamically creates X1 | Untestable in current runtime |

## Exact accounting

```text
OUTWARD: 1/2 SW_out + 1/2 WRITE_out + 1/2 OUTSIDE = 3/2
INWARD:  1/2 INSIDE + 1/2 WRITE_in + 1/2 SW_in   = 3/2
TOTAL:                                                    3 = D
```

The useful `1/2 + 1/2` statement is therefore not an entity equation. It is a
paired route grammar repeated across SW, write, and boundary-position roles.

## Boundaries

- No new operator or entity was registered.
- No physical intervention was synthesized or executed.
- The run does not prove that B creates X1.
- The run does not prove that B and X1 carry equal causal information.
- `S8_BINARY_SURFACE`, not W8, remains the canonical registered source.
- The next constructive seam is a sourced mapping from the outward/return route
  fields to B-side and X1-side observables—not another test of fixed W9 labels.

## Controls and custody

- Source hashes: `13/13` matched.
- Wrong controls: `8/8` rejected.
- Same-run repair: `false`.
