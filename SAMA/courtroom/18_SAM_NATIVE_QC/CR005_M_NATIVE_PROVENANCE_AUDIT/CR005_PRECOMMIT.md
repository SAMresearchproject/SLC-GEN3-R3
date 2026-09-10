# CR005 — M_native Provenance Audit

**Branch:** 18_SAM_NATIVE_QC
**Sealed by:** Sean Brady, 2026-06-24
**Question source:** [QGC_SESSION_MEMO_2026_06_24.md](../QGC_SESSION_MEMO_2026_06_24.md) §6.1 (the BLOCKER)
**Input artifact:** [CR252_particle_catalog_v2.csv](../../09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_particle_catalog_v2.csv) — verified bit-identical to 2026-06-15 baseline

---

## Question

For every M_native value in the CR252 particle catalog (321 candidates;
126 promoted to matter via downstream gating), was the value computed
from CR238 substrate atoms with zero free parameters, OR was a known
physical particle mass (or any value chosen to match an observed mass)
used as an input at any point in the upstream construction chain?

```text
   Specifically:

   (a) Formula-level audit. For every M_native formula in
       qp093a_all_stable_sam_particle_combination_enumerator.py, list
       every numeric literal, named constant, and imported value.
       Classify each input into the locked taxonomy below.

   (b) Upstream-CR provenance walk. For each upstream CR referenced
       by qp093a (CR221 κ derivation, CR222 constants-only generator,
       CR224 zero-free-parameter row engine, CR225 carrier hidden
       clock selector, CR226 vaulted SOB), open the CR's precommit
       and result. Catalog every constant the CR declares as input,
       classify each into the same taxonomy, and trace whether any
       declared input is a known particle mass or a value-chosen-to-
       match-observation.

   (c) Smoking-gun search. Search every upstream CR runner script
       and every CSV/JSON in the upstream chain for the literal
       string representations of known particle masses (proton
       938.272 MeV, electron 0.511 MeV, muon 105.66 MeV, neutron
       939.565 MeV, Higgs 125250 MeV / 125.250 GeV / 125.20 GeV).
       Any literal appearance as an INPUT (not as a downstream
       comparison) is a tautology flag.

   (d) Provenance verdict per formula. For each of qp093a's M_native
       formula classes (single-axis, triadic, pair, Higgs scalar,
       carrier weight, hidden source), produce a verdict:
       substrate_derived / unit_convention / structural_constant /
       requires_upstream_audit / physics_fit.

   (e) Overall verdict: did the cascade-session proton match
       (QP093A-0306 → 938.272 MeV at 0.03% error) and Higgs match
       (QP093A-0043 → 125,752 MeV at 0.4%) rest on substrate-derived
       M_native values, or on physics-fit inputs?
```

## Honest framing

This is the §6.1 BLOCKER from the cascade session memo. Per
[feedback_methodology_over_theory], the goal is exemplary testing
protocol, not proving theory right. Per
[feedback_audit_findings_get_verified], findings get verified, not
inherited — even if an upstream CR's result claims "zero free
parameters," CR005 verifies that claim against the actual code and
data on disk.

**The verdict determines whether the cascade-session proton/Higgs
matches are genuine substrate-derived predictions or tautological
artifacts of physics-fit inputs.** A FAIL invalidates the
"substrate-derived particle mass" patent claim and the §4
striking-match narrative in QGC_SESSION_MEMO_2026_06_24.md. A
PASS upgrades those from "interesting but disqualified" to
"defensible structural prediction" — within the audit surface
this CR examines.

CR005 does NOT prove the proton match is non-coincidental. That
requires §6.2 (K1 frozen envelope for additional particles) and
§6.7 (prior-probability analysis). CR005 only proves provenance:
the values are substrate-derived, not fit.

## Locked classification taxonomy

Every input identified in (a) and (b) above gets exactly one of
these classifications:

