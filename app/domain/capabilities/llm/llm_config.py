from dataclasses import dataclass, replace
from typing import Any, Mapping, Type
from pydantic import BaseModel

DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()


@dataclass
class LLMConfig:
    schema: Type[BaseModel] | None = None
    user_prompt: str = ""
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"
    temperature: float = 0.1


def build_llm_config(
    *,
    overrides: Mapping[str, Any] | None = None,
) -> LLMConfig:
    config = LLMConfig()
    merged = dict(overrides or {})
    return replace(config, **merged) if merged else config
