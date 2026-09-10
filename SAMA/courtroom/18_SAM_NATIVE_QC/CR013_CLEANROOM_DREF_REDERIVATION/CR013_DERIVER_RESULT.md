# CR013 DERIVER Result — d_ref cleanroom re-derivation

**Session context:** DERIVER role. Whitelist-only reading. Six files
(W1–W6) in `INPUTS_REDACTED/` were the sole source. No other repo
artifact was opened. No physics question was asked of the operator.

**Tier legend used below:**
- **ATOM** — primitive value, not further derived within the whitelist
- **COMPOSED** — value formed by composing other sealed values through a
  standard formula (Compton composition, etc.)
- **DERIVED-with-citation** — value derived from a specific sealed
  structural claim with the citing whitelist entry named
- **FITTED** — value fitted to an external observation, with the fit
  named
- **UNDERDETERMINED** — not fixed by the whitelist; admissible-set
  reasoning applied

---

## Task 1 — d_ref of the write-to-read pop-bounce-intersect mechanism, in SI meters

### Result

**UNDERDETERMINED as a single SI number.** The whitelist supplies a
natural dilute-limit reach (the substrate closed-loop scale) and states
qualitatively that the actual reach in §1.5's termination condition
depends on pop density; it does not close either (a) which limit governs
the write-to-read mechanism in laboratory conditions or (b) the
projection level from base-substrate to lab SI. Task 4 authorises this
as a CLEAN answer; the admissible set with tier-tagged chains follows.

### Admissible candidate set

#### Candidate A — d_ref = λ_spaghettio = 3.877 μm SI (dilute-limit reach)

This is the substrate closed-loop scale identified in W1 (CR010) §1.2.
It is the natural dilute-limit reach if the write-to-read mechanism's
reach is identified with the loop's own characteristic length (the
self-reunion route: an isolated pop's endpoints rejoin their own
origin because no other pop-endpoints are within the same loop-scale
neighbourhood).

**Tier chain:**

| Step | Value | Tier | Whitelist citation |
|---|---|---|---|
| Primitive arity | ĥ = 2 | **ATOM** | W2 §"Locked Structural Claim" |
| Derived dimension | d̂ = ĥ + 1 = 3 | **DERIVED-with-citation** | W2 §"Locked Structural Claim" (two-mirror reciprocity: 2 in-plane + 1 axis) |
| Tensor-6 identification | ĥ·d̂ = 6 | **DERIVED-with-citation** | W3 §"Locked Structural Claim" |
| eV scale anchor | base_eV ≈ 0.008477 eV | **FITTED** | W4 §"Substrate Derivation Rule" (anchored to PDG Δm²_31 = 2.515 × 10⁻³ eV²) |
| Heaviest neutrino mass eigenstate | m_3 = 6 × base_eV ≈ 50.864 meV | **DERIVED-with-citation** | W4 §"Substrate Derivation Rule" · W3 §"CR001@20 Mass-Ratio Reading" |
| SI constant | ℏc = 197.327 MeV·fm | **ATOM** | W6 §1 (CODATA/SI; c defined exactly) |
| Compton composition | λ_C(m_3) = ℏc / (m_3 c²) ≈ 3.877 μm | **COMPOSED** | Standard Compton formula on the derived m_3 |
| Substrate closed-loop identification | λ_spaghettio ≡ λ_C(m_3) | **DERIVED-with-citation** | W1 §1.2 (structural identification, sealed by CR010) |

**Selection condition for Candidate A**: a sealed statement that the
operative regime for the write-to-read reach is the dilute limit (i.e.,
that the self-reunion route dominates and reach ≈ loop scale). The
whitelist mentions the reach termination condition in §1.5 as cross-
reunion with **other** pops (density-dependent), and refers to the
loop-scale identification in §1.2 as the intrinsic substrate length,
but does not explicitly identify d_ref with λ_spaghettio.

#### Candidate B — d_ref = R^N · λ_spaghettio (Home-nesting projection level)

W1 §1.8 states: *"R-power dressings in downstream coupling laws are
structural consequences of Home-nesting projection levels, not device
parameters."* This admits the possibility that the base-substrate reach
translates into laboratory SI through some R-power (R = 12 per W2's
substrate atom register). The specific exponent N is not derived in the
whitelist.

