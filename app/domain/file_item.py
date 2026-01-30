from pydantic import BaseModel
from typing import Optional


class FileItem(BaseModel):
    filename: str
    """原始文件名"""

    content_type: str
    """MIME 类型，如 application/pdf"""

    data: bytes
    """文件二进制内容"""

    language: Optional[str] = None
    """文件内容的语言代码（ISO 639-1 / BCP-47）
    示例:
        - "zh"
        - "en"
        - "ja"
        - "zh-CN"
    None 表示未知 / 自动检测
    """
