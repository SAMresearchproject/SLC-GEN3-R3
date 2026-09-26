# Branch06: positive local realization of the whole-road distance

This Codex-developed extension starts from the retained master-spine source
law q(u)=1−t+t/u³, t=1/pi, u=1+z, and D_n=q D_M. It preserves the
historical SN/BAO forward packets and their calibrations. The question is
whether this whole-road coordinate admits a positive local radial and volume
map at every past redshift, and what must travel with an observational ruler.

## Uniform radial positivity

Write H(u)^2=H0² sum_j Omega_j u^(p_j), with Omega_j>=0 and p_j<=4,
and H>0 for u>=1. Flat nonnegative radiation/matter/Lambda is the selected
physical background. For1<=v<=u, termwise comparison gives
H(u)/H(v)<=(u/v)². Consequently

    D_M/D_H=H(u) integral_1^u dv/H(v)<=u(u−1).

The exact derivative of the whole-road coordinate is

    dD_n/dz=J_r D_H,
    J_r=q+q' D_M/D_H, q'=−3t/u⁴.

Therefore, uniformly for allu>=1,

    J_r>=1−t−3t/u²+4t/u³
       =1−5t/4+t (u−2)²(u+4)/(4u³)
       >=1−5/(4pi)>0.

The bound is sharp over this background class: pure radiation attains equality
at u=2. It is an analytic all-redshift statement, not extrapolation of a grid.
Also J_r<=q<=1 and q>=1−t. Thus the radial coordinate transformation is
strictly increasing and its volume Jacobian obeys

    q² J_r >= (1−1/pi)²(1−5/(4pi)) >0.

The latter product lower bound need not be jointly sharp. The native operation
checks the exact polynomial factorization, encloses the constants with Arb,
and computes the source-packet profile at declared redshifts. Positive density
weights and the exponent bound are assumptions; arbitrary expansion histories
are not included. A radial derivative J_r is a coordinate stretch, not a new
physical light-speed assignment or a replacement of the existing c_eff floor.

## Local transport requires the accumulated distance

For z_a<z_b, let DeltaD=D_M(b)−D_M(a). Then

    D_n(b)−D_n(a)=q_b DeltaD+(q_b−q_a)D_M(a).

The last term carries prior distance information. Equivalently the affine
state(D_n,1) advances by

    T(b|a)=[[q_b/q_a,q_b DeltaD],[0,1]].

These maps compose exactly: T(c|b)T(b|a)=T(c|a), with the summed reference
increments. They invert on the positive q domain. The adapter verifies this
with rational source-compatible t=1/4 and arbitrary exact prefix increments;
this rational control tests the algebra, while physical t=1/pi is enclosed
separately. The nonzero omitted-memory term is retained explicitly.
The continuum form is dD_n=q dD_M+D_M dq. It realizes the declared whole-road
coordinate without substituting integral q dD_M as a different distance law.

## Matched radial/transverse ruler and covariance

An infinitesimal isotropic reference ruler r transforms as r_perp=q r and
r_parallel=J_r r, while D_n=q D_M and D_H,n=J_r D_H. Hence

    r_perp/D_n=r/D_M,
    r_parallel/D_H,n=r/D_H.

Transforming only distance would manufacture an observable change. An actual
physical mechanism changing a ruler is a separate source question. The
native exact two-channel control returns unchanged quadratic likelihood
r^T C^−1 r under y->S y,C->S C S^T with S=diag(q,J_r), and retains the
changed unmatched result. This is coordinate covariance, not a new fit or a
new data-derived covariance. Finite rulers use endpoint differences, whereas
this local Jacobian statement is differential.

## Native execution and arithmetic

`DistanceExpansionAdapter`, operation `GEN4_VOLI_DISTANCE_LOCAL_RETURN`,
uses the hash-bound inherited THERMAL_DISTANCE_SUMMARY.json background.
FLINT exact rationals and polynomials establish the algebraic identities;
Arb192 encloses pi-dependent universal constants. mpmath quadrature at40and65
digits returns paired source-packet profiles; precision agreement is a
numerical convergence diagnostic, not a certified quadrature enclosure.
No observational fit, new plasma evolution or external catalog is part of
this operation. Original ROOT and RH owner-pause remain unchanged.
