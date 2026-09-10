# CR211 Precommit

Task: verify HH001 Haunted House content against Courtroom data.

This is a Courtroom verification test. It does not ask whether Haunted House is
the Courtroom. It takes the HH001 tables, PDF, and supporting notes as the
submitted work and compares their contents against live Courtroom records.

Pass condition:
- HH001 source files resolve and hash.
- HH001 row counts and Z coverage replay against CR119 periodic rows.
- HH001 Fano address scaffold closes against the SAM R/D/face-state data.
- HH001 CR119-sourced columns match Courtroom data row by row.
- HH001 diagnostic/falsified columns remain recorded as diagnostic/falsified.
- Any HH001 column that is not backed by Courtroom data is explicitly flagged.

Primary Courtroom comparison data:
- CR113, CR114, CR115, CR116 for R, D, 18, 126, and carrier status.
- CR119 for particle, matter, periodic, qA, qA/8, labels, and frontier rows.
- LC02 for the Higgs closed-form replay when H_native/H_reveal wording is
  needed.
- CR210 for the prior HH001 intake and source inventory.

Wrong controls:
- Treat every HH001 column as Courtroom-native without checking source.
- Treat embedded atomic reference values as CR119-derived.
- Hide row mismatches.
- Hide diagnostic failures.
- Use known labels as construction inputs.
- Relabel Z119-Z126 as known elements.
- Promote per-element XOR/action residual diagnostics as closed if they fail.
