from pydantic import BaseModel, Field
from typing import Optional,List

class Standard(BaseModel):
    """
    你是一个中文标准信息结构化抽取助手，提取 markdown 格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    standard_name: Optional[str] = Field(None,description="标准的名称")
    standard_code: Optional[str] = Field(None,description="标准号,请抽取完整,格式为：DB45/T 1257—2015")

    standard_type: Optional[int] = Field(
        None,
        description=(
        "标准的类型,"
        "取值范围："
        "1=国家标准,2=行业标准,3=地方标准,4=团体标准"
        )
    )    
    standard_status: Optional[int] = Field(
        None,
        description=(
        "标准状态代码。"
        "取值范围："
        "1=发布,2=现行,3=废止"
        )
    )
    publish_date: Optional[str] = Field(None,description="发布时间,例如:2023年6月输出2023-06")
    implement_date: Optional[str] = Field(None,description="实施时间,例如:2023年6月输出2023-06")
    drafting_organizations: Optional[List[str]] = Field(default_factory=list,description="起草单位")
    drafters: Optional[List[str]] = Field(default_factory=list,description="起草人")