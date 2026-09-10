# REPLACEMENT_RECORD -- CR-122 verdict language regrade (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `00_governance/CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE/CR122_result.md` and `CR122_summary.json` |
| Original result.md SHA-256 | `ad657f42b3e423440f57fd95e4a08ddf33710120543747855d5b7ce8ce01a883` |
| Original summary.json SHA-256 | `0108980571c1fec4103cbf91a36c1bfb21cc84f5f3ba99ae2a2d9064a1a5ada1` |
| Original verdict | `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `f4afeafda1f950b61709b996f2c2a34a5f698b99a302b7cb4039a355f09dbca0` |
| Replacement summary.json SHA-256 | `71e5cae00152f03f8fd77e40245fb928ebe7dd7382c460eb31ab44698fe29d32` |
| Replacement verdict | `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED` |
| Verdict direction | `DOWNGRADED` |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-139 CR-122 verdict language regrade |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (categorical rejection language unsupported by 1.475 sigma) |
| Audit finding tier | `Tier 3 REGRADE_TO_BOUNDARY` |
| Ingest dependency | CR-136 qp_chain ingest lock `2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c` |

## 3. Defect summary

CR-122's headline claim stated that direct qA-as-mass is "REJECTED everywhere" at a maximum significance of 1.4753 sigma against Planck Omega_b h^2. In conventional inferential statistics, 1.475 sigma corresponds to a one-sided p-value of approximately 0.07 (two-sided ~0.14) -- a result that DISFAVORS the alternative but does NOT reject it. Conventional rejection thresholds are typically 2 sigma ("tension") or 3 sigma ("strong tension"); 1.475 sigma is below both.

The categorical "REJECTED" framing is a stronger statement than the 1.475 sigma evidence supports. The underlying carrier-compression mechanism (1/8 + qA = gravity path through ledger compression) is structurally meaningful and is **preserved** by this regrade. So are the 10 gated downstream CRs that ride on the mechanism. The regrade affects the linguistic strength of the rejection claim, not the structural content of CR-122.

## 4. What changed

- The verdict line in `CR122_result.md` is regraded from `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_SEALED__TEN_PRIOR_CRS_UNIFIED_NONE_INVALIDATED` to `CR122_CARRIER_COMPRESSION_GATE_RETROACTIVE_BRIDGE_BOUNDARY__REJECTED_DOWNGRADED_TO_DISFAVORED_AT_1_475_SIGMA__MECHANISM_PRESERVED`.
- The `result_class` field in `CR122_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR122_summary.json` documenting the statistical evidence, the preserved mechanism, and the CR-136 ingest dependency.
- A header block is prepended to `CR122_result.md` linking to this archive entry and explaining the disfavoring vs rejection distinction.
- The headline language inside the result.md (`Direct qA-as-mass would overread Planck Omega_b h^2 by 0.66-0.99 percent (max 1.475 sigma) - REJECTED everywhere.`) is **preserved verbatim as the historical declaration** so the regrade is auditable rather than silent. The header block + new verdict line provide the corrected interpretation.

## 5. Restoration requirements (path back to PASS)

To restore CR-122 to PASS (genuine "REJECTED" status), **any one** of the following must hold:

1. Improved Planck-lite (or successor) precision on Omega_b h^2 such that the 0.66-0.99% overread interval corresponds to >= 3 sigma (conventional 'strong tension' threshold), promoting the disfavoring to a genuine rejection.
   - *how to verify:* Reviewer reads the Planck-lite (or successor) reported sigma on Omega_b h^2 in the current verified data release, computes 0.66-0.99% as a sigma multiple, and confirms it crosses 3 sigma. Source verification (peer-reviewed paper or Planck Collaboration release) required.
2. Independent dataset (DES, SPT, ACT, or successor) reaching the same 0.66-0.99% overread interval at >= 3 sigma significance, confirming the disfavoring is not Planck-specific.
   - *how to verify:* Reviewer reads the independent-dataset result, confirms a comparable overread is reported, confirms the sigma significance is >= 3, and confirms the dataset is genuinely independent of Planck (not a re-analysis of the same data).
3. OR a theoretical structural argument internal to SAM that forbids direct-qA-as-mass independent of Planck contact (e.g., from CR-121's 1/8 release mechanism plus a no-double-counting axiom). If structurally forbidden, the 1.475 sigma empirical contact is supporting evidence rather than the sole basis for rejection.
   - *how to verify:* Reviewer reads the structural argument, confirms it does not depend on the Planck-Omega_b comparison, and confirms it explicitly forbids the rejected route at the level of SAM's substrate-write grammar.


### 5a. Restoration falsifier

A high-precision dataset (Planck successor, joint Planck+DES, or any independent CMB+LSS combination) reaching the same 0.66-0.99% overread interval at LOWER sigma significance than current Planck-lite (e.g., 1.0 sigma) would BLOCK restoration, because the disfavoring would be weaker rather than stronger. Empirical regression of the disfavoring level is a blocking condition.

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite the specific verified dataset and confidence calculation supporting the >= 3 sigma claim

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-122 record does NOT:

- Refute the carrier-compression mechanism. The 1/8 + 7/8 split, ledger compression to A readout, and the admission gate for baryon/CMB inventory all remain SAM-native structural claims.
- Re-evaluate any of the 10 gated downstream CRs. CR016, CR018-CR023 (in 07 and 08), CR111, CR114, CR117 remain sealed with their original verdicts.
- Touch the qp092h source artifact. The internal copy at `upstream_artifacts/qp092/qp092h_baryon_cmb_carrier_gate/qp092h_summary.json` is unchanged from CR-136 ingest.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | UNKNOWN | result.md `ad657f42...e01a883` / summary.json `01089805...1a5ada1` | CR122 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| qp_chain ingest | 2026-06-17 | ingest lock `2d6db0a6...55a4d2c` | CR-136 ingest |
| Replacement sealed | 2026-06-17 | result.md `f4afeafd...09dbca0` / summary.json `71e5cae0...fe29d32` | CR-139 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-122 finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR122.md`
- qp_chain ingest: `00_governance/CR136_QP_CHAIN_INGEST/CR136_result.md`
- Event README: `../EVENT_README.md`
- CR-139 result: `00_governance/CR139_CR122_REGRADE_LANGUAGE/CR139_result.md`
