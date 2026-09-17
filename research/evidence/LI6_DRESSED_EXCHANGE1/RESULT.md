# Dressed eigenstate reference and retained terminal exchange

Date: 2026-09-16. Direction: Sean Brady. Mathematical design, implementation,
execution and independent checks: Codex, OpenAI AI research collaborator.
Authority: H001469; predecessor research H001464.

The exact dressed pair retains the entire33-dimensional complement and its
11-level/3-channel creation recurrence. Using both left and right Hamiltonian
action exposes full-rank terminal action on that complement. Adding the three
terminal words as channels still gives independent forward and reverse product
families. These findings now supply installed R4 source operations and fixtures.

For the dressed-source creation and explicit terminal construction:
**The test result suggests strong contact with the concept.**
For generic quadratic scalar exchange closure of the specified three-channel
LEFT/COMMUTATOR_REFERENCE lifts and the six-channel terminal extension:
**The test falsifies the concept.** General native factorized scattering remains open.

## Exact source and reference

Retain the original64-state source, full potential and attractive full-support
amplitudes at g=1 from H001462–H001464. Work over Q(sqrt(5)), without introducing
a floating-point reference or fitted source Hamiltonian:

```
z = sqrt(5)-2
Psi0 = |--> + z |++>
H64 = 64 H
Eref = 15408 - 64 sqrt(5)
H64 Psi0 = Eref Psi0
x = 64 E; omega = x-Eref
```

The unnormalized reference avoids unnecessary algebraic field extensions.
It is the lower eigenstate of the protected pair block, not the groundstate of
the entire64-state Hamiltonian. Excitation shifts retain their signs.
Use the original reversible seed words S0,S1,S2 from H001464. Their action on
Psi0 yields a new seed frame Q0'. Exact invariant closure returns dimension33.
The independent relation to the earlier recurrence is

```
Gamma = [[1,0,0],[z,1,0],[0,0,1+z]]
Qn' = Qn Gamma
Gn' = Gamma^T Gn Gamma
An' = Gamma^-1 An Gamma; Bn' = Gamma^-1 Bn Gamma
Fn' = Gamma^T Fn Gamma^-T
C'(x) = C(x) Gamma^-T.
```

Gamma is invertible at the retained z. Native computation recovers the recurrence
from the new seed; independent FLINT arithmetic checks the gauge relations and
every creation-residual coefficient. Creation still satisfies Q0'^T C'=I and
(H64-x)C'=-Q10' G10'^-1 F11'. It retains all33 source eigenstates.

## Full operator action and exchange

The LEFT lift acts by H64 L. The dressed commutator lift acts by
H64 L-L H64+Eref L, so Ln Psi0=Qn' and L11 Psi0=0. With the retained row-channel
recurrence and B(x)=sum Ln Gn'^-1 Fn'(x), telescoping gives

```
[H64,B(x)]-(x-Eref)B(x)
 = L11 G10'^-1 F10'(x) - L10 G10'^-1 F11'(x).
```

The first terminal term is part of the operator identity even though it
annihilates Psi0. Native exchange tests at (u,v)=(0,1) yield:

| Family, acting on Psi0 | Reverse rank | Combined forward/reverse rank | Reverse column upper bound |
|---|---:|---:|---:|
| Three channels, LEFT | 9 | 18 | 9 |
| Three channels, COMMUTATOR_REFERENCE | 9 | 18 | 9 |
| Three commutator channels plus three terminal words | 18 | 36 | 18 |

In the last row, every product with a terminal word on the right vanishes on
Psi0. Only18 reversed columns can survive, while a36-minor of the joined families
is nonzero. This excludes a generic scalar exchange matrix for this six-channel
extension already on the reference. Each displayed lower bound is certified at
primes65519 and1000039 with explicit Q(sqrt(5)) embeddings and nonzero minors.
The matrices and minors were independently reconstructed with FLINT. Regular
nonzero specialization certifies a nonzero polynomial minor, hence generic
nonclosure of the specified family. It does not classify other lifts or
on-shell restrictions. The native-family three-exchange test was conditional on
quadratic closure and therefore is not assigned here. Installed functionality is
separately exercised by a noncommuting constant-exchange fixture.

Stacking L11,a on the complete33-dimensional invariant complement gives rank33.
A33-column upper bound and nonzero33-minors at both primes give the exact rank
in characteristic zero: the common kernel is zero. Every nonzero complement
vector activates at least one commutator terminal word. This sharpens the earlier
LEFT-lift rank25/kernel8 result and establishes that the dressed terminal action
must remain available in subsequent algebraic work.

## Execution and installation

The repaired candidate executes9 source-bound ATOM3D calls with449,281 native
assertions. The independent checker passes199 checks. `EXECUTION.json` lists
these9 calls; `SESSION_STATUS.json` retains the shared older session's cumulative
receipts, including earlier work. `attempt1/` retains four successful arithmetic
results and the Python retention fault that interrupted its creation lookup.
A matrix-validation loop shadowed the immutable record key; the corrected pass
recomputed all9 calls with proper records. The failed domain receipt is preserved.
Two compilation failures and their diagnostics are retained in the package campaign;
the final native build has no warnings and uses undefined-behavior sanitization.

[Installed R4 package](../GEN3_R4_SOURCE_OPERATORS1/RESULT.md) supplies eight reusable
operations. All9 research calls replay exactly through the installed ATOM3D aliases.
The original full-source quartet also passes the installed pair-root operation.
The research checkpoint is explicitly carried into the fresh installed session;
source creation, exchange certificates and terminal action export in a new process
with no native worker or arithmetic. H001463/H001464 artifacts remain unchanged.

A useful next research step is to organize the full terminal-containing operator
module on the complement, using the installed exact action and product operations,
and determine a finite family stable under the required left/right actions before
seeking its exchange coefficients. The completed six-channel extension supplies
an explicit starting boundary. The general scattering law and sectors0/2 charge
charts remain open; neither is required for this completed capability installation.
