# CR092 HIGGS_SECTOR (Mass Slice)

## Test Class

```text
OBSERVATIONAL_COMPARISON_OF_LOCKED_09A_PREDICTION_AGAINST_CERN_HIGGS_MASS_ANCHORS
```

## Preflight

```text
13 is observational. 09a's locked Higgs mass prediction is read verbatim
from 09a/CR062a row 15. It is compared to ATLAS, CMS, and the official
ATLAS+CMS Run-1 combined Higgs mass measurement under the four-pillar
blindness protocol.

This precommit handles the Higgs MASS slice of the CR092 scope.
Higgs branching-ratio signal strengths (H004..H015 in CR090 inventory)
are not addressable at this CR because 09a's evidence ledger does not
expose direct numeric BR predictions. Those rows are labeled
INFORMATION_INSUFFICIENT_AT_THIS_CR and deferred.
```

## Anchor Rows Considered

```text
H001 ATLAS    Higgs boson mass
H002 CMS      Higgs boson mass
H003 ATLAS+CMS Run-1 combination Higgs boson mass
H004..H015    Higgs branching-ratio signal strengths    INFORMATION_INSUFFICIENT_AT_THIS_CR
```

## Observation Band (Guidance)

```text
Higgs mass    band = 300 MeV    (~0.24% of central; driven by ATLAS-CMS
                                  disagreement 270 MeV)
```

## Pass Conditions (Reporting Completion)

Same as CR091. The runner emits predictions hashed before envelope is
opened, evidence rows with full sha256 + utc fields, summary, and result.

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
