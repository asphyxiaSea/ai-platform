from pydantic import BaseModel, Field

class Standard(BaseModel):
    """
    你是一个中文标准信息结构化抽取助手，提取 markdown 格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    standard_name: str = Field("", description="标准名称")
    standard_code: str = Field("", description="标准号")
    standard_type: str = Field("", description="标准类型")
    standard_status: str = Field("", description="标准状态")
    publish_date: str = Field("", description="发布时间,例如:2023年6月输出2023-06")
    implement_date: str = Field("", description="实施时间,例如:2023年6月输出2023-06")
    drafting_organizations: str = Field("", description="起草单位")
    drafters: str = Field("", description="起草人")