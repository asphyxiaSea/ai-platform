from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import (
    DEFAULT_SYSTEM_PROMPT,
    LLMConfig,
)


class LLMTaskMode(str, Enum):
    CHAT = "chat"
    MULTIMODAL = "multimodal"


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]
    task_mode: LLMTaskMode = LLMTaskMode.CHAT
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    user_prompt: str = ""

    llm: LLMConfig = field(default_factory=LLMConfig)


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    user_prompt: str = "",
    task_mode: LLMTaskMode = LLMTaskMode.CHAT,
) -> LLMTaskConfig:
    """构建 LLMTaskConfig（仅覆盖需要的字段）"""
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    llm = LLMConfig()
    return LLMTaskConfig(
        schema=schema,
        task_mode=task_mode,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        llm=llm,
    )
