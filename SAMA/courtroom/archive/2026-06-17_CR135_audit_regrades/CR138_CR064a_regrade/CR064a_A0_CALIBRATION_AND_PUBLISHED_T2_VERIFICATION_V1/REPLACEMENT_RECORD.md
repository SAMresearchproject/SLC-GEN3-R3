# REPLACEMENT_RECORD -- CR-064a verdict regrade (SEALED -> BOUNDARY)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/CR064a_result.md` and `CR064a_summary.json` |
| Original result.md SHA-256 | `515a0925ccc96eee07c9877e06f5a040ee40fbdfa9d04c64496c07ab92410867` |
| Original summary.json SHA-256 | `27948045b36b52e63a4d5da58061597aaaa638f724cff2eb2951f4ade0bd10e4` |
| Original verdict | `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `c2eb68ad697640fec64237f010be4f1922bb975a2a70aa1be7c52f88338d7fd1` |
| Replacement summary.json SHA-256 | `b3d119a35ee2ce8947cda14e176b59b1c8436f38730a5b73132fd4acb730a398` |
| Replacement verdict | `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE` |
| Verdict direction | `DOWNGRADED` |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-138 CR-064a verdict regrade |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (PASS held despite gate-rate artifact + unverified citations) |
| Audit finding tier | `Tier 3 REGRADE_TO_BOUNDARY` |

## 3. Defect summary

CR-064a v1.1 was sealed with PASS (`CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED`) on 2026-06-16. The seal rested on a 10-platform consistency table whose headline was "5 AT_THE_LIMIT, 0 violations". The hostile audit identified three vulnerabilities not disclosed in the result.md:

### Gate-rate artifact (1.0248 cluster)

Three of the five AT_THE_LIMIT systems share an IDENTICAL T2 * omega product of 6.2832e4:

| Platform | T2 observed | gate omega | T2 * omega |
| --- | --- | --- | --- |
| Quantinuum H1 (171Yb+ clock states) | 10 s | 6.2832e3 rad/s | 6.2832e+04 |
| IonQ Forte (171Yb+) | 1 s | 6.2832e4 rad/s | 6.2832e+04 |
| Delft NV cryogenic + dynamical decoupling | 1 s | 6.2832e4 rad/s | 6.2832e+04 |

These three platforms are reported as independent confirmations of the T2_grav_v1_1 formula at the AT_THE_LIMIT band. They are not three independent confirmations. They are three platforms with identical T2*omega products -- a *cluster*, not a confirmation count.

### Citation debt

All 10 published T2 measurements in the consistency table are tagged `[VERIFY_PRECOMMIT]`, the author's own marker indicating the value has not been independently verified against current literature post Jan-2026 training cutoff. The seal stands on inputs the author has not yet checked.

### Band and falsifier cushions

The AT_THE_LIMIT classification is a factor-4 band (T2_observed / T2_grav between 0.5 and 2.0). The pre-committed falsifier requires a factor-10 cushion (T2 > 10x T2_grav). These cushions together absorb a wide range of empirical outcomes while still reporting "consistent". The result.md does not display these bandwidths at the headline level.

## 4. What changed

- The verdict line in `CR064a_result.md` is regraded from `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED` to `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE`.
- The `result_class` field in `CR064a_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR064a_summary.json` documenting all three triggers (gate-rate artifact, citation debt, band/cushion).
- A header block is prepended to `CR064a_result.md` linking to this archive entry and disclosing the gate-rate artifact at the top of the file.
- The formula, consistency table, predictions, and wrong controls are **preserved verbatim** as the historical v1.1 declaration. The regrade affects only the verdict line.

## 5. Restoration requirements (path back to PASS)

To restore CR-064a v1.1 to PASS, **all** of the following must hold:

1. All 10 [VERIFY_PRECOMMIT] citations in the consistency table MUST be independently verified against current published literature (post-Jan-2026 and current as of restoration date), with each measurement's T2_observed, operating omega_gate, and platform-class confirmed to a primary source.
   - *how to verify:* Reviewer reads the consistency table, follows each citation to its primary source (peer-reviewed paper, manufacturer published spec, conference talk with archived slides), confirms T2 value and gate rate within stated uncertainty. Open verification log accompanies the restoration CR.
2. The 1.0248 gate-rate artifact MUST be disclosed in the result.md and either (a) explained as a structural prediction (e.g., three platforms land at the same T2*omega for a substrate-derived reason that does NOT depend on choosing platforms with that ratio), OR (b) demonstrated to be broken by adding non-1.0248 platforms within the AT_THE_LIMIT band.
   - *how to verify:* Reviewer reads the result.md, confirms the artifact is named (not implicit), and confirms either a structural prediction is offered with reasoning, or additional non-1.0248 platforms are added with verified citations. Silent omission disqualifies restoration.
3. At least three independent platform measurements at distinct T2*omega products (not in the 1.0248 cluster) MUST sit within the AT_THE_LIMIT band, OR the AT_THE_LIMIT band MUST be narrowed from factor-4 to a band defensible by the spread of verified measurements.
   - *how to verify:* Reviewer counts distinct T2*omega products in the AT_THE_LIMIT band post-verification, confirms count >= 3 OR confirms the new band width is justified explicitly by the empirical spread (e.g., 1-sigma weighted by experimental uncertainties on each citation).
4. The trapped-ion plateau prediction (T2 ceiling ~10 s at kHz gate rates) MUST be re-evaluated against current Quantinuum / IonQ specifications. If those specifications have moved past the prediction by more than the AT_THE_LIMIT band width, the plateau prediction is itself falsified and blocks restoration.
   - *how to verify:* Reviewer checks Quantinuum H1, H2, IonQ Forte/Tempo published T2 specs current to restoration date; confirms 10 s ceiling holds within the AT_THE_LIMIT band at the cited gate rate. If T2 > 100 s at the same gate rate without compensating new structural inputs, restoration blocked.


### 5a. Restoration falsifier

Any platform measurement (independent of the 10 currently in the table) clean-exceeding T2_grav_v1_1 = 16*pi*R^4/(17*omega_gate) by a factor of 10 or more at its operating omega_gate, with non-gravitational channels rigorously subtracted, falsifies CR-064a v1.1 entirely (not just blocks restoration). Such a result would trigger an appeal CR (CR-064b) with its own v1.2 formulation or formal refutation, following the same protocol that converted CR-063a v1.0 to REFUTED.

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event
- Not delete the present BOUNDARY state; if restoration succeeds, the present artifact is in turn archived
- Cite at least three independent verified platform measurements at distinct T2*omega products, OR document the structural reason three platforms cluster at 1.0248

## 6. What this artifact still does NOT do (post-regrade)

The BOUNDARY CR-064a v1.1 record does NOT:

- Claim the formula T2_grav = 16*pi*R^4 / (17*omega_gate) is itself wrong -- the issue is evidentiary discipline, not refutation.
- Refute the underlying gravity-mechanism (CR-121) or carrier-compression gate (CR-122).
- Claim the trapped-ion plateau prediction is false -- it is held open pending verified spec re-evaluation.
- Repair any self-hash defect in CR-064a (separate concern; this CR focuses on verdict regrade only).

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T01:45:29Z | result.md `515a0925...2410867` / summary.json `27948045...0bd10e4` | CR064a runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `c2eb68ad...38d7fd1` / summary.json `b3d119a3...730a398` | CR-138 runner |
| Curator sign-off | PENDING | -- | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-064a finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1.md`
- Refuted prior claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/` (REFUTED per CR-137)
- Event README: `../EVENT_README.md`
- CR-138 result: `00_governance/CR138_CR064A_REGRADE_TO_BOUNDARY/CR138_result.md`
