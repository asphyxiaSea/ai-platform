from typing import Type
from pydantic import BaseModel
from enum import Enum

class InputMode(Enum):
    IMAGE = "image"
    PDFTOTEXT = "pdftotext"
    PDFTOIMAGE = "pdftoimage"
    PDFTOTEXTANDIAMGE = "pdftotextandimage"

class TaskConfig:
    def __init__(
        self,
        schema: Type[BaseModel],
        model: str="gemma3:latest",
        vl_model:str="qwen3-vl:latest",
        # 模型保守程度，越高越不保守
        temperature: float = 0.0,
        max_tokens: int = 2048,
        page_range: str = "0-20",
        input_mode: InputMode = InputMode.PDFTOTEXT,
    ):
        self.schema = schema
        self.model = model
        self.vl_model = vl_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.page_range = page_range
        self.input_mode = input_mode
