from dataclasses import dataclass
from enum import Enum
from typing import Any


class Sam3TaskMode(str, Enum):
    SEGMENT_INSTANCE_TEXTS = "segment_instance_texts"


@dataclass
class Sam3TaskConfig:
    reference_config: dict[str, Any]
    target_config: dict[str, Any]
    task_mode: Sam3TaskMode = Sam3TaskMode.SEGMENT_INSTANCE_TEXTS


def Sam3TaskConfig_factory(
    *,
    reference_config: dict[str, Any],
    target_config: dict[str, Any],
    **overrides,
) -> Sam3TaskConfig:
    return Sam3TaskConfig(
        reference_config=reference_config,
        target_config=target_config,
        **overrides,
    )
