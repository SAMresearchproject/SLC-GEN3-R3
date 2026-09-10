# CR222e Paul Revere Warning Emission Gate Result

**Result class:** `CR222e_PASS_PR_WARNING_EMISSION_GATE__SEALED_PACKET_PROMOTION_TRIGGER_TENSOR_WRITE`

**Checks:** 15/15

**CR222e_emission_state_machine.csv SHA-256:** `a79ee4b0d5519c85eb6edded7f96e698b51a274b56e1e64f2b160c5ef211f2d7`

## Verdict

CR222e defines the emission gate:

```text
VALID_PR_WARNING = SEALED_PACKET + G_protocol=1 + A_leak>=A_side
A_side = 1/24
```

Emission is separate:

```text
qA > 0
T = qA/8
W = 7qA/8
```

The corrected support stack is preserved:

```text
12 unique support rows = 81
QP093A-0303 mirror     = 81
closure                = 162
```

Support inventory alone does not emit. A sealed packet with no protocol gate
remains `SEALED_PACKET`; it does not become a warning write.
