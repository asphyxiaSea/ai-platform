import json

import httpx

from app.domain.errors import ExternalServiceError, InvalidRequestError
from app.domain.file_item import FileItem
from app.infra.url_config import SAM3_IMAGE_SEGMENT_TEXTS_URL


async def sam3_segment_instance_texts(
    *,
    file_item: FileItem,
    config_data: dict,
):
    is_image = file_item.content_type.startswith("image/")
    if not is_image:
        raise InvalidRequestError(
            message="不支持的文件类型",
            detail=file_item.content_type,
        )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                SAM3_IMAGE_SEGMENT_TEXTS_URL,
                files={
                    "image_file": (
                        file_item.filename,
                        file_item.data,
                        file_item.content_type,
                    )
                },
                data={
                    "config": json.dumps(config_data, ensure_ascii=False),
                },
            )
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="Sam3 服务异常",
            detail=str(exc),
        ) from exc
