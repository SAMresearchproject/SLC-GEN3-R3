# CR222 PRECOMMIT - Carrier Ledger 12 Plus 1

## Scope

Generate the support ledger from SAM constants and the corrected row-order
selector:

```text
alpha_H = 2
D = 3
R = 12
Pi = (1, 2, 3, 4, 6, 8, 9, 12)
```

## Generator

Twelve unpacked modes:

```text
carrier modes        = 18 + 1 + 9 + 8 = 36
source support modes = 1 + 2 + 3 + 4 + 6 + 8 + 9 + 12 = 45
unpacked total       = 36 + 45 = 81 = D^4
```

`QP093A-0303` is not one of the twelve unpacked modes. It is the separate
mirror/checksum row:

```text
0303 = 81 = D^4
closure = 81 + 81 = 162 = 2D^4
```

`QP093A-0306`, source packet `p=1`, is required inside the eight source-support
modes.

## Downstream Validation

CR119 and CR214 are read only after construction to verify row IDs, partitions,
operator classes, and native masses. CR219 is read only to confirm the support
rows are absent from the 126 promoted matter rows.

## Wrong Controls

```text
missing 0306:p=1       -> 161
restoring 0305 duplicate -> 163
omitting 0303 mirror   -> 81
```

## Pre-run Hash

Expected generated `Tier1_CarrierLedger81.csv` hash:

```text
5de140e2d87cc1f9b04eaec4a669c7869128fc24f815bb237e2e45123967f9e1
```
