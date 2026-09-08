"""Bounded RH and ATOM3D extension gates for SLCV32-RZ Q1.

RH enters only through completed, file-bound services that vary by event and
within an event's admissible choices with a source-bound target mapping.  The
four inherited E1 readouts are exact global shared-reference constants, so Q1
records their typed no-gain result and installs no RH feature.

ATOM3D remains a read-only representative application extension over the
corrected R4 release.  It creates a separate untrained application-head
receipt and cannot mutate the quality base, specialize, or assign physics.
"""

from __future__ import annotations

from copy import deepcopy
import gzip
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Mapping

from .canonical import (
    CanonicalError,
    canonical_sha256,
    file_sha256,
    load_exact_json,
    require_seal,
    seal_dict,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RH_CONTRACT_PATH = PACKAGE_ROOT / "config" / "RH_RELATIVE_QUALITY_SERVICE_CONTRACT.json"
DEFAULT_ATOM3D_CONTRACT_PATH = PACKAGE_ROOT / "config" / "ATOM3D_IMMUTABLE_EXTENSION_CONTRACT.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ExtensionBoundaryError(CanonicalError):
    """An RH or ATOM3D request crossed Q1's application boundary."""


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ExtensionBoundaryError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _strict_relative(value: Any, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ExtensionBoundaryError(f"{label} must be a non-empty relative path")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise ExtensionBoundaryError(f"{label} is not a strict relative path")
    return relative


def _repository_path(repository_root: Path, relative_value: Any, label: str) -> Path:
    relative = _strict_relative(relative_value, label)
    cursor = repository_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ExtensionBoundaryError(f"{label} uses a prohibited symlink: {cursor}")
    try:
        resolved = cursor.resolve(strict=True)
        resolved.relative_to(repository_root)
    except (OSError, ValueError) as exc:
        raise ExtensionBoundaryError(f"{label} escaped custody or is unavailable") from exc
    if not resolved.is_file():
        raise ExtensionBoundaryError(f"{label} is not a file")
    return resolved


def _load_contract(path: Path, schema: str, status: str, label: str) -> dict[str, Any]:
    if path.is_symlink():
        raise ExtensionBoundaryError(f"{label} cannot be a symlink")
    value = load_exact_json(path.resolve(strict=True))
    if not isinstance(value, dict):
        raise ExtensionBoundaryError(f"{label} must be an object")
    try:
        require_seal(value, label)
    except CanonicalError as exc:
        raise ExtensionBoundaryError(str(exc)) from exc
    if value.get("schema") != schema or value.get("status") != status:
        raise ExtensionBoundaryError(f"{label} schema/status is not admitted")
    return value


def _load_bound_exact_json(
    repository_root: Path,
    binding: Mapping[str, Any],
    label: str,
    *,
    default_semantic_field: str = "semantic_sha256",
) -> tuple[Path, dict[str, Any]]:
    path = _repository_path(repository_root, binding.get("path"), label)
    if file_sha256(path) != _require_sha256(binding.get("file_sha256"), f"{label}.file_sha256"):
        raise ExtensionBoundaryError(f"{label} file identity changed")
    value = load_exact_json(path)
    if not isinstance(value, dict):
        raise ExtensionBoundaryError(f"{label} must be an exact JSON object")
    semantic_field = binding.get("semantic_field", default_semantic_field)
    try:
        require_seal(value, label, semantic_field)
    except CanonicalError as exc:
        raise ExtensionBoundaryError(str(exc)) from exc
    if value.get(semantic_field) != binding.get("semantic_sha256"):
        raise ExtensionBoundaryError(f"{label} semantic identity changed")
    if binding.get("schema") is not None and value.get("schema") != binding["schema"]:
        raise ExtensionBoundaryError(f"{label} schema changed")
    if binding.get("status") is not None and value.get("status") != binding["status"]:
        raise ExtensionBoundaryError(f"{label} status changed")
    return path, value


class RHServiceGate:
    """Verify inherited completed RH services and apply Q1's materiality gate."""

    def __init__(
        self,
        contract_path: str | Path | None = None,
        *,
        repository_root: str | Path | None = None,
    ) -> None:
        self.repository_root = Path(repository_root or REPOSITORY_ROOT).resolve(strict=True)
        self.contract_path = Path(contract_path or DEFAULT_RH_CONTRACT_PATH)
        self.contract = _load_contract(
            self.contract_path,
            "SLCV32_RZ_Q1_RH_RELATIVE_QUALITY_SERVICE_CONTRACT_V1",
            "FROZEN_TYPED_MATERIALITY_GATE",
            "Q1 RH service contract",
        )

    def evaluate(self) -> dict[str, Any]:
        _, source_contract = _load_bound_exact_json(
            self.repository_root,
            self.contract["e1_source_contract"],
            "E1 RH source contract",
        )
        _, source_result = _load_bound_exact_json(
            self.repository_root,
            self.contract["e1_source_result"],
            "E1 RH source result",
        )
        result_binding = self.contract["e1_source_result"]
        if (
            source_result.get("contract_semantic_sha256")
            != self.contract["e1_source_contract"]["semantic_sha256"]
            or source_result.get("interpretation", {}).get("outcome")
            != result_binding["outcome"]
            or source_result.get("interpretation", {}).get("quality_gain_claimed") is not False
            or source_result.get("assertions", {}).get("open_rh_boundary_admitted") is not False
        ):
            raise ExtensionBoundaryError("E1 RH source result crossed its completed/no-gain boundary")

        contract_features = source_contract.get("features")
        result_features = source_result.get("rh_feature_provenance")
        if not isinstance(contract_features, list) or not isinstance(result_features, list):
            raise ExtensionBoundaryError("E1 RH feature roster is unavailable")
        expected = self.contract["inherited_service_expectation"]
        expected_count = expected["completed_provenance_bound_service_count"]
        if len(contract_features) != expected_count or len(result_features) != expected_count:
            raise ExtensionBoundaryError("E1 RH completed-service count changed")
        contract_by_id = {row.get("service_id"): row for row in contract_features if isinstance(row, Mapping)}
        if len(contract_by_id) != expected_count:
            raise ExtensionBoundaryError("E1 RH service identities are invalid or duplicated")

        rows: list[dict[str, Any]] = []
        for result_row in result_features:
            if not isinstance(result_row, Mapping):
                raise ExtensionBoundaryError("E1 RH feature result row must be an object")
            service_id = result_row.get("service_id")
            contract_row = contract_by_id.get(service_id)
            if not isinstance(contract_row, Mapping):
                raise ExtensionBoundaryError(f"E1 RH result substituted service: {service_id}")
            if (
                result_row.get("mathematical_status") != "COMPLETED_REUSABLE"
                or contract_row.get("mathematical_status") != "COMPLETED_REUSABLE"
                or result_row.get("source_provenance") != contract_row.get("source_provenance")
            ):
                raise ExtensionBoundaryError(f"RH service is not completed/provenance-bound: {service_id}")
            provenance = result_row["source_provenance"]
            if not isinstance(provenance, Mapping):
                raise ExtensionBoundaryError(f"RH service provenance is unavailable: {service_id}")
            history_path = _repository_path(
                self.repository_root, provenance.get("history_path"), f"{service_id} history"
            )
            artifact_path = _repository_path(
                self.repository_root, provenance.get("artifact_path"), f"{service_id} artifact"
            )
            if file_sha256(history_path) != provenance.get("history_file_sha256"):
                raise ExtensionBoundaryError(f"RH service history identity changed: {service_id}")
            if file_sha256(artifact_path) != provenance.get("artifact_file_sha256"):
                raise ExtensionBoundaryError(f"RH service artifact identity changed: {service_id}")
            installed = contract_row.get("installed_feature")
            if not isinstance(installed, Mapping):
                raise ExtensionBoundaryError(f"RH installed-feature description missing: {service_id}")
            if (
                installed.get("global_shared_reference") is not True
                or installed.get("query_dependent") is not False
                or installed.get("candidate_dependent") is not False
                or installed.get("gradient_status") != "ZERO_PAIRWISE_DIFFERENCE"
                or result_row.get("value_ppm") != installed.get("value_ppm")
            ):
                raise ExtensionBoundaryError(f"inherited RH constant semantics changed: {service_id}")
            rows.append(
                seal_dict(
                    {
                        "schema": "SLCV32_RZ_Q1_RH_SERVICE_ASSESSMENT_V1",
                        "service_id": service_id,
                        "mathematical_status": "COMPLETED_REUSABLE",
                        "provenance_bound": True,
                        "history_id": provenance["history_id"],
                        "event_varying": False,
                        "within_event_choice_varying": False,
                        "source_bound_relative_target_mapping": False,
                        "admitted_to_q1_relative_quality_target": False,
                        "outcome": "TYPED_NO_GAIN",
                        "reason": "GLOBAL_SHARED_REFERENCE_CONSTANT_HAS_ZERO_WITHIN_QUERY_PAIRWISE_DIFFERENCE",
                    }
                )
            )

        if len(rows) != expected_count:
            raise ExtensionBoundaryError("RH service assessment roster changed")
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_RH_SERVICE_MATERIALITY_RESULT_V1",
                "status": "PASS_TYPED_NO_GAIN",
                "candidate": self.contract["candidate"],
                "completed_provenance_bound_services_verified": len(rows),
                "event_varying_services_verified": 0,
                "relative_target_material_services_admitted": 0,
                "services": rows,
                "outcome": expected["typed_outcome"],
                "quality_gain_claimed": False,
                "rh_feature_columns_installed": 0,
                "open_rh_boundary_admitted": False,
                "preserved_rh_status": self.contract["preserved_rh_status"],
                "future_admission_rule": {
                    "completed_provenance_bound": True,
                    "event_varying": True,
                    "within_event_choice_varying": True,
                    "source_bound_relative_target_mapping": True,
                    "complete_catalog_identical_budget_positive_heldout_delta": True,
                },
                "e1_rh_source_contract_semantic_sha256": source_contract["semantic_sha256"],
                "e1_rh_source_result_semantic_sha256": source_result["semantic_sha256"],
            }
        )


