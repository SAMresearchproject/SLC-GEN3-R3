# CR223b PRECOMMIT - PR Qutrit Tomography & Purity-Estimator Lock

## Scope

Lock the qutrit tomography measurement basis (eight Gell-Mann observables
plus normalization) and the purity estimator

```text
A_hat_leak = 1 - Tr(rho_hat^2)
```

with PSD-projected linear inversion. Validate on a sealed roster of seven
synthetic states using disjoint validation/test shot splits.

## Locked invariants

```text
A_side                    = 1/24
bias tolerance near A_side = 1/96
coverage target           = 0.90
balanced-accuracy target  = 0.90
shots per measurement set = 5000
validation trials/state   = 200
test trials/state         = 200
validation RNG seed       = 20260621
test RNG seed             = 30260621
basis_csv_sha256          = 64621c1c7c091fe4ed941d1aa3925e413ca39f26d86e9d5c09645a5d25fbf826
state_roster_sha256       = e9b2b2a3960d72db453ee726b3213b143a9105203bf48882083d8c9fa18dea27
```

## Estimator pipeline (sealed)

```text
1. for a in 1..8: sample b_hat_a via N-shot multinomial in eigenbasis of lambda_a
2. rho_LI = (1/3) I + (1/2) sum_a b_hat_a lambda_a
3. eigendecompose rho_LI; clip negative eigenvalues to 0; renormalize trace
4. A_hat_leak = 1 - Tr(rho_PSD^2)
```

No fitted parameter, no threshold-aware reconstruction, no state-label
branching. WC1..WC6 are documented and verified in CR223b_wrong_controls.csv.
