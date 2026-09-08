"""Strict binding of Q3 to one copied, sealed V6/ICF1 foundation bundle."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .canonical import canonical_sha256, file_sha256, load_exact_json


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BINDING_PATH = CANDIDATE_ROOT / "preexecution/SEALED_ICF1_BINDING.json"
BINDING_SCHEMA = "SLCV33_ICF1_SEALED_FOUNDATION_BINDING_V1"
BINDING_STATUS = "SEALED_UNINSTALLED_FOUNDATION_BOUND"


class FoundationBindingError(RuntimeError):
    """The sealed V6 foundation bundle is absent, foreign, or not exactly bound."""


@dataclass(frozen=True, slots=True)
class FoundationBinding:
    path: Path
    candidate_root: Path
    foundation_release: str
    custody_product: str
    custody_release: str
    snapshot_path: Path
    snapshot_relative_path: str
    snapshot_sha256: str
    snapshot_metadata_sha256: str
    active_source_semantic_sha256: str
    test_source_semantic_sha256: str
    source_file_count: int
    test_file_count: int
    tests_passed: int
    release_manifest_path: Path
    release_manifest_sha256: str
    release_manifest_semantic_sha256: str
    independent_validation_path: Path
    independent_validation_sha256: str
    independent_validation_semantic_sha256: str
    native_module_archive_path: str
    native_module_sha256: str
    import_policy: str
    binding_file_sha256: str

    @property
    def semantic_sha256(self) -> str:
        """Compatibility alias for the bound V6 active-source semantic identity."""

        return self.active_source_semantic_sha256


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FoundationBindingError(f"{label} must be a JSON object")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise FoundationBindingError(f"{label} must be a nonempty string")
    return value


def _sha256(value: Any, label: str) -> str:
    digest = _text(value, label)
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise FoundationBindingError(f"{label} must be lowercase hexadecimal SHA-256")
    return digest


def _strict_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise FoundationBindingError(f"{label} must be a nonnegative exact integer")
    return value


def _contained_path(candidate_root: Path, relative: Any, label: str) -> tuple[str, Path]:
    text = _text(relative, label)
    raw = Path(text)
    if raw.is_absolute() or ".." in raw.parts:
        raise FoundationBindingError(f"{label} must be candidate-root-relative and contained")
    root = candidate_root.resolve()
    resolved = (root / raw).resolve()
    if not resolved.is_relative_to(root):
        raise FoundationBindingError(f"{label} resolves outside the Q3 candidate root")
    return text, resolved


def _verify_bound_json_artifact(
    candidate_root: Path,
    row: Mapping[str, Any],
    label: str,
) -> tuple[Path, str, str]:
    _relative, path = _contained_path(candidate_root, row.get("path"), f"{label}.path")
    raw_hash = _sha256(row.get("raw_sha256"), f"{label}.raw_sha256")
    semantic = _sha256(row.get("semantic_sha256"), f"{label}.semantic_sha256")
    if not path.is_file() or file_sha256(path) != raw_hash:
        raise FoundationBindingError(f"{label} bytes are absent or differ: {path}")
    value = load_exact_json(path)
    if not isinstance(value, Mapping):
        raise FoundationBindingError(f"{label} is not an exact JSON object")
    actual_semantic = value.get("semantic_sha256")
    if actual_semantic is None:
        actual_semantic = canonical_sha256(value)
    if actual_semantic != semantic:
        raise FoundationBindingError(f"{label} semantic identity differs")
    return path, raw_hash, semantic


def require_sealed_icf1_binding(
    path: str | Path = DEFAULT_BINDING_PATH,
) -> FoundationBinding:
    """Verify the concrete copied-foundation binding and every named artifact."""

    binding_path = Path(path)
    if not binding_path.is_file():
        raise FoundationBindingError(
            f"Q3 execution blocked: sealed ICF1 binding is absent: {binding_path}"
        )
    candidate_root = binding_path.resolve().parent.parent
    value = _mapping(load_exact_json(binding_path), "ICF1 binding")
    if value.get("schema") != BINDING_SCHEMA or value.get("status") != BINDING_STATUS:
        raise FoundationBindingError("ICF1 binding schema or sealed status differs")
    if value.get("foundation_release") != "SLCV33-ICF1":
        raise FoundationBindingError("ICF1 foundation release differs")
    if value.get("custody_product") != "SLC_CUSTODY_NATIVE_ARCHITECTURE":
        raise FoundationBindingError("ICF1 custody product differs")
    if value.get("custody_release") != "V6":
        raise FoundationBindingError("ICF1 custody release differs")
    if value.get("import_policy") != (
        "EXTRACT_EPHEMERALLY_VERIFY_EVERY_ARCHIVE_MEMBER_IMPORT_BOUND_SRC_ONLY"
    ):
        raise FoundationBindingError("ICF1 bound-snapshot import policy differs")
    if value.get("installed_or_promoted") is not False:
        raise FoundationBindingError("ICF1 binding must remain uninstalled and unpromoted")

    snapshot = _mapping(value.get("snapshot"), "snapshot binding")
    snapshot_relative, snapshot_path = _contained_path(
        candidate_root, snapshot.get("path"), "snapshot.path"
    )
    if snapshot_relative != "foundation/SLCV33-ICF1/SOURCE_SNAPSHOT.zip":
        raise FoundationBindingError("ICF1 snapshot candidate-relative path differs")
    snapshot_hash = _sha256(snapshot.get("raw_sha256"), "snapshot.raw_sha256")
    if not snapshot_path.is_file() or file_sha256(snapshot_path) != snapshot_hash:
        raise FoundationBindingError("bound V6 snapshot bytes are absent or differ")
    snapshot_metadata = _sha256(snapshot.get("metadata_sha256"), "snapshot.metadata_sha256")
    active_semantic = _sha256(
        snapshot.get("active_source_semantic_sha256"),
        "snapshot.active_source_semantic_sha256",
    )
    test_semantic = _sha256(
        snapshot.get("test_source_semantic_sha256"),
        "snapshot.test_source_semantic_sha256",
    )
    source_count = _strict_nonnegative_int(snapshot.get("source_file_count"), "source_file_count")
    test_count = _strict_nonnegative_int(snapshot.get("test_file_count"), "test_file_count")
    tests_passed = _strict_nonnegative_int(snapshot.get("tests_passed"), "tests_passed")
    if source_count < 1 or test_count < 1 or tests_passed < 1:
        raise FoundationBindingError("bound V6 snapshot counts must be positive")

    release_path, release_hash, release_semantic = _verify_bound_json_artifact(
        candidate_root,
        _mapping(value.get("release_manifest"), "release_manifest"),
        "release_manifest",
    )
    validation_path, validation_hash, validation_semantic = _verify_bound_json_artifact(
        candidate_root,
        _mapping(value.get("independent_validation"), "independent_validation"),
        "independent_validation",
    )
    native = _mapping(value.get("native_module"), "native_module")
    archive_path = _text(native.get("archive_path"), "native_module.archive_path")
    archive = Path(archive_path)
    if archive.is_absolute() or ".." in archive.parts or archive_path != "src/slc_custody/native_substrate.py":
        raise FoundationBindingError("bound native-module archive path differs")
    native_hash = _sha256(native.get("sha256"), "native_module.sha256")
    return FoundationBinding(
        path=binding_path.resolve(),
        candidate_root=candidate_root,
        foundation_release="SLCV33-ICF1",
        custody_product="SLC_CUSTODY_NATIVE_ARCHITECTURE",
        custody_release="V6",
        snapshot_path=snapshot_path,
        snapshot_relative_path=snapshot_relative,
        snapshot_sha256=snapshot_hash,
        snapshot_metadata_sha256=snapshot_metadata,
        active_source_semantic_sha256=active_semantic,
        test_source_semantic_sha256=test_semantic,
        source_file_count=source_count,
        test_file_count=test_count,
        tests_passed=tests_passed,
        release_manifest_path=release_path,
        release_manifest_sha256=release_hash,
        release_manifest_semantic_sha256=release_semantic,
        independent_validation_path=validation_path,
        independent_validation_sha256=validation_hash,
        independent_validation_semantic_sha256=validation_semantic,
        native_module_archive_path=archive_path,
        native_module_sha256=native_hash,
        import_policy=str(value["import_policy"]),
        binding_file_sha256=file_sha256(binding_path),
    )
