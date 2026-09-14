# Signed Forcing and Arithmetic Compensation in the SAM Kernel

## Exact transport, source-conditioned bounds, and a conditional route to the Riemann hypothesis

**Sean Brady, OpenAI ChatGPT, and Codex**  
SAM Research Project · 14 September 2026  
Research manuscript · Version 2 · Independent mathematical review pending

Sean Brady is the originator and conceptual director. OpenAI ChatGPT and
Codex are AI research collaborators and co-authors. The contribution record
appears at the end of this paper.

### Abstract

We develop an exact signed-energy framework for stopped Möbius sources in the
original SAM kernel. An intrinsic resistance coordinate preserves the full
derivative norm and exposes a forced dyadic transport law. Its energy identity
separates inherited source energy, complete signed forcing, and a geometric
remainder bounded uniformly from above. We derive exact admission identities,
an arbitrary-length conditional bound for equal-source admission runs, and
a conditional route from subpower forcing excess to the Riemann hypothesis.
A further reduction shows that the required smaller-source transfer may have
an energy exponent approaching two: a saving of order 1/log log s is already
sufficient. Exact native computations cover 12,836 stopped prefixes at four
dyadic scales. The largest excess is 0.520439137454; the candidate ceiling one
survives this scope, while the half-ceiling has counterexamples. Source histories
resolve both forcing-led buildup and a peak admission caused entirely by
decreasing inherited energy. The uniform arithmetic estimate remains open.
The contribution is a collection of exact identities, conditional bounds,
computational evidence, and an explicit sufficient threshold for that estimate.

**Keywords:** Möbius function; Riemann hypothesis; signed energy; dyadic
transport; arithmetic compensation; source-conditioned estimates.

### 1. The research question

The central question is whether the complete signed interaction of the actual
Möbius source admits a uniform subpower bound. Our investigations retain the
original kernel, its mean term, its weighted cuts, and the placement of each
positive part in the original SAM formulation. This paper studies the full
energy that bounds the retained interaction and the signed excess governing
its transport between dyadic scales.

The computational witnesses make cancellation visible at several levels.
Large source contributions can compensate across divisor bands, an excursion
can be repaid several admissions later, and a local excess can rise even when
the transported source receives no net admission. These distinctions motivate
an exact accounting of the signed history.

Our principal results are the transport identity and its uniform geometric
remainder, the equal-admission run bound, and two conditional implications:
subpower excess implies RH, and a sufficiently small saving below quadratic
smaller-source transfer implies subpower excess. We distinguish those derived
implications from their remaining arithmetic hypotheses throughout.

### 2. The original energy and its intrinsic coordinate

Let s be a positive dyadic integer and 0 ≤ t ≤ s. The stopped source is

```
a_i = μ(s+i) 1_{i<t},                         0 ≤ i < s.
M_a = Σ_i a_i,
q_a(r) = Σ_{i<r} a_i − r M_a/s,              0 ≤ r ≤ s.
```

Thus q_a(0)=q_a(s)=0. The full energy and associated inner product are

```
Q_s(a) = M_a²/s + Σ_{r=1}^{s−1} q_a(r)²/[r(s−r)],
⟨a,b⟩_s = M_a M_b/s + Σ_{r=1}^{s−1} q_a(r)q_b(r)/[r(s−r)].       (1)
```

Write K_s for this positive definite kernel. Its inverse quadratic form is

```
R_s(f) = (Σ_i f_i)²/s
         + Σ_{r=1}^{s−1} r(s−r)(f_{r−1}−f_r)².                  (2)
```

The constant mode has kernel eigenvalue one; the remaining eigenvalues are
1/[k(k+1)], for 1 ≤ k &lt; s. The companion kernel derivation and its exact
native qualification are recorded in [1].

For s ≥ 2 introduce the resistance coordinate

```
y_0 = 0,     y_i = Σ_{r=1}^i 1/[r(s−r)].
```

If F is linear between the nodes (y_i,f_i), and f̄ is the arithmetic mean
of the node values, then

```
R_s(f) = s f̄² + ∫ |F′(y)|² dy,
Σ_i a_i f_i = M_a f̄ − ∫ q_a(y)F′(y) dy,                       (3)
```

