# CR276 — Particle Sieve Anchoring Table — RESULT

**Verdict:** PASS
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Precommit:** `d9babfc8e319db4fec4d044c6d7ab1d84f2509bc4107b0beb8b36afef8e804db`

## Gates

| gate | result |
| --- | :---: |
| G1_all_categorized | PASS |
| G2_pdg_anchored_matches_6 | PASS |
| G3_fold_identity_preserved | PASS |
| G4_bow_trace_pair_tagged | PASS |
| G5_identity_class_counts | PASS |
| G6_rejected_reasons_preserved | PASS |
| G7_hash_whitelist | PASS |

## Row counts by category

| category | count |
| --- | ---: |
| COMPOSITE_UNANCHORED | 171 |
| SAM_ORPHAN | 114 |
| REJECTED | 21 |
| PDG_CANDIDATE | 9 |
| PDG_ANCHORED | 6 |
| **TOTAL** | **321** |

## PDG-anchored rows

| candidate_id | PDG | SAM role | sealed CR |
| --- | --- | --- | --- |
| QP093A-0299 | Higgs (H) | closed_scalar_loop_parent | known_match column + CR269 |
| QP093A-0300 | graviton | T13_named_carrier | Vol II.1 §9.5 |
| QP093A-0301 | photon | T13_named_carrier | Vol II.1 §9.5 |
| QP093A-0302 | W | T13_named_carrier | Vol II.1 §9.5 |
| QP093A-0303 | Z | T13_named_carrier | Vol II.1 §9.5 |
| QP093A-0304 | gluon | T13_named_carrier | Vol II.1 §9.5 |

## Vol II.1 §10.5 identity class counts (CR253 subset)

| identity class | expected | got |
| --- | ---: | ---: |
| electron_like_minus | 2 | 2 |
| positron_substrate_slot | 2 | 2 |
| heavier_charged_lepton_minus | 2 | 2 |
| heavier_positron_substrate_slot | 2 | 2 |
| neutrino_like | 2 | 2 |
| quark_like_charged | 56 | 56 |
| neutral_higher_partition | 14 | 14 |

## SAM_ORPHAN role breakdown

| SAM role | count |
| --- | ---: |
| quark_like_charged | 76 |
| neutral_higher_partition | 21 |
| lifted_connector | 8 |
| positron_substrate_slot_conjugate | 3 |
| positron_substrate_slot | 1 |
| bow_trace_matter_only | 1 |
| heavier_positron_substrate_slot | 1 |
| third_generation_positron_substrate_slot | 1 |
| hard_zero_falsifier | 1 |
| SAM_accumulation_field_carrier | 1 |
| **TOTAL SAM_ORPHAN** | **114** |

## What this CR seals

The 321-row CR252 catalog is now row-indexed by sealed-CR anchor. Downstream work (mass-lift derivation, hadron identification, forecast locks) reads from CR276_anchoring_table.csv rather than having to re-derive scattered particle-side identifications from Vol II.1 sections and downstream CRs.

## Provenance

- CR252 catalog sha256 = `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`
- Precommit sha256 = `d9babfc8e319db4fec4d044c6d7ab1d84f2509bc4107b0beb8b36afef8e804db`
- Stewardship sha256 = `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`