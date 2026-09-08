"""Q1 hardware roles with exact host-independent mathematical semantics.

H14F remains a fourteen-worker SLC architectural contract.  It is never used
to derive a host scheduler width.  Core i9 owns exact reference and
reconstruction, Ryzen CPU owns generation/training/search, and the 780M lane
can produce only a protocol result pending byte-exact Core-i9 reconstruction.
This module implements no network or remote-transfer operation.
"""

from __future__ import annotations

from pathlib import Path
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
DEFAULT_CONTRACT_PATH = PACKAGE_ROOT / "config" / "HARDWARE_PROTOCOL_CONTRACT.json"

CORE_I9 = "CORE_I9_EXACT_REFERENCE"
RYZEN_CPU = "RYZEN_9_8945HS_PRIMARY"
RYZEN_780M = "RYZEN_780M_RUSTICL_ACCELERATOR"
H14F_ARCHITECTURAL_CARDINALITY = 14

EXACT_WORKLOADS = frozenset(
    {
        "EXACT_REFERENCE",
        "INDEPENDENT_VALIDATION",
        "PREDECESSOR_RECONSTRUCTION",
        "READOUT_RECONSTRUCTION",
    }
)
RYZEN_WORKLOADS = frozenset(
    {
        "CATALOG_GENERATION",
        "FEATURE_EXTRACTION",
        "MODEL_TRAINING",
        "QUALITY_SEARCH",
        "SCORE_BATCH",
    }
)
REGULARITIES = frozenset({"REGULAR", "IRREGULAR"})
MEMORY_SHAPES = frozenset(
    {"SCALAR", "SPARSE", "RAGGED", "CONTIGUOUS_I64", "DENSE_RECTANGULAR_I64"}
)


class HardwareBoundaryError(CanonicalError):
    """A host route or reconstruction crossed Q1's hardware boundary."""


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise HardwareBoundaryError(f"{label} must be a positive exact integer")
    return value


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 160:
        raise HardwareBoundaryError(f"{label} must be a non-empty bounded string")
    return value


