# CR104b NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION

## Test Class

```text
APPEAL_FORWARD_RESEARCH_QUESTION_LOCK_FOR_UPSTREAM_DERIVATION
(does NOT modify CR104, CR104a, CR103a, or any prior CR)
```

## Preflight

```text
DS014 (DOWN_BOTTOM_LAYERED_GAP_SANDBOX, upstream SAM) uses a
9/8 = 1.125 layered_fraction multiplier to bring down quark (d) and
bottom quark (b) mass predictions to within ~3% of observed. DS014
already includes a DS014_reciprocal_control.py that tests whether
9/8 (and 8/9) is structural - improves d/b only - or curve-fitting
- improves u/s/c/t universally.

The user's question, sealed verbatim in conversation, asks the
deeper version: even if 9/8 survives the DS014 reciprocal control
as 'structural for d/b only', can 9/8 be DERIVED from the
R=12 / D=3 / half-write substrate geometry, rather than introduced
as a chosen layered fraction?

If yes, 9/8 becomes a theorem-grade native correction with no fit at
any layer. If no, 9/8 remains a fit even though it only fits the
right quarks, and the bounce cost in G435 carries a hidden free
parameter for d/b.

This CR LOCKS the question, the candidate derivations identified by
the Courtroom under conversation, and the upstream DS014 verification
chain. It does NOT claim to derive 9/8; it commits a research target
that any future upstream SAM theorem PASS must satisfy.
```

## The Question (Locked Verbatim)

User original (conversation, 2026-06-13):

```text
And the 9/8 might be the native resolved-bounce correction, not a fit,
if we can connect it to R=12 / D=3 / 1/2 write geometry.
This is the big question now: Can SAM derive the 9/8 bounce factor
from resolved half-write geometry?
```

Spell corrections: none required.

## Upstream Verification

```text
DS014 (DOWN_BOTTOM_LAYERED_GAP_SANDBOX)
  layered_fraction "9/8" with value 1.125
  used as multiplier on d and b quark base mass predictions
  produces ~3% relative error against PDG d/b masses
  DS014_reciprocal_control.py tests structural-vs-fit dichotomy

The "8" in 9/8 connects directly to G435 BOUNCE_COST_MASS_PROPORTIONALITY
PASS:
  r_bounce = (A0/2) * (q / 2^D) = (A0/2) * (q/8)
  slot_denominator = 8 = 2^D for D=3

The "9" has no current upstream derivation; it is the open question.
```

## Candidate Derivations Identified (Courtroom Note, Not Claim)

Four candidate forms for 9/8, all converging at D=3:

```text
Form 1   (2^D + 1) / 2^D                  binary cells + center / binary cells
Form 2   D^2 / 2^D                        dimension squared / binary cell
Form 3   (R - D) / 2^D                    radix minus dim / binary cell
Form 4   (corners + interior) / corners   D=3 cube topology
                                          (8 corners + 1 volume) / 8 corners

At D=3 all four = 9/8.

At D=2:  Form 1 = 5/4, Form 2 = 1, Form 3 n/a, Form 4 = 5/4
At D=4:  Form 1 = 17/16, Form 2 = 1, Form 3 n/a, Form 4 = 17/16

Form 2 (D^2 / 2^D) is the only candidate that gives a non-trivial
ratio specifically at D=3 and collapses to 1 at D=2 and D=4.
That would single out our 3D world as structurally privileged.

This is a Courtroom NOTE recording candidate derivations sketched in
conversation. It is NOT a derivation. The actual derivation must
happen upstream in SAM with theorem-grade PASS, then return as an
appeal row that promotes this CR's open-question lock to a
QUESTION_CLOSED_BY_UPSTREAM_THEOREM verdict.
```

## What Would Convert Candidate To Derivation

```text
1. Show QGA021 half-write route (1/2 SW | 1/2 W | 1/2 OUT | 1/2 IN |
   1/2 W | 1/2 SW) maps onto edges of the D=3 binary cell (cube),
   not just as an abstract 6-slot sequence.

2. Show the WRITE event lives at the interior volume of the cube
   (the resolved 3D ledger event).

3. Show the bounce energy normalizes by corners (octants = 2^D = 8).

4. The resulting (8 corners + 1 volume) / 8 corners = 9/8 emerges as
   the UNIQUE non-trivial bounce correction at D=3.

5. DS014 reciprocal control confirms 9/8 improves d/b only, not
   u/s/c/t universally (already in upstream as control test).

If 1-4 close in upstream SAM with a theorem-grade PASS like G435 or
G470, then 9/8 is theorem-grade native and DS014's d/b mass
predictions gain a derivation chain back to D=3 substrate topology.
No fit anywhere.
```

## Possible Outcomes (Forward-Blind)

```text
QUESTION_CLOSED_BY_UPSTREAM_THEOREM
    SAM upstream produces a theorem-grade PASS deriving 9/8 from
    D=3 half-write geometry; appeal row CR104b-1 records the
    closure; CR104b verdict promoted.

QUESTION_DISFAVORED_BY_RECIPROCAL_CONTROL_FAILURE
    DS014_reciprocal_control finds 9/8 improves u/s/c/t too;
    9/8 reduces to fit; appeal row CR104b-2 records the
    disfavoring; G435 bounce cost loses theorem-grade status for
    d/b corrections; substantial breadcrumb downstream.

QUESTION_REMAINS_OPEN
    no upstream derivation, no reciprocal control failure;
    the question stays sealed in the courtroom record for the
    next attempt.
```

## What CR104b Does NOT Do

```text
- does not claim to derive 9/8
- does not modify any prior CR verdict
- does not modify CR100 question lock, CR103a appeal lock, CR104
  verdict, or CR104a Layer 4 appeal lock
- does not commit SAM to any specific candidate derivation form
- does not promote DS014 layered_fraction beyond its current status
```

## Why Bold Locking Is Justified

```text
User authorization 2026-06-13:
  "Fortune favors the bold- keep it in the courtroom. Any failure
   can provide extremely valuable breadcrumbs downstream- success
   would be a provincial hole in one."

Failure mode (DS014 reciprocal control disfavors 9/8 as universal
fit, or upstream cannot derive 9/8 from D=3 geometry): G435 d/b
mass corrections lose theorem-grade status; this is informative
downstream because it identifies a specific structural debt.

Success mode (upstream SAM derives 9/8 from D=3 half-write geometry
with theorem-grade PASS, AND DS014 reciprocal control confirms 9/8
improves d/b only): the bounce cost chain becomes derivation-only
all the way down to D=3 substrate topology. Hole in one.

Either outcome is on the public sealed record.
```

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have been generated unverifiably if no upstream SAM
work used 9/8 anywhere. DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX
demonstrates upstream use of the exact 9/8 = 1.125 layered_fraction
on d/b masses, with an explicit DS014_reciprocal_control test of
fit-vs-structural. The question is real and the derivation target
is concrete.

This CR locks the question and the candidate derivation forms into
the cryptographic record so any future SAM theorem PASS that closes
it can be matched against the sealed formulation. The question
cannot be quietly rewritten to fit the closure later.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