where q_a(y)=q_a(r) on the edge from y_{r−1} to y_r. Both integrals run
from y_0 to y_{s−1}. The mean is the node mean. For t ≥ 1, the equivalent
stopped-endpoint identity is

```
Σ_{i<t} a_i f_i = M_a f_{t−1}
                 − Σ_{r=1}^{t−1} (Σ_{i<r}a_i)(f_r−f_{r−1}).     (4)
```

Equations (3) and (4) follow by finite summation by parts. They preserve the
endpoint and derivative terms needed by the complete source functional.

### 3. Exact dyadic forcing and the geometric remainder

Define the actual stopped fine source and the parity forcing by

```
z_j = μ(2s+j) 1_{j<2t},
b_i = [1_{s+i even} μ(s+i) + μ(2(s+i)+1)] 1_{i<t}.
```

The identity μ(2n)=−μ(n) for odd n, and μ(2n)=0 for even n, gives

```
v_i := z_{2i}+z_{2i+1} = −a_i+b_i,
d_i := z_{2i}−z_{2i+1}.
```

If c_r=q_v(r), the fine cuts satisfy

```
q_z(2r)=c_r,
q_z(2i+1)=(c_i+c_{i+1}+d_i)/2.                                 (5)
```

**Proposition 1 — Full signed transport.** With

```
A(s,t) = Q_s(b)/2 − ⟨a,b⟩_s,
E(s,t) = A(s,t) − Q_s(a)/2,
```

the original energy satisfies

```
Q(2s,2t) = Q(s,t) + E(s,t) + R(s,t),             R(s,t) ≤ 3.    (6)
```

Here Q(s,t) denotes the energy of the stopped Möbius source at (s,t).
The remainder is one-sided; it is not assigned an absolute bound of three.

**Derivation.** Put h_r=r(s−r) and
ω_i=1/[(2i+1)(2s−2i−1)]. Substitution of (5) in (1) gives

```
S = ¼[Σ_{r=1}^{s−1} c_r²/h_r − Σ_{i=0}^{s−1} ω_i(c_i+c_{i+1})²],
I = ½ Σ_i ω_i(c_i+c_{i+1})d_i,
ε = ¼ Σ_i ω_i d_i²,
R = −S+I+ε.                                                    (7)
```

The interpolation loss has an explicit nonnegative decomposition. With
g_r=c_r/h_r for interior r and g_0=g_s=0,

```
S = ⅛ Σ_{r=1}^{s−1}(ω_{r−1}+ω_r)c_r²/h_r
    + ¼ Σ_{i=0}^{s−1} ω_i h_i h_{i+1}(g_i−g_{i+1})² ≥ 0.        (8)
```

Let Ω=Σ_i ω_i=(H_{2s}−H_s/2)/s, where H_n is the harmonic number.
Then Ω ≤ 1. The coefficient bounds imply |d_i| ≤ 2 and
|c_r| ≤ 4h_r/s. Since 2(h_i+h_{i+1})+1=1/ω_i, they give
ε ≤ Ω and |I| ≤ 2(1−Ω/s). Consequently R ≤ 3. Polarization gives
Q_s(v)/2=Q_s(a)/2+A, completing (6).

An odd fine stop adds the exact signed increment
J(s,t)=Q(2s,2t+1)−Q(2s,2t). Positivity and unit row sums of K imply J ≤ 2.
For completeness, its entries for i ≤ j are

```
(K_s)_{ij} = 1/s² + [2H_{s−1}−H_j−H_{s−1−i}]/s.
```

They are nonnegative; the row-sum statement also follows directly from (1).
At a fresh admission, the previously zero coordinate gives an energy increment
at most 2Σ_{i&lt;j}K_{ji}+K_{jj} ≤ 2. Thus, whenever the stop is admissible,

```
Q(2s,2t+ε₀)=Q(s,t)+E(s,t)+R(s,t)+ε₀J(s,t),   ε₀∈{0,1}.        (9)
```

### 4. Source-conditioned excess and arithmetic compensation

