# CR278 — Neutron Rule Consolidation

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_CONSOLIDATION_CR (documentation + re-verification, no new fits)
**Downstream of:** CR238 + CR240 + CR245 + CR247 + CR248 + CR274
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

**STATUS: DRAFT — showing to Sean before sealing.**

---

## Question

The neutron rule for nuclear binding is sealed in five separate CRs:

- CR240 identifies the rest-mass channel `Q_mass = 4·A·κ` (STRONG_PASS)
- CR247 seals the two-particle inverse `Φ(Z,N) = Z·φ_balanced + (N-Z)·φ_excess` (STRONG_PASS on 6/6 identities, 69 rows)
- CR248 Phase A extends to the four-particle spine {proton, balanced_neutron, excess_neutron, electron} with excess neutron carrying `dQ = 7093/192` (STRONG_PASS on 6 identities at exact Fraction)
- CR245 derives the asymmetry identity `(Q_mass − Q_sub)²/Q_mass = (N−Z)²/A · 7093²/(192·7117)` theorem-grade (71/71 rows zero deviation)
- CR274 verifies the tensor cipher `F_conn = (N−Z)·(7093/192)` exact on all 55 training isotopes (G0)

Each piece is sealed at its own grade. What is missing is a single sealed
artifact that assembles them into one statement — "this is the neutron rule
for binding" — and re-verifies the assembled statement end-to-end on the
sealed dataset in one pass.

Can we consolidate the five sealed pieces into a single CR that:

  (a) States the neutron rule in one place, with every typed quantity named,
  (b) Re-verifies each of the five component identities under one runner on
      one dataset at Fraction precision (documentation + regression, not
      re-derivation), and
  (c) Runs two wrong controls that swap or eliminate the balanced/excess
      distinction, confirming the split is load-bearing?

## Honest Framing

**K3 status: STRUCTURAL CONSOLIDATION — no new derivation, no new fit, zero
free parameters introduced.** Every quantity this CR verifies has already
been sealed at STRONG_PASS or theorem-grade in an upstream CR. This CR
gathers them into one runner, one dataset, one result artifact so
downstream work (Vol II §4, Vol III, future public-facing derivations)
can cite the rule with a single hash rather than five.

**No claim of new physics.** The rule is discovered, sealed, and now
consolidated. If any gate fails, that means one of the upstream sealed
CRs failed to reproduce under the consolidation runner — a regression
signal, not a new falsification.

## The Neutron Rule (stated in one place, for citation)

A nucleon in the SAM binding ledger occupies exactly one of four typed
slots. Each slot carries a signed rational vector
`φ = (u, d, e, Q_mass, Q_sub, dQ)` in the CR238 substrate atoms:

```text
proton              φ_p  = ( 2, 1, 0,  4·κ,   8·κ,          −4·κ         )
balanced neutron    φ_nb = ( 1, 2, 0,  4·κ,   0,            +4·κ         )
excess   neutron    φ_ne = ( 1, 2, 0,  4·κ,   1/8,          +7093/192    )
electron            φ_e  = ( 0, 0, 1,  0,     0,             0           )
```

Substrate atom references (locked from CR238):

```text
κ  = 7117/768    (rest-mass channel coefficient, C-12 anchored)
g  = 1/64        (excess-neutron source-support fee)
GAP = 7093/192   (excess-neutron mass-vs-substrate gap)
D_LOCKED = 7093² / (192·7117) = 50310649 / 1366464 = 36.81813  (CR245 theorem-grade)
```

For a nucleus (Z, N) with `A = Z + N`, the population vector is
`n_p = Z, n_nb = Z, n_ne = N − Z, n_el = Z` (electrons balance the
proton charge for the neutral atom). The six identities that close on
this population are:

```text
u_total    = 2Z + N                          (Rule 1: source count u)
d_total    = Z + 2N                          (Rule 2: source count d)
e_total    = Z                               (Rule 3: source count e)
Q_mass     = 4·A·κ                           (Rule 4: rest-mass channel, CR240)
Q_sub      = 8·Z·κ + (N−Z)·(1/8)             (Rule 5: source-coupling asymmetry)
dQ_total   = (N−Z)·(7093/192)                (Rule 6: gap identity, CR274 G0)
```

And the derived identity locked theorem-grade at CR245:

```text
(Q_mass − Q_sub)² / Q_mass  ≡  (N−Z)²/A · 7093²/(192·7117)
                            =  (N−Z)²/A · D_LOCKED
```

**This is the neutron rule.** Four slots, six identities, one derived
theorem, all exact rational arithmetic.

## Locked Inputs (frozen SHA256)

| field | sha256 | description |
| --- | --- | --- |
| CR248 train_lane_a.csv | `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc` | 35 nuclei with (Z, N, A, atomic_mass_u) |
| CR248 test_holdout.csv | `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8` | 20 nuclei, all N≥Z |
| CR274 residuals.csv | `ec71a6c2f8cf5bed0f1ec64efb7f57a394e6cef8f9ad3fe268d528009a8476e5` | 55-row reference for G5 cipher check |

Together the 35 + 20 = 55 rows are the same set CR274 used and are all
N ≥ Z by construction.

## Locked Pipeline

