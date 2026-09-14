# Original-kernel spectral adoption and signed divisor follow-through

14 September 2026. Owner directed adoption of the two Downloads files:
RH_ORIGINAL_KERNEL_IDEAS_2026-09-14.md and kernel_spectrum_validation.json.
The supplied algebra/reference experiment is attributed to ChatGPT's review
of snapshot 667740d6baedbfaed574e4d19edf933698ea24c0. Codex implements native
adoption and the prefix-area, joint discrepancy and dual-source deductions
below. Sean Brady supplies the conceptual direction.

## Adopted exact geometry

For the original length-s stopped source a_i=mu(s+i)1_(i<t), the full
kernel is K=Pi+L^+, with inverse K^-1=Pi+L. Here

    f^T L f = sum_(r=1)^(s-1) r(s-r)(f_(r-1)-f_r)^2.

Its spectrum is 1 followed by 1/[k(k+1)], 1<=k<s. The supplied integer
polynomials p_k and exact norms d_k give signed moments A_k=sum a_i p_k(i).
With m=min(s-1,ceil(sqrt(s))), define

    F_m=A_0²/s + sum_(k=1)^m A_k²/[d_k k(k+1)].

The supplied uniform enclosure F_m<=Q<=F_m+1 is retained. The tighter native
tail is (N-sum_(k=0)^m A_k²/d_k)/[(m+1)(m+2)], with zero tail at m=s-1.
It is distinct from the measured tail Q-F_m. Combining the installed
projection/diagonal bounds gives V_U<=sum_roster F_m+b_U and
sum_roster F_m<=V_U+10b_U on the original roster. No original baseline,
positive-part placement, cutoff or tau changes.

## Native execution

RH-ORIGINAL-KERNEL-SPECTRAL-R1 and its bounded discrepancy successor execute
through NativeDomainSession on the existing GEN3-RXT-R7.1 pod. Startup
verifies SLC-GEN3-R3 / SLC-GEN3-CEV1-R3 / RH-GEN3-GROWTH-V4. C++/GMP owns
research arithmetic; Python supplies transport and identified comparisons.

- Small-scale native qualification: 1,496 eigenvector coordinate equations,
  136 norms, 680 orthogonality pairs, 126 full-energy control cases,
  126 return identities, 198 smaller-source divisor moments, plus 16 traces.
- Six reference anchors: 78 exact equalities against the supplied fractions.
- Four overlapping saved native cases: 12 exact Qhat/D_adm/X_adm equalities.
- All 513 prefixes at s512: exact spectral enclosures and original positive
  cross bounds; every extremal tie retained.
- Six anchors reconstructed from complete smaller-source factors at degrees
  0 through 5; source-selected s512 extrema receive the same readout.
- Joint harmonic discrepancy follow-up: 336 exact checks, including all
  retained degree decompositions, prefix-area and degree-one divisor formulas,
  joint energy reconstruction and previous native low-energy equality.

The native inherited sieve regenerates mu from its definition and exports
stopped-source hashes. The supplied JSON has no source-vector hashes, so a
reference source-hash match is not claimed. Existing native quantity equality
is recorded separately. U/tau/g are not reconstructed or assigned surrogate
values; no C1 endpoint certificate is issued by this bounded readout.

The first compilation exposed an ambiguous JSON-to-integer conversion when
retaining ties. Explicit conversion corrects it; the first source and remote
build log remain preserved. Numerical qualification and results are from the
corrected content-addressed binary.

## Source-selected results

| s | t | Full Q | Retained F_m | Certified F_m+tailUpper | Original X_adm |
|---:|---:|---:|---:|---:|---:|
|512|43|0.555231709284|0.552371572549|0.586718845203|0.394728352546|
|512|75|0.618079351000|0.614770802521|0.680996992344|0.373850982622|
|1024|395|0.475564089882|0.466854660869|0.678096752400|-0.028111713533|
|2048|783|0.683043152740|0.677208449667|0.878611001077|0.175483476582|
|8192|1670|1.013888925876|1.011698779390|1.128509721058|0.678424313172|
|8192|6994|0.380527745338|0.375479575337|0.866865044394|-0.569443581100|

At s512 the unique positive-cross maximum is t43, the unique full-energy
maximum is t75, and the unique certified-upper maximum is t512. The latter
is 0.9846933110741277. All 513 prefixes have positive cross below 1/2.
The selection distinguishes actual source energy from looseness of an upper
bound; none of these finite facts reinstates the half-bound rejected in H001419.

At s8192,t6994, the weighted return identity reads

    Q = Q_open + E_closed + cross_open_closed
      = 0.0451672349834 + 0.4024605412682 - 0.0671000309140.

The last zero is at6097 and the signed return area is -27.484172662354226.
The completed returns retain their weighted footprint; the signed coupling
reduces the complete energy. At t1670 the corresponding coupling is positive.

## New deduction: the first mode is signed prefix area

Write P_r=sum_(i<r)a_i and M=P_t. Summation by parts gives, for t>=1,

    A_k = p_k(t-1) M
          + sum_(r=1)^(t-1) P_r [p_k(r-1)-p_k(r)].                 (S1)

This identity follows by substituting a_i=P_(i+1)-P_i and collecting terms.
Since p_1(i)=s-1-2i,

    A_1=(s-2t+1)M+2 sum_(r=1)^(t-1)P_r,
    modeEnergy_1=3 A_1²/[2s(s²-1)].                              (S2)

At s8192,t6994, M=-10, prefix area=-149308, A1=-240666.
The first cut mode contributes0.158034138856 while the mean contributes
0.01220703125. These are actual signed moments before squaring.

