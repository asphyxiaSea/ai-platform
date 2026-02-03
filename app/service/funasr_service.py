from app.domain.file_item import FileItem
from app.infra.funasr_client import transcribe


async def transcribe_service(
    *,
    file_item: FileItem,
    model_key: str = "",
) -> dict[str, str]:
    text = await transcribe(file_path=file_item.path or "", model_key=model_key)
    return {"text": text}
