from app.domain.context import TaskContext
from app.domain.file_item import FileItem
from app.domain.tasks.task_runner import run_task
from app.domain.templates.sam3.config import Sam3TaskConfig
from app.domain.templates.sam3.template import build_sam3_task


async def sam3_service(
    *,
    file_item: FileItem,
    taskconfig: Sam3TaskConfig,
):
    task = build_sam3_task(taskconfig)
    context = TaskContext(file_items=[file_item])
    return await run_task(task, context)
