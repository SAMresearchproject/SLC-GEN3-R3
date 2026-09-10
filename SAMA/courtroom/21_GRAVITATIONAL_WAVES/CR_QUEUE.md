# 21_GRAVITATIONAL_WAVES — CR Queue

**Sean Brady, 2026-06-28**
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

Candidate test list for branch 21. Each CR has a one-line claim,
the falsifier, the catalog data needed, and the depends-on chain.
None are sealed yet — Sean picks one to lock first.

---

## CR001 — Radiated-energy cap at Θ/R² = 1/8

**Claim:** For every confirmed binary-merger gravitational wave
event in GWTC-3, the radiated energy fraction satisfies
`E_GW / (M_total · c²) ≤ Θ/R² = 1/8 = 12.5%`.

**Why it matters:** First load-bearing prediction of the
carrier-tensor framing. Single hard cap, derivable from substrate
atoms (Θ = 18, R² = 144), no fitted parameters.

**Falsifier:** Any one catalog event whose published E_GW exceeds
12.5% of total mass-energy.

**Catalog data:**
[GWTC-3 confident events](https://gwosc.org/eventapi/html/GWTC/) —
need to download as JSON or CSV. Columns required: M_total,
M_final, χ_eff, radiated energy / M_total. The radiated fraction
`(M_total - M_final) / M_total · c² ≈ E_GW / (M_total · c²)`.

**Wrong controls:**
- W1: same gate at 1/4 (Θ/R² × 2). Should be loose — passes
  trivially.
- W2: same gate at 1/16 (Θ/R² / 2). Should be tight — should
  catch high-mass BBH events.
- W3: same gate at GR's optimistic post-Newtonian estimate (~0.10
  for equal-mass, non-spinning). Compare envelopes.

**Verdict tree:**
- PASS: all GWTC-3 confident events ≤ 1/8.
- BOUNDARY: 1–2 events within 0.5% of cap.
- FAIL: ≥ 1 event > 1/8.

**Depends on:** CR229@09a (inclusion-exclusion identity sealed) +
CR258@09a (primitive closure).

---

## CR002 — GW emission requires binary merger

**Claim:** No observed gravitational-wave detection at
LIGO/Virgo/KAGRA sensitivity has been confirmed for a non-binary
event (single core-collapse SN, isolated NS spin-down, accretion
events). Every confirmed event is a binary coalescence.

**Why it matters:** SAM's carrier-tensor framing predicts no GW
emission from single Home formations because the lone horizon
captures all carriers. If LIGO ever confirms a non-binary chirp-
class signal, the framing is killed.

**Falsifier:** Any LIGO/Virgo confirmed-class detection labeled
core-collapse SN, isolated-NS, or non-merger origin.

**Catalog data:** GWTC-3 catalog (event classification column),
plus LIGO O4 trigger list filtered to confirmed events. SN
triggers (e.g., SN1987A-class searches) — null results
historically.

**Wrong controls:**
- W1: include "candidate" (unconfirmed) events; check rate.
- W2: include sub-threshold triggers; verify no SN-coincident
  triggers exceed background.

**Verdict tree:**
- PASS: 100% of confirmed events are binary coalescence.
- BOUNDARY: 1 anomalous event with ambiguous origin classification.
- FAIL: ≥ 1 confirmed non-binary GW event.

**Depends on:** CR001 PASS.

---

## CR003 — Ringdown frequency dimensionless factor in substrate units

**Claim:** The Schwarzschild quasi-normal-mode dimensionless
frequency factor (GR value ≈ 0.37367) reduces to a finite rational
expression in (R, d̂, Θ, π) per the CR258 primitive-closure audit
discipline.

**Why it matters:** Ringdown frequencies are precisely measured by
LIGO. If the dimensionless factor is a substrate atom, SAM derives
it. If not, that's a structural gap to be documented honestly.

**Falsifier:** No finite (R, d̂, Θ, π) expression evaluates to
0.37367 within abs_tol 1e-3 across enumerated candidates.

**Catalog data:** None (this is a substrate-derivation CR). LIGO
ringdown measurements (e.g., GW150914 220 Hz) become validation
once a substrate identity is locked.

**Candidates to enumerate (precommit-time):**
- `1/(πd̂) ≈ 0.1061` — too small
- `1/(2π) ≈ 0.1592` — too small
- `d̂/(2π·R) ≈ 0.0398` — too small
- `Θ/(π·R²) ≈ 0.0398` — same
- `1/(π × something)` — open
- Possibly involves the bigrade alphabet sum 45

**Verdict tree:**
- PASS: one rational-in-(R,d̂,Θ,π) expression matches GR's 0.37367
  within 0.5%.
- BOUNDARY: no exact match but a substrate expression within 5%.
- FAIL: no candidate within 10%. Documents that GR's coefficient
  may not be a substrate atom.

**Depends on:** CR001 PASS + CR258 closure.

---

## CR004 — Donut topology: GW170817 angular emission pattern

**Claim:** The angular intensity profile of GW170817's radiated
energy shows a substrate signature distinguishable from GR's pure
sin²(2θ) quadrupole — specifically, discrete intensity steps
corresponding to the bigrade alphabet {1, 2, 3, 4, 6, 8, 9, 12}.

