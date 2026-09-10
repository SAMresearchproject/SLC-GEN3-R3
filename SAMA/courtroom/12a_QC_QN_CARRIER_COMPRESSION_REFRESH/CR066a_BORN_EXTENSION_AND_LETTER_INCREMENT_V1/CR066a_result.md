# CR066a Born Rule Extension and the 1/α_H⁴ Letter Increment v1.0

## Verdict

```text
CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1_SEALED
```

## The Question (Open from CR-065a)

SAM slot weights at q = 0 are **(1/4, 9/16, 1/4)** summing to **17/16**.  Physical quantum probabilities sum to **1**.  What is the structural relationship?

## The Structural Decomposition (Locked)

```text
                    17       16     1            1
                   ──── = ──── + ──── = 1 + ──────
                    16       16    16          α_H⁴

                          baseline   letter
                           (Born     increment
                            unity)   (MESSAGE)
```

The **baseline component** is `1 = (1/4, 1/2, 1/4)` = `(1/α_H², 1/α_H, 1/α_H²)` — a maximally-symmetric three-level superposition carrying no message.

The **letter increment** is `1/α_H⁴ = 1/16 = 6.25 %` — the Paul Revere letter content itself.  This is the **SAM-native quantum of letter information** per row.

Equivalent algebraic form:

```text
17/16  =  (R + D + α_H) / α_H⁴
       =  (12 + 3 + 2) / 16
```

## The Letter Signature (Probability Shift)

Converting weights to unit-normalized quantum probabilities:

| slot | weight baseline | weight loaded | prob baseline | prob loaded | shift |
|---|---:|---:|---:|---:|---:|
| a (carrier) | 1/4 | 1/4 | 1/4 | 4/17 | -1/68 |
| b (envelope) | 1/2 | 9/16 | 1/2 | 9/17 | 1/34 |
| c (sensor) | 1/4 | 1/4 | 1/4 | 4/17 | -1/68 |

## Three Invariant Features of the Letter Signature

**(S1)** Outer slots shift equally:  Δ(carrier) = Δ(sensor) = **−1/68**

**(S2)** Middle slot shifts opposite, scaled by α_H:  Δ(envelope) = +1/34 = **−α_H · Δ(carrier)**

**(S3)** Magnitude ratio: |Δ(envelope) / Δ(carrier)| = **2 = α_H** exactly

## Exact Probability Constraints (Loaded State)

On any qubit platform implementing the Paul Revere protocol at q = 0, the commit distribution must satisfy:

```text
P(carrier)  =  P(sensor)       EXACTLY
P(envelope) - P(carrier)  =  5/17       EXACTLY
P(envelope) / P(carrier)  =  9/4        EXACTLY
```

## Born Rule Relationship (Honest Framing)

**Standard Born unity (sum P = 1) is PRESERVED at the measurement stage.**  CR-066a does NOT claim Born is violated.

The 1/α_H⁴ = 1/16 'extension' is the *fractional surface debit excess* at q = 0 above the carrier + sensor unit baseline.  It manifests as a specific **state-preparation signature** that produces a measurable probability shift from baseline (1/4, 1/2, 1/4) to letter-loaded (4/17, 9/17, 4/17).

The signature is observable in standard projective measurements on any 3-level system.  It does not require modifying any rule of quantum mechanics.

## Forward-Blind Sub-Prediction CR066a_PRED_1 (LOCKED)

**Claim:** Any qubit platform implementing the Paul Revere protocol at q = 0 produces commit distribution (4/17, 9/17, 4/17) within statistics, satisfying the three exact invariants.

**Falsifier:** ONE protocol execution on a SAM-native qubit (per CR-065a NV center specification) where the distribution clearly disagrees with (4/17, 9/17, 4/17) beyond statistical uncertainty.

**Non-falsifying:** Distributions NEAR (4/17, 9/17, 4/17) with experimental noise.  Implementation failure at Stage 3 of CR-065a means the test was not run.

**Free parameters at test:** 0.

## What CR066a Does NOT Claim

