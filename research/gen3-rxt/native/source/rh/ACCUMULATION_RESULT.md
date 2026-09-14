# Source accumulation: completed research cycle and remaining estimate

Status: completed bounded source-history investigation; RUN2 is now paused
by owner. No further native computation was launched after the stop.
Sean supplied the source-accumulation direction. Codex supplied the analytic
candidate and derivations; GEN3 executed the encoded source arithmetic,
exact log accounts, native candidate comparisons and selected witness checks.

## What enters each source admission

For a_t=mu(s+t), fixed cell weights W_I and fixed projected source columns
beta_I(t), the original-source update is exactly

    M_(t+1)=M_t+a_t,
    Z_I,t+1=Z_I,t+a_t beta_I(t),
    delta_t=a_t^2[1/s+sum_I beta_I(t)^2/W_I],
    F_t=2a_t[M_t/s+sum_I beta_I(t)Z_I,t/W_I],
    Q_(t+1)=Q_t+delta_t+F_t,
    D_(t+1)=D_t+delta_t, X_(t+1)=X_t+F_t.

Keep B_s=tau_U+earlier original-block energies fixed while this block enters.
Then A_t=B_s+Q_t, d_t=delta_t/A_t, f_t=F_t/A_t, and

    log(A_(t+1)/A_t)=log(1+d_t+f_t).

The exact saved fields are d_raw=delta_t, f_raw=F_t, d, f, D, X, Q,
A_before and A_after. SOURCE_TRACE_READABLE.csv renders every one of the
75 admissions for both geometries, including negative signed feedback and
cumulative X. CASE_s512_t75.json retains their exact rational values.
The native U/D/L/V log accounts retain exact rational log arguments and
verify U-D=L and U+D=V. Rise/fall logs are diagnostic; no positive part is
taken per admission. The original criterion applies [X_T]_+ after each
complete signed block accumulation and then sums the original roster.

## Completed cycle: candidate to evidence to selection to outcome

1. **Candidate inequality.** Define
   L_t=(delta_t+F_t)^2/[2 A_t max(A_t,A_(t+1))] and
   Phi_T=sum_(t<T)f_t-sum_(t<T)L_t. The elementary logarithm remainder gives
   the derived uniform lemma log((B_s+Q_T)/B_s)<=D_T/B_s+Phi_T.
   Codex proposed the arithmetic candidate C1: Phi_T<=H_(s-1)D_T/B_s.
   The divisor/harmonic substitution and original-target implication are
   explicit in DERIVATION.md; the additional step is the signed arithmetic
   estimate A3 there.

2. **Relevant retained evidence.** With original U2047 and tau=12225/1024,
   GEN3 reused the saved s512,t75 path and original earlier blocks. C1 has
   zero violations in 75 full and 75 projected prefix checks. At t75 the
   projected Phi is 0.027580317 versus RHS 0.123685688. Its signed X is
   +0.373850983; Qhat is 0.613543636 and D_adm is 0.239692653.
   Projected rise/fall/net logs are about 0.120540119 / 0.075127801 /
   0.045412318. Full logs are about 0.118260777 / 0.073503882 /
   0.044756894. These are finite source-path observations. They show how
   successive feedback cancels and accumulates, beyond an endpoint score.

3. **Native next-investigation selection.** GEN3 compared exact
   Phi_t/(H D_t/B_s) over the 73 saved projected prefixes with nonzero
   denominator. The unique maximum is s512,t43, about 0.361531581.
   SOURCE_HISTORY_SELECTION.json retains the input history, all ties and
   native certificate. No novelty input or forced winner change was used.
   Codex mapped that selected prefix into the retained fourth-root/cofactor
   question: does this original-growth admission also grow transport R?