class HardwareProtocol:
    """Load the frozen E1 hardware contract and enforce Q1's bounded overlay."""

    def __init__(
        self,
        contract_path: str | Path | None = None,
        *,
        repository_root: str | Path | None = None,
        available_profiles: set[str] | frozenset[str] | None = None,
    ) -> None:
        self.repository_root = Path(repository_root or REPOSITORY_ROOT).resolve(strict=True)
        path = Path(contract_path or DEFAULT_CONTRACT_PATH)
        if path.is_symlink():
            raise HardwareBoundaryError("hardware protocol contract cannot be a symlink")
        self.contract_path = path.resolve(strict=True)
        contract = load_exact_json(self.contract_path)
        if not isinstance(contract, Mapping):
            raise HardwareBoundaryError("hardware protocol contract must be an object")
        try:
            require_seal(contract, "hardware protocol contract")
        except CanonicalError as exc:
            raise HardwareBoundaryError(str(exc)) from exc
        if contract.get("schema") != "SLCV32_RZ_Q1_HARDWARE_PROTOCOL_CONTRACT_V1":
            raise HardwareBoundaryError("hardware protocol schema is not admitted")
        if contract.get("status") != "FROZEN_BOUNDED_NON_PROMOTED_PORTABLE_PROTOCOL":
            raise HardwareBoundaryError("hardware protocol status is not frozen/bounded")

        source = contract.get("e1_source_contract")
        if not isinstance(source, Mapping):
            raise HardwareBoundaryError("E1 source hardware contract binding is unavailable")
        source_path = self.repository_root / str(source.get("path"))
        if source_path.is_symlink():
            raise HardwareBoundaryError("E1 source hardware contract cannot be a symlink")
        try:
            source_path = source_path.resolve(strict=True)
            source_path.relative_to(self.repository_root)
        except (OSError, ValueError) as exc:
            raise HardwareBoundaryError("E1 source hardware contract escaped custody") from exc
        if file_sha256(source_path) != source.get("file_sha256"):
            raise HardwareBoundaryError("E1 source hardware contract file identity changed")
        inherited = load_exact_json(source_path)
        if not isinstance(inherited, Mapping):
            raise HardwareBoundaryError("E1 source hardware contract must be an object")
        try:
            require_seal(inherited, "E1 source hardware contract")
        except CanonicalError as exc:
            raise HardwareBoundaryError(str(exc)) from exc
        if (
            inherited.get("schema") != source.get("schema")
            or inherited.get("semantic_sha256") != source.get("semantic_sha256")
        ):
            raise HardwareBoundaryError("E1 source hardware contract semantics changed")

        h14f = contract.get("h14f_architectural_contract")
        inherited_h14f = inherited.get("h14f_architectural_contract")
        if (
            not isinstance(h14f, Mapping)
            or not isinstance(inherited_h14f, Mapping)
            or h14f.get("structural_worker_cardinality") != H14F_ARCHITECTURAL_CARDINALITY
            or inherited_h14f.get("structural_worker_cardinality")
            != H14F_ARCHITECTURAL_CARDINALITY
            or h14f.get("maps_to_host_scheduler_width") is not False
            or inherited_h14f.get("maps_to_host_scheduler_width") is not False
        ):
            raise HardwareBoundaryError("H14F cardinality drifted into host scheduling")

        profiles_raw = contract.get("profiles")
        inherited_profiles_raw = inherited.get("profiles")
        if not isinstance(profiles_raw, list) or not isinstance(inherited_profiles_raw, list):
            raise HardwareBoundaryError("hardware profiles are unavailable")
        profiles: dict[str, Mapping[str, Any]] = {}
        inherited_profiles = {
            row.get("profile_id"): row for row in inherited_profiles_raw if isinstance(row, Mapping)
        }
        for row in profiles_raw:
            if not isinstance(row, Mapping):
                raise HardwareBoundaryError("Q1 host profile must be an object")
            profile_id = row.get("profile_id")
            if not isinstance(profile_id, str) or profile_id in profiles:
                raise HardwareBoundaryError("Q1 host profile identity is invalid or duplicated")
            width = _positive_int(row.get("scheduler_width"), f"{profile_id}.scheduler_width")
            inherited_row = inherited_profiles.get(profile_id)
            if not isinstance(inherited_row, Mapping) or inherited_row.get("scheduler_width") != width:
                raise HardwareBoundaryError(f"Q1 profile differs from inherited E1 width: {profile_id}")
            if width == H14F_ARCHITECTURAL_CARDINALITY:
                raise HardwareBoundaryError("host scheduler width cannot be sourced from H14F cardinality")
            admitted = row.get("admitted_workload_kinds")
            if not isinstance(admitted, list) or not admitted or len(set(admitted)) != len(admitted):
                raise HardwareBoundaryError(f"{profile_id} workload roster is invalid")
            if row.get("native_credit_authority") is not False:
                raise HardwareBoundaryError("Q1 host profiles cannot independently assign native credit")
            profiles[profile_id] = row
        if set(profiles) != {CORE_I9, RYZEN_CPU, RYZEN_780M}:
            raise HardwareBoundaryError("Q1 requires exactly i9, Ryzen CPU and Ryzen 780M profiles")
        if set(profiles[CORE_I9]["admitted_workload_kinds"]) != EXACT_WORKLOADS:
            raise HardwareBoundaryError("Core i9 exact-reference role changed")
        if not RYZEN_WORKLOADS <= set(profiles[RYZEN_CPU]["admitted_workload_kinds"]):
            raise HardwareBoundaryError("Ryzen generation/training/search role changed")
        if profiles[RYZEN_780M].get("mandatory_reconstruction_profile_id") != CORE_I9:
            raise HardwareBoundaryError("780M lane lost its Core-i9 reconstruction gate")

        policy = contract.get("routing_policy")
        gate = contract.get("reconstruction_gate")
        transfer = contract.get("transfer_boundary")
        if not all(isinstance(row, Mapping) for row in (policy, gate, transfer)):
            raise HardwareBoundaryError("hardware routing/gate/transfer policy is unavailable")
        if (
            policy.get("payload_hash_before_route") is not True
            or policy.get("host_choice_changes_mathematical_semantics") is not False
            or gate.get("native_cpu_reconstruction_required") is not True
            or gate.get("reconstruction_profile_id") != CORE_I9
            or gate.get("q1_bounded_run_claims_native_780m_execution_credit") is not False
            or transfer.get("remote_transfer_authorized") is not False
            or transfer.get("remote_execution_authorized") is not False
            or transfer.get("network_operation_implemented_by_q1_hardware_module") is not False
        ):
            raise HardwareBoundaryError("Q1 hardware safety boundary changed")

        self.contract = contract
        self.inherited_contract = inherited
        self.profiles = profiles
        self.policy = policy
        self.gate = gate
        self.available_profiles = frozenset(available_profiles or profiles)
        if not self.available_profiles <= set(profiles):
            raise HardwareBoundaryError("available_profiles contains an unknown host")

    def route(
        self,
        *,
        work_id: str,
        workload_kind: str,
        mathematical_payload: Any,
        regularity: str = "IRREGULAR",
        batch_size: int = 1,
        memory_shape: str = "SCALAR",
        gpu_eligible: bool = False,
        remote_transfer_requested: bool = False,
    ) -> dict[str, Any]:
        """Route one exact payload without changing its mathematical identity."""

        work_id = _identifier(work_id, "work_id")
        workload_kind = _identifier(workload_kind, "workload_kind")
        if workload_kind not in EXACT_WORKLOADS | RYZEN_WORKLOADS:
            raise HardwareBoundaryError(f"unsupported workload_kind: {workload_kind}")
        if regularity not in REGULARITIES:
            raise HardwareBoundaryError(f"unsupported regularity: {regularity}")
        batch_size = _positive_int(batch_size, "batch_size")
        if memory_shape not in MEMORY_SHAPES:
            raise HardwareBoundaryError(f"unsupported memory_shape: {memory_shape}")
        if not isinstance(gpu_eligible, bool) or not isinstance(remote_transfer_requested, bool):
            raise HardwareBoundaryError("gpu_eligible and remote_transfer_requested must be boolean")
        if remote_transfer_requested:
            raise HardwareBoundaryError("remote transfer is not authorized by Q1")
        payload_hash = canonical_sha256(mathematical_payload)

        gpu_shapes = set(self.policy["gpu_memory_shapes"])
        gpu_suitable = (
            workload_kind == "SCORE_BATCH"
            and gpu_eligible
            and regularity == self.policy["gpu_required_regularity"]
            and self.policy["gpu_minimum_batch_size"] <= batch_size
            <= self.policy["gpu_maximum_batch_size"]
            and memory_shape in gpu_shapes
        )
        fallback_used = False
        fallback_reason: str | None = None
        if workload_kind in EXACT_WORKLOADS:
            if CORE_I9 not in self.available_profiles:
                raise HardwareBoundaryError("Core i9 exact-reference lane is mandatory but unavailable")
            selected = CORE_I9
            reason = "EXACT_REFERENCE_OR_RECONSTRUCTION_REQUIRED"
        elif gpu_suitable and RYZEN_780M in self.available_profiles:
            selected = RYZEN_780M
            reason = "REGULAR_BOUNDED_SCORE_BATCH_PROTOCOL_LANE"
        elif RYZEN_CPU in self.available_profiles:
            selected = RYZEN_CPU
            reason = "RYZEN_GENERATION_TRAINING_OR_QUALITY_SEARCH"
            if gpu_suitable:
                fallback_used = True
                fallback_reason = "RYZEN_780M_PROFILE_UNAVAILABLE"
        elif CORE_I9 in self.available_profiles:
            selected = CORE_I9
            reason = "EXPLICIT_PORTABLE_CPU_FALLBACK"
            fallback_used = True
            fallback_reason = "RYZEN_CPU_PROFILE_UNAVAILABLE"
        else:
            raise HardwareBoundaryError("no compatible local Q1 host profile is available")

        profile = self.profiles[selected]
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_HOST_ROUTE_RECEIPT_V1",
                "status": "ROUTED",
                "work_id": work_id,
                "workload_kind": workload_kind,
                "regularity": regularity,
                "batch_size": batch_size,
                "memory_shape": memory_shape,
                "gpu_eligible": gpu_eligible,
                "gpu_suitable": gpu_suitable,
                "selected_profile_id": selected,
                "selected_scheduler_width": profile["scheduler_width"],
                "selected_lane_role": profile["lane_role"],
                "routing_reason": reason,
                "fallback_used": fallback_used,
                "fallback_reason": fallback_reason,
                "mathematical_payload": mathematical_payload,
                "mathematical_payload_semantic_sha256": payload_hash,
                "host_choice_changes_mathematical_semantics": False,
                "h14f_structural_worker_cardinality": H14F_ARCHITECTURAL_CARDINALITY,
                "h14f_cardinality_used_as_scheduler_width": False,
                "native_cpu_reconstruction_gate_required": selected == RYZEN_780M,
                "reconstruction_profile_id": CORE_I9 if selected == RYZEN_780M else None,
                "remote_transfer_requested": False,
                "remote_transfer_performed": False,
                "native_780m_execution_credited": False,
                "hardware_contract_semantic_sha256": self.contract["semantic_sha256"],
            }
        )

    @staticmethod
    def verify_payload_identity(route_receipt: Mapping[str, Any], payload: Any) -> bool:
        try:
            require_seal(route_receipt, "host route receipt")
            expected = canonical_sha256(payload)
        except CanonicalError:
            return False
        return (
            route_receipt.get("mathematical_payload") == payload
            and route_receipt.get("mathematical_payload_semantic_sha256") == expected
            and route_receipt.get("host_choice_changes_mathematical_semantics") is False
            and route_receipt.get("h14f_cardinality_used_as_scheduler_width") is False
            and route_receipt.get("remote_transfer_performed") is False
        )

    def build_780m_protocol_result(
        self,
        route_receipt: Mapping[str, Any],
        output: Any,
        *,
        remote_transfer_performed: bool = False,
        native_780m_execution_claimed: bool = False,
    ) -> dict[str, Any]:
        """Build a bounded protocol result; this does not claim native execution."""

        try:
            require_seal(route_receipt, "780M route receipt")
        except CanonicalError as exc:
            raise HardwareBoundaryError(str(exc)) from exc
        if route_receipt.get("selected_profile_id") != RYZEN_780M:
            raise HardwareBoundaryError("protocol result requires an admitted 780M route")
        if remote_transfer_performed:
            raise HardwareBoundaryError("remote transfer is not authorized by Q1")
        if native_780m_execution_claimed:
            raise HardwareBoundaryError(
                "bounded Q1 protocol semantics cannot claim unverified native 780M credit"
            )
        output_hash = canonical_sha256(output)
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_780M_PROTOCOL_RESULT_V1",
                "status": "PROTOCOL_EMULATION_PENDING_I9_RECONSTRUCTION",
                "work_id": route_receipt["work_id"],
                "route_semantic_sha256": route_receipt["semantic_sha256"],
                "mathematical_payload_semantic_sha256": route_receipt[
                    "mathematical_payload_semantic_sha256"
                ],
                "output": output,
                "output_semantic_sha256": output_hash,
                "protocol_profile_id": RYZEN_780M,
                "persistent_protocol_semantics": True,
                "remote_transfer_performed": False,
                "native_780m_execution_claimed": False,
                "native_780m_execution_credited": False,
                "cpu_reconstruction_required": True,
                "cpu_reconstruction_profile_id": CORE_I9,
            }
        )

    def admit_780m_reconstruction(
        self,
        route_receipt: Mapping[str, Any],
        protocol_result: Mapping[str, Any],
        i9_cpu_output: Any,
    ) -> dict[str, Any]:
        """Admit protocol semantics only after exact i9 output reconstruction."""

        try:
            require_seal(route_receipt, "780M route receipt")
            require_seal(protocol_result, "780M protocol result")
        except CanonicalError as exc:
            raise HardwareBoundaryError(str(exc)) from exc
        if (
            route_receipt.get("selected_profile_id") != RYZEN_780M
            or route_receipt.get("native_cpu_reconstruction_gate_required") is not True
            or route_receipt.get("reconstruction_profile_id") != CORE_I9
            or protocol_result.get("route_semantic_sha256") != route_receipt.get("semantic_sha256")
            or protocol_result.get("remote_transfer_performed") is not False
            or protocol_result.get("native_780m_execution_claimed") is not False
            or protocol_result.get("native_780m_execution_credited") is not False
        ):
            raise HardwareBoundaryError("780M protocol result crossed its reconstruction boundary")
        cpu_hash = canonical_sha256(i9_cpu_output)
        if (
            protocol_result.get("output") != i9_cpu_output
            or protocol_result.get("output_semantic_sha256") != cpu_hash
        ):
            raise HardwareBoundaryError("780M protocol output differs from exact i9 reconstruction")
        return seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_780M_CPU_RECONSTRUCTION_ADMISSION_V1",
                "status": "PROTOCOL_SEMANTICS_ADMITTED",
                "work_id": route_receipt["work_id"],
                "route_semantic_sha256": route_receipt["semantic_sha256"],
                "protocol_result_semantic_sha256": protocol_result["semantic_sha256"],
                "output_semantic_sha256": cpu_hash,
                "cpu_reconstruction_profile_id": CORE_I9,
                "cpu_reconstruction_exact": True,
                "protocol_semantics_admitted": True,
                "native_780m_execution_credited": False,
                "remote_transfer_performed": False,
                "host_choice_changes_mathematical_semantics": False,
                "h14f_structural_worker_cardinality": H14F_ARCHITECTURAL_CARDINALITY,
                "h14f_cardinality_used_as_scheduler_width": False,
            }
        )


__all__ = [
    "CORE_I9",
    "EXACT_WORKLOADS",
    "H14F_ARCHITECTURAL_CARDINALITY",
    "HardwareBoundaryError",
    "HardwareProtocol",
    "RYZEN_780M",
    "RYZEN_CPU",
    "RYZEN_WORKLOADS",
]
