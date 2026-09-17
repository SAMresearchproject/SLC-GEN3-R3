# Native Li-6 pair: exchange-word preparation, collective equation and charge

Date: 2026-09-15 (America/Chicago). Sean Brady supplied the native algorithmic
Bethe-string direction and authorized the direct construction. Codex, OpenAI
AI research collaborator, supplied the construction, derivation and execution.

## Result

The original Li-6 source now has an explicit native two-excitation construction:

    Psi(z) = (Omega + z R_L R_R Omega)/sqrt(1+z^2),
    delta z^2 - 4 c z - delta = 0.

The reference, creation operators and supporting projector are polynomials
in admitted source cycle operations. These states are exact eigenstates of
the full64-state Hamiltonian in its accepted invariant quartet. The original
potential and all302 reversible exchange pairs remain. The construction
works throughout the accepted13-dimensional quartet-preserving amplitude
family, with the pure-state limit handled when delta=0.

For the native collective pair, its exact source eigenstate construction and
the charge organizing it: **The test result suggests strong contact with the
concept.**

One full-support example has z=sqrt(5)-2, a finite-quartet pair-addition defect
of -6g for g>0, and mean layer-graph separation reduced from1 to
1-1/(2sqrt(5)). The construction gives a native algorithmic pair and a solved
reference for the Bethe continuation. A native spectral-parameter/scattering
law and a Bethe-string assignment remain open.

## Native reference and creation words

Use the established intrinsic layer order

    28,57,85,170,198,227,309,422.

Indices below are zero-based. The two local quartet states are

    u0=(e1+e6)/sqrt(2),   u1=(e3+e7)/sqrt(2).

For admitted cycle k, write E_k for its directed raising matrix and
F_k=E_k+E_k^T. Cycle5 sends layer masks57->170,85->198,309->422.
It sends u0 to u1 and annihilates u1. Cycle1 symmetrizes the two source
representatives in each u state. The local and full quartet projectors are

    p=(F1^2+F1)/2,       P=p tensor p.

These equal the accepted source projectors exactly. Define

    |->=(u0-u1)/sqrt(2),     |+>=(u0+u1)/sqrt(2),
    Omega=|-->.

The reference is directly prepared from a source code:

    |->=(I-F5)(I+F1)|57>/2.

On the original64-state graph this is

    Omega=(I-A22)(I+A6)(I-A23)(I+A7)|s=(57<<9)>/4.

Set E=E5, Z=E^T E-E E^T and

    R=(Z+E-E^T)/2,
    R_L=R tensor I,   R_R=I tensor R.

R is nilpotent, R|->=|+>, R|+>=0, and the two layer operators commute.
Consequently R_L R_R Omega=|++>. The directed matrices come from the actual
source cycle orientations. No additional source states are introduced.

## Full-source eigenstate equation

Keep H=V+g A(w) and the accepted13 amplitude directions. In this section

    mu=w4+2w6,   a=w20,   b=w21,   c=w22=w23,
    J=(a+b)/2,   delta=(a-b)/2.

These a,b,c names are quartet parameters, distinct from the five variables
named a,b,c,d,e in H001460. In the normalized source basis
|-->,|-+>,|+->,|++>, the quartet exchange matrix is

    B = [ mu+J-2c     0          0       delta    ]
        [    0      mu-J     -delta       0      ]
        [    0     -delta     mu-J        0      ]
        [  delta      0          0      mu+J+2c  ].

V is959/4 times I on this subspace. The calculation checks A(w)W=W B(w)
in every original source row for all13 amplitude directions; W/4 is the
normalized64-by4 source frame saved in NATIVE_RESULT.json.

Substitute Omega+z|++> into every source eigenstate equation. The energy and
remaining coefficient are

    E(z)=959/4+g(mu+J-2c+delta z),
    (H-E(z))(Omega+z|++>)
       = -g(delta z^2-4cz-delta)|++>.

This derives the collective quadratic from the full source action. With
s=sqrt(4c^2+delta^2), the even energies are

    E_even,-/+ =959/4+g(mu+J -/+ s).

For c>0, the lower even state at positive g has the regular coefficient
z=-delta/(2c+s). Its orthogonal partner is (-z Omega+|++>)/sqrt(1+z^2).
The odd energies are959/4+g(mu-J +/- delta). At delta=0, Omega and |++>
are separately eigenstates. Quartet parity is conserved; bare excitation
number is mixed by the delta term.

## The charge organizing the pair

Let C=R_L R_R P. The projector R R^dagger counts the raised local state,
so the bare and dressed excitation numbers are

    N=(R_L R_L^dagger+R_R R_R^dagger)P,
    T=2c(N-P)+delta(C+C^dagger),
    N_dressed=P+T/s.

N_dressed has quartet eigenvalues0,1,1,2, assigning0 and2 to the lower and
upper even states. Native exact arithmetic checks [H,T]=0 and
T^2=s^2 P_even; the parameter commutator identity is checked on every pair
of the13 amplitude directions. An independent reconstruction checks the
lifted charge in the original64-state matrices.

For fixed amplitudes this is a quartet-supported constant charge in the
already established quartet charge span. It gives that charge an explicit
native excitation interpretation. The remaining complement charge search
retains its H001460 status.

## Pair addition, correlation and native separation

