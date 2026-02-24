from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.service.files_parse_service import files_parse_service
from app.domain.resources.build_schema import get_schema_model
from app.domain.templates.files_parse.config import FilesTaskConfig
from app.domain.errors import InvalidRequestError
from app.util.file_utils import upload_file_to_item
from app.api.models.schema_payload import SchemaPayload
import json

router = APIRouter(prefix="/files", tags=["files parse"])

@router.post("/parse")
async def parse(
    system_prompt: Optional[str] = Form(None),
    pdf_process: Optional[str] = Form(None),
    text_process: Optional[str] = Form(None),
    schema_payload_json: str = Form(...),
    files: List[UploadFile] = File(...),
):
    if not files:
        raise InvalidRequestError(message="No files provided")

    #  解析 schema
    try:
        schema_payload = SchemaPayload.parse_json(schema_payload_json)
    except Exception as e:
        raise InvalidRequestError(
            message="Invalid schema payload",
            detail=str(e),
        ) from e

    try:
        # 自动装配 Schema
        schema_model = get_schema_model(
            schema_name=schema_payload.schema_name,
            fields=schema_payload.fields,
        )
    except Exception as e:
        # 捕获 get_schema_model 内部可能抛出的所有错误
        raise InvalidRequestError(
            message="Schema的格式不正确，检查字段类型及格式",
            detail=str(e),
        ) from e
    # 前处理
    try:
        preprocess_dict = json.loads(pdf_process) if pdf_process else None
        postprocess_dict = json.loads(text_process) if text_process else None
    except json.JSONDecodeError as e:
        raise InvalidRequestError(
            message="Invalid pdf_process or text_process JSON",
            detail=str(e),
        ) from e

    config = FilesTaskConfig(
        schema=schema_model,
        system_prompt=system_prompt,
        pdf_process=preprocess_dict,
        text_process=postprocess_dict,
    )

    # 文件读取 + 落盘
    uploaded_items = []
    for f in files:
        uploaded_items.append(await upload_file_to_item(upload_file=f))

    file_items = [u.item for u in uploaded_items]

    try:
        return await files_parse_service(
            config=config,
            file_items=file_items,
        )
    finally:
        for u in uploaded_items:
            await u.cleanup()
