# Native spectral creation and the terminal terms in the exchange algebra

Date: 2026-09-16, America/Chicago. Direction: Sean Brady. Mathematical design,
implementation and execution: Codex, OpenAI AI research collaborator.

## Result

The retained eleven-level recurrence now supplies exact spectral creation
formulas for all33 states of the symmetric complement. The next exchange test
has also executed: for each of two specified source-word lifts, the nine
products in one spectral order and the nine in the reverse order are eighteen
independent vectors, already when acting on the native reference. Thus these
lifts do not have a generic9-by9 scalar channel exchange matrix.

For the full-source spectral creation formula and explicit terminal action:
**The test result suggests strong contact with the concept.**

For generic nine-product quadratic exchange closure of the two tested lifts:
**The test falsifies the concept.**

The result identifies the next algebraic ingredient. The terminal operator
words vanish on the reference, but their joint action has exact rank25 on the
33-state complement. Their common kernel has dimension8, and no nonzero vector
in that kernel remains there after one Hamiltonian action. In particular,
every complement eigenstate activates at least one terminal word of the first
lift. A reference-state recurrence cannot discard those terms when reused
as an operator relation on further excitations.

Four new source-bound ATOM3D calls retain481,189 native assertions. Independent
FLINT/NumPy reconstruction passes262 checks. All four C++ builds finish without
warnings under the retained undefined-behavior sanitizer. No domain call fails.
The original64-state source, potential, full-support attractive amplitude
assignment and g=1 remain fixed. This is one amplitude fixture; a general
Bethe exchange/scattering construction remains open.

## Exact spectral creation from the source recurrence

Use H64=64H and the H001463 matrices Q_n,G_n,A_n,B_n,F_n, n=0,...,10.
The spectral parameter in this calculation is **x=64E**, distinct from the
earlier dimensionless two-root coordinate. Define

    C(x)=sum_(n=0)^10 Q_n G_n^-1 F_n(x).

Exact rational arithmetic checks every coefficient in

    (H64-xI) C(x) = -Q_10 G_10^-1 F_11(x),
    Q_0^T C(x) = I_3.

Consequently F_11(x)a=0 gives the original-source eigenstate C(x)a.
The normalization identity makes this map injective on the terminal kernel.
Conversely, the retained full-rank recurrence reconstructs any complement
eigenstate from a=Q_0^T psi, so it loses no eigenstates. The independently
checked characteristic polynomial is squarefree of degree33; its rational
irreducible factors have degrees15 and18, matching the retained sector sizes.
No new numerical root approximation is used in this campaign.

`NATIVE_RESULT.json` retains all eleven64-by3 coefficient matrices of C(x)
and its terminal source factor. `VALIDATION.json` checks the identities with
independent FLINT rational arithmetic and records the polynomial factors.

## A declared native operator lift

The existing native local operators are R=local_creation_times2/2 and
T=2F2=2(E2+E2^T), with R|->=|+> and T|->=|r>, |r>=layer mask28.
On the two original layers, use the row of three source words

    S_0=4(T_L+T_R),
    S_1=4(R_L T_R+T_L R_R),
    S_2=4T_L T_R.

Their action on Omega=|--> is exactly Q_0, with the retained integer frame
normalization. Lift the recurrence to full64-by64 operators:

    L_(-1)=0, L_0=S,
    L_(n+1)=H64 L_n-L_n A_n-L_(n-1)B_n,
    B_b(x)=sum_(n,a) L_(n,a) [G_n^-1 F_n(x)]_(a,b).

Then L_n Omega=Q_n and B_b(x)Omega=C_b(x). This extension is a specified
candidate, fixed before its exchange test. A state preparation alone does
not uniquely specify an operator on other input states. No right reference
projector is inserted to make subsequent products vanish.

The proposed quadratic relation allows an arbitrary scalar coefficient for
each of the nine reversed channel products:

    B_a(u)B_b(v) = sum_(c,d) S_ab^cd(u,v) B_c(v)B_d(u).

At (u,v)=(0,1) and (73,15400), each order has rank9 and their combined rank
is18. This holds both as full source operators and on Omega. Native modular
elimination supplies explicit nonzero minors at primes1000003 and1000033;
independent reconstruction reproduces every certificate. All rational
denominators are invertible at these primes. Since eighteen is also the column
upper bound, this establishes rank18 over Q at the displayed points. The
minors are polynomials in u,v with fixed rational source denominators; one
nonzero value establishes generic nonclosure, including for a meromorphic
scalar exchange matrix defined on an open spectral set.

This result concerns the displayed off-shell operator families. It does not
classify other lifts, reference states, amplitude assignments, or relations
restricted to selected on-shell root pairs. A three-excitation consistency
test was not assigned after this two-creation relation failed to close.

## The operator term that the reference annihilates

The same recurrence yields the full operator identity

    (H64-x) B(x)
      = L_11 G_10^-1 F_10(x) - L_10 G_10^-1 F_11(x).

This follows by telescoping the operator recurrence and the Gram-adjoint
identities. Every matrix coefficient is additionally reconstructed modulo
both primes. Acting on Omega removes the first term because L_11 Omega=0
and gives the exact state identity above.

`EXACT_RESULT.json` supplies a small-rational source frame W for the
33-state complement, H64 W=W K, and the complete exact stacked matrix

    T_terminal = stack_a (L_(11,a) W).

Its rank over Q is25. A full kernel basis N has eight columns and satisfies
T_terminal N=0. The exact matrix T_terminal K N has rank8. If a nonzero
eigenvector lay in this kernel, this last matrix would annihilate its
coefficient vector; the full column rank excludes that possibility.

Seven of these eight kernel directions already lie in the common kernel of
the three seed words; their exact stacked seed rank is26. The additional
terminal-kernel direction and all eight source vectors are retained. These
kernel statements concern the reversible-cycle lift above.

This is the concrete distinction the next construction must retain:
**Q_11=0 is a statement about preparation from Omega; L_11 is a nonzero
source operator with a measured action on excited inputs.**

## Directed-cycle correction

The immediate source-native correction replaces T=2F2 by T=2E2, a nilpotent
directed move. E2^T annihilates |->, so the exact initial frame and all33
spectral creation states stay the same. R, H64 and the recurrence are retained.
This changes the operator action after preparation and is a second specified
lift, not a change of source Hamiltonian.

At (u,v)=(0,1), the nine reverse products and eighteen combined products on
Omega again have ranks9 and18 at both primes. Their nonzero minors establish
the same generic nine-product nonclosure for this directed lift.
`DIRECTED_RESULT.json` and its independent validation preserve the result.

## Next question and R4 custody

The recommended next construction uses the known **dressed pair eigenstate**
as the reference and retains terminal operator action explicitly when
deriving the exchange algebra. The current Omega is a preparation reference;
at the retained delta=-1 it is not a Hamiltonian eigenstate. The earlier
pair supplies an exact eigenstate and source preparation, so this change has
a native input already available. Whether it enables a compact closed
exchange law is the next test, not a result of this campaign.

`NEXT_QUESTION.json` records that bounded successor. The earlier pair, roots,
recurrence and open affine-charge charts retain their established results.
The multientropy paper remains a later entanglement investigation; this
campaign did not open that branch.

`R4_INSTALLATION_NOTE.md` and `R4_INSTALLATION_CANDIDATE.json` extend the
earlier integration packet. Status: **CANDIDATE_NOT_INSTALLED**. Installed
SLC-GEN3-R4, CE and generation are unchanged. `COMPLETE_SESSION_STATUS.json`
contains the four new calculation receipts alongside the two earlier calls
in the same current-generation session.
