# Current-source control of forcing-excess overshoot and drift

14 September 2026. Sean Brady requests a source-conditioned explanation and
future control at the peak1071, recrossing1077 and recovery1130, comparison
with other demanding/held-out windows, and selection accounting by native
cost and mathematical outcome. The target remains E=A-Q_a/2. No monotonicity
condition or new representation is introduced.

Codex supplies the bounded rule grammar, causal support-certificate derivation,
native implementation and outcome accounting. GEN3 performs calibration,
frozen evaluation and exact support-branch enumeration through actual
NativeDomainSession calls, with the current SLC/CE/RH binding and saved pod.

## The distinction tested

Two different objects are retained:

1. A finite calibrated hypothesis: a current source-sign/pairing-sign signature
   predicts an upper remaining overshoot and a terminal signed-drift interval.
2. An exact conditional finite-horizon certificate: the current full weighted
   state bounds every continuation satisfying known squarefree support,
   without knowing the next nonzero Möbius signs.

The first is tested against unseen-by-fitting suffixes. The second is a
finite algebraic bound for all allowed sign continuations at the specified
current state. Realized future values are used only AFTER constructing that
certificate, for comparison. Neither object assumes compensation.

## Frozen current-state rule

The signature consists of the last admitted alpha,beta, signs of the NEXT
kernel pairings Ka,Kb computed from the current prefix, sign of the last
signed increment, and parity of the last original index. All are available
at the forecast stop. No future peak, repayment time or interval extremum
is a signature feature.

Calibration uses scale512 stops1..192 and labels only through256. At horizons
8,32,64, GEN3 stores each signature's calibration maximum overshoot and
minimum/maximum terminal drift. This produces70 groups. The model and source
contract are frozen by SHA256 BEFORE evaluation. Unmatched signatures remain
uncovered rather than receiving a silently fitted fallback.

Evaluation covers later512 stops beginning257, the separate2048 source scale,
and held-out4096. The known4096 stress history remains exploratory held-out
evaluation, not a newly untouched test. No2048 forcing outcomes or4096 data
enter the calibration. Right-censored horizons near a source endpoint are
reported explicitly rather than counted as completed horizons.

Eight-admission results:

| Evaluation | Matched states | Unmatched | Overshoot-bound failures | Drift-interval failures |
|---|---:|---:|---:|---:|
|Later512|213|35|61|119|
|2048|1723|317|247|838|
|4096|3246|842|505|1630|

The32/64-admission failures and exact first counterexamples are also retained.
For this frozen calibrated-signature bound: **The test falsifies the concept.**
This rules out the declared fitted bounds, not every possible source-conditioned
rule. Recognizing a sign pattern and assigning its previous maximum is not
the future control supplied by the second calculation.

## Current-state support certificate

At current stop t, retain the actual prefix state and the original full
kernel. For each of the next at most four admissions, the future parent
alpha and odd-child gamma are zero at squareful indices and belong to
{-1,+1} at squarefree indices. Set beta=alpha+gamma at even parent indices,
and beta=gamma at odd ones. GEN3 enumerates all these possibilities, updates
the signed prefix state along each path, and retains the largest attained
excess plus minimum/maximum terminal drift.

The algorithm has no input for future Möbius signs. Squarefree support is
computed from the known future integer indices. Dependencies between future
nonzero signs are relaxed, so every actual continuation is included. No sum
of clipped or absolute admission increments is substituted for a path.

The validity follows by induction over the finite branch tree: every actual
next source pair lies in an enumerated branch, and each branch uses the exact
original signed energy update. Its path maximum bounds the actual path and
its terminal extrema bound the signed terminal contribution. This provides
conditional future control at the specified prefix, independent of whether
the actual future repays or reinforces.

| Current stop | Current E | Upper E over next4 | Terminal drift interval | Support branches |
|---:|---:|---:|---|---:|
|1071|0.514400059|0.589424759|[-0.069410267,+0.075024700]|32|
|1077|0.493799231|0.600499614|[-0.096696737,+0.106700383]|64|
|1130|0.261231122|0.343086070|[-0.072035796,+0.081854948]|64|

All three certify the retained C=1 ceiling over this short horizon. At1130,
the current state also certifies staying below1/2 for the next four admissions.
At1077, crossing below1/2 does not itself yield that stronger short-horizon
certificate: its allowed upper value is0.600500. The certificate preserves
both positive and negative possible terminal drift.

The corresponding signatures recur at188,183,62 OTHER4096 positions. The
current weighted state at every one of these matching positions certifies
C=1 for its next up-to-four admissions. A separate bound is computed from
each position's actual magnitudes; a common signature-level constant is not
inferred. Held-out227,790,4094,4095 also receive certificates. The last two
have only two and one remaining admissions, explicitly recorded.

