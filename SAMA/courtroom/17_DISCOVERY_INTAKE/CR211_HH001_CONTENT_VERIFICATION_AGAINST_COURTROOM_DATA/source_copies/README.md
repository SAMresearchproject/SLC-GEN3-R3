# Haunted House

A private SAM exploration repository for ideas that have not been explored before.

```text
Originator, author, and conceptual driver: Sean Brady
Co-author and technical collaborator: AI collaborator (see AUTHORS.md)
```

## What This Repo Is

Haunted House is the upstream-of-Courtroom space for SAM. It exists to follow
structural patterns wherever they lead, before any Courtroom rules apply. The
working assumption is that we are exploring rooms nobody has been in:

```text
no prior physics has come to these conclusions
no external dataset can be used as a fit target
no community of explorers has triangulated these rooms yet
the only navigation is structural consistency
```

This is a deliberate stance, not a license for sloppiness. The discipline
remains: zero free parameters, integer matches treated as structural readings
(not coincidences), and explicit status flags on every claim. What is dropped
is pre-commitment to a test outcome. Ideas are allowed to be wrong here. They
are NOT allowed to be wrong in the Courtroom.

## What This Repo Is Not

```text
not              The Courtroom (testing / sealed-envelope / wrong-controls)
not              Stam_model-A-v1.0 (parent SAM derivation stack)
not              quantum_phase    (private SAM quantum-phase branch)
not              a publication venue
not              a place to file claims at theorem-grade
not              a place to fit anything to external data
```

If an exploration here matures, it gets handed off to the Courtroom as a CR-class
test, or to a parent repo as a derivation entry. Haunted House does not seal,
hash-freeze, or close anything on its own.

## Relationship To Other Repos

```text
Stam_model-A-v1.0   <--  derivation stack (sealed)
quantum_phase       <--  QP/QC/QN exploration branch (private)
The_Courtroom       <--  CR-class tests, sealed verdicts, hash freezes
Haunted_House       <--  upstream-of-Courtroom exploration (this repo)
```

Flow:

```text
Haunted_House idea -> reading proposal -> Courtroom CR test -> sealed verdict
                                                            -> parent-repo derivation
```

A Haunted House entry can also be archived without promotion. That is allowed
and intended.

## Repo Layout

```text
README.md               this document
HOUSE_RULES.md          the exploration posture (read this second)
LICENSE.md              proprietary, all rights reserved
NOTICE.md
AUTHORS.md
STEWARDSHIP.md

explorations/           individual exploration notes
readings/               structural reading proposals (cross-channel patterns)
questions/              open questions / things noticed but not yet explored
archive/                explored and set aside, or graduated to other repos
```

Each subdirectory has an `INDEX.md` listing entries with status flags.

## Status Vocabulary

Every entry carries one of these flags:

```text
SHADOW             noticed but not investigated yet
EXPLORING          actively being followed
READING            structural reading proposed (not promoted)
HANDED_OFF         moved to Courtroom or parent repo for testing
ARCHIVED           explored and set aside without promotion
RETIRED            withdrawn (the reading did not hold)
```

A SHADOW becoming a HANDED_OFF is the success path. A SHADOW becoming a
RETIRED is also a success path. The failure mode is a SHADOW that lingers
without status or graduates without testing.

## How To Read An Entry

Each entry should declare:

```text
status            (one of the flags above)
what_is_noticed   (the structural pattern, integer match, or anomaly)
why_it_matters    (which SAM closure or open question it touches)
what_would_break  (what observation or wrong-control would falsify it)
next_move         (explore further / propose CR / archive / retire)
```

If an entry cannot fill out "what_would_break", it stays in `questions/` or
`shadows`, not in `readings/`. Unfalsifiable patterns are not promoted.

## Provenance

This repository is private research material.

```text
Copyright (c) 2026 Sean Brady. All rights reserved.
```

See [LICENSE.md](LICENSE.md), [HOUSE_RULES.md](HOUSE_RULES.md),
[AUTHORS.md](AUTHORS.md), and [NOTICE.md](NOTICE.md).
