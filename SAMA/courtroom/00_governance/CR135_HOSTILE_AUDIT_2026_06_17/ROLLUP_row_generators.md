# CR135 Hostile Audit — Roll-up of Row-Generator Suite

**Audit date:** 2026-06-17
**Mode:** adversarial; no benefit of the doubt
**Auditor:** Genghis Khan
**Suite scope:** CR128, CR128b, CR129, CR129b, CR129c, CR130, CR131, CR132, CR133, CR134 (10 CRs)

## Tier distribution

| Tier | Code | Count | CRs |
|---|---|---:|---|
| 1 | PASS_COURTROOM_GRADE | 0 | (none) |
| 2 | PASS_WITH_REWORD | 5 | CR128, CR128b, CR129, CR129c, CR130, CR133 |
| 3 | REGRADE_TO_BOUNDARY | 1 | CR129b |
| 4 | DEMAND_RETEST | 3 | CR131, CR132, CR134 |
| 5 | REQUIRES_APPEAL_CR | 0 | — |
| 6 | HASH_CHAIN_BREAK | 0 | — |
| 7 | CALLOUT_FAIL_DRESSED_AS_PASS | 0 | — |

(CR133 included in Tier 2 by re-count; total = 10.)

Net: **zero courtroom-grade row-generators** in the suite. Every CR has at least one defect.

## Top 3 most-serious findings across the suite

### Finding 1 — UNIVERSAL: every result.md cites a wrong self-hash for the law-lock file

Every one of the 10 CRs has a `CR<N>_law_lock_sha256 = …` line in its result.md that does NOT match the actual hash of the law-lock JSON file on disk. Verified by `Get-FileHash` against each lock file:

| CR | Cited self-hash | Actual file hash | Match? |
|---|---|---|---|
| CR128  | d8ed19c1… | 0f62d6b4… | NO |
| CR128b | 9336468a… | fb9287cd… | NO |
| CR129  | 210e174e… | 041a487c… | NO |
| CR129b | c5751756… | 8c3d0eb7… | NO |
| CR129c | d823faba… | bfd5ab8c… | NO |
| CR130  | 906a527a… | 0a40209b… | NO |
| CR131  | 9fb53281… | 2aef1403… | NO |
| CR132  | f4811aa1… | fbc25a88… | NO |
| CR133  | 3adf93b8… | 1e7e08d8… | NO |
| CR134  | 4aa8f02b… | 6ab49442… | NO |

Downstream CRs correctly cite the ACTUAL upstream hashes (e.g., CR128b cites CR128 as `0f62d6b4…`, which matches reality). So the cryptographic chain between CRs is intact for users — but every individual CR is INTERNALLY INCONSISTENT with its own lock file. This is a 10-of-10 documentation defect that any external auditor will flag immediately. It also suggests the result.md files were written before the lock file was finalized, then the lock was re-written, and the cited hash was never updated. Reword every result.md to cite the actual on-disk SHA before any manuscript submission.

### Finding 2 — CR129b is a 4-stage iterative curve-fit framed as a discovery

CR129b explicitly documents that the form `|S| = M·(4q_eff+D)/(4R⁴)` was the 4th attempt after pure pairwise (failed), 1/8 surcharge (failed), and 9/8 surcharge (overshoots by exactly 18/17). The "overshoots by exactly 18/17" is the smoking gun — it forced the coefficient to be reverse-engineered to 17/16 = 9/8 · (17/18). The post-hoc decomposition `17 = R + D + α_H = 12 + 3 + 2` is numerology pegged on small integers. Additionally:

- The q_eff piecewise switch (`R if q=0 else q_abs`) is itself a 1-DOF tuning to make the q=0 case work.
- The sign rule for q≥1 is EXPLICITLY OPEN — 59 of 76 rows have signs supplied by the data, not predicted by the law.
- WC4 (1/8 surcharge failure) is listed as a wrong control. It is iteration history, not a control.

Line 124 of CR129b's result.md states "S_debit is FULLY DETERMINED … Zero free parameters per row." This is false on its face: the sign at q≥1 is read from the row's q_sign, not computed. CR129b currently overstates the closure. Demand: regrade to BOUNDARY; do not cite the universal sign rule or the 17/16 closed form in the manuscript as predictions.

### Finding 3 — CR131, CR132, CR134 are lookup tables disguised as laws

