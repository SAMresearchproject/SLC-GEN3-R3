[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Cosmic Inventory from the Accumulation Floor

## Conceptual abstract

The accumulation floor enters cosmology through a typed inventory operator.
The construction begins with the binary horizon state count \(S=2^D\),
distributes that count equally over \(D\) relabeling-symmetric directions, and
scales the resulting quotient measure by the universal floor \(A_0\). This
produces

\[
\chi=\frac{S}{D}A_0=\frac{2}{9\pi}.
\]

The quotient is then consumed by the baryonic split while the route radix
closes the clean total matter account:

\[
\Omega_b=\alpha_HA_0(1-\chi),
\qquad
\Omega_m=RA_0=\frac1\pi.
\]

These equations yield the clean inventory. A later directional-cumulant
operator emits a distinct effective readout,

\[
\Omega_{m,\mathrm{eff}}
=RA_0-2A_0(\chi+D\chi^2),
\]

without replacing the clean identity. The distinction is central: equal units
do not make a universal inventory and an application-specific response
interchangeable. The evidence history is also part of the construction. The
original \(\chi\) account overstated three algebraic rewrites as independent
paths; the corrected combinatorial, Monte Carlo and symmetry-quotient records
retain the exact value while correcting its provenance. The later locked-stack
replay keeps the \(18\)-unit tensor carrier outside the matter and rest-mass
table.

## 1. Opening question and conceptual picture

This chapter asks:

> Starting only from the registered Volume I primitive packet, can the cosmic
> baryon, matter, complementary and effective inventories be reconstructed
> from first relation to numerical endpoint while preserving the distinction
> between a clean identity, a directional refinement, a carrier and matter?

The conceptual picture is a fork after a common beginning:

\[
(\alpha_H,D,R,A_0)
\longrightarrow
S=2^D
\longrightarrow
\mu_H=\frac{S}{D}
\longrightarrow
\chi=A_0\mu_H.
\]

From \(\chi\), one branch constructs the clean ledger,

\[
\chi
\longrightarrow
(\Omega_b,\Omega_m,\Omega_c,\Omega_\Lambda),
\]

while a second branch applies a declared directional second-order response,

\[
\chi
\longrightarrow
K_{ij}=\chi^2\delta_{ij}
\longrightarrow
\operatorname{tr}K=D\chi^2
\longrightarrow
\Omega_{m,\mathrm{eff}}.
\]

The branches share primitives, not type. The clean branch answers how the
closed cosmic substrate account partitions. The effective branch answers how
one declared response operator refines the matter readout. Neither is a
replacement for the other.

## 2. Definitions, domains and type firewall

| Symbol | Exact definition | Type | Domain/units |
|---|---|---|---|
| \(\alpha_H\) | \(2\) | primitive distinction arity | positive integer, dimensionless |
| \(D\) | \(3\) | spatial support dimension | positive integer, dimensionless |
| \(S\) | \(2^D=8\) | binary horizon state count | positive integer, dimensionless |
| \(R\) | \(\alpha_H^2D=12\) | route radix | positive integer, dimensionless |
| \(A_0\) | \(1/(\pi R)=1/(12\pi)\) | universal accumulation floor | dimensionless amplitude |
| \(\Theta\) | \(\alpha_HD^2=18\) | first overflow; tensor carrier | dimensionless count, not rest mass |
| \(M\) | \(R^2-\Theta=126\) | retained matter-side capacity | dimensionless count |
| \(\mu_H\) | \(S/D=8/3\) | direction-additive horizon quotient measure | dimensionless |
| \(\chi\) | \(A_0\mu_H\) | horizon-quotient bias/readout | dimensionless |
| \(\Omega_b\) | \(\alpha_HA_0(1-\chi)\) | clean baryon inventory | dimensionless fraction |
| \(\Omega_m\) | \(RA_0\) | clean total matter inventory | dimensionless fraction |
| \(\Omega_c\) | \(\Omega_m-\Omega_b\) | clean nonbaryonic remainder | dimensionless fraction |
| \(\Omega_\Lambda\) | \(1-\Omega_m\) | clean complementary inventory | dimensionless fraction |
| \(K_{ij}\) | \(\chi^2\delta_{ij}\) | directional second-cumulant kernel | \(D\times D\), dimensionless |
| \(\Omega_{m,\mathrm{eff}}\) | \(RA_0-2A_0(\chi+D\chi^2)\) | application-specific effective matter readout | dimensionless fraction |

Three firewalls govern every later substitution.

1. The numerical equality \(A_0R=1/\pi\) appears in both a cosmic
   inventory and a line-of-sight road. The operators are different, so the
   objects remain differently typed.
2. \(\Theta=18\) is a tensor carrier. It is not added to the \(126\) retained
   matter rows and is not promoted to rest mass.
3. \(\Omega_{m,\mathrm{eff}}\) is an emitted response of its declared
   directional operator. It does not overwrite \(\Omega_m=1/\pi\).

## 3. Derive the horizon quotient from binary state allocation

### 3.1 Construct the finite state space

For \(D\) binary directions, the horizon state space is

\[
\mathcal H_D=\{0,1\}^D.
\]

Each of the \(D\) coordinates has two states. The multiplication principle
therefore gives

\[
|\mathcal H_D|
=\underbrace{2\cdot2\cdots2}_{D\ \mathrm{factors}}
=2^D
=S.
\]

At \(D=3\),

\[
S=2^3=8.
\]

The use of \(2^D\) is a premise of the binary face-state construction. It is
not replaceable by \(3^D\) merely because the spatial support has three
directions.

### 3.2 Impose direction additivity and relabeling symmetry

Let \(\mu_i\) be the measure allocated to direction \(i\), where
\(i\in\{1,\ldots,D\}\). Direction additivity requires

\[
\sum_{i=1}^{D}\mu_i=S.
\]

Relabeling symmetry under the permutation group \(S_D\) makes every direction
equivalent, so

\[
\mu_1=\mu_2=\cdots=\mu_D=\mu_H.
\]

Substituting this equality into the additive constraint gives

\[
\underbrace{\mu_H+\cdots+\mu_H}_{D\ \mathrm{terms}}
=D\mu_H=S.
\]

Since \(D>0\), division by \(D\) yields the unique symmetric allocation

\[
\boxed{\mu_H=\frac{S}{D}=\frac{2^D}{D}}.
\]

At \(D=3\), this is \(\mu_H=8/3\). [`G:G305`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) makes the scope explicit:
the result follows inside the binary-state, additive-allocation and
direction-relabeling axioms. It is not the orbit count of binary strings under
\(S_D\), which is \(D+1=4\) at \(D=3\), and it is not the active-incidence
count \(2^{D-1}=4\).

### 3.3 Scale the quotient by the universal floor

The horizon quotient readout is defined by

\[
\chi=A_0\mu_H.
\]

Insert the two source identities:

\[
\chi
=\frac1{12\pi}\frac83.
\]

Multiply numerators and denominators:

\[
\chi
=\frac{8}{36\pi}.
\]

Divide numerator and denominator by \(4\):

\[
\boxed{\chi=\frac2{9\pi}}
=0.0707355302630646\ldots.
\]

This is a derived identity conditional on the registered primitives and the
explicit quotient axioms. No observed cosmic density is used to select its
value.

## 4. Chi correction chain and its wrong controls

### 4.1 Preserve the overextended first account

[`G:G219`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) recorded three verbal routes to \(\chi\): face-state cycle,
Born-rule bias and saturation coherence. Its numerical endpoint was correct,
but its claim that the paths were independent was overextended. Algebraically,
the three expressions reduce to the same relation:

\[
\frac{2^D}{D}A_0,
\]

\[
\alpha_H\frac{2^{D-1}}D A_0
=2\frac{2^{D-1}}D A_0
=\frac{2^D}{D}A_0,
\]

and

\[
\frac{2^D\alpha_H/D}{\alpha_H}A_0
=\frac{2^D}{D}A_0.
\]

Calling these three independent calculations would count algebraic rewriting
as new evidence. The source record remains visible because it explains why a
correction was needed.

### 4.2 Correct the provenance without changing the value

[`G:G219B`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) replaces the independence claim with two properly distinguished
operations:

1. direct enumeration of \(2^D\) binary configurations followed by equal
   direction allocation; and
2. numerical sampling of that declared finite structure.

The direct route gives \(0.07073553026306459\). The reported Monte Carlo route
gives \(0.07073553026306460\) at \(D=3\). The correction therefore changes the
evidential account, not the exact endpoint.

### 4.3 Retest stochastic behavior and make the controls bite

[`G:G219C`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) used \(200{,}000\) samples per run, ten seeds and three directions.
Its grand mean equals the closed form, the maximum directional deviation is
\(1.6795267466836183\times10^{-4}\), and the empirical/theoretical standard-
deviation ratio is \(1.1391418333\). Different seeds produced different
direction-level samples, which confirms that the Monte Carlo output was not a
hard-coded repetition of the closed form.

The wrong controls change load-bearing premises and therefore change the
endpoint:

| Control | Emitted value | Shift from registered \(\chi\) | Meaning |
|---|---:|---:|---|
| Replace \(2^D\) by \(3^D\) | \(0.238732414638\) | \(+0.167996884375\) | Binary state count is load-bearing. |
| Replace \(D=3\) by \(D=2\) while retaining the control's declared scaling | \(0.0530516476973\) | \(-0.0176838825658\) | Spatial support is load-bearing. |
| Replace \(D=3\) by \(D=4\) | \(0.106103295395\) | \(+0.0353677651315\) | The registered dimension is not decorative. |
| Increase \(A_0\) by ten percent | \(0.0778090832894\) | \(+0.00707355302631\) | The floor scales the quotient linearly. |
| Decrease \(A_0\) by ten percent | \(0.0636619772368\) | \(-0.00707355302631\) | The opposite linear response is recovered. |

[`G:G305`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) adds structural wrong controls. The no-quotient candidate \(8\), the
ternary candidate \(9\), active incidence \(4\), orbit count \(4\), and
\(2^D/(D-1)=4\) all fail the additive symmetric-allocation relation. Defining
\(\mu_H=\chi_{\rm target}/A_0\) reproduces the number but is rejected as
circular.

## 5. Clean cosmic inventory and effective branch

### 5.1 Derive the baryon inventory

The clean baryon relation is

\[
\Omega_b=\alpha_HA_0(1-\chi).
\]

Insert \(\alpha_H=2\), \(A_0=1/(12\pi)\), and
\(\chi=2/(9\pi)\):

\[
\Omega_b
=2\frac1{12\pi}\left(1-\frac2{9\pi}\right).
\]

Combine the leading factor:

\[
\Omega_b
=\frac1{6\pi}\left(1-\frac2{9\pi}\right).
\]

Write the parenthesis over a common denominator:

\[
1-\frac2{9\pi}
=\frac{9\pi-2}{9\pi}.
\]

Therefore

\[
\boxed{
\Omega_b=\frac{9\pi-2}{54\pi^2}
}
=0.0492990112661008\ldots.
\]

The factor \(1-\chi\) is load-bearing. Removing it changes the baryon split,
as the [`CR:CR281@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr281-cosmic-budget-typed-readout-promotion/README.md) wrong-control ledger records.

### 5.2 Derive clean total matter

The clean matter identity consumes the route radix once:

\[
\Omega_m=RA_0.
\]

Substitute \(R=12\) and \(A_0=1/(12\pi)\):

\[
\Omega_m
=12\frac1{12\pi}
=\frac{12}{12}\frac1\pi
=\boxed{\frac1\pi}
=0.318309886183791\ldots.
\]

The same cancellation can be exposed through the horizon projection. From

\[
A_0=\frac{A_H}{4\pi D},
\qquad
R=\alpha_H^2D=2\alpha_HD
\quad\text{for the locked }\alpha_H=2,
\]

one obtains

\[
RA_0
=\frac{2\alpha_HD}{4\pi D}A_H
=\frac{\alpha_HA_H}{2\pi}.
\]

At \(A_H=1\) and \(\alpha_H=2\), this again gives \(1/\pi\). The
cancellation of \(D\) explains the closed form; it does not erase the
dimensional premise used to build \(R\) and \(A_0\).

### 5.3 Derive the clean remainder and complement

The clean nonbaryonic remainder is

\[
\Omega_c=\Omega_m-\Omega_b.
\]

Using a common denominator \(54\pi^2\),

\[
\Omega_c
=\frac{54\pi}{54\pi^2}
-\frac{9\pi-2}{54\pi^2}
=\boxed{\frac{45\pi+2}{54\pi^2}}
=0.269010874917690\ldots.
\]

The clean complement is

\[
\boxed{
\Omega_\Lambda=1-\Omega_m
=1-\frac1\pi
=\frac{\pi-1}{\pi}
}
=0.681690113816209\ldots.
\]

This is the clean matter/complement ledger. When an explicit radiation term
is inserted into a background-expansion adapter, closure instead uses
\(\Omega_{\Lambda,\mathrm{bg}}=1-\Omega_m-\Omega_r\). The additional
subtraction is radiation bookkeeping, not a revision of the clean identity.

### 5.4 Derive the directional second-order term

The effective branch begins with an isotropic diagonal kernel

\[
K_{ij}=\chi^2\delta_{ij},
\qquad i,j\in\{1,\ldots,D\}.
\]

For \(i\ne j\), \(\delta_{ij}=0\), so mixed direction cumulants vanish.
For \(i=j\), \(\delta_{ii}=1\), so every diagonal entry equals \(\chi^2\).
Taking the trace gives

\[
\operatorname{tr}K
=\sum_{i=1}^{D}K_{ii}
=\sum_{i=1}^{D}\chi^2
=\boxed{D\chi^2}.
\]

At \(D=3\),

\[
\chi^2
=\left(\frac2{9\pi}\right)^2
=\frac4{81\pi^2}
=0.005003515241596928\ldots,
\]

and

\[
D\chi^2
=\frac4{27\pi^2}
=0.0150105457247908\ldots.
\]

The coefficient \(D\) comes from the diagonal trace. At \(D=3\), the false
friend \(\binom D2\) also equals \(3\), but the two functions separate away
from three dimensions: for \(D=4\), the trace coefficient is \(4\) whereas
\(\binom42=6\). [`G:G313`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) uses that grid to reject the accidental equality,
along with \(D^2\), a hard-coded coefficient \(3\), and the target-fitted
coefficient \(3.027192735\ldots\).

### 5.5 Construct the effective readout without overwriting the clean ledger

The registered effective operator is

\[
\Omega_{m,\mathrm{eff}}
=RA_0-2A_0(\chi+D\chi^2).
\]

Separate its steps. First form the directional response:

\[
\chi+D\chi^2
=0.0707355302630646
+0.0150105457247908
=0.0857460759878554\ldots.
\]

Then apply the two-face floor weight:

\[
2A_0(\chi+D\chi^2)
=\frac1{6\pi}(\chi+D\chi^2)
=0.00454897061473347\ldots.
\]

Finally subtract that emitted response from the clean total:

\[
\boxed{
\Omega_{m,\mathrm{eff}}
=\frac1\pi-2A_0(\chi+D\chi^2)
=0.313760915569057\ldots
}.
\]

Its associated effective split is

\[
\Omega_{\mathrm{trapped,eff}}
=\Omega_{m,\mathrm{eff}}-\Omega_b
=0.264461904302956\ldots,
\]

\[
\Omega_{\mathrm{vacuum,eff}}
=1-\Omega_{m,\mathrm{eff}}
=0.686239084430943\ldots.
\]

These are effective-branch readouts. The clean \(\Omega_c\) and
\(\Omega_\Lambda\) above remain unchanged in the clean branch.

## 6. Residual localization, candidate selection and structural correction

[`G:G310`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) held \(\Omega_b\) fixed and asked which side of the matter-to-baryon
ratio carried the residual. The clean ratio was \(5.45671947589\), while the
declared target implied \(\Omega_m\approx0.313753697401\) if \(\Omega_b\)
remained fixed. Fitting \(\chi\) instead would require
\(\chi\approx0.0572411734205\) and would move the otherwise clean baryon row.
The test therefore localized the response to the total-matter side rather
than rewriting the horizon quotient.

[`G:G312`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) scanned the coefficient of the \(\chi^2\) term. The target-implied
coefficient \(3.027192735\ldots\) was close to \(D=3\), but an exact fitted
noninteger coefficient was rejected as a derivation. The integer \(D\) route
emitted \(\Omega_{m,\mathrm{eff}}=0.3137609155690572\) and preserved
\(\Omega_b\). The source correctly held this as candidate-grade until the
directional trace was supplied.

[`G:G313`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) then constructed \(K_{ij}=\chi^2\delta_{ij}\), recovered
\(\operatorname{tr}K=D\chi^2\), verified zero mixed terms and rejected the
dimension-three false friends. The source retained a narrower open item: the
local second-order kernel itself was not derived there from a path integral.
This is why the effective readout is used only through its declared operator.

## 7. Locked-stack inventory replay and typed promotion

### 7.1 First focused derivations

[`CR:CR018@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr018-a0-chi-baryon-inventory-derivation/README.md) replayed \(A_0\), \(\mu_H\), \(\chi\) and \(\Omega_b\). It
records all four identities, the corrected G219B route, the G219C sampling
retest and the G305 wrong controls as passing source conditions.

[`CR:CR019@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr019-effective-matter-inventory-refinement/README.md) then replayed the effective branch. It retained
\(\Omega_b=0.049299011266101\), emitted
\(\Omega_{m,\mathrm{eff}}=0.313760915569057\), and verified that the
directional coefficient is \(D=3\).

### 7.2 Boundary verdict

[`CR:CR023@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr023-baryon-cosmology-branch-verdict/README.md) preserved the branch as a source `BOUNDARY` result. Its boundary
was explicit: the inventory and scoped acoustic contacts did not constitute
full recombination, perturbation, TT/TE/EE, Planck-likelihood, or distance-
triad closure. Later tests may close some separately registered questions;
they do not retroactively change this artifact's source field.

### 7.3 Typed-readout promotion and implementation correction

[`CR:CR281@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr281-cosmic-budget-typed-readout-promotion/README.md) placed the clean structural inventory and physical-density
cascade in one typed contract. Its first execution failed because the runner
looked for `free_parameters_total` in `CR114_summary.json` instead of the
precommitted `CR114_cosmic_baryon_bridge.json`. The lookup was corrected
without changing the verdict tree or equations. The corrected execution
retained seven wrong-control rejections, including the clean/effective
separation, the ban on treating a Planck comparator as input, the distinction
between \(\Omega_b\) and \(\omega_b\), and the requirement that the dimensional
factor \(K\) have a source.

### 7.4 Last Campaign replay and carrier firewall

[`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) restarted from the locked packet

\[
\alpha_H=2,
\qquad R=12,
\qquad D=3,
\qquad \text{carrier side}=\frac18,
\qquad \text{retained side}=\frac78.
\]

It recovered the baryon and effective-matter readouts, passed \(58/58\)
matter-inventory checks, retained all \(126/126\) matter rows, and rejected
\(10/10\) wrong controls. Its most important cross-volume guard is that
\(\Theta=18\) remains carrier-only. The null-conjugate boundary row with
native value \(18\), surface debit \(18\), observed mass \(0\) and charge
readout \(0\) is not promoted into matter. Volume I may consume the replayed
inventory; the particle-row grammar remains Volume II.

## 8. Deviation chain and control ledger

| Deviation or wrong control | What it changes or exposes | Preserved resolution |
|---|---|---|
| Count G219's three algebraic rewrites as independent paths | Inflates evidential independence without changing the arithmetic. | Preserve G219; replace the account with G219B, G219C and G305. |
| Use \(3^D\) rather than \(2^D\) | Emits \(\chi\approx0.2387324\) and shifts \(\Omega_b\). | Retain the binary state-space premise. |
| Use an orbit count or active incidence as \(\mu_H\) | Emits \(4\), not the unique equal additive allocation \(8/3\). | Enforce the stated observable and symmetry axioms. |
| Define \(\mu_H=\chi_{\rm target}/A_0\) | Reproduces the endpoint circularly. | Derive the quotient before any comparator is consulted. |
| Fit \(\chi\) to repair the matter ratio | Damages the baryon row and changes an upstream identity. | Localize the response to the effective matter operator. |
| Use exact fitted coefficient \(3.027192735\ldots\) | Turns a comparator-derived number into a structural coefficient. | Use the diagonal trace \(D\chi^2\). |
| Use \(\binom D2\), \(D^2\), or hard-coded \(3\) | Agrees accidentally or counts mixed pairs not present in the diagonal kernel. | Check the \(D\)-grid and zero off-diagonal terms. |
| Substitute \(\Omega_{m,\mathrm{eff}}\) for \(\Omega_m\) globally | Rewrites a universal clean identity with an application response. | Carry both symbols and operators explicitly. |
| Count \(\Theta=18\) as matter or rest mass | Mixes transport support with retained matter rows. | Preserve the carrier-only type and the \(126\)-row ledger. |
| Remove the first failed CR281 execution | Erases a source-path implementation fault. | Retain it and document the corrected lookup. |
| Read source `PASS` or `BOUNDARY` as SAMA approval | Conflates evidence status with owner review. | Keep this exact revision false/null until explicit owner approval. |

## 9. Established result, exact boundary and forward handoff

The clean inventory established by the registered source chain is

\[
\boxed{
\begin{aligned}
\chi&=\frac2{9\pi},\\
\Omega_b&=\frac{9\pi-2}{54\pi^2},\\
\Omega_m&=\frac1\pi,\\
\Omega_c&=\frac{45\pi+2}{54\pi^2},\\
\Omega_\Lambda&=\frac{\pi-1}{\pi}.
\end{aligned}
}
\]

The separate directional readout is

\[
\boxed{
K_{ij}=\chi^2\delta_{ij},
\qquad
\Omega_{m,\mathrm{eff}}
=RA_0-2A_0(\chi+D\chi^2)
=0.313760915569057\ldots
}.
\]

No new chapter-level SAMA result classification is assigned: the registered
crosswalk contains no authorized classification for these twelve rows. Their
source `PASS`, `FAIL`, `BOUNDARY` and internal verdict strings remain
historical evidence metadata.

What remains specifically open here is the deeper derivation of the local
second-order kernel from the upstream path-integral construction and every
application outside the declared effective operator. The clean/effective
separation and carrier firewall are not open substitutions. `SAMA-D000019`
now consumes \(\Omega_b\), \(\chi\), the closed containers and \(A_0\) to
derive the baryon-to-photon and dimensional Hubble cascade. Volume II receives
the \(126\)-row matter side without receiving the \(18\)-unit carrier as mass.

## 10. Focused test and result index

| Exact qualified key | Role | Preserved outcome or boundary | Direct result | Test folder |
|---|---|---|---|---|
| [`G:G219`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | preserved failure predecessor | Exact \(\chi\) value with overextended independence account; no registry classification added. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219_summary_md.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G219B`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | correction | Reframes the route as direct combinatorics plus sampling; \(3^D\) control rejected. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219B_summary.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G219C`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | stochastic retest | Ten-seed Monte Carlo confirmation and five biting wrong controls. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219C_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G305`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | symmetry premise | Unique \(2^D/D\) additive allocation inside explicit axioms; seven wrong controls. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G305_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G310`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | residual localization | Holds \(\Omega_b\) fixed and localizes the tested ratio residual to the matter side. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G310_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G312`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | candidate/control | Selects the \(D\chi^2\) candidate while rejecting target-fit uniqueness and theorem-grade overstatement. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G312_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G313`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | structural construction | Derives \(D\chi^2\) as a diagonal trace; rejects false-friend coefficients. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G313_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`CR:CR018@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr018-a0-chi-baryon-inventory-derivation/README.md) | inventory construction | Source `CLEAN`/`PASS`; exact \(A_0,\mu_H,\chi,\Omega_b\) packet. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION) |
| [`CR:CR019@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr019-effective-matter-inventory-refinement/README.md) | effective result | Source `CLEAN`/`PASS`; effective split with \(D=3\) and unchanged baryon row. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT) |
| [`CR:CR023@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr023-baryon-cosmology-branch-verdict/README.md) | branch boundary | Source `CLEAN`/`BOUNDARY`; exact full-CMB and full-recombination exclusions retained. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT) |
| [`CR:CR281@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr281-cosmic-budget-typed-readout-promotion/README.md) | typed promotion result | Clean/effective contract, dimensional handoff, seven wrong controls and preserved lookup correction. | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | locked-stack retest | Replays both inventory lanes, \(58/58\) matter checks, \(126/126\) rows and \(10/10\) rejected controls while preserving the carrier firewall. | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY) |

