# AUDIT: CR129 OCTET_COMPOSITE 3-Body Mass Law v1.0

**Tier verdict:** 2 — PASS_WITH_REWORD
**Headline finding:** `M = 36*(a²+b²+c²)` fits 76/76 in-sample triples and 28/28 2-body OCTET rows via the CR128 BCP formula — but the result.md's self-hash is wrong, the WC on "why 3-body has no antisymmetric term" is admitted to be "observed structurally, not derived", and 76 distinct triples does not exhaustively cover the (8 choose 3 with repetition) = 120 multiset space.

## Criteria results

| Criterion | Result | Note |
|---|---|---|
| C1 HASH_CHAIN_INTEGRITY | PARTIAL FAIL | Upstream hashes verify. Self-cited `CR129_law_lock_sha256 = 210e174e…` does NOT match actual file `041a487c…`. Downstream uses correct value. |
| C2 FALSIFIER_PRECOMMITTED | PASS | "ONE single future 3-body OCTET row whose M_native deviates from the formula by any non-zero integer" is concrete. |
| C3 WRONG_CONTROLS_LOAD_BEARING | FAIL | WC7 ("symmetry observation noted") admits the no-antisymmetric-term claim is "observed structurally, not derived." None of WC1–WC7 is a destructive control. The closest is WC5 (2-body OCTET rows use CR128 formula) — which is a CONFIRMATION, not a null-control. |
| C4 FREE_PARAMETERS_HONESTLY_ZERO | FAIL | The coefficient `R*D = 36` is one of many factorizations of 36 in the SAM algebra (also `α_H²*9 = 4*9`, `(R+D)²·… ≈`). Why R*D specifically? Because it fits. The functional form `Sum a_i²` was selected from alternatives like `Sum a_i*b_i` or `(Σa_i)² + k·Σ(a_i-a_j)²`. CR130 in fact rewrites it as the latter (Newton identity), showing the form was non-unique. |
| C5 IN_SAMPLE_DISCLOSED | PASS | WC3: "Formula M_native = R*D*(a^2+b^2+c^2) was extracted by inspecting the OCTET 3-body row collection. In-sample 100% match confirms generator consistency…" Honest. |
| C6 VERDICT_GRADE_MATCHES_EVIDENCE | BOUNDARY | SEALED is overclaimed; should be "_GENERATOR_CONSISTENCY_SEALED_FORWARD_BLIND_PENDING". |
| C7 APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS WITH NIT | Algebra extension and 4-body extension both correctly routed to appeal CRs. |
| C8 TEXT_MATCHES_VERDICT | PASS | Headline 76/76 + 28/28 is defensible. |
| C9 TIMESTAMP_ORDERING_FORMULA_THEN_DATA | FAIL | `law_committed_utc = 2026-06-15T22:50:14Z`, 20 minutes after CR128. No precommit hash predating the inspection of the OCTET 3-body rows in CR119. |

## Specific demands

- REWORD line 6: `_SEALED` → `_SEALED_AS_GENERATOR_CONSISTENCY`.
- REWORD line 109: `CR129_law_lock_sha256 = 210e174e…` → actual `041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710`.
- REWORD line 129 WC7: "fully symmetric structure is observed in-sample on 76 triples; algebraic reason (no linear antisymmetric in S_n on multisets) is provided in CR130 but is not a derivation of why R*D is the specific coefficient."
- RETEST: out-of-sample split. Hold out 20 random triples, fit on 56, predict the held-out 20. Currently no train/test split.
- RETEST: try `R²*(a²+b²+c²) = 144*Σ` or `D²*(a²+b²+c²) = 9*Σ` and demonstrate they fail. Currently no alternate-coefficient null control.
- APPEAL_CR: first-principles derivation of why prefactor = R*D rather than R² or 4R; CR130 makes this an open question but should be a named appeal CR.

## Quoted evidence

> "WC7_symmetry_observation_noted -- The 3-body formula is fully symmetric in (a, b, c) -- no antisymmetric term. Unlike the 2-body case (where |a-b| is essential), 3-body M_native depends only on the multiset {a, b, c}. **This is observed structurally, not derived.**"

> "Formula M_native = R*D*(a^2+b^2+c^2) was extracted by inspecting the OCTET 3-body row collection."

> "Distinct 3-body triples observed: 76" (out of 120 multisets possible in 8-element algebra of size 3 with repetition; 36% coverage gap)

> "CR129_law_lock_sha256 = 210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360" (actual: 041a487c…)

## Verdict text

CR129 reaches the same standard as CR128/CR128b — clean inductive extraction with forward-blind commitment but no train/test split and no destructive wrong-controls. Tier 2. The non-uniqueness of the coefficient (R*D vs R² vs 4R) is the load-bearing weakness; CR130 partially compensates by showing the algebraic rewriting, but CR129 alone does not derive the form. Manuscript must say "generator consistent 76/76; coefficient choice R*D is observational, not derived."
