from dataclasses import dataclass, field
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig, build_llm_config


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]

    llm: LLMConfig = field(default_factory=LLMConfig)


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    user_prompt: str = "",
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
        llm=llm,
    )
