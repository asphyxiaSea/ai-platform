from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Type
from pydantic import BaseModel
from app.domain.capabilities.llm.llm_config import LLMConfig


class LLMTaskMode(str, Enum):
    CHAT = "chat"
    MULTIMODAL = "multimodal"


@dataclass
class LLMTaskConfig:
    schema: Type[BaseModel]
    task_mode: LLMTaskMode = LLMTaskMode.CHAT
    system_prompt: str | None = None
    text: str = ""

    llm: LLMConfig = field(default_factory=LLMConfig)
