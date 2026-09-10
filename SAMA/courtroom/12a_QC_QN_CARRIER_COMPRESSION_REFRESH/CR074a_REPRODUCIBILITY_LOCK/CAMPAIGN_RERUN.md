# CAMPAIGN RERUN PROCEDURE

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

## What this is

This document tells a partner lab (or any independent reviewer) how to
rerun the Paul Revere Field Comparison Campaign (CR070a-CR073a)
end-to-end from this reproducibility pack and verify that the
outputs hash-match the recorded results.

## Prerequisites

1. Python 3.12.10 (exact). Install from python.org or
   via pyenv: `pyenv install 3.12.10`.
2. The single CAMPAIGN_REPRODUCIBILITY_PACK.zip file from this CR074a.

## Procedure

```bash
# 1. Unzip the pack
unzip CAMPAIGN_REPRODUCIBILITY_PACK.zip
cd CAMPAIGN_REPRODUCIBILITY_PACK

# 2. Create a fresh Python venv at the pinned version
python3.12 -m venv .venv
source .venv/bin/activate    # POSIX
.venv\Scripts\activate       # Windows PowerShell

# 3. Verify Python version
python --version    # must report 3.12.10

# 4. Install pinned dependencies
pip install -r requirements.txt
pip list    # numpy 2.4.4, matplotlib 3.10.9

# 5. Rerun each CR runner in order
cd CR070a_EXPANDED_NV_DIAMOND_T2_CONTACT_TABLE && python CR070a_runner.py && cd ..
cd CR071a_PHOTONIC_PR_LETTER_FRAMEWORK_MAPPING && python CR071a_runner.py && cd ..
cd CR072a_PHOTONIC_EMPIRICAL_CONTACT_TABLE && python CR072a_runner.py && cd ..
cd CR073a_CROSS_PLATFORM_PR_LETTER_SCALING_TEST && python CR073a_runner.py && cd ..

# 6. Verify hashes match
# Use the PACK_MANIFEST.csv to recompute SHA-256 of every emitted file
# and compare against the recorded value.
```

## What you should see

Each runner prints a final `Result class: ...` line summarizing the
X-of-Y outcomes for predictions, wrong controls, row classifications.
The result class strings should byte-identically match the recorded
ones in this pack's summary.json files.

Expected result classes:

```text
CR070a_EXPANDED_NV_DIAMOND_T2_TABLE_SEALED__
  PREDICTIONS_10_OF_12__WRONG_CONTROLS_7_OF_8__
  ROWS_22__CONSISTENT_17__BOUNDARY_1__VIOLATIONS_4

CR071a_PHOTONIC_MAPPING_SEALED__
  PREDICTIONS_8_OF_8__WRONG_CONTROLS_8_OF_8__
  MAPPING_ROWS_10__FREE_PARAMETERS_0

CR072a_PHOTONIC_EMPIRICAL_TABLE_SEALED__
  PREDICTIONS_11_OF_11__WRONG_CONTROLS_7_OF_8__
  ROWS_14__CONSISTENT_14__BOUNDARY_0__VIOLATIONS_0

CR073a_CROSS_PLATFORM_T_FIRE_SCALING_SEALED__
  PREDICTIONS_11_OF_11__WRONG_CONTROLS_9_OF_9__
  NV_ROWS_22__PHOTONIC_ROWS_14__
  PHOTONIC_WITHIN_0_25_0_OF_14__PHOTONIC_WITHIN_0_15_0_OF_14__
  VERDICT_STRUCTURAL_FLOOR_BREACHED_AGAINST_TEXTBOOK_1_OVER_E_REFERENCE
```

If you see different result_class strings, something in your
environment differs from the locked spec. Most common causes:
wrong Python patch version (3.12.10 vs 3.12.x), wrong numpy or
matplotlib version, or a CSV character-encoding/line-ending issue.

## Discipline drift caught in pack-build

The per-CR `requirements.txt` files in each CR directory declare
`numpy==1.26.4` and `matplotlib==3.8.4`. The ACTUAL versions used
were 2.4.4 and 3.10.9. The pack-level `requirements.txt` pins the
ACTUAL versions for byte-identical reproduction. The per-CR files
are preserved as historical artifacts; changing them would require
new CRs.

## What this pack is NOT

This is a reproducibility pack, not a partner-lab agreement and not
a commercial deployment. The PR letter alarm at A_side = 1/24 is
SAM-native; lifting any CR from PROVISIONAL_AUTHOR_BEST_EFFORT to
VERIFIED requires partner-lab citation verification (for CR070a /
CR072a published-T2 / tau_ent values) and/or partner-lab hardware
measurement of actual A_leak-threshold-crossing alarm times (for
CR073a load-bearing validation).

## Stewardship

Per `STEWARDSHIP.md` (included in this pack). Any commercial value
flowing from this work or its derivatives is subject to the
stewardship intent: revenue funds humanitarian causes.
