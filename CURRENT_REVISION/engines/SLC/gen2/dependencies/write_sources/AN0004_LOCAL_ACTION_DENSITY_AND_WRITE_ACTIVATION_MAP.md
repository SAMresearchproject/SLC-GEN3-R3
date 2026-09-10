# AN0004 — Local action density and Write activation

Date: 2026-09-08. Owner: Sean Brady. Technical derivation and execution: Codex.

This continues [AN0003](AN0003_WRITE_TIME_QUARTER_PHASE_GOLDEN_SPHERE_AND_CMB_SCALE.md).
The question was to use R4's capabilities to derive the local action-density
and Write-activation map for the fixed-sphere/Write-clock construction.

**The result is an explicit local geometric phase-action density and an exact
readout of activation from the signed reciprocal interaction.** The complete
native phase/gate grid passes, including active interactions whose scalar
action change is zero. Density varies inside a quarter stroke, while the
identified completed-Write action remains pi*hbar/2.

The work ran in **RH-GEN2-R4-V1, SLC-GEN2-R4, SLC-GEN2-CEV1-R4** through the
saved RH domain session: **65 successful calls, 22 distinct operation names,
870 checks**. The campaign is
[RH_LOCAL_ACTION_ACTIVATION1](../SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/RESULT.md),
with the [full derivation](../SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/DERIVATION.md)
and [actual calculation receipts](../SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/CALCULATION_RECEIPTS.json).

## The source join

The installed J4 source has three phase roles a, b and p. On the native grid,
phi_j=pi*q_j/2, q_j in Z4. Its positive contact account is

    E = 6 - 2 cos(phi_a-phi_p) + 2 cos(phi_b-phi_p).

The owner's Exact Algebra paper supplies

    H_W9 = H_W8 + B Delta H_X1,  B in {0,1}.

SAM_QM supplies

    dS = hbar dphi,  S = integral L_A ds.

The explicit Codex construction identifies the two signed J4 couplings with
a local X1 exchange witness and applies the paper's one Boolean gate to both:

    C_a = -2B exp(i(phi_a-phi_p)),
    C_b = +2B exp(i(phi_b-phi_p)),
    E_B = 6 + Re(C_a+C_b).

At B=1, this agrees with the installed native contact action at all 64 phase
states. At B=0, it gives the declared inactive extension. The construction's
continuous phase pairs are (cos phi_j,sin phi_j). The source join and this
continuous extension are identified derivations; the role names do not yet
assign physical spin, mutual orbit or a mass/site trajectory. E_B is the
native contact account; S is the physical path action under the phase map.

The paper sources and their inspected equations are preserved in the
[owner-source join](../SAM_REVIEW/campaigns/RH_MINIMUM_WRITE_ADVANCE1/OWNER_SOURCE_JOIN.md).
The original supplied files were
`/home/sam/Documents/SAM PAPER/SAM_Exact_Algebra_of_the_Write_2026-08-09(1).docx`
and `/home/sam/Documents/SAM PAPER/SAM_QM.pdf`.

## The local action-density formula

Keep the sphere radius R_H fixed and the original contact reference E_*=6.
Define the source logarithmic latitude and phase derivatives by

    u = ln(E_B/6),
    g_a =  2B sin(phi_a-phi_p) = -Im C_a,
    g_b = -2B sin(phi_b-phi_p) = -Im C_b,
    g_p = -g_a-g_b.

For fixed B,

    du = (g_a dphi_a + g_b dphi_b + g_p dphi_p)/E_B.

R4's fixed-sphere metric is

    ds_j^2 = R_H^2 sech^2(u)(du^2+dphi_j^2).

Under the paper's identified phase-action relation, the one-form is

    omega_j = hbar dphi_j
            = hbar Im[d log(exp(u+i phi_j))].

For a pure role-j stroke with orientation sigma=sign(dphi_j), this gives

    L_j = sigma (hbar/R_H) cosh(u) / sqrt(1+(g_j/E_B)^2),

    D_j^2 := (R_H L_j/hbar)^2
           = (E_B^2+36)^2 / [144(E_B^2+g_j^2)],

    ln |D_j| = (1/2)ln D_j^2.

This is the local geometric density in units hbar/R_H. R4 evaluates its exact
rational square and its exact formal logarithm. The sign remains attached
to the phase direction. Absolute phase is unnecessary for this magnitude:
the signed interaction components supply E_B and all three g_j.

The [complete atlas](../SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/work/core1/ATLAS.json)
contains 128 phase/gate configurations and 384 role-density entries. Its
nine distinct squared values are

    9/13, 9/10, 169/180, 1, 625/612, 625/576,
    169/144, 289/225, 25/9.

Some useful active examples are:

| q=(a,b,p) | E_B | (g_a,g_b,g_p) | D_a^2 | D_b^2 | D_p^2 |
|---|---:|---|---:|---:|---:|
| (0,0,0) | 6 | (0,0,0) | 1 | 1 | 1 |
| (1,0,0) | 8 | (2,0,-2) | 625/612 | 625/576 | 625/612 |
| (0,2,1) | 6 | (-2,-2,4) | 9/10 | 9/10 | 9/13 |
| (2,0,0) | 10 | (0,0,0) | 289/225 | 289/225 | 289/225 |
| (0,2,0) | 2 | (0,0,0) | 25/9 | 25/9 | 25/9 |

For B=0 the atlas supplies inactive geometry reference values D_j^2=1.
Those rows do not count as Writes. Gate changes are separate construction
changes; the density formula does not assign them a duration.

## A quarter Write has fixed action with varying local density

For an admitted monotone completed quarter stroke,

    integral L_j ds_j = sigma*pi*hbar/2,
    integral |L_j| ds_j = pi*hbar/2 = h_P/4.

