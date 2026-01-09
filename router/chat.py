from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from service.chat_extract_service import chat_extract_service
from domain import FileItem

router = APIRouter(prefix="/ollama_api", tags=["ollama"])
@router.post("/chat")
async def chat(
    schema_name: str = Form(...),
    files: List[UploadFile] = File(...),
):
    if not files:
        raise HTTPException(400, "No files provided")

    file_items: list[FileItem] = []

    for f in files:
        file_items.append(
            FileItem(
                filename=f.filename or "",
                content_type=f.content_type or "",
                data=await f.read(),
            )
        )

    return await chat_extract_service(
        schema_name=schema_name,
        file_items=file_items,
    )