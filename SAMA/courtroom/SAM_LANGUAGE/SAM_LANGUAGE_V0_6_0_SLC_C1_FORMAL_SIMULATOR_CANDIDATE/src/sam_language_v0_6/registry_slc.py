"""Direct SLC C1 formal-state integration for the SAM Language registry."""

from __future__ import annotations

from typing import Any

from .errors import SLCStateInvariantError
from .slc_state import (
    DIMENSION,
    ENGINE_CONTRACT_HASH,
    FORMAL_AUTHORITY,
    FROZEN_SOURCE_HASHES,
    REGISTER_SIZE,
    ExactSLCState,
    binary_flip,
    inspect_state,
    prepare_request,
    x1_response,
    zero_state,
)


SLC_SOURCE_KEYS = (
    "parent_v05_release",
    "slcx002_operators",
    "slcx003_operator_lift",
    "slcx003_formal_grammar",
    "slc_c1_contract",
)
FORMAL_MODE = "slc-c1-formal"


def _site_index(entity: Any) -> int:
    value = entity.metadata.get("site_index")
    if type(value) is not int:
        raise SLCStateInvariantError(
            f"{entity.entity_id} does not carry a typed SLC site index"
        )
    return value


def _state_value(entity: Any) -> ExactSLCState:
    state = entity.metadata.get("_slc_state")
    if not isinstance(state, ExactSLCState):
        raise SLCStateInvariantError(
            f"{entity.entity_id} does not carry an exact SLC state"
        )
    state.assert_exact_normalization()
    state.require_replayable_zero_origin_custody()
    return state


def _state_entity(state: ExactSLCState, *, operator: str) -> Any:
    from .runtime import Authority, Entity

    dossier = inspect_state(state)
    return Entity(
        entity_id=f"SLC_STATE_{state.state_hash[:16]}_{state.history_hash[:16]}",
        scalar_value=None,
        semantic_type="SLCState12",
        authority=Authority(
            FORMAL_AUTHORITY,
            "SLCX002/SLCX003 plus V0_6_SLC_C1_CONTRACT.json",
            "Exact real 12-lebit formal state; phase, publication, and physical connectivity remain open",
        ),
        contextual_roles=("slc_c1_exact_joint_state",),
        metadata={
            "_slc_state": state,
            "result_payload": dossier,
            "produced_by": operator,
            "state_hash": state.state_hash,
            "history_hash": state.history_hash,
        },
        source_keys=SLC_SOURCE_KEYS,
        semantic_scope="SLC_C1_FORMAL",
    )


def _readout_entity(state: ExactSLCState) -> Any:
    from .runtime import Authority, Entity

    dossier = inspect_state(state)
    return Entity(
        entity_id=f"SLC_INSPECTION_{state.state_hash[:16]}_{state.history_hash[:16]}",
        scalar_value=None,
        semantic_type="SLCStateInspection",
        authority=Authority(
            FORMAL_AUTHORITY,
            "V0_6_SLC_C1_CONTRACT.json",
            "Read-only exact formal-state dossier",
        ),
        contextual_roles=("slc_c1_exact_state_inspection",),
        metadata={"result_payload": dossier},
        source_keys=SLC_SOURCE_KEYS,
        semantic_scope="SLC_C1_FORMAL",
    )


def _evaluate_zero(
    args: tuple[Any, ...], *, context: Any = None, registry: Any = None
) -> Any:
    del context, registry
    if args:
        raise SLCStateInvariantError("SLC_ZERO_REGISTER accepts no arguments")
    return _state_entity(zero_state(), operator="SLC_ZERO_REGISTER")


def _evaluate_binary_flip(
    args: tuple[Any, ...], *, context: Any = None, registry: Any = None
) -> Any:
    del context, registry
    state, site = args
    return _state_entity(
        binary_flip(_state_value(state), _site_index(site)),
        operator="SLC_BINARY_FLIP",
    )


def _evaluate_prepare_request(
    args: tuple[Any, ...], *, context: Any = None, registry: Any = None
) -> Any:
    del context, registry
    state, site = args
    return _state_entity(
        prepare_request(_state_value(state), _site_index(site)),
        operator="SLC_PREPARE_REQUEST",
    )


def _evaluate_x1_response(
    args: tuple[Any, ...], *, context: Any = None, registry: Any = None
) -> Any:
    del context, registry
    state, control, target = args
    return _state_entity(
        x1_response(
            _state_value(state),
            _site_index(control),
            _site_index(target),
        ),
        operator="SLC_X1_RESPONSE",
    )


def _evaluate_inspection(
    args: tuple[Any, ...], *, context: Any = None, registry: Any = None
) -> Any:
    del context, registry
    return _readout_entity(_state_value(args[0]))


def extend_registry(registry: Any) -> Any:
    """Install the exact formal C1 surface after core and QP registration."""

    from .runtime import Authority, Entity, OperatorSignature

    authority = Authority(
        FORMAL_AUTHORITY,
        "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY",
        "Complete real two-operation 12-lebit formal lift",
    )
    for site in range(REGISTER_SIZE):
        entity = Entity(
            entity_id=f"SLC_L{site}",
            scalar_value=site,
            semantic_type="SLCLebitSite",
            authority=authority,
            contextual_roles=("slc_formal_register_address",),
            metadata={
                "site_index": site,
                "register_size": REGISTER_SIZE,
                "address_status": "FORMAL_NOT_PHYSICAL_CONNECTIVITY",
            },
            source_keys=("slcx003_formal_grammar", "slc_c1_contract"),
            semantic_scope="SLC_C1_FORMAL",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id
        registry.aliases[f"L{site}"] = entity.entity_id

    signatures = {
        "SLC_ZERO_REGISTER": ((), "SLCState12", _evaluate_zero),
        "SLC_BINARY_FLIP": (
            ("SLCRegisterState", "SLCLebitSite"),
            "SLCState12",
            _evaluate_binary_flip,
        ),
        "SLC_PREPARE_REQUEST": (
            ("SLCRegisterState", "SLCLebitSite"),
            "SLCState12",
            _evaluate_prepare_request,
        ),
        "SLC_X1_RESPONSE": (
            ("SLCRegisterState", "SLCLebitSite", "SLCLebitSite"),
            "SLCState12",
            _evaluate_x1_response,
        ),
        "SLC_INSPECT_STATE": (
            ("SLCRegisterState",),
            "SLCStateInspection",
            _evaluate_inspection,
        ),
    }
    for name, (arg_types, result_type, evaluator) in signatures.items():
        registry.operators[name] = OperatorSignature(
            name=name,
            arg_types=tuple(arg_types),
            result_type=result_type,
            result_entity=None,
            authority=authority,
            source_keys=SLC_SOURCE_KEYS,
            evaluator=evaluator,
            semantic_scope="SLC_C1_FORMAL",
            required_mode=FORMAL_MODE,
        )

    registry.metadata["slc_c1"] = {
        "status": FORMAL_AUTHORITY,
        "execution_profile": FORMAL_MODE,
        "register_size": REGISTER_SIZE,
        "state_dimension": DIMENSION,
        "engine_contract_hash": ENGINE_CONTRACT_HASH,
        "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
        "state_authority": "EXACT_REAL_FORMAL",
        "open_boundaries": [
            "complex_phase",
            "publication_born_readout",
            "physical_connectivity",
            "coupling_cost",
            "hardware_realization",
        ],
    }
    return registry


__all__ = ["FORMAL_MODE", "SLC_SOURCE_KEYS", "extend_registry"]
