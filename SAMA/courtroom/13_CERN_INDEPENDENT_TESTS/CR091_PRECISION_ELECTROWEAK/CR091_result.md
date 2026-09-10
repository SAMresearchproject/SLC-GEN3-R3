# CR091 Precision Electroweak - Provisional Result
## Verdict
```text
CR091_OBSERVATIONAL_COMPARISON_REPORT_BUILT (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```
## Courtroom Fields
```text
execution_status = CLEAN
result_class     = OBSERVATIONAL_COMPARISON_REPORT_BUILT
scope_status     = PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
anchor_rows      = 6
```
## Blindness Proof
```text
prediction_commit_sha256 = 3ddf7b91126e7d4fcae3892b2d2bde87238f5eb9c3d3696370f03502d7d5f23d
prediction_commit_utc    = 2026-06-13T21:24:58Z
anchor_envelope_sha256   = 11f07de3e30131658bd9944a4d29dbb9631c0291be79397cf2b6db9d94f5073f
anchor_envelope_open_utc = 2026-06-13T21:24:58Z
temporal_ordering        = OK (prediction commit precedes envelope open)
blindness_protocol_cite  = 13_CERN_INDEPENDENT_TESTS\BLINDNESS_PROTOCOL.md
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```
## Per-Row Comparison
| Row | Observable | Experiment | CERN value | 09a prediction | Residual | Band | Label |
|---|---|---|---|---|---|---|---|
| EW001 | W boson mass | ATLAS | 80366.5 +/- 9.8 (stat) +/- 12.5 (sys) MeV | 80365.1 MeV | -1.40 MeV (-0.0017%) | +/- 25 MeV | AGREEMENT_WITHIN_DECLARED_BAND |
| EW002 | W boson mass | CMS | 80360.2 +/- 2.1 (stat) +/- 9.7 (sys) MeV | 80365.1 MeV | +4.90 MeV (+0.0061%) | +/- 25 MeV | AGREEMENT_WITHIN_DECLARED_BAND |
| EW003 | W boson mass | LHCb | 80354.0 +/- 23.0 (stat) +/- 22.0 (sys) MeV | 80365.1 MeV | +11.10 MeV (+0.0138%) | +/- 25 MeV | AGREEMENT_WITHIN_DECLARED_BAND |
| EW004 | Z boson mass | LEP combined (legacy CERN) | 91187.6 +/- 2.1 (stat) +/- 0.0 (sys) MeV | 91161.5 MeV | -26.10 MeV (-0.0286%) | +/- 5 MeV | AGREEMENT_OUTSIDE_DECLARED_BAND |
| EW007 | Top quark mass | ATLAS | 172690.0 +/- 250.0 (stat) +/- 0.0 (sys) MeV | 172542.0 MeV | -148.00 MeV (-0.0857%) | +/- 1000 MeV | AGREEMENT_WITHIN_DECLARED_BAND |
| EW008 | Top quark mass | CMS | 171770.0 +/- 370.0 (stat) +/- 0.0 (sys) MeV | 172542.0 MeV | +772.00 MeV (+0.4494%) | +/- 1000 MeV | AGREEMENT_WITHIN_DECLARED_BAND |

## Row Label Counts
```text
AGREEMENT_WITHIN_DECLARED_BAND                5
AGREEMENT_OUTSIDE_DECLARED_BAND               1
INFORMATION_INSUFFICIENT_AT_THIS_CR           0
```
## Open Debts
```text
- BLINDNESS_PROTOCOL sha256 sibling file not yet written
- Seal sha256 sibling file not yet written
- citation_verification_status PENDING on every anchor row (curator sign-off)
```
## Rule-9 Reminder
```text
This CR does not falsify 09a. 09a's exemplary verdict is preserved
regardless of where each residual lands. Per-row labels are
observational reporting under blindness discipline.
```
