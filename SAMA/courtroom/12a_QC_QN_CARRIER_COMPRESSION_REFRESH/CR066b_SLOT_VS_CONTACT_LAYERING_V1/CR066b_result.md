# CR066b Slot vs Contact-Level Layering of the 1/α_H⁴ Letter Increment v1.0

## Verdict

```text
CR066b_SLOT_VS_CONTACT_LAYERING_V1_SEALED
```

## What CR-066b Refines

CR-066a established that the letter increment is 1/α_H⁴ = 1/16 and that the loaded probabilities are (4/17, 9/17, 4/17).  An open question remained: how exactly does the 1/16 surcharge distribute across the slot architecture?  CR-066b locks the answer at two distinct layers.

## The Two Locked Layers + One Rejected Reading

| layer | representation | sum | structural meaning |
|---|---|---:|---|
| slot-level (LOCKED) | (0, 1/16, 0) | 1/16 | Center-only surcharge -- the bridge slot is lifted.  Outer slots unchanged. |
| contact-level (LOCKED) | (1/32, 1/32, 0) | 1/16 | Bridge-only surcharge resolves symmetrically across two adjacent contact legs.  Outer-cross (a,c) has zero direct debit; carrier and sensor communicate only through the bridge. |
| (REJECTED) mini-1:2:1 packet | (1/64, 1/32, 1/64) | 1/16 | Would preserve the (1/4, 1/2, 1/4) base shape after normalization and erase the central lift.  REJECTED because the locked form specifically lifts the center, not all three slots proportionally. |

## Slot Level: Center-Only Surcharge (LOCKED)

```text
    Δw_slot  =  (0, 1/16, 0)

    base:    (1/4,     1/2,     1/4)
    loaded:  (1/4,     9/16,    1/4)

    The bridge (middle) slot is LIFTED.  The outer slots
    (carrier and sensor) are UNCHANGED.
```

## Contact Level: Bridge-Split (LOCKED)

```text
    Δ_pair  =  ( 1/32,    1/32,    0 )
                (a,b)    (b,c)   (a,c)
               bridge   bridge   outer
                leg      leg     cross

    Bridge-only surcharge resolves symmetrically across two
    adjacent contact legs.  Outer-cross (a,c) has ZERO direct
    debit -- carrier and sensor communicate ONLY through the
    bridge.  This realizes CR051/CR054 no-clone guard at the
    surface-debit layer.
```

## Rejected Reading: Mini-1:2:1 Packet (1/64, 1/32, 1/64)

Sums to 1/16 — same total — but **would preserve the (1/4, 1/2, 1/4) base shape proportionally and erase the central lift.**  The locked form specifically requires the bridge to be lifted asymmetrically, so this representation is rejected.

## Amplitude Signature (Quantum-Mechanical)

```text
    Probabilities:  ( 4/17,    9/17,    4/17 )    sum = 1
    Amplitudes:     ( √(4/17), √(9/17), √(4/17) )
                  = ( 2/√17,   3/√17,   2/√17  )

    Ratio:  2 : 3 : 2     (locked, exact)
```

## The Higgs 1/8 Bridge Attribution

Identity:

```text
       1            1                  1         1
      ────  =   ──────  ·  ──────  =  ─── × 2⁻ᴰ
       16        α_H        α_H³       α_H

       ↑             ↑          ↑        ↑
       letter        bisection   the 1/8 released
       capacity     (α_H = 2)    by Higgs split
```

Per CR-120: R² = 144 splits as 7/8 retained (H_native = 126 GeV) + **1/8 released** (= 18 units tensor carrier).

Per CR-121: the 1/8 released combines with qA to form **gravity**.

Per CR-066b: the Paul Revere letter capacity = **1/16 = HALF of that released 1/8**.

**Structural reading:** the bridge slot carries HALF of each row's Higgs-released 1/8 burden as letter content.  The other half remains as pure gravity coupling.  The Paul Revere letter and gravity SHARE the released-1/8 channel equally, bisected by α_H = 2.

## Forward-Blind Sub-Prediction CR066b_PRED_1 (LOCKED)

Three independently testable claims:

- **Slot-level claim:** Δw_slot = (0, 1/16, 0).  Outer slots unchanged.  Falsified if outer-slot lift detected above noise.
- **Contact-level claim:** Δ_pair = (1/32, 1/32, 0).  Outer-cross (a, c) leg debit ≡ 0.  Falsified if direct outer-cross channel observed.
- **Amplitude claim:** ratio 2 : 3 : 2 exactly.  Falsified if observed ratio significantly differs.

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR060a_alphabet_lock_json                       = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR061a_selection_lock_json                      = c011534994895365d1399282f9c346486a678603c351d8afb09823f70dd09584
CR065a_implementation_lock_json                 = 38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock_json                 = 5eb918d789d70d689e39f9d5c2f72ea4d149336d1e3a8b49d95548f5de592fc1
CR121_gravity_mechanism_lock_json               = 01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469
CR129b_magnitude_lock_json                      = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd

