# CR120C Precommit

record_id: `CR120C_ANCILLA_PARITY_CLOSURE_FACILITY_CANDIDATE`
task: `Investigate what physical interaction or measurement facilitates 8 + 1 closure from attached working note`
classification: `CONSTRUCTIVE_NEW_WORK / RESEARCH_CANDIDATE`
authority: `PROPOSAL_ONLY`
evidence_status: `NOT_EVIDENCE`
validation_state: `UNVALIDATED_PHYSICAL_IDENTITY`

## Question frozen before execution

What physical interaction or measurement could implement the already typed
SAM route

```text
RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)
  -> W9_CLOSURE_WITNESS
```

and by what mechanism could it move an unresolved state into a closure sector?

## Primary candidate frozen before execution

The primary research candidate is an ancilla-mediated weight-8 parity
measurement:

```text
b = (b1,...,b8) in GF(2)^8
x = independently prepared X1 probe/reference bit
m = x XOR b1 XOR ... XOR b8
```

Candidate physical sequence:

1. prepare the X1 ancilla in a declared reference state `x`;
2. couple each of eight proposed S8 binary channels to X1 through an
   entangling interaction;
3. measure X1 to obtain the proposed W9 syndrome `m`;
4. interpret the measurement as a projection into one parity sector;
5. if deterministic target-sector closure is required, apply a precommitted
   outcome-conditioned parity-flipping operation and measure again.

For a computational-basis parity extraction, one ideal circuit realization is
the ordered product of eight data-to-ancilla controlled-X operations. Equivalent
controlled-phase/dispersive realizations are platform-dependent and are not
identified with SAM's `B_CONTACT_OPERATOR` by this test.

## Competing candidates retained

| Candidate | Proposed role | Status before execution |
|---|---|---|
| Ancilla parity extraction | projects/certifies a binary constraint sector | primary conditional model |
| Signed eight-face Gauss residual | measures a local conservation constraint | open analogy |
| Constraint-penalty Hamiltonian | energetically suppresses violations | open enforcement model |
| Structural null | B is a typed structural relation with no physical measurement | live wrong-model control |

No candidate may be installed or promoted by this result.

## Precommitted consistency gates

1. Enumerate all `2^8 * 2 = 512` `(S8, X1)` input combinations.
2. Verify `m = x XOR parity(S8)` for the complete candidate transfer table.
3. Every single S8-bit flip must invert `m` at fixed X1.
4. Every two-bit S8 flip must preserve `m` at fixed X1.
5. Flipping X1 must invert `m` for every S8 pattern.
6. The two proposed parity sectors must each contain 128 S8 patterns for a
   fixed X1 and 256 rows in the full transfer table.
7. A conditional single-bit operation must move every rejected ideal parity
   outcome into the target parity sector on a second check.
8. Postselection-only yield must remain visible as 1/2 for a uniformly sampled
   input ensemble; it must not be called deterministic closure.
9. A single W9 syndrome bit must not be called unique resolution: eight
   possible single-site faults require at least 3 bits to identify, or 4 bits
   when the no-fault case is also included.
10. Majority, unsigned-sum, selected-bit, stuck-X1, and randomized-X1 controls
    must remain distinguishable from the complete parity transfer rule.
11. Local SAM sources must be scanned for explicit physical semantics. Absence
    of `parity`, `ancilla`, `syndrome`, `measurement`, `projector`, `Gauss`, or
    `Hamiltonian` semantics must prohibit identification of B, X1, S8, or W9
    with the candidate apparatus.
12. The CR120 frontier must remain missing and no raw traceback may reach the
    result.

## Precommitted disposition

If all logical gates are satisfied, the disposition is:

`RESEARCH_CANDIDATE_ANCILLA_PARITY_MEASUREMENT_PLUS_FEEDBACK_MECHANICALLY_COHERENT_SAM_PHYSICAL_IDENTITY_UNSOURCED`

