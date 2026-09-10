# CR005b -- QNM Damping Substrate Dynamics -- RESULT

```text
verdict          : PASS
execution_status : CLEAN
precommit_hash   : bac6d988df1546127f9cca0ba9831928600d09af3ed83aae14a5e3c5c612484b
runner_hash      : 15d0f18283bb238466455e7d405b2b0948facfb258dc25a5254b71efb427fbb8
free_parameters  : 0
sam_language_v0_3_consulted_during_development : false
sam_language_v0_3_candidate_hash_known_to_research_agent : false
```

## Core result

The precommitted damping-shell selector evaluates to:

```text
damping_shell = L - V = 162 - 27 = 135
              = R^2 - d_hat^2 = 144 - 9 = 135
omega_I*M     = R/(L - V)
              = 12/135
              = 4/45
              = 0.08888888888888889
```

External comparator (Berti/Cardoso/Starinets 2009 via CR003): 0.08896232
Relative gap: 0.082541812209 percent.

## Wrong controls

| control | expression | value | error pct | status |
|---|---|---:|---:|---|
| WC1_capacity_denominator | `R/R^2` | 0.0833333333333 | 6.327383 | role_rejected |
| WC2_closed_ledger_denominator | `R/L` | 0.0740740740741 | 16.735452 | role_rejected |
| WC3_matter_denominator | `R/M` | 0.0952380952381 | 7.054419 | role_rejected |
| WC4_dimension_numerator | `d_hat/(L - V)` | 0.0222222222222 | 75.020635 | role_rejected |
| WC5_theta_numerator | `Theta/(L - V)` | 0.133333333333 | 49.876187 | role_rejected |
| WC6_pi_neighbor | `(pi + S)/M` | 0.0884253385206 | 0.603606 | role_rejected_pi_not_sourced_in_damping_shell_rule |

## Verdict statement

CR005b PASS. The Schwarzschild fundamental QNM damping coefficient `omega_I*M = 4/45` is derived from the route-radix leak over the unresolved damping shell `L - V`, with exact source identities, zero free parameters, and wrong controls rejected under the precommitted gates.
