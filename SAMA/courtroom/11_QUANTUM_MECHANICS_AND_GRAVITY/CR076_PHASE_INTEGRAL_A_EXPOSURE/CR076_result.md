# CR076 Phase Integral / A Exposure

## Verdict
```text
CR076_BOUNDARY
```

## Reason
```text
integral form not explicit; A_exposure+A_route+phase functional present
```

## Phase Summary
```text
P1 seal+hash         verified=242
P2 A_exposure        hits=5
P3 A_route           hits=3
P4 phase functional  hits=4
P5 integral form     hits=0
P6 fit-scan          fail=0
P7 G286-class        present=True
P8 wrong controls    passed=6/6
```

## Rule-9
This test could have falsified the claim that SAM's A_exposure +
A_route + phase functional reproduces the phase integral form
Δφ = ∫A ds / ℏ in substrate-count language with zero free parameters.
