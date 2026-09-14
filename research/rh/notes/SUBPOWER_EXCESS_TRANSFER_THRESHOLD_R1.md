# Subpower excess: the arithmetic transfer threshold

14 September 2026. Codex derivation within the Sean Brady / OpenAI ChatGPT /
Codex SAM research collaboration. Owner instruction: obtain the subpower
excess bound using the existing theory and work, with a20-minute window for
updated material to be made downloadable.

**Outcome:** a weaker sufficient arithmetic transfer condition is derived,
including a scale-dependent exponent tending to the critical value2. Its
uniform actual-source validity is unresolved. This manuscript does not install
the requested subpower bound as established. It records the new analytic
reduction and the precise remaining source inequality.

The target is still the full signed E(s,t)=A(s,t)-Q(s,t)/2. The retained
divisor identity and original derivative norm are used without replacing
Möbius factors by arbitrary vectors or separating their signed band energies.

## 1. Use the existing smaller-source geometry

For s=2^j, j>=1, retain the campaign's literal input energy

    U_s = sum_(dyadic n<=u) Q_n(mu(n),...,mu(min(2n-1,u))),
    u=floor(sqrt(2s-1)),

with original zero padding. In particular U_s>=1. Write F_m(s,t) for the
retained original spectral energy, m=min(s-1,ceil(sqrt(s))). The existing
exact tail gives Q(s,t)<=F_m(s,t)+1.

The joint dual identity, with the complete signed divisor sum, is

    F_m(s,t) = sup_(f in H_m, f!=0) |L_(s,t)(f)|^2/R_s(f),
    L_(s,t)(f) = -sum_(a,b<=u) mu(a)mu(b)
                   sum_(v=ceil(s/(ab)))^floor((s+t-1)/(ab)) f(abv-s),
    R_s(f) = (sum_i f_i)^2/s
             +sum_(r=1)^(s-1) r(s-r)(f_(r-1)-f_r)^2.

All signed factor-pair interactions are inside L before squaring. This
retains the cancellation observed in the existing native band readouts.

The sufficient source inequality examined here is

    (T) |L_(s,t)(f)|^2 <= C(1+j)^A U_s^(p_j) R_s(f),

uniformly over actual dyadic sources, stops and f in H_m, with fixed finite
C>=0,A>=0. The previous candidate is the much more specific p_j=1,C=1/4,A=0.
The new deduction concerns which exponents p_j suffice; it does not assume
the previous candidate's uniform validity.

## 2. Exact reduction in the dyadic index

Put H_j=max_(0<=t<=2^j) Q(2^j,t) and J_n=1+sum_(j=0)^n H_j.
H_0=1. The largest dyadic block entering U_(2^j) has index floor(j/2):

    floor(log_2 floor(sqrt(2^(j+1)-1))) = floor(j/2).

For even j=2r, u lies between2^r and2^(r+1)-1. For odd j=2r+1,
u=2^(r+1)-1. Thus in both cases

    U_(2^j) <= J_floor(j/2).

Assume p_j is nondecreasing and p_j>=1; the constant case also qualifies.
Take the joint supremum in (T), add the exact tail, and sum whole energies.
For some fixed B>=1, enlarged for finite initial scales,

    J_n <= B(n+1)^(A+1) J_floor(n/2)^(p_n).                       (1)

For example B=C+3 suffices for n>=1: sum_(j=1)^n C(1+j)^A is at most
C n(n+1)^A, and the remaining unit tails and J's initial term are at most
n+2. Since J>=1, the claimed bound absorbs both contributions.

The square-root source reduction therefore acts by halving n=log_2 s.
An energy transfer power below2 can be iterated even when it exceeds1.

## 3. A fixed power below two is enough

Suppose1<p<2 and p_j=p. Set a=log_2 p, so0<a<1. Taking logarithms in(1),

    log J_n <= p log J_floor(n/2) + log B +(A+1)log(n+1).

Iterate to the fixed base range. At depth k the additive term is weighted
by p^k. Summing these terms gives

    log J_n = O(n^a),
    H_j <= exp(O(j^a)).                                          (2)

