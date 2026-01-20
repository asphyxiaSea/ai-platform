from typing import Type
from pydantic import BaseModel
from domain.marker import Marker

from typing import Type,Any
from pydantic import BaseModel
from enum import Enum

DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
"""

class TaskMode(Enum):
    FILESTOTEXTBYMARKER = "filestotextbymarker"
    FILESTOTEXTBYPADDLE = "filestotextbypaddle"

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
        system_prompt: str=DEFAULT_SYSTEM_PROMPT,
        task_mode: TaskMode = TaskMode.FILESTOTEXTBYPADDLE,
        # 修改marker-pdf配置
        marker: Marker | None = None,
        # 输入文件前处理
        preprocess: dict[str,Any] | None = None,
    ):
        self.schema = schema
        self.model = model
        self.vl_model = vl_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.task_mode = task_mode
        self.marker = marker
        self.preprocess = preprocess

def TaskConfig_factory(
    *,
    schema: Type[BaseModel],
    task_mode: TaskMode = TaskMode.FILESTOTEXTBYPADDLE,
    model: str = "gemma3:12b",
    vl_model: str = "qwen3-vl:latest",
    temperature: float = 0.1,
    max_tokens: int = 2048,
    preprocess: dict[str,Any] | None = None,
) -> TaskConfig:
    """
    构建 TaskConfig
    """

    return TaskConfig(
        schema=schema,
        model=model,
        vl_model=vl_model,
        temperature=temperature,
        max_tokens=max_tokens,
        task_mode=task_mode,
        preprocess=preprocess,
    )

