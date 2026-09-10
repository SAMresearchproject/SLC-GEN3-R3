# CR222e PRECOMMIT - Paul Revere Warning Emission Gate

## Scope

Define when a sealed Paul Revere packet becomes an emitted warning write.
This consumes CR222a, CR222b, CR222c, and CR222d. It does not regenerate the
physics engine.

## Rule

```text
VALID_PR_WARNING = SEALED_PACKET + G_protocol=1 + A_leak>=A_side
A_side = 1/24
```

Emission is allowed only after the warning gate:

```text
qA > 0
T = qA/8
W = 7qA/8
```

Support inventory alone cannot emit.

## Pre-run Hash

Expected `CR222e_emission_state_machine.csv` hash:

```text
a79ee4b0d5519c85eb6edded7f96e698b51a274b56e1e64f2b160c5ef211f2d7
```
