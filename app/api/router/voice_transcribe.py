from fastapi import APIRouter, UploadFile, File
from app.service.funasr_service import transcribe_service
from app.domain.task_config_factory import VoiceTaskConfig_factory
from app.util.file_utils import upload_file_to_item

router = APIRouter(prefix="/voice", tags=["voice_transcribe"])


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model_key: str = "",
):
    uploaded = await upload_file_to_item(upload_file=file)
    try:
        taskconfig = VoiceTaskConfig_factory(model_key=model_key)
        return await transcribe_service(
            file_item=uploaded.item,
            taskconfig=taskconfig,
        )
    finally:
        await uploaded.cleanup()
