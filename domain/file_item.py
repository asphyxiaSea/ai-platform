from typing import Literal
from pydantic import BaseModel


class FileItem(BaseModel):
    filename: str
    content_type: str
    data: bytes