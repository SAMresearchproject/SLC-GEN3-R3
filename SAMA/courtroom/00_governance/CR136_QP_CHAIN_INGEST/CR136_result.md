# CR136 qp_chain Ingest v1.0

## Verdict

```text
CR136_QP_CHAIN_INGEST_V1_SEALED
```

## Scope

CR-120, CR-121, and CR-122 cite SHA-256 hashes of artifacts that physically live OUTSIDE The_Courtroom at `C:/VS/quantum_phase/artifacts/`. A reviewer cloning the repo cannot reproduce any Higgs-or-gravity-related claim because the artifacts those hashes refer to are not in the repository. CR-136 ingests the referenced artifacts (bit-identical, SHA-verified) into `The_Courtroom/upstream_artifacts/`, producing an internal copy whose SHA-256 matches what the consuming CRs recorded.

This is an INGEST, not a verdict change. CR-120, CR-121, and CR-122 themselves are NOT modified by CR-136 -- the chain of custody is preserved by adding an internal copy alongside the external original, not by editing the consuming CRs. A reviewer who wants to verify any cited SHA-256 looks it up in `CR136_ingest_manifest.csv` to find the internal path, then runs `Get-FileHash` to confirm the value matches.

## Inputs

- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
- CR-120 ledger: `09a_PARTICLE_MASS_CHAIN\CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE\CR120_qp091_chain_ledger.csv`
- CR-121 ledger: `11_QUANTUM_MECHANICS_AND_GRAVITY\CR121_SAM_GRAVITY_MECHANISM_INTAKE\CR121_mechanism_chain_ledger.csv`
- External qp_chain root: `C:\VS\quantum_phase\artifacts`
- Internal destination: `upstream_artifacts/`
- Source manifest: `CR136_source_manifest.csv`

## Ingest Summary

- **Total targets discovered:** 42
- **ALREADY_INGESTED:** 42

## Predictions

- **[PASS]** P1_external_root_accessible -- C:\VS\quantum_phase\artifacts exists = True
- **[PASS]** P2_targets_discovered_from_consuming_CRs -- discovered 42 unique (folder, summary_file) targets across CR-120, CR-121, CR-122 ledgers
- **[PASS]** P3_all_externals_present -- present: 42/42
- **[PASS]** P4_external_sha_matches_recorded -- sha-matches-recorded: 42/42
- **[PASS]** P5_all_targets_ingested_or_already_ingested -- in-clean-state: 42/42 (statuses: ALREADY_INGESTED)
- **[PASS]** P6_internal_sha_matches_external_sha -- every ingested artifact's internal copy hashes to the same value as its external source

## Wrong Controls

- **[PASS]** WC1_external_root_exists -- C:\VS\quantum_phase\artifacts present = True
    - load-bearing deletion: If the external qp_chain root is missing, ingest cannot proceed; this WC would FAIL.
- **[PASS]** WC2_manifest_covers_all_consuming_CR_references -- required: 42; covered: 42; missing: none
    - load-bearing deletion: If any consuming-CR reference were not in the manifest, this WC would FAIL.
- **[PASS]** WC3_no_duplicate_internal_paths -- no duplicate destination paths
    - load-bearing deletion: If two distinct artifacts mapped to the same internal path, the second copy would clobber the first; this WC would FAIL.
- **[PASS]** WC4_internal_copies_match_consumer_recorded_sha -- internal-sha matches consumer-recorded-sha on 42 of 42 cleanly ingested artifacts
    - load-bearing deletion: If any internal copy's SHA disagreed with what CR-120/121/122 recorded, the chain of custody breaks; this WC would FAIL.
- **[PASS]** WC5_no_anomalies -- anomalous statuses: 0
    - load-bearing deletion: If any target had a SHA mismatch, was missing, or had internal drift, this WC would FAIL.
- **[PASS]** WC6_audit_verdict_reference_resolves -- AUDIT_VERDICT exists=True; hash matches
    - load-bearing deletion: If the audit verdict moved/edited, the recorded reference would be unverifiable.
- **[PASS]** WC7_CR122_qp092h_reference_resolves_internally -- qp092h internal copy = upstream_artifacts\qp092\qp092h_baryon_cmb_carrier_gate\qp092h_summary.json; SHA matches CR-122 recorded value = True
    - load-bearing deletion: If CR-122's qp092h reference does NOT resolve to an internal artifact with the expected SHA, the carrier-compression gate cannot be audited from inside the repo.

## Per-Artifact Manifest (sample of first 8 + last 4)

