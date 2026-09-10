# CR239 — Safer Native Mass / Gravity Bridge Design

**Working title:** CR239 Native Source Write to Measured Mass / Gravity Bridge  
**Status:** Design draft / precommit scaffold  
**Purpose:** Test whether the CR238 completed source write \(Q(P)\) can be bridged to measured inertial and gravitational mass with one global dimensional bridge \(\mu_Q\), while protecting SAM from unfairly failing against low-confidence evaluated or extrapolated mass values.

---

## 1. Core Question

CR238 left one measured-unit bridge open:

\[
m_i(P)=m_g(P)=\mu_Q Q(P).
\]

CR239 asks:

\[
\boxed{\text{Can one global }\mu_Q\text{ convert native }Q(P)\text{ into measured inertial/gravitational mass?}}
\]

The test must distinguish three outcomes:

1. **Direct bridge:** \(Q(P)\) is proportional to measured mass through one \(\mu_Q\).
2. **Structured residual:** \(Q(P)\) is a native source/coupling skeleton, but measured mass needs a binding/readout residual.
3. **Fail:** \(Q(P)\) does not outperform simple controls such as \(A=Z+N\), \(Z\), or monotone randomized ladders.

---

## 2. Locked Native Inputs

CR239 must use the CR238 typed spine output, not raw injected constants.

From CR238:

\[
\mathcal F=81,
\qquad
S=8,
\qquad
\alpha_H=2.
\]

Derived:

\[
D=3,
\qquad
R=12,
\qquad
\kappa=\frac{7117}{768},
\qquad
g=\frac{1}{64}.
\]

Element/source engine:

\[
N(Z)=Z+\left\lfloor\frac{Z}{R}\left\lfloor\frac{Z-1}{R}\right\rfloor\right\rfloor.
\]

\[
G(Z,N)=Z\kappa+(N-Z)g.
\]

\[
Q(Z,N)=S\,G(Z,N).
\]

For canonical SAM:

\[
Q=8G=7G+G.
\]

---

## 3. Measurement-Layer Warning

AME2020, NUBASE, and later mass tables must be treated as **reveal/evaluation layers**, not unquestionable authority layers.

CR239 may only hard-fail against high-confidence experimentally measured masses.

Evaluated or extrapolated mass rows must be separated into confidence lanes.

Use this rule:

\[
\boxed{\text{High-confidence measured masses can falsify the direct bridge.}}
\]

\[
\boxed{\text{Evaluated/extrapolated rows produce residual maps or prediction conflicts, not automatic failure.}}
\]

---

## 4. Data Lanes

### Lane A — High-Confidence Measured Masses

Use only rows with direct experimental mass measurements and small reported uncertainties.

This is the strictest lane.

CR239 may hard-fail the direct bridge here.

Required columns:

```text
Z
N
A
symbol
mass_atomic_u
mass_uncertainty_u
measurement_class
source_table
source_reference
confidence_lane
```

Required lane label:

```text
LANE_A_HARD_MEASURED
```

Hard-fail logic applies only to Lane A.

---

### Lane B — Evaluated Recommended Masses

Use AME-style recommended values with uncertainty weighting.

For each row:

\[
z(P)=\frac{m_{\mathrm{eval}}(P)-\mu_QQ(P)}{\sigma_{\mathrm{eval}}(P)}.
\]

This lane evaluates whether SAM is outside the evaluator uncertainty, but it does **not** automatically kill SAM if the row is network-adjusted, weakly connected, or dependent on model assumptions.

Required lane label:

```text
LANE_B_EVALUATED
```

Allowed verdicts:

```text
PASS_LANE_B_WITHIN_UNCERTAINTY
BOUNDARY_LANE_B_STRUCTURED_RESIDUAL
FAIL_LANE_B_SYSTEMATIC_MISMATCH
```

---

### Lane C — Extrapolated / Frontier Values

Rows marked as extrapolated, estimated, frontier, or otherwise weakly constrained go here.

This lane is not a hard-fail lane.

It is a prediction lane.

Required lane label:

```text
LANE_C_EXTRAPOLATED_FRONTIER
```

Allowed verdicts:

```text
PREDICTION_CONFLICT_WITH_EVALUATOR
BOUNDARY_FRONTIER_ROW
SAM_FORWARD_PREDICTION_RECORDED
```

Use this lane especially for superheavy and neutron-rich rows where evaluated tables may rely on extrapolation.

---

### Lane D — Post-AME2020 Measurement Challenge

Freeze SAM predictions against the older reference layer, then compare to later direct measurements.

This is the best lane for testing whether SAM can outperform extrapolated/evaluated expectations.

Question:

\[
\boxed{\text{Does SAM predict later direct measurements better than the prior evaluated/extrapolated table?}}
\]

Required lane label:

```text
LANE_D_POST_EVALUATION_CHALLENGE
```

Compare:

\[
|m_{\mathrm{new}}-m_{\mathrm{SAM}}|
\]

against:

\[
|m_{\mathrm{new}}-m_{\mathrm{prior\ eval}}|.
\]

