# CR222f PR Platform Adapter Contract Result

**Result class:** `CR222f_PASS_PR_PLATFORM_ADAPTER_CONTRACT__NV_PHOTONIC_NO_NEW_PHYSICS`

**Checks:** 16/16

**CR222f_platform_adapter_contract.csv SHA-256:** `79b809caa041f42a324203396e6531a5a3b2b48167038b59831bd40169179ba8`

## Verdict

CR222f maps the sealed PR protocol to platform observables without changing the
physics:

```text
sealed PR packet -> platform observables -> warning_allowed -> emitted/not_emitted
```

Adapter firing times:

```text
NV:       t_fire = T2*(-1/2*ln(23/24))
photonic: t_fire = tau_ent*(-1/2*ln(23/24))
```

The threshold remains:

```text
A_side = 1/24
```

and emission still requires:

```text
G_protocol=1
A_leak(t) >= A_side
qA>0
T=qA/8
W=7qA/8
```

No platform row changes the packet checksum, promotion gate, tensor witness, or
support roster.
