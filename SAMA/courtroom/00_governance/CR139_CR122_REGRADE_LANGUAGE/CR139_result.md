# CR139 CR-122 Verdict Language Regrade (SEALED -> BOUNDARY) v1.0

## Verdict

```text
CR139_CR122_REGRADE_LANGUAGE_V1_SEALED
```

## Scope

CR-122 sealed with the headline language 'Direct qA-as-mass would overread Planck Omega_b h^2 by 0.66-0.99 percent (max 1.475 sigma) - REJECTED everywhere.' The hostile audit identified this as a Tier 3 categorical-language overclaim: 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14), which DISFAVORS the alternative but does NOT reject it at conventional thresholds. CR-139 regrades the verdict from PASS to BOUNDARY, preserves the historical declaration verbatim for audit traceability, and adds an audit_regrade block to summary.json plus a header block to result.md documenting the disfavoring-vs-rejection distinction.

The underlying carrier-compression mechanism (1/8 + qA -> ledger compression -> A readout) is PRESERVED. The 10 gated downstream CRs (CR016, CR018-CR023 in 07 and 08, CR111, CR114, CR117) remain sealed with their original verdicts -- they ride on the mechanism, not on the statistical strength of the rejection claim.

## Inputs

- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
- qp_chain ingest lock: `00_governance/CR136_QP_CHAIN_INGEST/CR136_ingest_lock.json` (`2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c`)
- Target: `00_governance/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/`
- Source manifest: `CR139_source_manifest.csv`

## Statistical Evidence

| Quantity | Value |
| --- | --- |
| max_sigma_vs_planck | 1.4753 |
| approx_one_sided_p_value | 0.0701 |
| approx_two_sided_p_value | 0.1402 |
| overread_min_percent | 0.6631 |
| overread_mean_percent | 0.8808 |
| overread_max_percent | 0.9947 |
| conventional_rejection_threshold_sigma | 3.0 |
| conventional_tension_threshold_sigma | 2.0 |

**Conclusion:** 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14), which DISFAVORS direct qA-as-mass but does not REJECT it at conventional thresholds (typically 2-sigma for 'tension' and 3-sigma for 'strong tension').

## Target Outcome

- **Status:** ALREADY_REGRADED
- **From verdict:** `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED`
- **To verdict:** `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED`
- **Result.md SHA-256:** `f4afeafda1f950b61709b996f2c2a34a5f698b99a302b7cb4039a355f09dbca0`
- **Summary.json SHA-256:** `71e5cae00152f03f8fd77e40245fb928ebe7dd7382c460eb31ab44698fe29d32`
- **Archived original result.md SHA-256:** `ad657f42b3e423440f57fd95e4a08ddf33710120543747855d5b7ce8ce01a883`
- **Archived original summary.json SHA-256:** `0108980571c1fec4103cbf91a36c1bfb21cc84f5f3ba99ae2a2d9064a1a5ada1`

## Predictions

- **[PASS]** P1_CR122_target_exists -- target dir = C:\VS\The_Courtroom\00_governance\CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE
- **[PASS]** P2_archived_original_was_SEALED -- archived result_class = 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED'
- **[PASS]** P3_regrade_applied_or_already_applied -- status = ALREADY_REGRADED
- **[PASS]** P4_post_regrade_result_class_is_BOUNDARY_string -- current result_class = 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED'
- **[PASS]** P5_CR136_ingest_dependency_resolved -- qp092h internal copy present with expected SHA
- **[PASS]** P6_restoration_requirements_documented_with_concrete_items -- REPLACEMENT_RECORD names Planck and 3 sigma threshold concretely.

## Wrong Controls

- **[PASS]** WC1_archived_original_was_PASS -- archived result_class = 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED'; expected 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED'
    - load-bearing deletion: If archived original had a different verdict, the regrade would be operating on the wrong starting point.
- **[PASS]** WC2_current_result_class_is_BOUNDARY -- current result_class = 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED'; expected 'CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED'
    - load-bearing deletion: If result_class were not updated to the BOUNDARY string, this WC would FAIL.
- **[PASS]** WC3_archived_originals_hash_match -- Archived hashes match recorded.
    - load-bearing deletion: If archived originals were edited/corrupted, this WC would FAIL.
