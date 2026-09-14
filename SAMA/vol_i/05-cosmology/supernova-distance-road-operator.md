[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Supernova Distance-Road Operator

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

A supernova catalog supplies a redshift \(z\) and a luminosity-distance
readout encoded by distance modulus. Volume I asks how that readout changes
when the global accumulation road is made explicit. The operator is fixed in
two steps:

\[
A_{\rm los}(z)=\frac1\pi\left[1-(1+z)^{-3}\right],
\]

\[
D_{\rm native}(z)=D_{\rm readout}(z)[1-A_{\rm los}(z)].
\]

Because distance modulus is logarithmic, the same conversion becomes

\[
\mu_{\rm native}
=\mu_{\rm obs}+5\log_{10}[1-A_{\rm los}(z)].
\]

That compact result is the endpoint of a longer research chain. The early
tests got the direction of the road right, exposed an absolute-scale offset,
separated that offset from residual shape pressure, and found that native
source curvature could not be treated as the sole selector. Later work fixed
the explicit redshift road, built an exact 1,701-row ledger, kept the BAO
ledger independent, preserved a boundary verdict whose gate logic was wrong,
and installed a corrected appeal using identical numerics. This chapter keeps
every one of those steps because the deviations explain why the settled
operator has its present type and custody.

## 1. Opening question

The chapter asks:

> Given a supernova luminosity-distance readout, does the settled global road
> define a zero-catalog-fit native distance and modulus ledger from beginning
> to end, and does the registered correction chain preserve the failed or
> diagnostic stages that selected its valid boundary?

There are three questions nested inside it:

1. What is the algebraic distance conversion?
2. How is that conversion transported into magnitude space?
3. Which parts of the historical discovery chain are formulas, which are
   diagnostics, and which execution carries the authorized classification?

The conceptual picture is a catalog ruler with two coordinate markings. The
observed modulus encodes the conventional readout distance; the fixed
\(1-A_{\rm los}(z)\) road factor maps that same row to its native-distance
marking before any residual is scored.

## 2. Typed inputs, outputs and units

| Quantity | Definition/role | Type | Units/domain |
|---|---|---|---|
| \(A_0\) | \(1/(12\pi)\) | universal accumulation floor | dimensionless |
| \((R,D)\) | \((12,3)\) | locked global-road primitives | dimensionless |
| \(z\) | catalog redshift | line-of-sight coordinate | \(z\ge0\) |
| \(A_{\rm los}(z)\) | \((1/\pi)[1-(1+z)^{-3}]\) | global accumulation road | dimensionless |
| \(f_A(z)\) | \(1-A_{\rm los}(z)\) | native/readout road fraction | dimensionless, positive |
| \(D_{\rm readout}\) | conventional luminosity-distance coordinate | observed/catalog readout | Mpc |
| \(D_{\rm native}\) | \(D_{\rm readout}f_A\) | substrate-native road distance | Mpc |
| \(\mu_{\rm obs}\) | catalog distance modulus | logarithmic readout | mag |
| \(\mu_{\rm native}\) | native-road modulus | transformed readout | mag |
| \(H_0\) | declared external distance-scale input | calibration input, not catalog-fit parameter | km s\(^{-1}\) Mpc\(^{-1}\) |

The road is not a host-galaxy source field. Host stellar mass does not appear
in \(A_{\rm los}(z)\), \(f_A(z)\), or the modulus conversion. The locally
measured light speed remains \(c\); \(f_A=c_{\rm eff}/c\) is a coordinate-road
ratio.

## 3. Derive the native distance operator

Start from the global road established in `SAMA-D000010`:

\[
A_{\rm los}(z)=A_0R[1-(1+z)^{-D}].
\]

Insert \(A_0=1/(\pi R)\) and \(D=3\):

\[
A_{\rm los}(z)=\frac1\pi[1-(1+z)^{-3}].
\]

The native fraction of the conventional road is

\[
f_A(z)=\frac{c_{\rm eff}(z)}c=1-A_{\rm los}(z).
\]

Therefore

\[
\boxed{
D_{\rm native}(z)=D_{\rm readout}(z)f_A(z)
=D_{\rm readout}(z)[1-A_{\rm los}(z)]
}.
\]

The inverse form is useful when a native source curve is being mapped forward
to its readout coordinate:

\[
\boxed{
D_{\rm readout}(z)=\frac{D_{\rm native}(z)}{1-A_{\rm los}(z)}
}.
\]

These are the same identity solved in opposite directions. The historical
G397 notation used a native source curve \(D_{\rm source}\) and wrote its
road-stretched representation as \(D_{\rm SAM}=D_{\rm source}/(1-A)\).
The later catalog ledger starts from the readout and recovers its native road
by multiplication. Reversing the direction of the map is not a sign change.

### 3.1 Boundary behavior

At \(z=0\), \(A_{\rm los}=0\), so

\[
D_{\rm native}(0)=D_{\rm readout}(0).
\]

At high redshift,

\[
\frac{D_{\rm native}}{D_{\rm readout}}
\longrightarrow1-\frac1\pi.
\]

The conversion is therefore zero at the origin, monotone in magnitude and
bounded. It is not a fixed percentage correction applied to every catalog
row.

### 3.2 Worked distance example

At \(z=1\),

\[
A_{\rm los}(1)
=\frac1\pi\left(1-2^{-3}\right)
=\frac7{8\pi}
\approx0.278521.
\]

Thus

\[
f_A(1)\approx0.721479.
\]

A readout distance of \(1000\) Mpc maps to a native distance of about
\(721.479\) Mpc. This arithmetic illustrates the operator; it is not a
substitute catalog comparison.

## 4. Derive the luminosity-modulus operator

Distance modulus is

\[
\mu=5\log_{10}\left(\frac{D_L}{10\ \mathrm{pc}}\right).
\]

For \(D_L\) in Mpc, the equivalent form is

\[
\mu=5\log_{10}\left(\frac{D_L}{\mathrm{Mpc}}\right)+25.
\]

Apply the native distance conversion:

\[
\mu_{\rm native}
=5\log_{10}\left(
\frac{D_{\rm readout}[1-A_{\rm los}]}{10\ \mathrm{pc}}
\right).
\]

Use \(\log(ab)=\log a+\log b\):

\[
\mu_{\rm native}
=5\log_{10}\left(\frac{D_{\rm readout}}{10\ \mathrm{pc}}\right)
+5\log_{10}[1-A_{\rm los}].
\]

The first term is \(\mu_{\rm obs}\). Hence

\[
\boxed{
\mu_{\rm native}(z)
=\mu_{\rm obs}(z)+5\log_{10}[1-A_{\rm los}(z)]
}.
\]

Since \(0<1-A_{\rm los}\le1\), the road term is nonpositive. For small
\(A_{\rm los}\), expand \(\ln(1-A)=-A-A^2/2-\cdots\):

\[
5\log_{10}(1-A)
=\frac5{\ln10}\ln(1-A)
\simeq-\frac5{\ln10}A+O(A^2).
\]

The shift therefore approaches zero continuously at low redshift. At the
worked \(z=1\) example, it is approximately

\[
5\log_{10}(0.721479)\approx-0.709\ \mathrm{mag}.
\]

The exact ledger evaluates the row formula rather than this rounded example.

## 5. Supernova discovery and correction chain

The discovery chain is preserved in its actual order because each stage
answers a different technical question.

### 5.1 G375: establish the sign/category result

`G:G375@SAM-ARCHIVE` tested the prior statement that positive accumulated
road makes source separation shorter than the observed road. Its source
equation was written additively,

\[
D_{\rm obs}=D_{\rm source}+D_{A\text{-road}},
\]

so positive bounded \(D_{A\text{-road}}\) implies

\[
D_{\rm source}<D_{\rm obs}.
\]

The zero-road control makes the distances equal, the sign-flipped road makes
the source farther away, and a road larger than the observed distance yields
an invalid nonpositive source distance. This stage establishes direction, not
the final redshift law.

### 5.2 G397: freeze a curve and expose the shape gap

`G:G397@SAM-ARCHIVE` used the historical native source curve

\[
D_{\rm source}(z)=\frac c{H_0}z\left(1+\frac{3z}{20}\right)
\]

and the forward road map

\[
D_{\rm SAM}=\frac{D_{\rm source}}{1-A_{\rm measure}}.
\]

One weighted magnitude offset per dataset was allowed as a frozen nuisance.
The result preserved `LCDM_SHAPE_GAP_VISIBLE`: the sign survived, but an
absolute-scale offset and a residual redshift-dependent shape could not be
collapsed into one undifferentiated discrepancy.

### 5.3 G398: keep the failed shape pressure visible

`G:G398@SAM-ARCHIVE` separated raw one-sided residuals from aligned residual
shape. After the G397 offset, Pantheon and DES were no longer simply one-sided,
but both retained a positive redshift slope. The source recorded this as road-
amplitude and source-curvature pressure. Parameter scans in this stage were
diagnostic; they were not promotion of a fitted final law.

This is the meaningful failure in the discovery chain: sign correctness and a
constant alignment did not finish the curve shape.

### 5.4 G398B: isolate the constant-scale diagnostic

`G:G398B@SAM-ARCHIVE` recorded raw offsets

\[
0.1677763450\ \mathrm{mag}\quad(\mathrm{DES-Y5}),
\]

\[
0.2537315055\ \mathrm{mag}\quad(\mathrm{Pantheon}),
\]

\[
0.3042073809\ \mathrm{mag}\quad(\mathrm{Union3}),
\]

with a common weighted value \(0.1977115918\) mag. It also emitted
\(H_0\)-equivalent scale values, but explicitly typed them as diagnostics,
not promoted cosmological measurements. This prevents a scale conversion from
being mistaken for a new fitted physical constant.

### 5.5 G399: correct the order of interpretation

`G:G399@SAM-ARCHIVE` selected the constant-scale lane first and dataset zero
points second. The correction was conceptual as well as numerical: a common
distance-scale mismatch should be identified before assigning every part of
it to dataset-specific calibration. The test explicitly did not replace the
then-declared CMB-lane \(H_0\).

### 5.6 G400: retest native source curvature

`G:G400@SAM-ARCHIVE` retained the native source-curvature term

\[
q_{\rm native}=\frac3{18_{12}}=\frac3{20},
\]

but found it was not the sole residual selector. Its diagnostic scan located a
different best \(q\), while the native term remained framework provenance.
The correction was not to discard \(3/20\); it was to stop asking source
curvature alone to carry road response.

### 5.7 G401: preserve source curvature inside a coupled selector

`G:G401@SAM-ARCHIVE` held the native \(3/20\) source term fixed and varied a
road-coupling diagnostic. It recorded better diagnostic scores than a
source-curvature-only scan. This stage established the source/road split but
did not install the scan parameter as the settled cosmological road.

### 5.8 G688c: replace the diagnostic lane with the explicit global road

`G:G688c@SAM-ARCHIVE` applied the settled
\(A_{\rm los}(z)\) directly to all 1,701 rows:

\[
z\mapsto A_{\rm los}(z)
\mapsto c_{\rm eff}(z)
\mapsto D_{\rm native}(z).
\]

It recorded maximum distance-identity error
\(1.136868377216\times10^{-13}\) Mpc, centered RMS changing from
\(0.201749994\) mag to \(0.146364056\) mag, and a bin-range reduction of
\(0.759555937\). This is the constructive handoff from historical selector
diagnostics to the explicit formula used by the Courtroom ledger.

## 6. Supernova distance ledger and replay

### 6.1 CR013: exact row construction

[`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) recomputed 1,701 supernova rows. For each row, the execution
evaluated

\[
A_{\rm los}(z_i),\quad
c_{\rm eff}(z_i),\quad
D_{{\rm native},i},\quad
\mu_{{\rm native},i}
\]

and recorded zero maximum error for every declared row identity. The low-\(z\)
mean accumulation was \(0.006234707158\); the high-\(z\) mean was
\(0.292724398411\). BAO inputs were not loaded.

### 6.2 CR015: independent-ledger control

[`CR:CR015@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr015-sn-bao-independent-ledger-lock/README.md) required SN and BAO ledger functions to be defined before their
same-\(z\) overlap was inspected. It recorded zero identity error and maximum
overlap shrinkage difference \(0.240000\%\). The overlap is a witness after
independent construction, not a formula source for either probe.

### 6.3 CR017: typed closure boundary

[`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) closed the branch only after the typed bridge, SN ledger, BAO
ledger, independent lock and compressed acoustic ratio existed as local CR
dependencies. It kept CMB modal and polarization closure explicitly open.
Thus the distance road could close without absorbing an unexecuted full-CMB
claim.

### 6.4 CR018 to CR018b: preserve the result and correct the gate logic

The original CR018 execution remains sealed. Its direct prediction conditions
passed, but its verdict was `BOUNDARY` because three auxiliary sensitivity
thresholds were treated as load-bearing gates. The correction did not erase
that run or change its numerical content.

[`CR:CR018b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr018b-sam-zero-parameter-sn-bao-distance-verdict-ladder-appeal/README.md) replayed the identical inputs, seeds and 1,000-trial null
distributions while restructuring the verdict ladder:

| Layer | Role after correction |
|---|---|
| P1 supernova prediction versus data | load-bearing gate |
| P2 BAO prediction versus data | load-bearing gate |
| P3 drag-ruler comparison | load-bearing gate |
| E4 probe-split sweep | reported sensitivity evidence |
| E5 SN null distribution | reported sensitivity evidence |
| E6 BAO null distribution | reported sensitivity evidence |

For the supernova member, the appeal records

\[
n_{\rm SN}=1580,
\qquad H_0=73.04\ \mathrm{km\,s^{-1}\,Mpc^{-1}},
\]

\[
\boxed{
\overline{\Delta\mu}_{\rm weighted}=-0.0090723\ \mathrm{mag}
}.
\]

The \(H_0\) value is a declared external calibration input, not a fit to the
catalog. No magnitude offset and no host-log-mass correction are fitted. The
appeal supplements CR018 and is the downstream citation; the original
boundary result remains in the audit trail.

### 6.5 LC07: locked-stack retest

[`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) starts from \(R=12,D=3,A_0=1/(12\pi)\), reconstructs all 1,701 SN
rows, and records maximum modulus identity error
\(7.105427357601002\times10^{-15}\). It rejects \(D\)-refitting, bin
cherry-picking, target substitution, shared-data leakage and overlap
overstatement. Its 113 checks pass and all 10 registered wrong controls reject.

## 7. Wrong controls and what they teach

| Wrong or diagnostic route | Failure mode | Correct route |
|---|---|---|
| Set \(A_{\rm los}=0\) | Removes the native/readout distinction and reverts every row to its conventional road. | Evaluate the fixed redshift operator row by row. |
| Flip the road sign | Makes positive accumulated road expand native distance beyond readout, contrary to the established sign packet. | Use \(D_{\rm native}=D_{\rm readout}(1-A_{\rm los})\). |
| Apply one constant percentage | Violates \(A_{\rm los}(0)=0\) and its redshift dependence. | Retain the bounded \(z\)-dependent fraction. |
| Insert host stellar mass | Changes a global line-of-sight road into a source-environment correction. | Keep the host term absent from this operator. |
| Fit a catalog offset into the operator | Converts a fixed transformation into a nuisance fit and confuses scale diagnostics with road law. | Declare external calibration and zero catalog-fit parameters. |
| Treat diagnostic \(H_0\)-equivalents as measurements | Promotes scale bookkeeping beyond its source boundary. | Preserve them as historical diagnostics only. |
| Use source curvature alone | Leaves the aligned residual shape pressure seen in G398/G400. | Keep source curvature typed and use the settled explicit road. |
| Load BAO rows to construct the SN ledger | Creates cross-probe leakage. | Build SN independently; inspect overlap afterward. |
| Refit \(D\) or select bins | Mutates the primitive stack or target population after seeing outputs. | Lock \(D=3\) and replay every declared row. |
| Treat auxiliary null thresholds as direct gates | Repeats the CR018 verdict-ladder error. | Gate on declared direct prediction conditions and report sensitivity evidence separately. |

## 8. Established result, boundary and forward handoff

The native supernova operator is

\[
\boxed{
D_{\rm native}=D_{\rm readout}[1-A_{\rm los}(z)],
\qquad
\mu_{\rm native}=\mu_{\rm obs}+5\log_{10}[1-A_{\rm los}(z)].
}
\]

The registered direct anchor uses 1,580 post-cut Pantheon+SH0ES rows at the
declared \(H_0=73.04\) input and records weighted mean residual
(-0.0090723) mag, with zero catalog-fit parameters and no host-mass
correction.

For the scoped distance chain carried by [`CR:CR018b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr018b-sam-zero-parameter-sn-bao-distance-verdict-ladder-appeal/README.md) and replayed by
[`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md):

**The test result suggests strong contact with the concept.**

The classification does not state that the Hubble probe split is closed, does
not merge the SN and BAO calibrations, and does not extend the compressed
distance result into full recombination, modal or polarization physics.
`SAMA-D000012` receives the independent BAO projection and ruler bridge.

Exact evidence is the complete registered sequence in Section 9. The
specifically open boundary is the Hubble-probe split, independent BAO
calibration and full recombination, modal and polarization development beyond
the scoped luminosity-road operator.

## 9. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result |
|---|---|---|---|
| `G:G375@SAM-ARCHIVE` | Sign premise | `G375_SN_A_ROAD_STRETCH_PRIOR_PREDICTION_SIGN_PASS`; positive road implies shorter native/source distance. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G375_SN_A_ROAD_STRETCH_PRIOR_PREDICTION/G375_output.json) |
| `G:G397@SAM-ARCHIVE` | Frozen-curve premise | `G397_PASS_FROZEN_DISTANCE_CURVE_PREFLIGHT__LCDM_SHAPE_GAP_VISIBLE`; scale and shape not conflated. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G397_FROZEN_SN_DISTANCE_CURVE_PREFLIGHT/G397_output.json) |
| `G:G398@SAM-ARCHIVE` | Preserved failure/diagnosis | `G398_PASS_DISTANCE_RESIDUAL_SHAPE_LOCALIZED__RAW_OFFSET_PLUS_ROAD_AMPLITUDE_PRESSURE`; aligned shape pressure retained. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G398_DISTANCE_RESIDUAL_SHAPE_DIAGNOSIS/G398_RESULT.md) |
| `G:G398B@SAM-ARCHIVE` | Scale control | `G398B_PASS_SN_RAW_OFFSET_CONSTANT_DOMINANT__CURVE_GROWTH_SECONDARY`; \(H_0\)-equivalents remain diagnostics. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G398B_SN_CONSTANT_OFFSET_DIAGNOSTIC/G398B_RESULT.md) |
| `G:G399@SAM-ARCHIVE` | Interpretation correction | `G399_PASS_SN_OFFSET_IS_SCALE_LANE_FIRST__DATASET_ZERO_POINT_SECOND`; no replacement \(H_0\) claim. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G399_SN_CONSTANT_SCALE_ORIGIN_SELECTOR/G399_RESULT.md) |
| `G:G400@SAM-ARCHIVE` | Retest | `G400_PASS_NATIVE_3_OVER_18_RECORDED__SOURCE_CURVATURE_NOT_SOLE_SELECTOR`; native source term retained with boundary. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G400_SN_NATIVE_CURVATURE_AFTER_SCALE/G400_RESULT.md) |
| `G:G401@SAM-ARCHIVE` | Coupling boundary | `G401_PASS_NATIVE_SOURCE_SURVIVES_AS_ROAD_COUPLED_SELECTOR`; diagnostic coupling not promoted as final road. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G401_SN_NATIVE_SOURCE_ROAD_COUPLING/G401_RESULT.md) |
| `G:G688c@SAM-ARCHIVE` | Explicit road construction | `G688c_PASS_Z_A_EFFECTIVE_LIGHT_SPEED_RULER_BUILDS_NATIVE_DISTANCE_LANE`; 1,701-row explicit conversion. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G688c_Z_A_EFFECTIVE_LIGHT_SPEED_RULER/G688c_RESULT.md) |
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | SN ledger construction | Source execution `CLEAN`, scientific verdict `PASS`; exact 1,701-row identities and no BAO input. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md) |
| [`CR:CR015@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr015-sn-bao-independent-ledger-lock/README.md) | Independent-ledger control | Source execution `CLEAN`, scientific verdict `PASS`; zero identity error and \(0.240000\%\) maximum overlap witness. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_result.md) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | Typed closure boundary | Source execution `CLEAN`, scientific verdict `PASS`; compressed distance closure with modal/polarization open. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md) |
| [`CR:CR018b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr018b-sam-zero-parameter-sn-bao-distance-verdict-ladder-appeal/README.md) | Corrected direct anchor | Preserved appeal `PASS`; 1,580 SN rows, \(-0.0090723\) mag weighted residual, zero catalog-fit parameters. **The test result suggests strong contact with the concept.** | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_result.md) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | Locked-stack replay | `LC07_PASS_SN_BAO_DISTANCE_ROAD_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; full rows, 113/113 checks, 10/10 controls. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md) |

