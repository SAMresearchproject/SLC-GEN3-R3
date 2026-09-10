# CR120U Correction Ledger

Recorded after the successful result run and before final handoff.

## Terminology correction

The precommit's binding-handoff block labeled the value `4` as the **cell
coordination number**. The executed incidence result establishes:

```text
vertex degree within an octahedral cell = 4
faces / possible face-sharing slots per isolated cell = 8
```

Those are different objects. The generated `CR120U_BINDING_HANDOFF.md` has
been corrected to use `vertex degree = 4` and to state the eight face-sharing
slots separately.

No numerical incidence result changes:

```text
V = 6
E = 12
F = 8
8C = exposed_faces + 2I
```

The sealed precommit is preserved unchanged. This ledger controls the wording
for downstream binding work.