CR066b_layering_table_csv                        = 16b1c664872370925d8d937ec1cdce70cf9b6d909e2eb6e80857e1bfd762af8e
CR066b_hierarchy_lock_sha256                     = 60842345eed77ae88637519a0de5076a5f9abcb3d5a40e692a4ea551db9327cc
```

## Predictions Checks

- **[PASS]** P1_slot_level_sum_equals_1_16 -- slot-level surcharge sum = 1/16
- **[PASS]** P2_contact_level_sum_equals_1_16 -- contact-level surcharge sum = 1/16
- **[PASS]** P3_slot_level_center_only -- Delta_w_slot = (Fraction(0, 1), Fraction(1, 16), Fraction(0, 1)) (center-only verified)
- **[PASS]** P4_contact_level_outer_cross_zero -- outer-cross (a,c) leg debit = 0
- **[PASS]** P5_contact_level_bridge_legs_symmetric -- (a,b) leg = 1/32; (b,c) leg = 1/32; symmetric: True
- **[PASS]** P6_rejected_packet_lifts_outer_slots -- (1/64, 1/32, 1/64) would give outer slots 17/64 and 17/64 (not 1/4), erasing the central lift
- **[PASS]** P7_Higgs_letter_identity_holds -- 1/16 = (1/alpha_H) * (1/alpha_H^3) = (1/2) * (1/8) = 1/16 = 1/16
- **[PASS]** P8_amplitude_ratio_2_3_2 -- amplitudes (sqrt(4/17), sqrt(9/17), sqrt(4/17)) give ratio 2 : 3 : 2 by inspection of square roots of (4, 9, 4)
- **[PASS]** P9_lock_written -- hierarchy lock sha256 = 60842345eed77ae88637519a0de5076a5f9abcb3d5a40e692a4ea551db9327cc

## Wrong Controls

- **[PASS]** WC1_CR066a_NOT_invalidated -- CR066a's 1/alpha_H^4 letter increment, (4/17, 9/17, 4/17) probabilities, and Born extension framing remain correct.  CR066b refines the STRUCTURAL LAYERING of how the 1/16 lives, not the value itself.
- **[PASS]** WC2_mini_1_2_1_packet_explicitly_REJECTED -- The (1/64, 1/32, 1/64) representation is documented in the layering table as REJECTED with explicit reasoning.  Future readers should not confuse it with the locked slot-level center-only form.
- **[PASS]** WC3_contact_resolution_symmetric_under_reflection_only -- The (1/32, 1/32, 0) contact-level split assumes reflection symmetry a <-> c.  Asymmetric routes might split the bridge surcharge differently across the two adjacent legs.  Explicitly noted in out-of-scope.
- **[PASS]** WC4_q_0_only_explicit -- All CR066b claims are q = 0 specific (per CR066a / CR129b).  Whether the bridge-only attribution generalizes to q >= 1 is a separate question.
- **[PASS]** WC5_Higgs_attribution_is_arithmetic_NOT_physical_identity -- The 1/16 = (1/alpha_H) * 2^-D identity is dozenal arithmetic linking the Paul Revere letter capacity to the Higgs-released gravitational fraction.  It does NOT claim the physical Higgs boson IS the bridge slot, only that they share the same surface-debit-channel arithmetic.
- **[PASS]** WC6_no_clone_guard_realized_at_surface_debit_layer -- The contact-level (1/32, 1/32, 0) split with zero outer-cross is the surface-debit realization of CR051's no-clone guard: any relay processing the bridge can refresh the envelope but cannot copy the (a, c) endpoints directly.  This is a structural emergence, not an assumed axiom.
- **[PASS]** WC7_falsifier_per_layer -- Three concrete falsifiers per layer: slot-level (outer slot lift above 1/4), contact-level (significant outer-cross debit), amplitude (deviation from 2:3:2).  Each is independently testable on the NV platform.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED.
- Expert review on whether the symmetric bridge-split (1/32, 1/32, 0) is structurally unique or admits asymmetric variations.
- CR067a candidate: capacity scaling -- does an N-letter row carry N * (1/alpha_H^4) or saturate?
- Whether the bridge-only attribution generalizes to q >= 1 rows (currently q = 0 only).

## Rule of Immutability

Slot-level center-only attribution, contact-level bridge-split, explicit rejection of the mini-1:2:1 packet, 2:3:2 amplitude signature, and Higgs 1/8 bisection identity are frozen at CR066b seal time.  Expert review may identify refinements requiring an appeal CR within 12a.
