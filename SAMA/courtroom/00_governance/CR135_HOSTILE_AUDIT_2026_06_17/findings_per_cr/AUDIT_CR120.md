# AUDIT_CR120 — Hostile Findings

**CR:** `CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE`
**Sealed lock sha256:** `09cf6beaf8bd6fb1520b740b4451491a664e220897e4803f514fd9adcd9e604d`
**Sealed at:** `2026-06-15T19:20:34Z`
**Headline under attack:** `H_reveal = R²(1−2⁻ᴰ) − D²/R = 144·7/8 − 9/12 = 125.25 GeV EXACT`
**Auditor stance:** adversarial; no benefit of the doubt.

---

## Tier Verdict

**TIER 6 — HASH_CHAIN_BREAK** (primary)
**TIER 4 — DEMAND_RETEST** (secondary, C9 evidence-of-ordering insufficient)

CR120 fails two distinct criteria. The hash-chain break is the more structurally severe issue; the formula-then-data ordering challenge is the one most damaging to the manuscript's headline. Both must be cured before this CR carries the Higgs claim into the manuscript.

---

## Pass/Fail per Criterion (C1–C9)

| # | Criterion | Verdict | Notes |
|---|---|---|---|
| C1 | HASH_CHAIN_INTEGRITY | **FAIL** | All 33 `qp091*`/`qp092a-b` upstream `summary.json` files live in `C:/VS/quantum_phase/artifacts/`, not in `The_Courtroom`. Confirmed by glob: zero `qp091*` or `qp092*` paths under `C:/VS/The_Courtroom`. Only their sha256 fingerprints are stored in `CR120_qp091_chain_intake_lock.json`. The bytes are orphaned references. |
| C2 | FALSIFIER_PRECOMMITTED | PASS (partial) | Three forward-blind predictions (`CR120_PRED_1/2/3`) each carry a one-line falsification criterion. **However** `CR120_PRED_1`'s falsifier is "outside the 125.25 +/- structural uncertainty band" — the structural band is undefined. Not falsifiable by a single observation as written. |
| C3 | WRONG_CONTROLS_LOAD_BEARING | PASS | Inside `qp091t_controls.csv`, C7 (R=10), C8 (D=2) numerically break the form (87.5, 108). These are real wrong controls. WC list in the CR itself is mostly procedural ("does not modify…") rather than load-bearing — that part is sanity-check theater. |
| C4 | FREE_PARAMETERS_HONESTLY_ZERO | **FAIL** | The functional form `R²(1−2⁻ᴰ) − D²/R` is composite of two pieces. The first piece alone (R²·7/8 = 126) overshoots the PDG target by 0.6%. The −D²/R correction (= 0.75) lands the result exactly on 125.25. The CR claims zero free parameters but does not document an *independent* derivation of *why* D²/R is the correction (rather than D/R, D³/R², D²/R², etc.). qp091u's "wrong controls reject D²/D⁴, R¹⁰/R²⁴" is an after-the-fact survival test, not a forward derivation. The form *choice* among admissible algebraic siblings is a hidden degree of freedom. |
| C5 | IN_SAMPLE_DISCLOSED | **FAIL** | qp091t was generated on 2026-06-15T06:09:45Z. qp091p (04:27Z) had `H_earth_local = 125.247738…` with gap of 2.26 MeV to a CR062 target of 125.25. The target value 125.25 was visible the whole time. The CR does not characterise the 125.25 closure as *generator consistency* with an in-sample target; it presents it as a first-principles closed form. Quoted from `CR120_HEADLINE_HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY.md`: "derived from `{R=12, D=3}` alone with **zero free parameters**, **no H input**." This overstates the epistemic content of the chain. |
| C6 | VERDICT_GRADE_MATCHES_EVIDENCE | PARTIAL FAIL | The verdict `CR120_QP091_CHAIN_INTAKE_SEALED__HIGGS_125_25_EXACT_FROM_R_AND_D_ONLY` reads as if a derivation, not an intake, was sealed. The CR is an intake; treating its headline as established physics is a category mistake the verdict text invites. Note also `qp091_chain_all_passed = false` (boundary count = 2) — the verdict says SEALED but two upstream stages failed PASSed bit. |
| C7 | APPEAL_VS_FALSIFICATION_BRIGHT_LINE | PASS (weak) | `CR120_PRED_3` distinguishes "fit to PDG precision" (= falsification, chain has hit a frontier) from "native operator extension" (= appeal). The line is drawable, though qp091ad's epsilon residual escape hatch is wide and post-hoc. |
| C8 | TEXT_MATCHES_VERDICT | **FAIL** | "EXACT" is a numerical statement about a specific arithmetic identity, not about a physical-prediction comparison. The result.md says "EXACT" eight times. The qp091ad BOUNDARY (open epsilon residual) means the underlying chain is not exact at the precision the manuscript would want to claim. The wrong-control WC3 acknowledges this ("qp091ad is a FINER-SCALE epsilon residual at the surface-debit fine-structure level; 125.25 itself is closed EXACTLY at qp091t") — but "EXACT at qp091t" is a tautological statement about an algebraic identity, not about empirical agreement. |
| C9 | TIMESTAMP_ORDERING_FORMULA_THEN_DATA | **FAIL — SEVERE** | Direct evidence from the qp091 chain inside `C:/VS/quantum_phase/artifacts/`: `qp091r` (sealed 2026-06-15T05:34:09Z) explicitly lists `126 − D²/R = 125.25` under a section titled "Wrong Lane Control" — meaning the form `126 − D²/R = 125.25` was identified as a value-match BEFORE the qp091t closure was sealed. The form was promoted from "wrong lane control" at qp091r → "Native / Reveal Surface" at qp091s (05:54Z) → "active_derivation" at qp091t (06:09Z) within 35 minutes. This is exactly the pattern C9 is designed to catch: the form was constructed against a visible target, not declared and then tested. CR120 does not address this. |

