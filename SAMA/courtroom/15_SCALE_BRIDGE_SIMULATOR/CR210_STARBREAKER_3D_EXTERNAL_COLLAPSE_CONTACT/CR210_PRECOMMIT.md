# CR210 Precommit

```text
test_id = CR210
task = Rerun latest Starbreaker 3D and external collapse contact tests then hard-freeze the scoped result
classification = CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION
approval = approved
preflight = PREFLIGHT_20260714_202237_no_script.md
source_repo = C:\VS\The_Basement
source_mutation_allowed = deterministic output regeneration only
new_simulator_parameters = 0
external_fit_parameters = 0
external_signature_count = 1
authority = JSON + CSV + wrapped test logs + SHA-256 manifests
html_role = presentation_only
```

The source boundary is sealed in `CR210_precommit_source_manifest.json` before
the replay. Every listed file must exist before execution. Source code must
remain unchanged, and every regenerated Basement output must reproduce its
precommit SHA-256 digest exactly.

The Courtroom verdict may reach only:

```text
PASS_SCOPED_STARBREAKER_3D_EXTERNAL_COLLAPSE_DIRECTIONAL_CONTACT
```

It may not become a physical compactness calibration, black-hole prediction,
hydrodynamic validation, time-to-collapse result, or promotion of the A packing
law.
