# QC001 - Private Particle-Informed Paul Revere Carrier Selector

## Result

```text
QC001_PARTICLE_INFORMED_PAUL_REVERE_CARRIER_SELECTED
```

QC001 revisits the QP012B Paul Revere letter after the particle and isotope
closures. The question is no longer only whether a pre-resolution letter can
exist. The question is which SAM-native physical lane should carry it.

## Main Readout

```text
primary_letter_carrier = QUBIT-NL-001
control_envelope = QUBIT-CL-001
boundary_stress_sensor = QUBIT-UNK-001
support_lanes = 3
free_parameters_introduced = 0
```

The selected stack is:

```text
neutral unresolved route      -> protected carrier
charged lepton lane           -> control/readout envelope
8/4 partition boundary route  -> stress / basin sensor
triadic/color/composite lanes -> material support, not primary carrier
```

## Carrier Selector Table

| rank | route | particle family | lead band | QP016 closure | QC role | selector result |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | QUBIT-NL-001 | neutral_lepton_like | EXCEPTIONAL_LETTER_WINDOW | STABLE_SELF_CLOSURE_SELECTED | PRIMARY_PRE_RESOLUTION_LETTER_CARRIER | SELECTED_PRIMARY_LETTER_CARRIER |
| 2 | QUBIT-UNK-001 | unknown_partition_carrier | LONG_LETTER_WINDOW | BOUNDARY_REORGANIZATION_CANDIDATE | BOUNDARY_STRESS_SENSOR | SELECTED_BOUNDARY_STRESS_SENSOR |
| 3 | QUBIT-CL-001 | charged_lepton_like | LONG_LETTER_WINDOW | TRANSIENT_COMMIT_TAIL | CONTROL_ENVELOPE_AND_READOUT_LANE | SELECTED_CONTROL_ENVELOPE |
| 4 | QUBIT-BN-001 | boundary_neutral | USABLE_LETTER_WINDOW | TRANSIENT_COMMIT_TAIL | CLOCK_OR_SCALAR_RETURN_SUPPORT | SECONDARY_SUPPORT_NOT_PRIMARY |
| 5 | QUBIT-TM-001 | triadic_minus_channel | TIGHT_LETTER_WINDOW | TRANSIENT_COMMIT_TAIL | MATERIAL_PAYLOAD_SUPPORT | SUPPORT_NOT_PRIMARY_CARRIER |
| 6 | QUBIT-TP-001 | triadic_plus_channel | TIGHT_LETTER_WINDOW | TRANSIENT_COMMIT_TAIL | MATERIAL_PAYLOAD_SUPPORT | SUPPORT_NOT_PRIMARY_CARRIER |
| 7 | QUBIT-COLOR-001 | native_color_triad_readout | MINIMAL_LETTER_WINDOW | TRANSIENT_COMMIT_TAIL | INTERNAL_COLOR_SUPPORT_NOT_EXTERNAL_LABEL | SUPPORT_NOT_PRIMARY_CARRIER |

## Carrier / Envelope / Support Stack

| layer | name | route | family | role |
| ---: | --- | --- | --- | --- |
| 1 | protected carrier | QUBIT-NL-001 | neutral_lepton_like | carry unresolved phase and Paul Revere syndrome letter |
| 2 | control envelope | QUBIT-CL-001 | charged_lepton_like | supply controlled A-contact for steering and readout |
| 3 | boundary stress sensor | QUBIT-UNK-001 | unknown_partition_carrier | report basin/reorganization pressure before final route identity resolves |
| 4 | material/composite support | triadic/color/support lanes | 3 support lanes | hold apparatus structure, shielding, and coherence platform |

## Interpretation

The Paul Revere letter should ride the neutral unresolved lane, not the charged
apparatus lane. The charged lane matters because it can act as a controlled
envelope for steering and readout, but QC001 separates that from the protected
carrier.

This keeps the QP012B restriction intact:

```text
allowed before resolution:
route family, boundary stress, A_SIDE/A_SHARE timing, basin bias, syndrome signal

not allowed before resolution:
final ledger outcome, logical route identity
```

## Why Particles Matter Here

Before particle closure, QP012B could say which route produced the strongest
letter. After particle closure, QC001 can name the physical lane:

```text
QUBIT-NL-001 -> neutral lepton-like unresolved carrier
QUBIT-CL-001 -> charged lepton-like control envelope
QUBIT-UNK-001 -> partition-boundary stress sensor
```

That is the first real bridge from SAM particle work back into the
quantum-computing lane.

## Outputs

```text
artifacts/qc001/qc001_preflight.md
artifacts/qc001/qc001_particle_informed_carrier_selector.csv
artifacts/qc001/qc001_carrier_envelope_support_stack.csv
artifacts/qc001/qc001_schema.csv
artifacts/qc001/qc001_summary.json
artifacts/qc001/qc001_next_frontier.csv
```

## Next Frontier

```text
QC002_PRIVATE_CARRIER_ENVELOPE_SEPARATION_LAW
```
