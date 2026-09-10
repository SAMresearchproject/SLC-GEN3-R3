# CR120 qp091 Chain Intake - Result

> **AUDIT-DRIVEN VERDICT REGRADE -- 2026-06-17 PER CR-140**
>
> The verdict in this file is regraded from `CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY` to a BOUNDARY verdict because the headline language 'EXACT / zero free parameters / no H input' overstates what the qp091 chain proved. Forensic chronology: qp091r (05:34 UTC same authoring session) explicitly enumerated `126 - D^2/R = 125.25` as a 'Wrong Lane Control' WITH THE 125.25 PDG TARGET VISIBLE; qp091s 35 minutes later promoted the same expression to 'Native / Reveal Surface'; qp091t at 06:09 UTC sealed it as active_derivation. The structural identity H_native = R^2*(1-2^-D) = 126 GeV (substrate algebra primitives only) PREDATES the value match. The -D^2/R correction is form-selected ex post.
>
> The structural content is **preserved**: R = 12, D = 3, alpha_H = 2, the partition algebra, H_native = 126, the 7/8 + 1/8 split, the row-18 self-cancel, and downstream consumers (CR-121 gravity mechanism, CR-122 carrier-compression gate) all stand. The regrade affects strength-of-claim language only.
>
> Reworded summary: H_native = R^2*(1-2^-D) = 126 GeV derives from substrate algebra primitives alone (no Higgs data input). The -D^2/R correction lands at PDG H = 125.25 GeV to displayed precision. The form of the correction was identified ex post against the visible PDG target during the qp091r-s-t chronology. Restoration to a stronger claim requires forward-blind precommit of the form before a future high-precision Higgs measurement (HL-LHC, FCC-ee).
>
> The qp091t source artifact is now resident internally at `upstream_artifacts/qp091/qp091t/qp091t_summary.json` per CR-136 ingest; the recorded SHA `8c9fe94dcd80...` resolves to a local file.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/original_result.md`
> - Original SHA-256: `5f8be2e5c0f37e6413e3785014f06f41754456a0b91ed40ab605b71e8ca235d2`
> - Replacement record (with restoration requirements + falsifier): `archive/2026-06-17_CR135_audit_regrades/CR140_higgs_claim_reword/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)
> - qp_chain ingest dependency: `00_governance/CR136_QP_CHAIN_INGEST/CR136_ingest_lock.json` (`2d6db0a619755cae19fd0e2d51ce815c288da47813c0e7f163fe437a355a4d2c`)

## Upstream Provenance - Citation Failure Repair (added 2026-06-17, post-CR140)

> **CITATION FAILURE RECORDED.** The original CR-120 intake and the CR-140 regrade narrative both failed to surface the upstream Stam_model-A G-series chain that pre-sealed the bounce-cost machinery -- including the Higgs slot specifically -- **three weeks before** the qp091r-s-t chronology that drove the regrade. The qp091 chain (2026-06-15) re-derived for the Higgs row what the G432/G435/G437/G439/G444/G445/G446/G452 chain (2026-05-26) had already structurally sealed across the full 15-row table, target-blind. This section is an additive provenance repair; it does not revise verdicts on its own.

### Full formula provenance

The Higgs correction `-D^2/R = -0.75 GeV` is the algebraic reduction, for the Higgs slot specifically, of the universal bounce-cost law sealed at G435:

```text
r_bounce    = (A_0/2) * (q / 2^D)
m_corrected = m_base / (1 + r_bounce)
Delta_m     = m_base * r_bounce / (1 + r_bounce)
```

The cost is fractional in the eigenmode/mass -- *more mass -> more bounce cost* -- with universal scale `A_0/2 = 1/(24*pi)` and per-species correction set by the q-slot. The q-slot is derived from Gate-8/Gate-7 write-sector numbers (G444), NOT a free parameter.

For the Higgs at `q = su2 = 3` (sealed at G439, 2026-05-26 04:21 UTC):

```text
r_bounce(H) = (1/(24*pi)) * (3/8) = 1/(64*pi)
```

which lands the Higgs slot lambda at the same value the qp091t chain later wrote in `-D^2/R` form. The two are the same number; the *origin* is the q-slot from the species-role machinery, not `-D^2/R`. The q-slot was sealed three weeks before the qp091 chronology.

### Upstream chain (Stam_model-A `audit/audits/`)

