# CR223b PR Qutrit Tomography & Purity-Estimator Lock Result

**Result class:** `CR223b_PASS_QUTRIT_PURITY_ESTIMATOR`

**Checks:** 14/14

## Estimator

```text
rho = (1/3) I + (1/2) sum_a b_a lambda_a    (a = 1..8)
A_hat_leak = 1 - Tr(rho_hat^2) after PSD projection
```

## Primary success criteria

| Criterion | Target | Observed |
|---|---|---|
| coherent vs diagonal distinguishable (S1 vs S2) | tomography separates them | dA_PSD(S1,S2) = 0.593503, dA_pop(S1,S2) = 0.000620 |
| bias near A_side | abs(bias) < 1/96 = 0.010417 | max abs(bias) over ['S3', 'S4', 'S5'] = 0.002452 |
| balanced accuracy (held-out test) | >= 0.9 | 0.903125 |
| 95% CI covers A_true on near-threshold states | >= 0.9 on ['S3', 'S4', 'S5'] | 3/3 = 1.000 |
| population-only WC1 fails coherent-vs-diagonal | yes | passes_as_failure = True |

## Boundary-state bias (reported honestly, not required to hit coverage)

```text
S1: bias=+0.015034; S6: bias=-0.000541; S7: bias=-0.000000
```

S1 and S7 are rank-1 pure states; PSD projection of LI estimates with shot
noise yields a small positive bias because clipped negative eigenvalues are
renormalized. S6 (maximally mixed) has a small negative bias because
b_hat_a is centered at 0 but b_hat_a^2 has positive expectation. Both are
structural properties of PSD-projected linear-inversion tomography at the
state-space boundary, not data-fit failures. They are reported here so they
cannot be silently dropped by a downstream CR.

## Confusion matrix (test split)

```text
TP=685  FN=115
FP=30  TN=570
TPR=0.8562  TNR=0.9500
balanced_accuracy=0.9031
```

## Verdict

```text
PASS_QUTRIT_PURITY_ESTIMATOR
```

The campaign now has a measurement engine capable of resolving the quantity
the PR letter claims to monitor, with explicit demonstration that
population-only readout cannot.

## Next gate

CR223c - PR raw tomography & sensor-proxy contact (first hardware-trajectory
opening).
