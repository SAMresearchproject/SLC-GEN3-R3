[SAM](../../README.md) · [Volume IV](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# RH Radial Compiler — A0, Closure, and the Logarithmic Coordinate

## RH: original signed growth and arithmetic compensation — 14 September 2026

The selected domain is RH-GEN3-GROWTH-V4 on SLC-GEN3-R3. The controlling task remains the original uniform signed-growth estimate for actual Möbius interaction on the common source sequence. The current route uses the exact original-kernel spectrum, dyadic forcing energy, signed admissions and arithmetic compensation. The R2 paper gives exact transport and conditional subpower bounds. Complete scans at scales 32, 512, 4096 and 8192 cover 12,836 prefixes; the half ceiling fails at 13 prefixes, while the unit candidate passes those scans. Four-admission recovery certificates and equal-admission telescoping expose compensation. The uniform arithmetic estimate remains open; independent mathematical review of the R2 paper is pending.

[Current derivations, code and results](../../../research/rh/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The radial compiler is the typed bridge from Volume I accumulation to the real
translation coordinate used by the RH program. The universal floor is

\[
A_0=\frac1{12\pi}.
\]

For a source whose total accumulation closes at `r_c`, normalize the interval
between floor and closure:

\[
q(r)=\frac{A_{\rm total}(r)-A_0}{1-A_0}=\frac{r_c}{r},
\qquad
u=-\log q=\log\frac r{r_c}.
\]

The construction is not a change in the meaning of `A0`. It is an operator
that consumes the accumulation field and emits a real route coordinate.

## 1. Multiplication becomes translation

Under `r -> n r`,

\[
u(nr)=u(r)+\log n.
\]

Ordinary-prime and prime-power scales therefore act as logarithmic
translations. The half-density factor becomes `n^{-1/2}`, matching the
critical centering used by the completed arithmetic.

## 2. Endpoint and Green structure

On the half-line coordinate, the base operator

\[
L=-\frac{d^2}{du^2}+\frac14
\]

has endpoint null modes `e^{u/2}` and `e^{-u/2}`. The endpoint conditions in
the admissible test space remove the common non-decaying modes needed by the
completed formulation. Later Green and tail constructions inherit this route;
they do not rederive `A0` or treat it as a fitted RH parameter.

## 3. Type firewall

- `A0` is the universal accumulation floor.
- `A_total(r)` is a field value.
- `q` is a normalized radial ratio.
- `u` is a logarithmic translation coordinate.
- A prime translation on `u` is not a claim that a prime is a physical radius.
- The radial compiler does not itself prove a positivity theorem.

The recovered A0 relation predates the later explicit primitive names; Volume
I carries that genealogy. Volume IV uses the typed relation without rewriting
the discovery order.

## Evidence and records

Atomic records: `SAMA-C000261-R001`, with inherited A0 records
`SAMA-C000001-R001`, `SAMA-C000257-R001`, and `SAMA-C000258-R001`.
RH result route: `SAMA-RH-R0002`.

Sources: [Volume I technical spine](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md)
and the public radial-compiler source pinned in the provenance matrix.

## Revision boundary

This unapproved chapter installs no physical radial identification, new free
parameter, zero-selection rule, or independent RH result.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000059`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RH_RADIAL_COMPILER_A0_CLOSURE_AND_LOG_COORDINATE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

</details>
