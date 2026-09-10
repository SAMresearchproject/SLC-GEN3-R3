# CR005 M_native Provenance Audit — Result

**Verdict:** `BOUNDARY`
**Started:** 2026-06-24T22:26:17+00:00
**Completed:** 2026-06-24T22:26:18+00:00

## Headline findings
- Physics-fit inputs in qp093a formulas: **0**
- Physics-fit inputs across upstream CRs (CR221/222/224/225/226/238): **0**
- Smoking-gun (PDG mass literal) matches in input positions: **0**
- Smoking-gun matches in downstream-only contexts: 0
- requires_upstream_audit items remaining: 0

## Verifications
- V-1_formula_audit_written: True
- V-2_upstream_audit_written: True
- V-3_smoking_gun_written: True
- V-4_provenance_chain_written: True
- V-5_cascade_rows_walked: True
- V-6_verdict_resolved: True

## Wrong controls
- WC-1 (R load-bearing): passed=False
- WC-2 (no proton-mass input): passed=True
- WC-3 (downstream allowed): passed=True
- WC-4 (audit surface complete): passed=True

## Pass conditions
- P1_verifications: True
- P2_zero_formula_physics_fit: True
- P3_zero_smoking_gun_inputs: True
- P4_zero_upstream_physics_fit: True
- P5_wrong_controls_pass: False

## Per-upstream-CR classification rollup
- **CR221** (0 constants): {}
- **CR222** (13 constants): {'substrate_atom': 10, 'structural_constant': 3}
- **CR224** (13 constants): {'substrate_atom': 10, 'structural_constant': 3}
- **CR225** (0 constants): {}
- **CR226** (0 constants): {}
- **CR238** (2 constants): {'substrate_atom': 2}

## Interpretation

See [CR005_provenance_chain.md](CR005_provenance_chain.md) for the
per-formula and per-cascade-row construction walks.
See [CR005_formula_audit.csv](CR005_formula_audit.csv) for the
per-input classification of qp093a's M_native formulas.
See [CR005_upstream_cr_audit.csv](CR005_upstream_cr_audit.csv) for
the per-upstream-CR declared-constant audit.
See [CR005_smoking_gun_search.csv](CR005_smoking_gun_search.csv) for
every PDG-mass literal match with file/line/context.

## Appeal path

Per CR005_PRECOMMIT.md §APPEAL: BOUNDARY items may be regraded if
each requires_upstream_audit item is named, bounded, and resolved
(or formally deferred to a follow-on CR005a).
