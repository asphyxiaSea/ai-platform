from app.domain.templates.files_parse.config import FilesParseConfig
from app.domain.templates.files_parse.template import build_files_parse_task
from app.domain.resources.context import TaskContext
from app.domain.resources.file_item import FileItem
from app.domain.tasks.task_runner import run_task


async def files_parse_service(
    *,
    config: FilesParseConfig,
    file_items: list[FileItem],
):
    task = build_files_parse_task(config)
    context = TaskContext(file_items=file_items)
    return await run_task(task, context)
