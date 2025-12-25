from typing import Type
from pydantic import BaseModel

class TaskConfig:
    def __init__(
        self,
        schema: Type[BaseModel],
        model: str,
        # 模型保守程度，越高越不保守
        temperature: float = 0.0,
        max_tokens: int = 2048,
        page_range: str = "0-20"
    ):
        self.schema = schema
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.page_range = page_range
