# CR138 CR-064a Verdict Regrade (SEALED -> BOUNDARY) v1.0

## Verdict

```text
CR138_CR064A_REGRADE_TO_BOUNDARY_V1_SEALED
```

## Scope

CR-064a v1.1 is the rescue claim that emerged after CR-063a v1.0 was empirically falsified (regraded to REFUTED per CR-137). The rescue introduced two new structural inputs (A_0 = 1/(pi*R) operating-point enhancement, omega reinterpreted as gate response rate) and was sealed with a 10-platform consistency table headlined '5 of 10 AT_THE_LIMIT, 0 violations'. The hostile audit identified three vulnerabilities in that seal that are not disclosed in the original result.md:

1. **Gate-rate artifact:** Quantinuum H1, IonQ Forte, and Delft NV cryo+DD share an IDENTICAL T2*omega product of 6.2832e4 -- three platforms reported as independent confirmations are one observation, not three.

2. **Citation debt:** All 10 published T2 citations are tagged [VERIFY_PRECOMMIT] (author's own placeholder for 'not yet independently verified against current literature').

3. **Wide bands + cushions:** The AT_THE_LIMIT classification is a factor-4 band, and the pre-committed falsifier requires a factor-10 cushion -- together absorbing a wide range of outcomes while reporting 'consistent'.

CR-138 regrades CR-064a v1.1 from PASS to BOUNDARY pending three concrete restoration requirements documented in the REPLACEMENT_RECORD. The formula T2_grav = 16*pi*R^4 / (17*omega_gate), the consistency table, predictions, and wrong controls are preserved verbatim as the historical v1.1 declaration; only the verdict line and the audit_regrade summary metadata are changed.

## Inputs

- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
- Target: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`
- Refuted prior claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/` (REFUTED per CR-137)
- Source manifest: `CR138_source_manifest.csv`

## The Gate-Rate Artifact (1.0248 cluster)

| Platform | T2 observed | gate omega | T2 * omega |
| --- | --- | --- | --- |
| Quantinuum H1 (171Yb+ clock states) | 10 s | 6.2832e3 rad/s | 6.2832e+04 |
| IonQ Forte (171Yb+) | 1 s | 6.2832e4 rad/s | 6.2832e+04 |
| Delft NV cryogenic + dynamical decoupling | 1 s | 6.2832e4 rad/s | 6.2832e+04 |

**Implication:** Three platforms reported as independent AT_THE_LIMIT confirmations are one observation, not three. The headline '5 of 10 platforms AT THE LIMIT' actually represents two distinct T2*omega measurements within the band (Stanford fluxonium at 3.13e4; the cluster at 6.28e4) plus the Innsbruck Ca+ point at 3.14e5. The 5/10 framing oversells the breadth of empirical support.

## Target Outcome

- **Status:** ALREADY_REGRADED
- **From verdict:** `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED`
- **To verdict:** `CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE`
- **Result.md SHA-256:** `c2eb68ad697640fec64237f010be4f1922bb975a2a70aa1be7c52f88338d7fd1`
- **Summary.json SHA-256:** `b3d119a35ee2ce8947cda14e176b59b1c8436f38730a5b73132fd4acb730a398`
- **Archived original result.md SHA-256:** `515a0925ccc96eee07c9877e06f5a040ee40fbdfa9d04c64496c07ab92410867`
- **Archived original summary.json SHA-256:** `27948045b36b52e63a4d5da58061597aaaa638f724cff2eb2951f4ade0bd10e4`

## Predictions

- **[PASS]** P1_CR064a_target_exists -- target dir = C:\VS\The_Courtroom\12a_QC_QN_CARRIER_COMPRESSION_REFRESH\CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1
- **[PASS]** P2_archived_original_was_v1_1_SEALED -- archived result_class = 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED'
- **[PASS]** P3_regrade_applied_or_already_applied -- status = ALREADY_REGRADED
- **[PASS]** P4_post_regrade_result_class_is_BOUNDARY_string -- current result_class = 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE'
- **[PASS]** P5_refuted_prior_CR063a_resolves_and_is_REFUTED -- CR-063a is in REFUTED state per CR-137 (precondition for CR-138's narrative)
- **[PASS]** P6_restoration_requirements_documented_with_concrete_items -- REPLACEMENT_RECORD names [VERIFY_PRECOMMIT] and 1.0248 explicitly in restoration items.

## Wrong Controls

- **[PASS]** WC1_archived_original_was_PASS -- archived result_class = 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED'; expected 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_SEALED'
    - load-bearing deletion: If archived original had a different verdict, the regrade would be operating on the wrong starting point.
- **[PASS]** WC2_current_result_class_is_BOUNDARY -- current result_class = 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE'; expected 'CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE'
    - load-bearing deletion: If result_class were not updated to the BOUNDARY string, this WC would FAIL.
- **[PASS]** WC3_archived_originals_hash_match -- Archived result.md and summary.json hash to the values recorded in original_sha256.txt.
    - load-bearing deletion: If either archived original were edited/corrupted, this WC would FAIL.
- **[PASS]** WC4_audit_regrade_block_well_formed_and_from_neq_to -- audit_regrade present with correct fields and from != to.
    - load-bearing deletion: If from_verdict == to_verdict, or required field stripped, this WC would FAIL.
- **[PASS]** WC5_audit_verdict_reference_resolves -- AUDIT_VERDICT exists=True; hash matches
    - load-bearing deletion: If audit verdict file moved/edited, the recorded reference would be unverifiable.
- **[PASS]** WC6_REPLACEMENT_RECORD_has_concrete_restoration_requirements -- section=True; falsifier_subsection=True; concrete_items_present=True
    - load-bearing deletion: If restoration requirements were N/A/vague/missing concrete items ([VERIFY_PRECOMMIT], 1.0248, AT_THE_LIMIT band), this WC would FAIL.
- **[PASS]** WC7_gate_rate_artifact_disclosed_in_audit_regrade -- audit_regrade.triggers.gate_rate_artifact contains 3 platforms at identical T2*omega = 6.2832e4
    - load-bearing deletion: If the 1.0248 artifact were not disclosed in the regrade record, the regrade would be cosmetic; this WC would FAIL.
- **[PASS]** WC8_refuted_prior_CR063a_in_REFUTED_state -- CR-063a result.md exists and contains REFUTED_BY_TRANSMON_T2_CONTACT marker (set by CR-137).
    - load-bearing deletion: If CR-137 had not run (CR-063a still PASS), CR-138's narrative (rescue of a refuted claim) would be inconsistent; this WC would FAIL.

## Restoration Requirements (path back to PASS for CR-064a v1.1)

1. All 10 [VERIFY_PRECOMMIT] citations in the consistency table MUST be independently verified against current published literature (post-Jan-2026 and current as of restoration date), with each measurement's T2_observed, operating omega_gate, and platform-class confirmed to a primary source.
    - *how to verify:* Reviewer reads the consistency table, follows each citation to its primary source (peer-reviewed paper, manufacturer published spec, conference talk with archived slides), confirms T2 value and gate rate within stated uncertainty. Open verification log accompanies the restoration CR.
2. The 1.0248 gate-rate artifact MUST be disclosed in the result.md and either (a) explained as a structural prediction (e.g., three platforms land at the same T2*omega for a substrate-derived reason that does NOT depend on choosing platforms with that ratio), OR (b) demonstrated to be broken by adding non-1.0248 platforms within the AT_THE_LIMIT band.
    - *how to verify:* Reviewer reads the result.md, confirms the artifact is named (not implicit), and confirms either a structural prediction is offered with reasoning, or additional non-1.0248 platforms are added with verified citations. Silent omission disqualifies restoration.
3. At least three independent platform measurements at distinct T2*omega products (not in the 1.0248 cluster) MUST sit within the AT_THE_LIMIT band, OR the AT_THE_LIMIT band MUST be narrowed from factor-4 to a band defensible by the spread of verified measurements.
    - *how to verify:* Reviewer counts distinct T2*omega products in the AT_THE_LIMIT band post-verification, confirms count >= 3 OR confirms the new band width is justified explicitly by the empirical spread (e.g., 1-sigma weighted by experimental uncertainties on each citation).
4. The trapped-ion plateau prediction (T2 ceiling ~10 s at kHz gate rates) MUST be re-evaluated against current Quantinuum / IonQ specifications. If those specifications have moved past the prediction by more than the AT_THE_LIMIT band width, the plateau prediction is itself falsified and blocks restoration.
    - *how to verify:* Reviewer checks Quantinuum H1, H2, IonQ Forte/Tempo published T2 specs current to restoration date; confirms 10 s ceiling holds within the AT_THE_LIMIT band at the cited gate rate. If T2 > 100 s at the same gate rate without compensating new structural inputs, restoration blocked.

### Restoration Falsifier

Any platform measurement (independent of the 10 currently in the table) clean-exceeding T2_grav_v1_1 = 16*pi*R^4/(17*omega_gate) by a factor of 10 or more at its operating omega_gate, with non-gravitational channels rigorously subtracted, falsifies CR-064a v1.1 entirely (not just blocks restoration). Such a result would trigger an appeal CR (CR-064b) with its own v1.2 formulation or formal refutation, following the same protocol that converted CR-063a v1.0 to REFUTED.

## CR-138 Falsifier (LOCKED)

Re-executing `CR138_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match the value recorded here.

**Free parameters:** 0.

## Cryptographic Chain

```text
CR135_audit_verdict_sha256                = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
CR138_source_manifest_csv                 = e69a696da08ac4bcba699e8dd09a06102870f1220a6b97e0cef027c454081244
CR138_regrade_manifest_csv                = da09296252dd7048e2e0c13c2459957c4205d1a0981594321076b5f415fdc28e
CR138_predictions_csv                     = 8f6e23cf86b8a0e02799694e49e611aa0a4e3e5f6bad7ccc05ec982a197f2a38
CR138_wrong_controls_csv                  = 28076700d4d1bae55373413fc318516b69c4f56cc243696b540eef0c2cdbe84e
CR138_regrade_lock_json                   = 0536cccdf7a2b45cafee3002d576f99d1a4f2b399a9e6cc9858297883972d69e
```

## Rule of Immutability

Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-138 seal time. Future falsification must be in an appeal CR.