**Tier chain:**

| Step | Value | Tier |
|---|---|---|
| R substrate atom | R = 12 | **DERIVED-with-citation** — W2 §"Seven Carrier-Atom Reconstructions" (R = ĥ²·d̂ = 12) |
| Home-nesting projection admissibility | R^N as dressing | **DERIVED-with-citation** — W1 §1.8 |
| Exponent N | *(no value)* | **UNDERDETERMINED** |
| Candidate d_ref | R^N × 3.877 μm | **UNDERDETERMINED** (in N) |

**Selection condition for Candidate B**: a sealed derivation of the
specific R-power for the write-to-read mechanism's projection from the
substrate loop-scale to the laboratory SI frame.

#### Candidate C — d_ref not fixed by any lab-coupling observation in the whitelist

W6 (SAM_ON_EARTH v1) §3 states: *"Any uniform substrate rescale of
lengths cancels in the dimensionless ratio d_ref/d on which SAM's
laboratory coupling laws depend."* Under this reading, the laboratory
observable is the ratio d_ref/d and not d_ref alone. Absolute d_ref in
SI meters is therefore not directly constrained by the coupling-law
observables described in the whitelist.

**Tier chain:**

| Step | Statement | Tier |
|---|---|---|
| Ratio-dependence of coupling law | Lab coupling law depends on d_ref/d, not d_ref alone | **DERIVED-with-citation** — W6 §3 |
| Absolute d_ref value | *(unfixed by the lab coupling-law observable)* | **UNDERDETERMINED** |

**Selection condition for Candidate C**: a sealed observable that fixes
d_ref alone (rather than the ratio d_ref/d).

#### Dense-limit alternative — d_ref < λ_spaghettio

W1 §1.5 states the termination condition is intersection with endpoints
of OTHER pops. In the dense limit, the reach is shorter than the
dilute-limit self-reunion reach and functionally proportional to a
negative power of pop density. The whitelist gives the termination
condition qualitatively; it does not supply a mean-free-path functional
form.

**Tier chain:**

| Step | Statement | Tier |
|---|---|---|
| Termination condition | Cross-reunion with endpoints of other pops | **DERIVED-with-citation** — W1 §1.5 |
| Density scaling of reach | Reach decreases with pop density | **DERIVED-with-citation** — W1 §1.5 (qualitative) |
| Mean-free-path functional form | *(no formula)* | **UNDERDETERMINED** |
| Lab-scale pop density | *(no value)* | **UNDERDETERMINED** |
| Dense-limit d_ref in SI | *(no value)* | **UNDERDETERMINED** |

**Selection condition for the dense-limit alternative**: a sealed
mean-free-path formula for the pop-bounce-intersect mechanism, plus a
sealed lab-scale pop density.

---

## Task 2 — Projection factor to lab SI

### Result

**Split by observable.**

**(i) For the coupling-law ratio d_ref/d:** projection factor = 1
(identity). Any uniform substrate rescale cancels in the ratio per W6
§3. **Tier: DERIVED-with-citation** — W6 §3 verbatim clause. No
additional projection factor is required to translate the ratio-form
coupling law into laboratory SI.

**(ii) For absolute d_ref in SI meters:** UNDERDETERMINED.

W1 §1.8 introduces R-power dressings as structural consequences of
Home-nesting projection levels but does not fix the specific R-power N
required for base-substrate → laboratory SI. W6 §3 confirms that
uniform rescale is unfixed by lab-coupling observables. Two consistent
readings remain admissible:

- (ii-a) Adopt the SI-frame anchor as the operational projection: read
  the substrate closed-loop scale directly in SI meters through the W6
  §1 constants table. Under this convention, the projection factor for
  the write-to-read reach IS 1 (i.e., λ_spaghettio quoted directly in
  SI meters, no further dressing). **Tier: DERIVED-with-citation** — W6
  §3 (SI unit lock) plus W1 §1.2 (SI value of λ_spaghettio).
- (ii-b) Adopt an R^N dressing per W1 §1.8. **Tier: UNDERDETERMINED**
  in N.

The whitelist does not decide between (ii-a) and (ii-b).

---

## Task 3 — Density / rate dependence of the reach

