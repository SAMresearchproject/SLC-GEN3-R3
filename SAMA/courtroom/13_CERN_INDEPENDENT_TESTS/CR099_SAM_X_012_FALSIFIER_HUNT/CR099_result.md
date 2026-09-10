# CR099 SAM-X-012 Falsifier Hunt - Wanted Poster

## Verdict

```text
CR099_FALSIFIER_SIGNATURE_SEALED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## What This Is

SAM commits, on the record, that no particle exists at partition (7,5).
This is a NEGATIVE prediction with a clean falsifier: find one and SAM
is broken.

This document is a 'wanted poster' for experimentalists. It decodes
SAM-X-012's structural prediction into observable language (charge,
mass, structural class) so a MoEDAL / CMS / LHCb / ATLAS analyst can
look at the right place and either find the falsifier or report a
null result.

## Commitment Proof

```text
prediction_commit_sha256   = cd046d9004337217b79e2f3d08ef00993df3ca095018f38e5b0f1995c121bd9e
prediction_commit_utc      = 2026-06-13T21:48:25Z
falsifier_signature_sha256 = b79c01d09167f561c706f8f9da686e23147489669b27e0bc43533edff6e47c90
signature_sibling          = CR099_falsifier_signature.json.sha256.txt
blindness_protocol_sha256  = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## What To Look For

**CRITERION A - Charge.** A particle with electric charge Q in any of:

| Q (fraction) | Q (decimal) | Note |
|---|---|---|
| -7/12 | -0.5833 | non-SM rational charge |
| -5/12 | -0.4167 | non-SM rational charge |
| +5/12 | +0.4167 | non-SM rational charge |
| +7/12 | +0.5833 | non-SM rational charge |
| -1/6 | -0.1667 | non-SM rational charge |
| +1/6 | +0.1667 | non-SM rational charge |

None of these are in the SM rational-charge set {0, +/-1/3, +/-2/3, +/-1}.

**CRITERION B - Mass.** Mass M in the band **[1.0 MeV, 10000.0 MeV]**.

Rationale (from sealed declared_premises):

```text
SAM-X-006 ((8,4) layered at a=4 PROPAGATION) = 1.025 MeV; SAM-X-007 ((9,3) paired transition at a=4) = 1.537 MeV; SAM-X-008 ((6,4,2) mixed layered at a=4) = 228 MeV. A (7,5) at the same a=4 PROPAGATION default would land in this 1 MeV - few GeV bracket. Extended upper bound to 10 GeV for conservative search coverage.
```

**CRITERION C - Primary carrier.** The particle must be identified as
a primary carrier, not a composite, bound state, or threshold artefact.
SAM cannot escape falsification by claiming a found state is 'really a
composite' - the criterion is locked at seal time.

## Where To Look

**Primary probe:**

```text
{
  "experiment": "MoEDAL (Monopole and Exotics Detector at the LHC)",
  "location": "LHC Interaction Point 8 (shared cavern with LHCb)",
  "sensitivity_mechanism": "(Z/beta)^2 ionization signature in Nuclear Track Detectors (NTDs)",
  "current_run_status": "Run 1 + Run 2 data published; Run 3 ongoing as of 2026-06; MoEDAL-MAPP extension commissioning",
  "published_searches_related": [
    "magnetic monopole searches (multiple Run-1 and Run-2 publications)",
    "milli-charged particle search",
    "fractionally charged particle limits at Q = 1/3 and 2/3"
  ],
  "gap_relative_to_SAM_X_012": "No published MoEDAL search at Q = +/- 7/12, +/- 5/12, or +/- 1/6 in the 1 MeV - 10 GeV mass band. A re-analysis of existing Run-1 + Run-2 NTD data at these specific (Q, M) coordinates would constitute a direct falsifier test."
}
```

**Secondary probes:**

- **CMS Heavy Stable Charged Particle (HSCP) search** - standard HSCP analysis threshold typically above 10s of GeV; dedicated low-mass extension would be needed to reach SAM-X-012 band
- **ATLAS HSCP search** - same threshold issue as CMS
- **LHCb tracking dE/dx fractional-charge analysis** - has reported limits on doubly-charged scalar bosons; not yet at Q = +/- 5/12 or 7/12 wedge
- **MoEDAL-MAPP (Run-3 extension)** - adds scintillator + active calorimeter; sensitivity extends to longer-lived neutral and charged exotics; in commissioning; strongest near-term probe of SAM-X-012's mass band

## How A Find Or Null Result Is Recorded

```text
if CERN publishes a result meeting CRITERION A + B + C:
    appeal row CR099a_<DATE>_<EXP>_FALSIFIED is appended
    appeal verdict = SAM_X_012_FALSIFIED
    09a structural foundation flagged for repair
    original CR099 signature is NOT modified

if MoEDAL Run-3 + MoEDAL-MAPP publishes null in the band:
    appeal row CR099a_<DATE>_<EXP>_NULL is appended
    appeal verdict = SAM_X_012_HOLDS_UNDER_NEGATIVE_CONFIRMATION
    SAM partition-algebra commitment strengthened
    original CR099 signature is NOT modified

if CERN publishes a near-miss (Q close to set; or mass at band edge):
    appeal row CR099a_<DATE>_<EXP>_NEAR_MISS is appended
    appeal verdict = SAM_X_012_PARTIAL_TEST_INCONCLUSIVE
    NO reframing of the original signature is allowed
```

## Anti-Motivated-Padding Rules

These are the rules that prevent SAM from wriggling out:

- **rule_1**: The candidate charge set is fixed at seal time. Adding new charges after CERN publishes is a protocol violation.
- **rule_2**: The mass band is fixed at seal time. Narrowing or widening after CERN publishes is a protocol violation.
- **rule_3**: CRITERION C (primary carrier) is required - SAM cannot escape falsification by claiming a found state is 'really a composite'. The criterion is locked at seal.
- **rule_4**: If MoEDAL or any CERN program publishes a result that meets criteria A+B+C, the appeal row records SAM_X_012_FALSIFIED with the publication reference. No reinterpretation.

## Rule-9 Line

```text
This CR is a structured invitation to break SAM. The signature is
sealed; the falsifier criteria are fixed; the CERN probes are named.
Now we wait for CERN.

Breaking SAM is good. Breaking SAM lets us fix it. Hiding from a
falsifier would be the failure mode, not finding one.
```
