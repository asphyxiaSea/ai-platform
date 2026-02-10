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
    MULTIMODAL = "multimodal"


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]

    # LLM / VLM
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"

    # generation
    temperature: float = 0.1
    max_tokens: int = 2048
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    task_mode: LLMTaskMode = LLMTaskMode.MULTIMODAL


def LLMTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    **overrides,
) -> LLMTaskConfig:
    """构建 LLMTaskConfig（仅覆盖需要的字段）"""
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    return LLMTaskConfig(schema=schema, system_prompt=system_prompt, **overrides)
