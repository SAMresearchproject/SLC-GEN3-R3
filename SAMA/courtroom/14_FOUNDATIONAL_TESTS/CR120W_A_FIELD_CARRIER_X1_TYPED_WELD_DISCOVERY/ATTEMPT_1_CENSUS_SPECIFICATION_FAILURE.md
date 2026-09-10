# CR120W attempt 1 census-specification failure

Status: `ABORTED_SOURCE_GATE__NO_PROMOTED_SCIENTIFIC_VERDICT`

The first execution reconstructed 26 partition-one rows while the frozen
contract incorrectly expected 25. The exact composition is:

```text
15 one-body matter/conjugate occurrences
 3 legal nonlocal infrastructure occurrences
 8 rejected-control occurrences
--
26 total partition-one occurrences
```

The only failing control was:

```text
WC02_EQUAL_TREATMENT observed=26 required=25
```

All 25 frozen source hashes matched and the runner returned
`FAIL_CR120W_SOURCE_OR_CANDIDATE_RECONSTRUCTION`. No registry mutation occurred.

Attempt-1 seals:

```text
contract  85262f761cc6ca27a8f8a7bf60c51324011579d4a9622401cad37295112bd41e
precommit 1edd2abb8e99abf625eb894e046d732e14378063fc7d9dd25c15a429a770ef6a
manifest  377bb77c46d83a15f82a933d0c56b4c33ecaf56fca50ce85bc4423813408b182
runner    a5bf5f1101d9d72c678875525b4283e0ca9475b11883350b238d0034a9759ab9
release   4eb893e1513319fd26079c0173ea25632bce45133a27c738b3305b2370a603c3
```

The opened candidate outcome is not used to alter any scientific gate.

