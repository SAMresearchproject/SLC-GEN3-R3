# CR279 Higgs Direct-Weld Promotion Result

generated_utc: 2026-07-11T08:21:53+00:00
primary_verdict: PASS_HIGGS_DIRECT_WELD_PROMOTION
execution_status: CLEAN

## Typed Chain

```text
Resolved Higgs ontology
-> q_H = 3
-> r_bounce,H = 1/(64*pi)
-> q_A,H = m_H_native * (1 + r_bounce,H)
-> Higgs A-source readout
```

## Replay Values

- m_H_native_MeV: 125077.36096514532
- m_H source: G745c scalar formula output, not measured Higgs target
- r_bounce,H exact: 1/(64*pi)
- r_bounce,H decimal: 0.004973591971621730
- q_A,H_MeV: 125699.44472347321
- q_A,H / m_H exact: 1 + 1/(64*pi)
- q_A,H / m_H decimal: 1.004973591971621838

## Wrong Controls

- [PASS] WC1_q_equals_q_A_rejected
- [PASS] WC2_identity_no_bounce_rejected
- [PASS] WC3_post_multiplier_9_16_rejected
- [PASS] WC4_wrong_q_role_substitution_rejected
- [PASS] WC5_measured_target_selector_rejected
- [PASS] WC6_D2_over_R_as_origin_rejected
- [PASS] WC7_new_Higgs_operator_rejected

## Boundaries Preserved

- CR120 remains a neighboring boundary/intake record; this CR does not rewrite it.
- G748c remains the source direct-weld result; this CR promotes it without mutation.
- No measured Higgs target or observed residual entered the derivation path.

## Verdict Statement

PASS_HIGGS_DIRECT_WELD_PROMOTION. The G748c direct weld is promoted as a typed Courtroom record.