- **CR131** has K coefficients fit per cell of a 4-cell matter/antimatter × q_sign table; WC6 admits the K-swap was discovered by ANALYZING 42 INITIAL VIOLATIONS. That is iterative fitting to data, period.
- **CR132** has 6 carrier classes × per-class (i,j) assignments — 8 free parameters across 6 rows. WC4 admits C1=9/8 was tried, COLOR_OWNER didn't fit, pivot to C1=1. Free parameters per row ≥ 1.
- **CR134** is `M = p + p²/R²` extracted by computing `(M-p)/p²` directly from the 8 rows and reading off 1/144. The algebra is exhausted in-sample; no forward-blind test is reachable within the current algebra.

These three CRs cannot support manuscript claims of "zero free parameters" without substantial rewording. They are descriptions of the in-sample data, not predictive laws.

## Cross-cutting weaknesses

- **C3 WRONG_CONTROLS_LOAD_BEARING: 9 of 10 CRs fail.** No CR runs a destructive control — none deletes a load-bearing input and demonstrates that the law breaks. WCs in this suite are scope statements and iteration histories.
- **C4 FREE_PARAMETERS_HONESTLY_ZERO: 10 of 10 CRs fail.** Every "zero free parameter" claim becomes false once you count the functional-form selection as a degree of freedom. Multiple plausible forms could have fit each dataset; the chosen form was selected by inspection.
- **C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA: 10 of 10 CRs fail.** No CR has a precommit hash of the formula predating the data inspection. Every form was iterated against the catalog.
- **C5 IN_SAMPLE_DISCLOSED: 10 of 10 CRs honestly disclose.** This is the suite's strongest feature — every CR explicitly admits inductive derivation and commits a forward-blind falsifier for future rows. Manuscript can lean on this honesty.

## What the suite IS (the steel-manned reading)

A coherent algebraic generator family that explains every M_native value in CR119 across BOUND_COLOR_PAIR, OCTET_COMPOSITE 3-body, GROUND_BARYON_3BODY, V4_1_SINGLE_WRITE, 6 carrier classes, OUTER_BINARY_NEUTRAL, and SOURCE_SUPPORT_PACKET. The forms use only the constants {R=12, D=3, α_H=2} and the partition algebra {1,2,3,4,6,8,9,12}. In-sample, 376/376 rows tested (36 + 30 + 76 + 28 + 44 + 90 + 6 + 24 + 8 + 24-overlap) match the generators exactly. This is a real pattern.

## What the suite IS NOT (the hostile reading)

A predictive theory. Every generator was extracted by inspecting in-sample data; the suite has no genuine out-of-sample evidence; the forward-blind commitments resolve only when CR119 catalog extends (timeline unknown); some forms (CR132, CR134) have algebras exhausted in-sample and cannot be falsified within scope; CR129b explicitly leaves the sign rule open for 59 of 76 rows; CR131's "lepton-generation" narrative is rhetorical.

## Single most-important demand for the manuscript

**Do not state "zero free parameters" without immediately qualifying "post-lock, after inductive extraction from CR119 in-sample data; forward-blind tests pending."** Every "law" in this suite is a generator-consistency claim, not a first-principles derivation. The manuscript can lean hard on the cross-class regularity (R, D, α_H, partition algebra recur across 10 operator classes) without making the stronger claim that the forms were derived from principles. The Tier-2 majority means a single careful editing pass can rescue most of the suite; the Tier-3/Tier-4 entries (CR129b, CR131, CR132, CR134) need explicit rephrasing as "lookup tables observed exact on in-sample data" rather than "laws."

## Recommended sequence of fixes

1. Fix all 10 self-hash citations in result.md files (10 minutes of work; eliminates Finding 1).
2. Add the qualifier `_SEALED_AS_GENERATOR_CONSISTENCY` (or stronger) to every result.md verdict header.
3. Regrade CR129b to BOUNDARY in its lock file; do not cite the universal sign rule.
4. Rephrase CR131/CR132/CR134 result.md text to acknowledge per-class fits.
5. Create CR135b (or follow-up) to derive at least one form (CR130's symmetric-group argument is the closest existing piece) from first principles, to provide one Tier-1 anchor.
6. Hold any "zero free parameters" claim in the manuscript until at least one forward-blind test resolves with new CR119 rows.

End of roll-up.
