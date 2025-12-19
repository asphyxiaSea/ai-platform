from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from schemas.registry import SCHEMA_REGISTRY

from service.ollama_chat_service import chat_with_pdf,chat_text_only,chat_with_images

router = APIRouter(prefix="/ollama_api/chat", tags=["ollama"])

@router.post("/text")
async def ollama_chat_text(
    model: str = Form(...),
    prompt: str = Form(...),
    schema_name: str = Form(...),
):

    result = chat_text_only(
        model=model,
        prompt=prompt,
        schema_name=schema_name
    )
    return result

@router.post("/images")
async def ollama_chat_images(
    model: str = Form(...),
    prompt: str = Form(...),
    schema_name: str = Form(...),
    images: List[UploadFile] = File(...)
):

    image: List[bytes] = []

    for img in images:
        content_type = img.content_type
        if not content_type or not content_type.startswith("image/"):
            raise HTTPException(400, f"{img.filename} is not an image")

        image.append(await img.read())

    result = chat_with_images(
        model=model,
        prompt=prompt,
        schema_name=schema_name,
        images=image
    )

    return result


@router.post("/pdf")
async def ollama_chat_pdf(
    model: str = Form(...),
    prompt: str = Form(...),
    schema_name: str = Form(...),
    pdf_file: UploadFile = File(...)
):

    filename = pdf_file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    pdf_bytes = await pdf_file.read()

    result = chat_with_pdf(
        model=model,
        prompt=prompt,
        schema_name=schema_name,
        pdf_bytes=pdf_bytes
    )

    return result