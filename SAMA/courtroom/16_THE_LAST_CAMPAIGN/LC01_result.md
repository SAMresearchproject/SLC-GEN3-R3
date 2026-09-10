# LC01 Primitive Stack Lock and Replay Register

## Verdict

```text
LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER
```

## What LC01 Does

LC01 locks the primitive stack, source chain, wrong controls, and downstream lane register for The Last Campaign.
It begins the replay campaign. It does not claim any downstream lane has already replayed.

## Locked Stack

- alpha_H = 2
- R = 12
- D = 3
- A0 = 1/(pi*R) = 0.026525823848649222628147293895
- R^2 = 144
- split fraction = 2^-D = 1/8
- retained side = 7/8
- carrier side = 1/8
- bounce lift = D^2/2^D = 9/8
- resolved half-bounce = D^2/2^(D+1) = 9/16
- surface debit = D^2/R = 3/4 = 0.75

## Immediate Consequences Locked For Replay

- split loss = R^2/8 = 18
- retained parent = R^2*(7/8) = 126
- observed Higgs surface = 126 - 0.75 = 125.25
- tensor carrier identity = alpha_H*D^2 = 18
- 18 is carrier-only, not a matter/rest-mass row

## Replay Register

LC02-LC11 are registered in `LC01_downstream_lane_register.csv` and remain pending.

## Wrong Controls

`LC01_wrong_controls.csv` registers 30 controls. LC01 directly rejects primitive mutation, the old 2*pi route restore, carrier/matter promotion, surface-debit confusion, and Higgs carrier/debit swaps. The remaining controls are mandatory guards for lane replay.

## Files

- `16_THE_LAST_CAMPAIGN\LC01_primitive_stack_declared.csv`
- `16_THE_LAST_CAMPAIGN\LC01_source_chain.csv`
- `16_THE_LAST_CAMPAIGN\LC01_downstream_lane_register.csv`
- `16_THE_LAST_CAMPAIGN\LC01_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN\LC01_checks.csv`
- `16_THE_LAST_CAMPAIGN\LC01_primitive_stack_lock.json`
- `16_THE_LAST_CAMPAIGN\LC01_summary.json`
- `16_THE_LAST_CAMPAIGN\LC01_hashes.txt`