```text
   substrate_atom            CR238 atom: {1, α_H=2, D=3, α_H²=4,
                             R/2=6, S−1=7, S=8, D²=9, R=12,
                             α_H^(D+1)=16, α_H^(D+1)+1=17, Θ=18,
                             α_H·R=24, ℱ=81}
                             OR derived rational of substrate atoms
                             (e.g., S² = 64, R² = 144, D²/R = 0.75,
                             κ_num = 7117, κ = 7117/768)

   structural_constant       Named typed value in the CR238 framework
                             that is NOT a substrate atom directly but
                             traces to substrate-atom arithmetic
                             (e.g., A₀ = 1/(12π), N_max = 16πR⁴/17)

   unit_convention           Value introduced for unit conversion or
                             scale, not as a physical input
                             (e.g., 1000 for MeV scaling, 931.494
                             MeV/u IUPAC atomic-mass-unit conversion
                             when used as a CSV display multiplier,
                             not as a construction input)

   requires_upstream_audit   Input that depends on a sealed upstream
                             CR whose precommit/runner has not been
                             walked in this CR; resolution requires
                             reading that CR's chain (becomes a
                             BOUNDARY item, see verdict gates)

   physics_fit               Value that equals a known particle mass,
                             or any value documented in upstream CR
                             as having been chosen to match observed
                             physical data. SMOKING GUN — promotes
                             verdict to FAIL.
```

## Locked smoking-gun search list

The runner searches every file in the upstream chain (qp093a source,
CR221/222/224/225/226 precommits/runners/results) for these literals:

```text
   particle / mass (MeV)        / variants searched
   ────────────────────────────────────────────────
   electron       0.511          0.511 0.5109 0.51099
   muon         105.66          105.66 105.65 105.6583
   pion (π±)    139.57          139.57 139.5704 139.6
   pion (π0)    134.98          134.98 134.9768
   neutral kaon 497.65          497.65 497.611
   proton       938.272         938.272 938.27 938.28 938.3
   neutron      939.565         939.565 939.57 939.6
   Lambda      1115.7           1115.7 1115.683
   Z boson    91188             91188 91.1876
   W boson    80369             80369 80.369
   Higgs     125250             125250 125.25 125.20 125.10
   top-quark 173000             173000 173.0 172.9 173.2
   IUPAC u-MeV 931.494          931.494 931.49 931.5
```

A literal appearance in an upstream CR's RUNNER or PRECOMMIT as an
INPUT triggers physics_fit classification. A literal appearance in
a CR's RESULT or downstream-comparison CSV does NOT trigger (those
are reveal-side, allowed by R-3 discipline).

## Locked verification gates

```text
V-1   Every numeric literal and named constant in qp093a's M_native
      computation paths is enumerated in CR005_formula_audit.csv
      with a classification verdict and source pointer

V-2   Every upstream CR (CR221, CR222, CR224, CR225, CR226) has a
      provenance row in CR005_upstream_cr_audit.csv with: declared
      inputs, declared outputs, classification per input, and
      smoking-gun search result

V-3   The 13 known-particle-mass literals (locked list above) are
      searched across all upstream CR files; any match outside a
      RESULT.md or downstream-comparison CSV is flagged in
      CR005_smoking_gun_search.csv

V-4   For each qp093a M_native formula class (single-axis, triadic,
      pair, Higgs scalar, carrier weight, hidden source), a provenance
      chain is documented in CR005_provenance_chain.md tracing every
      input back to either a substrate atom, a unit convention, or
      a flagged tautology

V-5   The cascade-cited rows (QP093A-0306 proton, QP093A-0043 Higgs,
      QP093A-0313 R+1) have their full input chain explicitly
      walked in CR005_provenance_chain.md, with the M_native
      construction shown atom-by-atom

V-6   The verdict is one of: PASS, BOUNDARY (with named upstream-audit
      items), or FAIL (with named physics-fit items)
```

## Locked verdict gates

