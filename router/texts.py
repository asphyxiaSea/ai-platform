from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from service.text_service import chat_texts_pdfs_services


router = APIRouter(prefix="/ollama_api/chat/texts", tags=["ollama"])

@router.post("/pdfs")
async def chat_multimodal_pdfs(
    model: str = Form(...),
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

    result = chat_texts_pdfs_services(
        model=model,
        schema_name=schema_name,
        pdf_bytes_list=pdf_bytes_list
    )

    return result