from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from service.multimodal_service import chat_multimodal_pdfs_services,chat_multimodal_images_services

router = APIRouter(prefix="/ollama_api/chat/multimodal", tags=["ollama"])

@router.post("/images")
async def chat_multimodal_images(
    schema_name: str = Form(...),
    image_files: List[UploadFile] = File(...)
):

    image_bytes: List[bytes] = []

    for img in image_files:
        content_type = img.content_type
        if not content_type or not content_type.startswith("image/"):
            raise HTTPException(400, f"{img.filename} is not an image")

        image_bytes.append(await img.read())

    result = chat_multimodal_images_services(
        schema_name=schema_name,
        image_bytes=image_bytes
    )

    return result


@router.post("/pdfs")
async def chat_multimodal_pdfs(
    schema_name: str = Form(...),
    pdf_files: List[UploadFile] = File(...)
):
    pdf_bytes_list = []

    for pdf_file in pdf_files:
        filename = pdf_file.filename or ""
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are supported: {filename}"
            )

        pdf_bytes = await pdf_file.read()
        pdf_bytes_list.append(pdf_bytes)

    result = chat_multimodal_pdfs_services(
        schema_name=schema_name,
        pdf_bytes_list=pdf_bytes_list
    )

    return result