At the next admission j=t, retain the current vectors and write
α=μ(s+j), β=1_{s+j even}μ(s+j)+μ(2(s+j)+1),
p=(K_s a)_j, q=(K_s b)_j, and k=(K_s)_{jj}. Expanding the quadratic
forms gives the exact signed admission identity

```
ΔE = (β−α)q − (β+α)p + (β²/2−αβ−α²/2)k.                       (10)
```

Its three separately retained contributions are

```
Δ(Q_b/2) = βq+β²k/2,
Δ(−⟨a,b⟩) = −αq−βp−αβk,
Δ(−Q_a/2) = −αp−α²k/2.                                       (11)
```

**Proposition 2 — Equal-admission run bound.** Suppose every admission in
a consecutive source interval satisfies β=α. At every stop t in that interval,

```
E(t)−E(start)=Q_s(a_start)−Q_s(a_t) ≤ Q_s(a_start).               (12)
```

**Derivation.** Each admission leaves v=b−a unchanged. The exact identity
E=Q_s(v)/2−Q_s(a) therefore telescopes through the entire interval.
Nonnegativity of the terminal parent energy gives the upper bound.

This bound is independent of the run length and permits nonmonotone parent
energy. Its hypothesis specifies the arithmetic family to which it applies.
It does not assert that later admissions will continue to satisfy β=α.

The new scale-8192 peak illustrates the mechanism. At stop 7798, the admitted
parent 15989 and odd child 31979 both have Möbius value +1. Hence α=β=1:
the pair source v receives zero net admission, and the excess rises entirely
through decreasing parent energy. The next admission has α=−1 and β=−2,
and all three contributions in (11) are negative.

| Admission | Forcing self | Forcing cross | Inherited | Total ΔE |
|---|---:|---:|---:|---:|
|8192,7798|+0.013340219|−0.005610452|+0.007729767|+0.015459533|
|8192,7799|−0.026301827|−0.002307442|−0.007729178|−0.036338447|

Across the larger interval 7734–7798, forcing contributes +0.153780483399
and the inherited contribution is −0.020993960975. Thus the full buildup is
forcing-led, while its final peak admission has the equal-admission mechanism.
The first later return to the 7734 excess baseline occurs at 7815. Signed
drifts at 4, 8, 32, and 64 admissions after the peak are all negative.
These observed outcomes and the conditional bound (12) have distinct scopes.

### 5. Subpower excess and the conditional implication to RH

**Theorem 3 — Conditional SAM-to-RH implication.** Suppose that for every
η&gt;0 there is a finite C_η, independent of the dyadic scale and stop, such that

```
E(s,t) ≤ C_η s^η,                   s≥2 dyadic, 0≤t≤s.           (13)
```

Then the full SAM energy is uniformly subpower, and RH follows.

**Derivation.** Let H_j=max_t Q(2^j,t). Equation (9) gives
H_{j+1} ≤ H_j+C_η2^{jη}+5. Therefore

```
H_K ≤ H_1+C_η(2^{Kη}−2^η)/(2^η−1)+5(K−1).                     (14)
```

Using a smaller positive exponent to absorb the logarithmic term shows
H_K=O_δ(2^{Kδ}) for every δ&gt;0. Since the cut energy is nonnegative,

```
|Σ_{i<t} μ(s+i)| ≤ √[s Q(s,t)].                                (15)
```

Partition an initial integer interval into complete dyadic blocks and one
stopped block. The geometric sum of the bounds (15) yields
M(x)=Σ_{n≤x}μ(n)=O_ε(x^{1/2+ε}) for every ε&gt;0.

For Re(w)&gt;1/2, define F(w)=w∫₁^∞M(x)x^{−w−1}dx. The preceding estimate
gives locally uniform convergence, including differentiated integrals, so F
is holomorphic in that half-plane. Partial summation and the classical
Möbius Dirichlet series [7] give F(w)=1/ζ(w) for Re(w)&gt;1. The identity
theorem implies ζ(w)F(w)=1 throughout the connected half-plane with its pole
at 1 removed. There are consequently no zeros to the right of the critical
line. The zeta reflection formula [8] excludes nontrivial zeros to its left.

