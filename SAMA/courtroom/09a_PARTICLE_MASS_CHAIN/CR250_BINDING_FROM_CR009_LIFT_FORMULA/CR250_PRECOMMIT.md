# CR250 — Binding from CR009 Lift Formula on CR247 Phi Decomposition

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-25
**Input dataset:** [CR242_binding_dataset.csv](../CR242_SAM_BINDING_CURVATURE_DERIVATION/CR242_binding_dataset.csv) (71 nuclei AME2020-derived)
**Test corpus:** 69 nuclei with N ≥ Z (CR247 scope; H-1 and He-3 with N < Z reserved)
**Provenance backing:**
- CR009 PASS — connection-fee triadic `(R + sign·(q+D))/R` and pair `(q+D)/R⁴` sealed at K1 on qp093a catalog
- CR247 STRONG_PASS — `Phi(Z, N) = Z·phi_balanced + (N − Z)·phi_excess_neutron` exact 69/69
- CR005 PASS — zero physics-fit across 76 upstream substrate constants
- CR238 substrate atoms (R, D, S, α_H, Θ, ℱ, V, M, L, κ, g, μ_Q) all sealed

**This CR's discipline:** zero new candidate rules. The formula below is the
single most direct algebraic composition of CR009's sealed lift form with
CR247's sealed phi decomposition, with **every constant traceable to a sealed
upstream CR**. No fitted parameters, no candidate search, no outside-data
comparison.

---

## Question

Per Sean's 2026-06-24 framing and the cascade derivation in
`C:\VS\chat_history\Chat5-QGC_Subtrate_Shape.md` lines 14098–14596:

> "The 'binding energy' of conventional physics IS the closure fee the
> substrate charges, expressed in mass-equivalent units."
> — Chat5 line 14588

CR009 sealed the per-connection fee on stable particles (the lift formula).
CR247 sealed the per-nucleus phi decomposition into Z balanced positions
and (N − Z) excess-neutron positions, with each position carrying a typed
channel-gap dQ in CR238 substrate units.

**Direct question:** when the CR009 lift formula is applied to each CR247
phi position via that position's sealed dQ value, and the per-position
contributions are summed per CR247 Block G's identity
`B_u(Z, N) = Z·s_b + (N − Z)·s_e`, what binding curvature does the
substrate algebra natively produce — and how does it relate to the AME2020
observed B_u?

This is not a fitting test. There are no free parameters and no candidate
rules to search. CR250 reports the residual shape that the sealed
upstream algebra produces, so the substrate can speak for itself.

---

## Sealed formula (above the line)

