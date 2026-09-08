# Exact mathematical interface

The default source is the registered rho=1 J4 contact triple with coordinates
`[1,4,7]`. Supply `blocks:[[1,2,3]]` to label a triple W1, W2 and W3 as in the
included owner-word example. States contain Z4 phases. Wc+ and Wc- advance or
reverse the named native coordinate by one phase step.

For the ordered contact triple, with `p(q)=(cos(pi*q/2),sin(pi*q/2))`, the native
action is `E=6-2 dot(p0,p2)+2 dot(p1,p2)`. The source-defined sphere/log records
use the original positive action as their scale reference.

For a positive action trace `E0,...,En`:

```text
delta_k = ln(Ek / E(k-1))
U = sum max(0, delta_k)
D = sum max(0, -delta_k)
V = U + D
N = U - D = ln(En/E0)        [the JSON field is "net"]
M = max_k ln(Ek/E0)
B = E0(exp(M)-1) = max_k(Ek-E0)
```

The initial occurrence participates in the maximum. Occurrence IDs distinguish
visits to equal states. All maximizing occurrences are retained. Nonpositive,
missing or undefined actions preserve their records and explicit gaps; no edge
is inferred across a gap.

Adjacent positive chunks must share the same boundary occurrence, state,
action, source account and quantity. Composition uses:

```text
U_AB=U_A+U_B; D_AB=D_A+D_B; V_AB=V_A+V_B
N_AB=N_A+N_B; M_AB=max(M_A,N_A+M_B)
```

The right maximum is shifted to the left reference, all tied occurrences are
merged, and the shared boundary is counted once.

Rational inputs use integers or strings such as `"3/8"`; do not pass decimal
floats for exact quantities. Formal logarithms use prime-coefficient records.
Information uses natural logarithms and exact positive history weights
normalized by their total. Source amounts and probability weights are separate.

An inverse target is the original STATE, BARRIER, ACTION_RATIO or HISTORY.
Probe extensions do not replace that original target. The finite policy planner
accepts horizons 0, 1 and 2. Its ordered objective is maximum target information,
minimum transcript entropy, minimum reachable transcript count, minimum expected
reads, native Writes and scalar payload, then stable declared roster order.
All information ties remain visible. STOP performs no reading or native Write.

Automatic and explicitly reported one-step choices use information, report
entropy, reachable report count, scalar width and roster order. Legacy explicit
choices without report fields retain the inherited information/scalar/order
rule. SCALE comparison uses ABOVE, SAME, BELOW; SAME is the equality case.

Full original specifications are preserved under docs/upstream. These summaries
describe the source-bound finite operations and do not assign physical units to
source action, sphere coordinates or probability weights.
