# SAM_cheat_sheet - Primitives, Constants, and Formula Surface

Status: constructive reference artifact, 2026-06-28.

Preflight: `artifacts/preflight_filled/PREFLIGHT_20260628_135221_no_script.md`.

Primary sources:

| Source | Use |
| --- | --- |
| `docs/SAM_UNIFICATION_NOTE_2026_06_28.md` | primitive cascade, compact matter laws, unification framing |
| `docs/SAM_PRIMITIVE_BASIS_2026_06_28.md` | primitive-basis statement and CR258 closure summary |
| `09a_PARTICLE_MASS_CHAIN/CR258_SUBSTRATE_PRIMITIVE_CLOSURE_AUDIT/CR258_result.md` | latest 09a primitive-closure audit |
| `09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_result.md` through `CR256_*` | current 09a 80-row stable matter closure |
| `09a_PARTICLE_MASS_CHAIN/CR257_A_MEETS_THETA_AT_D_1/CR257_result.md` | downstream $d=1$ A-Theta reduction, not a fourth row sector |
| `docs/SAM_RESULTS_COMPACT.md` | compact current formula map across distance, halo, neutrino, binding, and fate branches |
| `06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST/CR019_result.md` | current sub-percent CMB acoustic geometry readout |

## Primitive Basis

Current primitive coordinate statement:

$$
\hat h \perp \hat d \perp \pi,\qquad \hat h=2,\qquad \hat d=3.
$$

| Primitive axis | Value | Function |
| --- | ---: | --- |
| $\hat h$ | $2$ | binary horizon/split readout |
| $\hat d$ | $3$ | dimensional readout |
| $\pi$ | $\pi$ | route-completion normalization for accumulation |

Closure selector:

$$
\hat d^{\hat d-1}=\hat h^{\hat d}+1,\qquad 3^2=2^3+1.
$$

Rational SAM substrate quantities reduce to expressions in $(\hat h,\hat d)$. Accumulation quantities use the same rational basis with $\pi$ as the route-completion axis.

## Derived Substrate Constants

| Quantity | Formula | Value |
| --- | --- | ---: |
| split count | $S=\hat h^{\hat d}$ | $8$ |
| dimensional square | $\hat d^2$ | $9$ |
| face closure | $F=\hat d^{\hat d+1}$ | $81$ |
| write cell | $\mathcal{V}=\hat d^{\hat d}$ | $27$ |
| route radix | $R=\hat h^2\hat d$ | $12$ |
| route square | $R^2=\hat h^4\hat d^2$ | $144$ |
| tensor bridge | $\Theta=\hat h\hat d^2=R^2/\hat h^{\hat d}$ | $18$ |
| closed ledger | $\mathcal{L}=\hat hF$ | $162$ |
| matter capacity | $M=R^2-\Theta=\hat h\hat d^2(\hat h^3-1)$ | $126$ |
| accumulation floor | $A_0=1/(\pi R)=1/(12\pi)$ | $0.02652582385$ |
| route share | $A_{\mathrm{share}}=\pi A_0=1/R$ | $1/12$ |
| side share | $A_{\mathrm{side}}=A_{\mathrm{share}}/2$ | $1/24$ |

Ledger identities:

$$
R^2+\Theta=\mathcal{L}=162,\qquad R^2-\Theta=M=126,\qquad \mathcal{L}-M=2\Theta=36,\qquad M/R^2=7/8.
$$

## Section 4 and Matter-Law Constants

| Constant | Formula | Value |
| --- | --- | ---: |
| positive charged coefficient | $c_+=1+1/\hat h^2$ | $5/4$ |
| negative charged coefficient | $c_-=1+1/\hat h$ | $3/2$ |
| tensor share | $\hat h^{-\hat d}=\Theta/R^2$ | $1/8$ |
| retained share | $1-\hat h^{-\hat d}$ | $7/8$ |
| negative antimatter conjugate base | $c_+/c_-$ | $5/6$ |
| positive antimatter conjugate base | $c_-/c_+$ | $6/5$ |
| bigrade alphabet | $\{1,2,3,4,6,8,9,12\}$ | sum $45$ |
| lifted connector | $L_p=p+p^2/R^2$ | $L_6=25/4$ |

