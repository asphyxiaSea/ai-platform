from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from service.ollama_chat_service import chat_with_pdf,chat_text_only,chat_with_images

router = APIRouter(prefix="/api/ollama/chat", tags=["ollama"])

@router.post("/text")
async def ollama_chat_text(
    model: str = Form(...),
    prompt: str = Form(...)
):
    content = chat_text_only(
        model=model,
        prompt=prompt
    )
    return {"content": content}

@router.post("/chat/images")
async def ollama_chat_images(
    model: str = Form(...),
    prompt: str = Form(...),
    images: List[UploadFile] = File(...)
):
    image_bytes_list: List[bytes] = []

    for img in images:
        content_type = img.content_type
        if not content_type or not content_type.startswith("image/"):
            raise HTTPException(400, f"{img.filename} is not an image")

        image_bytes_list.append(await img.read())

    content = chat_with_images(
        model=model,
        prompt=prompt,
        images_bytes=image_bytes_list
    )

    return {"content": content}


@router.post("/pdf")
async def ollama_chat_pdf(
    model: str = Form(...),
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    pdf_bytes = await file.read()

    content = chat_with_pdf(
        model=model,
        prompt=prompt,
        pdf_bytes=pdf_bytes
    )

    return {"content": content}