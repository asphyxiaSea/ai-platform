from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.context import TaskContext


class TaskStep(Protocol):
    async def execute(self, context: "TaskContext") -> None:
        ...


@dataclass
class Task:
    name: str
    steps: list[TaskStep]
