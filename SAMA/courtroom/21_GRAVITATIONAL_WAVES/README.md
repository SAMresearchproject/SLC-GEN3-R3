# 21 — Gravitational Waves

**Branch opened:** 2026-06-28
**Architect:** Sean Brady
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## The SAM reading of a gravitational wave

A gravitational wave is **a wave of carrier tensors** — Θ-class
substrate elements (the 18-element overlap between the two 81-element
ledger sides per CR229) — that **escape a violent event before the
forming Home seals them inside its horizon**.

In SAM:

- A **Home** is any A=1 full-local-closure. Black holes, neutron-star
  remnants, and the cosmological seed are all the same primitive at
  different scales (manuscript §19).
- A normal Home formation captures **all** carrier tensors inside the
  horizon. The 1/8 tensor share (Θ/R²) stays bound; the 7/8 retained
  share (M/R²) stays bound. **No radiation.**
- This is *why we don't detect GWs constantly.* Every star that
  collapses into a BH would otherwise emit. They don't, because the
  carriers don't escape — the horizon seals before any Θ can radiate.

GW emission requires **two Homes to merge** under conditions where
their carrier-tensor populations interact *before* the unified horizon
closes. Some carriers get exposed across the merger boundary,
overrun the local horizon-formation timescale, and **radiate outward
as a Θ-wave**. The wave is the substrate's accounting for carriers
that "did not get a chance to link up with particles" after the
violent event.

This branch's purpose is to **derive the substrate conditions for
GW emission** and predict observable signatures from substrate
atoms — not to fit waveform templates.

## Why this is a separate branch

Prior GW170817 work in this courtroom lives at
[04_PHOTON_ROAD_SHAPIRO_DELAY/CR147](../04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/)
and addresses the **arrival-delay mechanism** (1.74 s between GW and
EM signals). CR147 sealed PASS: the delay is local engine time, not
post-release Shapiro-style propagation.

Branch 21 goes deeper — not "why was the delay 1.74 s" but **"what
substrate process makes a gravitational wave exist at all, and what
predicts when one will and won't be emitted."**

