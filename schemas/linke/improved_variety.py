from pydantic import BaseModel, Field
from typing import Optional, Literal,List

class ImprovedVariety(BaseModel):
    """
    你是一个中文良种信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
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
    breeder: Optional[List[str]] = Field(None,description="选育人,注意：有些文本种选育人是用、隔开")