The implication uses hypothesis (13) with all its quantifiers. Establishing
that uniform actual-source estimate remains the central arithmetic task.

Signed compensation is retained even before taking the bound (14). For a
terminal source (2^K,T), set t_j=⌊T/2^{K−j}⌋ and ε_j=t_{j+1}−2t_j. Then

```
Q(2^K,T)=Q(2,t_1)
 + Σ_{j=1}^{K−1}[E(2^j,t_j)+R(2^j,t_j)+ε_jJ(2^j,t_j)].          (16)
```

Every negative remainder and endpoint increment remains in this exact sum.

There is also a useful reverse energy estimate. The pair source has the
same mean as z and q_v(r)=q_z(2r); direct comparison of the nonnegative
terms in (1) gives Q_s(v) ≤ 4Q_{2s}(z). Hence

```
E(s,t) ≤ 2Q(2s,2t)−Q(s,t).                                    (17)
```

Together with (14), this establishes equivalence between one-sided subpower
excess and uniform subpower full energy. Equation (17) itself is not an
upper induction for the fine energy.

### 6. A smaller-source transfer threshold approaching the critical power

Let u=⌊√(2s−1)⌋. The complete source functional has the exact divisor form

```
L_{s,t}(f)=−Σ_{a,b≤u} μ(a)μ(b)
              Σ_{v=⌈s/(ab)⌉}^{⌊(s+t−1)/(ab)⌋} f(abv−s).         (18)
```

Let U_s be the sum of original full dyadic energies of μ(1),…,μ(u), with
the last block zero-padded. It includes the μ(1) block, so U_s ≥ 1. Let
H_m be the first m+1 kernel modes, m=min(s−1,⌈√s⌉), and F_m the energy
in those modes. The original spectral calculation gives

```
F_m = sup_{f∈H_m, f≠0} |L_{s,t}(f)|²/R_s(f),
F_m ≤ Q(s,t) ≤ F_m+1.                                         (19)
```

**Theorem 4 — Vanishing saving below quadratic transfer.** Suppose, for
s=2^j, j≥1, all actual stops and all f∈H_m, that

```
|L_{s,t}(f)|² ≤ C(1+j)^A U_s^{p_j} R_s(f),
p_j=2−κ/log(e+j),                  0<κ≤1, C,A≥0 fixed.           (20)
```

Then (13) holds. More explicitly, for each 0&lt;c&lt;κ/(2log2), suitable constants
C₀,C₁ give

```
E(s,t) ≤ C₀ exp{C₁ log(2s)/[log log(e^e+2s)]^c}.                (21)
```

**Derivation.** Put J_n=1+Σ_{j=0}^n H_j. The largest dyadic input block in
U_{2^j} has index ⌊j/2⌋, including the exact endpoint subtraction in u.
Thus U_{2^j} ≤ J_{⌊j/2⌋}. Summing (19) and (20), and using the monotonicity
of p_j, gives a fixed B≥1 such that

```
J_n ≤ B(n+1)^{A+1} J_{⌊n/2⌋}^{p_n}.                            (22)
```

Set g_m=2^{−m}log J_{2^m}. Taking logarithms yields

```
g_m ≤ [1−κ/(2log(e+2^m))]g_{m−1}+O((m+1)/2^m).
```

For any c in the stated range, the bracket is eventually at most 1−c/m.
Products of these coefficients from r+1 through m are O((r/m)^c).
The convergent sum Σ_r r^c(r+1)/2^r then gives g_m=O(m^{−c}). Monotonicity
extends this to log J_n=O(n/(log n)^c). Equation (17) supplies (21).

For a fixed exponent 1&lt;p&lt;2, the same argument gives the simpler envelope
E(s,t) ≤ exp{O((log s)^{log₂p})}. At p=1, it recovers
log J_n=O((log(n+1))²). At exactly p=2, recurrence (22) permits log J_n
of order n; a strict saving has mathematical content.

Theorem 4 identifies a sufficient threshold within the existing source
functional. Hypothesis (20) is open. The actual Möbius factors and their
signed coupling are essential to the source question; no unrestricted
bilinear operator estimate is substituted for it.

