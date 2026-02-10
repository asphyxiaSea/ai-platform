from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal, Type
from pydantic import BaseModel
from app.domain.marker import Marker

DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()

class FilesTaskMode(str, Enum):
    FILESTOTEXTBYMARKER = "filestotextbymarker"
    FILESTOTEXTBYPADDLE = "filestotextbypaddle"


@dataclass
class FilesTaskConfig:
    schema: Type[BaseModel]

    # LLM / VLM
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"

    # generation
    temperature: float = 0.1
    max_tokens: int = 2048
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    # pipeline
    task_mode: FilesTaskMode = FilesTaskMode.FILESTOTEXTBYPADDLE
    marker: Marker | None = None

    # process
    preprocess: dict[str, Any] | None = None
    postprocess: dict[str, Any] | None = None


def FilesTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    **overrides,
) -> FilesTaskConfig:
    """构建 FilesTaskConfig（仅覆盖需要的字段）"""
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    return FilesTaskConfig(schema=schema, system_prompt=system_prompt, **overrides)


@dataclass
class FilesParseConfig:
    parser_backend: Literal["marker", "paddle"]
    model: str
    schema: type[BaseModel]
    temperature: float = 0.1
    system_prompt: str | None = DEFAULT_SYSTEM_PROMPT
    pdf_process: dict | None = None
    text_process: dict | None = None
    marker: Marker | None = None
