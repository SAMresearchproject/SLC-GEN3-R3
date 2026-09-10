# CR068a — Paul Revere Warning-Only Simulator V1.0

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repository root.

---

## What this is

The **warning-only** version of the Paul Revere protocol — the historical Paul Revere, a warning that arrives ahead of the harm. Detects when the protected qubit window has been compromised, before the compromise commits to the ledger, and emits a typed alarm event with timestamp and stress magnitude.

This is the **foundation** that CR067a's self-correction loop builds on. Building the warning version first establishes that we can reliably *detect* compromise before we ask whether we can *correct* it.

## The alarm

- **Observable:** `A_leak = 1 − Tr(ρ²) = 1 − purity`
- **Threshold:** `A_side = 1/24` (the SAM page-one entrance to the basin-forming regime)
- **What fires:** a typed `PaulRevereLetter` payload carrying `(t_fire, A_leak_at_fire, sensor_population, carrier_population, envelope_population, sample_index, reason)`
- **What is NOT exposed:** the carrier's logical route identity. The letter carries the carrier's *population* (a readable observable) but never the route the carrier holds.

## SAM threshold hierarchy

```text
A_leak < 1/24       →  protected unresolved route          (no alarm)
1/24 ≤ A_leak < 1/12  →  basin forming, ALARM FIRES        (recoverable)
A_leak ≥ 1/12       →  uncontrolled write — route is gone  (too late)
```

The warning fires at the *entrance* to the basin-forming regime — early enough that downstream correction (CR067a) still has room to act.

## How to run

```bash
pip install -r requirements.txt
python paul_revere_warning_only_v1.py
```

Runs three cycles automatically:
1. Room-temperature NV (T1 = T2 = 1 ms, 100 μs window)
2. Fast-decoherence test (T1 = T2 = 0.1 ms, 100 μs window) — for P3 scaling
3. No-decoherence control (Lindblad operators removed) — for WC1 false-positive check

Output artifacts written next to the script.

## Predictions (P1–P8)

- P1 — alarm fires within window at room temperature
- P2 — alarm event carries timestamp and stress magnitude
- P3 — alarm time scales with T2 inverse
- P4 — carrier population unchanged by alarm emission
- P5 — alarm fires before A_share basin commit boundary
- P6 — no alarm in no-decoherence control
- P7 — alarm is monotonic in A_leak (no double-fire, no revert)
- P8 — protocol completes end-to-end

## Wrong controls (WC1–WC6)

- WC1 — zero decoherence gives zero alarms
- WC2 — alarm fires after threshold cross, not before
- WC3 — alarm timestamp matches independent purity measurement
- WC4 — alarm magnitude monotonic in actual decoherence
- WC5 — runner does not modify upstream locks
- WC6 — no free parameters introduced

## Scope

CR068a IS:
- A classical software simulation of the warning layer only
- Foundation underneath CR067a's self-correction loop
- Standalone deliverable: a working alarm system for quantum-state compromise

CR068a IS NOT:
- A self-correction protocol (that is CR067a)
- A hardware demonstration (requires partner-lab Stage 4)

## Stewardship

Per `STEWARDSHIP.md`: if commercialization generates revenue, that revenue is intended to fund humanitarian causes — housing, addiction recovery, charitable medical support, education and opportunity access, community charities, environmental prosperity.

## Contact

`sbnvh@missouri.edu`