## 10. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000001-R001` | Supplies the universal floor upstream of the global road. |
| `SAMA-C000060-R001` | Supplies the effective traversal-distance identity. |
| `SAMA-C000062-R001` | Defines \(A_{\rm los}(z)\). |
| `SAMA-C000065-R001` | Defines native cosmological distance conversion. |
| `SAMA-C000066-R001` | Derives the luminosity-modulus conversion and excludes a host term. |
| `SAMA-C000067-R001` | Records the direct SN ledger and classified anchor. |
| `SAMA-C000068-R001` | Enforces independent probe ledgers and calibration typing. |
| `SAMA-C000122-R001` | Enforces the Volume I subject and cross-volume boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source statuses, authorized classification and false approval state. |

## 11. Source chronology and approval boundary

The eight G records preserve the historical discovery route. Their selectors,
offsets and source-era interpretive labels do not supersede the settled
global-road identity. The five Courtroom/Last Campaign keys preserve the later
ledger, independence control, typed closure, corrected appeal and locked-stack
replay. Courtroom links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

Executable artifacts control their numerical results. Active `SAM_LIVE`
documents control present-tense authority. Volume I owns the distance-road
operator; matter grammar remains Volume II and executable internals remain
Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. The
authorized strong-contact classification, source fidelity, correction logic
and mechanical validation do not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | [CR013_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_PRECOMMIT.md)<br>[CR013_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_declared_premises.json) | [CR013_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_runner.py) | [CR013_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_candidate_rows.csv) | [CR013_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md)<br>[CR013_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_summary.json) | [All 8 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) |
| [`CR:CR015@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr015-sn-bao-independent-ledger-lock/README.md) | [CR015_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_PRECOMMIT.md)<br>[CR015_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_declared_premises.json) | [CR015_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_runner.py) | [CR015_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_candidate_rows.csv) | [CR015_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_result.md)<br>[CR015_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK/CR015_summary.json) | [All 10 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr015-sn-bao-independent-ledger-lock/README.md) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | [CR017_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_PRECOMMIT.md)<br>[CR017_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_declared_premises.json) | [CR017_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_runner.py) | [CR017_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_candidate_rows.csv) | [CR017_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md)<br>[CR017_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_summary.json) | [All 10 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) |
| [`CR:CR018b@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr018b-sam-zero-parameter-sn-bao-distance-verdict-ladder-appeal/README.md) | [CR018b_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_PRECOMMIT.md)<br>[CR018b_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_declared_premises.json) | [CR018b_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_runner.py) | [CR018b_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_runner.py)<br>[CR018b_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_result.md)<br>[CR018b_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_summary.json) | [CR018b_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_result.md)<br>[CR018b_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL/CR018b_summary.json) | [All 8 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr018b-sam-zero-parameter-sn-bao-distance-verdict-ladder-appeal/README.md) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [LC07_bao_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_bao_candidate_rows.csv)<br>[LC07_cmb_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_cmb_candidate_rows.csv)<br>[LC07_sn_bao_independent_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_bao_independent_candidate_rows.csv)<br>[LC07_sn_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_candidate_rows.csv)<br>[LC07_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_wrong_controls.csv) | [LC07_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md)<br>[LC07_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_summary.json) | [All 17 files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000011`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/SUPERNOVA_DISTANCE_ROAD_OPERATOR.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000011 | Cosmological Distance | Native Supernova Distance and Luminosity-Distance Ledgers |

| Document field | Value |
|---|---|
| Purpose | Derive the native distance and luminosity-modulus operators, preserve the complete supernova discovery/deviation/correction chain, and route the independent ledger through its corrected zero-parameter appeal and locked-stack replay. |
| Prerequisite documents | `SAMA-D000002`, `SAMA-D000010` |
| Used by | `SAMA-D000012`; focused child of `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
