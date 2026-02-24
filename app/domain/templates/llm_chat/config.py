from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig, build_llm_config


class LLMTaskMode(str, Enum):
    CHAT = "chat"
    MULTIMODAL = "multimodal"


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]
    task_mode: LLMTaskMode = LLMTaskMode.CHAT

    llm: LLMConfig = field(default_factory=LLMConfig)


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    user_prompt: str = "",
    task_mode: LLMTaskMode = LLMTaskMode.CHAT,
) -> LLMTaskConfig:
    """构建 LLMTaskConfig（仅覆盖需要的字段）"""
    merged_overrides: dict[str, Any] = {
        "schema": schema,
        "user_prompt": user_prompt,
    }
    if system_prompt is not None:
        merged_overrides["system_prompt"] = system_prompt
    llm = build_llm_config(overrides=merged_overrides)
    return LLMTaskConfig(
        schema=schema,
        task_mode=task_mode,
        llm=llm,
    )
