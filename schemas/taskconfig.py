from typing import Type,Any
from pydantic import BaseModel
from enum import Enum
from util import MarkerPDF

class TaskMode(Enum):
    IMAGE = "image"
    PDFTOTEXT = "pdftotext"
    PDFTOIMAGE = "pdftoimage"
    PDFTOTEXTANDIAMGE = "pdftotextandimage"
    PDFTOTEXTBYCHUNK = "pdftotextbychunk"
    PDFTOIMAGEBYCHUNK = "pdftoimagebychunk"

class TaskConfig:
    def __init__(
        self,
        schema: Type[BaseModel],
        model: str="gemma3:latest",
        vl_model:str="qwen3-vl:latest",
        # 模型保守程度，越高越不保守
        temperature: float = 0.1,
        max_tokens: int = 2048,
        task_mode: TaskMode = TaskMode.PDFTOTEXTANDIAMGE,
        # 修改marker-pdf配置
        markerpdf: MarkerPDF | None = None,
        markerpdf_config: dict[str, Any] | None = None,
    ):
        self.schema = schema
        self.model = model
        self.vl_model = vl_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.task_mode = task_mode
        self.markerpdf = markerpdf
        self.markerpdf_config = markerpdf_config