| Folder | Summary file | Consumers | Recorded SHA-256 (first 12) | Internal path | Status |
| --- | --- | --- | --- | --- | --- |
| `campaign08_qp091b_h_freeze` | `campaign08_qp091b_h_freeze_summary.json` | CR-120 | `b9237ea09dd6...` | `upstream_artifacts/qp091/campaign08_qp091b_h_freeze/campaign08_qp091b_h_freeze_summary.json` | ALREADY_INGESTED |
| `qp091a` | `qp091a_summary.json` | CR-120 | `55f6dc3fefe3...` | `upstream_artifacts/qp091/qp091a/qp091a_summary.json` | ALREADY_INGESTED |
| `qp091aa` | `qp091aa_summary.json` | CR-120 | `eb0296a65a7b...` | `upstream_artifacts/qp091/qp091aa/qp091aa_summary.json` | ALREADY_INGESTED |
| `qp091ab` | `qp091ab_summary.json` | CR-120 | `d4edaec75cbf...` | `upstream_artifacts/qp091/qp091ab/qp091ab_summary.json` | ALREADY_INGESTED |
| `qp091ac` | `qp091ac_summary.json` | CR-120 | `8e5b3efcf0bd...` | `upstream_artifacts/qp091/qp091ac/qp091ac_summary.json` | ALREADY_INGESTED |
| `qp091ad` | `qp091ad_summary.json` | CR-120 | `511b25f604fe...` | `upstream_artifacts/qp091/qp091ad/qp091ad_summary.json` | ALREADY_INGESTED |
| `qp091b` | `qp091b_summary.json` | CR-120 | `7d0cc8681f28...` | `upstream_artifacts/qp091/qp091b/qp091b_summary.json` | ALREADY_INGESTED |
| `qp091c` | `qp091c_summary.json` | CR-120 | `79261edb19f9...` | `upstream_artifacts/qp091/qp091c/qp091c_summary.json` | ALREADY_INGESTED |
| `qp092e_weak_field_external_readout` | `qp092e_summary.json` | CR-121 | `d92ce93c234a...` | `upstream_artifacts/qp092/qp092e_weak_field_external_readout/qp092e_summary.json` | ALREADY_INGESTED |
| `qp092f_tensor_carrier_wave_mode` | `qp092f_summary.json` | CR-121 | `b122cec6fd33...` | `upstream_artifacts/qp092/qp092f_tensor_carrier_wave_mode/qp092f_summary.json` | ALREADY_INGESTED |
| `qp092g_tensor_carrier_bridge_packet` | `qp092g_summary.json` | CR-121 | `b5ee2482db3c...` | `upstream_artifacts/qp092/qp092g_tensor_carrier_bridge_packet/qp092g_summary.json` | ALREADY_INGESTED |
| `qp092h_baryon_cmb_carrier_gate` | `qp092h_summary.json` | CR-121,CR-122 | `5b8139aa9088...` | `upstream_artifacts/qp092/qp092h_baryon_cmb_carrier_gate/qp092h_summary.json` | ALREADY_INGESTED |

*(showing 8 + 4 of 42 total; full table in `CR136_ingest_manifest.csv`)*

## Falsifier (LOCKED)

Re-executing `CR136_runner.py` on the post-ingest state MUST produce zero new `INGESTED` entries (only `ALREADY_INGESTED`), zero SHA mismatches between external and internal copies, and the recomputed lock SHA-256 MUST match the value recorded here. Any deviation falsifies v1.0.

**Free parameters:** 0.

## Cryptographic Chain

```text
CR135_audit_verdict_sha256                = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
CR136_source_manifest_csv                 = 3e403338cab189a50d4cfe1e4362ce4b99036dcd52d991292da59c8f83b6f22d
CR136_ingest_manifest_csv                 = 9adfb3746dbbb5e6abb3c11fd07e954779f927d9472c5819b0f574b581ecef4a
CR136_predictions_csv                     = 83c1ad764fbaf375d0e0c16cc7fb9a97ab00d09bcff0b5ac93eea2feca03d22f
CR136_wrong_controls_csv                  = bf9d31d84cdafd8e598793cdd75cadbf8df4e903dba80f327d1321c1680a1a7d
CR136_ingest_lock_json                    = 2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c
```

## Follow-up CRs

- **CR-139** (CR-122 verdict regrade): can now reference internal qp092h path when adding its header block.
- **CR-140** (Higgs claim reword): can now reference internal qp091t / qp091r paths when adding its header block.
- **CR-136b** (optional): rewrite CR-120/121/122 runner.py files to point at internal paths so the runners are themselves re-executable from inside The_Courtroom alone. NOT required for audit-driven hash resolution.

## Rule of Immutability

Ingest manifest, internal destinations, falsifier, and wrong controls are frozen at CR-136 seal time. Future falsification (failed idempotency, new SHA mismatches, missing ingest entries) must be in an appeal CR within `00_governance/`.
