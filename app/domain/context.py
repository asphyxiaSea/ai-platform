from dataclasses import dataclass, field
from typing import Any
from app.domain.file_item import FileItem


@dataclass
class TaskContext:
    # 任务上下文，包含文件列表、输出结果与最终结果
    file_items: list[FileItem]
    result: Any = None
    outputs: dict[str, Any] = field(default_factory=dict)

    def set_output(self, key: str, value: Any) -> None:
        self.outputs[key] = value

    def get_output(self, key: str, default: Any = None) -> Any:
        return self.outputs.get(key, default)
