# CR222 Carrier Ledger 12 Plus 1 Result

**Result class:** `CR222_PASS_CARRIER_LEDGER__12_UNPACKED_81__0303_MIRROR__162_CLOSURE`

**Checks:** 18/18

**Tier1_CarrierLedger81.csv SHA-256:** `5de140e2d87cc1f9b04eaec4a669c7869128fc24f815bb237e2e45123967f9e1`

## Verdict

The corrected support ledger closes cleanly:

```text
18 + 1 + 9 + 8 + (1 + 2 + 3 + 4 + 6 + 8 + 9 + 12) = 81
0303 = 81
81 + 81 = 162
```

`QP093A-0303` is kept outside the twelve unpacked modes as the mirror/checksum
row. `QP093A-0306:p=1` is restored inside the eight source-support modes.

## Tensor Role

The tensor carrier locks the clean ratios:

```text
18/36  = 1/2
18/81  = 2/9
18/162 = 1/9
```

So the tensor row is recorded as timing / gravity / witness floor, not message
payload and not promoted matter.

## Outputs

- `Tier1_CarrierLedger81.csv`
- `CR222_mirror_closure_0303.csv`
- `CR222_support_closure_162.csv`
- `CR222_ledger_totals.csv`
- `CR222_wrong_controls.csv`
- `CR222_validation_against_CR119_support.csv`
- `CR222_validation_against_CR214_complement.csv`
- `CR222_checks.csv`
- `CR222_summary.json`
- `HASHES.txt`