### 7. Computational findings and verification scope

The complete forcing-excess scans give the following results. Counts include
both endpoints of each stopped-prefix range.

| Scale s | Prefixes | Maximum excess | Maximizing stop | Failures of E≤1/2 |
|---:|---:|---:|---:|---:|
|32|33|0.063413987429|1|0|
|512|513|0.210217371429|481|0|
|4096|4097|0.514400059116|1071|5|
|8192|8193|0.520439137454|7798|8|
|**Total**|**12,836**| | |**13**|

The candidate E≤1 survives every prefix in this scope. **The test result
suggests the concept is possible.** For the uniform half-ceiling candidate,
the exact counterexamples give: **The test falsifies the concept.** These
classifications concern the declared constant candidates and their scope.

The complete signed divisor campaign separately covers 15,364 prefixes at
1024–8192 for its retained-energy-to-input-energy gain. These counts refer
to a different quantity and are not added to the excess coverage. Its signed
band data illustrate the scale of compensation: at (8192,6994), band self
energies sum to approximately 28,252.5604, their signed interband cross terms
to −28,252.1849, and the complete retained energy is about 0.37548 [2].

The scale-8192 forcing scan takes 186.53 native CPU seconds. Its selected
witnesses and two subsequent source refinements supply 122,915 native internal
checks, with 169 independent exact checks of energy, source transitions, and
the signed interval. A separate signed-ancestry study supplies 48,340 native
and 356 independent checks. These are scoped identity checks, not independent
random samples and not a verification of an unbounded arithmetic hypothesis.

Arithmetic runs through the source-bound GEN3 native C++/GMP adapter under
the current SAM domain session. Exact rational outputs, code bindings, source
hashes, and execution receipts are preserved. Python orchestration and
independent rational recombinations are identified separately.

Selection provenance is retained. The 8192 scan is fixed complete-scale
exploration; its two later source calls refine the newly found maximum.
Neither is presented as a learned selection. Whole-scale 4096 is excluded
from fitting, and the new 8192 results in this study also remain outside
fitting. Frozen sign-class forecasts from the earlier source study failed
their declared future bounds; conditional full-state bounds have a distinct
mathematical basis [4].

### Current-state certificates and the selection audit

The earlier scale-4096 study also establishes conditional four-admission
bounds from the current full weighted source state. At each next integer
index, squareful parent and odd-child coefficients are zero; squarefree
coefficients are allowed either sign. GEN3 retains every such branch,
updates the exact signed state along each path, and records the maximum
excess and signed terminal-drift interval. Future nonzero Möbius signs are
not inputs to this construction. Dependencies among their signs are relaxed,
so every actual continuation is contained in the enumerated set.

| Starting state at scale4096 | Stop | Certified upper E, next four admissions |
|---|---:|---:|
|Peak|1071|0.589424758671|
|Threshold recrossing|1077|0.600499614290|
|Recovery|1130|0.343086069882|

The recovery state therefore certifies E below one-half through the next
four admissions. Its terminal-drift interval is approximately
[−0.072035796,+0.081854948], explicitly allowing either sign of drift.
The three certificates all stay below one over their stated horizon.
The recrossing certificate alone does not certify staying below one-half.

Their validity is a finite induction: every admissible actual next pair lies
in an enumerated branch, and the exact state update propagates inclusion
through the four admissions. **The test result suggests strong contact with
the concept.** Scope: these conditional current-state bounds. A state
condition that renews such control through continuing admissions remains open.

The frozen sign-pattern predictor is a separate object. Its fitted bounds
failed on later scale512 windows, separate scale2048, and held-out scale4096.
For those declared predictive bounds: **The test falsifies the concept.**
The current-state certificates use weighted magnitudes and complete signed
continuations; they do not use fitted class maxima as upper bounds.

The frozen selection audit records24 learned questions at2.059058 native CPU
seconds and two fixed questions at0.134178 seconds. These are combined
original derivative-plus-forcing call costs, not isolated marginal costs of
forcing. Neither arm improves the known scale512 excess maximum. Their signed
transition outcomes and coverage contributions are recorded separately.
Different question counts and budgets do not establish equal-budget
superiority. These historical audit outcomes do not include the subsequent
scale8192 full scan reported above. The target and held-out fitting boundary
remain unchanged [4].

