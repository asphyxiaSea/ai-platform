from dataclasses import dataclass
from enum import Enum
from typing import Type
from pydantic import BaseModel


DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()


class LLMTaskMode(str, Enum):
    CHAT = "chat"
    MULTIMODAL = "multimodal"


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]

    user_prompt: str = ""
    has_images: bool = False

    # LLM / VLM
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"

    # generation
    temperature: float = 0.1
    max_tokens: int = 2048
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    task_mode: LLMTaskMode = LLMTaskMode.CHAT


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    user_prompt: str = "",
    has_images: bool = False,
    **overrides,
) -> LLMTaskConfig:
    """构建 LLMTaskConfig（仅覆盖需要的字段）"""
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    task_mode = overrides.pop("task_mode", None)
    if task_mode is None:
        task_mode = LLMTaskMode.MULTIMODAL if has_images else LLMTaskMode.CHAT
    return LLMTaskConfig(
        schema=schema,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        has_images=has_images,
        task_mode=task_mode,
        **overrides,
    )
