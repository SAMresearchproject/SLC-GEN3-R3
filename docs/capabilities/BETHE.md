# Exact Bethe algebra and A3D41 construction — R4

These five operations execute in the shared warm C++/GMP consumer. All active CE
domains accept GEN3 names; ATOM3D alone accepts corresponding ATOM3D aliases.
Existing models, source operators, logarithms and immutable checkpoint roots persist.

Algebra requests have exactly `name`, `source_binding`, `context`, `data`.
`context` uses the existing source contract: distinct ordered `basis` (1..64),
`field: {radicand: 0}` for Q or an admitted nonsquare real quadratic field,
nonempty `units` and `history` objects, and an explicit `spectral_coordinate`.
All numbers are integers, rational strings or `{a,b}` quadratic coefficients.
Record names are immutable; successful calls retain full inputs and outputs.

| Operation | Data |
|---|---|
| GEN3_OPERATOR_MODULE | `mode: EXACT` or `MODULAR`, square `left_H`, square `right_H`, 1..8 rectangular `seeds`. Source basis identifies the left rows; the declared right_H column order is retained. MODULAR requires `prime`; returns a lower-bound witness. EXACT computes a closed echelon basis and left/right action tables. Optional `full_box: true` requires `prime` and regenerates a full-rank modular witness before using matrix units. This is an exact block method, composable with the retained Li6 polynomial block decomposition. |
| GEN3_OPERATOR_PRODUCT | SUPPORT: `mode`, `dimension`, distinct matrix-unit `coordinates: [[i,j],...]`; returns transitive product support, additions and all nonzero multiplication triples. CONTRACT additionally takes `left` and `right` ascending sparse polynomials: each power is `[[coordinate_id,coefficient],...]`. Optional `u,v` evaluates products; omission returns every bivariate coefficient. Correction is A(u)B(v)-A(v)B(u), with channel order retained. |
| GEN3_LOCAL_EXCHANGE_OBSTRUCTION | `mode: DIFFERENCE` or `TWO_PARAMETER`, `local_dimension` 2..8 and rational square `H` of size local_dimension squared. Source basis uses left factor then right. The first returns outer-changing entries of [h12+h23,[h12,h23]]. The second eliminates the unrestricted local derivative g and returns an exact inconsistency witness or INCONCLUSIVE. Optional `max_rows`1..262144 and `max_rank`1..4096 bound elimination. Passing these necessary tests does not assign an R matrix. |
| GEN3_CONSTRUCTION_EVALUATE | Special top-level fields: `name`, `source_contract: A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1`, `family_ids` (1..32 distinct IDs in0..4799999), `contexts` (1..32 distinct indices in0..31). The installed authenticated source provider supplies the original geometry and TMR1 tensors. Returns exact minimum action and complete262144-state bitset (hex) for each context; with contexts3 and11 also reports common-minimum count, set equality and the shared four-state orbit label. |
| GEN3_BETHE_EXPORT | Top-level `name`, `source_binding` only. Returns the complete retained record and digest without native computation. Construction calls return the installed provider binding to use for export. |

Context index = mask +4*kind +8*channel +16*receiver. The construction evaluator
ports the original native construction lowering and CPU phase formulas; exact
128-bit integer accumulation precedes division by576. It assigns no physical scale.

Product associativity is an algebra calculation. Factorized exchange, state-dependent
Yang–Baxter consistency and full Bethe equations remain separate research questions.
The completed Li6 fixtures retain2070 module directions,2080 product directions,
68608 nonzero products and the exact regular local obstruction.