For g>0 define the finite-quartet pair-addition defect by

    Delta_add=E_even,+ + E_even,- - 2 E_odd,min
             =g[2(a+b)+|a-b|].

This compares the even pair excitation gap with twice the lowest odd
excitation gap, relative to the lower even reference. Both even levels are
mixtures of zero and two bare excitations when delta!=0; their excitation
labels refer to N_dressed. The lower even state is the quartet ground in all
six reported examples. The quartet is an excited invariant manifold of the
full64-state system. Delta_add is a finite-sector addition diagnostic;
a spatial asymptotic two-particle threshold is unassigned.

For the attractive example choose all y coordinates1 except
y7=-3,y8=-1 (y9=1). Thus mu=3,a=-3,b=-1,c=1 and every source amplitude is
nonzero. At g=1:

    z=sqrt(5)-2,
    E_even,-=238.5139320225002,
    E_even,+=242.9860679774998,
    E_odd,min=243.75,        Delta_add=-6.

The lower pair has double-excitation probability
p=z^2/(1+z^2)=0.0527864045..., connected excitation correlation
p(1-p)=1/20, and two-layer concurrence1/sqrt(5).

Define relative separation as shortest-path distance between the two masks
on the actual eight-state layer graph. For the reference Omega its mean is1
and its same-mask probability is1/4. For the attractive lower pair these are

    mean distance = 1-1/(2sqrt(5)) =0.7763932022500211,
    same-mask probability = (1+1/sqrt(5))/4 =0.3618033988749895.

This separation is a source graph observable, not a nuclear length.

| Example (a,b,c) | Delta_add/g | Concurrence | Mean source separation |
|---|---:|---:|---:|
|(-3,-1,1)|-6|0.4472135955|0.7763932023|
|(-2,-2,1), conversion off|-8|0|1|
|(1,3,3)|10|0.1643989873|0.9178005063|
|(-1,-3,1), opposite conversion|-6|0.4472135955|1.2236067977|
|(-5,-1,1)|-8|0.7071067812|0.6464466094|
|(-3,-1,4)|-6|0.1240347346|0.9379826327|

The conversion-free control retains an attractive addition defect while its
states are products. Reversing delta preserves the quartet spectrum and
concurrence but changes native separation. These results distinguish the
energy interaction, coherent pair conversion and source-coordinate
organization. The three observables carry different information.

## Connection to the charge search and Bethe construction

The most recent coupled-amplitude search varied y3,y4,y6,y10,y12 with the
other eight fixed to a common scale. All five directions leave B unchanged.
In its normalized convention a=b=c=1 and delta=0. The new pair-conversion
direction is y7-y8, already allowed by the full13-dimensional source family.
This explains precisely why the latest complement search did not probe this
collective pair mixing.

Test a pure raising construction on the bare native reference:

    B(lambda)=f(lambda) R_L+h(lambda) R_R.

Nilpotency and commutation give

    B(lambda1)B(lambda2)Omega
       =[f(lambda1)h(lambda2)+h(lambda1)f(lambda2)]|++>.

Its source residual has a reference component g delta Omega. For delta!=0,
no choices of the two parameters make this nonzero vector an eigenstate.
For this raising-only two-B ansatz on Omega with nonzero conversion:
**The test falsifies the concept.** The native mixed pair above supplies the
replacement reference and dressing; extending the creation algebra is next.

The retained auxiliary three-spin Gaudin result has a three-dimensional
two-excitation sector and an independently verified conjugate rapidity pair.
This native quartet has a one-dimensional bare double-excitation sector and
a two-dimensional even mixed sector. Its real collective coefficient z
currently obeys the source quadratic above. The auxiliary rapidities have
not been assigned to z or to these native states.

The next concrete construction should add native layer excitation modes and
derive a spectral-parameter creation law whose two-excitation residual is
nontrivial. The solved pair and dressed number provide exact reduction and
reconstruction formulas. NEXT_QUESTION.json records that continuation together
with the unchanged eleven H001460 complement charge charts.

## Execution and files

Two actual ATOM3D DomainSession calls use source-bound C++/GMP adapters on
A3D41-T18-CONTACT-R2 / SLC-GEN3-R4 / SLC-GEN3-CEV1-R4, generation
GEN3-CERTIFIEDLOG1-20260915-G1. The installed interface has no first-class
native-pair operation; this is an explicit application adapter, following the
preceding Li-6 campaigns. No global runtime revision is installed.

15,594 native assertions and189 independent checks pass. The first call
checks preparation/creation, all13 full-source direction identities, the
quadratic residual and six complete state reconstructions. The second checks
native projector/preparation and the dressed charge. Independent Python/NumPy
checks reconstruct the original phase moves and graph, integer identities,
full64 spectra, state residuals, correlation and charge action. Build
warnings and their scope are preserved in EXECUTION_NOTES.json. Neither
domain call failed or remained incomplete.

- [Native pair output](NATIVE_RESULT.json), [preparation and charge](DRESSED_RESULT.json).
- [Independent source checks](VALIDATION.json), [independent charge checks](DRESSED_VALIDATION.json).
- [Session receipts/status](DRESSED_STATUS.json), [summary](SUMMARY.json).
- [Next question](NEXT_QUESTION.json), [execution notes](EXECUTION_NOTES.json).

Physical amplitude selection, MeV assignment, paused training and the suspended
Chalkboard retain their existing scope.
