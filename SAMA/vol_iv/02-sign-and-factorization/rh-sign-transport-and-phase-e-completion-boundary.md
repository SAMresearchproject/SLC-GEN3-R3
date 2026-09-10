[SAM](../../README.md) · [Volume IV](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# RH Sign Transport and the Phase-E Completion Boundary

## Conceptual abstract

The completed-Weil inertia campaign establishes an exact transport instrument
before testing whether W9/Theta completion removes negative directions. For a
dimension-`d` source form `G_T`, the rational map

\[
J_T=\begin{bmatrix}I_d\\-I_d\end{bmatrix},\qquad
H_T=\frac14J_TG_TJ_T^T
\]

satisfies `G_T=J_T^T H_T J_T`. It preserves entries and inertia on the
antisymmetric image while exposing the symmetric kernel.

## 1. Correct kernel identity

With

\[
S=\{(x,x)\},\qquad A=\{(x,-x)\}=\operatorname{im}J_T,
\]

the full identity is

\[
\ker H_T=S\oplus J_T(\ker G_T),
\qquad
n_0(H_T)=d+n_0(G_T).
\]

This correction matters because completion adds the symmetric kernel but does
not silently delete a negative direction carried by `G_T`.

## 2. Phase-E test

The installed Theta encoder/decoder and completion predicate verify exact
rational symmetry, reciprocal W9 custody, route and payload identity, local
`A` and `q_A`, complete delivery, and AFC closure. They contain no sign,
inertia, positive-weight, or Gram requirement.

For every positive rational `epsilon`,

\[
G_\epsilon=\operatorname{diag}(\epsilon,-\epsilon)
\]

and its lifted form satisfy the installed completion conditions while retaining
one negative direction. The scoped concept is that the installed W9/Theta
completion conditions alone force negative inertia to vanish and finish the
route. **The test falsifies the concept.**

## 3. Retained value

The exact transport, W9/Theta custody, rational pullback, and sign-resolving
counterfamily remain useful. The failed concept identifies the missing type:
a source-native admissibility or positive incidence rule must connect completed
history to the sign, rather than being inferred from completion itself.

## Evidence and records

Atomic records: `SAMA-C000264-R001`, `SAMA-C000281-R001`,
`SAMA-C000282-R001`.
RH result route: `SAMA-RH-R0005`.

Primary source: [RH current authority, Phase B–E sections](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/rh/RH_CURRENT_AUTHORITY_SNAPSHOT.md).

## Revision boundary

Phase F remains closed and unexecuted. This unapproved chapter does not revive
it or weaken the retained exact sign instrument.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000062`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RH_SIGN_TRANSPORT_AND_PHASE_E_COMPLETION_BOUNDARY.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

</details>
