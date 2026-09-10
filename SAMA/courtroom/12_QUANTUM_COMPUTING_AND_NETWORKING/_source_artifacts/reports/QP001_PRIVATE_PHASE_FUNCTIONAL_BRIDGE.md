# QP001 - Private Phase Functional Bridge

Location: `D:\quantum_phase`

## Verdict

`QP001_PRIVATE_PHASE_FUNCTIONAL_BRIDGE_BUILT`

QP001 turns the private phase-field threshold ladder into an accumulated-A route law.

```text
A_route[N+1] = A_route[N] + epsilon_route
epsilon_route = A_exposure_per_t_SW
state = state_class(A_route)
write_accessibility = clamp((A_route - A_SIDE) / (A_SHARE - A_SIDE), 0, 1)
qg_competition = clamp((A_route - A_ALPHA_H_SQ) / (A_ALPHA_H_D - A_ALPHA_H_SQ), 0, 1)
phase_coherence = 1 - max(write_accessibility, qg_competition)
```

## Main Read

The private ladder now behaves as a route functional. Below `A_SIDE = 1/24`,
there is no ledger-write access. Between `A_SIDE` and `A_SHARE = 1/12`,
write candidacy turns on. At and above `A_SHARE`, A-resolution can write.
The per-route QG competition band begins at `A_ALPHA_H_SQ = 1/3` and
reaches the WRITE midpoint at `A_ALPHA_H_D = 1/2`.

## Phase Safety Leaders

| Rank | Qubit | Route | ticks to A_SHARE | state at one t_SW |
| ---: | --- | --- | ---: | --- |
| 1 | QUBIT-NL-001 | single_block__neutral_identity_outer_binary_active | 2019874.91168 | PRE_WRITE_PHASE |
| 2 | QUBIT-UNK-001 | layered_admissible__binary_split__8_4 | 53578.8461036 | PRE_WRITE_PHASE |
| 3 | QUBIT-CL-001 | single_block__alpha_H^2*D__integer_winding | 18778.865045 | PRE_WRITE_PHASE |
| 4 | QUBIT-BN-001 | outer_binary__scalar_even_return_seed | 1421.22303376 | PRE_WRITE_PHASE |

## Outputs

```text
qp001_threshold_transition_law.csv
qp001_qubit_phase_functional_table.csv
qp001_route_evolution_samples.csv
qp001_phase_functional_summary.json
qp001_next_frontier.csv
```

## Next Frontier

`QP002_PRIVATE_GAMMA_RES_PHASE_WRITE_SELECTOR`

QP002 should use this functional to build the write selector:
`Gamma_res^phase(A_route, X_contact, X_environment)`. That is the point
where unresolved route evolution becomes a private, testable resolution
law instead of only a threshold ladder.

Generated at UTC: `2026-06-07T02:24:39.769282+00:00`