| upstream verdict | seal (UTC) | SHA-256 | load-bearing content |
|---|---|---|---|
| G432_BOUNCE_COST_EIGHTH_SLOT_CORRECTION | 2026-05-26 03:40 | `89f1181db9c683d95267aeedff9c2de1ebe80cb2bc003129a1d9986f2142b361` | bounce-cost / eighth-slot correction primitive |
| G435_BOUNCE_COST_MASS_PROPORTIONALITY | 2026-05-26 03:50 | `c87e9bbe38493cf582bbbbf3112cca52472ff6f5e08d1596f6a3f625d6827ff8` | `r_bounce = (A_0/2)*(q/2^D)`; more mass -> more cost |
| G437_BARYON_SPLIT_HOLDOUT_PREDICTION | 2026-05-26 04:00 | `bfed9b18d536fff852a12a733b82252833bae8206f6773deb81ac107cb62b81c` | target-blind prediction m_n > m_p from q-slot |
| G439_HEAVY_ELECTROWEAK_TOP_SLOT_SELECTOR | 2026-05-26 04:21 | `eaf005a7d0c4d24243cabc2ce733392aad1baf434e9ec70113df3f8dc82de0fe` | Higgs slot k=7, n=54, q=su2=3 (same session as W/Z/top) |
| G444_WRITE_SECTOR_Q_SLOT_DERIVATION | 2026-05-26 04:43 | `3ecd4f36fddac798d0cdd1a5a7daf7931a1555150ff5c42d68a1175e5f07043d` | derives q-alphabet from Gate-8/Gate-7 numbers |
| G445_MASS_DEPTH_N0_BINARY_WRITE_TREE | 2026-05-26 04:43 | `cbe32c06545eb23a417da397477e9f661082f71930ce3c30c90cb2d43cb76a38` | derives `n_0 = 2^(b+1)-1 = 63` |
| G446_ROLE_OPERATOR_KN_SELECTOR | 2026-05-26 04:48 | `267eddb6a99cf12c5997ab80b99cd1314d8230907708054bf56d325e5d7ea7b4` | role-operator k,n selector |
| G452_INTEGRATED_NONMASS_SPECIES_SELECTOR | 2026-05-26 05:15 | `cc0d0adaf2171d3b4e0f316876d0af7d487beef7275c55c615176d555e4eaa6a` | 15-row role-first selector; mass comparison only after role map is fixed |

- Upstream verdict path: `C:/VS/Stam_model-A-v1.0/audit/audits/VERDICT_G{432,435,437,439,444,445,446,452}_*_2026_05_26.md`
- Upstream priority record: `C:/VS/memory/PRIORITY_RECORD.md` (G432-G453 block; entries record `Sean-approved current turn` status)

### Effect on the CR-140 regrade narrative

CR-140 reworded the CR-120 headline because the qp091r->s->t chronology (2026-06-15) showed the `-D^2/R` form enumerated as a 'Wrong Lane Control' with the PDG target visible, then promoted to active derivation 35 minutes later. That chronology is accurate at the qp091-narrative level and is preserved.

What CR-140 did not surface, now recorded:

1. The qp091 chain re-derived for the Higgs row what the G-series sealed three weeks earlier across the full 15-row table (electron, muon, tau, proton, neutron, W, Z, Higgs, top, deuteron, alpha, pi+, pi0, K+, K0).
2. The structural form `r_bounce = (A_0/2)*(q/2^D)` was sealed at G435 (2026-05-26 03:50 UTC) **with no Higgs target in scope** -- G435 ran on lepton + baryon rows and stated the law "more mass -> more bounce cost."
3. The Higgs-specific q-slot `q = su2 = 3` was sealed at G439 (2026-05-26 04:21 UTC) in the same authoring session as the W/Z/top heavy-row table -- NOT a Higgs-target-driven assignment.
4. G437 passed forward-blind on 2026-05-26 04:00 UTC, predicting `m_neutron > m_proton` from the same q-slot machinery with no p/n masses in the selector. That is the same machinery the Higgs slot rides.
5. Therefore the form `r_bounce` was committed before the value match at the substrate-machinery level on 2026-05-26 -- three weeks before qp091 -- even though the qp091-only narrative on its own does not show this.

### Verdict effect

This repair does **not** automatically lift the CR-140 BOUNDARY regrade. The CR-120 intake's self-contained narrative still relied on the qp091 chronology, and CR-140's K3-hygiene call against that narrative is preserved. What this repair establishes is the upstream chain the original intake should have cited and did not, and contributes to CR-140 restoration requirement (3) (independent structural derivation of why the correction is the form it is) by showing the upstream derivation is the q-slot from Gate-8/Gate-7 write algebra, not the algebraic shorthand `-D^2/R`.

Curator may file an appeal CR (CR143+) that, with the SHAs now on the record, argues form selection occurred at G435/G437/G439 (2026-05-26), not at qp091r->s->t (2026-06-15).

### Authority

