# CR120Z Precommit — X1 Entanglement-Response Quantum Sandbox

## Aim

Test whether the archived order `B contact -> X1 response -> closure` admits a clean quantum realization in which the distinct response operation generates or heralds nonseparability. This is an existence and discrimination experiment, not a claim that the chosen gates are already the physical SAM operators.

## Frozen realization

The input is `|00>`. The sandbox analog of B is a local Hadamard operation on subsystem A. It creates a request-side coherent alternative but cannot entangle two systems by itself. The sandbox analog of X1 is a distinct controlled response, `CNOT A->B`. The primary sequence is therefore:

```text
|00> -- B:H_A -- X1:CNOT_A->B -- candidate joint state
```

The order is frozen before execution. `X1=1` is never used as an amplitude, probability, qubit value, phase, or matrix. The six archival half-slot weights are not mapped to quantum amplitudes.

## Frozen discriminators

- Partial-transpose negativity.
- Two-qubit concurrence.
- Fidelity with `|Phi+>`.
- CHSH using `A0=Z`, `A1=X`, `B0=(Z+X)/sqrt(2)`, `B1=(Z-X)/sqrt(2)`.
- Reduced-state invariance under a predeclared remote-unitary angle sweep.
- Remote A-D state after Bell versus product central measurements on B-C.

## Controls

1. B only.
2. X1 only.
3. Reverse order X1 then B.
4. Classical correlated return `1/2 |00><00| + 1/2 |11><11|`.
5. Product central measurement during swapping.
6. False/unresolved herald obtained by averaging every Bell outcome without correction.
7. Depolarizing visibility scan with no fitted parameters.

## Pass rule

The ordered candidate must be a physical Bell state with negativity `1/2`, concurrence `1`, fidelity `1`, and CHSH `2 sqrt(2)`. All four direct controls must be separable and Bell-local under the frozen settings. The Bell-response swapping arm must herald an entangled A-D state while the product and false-herald controls remain separable. Local marginals must remain invariant across remote setting operations. Noise thresholds must agree with the analytic `v>1/3` negativity and `v>1/sqrt(2)` CHSH boundaries to the fixed 0.005 grid.

## Meaning of a pass

A pass would establish that the **typed B-then-X1 relay grammar is quantum-capable**: there exists a minimal standard quantum-channel realization in which B prepares the request and a distinct X1 response creates or heralds entanglement, and the ordering matters. It would not identify the sandbox gates with the physical B or X1 entities, and it would not install a SAM operator.

## Custody

Sources, contract, precommit, and runner are hash-sealed before execution. The simulation is deterministic, uses every predeclared control, performs no fitting, and permits no same-run repair.
