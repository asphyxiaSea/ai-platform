import json

from fastapi import APIRouter, File, Form, UploadFile

from app.domain.errors import InvalidRequestError
from app.domain.templates.sam3.config import Sam3TaskConfig_factory
from app.service.sam3_service import sam3_service
from app.util.file_utils import upload_file_to_item


router = APIRouter(prefix="/sam3", tags=["sam3"])


@router.post("/height-measure")
async def height_measure(
    image_file: UploadFile = File(...),
    reference_config: str = Form(...),
    target_config: str = Form(...),
):
    if not image_file:
        raise InvalidRequestError(message="No image_file provided")

    try:
        reference_config_data = json.loads(reference_config)
        target_config_data = json.loads(target_config)
    except json.JSONDecodeError as e:
        raise InvalidRequestError(
            message="Invalid reference_config or target_config JSON",
            detail=str(e),
        ) from e

    reference_texts = reference_config_data.get("texts")
    target_texts = target_config_data.get("texts")
    if not isinstance(reference_texts, list):
        raise InvalidRequestError(
            message="reference_config.texts must be a list",
            detail=reference_texts,
        )
    if not isinstance(target_texts, list):
        raise InvalidRequestError(
            message="target_config.texts must be a list",
            detail=target_texts,
        )

    ruler_real_height = reference_config_data.get("ruler_real_height")
    if not isinstance(ruler_real_height, (int, float)):
        raise InvalidRequestError(
            message="reference_config.ruler_real_height must be a number",
            detail=ruler_real_height,
        )
    if ruler_real_height <= 0:
        raise InvalidRequestError(
            message="reference_config.ruler_real_height must be > 0",
            detail=ruler_real_height,
        )

    # 该字段仅用于本地高度换算，不应透传给 Sam3 外部分割服务。
    reference_seg_config = dict(reference_config_data)
    reference_seg_config.pop("ruler_real_height", None)

    uploaded = await upload_file_to_item(upload_file=image_file)
    try:
        taskconfig = Sam3TaskConfig_factory(
            reference_config=reference_seg_config,
            target_config=target_config_data,
            ruler_real_height=float(ruler_real_height),
        )
        return await sam3_service(
            file_item=uploaded.item,
            taskconfig=taskconfig,
        )
    finally:
        await uploaded.cleanup()
