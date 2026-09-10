# CR120C Research Candidate Result

record_id: `CR120C_ANCILLA_PARITY_CLOSURE_FACILITY_CANDIDATE`
sealed_utc: `2026-07-13T18:08:17Z`
result_class: `RESEARCH_CANDIDATE`
authority: `PROPOSAL_ONLY`
evidence_status: `NOT_EVIDENCE`
scientific_pass_claimed: `false`
disposition: `RESEARCH_CANDIDATE_ANCILLA_PARITY_MEASUREMENT_PLUS_FEEDBACK_MECHANICALLY_COHERENT_SAM_PHYSICAL_IDENTITY_UNSOURCED`

## Best physical candidate

The strongest concrete mechanism is an **ancilla-mediated weight-8 parity
measurement**.

```text
prepare X1 reference x
couple each proposed S8 binary channel to X1
measure X1: m = x XOR b1 XOR ... XOR b8
condition the S8 state into the measured parity sector
if target-sector closure is required, apply outcome-conditioned feedback
remeasure independently
```

In a gate implementation, the candidate B interaction is an ordered sequence
of eight data-to-ancilla entangling couplings. X1 accumulates only the joint
parity, not the individual component values. Measuring X1 can therefore project
or certify the parity sector without revealing which component contributed.

## What actually facilitates closure

- **Measurement alone:** projects into one of two parity sectors. Keeping only
  the target outcome is postselection, with ideal yield `1/2` for a uniform
  input ensemble.
- **Measurement plus feedback:** when the measured parity is wrong, one
  precommitted parity-flipping operation followed by remeasurement moves the
  state into the target sector in all 512 ideal finite-model challenges.
- **Penalty interaction:** could instead make nonclosure energetically costly,
  but that is a different physical model and was not executed here.

## Exhaustive conditional-model findings

```text
complete (S8, X1) combinations                  512
single-bit flips invert W9 candidate            4096 / 4096
two-bit flips preserve W9 candidate             14336 / 14336
X1 flips invert W9 candidate                    512 / 512
ideal feedback reaches target parity            512 / 512
uniform postselection yield                     1/2
S8 patterns per parity sector at fixed X1       128
```

## Closure is not unique resolution

All eight possible single-channel faults produce the same one-bit parity
syndrome. At least three independent bits are needed to distinguish eight fault
locations, or four bits when the no-fault case is included. The fixed feedback
operation can enforce the target parity, but it does not identify the original
fault or recover the pre-error state.

## SAM boundary

The active SAM route is type-compatible with the abstract input/output shape,
but the scoped sources do not define:

- S8 as eight addressable GF(2) channels;
- X1 as an independently prepared probe;
- B as an entangling or measurement interaction;
- W9 as a binary syndrome payload;
- a feedback/correction operator.

Therefore the parity mechanism is a mechanically coherent and falsifiable
research candidate, not the established physical identity of the SAM entities.
The signed Gauss residual, constraint-penalty Hamiltonian, and structural-null
models remain live competitors.

The CR120 frontier remains unchanged:

```text
PROPAGATE_CLOSURE missing
LEDGER_SITE missing
ADJACENT missing
ADJACENT_LEDGER_STATE missing
```

## Next physical discriminator

Implement or simulate a blinded transfer study with independently prepared X1:
all 256 S8 patterns for each X1 initialization, repeated nondemolition readout,
single- and two-channel flips, no-feedback and random-feedback controls, and a
second independent closure check. The parity candidate survives only if the
complete transfer rule and sector-preserving backaction are observed.
