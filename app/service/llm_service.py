from app.domain.templates.llm_chat.config import LLMTaskConfig
from app.domain.templates.llm_chat.template import build_llm_task
from app.domain.resources.context import TaskContext
from app.domain.resources.file_item import FileItem
from app.domain.tasks.task_runner import run_task


async def llm_service(
    *,
    taskconfig: LLMTaskConfig,
    file_items: list[FileItem],
):
    task = build_llm_task(taskconfig)
    context = TaskContext(file_items=file_items)
    return await run_task(task, context)