### Result

**YES**, the reach is density-dependent per W1 §1.5. **Functional form
is UNDERDETERMINED** in the whitelist.

**What the record says explicitly:**

From W1 §1.5: *"The broken-strand endpoints propagate through the
surrounding spaghettio lattice ('bounce') until they intersect
endpoints of other popped strands elsewhere on the substrate. The
intersection pattern of these bounced endpoints encodes structural
information into the substrate."*

The termination condition — intersection with endpoints of OTHER pops
— is intrinsically a function of concurrent pop density on the
substrate. This gives:

- **Dilute limit** (few pops per loop-scale region): endpoints exhaust
  themselves in self-reunion routes at the loop scale ≈ λ_spaghettio.
  This is the Candidate A upper-bound reach.
- **Dense limit** (many pops per loop-scale region): endpoints
  intersect another pop's endpoint before completing a self-reunion.
  Reach < λ_spaghettio and monotonically decreasing in pop density.

**What the record does NOT give:**

- No mean-free-path formula relating reach to pop density.
- No pop cross-section or endpoint-propagation-dynamics specification
  that would permit derivation of a mean-free-path formula.
- No lab-scale pop-density scale.
- No specification of which limit (dilute or dense) governs the
  write-to-read mechanism at any operating condition.

The functional form of the reach's density dependence is
**UNDERDETERMINED** by the whitelist.

---

## Task 4 — Summary of underdetermination and admissible-set collapse conditions

### Admissible candidates for d_ref (SI meters)

| Candidate | d_ref | Tier of value | What would select it |
|---|---|---|---|
| A (dilute self-reunion) | 3.877 μm | COMPOSED via the chain above | A sealed identification that the write-to-read reach IS the substrate loop scale in the operative regime |
| B (Home-nesting dressed) | R^N × 3.877 μm | DERIVED-with-citation, N UNDERDETERMINED | A sealed derivation of the Home-nesting projection exponent N for the write-to-read mechanism |
| C (ratio-only) | absolute d_ref not observably fixed | META-observation per W6 §3 | A sealed observable that fixes d_ref alone rather than the ratio d_ref/d |
| Dense-limit | < 3.877 μm | UNDERDETERMINED | A sealed mean-free-path formula + a sealed lab-scale pop density |

### Collapse conditions

The admissible set collapses to a single SI value if the following are
sealed by additional content beyond the whitelist:

1. **Regime identification.** Which of {dilute, dense} governs the
   write-to-read mechanism in the operating condition of interest. If
   dilute, Candidate A is selected (up to the projection factor of
   Task 2). If dense, the dense-limit alternative applies but requires
   a functional form.
2. **Projection level.** The R-power N in W1 §1.8's Home-nesting
   dressing, or a sealed statement that the SI-frame anchor (W6) is
   the operational projection with N = 0.
3. **Functional form (if dense).** A sealed mean-free-path formula
   relating reach to pop density, plus a sealed lab-scale pop-density
   scale.
4. **Observable specification.** If Candidate C is the operative
   reading, a sealed observable that fixes d_ref alone (rather than
   d_ref/d) is required for an SI number to be lab-observable at all.

None of 1–4 is closed by the six-file whitelist.

---

## One-line summary

**d_ref in SI meters is UNDERDETERMINED by the six-file sealed record.**
The natural dilute-limit reach is Candidate A: `3.877 μm` (COMPOSED via
CR268 tensor-6 identification, CR001@20 base_eV anchor, standard Compton
composition, and CR010 §1.2 loop-scale identification). Density
dependence of the reach is CONFIRMED as a qualitative feature (CR010
§1.5) but the functional form is UNDERDETERMINED. Projection factor to
lab SI is 1 for the coupling-law ratio d_ref/d (per SAM_ON_EARTH v1 §3)
and UNDERDETERMINED for the absolute d_ref.

## Attribution

Six files opened and read: W1 CR010 (redacted), W2 CR266 (redacted),
W3 CR268 (redacted), W4 CR001@20 (redacted), W5 CR004 (redacted),
W6 SAM_ON_EARTH v1 (redacted). No other repo artifact accessed.
No physics question posed to the operator. This result was written
directly from the sealed record with the tier tags as specified.
