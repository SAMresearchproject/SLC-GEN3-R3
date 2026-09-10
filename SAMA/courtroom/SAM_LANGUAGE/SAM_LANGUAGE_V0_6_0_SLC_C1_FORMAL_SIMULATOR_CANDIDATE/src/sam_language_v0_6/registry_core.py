"""Inherited core-registry view within the combined v0.5 registry."""

from .runtime import load_registry


def core_registry_snapshot() -> dict[str, object]:
    registry = load_registry()
    return {
        "entities": {
            key: value
            for key, value in registry.entities.items()
            if value.semantic_scope == "CORE"
        },
        "operators": {
            key: value
            for key, value in registry.operators.items()
            if value.semantic_scope == "CORE"
        },
    }


__all__ = ["core_registry_snapshot"]
