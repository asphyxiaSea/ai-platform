from __future__ import annotations

from dataclasses import dataclass
from fastapi import UploadFile
from app.domain.file_item import FileItem


@dataclass(slots=True)
class IncomingFile:
    filename: str
    content_type: str
    data: bytes

    @classmethod
    async def from_upload_file(cls, upload_file: UploadFile) -> "IncomingFile":
        data = await upload_file.read()
        return cls(
            filename=upload_file.filename or "",
            content_type=upload_file.content_type or "",
            data=data,
        )

    def to_file_item(self) -> FileItem:
        return FileItem(
            filename=self.filename,
            content_type=self.content_type,
            data=self.data,
        )