```text
Substrate atoms (all sealed upstream):
  R       = 12              (CR238)
  D       = 3               (CR238)
  S       = 8               (CR238)
  kappa   = 7117/768        (CR221)
  g       = 1/64            (CR221)
  R4      = R^4 = 20736
  mu_Q    = 192/7117  u     (CR240; Q-unit → atomic-mass-unit conversion)

CR247 sealed phi positions (verbatim from CR247 result.md lines 30–32):
  phi_balanced       = (u=3, d=3, e=1, Q_mass = 8*kappa,  Q_sub = 8*kappa,  dQ = 0)
  phi_excess_neutron = (u=1, d=2, e=0, Q_mass = 4*kappa,  Q_sub = 1/8,      dQ = 4*kappa - 1/8 = 7093/192)

CR009 sealed pair-connection lift form (verbatim from CR009 result.md lines 33–36 and 125–131):
  For n_conn = 1, BOUND_COLOR_PAIR class:
    M_obs / M_nat = 1 + sign · (q_abs + D) / R^4

  The pair lift fraction is therefore:  (q_abs + D) / R^4
  applied to the substrate Q-channel and converted to atomic mass units via mu_Q.

CR250 application (no fitted constants; no candidate selection):
  Each CR247 phi position represents a substrate-position carrying its own dQ.
  An excess neutron joins a balanced bundle via one substrate-atom connection
  (n_conn = 1 = single-connection event in the qp093a operator-class taxonomy).
  The connection charges the CR009 pair lift, with the position's dQ playing
  the role of the substrate q quantum being routed.

  s_b  = (dQ_b + D) / R^4 * mu_Q   evaluated at  dQ_b = 0
       = D / R^4 * mu_Q
       = 3 / 20736 * 192 / 7117
       = 576 / (20736 * 7117)
       = 1 / (36 * 7117)
       = 1 / 256212
       ≈ 3.903e-6 u  per balanced position

  s_e  = (dQ_e + D) / R^4 * mu_Q   evaluated at  dQ_e = 7093/192
       = (7093/192 + 3) / 20736 * 192 / 7117
       = (7093/192 + 576/192) / 20736 * 192 / 7117
       = (7669/192) / 20736 * 192 / 7117
       = 7669 / (20736 * 7117)
       ≈ 5.196e-5 u  per excess neutron

  B_u_pred(Z, N) = Z * s_b + (N - Z) * s_e          (CR247 Block G identity)

Notes on each design choice:
  - Pair depth (R^4) and not triadic depth (R^1) is selected because adding a
    nucleon to an existing nucleus is a single-connection event; CR009's pair
    branch covers n_conn = 1 BOUND_COLOR_PAIR.
  - dQ_b = 0 means the balanced position has Q_mass = Q_sub; per the CR009
    pair form, the lift at q = 0 is D/R^4 (the substrate's bare-connection floor,
    the "D term" CR009 wrong control WC-3 confirmed is load-bearing).
  - dQ_e = 7093/192 is the sealed CR247 channel gap per excess neutron.
  - mu_Q converts substrate Q-units back to atomic mass units per CR240.
```

**Zero free parameters. Zero candidate rules. Two algebraic terms,
both derivable from sealed CR238/CR240 atoms applied to sealed CR247
phi positions via sealed CR009 lift form.**

---

## What the formula predicts before the runner sees the dataset

Hand-evaluated predictions on six sentinel rows (locked above the line
so the runner cannot fit them):

```text
Au-197 (Z=79, N=118, N-Z=39):
  B_pred = 79 * 3.903e-6 + 39 * 5.196e-5
         = 3.083e-4 + 2.026e-3
         = 2.334e-3 u
         ≈ 2.175 MeV

  B_obs (from CR242 dataset) ≈ 0.0334 u ≈ 31.1 MeV.
  Predicted/observed ratio ≈ 0.070, undershoot factor ≈ 14.3.

C-12 (Z=6, N=6, N-Z=0):
  B_pred = 6 * 3.903e-6 + 0
         = 2.34e-5 u
         ≈ 0.022 MeV

  B_obs is structurally 0 in the AMU convention (C-12 defines the unit).

N-14 (Z=7, N=7, N-Z=0):
  B_pred = 7 * 3.903e-6 + 0
         = 2.73e-5 u
         ≈ 0.025 MeV

  B_obs ≈ -0.003074 u ≈ -2.86 MeV (negative — m_obs > A*u).

C-14 (Z=6, N=8, N-Z=2):
  B_pred = 6 * 3.903e-6 + 2 * 5.196e-5
         = 2.34e-5 + 1.039e-4
         = 1.273e-4 u
         ≈ 0.119 MeV

  B_obs ≈ -0.003242 u ≈ -3.02 MeV.

He-4 (Z=2, N=2, N-Z=0):
  B_pred = 2 * 3.903e-6 = 7.81e-6 u ≈ 0.007 MeV
  B_obs ≈ -0.0026 u ≈ -2.43 MeV.

U-238 (Z=92, N=146, N-Z=54):
  B_pred = 92 * 3.903e-6 + 54 * 5.196e-5
         = 3.59e-4 + 2.806e-3
         = 3.165e-3 u
         ≈ 2.95 MeV

  B_obs ≈ -0.051 u ≈ -47.3 MeV (very negative in AMU baseline).
```