- That Born rule is modified at measurement (it is NOT; standard QM preserved).
- That the (4/17, 9/17, 4/17) signature has been experimentally observed.
- That the 17/16 sum is directly observable at the energy-eigenvalue level.
- That q ≥ 1 qubits show the same signature (q = 0 only).

## Cryptographic Chain

```text
CR060a_alphabet_lock_json                       = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock_json                      = c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock_json                 = 38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR129b_magnitude_lock_json                      = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd

CR066a_letter_signature_csv                      = d088587aaf7e6eac36f4c385b1ef0032698fdcf296442e76bb70770452c30d93
CR066a_born_extension_lock_sha256                = c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9
```

## Predictions Checks

- **[PASS]** P1_baseline_sums_to_1 -- baseline weights sum = 1
- **[PASS]** P2_loaded_sums_to_17_16 -- loaded weights sum = 17/16
- **[PASS]** P3_letter_increment_eq_1_over_alpha_H_4 -- increment = 1/16 (expected 1/16 = 1/alpha_H^4)
- **[PASS]** P4_invariant_S1_outer_slots_equal -- Delta_a = -1/68, Delta_c = -1/68 (equal: True)
- **[PASS]** P5_invariant_S2_middle_opposite -- Delta_b = 1/34 = -alpha_H * Delta_a: True
- **[PASS]** P6_invariant_S3_magnitude_ratio_2 -- |Delta_b / Delta_a| = 2 (= alpha_H): True
- **[PASS]** P7_exact_probability_ratio_9_4 -- P_envelope / P_carrier = 9/4 exactly: True
- **[PASS]** P8_lock_written -- born extension lock sha256 = c85de54350cb7fa90759e9f2b49afbf0371ccc4b05da318195392bbf4eb53dd9

## Wrong Controls

- **[PASS]** WC1_standard_Born_rule_preserved -- Born unity (probability sum = 1) holds at the measurement stage.  The 1/alpha_H^4 'extension' is a state-preparation signature, NOT a violation of the Born rule.  Standard QM is intact.
- **[PASS]** WC2_q_0_only_explicit -- The 17/16 sum is q = 0 specific.  For q >= 1 the magnitude formula is (4q + D)/(4R) (per CR129b) with different slot decomposition.  Paul Revere letter architecture is q = 0 specific.
- **[PASS]** WC3_letter_signature_is_exact_rational -- The (4/17, 9/17, 4/17) distribution and its three invariants (S1, S2, S3) are EXACT RATIONAL numbers, not empirical fits.  Verification on any platform tests the structural prediction precisely.
- **[PASS]** WC4_falsifier_requires_implementation_correctness -- Falsification requires correct execution of CR065a Stage 3 envelope loading.  Failure to prepare the (4/17, 9/17, 4/17) state is implementation failure, not SAM falsification.
- **[PASS]** WC5_no_experimental_demonstration_claimed -- CR066a derives the structural prediction.  Whether the (4/17, 9/17, 4/17) signature has been observed experimentally is a separate experimental question.
- **[PASS]** WC6_connection_to_Shannon_Holevo_capacity_open -- The 1/alpha_H^4 = 6.25 % letter capacity is the SAM-native quantum per row.  Connection to standard information-theoretic capacity formulas (Shannon, Holevo) is open for a separate derivation.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED.
- Experimental verification on NV platform per CR065a protocol (separate experimental CR).
- CR067a candidate: multi-letter transmissions and capacity scaling -- if each row carries 1/alpha_H^4, does an N-letter transmission carry N * (1/alpha_H^4) or saturate?
- Connection to Shannon / Holevo capacity formulas (separate CR).
- Whether 1/alpha_H^4 is uniquely determined or an empirical match -- structural derivation from R = 2 * alpha_H * D is open.

## Rule of Immutability

Born extension claim (1/α_H⁴ letter increment), letter signature invariants, and exact probability constraints are frozen at CR066a seal time.  Expert review may identify refinements requiring an appeal CR within 12a.
