# CR119 Validation

sealed_utc: `2026-07-12T09:02:06Z`
scientific_result_status: `PASS`
primary_verdict: `PASS_TYPED_CLOSURE_HIERARCHY_AND_PROMOTION_LADDER`

## Gates

- `G10_particle_face_verdict_inheritance`: `True`
- `G11_role_conflict_count`: `True`
- `G12_no_physical_overpromotion`: `True`
- `G13_machine_readable_handoff`: `True`
- `G1_source_hashes`: `True`
- `G2_exact_node_reproduction`: `True`
- `G3_DAG_acyclicity`: `True`
- `G4_independent_path_equality`: `True`
- `G5_typed_operator_separation`: `True`
- `G6_same_value_occurrence_separation`: `True`
- `G7_promotion_rule_enforcement`: `True`
- `G8_direct_S_rejection`: `True`
- `G9_scalar_one_row_rejection`: `True`
- `precommit_hash_matches_sidecar`: `True`
- `wrong_controls_all_rejected`: `True`
- `cycle_count`: `0`

## Component Findings

- `FORMAL_DERIVATION_DAG`: `PASS`
- `CONTACT_AXIS_RESOLUTION_EDGE`: `PASS`
- `CARRIER_CONTAINER_PROMOTION`: `PASS`
- `PARTICLE_FACE_EDGE`: `STRUCTURAL_ONLY`
- `FULL_LEDGER_TERMINUS`: `PASS`
- `SAME_VALUE_OCCURRENCE_TYPING`: `PASS`
- `PHYSICAL_PROPAGATION_MECHANISM`: `OPEN`
