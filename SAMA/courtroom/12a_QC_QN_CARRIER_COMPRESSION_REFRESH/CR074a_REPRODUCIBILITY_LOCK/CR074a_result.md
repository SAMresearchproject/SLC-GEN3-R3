# CR074a Reproducibility Lock - Result

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR074a/6)

**Result class:** `CR074a_REPRODUCIBILITY_PACK_SEALED__PREDICTIONS_11_OF_11__WRONG_CONTROLS_9_OF_9__PACK_FILES_50__HASH_MATCHES_40_OF_40__PYTHON_3.12.10__DISCIPLINE_DRIFT_NUMPY_AND_MATPLOTLIB_PER_CR_VS_ACTUAL_CAUGHT_AND_RESOLVED`

**Predictions passed:** 11/11
**Wrong controls passed:** 9/9
**Free parameters:** 0

## Honest aggregate verdict

CR074a sealed the reproducibility lock for the Paul Revere Field Comparison Campaign. CAMPAIGN_REPRODUCIBILITY_PACK.zip emitted with 50 files (44 CR artifacts + 6 pack-level files + 1 stewardship + 1 campaign doc). All 40 of 40 per-CR HASHES.txt entries verified against on-disk SHA-256. Pinned to Python 3.12.10 + numpy 2.4.4 + matplotlib 3.10.9 (ACTUAL versions used). Discipline drift finding caught: per-CR requirements.txt files declared numpy==1.26.4 + matplotlib==3.8.4 but actual installed versions differed; pack-level requirements.txt pins ACTUAL versions; per-CR pins preserved as historical artifacts. No stochastic steps in any runner; seeds.json documents the empty stochastic inventory. CAMPAIGN_RERUN.md provides partner-lab rerun procedure. STEWARDSHIP.md included verbatim. Predictions 11/11 pass; wrong controls 9/9 pass.

## Reproducibility pinning

- Python: `3.12.10`
- Pinned requirements (ACTUAL): `numpy==2.4.4, matplotlib==3.10.9`
- Per-CR declared (DRIFT): `numpy==1.26.4, matplotlib==3.8.4`
- Pack file: `CAMPAIGN_REPRODUCIBILITY_PACK.zip`
- Pack file count: 50
- Hash verifications: 40/40

## Predictions

- **[PASS]** P1_all_CR_directories_present_with_expected_artifacts
- **[PASS]** P2_every_artifact_hash_matches_HASHES_txt_entry
- **[PASS]** P3_pinned_requirements_use_equals_equals
- **[PASS]** P4_python_version_pin_is_exact
- **[PASS]** P5_seeds_json_documents_all_stochastic_steps
- **[PASS]** P6_CAMPAIGN_RERUN_md_exists_and_self_contained
- **[PASS]** P7_STEWARDSHIP_md_included_verbatim
- **[PASS]** P8_pack_does_not_include_external_non_citation_data
- **[PASS]** P9_pack_is_single_file_emission
- **[PASS]** P10_discipline_drift_finding_documented
- **[PASS]** P11_protocol_completes_end_to_end

## Wrong controls

- **[PASS]** WC1_requirements_with_loose_pin_rejected
- **[PASS]** WC2_missing_CR_artifact_detected
- **[PASS]** WC3_hash_mismatch_in_pack_vs_HASHES_txt_detected
- **[PASS]** WC4_missing_STEWARDSHIP_md_rejected
- **[PASS]** WC5_no_Docker_requirement
- **[PASS]** WC6_runner_does_not_modify_upstream_artifacts
- **[PASS]** WC7_no_free_parameters
- **[PASS]** WC8_pack_does_not_include_partner_lab_claims
- **[PASS]** WC9_per_CR_pin_drift_is_caught_not_silently_corrected

## Discipline drift caught

Per-CR `requirements.txt` files in CR070a, CR072a, CR073a declared `numpy==1.26.4` and `matplotlib==3.8.4`. Actual installed versions during the campaign run were `numpy==2.4.4` and `matplotlib==3.10.9`. CR074a's pack-level `requirements.txt` pins the ACTUAL versions so a partner lab gets byte-identical results. Per-CR files are preserved as historical artifacts; changing them would require new CRs.

This is the kind of finding the reproducibility CR is FOR. Reported openly per the campaign's max-testing-failures-included discipline.

## Scope boundary

CR074a IS:
- A single-file reproducibility pack a partner lab can rerun
- A hash-verified bundle of CR070a-CR073a artifacts
- A pinned-environment spec (Python + deps + seeds) for byte-identical reproduction

CR074a IS NOT:
- A partner-lab agreement
- A hardware deployment
- A commercial protocol claim

## Stewardship

Per `STEWARDSHIP.md`.
