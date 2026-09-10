# CR113 A4 Completed-WRITE Address Count Theorem

## Verdict

```text
CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM
```

## Theorem Statement

At A=1 the parent-ledger crossing is closed, so the completed WRITE is a boundary-address object. The manifold address axis has M_w=4 from two oriented faces times two surface dimensions. The route-depth axis has D_route=3 from C_w weights 1/2+1/2+1+1. Because these are distinct address axes, R=M_w*D_route=4*3=12. A0 is applied only after R is fixed.

## Derived Count

```text
M_w      = 4
D_route  = 3
R        = M_w * D_route = 4 * 3 = 12
A_share  = 1/12
A_side   = 1/24
A0       = downstream floor normalization after R is fixed
```

## Load-Bearing Source Chain

- PRIORITY_RECORD_A4_R_FIRST_ADDENDUM: `C:\VS\memory\PRIORITY_RECORD.md` sha256 `640c41f5d31878891e22a13d1ef5d3a8ed7cb47e9a8ed07934d110471dbfebb4`
- G11555_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM\G11555_summary.json` sha256 `05d4e7390eba729cded60299e4d18093a87cf0a92c63845ab8da7b569fed4ffb`
- G11555_VERDICT: `C:\VS\Stam_model-A-v1.0\audit\audits\VERDICT_G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM_2026_06_03.md` sha256 `2ae3a892572112d34a2a478136fe040bf8a639c6206b5047448ea9e48469e50b`
- G11555_CHECKS: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM\G11555_checks.csv` sha256 `0c714b2b776e28bac1e9777ad160b7ecb9f213a26f82218f7baacd78dcfd60c4`
- G11555_WRONG_CONTROLS: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM\G11555_wrong_controls.csv` sha256 `9528676b5135f89df0a18274a1e73376a6f6b4bd31534b5398d820b74e2f35b1`
- G11555_LANES: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM\G11555_observer_lanes.csv` sha256 `914414d1b9a6beae7300f334382485611a99e0f79050fb2f7c5c377bd8416668`
- RADIX_ROUTE_KERNEL: `C:\VS\Stam_model-A-v1.0\sam\radix_route_kernel.py` sha256 `4d2caf96435489ffa4673915cd97482c94e42f8908fda9a1cdc93e3217eca72f`
- G585C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G585c_A_SHARE_SIDE_STATUS_SELECTOR_WITH_ROUTE_DEPTH\G585c_summary.json` sha256 `5f0683b23eefce74833ab5d7910389ef864ff7d35880fbc28a1dbe850edbe6b0`
- G586C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G586c_HORIZON_NORMAL_SIDE_PAIR_COMPATIBILITY_SELECTOR\G586c_summary.json` sha256 `669a9825461a7f81da8b61e8e816dda05352ff5eb5abf256fdc0f2eaadd0282f`
- G587C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G587c_TWO_PIECE_MANIFOLD_READING_LAB\G587c_summary.json` sha256 `e4d992533d5a75d650ba72db1d954dcf61f0ebac47cf268ff3b042acb54b8d78`
- G587C_VERDICT: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G587c_TWO_PIECE_MANIFOLD_READING_LAB\G587c_verdict.md` sha256 `37c79ecc6b3ebf366757cccd5c61146a1d4db6f61b75c83f9aa5f5c6d376bc27`
- G587C_VALIDATION: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G587c_TWO_PIECE_MANIFOLD_READING_LAB\G587c_validation_checks.csv` sha256 `689260a9f597582e5a7234ef4a071a8660d7b0fb9c9c48c80f68a4287892e31b`
- G587C_WRONG_CONTROLS: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G587c_TWO_PIECE_MANIFOLD_READING_LAB\G587c_wrong_controls.csv` sha256 `12cc0824a236cd0792d97c2a6d73935196390a2b5049a81a5d1ee38bac91a9e6`
- G588C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G588c_V4_1_MANIFOLD_REFINEMENT_FINAL_AUDIT\G588c_summary.json` sha256 `7013119ad1272b1e6d4557ca69545f50aa56fe846553a65452f342972184a7f2`
- G588C_PROMOTABLE_TABLE: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G588c_V4_1_MANIFOLD_REFINEMENT_FINAL_AUDIT\G588c_promotable_refinement_table.csv` sha256 `5cce50da99c272f8f88c3bc9d701a4d34fe772b64fc5c6049c7b21a2a349b57e`
- G588C_KERNEL_COHERENCE: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G588c_V4_1_MANIFOLD_REFINEMENT_FINAL_AUDIT\G588c_kernel_coherence_check.csv` sha256 `0d83c8ed6185c4da7c0e64f9e93e608a0e090a59069954b577bff2b1c3bc4299`
- G591C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G591c_CONJUGATE_PAIR_ROLE_ASSIGNMENT_SELECTOR\G591c_summary.json` sha256 `8846447d23170febd56acf06dfd9041580050cf5bbc047138663d66b47629d33`
- G609C_SUMMARY: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G609c_BIPARTITE_WRITE_D_3_COUNT_AUDIT\G609c_summary.json` sha256 `e460899b90e0d5d0b43fc5af70b9b3811272899fdd94b9760d20859f4f51c14f`

## Pass Checks

- PASS P1_sources_present: All load-bearing source artifacts are present.
- PASS P2_A1_boundary_closure: G11555 closes A=1 as the horizon bell and rejects A>1 as parent-ledger write.
- PASS P3_G11555_two_lanes_agree: Outside observer and infaller lanes both reject completed parent-ledger crossing.
- PASS P4_astronaut_phrase_has_provenance_but_is_not_load_bearing: The literal astronaut-falls-forever wording exists in recursion provenance; G11555 supplies theorem wording.
- PASS P5_manifold_measure_four: G587c/G588c support M_w = outside 2D + inside 2D = 4.
- PASS P6_route_depth_three: The radix kernel and G587c support D_route = 1/2 + 1/2 + 1 + 1 = 3.
- PASS P7_product_closes_R12: Completed-WRITE address count closes as M_w * D_route = 4 * 3 = 12.
- PASS P8_face_axis_and_route_axis_are_distinct: The face axis and route-depth axis are not collapsed into one count.
- PASS P9_no_double_counting_pair_compatibility: G585c/G586c/G591c/G609c support side completion, pair compatibility, M_out/M_in roles, and D=3 count.
- PASS P10_priority_record_matches_R_first_chain: Current priority record uses R-first completed-WRITE address count and retires 2*pi as first-line R defense.

## Wrong Controls

- REJECTED WC1_single_unoriented_2D_surface: Count only one unoriented 2D surface so M_w=2.
- REJECTED WC2_ordinary_3D_volume_at_A1: Treat A=1 as ordinary traversable 3D volume with completed parent crossing.
- REJECTED WC3_additive_4_plus_3: Use additive address count 4+3 instead of product address count.
- REJECTED WC4_D_route_as_spatial_dimension: Treat D_route=3 as the spatial dimension primitive rather than route-depth.
- REJECTED WC5_double_count_faces: Turn M_out/M_in into two extra full W_in pieces rather than a split unit.
- REJECTED WC6_2pi_or_A0_smuggling: Derive R from 2*pi/A0 normalization instead of from completed WRITE address count.
- REJECTED WC7_wrong_route_contacts: Use five-half, seven-half, full-contact, or triadic route variants.
- REJECTED WC8_GR_finite_infaller_equals_SAM_parent_crossing: Declare finite GR infaller continuation to be completed SAM parent-ledger crossing.

## Scope

- Closes A4 completed-WRITE address count at structural theorem-gate grade.
- Does not derive D=3 from scratch; D remains inherited from the accepted D primitive / route kernel.
- Does not derive alpha_H=2 from scratch; M_w uses the oriented-boundary surface reading already promoted by G587c/G588c.
- Does not use 2*pi or A0 to derive R; A0 is downstream normalization after R=12 is fixed.
- Does not claim full black-hole, cosmology, or matter-spectrum theorem closure.

## Open Debts

- Reviewer may still ask for a prose theorem write-up in the manuscript/audit narrative.
- G587c caveat is now narrowed by this closure gate but should be quoted honestly as structural theorem-gate grade, not primitive-from-nothing grade.

## Hash

```text
CR113_completed_write_address_count_lock.json sha256 = 6892987bdd978f03fa42cb7d0ef14e24cdd08e11e154ef8ced5cd5ede3fd15b4
```
