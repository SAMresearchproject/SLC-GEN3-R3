[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Periodic and Composite Matter

## Opening question

> How can one finite construction reach a 126-row periodic surface, extend it
> through eight source-native frontier identities, apply a nuclear readout
> without refitting, and then describe composite matter without turning shared
> counts, labels or scalar values into false type identities?

## Conceptual abstract

Periodic matter is not constructed by starting with the conventional name of
an element and solving backward for a SAM row. The source order is native
first:

\[
\text{native }Z\text{-indexed row}
\longrightarrow
\text{invariant audit}
\longrightarrow
\text{authorized label or comparator}.
\]

LC:LC05 executes that order for \(Z=1,\ldots,126\). It retains 126 native
periodic rows, applies 118 downstream known labels, and leaves the eight rows
\(Z=119,\ldots,126\) as source-native frontier identities. The same replay
also retains a scoped 162-row isotope roster. Those two counts do not describe
the same table: an element family is indexed by \(Z\), an isotope by
\((Z,N,A)\), and a representative isotope is one selected isotope used for a
one-row-per-element readout.

The frontier family uses the balanced anchors

\[
Z=N,\qquad A=Z+N=2Z.
\]

Its terminal row has

\[
Z=N=126=M,\qquad A=252=2M=14\Theta.
\]

CR:CR273@09a records five exact contacts at that terminus. CR:CR274@09a
supplies a historical fitted nuclear readout; CR:CR277@09a freezes that
readout and applies it with zero refit to one representative isotope for every
\(Z\) from 1 through 126. The reported full-table residuals remain visible as
readout evidence. They neither convert the fitted coefficients into substrate
primitives nor convert frontier identities into observed elements.

Composite matter introduces a second conceptual movement. A constituent
catalog does not become a bound object by adding row numbers. The route is

\[
\text{constituent rows}
\longrightarrow
\text{typed connector and debit pattern}
\longrightarrow
\text{finite composite closure}
\longrightarrow
\text{emitted source or carrier behavior}.
\]

CR:CR252@09a retains 169 bound-composite rows in the 321-row catalog.
LC:LC06 retains 63 bound composites inside a different 126-row matter
inventory. The four-slot nuclear ledger is a third projection. This chapter
keeps all three and explains why their unequal counts are expected.

## 1. The typed problem and its dependency chain

The periodic chapter begins only after two earlier constructions exist.
[SAMA-D000030](nuclear-ledger-and-isotope-families.md) supplies the nuclear
address

\[
(Z,N,A),\qquad A=Z+N,
\]

the four slot populations

\[
(n_p,n_{n_b},n_{n_e},n_e)=(Z,Z,N-Z,Z),
\]

and the distinction among an element family, an isotope and a representative
isotope. [SAMA-D000032](../04-binding/binding-and-the-exact-asymmetry-bridge.md) supplies
the exact asymmetry input and the declared operation order for the historical
nuclear readout.

The dependency chain is therefore

\[
\begin{aligned}
\text{typed matter and row grammar}
&\longrightarrow \text{nuclear slots}\\
&\longrightarrow \text{isotope address }(Z,N,A)\\
&\longrightarrow \text{one native element family per }Z\\
&\longrightarrow \text{representative-isotope selection}\\
&\longrightarrow \text{historical binding readout}\\
&\longrightarrow \text{periodic and frontier display}.
\end{aligned}
\]

The display is last. This is important because the known label, the chosen
representative isotope and the measured comparison value are outputs or
comparators. None is permitted to select the native row.

A composite path begins from an already admitted constituent row:

\[
\begin{aligned}
\{\text{admitted constituents}\}
&\longrightarrow \text{connector class}\\
&\longrightarrow \text{surface credit or debit}\\
&\longrightarrow \text{closure gate}\\
&\longrightarrow \text{composite row or nuclear object}\\
&\longrightarrow \text{source-support return}.
\end{aligned}
\]

The braces denote a typed collection, not a request to sum the constituents'
catalog numbers. SAMA-C000179-R001 fixes this route.

## 2. Definitions, domains and units

| Object | Definition | Domain or unit | Type boundary |
|---|---|---|---|
| \(Z\) | proton number and element-family coordinate | integer \(1\le Z\le126\) on this surface | Selects a family, not a unique isotope. |
| \(N\) | neutron number | nonnegative integer | Joins \(Z\) to select an isotope. |
| \(A\) | \(Z+N\) | nucleon count | Not the accumulation field \(A(r)\). |
| \(M\) | retained matter horizon \(7R^2/8=126\) | exact retained-capacity count | Shared value does not identify the periodic and matter-inventory schemas. |
| \(\Theta\) | released carrier \(R^2/8=18\) | carrier count/support role | Not an element, isotope or mass. |
| element-family row | one native row indexed by \(Z\) | periodic schema | May contain many isotope rows. |
| isotope row | row indexed by \((Z,N,A)\) | isotope schema | Multiple rows can share one \(Z\). |
| representative isotope | one source-selected isotope for an element-family readout | comparison schema | Does not replace the isotope family. |
| known label | downstream conventional identifier | reveal field | Never a construction input. |
| frontier identity | source-native \(Z=119,\ldots,126\) identifier | SAM periodic schema | Not an observation. |
| constituent matter row | admitted finite row | particle or matter schema | Row number is not a binding coefficient. |
| connector/debit pattern | typed relational operators among constituents | exact source-support channels | Not reducible to row-number addition. |
| composite closure | finite gate acting on a connected configuration | composite schema | Must not be inferred from a matching scalar alone. |
| readout RMS | root-mean-square comparison residual | MeV | Evidence about the declared readout, not a substrate unit. |

The central count firewall is

\[
\begin{array}{rcl}
321&=&\text{finite-particle catalog rows},\\
169&=&\text{bound-composite rows inside that catalog},\\
126&=&\text{matter-inventory rows }(63+63),\\
126&=&\text{periodic element-family rows},\\
80&=&\text{tensor-compatible matter/antimatter surface},\\
162&=&\text{scoped isotope-roster or terminal-ledger count, by context}.
\end{array}
\]

Numerical equality between two lines is not a cast between their schemas.
SAMA-C000142-R001, SAMA-C000166-R001 and SAMA-C000176-R001 make that
firewall explicit.

## 3. Native-first periodic construction

### 3.1 Generate the family coordinate

For every integer

\[
Z\in\{1,2,\ldots,126\},
\]

emit one native family row

\[
E_Z=(Z,\mathrm{native\_id}_Z,\mathrm{frontier\_flag}_Z,\ldots).
\]

The ellipsis denotes source-defined fields; it does not authorize filling
unavailable shell, decay or chemistry columns. The row exists because the
native finite construction admits \(Z\), not because a downstream table
already supplies a name.

### 3.2 Audit before reveal

The row then passes the source-defined invariants. At minimum the periodic
surface checks:

\[
1\le Z\le126,
\]

\[
\#\{E_Z\}=126,
\]

and uniqueness of the native coordinate:

\[
E_{Z_1}=E_{Z_2}\Longrightarrow Z_1=Z_2.
\]

Only after those checks may a known-label comparator act:

\[
\mathcal L_{\rm known}(E_Z)=
\begin{cases}
\text{authorized known label}, & 1\le Z\le118,\\
\text{native frontier identity}, & 119\le Z\le126.
\end{cases}
\]

This ordering is SAMA-C000144-R001. It prevents label backfill from becoming a
hidden generator.

### 3.3 Join an isotope without erasing the family

An isotope is a row

\[
I_{Z,N}=(Z,N,A=Z+N,\ldots).
\]

The family projection forgets \(N\) only for the purpose of grouping:

\[
\pi_Z(I_{Z,N})=E_Z.
\]

Because many values of \(N\) can share the same \(Z\), \(\pi_Z\) is
many-to-one. It cannot be inverted without a selection rule. A representative
selector

\[
\sigma_{\rm rep}:E_Z\longmapsto I_{Z,N_{\rm rep}(Z)}
\]

chooses one isotope for a full-table readout. It does not state

\[
\{I_{Z,N}:N\text{ admitted}\}
=\{I_{Z,N_{\rm rep}(Z)}\}.
\]

This is the technical content of SAMA-C000166-R001.

### 3.4 Why the two 126-row surfaces remain different

LC:LC06 partitions its matter inventory as

\[
126=63\text{ stable single writes}+63\text{ bound composites}.
\]

LC:LC05 partitions the periodic surface as

\[
126=118\text{ downstream-labeled families}
+8\text{ frontier families}.
\]

The partitions have different predicates and different member types.
Therefore a bijection based only on row position would be a display alignment,
not a physical or grammatical identity. SAMA-C000176-R001 calls the shared
cardinality a structural contact at \(M=126\), and nothing stronger is
required for the periodic construction.

## 4. Deviation chain: wrong controls and corrected route

The source chain is informative because it exposes several tempting but
incorrect controls.

### 4.1 Wrong control: label-first reconstruction

The wrong route is

\[
\text{known name or measured mass}
\longrightarrow
\text{chosen isotope}
\longrightarrow
\text{fitted native row}.
\]

It can reproduce a familiar display while destroying the direction of
construction. The correction is to freeze the native \(Z\)-indexed surface,
audit it, and apply labels and measurements only downstream. LC:LC05 retains
that ordering.

### 4.2 Wrong control: count equality as schema identity

Another wrong control identifies the 126 matter-inventory rows with the 126
periodic rows because both totals equal \(M\). It fails immediately under
partition audit:

\[
63+63\ne118+8
\]

as typed decompositions, even though both scalar sums equal 126. The
correction preserves two tables and records only their shared horizon.

### 4.3 Wrong control: a representative isotope is the isotope family

A one-row-per-\(Z\) binding table needs a representative isotope. Treating
that selected isotope as all isotopes hides the selector and suppresses
isotope multiplicity. The correction writes the map
\(\sigma_{\rm rep}\) explicitly, retains the isotope vault separately, and
reports whole-table residuals as representative-isotope readout evidence.

### 4.4 Deviation from fitted benchmark to frozen extension

CR:CR274@09a uses a 55-row benchmark. Its base readout records
\(3.9102\) MeV RMS. Four family gates produce a historical fitted readout of
\(2.7160\) MeV RMS with 50 of 55 rows within 5 MeV. Those fitted parameters
are neither native periodic inputs nor substrate primitives.

The corrective extension is not another fit. CR:CR277@09a freezes the
CR274 operator and evaluates one representative isotope at every
\(Z=1,\ldots,126\) with zero refit. It first reproduces the benchmark
predictions to less than \(10^{-3}\) MeV, then reports the extended subsets.
This gives a chronological chain:

\[
\text{55-row fitted construction}
\longrightarrow
\text{freeze}
\longrightarrow
\text{benchmark reproduction}
\longrightarrow
\text{126-row zero-refit readout}.
\]

The visible rise in the light-row residual is not deleted. It marks the
operator's extrapolation behavior.

### 4.5 Wrong control: frontier name as observational status

The eight frontier rows have native names and exact balanced addresses.
Replacing their status with observed merely because they have names would
turn a source identifier into an external measurement. The correction retains
the identities, forecast locks and open outputs separately.

### 4.6 Wrong control: composite row-number addition

If constituent catalog indices \(i\) and \(j\) are added,
\(i+j\) contains no connector orientation, pair class, debit, closure gate or
emitted carrier channel. Two different connected configurations may therefore
share the same sum. The corrected composite object is at least

\[
C=\bigl(\{r_i\},\Gamma,\mathcal D,\mathcal G_{\rm close},
\mathcal E_{\rm source}\bigr),
\]

where \(\Gamma\) is the typed connector pattern, \(\mathcal D\) the debit or
credit operator, \(\mathcal G_{\rm close}\) the closure gate and
\(\mathcal E_{\rm source}\) the emitted source-support behavior.

## 5. Periodic surface and frontier readout

### 5.1 LC:LC05 source anchor

LC:LC05 replays the periodic and isotope packet from the locked primitive
stack. It retains:

- 126 of 126 native periodic rows;
- 118 downstream known labels;
- eight native frontier identities;
- the older scoped 162-row isotope roster; and
- the CR071 frontier seal carried by that packet.

The decimal replay of the one-eighth/seven-eighths source split has maximum
error \(10^{-96}\) against a \(10^{-90}\) tolerance. Its diagnostic controls
retain label backfill, row deletion, primitive mutation, frontier relabeling
and other type-collapsing alternatives. The result supplies the periodic
surface and vault custody but no complete shell, half-life, decay, chemistry
or synthesis operator. That boundary is SAMA-C000167-R001.

### 5.2 Deriving the eight balanced frontier anchors

For

\[
Z\in\{119,120,121,122,123,124,125,126\},
\]

set

\[
N=Z
\]

and then

\[
A=Z+N=2Z.
\]

The resulting addresses are:

| Native identity | \(Z\) | \(N\) | \(A\) |
|---|---:|---:|---:|
| Harlium | 119 | 119 | 238 |
| Brockium | 120 | 120 | 240 |
| Uniquium | 121 | 121 | 242 |
| Liamium | 122 | 122 | 244 |
| Cooperium | 123 | 123 | 246 |
| Lindesium | 124 | 124 | 248 |
| Dorisium | 125 | 125 | 250 |
| Jerroldium | 126 | 126 | 252 |

These are frontier identities. The table derives addresses; it does not emit
measurements.

### 5.3 CR:CR273@09a five-way terminus

At Jerroldium-252,

\[
Z=N=126=M.
\]

Therefore

\[
A=Z+N=252=2M.
\]

Because \(\Theta=18\),

\[
14\Theta=14\cdot18=252=A.
\]

The balanced quark ledger gives

\[
u=2Z+N=3Z=378
\]

and

\[
d=Z+2N=3Z=378.
\]

With the source volume address \(\hat V=54\),

\[
7\hat V=7\cdot54=378=u=d.
\]

The neutral electron count is

\[
e=Z=126.
\]

CR:CR273@09a records five contacts: the matter horizon, the source
doubly-magic predicate, carrier-mode inheritance, noble-cipher inheritance
and 126-fold component symmetry. The arithmetic contacts are exact. Stability,
chemistry, synthesis and observation remain assigned to their designated
reveals.

### 5.4 CR:CR274@09a construction and CR:CR277@09a retest

CR:CR274@09a enters here only after the exact nuclear and asymmetry columns
exist. Its historical chain is

\[
(Z,N)
\longrightarrow
\text{base nonlinear geometry}
\longrightarrow
\text{locked asymmetry coefficient}
\longrightarrow
\text{four fitted family gates}
\longrightarrow
\text{55-row comparison}.
\]

It records the benchmark change

\[
3.9102\ {\rm MeV}
\longrightarrow
2.7160\ {\rm MeV}.
\]

CR:CR277@09a then holds those choices fixed. On the 118 observed
representative rows it reports \(6.672\) MeV RMS. By subset it reports:

| Subset | Rows | RMS (MeV) | Interpretation |
|---|---:|---:|---|
| light \(Z=1\) to \(7\) | 7 | 19.907 | visible extrapolation outside the base fit range |
| middle \(Z=8\) to \(82\) | 75 | 4.145 | central representative-isotope range |
| heavy \(Z=83\) to \(118\) | 36 | 5.752 | heavy extension |
| all observed \(Z=1\) to \(118\) | 118 | 6.672 | whole observed representative table |
| extended-only | 78 | 7.974 | rows absent from the original 55-row set |

The operator is not refitted for the table or for the eight frontier rows.
SAMA-C000171-R001 keeps the nonlinear-binding requirement;
SAMA-C000175-R001 keeps the fitted-readout boundary; SAMA-C000177-R001 keeps
the zero-refit outcome.

## 6. Composite inventory joins

### 6.1 CR:CR252@09a and the 321-row catalog

CR:CR252@09a refreshes the finite-particle catalog and retains its exact
typed bins:

\[
321
=35\text{ elementary}
+169\text{ bound composite}
+117\text{ placeholder}.
\]

The 169 bound rows answer a catalog question: which source-defined composite
entries are carried by this finite-particle table? They do not state that
every bound matter inventory, isotope roster or computation grammar must have
169 rows.

### 6.2 LC:LC06 and the 126-row matter inventory

LC:LC06 asks a different question and retains

\[
126
=63\text{ stable single writes}
+63\text{ bound composites}.
\]

Its table contains no antimatter rows. It also does not promote carrier
traffic into matter. The null-conjugate witness has native value 18 and debit
18, yet closes to

\[
M_{\rm obs}=0,\qquad q_A=0.
\]

Thus the same displayed number can participate in a carrier route and in a
cancelled candidate without becoming an admitted matter row.

### 6.3 Four-slot nuclei as a third projection

A nucleus is constructed from the typed slot population

\[
(Z,Z,N-Z,Z),
\]

not from a lookup in either composite count. Its composite closure retains
proton, balanced-neutron, excess-neutron and electron roles before applying
binding geometry. A single nucleus can therefore be represented:

- as a connected finite object;
- as one isotope row;
- as the representative row for an element family; and
- through constituent and source-support ledgers.

Those are linked projections of one constructed object, not interchangeable
row catalogs.

### 6.4 Composite source return

Once a composite has passed its finite closure, its observed matter readout
may enter

\[
q_A=M_{\rm obs}\left(1+\frac{|q|}{R^2}\right).
\]

That does not mean that \(q_A\) admitted the composite. Admission occurred
before this source-support gate. The output can then split into one-eighth
carrier support and seven-eighths retained support, which is developed in
[SAMA-D000033](../05-carriers-and-reception/carrier-container-return-to-accumulation.md).

## 7. Worked examples and exact derivations

### 7.1 A family, two isotopes and one representative

Let \(Z=6\). Two isotope addresses are

\[
I_{6,6}=(6,6,12)
\]

and

\[
I_{6,8}=(6,8,14).
\]

Both project to the same element family:

\[
\pi_Z(I_{6,6})=\pi_Z(I_{6,8})=E_6.
\]

If the source selects \(I_{6,6}\) as the representative row, the readout
contains one row for \(E_6\); it has not deleted \(I_{6,8}\) from the isotope
family. This small example is the exact reason a 126-row representative table
cannot be called an all-isotope table.

### 7.2 Horizon contact without table identity

The retained horizon is

\[
M=\frac78R^2=\frac78\cdot144=126.
\]

The periodic surface reaches

\[
\sum_{Z=1}^{126}1=126
\]

family rows. The matter inventory reaches

\[
63+63=126
\]

matter rows. The equal scalar is useful:

\[
\#\mathcal P=\#\mathcal M=M.
\]

But their type signatures differ:

\[
\mathcal P:\ Z\mapsto E_Z,
\qquad
\mathcal M:\ \text{matter address}\mapsto
\{\text{single},\text{bound}\}.
\]

Cardinality contact is retained; membership identity is not asserted.

### 7.3 Composite configurations with equal row-number sum

Suppose two candidate pairs have catalog indices

\[
i+j=k+\ell.
\]

If the first is an equal pair and the second an unequal pair, their surface
operators are different even though the scalar sums match:

\[
\mathcal D_{\rm eq}(r_i,r_j)
\ne
\mathcal D_{\rm neq}(r_k,r_\ell).
\]

If their connector orientations also differ,

\[
\Gamma_{ij}\ne\Gamma_{k\ell},
\]

then the closure gates consume different typed states. Row-number addition
cannot recover either difference. The composite tuple
\((\{r\},\Gamma,\mathcal D,\mathcal G_{\rm close},\mathcal E_{\rm source})\)
does.

## 8. Chemistry and current-authority boundary

The periodic construction safely exports:

- one native family per \(Z\) through 126;
- downstream known labels through \(Z=118\);
- eight source-native frontier identities;
- the balanced electron count \(e=Z\);
- directly sealed carrier and noble-cipher predicates; and
- explicit open fields for unavailable shell, decay, chemistry and synthesis
  results.

It does not yet supply a complete chemistry operator. In particular,

\[
Z+\text{frontier name}
\not\Longrightarrow
\text{bonding, valence, stability or synthesis}.
\]

A later chemistry construction must begin from typed electron, shell/cipher,
binding and composite operators and must preserve its own evidence chain.

Current ATOM3D geometry, current binding status and physical calibration live
under their current live authorities. Historical CR274 and CR277 readouts are
retained here because they are load-bearing steps in the Volume II
derivation, not because they replace current binding authority.
SAMA-C000180-R001 owns this boundary.

## 9. Established result and forward handoff

The source chain establishes the following within this chapter's scope:

1. The periodic surface is generated natively as 126 one-row-per-\(Z\)
   families.
2. Known labels and measured comparators enter only after construction.
3. Element families, isotope rows and representative isotope rows are
   distinct types connected by explicit projections and selectors.
4. LC:LC05 retains 118 labeled and eight frontier families together with a
   separately typed isotope roster.
5. The \(Z=119\) to \(126\) frontier family follows \(Z=N\), \(A=2Z\).
6. CR:CR273@09a records the exact Jerroldium-252 terminus contacts.
7. CR:CR277@09a applies the frozen CR274 readout with zero refit and preserves
   the complete subset metrics.
8. CR:CR252@09a's 169 catalog composites and LC:LC06's 63 inventory
   composites are different projections.
9. Composite closure requires constituent, connector, debit, gate and source
   roles, not row-number addition.
10. Chemistry, observation, synthesis and current ATOM3D/binding authority
    remain at their explicitly typed boundaries.

Every document-test crosswalk row assigned here has
\(result\_classification=\mathrm{null}\). The source artifacts retain their
own recorded status and verdict fields; this document does not rewrite them.

[SAMA-D000033](../05-carriers-and-reception/carrier-container-return-to-accumulation.md) receives closed
matter and composite outputs, keeps the material source typed as matter, and
derives the carrier/container return into compressed accumulation readout.

## 10. Focused test evidence

| Test record key | Chronological role | Focused outcome | Preserved boundary |
|---|---|---|---|
| LC:LC05 | Source anchor for periodic/frontier chain | Retains 126 native rows, 118 downstream labels, eight frontier identities and the scoped isotope roster. | No complete shell, decay, chemistry or synthesis operator. |
| CR:CR273@09a | Frontier terminus result | Records the \(Z=N=126,\ A=252\) five-way contact. | Frontier identity is not observation; stability, chemistry and synthesis remain open. |
| CR:CR274@09a | Historical fitted construction | Records \(3.9102\to2.7160\) MeV RMS and 50/55 within 5 MeV after four family gates. | Fitted readout parameters are not substrate primitives or automatic current authority. |
| CR:CR277@09a | Zero-refit retest and extension | Applies the frozen readout to one representative isotope for every \(Z=1,\ldots,126\). | Representative rows are not every isotope; frontier rows are not observations. |
| CR:CR252@09a | Composite catalog premise | Retains the refreshed 321-row catalog and its 169 bound-composite bin. | Catalog bins do not redefine other surfaces. |
| LC:LC06 | Matter-inventory retest | Retains 63 single plus 63 bound rows and the zero-matter null witness. | The inventory is not the periodic surface and promotes neither carriers nor antimatter. |

### Exact test-reference route

- [LC:LC05 result](../../courtroom/16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_result.md)
- [CR:CR273@09a result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR273_JERROLDIUM_FIVE_WAY_CONVERGENCE/CR273_result.md)
- [CR:CR274@09a result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR274_GATED_NUCLEAR_READOUT_OPERATORS/CR274_result.md)
- [CR:CR277@09a result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR277_ONE_HUNDRED_TWENTY_SIX_ELEMENT_TABLE_AND_SOB_FRONTIER_LOCKS/CR277_result.md)
- [CR:CR252@09a result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result.md)
- [LC:LC06 result](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)

## 11. Atomic record index

| Record ID | Role in this document |
|---|---|
| SAMA-C000142-R001 | Keeps the 126-row matter inventory as 63 single plus 63 bound writes. |
| SAMA-C000144-R001 | Requires native construction before label or comparator reveal. |
| SAMA-C000166-R001 | Separates element-family, isotope and representative-isotope rows. |
| SAMA-C000167-R001 | Retains the isotope/frontier packet and its typed open outputs. |
| SAMA-C000171-R001 | Requires nonlinear binding geometry beyond a contact count. |
| SAMA-C000175-R001 | Types CR274 as historical fitted readout evidence. |
| SAMA-C000176-R001 | Constructs the native periodic surface and protects it from matter-inventory collapse. |
| SAMA-C000177-R001 | Records the zero-refit 126-representative-element readout and subset metrics. |
| SAMA-C000178-R001 | Defines the \(Z=119\) to \(126\) balanced frontier and Jerroldium terminus. |
| SAMA-C000179-R001 | Routes composite closure through connectors, debit and emitted support. |
| SAMA-C000180-R001 | Preserves the chemistry and current ATOM3D/binding authority boundaries. |

## 12. External references and source-citation boundary

This chapter introduces no independent external dataset or new observational
claim. Known element labels, representative-isotope comparators and nuclear
comparison values remain inside the exact registered source artifacts cited
in Section 10. Their provenance, source commit and SHA-256 are retained by the
permanent test registry. The chapter adds only the typed derivation and
cross-document synthesis of those registered sources.

## 13. Revision and approval

This exact revision has reviewed_and_approved: false and approval: null until
Sean Brady explicitly approves it. No test classification, source status,
frontier observation status or current live-authority statement is promoted by
this draft.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000031`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/PERIODIC_AND_COMPOSITE_MATTER.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000031 | Composite Matter | Periodic Surface, Frontier Family and Composite Closure |

| Document field | Value |
|---|---|
| Purpose | Construct the native 126-row periodic surface, distinguish element families from isotopes and representative-isotope readouts, derive the eight-row frontier family, and return periodic rows to composite closure without collapsing the 321-, 126-, 80- or nuclear-ledger schemas. |
| Prerequisite documents | [SAMA-D000030](nuclear-ledger-and-isotope-families.md); [SAMA-D000032](../04-binding/binding-and-the-exact-asymmetry-bridge.md) |
| Used by | SAMA-D000033 and the Volume II parent SAMA-P000003; generated from the document catalog |

</details>
