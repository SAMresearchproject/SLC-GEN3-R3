# CR069a — Stage 2: Empirical T2 Contact Table

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` and `EPISTEMIC_STANCE.md` at repo root.

## What this is

The Stage 2 deliverable for lifting CR064a v1.1 (`T2_grav = 16π·R⁴/(17·ω_drive)`) from BOUNDARY toward PASS. Compares the floor prediction against published T2 measurements from NV centers, superconducting transmons, trapped ions, and optical clocks.

## How it works

1. Input: `CR069a_published_t2_table.csv` — literature T2 measurements with citation tags, each carrying `[VERIFY_PRECOMMIT_AGAINST_PUBLISHED_PAPER]` for partner-lab confirmation
2. Runner: computes T2_grav at each row's `omega_drive`, classifies the row as CONSISTENT_WITH_FLOOR / BOUNDARY_AT_FLOOR / VIOLATION_OF_FLOOR
3. Output: `CR069a_contact_analysis.csv`, `CR069a_summary.json`, `CR069a_contact_plot.png`, `CR069a_result.md`

## How to run

```bash
pip install -r requirements.txt
python CR069a_runner.py
```

## The honest verdict

CR069a does not validate the gravitational T2 floor. It checks whether published measurements are *consistent* with the floor (a necessary, not sufficient, condition). Current measurements sit far above the floor — they are environmental-noise-limited, not engineering-limited by gravity. The interesting test is years away: push T2_observed close to T2_grav and ask whether it saturates at the floor.

What CR069a *does* establish:
- No populated published measurement falsifies CR064a v1.1
- The framework for ongoing partner-lab verification is in place
- Initial provisional population of 8 representative platform rows, each tagged for citation confirmation

## What partner-lab verification adds

Each row sits at `PROVISIONAL_AUTHOR_BEST_EFFORT` status. A partner lab (or experimental collaborator) confirms each citation against the actual published paper and lifts the row to `VERIFIED`. When the verified fraction reaches a structural threshold across diverse platforms, the aggregate verdict can be promoted from `PROVISIONAL` to `STAGE2_VERIFIED`, which is what lifts CR064a v1.1 from BOUNDARY toward PASS.

## Stewardship

Per `STEWARDSHIP.md`.
