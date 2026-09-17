# Li6 full-graph symmetry and spectral family

Date: 2026-09-15. Direction: Sean Brady. Mathematical construction, source
mapping, native implementation and execution: Codex, OpenAI AI research collaborator.

## Result

The entire64-state fixed-current Li6 source graph now has an exact spectral
construction with its original potential unchanged and all302 reversible
exchange pairs retained. Two commuting involutions reduce its candidate
Hamiltonian into blocks of dimensions20,16,16,12. Native arbitrary-precision
arithmetic derives each block's characteristic polynomial with symbolic
coupling g and verifies the exact complete change of basis.

For this full-source symmetry reduction and commuting polynomial family:
**The test result suggests strong contact with the concept.**

This is a symmetry-generated spectral construction. A full-graph Gaudin charge
construction and Bethe-string assignment remain open. The original selected
Gaudin sectors and their operator records retain their source scope.

## Preserved Hamiltonian

Let V be the diagonal matrix of the original64 COVER_03 source potentials,
assignment0/rho1, on the retained fixed-current fiber. Let A be the symmetric
adjacency matrix containing every one of the302 original exchange pairs.

    H(g) = V + g A.

The single equal real coherent amplitude g is a new Codex candidate assignment
on these source edges. It is not a derived native event amplitude or an energy
conversion. A has zero diagonal, so every diagonal entry of H remains the
original source potential for every g. All64 source states and all302 pairs
remain present. The exact trace relation is

    tr H(g)^2 = 6603857824/4096 + 604 g^2.

V does not commute with A. The full graph is connected; its smaller symmetry
blocks are superpositions of source states, rather than disconnected subsets.

## Exact source symmetries

The first native pass checks all source-code XOR translations, with and
without global phase conjugation. Only the identity and conjugation preserve
the fixed fiber in this search. Both preserve the potential and adjacency.

For the source encoding q_e=b_e+2*c_e, complex conjugation takes q_e to -q_e
mod4. On the original integer state code it is exactly

    C(s) = s XOR ((s AND 511) << 9).

It fixes eight states and pairs the remaining56. The native graph search then
enumerates all adjacency automorphisms preserving the actual potential values.
Colour refinement gives20 classes; the exhaustive backtracking traversal
finishes after241 nodes, without reaching either cap. It finds four permutations:

    I, C, S, CS;  C^2=S^2=I,  CS=SC.

S is defined by the complete source-index permutation retained in FAMILY.json
and spectral_RESULT.json. Its native phase-coordinate interpretation is not
assigned. The four permutation traces are64,8,8,0. The symmetry search preserves
the equal-amplitude adjacency; individual cycle/increment labels are retained
as source history, but are not additional colours in this search. Arbitrary
unequal edge amplitudes need not preserve these operator symmetries.

For signs a,b in {+1,-1}, the exact projectors are

    Pi_ab = (I+a*C)(I+b*S)/4,
    rank Pi_ab = (64+8a+8b)/4.

Their ranks are20,16,16,12; they are orthogonal and sum to the full identity.
Both V and A commute with each projector. The source basis is therefore
retained completely under the direct-sum transformation.

## Compatible spectral family

For an independent formal spectral parameter u, define

    T(u;g) = H(g) + u*C + u^2*S.

All coefficient matrices commute, so [T(u;g),T(w;g)]=0 for every u,w,g.
The original candidate Hamiltonian occurs at u=0. On the (a,b) block,

    T_ab(u;g) = H_ab(g) + (a*u+b*u^2) I.

Consequently the four characteristic polynomials computed for H also give
the complete spectrum of T by these explicit scalar shifts. The ordinary
resolvent (zI-H(g))^-1 supplies an additional rational commuting family wherever
the inverse exists. These constructions do not invoke a Yang-Baxter relation
or introduce a Bethe-string identification.

The four projectors are independent because all four character spaces have
positive dimension. Their symmetry information distinguishes the sectors;
it does not determine every eigenvalue inside each sector.

## Exact full spectral equation

For each symmetry orbit, the native constructor creates signed basis columns
with entries0,+1,-1. Columns have squared norm1,2 or4. Let U_ab contain the
columns for a character, and W_ab=U_ab^T U_ab. The native calculation verifies

    A U_ab = U_ab B_ab,
    V U_ab = U_ab D_ab,
    W_ab B_ab = B_ab^T W_ab.

