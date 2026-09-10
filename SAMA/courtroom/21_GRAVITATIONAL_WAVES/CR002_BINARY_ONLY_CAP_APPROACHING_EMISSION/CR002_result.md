# CR002 — Binary-Only Cap-Approaching Emission — RESULT

```text
verdict           : PASS
mode              : EXPLORATORY
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18
runner_hash       : f01625dd258d73eb66383ff1bada49a2a9cafc2e4fcb153c08f41e30b2acfc0c
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

The SAM-refined prediction — **only binary mergers can approach the
Θ/R² = 1/8 carrier-tensor cap; single-Home formations may emit but
at amplitudes vastly suppressed below the cap** — is consistent with
the LIGO/Virgo confirmed-event catalog and with published targeted
SN-search upper limits.

| gate | result |
| --- | --- |
| **G1** all CR001 representative events are binary coalescence | **PASS** (16/16) |
| **G2** no confirmed non-binary GW detection in LIGO/Virgo catalog | **PASS** (count = 0) |
| **G3** LIGO targeted SN upper limits leave headroom for SAM's "tiny" emission | **PASS** (5 orders of magnitude headroom) |

## Framing refinement adopted at CR002

Per Sean's CR002-design refinement:

> "I would guess that formation of a Home or even an SN may produce
> 'tiny' GW."

The carrier-tensor framing's prediction for single-Home formations
(SN core-collapse, isolated NS birth) is **not zero** but **far
below the binary cap**. The substrate reading: a single collapsing
Home has no overlap partner to facilitate carrier ejection, so the
emission comes only from geometric asymmetries during the collapse
itself — predicted small.

Closed-form substrate expression for the suppression factor is
**open** (candidate CR002b / CR007 in the branch queue).

## G1 — Classification (16/16 binary)

All 16 representative events in the CR001 set are binary coalescence.
Sub-class breakdown:

| Sub-class | Count | Events |
| --- | ---: | --- |
| BBH | 11 | GW150914, GW151012, GW151226, GW170104, GW170608, GW170729, GW170809, GW170814, GW170818, GW170823 |
| BBH-asym | 1 | GW190412 |
| BBH-IMBH | 1 | GW190521 |
| BNS | 2 | GW170817, GW190425 |
| NSBH | 1 | GW200115 |
| NSBH? (mass-gap) | 1 | GW190814 |

The within-binary sub-class ambiguity on GW190814 (NSBH vs
low-mass BBH) does not affect the binary-only finding.

## G2 — No confirmed non-binary detections

Catalog status as of GWTC-3 + O4 early 2026:

- Confirmed non-binary chirp-class events: **0**
- Confirmed continuous-wave (CW) isolated-NS detections: **0**
- Confirmed stochastic-background detections: **0**
- Confirmed SN-coincident GW events: **0**

LIGO/Virgo published "confident" event catalogs contain only
binary coalescences. The SAM-predicted binary-only cap-approaching
emission pattern holds.

## G3 — SN upper-limit consistency

The LIGO targeted-SN search published upper bounds on radiated
energy from a hypothetical nearby (~10 kpc) core-collapse SN:

```text
O1+O2 envelope upper limit  :  E_GW < ~ 10⁻⁴ M_⊙ c²
O3   envelope upper limit  :  E_GW < ~ 10⁻⁵ M_⊙ c²
typical Type II progenitor :  M ~ 15 M_⊙
implied f_rad upper bound  :  ~ 6.7 × 10⁻⁷ (O3)

