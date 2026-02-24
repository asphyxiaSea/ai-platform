from dataclasses import dataclass, field
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig
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
