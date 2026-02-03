import httpx
from app.domain.errors import ExternalServiceError, InvalidRequestError
from app.infra.url_config import FUNASR_TRANSCRIBE_PATH_URL


async def transcribe(
    *,
    file_path: str,
    model_key: str = "",
) -> str:

    if not file_path:
        raise InvalidRequestError(
            message="file_path 不能为空",
        )

    params: dict[str, str] = {"path": file_path}
    if model_key:
        params["model_key"] = model_key

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                FUNASR_TRANSCRIBE_PATH_URL,
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="FunASR 服务异常",
            detail=str(exc),
        ) from exc

    return data.get("text", "")
