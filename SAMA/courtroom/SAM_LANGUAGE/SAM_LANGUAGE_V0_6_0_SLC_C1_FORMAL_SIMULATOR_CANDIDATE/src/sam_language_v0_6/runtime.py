"""Core runtime for the SAM Language v0.6.0 SLC C1 simulator candidate."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
import json
import re
import uuid

from .kernels import earth_orbit_clock_packet

from .errors import (
    AuthorityError,
    ContextRoleError,
    NameResolutionError,
    ParseError,
    ProvenanceCycleError,
    ProvenanceError,
    RawProgramExecutionError,
    SamLanguageError,
    SLCFormalProfileRequired,
    TypeCheckError,
)


PARENT_HASH = "0ee6649ed0c8f863fd5de5ef54e6ce305e1b1c44a0e24a5a4f57c1ef544742d0"
PATCH_PARENT_HASH = "92d216ecba10ebae64e15c0d36514cc08dd3a133138bc95445c395911128021c"
GRANDPARENT_V03_HASH = "81a055c404879611e12c895602f309f97aad5a8d2627414396ef29a321235e39"
CR119_VERDICT = "PASS_TYPED_CLOSURE_HIERARCHY_AND_PROMOTION_LADDER"
PATCH_VERSION = "0.6.0"
IMPLEMENTATION_PARENT_CODE_HASH = "726011b38d27a9b5403a7df66d8d4d5ac7c49960bc331d65f57c66de7a7ecaf0"

CR119_BRANCH = "14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER"
CR005_BRANCH = "03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT"
SOURCE_RECORDS = {
    "parent_v05_release": {
        "path": "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_RELEASE_MANIFEST.json",
        "sha256": "fa15a3d6f81b3a1af1fa59a3fc00ee4fd78094d376d6939f08739e99a0958782",
    },
    "slcx002_operators": {
        "path": "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/release/SLCX002_OPERATOR_MATRICES.json",
        "sha256": "3974aabdc8b9a4dd5edff8cf9030c59aeba641d222871c4e9498ba1b40ea052d",
    },
    "slcx003_operator_lift": {
        "path": "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/release/SLCX003_OPERATOR_LIFT.json",
        "sha256": "26029b0ed3ec02049a73c46215be726df9e698fc15209c823cf64280662444a6",
    },
    "slcx003_formal_grammar": {
        "path": "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/release/SLCX003_12_LEBIT_FORMAL_GRAMMAR.md",
        "sha256": "34f549336a183b4bcc7a6ebe5f468207610b7ee6dd393015aff629590529fb61",
    },
    "slc_c1_contract": {
        "path": "SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json",
        "sha256": "0250471ad673667e8e39527a0de777a2ff7541c3bec5ba4d6f95ad82a27cb3bd",
    },
    "parent_v04_release": {
        "path": "SAM_LANGUAGE_V0_4/SAM_LANGUAGE_V0_4_RELEASE_RECORD.json",
        "sha256": "2d4175819bafeb34986a8e3072b241cc18e6198f0edb7c3dfe3daf506746916e",
    },
    "typed_hierarchy": {
        "path": f"{CR119_BRANCH}/CR119_typed_hierarchy.json",
        "sha256": "ad197382fb2594d32afa56ec936371bf093aa373656088792705343239359228",
    },
    "handoff_contract": {
        "path": f"{CR119_BRANCH}/CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        "sha256": "72fc859df41b277226a5693620ceb711de5b6fd107a8408f5a90ef8eab9dc63c",
    },
    "result": {
        "path": f"{CR119_BRANCH}/CR119_result.md",
        "sha256": "4960244185e251d8a696fbff61afdd6ed4da9a956f24baccdb28e3d80d387208",
    },
    "provenance": {
        "path": f"{CR119_BRANCH}/CR119_provenance.json",
        "sha256": "bb9525a34ed67f07b417cefee31381243a5fd0cf80038cc10132cb6171be8eb6",
    },
    "cr005_runner": {
        "path": f"{CR005_BRANCH}/CR005_runner.py",
        "sha256": "5df0d0076ed89bc54515d692f7008f353b684cf4c2b7ddae929985f50a45e42f",
    },
    "cr005_premises": {
        "path": f"{CR005_BRANCH}/CR005_declared_premises.json",
        "sha256": "10ecccf596584e92cae1825dfb2dca30e7966a7c6f97abb5ea836e6950edbb7b",
    },
    "cr005_summary": {
        "path": f"{CR005_BRANCH}/CR005_summary.json",
        "sha256": "51bccd3cb4653990b598c13137b1448231e74c5711a1f2744df70f99089ab203",
    },
    "qp_grammar_contract": {
        "path": "SAM_LANGUAGE_QP_PARTICLE_GRAMMAR_V1_FROZEN/registry/QP_GRAMMAR_CONTRACT.json",
        "sha256": "a3376a5b2f4f093eff3e40eea792423c97fd3f3d8418051539b505455b267c2a",
    },
    "qp_triad_admissibility": {
        "path": "SAM_LANGUAGE_QP_PARTICLE_GRAMMAR_V1_FROZEN/registry/QP_TRIAD_ADMISSIBILITY.csv",
        "sha256": "1af0edd3351f827602fca6a1a795001124b690a6b4bc3964b7ccb2dc3cd84398",
    },
    "qp_source_reconciliation": {
        "path": "SAM_LANGUAGE_QP_PARTICLE_GRAMMAR_V1_FROZEN/SOURCE_AND_FORMULA_RECONCILIATION.csv",
        "sha256": "2da5201db5c7271621dc52520cf491e9527b4c9fc7853f250a5534e499919983",
    },
    "qp_native_signatures": {
        "path": "15_SCALE_BRIDGE_SIMULATOR/PDG_REVEAL_STAGEB_POST_ASSEMBLY_NATIVE_SIGNATURE_FREEZE/STAGEB_TEMPLATE_NATIVE_SIGNATURES.csv",
        "sha256": "b898869d09e0c3440803626503e76b9ed0108f0b4dd30a28ad16c00e1386410a",
    },
}


@dataclass(frozen=True)
class Authority:
    status: str
    source: str
    note: str = ""


@dataclass(frozen=True)
class Entity:
    entity_id: str
    scalar_value: int | float | Fraction | None
    semantic_type: str
    authority: Authority
    contextual_roles: tuple[str, ...] = ()
    ledger_role: str = "non_ledger"
    metadata: dict[str, object] = field(default_factory=dict, compare=False)
    source_keys: tuple[str, ...] = ("typed_hierarchy", "handoff_contract")
    semantic_scope: str = "CORE"


@dataclass(frozen=True)
class OperatorSignature:
    name: str
    arg_types: tuple[str, ...]
    result_type: str
    result_entity: str | None
    authority: Authority
    structural_only: bool = False
    source_keys: tuple[str, ...] = ("typed_hierarchy", "handoff_contract")
    evaluator: object | None = field(default=None, compare=False, repr=False)
    semantic_scope: str = "CORE"
    required_mode: str | None = None


@dataclass
class LetStatement:
    name: str
    expression: object
    declared_type: str | None = None


@dataclass(frozen=True)
class NameExpression:
    name: str


@dataclass(frozen=True)
class NumberExpression:
    value: float
    source_text: str


@dataclass(frozen=True)
class CallExpression:
    operator: str
    args: tuple[str, ...]


@dataclass(frozen=True)
class ReturnStatement:
    name: str


@dataclass(frozen=True)
class AssertEqualStatement:
    left: str
    right: str


@dataclass(frozen=True)
class RoleStatement:
    entity_name: str
    context: str
    role: str


@dataclass(frozen=True)
class InsertLedgerRowStatement:
    name: str


@dataclass
class Program:
    statements: list[object]
    source_text: str


@dataclass
class CheckedProgram:
    program: Program
    environment: dict[str, Entity]
    return_entity: Entity
    trace: list[dict]
    mode: str = "normal"
    warnings: list[str] = field(default_factory=list)
    context: "ExecutionContext | None" = None


@dataclass
class ExecutionContext:
    """State owned by one checked program and never shared globally."""

    claimed_global_once: set[str] = field(default_factory=set)
    source_keys: list[str] = field(default_factory=list)

    def claim_global_once(self, key: str) -> bool:
        if key in self.claimed_global_once:
            return False
        self.claimed_global_once.add(key)
        return True

    def add_sources(self, *keys: str) -> None:
        for key in keys:
            if key and key not in self.source_keys:
                self.source_keys.append(key)


@dataclass
class ExecutionResult:
    entity_id: str
    scalar_value: int | float | Fraction | None
    semantic_type: str
    authority_status: str
    trace: list[dict]
    source_trace: list[dict]
    warnings: list[str] = field(default_factory=list)
    result_payload: dict[str, object] = field(default_factory=dict)
    semantic_scope: str = "CORE"

    def as_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "scalar_value": _serialize_exact(self.scalar_value),
            "semantic_type": self.semantic_type,
            "authority_status": self.authority_status,
            "semantic_scope": self.semantic_scope,
            "trace": _serialize_exact(self.trace),
            "source_trace": _serialize_exact(self.source_trace),
            "warnings": self.warnings,
            "result_payload": _serialize_exact(self.result_payload),
        }


@dataclass
class Registry:
    entities: dict[str, Entity]
    aliases: dict[str, str]
    operators: dict[str, OperatorSignature]
    allowed_context_roles: dict[tuple[str, str], str]
    open_edges: set[tuple[str, str]]
    forbidden_equalities: set[tuple[str, str]]
    metadata: dict[str, object] = field(default_factory=dict)

    def entity(self, name: str) -> Entity:
        from .errors import UnknownEntityError

        entity_id = self.aliases.get(name, name)
        if entity_id not in self.entities:
            raise UnknownEntityError(f"No registered entity named {name}")
        return self.entities[entity_id]

    def operator(self, name: str) -> OperatorSignature:
        from .errors import UnknownOperatorError

        if name not in self.operators:
            raise UnknownOperatorError(f"No registered operator named {name}")
        return self.operators[name]


def _serialize_exact(value: object) -> object:
    """Recursively serialize exact rationals without changing legacy values."""

    if isinstance(value, Fraction):
        return {"exact": str(value), "decimal": float(value)}
    if isinstance(value, dict):
        return {str(key): _serialize_exact(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_serialize_exact(item) for item in value]
    if isinstance(value, list):
        return [_serialize_exact(item) for item in value]
    return value


def _authority(status: str, note: str = "") -> Authority:
    return Authority(status=status, source="CR119_LANGUAGE_HANDOFF_CONTRACT", note=note)


def _evaluate_earth_orbit_clock(
    args: tuple[Entity, ...], *, context: ExecutionContext | None = None, registry: Registry | None = None
) -> Entity:
    values = [float(arg.scalar_value) for arg in args]
    packet = earth_orbit_clock_packet(
        speed_of_light_m_s=values[0],
        earth_mu_m3_s2=values[1],
        earth_ground_radius_m=values[2],
        orbit_radius_m=values[3],
        nominal_clock_frequency_hz=values[4],
        seconds_per_day=values[5],
    )
    orbit_radius = packet["orbit_radius_m"]
    orbit_token = str(int(orbit_radius)) if orbit_radius.is_integer() else format(orbit_radius, ".15g")
    return Entity(
        entity_id=f"EARTH_ORBIT_CLOCK_PACKET_R{orbit_token}M",
        scalar_value=packet["net_exact_us_day"],
        semantic_type="EarthOrbitClockPacket",
        authority=Authority(
            "ACTIVE",
            f"{CR005_BRANCH}/CR005_runner.py",
            "Calculated with the CR005 equations and caller-supplied inputs",
        ),
        contextual_roles=("circular_earth_orbit_clock_packet",),
        metadata={"result_payload": packet},
        source_keys=("cr005_runner", "cr005_premises"),
    )


def load_registry(
    contract_path: str | Path | None = None,
    *,
    data_dir: str | Path | None = None,
) -> Registry:
    """Load core, QP, and SLC C1 through one ordered registry path."""

    if contract_path is not None:
        path = Path(contract_path)
        if path.is_dir():
            data_dir = path
        elif path.exists():
            json.loads(path.read_text(encoding="utf-8"))
            if path.name == "QP_SOURCE_MANIFEST.json":
                data_dir = path.parent

    entities = {
        "H2_ARITY": Entity("H2_ARITY", 2, "Arity", _authority("ACTIVE"), ("closure_mirror_arity",)),
        "D3_DIMENSION": Entity("D3_DIMENSION", 3, "Dimension", _authority("ACTIVE"), ("spatial_dimension",)),
        "R12_CLOSURE_RADIUS": Entity("R12_CLOSURE_RADIUS", 12, "ClosureRadius", _authority("ACTIVE"), ("closure_radius",)),
        "S8_BINARY_SURFACE": Entity(
            "S8_BINARY_SURFACE", 8, "BinarySurface", _authority("ACTIVE"),
            ("binary_sign_state_surface", "cross_polytope_facet_surface", "release_split_surface"),
        ),
        "X1_AXIS_SELF_CHANNEL": Entity(
            "X1_AXIS_SELF_CHANNEL", 1, "AxisChannel",
            _authority("ACTIVE", "CR267 axis-self / axis-fee channel retained through CR119"),
            ("axis_self_coupling", "axis_fee"),
            metadata={"operator": False, "lift": "NOT_APPLICABLE"},
        ),
        "W9_CLOSURE_WITNESS": Entity(
            "W9_CLOSURE_WITNESS", 9, "ClosureWitness", _authority("ACTIVE"),
            ("resolved_closure_witness",),
        ),
        "THETA18_NATIVE_BUDGET": Entity(
            "THETA18_NATIVE_BUDGET", 18, "NativeClosureBudget", _authority("ACTIVE"),
            ("native_closure_budget",),
        ),
        "V27_VOLUME_CONTAINER": Entity(
            "V27_VOLUME_CONTAINER", 27, "VolumeContainer", _authority("ACTIVE"),
            ("volume_container",),
        ),
        "F81_COMPLETED_FACE": Entity(
            "F81_COMPLETED_FACE", 81, "CompletedFace", _authority("ACTIVE"),
            ("completed_face_capacity",),
        ),
        "P80_PARTICLE_FACE_CONTENT": Entity(
            "P80_PARTICLE_FACE_CONTENT", 80, "ParticleFaceContent",
            _authority("STRUCTURAL_ONLY", "CR283 edge inherited as structural only"),
            ("particle_face_content",), ledger_role="matter_capacity_not_particle_row",
        ),
        "M126_MATTER_CAPACITY": Entity(
            "M126_MATTER_CAPACITY", 126, "MatterCapacity", _authority("ACTIVE"),
            ("retained_matter_capacity",),
        ),
        "N144_NATIVE_CLOSURE": Entity(
            "N144_NATIVE_CLOSURE", 144, "NativeClosure", _authority("ACTIVE"),
            ("native_closure",),
        ),
        "L162_FULL_LEDGER": Entity(
            "L162_FULL_LEDGER", 162, "FullLedger", _authority("ACTIVE"),
            ("closed_ledger",), ledger_role="closed_ledger",
        ),
        "B_CONTACT_OPERATOR": Entity(
            "B_CONTACT_OPERATOR", None, "ContactOperator",
            _authority("ACTIVE", "B/contact to X1 axis-fee witness bridge PASS"),
            ("bow_contact_operator", "non_row_contact_operator"),
            metadata={"acts_through": "X1_AXIS_SELF_CHANNEL", "operator": True},
        ),
        "A_OPERATOR": Entity(
            "A_OPERATOR", None, "AOperator",
            _authority("ACTIVE_IN_SOURCE_SCOPE", "A is active in its sealed scope; A -> B/contact remains OPEN"),
            ("non_row_a_operator",),
            metadata={"relation_to_B": "OPEN", "operator": True},
        ),
        "C1_ROAD_LIGHT_CARRIER": Entity(
            "C1_ROAD_LIGHT_CARRIER", 1, "Carrier", _authority("ACTIVE"),
            ("road_light_carrier", "scalar_one_carrier"), ledger_role="carrier",
            metadata={"lift": "NONE", "historical_alias": "SCALAR_ONE_CARRIER"},
        ),
        "P1_LIFT_BEARING_SUPPORT": Entity(
            "P1_LIFT_BEARING_SUPPORT", 1, "LiftBearingSupport", _authority("ACTIVE"),
            ("lift_bearing_support", "scalar_one_support"), ledger_role="support",
            metadata={"lift_excess": "1/144", "lifted_value": "145/144", "historical_alias": "SCALAR_ONE_SUPPORT"},
        ),
        "A1_HISTORICAL_ROW_PROXY": Entity(
            "A1_HISTORICAL_ROW_PROXY", 1, "HistoricalRowProxy",
            Authority("SUPERSEDED", f"{CR119_BRANCH}/CR119_source_chain", "QP093A-0305 row proxy remains historical and inactive"),
            ("retired_row_proxy",), ledger_role="retired_row",
            metadata={"active_particle_row": False, "superseded_by": "A_OPERATOR"},
            source_keys=("result", "provenance"),
        ),
        "CARRIER8": Entity("CARRIER8", 8, "Carrier", _authority("ACTIVE"), ("carrier_scalar_eight",), ledger_role="carrier"),
        "SUPPORT8": Entity("SUPPORT8", 8, "Support", _authority("ACTIVE"), ("support_scalar_eight",), ledger_role="support"),
        "CARRIER9": Entity("CARRIER9", 9, "Carrier", _authority("ACTIVE"), ("carrier_scalar_nine",), ledger_role="carrier"),
        "SUPPORT9": Entity("SUPPORT9", 9, "Support", _authority("ACTIVE"), ("support_scalar_nine",), ledger_role="support"),
        "SUPPORT12": Entity("SUPPORT12", 12, "Support", _authority("ACTIVE"), ("support_scalar_twelve",), ledger_role="support"),
        "FACE81_ROLE_CLOSURE_CAPACITY": Entity("FACE81_ROLE_CLOSURE_CAPACITY", 81, "CompletedFace", _authority("ACTIVE"), ("closure_capacity_81",)),
        "FACE81_ROLE_COMPLETED_FACE": Entity("FACE81_ROLE_COMPLETED_FACE", 81, "CompletedFace", _authority("ACTIVE"), ("completed_face_81",)),
        "FACE81_ROLE_CONDITIONAL_PARTICLE_EDGE": Entity(
            "FACE81_ROLE_CONDITIONAL_PARTICLE_EDGE", 81, "CompletedFace",
            _authority("STRUCTURAL_ONLY", "distinct 81 role occurrence inherited with P80 edge"),
            ("conditional_particle_edge_81",),
        ),
    }
    aliases = {key: key for key in entities}
    aliases.update(
        {
            "h": "H2_ARITY", "H2": "H2_ARITY",
            "D": "D3_DIMENSION", "D3": "D3_DIMENSION",
            "R": "R12_CLOSURE_RADIUS", "R12": "R12_CLOSURE_RADIUS",
            "S": "S8_BINARY_SURFACE", "S8": "S8_BINARY_SURFACE",
            "X": "X1_AXIS_SELF_CHANNEL", "X1": "X1_AXIS_SELF_CHANNEL",
            "W": "W9_CLOSURE_WITNESS", "W9": "W9_CLOSURE_WITNESS",
            "Theta": "THETA18_NATIVE_BUDGET", "V": "V27_VOLUME_CONTAINER",
            "F": "F81_COMPLETED_FACE", "P": "P80_PARTICLE_FACE_CONTENT",
            "M": "M126_MATTER_CAPACITY", "N": "N144_NATIVE_CLOSURE",
            "L": "L162_FULL_LEDGER", "B": "B_CONTACT_OPERATOR", "A": "A_OPERATOR",
            "SCALAR_ONE_CARRIER": "C1_ROAD_LIGHT_CARRIER",
            "SCALAR_ONE_SUPPORT": "P1_LIFT_BEARING_SUPPORT",
            "HISTORICAL_A_FIELD_ROW_PROXY": "A1_HISTORICAL_ROW_PROXY",
        }
    )
    operators = {
        "RESOLVE": OperatorSignature(
            "RESOLVE", ("BinarySurface", "ContactOperator", "AxisChannel"),
            "ClosureWitness", "W9_CLOSURE_WITNESS",
            _authority("ACTIVE", "B/contact -> X1 axis-fee -> W9 PASS"),
        ),
        "PROMOTE_VOLUME": OperatorSignature(
            "PROMOTE_VOLUME", ("ClosureWitness", "Dimension"),
            "VolumeContainer", "V27_VOLUME_CONTAINER", _authority("ACTIVE"),
        ),
        "PROMOTE_FACE": OperatorSignature(
            "PROMOTE_FACE", ("VolumeContainer", "Dimension"),
            "CompletedFace", "F81_COMPLETED_FACE", _authority("ACTIVE"),
        ),
        "MIRROR_CLOSE": OperatorSignature(
            "MIRROR_CLOSE", ("CompletedFace", "Arity"),
            "FullLedger", "L162_FULL_LEDGER", _authority("ACTIVE"),
        ),
        "RETAIN_MATTER": OperatorSignature(
            "RETAIN_MATTER", ("NativeClosureBudget", "PrimaryCarrier"),
            "MatterCapacity", "M126_MATTER_CAPACITY", _authority("ACTIVE"),
        ),
        "RESERVE_CLOSURE_ADDRESS": OperatorSignature(
            "RESERVE_CLOSURE_ADDRESS", ("CompletedFace", "AxisChannel"),
            "ParticleFaceContent", "P80_PARTICLE_FACE_CONTENT",
            _authority("STRUCTURAL_ONLY", "P80 is conditional structural-only"), structural_only=True,
        ),
        "EARTH_ORBIT_CLOCK": OperatorSignature(
            "EARTH_ORBIT_CLOCK",
            ("Number", "Number", "Number", "Number", "Number", "Number"),
            "EarthOrbitClockPacket",
            None,
            Authority(
                "ACTIVE",
                f"{CR005_BRANCH}/CR005_runner.py",
                "Parameterized circular Earth-orbit clock calculation from CR005",
            ),
            source_keys=("cr005_runner", "cr005_premises"),
            evaluator=_evaluate_earth_orbit_clock,
        ),
    }
    allowed_context_roles = {
        ("S8_BINARY_SURFACE", "binary_sign_state_surface"): "BinarySurface",
        ("S8_BINARY_SURFACE", "cross_polytope_facet_surface"): "BinarySurface",
        ("S8_BINARY_SURFACE", "release_split_surface"): "BinarySurface",
        ("F81_COMPLETED_FACE", "completed_face_capacity"): "CompletedFace",
        ("FACE81_ROLE_CLOSURE_CAPACITY", "closure_capacity_81"): "CompletedFace",
        ("FACE81_ROLE_COMPLETED_FACE", "completed_face_81"): "CompletedFace",
        ("FACE81_ROLE_CONDITIONAL_PARTICLE_EDGE", "conditional_particle_edge_81"): "CompletedFace",
        ("THETA18_NATIVE_BUDGET", "native_closure_budget"): "NativeClosureBudget",
    }
    open_edges = {("A_OPERATOR", "B_CONTACT_OPERATOR")}
    forbidden_equalities = {
        ("A_OPERATOR", "B_CONTACT_OPERATOR"),
        ("B_CONTACT_OPERATOR", "X1_AXIS_SELF_CHANNEL"),
    }
    registry = Registry(entities, aliases, operators, allowed_context_roles, open_edges, forbidden_equalities)
    from .registry_qp import extend_registry as extend_qp
    from .registry_slc import extend_registry as extend_slc

    return extend_slc(extend_qp(registry, data_dir=data_dir))

def registry_payload() -> dict:
    registry = load_registry()
    return {
        "patch_version": PATCH_VERSION,
        "implementation_parent_code_hash": IMPLEMENTATION_PARENT_CODE_HASH,
        "parent_hash": PARENT_HASH,
        "patch_parent_hash": PATCH_PARENT_HASH,
        "grandparent_v03_hash": GRANDPARENT_V03_HASH,
        "cr119_verdict": CR119_VERDICT,
        "entities": {k: _entity_payload(v) for k, v in registry.entities.items()},
        "aliases": dict(sorted(registry.aliases.items())),
        "operators": {
            k: {
                "arg_types": list(v.arg_types),
                "result_type": v.result_type,
                "result_entity": v.result_entity,
                "authority": v.authority.__dict__,
                "structural_only": v.structural_only,
                "semantic_scope": v.semantic_scope,
                "computed": v.evaluator is not None,
                "required_mode": v.required_mode,
                "sources": _source_payload(v.source_keys),
            }
            for k, v in registry.operators.items()
        },
        "allowed_context_roles": [
            {"entity_id": k[0], "contextual_role": k[1], "semantic_type": v}
            for k, v in sorted(registry.allowed_context_roles.items())
        ],
        "open_edges": [list(edge) for edge in sorted(registry.open_edges)],
        "forbidden_equalities": [list(edge) for edge in sorted(registry.forbidden_equalities)],
        "source_records": SOURCE_RECORDS,
        "metadata": _serialize_exact(
            {key: value for key, value in registry.metadata.items() if key != "qp_data_dir"}
        ),
        "open_operators": list(registry.metadata.get("open_operators", [])),
    }


def _source_payload(source_keys: tuple[str, ...]) -> list[dict]:
    return [dict(SOURCE_RECORDS[key], source_key=key) for key in source_keys if key in SOURCE_RECORDS]


def _entity_payload(entity: Entity) -> dict:
    return {
        "entity_id": entity.entity_id,
        "scalar_value": _serialize_exact(entity.scalar_value),
        "semantic_type": entity.semantic_type,
        "authority": entity.authority.__dict__,
        "contextual_roles": list(entity.contextual_roles),
        "ledger_role": entity.ledger_role,
        "metadata": _serialize_exact(dict(entity.metadata)),
        "semantic_scope": entity.semantic_scope,
        "sources": _source_payload(entity.source_keys),
    }


def entity_trace(name: str) -> dict:
    """Return a symbol-qualified entity trace without treating the name as a file."""
    registry = load_registry()
    entity = registry.entity(name)
    payload = _entity_payload(entity)
    payload["requested_name"] = name
    payload["canonical_entity_id"] = entity.entity_id
    payload["derivation_trace"] = _derivation_trace(entity.entity_id)
    return payload


def _derivation_trace(entity_id: str) -> list[str]:
    traces = {
        "S8_BINARY_SURFACE": ["H2^D3 -> S8"],
        "X1_AXIS_SELF_CHANNEL": ["D3^(D3-1) - S8 -> X1"],
        "W9_CLOSURE_WITNESS": ["S8 --B through X1--> W9"],
        "THETA18_NATIVE_BUDGET": ["H2 * W9 -> Theta18", "R12^2 / S8 -> Theta18"],
        "V27_VOLUME_CONTAINER": ["S8 --B through X1--> W9", "W9 * D3 -> V27"],
        "F81_COMPLETED_FACE": ["S8 --B through X1--> W9", "W9 * D3 -> V27", "V27 * D3 -> F81"],
        "P80_PARTICLE_FACE_CONTENT": ["F81 - X1 -> P80 [STRUCTURAL_ONLY]"],
        "M126_MATTER_CAPACITY": ["N144 - Theta18 -> M126", "(S8 - X1) * Theta18 -> M126"],
        "N144_NATIVE_CLOSURE": ["R12^2 -> N144", "S8 * Theta18 -> N144"],
        "L162_FULL_LEDGER": [
            "S8 --B through X1--> W9",
            "W9 * D3 -> V27",
            "V27 * D3 -> F81",
            "F81 * H2 -> L162",
        ],
        "B_CONTACT_OPERATOR": ["B_CONTACT_OPERATOR acts through X1_AXIS_SELF_CHANNEL", "B_CONTACT_OPERATOR != X1_AXIS_SELF_CHANNEL"],
        "A_OPERATOR": ["A_OPERATOR active in its sealed source scope", "A_OPERATOR -> B_CONTACT_OPERATOR remains OPEN"],
        "C1_ROAD_LIGHT_CARRIER": ["scalar address 1; carrier occurrence; no local support lift"],
        "P1_LIFT_BEARING_SUPPORT": ["scalar address 1; support occurrence", "lift excess = 1/144", "lifted value = 145/144"],
        "A1_HISTORICAL_ROW_PROXY": ["QP093A-0305 historical scalar-one row proxy", "SUPERSEDED by A_OPERATOR", "active_particle_row = false"],
    }
    return list(traces.get(entity_id, [f"{entity_id} is a registered typed occurrence"]))


def explain_operator(name: str) -> dict:
    registry = load_registry()
    op = registry.operator(name)
    return {
        "operator_id": op.name,
        "signature": {
            "arg_types": list(op.arg_types),
            "result_type": op.result_type,
            "result_entity": op.result_entity,
            "computed": op.evaluator is not None,
            "required_mode": op.required_mode,
        },
        "authority": op.authority.__dict__,
        "structural_only": op.structural_only,
        "semantic_scope": op.semantic_scope,
        "sources": _source_payload(op.source_keys),
        "notes": {
            "B_is_not_X1": True if op.name == "RESOLVE" else None,
            "A_to_B_relation": "OPEN" if op.name == "RESOLVE" else None,
        },
    }


def sources_for_entity(name: str) -> dict:
    registry = load_registry()
    entity = registry.entity(name)
    return {
        "requested_name": name,
        "canonical_entity_id": entity.entity_id,
        "sources": _source_payload(entity.source_keys),
    }


def sources_for_operator(name: str) -> dict:
    registry = load_registry()
    operator = registry.operator(name)
    return {
        "operator_id": operator.name,
        "semantic_scope": operator.semantic_scope,
        "sources": _source_payload(operator.source_keys),
    }

def parse_program(source_text: str) -> Program:
    statements: list[object] = []
    for statement in _split_statements(source_text):
        if statement.startswith("let "):
            statements.append(_parse_let(statement))
        elif statement.startswith("return "):
            statements.append(ReturnStatement(statement[len("return ") :].strip()))
        elif statement.startswith("assert "):
            match = re.fullmatch(r"assert\s+([A-Za-z0-9_]+)\s*==\s*([A-Za-z0-9_]+)", statement)
            if not match:
                raise ParseError(f"Unsupported assertion syntax: {statement}")
            statements.append(AssertEqualStatement(match.group(1), match.group(2)))
        elif statement.startswith("ROLE "):
            match = re.fullmatch(r"ROLE\s+([A-Za-z0-9_]+)@([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)", statement)
            if not match:
                raise ParseError(f"Unsupported role syntax: {statement}")
            statements.append(RoleStatement(match.group(1), match.group(2), match.group(3)))
        elif statement.startswith("INSERT_LEDGER_ROW("):
            match = re.fullmatch(r"INSERT_LEDGER_ROW\(([A-Za-z0-9_]+)\)", statement)
            if not match:
                raise ParseError(f"Unsupported ledger insertion syntax: {statement}")
            statements.append(InsertLedgerRowStatement(match.group(1)))
        else:
            raise ParseError(f"Unsupported statement: {statement}")
    if not any(isinstance(stmt, ReturnStatement) for stmt in statements):
        raise ParseError("Program must contain a return statement")
    return Program(statements=statements, source_text=source_text)


def _split_statements(source_text: str) -> list[str]:
    cleaned: list[str] = []
    buffer = ""
    depth = 0
    for raw_line in source_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if buffer:
            buffer += " " + line
        else:
            buffer = line
        depth += line.count("(") - line.count(")")
        if depth == 0:
            cleaned.append(buffer.strip())
            buffer = ""
    if buffer:
        raise ParseError("Unbalanced call expression")
    return cleaned


def _parse_let(statement: str) -> LetStatement:
    match = re.fullmatch(r"let\s+([A-Za-z0-9_]+)(?::\s*([A-Za-z0-9_]+))?\s*=\s*(.+)", statement)
    if not match:
        raise ParseError(f"Unsupported let syntax: {statement}")
    name, declared_type, expression_text = match.groups()
    expression_text = expression_text.strip()
    number = re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", expression_text)
    call = re.fullmatch(r"([A-Z][A-Z0-9_]*)\((.*)\)", expression_text)
    if call:
        args = tuple(part.strip() for part in call.group(2).split(",") if part.strip())
        expression = CallExpression(call.group(1), args)
    elif number:
        expression = NumberExpression(float(expression_text), expression_text)
    else:
        expression = NameExpression(expression_text)
    return LetStatement(name=name, declared_type=declared_type, expression=expression)


VALID_EXECUTION_MODES = {"normal", "research", "slc-c1-formal"}


def check_program(program: Program, *, mode: str = "normal", registry: Registry | None = None) -> CheckedProgram:
    if mode not in VALID_EXECUTION_MODES:
        raise AuthorityError(
            f"Unknown execution mode {mode!r}; expected one of {sorted(VALID_EXECUTION_MODES)}"
        )
    registry = registry or load_registry()
    context = ExecutionContext()
    env: dict[str, Entity] = {}
    trace: list[dict] = []
    warnings: list[str] = []
    return_entity: Entity | None = None

    for stmt in program.statements:
        if isinstance(stmt, LetStatement):
            entity = _check_let(stmt, env, registry, mode, warnings, trace, context)
            env[stmt.name] = entity
        elif isinstance(stmt, ReturnStatement):
            return_entity = _resolve_symbol(stmt.name, env, registry)
        elif isinstance(stmt, AssertEqualStatement):
            _check_assert_equal(stmt, env, registry)
            trace.append({"stage": "authority", "assert_equal": [stmt.left, stmt.right], "status": "PASS"})
        elif isinstance(stmt, RoleStatement):
            _check_role(stmt, env, registry)
            trace.append({"stage": "contextual_role", "entity": stmt.entity_name, "context": stmt.context, "status": "PASS"})
        elif isinstance(stmt, InsertLedgerRowStatement):
            _check_insert_ledger_row(stmt, env, registry)
        else:
            raise TypeCheckError(f"Unsupported AST node: {type(stmt).__name__}")

    if return_entity is None:
        raise TypeCheckError("Checked program has no return entity")
    context.add_sources(*return_entity.source_keys)
    return CheckedProgram(
        program=program,
        environment=env,
        return_entity=return_entity,
        trace=trace,
        mode=mode,
        warnings=warnings,
        context=context,
    )


def _check_let(
    stmt: LetStatement,
    env: dict[str, Entity],
    registry: Registry,
    mode: str,
    warnings: list[str],
    trace: list[dict],
    context: ExecutionContext,
) -> Entity:
    from .type_system import is_assignable, known_qp_types, known_slc_types

    known_types = {e.semantic_type for e in registry.entities.values()}
    known_types.update(op.result_type for op in registry.operators.values())
    known_types.add("Number")
    known_types.update(known_qp_types())
    known_types.update(known_slc_types())
    if stmt.declared_type and stmt.declared_type not in known_types:
        raise TypeCheckError(f"Unknown type: {stmt.declared_type}")
    if isinstance(stmt.expression, NumberExpression):
        if stmt.declared_type and not is_assignable("Number", stmt.declared_type):
            raise TypeCheckError(
                f"Declared type {stmt.declared_type} does not match numeric literal:Number"
            )
        entity = Entity(
            entity_id=f"NUMBER_LITERAL_{stmt.name}",
            scalar_value=stmt.expression.value,
            semantic_type="Number",
            authority=Authority("ACTIVE", "SAM_SOURCE_LITERAL"),
            metadata={"source_text": stmt.expression.source_text},
            source_keys=(),
        )
        trace.append(
            {
                "stage": "literal_resolution",
                "name": stmt.name,
                "semantic_type": "Number",
                "value": stmt.expression.value,
                "status": "PASS",
            }
        )
        return entity
    if isinstance(stmt.expression, NameExpression):
        entity = _resolve_symbol(stmt.expression.name, env, registry)
        _validate_authority_for_use(entity)
        if stmt.declared_type and not is_assignable(entity.semantic_type, stmt.declared_type):
            raise TypeCheckError(
                f"Declared type {stmt.declared_type} does not match {entity.entity_id}:{entity.semantic_type}"
            )
        trace.append({"stage": "name_resolution", "name": stmt.name, "entity_id": entity.entity_id, "status": "PASS"})
        return entity
    if isinstance(stmt.expression, CallExpression):
        signature = registry.operator(stmt.expression.operator)
        args = tuple(_resolve_symbol(arg, env, registry) for arg in stmt.expression.args)
        if len(args) != len(signature.arg_types):
            raise TypeCheckError(
                f"{signature.name} expected {len(signature.arg_types)} args, found {len(args)}"
            )
        found_types = tuple(arg.semantic_type for arg in args)
        if not all(is_assignable(actual, expected) for actual, expected in zip(found_types, signature.arg_types)):
            raise TypeCheckError(
                f"{signature.name} expects {signature.arg_types}, found {found_types}"
            )
        for arg in args:
            _validate_authority_for_use(arg)
        if signature.authority.status == "OPEN":
            raise AuthorityError(f"{signature.name} has OPEN authority")
        if signature.required_mode is not None and mode != signature.required_mode:
            raise SLCFormalProfileRequired(
                f"{signature.name} requires --slc-c1-formal"
            )
        if signature.structural_only and mode != "research":
            raise AuthorityError(f"{signature.name} is STRUCTURAL_ONLY and requires --research")
        if signature.evaluator is not None:
            try:
                result = signature.evaluator(args, context=context, registry=registry)
            except SamLanguageError:
                raise
            except (ArithmeticError, ValueError) as exc:
                raise TypeCheckError(f"{signature.name} calculation failed: {exc}") from exc
        else:
            if signature.result_entity is None:
                raise TypeCheckError(f"{signature.name} has no result entity or evaluator")
            result = registry.entity(signature.result_entity)
        if result.authority.status == "STRUCTURAL_ONLY" and mode == "research":
            warnings.append(f"{result.entity_id} is STRUCTURAL_ONLY; no particle row is activated")
        elif result.authority.status == "FORMAL_CANDIDATE" and mode == "slc-c1-formal":
            pass
        elif result.authority.status != "ACTIVE":
            raise AuthorityError(f"{result.entity_id} has authority status {result.authority.status}")
        trace.append(
            {
                "stage": "typed_execution_plan",
                "operator": signature.name,
                "args": [arg.entity_id for arg in args],
                "result_entity": result.entity_id,
                "computed": signature.evaluator is not None,
                "computed_scalar_value": result.scalar_value,
                "status": "PASS",
            }
        )
        context.add_sources(*signature.source_keys)
        for arg in args:
            context.add_sources(*arg.source_keys)
        context.add_sources(*result.source_keys)
        return result
    raise TypeCheckError(f"Unsupported let expression: {stmt.expression!r}")


def _resolve_symbol(name: str, env: dict[str, Entity], registry: Registry) -> Entity:
    if name in env:
        return env[name]
    return registry.entity(name)


def _validate_authority_for_use(entity: Entity) -> None:
    if entity.authority.status == "OPEN":
        raise AuthorityError(f"{entity.entity_id} has OPEN authority and cannot be used authoritatively")
    if entity.authority.status == "CONFLICT":
        raise AuthorityError(f"{entity.entity_id} has CONFLICT authority and cannot be used authoritatively")
    if entity.authority.status in {"RETIRED", "SUPERSEDED"}:
        raise AuthorityError(
            f"{entity.entity_id} is {entity.authority.status} and cannot be used as an active row"
        )


def _canonical_pair(left: Entity, right: Entity) -> tuple[str, str]:
    return tuple(sorted((left.entity_id, right.entity_id)))


def _check_assert_equal(stmt: AssertEqualStatement, env: dict[str, Entity], registry: Registry) -> None:
    left = _resolve_symbol(stmt.left, env, registry)
    right = _resolve_symbol(stmt.right, env, registry)
    pair = _canonical_pair(left, right)
    forbidden = {tuple(sorted(edge)) for edge in registry.forbidden_equalities | registry.open_edges}
    if pair in forbidden:
        raise AuthorityError(f"Equality is not authorized for {left.entity_id} and {right.entity_id}")
    if left.entity_id != right.entity_id:
        raise AuthorityError(
            f"Scalar equality is insufficient: {left.entity_id}:{left.semantic_type} != "
            f"{right.entity_id}:{right.semantic_type}"
        )


def _check_role(stmt: RoleStatement, env: dict[str, Entity], registry: Registry) -> None:
    entity = _resolve_symbol(stmt.entity_name, env, registry)
    key = (entity.entity_id, stmt.context)
    if key not in registry.allowed_context_roles:
        raise ContextRoleError(
            f"Unsupported contextual role {stmt.role} for {entity.entity_id}@{stmt.context}"
        )
    expected_type = registry.allowed_context_roles[key]
    if entity.semantic_type != expected_type:
        raise ContextRoleError(
            f"Role {stmt.context} expects {expected_type}, found {entity.semantic_type}"
        )


def _check_insert_ledger_row(stmt: InsertLedgerRowStatement, env: dict[str, Entity], registry: Registry) -> None:
    entity = _resolve_symbol(stmt.name, env, registry)
    if entity.semantic_type in {"AOperator", "ContactOperator", "AxisChannel"}:
        raise AuthorityError(f"{entity.entity_id} cannot be inserted as a ledger row")
    if entity.ledger_role in {"non_ledger", "retired_row", "matter_capacity_not_particle_row"}:
        raise AuthorityError(f"{entity.entity_id} is not an active particle ledger row")


def execute_checked(checked: CheckedProgram | Program) -> ExecutionResult:
    if isinstance(checked, Program):
        raise RawProgramExecutionError("Raw parsed Program cannot execute; run check_program first")
    entity = checked.return_entity
    context_keys = tuple(checked.context.source_keys) if checked.context is not None else ()
    source_keys = tuple(dict.fromkeys(("parent_v05_release",) + context_keys + entity.source_keys))
    source_trace = _source_payload(source_keys)
    trace = checked.trace + [
        {
            "stage": "execution",
            "entity_id": entity.entity_id,
            "scalar_value": entity.scalar_value,
            "semantic_type": entity.semantic_type,
            "status": "PASS",
        }
    ]
    return ExecutionResult(
        entity_id=entity.entity_id,
        scalar_value=entity.scalar_value,
        semantic_type=entity.semantic_type,
        authority_status=entity.authority.status,
        trace=trace,
        source_trace=source_trace,
        warnings=list(checked.warnings),
        result_payload=dict(entity.metadata.get("result_payload", {})),
        semantic_scope=entity.semantic_scope,
    )


def run_program_text(source_text: str, *, mode: str = "normal") -> ExecutionResult:
    program = parse_program(source_text)
    checked = check_program(program, mode=mode)
    return execute_checked(checked)


class ProvenanceStore:
    """Append-only provenance store for v0.4 validation."""

    def __init__(self):
        self.records: list[dict] = []
        self.dependencies: dict[str, set[str]] = {}

    def add_assertion(
        self,
        entity_id: str,
        predicate: str,
        value: object,
        *,
        source_id: str,
        supersedes: str | None = None,
    ) -> dict:
        if supersedes is not None and not any(record["id"] == supersedes for record in self.records):
            raise ProvenanceError(f"Supersession target not found: {supersedes}")
        prior = [
            record
            for record in self.records
            if record["entity_id"] == entity_id and record["predicate"] == predicate and record["status"] != "CONFLICT"
        ]
        if supersedes is None:
            incompatible = [record for record in prior if record["value"] != value]
            if incompatible:
                conflict = self._record(
                    entity_id,
                    predicate,
                    value,
                    source_id=source_id,
                    status="CONFLICT",
                    conflicts_with=[record["id"] for record in incompatible],
                    supersedes=None,
                )
                return conflict
        return self._record(
            entity_id,
            predicate,
            value,
            source_id=source_id,
            status="ACTIVE",
            conflicts_with=[],
            supersedes=supersedes,
        )

    def _record(
        self,
        entity_id: str,
        predicate: str,
        value: object,
        *,
        source_id: str,
        status: str,
        conflicts_with: list[str],
        supersedes: str | None,
    ) -> dict:
        record = {
            "id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"{len(self.records)}:{entity_id}:{predicate}:{source_id}:{value}")),
            "entity_id": entity_id,
            "predicate": predicate,
            "value": value,
            "source_id": source_id,
            "status": status,
            "conflicts_with": conflicts_with,
            "supersedes": supersedes,
        }
        self.records.append(record)
        return record

    def add_dependency(self, source: str, depends_on: str) -> None:
        graph = {key: set(value) for key, value in self.dependencies.items()}
        graph.setdefault(source, set()).add(depends_on)
        cycle = _find_cycle(graph)
        if cycle:
            raise ProvenanceCycleError(cycle)
        self.dependencies = graph

    def as_dict(self) -> dict:
        return {
            "records": list(self.records),
            "dependencies": {key: sorted(value) for key, value in sorted(self.dependencies.items())},
        }


def _find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def walk(node: str) -> list[str] | None:
        if node in visiting:
            start = visiting.index(node)
            return visiting[start:] + [node]
        if node in visited:
            return None
        visiting.append(node)
        for neighbor in sorted(graph.get(node, ())):
            cycle = walk(neighbor)
            if cycle:
                return cycle
        visiting.pop()
        visited.add(node)
        return None

    for root in sorted(graph):
        cycle = walk(root)
        if cycle:
            return cycle
    return None


VALID_CLOSURE_PROGRAM = """
let w = RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)
let v = PROMOTE_VOLUME(w, D3_DIMENSION)
let f = PROMOTE_FACE(v, D3_DIMENSION)
let l = MIRROR_CLOSE(f, H2_ARITY)
return l
""".strip()