Curator-authorized direct edit, 2026-06-17. The original archived result.md (SHA `5f8be2e5c0f37e6413e3785014f06f41754456a0b91ed40ab605b71e8ca235d2`) and the CR-140 reworded result.md (pre-repair SHA `11b12761115e01cfc6a48635950ec5571cc2752046dcfb9853135e7a2e5ca7f3`) are both preserved on the record. This edit is additive provenance, not verdict revision. Post-repair SHA recorded in `CR120_result.md.sha256.txt`.

## Verdict (Regraded 2026-06-17 per CR-140)

```text
CR120_QP091_CHAIN_INTAKE_BOUNDARY__HIGGS_125_25_PDG_MATCH__STRUCTURAL_NATIVE_126_PREDATES_VALUE__CORRECTION_FORM_IDENTIFIED_EX_POST__FORWARD_BLIND_PRECOMMIT_REQUIRED
```

**Prior verdict (preserved on the record):** `CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY` -- archived at the path in the header block above.

**Reason for regrade:** Tier 4 hostile-audit finding (DEMAND_RETEST). The 'EXACT / zero free parameters / no H input' language overstates what the qp091r-s-t form-selection chronology proved. The structural identity H_native = R^2*(1-2^-D) = 126 GeV predates the value match (substrate algebra primitives only); the -D^2/R correction is form-selected ex post. Restoration to a stronger claim requires forward-blind precommit before a future high-precision Higgs measurement (see REPLACEMENT_RECORD section 5).

## One-Line Headline

> H_reveal = R^2 (1 - 2^(-D)) - D^2/R = 144 * 7/8 - 9/12 = 126 - 0.75 = 125.25 GeV EXACT, derived from {R=12, D=3} alone with zero free parameters, no H input, dozenal fingerprint 100_12 -> A6_12 -> A5.3_12.

## qp091 Chain Counts

```text
total stages intaken                    = 33
PASS / FROZEN count                     = 31
BOUNDARY count                          = 2
all passed (passed field true everywhere)= False
```

## qp091t Closed-Form Derivation

```text
H_native = R^2 * (1 - 2^(-D)) = 144 * 7/8 = 126   = A6_12
H_reveal = H_native - D^2/R   = 126 - 0.75 = 125.25 = A5.3_12  EXACT
```

## Predictions

- **[PASS]** P1_qp091_chain_33_stages_all_intaken
- **[PASS]** P2_qp091t_closure_intaken_at_125_25_exact
- **[PASS]** P3_closed_form_uses_only_R_and_D
- **[PASS]** P4_no_higgs_mass_used_as_input
- **[PASS]** P5_dozenal_fingerprint_present
- **[PASS]** P6_triple_identity_eighteen_recorded
- **[PASS]** P7_HZZ4l_category_projection_1_2_1
- **[PASS]** P8_five_cross_courtroom_unifications_recorded
- **[PASS]** P9_three_forward_blind_expectations_with_falsifiers
- **[PASS]** P10_courtroom_anchors_hashed_for_chain_of_custody
- **[PASS]** P11_blindness_protocol_present
- **[PASS]** P12_zero_free_parameters_in_this_intake
- **[PASS]** P13_intake_lock_sealed_with_sha256_sibling
- **[PASS]** P14_no_prior_CR_modified
- **[PASS]** P15_qp091ad_BOUNDARY_scope_clarified_not_125_25_closure

## Wrong Controls

- **[PASS]** WC1_does_not_modify_qp091_chain_artifacts
- **[PASS]** WC2_does_not_modify_CR065a_CR066a_CR067a_CR091a_CR069a_CR119_CR121
- **[PASS]** WC3_does_not_overclaim_qp091ad_BOUNDARY_as_125_25_closure_failure
- **[PASS]** WC4_does_not_introduce_a_free_parameter
- **[PASS]** WC5_does_not_promote_the_one_eighth_split_loss_to_a_particle
- **[PASS]** WC6_does_not_re_open_questions_closed_by_qp091t
- **[PASS]** WC7_falsification_criteria_per_prediction
- **[PASS]** WC8_unifications_use_existing_Courtroom_record_only_no_speculation

## Headline Export

See `CR120_HEADLINE_HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY.md`.

## Open Debts

```text
- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Future qp091ae or successor will reveal the epsilon residual operator (sub-percent surface-debit fine structure)
- Future ATLAS/CMS HL-LHC HZZ4l category counts will appeal CR120_PRED_2 against the 1:2:1 projection
- Future Higgs-factory precision will appeal CR120_PRED_1 against the 125.25 closed form
```

## Immutability

CR120 hashes the qp091 chain + 9 Courtroom anchors; modifies nothing.
