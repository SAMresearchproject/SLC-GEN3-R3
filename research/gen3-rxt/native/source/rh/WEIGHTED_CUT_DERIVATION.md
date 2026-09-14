# Weighted cut-cell source energy and the exact missing interaction

Owner requested GEN3 investigation of weighted cut-cell projected energy and
the uniform subpower bound for the actual retained signed Mobius source.
Codex derives the following from the completed original geometry and projection;
GEN3 executes its source-bound finite contractions. No new closure requirement.

## Original projected kernel

Use a_i=mu(s+i) for0<=i<t and zero otherwise, in the original length-s block.
Let h_i have mean coordinate1/sqrt(s) and centered cut coordinate
(1_(i<r)-r/s)/sqrt(r(s-r)). For the installed orthogonal cell projection P,

    Khat_(i,j)=<P h_i,P h_j>
      =1/s+sum_I beta_I(i) beta_I(j)/W_I,
    beta_I(i)=sum_(r in I,r>i)w_r-(1/s)sum_(r in I)r w_r,
    w_r=1/[r(s-r)],  W_I=sum_(r in I)w_r.                    (1)

Thus the actual retained signed energy is exactly

    Qhat_s,t=sum_(i,j<t) mu(s+i)mu(s+j) Khat_(i,j)
      =M_s(t)^2/s+sum_I Z_I^2/W_I,
    Z_I=sum_(i<t)mu(s+i)beta_I(i).                           (2)

Source summation precedes each square. Means, original weights and zero-padded
stops remain included. The kernel is fixed by geometry, independent of mu.

## Uniform constant diagonal bound

The full Gram matrix K of the h_i has trace

    tr K=sum_i 1/s
         +sum_(r=1)^(s-1) [sum_i(1_(i<r)-r/s)^2]/[r(s-r)]
        =1+sum_(r=1)^(s-1)1/s =2-1/s.                      (3)

Here sum_i(1_(i<r)-r/s)^2=r(s-r)/s exactly. Since P is orthogonal,
Khat is positive semidefinite and tr Khat<=tr K. Define the ADMISSION diagonal
and cross term, distinct from the earlier primitive-channel and cofactor symbols:

    D_adm=sum_(i<t)mu(s+i)^2 Khat_(i,i),
    X_adm=2sum_(0<=i<j<t)mu(s+i)mu(s+j)Khat_(i,j).

Because |mu|<=1 and Khat_(i,i)>=0,

    0<=D_adm<=tr Khat<=2-1/s<2,
    Qhat_s,t=D_adm+X_adm.                                  (4)

This bound is established uniformly for every scale and stop, including the
finite base s1. It uses no cancellation hypothesis or numerical constant fit.

Nonnegativity of Qhat and(4) give

    [X_adm]_+ <=Qhat_s,t <=[X_adm]_++2-1/s.                 (5)

Hence, on the SAME original roster/common sequence, the exact original
projected-energy subpower target is equivalent to

    for every eta>0,
    sum_original_roster [X_adm(s,t)]_+ <= C_eta U_j^eta.     (6)

Equation(6) is the original target expressed through weighted Mobius pair
interactions. It is OPEN. There is no separate diagonal obligation, and no
requirement that every pair or every block cross term be nonpositive.

## Connection to the already fixed normalization

The original tau_U is exactly sum_roster(2-1/s), the full energy-matrix trace.
Let V_U=sum_roster[X_adm]_+. Summing(4)-(5) gives

    V_U<=Qhat_U<=V_U+tau_U,
    1<=(tau_U+Qhat_U)/(tau_U+V_U)<=2.                       (8)

The completed original projection residual is at most8 times the roster
count, and tau_U is at least that count. Consequently

    1<=(tau_U+Q_U)/(tau_U+V_U)<=10.                         (9)

Thus the original logarithmic criterion and the retained actual pair-cross
criterion differ by at most log10, with the SAME original tau. This is a
completed transfer with an absolute constant, not another growth estimate.

## What is actually missing

The projection error is already uniformly bounded by8; the admission diagonal
is now uniformly bounded by2. Source identities and kernels are explicit.
The missing implication is a quantitative, source-specific bound on the
POSITIVE part of the complete weighted pair interaction in(6), uniformly
along the prescribed common unbounded sequence. Kernel boundedness and exact
source reconstruction do not by themselves bound that signed contraction.

For the original fourth-root route, write Gamma=max_t Qhat(R;t)/E_u,
rho=max_t M_s(t)^2/(s E_u), ell=Lbound_s/E_u, H=H_(s-1).
The completed equivalent reductions say

    Gamma<=2(1+8H)rho+2ell,  rho<=2Gamma+2ell.

Substituting one into the other gives only

    Gamma<=(4+32H)Gamma+(6+32H)ell.                         (7)

For H>=0 this supplies no upper bound on Gamma: the same unknown returns
with coefficient at least4. This identifies why a transfer identity is not
the missing estimate. Equation(7) does not contradict any completed result;
it diagnoses the dependency structure of this particular combination.
GEN3 can verify the polynomial coefficient composition exactly.

The implication needed is(6), or equivalently any established source-gain
estimate sufficient for the recorded recurrence. These are alternate routes
to one target. No additional data, invented phase, source or new tau enters.

## Native investigation

At original s1024,t395 and auxiliary s2048,t783 and s4096,t4064/t4095,
retain all installed weighted cells. Execute original mu projection; reuse
existing cell outputs where present. Compute D_adm, X_adm, projected trace,
mean/cell energy, and the largest cell with all ties. Identify whether the
measured positive cross interaction is in the mean or the retained cut cells.
Check exact energy reconstruction and the new constant diagonal consequence.
This evaluates the actual signed source in(6), not an unrestricted input norm.

For efficiency beta_I(i) is constant before and after its cell. Native prefix
counts of mu^2 and signed mu sums contract those tails; only each cell's own
interior is traversed. Total lowering is linear in s plus the number of cells.
