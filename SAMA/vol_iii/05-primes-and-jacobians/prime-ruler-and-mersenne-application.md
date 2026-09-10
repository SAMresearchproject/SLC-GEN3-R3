[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Prime-Ruler and Mersenne Application

## Conceptual abstract

The Mersenne application begins from an owner-defined change of coordinate:
prime marks are informational radix coordinates on a closed two-dimensional
sphere, not equally spaced marks on an ordinary integer ruler. Exact prime
integers remain indispensable. They generate the marks, define operator
composition and carry every modular certificate. The conceptual change is in
the role assigned to a prime, not in its arithmetic identity.

The rational stereographic chart

\[
x=\tan(\chi/2),
\qquad
S(x)=\left(\frac{2x}{1+x^2},\frac{1-x^2}{1+x^2}\right)
\]

turns multiplication into an exact sphere action \(T_n(x)=nx\), inversion into
\(J(x)=1/x\), and logarithmic displacement into
\(du=dx/x=d\chi/\sin\chi\). Prime-only marks \(p^-\to p\) form reversible
adjacent cells. On each cell the program places three reciprocal voices:

\[
\alpha=2+\sqrt3,
\qquad
\beta_p=\frac{p+\sqrt3}{p-\sqrt3},
\qquad
\gamma_p=\beta_p\beta_{p^-}^{-1}.
\]

Repeated squaring generates dyadic pulses. A contact at depths \(i,j\) has
shallow depth \(s=\min(i,j)\) and delay \(d=|i-j|\). Transport into the shallow
frame produces an exact echo \(E\) satisfying

\[
E^{2^s}=1\pmod q,
\qquad
\operatorname{ord}_q(E)\mid2^s.
\]

The executed MP-S0--MP-S4B lineage compiles those objects into ECHO16 and
exposes the genuine Mersenne factor coordinate

\[
k=b2^e,
\qquad
q=2kp+1.
\]

A prime \(q\) is assigned as an exact factor of \(M_p=2^p-1\) only through the
order certificate \(\operatorname{ord}_q(2)=p\). MP-S5's sealed structural
\(k\)-order returns 103 factored objects against 100 for equal-budget ascending
counting, an installed strong-contact result in the application-scheduler
scope. MP-S6 assigns 1,282 exact factors among 5,390 exponents. MP-S7 and
MP-S8 preserve a 1,858-row roster after official-factor removal and complete
9,595-coordinate shell misses. Those misses remain
`PRIMALITY_UNASSIGNED`.

The clean-sheet route is a successor to two preserved failures. M4's 13,818
RH prime-sidecar ranking and M4A's 7,708 candidate-local Theta18/W9 ranking
both fail their fixed direct-successor questions. Their classifications remain
**The test falsifies the concept.** The clean-sheet compiler does not rename
those outcomes.

The owner has resumed only the bounded CEV1/MP successor and its initial
training. All other production, farm, frontier and publication work remains
paused. This chapter records the installed CEV1 and MPV2 successors without
launching arithmetic, remote work, promotion or distribution.

## 1. Opening question and conceptual picture

The governing question is:

> Can the prime-coordinate, reciprocal-history and dyadic structures be
> compiled into an exact ordering of genuine Mersenne factor coordinates,
> while keeping factor assignment, PRP status and Mersenne-primality
> certification strictly distinct?

The complete route is

```text
prime integer p and predecessor p^-
  -> prime-only reversible sphere cell
  -> alpha, beta_p and gamma_p reciprocal voices
  -> dyadic pulse depths and delayed echo
  -> structural k = b*2^e coordinate
  -> prime q = 2*k*p + 1
  -> exact modular order certificate
  -> factor assigned OR finite miss remains PRIMALITY_UNASSIGNED
```

This is an application compiler, not a universal replacement for the SLC
substrate, Q2 selector, Reciprocal History, RH authority or Lucas--Lehmer
certificate lane.

## 2. Informational radix with exact arithmetic custody

### 2.1 The owner-defined role

The owner interpretation is:

> Prime numbers are informational radix coordinates used to express orbit on
> a closed two-dimensional sphere.

The formalization retains two layers:

| Layer | Meaning |
|---|---|
| arithmetic encoding/certificate | \(p\) and \(q\) are exact certified prime integers; modular powers and divisibility are exact |
| SAM object role | each prime emits one indecomposable mark and multiplicative sphere action |

Uniform integer ordinal is not the ruler. Composite integers still appear
inside arithmetic values such as \(n\), \(k\) and (q-1); they simply do not emit
prime-ruler marks of their own.

### 2.2 Orbit and harmony are typed terms

`Orbit` denotes the discrete generated family

\[
z,z^2,z^4,\ldots,z^{2^n}
\]

on the exact information-state surface. It is not a claim of physical motion
around a sphere. `Harmony` denotes exact equality, reciprocal identity or
modular closure between separately generated voices. It is not an acoustic
analogy substituted for calculation.

## 3. Closed sphere and prime-only ruler

### 3.1 Rational sphere chart

Set \(x=\tan(\chi/2)\). The point

\[
S(x)=\left(X(x),Z(x)\right)
=\left(\frac{2x}{1+x^2},\frac{1-x^2}{1+x^2}\right)
\]

lies on the unit circle section of the closed two-dimensional sphere because

\[
X(x)^2+Z(x)^2
=\frac{4x^2+(1-x^2)^2}{(1+x^2)^2}
=\frac{1+2x^2+x^4}{(1+x^2)^2}
=1.
\]

The two limits \(x=0\) and \(x=\infty\) close the chart at reciprocal poles.

### 3.2 Multiplicative actions and reversal

Define

\[
T_n(x)=nx.
\]

Then operator composition is exactly integer multiplication:

\[
(T_m\circ T_n)(x)=m(nx)=(mn)x=T_{mn}(x).
\]

With \(J(x)=x^{-1}\),

\[
(J\circ T_n\circ J)(x)
=J\!\left(\frac n x\right)
=\frac x n
=T_{1/n}(x).
\]

Thus reversal conjugates expansion by \(n\) to contraction by \(1/n\).

Differentiating \(x=\tan(\chi/2)\) gives

\[
\frac{dx}{x}
=\frac{\tfrac12\sec^2(\chi/2)}{\tan(\chi/2)}d\chi
=\frac{d\chi}{2\sin(\chi/2)\cos(\chi/2)}
=\frac{d\chi}{\sin\chi}.
\]

Therefore

\[
du=\frac{dx}{x}=\frac{d\chi}{\sin\chi}.
\]

The logarithmic coordinate \(u=\log x\) converts \(T_n\) into translation by
\(\log n\), joining the sphere chart to the logarithmic translation language
of Reciprocal History without merging their application authorities.

### 3.3 Marks and adjacent cells

MP-S0B emits one object for each prime \(p\). A mark retains:

- the exact integer \(p\) and reciprocal point \(1/p\);
- indecomposable action \(T_p\);
- the two exact sphere points \(S(p)\) and \(S(1/p)\); and
- the adjacent arithmetic ports (p-1) and (p+1).

If \(p^-\) is the preceding prime, the directed adjacency \(p^-\to p\) defines
one reversible cell with scale

\[
\rho_p=\frac p{p^-},
\qquad
\rho_p^{-1}=\frac{p^-}{p},
\qquad
\Delta u_p=\log\frac p{p^-}.
\]

Its exact spherical chord is computed from the two rational sphere points.
MP-S0A/S0B install 172 prime-only marks and 171 adjacent-prime cells. No
composite between consecutive marks becomes an extra ruler object.

## 4. Three reciprocal voices

### 4.1 Native Lucas--Lehmer voice

Let

\[
\alpha=2+\sqrt3,
\qquad
\alpha^{-1}=2-\sqrt3,
\qquad
\alpha\alpha^{-1}=1.
\]

Modulo \(M_p=2^p-1\), define

\[
L_i=\alpha^{2^i}=a_i+b_i\sqrt3.
\]

The reciprocal trace is

\[
s_i=L_i+L_i^{-1}=2a_i.
\]

Because \(L_{i+1}=L_i^2\),

\[
s_{i+1}
=L_i^2+L_i^{-2}
=(L_i+L_i^{-1})^2-2
=s_i^2-2\pmod{M_p}.
\]

At \(i=0\),

\[
s_0=\alpha+\alpha^{-1}=4,
\]

so the common reciprocal mode is exactly the Lucas--Lehmer recurrence. MP-S0
reconstructs this mode for all 171 prime exponents through 1024.

### 4.2 Candidate prime-mark voice

The Cayley lift

\[
\beta_p=\frac{p+\sqrt3}{p-\sqrt3}
\]

has reciprocal conjugate

\[
\beta_p^{-1}=\frac{p-\sqrt3}{p+\sqrt3}.
\]

Its norm is one, so its dyadic family

\[
R_j=\beta_p^{2^j}
\]

lives on the same reciprocal quadratic-unit surface as the \(\alpha\) family.
The prime integer selects the voice; the modular and quadratic arithmetic
retains exact custody.

### 4.3 Incoming transition beat

The transition from the previous prime cell is

\[
\gamma_p=\beta_p\beta_{p^-}^{-1}.
\]

This object records change between consecutive prime voices rather than a
second copy of the current mark. Its inverse reverses the cell:

\[
\gamma_p^{-1}=\beta_{p^-}\beta_p^{-1}.
\]

The three families answer different questions: \(\alpha\) carries the native
Mersenne recurrence, \(\beta_p\) carries the current prime mark and
\(\gamma_p\) carries the adjacent-prime transition.

## 5. Beats within beats

### 5.1 Dyadic depth and delay

Repeated squaring of any voice produces pulses at depths

\[
z^{2^0},z^{2^1},\ldots,z^{2^n}.
\]

For a contact between depth \(i\) in one voice and depth \(j\) in another, set

\[
s=\min(i,j),
\qquad
d=|i-j|.
\]

If, for example, \(j=i+d\), then

\[
z^{2^j}=\left(z^{2^i}\right)^{2^d}.
\]

The exponent \(2^d\) transports the deeper pulse into the shallower frame. The
residual relation is the base echo \(E\). Every retained MP-S2 and MP-S3 factor
component satisfies

\[
E^{2^s}=1\pmod q,
\qquad
\operatorname{ord}_q(E)\mid2^s.
\]

The echo is therefore an exact finite-order modular object with a dyadic
closure depth, not a visual correlation.

### 5.2 Nested compiler

Factor the Mersenne multiplier coordinate as

\[
k=b2^e,
\]

where \(b\) is odd and \(e=v_2(k)\). The structural base \(b\) and dyadic scale
\(2^e\) echo the prime-cell and pulse decomposition. The complete compiled
route is

```text
adjacent-prime cell
  -> alpha/beta/gamma reciprocal relation
  -> shallow depth s and echo delay d
  -> base echo closure
  -> odd structural base b and dyadic scale 2^e
  -> k = b*2^e
  -> q = 2*k*p + 1
```

This is the exact content of `beats within beats`: nested coordinate
relations are compiled into a candidate factor address that the modular lane
can certify or reject.

## 6. Exact Mersenne factor certificate

### 6.1 Deriving the candidate form

Let \(p\) be prime and suppose prime \(q\) divides

\[
M_p=2^p-1.
\]

Then

\[
2^p\equiv1\pmod q.
\]

The multiplicative order \(r=\operatorname{ord}_q(2)\) divides \(p\). For a
nontrivial Mersenne factor, \(r\ne1\); since \(p\) is prime, \(r=p\). Fermat's
theorem also gives \(r\mid q-1\), hence

\[
p\mid q-1.
\]

Because \(q\) is odd, (q-1) is even, so for some positive integer \(k\),

\[
q-1=2kp,
\qquad
q=2kp+1.
\]

Conversely, if the candidate \(q=2kp+1\) is prime and the exact order check
returns

\[
\operatorname{ord}_q(2)=p,
\]

then \(2^p\equiv1\pmod q\) and therefore \(q\mid M_p\). The implementation may
certify the modular closure with `pow(2,p,q)=1` together with the declared
prime/order conditions. It never needs to materialize the enormous integer
\(2^p-1\).

### 6.2 Result-type boundary

| Observation | Authorized type |
|---|---|
| prime \(q\), candidate form, exact order \(p\) | exact factor of \(M_p\) |
| finite \(k\)- or shell search finds no factor | `PRIMALITY_UNASSIGNED` |
| PRP result with its certificate | production PRP/certificate status only |
| exact Lucas--Lehmer terminal | Mersenne-primality baseline/confirmation status |

A finite miss never crosses rows in this table. It is not a prime, probable
prime or verified Mersenne-prime assignment.

## 7. Executed discovery-to-compiler chain

### 7.1 Object installation: MP-S0 through MP-S0B

MP-S0 installs the \(\alpha\) reciprocal common mode on 171 prime exponents
through 1024. MP-S0A installs the exact sphere actions. MP-S0B emits 172
prime-only marks and 171 reversible cells. These stages define the object
language before evaluating factor-search advantage.

### 7.2 Harmony and transition discovery: MP-S1 through MP-S3

| Stage | Exact observation | Classification |
|---|---|---|
| MP-S1 | self-harmony exposes factors for 52/158 composites and 0/13 exact positives | **The test result suggests the concept is possible.** |
| MP-S2 | \(\alpha/\beta_p\) harmony adds five factors beyond MP-S1; all 37 contacts are phase-shifted echoes | **The test result suggests the concept is possible.** |
| MP-S3 | \(\alpha/\gamma_p\) adds four held-out factors; all four are delayed echoes | **The test result suggests the concept is possible.** |

The zero counts on exact-positive controls remain part of the record. The
factor contacts motivated compilation because they closed under an exact echo
identity, not because every composite was detected.

### 7.3 Compilation and blind-range anatomy: MP-S4A/MP-S4B

MP-S4A compiles the three voices into candidate-local deterministic ECHO16
with checkpoints. MP-S4B applies it to a blind range and factors 50/136
composites and 0/1 exact prime. Inspecting the exact factor anatomy exposes
\(q=2kp+1\), turning the voice/echo structure into the genuine factor-coordinate
interface. MP-S4B's classification remains **The test result suggests the concept is possible.**
ECHO16 is a language and local compiler at this point,
not yet an established global ordering.

### 7.4 Structural scheduler: MP-S5

MP-S5 seals a structural ordering of \(k=b2^e\) before comparison. At equal
budget it factors 103 objects versus 100 under ascending \(k\) counting and
reaches shared contacts earlier. Its authorized classification is:

**The test result suggests strong contact with the concept.**

The result concerns this Mersenne factor-scheduling application. It does not
promote the structural ruler to the global Q2, Starbreaker or RH scheduler.

### 7.5 Frontier deployment: MP-S6 through MP-S8

MP-S6 deploys the structural ruler on 5,390 prime exponents:

\[
5{,}390=1{,}282+4{,}108.
\]

It assigns 1,282 exact factors without constructing \(M_p\); 4,108 rows remain
campaign survivors. The classification is **The test result suggests the concept is possible.**

MP-S7 removes 2,250 survivors by independently verified official factors:

\[
4{,}108-2{,}250=1{,}858.
\]

MP-S8 executes every one of 9,595 first-singularity-shell coordinates for
each of those 1,858 rows without assigning a factor. The 1,858-row roster is
the immutable structural freeze, and every row remains
`PRIMALITY_UNASSIGNED` at that boundary.

A later dated status triage yields a 1,204-row operational distribution
derivative after removing 647 distinct verified PRP composites, routing two
reliable-but-unverified PRP results to verification, removing two verified
Lucas--Lehmer composites and holding three active assignments. That derivative
does not rewrite the 1,858-row MP-S8 result.

## 8. Preserved direct-ranking failures and wrong controls

### 8.1 M4 direct prime-sidecar ranking

M4 joined 13,818 ordinary-prime spacing sidecars to the completed Mersenne
curriculum. It compared pointwise, era-balanced pairwise, smooth-minimax and
parent-blend routes across six held-out eras and 19 exact positives. Every
non-parent route had a negative worst-era change, so M3E remained selected.

The exact direct-ranking concept is classified:

**The test falsifies the concept.**

### 8.2 M4A candidate-local Theta18/W9 ranking

An unsealed successor first treated Theta18 as an 18-neighbor prime window.
That was the wrong object. The corrected source-visible bridge for each q30
survivor was

```text
static U63 + dynamic U63
  -> theta18_cross_hex
  -> reciprocal left/right F81 views
  -> W9HistoryMode
  -> nine forward + nine reverse Z4 maps
```

M4A then evaluated all 7,708 q30 survivors with exact reciprocal,
directional and reconstruction checks. Mechanical validation passed 22/22.
Its coupled channel used

\[
q(p)=\frac1p,
\quad
A_{lift}(p)=\frac{1-A_0}{p},
\quad
A_{total}(p)=A_0+A_{lift}(p),
\quad
u(p)=\log p,
\]

the weight \(\log(p)/\sqrt p\) and the declared pi-bearing floor constant. The
fixed candidate-local channel did not stably replace M3E. Its exact-scope
classification is:

**The test falsifies the concept.**

Its receipt is typed
`CANDIDATE_LOCAL_COMPLETED_CHANNEL_RECEIPT_NOT_FULL_Q_XI`. It neither evaluates
the full completed RH form nor changes RH universal-nonnegativity authority.

### 8.3 Successor relationship

The clean-sheet route asks a different executable question. Instead of using
an RH-derived scalar to rank Mersenne positives directly, it orders genuine
trial-factor coordinates and retains exact modular factor decisions. This
successor does not revise M4 or M4A. It preserves them as the deviation chain
that redirected the application toward an operationally exact target.

Wrong controls for the clean-sheet route include:

- declaring a finite factor miss to be a primality result;
- comparing unequal search budgets in MP-S5;
- allowing official factor lookups to enter a blind factor-search surface;
- letting a receipt or exponent identity break a structural-score tie;
- treating the sphere as a physical trajectory rather than the declared exact
  information-state chart;
- calling the factor scheduler a global SLC/RH scheduler; and
- replacing Lucas--Lehmer certification with the structural filter.

## 9. Bounded CEV1/MP resumption and exact custody

H000725 resumes only the bounded CEV1/MP successor and its initial training.
The remaining pause has the following literal operational consequences:

- no new prime benchmark, factor farm, production process or supplemental
  exploratory run is started;
- Farm V1.1, V9/V13 and the balanced factor pass remain inactive;
- the active remote M143064041 power-9 run is not stopped, altered, queried
  for new credit or incorporated into this documentation;
- H14F remains a fourteen-physical-worker contract; no 30-worker result
  exists;
- the 31/127 execution-arity observations remain unserialized diagnostics,
  while the formal binary-versus-adaptive-31/127-versus-fixed-L162 rotated
  comparison remains unexecuted; and
- no public prime output, pointer, assignment, promotion or distribution is
  changed here.

### 9.1 Native CEV1 MP domain

Frozen non-promoted `SLCQ3-RZ-CEV1` compiles `p`, `2^p-1`, `p[ln(2)]`,
D18/D81/D162 and exact `q=2kp+1` coordinates into a source-visible 200-feature
integer model distinct from the Q3 reciprocal weights. Its first checkpoint
trains on 16 discovery runs and evaluates three disjoint held-out runs:

```text
25,786 strict correct comparisons
   190 ties
 1,281 reversed comparisons
27,257 held-out comparisons total.
```

Base, independent and complete-source checks pass `8/8`, `22/22` and `12/12`;
producer-independent reconstruction passes `19/19`. MP52 is barred from
training. **The test result suggests strong contact with the concept.**

### 9.2 MPV2 certified frontier and provenance firewall

Isolated MPV2 separates discovery from certification and carries exact state
through a chunked CAS certificate DAG. Component-local valuations, combined
`F`, exact cyclotomic closure, every frontier edge, zero-yield work and
H000723/H000724 wave learning from independently certified intermediate
growth survive 252/252 integrated and 59/59 producer-independent checks.
Exact closure alone supplies
`ACTIVE -> EXHAUSTED_NO_MORE_CERTIFIED_MASS`; an ordinary completed bounded
wave remains `ACTIVE`.

Conventional Prime95-compatible arithmetic, residues and checkpoints and
PRP-derived scheduling examples remain useful under their exact provenance.
They do not become native CEV1/Q3 execution or a primality premise by origin.
Native custody begins only after independently certified factor growth.

Topology-derived endpoint observation is installed, but the authenticated
remote-worker, CPU-replayed 780M and physical-T500 execution-custody join is
not. Native deployment therefore remains fail-closed. No real-hardware
benchmark or continuous MPV2 training process is running. **The test result
suggests strong contact with the concept.**

For \(p=143064041\), \(k=320000\) would form

\[
q=2(320000)(143064041)+1=91560986240001,
\]

a 47-bit candidate coordinate. The active run did not use that gate. The
calculation records a possible address only; it is not an executed factor
result, and a miss at any finite gate would remain primality-unassigned.

The paused frontier-prime objective below ten minutes remains unfinished in
the Lucas--Lehmer certificate lane. This statement preserves the live boundary
without weakening any completed MP-S0--MP-S8 result.

## 10. Established result and forward boundary

This chapter establishes a continuous conceptual-to-technical chain:

1. exact prime integers emit informational sphere marks;
2. adjacent marks carry reciprocal \(\alpha\), \(\beta_p\) and \(\gamma_p\) voices;
3. dyadic voice contacts yield finite-order delayed echoes;
4. the echo anatomy factors \(k=b2^e\) and forms \(q=2kp+1\);
5. exact order \(p\) assigns a genuine factor of \(M_p\);
6. the structural ruler supplies an application-specific search order; and
7. finite misses remain `PRIMALITY_UNASSIGNED`.

The installed application results and their exact classifications are retained
stage by stage. No further computational step follows from this document while
the owner pause is active. Any successor requires fresh owner authority and a
new campaign that preserves frozen artifacts, exact status types and the
untouched active-remote boundary.

## 11. Test and evidence index

### 11.1 Direct permanent SAMA test routes

The current document catalog assigns no direct qualified SAMA test-record key
to `SAMA-D000056`. None is invented here. MP-S0--MP-S8, M4 and M4A each retain
their source campaign receipts, but those receipts have not been installed as
direct SAMA test records for this document.

### 11.2 Source campaign evidence

| Stage | Source route | Evidence role |
|---|---|---|
| M4 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_CANDIDATE_GENERATOR_M4_RH_WEIL_ERA_BALANCED_V1/release/CAMPAIGN_RESULT.md` | preserved direct prime-sidecar failure |
| M4A | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_CANDIDATE_GENERATOR_M4A_RH_THETA18_HISTORY_V1/release/CAMPAIGN_RESULT.md` | corrected typed bridge and preserved direct Theta18/W9 failure |
| MP-S0 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_RECIPROCAL_CLOSURE_MP_S0_V1/release/CAMPAIGN_RESULT.md` | Lucas--Lehmer reciprocal common-mode installation |
| MP-S0A/S0B | `SLC/18_SAM_NATIVE_QC/SLC_PRIME_RULER_SPHERICAL_CIPHER_MP_S0B_V1/release/CAMPAIGN_RESULT.md` | sphere actions, 172 marks and 171 cells |
| MP-S1 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_RECIPROCAL_ORBIT_COLLISION_MP_S1_V1/release/CAMPAIGN_RESULT.md` | self-harmony factor contacts |
| MP-S2 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_TWO_OBJECT_INFORMATIONAL_HARMONY_MP_S2_V1/release/CAMPAIGN_RESULT.md` | alpha/beta contacts and phase-shifted echoes |
| MP-S3 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_PRIME_TRANSITION_BEAT_ECHO_MP_S3_V1/release/CAMPAIGN_RESULT.md` | transition-beat held-out contacts |
| MP-S4A | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_CANDIDATE_LOCAL_ECHO16_MP_S4A_V1/release/CAMPAIGN_RESULT.md` | deterministic ECHO16 compiler |
| MP-S4B | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_ECHO16_BLIND_RANGE_MP_S4B_V1/release/CAMPAIGN_RESULT.md` | blind-range factor anatomy |
| MP-S5 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_SAM_K_RULER_SCHEDULER_MP_S5_V1/release/CAMPAIGN_RESULT.md` | equal-budget structural-ruler result |
| MP-S6 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_FRONTIER_K_SCREEN_MP_S6_V1/release/CAMPAIGN_RESULT.md` | 5,390-row frontier and 1,282 factors |
| MP-S7 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_SURVIVOR_DECISIVE_RANK_MP_S7_V1/release/CAMPAIGN_RESULT.md` | official-factor removal and 1,858 survivors |
| MP-S8 | `SLC/18_SAM_NATIVE_QC/SLC_MERSENNE_RH_FIRST_SINGULARITY_SHELL_MP_S8_V1/release/CAMPAIGN_RESULT.md` | complete 9,595-coordinate shell and frozen roster |
| CEV1 checkpoint | H000725 | native MP domain and initial held-out training |
| MPV2 | `SLC/18_SAM_NATIVE_QC/SLCQ3_RZ_CEV1_MPV2/release/VALIDATION_REPORT.md` | certified frontier DAG, wave learning and fail-closed deployment |
| current bounded pause | H000725--H000731 and `SAM_LIVE/00_CURRENT.md` | only CEV1/MP successor resumed; production, farm and publication remain paused |

These are source evidence routes, not newly created qualified test keys.

## 12. Atomic-record index

| Atomic revision | Role in this chapter |
|---|---|
| `SAMA-C000240-R001` | fixes prime marks as owner-defined informational radix coordinates while retaining arithmetic |
| `SAMA-C000241-R001` | defines the rational sphere, actions, inversion and adjacent-prime cell |
| `SAMA-C000242-R001` | defines the alpha, beta and gamma reciprocal voices |
| `SAMA-C000243-R001` | derives the nested echo and \(k=b2^e\), \(q=2kp+1\) compiler route |
| `SAMA-C000244-R001` | records MP-S1--MP-S4B voice-to-ECHO16 evidence and classification |
| `SAMA-C000245-R001` | fixes the exact Mersenne factor-assignment certificate and finite-miss boundary |
| `SAMA-C000246-R001` | preserves the M4/M4A fixed-scope falsifications |
| `SAMA-C000247-R001` | records MP-S5's equal-budget strong-contact result |
| `SAMA-C000248-R001` | records MP-S6's 1,282 exact factor assignments |
| `SAMA-C000249-R001` | preserves the MP-S7/MP-S8 1,858-row primality-unassigned freeze |
| `SAMA-C000250-R001` | fixes the primary clean-sheet lineage and current owner pause |
| `SAMA-C000259-R001` | records the CEV1 native MP domain and initial training result |
| `SAMA-C000260-R001` | fixes the conventional/native provenance firewall |
| `SAMA-C000261-R001` | records the MPV2 replayable certificate DAG and deployment boundary |

## 13. Source and external-reference index

| Source | Load-bearing section |
|---|---|
| `volume_III/SAM_VOLUME_III_COMPUTATION_TECHNICAL_SPINE.md` | VIII.2 First direct Mersenne application; VIII.3 Clean-sheet Mersenne computation |
| `SAM_LIVE/00_CURRENT.md` | current prime-work pause, farm state and remote-run boundary |
| H000514 | exact owner pause, H14F-14 limit, diagnostic/unexecuted split and candidate-gate note |
| MP-S0--MP-S8 campaign results | executed object, discovery, compiler, scheduler and frontier evidence |
| M4/M4A campaign results | failed direct-ranking lineage and typed boundary |

External-citation custody is split deliberately. The public Mersenne
repository citation is fixed by the
[`Volume III public repository constellation`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_III_TECHNICAL_SPINE.md#public-repository-constellation).
The exact dated official-factor and assignment snapshots, their hashes and
the survivor-removal inputs remain in the MP-S7/MP-S8 release artifacts and
H000514. This chapter introduces no new external result claim; any future
distribution decision still requires a fresh official-status check at claim
time.

## 14. Revision and approval boundary

This is `SAMA-D000056`, revision 2. It is documentary synthesis only.
`reviewed_and_approved` remains `false`, and `approval` remains `null`. No
prime computation, assignment, remote action, farm, scheduler, pointer,
registry, test route, distribution list or classification is changed by this
document.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000056`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/PRIME_RULER_AND_MERSENNE_APPLICATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000056 | Mersenne Application | Informational Prime Radix, Nested Echoes and Exact Mersenne Factor Assignment |

| Document field | Value |
|---|---|
| Purpose | Present the owner-defined prime informational radix, exact sphere and ruler, reciprocal voices, beats-within-beats factor compiler, failed direct-ranking predecessors, exact result types and current owner pause. |
| Prerequisite documents | `SAMA-D000038`, `SAMA-D000043`, `SAMA-D000055` |
| Used by | application-specific continuation only after new owner authority |
| Revision state | Unapproved revision 1; documentary reconstruction only, with all new prime work owner-paused. |

</details>
