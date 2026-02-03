from fastapi import APIRouter, UploadFile, File
from app.service.funasr_service import transcribe_service
from app.util.file_utils import upload_file_to_item

router = APIRouter(prefix="/voice", tags=["voice_transcribe"])


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model_key: str = "",
):
    uploaded = await upload_file_to_item(upload_file=file)
    try:
        return await transcribe_service(
            file_item=uploaded.item,
            model_key=model_key,
        )
    finally:
        await uploaded.cleanup()
