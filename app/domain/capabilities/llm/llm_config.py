from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping, Type
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
class LLMConfig:
    schema: Type[BaseModel] | None = None
    user_prompt: str = ""
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    task_mode: LLMTaskMode = LLMTaskMode.CHAT
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"
    temperature: float = 0.1


def build_llm_config(
    *,
    base: LLMConfig | None = None,
    schema: Type[BaseModel] | None = None,
    system_prompt: str | None = None,
    overrides: Mapping[str, Any] | None = None,
) -> LLMConfig:
    config = base or LLMConfig()
    merged = dict(overrides or {})
    if schema is not None:
        merged["schema"] = schema
    if system_prompt is not None:
        merged["system_prompt"] = system_prompt
    return replace(config, **merged) if merged else config