```text
PASS conditions (all required):
  P1  V-1 through V-6 hold
  P2  Zero inputs classified as physics_fit
  P3  Zero smoking-gun literals appear as inputs in upstream chain
  P4  All single-axis, triadic, pair, Higgs scalar, carrier, hidden-
      source formulas trace to substrate_atom + unit_convention +
      structural_constant (no requires_upstream_audit residue)
  P5  Cascade-cited rows (QP093A-0306, 0043, 0313) have fully-
      walked substrate-derived construction chains

BOUNDARY conditions:
  B1  ≤ 3 inputs require additional upstream audit (requires_upstream_audit
      classification) where the path to substrate_atom is plausible
      but not closed in this CR; named in summary.json as deferred
  B2  Smoking-gun search returns matches that are determined to be
      downstream-comparison-only after manual inspection (not input
      uses)
  B3  An axis_factor or other formula constant is structurally typed
      (e.g., 5/4 = (α_H+D)/α_H²) but the derivation walk-through
      is not yet sealed in an upstream CR; classification is
      structural_constant_pending_seal

FAIL conditions:
  F1  ANY input classified as physics_fit (smoking gun confirmed
      as load-bearing input)
  F2  ANY known-particle-mass literal in the smoking-gun list appears
      as an input to an upstream CR's runner or as a hardcoded
      constant in qp093a's M_native formulas
  F3  CR221's κ derivation traces to a fit against observed gravity
      data rather than substrate-atom arithmetic
  F4  CR222's "constants-only" claim is contradicted by an actual
      input that is not a substrate atom or unit convention
  F5  CR224's "zero free parameters" claim is contradicted by an
      actual fitted parameter
  F6  Cascade-cited row (QP093A-0306, 0043, 0313) construction
      cannot be walked to substrate atoms
  F7  Runner crashes or audit incomplete
```

## APPEAL — boundary regrade path

**Sean's policy (carried from CR252):** Findings get verified, not
inherited. If a BOUNDARY result's requires_upstream_audit items can
be:

1. **Named** — each item attributed to a specific sealed upstream
   CR with the unaudited portion explicitly identified
2. **Bounded** — the unaudited portion does NOT include any of the
   cascade-cited rows' construction inputs
3. **Resolved** — either by walking the additional upstream CR
   within this CR (amending CR005_provenance_chain.md), or by
   formally deferring to a follow-on audit CR (CR005a) with the
   deferred items listed

Then the BOUNDARY is **regraded to PASS_REGRADED_FROM_BOUNDARY** by
amending CR005_summary.json with:

```text
   "verdict_class": "PASS_REGRADED_FROM_BOUNDARY",
   "appeal_basis": "all requires_upstream_audit items named/bounded/resolved",
   "deferred_to_followon": [...],
   "appeal_authorized_by": "Sean Brady",
   "appeal_sealed_at_utc": "<timestamp>",
```

A FAIL (F1-F7) is **not appealable** — physics-fit inputs are
structural tautologies; the cascade-cited matches must be reframed
as a fit-result rather than a prediction, and the patent claim
"substrate-derived particle mass calculator" must be withdrawn or
narrowed.

## Wrong controls

```text
WC-1  (load-bearing substrate atom presence) Confirm R=12 appears
      as an input in qp093a's M_native formulas AND in CR238's
      declared atoms. Expected: present in both. Confirms the audit
      surface is actually examining substrate-atom usage.

WC-2  (load-bearing non-presence of physics fit) Confirm m_proton =
      938.272 does NOT appear as a numeric literal in any upstream
      CR runner or precommit. Expected: zero matches in input
      positions. If a match exists, FAIL by F2.

WC-3  (R-3 discipline: downstream-only literal allowed) Confirm
      that PDG mass literals MAY appear in CSVs labeled as
      "known_label" or "downstream_only" comparisons (per
      qp093a's CR119 reveal pattern), and these do NOT trigger
      physics_fit classification. Expected: such matches are
      identified and explicitly excluded with named justification.

WC-4  (audit surface non-trivial) Confirm the formula audit captures
      at minimum: line 230 (Higgs surface debit), line 256 (qA
      capacity div), line 295-296 (carrier/retained split),
      line 327-329 (single-axis native mass), line 401 (triadic
      m_native), line 434 (pair m_native), line 456 (Higgs scalar).
      Expected: all 7 formulas present in CR005_formula_audit.csv.
```

## Falsifiers