4. **Executed outcome.** At t43 the admitted n554=2*277, A=6, has smooth
   cofactor k=2<A and rough mu(277)=-1. The general retained identity gives
   R(n)=mu(k)[1+mu(m)]=0. Native projections at stops42 and43 give

       Delta Qhat(mu) = +0.09367983349,
       Delta Qhat(a2) = +0.00446684680,
       Delta Cross   = -0.09814668030,
       Delta Qhat(R) = 0 exactly.

   Both the polarization conservation difference and the original admission
   law difference are exactly zero in CYCLE_RESULT.json. The greatest
   observed C1 demand therefore occurs at a zero transport admission.
   That explains why source-history relevance and fourth-root growth
   relevance must be recorded separately.

5. **Updated obligation and proposed next question.** Codex used the
   all-scale cofactor identity to derive the support lemma in
   TRANSPORT_SUPPORT_LEMMA.md: zero R admissions leave all fixed projected
   coordinates unchanged. Hence max_t Qhat(R)=max over its surviving-support
   stops. The neighboring surviving stops are42 and44;44 is the next proposed
   investigation. The open sufficient fourth-root inequality is
   max_surviving Qhat(R)<=C_epsilon s^epsilon E_u4, with the actual smaller
   source and the documented valid recursive transfer. No D_adm<2 claim is
   transferred to the non-unit R coefficients. That inequality remains open.
   The owner stopped RUN2 before any follow-on44 investigation or main-run
   controller integration. The next lead is proposed, not executed or consumed.

This is one complete native evidence/selection/check cycle. The main RUN2
selector remained unchanged and did not consume its new history evidence.
SELECTION_AUDIT.md names the exact main-run fields and code path. Its
RH_SEARCH_* two-point accounts are distinct from the RH_SOURCE_* admission
accounts used here. Native GEN3 selected a witness under the encoded rule;
it is not attributed with independently inventing Codex's analytic rule.

## Dependency and claim map

| Bound | RHS dependency | Current status / additional step |
|---|---|---|
| L1: log((B+Q)/B)<=D/B+Phi | Same-scale Phi unresolved; D controlled | Derived uniform lemma; needs a bound for signed Phi |
| C1: Phi<=H D/B | Controlled diagonal/geometry; B eliminated in consequence | Proposed arithmetic inequality; 150 finite prefix checks pass; uniform A3 open |
| L2: Q<=2(1+H)exp(2(1+H)/tau_U) | Controlled geometric quantities | Derived conditional uniform lemma assuming C1; original roster then gives subpower growth |
| Support identity S1 | Exact zero coefficients in retained source | Derived uniform lemma; max transport energy can be restricted to surviving stops |
| Qhat(mu)<=2 Qhat(R)+2 L_s | Same-scale R unresolved; quadratic L_s controlled | Derived uniform transfer; needs transport growth control |
| F17/S3: Qhat(R)<=C_epsilon s^epsilon E_u4 | Smaller-scale quantity with valid recursive transfer | Uniform source gain open; support identity removes redundant stops only |
| Six RUN2 envelope expressions | Constant/geometry/diagonal controlled, or same-scale mean/active energy unresolved | Finite envelopes only; uniform coefficient estimate needed, plus control of any unresolved RHS factor |

CANDIDATE_BOUND_DEPENDENCIES.json gives the six separate finite-expression
tags. Neither finite coefficients nor finite C1 pass counts establish the
uniform arithmetic estimate. The current result language for the completed
source-history test is: **The test result suggests strong contact with the
concept.** The test's scope is exact accumulation, candidate-path contact and
arithmetic support structure. Uniform signed growth and RH remain open.

## Custody and partial work

The session is PROJECT_DOMAIN_SESSIONS1/sessions/
RH_f35d5194e67a48009e5441d4ec4259db. Native signed graphs, log readouts and
managed receipts are retained alongside run.py and followup.py. Python CSV
and decimal summaries are renderings of saved native values, not new native
executions. The later s1024,t150 path retains its admission graph and full
compensator/log; its projected compensator was interrupted and has no
completed result. s1024,t395 was not executed. BOUNDED_STOP.json preserves
that boundary. No broad census was launched to populate these readouts.
