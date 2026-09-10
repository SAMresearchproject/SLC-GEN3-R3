[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Recombination and Acoustic Geometry

## Conceptual abstract

The cosmic inventory does not directly emit an acoustic angle. It first
defines a background expansion and thermal clock. That clock sets the plasma
temperature and density, which determine an ionization history \(x_e\). The
ionization history sets Thomson and baryon-drag optical depths, those depths
locate the last-scattering and drag epochs, and only then can the sound horizon
and its angular projection be evaluated.

The complete dependency chain is

\[
(\Omega_m,\Omega_b,H_0,T_0,N_{\rm eff})
\longrightarrow
(H(a),T(a),n_H(a))
\longrightarrow
x_e(a)
\longrightarrow
(a_*,a_d)
\longrightarrow
(r_s,D_M)
\longrightarrow
(\theta_*,\ell_A,r_d).
\]

The route history is as important as the endpoint. [`CR:CR001@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) used a Saha
first approximation and a then-uncorrected optical-depth operator. It missed
two declared five-percent gates. [`CR:CR001b@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md) introduced Peebles
nonequilibrium transport and exposed two implementation defects: a net
\(3.4\ \mathrm{eV}\) Boltzmann factor that does not drive ordinary hydrogen
recombination and a factor \(1/(a^2H)\) incorrectly placed in proper-time
optical depth. [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) corrected the net factor to
\(13.6\ \mathrm{eV}\), corrected optical depth to \(1/(aH)\), kept the
substrate identities, comparison inputs, gates and controls fixed, and
recovered all three registered acoustic gates.

The conceptual firewall is exact: proper-time optical depth contains
\(1/(aH)\), while conformal-distance and sound-horizon integrals contain
\(1/(a^2H)\). Exchanging the two is an implementation error, not a physical
alternative. The corrected native-recombination result has the registered
classification **The test result suggests strong contact with the concept.**
The remaining native-recombination and precision-nucleosynthesis work stays
explicitly open.

## 1. Opening question and conceptual picture

This chapter asks:

> Given the registered baryon and matter inventories, can the early-universe
> background be carried through hydrogen recombination, optical-depth epoch
> selection and acoustic geometry from start to finish, with the Saha failure,
> Peebles appeal, implementation defects, corrected retest and precision
> boundaries all remaining visible?

There are four conceptual stages.

1. **Background.** Expansion dilutes matter and radiation differently, while
   the thermal clock cools as \(T=T_0/a\).
2. **Plasma transport.** The free-electron fraction evolves from an ionized
   state toward neutral hydrogen. Saha gives instantaneous equilibrium;
   Peebles transport describes nonequilibrium freeze-out with Lyman-
   \(\alpha\) trapping and two-photon decay.
3. **Epoch selection.** Thomson and drag optical depths integrate scattering
   along proper time and select \(a_*\) and \(a_d\) by unit depth.
4. **Geometry.** The sound horizon integrates a conformal-distance speed;
   the radial comoving distance projects that ruler into \(\theta_*\),
   \(\ell_A\), and \(r_d\).

Each stage consumes the previous output. Repairing a late acoustic ratio by
altering an unrelated matter-binding rule reverses that dependency order; the
preserved failed audit [`CR:CR019b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr019b-theta-star-lift-rule-audit/README.md) is the evidence for that distinction.

## 2. Definitions, domains, units and assumptions

| Symbol | Definition or role | Type | Units/domain |
|---|---|---|---|
| \(a\) | \(1/(1+z)\), with \(a=1\) today | scale factor | positive, dimensionless |
| \(H(a)\) | \(\dot a/a\) | background expansion rate | s\(^{-1}\) |
| \(E(a)\) | \(H(a)/H_0\) | normalized expansion | dimensionless |
| \(T(a)\) | \(T_0/a\) | photon thermal clock | K |
| \(\Omega_\gamma\) | present photon energy density divided by present critical energy density | photon fraction | dimensionless |
| \(\Omega_r\) | \(\Omega_\gamma(1+0.2271N_{\rm eff})\) | declared radiation fraction | dimensionless |
| \(\Omega_{\Lambda,\rm bg}\) | \(1-\Omega_m-\Omega_r\) | explicit-radiation closure term | dimensionless |
| \(n_H\) | hydrogen-number density in the H-only runner | plasma density | m\(^{-3}\) |
| \(x_e\) | \(n_e/n_H\) | free-electron fraction | dimensionless, \(0\le x_e\le1\) in the runner |
| \(\alpha_B\) | case-B recombination coefficient | plasma rate coefficient | m\(^3\) s\(^{-1}\) |
| \(\beta_2,\beta_{\rm eff}\) | \(n=2\) and net photoionization-rate functions | plasma rates | s\(^{-1}\) |
| \(C\) | Peebles escape/two-photon correction | probability-like rate modifier | dimensionless |
| \(\tau(a)\) | Thomson optical depth from \(a\) to today | proper-time scattering integral | dimensionless |
| \(\tau_d(a)\) | baryon-drag optical depth | drag integral | dimensionless |
| \(a_*,z_*\) | \(\tau(a_*)=1\), \(z_*=a_*^{-1}-1\) | registered last-scattering criterion | dimensionless |
| \(a_d,z_d\) | \(\tau_d(a_d)=1\), \(z_d=a_d^{-1}-1\) | registered drag criterion | dimensionless |
| \(R_b(a)\) | \(3\rho_b/(4\rho_\gamma)\) | baryon-loading ratio | dimensionless |
| \(c_s(a)\) | \(c/\sqrt{3(1+R_b)}\) | photon-baryon sound speed | m s\(^{-1}\) |
| \(r_s(a)\) | comoving sound horizon | ruler | m or Mpc |
| \(D_M(z)\) | flat comoving radial distance | projection distance | m or Mpc |
| \(\theta_*\) | \(r_s(a_*)/D_M(z_*)\) | compressed acoustic angle | dimensionless/radians |
| \(\ell_A\) | \(\pi/\theta_*\) | acoustic multipole scale | dimensionless |
| \(r_d\) | \(r_s(a_d)\) | drag sound horizon | Mpc |

The corrected registered runner is hydrogen-only: it treats all baryons as
hydrogen in \(n_H\) and does not implement the later H+He refinements of a
precision recombination code. Its BBN lane is schematic. Those are exact
scope boundaries, not hidden corrections to the equations it did execute.

## 3. Construct the expansion background and thermal clock

### 3.1 Derive the scale-factor powers

Nonrelativistic matter dilutes with physical volume:

\[
\rho_m(a)=\rho_{m,0}a^{-3}.
\]

Radiation has the same volume dilution plus one factor from redshifting photon
energy:

\[
\rho_r(a)=\rho_{r,0}a^{-4}.
\]

For a flat matter-radiation-complement adapter, divide the Friedmann relation
by \(H_0^2\):

\[
E(a)^2
=\frac{H(a)^2}{H_0^2}
=\Omega_ra^{-4}+\Omega_ma^{-3}+\Omega_{\Lambda,\rm bg}.
\]

The expanding branch uses the positive root,

\[
\boxed{
H(a)=H_0
\sqrt{\Omega_ra^{-4}+\Omega_ma^{-3}+\Omega_{\Lambda,\rm bg}}
}.
\]

In redshift coordinates, \(a^{-1}=1+z\), so

\[
\boxed{
E(z)=
\sqrt{\Omega_r(1+z)^4+\Omega_m(1+z)^3+\Omega_{\Lambda,\rm bg}}
}.
\]

The clean complement from `SAMA-D000018` is
\(1-\Omega_m\). Once explicit radiation is placed in the numerical
background, flat closure instead requires

\[
\boxed{
\Omega_{\Lambda,\rm bg}=1-\Omega_m-\Omega_r
}.
\]

This is a bookkeeping refinement of the background adapter, not a replacement
of the clean inventory.

### 3.2 Build photon and radiation density with correct physical type

The blackbody photon energy density is

\[
u_\gamma(T_0)
=\frac{\pi^2}{15}
\frac{(k_BT_0)^4}{\hbar^3c^3}.
\]

Critical density in the Friedmann equation is a mass density, so convert
energy density using \(\rho_{\gamma,0}=u_\gamma/c^2\). With

\[
\rho_{c,0}=\frac{3H_0^2}{8\pi G},
\]

the photon fraction is

\[
\Omega_\gamma=\frac{\rho_{\gamma,0}}{\rho_{c,0}}.
\]

The registered radiation adapter includes standard effective relativistic
content:

\[
\boxed{
\Omega_r=\Omega_\gamma(1+0.2271N_{\rm eff})
}.
\]

This correctly typed reconstruction is why the reported-only defective E5 row
of [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) is not propagated from `SAMA-D000019`.

### 3.3 Derive matter-radiation equality

Equality occurs when

\[
\Omega_ra_{\rm eq}^{-4}
=\Omega_ma_{\rm eq}^{-3}.
\]

Multiply both sides by \(a_{\rm eq}^4\):

\[
\Omega_r=\Omega_ma_{\rm eq}.
\]

Divide by \(\Omega_m>0\):

\[
a_{\rm eq}=\frac{\Omega_r}{\Omega_m}.
\]

Since \(1+z=a^{-1}\),

\[
\boxed{
1+z_{\rm eq}=\frac{\Omega_m}{\Omega_r}
=\frac{\omega_m}{\omega_r}
}.
\]

Multiplication by the common \(h^2\) gives the second form without changing
the ratio.

### 3.4 Derive the thermal and number-density clocks

Adiabatic photon redshift gives

\[
\boxed{T(a)=\frac{T_0}{a}=T_0(1+z)}.
\]

The registered H-only transport uses

\[
\boxed{
n_H(a)=\frac{\Omega_b\rho_{c,0}}{m_pa^3}
}.
\]

The \(a^{-3}\) factor follows number dilution. These two functions provide the
temperature and collision density consumed by the ionization equations.

### 3.5 Preserve the declared-premises baryon-value inconsistency

The declared-premises JSON files for CR001, CR001b and CR001c each carry the
stale literal

\[
\Omega_b^{\rm declared}
=0.04929890833649833.
\]

The runners and their executable summaries instead recompute the registered
formula

\[
\Omega_b
=2A_0(1-\chi)
=0.049299011266100756.
\]

Their signed difference, declared minus executable, is

\[
0.04929890833649833
-0.049299011266100756
=-1.0292960242463955\times10^{-7}.
\]

The runner and executable summary are the numerical authority for the
executed background, acoustic outputs and controls. The three stale
declared-premises literals remain preserved as a source-documentation defect;
they are not silently rewritten and are not substituted into the replay in
this chapter. This inconsistency is distinct from both the net-Boltzmann and
optical-depth implementation defects described below.

## 4. From Saha equilibrium to Peebles transport

### 4.1 Derive the Saha initial condition

For the source runner's hydrogen equilibrium, define

\[
S_{\rm H}(T,n_H)
=\frac1{n_H}
\left(\frac{m_ek_BT}{2\pi\hbar^2}\right)^{3/2}
\exp\!\left(-\frac{13.6\ \mathrm{eV}}{k_BT}\right).
\]

The equilibrium relation is

\[
\frac{x_e^2}{1-x_e}=S_{\rm H}.
\]

Multiply by \(1-x_e\):

\[
x_e^2=S_{\rm H}(1-x_e)
=S_{\rm H}-S_{\rm H}x_e.
\]

Bring every term to the left:

\[
x_e^2+S_{\rm H}x_e-S_{\rm H}=0.
\]

The quadratic formula gives

\[
x_e
=\frac{-S_{\rm H}\pm\sqrt{S_{\rm H}^2+4S_{\rm H}}}{2}.
\]

The negative branch is unphysical. The source runner therefore uses

\[
\boxed{
x_e^{\rm Saha}
=\frac{-S_{\rm H}+\sqrt{S_{\rm H}^2+4S_{\rm H}}}{2}
}.
\]

Saha supplies instantaneous equilibrium. It does not encode delayed escape
and nonequilibrium freeze-out, so the first test treated it only as an initial
approximation.

### 4.2 Define the case-B recombination rate

The registered Peebles execution uses the Pequignot--Petitjean fit

\[
\alpha_B(T)
=4.309\times10^{-19}
\frac{t^{-0.6166}}{1+0.6703t^{0.5300}}
\ \mathrm{m^3\,s^{-1}},
\qquad
t=\frac{T}{10^4\ \mathrm K}.
\]

Multiplying \(\alpha_Bn_H\) gives s\(^{-1}\), so the recombination term
\(\alpha_Bn_Hx_e^2\) has the correct rate dimension.

### 4.3 Keep the two photoionization rates in their proper roles

The raw \(n=2\) rate used inside the Peebles \(C\)-factor is

\[
\beta_2(T)
=\alpha_B(T)
\left(\frac{m_ek_BT}{2\pi\hbar^2}\right)^{3/2}
\exp\!\left(-\frac{3.4\ \mathrm{eV}}{k_BT}\right).
\]

The corrected net rate driving the ODE toward ordinary hydrogen equilibrium
is

\[
\boxed{
\beta_{\rm eff}(T)
=\alpha_B(T)
\left(\frac{m_ek_BT}{2\pi\hbar^2}\right)^{3/2}
\exp\!\left(-\frac{13.6\ \mathrm{eV}}{k_BT}\right)
}.
\]

The distinction is load-bearing. The \(3.4\ \mathrm{eV}\) factor belongs to
the \(n=2\) photoionization channel inside \(C\). Used alone as the net ODE
factor, it drives the wrong equilibrium and leaves \(x_e\) essentially one.
The additional \(10.2\ \mathrm{eV}\) Lyman-\(\alpha\) energy makes the net
factor \(13.6\ \mathrm{eV}\).

### 4.4 Construct the Peebles \(C\)-factor

Define the Sobolev escape factor

\[
K_\alpha(z)=\frac{\lambda_\alpha^3}{8\pi H(z)},
\]

with \(\lambda_\alpha=1.215682\times10^{-7}\ \mathrm m\), and let
\(\Lambda_{2\gamma}=8.227\ \mathrm{s^{-1}}\). The source \(C\)-factor is

\[
\boxed{
C(z)=
\frac{1+K_\alpha\Lambda_{2\gamma}n_H(1-x_e)}
{1+K_\alpha(\Lambda_{2\gamma}+\beta_2)n_H(1-x_e)}
}.
\]

The numerator includes the two-photon escape channel; the denominator includes
that channel plus reionization from \(n=2\). The factors combine to delay
effective recombination relative to instantaneous Saha equilibrium.

### 4.5 Write the nonequilibrium ODE and its execution domain

The corrected source ODE is

\[
\boxed{
\frac{dx_e}{dz}
=\frac{C(z)}{H(z)(1+z)}
\left[
\alpha_B(T)n_H(z)x_e^2
-\beta_{\rm eff}(T)(1-x_e)
\right]
}.
\]

The bracket has units s\(^{-1}\), while \(H^{-1}\) has seconds, leaving a
dimensionless derivative with respect to dimensionless redshift. The source
sets \(x_e\) from Saha at \(z=1800\), integrates down to \(z=10\) with an
automatic stiff solver, uses \(x_e=1\) above the integration interval and
freezes the terminal value below it. Free-electron density is then

\[
n_e(a)=x_e(a)n_H(a).
\]

This is an executable construction with explicit interpolation and endpoint
conventions, not a claim of an all-species recombination theorem.

## 5. Derive the optical-depth and conformal-distance firewall

### 5.1 Thomson depth follows proper time

Over proper time \(dt\), the differential scattering depth is

\[
d\tau=n_e\sigma_Tc\,dt.
\]

From \(H=\dot a/a\),

\[
\dot a=aH.
\]

Therefore

\[
dt=\frac{da}{\dot a}=\frac{da}{aH(a)}.
\]

Substitute into \(d\tau\):

\[
d\tau
=\frac{n_e(a)\sigma_Tc}{aH(a)}\,da.
\]

Integrating from an earlier scale factor \(a\) to today gives

\[
\boxed{
\tau(a)
=\int_a^1
\frac{n_e(a')\sigma_Tc}{a'H(a')}\,da'
}.
\]

The registered operational last-scattering scale factor solves

\[
\tau(a_*)=1,
\qquad
z_*=a_*^{-1}-1.
\]

### 5.2 Drag depth adds the baryon-loading weight

The source drag operator is

\[
\boxed{
\tau_d(a)
=\int_a^1
\frac{n_e(a')\sigma_Tc}
{a'H(a')R_b(a')}\,da'
}.
\]

It selects

\[
\tau_d(a_d)=1,
\qquad
z_d=a_d^{-1}-1.
\]

The additional \(1/R_b\) changes the epoch selected by the same ionization
history; it does not change the proper-time factor \(1/(aH)\).

### 5.3 Conformal distance carries one additional factor of \(a^{-1}\)

Conformal time is defined by

\[
d\eta_{\rm conf}=\frac{dt}{a}.
\]

Insert \(dt=da/(aH)\):

\[
d\eta_{\rm conf}
=\frac{da}{a^2H(a)}.
\]

Therefore distance and sound-horizon integrals correctly contain
\(1/(a^2H)\). The two operators can be compared directly:

| Operator | Time variable | Scale-factor denominator |
|---|---|---|
| Thomson or drag optical depth | proper time \(dt\) | \(aH\) |
| comoving distance or sound horizon | conformal time \(dt/a\) | \(a^2H\) |

Using \(1/(a^2H)\) in optical depth multiplies the high-redshift integrand by
an erroneous factor \(1/a\). This pushes the unit-depth crossing to larger
\(a\), hence much lower redshift. The distinction is a derivation firewall,
not an adjustable convention.

## 6. Acoustic background and parameter-free baryon-ruler route

“Parameter-free” in this preserved source route means no catalog parameter is
fitted to make the three acoustic gates pass. It does not mean the calculation
has no declared external inputs. The exact [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) numerical packet
uses the source's precommitted BAO-side
\(H_0=68.76\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\), FIRAS
\(T_0=2.7255\ \mathrm K\), and \(N_{\rm eff}=3.046\). The later
\(H_{0,\rm SAM}=67.2503751950\) cascade from `SAMA-D000019` is a distinct
registered route and is not substituted backward into this sealed test.

### 6.1 Derive baryon loading

Matter and photons scale as

\[
\rho_b(a)=\rho_{b,0}a^{-3},
\qquad
\rho_\gamma(a)=\rho_{\gamma,0}a^{-4}.
\]

Thus

\[
R_b(a)
=\frac{3\rho_b(a)}{4\rho_\gamma(a)}
=\frac{3\rho_{b,0}a^{-3}}
{4\rho_{\gamma,0}a^{-4}}.
\]

Cancel \(a^{-3}\), leaving one factor \(a\):

\[
\boxed{
R_b(a)=\frac{3\Omega_b}{4\Omega_\gamma}a
}.
\]

The sound speed of the tightly coupled photon-baryon fluid is

\[
\boxed{
c_s(a)=\frac{c}{\sqrt{3[1+R_b(a)]}}
}.
\]

At early times \(R_b\to0\), so \(c_s\to c/\sqrt3\). Increasing baryon
loading lowers the sound speed, as the denominator requires.

### 6.2 Integrate the sound horizon

Physical propagation over \(dt\) contributes \(c_s\,dt\). A comoving length
divides physical length by \(a\), so

\[
dr_s=\frac{c_s\,dt}{a}.
\]

Using \(dt=da/(aH)\),

\[
dr_s=\frac{c_s(a)}{a^2H(a)}\,da.
\]

Integrating from the early limit to \(a\),

\[
\boxed{
r_s(a)=\int_0^a
\frac{c_s(a')}{a'^2H(a')}\,da'
}.
\]

The last-scattering ruler is \(r_s(a_*)\); the drag ruler is

\[
\boxed{r_d=r_s(a_d)}.
\]

### 6.3 Integrate comoving radial distance

For a flat background, a photon satisfies \(d\chi=c\,dt/a\). Therefore

\[
D_M(z_*)
=c\int_{a_*}^{1}\frac{da}{a^2H(a)}.
\]

Using \(dz=-da/a^2\), the same relation is

\[
\boxed{
D_M(z_*)=c\int_0^{z_*}\frac{dz}{H(z)}
}.
\]

The equality of the two forms is a coordinate transformation; it is not a
second independent physical road.

### 6.4 Form the angular and multipole observables

The angle subtended by the comoving ruler is

\[
\boxed{
\theta_*=\frac{r_s(a_*)}{D_M(z_*)}
}.
\]

The conventional reported scale is \(100\theta_*\). The corresponding
acoustic multipole is

\[
\boxed{
\ell_A=\frac\pi{\theta_*}
}.
\]

The inverse relation means a positive shift in \(\theta_*\) creates a negative
shift in \(\ell_A\). This shared dependence is why the two gates are not
independent diagnoses of a recombination error, even though both are reported.

## 7. Native recombination failure, correction and retest

### 7.1 CR001: preserve the first failed execution

[`CR:CR001@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) kept the substrate densities and the declared external
background inputs fixed, derived \(z_*\) and \(z_d\) with a Saha-first route,
and applied the then-precommitted optical-depth operator. It recorded

| Observable | CR001 value | Declared comparator | Relative difference | Source gate |
|---|---:|---:|---:|---|
| \(z_*\) | \(995.1869\) | \(1089.9200\) | \(-8.692\%\) | evidence |
| \(z_d\) | \(985.6676\) | \(1059.9400\) | \(-7.007\%\) | evidence |
| \(r_s(a_*)\) | \(150.3915\ \mathrm{Mpc}\) | \(144.4300\ \mathrm{Mpc}\) | \(+4.128\%\) | evidence |
| \(D_M(z_*)\) | \(13516.8028\ \mathrm{Mpc}\) | \(13869.6000\ \mathrm{Mpc}\) | \(-2.544\%\) | evidence |
| \(100\theta_*\) | \(1.1126\) | \(1.0411\) | \(+6.870\%\) | failed \(5\%\) gate |
| \(\ell_A\) | \(282.3583\) | \(301.7600\) | \(-6.430\%\) | failed \(5\%\) gate |
| \(r_d\) | \(151.3119\ \mathrm{Mpc}\) | \(147.0900\ \mathrm{Mpc}\) | \(+2.870\%\) | passed \(5\%\) gate |

The artifact's source verdict is `FAIL`. Its original root-cause discussion
emphasized the Saha approximation. The subsequent appeal discovered that the
optical-depth \(a\)-power was also wrong, so the preserved first diagnosis is
not treated as the final causal separation.

### 7.2 CR001b: implement Peebles transport and expose both defects

The first Peebles precommit placed the \(3.4\ \mathrm{eV}\) factor in the net
photoionization term. Executed literally, that equation held
\(x_e\approx1\), produced no recombination crossing, and crashed. The runner
documented a departure: it used the corrected \(13.6\ \mathrm{eV}\) net
factor so that the plasma would recombine, while preserving the precommitted
\(1/(a^2H)\) optical-depth formula to expose its effect.

With that improper optical-depth power still present,
[`CR:CR001b@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md) recorded

\[
z_*=227.3151,
\qquad
z_d=427.1521,
\]

\[
r_s(a_*)=328.2601\ \mathrm{Mpc},
\qquad
r_d=244.1354\ \mathrm{Mpc},
\]

\[
100\theta_*=2.5221,
\qquad
\ell_A=124.5623.
\]

All three five-percent gates failed. This extreme displacement is exactly
what the extra factor \(1/a\) predicts: at recombination \(a\sim10^{-3}\),
the wrong integrand amplifies early optical depth by roughly three orders of
magnitude relative to the proper-time form before integration and weighting.
The source failure therefore became useful localization evidence.

### 7.3 CR001c: encode both corrections before the retest

The corrected precommit made both changes explicit:

\[
\exp\!\left(-\frac{3.4\ \mathrm{eV}}{k_BT}\right)
\quad\longrightarrow\quad
\exp\!\left(-\frac{13.6\ \mathrm{eV}}{k_BT}\right)
\]

in the net ODE rate, while retaining the \(3.4\ \mathrm{eV}\) rate only
inside the declared \(C\)-factor, and

\[
\frac1{a^2H}
\quad\longrightarrow\quad
\frac1{aH}
\]

in Thomson and drag optical depths. The substrate identities, external
inputs, five-percent gates, evidence set and random-density controls remained
unchanged.

[`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) then emitted

| Observable | Corrected SAM | Declared comparator | Relative difference |
|---|---:|---:|---:|
| \(z_*\) | \(1073.0632\) | \(1089.9200\) | \(-1.547\%\) |
| \(z_d\) | \(1055.8115\) | \(1059.9400\) | \(-0.390\%\) |
| \(r_s(a_*)\) | \(143.2991\ \mathrm{Mpc}\) | \(144.4300\ \mathrm{Mpc}\) | \(-0.783\%\) |
| \(D_M(z_*)\) | \(13532.7423\ \mathrm{Mpc}\) | \(13869.6000\ \mathrm{Mpc}\) | \(-2.429\%\) |
| \(100\theta_*\) | \(1.0589\) | \(1.0411\) | \(+1.710\%\) |
| \(\ell_A\) | \(296.6827\) | \(301.7600\) | \(-1.683\%\) |
| \(r_d\) | \(144.8064\ \mathrm{Mpc}\) | \(147.0900\ \mathrm{Mpc}\) | \(-1.552\%\) |

All three registered gates passed. The correction did not erase the two
failed predecessors; it supplied a new artifact with explicit successor and
correction relationships.

### 7.4 Preserve the random-density controls

For the corrected route, the canonical absolute \(100\theta_*\) deviation was
\(0.01710\). In \(1000\) random \(\Omega_m\in[0.05,0.95]\) trials, \(77\)
were at least as close, placing the canonical row at the \(7.70\)th
percentile of that null. In \(1000\) random
\((\Omega_m,\Omega_b)\) trials, \(164\) were at least as close, a
\(16.40\)th-percentile result.

These controls test whether broad random density choices commonly reproduce
the same compressed angle. They do not convert the acoustic comparison into a
uniqueness theorem, and they are not used to fit the canonical densities.

## 8. Acoustic lift failure and BBN boundary

### 8.1 CR019b rejects the wrong operator before native recombination

Before the Branch 19 native transport, [`CR:CR019b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr019b-theta-star-lift-rule-audit/README.md) tested whether the
static binding-work lift could repair a \(+0.605\%\) compressed-angle
residual from a conventional Hu--Sugiyama/Eisenstein--Hu route. No declared
lift candidate passed the joint \(\theta_*,\ell_A,r_d\) gate.

One candidate reduced the angle residual to \(+0.030\%\) but moved \(r_d\)
to \(+3.59\%\), outside the declared joint tolerance. A brute-force
two-density grid found a numerical optimum, but it was correctly retained as
diagnostic rather than mislabeled as a substrate lift. The forbidden
\(\Theta\)-lift control worsened the packet. The source `FAIL` therefore
localized the missing operator to dynamic recombination rather than static
binding work and directly motivated the later plasma route.

### 8.2 G396 and CR021 retain scoped light-element contact

[`G:G396`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) records a scoped BBN compatibility result with

\[
\omega_b=0.0223687835029,
\qquad
\eta_{10}=6.12680980144,
\]

and a native helium contact value \(0.229944122806\) against the source's
\(0.247\) comparator. Its own boundary excludes native precision D/H, Li/H,
weak freeze-out, neutron lifetime and a full nuclear network.

[`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) retains that row inside a source `BOUNDARY` packet. It explicitly
does not establish a full Planck likelihood, full recombination,
perturbation, TT/TE/EE, or theorem-level CMB closure. The CR001c runner's
separate schematic Wagoner estimate \(Y_p\approx0.3938\) overshoots its
declared comparator and remains evidence only. These two helium-related
numbers come from different declared approximations and are not averaged or
substituted for one another.

## 9. Deviation, failure, correction and control ledger

| Route or control | Observed consequence | Preserved resolution or boundary |
|---|---|---|
| Use Saha as the complete recombination history | CR001 misses the \(100\theta_*\) and \(\ell_A\) gates; its initial causal account is later refined. | Preserve CR001 and introduce nonequilibrium Peebles transport. |
| Use \(3.4\ \mathrm{eV}\) as the net ODE Boltzmann factor | \(x_e\) remains essentially one; no recombination crossing exists. | Use \(13.6\ \mathrm{eV}\) in \(\beta_{\rm eff}\); retain \(3.4\ \mathrm{eV}\) only inside \(C\). |
| Use \(1/(a^2H)\) in optical depth | Unit-depth crossing shifts to \(z_*\approx227\), and all CR001b gates fail dramatically. | Derive \(dt=da/(aH)\) and use \(1/(aH)\). |
| Remove \(1/(a^2H)\) from sound horizon or comoving distance | Deletes the conformal-time factor and changes the ruler/road. | Keep \(d\eta_{\rm conf}=da/(a^2H)\). |
| Repair acoustic geometry with the binding-work lift | One ratio can improve while the joint \(r_d\) packet fails. | Preserve CR019b and route work to recombination dynamics. |
| Count the brute-force density optimum as a substrate operator | Converts a diagnostic fit into a derived law. | Keep it diagnostic only. |
| Lift \(\Theta=18\) | Violates the carrier type and worsens the acoustic packet. | Keep the tensor carrier exempt from matter-lift rules. |
| Erase CR001 or CR001b after CR001c | Removes the evidence that isolated the two implementation defects. | Retain all three artifacts and their correction relations. |
| Replace CR001c's \(H_0=68.76\) with the later CR036 value | Alters a sealed test's input and numerical outputs post hoc. | Keep source chronology; run a separately registered successor if desired. |
| Infer full CMB shape from \(\theta_*,\ell_A,r_d\) | Exceeds compressed acoustic geometry. | Route full spectra to `SAMA-D000021`. |
| Infer precision BBN from G396 or the schematic Wagoner lane | Exceeds each source's declared network and species scope. | Keep full nucleosynthesis explicitly open. |
| Treat source `PASS`/`FAIL` as owner approval | Conflates evidence with review. | Maintain false/null approval state. |

## 10. Connections across SAM

Upstream, `SAMA-D000012` supplies the distinction between a compressed
ruler-road ratio and a native recombination calculation. Its two drag-ruler
packets retain their own dependency graphs and are not exchanged here.
`SAMA-D000018` supplies the clean \(\Omega_m\) and \(\Omega_b\). `SAMA-D000019`
supplies the later eta-to-Hubble cascade and the type distinction between
substrate quantities and external adapters.

Downstream, `SAMA-D000021` uses a standard recombination engine and the fixed
cosmic density/perturbation packet to test full CMB shape. That lane answers a
different question from this native Peebles lane. The two can coexist:

| Lane | Recombination operator | Question |
|---|---|---|
| Native thermal lane | source-built hydrogen-only Peebles transport with corrected optical depth | Can the fixed inventory generate acoustic epochs and compressed geometry through explicit plasma transport? |
| Full-shape lane | standard recombination inside the declared Boltzmann engine | Can the fixed SAM cosmic packet reproduce spectral shape through an established computational adapter? |

Volume II may receive matter as a source-side inventory but owns particle and
isotope grammar. Volume III may execute Boltzmann or exact-state computation
but does not rewrite the Volume I plasma and inventory definitions.

## 11. Established result, exact boundary and forward handoff

The compression-safe technical route is

\[
\boxed{
\begin{aligned}
H(a)&=H_0\sqrt{\Omega_ra^{-4}+\Omega_ma^{-3}
+\Omega_{\Lambda,\rm bg}},\\
T(a)&=T_0/a,\\
\frac{dx_e}{dz}
&=\frac{C}{H(1+z)}
\left[\alpha_Bn_Hx_e^2-\beta_{\rm eff}(1-x_e)\right],\\
\tau(a)&=\int_a^1\frac{n_e\sigma_Tc}{aH}\,da,\\
\tau_d(a)&=\int_a^1\frac{n_e\sigma_Tc}{aHR_b}\,da,\\
r_s(a)&=\int_0^a\frac{c_s}{a^2H}\,da,\\
D_M(z_*)&=c\int_{a_*}^1\frac{da}{a^2H},\\
\theta_*&=r_s(a_*)/D_M(z_*),
\qquad
\ell_A=\pi/\theta_*,
\qquad
r_d=r_s(a_d).
\end{aligned}
}.
\]

For the corrected [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) lane, the exact registered classification is:

**The test result suggests strong contact with the concept.**

That classification belongs to the corrected retest only. It does not erase
the source `FAIL` records of [`CR:CR001@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) and [`CR:CR001b@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md), classify the
failed CR019b lift, or turn G396/CR021 into precision BBN. The remaining open
work is specific: refine hydrogen-only native recombination, incorporate
helium and fuller atomic transport, replace the schematic light-element lane
with a full nucleosynthesis network, and test any altered background in a new
registered successor rather than changing the sealed CR001c packet.

The corrected acoustic packet hands \(z_*,z_d,r_s,D_M,\theta_*,\ell_A,r_d\)
forward to the Volume I synthesis. Full TT/TE/EE shape and perturbation
selection continue in `SAMA-D000021` under their own evidence keys.

## 12. Focused test and result index

| Exact qualified key | Role | Preserved outcome or boundary | Direct result | Test folder |
|---|---|---|---|---|
| [`G:G396`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | scoped BBN premise | Source verdict `G396_PASS_TOE_G23_SCOPED_BBN_COMPATIBILITY__PRECISION_LIGHT_ELEMENTS_OPEN`; precision network remains open. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G396_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`CR:CR001@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) | preserved failure | Source `CLEAN`/`FAIL`; Saha-first and then-current optical-depth route misses two acoustic gates while \(r_d\) passes. | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN) |
| [`CR:CR001b@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md) | correction-stage failure | Source `FAIL`; exposes the net-Boltzmann and optical-depth defects, preserves the latter in execution, and fails all three gates. | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL) |
| [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) | corrected retest | Source `CLEAN`/`PASS`; corrected \(13.6\ \mathrm{eV}\) net factor and \(1/(aH)\) depth recover all three gates. **The test result suggests strong contact with the concept.** | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL) |
| [`CR:CR019b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr019b-theta-star-lift-rule-audit/README.md) | preserved wrong-operator failure | Audit-informative source `FAIL`; binding lift cannot close the joint acoustic packet and future work is localized to recombination. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_result.md) | [folder](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT) |
| [`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) | boundary result | Source `CLEAN`/`BOUNDARY`; Planck-lite and scoped BBN contact only, with full likelihood, recombination, perturbation and TT/TE/EE closure excluded. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT) |

