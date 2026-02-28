from app.domain.tasks.task import Task
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.context import TaskContext
    
async def run_task(task: Task, context: "TaskContext"):
    for step in task.steps:
        await step.execute(context)
    return context.result
