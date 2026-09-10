# CR261 — Pair-Write Binding Extension — RESULT

```text
verdict           : BOUNDARY
classification    : BINDING_CLOSURE_EXTENSION_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-30
precommit_hash    : 5b2d07b5c1447c39c221e4a53febeff6b379acfae6788cb675970017acfe2001
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
free_parameters_introduced : 4   (a, b, c, e — fitted; d locked from CR245)
```

## Headline

The named gap in CR248 (linear B_u model insufficient at 24.52 MeV RMS) is
closed by extending the four-particle algebraic decomposition with the
five-term BW pair-write form, using CR245's structurally-derived asymmetry
coefficient `d = 7093²/(192·7117)` locked theorem-grade.

```text
CR248 linear:   train RMS = 24.52 MeV    (BOUNDARY)
CR261 BW fit:   train RMS = 5.555 MeV   (4.41× improvement)
                test  RMS = 8.574 MeV
                SOB126 (Z<119) RMS = nan MeV
```

## Locked model (asymmetry derived; four fitted)

```text
B_u(Z,N,A) = a · A                              ← volume      (fit)
            − b · A^(2/3)                       ← surface     (fit)
            − c · Z(Z−1)/A^(1/3)                ← Coulomb     (fit)
            − d · (N−Z)²/A                      ← asymmetry   (LOCKED CR245)
            − e · δ_pair · A^(−1/2)             ← pairing     (fit)

d = 7093² / (192·7117) = 50310649 / 1366464 ≈ 36.8242
    derived from (Q_mass − Q_sub)² / Q_mass = (N−Z)²/A · 7093²/(192·7117)
    sealed CR245@09a
```

| coefficient | fitted value (MeV) |
| --- | ---: |
| a (volume)    |    +8.1741 |
| b (surface)   |   +19.7669 |
| c (Coulomb)   |    +0.5854 |
| d (asymmetry) |   +36.8181  (LOCKED) |
| e (pairing)   |   -41.8907 |

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| Phase A | CR248 four-particle algebra regression | PASS |
| G1 | CR245 asymmetry identity exact on all rows | PASS |
| G2 | Lane A train RMS ≤ 4.0 MeV | FAIL |
| G3 | Lane A test  RMS ≤ 5.0 MeV | FAIL |
| G4 | ≥ 5× improvement over CR248 (24.52 MeV linear) | FAIL |
| G5 | Anchor cases within 5 MeV residual | FAIL |
| G6 | Precommit hash + forbidden-file guard | PASS |

## Anchor cases

| isotope | B_u observed | B_u predicted | residual |
| --- | ---: | ---: | ---: |
| C-12  | +0.000 | -1.098 | -1.098 MeV |
| C-13  | -3.125 | -13.325 | -10.200 MeV |
| Au-197 | +31.141 | +36.807 | +5.666 MeV |

## Jerroldium frontier (Z = 119–126) — predicted B_u under fitted model

| Z | symbol | N | A | B_u_pred (MeV) |
| ---: | --- | ---: | ---: | ---: |
| 119 | Uue | 218 | 337 | -454.677 |
| 120 | Ubn | 230 | 350 | -577.668 |
| 121 | Ubu | 121 | 242 | -156.267 |
| 122 | Ubb | 132 | 254 | -93.064 |
| 123 | Ubt | 143 | 266 | -67.194 |
| 124 | Ubq | 155 | 279 | -56.726 |
| 125 | Ubp | 166 | 291 | -71.396 |
| 126 | Ubh | 178 | 304 | -105.159 |

These are reported predictions; no observation exists to compare. The
Z = 119–126 frontier window is the natural target for a forthcoming
forecast-lock CR (analogous to the DUNE Δm² = 35 and LISA ω_R·M = 3/8
locks).

## Verdict statement

CR261 verdict: **BOUNDARY**. See gates section for failure details.

`CR261_BOUNDARY_PAIR_WRITE_BINDING_EXTENSION_CR248_GAP_CLOSED_BY_FIVE_TERM_BW_WITH_CR245_ASYMMETRY_LOCKED_THEOREM_GRADE_FOUR_PARAMETERS_FIT_ASYMMETRY_DERIVED_TRAIN_RMS_5.55_TEST_RMS_8.57_SOB126_PROPAGATION_AND_JERROLLDIUM_FRONTIER_EMITTED`
