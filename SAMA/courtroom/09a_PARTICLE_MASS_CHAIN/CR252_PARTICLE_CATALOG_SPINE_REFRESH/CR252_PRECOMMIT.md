# CR252 — Particle Catalog Spine-Refresh

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-24
**Upstream concern:** provenance audit for downstream branch-18 CR005 (M_native audit)
**Stance:** non-destructive regen; staying close to the original test

> **AMENDMENT NOTICE — 2026-06-24.** V-3 below incorrectly specified
> `matter_row_allowed=yes count = 126`, conflating qp093a's matter column
> (baseline = 286) with the downstream CR119 matter table boundary
> (which IS 126). F2 inherited the same error. The sealed text below is
> preserved as the recorded spec error. The corrected V-3/F2 live in
> [CR252_PRECOMMIT_AMENDMENT.md](CR252_PRECOMMIT_AMENDMENT.md). The
> first-run FAIL artifacts (sealed under this precommit) are preserved
> for audit trail; re-execution proceeded under the amended spec.

---

## Question

Does the `qp093a_all_stable_sam_particle_combination_enumerator.py` generator,
re-executed without source modification under the current spine envelope
(post-CR238 substrate-spine compaction, post-CR243 mass-lift channel typing,
post-CR244 unequal-pair typed forms), produce the same 321-row particle
catalog and 126-row matter table that were emitted on 2026-06-15? If
not, can every row-level discrepancy be **named to a specific spine
advancement CR** sealed between 2026-06-15 and today?

```text
   Specifically:

   (a) Spine-constant audit. For every numeric constant qp093a hardcodes
       (R, D, α_H, PARTITION, S, axis_factors, pair-mass formula
       coefficients, qA-channel divisor R², carrier-split 1/8, retained
       7/8, Higgs scalar 7/8 · R² · 1000, surface-debit D²/R), confirm
       whether the post-CR238 canonical value matches.

   (b) Bit-identical re-execution. Run the qp093a script unchanged
       against current upstream qp091/qp092 artifacts; capture the
       fresh 321-row catalog.

   (c) Row-by-row delta. For every QP093A-#### candidate_id: compare
       2026-06-15 M_native, q_abs, partition_signature, M_observed,
       qA, stability_status against the regen values.

   (d) Discrepancy classification. Every difference falls into one of:
         - unchanged: bit-identical
         - environment_drift: floating-point or library-version artifact
         - named_spine_advancement: explainable by a specific sealed CR
         - unexplained: cannot be attributed to a known spine update
```

## Framework-advancement concern (why we are rerunning)

The `qp093a_candidate_catalog.csv` source artifact that CR119 intook,
CR219 exported as the 126-row promoted-matter table, and Sean's
`126part_with_carriers.xlsx` was hand-annotated from, was last
regenerated on **2026-06-15** (per `latest_table_source_manifest.csv`
sha256 manifest). Between 2026-06-15 and 2026-06-24 the substrate
spine has materially advanced in branch 09a:

```text
CR ID    Title                                       Sealed     Spine impact
─────────────────────────────────────────────────────────────────────────────
CR214    CR119 particle-complement pattern audit     post-0615  audit only
CR215    CR214 carrier numeric duplicate audit       post-0615  audit only
CR216    Carrier duplicate retirement                post-0615  spine-touch
CR217    Dedup structural identity audit             post-0615  spine-touch
CR218    Hidden source bigrade derivation            post-0615  spine-touch
CR229    Carrier tensor inclusion-exclusion identity 2026-06-22 derived only
CR238    Substrate spine compaction                  post-0615  SPINE-CRITICAL
CR243    Mass-lift channel typing Y(P)=X/K           post-0615  SPINE-CRITICAL
CR244    Unequal-pair typed forms                    post-0615  SPINE-CRITICAL
CR245    Binding curvature from typed substrate      post-0615  derived only
CR247    SOB inverse second-layer                    post-0615  derived only
CR248    SOB micro-channel debit occupancy           post-0615  derived only
CR249    A-kernel binding geometry                   post-0615  derived only
CR250    C_A lock and refit                          post-0615  derived only
CR251    Bounce-aware asymmetric isolation           post-0615  derived only
```

Branch 18 downstream (LCQC004 / LCQC004a / LCQC006a / CR001-CR004
sealed 2026-06-24) cites the substrate atoms `{R, D, α_H, S, Θ, R²,
M=126, L=162, N_max=16πR⁴/17, A_0=1/(12π), κ_num=7117}` and the
typed surface-debit `D²/R` and Higgs identity
`R²(1−2⁻ᴰ) − D²/R = 125.25 GeV`. The 2026-06-24 cascade session also
derived the connection-fee formula `(R + q + D)/R` for triadic shapes
and matched the proton mass at 0.03%. **All of these downstream uses
rest on M_native values originally emitted by a pre-CR238 run of
qp093a.**

