from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from service.multimodal_service import chat_multimodal_images_services
from service.text_service import chat_texts_pdfs_services
router = APIRouter(prefix="/ollama_api/chat", tags=["ollama"])

@router.post("/combined")
async def chat_multimodal_extract(
    schema_name: str = Form(...),
    image_files: List[UploadFile] | None = File(None),
    pdf_files: List[UploadFile] | None = File(None),
):
    # -------- 1. 必须且只能传一个 --------
    if (not image_files and not pdf_files) or (image_files and pdf_files):
        raise HTTPException(
            status_code=400,
            detail="You must provide either images or pdfs, but not both"
        )

    # -------- 2. images 路径 --------
    if image_files:
        image_bytes: list[bytes] = []

        for img in image_files:
            ct = img.content_type or ""
            if not ct.startswith("image/"):
                raise HTTPException(
                    400,
                    f"{img.filename} is not an image"
                )

            image_bytes.append(await img.read())

        return chat_multimodal_images_services(
            schema_name=schema_name,
            image_bytes=image_bytes
        )

    # -------- 3. pdfs 路径 --------
    pdf_bytes_list: list[bytes] = []

    for pdf in pdf_files:  # type: ignore
        filename = pdf.filename or ""
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                400,
                f"Only PDF files are supported: {filename}"
            )

        pdf_bytes_list.append(await pdf.read())

    return chat_texts_pdfs_services(
        schema_name=schema_name,
        pdf_bytes_list=pdf_bytes_list
    )