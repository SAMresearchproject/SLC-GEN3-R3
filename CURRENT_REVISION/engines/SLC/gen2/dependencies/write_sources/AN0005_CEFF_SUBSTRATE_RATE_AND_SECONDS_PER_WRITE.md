# A0, the substrate effective speed, and seconds per Write

Date: 2026-09-08. RH_PHYSICAL_WRITE_CLOCK1, continuing H001083.

Sean Brady directed the continuation toward **c_eff and its substrate A0
dependence**. The resulting clock map is

\[
\boxed{c_{\rm eff}=c(1-A),\qquad
\Delta t_W=\frac{R_H}{c}
\int_{\phi_0}^{\phi_0+\pi/2}\frac{d\phi_j}{(1-A)\mathcal D_j}.}
\]

Here R_H is the fixed native sphere radius, and
\(\mathcal D_j=R_H|\mathcal L_j|/\hbar\) is the completed H001083 local
geometric phase-action density. The explicit Codex continuation identifies
\(ds_{\rm native}/dt=c_{\rm eff}\) along the selected source phase path.
The resulting t is the time coordinate of that effective-speed readout.

For the active equatorial partner stroke with constant A,

\[
\boxed{\Delta t_W=\frac{\pi R_H}{2c(1-A)},\qquad
\nu_W=\frac{2c(1-A)}{\pi R_H}.}
\]

This supplies the time/radius and rate/radius coefficients. Selecting the
physical radius selects the numerical seconds per Write for this path.

## 1. Owner sources and the meaning of A

The supplied Time/Distance paper section 5.3 gives the effective-speed
relation. Its equations 20-21 give

\[
A=A_{\rm los}(z)=12A_0[1-(1+z)^{-3}],\quad
A_0=\frac1{12\pi},\quad C=12A_0=\frac1\pi,
\]
\[
D_{\rm native}=(1-A)D_{\rm readout}.
\]

The conceptual spine section 4.3 identifies c as the invariant substrate
tooth-rate. Thus A0 sets the amplitude of the effective-speed law through
the source accumulation A. The variable A in the numerical table below is
the global accumulation A_los. Its named A0 level has

\[
(1+z_{A_0})^3=\frac{12}{11},\qquad
\ln(1+z_{A_0})=\frac13\ln\frac{12}{11}.
\]

At z=0 the source law gives A_los=0. The A0 row is the separately named
accumulation level A_los=A0. The local source lift A_s=2GM/(c^2r) has its
own normalization and A_s=1 closure condition.

## 2. Direct native-path clock coefficients

The SI input c=299792458 m/s is retained from the supplied CR036 source.
All following coefficients were evaluated through the installed RH/R4
session. Numerical displays use rational enclosures of symbolic pi.

| Accumulation context | c_eff/c | c_eff (m/s) | ns per native metre | Quarter-Write ns per radius metre |
|---|---:|---:|---:|---:|
| Zero accumulation | 1.000000000000 | 299792458.000000 | 3.335640951982 | 5.239612554879 |
| Floor level A=A0 | 0.973474176151 | 291840216.067938 | 3.426532550837 | 5.382384744497 |
| z=1 | 0.721478849589 | 216293917.713354 | 4.623338513500 | 7.262323154536 |
| Saturation A=1/pi | 0.681690113816 | 204365554.815261 | 4.893192499607 | 7.686208804683 |

For example, the A0 equatorial law is

\[
\Delta t_W(A_0)=5.382384744497399\times10^{-9}
\left(\frac{R_H}{1\,\mathrm m}\right)\mathrm s.
\]

At fixed native radius and the same dimensionless stroke, the
floor-to-ceiling relation is exact:

\[
\frac{\Delta t_W(C)}{\Delta t_W(A_0)}
=\frac{1-A_0}{1-12A_0}
=\frac{12\pi-1}{12\pi-12}
\simeq 1.4280303563472.
\]