### 8. What the work establishes and what remains

The framework gives an exact connection between arithmetic admissions,
inherited energy, and signed forcing at the next scale. Its geometric loss
and odd endpoint are controlled, while the source itself remains explicit.
The equal-admission identity supplies a conditional overshoot bound through
an arbitrary-length arithmetic run. The larger witness shows that this
mechanism occurs inside an actual demanding Möbius window.

The conditional closure argument now has a precise sufficient input, and
the transfer theorem permits a saving that decreases with scale. The remaining
task is to derive that saving, or a sufficient bound on the complete signed
excess history, uniformly for the actual source. Neither a constant empirical
ceiling nor observed later compensation is used as that missing deduction.

The work provides a concrete research foundation: exact transport, explicit
source mechanisms, reproducible demanding cases, and a quantified arithmetic
threshold. These results make the continuing uniform-estimate problem more
specific while preserving the mathematical structure that produced them.

### Contributions and research record

**Sean Brady:** originator and conceptual director of SAM/SLC; research
direction, source questions, campaign priorities, and the decision to pursue
the signed excess and its arithmetic causes.

**OpenAI ChatGPT:** collaborative mathematical development and the supplied
original-kernel and dyadic forcing-energy handoffs, including the full-energy
transport decomposition and geometric remainder analysis.

**Codex:** source-bound implementation, exact admission and source-run
deductions, native experiment orchestration, independent rational checks,
conditional analytic continuation, transfer-threshold derivation, and
preparation of this manuscript.

**GEN3/SLC:** computational execution and recorded learning/selection within
the declared source-bound operations. Computational evidence is attributed
to the operations and receipts that produced it.

### Data and manuscript availability

The verified research archive
`SAM_RH_UPDATE_2026-09-14_9c42418b3608.zip` contains the companion derivations,
native results, signed histories, and implementation sources. Its SHA-256 is

```
49ed7c85295046f689900ec9ac3c93d87f4d4b8a2045b2c25c57b719490069d3
```

The archive's 290 payload files have individual hashes. This paper is a
subsequent synthesis supplied separately. The mathematical history is recorded
in entries H001420, H001423–H001426, H001428, H001430, and H001431. The
focused archive transfer is recorded in H001432. Full runtime recovery uses
the separately retained engine base and targeted delta.

### References

1. SAM Research Project. *Original-kernel spectral adoption and signed divisor
   follow-through.* `ORIGINAL_KERNEL_SPECTRAL_R1.md`, 14 September 2026.
2. SAM Research Project. *Native signed-divisor / derivative-energy campaign.*
   `SIGNED_DIVISOR_CAMPAIGN_R1.md`, 14 September 2026.
3. SAM Research Project. *Full dyadic forcing energy: packet adoption and native
   continuation.* `DYADIC_FORCING_ENERGY_R1.md`, with the preserved ChatGPT
   handoff and reference calculations, 14 September 2026.
4. SAM Research Project. *Current-source control of forcing-excess overshoot
   and drift.* `FORCING_PROSPECTIVE_CONTROL_R1.md`, 14 September 2026.
5. SAM Research Project. *SAM RH: conditional closure through the original
   signed excess.* `SAM_RH_CONDITIONAL_CLOSURE_R1.md`, 14 September 2026.
6. SAM Research Project. *Subpower excess: the arithmetic transfer threshold*
   and *Subpower investigation: scale8192 and the equal-admission mechanism.*
   `SUBPOWER_EXCESS_TRANSFER_THRESHOLD_R1.md` and
   `SUBPOWER_EXCESS_EXTENSION_R1.md`, 14 September 2026.
7. NIST Digital Library of Mathematical Functions. Equation 27.4.5, Möbius
   Dirichlet series: https://dlmf.nist.gov/27.4.E5.
8. NIST Digital Library of Mathematical Functions. Section 25.4, zeta reflection
   formulas: https://dlmf.nist.gov/25.4.
