# CR071a — Photonic PR Letter Framework Mapping

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` at repo root.

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (second of six CRs)

## What this is

CR071a is the **first novel design piece** in the Paul Revere Field
Comparison Campaign. It maps the NV-diamond Paul Revere letter
framework (CR060a alphabet, CR065a implementation spec, CR068a
warning-only V1) onto photonic-platform observables for the QN010
strongest-alignment candidate: Qunnect/Cisco metro photonic
entanglement swap.

The mapping introduces zero free parameters. Every photonic
equivalent is derived from one of: a CR060a alphabet ratio
(4/17, 9/17, 4/17, 1/24, 1/12), a direct application of the T2_grav
v1.1 formula at the photonic operating omega, a standard quantum-
information generalization (single-qubit to two-qubit purity loss),
or a direct copy from QN015's already-emitted 4-vertex diamond
hardware role map.

## How it works

1. Input: `CR071a_mapping_table.csv` — 10 mapping rows from NV-
   diamond observables to photonic equivalents
2. Runner: validates the mapping against 8 predictions and 8 wrong
   controls; computes T2_grav v1.1 at canonical photonic operating
   wavelengths
3. Output: `CR071a_falsifier_list.csv` (distilled), `CR071a_t2_grav_at_photonic.csv`,
   `CR071a_summary.json`, `CR071a_result.md`

## How to run

```bash
python CR071a_runner.py
```

(no external pip deps; stdlib only)

## The honest verdict (expected)

CR071a is expected to PASS structurally — the mapping is well-formed,
every row has a non-empty falsifier, no free knobs are introduced.
The real test of whether the mapping is correct comes in CR072a
(photonic empirical contact table) and CR073a (cross-platform t_fire
scaling test, the load-bearing test).

## What's in the mapping table

10 rows, one per canonical NV-diamond observable:

- A_leak, A_side, A_share, T2-equivalent, t_fire,
- carrier_slot, envelope_slot, sensor_slot, ledger_node,
- T2_grav_floor

Each row carries: NV definition, photonic equivalent, photonic
definition, structural basis, public source vocabulary, free-knob
flag, falsifier statement.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.
