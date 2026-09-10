# CR074a — Reproducibility Lock

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` at repo root.

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (fifth of six CRs;
engineering CR)

## What this is

CR074a locks the CR070a-CR073a runner chain for partner-lab
reproduction. It walks each CR directory, verifies all expected
artifacts present, verifies SHA-256 hashes against per-CR
HASHES.txt entries, captures actual Python/dep versions used,
emits the three reproducibility-minimum files (`requirements.txt`,
`.python-version`, `seeds.json`), and bundles everything plus
`STEWARDSHIP.md` plus `CAMPAIGN_RERUN.md` plus the campaign doc
into a single `CAMPAIGN_REPRODUCIBILITY_PACK.zip`.

## How to run

```bash
python CR074a_runner.py
```

(no external pip deps; stdlib only — uses hashlib, zipfile, csv,
json, re)

## Discipline drift it catches

Per-CR `requirements.txt` files declared `numpy==1.26.4` and
`matplotlib==3.8.4`. The actual installed versions used during the
campaign were `numpy==2.4.4` and `matplotlib==3.10.9`. CR074a's
pack-level `requirements.txt` pins the ACTUAL versions; per-CR
files are preserved as historical artifacts. This finding is
reported openly per the campaign's "max testing, failures included"
discipline.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.
