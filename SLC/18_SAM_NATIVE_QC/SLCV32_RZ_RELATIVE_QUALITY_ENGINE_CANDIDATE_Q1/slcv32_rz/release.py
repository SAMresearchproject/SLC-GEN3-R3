"""Canonical pre-tail release custody for SLCV32-RZ Q1.

The release manifest covers every regular file in the candidate tree except
the manifest itself and the two post-manifest validation/freeze receipts.  A
file is never silently ignored: symlinks, Python bytecode, path escapes,
undeclared additions and missing artifacts are custody failures.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from .canonical import (
    CanonicalError,
    file_sha256,
    load_exact_json,
    require_seal,
    seal_dict,
    write_canonical_json,
)


CANDIDATE = "SLCV32-RZ RELATIVE QUALITY ENGINE CANDIDATE Q1"
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
RELEASE_MANIFEST_PATH = PACKAGE_ROOT / "release" / "RELEASE_MANIFEST.json"

# This is the complete and exact post-manifest tail.  In particular, primary
# validation and all execution evidence remain inside the pre-tail manifest.
MANIFEST_EXCLUSIONS = frozenset(
    {
        "release/FINAL_FREEZE_RECEIPT.json",
        "release/INDEPENDENT_VALIDATION.json",
        "release/RELEASE_MANIFEST.json",
    }
)

REQUIRED_PRETAIL_FILES = frozenset(
    {
        "config/ATOM3D_IMMUTABLE_EXTENSION_CONTRACT.json",
        "config/GROUPED_CATALOG_CONTRACT.json",
        "config/HARDWARE_PROTOCOL_CONTRACT.json",
        "config/QUALITY_TARGET_CONTRACT.json",
        "config/RH_RELATIVE_QUALITY_SERVICE_CONTRACT.json",
        "config/SLCV32_Q1_E1_INHERITANCE_CONTRACT.json",
        "freeze_candidate.py",
        "independent_validate_candidate.py",
        "run_candidate.py",
        "validate_candidate.py",
        "preexecution/COMPLETE_EVALUATION_CATALOGS.json",
        "preexecution/CATALOG_STATISTICS.json",
        "preexecution/HARDER_TRAIN_CATALOG.json",
        "preexecution/Q1_GROUP_SPLIT_MANIFEST.json",
        "preexecution/SELECTOR_BUDGET.json",
        "preexecution/SOURCE_ADMISSION.json",
        "release/ARCHITECTURE_RESULT.json",
        "release/DEPENDENCY_SOURCE_MANIFEST.json",
        "release/QUALITY_ENGINE_RESULT.json",
        "release/VALIDATION_RESULT.json",
        "release/atom3d/ATOM3D_EXTENSION_RECEIPT.json",
        "release/execution/AMBIGUITY_SERVICE_RECEIPT.json",
        "release/execution/CHECKPOINT_CHAIN_PRIMARY.json",
        "release/execution/CHECKPOINT_CHAIN_REPLAY.json",
        "release/execution/CHECKPOINT_REPLAY_IDENTITY.json",
        "release/execution/FROZEN_PREDECESSOR_RECONSTRUCTION_ADMISSION.json",
        "release/execution/SELECTOR_COMPARISON_PRIMARY.json",
        "release/execution/SELECTOR_COMPARISON_REPLAY.json",
        "release/hardware/HARDWARE_PROTOCOL_RESULT.json",
        "release/rh/RH_SERVICE_DECISION.json",
        "slcv32_rz/__init__.py",
        "slcv32_rz/canonical.py",
        "slcv32_rz/catalogs.py",
        "slcv32_rz/checkpoints.py",
        "slcv32_rz/evaluation.py",
        "slcv32_rz/extensions.py",
        "slcv32_rz/hardware.py",
        "slcv32_rz/inheritance.py",
        "slcv32_rz/pipeline.py",
        "slcv32_rz/release.py",
        "slcv32_rz/selectors.py",
        "slcv32_rz/source_quality.py",
        "tests/test_boundaries.py",
        "tests/test_release.py",
        "tests/test_selectors_evaluation.py",
        "tests/test_source_quality_catalogs.py",
    }
)

REQUIRED_FALSE_BOUNDARIES = frozenset(
    {
        "atom3d_specialization_started",
        "current_pointer_changed",
        "frozen_predecessor_modified",
        "full_scale_tuning_started",
        "git_custody_performed",
        "m143064041_touched",
        "native_780m_execution_credited",
        "physical_calibration_started",
        "prime_work_performed",
        "production_deployment_started",
        "promoted",
        "publication_or_sync_performed",
        "remote_transfer_performed",
    }
)


class ReleaseCustodyError(CanonicalError):
    """The Q1 pre-tail release tree differs from its exact custody contract."""


def strict_relative(value: str) -> str:
    """Return a normalized strict POSIX relative path or reject it."""

    if not isinstance(value, str) or not value or "\\" in value:
        raise ReleaseCustodyError(f"release path is not strict relative: {value!r}")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise ReleaseCustodyError(f"release path is not strict relative: {value!r}")
    if relative.as_posix() != value:
        raise ReleaseCustodyError(f"release path is not canonical POSIX form: {value!r}")
    return value


def _resolved_root(root: str | Path) -> Path:
    supplied = Path(root)
    if supplied.is_symlink():
        raise ReleaseCustodyError("candidate root cannot be a symlink")
    try:
        resolved = supplied.resolve(strict=True)
    except OSError as exc:
        raise ReleaseCustodyError(f"candidate root is unavailable: {supplied}") from exc
    if not resolved.is_dir():
        raise ReleaseCustodyError("candidate root is not a directory")
    return resolved


def _normalize_required(expected_files: Iterable[str]) -> frozenset[str]:
    rows = [strict_relative(path) for path in expected_files]
    if len(rows) != len(set(rows)):
        raise ReleaseCustodyError("required pre-tail file roster contains duplicates")
    excluded = sorted(set(rows) & MANIFEST_EXCLUSIONS)
    if excluded:
        raise ReleaseCustodyError(f"post-manifest tail cannot be required pre-tail: {excluded}")
    return frozenset(rows)


def candidate_file_roster(root: str | Path = PACKAGE_ROOT) -> tuple[Path, ...]:
    """Return every admitted pre-tail file and reject indirect/bytecode paths."""

    base = _resolved_root(root)
    files: list[Path] = []
    for path in base.rglob("*"):
        if path.is_symlink():
            raise ReleaseCustodyError(f"candidate tree contains prohibited symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(base).as_posix()
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            raise ReleaseCustodyError(f"candidate tree contains prohibited bytecode: {relative}")
        if relative in MANIFEST_EXCLUSIONS:
            continue
        files.append(path)
    return tuple(sorted(files, key=lambda path: path.relative_to(base).as_posix()))


def bytecode_artifacts(root: str | Path = PACKAGE_ROOT) -> tuple[str, ...]:
    """List bytecode artifacts without otherwise validating the tree."""

    base = _resolved_root(root)
    return tuple(
        sorted(
            path.relative_to(base).as_posix()
            for path in base.rglob("*")
            if path.is_file()
            and ("__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"})
        )
    )


def build_release_manifest(
    *,
    root: str | Path = PACKAGE_ROOT,
    output_path: str | Path = RELEASE_MANIFEST_PATH,
    expected_files: Iterable[str] = REQUIRED_PRETAIL_FILES,
) -> dict[str, Any]:
    """Build the canonical complete pre-tail manifest.

    ``expected_files`` permits the orchestrator to bind an even larger frozen
    release roster while retaining Q1's mandatory core.  It may not weaken the
    mandatory roster.
    """

    base = _resolved_root(root)
    output = Path(output_path)
    if output.is_symlink():
        raise ReleaseCustodyError("release manifest output cannot be a symlink")
    try:
        output_relative = output.resolve(strict=False).relative_to(base).as_posix()
    except ValueError as exc:
        raise ReleaseCustodyError("release manifest output escapes candidate root") from exc
    if output_relative != "release/RELEASE_MANIFEST.json":
        raise ReleaseCustodyError("release manifest output must be its canonical excluded path")

    required = _normalize_required(expected_files)
    if not REQUIRED_PRETAIL_FILES <= required:
        missing_core = sorted(REQUIRED_PRETAIL_FILES - required)
        raise ReleaseCustodyError(f"required pre-tail roster weakens Q1 core: {missing_core}")
    paths = candidate_file_roster(base)
    declared = {path.relative_to(base).as_posix() for path in paths}
    missing = sorted(required - declared)
    if missing:
        raise ReleaseCustodyError(f"required Q1 pre-tail files are missing: {missing}")
    artifacts = [
        {
            "bytes": path.stat().st_size,
            "path": path.relative_to(base).as_posix(),
            "sha256": file_sha256(path),
        }
        for path in paths
    ]
    manifest = seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_RELEASE_MANIFEST_V1",
            "status": "SEALED_COMPLETE_PRETAIL_NON_PROMOTED_CANDIDATE",
            "candidate": CANDIDATE,
            "artifact_count": len(artifacts),
            "artifacts": artifacts,
            "manifest_exclusions": sorted(MANIFEST_EXCLUSIONS),
            "required_pretail_files": sorted(required),
            "boundaries": {name: False for name in sorted(REQUIRED_FALSE_BOUNDARIES)},
        }
    )
    write_canonical_json(output, manifest)
    return manifest


def verify_release_manifest(
    manifest_path: str | Path = RELEASE_MANIFEST_PATH,
    *,
    root: str | Path = PACKAGE_ROOT,
    expected_files: Iterable[str] = REQUIRED_PRETAIL_FILES,
) -> dict[str, Any]:
    """Verify hashes, sizes, roster completeness, semantics and boundaries."""

    base = _resolved_root(root)
    manifest_input = Path(manifest_path)
    if manifest_input.is_symlink():
        raise ReleaseCustodyError("release manifest cannot be a symlink")
    try:
        manifest_resolved = manifest_input.resolve(strict=True)
        manifest_resolved.relative_to(base)
    except (OSError, ValueError) as exc:
        raise ReleaseCustodyError("release manifest escapes or is unavailable") from exc
    if manifest_resolved.relative_to(base).as_posix() != "release/RELEASE_MANIFEST.json":
        raise ReleaseCustodyError("release manifest is not at its canonical path")

    value = load_exact_json(manifest_resolved)
    if not isinstance(value, Mapping):
        raise ReleaseCustodyError("release manifest must be an object")
    try:
        require_seal(value, "Q1 release manifest")
    except CanonicalError as exc:
        raise ReleaseCustodyError(str(exc)) from exc
    if value.get("schema") != "SLCV32_RZ_Q1_RELEASE_MANIFEST_V1":
        raise ReleaseCustodyError("release manifest schema differs")
    if value.get("status") != "SEALED_COMPLETE_PRETAIL_NON_PROMOTED_CANDIDATE":
        raise ReleaseCustodyError("release manifest status differs")
    if value.get("candidate") != CANDIDATE:
        raise ReleaseCustodyError("release manifest candidate differs")
    if value.get("manifest_exclusions") != sorted(MANIFEST_EXCLUSIONS):
        raise ReleaseCustodyError("release manifest exclusions differ")

    required = _normalize_required(expected_files)
    if not REQUIRED_PRETAIL_FILES <= required:
        raise ReleaseCustodyError("verification required roster weakens Q1 core")
    if value.get("required_pretail_files") != sorted(required):
        raise ReleaseCustodyError("release manifest required pre-tail roster differs")
    boundaries = value.get("boundaries")
    if not isinstance(boundaries, Mapping) or set(boundaries) != REQUIRED_FALSE_BOUNDARIES:
        raise ReleaseCustodyError("release manifest prohibited-boundary roster differs")
    if any(boundaries[name] is not False for name in boundaries):
        raise ReleaseCustodyError("release manifest crossed a prohibited boundary")

    rows = value.get("artifacts")
    if not isinstance(rows, list) or value.get("artifact_count") != len(rows):
        raise ReleaseCustodyError("release manifest artifact count differs")
    by_path: dict[str, Mapping[str, Any]] = {}
    order: list[str] = []
    for index, raw in enumerate(rows):
        if not isinstance(raw, Mapping) or set(raw) != {"bytes", "path", "sha256"}:
            raise ReleaseCustodyError(f"release artifact row {index} is invalid")
        relative = strict_relative(raw["path"])
        if relative in MANIFEST_EXCLUSIONS or relative in by_path:
            raise ReleaseCustodyError(f"release artifact path is excluded/duplicated: {relative}")
        cursor = base
        for part in PurePosixPath(relative).parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ReleaseCustodyError(f"release artifact uses symlink: {relative}")
        try:
            path = cursor.resolve(strict=True)
            path.relative_to(base)
        except (OSError, ValueError) as exc:
            raise ReleaseCustodyError(f"release artifact escapes or is absent: {relative}") from exc
        if not path.is_file():
            raise ReleaseCustodyError(f"release artifact is not a file: {relative}")
        byte_count = raw["bytes"]
        digest = raw["sha256"]
        if (
            isinstance(byte_count, bool)
            or not isinstance(byte_count, int)
            or byte_count < 0
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ReleaseCustodyError(f"release artifact metadata is invalid: {relative}")
        if path.stat().st_size != byte_count or file_sha256(path) != digest:
            raise ReleaseCustodyError(f"release artifact differs from manifest: {relative}")
        by_path[relative] = raw
        order.append(relative)
    if order != sorted(order):
        raise ReleaseCustodyError("release artifact roster is not in canonical order")
    actual = {path.relative_to(base).as_posix() for path in candidate_file_roster(base)}
    if actual != set(by_path):
        raise ReleaseCustodyError(
            "release artifact roster drifted; "
            f"undeclared={sorted(actual - set(by_path))}, missing={sorted(set(by_path) - actual)}"
        )
    if not required <= set(by_path):
        raise ReleaseCustodyError("release manifest omits a required pre-tail file")
    return dict(value)


__all__ = [
    "CANDIDATE",
    "MANIFEST_EXCLUSIONS",
    "PACKAGE_ROOT",
    "RELEASE_MANIFEST_PATH",
    "REQUIRED_FALSE_BOUNDARIES",
    "REQUIRED_PRETAIL_FILES",
    "ReleaseCustodyError",
    "build_release_manifest",
    "bytecode_artifacts",
    "candidate_file_roster",
    "strict_relative",
    "verify_release_manifest",
]
