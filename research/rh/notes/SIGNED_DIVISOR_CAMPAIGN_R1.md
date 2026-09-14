# Native signed-divisor / derivative-energy campaign

Status: ACTIVE in the existing feedback and CPU producer. The owner has
cancelled all scheduled stops, the final backup and automatic provider pause
(H001422). No replacement stop is installed. This supersedes the operational
6:30 deadline recorded at the initial campaign-contract freeze.

Sean Brady supplies research direction; ChatGPT supplies the campaign handoff
and dual-witness proposal; Codex supplies the completed local derivation,
native implementation, analytic follow-through and integration. The handoff is
preserved in results/signed_divisor_campaign_r1/sources/.

## Frozen mathematical contract

Contract RH-SIGNED-DIVISOR-R1 binds ORIGINAL_KERNEL_SPECTRAL_R1.md (S5)-(S7)
by SHA256. It keeps the complete actual-source divisor functional, including
mean, in the integer polynomial test space p_0,...,p_m,
m=min(s-1,ceil(sqrt(s))). Its derivative Gram matrix is diagonal:

    G_0=s, G_k=d_(s,k) k(k+1), k>=1.

The smaller-source factor is the literal original full dyadic energy

    E_u=sum_(dyadic n<=u) Q_n(mu(n),...,mu(min(2n-1,u))),
    u=floor(sqrt(2s-1)), with original zero padding in the last block.

Its first block is mu(1)=1, so E_u>=1. No fitted denominator or source-vector
operator norm is substituted. For ell_k=sum_i mu(s+i)1_(i<t)p_k(i), native GMP
returns cstar_k=ell_k/G_k, d=ell^T G^-1 ell=F_m and required gain d/E_u.
It verifies G cstar=ell, J(cstar)=L(cstar)=d. When d=0 the returned zero
vector is not asserted to be a unique maximizing direction.

The finite certificate for every test direction c is

    d J(c)-(ell.c)^2
      =sum_(i<j)G_i G_j(c_i cstar_j-c_j cstar_i)^2 >=0.

The frozen candidate family is B(s)=1/16,1/8,1/4,1/2,1,2, all degree0.
Each candidate supplies F_m<=B E_u; the completed original tail then gives
Q<=B E_u+1 and the decreasing square-root recurrence gives subpower growth.
The family is sufficient, not an additional required condition for RH.
Original source means, signed drift/discrepancy and return coupling remain
joined. Complete-source spectral tails are not relabelled discrepancy tails.

## First campaign result

All15364 prefixes at s1024,2048,4096,8192 receive exact joint normalized dual
scores. This is complete coverage of that quantity. Full original Q/Qhat,
D_adm, X_adm, exact maximizing test functions and full-degree divisor
reconstruction are retained at every maximum tie and selected requests.

| Scale | Prefixes | Maximum F_m/E_u | Every maximum stop | B=1/8 failures |
|---:|---:|---:|---|---:|
|1024|1025|0.088967031602|962|0|
|2048|2049|0.134688011607|2047,2048|7|
|4096|4097|0.153898057352|4094,4095|45|
|8192|8193|0.160919124000|1670|242|

B=1/16 fails45,945,1203,2989 prefixes respectively. B=1/4 and larger
frozen constants survive every declared prefix. The selected existing owning-
engine s16384,t3404 source has required gain0.12176772999960468 and also passes
B=1/4. Its source object and original request are retained by hash.

For B=1/8 and B=1/16: **The test falsifies the concept.**
For the B=1/4 source-gain candidate: **The test result suggests the concept
is possible.** Uniform validity remains OPEN. No RH closure is claimed.

The four full-prefix native calls take0.195,1.260,5.106,8.183seconds respectively;
peak RSS reaches321548KiB at8192. Those are native-wrapper elapsed times, not
end-to-end adoption times. The16384 selected deep call takes7.396seconds,
7.376native CPU seconds, peak795496KiB. Its independent source/full-kernel and
dual checks pass. Source, training, transfer, publication and receipt costs
remain individually available in their native and transport records.

## What the signed product bands reveal

Every ordered smaller-source factor pair is retained in deterministic dyadic
product bands. The native readout stores all per-band mode vectors and ALL
interband signed crosses, plus each band's contraction against cstar.

| Endpoint | Sum of band self energies | Sum of interband crosses | Joint retained energy |
|---|---:|---:|---:|
|8192,1670|3340.554542529|-3339.542843749|1.011698779|
|8192,6994|28252.560385784|-28252.184906209|0.375479575|
|4096,4094|18557.874827710|-18556.944209440|0.930618270|

The respective sums of absolute contractions against cstar are121.1361,
58.8220 and189.8098, while their complete signed contractions equal the small
joint energies in the last column. Independent band charges discard the
actual compensation. This identifies the important loss to avoid in the next
source estimate. The mandatory low-mean/high-history source8192,6994 remains
in training and in the deep signed-coupling readout.

## Next analytic statement: cumulative signed divisor coefficients

Codex deduction from the exact source synthesis: put

    c_u(d)=sum_(ab=d,a,b<=u)mu(a)mu(b),
    C_u(D)=sum_(d<=D)c_u(d)
          =sum_(a<=min(u,D))mu(a) M(min(u,floor(D/a))),
    M(y)=sum_(n<=y)mu(n),
    T_d(f)=sum_(v=ceil(s/d))^floor((s+t-1)/d) f(dv-s).

For D=u², finite summation by parts gives

    L_s,t(f)=-C_u(D)T_D(f)
              +sum_(d=1)^(D-1) C_u(d)[T_(d+1)(f)-T_d(f)].

