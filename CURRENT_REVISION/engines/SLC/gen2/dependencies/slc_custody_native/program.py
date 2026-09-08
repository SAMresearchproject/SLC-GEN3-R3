"""Composable custody-native programs with forward and reverse execution."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Hashable, Iterable

from .compiler import CompiledCustodyMorphism, FiberReceipt


@dataclass(frozen=True, slots=True)
class ProgramReceipt:
    schema: str
    program_id: str
    stage_receipts: tuple[FiberReceipt, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "program_id": self.program_id,
            "stage_receipts": [receipt.to_dict() for receipt in self.stage_receipts],
        }


@dataclass(frozen=True, slots=True)
class ProgramState:
    visible: Hashable
    receipt: ProgramReceipt


class CompiledCustodyProgram:
    """A typed sequence that retains enough stage custody to run backward."""

    def __init__(
        self,
        name: str,
        stages: Iterable[CompiledCustodyMorphism[Any, Any]],
    ) -> None:
        self.name = str(name)
        self.stages = tuple(stages)
        if not self.stages:
            raise ValueError("custody program requires at least one stage")
        for first, second in zip(self.stages, self.stages[1:]):
            missing = set(first.visible_outputs) - set(second.domain)
            if missing:
                raise ValueError("adjacent custody stages have incompatible domains")
        digest = hashlib.sha256()
        digest.update(self.name.encode("utf-8"))
        for stage in self.stages:
            digest.update(stage.morphism_id.encode("ascii"))
        self.program_id = digest.hexdigest()

    @property
    def domain(self) -> tuple[Hashable, ...]:
        return self.stages[0].domain

    def execute(self, item: Hashable) -> ProgramState:
        visible: Hashable = item
        receipts: list[FiberReceipt] = []
        for stage in self.stages:
            state = stage.encode(visible)
            visible = state.visible
            receipts.append(state.receipt)
        return ProgramState(
            visible=visible,
            receipt=ProgramReceipt(
                schema="SLC_CUSTODY_NATIVE_PROGRAM_RECEIPT_V1",
                program_id=self.program_id,
                stage_receipts=tuple(receipts),
            ),
        )

    def reconstruct(self, final_visible: Hashable, receipt: ProgramReceipt) -> Hashable:
        if receipt.program_id != self.program_id:
            raise ValueError("receipt belongs to a different custody program")
        if len(receipt.stage_receipts) != len(self.stages):
            raise ValueError("program receipt has the wrong stage count")
        visible = final_visible
        for stage, stage_receipt in zip(reversed(self.stages), reversed(receipt.stage_receipts)):
            visible = stage.decode(visible, stage_receipt)
        return visible

    def directly_minimized_morphism(
        self,
    ) -> tuple[CompiledCustodyMorphism[Any, Any], tuple[dict[str, object], ...]]:
        minimized = self.stages[0]
        reports: list[dict[str, object]] = []
        for stage in self.stages[1:]:
            minimized, report = minimized.compose(
                stage,
                name=f"{self.name}_DIRECT_MINIMAL_STAGE_{len(reports) + 2}",
            )
            reports.append(report)
        return minimized, tuple(reports)

    def audit(self) -> dict[str, object]:
        reconstruction_failures: list[str] = []
        augmented_keys: set[tuple[Hashable, tuple[tuple[str, int], ...]]] = set()
        for item in self.domain:
            state = self.execute(item)
            key = (
                state.visible,
                tuple(
                    (receipt.morphism_id, receipt.fiber_index)
                    for receipt in state.receipt.stage_receipts
                ),
            )
            augmented_keys.add(key)
            if self.reconstruct(state.visible, state.receipt) != item:
                reconstruction_failures.append(repr(item))
        minimized, reports = self.directly_minimized_morphism()
        return {
            "schema": "SLC_CUSTODY_NATIVE_PROGRAM_AUDIT_V1",
            "program_id": self.program_id,
            "stage_count": len(self.stages),
            "input_count": len(self.domain),
            "augmented_key_count": len(augmented_keys),
            "augmented_map_injective": len(augmented_keys) == len(self.domain),
            "reconstruction_failures": reconstruction_failures,
            "direct_minimized_morphism_id": minimized.morphism_id,
            "direct_minimized_profile": minimized.profile.to_dict(),
            "composition_reports": list(reports),
            "status": (
                "PASS"
                if not reconstruction_failures and len(augmented_keys) == len(self.domain)
                else "FAIL"
            ),
        }