---

## Specific Demands

### DEMAND-CR120-A (hash-chain break, blocks manuscript)
**Required:** Either ingest the 33 qp091/qp092 `summary.json` files into a `The_Courtroom/upstream_artifacts/qp091_chain/` directory and re-seal the intake lock, OR strike all "intaken" language from the CR and downgrade it to a "fingerprint-only" reference manifest. As currently sealed, the intake hashes are pointers to a directory outside the Courtroom's immutability boundary.

### DEMAND-CR120-B (C4 hidden form choice)
**Required:** A separate CR that enumerates the family of admissible algebraic corrections to `R²(1−2⁻ᴰ)` (e.g., `D/R`, `D²/R²`, `D²/R`, `D³/R²`) and shows from SAM first principles — not from data — why `D²/R` is the unique allowed surface debit. Until that exists, `free_parameters = 0` is a typographic claim, not a defensible one.

### DEMAND-CR120-C (C9 ordering rebuttal)
**Required:** REWORD CR120 result.md to acknowledge the qp091r → qp091s → qp091t form-promotion path explicitly, and characterise the 125.25 closure as the *retroactive* identification of a clean algebraic decomposition of a known target rather than an a-priori prediction. Alternative defense: identify any pre-qp091r artifact in the SAM corpus that declares `R²(1−2⁻ᴰ) − D²/R` as the EW closure form before any comparison to 125.25.

### DEMAND-CR120-D (manuscript reframing)
**Required:** If the manuscript intends to use 125.25, drop "EXACT" rhetoric. Frame the claim as: "the SAM closed-loop algebra admits a two-term decomposition `R²·7/8 − D²/R` that reproduces the PDG Higgs mass to the displayed precision." That is defensible. "Zero free parameters, exact derivation" is not.

### DEMAND-CR120-E (boundary disclosure)
**Required:** Result.md must surface `qp091_chain_all_passed = False` and the two BOUNDARY stages (qp091b missing EW normalization primitive, qp091c missing neutral rotation metric) in the headline, not bury them in a counts block.

---

## Quoted Evidence

From `qp091r/QP091R_result.md` (sealed 05:34:09Z, ~35 min before qp091t):

> ## Wrong Lane Control
> ```text
> 126 - D^2/R = 125.250000000000000000000000000000 GeV
> ```
> That lands on the `125.25` reveal row, but it is not the qA-bounce lane.

From `qp091t/qp091t_summary.json` (sealed 06:09:45Z):

> `"active_derivation": "H_native = R^2*(1-2^-D); H_reveal = H_native - D^2/R"`

From `qp091t/qp091t_controls.csv` C9:

> `"Is H_native generated from R and D before comparison to the reveal row?"` → "no Higgs target in parent generation" → PASS

But the same form was sitting in `qp091r` as a "Wrong Lane Control" 35 minutes earlier *because the 125.25 target was visible.* C9 of qp091t passes only on the narrow technicality that R and D themselves are not the Higgs value — the *choice* of `−D²/R` as the correction term was made with 125.25 in view. C9 of qp091t is not the answer to the C9 audit criterion.

From `CR120_qp091_chain_intake_lock.json`:

> `"sealed_at_utc": "2026-06-15T19:20:34Z"` → 13 hours AFTER qp091t generation

From CR120 runner (line 83):

> `QP_DIR = Path(r"C:/VS/quantum_phase/artifacts")`

Confirms hash chain points outside Courtroom.
