# CR244 Unequal-Pair Typed Forms — Precommit

## Question

CR243 confirmed the five clean-class typed forms but reported `0/42` on
unequal-pair residual quantization against the unit family
`{1/R², 1/(R·S), 1/(D·S²), 1/R, 1/M, 1/L}`. The X-column 2-decimal storage
masked the structure of the Y values which cluster in the `1e-4` range — an
order of magnitude smaller than the smallest unit in that family.

Sean inspected the 42 unequal-pair rows after the CR243 BOUNDARY readout and
proposed two typed lane forms:

```text
ORDINARY (neither a nor b = 9):
   Y = sign(a - b) · (|a - b| + D) / R^4

OCTET-involved (a = 9 or b = 9):
   Y = sign(a - b) · (|a - b| + D^2/R) / R^4
```

CR244 tests whether these forms close the unequal-pair lane against the same
SHA-locked source CR243 used.

## Honest framing of K3 (target hygiene)

The two lane forms were proposed by inspection of the 42 unequal-pair rows
*after* CR243 sealed and reported the BOUNDARY on quantization. K3 status
is therefore **PARTIAL — DECLARED**, same as CR243: the forms are not blind,
and CR244 tests their survival under

  (i)   the full set of 42 rows (not just the rows used to propose them);
  (ii)  substrate-constant perturbations `{R, D}`;
  (iii) an explicit class-trigger swap (use ordinary form on OCTET-involved
        rows and vice versa);
  (iv)  alternate-denominator wrong controls.

The forms passing all four under the locked tolerance discipline is what
CR244 adds beyond the inspection.

## Locked substrate atoms (read-only from CR238)

```text
R = 12        D = 3        S = 8        alpha_H = 2
M = 126       L = 162      Theta = 18   V = 27
kappa = 7117/768            g = 1/64
R^4 = 20736
```

## Locked typed forms

```text
ORDINARY lane:        Y = sign(a - b) · (|a - b| + D)     / R^4
OCTET-involved lane:  Y = sign(a - b) · (|a - b| + D^2/R) / R^4

OCTET-trigger rule:  row is OCTET-involved iff one of {a, b} equals 9.
                     Otherwise the row is ORDINARY.

Sign convention:     sign(a - b) is positive for a > b (positive_debit),
                     negative for a < b (negative_credit).

Notation in the table:
    pair_write[a|antib]   with a != b.
    All 42 unequal-pair rows carry surface_depth = depth=3.
```

The `D^2/R = 9/12 = 3/4` term in the OCTET-involved numerator is the
substrate-typed correction that distinguishes OCTET-charge involvement from
the ordinary lane. It is NOT `D * 2 = 6`.

## Tolerance discipline

The source workbook stores column `X` at 2-decimal precision. A row matches
the typed form if either of:

```text
(i)  X-round match:  round(K_native * Y_typed_form, 2) == X_stored
(ii) Y-tolerance:    |Y_observed - Y_typed_form| <= max(1e-5, 0.005/|K|)
```

Both criteria are reported per row. The verdict uses (i) — X-round match —
as primary, with (ii) reported as the secondary tolerance check.

## Wrong controls

```text
WC-R1   R = 10  (D=3, S=8 fixed)            ⇒ R^4 = 10000  ⇒ break both lanes
WC-R2   R = 11  (D=3, S=8 fixed)            ⇒ R^4 = 14641  ⇒ break both lanes
WC-R3   R = 13  (D=3, S=8 fixed)            ⇒ R^4 = 28561  ⇒ break both lanes
WC-D1   D = 2   (R=12, S=8 fixed)           ⇒ numerator term shifts
WC-D2   D = 4   (R=12, S=8 fixed)           ⇒ numerator term shifts
WC-T1   trigger swap: apply ORDINARY form to OCTET-involved rows and
        OCTET form to ORDINARY rows         ⇒ break both lanes
WC-A1   alternate denominator R^3 = 1728    ⇒ magnitude wrong by factor 12
WC-A2   alternate denominator R^2 * M = 18144 ⇒ magnitude wrong
WC-A3   alternate numerator |a-b| + D^2 = |a-b| + 9 on ORDINARY lane
        (replaces +D with +D^2; should over-predict)
```

Pass condition: each WC degrades the match count below the canonical count.
The match count for "ORDINARY" lane WCs is over 30 rows; the match count for
"OCTET" lane WCs is over 12 rows. WC-T1 is evaluated over all 42 rows.

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  ORDINARY lane:  30/30 X-round match
  S2  OCTET lane:     12/12 X-round match
  S3  WC-R1, WC-R2, WC-R3: each degrades both lanes
  S4  WC-D1, WC-D2: each degrades at least one lane
  S5  WC-T1 (trigger swap): degrades both lanes
  S6  WC-A1, WC-A2, WC-A3: each degrades at least one lane

BOUNDARY conditions:
  B1  S1 and S2 hold
  B2  At least one WC in S3..S6 fails to degrade

FAIL conditions (any one):
  F1  S1 or S2 fails: typed form does not close the lane
  F2  WC-R or WC-D fails to degrade: substrate atom is not actually
      load-bearing for the lane form
  F3  WC-T1 does not degrade: the OCTET-trigger rule is not real
```

Verdict precedence: STRONG_PASS > BOUNDARY > FAIL.

## Outputs (locked file shape)

```text
CR244_summary.json                    — full readout, verdict, WC results
CR244_unequal_pair_predictions.csv    — per-row prediction, X-round, Y-tol match
CR244_wrong_controls.csv              — per-WC per-lane match counts
CR244_input_manifest.csv              — input SHA + row counts
HASHES.txt                            — SHA-256 of all CR244 artifacts
```

## Cryptographic chain (inputs)

```text
CR238_PRECOMMIT.md (substrate spine compaction)
  = 5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR238_result.md (substrate spine compaction)
  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR243_PRECOMMIT.md (clean-class channel typing)
  = 4ea9789806a8bd17e0c314cb6508ee9ab80c0212b49e68b0cdf94fd052d97dc2
CR243_result.md (clean-class STRONG_PASS, unequal-pair BOUNDARY)
  = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR243_input_snapshot.xlsx (same source used by CR243)
  = 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
```

CR244 reads the same SHA-locked snapshot as CR243. CR244 does not modify
CR243; CR243 BOUNDARY remains as audit trail for the precommit unit family
that did not include `1/R^4`.

## Falsifiers

```text
F1   Either lane fails on at least one of its 42 / 12 / 30 rows: the
     proposed typed form is wrong for that lane.
F2   WC-R1..R3 do not all degrade: R^4 is not actually the denominator.
F3   WC-D1..D2 do not all degrade at least one lane: D is not in the
     numerator the typed form ascribes.
F4   WC-T1 trigger swap preserves match rate: the OCTET-trigger rule is
     not real — the +D vs +D^2/R distinction is row-coincidental.
F5   WC-A1..A3 alternate denominators or numerators pass: the locked
     R^4 + (|a-b|+D) / (|a-b|+D^2/R) typed form is not uniquely selected.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, both lane forms, OCTET-trigger
rule, tolerance discipline, wrong controls, verdict gates, falsifiers all
locked above the line.