```text
Step 1: verify precommit hash + input file hashes + forbidden-file guard.

Step 2: parse CR248 train + test → 55 nuclei (Z, N, A).

Step 3: for each nucleus, compute the six identities at Fraction precision
        using the four-particle spine defined above. Verify equality on
        every row.

Step 4: compute CR245's derived asymmetry identity
        `(Q_mass − Q_sub)² / Q_mass` and `(N−Z)²/A · D_LOCKED` at Fraction
        precision. Verify exact equality on every row.

Step 5: compute CR274's cipher identity `F_conn = (N−Z)·(7093/192)`
        at Fraction precision. Verify exact equality on every row.

Step 6: run wrong control W1 — swap φ_balanced and φ_excess vectors.
        With the swap, at least one of the six identities must fail on
        every N > Z row (rows where excess neutrons exist).

Step 7: run wrong control W2 — eliminate the balanced/excess distinction,
        assign every neutron `dQ = 7093/192`. Under this rule, the
        `dQ_total` identity should read `N·(7093/192)` instead of
        `(N−Z)·(7093/192)`, failing on every N > 0 row where Z > 0.

Step 8: emit result.md with the rule stated, per-row verification
        summary, and wrong-control audit. Write HASHES.txt.
```

## Sealed PASS Gates

```text
G1  Rest-mass channel: for all 55 rows, Q_mass(Z, N) = 4·A·κ exact under
    Fraction arithmetic. (Regression on CR240.)

G2  Source-coupling asymmetry: for all 55 rows,
    Q_sub(Z, N) = 8·Z·κ + (N−Z)·(1/8) exact under Fraction arithmetic.

G3  Four-particle spine: all six identities (u, d, e, Q_mass, Q_sub, dQ)
    close exactly on all 55 rows under Fraction arithmetic.
    (Regression on CR248 Phase A.)

G4  CR245 asymmetry identity: `(Q_mass − Q_sub)² / Q_mass` equals
    `(N−Z)²/A · 7093²/(192·7117)` at Fraction precision on all 55 rows.
    (Regression on CR245 theorem-grade.)

G5  CR274 gap identity: `F_conn = (N−Z)·(7093/192)` exact on all 55 rows.
    (Regression on CR274 G0.)

G6  Wrong control W1 (swap balanced ↔ excess): at least one of the six
    identities fails on every N > Z row. If W1 passes any N > Z row, the
    balanced/excess distinction is not load-bearing there — CR fails.

G7  Wrong control W2 (all neutrons carry the excess dQ = 7093/192): the
    dQ_total identity fails on every row with N > Z AND Z > 0. If W2
    passes any such row, the balanced/excess distinction is spurious
    for the gap identity — CR fails.

G8  Precommit hash + input hashes verified; forbidden-file open() guard
    not tripped.

PASS      iff G1 AND G2 AND G3 AND G4 AND G5 AND G6 AND G7 AND G8 all hold.

BOUNDARY  iff G1..G5 all hold (identities reproduce) but one of {G6, G7}
          shows insensitive wrong-control coverage.

FAIL      iff any of G1..G5 fail (regression on a sealed upstream) OR G8
          fails (whitelist/hash).
```

## Reported Evidence (not gated)

```text
E1  Per-row identity verification table (55 rows × 6 identities + CR245
    derived + CR274 gap), all showing "exact" under Fraction arithmetic.

E2  Wrong-control audit: for W1 and W2, count the rows where each identity
    fails, and show the first-few-row detail for reader inspection.

E3  Consolidation statement, formatted for citation by downstream CRs
    and Vol II §4.

E4  Cross-reference table linking each of the six identities back to its
    original sealed CR (CR240 for Rule 4, CR247/CR248 for Rules 1-3 + 5,
    CR248 Phase A for Rule 6, CR245 for the derived asymmetry, CR274 G0
    for the gap identity).
```

## Free Parameters Introduced

**Zero.** Every quantity in this CR is either a typed constant from
CR238 (κ, g, GAP, D_LOCKED) or a per-nucleon vector from CR248 Phase A
(φ_p, φ_nb, φ_ne, φ_e). Nothing is fitted, nothing is calibrated. This
CR is documentation + regression + wrong-control audit only.

## Rule-9 Line

```text
This CR could have falsified the claim that the neutron rule for binding
— four typed nucleon slots with balanced vs excess split, six identity
closures, and the CR245 asymmetry derivation — reproduces bit-exactly
under one runner on the sealed 55-row dataset, and that the balanced/excess
distinction is load-bearing under two wrong controls. It could have
failed by:
  (i)   any of the five upstream sealed identities failing to reproduce
        (regression signal on CR240, CR247, CR248, CR245, or CR274);
  (ii)  wrong controls not falsifying any row (insensitive control,
        meaning the split is not load-bearing where the CR claimed);
  (iii) whitelist / hash gate tripping.
It could NOT have failed by any new fitted coefficient missing its
target, because no new fitted coefficients exist in this CR.
```

## What This CR Seals

If PASS: the neutron rule for binding has a single citable handle at
`CR278_NEUTRON_RULE_CONSOLIDATION`. Vol II §4, Vol III, and any downstream
public-facing derivation can cite one hash and reference one page for the
rule that CR240 / CR245 / CR247 / CR248 / CR274 sealed piecemeal.

The wrong controls make the balanced/excess distinction structurally
falsifiable on this dataset — a reader can verify that swapping the two
neutron types breaks the identities on every N > Z row.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR238 (typed channel table, κ + g locked) | per branch HASHES |
| CR240 (rest-mass channel) | per branch HASHES |
| CR245 (asymmetry theorem-grade) | per branch HASHES |
| CR247 (two-particle inverse) | per branch HASHES |
| CR248 (four-particle spine, Phase A STRONG_PASS) | precommit `7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa` |
| CR274 (gated nuclear-readout, G0 cipher exact) | precommit `c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9` |
| Stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