This CR exists to discover whether that provenance trail is
clean — by re-executing the same code against the current spine
envelope and surfacing any row-level deltas explicitly, with named
attribution to spine advancements where deltas exist. The audit is
the proof; the freshness of the catalog is the byproduct.

**No row may be silently changed. No row may be added or dropped
without naming the upstream CR that authorized the change. The
discrepancies are the concern — finding them and explaining them is
the test.**

## Locked spine atoms (read-only, comparison surface)

The audit compares these qp093a-hardcoded values against the
post-CR238 canonical values. The canonical values are sourced from
the named CR; the comparison is the test.

```text
   qp093a source line  qp093a value          post-CR238 canonical    source
   ─────────────────────────────────────────────────────────────────────────
   L54  R              Decimal(12)            12                      CR238 §1
   L55  D              Decimal(3)             3                       CR238 §1
   L56  ALPHA_H        Decimal(2)             2                       CR238 §1
   L57  PARTITION      {1,2,3,4,6,8,9,12}     {1,2,3,4,6,8,9,12}      LCQC002 / CR238 (write-residual subset)
   L61  EIGHT          Decimal(8)             S = α_H^D = 8           CR238 §1
   L60  SEVEN          Decimal(7)             S−1 = 7                 CR238 §1
   L230 D²/R           D*D/R = 9/12 = 0.75    D²/R = 0.75             CR114 / CR229 (Higgs surface debit)
   L256 qA divisor     R*R = 144              R² = 144                CR229 (matter capacity)
   L295 carrier split  qA/EIGHT = qA/8        α_H^D = 8 split         CR238 + CR222d
   L296 retained       qA*SEVEN/EIGHT = 7qA/8 (S−1)/S split            CR238 + CR222d
   L328 axis_factor    plus=1.25, minus=1.5,  POST-CR243 RECHECK      [CR243 typed channels]
                       neutral=0.125          REQUIRED
   L434 pair m_native  a·b·R + |q|·D          POST-CR244 RECHECK      [CR244 unequal-pair forms]
                                              REQUIRED
   L456 Higgs scalar   R²·7/8 · 1000          R²(1−2⁻ᴰ) = 126         per Higgs identity memo
                                              ⇒ R²·7/8 ✓ (D=3)
```

**Audit verdict per row:**
- `match` — qp093a value equals post-CR238 canonical value
- `drift` — values differ; classification required
- `requires_recheck` — value depends on a post-CR238 sealed CR
  whose impact on qp093a's formula is non-trivial; explicit derivation
  needed to determine match-vs-drift

## Locked program

```text
   step  action                                         output
   ──────────────────────────────────────────────────────────────────────────
   1     Open qp093a script; extract every numeric      CR252_spine_input_audit.csv
         constant + formula coefficient with source     (one row per audited element,
         line reference                                  match/drift/requires_recheck verdict)

   2     For each `requires_recheck`, trace the post-   CR252_recheck_derivations.md
         CR238 derivation (axis_factor: walk through    (named CR + derivation chain
         CR243 typed channel forms; pair m_native:      per recheck item)
         walk through CR244 unequal-pair forms)

   3     Re-execute qp093a in current environment       CR252_particle_catalog_v2.csv
         WITHOUT source modification. Pipe the          (full 321-row regen, identical
         output to the CR252 directory.                  schema to 2026-06-15)

   4     Row-by-row diff: join 2026-06-15 catalog       CR252_row_delta.csv
         and v2 catalog on candidate_id; compute        (one row per QP093A-####
         deltas for M_native, M_observed_candidate,     candidate_id, with deltas +
         q_abs, partition_signature, stability_status, classification)
         matter_row_allowed, qA_source_support,
         tensor_carrier_support, retained_write_support

   5     Discrepancy classification: for every row      column added to row_delta:
         where any field changed, classify as:           change_class
         { unchanged | environment_drift |               (one of the 4 named classes)
           named_spine_advancement | unexplained }

   6     Aggregate: counts per change_class; counts     CR252_aggregate.csv
         per spine_advancement_cr (named); list of     (rolled-up summary)
         unexplained rows if any
```

## Locked verifications