The cancellation follows directly from L_j ds_j=hbar dphi_j. h_P is Planck's
constant, distinct from SAM h_hat=2. Event count retains the absolute phase
travel, so reversal does not erase completed Writes.

R4 explicitly evaluates interior points of the partner route
(phi_a,phi_b)=(0,pi), phi_p:0->pi/2. With t=tan(phi_p/2):

| t | E_B | D_p^2 |
|---|---:|---:|
| 0 | 2 | 25/9 |
| 1/2 | 18/5 | 2601/3625 |
| 3/4 | 122/25 | 21836929/33890625 |
| 1 | 6 | 9/13 |

Density decreases and then increases within this one quarter stroke. The
t=3/4 value is below every native-grid value. Thus the nine native values
are an endpoint atlas, not continuous extrema. R4's incremental density
history preserves both changes and the net squared-density log ln(81/325).
The three sample intervals remain samples of one Write route.

The corresponding length and time are

    ell_W = R_H integral sech(u) sqrt(1+(g_j/E_B)^2) |dphi_j|,
    tau_W = integral ds_j/v_transfer(s_j).

Assigning R_H and the actual transfer law turns the normalized local map
into a dimensional length and duration. The earlier constant-L formula is
the constant-density case of this integral.

## Activation survives exact scalar cancellation

The complex pair norms give an exact operational gate:

    B = |C_a|^2/4 = |C_b|^2/4
      = (|C_a|^2+|C_b|^2)/8.

At q=000, an active exchange has C_a=-2, C_b=+2 and E_B=6. An inactive
exchange has C_a=C_b=0 and also E_B=6. The signed witness distinguishes the
two exactly. At other phases the needed information can lie in the
imaginary components, which is why preserving both quadratures matters.

Scalar action cancels whenever

    cos(phi_a-phi_p)=cos(phi_b-phi_p).

This occurs in **24 of the 64 active native phase configurations**. On the
declared uniform phase/gate roster, native boundary information returns:

| Readout, after the phase frame is known | Remaining gate information |
|---|---:|
| Scalar E_B | (3/8)ln2 |
| Re C_a only | (1/2)ln2 |
| Im C_a only | (1/2)ln2 |
| One complete complex pair C_a | 0 |
| Both complete complex pairs | 0 |

The norm formula also recovers B when the absolute phase frame is unknown.
These are exact information quantities under the specified test measure;
they are not physical activation probabilities. Native custody preserves
one distinguishing bit in each two-member scalar fiber and recovers both
original B values exactly.

The useful distinction is between **recovering B from an existing exchange**
and **deriving the source dynamics that selects B**. This work completes the
first map. A local matter/spin/site law is the input needed for the second.

## Activation, propagation and completion

The map retains this order:

    local signed exchange -> reconstructed B
      -> legal directed phase route and local L_j
      -> completed quarter advance q -> q+sigma e_j (mod 4)
      -> durable W8 record after transient X1 clears.

The native W7+ example q=000->001 has E_1=6 at both endpoints. It still
returns one directed completed event, preserved shell state 37 and
X1_completion_custody=0. The cleared transient is read after completion;
the reconstructed B describes activation at the interaction.

R4's causal encounter transfers three actual signed witness frames and
recovers every emission by inverse execution. Its declared order ticks
are not seconds. An empty arrival tick remains an explicit zero arrival,
and the transfer performs no maintained-state reset.

For an actual local W7+ source with E_1:6->10, the measured receiver
component initially leaves 16 possible histories and seven action ratios.
R4's adaptive policy selects one exact logarithmic report. The actual
ln(5/3) report recovers the original ratio 5/3 and its one matching history,
then the policy selects STOP. This is a direct use of R4's logarithmic
capability for the source question.

## The mass-density and clock connection

The [earlier CMB source bridge](../SAM_REVIEW/campaigns/RH_MINIMUM_WRITE_ADVANCE1/CMB_SCALE_BRIDGE.md)
retains A0=1/(12pi), C=1/pi, ln(C/A0)=ln12 and c/H0=4457.85554550 Mpc.
The new density formula uses the source reference E_*=6; no equality between
E_B/6 and A/A_* is inserted.

For a declared spherical enclosed-mass account,

    A_M(r)=2G M(<r)/(c^2 r),
    dln A_M/dr = 4pi r^2 rho(r)/M(<r) - 1/r.

If a physical source identifies the sphere latitude with ln(A_M/A_*), its
phase/mass differential must satisfy

    (g/E_B) dot dphi = dln A_M.

At q=(0,2,1), the executed source gives g/E_1=(-1/3,-1/3,2/3). R4 derives
the complete zero-log-change family

    dphi = s(-1,1,0) + t(2,0,1).

One scalar mass-action rate leaves two phase directions free. A local
mass/site/exchange field should therefore retain the signed phase data
when it supplies the actual spin, orbit and progression route. This is the
more informative continuation from the completed local map.

The remaining physical assignments are the source's R_H, its interior
motion-to-phase relation, the dynamics selecting B and the physical transfer
and record-completion law. The normalized density, activation readout and
native completed-event map are now documented and executed.

For the declared construction and these executed maps: **The test result
suggests strong contact with the concept.**

Current authority is [RH live](../SAM_LIVE/02_RH_CURRENT.md). The executable
[handoff](../SAM_REVIEW/campaigns/RH_LOCAL_ACTION_ACTIVATION1/HANDOFF.md)
identifies the precise source checkpoint and continuation. This note does
not change the separate universal RH mathematical frontier.

Negative drift check: CLEAR. Owner disclosure: the signed reciprocal witness
recovers activation even under exact scalar cancellation, and local density
can vary inside one completed Write. These are useful inputs to the physical
mass/phase continuation.
