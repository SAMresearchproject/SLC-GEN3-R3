# CR005f Trace-Corrected Weak-CCSN Pixel Bridge Precommit

## Status of CR005e

CR005e stopped on its first Starbreaker scenario before creating a release.
The failure was numerical: independently finite-differenced diagonal tensor
components retained a relative trace residue of
`9.43617769285563e-09`, above the runner's `1e-10` check. No CCSN/Starbreaker
match, null distribution, door statistic, or scientific verdict was opened.
CR005e remains immutable and is not rerun.

## Only permitted correction

For the trace-free quadrupole source,

```text
S_xx + S_yy + S_zz = 0.
```

After the two locked finite differences, CR005f sets

```text
S_zz := -(S_xx + S_yy)
```

before observer projection. The pre-correction numerical residue and the
post-correction residual are both emitted. This is an exact algebraic
projection with zero fitted parameters, not a relaxed threshold.

## Everything else remains frozen

The CR005e source population, waveform doors, post-bounce alignment, 2,049
samples, three-sample edge trim, 48 by 64 pixel grid, thirteen observer
directions, Hellinger statistic, same-door selection, 47 shift nulls, reversal
controls, separable null, evidence ladder, and physical-claim boundary are
unchanged. The CR005e contract is hash-pinned as a CR005f source.

The runner may change campaign identifiers, source paths, trace provenance
fields, and output prefixes only in addition to the exact trace projection.

## Verdict boundary

The run may find a strong, directional, or absent normalized morphology
relationship. It cannot calculate physical strain, luminosity, seconds,
hertz, source distance, detector reach, or prove a shared mechanism.

Same-run repair remains prohibited.
