from pydantic import BaseModel, Field
from typing import List, Optional
class Patent(BaseModel):
    """
    你是一个中文专利信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    patent_name: str = Field(
        "",
        description="专利名称"
    )

    patent_type: Optional[int] = Field(
        None,
        description=(
        "专利类型代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=PCT，2=发明专利，3=实用新型专利，4=外观设计"
        )
    )

    legal_status: Optional[int] = Field(
        None,
        description=(
        "法律状态代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=申请，2=授权，3=转让，4=失效，5=撤回，6=驳回。"
        )
    )

    application_date: str = Field(
        "",
        description="申请时间，输出格式示例：2022-05、2022-05-12"
    )

    grant_date: str = Field(
        "",
        description="授权时间，未授权则为空字符串，输出格式示例：2023-08"
    )

    project: str = Field(
        "",
        description="依托项目名称，未识别到则为空字符串"
    )

    inventors: List[str] = Field(
        default_factory=list,
        description="发明人列表，按原文顺序提取"
    )
