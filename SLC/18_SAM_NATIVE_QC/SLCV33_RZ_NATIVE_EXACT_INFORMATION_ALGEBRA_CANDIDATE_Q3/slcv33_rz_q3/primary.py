"""Full contract-gated SLCV33-RZ Q3 primary execution custody."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import gzip
import os
from pathlib import Path
import tempfile
import time
from typing import Any, Callable, Mapping, Sequence

from .binding import DEFAULT_BINDING_PATH, FoundationBinding, require_sealed_icf1_binding
from .canonical import (
    OrderedSemanticDigest,
    canonical_bytes,
    canonical_sha256,
    file_sha256,
    iter_canonical_bytes,
    load_exact_json,
    seal,
    validate_semantic_seal,
)
from .catalogs import Q3CatalogBundle, build_q3_catalog_bundle, evaluate_installed_q2_continuity
from .comparator import load_q2_current_model, score_q2_current
from .evaluation import (
    CompactChangedAccumulator,
    CompactOutcomeStore,
    EvaluationResult,
    PairOutcome,
    StreamingEvaluationAccumulator,
    changed_error_receipt,
    compact_changed_from_store,
    evaluate_complete_catalog,
)
from .features import FEATURE_SCHEMAS, REPRESENTATION_WIDTHS, Representation
from .foundation import BoundV6Foundation
from .source import (
    FEATURE_SOURCE_FIELDS,
    Q3Inventory,
    load_frozen_q2_inventory,
    target_ledger_provenance,
)
from .streaming import (
    Q3SplitQuerySource,
    StreamingCatalogAccumulator,
    StreamingFitResult,
    fit_q3_budget_streaming,
)
from .training import ExactHybridModel, RankRow, fit_q3_budget


LOCK_SCHEMA = "SLCV33_RZ_Q3_HOLDOUT_WINNER_LOCK_V1"
LOCK_STATUS = "SEALED_HOLDOUT_WINNER_LOCK"
CONTROL_TOKEN_SCHEMA = "SLCV33_RZ_Q3_CONTROL_REVEAL_TOKEN_V1"
CONTROL_TOKEN_STATUS = "SEALED_CONTROL_REVEAL_AUTHORIZATION"
PRIMARY_RESULT_SCHEMA = "SLCV33_RZ_Q3_PRIMARY_RESULT_V1"
VALIDATION_BUNDLE_SCHEMA = "SLCV33_RZ_Q3_PRIMARY_COMPACT_VALIDATION_BUNDLE_V2"
ARTIFACT_MANIFEST_SCHEMA = "SLCV33_RZ_Q3_PRIMARY_ARTIFACT_MANIFEST_V1"
FEATURE_SCHEMA_ARTIFACT_SCHEMA = "SLCV33_RZ_Q3_NATIVE_FEATURE_SCHEMA_V1"
STRUCTURED_FLAT_ABLATION_SCHEMA = "SLCV33_RZ_Q3_STRUCTURED_VS_FLAT_ABLATION_V1"
SELECTION_SCHEMA = "SLCV33_RZ_Q3_HOLDOUT_SELECTION_V1"
MODEL_RECEIPT_SCHEMA = "SLCV33_RZ_Q3_EXACT_MODEL_RECEIPT_V1"
EVALUATION_RECEIPT_SCHEMA = "SLCV33_RZ_Q3_EVALUATION_RECEIPT_V1"
SOURCE_RECEIPT_SCHEMA = "SLCV33_RZ_Q3_SOURCE_SPLIT_RECEIPT_V1"
CATALOG_RECEIPT_SCHEMA = "SLCV33_RZ_Q3_CATALOG_RECEIPT_V1"

WORK_DIRNAME = "work"
WINNER_LOCK_FILENAME = "HOLDOUT_WINNER_LOCK.json"
CONTROL_TOKEN_FILENAME = "Q3_CONTROL_REVEAL_TOKEN.json"
PRIMARY_RESULT_FILENAME = "Q3_PRIMARY_RESULT.json"
VALIDATION_BUNDLE_FILENAME = "Q3_PRIMARY_VALIDATION_BUNDLE.json.gz"
ARTIFACT_MANIFEST_FILENAME = "Q3_PRIMARY_ARTIFACT_MANIFEST.json"
FEATURE_SCHEMA_FILENAME = "Q3_NATIVE_FEATURE_SCHEMA.json"
STRUCTURED_FLAT_ABLATION_FILENAME = "Q3_STRUCTURED_VS_FLAT_ABLATION.json"


class PrimaryExecutionError(RuntimeError):
    """The Q3 primary chronology, selection, or write-once custody differs."""


@dataclass(frozen=True, slots=True)
class PrimaryPaths:
    candidate_root: Path
    work_dir: Path
    winner_lock: Path
    control_token: Path
    primary_result: Path
    validation_bundle: Path
    artifact_manifest: Path
    feature_schema: Path
    structured_flat_ablation: Path

    @classmethod
    def under(cls, candidate_root: str | Path) -> "PrimaryPaths":
        root = Path(candidate_root)
        work = root / WORK_DIRNAME
        return cls(
            candidate_root=root,
            work_dir=work,
            winner_lock=work / WINNER_LOCK_FILENAME,
            control_token=work / CONTROL_TOKEN_FILENAME,
            primary_result=work / PRIMARY_RESULT_FILENAME,
            validation_bundle=work / VALIDATION_BUNDLE_FILENAME,
            artifact_manifest=work / ARTIFACT_MANIFEST_FILENAME,
            feature_schema=root / FEATURE_SCHEMA_FILENAME,
            structured_flat_ablation=work / STRUCTURED_FLAT_ABLATION_FILENAME,
        )


@dataclass(frozen=True, slots=True)
class WinnerSelection:
    baseline_selector_id: str
    baseline_model_semantic_sha256: str
    selected_selector_id: str
    selected_model_semantic_sha256: str | None
    selected_representation: str
    disposition: str
    admitted_selector_ids: tuple[str, ...]
    excluded_selector_ids: tuple[str, ...]
    semantic_sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": SELECTION_SCHEMA,
            "baseline_family": "R0_Q2_70_REFIT",
            "baseline_selector_id": self.baseline_selector_id,
            "baseline_model_semantic_sha256": self.baseline_model_semantic_sha256,
            "selected_selector_id": self.selected_selector_id,
            "selected_model_semantic_sha256": self.selected_model_semantic_sha256,
            "selected_representation": self.selected_representation,
            "disposition": self.disposition,
            "admitted_selector_ids": self.admitted_selector_ids,
            "excluded_selector_ids": self.excluded_selector_ids,
            "semantic_sha256": self.semantic_sha256,
        }


def _directory_fsync(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_once_bytes(path: str | Path, payload: bytes) -> str:
    """Atomically install bytes once; identical replay is admitted, drift is barred."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not target.is_file() or target.read_bytes() != payload:
            raise PrimaryExecutionError(f"write-once artifact differs: {target}")
        return "REUSED_IDENTICAL"

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, target)
            disposition = "CREATED"
            _directory_fsync(target.parent)
        except FileExistsError:
            if not target.is_file() or target.read_bytes() != payload:
                raise PrimaryExecutionError(f"write-once artifact raced with differing bytes: {target}")
            disposition = "REUSED_IDENTICAL"
    finally:
        temporary.unlink(missing_ok=True)
    return disposition