**Pre-run honest reading:** This minimal CR009+CR247 composition produces
a curve that is **strictly positive and monotonic in (N − Z)** with a small
positive baseline scaling as Z. The observed B_u has both signs (negative
for light and very heavy in the AMU baseline, positive in the iron-peak
region). So the minimal formula will misclassify sign on at least the
light and very-heavy ends.

The expected residual shape:
- Sign disagreement on light nuclei (B_obs < 0 < B_pred)
- Sign disagreement on actinides (B_obs < 0 < B_pred)
- Magnitude undershoot ~14× near gold
- Order-of-magnitude undershoot on the iron peak

**This is a no-fit no-search structural prediction. The residual shape
encodes what the minimal composition is missing — sign-changing curve
structure that would need to come from either (i) a different phi position
selecting CR009's triadic depth instead of pair depth, (ii) the s_b term
having a position-dependent sign not visible in dQ_b = 0, or
(iii) additional sealed structure from CR248 phase-A that CR250 doesn't yet
incorporate. The point of CR250 is to make those three follow-up directions
explicit by showing exactly where the minimal composition lands.**

---

## Test corpus (locked above the line)

- Source: `CR242_binding_dataset.csv` (71 AME2020-derived rows)
- Sha256: to be recorded in result file from the artifact
- Filter: rows with `N >= Z` (CR247's sealed scope — 69 rows)
- Excluded: H-1 (Z=1, N=0), He-3 (Z=2, N=1) — the N < Z symmetric
  variant of CR247 is reserved for a future CR

The runner reads (Z, N, A, B_u) from the dataset only. No mass-measurement
constants enter the formula.

---

## Verdict ladder (locked above the line)

CR250 reports **shape and magnitude separately** because the minimal
composition is known above the line to undershoot magnitude.

### Shape verdict (load-bearing for STRUCTURAL_PASS):
- `SHAPE_MONOTONIC_IN_NminusZ`: residuals ordered by (N − Z) show
  monotonic trend in `|Δ| / max(|B_obs|, 1e-6)` — TRUE/FALSE
- `LINEAR_RESCALE_RMS`: fit a single overall scale factor `α` to
  `B_obs = α · B_pred + 0` and report the resulting RMS. If RMS after
  rescale is < 1 MeV across all 69 nuclei, the **shape** is consistent
  with the substrate composition (and the missing factor is a single
  multiplicative constant traceable to a follow-up CR).

### Magnitude verdict (informational — not load-bearing for PASS):
- `max(|Δ|)` in MeV across 69 nuclei
- `mean(|Δ|)` and `RMS(|Δ|)` in MeV
- Top-10 worst rows table
- Best-10 (smallest |Δ|) rows table

### Overall verdict scoring:
- **STRUCTURAL_PASS** if `SHAPE_MONOTONIC_IN_NminusZ` is TRUE
  AND `LINEAR_RESCALE_RMS` < 1 MeV
  AND all wrong controls pass
- **BOUNDARY** if shape is monotonic but `LINEAR_RESCALE_RMS` ≥ 1 MeV
  (substrate composition has right structure but additional terms needed)
- **FAIL** if `SHAPE_MONOTONIC_IN_NminusZ` is FALSE
  (substrate composition has wrong structure, not a missing-coefficient issue)

This ladder is designed to honor the cascade insight (B_u IS the closure
fee) while acknowledging Sean's 2026-06-24 stacking-precision observation
("we proved on 'a' particle to 5 decimal points, now we are stacking
hundreds, thousands of particles and expecting the same precision?").
A single missing scale factor would be a STRUCTURAL_PASS, not a FAIL.

---

## Wrong controls (locked above the line)

Each WC perturbs one element of the sealed composition and reports
whether the shape-monotonic property and the rescale-RMS gate still hold.
A passing WC is one where the perturbation BREAKS the shape gate (proving
the unperturbed element was load-bearing).

- **WC-1 swap_phi_dQ**: swap dQ_b ↔ dQ_e (dQ_b becomes 7093/192,
  dQ_e becomes 0). If the formula is structural, this should break shape
  on N=Z rows (which now incorrectly inherit excess-neutron contribution).
- **WC-2 triadic_depth**: replace R^4 with R in the lift denominator
  (use the triadic form on a pair-class connection). If pair depth is
  load-bearing, magnitudes inflate by 1728× and rescale-RMS explodes.
- **WC-3 drop_D**: replace `(q + D)` with `q` in the lift numerator
  (zero out the D term). CR009 WC-3 already proved D is load-bearing
  at the particle level; this checks it's load-bearing at the nuclear
  level too. Eliminates s_b entirely (since dQ_b = 0).
- **WC-4 perturb_mu_Q**: replace mu_Q = 192/7117 with 192/7118.
  Checks the Q→u conversion constant CR240 sealed is load-bearing.
- **WC-5 shuffle_NminusZ**: shuffle the (N − Z) values across the 69
  nuclei (preserve Z but reassign N − Z). If (N − Z) structure carries
  real signal, shuffle should destroy correlation between B_pred and B_obs.

All five WCs must pass (i.e., break) for the unperturbed formula's
PASS-or-BOUNDARY verdict to be accepted.

---

## K-gates (locked above the line)

- **K1**: External anchor — AME2020 B_u values are external measurements;
  formula is sealed before runner reads the dataset; reveal-against-frozen-envelope
  protocol holds (no parameter tuning permitted at any stage).
- **K2**: Falsifiers F1–F4 (below) pre-stated; none may fire.
  - F1: `LINEAR_RESCALE_RMS` < 1 MeV ⇒ STRUCTURAL_PASS, else BOUNDARY/FAIL
  - F2: Any WC fails to break ⇒ corresponding element not load-bearing ⇒ FAIL
  - F3: Best-10 rows by |Δ| include any cascade-cited anchor (Au-197,
    C-12, C-13) with classification = `exact_match` (< 0.001 u) ⇒ note
    but does not change verdict (these are independent anchors)
  - F4: Shape verdict FAIL ⇒ overall FAIL regardless of rescale
- **K3**: Structural composition test, not blind discovery — the sealed
  upstream pieces (CR009 lift, CR247 phi) determine the formula; CR250
  composes them and runs.
- **K4**: Zero free parameters. The formula's 8 constants
  (R, D, S, κ, g, μ_Q, dQ_b, dQ_e) are all sealed in upstream CRs.
- **K5**: `python CR250_runner.py` produces the result file deterministically.

---

## What CR250 does NOT do

- Does not test alternative connection-topology rules (per-Z·(N−Z) pairs,
  liquid-drop A·(A−1)/2, surface A^(2/3), etc.). That is candidate-rule
  search which Sean's 2026-06-25 framing explicitly excluded.
- Does not compare to PDG, ΛCDM, GR, QM, or any outside model
  (R-3 discipline per [feedback_no_outside_model_comparison]).
- Does not modify any upstream sealed CR. CR009, CR238, CR240, CR247
  remain frozen.
- Does not search for the "right" scale factor that closes the rescale-RMS
  to PDG-grade precision. CR250 reports what the algebra natively says
  and where it lands.
- Does not extend to N < Z. The symmetric variant with
  `n_balanced = N` and `n_excess_proton = Z − N` is reserved.

---

## Provenance chain (cryptographic, to be recorded in result)

- CR005_result.md sha256 (M_native zero physics-fit underpins formula)
- CR009_result.md sha256 (connection-fee lift forms)
- CR238_result.md sha256 (substrate atoms)
- CR240_result.md sha256 (μ_Q Q→u conversion)
- CR247_result.md sha256 (phi decomposition)
- CR242_binding_dataset.csv sha256 (test corpus)
- CR250_PRECOMMIT.md sha256 (this file)

---

## Rule of Immutability

Sealed 2026-06-25 by Sean Brady. Formula, phi positions, lift form,
test corpus, verdict ladder, wrong controls, K-gates all frozen above
the line. Any amendment requires explicit AMENDMENT.md with preserved
first-run artifacts under `_FIRSTRUN_*` suffix per Courtroom audit-trail
discipline.
