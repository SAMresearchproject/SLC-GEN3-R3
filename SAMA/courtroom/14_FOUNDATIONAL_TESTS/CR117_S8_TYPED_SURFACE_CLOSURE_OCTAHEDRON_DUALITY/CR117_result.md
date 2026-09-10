# CR117 Result

record_id: `CR117_S8_TYPED_SURFACE_CLOSURE_OCTAHEDRON_DUALITY`
sealed_utc: `2026-07-12T03:18:19Z`
scientific_result_status: `PASS`
primary_verdict: `PASS_S8_TYPED_SURFACE_CLOSURE_UNIFICATION`

## Typed Result

The CR keeps three objects separate until derived:

```text
S_state = h^D = 2^3 = 8
S_cross = 2^D = 2^3 = 8
S_split = R^2/Theta = 144/18 = 8
```

At the canonical source-controlled point `h=2, D=3`, all three equal `8`.

## Cube-Octahedron Closure

Octahedron `(V,E,F)=(6,12,8)=(hD,R,S)`.
Cube `(V,E,F)=(8,12,6)=(S,R,hD)`.
Euler closure: `6-12+8=2=h`.

The eight binary sign states are in exact bijection with the eight octahedral triangular faces; each face lies in one sign octant and has outward normal sign equal to the corresponding cube vertex.

## Uniqueness And Rigidity

Dimension scan `D in [1,12]`: state/split equality at `[3]`, cross-edge/radix equality at `[3]`, cube-edge/radix equality at `[3]`.
Octahedron rigidity rank: `12` of required `12`.
Unbraced cube rigidity rank: `12` of required `18`.

## Boundaries Preserved

- `2^3` does not count every arbitrary separating surface.
- The octahedron result is mathematical/combinatorial and remains a candidate SAM realization, not proof of literal physical substrate atoms.
- Historical S=8 wording is not overwritten; CR238's older `{F,S}` primitive direction is retained as a source conflict controlled by CR258 for this CR.

## Firewall

```text
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```
