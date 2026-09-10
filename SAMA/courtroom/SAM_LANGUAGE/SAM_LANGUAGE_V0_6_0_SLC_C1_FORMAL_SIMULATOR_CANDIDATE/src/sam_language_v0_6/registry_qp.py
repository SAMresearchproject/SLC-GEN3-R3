"""QP entities and operators installed into the single v0.5 registry."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path
from typing import Any

from .errors import ContractValidationError, QPDomainError, QPMultiplicityError, QPRegistrationError
from .qp_grammar import (
    ALPHABET,
    CARRIER_NATIVE,
    CONTROL_NAMES,
    DEPTHS,
    ROUTES,
    ProductionSpec,
    carrier_terminal,
    census_payload,
    enumerate_production_specs,
    explicit_control,
    hidden_support,
    ordered_pair,
    scalar_parent,
    triad_surface_gate,
    unary_conjugate,
    unary_direct,
    unordered_triad_candidate,
)
from .qp_native import (
    READOUT_FIELDS,
    default_data_dir,
    exact_readout,
    native_packet,
    validate_packaged_sources,
    verify_native_inverse,
    verify_native_reconciliation,
    verify_source_reconciliation,
)


OPEN_OPERATORS = (
    "PHYSICAL_OCCURRENCE_FROM_COMPLETED_WRITE",
    "ENTITY_LINEAGE",
    "RECIPROCAL_RELATION_INSTANCE",
    "RELAY_TO_WRITE",
    "A_TO_SLOT_LEDGER_MULTIPLICITY",
    "STARBREAKER_FORMATION_TRANSITION",
    "TERMINAL_REMNANT",
    "REMNANT_ISOTOPE_DECODER",
    "FORMATION_CONSERVATION_ACCOUNT",
    "STATE_BINDING_READOUT",
    "QP_PHYSICAL_ENTITY",
    "QP_OCCUPIED_LEDGER_SLOT",
    "QP_PHYSICAL_MASS",
    "QP_BINDING_ENERGY",
)


def _data_dir(registry: Any | None = None, data_dir: str | Path | None = None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    if registry is not None:
        configured = registry.metadata.get("qp_data_dir")
        if configured:
            return Path(str(configured))
    return default_data_dir()


def load_triad_allowed(data_dir: str | Path | None = None) -> frozenset[str]:
    root = _data_dir(data_dir=data_dir)
    validate_packaged_sources(root)
    path = root / "QP_TRIAD_ADMISSIBILITY.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 120 or len({row["signature"] for row in rows}) != 120:
        raise ContractValidationError("Frozen triad registry must contain 120 unique signatures")
    allowed = frozenset(
        row["signature"] for row in rows if row["typed_guard_allowed"].lower() == "true"
    )
    if len(allowed) != 107:
        raise ContractValidationError(f"Frozen triad registry must admit 107 signatures; found {len(allowed)}")
    return allowed


def _value(entity: Any) -> Any:
    if "qp_value" in entity.metadata:
        return entity.metadata["qp_value"]
    components = entity.metadata.get("components", ())
    return components[0] if len(components) == 1 else components


def _spec_entity(spec: ProductionSpec, Authority: Any, Entity: Any) -> Any:
    scope = "REJECTED_CONTROL" if spec.census_role == "REJECTED" else "STRUCTURAL_GRAMMAR"
    return Entity(
        entity_id=spec.signature,
        scalar_value=spec.native_account,
        semantic_type=spec.semantic_type,
        authority=Authority(
            "ACTIVE",
            "SAM_LANGUAGE_QP_PARTICLE_GRAMMAR_V1_FROZEN/registry/QP_GRAMMAR_CONTRACT.json",
            "Finite structural QP grammar; no physical identity, mass, or binding authority",
        ),
        contextual_roles=(spec.census_role.lower(),),
        ledger_role="non_ledger",
        metadata={
            **spec.metadata,
            "canonical_signature": spec.signature,
            "census_role": spec.census_role,
            "components": spec.components,
            "exact_native_account": str(spec.native_account),
            "physical_identity": "OPEN_UNREGISTERED",
        },
        source_keys=("qp_grammar_contract", "qp_source_reconciliation"),
        semantic_scope=scope,
    )


def _production_spec(entity: Any) -> ProductionSpec:
    signature = str(entity.metadata.get("canonical_signature", entity.entity_id))
    return ProductionSpec(
        signature,
        entity.semantic_type,
        str(entity.metadata.get("census_role", "CANDIDATE")),
        Fraction(entity.scalar_value),
        tuple(entity.metadata.get("components", ())),
        dict(entity.metadata),
    )


def _constructor_evaluator(operator: str):
    def evaluator(args: tuple[Any, ...], *, context: Any, registry: Any) -> Any:
        from .runtime import Authority, Entity

        if operator == "QP_UNARY_DIRECT":
            spec = unary_direct(int(_value(args[0])), int(_value(args[1])), str(_value(args[2])))
        elif operator == "QP_UNARY_CONJUGATE":
            spec = unary_conjugate(int(_value(args[0])), int(_value(args[1])), str(_value(args[2])))
        elif operator == "QP_ORDERED_PAIR":
            spec = ordered_pair(int(_value(args[0])), int(_value(args[1])))
        elif operator == "QP_UNORDERED_TRIAD":
            spec = unordered_triad_candidate(*(int(_value(arg)) for arg in args))
        elif operator == "QP_TRIAD_SURFACE_GATE":
            allowed = load_triad_allowed(_data_dir(registry))
            spec = triad_surface_gate(_production_spec(args[0]), allowed)
        elif operator == "QP_HIDDEN_SUPPORT":
            spec = hidden_support(int(_value(args[0])))
        elif operator == "QP_CARRIER_TERMINAL":
            spec = carrier_terminal(str(_value(args[0])))
        elif operator == "QP_SCALAR_PARENT":
            if not context.claim_global_once("QP_SCALAR_PARENT"):
                raise QPMultiplicityError("QP scalar parent is GLOBAL_ONCE within one program")
            spec = scalar_parent()
        elif operator == "QP_EXPLICIT_CONTROL":
            spec = explicit_control(str(_value(args[0])))
        else:
            raise QPRegistrationError(f"No integrated QP constructor evaluator for {operator}")
        return _spec_entity(spec, Authority, Entity)

    return evaluator


def _native_signature_evaluator(args: tuple[Any, ...], *, context: Any, registry: Any) -> Any:
    from .runtime import Authority, Entity

    production = args[0]
    signature = str(production.metadata.get("canonical_signature", production.entity_id))
    try:
        packet = native_packet(signature, _data_dir(registry))
    except KeyError as exc:
        raise QPRegistrationError(f"No native signature registered for {signature}") from exc
    return Entity(
        entity_id=f"NS:{signature}",
        scalar_value=None,
        semantic_type="QPNativeSignature",
        authority=Authority(
            "ACTIVE",
            "15_SCALE_BRIDGE_SIMULATOR/PDG_REVEAL_STAGEB_POST_ASSEMBLY_NATIVE_SIGNATURE_FREEZE/STAGEB_TEMPLATE_NATIVE_SIGNATURES.csv",
            "Exact structural native packet; not a physical mass packet",
        ),
        metadata={
            "canonical_signature": signature,
            "native_signature_packet": packet,
            "result_payload": packet,
            "physical_mass": "OPEN_UNREGISTERED",
        },
        source_keys=("qp_native_signatures", "qp_source_reconciliation"),
        semantic_scope="STRUCTURAL_GRAMMAR",
    )


def _readout_evaluator(operator: str):
    def evaluator(args: tuple[Any, ...], *, context: Any, registry: Any) -> Any:
        from .runtime import Authority, Entity

        packet = dict(args[0].metadata["native_signature_packet"])
        field, value, semantic_type = exact_readout(packet, operator)
        signature = packet["canonical_signature"]
        return Entity(
            entity_id=f"NR:{operator}:{signature}",
            scalar_value=value,
            semantic_type=semantic_type,
            authority=Authority(
                "ACTIVE",
                "15_SCALE_BRIDGE_SIMULATOR/PDG_REVEAL_STAGEB_POST_ASSEMBLY_NATIVE_SIGNATURE_FREEZE/STAGEB_TEMPLATE_NATIVE_SIGNATURES.csv",
                "Exact structural readout; physical interpretation remains open",
            ),
            metadata={
                "canonical_signature": signature,
                "native_field": field,
                "exact": str(value),
                "result_payload": {"canonical_signature": signature, "field": field, "exact": str(value)},
            },
            source_keys=("qp_native_signatures", "qp_source_reconciliation"),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )

    return evaluator


def extend_registry(registry: Any, data_dir: str | Path | None = None) -> Any:
    """Install QP values into a newly constructed core registry."""

    from .runtime import Authority, Entity, OperatorSignature

    root = _data_dir(data_dir=data_dir)
    validate_packaged_sources(root)
    registry.metadata["qp_data_dir"] = str(root)
    registry.metadata["open_operators"] = list(OPEN_OPERATORS)
    registry.metadata["qp_source_verified"] = True

    authority = Authority(
        "ACTIVE",
        "SAM_LANGUAGE_QP_PARTICLE_GRAMMAR_V1_FROZEN/registry/QP_GRAMMAR_CONTRACT.json",
        "Finite theorem-grade structural grammar; physical formation remains open",
    )

    for p in ALPHABET:
        entity = Entity(
            f"QP_P{p}",
            Fraction(p),
            "QPPartitionLabel",
            authority,
            ("qp_partition_label",),
            metadata={"qp_value": p, "domain": "QP_PARTITION_ALPHABET"},
            source_keys=("qp_grammar_contract",),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id
    for depth in DEPTHS:
        entity = Entity(
            f"QP_D{depth}",
            Fraction(depth),
            "QPDepth",
            authority,
            ("qp_closure_depth",),
            metadata={"qp_value": depth},
            source_keys=("qp_grammar_contract",),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id
    for route in ROUTES:
        entity = Entity(
            f"QP_ROUTE_{route.upper()}",
            None,
            "QPRouteMode",
            authority,
            ("qp_route_mode",),
            metadata={"qp_value": route},
            source_keys=("qp_grammar_contract",),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id
    for name in CARRIER_NATIVE:
        entity = Entity(
            f"QP_CARRIER_{name}",
            None,
            "QPCarrierTerminalName",
            authority,
            ("qp_carrier_terminal_name",),
            metadata={"qp_value": name},
            source_keys=("qp_grammar_contract",),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id
    for name in CONTROL_NAMES:
        entity = Entity(
            f"QP_CONTROL_{name}",
            None,
            "QPControlName",
            authority,
            ("qp_control_name",),
            metadata={"qp_value": name},
            source_keys=("qp_grammar_contract",),
            semantic_scope="REJECTED_CONTROL",
        )
        registry.entities[entity.entity_id] = entity
        registry.aliases[entity.entity_id] = entity.entity_id

    signatures = {
        "QP_UNARY_DIRECT": (("QPPartitionLabel", "QPDepth", "QPRouteMode"), "QPUnaryDirectTemplate"),
        "QP_UNARY_CONJUGATE": (("QPPartitionLabel", "QPDepth", "QPRouteMode"), "QPUnaryConjugateTemplate"),
        "QP_ORDERED_PAIR": (("QPPartitionLabel", "QPPartitionLabel"), "QPOrderedPairTemplate"),
        "QP_UNORDERED_TRIAD": (
            ("QPPartitionLabel", "QPPartitionLabel", "QPPartitionLabel"),
            "QPUnorderedTriadCandidate",
        ),
        "QP_TRIAD_SURFACE_GATE": (("QPUnorderedTriadCandidate",), "QPLocalTriadTemplate"),
        "QP_HIDDEN_SUPPORT": (("QPPartitionLabel",), "QPHiddenSupport"),
        "QP_CARRIER_TERMINAL": (("QPCarrierTerminalName",), "QPCarrierInfrastructure"),
        "QP_SCALAR_PARENT": ((), "QPGlobalScalarParent"),
        "QP_EXPLICIT_CONTROL": (("QPControlName",), "QPRejectedConstruction"),
    }
    for name, (arg_types, result_type) in signatures.items():
        registry.operators[name] = OperatorSignature(
            name,
            tuple(arg_types),
            result_type,
            None,
            authority,
            source_keys=("qp_grammar_contract", "qp_source_reconciliation"),
            evaluator=_constructor_evaluator(name),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )

    registry.operators["QP_NATIVE_SIGNATURE"] = OperatorSignature(
        "QP_NATIVE_SIGNATURE",
        ("QPGrammarProduction",),
        "QPNativeSignature",
        None,
        authority,
        source_keys=("qp_native_signatures", "qp_source_reconciliation"),
        evaluator=_native_signature_evaluator,
        semantic_scope="STRUCTURAL_GRAMMAR",
    )
    for name, (_, result_type) in READOUT_FIELDS.items():
        registry.operators[name] = OperatorSignature(
            name,
            ("QPNativeSignature",),
            result_type,
            None,
            authority,
            source_keys=("qp_native_signatures",),
            evaluator=_readout_evaluator(name),
            semantic_scope="STRUCTURAL_GRAMMAR",
        )
    return registry


def enumerate_qp_productions(data_dir: str | Path | None = None) -> list[dict[str, Any]]:
    allowed = load_triad_allowed(data_dir)
    return [spec.record() for spec in enumerate_production_specs(allowed)]


def inspect_qp_production(signature: str, data_dir: str | Path | None = None) -> dict[str, Any]:
    specs = {spec.signature: spec for spec in enumerate_production_specs(load_triad_allowed(data_dir))}
    if signature not in specs:
        raise QPRegistrationError(f"No canonical QP production named {signature}")
    spec = specs[signature]
    packet = native_packet(signature, data_dir)
    return {
        "production": spec.record(),
        "components": list(spec.components),
        "metadata": dict(spec.metadata),
        "native_signature": packet,
        "ordinary_gate_executable": spec.census_role != "REJECTED" or not signature.startswith("UT:"),
    }


def grammar_census(data_dir: str | Path | None = None) -> dict[str, Any]:
    return census_payload(enumerate_production_specs(load_triad_allowed(data_dir)))


def verify_qp_source_reconciliation(data_dir: str | Path | None = None) -> dict[str, Any]:
    return verify_source_reconciliation(data_dir)


def verify_qp_native_reconciliation(data_dir: str | Path | None = None) -> dict[str, Any]:
    return verify_native_reconciliation(data_dir)


def verify_qp_native_inverse(data_dir: str | Path | None = None) -> dict[str, Any]:
    return verify_native_inverse(data_dir)
