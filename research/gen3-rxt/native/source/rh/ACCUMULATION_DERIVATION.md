# Source-accumulation compensator and the original positive-growth target

Owner direction: retain RUN2's worker/deadline, reuse admissions, separate
source history from search history, and develop a relevant arithmetic bound.
Codex supplies the derivation below. GEN3 executes the exact source-history
arithmetic, logarithmic accounts, candidate comparisons and selected follow-up.

## Definitions and positive-part placement

Fix the saved original U roster and tau_U throughout admission. In a block,
v_t=sum_(i<t)mu(s+i) P h_i, Q_t=||v_t||^2, with P the installed fixed cut-cell
projection. The full-kernel history is recorded alongside it with P=identity.
Let B_s=tau_U+sum_(earlier original blocks)Q_block. It is constant throughout
this block; all later blocks are zero. Write A_t=B_s+Q_t. Define RAW increments

    delta_t=mu(s+t)^2 ||P h_t||^2,
    F_t=2 mu(s+t)<v_t,P h_t>,
    Q_(t+1)-Q_t=delta_t+F_t,
    D_T=sum_(t<T)delta_t,  X_adm(T)=sum_(t<T)F_t.

The recorded fields d_raw/f_raw are delta_t/F_t. Normalized fields are

    d_t=delta_t/A_t,  f_t=F_t/A_t,  x_t=d_t+f_t>-1.

Thus the signed normalized feedback f_t differs from raw F_t; neither is
replaced by its positive part. The original target takes [X_adm(T)]_+ only
AFTER the complete block's signed sum, then sums over the original roster.
The U/D rise/fall decomposition is a diagnostic of the exact logarithmic
history, not a replacement target involving sums of positive admissions.

## Derived uniform lemma: signed accumulation minus variation loss

For every x>-1,

    x-log(1+x)=x^2 integral_0^1 u/(1+ux) du
              >= x^2/[2 max(1,1+x)].

This follows by bounding the positive denominator by max(1,1+x). Define the
nonnegative rational loss and its complete signed compensator

    L_t=(delta_t+F_t)^2/[2 A_t max(A_t,A_(t+1))],
    Phi_T=sum_(t<T)f_t - sum_(t<T)L_t.

Telescoping the exact logarithmic source history gives, at every scale/stop,

    log((B_s+Q_T)/B_s)
       <= sum_(t<T)d_t + Phi_T
       <= D_T/B_s + Phi_T.                              (L1)

The original geometry supplies D_T<=2-1/s. L1 is a derived uniform lemma:
it applies to every retained signed source path, not just tested paths.
It separates the whole signed feedback from the known diagonal budget and
an explicit loss caused by both rises and falls. It imposes no sign on
individual F_t and uses no clipped admission history.

## Candidate arithmetic inequality and its exact relevance

Motivated by the harmonic kernel below, test the following SOURCE-SPECIFIC
candidate, with H=H_(s-1):

    Phi_T <= H D_T/B_s.                                 (C1)

C1 is proposed, not established uniformly. Tests cover only retained actual
source admissions. Its right-hand side is controlled: H is geometry,
D_T<=2-1/s, B_s>=tau_U. Although B_s contains prior source energy, that
baseline can be eliminated in the consequence without bounding that energy.
Indeed L1+C1 imply, with C=(1+H)D_T,

    Q_T <= B_s[exp(C/B_s)-1]
         <= C exp(C/B_s)
         <= 2(1+H) exp(2(1+H)/tau_U).                    (L2)

The middle inequality is exp(z)-1<=z exp(z) for z>=0. On the ORIGINAL roster,
H<=1+log U, the number of blocks is O(loglog U), and tau_U grows in proportion
to loglog U from the recorded successive-dyadic roster. Hence the roster
sum in L2 is U^o(1), uniformly in the original stops, on the same common
sequence. The completed original transfer then applies.

This is a conditional closure route through ONE candidate estimate, not a
new required bound. The original weighted interaction bound remains the
objective if another route succeeds. The exact additional inequality needed
here is C1 on the actual source at unbounded original scales, with the
original constants. A finite maximum of B_s Phi/(H D) only measures the tested
paths; it does not establish C1 uniformly.

## Source arithmetic inside the compensator

For the full kernel, direct summation of the retained cut geometry gives,
for i<=t,

    K(i,t)=1/s^2+[2H_(s-1)-H_(s-i-1)-H_t]/s.

Let M_t=sum_(i<t)mu(s+i), J_t=sum_(i<t)mu(s+i)H_(s-i-1). Then

    F_t=2mu(s+t){[1/s^2+(2H_(s-1)-H_t)/s]M_t-J_t/s}.      (A1)

This identifies the actual harmonic-weighted signed prefix whose interaction
must be estimated; it is not a generic vector norm. For the projected kernel,

    F_t=2mu(s+t)[M_t/s+sum_I beta_I(t)Z_I(t)/W_I],
    Z_I(t)=-sum_k c_u(k) H_(I,t)(k),
    c_u=mu_(<=u)*mu_(<=u), u=floor(sqrt(2s-1)).            (A2)

The retained identities give H_(I,t)(k)=J_I(t)/k+E_(I,t)(k), with
|E_(I,t)(k)|<=2W_I and the original partial-stop J_I retained. Inserting A2
into C1 makes its unresolved arithmetic content explicit:

    sum_t 2mu(s+t)/A_t *
      [M_t/s - sum_I beta_I(t)/W_I sum_k c_u(k)H_(I,t)(k)]
      - sum_t L_t <= H D_T/B_s.                          (A3)

All t, I and k sums retain their signs. The known discrepancy bound alone
would leave sum|c_u(k)| if used term by term; that does not close A3.
The next source question is which actual divisor/cofactor relation supplies
compensation at the retained prefix where native selection finds the greatest
relative demand B_s Phi/(H D). That witness is chosen by source-history
arithmetic, not novelty or a changed score designed to force a new winner.

## Explicit documented fourth-root route

F12-F18 of the retained formula packet give the auxiliary completion
f(A)=-A S(u4), generally not mu(A), and R=mu+a2, where
Q(a2)<=32(1+H_u4)^4(1+8H_(s-1)). The actual smaller-source transport reduces
to fourth-root anchors and E_u4>=1. The open sufficient estimate is

    max_t Qhat_s,t(R) <= C_epsilon s^epsilon E_u4.

That right-hand side is a smaller-scale quantity with the completed recursive
transfer. The transfer is valid; its source-specific gain inequality remains
open. C1 applied to the original source is an alternate route. Neither the
same-scale comparison Q(R)<=2Q(mu)+2Q(a2), nor a finite observed ratio,
substitutes for the smaller-scale gain bound.
