from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.service.files_parse_service import files_parse_service
from app.domain.build_schema import get_schema_model
from app.domain.task_config_factory import FilesTaskConfig_factory
from app.domain.errors import InvalidRequestError
from app.util.file_utils import upload_file_to_item
from app.api.models.schema_payload import SchemaPayload
import json

router = APIRouter(prefix="/files", tags=["files parse"])

@router.post("/parse")
async def parse(
    system_prompt: Optional[str] = Form(None),
    preprocess: Optional[str] = Form(None),
    postprocess: Optional[str] = Form(None),
    schema: str = Form(...),
    files: List[UploadFile] = File(...),
):
    if not files:
        raise InvalidRequestError(message="No files provided")

    #  解析 schema
    try:
        schema_payload = SchemaPayload.parse_json(schema)
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
        preprocess_dict = json.loads(preprocess) if preprocess else None
        postprocess_dict = json.loads(postprocess) if postprocess else None
    except json.JSONDecodeError as e:
        raise InvalidRequestError(
            message="Invalid preprocess or postprocess JSON",
            detail=str(e),
        ) from e

    #  自动装配 taskconfig
    taskconfig = FilesTaskConfig_factory(
        schema=schema_model,
        preprocess=preprocess_dict,
        postprocess=postprocess_dict,
        system_prompt=system_prompt,
    )

    # 文件读取 + 落盘
    uploaded_items = []
    for f in files:
        uploaded_items.append(await upload_file_to_item(upload_file=f))

    file_items = [u.item for u in uploaded_items]

    try:
        return await files_parse_service(
            taskconfig=taskconfig,
            file_items=file_items,
        )
    finally:
        for u in uploaded_items:
            await u.cleanup()
