# REPLACEMENT_RECORD -- CR-120 Higgs claim reword (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_result.md` and `CR120_summary.json` |
| Original result.md SHA-256 | `5f8be2e5c0f37e6413e3785014f06f41754456a0b91ed40ab605b71e8ca235d2` |
| Original summary.json SHA-256 | `2eca623b608b3e367a5b366bc7515801b9bf5b6823a1a90aa992a57e12741388` |
| Original verdict | `CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `11b12761115e01cfc6a48635950ec5571cc2752046dcfb9853135e7a2e5ca7f3` |
| Replacement summary.json SHA-256 | `32a8a3147e2a711ad706f060b65133503ae7b15c92fa5fd927daa6c857687a82` |
| Replacement verdict | `CR120_QP091_CHAIN_INTAKE_BOUNDARY__HIGGS_125_25_PDG_MATCH__STRUCTURAL_NATIVE_126_PREDATES_VALUE__CORRECTION_FORM_IDENTIFIED_EX_POST__FORWARD_BLIND_PRECOMMIT_REQUIRED` |
| Verdict direction | `DOWNGRADED` |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-140 CR-120 Higgs claim reword |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion failed | `C4 FREE_PARAMETERS_HONESTLY_ZERO` and `C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA` |
| Audit finding tier | `Tier 4 DEMAND_RETEST + Tier 6 HASH_CHAIN_BREAK` (HCB resolved by CR-136) |
| Ingest dependency | CR-136 qp_chain ingest lock `2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c` |

## 3. Defect summary

CR-120's headline language stated H_reveal = R^2*(1-2^-D) - D^2/R = 125.25 GeV "EXACT, derived from {R=12, D=3} alone with zero free parameters, no H input." Forensic chronology of the upstream qp091 chain reveals the form-selection process:

- **qp091o/p (earlier same authoring session):** Made the 2.27 MeV gap between H_native = R^2*(1-2^-D) = 126 GeV and the measured PDG H = 125.25 GeV visible to the author.
- **qp091r (05:34 UTC):** Explicitly enumerated `126 - D^2/R = 125.25` as a "Wrong Lane Control" alongside other candidate corrections. The 125.25 PDG target was visible at this point.
- **qp091s (35 minutes later, same session):** Promoted the same `126 - D^2/R` expression from "Wrong Lane Control" to "Native / Reveal Surface". No new derivation between qp091r and qp091s; the form simply moved from candidate-to-reject to active-derivation.
- **qp091t (06:09 UTC):** Sealed `H_reveal = H_native - D^2/R` as active_derivation.

The structural identity H_native = R^2*(1-2^-D) = 126 GeV predates the value match (derives from substrate algebra primitives R, D, alpha_H alone, independent of any Higgs data). The -D^2/R correction is form-selected ex post against the visible target.

"EXACT" framing overstates by the structural-vs-form-selected gap. "Zero free parameters" overstates because the form of the correction was chosen with target visibility (a hidden degree of freedom in form-space even though no scalar parameter was fitted). "No H input" is technically true at the numeric level (the value 125.25 was not loaded as a constraint) but visibly false at the form-selection level.

## 4. What changed

- The verdict line in `CR120_result.md` is regraded from `CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY` to `CR120_QP091_CHAIN_INTAKE_BOUNDARY__HIGGS_125_25_PDG_MATCH__STRUCTURAL_NATIVE_126_PREDATES_VALUE__CORRECTION_FORM_IDENTIFIED_EX_POST__FORWARD_BLIND_PRECOMMIT_REQUIRED`.
- The `result_class` field in `CR120_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR120_summary.json` documenting the forensic chronology, preserved structural content, stripped language, and CR-136 ingest dependency.
- A header block is prepended to `CR120_result.md` explaining the disfavoring-vs-EXACT distinction.
- The historical declaration ("EXACT, derived from {R=12, D=3} alone with zero free parameters, no H input") is **preserved verbatim** in the original result.md text so the regrade is auditable rather than silent. The header block + new verdict line provide the corrected interpretation.

## 5. Restoration requirements (path back to PASS)

To restore CR-120 to PASS (genuine "EXACT" status), **all** of the following must hold:

1. Forward-blind precommit of the FORM `H = R^2*(1-2^-D) - D^2/R` BEFORE any future high-precision Higgs measurement (HL-LHC, FCC-ee, or successor). The form must be hash-sealed in a Courtroom CR with timestamp predating the measurement release.
   - *how to verify:* Reviewer reads the precommit CR's seal timestamp, confirms it predates the high-precision measurement's public release date, and confirms the form was sealed without further enumeration or modification.
2. Successful forward-blind contact with the future high-precision Higgs measurement: the precommitted formula's prediction must match the new measured value within the new measurement's uncertainty band.
   - *how to verify:* Reviewer reads the published high-precision measurement, computes the precommitted formula's prediction, and confirms the prediction lies within the measurement's stated uncertainty (e.g., 1 sigma).
3. Independent structural derivation of why the -D^2/R correction is the unique form among substrate-algebra candidates. Either (a) a derivation chain that arrives at -D^2/R without enumeration of alternatives, or (b) a complete enumeration of all substrate-algebra-grade two-term corrections showing only -D^2/R lands at the closed-loop saturation surface.
   - *how to verify:* Reviewer reads the structural derivation, confirms no step references the 125.25 numeric target, and confirms the chain arrives at -D^2/R from first principles or from an exhaustive enumeration.
4. Self-disclosure of the qp091r-s-t form-selection chronology in any future restoration CR. The chronology is part of the audit record and cannot be omitted.
   - *how to verify:* Reviewer confirms the restoration CR cites or reproduces the qp091r-s-t chronology in its scope or methodology section.


### 5a. Restoration falsifier

A future high-precision Higgs measurement (HL-LHC, FCC-ee, or successor) deviating from the precommitted H = R^2*(1-2^-D) - D^2/R prediction by more than the new measurement's stated uncertainty (e.g., 1 sigma) BLOCKS restoration. The current ~0.06% match to PDG is within current PDG uncertainty, but HL-LHC will tighten that uncertainty by a factor of ~10. Form survives only if it matches at the new precision.

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite the precommit CR's seal timestamp + the future high-precision Higgs measurement's release date as concrete forward-blind evidence
- Self-disclose the qp091r-s-t form-selection chronology (audit-record obligation; cannot be omitted)

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-120 record does NOT:

- Refute the H_native = R^2*(1-2^-D) = 126 GeV identity. The structural identity predates the value match and rests on substrate-algebra primitives.
- Refute the numerical match H = 125.25 GeV. The number is correct; the issue is HOW the form was selected.
- Modify CR-121 (gravity mechanism rides on the 7/8 + 1/8 split, which is independent of value-match strength), CR-122 (carrier-compression gate), or CR-119 (row enumeration; row-18 self-cancel).
- Touch the upstream qp091 chain. The qp091 chain is preserved as the historical declaration with its full chronology auditable.

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | UNKNOWN | result.md `5f8be2e5...ca235d2` / summary.json `2eca623b...2741388` | CR120 runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| qp_chain ingest | 2026-06-17 | ingest lock `2d6db0a6...55a4d2c` | CR-136 ingest |
| Replacement sealed | 2026-06-17 | result.md `11b12761...e5ca7f3` / summary.json `32a8a314...7687a82` | CR-140 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-120 finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR120.md`
- qp_chain ingest: `00_governance/CR136_QP_CHAIN_INGEST/CR136_result.md`
- Event README: `../EVENT_README.md`
- CR-140 result: `00_governance/CR140_CR120_HIGGS_CLAIM_REWORD/CR140_result.md`
