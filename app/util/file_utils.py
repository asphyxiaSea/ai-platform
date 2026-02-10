import asyncio
import os
import tempfile
from dataclasses import dataclass
from fastapi import UploadFile
from app.domain.resources.file_item import FileItem


@dataclass(slots=True)
class UploadedFileItem:
    item: FileItem

    async def cleanup(self) -> None:
        if self.item.path:
            await asyncio.to_thread(os.remove, self.item.path)


async def upload_file_to_item(
    *,
    upload_file: UploadFile,
    persist_path: str | None = None,
) -> UploadedFileItem:
    filename = upload_file.filename or ""
    content_type = upload_file.content_type or ""

    path: str
    if persist_path:
        dir_path = os.path.dirname(persist_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        path = persist_path
    else:
        suffix = ""
        if filename:
            _, ext = os.path.splitext(filename)
            suffix = ext
        path = await asyncio.to_thread(_prepare_temp_path, suffix)

    data = await asyncio.to_thread(_stream_copy_to_path, upload_file, path)

    item = FileItem(
        filename=filename,
        content_type=content_type,
        data=data,
        path=path,
    )
    return UploadedFileItem(item=item)


def _prepare_temp_path(suffix: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        return tmp.name


def _stream_copy_to_path(upload_file: UploadFile, path: str) -> bytes:
    file_obj = upload_file.file
    try:
        file_obj.seek(0)
    except Exception:
        pass

    data = bytearray()
    with open(path, "wb") as f:
        while True:
            chunk = file_obj.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            data.extend(chunk)
    return bytes(data)
