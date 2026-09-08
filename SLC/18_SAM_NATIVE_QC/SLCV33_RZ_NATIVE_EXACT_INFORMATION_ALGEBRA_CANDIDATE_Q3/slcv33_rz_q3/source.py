"""Frozen Q2 source inventory admission and target-blind Q3 split."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
import gzip
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping

from .canonical import canonical_sha256, file_sha256, load_exact_json, validate_semantic_seal


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
Q1_ROOT = REPOSITORY_ROOT / "SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q1"
Q2_ROOT = REPOSITORY_ROOT / "SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q2"
Q2_SPLIT_MANIFEST = Q2_ROOT / "preexecution/Q2_GROUP_SPLIT_MANIFEST.json"
EXPECTED_Q2_SPLIT_FILE_SHA256 = "e52b0930c2a0a32aaffa96281bf6c084d55479b79a2e711b4907f20e939577bd"
EXPECTED_E1_SOURCE_INDEX_SHA256 = "08f7aaf28a19534e9c9a9baeba521d0d32c7d7d9c2a2a9950ad5c3b12ffee034"
EXPECTED_E1_SOURCE_INDEX_SEMANTIC = "88f57ad8ad0c8fb456a8327a1c8f49b395ea2333fae7a1280870d4184419edc5"
EXPECTED_W9P_LEDGER_SHA256 = "91853c85bf44d3c86a74239176bd22ba42ee6c6d2d54e49cedcc51f3f1dd0add"
Q3_NAMESPACE = "SLCV33_RZ_Q3_FULL_RANKING_GROUP_V1"
CANONICAL_ROLE = "CANONICAL_MODEL_EXAMPLE"
REPLICATE_ROLE = "REPLAY_REPLICATE"
SPLITS = ("TRAIN", "HOLDOUT", "CONTROL")

EXPECTED_TRANSITIONS = {
    ("TRAIN", "TRAIN"): 251,
    ("TRAIN", "HOLDOUT"): 69,
    ("HOLDOUT", "TRAIN"): 69,
    ("HOLDOUT", "HOLDOUT"): 27,
    ("CONTROL", "CONTROL"): 96,
}


class SourceAdmissionError(RuntimeError):
    """The frozen source inventory, grouping, split, or access boundary differs."""


@dataclass(frozen=True, slots=True)
class SourceVisibleChoice:
    """The complete and only object admitted to Q3 feature construction."""

    axis: int
    modulus: int
    left_shell: int
    right_shell: int
    left_direction: int
    right_direction: int
    route_domain: str
    physical_relation_domain: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "axis": self.axis,
            "left_direction": self.left_direction,
            "left_shell": self.left_shell,
            "modulus": self.modulus,
            "physical_relation_domain": self.physical_relation_domain,
            "right_direction": self.right_direction,
            "right_shell": self.right_shell,
            "route_domain": self.route_domain,
        }


FEATURE_SOURCE_FIELDS = tuple(SourceVisibleChoice.__dataclass_fields__)


@dataclass(frozen=True, slots=True)
class SourceRecord:
    """Target-blind source custody.  Metadata never enters a feature function."""

    receipt_index: int
    sample_role: str
    old_q2_group_id: str
    old_q2_split: str
    visible: SourceVisibleChoice


@dataclass(frozen=True, slots=True)
class Q3Group:
    q3_group_id: str
    old_q2_group_id: str
    old_q2_split: str
    q3_split: str
    physical_key: tuple[Any, ...]
    records: tuple[SourceRecord, ...]

    @property
    def axis(self) -> int:
        return int(self.physical_key[0])

    @property
    def multiplicity(self) -> int:
        return len(self.records)

    @property
    def canonical_records(self) -> tuple[SourceRecord, ...]:
        return tuple(row for row in self.records if row.sample_role == CANONICAL_ROLE)


@dataclass(frozen=True, slots=True)
class Q3Inventory:
    groups: tuple[Q3Group, ...]
    source_index_path: Path
    q2_split_manifest_path: Path
    transition_counts: tuple[tuple[str, str, int], ...]

    @property
    def records(self) -> tuple[SourceRecord, ...]:
        return tuple(record for group in self.groups for record in group.records)

    def groups_for_split(self, split: str) -> tuple[Q3Group, ...]:
        if split not in SPLITS:
            raise SourceAdmissionError(f"unknown split: {split}")
        return tuple(group for group in self.groups if group.q3_split == split)


def _strict_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SourceAdmissionError(f"{label} must be an exact integer")
    return value


def physical_group_key(choice: SourceVisibleChoice) -> tuple[Any, ...]:
    return (
        choice.axis,
        choice.modulus,
        min(choice.left_shell, choice.right_shell),
        max(choice.left_shell, choice.right_shell),
        choice.route_domain,
        choice.physical_relation_domain,
    )


def q3_group_id(key: tuple[Any, ...]) -> str:
    return canonical_sha256(
        {
            "axis": key[0],
            "endpoint_max": key[3],
            "endpoint_min": key[2],
            "modulus": key[1],
            "namespace": Q3_NAMESPACE,
            "physical_relation_domain": key[5],
            "route_domain": key[4],
        }
    )


def _load_source_rows() -> tuple[Path, tuple[Mapping[str, Any], ...]]:
    if str(Q1_ROOT) not in sys.path:
        sys.path.insert(0, str(Q1_ROOT))
    from slcv32_rz.source_quality import E1_SOURCE_INDEX  # noqa: PLC0415

    source_path = Path(E1_SOURCE_INDEX)
    if file_sha256(source_path) != EXPECTED_E1_SOURCE_INDEX_SHA256:
        raise SourceAdmissionError("frozen E1 source-index bytes differ")
    source = load_exact_json(source_path)
    if not isinstance(source, Mapping) or source.get("semantic_sha256") != EXPECTED_E1_SOURCE_INDEX_SEMANTIC:
        raise SourceAdmissionError("frozen E1 source-index semantic identity differs")
    # This is a historical sealed source whose semantic serializer predates
    # Q3.  The immutable file hash and its pinned historical semantic field are
    # both checked; Q3 does not reinterpret that predecessor seal.
    rows = source.get("rows")
    if not isinstance(rows, list) or len(rows) != 5120:
        raise SourceAdmissionError("frozen E1 source index must contain 5,120 rows")
    return source_path, tuple(rows)


def _load_q2_membership() -> tuple[dict[int, tuple[str, str]], Mapping[str, Any]]:
    if file_sha256(Q2_SPLIT_MANIFEST) != EXPECTED_Q2_SPLIT_FILE_SHA256:
        raise SourceAdmissionError("frozen Q2 split-manifest bytes differ")
    manifest = load_exact_json(Q2_SPLIT_MANIFEST)
    if not isinstance(manifest, Mapping) or not validate_semantic_seal(manifest):
        raise SourceAdmissionError("frozen Q2 split-manifest semantic seal differs")
    group_rows = manifest.get("group_rows")
    if not isinstance(group_rows, list) or len(group_rows) != 512:
        raise SourceAdmissionError("frozen Q2 split manifest must contain 512 groups")
    membership: dict[int, tuple[str, str]] = {}
    for row in group_rows:
        group_id = row.get("group_sha256")
        split = row.get("split")
        indices = row.get("member_receipt_indices")
        if not isinstance(group_id, str) or len(group_id) != 64 or split not in SPLITS:
            raise SourceAdmissionError("frozen Q2 group metadata differs")
        if not isinstance(indices, list):
            raise SourceAdmissionError("frozen Q2 group member list differs")
        for raw_index in indices:
            index = _strict_int(raw_index, "receipt index")
            if index in membership:
                raise SourceAdmissionError("receipt index appears in multiple Q2 groups")
            membership[index] = (group_id, split)
    if set(membership) != set(range(5120)):
        raise SourceAdmissionError("Q2 group manifest does not cover receipt indices 0..5119")
    return membership, manifest


def _visible_from_index_row(index: int, row: Mapping[str, Any]) -> tuple[str, SourceVisibleChoice]:
    event = row.get("event")
    if not isinstance(event, Mapping):
        raise SourceAdmissionError(f"source row {index} has no event object")
    if _strict_int(row.get("pair_catalog_index"), "pair catalog index") != index:
        raise SourceAdmissionError("source row ordinal differs from pair catalog index")
    replicate = _strict_int(event.get("replicate_index"), "replicate index")
    role = CANONICAL_ROLE if replicate == 0 else REPLICATE_ROLE
    route = event.get("route_domain")
    relation = event.get("physical_relation_domain")
    if not isinstance(route, str) or not isinstance(relation, str):
        raise SourceAdmissionError("source-visible domains must be strings")
    return role, SourceVisibleChoice(
        axis=_strict_int(event.get("axis"), "axis"),
        modulus=_strict_int(event.get("modulus"), "modulus"),
        left_shell=_strict_int(event.get("left_shell"), "left shell"),
        right_shell=_strict_int(event.get("right_shell"), "right shell"),
        left_direction=_strict_int(event.get("left_direction"), "left direction"),
        right_direction=_strict_int(event.get("right_direction"), "right direction"),
        route_domain=route,
        physical_relation_domain=relation,
    )


@lru_cache(maxsize=1)
def load_frozen_q2_inventory() -> Q3Inventory:
    """Load source-visible rows plus the frozen Q2 group manifest.

    The W9P target ledger is not opened here.  In particular, no CONTROL
    inverse, endpoint, checkpoint, or quality value is deserialized.
    """

    source_path, source_rows = _load_source_rows()
    membership, _manifest = _load_q2_membership()
    records_by_old_group: dict[str, list[SourceRecord]] = defaultdict(list)
    old_split_by_group: dict[str, str] = {}
    for index, row in enumerate(source_rows):
        role, visible = _visible_from_index_row(index, row)
        old_group, old_split = membership[index]
        previous = old_split_by_group.setdefault(old_group, old_split)
        if previous != old_split:
            raise SourceAdmissionError("one frozen Q2 group crosses splits")
        records_by_old_group[old_group].append(
            SourceRecord(index, role, old_group, old_split, visible)
        )

    provisional: list[tuple[str, str, tuple[Any, ...], str, tuple[SourceRecord, ...]]] = []
    for old_group, mutable_records in records_by_old_group.items():
        records = tuple(sorted(mutable_records, key=lambda row: row.receipt_index))
        keys = {physical_group_key(row.visible) for row in records}
        if len(keys) != 1:
            raise SourceAdmissionError("one frozen Q2 group crosses physical keys")
        key = next(iter(keys))
        provisional.append((old_group, records[0].old_q2_split, key, q3_group_id(key), records))
    if len(provisional) != 512:
        raise SourceAdmissionError("Q3 must reuse exactly 512 frozen Q2 groups")

    q3_split_by_old_group: dict[str, str] = {}
    for axis in range(4):
        axis_rows = [row for row in provisional if row[2][0] == axis]
        if len(axis_rows) != 128:
            raise SourceAdmissionError("Q3 requires 128 frozen physical groups per axis")
        controls = [row for row in axis_rows if row[1] == "CONTROL"]
        reusable = sorted((row for row in axis_rows if row[1] != "CONTROL"), key=lambda row: row[3])
        if len(controls) != 24 or len(reusable) != 104:
            raise SourceAdmissionError("Q3 control-preserving source counts differ")
        for row in controls:
            q3_split_by_old_group[row[0]] = "CONTROL"
        for ordinal, row in enumerate(reusable):
            q3_split_by_old_group[row[0]] = "TRAIN" if ordinal < 80 else "HOLDOUT"

    groups = tuple(
        Q3Group(
            q3_group_id=new_group,
            old_q2_group_id=old_group,
            old_q2_split=old_split,
            q3_split=q3_split_by_old_group[old_group],
            physical_key=key,
            records=records,
        )
        for old_group, old_split, key, new_group, records in sorted(provisional, key=lambda row: row[3])
    )
    transitions = Counter((group.old_q2_split, group.q3_split) for group in groups)
    if transitions != Counter(EXPECTED_TRANSITIONS):
        raise SourceAdmissionError(f"Q3 split transition counts differ: {dict(transitions)}")
    for split, expected in (("TRAIN", 320), ("HOLDOUT", 96), ("CONTROL", 96)):
        if sum(group.q3_split == split for group in groups) != expected:
            raise SourceAdmissionError(f"Q3 {split} group count differs")
    if Counter(group.multiplicity for group in groups) != Counter({4: 136, 10: 240, 16: 136}):
        raise SourceAdmissionError("frozen Q2 group multiplicity roster differs")
    if any(len(group.canonical_records) != 2 for group in groups):
        raise SourceAdmissionError("every frozen Q2 group must retain two canonical queries")
    transition_rows = tuple(sorted((old, new, count) for (old, new), count in transitions.items()))
    return Q3Inventory(groups, source_path, Q2_SPLIT_MANIFEST, transition_rows)


def load_target_choices(
    inventory: Q3Inventory,
    *,
    splits: Iterable[str],
    control_winner_lock: Mapping[str, Any] | None = None,
) -> dict[int, Any]:
    """Load hidden target rows only for explicitly admitted splits.

    CONTROL raw lines are not JSON-deserialized unless a sealed HOLDOUT winner
    lock is supplied.  This function is not called by source or feature tests.
    """

    requested = frozenset(splits)
    if not requested or not requested <= set(SPLITS):
        raise SourceAdmissionError("target split request is invalid")
    if "CONTROL" in requested:
        if not isinstance(control_winner_lock, Mapping):
            raise SourceAdmissionError("CONTROL target access requires a winner lock")
        if control_winner_lock.get("status") != "SEALED_HOLDOUT_WINNER_LOCK":
            raise SourceAdmissionError("CONTROL winner lock status differs")
        if not isinstance(control_winner_lock.get("semantic_sha256"), str):
            raise SourceAdmissionError("CONTROL winner lock has no semantic SHA-256")

    if str(Q1_ROOT) not in sys.path:
        sys.path.insert(0, str(Q1_ROOT))
    from slcv32_rz.source_quality import (  # noqa: PLC0415
        W9P_LEDGER,
        _extract_choice,
        _loads_historical,
    )

    ledger_path = Path(W9P_LEDGER)
    if file_sha256(ledger_path) != EXPECTED_W9P_LEDGER_SHA256:
        raise SourceAdmissionError("frozen W9P target-ledger bytes differ")
    source = load_exact_json(inventory.source_index_path)
    index_rows = source["rows"]
    record_by_index = {record.receipt_index: record for record in inventory.records}
    result: dict[int, Any] = {}
    with gzip.open(ledger_path, "rb") as handle:
        for index, raw_line in enumerate(handle):
            record = record_by_index[index]
            group = next(group for group in inventory.groups if group.old_q2_group_id == record.old_q2_group_id)
            if group.q3_split not in requested:
                continue
            ledger_row = _loads_historical(raw_line)
            result[index] = _extract_choice(
                index_rows[index],
                ledger_row,
                group_sha256=group.q3_group_id,
                split=group.q3_split,
            )
    return result


def target_ledger_provenance() -> dict[str, str]:
    """Return frozen target-ledger custody without deserializing target rows."""

    if str(Q1_ROOT) not in sys.path:
        sys.path.insert(0, str(Q1_ROOT))
    from slcv32_rz.source_quality import W9P_LEDGER  # noqa: PLC0415

    ledger_path = Path(W9P_LEDGER)
    observed = file_sha256(ledger_path)
    if observed != EXPECTED_W9P_LEDGER_SHA256:
        raise SourceAdmissionError("frozen W9P target-ledger bytes differ")
    return {
        "path": str(ledger_path),
        "file_sha256": observed,
    }
