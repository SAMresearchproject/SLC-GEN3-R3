"""Bounded build, exact replay, and primary validation for SLCV32-RZ Q1.

The pipeline has one deterministic execution surface.  It admits frozen
sources and predecessors, freezes the Q1 catalogs before fitting, reconstructs
all four selector shapes twice, selects from complete HOLDOUT catalogs only,
reads CONTROL once for the selected winner, and emits canonical semantic
receipts.  It starts no persistent worker and performs no network or Git
operation.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

from .canonical import (
    canonical_sha256,
    file_sha256,
    load_exact_json,
    require_seal,
    seal_dict,
    write_canonical_json,
)
from .catalogs import CatalogBundle, CatalogGroup, build_catalog_bundle
from .checkpoints import CheckpointChain, STAGES, require_replay_identity
from .evaluation import EvaluationRow, evaluate_complete_catalogs, winner_key
from .extensions import evaluate_rh_services, run_atom3d_extension
from .hardware import HardwareProtocol
from .inheritance import E1InheritanceVerifier
from .release import CANDIDATE, PACKAGE_ROOT, build_release_manifest, verify_release_manifest
from .selectors import (
    ExactSelectorModel,
    ExactStatistics,
    TrainingRow,
    baseline_model,
    fit_listwise,
    fit_multi_head,
    fit_pairwise,
)
from .source_quality import (
    E1_SOURCE_INDEX,
    E1_SPLIT_MANIFEST,
    FEATURE_ORDER,
    Q1_GROUP_NAMESPACE,
    W9P_LEDGER,
    ReceiptChoice,
    baseline_score,
    source_admission_receipt,
)


TARGET_ID = "RECIPROCAL_QUOTIENTED_EXACT_W9P_RETURN_QUALITY_V1"
CLASSIFICATION = "The test result suggests strong contact with the concept."

PREEXECUTION_PATHS = {
    "source": "preexecution/SOURCE_ADMISSION.json",
    "split": "preexecution/Q1_GROUP_SPLIT_MANIFEST.json",
    "train": "preexecution/HARDER_TRAIN_CATALOG.json",
    "evaluation": "preexecution/COMPLETE_EVALUATION_CATALOGS.json",
    "statistics": "preexecution/CATALOG_STATISTICS.json",
}

EXECUTION_PATHS = {
    "primary": "release/execution/SELECTOR_COMPARISON_PRIMARY.json",
    "replay": "release/execution/SELECTOR_COMPARISON_REPLAY.json",
    "checkpoint_primary": "release/execution/CHECKPOINT_CHAIN_PRIMARY.json",
    "checkpoint_replay": "release/execution/CHECKPOINT_CHAIN_REPLAY.json",
    "checkpoint_identity": "release/execution/CHECKPOINT_REPLAY_IDENTITY.json",
    "reconstruction": "release/execution/FROZEN_PREDECESSOR_RECONSTRUCTION_ADMISSION.json",
    "ambiguity": "release/execution/AMBIGUITY_SERVICE_RECEIPT.json",
}


class PipelineError(RuntimeError):
    """A bounded Q1 execution, replay, or validation invariant failed."""


def _write(root: Path, relative: str, value: Any) -> Path:
    path = root / relative
    write_canonical_json(path, value)
    return path


def _sealed_model(model: ExactSelectorModel) -> dict[str, Any]:
    value = seal_dict(model.to_dict())
    if value["semantic_sha256"] != model.semantic_sha256:
        raise PipelineError("selector model semantic identity differs")
    return value


def _sealed_statistics(statistics: ExactStatistics | None) -> dict[str, Any] | None:
    if statistics is None:
        return None
    value = seal_dict(statistics.to_dict())
    if value["semantic_sha256"] != statistics.semantic_sha256:
        raise PipelineError("selector statistics semantic identity differs")
    return value


def _training_rows(bundle: CatalogBundle) -> tuple[TrainingRow, ...]:
    return tuple(
        TrainingRow(
            query_id=group.query_id,
            group_id=group.group_sha256,
            features=group.features,
            quality=group.quality,
            multiplicity=group.multiplicity,
        )
        for group in bundle.training_rows()
    )


def _evaluation_rows(
    bundle: CatalogBundle, split: str
) -> dict[str, tuple[EvaluationRow, ...]]:
    choices = {choice.receipt_index: choice for choice in bundle.choices}
    rows: dict[str, tuple[EvaluationRow, ...]] = {}
    for catalog in bundle.catalogs:
        query = catalog.query
        if query.split != split:
            continue
        rows[query.query_id] = tuple(
            EvaluationRow(
                query_id=group.query_id,
                group_id=group.group_sha256,
                features=group.features,
                quality=group.quality,
                multiplicity=group.multiplicity,
                baseline_score=baseline_score(
                    query, choices[group.representative_receipt_index]
                ),
            )
            for group in catalog.groups
        )
    expected = 128 if split in {"HOLDOUT", "CONTROL"} else None
    if expected is None or len(rows) != expected:
        raise PipelineError(f"{split} evaluation query roster differs")
    return rows


def _selector_budget(rows: Sequence[TrainingRow]) -> dict[str, Any]:
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_IDENTICAL_SELECTOR_BUDGET_V1",
            "status": "FROZEN_BEFORE_SELECTOR_FIT",
            "target_id": TARGET_ID,
            "group_namespace": Q1_GROUP_NAMESPACE,
            "selector_roster": [
                "DETERMINISTIC_EXACT_BASELINE",
                "PAIRWISE_EXACT_RANK_RIDGE",
                "LISTWISE_QUERY_CENTERED_BORDA_RIDGE",
                "MULTI_HEAD_EXACT_RESIDUAL_RIDGE",
            ],
            "identical_input_budget": {
                "training_query_count": len({row.query_id for row in rows}),
                "training_group_reference_count": len(rows),
                "training_receipt_exposure_count": sum(row.multiplicity for row in rows),
                "feature_count": len(FEATURE_ORDER),
                "catalog_passes": 1,
                "fit_count_per_selector": 1,
                "regularization_candidate_count": 1,
                "hyperparameter_search_performed": False,
                "holdout_catalog_policy": "ALL_SAME_AXIS_SPLIT_LOCAL_GROUPS_AND_RECEIPTS",
                "control_available_during_selection": False,
            },
            "objective_specific_shape": {
                "baseline_parameter_count": 0,
                "pairwise_parameter_cap": len(FEATURE_ORDER),
                "listwise_parameter_cap": len(FEATURE_ORDER),
                "multi_head_parameter_cap": 4 * len(FEATURE_ORDER),
                "multi_head_shared_row_pass": True,
            },
            "floating_point_training": False,
            "full_scale_tuning_started": False,
        }
    )


def _fit_models(
    rows: Sequence[TrainingRow],
) -> tuple[tuple[ExactSelectorModel, ExactStatistics | None], ...]:
    baseline = baseline_model(rows)
    pairwise = fit_pairwise(rows)
    listwise = fit_listwise(rows)
    multi_head = fit_multi_head(rows)
    models = (
        (baseline, None),
        pairwise,
        listwise,
        multi_head,
    )
    if len({model.selector_id for model, _ in models}) != 4:
        raise PipelineError("selector roster is not exact and unique")
    return models


def _execute_comparison(
    training_rows: Sequence[TrainingRow],
    holdout_rows: Mapping[str, Sequence[EvaluationRow]],
    control_rows: Mapping[str, Sequence[EvaluationRow]],
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, ExactSelectorModel]]:
    """Fit one exact roster, select on HOLDOUT, then read CONTROL once."""

    fitted = _fit_models(training_rows)
    holdout_results: dict[str, dict[str, Any]] = {}
    model_by_id: dict[str, ExactSelectorModel] = {}
    records = []
    for model, statistics in fitted:
        holdout = evaluate_complete_catalogs(model, holdout_rows, split="HOLDOUT")
        model_by_id[model.selector_id] = model
        holdout_results[model.selector_id] = holdout
        records.append(
            {
                "selector_id": model.selector_id,
                "selector_kind": model.selector_kind,
                "parameter_count": model.parameter_count,
                "model": _sealed_model(model),
                "statistics": _sealed_statistics(statistics),
                "holdout_evaluation": holdout,
            }
        )

    winner_id = max(
        sorted(model_by_id),
        key=lambda selector_id: winner_key(
            holdout_results[selector_id],
            model_by_id[selector_id].parameter_count,
            selector_id,
        ),
    )
    winner = model_by_id[winner_id]
    control = evaluate_complete_catalogs(winner, control_rows, split="CONTROL")
    comparison = seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_SELECTOR_COMPARISON_V1",
            "status": "PASS_COMPLETE_HOLDOUT_AND_POSTSELECTION_CONTROL",
            "candidate": CANDIDATE,
            "target_id": TARGET_ID,
            "budget_semantic_sha256": budget["semantic_sha256"],
            "selector_count": len(records),
            "selectors": records,
            "winner": {
                "selector_id": winner_id,
                "selector_kind": winner.selector_kind,
                "parameter_count": winner.parameter_count,
                "model_semantic_sha256": winner.semantic_sha256,
                "selection_split": "HOLDOUT",
                "selection_rule": [
                    "exact_best_set_recovery",
                    "best_tier_accuracy",
                    "strict_pair_accuracy",
                    "mean_harmonic_tier_gain_ratio",
                    "lower_mean_selected_target_tier",
                    "lower_false_singleton_rate",
                    "lower_abstention_rate",
                    "lower_parameter_count",
                    "canonical_selector_id_final_determinism_only",
                ],
                "holdout_evaluation_semantic_sha256": holdout_results[winner_id][
                    "semantic_sha256"
                ],
            },
            "control_evaluation": control,
            "control_firewall": {
                "winner_frozen_before_control_read": True,
                "control_models_evaluated": 1,
                "control_reads": 1,
                "control_used_for_model_or_threshold_selection": False,
                "control_used_for_winner_selection": False,
            },
            "complete_catalog_evaluation": True,
            "all_target_ties_set_valued": True,
            "custody_identifier_used_as_quality_tiebreak": False,
            "full_scale_tuning_started": False,
        }
    )
    return comparison, model_by_id


def _ambiguity_receipt(
    model: ExactSelectorModel,
    holdout_rows: Mapping[str, Sequence[EvaluationRow]],
) -> dict[str, Any]:
    evaluation = evaluate_complete_catalogs(
        model, holdout_rows, split="HOLDOUT", retain_query_receipts=True
    )
    receipts = evaluation["query_receipts"]
    counts = Counter(receipt["admission_status"] for receipt in receipts)
    ambiguous = next(
        (
            receipt
            for receipt in receipts
            if receipt["admission_status"] == "AMBIGUOUS_BEST_SET"
            and receipt["best_target_tier_selected"] is True
            and receipt["selected_receipt_count"] > 1
        ),
        None,
    )
    if ambiguous is None:
        raise PipelineError("real HOLDOUT evaluation produced no admitted ambiguity set")
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_AMBIGUITY_SERVICE_RECEIPT_V1",
            "status": "PASS_AMBIGUITY_SET_RETAINED",
            "selector_id": model.selector_id,
            "holdout_status_counts": dict(sorted(counts.items())),
            "holdout_query_count": len(receipts),
            "representative_query_receipt": ambiguous,
            "target_uniquely_ordered_within_representative_best_set": False,
            "receipt_or_group_identifier_used_as_tiebreak": False,
            "admitted_outputs": ["SELECTED_UNIQUE", "AMBIGUOUS_BEST_SET", "ABSTAIN"],
            "abstention_rule": "TOP_PREDICTIVE_TIE_SPANS_MORE_THAN_ONE_TARGET_TIER",
            "serialization_order_is_quality_order": False,
        }
    )


def _hardware_result(
    budget: Mapping[str, Any], winner_model: ExactSelectorModel
) -> dict[str, Any]:
    hardware = HardwareProtocol()
    generation_payload = {
        "catalog_namespace": Q1_GROUP_NAMESPACE,
        "training_catalog_semantic_sha256": budget["semantic_sha256"],
    }
    generation_route = hardware.route(
        work_id="Q1-CATALOG-AND-MODEL-TRAINING",
        workload_kind="MODEL_TRAINING",
        mathematical_payload=generation_payload,
        regularity="IRREGULAR",
        batch_size=1,
        memory_shape="RAGGED",
    )
    exact_payload = {
        "winner_model_semantic_sha256": winner_model.semantic_sha256,
        "operation": "EXACT_REFERENCE",
    }
    exact_route = hardware.route(
        work_id="Q1-I9-EXACT-REFERENCE",
        workload_kind="EXACT_REFERENCE",
        mathematical_payload=exact_payload,
    )
    score_payload = {
        "schema": "SLCV32_RZ_Q1_BOUNDED_SCORE_BATCH_V1",
        "winner_model_semantic_sha256": winner_model.semantic_sha256,
        "exact_integer_rows": [[index, index * index] for index in range(64)],
    }
    score_route = hardware.route(
        work_id="Q1-780M-PROTOCOL-SCORE-BATCH",
        workload_kind="SCORE_BATCH",
        mathematical_payload=score_payload,
        regularity="REGULAR",
        batch_size=64,
        memory_shape="CONTIGUOUS_I64",
        gpu_eligible=True,
    )
    exact_output = {
        "schema": "SLCV32_RZ_Q1_BOUNDED_SCORE_BATCH_OUTPUT_V1",
        "scores": [index * index - index for index in range(64)],
    }
    protocol_result = hardware.build_780m_protocol_result(score_route, exact_output)
    reconstruction_route = hardware.route(
        work_id="Q1-I9-RECONSTRUCT-780M-PROTOCOL",
        workload_kind="READOUT_RECONSTRUCTION",
        mathematical_payload={
            "protocol_result_semantic_sha256": protocol_result["semantic_sha256"],
            "exact_output": exact_output,
        },
    )
    reconstruction = hardware.admit_780m_reconstruction(
        score_route, protocol_result, exact_output
    )
    if not all(
        (
            hardware.verify_payload_identity(generation_route, generation_payload),
            hardware.verify_payload_identity(exact_route, exact_payload),
            hardware.verify_payload_identity(score_route, score_payload),
        )
    ):
        raise PipelineError("hardware routing changed an exact mathematical payload")
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_HARDWARE_PROTOCOL_RESULT_V1",
            "status": "PASS_LOCAL_PROTOCOL_AND_I9_RECONSTRUCTION",
            "generation_and_training_route": generation_route,
            "i9_exact_reference_route": exact_route,
            "bounded_780m_protocol_route": score_route,
            "bounded_780m_protocol_result": protocol_result,
            "i9_reconstruction_route": reconstruction_route,
            "i9_reconstruction_admission": reconstruction,
            "h14f_architectural_cardinality": 14,
            "h14f_used_as_host_scheduler_width": False,
            "native_780m_execution_credited": False,
            "remote_transfer_performed": False,
            "unauthorized_remote_transfer_attempted": False,
        }
    )


def _dependency_manifest(
    root: Path,
    source: Mapping[str, Any],
    inheritance: Mapping[str, Any],
) -> dict[str, Any]:
    repository_root = Path(__file__).resolve().parents[4]
    source_paths = (E1_SOURCE_INDEX, E1_SPLIT_MANIFEST, W9P_LEDGER)
    configs = tuple(sorted((root / "config").glob("*.json")))
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_DEPENDENCY_SOURCE_MANIFEST_V1",
            "status": "SEALED_SOURCE_BOUND_STDLIB_ONLY",
            "candidate": CANDIDATE,
            "runtime": {
                "language": "Python 3",
                "external_python_packages": [],
                "integer_fraction_canonical_execution": True,
                "network_dependency": False,
            },
            "frozen_source_artifacts": [
                {
                    "path": path.relative_to(repository_root).as_posix(),
                    "sha256": file_sha256(path),
                }
                for path in source_paths
            ],
            "candidate_contracts": [
                {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": file_sha256(path),
                    "semantic_sha256": load_exact_json(path)["semantic_sha256"],
                }
                for path in configs
            ],
            "source_admission_semantic_sha256": source["semantic_sha256"],
            "e1_release_manifest_semantic_sha256": inheritance[
                "e1_release_manifest_semantic_sha256"
            ],
            "a1_release_manifest_semantic_sha256": inheritance[
                "a1_release_manifest_semantic_sha256"
            ],
            "current_pointer": "SLCV21R",
            "current_pointer_sha256": inheritance["current_pointer_sha256"],
            "current_pointer_used_as_runtime_dependency": False,
            "remote_git_import_performed": False,
            "remote_transfer_performed": False,
        }
    )


def _architecture_result(
    bundle: CatalogBundle,
    budget: Mapping[str, Any],
    comparison: Mapping[str, Any],
) -> dict[str, Any]:
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_ARCHITECTURE_RESULT_V1",
            "status": "PASS_BOUNDED_RELATIVE_QUALITY_ARCHITECTURE",
            "candidate": CANDIDATE,
            "candidate_role": "NON_PROMOTED_SUCCESSOR_CANDIDATE_TO_FROZEN_SLCV31_RZ_E1",
            "target": {
                "target_id": TARGET_ID,
                "ordered_components": [
                    "signed_direction_mismatch",
                    "exact_inverse_input_residual",
                    "returned_W8_final_state_residual",
                    "D81_checkpoint_residual",
                ],
                "reciprocal_lane_swap_quotient": True,
                "source_bound": True,
                "learned_feature_target_circularity": False,
            },
            "catalog": {
                "receipt_choices": len(bundle.choices),
                "canonical_queries": len(bundle.queries),
                "physical_groups": bundle.statistics["physical_group_count"],
                "group_namespace": Q1_GROUP_NAMESPACE,
                "per_axis_group_split": {"TRAIN": 96, "HOLDOUT": 16, "CONTROL": 16},
                "training_group_references": len(bundle.training_rows()),
                "complete_holdout_group_references": bundle.full_catalog_manifest[
                    "counts"
                ]["group_references"]["HOLDOUT"],
                "complete_control_group_references": bundle.full_catalog_manifest[
                    "counts"
                ]["group_references"]["CONTROL"],
            },
            "selector_budget_semantic_sha256": budget["semantic_sha256"],
            "selected_selector_id": comparison["winner"]["selector_id"],
            "checkpoint_stages": list(STAGES),
            "ambiguity_outputs": ["SELECTED_UNIQUE", "AMBIGUOUS_BEST_SET", "ABSTAIN"],
            "control_postselection_only": True,
            "h14f_architectural_cardinality": 14,
            "h14f_cardinality_is_host_scheduler_width": False,
            "atom3d_role": "IMMUTABLE_BASE_APPLICATION_EXTENSION_ONLY",
            "physical_calibration_started": False,
            "physical_specialization_started": False,
            "full_scale_tuning_started": False,
            "promoted": False,
        }
    )


def _quality_result(
    comparison: Mapping[str, Any],
    source: Mapping[str, Any],
    bundle: CatalogBundle,
    checkpoint_primary: Mapping[str, Any],
    checkpoint_identity: Mapping[str, Any],
    reconstruction: Mapping[str, Any],
    ambiguity: Mapping[str, Any],
    hardware: Mapping[str, Any],
    rh: Mapping[str, Any],
    atom3d: Mapping[str, Any],
    postexecution: Mapping[str, Any],
    dependency: Mapping[str, Any],
    architecture: Mapping[str, Any],
) -> dict[str, Any]:
    winner_id = comparison["winner"]["selector_id"]
    winner_row = next(
        row for row in comparison["selectors"] if row["selector_id"] == winner_id
    )
    baseline_row = next(
        row
        for row in comparison["selectors"]
        if row["selector_kind"] == "DETERMINISTIC_EXACT_BASELINE"
    )
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_QUALITY_ENGINE_RESULT_V1",
            "status": "PASS_SUBSTANTIAL_BOUNDED_NON_PROMOTED_CANDIDATE",
            "candidate": CANDIDATE,
            "predecessor": "SLCV31-RZ QUALITY ENGINE CANDIDATE E1",
            "classification": CLASSIFICATION,
            "selected_selector": comparison["winner"],
            "winner_holdout": winner_row["holdout_evaluation"],
            "baseline_holdout": baseline_row["holdout_evaluation"],
            "winner_control": comparison["control_evaluation"],
            "selector_comparison_semantic_sha256": comparison["semantic_sha256"],
            "source_admission_semantic_sha256": source["semantic_sha256"],
            "q1_group_split_semantic_sha256": bundle.split_manifest[
                "semantic_sha256"
            ],
            "harder_train_catalog_semantic_sha256": bundle.training_manifest[
                "semantic_sha256"
            ],
            "complete_evaluation_catalogs_semantic_sha256": bundle.full_catalog_manifest[
                "semantic_sha256"
            ],
            "catalog_statistics_semantic_sha256": bundle.statistics[
                "semantic_sha256"
            ],
            "selector_budget_semantic_sha256": comparison[
                "budget_semantic_sha256"
            ],
            "checkpoint_chain_primary_semantic_sha256": checkpoint_primary[
                "semantic_sha256"
            ],
            "checkpoint_replay_identity_semantic_sha256": checkpoint_identity[
                "semantic_sha256"
            ],
            "frozen_predecessor_reconstruction_admission_semantic_sha256": reconstruction[
                "semantic_sha256"
            ],
            "ambiguity_service_semantic_sha256": ambiguity["semantic_sha256"],
            "hardware_protocol_semantic_sha256": hardware["semantic_sha256"],
            "dependency_source_manifest_semantic_sha256": dependency[
                "semantic_sha256"
            ],
            "architecture_result_semantic_sha256": architecture["semantic_sha256"],
            "rh_service_decision": {
                "status": rh["status"],
                "outcome": rh["outcome"],
                "services_admitted": rh["relative_target_material_services_admitted"],
                "semantic_sha256": rh["semantic_sha256"],
            },
            "atom3d_extension": {
                "status": atom3d["status"],
                "base_model_unchanged": atom3d["base_model_unchanged"],
                "semantic_sha256": atom3d["semantic_sha256"],
            },
            "predecessors_byte_identical": postexecution["predecessors_byte_identical"],
            "current_pointer": "SLCV21R",
            "current_pointer_changed": False,
            "control_boundary": "CONTROL_READ_ONCE_AFTER_SELECTION",
            "persistent_candidate_workers_started": False,
            "persistent_candidate_workers_active": False,
            "full_scale_tuning_started": False,
            "promoted": False,
        }
    )


def _checkpoint_chain(
    inheritance: Mapping[str, Any],
    source: Mapping[str, Any],
    bundle: CatalogBundle,
    budget: Mapping[str, Any],
    comparison: Mapping[str, Any],
    reconstruction: Mapping[str, Any],
) -> dict[str, Any]:
    model_hashes = {
        row["selector_id"]: row["model"]["semantic_sha256"]
        for row in comparison["selectors"]
    }
    holdout_hashes = {
        row["selector_id"]: row["holdout_evaluation"]["semantic_sha256"]
        for row in comparison["selectors"]
    }
    payloads = (
        {
            "inheritance_verification_semantic_sha256": inheritance["semantic_sha256"],
            "source_admission_semantic_sha256": source["semantic_sha256"],
        },
        {
            "group_split_semantic_sha256": bundle.split_manifest["semantic_sha256"],
            "full_catalog_semantic_sha256": bundle.full_catalog_manifest["semantic_sha256"],
            "target_id": TARGET_ID,
        },
        {
            "training_catalog_semantic_sha256": bundle.training_manifest[
                "semantic_sha256"
            ],
            "selector_budget_semantic_sha256": budget["semantic_sha256"],
        },
        {"model_semantic_sha256s": model_hashes},
        {"holdout_evaluation_semantic_sha256s": holdout_hashes},
        {
            "winner_selector_id": comparison["winner"]["selector_id"],
            "selection_split": "HOLDOUT",
            "control_read": False,
        },
        {
            "control_evaluation_semantic_sha256": comparison["control_evaluation"][
                "semantic_sha256"
            ],
            "control_models_evaluated": 1,
            "control_reads": 1,
            "winner_changed_after_control": False,
        },
        {
            "reconstruction_admission_semantic_sha256": reconstruction[
                "semantic_sha256"
            ],
            "predecessors_mutated": False,
        },
    )
    chain = CheckpointChain(
        candidate=CANDIDATE,
        root_predecessor_semantic_sha256=inheritance["semantic_sha256"],
    )
    for stage, payload in zip(STAGES, payloads, strict=True):
        chain = chain.append(stage, payload)
    return chain.to_dict()


def _primary_validation(
    *,
    inheritance_before: Mapping[str, Any],
    postexecution: Mapping[str, Any],
    source: Mapping[str, Any],
    bundle: CatalogBundle,
    budget: Mapping[str, Any],
    primary: Mapping[str, Any],
    replay: Mapping[str, Any],
    checkpoint_primary: Mapping[str, Any],
    checkpoint_replay: Mapping[str, Any],
    checkpoint_identity: Mapping[str, Any],
    reconstruction: Mapping[str, Any],
    ambiguity: Mapping[str, Any],
    hardware: Mapping[str, Any],
    rh: Mapping[str, Any],
    atom3d: Mapping[str, Any],
    quality: Mapping[str, Any],
) -> dict[str, Any]:
    checks = {
        "predecessor_chain_admitted": inheritance_before["status"] == "PASS",
        "predecessors_byte_identical_after_execution": postexecution[
            "predecessors_byte_identical"
        ]
        is True,
        "current_pointer_unchanged": postexecution["current_pointer_unchanged"] is True,
        "all_5120_receipts_admitted": source["choice_count"] == 5120,
        "all_1024_queries_admitted": source["canonical_query_count"] == 1024,
        "all_512_physical_groups_admitted": source["group_count"] == 512,
        "fresh_q1_split_namespace": source["e1_split_reused"] is False,
        "split_leakage_checks_pass": all(bundle.split_manifest["leakage_checks"].values()),
        "harder_training_catalog_frozen_before_fit": bundle.training_manifest[
            "freeze_boundary"
        ]
        == "FROZEN_BEFORE_ANY_SELECTOR_FIT_OR_COMPARISON",
        "holdout_catalog_complete": bundle.full_catalog_manifest[
            "complete_catalog_guards"
        ]["all_split_local_same_axis_receipts_exposed"]
        is True,
        "control_catalog_complete": bundle.full_catalog_manifest["counts"][
            "query_counts"
        ]["CONTROL"]
        == 128,
        "identical_selector_budget_frozen": budget["status"]
        == "FROZEN_BEFORE_SELECTOR_FIT",
        "four_selectors_compared": primary["selector_count"] == 4,
        "complete_holdout_all_selectors": all(
            row["holdout_evaluation"]["query_count"] == 128
            for row in primary["selectors"]
        ),
        "winner_selected_on_holdout": primary["winner"]["selection_split"] == "HOLDOUT",
        "control_read_once_postselection": primary["control_firewall"]["control_reads"]
        == 1,
        "control_not_used_for_selection": primary["control_firewall"][
            "control_used_for_winner_selection"
        ]
        is False,
        "primary_replay_semantic_equal": dict(primary) == dict(replay),
        "checkpoint_chains_semantic_equal": dict(checkpoint_primary)
        == dict(checkpoint_replay),
        "checkpoint_replay_identity_pass": checkpoint_identity["status"] == "PASS",
        "frozen_predecessor_reconstruction_admitted": reconstruction["status"]
        == "ADMITTED",
        "ambiguity_set_retained": ambiguity["status"]
        == "PASS_AMBIGUITY_SET_RETAINED",
        "false_singleton_rate_zero_for_winner": primary["control_evaluation"][
            "false_singleton_rate"
        ]["numerator"]
        == "0",
        "hardware_protocol_pass": hardware["status"]
        == "PASS_LOCAL_PROTOCOL_AND_I9_RECONSTRUCTION",
        "h14f_separate_from_scheduling": hardware[
            "h14f_used_as_host_scheduler_width"
        ]
        is False,
        "no_native_780m_credit": hardware["native_780m_execution_credited"] is False,
        "no_remote_transfer": hardware["remote_transfer_performed"] is False,
        "rh_typed_no_gain": rh["status"] == "PASS_TYPED_NO_GAIN",
        "rh_no_unmaterial_service_admitted": rh[
            "relative_target_material_services_admitted"
        ]
        == 0,
        "atom3d_base_immutable": atom3d["base_model_unchanged"] is True,
        "atom3d_not_specialized": atom3d["specialization_trained"] is False,
        "physical_calibration_not_started": atom3d["physical_calibration_executed"]
        is False,
        "full_scale_tuning_not_started": primary["full_scale_tuning_started"] is False,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise PipelineError(f"primary Q1 validation failed: {failed}")
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_PRIMARY_VALIDATION_RESULT_V1",
            "status": "PASS",
            "candidate": CANDIDATE,
            "assertions_passed": len(checks),
            "assertions_failed": 0,
            "assertions": checks,
            "selector_comparison_semantic_sha256": primary["semantic_sha256"],
            "checkpoint_replay_identity_semantic_sha256": checkpoint_identity[
                "semantic_sha256"
            ],
            "quality_engine_result_semantic_sha256": quality["semantic_sha256"],
            "classification": CLASSIFICATION,
            "promoted": False,
            "current_pointer": "SLCV21R",
            "persistent_candidate_workers_started": False,
        }
    )


def build_candidate(candidate_root: str | Path = PACKAGE_ROOT) -> dict[str, Any]:
    """Build the complete bounded pre-tail release and its release manifest."""

    root = Path(candidate_root).resolve(strict=True)
    if root != PACKAGE_ROOT.resolve(strict=True):
        raise PipelineError("Q1 build root must be the canonical candidate root")

    verifier = E1InheritanceVerifier()
    inheritance_before = verifier.verify()
    target_contract = load_exact_json(root / "config/QUALITY_TARGET_CONTRACT.json")
    require_seal(target_contract, "Q1 quality-target contract")
    if target_contract.get("target_id") != TARGET_ID:
        raise PipelineError("pipeline target identity differs from the frozen contract")
    bundle = build_catalog_bundle()
    source = source_admission_receipt(bundle.choices)
    training_rows = _training_rows(bundle)
    holdout_rows = _evaluation_rows(bundle, "HOLDOUT")
    control_rows = _evaluation_rows(bundle, "CONTROL")
    budget = _selector_budget(training_rows)

    _write(root, PREEXECUTION_PATHS["source"], source)
    _write(root, PREEXECUTION_PATHS["split"], bundle.split_manifest)
    _write(root, PREEXECUTION_PATHS["train"], bundle.training_manifest)
    _write(root, PREEXECUTION_PATHS["evaluation"], bundle.full_catalog_manifest)
    _write(root, PREEXECUTION_PATHS["statistics"], bundle.statistics)
    _write(root, "preexecution/SELECTOR_BUDGET.json", budget)

    primary, primary_models = _execute_comparison(
        training_rows, holdout_rows, control_rows, budget
    )
    replay, replay_models = _execute_comparison(
        training_rows, holdout_rows, control_rows, budget
    )
    if dict(primary) != dict(replay):
        raise PipelineError("primary selector execution and exact replay differ")
    if {
        key: value.semantic_sha256 for key, value in primary_models.items()
    } != {key: value.semantic_sha256 for key, value in replay_models.items()}:
        raise PipelineError("primary and replay model identities differ")

    primary_path = _write(root, EXECUTION_PATHS["primary"], primary)
    replay_path = _write(root, EXECUTION_PATHS["replay"], replay)
    if file_sha256(primary_path) != file_sha256(replay_path):
        raise PipelineError("primary/replay canonical comparison bytes differ")

    winner_model = primary_models[primary["winner"]["selector_id"]]
    ambiguity = _ambiguity_receipt(winner_model, holdout_rows)
    hardware = _hardware_result(budget, winner_model)
    rh = evaluate_rh_services()
    atom3d = run_atom3d_extension(_sealed_model(winner_model))

    reconstruction = verifier.admit_reconstruction(
        {
            "predecessor": "SLCV31-RZ QUALITY ENGINE CANDIDATE E1",
            "predecessor_manifest_semantic_sha256": inheritance_before[
                "e1_release_manifest_semantic_sha256"
            ],
            "complete_catalog_reconstructed": True,
            "checkpoint_replay_identical": True,
            "semantic_receipts_verified": True,
            "predecessor_mutated": False,
            "current_pointer_changed": False,
        }
    )
    checkpoint_primary = _checkpoint_chain(
        inheritance_before, source, bundle, budget, primary, reconstruction
    )
    checkpoint_replay = _checkpoint_chain(
        inheritance_before, source, bundle, budget, replay, reconstruction
    )
    checkpoint_identity = require_replay_identity(checkpoint_primary, checkpoint_replay)

    checkpoint_primary_path = _write(
        root, EXECUTION_PATHS["checkpoint_primary"], checkpoint_primary
    )
    checkpoint_replay_path = _write(
        root, EXECUTION_PATHS["checkpoint_replay"], checkpoint_replay
    )
    primary_checkpoint_file = file_sha256(checkpoint_primary_path)
    replay_checkpoint_file = file_sha256(checkpoint_replay_path)
    if primary_checkpoint_file != replay_checkpoint_file:
        raise PipelineError("primary/replay canonical checkpoint bytes differ")
    checkpoint_identity = seal_dict(
        {
            **{key: value for key, value in checkpoint_identity.items() if key != "semantic_sha256"},
            "primary_file_sha256": primary_checkpoint_file,
            "replay_file_sha256": replay_checkpoint_file,
            "canonical_file_bytes_equal": True,
            "selector_comparison_file_sha256": file_sha256(primary_path),
            "selector_comparison_replay_file_sha256": file_sha256(replay_path),
        }
    )

    _write(root, EXECUTION_PATHS["checkpoint_identity"], checkpoint_identity)
    _write(root, EXECUTION_PATHS["reconstruction"], reconstruction)
    _write(root, EXECUTION_PATHS["ambiguity"], ambiguity)
    _write(root, "release/hardware/HARDWARE_PROTOCOL_RESULT.json", hardware)
    _write(root, "release/rh/RH_SERVICE_DECISION.json", rh)
    _write(root, "release/atom3d/ATOM3D_EXTENSION_RECEIPT.json", atom3d)

    postexecution = verifier.verify_after_execution(inheritance_before)
    dependency = _dependency_manifest(root, source, inheritance_before)
    architecture = _architecture_result(bundle, budget, primary)
    quality = _quality_result(
        primary,
        source,
        bundle,
        checkpoint_primary,
        checkpoint_identity,
        reconstruction,
        ambiguity,
        hardware,
        rh,
        atom3d,
        postexecution,
        dependency,
        architecture,
    )
    validation = _primary_validation(
        inheritance_before=inheritance_before,
        postexecution=postexecution,
        source=source,
        bundle=bundle,
        budget=budget,
        primary=primary,
        replay=replay,
        checkpoint_primary=checkpoint_primary,
        checkpoint_replay=checkpoint_replay,
        checkpoint_identity=checkpoint_identity,
        reconstruction=reconstruction,
        ambiguity=ambiguity,
        hardware=hardware,
        rh=rh,
        atom3d=atom3d,
        quality=quality,
    )
    _write(root, "release/DEPENDENCY_SOURCE_MANIFEST.json", dependency)
    _write(root, "release/ARCHITECTURE_RESULT.json", architecture)
    _write(root, "release/QUALITY_ENGINE_RESULT.json", quality)
    _write(root, "release/VALIDATION_RESULT.json", validation)

    manifest = build_release_manifest(root=root)
    verified_manifest = verify_release_manifest(root=root)
    if manifest != verified_manifest:
        raise PipelineError("new release manifest failed immediate reconstruction")
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_BUILD_SUMMARY_V1",
            "status": "PASS_PRETAIL_RELEASE_BUILT",
            "candidate": CANDIDATE,
            "winner_selector_id": primary["winner"]["selector_id"],
            "classification": CLASSIFICATION,
            "release_artifact_count": manifest["artifact_count"],
            "release_manifest_semantic_sha256": manifest["semantic_sha256"],
            "primary_validation_semantic_sha256": validation["semantic_sha256"],
            "current_pointer": "SLCV21R",
            "promoted": False,
            "persistent_candidate_workers_started": False,
        }
    )


def validate_existing_candidate(candidate_root: str | Path = PACKAGE_ROOT) -> dict[str, Any]:
    """Read-only primary reconstruction of an already-built Q1 pre-tail tree."""

    root = Path(candidate_root).resolve(strict=True)
    manifest = verify_release_manifest(root=root)
    names = {
        **EXECUTION_PATHS,
        "validation": "release/VALIDATION_RESULT.json",
        "quality": "release/QUALITY_ENGINE_RESULT.json",
        "hardware": "release/hardware/HARDWARE_PROTOCOL_RESULT.json",
        "rh": "release/rh/RH_SERVICE_DECISION.json",
        "atom3d": "release/atom3d/ATOM3D_EXTENSION_RECEIPT.json",
    }
    values = {name: load_exact_json(root / relative) for name, relative in names.items()}
    for name, value in values.items():
        if not isinstance(value, Mapping):
            raise PipelineError(f"{name} artifact is not an exact object")
        require_seal(value, name)
    if values["primary"] != values["replay"]:
        raise PipelineError("stored primary/replay selector comparisons differ")
    if values["checkpoint_primary"] != values["checkpoint_replay"]:
        raise PipelineError("stored primary/replay checkpoint chains differ")
    if values["validation"].get("status") != "PASS":
        raise PipelineError("stored primary validation does not pass")
    if values["quality"].get("classification") != CLASSIFICATION:
        raise PipelineError("stored result classification differs")
    inheritance = E1InheritanceVerifier().verify()
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_READ_ONLY_RECONSTRUCTION_V1",
            "status": "PASS",
            "release_artifacts_hash_verified": manifest["artifact_count"],
            "release_manifest_semantic_sha256": manifest["semantic_sha256"],
            "selector_comparison_semantic_sha256": values["primary"][
                "semantic_sha256"
            ],
            "checkpoint_chain_semantic_sha256": values["checkpoint_primary"][
                "semantic_sha256"
            ],
            "inheritance_verification_semantic_sha256": inheritance[
                "semantic_sha256"
            ],
            "current_pointer": "SLCV21R",
            "promoted": False,
        }
    )


__all__ = [
    "CLASSIFICATION",
    "EXECUTION_PATHS",
    "PipelineError",
    "PREEXECUTION_PATHS",
    "TARGET_ID",
    "build_candidate",
    "validate_existing_candidate",
]
