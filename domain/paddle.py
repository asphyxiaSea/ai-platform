import httpx
from domain.file_item import FileItem

# class Paddle:
#     def __init__(
#         self, 
#         use_table_recognition: bool = False,
#         markdown_ignore_labels: list[str] | None = None,

#     ):


async def extract_file(
    *,
    file_item: FileItem,
) -> str:

    is_pdf = file_item.content_type == "application/pdf"
    is_image = file_item.content_type.startswith("image/")

    if not (is_pdf or is_image):
        raise ValueError(f"Unsupported file type: {file_item.content_type}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            "http://localhost:8003/paddle/pp-structurev3/predict",
            files={
                "file": (file_item.filename, file_item.data, file_item.content_type)
            },
        )
        resp.raise_for_status()
        data = resp.json()

    text = data.get("markdown_text", "")
    return text


