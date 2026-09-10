# CR120ZB Functional Hardware Interface Specification

This specification defines what a later laboratory implementation must supply without declaring that any existing gate is physically B or X1.

## Request-side B interface

- Independently addressable first time window.
- Local operation on the designated request subsystem.
- Capable of preparing coherence from a computational-basis input.
- Can be disabled, dephased, substituted by a local unitary, or moved after the response window without changing the remainder of the schedule.

## Response-side X1 interface

- Independently addressable later time window.
- Joint operation or resolved joint measurement involving both designated subsystems.
- Can be disabled, applied before B, or replaced by a product operation under matched duration and calibration.
- Its event flag must be fixed before remote measurement outcomes are opened.

## Non-identity criterion

The ports count as a functional request/response realization only if the forward-order interaction produces nonseparability beyond both isolated stages, reverse order, matched local operations, dephased request, and classical return. Relabeling two compiler segments of one indivisible entangling pulse does not meet the criterion.

## Hardware record required later

Raw shots, device and qubit identifiers, pulse/circuit bytes, randomized schedule, timestamps, calibration split, readout matrix, leakage and crosstalk monitors, every herald and nondetection, uncertainty intervals, and an untouched replication block.