This follows by substituting c_u(d)=C_u(d)-C_u(d-1) and collecting terms;
C_u(0)=0. Empty arithmetic-progression ranges contribute zero. It retains
all signs and the terminal term. The exact smaller-source prefix formula
makes the arithmetic dependency explicit. The proposed next bound is this
WHOLE expression squared <= B(s) E_u R_s(f), retaining coupling rather than
charging the large individual band energies. Its uniform inequality is OPEN;
the new Abel representation itself is an algebraic deduction, not a native
experiment or a replacement target.

## Learning and real adoption

The new target is carried by the native successor
GEN3_TRANSFER_RH_SIGNED_DIVISOR_R1, integrated as a versioned supplement to
GEN3_TRANSFER_RH in the existing rh_feedback_loop.py. It fits an exact rational
regression stump on source-only features M/s, prefix-area/s², N/s and t/s,
with supervised label F_m/E_u. Native fit, model parameters and rules are
stored with binary, contract and source hashes. Its state lives in the
existing atomic RH generation; the original native transfer head and rows
are retained independently, not overwritten by a new schema.

- Cycle18 publishes six-anchor training and derivative requests in generation
  68c97ac0bef05bb92be74e45ce04c7eb3fbf9e88660c73e75af8bf974feb1f65.
- The existing CPU producer adopts it and executes NEW selected derivative
  witnesses, each independently certified against regenerated actual mu,
  full original kernel energy, tail enclosure and dual attainment.
- Cycle19 admits21 derivative windows and publishes
  b320236663f89867aa6aaa64539a29d27db6d115b84e8750048409f5412e03b1;
  the producer executes its learned follow-ups.
- Cycle20 admits30 derivative windows, including the16384 follow-up, and
  publishes f5a5c11683276308cd5579a5b4eae13770a36c568f895f64b78de8d80bc17f26.
  Its original prime-trace corpus remains515 windows/270575 rows/541150 checks.

Scale4096 is wholly excluded from training. The frozen six-anchor predictor
is evaluated on its4097 prefixes: mean squared error0.002838986622140045,
maximum absolute error0.12449428267188256. This is measured prediction error,
not a certificate of source gain. Exact arithmetic certifies selected outputs
regardless of predictor error. The model's initial tied-score ordering selected
early prefixes. R2 retains its regression score and resolves ties by distance
to the measured same-scale demand maximum, with an explicit selection reason.
No target-derived feature is disguised as independent predictive evidence.

Certificate choice remains deterministic among the already valid exact tail
bounds; no learned theorem-validity claim is made. Readable source-conditioned
regression rules and complete signed witnesses support analytic review.

The existing40 learned/24 fresh allowance is preserved across routes: up to
8/4 slots are reserved for the new target, with32/20 for legacy suggestions.
The CPU worker consumes the new requests before its preserved old coverage.
No second producer or coordinator is installed. Owner locks serialize native
calls with existing work; hashes include native version in the cache key.
All previous generations, source rows and original CPU cursors remain.

## Operations and preservation

The first producer reload drains its current batch using its existing SIGTERM
handler, then resumes the SAME unit and cursor. Seven feedback integration
checks pass. Four pause-gate and three transfer-order checks pass. A redundant
session-open path for already-completed requests is removed. Native version
hashes are included in model and transport cache keys for the R2 selector.

A stale5AM preservation control terminated the shared native service during
the pilot; the pod stayed up and the separate CPU producer continued. The
missing socket failed a feedback attempt and preserved its pending cycle.
Recovery initially exceeded the service launcher's60-second wait, while the
native process continued loading. It subsequently became ready. Its recovered
HEAD exactly matches authenticated root
b997ecde998a7cc4c4f3f499a68621baf546f4884b58f6a5dbdf417ee9759e9d.
Cycle20 completes after recovery. The cancelled-stop policy now covers that
preservation control and the formerly stale feedback transport deadline.
Native PID1256225 and its checkpoint watcher1257909 are verified.

All scheduled stops, final cleanup/backup and provider pause are CANCELLED
under H001422. Numeric epochs retained for legacy comparison code are inactive
compatibility sentinels, not scheduled dates. The archive entry point returns
CANCELLED_BY_OWNER; the provider pause gate rejects the cancelled policy.
Research admission remains open. No provider-stop request or full backup was
issued by this campaign.

The owning engine has no pending source jobs at inspection. Its authenticated
index contains833 completed harmonic sources at16384 and543 at65536. We reuse
one16384 endpoint;65536 and the broader next-scale ladder remain queued as
continuation work, with exact source IDs retained. The currently qualified
campaign adapter permits selected sources through16384. Extending the next
scale requires a bounded successor/cost check; no unexecuted larger results
are counted. The existing model-selected follow-up loop remains active.

## Artifacts and continuation

results/signed_divisor_campaign_r1/ contains CONTRACT.json, BOOTSTRAP.json,
bootstrap/, models/, executed/, coverage/, analytic_review/, larger_sources/,
LARGER_SOURCE_INDEX.json, NATIVE_RECOVERY_VERIFIED.json and
CANCELLED_DEADLINES_RECONCILED.json. CONFIG references and installed locators
bind native binaries, source bundles, model versions and contract hashes.
Each native call retains actual DomainSession input/output/receipt files and
its pod archive. Whole-prefix scalar tables, maximum ties and complete
selected vectors are retained; no broad duplicate source-vector export.

For the native representation/adoption experiment: **The test result suggests
strong contact with the concept.** The original uniform signed-growth estimate
and the new candidate's uniform signed-divisor gain remain OPEN.
