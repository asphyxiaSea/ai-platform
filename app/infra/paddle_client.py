import httpx
from app.domain.resources.file_item import FileItem
from app.domain.errors import ExternalServiceError, InvalidRequestError
from app.infra.url_config import PADDLE_EXTRACT_PATH_URL


async def extract_file(
    *,
    file_item: FileItem,
) -> str:

    is_pdf = file_item.content_type == "application/pdf"
    is_image = file_item.content_type.startswith("image/")

    if not (is_pdf or is_image):
        raise InvalidRequestError(
            message="不支持的文件类型",
            detail=file_item.content_type,
        )

    if not file_item.path:
        raise InvalidRequestError(
            message="file_path 不能为空",
        )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                PADDLE_EXTRACT_PATH_URL,
                params={
                    "pipeline": "default",
                    "path": file_item.path,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="Paddle 服务异常",
            detail=str(exc),
        ) from exc

    text = data.get("markdown_text", "")
    return text