To see the sum explicitly, let d=floor(log_2 n). After reindexing k=d-r,
the bound is a fixed multiple of p^d sum_(r>=0)(1+r)/p^r; this series
converges for p>1. The base term is also O(p^d)=O(n^a).

The original pair-compression estimate gives

    E(s,t) = Q_s(v)/2-Q(s,t) <= 2Q(2s,2t)-Q(s,t) <= 2H_(j+1).

Therefore(T) implies the explicit subpower bound

    E(s,t) <= exp(O((log s)^(log_2 p))).                          (3)

For p=3/2 the exponent is log_2(3/2)<1. For each eta>0, the right side
of(3) is at most C_eta s^eta after absorbing finitely many scales. Negative
values of E require no absolute-value bound. At p=1, the same recurrence
instead gives log J_n=O((log(n+1))^2), agreeing with the earlier linear route.

## 4. Even a vanishing saving from two suffices

A fixed gap below2 is more than the induction needs. Let0<kappa<=1 and

    p_j = 2-kappa/log(e+j).

Then(T) still implies subpower excess. Here is an explicit bound. Set
q_m=log J_(2^m) and g_m=q_m/2^m. Equation(1) gives

    g_m <= [1-kappa/(2 log(e+2^m))] g_(m-1) + O((m+1)/2^m).

Fix any0<c<kappa/(2 log2). For all sufficiently large m the bracket is
at most1-c/m. Its products from r+1 to m are O((r/m)^c), so iteration gives

    g_m = O(m^(-c))

because sum_r r^c(r+1)/2^r converges. Monotonicity of J brackets general
n between consecutive powers of2 and yields

    log J_n = O(n/(log n)^c).

Consequently the unchanged excess satisfies, conditional on(T),

    E(s,t) <= C_0 exp[C_1 log(2s)/(log log(e^e+2s))^c],           (4)

uniformly in t. The exponent divided by log s tends to zero, so(4) implies
the requested E(s,t)<=C_eta s^eta for every eta>0.

This places the arithmetic target just below the quadratic input-energy
power. It allows the saving to shrink as1/log log s. It does not require a
constant forcing ceiling, a constant linear gain, or monotone compensation.

## 5. Why merely quadratic transfer does not finish this induction

With p_j=2, equation(1) gives only log J_n=O(n). In fact the model
J_n=exp(an), a>0, satisfies an inequality of form(1) for sufficiently large
n when its polynomial factor has positive degree: the rounding cost in
2 floor(n/2) is bounded and absorbed by that factor. Thus this recurrence
alone permits polynomial-in-s energy growth.

The bilinear source identity explains where this threshold enters. If the
two smaller-source factors were replaced by an arbitrary common vector x,
then L would be quadratic in x, its squared norm quartic, and the input
energy quadratic. Under x->lambda x, these scale as lambda^4 and
lambda^(2p), respectively. No nonzero unrestricted bilinear map can satisfy
the same source-independent bound with p<2 for all lambda.

Our task concerns the actual Möbius vector, with its arithmetic relations
and fixed coefficient values. The strict saving must be established for
that source class. Unrestricted tensor-norm estimates cannot silently supply
it. The observed large negative interband crosses indicate a mechanism to
retain; their finite values do not yet establish the scale-uniform saving.

## 6. Result and next exact source question

The derived result is the threshold theorem: (T), even with the above p_j
tending to2, supplies the original subpower excess bound. The unresolved
arithmetic question is now explicitly weaker than the prior linear transfer:

    Does the complete actual-source signed divisor functional satisfy(T)
    with p_j=2-kappa/log(e+j), for some fixed kappa>0 and polylogarithmic
    prefactor, uniformly in its original stopped source and test function?

This is a route to derive the SAME E bound, not a replacement of E or of its
kernel. No fit, held-out witness, finite maximum, independent-band absolute
charge, or assumed future repayment is used in the threshold derivation.

The arithmetic inequality(T) remains open. The previous conditional closure
manuscript carries the subsequent implication to RH. No new native research
arithmetic was needed for this manuscript derivation; the prior48,340 native
and356 independent checks remain evidence for their explicitly finite
identities. This note adds no new experimental classification or test count.