substrate cap              :  0.125
headroom factor            :  ~ 1.88 × 10⁵
```

The current LIGO upper bound on SN GW radiated fraction is **five
orders of magnitude below the substrate cap**. Any plausible
"tiny" substrate suppression factor (e.g., scaling with 1/ℒ², 1/F²,
or some other small substrate quotient) easily fits inside this
window. **LIGO has not already ruled out SAM's permitted
single-event emission.**

## What this CR seals

1. The currently observed gravitational-wave catalog is exclusively
   binary coalescence. SAM's prediction — only binary mergers
   can radiate at the cap-approaching scale — is consistent with
   observation.
2. SAM's framing-allowed "tiny" emission from single-Home formations
   is consistent with current LIGO non-detections at the targeted-SN
   sensitivity (five orders of magnitude headroom). The framing is
   not yet falsified by non-detection.
3. The carrier-tensor framing now passes its first two falsifiable
   tests (CR001 cap + CR002 binary-only emission). The next
   discriminating test is **CR003 ringdown frequency in substrate
   units** — first test where SAM either derives a coefficient GR
   only fits, or surfaces a structural gap.

## What this CR does NOT seal

- A specific substrate-derived numerical prediction for SN GW
  amplitude. Sean's "tiny" remains qualitative; CR002b / CR007
  is the open follow-up that would lock the closed-form suppression
  factor in (R, d̂, Θ, ℒ).
- The detectability threshold at next-generation detectors. Einstein
  Telescope and Cosmic Explorer (planned ~ 2030s) will reach
  f_rad ≲ 10⁻⁹ for galactic SN. SAM's "tiny" prediction needs to
  fall above that threshold to be ever-detectable, or it predicts
  permanent non-detection. Open.
- Stochastic GW background from accumulated single-event emission
  across cosmic history. Open.
- Continuous-wave (CW) limits on isolated millisecond-pulsar spin-down.
  These are upper limits at 10⁻²⁶ strain — also consistent with
  "tiny" emission. Not gated here.

## What CR001 + CR002 together establish

The carrier-tensor framing of gravitational waves has now passed two
falsifiable tests:

| CR | Test | Result |
| --- | --- | --- |
| CR001 | substrate cap Θ/R² = 1/8 on radiated fraction | PASS (16/16 events ≤ 6%, max 5.98%) |
| CR002 | binary-only pattern + tiny-SN consistency | PASS (G1+G2+G3 all clean) |

Two false-friendly windows on the framing closed:

- **CR001 could have been killed** by any single event > 12.5%.
  None observed.
- **CR002 could have been killed** by any confirmed non-binary chirp.
  None confirmed.

The framing is still alive, but its discriminating power against
standard GR remains weak at the cap and emission-pattern level —
both predictions are consistent with current data, and GR doesn't
forbid either. The discrimination comes from CR003+: ringdown
frequency derivation, donut topology, polarization-mode counting.

## Source citations

- GWTC-1: Abbott et al. 2019, Phys. Rev. X 9 031040
- GWTC-2: Abbott et al. 2021, Phys. Rev. X 11 021053
- GWTC-2.1: Abbott et al. 2024, Phys. Rev. D 109 022001
- GWTC-3: Abbott et al. 2023, Phys. Rev. X 13 041039
- Targeted SN search O1+O2: Abbott et al. 2020, Phys. Rev. D 101 084002
- O3 targeted SN search updates: Abbott et al. 2024 (preprint)

## Provenance hash chain

```text
precommit          : a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18
runner             : f01625dd258d73eb66383ff1bada49a2a9cafc2e4fcb153c08f41e30b2acfc0c
upstream CR001     : precommit 1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805
branch README      : 1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595
branch FRAMING     : a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941
branch CR_QUEUE    : ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66
stewardship        : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR002 PASS (EXPLORATORY).** The currently observed
gravitational-wave catalog is binary-only at the cap-approaching
scale, consistent with the SAM carrier-tensor framing. LIGO's
targeted SN-search upper limits leave five orders of magnitude of
headroom for the framing-allowed sub-cap "tiny" emission. The
framing survives a second falsifiable test; CR003+ become the next
discriminating probes.

`BINARY_ONLY_CAP_APPROACHING_EMISSION_16_OF_16_BINARY_ZERO_NON_BINARY_CONFIRMED_SN_UPPER_LIMITS_5_ORDERS_HEADROOM_PASS_EXPLORATORY`
