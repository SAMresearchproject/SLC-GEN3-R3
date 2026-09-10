# CR073a — Cross-Platform PR Letter Scaling Test (LOAD-BEARING)

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. See `STEWARDSHIP.md` at repo root.

**Campaign:** PAUL_REVERE_FIELD_COMPARISON (fourth of six CRs;
load-bearing test)

## What this is

CR073a is the campaign's load-bearing cross-platform scaling test.
It applies the SAM t_fire predictor (derived from CR068a's
A_side = 1/24 alarm and a pure-dephasing exponential decoherence
model) to:

- 22 NV-diamond rows from CR070a (with T2_observed)
- 14 photonic rows from CR072a (with tau_ent_observed)

and tests whether the SAME constant `c0_SAM ~ 0.0210` applies on
both populations.

## Data gap (honest up front)

No published `t_fire_observed` values exist for either NV-diamond
or photonic platforms. The PR letter alarm at A_leak = 1/24 is
SAM-native. CR073a uses the **textbook 1/e purity-decay convention**
(T2/2) as the portable comparison reference, with the data gap
documented explicitly. Partner-lab measurement of actual alarm
times under the SAM A_side = 1/24 protocol is the named verification
path.

## How it works

1. Inputs: `CR070a_contact_analysis.csv` + `CR072a_contact_analysis.csv`
2. Runner: applies `t_fire = coherence_time * c0_SAM` to every row;
   compares to `t_fire_obs = coherence_time * 0.5` (textbook 1/e);
   computes per-row residual; counts rows within 0.25 and 0.15;
   applies pre-committed thresholds
3. Outputs: `CR073a_t_fire_per_row.csv`, `CR073a_residual_distribution.csv`,
   `CR073a_summary.json`, `CR073a_residual_plot.png`, `CR073a_result.md`

## How to run

```bash
pip install -r requirements.txt
python CR073a_runner.py
```

## Honest expected outcome

The SAM A_side = 1/24 alarm fires at ~4.2% purity loss; the
textbook 1/e convention fires at ~63%. The constants differ by a
factor of ~23. Uniform residual ~95.8% on every row — far above
the 0.25 tolerance. Expected result: structural floor breached
against the textbook reference (0 of 14 photonic rows within 0.25),
while structural cross-platform formula generalization holds
(same c0_SAM, same R² ~ 1.0 on both fits).

This is the campaign's anticipated **valuable negative result against
the textbook reference**: SAM's threshold is structurally tighter
than the conventional 1/e alarm by design. The cross-platform
generalization at the formula layer is real. The absolute tolerance
gap is real. Partner-lab measurement closes the loop.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.