Pass condition for this lane:

\[
\mathrm{median}\left(|m_{\mathrm{new}}-m_{\mathrm{SAM}}|\right)
<
\mathrm{median}\left(|m_{\mathrm{new}}-m_{\mathrm{prior\ eval}}|\right)
\]

and the result must survive uncertainty weighting.

---

## 5. Atomic vs Nuclear Mass Rule

CR239 must compare like with like.

AME-style tables commonly report **atomic masses**.

SAM source address includes electrons:

\[
P_{Z,N}=Zp+Nn+Ze.
\]

Therefore, the first CR239 comparison should use atomic masses.

If a nuclear-mass lane is added later, it must explicitly subtract electron masses and electron binding corrections:

\[
m_{\mathrm{nucleus}}
=
 m_{\mathrm{atom}}-Zm_e+E_{\mathrm{electron\ binding}}/c^2.
\]

Do not mix atomic masses and nuclear masses in the same score.

---

## 6. Gate 1 — Ratio-Only Test

This gate uses no \(\mu_Q\).

For pairs \((P_i,P_j)\):

\[
\frac{m(P_i)}{m(P_j)}
\stackrel{?}{=}
\frac{Q(P_i)}{Q(P_j)}.
\]

Define ratio error:

\[
\epsilon_{ij}^{\mathrm{ratio}}
=
\left|
\frac{m_i/m_j}{Q_i/Q_j}-1
\right|.
\]

This is the cleanest first stress test because the unit bridge cancels.

If this gate fails badly in Lane A, one global \(\mu_Q\) cannot rescue the direct bridge.

---

## 7. Gate 2 — One-Anchor Unit Bridge

Choose exactly one anchor before scoring.

Recommended first anchor:

\[
{}^{12}\mathrm C,
\qquad
m({}^{12}\mathrm C)=12u.
\]

Compute:

\[
\mu_Q=\frac{12u}{Q({}^{12}\mathrm C)}.
\]

Freeze \(\mu_Q\).

Then predict:

\[
m_{\mathrm{SAM}}(P)=\mu_QQ(P).
\]

Residual:

\[
\epsilon(P)=\frac{m_{\mathrm{measured}}(P)-m_{\mathrm{SAM}}(P)}{m_{\mathrm{measured}}(P)}.
\]

No row-by-row correction is allowed in the direct bridge test.

---

## 8. Gate 3 — Isotope Increment Test

This is the truth-serum test.

For fixed \(Z\), increasing neutron number by one changes:

\[
G(Z,N+1)-G(Z,N)=g=\frac{1}{64}.
\]

Therefore:

\[
Q(Z,N+1)-Q(Z,N)=Sg=8\cdot\frac{1}{64}=\frac{1}{8}.
\]

If the direct bridge is true, then the predicted mass increment is:

\[
\Delta m_{\mathrm{SAM}}=\mu_Q\cdot\frac{1}{8}.
\]

Compare this to measured isotope mass spacing.

Possible outcomes:

- If isotope increments agree broadly, the direct bridge is very strong.
- If isotope increments fail but residuals are structured, \(Q(P)\) may be the source skeleton rather than full measured rest mass.
- If increments fail randomly, the direct mass bridge likely fails.

---

## 9. Gate 4 — Residual Structure Test

If the direct bridge does not close, do not discard the result immediately.

Define:

\[
\Delta m(P)=m_{\mathrm{measured}}(P)-\mu_QQ(P).
\]

Then test whether residuals track:

- nuclear binding structure;
- neutron excess \(N-Z\);
- shell closures;
- SAM cycle boundaries;
- stability/clock state;
- actinide or superheavy frontier status.

A structured residual means:

\[
Q(P)=\text{native source skeleton}
\]

and

\[
\Delta m(P)=\text{binding/readout correction candidate}.
\]

That is a boundary result, not an automatic failure.

---

## 10. Gate 5 — Gravitational Source Readout

If \(m(P)=\mu_QQ(P)\) is viable, the exterior accumulation field becomes:

\[
A_P(r)=\frac{2G_N\mu_QQ(P)}{c^2r}.
\]

This closes the chain:

\[
Q(P)
\rightarrow
m_i=m_g
\rightarrow
A_P(r).
\]

The composition-level test is:

\[
Q_{\mathrm{sample}}=\sum_k n_kQ(P_k).
\]

\[
M_{\mathrm{SAM}}=\mu_QQ_{\mathrm{sample}}.
\]

Then compare against measured bulk inertial mass and gravitational source behavior.

The composition test is downstream. Do not run it before the isotope/atomic-mass gates are understood.

---

## 11. Wrong Controls

Run all controls under the same lane structure.

### WC1 — \(R=10\)

Regenerate \(N(Z)\), \(G\), and \(Q\) with \(R=10\).

Expected: degradation.

### WC2 — \(R=11\)

Expected: degradation.

### WC3 — \(R=13\)

Expected: degradation.

### WC4 — \(S=7\)

Expected: typed bridge fails or degrades.

### WC5 — \(S=9\)

Expected: typed bridge fails or degrades.

