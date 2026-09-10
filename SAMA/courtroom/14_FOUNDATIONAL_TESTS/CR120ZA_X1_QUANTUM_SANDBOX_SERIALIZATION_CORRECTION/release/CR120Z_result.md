# CR120Z — X1 Entanglement-Response Quantum Sandbox

## Primary verdict

`PASS_X1_RESPONSE_INTERFACE_QUANTUM_CAPABLE_SANDBOX__ORDERED_B_THEN_X1_GENERATES_AND_HERALDS_NONSEPARABILITY__PHYSICAL_WELD_OPEN`

## The fun result

The archived relay grammar has a clean quantum realization. In the frozen minimal model, B first creates a local coherent request and X1 then supplies a distinct controlled response:

```text
|00> -- B:H_A -- X1:CNOT_A->B --> |Phi+>
```

That ordered route produces a maximally entangled state:

- negativity: `0.5`
- concurrence: `1`
- fidelity with `|Phi+>`: `1`
- frozen-setting CHSH: `2.82842712475` = `2 sqrt(2)`

The ordering is load-bearing. B alone, X1 alone, X1-before-B, and the classical correlated-return state all have zero negativity. Ordinary reciprocal correlation therefore does not pass as entanglement.

## Relay extension

The same response interpretation works as a central entanglement-swapping interface. An X1-indexed Bell response on the two middle systems heralds a remote pair with negativity `0.5` and CHSH `2.82842712475`. A product central measurement and an unresolved false herald both leave the remote pair separable.

Local marginals remain invariant across every frozen remote-setting rotation; the maximum trace distance is `1.11e-16`. The quantum relay changes joint correlations without becoming a controllable signal.

## Robustness

Under depolarizing noise, the first grid point with nonzero negativity is `v=0.335`, immediately above the analytic boundary `1/3`. The first frozen-setting CHSH violation is `v=0.71`, immediately above `1/sqrt(2)`. No parameters were fitted.

## Supported interpretation

This establishes **quantum capability of the typed grammar**: a distinct B-contact followed by an X1-response can generate or herald nonseparability, and the order matters. It gives the X1 response-interface hypothesis a concrete mathematical target for later empirical or hardware work.

## Boundary

The chosen `H` and `CNOT` maps are a prospective minimal realization, not discovered physical definitions of B or X1. X1 is not equated with entanglement, its scalar value is not used as an amplitude, W9 is not used as a Bell witness, and no SAM operator was installed.

## Custody

- Sources: `10/10` hashes matched.
- Seal: `PASS`.
- Hard gates: `9/9`.
- Wrong controls: `12/12`.
- Same-run repair: `false`.
- Registry mutation: `false`.
