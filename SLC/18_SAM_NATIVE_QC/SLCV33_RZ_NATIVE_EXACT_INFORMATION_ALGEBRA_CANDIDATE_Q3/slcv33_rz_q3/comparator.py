"""Installed frozen SLCQ2-RZ continuity comparator."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

from .canonical import file_sha256
from .source import REPOSITORY_ROOT, SourceVisibleChoice


CURRENT_Q2_ROOT = REPOSITORY_ROOT / "SLC/18_SAM_NATIVE_QC/SLCQ2_RZ_CURRENT_REVISION_V1"
CURRENT_Q2_RUNTIME = CURRENT_Q2_ROOT / "slcq2_rz_current.py"
EXPECTED_CURRENT_Q2_RUNTIME_SHA256 = "62a4e4ae90a86e9e83f2dba631d4252fe392ffb1cb95c3c8799ff497845f65a8"


class ComparatorError(RuntimeError):
    """The installed frozen Q2 comparator bytes or model differ."""


def load_q2_current_model():
    if file_sha256(CURRENT_Q2_RUNTIME) != EXPECTED_CURRENT_Q2_RUNTIME_SHA256:
        raise ComparatorError("installed frozen Q2 runtime bytes differ")
    if str(CURRENT_Q2_ROOT) not in sys.path:
        sys.path.insert(0, str(CURRENT_Q2_ROOT))
    from slcq2_rz_current import load_frozen_model  # noqa: PLC0415

    return load_frozen_model()


def score_q2_current(
    query: SourceVisibleChoice,
    candidate: SourceVisibleChoice,
    *,
    model=None,
) -> tuple[Fraction, ...]:
    frozen = model or load_q2_current_model()
    if str(CURRENT_Q2_ROOT) not in sys.path:
        sys.path.insert(0, str(CURRENT_Q2_ROOT))
    from slcq2_rz_current import score  # noqa: PLC0415

    return score(query, candidate, model=frozen)
