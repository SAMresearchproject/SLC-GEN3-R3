# Updated native domains and the RH feedback cycle

Owner direction: update SB/A3D41 with the new mathematical information before
running simulations, learn from the updated domains, and return the useful
construction knowledge to RH. Implementation: Codex, 13 September 2026.

The installed successor is GEN3-RXT-R7.1; the initial R7 implementation and its completed results remain preserved. Its admitted source bundles remain the original
source contracts; new operations are implemented in the native C++ engine.
`installation/ACTIVE.json` identifies the installed pod release. The workstation
global SLC and its paused workloads are separate from this pod update.

## Mathematical mapping

SB-GEN3-RXT-R2 adds signed receiver-vector energy repayment to each newly
executed J4 history. For adjacent source phases x,y, each child has one phase
of support, a=b=1. The existing physical action and exact U/D/V/L/M logarithmic
account retain their source definition. The new observable measures the
difference of the two signed receiver vectors; it does not rename that
difference as a propagated physical action.

For positive supports a,b the exact common rule is

    left_energy = ||x||²/a
    right_energy = ||y||²/b
    parent_energy = ||x-y||²/(a+b)
    repayment = ||b*x+a*y||²/[a*b*(a+b)]
    gain = parent_energy-left_energy = right_energy-repayment.

Zero support is admitted only with a zero source vector. These cases are
handled explicitly. The vector identity applies to the scalar RH prime-child
recurrence with its own native Q supports. No physical SB unit becomes an RH
support count.

A3D41-RXT-R3 computes the complete intersection of the minima in source
contexts 3 and 11. Let their energies be E3,E11, with minima m3,m11. Then

    min(E3+E11) >= m3+m11,

and equality occurs exactly at the common minimizers. For an empty
intersection the finite source has strictly positive joint excess. Every
intersection state is preserved in a content-addressed bitmap, with both
original minimum-set witnesses. This includes partial intersections, unequal
minimum counts, and all ties, beyond the earlier identical-four-state target.

## Learning and continued execution

`GEN3_TRANSFER_OBSERVE` reads native outcomes and newly measured SB histories.
`GEN3_TRANSFER_FIT` fits class-balanced exact C++/GMP trees of depth 0..3, selects by development
balanced accuracy, and saves readable rules, source witnesses and exceptions.
A3D41 retains the original whole-pattern train/development/test partition.
SB uses whole-rho partitions, so repeated phases of one rho stay together.
Reserved test rows do not select the models. R7.1 weights the two training classes equally and uses the training prevalence as the classification threshold; displayed leaf probabilities remain the empirical source fractions. If a new tree has no split, the planner uses the existing acquired orbit/channel policy. The original R7 unweighted fit selected a constant common-minimum model; its result and the correction are both preserved.

`GEN3_TRANSFER_PLAN` ranks construction candidates with the acquired common-
minimum model, retaining every probability tie and every candidate. Each
updated native campaign pool observes sampled new families and all SB accounts.
Every eighth pool refits the transfer models. The existing 45-target ingestion
and scheduled training reviews remain active.

The bounded production run first calibrates on 1,024 retained source families
and 128 new SB histories. It then uses previously unused construction ordinals
4,750,000 through 4,782,767: 32,768 families, 1,024 SB histories and 256 horizon
cases. That interval is beyond the original weekend campaign's end ordinal.
Actual native `newly_computed` counts are recorded separately from reused rows. R7.1 executes a further 4,096 unused families from ordinal4,782,768, plus64 SB histories and32 horizon cases, then updates the two established orbit/channel models and their readable rules. Its actual learned RH exception selects a further five-window full-trace question; those results feed back into the installed native RH model.

`GEN3_TRANSFER_RH` checks the shared identity against complete retained RH
prime traces, evaluates the SB model on those actual RH inputs, and trains an
RH-specific model. Its ranked post-minimum variation witnesses generate
explicit neighboring-window full-trace requests through the source-bound
RH_PRIME_VARIATION_R2 operation. The independent 24-lane broad RH queue continues.

## Readable condition behind the transfer exceptions

For scalar RH children with a>0,

    gain > 0 iff a*y² - 2*a*x*y - b*x² > 0.

For x!=0, write r=y/x and beta=b/a. This becomes

    r² - 2*r - beta > 0.

For x=0, the gain is positive exactly when y is nonzero. In SB's two-dimensional
case replace x*y with the inner product and the squares with squared norms.
Thus sign, norm order and support order are useful learned features, while the
exact inequality also depends on the actual ratios. SB's unit phase supports
and RH's varying native Q supports can select different decision branches.

The qualification records this difference: the direct SB rule transfers poorly,
while native RH retraining reaches 5975/6062 balanced accuracy on the retained
largest-scale development rows. All 14,832 exact identity comparisons pass.
The remaining uniform RH task is still the bound on the accumulated positive
gains after a source-selected minimum, with the original N and harmonic scale.
The new rule identifies the positive stages; a uniform magnitude estimate
remains open.

## Execution and recovery records

- `results/R7_DOMAIN_QUALIFICATION.json`: arithmetic, CPU/CUDA complete minima,
  learned fitting, ties, restart, native campaign and actual RH transfer.
- `installation/R7_PROMOTION.json` and `installation/R71_PROMOTION.json`: preserved predecessors and retained native
  models, core memories and RH route learning.
- `results/R7_DOMAIN_FEEDBACK_RUN.json`: actual production progress and receipts.
- `results/R71_FINAL_DOMAIN_FIT.json`: installed balanced learned trees and readable rules; the earlier R7 fit remains preserved.
- `results/R71_FINAL_RH_LEARNING.json`: source-bound RH learning after the new actual calculations.
- `tools/run_domain_feedback_r7.py`: initial bounded execution; `tools/finish_domain_feedback_r71.py` records the corrected installed continuation.

Owner scheduling and storage controls are read before each production pool.
The small isolated qualification used 64-family construction chunks because
the production engine already held 83,632 MiB of GPU workspace. The rejected
larger qualification admissions and corrected runs remain recorded. Production
uses the single installed engine and its existing 640-family CUDA width.
