# GEN3-R4 native structured arithmetic contract

Protocol remains one JSON object per line, `{op,payload}` to the existing warm
C++/GMP worker; replies `{ok:true,result}` or `{ok:false,error}`. Existing
operations remain available. Exact numbers are integer JSON values or rational
strings and are returned as canonical rational strings. Floating inputs reject.

The managed Python consumer authenticates source identity, basis ordering,
normalization, units/reference, history, executable binding and stored native
record before invoking readout or extension. Native `record` is an internal
trusted-store interface, never a caller-supplied public certificate. Native
validation checks its registered norms/eigenvalues, weights, mode order, mean,
nonnegative residual and all energy-tail arithmetic. It does not claim that
internal structural validation authenticates a source's provenance.

## Registered provider and record

`MEAN_CUT_V1`: dimension s, K=mean projector + weighted path Laplacian inverse
on the mean-zero space. lambda_0=1; lambda_k=1/[k(k+1)]. The integer basis and
norm recurrence are adapted from completed
`GEN3_RXT_RH_WEEKEND1/extensions/original_kernel_spectral_r1/search.cpp`.
Only two temporary basis rows are allocated; the durable record contains no
matrix, basis-coordinate arrays, or duplicated source vector.

`SPECTRAL_ADMIT {source:[...],kernel?:"MEAN_CUT_V1",max_degree?,max_new_modes?,max_basis_coordinates?}`
returns `{record,counters,requested_degree,status}`. Default degree min(s-1,4).
`SPECTRAL_EXTEND` takes the same fields and `record` from authenticated custody.
It computes only missing signed source projections. Reconstructing old basis
coordinates is separately counted; stored moments are never recomputed.

Record schema `GEN3_NATIVE_SPECTRAL_RECORD_V1` contains `kernel,s,m,mean`
(where mean is the signed sum M, not M/s), `source_norm_squared`, `modes`,
`retained_energy`, `residual_norm_squared`, `lambda_tail`, `tail_upper`,
`retained_mode_count`, `full_spectrum`. Each mode contains
`k,moment,norm,weight,eigenvalue`; weight=moment^2/norm. m is the largest degree;
mode count is m+1. Generic rational source norm is the exact sum of squares.

## Readouts

`SCALAR_LOG {record,reference?,rho?,epsilon?,numerical?,max_terms?}` returns
kind `CERTIFIED_SCALAR_LOG1P`, exact `energy_lower,energy_upper`, positive
`lower_argument,upper_argument,width_ratio`, explicit `formal_enclosure`,
`formal_tolerance_met` under rho, and optional `numerical` interval. Reference
is a positive divisor of the energy inside log(1+Q/reference), default 1.
Default rho is 1000001/1000000; it must exceed 1.
`DIRECT_SCALAR_LOG` substitutes the admitted `source` for `record` and computes
exact Q using O(s) prefix cuts. It preserves the direct scalar route.

`SPECTRAL_LOG {record,tau?,epsilon?,coefficient_order?,numerical?,max_terms?}`
returns kind `CERTIFIED_SOURCE_SPECTRAL_LOG`, `terms` with
`k,moment,weight,argument=1+tau*lambda`, `tail` with
`log_weight=residual,log_argument=1+tau*lambda_tail,linear_upper=tau*tail_upper`,
`derivative {lower,upper,tail_upper}`, and `coefficients` containing
`order,retained,absolute_tail,lower,upper`. First derivative is at supplied tau;
coefficients are the formal expansion about zero, order default 4. Sufficient
analytic convergence scope is explicitly abs(tau)<1. tau defaults to 1 and
must be nonnegative. This target is the source quadratic spectral logarithm;
it is distinct from scalar log and trace log determinant.

A numerical request sets `numerical:true`. Both readouts return exact rational
`numerical {lower,upper,width,evaluation_width,mode_tail_upper,epsilon,tolerance_met}`.
For scalar logs the interval uses independently evaluated monotone endpoints;
the evaluation-width and mode-tail entries are separately valid allowances,
not necessarily a decomposition equal to the tighter total width. For spectral
logs the interval is the retained expression enclosure plus the smaller of
the rational linear tail and the certified logarithmic tail upper bound.
Default epsilon=1/1000000, strictly positive. Native default numerical=false;
the public interface may choose true. Evaluation uses rational range reduction
x=2^e*y with 1<=y<2 and the atanh series z=(y-1)/(y+1). After n terms the
nonnegative remainder is at most 2*z^(2n+1)/[(2n+1)(1-z^2)]. No floating
arithmetic, factorization or denominator-clearing exponentiation is used.
Negative logarithms are obtained by reciprocal and interval negation.

`status` is `EXACT_SYMBOLIC` for zero symbolic tail (when no numerical interval
is requested), `CERTIFIED_WITHIN_TOLERANCE` when the requested bound succeeds,
or `CERTIFIED_BUDGET_LIMITED` with its valid enclosure otherwise. For numerical
requests success always uses TOTAL interval width <= epsilon, regardless of
whether the symbolic mode tail or rho test already passes. EXTEND instead uses
`REQUESTED_DEGREE_COMPLETE` or `CERTIFIED_BUDGET_LIMITED`.

Adaptive orchestration increases degree on its declared ladder using EXTEND,
and increases max_terms when evaluation error limits accuracy. It stops on
success, exhausted budgets, or no further degree/precision progress. A zero
extension budget retains an existing valid record with zero new projections.

## Exact-total transport

`TRANSPORT_LOG {initial_energy,reference?,increments:[{E,R,J,epsilon_0?,Q_next,...history}],numerical?,epsilon?,max_terms?}`
requires nonnegative initial and reconstructed energies and verifies each
`Q_next=Q_current+E+R+epsilon_0*J` exactly. Endpoint epsilon_0 is integer 0 or 1,
default 0. E,R,J retain their signs without absolute-value bounds. Each complete
increment object is preserved with `Q_current,Q_next,ratio,formal_log` and
optional numerical interval. The output includes `final_energy,telescope_ratio`,
exact formal telescope log and optional certified telescope numerical interval.
Ratios are `(reference+Q_next)/(reference+Q_current)`. Zero denominators and
invalid totals reject. Interval-history rise/fall aggregation is deferred.

## Bounds and counters

s=1..65536; retained degree 0..min(s-1,256); max_new_modes=0..257, default257;
max_basis_coordinates=1..16777216, default4194304. Admission requires room for
the mean mode. Extension reduces achieved degree to fit its declared work
budget and returns a valid budget-limited record. Requested degrees outside
the supported degree range reject. Full-degree exact certificates are available
through dimension257. At s=1 the mean is the complete spectrum.
coefficient_order=1..32; max_terms=1..512, default64; transport chain<=4096;
exact operand text<=16384 characters; log range-reduction exponent<=65536.
The application-level request, resource and custody policies remain additional
constraints of the established consumer.

`counters`: new_source_modes, reused_source_modes,
source_projection_coordinates, basis_coordinates, basis_rebuilt_coordinates,
source_norm_coordinates, direct_energy_cuts, log_series_terms. Counts describe
actual scoped work in this call. Readout validation arithmetic is performed
but is not represented as source projection work. Every evaluated n-term
atanh series contributes n to log_series_terms; equal retained arguments share
a numerical node within a profile. Fresh exported records require no native
call; this is handled by the authenticated store.
