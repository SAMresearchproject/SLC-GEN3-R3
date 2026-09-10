"""Single audited type-assignability relation for SAM Language v0.6."""

from __future__ import annotations

from functools import lru_cache


TYPE_PARENTS: dict[str, tuple[str, ...]] = {
    "QPTemplate": ("QPGrammarProduction",),
    "QPUnaryTemplate": ("QPTemplate",),
    "QPRelationTemplate": ("QPTemplate",),
    "QPInfrastructure": ("QPGrammarProduction",),
    "QPGlobalProduction": ("QPGrammarProduction",),
    "QPRejectedProduction": ("QPGrammarProduction",),
    "QPUnaryDirectTemplate": ("QPUnaryTemplate",),
    "QPUnaryConjugateTemplate": ("QPUnaryTemplate",),
    "QPOrderedPairTemplate": ("QPRelationTemplate",),
    "QPUnorderedTriadCandidate": ("QPRelationTemplate",),
    "QPLocalTriadTemplate": ("QPRelationTemplate",),
    "QPRejectedConstruction": ("QPRejectedProduction",),
    "QPHiddenSupport": ("QPInfrastructure",),
    "QPCarrierInfrastructure": ("QPInfrastructure",),
    "QPGlobalScalarParent": ("QPGlobalProduction",),
    "QPSurfaceDebitOrCredit": ("QPExactAccount",),
    "QPObservedCandidateAccount": ("QPExactAccount",),
    "QPSourceSupport": ("QPExactAccount",),
    "QPTensorCarrierSupport": ("QPExactAccount",),
    "QPRetainedWriteSupport": ("QPExactAccount",),
    "SLCState12": ("SLCRegisterState",),
    "SLCStateInspection": ("SLCFormalReadout",),
}

QP_LEAF_TYPES = {
    "QPPartitionLabel",
    "QPDepth",
    "QPRouteMode",
    "QPCarrierTerminalName",
    "QPControlName",
    "QPGrammarProduction",
    "QPTemplate",
    "QPUnaryTemplate",
    "QPRelationTemplate",
    "QPInfrastructure",
    "QPGlobalProduction",
    "QPRejectedProduction",
    "QPUnaryDirectTemplate",
    "QPUnaryConjugateTemplate",
    "QPOrderedPairTemplate",
    "QPUnorderedTriadCandidate",
    "QPLocalTriadTemplate",
    "QPRejectedConstruction",
    "QPHiddenSupport",
    "QPCarrierInfrastructure",
    "QPGlobalScalarParent",
    "QPNativeSignature",
    "QPExactAccount",
    "QPSurfaceDebitOrCredit",
    "QPObservedCandidateAccount",
    "QPSourceSupport",
    "QPTensorCarrierSupport",
    "QPRetainedWriteSupport",
}

SLC_LEAF_TYPES = {
    "SLCLebitSite",
    "SLCRegisterState",
    "SLCState12",
    "SLCFormalReadout",
    "SLCStateInspection",
}


@lru_cache(maxsize=None)
def _ancestors(actual_type: str) -> frozenset[str]:
    result = {actual_type}
    for parent in TYPE_PARENTS.get(actual_type, ()):
        result.update(_ancestors(parent))
    return frozenset(result)


def is_assignable(actual_type: str, expected_type: str) -> bool:
    """Return whether ``actual_type`` may fill ``expected_type``.

    This relation affects type checking only.  It never aliases values,
    authorities, occurrences, or same-scalar entities.
    """

    return expected_type in _ancestors(actual_type)


def known_qp_types() -> set[str]:
    return set(QP_LEAF_TYPES) | set(TYPE_PARENTS) | {
        parent for parents in TYPE_PARENTS.values() for parent in parents
    }


def known_slc_types() -> set[str]:
    return set(SLC_LEAF_TYPES) | {
        key for key in TYPE_PARENTS if key.startswith("SLC")
    } | {
        parent
        for key, parents in TYPE_PARENTS.items()
        if key.startswith("SLC")
        for parent in parents
    }


def hierarchy_payload() -> dict[str, object]:
    return {
        "relation": "TYPE_CHECKING_ONLY",
        "parents": {key: list(value) for key, value in sorted(TYPE_PARENTS.items())},
        "known_qp_types": sorted(known_qp_types()),
        "known_slc_types": sorted(known_slc_types()),
        "non_identity_guarantee": True,
    }