- **[PASS]** WC4_audit_regrade_block_well_formed_and_from_neq_to -- audit_regrade present with correct fields and from != to.
    - load-bearing deletion: If from_verdict == to_verdict or required field stripped, this WC would FAIL.
- **[PASS]** WC5_audit_verdict_reference_resolves -- AUDIT_VERDICT exists=True; hash matches
    - load-bearing deletion: If audit verdict moved/edited, this WC would FAIL.
- **[PASS]** WC6_qp092h_ingest_dependency_satisfied -- qp092h internal copy exists = True; SHA matches expected = True
    - load-bearing deletion: If qp092h were not internally ingested per CR-136, CR-139's narrative (carrier-compression mechanism preserved with internal hash resolution) would not hold.
- **[PASS]** WC7_statistical_evidence_documented -- statistical_evidence missing = []; max_sigma_value_matches = True
    - load-bearing deletion: If statistical_evidence were stripped or sigma value altered, regrade rationale would be unsupported.
- **[PASS]** WC8_preserved_mechanism_and_downstream_verdicts_documented -- preserved_mechanism block has downstream_verdicts_unchanged=True and >= 10 gated CRs listed = True
    - load-bearing deletion: If preserved_mechanism were stripped or downstream CR list were short, the regrade would risk being read as mechanism refutation.

## Restoration Requirements (path back to PASS for CR-122)

To restore CR-122 to PASS (genuine 'REJECTED' status), **any one** of the following must hold:

1. Improved Planck-lite (or successor) precision on Omega_b h^2 such that the 0.66-0.99% overread interval corresponds to >= 3 sigma (conventional 'strong tension' threshold), promoting the disfavoring to a genuine rejection.
    - *how to verify:* Reviewer reads the Planck-lite (or successor) reported sigma on Omega_b h^2 in the current verified data release, computes 0.66-0.99% as a sigma multiple, and confirms it crosses 3 sigma. Source verification (peer-reviewed paper or Planck Collaboration release) required.
2. Independent dataset (DES, SPT, ACT, or successor) reaching the same 0.66-0.99% overread interval at >= 3 sigma significance, confirming the disfavoring is not Planck-specific.
    - *how to verify:* Reviewer reads the independent-dataset result, confirms a comparable overread is reported, confirms the sigma significance is >= 3, and confirms the dataset is genuinely independent of Planck (not a re-analysis of the same data).
3. OR a theoretical structural argument internal to SAM that forbids direct-qA-as-mass independent of Planck contact (e.g., from CR-121's 1/8 release mechanism plus a no-double-counting axiom). If structurally forbidden, the 1.475 sigma empirical contact is supporting evidence rather than the sole basis for rejection.
    - *how to verify:* Reviewer reads the structural argument, confirms it does not depend on the Planck-Omega_b comparison, and confirms it explicitly forbids the rejected route at the level of SAM's substrate-write grammar.

### Restoration Falsifier

A high-precision dataset (Planck successor, joint Planck+DES, or any independent CMB+LSS combination) reaching the same 0.66-0.99% overread interval at LOWER sigma significance than current Planck-lite (e.g., 1.0 sigma) would BLOCK restoration, because the disfavoring would be weaker rather than stronger. Empirical regression of the disfavoring level is a blocking condition.

## CR-139 Falsifier (LOCKED)

Re-executing `CR139_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match.

**Free parameters:** 0.

## Cryptographic Chain

```text
CR135_audit_verdict_sha256                = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
CR136_ingest_lock_sha256                  = 2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c
CR139_source_manifest_csv                 = 51de903614eaf874d2f69732f59e940e692b0698fe38cfc2f9e94e925a19ee55
CR139_regrade_manifest_csv                = 634b4f18914d715dcf101b2b00b88453375f7db764363e12ad78c243b6596e26
CR139_predictions_csv                     = 17ea61db9eae47a402a4988e650a8e1c10e0a19c113e053248e165097e18a714
CR139_wrong_controls_csv                  = 1e56ffa6374a4e16c0e7d5a75a4ef7a83b97da906ca3aed4f54d8106d7110ed8
CR139_regrade_lock_json                   = 329372c4c51046832b337ced42f0cd2af51ca0c6430f005630c66abacaaaf6f9
```

## Rule of Immutability

Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-139 seal time. Future falsification must be in an appeal CR.
