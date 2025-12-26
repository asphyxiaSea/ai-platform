from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from service.chat_extract_service import chat_extract_service
router = APIRouter(prefix="/ollama_api", tags=["ollama"])

@router.post("/chat")
async def chat(
    schema_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(400, "No files provided")

    pdf_bytes_list: list[bytes] = []
    image_bytes_list: list[bytes] = []

    for f in files:
        ct = f.content_type or ""
        filename = f.filename or ""
        data = await f.read()

        # --- PDF ---
        if ct == "application/pdf" or filename.lower().endswith(".pdf"):
            pdf_bytes_list.append(data)
        # --- 图片 ---
        elif ct.startswith("image/"):
            image_bytes_list.append(data)
        # --- 不支持类型 ---
        else:
            raise HTTPException(
                400,
                f"Unsupported file type: {filename} ({ct})"
        )

    return await chat_extract_service(
        schema_name=schema_name,
        image_bytes_list=image_bytes_list,
        pdf_bytes_list=pdf_bytes_list,
    )