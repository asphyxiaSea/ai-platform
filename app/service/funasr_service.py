from app.domain.file_item import FileItem
from app.domain.task_config_factory import VoiceTaskConfig, VoiceTaskMode
from app.domain.errors import UnsupportedOperationError
from app.infra.funasr_client import transcribe


async def transcribe_service(
    *,
    file_item: FileItem,
    taskconfig: VoiceTaskConfig,
) -> dict[str, str]:
    if taskconfig.task_mode != VoiceTaskMode.TRANSCRIBE:
        raise UnsupportedOperationError(
            message="未知的任务模式",
            detail=str(taskconfig.task_mode),
        )
    text = await transcribe(file_path=file_item.path or "", model_key=taskconfig.model_key)
    return {"text": text}
