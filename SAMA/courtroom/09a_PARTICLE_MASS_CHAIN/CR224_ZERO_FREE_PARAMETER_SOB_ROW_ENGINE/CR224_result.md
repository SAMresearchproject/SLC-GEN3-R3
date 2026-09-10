# CR224 Zero-Free-Parameter SOB Row Engine

Result: **CR224_PASS_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE__126_NATIVE_CARD_ROWS__NATIVE_PNG_FIELDS_COMPLETE__DOWNSTREAM_REVEAL_FIELDS_BOUNDARIED__MATCHES_CR222_126_OF_126**

## Direct Answer

The multi-tier engine was built and run. It produced **126 SOB native card
rows** from SAM constants only.

Every tier declares `free_parameters = 0`.

Generated native PNG/card fields include:

- `SOB#`
- `Z`
- `A = Z + N`
- `P = Zp + Nn + Ze`
- quark address `(2Z+N)u + (Z+2N)d + Ze`
- shell/light lane
- action closure lane
- `G(P)`
- `GR(P)=8G(P)`
- `GR(P)=7G(P)+G(P)`

The generated rows match CR222 on compared native fields: **126/126**.

## Z=79 Native Card Row

```text
sob_id      = SOB79
Z           = 79
A           = 197
P           = 79p+118n+79e
quark       = 276u+315d+79e
G(P)        = 732.6966145833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
GR(P)       = 5861.572916666666666666666666666666666666666666666666666666666666666666666666666666666666666666666667
retained 7G = 5128.876302083333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
```

## Boundary

The engine does **not** claim to derive the downstream reveal fields:

- `Gold`
- `Au`
- physical measured mass `196.967`
- physical CLOCK label `stable`

Those columns exist in the SOB row surface, but are blank and marked
`NOT_CONSTANT_DERIVED`. The native row still carries a generated matter value
as `A=197`, and a generated clock/native lane as
`CONSTANT_HALF_WRITE_LANE`.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_sob_rows_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_png_field_reconciliation_Z079.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_field_provenance.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_verification_against_CR222.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_gold_like_native_card_row_Z079.json`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/CR224_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE/HASHES.txt`