```text
V-1   Row count audit: regen produces exactly 321 catalog rows
      (matches qp091/qp092 upstream invariant; spine atoms R/D/α_H
      unchanged guarantee this; if FAIL → environment_drift or
      upstream qp091/qp092 artifact change)

V-2   Bin distribution audit: regen bin counts match 2026-06-15
      bin counts exactly (stable_matter_rows, antimatter_conjugate_rows,
      unstable_resonance_rows, bound_composite_rows, carrier_only_rows,
      hidden_source_support_rows, rejected_fake_closures)

V-3   Matter promotion audit: regen produces exactly 126 rows with
      matter_row_allowed=yes (the CR119 matter table boundary)

V-4   candidate_id stability: every QP093A-#### id in 2026-06-15
      appears in regen with identical id; no id is added or removed

V-5   Spine input audit completeness: every numeric constant and
      formula coefficient in qp093a is enumerated in
      CR252_spine_input_audit.csv with a match/drift/requires_recheck
      verdict and a source CR pointer

V-6   Every `requires_recheck` element has a corresponding entry
      in CR252_recheck_derivations.md with the post-CR238 derivation
      walked through

V-7   Every row with change_class=named_spine_advancement names a
      specific sealed CR ID (CR238 / CR243 / CR244 / etc.) in the
      delta CSV's `attribution` column

V-8   No row carries change_class=unexplained
```

## Wrong controls

```text
WC-1  (no-op regen consistency) Re-execute qp093a a second time
      in the same environment within the same CR. Expected: bit-
      identical to first regen. If different → environment is
      non-deterministic and conclusions about source vs environment
      drift are not separable.

WC-2  (canonical-value substitution proof) For one `match`-verdicted
      constant (e.g., R=12), confirm that substituting a wrong value
      (R=10) into a fresh qp093a copy produces materially different
      output (different M_native values across most rows). Expected:
      rejection — wrong R produces wrong catalog. Confirms the audit
      surface is actually load-bearing.

WC-3  (downstream invariant preservation) For three structural
      identities cited by branch 18 — Higgs at QP093A-0043 with
      M_native = 135.0 (= D² · 15? — check), proton at QP093A-0306
      with M_native = 1.0069, single-atom R+1 at QP093A-0313 with
      M_native = 13.000 — verify presence in regen. If a row's
      M_native shifted, expected: every shift attributable to a
      named CR per V-7.

WC-4  (carrier-tensor non-promotion) Regen catalog's carrier_only_rows
      MUST still have matter_row_allowed=no (CR119's null-conjugate
      override + carrier non-promotion discipline preserved). Expected:
      6 carrier rows present, all matter_row_allowed=no.
```

## Verdict gates with explicit appeal path

```text
PASS conditions (all required for first-pass PASS):
  P1  V-1 through V-8 hold
  P2  All deltas classify as either { unchanged } or { named_spine_advancement }
  P3  WC-1 through WC-4 confirm
  P4  Zero rows with change_class = unexplained
  P5  Zero rows with change_class = environment_drift

BOUNDARY conditions (regrade-to-PASS path documented; see APPEAL):
  B1  Small numerical discrepancies (|Δ M_native| < 1e-6 relative,
      attributable to Decimal precision or float-vs-Decimal
      handling differences in qp091/qp092 source JSON parsing)
      across some rows — classified as environment_drift
  B2  A small number (≤ 5) of rows show change_class = unexplained
      where the discrepancy is small (|Δ| < 1% relative) and a
      reasonable spine advancement candidate exists but the
      derivation walk-through is not yet complete

FAIL conditions:
  F1  Row count ≠ 321 in regen
  F2  V-3 fails (matter promotion count ≠ 126)
  F3  Candidate_id mismatch (V-4 fails — rows added or removed
      without spine-advancement attribution)
  F4  Many (> 5) rows carry change_class = unexplained, OR any
      unexplained row has |Δ| > 1% relative
  F5  WC-1 fails (environment non-deterministic)
  F6  WC-2 fails (wrong R produces same output — audit surface
      not load-bearing)
  F7  WC-4 fails (carrier-tensor non-promotion discipline broken)
  F8  Branch-18-cited rows (QP093A-0306, 0043, 0313) missing or
      structurally shifted without named-CR attribution
```

## APPEAL — boundary regrade path

**Sean's policy (locked):** Discrepancies are the concern. Finding
them and explaining them is the test. If a BOUNDARY result's
discrepancies can be:

1. **Named** — every drifted row attributable to a specific sealed
   CR's spine advancement (CR238 / CR243 / CR244 / etc.), with the
   derivation walked through in `CR252_recheck_derivations.md`
2. **Bounded** — drift magnitudes are quantified and reported in
   `CR252_aggregate.csv` with min / max / median per-CR attribution
3. **Honored** — the regen output (CR252_particle_catalog_v2.csv)
   is adopted as the new canonical particle catalog; the 2026-06-15
   artifacts are stamped SUPERSEDED-FOR-PROVENANCE (not deleted,
   not characterized as "wrong" per
   [feedback_old_tests_proof_of_process])