## 11. Atomic SAMA source-record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000001-R001` | Defines the universal accumulation floor \(A_0\). |
| `SAMA-C000030-R001` | Supplies the locked R12 route radix. |
| `SAMA-C000031-R001` | Types \(\Theta18\) as first overflow and tensor carrier. |
| `SAMA-C000032-R001` | Supplies the \(18/126/144/162\) sector and carrier split. |
| `SAMA-C000091-R001` | Defines the horizon-quotient identity \(\chi=2/(9\pi)\). |
| `SAMA-C000092-R001` | Defines the clean cosmic inventory and its distinction from the road. |
| `SAMA-C000093-R001` | Separates clean \(\Omega_m\) from \(\Omega_{m,\mathrm{eff}}\). |
| `SAMA-C000094-R001` | Preserves the \(\chi\) and effective-inventory correction chain. |
| `SAMA-C000095-R001` | Records typed promotion and the carrier-safe locked replay. |
| `SAMA-C000122-R001` | Enforces the Volume I, Volume II and Volume III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from live authority. |
| `SAMA-C000125-R001` | Enforces historical-status, classification and approval typing. |

## 12. Sources and external references

- Sean Brady and SAM collaborators, [Volume I technical spine, V.1--V.2](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md).
- The pinned Courtroom artifacts in the focused index above, commit
  `b5e914f71377e86ef4c67e199973d9300795cda1`.
