from dataclasses import dataclass
from enum import Enum


class VoiceTaskMode(str, Enum):
    TRANSCRIBE = "transcribe"


@dataclass
class VoiceTaskConfig:
    model_key: str = ""
    task_mode: VoiceTaskMode = VoiceTaskMode.TRANSCRIBE


def VoiceTaskConfig_factory(
    *,
    model_key: str | None = None,
    **overrides,
) -> VoiceTaskConfig:
    """构建 VoiceTaskConfig（仅覆盖需要的字段）"""
    if model_key is None:
        model_key = ""
    return VoiceTaskConfig(model_key=model_key, **overrides)