## 13. Atomic SAMA source-record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000072-R001` | Supplies the earlier compressed acoustic ruler-road ratio and its limited scope. |
| `SAMA-C000073-R001` | Preserves distinct ruler packets and the failed lift-rule audit. |
| `SAMA-C000092-R001` | Supplies the clean cosmic inventory identities. |
| `SAMA-C000097-R001` | Supplies the photon-density dimensional conversion. |
| `SAMA-C000098-R001` | Supplies the distinct eta-to-Hubble cascade result and chronology boundary. |
| `SAMA-C000099-R001` | Declares external thermal, SI/CODATA and radiation inputs. |
| `SAMA-C000100-R001` | Defines the cosmological background and thermal clock. |
| `SAMA-C000101-R001` | Defines sound horizon, comoving distance and acoustic readouts. |
| `SAMA-C000102-R001` | Enforces the \(1/(aH)\) versus \(1/(a^2H)\) firewall. |
| `SAMA-C000103-R001` | Preserves the CR001 Saha-first failure. |
| `SAMA-C000104-R001` | Preserves the CR001b appeal and two surfaced implementation defects. |
| `SAMA-C000105-R001` | Records the corrected CR001c retest and exact classification. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Enforces status, classification and approval typing. |

## 14. Sources and external references

- Sean Brady and SAM collaborators, [Volume I technical spine, V.3 and V.5--V.8](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md).
- P. J. E. Peebles, [Recombination of the Primeval Plasma](https://doi.org/10.1086/149628), for the effective-atom lineage named by the registered source.
- S. Seager, D. D. Sasselov, and D. Scott, [How Exactly Did the Universe Become Neutral?](https://doi.org/10.1086/313388), for precision-recombination context and the H+He boundary.
- D. J. Fixsen, [The Temperature of the Cosmic Microwave Background](https://doi.org/10.1088/0004-637X/707/2/916), for the external thermal anchor.
- Planck Collaboration, [Planck 2018 results VI: cosmological parameters](https://doi.org/10.1051/0004-6361/201833910), for the source-declared compressed comparators.
- W. Hu and N. Sugiyama, [Small-Scale Cosmological Perturbations: An Analytic Approach](https://doi.org/10.1086/177989), and D. J. Eisenstein and W. Hu, [Baryonic Features in the Matter Transfer Function](https://doi.org/10.1086/305424), for the conventional fitting-formula lane distinguished from native transport.

These external works provide the established plasma, thermal and comparator
context named by the source artifacts. They do not replace the registered
substrate inventory or erase the preserved execution history.

## 15. Revision, hash and approval boundary

This is registered document `SAMA-D000020`, revision \(1\). The document
catalog and generated manifests bind this exact file to its computed SHA-256.
The primary spine hash is fixed above; every evidence key resolves to an
artifact hash and pinned source location through the permanent registry.
Hashes establish custody and exact revision identity, not approval.

All fifteen assigned atomic records and all six exact test keys appear
individually above. The only SAMA classification stated is the registered
classification for [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md), reproduced verbatim. Source verdict tokens
for the other rows remain historical metadata. `reviewed_and_approved`
remains `false`; `approval` remains `null` until Sean Brady explicitly
approves this exact revision.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G396`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G396_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G396_output.json)<br>[G396_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G396_output.json) | [G396_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G396_output.json)<br>[G396_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G396_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`CR:CR001@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) | [CR001_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_PRECOMMIT.md)<br>[CR001_declared_premises.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_declared_premises.json) | [CR001_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_runner.py) | [CR001_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_runner.py)<br>[CR001_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_result.md)<br>[CR001_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_summary.json) | [CR001_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_result.md)<br>[CR001_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN/CR001_summary.json) | [All 8 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001-sam-derived-thermal-ladder-cmb-and-bbn/README.md) |
| [`CR:CR001b@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md) | [CR001b_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_PRECOMMIT.md)<br>[CR001b_declared_premises.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_declared_premises.json) | [CR001b_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_runner.py) | [CR001b_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_runner.py)<br>[CR001b_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_result.md)<br>[CR001b_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_summary.json) | [CR001b_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_result.md)<br>[CR001b_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001b_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL/CR001b_summary.json) | [All 8 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001b-peebles-nonequilibrium-recombination-appeal/README.md) |
| [`CR:CR001c@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) | [CR001c_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_PRECOMMIT.md)<br>[CR001c_declared_premises.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_declared_premises.json) | [CR001c_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_runner.py) | [CR001c_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_runner.py)<br>[CR001c_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_result.md)<br>[CR001c_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_summary.json) | [CR001c_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_result.md)<br>[CR001c_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL/CR001c_summary.json) | [All 8 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr001c-peebles-plus-corrected-optical-depth-appeal/README.md) |
| [`CR:CR019b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr019b-theta-star-lift-rule-audit/README.md) | [CR019b_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_PRECOMMIT.md) | [CR019b_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_runner.py) | [CR019b_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_runner.py)<br>[CR019b_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_result.md)<br>[CR019b_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_summary.json) | [CR019b_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_result.md)<br>[CR019b_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019b_THETA_STAR_LIFT_RULE_AUDIT/CR019b_summary.json) | [All 6 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr019b-theta-star-lift-rule-audit/README.md) |
| [`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) | [CR021_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_PRECOMMIT.md)<br>[CR021_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_declared_premises.json) | [CR021_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_runner.py) | [CR021_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_runner.py)<br>[CR021_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md)<br>[CR021_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_summary.json) | [CR021_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md)<br>[CR021_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) |
| [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | [CR036_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_PRECOMMIT.md) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py)<br>[CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [All 7 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000020`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RECOMBINATION_AND_ACOUSTIC_GEOMETRY.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000020 | Early-Universe Cosmology | Thermal Clock, Peebles Recombination, Optical Depth and Acoustic Geometry |

| Document field | Value |
|---|---|
| Purpose | Carry the fixed cosmic inventory through the radiation background, thermal clock, Saha and Peebles ionization histories, corrected Thomson and drag optical depths, sound horizon and compressed acoustic observables while retaining every material failure and correction. |
| Prerequisite documents | `SAMA-D000012`, `SAMA-D000019` |
| Used by | `SAMA-D000021`; focused child of `SAMA-P000002`. |
| Primary theory source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), V.3 and V.5--V.8; SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`; all six qualified keys below resolve there. |
| Revision state | Source-bound revision 1; `reviewed_and_approved: false`; `approval: null`. |

</details>
