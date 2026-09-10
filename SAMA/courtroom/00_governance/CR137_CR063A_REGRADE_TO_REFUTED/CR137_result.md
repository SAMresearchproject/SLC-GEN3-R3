# CR137 CR-063a Verdict Regrade (SEALED → REFUTED) v1.0

## Verdict

```text
CR137_CR063A_REGRADE_TO_REFUTED_V1_SEALED
```

## Scope

CR-063a v1.0 hardware-translation claim was sealed as PASS on 2026-06-16. Its own pre-committed one-violation falsifier was empirically triggered at first contact with published transmon T2 data -- a factor of approximately 1932 overrun at 5 GHz. The rescue (CR-064a v1.1, A_0 enhancement + omega-as-gate-rate reinterpretation) introduces two new structural inputs and is audited separately as its own claim. Per the Courtroom protocol's own rules, a triggered one-violation falsifier whose fix requires new structural inputs REFUTES the original. CR-137 promotes CR-063a v1.0 to REFUTED on the record.

This regrade preserves the historical v1.0 declaration verbatim in CR-063a_result.md (formula, predictions, translation matrix, wrong controls) -- only the verdict line is changed, and an audit_regrade block is appended to its summary.json. The original is archived bit-identical with REPLACEMENT_RECORD documenting concrete restoration requirements and the restoration falsifier.

## Inputs

- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (`2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
- Target: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/`
- Surviving rescue claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`
- Source manifest: `CR137_source_manifest.csv`

## Empirical Falsification of v1.0

| Field | Value |
| --- | --- |
| Platform | IBM Heron / Eagle transmon (typical) |
| Gate omega | 3.1416e+07 rad/s |
| T2 observed | 100.0 microseconds |
| T2_grav v1.0 prediction | 51.8 ns |
| Overrun factor | ~= 1932x |
| v1.0 falsifier (literal) | *ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0.* |
| Source | CR064a published-T2 verification table (entry tagged [VERIFY_PRECOMMIT]) |

## Target Outcome

- **Status:** ALREADY_REGRADED
- **From verdict:** `CR063a_HARDWARE_TRANSLATION_V1_SEALED`
- **To verdict:** `CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1`
- **Current result_class:** `CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1`
- **Result.md SHA-256:** `c56e1bb2785eec8566d93104db960d49fac25e4bf8c15b11c09043b3a663fb04`
- **Summary.json SHA-256:** `6507324860144bc6a4369352793427e14511c55eb62bc3e053b1e64cc034ad63`
- **Archived original result.md SHA-256:** `710591fa467aae21f17aa121f3d629876a5fb35bbee632248d757ccbb2b52917`
- **Archived original summary.json SHA-256:** `1469b11fc76044a392ae51bf085e871770bbc19910df0a75dbc669123a3250b8`

## Predictions

- **[PASS]** P1_CR063a_target_exists — target dir = C:\VS\The_Courtroom\12a_QC_QN_CARRIER_COMPRESSION_REFRESH\CR063a_HARDWARE_TRANSLATION_V1
- **[PASS]** P2_archived_original_was_v1_0_SEALED — archived result_class = 'CR063a_HARDWARE_TRANSLATION_V1_SEALED'
- **[PASS]** P3_regrade_applied_or_already_applied — status = ALREADY_REGRADED
- **[PASS]** P4_post_regrade_result_class_is_REFUTED_string — current result_class = 'CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1'
- **[PASS]** P5_rescue_claim_CR064a_exists — CR-064a result.md exists = True
- **[PASS]** P6_restoration_requirements_documented — REPLACEMENT_RECORD.md includes section 5 with concrete restoration items + falsifier.

## Wrong Controls

- **[PASS]** WC1_archived_original_was_PASS — archived result_class = 'CR063a_HARDWARE_TRANSLATION_V1_SEALED'; expected 'CR063a_HARDWARE_TRANSLATION_V1_SEALED'
    - load-bearing deletion: If archived original had a different verdict (e.g. already REFUTED), the regrade would be operating on the wrong starting point; this WC would FAIL.
- **[PASS]** WC2_current_result_class_is_REFUTED — current result_class = 'CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1'; expected 'CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1'
    - load-bearing deletion: If the regrade did not update result_class (e.g. only the header was added), this WC would FAIL.
- **[PASS]** WC3_archived_originals_hash_match — Archived result.md and summary.json hash to the values recorded in original_sha256.txt.
    - load-bearing deletion: If either archived original were edited/corrupted, this WC would FAIL.
- **[PASS]** WC4_audit_regrade_block_well_formed_and_from_neq_to — audit_regrade present with correct from_verdict, to_verdict (distinct), driving_appeal_cr, driving_audit_verdict_sha256, and verdict_direction.
    - load-bearing deletion: If from_verdict == to_verdict (the bug class CR-141 WC8 catches), or if any required field were stripped, this WC would FAIL.
- **[PASS]** WC5_audit_verdict_reference_resolves — AUDIT_VERDICT exists=True; hash matches expected=2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
    - load-bearing deletion: If the audit verdict file were moved/edited, the recorded reference would be unverifiable; this WC would FAIL.
- **[PASS]** WC6_REPLACEMENT_RECORD_has_concrete_restoration_requirements — section=True; falsifier_subsection=True; concrete_items=True
    - load-bearing deletion: If restoration requirements were N/A, vague, or missing the falsifier subsection, this WC would FAIL. Downgraded verdicts MUST carry concrete restoration paths.
- **[PASS]** WC7_empirical_falsification_evidence_present — All 6 required trigger_evidence fields present in audit_regrade.
    - load-bearing deletion: If trigger_evidence were stripped (the regrade lacks evidentiary basis), this WC would FAIL.
- **[PASS]** WC8_surviving_rescue_claim_CR064a_resolves — CR-064a result.md exists = True; path = C:\VS\The_Courtroom\12a_QC_QN_CARRIER_COMPRESSION_REFRESH\CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1\CR064a_result.md
    - load-bearing deletion: If CR-064a (the surviving rescue claim) were missing, the regrade narrative would be incomplete; this WC would FAIL.

## Restoration Requirements (path back to PASS for CR-063a v1.0)

1. Original v1.0 formula T2_grav = 16*R^3/(17*omega) at A = 1 horizon condition (NOT the A_0 = 1/(pi*R) rescue) must agree with a measured T2 on at least one physical qubit platform under rigorous non-gravitational channel subtraction.
    - *how to verify:* Reviewer reads the measurement protocol, confirms the formula tested is literally 16*R^3/(17*omega), confirms the operating point is horizon (A=1) and NOT A_0, confirms subtraction protocol is reported transparently with all subtracted channels enumerated, and confirms the residual T2 equals T2_grav within experimental error.
2. The CR-064a v1.1 reinterpretation (omega as gate rate, A_0 scaling) MUST NOT be invoked. v1.0 stands or falls by its own declared formula and conditions.
    - *how to verify:* Reviewer confirms no part of the restoration argument uses omega_gate in place of qubit angular frequency, and confirms no A_0 enhancement factor is applied. Either substitution disqualifies the restoration.
3. The CR-064a published-T2 table must be re-verified against current literature (closing the [VERIFY_PRECOMMIT] open debt) with at least one entry matching v1.0's prediction (NOT v1.1's).
    - *how to verify:* Reviewer checks the verified-citation entries in CR-138 result, confirms at least one published T2 measurement equals the v1.0 T2_grav prediction within stated uncertainty at the cited gate angular frequency.

### Restoration Falsifier

A second platform measurement showing T2 > 10x * T2_grav_v1_0 at the relevant omega with channel subtraction, BLOCKS restoration. Given the existing approximately 1930x overrun on transmons, restoration is structurally implausible; this CR records that judgment rather than papering over it.

## CR-137 Falsifier (LOCKED)

Re-executing `CR137_runner.py` on the post-seal state MUST produce zero new `REGRADED` entries and zero new archive writes; the recomputed lock SHA-256 MUST match the value recorded here. Any deviation falsifies v1.0 of the regrade.

**Free parameters:** 0.

## Cryptographic Chain

```text
CR135_audit_verdict_sha256                = 2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661
CR137_source_manifest_csv                 = 2875c9253b158f03538838f2e53686f6a0d8ce0dd2549fa5c281cb44c1cf0710
CR137_regrade_manifest_csv                = 3a5578764edc6cec699495f843035780d6c6c7780ee3c7b036f090226ac5f96b
CR137_predictions_csv                     = dece65b6ec21605bbbacc2cb643dee3561e4a297e7ae2ce374ad202a1121c85d
CR137_wrong_controls_csv                  = 4be7fbc5dede5a69dd98548b62b4c668bece3a8b455daf35adb0646ebfd15474
CR137_regrade_lock_json                   = 34905be9be9d86036f5e7d1d0fc2828d61ae00f4ae4dec5d45459ce967a5cd9c
```

## Rule of Immutability

Verdict regrade, restoration requirements, restoration falsifier, and wrong controls are frozen at CR-137 seal time. Future falsification of CR-137 (failed idempotency, lock SHA mismatch on re-run) must be in an appeal CR within `00_governance/`.
