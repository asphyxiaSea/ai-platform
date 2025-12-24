from pydantic import BaseModel, Field

class MonoGraph(BaseModel):
    """
    你是一个专著信息结构化抽取助手。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    title: str = Field("", description="专著名称")
    publisher: str = Field("", description="出版社名称")
    publication_date: str = Field("", description="出版时间,例如:2023年6月输出2023-06")
    isbn: str = Field("", description="书号(ISBN)")
    word_count: str = Field("", description="字数,以千为单位,例如:30千字,输出30")