from pydantic import BaseModel, Field
from typing import Optional,List, Literal

class NewVarieties(BaseModel):
    """
    你是一个中文新品种信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    variety_name: Optional[str] = Field(
        None, description="品种名称"
    )

    species: Optional[str] = Field(
        None,
        description="所属的种和属"
    )
    variety_type: Literal[1, 2] = Field(
        description="品种类型,一般英文都是国际登录新品种,1=新品种、2=国际登录新品种"
    )
    variety_right_number: Optional[str] = Field(
        None,
        description="品种权号（植物新品种权号）"
    )
    variety_status: Optional[int] = Field(
        None,
        description=(
            "品种状态代码。"
            "取值范围："
            "1=申请，2=授权，3=转让"
        )
    )
    application_date: Optional[str] = Field(
        None,
        description="申请日期,输出格式如：2022-03-15、2022-03"
    )
    grant_date: Optional[str] = Field(
        None,
        description="授权日期,输出格式如：2022-03-15、2022-03"
    )
    variety_right_holder: Optional[str] = Field(
        None,
        description="品种权人（单位或个人）"
    )
    breeders: Optional[List[str]] = Field(
        default_factory=list,
        description="选育人列表，按原文顺序提取"
    )
