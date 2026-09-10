# CR117 Precommit

Record:

```text
CR117_S8_TYPED_SURFACE_CLOSURE_OCTAHEDRON_DUALITY
```

Precommit sealed UTC:

```text
2026-07-12T03:12:56Z
```

Metadata frozen before runner:

```text
scientific_result_status = PASS
prospective_record_class = SCIENTIFIC_TEST
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

Primary verdict to be returned if and only if every prediction passes:

```text
PASS_S8_TYPED_SURFACE_CLOSURE_UNIFICATION
```

Secondary scope notes allowed on PASS:

```text
MATHEMATICAL_AND_COMBINATORIAL_UNIFICATION_PASS
PHYSICAL_OCTAHEDRON_ONTOLOGY_REMAINS_CANDIDATE
```

## Source Hierarchy Frozen

CR258 controls the current primitive-base route:

```text
h = alpha_H = 2
D = 3
S_state = h^D
```

The runner must not define `S` by circularly assuming `S = 8`. It must derive:

```text
S_state = h^D = 8
S_cross = 2^D = 8
R = h^2 D = 12
Theta = h D^2 = 18
S_split = R^2 / Theta = 8
```

The older CR238 `{F,S}` foundational wording is preserved as a sealed historical source conflict and alias. It is not erased, and it is not used as the runner's primitive input.

## Predictions

P1. Binary state count: `|H_D| = |{0,1}^D| = 2^D = 8`.

P2. Reject arbitrary-boundary overclaim: `2^D` does not count all separating hyperplanes or arbitrary classification boundaries.

P3. Octahedron combinatorics: `(V,E,F) = (6,12,8)`.

P4. Cube combinatorics: `(V,E,F) = (8,12,6)`.

P5. Duality: cube and octahedron exchange vertices/faces and preserve edges.

P6. Binary-state/face bijection: construct all eight sign states and all eight triangular octahedron faces; require complete one-to-one coverage.

P7. SAM atom alignment: `V_oct = hD = 6`, `E_oct = R = 12`, `F_oct = S = 8`.

P8. Euler closure: `V - E + F = h = 2`.

P9. Release-share identity: `S_split = R^2 / Theta = 8`.

P10. Carrier fraction: `f_Theta = 1/S = 1/8`.

P11. State/split equality uniquely selects `D = 3` over the precommitted scan range `D in [1,12]`.

P12. Edge/radix equality uniquely selects `D = 3` for both cube and cross-polytope edge counts.

P13. Octahedral skeletal rigidity: exact rigidity-matrix rank reaches `3V - 6 = 12`.

P14. Cube skeletal flexibility: unbraced cube has rank less than `3V - 6 = 18`.

P15. Repository role reconciliation: every active S=8 occurrence is assigned a nonconflicting type or retained as an explicit unresolved/historical conflict.

## Wrong Controls

WC1. Ternary directions: `3^D = 27`, expected break.

WC2. Signed axes mistaken for surface: `2D = 6`, expected to identify octahedron vertices/cube faces, not S.

WC3. Cube faces claimed as eight, expected reject.

WC4. Octahedron vertices claimed as eight, expected reject.

WC5. Arbitrary hyperplane count, expected reject as false/unbounded.

WC6. One-quarter split, expected break against `R^2/Theta = 8`.

WC7. Sixteen-state split, expected break against `Theta=18` and dual geometry.

WC8. `D = 4`, expected state/split and edge/radix alignment failures.

WC9. Unbraced cube called rigid, expected reject by Maxwell count and rank.

WC10. Circular definition, expected provenance audit flag if `S=8` is used as primitive input.

WC11. Historical role overwrite, expected reject; role typing is append-only.

## Implementation Lock

The runner must be written only after this precommit file is hashed.

Required runner outputs:

```text
CR117_result.md
CR117_summary.json
CR117_provenance.json
CR117_typed_S8_contract.json
CR117_binary_state_face_bijection.csv
CR117_cube_octahedron_counts.csv
CR117_dimension_uniqueness_scan.csv
CR117_rigidity_results.json
CR117_wrong_controls.csv
CR117_VALIDATION.md
HASHES.txt
```

The runner must preserve:

```text
physical_geometry_status = CANDIDATE_REALIZATION
not_claimed = arbitrary separating surfaces, literal physical octahedral atoms, universal material-strength superiority
```
