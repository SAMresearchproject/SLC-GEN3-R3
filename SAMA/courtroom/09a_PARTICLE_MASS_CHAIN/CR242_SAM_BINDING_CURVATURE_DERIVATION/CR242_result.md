# CR242 SAM Binding-Curvature Derivation

Verdict: `BOUNDARY_CR242_SAM_TYPED_BINDING_SURFACE_REPRODUCES_BW_STRUCTURE`

## Question

CR242 tests the positive binding residual:

```text
B_u = A - m_measured
```

The coefficient fits use CR240 Lane A non-anchor rows only. The CR241 holdout is
reserved for out-of-sample testing.

## Model Comparison

| model | train RMS u | train R2 | test RMS u | test R2 |
|---|---:|---:|---:|---:|
| BW_BENCHMARK_FIT | 0.0038966335446124 | 0.990095520928387 | 0.00348340186706259 | 0.98728468142698 |
| SAM_TYPED_BASIS_FIT | 0.00308759365477247 | 0.993781397624767 | 0.00360531405821861 | 0.986379084803202 |
| SAM_ZERO_FREE_TYPED_CANDIDATE | 0.0426930640360485 | -0.188959765900887 | 0.0639858656432688 | -3.29030516806637 |

SAM/BW holdout RMS ratio: `1.03499802658682`

## Verdict Logic

STRONG pass: `False`

BOUNDARY pass: `True`

FAIL condition present: `False`

## Wrong Controls

- WC1_shuffled_train_B_u_labels: PASS (test RMS=0.06131921802425791, test R2=-2.9401549461027554)
- WC2_train_test_boundary_guard: PASS (test RMS=, test R2=)
- WC3_untyped_decimal_basis: COMPLETE (test RMS=0.005813830280858115, test R2=0.9645803076922601)
- WC4_zero_free_typed_candidate: COMPLETE (test RMS=0.06398586564326877, test R2=-3.2903051680663715)
- WC5_disallowed_claim_guard: PASS (test RMS=, test R2=)

## Claim Boundary

CR242 reports a binding-curvature surface test only. It does not fit the CR241
holdout, does not promote C5/C6/C7, and does not assert a theorem-grade nuclear
binding derivation.
