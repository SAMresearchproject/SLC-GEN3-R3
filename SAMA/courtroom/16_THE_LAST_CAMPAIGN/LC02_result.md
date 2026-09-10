# LC02 Higgs Closed-Form Replay

## Verdict

```text
LC02_PASS_HIGGS_CLOSED_FORM_REPLAY_FROM_LOCKED_PRIMITIVE_STACK
```

## Replay Result

LC02 replays the Higgs closed form from the LC01 locked primitive stack:

```text
H_native = R^2*(1 - 2^-D)
         = 144*(7/8)
         = 126

H_reveal = H_native - D^2/R
         = 126 - 9/12
         = 501/4
         = 125.25
```

The replay also preserves the split identities:

```text
R^2 * 2^-D = 18
alpha_H * D^2 = 18
carrier side = 1/8
retained side = 7/8
surface debit = 3/4
```

## Claim Grade

This is a downstream replay pass from the theorem-grade primitive stack. It does not relabel the older CR120 qp091 target-visible chronology as forward-blind. The CR120 caveat is preserved in `LC02_target_visibility_and_claim_grade.csv`.

## Wrong Controls

13/13 wrong controls were rejected, including no debit, D/R, D^2/R^2, D=2, D=4, R=10, R=24, restoring the old 2*pi q-split route, and swapping carrier/bounce quantities into the surface-debit slot.

## Files

- `16_THE_LAST_CAMPAIGN\LC02_higgs_replay_chain.csv`
- `16_THE_LAST_CAMPAIGN\LC02_source_chain.csv`
- `16_THE_LAST_CAMPAIGN\LC02_target_visibility_and_claim_grade.csv`
- `16_THE_LAST_CAMPAIGN\LC02_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN\LC02_checks.csv`
- `16_THE_LAST_CAMPAIGN\LC02_higgs_closed_form_replay_lock.json`
- `16_THE_LAST_CAMPAIGN\LC02_summary.json`
- `16_THE_LAST_CAMPAIGN\LC02_hashes.txt`
