"""Exact native-signature registry and reconciliation for QP productions."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .errors import ContractValidationError, QPRegistrationError


NATIVE_FILE = "QP_TEMPLATE_NATIVE_SIGNATURES.csv"
RECONCILIATION_FILE = "QP_SOURCE_RECONCILIATION.csv"
MANIFEST_FILE = "QP_SOURCE_MANIFEST.json"


def default_data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_packaged_sources(data_dir: str | Path | None = None) -> dict[str, Any]:
    root = Path(data_dir) if data_dir is not None else default_data_dir()
    manifest_path = root / MANIFEST_FILE
    if not manifest_path.is_file():
        raise ContractValidationError(f"Missing packaged QP source manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractValidationError(f"Unreadable packaged QP source manifest: {exc}") from exc
    failures: list[dict[str, str]] = []
    checked: list[dict[str, str]] = []
    for declared_path, expected in sorted(manifest.get("packaged_registry_hashes", {}).items()):
        path = root / Path(declared_path).name
        if not path.is_file():
            failures.append({"path": path.name, "reason": "MISSING", "expected": expected})
            continue
        observed = _sha256(path)
        checked.append({"path": path.name, "expected": expected, "observed": observed})
        if observed != expected:
            failures.append(
                {"path": path.name, "reason": "HASH_MISMATCH", "expected": expected, "observed": observed}
            )
    if failures:
        raise ContractValidationError(
            "Packaged QP registry validation failed: " + json.dumps(failures, sort_keys=True)
        )
    return {
        "status": "PASS",
        "manifest": MANIFEST_FILE,
        "checked_files": len(checked),
        "canonical_rows": manifest.get("canonical_join", {}).get("rows"),
        "candidate_id_semantic_selector": False,
    }


def load_native_index(
    data_dir: str | Path | None = None,
    *,
    validate: bool = True,
) -> dict[str, dict[str, str]]:
    root = Path(data_dir) if data_dir is not None else default_data_dir()
    if validate:
        validate_packaged_sources(root)
    path = root / NATIVE_FILE
    if not path.is_file():
        raise ContractValidationError(f"Missing packaged native-signature registry: {path}")
    rows = _read_csv(path)
    index = {row["canonical_signature"]: row for row in rows}
    if len(rows) != 321 or len(index) != 321:
        raise ContractValidationError(
            f"Native-signature registry must contain 321 unique canonical signatures; "
            f"found rows={len(rows)}, unique={len(index)}"
        )
    return index


def load_source_reconciliation(
    data_dir: str | Path | None = None,
    *,
    validate: bool = True,
) -> list[dict[str, str]]:
    root = Path(data_dir) if data_dir is not None else default_data_dir()
    if validate:
        validate_packaged_sources(root)
    rows = _read_csv(root / RECONCILIATION_FILE)
    if len(rows) != 321 or len({row["canonical_signature"] for row in rows}) != 321:
        raise ContractValidationError("QP source reconciliation is not a 321-row canonical bijection")
    return rows


def native_packet(signature: str, data_dir: str | Path | None = None) -> dict[str, Any]:
    index = load_native_index(data_dir)
    row = index.get(signature)
    if row is None:
        raise QPRegistrationError(f"No native signature registered for {signature}")
    packet = {
        "canonical_signature": row["canonical_signature"],
        "source_row_id": row["source_row_id"],
        "assembly_template_id": row["assembly_template_id"],
        "opaque_token_id": row["opaque_token_id"],
        "disposition": row["disposition"],
        "template_class": row["template_class"],
        "structural_bucket": row["structural_bucket"],
        "arity": row["arity"],
        "partition_signature": row["partition_signature"],
        "component_labels": row["component_labels"],
        "closure_depth": row["closure_depth"],
        "q_sign": row["q_sign"],
        "q_abs": row["q_abs"],
        "surface_sign": row["surface_sign"],
        "numeric_lane": row["numeric_lane"],
        "dependency_class": row["dependency_class"],
        "M_native_exact": row["M_native_fraction"],
        "S_debit_or_credit_exact": row["S_debit_or_credit_fraction"],
        "M_observed_candidate_exact": row["M_observed_candidate_fraction"],
        "qA_source_support_exact": row["qA_source_support_fraction"],
        "tensor_carrier_support_exact": row["tensor_carrier_support_fraction"],
        "retained_write_support_exact": row["retained_write_support_fraction"],
        "lift_excess_exact": row["lift_excess_fraction"],
        "raw_numeric_class_id": row["raw_numeric_class_id"],
        "typed_raw_class_id": row["typed_raw_class_id"],
        "dependency_class_id": row["dependency_class_id"],
        "dependency_core_class_id": row["dependency_core_class_id"],
        "dependency_residual_subclass_id": row["dependency_residual_subclass_id"],
        "scale_free_class_id": row["scale_free_class_id"],
        "membership_effect": row["membership_effect"],
        "particle_identity_assignment": row["particle_identity_assignment"],
        "physical_mass": "OPEN_UNREGISTERED",
        "binding_energy": "OPEN_UNREGISTERED",
    }
    packet["source_renderings"] = {
        key: row[key]
        for key in row
        if key.endswith("_source") or key.endswith("_fractional_digits")
    }
    return packet


READOUT_FIELDS = {
    "QP_NATIVE_ACCOUNT": ("M_native_exact", "QPExactAccount"),
    "QP_SURFACE_DEBIT_OR_CREDIT": ("S_debit_or_credit_exact", "QPSurfaceDebitOrCredit"),
    "QP_OBSERVED_CANDIDATE_ACCOUNT": ("M_observed_candidate_exact", "QPObservedCandidateAccount"),
    "QP_SOURCE_SUPPORT": ("qA_source_support_exact", "QPSourceSupport"),
    "QP_TENSOR_SUPPORT": ("tensor_carrier_support_exact", "QPTensorCarrierSupport"),
    "QP_RETAINED_SUPPORT": ("retained_write_support_exact", "QPRetainedWriteSupport"),
}


def exact_readout(packet: dict[str, Any], operator: str) -> tuple[str, Fraction, str]:
    field, semantic_type = READOUT_FIELDS[operator]
    source = packet[field]
    return field, Fraction(source), semantic_type


def verify_source_reconciliation(data_dir: str | Path | None = None) -> dict[str, Any]:
    rows = load_source_reconciliation(data_dir)
    failures = [
        row
        for row in rows
        if not all(
            row[key].lower() == "true"
            for key in ("formula_pass", "signature_match", "role_match", "lineage_match", "structural_match", "native_match")
        )
    ]
    return {
        "status": "PASS" if not failures else "FAIL",
        "rows": len(rows),
        "unique_signatures": len({row["canonical_signature"] for row in rows}),
        "failures": len(failures),
        "candidate_id_semantic_selector": False,
    }


def verify_native_reconciliation(data_dir: str | Path | None = None) -> dict[str, Any]:
    index = load_native_index(data_dir)
    required = {
        "M_native_fraction",
        "S_debit_or_credit_fraction",
        "M_observed_candidate_fraction",
        "qA_source_support_fraction",
        "tensor_carrier_support_fraction",
        "retained_write_support_fraction",
        "lift_excess_fraction",
    }
    missing = {
        signature: sorted(required - set(row))
        for signature, row in index.items()
        if required - set(row)
    }
    return {
        "status": "PASS" if not missing else "FAIL",
        "rows": len(index),
        "unique_signatures": len(index),
        "missing_fields": missing,
        "lookup_key": "canonical_signature",
    }


def _unit(digits: str) -> Fraction:
    count = int(digits or 0)
    return Fraction(1, 10**count)


def verify_native_inverse(data_dir: str | Path | None = None) -> dict[str, Any]:
    rows = list(load_native_index(data_dir).values())
    applicable = exact_both = bounded_both = zero_support = exceptions = 0
    records: list[dict[str, Any]] = []
    for row in rows:
        tensor = Fraction(row["tensor_carrier_support_fraction"])
        if tensor == 0:
            zero_support += 1
            records.append(
                {
                    "canonical_signature": row["canonical_signature"],
                    "status": "NONINVERTIBLE_ZERO_SUPPORT",
                }
            )
            continue
        applicable += 1
        q_abs = Fraction(row["q_abs"])
        observed = Fraction(row["M_observed_candidate_fraction"])
        native = Fraction(row["M_native_fraction"])
        surface = Fraction(row["S_debit_or_credit_fraction"])
        observed_hat = Fraction(1152) * tensor / (Fraction(144) + q_abs)
        native_hat = surface + observed_hat
        observed_cross = abs((144 + q_abs) * observed - 1152 * tensor)
        native_cross = abs((144 + q_abs) * (native - surface) - 1152 * tensor)
        u_t = _unit(row["tensor_carrier_support_fractional_digits"])
        u_o = _unit(row["M_observed_candidate_fractional_digits"])
        u_n = _unit(row["M_native_fractional_digits"])
        u_s = _unit(row["S_debit_or_credit_fractional_digits"])
        observed_bound = 3 * ((144 + q_abs) * u_o + 1152 * u_t)
        native_bound = 3 * ((144 + q_abs) * (u_n + u_s + u_o) + 1152 * u_t)
        exact = observed_hat == observed and native_hat == native
        bounded = observed_cross <= observed_bound and native_cross <= native_bound
        exact_both += int(exact)
        bounded_both += int(bounded)
        exceptions += int(not bounded)
        records.append(
            {
                "canonical_signature": row["canonical_signature"],
                "observed_reconstructed_exact": str(observed_hat),
                "native_reconstructed_exact": str(native_hat),
                "observed_exact": observed_hat == observed,
                "native_exact": native_hat == native,
                "source_precision_bounded": bounded,
                "status": (
                    "EXACT_RECONSTRUCTION"
                    if exact
                    else "SOURCE_PRECISION_BOUNDED_RECONSTRUCTION"
                    if bounded
                    else "INVERSE_EXCEPTION"
                ),
            }
        )
    return {
        "verdict": "PASS_QP_TENSOR_NATIVE_INVERSE" if exceptions == 0 else "BOUNDARY_QP_NATIVE_INVERSE_EXCEPTIONS_REMAIN",
        "status": "PASS" if exceptions == 0 else "BOUNDARY",
        "source_rows": len(rows),
        "applicable_nonzero_support_rows": applicable,
        "noninvertible_zero_support_rows": zero_support,
        "exact_both_rows": exact_both,
        "source_precision_bounded_both_rows": bounded_both,
        "exceptions": exceptions,
        "formula": {
            "M_observed": "1152*T/(144+q_abs)",
            "M_native": "S_debit_or_credit+M_observed",
        },
        "physical_mass_operator_registered": False,
        "records": records,
    }
