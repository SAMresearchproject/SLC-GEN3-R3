# Subpower investigation: scale8192 and the equal-admission mechanism

14 September 2026. Owner requests the subpower excess bound using existing
SAM theory and work, with a20-minute window to obtain updated pod material.
Codex supplies the transfer-threshold and source-run deductions; GEN3 supplies
the exact larger-scale scan and focused source values. Sean Brady is originator
and conceptual director; OpenAI ChatGPT and Codex are AI research collaborators.

**Current mathematical status:** the uniform subpower excess bound remains
OPEN. The new threshold theorem gives a weaker sufficient source inequality;
the actual-source validity of that inequality remains to be derived. The
new finite scan and the source-run identity below are completed results.

## 1. New analytic opening within the existing divisor route

`SUBPOWER_EXCESS_TRANSFER_THRESHOLD_R1.md` derives that the original complete
signed divisor estimate need not be linear in its actual smaller-source
energy U_s. A bound

    |L_s,t(f)|^2 <= C(1+log_2 s)^A U_s^(p_s) R_s(f)

would suffice even for p_s=2-kappa/log(e+log_2 s),0<kappa<=1. For every
0<c<kappa/(2log2), it yields the explicit conditional envelope

    E(s,t) <= C_0 exp[C_1 log(2s)/(log log(e^e+2s))^c].

That is subpower in s. The threshold theorem retains the original norm,
complete signed sum, actual input energy and spectral tail. Exactly quadratic
transfer alone permits polynomial growth in this recurrence. The strict
actual-source saving, even this vanishing one, is the open arithmetic step.

## 2. Complete next-scale native result

GEN3 executes RH_DYADIC_COUPLED_FORCING_SCAN_R1 at8192 through the existing
NativeDomainSession and qualified adapter. Every stop0..8192 is retained.

| Quantity | Result |
|---|---:|
|Maximum E|0.5204391374536774|
|Unique maximum stop|7798|
|E>1 failures|0|
|E>1/2 failures|8|
|E>1/4 failures|364|
|Maximum full Q|1.013888925875524 at1670|
|Maximum original positive X|0.6784243131715275 at1670|
|Minimum A|-0.07765367044788665 at1103|
|Prefixes with negative A|305|

The eight half-constant failures are7786,7794,7795,7796,7797,7798,7802,7803.
The earlier pilot plus this scan gives12,836 distinct complete-prefix cases
at32,512,4096,8192. C=1 survives this combined scope. For that finite
constant-candidate experiment: **The test result suggests the concept is
possible.** For C=1/2: **The test falsifies the concept.** Neither classification
supplies the unbounded source estimate.

At the new peak, the exact signed components give

    Q_a =0.5698467487748793,
    Q_b =0.7545851130012085,
    <a,b>=-0.4280699553405129,
    A=0.8053625118411172,
    E=0.5204391374536774,
    R=0.000005229229539372118,
    Q_fine=1.090291115458096.

Mean forcing is0.50018310546875 and cut forcing0.3051794063723671.
The full-Q and positive-X maximizer1670 instead has E=-0.21663446490338703.
The same excess target continues to distinguish demanding forcing from a
large inherited source energy.

## 3. Actual source at the peak and the next admission

Two focused native calls at7797 and7799, combined with the native peak7798,
retain the actual admitted source values and exact energy differences.

| Stop | Parent n | alpha=mu(n) | Odd child | gamma | beta |
|---|---:|---:|---:|---:|---:|
|7798|15989|1|31979|1|1|
|7799|15990|-1|31981|-1|-2|

At7798 the excess increment is+0.015459533094160554, comprising

    forcing self  +0.013340218658046249,
    forcing cross -0.005610452110965972,
    inherited     +0.007729766547080277.

The net forcing increment and inherited increment are equal. This has an
exact source explanation: alpha=beta, hence delta v=beta-alpha=0. The
complete transported vector is unchanged, and E=Q_s(v)/2-Q_s(a) gives

    delta E = -delta Q_a,
    delta A = -delta Q_a/2.                                      (1)