The logarithmic time span is

\[
\Delta\ln t_W=\ln\frac{12\pi-1}{12\pi-12}
\simeq 0.3562961216377.
\]

R4 retains the certified exact prime-log bounds

\[
\ln\frac{1218961}{853596}<\Delta\ln t_W
<\ln\frac{202469}{141782}.
\]

These correspond to the independently enclosed pi values
103993/33102 < pi < 104348/33215. The SI table uses the finer bracket
3.141592653589793238 < pi < 3.141592653589793239. Both enclosures and all
native rational endpoints are retained. Pi remains symbolic in the exact
formulas; decimal source constants retain their original source precision.

The accumulation span is ln(C/A0)=ln12. The time span uses the complement
1-A, so these are different source functions with different logarithms.

## 3. Joining the completed local action density

H001083's declared J4/X1 source construction gives

\[
C_a=-2B e^{i(\phi_a-\phi_p)},\quad
C_b=2B e^{i(\phi_b-\phi_p)},\quad E_B=6+\Re(C_a+C_b),
\]
\[
g=(-\Im C_a,-\Im C_b,\Im C_a+\Im C_b),\qquad
\mathcal D_j^2=\frac{(E_B^2+36)^2}{144(E_B^2+g_j^2)}.
\]

The geometric definition supplies
\(ds_{\rm native}/d\phi_j=R_H/\mathcal D_j\) for a positive pure-role stroke. Composing
it with the declared c_eff mapping gives

\[
\dot\phi_j=\frac{c(1-A)\mathcal D_j}{R_H},\qquad
\frac{dt}{d\phi_j}=\frac{R_H}{c(1-A)\mathcal D_j}.
\]

The new R4 calculation retains all nine completed native squared densities:
9/13, 9/10, 169/180, 1, 625/612, 625/576, 169/144, 289/225, 25/9.
For each named accumulation context and each certified pi endpoint it
computes the exact square

\[
\left(\frac1{R_H}\frac{dt}{d\phi_j}\right)^2
=\frac1{c^2(1-A)^2\mathcal D_j^2}.
\]

These are local differential values. A variable-density quarter uses the
full integral at the top of this note. The native grid is not a set of
continuous density extrema.

There is a source-defined equatorial case: fix phi_a=phi_b=0 and B=1,
and advance phi_p from 0 to pi/2. Then C_a+C_b=0 throughout the continuous
extension, E_B=6 and g_p=0; consequently \(\mathcal D_p=1\) throughout. This is
the H001083 partner quarter q000 to q001 and supplies the constant-density
case used in the table. The source's cancellation retains an active signed
interaction and the completed native Write.

## 4. Radius and mass conversion

If the fixed physical Home radius is assigned by the source closure law
R_H=2GM_H/c^2, the same equatorial map becomes

\[
\boxed{\Delta t_W=\frac{\pi G M_H}{c^3(1-A_{\rm los})}.}
\]

This composition keeps the local closure A_s=1 and the global readout
A_los as separate typed quantities. It gives

\[
\frac{\Delta t_W(A_0)}{M_H}
=7.994090348539402\times10^{-36}\ \mathrm{s/kg},
\]
\[
\frac{\Delta t_W(C)}{M_H}
=1.141580368909674\times10^{-35}\ \mathrm{s/kg}.
\]

The supplied CR036 cascade gives H0=67.25037519502037 km/s/Mpc and
c/H0=4457.855545498852 Mpc. If that cosmological reference length is
explicitly chosen as R_H, the A0 equatorial quarter is
7.403741982517747e17 s and the saturated quarter is
1.0572768301597827e18 s. These retain that specified cosmological radius
choice; the calculation does not identify it as the radius of a local Home.

