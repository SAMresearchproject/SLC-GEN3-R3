# CR222b PRECOMMIT - Paul Revere Packet Contract

## Scope

Define the Paul Revere packet layer that consumes CR222a:

```text
PR packet = header + route + support inventory + tensor witness + mirror checksum
```

CR222b does not regenerate or modify the physics engine.

## Header

```text
upstream_contract = CR222a
native_stack = Native63 + Bound63
matter_total = 126
support_stack = CarrierLedger81 + Mirror81
support_total = 162
Tier1_NativeStackContract.csv = 0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b
```

## Validity

```text
carrier support = 0300 + 0301 + 0302 + 0304 = 18 + 1 + 9 + 8 = 36
source support  = 0306 + 0307 + 0308 + 0309 + 0310 + 0311 + 0312 + 0313 = 45
unpacked total  = 81
mirror checksum = 0303 = 81
packet total    = 162
```

## Pre-run Hash

Expected `Paul_Revere_PacketContract.csv` hash:

```text
79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009
```
