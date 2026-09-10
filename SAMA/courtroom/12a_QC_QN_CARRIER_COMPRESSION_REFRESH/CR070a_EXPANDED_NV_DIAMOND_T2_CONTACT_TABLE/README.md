# CR070a — Expanded NV-Diamond T2 Contact Table

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` at repo root.

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (first of six CRs)

## What this is

CR070a deepens the CR069a 8-row mixed-platform T2 contact table into a
20-30 row NV-diamond-only surface. It inherits CR069a's 4 NV-diamond
rows verbatim and adds 18 additional published NV-diamond T2
measurements, all tagged `PROVISIONAL_AUTHOR_BEST_EFFORT` pending
partner-lab citation verification.

## How it works

1. Input: `CR070a_expanded_nv_t2_table.csv` — 22 NV-diamond T2 rows
   with citation tags, sample type, decoupling protocol, temperature
2. Runner: computes T2_grav v1.1 floor at each row's `omega_drive`,
   classifies as CONSISTENT / BOUNDARY / VIOLATION, validates against
   CR069a inherited-row integrity, runs 12 predictions and 8 wrong
   controls
3. Output: `CR070a_contact_analysis.csv`, `CR070a_summary.json`,
   `CR070a_contact_plot.png`, `CR070a_result.md`

## How to run

```bash
pip install -r requirements.txt
python CR070a_runner.py
```

## The honest verdict (expected)

CR070a is expected to surface several VIOLATION rows because
room-temperature Hahn-echo NV T2 in natural-abundance diamond
typically sits at 1-5 us, close to or below the 3.4 us NV-resonant
T2_grav floor. This is honest reporting; the campaign accepts honest
failures alongside passes. CR070a does not pass the table; it
populates the table and reports what's there.

## Inherited rows from CR069a

Rows 1-4 are inherited verbatim from CR069a's published T2 table:
Bar-Gill 2013 (cryo+12C+KDD), Maurer 2012 (nuclear memory),
Naydenov 2011 (RT+CPMG), Childress 2006 (RT+Hahn). Wrong control WC8
detects any drift from CR069a's frozen canonical values.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.
