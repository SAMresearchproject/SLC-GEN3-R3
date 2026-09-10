# CR223a PR Observable Identity Lock Result

**Result class:** `CR223a_PASS_PR_OBSERVABLE_IDENTITY_LOCKED`

**Checks:** 21/21

## Locked observable

```text
A_leak(t) = 1 - Tr(rho(t)^2)
t_fire    = inf{ t : A_leak(t) >= 1/24 }
A_side    = 1/24
```

## Four-model firing-coefficient table

| Model | Coefficient t_fire/T2 | Source |
|---|---:|---|
| M1 scalar exponential-purity surrogate | 0.0212798 | closed form: ln(24/23)/2 |
| M2 two-level pure dephasing | 0.0435057 | closed form: ln(12/11)/2 |
| M3 loaded qutrit equal pure dephasing | 0.0354358 | closed form: ln(4224/3935)/2 |
| M4 loaded qutrit NV Lindblad CR068a, analytic root | 0.0289615 | bisection on analytic Lindblad solution |
| M4 CR068a sample-grid alarm (200 samples / 100 us) | 0.0291460 | first sample with A_leak >= 1/24 |

The analytic Lindblad root for M4 (0.0289615) sits between CR068a sample
57 (0.028643, just below threshold) and sample 58
(0.029146, first crossing), confirming the simulator
output is the discrete-grid version of this Lindblad model.

## Hardware default observable (locked)

```text
t_fire^pred = inf{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }
```

`rho_cal(t)` is generated from independently measured T1, T2, SPAM, and pulse
parameters for the selected platform. CR223a does NOT lock a universal
`c0 * T2` coefficient.

## Verdict

```text
PASS_OBSERVABLE_IDENTITY_LOCKED
```

The repository now has one unambiguous hardware observable definition. Any
later CR that cites a single `c0 * T2` figure must declare which row of this
table it comes from. M3 != M2 != M1 and M3 != M4 are recorded as structural
checks, not numerical noise.

## Next gate

CR223b - PR qutrit tomography and purity-estimator lock.
