import json
import httpx
from app.domain.resources.file_item import FileItem
from app.domain.marker import Marker, filter_noisy
from app.domain.errors import ExternalServiceError, InvalidRequestError
from app.infra.url_config import MARKER_EXTRACT_URL


async def extract_file(
    *,
    file_item: FileItem,
    marker: Marker | None = None,
) -> str:

    is_pdf = file_item.content_type == "application/pdf"
    is_image = file_item.content_type.startswith("image/")

    if not (is_pdf or is_image):
        raise InvalidRequestError(
            message="不支持的文件类型",
            detail=file_item.content_type,
        )

    data: dict[str, str] = {}

    # PDF 页面拆分已在服务层的 preprocess 完成，Marker 仅需传递 config 和 processor_list
    if marker is not None:
        data["config"] = json.dumps(marker.to_config(), ensure_ascii=False)

        processors = marker.to_processor_list()
        if processors:
            data["processor_list"] = json.dumps(processors, ensure_ascii=False)

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                MARKER_EXTRACT_URL,
                files={
                    "file": (file_item.filename, file_item.data, file_item.content_type)
                },
                data=data,
            )
            resp.raise_for_status()
            json_data = resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="Marker 服务异常",
            detail=str(exc),
        ) from exc

    text = json_data.get("text", "")
    return text if marker and not marker.filter_noisy else filter_noisy(text)
