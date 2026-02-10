from dataclasses import dataclass
from typing import Any
from app.domain.resources.file_item import FileItem


@dataclass
class TaskContext:
    file_items: list[FileItem]
    texts: list[str] | None = None
    result: Any = None