For the conditional short-horizon source-control experiment:
**The test result suggests strong contact with the concept.**
The unresolved extension is a source-state condition that sustains this
control through continuing admissions, or another bound on the remaining
signed drift. This four-admission result does not assign a uniform continuing
bound or guarantee repayment at an unknown future time.

## Source values and actual later drift

All three requested transitions have alpha=0:

| Stop | Original index | Odd-child index | gamma=beta | Forcing self increment | Forcing cross increment | Inherited increment |
|---:|---:|---:|---:|---:|---:|---:|
|1071|5166|10333|-1|+0.015106019|+0.005540578|0|
|1077|5172|10345|+1|-0.015052039|-0.005517461|0|
|1130|5225|10451|+1|-0.009114467|-0.006492834|0|

The current weighted pairings distinguish the size of these effects. The
zero parent admission reduces the exact update to
Delta E=beta(q-p)+beta²k/2. At1077 and1130 the positive odd-child sign makes
both recorded forcing contributions negative; the inherited term is zero.
This explains those admitted reversals from their source and prefix pairings.
It does not assume the sign of a later odd child; that uncertainty is retained
in the support certificate. The
peak and recrossing have no actual overshoot over their following64 admissions.
At1130 the actual next4 overshoot is+0.015559570; the next8 overshoot is
+0.055816795, with terminal drift+0.035313506. By32 admissions the net drift
is+0.080582156; by64 it is-0.058236476. Recovery therefore does not make the
remaining excess monotone. These realized outcomes are kept separate from
the forecast and certificate inputs.

## Codex closed one-admission consequence

The branch rule also has a direct local expression. Write p=(Ka)_j,
q=(Kb)_j and k=K_jj at the next index, using the current prefix. If both
parent and odd child are squarefree, maximizing the exact signed increment
over their unknown signs gives

    even parent index: max Delta E=|q-p|+2|p|-k/2,
    odd parent index:  max Delta E=max(2|p|-k, 2|q|+k).

If only the odd child is squarefree, the maximum is |q-p|+k/2.
If only the parent is squarefree, it is2|p|-k at even indices and
|p+q|-k/2 at odd indices. If both are squareful the increment is zero.

These formulas follow by substituting beta=alpha+gamma or beta=gamma into
the unchanged admission identity and maximizing its two possible signs.
They are a Codex algebraic corollary of the enumerated support rule. Magnitudes
here describe an exact maximum over unknown source signs at ONE state;
the multistep computation still preserves signed paths and updated pairings.

## Selection cost and mathematical outcomes

The frozen audit snapshot includes24 completed learned questions and two
fixed-rule questions. Native costs are the measured COMBINED derivative-plus-
forcing call costs; marginal forcing-only cost is not assigned. End-to-end
latency and native elapsed time are stored separately per question.

| Role | Questions | Native CPU seconds | Maximum sampled E | Rising then net-compensating within8 | Eight-step behavior families |
|---|---:|---:|---:|---:|---:|
|Learned refinement|24|2.059058|+0.154064432|6|7|
|Fixed exploration|2|0.134178|-0.056350317|1|2|

Neither arm improves on the known same-scale bootstrap peak0.210217371;
neither supplies a new C=1/2 or C=1 counterexample. Learned refinement reaches
more demanding sampled excesses in this snapshot and supplies detailed local
transition outcomes; the earlier neighborhood audit records the broader
selected-region expansion supplied by the fixed arm. Unequal budgets remain
visible. No equal-budget superiority claim is made.

The behavior family is an OUTCOME label: sign of current increment, sign of
realized8-admission terminal drift and whether realized overshoot is positive.
It is not a prediction feature or training input. forcing_outcome_audit.py
now attaches measured native cost, exact excess/candidate outcome, realized
signed suffix outcomes and same-scale benchmark comparison to each selection
in the existing feedback reports. Its rational calculations are identified
readouts of the preserved native full-prefix curves, not new source arithmetic.
Held-out cases remain a separate role and outside fitting.

The fixed128 focus lies in the calibration segment; its forecast row is an
in-sample outcome audit, not predictive validation. The reported later512
validation counts start at257. Seventy-eight exact audit/suffix comparisons
agree with native returned outcomes or their explicit right-censoring.

## Records and validation

results/forcing_prospective_r1/ contains the pre-evaluation CONTRACT,
SELECTIONS snapshot, frozen model/reference, native BUILD/CONFIG/session
receipts, per-scale INPUT/EVALUATION files, completion,203 independent exact
checks, and frozen/current cost/outcome audits. Evaluation native times are
0.150s,0.763s,3.806s at512/2048/4096. Exact certificate branches, source values,
failure witnesses, right-censoring and recurrence counts are preserved.
Seven existing feedback checks pass after the report hook. Producer, fitting,
selector, target, allowances, held-out boundary and stop/storage policy remain
unchanged. No new worker or service restart is introduced.
