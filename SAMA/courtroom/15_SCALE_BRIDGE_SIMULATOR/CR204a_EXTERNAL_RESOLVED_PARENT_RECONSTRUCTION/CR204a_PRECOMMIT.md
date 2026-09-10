# CR204a Precommit

Question: Can the same resolved-SW reconstruction grammar map onto an actual
external reconstruction topology without relabeling CR204?

Frozen boundary input:

```text
CR204 remains BOUNDARY_RESOLVED_SW_PARENT_RECONSTRUCTION.
```

Best target:

```text
H -> ZZ* -> 4l
```

Appeal target:

```text
unobserved parent Higgs
two intermediate daughter branches
four visible final-state leptons
one reconstructed parent invariant
partial/off-shell branch behavior
clean wrong-control opportunities
```

Source rows:

```text
HZZ4l topology anchors from CR204a_topology_anchor_envelope.json
Higgs parent mass rows from CR092, topology-filtered
Z on-shell daughter row from CR091
CR204 scalar four-write via vector reconstruction row
```

This appeal tests whether the CR204 grammar can touch the external
`H -> ZZ* -> 4l` parent/daughter/final-state topology:

```text
external Higgs parent
external on-shell Z daughter
positive off-shell Z* remainder
four-visible-lepton final-state grammar
SAM visible parent closure from daughter-write lanes
hidden/source budget kept separate
```

This test could have falsified: the claim that visible resolved-SW parent
closure can be externally supported by the Higgs/ZZ*->4l reconstruction
topology while preserving CR204's hidden-budget separation and boundary status.
