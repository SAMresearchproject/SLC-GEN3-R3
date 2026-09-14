# Li-6 finite grammar, retained circulation and hidden lift

Date: 2026-09-06. Owner direction: Sean Brady. Technical proposal: Codex.

The authorized trial applies the complete QP093A construction grammar to the
existing Li-6 source geometry, retaining known isotope identity and the
completed H000969/H000974/H000975 sources.

## Objects and source selection

The six one-body addresses retain partition p, depth g, route and conjugation.
Each currently has p=1; p=1 at g=1 remains that address, not a tensor p=12.
The graph contains a K4 core, a residual pair and two depth joins. The four
complete core triangles are the candidate three-owner motifs. A motif cover
uses disjoint triangle edge sets and assigns the remaining relations to pair
motifs. This generates the pair-only cover and four one-triangle covers.

The candidate pair/triad projection matches the constituent partition tuple
to the QP row. It preserves endpoint species, routes and depths as context;
QP charge/conjugation labels are not reassigned as nuclear particle identities.
The rows selected by these tuples are QP093A-0235 (native 12, observed channel
43/4) and QP093A-0115 (native 108, observed channel 72). The center retains its
four existing source leaves and six placements. Native-27 whole-column rows
remain separate presentations and are evaluated as an additional signed probe.
Carrier roles remain infrastructure; the scalar parent and rejected control
rows do not become isotope constituents.

## Executable question and candidate operators

For the actual native T18 direction state, z_e is its complex unit edge
current, m_e is the source reference mask, and j=B(m z) is the saved site
current. This uses the native directions as currents, not as invented
parallel-transport phases. Reversing a cycle edge changes its incidence sign.

- Pair response on a relation: |j_u-j_v|^2.
- Main three-owner response: |sum_{e in triangle} c_e m_e z_e|^2 / 3.
- Endpoint comparison for the same triangle: sum_{e in triangle}
  |j_u-j_v|^2 / 3.
- New depth-loop response: |sum_{e in square} c_e m_e z_e|^2 / 4.

The factors 3 and 4 normalize the squared circulation against the cycle's
edge count. They are fixed before execution. A three-body source instance is
counted once, replaces its three pair motifs, and carries its complete row
coefficient. Both native and catalog observed-channel coefficients are kept.

The existing center action uses its completed TMR1 forms, with a depth-join
block active only when that relation is present. The residual-pair block is
always active. The main candidate source action is the sum of this center
response and the motif-cover response. A paired variant adds the existing
hidden-nine lift 9/16 times the normalized depth-loop response when both
joins are present. This is an additional circulation response of the existing
hidden packet, not a second source-account instance.

The two native-27 column responses are the mean endpoint exposures of their
three retained relations. Their signed surface probe is
(Phi_plus-Phi_minus)/192, in the H000975 convention. It is recorded separately
from the local pair/triad motif action to avoid counting both presentations as
independent copies of the same connections.

The trial asks whether three-owner circulation and the joining-dependent
hidden lift distinguish source histories and assemblies, and what minima and
separated-to-connected changes they produce. The six center placements, five
motif covers, two triad operators, two source coefficient channels, hidden-loop
on/off variants, all 128 rho settings, four reference masks and native/phase-
erased maps remain explicit. No binding-target coefficient is introduced.

## Exact information and hardware plan

The graph's site-incidence and cycle-incidence matrices will be retained.
Their ranks and a rational inverse on a complete set of rows determine whether
site current plus signed circulation recovers the nine edge currents.
Common quarter rotation must preserve every scalar response in this map.

Reuse the completed phase census. Compile center primitive responses and
grammar responses as separate batches with exact inverse address maps. This
avoids materializing their Cartesian product. H14F-14 evaluates direct source
forms, Ryzen-16 uses independent expansions, and the actual 780M contracts
integer features. T500 retains source operands, outputs and independent
readback. Compare calibration configurations before the full run.

The final minimum calculation combines the two exact batches. Its lower-bound
filter retains every potential minimizer; equality and all surviving source
addresses remain recoverable. The controls answer the immediate question:
phase erasure, circulation versus endpoint-only triads, hidden-loop on/off,
source reversal and exact reconstruction.

## Result boundary

The row-to-isotope motif projection and circulation couplings are Codex's
candidate assignments. Results are source-coordinate assembly actions and
their exact minima. Physical tensor selection, spin/magnetic/quadrupole
readouts and a MeV conversion remain named continuation items. Completed
predecessors retain their results and current named replay operations.
