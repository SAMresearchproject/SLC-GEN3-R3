#!/usr/bin/env python3
"""Frozen, source-visible inference runtime for current SLCQ3-RZ.

This module consumes only the sanitized current-local selected-model receipt
and the sealed Q3 feature/foundation implementation.  It never deserializes
the primary result and never opens training catalogs, target ledgers, fitting
code, primary-result content, or CONTROL material.  Its primary raw and
semantic identities arrive only through the sanitized model and terminal
release receipts created during promotion.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, NoReturn, Sequence


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CANDIDATE_ROOT = (
    ROOT
    / "SLC/18_SAM_NATIVE_QC/"
    "SLCV33_RZ_NATIVE_EXACT_INFORMATION_ALGEBRA_CANDIDATE_Q3"
)
Q2_ROOT = ROOT / "SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q2"
Q1_ROOT = ROOT / "SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q1"

FROZEN_MODEL_PATH = HERE / "release/FROZEN_SLCQ3_RZ_MODEL.json"
FEATURE_SCHEMA_PATH = CANDIDATE_ROOT / "Q3_NATIVE_FEATURE_SCHEMA.json"
FOUNDATION_BINDING_PATH = CANDIDATE_ROOT / "preexecution/SEALED_ICF1_BINDING.json"
WINNER_LOCK_PATH = CANDIDATE_ROOT / "work/HOLDOUT_WINNER_LOCK.json"
RELEASE_MANIFEST_PATH = CANDIDATE_ROOT / "release/RELEASE_MANIFEST.json"
FINAL_FREEZE_PATH = CANDIDATE_ROOT / "release/FINAL_FREEZE_RECEIPT.json"
INDEPENDENT_VALIDATION_PATH = CANDIDATE_ROOT / "release/INDEPENDENT_VALIDATION.json"
Q2_PACKAGE_INIT = Q2_ROOT / "slcv32_rz_q2/__init__.py"
Q2_ENGINE_PATH = Q2_ROOT / "slcv32_rz_q2/engine.py"
Q1_RUNTIME_FILES = {
    "slcv32_rz/__init__.py": "2865b8c1fb5d1b3a506638004d6833c20442276edddfc2d8310bcfc7d378addc",
    "slcv32_rz/canonical.py": "331b2593f6fd3ad7b33979de3b914b5ed07fb7ca803c456dd144cae892878a2a",
    "slcv32_rz/selectors.py": "0d9b5dcc960531ec4e56a5ecac7cdb54d20ba2b6c11cc0cb2cd9f78053c30a5e",
    "slcv32_rz/source_quality.py": "8c9fc2d72c6176aea5cbee3a7975e2bc551a611986ea654c7acf79886f6eea7a",
}

EXPECTED_CANDIDATE = "SLCV33_RZ_NATIVE_EXACT_INFORMATION_ALGEBRA_CANDIDATE_Q3"
EXPECTED_SELECTOR_ID = "Q3-R3_GRAPH-HYBRID-LISTWISE-ADJACENT-RIDGE-1D10"
EXPECTED_REPRESENTATION = "R3_GRAPH"
EXPECTED_PARAMETER_COUNT = 200
EXPECTED_MODEL_SEMANTIC_SHA256 = (
    "f43c6da7fe3ee7f25579d5ec4da414c37b9177ecfc51fbbd729445da200877f9"
)
EXPECTED_SELECTION_SEMANTIC_SHA256 = (
    "10292593863429c76d60279ee3086d9687731c1e9725a25ed89a8b2ed3acb159"
)
EXPECTED_FEATURE_ORDER_SEMANTIC_SHA256 = (
    "29e2ed6b27021abb8968d8a669058be2543b445d8216d6f68bacb50953708497"
)
EXPECTED_FEATURE_SCHEMA_FILE_SHA256 = (
    "58060e889c9731e0758ffacf51279b997382a1f2de2d6a2cd12d651506c696c2"
)
EXPECTED_FEATURE_SCHEMA_SEMANTIC_SHA256 = (
    "e93b58bf0df84000e5a8ebabf653e8c5bebdd743d0905b4461f60e8c2bc65917"
)
EXPECTED_FOUNDATION_BINDING_FILE_SHA256 = (
    "1827674276d2972651eb0c2463f158ca714aed10182ab6aa5c24d941926f7880"
)
EXPECTED_FOUNDATION_IMPORT_SEMANTIC_SHA256 = (
    "6e703f3eb00033b38d83afca843ed2a83ceb031f1b138a4e66fa89c904eaca25"
)
EXPECTED_FOUNDATION_SOURCE_SEMANTIC_SHA256 = (
    "b1e53f9ec38421b0cdfbd365354504564a63b4d6e9c746ca4b94671279120db5"
)
EXPECTED_FOUNDATION_SNAPSHOT_SHA256 = (
    "aa266d0f7f7dee219afbebdf83b051d0e52947189952f429b0ec2925409b98b8"
)
EXPECTED_PRIMARY_RESULT_FILE_SHA256 = (
    "9da5262def0753e8d1cb54944e131d39e25022e627f9f578386bb4d40739d499"
)
EXPECTED_PRIMARY_RESULT_SEMANTIC_SHA256 = (
    "9db1659c1424268c1049414a216d7b088dfb0a45a045c7e615ed68c1f591890f"
)
EXPECTED_WINNER_LOCK_FILE_SHA256 = (
    "c7e25205f2aad964aebd6b61c1a98dd568fc90a32abe818eaf4e6be18cddc83a"
)
EXPECTED_WINNER_LOCK_SEMANTIC_SHA256 = (
    "a19fbb6aa1ddb1d0288a309ea30aee882fde328a467408a9f187d0330682ff44"
)
EXPECTED_RELEASE_MANIFEST_FILE_SHA256 = (
    "26f730f9d0abbd1a10c61973acd448f443576c186bac00d186df2c421a168594"
)
EXPECTED_RELEASE_MANIFEST_SEMANTIC_SHA256 = (
    "3966fcd3cb7c49e71ebc50e77094edb13c9e957f236fca6e2d1711cfac45ca34"
)
EXPECTED_FINAL_FREEZE_FILE_SHA256 = (
    "035f91832d50aeb963df972fbb6ecd84db34171acc17fdd0372c7233b37e777a"
)
EXPECTED_FINAL_FREEZE_SEMANTIC_SHA256 = (
    "7822a6152186b03d03bec68936478eabd9f00b6eb25c0cfb4777b1a961e78d73"
)
EXPECTED_INDEPENDENT_VALIDATION_FILE_SHA256 = (
    "6033a6aabbcf056164552a1e5485980143a411fc18b7893d13dc49a616523a19"
)
EXPECTED_INDEPENDENT_VALIDATION_SEMANTIC_SHA256 = (
    "db381d43af40a0bc57317178e47ed06163c8327ee6ac35538efa7cd45abac9f5"
)
EXPECTED_Q2_PACKAGE_INIT_SHA256 = (
    "28e316be98723b176782f96d34d96825885cacb03139d5aabed8e52ea6db81c8"
)
EXPECTED_Q2_ENGINE_SHA256 = (
    "c901d6a330b75f0d06f6925a2d3dcf8642b85b4e4b2e3a04e92369ab4e352703"
)

_RUNTIME_HELPER_PATHS = (
    "slcv33_rz_q3/__init__.py",
    "slcv33_rz_q3/binding.py",
    "slcv33_rz_q3/canonical.py",
    "slcv33_rz_q3/custody.py",
    "slcv33_rz_q3/features.py",
    "slcv33_rz_q3/foundation.py",
    "slcv33_rz_q3/geometry.py",
    "slcv33_rz_q3/graph.py",
    "slcv33_rz_q3/hd.py",
    "slcv33_rz_q3/source.py",
)


class SLCQ3RZError(RuntimeError):
    """The sealed Q3 runtime, model, foundation, or request differs."""


def _fail(message: str) -> NoReturn:
    raise SLCQ3RZError(message)


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    try:
        with Path(path).open("rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
    except OSError as exc:
        raise SLCQ3RZError(f"required frozen artifact cannot be read: {path}") from exc
    return digest.hexdigest()


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_float(value: str) -> NoReturn:
    _fail(f"binary floating-point JSON value is barred: {value}")


def _load_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_reject_float,
            parse_constant=_reject_float,
        )
    except SLCQ3RZError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SLCQ3RZError(f"invalid frozen JSON artifact: {path}") from exc


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(f"{label} is not a JSON object")
    return value


def _semantic_object(value: Any, label: str, expected: str) -> Mapping[str, Any]:
    row = _mapping(value, label)
    body = dict(row)
    observed = body.pop("semantic_sha256", None)
    if observed != expected or _canonical_sha256(body) != observed:
        _fail(f"{label} semantic identity differs")
    return row


def _fraction(value: Any, label: str) -> Fraction:
    outer = _mapping(value, label)
    if set(outer) != {"__fraction__"}:
        _fail(f"{label} is not a canonical exact fraction")
    inner = _mapping(outer["__fraction__"], f"{label} payload")
    if set(inner) != {"denominator", "numerator"}:
        _fail(f"{label} exact-fraction fields differ")
    numerator_text = inner["numerator"]
    denominator_text = inner["denominator"]
    if not isinstance(numerator_text, str) or not isinstance(denominator_text, str):
        _fail(f"{label} exact-fraction coordinates are not strings")
    try:
        result = Fraction(int(numerator_text), int(denominator_text))
    except (ValueError, ZeroDivisionError) as exc:
        raise SLCQ3RZError(f"{label} exact fraction is invalid") from exc
    if (
        numerator_text != str(result.numerator)
        or denominator_text != str(result.denominator)
    ):
        _fail(f"{label} exact fraction is not normalized")
    return result


def _sha_text(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        _fail(f"{label} is not lowercase hexadecimal SHA-256")
    return value


def _verify_runtime_helpers() -> Mapping[str, Any]:
    if file_sha256(RELEASE_MANIFEST_PATH) != EXPECTED_RELEASE_MANIFEST_FILE_SHA256:
        _fail("sealed Q3 release-manifest bytes differ")
    manifest = _semantic_object(
        _load_strict_json(RELEASE_MANIFEST_PATH),
        "sealed Q3 release manifest",
        EXPECTED_RELEASE_MANIFEST_SEMANTIC_SHA256,
    )
    if (
        manifest.get("schema") != "SLCV33_RZ_Q3_RELEASE_MANIFEST_V1"
        or manifest.get("status") != "SEALED_UNINSTALLED_Q3_CANDIDATE"
        or manifest.get("candidate") != EXPECTED_CANDIDATE
    ):
        _fail("sealed Q3 release-manifest boundary differs")
    raw_rows = manifest.get("artifacts")
    if not isinstance(raw_rows, list):
        _fail("sealed Q3 release-manifest inventory differs")
    rows: dict[str, Mapping[str, Any]] = {}
    for raw in raw_rows:
        row = _mapping(raw, "release-manifest artifact")
        path = row.get("path")
        if not isinstance(path, str) or path in rows:
            _fail("sealed Q3 release-manifest path differs or repeats")
        rows[path] = row
    for relative in _RUNTIME_HELPER_PATHS:
        row = rows.get(relative)
        if row is None:
            _fail(f"runtime helper is absent from the sealed manifest: {relative}")
        path = CANDIDATE_ROOT / relative
        if (
            isinstance(row.get("bytes"), bool)
            or not isinstance(row.get("bytes"), int)
            or row["bytes"] != path.stat().st_size
            or _sha_text(row.get("sha256"), f"{relative} manifest hash")
            != file_sha256(path)
        ):
            _fail(f"sealed runtime helper bytes differ: {relative}")
    if file_sha256(Q2_PACKAGE_INIT) != EXPECTED_Q2_PACKAGE_INIT_SHA256:
        _fail("frozen Q2 compatibility package bytes differ")
    if file_sha256(Q2_ENGINE_PATH) != EXPECTED_Q2_ENGINE_SHA256:
        _fail("frozen Q2 compatibility engine bytes differ")
    for relative, expected in Q1_RUNTIME_FILES.items():
        if file_sha256(Q1_ROOT / relative) != expected:
            _fail(f"frozen Q1 compatibility helper bytes differ: {relative}")
    return manifest


# Verify every module that can execute during the candidate imports before the
# package is placed on sys.path.
_verify_runtime_helpers()
if str(CANDIDATE_ROOT) not in sys.path:
    sys.path.insert(0, str(CANDIDATE_ROOT))

from slcv33_rz_q3.binding import (  # noqa: E402
    FoundationBinding,
    require_sealed_icf1_binding,
)
from slcv33_rz_q3.canonical import canonical_sha256 as _exact_semantic_sha256  # noqa: E402
from slcv33_rz_q3.features import (  # noqa: E402
    FEATURE_SCHEMAS,
    FeatureReceipt,
    Representation,
    derive_representation as _derive_representation,
)
from slcv33_rz_q3.foundation import BoundV6Foundation  # noqa: E402
from slcv33_rz_q3.source import (  # noqa: E402
    CANONICAL_ROLE,
    REPLICATE_ROLE,
    Q3Group,
    SourceRecord,
    SourceVisibleChoice,
    physical_group_key,
    q3_group_id,
)


EXPECTED_SOURCE_VISIBLE_FIELDS = tuple(SourceVisibleChoice.__dataclass_fields__)


@dataclass(frozen=True, slots=True)
class CandidateGroupInput:
    """A target-blind concrete realization roster for one candidate fiber."""

    visible_records: tuple[SourceVisibleChoice, ...]

    def __post_init__(self) -> None:
        self._validated_roster()

    def _validated_roster(
        self,
    ) -> tuple[
        tuple[SourceVisibleChoice, ...],
        tuple[Any, ...],
        Counter[SourceVisibleChoice],
    ]:
        records = self.visible_records
        if not isinstance(records, tuple) or not records:
            _fail("candidate-group visible roster must be a nonempty tuple")
        if any(not isinstance(record, SourceVisibleChoice) for record in records):
            _fail("candidate-group roster contains a non-source-visible record")
        keys = {physical_group_key(record) for record in records}
        if len(keys) != 1:
            _fail("candidate-group roster crosses physical fibers")
        orientations = Counter(records)
        if len(orientations) != 2:
            _fail("candidate-group roster must contain exactly two visible orientations")
        first, second = tuple(orientations)
        if (
            first.axis != second.axis
            or first.modulus != second.modulus
            or first.route_domain != second.route_domain
            or first.physical_relation_domain != second.physical_relation_domain
            or first.left_shell != second.right_shell
            or first.right_shell != second.left_shell
            or first.left_direction != second.right_direction
            or first.right_direction != second.left_direction
        ):
            _fail("candidate-group orientations are not an exact reciprocal swap")
        count_pair = tuple(sorted(orientations.values()))
        if count_pair not in {(2, 2), (2, 8), (8, 8)}:
            _fail("candidate-group orientation multiplicities are outside the frozen Q3 roster")
        key = next(iter(keys))
        return records, key, orientations

    def _to_internal_q3_group(self) -> Q3Group:
        records, key, _orientations = self._validated_roster()
        token = q3_group_id(key)
        seen: set[SourceVisibleChoice] = set()
        source_records: list[SourceRecord] = []
        for index, visible in enumerate(records):
            role = CANONICAL_ROLE if visible not in seen else REPLICATE_ROLE
            seen.add(visible)
            source_records.append(
                SourceRecord(
                    receipt_index=index,
                    sample_role=role,
                    old_q2_group_id=token,
                    old_q2_split="RUNTIME_INFERENCE",
                    visible=visible,
                )
            )
        return Q3Group(
            q3_group_id=token,
            old_q2_group_id=token,
            old_q2_split="RUNTIME_INFERENCE",
            q3_split="RUNTIME_INFERENCE",
            physical_key=key,
            records=tuple(source_records),
        )


@dataclass(frozen=True, slots=True)
class FrozenSLCQ3RZModel:
    selector_id: str
    representation: str
    regularization: Fraction
    parameters: tuple[Fraction, ...]
    adjacent_weight: int
    statistics_semantic_sha256: str
    feature_order: tuple[str, ...]
    model_semantic_sha256: str
    selection_semantic_sha256: str
    foundation_import_semantic_sha256: str
    receipt_semantic_sha256: str


@dataclass(frozen=True, slots=True)
class RankOutcome:
    status: str
    ordered_candidate_indices: tuple[int, ...]
    top_candidate_indices: tuple[int, ...]
    scores: tuple[tuple[Fraction, ...], ...]


def _verify_terminal_source_seal(local: Mapping[str, Any]) -> FoundationBinding:
    manifest = _verify_runtime_helpers()
    if local.get("primary_result_file_sha256") != EXPECTED_PRIMARY_RESULT_FILE_SHA256:
        _fail("sanitized model primary-result raw binding differs")
    if local.get("primary_result_semantic_sha256") != EXPECTED_PRIMARY_RESULT_SEMANTIC_SHA256:
        _fail("sanitized model primary-result semantic binding differs")
    if local.get("feature_schema_file_sha256") != EXPECTED_FEATURE_SCHEMA_FILE_SHA256:
        _fail("sanitized model feature-schema raw binding differs")
    if local.get("feature_schema_semantic_sha256") != EXPECTED_FEATURE_SCHEMA_SEMANTIC_SHA256:
        _fail("sanitized model feature-schema semantic binding differs")
    if file_sha256(FEATURE_SCHEMA_PATH) != EXPECTED_FEATURE_SCHEMA_FILE_SHA256:
        _fail("sealed Q3 feature-schema bytes differ")
    schema = _semantic_object(
        _load_strict_json(FEATURE_SCHEMA_PATH),
        "sealed Q3 feature schema",
        EXPECTED_FEATURE_SCHEMA_SEMANTIC_SHA256,
    )
    graph_schema = _mapping(
        _mapping(schema.get("representations"), "feature representations").get("R3_GRAPH"),
        "R3_GRAPH feature schema",
    )
    if (
        schema.get("schema") != "SLCV33_RZ_Q3_NATIVE_FEATURE_SCHEMA_V1"
        or schema.get("status") != "FROZEN_PRE_PRIMARY"
        or schema.get("source_visible_fields") != list(EXPECTED_SOURCE_VISIBLE_FIELDS)
        or graph_schema.get("width") != EXPECTED_PARAMETER_COUNT
        or graph_schema.get("feature_names_semantic_sha256")
        != EXPECTED_FEATURE_ORDER_SEMANTIC_SHA256
    ):
        _fail("sealed Q3 R3_GRAPH feature schema differs")

    expected_pairs = (
        (
            "winner_lock_file_sha256",
            EXPECTED_WINNER_LOCK_FILE_SHA256,
            WINNER_LOCK_PATH,
        ),
        (
            "release_manifest_file_sha256",
            EXPECTED_RELEASE_MANIFEST_FILE_SHA256,
            RELEASE_MANIFEST_PATH,
        ),
        (
            "final_freeze_receipt_file_sha256",
            EXPECTED_FINAL_FREEZE_FILE_SHA256,
            FINAL_FREEZE_PATH,
        ),
        (
            "independent_validation_file_sha256",
            EXPECTED_INDEPENDENT_VALIDATION_FILE_SHA256,
            INDEPENDENT_VALIDATION_PATH,
        ),
    )
    for field, expected, path in expected_pairs:
        if local.get(field) != expected or file_sha256(path) != expected:
            _fail(f"sanitized model terminal raw binding differs: {field}")

    winner = _semantic_object(
        _load_strict_json(WINNER_LOCK_PATH),
        "sealed Q3 winner lock",
        EXPECTED_WINNER_LOCK_SEMANTIC_SHA256,
    )
    freeze = _semantic_object(
        _load_strict_json(FINAL_FREEZE_PATH),
        "sealed Q3 final freeze",
        EXPECTED_FINAL_FREEZE_SEMANTIC_SHA256,
    )
    independent = _semantic_object(
        _load_strict_json(INDEPENDENT_VALIDATION_PATH),
        "sealed Q3 independent validation",
        EXPECTED_INDEPENDENT_VALIDATION_SEMANTIC_SHA256,
    )
    semantic_pairs = (
        ("winner_lock_semantic_sha256", EXPECTED_WINNER_LOCK_SEMANTIC_SHA256),
        ("release_manifest_semantic_sha256", EXPECTED_RELEASE_MANIFEST_SEMANTIC_SHA256),
        ("final_freeze_receipt_semantic_sha256", EXPECTED_FINAL_FREEZE_SEMANTIC_SHA256),
        (
            "independent_validation_semantic_sha256",
            EXPECTED_INDEPENDENT_VALIDATION_SEMANTIC_SHA256,
        ),
    )
    for field, expected in semantic_pairs:
        if local.get(field) != expected:
            _fail(f"sanitized model terminal semantic binding differs: {field}")

    if (
        winner.get("schema") != "SLCV33_RZ_Q3_HOLDOUT_WINNER_LOCK_V1"
        or winner.get("status") != "SEALED_HOLDOUT_WINNER_LOCK"
        or winner.get("selected_selector_id") != EXPECTED_SELECTOR_ID
        or winner.get("selected_model_semantic_sha256")
        != EXPECTED_MODEL_SEMANTIC_SHA256
        or winner.get("selection_receipt_semantic_sha256")
        != EXPECTED_SELECTION_SEMANTIC_SHA256
        or winner.get("foundation_binding_file_sha256")
        != EXPECTED_FOUNDATION_BINDING_FILE_SHA256
    ):
        _fail("sealed Q3 winner-lock identity differs")
    if (
        freeze.get("schema") != "SLCV33_RZ_Q3_FINAL_FREEZE_RECEIPT_V1"
        or freeze.get("status") != "FROZEN_COMPLETE_UNINSTALLED_Q3"
        or freeze.get("winner_selector_id") != EXPECTED_SELECTOR_ID
        or freeze.get("primary_result_file_sha256")
        != EXPECTED_PRIMARY_RESULT_FILE_SHA256
        or freeze.get("release_manifest_file_sha256")
        != EXPECTED_RELEASE_MANIFEST_FILE_SHA256
        or freeze.get("release_manifest_semantic_sha256")
        != EXPECTED_RELEASE_MANIFEST_SEMANTIC_SHA256
        or freeze.get("foundation_binding_file_sha256")
        != EXPECTED_FOUNDATION_BINDING_FILE_SHA256
    ):
        _fail("sealed Q3 final-freeze identity differs")
    if (
        independent.get("schema") != "SLCV33_RZ_Q3_INDEPENDENT_VALIDATION_V1"
        or independent.get("status") != "PASS"
        or independent.get("assertions_failed") != 0
        or independent.get("selected_representation") != EXPECTED_REPRESENTATION
        or independent.get("selected_selector_id") != EXPECTED_SELECTOR_ID
        or independent.get("primary_result_file_sha256")
        != EXPECTED_PRIMARY_RESULT_FILE_SHA256
        or independent.get("primary_result_semantic_sha256")
        != EXPECTED_PRIMARY_RESULT_SEMANTIC_SHA256
        or independent.get("winner_lock_file_sha256")
        != EXPECTED_WINNER_LOCK_FILE_SHA256
        or independent.get("winner_lock_semantic_sha256")
        != EXPECTED_WINNER_LOCK_SEMANTIC_SHA256
        or independent.get("foundation_binding_file_sha256")
        != EXPECTED_FOUNDATION_BINDING_FILE_SHA256
    ):
        _fail("sealed Q3 independent-validation identity differs")
    if manifest.get("foundation_binding_file_sha256") != EXPECTED_FOUNDATION_BINDING_FILE_SHA256:
        _fail("sealed Q3 manifest foundation binding differs")

    if local.get("foundation_binding_file_sha256") != EXPECTED_FOUNDATION_BINDING_FILE_SHA256:
        _fail("sanitized model foundation raw binding differs")
    if file_sha256(FOUNDATION_BINDING_PATH) != EXPECTED_FOUNDATION_BINDING_FILE_SHA256:
        _fail("sealed Q3 foundation-binding bytes differ")
    binding = require_sealed_icf1_binding(FOUNDATION_BINDING_PATH)
    if (
        binding.binding_file_sha256 != EXPECTED_FOUNDATION_BINDING_FILE_SHA256
        or binding.foundation_release != "SLCV33-ICF1"
        or binding.custody_release != "V6"
        or binding.snapshot_sha256 != EXPECTED_FOUNDATION_SNAPSHOT_SHA256
        or binding.active_source_semantic_sha256
        != EXPECTED_FOUNDATION_SOURCE_SEMANTIC_SHA256
    ):
        _fail("sealed Q3 bound V6/ICF1 identity differs")
    return binding


def _validate_model(model: FrozenSLCQ3RZModel) -> None:
    if (
        model.selector_id != EXPECTED_SELECTOR_ID
        or model.representation != EXPECTED_REPRESENTATION
        or model.regularization != Fraction(1, 10)
        or model.adjacent_weight != 4
        or len(model.parameters) != EXPECTED_PARAMETER_COUNT
        or len(model.feature_order) != EXPECTED_PARAMETER_COUNT
        or model.feature_order != tuple(FEATURE_SCHEMAS[Representation.R3_GRAPH])
        or _exact_semantic_sha256(model.feature_order)
        != EXPECTED_FEATURE_ORDER_SEMANTIC_SHA256
        or model.model_semantic_sha256 != EXPECTED_MODEL_SEMANTIC_SHA256
        or model.selection_semantic_sha256 != EXPECTED_SELECTION_SEMANTIC_SHA256
        or model.foundation_import_semantic_sha256
        != EXPECTED_FOUNDATION_IMPORT_SEMANTIC_SHA256
    ):
        _fail("frozen SLCQ3-RZ model identity differs")
    identity = {
        "selector_id": model.selector_id,
        "representation": model.representation,
        "regularization": model.regularization,
        "parameters": model.parameters,
        "adjacent_weight": model.adjacent_weight,
        "statistics_semantic_sha256": model.statistics_semantic_sha256,
    }
    if _exact_semantic_sha256(identity) != model.model_semantic_sha256:
        _fail("frozen SLCQ3-RZ exact model semantic receipt differs")


def load_frozen_model() -> FrozenSLCQ3RZModel:
    """Load only the sanitized selected model and verify its sealed provenance."""

    local_raw = _load_strict_json(FROZEN_MODEL_PATH)
    local = _semantic_object(
        local_raw,
        "sanitized current SLCQ3-RZ model",
        _sha_text(
            _mapping(local_raw, "sanitized model").get("semantic_sha256"),
            "sanitized model semantic hash",
        ),
    )
    if (
        local.get("schema") != "SLCQ3_RZ_FROZEN_MODEL_V1"
        or local.get("status") != "FROZEN_SELECTED_INFERENCE_MODEL"
        or local.get("candidate") != EXPECTED_CANDIDATE
        or local.get("selector_id") != EXPECTED_SELECTOR_ID
        or local.get("representation") != EXPECTED_REPRESENTATION
        or local.get("parameter_count") != EXPECTED_PARAMETER_COUNT
        or local.get("model_semantic_sha256") != EXPECTED_MODEL_SEMANTIC_SHA256
        or local.get("selection_semantic_sha256")
        != EXPECTED_SELECTION_SEMANTIC_SHA256
        or local.get("feature_order_semantic_sha256")
        != EXPECTED_FEATURE_ORDER_SEMANTIC_SHA256
        or local.get("foundation_import_semantic_sha256")
        != EXPECTED_FOUNDATION_IMPORT_SEMANTIC_SHA256
    ):
        _fail("sanitized current SLCQ3-RZ model boundary differs")
    raw_parameters = local.get("parameters")
    raw_feature_order = local.get("feature_order")
    if not isinstance(raw_parameters, list) or not isinstance(raw_feature_order, list):
        _fail("sanitized current SLCQ3-RZ model arrays differ")
    if any(not isinstance(name, str) for name in raw_feature_order):
        _fail("sanitized current SLCQ3-RZ feature names differ")
    model = FrozenSLCQ3RZModel(
        selector_id=str(local["selector_id"]),
        representation=str(local["representation"]),
        regularization=_fraction(local.get("regularization"), "regularization"),
        parameters=tuple(
            _fraction(value, f"parameter[{index}]")
            for index, value in enumerate(raw_parameters)
        ),
        adjacent_weight=local.get("adjacent_weight"),
        statistics_semantic_sha256=_sha_text(
            local.get("statistics_semantic_sha256"),
            "training-statistics semantic hash",
        ),
        feature_order=tuple(raw_feature_order),
        model_semantic_sha256=str(local["model_semantic_sha256"]),
        selection_semantic_sha256=str(local["selection_semantic_sha256"]),
        foundation_import_semantic_sha256=str(
            local["foundation_import_semantic_sha256"]
        ),
        receipt_semantic_sha256=str(local["semantic_sha256"]),
    )
    _validate_model(model)
    _verify_terminal_source_seal(local)
    return model


def _coerce_group(value: CandidateGroupInput) -> Q3Group:
    if not isinstance(value, CandidateGroupInput):
        _fail("candidate is not a source-visible SLCQ3-RZ group input")
    group = value._to_internal_q3_group()
    if any(not isinstance(record, SourceRecord) for record in group.records):
        _fail("typed Q3 group contains a foreign record")
    visible = tuple(record.visible for record in group.records)
    if any(not isinstance(record, SourceVisibleChoice) for record in visible):
        _fail("typed Q3 group contains a non-source-visible choice")
    keys = {physical_group_key(record) for record in visible}
    if len(keys) != 1:
        _fail("typed Q3 group crosses physical fibers")
    key = next(iter(keys))
    if group.physical_key != key or group.q3_group_id != q3_group_id(key):
        _fail("typed Q3 group physical identity differs")
    if len(Counter(visible)) != 2:
        _fail("typed Q3 group does not contain exactly two visible orientations")
    return group


class SLCQ3RZRuntime:
    """One bound-V6 inference context, reusable across a complete roster."""

    def __init__(self, model: FrozenSLCQ3RZModel, binding: FoundationBinding) -> None:
        self.model = model
        self.binding = binding
        self._foundation_context: BoundV6Foundation | None = None
        self._foundation: BoundV6Foundation | None = None

    def __enter__(self) -> "SLCQ3RZRuntime":
        if self._foundation is not None:
            _fail("SLCQ3-RZ runtime context cannot be reentered")
        context = BoundV6Foundation(self.binding)
        foundation = context.__enter__()
        if (
            foundation.import_receipt.get("semantic_sha256")
            != self.model.foundation_import_semantic_sha256
        ):
            context.__exit__(None, None, None)
            _fail("bound V6/ICF1 runtime import receipt differs")
        self._foundation_context = context
        self._foundation = foundation
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        context = self._foundation_context
        self._foundation = None
        self._foundation_context = None
        if context is not None:
            context.__exit__(exc_type, exc, traceback)

    def derive_r3_graph(
        self,
        query: SourceVisibleChoice,
        candidate: CandidateGroupInput,
    ) -> FeatureReceipt:
        if self._foundation is None:
            _fail("SLCQ3-RZ runtime is not inside its bound-foundation context")
        if not isinstance(query, SourceVisibleChoice):
            _fail("query is not a source-visible Q3 choice")
        group = _coerce_group(candidate)
        receipt = _derive_representation(
            Representation.R3_GRAPH,
            query,
            group,
            self._foundation,
        )
        if (
            receipt.representation is not Representation.R3_GRAPH
            or receipt.feature_names != self.model.feature_order
            or receipt.source_field_names != EXPECTED_SOURCE_VISIBLE_FIELDS
            or receipt.foundation_import_semantic_sha256
            != self.model.foundation_import_semantic_sha256
            or receipt.custody_audit_passed is not True
            or len(receipt.values) != len(self.model.parameters)
            or any(not isinstance(value, Fraction) for value in receipt.values)
        ):
            _fail("source-visible Q3 feature receipt differs")
        return receipt

    def score(
        self,
        query: SourceVisibleChoice,
        candidate: CandidateGroupInput,
    ) -> tuple[Fraction, ...]:
        receipt = self.derive_r3_graph(query, candidate)
        exact = sum(
            (
                parameter * feature
                for parameter, feature in zip(
                    self.model.parameters,
                    receipt.values,
                    strict=True,
                )
            ),
            Fraction(),
        )
        return (exact,)

    def rank(
        self,
        query: SourceVisibleChoice,
        candidates: Sequence[CandidateGroupInput] | Iterable[CandidateGroupInput],
    ) -> RankOutcome:
        roster = tuple(candidates)
        if not roster:
            _fail("candidate roster is empty")
        scores = tuple(self.score(query, candidate) for candidate in roster)
        ordered = tuple(
            sorted(
                range(len(roster)),
                key=lambda index: (scores[index], -index),
                reverse=True,
            )
        )
        best = scores[ordered[0]]
        top = tuple(index for index in ordered if scores[index] == best)
        return RankOutcome(
            status="SELECTED_UNIQUE" if len(top) == 1 else "AMBIGUOUS_TOP_SCORE",
            ordered_candidate_indices=ordered,
            top_candidate_indices=top,
            scores=scores,
        )


def open_runtime(model: FrozenSLCQ3RZModel | None = None) -> SLCQ3RZRuntime:
    expected = load_frozen_model()
    if model is not None:
        _validate_model(model)
        if model != expected:
            _fail("caller-supplied frozen model differs from current SLCQ3-RZ")
    binding = require_sealed_icf1_binding(FOUNDATION_BINDING_PATH)
    return SLCQ3RZRuntime(expected, binding)


def derive_r3_graph(
    query: SourceVisibleChoice,
    candidate: CandidateGroupInput,
    *,
    model: FrozenSLCQ3RZModel | None = None,
) -> FeatureReceipt:
    with open_runtime(model) as runtime:
        return runtime.derive_r3_graph(query, candidate)


def score(
    query: SourceVisibleChoice,
    candidate: CandidateGroupInput,
    *,
    model: FrozenSLCQ3RZModel | None = None,
) -> tuple[Fraction, ...]:
    with open_runtime(model) as runtime:
        return runtime.score(query, candidate)


def rank(
    query: SourceVisibleChoice,
    candidates: Sequence[CandidateGroupInput] | Iterable[CandidateGroupInput],
    *,
    model: FrozenSLCQ3RZModel | None = None,
) -> RankOutcome:
    with open_runtime(model) as runtime:
        return runtime.rank(query, candidates)


__all__ = (
    "CandidateGroupInput",
    "FrozenSLCQ3RZModel",
    "RankOutcome",
    "SLCQ3RZError",
    "SLCQ3RZRuntime",
    "SourceVisibleChoice",
    "derive_r3_graph",
    "load_frozen_model",
    "open_runtime",
    "rank",
    "score",
)