## Latest 09a Particle Data

Latest 09a test inspected: `CR258_SUBSTRATE_PRIMITIVE_CLOSURE_AUDIT`, with 36/36 named quantities reduced to the primitive basis.

Current 09a stable matter surface: 80 rows closed by CR254 through CR256 over the CR253 surface. This is not the broader catalog-capacity surface.

| Current 09a sector | Rows | Source |
| --- | ---: | --- |
| matter charged | $32$ | CR254 |
| matter neutral | $16$ | CR255 |
| anti charged | $32$ | CR256 |
| total current stable matter surface | $80$ | CR254-CR256 over CR253 |

CR253 selects the 80-row surface:

$$
\mathrm{promoted}(r)\iff \mathrm{bin}(r)\in\{\mathrm{stable\ matter},\mathrm{antimatter\ conjugate}\}\ \mathrm{and}\ h_T(r)\in\{0,1\}.
$$

The three compact closure laws are:

| Sector | Rows | Law | CR |
| --- | ---: | --- | --- |
| matter charged | $32$ | $q_A=R^d c_s p(1+p/R^2)$, with $c_s=c_-$ for negative and $c_s=c_+$ for positive | CR254 |
| matter neutral | $16$ | $q_A=(p/8)R^d$ | CR255 |
| anti charged | $32$ | $q_{A,\mathrm{anti}}=q_{A,\mathrm{matter}}(5/6\ \mathrm{or}\ 6/5)(1\pm p/R^{d+1})$ | CR256 |
| total | $80$ | fully closed by the three compact laws above | CR254-CR256 |

CR257 records the downstream $d=1$ A-Theta meeting:

| $d=1$ reduction | Formula |
| --- | --- |
| $d=1$ negative A-Theta meeting | $q_{A,\mathrm{anti}}=R(5/4)p(1+p/R^2)^2$ |
| $d=1$ positive A-Theta meeting | $q_{A,\mathrm{anti}}=R(3/2)p(1-p^2/R^4)$ |

## Formula Surface

