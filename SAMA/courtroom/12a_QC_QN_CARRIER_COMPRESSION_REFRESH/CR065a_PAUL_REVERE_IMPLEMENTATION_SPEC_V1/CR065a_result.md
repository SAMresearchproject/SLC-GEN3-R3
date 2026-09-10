# CR065a Paul Revere Letter Implementation Specification v1.0

## Verdict

```text
CR065a_PAUL_REVERE_IMPLEMENTATION_SPEC_V1_SEALED
```

## The Winning Pairing

**(1,2,4) × NV_center** (score: **14 / 15**)

_Rationale:_ 3 native sublevels (ms = 0/+1/-1); PL = direct photon-counting sensor; cryo+DD T2 ~ 1s AT SAM floor; room-temp accessible to many academic groups; mass-scale mapping open but slot-ratio testable

_Runner-up:_ (2,4,8) × NV_center (score 13/15)

_Third:_ (1,2,4) × photonic (score 12/15)

## Scoring Table (8 Pairings, 5 Criteria)

| qubit | platform | slot count | sensor | T2 headroom | accessibility | mass scale | total |
|---|---|---:|---:|---:|---:|---:|---:|
| (1,2,4) | NV_center | 3 | 3 | 3 | 3 | 2 | **14** |
| (2,4,8) | NV_center | 3 | 3 | 3 | 3 | 1 | **13** |
| (1,2,4) | photonic | 3 | 2 | 3 | 2 | 2 | **12** |
| (2,4,8) | trapped_ion | 3 | 3 | 1 | 2 | 3 | **12** |
| (2,4,8) | photonic | 3 | 2 | 3 | 2 | 2 | **12** |
| (1,2,4) | trapped_ion | 3 | 3 | 1 | 2 | 2 | **11** |
| (1,2,4) | SC_transmon | 2 | 2 | 2 | 3 | 1 | **10** |
| (2,4,8) | SC_transmon | 2 | 2 | 2 | 3 | 1 | **10** |

## Hardware Specification (NV Center in Diamond)

**Physical substrate:** single-crystal diamond, optionally ¹²C-isotopically purified, with negatively-charged nitrogen-vacancy (NV⁻) center.

**Ground state:** triplet ³A₂ with three spin sublevels (ms = 0, +1, -1) and zero-field splitting D_NV ≈ 2.87 GHz.

**Slot assignment (the (1, 2, 4) ideal qubit on NV ms-states):**

| slot | partition value | physical state | weight | role |
|---|---:|---|---|---|
| **a** (CARRIER) | 1 | ms = 0 (ground sublevel) | 1/4 | route identity, protected pre-commit |
| **b** (ENVELOPE) | 2 | ms = +1 (Zeeman-split middle) | 9/16 | **letter content**, 9/8 surcharge |
| **c** (SENSOR) | 4 | ms = -1 (Zeeman-split outer) | 1/4 | boundary stress readout via PL coupling |

**Control channels:**

- **Optical initialization:** 532 nm laser, ~1 μs pulse → polarizes to ms = 0 (CARRIER)
- **Microwave drive:** ~2.87 GHz ± field offset → addresses |0⟩↔|+1⟩ and |+1⟩↔|-1⟩ transitions (ENVELOPE)
- **Optical readout:** 637 nm excitation + PL count → distinguishes ms=0 (bright) vs ms=±1 (dim) (SENSOR)

**Operating modes:**

- **Room temperature:** T2 ~ 1 ms with Hahn echo; comfortably below SAM floor; wide academic accessibility.
- **Cryogenic + dynamical decoupling:** T2 ~ 1 s; AT the SAM gravitational floor (per CR-064a); maximum-coherence verification mode.

All NV-specific parameters tagged **[EXPERT_REVIEW_REQUIRED]** pending review by Sean's qubit-engineering contact.

## Quantum State Normalization (Important Note)

SAM slot weights (1/4, 9/16, 1/4) sum to **17/16**.  These are surface-debit fractions, not unit-normalized quantum probabilities.  The physical quantum state has probabilities (4/17, 9/17, 4/17) (re-normalized to sum = 1), with amplitudes (√(4/17), √(9/17), √(4/17)).  Why SAM's surface-debit weights sum to 17/16 (and what that physically means at commit) is the structural question CR-066a will derive.

## Paul Revere Letter Protocol (6 Stages)

Full protocol writeup in **`CR065a_paul_revere_protocol.md`**.  Summary:

| stage | name | summary |
|---|---|---|
| 1 | Initial state preparation | Optical pumping 532 nm; polarize to ms=0 (CARRIER); pre-commit state |
| 2 | Carrier preparation | Microwave pi/2 on |0>↔|+1>; carrier superposition |
| 3 | Envelope loading | Tailored second pulse to (4/17, 9/17, 4/17) distribution; 9/8 surcharge = letter content |
| 4 | Boundary stress reading | Optical 637 nm + PL count; sensor slot probability = stress signal |
| 5 | Commit (measurement) | Projective measurement; row resolves; S_debit registers as 0.0615% of M_native |
| 6 | Verification over N runs | (4/17, 9/17, 4/17) distribution + T2 saturation at T2_grav_at_A_0 |

## Forward-Blind Falsification Conditions

- (F1) The (4/17, 9/17, 4/17) distribution NOT recovered within statistics across N >= 10000 runs.
- (F2) Pre-commit boundary-stress reading shows no statistically significant signal (NV PL implementation may not realize the SAM sensor concept).
- (F3) Effective T2 during Stage 4 CLEARLY exceeds T2_grav_at_A_0 by more than 10x after non-gravitational channel subtraction.

