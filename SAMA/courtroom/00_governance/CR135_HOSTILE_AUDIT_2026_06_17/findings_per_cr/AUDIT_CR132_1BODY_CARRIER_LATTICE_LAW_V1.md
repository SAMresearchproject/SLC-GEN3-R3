# AUDIT: CR132 1-Body Carrier Lattice Law v1.0

**Tier verdict:** 4 — DEMAND_RETEST
**Headline finding:** With only 6 data points (one per carrier class) the "law" `M = α_H^i · D^j` is a 6-cell lookup table where (i,j) is fit per-class — strictly equivalent to "the carrier masses are whatever they are"; WC4 admits the initial C1=9/8 was tried and discarded after COLOR_OWNER didn't fit, replaced by C1=1 via "user-directed pivot"; result.md self-hash is wrong.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream CR119 verified. Self-cited `CR132_law_lock_sha256 = f4811aa1…` does NOT match actual `fbc25a88…`. |
| C2 FALSIFIER_PRECOMMITTED | BOUNDARY | "ONE single future carrier row whose M_native deviates from the locked lattice value" is concrete, but with each carrier class having n=1 in the current catalog, the falsifier resolves only if a new instance of an EXISTING carrier class appears — that may never happen. A new carrier class warrants an appeal CR, not a violation (the appeal escape). |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | WC4 is a confession (C1=9/8 tried and failed); WC5 is a definitional choice (treat M=0 as a valid lattice point); WC6 excludes other classes. None destructively tests the lattice assignments. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | 6 carriers, 4 with (i,j) assignments. With (i,j) ∈ small integers and M in {0, 8, 9, 18, 81}, fitting `α_H^i · D^j` to each is trivial: 18 = 2·3², 9 = 3², 81 = 3⁴, 8 = 2³. Any small integer M can be written as such a product if M has prime factors only in {α_H, D} = {2, 3}. This is not a law — it is the observation that all 4 massive carriers happen to be 2^a · 3^b. The (i,j) per class is 8 fit parameters disguised as a lattice. |
| C5 IN_SAMPLE_DISCLOSED | PARTIAL PASS | WC5/WC6 disclose the inductive origin and the C1=9/8 → C1=1 pivot. But result.md does not explicitly say "this is a lookup table over 6 single-instance classes". |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | FAIL | SEALED is wrong. 6 data points × 6 free-form (i,j) assignments has degrees of freedom equal to data points. This is a fit with no residual. |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | FAIL | "Addition of a NEW carrier class warrants an appeal CR with extended lattice" — this is a perfect escape. Any future carrier row at any mass can be re-lattice-fit because new (i,j) is allocated per class. The law cannot be falsified by NEW class data. |
| C8 TEXT_MATCHES_VERDICT | FAIL | Line 33: "Bosons live on the lattice directly" — language implies derivation. Actually the bosons happen to have masses that factor over {2,3}. Description ≠ explanation. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | WC4: C1=9/8 was tried first, failed, then C1=1 was chosen. Form was iterated against data. No precommit. |

## Specific demands

- REWORD line 6: `_SEALED` → `_SEALED_AS_PER_CARRIER_LOOKUP_TABLE`.
- REWORD line 33 and elsewhere: "Bosons live on the lattice" → "Carrier M_native values happen to factor as 2^i · 3^j; (i,j) is assigned per class."
- REWORD line 78: `CR132_law_lock_sha256 = f4811aa1…` → actual `fbc25a887e01e8b6d5d84bb7a0fba8b4e26e1eca1b471caf3043dc9ba9559a32`.
- REWORD WC4: this is iteration history, not a wrong-control.
- RETEST: PRECOMMIT (i,j) for one class BEFORE inspecting its M_native. Currently every (i,j) is post-hoc.
- RETEST: predict (i,j) for a new carrier class from first principles before its M_native is observed.
- APPEAL_CR: derive (i,j) from SAM algebra; without this, CR132 is a tautology over a 6-element dataset.

## Quoted evidence

> "Initial probe tried C1 = 9/8 (from CR129b's middle-slot surcharge). Three carriers fit (9/8)*X form but COLOR_OWNER did not. User-directed pivot to C1 = 1 closed all six rows cleanly."

> "Each carrier sits at its own (α_H, D) lattice point." (a fit, not a law)

> "Carrier rows tested: **6** (each carrier class has n=1 in CR119)"

> "Addition of a NEW carrier class would warrant a lattice extension via appeal CR, not a v1.0 violation."

> "CR132_law_lock_sha256 = f4811aa11df61be7a9fa01d09dc15775f816ab153313dccda022a3b92491ec17" (actual: fbc25a88…)

## Verdict text

CR132 is the suite's weakest "law" — 6 data points × per-class (i,j) assignments is not zero free parameters; it is one free parameter per class, dressed up as a lattice. The "law" is the observation that all 4 massive carriers have prime factors only in {2, 3}; for small integers this is unremarkable. Tier 4 — DEMAND_RETEST. Manuscript must NOT cite CR132 as a law; can cite the observation that all carrier masses factor over {α_H, D}, but with a free (i,j) lookup per class.
