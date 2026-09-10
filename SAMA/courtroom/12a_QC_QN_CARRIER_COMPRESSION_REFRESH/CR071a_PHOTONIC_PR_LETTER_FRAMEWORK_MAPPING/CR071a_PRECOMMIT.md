# CR071a - Photonic PR Letter Framework Mapping - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR071a/6)
**Test class:** PHOTONIC_PR_LETTER_FRAMEWORK_MAPPING_FROM_NV_DIAMOND_ALPHABET
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR071a maps the NV-diamond Paul Revere letter framework (CR060a
alphabet, CR065a implementation spec, CR068a warning-only simulator)
onto photonic-platform observables for the QN010 strongest-alignment
candidate: Qunnect/Cisco metro photonic entanglement swap.

This is the **first novel design piece** in the Paul Revere Field
Comparison Campaign. CR070a expanded the NV-diamond surface using
the existing T2_grav v1.1 floor and existing CR068a alarm formula.
CR071a is different: it defines the photonic equivalents of A_leak,
A_side, A_share, T2-equivalent, t_fire-equivalent, and the
carrier/envelope/sensor/ledger slot assignments, using ONLY the
CR060a alphabet ratios (no new free parameters).

CR071a does NOT populate a photonic empirical table (that is
CR072a's role). CR071a does NOT test scaling across platforms
(that is CR073a's role). CR071a's deliverable is a mapping table
and a falsifier list.

## Inputs

```text
CR060a (PR letter alphabet lock)        - upstream, not modified
                                          slot weights 4/17, 9/17, 4/17
                                          A_side = 1/24, A_share = 1/12 = 1/R
CR065a (PR implementation spec)         - upstream, not modified
CR068a (warning-only V1)                - upstream, not modified
                                          A_leak = 1 - Tr(rho^2)
                                          t_fire = first crossing of A_side
CR070a (expanded NV-diamond T2 table)   - read-only reference for the
                                          NV side of the mapping
quantum_phase/QN010 candidate manifest  - photonic candidate identifier
                                          (Qunnect/Cisco metro photonic
                                          entanglement swap)
quantum_phase/QN015 diamond topology    - 4-vertex topology from
                                          earlier work; consistency
                                          check for the carrier/sensor/
                                          envelope/ledger photonic role
                                          assignment
Published photonic-platform terminology  - public sources (Qunnect,
                                          Cisco, RFC 9340, NIST
                                          photonic) for documentable
                                          photonic observables
```

Foundation primitives (unchanged):

```text
R       = 12
D       = 3
alpha_H = 2
```

Alphabet ratios (locked from CR060a, used unchanged):

```text
carrier_slot_weight  = 4/17    (outer slot a; route identity)
envelope_slot_weight = 9/17    (middle slot b; letter content, 9/8 surcharge)
sensor_slot_weight   = 4/17    (outer slot c; boundary stress readout)
A_side  = 1/24 = 1/(2R)        (warning threshold)
A_share = 1/12 = 1/R           (basin-commit boundary)
```

## The mapping (NV-diamond -> photonic)

CR071a's deliverable. Each NV-diamond observable maps to exactly one
photonic equivalent. Mapping uses only the CR060a alphabet ratios;
no free knobs.

```text
A_leak          NV:  1 - Tr(rho^2) over single NV electron spin
                PH:  1 - Tr(rho_AB^2) over two-photon Bell pair state
                     (post-link two-photon density matrix)

A_side          NV:  1/24 structural threshold from CR060a
                PH:  1/24 same structural threshold (no platform-specific knob)

A_share         NV:  1/12 = 1/R structural basin-commit boundary
                PH:  1/12 same structural boundary

T2-equivalent   NV:  electron spin T2 at omega_drive = NV resonant
                PH:  entanglement coherence time tau_ent at omega_drive =
                     photon angular frequency at operating wavelength
                     (e.g. 1550 nm telecom -> omega ~ 1.215e15 rad/s)

t_fire          NV:  first time A_leak(t) crosses A_side under T2 decoherence
                PH:  first time A_leak_photonic(t) crosses A_side under
                     entanglement decay characterized by tau_ent

Carrier slot    NV:  m_s = 0 spin sublevel
                PH:  signal-arm photon in protected metro fiber link
                     (matches QN015 DIAMOND-V1-CARRIER)

Envelope slot   NV:  m_s = +1 spin sublevel (weight 9/17, letter content)
                PH:  active polarization/phase compensation channel
                     (matches QN015 DIAMOND-V3-ENVELOPE)

Sensor slot     NV:  m_s = -1 spin sublevel (weight 4/17, boundary readout)
                PH:  boundary timing/drift monitor
                     (matches QN015 DIAMOND-V2-SENSOR)

Ledger node     NV:  spin measurement basis (post-write commit surface)
                PH:  delayed-commit Bell-state-analyzer endpoint
                     (matches QN015 DIAMOND-V4-LEDGER)

T2_grav floor   NV:  T2_grav(omega_NV) = 3.40 us at NV resonant 2.87 GHz
                PH:  T2_grav(omega_photonic) computed by SAME formula
                     16*pi*R^4/(17*omega) at the photonic operating
                     frequency. At telecom 1550 nm:
                     T2_grav ~ 5.04e-11 s = 50.4 ps
```

## Why this mapping has zero free parameters

Every photonic observable above is derived from one of:

1. A direct structural copy of an NV-diamond observable that is
   defined by CR060a alphabet ratios (A_side, A_share, slot weights)
   — these numbers do not change between platforms; they are
   structural consequences of R = 12.

2. A direct structural application of the T2_grav v1.1 formula
   (CR064a) at the photonic platform's omega_drive — same formula,
   different omega.

3. A mapping of a quantum-mechanical observable (A_leak = purity
   loss; t_fire = first crossing) to its multi-particle generalization
   (single-spin rho -> two-photon rho_AB), which is a standard
   quantum-information rewriting, not a fitted choice.

4. A direct apparatus-role copy from QN015's already-emitted
   4-vertex diamond hardware role map.

No knob in CR071a's mapping is adjustable. No threshold is fit to
photonic data (CR072a hasn't loaded photonic data yet). No
platform-specific scaling factor is introduced.

## Predictions

- **P1_every_NV_observable_has_one_photonic_equivalent**
  Every NV-diamond observable in the canonical set {A_leak, A_side,
  A_share, T2-equivalent, t_fire, carrier_slot, envelope_slot,
  sensor_slot, ledger_node, T2_grav_floor} has exactly one named
  photonic equivalent in the mapping table.

- **P2_every_photonic_equivalent_is_documentable_from_public_sources**
  Each photonic-side observable references public-source vocabulary
  from at least one of: Qunnect documentation, Cisco quantum-network
  whitepapers, IETF RFC 9340 (Quantum Internet), NIST photonic
  metrology terminology, standard quantum-optics textbook terms.

- **P3_mapping_uses_only_CR060a_alphabet_ratios**
  The mapping introduces no number that is not one of:
  {4/17, 9/17, 4/17, 1/24, 1/12, 16*pi*R^4/17}, the R = 12 / D = 3 /
  alpha_H = 2 primitives, or omega_drive substitutions into the
  T2_grav v1.1 formula.

- **P4_every_mapping_row_has_a_non_empty_specific_falsifier**
  Every row in the mapping table carries a falsifier statement that
  is non-empty, specific (names an observable behavior that would
  break the mapping), and falsifiable (a photonic measurement could
  in principle confirm or refute it).

- **P5_no_internal_ambiguity_in_assignment**
  Each NV observable maps to exactly one photonic equivalent
  (single-target). No NV observable has two photonic candidates that
  are both "consistent" — that would be ambiguity.

- **P6_T2_grav_formula_unchanged_across_platforms**
  T2_grav(omega) = 16*pi*R^4/(17*omega) is applied identically to
  NV omega_drive and photonic omega_drive. The runner computes
  T2_grav at the canonical telecom 1550 nm photonic omega and at
  a representative 1310 nm omega; these are the same formula, just
  different omega values.

- **P7_QN015_diamond_topology_consistency**
  The carrier/envelope/sensor/ledger slot assignments in the
  mapping match the QN015 diamond topology table verbatim. No
  conflicting role assignment.

- **P8_protocol_completes_end_to_end**
  Runner reads the mapping table, validates each row against P1-P7,
  emits the falsifier list, writes outputs without runtime error.

## Wrong controls

- **WC1_mapping_with_a_free_knob_is_rejected**
  Test row introduces a photonic-side scaling factor "k" not in the
  CR060a alphabet. Runner detects and rejects.

- **WC2_mapping_with_empty_falsifier_is_rejected**
  Test row has falsifier = "" (empty). Runner detects and rejects.

- **WC3_mapping_with_ambiguous_assignment_is_rejected**
  Test row gives two photonic candidates for the same NV observable.
  Runner detects and rejects.

- **WC4_mapping_that_requires_unpublished_photonic_observable_is_rejected**
  Test row references a photonic observable that is not in the
  documented public-source vocabulary list (e.g., a SAM-internal
  term re-used as if it were a photonic platform term). Runner
  detects and rejects.

- **WC5_runner_does_not_modify_upstream_locks**
  Runner is read-only on CR060a, CR065a, CR068a, CR070a, QN015 source
  artifacts.

- **WC6_no_free_parameters**
  All numbers in the mapping trace to CR060a alphabet ratios, R/D/
  alpha_H primitives, or the T2_grav v1.1 formula.

- **WC7_T2_grav_floor_computed_correctly_at_photonic_omega**
  Wrong control: compute T2_grav at telecom omega using the wrong
  formula (omega replaced with 1/omega). Result differs from the
  correct formula by 30+ orders of magnitude. Runner validates that
  the correct formula gives the documented ~50 ps floor at 1550 nm.

- **WC8_QN015_role_swap_rejected**
  Test mapping swaps the carrier and sensor photonic role
  assignments (DIAMOND-V1 <-> DIAMOND-V2). Runner detects the
  conflict with the QN015 frozen topology and rejects.

## Outputs

```text
CR071a_mapping_table.csv        - NV observable -> photonic equivalent
                                  + rationale + falsifier per row
CR071a_falsifier_list.csv       - distilled falsifier statements
                                  (what a photonic measurement must
                                  show to break the mapping)
CR071a_t2_grav_at_photonic.csv  - T2_grav v1.1 evaluated at canonical
                                  photonic operating wavelengths
                                  (1550 nm, 1310 nm, 850 nm)
CR071a_runner.py                - mapping validator
CR071a_summary.json             - pass/fail per prediction and WC
CR071a_result.md                - human-readable
HASHES.txt
```

## Falsifiers

- A photonic measurement showing that A_leak_photonic crossing
  A_side = 1/24 does NOT predict t_fire_photonic under the SAM
  formula (after platform-specific environmental subtraction) would
  falsify the mapping.
- A photonic platform that requires a free knob (e.g., a fitted
  scaling factor on A_side or A_share) for the alarm to fire at
  documented operating conditions would falsify the mapping.
- A two-photon Bell-pair density-matrix purity-loss measurement
  that does not correspond to A_leak = 1 - Tr(rho_AB^2) within
  standard quantum-optics tomography uncertainty would falsify the
  A_leak photonic identification.

These falsifiers are operational: a partner photonic lab can in
principle test each one.

## Free parameters

```text
free_parameters = 0
```

## Honest expected outcome at CR071a seal

CR071a is expected to PASS structurally: the mapping is well-formed,
every row has a falsifier, no free knobs are introduced. The real
test comes in CR072a (when photonic empirical rows load) and CR073a
(when t_fire scaling is tested cross-platform). CR071a establishes
the framework against which CR072a/CR073a then surface honest pass/
fail.

A specific honest concern: the T2_grav floor at telecom photonic
wavelengths is ~50 ps, far below typical entanglement coherence
times (us to s). This means CR072a will likely show all photonic
rows CONSISTENT with huge margins — the floor is structurally easy
to satisfy at photonic frequencies. The interesting CR073a test is
not "does photonic survive the floor" but "does the SAME predictor
that gives NV t_fire also give photonic t_fire."

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution.
Modifications to predictions, wrong controls, or scope after runner
output require a new CR.
