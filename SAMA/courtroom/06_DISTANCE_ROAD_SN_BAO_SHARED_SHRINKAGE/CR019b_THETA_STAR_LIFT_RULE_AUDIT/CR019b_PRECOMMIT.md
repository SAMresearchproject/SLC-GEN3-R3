# CR019b — θ_* Substrate-Lift Rule Audit

**Branch:** 06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE
**Classification:** AUDIT_CR (downstream of CR019@06 and CR249a@09a)
**Sealed by:** Sean Brady, 2026-06-29
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

CR019@06 sealed `100·θ_* = 1.04740` (SAM) vs `1.04110` (Planck 2018), a
+0.605% deviation. Planck's measurement σ on this observable is ≈
0.029%, so SAM and the Planck measurement are formally 20σ apart — the
highest-significance SAM-vs-data gap in the discrimination map (CR004@21).

The 09a binding work (CR249a + CR251 sealed) discovered a structural
lift-fee rule that fixed nuclear binding: bigrade-class substrate
quantities {1, 2, 3, 4, 6, 8, 9, 12} pay a `L_p = p + p²/R²` lift fee;
the carrier tensor Θ = 18 (the first overflow past R) does **not** pay
the fee. Applying this rule incorrectly (lifting Θ) broke binding;
removing Θ's lift fixed it, and `c_A = 1/(S·L) = 1/1296` landed within
0.44% (CR249a) and was statistically isolated from `1/(S·R²) = 1/1152`
at >5σ (CR251) via the bounce factor `L/R² = 9/8`.

The audit tests Sean Brady's hypothesis (2026-06-29):

> If the same lift-fee rule that fixed binding (Θ exempt; bigrade
> {1,2,3,4,6,8,9,12} lifted by `+p²/R²`) is applied to the substrate
> atoms in CR019's θ_* derivation, does the +0.605% θ_* gap close?

## Pre-registered hypotheses tested

CR019's substrate atoms (from CR019_runner.py lines 22-29):

```python
A_0 = 1/(12*pi)                         # uses R = 12 (bigrade)
OMEGA_M_SAM = 1/pi                      # = R * A_0 (R appears twice; cancels)
CHI = (8/3) * A_0                       # uses S = 8 (bigrade), d = 3 (bigrade)
OMEGA_B_SAM = 2 * A_0 * (1 - CHI)
```

**Θ = 18 does not appear explicitly in CR019's substrate inputs.** The
bigrade atoms that DO appear are R = 12, S = 8, d̂ = 3, d̂² = 9.

Pre-registered hypotheses (each candidate is a single substrate-lift
correction applied to the canonical Ω_m and/or Ω_b):

```text
H1: Lift R in A_0 denominator only (R -> L_R = 13)
    A_0_lifted = 1/(L_R*pi),  Omega_m = R*A_0_lifted = 12/(13*pi)

H2: Lift R consistently (in both A_0 and Omega_m factor)
    Omega_m unchanged (R/R cancellation), Omega_b shifts via chi

H3: Lift S and d in chi only
    chi_lifted = (L_S/L_d)*A_0

H4: Lift ALL bigrade atoms throughout

H5: Free Omega_m grid search (parameter-by-parameter for what closes theta_*)

H6: Joint Omega_m, Omega_b grid search

11 additional substrate-form candidates listed in the runner.

In every case: Theta = 18 is NOT lifted (per the binding-work rule).
One wrong-control candidate (Theta/(L_18*pi)) lifts Theta to verify
the binding finding from the opposite direction.
```

## Gates

```text
PASS:
  At least one substrate-lift correction (single-atom or simple compound)
  closes 100*theta_* gap to <= 0.1% AND keeps ell_A AND r_d each
  <= 1% from Planck.

BOUNDARY:
  A correction closes theta_* significantly (e.g., gap drops below 0.1%)
  but breaks ell_A or r_d beyond 1%.

FAIL (in audit sense — informative):
  No substrate-lift correction closes theta_* without breaking other
  observables. Identifies the gap as NOT in the substrate-lift layer;
  likely in the Hu-Sugiyama / EH fitting-formula error budget.
```

This is an audit CR. The "FAIL" outcome is informative — it eliminates
a candidate mechanism cleanly and points at where the 0.605% gap
actually lives. There is no scientific failure mode; the worst case is
"hypothesis ruled out, mechanism identified."

## What this CR seals

A definitive test of whether the 09a binding-work lift rule applies to
CR019@06's θ_* derivation. The outcome (whichever way it goes) becomes
the audit-trail record for the largest SAM-vs-data discrepancy in the
substrate grammar.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR019@06 sealed PASS | precommit `ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da` |
| CR249a@09a A-kernel binding geometry | sealed (per 09a HASHES.txt) |
| CR251@09a bounce-aware asymmetry isolation | sealed (per 09a HASHES.txt) |
| CR229@09a inclusion-exclusion identity | per 09a HASHES.txt |
| CR005@21 Θ-overflow + QNM derivation | precommit `624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b` |
| CR004@21 discrimination map | precommit `e519e7c5b8be99540c5c6984079e91f4e56b524d9b9c87e43baabd3f5f61933a` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
