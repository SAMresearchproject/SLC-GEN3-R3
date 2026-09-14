# The linear-transport bound that would complete the original target

Use DERIVATION.md(8). For each original s and stop t, let T_(s,t) map a
smaller coefficient vector v(m), m<=M=floor((2s-1)/A²), to the stopped
source sum_(mb=n)v(m)(r*r)(b) in the original block. The kernel r uses the
ACTUAL fourth-root anchors and explicit auxiliary completion. Let P_s be
the completed original mean/prefix projection. On the input define

    E_M(v)=sum_(dyadic N<=M) Q_(N,T_N)(v(N),...,v(N+T_N-1)),
    T_N=min(N,M-N+1),

using the same full original block geometry and zero padding at the last
stop. This is an auxiliary norm on the actual smaller source, not a new
choice of the original cutoff sequence.

The current attempted sufficient estimate is

    ||P_s T_(s,t)v||² <= C (1+log(e+s))^p E_M(v)       (1)

uniformly in original s,t, with fixed C,p, for the actual source-dependent
kernel. The native finite check examines this operator inequality for all
input vectors and retains the actual mu vector's contraction separately.
If a source-restricted estimate is needed instead, it must state exactly
which actual relations it uses; it will not silently replace(1).

## Why this estimate would finish the task

Let E(x) sum, over all dyadic scales N<=x, the maximum original source
energy over available stops at each scale. It is an auxiliary monotone
envelope. The completed constant projection residual and quartic additive
bound imply from(1)

    1+E(x) <= C' (1+log(e+x))^(p+6) [1+E(sqrt(2x))]. (2)

There are at most1+log_2 x scales. The exponent p+6 is a safe common
envelope for the polylogarithmic transport/additive terms; no new source
assumption is used in this transfer. For sufficiently large x the argument
sqrt(2x) decreases, and iterating(2) gives

    log(1+E(x))=O((loglog(e+x))²), E(x)=x^o(1).       (3)

Indeed log x is halved up to a fixed additive constant at each iteration;
the sum of O(loglog x) additive logarithmic costs over O(loglog x) levels
is O((loglog x)²). The terminal finite-scale energy is finite by |mu|<=1.
Thus every original roster is controlled, including the SAME prescribed
common sequence and every admissible stop. H001202 then returns the
original signed-feedback and positive-part criterion with its fixed tau.

This is a conditional completion argument. The uniform operator estimate(1)
is the present analytic target; finite matrices do not establish its constants.

## Exact finite certificate geometry

Each input dyadic block N with stop T has independent coordinates M,C_1,...,
C_(T-1), and diagonal energy weights

    d_M=T/N²+(H_(N-1)-H_(T-1))/N,
    d_r=1/[r(N-r)].

If K_i is an output column for input position i, the transformed columns are
(sum_(i<T)K_i+(N-T)K_(T-1))/N for M, and K_(r-1)-K_r for C_r.
The native compiler forms their full output Gram matrix G and input diagonal
D. A rational LDL certificate for C*D-G>=0 gives a finite bound. A host
calculation may propose the rational witness; GEN3 checks the matrix identity
and every pivot sign. The exact source contraction is checked independently
against the already retained projected transport.

## Source-divisor restriction and the fourth-root recursion

The actual smaller source satisfies sum_(d|n)mu(d)=0 for every n>1.
Let u be the fourth-root cutoff and M the smaller-source endpoint. Define
an integer extension matrix E from positions1,...,u to1,...,M by

    E_(n,j)=1_(n=j), n<=u,
    E_(n,j)=-sum_(d|n,d<n)E_(d,j), n>u.              (4)

Then mu(1..M)=E mu(1..u) exactly. This uses the actual divisor relations,
with no new source values or boundary assumptions. The current restricted
transport is P_s T_(s,t) E, measured against the SAME dyadic input geometry
through u. In the saved s1024 calculation it has6 input coordinates instead
of41, and all45 original output coordinates remain.

The intended bound may be weakened from polylogarithmic to SUBPOWER gain:

    for every epsilon>0, ||P_s T_(s,t)E z||²
            <=C_epsilon s^epsilon E_u(z)            (5)

uniformly in s,t for the actual source-dependent kernel. It is enough to
establish(5) on the actual low source if a source-specific proof supplies it.
The native finite matrix bound over all z is one sufficient route, not a
new project requirement.

The completed additive bound then gives an auxiliary recurrence with
argument(2x)^(1/4). Iterating with any fixed epsilon costs a geometric sum
epsilon*(1+1/4+1/16+...)log x plus O_epsilon((loglog x)²).
Thus E(x)<=x^((4/3)epsilon+o(1)); arbitrary epsilon yields E(x)=x^o(1).
This preserves the SAME original common sequence and its fixed constants.
The remaining obligation is the uniform signed gain in(5), not the finite
divisor extension or its original-criterion transfer.

For economical exact finite certificates, the executed route uses positive
weights w solving(CD-|G|)w=D*1. If w>0, each margin is positive and the
symmetric matrix CD-G is a sum of squares. This retains the signed G and
actual source energy; |G| is used only to certify the proposed operator norm.