| Topic | Native formula / current readout |
| --- | --- |
| Substrate constants from the SAM spine | $\hat h=2$, $\hat d=3$, $S=8$, $F=81$, $\mathcal{V}=27$, $R=12$, $\Theta=18$, $\mathcal{L}=162$, $M=126$, $A_0=1/(12\pi)$ |
| Horizon closure to accumulation floor | $A_{\mathrm{horizon}}=1$ projects to $A_0=A_{\mathrm{horizon}}/(4\pi \hat d)=1/(12\pi)=1/(\pi R)$ |
| Matter density | $\Omega_m=RA_0=1/\pi=0.3183098862$ |
| Baryon density | $\chi=(S/\hat d)A_0=2/(9\pi)$; $\Omega_b=2A_0(1-\chi)=0.04930$ |
| Pure SN distance channel | $A_{\mathrm{los}}(z)=(1/\pi)(1-(1+z)^{-3})$; $\mu_{\mathrm{native}}=\mu_{\mathrm{obs}}+5\log_{10}(1-A_{\mathrm{los}})$; CR018b uses 1580 SNe, no offset fit and no host-mass correction, residual $-0.00907$ mag |
| BAO distance / $r_d$ | $w=(\hat d/R)(\Omega_b/\Omega_{\mathrm{PBH}}/A)$; $r_{\mathrm{drag}}=r_\star(1+w)$; CR018b external BAO readout $r_d=147.769$ Mpc, Planck comparison $+0.461\%$, $\chi^2/n=1.7969$ for 12 DESI ratios |
| CMB acoustic geometry | CR019: $100\theta_\star=1.04740$ vs Planck $1.04110$ $(+0.605\%)$; $\ell_A=299.942$ vs $301.760$ $(-0.602\%)$; $r_d=147.769$ Mpc vs $147.090$ $(+0.461\%)$ |
| Periodic table / isotope workbook | $Z\rightarrow(N_{\mathrm{SOB}},A_{\mathrm{SOB}})\rightarrow P=Zp+Nn+Ze\rightarrow(G_{\mathrm{sub}},Q_{\mathrm{sub}},Q_{\mathrm{mass}},\chi)\rightarrow$ lane/support/binding/channel readouts over the SOB workbook surface |
| Carrier tensor scaffold | $[1,1,2,3,4,6,8,8,9,9,12,18,81]$; named carriers $(1,8,9,18,81)$ plus hidden support alphabet $(1,2,3,4,6,8,9,12)$ |
| Nuclear mass / substrate split | triadic lift $M_{\mathrm{obs}}/M_{\mathrm{native}}=(R+q+\hat d)/R=(15+q)/12$; pair lift $M_{\mathrm{obs}}/M_{\mathrm{native}}=1+(q+\hat d)/R^4$; Higgs reveal $R^2(1-2^{-\hat d})-\hat d^2/R=125.25$ GeV |
| Binding closure | $B_u^{(0)}=SA-(\Theta-1)A^{2/3}-(\hat d^2/R)Z(Z-1)/A^{1/3}-\hat h(R-1)(N-Z)^2/A+(S-1)\delta/\sqrt A-L_6\Lambda$; substrate form $8A-17A^{2/3}-(3/4)Z(Z-1)/A^{1/3}-22(N-Z)^2/A+7\delta/\sqrt A-(25/4)\Lambda$ |
| Galaxy radial halo law | $X(r)=V_{\mathrm{dark}}^2(r)/V_{\mathrm{bar}}^2(r)$ across 175 SPARC galaxies and 3391 points; CR031b $p=0.000999$ |
| Per-galaxy halo mass from $X_\infty$ | $X_{\infty,\mathrm{SAM}}=(R-\hat h)\Omega_m=10/\pi=3.1831$; $M_{\mathrm{halo}}(<R_{\mathrm{outer}})=R_{\mathrm{outer}}X_\infty V_{\mathrm{bar}}^2(R_{\mathrm{outer}})/G$; median ratio $0.9983$ in CR032 and $0.9993$ in CR033 |
| Native halo concentration / classes | $c_{\mathrm{SAM}}=1/\rho_{1/2}$; median $1.063$; classes over 175 galaxies: 94 late-saturating, 58 early-saturating, 15 rising-edge, 3 intermediate, 3 baryon-dominated inner-closure, 2 disturbed/non-closed |
| First neutrino selector | ratio selector $((\hat h\hat d)^2-1)/(\hat h-1)=35$ vs measured $33.895$; mass pattern $m_1:m_2:m_3=1:\sqrt2:6$; $\Sigma m_\nu=71.3$ meV |
| Black-hole / horizon bridge | $A(r_s)=1$ at the horizon, with photon sphere $A=2/3$ and ISCO $A=1/3$; the same closure projects to $A_0=1/(12\pi)$ |
| Big Bang acoustic / thermal clock | CR019 compressed clock values: $z_{\mathrm{eq}}=3596.43$, $z_\star=1091.22$, $z_d=1023.34$, $r_s(z_\star)=141.778$ Mpc, $D_M(z_\star)=13536.18$ Mpc |
| Fate identity | $\Omega_\Lambda=(\pi-1)/\pi$; $H_{\infty,\mathrm{native}}=H_0\sqrt{(\pi-1)/\pi}$; $H_{\infty,\mathrm{readout}}=H_0[(\pi-1)/\pi]^{3/2}$ |

## Compact Formula Block

```text
ĥ       = 2
d̂       = 3
S       = ĥ^d̂ = 8
F       = d̂^(d̂+1) = 81
V       = d̂^d̂ = 27
R       = ĥ^2 * d̂ = 12
Theta   = ĥ * d̂^2 = 18
L       = ĥ * F = 162
M       = R^2 - Theta = 126
A0      = 1 / (pi * R) = 1 / (12*pi)
Omega_m = R * A0 = 1/pi
chi     = (S/d̂) * A0 = 2/(9*pi)
Omega_b = 2*A0*(1-chi) ~= 0.04930
X_inf   = (R-ĥ) * Omega_m = 10/pi
H_inf,readout = H0 * ((pi-1)/pi)^(3/2)
```