- Planck Collaboration, [Planck 2018 results VI: cosmological parameters](https://doi.org/10.1051/0004-6361/201833910), used only where the preserved source tests declare comparator values.

The external cosmological paper supplies comparison context, not a primitive
or a hidden fit input to the derivations in Sections 3--5.

## 13. Revision, hash and approval boundary

This is registered document `SAMA-D000018`, revision \(1\). The document
catalog and generated manifests bind this exact file to its computed SHA-256;
the source-spine hash is stated at the top, and each test artifact has its own
registry hash. Hash equality establishes custody, not conceptual approval.

Every formula and result in this chapter is routed through the twelve atomic
records and twelve exact test keys listed above. Source verdict strings are
preserved as provenance; no unregistered SAMA classification has been added.
`reviewed_and_approved` remains `false`, and `approval` remains `null` until
Sean Brady explicitly approves this exact revision.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G219`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G219_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219_summary.json)<br>[G219_summary_md.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219_summary_md.md)<br>[G219_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219_summary.json) | [G219_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219_summary.json)<br>[G219_summary_md.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219_summary_md.md)<br>[G219_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219_summary.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G219B`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G219B_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219B_summary.json)<br>[G219B_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219B_summary.json) | [G219B_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219B_summary.json)<br>[G219B_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219B_summary.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G219C`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G219C_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219C_output.json)<br>[G219C_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219C_output.json) | [G219C_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G219C_output.json)<br>[G219C_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G219C_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G305`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G305_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G305_output.json)<br>[G305_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G305_output.json) | [G305_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G305_output.json)<br>[G305_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G305_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G310`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G310_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G310_output.json)<br>[G310_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G310_output.json) | [G310_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G310_output.json)<br>[G310_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G310_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G312`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G312_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G312_output.json)<br>[G312_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G312_output.json) | [G312_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G312_output.json)<br>[G312_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G312_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G313`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G313_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G313_output.json)<br>[G313_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G313_output.json) | [G313_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G313_output.json)<br>[G313_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G313_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`CR:CR018@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr018-a0-chi-baryon-inventory-derivation/README.md) | [CR018_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_PRECOMMIT.md)<br>[CR018_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_declared_premises.json) | [CR018_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_runner.py) | [CR018_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_runner.py)<br>[CR018_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_result.md)<br>[CR018_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_summary.json) | [CR018_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_result.md)<br>[CR018_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr018-a0-chi-baryon-inventory-derivation/README.md) |
| [`CR:CR019@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr019-effective-matter-inventory-refinement/README.md) | [CR019_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_PRECOMMIT.md)<br>[CR019_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_declared_premises.json) | [CR019_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_runner.py) | [CR019_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_runner.py)<br>[CR019_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_result.md)<br>[CR019_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_summary.json) | [CR019_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_result.md)<br>[CR019_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr019-effective-matter-inventory-refinement/README.md) |
| [`CR:CR023@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr023-baryon-cosmology-branch-verdict/README.md) | [CR023_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_PRECOMMIT.md)<br>[CR023_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_declared_premises.json) | [CR023_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_runner.py) | [CR023_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_runner.py)<br>[CR023_component_verdicts.csv](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_component_verdicts.csv)<br>[CR023_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_result.md)<br>[CR023_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_summary.json) | [CR023_component_verdicts.csv](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_component_verdicts.csv)<br>[CR023_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_result.md)<br>[CR023_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT/CR023_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr023-baryon-cosmology-branch-verdict/README.md) |
| [`CR:CR281@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr281-cosmic-budget-typed-readout-promotion/README.md) | [CR281_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_PRECOMMIT.md)<br>[CR281_typed_contract.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_typed_contract.json) | [CR281_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_runner.py) | [CR281_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_runner.py)<br>[CR281_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_result.md)<br>[CR281_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_summary.json) | [CR281_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_result.md)<br>[CR281_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION/CR281_summary.json) | [All 9 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr281-cosmic-budget-typed-readout-promotion/README.md) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [LC06_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_wrong_controls.csv) | [LC06_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)<br>[LC06_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json) | [All 10 files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000018`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/COSMIC_INVENTORY_FROM_ACCUMULATION_FLOOR.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000018 | Cosmic Inventory | Horizon Quotient, Clean Inventory, Effective Inventory and Correction Chain |

| Document field | Value |
|---|---|
| Purpose | Derive the horizon quotient, clean cosmic inventory and separately typed effective-matter refinement from the locked substrate packet; preserve the correction, wrong-control, promotion and replay chains. |
| Prerequisite documents | `SAMA-D000001`, `SAMA-D000002` |
| Used by | `SAMA-D000019`, `SAMA-D000022`, `SAMA-D000023`; focused child of `SAMA-P000002`. |
| Primary theory source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), especially V.1--V.2; SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`; every qualified key used below resolves there. |
| Revision state | Source-bound revision 1; `reviewed_and_approved: false`; `approval: null`. |

</details>
