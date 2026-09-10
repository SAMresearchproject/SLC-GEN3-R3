# 17_HAUNTED_HOUSE_INTAKE

## Branch Purpose

This branch receives Haunted House explorations that are mature enough for
Courtroom handling. Some entries may become scoped theorem-grade if they replay
against already locked SAM primitives without mutation.

Haunted House is upstream-of-Courtroom exploration. A Haunted House artifact can
be real, useful, and worth preserving without being promoted to a closed SAM
claim. This branch exists to make that distinction explicit:

```text
Haunted House artifact -> source/provenance intake -> claim triage -> CR test
```

## Current Test

```text
CR210_HH001_FANO_PLATES_126_INTAKE
```

HH001 brings in:

```text
C:\VS\Haunted_House
C:\VS\HH001_fano_plates_126.pdf
```

The intake target is narrow:

```text
verify HH001 source artifacts
hash the PDF and Haunted House inputs
check the Fano F_2^3 address algebra
check the 126-row SIS table and qA / qA/8 bridge to CR119
preserve falsified and open HH001 sub-readings without overpromotion
```

## Branch Boundary

This branch does not make Haunted House theorem-grade by default. It decides
which parts are safe to carry into Courtroom tests. HH001 is scoped theorem
grade only for the SAM address partition:

```text
R = 12
D = 3
R^2 = 144
2^D = 8
R^2 / 2^D = 18
000 carrier address = 18
seven nonzero F_2^3 Fano addresses = 7 * 18 = 126
```

The HH001 table and PDF verify that address partition as a 126-row surface tied
back to CR119 qA and qA/8.

Forbidden overclaims:

```text
the PDF alone is a theorem
the seven-channel physical mapping is closed
per-element XOR closure survived
ACTION residual equals nuclear spin
126 GeV conversion is derived
Haunted House entries count as Courtroom-grade evidence
```
