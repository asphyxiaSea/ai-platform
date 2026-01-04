from pydantic import BaseModel, Field
from typing import Optional

class MonoGraph(BaseModel):
    """
    你是一个中文专著信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    title: Optional[str] = Field(None,description="专著名称")
    publisher: Optional[str] = Field(None,description="出版社名称")
    publication_date: Optional[str] = Field(None,description="出版时间,例如:2023年6月输出2023-06")
    isbn: Optional[str] = Field(None,description="书号(ISBN)")
    word_count: Optional[str] = Field(None,description="字数,以千为单位,例如:30千字,输出30")