```text
F-PROTON-FIT  m_proton = 938.272 (or close variant) appears in
              upstream CR runner/precommit as input → QP093A-0306
              proton-match is tautological; cascade-session §4.1
              must be withdrawn as a prediction claim.

F-HIGGS-FIT   m_Higgs = 125250 / 125.250 (or variant) appears in
              upstream CR runner/precommit as input → QP093A-0043
              Higgs-match is tautological; cascade-session §4.2
              must be withdrawn.

F-MEV-FIT     IUPAC 931.494 MeV/u conversion is used as an INPUT
              to compute M_native (not just a downstream display
              conversion) → unit_convention reclassifies as
              physics_fit because the conversion is the link to
              observed mass.

F-AXIS-FIT    Any axis_factor in qp093a (1.25, 1.5, 0.125) is
              documented in upstream CR as fit-to-data rather than
              typed-rational of substrate atoms → physics_fit;
              touches single-axis row construction.

F-KAPPA-FIT   κ = 7117/768 in CR221 traces to a fit against observed
              gravity / mass data rather than substrate-atom
              arithmetic → the gravity bridge and every downstream
              M_native that uses κ is fit, not derived.
```

## Outputs

```text
   CR005_PRECOMMIT.md                  this file (sealed above the line)
   CR005_runner.py                     Python audit runner
   CR005_formula_audit.csv             one row per numeric/constant in
                                        qp093a M_native formulas
   CR005_upstream_cr_audit.csv         one row per upstream CR with
                                        declared inputs + verdict
   CR005_smoking_gun_search.csv        one row per known-mass literal
                                        with file/line of any match
   CR005_provenance_chain.md           per-formula provenance walk;
                                        per-cascade-row construction
                                        atom-by-atom
   CR005_wrong_controls.csv            WC-1 through WC-4 results
   CR005_summary.json                  verdict + V-1..V-6 + appeal
                                        block (if regraded)
   CR005_result.md                     verdict markdown
   HASHES.txt                          SHA-256 of all CR005 artifacts
```

## Cryptographic chain (inputs)

```text
   Catalog source (read-only):
   c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\
     CR252_PARTICLE_CATALOG_SPINE_REFRESH\CR252_particle_catalog_v2.csv
     (sha256 = 3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6)

   Generator source (read-only):
   C:\VS\quantum_phase\src\
     qp093a_all_stable_sam_particle_combination_enumerator.py

   Upstream CRs walked in this audit (read-only):
   c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\
     CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR\
     CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR\
     CR224_ZERO_FREE_PARAMETER_SOB_ROW_ENGINE\
     CR225_CARRIER_HIDDEN_CLOCK_SELECTOR\
     CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL\
     CR238_SUBSTRATE_SPINE_COMPACTION  (substrate-atom canonical source)

   Cascade-session context (read-only):
   c:\VS\The_Courtroom\18_SAM_NATIVE_QC\QGC_SESSION_MEMO_2026_06_24.md §4, §6.1
   c:\VS\The_Courtroom\18_SAM_NATIVE_QC\QGC_known_particle_mapping.csv
   c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\
     CR252_PARTICLE_CATALOG_SPINE_REFRESH\CR252_summary.json
```

## What CR005 DOES NOT close

- Does NOT prove the proton/Higgs matches are non-coincidental.
  That requires §6.2 (K1 frozen envelope) and §6.7 (prior probability).
  CR005 only determines whether they are substrate-derived vs fit.
- Does NOT audit CR119 / CR219 (those are intake/export wrappers,
  not M_native producers).
- Does NOT audit downstream usage in branch 18 cascade work. The
  cascade-session memo §4 striking-match claims live or die on
  CR005's verdict; CR005 does not itself adjudicate those claims.
- Does NOT alter qp093a, CR252, or any upstream CR. Read-only audit.
- Does NOT resolve lepton mass non-matches (§6.4) — out of scope.

## Sealed

Sean Brady, 2026-06-24. The audit question, classification taxonomy,
smoking-gun search list, verification gates V-1 through V-6, verdict
gates P/B/F, wrong controls, falsifiers, and outputs are all locked
above the line. The runner's actual provenance walk is the test.
The verdict is determined by what the runner finds, not by what was
hoped for.
