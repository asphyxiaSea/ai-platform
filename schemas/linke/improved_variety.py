from pydantic import BaseModel, Field
from typing import Optional, Literal

class ImprovedVariety(BaseModel):
    """
    你是一个中文良种信息结构化抽取助手。
    """

    variety_name: Optional[str] = Field(None,description="良种名称")
    species: Optional[str] = Field(None,description="树种")
    variety_level: Optional[str] = Field(None,description="良种等级")
    variety_code: Optional[str] = Field(None,description="良种编号")
    variety_status: Optional[Literal[1, 2]] = Field(
        None,
        description=(
        "良种状态代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=原始取得，2=继受取得"
        )
    )
    approval_date: Optional[str] = Field(None,description="认定或审定日期")
    applicant: Optional[str] = Field(None,description="申请人")
    breeder: Optional[str] = Field(None,description="选育人")