Then the BOUNDARY is **regraded to PASS** by amending
`CR252_summary.json` with:

```text
   "verdict_class": "PASS_REGRADED_FROM_BOUNDARY",
   "appeal_basis": "all discrepancies named to spine-advancement CRs;
                    drift bounded and documented; superseding stamped",
   "appeal_authorized_by": "Sean Brady",
   "appeal_sealed_at_utc": "<timestamp>",
   "named_attributions": { ... per-CR drift summary ... }
```

A BOUNDARY that fails to meet the named/bounded/honored criteria
remains BOUNDARY. A FAIL is not appealable — F1-F8 conditions are
structural failures that require diagnostic work before re-running.

## Falsifiers

```text
F-UNNAMED  Any row's M_native or partition_signature changes
           without attribution to a sealed upstream CR: the
           pre-CR238 catalog cannot be retroactively rationalized;
           the spine-refresh has revealed a true upstream gap that
           needs a new CR to seal.

F-COUNTS   Bin counts shift: the stability selector itself depends
           on a constant that changed; deeper than spine-refresh,
           the catalog construction logic itself needs review.

F-NONDET   WC-1 environment non-determinism: spine-refresh
           conclusions are not separable from runtime variation;
           re-pin environment (Python version, Decimal context)
           and re-run.

F-PROTON-DROP  QP093A-0306 missing from regen OR its M_native
           shifts > 0.5% without named attribution: the proton-match
           result from 2026-06-24 cascade is invalidated as a
           provenance claim; branch-18 CR005 must record this.

F-HIGGS-DROP   QP093A-0043 missing from regen OR its M_native
           shifts > 0.5% without named attribution: same as
           F-PROTON-DROP for the Higgs match.
```

## Outputs

```text
   CR252_PRECOMMIT.md                  this file
   CR252_runner.py                     Python runner implementing
                                        the locked program
   CR252_spine_input_audit.csv         one row per audited qp093a
                                        constant; verdict +
                                        canonical source CR pointer
   CR252_recheck_derivations.md        per-requires_recheck:
                                        named CR + derivation walk
   CR252_particle_catalog_v2.csv       fresh 321-row regen
   CR252_matter_table_v2.csv           matter-gated 126-row subset
   CR252_row_delta.csv                 row-by-row diff vs
                                        2026-06-15 catalog
   CR252_aggregate.csv                 rollup: counts per
                                        change_class + per
                                        spine_advancement_cr
   CR252_summary.json                  verdict + V-1..V-8 +
                                        appeal block (if regraded)
   CR252_result.md                     verdict markdown
   HASHES.txt                          SHA-256 of all CR252 artifacts
```

## Cryptographic chain (inputs)

```text
   qp093a generator (immutable for this CR):
   C:\VS\quantum_phase\src\qp093a_all_stable_sam_particle_combination_enumerator.py

   2026-06-15 source catalog (the comparison baseline):
   C:\VS\quantum_phase\artifacts\qp093a_stable_particle_combination_enumerator\
       qp093a_candidate_catalog.csv (sha256 in CR119 input_manifest)

   2026-06-15 latest exports (also baselines):
   C:\VS\quantum_phase\artifacts\latest_particle_matter_periodic_tables\
       latest_particle_table.csv
       latest_matter_table.csv
       latest_table_source_manifest.csv

   Upstream sealed CRs (read-only spine references):
   CR114, CR222d, CR229, CR232, CR238, CR240, CR243, CR244

   Downstream caller (read-only context):
   CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL
   CR219_PROMOTED_PARTICLE_ROWS_EXPORT
```

## What CR252 DOES NOT close

- Does NOT itself audit M_native provenance against substrate atoms
  end-to-end. That is branch-18 CR005's job, which CR252 prepares for.
- Does NOT validate the connection-fee formula or any K1 reveal
  against PDG masses. Branch-18 CR009 (proposed) is the K1 envelope.
- Does NOT modify qp093a's enumeration logic. Only re-executes it.
- Does NOT promote tensor carriers, change matter-row gating, or
  alter the null-conjugate boundary at QP093A-0088. These
  invariants are preserved from CR119 / qp092h.
- Does NOT touch the `126part_with_carriers.xlsx` file. That stays as
  Sean's historical analysis artifact; if CR252 regen produces a
  differing catalog, the xlsx is also stamped
  SUPERSEDED-FOR-PROVENANCE-via-CR252.

## Sealed

Sean Brady, 2026-06-24. The framework-advancement concern, the
spine-comparison surface, the locked program, V-1 through V-8,
the wrong controls, the verdict gates, the BOUNDARY-regrade
appeal path, and the falsifiers are all locked above the line.
The runner implementation, the regen execution, and the
discrepancy classification are the test.