Upstream contact in STAM:
- `c:\VS\Stam_model-A-v1.0\tests\Substrate\G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT\`
- `c:\VS\Stam_model-A-v1.0\tests\Substrate\G700c_GW170817_LOCAL_SOURCE_A_START_RESIDUAL_SPLIT\`
- `c:\VS\Stam_model-A-v1.0\tests\Substrate\G701c_BLIND_GW170817_SOURCE_OFFSET_A_DELAY\`

## Load-bearing substrate atoms for this branch

From the [SAM master formula sheet](../docs/SAM_MASTER_FORMULA_SHEET_2026_06_28.md):

| Atom | Closed form | Value | Role in GW physics |
| --- | --- | ---: | --- |
| Θ | ĥ·d̂² | 18 | carrier tensor / overlap / graviton row support |
| Θ/R² | ĥ^(−d̂) | 1/8 | **tensor share** — upper bound on radiated fraction |
| M/R² | — | 7/8 | retained share — usually all captured |
| 162 = ℒ | ĥ·ℱ | 162 | closed ledger — both ledger sides; merger total |
| 126 = M | R² − Θ | 126 | matter capacity — what stays bound |
| 36 = 2Θ | ℒ − M | 36 | overlap doubled — peak interaction window |
| R | ĥ²·d̂ | 12 | route radix — sets ringdown timescale |
| d̂ | — | 3 | dimensional readout — toroidal radiation geometry |

The **1/8 tensor share** is the headline candidate: it caps the
maximum fraction of merger mass-energy that can radiate as GWs. LIGO
binary BH events typically radiate ~3–5% of total mass-energy; SAM
predicts the hard cap is **12.5%** (1/8) and no observed event
exceeds it. CR001 below tests this.

## Open question Sean is chasing

**The "donut" reading of GW170817.** In conversation Sean has
characterized the GW170817 event as carriers being "forced out like
a donut" around the merger plane. This framing does **not** appear
in the sealed CR147 artifacts (which use release-surface and
A-road-differential language). The donut framing is a candidate
substrate-topology reading that this branch may formalize — likely
tied to the d̂ = 3 dimensional readout producing a toroidal emission
pattern out of the equatorial merger geometry.

If formalized: the donut is the **Θ-overlap projected into the
3-dimensional readout** during merger — the 18-element overlap can
only radiate transversely (no monopole, no dipole — consistent with
standard GR predictions, but here derived from substrate counting
rather than linearized GR).

## What this branch will test

See [CR_QUEUE.md](CR_QUEUE.md) for the candidate test list. Headline
predictions in scope:

1. **Energy cap** (CR001): E_GW / M_total ≤ Θ/R² = 1/8 for every
   observed merger. Falsifiable on any LIGO/Virgo catalog event
   exceeding 12.5%.
2. **Emission condition** (CR002): GW emission requires binary
   merger, not single collapse. No observed core-collapse SN should
   produce a chirp-class GW signal at LIGO sensitivity.
3. **Ringdown frequency** (CR003): f_QNM = c³/(2π·G·M) × s(R, d̂, Θ)
   where the substrate factor s reduces to a rational expression in
   (R, d̂, Θ) — no fitted post-Newtonian coefficients.
4. **Donut topology** (CR004): GW emission anisotropy in NS-NS
   mergers (e.g., GW170817) shows a transverse / toroidal preference
   tied to d̂ = 3 readout, not the standard quadrupole pattern alone.
5. **Polarization structure** (CR005): the two GR polarizations
   (h_+, h_×) correspond to the two 81-element ledger sides; their
   joint signature is the 18-element Θ overlap.
6. **Detection-rate sanity** (CR006): SAM's emission-condition
   prediction reproduces the observed LIGO event rate without
   invoking population synthesis priors — sets a substrate floor on
   binary fraction at horizon-formation events.

## External catalog data Sean will need

(Not yet on disk — to be sourced when CR001 seals.)

| Catalog | URL | Use |
| --- | --- | --- |
| GWTC-3 (LIGO/Virgo/KAGRA) | https://gwosc.org/eventapi/html/GWTC/ | event masses, radiated energies, ringdown freqs |
| GW170817 multi-messenger | https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/ | NS-NS, EM counterpart, delay |
| LIGO O4 events | https://gwosc.org/O4/ | live detection rate sanity |
| GWOSC strain data | https://gwosc.org/data/ | optional, for raw-strain CRs |

## Branch discipline (inherited from courtroom rules)

- Stewardship hash on every CR HASHES.txt.
- No fitted parameters. Every constant traces to Tier 1–10 of the
  [constants sheet](../docs/SAM_CONSTANTS.xlsx).
- No outside-model comparison for PASS/FAIL gates (per
  `feedback_no_outside_model_comparison`). LIGO events are catalog
  data, not GR-template comparisons.
- Old tests are proof of process. If a CR seals BOUNDARY or FAIL,
  it stays sealed; appeals get a suffix (e.g., CR001b).
- No post-hoc honesty notes in results (per
  `feedback_no_posthoc_honesty_notes`). If the precommit didn't
  predict X, the result doesn't disclaim X.

## Provenance

| artifact | sha256 |
| --- | --- |
| upstream CR147 (GW170817 A-release) | per [HASHES.txt](../04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/HASHES.txt) |
| CR229@09a (inclusion-exclusion identity) | per [HASHES.txt](../09a_PARTICLE_MASS_CHAIN/CR229_CARRIER_TENSOR_INCLUSION_EXCLUSION_IDENTITY/HASHES.txt) |
| CR258@09a (primitive closure audit) | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| manuscript §19 HOMES | `c:\VS\The_Courtroom\docs\COURTROOM_MANUSCRIPT_SECTION_19_HOMES.md` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