The exact reduced matrices are H_ab=D_ab+g*B_ab. They are self-adjoint in the
positive metric W_ab; W_ab^(1/2) H_ab W_ab^(-1/2) is real symmetric. All signed
columns together form an orthogonal complete64-dimensional basis. A reduced
block may have exchange on its diagonal after changing basis; the original
source-basis diagonal remains V exactly.

Set K_ab=64 H_ab. Its entries are integer polynomials in g. The native GMP
calculation returns the monic polynomial

    p_ab(lambda,g) = det(lambda I-K_ab(g))
                  = sum_(k=0)^m c_ab,k(g) lambda^(m-k).

The recurrence starts R0=I and uses

    c_k = -tr(K R_(k-1))/k,
    R_k = K R_(k-1) + c_k I.

Every coefficient division is checked exact. R_m vanishes coefficientwise,
giving a native all-parameter Cayley-Hamilton check for every block. The
full spectral equation in original source-action units is

    product_(a,b) p_ab(64 E,g) = 0,
    det(EI-H(g)) = 64^(-64) product_(a,b) p_ab(64 E,g).

All polynomial coefficients, original-state basis columns and reduced matrices
are retained in spectral_RESULT.json. The degrees20+16+16+12 retain all64
eigenvalues with multiplicity. For the declared candidate at g=1, the numerical
extrema are44.29800120076997 and245.84021379689852 in source-action units.
NUMERICAL_READOUT.json retains every eigenvalue at g=0,1/4,1,2 and the matched
block spectra. These are candidate-source spectra; physical energies are unassigned.

## Execution and checks

The native symmetry and polynomial calculations run as the explicit source-bound
LI6_FULL_GRAPH_SPECTRAL_R1 application operation through an ATOM3D DomainSession.
The current public operator recurrence admits dimensions at most16; the20-state
block is computed by this native GMP adapter. No global engine upgrade or
admission change occurs. Global runtime remains SLC-GEN3-R3 / SLC-GEN3-CEV1-R3,
GEN3-OPERATORLOG1-20260915-G1, domain engine A3D41-T18-CONTACT-R2.

77 independent checks pass. These include exact source-matrix intertwining,
character identities, full projector reconstruction, block determinants at
five (lambda,g) pairs per block using independent fraction-free elimination,
and two exact64-by64 determinant factorizations. Numerical full/block spectra
also agree at four coupling values. Numeric samples illustrate the exact
polynomial result; they are not its all-parameter justification.

Native accepted builds use undefined-behavior sanitization. The intermediate
automorphism build had one indentation warning; its source and build record
are preserved. The final spectral build is warning-free. No mathematical or
runtime failure occurred. The evolving native sources and original runner
are preserved alongside their source/binary hashes and session receipts.

## Roster integration and continuation

The compiler consumes the frozen FAMILY.json as a source spectral analysis,
retains its exact-result/validation hashes and displays it in Li6's details.
The existing17 selected Gaudin/obstruction records keep their original sector
identity. All37 recipes, two source mirrors and both exchange graphs remain.
The new analysis does not mark the whole isotope's spectrum or energy assigned.
Ten roster integration checks pass. A fresh checkpoint recovery returns the17
existing operator records by exact hash without increasing their native-call
counter. The final session contains40 returned calls with zero failed or
incomplete calls: three native spectral investigations,18 roster construction/
operator calls and19 recovery calls. The updated viewer data and JavaScript
syntax checks pass; browser interaction was not separately automated.

The next Li6 task is DERIVE_FULL_GRAPH_GAUDIN_CHARGES. A concrete feature for
that work is the six source potential levels: their multiplicities are
4,8,4,16,16,16 in increasing potential order. The earlier three-state charges
used distinct inhomogeneities within each block; a full-graph extension must
handle these repeated levels and the entire adjacency. O16 source-potential
binding remains the other roster task already identified by H001447.

## Artifacts

- [Family and source binding](FAMILY.json), [exact native result](spectral_RESULT.json).
- [Independent checks](VALIDATION.json), [numerical readout](NUMERICAL_READOUT.json).
- [Updated roster](roster_run/ROSTER.html), [roster JSON](roster_run/ROSTER.json).
- spectral.cpp, run.py, check.py; *_CONTRACT.json and *_STATUS.json retain actual execution custody.
- application_predecessor/ preserves the previous compiler installation.
