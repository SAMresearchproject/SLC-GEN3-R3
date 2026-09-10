# CR222f PRECOMMIT - PR Platform Adapter Contract

## Scope

Map the sealed PR protocol to platform observables without new physics:

```text
sealed PR packet -> platform observables -> warning_allowed / emitted
```

## Platform Inputs

```text
platform_id
coherence observable: T2 or tau_ent
leak observable: A_leak(t)
threshold: A_side = 1/24
packet checksum: 162
protocol gate: G_protocol
```

## Firing Time

```text
NV:       t_fire = T2*(-1/2*ln(23/24))
photonic: t_fire = tau_ent*(-1/2*ln(23/24))
```

## Pre-run Hash

Expected `CR222f_platform_adapter_contract.csv` hash:

```text
79b809caa041f42a324203396e6531a5a3b2b48167038b59831bd40169179ba8
```
