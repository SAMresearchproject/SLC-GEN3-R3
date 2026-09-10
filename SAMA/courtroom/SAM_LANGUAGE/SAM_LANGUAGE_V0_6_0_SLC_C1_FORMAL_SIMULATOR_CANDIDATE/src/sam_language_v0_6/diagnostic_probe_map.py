"""Mapping from v0.3 External Diagnostic Run 001 probes to v0.4 regressions."""

V03_PROBE_REGRESSION_MAP = {
    "CORE_S_ATOM": {
        "v04_regression": "test_supported_s8_contextual_role_passes",
        "coverage": "S8 entity remains typed BinarySurface with scalar value 8.",
    },
    "CORE_PARTITION_OVERFLOW": {
        "v04_regression": "parent_regression_28_28_pass",
        "coverage": "Inherited v0.3 regression replay remains PASS.",
    },
    "CORE_EXTENDED_OVERFLOW": {
        "v04_regression": "parent_regression_28_28_pass",
        "coverage": "Inherited v0.3 regression replay remains PASS.",
    },
    "CORE_CARRIER_OVERFLOW": {
        "v04_regression": "parent_regression_28_28_pass",
        "coverage": "Inherited v0.3 regression replay remains PASS.",
    },
    "CORE_TYPED_GRID_OVERFLOW": {
        "v04_regression": "parent_regression_28_28_pass",
        "coverage": "Inherited v0.3 regression replay remains PASS.",
    },
    "CORE_EXACT_S_STATE": {
        "v04_regression": "test_s8_carrier8_support8_remain_distinct",
        "coverage": "S8 state value remains 8 while carrier/support 8 stay distinct.",
    },
    "CORE_EXACT_S_SPLIT": {
        "v04_regression": "test_supported_s8_contextual_role_passes",
        "coverage": "S8 split role is retained as a contextual BinarySurface role.",
    },
    "CR117_BINARY_FACE_STATE_ROLE": {
        "v04_regression": "test_supported_s8_contextual_role_passes",
        "coverage": "Previously missing S8 binary-face role is now registered.",
    },
    "CR117_CROSS_POLYTOPE_FACET_ROLE": {
        "v04_regression": "registry_payload.allowed_context_roles",
        "coverage": "S8 cross-polytope-facet role is now registered.",
    },
    "CR117_RELEASE_SPLIT_ROLE": {
        "v04_regression": "registry_payload.allowed_context_roles",
        "coverage": "S8 release-split role is now registered.",
    },
    "CR281_DOMAIN_MULTIPLICITY_ROLE": {
        "v04_regression": "test_unsupported_contextual_role_is_rejected",
        "coverage": "Unsupported domain multiplicity role remains rejected.",
    },
    "CR233_THETA_LEDGER_ROLE": {
        "v04_regression": "registry_payload.allowed_context_roles",
        "coverage": "Theta native-closure-budget role is registered from CR119 import.",
    },
    "CR233_81_LEDGER_ROLE": {
        "v04_regression": "test_distinct_81_roles_exist",
        "coverage": "F81 and distinct 81 role occurrences are registered.",
    },
    "EXISTING_THETA_CLOSED_LEDGER_ROLE": {
        "v04_regression": "test_valid_closure_program_executes_to_l162",
        "coverage": "Theta remains typed in the closed hierarchy source path.",
    },
    "EXISTING_F_CLOSED_LEDGER_ROLE": {
        "v04_regression": "test_valid_closure_program_executes_to_l162",
        "coverage": "F81 remains typed in the closed hierarchy source path.",
    },
    "EXISTING_V_BOW_ROLE": {
        "v04_regression": "test_valid_closure_program_executes_to_l162",
        "coverage": "V27 promotion remains typed before face promotion.",
    },
    "EXISTING_L_CLOSED_LEDGER_ROLE": {
        "v04_regression": "test_valid_closure_program_executes_to_l162",
        "coverage": "L162 remains the typed FullLedger endpoint.",
    },
    "CR281_L_BOW_TERMINAL_ROLE": {
        "v04_regression": "test_unknown_entity_is_rejected",
        "coverage": "Unsupported experimental operator/terminal role remains rejected.",
    },
    "OPEN_HV_NUCLEAR_ROLE_GUARD": {
        "v04_regression": "authority_open_roles_rejected",
        "coverage": "OPEN authority roles cannot be used authoritatively.",
    },
    "CONFLICT_M3_NUCLEAR_ROLE_GUARD": {
        "v04_regression": "authority_conflict_roles_rejected",
        "coverage": "CONFLICT authority roles cannot be used authoritatively.",
    },
    "UNQUALIFIED_ROLE_GUARD": {
        "v04_regression": "test_unsupported_contextual_role_is_rejected",
        "coverage": "Role claims require explicit entity and contextual role.",
    },
    "WRONG_BOW_DOMAIN_GUARD": {
        "v04_regression": "test_direct_s8_volume_promotion_is_rejected",
        "coverage": "Wrong-domain operator routing is rejected by typed signatures.",
    },
    "WRONG_LEDGER_OVERLAP_GUARD": {
        "v04_regression": "test_direct_s8_volume_promotion_is_rejected",
        "coverage": "Wrong ledger-overlap routing is rejected by typed signatures.",
    },
    "BINDING_SCOPE_GUARD": {
        "v04_regression": "test_unknown_entity_is_rejected",
        "coverage": "Out-of-scope binding lift remains unavailable.",
    },
    "PARTICLE_NAME_GUARD": {
        "v04_regression": "test_historical_a_row_proxy_is_retired",
        "coverage": "Structural stability still does not activate a particle name or row.",
    },
    "TEXT_PARSER_ACCEPTS_UNSUPPORTED_ROLE": {
        "v04_regression": "test_unsupported_contextual_role_is_rejected",
        "coverage": "Parser output is checked before execution; unsupported role rejects.",
    },
    "TEXT_PARSER_ACCEPTS_UNKNOWN_TYPE": {
        "v04_regression": "test_unknown_type_is_rejected",
        "coverage": "Parser output is checked before execution; unknown type rejects.",
    },
    "PROVENANCE_DUPLICATE_ENTITY_OVERWRITE": {
        "v04_regression": "test_same_assertion_new_source_retains_both_trails",
        "coverage": "Duplicate assertion with new source appends a second trail.",
    },
    "PROVENANCE_DEPENDENCY_CYCLE": {
        "v04_regression": "test_dependency_cycle_raises_full_path",
        "coverage": "Dependency cycles raise ProvenanceCycleError with the full path.",
    },
}
