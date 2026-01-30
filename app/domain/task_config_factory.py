from dataclasses import dataclass
from enum import Enum
from typing import Any, Type
from pydantic import BaseModel
from app.domain.marker import Marker


DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()


class TaskMode(str, Enum):
    FILESTOTEXTBYMARKER = "filestotextbymarker"
    FILESTOTEXTBYPADDLE = "filestotextbypaddle"


@dataclass
class TaskConfig:
    schema: Type[BaseModel]

    # LLM / VLM
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"

    # generation
    temperature: float = 0.1
    max_tokens: int = 2048
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    # pipeline
    task_mode: TaskMode = TaskMode.FILESTOTEXTBYPADDLE
    marker: Marker | None = None

    # process
    preprocess: dict[str, Any] | None = None
    postprocess: dict[str, Any] | None = None


def TaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    **overrides,
) -> TaskConfig:
    """
    构建 TaskConfig（仅覆盖需要的字段）
    """
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    return TaskConfig(schema=schema, system_prompt=system_prompt, **overrides)
