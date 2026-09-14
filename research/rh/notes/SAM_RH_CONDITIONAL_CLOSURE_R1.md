# SAM RH: conditional closure through the original signed excess

14 September 2026. Owner direction: pursue SAM RH closure, including theoretical
work and work pending independent validation. Sean Brady is originator and
conceptual director; OpenAI ChatGPT and Codex are AI research collaborators.
The full-energy identity is the adopted ChatGPT packet. The implications,
compression bound and explicit signed ancestry below are Codex derivations.
GEN3 supplies source-bound exact readouts through the existing native adapter.

**Status:** conditional closure theorem derived; its uniform arithmetic
hypothesis remains OPEN. Independent review of the derivation is pending.
These are two distinct outstanding items. No unconditional RH conclusion is
installed. The active target remains E=A-Q_a/2, with its full signed history.

## 1. Exact statement sufficient for closure

For every dyadic s>=2 and every integer 0<=t<=s, let

    a_i = mu(s+i) 1_(i<t),
    b_i = [1_(s+i even) mu(s+i) + mu(2(s+i)+1)] 1_(i<t),
    v = -a+b,
    Q_s(a) = M_a^2/s + sum_(r=1)^(s-1) q_a(r)^2/[r(s-r)],
    q_a(r) = sum_(i<r) a_i - r M_a/s,
    E(s,t) = Q_s(b)/2 - <a,b>_s - Q_s(a)/2.

All means, centered cuts, stops and the complete signed cross term are the
original ones. Write Q(s,t)=Q_s(a). The arithmetic hypothesis is

    (H) For every eta>0 there is a finite C_eta, independent of s and t,
        such that E(s,t) <= C_eta s^eta for all dyadic s>=2 and 0<=t<=s.

The constant candidate E<=1 implies (H). Fixed polylogarithmic growth also
implies (H). Neither constant control nor monotone excess is necessary for
the following sufficient argument. A finite initial range can be absorbed
into C_eta; an unbounded omitted range cannot.

**Conditional conclusion:** (H) yields subpower full SAM energy, square-root
Möbius cancellation with every positive exponent allowance, and RH. The
original projected interactions retain [X_adm]_+<=Qhat<=Q. Their original
roster transfer remains as specified in the adopted packet; the direct
Möbius argument below additionally reaches RH without using roster-size
notation or changing its normalizations.

## 2. Signed transport, including every odd endpoint

The adopted identity and geometric bounds give

    Q(2s,2t) = Q(s,t) + E(s,t) + R(s,t),  R<=3.

For an odd stop let

    J(s,t) = Q(2s,2t+1)-Q(2s,2t),  J<=2.

J is the actual signed endpoint increment, not the number 2. Thus for
epsilon in {0,1}, whenever 2t+epsilon<=2s,

    Q(2s,2t+epsilon) = Q(s,t)+E(s,t)+R(s,t)+epsilon J(s,t).       (1)

For a terminal source (2^K,T), set t_j=floor(T/2^(K-j)), for 1<=j<=K,
and epsilon_j=t_(j+1)-2t_j. Summing (1) gives the exact ancestry identity

    Q(2^K,T) = Q(2,t_1)
      + sum_(j=1)^(K-1) [E(2^j,t_j)+R(2^j,t_j)
                         +epsilon_j J(2^j,t_j)].                 (2)

Negative excess, negative geometric remainder and negative endpoint increments
all remain in (2). No positive-part or absolute-value sum replaces them.
The admission identities from H001426 still describe each E within its
surrounding source interval; (2) adds exact accounting between source scales.

An upper bound on the complete signed sum in (2), uniformly over terminal
sources, suffices as well. This is an accounting consequence, not an assumed
predictive rule: evaluating that sum after its sources are known is not a
derivation of a uniform upper bound.

## 3. Close the energy induction under (H)