This is not a scientific PASS. It means only that the candidate mechanism is
internally coherent, exhaustive on the declared finite model, experimentally
motivated, and falsifiable.

## Frozen local sources

```text
d5283ccc6565bf75f0952d43df845496b02c3f8fadc288feba3d5b246e8b4358  C:/Users/drwho/.codex/attachments/52fb4fe5-c3c6-47af-8df9-2429cec59cac/pasted-text.txt
b131ba0b23189e2b1bbf365ca40db57bca10a8edbd05d4d85f170581c71108e6  14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_result.md
491b37f76cdcc3dc793c059d458aaa9fa46f250f3ce08b069720476b0849b137  14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_VALIDATION_REPORT.json
ad197382fb2594d32afa56ec936371bf093aa373656088792705343239359228  14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_typed_hierarchy.json
098c88a2275a359e6a9305836bb79baac306b1562dea117c1ecd2509f5b034e3  09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_result.md
c4cd0142a8d43b810c438586242a68f429de675f0d168169a11b085653d142ea  09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_result.md
1ed95b854c1f5370df69438484b1e2f80f7a2c19d288dc714a5e1c5b7316ac88  09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_summary.json
beb5effdf9c3d0a0050e686f9a716f6f547c54dcc6e54efa878f685b0fdf1beb  09a_PARTICLE_MASS_CHAIN/CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT/CR282_APPEAL_result.md
09ddbf4dd2647249404b3b9bbc8a01625ad181e848cc592fc98119c5b05de1b9  SAM_LANGUAGE_V0_4_1_CANDIDATE/V0_4_1_ENTITY_REGISTRY.json
5e7866eb0c8789c4d8fe321dd6ac131a8aff57429b58684bcd2507c03152a212  SAM_LANGUAGE_V0_4_1_CANDIDATE/V0_4_1_OPERATOR_REGISTRY.json
1e0be6539763de0347c75af8eda2259b385a99b3585a13e3ccecad2f49744ae4  SAM_NATIVE_MASTER_FORMULA_V4_2.md
976c649d071db8e2320406899dca3aae8a10dad2bcef277b2954c9c931d600cd  SAM_NATIVE_ACTION_ENGINE_V4_2.md
```

## External feasibility references

These papers support only the general physical feasibility of ancilla parity
measurement, projective sector preparation, repeated QND readout, and feedback.
They are not SAM authority.

- C. Eichler et al., *Entanglement stabilization using ancilla-based parity
  detection and real-time feedback in superconducting circuits*, npj Quantum
  Information 5, 69 (2019):
  https://www.nature.com/articles/s41534-019-0185-4
- L. Pereira, J. J. Garcia-Ripoll, and T. Ramos, *Parallel tomography of quantum
  non-demolition measurements in multi-qubit devices*, npj Quantum Information
  9, 22 (2023):
  https://www.nature.com/articles/s41534-023-00688-7
- P. Scholl et al., *Universal quantum operations and ancilla-based read-out for
  tweezer clocks*, Nature (2024):
  https://www.nature.com/articles/s41586-024-08005-8
- L. Sun et al., *Tracking photon jumps with repeated quantum non-demolition
  parity measurements*, Nature 511, 444-448 (2014):
  https://www.nature.com/articles/nature13436

## Hard boundaries

- `B_CONTACT_OPERATOR` is not declared to be a controlled gate, dispersive
  coupling, measurement, or Hamiltonian.
- `S8_BINARY_SURFACE` is not declared to be eight addressable qubits or faces.
- `X1_AXIS_SELF_CHANNEL` is not declared to be a probe or ancilla.
- `W9_CLOSURE_WITNESS` has no registered binary outcome payload.
- A one-bit parity witness certifies a sector but cannot uniquely identify an
  arbitrary error or reconstruct the original state.
- `PROPAGATE_CLOSURE`, `LEDGER_SITE`, `ADJACENT`, and
  `ADJACENT_LEDGER_STATE` remain missing.

Stop after one sealed conditional-model candidate.