R4's exact inverse gives the log-radius/log-duration basis (1,1).
Adding the local mass-radius law gives the log-mass/log-radius/log-duration
basis (1,1,1). These rational bases also span the real logarithmic scale
families by linearity. With A and the dimensionless path fixed,
(M_H,R_H,t_W) can all scale by the same positive factor. Thus c_eff has
supplied the conversion rate, while a selected physical length or mass
supplies the absolute time scale. No unique fundamental duration is
selected by the two dimensionless accumulation levels alone.

## 5. Readout consistency and activation

For the same transformed source/readout event, the paper's two relations
give exactly

\[
\frac{D_{\rm native}}{c_{\rm eff}}
=\frac{(1-A)D_{\rm readout}}{(1-A)c}
=\frac{D_{\rm readout}}c.
\]

The table instead compares a fixed native sphere and a fixed native path
while A changes. Its time ratio is therefore 1/(1-A). This states which
ruler is held fixed and prevents an implicit change in the sphere radius.

The completed activation readout remains
B=(|C_a|^2+|C_b|^2)/8. Fresh R4 boundary recovery preserves both existing
B alternatives at q000,E6 when only phase and scalar action are reported.
The effective-speed source equation adds no A-to-B evolution law.
The displayed per-Write rate applies to completed active strokes; it does
not assign the waiting time before activation. The physical identification
of interior spin/orbit/progression with the selected phase path remains
the motion input to this clock construction.

## 6. Execution, custody and result

RH-GEN2-R4-V1, SLC-GEN2-R4 and SLC-GEN2-CEV1-R4 were verified on generation
GEN2-REUSE-INFO1-20260907-G2-N72-RH1. The session is
RH_b09707b457d04d39ab47332bd60ca6ad.

There are 18 successful native calls across six operation names and 143
passing source/arithmetic/recovery checks. The 279-node high-precision
source DAG executes in eight exact R4 linear-inverse layers. Signed-log
and formal-log operations retain the normalized time range; boundary
operations carry activation, and a fresh consumer restores the complete
log graph exactly. Python compiles the equations, manages custody and
checks wiring; all source arithmetic outputs are native returned values.
Arb provides the explicitly identified pi enclosure and decimal displays.

The first general signed-log call was interrupted during full prime-factor
expansion, with no returned research result. Its input and source snapshot
are preserved. The successor uses the same arithmetic equations through
the installed exact readout inverse and keeps a separate, certified
prime-log enclosure. No installed engine or frozen predecessor was changed.

For this declared effective-speed Write-clock construction:
**The test result suggests the concept is possible.**

The useful new connection is c_eff(C)/c=(pi-1)/pi=Omega_Lambda from the
existing clean inventory account. Its reciprocal is the saturated clock
multiplier for a fixed native path. The efficient execution contribution
is to keep exact high-precision source equations in R4 inverse form while
using bounded prime-log representations for the requested logarithmic span.

Sources and executable record:

- [Owner Time/Distance paper](/home/sam/PycharmProjects/SAM_Research_Project/SAM_REVIEW/campaigns/RH_PHYSICAL_WRITE_CLOCK1/inputs/SAM_TIME_DISTANCE.pdf)
- [Conceptual spine sections 4.3 and 6](/home/sam/PycharmProjects/SAM_Research_Project/SAM_CONCEPTUAL_SPINE.md)
- [Volume I section V.9](/home/sam/PycharmProjects/SAM_Research_Project/volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md)
- [Completed H001083 density derivation](/home/sam/PycharmProjects/SAM_Research_Project/SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/DERIVATION.md)
- [Exact result and scale families](/home/sam/PycharmProjects/SAM_Research_Project/SAM_REVIEW/campaigns/RH_PHYSICAL_WRITE_CLOCK1/RESULT.json)
- [Native calculation receipts](/home/sam/PycharmProjects/SAM_Research_Project/SAM_REVIEW/campaigns/RH_PHYSICAL_WRITE_CLOCK1/CALCULATION_RECEIPTS.json)

Originator / conceptual director: Sean Brady.
AI research collaborators: OpenAI ChatGPT and Codex.