Let H_j=max_(0<=t<=2^j) Q(2^j,t). Equation (1) and (H) imply

    H_(j+1) <= H_j + C_eta 2^(j eta) + 5.

Consequently, for K>=1,

    H_K <= H_1 + C_eta (2^(K eta)-2^eta)/(2^eta-1) + 5(K-1).     (3)

To obtain H_K=O_delta(2^(K delta)) for any delta>0, use eta=delta/2
and absorb the linear K term. Constants may depend on delta but not on K
or the stop. There is no exchange of a finite tested maximum with a uniform
constant here: the constant in (3) comes from the explicit hypothesis (H).

For the stronger hypothesis E<=C(1+log s)^p, C>=0 and p>=0, summation gives
H_K=O((1+K)^(p+1)). In particular E<=1 would give H_K<=H_1+6(K-1).
These are consequences of the respective hypotheses, not measured bounds
outside the completed native scope.

## 4. Close the passage from SAM energy to the zeta zero statement

Let M(x)=sum_(n<=x) mu(n). Nonnegativity of the cut energy gives, for every
stopped dyadic block,

    |sum_(i<t) mu(s+i)| <= sqrt(s Q(s,t)).                         (4)

Partition [1,floor x] into complete blocks [2^j,2^(j+1)-1] and the final
stopped block. Use (3) in (4), then sum the geometric sequence of block
amplitudes. For every epsilon>0 this yields

    |M(x)| = O_epsilon(x^(1/2+epsilon)).                          (5)

For example, use the energy exponent delta=2epsilon. At the stronger
polylogarithmic hypothesis above the same calculation gives
M(x)=O(sqrt(x)(1+log x)^((p+1)/2)).

For a complex variable w with Re(w)>1/2, define

    F(w) = w integral_1^infinity M(x) x^(-w-1) dx.

