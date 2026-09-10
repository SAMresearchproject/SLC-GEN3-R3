# REPLACEMENT_RECORD — CR-063a verdict regrade (SEALED → REFUTED)

## 1. Replaced artifact

| Field | Value |
| --- | --- |
| Original path | `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR063a_HARDWARE_TRANSLATION_V1/CR063a_result.md` and `CR063a_summary.json` |
| Original result.md SHA-256 | `710591fa467aae21f17aa121f3d629876a5fb35bbee632248d757ccbb2b52917` |
| Original summary.json SHA-256 | `1469b11fc76044a392ae51bf085e871770bbc19910df0a75dbc669123a3250b8` |
| Original verdict | `CR063a_HARDWARE_TRANSLATION_V1_SEALED` |
| Replacement path | (identical to original) |
| Replacement result.md SHA-256 | `c56e1bb2785eec8566d93104db960d49fac25e4bf8c15b11c09043b3a663fb04` |
| Replacement summary.json SHA-256 | `6507324860144bc6a4369352793427e14511c55eb62bc3e053b1e64cc034ad63` |
| Replacement verdict | `CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1` |
| Verdict direction | `DOWNGRADED` |

## 2. Driving event

| Field | Value |
| --- | --- |
| Audit / appeal CR | CR-137 CR-063a verdict regrade |
| Audit verdict SHA-256 | `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661` |
| Date | 2026-06-17 |
| Criterion failed | `C6 VERDICT_GRADE_MATCHES_EVIDENCE` (PASS verdict held despite triggered one-violation falsifier) |
| Audit finding tier | `Tier 7 CALLOUT_FAIL_DRESSED_AS_PASS` |

## 3. Defect summary

CR-063a v1.0 was sealed with PASS status (`CR063a_HARDWARE_TRANSLATION_V1_SEALED`) on 2026-06-16T01:22:35Z. Its pre-committed one-violation falsifier (`CR063a_PRED_1`) stated: *"ONE rigorously-isolated T2 measurement on any platform exceeding T2_grav (after channel subtraction) falsifies v1.0."*

At first comparison with published literature (CR-064a, 2026-06-16, same author session), an IBM Heron / Eagle transmon T2 of ~= 100 microseconds at gate omega ~= pi * 1e7 rad/s was identified. The v1.0 prediction at the same omega is T2_grav = 1626.35 / omega ~= 51.8 ns. The observed T2 exceeds the v1.0 prediction by a factor of approximately **1932** -- five orders of magnitude beyond any plausible non-gravitational channel attribution. The falsifier was triggered.

The response in CR-064a was not to record falsification but to introduce a rescue v1.1 with two new structural inputs (A_0 = 1/(pi*R) operating-point enhancement, omega reinterpreted as substrate gate response rate rather than qubit angular frequency), and to leave CR-063a v1.0 sealed at the original horizon (A = 1) reading per CR-064a's own WC3. This is the Courtroom protocol weaponized against itself: a triggered one-violation falsifier whose verdict was preserved by routing the rescue through a sibling CR.

CR-137 promotes CR-063a v1.0 to REFUTED per the protocol's own rules.

## 4. What changed

- The verdict line in `CR063a_result.md` is regraded from `CR063a_HARDWARE_TRANSLATION_V1_SEALED` to `CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1`.
- The `result_class` field in `CR063a_summary.json` is updated to match.
- An `audit_regrade` object is prepended to `CR063a_summary.json` documenting the regrade chain and trigger evidence.
- A header block is prepended to `CR063a_result.md` linking to this archive entry.
- The formula, predictions, wrong controls, and translation matrix are **preserved verbatim** as the historical v1.0 declaration. The regrade affects only the verdict line.

## 5. Restoration requirements (path back to PASS)

To restore CR-063a v1.0 to PASS, **all** of the following must hold:

1. Original v1.0 formula T2_grav = 16*R^3/(17*omega) at A = 1 horizon condition (NOT the A_0 = 1/(pi*R) rescue) must agree with a measured T2 on at least one physical qubit platform under rigorous non-gravitational channel subtraction.
   - *how to verify:* Reviewer reads the measurement protocol, confirms the formula tested is literally 16*R^3/(17*omega), confirms the operating point is horizon (A=1) and NOT A_0, confirms subtraction protocol is reported transparently with all subtracted channels enumerated, and confirms the residual T2 equals T2_grav within experimental error.
2. The CR-064a v1.1 reinterpretation (omega as gate rate, A_0 scaling) MUST NOT be invoked. v1.0 stands or falls by its own declared formula and conditions.
   - *how to verify:* Reviewer confirms no part of the restoration argument uses omega_gate in place of qubit angular frequency, and confirms no A_0 enhancement factor is applied. Either substitution disqualifies the restoration.
3. The CR-064a published-T2 table must be re-verified against current literature (closing the [VERIFY_PRECOMMIT] open debt) with at least one entry matching v1.0's prediction (NOT v1.1's).
   - *how to verify:* Reviewer checks the verified-citation entries in CR-138 result, confirms at least one published T2 measurement equals the v1.0 T2_grav prediction within stated uncertainty at the cited gate angular frequency.


### 5a. Restoration falsifier

A second platform measurement showing T2 > 10x * T2_grav_v1_0 at the relevant omega with channel subtraction, BLOCKS restoration. Given the existing approximately 1930x overrun on transmons, restoration is structurally implausible; this CR records that judgment rather than papering over it.

### 5b. Restoration CR forward-link

When restoration is attempted, the new CR must:

- Reference this REPLACEMENT_RECORD by archive path and SHA-256
- Open a new archive entry for the restoration event (this file does not get rewritten; a NEW record is added)
- Not delete the present REFUTED state; if restoration succeeds, the present artifact is in turn archived under the restoration CR's date
- Cite an independent published T2 measurement (NOT one already in CR-064a's [VERIFY_PRECOMMIT]-tagged table) at the v1.0 horizon-condition formula

## 6. What this artifact still does NOT do (post-regrade)

The REFUTED CR-063a v1.0 record does NOT:

- Claim CR-064a v1.1 is also refuted — that is a distinct claim, audited separately in CR-138.
- Claim the underlying gravity-mechanism (CR-121) is refuted — CR-121's 1/8 + qA mechanism survives independently.
- Claim no SAM-native qubit can ever achieve T2_grav-limited operation — only that the specific v1.0 formula at horizon condition is contradicted by transmon contact.
- Repair any self-hash defect in CR-063a (separate concern; this CR focuses on the verdict regrade only).

## 7. Chain of custody

| Stage | Date | Hash | Actor |
| --- | --- | --- | --- |
| Original sealed | 2026-06-16T01:22:35Z | result.md `710591fa...2b52917` / summary.json `1469b11f...a3250b8` | CR063a runner |
| Audit finding | 2026-06-17 | audit verdict `2fe572d5...3b40661` | CR-135 hostile audit |
| Replacement sealed | 2026-06-17 | result.md `c56e1bb2...663fb04` / summary.json `65073248...034ad63` | CR-137 runner |
| Curator sign-off | PENDING | — | Sean Brady |

## 8. Cross-references

- Audit criteria: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_CRITERIA.md`
- Audit verdict: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md`
- CR-063a finding: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/findings_per_cr/AUDIT_CR063a_HARDWARE_TRANSLATION_V1.md`
- Surviving rescue claim: `12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1/`
- Event README: `../EVENT_README.md`
- CR-137 result: `00_governance/CR137_CR063A_REGRADE_TO_REFUTED/CR137_result.md`
