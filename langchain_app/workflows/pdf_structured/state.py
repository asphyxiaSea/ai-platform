from __future__ import annotations

from typing import Any, TypedDict
from typing_extensions import NotRequired

from pydantic import BaseModel


class PdfStructuredState(TypedDict):
    pdf_path: str
    schema_model: type[BaseModel]
    system_prompt: NotRequired[str]
    extracted_text: NotRequired[str]
    structured_output: NotRequired[dict[str, Any]]
