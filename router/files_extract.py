from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List,Optional
from service.extract_service import extract_service
from domain.file_item import FileItem
from domain.build_schema import get_schema_model
from domain.task_config_factory import TaskConfig_factory
from pydantic import BaseModel
import json

router = APIRouter(prefix="/files", tags=["files parse"])

class SchemaPayload(BaseModel):
    schema_name: str
    fields: list[dict]

# 防止schema错误空格
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
    postprocess: Optional[str] = Form(None), 
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

    try:
        # 自动装配 Schema
        schema_model = get_schema_model(
            schema_name=schema_payload.schema_name,
            fields=schema_payload.fields,
        )
    except Exception as e:
        # 捕获 get_schema_model 内部可能抛出的所有错误
        raise HTTPException(
            status_code=400,
            detail=f"Schema的格式不正确，检查字段类型及格式: {e}"
        )
    # 前处理
    try:
        preprocess_dict = json.loads(preprocess) if preprocess else None
        postprocess_dict = json.loads(postprocess) if postprocess else None
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid preprocess or postprocess JSON: {e}")


   #  自动装配 taskconfig
    taskconfig = TaskConfig_factory(schema=schema_model,preprocess=preprocess_dict,
                                    postprocess=postprocess_dict,system_prompt=system_prompt)

    # 文件读取
    file_items: list[FileItem] = []

    for f in files:
        data = await f.read()
        
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

