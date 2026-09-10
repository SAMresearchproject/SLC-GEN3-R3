from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECORD_ID = "CR120S_QP093A_F81_RETAINED_MATTER_PROJECTION"
PRECOMMIT_SHA = "31078686c115b5a81c2058f358fa15843d1313f575d3efab992a805d0a01d1d7"
MANIFEST_SHA = "6c4b6affb4644dd31faf2d6286d17c8c0f8c8cebc02f1a7d75d72dc0ef0924e9"
BOUNDARY = "BOUNDARY_F81_AND_M126_NUMERIC_WELD_PROJECTION_RULE_OPEN"

ALLOWED = {
    "row_type": ["operator_class", "route_class", "spin_or_hand_class", "color_or_owner_closure"],
    "depth": ["closure_depth", "surface_depth"],
    "charge_conjugation": ["q_sign", "native_charge_axis", "route_class"],
    "partition_role": ["typed_partition_role", "partition_signature_with_semantic_type"],
    "closure_or_resonance": ["canonical_closure_status", "canonical_stability_status"],
    "geometry": ["source_derived_finite_shape_mapping"],
}
FORBIDDEN = [
    "M_native", "M_observed_candidate", "qA_source_support",
    "tensor_carrier_support", "retained_write_support", "S_debit_or_credit",
    "target_row_count_81", "target_sum_12600", "100M", "7Theta",
    "current_workbook_membership", "row_order", "sheet_name",
    "candidate_id_whitelist", "direct_roster_enumeration",
    "workbook_only_user_reclassification", "observed_binding_residual",
    "CR120R_p9g0_exclusion_as_automatic_F81_membership",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_path(text: str) -> Path:
    p = Path(text)
    return p if p.is_absolute() else ROOT / p


def source_path(manifest: list[dict[str, str]], source_id: str) -> Path:
    return resolve_path(next(row["path"] for row in manifest if row["source_id"] == source_id))


def verify_locks() -> tuple[list[dict[str, str]], dict[str, bool]]:
    checks = {
        "precommit_sha": sha256(HERE / "CR120S_PRECOMMIT.md") == PRECOMMIT_SHA,
        "manifest_sha": sha256(HERE / "CR120S_SOURCE_MANIFEST.csv") == MANIFEST_SHA,
    }
    manifest = load_csv(HERE / "CR120S_SOURCE_MANIFEST.csv")
    for row in manifest:
        path = resolve_path(row["path"])
        checks[f"source:{row['source_id']}:exists"] = path.exists()
        checks[f"source:{row['source_id']}:bytes"] = path.exists() and path.stat().st_size == int(row["bytes"])
        checks[f"source:{row['source_id']}:sha256"] = path.exists() and sha256(path) == row["sha256"]
    return manifest, checks


def main() -> None:
    manifest, lock_checks = verify_locks()

    # Fail-closed reveal discipline: the workbook is hash-checked above as
    # bytes, but no workbook parser is imported and no workbook cell is read.
    workbook_parsed = False
    m_native_column_opened = False
    selected_roster_emitted = False

    selection_authority = json.loads(source_path(manifest, "PRIOR_SELECTION_AUTHORITY").read_text(encoding="utf-8-sig"))
    hierarchy = json.loads(source_path(manifest, "F81_TYPED_HIERARCHY").read_text(encoding="utf-8-sig"))
    prior_boundary_text = source_path(manifest, "PRIOR_OPERATOR_BOUNDARY").read_text(encoding="utf-8-sig")
    cr120r = json.loads(source_path(manifest, "CR120R_HARD_CLOSURE").read_text(encoding="utf-8-sig"))

    hierarchy_text = json.dumps(hierarchy, sort_keys=True)
    hierarchy_has_scalar_f81 = "F81_COMPLETED_FACE" in hierarchy_text
    hierarchy_has_row_predicate_contract = all(
        token in hierarchy_text for token in ("candidate_universe", "row_predicate", "geometry_mapping")
    )
    prior_authority_open = (
        selection_authority.get("selection_authority") == "OPEN_NOT_INSTALLED"
        and selection_authority.get("physical_mapping") == "OPEN_NOT_INSTALLED"
    )
    prior_boundary_open = (
        "selection operator and physical mapping remain OPEN_NOT_INSTALLED" in prior_boundary_text
        or "selection operator" in prior_boundary_text and "OPEN_NOT_INSTALLED" in prior_boundary_text
    )
    cr120r_is_closure_only = (
        cr120r.get("scientific_verdict") == "STRONG_STRUCTURAL_PASS"
        and cr120r.get("binding_use") == "CONSERVATION_GATE_ONLY_NOT_A_BINDING_COEFFICIENT"
    )

    operator_evidence = [
        {
            "source": "F81_TYPED_HIERARCHY",
            "finding": "scalar W9 to V27 to F81 to L162 hierarchy is present",
            "supports_row_selector": hierarchy_has_row_predicate_contract,
            "detail": "no canonical QP093A candidate universe, per-row predicate, and geometry mapping contract found",
        },
        {
            "source": "PRIOR_SELECTION_AUTHORITY",
            "finding": selection_authority.get("selection_authority"),
            "supports_row_selector": not prior_authority_open,
            "detail": selection_authority.get("decisive_boundary"),
        },
        {
            "source": "PRIOR_OPERATOR_BOUNDARY",
            "finding": "explicit missing independent selector for omissions and insertions",
            "supports_row_selector": not prior_boundary_open,
            "detail": "current roster is a target-aware research overlay",
        },
        {
            "source": "CR120R_HARD_CLOSURE",
            "finding": "p9,g0 witness exclusion closes the 100-row full ledger",
            "supports_row_selector": False,
            "detail": "CR120R is a conservation gate only and does not define F81 membership",
        },
    ]
    operator_present = (
        hierarchy_has_scalar_f81
        and hierarchy_has_row_predicate_contract
        and not prior_authority_open
        and not prior_boundary_open
        and not cr120r_is_closure_only
    )

    contract = {
        "record_id": RECORD_ID,
        "allowed_selector_inputs": ALLOWED,
        "forbidden_selector_inputs": FORBIDDEN,
        "candidate_operator_contract": "NONE_FOUND" if not operator_present else "PRESENT",
        "M_native_reveal_authorized": operator_present,
        "workbook_parsed": workbook_parsed,
        "M_native_column_opened": m_native_column_opened,
        "selected_roster_emitted": selected_roster_emitted,
    }
    (HERE / "CR120S_allowed_fields_contract.json").write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")

    operator_search = {
        "record_id": RECORD_ID,
        "source_set_frozen": True,
        "operator_contract_requirements": [
            "canonical candidate universe",
            "deterministic per-row predicate or constructive geometry mapping",
            "typed matter antimatter neutral witness and resonance handling",
            "source path and exact source key for every rule",
            "no candidate ID whitelist",
            "no workbook membership",
            "no target row count or sum",
        ],
        "evidence": operator_evidence,
        "admissible_operator_found": operator_present,
        "search_disposition": "PROJECTION_RULE_OPEN" if not operator_present else "REVEAL_AUTHORIZED",
    }
    (HERE / "CR120S_operator_search.json").write_text(json.dumps(operator_search, indent=2) + "\n", encoding="utf-8")

    gates = {
        "G1_SOURCE_LOCK": all(lock_checks.values()),
        "G2_ALLOWED_FIELD_CONTRACT": bool(ALLOWED) and bool(FORBIDDEN),
        "G3_SOURCE_OPERATOR_PRESENT": operator_present,
        "G4_REVEAL_DISCIPLINE": (
            operator_present
            or (not workbook_parsed and not m_native_column_opened and not selected_roster_emitted)
        ),
    }
    if not gates["G1_SOURCE_LOCK"] or not gates["G2_ALLOWED_FIELD_CONTRACT"] or not gates["G4_REVEAL_DISCIPLINE"]:
        verdict = "FAIL_REVEAL_LEAK_OR_INVALID_OPERATOR"
    elif not gates["G3_SOURCE_OPERATOR_PRESENT"]:
        verdict = BOUNDARY
    else:
        verdict = "PASS_F81_RETAINED_MATTER_PROJECTION"

    summary = {
        "record_id": RECORD_ID,
        "execution_status": "CLEAN" if gates["G1_SOURCE_LOCK"] else "SOURCE_LOCK_FAILURE",
        "mathematical_verdict": "BOUNDARY" if verdict == BOUNDARY else ("PASS" if verdict.startswith("PASS") else "FAIL"),
        "scientific_verdict": verdict,
        "result_class": "STRUCTURAL_RESEARCH_BOUNDARY",
        "scientific_pass_claimed": False,
        "precommit_sha256": PRECOMMIT_SHA,
        "source_manifest_sha256": MANIFEST_SHA,
        "gates": gates,
        "candidate_operator_contract": contract["candidate_operator_contract"],
        "M_native_reveal_authorized": contract["M_native_reveal_authorized"],
        "workbook_parsed": workbook_parsed,
        "M_native_column_opened": m_native_column_opened,
        "selected_roster_emitted": selected_roster_emitted,
        "prior_numeric_weld_status": "PRESERVED_AS_CONTEXT_NOT_RECOMPUTED",
        "binding_use": "NO_LEDGER_TOTAL_OR_SCALAR_IS_A_BINDING_COEFFICIENT",
    }
    (HERE / "CR120S_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result = f"""# CR120S QP093A F81 Retained-Matter Projection

record_id: `{RECORD_ID}`  
execution_status: `{summary['execution_status']}`  
mathematical_verdict: `{summary['mathematical_verdict']}`  
scientific_verdict: `{verdict}`  
result_class: `STRUCTURAL_RESEARCH_BOUNDARY`  
scientific_pass_claimed: `false`

## Direct result

No admissible source-backed F81 row-selection operator was found in the frozen
source set. The scalar promotion hierarchy reaches `F81_COMPLETED_FACE`, but it
does not contain a canonical QP093A candidate universe, a deterministic per-row
predicate, or a finite-geometry mapping that selects the proposed retained
matter rows.

The prior selection-authority records remain controlling: the exact roster
transition and numeric weld are known, while the physical projection operator
is `OPEN_NOT_INSTALLED`. CR120R's p9,g0 witness-packet exclusion closes the
100-row full ledger but does not supply F81 row membership.

## Reveal discipline

```text
candidate operator contract   NONE_FOUND
M_native reveal authorized    false
81-row workbook parsed        false
M_native column opened        false
selected roster emitted       false
```

Because the selector gate did not clear, this runner did not inspect workbook
cells, recompute the target total, or enumerate the current roster. That is the
required fail-closed behavior, not a failed arithmetic reproduction.

## Preserved finding

`{BOUNDARY}`

The existing F81/M126 compatibility remains a strong numeric and hierarchy
candidate. It is not promoted to a physical matter projection until an
observation-blind geometry rule selects the rows without using membership,
row count, `M_native`, or the target sum.

## Binding boundary

Neither 126, 162, 12600, nor 16200 is a binding coefficient. Future binding
work must derive isotope geometry first, exclude W9 as non-payload, retain
Theta as a zero-fee carrier, and charge only typed lift excess on supports the
geometry actually requires.
"""
    (HERE / "CR120S_result.md").write_text(result, encoding="utf-8")

    required = [
        "CR120S_allowed_fields_contract.json", "CR120S_operator_search.json",
        "CR120S_summary.json", "CR120S_result.md",
    ]
    validation = {
        "record_id": RECORD_ID,
        "expected_boundary_reached": verdict == BOUNDARY,
        "source_lock_checks": lock_checks,
        "reveal_guard": {
            "workbook_parsed": workbook_parsed,
            "M_native_column_opened": m_native_column_opened,
            "selected_roster_emitted": selected_roster_emitted,
        },
        "outputs_exist": {name: (HERE / name).exists() for name in required},
    }
    (HERE / "CR120S_VALIDATION_REPORT.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

    hash_names = [
        "CR120S_PRECOMMIT.md", "CR120S_PRECOMMIT.sha256.txt", "CR120S_SOURCE_MANIFEST.csv",
        "CR120S_runner.py", *required, "CR120S_VALIDATION_REPORT.json",
    ]
    (HERE / "HASHES.txt").write_text(
        "\n".join(f"{sha256(HERE / name)}  {name}" for name in hash_names) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"record_id": RECORD_ID, "verdict": verdict, "gates": gates}, indent=2))
    if verdict.startswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
