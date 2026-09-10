# CR282 Validation

sealed_utc: `2026-07-12T07:10:36Z`
scientific_result_status: `BOUNDARY`
primary_verdict: `BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN`

## Gates

- `precommit_hash_matches`: `True`
- `precommit_sidecar_matches`: `True`
- `G1_source_integrity`: `True`
- `G2_row_306_exactness`: `True`
- `G3_duplicate_audit_replay`: `True`
- `G4_retirement_scope_audit`: `True`
- `G5_ledger_exclusion`: `True`
- `G6_operator_functionality`: `True`
- `G7_surface_meeting_support`: `True`
- `G8_closure_witness_replay`: `True`
- `G9_typed_occurrence_consistency`: `True`
- `G10_historical_trace_test`: `True`
- `G11_axis_weld_test`: `False`
- `G12_model_comparison`: `True`
- `G13_no_retroactive_rewriting`: `True`
- `G14_no_circular_physical_promotion`: `True`
- `wrong_controls_all_rejected`: `True`

## Conclusion

Historical row trace passed. Axis-self weld remains open because no independent A-to-X1 source bridge is sealed.