### WC6 — shuffled \(N(Z)\)

Shuffle neutron counts among \(Z\) values with fixed seed:

```text
20260621
```

Expected: degradation.

### WC7 — shuffled \(Q(P)\)

Shuffle \(Q\) values among rows.

Expected: ratio and mass-bridge scores degrade.

### WC8 — monotone random ladder

Generate a monotone fake \(Q_{\mathrm{rand}}(Z)\) with the same endpoint range.

Expected: SAM should outperform monotone fake ladders if the bridge is meaningful.

### WC9 — simple \(A=Z+N\) baseline

Compare SAM \(Q(P)\) against the simplest mass-number baseline:

\[
A=Z+N.
\]

This is the most important practical control.

CR239 is only impressive if \(Q(P)\) beats or structurally improves on \(A\).

---

## 12. Output Files

Recommended directory:

```text
CR239_NATIVE_MASS_GRAVITY_BRIDGE/
```

Required outputs:

```text
CR239_PRECOMMIT.md
CR239_runner.py
CR239_summary.json
CR239_result.md
CR239_lane_a_hard_measured.csv
CR239_lane_b_evaluated.csv
CR239_lane_c_extrapolated_frontier.csv
CR239_lane_d_post_evaluation_challenge.csv
CR239_ratio_test.csv
CR239_one_anchor_bridge.csv
CR239_isotope_increment_test.csv
CR239_residual_structure.csv
CR239_wrong_controls.csv
CR239_input_manifest.csv
HASHES.txt
```

---

## 13. Verdict Classes

### Strong Direct Bridge Pass

```text
PASS_CR239_DIRECT_MASS_GRAVITY_BRIDGE
```

Requires:

- Lane A ratio test passes.
- One global \(\mu_Q\) predicts measured masses within predeclared tolerance.
- Isotope increment test does not break the bridge.
- SAM beats \(A=Z+N\) and wrong controls.

Allowed claim:

```text
SAM's completed source write Q(P) bridges directly to measured inertial and gravitational mass through one dimensional constant μ_Q.
```

---

### Boundary / Structured Residual

```text
BOUNDARY_CR239_SOURCE_SKELETON_WITH_STRUCTURED_RESIDUAL
```

Use if:

- \(Q(P)\) tracks mass directionally or by rank;
- direct one-scale conversion leaves systematic residuals;
- residuals are structured by binding, shell, neutron-excess, or SAM-cycle terms.

Allowed claim:

```text
Q(P) behaves as a native source/coupling skeleton, but measured rest mass requires a binding/readout residual map.
```

---

### Prediction Conflict Lane

```text
PREDICTION_CR239_FRONTIER_CONFLICT_WITH_EVALUATED_TABLE
```

Use for Lane C or Lane D when SAM disagrees with extrapolated/evaluated masses.

Allowed claim:

```text
SAM records a forward prediction conflict with the evaluated/extrapolated mass layer; this is not a hard failure unless later high-confidence measurements resolve against SAM.
```

---

### Fail

```text
FAIL_CR239_DIRECT_BRIDGE
```

Use if Lane A hard-measured masses show that \(Q(P)\) fails ratio and one-anchor tests and does not beat simple controls.

Allowed claim:

```text
Raw Q(P) is not measured mass. It remains a native substrate-coupling/source variable unless a separate bridge is derived.
```

---

## 14. Disallowed Claims

Do not claim:

```text
SAM failed because it disagreed with AME2020 extrapolated values.
```

Do not claim:

```text
SAM proved inertial and gravitational mass are Q(P).
```

Do not claim:

```text
A row-by-row fitted μ_Q closes the mass bridge.
```

Do not claim:

```text
Atomic and nuclear masses were compared interchangeably.
```

---

## 15. Minimal Honest Headline Options

If direct bridge passes:

```text
CR239_PASS_DIRECT_NATIVE_MASS_GRAVITY_BRIDGE__ONE_MU_Q__LANE_A_HARD_MEASURED
```

If structured residual:

```text
CR239_BOUNDARY_Q_AS_SOURCE_SKELETON__MEASURED_MASS_REQUIRES_RESIDUAL_MAP
```

If frontier conflict:

```text
CR239_PREDICTION_FRONTIER_MASS_CONFLICT__NOT_HARD_FAIL_UNTIL_DIRECT_MEASUREMENT
```

If fail:

```text
CR239_FAIL_RAW_Q_NOT_MEASURED_MASS__DIRECT_BRIDGE_REJECTED
```

---

## 16. Plain-English Summary

CR239 should not ask whether AME2020 is perfectly right.

It should ask whether SAM's native source write \(Q(P)\) survives contact with measured mass data under a fair confidence-lane design.

The strongest possible result is one global bridge:

\[
m_i=m_g=\mu_QQ(P).
\]

The next-best result is still useful:

\[
Q(P)=\text{source skeleton},
\qquad
m(P)=\mu_QQ(P)+\Delta m_{\mathrm{binding}}(P).
\]

The key is to separate hard measurements from evaluated/extrapolated frontier values before deciding what counts as a failure.
