# CR067b — Paul Revere NV-Center Simulator V1.0 — CRYO + DYNAMICAL DECOUPLING

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repo root.

## What this is

The **cryo + dynamical decoupling** operating-point version of CR067a's self-correction simulator. Same architecture, same loaded state, same protocol, same predictions — only the NV operating parameters change:

| CR | regime | T1 | T2 | window/T1 |
|---|---|---|---|---|
| **CR067a** | room temperature | 1 ms | 1 ms | 10% (P3 near-miss expected) |
| **CR067b** | cryo + DD (Hanson regime) | 1 s | 1 s | 0.01% (clean pass expected) |

This is the partner-lab reference characterization. Hanson group at Delft operates at this regime with isotopically purified ¹²C diamond and CPMG/KDD pulse sequences. The simulator is set up to mirror what a lab run would see.

## How to run

```bash
pip install -r requirements.txt
python paul_revere_nv_simulator_v1_cryo.py
```

## Architectural relationship to CR067a

CR067b does **not** supersede CR067a. Both stand:
- **CR067a** = the room-temperature operating-point reference (useful for many academic NV groups that operate at room temp)
- **CR067b** = the cryo+DD operating-point reference (useful for Hanson-style high-coherence labs and partner hand-off)

The PRECOMMIT predictions are identical between CR067a and CR067b. The only difference is the operating-point parameters and the consequent residuals on the predictions that depend on T1/T2.

## Stewardship

Per `STEWARDSHIP.md`.
