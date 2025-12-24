from pydantic import BaseModel, Field
from typing import List
class Patent(BaseModel):
    """
    你是一个专利信息结构化抽取助手。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    patent_name: str = Field(
        "",
        description="专利名称"
    )

    patent_type: str = Field(
        "",
        description="专利类型，例如：发明专利、实用新型专利、外观设计专利"
    )

    legal_status: str = Field(
        "",
        description="法律状态，例如：已授权、申请中、已公开、已失效"
    )

    application_date: str = Field(
        "",
        description="申请时间,例如:2022年5月、2022-05、2022-05-12"
    )

    grant_date: str = Field(
        "",
        description="授权时间,例如:2023年8月、2023-08;未授权则为空字符串"
    )

    project: str = Field(
        "",
        description="依托项目名称，例如：国家重点研发计划项目；无则为空字符串"
    )

    inventors: List[str] = Field(
        default_factory=list,
        description="发明人列表，按原文顺序提取"
    )
