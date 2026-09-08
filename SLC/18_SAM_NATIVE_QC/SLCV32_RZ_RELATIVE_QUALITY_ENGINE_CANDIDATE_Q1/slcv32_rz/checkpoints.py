"""Predecessor-linked exact Q1 checkpoint and replay custody."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .canonical import canonical_sha256, require_seal, seal_dict


class CheckpointError(RuntimeError):
    """A checkpoint chain or deterministic replay differs."""


STAGES = (
    "FROZEN_PREDECESSORS_AND_SOURCES_ADMITTED",
    "Q1_GROUP_SPLIT_AND_TARGET_CATALOG_FROZEN",
    "HARDER_TRAIN_CATALOG_FROZEN",
    "EXACT_SELECTOR_MODELS_RECONSTRUCTED",
    "COMPLETE_HOLDOUT_EVALUATED",
    "WINNER_SELECTED_BEFORE_CONTROL",
    "CONTROL_READ_ONCE_AFTER_SELECTION",
    "FROZEN_PREDECESSOR_RECONSTRUCTION_ADMITTED",
)


@dataclass(frozen=True, slots=True)
class CheckpointChain:
    candidate: str
    root_predecessor_semantic_sha256: str
    checkpoints: tuple[dict[str, Any], ...] = ()

    def append(self, stage: str, payload: Mapping[str, Any]) -> "CheckpointChain":
        expected_index = len(self.checkpoints)
        if expected_index >= len(STAGES) or stage != STAGES[expected_index]:
            raise CheckpointError(
                f"checkpoint stage {stage!r} differs from expected {STAGES[expected_index:expected_index + 1]}"
            )
        if not isinstance(payload, Mapping):
            raise CheckpointError("checkpoint payload must be an object")
        previous = (
            self.root_predecessor_semantic_sha256
            if not self.checkpoints
            else self.checkpoints[-1]["semantic_sha256"]
        )
        checkpoint = seal_dict(
            {
                "schema": "SLCV32_RZ_Q1_EXACT_CHECKPOINT_V1",
                "candidate": self.candidate,
                "checkpoint_index": expected_index,
                "stage": stage,
                "predecessor_semantic_sha256": previous,
                "payload": dict(payload),
                "payload_semantic_sha256": canonical_sha256(payload),
            }
        )
        return CheckpointChain(
            candidate=self.candidate,
            root_predecessor_semantic_sha256=self.root_predecessor_semantic_sha256,
            checkpoints=self.checkpoints + (checkpoint,),
        )

    def verify_complete(self) -> None:
        if len(self.checkpoints) != len(STAGES):
            raise CheckpointError("checkpoint chain is incomplete")
        previous = self.root_predecessor_semantic_sha256
        for index, (stage, checkpoint) in enumerate(zip(STAGES, self.checkpoints, strict=True)):
            require_seal(checkpoint, f"checkpoint {index}")
            if (
                checkpoint.get("checkpoint_index") != index
                or checkpoint.get("stage") != stage
                or checkpoint.get("predecessor_semantic_sha256") != previous
                or checkpoint.get("payload_semantic_sha256")
                != canonical_sha256(checkpoint.get("payload"))
            ):
                raise CheckpointError(f"checkpoint {index} chain identity differs")
            previous = checkpoint["semantic_sha256"]

    def to_dict(self) -> dict[str, Any]:
        self.verify_complete()
        value = {
            "schema": "SLCV32_RZ_Q1_EXACT_CHECKPOINT_CHAIN_V1",
            "candidate": self.candidate,
            "checkpoint_count": len(self.checkpoints),
            "root_predecessor_semantic_sha256": self.root_predecessor_semantic_sha256,
            "terminal_checkpoint_semantic_sha256": self.checkpoints[-1]["semantic_sha256"],
            "checkpoints": list(self.checkpoints),
        }
        value["semantic_sha256"] = canonical_sha256(value)
        return value


def require_replay_identity(primary: Mapping[str, Any], replay: Mapping[str, Any]) -> dict[str, Any]:
    for label, chain in (("primary", primary), ("replay", replay)):
        require_seal(chain, f"{label} checkpoint chain")
        if (
            chain.get("schema") != "SLCV32_RZ_Q1_EXACT_CHECKPOINT_CHAIN_V1"
            or chain.get("checkpoint_count") != len(STAGES)
            or not isinstance(chain.get("checkpoints"), list)
            or len(chain["checkpoints"]) != len(STAGES)
        ):
            raise CheckpointError(f"{label} checkpoint chain is not complete")
    if dict(primary) != dict(replay):
        raise CheckpointError("primary and replay checkpoint chains differ")
    return seal_dict(
        {
            "schema": "SLCV32_RZ_Q1_CHECKPOINT_REPLAY_IDENTITY_V1",
            "status": "PASS",
            "primary_semantic_sha256": primary.get("semantic_sha256"),
            "replay_semantic_sha256": replay.get("semantic_sha256"),
            "byte_semantic_equal": True,
            "checkpoint_count": primary.get("checkpoint_count"),
        }
    )


__all__ = [
    "CheckpointChain",
    "CheckpointError",
    "STAGES",
    "require_replay_identity",
]
