# CR002 — Binary-Only Cap-Approaching Emission

**Branch:** 21_GRAVITATIONAL_WAVES
**Mode:** EXPLORATORY
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** CR001 PASS (carrier-tensor cap holds 16/16)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Framing refinement (Sean, 2026-06-28)

The original [GW_SUBSTRATE_FRAMING.md](../GW_SUBSTRATE_FRAMING.md)
stated GW emission "requires" binary merger; single Home formations
were characterized as "silent." During CR002 design Sean refined the
substrate reading:

> "I would guess that formation of a Home or even an SN may produce
> 'tiny' GW."

The refined SAM prediction is therefore:

```text
Single-Home formation (core-collapse SN, isolated NS birth):
  GW emission  >  0
  but suppressed far below the binary cap Theta/R^2 = 1/8
  driven by geometric asymmetry of the collapse, not by overlap
  with a partner Home's carrier allocation

Binary merger (BBH, BNS, NSBH):
  GW emission CAN approach (but not exceed) Theta/R^2 = 1/8
  because two Home boundaries overlap before either fully captures
  its carriers (carrier-tensor framing, README sect. 3)
```

CR002 tests the **observed pattern**, not Sean's specific
suppression-factor prediction (which is left for a future CR):

- All currently confirmed LIGO/Virgo events should be binary mergers
  (the cap-approaching channel)
- LIGO's published upper limits on SN-class GW emission should NOT
  yet be in tension with the "tiny" prediction — current detector
  sensitivity is consistent with sub-detection-floor emission

## Question

For the curated GWTC representative set:

1. **Classification**: are all confirmed events binary coalescences
   (BBH / BNS / NSBH), with no confirmed single-event chirp?
2. **Upper-limit consistency**: is the LIGO O1+O2+O3 published upper
   bound on per-event SN GW emission `f_rad < ~10⁻⁴` consistent with
   SAM's "tiny" prediction (i.e., LIGO hasn't already ruled out the
   suppressed emission)?

## Data discipline

Same in-code-literal discipline as CR001. Event classifications
from LIGO/Virgo catalog papers. SN upper limits cited from:

- Abbott et al. 2020, Phys. Rev. D 101, 084002 — "Optically-targeted
  search for gravitational waves emitted by core-collapse supernovae
  during the first and second observing runs of advanced LIGO and
  advanced Virgo"
- Abbott et al. 2024, Astrophys. J. (preprint) — O3 targeted SN
  search updates

Reference values (declared numeric literals; not file reads at
runtime):

```text
LIGO O1+O2 targeted SN upper limit on E_GW for nearby SN
  (galactic, ~10 kpc, optimal orientation, well-localized):
    E_GW_upper  <  ~ 10^-4  M_sun c^2     (most stringent at peak sensitivity)

LIGO O3 targeted SN upper limit (improved):
    E_GW_upper  <  ~ 10^-5  to 10^-6  M_sun c^2

Typical progenitor mass for Type II SN: ~ 10-25 M_sun
Typical remnant mass (NS or BH):         ~ 1.4-5  M_sun
Typical f_rad upper bound for SN:        E_GW_upper / M_progenitor
                                        ~ 10^-6 to 10^-7
```

## Gates

**G1 — Classification**: every confirmed event in the CR001
representative set is classified as binary coalescence.

**G2 — No confirmed single-event chirp**: LIGO/Virgo published
"confident" event catalog does not contain a non-binary detection.

**G3 — SN upper-limit consistency**: published SN-search upper
limits on f_rad (~10⁻⁶ at best) leave headroom for any sub-cap
"tiny" SAM prediction. The framing is not yet falsified by
non-detection.

## Verdict tree

```text
PASS:
  G1 PASS AND G2 PASS AND G3 PASS
  -> binary-only pattern observed; tiny single-event emission
     consistent with current upper limits

BOUNDARY:
  one event with ambiguous classification (e.g., NSBH-vs-BBH for
  GW190814 mass-gap object) AND no confirmed non-binary
  -> framing survives but flag the ambiguous case

FAIL:
  any confirmed LIGO event classified as single-source chirp OR
  SN upper limit constrains emission below any plausible "tiny"
  scale (which would say current sensitivity ALREADY rules out
  the framing-allowed emission)
```

## What this CR seals

If PASS: the observed catalog pattern (binary-only cap-approaching
emission) is consistent with the carrier-tensor framing. Single
Home formations remain candidates for sub-detection-floor emission;
future detectors (Einstein Telescope, Cosmic Explorer) become the
sharper test.

If FAIL: either a non-binary confirmed event exists (kills the
binary-overlap mechanism), or SN upper limits have already pushed
SAM's allowed emission below physical interpretability.

## What this CR does NOT yet seal

- Specific substrate-derived suppression factor for single-event
  emission. Sean's "tiny" is a qualitative refinement; the
  closed-form (R, d̂, Θ, ℒ) expression for SN GW amplitude is
  open for a future CR (candidate: CR002b or CR007).
- Stochastic background from many distant unresolved single-event
  emissions. Open.
- Continuous-wave (isolated NS spin-down) limits. Open.

## Source citations (precommit-declared)

| Citation | Use |
| --- | --- |
| GWTC-1, GWTC-2.1, GWTC-3 catalog papers | event classification table |
| Abbott et al. 2020 PRD 101 084002 | O1+O2 targeted SN search upper limits |
| Abbott et al. 2024 (O3 preprint) | O3 targeted SN search upper limits |
| Hayama et al. 2015 PRD 92 122001 | SN GW theoretical templates |
| Pajkos et al. 2021 ApJ 914 80 | rotating core-collapse SN GW predictions |

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR001 PASS (upstream) | precommit `1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805` |
| branch README.md | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| branch GW_SUBSTRATE_FRAMING.md | `a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941` |
| branch CR_QUEUE.md | `ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