def write_once_exact_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    if not validate_semantic_seal(payload):
        raise PrimaryExecutionError("write-once JSON payload has no valid semantic seal")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            for block in iter_canonical_bytes(payload):
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
        return _install_staged_file_once(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def _install_staged_file_once(temporary: Path, target: Path) -> str:
    """Install one staged file without loading either side into memory."""

    if target.exists():
        if (
            not target.is_file()
            or target.stat().st_size != temporary.stat().st_size
            or file_sha256(target) != file_sha256(temporary)
        ):
            raise PrimaryExecutionError(f"write-once staged artifact differs: {target}")
        return "REUSED_IDENTICAL"
    try:
        os.link(temporary, target)
        _directory_fsync(target.parent)
        return "CREATED"
    except FileExistsError:
        if (
            not target.is_file()
            or target.stat().st_size != temporary.stat().st_size
            or file_sha256(target) != file_sha256(temporary)
        ):
            raise PrimaryExecutionError(
                f"write-once staged artifact raced with differing bytes: {target}"
            )
        return "REUSED_IDENTICAL"


def write_once_gzip_exact_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    """Stream one sealed canonical JSON object into deterministic gzip custody."""

    if not validate_semantic_seal(payload):
        raise PrimaryExecutionError("write-once gzip payload has no valid semantic seal")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as raw:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                compresslevel=9,
                fileobj=raw,
                mtime=0,
            ) as compressed:
                for block in iter_canonical_bytes(payload):
                    compressed.write(block)
            raw.flush()
            os.fsync(raw.fileno())
        return _install_staged_file_once(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def load_sealed_json(
    path: str | Path,
    *,
    schema: str,
    status: str | None = None,
) -> Mapping[str, Any]:
    target = Path(path)
    if not target.is_file():
        raise PrimaryExecutionError(f"required sealed artifact is absent: {target}")
    value = load_exact_json(target)
    if not isinstance(value, Mapping) or value.get("schema") != schema:
        raise PrimaryExecutionError(f"sealed artifact schema differs: {target}")
    if status is not None and value.get("status") != status:
        raise PrimaryExecutionError(f"sealed artifact status differs: {target}")
    if not validate_semantic_seal(value):
        raise PrimaryExecutionError(f"sealed artifact semantic hash differs: {target}")
    return value


def load_native_feature_schema(path: str | Path) -> Mapping[str, Any]:
    """Require the candidate-owned schema artifact to equal runtime schemas."""

    value = load_sealed_json(path, schema=FEATURE_SCHEMA_ARTIFACT_SCHEMA, status="FROZEN_PRE_PRIMARY")
    if tuple(value.get("source_visible_fields", ())) != FEATURE_SOURCE_FIELDS:
        raise PrimaryExecutionError("native feature-schema source field roster differs")
    representations = value.get("representations")
    if not isinstance(representations, Mapping) or set(representations) != {
        representation.value for representation in Representation
    }:
        raise PrimaryExecutionError("native feature-schema representation roster differs")
    for representation in Representation:
        row = representations[representation.value]
        if not isinstance(row, Mapping):
            raise PrimaryExecutionError("native feature-schema row is not an object")
        if row.get("width") != REPRESENTATION_WIDTHS[representation]:
            raise PrimaryExecutionError(f"{representation.value} schema width artifact differs")
        if row.get("feature_names_semantic_sha256") != canonical_sha256(
            FEATURE_SCHEMAS[representation]
        ):
            raise PrimaryExecutionError(f"{representation.value} feature-name seal differs")
        if "feature_names" in row and tuple(row["feature_names"]) != FEATURE_SCHEMAS[representation]:
            raise PrimaryExecutionError(f"{representation.value} expanded feature-name artifact differs")
    return value


def _model_record(model: ExactHybridModel) -> dict[str, object]:
    return {
        "selector_id": model.selector_id,
        "representation": model.representation,
        "regularization": model.regularization,
        "adjacent_weight": model.adjacent_weight,
        "parameters": model.parameters,
        "parameter_count": len(model.parameters),
        "statistics_semantic_sha256": model.statistics_semantic_sha256,
        "semantic_sha256": model.semantic_sha256,
    }


def _compact_evaluation(result: EvaluationResult) -> dict[str, object]:
    full = result.to_dict()
    outcomes = full.pop("pair_outcomes", None)
    full.update(
        {
            "feature_collision_weight": result.representation_collision_weight,
            "feature_collision_rate": result.representation_collision_rate,
            "pair_outcome_count": result.pair_outcome_count,
            "pair_outcomes_semantic_sha256": (
                result.pair_outcomes_semantic_sha256
                if outcomes is None
                else canonical_sha256(outcomes)
            ),
            "semantic_sha256": result.semantic_sha256,
        }
    )
    return full


def _full_evaluation(result: EvaluationResult) -> dict[str, object]:
    body = result.to_dict()
    body.update(
        {
            "feature_collision_weight": result.representation_collision_weight,
            "feature_collision_rate": result.representation_collision_rate,
            "semantic_sha256": result.semantic_sha256,
        }
    )
    return body


def _compact_changed(receipt: Mapping[str, Any]) -> dict[str, object]:
    categories = ("fixed", "introduced", "unchanged_error", "changed_correct")
    return {
        "baseline_selector_id": receipt["baseline_selector_id"],
        "candidate_selector_id": receipt["candidate_selector_id"],
        "baseline_error_count": receipt["baseline_error_count"],
        "candidate_error_count": receipt["candidate_error_count"],
        "net_error_reduction": receipt["net_error_reduction"],
        "category_counts": {name: len(receipt[name]) for name in categories},
        "category_semantic_sha256s": {
            name: canonical_sha256(receipt[name]) for name in categories
        },
        "fixed": receipt["fixed"],
        "introduced": receipt["introduced"],
        "changed_correct": receipt["changed_correct"],
        "semantic_sha256": receipt["semantic_sha256"],
    }


def _selection_key(model: ExactHybridModel, result: EvaluationResult) -> tuple[object, ...]:
    return (
        result.error_count,
        -result.strict_pair_correct,
        result.score_tie_weight,
        result.representation_collision_weight,
        model.selector_id,
    )


def select_holdout_winner(
    models: Sequence[ExactHybridModel],
    holdout_evaluations: Mapping[str, EvaluationResult],
) -> WinnerSelection:
    """Apply the frozen exact-best-set/error/tie-break selection rule."""

    model_by_id = {model.selector_id: model for model in models}
    if len(model_by_id) != 15 or set(model_by_id) != set(holdout_evaluations):
        raise PrimaryExecutionError("HOLDOUT selection requires exactly the 15 fitted model evaluations")
    admitted = tuple(
        model
        for model in models
        if holdout_evaluations[model.selector_id].exact_best_set_recovery == Fraction(1)
    )
    excluded = tuple(model for model in models if model not in admitted)
    r0_models = tuple(
        model for model in models if model.representation == Representation.R0.value
    )
    r0_admitted = tuple(model for model in admitted if model in r0_models)
    baseline = min(
        r0_admitted or r0_models,
        key=lambda model: _selection_key(model, holdout_evaluations[model.selector_id]),
    )
    baseline_result = holdout_evaluations[baseline.selector_id]
    if admitted:
        best = min(
            admitted,
            key=lambda model: _selection_key(model, holdout_evaluations[model.selector_id]),
        )
        best_result = holdout_evaluations[best.selector_id]
    else:
        best = None
        best_result = None
    if (
        best is not None
        and best.representation != Representation.R0.value
        and best_result is not None
        and best_result.error_count < baseline_result.error_count
    ):
        selected = best
        disposition = "Q3_REPRESENTATION_ADMITTED_STRICT_ERROR_REDUCTION"
    elif r0_admitted:
        selected = baseline
        disposition = "R0_Q2_70_REFIT_RETAINED"
    else:
        selected = None
        disposition = "NO_SELECTION"
    body = {
        "schema": SELECTION_SCHEMA,
        "baseline_family": "R0_Q2_70_REFIT",
        "baseline_selector_id": baseline.selector_id,
        "baseline_model_semantic_sha256": baseline.semantic_sha256,
        "selected_selector_id": selected.selector_id if selected is not None else "NO_SELECTION",
        "selected_model_semantic_sha256": selected.semantic_sha256 if selected is not None else None,
        "selected_representation": selected.representation if selected is not None else "NO_SELECTION",
        "disposition": disposition,
        "admitted_selector_ids": tuple(sorted(model.selector_id for model in admitted)),
        "excluded_selector_ids": tuple(sorted(model.selector_id for model in excluded)),
    }
    return WinnerSelection(
        baseline_selector_id=baseline.selector_id,
        baseline_model_semantic_sha256=baseline.semantic_sha256,
        selected_selector_id=body["selected_selector_id"],
        selected_model_semantic_sha256=body["selected_model_semantic_sha256"],
        selected_representation=body["selected_representation"],
        disposition=disposition,
        admitted_selector_ids=body["admitted_selector_ids"],
        excluded_selector_ids=body["excluded_selector_ids"],
        semantic_sha256=canonical_sha256(body),
    )


def build_source_receipt(
    inventory: Q3Inventory,
    binding: FoundationBinding,
    binding_path: str | Path,
    feature_schema_path: str | Path,
    feature_schema: Mapping[str, Any],
    foundation_import_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    split_counts = {
        split: sum(group.q3_split == split for group in inventory.groups)
        for split in ("TRAIN", "HOLDOUT", "CONTROL")
    }
    body = {
        "schema": SOURCE_RECEIPT_SCHEMA,
        "status": "PASS_FROZEN_Q2_INVENTORY_REUSED_CONTROL_PRESERVED",
        "foundation": {
            "foundation_release": binding.foundation_release,
            "custody_release": binding.custody_release,
            "snapshot_sha256": binding.snapshot_sha256,
            "snapshot_metadata_sha256": binding.snapshot_metadata_sha256,
            "source_semantic_sha256": binding.active_source_semantic_sha256,
            "test_source_semantic_sha256": binding.test_source_semantic_sha256,
            "native_module_archive_path": binding.native_module_archive_path,
            "native_module_sha256": binding.native_module_sha256,
            "binding_file_sha256": file_sha256(binding_path),
            "import_receipt": dict(foundation_import_receipt),
        },
        "source_index_path": str(inventory.source_index_path),
        "source_index_file_sha256": file_sha256(inventory.source_index_path),
        "q2_split_manifest_path": str(inventory.q2_split_manifest_path),
        "q2_split_manifest_file_sha256": file_sha256(inventory.q2_split_manifest_path),
        "physical_group_count": len(inventory.groups),
        "source_receipt_count": len(inventory.records),
        "split_group_counts": split_counts,
        "transition_counts": inventory.transition_counts,
        "multiplicity_counts": {
            str(multiplicity): sum(group.multiplicity == multiplicity for group in inventory.groups)
            for multiplicity in (4, 10, 16)
        },
        "source_visible_field_schema": FEATURE_SOURCE_FIELDS,
        "native_feature_schema": {
            "path": str(Path(feature_schema_path)),
            "file_sha256": file_sha256(feature_schema_path),
            "semantic_sha256": feature_schema["semantic_sha256"],
        },
        "barred_fields_entered_features": (),
        "control_targets_loaded": False,
    }
    return seal(body)


def build_catalog_receipt(bundle: Q3CatalogBundle) -> dict[str, Any]:
    feature_counts = {
        representation.value: len(bundle.feature_receipt_semantic_sha256s[representation])
        for representation in Representation
    }
    body = {
        "schema": CATALOG_RECEIPT_SCHEMA,
        "status": "PASS_EXACT_COMPLETE_CATALOG",
        "split": bundle.split,
        "catalog_semantic_sha256": bundle.semantic_sha256,
        "query_count": bundle.query_count,
        "group_reference_count": bundle.group_reference_count,
        "exact_group_quality_checks": bundle.exact_group_quality_checks,
        "representation_widths": {
            representation.value: REPRESENTATION_WIDTHS[representation]
            for representation in Representation
        },
        "feature_receipt_counts": feature_counts,
        "feature_receipt_roster_semantic_sha256s": {
            representation.value: canonical_sha256(
                bundle.feature_receipt_semantic_sha256s[representation]
            )
            for representation in Representation
        },
        "zero_variance_receipts": {
            representation.value: bundle.zero_variance_receipts[representation]
            for representation in Representation
        },
        "hd_factor_product_quotient_audits": {
            "relation_count_per_row": 3,
            "row_count": feature_counts[Representation.R2.value],
            "status": "PASS_EXACT_OR_CONSTRUCTION_RAISES",
        },
        "custody_chain_uncomputation_audits": {
            "flat_row_count": feature_counts[Representation.R3_FLAT.value],
            "graph_row_count": feature_counts[Representation.R3_GRAPH.value],
            "status": "PASS_EXACT_OR_CONSTRUCTION_RAISES",
        },
        "source_field_firewall": {
            "admitted": FEATURE_SOURCE_FIELDS,
            "status": "PASS_TARGET_HASH_ID_TIMING_EXCLUDED_FROM_FEATURES",
        },
    }
    return seal(body)


def build_model_receipt(models: Sequence[ExactHybridModel]) -> dict[str, Any]:
    if len(models) != 15:
        raise PrimaryExecutionError("model receipt requires exactly 15 fits")
    return seal(
        {
            "schema": MODEL_RECEIPT_SCHEMA,
            "status": "PASS_EXACT_RATIONAL_15_MODEL_BUDGET",
            "objective": "FROZEN_Q2_HYBRID_LISTWISE_PLUS_ADJACENT",
            "models": tuple(_model_record(model) for model in models),
        }
    )


def _evaluate_all_models(
    bundle: Q3CatalogBundle,
    models: Sequence[ExactHybridModel],
) -> tuple[EvaluationResult, dict[str, EvaluationResult]]:
    q2_result = evaluate_installed_q2_continuity(bundle)
    fitted = {
        model.selector_id: evaluate_complete_catalog(
            bundle.complete_rows_by_representation[Representation(model.representation)],
            selector_id=model.selector_id,
            scorer=model.score,
        )
        for model in models
    }
    return q2_result, fitted


def _evaluation_receipt(
    split: str,
    q2_result: EvaluationResult,
    fitted: Mapping[str, EvaluationResult],
) -> dict[str, Any]:
    return seal(
        {
            "schema": EVALUATION_RECEIPT_SCHEMA,
            "status": "PASS_COMPLETE_EXACT_CATALOG_EVALUATION",
            "split": split,
            "q2_current_fixed": _compact_evaluation(q2_result),
            "fitted_models": {
                selector: _compact_evaluation(result)
                for selector, result in sorted(fitted.items())
            },
        }
    )


def _changed_receipts(
    q2_result: EvaluationResult,
    fitted: Mapping[str, EvaluationResult],
    r0_baseline_selector_id: str,
) -> dict[str, Any]:
    baseline = fitted[r0_baseline_selector_id]
    versus_q2 = {
        selector: changed_error_receipt(q2_result, result)
        for selector, result in sorted(fitted.items())
    }
    versus_r0 = {
        selector: changed_error_receipt(baseline, result)
        for selector, result in sorted(fitted.items())
    }
    return {
        "versus_q2_current_fixed": versus_q2,
        "versus_r0_q2_70_refit": versus_r0,
    }


def _compact_changed_roster(roster: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    return {
        family: {
            selector: _compact_changed(receipt)
            for selector, receipt in sorted(receipts.items())
        }
        for family, receipts in roster.items()
    }


def write_holdout_winner_lock(
    path: str | Path,
    *,
    body: Mapping[str, Any],
) -> tuple[Mapping[str, Any], str]:
    required = {
        "foundation_binding_file_sha256",
        "foundation_snapshot_sha256",
        "foundation_semantic_sha256",
        "source_receipt_semantic_sha256",
        "train_catalog_semantic_sha256",
        "holdout_catalog_semantic_sha256",
        "model_receipt_semantic_sha256",
        "holdout_evaluation_receipt_semantic_sha256",
        "selection_receipt_semantic_sha256",
        "baseline_selector_id",
        "selected_selector_id",
        "selected_model_semantic_sha256",
    }
    if not required <= set(body):
        raise PrimaryExecutionError(
            f"HOLDOUT winner lock body lacks fields: {sorted(required - set(body))}"
        )
    payload = seal(
        {
            "schema": LOCK_SCHEMA,
            "status": LOCK_STATUS,
            "control_targets_deserialized_before_lock": False,
            **body,
        }
    )
    return payload, write_once_exact_json(path, payload)


def load_holdout_winner_lock(path: str | Path) -> Mapping[str, Any]:
    return load_sealed_json(path, schema=LOCK_SCHEMA, status=LOCK_STATUS)


def _write_control_token(
    winner_lock_path: str | Path,
    token_path: str | Path,
) -> tuple[Mapping[str, Any], str]:
    lock = load_holdout_winner_lock(winner_lock_path)
    token = seal(
        {
            "schema": CONTROL_TOKEN_SCHEMA,
            "status": CONTROL_TOKEN_STATUS,
            "winner_lock_path": str(Path(winner_lock_path)),
            "winner_lock_file_sha256": file_sha256(winner_lock_path),
            "winner_lock_semantic_sha256": lock["semantic_sha256"],
            "selected_selector_id": lock["selected_selector_id"],
            "selected_model_semantic_sha256": lock["selected_model_semantic_sha256"],
            "chronology": (
                "HOLDOUT_WINNER_LOCK_PERSISTED",
                "CONTROL_REVEAL_TOKEN_PERSISTED",
                "CONTROL_TARGET_LOAD_MAY_BEGIN",
            ),
        }
    )
    return token, write_once_exact_json(token_path, token)


def load_control_catalog_after_lock(
    inventory: Q3Inventory,
    *,
    binding_path: str | Path,
    winner_lock_path: str | Path,
    control_token_path: str | Path,
    chronology_events: list[dict[str, object]] | None = None,
    catalog_builder: Callable[..., Q3CatalogBundle] = build_q3_catalog_bundle,
    foundation: BoundV6Foundation | None = None,
) -> tuple[Q3CatalogBundle, Mapping[str, Any]]:
    """Persist lock-bound reveal authorization before any CONTROL target load."""

    events = chronology_events if chronology_events is not None else []
    lock = load_holdout_winner_lock(winner_lock_path)
    events.append(
        {
            "sequence": len(events) + 1,
            "event": "HOLDOUT_WINNER_LOCK_VERIFIED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    token, disposition = _write_control_token(winner_lock_path, control_token_path)
    if disposition != "CREATED":
        raise PrimaryExecutionError(
            "CONTROL reveal token already exists while no primary result is installed; "
            "repeated CONTROL target access is barred"
        )
    events.append(
        {
            "sequence": len(events) + 1,
            "event": "CONTROL_REVEAL_TOKEN_PERSISTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
            "token_file_sha256": file_sha256(control_token_path),
        }
    )
    events.append(
        {
            "sequence": len(events) + 1,
            "event": "CONTROL_TARGET_LOAD_STARTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    builder_keywords: dict[str, object] = {
        "binding_path": binding_path,
        "control_winner_lock": lock,
    }
    if foundation is not None:
        builder_keywords["foundation"] = foundation
    bundle = catalog_builder(inventory, "CONTROL", **builder_keywords)
    events.append(
        {
            "sequence": len(events) + 1,
            "event": "CONTROL_TARGET_LOAD_COMPLETED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    return bundle, token


def load_control_stream_source_after_lock(
    inventory: Q3Inventory,
    *,
    binding_path: str | Path,
    winner_lock_path: str | Path,
    control_token_path: str | Path,
    chronology_events: list[dict[str, object]],
    foundation: BoundV6Foundation,
    source_builder: Callable[..., Q3SplitQuerySource] = Q3SplitQuerySource,
) -> tuple[Q3SplitQuerySource, Mapping[str, Any]]:
    """Create the query-local CONTROL source only after lock and token persist."""

    lock = load_holdout_winner_lock(winner_lock_path)
    chronology_events.append(
        {
            "sequence": len(chronology_events) + 1,
            "event": "HOLDOUT_WINNER_LOCK_VERIFIED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    token, disposition = _write_control_token(winner_lock_path, control_token_path)
    if disposition != "CREATED":
        raise PrimaryExecutionError(
            "CONTROL reveal token already exists while no primary result is installed; "
            "repeated CONTROL target access is barred"
        )
    chronology_events.append(
        {
            "sequence": len(chronology_events) + 1,
            "event": "CONTROL_REVEAL_TOKEN_PERSISTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
            "token_file_sha256": file_sha256(control_token_path),
        }
    )
    chronology_events.append(
        {
            "sequence": len(chronology_events) + 1,
            "event": "CONTROL_TARGET_LOAD_STARTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    source = source_builder(
        inventory,
        "CONTROL",
        binding_path=binding_path,
        control_winner_lock=lock,
        foundation=foundation,
    )
    chronology_events.append(
        {
            "sequence": len(chronology_events) + 1,
            "event": "CONTROL_TARGET_LOAD_COMPLETED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
        }
    )
    return source, token


def _evaluate_control_locked(
    bundle: Q3CatalogBundle,
    model_by_id: Mapping[str, ExactHybridModel],
    selection: WinnerSelection,
) -> tuple[EvaluationResult, dict[str, EvaluationResult]]:
    q2 = evaluate_installed_q2_continuity(bundle)
    selector_ids = (
        (selection.baseline_selector_id,)
        if selection.disposition == "NO_SELECTION"
        else tuple(sorted({selection.baseline_selector_id, selection.selected_selector_id}))
    )
    fitted = {}
    for selector in selector_ids:
        model = model_by_id[selector]
        fitted[selector] = evaluate_complete_catalog(
            bundle.complete_rows_by_representation[Representation(model.representation)],
            selector_id=model.selector_id,
            scorer=model.score,
        )
    return q2, fitted


def _q2_score_rows(bundle: Q3CatalogBundle) -> tuple[dict[str, object], ...]:
    model = load_q2_current_model()
    return tuple(
        {
            "query_token": query_token,
            "group_token": group_token,
            "score": score_q2_current(query, candidate, model=model),
        }
        for (query_token, group_token), (query, candidate) in sorted(bundle.visible_pairs.items())
    )


def _q2_model_record() -> dict[str, object]:
    model = load_q2_current_model()
    return {
        "selector_id": model.selector_id,
        "architecture": model.architecture,
        "feature_order": model.feature_order,
        "heads": model.heads,
        "semantic_sha256": model.semantic_sha256,
    }


def _validation_rows(
    bundle: Q3CatalogBundle,
    representations: Sequence[Representation],
) -> dict[str, object]:
    return {
        representation.value: bundle.complete_rows_by_representation[representation]
        for representation in representations
    }


def _group_roster(inventory: Q3Inventory) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "q3_group_id": group.q3_group_id,
            "old_q2_group_id": group.old_q2_group_id,
            "old_q2_split": group.old_q2_split,
            "q3_split": group.q3_split,
            "axis": group.axis,
            "physical_key": group.physical_key,
            "multiplicity": group.multiplicity,
            "member_receipt_indices": tuple(record.receipt_index for record in group.records),
        }
        for group in inventory.groups
    )


@dataclass(frozen=True, slots=True)
class StreamingEvaluationPass:
    catalog_receipt: Mapping[str, Any]
    q2_result: EvaluationResult
    fitted_results: Mapping[str, EvaluationResult]
    score_digest_receipts: Mapping[str, Mapping[str, object]]
    outcome_store: CompactOutcomeStore | None
    compact_changed_receipts: Mapping[str, Mapping[str, Mapping[str, object]]] | None


def _outcomes_by_key(
    outcomes: Sequence[PairOutcome],
) -> dict[tuple[str, str, str], PairOutcome]:
    result = {row.key: row for row in outcomes}
    if len(result) != len(outcomes):
        raise PrimaryExecutionError("one query repeats a strict pair")
    return result


def _evaluate_streaming_source(
    source: Q3SplitQuerySource,
    models: Sequence[ExactHybridModel],
    *,
    retain_compact_outcomes: bool,
    changed_baselines: Mapping[str, str] | None = None,
) -> StreamingEvaluationPass:
    """Score one query at a time and retain only compact exact receipts."""

    model_by_id = {model.selector_id: model for model in models}
    if len(model_by_id) != len(models):
        raise PrimaryExecutionError("streaming evaluation model selector IDs repeat")
    q2_model = load_q2_current_model()
    selector_ids = ("Q2_CURRENT_FIXED",) + tuple(sorted(model_by_id))
    accumulators = {
        selector: StreamingEvaluationAccumulator.create(selector)
        for selector in selector_ids
    }
    score_digests = {
        selector: OrderedSemanticDigest.create() for selector in selector_ids
    }
    catalog = StreamingCatalogAccumulator.create(source.split, tuple(Representation))
    outcome_store = (
        CompactOutcomeStore.create(selector_ids) if retain_compact_outcomes else None
    )
    changed_accumulators: dict[
        str, dict[str, CompactChangedAccumulator]
    ] | None = None
    if changed_baselines is not None:
        if any(selector not in selector_ids for selector in changed_baselines.values()):
            raise PrimaryExecutionError("streaming changed-error baseline is not evaluated")
        changed_accumulators = {
            family: {
                selector: CompactChangedAccumulator.create(baseline, selector)
                for selector in selector_ids
                if selector != "Q2_CURRENT_FIXED"
            }
            for family, baseline in changed_baselines.items()
        }

    for query in source.iter_queries(tuple(Representation), accumulator=catalog):
        visible_by_group = {
            group_token: (query_visible, candidate_visible)
            for group_token, query_visible, candidate_visible in query.visible_pairs
        }
        r0_rows = query.complete_rows[Representation.R0]
        q2_scores = {
            row.group_token: score_q2_current(
                visible_by_group[row.group_token][0],
                visible_by_group[row.group_token][1],
                model=q2_model,
            )
            for row in r0_rows
        }
        outcomes_by_selector: dict[str, tuple[PairOutcome, ...]] = {
            "Q2_CURRENT_FIXED": accumulators["Q2_CURRENT_FIXED"].observe_query(
                r0_rows, q2_scores
            )
        }
        for row in r0_rows:
            score_digests["Q2_CURRENT_FIXED"].observe(
                {
                    "query_token": query.query_token,
                    "group_token": row.group_token,
                    "score": q2_scores[row.group_token],
                }
            )
        for selector, model in sorted(model_by_id.items()):
            rows = query.complete_rows[Representation(model.representation)]
            scores = {row.group_token: model.score(row) for row in rows}
            outcomes_by_selector[selector] = accumulators[selector].observe_query(
                rows, scores
            )
            for row in rows:
                score_digests[selector].observe(
                    {
                        "query_token": query.query_token,
                        "group_token": row.group_token,
                        "score": scores[row.group_token],
                    }
                )
        if outcome_store is not None:
            outcome_store.observe_query(outcomes_by_selector)
        if changed_accumulators is not None and changed_baselines is not None:
            keyed = {
                selector: _outcomes_by_key(outcomes)
                for selector, outcomes in outcomes_by_selector.items()
            }
            roster = set(keyed["Q2_CURRENT_FIXED"])
            if any(set(rows) != roster for rows in keyed.values()):
                raise PrimaryExecutionError(
                    "streaming changed-error strict-pair rosters differ"
                )
            for family, baseline_selector in changed_baselines.items():
                baseline_rows = keyed[baseline_selector]
                for selector, accumulator in changed_accumulators[family].items():
                    candidate_rows = keyed[selector]
                    for key in sorted(roster):
                        accumulator.observe(
                            key,
                            baseline_rows[key].outcome,
                            candidate_rows[key].outcome,
                        )

    results = {selector: accumulator.finalize() for selector, accumulator in accumulators.items()}
    q2_result = results.pop("Q2_CURRENT_FIXED")
    compact_changed = None
    if changed_accumulators is not None:
        compact_changed = {
            family: {
                selector: accumulator.finalize(
                    q2_result if accumulator.baseline_selector_id == "Q2_CURRENT_FIXED" else results[
                        accumulator.baseline_selector_id
                    ],
                    results[selector],
                )
                for selector, accumulator in selectors.items()
            }
            for family, selectors in changed_accumulators.items()
        }
    return StreamingEvaluationPass(
        catalog_receipt=catalog.finalize(),
        q2_result=q2_result,
        fitted_results=results,
        score_digest_receipts={
            selector: digest.receipt() for selector, digest in score_digests.items()
        },
        outcome_store=outcome_store,
        compact_changed_receipts=compact_changed,
    )


def _compact_changed_from_holdout_store(
    store: CompactOutcomeStore,
    q2_result: EvaluationResult,
    fitted: Mapping[str, EvaluationResult],
    r0_baseline_selector_id: str,
) -> dict[str, dict[str, Mapping[str, object]]]:
    baseline = fitted[r0_baseline_selector_id]
    return {
        "versus_q2_current_fixed": {
            selector: compact_changed_from_store(store, q2_result, result)
            for selector, result in sorted(fitted.items())
        },
        "versus_r0_q2_70_refit": {
            selector: compact_changed_from_store(store, baseline, result)
            for selector, result in sorted(fitted.items())
        },
    }


def _execution_source_file_hashes(candidate_root: Path) -> dict[str, dict[str, str]]:
    files = tuple(sorted((candidate_root / "slcv33_rz_q3").glob("*.py"))) + tuple(
        sorted((candidate_root / "tests").glob("*.py"))
    ) + (
        candidate_root / "run_q3.py",
        candidate_root / "validate_q3_primary.py",
        candidate_root / "preexecution/NATIVE_EXACT_SUCCESSOR_CONTRACT.json",
        candidate_root / FEATURE_SCHEMA_FILENAME,
    )
    if any(not path.is_file() for path in files):
        missing = tuple(str(path) for path in files if not path.is_file())
        raise PrimaryExecutionError(f"primary execution source file is absent: {missing}")
    return {
        str(path.relative_to(candidate_root)): {
            "path": str(path.relative_to(candidate_root)),
            "file_sha256": file_sha256(path),
        }
        for path in files
    }


def _elapsed_decimal(nanoseconds: int) -> str:
    return f"{nanoseconds // 1_000_000_000}.{nanoseconds % 1_000_000_000:09d}"


def _runtime_receipt(phase_nanoseconds: Mapping[str, int], total_nanoseconds: int) -> dict[str, object]:
    return {
        "clock": "time.perf_counter_ns",
        "phases": {
            phase: {
                "elapsed_nanoseconds": elapsed,
                "elapsed_seconds_decimal": _elapsed_decimal(elapsed),
            }
            for phase, elapsed in phase_nanoseconds.items()
        },
        "total_elapsed_nanoseconds": total_nanoseconds,
        "total_elapsed_seconds_decimal": _elapsed_decimal(total_nanoseconds),
    }


def _semantic_chronology(events: Sequence[Mapping[str, object]]) -> tuple[dict[str, object], ...]:
    """Remove execution-clock coordinates from deterministic validation identity."""

    return tuple(
        {
            key: value
            for key, value in event.items()
            if key != "clock_nanoseconds_runtime_only"
        }
        for event in events
    )


def build_structured_flat_ablation(primary_result: Mapping[str, Any]) -> dict[str, Any]:
    """Derive the frozen R3_GRAPH versus R3_FLAT TRAIN/HOLDOUT comparison."""

    if primary_result.get("schema") != PRIMARY_RESULT_SCHEMA or not validate_semantic_seal(primary_result):
        raise PrimaryExecutionError("structured/flat ablation requires the sealed primary result")
    model_receipt = primary_result.get("model_receipt")
    evaluations = primary_result.get("evaluations")
    if not isinstance(model_receipt, Mapping) or not isinstance(evaluations, Mapping):
        raise PrimaryExecutionError("primary result lacks model or evaluation receipts")
    models = model_receipt.get("models")
    if not isinstance(models, (list, tuple)):
        raise PrimaryExecutionError("primary model receipt roster differs")
    by_representation: dict[str, dict[Fraction, Mapping[str, Any]]] = {
        Representation.R3_FLAT.value: {},
        Representation.R3_GRAPH.value: {},
    }
    for row in models:
        if not isinstance(row, Mapping) or row.get("representation") not in by_representation:
            continue
        ridge = row.get("regularization")
        if not isinstance(ridge, Fraction):
            raise PrimaryExecutionError("in-memory primary ridge identity is not exact Fraction")
        by_representation[str(row["representation"])][ridge] = row
    if any(len(rows) != 3 for rows in by_representation.values()):
        raise PrimaryExecutionError("structured/flat ablation lacks three ridges per representation")

    comparison_rows = []
    for ridge in sorted(by_representation[Representation.R3_FLAT.value]):
        flat_model = by_representation[Representation.R3_FLAT.value][ridge]
        graph_model = by_representation[Representation.R3_GRAPH.value].get(ridge)
        if graph_model is None:
            raise PrimaryExecutionError("structured/flat ridge rosters differ")
        split_rows: dict[str, object] = {}
        for split in ("TRAIN", "HOLDOUT"):
            split_receipt = evaluations.get(split)
            if not isinstance(split_receipt, Mapping):
                raise PrimaryExecutionError(f"primary result lacks {split} evaluation receipt")
            fitted = split_receipt.get("fitted_models")
            if not isinstance(fitted, Mapping):
                raise PrimaryExecutionError(f"{split} fitted evaluation roster differs")
            flat = fitted[str(flat_model["selector_id"])]
            graph = fitted[str(graph_model["selector_id"])]
            split_rows[split] = {
                "flat_selector_id": flat_model["selector_id"],
                "graph_selector_id": graph_model["selector_id"],
                "flat_exact_best_set_recovery": flat["exact_best_set_recovery"],
                "graph_exact_best_set_recovery": graph["exact_best_set_recovery"],
                "flat_error_count": flat["error_count"],
                "graph_error_count": graph["error_count"],
                "graph_minus_flat_error_count": graph["error_count"] - flat["error_count"],
                "flat_strict_pair_correct": flat["strict_pair_counts"]["correct"],
                "graph_strict_pair_correct": graph["strict_pair_counts"]["correct"],
                "graph_minus_flat_strict_pair_correct": (
                    graph["strict_pair_counts"]["correct"]
                    - flat["strict_pair_counts"]["correct"]
                ),
                "flat_score_tie_weight": flat["score_tie_weight"],
                "graph_score_tie_weight": graph["score_tie_weight"],
                "graph_minus_flat_score_tie_weight": (
                    graph["score_tie_weight"] - flat["score_tie_weight"]
                ),
                "flat_representation_collision_weight": flat["representation_collision_weight"],
                "graph_representation_collision_weight": graph["representation_collision_weight"],
                "graph_minus_flat_representation_collision_weight": (
                    graph["representation_collision_weight"]
                    - flat["representation_collision_weight"]
                ),
                "flat_evaluation_semantic_sha256": flat["semantic_sha256"],
                "graph_evaluation_semantic_sha256": graph["semantic_sha256"],
            }
        comparison_rows.append({"regularization": ridge, "splits": split_rows})
    control_receipt = evaluations.get("CONTROL")
    control_selectors = ()
    if isinstance(control_receipt, Mapping) and isinstance(control_receipt.get("fitted_models"), Mapping):
        control_selectors = tuple(sorted(control_receipt["fitted_models"]))
    return seal(
        {
            "schema": STRUCTURED_FLAT_ABLATION_SCHEMA,
            "status": "PASS_DERIVED_FROM_PRIMARY_TRAIN_HOLDOUT",
            "primary_result_semantic_sha256": primary_result["semantic_sha256"],
            "comparison_rows": tuple(comparison_rows),
            "selection": primary_result["selection"],
            "control_scope": {
                "evaluated_fitted_selector_ids": control_selectors,
                "rule": "CONTROL_CONTAINS_ONLY_LOCKED_WINNER_AND_R0_REFIT_BASELINE_NOT_A_POST_REVEAL_ABLATION",
            },
        }
    )


def _run_primary_pipeline_with_foundation(
    candidate_root: str | Path,
    *,
    binding_path: str | Path,
    foundation_consumer: BoundV6Foundation,
) -> Mapping[str, Any]:
    """Execute Q3 once after a valid binding and preserve all frozen boundaries."""

    paths = PrimaryPaths.under(candidate_root)
    binding = require_sealed_icf1_binding(binding_path)
    binding_file_hash = file_sha256(binding_path)
    feature_schema_artifact = load_native_feature_schema(paths.feature_schema)
    execution_source_file_hashes = _execution_source_file_hashes(paths.candidate_root)
    if paths.primary_result.is_file():
        existing = load_sealed_json(paths.primary_result, schema=PRIMARY_RESULT_SCHEMA)
        foundation = existing.get("foundation")
        if not isinstance(foundation, Mapping) or foundation.get("binding_file_sha256") != binding_file_hash:
            raise PrimaryExecutionError("existing primary result is bound to a different foundation manifest")
        return {
            "schema": "SLCV33_RZ_Q3_PRIMARY_RUN_RECEIPT_V1",
            "status": "PASS_EXISTING_PRIMARY_RESULT_REUSED_NO_TARGET_ACCESS",
            "primary_result_path": str(paths.primary_result),
            "primary_result_file_sha256": file_sha256(paths.primary_result),
            "primary_result_semantic_sha256": existing["semantic_sha256"],
            "control_targets_loaded_this_execution": False,
        }

    started = time.perf_counter_ns()
    phase_nanoseconds: dict[str, int] = {}

    def timed(label: str, function: Callable[[], Any]) -> Any:
        phase_started = time.perf_counter_ns()
        value = function()
        phase_nanoseconds[label] = time.perf_counter_ns() - phase_started
        return value

    inventory = timed("inventory_load", load_frozen_q2_inventory)
    source_receipt = build_source_receipt(
        inventory,
        binding,
        binding_path,
        paths.feature_schema,
        feature_schema_artifact,
        foundation_consumer.import_receipt,
    )
    train = timed(
        "train_catalog",
        lambda: build_q3_catalog_bundle(
            inventory,
            "TRAIN",
            binding_path=binding_path,
            foundation=foundation_consumer,
        ),
    )
    holdout = timed(
        "holdout_catalog",
        lambda: build_q3_catalog_bundle(
            inventory,
            "HOLDOUT",
            binding_path=binding_path,
            foundation=foundation_consumer,
        ),
    )
    train_catalog_receipt = build_catalog_receipt(train)
    holdout_catalog_receipt = build_catalog_receipt(holdout)
    models = timed(
        "fit_15_exact_models",
        lambda: fit_q3_budget(train.rows_by_representation, binding_path=binding_path),
    )
    model_by_id = {model.selector_id: model for model in models}
    model_receipt = build_model_receipt(models)
    train_q2, train_fitted = timed(
        "train_evaluation_16_selectors",
        lambda: _evaluate_all_models(train, models),
    )
    holdout_q2, holdout_fitted = timed(
        "holdout_evaluation_16_selectors",
        lambda: _evaluate_all_models(holdout, models),
    )
    train_evaluation_receipt = _evaluation_receipt("TRAIN", train_q2, train_fitted)
    holdout_evaluation_receipt = _evaluation_receipt("HOLDOUT", holdout_q2, holdout_fitted)
    selection = select_holdout_winner(models, holdout_fitted)
    train_changed = _changed_receipts(
        train_q2, train_fitted, selection.baseline_selector_id
    )
    holdout_changed = _changed_receipts(
        holdout_q2, holdout_fitted, selection.baseline_selector_id
    )

    lock_body = {
        "foundation_binding_file_sha256": binding_file_hash,
        "foundation_snapshot_sha256": binding.snapshot_sha256,
        "foundation_semantic_sha256": binding.semantic_sha256,
        "source_receipt_semantic_sha256": source_receipt["semantic_sha256"],
        "train_catalog_semantic_sha256": train.semantic_sha256,
        "holdout_catalog_semantic_sha256": holdout.semantic_sha256,
        "model_receipt_semantic_sha256": model_receipt["semantic_sha256"],
        "holdout_evaluation_receipt_semantic_sha256": holdout_evaluation_receipt["semantic_sha256"],
        "selection_receipt_semantic_sha256": selection.semantic_sha256,
        "baseline_selector_id": selection.baseline_selector_id,
        "selected_selector_id": selection.selected_selector_id,
        "selected_model_semantic_sha256": selection.selected_model_semantic_sha256,
        "selected_representation": selection.selected_representation,
        "selection_disposition": selection.disposition,
    }
    lock_started = time.perf_counter_ns()
    winner_lock, lock_disposition = write_holdout_winner_lock(paths.winner_lock, body=lock_body)
    phase_nanoseconds["holdout_winner_lock"] = time.perf_counter_ns() - lock_started

    chronology_events: list[dict[str, object]] = [
        {
            "sequence": 1,
            "event": "HOLDOUT_WINNER_LOCK_PERSISTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
            "write_disposition": lock_disposition,
            "winner_lock_file_sha256": file_sha256(paths.winner_lock),
        }
    ]
    control_started = time.perf_counter_ns()
    control, control_token = load_control_catalog_after_lock(
        inventory,
        binding_path=binding_path,
        winner_lock_path=paths.winner_lock,
        control_token_path=paths.control_token,
        chronology_events=chronology_events,
        foundation=foundation_consumer,
    )
    phase_nanoseconds["control_catalog_after_lock"] = time.perf_counter_ns() - control_started
    control_catalog_receipt = build_catalog_receipt(control)
    control_q2, control_fitted = timed(
        "control_locked_evaluation",
        lambda: _evaluate_control_locked(control, model_by_id, selection),
    )
    control_evaluation_receipt = _evaluation_receipt("CONTROL", control_q2, control_fitted)
    control_changed = _changed_receipts(
        control_q2, control_fitted, selection.baseline_selector_id
    )

    if selection.disposition == "NO_SELECTION":
        winner_holdout_changed: object = "NO_SELECTION"
        winner_control_changed: object = "NO_SELECTION"
        control_representations = (Representation.R0,)
    else:
        winner_holdout_changed = {
            family: receipts[selection.selected_selector_id]
            for family, receipts in holdout_changed.items()
        }
        winner_control_changed = {
            family: receipts[selection.selected_selector_id]
            for family, receipts in control_changed.items()
        }
        control_representations = tuple(
            sorted(
                {
                    Representation.R0,
                    Representation(selection.selected_representation),
                },
                key=lambda value: value.value,
            )
        )
    validation_bundle = seal(
        {
            "schema": VALIDATION_BUNDLE_SCHEMA,
            "status": "PASS_COMPLETE_SOURCE_INDEPENDENT_RECOMPUTATION_PAYLOAD",
            "foundation": source_receipt["foundation"],
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "execution_source_file_sha256s": execution_source_file_hashes,
            "source_visible_field_schema": FEATURE_SOURCE_FIELDS,
            "feature_schemas": {
                representation.value: FEATURE_SCHEMAS[representation]
                for representation in Representation
            },
            "representation_widths": {
                representation.value: REPRESENTATION_WIDTHS[representation]
                for representation in Representation
            },
            "split_group_multiplicity_roster": _group_roster(inventory),
            "source_receipt": source_receipt,
            "catalog_receipts": {
                "TRAIN": train_catalog_receipt,
                "HOLDOUT": holdout_catalog_receipt,
                "CONTROL": control_catalog_receipt,
            },
            "exact_q3_models": model_receipt,
            "q2_current_fixed_model": _q2_model_record(),
            "holdout_complete_rank_rows": _validation_rows(holdout, tuple(Representation)),
            "control_complete_rank_rows": _validation_rows(control, control_representations),
            "holdout_q2_current_exact_score_rows": _q2_score_rows(holdout),
            "control_q2_current_exact_score_rows": _q2_score_rows(control),
            "holdout_evaluations_full": {
                "Q2_CURRENT_FIXED": _full_evaluation(holdout_q2),
                **{
                    selector: _full_evaluation(result)
                    for selector, result in sorted(holdout_fitted.items())
                },
            },
            "control_evaluations_full": {
                "Q2_CURRENT_FIXED": _full_evaluation(control_q2),
                **{
                    selector: _full_evaluation(result)
                    for selector, result in sorted(control_fitted.items())
                },
            },
            "holdout_changed_error_receipts_for_locked_winner": winner_holdout_changed,
            "control_changed_error_receipts_for_locked_winner": winner_control_changed,
            "selection": selection.to_dict(),
            "chronology": {
                "winner_lock": winner_lock,
                "control_reveal_token": control_token,
                "events": _semantic_chronology(chronology_events),
                "status": "PASS_LOCK_PERSISTED_BEFORE_CONTROL_TARGET_LOAD",
            },
        }
    )
    bundle_started = time.perf_counter_ns()
    validation_bytes = gzip.compress(canonical_bytes(validation_bundle), compresslevel=9, mtime=0)
    bundle_disposition = write_once_bytes(paths.validation_bundle, validation_bytes)
    validation_bundle_file_hash = file_sha256(paths.validation_bundle)
    phase_nanoseconds["validation_bundle_build_and_write"] = time.perf_counter_ns() - bundle_started

    total_before_result = time.perf_counter_ns() - started
    primary_result = seal(
        {
            "schema": PRIMARY_RESULT_SCHEMA,
            "status": "PASS_Q3_PRIMARY_COMPLETE_UNINSTALLED",
            "automatic_promotion": False,
            "foundation": source_receipt["foundation"],
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "source_receipt": source_receipt,
            "catalog_receipts": {
                "TRAIN": train_catalog_receipt,
                "HOLDOUT": holdout_catalog_receipt,
                "CONTROL": control_catalog_receipt,
            },
            "model_receipt": model_receipt,
            "selection": selection.to_dict(),
            "evaluations": {
                "TRAIN": train_evaluation_receipt,
                "HOLDOUT": holdout_evaluation_receipt,
                "CONTROL": control_evaluation_receipt,
            },
            "changed_error_receipts": {
                "TRAIN": _compact_changed_roster(train_changed),
                "HOLDOUT": _compact_changed_roster(holdout_changed),
                "CONTROL": _compact_changed_roster(control_changed),
            },
            "chronology": {
                "events": chronology_events,
                "winner_lock_file_sha256": file_sha256(paths.winner_lock),
                "winner_lock_semantic_sha256": winner_lock["semantic_sha256"],
                "control_reveal_token_file_sha256": file_sha256(paths.control_token),
                "control_reveal_token_semantic_sha256": control_token["semantic_sha256"],
                "status": "PASS_LOCK_PERSISTED_BEFORE_SINGLE_CONTROL_REVEAL",
            },
            "validation_bundle": {
                "path": str(paths.validation_bundle),
                "schema": VALIDATION_BUNDLE_SCHEMA,
                "compression": "gzip_mtime_0_level_9",
                "file_sha256": validation_bundle_file_hash,
                "semantic_sha256": validation_bundle["semantic_sha256"],
                "write_disposition": bundle_disposition,
            },
            "counts": {
                "physical_groups": len(inventory.groups),
                "source_receipts": len(inventory.records),
                "fitted_models": len(models),
                "train_selectors_evaluated": 1 + len(train_fitted),
                "holdout_selectors_evaluated": 1 + len(holdout_fitted),
                "control_selectors_evaluated": 1 + len(control_fitted),
                "control_target_loads_this_execution": 1,
            },
            "runtime": _runtime_receipt(phase_nanoseconds, total_before_result),
            "preserved_boundaries": (
                "NO_PROMOTION",
                "NO_CURRENT_POINTER_OR_LIVE_HISTORY_CHANGE",
                "NO_Q2_Q1_SLCV21R_OR_EXACT_WRITE_MUTATION",
                "NO_CONTROL_BEFORE_HOLDOUT_WINNER_LOCK",
                "NO_DOWNSTREAM_EXECUTION",
            ),
        }
    )
    result_disposition = write_once_exact_json(paths.primary_result, primary_result)
    structured_flat_ablation = build_structured_flat_ablation(primary_result)
    ablation_disposition = write_once_exact_json(
        paths.structured_flat_ablation,
        structured_flat_ablation,
    )

    manifest = seal(
        {
            "schema": ARTIFACT_MANIFEST_SCHEMA,
            "status": "PASS_WRITE_ONCE_PRIMARY_ARTIFACT_CUSTODY",
            "execution_source_file_sha256s": execution_source_file_hashes,
            "foundation_binding": {
                "path": str(Path(binding_path)),
                "file_sha256": binding_file_hash,
                "snapshot_sha256": binding.snapshot_sha256,
                "semantic_sha256": binding.semantic_sha256,
                "snapshot_metadata_sha256": binding.snapshot_metadata_sha256,
                "native_module_archive_path": binding.native_module_archive_path,
                "native_module_sha256": binding.native_module_sha256,
                "import_receipt_semantic_sha256": foundation_consumer.import_receipt[
                    "semantic_sha256"
                ],
            },
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "embedded_semantic_artifacts": {
                "source_receipt": source_receipt["semantic_sha256"],
                "train_catalog": train.semantic_sha256,
                "holdout_catalog": holdout.semantic_sha256,
                "control_catalog": control.semantic_sha256,
                "model_receipt": model_receipt["semantic_sha256"],
                "train_evaluation_receipt": train_evaluation_receipt["semantic_sha256"],
                "holdout_evaluation_receipt": holdout_evaluation_receipt["semantic_sha256"],
                "control_evaluation_receipt": control_evaluation_receipt["semantic_sha256"],
                "selection": selection.semantic_sha256,
            },
            "artifacts": {
                FEATURE_SCHEMA_FILENAME: {
                    "path": FEATURE_SCHEMA_FILENAME,
                    "file_sha256": file_sha256(paths.feature_schema),
                    "semantic_sha256": feature_schema_artifact["semantic_sha256"],
                },
                WINNER_LOCK_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{WINNER_LOCK_FILENAME}",
                    "file_sha256": file_sha256(paths.winner_lock),
                    "semantic_sha256": winner_lock["semantic_sha256"],
                },
                CONTROL_TOKEN_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{CONTROL_TOKEN_FILENAME}",
                    "file_sha256": file_sha256(paths.control_token),
                    "semantic_sha256": control_token["semantic_sha256"],
                },
                VALIDATION_BUNDLE_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{VALIDATION_BUNDLE_FILENAME}",
                    "file_sha256": validation_bundle_file_hash,
                    "semantic_sha256": validation_bundle["semantic_sha256"],
                },
                PRIMARY_RESULT_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{PRIMARY_RESULT_FILENAME}",
                    "file_sha256": file_sha256(paths.primary_result),
                    "semantic_sha256": primary_result["semantic_sha256"],
                },
                STRUCTURED_FLAT_ABLATION_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{STRUCTURED_FLAT_ABLATION_FILENAME}",
                    "file_sha256": file_sha256(paths.structured_flat_ablation),
                    "semantic_sha256": structured_flat_ablation["semantic_sha256"],
                },
            },
        }
    )
    manifest_disposition = write_once_exact_json(paths.artifact_manifest, manifest)
    return {
        "schema": "SLCV33_RZ_Q3_PRIMARY_RUN_RECEIPT_V1",
        "status": "PASS_Q3_PRIMARY_COMPLETE_UNINSTALLED",
        "selected_selector_id": selection.selected_selector_id,
        "selected_representation": selection.selected_representation,
        "primary_result_path": str(paths.primary_result),
        "primary_result_file_sha256": file_sha256(paths.primary_result),
        "primary_result_semantic_sha256": primary_result["semantic_sha256"],
        "validation_bundle_path": str(paths.validation_bundle),
        "validation_bundle_file_sha256": validation_bundle_file_hash,
        "artifact_manifest_path": str(paths.artifact_manifest),
        "artifact_manifest_file_sha256": file_sha256(paths.artifact_manifest),
        "write_dispositions": {
            "winner_lock": lock_disposition,
            "validation_bundle": bundle_disposition,
            "primary_result": result_disposition,
            "structured_flat_ablation": ablation_disposition,
            "artifact_manifest": manifest_disposition,
        },
        "control_targets_loaded_this_execution": True,
        "automatic_promotion": False,
    }


def _run_streaming_primary_pipeline_with_foundation(
    candidate_root: str | Path,
    *,
    binding_path: str | Path,
    foundation_consumer: BoundV6Foundation,
) -> Mapping[str, Any]:
    """Execute the primary with query-local rows and compact exact evidence."""

    paths = PrimaryPaths.under(candidate_root)
    binding = require_sealed_icf1_binding(binding_path)
    binding_file_hash = file_sha256(binding_path)
    feature_schema_artifact = load_native_feature_schema(paths.feature_schema)
    execution_source_file_hashes = _execution_source_file_hashes(paths.candidate_root)
    if paths.primary_result.is_file():
        existing = load_sealed_json(paths.primary_result, schema=PRIMARY_RESULT_SCHEMA)
        foundation = existing.get("foundation")
        if (
            not isinstance(foundation, Mapping)
            or foundation.get("binding_file_sha256") != binding_file_hash
        ):
            raise PrimaryExecutionError(
                "existing primary result is bound to a different foundation manifest"
            )
        return {
            "schema": "SLCV33_RZ_Q3_PRIMARY_RUN_RECEIPT_V1",
            "status": "PASS_EXISTING_PRIMARY_RESULT_REUSED_NO_TARGET_ACCESS",
            "primary_result_path": str(paths.primary_result),
            "primary_result_file_sha256": file_sha256(paths.primary_result),
            "primary_result_semantic_sha256": existing["semantic_sha256"],
            "control_targets_loaded_this_execution": False,
        }

    started = time.perf_counter_ns()
    phase_nanoseconds: dict[str, int] = {}

    def timed(label: str, function: Callable[[], Any]) -> Any:
        phase_started = time.perf_counter_ns()
        value = function()
        phase_nanoseconds[label] = time.perf_counter_ns() - phase_started
        return value

    inventory = timed("inventory_load", load_frozen_q2_inventory)
    source_receipt = build_source_receipt(
        inventory,
        binding,
        binding_path,
        paths.feature_schema,
        feature_schema_artifact,
        foundation_consumer.import_receipt,
    )
    train_source = timed(
        "train_source_target_load",
        lambda: Q3SplitQuerySource(
            inventory,
            "TRAIN",
            binding_path=binding_path,
            foundation=foundation_consumer,
        ),
    )
    fit_result: StreamingFitResult = timed(
        "fit_15_exact_models_query_local",
        lambda: fit_q3_budget_streaming(train_source),
    )
    models = fit_result.models
    model_by_id = {model.selector_id: model for model in models}
    model_receipt = build_model_receipt(models)

    holdout_source = timed(
        "holdout_source_target_load",
        lambda: Q3SplitQuerySource(
            inventory,
            "HOLDOUT",
            binding_path=binding_path,
            foundation=foundation_consumer,
        ),
    )
    holdout_pass = timed(
        "holdout_query_local_evaluation_16_selectors",
        lambda: _evaluate_streaming_source(
            holdout_source,
            models,
            retain_compact_outcomes=True,
        ),
    )
    if holdout_pass.outcome_store is None:
        raise PrimaryExecutionError("HOLDOUT compact outcome store is absent")
    holdout_evaluation_receipt = _evaluation_receipt(
        "HOLDOUT", holdout_pass.q2_result, holdout_pass.fitted_results
    )
    selection = select_holdout_winner(models, holdout_pass.fitted_results)
    holdout_changed = _compact_changed_from_holdout_store(
        holdout_pass.outcome_store,
        holdout_pass.q2_result,
        holdout_pass.fitted_results,
        selection.baseline_selector_id,
    )

    lock_body = {
        "foundation_binding_file_sha256": binding_file_hash,
        "foundation_snapshot_sha256": binding.snapshot_sha256,
        "foundation_semantic_sha256": binding.semantic_sha256,
        "source_receipt_semantic_sha256": source_receipt["semantic_sha256"],
        "train_catalog_semantic_sha256": fit_result.catalog_receipt["semantic_sha256"],
        "holdout_catalog_semantic_sha256": holdout_pass.catalog_receipt["semantic_sha256"],
        "model_receipt_semantic_sha256": model_receipt["semantic_sha256"],
        "holdout_evaluation_receipt_semantic_sha256": holdout_evaluation_receipt[
            "semantic_sha256"
        ],
        "selection_receipt_semantic_sha256": selection.semantic_sha256,
        "baseline_selector_id": selection.baseline_selector_id,
        "selected_selector_id": selection.selected_selector_id,
        "selected_model_semantic_sha256": selection.selected_model_semantic_sha256,
        "selected_representation": selection.selected_representation,
        "selection_disposition": selection.disposition,
    }
    lock_started = time.perf_counter_ns()
    winner_lock, lock_disposition = write_holdout_winner_lock(
        paths.winner_lock, body=lock_body
    )
    phase_nanoseconds["holdout_winner_lock"] = time.perf_counter_ns() - lock_started
    chronology_events: list[dict[str, object]] = [
        {
            "sequence": 1,
            "event": "HOLDOUT_WINNER_LOCK_PERSISTED",
            "clock_nanoseconds_runtime_only": time.perf_counter_ns(),
            "write_disposition": lock_disposition,
            "winner_lock_file_sha256": file_sha256(paths.winner_lock),
        }
    ]

    changed_baselines = {
        "versus_q2_current_fixed": "Q2_CURRENT_FIXED",
        "versus_r0_q2_70_refit": selection.baseline_selector_id,
    }
    train_pass = timed(
        "train_query_local_evaluation_16_selectors",
        lambda: _evaluate_streaming_source(
            train_source,
            models,
            retain_compact_outcomes=False,
            changed_baselines=changed_baselines,
        ),
    )
    if train_pass.catalog_receipt != fit_result.catalog_receipt:
        raise PrimaryExecutionError(
            "TRAIN fit and evaluation catalog digests are not byte-identical"
        )
    if train_pass.compact_changed_receipts is None:
        raise PrimaryExecutionError("TRAIN compact changed-error receipts are absent")
    train_evaluation_receipt = _evaluation_receipt(
        "TRAIN", train_pass.q2_result, train_pass.fitted_results
    )

    control_selector_ids = (
        (selection.baseline_selector_id,)
        if selection.disposition == "NO_SELECTION"
        else tuple(
            sorted({selection.baseline_selector_id, selection.selected_selector_id})
        )
    )
    control_models = tuple(model_by_id[selector] for selector in control_selector_ids)
    control_source_started = time.perf_counter_ns()
    control_source, control_token = load_control_stream_source_after_lock(
        inventory,
        binding_path=binding_path,
        winner_lock_path=paths.winner_lock,
        control_token_path=paths.control_token,
        chronology_events=chronology_events,
        foundation=foundation_consumer,
    )
    phase_nanoseconds["control_source_after_lock"] = (
        time.perf_counter_ns() - control_source_started
    )
    control_pass = timed(
        "control_query_local_locked_evaluation",
        lambda: _evaluate_streaming_source(
            control_source,
            control_models,
            retain_compact_outcomes=False,
            changed_baselines=changed_baselines,
        ),
    )
    if control_pass.compact_changed_receipts is None:
        raise PrimaryExecutionError("CONTROL compact changed-error receipts are absent")
    control_evaluation_receipt = _evaluation_receipt(
        "CONTROL", control_pass.q2_result, control_pass.fitted_results
    )

    if selection.disposition == "NO_SELECTION":
        winner_holdout_changed: object = "NO_SELECTION"
        winner_control_changed: object = "NO_SELECTION"
    else:
        winner_holdout_changed = {
            family: receipts[selection.selected_selector_id]
            for family, receipts in holdout_changed.items()
        }
        winner_control_changed = {
            family: receipts[selection.selected_selector_id]
            for family, receipts in control_pass.compact_changed_receipts.items()
        }

    target_ledger = target_ledger_provenance()
    validation_bundle = seal(
        {
            "schema": VALIDATION_BUNDLE_SCHEMA,
            "status": "PASS_COMPACT_SOURCE_INDEPENDENT_RECOMPUTATION_PAYLOAD",
            "foundation": source_receipt["foundation"],
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "execution_source_file_sha256s": execution_source_file_hashes,
            "source_visible_field_schema": FEATURE_SOURCE_FIELDS,
            "feature_schemas": {
                representation.value: FEATURE_SCHEMAS[representation]
                for representation in Representation
            },
            "representation_widths": {
                representation.value: REPRESENTATION_WIDTHS[representation]
                for representation in Representation
            },
            "split_group_multiplicity_roster": _group_roster(inventory),
            "frozen_reconstruction_sources": {
                "source_index": {
                    "path": str(inventory.source_index_path),
                    "file_sha256": file_sha256(inventory.source_index_path),
                },
                "q2_split_manifest": {
                    "path": str(inventory.q2_split_manifest_path),
                    "file_sha256": file_sha256(inventory.q2_split_manifest_path),
                },
                "target_ledger": target_ledger,
            },
            "source_receipt": source_receipt,
            "catalog_receipts": {
                "TRAIN": fit_result.catalog_receipt,
                "HOLDOUT": holdout_pass.catalog_receipt,
                "CONTROL": control_pass.catalog_receipt,
            },
            "training_statistics_receipts": fit_result.statistics_receipts,
            "exact_q3_models": model_receipt,
            "q2_current_fixed_model": _q2_model_record(),
            "evaluation_receipts": {
                "TRAIN": train_evaluation_receipt,
                "HOLDOUT": holdout_evaluation_receipt,
                "CONTROL": control_evaluation_receipt,
            },
            "ordered_score_digest_receipts": {
                "TRAIN": train_pass.score_digest_receipts,
                "HOLDOUT": holdout_pass.score_digest_receipts,
                "CONTROL": control_pass.score_digest_receipts,
            },
            "holdout_compact_outcome_roster": holdout_pass.outcome_store.roster_receipt(),
            "compact_changed_error_receipts": {
                "TRAIN": train_pass.compact_changed_receipts,
                "HOLDOUT": holdout_changed,
                "CONTROL": control_pass.compact_changed_receipts,
            },
            "holdout_changed_error_receipts_for_locked_winner": winner_holdout_changed,
            "control_changed_error_receipts_for_locked_winner": winner_control_changed,
            "selection": selection.to_dict(),
            "ordered_digest_contract": {
                "algorithm": OrderedSemanticDigest.ALGORITHM,
                "item_grammar": "CANONICAL_EXACT_JSON_NO_TERMINAL_LF",
                "sequence_grammar": "OPEN_BRACKET_COMMA_JOIN_ITEMS_CLOSE_BRACKET_LF",
            },
            "independent_reconstruction_contract": {
                "q3_package_import_permitted": False,
                "read_and_hash_frozen_sources": True,
                "rebuild_physical_groups_and_q3_split": True,
                "derive_all_source_visible_features_from_bound_v6": True,
                "reconstruct_exact_rank_rows_and_selected_tiers": True,
                "recompute_five_train_statistics_and_fifteen_ridge_models": True,
                "recompute_train_holdout_control_scores_metrics_and_changed_errors": True,
                "compare_every_ordered_digest_and_semantic_seal": True,
            },
            "chronology": {
                "winner_lock": winner_lock,
                "control_reveal_token": control_token,
                "events": _semantic_chronology(chronology_events),
                "status": "PASS_LOCK_PERSISTED_BEFORE_CONTROL_TARGET_LOAD",
            },
        }
    )
    bundle_started = time.perf_counter_ns()
    bundle_disposition = write_once_gzip_exact_json(
        paths.validation_bundle, validation_bundle
    )
    validation_bundle_file_hash = file_sha256(paths.validation_bundle)
    phase_nanoseconds["validation_bundle_stream_and_write"] = (
        time.perf_counter_ns() - bundle_started
    )

    total_before_result = time.perf_counter_ns() - started
    primary_result = seal(
        {
            "schema": PRIMARY_RESULT_SCHEMA,
            "status": "PASS_Q3_PRIMARY_COMPLETE_UNINSTALLED",
            "automatic_promotion": False,
            "execution_mode": "QUERY_LOCAL_EXACT_STREAMING_V1",
            "foundation": source_receipt["foundation"],
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "source_receipt": source_receipt,
            "catalog_receipts": {
                "TRAIN": fit_result.catalog_receipt,
                "HOLDOUT": holdout_pass.catalog_receipt,
                "CONTROL": control_pass.catalog_receipt,
            },
            "training_statistics_receipts": fit_result.statistics_receipts,
            "model_receipt": model_receipt,
            "selection": selection.to_dict(),
            "evaluations": {
                "TRAIN": train_evaluation_receipt,
                "HOLDOUT": holdout_evaluation_receipt,
                "CONTROL": control_evaluation_receipt,
            },
            "changed_error_receipts": {
                "TRAIN": train_pass.compact_changed_receipts,
                "HOLDOUT": holdout_changed,
                "CONTROL": control_pass.compact_changed_receipts,
            },
            "chronology": {
                "events": chronology_events,
                "winner_lock_file_sha256": file_sha256(paths.winner_lock),
                "winner_lock_semantic_sha256": winner_lock["semantic_sha256"],
                "control_reveal_token_file_sha256": file_sha256(paths.control_token),
                "control_reveal_token_semantic_sha256": control_token["semantic_sha256"],
                "status": "PASS_LOCK_PERSISTED_BEFORE_SINGLE_CONTROL_REVEAL",
            },
            "validation_bundle": {
                "path": str(paths.validation_bundle),
                "schema": VALIDATION_BUNDLE_SCHEMA,
                "compression": "gzip_mtime_0_level_9_streamed",
                "file_sha256": validation_bundle_file_hash,
                "semantic_sha256": validation_bundle["semantic_sha256"],
                "write_disposition": bundle_disposition,
            },
            "counts": {
                "physical_groups": len(inventory.groups),
                "source_receipts": len(inventory.records),
                "fitted_models": len(models),
                "train_selectors_evaluated": 1 + len(train_pass.fitted_results),
                "holdout_selectors_evaluated": 1 + len(holdout_pass.fitted_results),
                "control_selectors_evaluated": 1 + len(control_pass.fitted_results),
                "control_target_loads_this_execution": 1,
            },
            "runtime": _runtime_receipt(phase_nanoseconds, total_before_result),
            "preserved_boundaries": (
                "NO_PROMOTION",
                "NO_CURRENT_POINTER_OR_LIVE_HISTORY_CHANGE",
                "NO_Q2_Q1_SLCV21R_OR_EXACT_WRITE_MUTATION",
                "NO_CONTROL_BEFORE_HOLDOUT_WINNER_LOCK",
                "NO_DOWNSTREAM_EXECUTION",
            ),
        }
    )
    result_disposition = write_once_exact_json(paths.primary_result, primary_result)
    structured_flat_ablation = build_structured_flat_ablation(primary_result)
    ablation_disposition = write_once_exact_json(
        paths.structured_flat_ablation, structured_flat_ablation
    )

    manifest = seal(
        {
            "schema": ARTIFACT_MANIFEST_SCHEMA,
            "status": "PASS_WRITE_ONCE_PRIMARY_ARTIFACT_CUSTODY",
            "execution_source_file_sha256s": execution_source_file_hashes,
            "foundation_binding": {
                "path": str(Path(binding_path)),
                "file_sha256": binding_file_hash,
                "snapshot_sha256": binding.snapshot_sha256,
                "semantic_sha256": binding.semantic_sha256,
                "snapshot_metadata_sha256": binding.snapshot_metadata_sha256,
                "native_module_archive_path": binding.native_module_archive_path,
                "native_module_sha256": binding.native_module_sha256,
                "import_receipt_semantic_sha256": foundation_consumer.import_receipt[
                    "semantic_sha256"
                ],
            },
            "foundation_import_receipt": foundation_consumer.import_receipt,
            "embedded_semantic_artifacts": {
                "source_receipt": source_receipt["semantic_sha256"],
                "train_catalog": fit_result.catalog_receipt["semantic_sha256"],
                "holdout_catalog": holdout_pass.catalog_receipt["semantic_sha256"],
                "control_catalog": control_pass.catalog_receipt["semantic_sha256"],
                "model_receipt": model_receipt["semantic_sha256"],
                "train_evaluation_receipt": train_evaluation_receipt["semantic_sha256"],
                "holdout_evaluation_receipt": holdout_evaluation_receipt[
                    "semantic_sha256"
                ],
                "control_evaluation_receipt": control_evaluation_receipt[
                    "semantic_sha256"
                ],
                "selection": selection.semantic_sha256,
                "validation_bundle": validation_bundle["semantic_sha256"],
            },
            "artifacts": {
                FEATURE_SCHEMA_FILENAME: {
                    "path": FEATURE_SCHEMA_FILENAME,
                    "file_sha256": file_sha256(paths.feature_schema),
                    "semantic_sha256": feature_schema_artifact["semantic_sha256"],
                },
                WINNER_LOCK_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{WINNER_LOCK_FILENAME}",
                    "file_sha256": file_sha256(paths.winner_lock),
                    "semantic_sha256": winner_lock["semantic_sha256"],
                },
                CONTROL_TOKEN_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{CONTROL_TOKEN_FILENAME}",
                    "file_sha256": file_sha256(paths.control_token),
                    "semantic_sha256": control_token["semantic_sha256"],
                },
                VALIDATION_BUNDLE_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{VALIDATION_BUNDLE_FILENAME}",
                    "file_sha256": validation_bundle_file_hash,
                    "semantic_sha256": validation_bundle["semantic_sha256"],
                },
                PRIMARY_RESULT_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{PRIMARY_RESULT_FILENAME}",
                    "file_sha256": file_sha256(paths.primary_result),
                    "semantic_sha256": primary_result["semantic_sha256"],
                },
                STRUCTURED_FLAT_ABLATION_FILENAME: {
                    "path": f"{WORK_DIRNAME}/{STRUCTURED_FLAT_ABLATION_FILENAME}",
                    "file_sha256": file_sha256(paths.structured_flat_ablation),
                    "semantic_sha256": structured_flat_ablation["semantic_sha256"],
                },
            },
        }
    )
    manifest_disposition = write_once_exact_json(paths.artifact_manifest, manifest)
    return {
        "schema": "SLCV33_RZ_Q3_PRIMARY_RUN_RECEIPT_V1",
        "status": "PASS_Q3_PRIMARY_COMPLETE_UNINSTALLED",
        "execution_mode": "QUERY_LOCAL_EXACT_STREAMING_V1",
        "selected_selector_id": selection.selected_selector_id,
        "selected_representation": selection.selected_representation,
        "primary_result_path": str(paths.primary_result),
        "primary_result_file_sha256": file_sha256(paths.primary_result),
        "primary_result_semantic_sha256": primary_result["semantic_sha256"],
        "validation_bundle_path": str(paths.validation_bundle),
        "validation_bundle_file_sha256": validation_bundle_file_hash,
        "artifact_manifest_path": str(paths.artifact_manifest),
        "artifact_manifest_file_sha256": file_sha256(paths.artifact_manifest),
        "write_dispositions": {
            "winner_lock": lock_disposition,
            "validation_bundle": bundle_disposition,
            "primary_result": result_disposition,
            "structured_flat_ablation": ablation_disposition,
            "artifact_manifest": manifest_disposition,
        },
        "control_targets_loaded_this_execution": True,
        "automatic_promotion": False,
    }


def run_primary_pipeline(
    candidate_root: str | Path,
    *,
    binding_path: str | Path = DEFAULT_BINDING_PATH,
) -> Mapping[str, Any]:
    """Verify/import the sealed V6 snapshot, then execute the gated Q3 pipeline."""

    binding = require_sealed_icf1_binding(binding_path)
    with BoundV6Foundation(binding) as foundation_consumer:
        return _run_streaming_primary_pipeline_with_foundation(
            candidate_root,
            binding_path=binding_path,
            foundation_consumer=foundation_consumer,
        )
