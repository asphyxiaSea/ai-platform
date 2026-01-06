from pydantic import BaseModel, Field
from typing import List, Optional, Literal
class Patent(BaseModel):
    """
    你是一个专利信息结构化抽取助手，提取文本信息。
    """
    patent_name: Optional[str] = Field(
        None,
        description="专利名称"
    )

    patent_number: Optional[str] = Field(
        None,
        description="专利号"
    )

    patent_type: Optional[Literal[1, 2, 3, 4]] = Field(
        None,
        description="专利类型：1=PCT, 2=发明, 3=实用新型, 4=外观"
    )

    legal_status: Optional[Literal[1, 2, 3, 4, 5, 6]] = Field(
        None,
        description="专利状态：1=申请, 2=授权, 3=转让, 4=失效, 5=撤回, 6=驳回"
    )

    application_date: Optional[str] = Field(
        None,
        description="专利申请时间，输出格式：2022-05"
    )

    grant_date: Optional[str] = Field(
        None,
        description="专利授权时间，输出格式：2023-08"
    )

    project: Optional[str] = Field(
        None,
        description="专利依托项目名称"
    )

    inventors: Optional[List[str]] = Field(
        None,
        description="发明人列表，按原文顺序提取"
    )