class Atom3DExtensionGate:
    """Verify corrected R4 custody and emit one separate untrained Q1 head."""

    def __init__(
        self,
        contract_path: str | Path | None = None,
        *,
        repository_root: str | Path | None = None,
    ) -> None:
        self.repository_root = Path(repository_root or REPOSITORY_ROOT).resolve(strict=True)
        self.contract_path = Path(contract_path or DEFAULT_ATOM3D_CONTRACT_PATH)
        self.contract = _load_contract(
            self.contract_path,
            "SLCV32_RZ_Q1_ATOM3D_IMMUTABLE_EXTENSION_CONTRACT_V1",
            "FROZEN_REPRESENTATIVE_IMMUTABLE_BASE_BOUNDARY",
            "Q1 ATOM3D extension contract",
        )
        self._representative: dict[str, Any] | None = None

    def _verify_r4_release(self) -> tuple[dict[str, Any], dict[str, Any]]:
        release = self.contract["r4_release"]
        manifest_path = _repository_path(
            self.repository_root, release.get("manifest_path"), "R4 release manifest"
        )
        if file_sha256(manifest_path) != release.get("manifest_file_sha256"):
            raise ExtensionBoundaryError("R4 release manifest file identity changed")
        manifest = load_exact_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ExtensionBoundaryError("R4 release manifest must be an exact JSON object")
        semantic_field = release["manifest_semantic_field"]
        try:
            require_seal(manifest, "R4 release manifest", semantic_field)
        except CanonicalError as exc:
            raise ExtensionBoundaryError(str(exc)) from exc
        if (
            manifest.get(semantic_field) != release["manifest_semantic_sha256"]
            or manifest.get("schema") != release["manifest_schema"]
            or manifest.get("status") != release["manifest_status"]
        ):
            raise ExtensionBoundaryError("R4 release manifest semantics changed")
        artifact_map = manifest.get("artifacts")
        if not isinstance(artifact_map, Mapping) or len(artifact_map) != release["required_artifact_count"]:
            raise ExtensionBoundaryError("R4 release manifest artifact count changed")
        release_root = manifest_path.parent
        seen: set[str] = set()
        for index, (raw_relative, row) in enumerate(sorted(artifact_map.items())):
            if not isinstance(row, Mapping):
                raise ExtensionBoundaryError(f"R4 artifact row {index} is not an object")
            relative = _strict_relative(raw_relative, f"R4 artifact {index}.path").as_posix()
            if relative in seen:
                raise ExtensionBoundaryError(f"R4 artifact path is duplicated: {relative}")
            seen.add(relative)
            path = release_root / relative
            if path.is_symlink():
                raise ExtensionBoundaryError(f"R4 artifact cannot be a symlink: {relative}")
            try:
                path = path.resolve(strict=True)
                path.relative_to(release_root)
            except (OSError, ValueError) as exc:
                raise ExtensionBoundaryError(f"R4 artifact escaped custody: {relative}") from exc
            if (
                path.stat().st_size != row.get("bytes")
                or file_sha256(path) != row.get("sha256")
            ):
                raise ExtensionBoundaryError(f"R4 artifact identity changed: {relative}")

        ledger_path = _repository_path(
            self.repository_root,
            release.get("representative_ledger_path"),
            "R4 representative receipt ledger",
        )
        if file_sha256(ledger_path) != release.get("representative_ledger_sha256"):
            raise ExtensionBoundaryError("R4 representative receipt ledger identity changed")
        expected = self.contract["representative_receipt"]
        selected: dict[str, Any] | None = None
        try:
            with gzip.open(ledger_path, "rt", encoding="utf-8") as handle:
                for line in handle:
                    value = json.loads(line)
                    if value.get("receipt_id") == expected["receipt_id"]:
                        selected = value
                        break
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ExtensionBoundaryError("R4 representative receipt ledger is unreadable") from exc
        if selected is None:
            raise ExtensionBoundaryError("R4 representative receipt is unavailable")
        claimed = selected.get("receipt_semantic_sha256")
        unsigned = dict(selected)
        unsigned.pop("receipt_semantic_sha256", None)
        if (
            claimed != expected["receipt_semantic_sha256"]
            or canonical_sha256(unsigned) != claimed
            or selected.get("family_id") != expected["family_id"]
            or selected.get("pair_id") != expected["pair_id"]
            or selected.get("source_word") != expected["source_word"]
            or selected.get("inverse", {}).get("return_word") != expected["return_word"]
            or selected.get("arithmetic_custody", {}).get("cross_term_account")
            != expected["informational_cross_term"]
        ):
            raise ExtensionBoundaryError("R4 representative receipt semantics changed")
        self._representative = selected
        return manifest, selected

    def verify_provenance(self) -> dict[str, Any]:
        _, e1_contract = _load_bound_exact_json(
            self.repository_root,
            self.contract["e1_source_contract"],
            "E1 ATOM3D source contract",
        )
        _, e1_result = _load_bound_exact_json(
            self.repository_root,
            self.contract["e1_representative_result"],
            "E1 ATOM3D representative result",
            default_semantic_field="fixture_execution_semantic_sha256",
        )
        boundary = self.contract["boundary"]
        e1_boundary = e1_contract.get("boundary")
        if not isinstance(e1_boundary, Mapping):
            raise ExtensionBoundaryError("E1 ATOM3D boundary is unavailable")
        if (
            e1_boundary.get("immutable_base") is not True
            or e1_boundary.get("specialized_training_executed") is not False
            or e1_boundary.get("physical_geometry_installed") is not False
            or e1_result.get("immutable_a1_base_verified") is not True
            or e1_result.get("readout", {}).get("specialization_trained") is not False
            or e1_result.get("readout", {}).get("base_model_promoted") is not False
        ):
            raise ExtensionBoundaryError("E1 ATOM3D immutable-base boundary changed")
        if (
            boundary.get("immutable_quality_base") is not True
            or boundary.get("application_head_checkpoint_separate") is not True
            or boundary.get("specialized_training_executed") is not False
            or boundary.get("physical_calibration_executed") is not False
            or boundary.get("physical_specialization_executed") is not False
        ):
            raise ExtensionBoundaryError("Q1 ATOM3D boundary is not immutable/untrained")
        manifest, representative = self._verify_r4_release()
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_ATOM3D_PROVENANCE_VERIFICATION_V1",
                "status": "PASS",
                "history_entry": e1_contract["authority"]["history_entry"],
                "classification_preserved": e1_contract["authority"]["classification"],
                "r4_release_manifest_semantic_sha256": manifest[
                    self.contract["r4_release"]["manifest_semantic_field"]
                ],
                "r4_release_artifacts_verified": len(manifest["artifacts"]),
                "representative_receipt_id": representative["receipt_id"],
                "representative_receipt_semantic_sha256": representative[
                    "receipt_semantic_sha256"
                ],
                "e1_representative_result_semantic_sha256": e1_result[
                    "fixture_execution_semantic_sha256"
                ],
                "immutable_e1_atom3d_base_verified": True,
                "physical_calibration_executed": False,
                "specialized_training_executed": False,
            }
        )

    def execute(
        self,
        base_model: Any,
        *,
        specialization_requested: bool = False,
        physical_calibration_requested: bool = False,
    ) -> dict[str, Any]:
        """Emit a deterministic representative application head without training."""

        if not isinstance(specialization_requested, bool) or not isinstance(
            physical_calibration_requested, bool
        ):
            raise ExtensionBoundaryError("extension request flags must be boolean")
        if specialization_requested:
            raise ExtensionBoundaryError("ATOM3D specialization is outside Q1")
        if physical_calibration_requested:
            raise ExtensionBoundaryError("ATOM3D physical calibration is outside Q1")
        base_before = canonical_sha256(base_model)
        provenance = self.verify_provenance()
        if self._representative is None:
            raise ExtensionBoundaryError("representative receipt was not installed")
        representative = self._representative
        expected = self.contract["representative_receipt"]
        head_identity = canonical_sha256(
            {
                "extension_id": self.contract["extension_id"],
                "base_model_semantic_sha256": base_before,
                "representative_receipt_semantic_sha256": expected[
                    "receipt_semantic_sha256"
                ],
                "parameters": [],
                "training_status": "UNTRAINED_REPRESENTATIVE_BOUNDARY",
            }
        )
        base_after = canonical_sha256(base_model)
        if base_after != base_before:
            raise ExtensionBoundaryError("ATOM3D extension mutated the quality base")
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_ATOM3D_REPRESENTATIVE_EXTENSION_RESULT_V1",
                "status": "PASS_IMMUTABLE_BASE_APPLICATION_EXTENSION",
                "candidate": self.contract["candidate"],
                "extension_id": self.contract["extension_id"],
                "provenance_semantic_sha256": provenance["semantic_sha256"],
                "base_model_semantic_sha256_before": base_before,
                "base_model_semantic_sha256_after": base_after,
                "base_model_unchanged": True,
                "base_model_promoted": False,
                "application_head_checkpoint_separate": True,
                "application_head_checkpoint_semantic_sha256": head_identity,
                "application_head_parameters": [],
                "application_head_training_status": "UNTRAINED_REPRESENTATIVE_BOUNDARY",
                "representative": {
                    "family_id": representative["family_id"],
                    "pair_id": representative["pair_id"],
                    "receipt_id": representative["receipt_id"],
                    "receipt_semantic_sha256": representative["receipt_semantic_sha256"],
                    "source_word": deepcopy(representative["source_word"]),
                    "return_word": deepcopy(representative["inverse"]["return_word"]),
                    "principal_face": deepcopy(expected["principal_face"]),
                    "informational_cross_term": representative["arithmetic_custody"][
                        "cross_term_account"
                    ],
                    "exact_reversal_admitted": True,
                },
                "classification_preserved": provenance["classification_preserved"],
                "informational_cross_term_is_physical_energy": False,
                "physical_fields": {
                    "physical_scale": "OPEN_UNASSIGNED",
                    "physical_branch": "OPEN_UNASSIGNED",
                    "binding": "OPEN_UNASSIGNED",
                    "energy": "OPEN_UNASSIGNED",
                },
                "specialization_trained": False,
                "physical_calibration_executed": False,
                "physical_specialization_executed": False,
                "afc_transport_installed": False,
            }
        )


def evaluate_rh_services() -> dict[str, Any]:
    return RHServiceGate().evaluate()


def run_atom3d_extension(base_model: Any) -> dict[str, Any]:
    return Atom3DExtensionGate().execute(base_model)


__all__ = [
    "Atom3DExtensionGate",
    "DEFAULT_ATOM3D_CONTRACT_PATH",
    "DEFAULT_RH_CONTRACT_PATH",
    "ExtensionBoundaryError",
    "RHServiceGate",
    "evaluate_rh_services",
    "run_atom3d_extension",
]
