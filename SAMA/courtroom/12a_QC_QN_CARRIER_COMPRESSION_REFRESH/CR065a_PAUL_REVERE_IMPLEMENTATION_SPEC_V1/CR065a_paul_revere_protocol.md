# Paul Revere Letter Protocol on NV Center

This protocol implements the SAM-native Paul Revere letter on the NV center
in diamond, realizing the (1, 2, 4) foundational ideal qubit.  All amplitudes
are in standard quantum-mechanical convention (the SAM (1/4, 9/16, 1/4) slot
weights are *probabilities*, so amplitudes are square roots).

## Stage 1: Initial State Preparation (Pre-Letter, |pre-commit>)

Action:  Optical pumping at 532 nm, ~1 microsecond pulse.

Outcome: NV polarized into |ms = 0> (the CARRIER, slot a).

State:   |psi_0> = |ms = 0>

In SAM terms: qA_source_support = M_native = 756 (inventory).
              S_debit = 0 (no surface debit yet; pre-resolution).
              The row is in pure write_candidacy state.

## Stage 2: Carrier Preparation (Activate Slot a)

Action:  Microwave pi/2 pulse on |0> <-> |+1> transition at omega_+1 =
         2.87 GHz + 28 MHz/mT * B_z.

Outcome: Equal superposition of ms = 0 and ms = +1.

State:   |psi_1> = (|0> + |+1>) / sqrt(2)

In SAM terms: Carrier slot a is now in superposition; envelope and sensor
              slots are not yet populated.

## Stage 3: Envelope Loading (Write the Letter Content)

Action:  Second microwave pulse on the |+1> <-> |-1> transition with
         a tailored amplitude that distributes population as
         (1/4, 9/16, 1/4) across (|0>, |+1>, |-1>).

         The amplitudes are sqrt(1/4) = 1/2 on the carrier and sensor,
         and sqrt(9/16) = 3/4 on the envelope (with appropriate phase
         to preserve normalization: 1/4 + 9/16 + 3/16 = 1 ... wait,
         normalization check: |1/2|^2 + |3/4|^2 + |1/2|^2 = 1/4 + 9/16 +
         1/4 = 4/16 + 9/16 + 4/16 = 17/16.  This exceeds 1.

         CORRECTION: the SAM slot weights (1/4, 9/16, 1/4) summing to 17/16
         are SURFACE DEBIT FRACTIONS, not quantum probabilities.  The
         physical quantum amplitudes must be NORMALIZED such that |alpha|^2
         + |beta|^2 + |gamma|^2 = 1.

         The 17/16 sum reflects the surface-debit total in SAM, but the
         physical state's probability amplitudes are RELATIVE (in the same
         ratio 4:9:4 = 0.235:0.529:0.235).  The actual quantum probabilities
         after normalization are (4/17, 9/17, 4/17).

Outcome: State |psi_2> = sqrt(4/17)|0> + sqrt(9/17)|+1> + sqrt(4/17)|-1>

In SAM terms: The envelope slot now carries the 9/8 surcharge on its
              1/2 (=8/16) base weight, yielding 9/16 relative weight.
              The 9/8 surcharge is the LETTER CONTENT itself.

## Stage 4: Boundary Stress Reading (Sensor Slot c)

Action:  Optical excitation at 637 nm, photon counting over a time
         window before the commit collapses the state.

Outcome: PL counts proportional to the sensor-slot probability
         |sqrt(4/17)|^2 = 4/17 ~ 23.5%.  The carrier (ms=0) is
         "bright" (PL count baseline), envelope and sensor are
         "dim" (reduced PL).

In SAM terms: The PL count IS the boundary stress signal.  In SAM's
              architecture, the sensor slot's weight maps directly to
              detector counts BEFORE the row commits.

## Stage 5: Commit (Measure, Row Resolves)

Action:  Strong projective measurement via optical readout pulse.

Outcome: The state collapses to one of |0>, |+1>, |-1> with
         probabilities (4/17, 9/17, 4/17).

In SAM terms: The row commits.  S_debit registers as a measurable
              energy shift in the resolved row's mass:
              M_observed = M_native - S_debit = 756 - 0.4648 = 755.535 MeV
              (in inventory units).

              The DIMENSIONLESS S/M ratio = 17/(16*R^3) = 6.149e-4 = 0.0615%
              is the physically testable quantity, NOT the absolute MeV
              scale.

## Stage 6: Verification Over N Runs

Action:  Repeat stages 1-5 across N >= 10000 runs.

Outcome: The statistical distribution of commit outcomes should match
         (4/17, 9/17, 4/17) within sqrt(N) statistics.

         Additionally, the EFFECTIVE T2 of the |psi_2> state during
         Stage 4 (the pre-commit boundary-stress reading window)
         should saturate at T2_grav_at_A_0 = 16 * pi * R^4 /
         (17 * omega_gate) when all non-gravitational channels are
         minimized.

         For omega_gate = 2*pi * 10 kHz (typical NV cryo+DD effective
         rate), T2_grav_at_A_0 ~ 976 ms ~ 1 second.

In SAM terms: Confirmation of the (1/4, 9/16, 1/4) slot-weight
              distribution + saturation of T2 at T2_grav_at_A_0 would
              be DIRECT EXPERIMENTAL CONFIRMATION of CR060a/CR061a/
              CR063a/CR064a structural predictions.

## Forward-Blind Falsification Conditions

The protocol fails (kills CR065a v1.0) if any of the following are
observed under proper experimental conditions:

(F1) The (4/17, 9/17, 4/17) probability distribution is NOT recovered
     within statistics across N >= 10000 runs of the protocol.
     -> Falsifies the (1/4, 9/16, 1/4) slot decomposition.

(F2) The pre-commit boundary-stress reading at Stage 4 shows no
     statistically significant signal at all.
     -> Suggests the boundary sensor concept is not realized in NV PL
     readout (other implementations might still work).

(F3) The effective T2 during Stage 4 CLEARLY exceeds T2_grav_at_A_0
     by more than 10x after non-gravitational channel subtraction.
     -> Kills the SAM gravitational floor claim from CR064a.

## Honest Scope

- Stage 3's envelope loading sequence is the most experimentally
  delicate -- it requires a tailored composite pulse to produce the
  (4/17, 9/17, 4/17) distribution.  Standard CPMG/Knill sequences
  must be modified.  Expert review required.

- The connection between SAM's surface-debit weights (summing to 17/16)
  and physical quantum probabilities (summing to 1) is via normalization
  ratios 4:9:4.  This is the correct probabilistic interpretation but
  the structural significance of the 17/16 sum's physical realization is
  not yet derived in this CR.

- T2 measurements require careful subtraction of NV-specific decoherence
  sources: 13C nuclear bath, surface defects, charge-state instabilities,
  etc.  Isolating the gravitational channel is non-trivial.

- All NV-specific operating parameters are tagged [EXPERT_REVIEW_REQUIRED].