On every compact subset of this half-plane choose epsilon strictly smaller
than its distance to Re(w)=1/2. Equation (5) supplies an integrable uniform
majorant, including the logarithmic factors required by differentiation.
Thus F is holomorphic there. Partial summation and the classical Möbius
Dirichlet series give F(w)=1/zeta(w) when Re(w)>1. The classical identity is
[DLMF 27.4.5](https://dlmf.nist.gov/27.4.E5).

On the connected domain {Re(w)>1/2}\{1}, the identity theorem now gives
zeta(w)F(w)=1. Hence zeta has no zero in that half-plane. The
[zeta reflection formula](https://dlmf.nist.gov/25.4.E2) sends each nontrivial
zero to its reflection across Re(w)=1/2. A nontrivial zero to the left would
therefore give one to the right. All nontrivial zeros consequently lie on
Re(w)=1/2, under (H). The pole at 1 is excluded explicitly and causes no
zero argument at that point.

The cited classical inputs are independent of SAM; the conditional analytic
continuation above is written out to expose every implication being used.

## 5. The excess condition matches the full-energy cancellation scale

There is a useful reverse algebraic estimate. For any fine vector z of
length 2s, put v_i=z_(2i)+z_(2i+1). Its mean is M_v=M_z and its centered
cuts satisfy q_v(r)=q_z(2r). Therefore

    Q_s(v) = M_z^2/s + sum_(r=1)^(s-1) q_z(2r)^2/[r(s-r)]
           <= 4 Q_(2s)(z).                                      (6)

Indeed, the mean on the right is twice that on the left, its even-cut
terms equal those on the left, and its remaining odd-cut terms are
nonnegative. Polarization in the original kernel gives

    E(s,t)=Q_s(v)/2-Q(s,t) <= 2 Q(2s,2t)-Q(s,t).                  (7)

Thus subpower full energy implies the same one-sided subpower excess
condition (H). No bound on |R| is used. Combining this with Section 3
establishes equivalence of (H) and uniform subpower full energy.

For completeness, the cancellation estimate (5) also implies subpower full
energy. Suppose |M(x)|<=D_delta x^(1/2+delta), enlarged to cover x>=1.
Every partial sum P_r of a stopped source in [s,2s) has magnitude at most
L=2D_delta(2s)^(1/2+delta); so |M_a|<=L and |q_a(r)|<=2L. Since

    sum_(r=1)^(s-1) 1/[r(s-r)] = 2 H_(s-1)/s,

we obtain Q(s,t)<=L^2(1+8H_(s-1))/s. Choose delta smaller than half the
desired energy exponent and absorb the logarithm. Thus (H), subpower full
energy and (5) are equivalent within the stated quantifiers. The constant
candidate E<=1 is stronger than the subpower formulation and is not assigned
this equivalence.

## 6. Where the attempted unconditional closure currently reaches

Applying (7) inside (1) gives

    Q(2s,2t) <= 2Q(2s,2t)+R(s,t),

which rearranges to a lower bound Q(2s,2t)>=-R(s,t). It supplies no upper
energy induction. The compression inequality therefore clarifies the scale
of the target but cannot be used as its own closure hypothesis.

The current four-admission certificates start from actual weighted states
and bound their possible continuations. A renewable certificate must also
establish that every reached terminal state satisfies the premise needed
for the next certificate, with a bound uniform in s. The existing calculation
starts a new certificate using each observed actual state; it has not
established that invariant for all subsequent states or unbounded scales.
Likewise the frozen fitted sign-class bounds have their recorded failures.

The exact missing statement is therefore (H), or a source-derived signed
budget sufficient for the sum in (2). A derivation must use actual arithmetic
relations to control repeated reinforcement and later compensation before
assuming the final energy bound. The exact one-admission law, full divisor
identity and weighted state are available inputs. Neither finite maxima nor
assumed repayment fills this step.

The useful advance is a complete conditional path from the unchanged SAM
source target to RH, with signed scale accounting and explicit converse
energy control. The remaining arithmetic obligation is named rather than
being classified as an already derived result awaiting external review.

## 7. Native validation and continuing research boundary

`tools/forcing_closure_r1.py` calls the installed native forcing operation
through NativeDomainSession. Its source endpoints are the binary ancestors
of (4096,1071), (4096,1077), (4096,1130), and (8192,2142), the last carrying
the peak forcing into its actual fine source. Every E, R and odd increment
is retained in order. The script independently recombines native rationals
to check (2), (6), (7), endpoint agreement and the one-sided remainder bounds.
Counts and session receipts are in `results/forcing_closure_r1/COMPLETION.json`.
These checks concern exact finite identities, not hypothesis (H).

The completed run has22 unique native witnesses,48,340 native internal checks
and356 independent rational checks, all passing. The complete signed ancestry
totals below have base energy zero; displayed values are rounded, while the
receipt retains exact rationals.

| Terminal (s,t) | Sum E | Sum R | Sum odd increments | Final Q |
|---|---:|---:|---:|---:|
|4096,1071|0.311947564468|-0.059308178194|0.013487611776|0.266126998049|
|4096,1077|0.299731512131|-0.059263587500|0.025652240451|0.266120165082|
|4096,1130|0.361477014828|-0.059436594168|0|0.302040420660|
|8192,2142|0.826347623585|-0.059629619607|0.013487611776|0.780205615753|

For the exact signed scale-accounting experiment: **The test result suggests
strong contact with the concept.** This classification concerns the tested
identities. The uniform hypothesis (H) has not been established by this run.
In particular, the final Q column is full source energy, not the excess
measured at that terminal source. The negative accumulated remainder is a
retained mathematical contribution, not replaced by its upper bound3.

All selected points have the role OWNER_FOCUSED_THEORETICAL_VALIDATION.
They do not enter fitting; scale4096 remains held out of fitting. No selector,
feedback budget, pod stop, backup schedule or producer policy is changed.
The manuscript's derived steps are available for independent review now;
the unbounded source estimate remains the active theoretical task.
