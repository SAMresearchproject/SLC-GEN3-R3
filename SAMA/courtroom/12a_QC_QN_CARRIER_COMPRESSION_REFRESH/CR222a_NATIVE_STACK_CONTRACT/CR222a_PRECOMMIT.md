# CR222a PRECOMMIT - Native Stack Contract

## Scope

Lock the stack that the Paul Revere protocol layer consumes:

```text
Native63 + Bound63 + CarrierLedger81 + Mirror81
```

This CR does not generate new physics rows. It verifies and records the passed
CR220, CR221, and CR222 products as a contract.

## Dimension Discipline

```text
matter engine:     63 + 63 = 126 rows
support integrity: 81 + 81 = 162 ledger value
```

These are separate dimensions. The contract rejects flattening them into one
combined row count.

## Paul Revere Boundary

PR may consume this stack as a protocol layer:

```text
message route + support inventory + tensor witness + ledger checksum
```

PR may not claim to generate the matter rows or turn support rows into matter.

## Pre-run Hash

Expected `Tier1_NativeStackContract.csv` hash:

```text
0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b
```
