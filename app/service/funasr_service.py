from app.domain.resources.context import TaskContext
from app.domain.resources.file_item import FileItem
from app.domain.templates.voice_transcribe.config import VoiceTaskConfig
from app.domain.templates.voice_transcribe.template import build_voice_task
from app.domain.tasks.task_runner import run_task


async def transcribe_service(
    *,
    file_item: FileItem,
    taskconfig: VoiceTaskConfig,
) -> dict[str, str]:
    task = build_voice_task(taskconfig)
    context = TaskContext(file_items=[file_item])
    return await run_task(task, context)
