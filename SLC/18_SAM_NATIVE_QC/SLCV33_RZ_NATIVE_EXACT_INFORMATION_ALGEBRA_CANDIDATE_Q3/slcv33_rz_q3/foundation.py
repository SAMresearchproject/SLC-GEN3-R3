"""Verified ephemeral consumption of the sealed V6/ICF1 source snapshot.

Q3 is a projection consumer.  It does not originate HD, formal-log, finite
partition, receipt-sufficiency, or custody-ledger objects.  Those objects are
constructed by the exact ``slc_custody`` implementation imported from the
bound V6 archive after every archived member has been verified.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile
from types import ModuleType
from typing import Any, Mapping
import zipfile

from .binding import FoundationBinding
from .canonical import canonical_sha256


SNAPSHOT_METADATA_SCHEMA = "SLC_CUSTODY_NATIVE_ARCHITECTURE_SOURCE_SNAPSHOT_V6"
BOUND_HD_SCHEMA = "SLCV33_RZ_Q3_BOUND_V6_HD_OBJECT_V1"
BOUND_CUSTODY_SCHEMA = "SLCV33_RZ_Q3_BOUND_V6_CUSTODY_OBJECT_V1"
UNDEFINED_QUOTIENT_SCHEMA = "SLCV33_RZ_Q3_V6_UNDEFINED_QUOTIENT_V1"


class FoundationConsumptionError(RuntimeError):
    """The V6 archive, import origin, or canonical serialization differs."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _inventory_semantic(rows: object, label: str) -> str:
    if not isinstance(rows, list):
        raise FoundationConsumptionError(f"{label} inventory is not a list")
    return _sha256_bytes(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _archive_relative(name: object, label: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name:
        raise FoundationConsumptionError(f"{label} is not a canonical archive path")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise FoundationConsumptionError(f"{label} escapes the archive root")
    if str(path) != name:
        raise FoundationConsumptionError(f"{label} is not normalized")
    return name


def _fraction_dict(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def _strict_roundtrip(cls: type, serialized: Mapping[str, Any], label: str) -> None:
    restored = cls.from_dict(serialized)
    if restored.to_dict() != dict(serialized):
        raise FoundationConsumptionError(f"bound V6 {label} serialization is not stable")


class BoundV6Foundation:
    """Context-bound importer and canonical-object factory for one V6 archive."""

    def __init__(self, binding: FoundationBinding) -> None:
        self.binding = binding
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self._source_root: Path | None = None
        self._imported_names: tuple[str, ...] = ()
        self._active = False
        self._metadata: Mapping[str, Any] | None = None
        self.package: ModuleType | None = None
        self.hd_module: ModuleType | None = None
        self.information_module: ModuleType | None = None
        self.native_module: ModuleType | None = None

    @property
    def source_root(self) -> Path:
        if self._source_root is None:
            raise FoundationConsumptionError("bound V6 foundation is not active")
        return self._source_root

    def _require_active(self) -> None:
        if not self._active:
            raise FoundationConsumptionError("bound V6 foundation is not active")

    @staticmethod
    def _reject_preloaded_foreign_package() -> None:
        foreign = sorted(
            name for name in sys.modules
            if name == "slc_custody" or name.startswith("slc_custody.")
        )
        if foreign:
            raise FoundationConsumptionError(
                "foreign or mutable slc_custody modules are already loaded: "
                + ", ".join(foreign)
            )

    def _verify_archive(self) -> tuple[Mapping[str, Any], dict[str, bytes]]:
        try:
            archive = zipfile.ZipFile(self.binding.snapshot_path, "r")
        except (OSError, zipfile.BadZipFile) as exc:
            raise FoundationConsumptionError("bound V6 snapshot is not a readable ZIP") from exc
        with archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise FoundationConsumptionError("bound V6 snapshot has duplicate members")
            for info in infos:
                _archive_relative(info.filename, "archive member")
                if info.is_dir() or info.flag_bits & 0x1:
                    raise FoundationConsumptionError("bound V6 snapshot has a directory or encrypted member")
                mode = info.external_attr >> 16
                file_type = stat.S_IFMT(mode)
                if file_type not in (0, stat.S_IFREG):
                    raise FoundationConsumptionError("bound V6 snapshot has a non-regular member")
            try:
                metadata_payload = archive.read("SNAPSHOT_METADATA.json")
                metadata = json.loads(metadata_payload.decode("utf-8"))
            except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise FoundationConsumptionError("bound V6 snapshot metadata is absent or invalid") from exc
            if _sha256_bytes(metadata_payload) != self.binding.snapshot_metadata_sha256:
                raise FoundationConsumptionError("bound V6 snapshot metadata hash differs")
            if not isinstance(metadata, Mapping):
                raise FoundationConsumptionError("bound V6 snapshot metadata is not an object")
            if (
                metadata.get("schema") != SNAPSHOT_METADATA_SCHEMA
                or metadata.get("product") != self.binding.custody_product
                or metadata.get("release") != self.binding.custody_release
                or metadata.get("foundation") != self.binding.foundation_release
            ):
                raise FoundationConsumptionError("bound V6 snapshot metadata identity differs")
            source_rows = metadata.get("source_files")
            test_rows = metadata.get("test_files")
            if _inventory_semantic(source_rows, "source") != self.binding.active_source_semantic_sha256:
                raise FoundationConsumptionError("bound V6 source inventory semantic hash differs")
            if _inventory_semantic(test_rows, "test") != self.binding.test_source_semantic_sha256:
                raise FoundationConsumptionError("bound V6 test inventory semantic hash differs")
            if metadata.get("active_source_semantic_sha256") != self.binding.active_source_semantic_sha256:
                raise FoundationConsumptionError("bound V6 metadata source semantic differs")
            if metadata.get("test_source_semantic_sha256") != self.binding.test_source_semantic_sha256:
                raise FoundationConsumptionError("bound V6 metadata test semantic differs")
            if metadata.get("expected_tests") != self.binding.tests_passed:
                raise FoundationConsumptionError("bound V6 metadata test count differs")
            if not isinstance(source_rows, list) or not isinstance(test_rows, list):
                raise FoundationConsumptionError("bound V6 inventories are not lists")
            if len(source_rows) != self.binding.source_file_count or len(test_rows) != self.binding.test_file_count:
                raise FoundationConsumptionError("bound V6 inventory counts differ")

            payload_by_name: dict[str, bytes] = {
                "SNAPSHOT_METADATA.json": metadata_payload
            }
            expected_names = {"SNAPSHOT_METADATA.json"}
            for root_name, rows in (("src", source_rows), ("tests", test_rows)):
                seen: set[str] = set()
                for index, row in enumerate(rows):
                    if not isinstance(row, Mapping) or set(row) != {"bytes", "path", "sha256"}:
                        raise FoundationConsumptionError(
                            f"bound V6 {root_name} inventory row {index} is noncanonical"
                        )
                    relative = _archive_relative(row.get("path"), f"{root_name} inventory path")
                    if relative in seen:
                        raise FoundationConsumptionError(f"bound V6 {root_name} inventory repeats a path")
                    seen.add(relative)
                    member = f"{root_name}/{relative}"
                    expected_names.add(member)
                    try:
                        payload = archive.read(member)
                    except KeyError as exc:
                        raise FoundationConsumptionError(f"bound V6 member is absent: {member}") from exc
                    size = row.get("bytes")
                    digest = row.get("sha256")
                    if type(size) is not int or size < 0 or len(payload) != size:
                        raise FoundationConsumptionError(f"bound V6 member size differs: {member}")
                    if not isinstance(digest, str) or _sha256_bytes(payload) != digest:
                        raise FoundationConsumptionError(f"bound V6 member hash differs: {member}")
                    payload_by_name[member] = payload
            if set(names) != expected_names:
                raise FoundationConsumptionError("bound V6 archive member roster differs from metadata")
            native_payload = payload_by_name.get(self.binding.native_module_archive_path)
            if native_payload is None or _sha256_bytes(native_payload) != self.binding.native_module_sha256:
                raise FoundationConsumptionError("bound V6 native module hash differs")
            return metadata, payload_by_name

    def __enter__(self) -> "BoundV6Foundation":
        if self._active:
            raise FoundationConsumptionError("bound V6 foundation context cannot be reentered")
        self._reject_preloaded_foreign_package()
        metadata, payloads = self._verify_archive()
        self._temporary = tempfile.TemporaryDirectory(prefix="slcv33_q3_bound_v6_")
        root = Path(self._temporary.name).resolve()
        for name, payload in sorted(payloads.items()):
            target = root.joinpath(*PurePosixPath(name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        source_root = root / "src"
        sys.path.insert(0, str(source_root))
        prior_names = set(sys.modules)
        try:
            package = importlib.import_module("slc_custody")
            hd_module = importlib.import_module("slc_custody.hd")
            information_module = importlib.import_module("slc_custody.information")
            native_module = importlib.import_module("slc_custody.native_substrate")
            imported_names = tuple(
                sorted(
                    name for name in set(sys.modules) - prior_names
                    if name == "slc_custody" or name.startswith("slc_custody.")
                )
            )
            for name in imported_names:
                module = sys.modules[name]
                origin = getattr(module, "__file__", None)
                if origin is None or not Path(origin).resolve().is_relative_to(source_root):
                    raise FoundationConsumptionError(
                        f"bound V6 import resolved outside extracted src: {name}"
                    )
            native_origin = Path(native_module.__file__).resolve()
            if native_origin != (source_root / self.binding.native_module_archive_path.removeprefix("src/")).resolve():
                raise FoundationConsumptionError("bound V6 native module origin differs")
            if _sha256_bytes(native_origin.read_bytes()) != self.binding.native_module_sha256:
                raise FoundationConsumptionError("imported bound V6 native module bytes differ")
        except Exception:
            for name in tuple(sys.modules):
                if name == "slc_custody" or name.startswith("slc_custody."):
                    sys.modules.pop(name, None)
            if sys.path and sys.path[0] == str(source_root):
                sys.path.pop(0)
            else:
                try:
                    sys.path.remove(str(source_root))
                except ValueError:
                    pass
            self._temporary.cleanup()
            self._temporary = None
            raise
        self._source_root = source_root
        self._metadata = metadata
        self._imported_names = imported_names
        self.package = package
        self.hd_module = hd_module
        self.information_module = information_module
        self.native_module = native_module
        self._active = True
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        source_text = str(self._source_root) if self._source_root is not None else None
        for name in reversed(self._imported_names):
            sys.modules.pop(name, None)
        if source_text is not None:
            try:
                sys.path.remove(source_text)
            except ValueError:
                pass
        if self._temporary is not None:
            self._temporary.cleanup()
        self._temporary = None
        self._source_root = None
        self._metadata = None
        self._imported_names = ()
        self.package = None
        self.hd_module = None
        self.information_module = None
        self.native_module = None
        self._active = False

    @property
    def import_receipt(self) -> dict[str, object]:
        self._require_active()
        body = {
            "schema": "SLCV33_RZ_Q3_BOUND_V6_IMPORT_RECEIPT_V1",
            "foundation_release": self.binding.foundation_release,
            "custody_product": self.binding.custody_product,
            "custody_release": self.binding.custody_release,
            "snapshot_path": self.binding.snapshot_relative_path,
            "snapshot_sha256": self.binding.snapshot_sha256,
            "snapshot_metadata_sha256": self.binding.snapshot_metadata_sha256,
            "active_source_semantic_sha256": self.binding.active_source_semantic_sha256,
            "test_source_semantic_sha256": self.binding.test_source_semantic_sha256,
            "source_file_count": self.binding.source_file_count,
            "test_file_count": self.binding.test_file_count,
            "tests_passed": self.binding.tests_passed,
            "native_module_archive_path": self.binding.native_module_archive_path,
            "native_module_sha256": self.binding.native_module_sha256,
            "import_policy": self.binding.import_policy,
            "module_origin": "EPHEMERALLY_EXTRACTED_BOUND_SNAPSHOT_SRC",
            "active_source_imported": False,
            "every_archive_member_verified": True,
        }
        return {**body, "semantic_sha256": canonical_sha256(body)}

    def serialize_hd(
        self,
        value: int | Fraction,
        *,
        source_provenance: str,
    ) -> dict[str, object]:
        """Construct one HD object and all finite proof objects in bound V6."""

        self._require_active()
        exact = Fraction(value)
        assert self.hd_module is not None and self.native_module is not None
        signature_cls = self.hd_module.HDSignature
        signature = signature_cls.from_rational(exact)
        signature_row = signature.to_dict()
        _strict_roundtrip(signature_cls, signature_row, "HD signature")
        body: dict[str, object] = {
            "schema": BOUND_HD_SCHEMA,
            "exact_rational": _fraction_dict(exact),
            "hd_signature": signature_row,
            "source_provenance": source_provenance,
        }
        if exact == 0:
            body.update(
                {
                    "prime_valuation_vector": None,
                    "formal_log_monoid_element": None,
                    "bounded_factor_proof": None,
                    "zero_boundary": "DISTINCT_ZERO_VARIANT_NO_FINITE_VALUATION",
                }
            )
        else:
            valuation_cls = self.native_module.PrimeValuationVector
            valuation = valuation_cls.from_rational(
                exact, source_provenance=source_provenance
            )
            valuation_row = valuation.to_dict()
            _strict_roundtrip(valuation_cls, valuation_row, "prime valuation vector")
            formal_cls = self.native_module.FormalLogMonoidElement
            formal = formal_cls.from_positive_rational(
                abs(exact), source_provenance=source_provenance
            )
            formal_row = formal.to_dict()
            _strict_roundtrip(formal_cls, formal_row, "formal-log monoid element")
            factor_cls = self.hd_module.RationalFactorProof
            factor = factor_cls.build(
                exact,
                maximum_component=max(abs(exact.numerator), exact.denominator),
            )
            factor_row = factor.to_dict()
            _strict_roundtrip(factor_cls, factor_row, "bounded factor proof")
            if valuation.rational_value != exact or signature.value != exact:
                raise FoundationConsumptionError("bound V6 HD reconstruction differs")
            body.update(
                {
                    "prime_valuation_vector": valuation_row,
                    "formal_log_monoid_element": formal_row,
                    "bounded_factor_proof": factor_row,
                    "zero_boundary": None,
                }
            )
        body["semantic_sha256"] = canonical_sha256(body)
        return body

    def hd_product(
        self,
        left: Mapping[str, Any],
        right: Mapping[str, Any],
        *,
        source_provenance: str,
    ) -> dict[str, object]:
        self._require_active()
        assert self.hd_module is not None
        left_signature = self.hd_module.HDSignature.from_dict(left["hd_signature"])
        right_signature = self.hd_module.HDSignature.from_dict(right["hd_signature"])
        result = left_signature.multiply(right_signature)
        serialized = self.serialize_hd(result.value, source_provenance=source_provenance)
        if serialized["hd_signature"] != result.to_dict():
            raise FoundationConsumptionError("bound V6 HD product serialization differs")
        return serialized

    def hd_quotient(
        self,
        numerator: Mapping[str, Any],
        denominator: Mapping[str, Any],
        *,
        source_provenance: str,
    ) -> dict[str, object]:
        self._require_active()
        assert self.hd_module is not None
        top = self.hd_module.HDSignature.from_dict(numerator["hd_signature"])
        bottom = self.hd_module.HDSignature.from_dict(denominator["hd_signature"])
        if bottom.is_zero:
            body = {
                "schema": UNDEFINED_QUOTIENT_SCHEMA,
                "variant": "UNDEFINED_QUOTIENT",
                "reason": "V6_HD_DIVISION_BY_DISTINCT_ZERO_VARIANT",
                "numerator_semantic_sha256": numerator["semantic_sha256"],
                "denominator_semantic_sha256": denominator["semantic_sha256"],
                "source_provenance": source_provenance,
            }
            return {**body, "semantic_sha256": canonical_sha256(body)}
        result = top.divide(bottom)
        serialized = self.serialize_hd(result.value, source_provenance=source_provenance)
        if serialized["hd_signature"] != result.to_dict():
            raise FoundationConsumptionError("bound V6 HD quotient serialization differs")
        return serialized

    def serialize_custody(
        self,
        best_orientation_multiplicity: int,
        other_orientation_multiplicity: int,
    ) -> dict[str, object]:
        """Construct the exact two-channel custody object in bound V6."""

        self._require_active()
        if type(best_orientation_multiplicity) is not int or type(other_orientation_multiplicity) is not int:
            raise FoundationConsumptionError("custody multiplicities must be exact integers")
        if best_orientation_multiplicity < 1 or other_orientation_multiplicity < 1:
            raise FoundationConsumptionError("custody multiplicities must be positive")
        assert self.hd_module is not None
        assert self.information_module is not None
        assert self.native_module is not None
        best = best_orientation_multiplicity
        other = other_orientation_multiplicity
        multiplicity = best + other
        domain = tuple((orientation, index) for orientation, size in enumerate((best, other)) for index in range(size))
        partition_cls = self.information_module.InformationPartition
        visible = partition_cls.from_map("Q3_VISIBLE_GROUP", domain, lambda _item: 0)
        orientation = partition_cls.from_map("Q3_ORIENTATION", domain, lambda item: item[0])
        realization = partition_cls.from_map("Q3_REALIZATION", domain, lambda item: item[1])
        channel_cls = self.information_module.ReceiptChannel
        system = self.information_module.ReceiptSystem(
            visible,
            (
                channel_cls("ORIENTATION_RECEIPT", orientation),
                channel_cls("REALIZATION_RECEIPT", realization),
            ),
        )
        distribution = self.information_module.ExactDistribution.uniform(
            domain,
            provenance="Q3_FROZEN_PHYSICAL_GROUP_UNIFORM_MEMBER_LAW",
        )
        sufficiency = system.minimum_sufficient_channels()
        if (
            sufficiency.selected_channels
            != ("ORIENTATION_RECEIPT", "REALIZATION_RECEIPT")
            or not sufficiency.reconstructs_source
            or not sufficiency.exact_minimum
        ):
            raise FoundationConsumptionError("bound V6 minimum receipt custody differs")
        identity = system.information_identity(distribution, sufficiency.selected_channels)
        uncomputation = system.uncomputation_plan()
        if identity.get("identity_exact") is not True or identity.get("augmented_injective") is not True:
            raise FoundationConsumptionError("bound V6 custody identity differs")
        if uncomputation.get("status") != "CERTIFIED_INFORMATION_RECOVERABLE":
            raise FoundationConsumptionError("bound V6 uncomputation status differs")

        direct = distribution.source_entropy
        orientation_innovation = distribution.observable_entropy(orientation)
        realization_innovation = distribution.conditional_source_entropy(orientation)
        if direct != orientation_innovation + realization_innovation:
            raise FoundationConsumptionError("bound V6 custody chain law differs")
        hierarchical_support = (
            self.hd_module.FormalLogElement.from_positive_rational(2)
            + realization_innovation
        )
        support_overhead = hierarchical_support - direct

        formal_cls = self.native_module.FormalLogMonoidElement
        hidden = formal_cls.from_positive_rational(
            multiplicity, source_provenance="Q3_BOUND_V6_HIDDEN_INFORMATION"
        )
        retained = formal_cls.from_positive_rational(
            multiplicity, source_provenance="Q3_BOUND_V6_RETAINED_INFORMATION"
        )
        erased = formal_cls.from_positive_rational(
            1, source_provenance="Q3_BOUND_V6_ZERO_LOGICAL_ERASURE"
        )
        source_seal = self.native_module.NativeSourceSeal(
            role="Q3_BOUND_CANONICAL_CUSTODY_SOURCE",
            revision=self.binding.custody_release,
            repository_relative_path=self.binding.native_module_archive_path,
            sha256=self.binding.native_module_sha256,
        )
        annotation_seed = {
            "best_orientation_multiplicity": best,
            "other_orientation_multiplicity": other,
            "source_module_sha256": self.binding.native_module_sha256,
        }
        annotation = self.native_module.CustodyAnnotation(
            annotation_id=canonical_sha256(annotation_seed),
            source_operation_id="Q3_PHYSICAL_GROUP_RECEIPT_PARTITION_V1",
            input_space="Q3FrozenPhysicalGroupMember",
            visible_fiber_cardinality=multiplicity,
            generated_receipt_channels=("ORIENTATION_RECEIPT", "REALIZATION_RECEIPT"),
            retained_receipt_channels=("ORIENTATION_RECEIPT", "REALIZATION_RECEIPT"),
            reconstructible=True,
            hidden_information=hidden,
            retained_information=retained,
            logical_erasure=erased,
            logical_erasure_status="NO_ERASURE_RECEIPTS_RETAINED",
            probability_model_provenance="Q3_FROZEN_PHYSICAL_GROUP_UNIFORM_MEMBER_LAW",
            source_seal=source_seal,
        )
        annotation_row = annotation.to_dict()
        _strict_roundtrip(self.native_module.CustodyAnnotation, annotation_row, "custody annotation")
        body = {
            "schema": BOUND_CUSTODY_SCHEMA,
            "best_orientation_multiplicity": best,
            "other_orientation_multiplicity": other,
            "direct_multiplicity": multiplicity,
            "partitions": {
                "visible": visible.to_dict(),
                "orientation": orientation.to_dict(),
                "realization": realization.to_dict(),
            },
            "receipt_sufficiency": sufficiency.to_dict(),
            "information_identity": identity,
            "uncomputation_plan": uncomputation,
            "formal_logs": {
                "direct_information": direct.to_dict(),
                "orientation_innovation": orientation_innovation.to_dict(),
                "realization_innovation": realization_innovation.to_dict(),
                "hierarchical_support": hierarchical_support.to_dict(),
                "support_overhead": support_overhead.to_dict(),
            },
            "custody_annotation": annotation_row,
            "chain_law": "DIRECT=ORIENTATION_INNOVATION+REALIZATION_INNOVATION",
            "chain_law_exact": True,
            "composition_depth": 2,
            "source_module_sha256": self.binding.native_module_sha256,
        }
        return {**body, "semantic_sha256": canonical_sha256(body)}


__all__ = (
    "BOUND_CUSTODY_SCHEMA",
    "BOUND_HD_SCHEMA",
    "BoundV6Foundation",
    "FoundationConsumptionError",
    "SNAPSHOT_METADATA_SCHEMA",
    "UNDEFINED_QUOTIENT_SCHEMA",
)
