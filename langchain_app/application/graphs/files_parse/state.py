from __future__ import annotations

from operator import add
from typing import Annotated, Any, TypedDict

from app.domain.file_item import FileItem


class TraceItem(TypedDict):
    node: str
    status: str
    duration_ms: float
    summary: dict[str, Any]


class FilesParseState(TypedDict, total=False):
    file_items: list[FileItem]
    texts: list[str]
    result: dict[str, Any]
    trace: Annotated[list[TraceItem], add]
