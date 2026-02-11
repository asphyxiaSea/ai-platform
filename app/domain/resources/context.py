from dataclasses import dataclass
from typing import Any
from app.domain.resources.file_item import FileItem


@dataclass
class TaskContext:
    # 任务上下文，包含文件列表、文本列表和结果
    file_items: list[FileItem]
    texts: list[str] | None = None
    result: Any = None