The admission at the peak therefore increases excess through falling parent
energy while adding zero to v. Individual fine coefficients are not zero:
the fine pair is(-1,+1). Its pair detail and R remain explicitly retained.

At7799 delta v=-1. Its excess increment is-0.036338447235953475:
forcing self-0.02630182712540913, forcing cross-0.002307442219461373 and
inherited-0.007729177891082969. The resulting E is0.484100690217724.
All three signed contributions reinforce this immediate decrease.

## 4. An exact bound through an arbitrarily long equal-admission run

For any consecutive source interval of admissions with beta=alpha, v is
constant throughout. If a_start is the inherited vector at the interval's
entrance, then at EVERY later stop within that interval,

    E(t)-E(start) = Q_s(a_start)-Q_s(a_t) <= Q_s(a_start).         (2)

This follows from nonnegativity of the full parent energy, with no absolute
increment sum, monotonicity requirement or eventual repayment assumption.
The bound is independent of the number of admissions in the run. It gives
conditional source-structure control for this specific arithmetic family.
The condition is equality of the actual admitted parent/forcing values;
it is not inferred from their signs after observing a future maximum.

At the7797 entrance to the observed neutral step, Q_v/2 is
1.0902858862285567 approximately. That is the run's resulting upper ceiling
on E, so this particular bound alone does not certify C=1 through arbitrary
further neutral admissions. Non-neutral admissions can change Q_v and remain
part of the unbounded arithmetic problem. The actual next step here is
non-neutral and compensating, as recorded above.

For the exact source-transition and equal-admission control experiment:
**The test result suggests strong contact with the concept.** Scope: the
observed native transition and the derived conditional source-run identity.

## 5. Preserve the surrounding signed interval

The native complete-prefix curve supplies the interval7734..7862, retained
in SIGNED_WINDOW.json with every delta E, delta A and inherited increment.
The entrance E is0.38765261502885784. Its rise to7798 consists of forcing
+0.15378048339938882 and inherited contribution-0.020993960974569195.
The immediate peak admission's inherited mechanism and the complete interval's
forcing-led buildup are therefore both retained at their proper scopes.

The first subsequent return to the7734 baseline occurs at7815,17 admissions
after the peak. Actual signed drift after4/8/32/64 admissions is respectively
-0.01041859596752819,-0.04862452846778227,-0.24261542032242775,
-0.2752538439557827. The maximum rise above the peak over each horizon is0.
These are realized outcomes, separate from the conditional estimate(2).

## 6. Verification, provenance and download contents

The full scan takes186.531558 native CPU seconds,186.927423 elapsed seconds,
with peak RSS763548KiB. Its three selected deep witnesses pass73,749 native
internal checks and21 independent Fraction checks. The two focused readouts
add49,166 native checks and16 independent checks. Four further exact checks
verify(1) at the peak;128 signed interval recombinations pass.

Totals for this extension are122,915 native internal witness checks and169
independent checks, alongside the native full-prefix recurrence/readout checks.
The previous closure's48,340/356 checks remain separate.

All8192 scan points are fixed complete-scale exploration. The two subsequent
questions are refinement of its newly found maximum, not model-selected
discoveries. No new result in this extension enters fitting;4096 remains
held out. Existing production, selector, budgets and cancelled stop policies
are unchanged. No new daemon or restart is introduced.

Artifacts: results/subpower_excess_extension_r1/ contains the compressed full
curve, scan completion, source-conditioned focus, signed window and native
session receipts. tools/subpower_excess_extension_r1.py and
tools/subpower_peak_source_r1.py reproduce the native calls; their source
binding and execution receipts identify the arithmetic engine.

The focused download packet includes this result, both theoretical notes,
prior source-history work, native records and implementation sources. It is
copied to persistent pod storage, then downloaded by authenticated HTTPS and
checked against its compressed hash and every payload hash. The separate
download receipt records the actual completed transfer. Existing full engine
recovery remains with the previously verified base and targeted delta.
