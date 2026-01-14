from typing import Type
from pydantic import BaseModel
from domain.marker import Marker
from domain.task_mode import TaskMode

class TaskConfig:
    def __init__(
        self,
        *,
        schema: Type[BaseModel],
        model: str="gemma3:12b",
        vl_model:str="qwen3-vl:latest",
        # 模型保守程度，越高越不保守
        temperature: float = 0.1,
        max_tokens: int = 2048,
        task_mode: TaskMode = TaskMode.FILESTOTEXTBYPADDLE,
        # 修改marker-pdf配置
        marker: Marker | None = None,
    ):
        self.schema = schema
        self.model = model
        self.vl_model = vl_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.task_mode = task_mode
        self.marker = marker
