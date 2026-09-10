# CR213 D3 to Particle Breadcrumb Audit - Precommit

## Question

Does the imported D=3-to-particle breadcrumb markdown identify live,
Courtroom-backed dependencies between D=3 and the particle stack, and what
remains open?

## Source Intake

The source is an external markdown artifact supplied by the curator. CR213
imports its content as a sanitized Courtroom input, records the source hash, and
does not place the source directory name into emitted artifacts.

## Pass Conditions

```text
P1  Imported markdown resolves, hashes, and is copied into the CR213 folder.
P2  Imported markdown contains the D=3 particle-stack breadcrumb question.
P3  CR115 confirms D=3 as the unique stable carrier dimension and rejects
    reverse derivation from particle matches.
P4  CR119 confirms the table boundary: 321 particle rows, 126 matter rows,
    126 periodic rows, and no 126-particle-row promotion.
P5  LC02 and LC04 confirm D=3 is present in the locked Last Campaign primitive
    stack and particle replay.
P6  QP093A, role-operator algebra, and the lepton-row breadcrumb are classified
    without overclaim.
P7  The generation-count derivation remains OPEN unless a derivation is found.
```

## Wrong Controls

```text
WC1  Treat 126 matter/periodic capacity as 126 particle rows.
WC2  Derive D=3 from particle masses, Higgs, R, A0, or downstream matches.
WC3  Treat a source-code comment as a generation-count theorem.
WC4  Treat upstream source-code dependency as a completed D-perturbation result.
WC5  Treat LC04 in-sample generator consistency as first-principles derivation.
WC6  Emit source directory labels into new CR213 files.
```

## Expected Verdict Shape

CR213 may pass as a scoped breadcrumb-audit intake if it separates:

```text
BACKED       D=3 is live in CR115, CR119, LC02, LC04, and QP093A intake.
SUGGESTIVE   Role-operator and lepton-row breadcrumbs exist upstream.
OPEN         Direct derivation of SM generation count from D=3 is not yet sealed.
NEXT         D-perturbation replay is a separate executable CR.
```
