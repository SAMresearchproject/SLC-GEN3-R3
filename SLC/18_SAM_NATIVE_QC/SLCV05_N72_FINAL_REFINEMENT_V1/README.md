# SLC v0.5 N72 final-refinement campaign

This campaign treats the executed H14E shared-cache result as a sealed
baseline and searches for a faster exact local N72 execution revision.  It
does not edit H14E, alter the frozen v0.4 release, change the N72 numerical
object, or change T18 and q semantics.

The search is layered so cheap exact measurements prune weak ideas before
complete-prime or three-prime runs:

1. hardware, topology, cache, filesystem, and power-state diagnostics;
2. kernel arithmetic, allocation, one-index, and fused-chunk micro-tuning;
3. root-batch/cache-amortization and memory-reserve tuning;
4. hybrid P/E-core roster, affinity, queue, and tail tuning; and
5. persistent-pool full-N72 repeatability and independent reconstruction.

Every numerical lane must reproduce the appropriate H14E modular tensor or
the complete H14E operator and 871-coefficient result.  The 8 GiB available-
memory reserve is invariant.  The campaign may run many N72-equivalent
measurements, but full three-prime runs are reserved for configurations that
earn them through exact lower-cost tests.

At completion, the fastest exact reserve-safe repeated full-N72
configuration is installed in a new current-revision artifact.  This is an
owner-requested final refinement of the v0.5 execution candidate, not a
promotion of the still-unexecuted v0.5 N96 release.

