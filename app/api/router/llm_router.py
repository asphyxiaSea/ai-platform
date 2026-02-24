from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.api.models.schema_payload import SchemaPayload
from app.domain.resources.build_schema import get_schema_model
from app.domain.errors import InvalidRequestError
from app.domain.templates.llm_chat.config import LLMTaskConfig_factory
from app.service.llm_service import llm_service
from app.util.file_utils import upload_file_to_item

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/structure")
async def structure_parse(
    system_prompt: Optional[str] = Form(None),
    user_prompt: str = Form(...),
    schema_payload_json: str = Form(...),
    image_files: Optional[List[UploadFile]] = File(None),
):

    try:
        schema_payload = SchemaPayload.parse_json(schema_payload_json)
    except Exception as e:
        raise InvalidRequestError(
            message="Invalid schema payload",
            detail=str(e),
        ) from e

    try:
        schema_model = get_schema_model(
            schema_name=schema_payload.schema_name,
            fields=schema_payload.fields,
        )
    except Exception as e:
        raise InvalidRequestError(
            message="Schema的格式不正确，检查字段类型及格式",
            detail=str(e),
        ) from e

    taskconfig = LLMTaskConfig_factory(
        schema=schema_model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    uploaded_items = []
    for f in image_files or []:
        uploaded_items.append(await upload_file_to_item(upload_file=f))

    file_items = [u.item for u in uploaded_items]

    try:
        return await llm_service(
            taskconfig=taskconfig,
            file_items=file_items,
        )
    finally:
        for u in uploaded_items:
            await u.cleanup()
