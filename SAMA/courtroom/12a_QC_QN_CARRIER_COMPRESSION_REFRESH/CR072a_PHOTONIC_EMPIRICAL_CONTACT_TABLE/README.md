# CR072a — Photonic Empirical Contact Table

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` at repo root.

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (third of six CRs)

## What this is

CR072a is the photonic counterpart of CR070a. It populates a
photonic-platform empirical contact table using the CR071a mapping
(tau_ent = photonic T2-equivalent per M04). Each row carries a
published-literature value for tau_ent, the row's photonic
omega_drive (derived from operating wavelength), citation tag,
conditions, and `PROVISIONAL_AUTHOR_BEST_EFFORT` verify status.

## How it works

1. Input: `CR072a_photonic_empirical_table.csv` — 14 photonic rows
   from Vienna fiber entanglement, Micius satellite, atomic
   memories, color-center memories, QKD networks, industry metro
   demos, laser-stabilized coherent distribution
2. Runner: computes T2_grav v1.1 at each row's photonic ω, classifies
   as CONSISTENT / BOUNDARY / VIOLATION, validates ω-from-wavelength
   consistency, runs 11 predictions and 8 wrong controls
3. Output: `CR072a_contact_analysis.csv`, `CR072a_summary.json`,
   `CR072a_contact_plot.png`, `CR072a_result.md`

## How to run

```bash
pip install -r requirements.txt
python CR072a_runner.py
```

## The honest verdict (expected)

T2_grav at telecom 1550 nm is ~50 ps. Typical photonic entanglement
coherence times are microseconds to seconds. Most populated rows
expected CONSISTENT_WITH_FLOOR with huge margins. The interesting
test is CR073a (cross-platform t_fire scaling), not CR072a.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.