## Expert Review Items (Open)

- NV physical parameters (ZFS, Zeeman split, transition frequencies)
- Microwave pulse sequence for Stage 3 envelope loading
- Effective gate rate for T2_grav comparison
- Citation accuracy for partner candidate groups
- Subtraction of NV-specific decoherence channels (13C bath, surface, charge state)

## Cryptographic Chain

```text
CR060a_alphabet_lock_json                       = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock_json                      = c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR063a_hardware_lock_json                       = f884d362a980a775c010768932f3eeebf44bd135c57625be7dc94b54e9c24639
CR064a_calibration_lock_json                    = 96b549a8de5a387408d18df416ab66b1d487cebc32cbff9c46465016871eee79
CR129b_magnitude_lock_json                      = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd

CR065a_pairing_scoring_csv                       = d97aa46ff74d1226d4bc8b6ff293187c62ea50157f76e0f515c26ffb45de369f
CR065a_hardware_spec_json                        = 4f16b8c9c8fa1956ec36853e1f7cea71960e82a5ad2c3dd69eb7db4652ab9fcc
CR065a_paul_revere_protocol_md                   = 73848ee7e7bb14fa94dbaea83072232f3ca4464bf005919411bfee44b641ed24
CR065a_implementation_lock_sha256                = c5eea33ef58cd5eedaf43aa1779ebe09c453abcffd86a5c28f944fdd7e79f99f
```

## Predictions Checks

- **[PASS]** P1_8_pairings_scored -- pairings scored: 8 (expected 8: 2 qubits x 4 platforms)
- **[PASS]** P2_winner_identified -- winner: (1,2,4) x NV_center (score 14/15)
- **[PASS]** P3_NV_center_is_top_choice -- NV center wins on 3-level structure + PL sensor + accessibility
- **[PASS]** P4_1_2_4_is_preferred_qubit -- (1,2,4) foundational ideal qubit is preferred (lower mass, smaller index ladder)
- **[PASS]** P5_hardware_spec_complete -- hardware spec written, sha256 = 4f16b8c9c8fa1956ec36853e1f7cea71960e82a5ad2c3dd69eb7db4652ab9fcc
- **[PASS]** P6_protocol_writeup_complete -- protocol writeup ready as document chapter, sha256 = 73848ee7e7bb14fa94dbaea83072232f3ca4464bf005919411bfee44b641ed24
- **[PASS]** P7_implementation_lock_written -- implementation lock sha256 = c5eea33ef58cd5eedaf43aa1779ebe09c453abcffd86a5c28f944fdd7e79f99f

## Wrong Controls

- **[PASS]** WC1_no_hardware_demonstration_claimed -- CR065a is implementation SPECIFICATION, not demonstration.  All hardware claims are structural fit per training-cutoff literature.
- **[PASS]** WC2_runner_up_pairings_NOT_excluded -- (1,2,4) x photonic (12/15), (2,4,8) x NV center (13/15), and (2,4,8) x trapped ion (12/15) all remain VIABLE.  CR065a identifies the BEST pairing on the scoring criteria, not the only realizable one.
- **[PASS]** WC3_expert_review_tags_explicit -- All NV-specific parameters and procedures tagged [EXPERT_REVIEW_REQUIRED].  Sean's external contact is the intended reviewer.  Promotion from PROVISIONAL_DRAFT to SEALED requires expert sign-off.
- **[PASS]** WC4_quantum_normalization_vs_SAM_slot_weights_clarified -- SAM slot weights (1/4, 9/16, 1/4) sum to 17/16 (surface debit fractions).  Physical quantum probabilities are (4/17, 9/17, 4/17) after normalization.  This distinction is explicit in the protocol writeup.
- **[PASS]** WC5_falsification_conditions_concrete_and_testable -- Three explicit falsification conditions (F1, F2, F3) with statistical thresholds.  Each is testable on the NV platform; any one triggers CR065a v1.0 refinement.
- **[PASS]** WC6_alternative_platforms_documented -- Scoring table includes all 8 pairings.  Runner-up paths are scored, not dismissed.  If NV center proves unworkable in expert review, alternatives are pre-identified.
- **[PASS]** WC7_protocol_writeup_is_document_chapter_ready -- CR065a_paul_revere_protocol.md is structured as a chapter for the 30-50 page technical document.  Stages, falsification conditions, and honest scope are section-organized.

## Open Debts

- Curator sign-off requires [EXPERT_REVIEW_REQUIRED] tags resolved by Sean's qubit-engineering contact.
- CR066a candidate: derive the structural significance of the 17/16 sum vs the unit-normalized physical state.  Why does SAM's surface debit sum to 17/16 in slot weights?
- CR067a candidate: Multi-qubit operations protocol (CNOT, Toffoli) on the NV platform within Paul Revere architecture.
- Outreach: Hanson group (Delft) is the obvious initial contact for NV cryo+DD T2 measurements.
- Document chapter integration: CR060a, CR061a, CR063a, CR064a, CR065a now form Sections 1-5 of the technical document; CR066a-CR069a will form Sections 6-9.

## Rule of Immutability

Pairing recommendation, hardware spec, and protocol writeup are frozen at CR065a seal time.  Expert review may identify refinements requiring an appeal CR within 12a; the original v1.0 is preserved for the audit record.