There is also an exact closed smaller-source expression. Set
u=floor(sqrt(2s-1)); for d=ab let l=ceil(s/d), h=floor((s+t-1)/d),
nu=max(0,h-l+1). The supplied divisor synthesis gives

    A_1=-sum_(a,b<=u) mu(a)mu(b) nu [3s-1-ab(l+h)].                (S3)

An empty interval contributes zero. This follows by summing
p_1(abv-s)=3s-1-2abv over l<=v<=h. All six anchors satisfy (S2)-(S3)
in native integer arithmetic. The complete ordered factor pairs are retained.

## New deduction and execution: discrepancy in all retained modes

Use the already retained harmonic drift delta=-(sum_(n<=u)mu(n)/n)^2.
On the stopped source set e_i=a_i-delta for i<t, zero otherwise.
Let B_k=sum_(i<t)p_k(i), A_k^d=delta B_k, A_k^e=A_k-A_k^d.
With weights omega_0=1/s and omega_k=1/[d_k k(k+1)] for k>=1,

    F_m = F_d + F_e + C_de,
    F_d=sum omega_k (A_k^d)^2,
    F_e=sum omega_k (A_k^e)^2,
    C_de=2 sum omega_k A_k^d A_k^e.                              (S4)

| s,t | F_d | F_e | C_de |
|---|---:|---:|---:|
|512,43|0.000168098203|0.571649736943|-0.019446262597|
|512,75|0.000420528579|0.647139677614|-0.032789403671|
|1024,395|0.000047046864|0.474333686676|-0.007526072671|
|2048,783|0.000031325831|0.668819640071|0.008357483764|
|8192,1670|7.719797e-11|1.011681693121|0.000017086192|
|8192,6994|6.533299e-10|0.375471258042|0.000008316642|

At the two s8192 anchors the harmonic drift is tiny across the complete
retained energy, not just the mean, and its joint cross with discrepancy is
positive. The signed divisor discrepancy is the substantive source term there.
No uniform small-drift assertion is inferred from these finite values.

## New deduction: one joint dual estimate for the recursive route

Let H_m=span(p_0,...,p_m), and define the positive quadratic form

    R_s(f)=(sum_i f_i)^2/s
           +sum_(r=1)^(s-1)r(s-r)(f_(r-1)-f_r)^2.

Since R_s(f)=f^T K^-1 f and H_m is invariant under K,

    F_m = sup_(f in H_m, f!=0) (sum_i a_i f_i)^2/R_s(f)
        = sup_(f in H_m) [2 sum_i a_i f_i-R_s(f)].                 (S5)

To derive this, expand f in the orthonormal polynomial basis, complete each
square, and sum. The optimizer is the truncated K a; its quadratic cost and
source pairing both equal F_m. Thus this is a joint norm identity, with no
required separate bound on each mode or percentage of explained energy.

The numerator has the exact smaller-source form

    sum_i a_i f_i = -sum_(a,b<=u)mu(a)mu(b)
                      sum_(v=ceil(s/ab))^floor((s+t-1)/ab) f(abv-s). (S6)

Use the existing full dyadic input energy E_u(mu(1..u)), including its
original zero-padded final block. A sufficient actual-source estimate is

    |right side of (S6)|² <= G(s) E_u(mu) R_s(f), all f in H_m,     (S7)

uniformly in original s,t. It would yield Q_s,t<=G(s)E_u(mu)+1.
For the existing envelope over maximum stops at each dyadic scale,
E_u(mu)<=E(sqrt(2s)); summing over O(log x) output scales gives a decreasing
square-root recurrence. A polylogarithmic G gives
log(1+E(x))=O((loglog x)^2). Arbitrary subpower gains also suffice: the
successive log-scale exponents sum as 1+1/2+1/4+...=2, and an arbitrarily
small exponent absorbs that fixed factor. Finite base scales enter the
constant. This is a source-restricted route; replacing both mu factors by
arbitrary vectors would be a different, stronger operator question.

(S7) remains OPEN. Codex recommends working directly on its signed bilinear
sum, using the prefix-area and higher polynomial differences to organize
the discrepancy. The benefit is a transparent joint output norm and genuine
smaller-source support. The unresolved work is the uniform signed gain;
bounding each factor pair absolutely loses the cancellation under study.

## Result and continuation

**The test result suggests strong contact with the concept.** Scope: the
original-kernel spectral/divisor/weighted-return representation and its
native source execution. The original uniform signed-growth estimate remains
OPEN. Larger source-selected s16384/s65536 cases and baseline-specific C1
certificates are pending; no unexecuted results are counted.

This is a completed bounded research pass with two saved native readout
configurations, not a continuous worker or a change to the production learner.
The prior half-bound witness and all prior source results remain preserved.

Artifacts relative to this campaign:
- results/original_kernel_spectral_r1/sources/: immutable copies of both supplied files.
- results/original_kernel_spectral_r1/CONFIG.json, QUALIFICATION.json, COMPLETION.json.
- results/original_kernel_spectral_r1/ANCHOR_*.json and PREFIX_SCAN.json.
- results/original_kernel_discrepancy_r1/CONFIG.json, ANCHOR_*.json, COMPLETION.json.
- extensions/original_kernel_spectral_r1/ and extensions/original_kernel_discrepancy_r1/.
- tools/original_kernel_spectral_r1.py and tools/original_kernel_discrepancy_r1.py.

Source sessions:
RH_20dddafc219b4b2693b4573488e0502a (spectral),
RH_2170d04329114c219a14c5339ce88974 (discrepancy), each under its result directory.
