from dataclasses import dataclass, field
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig
from app.domain.capabilities.llm.build_llm_prompte import DEFAULT_SYSTEM_PROMPT
from app.domain.capabilities.paddle.paddle_config import PaddleConfig

@dataclass
class FilesTaskConfig:
    schema: Type[BaseModel]
    system_prompt: str | None = None
    user_prompt: str = ""

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
    user_prompt: str = "",
    paddle: PaddleConfig | None = None,
    pdf_process: dict[str, Any] | None = None,
    text_process: dict[str, Any] | None = None,
) -> FilesTaskConfig:
    """构建 FilesTaskConfig（仅覆盖需要的字段）"""
    llm = LLMConfig()
    return FilesTaskConfig(
        schema=schema,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        llm=llm,
        paddle=paddle,
        pdf_process=pdf_process,
        text_process=text_process,
    )
