from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List,Optional
from service.extract_service import extract_service
from domain import FileItem
from domain.build_schema import build_pydantic_schema
from domain.task_config_factory import TaskConfig_factory
from pydantic import BaseModel
from domain.preprocess import pdf_preprocess
import json

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
    system_prompt: Optional[str] = Form(None), 
    preprocess: Optional[str] = Form(None),  
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
    # 前处理
    try:
        preprocess_dict = json.loads(preprocess) if preprocess else None
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid preprocess JSON: {e}")


   #  自动装配 taskconfig 
    taskconfig = TaskConfig_factory(schema=schema_model,preprocess=preprocess_dict)

    # 文件读取
    file_items: list[FileItem] = []

    for f in files:
        data = await f.read()

        # === PDF 前处理（仅此处使用 preprocess）===
        if f.content_type == "application/pdf":
            data = pdf_preprocess(
                pdf_bytes=data,
                preprocess=taskconfig.preprocess,
            )

        file_items.append(
            FileItem(
                filename=f.filename or "",
                content_type=f.content_type or "",
                data=data,
            )
        )

    return await extract_service(
        taskconfig=taskconfig,
        file_items=file_items,
    )

