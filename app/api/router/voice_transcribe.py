import asyncio
import os
from fastapi import APIRouter, UploadFile, File
from app.service.funasr_service import transcribe_service
from app.util.file_utils import upload_file_to_item

router = APIRouter(prefix="/voice", tags=["voice_transcribe"])


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model_key: str = "",
):
    file_item = await upload_file_to_item(upload_file=file)
    try:
        return await transcribe_service(
            file_item=file_item,
            model_key=model_key,
        )
    finally:
        if file_item.path:
            await asyncio.to_thread(os.remove, file_item.path)
