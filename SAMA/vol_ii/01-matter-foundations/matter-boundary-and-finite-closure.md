[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Matter Boundary and Finite Closure

## ATOM3D: contact, grammar and signed decoding — 14 September 2026

A3D41-T18-CONTACT-R2 uses SLC-GEN3-R3; A3D41-RXT-R3 supplies the joint native successor. Ordinary contact retains four minima and 113,664 agreeing readouts. Li-6 grammar retains both selected covers and every tie across six placements and 128 rho settings. Two Write responses and a signed N01 bit recover all 192 tested configurations. The test result suggests strong contact with the concept. The separate distinct-selector and physical-coefficient/MeV work remain owner-paused.

[Current derivations, code and results](../../../research/atom3d/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Opening question

> When does a substrate-supported configuration become matter, and what may be
> carried forward after that transition without confusing source support with
> measured rest mass?

## Conceptual abstract

Volume I supplies distinction, connectivity, capacity, accumulation and
transport. None of those roles is yet a finite material object. Volume II
begins only when connector support and carrier routing pass a typed closure
condition and produce a finite closed write. The resulting matter row remains
coupled to the substrate, but it is not substrate folded into a larger number.

The conceptual picture is a closure with two sides. A closed radix-square
domain has a one-eighth released carrier side and a seven-eighths retained
side. Matter occupies an admitted finite write on the retained side. Once the
write is admitted, it emits a source-support quantity \(q_A\); that support is
split into unresolved carrier support \(T\) and retained-write support \(W\).
The split conserves \(q_A\), but neither \(q_A\) nor its two parts is thereby
declared to be measured particle mass.

That last distinction was not imposed after the fact. The direct bridge
\(m_i=m_g=\mu_QQ\) was executed and failed its locked mass-number control.
The failure organized sharply along neutron excess \(N-Z\). The correction
was therefore a type correction: retain the source channel, reject its direct
identification with rest mass, and route it through carrier conservation and
ledger compression before an accumulation readout.

## 1. The category transition

### 1.1 The transition is operational, not numerical

The source-bound transition is

```text
connector support + carrier routing + typed closure gate
    -> finite closed write
    -> admitted matter row.
```

Every arrow changes or preserves a declared type. Connector support supplies
relations. Carrier routing moves unresolved support. The closure gate decides
whether the candidate write is finite matter. Only the final admitted object
is a matter row.

The following shortcut is therefore invalid:

```text
substrate value -> numerically larger value -> matter.
```

A connector, carrier, hidden-support row, catalog candidate, grammar address
or non-row operator can have an exact scalar value without being matter. A
matter row can in turn emit substrate-facing support without ceasing to be
matter. Category is carried by the schema and operator, not inferred from the
number printed in a cell.

### 1.2 Coupled categories do not become identical categories

The two directions across the interface are different:

1. Substrate-to-matter: connectors and carriers support a closure gate that
   admits a finite write.
2. Matter-to-substrate: an admitted closed write emits \(q_A\), whose carrier
   share is compressed into an \(A\)-source readout.

The return route is


\[
\text{closed matter write}
\longrightarrow q_A
\longrightarrow \frac18\text{ carrier support}
\longrightarrow \text{ledger compression}
\longrightarrow A(r)=\frac{r_s}{r}.
\]

The route says that matter sources an accumulation readout. It does not say
that matter is substrate, that the carrier is matter, or that \(q_A\) is a
measured mass.

## 2. Definitions, domains and units

| Object | Definition | Domain or unit | Type boundary |
|---|---|---|---|
| \(\alpha_H\) | \(2\) | dimensionless | Binary readout, not a row count. |
| \(D\) | \(3\) | dimensionless support dimension | Used in closure identities, not fitted here. |
| \(S\) | \(\alpha_H^D=8\) | dimensionless multiplicity | Denominator of the carrier/retained split. |
| \(R\) | \(\alpha_H^2D=12\) | dimensionless route radix | \(R^2\) is the closed-domain capacity in this construction. |
| \(\Theta\) | \(R^2/S=18\) | structural support units | Released tensor-carrier side; not matter or rest mass. |
| \(M\) | \((S-1)R^2/S=126\) | structural capacity units | Retained capacity; not by itself the count of every 126-row surface. |
| \(r\) | a source-table row | schema-dependent record | Becomes matter only if its admission predicate passes. |
| \(M_{\rm obs}(r)\) | finite observed/readout value on an admitted row | source-table mass/readout units | An input to the support gate after admission. |
| \(q(r)\) | charge or role coordinate | schema-defined integer or rational | Its meaning depends on the row schema. |
| \(q_A(r)\) | A-source support | same algebraic scale as \(M_{\rm obs}\) in the source table | Coupling/support channel, not direct measured rest mass. |
| \(T(r)\) | \(q_A/S\) | source-support units | Unresolved tensor-carrier support. |
| \(W(r)\) | \((S-1)q_A/S\) | source-support units | Retained-write support. |
| \(A(r)\) | \(r_s/r\) after declared compression | dimensionless accumulation | Downstream readout; not identical to the row's \(q_A\). |

The letter \(M\) is overloaded in the historical sources. In this chapter,
\(M=126\) denotes retained capacity and \(M_{\rm obs}(r)\) denotes the
row-level admitted readout. A formula is well typed only when the relevant
meaning has been named.

## 3. Deriving the finite closed domain

### 3.1 Foundation to radix square

Begin with the locked structural values

\[
\alpha_H=2,
\qquad
D=3.
\]

The surface multiplicity and route radix follow as

\[
S=\alpha_H^D=2^3=8,
\]

\[
R=\alpha_H^2D=2^2\cdot3=12.
\]

The closed radix-square capacity is therefore

\[
R^2=12^2=144.
\]

### 3.2 One-eighth release

The carrier fraction is the reciprocal surface multiplicity,

\[
f_{\rm carrier}=\frac1S=\frac18=2^{-D}.
\]

Applying it to the full closed domain gives

\[
\Theta
=R^2f_{\rm carrier}
=144\left(\frac18\right)
=18.
\]

The same value is recovered through the independent structural identity

\[
\Theta=\alpha_HD^2=2\cdot3^2=18.
\]

The equal values establish an arithmetic weld between two routes. They do not
change the output's type: \(\Theta18\) is released carrier traffic.

### 3.3 Seven-eighths retention

The complementary retained fraction is

\[
f_{\rm retained}=1-f_{\rm carrier}
=1-\frac18
=\frac78.
\]

Hence

\[
M
=R^2f_{\rm retained}
=144\left(\frac78\right)
=126.
\]

The full capacity closes exactly:

\[
\Theta+M=18+126=144=R^2.
\]

This is a decomposition into unlike roles. Equality in the same arithmetic
ledger does not imply equality of type. The 18 side is released carrier; the
126 side is retained capacity in which finite writes may be admitted.

## 4. Deriving the matter source-support gate

### 4.1 Admission comes first

Let \({\rm Adm}(r)\) be the source-defined finite-matter predicate. The gate is
piecewise:

\[
q_A(r)=
\begin{cases}
M_{\rm obs}(r)\left(1+\dfrac{|q(r)|}{R^2}\right),
& {\rm Adm}(r)=1,\\
0,&{\rm Adm}(r)=0.
\end{cases}
\]

The first line is not itself an admission rule. It is evaluated after the row
has passed the source-table matter condition. This ordering prevents a
non-matter scalar from becoming matter merely because the arithmetic can be
performed.

Expanding the admitted branch shows its two terms:

\[
q_A
=M_{\rm obs}
+M_{\rm obs}\frac{|q|}{R^2}.
\]

The first term carries the admitted write. The second is its charge- or
role-conditioned support increment on the radix-square domain. Both are in the
source-support channel.

### 4.2 Carrier and retained decomposition

Apply the same one-eighth/seven-eighths decomposition to the support:

\[
T=\frac{q_A}{S}=\frac{q_A}{8},
\]

\[
W=\frac{S-1}{S}q_A=\frac78q_A.
\]

Conservation follows without approximation:

\[
T+W
=\frac{q_A}{8}+\frac{7q_A}{8}
=q_A.
\]

This identity is the local algebraic reason that ledger compression can carry
the source forward without adding a matter row. The split redistributes one
support quantity; it does not create an additional object.

### 4.3 Worked admitted-row arithmetic

For an admitted illustrative row with
\(M_{\rm obs}=12\) and \(|q|=3\), the exact source-support calculation is

\[
q_A
=12\left(1+\frac3{144}\right)
=12\left(\frac{49}{48}\right)
=\frac{49}{4}.
\]

The two support channels are then

\[
T=\frac18\frac{49}{4}=\frac{49}{32},
\qquad
W=\frac78\frac{49}{4}=\frac{343}{32},
\]

and

\[
T+W=\frac{392}{32}=\frac{49}{4}=q_A.
\]

The example demonstrates the operator. It does not assign a conventional
particle identity or claim that \(49/4\) is a measured rest mass.

### 4.4 Worked boundary row: the null conjugate

LC06 preserves `QP093A-0088` with

\[
M_{\rm native}=18,
\qquad
S_{\rm debit}=18,
\qquad
M_{\rm obs}=0,
\qquad
q_A=0.
\]

The native value and debit cancel before matter admission. The number 18 also
labels \(\Theta\), but that numerical coincidence promotes neither object:
the row has zero observed matter and \(\Theta18\) remains carrier-only. This is
the sharpest row-level witness that scalar equality cannot replace type.

## 5. Matter admission and type boundaries

QP034 separates collective lane support from localized particle identity. Its
stable lane reaches closure fraction \(0.9999993719460315\), and its strongest
slot has self-support score \(0.9880873618629215\), yet the run records zero
fixed-point slot promotions. Strong support is therefore a candidate
condition, not particle admission.

The finite-matter boundary can be summarized by five non-equivalences:

\[
\text{support lane}\ne\text{particle identity},
\]

\[
\text{carrier}\ne\text{matter row},
\]

\[
\text{native candidate}\ne\text{admitted matter},
\]

\[
q_A\ne\text{measured rest mass},
\]

\[
\text{non-row operator}\ne\text{additional row}.
\]

LC01 fixes the primitives and the wrong-control register before downstream
replay. It establishes \(18+126=144\) and explicitly types 18 as carrier-only.
The lock is custody for subsequent tests; it does not pre-award their results.

## 6. Direct source examples

### 6.1 CR238 matter-gate regrade

CR238 derives the typed kernel from \(\mathcal F=81\), \(S=8\),
\(\alpha_H=2\) and the resulting \(D=3,R=12\). Its matter block then applies
the gate without injecting literal 144 or 8 into the functional code:

| Source class | Rows | Reproduced | Operator |
|---|---:|---:|---|
| admitted matter | 126 | 126 | \(q_A=M_{\rm obs}(1+|q|/R^2)\), \(T=q_A/S\), \(W=(S-1)q_A/S\) |
| blocked | 13 | 13 | \(M_{\rm obs}=q_A=T=W=0\) |
| hidden support | 8 | 8 | \(M_{\rm native}=p+p^2/R^2\) |

The three rows classes answer different questions. The hidden-support formula
can generate a nonzero native structural value while the matter channel
remains unavailable. The blocked rows show the same boundary from the other
direction.

### 6.2 QP092d conservation

QP092d tests the carrier split across 7 particle-source rows, 6 macro-ledger
rows and 18 propagation rows. All 31 scoped rows pass their respective
reconstruction checks; 3/3 ledger scopes close, the maximum conservation
relative error is approximately \(2.98274132099\times10^{-19}\), and direct
\(q_A\)-as-mass use rejects on 24/24 rows. No matter rows are added.

The execution therefore supports exactly the typed statement derived above:

\[
\frac18q_A+\frac78q_A=q_A,
\]

followed by ledger compression before \(A\) updates.

## 7. Direct-bridge deviation, correction and locked replay

### 7.1 Starting proposition

CR238 established a native source quantity \(Q(P)\) and the typed matter
support route. The direct next question was whether one global conversion
could make that source quantity measured inertial and gravitational mass:

\[
m_i(P)=m_g(P)=\mu_QQ(P).
\]

CR239 fixed the one-anchor bridge at carbon-12:

\[
Q(^{12}{\rm C})=\frac{7117}{16},
\qquad
\mu_Q=\frac{192}{7117}\ {\rm u\ per\ Q\!\!-unit},
\]

so that the anchor maps exactly to \(12\,\mathrm u\).

### 7.2 Failure against the locked control

The direct bridge did not generalize. Its Lane-A one-anchor RMS residual was
\(0.189480\), whereas the locked mass-number control

\[
A=Z+N
\]

had RMS \(0.00202\), approximately ninety times smaller. The precommitted
non-failure condition required \(Q\) to beat that control by a factor of two;
the source result therefore records `FAIL_CR239_DIRECT_BRIDGE`.

The isotope increment makes the scale failure explicit. The source channel
predicts

\[
\Delta m_{\rm SAM}
=\mu_QSg
=\frac{\mu_Q}{8}
=\frac{24}{7117}\,\mathrm u
\approx0.003372\,\mathrm u
\]

per added neutron, while the 14 measured isotope pairs produce a mean
measured-to-predicted ratio \(296.45\) and median \(296.66\).

### 7.3 The failure contains the correction direction

The residual was highly organized rather than shuffled noise:

| Subset or axis | Source result |
|---|---:|
| \(N=Z\) subset RMS | \(0.0023\) across 12 rows |
| \(N\ne Z\) subset RMS | \(0.2152\) across 37 rows |
| Spearman correlation with \(N-Z\) | \(+0.984\) |
| Spearman correlation with mass number \(A\) | \(+0.961\) |

The source skeleton retains information—shuffling \(Q\) worsened the RMS by
about \(26\times\)—but a single multiplicative conversion does not supply the
neutron-excess rest-mass channel. The correct conclusion is therefore narrow:
raw \(Q\) remains a substrate-coupling/source variable, and measured rest mass
requires a separately typed bridge.

### 7.4 Correction and retest

QP092d supplies the correction: conserve \(q_A\) through its one-eighth
carrier and seven-eighths retained components, add no matter row, and require
compression before accumulation updates. LC03 then replays the complete route

```text
closed matter -> qA -> 1/8 carrier -> ledger compression
              -> A(r) -> force/clock/road readout
```

while rejecting 15/15 wrong controls, including direct \(q_A\)-as-mass, no
compression, no carrier, \(1/4\) and \(1/16\) splits, carrier-to-matter
promotion, mass-only sourcing and lane mixing.

LC06 retests the boundary on the matter inventory: 126/126 matter rows,
63/63 stable single writes, 63/63 bound composites, no antimatter rows in
that table, maximum Decimal split error \(10^{-96}\), and the null-conjugate
witness preserved. The failed direct bridge is not deleted; it is the evidence
that determines the corrected type route.

## 8. Established result and exact boundary

The source artifacts establish the following bounded construction:

1. Matter is a finite closed-write category supported by, but not identical
   to, substrate connectors and carriers.
2. \(R^2=144\) decomposes exactly into \(\Theta=18\) released carrier and
   \(M=126\) retained capacity.
3. After admission, \(q_A=M_{\rm obs}(1+|q|/R^2)\) and its exact support split
   is \(T=q_A/8\), \(W=7q_A/8\), \(T+W=q_A\).
4. The direct identity of raw source \(Q\) or \(q_A\) with measured rest mass
   is rejected by the preserved CR239 failure and the QP092d/LC03 route.
5. Ledger compression is required before the source reaches an accumulation
   readout; no carrier or compression address is added as a matter row.

No project-wide result classification is assigned in this document because
the registered atomic and crosswalk records carry `result_classification:
null`. The exact source verdict/status tokens are preserved in the index
below.

## 9. Controls, deviations and rejected substitutions

| Proposed substitution | What happens | Preserved lesson |
|---|---|---|
| Numerical growth implies matter | Admits unsupported values and carriers | Admission is a typed predicate. |
| Lane support implies particle identity | QP034 has strong support but zero fixed-point promotions | Support and identity are separate. |
| \(\Theta18\) is a matter/rest-mass row | Contradicts LC01 and the LC06 null witness | Released traffic remains carrier-only. |
| \(q_A\) is measured mass | QP092d rejects 24/24 direct rows; CR239 loses to \(A=Z+N\) | Source support needs its own bridge and compression route. |
| Omit ledger compression | LC03 wrong control rejects | Carrier conservation alone is not an \(A\)-readout. |
| Use \(1/4\) or \(1/16\) instead of \(1/8\) | LC03 wrong controls reject | The split is fixed by \(S=8\). |
| Delete blocked/null rows | Would erase the type boundary | Failed and null rows remain part of the evidence. |

## 10. Connections and forward handoff

`SAMA-D000003` supplies the spherical accumulation readout reached only after
the matter source has passed through the typed return route. This chapter owns
the interface and finite gate; it does not repeat the full Volume I force,
clock or road operators.

`SAMA-D000025` receives four facts without alteration:

```text
matter != substrate
R^2 = 18 released carrier + 126 retained capacity
qA = source support, not measured rest mass
support must remain typed through carrier/container routing.
```

That next chapter identifies which connector, substrate-atom and container
roles can participate in the route. It must not infer those roles from raw
numeric order.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| [`CR:CR238@09a`](../../tests/courtroom/09a-particle-mass-chain-cr238-substrate-spine-compaction/README.md) | Typed primitive and matter-gate premise | `CLEAN`; source verdict `PASS` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION) |
| [`CR:CR239@09a`](../../tests/courtroom/09a-particle-mass-chain-cr239-native-mass-gravity-bridge/README.md) | Preserved failed direct source/rest-mass bridge | `CLEAN`; source verdict `FAIL_CR239_DIRECT_BRIDGE` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE) |
| [`QP:QP092d`](../../tests/courtroom/upstream-artifacts-qp092/README.md) | Carrier-conservation correction | `CLEAN`; `PASS_QP092D_TENSOR_CARRIER_CONSERVATION_SOURCE_LEDGER_CLOSURE...` | [result](../../courtroom/upstream_artifacts/qp092/qp092d_tensor_carrier_conservation/qp092d_summary.json) | [folder](../../courtroom/upstream_artifacts/qp092/qp092d_tensor_carrier_conservation) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | Locked mechanism retest through ledger compression | `LC03_PASS_QA_LEDGER_COMPRESSION_GRAVITY_AS_A_REPLAY` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | Locked matter-inventory and null-boundary retest | `LC06_PASS_BARYON_AND_MATTER_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY) |
| [`QP:QP034`](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | Lane-support/particle-identity boundary | `QP034_LANE_SUPPORT_PARTICLE_IDENTITY_SEPARATED` | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP034_PRIVATE_LANE_SUPPORT_VS_PARTICLE_IDENTITY_SEPARATOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | Primitive stack and wrong-control lock | `LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000005-R001` | Closed-matter-to-accumulation return route. |
| `SAMA-C000126-R001` | Matter/substrate category distinction. |
| `SAMA-C000127-R001` | Typed finite-closure route and admission boundary. |
| `SAMA-C000128-R001` | Exact \(18+126=144\) carrier/retained split. |
| `SAMA-C000129-R001` | Finite matter source-support gate. |
| `SAMA-C000130-R001` | Exact one-eighth/seven-eighths support conservation. |
| `SAMA-C000131-R001` | Source-support/rest-mass distinction and null witness. |

## External references

No external bibliographic source is used directly. All numerical results and
boundaries are routed through the registered SAM/Courtroom artifacts above.

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`QP:QP034`](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All 107 files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) |
| [`QP:QP092d`](../../tests/courtroom/upstream-artifacts-qp092/README.md) | [All package files](../../tests/courtroom/upstream-artifacts-qp092/README.md) | [All package files](../../tests/courtroom/upstream-artifacts-qp092/README.md) | [All package files](../../tests/courtroom/upstream-artifacts-qp092/README.md)<br>[qp092d_summary.json](../../courtroom/upstream_artifacts/qp092/qp092d_tensor_carrier_conservation/qp092d_summary.json) | [qp092d_summary.json](../../courtroom/upstream_artifacts/qp092/qp092d_tensor_carrier_conservation/qp092d_summary.json) | [All 11 files](../../tests/courtroom/upstream-artifacts-qp092/README.md) |
| [`CR:CR238@09a`](../../tests/courtroom/09a-particle-mass-chain-cr238-substrate-spine-compaction/README.md) | [CR238_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_PRECOMMIT.md) | [CR238_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_runner.py) | [CR238_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_wrong_controls.csv) | [CR238_blocked_row_audit.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_blocked_row_audit.csv)<br>[CR238_matter_row_audit.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_matter_row_audit.csv)<br>[CR238_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_result.md)<br>[CR238_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_summary.json)<br>[CR238_surcharge_audit.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR238_SUBSTRATE_SPINE_COMPACTION/CR238_surcharge_audit.csv) | [All 15 files](../../tests/courtroom/09a-particle-mass-chain-cr238-substrate-spine-compaction/README.md) |
| [`CR:CR239@09a`](../../tests/courtroom/09a-particle-mass-chain-cr239-native-mass-gravity-bridge/README.md) | [CR239_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_PRECOMMIT.md) | [CR239_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_runner.py) | [CR239_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_wrong_controls.csv) | [CR239_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_result.md)<br>[CR239_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_summary.json) | [All 16 files](../../tests/courtroom/09a-particle-mass-chain-cr239-native-mass-gravity-bridge/README.md) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC01_primitive_stack_lock_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock_runner.py) | [LC01_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv)<br>[LC01_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv.sha256.txt) | [LC01_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md)<br>[LC01_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md.sha256.txt)<br>[LC01_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json)<br>[LC01_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC03_qa_ledger_compression_gravity_a_replay_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_qa_ledger_compression_gravity_a_replay_runner.py) | [LC03_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv)<br>[LC03_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv.sha256.txt) | [LC03_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md)<br>[LC03_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md.sha256.txt)<br>[LC03_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json)<br>[LC03_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [LC06_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_wrong_controls.csv) | [LC06_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)<br>[LC06_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json) | [All 10 files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000024`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/MATTER_BOUNDARY_AND_FINITE_CLOSURE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000024 | Matter Foundations | Matter/Substrate Category Boundary and Finite Closure |

| Document field | Value |
|---|---|
| Purpose | Present the category transition from substrate accumulation to finite matter closure, derive the typed matter-support split, and preserve the failed direct source-to-rest-mass bridge that fixes the boundary. |
| Prerequisite documents | `SAMA-D000003` |
| Used by | `SAMA-D000025`; generated from the document catalog |

</details>
