# CR115 D3 Invariant-Carrier Uniqueness Theorem Gate

## Verdict

```text
CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE
```

## Theorem Statement

Given substrate-internal displacement-response identity and no external identity carrier, all admissible persistent matter-identity handles reduce to a self-contained stable source/topological sector. For the 1D loop/twist/intersection carrier, obstruction_dim=3-D, so D=3 is the unique stable dimension.

## Calibration

This gate answers the F-002 trap directly: G347 is the computational topology core; G349-G354 are the SAM structural-commitment layer that makes the carrier class necessary. The result is an inside-SAM theorem gate, not an external peer-review or empirical-proof claim.

## Computed Topology Core

```text
obstruction_dim = 3 - D
D=1: obstruction=2, stable=False, overconstrained
D=2: obstruction=1, stable=False, overconstrained
D=3: obstruction=0, stable=True, stable_point_obstruction
D=4: obstruction=-1, stable=False, unwinds_or_slides
D=5: obstruction=-2, stable=False, unwinds_or_slides
D=6: obstruction=-3, stable=False, unwinds_or_slides
D=7: obstruction=-4, stable=False, unwinds_or_slides
stable_ds = [3]
```

## Carrier Closure

- loop_link_topology: sufficient_open_route -> closed_1D_loop_substrate -> stable_loop_link_deformation_class -> stable_loop_link_sector (CLOSED_TO_STABLE_SECTOR)
- spectral_eigenmode: alternate_live_in_G348 -> carrier_with_boundary_conditions -> spectrum_of_deformation_operator_class -> stable_source_topological_sector (CLOSED_TO_STABLE_SECTOR)
- endpoint_F4_label: alternate_live_in_G348 -> edge_or_boundary_transport -> closed_loop_transport_conjugacy_class -> stable_source_topological_sector (CLOSED_TO_STABLE_SECTOR)
- ledger_history: alternate_live_in_G348 -> ordered_SW_path -> path_homotopy_or_closed_transport_class -> stable_source_topological_sector (CLOSED_TO_STABLE_SECTOR)
- phase_holonomy: alternate_live_in_G348 -> path_or_closed_loop -> closed_phase_holonomy -> stable_source_topological_sector (CLOSED_TO_STABLE_SECTOR)

## Load-Bearing Source Chain

