from dataclasses import dataclass, field
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig, build_llm_config
from app.domain.capabilities.paddle.paddle_config import PaddleConfig

@dataclass
class FilesTaskConfig:
    schema: Type[BaseModel]

    llm: LLMConfig = field(default_factory=LLMConfig)

    # pipeline
    paddle: PaddleConfig | None = None

    # process
    pdf_process: dict[str, Any] | None = None
    text_process: dict[str, Any] | None = None


def FilesTaskConfig_factory(
    *,
    schema: Type[BaseModel],
    system_prompt: str | None = None,
    llm_config: LLMConfig | None = None,
    **overrides,
) -> FilesTaskConfig:
    """构建 FilesTaskConfig（仅覆盖需要的字段）"""
    llm = build_llm_config(
        base=llm_config,
        schema=schema,
        system_prompt=system_prompt,
    )
    return FilesTaskConfig(schema=schema, llm=llm, **overrides)
