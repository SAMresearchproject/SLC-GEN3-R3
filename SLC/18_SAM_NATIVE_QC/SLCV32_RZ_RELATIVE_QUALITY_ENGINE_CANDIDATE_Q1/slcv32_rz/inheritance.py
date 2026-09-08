"""Read-only Q1 custody for frozen SLCV31-RZ E1 and SLCV30-RZ A1.

The verifier admits predecessor reconstruction only after checking every file
listed by each predecessor release manifest, the excluded post-manifest tail,
the tail's bidirectional file/semantic crosslinks, and the unchanged SLCV21R
pointer.  It imports no predecessor Python and performs no predecessor write.
"""

from __future__ import annotations

from copy import deepcopy
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
DEFAULT_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONTRACT_PATH = PACKAGE_ROOT / "config" / "SLCV32_Q1_E1_INHERITANCE_CONTRACT.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class InheritanceError(CanonicalError):
    """Frozen predecessor custody or reconstruction admission failed."""


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise InheritanceError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _strict_relative(value: Any, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise InheritanceError(f"{label} must be a non-empty relative path")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise InheritanceError(f"{label} is not a strict relative path: {value}")
    return relative


def _resolve_root(path: Path, label: str) -> Path:
    if path.is_symlink():
        raise InheritanceError(f"{label} cannot be a symlink: {path}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise InheritanceError(f"{label} is unavailable: {path}") from exc
    if not resolved.is_dir():
        raise InheritanceError(f"{label} is not a directory: {resolved}")
    return resolved


def _resolve_beneath(base: Path, relative_value: Any, label: str, *, directory: bool = False) -> Path:
    relative = _strict_relative(relative_value, label)
    cursor = base
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise InheritanceError(f"{label} uses prohibited symlink component: {cursor}")
    try:
        resolved = cursor.resolve(strict=True)
        resolved.relative_to(base)
    except (OSError, ValueError) as exc:
        raise InheritanceError(f"{label} escapes custody or is unavailable: {cursor}") from exc
    if directory and not resolved.is_dir():
        raise InheritanceError(f"{label} is not a directory: {resolved}")
    if not directory and not resolved.is_file():
        raise InheritanceError(f"{label} is not a file: {resolved}")
    return resolved


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = load_exact_json(path)
    except CanonicalError as exc:
        raise InheritanceError(f"{label} is not exact JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise InheritanceError(f"{label} must be a JSON object")
    return value


def _verify_semantic(value: Mapping[str, Any], field: Any, expected: Any, label: str) -> str:
    if not isinstance(field, str) or not field:
        raise InheritanceError(f"{label}.semantic_field must be a non-empty string")
    expected_hash = _require_sha256(expected, f"{label}.{field}.expected")
    if value.get(field) != expected_hash:
        raise InheritanceError(f"{label} embedded {field} differs from custody")
    unsigned = dict(value)
    unsigned.pop(field, None)
    observed = canonical_sha256(unsigned)
    if observed != expected_hash:
        raise InheritanceError(f"{label} semantic identity differs from custody")
    return observed


def _manifest_candidates(root: Path, exclusions: set[str]) -> set[str]:
    paths: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise InheritanceError(f"frozen predecessor contains a symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if relative not in exclusions:
            paths.add(relative)
    return paths


class E1InheritanceVerifier:
    """Verify the full E1 -> A1 frozen chain without importing either package."""

    def __init__(
        self,
        *,
        repository_root: str | Path | None = None,
        contract_path: str | Path | None = None,
    ) -> None:
        self.repository_root = _resolve_root(
            Path(repository_root) if repository_root is not None else DEFAULT_REPOSITORY_ROOT,
            "repository_root",
        )
        contract_input = Path(contract_path) if contract_path is not None else DEFAULT_CONTRACT_PATH
        if contract_input.is_symlink():
            raise InheritanceError("Q1 inheritance contract cannot be a symlink")
        try:
            self.contract_path = contract_input.resolve(strict=True)
        except OSError as exc:
            raise InheritanceError("Q1 inheritance contract is unavailable") from exc
        self.contract = _load_object(self.contract_path, "Q1 inheritance contract")
        try:
            require_seal(self.contract, "Q1 inheritance contract")
        except CanonicalError as exc:
            raise InheritanceError(str(exc)) from exc
        if self.contract.get("schema") != "SLCV32_RZ_Q1_E1_INHERITANCE_CONTRACT_V1":
            raise InheritanceError("Q1 inheritance contract schema is not admitted")
        if self.contract.get("status") != "FROZEN_SOURCE_BOUND_NON_PROMOTED_PREDECESSOR_DELEGATION":
            raise InheritanceError("Q1 inheritance contract status is not frozen/non-promoted")
        self.e1_root = _resolve_beneath(
            self.repository_root,
            self.contract.get("predecessor_repository_relative_root"),
            "E1 predecessor root",
            directory=True,
        )
        self._last_verification: dict[str, Any] | None = None

    def _repository_path(self, relative: Any, label: str) -> Path:
        return _resolve_beneath(self.repository_root, relative, label)

    @staticmethod
    def _predecessor_path(root: Path, relative: Any, label: str) -> Path:
        return _resolve_beneath(root, relative, label)

    def _verify_bound_json(
        self, root: Path, binding: Mapping[str, Any], label: str
    ) -> tuple[Path, dict[str, Any]]:
        path = self._predecessor_path(root, binding.get("path"), label)
        expected_file = _require_sha256(
            binding.get("file_sha256", binding.get("sha256")), f"{label}.file_sha256"
        )
        if file_sha256(path) != expected_file:
            raise InheritanceError(f"{label} file identity differs from custody")
        value = _load_object(path, label)
        field = binding.get("semantic_field")
        if field is not None:
            _verify_semantic(value, field, binding.get("semantic_sha256"), label)
        expected_schema = binding.get("schema")
        if expected_schema is not None and value.get("schema") != expected_schema:
            raise InheritanceError(f"{label} schema differs from custody")
        expected_status = binding.get("status")
        if expected_status is not None and value.get("status") != expected_status:
            raise InheritanceError(f"{label} status differs from custody")
        return path, value

    def _verify_complete_manifest(
        self,
        *,
        root: Path,
        manifest: Mapping[str, Any],
        expected_count: int,
        expected_exclusions: list[str],
        label: str,
    ) -> dict[str, Mapping[str, Any]]:
        if isinstance(expected_count, bool) or not isinstance(expected_count, int) or expected_count < 1:
            raise InheritanceError(f"{label} expected count is invalid")
        rows = manifest.get("artifacts")
        if not isinstance(rows, list) or len(rows) != expected_count:
            raise InheritanceError(f"{label} artifact roster length changed")
        if manifest.get("artifact_count") != expected_count:
            raise InheritanceError(f"{label} artifact_count changed")
        if manifest.get("manifest_exclusions") != expected_exclusions:
            raise InheritanceError(f"{label} manifest exclusion roster changed")
        exclusions = set(expected_exclusions)
        required_tail = {
            "release/FINAL_FREEZE_RECEIPT.json",
            "release/INDEPENDENT_VALIDATION.json",
            "release/RELEASE_MANIFEST.json",
        }
        if exclusions != required_tail:
            raise InheritanceError(f"{label} must use the exact three-file tail exclusion")

        by_path: dict[str, Mapping[str, Any]] = {}
        ordered: list[str] = []
        for index, row in enumerate(rows):
            if not isinstance(row, Mapping):
                raise InheritanceError(f"{label} artifact row {index} is not an object")
            relative = _strict_relative(row.get("path"), f"{label}.artifacts[{index}].path").as_posix()
            if relative in by_path or relative in exclusions:
                raise InheritanceError(f"{label} artifact path duplicated or excluded: {relative}")
            expected_hash = _require_sha256(row.get("sha256"), f"{label}.{relative}.sha256")
            expected_bytes = row.get("bytes")
            if isinstance(expected_bytes, bool) or not isinstance(expected_bytes, int) or expected_bytes < 0:
                raise InheritanceError(f"{label} byte count is invalid: {relative}")
            path = self._predecessor_path(root, relative, f"{label} artifact {relative}")
            if path.stat().st_size != expected_bytes:
                raise InheritanceError(f"{label} byte count changed: {relative}")
            if file_sha256(path) != expected_hash:
                raise InheritanceError(f"{label} file identity changed: {relative}")
            by_path[relative] = row
            ordered.append(relative)
        if ordered != sorted(ordered):
            raise InheritanceError(f"{label} artifact roster is not canonical path order")
        actual = _manifest_candidates(root, exclusions)
        declared = set(by_path)
        if actual != declared:
            raise InheritanceError(
                f"{label} complete roster differs; undeclared={sorted(actual - declared)}, "
                f"unavailable={sorted(declared - actual)}"
            )
        return by_path

    def _verify_e1(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], int]:
        manifest_binding = self.contract["required_release_manifest"]
        manifest_path, manifest = self._verify_bound_json(
            self.e1_root, manifest_binding, "E1 release manifest"
        )
        if manifest.get("candidate") != self.contract.get("predecessor"):
            raise InheritanceError("E1 manifest candidate identity changed")
        if manifest.get("boundaries") != self.contract.get("required_release_boundaries"):
            raise InheritanceError("E1 frozen/non-promotion boundary map changed")
        rows = self._verify_complete_manifest(
            root=self.e1_root,
            manifest=manifest,
            expected_count=manifest_binding["artifact_count"],
            expected_exclusions=manifest_binding["manifest_exclusions"],
            label="E1 release manifest",
        )

        tail: dict[str, tuple[Path, dict[str, Any], Mapping[str, Any]]] = {}
        for binding in self.contract["tail_artifacts"]:
            role = binding.get("role")
            if not isinstance(role, str) or role in tail:
                raise InheritanceError("E1 tail role is invalid or duplicated")
            path, value = self._verify_bound_json(self.e1_root, binding, role)
            tail[role] = (path, value, binding)
        if set(tail) != {"E1_INDEPENDENT_VALIDATION", "E1_FINAL_FREEZE_RECEIPT"}:
            raise InheritanceError("E1 tail role roster changed")
        independent_path, independent, independent_binding = tail["E1_INDEPENDENT_VALIDATION"]
        freeze_path, freeze, freeze_binding = tail["E1_FINAL_FREEZE_RECEIPT"]

        if (
            independent.get("candidate") != self.contract["predecessor"]
            or independent.get("failed") != 0
            or independent.get("release_artifacts_hash_verified") != manifest_binding["artifact_count"]
            or independent.get("release_manifest_semantic_sha256")
            != manifest_binding["semantic_sha256"]
            or independent.get("current_pointer_changed") is not False
            or independent.get("current_slc_revision") != "SLCV21R"
            or independent.get("promoted") is not False
        ):
            raise InheritanceError("E1 independent validation no longer admits frozen inheritance")
        if (
            freeze.get("candidate") != self.contract["predecessor"]
            or freeze.get("artifact_count") != manifest_binding["artifact_count"]
            or freeze.get("all_persistent_workers_stopped") is not True
            or freeze.get("execution_processes_active") is not False
            or freeze.get("promoted") is not False
            or freeze.get("current_slc_revision") != "SLCV21R"
            or freeze.get("release_manifest_file_sha256") != manifest_binding["file_sha256"]
            or freeze.get("release_manifest_semantic_sha256") != manifest_binding["semantic_sha256"]
            or freeze.get("independent_validation_file_sha256")
            != independent_binding["file_sha256"]
            or freeze.get("independent_validation_semantic_sha256")
            != independent_binding["semantic_sha256"]
        ):
            raise InheritanceError("E1 final freeze tail crosslinks changed")
        if file_sha256(manifest_path) != freeze["release_manifest_file_sha256"]:
            raise InheritanceError("E1 manifest changed after final-freeze crosslink")
        if file_sha256(independent_path) != freeze["independent_validation_file_sha256"]:
            raise InheritanceError("E1 independent validation changed after final-freeze crosslink")
        if file_sha256(freeze_path) != freeze_binding["file_sha256"]:
            raise InheritanceError("E1 final freeze receipt changed during verification")

        a1_binding = self.contract["a1_inheritance_contract"]
        _, a1_contract = self._verify_bound_json(
            self.e1_root, a1_binding, "E1-to-A1 inheritance contract"
        )
        a1_relative = _strict_relative(a1_binding["path"], "E1-to-A1 contract path").as_posix()
        manifest_row = rows.get(a1_relative)
        if manifest_row is None or manifest_row.get("sha256") != a1_binding["file_sha256"]:
            raise InheritanceError("E1-to-A1 contract is not cross-pinned by the complete E1 manifest")
        return manifest, independent, a1_contract, len(rows)

    def _verify_a1(self, a1_contract: Mapping[str, Any]) -> tuple[dict[str, Any], int]:
        if a1_contract.get("schema") != "SLCV31_RZ_E1_A1_INHERITANCE_CONTRACT_V1":
            raise InheritanceError("E1-to-A1 contract schema changed")
        a1_root = _resolve_beneath(
            self.repository_root,
            a1_contract.get("predecessor_repository_relative_root"),
            "A1 predecessor root",
            directory=True,
        )
        roots: dict[str, tuple[Path, dict[str, Any], Mapping[str, Any]]] = {}
        for binding in a1_contract.get("root_artifacts", []):
            role = binding.get("role")
            if not isinstance(role, str) or role in roots:
                raise InheritanceError("A1 root-artifact role is invalid or duplicated")
            path, value = self._verify_bound_json(a1_root, binding, role)
            roots[role] = (path, value, binding)
        required_roles = {
            "A1_RELEASE_MANIFEST",
            "A1_INDEPENDENT_VALIDATION",
            "A1_FINAL_FREEZE_RECEIPT",
            "A1_ARCHITECTURE_RESULT",
            "A1_DEPENDENCY_SOURCE_MANIFEST",
        }
        if set(roots) != required_roles:
            raise InheritanceError("A1 root-artifact role roster changed")
        manifest_path, manifest, manifest_binding = roots["A1_RELEASE_MANIFEST"]
        independent_path, independent, independent_binding = roots["A1_INDEPENDENT_VALIDATION"]
        _, freeze, _ = roots["A1_FINAL_FREEZE_RECEIPT"]
        if (
            manifest.get("candidate") != a1_contract.get("predecessor")
            or manifest.get("schema") != "SLCV30_RZ_A1_RELEASE_MANIFEST_V1"
            or manifest.get("status") != a1_contract.get("required_release_status")
            or manifest.get("promoted") is not False
            or manifest.get("current_pointer_changed") is not False
            or manifest.get("frozen_predecessor_modified") is not False
        ):
            raise InheritanceError("A1 release manifest changed its frozen boundary")
        rows = self._verify_complete_manifest(
            root=a1_root,
            manifest=manifest,
            expected_count=a1_contract["required_release_artifact_count"],
            expected_exclusions=a1_contract["manifest_exclusions"],
            label="A1 release manifest",
        )
        if (
            independent.get("status") != "PASS"
            or independent.get("assertions_failed") != 0
            or independent.get("release_artifacts_hash_verified") != len(rows)
            or independent.get("release_manifest_semantic_sha256")
            != manifest_binding["semantic_sha256"]
            or independent.get("current_pointer_still_slcv21r") is not True
            or independent.get("promoted") is not False
        ):
            raise InheritanceError("A1 independent validation no longer admits inheritance")
        if (
            freeze.get("status") != "COMPLETE_FROZEN_NON_PROMOTED_STOPPED"
            or freeze.get("all_bounded_candidate_workers_stopped") is not True
            or freeze.get("promotion_started") is not False
            or freeze.get("current_pointer") != "SLCV21R"
            or freeze.get("release_manifest_file_sha256") != manifest_binding["sha256"]
            or freeze.get("release_manifest_semantic_sha256") != manifest_binding["semantic_sha256"]
            or freeze.get("independent_validation_file_sha256") != independent_binding["sha256"]
            or freeze.get("independent_validation_semantic_sha256")
            != independent_binding["semantic_sha256"]
        ):
            raise InheritanceError("A1 final freeze tail crosslinks changed")
        if file_sha256(manifest_path) != freeze["release_manifest_file_sha256"]:
            raise InheritanceError("A1 manifest changed after final-freeze crosslink")
        if file_sha256(independent_path) != freeze["independent_validation_file_sha256"]:
            raise InheritanceError("A1 independent validation changed after final-freeze crosslink")
        return manifest, len(rows)

    def _verify_pointer(self, a1_contract: Mapping[str, Any]) -> tuple[Path, str]:
        pointer = self.contract["current_pointer"]
        path = self._repository_path(pointer.get("path"), "current SLC pointer")
        expected = _require_sha256(pointer.get("file_sha256"), "current_pointer.file_sha256")
        observed = file_sha256(path)
        if observed != expected:
            raise InheritanceError("current SLC pointer changed")
        inherited = a1_contract.get("current_pointer")
        if not isinstance(inherited, Mapping) or inherited.get("sha256") != expected:
            raise InheritanceError("Q1 and E1-to-A1 pointer custody differ")
        try:
            pointer_value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise InheritanceError("current SLC pointer is unreadable") from exc
        if pointer.get("resolves_to") not in json.dumps(pointer_value, sort_keys=True):
            raise InheritanceError("current SLC pointer no longer resolves to SLCV21R")
        if pointer.get("used_as_runtime_dependency") is not False:
            raise InheritanceError("Q1 cannot use the mutable current pointer as runtime custody")
        return path, observed

    def verify(self) -> dict[str, Any]:
        """Verify E1, inherited A1, both release tails, and the live pointer."""

        e1_manifest, e1_independent, a1_contract, e1_count = self._verify_e1()
        a1_manifest, a1_count = self._verify_a1(a1_contract)
        pointer_path, pointer_hash = self._verify_pointer(a1_contract)
        receipt = seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_E1_A1_INHERITANCE_VERIFICATION_V1",
                "status": "PASS",
                "candidate": self.contract["candidate"],
                "predecessor": self.contract["predecessor"],
                "inherited_predecessor": a1_contract["predecessor"],
                "e1_release_artifacts_verified": e1_count,
                "a1_release_artifacts_verified": a1_count,
                "post_manifest_tail_artifacts_verified": 4,
                "tail_file_semantic_crosslink_sets_verified": 2,
                "e1_release_manifest_semantic_sha256": e1_manifest["semantic_sha256"],
                "e1_independent_validation_semantic_sha256": e1_independent["semantic_sha256"],
                "a1_release_manifest_semantic_sha256": a1_manifest[
                    "manifest_semantic_sha256"
                ],
                "current_pointer_path": pointer_path.relative_to(self.repository_root).as_posix(),
                "current_pointer_sha256": pointer_hash,
                "current_pointer": "SLCV21R",
                "predecessor_python_imported": False,
                "predecessors_mutated": False,
                "predecessor_copy_created": False,
                "promotion_performed": False,
                "read_only_reconstruction_admission_available": True,
            }
        )
        self._last_verification = receipt
        return deepcopy(receipt)

    def verify_after_execution(self, before: Mapping[str, Any]) -> dict[str, Any]:
        """Require exact predecessor/pointer custody before and after one Q1 action."""

        try:
            require_seal(before, "preexecution inheritance receipt")
        except CanonicalError as exc:
            raise InheritanceError(str(exc)) from exc
        after = self.verify()
        if dict(before) != after:
            raise InheritanceError("predecessor custody identity changed across Q1 execution")
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_POSTEXECUTION_INHERITANCE_ADMISSION_V1",
                "status": "PASS",
                "before_semantic_sha256": before["semantic_sha256"],
                "after_semantic_sha256": after["semantic_sha256"],
                "predecessors_byte_identical": True,
                "current_pointer_unchanged": True,
            }
        )

    def admit_reconstruction(self, reconstruction: Mapping[str, Any]) -> dict[str, Any]:
        """Admit a Q1 reconstruction receipt against the verified frozen E1 identity."""

        verification = self.verify()
        required = {
            "predecessor",
            "predecessor_manifest_semantic_sha256",
            "complete_catalog_reconstructed",
            "checkpoint_replay_identical",
            "semantic_receipts_verified",
            "predecessor_mutated",
            "current_pointer_changed",
        }
        if not isinstance(reconstruction, Mapping) or set(reconstruction) != required:
            raise InheritanceError("reconstruction receipt fields differ from the Q1 admission contract")
        if (
            reconstruction.get("predecessor") != self.contract["predecessor"]
            or reconstruction.get("predecessor_manifest_semantic_sha256")
            != verification["e1_release_manifest_semantic_sha256"]
            or reconstruction.get("complete_catalog_reconstructed") is not True
            or reconstruction.get("checkpoint_replay_identical") is not True
            or reconstruction.get("semantic_receipts_verified") is not True
            or reconstruction.get("predecessor_mutated") is not False
            or reconstruction.get("current_pointer_changed") is not False
        ):
            raise InheritanceError("frozen E1 reconstruction is not admissible")
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_FROZEN_E1_RECONSTRUCTION_ADMISSION_V1",
                "status": "ADMITTED",
                "predecessor": self.contract["predecessor"],
                "inheritance_verification_semantic_sha256": verification["semantic_sha256"],
                "predecessor_manifest_semantic_sha256": verification[
                    "e1_release_manifest_semantic_sha256"
                ],
                "complete_catalog_reconstructed": True,
                "checkpoint_replay_identical": True,
                "semantic_receipts_verified": True,
                "predecessors_mutated": False,
                "current_pointer_changed": False,
            }
        )

    @property
    def last_verification(self) -> dict[str, Any] | None:
        return deepcopy(self._last_verification)


__all__ = [
    "DEFAULT_CONTRACT_PATH",
    "DEFAULT_REPOSITORY_ROOT",
    "E1InheritanceVerifier",
    "InheritanceError",
]
