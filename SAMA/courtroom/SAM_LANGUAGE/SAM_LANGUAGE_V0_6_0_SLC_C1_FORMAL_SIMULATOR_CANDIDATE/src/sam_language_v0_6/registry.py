"""Combined deterministic core, QP, and formal SLC C1 registry API."""

from .registry_qp import (
    enumerate_qp_productions,
    grammar_census,
    inspect_qp_production,
    verify_qp_native_inverse,
    verify_qp_native_reconciliation,
    verify_qp_source_reconciliation,
)
from .runtime import (
    entity_trace,
    explain_operator,
    load_registry,
    registry_payload,
    sources_for_entity,
    sources_for_operator,
)

__all__ = [
    "entity_trace",
    "enumerate_qp_productions",
    "explain_operator",
    "grammar_census",
    "inspect_qp_production",
    "load_registry",
    "registry_payload",
    "sources_for_entity",
    "sources_for_operator",
    "verify_qp_native_inverse",
    "verify_qp_native_reconciliation",
    "verify_qp_source_reconciliation",
]
