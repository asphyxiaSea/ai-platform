from dataclasses import dataclass, field
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import (
    LLMConfig,
    LLMTaskMode,
    build_llm_config,
)


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]
    has_images: bool = False

    llm: LLMConfig = field(default_factory=LLMConfig)


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    user_prompt: str = "",
    has_images: bool = False,
    llm_config: LLMConfig | None = None,
    **overrides,
) -> LLMTaskConfig:
    """构建 LLMTaskConfig（仅覆盖需要的字段）"""
    task_mode = overrides.pop("task_mode", None)
    if task_mode is None:
        task_mode = LLMTaskMode.MULTIMODAL if has_images else LLMTaskMode.CHAT
    merged_overrides: dict[str, Any] = {
        "user_prompt": user_prompt,
        "task_mode": task_mode,
    }
    llm = build_llm_config(
        base=llm_config,
        schema=schema,
        system_prompt=system_prompt,
        overrides=merged_overrides,
    )
    return LLMTaskConfig(
        schema=schema,
        has_images=has_images,
        llm=llm,
        **overrides,
    )
