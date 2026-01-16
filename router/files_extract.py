from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from service.extract_service import extract_service
from domain import FileItem
from domain.build_schema import build_pydantic_schema
from domain.task_config_factory import TaskConfig_factory
from pydantic import BaseModel

router = APIRouter(prefix="/files", tags=["files parse"])

class SchemaPayload(BaseModel):
    schema_name: str
    fields: list[dict]

def clean_text(s: str) -> str:
    return (
        s.replace("\u00a0", " ")
         .replace("\u200b", "")
         .replace("\ufeff", "")
    )

@router.post("/parse")
async def parse(
    system_prompt: str | None = Form(None),
    schema: str = Form(...),
    files: List[UploadFile] = File(...),
):
    if not files:
        raise HTTPException(400, "No files provided")
    
    schema = clean_text(schema)

    #  解析 schema
    try:
        schema_payload = SchemaPayload.model_validate_json(schema)
    except Exception as e:
        raise HTTPException(400, f"Invalid schema payload: {e}")

    #  自动装配 Schema
    schema_model = build_pydantic_schema(
        schema_name=schema_payload.schema_name,
        fields=schema_payload.fields,
    )

   #  自动装配 taskconfig 
    taskconfig = TaskConfig_factory(schema=schema_model)

    # 文件读取
    file_items: list[FileItem] = [
        FileItem(
            filename=f.filename or "",
            content_type=f.content_type or "",
            data=await f.read(),
        )
        for f in files
    ]

    # 交给 service
    return await extract_service(
        taskconfig = taskconfig,
        file_items=file_items,
    )