- CR115_RUNNER [EXECUTABLE_GATE]: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM\CR115_runner.py` sha256 `0c9c3d7cf30a20e2f1b833c77c89505e72a58eadefca35ec909e7c596128e5e5`
- G347_OUTPUT [COMPUTATIONAL_TOPOLOGY_CORE]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G347_d3_theorem_route_audit\G347_output.json` sha256 `0e1c662c80e2eac4eb89e5aa6d13de251b5520edb4318a8da042ec7b00775f83`
- G348_OUTPUT [STRUCTURED_PREMISE_AUDIT]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G348_loop_topology_identity_premise\G348_output.json` sha256 `ce02e5efcfd82aeabe129ff2564544560c3d74a6b20d8073c779ab40aa5236d3`
- G349_OUTPUT [STRUCTURED_REDUCTION_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G349_worldsheet_identity_reduction\G349_output.json` sha256 `45d4164aaca93cc34a2634cd6b833e8f91c355d9f3bbd4f59bd51e4efd4b374f`
- G350_OUTPUT [STRUCTURED_REDUCTION_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G350_identity_deformation_quotient\G350_output.json` sha256 `3781fae9d06191654185d1ecbc482bc54e41902a9368aa360ef9d5141adb90d3`
- G351_OUTPUT [GAP_LOCALIZATION_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G351_d3_route_c_proof_wording\G351_output.json` sha256 `216cd3702a397176bed5e5cbd05b1b15775f50c285510e42b32203e810dcc8da`
- G352_OUTPUT [STRUCTURED_REDUCTION_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G352_self_contained_holonomy_topology\G352_output.json` sha256 `46b2b8ae07d95d6c376af38b22a20ba124201fdec7dd6f32d3f9ffab16c602d5`
- G353_OUTPUT [PROVENANCE_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G353_no_external_identity_provenance\G353_output.json` sha256 `ff43fd9c42b97aa62184bbda6da15fa2e6feb751f653cf79abb1cc2d8e0f845b`
- G354_OUTPUT [FRAMEWORK_PRINCIPLE_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G354_displacement_response_identity\G354_output.json` sha256 `adfb155e8bfca9c181fb7c8302f72526154ba091e37a977e3a4ee587d507dc16`
- G355_OUTPUT [AGGREGATE_THEOREM_RECORD]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G355_d3_displacement_response_theorem\G355_output.json` sha256 `3cd6662d64c290c3850f51395e35566aaa3992ebff40f1e266d47eeff69e3529`
- THEOREM_D3 [THEOREM_TEXT]: `C:\VS\Stam_model-A-v1.0\audit\audits\THEOREM_D3_DISPLACEMENT_RESPONSE.md` sha256 `46590595f63726e913a58b4ad5e1d4cdc2443cead49584a1e154badef400b9d8`
- VERDICT_G355 [VERDICT_TEXT]: `C:\VS\Stam_model-A-v1.0\audit\audits\VERDICT_G355_d3_displacement_response_theorem_2026_05_25.md` sha256 `c82f41b0a60245b488c7801fede3bb1fca31e59e593f380a650f79e8f25069c6`
- HOSTILE_AUDIT_F002 [EXTERNAL_HOSTILE_AUDIT]: `C:\VS\Stam_model-A-v1.0\audit\audit.md` sha256 `a795d712fa933dcb56043c11055e62af5a32fb338889ec354c2e78bcb744cb6d`

## Pass Checks

- PASS P1_sources_present: All load-bearing source artifacts are present.
- PASS P2_hostile_audit_trap_acknowledged: The gate explicitly separates G347 computational topology from assertion/commitment records.
- PASS P3_G348_open_premise_captured: G348's live alternate carriers are copied into the CR115 reduction table rather than ignored.
- PASS P4_G349_extended_support_reduces_alternates: All G348 alternate carriers require extended support before quotienting.
- PASS P5_G350_deformation_quotient_rejects_raw_carriers: Raw labels, histories, phases, and spectra survive only as deformation classes.
- PASS P6_G352_self_contained_holonomy_reduces: Self-contained nontrivial holonomy/transport identity reduces to a stable source sector.
- PASS P7_G354_identity_principle_accepted_for_gate: Displacement-response identity supplies the no-external identity rule used by CR115.
- PASS P8_all_admissible_carriers_close_to_stable_sector: Every G348 carrier is now routed to the stable source/topological sector under the declared SAM rules.
- PASS P9_dimension_selector_computed_and_matches_sources: CR115 recomputes obstruction_dim=3-D and finds D=3 as the unique stable row.
- PASS P10_G351_gap_is_specifically_closed: G351 named the holonomy/topology gap; G352 and CR115 close that exact gap under no-external identity.
- PASS P11_G355_chain_remains_consistent: G355 aggregate chain remains consistent with the explicit uniqueness closure.
- PASS P12_current_record_status_found: Priority record currently records D=3 as derived inside SAM, so CR115 is an appeal/closure support artifact rather than a new free parameter.

## Wrong Controls

- REJECTED WC1_poset_axioms_alone_derive_D3: Finite poset axioms alone derive D=3.
- REJECTED WC2_topology_sufficient_implies_necessary: Loop topology being sufficient in G348 already made it necessary.
- REJECTED WC3_rule_out_alternates_by_assertion: Rule out spectra, labels, ledger history, and phase holonomy by assertion.
- REJECTED WC4_raw_ledger_string_persistent: Raw ordered ledger history is itself persistent matter identity.
- REJECTED WC5_bare_endpoint_label_persistent: Bare endpoint/F4 label is persistent matter identity without closed-loop transport.
- REJECTED WC6_open_path_phase_persistent: Open path phase is persistent matter identity without closed holonomy.
- REJECTED WC7_standalone_spectral_number_persistent: A standalone spectral number is persistent matter identity without operator-domain deformation class.
- REJECTED WC8_external_background_identity: External/background holonomy can be intrinsic matter identity in SAM.
- REJECTED WC9_contractible_phase_identity: Contractible self-contained phase is persistent nontrivial matter identity.
- REJECTED WC10_holonomy_alone_derives_D3: Holonomy by itself derives D=3 without a stable source/topological sector.
- REJECTED WC11_D2_or_D4_stable_identity: D=2 or D=4 supplies the same stable nontrivial loop/twist identity.
- REJECTED WC12_import_string_critical_dimension: D=3 is imported from string-theory critical dimension or other external target.
- REJECTED WC13_assertion_script_equals_computation: Treat G348-G355 assertion/commitment records as if every layer were computational math.
- REJECTED WC14_downstream_R_A0_Higgs_derives_D3: Use R=12, A0, Higgs, 2pi, or downstream particle matches as the D=3 derivation.
- REJECTED WC15_external_peer_review_or_empirical_proof_claim: Claim external peer-review closure or empirical proof of D=3.

## Scope

- Closes the G348 carrier-necessity gap inside SAM by routing all G348 identity-carrier alternatives through support, deformation quotient, and self-contained stable-sector rules.
- Keeps G347 as the only load-bearing computational topology selector.
- Recalibrates G355: strong inside-SAM theorem gate, not external peer-review or empirical proof.
- Does not derive D=3 from R=12, A0, Higgs, 2pi, SN/BAO, or particle mass matches.
- Does not derive the matter spectrum, chirality, anomaly cancellation, or exact masses.

## Open Debts

- For publication, write the carrier-uniqueness theorem in prose with the source-type calibration visible.
- External topology review can still be invited for the G347 obstruction theorem wording.
- If desired, backfill G348-G355 with explicit test_type fields so assertion records are machine-labeled.

## Hash

```text
CR115_invariant_carrier_uniqueness_lock.json sha256 = 369b2651f6a14bc608aac4e2e4ba1778f3dff6150d1e766eb990ddf2ab048fe0
```