**Why it matters:** First test of the "donut" framing Sean has
described conceptually. Predicts a discrete substrate signature
in a continuously-modeled GR observable.

**Falsifier:** GW170817 polarization-decomposed angular intensity
fits a smooth GR template better than a step-quantized substrate
template at > 3σ.

**Catalog data:** GW170817 sky-localization and polarization
posteriors from the LIGO/Virgo public data release. Multi-messenger
constraints (GRB 170817A, kilonova AT 2017gfo) may add geometric
priors on the inclination angle.

**Wrong controls:**
- W1: same test on BBH event (no EM counterpart, no inclination
  prior) — should be insensitive due to ambiguous geometry.
- W2: random bigrade-set substitution — should not reproduce
  GW170817 pattern.

**Verdict tree:**
- PASS: substrate-step template fits at > 2σ over smooth GR.
- BOUNDARY: ambiguous fit between substrate-step and smooth GR.
- FAIL: smooth GR fits decisively better.

**Depends on:** CR001 + CR002 PASS. Extends [CR147@04](../04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/)
from arrival-delay mechanism to emission-topology.

---

## CR005 — Polarization ledger correspondence

**Claim:** The two GR polarizations h_+ and h_× correspond to the
two 81-element ledger sides. Their joint signal corresponds to the
18-element Θ overlap. SAM therefore predicts **exactly zero
amplitude in any non-tensor polarization mode** (scalar, vector,
longitudinal).

**Why it matters:** LIGO/Virgo/KAGRA have published constraints on
non-tensor polarization modes (Isi et al. and follow-ups). SAM's
prediction matches GR's prediction quantitatively but for a
different reason (substrate counting vs spin-2 boson).

**Falsifier:** Any confirmed detection of non-tensor GW
polarization mode above background.

**Catalog data:** Isi et al. 2017 (LIGO/Virgo polarization tests),
plus GWTC-3 polarization-mode posteriors.

**Wrong controls:**
- W1: SAM-with-three-sided-ledger thought experiment — would
  predict 3 polarizations, falsifiable.
- W2: SAM-with-one-sided-ledger — would predict 0 polarizations,
  also falsifiable by every GW detection ever.

**Verdict tree:**
- PASS: non-tensor mode amplitudes consistent with zero at LIGO
  sensitivity.
- BOUNDARY: marginal non-tensor signature in one event.
- FAIL: confirmed non-tensor polarization detection.

**Depends on:** CR001 + CR002 PASS, CR229@09a inclusion-exclusion.

---

## CR006 — Detection-rate sanity from emission-condition prediction

**Claim:** The observed LIGO/Virgo/KAGRA detection rate is
consistent with SAM's emission-condition prediction (only
binary mergers radiate, capped at 1/8) without invoking any free
population-synthesis parameter.

**Why it matters:** Standard astrophysical rate calculations have
multiple knobs (IMF, binary fraction, common-envelope efficiency,
metallicity). SAM gives a substrate-derived emission probability
per Home-formation event; combined with cosmic SFR (an external
measured input), it should produce a rate estimate without fitting.

**Falsifier:** Predicted rate disagrees with observed (1.5×10⁻⁷
to 1.5×10⁻⁶ per Mpc³ per year for BBH at z<1 per O3) by > 1
order of magnitude.

**Catalog data:** GWTC-3 detection rates, LIGO O3/O4 sensitivity
horizons.

**Verdict tree:**
- PASS: within factor 3 of observed.
- BOUNDARY: factor 3–10.
- FAIL: > factor 10.

**Depends on:** CR001 + CR002 + CR005 PASS. Requires substrate
binary-formation probability — open derivation.

---

## Test sequencing (suggested)

1. **CR001** — substrate cap on radiated energy. Cleanest first test;
   killing prediction directly observable in GWTC-3. Single CSV
   download. Most informative for branch viability.
2. **CR002** — binary-only emission condition. Pure catalog check.
3. **CR003** — ringdown frequency in substrate units. Substrate-
   derivation only; no catalog download needed. Can run in parallel.
4. **CR004** — donut topology test on GW170817 specifically.
   Requires posterior data; harder but most novel.
5. **CR005** — polarization ledger correspondence. Match GR quanti-
   tatively, derive differently.
6. **CR006** — rate sanity. Requires CR001+CR002 sealed; depends on
   open astrophysical inputs.

CR001 is the recommended first lock. If it fails the entire framing
falls — efficient to test first.

## Out of scope for branch 21 (deferred)

- Primordial GWs / inflation-era stochastic background
- CMB B-mode tensor-to-scalar ratio derivation (lives in branch 19?)
- GW memory effect amplitude formula
- Continuous-wave (isolated NS) GW upper limits — by SAM these
  should be zero, but the framing in CR002 handles that case
- Gravitational lensing of GWs by intermediate masses

## Provenance reminder

Every CR in this queue, when sealed, must:
- Cite this CR_QUEUE.md by hash in its precommit
- Cite the [GW_SUBSTRATE_FRAMING.md](GW_SUBSTRATE_FRAMING.md) by hash
- Cite the [README.md](README.md) by hash
- Include the stewardship hash `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
- Reference upstream [CR147@04](../04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/) and
  [CR229@09a](../09a_PARTICLE_MASS_CHAIN/CR229_CARRIER_TENSOR_INCLUSION_EXCLUSION_IDENTITY/) by hash
