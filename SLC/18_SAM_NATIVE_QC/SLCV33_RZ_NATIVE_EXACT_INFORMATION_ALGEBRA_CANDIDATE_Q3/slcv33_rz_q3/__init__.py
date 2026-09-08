"""Candidate-owned exact Q3 representation and ranking implementation.

The package is intentionally noninstalling.  It reads frozen predecessors,
never mutates them, and keeps CONTROL target access behind the sealed ICF1
foundation binding and winner-lock gates.
"""

from .binding import FoundationBindingError, require_sealed_icf1_binding
from .features import FEATURE_SCHEMAS, Representation, derive_representation
from .source import Q3Inventory, load_frozen_q2_inventory

__all__ = (
    "FEATURE_SCHEMAS",
    "FoundationBindingError",
    "Q3Inventory",
    "Representation",
    "derive_representation",
    "load_frozen_q2_inventory",
    "require_sealed_icf1_binding",
)
